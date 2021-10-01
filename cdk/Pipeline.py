from aws_cdk import (
    aws_codepipeline,
    aws_codepipeline_actions,
    core,
)

from maintenance_app.maintenance_app_stack import MaintenanceAppStack


class Pipeline(core.Stack):
    def __init__(self, app: core.App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Define some variables
        bucket = {'desired_bucket' : 'clemson_prod'}
        oauth = core.SecretValue.secrets_manager('github-token')
        source_output = aws_codepipeline.Artifact(artifact_name='source')

        # define the pipeline
        pipeline = aws_codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name=f"{props['namespace']}",
        )

        source_stage = pipeline.add_stage(stage_name='FetchSource')
        source_stage.add_action(aws_codepipeline_actions.GitHubSourceAction(
            oauth_token=oauth,
            output=source_output,
            owner='clemsonMakerspace',
            repo='unified-makerspace',
            action_name='GitHubSource'
        ))

        # beta_stage = pipeline.add_stage(stage_name='Beta')
        # beta_stage.add_action()

        approval_stage = pipeline.add_stage(stage_name='ManualApproval')
        approval_stage.add_action(
            aws_codepipeline_actions.ManualApprovalAction(action_name='ManualApproval'))

        # prod_stage = pipeline.add_stage(stage_name='Prod')
        # prod_stage.add_action()
