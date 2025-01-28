
# This stack is based on the following blog post:
# https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/
from aws_cdk import (
    aws_secretsmanager,
    SecretValue,
    App,
    Stack,
    Environment
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, ManualApprovalStep
from makerspace import MakerspaceStage
from dns import Domains
# from constructs import Construct
from accounts_config import accounts

class Pipeline(Stack):
    """
    The Pipeline stack sets up a CI/CD pipeline for the Makerspace application, automating
    the deployment process across Beta and Prod environments. This stack is based on the 
    blog post: 
    https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/

    Define our pipeline:
    The pipeline automatically creates and manages the following stages:
    - **Source**: Fetches the source code from the GitHub repository and triggers the pipeline 
                  on new commits.
    - **Build**: Compiles the application (if necessary) and synthesizes the CDK application. 
                 The output is a Cloud Assembly used for subsequent stages.
    - **UpdatePipeline**: Updates the pipeline itself when changes are made, such as adding a new 
                          deployment stage or assets.
    - **PublishAssets**: Publishes file assets to S3 and Docker images to ECR in relevant accounts 
                         and regions for use during deployments.
    - **Beta Deployment**: Deploys the application to the Beta environment and tests the frontend 
                           and backend endpoints.
    - **Prod Deployment**: Promotes the Beta deployment to Prod after manual approval and tests 
                           the frontend and backend endpoints.

    Parameters:
    - app (App): The parent application that owns this stack.
    - id (str): The unique identifier for this stack.
    - env (Environment): The AWS environment where the stack is deployed, including account and region.

    Key Features:
    - **Pipeline Definition**:
        - Automatically triggers on commits to the specified branch in the Unified Makerspace repo.
        - Includes stages for building, testing, and deploying the application.
    - **Beta Stage**:
        - Deploys the application to the Beta environment.
        - Tests the Beta frontend (CloudFront) and backend (Lambda functions).
    - **Prod Stage**:
        - Promotes the Beta deployment to Prod with manual approval.
        - Tests the Prod frontend (CloudFront).
    - **Secrets Management**:
        - Retrieves the backend API key from AWS Secrets Manager.
    - **Shell Steps**:
        - Performs operations such as dependency installation, environment variable setup, 
          and CDK synthesis.

    Notes:
    - The pipeline uses cross-account keys to allow the Prod account to access the artifact bucket.
    - Build commands ensure compatibility by removing old CDK V1 dependencies and setting up 
      environment variables for the visitor console frontend.

    Documentation Links:
        - aws_cdk.pipelines.CodePipeline:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        - aws_cdk.pipelines.CodePipelineSource:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html
        - aws_cdk.pipelines.ShellStep:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html
        - aws_cdk.pipelines.ManualApprovalStep:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ManualApprovalStep.html
        - aws_secretsmanager.Secret:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_secretsmanager/Secret.html
        - aws_secretsmanager.SecretValue:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_secretsmanager/SecretValue.html
    """
    def __init__(self, app: App, id: str, *,
                 env: Environment) -> None:
        super().__init__(app, id, env=env)
        
        # Active listener on the designated branch in the Unified Makerspace Repo
        codestar_source = CodePipelineSource.connection("clemsonMakerspace/unified-makerspace", "mainline",
                connection_arn="arn:aws:codestar-connections:us-east-1:944207523762:connection/0d26aa24-5271-44cc-b436-3ddd4e2c9842"
            )
        
        # Retrieve backend api key for beta and prod from secrets manager
        beta_secret_name: str = "BetaSharedApiGatewayKey"
        prod_secret_name: str = "ProdSharedApiGatewayKey"
        beta_shared_secrets = aws_secretsmanager.Secret.from_secret_name_v2(
                self, 
                "BetaSharedGatewaySecrets",
                beta_secret_name
        )
        beta_shared_api_key: SecretValue = beta_shared_secrets.secret_value_from_json("api_key")

        prod_shared_secrets = aws_secretsmanager.Secret.from_secret_name_v2(
                self, 
                "ProdSharedGatewaySecrets",
                prod_secret_name
        )
        prod_shared_api_key: SecretValue = prod_shared_secrets.secret_value_from_json("api_key")

        # Commands used to build pipeline in the Build stage
        deploy_cdk_shell_step = ShellStep("Synth",
            # Use a connection created using the AWS console to authenticate to GitHub
            input=codestar_source,
            commands=[    
                # Clear the CDK context cache and remove old cdk.out file
                'rm -rf /tmp/* || echo "No /tmp/ folder present"',
                'rm -f .cdk.context.json || echo "No context cache to clear"',
                'rm -rf cdk.out || echo "No output directory to clear"',
                
                # Uninstall all AWS CDK V1 packages 
                "pip uninstall -y 'aws-cdk.*' || echo 'No CDK V1 packages found'",
                
                # install dependancies for frontend
                'cd site/visitor-console',
                'npm install',

                # build for beta
                f'echo "VITE_BACKEND_KEY={beta_shared_api_key.unsafe_unwrap()}" > .env',
                f'VITE_API_ENDPOINT="https://{Domains("Beta").api}" npm run build',
                'mkdir -p ../../cdk/visit/console/Beta',
                'cp -r dist/* ../../cdk/visit/console/Beta',

                # build for prod
                f'echo "VITE_BACKEND_KEY={prod_shared_api_key.unsafe_unwrap()}" > .env',
                f'VITE_API_ENDPOINT="https://{Domains("Prod").api}" npm run build',
                'mkdir -p ../../cdk/visit/console/Prod',
                'cp -r dist/* ../../cdk/visit/console/Prod',
                
                # cd to cdk directory
                'cd ../../cdk',

                # cd to api_gateway/lambda_code directory
                'cd api_gateway/lambda_code',

                # Copy the api_defaults.py file to all the handler lambda
                # asset directories it is needed as a module in.
                "for dir in $(find . -type d -name '*handler'); do cp api_defaults.py $dir; done",

                # cd back to cdk directory
                'cd ../../',

                # synth the app
                "npm install -g aws-cdk && pip install -r requirements.txt --force-reinstall",
                "cdk synth"
            ],
            primary_output_directory="cdk/cdk.out",
        )
        
        # Create Pipeline object
        pipeline = CodePipeline(self, "Pipeline",
            synth=deploy_cdk_shell_step, # Pass in commands from Shell Step
            cross_account_keys=True  # Necessary to allow the prod account to access our artifact bucket
        )
        
        # Create the stack for beta
        self.beta_stage = MakerspaceStage(self, 'Beta', env=accounts['Beta'])
        beta_deploy_stage = pipeline.add_stage(self.beta_stage)

        # Curl beta frontend
        beta_deploy_stage.add_post(
            ShellStep(
                "TestBetaCloudfrontEndpoint",
                commands=[
                    "curl https://beta-visit.cumaker.space/",
                ],
            )
        )

        beta_deploy_stage.add_post(
            ShellStep(
                "TestBetaBackendHandlers",
                input=codestar_source, # pass entire codestar connection to repo
                commands=[
                    "pip install pytest --force-reinstall",
                    # "pip install python3 --force-reinstall",
                    "pip install moto --force-reinstall",
                    "pip install aws-cdk-lib constructs --force-reinstall",
                    "pip install boto3 --force-reinstall",
                    "PYTHONPATH=cdk/api_gateway/ python3 -m pytest -vs --import-mode=importlib --disable-warnings cdk/api_gateway/tests"
                ],
            )
        )

        # Create the stack for prod
        self.prod_stage = MakerspaceStage(self, 'Prod', env=accounts['Prod'])
        prod_deploy_stage = pipeline.add_stage(self.prod_stage, 
            pre=[ManualApprovalStep("PromoteBetaToProd")]
        )

        # Curl prod frontend
        prod_deploy_stage.add_post(
            ShellStep(
                "TestingProdCloudfrontEndpoint",
                commands=[
                    "curl https://visit.cumaker.space/",
                ],
            )
        )

        # Run API Endpoint test script for Prod
        # prod_deploy_stage.add_post(
        #     ShellStep(
        #         "TestProdBackendHandlers",
        #         input=codestar_source, # pass entire codestar connection to repo
        #         commands=[
        #             "ENV=Prod python3 cdk/visit/lambda_code/test_api/testing_script.py",
        #         ],
        #     )
        # )

