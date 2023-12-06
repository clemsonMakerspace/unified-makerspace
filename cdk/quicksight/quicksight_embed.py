# analytics_construct.py
from aws_cdk import core, aws_lambda as _lambda, aws_iam, aws_apigateway as apigateway

class QuickSightEmbedConstruct(core.Construct):
    def __init__(self, scope: core.Construct, id: str, aws_account_id: str, dashboard_id: str, quicksight_user_arn: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # IAM Role for Lambda
        lambda_role = aws_iam.Role(
            self, 'DashboardGeneratorRole',
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
            self,
            "QuickSightDashboardGenerator",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="dashboard_generator.lambda_handler",
            code=_lambda.Code.from_asset('visit/lambda_code/quicksight'),
            role=lambda_role,
            environment={
                'AWS_ACCOUNT_ID': aws_account_id,
                'DASHBOARD_ID': dashboard_id,
                'QUICKSIGHT_USER_ARN': quicksight_user_arn
            }
        )

        # API Gateway REST API
        allowed_origins = ['https://visit.cumaker.space']

        api = apigateway.RestApi(
            self,
            'DashboardAPI',
            rest_api_name='QSDashboardEmbedAPI',
            description='API for generating QuickSight dashboard embed URLs.',
             default_cors_preflight_options=apigateway.CorsOptions(
                 allow_origins = allowed_origins,
                 allow_methods = ['GET']             
                 )
        )


        # Lambda integration
        lambda_integration = apigateway.LambdaIntegration(
            lambda_dashboard_generator,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method('GET', lambda_integration)

        # Outputs
        core.CfnOutput(
            self,
            "QSDashboardAPIUrl",
            value=api.url,
            description="URL for the QuickSight Dashboard Embed URL API"
        )
