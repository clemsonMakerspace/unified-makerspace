#!/usr/bin/env python3

from aws_cdk import core
from maintenance_app.maintenance_app_stack import MaintenanceAppStack
from Pipeline import Pipeline
from Pipeline import stage, school

props = {
    'namespace': 'unified-makerspace',
    'env': core.Environment(
        account='944207523762',
        region='us-east-1')}
app = core.App()

maintenance_app = MaintenanceAppStack(
    app, f"{props['namespace']}-maintenance-app", stage, school)

pipeline = Pipeline(app, f"{props['namespace']}-pipeline", env=props['env'])
# pipeline.add_dependency(maintenance_app)

app.synth()
