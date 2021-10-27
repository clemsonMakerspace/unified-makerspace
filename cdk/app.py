#!/usr/bin/env python3

from aws_cdk import core
from maintenance_app.maintenance_app_stack import MaintenanceAppStack
from pipeline import Pipeline
from dns import MakerspaceDns
from accounts_config import accounts

from makerspace import MakerspaceStack

app = core.App()

"""
Section 1: Global resources that exist in only one account

The DNS records shared by all of the organization accounts exist in
the Prod account to discourage changing them. This is due to the
security concerns posed by using Route53 NS records. See the
below blog post for details:

https://nabeelxy.medium.com/dangling-dns-records-are-a-real-vulnerability-361f2a29d37f

Also, all Pipeline-related resources go here, because we don't deploy
those directly. Instead, we use the Pipline's self-mutation to update
all the child stacks. So, everything beta/prod goes here.
"""
pipeline = Pipeline(app, 'Pipeline', env=accounts['Prod'])


"""
Section 2: Resources that exist within the same account

This section is for the alpha or development environments. For
these, we need to deploy each by hand, and each user should have the
only credentials that deploy to their own dev account. This loop
generates a stack for each user that deploys to their own account.
"""
for user in ['mhall6', 'kejiax', 'ddejesu', 'dwball', 'weiminl']:

    stage = f'Dev-{user}'
    environment = accounts[stage]

    MakerspaceStack(app, stage, env=environment)

app.synth()
