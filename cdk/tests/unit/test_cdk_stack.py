import json
import pytest

import aws_cdk_lib as core
from cdk.cdk_stack import CdkStack


def get_template():
    app = core.App()
    CdkStack(app, "cdk")
    return json.dumps(app.synth().get_stack("cdk").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
