# This stack is based on the following blog post:
# https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/
from aws_cdk import Environment, Stack
from aws_cdk import pipelines as pipelines
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct

from accounts_config import accounts
from dns import Domains
from makerspace import MakerspaceStage


class Pipeline(Stack):
    def __init__(self, app: Construct, id: str, *, env: Environment) -> None:
        super().__init__(app, id, env=env)

        deploy_cdk_shell_step = ShellStep(
            "Synth",
            # use a connection created using the AWS console to authenticate to GitHub.
            input=CodePipelineSource.connection(
                "clemsonMakerspace/unified-makerspace",
                "mainline",
                connection_arn="arn:aws:codestar-connections:us-east-1:944207523762:connection/0d26aa24-5271-44cc-b436-3ddd4e2c9842",
            ),
            commands=[
                # install dependancies for frontend
                "cd site/visitor-console",
                "npm install",
                # build for beta
                f'VITE_API_ENDPOINT="https://{Domains("Beta").api}" npm run build',
                "mkdir -p ../../cdk/visit/console/Beta",
                "cp -r dist/* ../../cdk/visit/console/Beta",
                # build for prod
                f'VITE_API_ENDPOINT="https://{Domains("Prod").api}" npm run build',
                "mkdir -p ../../cdk/visit/console/Prod",
                "cp -r dist/* ../../cdk/visit/console/Prod",
                "cd ../..",
                # synth the app
                "cd cdk",
                "ls",
                "npm install -g aws-cdk",
                "pip install -r requirements.txt",
                "cdk synth",
            ],
            primary_output_directory="cdk/cdk.out",
        )

        pipeline = CodePipeline(
            self,
            "Pipeline",
            synth=deploy_cdk_shell_step,
            cross_account_keys=True,  # necessary to allow the prod account to access our artifact bucket
        )

        # Test beta
        self.beta = MakerspaceStage(self, "Beta", env=accounts["Beta"])
        deploy_stage = pipeline.add_stage(self.beta)
        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestViewerEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": self.beta.hc_viewer_url},
                commands=["curl -Ssf $ENDPOINT_URL"],
            )
        )

        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestAPIGatewayEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": self.beta.hc_endpoint},
                commands=[
                    "curl --location -X POST $ENDPOINT_URL/visit",
                ],
            )
        )

        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestBetaFrontend",
                commands=[
                    "curl https://beta-visit.cumaker.space/",
                ],
            )
        )

        # test prod
        self.prod = MakerspaceStage(self, "Prod", env=accounts["Prod"])
        deploy_stage = pipeline.add_stage(self.prod)
        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestViewerEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": self.prod.hc_viewer_url},
                commands=["curl -Ssf $ENDPOINT_URL"],
            )
        )

        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestAPIGatewayEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": self.prod.hc_endpoint},
                commands=[
                    "curl --location -X POST $ENDPOINT_URL/visit",
                ],
            )
        )

        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestProdFrontend",
                commands=[
                    "curl https://visit.cumaker.space/",
                ],
            )
        )
