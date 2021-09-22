#!/usr/bin/env python3

# test change
from aws_cdk import core
from maintenance_app.maintenance_app_stack import MaintenanceAppStack
from Pipeline import Pipeline

props = {'namespace': 'unified-makerspace'}
app = core.App()

maintenance_app = MaintenanceAppStack(
    app, f"{props['namespace']}-maintenance-app")

pipeline = Pipeline(app, f"{props['namespace']}-pipeline", props)
# pipeline.add_dependency(maintenance_app)

app.synth()
