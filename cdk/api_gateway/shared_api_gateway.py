
from aws_cdk import (
    Stack,
    Environment,
    aws_certificatemanager,
    aws_lambda,
    aws_apigateway,
    Aws
)
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
                 *, env: Environment, create_dns: bool, 
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
        
        # Deploy the api to a stage
        stage_name: str = f"{stage}"
        self.deploy_api_stage(stage_name)

        # Create a usage plan for the stage
        plan_name: str = "SharedAPIAdminPlan"
        self.create_usage_plan(plan_name)

        # Add an api key to the usage plan
        key_name: str = "SharedAPIAdminKey"
        self.api_key = self.api.add_api_key(key_name)
        self.plan.add_api_key(self.api_key)


    def create_rest_api(self):

        # Create the Rest API
        self.api = aws_apigateway.RestApi(self, 'SharedApiGateway')

        # Handle dns integration
        if self.create_dns:
            domain_name = self.zones.api.zone_name
            # certificate = aws_certificatemanager.DnsValidatedCertificate(self, 'ApiGatewayCert',
            #                                                              domain_name=domain_name,
            #                                                              hosted_zone=self.zones.api)
            
            # Reference an existing certificate
            existing_certificate_arn = f"arn:aws:acm:{Aws.REGION}:{Aws.ACCOUNT_ID}:certificate/f002de99-9a60-48c4-8744-4a1e18424840"
            certificate = aws_certificatemanager.Certificate.from_certificate_arn(
                self, 'ExistingApiCertificate', existing_certificate_arn
            )

            # self.api.add_domain_name('ApiGatewayDomainName',
            #                          domain_name=domain_name,
            #                          certificate=certificate)
            
            # Add a domain name to the API
            self.api_domain_name = aws_apigateway.DomainName(
                self,
                "ExistingApiDomainName",
                domain_name=domain_name,
                certificate=certificate
            )

            # Reference the existing API Gateway Domain Name
            # self.api_domain_name = aws_apigateway.DomainName.from_domain_name_attributes(
            #     self,
            #     "ExistingApiDomainName",
            #     domain_name=domain_name,
            #     domain_name_alias_hosted_zone_id="Z02880721JJ9EMQ8VFEV3",
            #     domain_name_alias_target=f"d-6fxcutcsv0.execute-api.{Aws.REGION}.amazonaws.com."
            # )
            
            # Associate the existing domain with the new Rest API using BasePathMapping
            aws_apigateway.BasePathMapping(
                self,
                "BasePathMapping",
                domain_name=self.api_domain_name,
                rest_api=self.api,
            )


    def deploy_api_stage(self, stage_name: str = "prod"):
        self.stage = aws_apigateway.Stage(
            self, id=stage_name,
            deployment=self.api.latest_deployment,
            stage_name=stage_name,
        )

    
    def create_usage_plan(self, plan_name: str = "UsagePlan"):
        self.plan = self.api.add_usage_plan(
            plan_name,
            name=plan_name,
            throttle=aws_apigateway.ThrottleSettings(
                rate_limit=50,
                burst_limit=10
            )
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
        self.users.add_method('POST', users_handler, api_key_required=True)
    

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
        self.equipment.add_method('POST', equipment, api_key_required=True)
        
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
        self.qualifications_user_id.add_method('PATCH', qualifications_user_id, api_key_required=True)
