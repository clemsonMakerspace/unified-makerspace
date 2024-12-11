
from aws_cdk import (
    Stack,
    Environment,
    aws_certificatemanager,
    aws_lambda,
    aws_apigateway,
    aws_iam,
    custom_resources,
    Aws,
    PhysicalName,
    Duration
)

import boto3
import json
from pathlib import Path
import os

from constructs import Construct
from dns import MakerspaceDns


class SharedApiGateway(Stack):
    """
    Amazon API Gateway for all Lambdas, will be fronted by `api.cumaker.space`.

    Structure
    ---

    Each API that integrates with this stack needs to be imported as a Lambda
    function. For now there's only four, but eventually we should pass them
    in in some more structured way.

    Each lambda is a method handler thats maps to a resource and is expected to
    parse and call the appropriate methods to handle the request.

    For example, consider the resource '/users'. There should the utilized lambda
    must handle all of the method requests for it -- e.g., GET /users -- as well
    as handle all requests for sub-resources -- e.g., GET /users/{UserID}.

    Authorization
    ---

    This API Gateway uses API keys for authorization, but cognito authorizers may
    be considered soon. The only authorizer we would care about is the cognito pool
    that keeps track of makerspace employees (and CUCourse).
    """

    def __init__(self, scope: Construct, stage: str,
                user: aws_lambda.Function, visits: aws_lambda.Function,
                 qualifications: aws_lambda.Function, equipment: aws_lambda.Function,
                 tiger_training: aws_lambda.Function,
                 *, backend_api_key: str = None, 
                 env: Environment, create_dns: bool, 
                zones: MakerspaceDns = None):

        super().__init__(scope, 'SharedApiGateway', env=env)

        self.create_dns = create_dns
        self.zones = zones

        self.create_rest_api()

        # Scheme of "..._user_id" indicates routing for endpoints with
        # the path parameter {user_id}

        # /user routing
        self.route_users(user)
        self.route_users_user_id(user)

        # /visits routing
        self.route_visits(visits)
        self.route_visits_user_id(visits)

        # /equipment routing
        self.route_equipment(equipment)
        self.route_equipment_user_id(equipment)

        # /qualifications routing
        self.route_qualifications(qualifications)
        self.route_qualifications_user_id(qualifications)

        # /tiger_training routing
        self.route_tiger_training(tiger_training)
        
        # Deploy the api to a stage
        stage_name: str = f"{stage}"
        self.deploy_api_stage(stage_name)

        # Create a usage plan for the stage
        plan_name: str = "SharedAPIAdminPlan"
        self.create_usage_plan(plan_name)

        # Handle api key
        api_key_name: str = "SharedAPIAdminKey"

        # Create a Lambda function to delete an api key if it exists
        self.api_key_checker_lambda()

        # Allow the api key checker to get api keys
        self.checker_get_all_keys_role = aws_iam.PolicyStatement(
            actions=["apigateway:GET"],
            resources=[f"arn:aws:apigateway:{self.region}::/apikeys/*"]  # Adjust resource scoping if necessary
        )

        # Allow the api key checker to delete api keys
        self.checker_delete_any_key_role = aws_iam.PolicyStatement(
            actions=["apigateway:DELETE"],
            resources=[f"arn:aws:apigateway:{self.region}::/apikeys/*"]  # Adjust resource scoping if necessary
        )

        # Sanity IAM role
        self.alt_checker_get_all_keys_role = aws_iam.PolicyStatement(
            actions=["apigateway:GET"],
            resources=[f"arn:aws:apigateway:{self.region}::/apikeys"]  # Adjust resource scoping if necessary
        )

        self.lambda_api_key_checker.role.add_to_policy(self.checker_get_all_keys_role)
        self.lambda_api_key_checker.role.add_to_policy(self.checker_delete_any_key_role)
        self.lambda_api_key_checker.role.add_to_policy(self.alt_checker_get_all_keys_role)
        
        # Create an IAM Role for the AwsCustomResource
        custom_resource_role = aws_iam.Role(
            self, "CustomResourceRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "InvokeLambdaPolicy": aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            actions=["lambda:InvokeFunction"],
                            resources=[self.lambda_api_key_checker.function_arn]
                        )
                    ]
                )
            }
        )


        # Use the custom resource to call the api key checker
        # (and delete any matching api key with the same name)
        custom_resource = custom_resources.AwsCustomResource(
            self, "ApiKeyRetriever",
            on_create=custom_resources.AwsSdkCall(
                service="Lambda",
                action="invoke",
                parameters={
                    "FunctionName": self.lambda_api_key_checker.function_name,
                    "Payload": json.dumps({"ApiKeyName": api_key_name})  # Serialize payload as JSON
                },
                physical_resource_id=custom_resources.PhysicalResourceId.of(api_key_name)
            ),
            policy=custom_resources.AwsCustomResourcePolicy.from_sdk_calls(resources=custom_resources.AwsCustomResourcePolicy.ANY_RESOURCE),
            role=custom_resource_role,  # Attach the role to the custom resource
        )

        # Create a new API Key
        self.api_key = self.api.add_api_key(
            "SharedAPIKey",
            api_key_name=api_key_name,
            value=backend_api_key
        )

        # Add the api key to the usage plan
        self.plan.add_api_key(self.api_key)

        # WARNING:
        # The following is a band-aid patch that should be fixed in the future.
        # With the implementation of api key and the need for the STATIC frontend
        # to be able to use the backend api, the need to statically store the
        # backend api key is a thing. This, unfortunately, means that any method
        # that requires the api key will visibly show this in network traffic.
        # As such, while the frontend remains static, the api key should be used
        # behind the Amplify login page to reduce the chance of security risk of
        # leaking the key. This also means that the SharedAPIGateway stack MUST
        # be created before the Visit stack to ensure the api key is written to
        # the right location before the s3 bucket is deployed.

        # Config filename
        config_filename: str = ".env"

        # Data to store
        data: str = f"BACKEND_KEY={backend_api_key}"

        # Path to the file to write the data to
        # Assumes directory structure is cdk/visit/console/{stage_name} and the CWD
        # is 'cdk'
        config_path: Path = Path(f"{os.getcwd()}/visit/console/{stage_name}/{config_filename}")

        # Write data to the file
        with open(config_path, "w") as outfile:
            outfile.write(data)


    def create_rest_api(self):

        # Create the Rest API
        self.api = aws_apigateway.RestApi(self, 'SharedApiGateway')

        # Handle dns integration
        if self.create_dns:
            domain_name = self.zones.api_hosted_zone.zone_name
            self.url: str = f"https://{domain_name}"
            # Depreciated way of making certificate
            # certificate = aws_certificatemanager.DnsValidatedCertificate(self, 'ApiGatewayCert',
            #                                                              domain_name=self.domains.api,
            #                                                              hosted_zone=self.api)

            certificate = aws_certificatemanager.Certificate(
                self, 'ApiGatewayCert',
                domain_name=domain_name,
                validation=aws_certificatemanager.CertificateValidation.from_dns(self.zones.api_hosted_zone)
            )

            self.api.add_domain_name('ApiGatewayDomainName',
                                     domain_name=domain_name,
                                     certificate=certificate)

    def deploy_api_stage(self, stage_name: str = "Prod"):
        if not self.api.latest_deployment:
            deployment = aws_apigateway.Deployment(self, 'ApiDeployment', api=self.api)
        else:
            deployment = self.api.latest_deployment

        self.stage = aws_apigateway.Stage(
            self, id=stage_name,
            deployment=deployment,
            stage_name=stage_name,
        )

    
    def create_usage_plan(self, plan_name: str = "UsagePlan"):
        self.plan = self.api.add_usage_plan(
            plan_name,
            name=plan_name,
            throttle=aws_apigateway.ThrottleSettings(
                rate_limit=50,
                burst_limit=10
            ),
            api_stages=[
                aws_apigateway.UsagePlanPerApiStage(
                    stage=self.stage
                )
            ]
        )


    """
    Users:

    Used to manage the information for each user. Can get every
    users' information, add a new user, get a specific user's
    information, and update a user's information.

    Endpoints:
    /users
      - GET
      - POST

    /users/{user_id}
      - GET
      - PATCH
    """
    def route_users(self, users: aws_lambda.Function):

        # create resource '/users'
        users_handler = aws_apigateway.LambdaIntegration(users)
        self.users = self.api.root.add_resource('users')

        # methods
        self.users.add_method('GET', users_handler, api_key_required=True)
        self.users.add_method('POST', users_handler)
    

    def route_users_user_id(self, users: aws_lambda.Function):
        
        # adds a path parameter '{user_id}' to /users
        users_handler = aws_apigateway.LambdaIntegration(users)
        self.users_user_id = self.users.add_resource('{user_id}')

        # methods
        self.users_user_id.add_method('GET', users_handler, api_key_required=True)
        self.users_user_id.add_method('PATCH', users_handler, api_key_required=True)
    

    """
    Visits:

    Used to track visits. Can get all visits, add a new visit,
    and retrieve visits by users and timestamps.

    Endpoints:
    /visits
      - GET
      - POST

    /visits/{user_id}
      - GET
    """
    def route_visits(self, visits: aws_lambda.Function):

        # create resource '/visits'
        visits_handler = aws_apigateway.LambdaIntegration(visits)
        self.visits = self.api.root.add_resource('visits')

        # methods
        self.visits.add_method('GET', visits_handler, api_key_required=True)
        self.visits.add_method('POST', visits_handler, api_key_required=True)

    def route_visits_user_id(self, visits: aws_lambda.Function):
        
        # adds a path parameter '{user_id}' to /visits
        visits_user_id = aws_apigateway.LambdaIntegration(visits)
        self.visits_user_id = self.visits.add_resource('{user_id}')

        # methods
        self.visits_user_id.add_method('GET', visits_user_id, api_key_required=True)


    """
    Equipment

    Used to manage storing, retrieving, and updating equipment usage
    logs gathered from the equipment usage form. Can retrieve all
    equipment data, add a new entry based on a submission, get the
    equipment logs by user and timestamps, and update any equipment
    log relating to a user (given a timestamp or the latest without one).

    Endpoints:
    /equipment
      - GET
      - POST

    /equipment/{user_id}
      - GET
      - PATCH
    """
    def route_equipment(self, equipment: aws_lambda.Function):

        # create resource '/equipment'
        equipment = aws_apigateway.LambdaIntegration(equipment)
        self.equipment = self.api.root.add_resource('equipment')

        # methods
        self.equipment.add_method('GET', equipment, api_key_required=True)
        self.equipment.add_method('POST', equipment)
        
    def route_equipment_user_id(self, equipment: aws_lambda.Function):
        
        # adds a path parameter '{user_id}' to /equipment
        equipment_user_id = aws_apigateway.LambdaIntegration(equipment)
        self.equipment_user_id = self.equipment.add_resource('{user_id}')

        # methods
        self.equipment_user_id.add_method('GET', equipment_user_id, api_key_required=True)
        self.equipment_user_id.add_method('PATCH', equipment_user_id, api_key_required=True)


    """
    Qualifications

    Used to track a user's progress on the Tiger Training program, specifically
    any training courses and waivers. Can get all qualifications for every user,
    add a new user to the qualifications table, get a specific user's qualifications,
    and update a user's qualifications.

    Endpoints:
    /qualifications
      - GET
      - POST

    /qualifications/{user_id}
      - GET
      - PATCH
    """
    def route_qualifications(self, qualifications: aws_lambda.Function):

        # create resource '/qualifications'
        qualifications = aws_apigateway.LambdaIntegration(qualifications)
        self.qualifications = self.api.root.add_resource('qualifications')

        # methods
        self.qualifications.add_method('GET', qualifications, api_key_required=True)
        self.qualifications.add_method('POST', qualifications, api_key_required=True)
        
    def route_qualifications_user_id(self, qualifications: aws_lambda.Function):
        
        # adds a path parameter '{user_id}' to /qualifications
        qualifications_user_id = aws_apigateway.LambdaIntegration(qualifications)
        self.qualifications_user_id = self.qualifications.add_resource('{user_id}')

        # methods
        self.qualifications_user_id.add_method('GET', qualifications_user_id, api_key_required=True)


    """
    Tiger Training

    Used to pull data from Tiger Training and store it to the backend using the
    necessary endpoints. Admittedly, this isn't the prettiest solution, but it
    is necessary to achieve the desired end goal of pressing a button on the
    frontend and automatically pulling/storing new course completions.

    Endpoints:
    /tiger_training
      - ANY
    """
    def route_tiger_training(self, tiger_training: aws_lambda.Function):

        # create resource '/tiger_training'
        tiger_training = aws_apigateway.LambdaIntegration(tiger_training)
        self.tiger_training = self.api.root.add_resource('tiger_training')

        # methods
        self.tiger_training.add_method('ANY', tiger_training, api_key_required=True)
    

    def api_key_checker_lambda(self):
        #self.lambda_api_key_checker = aws_lambda.Function(
        #    self,
        #    'ApiKeyChecker',
        #    function_name=PhysicalName.GENERATE_IF_NEEDED,
        #    code=aws_lambda.Code.from_asset('api_gateway/lambda_code/api_key_checker'),
        #    handler='api_key_checker.handler',
        #    timeout=Duration.seconds(15),
        #    runtime=aws_lambda.Runtime.PYTHON_3_12)

        # Create a Lambda function to query for an API Key
        self.lambda_api_key_checker = aws_lambda.Function(
            self, "ApiKeyCheckerFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            timeout=Duration.seconds(15),
            code=aws_lambda.Code.from_inline("""
import boto3
import logging
import json
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def delete_key(client, api_key_name: str) -> bool:

    deleted_key: bool = False

    response = client.get_api_keys(includeValues=False)

    # Check for matching key name
    for key in response['items']:
        if key['name'] == api_key_name:

            # Delete the key
            try:
                client.delete_api_key(apiKey=key['id'])
                logger.info(f"Deleted key '{key['id']}'")
                deleted_key = True
            except Exception as e:
                raise Exception(f"Error deleting API Key: {e}")

    return deleted_key

def handler(event, context):

    logger.info("Event:")
    logger.info(json.dumps(event, indent=2))
    
    try:
        client = boto3.client('apigateway')

        if 'ApiKeyName' not in event:
            raise Exception("Missing 'ApiKeyName' from event input fields.")

        api_key_name = event['ApiKeyName']

        # Try and delete the key
        delete_key(client, api_key_name)

        # Wait 5 seconds for changes to propagate
        time.sleep(5)

        # Ensure key was deleted (delete_key should return False for no key deleted)
        key_deleted: bool = delete_key(client, api_key_name)

        if key_deleted:
            raise Exception(f"Api key still existed after deleting first time.")

        return {}

    except Exception as e:
        raise Exception(f"Error occurred: {e}")
            """),
        )
