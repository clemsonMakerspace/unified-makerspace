"""
## Amazon EC2 Auto Scaling Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

### Auto Scaling Group

An `AutoScalingGroup` represents a number of instances on which you run your code. You
pick the size of the fleet, the instance type and the OS image:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_ec2 as ec2

autoscaling.AutoScalingGroup(self, "ASG",
    vpc=vpc,
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
    machine_image=ec2.AmazonLinuxImage()
)
```

NOTE: AutoScalingGroup has an property called `allowAllOutbound` (allowing the instances to contact the
internet) which is set to `true` by default. Be sure to set this to `false`  if you don't want
your instances to be able to start arbitrary connections. Alternatively, you can specify an existing security
group to attach to the instances that are launched, rather than have the group create a new one.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_security_group = ec2.SecurityGroup(self, "SecurityGroup", ...)
autoscaling.AutoScalingGroup(self, "ASG",
    vpc=vpc,
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
    machine_image=ec2.AmazonLinuxImage(),
    security_group=my_security_group
)
```

### Machine Images (AMIs)

AMIs control the OS that gets launched when you start your EC2 instance. The EC2
library contains constructs to select the AMI you want to use.

Depending on the type of AMI, you select it a different way.

The latest version of Amazon Linux and Microsoft Windows images are
selectable by instantiating one of these classes:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Pick a Windows edition to use
windows = ec2.WindowsImage(ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE)

# Pick the right Amazon Linux edition. All arguments shown are optional
# and will default to these values when omitted.
amzn_linux = ec2.AmazonLinuxImage(
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

# For other custom (Linux) images, instantiate a `GenericLinuxImage` with
# a map giving the AMI to in for each region:

linux = ec2.GenericLinuxImage({
    "us-east-1": "ami-97785bed",
    "eu-west-1": "ami-12345678"
})
```

> NOTE: The Amazon Linux images selected will be cached in your `cdk.json`, so that your
> AutoScalingGroups don't automatically change out from under you when you're making unrelated
> changes. To update to the latest version of Amazon Linux, remove the cache entry from the `context`
> section of your `cdk.json`.
>
> We will add command-line options to make this step easier in the future.

### AutoScaling Instance Counts

AutoScalingGroups make it possible to raise and lower the number of instances in the group,
in response to (or in advance of) changes in workload.

When you create your AutoScalingGroup, you specify a `minCapacity` and a
`maxCapacity`. AutoScaling policies that respond to metrics will never go higher
or lower than the indicated capacity (but scheduled scaling actions might, see
below).

There are three ways to scale your capacity:

* **In response to a metric** (also known as step scaling); for example, you
  might want to scale out if the CPU usage across your cluster starts to rise,
  and scale in when it drops again.
* **By trying to keep a certain metric around a given value** (also known as
  target tracking scaling); you might want to automatically scale out and in to
  keep your CPU usage around 50%.
* **On a schedule**; you might want to organize your scaling around traffic
  flows you expect, by scaling out in the morning and scaling in in the
  evening.

The general pattern of autoscaling will look like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
    min_capacity=5,
    max_capacity=100
)

# Step scaling
auto_scaling_group.scale_on_metric(...)

# Target tracking scaling
auto_scaling_group.scale_on_cpu_utilization(...)
auto_scaling_group.scale_on_incoming_bytes(...)
auto_scaling_group.scale_on_outgoing_bytes(...)
auto_scaling_group.scale_on_request_count(...)
auto_scaling_group.scale_to_track_metric(...)

# Scheduled scaling
auto_scaling_group.scale_on_schedule(...)
```

#### Step Scaling

This type of scaling scales in and out in deterministics steps that you
configure, in response to metric values. For example, your scaling strategy to
scale in response to a metric that represents your average worker pool usage
might look like this:

```
 Scaling        -1          (no change)          +1       +3
            │        │                       │        │        │
            ├────────┼───────────────────────┼────────┼────────┤
            │        │                       │        │        │
Worker use  0%      10%                     50%       70%     100%
```

(Note that this is not necessarily a recommended scaling strategy, but it's
a possible one. You will have to determine what thresholds are right for you).

Note that in order to set up this scaling strategy, you will have to emit a
metric representing your worker utilization from your instances. After that,
you would configure the scaling something like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
worker_utilization_metric = cloudwatch.Metric(
    namespace="MyService",
    metric_name="WorkerUtilization"
)

capacity.scale_on_metric("ScaleToCPU",
    metric=worker_utilization_metric,
    scaling_steps=[{"upper": 10, "change": -1}, {"lower": 50, "change": +1}, {"lower": 70, "change": +3}
    ],

    # Change this to AdjustmentType.PERCENT_CHANGE_IN_CAPACITY to interpret the
    # 'change' numbers before as percentages instead of capacity counts.
    adjustment_type=autoscaling.AdjustmentType.CHANGE_IN_CAPACITY
)
```

The AutoScaling construct library will create the required CloudWatch alarms and
AutoScaling policies for you.

#### Target Tracking Scaling

This type of scaling scales in and out in order to keep a metric around a value
you prefer. There are four types of predefined metrics you can track, or you can
choose to track a custom metric. If you do choose to track a custom metric,
be aware that the metric has to represent instance utilization in some way
(AutoScaling will scale out if the metric is higher than the target, and scale
in if the metric is lower than the target).

If you configure multiple target tracking policies, AutoScaling will use the
one that yields the highest capacity.

The following example scales to keep the CPU usage of your instances around
50% utilization:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_cpu_utilization("KeepSpareCPU",
    target_utilization_percent=50
)
```

To scale on average network traffic in and out of your instances:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_incoming_bytes("LimitIngressPerInstance",
    target_bytes_per_second=10 * 1024 * 1024
)
auto_scaling_group.scale_on_outcoming_bytes("LimitEgressPerInstance",
    target_bytes_per_second=10 * 1024 * 1024
)
```

To scale on the average request count per instance (only works for
AutoScalingGroups that have been attached to Application Load
Balancers):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_request_count("LimitRPS",
    target_requests_per_second=1000
)
```

#### Scheduled Scaling

This type of scaling is used to change capacities based on time. It works by
changing `minCapacity`, `maxCapacity` and `desiredCapacity` of the
AutoScalingGroup, and so can be used for two purposes:

* Scale in and out on a schedule by setting the `minCapacity` high or
  the `maxCapacity` low.
* Still allow the regular scaling actions to do their job, but restrict
  the range they can scale over (by setting both `minCapacity` and
  `maxCapacity` but changing their range over time).

A schedule is expressed as a cron expression. The `Schedule` class has a `cron` method to help build cron expressions.

The following example scales the fleet out in the morning, going back to natural
scaling (all the way down to 1 instance if necessary) at night:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_schedule("PrescaleInTheMorning",
    schedule=autoscaling.Schedule.cron(hour="8", minute="0"),
    min_capacity=20
)

auto_scaling_group.scale_on_schedule("AllowDownscalingAtNight",
    schedule=autoscaling.Schedule.cron(hour="20", minute="0"),
    min_capacity=1
)
```

### Configuring Instances using CloudFormation Init

It is possible to use the CloudFormation Init mechanism to configure the
instances in the AutoScalingGroup. You can write files to it, run commands,
start services, etc. See the documentation of
[AWS::CloudFormation::Init](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html)
and the documentation of CDK's `aws-ec2` library for more information.

When you specify a CloudFormation Init configuration for an AutoScalingGroup:

* you *must* also specify `signals` to configure how long CloudFormation
  should wait for the instances to successfully configure themselves.
* you *should* also specify an `updatePolicy` to configure how instances
  should be updated when the AutoScalingGroup is updated (for example,
  when the AMI is updated). If you don't specify an update policy, a *rolling
  update* is chosen by default.

Here's an example of using CloudFormation Init to write a file to the
instance hosts on startup:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
autoscaling.AutoScalingGroup(self, "ASG",
    # ...

    init=ec2.CloudFormationInit.from_elements(
        ec2.InitFile.from_string("/etc/my_instance", "This got written during instance startup")),
    signals=autoscaling.Signals.wait_for_all(
        timeout=Duration.minutes(10)
    )
)
```

### Signals

In normal operation, CloudFormation will send a Create or Update command to
an AutoScalingGroup and proceed with the rest of the deployment without waiting
for the *instances in the AutoScalingGroup*.

Configure `signals` to tell CloudFormation to wait for a specific number of
instances in the AutoScalingGroup to have been started (or failed to start)
before moving on. An instance is supposed to execute the
[`cfn-signal`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-signal.html)
program as part of its startup to indicate whether it was started
successfully or not.

If you use CloudFormation Init support (described in the previous section),
the appropriate call to `cfn-signal` is automatically added to the
AutoScalingGroup's UserData. If you don't use the `signals` directly, you are
responsible for adding such a call yourself.

The following type of `Signals` are available:

* `Signals.waitForAll([options])`: wait for all of `desiredCapacity` amount of instances
  to have started (recommended).
* `Signals.waitForMinCapacity([options])`: wait for a `minCapacity` amount of instances
  to have started (use this if waiting for all instances takes too long and you are happy
  with a minimum count of healthy hosts).
* `Signals.waitForCount(count, [options])`: wait for a specific amount of instances to have
  started.

There are two `options` you can configure:

* `timeout`: maximum time a host startup is allowed to take. If a host does not report
  success within this time, it is considered a failure. Default is 5 minutes.
* `minSuccessPercentage`: percentage of hosts that needs to be healthy in order for the
  update to succeed. If you set this value lower than 100, some percentage of hosts may
  report failure, while still considering the deployment a success. Default is 100%.

### Update Policy

The *update policy* describes what should happen to running instances when the definition
of the AutoScalingGroup is changed. For example, if you add a command to the UserData
of an AutoScalingGroup, do the existing instances get replaced with new instances that
have executed the new UserData? Or do the "old" instances just keep on running?

It is recommended to always use an update policy, otherwise the current state of your
instances also depends the previous state of your instances, rather than just on your
source code. This degrades the reproducibility of your deployments.

The following update policies are available:

* `UpdatePolicy.none()`: leave existing instances alone (not recommended).
* `UpdatePolicy.rollingUpdate([options])`: progressively replace the existing
  instances with new instances, in small batches. At any point in time,
  roughly the same amount of total instances will be running. If the deployment
  needs to be rolled back, the fresh instances will be replaced with the "old"
  configuration again.
* `UpdatePolicy.replacingUpdate([options])`: build a completely fresh copy
  of the new AutoScalingGroup next to the old one. Once the AutoScalingGroup
  has been successfully created (and the instances started, if `signals` is
  configured on the AutoScalingGroup), the old AutoScalingGroup is deleted.
  If the deployment needs to be rolled back, the new AutoScalingGroup is
  deleted and the old one is left unchanged.

### Allowing Connections

See the documentation of the `@aws-cdk/aws-ec2` package for more information
about allowing connections between resources backed by instances.

### Max Instance Lifetime

To enable the max instance lifetime support, specify `maxInstanceLifetime` property
for the `AutoscalingGroup` resource. The value must be between 7 and 365 days(inclusive).
To clear a previously set value, leave this property undefined.

### Instance Monitoring

To disable detailed instance monitoring, specify `instanceMonitoring` property
for the `AutoscalingGroup` resource as `Monitoring.BASIC`. Otherwise detailed monitoring
will be enabled.

### Monitoring Group Metrics

Group metrics are used to monitor group level properties; they describe the group rather than any of its instances (e.g GroupMaxSize, the group maximum size). To enable group metrics monitoring, use the `groupMetrics` property.
All group metrics are reported in a granularity of 1 minute at no additional charge.

See [EC2 docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-instance-monitoring.html#as-group-metrics) for a list of all available group metrics.

To enable group metrics monitoring using the `groupMetrics` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Enable monitoring of all group metrics
autoscaling.AutoScalingGroup(stack, "ASG",
    group_metrics=[GroupMetrics.all()]
)

# Enable monitoring for a subset of group metrics
autoscaling.AutoScalingGroup(stack, "ASG",
    group_metrics=[autoscaling.GroupMetrics(GroupMetric.MIN_SIZE, GroupMetric.MAX_SIZE)]
)
```

### Future work

* [ ] CloudWatch Events (impossible to add currently as the AutoScalingGroup ARN is
  necessary to make this rule and this cannot be accessed from CloudFormation).
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

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_sns
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.AdjustmentTier",
    jsii_struct_bases=[],
    name_mapping={
        "adjustment": "adjustment",
        "lower_bound": "lowerBound",
        "upper_bound": "upperBound",
    },
)
class AdjustmentTier:
    def __init__(
        self,
        *,
        adjustment: jsii.Number,
        lower_bound: typing.Optional[jsii.Number] = None,
        upper_bound: typing.Optional[jsii.Number] = None,
    ) -> None:
        """An adjustment.

        :param adjustment: What number to adjust the capacity with. The number is interpeted as an added capacity, a new fixed capacity or an added percentage depending on the AdjustmentType value of the StepScalingPolicy. Can be positive or negative.
        :param lower_bound: Lower bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is higher than this value. Default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        :param upper_bound: Upper bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is lower than this value. Default: +Infinity
        """
        self._values: typing.Dict[str, typing.Any] = {
            "adjustment": adjustment,
        }
        if lower_bound is not None:
            self._values["lower_bound"] = lower_bound
        if upper_bound is not None:
            self._values["upper_bound"] = upper_bound

    @builtins.property
    def adjustment(self) -> jsii.Number:
        """What number to adjust the capacity with.

        The number is interpeted as an added capacity, a new fixed capacity or an
        added percentage depending on the AdjustmentType value of the
        StepScalingPolicy.

        Can be positive or negative.
        """
        result = self._values.get("adjustment")
        assert result is not None, "Required property 'adjustment' is missing"
        return result

    @builtins.property
    def lower_bound(self) -> typing.Optional[jsii.Number]:
        """Lower bound where this scaling tier applies.

        The scaling tier applies if the difference between the metric
        value and its alarm threshold is higher than this value.

        :default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        """
        result = self._values.get("lower_bound")
        return result

    @builtins.property
    def upper_bound(self) -> typing.Optional[jsii.Number]:
        """Upper bound where this scaling tier applies.

        The scaling tier applies if the difference between the metric
        value and its alarm threshold is lower than this value.

        :default: +Infinity
        """
        result = self._values.get("upper_bound")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdjustmentTier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.AdjustmentType")
class AdjustmentType(enum.Enum):
    """How adjustment numbers are interpreted."""

    CHANGE_IN_CAPACITY = "CHANGE_IN_CAPACITY"
    """Add the adjustment number to the current capacity.

    A positive number increases capacity, a negative number decreases capacity.
    """
    PERCENT_CHANGE_IN_CAPACITY = "PERCENT_CHANGE_IN_CAPACITY"
    """Add this percentage of the current capacity to itself.

    The number must be between -100 and 100; a positive number increases
    capacity and a negative number decreases it.
    """
    EXACT_CAPACITY = "EXACT_CAPACITY"
    """Make the capacity equal to the exact number given."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.ApplyCloudFormationInitOptions",
    jsii_struct_bases=[],
    name_mapping={
        "config_sets": "configSets",
        "embed_fingerprint": "embedFingerprint",
        "ignore_failures": "ignoreFailures",
        "print_log": "printLog",
    },
)
class ApplyCloudFormationInitOptions:
    def __init__(
        self,
        *,
        config_sets: typing.Optional[typing.List[builtins.str]] = None,
        embed_fingerprint: typing.Optional[builtins.bool] = None,
        ignore_failures: typing.Optional[builtins.bool] = None,
        print_log: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Options for applying CloudFormation init to an instance or instance group.

        :param config_sets: ConfigSet to activate. Default: ['default']
        :param embed_fingerprint: Force instance replacement by embedding a config fingerprint. If ``true`` (the default), a hash of the config will be embedded into the UserData, so that if the config changes, the UserData changes and instances will be replaced (given an UpdatePolicy has been configured on the AutoScalingGroup). If ``false``, no such hash will be embedded, and if the CloudFormation Init config changes nothing will happen to the running instances. If a config update introduces errors, you will not notice until after the CloudFormation deployment successfully finishes and the next instance fails to launch. Default: true
        :param ignore_failures: Don't fail the instance creation when cfn-init fails. You can use this to prevent CloudFormation from rolling back when instances fail to start up, to help in debugging. Default: false
        :param print_log: Print the results of running cfn-init to the Instance System Log. By default, the output of running cfn-init is written to a log file on the instance. Set this to ``true`` to print it to the System Log (visible from the EC2 Console), ``false`` to not print it. (Be aware that the system log is refreshed at certain points in time of the instance life cycle, and successful execution may not always show up). Default: true
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if config_sets is not None:
            self._values["config_sets"] = config_sets
        if embed_fingerprint is not None:
            self._values["embed_fingerprint"] = embed_fingerprint
        if ignore_failures is not None:
            self._values["ignore_failures"] = ignore_failures
        if print_log is not None:
            self._values["print_log"] = print_log

    @builtins.property
    def config_sets(self) -> typing.Optional[typing.List[builtins.str]]:
        """ConfigSet to activate.

        :default: ['default']
        """
        result = self._values.get("config_sets")
        return result

    @builtins.property
    def embed_fingerprint(self) -> typing.Optional[builtins.bool]:
        """Force instance replacement by embedding a config fingerprint.

        If ``true`` (the default), a hash of the config will be embedded into the
        UserData, so that if the config changes, the UserData changes and
        instances will be replaced (given an UpdatePolicy has been configured on
        the AutoScalingGroup).

        If ``false``, no such hash will be embedded, and if the CloudFormation Init
        config changes nothing will happen to the running instances. If a
        config update introduces errors, you will not notice until after the
        CloudFormation deployment successfully finishes and the next instance
        fails to launch.

        :default: true
        """
        result = self._values.get("embed_fingerprint")
        return result

    @builtins.property
    def ignore_failures(self) -> typing.Optional[builtins.bool]:
        """Don't fail the instance creation when cfn-init fails.

        You can use this to prevent CloudFormation from rolling back when
        instances fail to start up, to help in debugging.

        :default: false
        """
        result = self._values.get("ignore_failures")
        return result

    @builtins.property
    def print_log(self) -> typing.Optional[builtins.bool]:
        """Print the results of running cfn-init to the Instance System Log.

        By default, the output of running cfn-init is written to a log file
        on the instance. Set this to ``true`` to print it to the System Log
        (visible from the EC2 Console), ``false`` to not print it.

        (Be aware that the system log is refreshed at certain points in
        time of the instance life cycle, and successful execution may
        not always show up).

        :default: true
        """
        result = self._values.get("print_log")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplyCloudFormationInitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.BaseTargetTrackingProps",
    jsii_struct_bases=[],
    name_mapping={
        "cooldown": "cooldown",
        "disable_scale_in": "disableScaleIn",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
    },
)
class BaseTargetTrackingProps:
    def __init__(
        self,
        *,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Base interface for target tracking props.

        Contains the attributes that are common to target tracking policies,
        except the ones relating to the metric and to the scalable target.

        This interface is reused by more specific target tracking props objects.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        :default: false
        """
        result = self._values.get("disable_scale_in")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: - Same as the cooldown.
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseTargetTrackingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.BasicLifecycleHookProps",
    jsii_struct_bases=[],
    name_mapping={
        "lifecycle_transition": "lifecycleTransition",
        "notification_target": "notificationTarget",
        "default_result": "defaultResult",
        "heartbeat_timeout": "heartbeatTimeout",
        "lifecycle_hook_name": "lifecycleHookName",
        "notification_metadata": "notificationMetadata",
        "role": "role",
    },
)
class BasicLifecycleHookProps:
    def __init__(
        self,
        *,
        lifecycle_transition: "LifecycleTransition",
        notification_target: "ILifecycleHookTarget",
        default_result: typing.Optional["DefaultResult"] = None,
        heartbeat_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """Basic properties for a lifecycle hook.

        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "lifecycle_transition": lifecycle_transition,
            "notification_target": notification_target,
        }
        if default_result is not None:
            self._values["default_result"] = default_result
        if heartbeat_timeout is not None:
            self._values["heartbeat_timeout"] = heartbeat_timeout
        if lifecycle_hook_name is not None:
            self._values["lifecycle_hook_name"] = lifecycle_hook_name
        if notification_metadata is not None:
            self._values["notification_metadata"] = notification_metadata
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def lifecycle_transition(self) -> "LifecycleTransition":
        """The state of the Amazon EC2 instance to which you want to attach the lifecycle hook."""
        result = self._values.get("lifecycle_transition")
        assert result is not None, "Required property 'lifecycle_transition' is missing"
        return result

    @builtins.property
    def notification_target(self) -> "ILifecycleHookTarget":
        """The target of the lifecycle hook."""
        result = self._values.get("notification_target")
        assert result is not None, "Required property 'notification_target' is missing"
        return result

    @builtins.property
    def default_result(self) -> typing.Optional["DefaultResult"]:
        """The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs.

        :default: Continue
        """
        result = self._values.get("default_result")
        return result

    @builtins.property
    def heartbeat_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum time between calls to RecordLifecycleActionHeartbeat for the hook.

        If the lifecycle hook times out, perform the action in DefaultResult.

        :default: - No heartbeat timeout.
        """
        result = self._values.get("heartbeat_timeout")
        return result

    @builtins.property
    def lifecycle_hook_name(self) -> typing.Optional[builtins.str]:
        """Name of the lifecycle hook.

        :default: - Automatically generated name.
        """
        result = self._values.get("lifecycle_hook_name")
        return result

    @builtins.property
    def notification_metadata(self) -> typing.Optional[builtins.str]:
        """Additional data to pass to the lifecycle hook target.

        :default: - No metadata.
        """
        result = self._values.get("notification_metadata")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role that allows publishing to the notification target.

        :default: - A role is automatically created.
        """
        result = self._values.get("role")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicLifecycleHookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.BasicScheduledActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "desired_capacity": "desiredCapacity",
        "end_time": "endTime",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "start_time": "startTime",
    },
)
class BasicScheduledActionProps:
    def __init__(
        self,
        *,
        schedule: "Schedule",
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> None:
        """Properties for a scheduled scaling action.

        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "schedule": schedule,
        }
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if end_time is not None:
            self._values["end_time"] = end_time
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def schedule(self) -> "Schedule":
        """When to perform this action.

        Supports cron expressions.

        For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            08 * * ?
        """
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return result

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """The new desired capacity.

        At the scheduled time, set the desired capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        :default: - No new desired capacity.
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def end_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action expires.

        :default: - The rule never expires.
        """
        result = self._values.get("end_time")
        return result

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """The new maximum capacity.

        At the scheduled time, set the maximum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        :default: - No new maximum capacity.
        """
        result = self._values.get("max_capacity")
        return result

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """The new minimum capacity.

        At the scheduled time, set the minimum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        :default: - No new minimum capacity.
        """
        result = self._values.get("min_capacity")
        return result

    @builtins.property
    def start_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action becomes active.

        :default: - The rule is activate immediately.
        """
        result = self._values.get("start_time")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicScheduledActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.BasicStepScalingPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "metric": "metric",
        "scaling_steps": "scalingSteps",
        "adjustment_type": "adjustmentType",
        "cooldown": "cooldown",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "min_adjustment_magnitude": "minAdjustmentMagnitude",
    },
)
class BasicStepScalingPolicyProps:
    def __init__(
        self,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        scaling_steps: typing.List["ScalingInterval"],
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metric": metric,
            "scaling_steps": scaling_steps,
        }
        if adjustment_type is not None:
            self._values["adjustment_type"] = adjustment_type
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if min_adjustment_magnitude is not None:
            self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @builtins.property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to scale on."""
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return result

    @builtins.property
    def scaling_steps(self) -> typing.List["ScalingInterval"]:
        """The intervals for scaling.

        Maps a range of metric values to a particular scaling behavior.
        """
        result = self._values.get("scaling_steps")
        assert result is not None, "Required property 'scaling_steps' is missing"
        return result

    @builtins.property
    def adjustment_type(self) -> typing.Optional[AdjustmentType]:
        """How the adjustment numbers inside 'intervals' are interpreted.

        :default: ChangeInCapacity
        """
        result = self._values.get("adjustment_type")
        return result

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Grace period after scaling activity.

        :default: Default cooldown period on your AutoScalingGroup
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: Same as the cooldown
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        :default: No minimum scaling effect
        """
        result = self._values.get("min_adjustment_magnitude")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicStepScalingPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.BasicTargetTrackingScalingPolicyProps",
    jsii_struct_bases=[BaseTargetTrackingProps],
    name_mapping={
        "cooldown": "cooldown",
        "disable_scale_in": "disableScaleIn",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "target_value": "targetValue",
        "custom_metric": "customMetric",
        "predefined_metric": "predefinedMetric",
        "resource_label": "resourceLabel",
    },
)
class BasicTargetTrackingScalingPolicyProps(BaseTargetTrackingProps):
    def __init__(
        self,
        *,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        target_value: jsii.Number,
        custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric] = None,
        predefined_metric: typing.Optional["PredefinedMetric"] = None,
        resource_label: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for a Target Tracking policy that include the metric but exclude the target.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metric.
        :param resource_label: The resource label associated with the predefined metric. Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the format should be: app///targetgroup// Default: - No resource label.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_value": target_value,
        }
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if custom_metric is not None:
            self._values["custom_metric"] = custom_metric
        if predefined_metric is not None:
            self._values["predefined_metric"] = predefined_metric
        if resource_label is not None:
            self._values["resource_label"] = resource_label

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        :default: false
        """
        result = self._values.get("disable_scale_in")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: - Same as the cooldown.
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def target_value(self) -> jsii.Number:
        """The target value for the metric."""
        result = self._values.get("target_value")
        assert result is not None, "Required property 'target_value' is missing"
        return result

    @builtins.property
    def custom_metric(self) -> typing.Optional[aws_cdk.aws_cloudwatch.IMetric]:
        """A custom metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        :default: - No custom metric.
        """
        result = self._values.get("custom_metric")
        return result

    @builtins.property
    def predefined_metric(self) -> typing.Optional["PredefinedMetric"]:
        """A predefined metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        :default: - No predefined metric.
        """
        result = self._values.get("predefined_metric")
        return result

    @builtins.property
    def resource_label(self) -> typing.Optional[builtins.str]:
        """The resource label associated with the predefined metric.

        Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the
        format should be:

        app///targetgroup//

        :default: - No resource label.
        """
        result = self._values.get("resource_label")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicTargetTrackingScalingPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.BlockDevice",
    jsii_struct_bases=[],
    name_mapping={
        "device_name": "deviceName",
        "volume": "volume",
        "mapping_enabled": "mappingEnabled",
    },
)
class BlockDevice:
    def __init__(
        self,
        *,
        device_name: builtins.str,
        volume: "BlockDeviceVolume",
        mapping_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Block device.

        :param device_name: The device name exposed to the EC2 instance.
        :param volume: Defines the block device volume, to be either an Amazon EBS volume or an ephemeral instance store volume.
        :param mapping_enabled: (deprecated) If false, the device mapping will be suppressed. If set to false for the root device, the instance might fail the Amazon EC2 health check. Amazon EC2 Auto Scaling launches a replacement instance if the instance fails the health check. Default: true - device mapping is left untouched
        """
        self._values: typing.Dict[str, typing.Any] = {
            "device_name": device_name,
            "volume": volume,
        }
        if mapping_enabled is not None:
            self._values["mapping_enabled"] = mapping_enabled

    @builtins.property
    def device_name(self) -> builtins.str:
        """The device name exposed to the EC2 instance.

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "/dev/sdh" , "xvdh"
        """
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return result

    @builtins.property
    def volume(self) -> "BlockDeviceVolume":
        """Defines the block device volume, to be either an Amazon EBS volume or an ephemeral instance store volume.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            BlockDeviceVolume.ebs(15) , BlockDeviceVolume.ephemeral(0)
        """
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return result

    @builtins.property
    def mapping_enabled(self) -> typing.Optional[builtins.bool]:
        """(deprecated) If false, the device mapping will be suppressed.

        If set to false for the root device, the instance might fail the Amazon EC2 health check.
        Amazon EC2 Auto Scaling launches a replacement instance if the instance fails the health check.

        :default: true - device mapping is left untouched

        :deprecated: use ``BlockDeviceVolume.noDevice()`` as the volume to supress a mapping.

        :stability: deprecated
        """
        result = self._values.get("mapping_enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockDevice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockDeviceVolume(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.BlockDeviceVolume",
):
    """Describes a block device mapping for an EC2 instance or Auto Scaling group."""

    def __init__(
        self,
        ebs_device: typing.Optional["EbsDeviceProps"] = None,
        virtual_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param ebs_device: EBS device info.
        :param virtual_name: Virtual device name.
        """
        jsii.create(BlockDeviceVolume, self, [ebs_device, virtual_name])

    @jsii.member(jsii_name="ebs")
    @builtins.classmethod
    def ebs(
        cls,
        volume_size: jsii.Number,
        *,
        encrypted: typing.Optional[builtins.bool] = None,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional["EbsDeviceVolumeType"] = None,
    ) -> "BlockDeviceVolume":
        """Creates a new Elastic Block Storage device.

        :param volume_size: The volume size, in Gibibytes (GiB).
        :param encrypted: Specifies whether the EBS volume is encrypted. Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption Default: false
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume. Default: - none, required for {@link EbsDeviceVolumeType.IO1}
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        """
        options = EbsDeviceOptions(
            encrypted=encrypted,
            delete_on_termination=delete_on_termination,
            iops=iops,
            volume_type=volume_type,
        )

        return jsii.sinvoke(cls, "ebs", [volume_size, options])

    @jsii.member(jsii_name="ebsFromSnapshot")
    @builtins.classmethod
    def ebs_from_snapshot(
        cls,
        snapshot_id: builtins.str,
        *,
        volume_size: typing.Optional[jsii.Number] = None,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional["EbsDeviceVolumeType"] = None,
    ) -> "BlockDeviceVolume":
        """Creates a new Elastic Block Storage device from an existing snapshot.

        :param snapshot_id: The snapshot ID of the volume to use.
        :param volume_size: The volume size, in Gibibytes (GiB). If you specify volumeSize, it must be equal or greater than the size of the snapshot. Default: - The snapshot size
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume. Default: - none, required for {@link EbsDeviceVolumeType.IO1}
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        """
        options = EbsDeviceSnapshotOptions(
            volume_size=volume_size,
            delete_on_termination=delete_on_termination,
            iops=iops,
            volume_type=volume_type,
        )

        return jsii.sinvoke(cls, "ebsFromSnapshot", [snapshot_id, options])

    @jsii.member(jsii_name="ephemeral")
    @builtins.classmethod
    def ephemeral(cls, volume_index: jsii.Number) -> "BlockDeviceVolume":
        """Creates a virtual, ephemeral device.

        The name will be in the form ephemeral{volumeIndex}.

        :param volume_index: the volume index. Must be equal or greater than 0
        """
        return jsii.sinvoke(cls, "ephemeral", [volume_index])

    @jsii.member(jsii_name="noDevice")
    @builtins.classmethod
    def no_device(cls) -> "BlockDeviceVolume":
        """Supresses a volume mapping."""
        return jsii.sinvoke(cls, "noDevice", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ebsDevice")
    def ebs_device(self) -> typing.Optional["EbsDeviceProps"]:
        """EBS device info."""
        return jsii.get(self, "ebsDevice")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="virtualName")
    def virtual_name(self) -> typing.Optional[builtins.str]:
        """Virtual device name."""
        return jsii.get(self, "virtualName")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAutoScalingGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup",
):
    """A CloudFormation ``AWS::AutoScaling::AutoScalingGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
    :cloudformationResource: AWS::AutoScaling::AutoScalingGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        max_size: builtins.str,
        min_size: builtins.str,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        capacity_rebalance: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        cooldown: typing.Optional[builtins.str] = None,
        desired_capacity: typing.Optional[builtins.str] = None,
        health_check_grace_period: typing.Optional[jsii.Number] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        launch_configuration_name: typing.Optional[builtins.str] = None,
        launch_template: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]] = None,
        lifecycle_hook_specification_list: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LifecycleHookSpecificationProperty"]]]] = None,
        load_balancer_names: typing.Optional[typing.List[builtins.str]] = None,
        max_instance_lifetime: typing.Optional[jsii.Number] = None,
        metrics_collection: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MetricsCollectionProperty"]]]] = None,
        mixed_instances_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MixedInstancesPolicyProperty"]] = None,
        new_instances_protected_from_scale_in: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        notification_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.NotificationConfigurationProperty"]]]] = None,
        placement_group: typing.Optional[builtins.str] = None,
        service_linked_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List["CfnAutoScalingGroup.TagPropertyProperty"]] = None,
        target_group_arns: typing.Optional[typing.List[builtins.str]] = None,
        termination_policies: typing.Optional[typing.List[builtins.str]] = None,
        vpc_zone_identifier: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::AutoScaling::AutoScalingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param max_size: ``AWS::AutoScaling::AutoScalingGroup.MaxSize``.
        :param min_size: ``AWS::AutoScaling::AutoScalingGroup.MinSize``.
        :param auto_scaling_group_name: ``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.
        :param availability_zones: ``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.
        :param capacity_rebalance: ``AWS::AutoScaling::AutoScalingGroup.CapacityRebalance``.
        :param cooldown: ``AWS::AutoScaling::AutoScalingGroup.Cooldown``.
        :param desired_capacity: ``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.
        :param health_check_grace_period: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.
        :param health_check_type: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.
        :param instance_id: ``AWS::AutoScaling::AutoScalingGroup.InstanceId``.
        :param launch_configuration_name: ``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.
        :param launch_template: ``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.
        :param lifecycle_hook_specification_list: ``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.
        :param load_balancer_names: ``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.
        :param max_instance_lifetime: ``AWS::AutoScaling::AutoScalingGroup.MaxInstanceLifetime``.
        :param metrics_collection: ``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.
        :param mixed_instances_policy: ``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.
        :param new_instances_protected_from_scale_in: ``AWS::AutoScaling::AutoScalingGroup.NewInstancesProtectedFromScaleIn``.
        :param notification_configurations: ``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.
        :param placement_group: ``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.
        :param service_linked_role_arn: ``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.
        :param tags: ``AWS::AutoScaling::AutoScalingGroup.Tags``.
        :param target_group_arns: ``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.
        :param termination_policies: ``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.
        :param vpc_zone_identifier: ``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.
        """
        props = CfnAutoScalingGroupProps(
            max_size=max_size,
            min_size=min_size,
            auto_scaling_group_name=auto_scaling_group_name,
            availability_zones=availability_zones,
            capacity_rebalance=capacity_rebalance,
            cooldown=cooldown,
            desired_capacity=desired_capacity,
            health_check_grace_period=health_check_grace_period,
            health_check_type=health_check_type,
            instance_id=instance_id,
            launch_configuration_name=launch_configuration_name,
            launch_template=launch_template,
            lifecycle_hook_specification_list=lifecycle_hook_specification_list,
            load_balancer_names=load_balancer_names,
            max_instance_lifetime=max_instance_lifetime,
            metrics_collection=metrics_collection,
            mixed_instances_policy=mixed_instances_policy,
            new_instances_protected_from_scale_in=new_instances_protected_from_scale_in,
            notification_configurations=notification_configurations,
            placement_group=placement_group,
            service_linked_role_arn=service_linked_role_arn,
            tags=tags,
            target_group_arns=target_group_arns,
            termination_policies=termination_policies,
            vpc_zone_identifier=vpc_zone_identifier,
        )

        jsii.create(CfnAutoScalingGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::AutoScaling::AutoScalingGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> builtins.str:
        """``AWS::AutoScaling::AutoScalingGroup.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-maxsize
        """
        return jsii.get(self, "maxSize")

    @max_size.setter # type: ignore
    def max_size(self, value: builtins.str) -> None:
        jsii.set(self, "maxSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> builtins.str:
        """``AWS::AutoScaling::AutoScalingGroup.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-minsize
        """
        return jsii.get(self, "minSize")

    @min_size.setter # type: ignore
    def min_size(self, value: builtins.str) -> None:
        jsii.set(self, "minSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-autoscalinggroupname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter # type: ignore
    def auto_scaling_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "autoScalingGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter # type: ignore
    def availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "availabilityZones", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="capacityRebalance")
    def capacity_rebalance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::AutoScalingGroup.CapacityRebalance``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-capacityrebalance
        """
        return jsii.get(self, "capacityRebalance")

    @capacity_rebalance.setter # type: ignore
    def capacity_rebalance(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "capacityRebalance", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cooldown")
    def cooldown(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.Cooldown``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-cooldown
        """
        return jsii.get(self, "cooldown")

    @cooldown.setter # type: ignore
    def cooldown(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cooldown", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="desiredCapacity")
    def desired_capacity(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        """
        return jsii.get(self, "desiredCapacity")

    @desired_capacity.setter # type: ignore
    def desired_capacity(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "desiredCapacity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckGracePeriod")
    def health_check_grace_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthcheckgraceperiod
        """
        return jsii.get(self, "healthCheckGracePeriod")

    @health_check_grace_period.setter # type: ignore
    def health_check_grace_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckGracePeriod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckType")
    def health_check_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthchecktype
        """
        return jsii.get(self, "healthCheckType")

    @health_check_type.setter # type: ignore
    def health_check_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.InstanceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-instanceid
        """
        return jsii.get(self, "instanceId")

    @instance_id.setter # type: ignore
    def instance_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "instanceId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="launchConfigurationName")
    def launch_configuration_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchconfigurationname
        """
        return jsii.get(self, "launchConfigurationName")

    @launch_configuration_name.setter # type: ignore
    def launch_configuration_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "launchConfigurationName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchtemplate
        """
        return jsii.get(self, "launchTemplate")

    @launch_template.setter # type: ignore
    def launch_template(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]],
    ) -> None:
        jsii.set(self, "launchTemplate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lifecycleHookSpecificationList")
    def lifecycle_hook_specification_list(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LifecycleHookSpecificationProperty"]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecificationlist
        """
        return jsii.get(self, "lifecycleHookSpecificationList")

    @lifecycle_hook_specification_list.setter # type: ignore
    def lifecycle_hook_specification_list(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LifecycleHookSpecificationProperty"]]]],
    ) -> None:
        jsii.set(self, "lifecycleHookSpecificationList", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerNames")
    def load_balancer_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-loadbalancernames
        """
        return jsii.get(self, "loadBalancerNames")

    @load_balancer_names.setter # type: ignore
    def load_balancer_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "loadBalancerNames", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxInstanceLifetime")
    def max_instance_lifetime(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::AutoScalingGroup.MaxInstanceLifetime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-maxinstancelifetime
        """
        return jsii.get(self, "maxInstanceLifetime")

    @max_instance_lifetime.setter # type: ignore
    def max_instance_lifetime(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxInstanceLifetime", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metricsCollection")
    def metrics_collection(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MetricsCollectionProperty"]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-metricscollection
        """
        return jsii.get(self, "metricsCollection")

    @metrics_collection.setter # type: ignore
    def metrics_collection(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MetricsCollectionProperty"]]]],
    ) -> None:
        jsii.set(self, "metricsCollection", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mixedInstancesPolicy")
    def mixed_instances_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MixedInstancesPolicyProperty"]]:
        """``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-mixedinstancespolicy
        """
        return jsii.get(self, "mixedInstancesPolicy")

    @mixed_instances_policy.setter # type: ignore
    def mixed_instances_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MixedInstancesPolicyProperty"]],
    ) -> None:
        jsii.set(self, "mixedInstancesPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="newInstancesProtectedFromScaleIn")
    def new_instances_protected_from_scale_in(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::AutoScalingGroup.NewInstancesProtectedFromScaleIn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-newinstancesprotectedfromscalein
        """
        return jsii.get(self, "newInstancesProtectedFromScaleIn")

    @new_instances_protected_from_scale_in.setter # type: ignore
    def new_instances_protected_from_scale_in(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "newInstancesProtectedFromScaleIn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="notificationConfigurations")
    def notification_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.NotificationConfigurationProperty"]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        """
        return jsii.get(self, "notificationConfigurations")

    @notification_configurations.setter # type: ignore
    def notification_configurations(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.NotificationConfigurationProperty"]]]],
    ) -> None:
        jsii.set(self, "notificationConfigurations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="placementGroup")
    def placement_group(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-placementgroup
        """
        return jsii.get(self, "placementGroup")

    @placement_group.setter # type: ignore
    def placement_group(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "placementGroup", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceLinkedRoleArn")
    def service_linked_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-servicelinkedrolearn
        """
        return jsii.get(self, "serviceLinkedRoleArn")

    @service_linked_role_arn.setter # type: ignore
    def service_linked_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "serviceLinkedRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupArns")
    def target_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-targetgrouparns
        """
        return jsii.get(self, "targetGroupArns")

    @target_group_arns.setter # type: ignore
    def target_group_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "targetGroupArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="terminationPolicies")
    def termination_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-termpolicy
        """
        return jsii.get(self, "terminationPolicies")

    @termination_policies.setter # type: ignore
    def termination_policies(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "terminationPolicies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcZoneIdentifier")
    def vpc_zone_identifier(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-vpczoneidentifier
        """
        return jsii.get(self, "vpcZoneIdentifier")

    @vpc_zone_identifier.setter # type: ignore
    def vpc_zone_identifier(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "vpcZoneIdentifier", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.InstancesDistributionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_demand_allocation_strategy": "onDemandAllocationStrategy",
            "on_demand_base_capacity": "onDemandBaseCapacity",
            "on_demand_percentage_above_base_capacity": "onDemandPercentageAboveBaseCapacity",
            "spot_allocation_strategy": "spotAllocationStrategy",
            "spot_instance_pools": "spotInstancePools",
            "spot_max_price": "spotMaxPrice",
        },
    )
    class InstancesDistributionProperty:
        def __init__(
            self,
            *,
            on_demand_allocation_strategy: typing.Optional[builtins.str] = None,
            on_demand_base_capacity: typing.Optional[jsii.Number] = None,
            on_demand_percentage_above_base_capacity: typing.Optional[jsii.Number] = None,
            spot_allocation_strategy: typing.Optional[builtins.str] = None,
            spot_instance_pools: typing.Optional[jsii.Number] = None,
            spot_max_price: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param on_demand_allocation_strategy: ``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandAllocationStrategy``.
            :param on_demand_base_capacity: ``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandBaseCapacity``.
            :param on_demand_percentage_above_base_capacity: ``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandPercentageAboveBaseCapacity``.
            :param spot_allocation_strategy: ``CfnAutoScalingGroup.InstancesDistributionProperty.SpotAllocationStrategy``.
            :param spot_instance_pools: ``CfnAutoScalingGroup.InstancesDistributionProperty.SpotInstancePools``.
            :param spot_max_price: ``CfnAutoScalingGroup.InstancesDistributionProperty.SpotMaxPrice``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if on_demand_allocation_strategy is not None:
                self._values["on_demand_allocation_strategy"] = on_demand_allocation_strategy
            if on_demand_base_capacity is not None:
                self._values["on_demand_base_capacity"] = on_demand_base_capacity
            if on_demand_percentage_above_base_capacity is not None:
                self._values["on_demand_percentage_above_base_capacity"] = on_demand_percentage_above_base_capacity
            if spot_allocation_strategy is not None:
                self._values["spot_allocation_strategy"] = spot_allocation_strategy
            if spot_instance_pools is not None:
                self._values["spot_instance_pools"] = spot_instance_pools
            if spot_max_price is not None:
                self._values["spot_max_price"] = spot_max_price

        @builtins.property
        def on_demand_allocation_strategy(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandAllocationStrategy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandallocationstrategy
            """
            result = self._values.get("on_demand_allocation_strategy")
            return result

        @builtins.property
        def on_demand_base_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandBaseCapacity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandbasecapacity
            """
            result = self._values.get("on_demand_base_capacity")
            return result

        @builtins.property
        def on_demand_percentage_above_base_capacity(
            self,
        ) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandPercentageAboveBaseCapacity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandpercentageabovebasecapacity
            """
            result = self._values.get("on_demand_percentage_above_base_capacity")
            return result

        @builtins.property
        def spot_allocation_strategy(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotAllocationStrategy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotallocationstrategy
            """
            result = self._values.get("spot_allocation_strategy")
            return result

        @builtins.property
        def spot_instance_pools(self) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotInstancePools``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotinstancepools
            """
            result = self._values.get("spot_instance_pools")
            return result

        @builtins.property
        def spot_max_price(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotMaxPrice``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotmaxprice
            """
            result = self._values.get("spot_max_price")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstancesDistributionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_type": "instanceType",
            "launch_template_specification": "launchTemplateSpecification",
            "weighted_capacity": "weightedCapacity",
        },
    )
    class LaunchTemplateOverridesProperty:
        def __init__(
            self,
            *,
            instance_type: typing.Optional[builtins.str] = None,
            launch_template_specification: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]] = None,
            weighted_capacity: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param instance_type: ``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.InstanceType``.
            :param launch_template_specification: ``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.LaunchTemplateSpecification``.
            :param weighted_capacity: ``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.WeightedCapacity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if launch_template_specification is not None:
                self._values["launch_template_specification"] = launch_template_specification
            if weighted_capacity is not None:
                self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.InstanceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-instancetype
            """
            result = self._values.get("instance_type")
            return result

        @builtins.property
        def launch_template_specification(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]]:
            """``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.LaunchTemplateSpecification``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-launchtemplatespecification
            """
            result = self._values.get("launch_template_specification")
            return result

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.WeightedCapacity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-weightedcapacity
            """
            result = self._values.get("weighted_capacity")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_specification": "launchTemplateSpecification",
            "overrides": "overrides",
        },
    )
    class LaunchTemplateProperty:
        def __init__(
            self,
            *,
            launch_template_specification: typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"],
            overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateOverridesProperty"]]]] = None,
        ) -> None:
            """
            :param launch_template_specification: ``CfnAutoScalingGroup.LaunchTemplateProperty.LaunchTemplateSpecification``.
            :param overrides: ``CfnAutoScalingGroup.LaunchTemplateProperty.Overrides``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "launch_template_specification": launch_template_specification,
            }
            if overrides is not None:
                self._values["overrides"] = overrides

        @builtins.property
        def launch_template_specification(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]:
            """``CfnAutoScalingGroup.LaunchTemplateProperty.LaunchTemplateSpecification``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html#cfn-as-group-launchtemplate
            """
            result = self._values.get("launch_template_specification")
            assert result is not None, "Required property 'launch_template_specification' is missing"
            return result

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateOverridesProperty"]]]]:
            """``CfnAutoScalingGroup.LaunchTemplateProperty.Overrides``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html#cfn-as-mixedinstancespolicy-overrides
            """
            result = self._values.get("overrides")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "version": "version",
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
        },
    )
    class LaunchTemplateSpecificationProperty:
        def __init__(
            self,
            *,
            version: builtins.str,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param version: ``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.Version``.
            :param launch_template_id: ``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateId``.
            :param launch_template_name: ``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "version": version,
            }
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name

        @builtins.property
        def version(self) -> builtins.str:
            """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-version
            """
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return result

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplateid
            """
            result = self._values.get("launch_template_id")
            return result

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplatename
            """
            result = self._values.get("launch_template_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LifecycleHookSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lifecycle_hook_name": "lifecycleHookName",
            "lifecycle_transition": "lifecycleTransition",
            "default_result": "defaultResult",
            "heartbeat_timeout": "heartbeatTimeout",
            "notification_metadata": "notificationMetadata",
            "notification_target_arn": "notificationTargetArn",
            "role_arn": "roleArn",
        },
    )
    class LifecycleHookSpecificationProperty:
        def __init__(
            self,
            *,
            lifecycle_hook_name: builtins.str,
            lifecycle_transition: builtins.str,
            default_result: typing.Optional[builtins.str] = None,
            heartbeat_timeout: typing.Optional[jsii.Number] = None,
            notification_metadata: typing.Optional[builtins.str] = None,
            notification_target_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param lifecycle_hook_name: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleHookName``.
            :param lifecycle_transition: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleTransition``.
            :param default_result: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.DefaultResult``.
            :param heartbeat_timeout: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.HeartbeatTimeout``.
            :param notification_metadata: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationMetadata``.
            :param notification_target_arn: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationTargetARN``.
            :param role_arn: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "lifecycle_hook_name": lifecycle_hook_name,
                "lifecycle_transition": lifecycle_transition,
            }
            if default_result is not None:
                self._values["default_result"] = default_result
            if heartbeat_timeout is not None:
                self._values["heartbeat_timeout"] = heartbeat_timeout
            if notification_metadata is not None:
                self._values["notification_metadata"] = notification_metadata
            if notification_target_arn is not None:
                self._values["notification_target_arn"] = notification_target_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def lifecycle_hook_name(self) -> builtins.str:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleHookName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecyclehookname
            """
            result = self._values.get("lifecycle_hook_name")
            assert result is not None, "Required property 'lifecycle_hook_name' is missing"
            return result

        @builtins.property
        def lifecycle_transition(self) -> builtins.str:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleTransition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecycletransition
            """
            result = self._values.get("lifecycle_transition")
            assert result is not None, "Required property 'lifecycle_transition' is missing"
            return result

        @builtins.property
        def default_result(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.DefaultResult``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-defaultresult
            """
            result = self._values.get("default_result")
            return result

        @builtins.property
        def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.HeartbeatTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-heartbeattimeout
            """
            result = self._values.get("heartbeat_timeout")
            return result

        @builtins.property
        def notification_metadata(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationMetadata``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationmetadata
            """
            result = self._values.get("notification_metadata")
            return result

        @builtins.property
        def notification_target_arn(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationTargetARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationtargetarn
            """
            result = self._values.get("notification_target_arn")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-rolearn
            """
            result = self._values.get("role_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleHookSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MetricsCollectionProperty",
        jsii_struct_bases=[],
        name_mapping={"granularity": "granularity", "metrics": "metrics"},
    )
    class MetricsCollectionProperty:
        def __init__(
            self,
            *,
            granularity: builtins.str,
            metrics: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param granularity: ``CfnAutoScalingGroup.MetricsCollectionProperty.Granularity``.
            :param metrics: ``CfnAutoScalingGroup.MetricsCollectionProperty.Metrics``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "granularity": granularity,
            }
            if metrics is not None:
                self._values["metrics"] = metrics

        @builtins.property
        def granularity(self) -> builtins.str:
            """``CfnAutoScalingGroup.MetricsCollectionProperty.Granularity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html#cfn-as-metricscollection-granularity
            """
            result = self._values.get("granularity")
            assert result is not None, "Required property 'granularity' is missing"
            return result

        @builtins.property
        def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnAutoScalingGroup.MetricsCollectionProperty.Metrics``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html#cfn-as-metricscollection-metrics
            """
            result = self._values.get("metrics")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsCollectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MixedInstancesPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template": "launchTemplate",
            "instances_distribution": "instancesDistribution",
        },
    )
    class MixedInstancesPolicyProperty:
        def __init__(
            self,
            *,
            launch_template: typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateProperty"],
            instances_distribution: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.InstancesDistributionProperty"]] = None,
        ) -> None:
            """
            :param launch_template: ``CfnAutoScalingGroup.MixedInstancesPolicyProperty.LaunchTemplate``.
            :param instances_distribution: ``CfnAutoScalingGroup.MixedInstancesPolicyProperty.InstancesDistribution``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "launch_template": launch_template,
            }
            if instances_distribution is not None:
                self._values["instances_distribution"] = instances_distribution

        @builtins.property
        def launch_template(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateProperty"]:
            """``CfnAutoScalingGroup.MixedInstancesPolicyProperty.LaunchTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html#cfn-as-mixedinstancespolicy-launchtemplate
            """
            result = self._values.get("launch_template")
            assert result is not None, "Required property 'launch_template' is missing"
            return result

        @builtins.property
        def instances_distribution(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.InstancesDistributionProperty"]]:
            """``CfnAutoScalingGroup.MixedInstancesPolicyProperty.InstancesDistribution``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html#cfn-as-mixedinstancespolicy-instancesdistribution
            """
            result = self._values.get("instances_distribution")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MixedInstancesPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "topic_arn": "topicArn",
            "notification_types": "notificationTypes",
        },
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            topic_arn: builtins.str,
            notification_types: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param topic_arn: ``CfnAutoScalingGroup.NotificationConfigurationProperty.TopicARN``.
            :param notification_types: ``CfnAutoScalingGroup.NotificationConfigurationProperty.NotificationTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "topic_arn": topic_arn,
            }
            if notification_types is not None:
                self._values["notification_types"] = notification_types

        @builtins.property
        def topic_arn(self) -> builtins.str:
            """``CfnAutoScalingGroup.NotificationConfigurationProperty.TopicARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html#cfn-autoscaling-autoscalinggroup-notificationconfigurations-topicarn
            """
            result = self._values.get("topic_arn")
            assert result is not None, "Required property 'topic_arn' is missing"
            return result

        @builtins.property
        def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnAutoScalingGroup.NotificationConfigurationProperty.NotificationTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html#cfn-as-group-notificationconfigurations-notificationtypes
            """
            result = self._values.get("notification_types")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.TagPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "propagate_at_launch": "propagateAtLaunch",
            "value": "value",
        },
    )
    class TagPropertyProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            propagate_at_launch: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            value: builtins.str,
        ) -> None:
            """
            :param key: ``CfnAutoScalingGroup.TagPropertyProperty.Key``.
            :param propagate_at_launch: ``CfnAutoScalingGroup.TagPropertyProperty.PropagateAtLaunch``.
            :param value: ``CfnAutoScalingGroup.TagPropertyProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "propagate_at_launch": propagate_at_launch,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnAutoScalingGroup.TagPropertyProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-Key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def propagate_at_launch(
            self,
        ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnAutoScalingGroup.TagPropertyProperty.PropagateAtLaunch``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-PropagateAtLaunch
            """
            result = self._values.get("propagate_at_launch")
            assert result is not None, "Required property 'propagate_at_launch' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnAutoScalingGroup.TagPropertyProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-Value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_size": "maxSize",
        "min_size": "minSize",
        "auto_scaling_group_name": "autoScalingGroupName",
        "availability_zones": "availabilityZones",
        "capacity_rebalance": "capacityRebalance",
        "cooldown": "cooldown",
        "desired_capacity": "desiredCapacity",
        "health_check_grace_period": "healthCheckGracePeriod",
        "health_check_type": "healthCheckType",
        "instance_id": "instanceId",
        "launch_configuration_name": "launchConfigurationName",
        "launch_template": "launchTemplate",
        "lifecycle_hook_specification_list": "lifecycleHookSpecificationList",
        "load_balancer_names": "loadBalancerNames",
        "max_instance_lifetime": "maxInstanceLifetime",
        "metrics_collection": "metricsCollection",
        "mixed_instances_policy": "mixedInstancesPolicy",
        "new_instances_protected_from_scale_in": "newInstancesProtectedFromScaleIn",
        "notification_configurations": "notificationConfigurations",
        "placement_group": "placementGroup",
        "service_linked_role_arn": "serviceLinkedRoleArn",
        "tags": "tags",
        "target_group_arns": "targetGroupArns",
        "termination_policies": "terminationPolicies",
        "vpc_zone_identifier": "vpcZoneIdentifier",
    },
)
class CfnAutoScalingGroupProps:
    def __init__(
        self,
        *,
        max_size: builtins.str,
        min_size: builtins.str,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        capacity_rebalance: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        cooldown: typing.Optional[builtins.str] = None,
        desired_capacity: typing.Optional[builtins.str] = None,
        health_check_grace_period: typing.Optional[jsii.Number] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        launch_configuration_name: typing.Optional[builtins.str] = None,
        launch_template: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.LaunchTemplateSpecificationProperty]] = None,
        lifecycle_hook_specification_list: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.LifecycleHookSpecificationProperty]]]] = None,
        load_balancer_names: typing.Optional[typing.List[builtins.str]] = None,
        max_instance_lifetime: typing.Optional[jsii.Number] = None,
        metrics_collection: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.MetricsCollectionProperty]]]] = None,
        mixed_instances_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.MixedInstancesPolicyProperty]] = None,
        new_instances_protected_from_scale_in: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        notification_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.NotificationConfigurationProperty]]]] = None,
        placement_group: typing.Optional[builtins.str] = None,
        service_linked_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[CfnAutoScalingGroup.TagPropertyProperty]] = None,
        target_group_arns: typing.Optional[typing.List[builtins.str]] = None,
        termination_policies: typing.Optional[typing.List[builtins.str]] = None,
        vpc_zone_identifier: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AutoScaling::AutoScalingGroup``.

        :param max_size: ``AWS::AutoScaling::AutoScalingGroup.MaxSize``.
        :param min_size: ``AWS::AutoScaling::AutoScalingGroup.MinSize``.
        :param auto_scaling_group_name: ``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.
        :param availability_zones: ``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.
        :param capacity_rebalance: ``AWS::AutoScaling::AutoScalingGroup.CapacityRebalance``.
        :param cooldown: ``AWS::AutoScaling::AutoScalingGroup.Cooldown``.
        :param desired_capacity: ``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.
        :param health_check_grace_period: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.
        :param health_check_type: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.
        :param instance_id: ``AWS::AutoScaling::AutoScalingGroup.InstanceId``.
        :param launch_configuration_name: ``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.
        :param launch_template: ``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.
        :param lifecycle_hook_specification_list: ``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.
        :param load_balancer_names: ``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.
        :param max_instance_lifetime: ``AWS::AutoScaling::AutoScalingGroup.MaxInstanceLifetime``.
        :param metrics_collection: ``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.
        :param mixed_instances_policy: ``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.
        :param new_instances_protected_from_scale_in: ``AWS::AutoScaling::AutoScalingGroup.NewInstancesProtectedFromScaleIn``.
        :param notification_configurations: ``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.
        :param placement_group: ``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.
        :param service_linked_role_arn: ``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.
        :param tags: ``AWS::AutoScaling::AutoScalingGroup.Tags``.
        :param target_group_arns: ``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.
        :param termination_policies: ``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.
        :param vpc_zone_identifier: ``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "max_size": max_size,
            "min_size": min_size,
        }
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if capacity_rebalance is not None:
            self._values["capacity_rebalance"] = capacity_rebalance
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if health_check_type is not None:
            self._values["health_check_type"] = health_check_type
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if launch_configuration_name is not None:
            self._values["launch_configuration_name"] = launch_configuration_name
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if lifecycle_hook_specification_list is not None:
            self._values["lifecycle_hook_specification_list"] = lifecycle_hook_specification_list
        if load_balancer_names is not None:
            self._values["load_balancer_names"] = load_balancer_names
        if max_instance_lifetime is not None:
            self._values["max_instance_lifetime"] = max_instance_lifetime
        if metrics_collection is not None:
            self._values["metrics_collection"] = metrics_collection
        if mixed_instances_policy is not None:
            self._values["mixed_instances_policy"] = mixed_instances_policy
        if new_instances_protected_from_scale_in is not None:
            self._values["new_instances_protected_from_scale_in"] = new_instances_protected_from_scale_in
        if notification_configurations is not None:
            self._values["notification_configurations"] = notification_configurations
        if placement_group is not None:
            self._values["placement_group"] = placement_group
        if service_linked_role_arn is not None:
            self._values["service_linked_role_arn"] = service_linked_role_arn
        if tags is not None:
            self._values["tags"] = tags
        if target_group_arns is not None:
            self._values["target_group_arns"] = target_group_arns
        if termination_policies is not None:
            self._values["termination_policies"] = termination_policies
        if vpc_zone_identifier is not None:
            self._values["vpc_zone_identifier"] = vpc_zone_identifier

    @builtins.property
    def max_size(self) -> builtins.str:
        """``AWS::AutoScaling::AutoScalingGroup.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-maxsize
        """
        result = self._values.get("max_size")
        assert result is not None, "Required property 'max_size' is missing"
        return result

    @builtins.property
    def min_size(self) -> builtins.str:
        """``AWS::AutoScaling::AutoScalingGroup.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-minsize
        """
        result = self._values.get("min_size")
        assert result is not None, "Required property 'min_size' is missing"
        return result

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-autoscalinggroupname
        """
        result = self._values.get("auto_scaling_group_name")
        return result

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-availabilityzones
        """
        result = self._values.get("availability_zones")
        return result

    @builtins.property
    def capacity_rebalance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::AutoScalingGroup.CapacityRebalance``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-capacityrebalance
        """
        result = self._values.get("capacity_rebalance")
        return result

    @builtins.property
    def cooldown(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.Cooldown``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-cooldown
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def desired_capacity(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthcheckgraceperiod
        """
        result = self._values.get("health_check_grace_period")
        return result

    @builtins.property
    def health_check_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthchecktype
        """
        result = self._values.get("health_check_type")
        return result

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.InstanceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-instanceid
        """
        result = self._values.get("instance_id")
        return result

    @builtins.property
    def launch_configuration_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchconfigurationname
        """
        result = self._values.get("launch_configuration_name")
        return result

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.LaunchTemplateSpecificationProperty]]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchtemplate
        """
        result = self._values.get("launch_template")
        return result

    @builtins.property
    def lifecycle_hook_specification_list(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.LifecycleHookSpecificationProperty]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecificationlist
        """
        result = self._values.get("lifecycle_hook_specification_list")
        return result

    @builtins.property
    def load_balancer_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-loadbalancernames
        """
        result = self._values.get("load_balancer_names")
        return result

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::AutoScalingGroup.MaxInstanceLifetime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-maxinstancelifetime
        """
        result = self._values.get("max_instance_lifetime")
        return result

    @builtins.property
    def metrics_collection(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.MetricsCollectionProperty]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-metricscollection
        """
        result = self._values.get("metrics_collection")
        return result

    @builtins.property
    def mixed_instances_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.MixedInstancesPolicyProperty]]:
        """``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-mixedinstancespolicy
        """
        result = self._values.get("mixed_instances_policy")
        return result

    @builtins.property
    def new_instances_protected_from_scale_in(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::AutoScalingGroup.NewInstancesProtectedFromScaleIn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-newinstancesprotectedfromscalein
        """
        result = self._values.get("new_instances_protected_from_scale_in")
        return result

    @builtins.property
    def notification_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAutoScalingGroup.NotificationConfigurationProperty]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        """
        result = self._values.get("notification_configurations")
        return result

    @builtins.property
    def placement_group(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-placementgroup
        """
        result = self._values.get("placement_group")
        return result

    @builtins.property
    def service_linked_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-servicelinkedrolearn
        """
        result = self._values.get("service_linked_role_arn")
        return result

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List[CfnAutoScalingGroup.TagPropertyProperty]]:
        """``AWS::AutoScaling::AutoScalingGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def target_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-targetgrouparns
        """
        result = self._values.get("target_group_arns")
        return result

    @builtins.property
    def termination_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-termpolicy
        """
        result = self._values.get("termination_policies")
        return result

    @builtins.property
    def vpc_zone_identifier(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-vpczoneidentifier
        """
        result = self._values.get("vpc_zone_identifier")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAutoScalingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLaunchConfiguration(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration",
):
    """A CloudFormation ``AWS::AutoScaling::LaunchConfiguration``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
    :cloudformationResource: AWS::AutoScaling::LaunchConfiguration
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        image_id: builtins.str,
        instance_type: builtins.str,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        block_device_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.BlockDeviceMappingProperty"]]]] = None,
        classic_link_vpc_id: typing.Optional[builtins.str] = None,
        classic_link_vpc_security_groups: typing.Optional[typing.List[builtins.str]] = None,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        iam_instance_profile: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_monitoring: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        kernel_id: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        launch_configuration_name: typing.Optional[builtins.str] = None,
        metadata_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.MetadataOptionProperty"]] = None,
        placement_tenancy: typing.Optional[builtins.str] = None,
        ram_disk_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        spot_price: typing.Optional[builtins.str] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::AutoScaling::LaunchConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param image_id: ``AWS::AutoScaling::LaunchConfiguration.ImageId``.
        :param instance_type: ``AWS::AutoScaling::LaunchConfiguration.InstanceType``.
        :param associate_public_ip_address: ``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.
        :param block_device_mappings: ``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.
        :param classic_link_vpc_id: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.
        :param classic_link_vpc_security_groups: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.
        :param ebs_optimized: ``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.
        :param iam_instance_profile: ``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.
        :param instance_id: ``AWS::AutoScaling::LaunchConfiguration.InstanceId``.
        :param instance_monitoring: ``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.
        :param kernel_id: ``AWS::AutoScaling::LaunchConfiguration.KernelId``.
        :param key_name: ``AWS::AutoScaling::LaunchConfiguration.KeyName``.
        :param launch_configuration_name: ``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.
        :param metadata_options: ``AWS::AutoScaling::LaunchConfiguration.MetadataOptions``.
        :param placement_tenancy: ``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.
        :param ram_disk_id: ``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.
        :param security_groups: ``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.
        :param spot_price: ``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.
        :param user_data: ``AWS::AutoScaling::LaunchConfiguration.UserData``.
        """
        props = CfnLaunchConfigurationProps(
            image_id=image_id,
            instance_type=instance_type,
            associate_public_ip_address=associate_public_ip_address,
            block_device_mappings=block_device_mappings,
            classic_link_vpc_id=classic_link_vpc_id,
            classic_link_vpc_security_groups=classic_link_vpc_security_groups,
            ebs_optimized=ebs_optimized,
            iam_instance_profile=iam_instance_profile,
            instance_id=instance_id,
            instance_monitoring=instance_monitoring,
            kernel_id=kernel_id,
            key_name=key_name,
            launch_configuration_name=launch_configuration_name,
            metadata_options=metadata_options,
            placement_tenancy=placement_tenancy,
            ram_disk_id=ram_disk_id,
            security_groups=security_groups,
            spot_price=spot_price,
            user_data=user_data,
        )

        jsii.create(CfnLaunchConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        """``AWS::AutoScaling::LaunchConfiguration.ImageId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-imageid
        """
        return jsii.get(self, "imageId")

    @image_id.setter # type: ignore
    def image_id(self, value: builtins.str) -> None:
        jsii.set(self, "imageId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancetype
        """
        return jsii.get(self, "instanceType")

    @instance_type.setter # type: ignore
    def instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "instanceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="associatePublicIpAddress")
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cf-as-launchconfig-associatepubip
        """
        return jsii.get(self, "associatePublicIpAddress")

    @associate_public_ip_address.setter # type: ignore
    def associate_public_ip_address(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "associatePublicIpAddress", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="blockDeviceMappings")
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.BlockDeviceMappingProperty"]]]]:
        """``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-blockdevicemappings
        """
        return jsii.get(self, "blockDeviceMappings")

    @block_device_mappings.setter # type: ignore
    def block_device_mappings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.BlockDeviceMappingProperty"]]]],
    ) -> None:
        jsii.set(self, "blockDeviceMappings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="classicLinkVpcId")
    def classic_link_vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcid
        """
        return jsii.get(self, "classicLinkVpcId")

    @classic_link_vpc_id.setter # type: ignore
    def classic_link_vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "classicLinkVpcId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="classicLinkVpcSecurityGroups")
    def classic_link_vpc_security_groups(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcsecuritygroups
        """
        return jsii.get(self, "classicLinkVpcSecurityGroups")

    @classic_link_vpc_security_groups.setter # type: ignore
    def classic_link_vpc_security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "classicLinkVpcSecurityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ebsOptimized")
    def ebs_optimized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ebsoptimized
        """
        return jsii.get(self, "ebsOptimized")

    @ebs_optimized.setter # type: ignore
    def ebs_optimized(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "ebsOptimized", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="iamInstanceProfile")
    def iam_instance_profile(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-iaminstanceprofile
        """
        return jsii.get(self, "iamInstanceProfile")

    @iam_instance_profile.setter # type: ignore
    def iam_instance_profile(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "iamInstanceProfile", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instanceid
        """
        return jsii.get(self, "instanceId")

    @instance_id.setter # type: ignore
    def instance_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "instanceId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceMonitoring")
    def instance_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancemonitoring
        """
        return jsii.get(self, "instanceMonitoring")

    @instance_monitoring.setter # type: ignore
    def instance_monitoring(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "instanceMonitoring", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kernelId")
    def kernel_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.KernelId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-kernelid
        """
        return jsii.get(self, "kernelId")

    @kernel_id.setter # type: ignore
    def kernel_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kernelId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.KeyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-keyname
        """
        return jsii.get(self, "keyName")

    @key_name.setter # type: ignore
    def key_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "keyName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="launchConfigurationName")
    def launch_configuration_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-autoscaling-launchconfig-launchconfigurationname
        """
        return jsii.get(self, "launchConfigurationName")

    @launch_configuration_name.setter # type: ignore
    def launch_configuration_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "launchConfigurationName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metadataOptions")
    def metadata_options(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.MetadataOptionProperty"]]:
        """``AWS::AutoScaling::LaunchConfiguration.MetadataOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-autoscaling-launchconfig-metadataoptions
        """
        return jsii.get(self, "metadataOptions")

    @metadata_options.setter # type: ignore
    def metadata_options(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.MetadataOptionProperty"]],
    ) -> None:
        jsii.set(self, "metadataOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="placementTenancy")
    def placement_tenancy(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-placementtenancy
        """
        return jsii.get(self, "placementTenancy")

    @placement_tenancy.setter # type: ignore
    def placement_tenancy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "placementTenancy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ramDiskId")
    def ram_disk_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ramdiskid
        """
        return jsii.get(self, "ramDiskId")

    @ram_disk_id.setter # type: ignore
    def ram_disk_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ramDiskId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter # type: ignore
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="spotPrice")
    def spot_price(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-spotprice
        """
        return jsii.get(self, "spotPrice")

    @spot_price.setter # type: ignore
    def spot_price(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "spotPrice", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userData")
    def user_data(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.UserData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-userdata
        """
        return jsii.get(self, "userData")

    @user_data.setter # type: ignore
    def user_data(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "userData", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_name": "deviceName",
            "ebs": "ebs",
            "no_device": "noDevice",
            "virtual_name": "virtualName",
        },
    )
    class BlockDeviceMappingProperty:
        def __init__(
            self,
            *,
            device_name: builtins.str,
            ebs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.BlockDeviceProperty"]] = None,
            no_device: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            virtual_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param device_name: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.DeviceName``.
            :param ebs: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.Ebs``.
            :param no_device: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.NoDevice``.
            :param virtual_name: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.VirtualName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "device_name": device_name,
            }
            if ebs is not None:
                self._values["ebs"] = ebs
            if no_device is not None:
                self._values["no_device"] = no_device
            if virtual_name is not None:
                self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> builtins.str:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.DeviceName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-devicename
            """
            result = self._values.get("device_name")
            assert result is not None, "Required property 'device_name' is missing"
            return result

        @builtins.property
        def ebs(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.BlockDeviceProperty"]]:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.Ebs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-ebs
            """
            result = self._values.get("ebs")
            return result

        @builtins.property
        def no_device(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.NoDevice``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-nodevice
            """
            result = self._values.get("no_device")
            return result

        @builtins.property
        def virtual_name(self) -> typing.Optional[builtins.str]:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.VirtualName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-virtualname
            """
            result = self._values.get("virtual_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockDeviceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_on_termination": "deleteOnTermination",
            "encrypted": "encrypted",
            "iops": "iops",
            "snapshot_id": "snapshotId",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class BlockDeviceProperty:
        def __init__(
            self,
            *,
            delete_on_termination: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            encrypted: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            snapshot_id: typing.Optional[builtins.str] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param delete_on_termination: ``CfnLaunchConfiguration.BlockDeviceProperty.DeleteOnTermination``.
            :param encrypted: ``CfnLaunchConfiguration.BlockDeviceProperty.Encrypted``.
            :param iops: ``CfnLaunchConfiguration.BlockDeviceProperty.Iops``.
            :param snapshot_id: ``CfnLaunchConfiguration.BlockDeviceProperty.SnapshotId``.
            :param volume_size: ``CfnLaunchConfiguration.BlockDeviceProperty.VolumeSize``.
            :param volume_type: ``CfnLaunchConfiguration.BlockDeviceProperty.VolumeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if delete_on_termination is not None:
                self._values["delete_on_termination"] = delete_on_termination
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if iops is not None:
                self._values["iops"] = iops
            if snapshot_id is not None:
                self._values["snapshot_id"] = snapshot_id
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def delete_on_termination(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.DeleteOnTermination``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-deleteonterm
            """
            result = self._values.get("delete_on_termination")
            return result

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.Encrypted``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-encrypted
            """
            result = self._values.get("encrypted")
            return result

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.Iops``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-iops
            """
            result = self._values.get("iops")
            return result

        @builtins.property
        def snapshot_id(self) -> typing.Optional[builtins.str]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.SnapshotId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-snapshotid
            """
            result = self._values.get("snapshot_id")
            return result

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.VolumeSize``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-volumesize
            """
            result = self._values.get("volume_size")
            return result

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.VolumeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-volumetype
            """
            result = self._values.get("volume_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockDeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.MetadataOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_endpoint": "httpEndpoint",
            "http_put_response_hop_limit": "httpPutResponseHopLimit",
            "http_tokens": "httpTokens",
        },
    )
    class MetadataOptionProperty:
        def __init__(
            self,
            *,
            http_endpoint: typing.Optional[builtins.str] = None,
            http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
            http_tokens: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param http_endpoint: ``CfnLaunchConfiguration.MetadataOptionProperty.HttpEndpoint``.
            :param http_put_response_hop_limit: ``CfnLaunchConfiguration.MetadataOptionProperty.HttpPutResponseHopLimit``.
            :param http_tokens: ``CfnLaunchConfiguration.MetadataOptionProperty.HttpTokens``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfig-metadataoption.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if http_endpoint is not None:
                self._values["http_endpoint"] = http_endpoint
            if http_put_response_hop_limit is not None:
                self._values["http_put_response_hop_limit"] = http_put_response_hop_limit
            if http_tokens is not None:
                self._values["http_tokens"] = http_tokens

        @builtins.property
        def http_endpoint(self) -> typing.Optional[builtins.str]:
            """``CfnLaunchConfiguration.MetadataOptionProperty.HttpEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfig-metadataoption.html#cfn-autoscaling-launchconfig-metadataoption-httpendpoint
            """
            result = self._values.get("http_endpoint")
            return result

        @builtins.property
        def http_put_response_hop_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnLaunchConfiguration.MetadataOptionProperty.HttpPutResponseHopLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfig-metadataoption.html#cfn-autoscaling-launchconfig-metadataoption-httpputresponsehoplimit
            """
            result = self._values.get("http_put_response_hop_limit")
            return result

        @builtins.property
        def http_tokens(self) -> typing.Optional[builtins.str]:
            """``CfnLaunchConfiguration.MetadataOptionProperty.HttpTokens``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfig-metadataoption.html#cfn-autoscaling-launchconfig-metadataoption-httptokens
            """
            result = self._values.get("http_tokens")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_id": "imageId",
        "instance_type": "instanceType",
        "associate_public_ip_address": "associatePublicIpAddress",
        "block_device_mappings": "blockDeviceMappings",
        "classic_link_vpc_id": "classicLinkVpcId",
        "classic_link_vpc_security_groups": "classicLinkVpcSecurityGroups",
        "ebs_optimized": "ebsOptimized",
        "iam_instance_profile": "iamInstanceProfile",
        "instance_id": "instanceId",
        "instance_monitoring": "instanceMonitoring",
        "kernel_id": "kernelId",
        "key_name": "keyName",
        "launch_configuration_name": "launchConfigurationName",
        "metadata_options": "metadataOptions",
        "placement_tenancy": "placementTenancy",
        "ram_disk_id": "ramDiskId",
        "security_groups": "securityGroups",
        "spot_price": "spotPrice",
        "user_data": "userData",
    },
)
class CfnLaunchConfigurationProps:
    def __init__(
        self,
        *,
        image_id: builtins.str,
        instance_type: builtins.str,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        block_device_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLaunchConfiguration.BlockDeviceMappingProperty]]]] = None,
        classic_link_vpc_id: typing.Optional[builtins.str] = None,
        classic_link_vpc_security_groups: typing.Optional[typing.List[builtins.str]] = None,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        iam_instance_profile: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_monitoring: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        kernel_id: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        launch_configuration_name: typing.Optional[builtins.str] = None,
        metadata_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLaunchConfiguration.MetadataOptionProperty]] = None,
        placement_tenancy: typing.Optional[builtins.str] = None,
        ram_disk_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        spot_price: typing.Optional[builtins.str] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::AutoScaling::LaunchConfiguration``.

        :param image_id: ``AWS::AutoScaling::LaunchConfiguration.ImageId``.
        :param instance_type: ``AWS::AutoScaling::LaunchConfiguration.InstanceType``.
        :param associate_public_ip_address: ``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.
        :param block_device_mappings: ``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.
        :param classic_link_vpc_id: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.
        :param classic_link_vpc_security_groups: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.
        :param ebs_optimized: ``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.
        :param iam_instance_profile: ``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.
        :param instance_id: ``AWS::AutoScaling::LaunchConfiguration.InstanceId``.
        :param instance_monitoring: ``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.
        :param kernel_id: ``AWS::AutoScaling::LaunchConfiguration.KernelId``.
        :param key_name: ``AWS::AutoScaling::LaunchConfiguration.KeyName``.
        :param launch_configuration_name: ``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.
        :param metadata_options: ``AWS::AutoScaling::LaunchConfiguration.MetadataOptions``.
        :param placement_tenancy: ``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.
        :param ram_disk_id: ``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.
        :param security_groups: ``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.
        :param spot_price: ``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.
        :param user_data: ``AWS::AutoScaling::LaunchConfiguration.UserData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "image_id": image_id,
            "instance_type": instance_type,
        }
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if classic_link_vpc_id is not None:
            self._values["classic_link_vpc_id"] = classic_link_vpc_id
        if classic_link_vpc_security_groups is not None:
            self._values["classic_link_vpc_security_groups"] = classic_link_vpc_security_groups
        if ebs_optimized is not None:
            self._values["ebs_optimized"] = ebs_optimized
        if iam_instance_profile is not None:
            self._values["iam_instance_profile"] = iam_instance_profile
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if instance_monitoring is not None:
            self._values["instance_monitoring"] = instance_monitoring
        if kernel_id is not None:
            self._values["kernel_id"] = kernel_id
        if key_name is not None:
            self._values["key_name"] = key_name
        if launch_configuration_name is not None:
            self._values["launch_configuration_name"] = launch_configuration_name
        if metadata_options is not None:
            self._values["metadata_options"] = metadata_options
        if placement_tenancy is not None:
            self._values["placement_tenancy"] = placement_tenancy
        if ram_disk_id is not None:
            self._values["ram_disk_id"] = ram_disk_id
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot_price is not None:
            self._values["spot_price"] = spot_price
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def image_id(self) -> builtins.str:
        """``AWS::AutoScaling::LaunchConfiguration.ImageId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-imageid
        """
        result = self._values.get("image_id")
        assert result is not None, "Required property 'image_id' is missing"
        return result

    @builtins.property
    def instance_type(self) -> builtins.str:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancetype
        """
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cf-as-launchconfig-associatepubip
        """
        result = self._values.get("associate_public_ip_address")
        return result

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLaunchConfiguration.BlockDeviceMappingProperty]]]]:
        """``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-blockdevicemappings
        """
        result = self._values.get("block_device_mappings")
        return result

    @builtins.property
    def classic_link_vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcid
        """
        result = self._values.get("classic_link_vpc_id")
        return result

    @builtins.property
    def classic_link_vpc_security_groups(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcsecuritygroups
        """
        result = self._values.get("classic_link_vpc_security_groups")
        return result

    @builtins.property
    def ebs_optimized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ebsoptimized
        """
        result = self._values.get("ebs_optimized")
        return result

    @builtins.property
    def iam_instance_profile(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-iaminstanceprofile
        """
        result = self._values.get("iam_instance_profile")
        return result

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instanceid
        """
        result = self._values.get("instance_id")
        return result

    @builtins.property
    def instance_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancemonitoring
        """
        result = self._values.get("instance_monitoring")
        return result

    @builtins.property
    def kernel_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.KernelId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-kernelid
        """
        result = self._values.get("kernel_id")
        return result

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.KeyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-keyname
        """
        result = self._values.get("key_name")
        return result

    @builtins.property
    def launch_configuration_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-autoscaling-launchconfig-launchconfigurationname
        """
        result = self._values.get("launch_configuration_name")
        return result

    @builtins.property
    def metadata_options(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLaunchConfiguration.MetadataOptionProperty]]:
        """``AWS::AutoScaling::LaunchConfiguration.MetadataOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-autoscaling-launchconfig-metadataoptions
        """
        result = self._values.get("metadata_options")
        return result

    @builtins.property
    def placement_tenancy(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-placementtenancy
        """
        result = self._values.get("placement_tenancy")
        return result

    @builtins.property
    def ram_disk_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ramdiskid
        """
        result = self._values.get("ram_disk_id")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-securitygroups
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def spot_price(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-spotprice
        """
        result = self._values.get("spot_price")
        return result

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LaunchConfiguration.UserData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-userdata
        """
        result = self._values.get("user_data")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLifecycleHook(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHook",
):
    """A CloudFormation ``AWS::AutoScaling::LifecycleHook``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html
    :cloudformationResource: AWS::AutoScaling::LifecycleHook
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        auto_scaling_group_name: builtins.str,
        lifecycle_transition: builtins.str,
        default_result: typing.Optional[builtins.str] = None,
        heartbeat_timeout: typing.Optional[jsii.Number] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        notification_target_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::AutoScaling::LifecycleHook``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_scaling_group_name: ``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.
        :param lifecycle_transition: ``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.
        :param default_result: ``AWS::AutoScaling::LifecycleHook.DefaultResult``.
        :param heartbeat_timeout: ``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.
        :param lifecycle_hook_name: ``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.
        :param notification_metadata: ``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.
        :param notification_target_arn: ``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.
        :param role_arn: ``AWS::AutoScaling::LifecycleHook.RoleARN``.
        """
        props = CfnLifecycleHookProps(
            auto_scaling_group_name=auto_scaling_group_name,
            lifecycle_transition=lifecycle_transition,
            default_result=default_result,
            heartbeat_timeout=heartbeat_timeout,
            lifecycle_hook_name=lifecycle_hook_name,
            notification_metadata=notification_metadata,
            notification_target_arn=notification_target_arn,
            role_arn=role_arn,
        )

        jsii.create(CfnLifecycleHook, self, [scope, id, props])

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
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> builtins.str:
        """``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-autoscalinggroupname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter # type: ignore
    def auto_scaling_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "autoScalingGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lifecycleTransition")
    def lifecycle_transition(self) -> builtins.str:
        """``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-lifecycletransition
        """
        return jsii.get(self, "lifecycleTransition")

    @lifecycle_transition.setter # type: ignore
    def lifecycle_transition(self, value: builtins.str) -> None:
        jsii.set(self, "lifecycleTransition", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultResult")
    def default_result(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.DefaultResult``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-defaultresult
        """
        return jsii.get(self, "defaultResult")

    @default_result.setter # type: ignore
    def default_result(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultResult", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="heartbeatTimeout")
    def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-heartbeattimeout
        """
        return jsii.get(self, "heartbeatTimeout")

    @heartbeat_timeout.setter # type: ignore
    def heartbeat_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "heartbeatTimeout", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-autoscaling-lifecyclehook-lifecyclehookname
        """
        return jsii.get(self, "lifecycleHookName")

    @lifecycle_hook_name.setter # type: ignore
    def lifecycle_hook_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "lifecycleHookName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="notificationMetadata")
    def notification_metadata(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationmetadata
        """
        return jsii.get(self, "notificationMetadata")

    @notification_metadata.setter # type: ignore
    def notification_metadata(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "notificationMetadata", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="notificationTargetArn")
    def notification_target_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationtargetarn
        """
        return jsii.get(self, "notificationTargetArn")

    @notification_target_arn.setter # type: ignore
    def notification_target_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "notificationTargetArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.RoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHookProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_name": "autoScalingGroupName",
        "lifecycle_transition": "lifecycleTransition",
        "default_result": "defaultResult",
        "heartbeat_timeout": "heartbeatTimeout",
        "lifecycle_hook_name": "lifecycleHookName",
        "notification_metadata": "notificationMetadata",
        "notification_target_arn": "notificationTargetArn",
        "role_arn": "roleArn",
    },
)
class CfnLifecycleHookProps:
    def __init__(
        self,
        *,
        auto_scaling_group_name: builtins.str,
        lifecycle_transition: builtins.str,
        default_result: typing.Optional[builtins.str] = None,
        heartbeat_timeout: typing.Optional[jsii.Number] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        notification_target_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::AutoScaling::LifecycleHook``.

        :param auto_scaling_group_name: ``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.
        :param lifecycle_transition: ``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.
        :param default_result: ``AWS::AutoScaling::LifecycleHook.DefaultResult``.
        :param heartbeat_timeout: ``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.
        :param lifecycle_hook_name: ``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.
        :param notification_metadata: ``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.
        :param notification_target_arn: ``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.
        :param role_arn: ``AWS::AutoScaling::LifecycleHook.RoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "auto_scaling_group_name": auto_scaling_group_name,
            "lifecycle_transition": lifecycle_transition,
        }
        if default_result is not None:
            self._values["default_result"] = default_result
        if heartbeat_timeout is not None:
            self._values["heartbeat_timeout"] = heartbeat_timeout
        if lifecycle_hook_name is not None:
            self._values["lifecycle_hook_name"] = lifecycle_hook_name
        if notification_metadata is not None:
            self._values["notification_metadata"] = notification_metadata
        if notification_target_arn is not None:
            self._values["notification_target_arn"] = notification_target_arn
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def auto_scaling_group_name(self) -> builtins.str:
        """``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-autoscalinggroupname
        """
        result = self._values.get("auto_scaling_group_name")
        assert result is not None, "Required property 'auto_scaling_group_name' is missing"
        return result

    @builtins.property
    def lifecycle_transition(self) -> builtins.str:
        """``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-lifecycletransition
        """
        result = self._values.get("lifecycle_transition")
        assert result is not None, "Required property 'lifecycle_transition' is missing"
        return result

    @builtins.property
    def default_result(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.DefaultResult``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-defaultresult
        """
        result = self._values.get("default_result")
        return result

    @builtins.property
    def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-heartbeattimeout
        """
        result = self._values.get("heartbeat_timeout")
        return result

    @builtins.property
    def lifecycle_hook_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-autoscaling-lifecyclehook-lifecyclehookname
        """
        result = self._values.get("lifecycle_hook_name")
        return result

    @builtins.property
    def notification_metadata(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationmetadata
        """
        result = self._values.get("notification_metadata")
        return result

    @builtins.property
    def notification_target_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationtargetarn
        """
        result = self._values.get("notification_target_arn")
        return result

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::LifecycleHook.RoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-rolearn
        """
        result = self._values.get("role_arn")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLifecycleHookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScalingPolicy(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy",
):
    """A CloudFormation ``AWS::AutoScaling::ScalingPolicy``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html
    :cloudformationResource: AWS::AutoScaling::ScalingPolicy
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        auto_scaling_group_name: builtins.str,
        adjustment_type: typing.Optional[builtins.str] = None,
        cooldown: typing.Optional[builtins.str] = None,
        estimated_instance_warmup: typing.Optional[jsii.Number] = None,
        metric_aggregation_type: typing.Optional[builtins.str] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
        policy_type: typing.Optional[builtins.str] = None,
        scaling_adjustment: typing.Optional[jsii.Number] = None,
        step_adjustments: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.StepAdjustmentProperty"]]]] = None,
        target_tracking_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.TargetTrackingConfigurationProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::AutoScaling::ScalingPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_scaling_group_name: ``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.
        :param adjustment_type: ``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.
        :param cooldown: ``AWS::AutoScaling::ScalingPolicy.Cooldown``.
        :param estimated_instance_warmup: ``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.
        :param metric_aggregation_type: ``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.
        :param min_adjustment_magnitude: ``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.
        :param policy_type: ``AWS::AutoScaling::ScalingPolicy.PolicyType``.
        :param scaling_adjustment: ``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.
        :param step_adjustments: ``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.
        :param target_tracking_configuration: ``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.
        """
        props = CfnScalingPolicyProps(
            auto_scaling_group_name=auto_scaling_group_name,
            adjustment_type=adjustment_type,
            cooldown=cooldown,
            estimated_instance_warmup=estimated_instance_warmup,
            metric_aggregation_type=metric_aggregation_type,
            min_adjustment_magnitude=min_adjustment_magnitude,
            policy_type=policy_type,
            scaling_adjustment=scaling_adjustment,
            step_adjustments=step_adjustments,
            target_tracking_configuration=target_tracking_configuration,
        )

        jsii.create(CfnScalingPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> builtins.str:
        """``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-autoscalinggroupname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter # type: ignore
    def auto_scaling_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "autoScalingGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="adjustmentType")
    def adjustment_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-adjustmenttype
        """
        return jsii.get(self, "adjustmentType")

    @adjustment_type.setter # type: ignore
    def adjustment_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "adjustmentType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cooldown")
    def cooldown(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.Cooldown``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-cooldown
        """
        return jsii.get(self, "cooldown")

    @cooldown.setter # type: ignore
    def cooldown(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cooldown", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="estimatedInstanceWarmup")
    def estimated_instance_warmup(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-estimatedinstancewarmup
        """
        return jsii.get(self, "estimatedInstanceWarmup")

    @estimated_instance_warmup.setter # type: ignore
    def estimated_instance_warmup(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "estimatedInstanceWarmup", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metricAggregationType")
    def metric_aggregation_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-metricaggregationtype
        """
        return jsii.get(self, "metricAggregationType")

    @metric_aggregation_type.setter # type: ignore
    def metric_aggregation_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "metricAggregationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minAdjustmentMagnitude")
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-minadjustmentmagnitude
        """
        return jsii.get(self, "minAdjustmentMagnitude")

    @min_adjustment_magnitude.setter # type: ignore
    def min_adjustment_magnitude(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "minAdjustmentMagnitude", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.PolicyType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-policytype
        """
        return jsii.get(self, "policyType")

    @policy_type.setter # type: ignore
    def policy_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "policyType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scalingAdjustment")
    def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-scalingadjustment
        """
        return jsii.get(self, "scalingAdjustment")

    @scaling_adjustment.setter # type: ignore
    def scaling_adjustment(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "scalingAdjustment", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stepAdjustments")
    def step_adjustments(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.StepAdjustmentProperty"]]]]:
        """``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-stepadjustments
        """
        return jsii.get(self, "stepAdjustments")

    @step_adjustments.setter # type: ignore
    def step_adjustments(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.StepAdjustmentProperty"]]]],
    ) -> None:
        jsii.set(self, "stepAdjustments", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetTrackingConfiguration")
    def target_tracking_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.TargetTrackingConfigurationProperty"]]:
        """``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration
        """
        return jsii.get(self, "targetTrackingConfiguration")

    @target_tracking_configuration.setter # type: ignore
    def target_tracking_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.TargetTrackingConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "targetTrackingConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.CustomizedMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_name": "metricName",
            "namespace": "namespace",
            "statistic": "statistic",
            "dimensions": "dimensions",
            "unit": "unit",
        },
    )
    class CustomizedMetricSpecificationProperty:
        def __init__(
            self,
            *,
            metric_name: builtins.str,
            namespace: builtins.str,
            statistic: builtins.str,
            dimensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.MetricDimensionProperty"]]]] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param metric_name: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.
            :param namespace: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.
            :param statistic: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.
            :param dimensions: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Dimensions``.
            :param unit: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "metric_name": metric_name,
                "namespace": namespace,
                "statistic": statistic,
            }
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric_name(self) -> builtins.str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-metricname
            """
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return result

        @builtins.property
        def namespace(self) -> builtins.str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-namespace
            """
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return result

        @builtins.property
        def statistic(self) -> builtins.str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-statistic
            """
            result = self._values.get("statistic")
            assert result is not None, "Required property 'statistic' is missing"
            return result

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.MetricDimensionProperty"]]]]:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-dimensions
            """
            result = self._values.get("dimensions")
            return result

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-unit
            """
            result = self._values.get("unit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomizedMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            """
            :param name: ``CfnScalingPolicy.MetricDimensionProperty.Name``.
            :param value: ``CfnScalingPolicy.MetricDimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnScalingPolicy.MetricDimensionProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnScalingPolicy.MetricDimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredefinedMetricSpecificationProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: builtins.str,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param predefined_metric_type: ``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.
            :param resource_label: ``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "predefined_metric_type": predefined_metric_type,
            }
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> builtins.str:
            """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-predefinedmetrictype
            """
            result = self._values.get("predefined_metric_type")
            assert result is not None, "Required property 'predefined_metric_type' is missing"
            return result

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-resourcelabel
            """
            result = self._values.get("resource_label")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredefinedMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.StepAdjustmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "scaling_adjustment": "scalingAdjustment",
            "metric_interval_lower_bound": "metricIntervalLowerBound",
            "metric_interval_upper_bound": "metricIntervalUpperBound",
        },
    )
    class StepAdjustmentProperty:
        def __init__(
            self,
            *,
            scaling_adjustment: jsii.Number,
            metric_interval_lower_bound: typing.Optional[jsii.Number] = None,
            metric_interval_upper_bound: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param scaling_adjustment: ``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.
            :param metric_interval_lower_bound: ``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.
            :param metric_interval_upper_bound: ``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "scaling_adjustment": scaling_adjustment,
            }
            if metric_interval_lower_bound is not None:
                self._values["metric_interval_lower_bound"] = metric_interval_lower_bound
            if metric_interval_upper_bound is not None:
                self._values["metric_interval_upper_bound"] = metric_interval_upper_bound

        @builtins.property
        def scaling_adjustment(self) -> jsii.Number:
            """``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-scalingadjustment
            """
            result = self._values.get("scaling_adjustment")
            assert result is not None, "Required property 'scaling_adjustment' is missing"
            return result

        @builtins.property
        def metric_interval_lower_bound(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervallowerbound
            """
            result = self._values.get("metric_interval_lower_bound")
            return result

        @builtins.property
        def metric_interval_upper_bound(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervalupperbound
            """
            result = self._values.get("metric_interval_upper_bound")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepAdjustmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.TargetTrackingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_value": "targetValue",
            "customized_metric_specification": "customizedMetricSpecification",
            "disable_scale_in": "disableScaleIn",
            "predefined_metric_specification": "predefinedMetricSpecification",
        },
    )
    class TargetTrackingConfigurationProperty:
        def __init__(
            self,
            *,
            target_value: jsii.Number,
            customized_metric_specification: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.CustomizedMetricSpecificationProperty"]] = None,
            disable_scale_in: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            predefined_metric_specification: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.PredefinedMetricSpecificationProperty"]] = None,
        ) -> None:
            """
            :param target_value: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.TargetValue``.
            :param customized_metric_specification: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.CustomizedMetricSpecification``.
            :param disable_scale_in: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.DisableScaleIn``.
            :param predefined_metric_specification: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.PredefinedMetricSpecification``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "target_value": target_value,
            }
            if customized_metric_specification is not None:
                self._values["customized_metric_specification"] = customized_metric_specification
            if disable_scale_in is not None:
                self._values["disable_scale_in"] = disable_scale_in
            if predefined_metric_specification is not None:
                self._values["predefined_metric_specification"] = predefined_metric_specification

        @builtins.property
        def target_value(self) -> jsii.Number:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.TargetValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-targetvalue
            """
            result = self._values.get("target_value")
            assert result is not None, "Required property 'target_value' is missing"
            return result

        @builtins.property
        def customized_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.CustomizedMetricSpecificationProperty"]]:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.CustomizedMetricSpecification``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-customizedmetricspecification
            """
            result = self._values.get("customized_metric_specification")
            return result

        @builtins.property
        def disable_scale_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.DisableScaleIn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-disablescalein
            """
            result = self._values.get("disable_scale_in")
            return result

        @builtins.property
        def predefined_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.PredefinedMetricSpecificationProperty"]]:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.PredefinedMetricSpecification``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-predefinedmetricspecification
            """
            result = self._values.get("predefined_metric_specification")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_name": "autoScalingGroupName",
        "adjustment_type": "adjustmentType",
        "cooldown": "cooldown",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "metric_aggregation_type": "metricAggregationType",
        "min_adjustment_magnitude": "minAdjustmentMagnitude",
        "policy_type": "policyType",
        "scaling_adjustment": "scalingAdjustment",
        "step_adjustments": "stepAdjustments",
        "target_tracking_configuration": "targetTrackingConfiguration",
    },
)
class CfnScalingPolicyProps:
    def __init__(
        self,
        *,
        auto_scaling_group_name: builtins.str,
        adjustment_type: typing.Optional[builtins.str] = None,
        cooldown: typing.Optional[builtins.str] = None,
        estimated_instance_warmup: typing.Optional[jsii.Number] = None,
        metric_aggregation_type: typing.Optional[builtins.str] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
        policy_type: typing.Optional[builtins.str] = None,
        scaling_adjustment: typing.Optional[jsii.Number] = None,
        step_adjustments: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnScalingPolicy.StepAdjustmentProperty]]]] = None,
        target_tracking_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnScalingPolicy.TargetTrackingConfigurationProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AutoScaling::ScalingPolicy``.

        :param auto_scaling_group_name: ``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.
        :param adjustment_type: ``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.
        :param cooldown: ``AWS::AutoScaling::ScalingPolicy.Cooldown``.
        :param estimated_instance_warmup: ``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.
        :param metric_aggregation_type: ``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.
        :param min_adjustment_magnitude: ``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.
        :param policy_type: ``AWS::AutoScaling::ScalingPolicy.PolicyType``.
        :param scaling_adjustment: ``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.
        :param step_adjustments: ``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.
        :param target_tracking_configuration: ``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "auto_scaling_group_name": auto_scaling_group_name,
        }
        if adjustment_type is not None:
            self._values["adjustment_type"] = adjustment_type
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if metric_aggregation_type is not None:
            self._values["metric_aggregation_type"] = metric_aggregation_type
        if min_adjustment_magnitude is not None:
            self._values["min_adjustment_magnitude"] = min_adjustment_magnitude
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if scaling_adjustment is not None:
            self._values["scaling_adjustment"] = scaling_adjustment
        if step_adjustments is not None:
            self._values["step_adjustments"] = step_adjustments
        if target_tracking_configuration is not None:
            self._values["target_tracking_configuration"] = target_tracking_configuration

    @builtins.property
    def auto_scaling_group_name(self) -> builtins.str:
        """``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-autoscalinggroupname
        """
        result = self._values.get("auto_scaling_group_name")
        assert result is not None, "Required property 'auto_scaling_group_name' is missing"
        return result

    @builtins.property
    def adjustment_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-adjustmenttype
        """
        result = self._values.get("adjustment_type")
        return result

    @builtins.property
    def cooldown(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.Cooldown``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-cooldown
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-estimatedinstancewarmup
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def metric_aggregation_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-metricaggregationtype
        """
        result = self._values.get("metric_aggregation_type")
        return result

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-minadjustmentmagnitude
        """
        result = self._values.get("min_adjustment_magnitude")
        return result

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScalingPolicy.PolicyType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-policytype
        """
        result = self._values.get("policy_type")
        return result

    @builtins.property
    def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-scalingadjustment
        """
        result = self._values.get("scaling_adjustment")
        return result

    @builtins.property
    def step_adjustments(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnScalingPolicy.StepAdjustmentProperty]]]]:
        """``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-stepadjustments
        """
        result = self._values.get("step_adjustments")
        return result

    @builtins.property
    def target_tracking_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnScalingPolicy.TargetTrackingConfigurationProperty]]:
        """``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration
        """
        result = self._values.get("target_tracking_configuration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScalingPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScheduledAction(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledAction",
):
    """A CloudFormation ``AWS::AutoScaling::ScheduledAction``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html
    :cloudformationResource: AWS::AutoScaling::ScheduledAction
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        auto_scaling_group_name: builtins.str,
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[builtins.str] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        recurrence: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::AutoScaling::ScheduledAction``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_scaling_group_name: ``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.
        :param desired_capacity: ``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.
        :param end_time: ``AWS::AutoScaling::ScheduledAction.EndTime``.
        :param max_size: ``AWS::AutoScaling::ScheduledAction.MaxSize``.
        :param min_size: ``AWS::AutoScaling::ScheduledAction.MinSize``.
        :param recurrence: ``AWS::AutoScaling::ScheduledAction.Recurrence``.
        :param start_time: ``AWS::AutoScaling::ScheduledAction.StartTime``.
        """
        props = CfnScheduledActionProps(
            auto_scaling_group_name=auto_scaling_group_name,
            desired_capacity=desired_capacity,
            end_time=end_time,
            max_size=max_size,
            min_size=min_size,
            recurrence=recurrence,
            start_time=start_time,
        )

        jsii.create(CfnScheduledAction, self, [scope, id, props])

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
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> builtins.str:
        """``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-asgname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter # type: ignore
    def auto_scaling_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "autoScalingGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="desiredCapacity")
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-desiredcapacity
        """
        return jsii.get(self, "desiredCapacity")

    @desired_capacity.setter # type: ignore
    def desired_capacity(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "desiredCapacity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScheduledAction.EndTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-endtime
        """
        return jsii.get(self, "endTime")

    @end_time.setter # type: ignore
    def end_time(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "endTime", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-maxsize
        """
        return jsii.get(self, "maxSize")

    @max_size.setter # type: ignore
    def max_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-minsize
        """
        return jsii.get(self, "minSize")

    @min_size.setter # type: ignore
    def min_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "minSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScheduledAction.Recurrence``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-recurrence
        """
        return jsii.get(self, "recurrence")

    @recurrence.setter # type: ignore
    def recurrence(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "recurrence", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScheduledAction.StartTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-starttime
        """
        return jsii.get(self, "startTime")

    @start_time.setter # type: ignore
    def start_time(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "startTime", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_name": "autoScalingGroupName",
        "desired_capacity": "desiredCapacity",
        "end_time": "endTime",
        "max_size": "maxSize",
        "min_size": "minSize",
        "recurrence": "recurrence",
        "start_time": "startTime",
    },
)
class CfnScheduledActionProps:
    def __init__(
        self,
        *,
        auto_scaling_group_name: builtins.str,
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[builtins.str] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        recurrence: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::AutoScaling::ScheduledAction``.

        :param auto_scaling_group_name: ``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.
        :param desired_capacity: ``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.
        :param end_time: ``AWS::AutoScaling::ScheduledAction.EndTime``.
        :param max_size: ``AWS::AutoScaling::ScheduledAction.MaxSize``.
        :param min_size: ``AWS::AutoScaling::ScheduledAction.MinSize``.
        :param recurrence: ``AWS::AutoScaling::ScheduledAction.Recurrence``.
        :param start_time: ``AWS::AutoScaling::ScheduledAction.StartTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "auto_scaling_group_name": auto_scaling_group_name,
        }
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if end_time is not None:
            self._values["end_time"] = end_time
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def auto_scaling_group_name(self) -> builtins.str:
        """``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-asgname
        """
        result = self._values.get("auto_scaling_group_name")
        assert result is not None, "Required property 'auto_scaling_group_name' is missing"
        return result

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-desiredcapacity
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScheduledAction.EndTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-endtime
        """
        result = self._values.get("end_time")
        return result

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-maxsize
        """
        result = self._values.get("max_size")
        return result

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-minsize
        """
        result = self._values.get("min_size")
        return result

    @builtins.property
    def recurrence(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScheduledAction.Recurrence``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-recurrence
        """
        result = self._values.get("recurrence")
        return result

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        """``AWS::AutoScaling::ScheduledAction.StartTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-starttime
        """
        result = self._values.get("start_time")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduledActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CommonAutoScalingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "associate_public_ip_address": "associatePublicIpAddress",
        "auto_scaling_group_name": "autoScalingGroupName",
        "block_devices": "blockDevices",
        "cooldown": "cooldown",
        "desired_capacity": "desiredCapacity",
        "group_metrics": "groupMetrics",
        "health_check": "healthCheck",
        "ignore_unmodified_size_properties": "ignoreUnmodifiedSizeProperties",
        "instance_monitoring": "instanceMonitoring",
        "key_name": "keyName",
        "max_capacity": "maxCapacity",
        "max_instance_lifetime": "maxInstanceLifetime",
        "min_capacity": "minCapacity",
        "notifications": "notifications",
        "notifications_topic": "notificationsTopic",
        "replacing_update_min_successful_instances_percent": "replacingUpdateMinSuccessfulInstancesPercent",
        "resource_signal_count": "resourceSignalCount",
        "resource_signal_timeout": "resourceSignalTimeout",
        "rolling_update_configuration": "rollingUpdateConfiguration",
        "signals": "signals",
        "spot_price": "spotPrice",
        "update_policy": "updatePolicy",
        "update_type": "updateType",
        "vpc_subnets": "vpcSubnets",
    },
)
class CommonAutoScalingGroupProps:
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        associate_public_ip_address: typing.Optional[builtins.bool] = None,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        block_devices: typing.Optional[typing.List[BlockDevice]] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        group_metrics: typing.Optional[typing.List["GroupMetrics"]] = None,
        health_check: typing.Optional["HealthCheck"] = None,
        ignore_unmodified_size_properties: typing.Optional[builtins.bool] = None,
        instance_monitoring: typing.Optional["Monitoring"] = None,
        key_name: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_instance_lifetime: typing.Optional[aws_cdk.core.Duration] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.List["NotificationConfiguration"]] = None,
        notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
        replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number] = None,
        resource_signal_count: typing.Optional[jsii.Number] = None,
        resource_signal_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        rolling_update_configuration: typing.Optional["RollingUpdateConfiguration"] = None,
        signals: typing.Optional["Signals"] = None,
        spot_price: typing.Optional[builtins.str] = None,
        update_policy: typing.Optional["UpdatePolicy"] = None,
        update_type: typing.Optional["UpdateType"] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Basic properties of an AutoScalingGroup, except the exact machines to run and where they should run.

        Constructs that want to create AutoScalingGroups can inherit
        this interface and specialize the essential parts in various ways.

        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param auto_scaling_group_name: The name of the Auto Scaling group. This name must be unique per Region per account. Default: - Auto generated by CloudFormation
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param group_metrics: Enable monitoring for group metrics, these metrics describe the group rather than any of its instances. To report all group metrics use ``GroupMetrics.all()`` Group metrics are reported in a granularity of 1 minute at no additional charge. Default: - no group metrics will be reported
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, leave this property undefined. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: (deprecated) SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: (deprecated) Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: (deprecated) How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1 if resourceSignalTimeout is set, 0 otherwise
        :param resource_signal_timeout: (deprecated) The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5) if resourceSignalCount is set, N/A otherwise
        :param rolling_update_configuration: (deprecated) Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param signals: Configure waiting for signals during deployment. Use this to pause the CloudFormation deployment to wait for the instances in the AutoScalingGroup to report successful startup during creation and updates. The UserData script needs to invoke ``cfn-signal`` with a success or failure code after it is done setting up the instance. Without waiting for signals, the CloudFormation deployment will proceed as soon as the AutoScalingGroup has been created or updated but before the instances in the group have been started. For example, to have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling rolling updates sample template: https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/AutoScaling/AutoScalingRollingUpdates.yaml Default: - Do not wait for signals
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_policy: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: - ``UpdatePolicy.rollingUpdate()`` if using ``init``, ``UpdatePolicy.none()`` otherwise
        :param update_type: (deprecated) What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        """
        if isinstance(rolling_update_configuration, dict):
            rolling_update_configuration = RollingUpdateConfiguration(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if group_metrics is not None:
            self._values["group_metrics"] = group_metrics
        if health_check is not None:
            self._values["health_check"] = health_check
        if ignore_unmodified_size_properties is not None:
            self._values["ignore_unmodified_size_properties"] = ignore_unmodified_size_properties
        if instance_monitoring is not None:
            self._values["instance_monitoring"] = instance_monitoring
        if key_name is not None:
            self._values["key_name"] = key_name
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_instance_lifetime is not None:
            self._values["max_instance_lifetime"] = max_instance_lifetime
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if notifications is not None:
            self._values["notifications"] = notifications
        if notifications_topic is not None:
            self._values["notifications_topic"] = notifications_topic
        if replacing_update_min_successful_instances_percent is not None:
            self._values["replacing_update_min_successful_instances_percent"] = replacing_update_min_successful_instances_percent
        if resource_signal_count is not None:
            self._values["resource_signal_count"] = resource_signal_count
        if resource_signal_timeout is not None:
            self._values["resource_signal_timeout"] = resource_signal_timeout
        if rolling_update_configuration is not None:
            self._values["rolling_update_configuration"] = rolling_update_configuration
        if signals is not None:
            self._values["signals"] = signals
        if spot_price is not None:
            self._values["spot_price"] = spot_price
        if update_policy is not None:
            self._values["update_policy"] = update_policy
        if update_type is not None:
            self._values["update_type"] = update_type
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        """Whether the instances can initiate connections to anywhere by default.

        :default: true
        """
        result = self._values.get("allow_all_outbound")
        return result

    @builtins.property
    def associate_public_ip_address(self) -> typing.Optional[builtins.bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        :default: - Use subnet setting.
        """
        result = self._values.get("associate_public_ip_address")
        return result

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        """The name of the Auto Scaling group.

        This name must be unique per Region per account.

        :default: - Auto generated by CloudFormation
        """
        result = self._values.get("auto_scaling_group_name")
        return result

    @builtins.property
    def block_devices(self) -> typing.Optional[typing.List[BlockDevice]]:
        """Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        :default: - Uses the block device mapping of the AMI

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        """
        result = self._values.get("block_devices")
        return result

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Default scaling cooldown for this AutoScalingGroup.

        :default: Duration.minutes(5)
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of instances in the fleet.

        If this is set to a number, every deployment will reset the amount of
        instances to this number. It is recommended to leave this value blank.

        :default: minCapacity, and leave unchanged during deployment

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def group_metrics(self) -> typing.Optional[typing.List["GroupMetrics"]]:
        """Enable monitoring for group metrics, these metrics describe the group rather than any of its instances.

        To report all group metrics use ``GroupMetrics.all()``
        Group metrics are reported in a granularity of 1 minute at no additional charge.

        :default: - no group metrics will be reported
        """
        result = self._values.get("group_metrics")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Configuration for health checks.

        :default: - HealthCheck.ec2 with no grace period
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def ignore_unmodified_size_properties(self) -> typing.Optional[builtins.bool]:
        """If the ASG has scheduled actions, don't reset unchanged group sizes.

        Only used if the ASG has scheduled actions (which may scale your ASG up
        or down regardless of cdk deployments). If true, the size of the group
        will only be reset if it has been changed in the CDK app. If false, the
        sizes will always be changed back to what they were in the CDK app
        on deployment.

        :default: true
        """
        result = self._values.get("ignore_unmodified_size_properties")
        return result

    @builtins.property
    def instance_monitoring(self) -> typing.Optional["Monitoring"]:
        """Controls whether instances in this group are launched with detailed or basic monitoring.

        When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account
        is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes.

        :default: - Monitoring.DETAILED

        :see: https://docs.aws.amazon.com/autoscaling/latest/userguide/as-instance-monitoring.html#enable-as-instance-metrics
        """
        result = self._values.get("instance_monitoring")
        return result

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        """Name of SSH keypair to grant access to instances.

        :default: - No SSH access will be possible.
        """
        result = self._values.get("key_name")
        return result

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        :default: desiredCapacity
        """
        result = self._values.get("max_capacity")
        return result

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum amount of time that an instance can be in service.

        The maximum duration applies
        to all current and future instances in the group. As an instance approaches its maximum duration,
        it is terminated and replaced, and cannot be used again.

        You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value,
        leave this property undefined.

        :default: none

        :see: https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html
        """
        result = self._values.get("max_instance_lifetime")
        return result

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        :default: 1
        """
        result = self._values.get("min_capacity")
        return result

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional[typing.List["NotificationConfiguration"]]:
        """Configure autoscaling group to send notifications about fleet changes to an SNS topic(s).

        :default: - No fleet change notifications will be sent.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        """
        result = self._values.get("notifications")
        return result

    @builtins.property
    def notifications_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """(deprecated) SNS topic to send notifications about fleet changes.

        :default: - No fleet change notifications will be sent.

        :deprecated: use ``notifications``

        :stability: deprecated
        """
        result = self._values.get("notifications_topic")
        return result

    @builtins.property
    def replacing_update_min_successful_instances_percent(
        self,
    ) -> typing.Optional[jsii.Number]:
        """(deprecated) Configuration for replacing updates.

        Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
        many instances must signal success for the update to succeed.

        :default: minSuccessfulInstancesPercent

        :deprecated: Use ``signals`` instead

        :stability: deprecated
        """
        result = self._values.get("replacing_update_min_successful_instances_percent")
        return result

    @builtins.property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """(deprecated) How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        :default: 1 if resourceSignalTimeout is set, 0 otherwise

        :deprecated: Use ``signals`` instead.

        :stability: deprecated
        """
        result = self._values.get("resource_signal_count")
        return result

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        :default: Duration.minutes(5) if resourceSignalCount is set, N/A otherwise

        :deprecated: Use ``signals`` instead.

        :stability: deprecated
        """
        result = self._values.get("resource_signal_timeout")
        return result

    @builtins.property
    def rolling_update_configuration(
        self,
    ) -> typing.Optional["RollingUpdateConfiguration"]:
        """(deprecated) Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        :default: - RollingUpdateConfiguration with defaults.

        :deprecated: Use ``updatePolicy`` instead

        :stability: deprecated
        """
        result = self._values.get("rolling_update_configuration")
        return result

    @builtins.property
    def signals(self) -> typing.Optional["Signals"]:
        """Configure waiting for signals during deployment.

        Use this to pause the CloudFormation deployment to wait for the instances
        in the AutoScalingGroup to report successful startup during
        creation and updates. The UserData script needs to invoke ``cfn-signal``
        with a success or failure code after it is done setting up the instance.

        Without waiting for signals, the CloudFormation deployment will proceed as
        soon as the AutoScalingGroup has been created or updated but before the
        instances in the group have been started.

        For example, to have instances wait for an Elastic Load Balancing health check before
        they signal success, add a health-check verification by using the
        cfn-init helper script. For an example, see the verify_instance_health
        command in the Auto Scaling rolling updates sample template:

        https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/AutoScaling/AutoScalingRollingUpdates.yaml

        :default: - Do not wait for signals
        """
        result = self._values.get("signals")
        return result

    @builtins.property
    def spot_price(self) -> typing.Optional[builtins.str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        :default: none
        """
        result = self._values.get("spot_price")
        return result

    @builtins.property
    def update_policy(self) -> typing.Optional["UpdatePolicy"]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        :default: - ``UpdatePolicy.rollingUpdate()`` if using ``init``, ``UpdatePolicy.none()`` otherwise
        """
        result = self._values.get("update_policy")
        return result

    @builtins.property
    def update_type(self) -> typing.Optional["UpdateType"]:
        """(deprecated) What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        :default: UpdateType.None

        :deprecated: Use ``updatePolicy`` instead

        :stability: deprecated
        """
        result = self._values.get("update_type")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place instances within the VPC.

        :default: - All Private subnets.
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonAutoScalingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CpuUtilizationScalingProps",
    jsii_struct_bases=[BaseTargetTrackingProps],
    name_mapping={
        "cooldown": "cooldown",
        "disable_scale_in": "disableScaleIn",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "target_utilization_percent": "targetUtilizationPercent",
    },
)
class CpuUtilizationScalingProps(BaseTargetTrackingProps):
    def __init__(
        self,
        *,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        target_utilization_percent: jsii.Number,
    ) -> None:
        """Properties for enabling scaling based on CPU utilization.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_utilization_percent: Target average CPU utilization across the task.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_utilization_percent": target_utilization_percent,
        }
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        :default: false
        """
        result = self._values.get("disable_scale_in")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: - Same as the cooldown.
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def target_utilization_percent(self) -> jsii.Number:
        """Target average CPU utilization across the task."""
        result = self._values.get("target_utilization_percent")
        assert result is not None, "Required property 'target_utilization_percent' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CpuUtilizationScalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.CronOptions",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
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
    ) -> None:
        """Options to configure a cron expression.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week

        :see: http://crontab.org/
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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.DefaultResult")
class DefaultResult(enum.Enum):
    CONTINUE = "CONTINUE"
    ABANDON = "ABANDON"


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceOptionsBase",
    jsii_struct_bases=[],
    name_mapping={
        "delete_on_termination": "deleteOnTermination",
        "iops": "iops",
        "volume_type": "volumeType",
    },
)
class EbsDeviceOptionsBase:
    def __init__(
        self,
        *,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional["EbsDeviceVolumeType"] = None,
    ) -> None:
        """Base block device options for an EBS volume.

        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume. Default: - none, required for {@link EbsDeviceVolumeType.IO1}
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if iops is not None:
            self._values["iops"] = iops
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def delete_on_termination(self) -> typing.Optional[builtins.bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        result = self._values.get("delete_on_termination")
        return result

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        :default: - none, required for {@link EbsDeviceVolumeType.IO1}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("iops")
        return result

    @builtins.property
    def volume_type(self) -> typing.Optional["EbsDeviceVolumeType"]:
        """The EBS volume type.

        :default: {@link EbsDeviceVolumeType.GP2}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("volume_type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsDeviceOptionsBase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceSnapshotOptions",
    jsii_struct_bases=[EbsDeviceOptionsBase],
    name_mapping={
        "delete_on_termination": "deleteOnTermination",
        "iops": "iops",
        "volume_type": "volumeType",
        "volume_size": "volumeSize",
    },
)
class EbsDeviceSnapshotOptions(EbsDeviceOptionsBase):
    def __init__(
        self,
        *,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional["EbsDeviceVolumeType"] = None,
        volume_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Block device options for an EBS volume created from a snapshot.

        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume. Default: - none, required for {@link EbsDeviceVolumeType.IO1}
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        :param volume_size: The volume size, in Gibibytes (GiB). If you specify volumeSize, it must be equal or greater than the size of the snapshot. Default: - The snapshot size
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if iops is not None:
            self._values["iops"] = iops
        if volume_type is not None:
            self._values["volume_type"] = volume_type
        if volume_size is not None:
            self._values["volume_size"] = volume_size

    @builtins.property
    def delete_on_termination(self) -> typing.Optional[builtins.bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        result = self._values.get("delete_on_termination")
        return result

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        :default: - none, required for {@link EbsDeviceVolumeType.IO1}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("iops")
        return result

    @builtins.property
    def volume_type(self) -> typing.Optional["EbsDeviceVolumeType"]:
        """The EBS volume type.

        :default: {@link EbsDeviceVolumeType.GP2}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("volume_type")
        return result

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        """The volume size, in Gibibytes (GiB).

        If you specify volumeSize, it must be equal or greater than the size of the snapshot.

        :default: - The snapshot size
        """
        result = self._values.get("volume_size")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsDeviceSnapshotOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceVolumeType")
class EbsDeviceVolumeType(enum.Enum):
    """Supported EBS volume types for blockDevices."""

    STANDARD = "STANDARD"
    """Magnetic."""
    IO1 = "IO1"
    """Provisioned IOPS SSD."""
    GP2 = "GP2"
    """General Purpose SSD."""
    ST1 = "ST1"
    """Throughput Optimized HDD."""
    SC1 = "SC1"
    """Cold HDD."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.Ec2HealthCheckOptions",
    jsii_struct_bases=[],
    name_mapping={"grace": "grace"},
)
class Ec2HealthCheckOptions:
    def __init__(self, *, grace: typing.Optional[aws_cdk.core.Duration] = None) -> None:
        """EC2 Heath check options.

        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. Default: Duration.seconds(0)
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if grace is not None:
            self._values["grace"] = grace

    @builtins.property
    def grace(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service.

        :default: Duration.seconds(0)
        """
        result = self._values.get("grace")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2HealthCheckOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.ElbHealthCheckOptions",
    jsii_struct_bases=[],
    name_mapping={"grace": "grace"},
)
class ElbHealthCheckOptions:
    def __init__(self, *, grace: aws_cdk.core.Duration) -> None:
        """ELB Heath check options.

        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. This option is required for ELB health checks.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "grace": grace,
        }

    @builtins.property
    def grace(self) -> aws_cdk.core.Duration:
        """Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service.

        This option is required for ELB health checks.
        """
        result = self._values.get("grace")
        assert result is not None, "Required property 'grace' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElbHealthCheckOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupMetric(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.GroupMetric",
):
    """Group metrics that an Auto Scaling group sends to Amazon CloudWatch."""

    def __init__(self, name: builtins.str) -> None:
        """
        :param name: -
        """
        jsii.create(GroupMetric, self, [name])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DESIRED_CAPACITY")
    def DESIRED_CAPACITY(cls) -> "GroupMetric":
        """The number of instances that the Auto Scaling group attempts to maintain."""
        return jsii.sget(cls, "DESIRED_CAPACITY")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="IN_SERVICE_INSTANCES")
    def IN_SERVICE_INSTANCES(cls) -> "GroupMetric":
        """The number of instances that are running as part of the Auto Scaling group This metric does not include instances that are pending or terminating."""
        return jsii.sget(cls, "IN_SERVICE_INSTANCES")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MAX_SIZE")
    def MAX_SIZE(cls) -> "GroupMetric":
        """The maximum size of the Auto Scaling group."""
        return jsii.sget(cls, "MAX_SIZE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MIN_SIZE")
    def MIN_SIZE(cls) -> "GroupMetric":
        """The minimum size of the Auto Scaling group."""
        return jsii.sget(cls, "MIN_SIZE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PENDING_INSTANCES")
    def PENDING_INSTANCES(cls) -> "GroupMetric":
        """The number of instances that are pending A pending instance is not yet in service, this metric does not include instances that are in service or terminating."""
        return jsii.sget(cls, "PENDING_INSTANCES")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="STANDBY_INSTANCES")
    def STANDBY_INSTANCES(cls) -> "GroupMetric":
        """The number of instances that are in a Standby state Instances in this state are still running but are not actively in service."""
        return jsii.sget(cls, "STANDBY_INSTANCES")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="TERMINATING_INSTANCES")
    def TERMINATING_INSTANCES(cls) -> "GroupMetric":
        """The number of instances that are in the process of terminating This metric does not include instances that are in service or pending."""
        return jsii.sget(cls, "TERMINATING_INSTANCES")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="TOTAL_INSTANCES")
    def TOTAL_INSTANCES(cls) -> "GroupMetric":
        """The total number of instances in the Auto Scaling group This metric identifies the number of instances that are in service, pending, and terminating."""
        return jsii.sget(cls, "TOTAL_INSTANCES")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """The name of the group metric."""
        return jsii.get(self, "name")


class GroupMetrics(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.GroupMetrics",
):
    """A set of group metrics."""

    def __init__(self, *metrics: GroupMetric) -> None:
        """
        :param metrics: -
        """
        jsii.create(GroupMetrics, self, [*metrics])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "GroupMetrics":
        """Report all group metrics."""
        return jsii.sinvoke(cls, "all", [])


class HealthCheck(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.HealthCheck",
):
    """Health check settings."""

    @jsii.member(jsii_name="ec2")
    @builtins.classmethod
    def ec2(
        cls,
        *,
        grace: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "HealthCheck":
        """Use EC2 for health checks.

        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. Default: Duration.seconds(0)
        """
        options = Ec2HealthCheckOptions(grace=grace)

        return jsii.sinvoke(cls, "ec2", [options])

    @jsii.member(jsii_name="elb")
    @builtins.classmethod
    def elb(cls, *, grace: aws_cdk.core.Duration) -> "HealthCheck":
        """Use ELB for health checks.

        It considers the instance unhealthy if it fails either the EC2 status checks or the load balancer health checks.

        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. This option is required for ELB health checks.
        """
        options = ElbHealthCheckOptions(grace=grace)

        return jsii.sinvoke(cls, "elb", [options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return jsii.get(self, "type")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gracePeriod")
    def grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        return jsii.get(self, "gracePeriod")


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.IAutoScalingGroup")
class IAutoScalingGroup(
    aws_cdk.core.IResource,
    aws_cdk.aws_iam.IGrantable,
    typing_extensions.Protocol,
):
    """An AutoScalingGroup."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAutoScalingGroupProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingGroupArn")
    def auto_scaling_group_arn(self) -> builtins.str:
        """The arn of the AutoScalingGroup.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> builtins.str:
        """The name of the AutoScalingGroup.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="osType")
    def os_type(self) -> aws_cdk.aws_ec2.OperatingSystemType:
        """The operating system family that the instances in this auto-scaling group belong to.

        Is 'UNKNOWN' for imported ASGs.
        """
        ...

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(
        self,
        id: builtins.str,
        *,
        lifecycle_transition: "LifecycleTransition",
        notification_target: "ILifecycleHookTarget",
        default_result: typing.Optional[DefaultResult] = None,
        heartbeat_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        :param id: -
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        ...

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *commands: builtins.str) -> None:
        """Add command to the startup script of fleet instances.

        The command must be in the scripting language supported by the fleet's OS (i.e. Linux/Windows).
        Does nothing for imported ASGs.

        :param commands: -
        """
        ...

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(
        self,
        id: builtins.str,
        *,
        target_utilization_percent: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        :param id: -
        :param target_utilization_percent: Target average CPU utilization across the task.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(
        self,
        id: builtins.str,
        *,
        target_bytes_per_second: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        :param id: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(
        self,
        id: builtins.str,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        scaling_steps: typing.List["ScalingInterval"],
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    ) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        :param id: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        ...

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(
        self,
        id: builtins.str,
        *,
        target_bytes_per_second: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        :param id: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(
        self,
        id: builtins.str,
        *,
        schedule: "Schedule",
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> "ScheduledAction":
        """Scale out or in based on time.

        :param id: -
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        ...

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(
        self,
        id: builtins.str,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        target_value: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...


class _IAutoScalingGroupProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore
    jsii.proxy_for(aws_cdk.aws_iam.IGrantable), # type: ignore
):
    """An AutoScalingGroup."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-autoscaling.IAutoScalingGroup"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingGroupArn")
    def auto_scaling_group_arn(self) -> builtins.str:
        """The arn of the AutoScalingGroup.

        :attribute: true
        """
        return jsii.get(self, "autoScalingGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> builtins.str:
        """The name of the AutoScalingGroup.

        :attribute: true
        """
        return jsii.get(self, "autoScalingGroupName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="osType")
    def os_type(self) -> aws_cdk.aws_ec2.OperatingSystemType:
        """The operating system family that the instances in this auto-scaling group belong to.

        Is 'UNKNOWN' for imported ASGs.
        """
        return jsii.get(self, "osType")

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(
        self,
        id: builtins.str,
        *,
        lifecycle_transition: "LifecycleTransition",
        notification_target: "ILifecycleHookTarget",
        default_result: typing.Optional[DefaultResult] = None,
        heartbeat_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        :param id: -
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props = BasicLifecycleHookProps(
            lifecycle_transition=lifecycle_transition,
            notification_target=notification_target,
            default_result=default_result,
            heartbeat_timeout=heartbeat_timeout,
            lifecycle_hook_name=lifecycle_hook_name,
            notification_metadata=notification_metadata,
            role=role,
        )

        return jsii.invoke(self, "addLifecycleHook", [id, props])

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *commands: builtins.str) -> None:
        """Add command to the startup script of fleet instances.

        The command must be in the scripting language supported by the fleet's OS (i.e. Linux/Windows).
        Does nothing for imported ASGs.

        :param commands: -
        """
        return jsii.invoke(self, "addUserData", [*commands])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(
        self,
        id: builtins.str,
        *,
        target_utilization_percent: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        :param id: -
        :param target_utilization_percent: Target average CPU utilization across the task.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = CpuUtilizationScalingProps(
            target_utilization_percent=target_utilization_percent,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(
        self,
        id: builtins.str,
        *,
        target_bytes_per_second: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        :param id: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(
            target_bytes_per_second=target_bytes_per_second,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(
        self,
        id: builtins.str,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        scaling_steps: typing.List["ScalingInterval"],
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    ) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        :param id: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = BasicStepScalingPolicyProps(
            metric=metric,
            scaling_steps=scaling_steps,
            adjustment_type=adjustment_type,
            cooldown=cooldown,
            estimated_instance_warmup=estimated_instance_warmup,
            min_adjustment_magnitude=min_adjustment_magnitude,
        )

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(
        self,
        id: builtins.str,
        *,
        target_bytes_per_second: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        :param id: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(
            target_bytes_per_second=target_bytes_per_second,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(
        self,
        id: builtins.str,
        *,
        schedule: "Schedule",
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> "ScheduledAction":
        """Scale out or in based on time.

        :param id: -
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props = BasicScheduledActionProps(
            schedule=schedule,
            desired_capacity=desired_capacity,
            end_time=end_time,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            start_time=start_time,
        )

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(
        self,
        id: builtins.str,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        target_value: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = MetricTargetTrackingProps(
            metric=metric,
            target_value=target_value,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.ILifecycleHook")
class ILifecycleHook(aws_cdk.core.IResource, typing_extensions.Protocol):
    """A basic lifecycle hook object."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role for the lifecycle hook to execute."""
        ...


class _ILifecycleHookProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """A basic lifecycle hook object."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-autoscaling.ILifecycleHook"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role for the lifecycle hook to execute."""
        return jsii.get(self, "role")


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.ILifecycleHookTarget")
class ILifecycleHookTarget(typing_extensions.Protocol):
    """Interface for autoscaling lifecycle hook targets."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookTargetProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        lifecycle_hook: ILifecycleHook,
    ) -> "LifecycleHookTargetConfig":
        """Called when this object is used as the target of a lifecycle hook.

        :param scope: -
        :param lifecycle_hook: -
        """
        ...


class _ILifecycleHookTargetProxy:
    """Interface for autoscaling lifecycle hook targets."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-autoscaling.ILifecycleHookTarget"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        lifecycle_hook: ILifecycleHook,
    ) -> "LifecycleHookTargetConfig":
        """Called when this object is used as the target of a lifecycle hook.

        :param scope: -
        :param lifecycle_hook: -
        """
        return jsii.invoke(self, "bind", [scope, lifecycle_hook])


@jsii.implements(ILifecycleHook)
class LifecycleHook(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.LifecycleHook",
):
    """Define a life cycle hook."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auto_scaling_group: IAutoScalingGroup,
        lifecycle_transition: "LifecycleTransition",
        notification_target: ILifecycleHookTarget,
        default_result: typing.Optional[DefaultResult] = None,
        heartbeat_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param auto_scaling_group: The AutoScalingGroup to add the lifecycle hook to.
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props = LifecycleHookProps(
            auto_scaling_group=auto_scaling_group,
            lifecycle_transition=lifecycle_transition,
            notification_target=notification_target,
            default_result=default_result,
            heartbeat_timeout=heartbeat_timeout,
            lifecycle_hook_name=lifecycle_hook_name,
            notification_metadata=notification_metadata,
            role=role,
        )

        jsii.create(LifecycleHook, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> builtins.str:
        """The name of this lifecycle hook.

        :attribute: true
        """
        return jsii.get(self, "lifecycleHookName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role that allows the ASG to publish to the notification target."""
        return jsii.get(self, "role")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.LifecycleHookProps",
    jsii_struct_bases=[BasicLifecycleHookProps],
    name_mapping={
        "lifecycle_transition": "lifecycleTransition",
        "notification_target": "notificationTarget",
        "default_result": "defaultResult",
        "heartbeat_timeout": "heartbeatTimeout",
        "lifecycle_hook_name": "lifecycleHookName",
        "notification_metadata": "notificationMetadata",
        "role": "role",
        "auto_scaling_group": "autoScalingGroup",
    },
)
class LifecycleHookProps(BasicLifecycleHookProps):
    def __init__(
        self,
        *,
        lifecycle_transition: "LifecycleTransition",
        notification_target: ILifecycleHookTarget,
        default_result: typing.Optional[DefaultResult] = None,
        heartbeat_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        auto_scaling_group: IAutoScalingGroup,
    ) -> None:
        """Properties for a Lifecycle hook.

        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        :param auto_scaling_group: The AutoScalingGroup to add the lifecycle hook to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "lifecycle_transition": lifecycle_transition,
            "notification_target": notification_target,
            "auto_scaling_group": auto_scaling_group,
        }
        if default_result is not None:
            self._values["default_result"] = default_result
        if heartbeat_timeout is not None:
            self._values["heartbeat_timeout"] = heartbeat_timeout
        if lifecycle_hook_name is not None:
            self._values["lifecycle_hook_name"] = lifecycle_hook_name
        if notification_metadata is not None:
            self._values["notification_metadata"] = notification_metadata
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def lifecycle_transition(self) -> "LifecycleTransition":
        """The state of the Amazon EC2 instance to which you want to attach the lifecycle hook."""
        result = self._values.get("lifecycle_transition")
        assert result is not None, "Required property 'lifecycle_transition' is missing"
        return result

    @builtins.property
    def notification_target(self) -> ILifecycleHookTarget:
        """The target of the lifecycle hook."""
        result = self._values.get("notification_target")
        assert result is not None, "Required property 'notification_target' is missing"
        return result

    @builtins.property
    def default_result(self) -> typing.Optional[DefaultResult]:
        """The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs.

        :default: Continue
        """
        result = self._values.get("default_result")
        return result

    @builtins.property
    def heartbeat_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum time between calls to RecordLifecycleActionHeartbeat for the hook.

        If the lifecycle hook times out, perform the action in DefaultResult.

        :default: - No heartbeat timeout.
        """
        result = self._values.get("heartbeat_timeout")
        return result

    @builtins.property
    def lifecycle_hook_name(self) -> typing.Optional[builtins.str]:
        """Name of the lifecycle hook.

        :default: - Automatically generated name.
        """
        result = self._values.get("lifecycle_hook_name")
        return result

    @builtins.property
    def notification_metadata(self) -> typing.Optional[builtins.str]:
        """Additional data to pass to the lifecycle hook target.

        :default: - No metadata.
        """
        result = self._values.get("notification_metadata")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role that allows publishing to the notification target.

        :default: - A role is automatically created.
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def auto_scaling_group(self) -> IAutoScalingGroup:
        """The AutoScalingGroup to add the lifecycle hook to."""
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecycleHookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.LifecycleHookTargetConfig",
    jsii_struct_bases=[],
    name_mapping={"notification_target_arn": "notificationTargetArn"},
)
class LifecycleHookTargetConfig:
    def __init__(self, *, notification_target_arn: builtins.str) -> None:
        """Properties to add the target to a lifecycle hook.

        :param notification_target_arn: The ARN to use as the notification target.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "notification_target_arn": notification_target_arn,
        }

    @builtins.property
    def notification_target_arn(self) -> builtins.str:
        """The ARN to use as the notification target."""
        result = self._values.get("notification_target_arn")
        assert result is not None, "Required property 'notification_target_arn' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecycleHookTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.LifecycleTransition")
class LifecycleTransition(enum.Enum):
    """What instance transition to attach the hook to."""

    INSTANCE_LAUNCHING = "INSTANCE_LAUNCHING"
    """Execute the hook when an instance is about to be added."""
    INSTANCE_TERMINATING = "INSTANCE_TERMINATING"
    """Execute the hook when an instance is about to be terminated."""


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.MetricAggregationType")
class MetricAggregationType(enum.Enum):
    """How the scaling metric is going to be aggregated."""

    AVERAGE = "AVERAGE"
    """Average."""
    MINIMUM = "MINIMUM"
    """Minimum."""
    MAXIMUM = "MAXIMUM"
    """Maximum."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.MetricTargetTrackingProps",
    jsii_struct_bases=[BaseTargetTrackingProps],
    name_mapping={
        "cooldown": "cooldown",
        "disable_scale_in": "disableScaleIn",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "metric": "metric",
        "target_value": "targetValue",
    },
)
class MetricTargetTrackingProps(BaseTargetTrackingProps):
    def __init__(
        self,
        *,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        target_value: jsii.Number,
    ) -> None:
        """Properties for enabling tracking of an arbitrary metric.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metric": metric,
            "target_value": target_value,
        }
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        :default: false
        """
        result = self._values.get("disable_scale_in")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: - Same as the cooldown.
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to track.

        The metric must represent a utilization, so that if it's higher than the
        target value, your ASG should scale out, and if it's lower it should
        scale in.
        """
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return result

    @builtins.property
    def target_value(self) -> jsii.Number:
        """Value to keep the metric around."""
        result = self._values.get("target_value")
        assert result is not None, "Required property 'target_value' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricTargetTrackingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.Monitoring")
class Monitoring(enum.Enum):
    """The monitoring mode for instances launched in an autoscaling group."""

    BASIC = "BASIC"
    """Generates metrics every 5 minutes."""
    DETAILED = "DETAILED"
    """Generates metrics every minute."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.NetworkUtilizationScalingProps",
    jsii_struct_bases=[BaseTargetTrackingProps],
    name_mapping={
        "cooldown": "cooldown",
        "disable_scale_in": "disableScaleIn",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "target_bytes_per_second": "targetBytesPerSecond",
    },
)
class NetworkUtilizationScalingProps(BaseTargetTrackingProps):
    def __init__(
        self,
        *,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        target_bytes_per_second: jsii.Number,
    ) -> None:
        """Properties for enabling scaling based on network utilization.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_bytes_per_second": target_bytes_per_second,
        }
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        :default: false
        """
        result = self._values.get("disable_scale_in")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: - Same as the cooldown.
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def target_bytes_per_second(self) -> jsii.Number:
        """Target average bytes/seconds on each instance."""
        result = self._values.get("target_bytes_per_second")
        assert result is not None, "Required property 'target_bytes_per_second' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkUtilizationScalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.NotificationConfiguration",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic", "scaling_events": "scalingEvents"},
)
class NotificationConfiguration:
    def __init__(
        self,
        *,
        topic: aws_cdk.aws_sns.ITopic,
        scaling_events: typing.Optional["ScalingEvents"] = None,
    ) -> None:
        """AutoScalingGroup fleet change notifications configurations.

        You can configure AutoScaling to send an SNS notification whenever your Auto Scaling group scales.

        :param topic: SNS topic to send notifications about fleet scaling events.
        :param scaling_events: Which fleet scaling events triggers a notification. Default: ScalingEvents.ALL
        """
        self._values: typing.Dict[str, typing.Any] = {
            "topic": topic,
        }
        if scaling_events is not None:
            self._values["scaling_events"] = scaling_events

    @builtins.property
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        """SNS topic to send notifications about fleet scaling events."""
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return result

    @builtins.property
    def scaling_events(self) -> typing.Optional["ScalingEvents"]:
        """Which fleet scaling events triggers a notification.

        :default: ScalingEvents.ALL
        """
        result = self._values.get("scaling_events")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.PredefinedMetric")
class PredefinedMetric(enum.Enum):
    """One of the predefined autoscaling metrics."""

    ASG_AVERAGE_CPU_UTILIZATION = "ASG_AVERAGE_CPU_UTILIZATION"
    """Average CPU utilization of the Auto Scaling group."""
    ASG_AVERAGE_NETWORK_IN = "ASG_AVERAGE_NETWORK_IN"
    """Average number of bytes received on all network interfaces by the Auto Scaling group."""
    ASG_AVERAGE_NETWORK_OUT = "ASG_AVERAGE_NETWORK_OUT"
    """Average number of bytes sent out on all network interfaces by the Auto Scaling group."""
    ALB_REQUEST_COUNT_PER_TARGET = "ALB_REQUEST_COUNT_PER_TARGET"
    """Number of requests completed per target in an Application Load Balancer target group.

    Specify the ALB to look at in the ``resourceLabel`` field.
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.RenderSignalsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "desired_capacity": "desiredCapacity",
        "min_capacity": "minCapacity",
    },
)
class RenderSignalsOptions:
    def __init__(
        self,
        *,
        desired_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Input for Signals.renderCreationPolicy.

        :param desired_capacity: The desiredCapacity of the ASG. Default: - desired capacity not configured
        :param min_capacity: The minSize of the ASG. Default: - minCapacity not configured
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """The desiredCapacity of the ASG.

        :default: - desired capacity not configured
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """The minSize of the ASG.

        :default: - minCapacity not configured
        """
        result = self._values.get("min_capacity")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderSignalsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.RequestCountScalingProps",
    jsii_struct_bases=[BaseTargetTrackingProps],
    name_mapping={
        "cooldown": "cooldown",
        "disable_scale_in": "disableScaleIn",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "target_requests_per_minute": "targetRequestsPerMinute",
        "target_requests_per_second": "targetRequestsPerSecond",
    },
)
class RequestCountScalingProps(BaseTargetTrackingProps):
    def __init__(
        self,
        *,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        target_requests_per_minute: typing.Optional[jsii.Number] = None,
        target_requests_per_second: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for enabling scaling based on request/second.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_requests_per_minute: Target average requests/minute on each instance. Default: - Specify exactly one of 'targetRequestsPerSecond' and 'targetRequestsPerSecond'
        :param target_requests_per_second: (deprecated) Target average requests/seconds on each instance. Default: - Specify exactly one of 'targetRequestsPerSecond' and 'targetRequestsPerSecond'
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if target_requests_per_minute is not None:
            self._values["target_requests_per_minute"] = target_requests_per_minute
        if target_requests_per_second is not None:
            self._values["target_requests_per_second"] = target_requests_per_second

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        :default: false
        """
        result = self._values.get("disable_scale_in")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: - Same as the cooldown.
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def target_requests_per_minute(self) -> typing.Optional[jsii.Number]:
        """Target average requests/minute on each instance.

        :default: - Specify exactly one of 'targetRequestsPerSecond' and 'targetRequestsPerSecond'
        """
        result = self._values.get("target_requests_per_minute")
        return result

    @builtins.property
    def target_requests_per_second(self) -> typing.Optional[jsii.Number]:
        """(deprecated) Target average requests/seconds on each instance.

        :default: - Specify exactly one of 'targetRequestsPerSecond' and 'targetRequestsPerSecond'

        :deprecated: Use 'targetRequestsPerMinute' instead

        :stability: deprecated
        """
        result = self._values.get("target_requests_per_second")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RequestCountScalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.RollingUpdateConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "max_batch_size": "maxBatchSize",
        "min_instances_in_service": "minInstancesInService",
        "min_successful_instances_percent": "minSuccessfulInstancesPercent",
        "pause_time": "pauseTime",
        "suspend_processes": "suspendProcesses",
        "wait_on_resource_signals": "waitOnResourceSignals",
    },
)
class RollingUpdateConfiguration:
    def __init__(
        self,
        *,
        max_batch_size: typing.Optional[jsii.Number] = None,
        min_instances_in_service: typing.Optional[jsii.Number] = None,
        min_successful_instances_percent: typing.Optional[jsii.Number] = None,
        pause_time: typing.Optional[aws_cdk.core.Duration] = None,
        suspend_processes: typing.Optional[typing.List["ScalingProcess"]] = None,
        wait_on_resource_signals: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Additional settings when a rolling update is selected.

        :param max_batch_size: The maximum number of instances that AWS CloudFormation updates at once. Default: 1
        :param min_instances_in_service: The minimum number of instances that must be in service before more instances are replaced. This number affects the speed of the replacement. Default: 0
        :param min_successful_instances_percent: The percentage of instances that must signal success for an update to succeed. If an instance doesn't send a signal within the time specified in the pauseTime property, AWS CloudFormation assumes that the instance wasn't updated. This number affects the success of the replacement. If you specify this property, you must also enable the waitOnResourceSignals and pauseTime properties. Default: 100
        :param pause_time: The pause time after making a change to a batch of instances. This is intended to give those instances time to start software applications. Specify PauseTime in the ISO8601 duration format (in the format PT#H#M#S, where each # is the number of hours, minutes, and seconds, respectively). The maximum PauseTime is one hour (PT1H). Default: Duration.minutes(5) if the waitOnResourceSignals property is true, otherwise 0
        :param suspend_processes: Specifies the Auto Scaling processes to suspend during a stack update. Suspending processes prevents Auto Scaling from interfering with a stack update. Default: HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
        :param wait_on_resource_signals: Specifies whether the Auto Scaling group waits on signals from new instances during an update. AWS CloudFormation must receive a signal from each new instance within the specified PauseTime before continuing the update. To have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling rolling updates sample template. Default: true if you specified the minSuccessfulInstancesPercent property, false otherwise
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if min_instances_in_service is not None:
            self._values["min_instances_in_service"] = min_instances_in_service
        if min_successful_instances_percent is not None:
            self._values["min_successful_instances_percent"] = min_successful_instances_percent
        if pause_time is not None:
            self._values["pause_time"] = pause_time
        if suspend_processes is not None:
            self._values["suspend_processes"] = suspend_processes
        if wait_on_resource_signals is not None:
            self._values["wait_on_resource_signals"] = wait_on_resource_signals

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        """The maximum number of instances that AWS CloudFormation updates at once.

        :default: 1
        """
        result = self._values.get("max_batch_size")
        return result

    @builtins.property
    def min_instances_in_service(self) -> typing.Optional[jsii.Number]:
        """The minimum number of instances that must be in service before more instances are replaced.

        This number affects the speed of the replacement.

        :default: 0
        """
        result = self._values.get("min_instances_in_service")
        return result

    @builtins.property
    def min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """The percentage of instances that must signal success for an update to succeed.

        If an instance doesn't send a signal within the time specified in the
        pauseTime property, AWS CloudFormation assumes that the instance wasn't
        updated.

        This number affects the success of the replacement.

        If you specify this property, you must also enable the
        waitOnResourceSignals and pauseTime properties.

        :default: 100
        """
        result = self._values.get("min_successful_instances_percent")
        return result

    @builtins.property
    def pause_time(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The pause time after making a change to a batch of instances.

        This is intended to give those instances time to start software applications.

        Specify PauseTime in the ISO8601 duration format (in the format
        PT#H#M#S, where each # is the number of hours, minutes, and seconds,
        respectively). The maximum PauseTime is one hour (PT1H).

        :default: Duration.minutes(5) if the waitOnResourceSignals property is true, otherwise 0
        """
        result = self._values.get("pause_time")
        return result

    @builtins.property
    def suspend_processes(self) -> typing.Optional[typing.List["ScalingProcess"]]:
        """Specifies the Auto Scaling processes to suspend during a stack update.

        Suspending processes prevents Auto Scaling from interfering with a stack
        update.

        :default: HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
        """
        result = self._values.get("suspend_processes")
        return result

    @builtins.property
    def wait_on_resource_signals(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the Auto Scaling group waits on signals from new instances during an update.

        AWS CloudFormation must receive a signal from each new instance within
        the specified PauseTime before continuing the update.

        To have instances wait for an Elastic Load Balancing health check before
        they signal success, add a health-check verification by using the
        cfn-init helper script. For an example, see the verify_instance_health
        command in the Auto Scaling rolling updates sample template.

        :default: true if you specified the minSuccessfulInstancesPercent property, false otherwise
        """
        result = self._values.get("wait_on_resource_signals")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RollingUpdateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.RollingUpdateOptions",
    jsii_struct_bases=[],
    name_mapping={
        "max_batch_size": "maxBatchSize",
        "min_instances_in_service": "minInstancesInService",
        "min_success_percentage": "minSuccessPercentage",
        "pause_time": "pauseTime",
        "suspend_processes": "suspendProcesses",
        "wait_on_resource_signals": "waitOnResourceSignals",
    },
)
class RollingUpdateOptions:
    def __init__(
        self,
        *,
        max_batch_size: typing.Optional[jsii.Number] = None,
        min_instances_in_service: typing.Optional[jsii.Number] = None,
        min_success_percentage: typing.Optional[jsii.Number] = None,
        pause_time: typing.Optional[aws_cdk.core.Duration] = None,
        suspend_processes: typing.Optional[typing.List["ScalingProcess"]] = None,
        wait_on_resource_signals: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Options for customizing the rolling update.

        :param max_batch_size: The maximum number of instances that AWS CloudFormation updates at once. This number affects the speed of the replacement. Default: 1
        :param min_instances_in_service: The minimum number of instances that must be in service before more instances are replaced. This number affects the speed of the replacement. Default: 0
        :param min_success_percentage: The percentage of instances that must signal success for the update to succeed. Default: - The ``minSuccessPercentage`` configured for ``signals`` on the AutoScalingGroup
        :param pause_time: The pause time after making a change to a batch of instances. Default: - The ``timeout`` configured for ``signals`` on the AutoScalingGroup
        :param suspend_processes: Specifies the Auto Scaling processes to suspend during a stack update. Suspending processes prevents Auto Scaling from interfering with a stack update. Default: HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
        :param wait_on_resource_signals: Specifies whether the Auto Scaling group waits on signals from new instances during an update. Default: true if you configured ``signals`` on the AutoScalingGroup, false otherwise
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if min_instances_in_service is not None:
            self._values["min_instances_in_service"] = min_instances_in_service
        if min_success_percentage is not None:
            self._values["min_success_percentage"] = min_success_percentage
        if pause_time is not None:
            self._values["pause_time"] = pause_time
        if suspend_processes is not None:
            self._values["suspend_processes"] = suspend_processes
        if wait_on_resource_signals is not None:
            self._values["wait_on_resource_signals"] = wait_on_resource_signals

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        """The maximum number of instances that AWS CloudFormation updates at once.

        This number affects the speed of the replacement.

        :default: 1
        """
        result = self._values.get("max_batch_size")
        return result

    @builtins.property
    def min_instances_in_service(self) -> typing.Optional[jsii.Number]:
        """The minimum number of instances that must be in service before more instances are replaced.

        This number affects the speed of the replacement.

        :default: 0
        """
        result = self._values.get("min_instances_in_service")
        return result

    @builtins.property
    def min_success_percentage(self) -> typing.Optional[jsii.Number]:
        """The percentage of instances that must signal success for the update to succeed.

        :default: - The ``minSuccessPercentage`` configured for ``signals`` on the AutoScalingGroup
        """
        result = self._values.get("min_success_percentage")
        return result

    @builtins.property
    def pause_time(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The pause time after making a change to a batch of instances.

        :default: - The ``timeout`` configured for ``signals`` on the AutoScalingGroup
        """
        result = self._values.get("pause_time")
        return result

    @builtins.property
    def suspend_processes(self) -> typing.Optional[typing.List["ScalingProcess"]]:
        """Specifies the Auto Scaling processes to suspend during a stack update.

        Suspending processes prevents Auto Scaling from interfering with a stack
        update.

        :default: HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
        """
        result = self._values.get("suspend_processes")
        return result

    @builtins.property
    def wait_on_resource_signals(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the Auto Scaling group waits on signals from new instances during an update.

        :default: true if you configured ``signals`` on the AutoScalingGroup, false otherwise
        """
        result = self._values.get("wait_on_resource_signals")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RollingUpdateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.ScalingEvent")
class ScalingEvent(enum.Enum):
    """Fleet scaling events."""

    INSTANCE_LAUNCH = "INSTANCE_LAUNCH"
    """Notify when an instance was launched."""
    INSTANCE_TERMINATE = "INSTANCE_TERMINATE"
    """Notify when an instance was terminated."""
    INSTANCE_TERMINATE_ERROR = "INSTANCE_TERMINATE_ERROR"
    """Notify when an instance failed to terminate."""
    INSTANCE_LAUNCH_ERROR = "INSTANCE_LAUNCH_ERROR"
    """Notify when an instance failed to launch."""
    TEST_NOTIFICATION = "TEST_NOTIFICATION"
    """Send a test notification to the topic."""


class ScalingEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.ScalingEvents",
):
    """A list of ScalingEvents, you can use one of the predefined lists, such as ScalingEvents.ERRORS or create a custom group by instantiating a ``NotificationTypes`` object, e.g: ``new NotificationTypes(``NotificationType.INSTANCE_LAUNCH``)``."""

    def __init__(self, *types: ScalingEvent) -> None:
        """
        :param types: -
        """
        jsii.create(ScalingEvents, self, [*types])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ALL")
    def ALL(cls) -> "ScalingEvents":
        """All fleet scaling events."""
        return jsii.sget(cls, "ALL")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ERRORS")
    def ERRORS(cls) -> "ScalingEvents":
        """Fleet scaling errors."""
        return jsii.sget(cls, "ERRORS")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="LAUNCH_EVENTS")
    def LAUNCH_EVENTS(cls) -> "ScalingEvents":
        """Fleet scaling launch events."""
        return jsii.sget(cls, "LAUNCH_EVENTS")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.ScalingInterval",
    jsii_struct_bases=[],
    name_mapping={"change": "change", "lower": "lower", "upper": "upper"},
)
class ScalingInterval:
    def __init__(
        self,
        *,
        change: jsii.Number,
        lower: typing.Optional[jsii.Number] = None,
        upper: typing.Optional[jsii.Number] = None,
    ) -> None:
        """A range of metric values in which to apply a certain scaling operation.

        :param change: The capacity adjustment to apply in this interval. The number is interpreted differently based on AdjustmentType: - ChangeInCapacity: add the adjustment to the current capacity. The number can be positive or negative. - PercentChangeInCapacity: add or remove the given percentage of the current capacity to itself. The number can be in the range [-100..100]. - ExactCapacity: set the capacity to this number. The number must be positive.
        :param lower: The lower bound of the interval. The scaling adjustment will be applied if the metric is higher than this value. Default: Threshold automatically derived from neighbouring intervals
        :param upper: The upper bound of the interval. The scaling adjustment will be applied if the metric is lower than this value. Default: Threshold automatically derived from neighbouring intervals
        """
        self._values: typing.Dict[str, typing.Any] = {
            "change": change,
        }
        if lower is not None:
            self._values["lower"] = lower
        if upper is not None:
            self._values["upper"] = upper

    @builtins.property
    def change(self) -> jsii.Number:
        """The capacity adjustment to apply in this interval.

        The number is interpreted differently based on AdjustmentType:

        - ChangeInCapacity: add the adjustment to the current capacity.
          The number can be positive or negative.
        - PercentChangeInCapacity: add or remove the given percentage of the current
          capacity to itself. The number can be in the range [-100..100].
        - ExactCapacity: set the capacity to this number. The number must
          be positive.
        """
        result = self._values.get("change")
        assert result is not None, "Required property 'change' is missing"
        return result

    @builtins.property
    def lower(self) -> typing.Optional[jsii.Number]:
        """The lower bound of the interval.

        The scaling adjustment will be applied if the metric is higher than this value.

        :default: Threshold automatically derived from neighbouring intervals
        """
        result = self._values.get("lower")
        return result

    @builtins.property
    def upper(self) -> typing.Optional[jsii.Number]:
        """The upper bound of the interval.

        The scaling adjustment will be applied if the metric is lower than this value.

        :default: Threshold automatically derived from neighbouring intervals
        """
        result = self._values.get("upper")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalingInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.ScalingProcess")
class ScalingProcess(enum.Enum):
    LAUNCH = "LAUNCH"
    TERMINATE = "TERMINATE"
    HEALTH_CHECK = "HEALTH_CHECK"
    REPLACE_UNHEALTHY = "REPLACE_UNHEALTHY"
    AZ_REBALANCE = "AZ_REBALANCE"
    ALARM_NOTIFICATION = "ALARM_NOTIFICATION"
    SCHEDULED_ACTIONS = "SCHEDULED_ACTIONS"
    ADD_TO_LOAD_BALANCER = "ADD_TO_LOAD_BALANCER"


class Schedule(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-autoscaling.Schedule",
):
    """Schedule for scheduled scaling actions."""

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
    ) -> "Schedule":
        """Create a schedule from a set of cron fields.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        """
        options = CronOptions(
            day=day, hour=hour, minute=minute, month=month, week_day=week_day
        )

        return jsii.sinvoke(cls, "cron", [options])

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(cls, expression: builtins.str) -> "Schedule":
        """Construct a schedule from a literal schedule expression.

        :param expression: The expression to use. Must be in a format that AutoScaling will recognize

        :see: http://crontab.org/
        """
        return jsii.sinvoke(cls, "expression", [expression])

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


class ScheduledAction(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.ScheduledAction",
):
    """Define a scheduled scaling action."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auto_scaling_group: IAutoScalingGroup,
        schedule: Schedule,
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param auto_scaling_group: The AutoScalingGroup to apply the scheduled actions to.
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props = ScheduledActionProps(
            auto_scaling_group=auto_scaling_group,
            schedule=schedule,
            desired_capacity=desired_capacity,
            end_time=end_time,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            start_time=start_time,
        )

        jsii.create(ScheduledAction, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.ScheduledActionProps",
    jsii_struct_bases=[BasicScheduledActionProps],
    name_mapping={
        "schedule": "schedule",
        "desired_capacity": "desiredCapacity",
        "end_time": "endTime",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "start_time": "startTime",
        "auto_scaling_group": "autoScalingGroup",
    },
)
class ScheduledActionProps(BasicScheduledActionProps):
    def __init__(
        self,
        *,
        schedule: Schedule,
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
        auto_scaling_group: IAutoScalingGroup,
    ) -> None:
        """Properties for a scheduled action on an AutoScalingGroup.

        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        :param auto_scaling_group: The AutoScalingGroup to apply the scheduled actions to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "schedule": schedule,
            "auto_scaling_group": auto_scaling_group,
        }
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if end_time is not None:
            self._values["end_time"] = end_time
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def schedule(self) -> Schedule:
        """When to perform this action.

        Supports cron expressions.

        For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            08 * * ?
        """
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return result

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """The new desired capacity.

        At the scheduled time, set the desired capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        :default: - No new desired capacity.
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def end_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action expires.

        :default: - The rule never expires.
        """
        result = self._values.get("end_time")
        return result

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """The new maximum capacity.

        At the scheduled time, set the maximum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        :default: - No new maximum capacity.
        """
        result = self._values.get("max_capacity")
        return result

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """The new minimum capacity.

        At the scheduled time, set the minimum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        :default: - No new minimum capacity.
        """
        result = self._values.get("min_capacity")
        return result

    @builtins.property
    def start_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action becomes active.

        :default: - The rule is activate immediately.
        """
        result = self._values.get("start_time")
        return result

    @builtins.property
    def auto_scaling_group(self) -> IAutoScalingGroup:
        """The AutoScalingGroup to apply the scheduled actions to."""
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Signals(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-autoscaling.Signals",
):
    """Configure whether the AutoScalingGroup waits for signals.

    If you do configure waiting for signals, you should make sure the instances
    invoke ``cfn-signal`` somewhere in their UserData to signal that they have
    started up (either successfully or unsuccessfully).

    Signals are used both during intial creation and subsequent updates.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _SignalsProxy

    def __init__(self) -> None:
        jsii.create(Signals, self, [])

    @jsii.member(jsii_name="waitForAll")
    @builtins.classmethod
    def wait_for_all(
        cls,
        *,
        min_success_percentage: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "Signals":
        """Wait for the desiredCapacity of the AutoScalingGroup amount of signals to have been received.

        If no desiredCapacity has been configured, wait for minCapacity signals intead.

        This number is used during initial creation and during replacing updates.
        During rolling updates, all updated instances must send a signal.

        :param min_success_percentage: The percentage of signals that need to be successful. If this number is less than 100, a percentage of signals may be failure signals while still succeeding the creation or update in CloudFormation. Default: 100
        :param timeout: How long to wait for the signals to be sent. This should reflect how long it takes your instances to start up (including instance start time and instance initialization time). Default: Duration.minutes(5)
        """
        options = SignalsOptions(
            min_success_percentage=min_success_percentage, timeout=timeout
        )

        return jsii.sinvoke(cls, "waitForAll", [options])

    @jsii.member(jsii_name="waitForCount")
    @builtins.classmethod
    def wait_for_count(
        cls,
        count: jsii.Number,
        *,
        min_success_percentage: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "Signals":
        """Wait for a specific amount of signals to have been received.

        You should send one signal per instance, so this represents the number of
        instances to wait for.

        This number is used during initial creation and during replacing updates.
        During rolling updates, all updated instances must send a signal.

        :param count: -
        :param min_success_percentage: The percentage of signals that need to be successful. If this number is less than 100, a percentage of signals may be failure signals while still succeeding the creation or update in CloudFormation. Default: 100
        :param timeout: How long to wait for the signals to be sent. This should reflect how long it takes your instances to start up (including instance start time and instance initialization time). Default: Duration.minutes(5)
        """
        options = SignalsOptions(
            min_success_percentage=min_success_percentage, timeout=timeout
        )

        return jsii.sinvoke(cls, "waitForCount", [count, options])

    @jsii.member(jsii_name="waitForMinCapacity")
    @builtins.classmethod
    def wait_for_min_capacity(
        cls,
        *,
        min_success_percentage: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "Signals":
        """Wait for the minCapacity of the AutoScalingGroup amount of signals to have been received.

        This number is used during initial creation and during replacing updates.
        During rolling updates, all updated instances must send a signal.

        :param min_success_percentage: The percentage of signals that need to be successful. If this number is less than 100, a percentage of signals may be failure signals while still succeeding the creation or update in CloudFormation. Default: 100
        :param timeout: How long to wait for the signals to be sent. This should reflect how long it takes your instances to start up (including instance start time and instance initialization time). Default: Duration.minutes(5)
        """
        options = SignalsOptions(
            min_success_percentage=min_success_percentage, timeout=timeout
        )

        return jsii.sinvoke(cls, "waitForMinCapacity", [options])

    @jsii.member(jsii_name="doRender")
    def _do_render(
        self,
        options: "SignalsOptions",
        count: typing.Optional[jsii.Number] = None,
    ) -> aws_cdk.core.CfnCreationPolicy:
        """Helper to render the actual creation policy, as the logic between them is quite similar.

        :param options: -
        :param count: -
        """
        return jsii.invoke(self, "doRender", [options, count])

    @jsii.member(jsii_name="renderCreationPolicy")
    @abc.abstractmethod
    def render_creation_policy(
        self,
        *,
        desired_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
    ) -> aws_cdk.core.CfnCreationPolicy:
        """Render the ASG's CreationPolicy.

        :param desired_capacity: The desiredCapacity of the ASG. Default: - desired capacity not configured
        :param min_capacity: The minSize of the ASG. Default: - minCapacity not configured
        """
        ...


class _SignalsProxy(Signals):
    @jsii.member(jsii_name="renderCreationPolicy")
    def render_creation_policy(
        self,
        *,
        desired_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
    ) -> aws_cdk.core.CfnCreationPolicy:
        """Render the ASG's CreationPolicy.

        :param desired_capacity: The desiredCapacity of the ASG. Default: - desired capacity not configured
        :param min_capacity: The minSize of the ASG. Default: - minCapacity not configured
        """
        render_options = RenderSignalsOptions(
            desired_capacity=desired_capacity, min_capacity=min_capacity
        )

        return jsii.invoke(self, "renderCreationPolicy", [render_options])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.SignalsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "min_success_percentage": "minSuccessPercentage",
        "timeout": "timeout",
    },
)
class SignalsOptions:
    def __init__(
        self,
        *,
        min_success_percentage: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Customization options for Signal handling.

        :param min_success_percentage: The percentage of signals that need to be successful. If this number is less than 100, a percentage of signals may be failure signals while still succeeding the creation or update in CloudFormation. Default: 100
        :param timeout: How long to wait for the signals to be sent. This should reflect how long it takes your instances to start up (including instance start time and instance initialization time). Default: Duration.minutes(5)
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if min_success_percentage is not None:
            self._values["min_success_percentage"] = min_success_percentage
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def min_success_percentage(self) -> typing.Optional[jsii.Number]:
        """The percentage of signals that need to be successful.

        If this number is less than 100, a percentage of signals may be failure
        signals while still succeeding the creation or update in CloudFormation.

        :default: 100
        """
        result = self._values.get("min_success_percentage")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """How long to wait for the signals to be sent.

        This should reflect how long it takes your instances to start up
        (including instance start time and instance initialization time).

        :default: Duration.minutes(5)
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignalsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StepScalingAction(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.StepScalingAction",
):
    """Define a step scaling action.

    This kind of scaling policy adjusts the target capacity in configurable
    steps. The size of the step is configurable based on the metric's distance
    to its alarm threshold.

    This Action must be used as the target of a CloudWatch alarm to take effect.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auto_scaling_group: IAutoScalingGroup,
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        metric_aggregation_type: typing.Optional[MetricAggregationType] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param auto_scaling_group: The auto scaling group.
        :param adjustment_type: How the adjustment numbers are interpreted. Default: ChangeInCapacity
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: The default cooldown configured on the AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. Default: Average
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = StepScalingActionProps(
            auto_scaling_group=auto_scaling_group,
            adjustment_type=adjustment_type,
            cooldown=cooldown,
            estimated_instance_warmup=estimated_instance_warmup,
            metric_aggregation_type=metric_aggregation_type,
            min_adjustment_magnitude=min_adjustment_magnitude,
        )

        jsii.create(StepScalingAction, self, [scope, id, props])

    @jsii.member(jsii_name="addAdjustment")
    def add_adjustment(
        self,
        *,
        adjustment: jsii.Number,
        lower_bound: typing.Optional[jsii.Number] = None,
        upper_bound: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Add an adjusment interval to the ScalingAction.

        :param adjustment: What number to adjust the capacity with. The number is interpeted as an added capacity, a new fixed capacity or an added percentage depending on the AdjustmentType value of the StepScalingPolicy. Can be positive or negative.
        :param lower_bound: Lower bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is higher than this value. Default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        :param upper_bound: Upper bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is lower than this value. Default: +Infinity
        """
        adjustment_ = AdjustmentTier(
            adjustment=adjustment, lower_bound=lower_bound, upper_bound=upper_bound
        )

        return jsii.invoke(self, "addAdjustment", [adjustment_])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> builtins.str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.StepScalingActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group": "autoScalingGroup",
        "adjustment_type": "adjustmentType",
        "cooldown": "cooldown",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "metric_aggregation_type": "metricAggregationType",
        "min_adjustment_magnitude": "minAdjustmentMagnitude",
    },
)
class StepScalingActionProps:
    def __init__(
        self,
        *,
        auto_scaling_group: IAutoScalingGroup,
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        metric_aggregation_type: typing.Optional[MetricAggregationType] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for a scaling policy.

        :param auto_scaling_group: The auto scaling group.
        :param adjustment_type: How the adjustment numbers are interpreted. Default: ChangeInCapacity
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: The default cooldown configured on the AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. Default: Average
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        self._values: typing.Dict[str, typing.Any] = {
            "auto_scaling_group": auto_scaling_group,
        }
        if adjustment_type is not None:
            self._values["adjustment_type"] = adjustment_type
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if metric_aggregation_type is not None:
            self._values["metric_aggregation_type"] = metric_aggregation_type
        if min_adjustment_magnitude is not None:
            self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @builtins.property
    def auto_scaling_group(self) -> IAutoScalingGroup:
        """The auto scaling group."""
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return result

    @builtins.property
    def adjustment_type(self) -> typing.Optional[AdjustmentType]:
        """How the adjustment numbers are interpreted.

        :default: ChangeInCapacity
        """
        result = self._values.get("adjustment_type")
        return result

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: The default cooldown configured on the AutoScalingGroup
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: Same as the cooldown
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def metric_aggregation_type(self) -> typing.Optional[MetricAggregationType]:
        """The aggregation type for the CloudWatch metrics.

        :default: Average
        """
        result = self._values.get("metric_aggregation_type")
        return result

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        :default: No minimum scaling effect
        """
        result = self._values.get("min_adjustment_magnitude")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepScalingActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StepScalingPolicy(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicy",
):
    """Define a acaling strategy which scales depending on absolute values of some metric.

    You can specify the scaling behavior for various values of the metric.

    Implemented using one or more CloudWatch alarms and Step Scaling Policies.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auto_scaling_group: IAutoScalingGroup,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        scaling_steps: typing.List[ScalingInterval],
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param auto_scaling_group: The auto scaling group.
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = StepScalingPolicyProps(
            auto_scaling_group=auto_scaling_group,
            metric=metric,
            scaling_steps=scaling_steps,
            adjustment_type=adjustment_type,
            cooldown=cooldown,
            estimated_instance_warmup=estimated_instance_warmup,
            min_adjustment_magnitude=min_adjustment_magnitude,
        )

        jsii.create(StepScalingPolicy, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lowerAction")
    def lower_action(self) -> typing.Optional[StepScalingAction]:
        return jsii.get(self, "lowerAction")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lowerAlarm")
    def lower_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "lowerAlarm")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="upperAction")
    def upper_action(self) -> typing.Optional[StepScalingAction]:
        return jsii.get(self, "upperAction")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="upperAlarm")
    def upper_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "upperAlarm")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicyProps",
    jsii_struct_bases=[BasicStepScalingPolicyProps],
    name_mapping={
        "metric": "metric",
        "scaling_steps": "scalingSteps",
        "adjustment_type": "adjustmentType",
        "cooldown": "cooldown",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "min_adjustment_magnitude": "minAdjustmentMagnitude",
        "auto_scaling_group": "autoScalingGroup",
    },
)
class StepScalingPolicyProps(BasicStepScalingPolicyProps):
    def __init__(
        self,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        scaling_steps: typing.List[ScalingInterval],
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
        auto_scaling_group: IAutoScalingGroup,
    ) -> None:
        """
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        :param auto_scaling_group: The auto scaling group.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metric": metric,
            "scaling_steps": scaling_steps,
            "auto_scaling_group": auto_scaling_group,
        }
        if adjustment_type is not None:
            self._values["adjustment_type"] = adjustment_type
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if min_adjustment_magnitude is not None:
            self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @builtins.property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to scale on."""
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return result

    @builtins.property
    def scaling_steps(self) -> typing.List[ScalingInterval]:
        """The intervals for scaling.

        Maps a range of metric values to a particular scaling behavior.
        """
        result = self._values.get("scaling_steps")
        assert result is not None, "Required property 'scaling_steps' is missing"
        return result

    @builtins.property
    def adjustment_type(self) -> typing.Optional[AdjustmentType]:
        """How the adjustment numbers inside 'intervals' are interpreted.

        :default: ChangeInCapacity
        """
        result = self._values.get("adjustment_type")
        return result

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Grace period after scaling activity.

        :default: Default cooldown period on your AutoScalingGroup
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: Same as the cooldown
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        :default: No minimum scaling effect
        """
        result = self._values.get("min_adjustment_magnitude")
        return result

    @builtins.property
    def auto_scaling_group(self) -> IAutoScalingGroup:
        """The auto scaling group."""
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepScalingPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TargetTrackingScalingPolicy(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicy",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        auto_scaling_group: IAutoScalingGroup,
        target_value: jsii.Number,
        custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric] = None,
        predefined_metric: typing.Optional[PredefinedMetric] = None,
        resource_label: typing.Optional[builtins.str] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param auto_scaling_group: 
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metric.
        :param resource_label: The resource label associated with the predefined metric. Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the format should be: app///targetgroup// Default: - No resource label.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = TargetTrackingScalingPolicyProps(
            auto_scaling_group=auto_scaling_group,
            target_value=target_value,
            custom_metric=custom_metric,
            predefined_metric=predefined_metric,
            resource_label=resource_label,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        jsii.create(TargetTrackingScalingPolicy, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> builtins.str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicyProps",
    jsii_struct_bases=[BasicTargetTrackingScalingPolicyProps],
    name_mapping={
        "cooldown": "cooldown",
        "disable_scale_in": "disableScaleIn",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "target_value": "targetValue",
        "custom_metric": "customMetric",
        "predefined_metric": "predefinedMetric",
        "resource_label": "resourceLabel",
        "auto_scaling_group": "autoScalingGroup",
    },
)
class TargetTrackingScalingPolicyProps(BasicTargetTrackingScalingPolicyProps):
    def __init__(
        self,
        *,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        target_value: jsii.Number,
        custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric] = None,
        predefined_metric: typing.Optional[PredefinedMetric] = None,
        resource_label: typing.Optional[builtins.str] = None,
        auto_scaling_group: IAutoScalingGroup,
    ) -> None:
        """Properties for a concrete TargetTrackingPolicy.

        Adds the scalingTarget.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metric.
        :param resource_label: The resource label associated with the predefined metric. Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the format should be: app///targetgroup// Default: - No resource label.
        :param auto_scaling_group: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_value": target_value,
            "auto_scaling_group": auto_scaling_group,
        }
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if disable_scale_in is not None:
            self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if custom_metric is not None:
            self._values["custom_metric"] = custom_metric
        if predefined_metric is not None:
            self._values["predefined_metric"] = predefined_metric
        if resource_label is not None:
            self._values["resource_label"] = resource_label

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[builtins.bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        :default: false
        """
        result = self._values.get("disable_scale_in")
        return result

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        :default: - Same as the cooldown.
        """
        result = self._values.get("estimated_instance_warmup")
        return result

    @builtins.property
    def target_value(self) -> jsii.Number:
        """The target value for the metric."""
        result = self._values.get("target_value")
        assert result is not None, "Required property 'target_value' is missing"
        return result

    @builtins.property
    def custom_metric(self) -> typing.Optional[aws_cdk.aws_cloudwatch.IMetric]:
        """A custom metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        :default: - No custom metric.
        """
        result = self._values.get("custom_metric")
        return result

    @builtins.property
    def predefined_metric(self) -> typing.Optional[PredefinedMetric]:
        """A predefined metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        :default: - No predefined metric.
        """
        result = self._values.get("predefined_metric")
        return result

    @builtins.property
    def resource_label(self) -> typing.Optional[builtins.str]:
        """The resource label associated with the predefined metric.

        Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the
        format should be:

        app///targetgroup//

        :default: - No resource label.
        """
        result = self._values.get("resource_label")
        return result

    @builtins.property
    def auto_scaling_group(self) -> IAutoScalingGroup:
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetTrackingScalingPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UpdatePolicy(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-autoscaling.UpdatePolicy",
):
    """How existing instances should be updated."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _UpdatePolicyProxy

    def __init__(self) -> None:
        jsii.create(UpdatePolicy, self, [])

    @jsii.member(jsii_name="replacingUpdate")
    @builtins.classmethod
    def replacing_update(cls) -> "UpdatePolicy":
        """Create a new AutoScalingGroup and switch over to it."""
        return jsii.sinvoke(cls, "replacingUpdate", [])

    @jsii.member(jsii_name="rollingUpdate")
    @builtins.classmethod
    def rolling_update(
        cls,
        *,
        max_batch_size: typing.Optional[jsii.Number] = None,
        min_instances_in_service: typing.Optional[jsii.Number] = None,
        min_success_percentage: typing.Optional[jsii.Number] = None,
        pause_time: typing.Optional[aws_cdk.core.Duration] = None,
        suspend_processes: typing.Optional[typing.List[ScalingProcess]] = None,
        wait_on_resource_signals: typing.Optional[builtins.bool] = None,
    ) -> "UpdatePolicy":
        """Replace the instances in the AutoScalingGroup one by one, or in batches.

        :param max_batch_size: The maximum number of instances that AWS CloudFormation updates at once. This number affects the speed of the replacement. Default: 1
        :param min_instances_in_service: The minimum number of instances that must be in service before more instances are replaced. This number affects the speed of the replacement. Default: 0
        :param min_success_percentage: The percentage of instances that must signal success for the update to succeed. Default: - The ``minSuccessPercentage`` configured for ``signals`` on the AutoScalingGroup
        :param pause_time: The pause time after making a change to a batch of instances. Default: - The ``timeout`` configured for ``signals`` on the AutoScalingGroup
        :param suspend_processes: Specifies the Auto Scaling processes to suspend during a stack update. Suspending processes prevents Auto Scaling from interfering with a stack update. Default: HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
        :param wait_on_resource_signals: Specifies whether the Auto Scaling group waits on signals from new instances during an update. Default: true if you configured ``signals`` on the AutoScalingGroup, false otherwise
        """
        options = RollingUpdateOptions(
            max_batch_size=max_batch_size,
            min_instances_in_service=min_instances_in_service,
            min_success_percentage=min_success_percentage,
            pause_time=pause_time,
            suspend_processes=suspend_processes,
            wait_on_resource_signals=wait_on_resource_signals,
        )

        return jsii.sinvoke(cls, "rollingUpdate", [options])


class _UpdatePolicyProxy(UpdatePolicy):
    pass


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.UpdateType")
class UpdateType(enum.Enum):
    """(deprecated) The type of update to perform on instances in this AutoScalingGroup.

    :deprecated: Use UpdatePolicy instead

    :stability: deprecated
    """

    NONE = "NONE"
    """(deprecated) Don't do anything.

    :stability: deprecated
    """
    REPLACING_UPDATE = "REPLACING_UPDATE"
    """(deprecated) Replace the entire AutoScalingGroup.

    Builds a new AutoScalingGroup first, then delete the old one.

    :stability: deprecated
    """
    ROLLING_UPDATE = "ROLLING_UPDATE"
    """(deprecated) Replace the instances in the AutoScalingGroup.

    :stability: deprecated
    """


@jsii.implements(aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget, IAutoScalingGroup)
class AutoScalingGroup(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroup",
):
    """A Fleet represents a managed set of EC2 instances.

    The Fleet models a number of AutoScalingGroups, a launch configuration, a
    security group and an instance role.

    It allows adding arbitrary commands to the startup scripts of the instances
    in the fleet.

    The ASG spans the availability zones specified by vpcSubnets, falling back to
    the Vpc default strategy if not specified.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instance_type: aws_cdk.aws_ec2.InstanceType,
        machine_image: aws_cdk.aws_ec2.IMachineImage,
        vpc: aws_cdk.aws_ec2.IVpc,
        init: typing.Optional[aws_cdk.aws_ec2.CloudFormationInit] = None,
        init_options: typing.Optional[ApplyCloudFormationInitOptions] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        user_data: typing.Optional[aws_cdk.aws_ec2.UserData] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        associate_public_ip_address: typing.Optional[builtins.bool] = None,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        block_devices: typing.Optional[typing.List[BlockDevice]] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        group_metrics: typing.Optional[typing.List[GroupMetrics]] = None,
        health_check: typing.Optional[HealthCheck] = None,
        ignore_unmodified_size_properties: typing.Optional[builtins.bool] = None,
        instance_monitoring: typing.Optional[Monitoring] = None,
        key_name: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_instance_lifetime: typing.Optional[aws_cdk.core.Duration] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.List[NotificationConfiguration]] = None,
        notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
        replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number] = None,
        resource_signal_count: typing.Optional[jsii.Number] = None,
        resource_signal_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        rolling_update_configuration: typing.Optional[RollingUpdateConfiguration] = None,
        signals: typing.Optional[Signals] = None,
        spot_price: typing.Optional[builtins.str] = None,
        update_policy: typing.Optional[UpdatePolicy] = None,
        update_type: typing.Optional[UpdateType] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param instance_type: Type of instance to launch.
        :param machine_image: AMI to launch.
        :param vpc: VPC to launch these instances in.
        :param init: Apply the given CloudFormation Init configuration to the instances in the AutoScalingGroup at startup. If you specify ``init``, you must also specify ``signals`` to configure the number of instances to wait for and the timeout for waiting for the init process. Default: - no CloudFormation init
        :param init_options: Use the given options for applying CloudFormation Init. Describes the configsets to use and the timeout to wait Default: - default options
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security group to launch the instances in. Default: - A SecurityGroup will be created if none is specified.
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param auto_scaling_group_name: The name of the Auto Scaling group. This name must be unique per Region per account. Default: - Auto generated by CloudFormation
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param group_metrics: Enable monitoring for group metrics, these metrics describe the group rather than any of its instances. To report all group metrics use ``GroupMetrics.all()`` Group metrics are reported in a granularity of 1 minute at no additional charge. Default: - no group metrics will be reported
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, leave this property undefined. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: (deprecated) SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: (deprecated) Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: (deprecated) How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1 if resourceSignalTimeout is set, 0 otherwise
        :param resource_signal_timeout: (deprecated) The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5) if resourceSignalCount is set, N/A otherwise
        :param rolling_update_configuration: (deprecated) Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param signals: Configure waiting for signals during deployment. Use this to pause the CloudFormation deployment to wait for the instances in the AutoScalingGroup to report successful startup during creation and updates. The UserData script needs to invoke ``cfn-signal`` with a success or failure code after it is done setting up the instance. Without waiting for signals, the CloudFormation deployment will proceed as soon as the AutoScalingGroup has been created or updated but before the instances in the group have been started. For example, to have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling rolling updates sample template: https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/AutoScaling/AutoScalingRollingUpdates.yaml Default: - Do not wait for signals
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_policy: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: - ``UpdatePolicy.rollingUpdate()`` if using ``init``, ``UpdatePolicy.none()`` otherwise
        :param update_type: (deprecated) What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        """
        props = AutoScalingGroupProps(
            instance_type=instance_type,
            machine_image=machine_image,
            vpc=vpc,
            init=init,
            init_options=init_options,
            role=role,
            security_group=security_group,
            user_data=user_data,
            allow_all_outbound=allow_all_outbound,
            associate_public_ip_address=associate_public_ip_address,
            auto_scaling_group_name=auto_scaling_group_name,
            block_devices=block_devices,
            cooldown=cooldown,
            desired_capacity=desired_capacity,
            group_metrics=group_metrics,
            health_check=health_check,
            ignore_unmodified_size_properties=ignore_unmodified_size_properties,
            instance_monitoring=instance_monitoring,
            key_name=key_name,
            max_capacity=max_capacity,
            max_instance_lifetime=max_instance_lifetime,
            min_capacity=min_capacity,
            notifications=notifications,
            notifications_topic=notifications_topic,
            replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent,
            resource_signal_count=resource_signal_count,
            resource_signal_timeout=resource_signal_timeout,
            rolling_update_configuration=rolling_update_configuration,
            signals=signals,
            spot_price=spot_price,
            update_policy=update_policy,
            update_type=update_type,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(AutoScalingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromAutoScalingGroupName")
    @builtins.classmethod
    def from_auto_scaling_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        auto_scaling_group_name: builtins.str,
    ) -> IAutoScalingGroup:
        """
        :param scope: -
        :param id: -
        :param auto_scaling_group_name: -
        """
        return jsii.sinvoke(cls, "fromAutoScalingGroupName", [scope, id, auto_scaling_group_name])

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(
        self,
        id: builtins.str,
        *,
        lifecycle_transition: LifecycleTransition,
        notification_target: ILifecycleHookTarget,
        default_result: typing.Optional[DefaultResult] = None,
        heartbeat_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> LifecycleHook:
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        :param id: -
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props = BasicLifecycleHookProps(
            lifecycle_transition=lifecycle_transition,
            notification_target=notification_target,
            default_result=default_result,
            heartbeat_timeout=heartbeat_timeout,
            lifecycle_hook_name=lifecycle_hook_name,
            notification_metadata=notification_metadata,
            role=role,
        )

        return jsii.invoke(self, "addLifecycleHook", [id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
    ) -> None:
        """Add the security group to all instances via the launch configuration security groups array.

        :param security_group: : The security group to add.
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM role assumed by instances of this fleet.

        :param statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *commands: builtins.str) -> None:
        """Add command to the startup script of fleet instances.

        The command must be in the scripting language supported by the fleet's OS (i.e. Linux/Windows).
        Does nothing for imported ASGs.

        :param commands: -
        """
        return jsii.invoke(self, "addUserData", [*commands])

    @jsii.member(jsii_name="applyCloudFormationInit")
    def apply_cloud_formation_init(
        self,
        init: aws_cdk.aws_ec2.CloudFormationInit,
        *,
        config_sets: typing.Optional[typing.List[builtins.str]] = None,
        embed_fingerprint: typing.Optional[builtins.bool] = None,
        ignore_failures: typing.Optional[builtins.bool] = None,
        print_log: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Use a CloudFormation Init configuration at instance startup.

        This does the following:

        - Attaches the CloudFormation Init metadata to the AutoScalingGroup resource.
        - Add commands to the UserData to run ``cfn-init`` and ``cfn-signal``.
        - Update the instance's CreationPolicy to wait for ``cfn-init`` to finish
          before reporting success.

        :param init: -
        :param config_sets: ConfigSet to activate. Default: ['default']
        :param embed_fingerprint: Force instance replacement by embedding a config fingerprint. If ``true`` (the default), a hash of the config will be embedded into the UserData, so that if the config changes, the UserData changes and instances will be replaced (given an UpdatePolicy has been configured on the AutoScalingGroup). If ``false``, no such hash will be embedded, and if the CloudFormation Init config changes nothing will happen to the running instances. If a config update introduces errors, you will not notice until after the CloudFormation deployment successfully finishes and the next instance fails to launch. Default: true
        :param ignore_failures: Don't fail the instance creation when cfn-init fails. You can use this to prevent CloudFormation from rolling back when instances fail to start up, to help in debugging. Default: false
        :param print_log: Print the results of running cfn-init to the Instance System Log. By default, the output of running cfn-init is written to a log file on the instance. Set this to ``true`` to print it to the System Log (visible from the EC2 Console), ``false`` to not print it. (Be aware that the system log is refreshed at certain points in time of the instance life cycle, and successful execution may not always show up). Default: true
        """
        options = ApplyCloudFormationInitOptions(
            config_sets=config_sets,
            embed_fingerprint=embed_fingerprint,
            ignore_failures=ignore_failures,
            print_log=print_log,
        )

        return jsii.invoke(self, "applyCloudFormationInit", [init, options])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Attach to ELBv2 Application Target Group.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(
        self,
        load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer,
    ) -> None:
        """Attach to a classic load balancer.

        :param load_balancer: -
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Attach to ELBv2 Application Target Group.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(
        self,
        id: builtins.str,
        *,
        target_utilization_percent: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> TargetTrackingScalingPolicy:
        """Scale out or in to achieve a target CPU utilization.

        :param id: -
        :param target_utilization_percent: Target average CPU utilization across the task.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = CpuUtilizationScalingProps(
            target_utilization_percent=target_utilization_percent,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(
        self,
        id: builtins.str,
        *,
        target_bytes_per_second: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> TargetTrackingScalingPolicy:
        """Scale out or in to achieve a target network ingress rate.

        :param id: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(
            target_bytes_per_second=target_bytes_per_second,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(
        self,
        id: builtins.str,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        scaling_steps: typing.List[ScalingInterval],
        adjustment_type: typing.Optional[AdjustmentType] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    ) -> StepScalingPolicy:
        """Scale out or in, in response to a metric.

        :param id: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = BasicStepScalingPolicyProps(
            metric=metric,
            scaling_steps=scaling_steps,
            adjustment_type=adjustment_type,
            cooldown=cooldown,
            estimated_instance_warmup=estimated_instance_warmup,
            min_adjustment_magnitude=min_adjustment_magnitude,
        )

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(
        self,
        id: builtins.str,
        *,
        target_bytes_per_second: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> TargetTrackingScalingPolicy:
        """Scale out or in to achieve a target network egress rate.

        :param id: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(
            target_bytes_per_second=target_bytes_per_second,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(
        self,
        id: builtins.str,
        *,
        target_requests_per_minute: typing.Optional[jsii.Number] = None,
        target_requests_per_second: typing.Optional[jsii.Number] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> TargetTrackingScalingPolicy:
        """Scale out or in to achieve a target request handling rate.

        The AutoScalingGroup must have been attached to an Application Load Balancer
        in order to be able to call this.

        :param id: -
        :param target_requests_per_minute: Target average requests/minute on each instance. Default: - Specify exactly one of 'targetRequestsPerSecond' and 'targetRequestsPerSecond'
        :param target_requests_per_second: (deprecated) Target average requests/seconds on each instance. Default: - Specify exactly one of 'targetRequestsPerSecond' and 'targetRequestsPerSecond'
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = RequestCountScalingProps(
            target_requests_per_minute=target_requests_per_minute,
            target_requests_per_second=target_requests_per_second,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(
        self,
        id: builtins.str,
        *,
        schedule: Schedule,
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[datetime.datetime] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[datetime.datetime] = None,
    ) -> ScheduledAction:
        """Scale out or in based on time.

        :param id: -
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props = BasicScheduledActionProps(
            schedule=schedule,
            desired_capacity=desired_capacity,
            end_time=end_time,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            start_time=start_time,
        )

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(
        self,
        id: builtins.str,
        *,
        metric: aws_cdk.aws_cloudwatch.IMetric,
        target_value: jsii.Number,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        disable_scale_in: typing.Optional[builtins.bool] = None,
        estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> TargetTrackingScalingPolicy:
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = MetricTargetTrackingProps(
            metric=metric,
            target_value=target_value,
            cooldown=cooldown,
            disable_scale_in=disable_scale_in,
            estimated_instance_warmup=estimated_instance_warmup,
        )

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingGroupArn")
    def auto_scaling_group_arn(self) -> builtins.str:
        """Arn of the AutoScalingGroup."""
        return jsii.get(self, "autoScalingGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> builtins.str:
        """Name of the AutoScalingGroup."""
        return jsii.get(self, "autoScalingGroupName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Allows specify security group connections for instances of this fleet."""
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="osType")
    def os_type(self) -> aws_cdk.aws_ec2.OperatingSystemType:
        """The type of OS instances of this fleet are running."""
        return jsii.get(self, "osType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The IAM role assumed by instances of this fleet."""
        return jsii.get(self, "role")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userData")
    def user_data(self) -> aws_cdk.aws_ec2.UserData:
        """UserData for the instances."""
        return jsii.get(self, "userData")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxInstanceLifetime")
    def max_instance_lifetime(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum amount of time that an instance can be in service."""
        return jsii.get(self, "maxInstanceLifetime")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="spotPrice")
    def spot_price(self) -> typing.Optional[builtins.str]:
        """The maximum spot price configured for the autoscaling group.

        ``undefined``
        indicates that this group uses on-demand capacity.
        """
        return jsii.get(self, "spotPrice")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="albTargetGroup")
    def _alb_target_group(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup]:
        return jsii.get(self, "albTargetGroup")

    @_alb_target_group.setter # type: ignore
    def _alb_target_group(
        self,
        value: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup],
    ) -> None:
        jsii.set(self, "albTargetGroup", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroupProps",
    jsii_struct_bases=[CommonAutoScalingGroupProps],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "associate_public_ip_address": "associatePublicIpAddress",
        "auto_scaling_group_name": "autoScalingGroupName",
        "block_devices": "blockDevices",
        "cooldown": "cooldown",
        "desired_capacity": "desiredCapacity",
        "group_metrics": "groupMetrics",
        "health_check": "healthCheck",
        "ignore_unmodified_size_properties": "ignoreUnmodifiedSizeProperties",
        "instance_monitoring": "instanceMonitoring",
        "key_name": "keyName",
        "max_capacity": "maxCapacity",
        "max_instance_lifetime": "maxInstanceLifetime",
        "min_capacity": "minCapacity",
        "notifications": "notifications",
        "notifications_topic": "notificationsTopic",
        "replacing_update_min_successful_instances_percent": "replacingUpdateMinSuccessfulInstancesPercent",
        "resource_signal_count": "resourceSignalCount",
        "resource_signal_timeout": "resourceSignalTimeout",
        "rolling_update_configuration": "rollingUpdateConfiguration",
        "signals": "signals",
        "spot_price": "spotPrice",
        "update_policy": "updatePolicy",
        "update_type": "updateType",
        "vpc_subnets": "vpcSubnets",
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "vpc": "vpc",
        "init": "init",
        "init_options": "initOptions",
        "role": "role",
        "security_group": "securityGroup",
        "user_data": "userData",
    },
)
class AutoScalingGroupProps(CommonAutoScalingGroupProps):
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        associate_public_ip_address: typing.Optional[builtins.bool] = None,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        block_devices: typing.Optional[typing.List[BlockDevice]] = None,
        cooldown: typing.Optional[aws_cdk.core.Duration] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        group_metrics: typing.Optional[typing.List[GroupMetrics]] = None,
        health_check: typing.Optional[HealthCheck] = None,
        ignore_unmodified_size_properties: typing.Optional[builtins.bool] = None,
        instance_monitoring: typing.Optional[Monitoring] = None,
        key_name: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_instance_lifetime: typing.Optional[aws_cdk.core.Duration] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.List[NotificationConfiguration]] = None,
        notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
        replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number] = None,
        resource_signal_count: typing.Optional[jsii.Number] = None,
        resource_signal_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        rolling_update_configuration: typing.Optional[RollingUpdateConfiguration] = None,
        signals: typing.Optional[Signals] = None,
        spot_price: typing.Optional[builtins.str] = None,
        update_policy: typing.Optional[UpdatePolicy] = None,
        update_type: typing.Optional[UpdateType] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        instance_type: aws_cdk.aws_ec2.InstanceType,
        machine_image: aws_cdk.aws_ec2.IMachineImage,
        vpc: aws_cdk.aws_ec2.IVpc,
        init: typing.Optional[aws_cdk.aws_ec2.CloudFormationInit] = None,
        init_options: typing.Optional[ApplyCloudFormationInitOptions] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        user_data: typing.Optional[aws_cdk.aws_ec2.UserData] = None,
    ) -> None:
        """Properties of a Fleet.

        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param auto_scaling_group_name: The name of the Auto Scaling group. This name must be unique per Region per account. Default: - Auto generated by CloudFormation
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param group_metrics: Enable monitoring for group metrics, these metrics describe the group rather than any of its instances. To report all group metrics use ``GroupMetrics.all()`` Group metrics are reported in a granularity of 1 minute at no additional charge. Default: - no group metrics will be reported
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, leave this property undefined. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: (deprecated) SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: (deprecated) Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: (deprecated) How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1 if resourceSignalTimeout is set, 0 otherwise
        :param resource_signal_timeout: (deprecated) The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5) if resourceSignalCount is set, N/A otherwise
        :param rolling_update_configuration: (deprecated) Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param signals: Configure waiting for signals during deployment. Use this to pause the CloudFormation deployment to wait for the instances in the AutoScalingGroup to report successful startup during creation and updates. The UserData script needs to invoke ``cfn-signal`` with a success or failure code after it is done setting up the instance. Without waiting for signals, the CloudFormation deployment will proceed as soon as the AutoScalingGroup has been created or updated but before the instances in the group have been started. For example, to have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling rolling updates sample template: https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/AutoScaling/AutoScalingRollingUpdates.yaml Default: - Do not wait for signals
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_policy: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: - ``UpdatePolicy.rollingUpdate()`` if using ``init``, ``UpdatePolicy.none()`` otherwise
        :param update_type: (deprecated) What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        :param instance_type: Type of instance to launch.
        :param machine_image: AMI to launch.
        :param vpc: VPC to launch these instances in.
        :param init: Apply the given CloudFormation Init configuration to the instances in the AutoScalingGroup at startup. If you specify ``init``, you must also specify ``signals`` to configure the number of instances to wait for and the timeout for waiting for the init process. Default: - no CloudFormation init
        :param init_options: Use the given options for applying CloudFormation Init. Describes the configsets to use and the timeout to wait Default: - default options
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security group to launch the instances in. Default: - A SecurityGroup will be created if none is specified.
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        """
        if isinstance(rolling_update_configuration, dict):
            rolling_update_configuration = RollingUpdateConfiguration(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        if isinstance(init_options, dict):
            init_options = ApplyCloudFormationInitOptions(**init_options)
        self._values: typing.Dict[str, typing.Any] = {
            "instance_type": instance_type,
            "machine_image": machine_image,
            "vpc": vpc,
        }
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if group_metrics is not None:
            self._values["group_metrics"] = group_metrics
        if health_check is not None:
            self._values["health_check"] = health_check
        if ignore_unmodified_size_properties is not None:
            self._values["ignore_unmodified_size_properties"] = ignore_unmodified_size_properties
        if instance_monitoring is not None:
            self._values["instance_monitoring"] = instance_monitoring
        if key_name is not None:
            self._values["key_name"] = key_name
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_instance_lifetime is not None:
            self._values["max_instance_lifetime"] = max_instance_lifetime
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if notifications is not None:
            self._values["notifications"] = notifications
        if notifications_topic is not None:
            self._values["notifications_topic"] = notifications_topic
        if replacing_update_min_successful_instances_percent is not None:
            self._values["replacing_update_min_successful_instances_percent"] = replacing_update_min_successful_instances_percent
        if resource_signal_count is not None:
            self._values["resource_signal_count"] = resource_signal_count
        if resource_signal_timeout is not None:
            self._values["resource_signal_timeout"] = resource_signal_timeout
        if rolling_update_configuration is not None:
            self._values["rolling_update_configuration"] = rolling_update_configuration
        if signals is not None:
            self._values["signals"] = signals
        if spot_price is not None:
            self._values["spot_price"] = spot_price
        if update_policy is not None:
            self._values["update_policy"] = update_policy
        if update_type is not None:
            self._values["update_type"] = update_type
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if init is not None:
            self._values["init"] = init
        if init_options is not None:
            self._values["init_options"] = init_options
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        """Whether the instances can initiate connections to anywhere by default.

        :default: true
        """
        result = self._values.get("allow_all_outbound")
        return result

    @builtins.property
    def associate_public_ip_address(self) -> typing.Optional[builtins.bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        :default: - Use subnet setting.
        """
        result = self._values.get("associate_public_ip_address")
        return result

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        """The name of the Auto Scaling group.

        This name must be unique per Region per account.

        :default: - Auto generated by CloudFormation
        """
        result = self._values.get("auto_scaling_group_name")
        return result

    @builtins.property
    def block_devices(self) -> typing.Optional[typing.List[BlockDevice]]:
        """Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        :default: - Uses the block device mapping of the AMI

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        """
        result = self._values.get("block_devices")
        return result

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Default scaling cooldown for this AutoScalingGroup.

        :default: Duration.minutes(5)
        """
        result = self._values.get("cooldown")
        return result

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of instances in the fleet.

        If this is set to a number, every deployment will reset the amount of
        instances to this number. It is recommended to leave this value blank.

        :default: minCapacity, and leave unchanged during deployment

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def group_metrics(self) -> typing.Optional[typing.List[GroupMetrics]]:
        """Enable monitoring for group metrics, these metrics describe the group rather than any of its instances.

        To report all group metrics use ``GroupMetrics.all()``
        Group metrics are reported in a granularity of 1 minute at no additional charge.

        :default: - no group metrics will be reported
        """
        result = self._values.get("group_metrics")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        """Configuration for health checks.

        :default: - HealthCheck.ec2 with no grace period
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def ignore_unmodified_size_properties(self) -> typing.Optional[builtins.bool]:
        """If the ASG has scheduled actions, don't reset unchanged group sizes.

        Only used if the ASG has scheduled actions (which may scale your ASG up
        or down regardless of cdk deployments). If true, the size of the group
        will only be reset if it has been changed in the CDK app. If false, the
        sizes will always be changed back to what they were in the CDK app
        on deployment.

        :default: true
        """
        result = self._values.get("ignore_unmodified_size_properties")
        return result

    @builtins.property
    def instance_monitoring(self) -> typing.Optional[Monitoring]:
        """Controls whether instances in this group are launched with detailed or basic monitoring.

        When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account
        is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes.

        :default: - Monitoring.DETAILED

        :see: https://docs.aws.amazon.com/autoscaling/latest/userguide/as-instance-monitoring.html#enable-as-instance-metrics
        """
        result = self._values.get("instance_monitoring")
        return result

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        """Name of SSH keypair to grant access to instances.

        :default: - No SSH access will be possible.
        """
        result = self._values.get("key_name")
        return result

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        :default: desiredCapacity
        """
        result = self._values.get("max_capacity")
        return result

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum amount of time that an instance can be in service.

        The maximum duration applies
        to all current and future instances in the group. As an instance approaches its maximum duration,
        it is terminated and replaced, and cannot be used again.

        You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value,
        leave this property undefined.

        :default: none

        :see: https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html
        """
        result = self._values.get("max_instance_lifetime")
        return result

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        :default: 1
        """
        result = self._values.get("min_capacity")
        return result

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[NotificationConfiguration]]:
        """Configure autoscaling group to send notifications about fleet changes to an SNS topic(s).

        :default: - No fleet change notifications will be sent.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        """
        result = self._values.get("notifications")
        return result

    @builtins.property
    def notifications_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """(deprecated) SNS topic to send notifications about fleet changes.

        :default: - No fleet change notifications will be sent.

        :deprecated: use ``notifications``

        :stability: deprecated
        """
        result = self._values.get("notifications_topic")
        return result

    @builtins.property
    def replacing_update_min_successful_instances_percent(
        self,
    ) -> typing.Optional[jsii.Number]:
        """(deprecated) Configuration for replacing updates.

        Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
        many instances must signal success for the update to succeed.

        :default: minSuccessfulInstancesPercent

        :deprecated: Use ``signals`` instead

        :stability: deprecated
        """
        result = self._values.get("replacing_update_min_successful_instances_percent")
        return result

    @builtins.property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """(deprecated) How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        :default: 1 if resourceSignalTimeout is set, 0 otherwise

        :deprecated: Use ``signals`` instead.

        :stability: deprecated
        """
        result = self._values.get("resource_signal_count")
        return result

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        :default: Duration.minutes(5) if resourceSignalCount is set, N/A otherwise

        :deprecated: Use ``signals`` instead.

        :stability: deprecated
        """
        result = self._values.get("resource_signal_timeout")
        return result

    @builtins.property
    def rolling_update_configuration(
        self,
    ) -> typing.Optional[RollingUpdateConfiguration]:
        """(deprecated) Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        :default: - RollingUpdateConfiguration with defaults.

        :deprecated: Use ``updatePolicy`` instead

        :stability: deprecated
        """
        result = self._values.get("rolling_update_configuration")
        return result

    @builtins.property
    def signals(self) -> typing.Optional[Signals]:
        """Configure waiting for signals during deployment.

        Use this to pause the CloudFormation deployment to wait for the instances
        in the AutoScalingGroup to report successful startup during
        creation and updates. The UserData script needs to invoke ``cfn-signal``
        with a success or failure code after it is done setting up the instance.

        Without waiting for signals, the CloudFormation deployment will proceed as
        soon as the AutoScalingGroup has been created or updated but before the
        instances in the group have been started.

        For example, to have instances wait for an Elastic Load Balancing health check before
        they signal success, add a health-check verification by using the
        cfn-init helper script. For an example, see the verify_instance_health
        command in the Auto Scaling rolling updates sample template:

        https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/AutoScaling/AutoScalingRollingUpdates.yaml

        :default: - Do not wait for signals
        """
        result = self._values.get("signals")
        return result

    @builtins.property
    def spot_price(self) -> typing.Optional[builtins.str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        :default: none
        """
        result = self._values.get("spot_price")
        return result

    @builtins.property
    def update_policy(self) -> typing.Optional[UpdatePolicy]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        :default: - ``UpdatePolicy.rollingUpdate()`` if using ``init``, ``UpdatePolicy.none()`` otherwise
        """
        result = self._values.get("update_policy")
        return result

    @builtins.property
    def update_type(self) -> typing.Optional[UpdateType]:
        """(deprecated) What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        :default: UpdateType.None

        :deprecated: Use ``updatePolicy`` instead

        :stability: deprecated
        """
        result = self._values.get("update_type")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place instances within the VPC.

        :default: - All Private subnets.
        """
        result = self._values.get("vpc_subnets")
        return result

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """Type of instance to launch."""
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def machine_image(self) -> aws_cdk.aws_ec2.IMachineImage:
        """AMI to launch."""
        result = self._values.get("machine_image")
        assert result is not None, "Required property 'machine_image' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch these instances in."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def init(self) -> typing.Optional[aws_cdk.aws_ec2.CloudFormationInit]:
        """Apply the given CloudFormation Init configuration to the instances in the AutoScalingGroup at startup.

        If you specify ``init``, you must also specify ``signals`` to configure
        the number of instances to wait for and the timeout for waiting for the
        init process.

        :default: - no CloudFormation init
        """
        result = self._values.get("init")
        return result

    @builtins.property
    def init_options(self) -> typing.Optional[ApplyCloudFormationInitOptions]:
        """Use the given options for applying CloudFormation Init.

        Describes the configsets to use and the timeout to wait

        :default: - default options
        """
        result = self._values.get("init_options")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role to associate with the instance profile assigned to this Auto Scaling Group.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        :default: A role will automatically be created, it can be accessed via the ``role`` property

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            role = iam.Role(self, "MyRole",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
            )
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security group to launch the instances in.

        :default: - A SecurityGroup will be created if none is specified.
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def user_data(self) -> typing.Optional[aws_cdk.aws_ec2.UserData]:
        """Specific UserData to use.

        The UserData may still be mutated after creation.

        :default:

        - A UserData object appropriate for the MachineImage's
        Operating System is created.
        """
        result = self._values.get("user_data")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceOptions",
    jsii_struct_bases=[EbsDeviceOptionsBase],
    name_mapping={
        "delete_on_termination": "deleteOnTermination",
        "iops": "iops",
        "volume_type": "volumeType",
        "encrypted": "encrypted",
    },
)
class EbsDeviceOptions(EbsDeviceOptionsBase):
    def __init__(
        self,
        *,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[EbsDeviceVolumeType] = None,
        encrypted: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Block device options for an EBS volume.

        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume. Default: - none, required for {@link EbsDeviceVolumeType.IO1}
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        :param encrypted: Specifies whether the EBS volume is encrypted. Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption Default: false
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if iops is not None:
            self._values["iops"] = iops
        if volume_type is not None:
            self._values["volume_type"] = volume_type
        if encrypted is not None:
            self._values["encrypted"] = encrypted

    @builtins.property
    def delete_on_termination(self) -> typing.Optional[builtins.bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        result = self._values.get("delete_on_termination")
        return result

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        :default: - none, required for {@link EbsDeviceVolumeType.IO1}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("iops")
        return result

    @builtins.property
    def volume_type(self) -> typing.Optional[EbsDeviceVolumeType]:
        """The EBS volume type.

        :default: {@link EbsDeviceVolumeType.GP2}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("volume_type")
        return result

    @builtins.property
    def encrypted(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the EBS volume is encrypted.

        Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption

        :default: false

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#EBSEncryption_supported_instances
        """
        result = self._values.get("encrypted")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsDeviceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceProps",
    jsii_struct_bases=[EbsDeviceSnapshotOptions],
    name_mapping={
        "delete_on_termination": "deleteOnTermination",
        "iops": "iops",
        "volume_type": "volumeType",
        "volume_size": "volumeSize",
        "snapshot_id": "snapshotId",
    },
)
class EbsDeviceProps(EbsDeviceSnapshotOptions):
    def __init__(
        self,
        *,
        delete_on_termination: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[EbsDeviceVolumeType] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties of an EBS block device.

        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume. Default: - none, required for {@link EbsDeviceVolumeType.IO1}
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        :param volume_size: The volume size, in Gibibytes (GiB). If you specify volumeSize, it must be equal or greater than the size of the snapshot. Default: - The snapshot size
        :param snapshot_id: The snapshot ID of the volume to use. Default: - No snapshot will be used
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if iops is not None:
            self._values["iops"] = iops
        if volume_type is not None:
            self._values["volume_type"] = volume_type
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if snapshot_id is not None:
            self._values["snapshot_id"] = snapshot_id

    @builtins.property
    def delete_on_termination(self) -> typing.Optional[builtins.bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        result = self._values.get("delete_on_termination")
        return result

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        :default: - none, required for {@link EbsDeviceVolumeType.IO1}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("iops")
        return result

    @builtins.property
    def volume_type(self) -> typing.Optional[EbsDeviceVolumeType]:
        """The EBS volume type.

        :default: {@link EbsDeviceVolumeType.GP2}

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        result = self._values.get("volume_type")
        return result

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        """The volume size, in Gibibytes (GiB).

        If you specify volumeSize, it must be equal or greater than the size of the snapshot.

        :default: - The snapshot size
        """
        result = self._values.get("volume_size")
        return result

    @builtins.property
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        """The snapshot ID of the volume to use.

        :default: - No snapshot will be used
        """
        result = self._values.get("snapshot_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsDeviceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AdjustmentTier",
    "AdjustmentType",
    "ApplyCloudFormationInitOptions",
    "AutoScalingGroup",
    "AutoScalingGroupProps",
    "BaseTargetTrackingProps",
    "BasicLifecycleHookProps",
    "BasicScheduledActionProps",
    "BasicStepScalingPolicyProps",
    "BasicTargetTrackingScalingPolicyProps",
    "BlockDevice",
    "BlockDeviceVolume",
    "CfnAutoScalingGroup",
    "CfnAutoScalingGroupProps",
    "CfnLaunchConfiguration",
    "CfnLaunchConfigurationProps",
    "CfnLifecycleHook",
    "CfnLifecycleHookProps",
    "CfnScalingPolicy",
    "CfnScalingPolicyProps",
    "CfnScheduledAction",
    "CfnScheduledActionProps",
    "CommonAutoScalingGroupProps",
    "CpuUtilizationScalingProps",
    "CronOptions",
    "DefaultResult",
    "EbsDeviceOptions",
    "EbsDeviceOptionsBase",
    "EbsDeviceProps",
    "EbsDeviceSnapshotOptions",
    "EbsDeviceVolumeType",
    "Ec2HealthCheckOptions",
    "ElbHealthCheckOptions",
    "GroupMetric",
    "GroupMetrics",
    "HealthCheck",
    "IAutoScalingGroup",
    "ILifecycleHook",
    "ILifecycleHookTarget",
    "LifecycleHook",
    "LifecycleHookProps",
    "LifecycleHookTargetConfig",
    "LifecycleTransition",
    "MetricAggregationType",
    "MetricTargetTrackingProps",
    "Monitoring",
    "NetworkUtilizationScalingProps",
    "NotificationConfiguration",
    "PredefinedMetric",
    "RenderSignalsOptions",
    "RequestCountScalingProps",
    "RollingUpdateConfiguration",
    "RollingUpdateOptions",
    "ScalingEvent",
    "ScalingEvents",
    "ScalingInterval",
    "ScalingProcess",
    "Schedule",
    "ScheduledAction",
    "ScheduledActionProps",
    "Signals",
    "SignalsOptions",
    "StepScalingAction",
    "StepScalingActionProps",
    "StepScalingPolicy",
    "StepScalingPolicyProps",
    "TargetTrackingScalingPolicy",
    "TargetTrackingScalingPolicyProps",
    "UpdatePolicy",
    "UpdateType",
]

publication.publish()
