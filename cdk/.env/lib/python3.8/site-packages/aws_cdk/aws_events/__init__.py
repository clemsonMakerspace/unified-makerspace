"""
## Amazon EventBridge Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Amazon EventBridge delivers a near real-time stream of system events that
describe changes in AWS resources. For example, an AWS CodePipeline emits the
[State
Change](https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html#codepipeline-event-type)
event when the pipeline changes it's state.

* **Events**: An event indicates a change in your AWS environment. AWS resources
  can generate events when their state changes. For example, Amazon EC2
  generates an event when the state of an EC2 instance changes from pending to
  running, and Amazon EC2 Auto Scaling generates events when it launches or
  terminates instances. AWS CloudTrail publishes events when you make API calls.
  You can generate custom application-level events and publish them to
  EventBridge. You can also set up scheduled events that are generated on
  a periodic basis. For a list of services that generate events, and sample
  events from each service, see [EventBridge Event Examples From Each
  Supported
  Service](https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html).
* **Targets**: A target processes events. Targets can include Amazon EC2
  instances, AWS Lambda functions, Kinesis streams, Amazon ECS tasks, Step
  Functions state machines, Amazon SNS topics, Amazon SQS queues, Amazon CloudWatch LogGroups, and built-in
  targets. A target receives events in JSON format.
* **Rules**: A rule matches incoming events and routes them to targets for
  processing. A single rule can route to multiple targets, all of which are
  processed in parallel. Rules are not processed in a particular order. This
  enables different parts of an organization to look for and process the events
  that are of interest to them. A rule can customize the JSON sent to the
  target, by passing only certain parts or by overwriting it with a constant.
* **EventBuses**: An event bus can receive events from your own custom applications
  or it can receive events from applications and services created by AWS SaaS partners.
  See [Creating an Event Bus](https://docs.aws.amazon.com/eventbridge/latest/userguide/create-event-bus.html).

## Rule

The `Rule` construct defines an EventBridge rule which monitors an
event based on an [event
pattern](https://docs.aws.amazon.com/eventbridge/latest/userguide/filtering-examples-structure.html)
and invoke **event targets** when the pattern is matched against a triggered
event. Event targets are objects that implement the `IRuleTarget` interface.

Normally, you will use one of the `source.onXxx(name[, target[, options]]) -> Rule` methods on the event source to define an event rule associated with
the specific activity. You can targets either via props, or add targets using
`rule.addTarget`.

For example, to define an rule that triggers a CodeBuild project build when a
commit is pushed to the "master" branch of a CodeCommit repository:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
on_commit_rule = repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project),
    branches=["master"]
)
```

You can add additional targets, with optional [input
transformer](https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_InputTransformer.html)
using `eventRule.addTarget(target[, input])`. For example, we can add a SNS
topic target which formats a human-readable message for the commit.

For example, this adds an SNS topic as a target:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
on_commit_rule.add_target(targets.SnsTopic(topic,
    message=events.RuleTargetInput.from_text(f"A commit was pushed to the repository {codecommit.ReferenceEvent.repositoryName} on branch {codecommit.ReferenceEvent.referenceName}")
))
```

## Scheduling

You can configure a Rule to run on a schedule (cron or rate).

The following example runs a task every day at 4am:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import EcsTask

ecs_task_target = EcsTask(cluster=cluster, task_definition=task_definition, role=role)

Rule(self, "ScheduleRule",
    schedule=Schedule.cron(minute="0", hour="4"),
    targets=[ecs_task_target]
)
```

If you want to specify Fargate platform version, set `platformVersion` in EcsTask's props like the following example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
platform_version = ecs.FargatePlatformVersion.VERSION1_4
ecs_task_target = EcsTask(cluster=cluster, task_definition=task_definition, role=role, platform_version=platform_version)
```

## Event Targets

The `@aws-cdk/aws-events-targets` module includes classes that implement the `IRuleTarget`
interface for various AWS services.

The following targets are supported:

* `targets.CodeBuildProject`: Start an AWS CodeBuild build
* `targets.CodePipeline`: Start an AWS CodePipeline pipeline execution
* `targets.EcsTask`: Start a task on an Amazon ECS cluster
* `targets.LambdaFunction`: Invoke an AWS Lambda function
* `targets.SnsTopic`: Publish into an SNS topic
* `targets.SqsQueue`: Send a message to an Amazon SQS Queue
* `targets.SfnStateMachine`: Trigger an AWS Step Functions state machine
* `targets.BatchJob`: Queue an AWS Batch Job
* `targets.AwsApi`: Make an AWS API call

### Cross-account targets

It's possible to have the source of the event and a target in separate AWS accounts:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import App, Stack
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codecommit as codecommit
import aws_cdk.aws_events_targets as targets

app = App()

stack1 = Stack(app, "Stack1", env=Environment(account=account1, region="us-east-1"))
repo = codecommit.Repository(stack1, "Repository")

stack2 = Stack(app, "Stack2", env=Environment(account=account2, region="us-east-1"))
project = codebuild.Project(stack2, "Project")

repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project)
)
```

In this situation, the CDK will wire the 2 accounts together:

* It will generate a rule in the source stack with the event bus of the target account as the target
* It will generate a rule in the target stack, with the provided target
* It will generate a separate stack that gives the source account permissions to publish events
  to the event bus of the target account in the given region,
  and make sure its deployed before the source stack

**Note**: while events can span multiple accounts, they *cannot* span different regions
(that is an EventBridge, not CDK, limitation).

For more information, see the
[AWS documentation on cross-account events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html).
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

import aws_cdk.aws_iam
import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.core.IInspectable)
class CfnArchive(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events.CfnArchive",
):
    """A CloudFormation ``AWS::Events::Archive``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html
    :cloudformationResource: AWS::Events::Archive
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        source_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Create a new ``AWS::Events::Archive``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param source_arn: ``AWS::Events::Archive.SourceArn``.
        :param description: ``AWS::Events::Archive.Description``.
        :param event_pattern: ``AWS::Events::Archive.EventPattern``.
        :param retention_days: ``AWS::Events::Archive.RetentionDays``.
        """
        props = CfnArchiveProps(
            source_arn=source_arn,
            description=description,
            event_pattern=event_pattern,
            retention_days=retention_days,
        )

        jsii.create(CfnArchive, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrArchiveName")
    def attr_archive_name(self) -> builtins.str:
        """
        :cloudformationAttribute: ArchiveName
        """
        return jsii.get(self, "attrArchiveName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventPattern")
    def event_pattern(self) -> typing.Any:
        """``AWS::Events::Archive.EventPattern``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-eventpattern
        """
        return jsii.get(self, "eventPattern")

    @event_pattern.setter # type: ignore
    def event_pattern(self, value: typing.Any) -> None:
        jsii.set(self, "eventPattern", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        """``AWS::Events::Archive.SourceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-sourcearn
        """
        return jsii.get(self, "sourceArn")

    @source_arn.setter # type: ignore
    def source_arn(self, value: builtins.str) -> None:
        jsii.set(self, "sourceArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Archive.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::Events::Archive.RetentionDays``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-retentiondays
        """
        return jsii.get(self, "retentionDays")

    @retention_days.setter # type: ignore
    def retention_days(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "retentionDays", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.CfnArchiveProps",
    jsii_struct_bases=[],
    name_mapping={
        "source_arn": "sourceArn",
        "description": "description",
        "event_pattern": "eventPattern",
        "retention_days": "retentionDays",
    },
)
class CfnArchiveProps:
    def __init__(
        self,
        *,
        source_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for defining a ``AWS::Events::Archive``.

        :param source_arn: ``AWS::Events::Archive.SourceArn``.
        :param description: ``AWS::Events::Archive.Description``.
        :param event_pattern: ``AWS::Events::Archive.EventPattern``.
        :param retention_days: ``AWS::Events::Archive.RetentionDays``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "source_arn": source_arn,
        }
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if retention_days is not None:
            self._values["retention_days"] = retention_days

    @builtins.property
    def source_arn(self) -> builtins.str:
        """``AWS::Events::Archive.SourceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-sourcearn
        """
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Archive.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Any:
        """``AWS::Events::Archive.EventPattern``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-eventpattern
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::Events::Archive.RetentionDays``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-archive.html#cfn-events-archive-retentiondays
        """
        result = self._values.get("retention_days")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnArchiveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEventBus(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events.CfnEventBus",
):
    """A CloudFormation ``AWS::Events::EventBus``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html
    :cloudformationResource: AWS::Events::EventBus
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Events::EventBus``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Events::EventBus.Name``.
        :param event_source_name: ``AWS::Events::EventBus.EventSourceName``.
        """
        props = CfnEventBusProps(name=name, event_source_name=event_source_name)

        jsii.create(CfnEventBus, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrPolicy")
    def attr_policy(self) -> builtins.str:
        """
        :cloudformationAttribute: Policy
        """
        return jsii.get(self, "attrPolicy")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::Events::EventBus.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::EventBus.EventSourceName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        return jsii.get(self, "eventSourceName")

    @event_source_name.setter # type: ignore
    def event_source_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "eventSourceName", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEventBusPolicy(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy",
):
    """A CloudFormation ``AWS::Events::EventBusPolicy``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
    :cloudformationResource: AWS::Events::EventBusPolicy
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        action: builtins.str,
        principal: builtins.str,
        statement_id: builtins.str,
        condition: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEventBusPolicy.ConditionProperty"]] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Events::EventBusPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: ``AWS::Events::EventBusPolicy.Action``.
        :param principal: ``AWS::Events::EventBusPolicy.Principal``.
        :param statement_id: ``AWS::Events::EventBusPolicy.StatementId``.
        :param condition: ``AWS::Events::EventBusPolicy.Condition``.
        :param event_bus_name: ``AWS::Events::EventBusPolicy.EventBusName``.
        """
        props = CfnEventBusPolicyProps(
            action=action,
            principal=principal,
            statement_id=statement_id,
            condition=condition,
            event_bus_name=event_bus_name,
        )

        jsii.create(CfnEventBusPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        """``AWS::Events::EventBusPolicy.Action``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-action
        """
        return jsii.get(self, "action")

    @action.setter # type: ignore
    def action(self, value: builtins.str) -> None:
        jsii.set(self, "action", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        """``AWS::Events::EventBusPolicy.Principal``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-principal
        """
        return jsii.get(self, "principal")

    @principal.setter # type: ignore
    def principal(self, value: builtins.str) -> None:
        jsii.set(self, "principal", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="statementId")
    def statement_id(self) -> builtins.str:
        """``AWS::Events::EventBusPolicy.StatementId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statementid
        """
        return jsii.get(self, "statementId")

    @statement_id.setter # type: ignore
    def statement_id(self, value: builtins.str) -> None:
        jsii.set(self, "statementId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEventBusPolicy.ConditionProperty"]]:
        """``AWS::Events::EventBusPolicy.Condition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-condition
        """
        return jsii.get(self, "condition")

    @condition.setter # type: ignore
    def condition(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEventBusPolicy.ConditionProperty"]],
    ) -> None:
        jsii.set(self, "condition", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::EventBusPolicy.EventBusName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-eventbusname
        """
        return jsii.get(self, "eventBusName")

    @event_bus_name.setter # type: ignore
    def event_bus_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "eventBusName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param key: ``CfnEventBusPolicy.ConditionProperty.Key``.
            :param type: ``CfnEventBusPolicy.ConditionProperty.Type``.
            :param value: ``CfnEventBusPolicy.ConditionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnEventBusPolicy.ConditionProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-key
            """
            result = self._values.get("key")
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnEventBusPolicy.ConditionProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-type
            """
            result = self._values.get("type")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnEventBusPolicy.ConditionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.CfnEventBusPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "principal": "principal",
        "statement_id": "statementId",
        "condition": "condition",
        "event_bus_name": "eventBusName",
    },
)
class CfnEventBusPolicyProps:
    def __init__(
        self,
        *,
        action: builtins.str,
        principal: builtins.str,
        statement_id: builtins.str,
        condition: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEventBusPolicy.ConditionProperty]] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Events::EventBusPolicy``.

        :param action: ``AWS::Events::EventBusPolicy.Action``.
        :param principal: ``AWS::Events::EventBusPolicy.Principal``.
        :param statement_id: ``AWS::Events::EventBusPolicy.StatementId``.
        :param condition: ``AWS::Events::EventBusPolicy.Condition``.
        :param event_bus_name: ``AWS::Events::EventBusPolicy.EventBusName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "principal": principal,
            "statement_id": statement_id,
        }
        if condition is not None:
            self._values["condition"] = condition
        if event_bus_name is not None:
            self._values["event_bus_name"] = event_bus_name

    @builtins.property
    def action(self) -> builtins.str:
        """``AWS::Events::EventBusPolicy.Action``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-action
        """
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return result

    @builtins.property
    def principal(self) -> builtins.str:
        """``AWS::Events::EventBusPolicy.Principal``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-principal
        """
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return result

    @builtins.property
    def statement_id(self) -> builtins.str:
        """``AWS::Events::EventBusPolicy.StatementId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statementid
        """
        result = self._values.get("statement_id")
        assert result is not None, "Required property 'statement_id' is missing"
        return result

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEventBusPolicy.ConditionProperty]]:
        """``AWS::Events::EventBusPolicy.Condition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-condition
        """
        result = self._values.get("condition")
        return result

    @builtins.property
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::EventBusPolicy.EventBusName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-eventbusname
        """
        result = self._values.get("event_bus_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventBusPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.CfnEventBusProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "event_source_name": "eventSourceName"},
)
class CfnEventBusProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Events::EventBus``.

        :param name: ``AWS::Events::EventBus.Name``.
        :param event_source_name: ``AWS::Events::EventBus.EventSourceName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if event_source_name is not None:
            self._values["event_source_name"] = event_source_name

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::Events::EventBus.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def event_source_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::EventBus.EventSourceName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        result = self._values.get("event_source_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventBusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRule(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events.CfnRule",
):
    """A CloudFormation ``AWS::Events::Rule``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
    :cloudformationResource: AWS::Events::Rule
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.TargetProperty"]]]] = None,
    ) -> None:
        """Create a new ``AWS::Events::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Events::Rule.Description``.
        :param event_bus_name: ``AWS::Events::Rule.EventBusName``.
        :param event_pattern: ``AWS::Events::Rule.EventPattern``.
        :param name: ``AWS::Events::Rule.Name``.
        :param role_arn: ``AWS::Events::Rule.RoleArn``.
        :param schedule_expression: ``AWS::Events::Rule.ScheduleExpression``.
        :param state: ``AWS::Events::Rule.State``.
        :param targets: ``AWS::Events::Rule.Targets``.
        """
        props = CfnRuleProps(
            description=description,
            event_bus_name=event_bus_name,
            event_pattern=event_pattern,
            name=name,
            role_arn=role_arn,
            schedule_expression=schedule_expression,
            state=state,
            targets=targets,
        )

        jsii.create(CfnRule, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventPattern")
    def event_pattern(self) -> typing.Any:
        """``AWS::Events::Rule.EventPattern``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventpattern
        """
        return jsii.get(self, "eventPattern")

    @event_pattern.setter # type: ignore
    def event_pattern(self, value: typing.Any) -> None:
        jsii.set(self, "eventPattern", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.EventBusName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventbusname
        """
        return jsii.get(self, "eventBusName")

    @event_bus_name.setter # type: ignore
    def event_bus_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "eventBusName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.ScheduleExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-scheduleexpression
        """
        return jsii.get(self, "scheduleExpression")

    @schedule_expression.setter # type: ignore
    def schedule_expression(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scheduleExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-state
        """
        return jsii.get(self, "state")

    @state.setter # type: ignore
    def state(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "state", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.TargetProperty"]]]]:
        """``AWS::Events::Rule.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-targets
        """
        return jsii.get(self, "targets")

    @targets.setter # type: ignore
    def targets(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.TargetProperty"]]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.AwsVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subnets": "subnets",
            "assign_public_ip": "assignPublicIp",
            "security_groups": "securityGroups",
        },
    )
    class AwsVpcConfigurationProperty:
        def __init__(
            self,
            *,
            subnets: typing.List[builtins.str],
            assign_public_ip: typing.Optional[builtins.str] = None,
            security_groups: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param subnets: ``CfnRule.AwsVpcConfigurationProperty.Subnets``.
            :param assign_public_ip: ``CfnRule.AwsVpcConfigurationProperty.AssignPublicIp``.
            :param security_groups: ``CfnRule.AwsVpcConfigurationProperty.SecurityGroups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "subnets": subnets,
            }
            if assign_public_ip is not None:
                self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None:
                self._values["security_groups"] = security_groups

        @builtins.property
        def subnets(self) -> typing.List[builtins.str]:
            """``CfnRule.AwsVpcConfigurationProperty.Subnets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-subnets
            """
            result = self._values.get("subnets")
            assert result is not None, "Required property 'subnets' is missing"
            return result

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[builtins.str]:
            """``CfnRule.AwsVpcConfigurationProperty.AssignPublicIp``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-assignpublicip
            """
            result = self._values.get("assign_public_ip")
            return result

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnRule.AwsVpcConfigurationProperty.SecurityGroups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-awsvpcconfiguration.html#cfn-events-rule-awsvpcconfiguration-securitygroups
            """
            result = self._values.get("security_groups")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.BatchArrayPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"size": "size"},
    )
    class BatchArrayPropertiesProperty:
        def __init__(self, *, size: typing.Optional[jsii.Number] = None) -> None:
            """
            :param size: ``CfnRule.BatchArrayPropertiesProperty.Size``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batcharrayproperties.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if size is not None:
                self._values["size"] = size

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.BatchArrayPropertiesProperty.Size``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batcharrayproperties.html#cfn-events-rule-batcharrayproperties-size
            """
            result = self._values.get("size")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchArrayPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.BatchParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_definition": "jobDefinition",
            "job_name": "jobName",
            "array_properties": "arrayProperties",
            "retry_strategy": "retryStrategy",
        },
    )
    class BatchParametersProperty:
        def __init__(
            self,
            *,
            job_definition: builtins.str,
            job_name: builtins.str,
            array_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.BatchArrayPropertiesProperty"]] = None,
            retry_strategy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.BatchRetryStrategyProperty"]] = None,
        ) -> None:
            """
            :param job_definition: ``CfnRule.BatchParametersProperty.JobDefinition``.
            :param job_name: ``CfnRule.BatchParametersProperty.JobName``.
            :param array_properties: ``CfnRule.BatchParametersProperty.ArrayProperties``.
            :param retry_strategy: ``CfnRule.BatchParametersProperty.RetryStrategy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "job_definition": job_definition,
                "job_name": job_name,
            }
            if array_properties is not None:
                self._values["array_properties"] = array_properties
            if retry_strategy is not None:
                self._values["retry_strategy"] = retry_strategy

        @builtins.property
        def job_definition(self) -> builtins.str:
            """``CfnRule.BatchParametersProperty.JobDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-jobdefinition
            """
            result = self._values.get("job_definition")
            assert result is not None, "Required property 'job_definition' is missing"
            return result

        @builtins.property
        def job_name(self) -> builtins.str:
            """``CfnRule.BatchParametersProperty.JobName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-jobname
            """
            result = self._values.get("job_name")
            assert result is not None, "Required property 'job_name' is missing"
            return result

        @builtins.property
        def array_properties(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.BatchArrayPropertiesProperty"]]:
            """``CfnRule.BatchParametersProperty.ArrayProperties``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-arrayproperties
            """
            result = self._values.get("array_properties")
            return result

        @builtins.property
        def retry_strategy(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.BatchRetryStrategyProperty"]]:
            """``CfnRule.BatchParametersProperty.RetryStrategy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchparameters.html#cfn-events-rule-batchparameters-retrystrategy
            """
            result = self._values.get("retry_strategy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.BatchRetryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"attempts": "attempts"},
    )
    class BatchRetryStrategyProperty:
        def __init__(self, *, attempts: typing.Optional[jsii.Number] = None) -> None:
            """
            :param attempts: ``CfnRule.BatchRetryStrategyProperty.Attempts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchretrystrategy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attempts is not None:
                self._values["attempts"] = attempts

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.BatchRetryStrategyProperty.Attempts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-batchretrystrategy.html#cfn-events-rule-batchretrystrategy-attempts
            """
            result = self._values.get("attempts")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchRetryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.DeadLetterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class DeadLetterConfigProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            """
            :param arn: ``CfnRule.DeadLetterConfigProperty.Arn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-deadletterconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            """``CfnRule.DeadLetterConfigProperty.Arn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-deadletterconfig.html#cfn-events-rule-deadletterconfig-arn
            """
            result = self._values.get("arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.EcsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "task_definition_arn": "taskDefinitionArn",
            "group": "group",
            "launch_type": "launchType",
            "network_configuration": "networkConfiguration",
            "platform_version": "platformVersion",
            "task_count": "taskCount",
        },
    )
    class EcsParametersProperty:
        def __init__(
            self,
            *,
            task_definition_arn: builtins.str,
            group: typing.Optional[builtins.str] = None,
            launch_type: typing.Optional[builtins.str] = None,
            network_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.NetworkConfigurationProperty"]] = None,
            platform_version: typing.Optional[builtins.str] = None,
            task_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param task_definition_arn: ``CfnRule.EcsParametersProperty.TaskDefinitionArn``.
            :param group: ``CfnRule.EcsParametersProperty.Group``.
            :param launch_type: ``CfnRule.EcsParametersProperty.LaunchType``.
            :param network_configuration: ``CfnRule.EcsParametersProperty.NetworkConfiguration``.
            :param platform_version: ``CfnRule.EcsParametersProperty.PlatformVersion``.
            :param task_count: ``CfnRule.EcsParametersProperty.TaskCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "task_definition_arn": task_definition_arn,
            }
            if group is not None:
                self._values["group"] = group
            if launch_type is not None:
                self._values["launch_type"] = launch_type
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if platform_version is not None:
                self._values["platform_version"] = platform_version
            if task_count is not None:
                self._values["task_count"] = task_count

        @builtins.property
        def task_definition_arn(self) -> builtins.str:
            """``CfnRule.EcsParametersProperty.TaskDefinitionArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskdefinitionarn
            """
            result = self._values.get("task_definition_arn")
            assert result is not None, "Required property 'task_definition_arn' is missing"
            return result

        @builtins.property
        def group(self) -> typing.Optional[builtins.str]:
            """``CfnRule.EcsParametersProperty.Group``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-group
            """
            result = self._values.get("group")
            return result

        @builtins.property
        def launch_type(self) -> typing.Optional[builtins.str]:
            """``CfnRule.EcsParametersProperty.LaunchType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-launchtype
            """
            result = self._values.get("launch_type")
            return result

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.NetworkConfigurationProperty"]]:
            """``CfnRule.EcsParametersProperty.NetworkConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-networkconfiguration
            """
            result = self._values.get("network_configuration")
            return result

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            """``CfnRule.EcsParametersProperty.PlatformVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-platformversion
            """
            result = self._values.get("platform_version")
            return result

        @builtins.property
        def task_count(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.EcsParametersProperty.TaskCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskcount
            """
            result = self._values.get("task_count")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.HttpParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_parameters": "headerParameters",
            "path_parameter_values": "pathParameterValues",
            "query_string_parameters": "queryStringParameters",
        },
    )
    class HttpParametersProperty:
        def __init__(
            self,
            *,
            header_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            path_parameter_values: typing.Optional[typing.List[builtins.str]] = None,
            query_string_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            """
            :param header_parameters: ``CfnRule.HttpParametersProperty.HeaderParameters``.
            :param path_parameter_values: ``CfnRule.HttpParametersProperty.PathParameterValues``.
            :param query_string_parameters: ``CfnRule.HttpParametersProperty.QueryStringParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if header_parameters is not None:
                self._values["header_parameters"] = header_parameters
            if path_parameter_values is not None:
                self._values["path_parameter_values"] = path_parameter_values
            if query_string_parameters is not None:
                self._values["query_string_parameters"] = query_string_parameters

        @builtins.property
        def header_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnRule.HttpParametersProperty.HeaderParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html#cfn-events-rule-httpparameters-headerparameters
            """
            result = self._values.get("header_parameters")
            return result

        @builtins.property
        def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnRule.HttpParametersProperty.PathParameterValues``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html#cfn-events-rule-httpparameters-pathparametervalues
            """
            result = self._values.get("path_parameter_values")
            return result

        @builtins.property
        def query_string_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnRule.HttpParametersProperty.QueryStringParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-httpparameters.html#cfn-events-rule-httpparameters-querystringparameters
            """
            result = self._values.get("query_string_parameters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.InputTransformerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_template": "inputTemplate",
            "input_paths_map": "inputPathsMap",
        },
    )
    class InputTransformerProperty:
        def __init__(
            self,
            *,
            input_template: builtins.str,
            input_paths_map: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            """
            :param input_template: ``CfnRule.InputTransformerProperty.InputTemplate``.
            :param input_paths_map: ``CfnRule.InputTransformerProperty.InputPathsMap``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "input_template": input_template,
            }
            if input_paths_map is not None:
                self._values["input_paths_map"] = input_paths_map

        @builtins.property
        def input_template(self) -> builtins.str:
            """``CfnRule.InputTransformerProperty.InputTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputtemplate
            """
            result = self._values.get("input_template")
            assert result is not None, "Required property 'input_template' is missing"
            return result

        @builtins.property
        def input_paths_map(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnRule.InputTransformerProperty.InputPathsMap``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputpathsmap
            """
            result = self._values.get("input_paths_map")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputTransformerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.KinesisParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"partition_key_path": "partitionKeyPath"},
    )
    class KinesisParametersProperty:
        def __init__(self, *, partition_key_path: builtins.str) -> None:
            """
            :param partition_key_path: ``CfnRule.KinesisParametersProperty.PartitionKeyPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "partition_key_path": partition_key_path,
            }

        @builtins.property
        def partition_key_path(self) -> builtins.str:
            """``CfnRule.KinesisParametersProperty.PartitionKeyPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html#cfn-events-rule-kinesisparameters-partitionkeypath
            """
            result = self._values.get("partition_key_path")
            assert result is not None, "Required property 'partition_key_path' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_vpc_configuration": "awsVpcConfiguration"},
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            aws_vpc_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.AwsVpcConfigurationProperty"]] = None,
        ) -> None:
            """
            :param aws_vpc_configuration: ``CfnRule.NetworkConfigurationProperty.AwsVpcConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-networkconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if aws_vpc_configuration is not None:
                self._values["aws_vpc_configuration"] = aws_vpc_configuration

        @builtins.property
        def aws_vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.AwsVpcConfigurationProperty"]]:
            """``CfnRule.NetworkConfigurationProperty.AwsVpcConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-networkconfiguration.html#cfn-events-rule-networkconfiguration-awsvpcconfiguration
            """
            result = self._values.get("aws_vpc_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.RedshiftDataParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database": "database",
            "sql": "sql",
            "db_user": "dbUser",
            "secret_manager_arn": "secretManagerArn",
            "statement_name": "statementName",
            "with_event": "withEvent",
        },
    )
    class RedshiftDataParametersProperty:
        def __init__(
            self,
            *,
            database: builtins.str,
            sql: builtins.str,
            db_user: typing.Optional[builtins.str] = None,
            secret_manager_arn: typing.Optional[builtins.str] = None,
            statement_name: typing.Optional[builtins.str] = None,
            with_event: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param database: ``CfnRule.RedshiftDataParametersProperty.Database``.
            :param sql: ``CfnRule.RedshiftDataParametersProperty.Sql``.
            :param db_user: ``CfnRule.RedshiftDataParametersProperty.DbUser``.
            :param secret_manager_arn: ``CfnRule.RedshiftDataParametersProperty.SecretManagerArn``.
            :param statement_name: ``CfnRule.RedshiftDataParametersProperty.StatementName``.
            :param with_event: ``CfnRule.RedshiftDataParametersProperty.WithEvent``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "database": database,
                "sql": sql,
            }
            if db_user is not None:
                self._values["db_user"] = db_user
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn
            if statement_name is not None:
                self._values["statement_name"] = statement_name
            if with_event is not None:
                self._values["with_event"] = with_event

        @builtins.property
        def database(self) -> builtins.str:
            """``CfnRule.RedshiftDataParametersProperty.Database``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-database
            """
            result = self._values.get("database")
            assert result is not None, "Required property 'database' is missing"
            return result

        @builtins.property
        def sql(self) -> builtins.str:
            """``CfnRule.RedshiftDataParametersProperty.Sql``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-sql
            """
            result = self._values.get("sql")
            assert result is not None, "Required property 'sql' is missing"
            return result

        @builtins.property
        def db_user(self) -> typing.Optional[builtins.str]:
            """``CfnRule.RedshiftDataParametersProperty.DbUser``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-dbuser
            """
            result = self._values.get("db_user")
            return result

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            """``CfnRule.RedshiftDataParametersProperty.SecretManagerArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-secretmanagerarn
            """
            result = self._values.get("secret_manager_arn")
            return result

        @builtins.property
        def statement_name(self) -> typing.Optional[builtins.str]:
            """``CfnRule.RedshiftDataParametersProperty.StatementName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-statementname
            """
            result = self._values.get("statement_name")
            return result

        @builtins.property
        def with_event(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnRule.RedshiftDataParametersProperty.WithEvent``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-redshiftdataparameters.html#cfn-events-rule-redshiftdataparameters-withevent
            """
            result = self._values.get("with_event")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftDataParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.RetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
        },
    )
    class RetryPolicyProperty:
        def __init__(
            self,
            *,
            maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param maximum_event_age_in_seconds: ``CfnRule.RetryPolicyProperty.MaximumEventAgeInSeconds``.
            :param maximum_retry_attempts: ``CfnRule.RetryPolicyProperty.MaximumRetryAttempts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-retrypolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if maximum_event_age_in_seconds is not None:
                self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts

        @builtins.property
        def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.RetryPolicyProperty.MaximumEventAgeInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-retrypolicy.html#cfn-events-rule-retrypolicy-maximumeventageinseconds
            """
            result = self._values.get("maximum_event_age_in_seconds")
            return result

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            """``CfnRule.RetryPolicyProperty.MaximumRetryAttempts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-retrypolicy.html#cfn-events-rule-retrypolicy-maximumretryattempts
            """
            result = self._values.get("maximum_retry_attempts")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"run_command_targets": "runCommandTargets"},
    )
    class RunCommandParametersProperty:
        def __init__(
            self,
            *,
            run_command_targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RunCommandTargetProperty"]]],
        ) -> None:
            """
            :param run_command_targets: ``CfnRule.RunCommandParametersProperty.RunCommandTargets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "run_command_targets": run_command_targets,
            }

        @builtins.property
        def run_command_targets(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RunCommandTargetProperty"]]]:
            """``CfnRule.RunCommandParametersProperty.RunCommandTargets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html#cfn-events-rule-runcommandparameters-runcommandtargets
            """
            result = self._values.get("run_command_targets")
            assert result is not None, "Required property 'run_command_targets' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunCommandParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class RunCommandTargetProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            values: typing.List[builtins.str],
        ) -> None:
            """
            :param key: ``CfnRule.RunCommandTargetProperty.Key``.
            :param values: ``CfnRule.RunCommandTargetProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "values": values,
            }

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnRule.RunCommandTargetProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def values(self) -> typing.List[builtins.str]:
            """``CfnRule.RunCommandTargetProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-values
            """
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunCommandTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.SqsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"message_group_id": "messageGroupId"},
    )
    class SqsParametersProperty:
        def __init__(self, *, message_group_id: builtins.str) -> None:
            """
            :param message_group_id: ``CfnRule.SqsParametersProperty.MessageGroupId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "message_group_id": message_group_id,
            }

        @builtins.property
        def message_group_id(self) -> builtins.str:
            """``CfnRule.SqsParametersProperty.MessageGroupId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html#cfn-events-rule-sqsparameters-messagegroupid
            """
            result = self._values.get("message_group_id")
            assert result is not None, "Required property 'message_group_id' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-events.CfnRule.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "id": "id",
            "batch_parameters": "batchParameters",
            "dead_letter_config": "deadLetterConfig",
            "ecs_parameters": "ecsParameters",
            "http_parameters": "httpParameters",
            "input": "input",
            "input_path": "inputPath",
            "input_transformer": "inputTransformer",
            "kinesis_parameters": "kinesisParameters",
            "redshift_data_parameters": "redshiftDataParameters",
            "retry_policy": "retryPolicy",
            "role_arn": "roleArn",
            "run_command_parameters": "runCommandParameters",
            "sqs_parameters": "sqsParameters",
        },
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            id: builtins.str,
            batch_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.BatchParametersProperty"]] = None,
            dead_letter_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.DeadLetterConfigProperty"]] = None,
            ecs_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.EcsParametersProperty"]] = None,
            http_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.HttpParametersProperty"]] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
            input_transformer: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.InputTransformerProperty"]] = None,
            kinesis_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.KinesisParametersProperty"]] = None,
            redshift_data_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RedshiftDataParametersProperty"]] = None,
            retry_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RetryPolicyProperty"]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            run_command_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RunCommandParametersProperty"]] = None,
            sqs_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.SqsParametersProperty"]] = None,
        ) -> None:
            """
            :param arn: ``CfnRule.TargetProperty.Arn``.
            :param id: ``CfnRule.TargetProperty.Id``.
            :param batch_parameters: ``CfnRule.TargetProperty.BatchParameters``.
            :param dead_letter_config: ``CfnRule.TargetProperty.DeadLetterConfig``.
            :param ecs_parameters: ``CfnRule.TargetProperty.EcsParameters``.
            :param http_parameters: ``CfnRule.TargetProperty.HttpParameters``.
            :param input: ``CfnRule.TargetProperty.Input``.
            :param input_path: ``CfnRule.TargetProperty.InputPath``.
            :param input_transformer: ``CfnRule.TargetProperty.InputTransformer``.
            :param kinesis_parameters: ``CfnRule.TargetProperty.KinesisParameters``.
            :param redshift_data_parameters: ``CfnRule.TargetProperty.RedshiftDataParameters``.
            :param retry_policy: ``CfnRule.TargetProperty.RetryPolicy``.
            :param role_arn: ``CfnRule.TargetProperty.RoleArn``.
            :param run_command_parameters: ``CfnRule.TargetProperty.RunCommandParameters``.
            :param sqs_parameters: ``CfnRule.TargetProperty.SqsParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "arn": arn,
                "id": id,
            }
            if batch_parameters is not None:
                self._values["batch_parameters"] = batch_parameters
            if dead_letter_config is not None:
                self._values["dead_letter_config"] = dead_letter_config
            if ecs_parameters is not None:
                self._values["ecs_parameters"] = ecs_parameters
            if http_parameters is not None:
                self._values["http_parameters"] = http_parameters
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path
            if input_transformer is not None:
                self._values["input_transformer"] = input_transformer
            if kinesis_parameters is not None:
                self._values["kinesis_parameters"] = kinesis_parameters
            if redshift_data_parameters is not None:
                self._values["redshift_data_parameters"] = redshift_data_parameters
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if run_command_parameters is not None:
                self._values["run_command_parameters"] = run_command_parameters
            if sqs_parameters is not None:
                self._values["sqs_parameters"] = sqs_parameters

        @builtins.property
        def arn(self) -> builtins.str:
            """``CfnRule.TargetProperty.Arn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-arn
            """
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return result

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnRule.TargetProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def batch_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.BatchParametersProperty"]]:
            """``CfnRule.TargetProperty.BatchParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-batchparameters
            """
            result = self._values.get("batch_parameters")
            return result

        @builtins.property
        def dead_letter_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.DeadLetterConfigProperty"]]:
            """``CfnRule.TargetProperty.DeadLetterConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-deadletterconfig
            """
            result = self._values.get("dead_letter_config")
            return result

        @builtins.property
        def ecs_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.EcsParametersProperty"]]:
            """``CfnRule.TargetProperty.EcsParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-ecsparameters
            """
            result = self._values.get("ecs_parameters")
            return result

        @builtins.property
        def http_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.HttpParametersProperty"]]:
            """``CfnRule.TargetProperty.HttpParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-httpparameters
            """
            result = self._values.get("http_parameters")
            return result

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            """``CfnRule.TargetProperty.Input``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-input
            """
            result = self._values.get("input")
            return result

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            """``CfnRule.TargetProperty.InputPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputpath
            """
            result = self._values.get("input_path")
            return result

        @builtins.property
        def input_transformer(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.InputTransformerProperty"]]:
            """``CfnRule.TargetProperty.InputTransformer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputtransformer
            """
            result = self._values.get("input_transformer")
            return result

        @builtins.property
        def kinesis_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.KinesisParametersProperty"]]:
            """``CfnRule.TargetProperty.KinesisParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-kinesisparameters
            """
            result = self._values.get("kinesis_parameters")
            return result

        @builtins.property
        def redshift_data_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RedshiftDataParametersProperty"]]:
            """``CfnRule.TargetProperty.RedshiftDataParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-redshiftdataparameters
            """
            result = self._values.get("redshift_data_parameters")
            return result

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RetryPolicyProperty"]]:
            """``CfnRule.TargetProperty.RetryPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-retrypolicy
            """
            result = self._values.get("retry_policy")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnRule.TargetProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def run_command_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.RunCommandParametersProperty"]]:
            """``CfnRule.TargetProperty.RunCommandParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-runcommandparameters
            """
            result = self._values.get("run_command_parameters")
            return result

        @builtins.property
        def sqs_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRule.SqsParametersProperty"]]:
            """``CfnRule.TargetProperty.SqsParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-sqsparameters
            """
            result = self._values.get("sqs_parameters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "event_bus_name": "eventBusName",
        "event_pattern": "eventPattern",
        "name": "name",
        "role_arn": "roleArn",
        "schedule_expression": "scheduleExpression",
        "state": "state",
        "targets": "targets",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_pattern: typing.Any = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnRule.TargetProperty]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Events::Rule``.

        :param description: ``AWS::Events::Rule.Description``.
        :param event_bus_name: ``AWS::Events::Rule.EventBusName``.
        :param event_pattern: ``AWS::Events::Rule.EventPattern``.
        :param name: ``AWS::Events::Rule.Name``.
        :param role_arn: ``AWS::Events::Rule.RoleArn``.
        :param schedule_expression: ``AWS::Events::Rule.ScheduleExpression``.
        :param state: ``AWS::Events::Rule.State``.
        :param targets: ``AWS::Events::Rule.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_bus_name is not None:
            self._values["event_bus_name"] = event_bus_name
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if state is not None:
            self._values["state"] = state
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.EventBusName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventbusname
        """
        result = self._values.get("event_bus_name")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Any:
        """``AWS::Events::Rule.EventPattern``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventpattern
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-rolearn
        """
        result = self._values.get("role_arn")
        return result

    @builtins.property
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.ScheduleExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-scheduleexpression
        """
        result = self._values.get("schedule_expression")
        return result

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::Events::Rule.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-state
        """
        result = self._values.get("state")
        return result

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnRule.TargetProperty]]]]:
        """``AWS::Events::Rule.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-targets
        """
        result = self._values.get("targets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.CronOptions",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
        "year": "year",
    },
)
class CronOptions:
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options to configure a cron expression.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if week_day is not None:
            self._values["week_day"] = week_day
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        """The day of the month to run this rule at.

        :default: - Every day of the month
        """
        result = self._values.get("day")
        return result

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        """The hour to run this rule at.

        :default: - Every hour
        """
        result = self._values.get("hour")
        return result

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        """The minute to run this rule at.

        :default: - Every minute
        """
        result = self._values.get("minute")
        return result

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        """The month to run this rule at.

        :default: - Every month
        """
        result = self._values.get("month")
        return result

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        """The day of the week to run this rule at.

        :default: - Any day of the week
        """
        result = self._values.get("week_day")
        return result

    @builtins.property
    def year(self) -> typing.Optional[builtins.str]:
        """The year to run this rule at.

        :default: - Every year
        """
        result = self._values.get("year")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.EventBusAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus_arn": "eventBusArn",
        "event_bus_name": "eventBusName",
        "event_bus_policy": "eventBusPolicy",
        "event_source_name": "eventSourceName",
    },
)
class EventBusAttributes:
    def __init__(
        self,
        *,
        event_bus_arn: builtins.str,
        event_bus_name: builtins.str,
        event_bus_policy: builtins.str,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Interface with properties necessary to import a reusable EventBus.

        :param event_bus_arn: The ARN of this event bus resource.
        :param event_bus_name: The physical ID of this event bus resource.
        :param event_bus_policy: The JSON policy of this event bus resource.
        :param event_source_name: The partner event source to associate with this event bus resource. Default: - no partner event source
        """
        self._values: typing.Dict[str, typing.Any] = {
            "event_bus_arn": event_bus_arn,
            "event_bus_name": event_bus_name,
            "event_bus_policy": event_bus_policy,
        }
        if event_source_name is not None:
            self._values["event_source_name"] = event_source_name

    @builtins.property
    def event_bus_arn(self) -> builtins.str:
        """The ARN of this event bus resource.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        """
        result = self._values.get("event_bus_arn")
        assert result is not None, "Required property 'event_bus_arn' is missing"
        return result

    @builtins.property
    def event_bus_name(self) -> builtins.str:
        """The physical ID of this event bus resource.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        result = self._values.get("event_bus_name")
        assert result is not None, "Required property 'event_bus_name' is missing"
        return result

    @builtins.property
    def event_bus_policy(self) -> builtins.str:
        """The JSON policy of this event bus resource.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        """
        result = self._values.get("event_bus_policy")
        assert result is not None, "Required property 'event_bus_policy' is missing"
        return result

    @builtins.property
    def event_source_name(self) -> typing.Optional[builtins.str]:
        """The partner event source to associate with this event bus resource.

        :default: - no partner event source

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        result = self._values.get("event_source_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBusAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.EventBusProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus_name": "eventBusName",
        "event_source_name": "eventSourceName",
    },
)
class EventBusProps:
    def __init__(
        self,
        *,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties to define an event bus.

        :param event_bus_name: The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this. Default: - automatically generated name
        :param event_source_name: The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this. Default: - no partner event source
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if event_bus_name is not None:
            self._values["event_bus_name"] = event_bus_name
        if event_source_name is not None:
            self._values["event_source_name"] = event_source_name

    @builtins.property
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        """The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this.

        :default: - automatically generated name

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        result = self._values.get("event_bus_name")
        return result

    @builtins.property
    def event_source_name(self) -> typing.Optional[builtins.str]:
        """The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this.

        :default: - no partner event source

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        result = self._values.get("event_source_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IResolvable)
class EventField(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.EventField"):
    """Represents a field in the event pattern."""

    @jsii.member(jsii_name="fromPath")
    @builtins.classmethod
    def from_path(cls, path: builtins.str) -> builtins.str:
        """Extract a custom JSON path from the event.

        :param path: -
        """
        return jsii.sinvoke(cls, "fromPath", [path])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _ctx: aws_cdk.core.IResolveContext) -> typing.Any:
        """Produce the Token's value at resolution time.

        :param _ctx: -
        """
        return jsii.invoke(self, "resolve", [_ctx])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        """Convert the path to the field in the event pattern to JSON."""
        return jsii.invoke(self, "toJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.
        """
        return jsii.invoke(self, "toString", [])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="account")
    def account(cls) -> builtins.str:
        """Extract the account from the event."""
        return jsii.sget(cls, "account")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="detailType")
    def detail_type(cls) -> builtins.str:
        """Extract the detail type from the event."""
        return jsii.sget(cls, "detailType")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="eventId")
    def event_id(cls) -> builtins.str:
        """Extract the event ID from the event."""
        return jsii.sget(cls, "eventId")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="region")
    def region(cls) -> builtins.str:
        """Extract the region from the event."""
        return jsii.sget(cls, "region")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="source")
    def source(cls) -> builtins.str:
        """Extract the source from the event."""
        return jsii.sget(cls, "source")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="time")
    def time(cls) -> builtins.str:
        """Extract the time from the event."""
        return jsii.sget(cls, "time")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        This may return an array with a single informational element indicating how
        to get this property populated, if it was skipped for performance reasons.
        """
        return jsii.get(self, "creationStack")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="displayHint")
    def display_hint(self) -> builtins.str:
        """Human readable display hint about the event pattern."""
        return jsii.get(self, "displayHint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        """the path to a field in the event pattern."""
        return jsii.get(self, "path")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.EventPattern",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "detail": "detail",
        "detail_type": "detailType",
        "id": "id",
        "region": "region",
        "resources": "resources",
        "source": "source",
        "time": "time",
        "version": "version",
    },
)
class EventPattern:
    def __init__(
        self,
        *,
        account: typing.Optional[typing.List[builtins.str]] = None,
        detail: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        detail_type: typing.Optional[typing.List[builtins.str]] = None,
        id: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[typing.List[builtins.str]] = None,
        resources: typing.Optional[typing.List[builtins.str]] = None,
        source: typing.Optional[typing.List[builtins.str]] = None,
        time: typing.Optional[typing.List[builtins.str]] = None,
        version: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Events in Amazon CloudWatch Events are represented as JSON objects. For more information about JSON objects, see RFC 7159.

        Rules use event patterns to select events and route them to targets. A
        pattern either matches an event or it doesn't. Event patterns are represented
        as JSON objects with a structure that is similar to that of events, for
        example:

        It is important to remember the following about event pattern matching:

        - For a pattern to match an event, the event must contain all the field names
          listed in the pattern. The field names must appear in the event with the
          same nesting structure.
        - Other fields of the event not mentioned in the pattern are ignored;
          effectively, there is a ``"*": "*"`` wildcard for fields not mentioned.
        - The matching is exact (character-by-character), without case-folding or any
          other string normalization.
        - The values being matched follow JSON rules: Strings enclosed in quotes,
          numbers, and the unquoted keywords true, false, and null.
        - Number matching is at the string representation level. For example, 300,
          300.0, and 3.0e2 are not considered equal.

        :param account: The 12-digit number identifying an AWS account. Default: - No filtering on account
        :param detail: A JSON object, whose content is at the discretion of the service originating the event. Default: - No filtering on detail
        :param detail_type: Identifies, in combination with the source field, the fields and values that appear in the detail field. Represents the "detail-type" event field. Default: - No filtering on detail type
        :param id: A unique value is generated for every event. This can be helpful in tracing events as they move through rules to targets, and are processed. Default: - No filtering on id
        :param region: Identifies the AWS region where the event originated. Default: - No filtering on region
        :param resources: This JSON array contains ARNs that identify resources that are involved in the event. Inclusion of these ARNs is at the discretion of the service. For example, Amazon EC2 instance state-changes include Amazon EC2 instance ARNs, Auto Scaling events include ARNs for both instances and Auto Scaling groups, but API calls with AWS CloudTrail do not include resource ARNs. Default: - No filtering on resource
        :param source: Identifies the service that sourced the event. All events sourced from within AWS begin with "aws." Customer-generated events can have any value here, as long as it doesn't begin with "aws." We recommend the use of Java package-name style reverse domain-name strings. To find the correct value for source for an AWS service, see the table in AWS Service Namespaces. For example, the source value for Amazon CloudFront is aws.cloudfront. Default: - No filtering on source
        :param time: The event timestamp, which can be specified by the service originating the event. If the event spans a time interval, the service might choose to report the start time, so this value can be noticeably before the time the event is actually received. Default: - No filtering on time
        :param version: By default, this is set to 0 (zero) in all events. Default: - No filtering on version

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if detail is not None:
            self._values["detail"] = detail
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if resources is not None:
            self._values["resources"] = resources
        if source is not None:
            self._values["source"] = source
        if time is not None:
            self._values["time"] = time
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def account(self) -> typing.Optional[typing.List[builtins.str]]:
        """The 12-digit number identifying an AWS account.

        :default: - No filtering on account
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def detail(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """A JSON object, whose content is at the discretion of the service originating the event.

        :default: - No filtering on detail
        """
        result = self._values.get("detail")
        return result

    @builtins.property
    def detail_type(self) -> typing.Optional[typing.List[builtins.str]]:
        """Identifies, in combination with the source field, the fields and values that appear in the detail field.

        Represents the "detail-type" event field.

        :default: - No filtering on detail type
        """
        result = self._values.get("detail_type")
        return result

    @builtins.property
    def id(self) -> typing.Optional[typing.List[builtins.str]]:
        """A unique value is generated for every event.

        This can be helpful in
        tracing events as they move through rules to targets, and are processed.

        :default: - No filtering on id
        """
        result = self._values.get("id")
        return result

    @builtins.property
    def region(self) -> typing.Optional[typing.List[builtins.str]]:
        """Identifies the AWS region where the event originated.

        :default: - No filtering on region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        """This JSON array contains ARNs that identify resources that are involved in the event.

        Inclusion of these ARNs is at the discretion of the
        service.

        For example, Amazon EC2 instance state-changes include Amazon EC2
        instance ARNs, Auto Scaling events include ARNs for both instances and
        Auto Scaling groups, but API calls with AWS CloudTrail do not include
        resource ARNs.

        :default: - No filtering on resource
        """
        result = self._values.get("resources")
        return result

    @builtins.property
    def source(self) -> typing.Optional[typing.List[builtins.str]]:
        """Identifies the service that sourced the event.

        All events sourced from
        within AWS begin with "aws." Customer-generated events can have any value
        here, as long as it doesn't begin with "aws." We recommend the use of
        Java package-name style reverse domain-name strings.

        To find the correct value for source for an AWS service, see the table in
        AWS Service Namespaces. For example, the source value for Amazon
        CloudFront is aws.cloudfront.

        :default: - No filtering on source

        :see: http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces
        """
        result = self._values.get("source")
        return result

    @builtins.property
    def time(self) -> typing.Optional[typing.List[builtins.str]]:
        """The event timestamp, which can be specified by the service originating the event.

        If the event spans a time interval, the service might choose
        to report the start time, so this value can be noticeably before the time
        the event is actually received.

        :default: - No filtering on time
        """
        result = self._values.get("time")
        return result

    @builtins.property
    def version(self) -> typing.Optional[typing.List[builtins.str]]:
        """By default, this is set to 0 (zero) in all events.

        :default: - No filtering on version
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-events.IEventBus")
class IEventBus(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Interface which all EventBus based classes MUST implement."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEventBusProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        """The ARN of this event bus resource.

        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> builtins.str:
        """The physical ID of this event bus resource.

        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> builtins.str:
        """The JSON policy of this event bus resource.

        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        """The partner event source to associate with this event bus resource.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        ...


class _IEventBusProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Interface which all EventBus based classes MUST implement."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-events.IEventBus"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        """The ARN of this event bus resource.

        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Arn-fn::getatt
        """
        return jsii.get(self, "eventBusArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> builtins.str:
        """The physical ID of this event bus resource.

        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-name
        """
        return jsii.get(self, "eventBusName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> builtins.str:
        """The JSON policy of this event bus resource.

        :attribute: true
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#Policy-fn::getatt
        """
        return jsii.get(self, "eventBusPolicy")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        """The partner event source to associate with this event bus resource.

        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbus.html#cfn-events-eventbus-eventsourcename
        """
        return jsii.get(self, "eventSourceName")


@jsii.interface(jsii_type="@aws-cdk/aws-events.IRule")
class IRule(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents an EventBridge Rule."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRuleProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> builtins.str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        """The name event rule.

        :attribute: true
        """
        ...


class _IRuleProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Represents an EventBridge Rule."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-events.IRule"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> builtins.str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        :attribute: true
        """
        return jsii.get(self, "ruleArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        """The name event rule.

        :attribute: true
        """
        return jsii.get(self, "ruleName")


@jsii.interface(jsii_type="@aws-cdk/aws-events.IRuleTarget")
class IRuleTarget(typing_extensions.Protocol):
    """An abstract target for EventRules."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRuleTargetProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: IRule,
        id: typing.Optional[builtins.str] = None,
    ) -> "RuleTargetConfig":
        """Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: The EventBridge Rule that would trigger this target.
        :param id: The id of the target that will be attached to the rule.
        """
        ...


class _IRuleTargetProxy:
    """An abstract target for EventRules."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-events.IRuleTarget"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: IRule,
        id: typing.Optional[builtins.str] = None,
    ) -> "RuleTargetConfig":
        """Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: The EventBridge Rule that would trigger this target.
        :param id: The id of the target that will be attached to the rule.
        """
        return jsii.invoke(self, "bind", [rule, id])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.OnEventOptions",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
    },
)
class OnEventOptions:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[IRuleTarget] = None,
    ) -> None:
        """Standard set of options for ``onXxx`` event handlers on construct.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        if isinstance(event_pattern, dict):
            event_pattern = EventPattern(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """A description of the rule's purpose.

        :default: - No description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Optional[EventPattern]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        """A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.
        """
        result = self._values.get("rule_name")
        return result

    @builtins.property
    def target(self) -> typing.Optional[IRuleTarget]:
        """The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        result = self._values.get("target")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnEventOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRule)
class Rule(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events.Rule",
):
    """Defines an EventBridge Rule in this stack.

    :resource: AWS::Events::Rule
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[IEventBus] = None,
        event_pattern: typing.Optional[EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional["Schedule"] = None,
        targets: typing.Optional[typing.List[IRuleTarget]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        props = RuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        jsii.create(Rule, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventRuleArn")
    @builtins.classmethod
    def from_event_rule_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        event_rule_arn: builtins.str,
    ) -> IRule:
        """Import an existing EventBridge Rule provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param event_rule_arn: Event Rule ARN (i.e. arn:aws:events:::rule/MyScheduledRule).
        """
        return jsii.sinvoke(cls, "fromEventRuleArn", [scope, id, event_rule_arn])

    @jsii.member(jsii_name="addEventPattern")
    def add_event_pattern(
        self,
        *,
        account: typing.Optional[typing.List[builtins.str]] = None,
        detail: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        detail_type: typing.Optional[typing.List[builtins.str]] = None,
        id: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[typing.List[builtins.str]] = None,
        resources: typing.Optional[typing.List[builtins.str]] = None,
        source: typing.Optional[typing.List[builtins.str]] = None,
        time: typing.Optional[typing.List[builtins.str]] = None,
        version: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Adds an event pattern filter to this rule.

        If a pattern was already specified,
        these values are merged into the existing pattern.

        For example, if the rule already contains the pattern::

           {
             "resources": [ "r1" ],
             "detail": {
               "hello": [ 1 ]
             }
           }

        And ``addEventPattern`` is called with the pattern::

           {
             "resources": [ "r2" ],
             "detail": {
               "foo": [ "bar" ]
             }
           }

        The resulting event pattern will be::

           {
             "resources": [ "r1", "r2" ],
             "detail": {
               "hello": [ 1 ],
               "foo": [ "bar" ]
             }
           }

        :param account: The 12-digit number identifying an AWS account. Default: - No filtering on account
        :param detail: A JSON object, whose content is at the discretion of the service originating the event. Default: - No filtering on detail
        :param detail_type: Identifies, in combination with the source field, the fields and values that appear in the detail field. Represents the "detail-type" event field. Default: - No filtering on detail type
        :param id: A unique value is generated for every event. This can be helpful in tracing events as they move through rules to targets, and are processed. Default: - No filtering on id
        :param region: Identifies the AWS region where the event originated. Default: - No filtering on region
        :param resources: This JSON array contains ARNs that identify resources that are involved in the event. Inclusion of these ARNs is at the discretion of the service. For example, Amazon EC2 instance state-changes include Amazon EC2 instance ARNs, Auto Scaling events include ARNs for both instances and Auto Scaling groups, but API calls with AWS CloudTrail do not include resource ARNs. Default: - No filtering on resource
        :param source: Identifies the service that sourced the event. All events sourced from within AWS begin with "aws." Customer-generated events can have any value here, as long as it doesn't begin with "aws." We recommend the use of Java package-name style reverse domain-name strings. To find the correct value for source for an AWS service, see the table in AWS Service Namespaces. For example, the source value for Amazon CloudFront is aws.cloudfront. Default: - No filtering on source
        :param time: The event timestamp, which can be specified by the service originating the event. If the event spans a time interval, the service might choose to report the start time, so this value can be noticeably before the time the event is actually received. Default: - No filtering on time
        :param version: By default, this is set to 0 (zero) in all events. Default: - No filtering on version
        """
        event_pattern = EventPattern(
            account=account,
            detail=detail,
            detail_type=detail_type,
            id=id,
            region=region,
            resources=resources,
            source=source,
            time=time,
            version=version,
        )

        return jsii.invoke(self, "addEventPattern", [event_pattern])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: typing.Optional[IRuleTarget] = None) -> None:
        """Adds a target to the rule. The abstract class RuleTarget can be extended to define new targets.

        No-op if target is undefined.

        :param target: -
        """
        return jsii.invoke(self, "addTarget", [target])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> builtins.str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example."""
        return jsii.get(self, "ruleArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        """The name event rule."""
        return jsii.get(self, "ruleName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.RuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "enabled": "enabled",
        "event_bus": "eventBus",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "schedule": "schedule",
        "targets": "targets",
    },
)
class RuleProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[IEventBus] = None,
        event_pattern: typing.Optional[EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional["Schedule"] = None,
        targets: typing.Optional[typing.List[IRuleTarget]] = None,
    ) -> None:
        """Properties for defining an EventBridge Rule.

        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        if isinstance(event_pattern, dict):
            event_pattern = EventPattern(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if schedule is not None:
            self._values["schedule"] = schedule
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """A description of the rule's purpose.

        :default: - No description.
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        """Indicates whether the rule is enabled.

        :default: true
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def event_bus(self) -> typing.Optional[IEventBus]:
        """The event bus to associate with this rule.

        :default: - The default event bus.
        """
        result = self._values.get("event_bus")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Optional[EventPattern]:
        """Describes which events EventBridge routes to the specified target.

        These routed events are matched events. For more information, see Events
        and Event Patterns in the Amazon EventBridge User Guide.

        :default: - None.

        :see:

        https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html

        You must specify this property (either via props or via
        ``addEventPattern``), the ``scheduleExpression`` property, or both. The
        method ``addEventPattern`` can be used to add filter values to the event
        pattern.
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        """A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see Name Type.
        """
        result = self._values.get("rule_name")
        return result

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        """The schedule or rate (frequency) that determines when EventBridge runs the rule.

        For more information, see Schedule Expression Syntax for
        Rules in the Amazon EventBridge User Guide.

        :default: - None.

        :see:

        https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html

        You must specify this property, the ``eventPattern`` property, or both.
        """
        result = self._values.get("schedule")
        return result

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[IRuleTarget]]:
        """Targets to invoke when this rule matches an event.

        Input will be the full matched event. If you wish to specify custom
        target input, use ``addTarget(target[, inputOptions])``.

        :default: - No targets.
        """
        result = self._values.get("targets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.RuleTargetConfig",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "id": "id",
        "batch_parameters": "batchParameters",
        "ecs_parameters": "ecsParameters",
        "input": "input",
        "kinesis_parameters": "kinesisParameters",
        "role": "role",
        "run_command_parameters": "runCommandParameters",
        "sqs_parameters": "sqsParameters",
        "target_resource": "targetResource",
    },
)
class RuleTargetConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        id: builtins.str,
        batch_parameters: typing.Optional[CfnRule.BatchParametersProperty] = None,
        ecs_parameters: typing.Optional[CfnRule.EcsParametersProperty] = None,
        input: typing.Optional["RuleTargetInput"] = None,
        kinesis_parameters: typing.Optional[CfnRule.KinesisParametersProperty] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        run_command_parameters: typing.Optional[CfnRule.RunCommandParametersProperty] = None,
        sqs_parameters: typing.Optional[CfnRule.SqsParametersProperty] = None,
        target_resource: typing.Optional[aws_cdk.core.IConstruct] = None,
    ) -> None:
        """Properties for an event rule target.

        :param arn: The Amazon Resource Name (ARN) of the target.
        :param id: (deprecated) A unique, user-defined identifier for the target. Acceptable values include alphanumeric characters, periods (.), hyphens (-), and underscores (_).
        :param batch_parameters: Parameters used when the rule invokes Amazon AWS Batch Job/Queue. Default: no parameters set
        :param ecs_parameters: The Amazon ECS task definition and task count to use, if the event target is an Amazon ECS task.
        :param input: What input to send to the event target. Default: the entire event
        :param kinesis_parameters: Settings that control shard assignment, when the target is a Kinesis stream. If you don't include this parameter, eventId is used as the partition key.
        :param role: Role to use to invoke this event target.
        :param run_command_parameters: Parameters used when the rule invokes Amazon EC2 Systems Manager Run Command.
        :param sqs_parameters: Parameters used when the FIFO sqs queue is used an event target by the rule.
        :param target_resource: The resource that is backing this target. This is the resource that will actually have some action performed on it when used as a target (for example, start a build for a CodeBuild project). We need it to determine whether the rule belongs to a different account than the target - if so, we generate a more complex setup, including an additional stack containing the EventBusPolicy. Default: the target is not backed by any resource
        """
        if isinstance(batch_parameters, dict):
            batch_parameters = CfnRule.BatchParametersProperty(**batch_parameters)
        if isinstance(ecs_parameters, dict):
            ecs_parameters = CfnRule.EcsParametersProperty(**ecs_parameters)
        if isinstance(kinesis_parameters, dict):
            kinesis_parameters = CfnRule.KinesisParametersProperty(**kinesis_parameters)
        if isinstance(run_command_parameters, dict):
            run_command_parameters = CfnRule.RunCommandParametersProperty(**run_command_parameters)
        if isinstance(sqs_parameters, dict):
            sqs_parameters = CfnRule.SqsParametersProperty(**sqs_parameters)
        self._values: typing.Dict[str, typing.Any] = {
            "arn": arn,
            "id": id,
        }
        if batch_parameters is not None:
            self._values["batch_parameters"] = batch_parameters
        if ecs_parameters is not None:
            self._values["ecs_parameters"] = ecs_parameters
        if input is not None:
            self._values["input"] = input
        if kinesis_parameters is not None:
            self._values["kinesis_parameters"] = kinesis_parameters
        if role is not None:
            self._values["role"] = role
        if run_command_parameters is not None:
            self._values["run_command_parameters"] = run_command_parameters
        if sqs_parameters is not None:
            self._values["sqs_parameters"] = sqs_parameters
        if target_resource is not None:
            self._values["target_resource"] = target_resource

    @builtins.property
    def arn(self) -> builtins.str:
        """The Amazon Resource Name (ARN) of the target."""
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return result

    @builtins.property
    def id(self) -> builtins.str:
        """(deprecated) A unique, user-defined identifier for the target.

        Acceptable values
        include alphanumeric characters, periods (.), hyphens (-), and
        underscores (_).

        :deprecated: prefer auto-generated id by specifying an empty string

        :stability: deprecated
        """
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return result

    @builtins.property
    def batch_parameters(self) -> typing.Optional[CfnRule.BatchParametersProperty]:
        """Parameters used when the rule invokes Amazon AWS Batch Job/Queue.

        :default: no parameters set
        """
        result = self._values.get("batch_parameters")
        return result

    @builtins.property
    def ecs_parameters(self) -> typing.Optional[CfnRule.EcsParametersProperty]:
        """The Amazon ECS task definition and task count to use, if the event target is an Amazon ECS task."""
        result = self._values.get("ecs_parameters")
        return result

    @builtins.property
    def input(self) -> typing.Optional["RuleTargetInput"]:
        """What input to send to the event target.

        :default: the entire event
        """
        result = self._values.get("input")
        return result

    @builtins.property
    def kinesis_parameters(self) -> typing.Optional[CfnRule.KinesisParametersProperty]:
        """Settings that control shard assignment, when the target is a Kinesis stream.

        If you don't include this parameter, eventId is used as the
        partition key.
        """
        result = self._values.get("kinesis_parameters")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role to use to invoke this event target."""
        result = self._values.get("role")
        return result

    @builtins.property
    def run_command_parameters(
        self,
    ) -> typing.Optional[CfnRule.RunCommandParametersProperty]:
        """Parameters used when the rule invokes Amazon EC2 Systems Manager Run Command."""
        result = self._values.get("run_command_parameters")
        return result

    @builtins.property
    def sqs_parameters(self) -> typing.Optional[CfnRule.SqsParametersProperty]:
        """Parameters used when the FIFO sqs queue is used an event target by the rule."""
        result = self._values.get("sqs_parameters")
        return result

    @builtins.property
    def target_resource(self) -> typing.Optional[aws_cdk.core.IConstruct]:
        """The resource that is backing this target.

        This is the resource that will actually have some action performed on it when used as a target
        (for example, start a build for a CodeBuild project).
        We need it to determine whether the rule belongs to a different account than the target -
        if so, we generate a more complex setup,
        including an additional stack containing the EventBusPolicy.

        :default: the target is not backed by any resource

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-cross-account-event-delivery.html
        """
        result = self._values.get("target_resource")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RuleTargetInput(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-events.RuleTargetInput",
):
    """The input to send to the event target."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _RuleTargetInputProxy

    def __init__(self) -> None:
        jsii.create(RuleTargetInput, self, [])

    @jsii.member(jsii_name="fromEventPath")
    @builtins.classmethod
    def from_event_path(cls, path: builtins.str) -> "RuleTargetInput":
        """Take the event target input from a path in the event JSON.

        :param path: -
        """
        return jsii.sinvoke(cls, "fromEventPath", [path])

    @jsii.member(jsii_name="fromMultilineText")
    @builtins.classmethod
    def from_multiline_text(cls, text: builtins.str) -> "RuleTargetInput":
        """Pass text to the event target, splitting on newlines.

        This is only useful when passing to a target that does not
        take a single argument.

        May contain strings returned by EventField.from() to substitute in parts
        of the matched event.

        :param text: -
        """
        return jsii.sinvoke(cls, "fromMultilineText", [text])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, obj: typing.Any) -> "RuleTargetInput":
        """Pass a JSON object to the event target.

        May contain strings returned by EventField.from() to substitute in parts of the
        matched event.

        :param obj: -
        """
        return jsii.sinvoke(cls, "fromObject", [obj])

    @jsii.member(jsii_name="fromText")
    @builtins.classmethod
    def from_text(cls, text: builtins.str) -> "RuleTargetInput":
        """Pass text to the event target.

        May contain strings returned by EventField.from() to substitute in parts of the
        matched event.

        :param text: -
        """
        return jsii.sinvoke(cls, "fromText", [text])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, rule: IRule) -> "RuleTargetInputProperties":
        """Return the input properties for this input object.

        :param rule: -
        """
        ...


class _RuleTargetInputProxy(RuleTargetInput):
    @jsii.member(jsii_name="bind")
    def bind(self, rule: IRule) -> "RuleTargetInputProperties":
        """Return the input properties for this input object.

        :param rule: -
        """
        return jsii.invoke(self, "bind", [rule])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-events.RuleTargetInputProperties",
    jsii_struct_bases=[],
    name_mapping={
        "input": "input",
        "input_path": "inputPath",
        "input_paths_map": "inputPathsMap",
        "input_template": "inputTemplate",
    },
)
class RuleTargetInputProperties:
    def __init__(
        self,
        *,
        input: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        input_paths_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_template: typing.Optional[builtins.str] = None,
    ) -> None:
        """The input properties for an event target.

        :param input: Literal input to the target service (must be valid JSON). Default: - input for the event target. If the input contains a paths map values wil be extracted from event and inserted into the ``inputTemplate``.
        :param input_path: JsonPath to take input from the input event. Default: - None. The entire matched event is passed as input
        :param input_paths_map: Paths map to extract values from event and insert into ``inputTemplate``. Default: - No values extracted from event.
        :param input_template: Input template to insert paths map into. Default: - None.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if input is not None:
            self._values["input"] = input
        if input_path is not None:
            self._values["input_path"] = input_path
        if input_paths_map is not None:
            self._values["input_paths_map"] = input_paths_map
        if input_template is not None:
            self._values["input_template"] = input_template

    @builtins.property
    def input(self) -> typing.Optional[builtins.str]:
        """Literal input to the target service (must be valid JSON).

        :default:

        - input for the event target. If the input contains a paths map
        values wil be extracted from event and inserted into the ``inputTemplate``.
        """
        result = self._values.get("input")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JsonPath to take input from the input event.

        :default: - None. The entire matched event is passed as input
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def input_paths_map(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Paths map to extract values from event and insert into ``inputTemplate``.

        :default: - No values extracted from event.
        """
        result = self._values.get("input_paths_map")
        return result

    @builtins.property
    def input_template(self) -> typing.Optional[builtins.str]:
        """Input template to insert paths map into.

        :default: - None.
        """
        result = self._values.get("input_template")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleTargetInputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Schedule(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-events.Schedule",
):
    """Schedule for scheduled event rules."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ScheduleProxy

    def __init__(self) -> None:
        jsii.create(Schedule, self, [])

    @jsii.member(jsii_name="cron")
    @builtins.classmethod
    def cron(
        cls,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> "Schedule":
        """Create a schedule from a set of cron fields.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year
        """
        options = CronOptions(
            day=day,
            hour=hour,
            minute=minute,
            month=month,
            week_day=week_day,
            year=year,
        )

        return jsii.sinvoke(cls, "cron", [options])

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(cls, expression: builtins.str) -> "Schedule":
        """Construct a schedule from a literal schedule expression.

        :param expression: The expression to use. Must be in a format that EventBridge will recognize
        """
        return jsii.sinvoke(cls, "expression", [expression])

    @jsii.member(jsii_name="rate")
    @builtins.classmethod
    def rate(cls, duration: aws_cdk.core.Duration) -> "Schedule":
        """Construct a schedule from an interval and a time unit.

        :param duration: -
        """
        return jsii.sinvoke(cls, "rate", [duration])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="expressionString")
    @abc.abstractmethod
    def expression_string(self) -> builtins.str:
        """Retrieve the expression for this schedule."""
        ...


class _ScheduleProxy(Schedule):
    @builtins.property # type: ignore
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> builtins.str:
        """Retrieve the expression for this schedule."""
        return jsii.get(self, "expressionString")


@jsii.implements(IEventBus)
class EventBus(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-events.EventBus",
):
    """Define an EventBridge EventBus.

    :resource: AWS::Events::EventBus
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        event_bus_name: typing.Optional[builtins.str] = None,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param event_bus_name: The name of the event bus you are creating Note: If 'eventSourceName' is passed in, you cannot set this. Default: - automatically generated name
        :param event_source_name: The partner event source to associate with this event bus resource Note: If 'eventBusName' is passed in, you cannot set this. Default: - no partner event source
        """
        props = EventBusProps(
            event_bus_name=event_bus_name, event_source_name=event_source_name
        )

        jsii.create(EventBus, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventBusArn")
    @builtins.classmethod
    def from_event_bus_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        event_bus_arn: builtins.str,
    ) -> IEventBus:
        """Import an existing event bus resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param event_bus_arn: ARN of imported event bus.
        """
        return jsii.sinvoke(cls, "fromEventBusArn", [scope, id, event_bus_arn])

    @jsii.member(jsii_name="fromEventBusAttributes")
    @builtins.classmethod
    def from_event_bus_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        event_bus_arn: builtins.str,
        event_bus_name: builtins.str,
        event_bus_policy: builtins.str,
        event_source_name: typing.Optional[builtins.str] = None,
    ) -> IEventBus:
        """Import an existing event bus resource.

        :param scope: Parent construct.
        :param id: Construct ID.
        :param event_bus_arn: The ARN of this event bus resource.
        :param event_bus_name: The physical ID of this event bus resource.
        :param event_bus_policy: The JSON policy of this event bus resource.
        :param event_source_name: The partner event source to associate with this event bus resource. Default: - no partner event source
        """
        attrs = EventBusAttributes(
            event_bus_arn=event_bus_arn,
            event_bus_name=event_bus_name,
            event_bus_policy=event_bus_policy,
            event_source_name=event_source_name,
        )

        return jsii.sinvoke(cls, "fromEventBusAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="grantPutEvents")
    @builtins.classmethod
    def grant_put_events(
        cls,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Permits an IAM Principal to send custom events to EventBridge so that they can be matched to rules.

        :param grantee: The principal (no-op if undefined).
        """
        return jsii.sinvoke(cls, "grantPutEvents", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        """The ARN of the event bus, such as: arn:aws:events:us-east-2:123456789012:event-bus/aws.partner/PartnerName/acct1/repo1."""
        return jsii.get(self, "eventBusArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> builtins.str:
        """The physical ID of this event bus resource."""
        return jsii.get(self, "eventBusName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventBusPolicy")
    def event_bus_policy(self) -> builtins.str:
        """The policy for the event bus in JSON form."""
        return jsii.get(self, "eventBusPolicy")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventSourceName")
    def event_source_name(self) -> typing.Optional[builtins.str]:
        """The name of the partner event source."""
        return jsii.get(self, "eventSourceName")


__all__ = [
    "CfnArchive",
    "CfnArchiveProps",
    "CfnEventBus",
    "CfnEventBusPolicy",
    "CfnEventBusPolicyProps",
    "CfnEventBusProps",
    "CfnRule",
    "CfnRuleProps",
    "CronOptions",
    "EventBus",
    "EventBusAttributes",
    "EventBusProps",
    "EventField",
    "EventPattern",
    "IEventBus",
    "IRule",
    "IRuleTarget",
    "OnEventOptions",
    "Rule",
    "RuleProps",
    "RuleTargetConfig",
    "RuleTargetInput",
    "RuleTargetInputProperties",
    "Schedule",
]

publication.publish()
