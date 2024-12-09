
# This stack is based on the following blog post:
# https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/
from aws_cdk import (
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
    def __init__(self, app: App, id: str, *,
                 env: Environment) -> None:
        super().__init__(app, id, env=env)

        # Define our pipeline
        #
        # Our pipeline will automatically create the following stages:
        # Source          – This stage is probably familiar. It fetches the source of your CDK app from your forked
        #                   GitHub repo and triggers the pipeline every time you push new commits to it.
        # Build           – This stage compiles your code (if necessary) and performs a cdk synth. The output of that
        #                   step is a cloud assembly, which is used to perform all actions in the rest of the pipeline.
        # UpdatePipeline  – This stage modifies the pipeline if necessary. For example, if you update your code to add
        #                   a new deployment stage to the pipeline or add a new asset to your application, the pipeline
        #                   is automatically updated to reflect the changes you made.
        # PublishAssets   – This stage prepares and publishes all file assets you are using in your app to Amazon Simple
        #                   Storage Service (Amazon S3) and all Docker images to Amazon Elastic Container Registry
        #                   (Amazon ECR) in every account and Region from which it’s consumed, so that they can be used
        #                   during the subsequent deployments.
        
        # Active listener on the designated branch in the Unified Makerspace Repo
        codestar_source = CodePipelineSource.connection("clemsonMakerspace/unified-makerspace", "mainline",
                connection_arn="arn:aws:codestar-connections:us-east-1:944207523762:connection/0d26aa24-5271-44cc-b436-3ddd4e2c9842"
            )
        
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
                f'VITE_API_ENDPOINT="https://{Domains("Beta").api}" npm run build',
                'mkdir -p ../../cdk/visit/console/Beta',
                'cp -r dist/* ../../cdk/visit/console/Beta',

                # build for prod
                f'VITE_API_ENDPOINT="https://{Domains("Prod").api}" npm run build',
                'mkdir -p ../../cdk/visit/console/Prod',
                'cp -r dist/* ../../cdk/visit/console/Prod',
                
                'cd ../..',

                # synth the app
                "cd cdk",
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
                "TestBetaAPIEndpoints",
                input=codestar_source, # pass entire codestar connection to repo
                commands=[
                    "pwd",
                    "pip install pytest --force-reinstall",
                    # "pip install python3 --force-reinstall",
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
        #         "TestProdAPIEndpoints",
        #         input=codestar_source, # pass entire codestar connection to repo
        #         commands=[
        #             "ENV=Prod python3 cdk/visit/lambda_code/test_api/testing_script.py",
        #         ],
        #     )
        # )

