from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3_deployment as s3deploy,
    aws_iot as iot,
    aws_cognito as cognito,
    aws_secretsmanager as secrets,
    aws_backup as backup,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins
)
import json

from thingcert import createThing as create_thing


class MaintenanceAppStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, stage = None, school = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        service = MaintenanceAppStack(self,'MaintenanceAppStack',stage,school)


class MaintenanceAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, stage = None, school = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        def bucket_prefix(stage,school):
                # Important to throw an error here because the wrong bucket
                # name will cause erros on deploy rather than build-time
                return {
                        'PROD': f'{school}-admin',
                        'BETA': f'{school}-beta-admin',
                        'DEV' : f'{school}-dev-admin',
                        }[stage]


    # -------------------DynamoDB Tables-----------------------

        # Tasks, Machines, Visitors, Visits, Users, Permissions

        # Create Tasks Resource
        tasksTable = ddb.Table(
            self, 'Tasks',
            partition_key={
                'name': 'task_id',
                'type': ddb.AttributeType.STRING},
            table_name='Tasks',
            billing_mode=ddb.BillingMode('PAY_PER_REQUEST')
        )

        # Create Machines resource
        machinesTable = ddb.Table(
            self, 'Machines',
            partition_key={
                'name': 'machine_name',
                'type': ddb.AttributeType.STRING},
            table_name='Machines',
            billing_mode=ddb.BillingMode('PAY_PER_REQUEST')
        )

        visitorsTable = ddb.Table(
            self, 'Visitors',
            partition_key={
                'name': 'hardware_id',
                'type': ddb.AttributeType.STRING},
            table_name='Visitors',
            billing_mode=ddb.BillingMode('PAY_PER_REQUEST')
        )

        visitsTable = ddb.Table(
            self, 'Visits',
            partition_key={
                'name': 'visitor_id',
                'type': ddb.AttributeType.STRING},
            sort_key={
                'name': 'sign_in_time',
                'type': ddb.AttributeType.NUMBER},
            table_name='Visits',
            billing_mode=ddb.BillingMode('PAY_PER_REQUEST')
        )

        usersTable = ddb.Table(
            self, 'Users',
            partition_key={
                'name': 'user_id',
                'type': ddb.AttributeType.STRING},
            table_name='Users',
            billing_mode=ddb.BillingMode('PAY_PER_REQUEST')
        )

        userVerificationTokenTable = ddb.Table(
            self, 'userVerificationToken',
            partition_key={
                'name': 'generatedToken',
                'type': ddb.AttributeType.STRING},
            table_name='userVerificationToken',
            billing_mode=ddb.BillingMode('PAY_PER_REQUEST')
        )

        plan = backup.BackupPlan.daily_monthly1_year_retention(
            self, 'BackupPlan'
        )

        plan.add_selection(
            'BackupSelection', resources=[
                backup.BackupResource.from_dynamo_db_table(tasksTable),
                backup.BackupResource.from_dynamo_db_table(machinesTable),
                backup.BackupResource.from_dynamo_db_table(visitorsTable),
                backup.BackupResource.from_dynamo_db_table(visitsTable),
                backup.BackupResource.from_dynamo_db_table(usersTable),
                backup.BackupResource.from_dynamo_db_table(
                    userVerificationTokenTable)
            ]
        )

    # --------------------S3 Buckets------------------------------

        # Create Public Front End S3 Bucket (will eventually not be public)
        FrontEndBucket = s3.Bucket(self, f'{bucket_prefix(stage,school)}-FrontEndBucket',
                                    website_index_document='index.html',
                                    website_error_document='index.html',
                                    public_read_access=False
                                    )

        s3deploy.BucketDeployment(self, 'DeployWebsite',
                                  sources=[
                                      s3deploy.Source.asset('maintenance_app/front-end/')],
                                  destination_bucket=FrontEndBucket
                                  )

    # --------------------CloudFront------------------------------
        oai = cloudfront.OriginAccessIdentity(self, 'FrontEndOAI')
        FrontEndBucket.grant_read(oai)

        # redirect to web app for internal routing
        internalRedirect = cloudfront.ErrorResponse(http_status=404,
                                                    response_http_status=200,
                                                    response_page_path='/index.html')

        cloudfront.Distribution(self, 'FrontEndDistribution',
                                default_behavior=cloudfront.BehaviorOptions(
                                    origin=origins.S3Origin(
                                        bucket=FrontEndBucket,
                                        origin_access_identity=oai,
                                        ),
                                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
                                    ),
                                default_root_object='index.html',
                                error_responses=[internalRedirect]
                                )

    # --------------------Cognito Pool------------------------------
        makerspaceUserCognitoPool = cognito.UserPool(self, "user-userpool",
                                                     user_pool_name="makerspace-user-userpool",
                                                     password_policy=cognito.PasswordPolicy(
                                                         min_length=6,
                                                         require_digits=False,
                                                         require_lowercase=False,
                                                         require_symbols=False,
                                                         require_uppercase=False
                                                     ),
                                                     self_sign_up_enabled=True,
                                                     user_verification={
                                                         "email_subject": "Your Verification Link",
                                                         "email_body": "Please click the link below to verify your email address. {##Verify Email##}",
                                                         "email_style": cognito.VerificationEmailStyle.LINK,
                                                     },
                                                     user_invitation={
                                                         "email_subject": "Your temporary password",
                                                         "email_body": "Your username is {username} and temporary password is {####}.",
                                                         "sms_message": "Your username is {username} and temporary password is {####}. "
                                                     },
                                                     sign_in_aliases={
                                                         "email": True
                                                     },
                                                     custom_attributes={
                                                         "firstname": cognito.StringAttribute(min_len=1, max_len=256, mutable=True),
                                                         "lastname": cognito.StringAttribute(min_len=1, max_len=256, mutable=True),
                                                         "role": cognito.StringAttribute(min_len=1, max_len=256, mutable=True)
                                                     },
                                                     # TODO: parameterize removal policy
                                                     )

        # TODO: rebase parameterization off of this branch
        makerspaceUserCognitoPool.add_domain('admin-makerspace-user-cognitoDomain',
                                             cognito_domain=cognito.CognitoDomainOptions(
                                                 domain_prefix=f'{bucket_prefix(stage,school)}-admin-makerspace-signup-users'
                                             )
                                             )

        userClient = cognito.UserPoolClient(self, 'user-client',
                                            user_pool=makerspaceUserCognitoPool,
                                            auth_flows=cognito.AuthFlow(
                                                custom=True,
                                                user_password=True,
                                                user_srp=True
                                            )
                                            )

        makerspaceVisitorCognitoPool = cognito.UserPool(self, "visitor-userpool",
                                                        user_pool_name="makerspace-visitor-userpool",
                                                        password_policy=cognito.PasswordPolicy(
                                                            min_length=6,
                                                            require_digits=False,
                                                            require_lowercase=False,
                                                            require_symbols=False,
                                                            require_uppercase=False
                                                        ),
                                                        self_sign_up_enabled=True,
                                                        user_verification={
                                                            "email_subject": "Your Verification Link",
                                                            "email_body": "Please click the link below to verify your email address. {##Verify Email##}",
                                                            "email_style": cognito.VerificationEmailStyle.LINK,
                                                        },
                                                        user_invitation={
                                                            "email_subject": "Your temporary password",
                                                            "email_body": "Your username is {username} and temporary password is {####}.",
                                                            "sms_message": "Your username is {username} and temporary password is {####}. "
                                                        },
                                                        sign_in_aliases={
                                                            "email": True
                                                        },
                                                        # TODO: parameterize removal policy
                                                        )

        # TODO: rebase parameterization off of this branch
        makerspaceVisitorCognitoPool.add_domain('admin-makerspace-visitor-cognitoDomain',
                                                cognito_domain=cognito.CognitoDomainOptions(
                                                    domain_prefix= f'{bucket_prefix(stage,school)}-admin-makerspace-signup-visitors'
                                                )
                                                )

        visitorClient = cognito.UserPoolClient(self, 'visitor-client',
                                               user_pool=makerspaceVisitorCognitoPool,
                                               auth_flows=cognito.AuthFlow(
                                                   custom=True,
                                                   user_password=True,
                                                   user_srp=True
                                               )
                                               )

    # ------------------Lambda Functions/API Integrations--------------------

        ###------Administrative------###

        ## ResetPassword ##
        ResetPasswordLambda = _lambda.Function(
            self, 'ResetPassword',
            function_name='ResetPassword',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='ResetPassword.ResetPasswordHandler',
            environment={
                'user_cognitoClientID': userClient.user_pool_client_id,
            }
        )
        # Add Lambda Integration for API
        ResetPasswordLambdaIntegration = apigw.LambdaIntegration(
            ResetPasswordLambda)

        ## TODO: GenerateUserToken
        GenerateUserTokenLambda = _lambda.Function(
            self, 'GenerateUserToken',
            function_name='GenerateUserToken',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GenerateUserToken.GenerateUserTokenHandler',
        )
        userVerificationTokenTable.grant_full_access(GenerateUserTokenLambda)
        # Add Lambda Integration for API
        GenerateUserTokenLambdaIntegration = apigw.LambdaIntegration(
            GenerateUserTokenLambda)

        ###------Machine------###

        ## CreateMachine ##
        CreateMachineLambda = _lambda.Function(
            self, 'CreateMachine',
            function_name='CreateMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateMachine.CreateMachineHandler',
        )
        # Granting Access to view machines DynamoDB Table
        machinesTable.grant_full_access(CreateMachineLambda)

        ## GetMachinesStatus ##
        GetMachinesStatusLambda = _lambda.Function(
            self, 'GetMachinesStatus',
            function_name='GetMachinesStatus',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetMachinesStatus.GetMachinesStatusHandler'
        )
        # Granting Access to view machines DynamoDB Table
        machinesTable.grant_full_access(GetMachinesStatusLambda)
        tasksTable.grant_full_access(GetMachinesStatusLambda)
        # Add Lambda Integration for API
        GetMachinesStatusLambdaIntegration = apigw.LambdaIntegration(
            GetMachinesStatusLambda)

        # DeleteMachine
        DeleteMachineLambda = _lambda.Function(
            self, 'DeleteMachine',
            function_name='DeleteMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='DeleteMachine.DeleteMachineHandler',
        )
        # Granting Access to view machines DynamoDB Table
        machinesTable.grant_full_access(DeleteMachineLambda)
        # Add Lambda Integration for API
        DeleteMachineLambdaIntegration = apigw.LambdaIntegration(
            DeleteMachineLambda)

        ###------Task------###

        ## CreateTask ##
        CreateTaskLambda = _lambda.Function(
            self, 'CreateTask',
            function_name='CreateTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateTask.CreateTaskHandler',
        )
        # Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(CreateTaskLambda)
        machinesTable.grant_full_access(CreateTaskLambda)
        # Add Lambda Integration for API
        CreateTaskLambdaIntegration = apigw.LambdaIntegration(CreateTaskLambda)

        ## GetTasks ##
        GetTasksLambda = _lambda.Function(
            self, 'GetTasks',
            function_name='GetTasks',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetTasks.GetTasksHandler',
        )
        # Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(GetTasksLambda)
        machinesTable.grant_full_access(GetTasksLambda)
        # Add Lambda Integration for API
        GetTasksLambdaIntegration = apigw.LambdaIntegration(GetTasksLambda)

        ## ResolveTask ##
        ResolveTaskLambda = _lambda.Function(
            self, 'ResolveTask',
            function_name='ResolveTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='ResolveTask.ResolveTaskHandler',
        )
        # Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(ResolveTaskLambda)
        machinesTable.grant_full_access(ResolveTaskLambda)
        # Add Lambda Integration for API
        ResolveTaskLambdaIntegration = apigw.LambdaIntegration(
            ResolveTaskLambda)

        ## UpdateTask ##
        UpdateTaskLambda = _lambda.Function(
            self, 'UpdateTask',
            function_name='UpdateTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='UpdateTask.UpdateTaskHandler',
        )
        # Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(UpdateTaskLambda)
        machinesTable.grant_full_access(UpdateTaskLambda)
        # Add Lambda Integration for API
        UpdateTaskLambdaIntegration = apigw.LambdaIntegration(UpdateTaskLambda)

        ###------User------###

        ## CreateUser ##
        CreateUserLambda = _lambda.Function(
            self, 'CreateUser',
            function_name='CreateUser',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateUser.CreateUserHandler',
            environment={
                'user_cognitoClientID': userClient.user_pool_client_id,
            }
        )
        # Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(CreateUserLambda)
        userVerificationTokenTable.grant_full_access(CreateUserLambda)
        # Add Lambda Integration for API
        CreateUserLambdaIntegration = apigw.LambdaIntegration(CreateUserLambda)

        ## DeleteUser ##
        DeleteUserLambda = _lambda.Function(
            self, 'DeleteUser',
            function_name='DeleteUser',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='DeleteUser.DeleteUserHandler',
            environment={
                'user_cognitoUserPoolID': makerspaceUserCognitoPool.user_pool_id,
            }
        )
        # Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(DeleteUserLambda)
        # Add Lambda Integration for API
        DeleteUserLambdaIntegration = apigw.LambdaIntegration(DeleteUserLambda)

        ## GetUser ##
        GetUsersLambda = _lambda.Function(
            self, 'GetUsers',
            function_name='GetUsers',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetUsers.GetUsersHandler',
        )
        # Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(GetUsersLambda)
        # Add Lambda Integration for API
        GetUsersLambdaIntegration = apigw.LambdaIntegration(GetUsersLambda)

        ## UpdateUser ##
        UpdateUserLambda = _lambda.Function(
            self, 'UpdateUser',
            function_name='UpdateUser',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='UpdateUser.UpdateUserHandler',
        )
        # Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(UpdateUserLambda)
        # Add Lambda Integration for API
        UpdateUserLambdaIntegration = apigw.LambdaIntegration(UpdateUserLambda)

        ###------Visitor------###

        ## CreateVisitor ##
        CreateVisitorLambda = _lambda.Function(
            self, 'CreateVisitor',
            function_name='CreateVisitor',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateVisitor.CreateVisitorHandler',
            environment={
                'visitor_cognitoClientID': visitorClient.user_pool_client_id,
            }
        )
        # Granting Access to view visitors and visits DynamoDB Table
        visitorsTable.grant_full_access(CreateVisitorLambda)
        visitsTable.grant_full_access(CreateVisitorLambda)
        # Add Lambda Integration for API
        CreateVisitorLambdaIntegration = apigw.LambdaIntegration(
            CreateVisitorLambda)

        ## GetVisitors ##
        GetVisitorsLambda = _lambda.Function(
            self, 'GetVisitors',
            function_name='GetVisitors',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetVisitors.GetVisitorsHandler',
        )
        # Granting Access to view visitors and visits DynamoDB Table
        visitorsTable.grant_full_access(GetVisitorsLambda)
        visitsTable.grant_full_access(GetVisitorsLambda)
        # Add Lambda Integration for API
        GetVisitorsLambdaIntegration = apigw.LambdaIntegration(
            GetVisitorsLambda)

        ## GetVisits ##
        GetVisitsLambda = _lambda.Function(
            self, 'GetVisits',
            function_name='GetVisits',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetVisits.GetVisitsHandler',
        )
        # Granting Access to view visitors and visits DynamoDB Table
        visitorsTable.grant_full_access(GetVisitsLambda)
        visitsTable.grant_full_access(GetVisitsLambda)
        # Add Lambda Integration for API
        GetVisitsLambdaIntegration = apigw.LambdaIntegration(GetVisitsLambda)

        ###------Sign in/out on Pi's------###
        ## SignIn ##
        RPI_SignInLambda = _lambda.Function(
            self, 'RPI_SignIn',
            function_name='RPI_SignIn',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='RPI_SignIn.RPI_SignIn_Handler',
        )
        # Granting Access to view users and loginInfo DynamoDB Table
        visitorsTable.grant_full_access(RPI_SignInLambda)
        visitsTable.grant_full_access(RPI_SignInLambda)
        # Add Lambda Integration for API
        RPI_SignInLambdaIntegration = apigw.LambdaIntegration(
            RPI_SignInLambda, proxy=True)

        ## SignOut ##
        RPI_SignOutLambda = _lambda.Function(
            self, 'RPI_SignOut',
            function_name='RPI_SignOut',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='RPI_SignOut.RPI_SignOut_Handler',
        )
        # Granting Access to view users and loginInfo DynamoDB Table
        visitorsTable.grant_full_access(RPI_SignOutLambda)
        visitsTable.grant_full_access(RPI_SignOutLambda)
        # Add Lambda Integration for API
        RPI_SignOutLambdaIntegration = apigw.LambdaIntegration(
            RPI_SignOutLambda, proxy=True)

        ## Log in ##
        LoginLambda = _lambda.Function(
            self, 'Login',
            function_name='Login',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='Login.loginHandler',
            environment={
                'user_cognitoClientID': userClient.user_pool_client_id,
            }
        )
        # Add permisisons for
        userVerificationTokenTable.grant_full_access(LoginLambda)
        usersTable.grant_full_access(LoginLambda)
        # Add Lambda Integration for API
        LoginLambdaIntegration = apigw.LambdaIntegration(LoginLambda)

# ----------------Master API--------------------------
        # Create Master API and enable CORS on all methods
        um_api = apigw.RestApi(self, 'Master API',
                               default_cors_preflight_options=apigw.CorsOptions(
                                   allow_origins=apigw.Cors.ALL_ORIGINS,
                                   allow_methods=apigw.Cors.ALL_METHODS
                               )
                               )

        # Add cognito authorizer
        cognitoAuth = apigw.CfnAuthorizer(self, "makerspaceWorkerAuth",
                                          rest_api_id=um_api.rest_api_id,
                                          type='COGNITO_USER_POOLS',
                                          identity_source='method.request.header.name.auth_token',
                                          provider_arns=[
                                              makerspaceUserCognitoPool.user_pool_arn],
                                          name="makerspaceWorkerAuth"
                                          )
        # NOTE: put s3 bucket and API Gateway on same domain to avoid using
        # CORS?

# ----------------Master API Methods--------------------------
        # Add ANY
        um_api.root.add_method('ANY')

        ###-----Administrative------###
        admin = um_api.root.add_resource('admin')

        ## Patch ##
        admin.add_method('PATCH', ResetPasswordLambdaIntegration)

        ## Post ##
        admin_POST_method = admin.add_method(
            'POST', GenerateUserTokenLambdaIntegration)
        # Add authorizer to admin POST
        # admin_POST_resource = admin_POST_method.node.find_child('Resource')
        # admin_POST_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # admin_POST_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ###------Machines------###
        machines = um_api.root.add_resource('machines')

        ## Delete ##
        machines_DELETE_method = machines.add_method(
            'DELETE', DeleteMachineLambdaIntegration)
        # Add authorizer to machines DELETE
        # machines_DELETE_resource = machines_DELETE_method.node.find_child('Resource')
        # machines_DELETE_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # machines_DELETE_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Post ##
        machines_POST_method = machines.add_method(
            'POST', GetMachinesStatusLambdaIntegration)
        # Add authorizer to machines POST
        # machines_POST_resource = machines_POST_method.node.find_child('Resource')
        # machines_POST_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # machines_POST_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ###------Tasks------###
        tasks = um_api.root.add_resource('tasks')

        ## Delete ##
        tasks_DELETE_method = tasks.add_method(
            'DELETE', ResolveTaskLambdaIntegration)
        # Add authorizer to tasks DELETE
        # tasks_DELETE_resource = tasks_DELETE_method.node.find_child('Resource')
        # tasks_DELETE_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # tasks_DELETE_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Get ##
        tasks_GET_method = tasks.add_method('GET', GetTasksLambdaIntegration)
        # Add authorizer to tasks GET
        # tasks_GET_resource = tasks_GET_method.node.find_child('Resource')
        # tasks_GET_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # tasks_GET_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Patch ##
        tasks_PATCH_method = tasks.add_method(
            'PATCH', UpdateTaskLambdaIntegration)
        # Add authorizer to tasks PATCH
        # tasks_PATCH_resource = tasks_PATCH_method.node.find_child('Resource')
        # tasks_PATCH_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # tasks_PATCH_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Post ##
        tasks_POST_method = tasks.add_method(
            'POST', CreateTaskLambdaIntegration)
        # Add authorizer to tasks POST
        # tasks_POST_resource = tasks_POST_method.node.find_child('Resource')
        # tasks_POST_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # tasks_POST_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ###------Users------###
        users = um_api.root.add_resource('users')

        ## Delete ##
        users_DELETE_method = users.add_method(
            'DELETE', DeleteUserLambdaIntegration)
        # Add authorizer to users DELETE
        # users_DELETE_resource = users_DELETE_method.node.find_child('Resource')
        # users_DELETE_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # users_DELETE_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Get ##
        users_GET_method = users.add_method('GET', GetUsersLambdaIntegration)
        # Add authorizer to users GET
        # users_GET_resource = users_GET_method.node.find_child('Resource')
        # users_GET_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # users_GET_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Patch ##
        users_PATCH_method = users.add_method(
            'PATCH', UpdateUserLambdaIntegration)
        # Add authorizer to users PATCH
        # users_PATCH_resource = users_PATCH_method.node.find_child('Resource')
        # users_PATCH_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # users_PATCH_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Post ##
        users.add_method('POST', LoginLambdaIntegration)

        ## Put ##
        users.add_method('PUT', CreateUserLambdaIntegration)

        ###------Visitors------###
        visitors = um_api.root.add_resource('visitors')

        ## Post ##
        visitors_POST_method = visitors.add_method(
            'POST', GetVisitsLambdaIntegration)
        # Add authorizer to visitors POST
        # visitors_POST_resource = visitors_POST_method.node.find_child('Resource')
        # visitors_POST_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # visitors_POST_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ## Put ##
        visitors.add_method('PUT', CreateVisitorLambdaIntegration)

        ## Get ##
        visits_GET_method = visitors.add_method(
            'GET', GetVisitorsLambdaIntegration)
        # Add authorizer to visitors POST
        # visits_POST_resource = visits_GET_method.node.find_child('Resource')
        # visits_POST_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        # visits_POST_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ###------Staging------###
        # Add stage deployment for API
        apiStageDeployment = apigw.Deployment(self, 'API Deployment',
                                              api=um_api
                                              )
        # Create stage with stage name "api"
        stage = apigw.Stage(self, 'api_stage',
                            deployment=apiStageDeployment,
                            stage_name='api'
                            )
        # Deploy the stage
        um_api.deployment_stage = stage

# #----------------IoT--------------------------
        # Creating API Gateway for IoT
        iot_api = apigw.RestApi(self, 'IoT API')

        # IoT API Methods

        # Add ANY
        iot_api.root.add_method('ANY')

        ###-----Raspberry Pi's------###

        # Sign in
        signin = iot_api.root.add_resource('signin')
        # Add sign in method
        signin.add_method('POST', RPI_SignInLambdaIntegration)

        # Sign out
        signout = iot_api.root.add_resource('signout')
        # Add sign out method
        signout.add_method('POST', RPI_SignOutLambdaIntegration)

        # IoT API deployment
        # Add stage deployment for API
        iot_apiStageDeployment = apigw.Deployment(self, 'IoT API Deployment',
                                                  api=iot_api
                                                  )
        # Create stage with stage name "api"
        iot_stage = apigw.Stage(self, 'iot_api_stage',
                                deployment=iot_apiStageDeployment,
                                stage_name='iot'
                                )
        # Deploy the stage
        iot_api.deployment_stage = iot_stage

        # Create All allowed policy
        IoT_All_Allowed_Policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "iot:Connect",
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": "iot:Publish",
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": "iot:Subscribe",
                    "Resource": "*"
                }
            ]
        }

        # Create policy for IoT Devices
        CUmakeit_IoT_Policy = iot.CfnPolicy(
            self,
            "IoT_All_Allowed",
            policy_name="IoT_All_Allowed",
            policy_document=IoT_All_Allowed_Policy)

        ## ---- Thing 1 ---- ##
        CUmakeit_01, cert01 = create_thing(self, '01', CUmakeit_IoT_Policy)

        ## ---- Thing 2 ---- ##
        CUmakeit_02, cert02 = create_thing(self, '02', CUmakeit_IoT_Policy)

        ## ---- Thing 3 ---- ##
        CUmakeit_03, cert03 = create_thing(self, '03', CUmakeit_IoT_Policy)

        ## ---- Thing 4 ---- ##
        CUmakeit_04, cert04 = create_thing(self, '04', CUmakeit_IoT_Policy)

        ## ---- Thing 5 ---- ##
        CUmakeit_05, cert05 = create_thing(self, '05', CUmakeit_IoT_Policy)

        ## ---- Thing 6 ---- ##
        CUmakeit_06, cert06 = create_thing(self, '06', CUmakeit_IoT_Policy)
