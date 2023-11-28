
from aws_cdk import core, aws_lambda as _lambda, aws_iam, aws_apigateway as apigateway

def setup_analytics(stack: core.Stack):
    # IAM Role for Lambda
    lambda_role = aws_iam.Role(
        stack, 'DashboardGeneratorRole',
        assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambda_FullAccess'),
        ]
    )
    lambda_role.add_to_policy(aws_iam.PolicyStatement(
        effect=aws_iam.Effect.ALLOW,
        actions=[
            'quicksight:DescribeDashboard',
            'quicksight:GetDashboardEmbedUrl',
            'quicksight:GetAuthCode'
        ],
        resources=['*'],
    ))

    # Lambda definition
    lambda_dashboard_generator = _lambda.Function(
        stack,
        "QuickSightDashboardGenerator",
        runtime=_lambda.Runtime.PYTHON_3_8,
        handler="dashboard_generator.lambda_handler",
        code=_lambda.Code.from_asset('visit/lambda_code/quicksight'),
        role=lambda_role,
        environment={
            'AWS_ACCOUNT_ID': '366442540808',  
            'DASHBOARD_ID': 'b153dda9-d2f2-4829-9f5d-df80daddda2d',
            'QUICKSIGHT_USER_ARN': 'arn:aws:quicksight:us-east-1:366442540808:user/default/AWSReservedSSO_AdministratorAccess_d2a4def0109cee0d/soll'
        }
    )

    # API Gateway REST API
    api = apigateway.RestApi(
        stack,
        'DashboardAPI',
        rest_api_name='QSDashboardEmbedAPI',
        description='API for generating QuickSight dashboard embed URLs.'
    )

    # Lambda integration
    lambda_integration = apigateway.LambdaIntegration(
        lambda_dashboard_generator,
        request_templates={"application/json": '{ "statusCode": "200" }'}
    )

    dashboard_resource = api.root.add_resource('dashboard')
    dashboard_resource.add_method('GET', lambda_integration)

    core.CfnOutput(
        stack,
        "QSDashboardAPIUrl",
        value=api.url,
        description="URL for the QuickSight Dashboard Embed URL API"
    )
