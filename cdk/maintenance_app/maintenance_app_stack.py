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
    aws_secretsmanager as secrets
)
import boto3, json

from thingcert import createThing as create_thing

class MaintenanceAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    #-------------------DynamoDB Tables-----------------------

        #Tasks, Machines, Visitors, Visits, Users, Permissions

        #Get the client
        dynamodb_client = boto3.client('dynamodb')

        #Define Existing Tables
        existing_tables = dynamodb_client.list_tables()['TableNames']

        #Create Tasks Resource
        if 'Tasks' not in existing_tables:
            tasksTable = ddb.Table(
                self, 'Tasks',
                partition_key={'name': 'task_id', 'type': ddb.AttributeType.STRING},
                table_name='Tasks'
            )
        #Find Parent Tasks Resource
        else:
            tasksTable = ddb.Table.from_table_name(self, 'Tasks', 'Tasks')


        #Create Machines resource
        if 'Machines' not in existing_tables:
            machinesTable = ddb.Table(
                self, 'Machines',
                partition_key={'name': 'machine_name', 'type': ddb.AttributeType.STRING},
                table_name='Machines'
            )
        #Find Machines Resource
        else:
            machinesTable = ddb.Table.from_table_name(self, 'Machines', 'Machines')


        #Create Visitors resource
        if 'Visitors' not in existing_tables:
            visitorsTable = ddb.Table(
                self, 'Visitors',
                partition_key={'name': 'hardware_id', 'type': ddb.AttributeType.STRING},
                table_name='Visitors'
            )
        #Find Visitors Resource
        else:
            visitorsTable = ddb.Table.from_table_name(self,
                'Visitors', 'Visitors')

        #Create Visits resource
        if 'Visits' not in existing_tables:
            visitsTable = ddb.Table (
                self, 'Visits',
                partition_key={'name': 'visitor_id', 'type': ddb.AttributeType.STRING},
                sort_key={'name': 'sign_in_time', 'type': ddb.AttributeType.NUMBER},
                table_name='Visits'
            )
        #Find Visits Resource
        else:
            visitsTable = ddb.Table.from_table_name(self,
                'Visits', 'Visits')


        #Create User resource
        if 'Users' not in existing_tables:
            usersTable = ddb.Table (
                self, 'Users',
                partition_key={'name': 'user_id', 'type': ddb.AttributeType.STRING},
                table_name='Users'
            )
        #Find User Resource
        else:
            usersTable = ddb.Table.from_table_name(self,
                'Users', 'Users')

    #-------------------S3 Buckets------------------------------

        #Create Public Front End S3 Bucket (will eventually not be public)
        FrontEndBucket = s3.Bucket(self, 'FrontEndBucket',
            website_index_document= 'index.html',
            bucket_name='admin.cumaker.space',
            public_read_access= True
        )

        s3deploy.BucketDeployment(self, 'DeployWebsite',
            sources=[s3deploy.Source.asset('maintenance_app/front-end/')],
            destination_bucket=FrontEndBucket
        )

        #TODO:
            #Subdomain
            #Add compiled build files for the website


    #------------------Lambda Functions/API Integrations--------------------

        ###------Administrative------###

        ## ResetPassword ##
        ResetPasswordLambda = _lambda.Function(
            self, 'ResetPassword',
            function_name = 'ResetPassword',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='ResetPassword.ResetPasswordHandler',
        )
        #Add Lambda Integration for API
        ResetPasswordLambdaIntegration = apigw.LambdaIntegration(ResetPasswordLambda)

        ## TODO: GenerateUserToken
        GenerateUserTokenLambda = _lambda.Function(
            self, 'GenerateUserToken',
            function_name = 'GenerateUserToken',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GenerateUserToken.GenerateUserTokenLambda',
        )
        #Add Lambda Integration for API
        GenerateUserTokenLambdaIntegration = apigw.LambdaIntegration(GenerateUserTokenLambda)



        ###------Machine------###

        ## CreateMachine ##
        CreateMachineLambda = _lambda.Function(
            self, 'CreateMachine',
            function_name = 'CreateMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateMachine.CreateMachineHandler',
        )
        #Granting Access to view machines DynamoDB Table
        machinesTable.grant_full_access(CreateMachineLambda)
        #Add Lambda Integration for API
        CreateMachineLambdaIntegration = apigw.LambdaIntegration(CreateMachineLambda)


        ## GetMachineStatus ##
        GetMachineStatusLambda = _lambda.Function(
            self, 'GetMachineStatus',
            function_name = 'GetMachineStatus',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetMachineStatus.GetMachineStatusHandler',
        )
        #Granting Access to view machines DynamoDB Table
        machinesTable.grant_full_access(GetMachineStatusLambda)
        #Add Lambda Integration for API
        GetMachineStatusLambdaIntegration = apigw.LambdaIntegration(GetMachineStatusLambda)


        ##DeleteMachine
        DeleteMachineLambda = _lambda.Function(
            self, 'DeleteMachine',
            function_name = 'DeleteMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='DeleteMachine.DeleteMachineHandler',
        )
        #Granting Access to view machines DynamoDB Table
        machinesTable.grant_full_access(DeleteMachineLambda)
        #Add Lambda Integration for API
        DeleteMachineLambdaIntegration = apigw.LambdaIntegration(DeleteMachineLambda)



        ###------Task------###

        ## CreateTask ##
        CreateTaskLambda = _lambda.Function(
            self, 'CreateTask',
            function_name = 'CreateTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateTask.CreateTaskHandler',
        )
        #Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(CreateTaskLambda)
        #Add Lambda Integration for API
        CreateTaskLambdaIntegration = apigw.LambdaIntegration(CreateTaskLambda)


        ## GetTasks ##
        GetTasksLambda = _lambda.Function(
            self, 'GetTasks',
            function_name = 'GetTasks',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetTasks.GetTasksHandler',
        )
        #Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(GetTasksLambda)
        #Add Lambda Integration for API
        GetTasksLambdaIntegration = apigw.LambdaIntegration(GetTasksLambda)


        ## ResolveTask ##
        ResolveTaskLambda = _lambda.Function(
            self, 'ResolveTask',
            function_name = 'ResolveTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='ResolveTask.ResolveTaskHandler',
        )
        #Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(ResolveTaskLambda)
        #Add Lambda Integration for API
        ResolveTaskLambdaIntegration = apigw.LambdaIntegration(ResolveTaskLambda)


        ## UpdateTask ##
        UpdateTaskLambda = _lambda.Function(
            self, 'UpdateTask',
            function_name = 'UpdateTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='UpdateTask.UpdateTaskHandler',
        )
        #Granting Access to view tasks DynamoDB Table
        tasksTable.grant_full_access(UpdateTaskLambda)
        #Add Lambda Integration for API
        UpdateTaskLambdaIntegration = apigw.LambdaIntegration(UpdateTaskLambda)



        ###------User------###

        ## CreateUser ##
        CreateUserLambda = _lambda.Function(
            self, 'CreateUser',
            function_name = 'CreateUser',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateUser.CreateUserHandler',
        )
        #Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(CreateUserLambda)
        #Add Lambda Integration for API
        CreateUserLambdaIntegration = apigw.LambdaIntegration(CreateUserLambda)


        ## DeleteUser ##
        DeleteUserLambda = _lambda.Function(
            self, 'DeleteUser',
            function_name = 'DeleteUser',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='DeleteUser.DeleteUserHandler',
        )
        #Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(DeleteUserLambda)
        #Add Lambda Integration for API
        DeleteUserLambdaIntegration = apigw.LambdaIntegration(DeleteUserLambda)


        ## GetUser ##
        GetUsersLambda = _lambda.Function(
            self, 'GetUsers',
            function_name = 'GetUsers',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetUsers.GetUsersHandler',
        )
        #Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(GetUsersLambda)
        #Add Lambda Integration for API
        GetUsersLambdaIntegration = apigw.LambdaIntegration(GetUsersLambda)


        ## UpdateUser ##
        UpdateUserLambda = _lambda.Function(
            self, 'UpdateUser',
            function_name = 'UpdateUser',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='UpdateUser.UpdateUserHandler',
        )
        #Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(UpdateUserLambda)
        #Add Lambda Integration for API
        UpdateUserLambdaIntegration = apigw.LambdaIntegration(UpdateUserLambda)



        ###------Visitor------###

        ## CreateVisitor ##
        CreateVisitorLambda = _lambda.Function(
            self, 'CreateVisitor',
            function_name = 'CreateVisitor',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='CreateVisitor.CreateVisitorHandler',
        )
        #Granting Access to view visitors and visits DynamoDB Table
        visitorsTable.grant_full_access(CreateVisitorLambda)
        visitsTable.grant_full_access(CreateVisitorLambda)
        #Add Lambda Integration for API
        CreateVisitorLambdaIntegration = apigw.LambdaIntegration(CreateVisitorLambda)


        ## GetVisitors ##
        GetVisitorLambda = _lambda.Function(
            self, 'GetVisitors',
            function_name = 'GetVisitors',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='GetVisitors.GetVisitorsHandler',
        )
        #Granting Access to view visitors and visits DynamoDB Table
        visitorsTable.grant_full_access(GetVisitorLambda)
        visitsTable.grant_full_access(GetVisitorLambda)
        #Add Lambda Integration for API
        GetVisitorsLambdaIntegration = apigw.LambdaIntegration(GetVisitorLambda)



        ###------Sign in/out on Pi's------###
        ## SignIn ##
        RPI_SignInLambda = _lambda.Function(
            self, 'RPI_SignIn',
            function_name = 'RPI_SignIn',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='RPI_SignIn.RPI_SignIn_Handler',
        )
        #Granting Access to view users and loginInfo DynamoDB Table
        visitorsTable.grant_full_access(RPI_SignInLambda)
        visitsTable.grant_full_access(RPI_SignInLambda)
        #Add Lambda Integration for API
        RPI_SignInLambdaIntegration = apigw.LambdaIntegration(RPI_SignInLambda, proxy=True)


        ## SignOut ##
        RPI_SignOutLambda = _lambda.Function(
            self, 'RPI_SignOut',
            function_name = 'RPI_SignOut',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='RPI_SignOut.RPI_SignOut_Handler',
        )
        #Granting Access to view users and loginInfo DynamoDB Table
        visitorsTable.grant_full_access(RPI_SignOutLambda)
        visitsTable.grant_full_access(RPI_SignOutLambda)
        #Add Lambda Integration for API
        RPI_SignOutLambdaIntegration = apigw.LambdaIntegration(RPI_SignOutLambda, proxy=True)

        ## Pre-Sign Up Trigger ##
        ConfirmUserLambda = _lambda.Function(
            self, 'ConfirmUser',
            function_name = 'ConfirmUser',
            runtime=_lambda.Runtime.NODEJS_12_X,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='ConfirmUser.ConfirmUserHandler',
        )

        #NOTE: Log in lambda has to bet put after cognito pool

#-------------------Cognito Pool------------------------------
        makerspaceCognitoPool = cognito.UserPool(self, "myuserpool",
            user_pool_name="myawesomeapp-userpool",
            self_sign_up_enabled=True,
            user_verification= {
                "email_subject": "Your Veriication code",
                "email_body": "Your verification code is {####}",
                "email_style": cognito.VerificationEmailStyle.CODE,
            },
            user_invitation={
                "email_subject": "Your temporary password",
                "email_body": "Your username is {username} and tempxorary password is {####}.",
                "sms_message": "Your username is {username} and temporary password is {####}. "
            },
            sign_in_aliases={
                "username": True,
                "email": True
            },
            standard_attributes={
                "email": {
                    "required": True,
                    "mutable": False
                }
            },
            custom_attributes={
                "fistname": cognito.StringAttribute(min_len=1, max_len=256, mutable=True),
                "lastname": cognito.StringAttribute(min_len=1, max_len=256, mutable=True),
                "role": cognito.StringAttribute(min_len=1, max_len=256, mutable=True)
            },
            lambda_triggers={
                "pre_authentication": ConfirmUserLambda
            }
        )

        ## Log in ##
        LoginLambda = _lambda.Function(
            self, 'Login',
            function_name = 'Login',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='Login.LoginHandler',
            environment = {
                'cognitoUserPool': makerspaceCognitoPool.user_pool_arn,
                #TODO: Pass client ID as well to Login
            }
        )

        #Add Lambda Integration for API
        LoginLambdaIntegration = apigw.LambdaIntegration(LoginLambda)

#----------------Master API--------------------------
        #Create Master API and enable CORS on all methods
        um_api = apigw.RestApi(self,'Master API',
            default_cors_preflight_options = apigw.CorsOptions(
                allow_origins = apigw.Cors.ALL_ORIGINS,
                allow_methods = apigw.Cors.ALL_METHODS
            )
        )

        #Add cognito authorizer
        cognitoAuth = apigw.CfnAuthorizer(self, "adminSectionAuth",
            rest_api_id=um_api.rest_api_id,
            type='COGNITO_USER_POOLS',
            identity_source='method.request.header.name.Authorization', #NOTE: Where to check for what to auth
            provider_arns=[makerspaceCognitoPool.user_pool_arn],
            name="adminSectionAuth"
        )

        #NOTE: put s3 bucket and API Gateway on same domain to avoid using CORS?

        # Add ANY
        um_api.root.add_method('ANY')

        ###-----Administrative------###
        administrative = um_api.root.add_resource('administrative')
        ## Patch ##
        administrative.add_method('PATCH', ResetPasswordLambdaIntegration)
        ## Post ##
        administrative.add_method('POST', GenerateUserTokenLambdaIntegration)

        ###------Machines------###
        machines = um_api.root.add_resource('machines')

        ## Delete ##
        machines.add_method('DELETE', DeleteMachineLambdaIntegration)
        ## Post ##
        machines.add_method('POST', GetMachineStatusLambdaIntegration)

        ###-----Raspberry Pi's------###
        ## Sign in ##
        signin = um_api.root.add_resource('signin')
        #Add sign in method
        signin.add_method('POST', RPI_SignInLambdaIntegration)

        ## Sign out
        signout = um_api.root.add_resource('signout')
        #Add sign out method
        signout.add_method('POST', RPI_SignOutLambdaIntegration)

        ###------Tasks------###
        tasks = um_api.root.add_resource('tasks')

        ## Delete ##
        tasks.add_method('DELETE', ResolveTaskLambdaIntegration)
        ## Get ##
        tasks.add_method('GET', GetTasksLambdaIntegration)
        ## Patch ##
        tasks.add_method('PATCH', UpdateTaskLambdaIntegration)
        ## Post ##
        createTaskMethod = tasks.add_method('POST', CreateTaskLambdaIntegration)
        # Add authorizer to create task
        method_resource = createTaskMethod.node.find_child('Resource')
        method_resource.add_property_override('AuthorizationType', 'COGNITO_USER_POOLS')
        method_resource.add_property_override('AuthorizerId', {"Ref": cognitoAuth.logical_id})

        ###------Users------###
        users = um_api.root.add_resource('users')

        ## Delete ##
        users.add_method('DELETE', DeleteUserLambdaIntegration)
        ## Get ##
        users.add_method('GET', GetUsersLambdaIntegration)
        ## Patch ##
        users.add_method('PATCH', UpdateUserLambdaIntegration)
        ## Post ##
        users.add_method('POST', LoginLambdaIntegration)
        ######################################################################
        ## NOTE: Documentation has separate POST method for change password ##
        ######################################################################
        ## Put ##
        users.add_method('PUT', CreateUserLambdaIntegration)


        ###------Visitors------###
        visitors = um_api.root.add_resource('visitors')

        ## Post ##
        visitors.add_method('POST', GetVisitorsLambdaIntegration)
        ## Put ##
        visitors.add_method('PUT', CreateVisitorLambdaIntegration)


# #----------------IoT--------------------------
        #Create All allowed policy
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
        CUmakeit_IoT_Policy = iot.CfnPolicy(self, "IoT_All_Allowed", policy_name="IoT_All_Allowed", policy_document= IoT_All_Allowed_Policy)

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
