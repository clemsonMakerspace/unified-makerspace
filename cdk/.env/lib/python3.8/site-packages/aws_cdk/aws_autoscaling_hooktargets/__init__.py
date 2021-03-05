"""
# Lifecycle Hook for the CDK AWS AutoScaling Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains integration classes for AutoScaling lifecycle hooks.
Instances of these classes should be passed to the
`autoScalingGroup.addLifecycleHook()` method.

Lifecycle hooks can be activated in one of the following ways:

* Invoke a Lambda function
* Publish to an SNS topic
* Send to an SQS queue

For more information on using this library, see the README of the
`@aws-cdk/aws-autoscaling` library.

For more information about lifecycle hooks, see
[Amazon EC2 AutoScaling Lifecycle hooks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html) in the Amazon EC2 User Guide.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_autoscaling
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.core


@jsii.implements(aws_cdk.aws_autoscaling.ILifecycleHookTarget)
class FunctionHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling-hooktargets.FunctionHook",
):
    """Use a Lambda Function as a hook target.

    Internally creates a Topic to make the connection.
    """

    def __init__(
        self,
        fn: aws_cdk.aws_lambda.IFunction,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """
        :param fn: Function to invoke in response to a lifecycle event.
        :param encryption_key: If provided, this key is used to encrypt the contents of the SNS topic.
        """
        jsii.create(FunctionHook, self, [fn, encryption_key])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        lifecycle_hook: aws_cdk.aws_autoscaling.ILifecycleHook,
    ) -> aws_cdk.aws_autoscaling.LifecycleHookTargetConfig:
        """Called when this object is used as the target of a lifecycle hook.

        :param scope: -
        :param lifecycle_hook: -
        """
        return jsii.invoke(self, "bind", [scope, lifecycle_hook])


@jsii.implements(aws_cdk.aws_autoscaling.ILifecycleHookTarget)
class QueueHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling-hooktargets.QueueHook",
):
    """Use an SQS queue as a hook target."""

    def __init__(self, queue: aws_cdk.aws_sqs.IQueue) -> None:
        """
        :param queue: -
        """
        jsii.create(QueueHook, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: aws_cdk.core.Construct,
        lifecycle_hook: aws_cdk.aws_autoscaling.ILifecycleHook,
    ) -> aws_cdk.aws_autoscaling.LifecycleHookTargetConfig:
        """Called when this object is used as the target of a lifecycle hook.

        :param _scope: -
        :param lifecycle_hook: -
        """
        return jsii.invoke(self, "bind", [_scope, lifecycle_hook])


@jsii.implements(aws_cdk.aws_autoscaling.ILifecycleHookTarget)
class TopicHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling-hooktargets.TopicHook",
):
    """Use an SNS topic as a hook target."""

    def __init__(self, topic: aws_cdk.aws_sns.ITopic) -> None:
        """
        :param topic: -
        """
        jsii.create(TopicHook, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: aws_cdk.core.Construct,
        lifecycle_hook: aws_cdk.aws_autoscaling.ILifecycleHook,
    ) -> aws_cdk.aws_autoscaling.LifecycleHookTargetConfig:
        """Called when this object is used as the target of a lifecycle hook.

        :param _scope: -
        :param lifecycle_hook: -
        """
        return jsii.invoke(self, "bind", [_scope, lifecycle_hook])


__all__ = [
    "FunctionHook",
    "QueueHook",
    "TopicHook",
]

publication.publish()
