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
    The SharedApiGateway stack sets up an Amazon API Gateway to manage API requests 
    for multiple Lambda functions. The gateway is fronted by a custom domain 
    (e.g., `api.cumaker.space`) and serves as a centralized interface for all backend services.

    Purpose
    ---
    This API Gateway integrates with various Lambda functions, each responsible for a specific 
    resource and its associated methods. It provides a RESTful interface where each Lambda 
    acts as a method handler for its respective resource. For example:
    - A Lambda function handling `/users` must process all HTTP methods for this resource 
      (e.g., GET /users, POST /users) as well as its sub-resources (e.g., GET /users/{user_id}).

    Structure
    ---
    The API Gateway is organized into the following resources and paths:
    - `/users`: Manage user information (GET, POST).
    - `/users/{user_id}`: Retrieve and update specific user information (GET, PATCH).
    - `/visits`: Track visits to the Makerspace (GET, POST).
    - `/visits/{user_id}`: Retrieve visits for a specific user (GET).
    - `/equipment`: Manage equipment usage logs (GET, POST).
    - `/equipment/{user_id}`: Retrieve or update equipment logs for a specific user (GET, PATCH).
    - `/qualifications`: Track Tiger Training qualifications (GET, POST).
    - `/qualifications/{user_id}`: Retrieve or update a user's qualifications (GET, PATCH).
    - `/tiger_training`: Interact with Tiger Training data (ANY).

    Authorization
    ---
    - The API uses API keys for authorization.
    - Future plans include integrating Cognito authorizers for Makerspace employees and CUCourse.

    Future Improvements
    ---
    Automating the creation of a usage plan and API key is currently not implemented due to time 
    constraints and challenges with recreating keys. These remain as manual steps for now.

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - stage (str): The deployment stage (e.g., "prod", "beta").
    - user (aws_lambda.Function): Lambda function for the `/users` resource.
    - visits (aws_lambda.Function): Lambda function for the `/visits` resource.
    - qualifications (aws_lambda.Function): Lambda function for the `/qualifications` resource.
    - equipment (aws_lambda.Function): Lambda function for the `/equipment` resource.
    - tiger_training (aws_lambda.Function): Lambda function for the `/tiger_training` resource.
    - env (Environment): The AWS environment, including account and region.
    - create_dns (bool): Whether to create a custom domain for the API Gateway.
    - zones (MakerspaceDns): Optional Makerspace DNS configuration.

    Key Features:
    - **REST API**:
        - Centralized API Gateway for multiple Lambda integrations.
        - Default CORS configuration allows all origins and HTTP methods.
    - **Routing**:
        - Defines routes for various resources and integrates them with respective Lambda functions.
    - **Custom Domain**:
        - Integrates the API Gateway with a custom domain if `create_dns` is enabled.
    - **Deployment**:
        - Deploys the API to a stage (e.g., "prod", "beta") and supports future usage plan automation.

    Documentation Links:
        - aws_apigateway.RestApi:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/RestApi.html
        - aws_apigateway.CorsOptions:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/CorsOptions.html
        - aws_apigateway.Stage:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/Stage.html
        - aws_apigateway.UsagePlan:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/UsagePlan.html
        - aws_lambda.Function:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        - aws_certificatemanager.Certificate:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_certificatemanager/Certificate.html
    """

    def __init__(self, scope: Construct, stage: str,
                user: aws_lambda.Function, visits: aws_lambda.Function,
                 qualifications: aws_lambda.Function, equipment: aws_lambda.Function,
                 tiger_training: aws_lambda.Function,
                 *,
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

        # Thing to do in the future:
        # Automate the creation of a usage plan and api key
        # alongside the deployed stage. Currently not implemented
        # due to time constraints and, for some reason, a lot of
        # trouble "recreating" a key if a key with the same name
        # already exists. self.create_usage_plan() will be left as
        # a stub for automating the creation of these things. For
        # now, this is left as a manual step to set up the environment.


    def create_rest_api(self):

        # Create the Rest API
        self.api = aws_apigateway.RestApi(
            self,
            'SharedApiGateway',
            default_cors_preflight_options=aws_apigateway.CorsOptions(
                allow_origins=aws_apigateway.Cors.ALL_ORIGINS,  # Allow all origins
                allow_methods=aws_apigateway.Cors.ALL_METHODS,  # Allow all HTTP methods
                allow_headers=["*"]
                #allow_headers=[
                #    "Content-Type",
                #    "Authorization",
                #    "X-Amz-Date",
                #    "X-Api-Key",
                #    "Accept",
                #    "Accept-Encoding",
                #    "Origin",
                #    "Connection",
                #    "Host",
                #    "User-Agent",
                #],
            ),
        )

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
            self, id=f"SharedApiGatewayDeploymentStage{stage_name}",
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
