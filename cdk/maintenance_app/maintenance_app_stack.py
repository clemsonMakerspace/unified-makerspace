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
    aws_iot as iot
)
import boto3

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
                partition_key={'name': 'visit_id', 'type': ddb.AttributeType.STRING},
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
        FrontEndBucket = s3.Bucket(self, 'FrontEndBucket')

        #TypeScript
        # const websiteBucket = new s3.Bucket(this, 'WebsiteBucket', {
        #     websiteIndexDocument: 'index.html',
        #     publicReadAccess: true
        # });

        # new s3deploy.BucketDeployment(this, 'DeployWebsite', {
        #     sources: [s3deploy.Source.asset('./website-dist')],
        #     destinationBucket: websiteBucket,
        #     destinationKeyPrefix: 'web/static' // optional prefix in destination bucket
        # });
        # s3deploy.BucketDeployment(
        #     self, 'DeployWebsite', 
        #     sources = s3deploy.Source.asset('maintenance_app/front-end'),
        #     destinationBucket = FrontEndBucket
        # )

        #TODO:
            #Subdomain/Make Public
        
    #------------------Lambda Functions/API Integrations--------------------

        ###------Machine------###

        ## CreateMachine ##
        CreateMachineLambda = _lambda.Function(
            self, 'CreateMachine',
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
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='DeleteUser.DeleteUserHandler',
        )
        #Granting Access to view users DynamoDB Table
        usersTable.grant_full_access(DeleteUserLambda)
        #Add Lambda Integration for API
        DeleteUserLambdaIntegration = apigw.LambdaIntegration(DeleteUserLambda)

        #TODO: GetUser once added
        # GetUsersLambda = _lambda.Function(
        #     self, 'DeleteUser',
        #     runtime=_lambda.Runtime.PYTHON_3_7,
        #     code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
        #     handler='GetUsers.GetUsersHandler',
        # )
        # #Granting Access to view users DynamoDB Table
        # usersTable.grant_full_access(GetUsersLambda)
        # #Add Lambda Integration for API
        # GetUsersLambdaIntegration = apigw.LambdaIntegration(GetUsersLambda)

        ###------Visitor------###

        ## CreateVisitor ##
        CreateVisitorLambda = _lambda.Function(
            self, 'CreateVisitor',
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
        SignInLambda = _lambda.Function(
            self, 'SignIn',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='SignIn.SignInHandler',
        )
        #NOTE: Lambda not currently up to date to use new tables
        #Granting Access to view users and loginInfo DynamoDB Table
        visitorsTable.grant_full_access(CreateVisitorLambda)
        visitsTable.grant_full_access(CreateVisitorLambda)
        #Add Lambda Integration for API
        SignInLambdaIntegration = apigw.LambdaIntegration(SignInLambda)

        
        ## SignOut ##
        SignOutLambda = _lambda.Function(
            self, 'SignOut',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
            handler='SignOut.SignOutHandler',
        )
        #NOTE: Lambda not currently up to date to use new tables
        #Granting Access to ___ DynamoDB Tables
        visitorsTable.grant_full_access(CreateVisitorLambda)
        visitsTable.grant_full_access(CreateVisitorLambda)
        #Add Lambda Integration for API
        SignOutLambdaIntegration = apigw.LambdaIntegration(SignOutLambda)
        

        #TODO: Authorization with JWT Token and Lamdba
        ###------Authorization------###
        ## UpdatePermissions ##
        # UpdatePermissionsLambda = _lambda.Function(
        #     self, 'UpdatePermissions',
        #     runtime=_lambda.Runtime.PYTHON_3_7,
        #     code=_lambda.Code.asset('maintenance_app/lambda-functions/'),
        #     handler='UpdatePermissions.UpdatePermissionsHandler',
        # )
        # #Granting Access to view machines DynamoDB Table
        # usersTable.grant_full_access(UpdatePermissionsLambda)
        # #Add Lambda Integration for API
        # UpdatePermissionsLambdaIntegration = apigw.LambdaIntegration(UpdatePermissionsLambda)

#----------------Master API--------------------------
        #Create Master API and enable CORS on all methods
        um_api = apigw.RestApi(self,'Master API')
        # , 
        #     default_Cors_Preflight_Options = apigw.CorsOptions(
        #         allowOrigins = apigw.Cors.ALL_ORIGINS,
        #         allowMethods = apigw.Cors.ALL_METHODS
        #     )
        # )
        # Add ANY 
        um_api.root.add_method('ANY')

        # um_api.add_cors_preflight(
        #     allowOrigins = apigw.Cors.ALL_ORIGINS,
        #     allowMethods = apigw.Cors.ALL_METHODS
        # )
        # #Enable CORS on all methods

        # new apigateway.RestApi(this, 'api', {
        #     defaultCorsPreflightOptions: {
        #         allowOrigins: apigateway.Cors.ALL_ORIGINS,
        #         allowMethods: apigateway.Cors.ALL_METHODS
        #     }
        # })

        # const bucket = new s3.Bucket(this, 'MyBucket', {
        #     websiteRedirect: {
        #         host: 'aws.amazon.com'
        #     }
        # })

        # bucket = s3.Bucket(self, "MyBucket", 
        #     website_redirect=s3.WebsiteRedirect (
        #         host_name="aws.amazon.com"
        #     )
        # )


        # ###------Auth------###
        # auth = um_api.root.add_resource('auth')

        # ## TODO: Delete ##
        # ## TODO: Put ##


        ###------Machines------###
        machines = um_api.root.add_resource('machines')

        ## Delete ##
        machines.add_method('DELETE', DeleteMachineLambdaIntegration)
        ## Post ##
        machines.add_method('POST', GetMachineStatusLambdaIntegration)


        ###------Tasks------###
        tasks = um_api.root.add_resource('tasks')

        ## Delete ##
        tasks.add_method('DELETE', ResolveTaskLambdaIntegration)
        ## Get ##
        tasks.add_method('GET', GetTasksLambdaIntegration)
        ## Patch ##
        tasks.add_method('PATCH', UpdateTaskLambdaIntegration)
        ## Post ##
        tasks.add_method('POST', CreateTaskLambdaIntegration)

        ###------Users------###
        users = um_api.root.add_resource('users')

        ## Delete ##
        users.add_method('DELETE',DeleteUserLambdaIntegration)
        ##TODO: Get ##
        # users.add_method('GET',GetUsersLambdaIntegration)
        ##TODO: Patch ##
        # users.add_method('PATCH',UpdateUsersLambdaIntegration)
        ##TODO: Post ##
        # users.add_method('POST',LoginLambdaIntegration)
        ## Put ##
        users.add_method('PUT',CreateUserLambdaIntegration)


        ###------Visitors------###
        visitors = um_api.root.add_resource('visitors')

        ## Post ##
        visitors.add_method('POST', GetVisitorsLambdaIntegration)
        ## Put ##
        visitors.add_method('PUT', CreateVisitorLambdaIntegration)


# #----------------IoT--------------------------
#         CUmakeit_01_Thing = iot.CfnThing(self, "CUmakeit_01", thing_name=self.stack_name)
#         CUmakeit_01_Cert = iot.CfnCertificate(self, "CUmakeit_01_Cert", certificate_signing_request=csr, status="ACTIVE")
#         CUmakeit_01_Policy = iot.CfnPolicy(self, "CUmakeit_01_Policy", policy_document=policy)

#         # Attach the Certificate to the Thing
#         iot.CfnThingPrincipalAttachment(self, "pi1CertificateAttachment", principal=pi1Cert.attr_arn, thing_name=raspberryPi1.ref)
        
#         # Attach the Policy to the Certificate
#         iot.CfnPolicyPrincipalAttachment(self, "pi1PolicyAttachment", principal=pi1Cert.attr_arn, policy_name=pi1Policy.ref)

#         raspberryPi2 = iot.CfnThing(self, "raspberryPi2", thing_name=self.stack_name)
#         pi2Cert = iot.CfnCertificate(self, "pi2Certificate", certificate_signing_request=csr, status="ACTIVE")
#         pi2Policy = iot.CfnPolicy(self, "pi2Policy", policy_document=policy)

#         # Attach the Certificate to the Thing
#         iot.CfnThingPrincipalAttachment(self, "pi2CertificateAttachment", principal=pi2Cert.attr_arn, thing_name=raspberryPi2.ref)
        
#         # Attach the Policy to the Certificate
#         iot.CfnPolicyPrincipalAttachment(self, "pi2PolicyAttachment", principal=pi2Cert.attr_arn, policy_name=pi2Policy.ref)