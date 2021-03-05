#!/usr/bin/env python3

from aws_cdk import core
from maintenance_app.maintenance_app_stack import MaintenanceAppStack


app = core.App()
MaintenanceAppStack(app, "maintenance-app")

app.synth()
