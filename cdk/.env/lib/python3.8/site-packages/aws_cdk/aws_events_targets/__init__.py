"""
# Event Targets for Amazon EventBridge

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains integration classes to send Amazon EventBridge to any
number of supported AWS Services. Instances of these classes should be passed
to the `rule.addTarget()` method.

Currently supported are:

* Start a CodeBuild build
* Start a CodePipeline pipeline
* Run an ECS task
* Invoke a Lambda function
* Publish a message to an SNS topic
* Send a message to an SQS queue
* Start a StepFunctions state machine
* Queue a Batch job
* Make an AWS API call
* Put a record to a Kinesis stream
* Log an event into a LogGroup
* Put a record to a Kinesis Data Firehose stream

See the README of the `@aws-cdk/aws-events` library for more information on
EventBridge.

## LogGroup

Use the `LogGroup` target to log your events in a CloudWatch LogGroup.

For example, the following code snippet creates an event rule with a CloudWatch LogGroup as a target.
Every events sent from the `aws.ec2` source will be sent to the CloudWatch LogGroup.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_logs as logs
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets

log_group = logs.LogGroup(self, "MyLogGroup",
    log_group_name="MyLogGroup"
)

rule = events.Rule(self, "rule",
    event_pattern=EventPattern(
        source=["aws.ec2"]
    )
)

rule.add_target(targets.CloudWatchLogGroup(log_group))
```
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

import aws_cdk.aws_batch
import aws_cdk.aws_codebuild
import aws_cdk.aws_codepipeline
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class AwsApi(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.AwsApi"):
    """Use an AWS Lambda function that makes API calls as an event rule target."""

    def __init__(
        self,
        *,
        policy_statement: typing.Optional[aws_cdk.aws_iam.PolicyStatement] = None,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
    ) -> None:
        """
        :param policy_statement: The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call
        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters
        """
        props = AwsApiProps(
            policy_statement=policy_statement,
            action=action,
            service=service,
            api_version=api_version,
            catch_error_pattern=catch_error_pattern,
            parameters=parameters,
        )

        jsii.create(AwsApi, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: aws_cdk.aws_events.IRule,
        id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this AwsApi as a result from an EventBridge event.

        :param rule: -
        :param id: -
        """
        return jsii.invoke(self, "bind", [rule, id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.AwsApiInput",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "catch_error_pattern": "catchErrorPattern",
        "parameters": "parameters",
    },
)
class AwsApiInput:
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
    ) -> None:
        """Rule target input for an AwsApi target.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if catch_error_pattern is not None:
            self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def action(self) -> builtins.str:
        """The service action to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return result

    @builtins.property
    def service(self) -> builtins.str:
        """The service to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return result

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        """API version to use for the service.

        :default: - use latest available API version

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        """
        result = self._values.get("api_version")
        return result

    @builtins.property
    def catch_error_pattern(self) -> typing.Optional[builtins.str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors
        """
        result = self._values.get("catch_error_pattern")
        return result

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        :default: - no parameters

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("parameters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.AwsApiProps",
    jsii_struct_bases=[AwsApiInput],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "catch_error_pattern": "catchErrorPattern",
        "parameters": "parameters",
        "policy_statement": "policyStatement",
    },
)
class AwsApiProps(AwsApiInput):
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        policy_statement: typing.Optional[aws_cdk.aws_iam.PolicyStatement] = None,
    ) -> None:
        """Properties for an AwsApi target.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: The parameters for the service action. Default: - no parameters
        :param policy_statement: The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if catch_error_pattern is not None:
            self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy_statement is not None:
            self._values["policy_statement"] = policy_statement

    @builtins.property
    def action(self) -> builtins.str:
        """The service action to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return result

    @builtins.property
    def service(self) -> builtins.str:
        """The service to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return result

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        """API version to use for the service.

        :default: - use latest available API version

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        """
        result = self._values.get("api_version")
        return result

    @builtins.property
    def catch_error_pattern(self) -> typing.Optional[builtins.str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors
        """
        result = self._values.get("catch_error_pattern")
        return result

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        :default: - no parameters

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def policy_statement(self) -> typing.Optional[aws_cdk.aws_iam.PolicyStatement]:
        """The IAM policy statement to allow the API call.

        Use only if
        resource restriction is needed.

        :default: - extract the permission from the API call
        """
        result = self._values.get("policy_statement")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class BatchJob(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.BatchJob",
):
    """(experimental) Use an AWS Batch Job / Queue as an event rule target.

    :stability: experimental
    """

    def __init__(
        self,
        job_queue: aws_cdk.aws_batch.IJobQueue,
        job_definition: aws_cdk.aws_batch.IJobDefinition,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        job_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param job_queue: -
        :param job_definition: -
        :param attempts: (experimental) The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: (experimental) The name of the submitted job. Default: - Automatically generated
        :param size: (experimental) The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        :stability: experimental
        """
        props = BatchJobProps(
            attempts=attempts, event=event, job_name=job_name, size=size
        )

        jsii.create(BatchJob, self, [job_queue, job_definition, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """(experimental) Returns a RuleTarget that can be used to trigger queue this batch job as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule, _id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.BatchJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "attempts": "attempts",
        "event": "event",
        "job_name": "jobName",
        "size": "size",
    },
)
class BatchJobProps:
    def __init__(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        job_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        """(experimental) Customize the Batch Job Event Target.

        :param attempts: (experimental) The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: (experimental) The name of the submitted job. Default: - Automatically generated
        :param size: (experimental) The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if attempts is not None:
            self._values["attempts"] = attempts
        if event is not None:
            self._values["event"] = event
        if job_name is not None:
            self._values["job_name"] = job_name
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        """(experimental) The number of times to attempt to retry, if the job fails.

        Valid values are 1–10.

        :default: no retryStrategy is set

        :stability: experimental
        """
        result = self._values.get("attempts")
        return result

    @builtins.property
    def event(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """(experimental) The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        :default: the entire EventBridge event

        :stability: experimental
        """
        result = self._values.get("event")
        return result

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the submitted job.

        :default: - Automatically generated

        :stability: experimental
        """
        result = self._values.get("job_name")
        return result

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        """(experimental) The size of the array, if this is an array batch job.

        Valid values are integers between 2 and 10,000.

        :default: no arrayProperties are set

        :stability: experimental
        """
        result = self._values.get("size")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class CloudWatchLogGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.CloudWatchLogGroup",
):
    """Use an AWS CloudWatch LogGroup as an event rule target."""

    def __init__(
        self,
        log_group: aws_cdk.aws_logs.ILogGroup,
        *,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """
        :param log_group: -
        :param event: The event to send to the CloudWatch LogGroup. This will be the event logged into the CloudWatch LogGroup Default: - the entire EventBridge event
        """
        props = LogGroupProps(event=event)

        jsii.create(CloudWatchLogGroup, self, [log_group, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to log an event into a CloudWatch LogGroup.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class CodeBuildProject(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.CodeBuildProject",
):
    """Start a CodeBuild build when an Amazon EventBridge rule is triggered."""

    def __init__(
        self,
        project: aws_cdk.aws_codebuild.IProject,
        *,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        event_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """
        :param project: -
        :param event: The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        :param event_role: The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered. Default: - a new role will be created
        """
        props = CodeBuildProjectProps(event=event, event_role=event_role)

        jsii.create(CodeBuildProject, self, [project, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Allows using build projects as event rule targets.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.CodeBuildProjectProps",
    jsii_struct_bases=[],
    name_mapping={"event": "event", "event_role": "eventRole"},
)
class CodeBuildProjectProps:
    def __init__(
        self,
        *,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        event_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """Customize the CodeBuild Event Target.

        :param event: The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        :param event_role: The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered. Default: - a new role will be created
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if event is not None:
            self._values["event"] = event
        if event_role is not None:
            self._values["event_role"] = event_role

    @builtins.property
    def event(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The event to send to CodeBuild.

        This will be the payload for the StartBuild API.

        :default: - the entire EventBridge event
        """
        result = self._values.get("event")
        return result

    @builtins.property
    def event_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered.

        :default: - a new role will be created
        """
        result = self._values.get("event_role")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class CodePipeline(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.CodePipeline",
):
    """Allows the pipeline to be used as an EventBridge rule target."""

    def __init__(
        self,
        pipeline: aws_cdk.aws_codepipeline.IPipeline,
        *,
        event_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """
        :param pipeline: -
        :param event_role: The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created
        """
        options = CodePipelineTargetOptions(event_role=event_role)

        jsii.create(CodePipeline, self, [pipeline, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.CodePipelineTargetOptions",
    jsii_struct_bases=[],
    name_mapping={"event_role": "eventRole"},
)
class CodePipelineTargetOptions:
    def __init__(
        self,
        *,
        event_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """Customization options when creating a {@link CodePipeline} event target.

        :param event_role: The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if event_role is not None:
            self._values["event_role"] = event_role

    @builtins.property
    def event_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered.

        :default: - a new role will be created
        """
        result = self._values.get("event_role")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.ContainerOverride",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "command": "command",
        "cpu": "cpu",
        "environment": "environment",
        "memory_limit": "memoryLimit",
        "memory_reservation": "memoryReservation",
    },
)
class ContainerOverride:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        command: typing.Optional[typing.List[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.List["TaskEnvironmentVariable"]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param container_name: Name of the container inside the task definition.
        :param command: Command to run inside the container. Default: Default command
        :param cpu: The number of cpu units reserved for the container. Default: The default value from the task definition.
        :param environment: Variables to set in the container's environment.
        :param memory_limit: Hard memory limit on the container. Default: The default value from the task definition.
        :param memory_reservation: Soft memory limit on the container. Default: The default value from the task definition.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "container_name": container_name,
        }
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if environment is not None:
            self._values["environment"] = environment
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation

    @builtins.property
    def container_name(self) -> builtins.str:
        """Name of the container inside the task definition."""
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return result

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        """Command to run inside the container.

        :default: Default command
        """
        result = self._values.get("command")
        return result

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units reserved for the container.

        :default: The default value from the task definition.
        """
        result = self._values.get("cpu")
        return result

    @builtins.property
    def environment(self) -> typing.Optional[typing.List["TaskEnvironmentVariable"]]:
        """Variables to set in the container's environment."""
        result = self._values.get("environment")
        return result

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """Hard memory limit on the container.

        :default: The default value from the task definition.
        """
        result = self._values.get("memory_limit")
        return result

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        """Soft memory limit on the container.

        :default: The default value from the task definition.
        """
        result = self._values.get("memory_reservation")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class EcsTask(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.EcsTask"):
    """Start a task on an ECS cluster."""

    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        platform_version: typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param cluster: Cluster where service will be deployed.
        :param task_definition: Task Definition of the task that should be started.
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param platform_version: The platform version on which to run your task. Unless you have specific compatibility requirements, you don't need to specify this. Default: - ECS will set the Fargate platform version to 'LATEST'
        :param role: Existing IAM role to run the ECS task. Default: A new IAM role is created
        :param security_group: (deprecated) Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: How many tasks should be started when this event is triggered. Default: 1
        """
        props = EcsTaskProps(
            cluster=cluster,
            task_definition=task_definition,
            container_overrides=container_overrides,
            platform_version=platform_version,
            role=role,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            task_count=task_count,
        )

        jsii.create(EcsTask, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Allows using tasks as target of EventBridge events.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """(deprecated) The security group associated with the task.

        Only applicable with awsvpc network mode.

        :default: - A new security group is created.

        :deprecated: use securityGroups instead.

        :stability: deprecated
        """
        return jsii.get(self, "securityGroup")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroups")
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """The security groups associated with the task.

        Only applicable with awsvpc network mode.

        :default: - A new security group is created.
        """
        return jsii.get(self, "securityGroups")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.EcsTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "task_definition": "taskDefinition",
        "container_overrides": "containerOverrides",
        "platform_version": "platformVersion",
        "role": "role",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "task_count": "taskCount",
    },
)
class EcsTaskProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        platform_version: typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties to define an ECS Event Task.

        :param cluster: Cluster where service will be deployed.
        :param task_definition: Task Definition of the task that should be started.
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param platform_version: The platform version on which to run your task. Unless you have specific compatibility requirements, you don't need to specify this. Default: - ECS will set the Fargate platform version to 'LATEST'
        :param role: Existing IAM role to run the ECS task. Default: A new IAM role is created
        :param security_group: (deprecated) Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: How many tasks should be started when this event is triggered. Default: 1
        """
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "task_definition": task_definition,
        }
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if task_count is not None:
            self._values["task_count"] = task_count

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """Cluster where service will be deployed."""
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return result

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition of the task that should be started."""
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List[ContainerOverride]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion]:
        """The platform version on which to run your task.

        Unless you have specific compatibility requirements, you don't need to specify this.

        :default: - ECS will set the Fargate platform version to 'LATEST'

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html
        """
        result = self._values.get("platform_version")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Existing IAM role to run the ECS task.

        :default: A new IAM role is created
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """(deprecated) Existing security group to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: A new security group is created

        :deprecated: use securityGroups instead

        :stability: deprecated
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """Existing security groups to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: A new security group is created
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets
        """
        result = self._values.get("subnet_selection")
        return result

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        """How many tasks should be started when this event is triggered.

        :default: 1
        """
        result = self._values.get("task_count")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class KinesisFirehoseStream(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.KinesisFirehoseStream",
):
    """Customize the Firehose Stream Event Target."""

    def __init__(
        self,
        stream: aws_cdk.aws_kinesisfirehose.CfnDeliveryStream,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """
        :param stream: -
        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire Event Bridge event
        """
        props = KinesisFirehoseStreamProps(message=message)

        jsii.create(KinesisFirehoseStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this Firehose Stream as a result from a Event Bridge event.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.KinesisFirehoseStreamProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message"},
)
class KinesisFirehoseStreamProps:
    def __init__(
        self,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """Customize the Firehose Stream Event Target.

        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire Event Bridge event
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        :default: - the entire Event Bridge event
        """
        result = self._values.get("message")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class KinesisStream(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.KinesisStream",
):
    """Use a Kinesis Stream as a target for AWS CloudWatch event rules.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # put to a Kinesis stream every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.KinesisStream(stream))
    """

    def __init__(
        self,
        stream: aws_cdk.aws_kinesis.IStream,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        partition_key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param stream: -
        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: Partition Key Path for records sent to this stream. Default: - eventId as the partition key
        """
        props = KinesisStreamProps(
            message=message, partition_key_path=partition_key_path
        )

        jsii.create(KinesisStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this Kinesis Stream as a result from a CloudWatch event.

        :param _rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [_rule, _id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.KinesisStreamProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "partition_key_path": "partitionKeyPath"},
)
class KinesisStreamProps:
    def __init__(
        self,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        partition_key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """Customize the Kinesis Stream Event Target.

        :param message: The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: Partition Key Path for records sent to this stream. Default: - eventId as the partition key
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if partition_key_path is not None:
            self._values["partition_key_path"] = partition_key_path

    @builtins.property
    def message(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        :default: - the entire CloudWatch event
        """
        result = self._values.get("message")
        return result

    @builtins.property
    def partition_key_path(self) -> typing.Optional[builtins.str]:
        """Partition Key Path for records sent to this stream.

        :default: - eventId as the partition key
        """
        result = self._values.get("partition_key_path")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class LambdaFunction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.LambdaFunction",
):
    """Use an AWS Lambda function as an event rule target."""

    def __init__(
        self,
        handler: aws_cdk.aws_lambda.IFunction,
        *,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """
        :param handler: -
        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        """
        props = LambdaFunctionProps(event=event)

        jsii.create(LambdaFunction, self, [handler, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this Lambda as a result from an EventBridge event.

        :param rule: -
        :param _id: -
        """
        return jsii.invoke(self, "bind", [rule, _id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.LambdaFunctionProps",
    jsii_struct_bases=[],
    name_mapping={"event": "event"},
)
class LambdaFunctionProps:
    def __init__(
        self,
        *,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """Customize the Lambda Event Target.

        :param event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if event is not None:
            self._values["event"] = event

    @builtins.property
    def event(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        :default: the entire EventBridge event
        """
        result = self._values.get("event")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.LogGroupProps",
    jsii_struct_bases=[],
    name_mapping={"event": "event"},
)
class LogGroupProps:
    def __init__(
        self,
        *,
        event: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """Customize the CloudWatch LogGroup Event Target.

        :param event: The event to send to the CloudWatch LogGroup. This will be the event logged into the CloudWatch LogGroup Default: - the entire EventBridge event
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if event is not None:
            self._values["event"] = event

    @builtins.property
    def event(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The event to send to the CloudWatch LogGroup.

        This will be the event logged into the CloudWatch LogGroup

        :default: - the entire EventBridge event
        """
        result = self._values.get("event")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SfnStateMachine(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.SfnStateMachine",
):
    """Use a StepFunctions state machine as a target for Amazon EventBridge rules."""

    def __init__(
        self,
        machine: aws_cdk.aws_stepfunctions.IStateMachine,
        *,
        input: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """
        :param machine: -
        :param input: The input to the state machine execution. Default: the entire EventBridge event
        :param role: The IAM role to be assumed to execute the State Machine. Default: - a new role will be created
        """
        props = SfnStateMachineProps(input=input, role=role)

        jsii.create(SfnStateMachine, self, [machine, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a properties that are used in an Rule to trigger this State Machine.

        :param _rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="machine")
    def machine(self) -> aws_cdk.aws_stepfunctions.IStateMachine:
        return jsii.get(self, "machine")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.SfnStateMachineProps",
    jsii_struct_bases=[],
    name_mapping={"input": "input", "role": "role"},
)
class SfnStateMachineProps:
    def __init__(
        self,
        *,
        input: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """Customize the Step Functions State Machine target.

        :param input: The input to the state machine execution. Default: the entire EventBridge event
        :param role: The IAM role to be assumed to execute the State Machine. Default: - a new role will be created
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if input is not None:
            self._values["input"] = input
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def input(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The input to the state machine execution.

        :default: the entire EventBridge event
        """
        result = self._values.get("input")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role to be assumed to execute the State Machine.

        :default: - a new role will be created
        """
        result = self._values.get("role")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SnsTopic(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.SnsTopic",
):
    """Use an SNS topic as a target for Amazon EventBridge rules.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SNS topic every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SnsTopic(topic))
    """

    def __init__(
        self,
        topic: aws_cdk.aws_sns.ITopic,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """
        :param topic: -
        :param message: The message to send to the topic. Default: the entire EventBridge event
        """
        props = SnsTopicProps(message=message)

        jsii.create(SnsTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this SNS topic as a result from an EventBridge event.

        :param _rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        """
        return jsii.invoke(self, "bind", [_rule, _id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        return jsii.get(self, "topic")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.SnsTopicProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message"},
)
class SnsTopicProps:
    def __init__(
        self,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
    ) -> None:
        """Customize the SNS Topic Event Target.

        :param message: The message to send to the topic. Default: the entire EventBridge event
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The message to send to the topic.

        :default: the entire EventBridge event
        """
        result = self._values.get("message")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SqsQueue(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events-targets.SqsQueue",
):
    """Use an SQS Queue as a target for Amazon EventBridge rules.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SQS queue every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SqsQueue(queue))
    """

    def __init__(
        self,
        queue: aws_cdk.aws_sqs.IQueue,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param queue: -
        :param message: The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)
        """
        props = SqsQueueProps(message=message, message_group_id=message_group_id)

        jsii.create(SqsQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: aws_cdk.aws_events.IRule,
        _id: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this SQS queue as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sqs-permissions
        """
        return jsii.invoke(self, "bind", [rule, _id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="queue")
    def queue(self) -> aws_cdk.aws_sqs.IQueue:
        return jsii.get(self, "queue")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.SqsQueueProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "message_group_id": "messageGroupId"},
)
class SqsQueueProps:
    def __init__(
        self,
        *,
        message: typing.Optional[aws_cdk.aws_events.RuleTargetInput] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Customize the SQS Queue Event Target.

        :param message: The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def message(self) -> typing.Optional[aws_cdk.aws_events.RuleTargetInput]:
        """The message to send to the queue.

        Must be a valid JSON text passed to the target queue.

        :default: the entire EventBridge event
        """
        result = self._values.get("message")
        return result

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        """Message Group ID for messages sent to this queue.

        Required for FIFO queues, leave empty for regular queues.

        :default: - no message group ID (regular queue)
        """
        result = self._values.get("message_group_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events-targets.TaskEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class TaskEnvironmentVariable:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        """An environment variable to be set in the container run as a task.

        :param name: Name for the environment variable. Exactly one of ``name`` and ``namePath`` must be specified.
        :param value: Value of the environment variable. Exactly one of ``value`` and ``valuePath`` must be specified.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        """Name for the environment variable.

        Exactly one of ``name`` and ``namePath`` must be specified.
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def value(self) -> builtins.str:
        """Value of the environment variable.

        Exactly one of ``value`` and ``valuePath`` must be specified.
        """
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsApi",
    "AwsApiInput",
    "AwsApiProps",
    "BatchJob",
    "BatchJobProps",
    "CloudWatchLogGroup",
    "CodeBuildProject",
    "CodeBuildProjectProps",
    "CodePipeline",
    "CodePipelineTargetOptions",
    "ContainerOverride",
    "EcsTask",
    "EcsTaskProps",
    "KinesisFirehoseStream",
    "KinesisFirehoseStreamProps",
    "KinesisStream",
    "KinesisStreamProps",
    "LambdaFunction",
    "LambdaFunctionProps",
    "LogGroupProps",
    "SfnStateMachine",
    "SfnStateMachineProps",
    "SnsTopic",
    "SnsTopicProps",
    "SqsQueue",
    "SqsQueueProps",
    "TaskEnvironmentVariable",
]

publication.publish()
