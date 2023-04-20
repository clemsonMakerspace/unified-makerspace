# This stack is based on the following blog post:
# https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/
from aws_cdk import (
    Environment, App, Stack
)
from constructs import Construct


from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, ManualApprovalStep
from makerspace import MakerspaceStage

from accounts_config import accounts
from dns import Domains

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

        codestar_source = CodePipelineSource.connection("DillonRanwala/unified-makerspace", "cdk-v2-test",
                    connection_arn="arn:aws:codestar-connections:us-east-1:149497240198:connection/24ef657f-09b9-40ed-bdbf-7f57ea583228"
                )
        deploy_cdk_shell_step = ShellStep("Synth",
            # use a connection created using the AWS console to authenticate to GitHub
            input=codestar_source,
            commands=[    
                # install dependancies for frontend
                'cd site/visitor-console',
                'npm install',

                # build for dev
                f'VITE_API_ENDPOINT="https://{Domains("Dev").api}" npm run build', #Edit domain?
                'mkdir -p ../../cdk/visit/console/Dev',
                'cp -r dist/* ../../cdk/visit/console/Dev',

                # # build for beta
                # f'VITE_API_ENDPOINT="https://{Domains("Beta").api}" npm run build',
                # 'mkdir -p ../../cdk/visit/console/Beta',
                # 'cp -r dist/* ../../cdk/visit/console/Beta',

                # # build for prod
                # f'VITE_API_ENDPOINT="https://{Domains("Prod").api}" npm run build',
                # 'mkdir -p ../../cdk/visit/console/Prod',
                # 'cp -r dist/* ../../cdk/visit/console/Prod',
                
                'cd ../..',

                # synth the app
                "cd cdk",
                "npm install -g aws-cdk && pip install -r requirements.txt",
                "cdk synth"
            ],
            primary_output_directory="cdk/cdk.out",
        )
        
        pipeline = CodePipeline(self, "Pipeline",
            synth=deploy_cdk_shell_step,
            cross_account_keys=True  # necessary to allow the prod account to access our artifact bucket
        )
        
         # create the stack for dev
        deploy = MakerspaceStage(self, 'Dev2', env=accounts['Dev-dranwal'])
        deploy_stage = pipeline.add_stage(deploy)



  
        deploy_stage.add_post(
            ShellStep(
                "TestAPIEndpoints",
                input=codestar_source, # pass entire codestar connection to repo
                commands=[
                    "ls",
                    "pwd",
                    "ls ..",
                    "python3 cdk/visit/lambda_code/test_api/testing_script.py",

                ],
            )
        )

        # # create the stack for beta
        # self.beta_stage = MakerspaceStage(self, 'Beta', env=accounts['Beta'])
        # beta_deploy_stage = pipeline.add_stage(self.beta_stage)


        # curl beta frontend
        # beta_deploy_stage.add_post(
        #     ShellStep(
        #         "TestBetaCloudfrontEndpoint",
        #         commands=[
        #             "curl https://beta-visit.cumaker.space/",
        #         ],
        #     )
        # )

        # beta_deploy_stage.add_post(
        #     ShellStep(
        #         "TestBetaAPIEndpoints",
        #         input=codestar_source, # pass entire codestar connection to repo
        #         commands=[
        #             "ENV=Beta python3 cdk/visit/lambda_code/test_api/testing_script.py",
        #         ],
        #     )
        # )

        # create the stack for prod
        # self.prod_stage = MakerspaceStage(self, 'Prod', env=accounts['Prod'])
        # prod_deploy_stage = pipeline.add_stage(self.prod_stage, 
        #     pre=[ManualApprovalStep("PromoteBetaToProd")]
        # )

        # # curl prod frontend
        # prod_deploy_stage.add_post(
        #     ShellStep(
        #         "TestingProdCloudfrontEndpoint",
        #         commands=[
        #             "curl https://visit.cumaker.space/",
        #         ],
        #     )
        # )

        # prod_deploy_stage.add_post(
        #     ShellStep(
        #         "TestProdAPIEndpoints",
        #         input=codestar_source, # pass entire codestar connection to repo
        #         commands=[
        #             "ENV=Prod python3 cdk/visit/lambda_code/test_api/testing_script.py",
        #         ],
        #     )
        # )

