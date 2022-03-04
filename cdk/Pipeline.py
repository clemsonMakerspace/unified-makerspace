# This stack is based on the following blog post:
# https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/
from aws_cdk import (
    core
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from makerspace import MakerspaceStage

from accounts_config import accounts


class Pipeline(core.Stack):
    def __init__(self, app: core.App, id: str, *,
                 env: core.Environment) -> None:
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
        deploy_cdk_shell_step = ShellStep("Synth",
            # Use a connection created using the AWS console to authenticate to GitHub
            # Other sources are available.
            input=CodePipelineSource.connection("clemsonMakerspace/unified-makerspace", "mainline",
                connection_arn="arn:aws:codestar-connections:us-east-1:944207523762:connection/0d26aa24-5271-44cc-b436-3ddd4e2c9842"
            ),
            commands=[
                # deploy cdk
                "cd cdk",  # TODO: Remove when we deprecate `cdk/`
                "npm install -g aws-cdk && pip install -r requirements.txt",
                "cdk synth"

                # TODO: "pytest unittest"
            ],
            primary_output_directory="cdk/cdk.out", # TODO: Remove when we deprecate `cdk/`
        )
        
        pipeline = CodePipeline(self, "Pipeline",
            synth=deploy_cdk_shell_step,
            cross_account_keys=True  # Necessary to allow the prod account to access our artifact bucket
        )
        

        # Now that our CodePipeline is created we can call `addStage` as many times as
        # necessary with any account and region (may be different from the
        # pipeline's).

        # Create our Beta stage
        self.beta = MakerspaceStage(self, 'Beta', env=accounts['Beta'])
        pipeline.add_stage(self.beta)

        # TODO: Add a validation stage before deploying to Prod

        # Create our Prod stage
        self.prod = MakerspaceStage(self, 'Prod', env=accounts['Prod'])
        pipeline.add_stage(self.prod)

