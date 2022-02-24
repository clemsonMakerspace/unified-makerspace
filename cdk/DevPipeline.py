from aws_cdk import (
    core
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, ManualApprovalStep

from makerspace import MakerspaceStage
from accounts_config import accounts

class DevPipeline(core.Stack):
    def __init__(self, app: core.App, id: str, *,
                 env: core.Environment) -> None:
        super().__init__(app, id, env=env)

        deploy_cdk_shell_step = ShellStep("Synth",
            input=CodePipelineSource.connection("Mjtlittle/unified-makerspace", "pipeline-development",
                connection_arn="arn:aws:codestar-connections:us-east-1:577283310524:connection/2e5ad00f-c205-4b57-a752-6aa33d55236c"
            ),
            commands=[
                
                # build for site A
                'cd site/visitor-console',
                'npm install',

                'VITE_API_ENDPOINT="https://A" npm run build',
                'mkdir -p ../../cdk/visit/console/DevA',
                'cp -r dist/* ../../cdk/visit/console/DevA',

                'VITE_API_ENDPOINT="https://B" npm run build',
                'mkdir -p ../../cdk/visit/console/DevB',
                'cp -r dist/* ../../cdk/visit/console/DevB',

                'cd ../..',

                # deploy cdk
                "cd cdk",
                "npm install -g aws-cdk && pip install -r requirements.txt",
                "cdk synth"
            ],
            primary_output_directory="cdk/cdk.out",
        )

        deploy_cdk_shell_step.add_output_directory("cdk/visit/console/DevA")
        deploy_cdk_shell_step.add_output_directory("cdk/visit/console/DevB")
        
        pipeline = CodePipeline(self, "Pipeline",
            synth=deploy_cdk_shell_step,
            cross_account_keys=True
        )
        
        self.a = MakerspaceStage(self, 'DevA', env=accounts['Dev-jlittl8'])
        pipeline.add_stage(self.a)

        self.b = MakerspaceStage(self, 'DevB', env=accounts['Dev-jlittl8'])
        pipeline.add_stage(self.b,
            pre=[ManualApprovalStep("PromoteToDevB")]
        )