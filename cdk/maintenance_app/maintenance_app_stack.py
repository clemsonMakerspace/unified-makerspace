from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3_deployment as s3deploy
)
import boto3

class MaintenanceAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    #-------------------DynamoDB Tables-----------------------

        #Get the client
        dynamodb_client = boto3.client('dynamodb')

        #Define Existing Tables
        existing_tables = dynamodb_client.list_tables()['TableNames']

        #Parent Tasks Table Definition
        ParentTable = None
        
        #Create Parent Tasks Resource
        if 'Parent_Tasks' not in existing_tables:
            ParentTable = ddb.Table(
                self, 'Parent_Tasks',
                partition_key={'name': 'Parent_Id', 'type': ddb.AttributeType.STRING},
                table_name='Parent_Tasks'
            )
        #Find Parent Tasks Resource
        else:
            ParentTable = ddb.Table.from_table_name(self, 'Parent_Tasks', 'Parent_Tasks')

        #Child Tasks Table Definition
        ChildTable = None

        #Create Child Tasks resource
        if 'Child_Tasks' not in existing_tables:
            ChildTable = ddb.Table(
                self, 'Child_Tasks',
                table_name='Child_Tasks',
                partition_key={'name': 'Due_Date', 'type': ddb.AttributeType.STRING},
                sort_key={'name': 'Parent_Id', 'type': ddb.AttributeType.STRING}
            )

            ChildTable.add_global_secondary_index(
                index_name='Parent_Index',
                partition_key={'name': 'Parent_Id', 'type': ddb.AttributeType.STRING},
                sort_key={'name': 'Due_Date', 'type': ddb.AttributeType.STRING}
            )
        #Find Child Tasks Resource
        else:
            ChildTable = ddb.Table.from_table_name(self, 'Child_Tasks', 'Child_Tasks')

        #Machines Table Definition
        MachineTable = None

        #Create Machines resource
        if 'Machines' not in existing_tables:
            MachineTable = ddb.Table(
                self, 'Machines',
                partition_key={'name': 'Machine_Id', 'type': ddb.AttributeType.STRING},
                table_name='Machines'
            )
        #Find Machines Resource
        else:
            MachineTable = ddb.Table.from_table_name(self, 'Machines', 'Machines')

        #Machine Types Table Definition
        MachineTypesTable = None

        #Create Machine Types resource
        if 'Machine_Types' not in existing_tables:
            MachineTypesTable = ddb.Table(
                self, 'Machine_Types',
                partition_key={'name': 'Machine_Type', 'type': ddb.AttributeType.STRING},
                table_name='Machine_Types'
            )
        #Find Machine Types Resource
        else:
            MachineTypesTable = ddb.Table.from_table_name(self,
                'Machine_Types', 'Machine_Types')

        ############# Sign-In System Tables #############

        #Create Makerspace_User resource
        if 'Makerspace_User' not in existing_tables:
            MakerspaceUser = ddb.Table (
                self, 'Makerspace_User',
                partition_key={'name': 'StudentID', 'type': ddb.AttributeType.STRING},
                sort_key={'name': 'SK', 'type': ddb.AttributeType.STRING},
                table_name='Makerspace_User'
            )

        #Create User_LoginInfo resource
        if 'User_Login_Info' not in existing_tables:
            UserLoginInfo = ddb.Table (
                self, 'User_Login_Info',
                partition_key={'name': 'StudentID', 'type': ddb.AttributeType.STRING},
                table_name='User_Login_Info'
            )

    #-------------------Global Indexes----------------------------

        #ParentIndex Definiton
        ParentIndex = ddb.Table.from_table_name(self, 
                'ParentIndex', 'Child_Tasks/index/Parent_Index')

    #-------------------S3 Buckets------------------------------

        #Policy Statement for S3 bucket
        S3Policy = iam.PolicyStatement(
            actions=['s3:*'],
            effect=iam.Effect.ALLOW,
            resources=['*']
        )

        #Create Export History Bucket Resource
        ExportHistoryBucket = s3.Bucket(self, 'ExportHistoryBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        
        #Create Export Machine History Bucket Resource
        ExportMachineHistoryBucket = s3.Bucket(self, 'ExportMachineHistoryBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        
        #Create Notification Emails Bucket Resource
        NotificationBucket = s3.Bucket(self, 'NotificationEmailsBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        #Default Emails Deployed to NotificationBucket
        s3deploy.BucketDeployment(self, 'DefaultEmails',
            sources=[s3deploy.Source.asset('./maintenance_app/default-emails')],
            destination_bucket=NotificationBucket
        )

        #Create Public Front End S3 Bucket (will eventually not be public)
        FrontEndBucket = s3.Bucket(self, 'FrontEndBucket')
        
    #------------------Machine Functions/API--------------------

        #View machine types function
        viewMachineTypes = _lambda.Function(
            self, 'ViewMachineTypes',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='view_machine_types.viewMachineTypesHandler',
        )

        viewMachineTypesIntegration = apigw.LambdaIntegration(viewMachineTypes)

        #view machine types api
        apigw.LambdaRestApi(
            self, 'ViewMachineTypesAPI',
            handler=viewMachineTypes
        )

        #Granting Access to view machine types
        MachineTypesTable.grant_full_access(viewMachineTypes)
        MachineTable.grant_full_access(viewMachineTypes)

        #view a machine by type given machine type
        viewMachineByTypes = _lambda.Function(
            self, 'ViewMachineByTypes',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='view_machine_by_types.viewMachineByTypesHandler',
        )

        viewMachineByTypesIntegration = apigw.LambdaIntegration(viewMachineByTypes)

        #View Machine By Type Api
        apigw.LambdaRestApi(
            self, 'ViewMachineByTypesAPI',
            handler=viewMachineByTypes
        )

        #Granting Access to view machine by types
        MachineTypesTable.grant_full_access(viewMachineByTypes)
        MachineTable.grant_full_access(viewMachineByTypes)

        #view a machine given id
        viewMachine = _lambda.Function(
            self, 'ViewMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='view_machine.viewMachineHandler',
        )

        viewMachineIntegration = apigw.LambdaIntegration(viewMachine)

        #View Machine Api
        apigw.LambdaRestApi(
            self, 'ViewMachineAPI',
            handler=viewMachine
        )

        #Granting Access to view Machine
        MachineTable.grant_full_access(viewMachine)

        #view upcoming tasks given id
        ViewMachineUpcomingTasks = _lambda.Function(
            self, 'ViewMachineUpcomingTasks',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='view_machine_upcoming_task.ViewMachineUpcomingTasksHandler',
        )

        ViewMachineUpcomingTasksIntegration = apigw.LambdaIntegration(ViewMachineUpcomingTasks)

        #View Machine Upcoming Api
        apigw.LambdaRestApi(
            self, 'ViewMachineUpcomingTasksAPI',
            handler=ViewMachineUpcomingTasks
        )

        #Granting Access to View Machine Upcoming
        ParentTable.grant_full_access(ViewMachineUpcomingTasks)
        ChildTable.grant_full_access(ViewMachineUpcomingTasks)
        MachineTable.grant_full_access(ViewMachineUpcomingTasks)
        ParentIndex.grant_full_access(ViewMachineUpcomingTasks)

        #View Parents By Machine Functions
        ViewParentsByMachine = _lambda.Function(
            self, 'ViewParentsByMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='ViewParentsByMachine.ViewParentsByMachineHandler',
        )

        ViewParentsByMachineIntegration = apigw.LambdaIntegration(ViewParentsByMachine)

        #View Parents By Machine Api
        apigw.LambdaRestApi(
            self, 'ViewParentsByMachineAPI',
            handler=ViewParentsByMachine
        )

        #Granting Access to View Parents By Machine
        ParentTable.grant_full_access(ViewParentsByMachine)
        MachineTable.grant_full_access(ViewParentsByMachine)

        #add machine to db
        addMachine = _lambda.Function(
            self, 'AddMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='add_machine.addMachineHandler',
        )

        addMachineIntegration = apigw.LambdaIntegration(addMachine)

        #Add machine api
        apigw.LambdaRestApi(
            self, 'AddMachineAPI',
            handler=addMachine
        )

        #Grant access to add machine
        MachineTable.grant_full_access(addMachine)
        MachineTypesTable.grant_full_access(addMachine)

        #add new machine type to db
        addMachineType = _lambda.Function(
            self, 'AddMachineType',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='add_machine_type.addMachineTypeHandler',
        )

        addMachineTypeIntegration = apigw.LambdaIntegration(addMachineType)

        #Add Machine Type Api
        apigw.LambdaRestApi(
            self, 'AddMachineTypeAPI',
            handler=addMachineType
        )

        #Grant access to add machine types
        MachineTypesTable.grant_full_access(addMachineType)

        #edit machine name
        editMachineName = _lambda.Function(
            self, 'EditMachineName',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='edit_machine_name.editMachineNameHandler',
        )

        editMachineNameIntegration = apigw.LambdaIntegration(editMachineName)

        #Edit Machine Api
        apigw.LambdaRestApi(
            self, 'EditMachineNameAPI',
            handler=editMachineName
        )

        #Grant access to edit machine
        MachineTable.grant_full_access(editMachineName)

        #delete machine
        deleteMachine = _lambda.Function(
            self, 'DeleteMachine',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='delete_machine.deleteMachineHandler',
        )

        deleteMachineIntegration = apigw.LambdaIntegration(deleteMachine)

        #Delete Machine Api
        apigw.LambdaRestApi(
            self, 'DeleteMachineAPI',
            handler=deleteMachine
        )

        #Granting Access to Delete Machine 
        ParentTable.grant_full_access(deleteMachine)
        ChildTable.grant_full_access(deleteMachine)
        MachineTable.grant_full_access(deleteMachine)
        MachineTypesTable.grant_full_access(deleteMachine)
        ParentIndex.grant_full_access(deleteMachine)

        #delete machine type
        deleteMachineType = _lambda.Function(
            self, 'DeleteMachineType',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/machine'),
            handler='delete_machine_type.deleteMachineTypeHandler',
        )

        deleteMachineTypeIntegration = apigw.LambdaIntegration(deleteMachineType)

        #Delete Machine Type Api
        apigw.LambdaRestApi(
            self, 'DeleteMachineTypeAPI',
            handler=deleteMachineType
        )

        #Granting Access to Delete Machine Type
        MachineTypesTable.grant_full_access(deleteMachineType)

    #------------------Task Functions/API---------------------

        #View Task Function
        ViewTask = _lambda.Function(
            self, 'ViewTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/task'),
            handler='ViewTask.ViewTaskHandler',
        )

        ViewTaskIntegration = apigw.LambdaIntegration(ViewTask)

        #View Task Api
        apigw.LambdaRestApi(
            self, 'ViewTaskApi',
            handler=ViewTask
        )

        #Granting Access for View Task
        ChildTable.grant_full_access(ViewTask)
        ParentTable.grant_full_access(ViewTask)

        #Create Task Function
        CreateTask = _lambda.Function(
            self, 'CreateTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/task'),
            handler='CreateTask.CreateTaskHandler',
        )

        CreateTaskIntegration = apigw.LambdaIntegration(CreateTask)

        #Create Task Api
        apigw.LambdaRestApi(
            self, 'CreateTaskApi',
            handler=CreateTask
        )

        #Granting Access for Create Task
        ChildTable.grant_full_access(CreateTask)
        ParentTable.grant_full_access(CreateTask)
        MachineTable.grant_full_access(CreateTask)

        #Edit Task Function
        EditTask = _lambda.Function(
            self, 'EditTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/task'),
            handler='EditTask.EditTaskHandler',
            timeout=core.Duration.seconds(30)
        )

        EditTaskIntegration = apigw.LambdaIntegration(EditTask)

        #Edit Task Api
        apigw.LambdaRestApi(
            self, 'EditTaskApi',
            handler=EditTask
        )

        #Granting Access for Edit Task
        ChildTable.grant_full_access(EditTask)
        ParentIndex.grant_full_access(EditTask)
        ParentTable.grant_full_access(EditTask)
        MachineTable.grant_full_access(EditTask)

        #View Upcoming Tasks Function
        ViewUpcomingTasks = _lambda.Function(
            self, 'ViewUpcomingTasks',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/task'),
            handler='ViewUpcomingTasks.ViewUpcomingTasksHandler'
        )

        ViewUpcomingTasksIntegration = apigw.LambdaIntegration(ViewUpcomingTasks)

        #View Upcoming Tasks API
        apigw.LambdaRestApi(
            self, 'ViewUpcomingTasksApi',
            handler=ViewUpcomingTasks
        )

        #Granting Access for View Upcoming Tasks
        ChildTable.grant_full_access(ViewUpcomingTasks)

        #Delete Task Function
        DeleteTask = _lambda.Function(
            self, 'DeleteTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/task'),
            handler='DeleteTask.DeleteTaskHandler',
            timeout=core.Duration.seconds(30)
        )

        DeleteTaskIntegration = apigw.LambdaIntegration(DeleteTask)

        #Delete Task Api
        apigw.LambdaRestApi(
            self, 'DeleteTaskApi',
            handler=DeleteTask
        )

        #Granting Access for Delete Task
        ChildTable.grant_full_access(DeleteTask)
        ParentIndex.grant_full_access(DeleteTask)
        ParentTable.grant_full_access(DeleteTask)
        MachineTable.grant_full_access(DeleteTask)

        #Complete Task Function
        CompleteTask = _lambda.Function(
            self, 'CompleteTask',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/task'),
            handler='CompleteTask.CompleteTaskHandler',
            timeout=core.Duration.seconds(10)
        )

        CompleteTaskIntegration = apigw.LambdaIntegration(CompleteTask)

        #Complete Task Api
        apigw.LambdaRestApi(
            self, 'CompleteTaskApi',
            handler=CompleteTask
        )

        #Granting Access for Complete Task
        ChildTable.grant_full_access(CompleteTask)

    #------------------Reporting Functions/API------------------




        # View Machine History Function
        ViewMachineHistory = _lambda.Function(
            self, 'ViewMachineHistory',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/reporting'),
            handler='ViewMachineHistory.ViewMachineHistoryHandler',
            timeout=core.Duration.seconds(30)
        )

        #View Machine History Api
        apigw.LambdaRestApi(
            self, 'ViewMachineHistoryApi',
            handler=ViewMachineHistory
        )

        #Granting Access for ViewMachine History
        ChildTable.grant_full_access(ViewMachineHistory)
        MachineTable.grant_full_access(ViewMachineHistory)
        ParentIndex.grant_full_access(ViewMachineHistory)
        
        # View History Function
        ViewHistory = _lambda.Function(
            self, 'ViewHistory',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/reporting'),
            handler='ViewHistory.ViewHistoryHandler',
            timeout=core.Duration.seconds(30)
        )

        #View History Api
        apigw.LambdaRestApi(
            self, 'ViewHistoryApi',
            handler=ViewHistory
        )

        #Granting Access for View History
        ChildTable.grant_full_access(ViewHistory)
        ParentIndex.grant_full_access(ViewHistory)
        ParentTable.grant_full_access(ViewHistory)

        #Export History Function
        ExportHistory = _lambda.Function(
            self, 'ExportHistory',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/reporting'),
            handler='ExportHistory.ExportHistoryHandler',
            initial_policy=[S3Policy],
            environment={'bucketName': ExportHistoryBucket.bucket_name},
            timeout=core.Duration.seconds(30)
        )

        #Export History Api
        apigw.LambdaRestApi(
            self, 'ExportHistoryApi',
            handler=ExportHistory
        )

        #Granting Access for Export History
        ChildTable.grant_full_access(ExportHistory)
        ParentTable.grant_full_access(ExportHistory)
        ParentIndex.grant_full_access(ExportHistory)

        #Export Machine History Function
        ExportMachineHistory = _lambda.Function(
            self, 'ExportMachineHistory',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/reporting'),
            handler='ExportMachineHistory.ExportMachineHistoryHandler',
            initial_policy=[S3Policy],
            environment={'bucketName': ExportMachineHistoryBucket.bucket_name},
            timeout=core.Duration.seconds(30)
        )

        #Export Machine History Api
        apigw.LambdaRestApi(
            self, 'ExportMachineHistoryApi',
            handler=ExportMachineHistory
        )

        #Granting Access for ExportMachine History
        ChildTable.grant_full_access(ExportMachineHistory)
        MachineTable.grant_full_access(ExportMachineHistory)
        ParentIndex.grant_full_access(ExportMachineHistory)

        #Update Report Email Function
        UpdateReportEmail = _lambda.Function(
            self, 'UpdateReportEmail',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/reporting'),
            handler='UpdateReportEmail.UpdateReportEmailHandler',
            initial_policy=[S3Policy],
            environment={'bucketName': NotificationBucket.bucket_name},
            timeout=core.Duration.seconds(30)
        )

        #Update Report Email Api
        apigw.LambdaRestApi(
            self, 'UpdateReportEmailApi',
            handler=UpdateReportEmail
        )

        #View Report Email Function
        ViewReportEmail = _lambda.Function(
            self, 'ViewReportEmail',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/reporting'),
            handler='ViewReportEmail.ViewReportEmailHandler',
            initial_policy=[S3Policy],
            environment={'bucketName': NotificationBucket.bucket_name},
            timeout=core.Duration.seconds(30)
        )

        #View Report Email Api
        apigw.LambdaRestApi(
            self, 'ViewReportEmailApi',
            handler=ViewReportEmail
        )


    #----------------Master API--------------------------
        um_api = apigw.LambdaRestApi()
        # /
        um_api.root.addMethod(httpMethod='ANY')

        # /tasks
        tasks = um_api.root.addResource('tasks')
        #
        tasks.addMethod(httpMethod='GET')
        # CreateTask
        tasks.addMethod(httpMethod='POST')

        # /tasks/{task_id}
        task = tasks.addResource('{task_id}')
        # ViewTask
        task.addMethod(httpMethod='GET')
        # DeleteTask
        task.addMethod(httpMethod='DELETE')
        # EditTask
        task.addMethod(httpMethod='PUT')
        # CompleteTask
        task.addMethod(httpMethod='POST')

        # /machines
        machines = um_api.root.addResource('machines')
        #
        machines.addMethod(httpMethod='GET')
        machines.addMethod(httpMethod='POST')

        # /machines/{machine_id}
        machine = machines.addResource('{machine_id}')
        machine.addMethod(httpMethod='GET')
        machine.addMethod(httpMethod='DELETE')
        machine.addMethod(httpMethod='PUT')


    #----------------Background Functions----------------

        #Maintain Tasks Function
        MaintainTasks = _lambda.Function(
            self, 'MaintainTasks',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/task'),
            handler='MaintainTasks.MaintainTasksHandler',
        )

        #Grant Access for MaintainTask
        ParentTable.grant_full_access(MaintainTasks)
        ChildTable.grant_full_access(MaintainTasks)
        ParentIndex.grant_full_access(MaintainTasks)

        #Rule For Maintain Tasks
        #MaintainTasksRule = events.Rule(self, 'MaintainTasksRule',
            #schedule=events.Schedule.cron(hour='20'),
            #targets=[targets.LambdaFunction(MaintainTasks)]
        #)

        #Notify Lead Function
        NotifyLead = _lambda.Function(
            self, 'NotifyLead',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/reporting'),
            handler='NotifyLead.NotifyLeadHandler',
            initial_policy=[S3Policy],
            environment={'bucketName': NotificationBucket.bucket_name},
            timeout=core.Duration.seconds(30)
        )

        #Grant Access for Notify Lead
        ChildTable.grant_full_access(NotifyLead)
        
        #Rule For Notify Lead
        #NotifyLeadRule = events.Rule(self, 'NotifyLeadRule',
            #schedule=events.Schedule.cron(hour='20'),
            #targets=[targets.LambdaFunction(NotifyLead)]
        #)

    #----------------Sign-In Lambdas----------------
    ### NOTE: Don't transfer over yet because these are RDS queries/editors
        #createUser
        #View machine types function
        createUser = _lambda.Function(
            self, 'createUser',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/signIn'),
            handler='CreateUser.CreateUserHandler',
        )    
        #getMajors
        getMajor = _lambda.Function(
            self, 'getMajors',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/signIn'),
            handler='getMajors.getStudentInfoHandler',
        )    
        #getStudentInfo
        getStudentInfo = _lambda.Function(
            self, 'getStudentInfo',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/signIn'),
            handler='getStudentInfo.getStudentInfoHandler',
        )    
        #getTotals
        
        #insertNewStudent
        insertNewStudent = _lambda.Function(
            self, 'insertNewStudent',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/signIn'),
            handler='insertNewStudent.insertNewStudentHandler',
        )    
        #isCardInDatabase
        isCardInDatabase = _lambda.Function(
            self, 'isCardInDatabase',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('maintenance_app/lambda-functions/signIn'),
            handler='isCardInDatabase.isCardInDatabaseHandler',
        )

        #Lambda@Edge authenticator

