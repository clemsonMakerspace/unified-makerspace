"""
## Amazon CloudWatch Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

## Metric objects

Metric objects represent a metric that is emitted by AWS services or your own
application, such as `CPUUsage`, `FailureCount` or `Bandwidth`.

Metric objects can be constructed directly or are exposed by resources as
attributes. Resources that expose metrics will have functions that look
like `metricXxx()` which will return a Metric object, initialized with defaults
that make sense.

For example, `lambda.Function` objects have the `fn.metricErrors()` method, which
represents the amount of errors reported by that Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
errors = fn.metric_errors()
```

You can also instantiate `Metric` objects to reference any
[published metric](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html)
that's not exposed using a convenience method on the CDK construct.
For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
hosted_zone = route53.HostedZone(self, "MyHostedZone", zone_name="example.org")
metric = Metric(
    namespace="AWS/Route53",
    metric_name="DNSQueries",
    dimensions={
        "HostedZoneId": hosted_zone.hosted_zone_id
    }
)
```

### Instantiating a new Metric object

If you want to reference a metric that is not yet exposed by an existing construct,
you can instantiate a `Metric` object to represent it. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
metric = Metric(
    namespace="MyNamespace",
    metric_name="MyMetric",
    dimensions={
        "ProcessingStep": "Download"
    }
)
```

### Metric Math

Math expressions are supported by instantiating the `MathExpression` class.
For example, a math expression that sums two other metrics looks like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
all_problems = MathExpression(
    expression="errors + faults",
    using_metrics={
        "errors": my_construct.metric_errors(),
        "faults": my_construct.metric_faults()
    }
)
```

You can use `MathExpression` objects like any other metric, including using
them in other math expressions:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
problem_percentage = MathExpression(
    expression="(problems / invocations) * 100",
    using_metrics={
        "problems": all_problems,
        "invocations": my_construct.metric_invocations()
    }
)
```

### Aggregation

To graph or alarm on metrics you must aggregate them first, using a function
like `Average` or a percentile function like `P99`. By default, most Metric objects
returned by CDK libraries will be configured as `Average` over `300 seconds` (5 minutes).
The exception is if the metric represents a count of discrete events, such as
failures. In that case, the Metric object will be configured as `Sum` over `300 seconds`, i.e. it represents the number of times that event occurred over the
time period.

If you want to change the default aggregation of the Metric object (for example,
the function or the period), you can do so by passing additional parameters
to the metric function call:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
minute_error_rate = fn.metric_errors(
    statistic="avg",
    period=Duration.minutes(1),
    label="Lambda failure rate"
)
```

This function also allows changing the metric label or color (which will be
useful when embedding them in graphs, see below).

> Rates versus Sums
>
> The reason for using `Sum` to count discrete events is that *some* events are
> emitted as either `0` or `1` (for example `Errors` for a Lambda) and some are
> only emitted as `1` (for example `NumberOfMessagesPublished` for an SNS
> topic).
>
> In case `0`-metrics are emitted, it makes sense to take the `Average` of this
> metric: the result will be the fraction of errors over all executions.
>
> If `0`-metrics are not emitted, the `Average` will always be equal to `1`,
> and not be very useful.
>
> In order to simplify the mental model of `Metric` objects, we default to
> aggregating using `Sum`, which will be the same for both metrics types. If you
> happen to know the Metric you want to alarm on makes sense as a rate
> (`Average`) you can always choose to change the statistic.

## Alarms

Alarms can be created on metrics in one of two ways. Either create an `Alarm`
object, passing the `Metric` object to set the alarm on:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Alarm(self, "Alarm",
    metric=fn.metric_errors(),
    threshold=100,
    evaluation_periods=2
)
```

Alternatively, you can call `metric.createAlarm()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fn.metric_errors().create_alarm(self, "Alarm",
    threshold=100,
    evaluation_periods=2
)
```

The most important properties to set while creating an Alarms are:

* `threshold`: the value to compare the metric against.
* `comparisonOperator`: the comparison operation to use, defaults to `metric >= threshold`.
* `evaluationPeriods`: how many consecutive periods the metric has to be
  breaching the the threshold for the alarm to trigger.

### Alarm Actions

To add actions to an alarm, use the integration classes from the
`@aws-cdk/aws-cloudwatch-actions` package. For example, to post a message to
an SNS topic when an alarm breaches, do the following:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudwatch_actions as cw_actions

# ...
topic = sns.Topic(stack, "Topic")
alarm = cloudwatch.Alarm(stack, "Alarm")

alarm.add_alarm_action(cw_actions.SnsAction(topic))
```

### Composite Alarms

[Composite Alarms](https://aws.amazon.com/about-aws/whats-new/2020/03/amazon-cloudwatch-now-allows-you-to-combine-multiple-alarms/)
can be created from existing Alarm resources.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
alarm_rule = AlarmRule.any_of(
    AlarmRule.all_of(
        AlarmRule.any_of(alarm1,
            AlarmRule.from_alarm(alarm2, AlarmState.OK), alarm3),
        AlarmRule.not(AlarmRule.from_alarm(alarm4, AlarmState.INSUFFICIENT_DATA))),
    AlarmRule.from_boolean(False))

CompositeAlarm(self, "MyAwesomeCompositeAlarm",
    alarm_rule=alarm_rule
)
```

### A note on units

In CloudWatch, Metrics datums are emitted with units, such as `seconds` or
`bytes`. When `Metric` objects are given a `unit` attribute, it will be used to
*filter* the stream of metric datums for datums emitted using the same `unit`
attribute.

In particular, the `unit` field is *not* used to rescale datums or alarm threshold
values (for example, it cannot be used to specify an alarm threshold in
*Megabytes* if the metric stream is being emitted as *bytes*).

You almost certainly don't want to specify the `unit` property when creating
`Metric` objects (which will retrieve all datums regardless of their unit),
unless you have very specific requirements. Note that in any case, CloudWatch
only supports filtering by `unit` for Alarms, not in Dashboard graphs.

Please see the following GitHub issue for a discussion on real unit
calculations in CDK: https://github.com/aws/aws-cdk/issues/5595

## Dashboards

Dashboards are set of Widgets stored server-side which can be accessed quickly
from the AWS console. Available widgets are graphs of a metric over time, the
current value of a metric, or a static piece of Markdown which explains what the
graphs mean.

The following widgets are available:

* `GraphWidget` -- shows any number of metrics on both the left and right
  vertical axes.
* `AlarmWidget` -- shows the graph and alarm line for a single alarm.
* `SingleValueWidget` -- shows the current value of a set of metrics.
* `TextWidget` -- shows some static Markdown.
* `AlarmStatusWidget` -- shows the status of your alarms in a grid view.

### Graph widget

A graph widget can display any number of metrics on either the `left` or
`right` vertical axis:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(GraphWidget(
    title="Executions vs error rate",

    left=[execution_count_metric],

    right=[error_count_metric.with(
        statistic="average",
        label="Error rate",
        color=Color.GREEN
    )]
))
```

Using the methods `addLeftMetric()` and `addRightMetric()` you can add metrics to a graph widget later on.

Graph widgets can also display annotations attached to the left or the right y-axis.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(GraphWidget(
    # ...
    # ...

    left_annotations=[{"value": 1800, "label": Duration.minutes(30).to_human_string(), "color": Color.RED}, {"value": 3600, "label": "1 hour", "color": "#2ca02c"}
    ]
))
```

The graph legend can be adjusted from the default position at bottom of the widget.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(GraphWidget(
    # ...
    # ...

    legend_position=LegendPosition.RIGHT
))
```

The graph can publish live data within the last minute that has not been fully aggregated.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(GraphWidget(
    # ...
    # ...

    live_data=True
))
```

The graph view can be changed from default 'timeSeries' to 'bar' or 'pie'.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(GraphWidget(
    # ...
    # ...

    view=GraphWidgetView.BAR
))
```

### Alarm widget

An alarm widget shows the graph and the alarm line of a single alarm:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(AlarmWidget(
    title="Errors",
    alarm=error_alarm
))
```

### Single value widget

A single-value widget shows the latest value of a set of metrics (as opposed
to a graph of the value over time):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(SingleValueWidget(
    metrics=[visitor_count, purchase_count]
))
```

### Text widget

A text widget shows an arbitrary piece of MarkDown. Use this to add explanations
to your dashboard:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(TextWidget(
    markdown="# Key Performance Indicators"
))
```

### Alarm Status widget

An alarm status widget displays instantly the status of any type of alarms and gives the
ability to aggregate one or more alarms together in a small surface.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(
    AlarmStatusWidget(
        alarms=[error_alarm]
    ))
```

### Query results widget

A `LogQueryWidget` shows the results of a query from Logs Insights:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
dashboard.add_widgets(LogQueryWidget(
    log_group_names=["my-log-group"],
    view=LogQueryVisualizationType.TABLE,
    # The lines will be automatically combined using '\n|'.
    query_lines=["fields @message", "filter @message like /Error/"
    ]
))
```

### Dashboard Layout

The widgets on a dashboard are visually laid out in a grid that is 24 columns
wide. Normally you specify X and Y coordinates for the widgets on a Dashboard,
but because this is inconvenient to do manually, the library contains a simple
layout system to help you lay out your dashboards the way you want them to.

Widgets have a `width` and `height` property, and they will be automatically
laid out either horizontally or vertically stacked to fill out the available
space.

Widgets are added to a Dashboard by calling `add(widget1, widget2, ...)`.
Widgets given in the same call will be laid out horizontally. Widgets given
in different calls will be laid out vertically. To make more complex layouts,
you can use the following widgets to pack widgets together in different ways:

* `Column`: stack two or more widgets vertically.
* `Row`: lay out two or more widgets horizontally.
* `Spacer`: take up empty space
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


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.AlarmActionConfig",
    jsii_struct_bases=[],
    name_mapping={"alarm_action_arn": "alarmActionArn"},
)
class AlarmActionConfig:
    def __init__(self, *, alarm_action_arn: builtins.str) -> None:
        """Properties for an alarm action.

        :param alarm_action_arn: Return the ARN that should be used for a CloudWatch Alarm action.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alarm_action_arn": alarm_action_arn,
        }

    @builtins.property
    def alarm_action_arn(self) -> builtins.str:
        """Return the ARN that should be used for a CloudWatch Alarm action."""
        result = self._values.get("alarm_action_arn")
        assert result is not None, "Required property 'alarm_action_arn' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlarmRule(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.AlarmRule"):
    """Class with static functions to build AlarmRule for Composite Alarms."""

    def __init__(self) -> None:
        jsii.create(AlarmRule, self, [])

    @jsii.member(jsii_name="allOf")
    @builtins.classmethod
    def all_of(cls, *operands: "IAlarmRule") -> "IAlarmRule":
        """function to join all provided AlarmRules with AND operator.

        :param operands: IAlarmRules to be joined with AND operator.
        """
        return jsii.sinvoke(cls, "allOf", [*operands])

    @jsii.member(jsii_name="anyOf")
    @builtins.classmethod
    def any_of(cls, *operands: "IAlarmRule") -> "IAlarmRule":
        """function to join all provided AlarmRules with OR operator.

        :param operands: IAlarmRules to be joined with OR operator.
        """
        return jsii.sinvoke(cls, "anyOf", [*operands])

    @jsii.member(jsii_name="fromAlarm")
    @builtins.classmethod
    def from_alarm(cls, alarm: "IAlarm", alarm_state: "AlarmState") -> "IAlarmRule":
        """function to build Rule Expression for given IAlarm and AlarmState.

        :param alarm: IAlarm to be used in Rule Expression.
        :param alarm_state: AlarmState to be used in Rule Expression.
        """
        return jsii.sinvoke(cls, "fromAlarm", [alarm, alarm_state])

    @jsii.member(jsii_name="fromBoolean")
    @builtins.classmethod
    def from_boolean(cls, value: builtins.bool) -> "IAlarmRule":
        """function to build TRUE/FALSE intent for Rule Expression.

        :param value: boolean value to be used in rule expression.
        """
        return jsii.sinvoke(cls, "fromBoolean", [value])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, alarm_rule: builtins.str) -> "IAlarmRule":
        """function to build Rule Expression for given Alarm Rule string.

        :param alarm_rule: string to be used in Rule Expression.
        """
        return jsii.sinvoke(cls, "fromString", [alarm_rule])

    @jsii.member(jsii_name="not")
    @builtins.classmethod
    def not_(cls, operand: "IAlarmRule") -> "IAlarmRule":
        """function to wrap provided AlarmRule in NOT operator.

        :param operand: IAlarmRule to be wrapped in NOT operator.
        """
        return jsii.sinvoke(cls, "not", [operand])


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.AlarmState")
class AlarmState(enum.Enum):
    """Enumeration indicates state of Alarm used in building Alarm Rule."""

    ALARM = "ALARM"
    """State indicates resource is in ALARM."""
    OK = "OK"
    """State indicates resource is not in ALARM."""
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    """State indicates there is not enough data to determine is resource is in ALARM."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.AlarmStatusWidgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarms": "alarms",
        "height": "height",
        "title": "title",
        "width": "width",
    },
)
class AlarmStatusWidgetProps:
    def __init__(
        self,
        *,
        alarms: typing.List["IAlarm"],
        height: typing.Optional[jsii.Number] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for an Alarm Status Widget.

        :param alarms: CloudWatch Alarms to show in widget.
        :param height: Height of the widget. Default: 3
        :param title: The title of the widget. Default: 'Alarm Status'
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alarms": alarms,
        }
        if height is not None:
            self._values["height"] = height
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def alarms(self) -> typing.List["IAlarm"]:
        """CloudWatch Alarms to show in widget."""
        result = self._values.get("alarms")
        assert result is not None, "Required property 'alarms' is missing"
        return result

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        :default: 3
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        """The title of the widget.

        :default: 'Alarm Status'
        """
        result = self._values.get("title")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        :default: 6
        """
        result = self._values.get("width")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmStatusWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAlarm(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm",
):
    """A CloudFormation ``AWS::CloudWatch::Alarm``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
    :cloudformationResource: AWS::CloudWatch::Alarm
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        comparison_operator: builtins.str,
        evaluation_periods: jsii.Number,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        alarm_actions: typing.Optional[typing.List[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        dimensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.List[builtins.str]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        metrics: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricDataQueryProperty"]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        ok_actions: typing.Optional[typing.List[builtins.str]] = None,
        period: typing.Optional[jsii.Number] = None,
        statistic: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        threshold_metric_id: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::CloudWatch::Alarm``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param comparison_operator: ``AWS::CloudWatch::Alarm.ComparisonOperator``.
        :param evaluation_periods: ``AWS::CloudWatch::Alarm.EvaluationPeriods``.
        :param actions_enabled: ``AWS::CloudWatch::Alarm.ActionsEnabled``.
        :param alarm_actions: ``AWS::CloudWatch::Alarm.AlarmActions``.
        :param alarm_description: ``AWS::CloudWatch::Alarm.AlarmDescription``.
        :param alarm_name: ``AWS::CloudWatch::Alarm.AlarmName``.
        :param datapoints_to_alarm: ``AWS::CloudWatch::Alarm.DatapointsToAlarm``.
        :param dimensions: ``AWS::CloudWatch::Alarm.Dimensions``.
        :param evaluate_low_sample_count_percentile: ``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.
        :param extended_statistic: ``AWS::CloudWatch::Alarm.ExtendedStatistic``.
        :param insufficient_data_actions: ``AWS::CloudWatch::Alarm.InsufficientDataActions``.
        :param metric_name: ``AWS::CloudWatch::Alarm.MetricName``.
        :param metrics: ``AWS::CloudWatch::Alarm.Metrics``.
        :param namespace: ``AWS::CloudWatch::Alarm.Namespace``.
        :param ok_actions: ``AWS::CloudWatch::Alarm.OKActions``.
        :param period: ``AWS::CloudWatch::Alarm.Period``.
        :param statistic: ``AWS::CloudWatch::Alarm.Statistic``.
        :param threshold: ``AWS::CloudWatch::Alarm.Threshold``.
        :param threshold_metric_id: ``AWS::CloudWatch::Alarm.ThresholdMetricId``.
        :param treat_missing_data: ``AWS::CloudWatch::Alarm.TreatMissingData``.
        :param unit: ``AWS::CloudWatch::Alarm.Unit``.
        """
        props = CfnAlarmProps(
            comparison_operator=comparison_operator,
            evaluation_periods=evaluation_periods,
            actions_enabled=actions_enabled,
            alarm_actions=alarm_actions,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            dimensions=dimensions,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            extended_statistic=extended_statistic,
            insufficient_data_actions=insufficient_data_actions,
            metric_name=metric_name,
            metrics=metrics,
            namespace=namespace,
            ok_actions=ok_actions,
            period=period,
            statistic=statistic,
            threshold=threshold,
            threshold_metric_id=threshold_metric_id,
            treat_missing_data=treat_missing_data,
            unit=unit,
        )

        jsii.create(CfnAlarm, self, [scope, id, props])

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
    @jsii.member(jsii_name="comparisonOperator")
    def comparison_operator(self) -> builtins.str:
        """``AWS::CloudWatch::Alarm.ComparisonOperator``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-comparisonoperator
        """
        return jsii.get(self, "comparisonOperator")

    @comparison_operator.setter # type: ignore
    def comparison_operator(self, value: builtins.str) -> None:
        jsii.set(self, "comparisonOperator", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="evaluationPeriods")
    def evaluation_periods(self) -> jsii.Number:
        """``AWS::CloudWatch::Alarm.EvaluationPeriods``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluationperiods
        """
        return jsii.get(self, "evaluationPeriods")

    @evaluation_periods.setter # type: ignore
    def evaluation_periods(self, value: jsii.Number) -> None:
        jsii.set(self, "evaluationPeriods", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="actionsEnabled")
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CloudWatch::Alarm.ActionsEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-actionsenabled
        """
        return jsii.get(self, "actionsEnabled")

    @actions_enabled.setter # type: ignore
    def actions_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "actionsEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmActions")
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::Alarm.AlarmActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmactions
        """
        return jsii.get(self, "alarmActions")

    @alarm_actions.setter # type: ignore
    def alarm_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "alarmActions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmDescription")
    def alarm_description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.AlarmDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmdescription
        """
        return jsii.get(self, "alarmDescription")

    @alarm_description.setter # type: ignore
    def alarm_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alarmDescription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.AlarmName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmname
        """
        return jsii.get(self, "alarmName")

    @alarm_name.setter # type: ignore
    def alarm_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alarmName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="datapointsToAlarm")
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.DatapointsToAlarm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
        """
        return jsii.get(self, "datapointsToAlarm")

    @datapoints_to_alarm.setter # type: ignore
    def datapoints_to_alarm(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "datapointsToAlarm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]]:
        """``AWS::CloudWatch::Alarm.Dimensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dimension
        """
        return jsii.get(self, "dimensions")

    @dimensions.setter # type: ignore
    def dimensions(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]],
    ) -> None:
        jsii.set(self, "dimensions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="evaluateLowSampleCountPercentile")
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluatelowsamplecountpercentile
        """
        return jsii.get(self, "evaluateLowSampleCountPercentile")

    @evaluate_low_sample_count_percentile.setter # type: ignore
    def evaluate_low_sample_count_percentile(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "evaluateLowSampleCountPercentile", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="extendedStatistic")
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.ExtendedStatistic``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-extendedstatistic
        """
        return jsii.get(self, "extendedStatistic")

    @extended_statistic.setter # type: ignore
    def extended_statistic(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "extendedStatistic", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="insufficientDataActions")
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::Alarm.InsufficientDataActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-insufficientdataactions
        """
        return jsii.get(self, "insufficientDataActions")

    @insufficient_data_actions.setter # type: ignore
    def insufficient_data_actions(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "insufficientDataActions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.MetricName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-metricname
        """
        return jsii.get(self, "metricName")

    @metric_name.setter # type: ignore
    def metric_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "metricName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metrics")
    def metrics(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricDataQueryProperty"]]]]:
        """``AWS::CloudWatch::Alarm.Metrics``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-metrics
        """
        return jsii.get(self, "metrics")

    @metrics.setter # type: ignore
    def metrics(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricDataQueryProperty"]]]],
    ) -> None:
        jsii.set(self, "metrics", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.Namespace``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-namespace
        """
        return jsii.get(self, "namespace")

    @namespace.setter # type: ignore
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "namespace", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="okActions")
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::Alarm.OKActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-okactions
        """
        return jsii.get(self, "okActions")

    @ok_actions.setter # type: ignore
    def ok_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "okActions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="period")
    def period(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Period``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-period
        """
        return jsii.get(self, "period")

    @period.setter # type: ignore
    def period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "period", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.Statistic``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-statistic
        """
        return jsii.get(self, "statistic")

    @statistic.setter # type: ignore
    def statistic(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "statistic", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Threshold``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-threshold
        """
        return jsii.get(self, "threshold")

    @threshold.setter # type: ignore
    def threshold(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "threshold", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="thresholdMetricId")
    def threshold_metric_id(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.ThresholdMetricId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dynamic-threshold
        """
        return jsii.get(self, "thresholdMetricId")

    @threshold_metric_id.setter # type: ignore
    def threshold_metric_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "thresholdMetricId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="treatMissingData")
    def treat_missing_data(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.TreatMissingData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-treatmissingdata
        """
        return jsii.get(self, "treatMissingData")

    @treat_missing_data.setter # type: ignore
    def treat_missing_data(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "treatMissingData", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.Unit``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-unit
        """
        return jsii.get(self, "unit")

    @unit.setter # type: ignore
    def unit(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "unit", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            """
            :param name: ``CfnAlarm.DimensionProperty.Name``.
            :param value: ``CfnAlarm.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnAlarm.DimensionProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnAlarm.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "expression": "expression",
            "label": "label",
            "metric_stat": "metricStat",
            "period": "period",
            "return_data": "returnData",
        },
    )
    class MetricDataQueryProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            expression: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricStatProperty"]] = None,
            period: typing.Optional[jsii.Number] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param id: ``CfnAlarm.MetricDataQueryProperty.Id``.
            :param expression: ``CfnAlarm.MetricDataQueryProperty.Expression``.
            :param label: ``CfnAlarm.MetricDataQueryProperty.Label``.
            :param metric_stat: ``CfnAlarm.MetricDataQueryProperty.MetricStat``.
            :param period: ``CfnAlarm.MetricDataQueryProperty.Period``.
            :param return_data: ``CfnAlarm.MetricDataQueryProperty.ReturnData``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
            }
            if expression is not None:
                self._values["expression"] = expression
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if period is not None:
                self._values["period"] = period
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnAlarm.MetricDataQueryProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            """``CfnAlarm.MetricDataQueryProperty.Expression``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-expression
            """
            result = self._values.get("expression")
            return result

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            """``CfnAlarm.MetricDataQueryProperty.Label``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-label
            """
            result = self._values.get("label")
            return result

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricStatProperty"]]:
            """``CfnAlarm.MetricDataQueryProperty.MetricStat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-metricstat
            """
            result = self._values.get("metric_stat")
            return result

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            """``CfnAlarm.MetricDataQueryProperty.Period``."""
            result = self._values.get("period")
            return result

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnAlarm.MetricDataQueryProperty.ReturnData``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-returndata
            """
            result = self._values.get("return_data")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param dimensions: ``CfnAlarm.MetricProperty.Dimensions``.
            :param metric_name: ``CfnAlarm.MetricProperty.MetricName``.
            :param namespace: ``CfnAlarm.MetricProperty.Namespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.DimensionProperty"]]]]:
            """``CfnAlarm.MetricProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-dimensions
            """
            result = self._values.get("dimensions")
            return result

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            """``CfnAlarm.MetricProperty.MetricName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-metricname
            """
            result = self._values.get("metric_name")
            return result

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            """``CfnAlarm.MetricProperty.Namespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-namespace
            """
            result = self._values.get("namespace")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric": "metric",
            "period": "period",
            "stat": "stat",
            "unit": "unit",
        },
    )
    class MetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricProperty"],
            period: jsii.Number,
            stat: builtins.str,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param metric: ``CfnAlarm.MetricStatProperty.Metric``.
            :param period: ``CfnAlarm.MetricStatProperty.Period``.
            :param stat: ``CfnAlarm.MetricStatProperty.Stat``.
            :param unit: ``CfnAlarm.MetricStatProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "metric": metric,
                "period": period,
                "stat": stat,
            }
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnAlarm.MetricProperty"]:
            """``CfnAlarm.MetricStatProperty.Metric``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-metric
            """
            result = self._values.get("metric")
            assert result is not None, "Required property 'metric' is missing"
            return result

        @builtins.property
        def period(self) -> jsii.Number:
            """``CfnAlarm.MetricStatProperty.Period``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-period
            """
            result = self._values.get("period")
            assert result is not None, "Required property 'period' is missing"
            return result

        @builtins.property
        def stat(self) -> builtins.str:
            """``CfnAlarm.MetricStatProperty.Stat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-stat
            """
            result = self._values.get("stat")
            assert result is not None, "Required property 'stat' is missing"
            return result

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            """``CfnAlarm.MetricStatProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-unit
            """
            result = self._values.get("unit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarmProps",
    jsii_struct_bases=[],
    name_mapping={
        "comparison_operator": "comparisonOperator",
        "evaluation_periods": "evaluationPeriods",
        "actions_enabled": "actionsEnabled",
        "alarm_actions": "alarmActions",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "dimensions": "dimensions",
        "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
        "extended_statistic": "extendedStatistic",
        "insufficient_data_actions": "insufficientDataActions",
        "metric_name": "metricName",
        "metrics": "metrics",
        "namespace": "namespace",
        "ok_actions": "okActions",
        "period": "period",
        "statistic": "statistic",
        "threshold": "threshold",
        "threshold_metric_id": "thresholdMetricId",
        "treat_missing_data": "treatMissingData",
        "unit": "unit",
    },
)
class CfnAlarmProps:
    def __init__(
        self,
        *,
        comparison_operator: builtins.str,
        evaluation_periods: jsii.Number,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        alarm_actions: typing.Optional[typing.List[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        dimensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAlarm.DimensionProperty]]]] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.List[builtins.str]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        metrics: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAlarm.MetricDataQueryProperty]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        ok_actions: typing.Optional[typing.List[builtins.str]] = None,
        period: typing.Optional[jsii.Number] = None,
        statistic: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        threshold_metric_id: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[builtins.str] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudWatch::Alarm``.

        :param comparison_operator: ``AWS::CloudWatch::Alarm.ComparisonOperator``.
        :param evaluation_periods: ``AWS::CloudWatch::Alarm.EvaluationPeriods``.
        :param actions_enabled: ``AWS::CloudWatch::Alarm.ActionsEnabled``.
        :param alarm_actions: ``AWS::CloudWatch::Alarm.AlarmActions``.
        :param alarm_description: ``AWS::CloudWatch::Alarm.AlarmDescription``.
        :param alarm_name: ``AWS::CloudWatch::Alarm.AlarmName``.
        :param datapoints_to_alarm: ``AWS::CloudWatch::Alarm.DatapointsToAlarm``.
        :param dimensions: ``AWS::CloudWatch::Alarm.Dimensions``.
        :param evaluate_low_sample_count_percentile: ``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.
        :param extended_statistic: ``AWS::CloudWatch::Alarm.ExtendedStatistic``.
        :param insufficient_data_actions: ``AWS::CloudWatch::Alarm.InsufficientDataActions``.
        :param metric_name: ``AWS::CloudWatch::Alarm.MetricName``.
        :param metrics: ``AWS::CloudWatch::Alarm.Metrics``.
        :param namespace: ``AWS::CloudWatch::Alarm.Namespace``.
        :param ok_actions: ``AWS::CloudWatch::Alarm.OKActions``.
        :param period: ``AWS::CloudWatch::Alarm.Period``.
        :param statistic: ``AWS::CloudWatch::Alarm.Statistic``.
        :param threshold: ``AWS::CloudWatch::Alarm.Threshold``.
        :param threshold_metric_id: ``AWS::CloudWatch::Alarm.ThresholdMetricId``.
        :param treat_missing_data: ``AWS::CloudWatch::Alarm.TreatMissingData``.
        :param unit: ``AWS::CloudWatch::Alarm.Unit``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "comparison_operator": comparison_operator,
            "evaluation_periods": evaluation_periods,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if evaluate_low_sample_count_percentile is not None:
            self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if insufficient_data_actions is not None:
            self._values["insufficient_data_actions"] = insufficient_data_actions
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if metrics is not None:
            self._values["metrics"] = metrics
        if namespace is not None:
            self._values["namespace"] = namespace
        if ok_actions is not None:
            self._values["ok_actions"] = ok_actions
        if period is not None:
            self._values["period"] = period
        if statistic is not None:
            self._values["statistic"] = statistic
        if threshold is not None:
            self._values["threshold"] = threshold
        if threshold_metric_id is not None:
            self._values["threshold_metric_id"] = threshold_metric_id
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def comparison_operator(self) -> builtins.str:
        """``AWS::CloudWatch::Alarm.ComparisonOperator``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-comparisonoperator
        """
        result = self._values.get("comparison_operator")
        assert result is not None, "Required property 'comparison_operator' is missing"
        return result

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        """``AWS::CloudWatch::Alarm.EvaluationPeriods``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluationperiods
        """
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return result

    @builtins.property
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CloudWatch::Alarm.ActionsEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-actionsenabled
        """
        result = self._values.get("actions_enabled")
        return result

    @builtins.property
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::Alarm.AlarmActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmactions
        """
        result = self._values.get("alarm_actions")
        return result

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.AlarmDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmdescription
        """
        result = self._values.get("alarm_description")
        return result

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.AlarmName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmname
        """
        result = self._values.get("alarm_name")
        return result

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.DatapointsToAlarm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
        """
        result = self._values.get("datapoints_to_alarm")
        return result

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAlarm.DimensionProperty]]]]:
        """``AWS::CloudWatch::Alarm.Dimensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dimension
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluatelowsamplecountpercentile
        """
        result = self._values.get("evaluate_low_sample_count_percentile")
        return result

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.ExtendedStatistic``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-extendedstatistic
        """
        result = self._values.get("extended_statistic")
        return result

    @builtins.property
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::Alarm.InsufficientDataActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-insufficientdataactions
        """
        result = self._values.get("insufficient_data_actions")
        return result

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.MetricName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-metricname
        """
        result = self._values.get("metric_name")
        return result

    @builtins.property
    def metrics(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAlarm.MetricDataQueryProperty]]]]:
        """``AWS::CloudWatch::Alarm.Metrics``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-metrics
        """
        result = self._values.get("metrics")
        return result

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.Namespace``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-namespace
        """
        result = self._values.get("namespace")
        return result

    @builtins.property
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::Alarm.OKActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-okactions
        """
        result = self._values.get("ok_actions")
        return result

    @builtins.property
    def period(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Period``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-period
        """
        result = self._values.get("period")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.Statistic``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-statistic
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudWatch::Alarm.Threshold``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-threshold
        """
        result = self._values.get("threshold")
        return result

    @builtins.property
    def threshold_metric_id(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.ThresholdMetricId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dynamic-threshold
        """
        result = self._values.get("threshold_metric_id")
        return result

    @builtins.property
    def treat_missing_data(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.TreatMissingData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-treatmissingdata
        """
        result = self._values.get("treat_missing_data")
        return result

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Alarm.Unit``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-unit
        """
        result = self._values.get("unit")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAnomalyDetector(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector",
):
    """A CloudFormation ``AWS::CloudWatch::AnomalyDetector``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
    :cloudformationResource: AWS::CloudWatch::AnomalyDetector
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        stat: builtins.str,
        configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.ConfigurationProperty"]] = None,
        dimensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.DimensionProperty"]]]] = None,
    ) -> None:
        """Create a new ``AWS::CloudWatch::AnomalyDetector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param metric_name: ``AWS::CloudWatch::AnomalyDetector.MetricName``.
        :param namespace: ``AWS::CloudWatch::AnomalyDetector.Namespace``.
        :param stat: ``AWS::CloudWatch::AnomalyDetector.Stat``.
        :param configuration: ``AWS::CloudWatch::AnomalyDetector.Configuration``.
        :param dimensions: ``AWS::CloudWatch::AnomalyDetector.Dimensions``.
        """
        props = CfnAnomalyDetectorProps(
            metric_name=metric_name,
            namespace=namespace,
            stat=stat,
            configuration=configuration,
            dimensions=dimensions,
        )

        jsii.create(CfnAnomalyDetector, self, [scope, id, props])

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
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        """``AWS::CloudWatch::AnomalyDetector.MetricName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricname
        """
        return jsii.get(self, "metricName")

    @metric_name.setter # type: ignore
    def metric_name(self, value: builtins.str) -> None:
        jsii.set(self, "metricName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        """``AWS::CloudWatch::AnomalyDetector.Namespace``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-namespace
        """
        return jsii.get(self, "namespace")

    @namespace.setter # type: ignore
    def namespace(self, value: builtins.str) -> None:
        jsii.set(self, "namespace", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stat")
    def stat(self) -> builtins.str:
        """``AWS::CloudWatch::AnomalyDetector.Stat``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-stat
        """
        return jsii.get(self, "stat")

    @stat.setter # type: ignore
    def stat(self, value: builtins.str) -> None:
        jsii.set(self, "stat", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.ConfigurationProperty"]]:
        """``AWS::CloudWatch::AnomalyDetector.Configuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-configuration
        """
        return jsii.get(self, "configuration")

    @configuration.setter # type: ignore
    def configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.ConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "configuration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.DimensionProperty"]]]]:
        """``AWS::CloudWatch::AnomalyDetector.Dimensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-dimensions
        """
        return jsii.get(self, "dimensions")

    @dimensions.setter # type: ignore
    def dimensions(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.DimensionProperty"]]]],
    ) -> None:
        jsii.set(self, "dimensions", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "excluded_time_ranges": "excludedTimeRanges",
            "metric_time_zone": "metricTimeZone",
        },
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            excluded_time_ranges: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.RangeProperty"]]]] = None,
            metric_time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param excluded_time_ranges: ``CfnAnomalyDetector.ConfigurationProperty.ExcludedTimeRanges``.
            :param metric_time_zone: ``CfnAnomalyDetector.ConfigurationProperty.MetricTimeZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if excluded_time_ranges is not None:
                self._values["excluded_time_ranges"] = excluded_time_ranges
            if metric_time_zone is not None:
                self._values["metric_time_zone"] = metric_time_zone

        @builtins.property
        def excluded_time_ranges(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAnomalyDetector.RangeProperty"]]]]:
            """``CfnAnomalyDetector.ConfigurationProperty.ExcludedTimeRanges``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-excludedtimeranges
            """
            result = self._values.get("excluded_time_ranges")
            return result

        @builtins.property
        def metric_time_zone(self) -> typing.Optional[builtins.str]:
            """``CfnAnomalyDetector.ConfigurationProperty.MetricTimeZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-configuration.html#cfn-cloudwatch-anomalydetector-configuration-metrictimezone
            """
            result = self._values.get("metric_time_zone")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            """
            :param name: ``CfnAnomalyDetector.DimensionProperty.Name``.
            :param value: ``CfnAnomalyDetector.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnAnomalyDetector.DimensionProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnAnomalyDetector.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-dimension.html#cfn-cloudwatch-anomalydetector-dimension-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetector.RangeProperty",
        jsii_struct_bases=[],
        name_mapping={"end_time": "endTime", "start_time": "startTime"},
    )
    class RangeProperty:
        def __init__(self, *, end_time: builtins.str, start_time: builtins.str) -> None:
            """
            :param end_time: ``CfnAnomalyDetector.RangeProperty.EndTime``.
            :param start_time: ``CfnAnomalyDetector.RangeProperty.StartTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "end_time": end_time,
                "start_time": start_time,
            }

        @builtins.property
        def end_time(self) -> builtins.str:
            """``CfnAnomalyDetector.RangeProperty.EndTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-endtime
            """
            result = self._values.get("end_time")
            assert result is not None, "Required property 'end_time' is missing"
            return result

        @builtins.property
        def start_time(self) -> builtins.str:
            """``CfnAnomalyDetector.RangeProperty.StartTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-anomalydetector-range.html#cfn-cloudwatch-anomalydetector-range-starttime
            """
            result = self._values.get("start_time")
            assert result is not None, "Required property 'start_time' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CfnAnomalyDetectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "stat": "stat",
        "configuration": "configuration",
        "dimensions": "dimensions",
    },
)
class CfnAnomalyDetectorProps:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        stat: builtins.str,
        configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAnomalyDetector.ConfigurationProperty]] = None,
        dimensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAnomalyDetector.DimensionProperty]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudWatch::AnomalyDetector``.

        :param metric_name: ``AWS::CloudWatch::AnomalyDetector.MetricName``.
        :param namespace: ``AWS::CloudWatch::AnomalyDetector.Namespace``.
        :param stat: ``AWS::CloudWatch::AnomalyDetector.Stat``.
        :param configuration: ``AWS::CloudWatch::AnomalyDetector.Configuration``.
        :param dimensions: ``AWS::CloudWatch::AnomalyDetector.Dimensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
            "stat": stat,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if dimensions is not None:
            self._values["dimensions"] = dimensions

    @builtins.property
    def metric_name(self) -> builtins.str:
        """``AWS::CloudWatch::AnomalyDetector.MetricName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-metricname
        """
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return result

    @builtins.property
    def namespace(self) -> builtins.str:
        """``AWS::CloudWatch::AnomalyDetector.Namespace``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-namespace
        """
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return result

    @builtins.property
    def stat(self) -> builtins.str:
        """``AWS::CloudWatch::AnomalyDetector.Stat``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-stat
        """
        result = self._values.get("stat")
        assert result is not None, "Required property 'stat' is missing"
        return result

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAnomalyDetector.ConfigurationProperty]]:
        """``AWS::CloudWatch::AnomalyDetector.Configuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-configuration
        """
        result = self._values.get("configuration")
        return result

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAnomalyDetector.DimensionProperty]]]]:
        """``AWS::CloudWatch::AnomalyDetector.Dimensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-anomalydetector.html#cfn-cloudwatch-anomalydetector-dimensions
        """
        result = self._values.get("dimensions")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalyDetectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCompositeAlarm(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.CfnCompositeAlarm",
):
    """A CloudFormation ``AWS::CloudWatch::CompositeAlarm``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html
    :cloudformationResource: AWS::CloudWatch::CompositeAlarm
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        alarm_name: builtins.str,
        alarm_rule: builtins.str,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        alarm_actions: typing.Optional[typing.List[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.List[builtins.str]] = None,
        ok_actions: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::CloudWatch::CompositeAlarm``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alarm_name: ``AWS::CloudWatch::CompositeAlarm.AlarmName``.
        :param alarm_rule: ``AWS::CloudWatch::CompositeAlarm.AlarmRule``.
        :param actions_enabled: ``AWS::CloudWatch::CompositeAlarm.ActionsEnabled``.
        :param alarm_actions: ``AWS::CloudWatch::CompositeAlarm.AlarmActions``.
        :param alarm_description: ``AWS::CloudWatch::CompositeAlarm.AlarmDescription``.
        :param insufficient_data_actions: ``AWS::CloudWatch::CompositeAlarm.InsufficientDataActions``.
        :param ok_actions: ``AWS::CloudWatch::CompositeAlarm.OKActions``.
        """
        props = CfnCompositeAlarmProps(
            alarm_name=alarm_name,
            alarm_rule=alarm_rule,
            actions_enabled=actions_enabled,
            alarm_actions=alarm_actions,
            alarm_description=alarm_description,
            insufficient_data_actions=insufficient_data_actions,
            ok_actions=ok_actions,
        )

        jsii.create(CfnCompositeAlarm, self, [scope, id, props])

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
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        """``AWS::CloudWatch::CompositeAlarm.AlarmName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmname
        """
        return jsii.get(self, "alarmName")

    @alarm_name.setter # type: ignore
    def alarm_name(self, value: builtins.str) -> None:
        jsii.set(self, "alarmName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmRule")
    def alarm_rule(self) -> builtins.str:
        """``AWS::CloudWatch::CompositeAlarm.AlarmRule``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmrule
        """
        return jsii.get(self, "alarmRule")

    @alarm_rule.setter # type: ignore
    def alarm_rule(self, value: builtins.str) -> None:
        jsii.set(self, "alarmRule", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="actionsEnabled")
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CloudWatch::CompositeAlarm.ActionsEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionsenabled
        """
        return jsii.get(self, "actionsEnabled")

    @actions_enabled.setter # type: ignore
    def actions_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "actionsEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmActions")
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::CompositeAlarm.AlarmActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmactions
        """
        return jsii.get(self, "alarmActions")

    @alarm_actions.setter # type: ignore
    def alarm_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "alarmActions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmDescription")
    def alarm_description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::CompositeAlarm.AlarmDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmdescription
        """
        return jsii.get(self, "alarmDescription")

    @alarm_description.setter # type: ignore
    def alarm_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alarmDescription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="insufficientDataActions")
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::CompositeAlarm.InsufficientDataActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-insufficientdataactions
        """
        return jsii.get(self, "insufficientDataActions")

    @insufficient_data_actions.setter # type: ignore
    def insufficient_data_actions(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "insufficientDataActions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="okActions")
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::CompositeAlarm.OKActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-okactions
        """
        return jsii.get(self, "okActions")

    @ok_actions.setter # type: ignore
    def ok_actions(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "okActions", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CfnCompositeAlarmProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_name": "alarmName",
        "alarm_rule": "alarmRule",
        "actions_enabled": "actionsEnabled",
        "alarm_actions": "alarmActions",
        "alarm_description": "alarmDescription",
        "insufficient_data_actions": "insufficientDataActions",
        "ok_actions": "okActions",
    },
)
class CfnCompositeAlarmProps:
    def __init__(
        self,
        *,
        alarm_name: builtins.str,
        alarm_rule: builtins.str,
        actions_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        alarm_actions: typing.Optional[typing.List[builtins.str]] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        insufficient_data_actions: typing.Optional[typing.List[builtins.str]] = None,
        ok_actions: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudWatch::CompositeAlarm``.

        :param alarm_name: ``AWS::CloudWatch::CompositeAlarm.AlarmName``.
        :param alarm_rule: ``AWS::CloudWatch::CompositeAlarm.AlarmRule``.
        :param actions_enabled: ``AWS::CloudWatch::CompositeAlarm.ActionsEnabled``.
        :param alarm_actions: ``AWS::CloudWatch::CompositeAlarm.AlarmActions``.
        :param alarm_description: ``AWS::CloudWatch::CompositeAlarm.AlarmDescription``.
        :param insufficient_data_actions: ``AWS::CloudWatch::CompositeAlarm.InsufficientDataActions``.
        :param ok_actions: ``AWS::CloudWatch::CompositeAlarm.OKActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alarm_name": alarm_name,
            "alarm_rule": alarm_rule,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_actions is not None:
            self._values["alarm_actions"] = alarm_actions
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if insufficient_data_actions is not None:
            self._values["insufficient_data_actions"] = insufficient_data_actions
        if ok_actions is not None:
            self._values["ok_actions"] = ok_actions

    @builtins.property
    def alarm_name(self) -> builtins.str:
        """``AWS::CloudWatch::CompositeAlarm.AlarmName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmname
        """
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return result

    @builtins.property
    def alarm_rule(self) -> builtins.str:
        """``AWS::CloudWatch::CompositeAlarm.AlarmRule``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmrule
        """
        result = self._values.get("alarm_rule")
        assert result is not None, "Required property 'alarm_rule' is missing"
        return result

    @builtins.property
    def actions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CloudWatch::CompositeAlarm.ActionsEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-actionsenabled
        """
        result = self._values.get("actions_enabled")
        return result

    @builtins.property
    def alarm_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::CompositeAlarm.AlarmActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmactions
        """
        result = self._values.get("alarm_actions")
        return result

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::CompositeAlarm.AlarmDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-alarmdescription
        """
        result = self._values.get("alarm_description")
        return result

    @builtins.property
    def insufficient_data_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::CompositeAlarm.InsufficientDataActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-insufficientdataactions
        """
        result = self._values.get("insufficient_data_actions")
        return result

    @builtins.property
    def ok_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudWatch::CompositeAlarm.OKActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-compositealarm.html#cfn-cloudwatch-compositealarm-okactions
        """
        result = self._values.get("ok_actions")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCompositeAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDashboard(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboard",
):
    """A CloudFormation ``AWS::CloudWatch::Dashboard``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
    :cloudformationResource: AWS::CloudWatch::Dashboard
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        dashboard_body: builtins.str,
        dashboard_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::CloudWatch::Dashboard``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dashboard_body: ``AWS::CloudWatch::Dashboard.DashboardBody``.
        :param dashboard_name: ``AWS::CloudWatch::Dashboard.DashboardName``.
        """
        props = CfnDashboardProps(
            dashboard_body=dashboard_body, dashboard_name=dashboard_name
        )

        jsii.create(CfnDashboard, self, [scope, id, props])

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
    @jsii.member(jsii_name="dashboardBody")
    def dashboard_body(self) -> builtins.str:
        """``AWS::CloudWatch::Dashboard.DashboardBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
        """
        return jsii.get(self, "dashboardBody")

    @dashboard_body.setter # type: ignore
    def dashboard_body(self, value: builtins.str) -> None:
        jsii.set(self, "dashboardBody", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Dashboard.DashboardName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
        """
        return jsii.get(self, "dashboardName")

    @dashboard_name.setter # type: ignore
    def dashboard_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dashboardName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboardProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_body": "dashboardBody",
        "dashboard_name": "dashboardName",
    },
)
class CfnDashboardProps:
    def __init__(
        self,
        *,
        dashboard_body: builtins.str,
        dashboard_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudWatch::Dashboard``.

        :param dashboard_body: ``AWS::CloudWatch::Dashboard.DashboardBody``.
        :param dashboard_name: ``AWS::CloudWatch::Dashboard.DashboardName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "dashboard_body": dashboard_body,
        }
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name

    @builtins.property
    def dashboard_body(self) -> builtins.str:
        """``AWS::CloudWatch::Dashboard.DashboardBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
        """
        result = self._values.get("dashboard_body")
        assert result is not None, "Required property 'dashboard_body' is missing"
        return result

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::Dashboard.DashboardName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
        """
        result = self._values.get("dashboard_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnInsightRule(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.CfnInsightRule",
):
    """A CloudFormation ``AWS::CloudWatch::InsightRule``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
    :cloudformationResource: AWS::CloudWatch::InsightRule
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        rule_body: builtins.str,
        rule_name: builtins.str,
        rule_state: builtins.str,
        tags: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, aws_cdk.core.CfnTag]]]] = None,
    ) -> None:
        """Create a new ``AWS::CloudWatch::InsightRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule_body: ``AWS::CloudWatch::InsightRule.RuleBody``.
        :param rule_name: ``AWS::CloudWatch::InsightRule.RuleName``.
        :param rule_state: ``AWS::CloudWatch::InsightRule.RuleState``.
        :param tags: ``AWS::CloudWatch::InsightRule.Tags``.
        """
        props = CfnInsightRuleProps(
            rule_body=rule_body, rule_name=rule_name, rule_state=rule_state, tags=tags
        )

        jsii.create(CfnInsightRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrRuleName")
    def attr_rule_name(self) -> builtins.str:
        """
        :cloudformationAttribute: RuleName
        """
        return jsii.get(self, "attrRuleName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudWatch::InsightRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleBody")
    def rule_body(self) -> builtins.str:
        """``AWS::CloudWatch::InsightRule.RuleBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulebody
        """
        return jsii.get(self, "ruleBody")

    @rule_body.setter # type: ignore
    def rule_body(self, value: builtins.str) -> None:
        jsii.set(self, "ruleBody", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        """``AWS::CloudWatch::InsightRule.RuleName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulename
        """
        return jsii.get(self, "ruleName")

    @rule_name.setter # type: ignore
    def rule_name(self, value: builtins.str) -> None:
        jsii.set(self, "ruleName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleState")
    def rule_state(self) -> builtins.str:
        """``AWS::CloudWatch::InsightRule.RuleState``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulestate
        """
        return jsii.get(self, "ruleState")

    @rule_state.setter # type: ignore
    def rule_state(self, value: builtins.str) -> None:
        jsii.set(self, "ruleState", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CfnInsightRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "rule_body": "ruleBody",
        "rule_name": "ruleName",
        "rule_state": "ruleState",
        "tags": "tags",
    },
)
class CfnInsightRuleProps:
    def __init__(
        self,
        *,
        rule_body: builtins.str,
        rule_name: builtins.str,
        rule_state: builtins.str,
        tags: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, aws_cdk.core.CfnTag]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudWatch::InsightRule``.

        :param rule_body: ``AWS::CloudWatch::InsightRule.RuleBody``.
        :param rule_name: ``AWS::CloudWatch::InsightRule.RuleName``.
        :param rule_state: ``AWS::CloudWatch::InsightRule.RuleState``.
        :param tags: ``AWS::CloudWatch::InsightRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "rule_body": rule_body,
            "rule_name": rule_name,
            "rule_state": rule_state,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule_body(self) -> builtins.str:
        """``AWS::CloudWatch::InsightRule.RuleBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulebody
        """
        result = self._values.get("rule_body")
        assert result is not None, "Required property 'rule_body' is missing"
        return result

    @builtins.property
    def rule_name(self) -> builtins.str:
        """``AWS::CloudWatch::InsightRule.RuleName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulename
        """
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return result

    @builtins.property
    def rule_state(self) -> builtins.str:
        """``AWS::CloudWatch::InsightRule.RuleState``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-rulestate
        """
        result = self._values.get("rule_state")
        assert result is not None, "Required property 'rule_state' is missing"
        return result

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, aws_cdk.core.CfnTag]]]]:
        """``AWS::CloudWatch::InsightRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-insightrule.html#cfn-cloudwatch-insightrule-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInsightRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMetricStream(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.CfnMetricStream",
):
    """A CloudFormation ``AWS::CloudWatch::MetricStream``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html
    :cloudformationResource: AWS::CloudWatch::MetricStream
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        firehose_arn: builtins.str,
        role_arn: builtins.str,
        exclude_filters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMetricStream.MetricStreamFilterProperty"]]]] = None,
        include_filters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMetricStream.MetricStreamFilterProperty"]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::CloudWatch::MetricStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firehose_arn: ``AWS::CloudWatch::MetricStream.FirehoseArn``.
        :param role_arn: ``AWS::CloudWatch::MetricStream.RoleArn``.
        :param exclude_filters: ``AWS::CloudWatch::MetricStream.ExcludeFilters``.
        :param include_filters: ``AWS::CloudWatch::MetricStream.IncludeFilters``.
        :param name: ``AWS::CloudWatch::MetricStream.Name``.
        :param tags: ``AWS::CloudWatch::MetricStream.Tags``.
        """
        props = CfnMetricStreamProps(
            firehose_arn=firehose_arn,
            role_arn=role_arn,
            exclude_filters=exclude_filters,
            include_filters=include_filters,
            name=name,
            tags=tags,
        )

        jsii.create(CfnMetricStream, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCreationDate")
    def attr_creation_date(self) -> builtins.str:
        """
        :cloudformationAttribute: CreationDate
        """
        return jsii.get(self, "attrCreationDate")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrLastUpdateDate")
    def attr_last_update_date(self) -> builtins.str:
        """
        :cloudformationAttribute: LastUpdateDate
        """
        return jsii.get(self, "attrLastUpdateDate")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        """
        :cloudformationAttribute: State
        """
        return jsii.get(self, "attrState")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudWatch::MetricStream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firehoseArn")
    def firehose_arn(self) -> builtins.str:
        """``AWS::CloudWatch::MetricStream.FirehoseArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-firehosearn
        """
        return jsii.get(self, "firehoseArn")

    @firehose_arn.setter # type: ignore
    def firehose_arn(self, value: builtins.str) -> None:
        jsii.set(self, "firehoseArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        """``AWS::CloudWatch::MetricStream.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="excludeFilters")
    def exclude_filters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMetricStream.MetricStreamFilterProperty"]]]]:
        """``AWS::CloudWatch::MetricStream.ExcludeFilters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-excludefilters
        """
        return jsii.get(self, "excludeFilters")

    @exclude_filters.setter # type: ignore
    def exclude_filters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMetricStream.MetricStreamFilterProperty"]]]],
    ) -> None:
        jsii.set(self, "excludeFilters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="includeFilters")
    def include_filters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMetricStream.MetricStreamFilterProperty"]]]]:
        """``AWS::CloudWatch::MetricStream.IncludeFilters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includefilters
        """
        return jsii.get(self, "includeFilters")

    @include_filters.setter # type: ignore
    def include_filters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMetricStream.MetricStreamFilterProperty"]]]],
    ) -> None:
        jsii.set(self, "includeFilters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::MetricStream.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudwatch.CfnMetricStream.MetricStreamFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"namespace": "namespace"},
    )
    class MetricStreamFilterProperty:
        def __init__(self, *, namespace: builtins.str) -> None:
            """
            :param namespace: ``CfnMetricStream.MetricStreamFilterProperty.Namespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "namespace": namespace,
            }

        @builtins.property
        def namespace(self) -> builtins.str:
            """``CfnMetricStream.MetricStreamFilterProperty.Namespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-metricstream-metricstreamfilter.html#cfn-cloudwatch-metricstream-metricstreamfilter-namespace
            """
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStreamFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CfnMetricStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "firehose_arn": "firehoseArn",
        "role_arn": "roleArn",
        "exclude_filters": "excludeFilters",
        "include_filters": "includeFilters",
        "name": "name",
        "tags": "tags",
    },
)
class CfnMetricStreamProps:
    def __init__(
        self,
        *,
        firehose_arn: builtins.str,
        role_arn: builtins.str,
        exclude_filters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMetricStream.MetricStreamFilterProperty]]]] = None,
        include_filters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMetricStream.MetricStreamFilterProperty]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudWatch::MetricStream``.

        :param firehose_arn: ``AWS::CloudWatch::MetricStream.FirehoseArn``.
        :param role_arn: ``AWS::CloudWatch::MetricStream.RoleArn``.
        :param exclude_filters: ``AWS::CloudWatch::MetricStream.ExcludeFilters``.
        :param include_filters: ``AWS::CloudWatch::MetricStream.IncludeFilters``.
        :param name: ``AWS::CloudWatch::MetricStream.Name``.
        :param tags: ``AWS::CloudWatch::MetricStream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "firehose_arn": firehose_arn,
            "role_arn": role_arn,
        }
        if exclude_filters is not None:
            self._values["exclude_filters"] = exclude_filters
        if include_filters is not None:
            self._values["include_filters"] = include_filters
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firehose_arn(self) -> builtins.str:
        """``AWS::CloudWatch::MetricStream.FirehoseArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-firehosearn
        """
        result = self._values.get("firehose_arn")
        assert result is not None, "Required property 'firehose_arn' is missing"
        return result

    @builtins.property
    def role_arn(self) -> builtins.str:
        """``AWS::CloudWatch::MetricStream.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-rolearn
        """
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return result

    @builtins.property
    def exclude_filters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMetricStream.MetricStreamFilterProperty]]]]:
        """``AWS::CloudWatch::MetricStream.ExcludeFilters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-excludefilters
        """
        result = self._values.get("exclude_filters")
        return result

    @builtins.property
    def include_filters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMetricStream.MetricStreamFilterProperty]]]]:
        """``AWS::CloudWatch::MetricStream.IncludeFilters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-includefilters
        """
        result = self._values.get("include_filters")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudWatch::MetricStream.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CloudWatch::MetricStream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-metricstream.html#cfn-cloudwatch-metricstream-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Color(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Color"):
    """A set of standard colours that can be used in annotations in a GraphWidget."""

    def __init__(self) -> None:
        jsii.create(Color, self, [])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="BLUE")
    def BLUE(cls) -> builtins.str:
        """blue - hex #1f77b4."""
        return jsii.sget(cls, "BLUE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="BROWN")
    def BROWN(cls) -> builtins.str:
        """brown - hex #8c564b."""
        return jsii.sget(cls, "BROWN")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GREEN")
    def GREEN(cls) -> builtins.str:
        """green - hex #2ca02c."""
        return jsii.sget(cls, "GREEN")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GREY")
    def GREY(cls) -> builtins.str:
        """grey - hex #7f7f7f."""
        return jsii.sget(cls, "GREY")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ORANGE")
    def ORANGE(cls) -> builtins.str:
        """orange - hex #ff7f0e."""
        return jsii.sget(cls, "ORANGE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PINK")
    def PINK(cls) -> builtins.str:
        """pink - hex #e377c2."""
        return jsii.sget(cls, "PINK")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PURPLE")
    def PURPLE(cls) -> builtins.str:
        """purple - hex #9467bd."""
        return jsii.sget(cls, "PURPLE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="RED")
    def RED(cls) -> builtins.str:
        """red - hex #d62728."""
        return jsii.sget(cls, "RED")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CommonMetricOptions",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "color": "color",
        "dimensions": "dimensions",
        "label": "label",
        "period": "period",
        "region": "region",
        "statistic": "statistic",
        "unit": "unit",
    },
)
class CommonMetricOptions:
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        """Options shared by most methods accepting metric options.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if color is not None:
            self._values["color"] = color
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period
        if region is not None:
            self._values["region"] = region
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """Account which this metric comes from.

        :default: - Deployment account.
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.

        :default: - Automatic color
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Dimensions of the metric.

        :default: - No dimensions.
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """Label for this metric when added to a Graph in a Dashboard.

        :default: - No label
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        :default: Duration.minutes(5)
        """
        result = self._values.get("period")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """Region which this metric comes from.

        :default: - Deployment region.
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        :default: Average
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        The default is to use all matric datums in the stream, regardless of unit,
        which is recommended in nearly all cases.

        CloudWatch does not honor this property for graphs.

        :default: - All metric datums in the given metric stream
        """
        result = self._values.get("unit")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonMetricOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.ComparisonOperator")
class ComparisonOperator(enum.Enum):
    """Comparison operator for evaluating alarms."""

    GREATER_THAN_OR_EQUAL_TO_THRESHOLD = "GREATER_THAN_OR_EQUAL_TO_THRESHOLD"
    """Specified statistic is greater than or equal to the threshold."""
    GREATER_THAN_THRESHOLD = "GREATER_THAN_THRESHOLD"
    """Specified statistic is strictly greater than the threshold."""
    LESS_THAN_THRESHOLD = "LESS_THAN_THRESHOLD"
    """Specified statistic is strictly less than the threshold."""
    LESS_THAN_OR_EQUAL_TO_THRESHOLD = "LESS_THAN_OR_EQUAL_TO_THRESHOLD"
    """Specified statistic is less than or equal to the threshold."""
    LESS_THAN_LOWER_OR_GREATER_THAN_UPPER_THRESHOLD = "LESS_THAN_LOWER_OR_GREATER_THAN_UPPER_THRESHOLD"
    """Specified statistic is lower than or greater than the anomaly model band.

    Used only for alarms based on anomaly detection models
    """
    GREATER_THAN_UPPER_THRESHOLD = "GREATER_THAN_UPPER_THRESHOLD"
    """Specified statistic is greater than the anomaly model band.

    Used only for alarms based on anomaly detection models
    """
    LESS_THAN_LOWER_THRESHOLD = "LESS_THAN_LOWER_THRESHOLD"
    """Specified statistic is lower than the anomaly model band.

    Used only for alarms based on anomaly detection models
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CompositeAlarmProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_rule": "alarmRule",
        "actions_enabled": "actionsEnabled",
        "alarm_description": "alarmDescription",
        "composite_alarm_name": "compositeAlarmName",
    },
)
class CompositeAlarmProps:
    def __init__(
        self,
        *,
        alarm_rule: "IAlarmRule",
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        composite_alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for creating a Composite Alarm.

        :param alarm_rule: Expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param composite_alarm_name: Name of the alarm. Default: Automatically generated name
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alarm_rule": alarm_rule,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if composite_alarm_name is not None:
            self._values["composite_alarm_name"] = composite_alarm_name

    @builtins.property
    def alarm_rule(self) -> "IAlarmRule":
        """Expression that specifies which other alarms are to be evaluated to determine this composite alarm's state."""
        result = self._values.get("alarm_rule")
        assert result is not None, "Required property 'alarm_rule' is missing"
        return result

    @builtins.property
    def actions_enabled(self) -> typing.Optional[builtins.bool]:
        """Whether the actions for this alarm are enabled.

        :default: true
        """
        result = self._values.get("actions_enabled")
        return result

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        """Description for the alarm.

        :default: No description
        """
        result = self._values.get("alarm_description")
        return result

    @builtins.property
    def composite_alarm_name(self) -> typing.Optional[builtins.str]:
        """Name of the alarm.

        :default: Automatically generated name
        """
        result = self._values.get("composite_alarm_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompositeAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.CreateAlarmOptions",
    jsii_struct_bases=[],
    name_mapping={
        "evaluation_periods": "evaluationPeriods",
        "threshold": "threshold",
        "actions_enabled": "actionsEnabled",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "comparison_operator": "comparisonOperator",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
        "period": "period",
        "statistic": "statistic",
        "treat_missing_data": "treatMissingData",
    },
)
class CreateAlarmOptions:
    def __init__(
        self,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional["TreatMissingData"] = None,
    ) -> None:
        """Properties needed to make an alarm from a metric.

        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        self._values: typing.Dict[str, typing.Any] = {
            "evaluation_periods": evaluation_periods,
            "threshold": threshold,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if comparison_operator is not None:
            self._values["comparison_operator"] = comparison_operator
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluate_low_sample_count_percentile is not None:
            self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if period is not None:
            self._values["period"] = period
        if statistic is not None:
            self._values["statistic"] = statistic
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        """The number of periods over which data is compared to the specified threshold."""
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return result

    @builtins.property
    def threshold(self) -> jsii.Number:
        """The value against which the specified statistic is compared."""
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return result

    @builtins.property
    def actions_enabled(self) -> typing.Optional[builtins.bool]:
        """Whether the actions for this alarm are enabled.

        :default: true
        """
        result = self._values.get("actions_enabled")
        return result

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        """Description for the alarm.

        :default: No description
        """
        result = self._values.get("alarm_description")
        return result

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        """Name of the alarm.

        :default: Automatically generated name
        """
        result = self._values.get("alarm_name")
        return result

    @builtins.property
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        """Comparison to use to check if metric is breaching.

        :default: GreaterThanOrEqualToThreshold
        """
        result = self._values.get("comparison_operator")
        return result

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M
        out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon
        CloudWatch User Guide.

        :default: ``evaluationPeriods``

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation
        """
        result = self._values.get("datapoints_to_alarm")
        return result

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        """Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant.

        Used only for alarms that are based on percentiles.

        :default: - Not configured.
        """
        result = self._values.get("evaluate_low_sample_count_percentile")
        return result

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) The period over which the specified statistic is applied.

        Cannot be used with ``MathExpression`` objects.

        :default: - The period from the metric

        :deprecated: Use ``metric.with({ period: ... })`` to encode the period into the Metric object

        :stability: deprecated
        """
        result = self._values.get("period")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        """(deprecated) What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        Cannot be used with ``MathExpression`` objects.

        :default: - The statistic from the metric

        :deprecated: Use ``metric.with({ statistic: ... })`` to encode the period into the Metric object

        :stability: deprecated
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def treat_missing_data(self) -> typing.Optional["TreatMissingData"]:
        """Sets how this alarm is to handle missing data points.

        :default: TreatMissingData.Missing
        """
        result = self._values.get("treat_missing_data")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateAlarmOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Dashboard(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.Dashboard",
):
    """A CloudWatch dashboard."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        dashboard_name: typing.Optional[builtins.str] = None,
        end: typing.Optional[builtins.str] = None,
        period_override: typing.Optional["PeriodOverride"] = None,
        start: typing.Optional[builtins.str] = None,
        widgets: typing.Optional[typing.List[typing.List["IWidget"]]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param dashboard_name: Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets
        """
        props = DashboardProps(
            dashboard_name=dashboard_name,
            end=end,
            period_override=period_override,
            start=start,
            widgets=widgets,
        )

        jsii.create(Dashboard, self, [scope, id, props])

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: "IWidget") -> None:
        """Add a widget to the dashboard.

        Widgets given in multiple calls to add() will be laid out stacked on
        top of each other.

        Multiple widgets added in the same call to add() will be laid out next
        to each other.

        :param widgets: -
        """
        return jsii.invoke(self, "addWidgets", [*widgets])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.DashboardProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_name": "dashboardName",
        "end": "end",
        "period_override": "periodOverride",
        "start": "start",
        "widgets": "widgets",
    },
)
class DashboardProps:
    def __init__(
        self,
        *,
        dashboard_name: typing.Optional[builtins.str] = None,
        end: typing.Optional[builtins.str] = None,
        period_override: typing.Optional["PeriodOverride"] = None,
        start: typing.Optional[builtins.str] = None,
        widgets: typing.Optional[typing.List[typing.List["IWidget"]]] = None,
    ) -> None:
        """Properties for defining a CloudWatch Dashboard.

        :param dashboard_name: Name of the dashboard. If set, must only contain alphanumerics, dash (-) and underscore (_) Default: - automatically generated name
        :param end: The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
        :param period_override: Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
        :param start: The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        :param widgets: Initial set of widgets on the dashboard. One array represents a row of widgets. Default: - No widgets
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name
        if end is not None:
            self._values["end"] = end
        if period_override is not None:
            self._values["period_override"] = period_override
        if start is not None:
            self._values["start"] = start
        if widgets is not None:
            self._values["widgets"] = widgets

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        """Name of the dashboard.

        If set, must only contain alphanumerics, dash (-) and underscore (_)

        :default: - automatically generated name
        """
        result = self._values.get("dashboard_name")
        return result

    @builtins.property
    def end(self) -> typing.Optional[builtins.str]:
        """The end of the time range to use for each widget on the dashboard when the dashboard loads.

        If you specify a value for end, you must also specify a value for start.
        Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        :default: When the dashboard loads, the end date will be the current time.
        """
        result = self._values.get("end")
        return result

    @builtins.property
    def period_override(self) -> typing.Optional["PeriodOverride"]:
        """Use this field to specify the period for the graphs when the dashboard loads.

        Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard.
        Specifying ``Inherit`` ensures that the period set for each graph is always obeyed.

        :default: Auto
        """
        result = self._values.get("period_override")
        return result

    @builtins.property
    def start(self) -> typing.Optional[builtins.str]:
        """The start of the time range to use for each widget on the dashboard.

        You can specify start without specifying end to specify a relative time range that ends with the current time.
        In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for
        minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months.
        You can also use start along with an end field, to specify an absolute time range.
        When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

        :default: When the dashboard loads, the start time will be the default time range.
        """
        result = self._values.get("start")
        return result

    @builtins.property
    def widgets(self) -> typing.Optional[typing.List[typing.List["IWidget"]]]:
        """Initial set of widgets on the dashboard.

        One array represents a row of widgets.

        :default: - No widgets
        """
        result = self._values.get("widgets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.Dimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Dimension:
    def __init__(self, *, name: builtins.str, value: typing.Any) -> None:
        """Metric dimension.

        :param name: Name of the dimension.
        :param value: Value of the dimension.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        """Name of the dimension."""
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def value(self) -> typing.Any:
        """Value of the dimension."""
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Dimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.GraphWidgetView")
class GraphWidgetView(enum.Enum):
    """Types of view."""

    TIME_SERIES = "TIME_SERIES"
    """Display as a line graph."""
    BAR = "BAR"
    """Display as a bar graph."""
    PIE = "PIE"
    """Display as a pie graph."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.HorizontalAnnotation",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "color": "color",
        "fill": "fill",
        "label": "label",
        "visible": "visible",
    },
)
class HorizontalAnnotation:
    def __init__(
        self,
        *,
        value: jsii.Number,
        color: typing.Optional[builtins.str] = None,
        fill: typing.Optional["Shading"] = None,
        label: typing.Optional[builtins.str] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Horizontal annotation to be added to a graph.

        :param value: The value of the annotation.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to be used for the annotation. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param fill: Add shading above or below the annotation. Default: No shading
        :param label: Label for the annotation. Default: - No label
        :param visible: Whether the annotation is visible. Default: true
        """
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }
        if color is not None:
            self._values["color"] = color
        if fill is not None:
            self._values["fill"] = fill
        if label is not None:
            self._values["label"] = label
        if visible is not None:
            self._values["visible"] = visible

    @builtins.property
    def value(self) -> jsii.Number:
        """The value of the annotation."""
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """The hex color code, prefixed with '#' (e.g. '#00ff00'), to be used for the annotation. The ``Color`` class has a set of standard colors that can be used here.

        :default: - Automatic color
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def fill(self) -> typing.Optional["Shading"]:
        """Add shading above or below the annotation.

        :default: No shading
        """
        result = self._values.get("fill")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """Label for the annotation.

        :default: - No label
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def visible(self) -> typing.Optional[builtins.bool]:
        """Whether the annotation is visible.

        :default: true
        """
        result = self._values.get("visible")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HorizontalAnnotation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarmAction")
class IAlarmAction(typing_extensions.Protocol):
    """Interface for objects that can be the targets of CloudWatch alarm actions."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAlarmActionProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, alarm: "IAlarm") -> AlarmActionConfig:
        """Return the properties required to send alarm actions to this CloudWatch alarm.

        :param scope: root Construct that allows creating new Constructs.
        :param alarm: CloudWatch alarm that the action will target.
        """
        ...


class _IAlarmActionProxy:
    """Interface for objects that can be the targets of CloudWatch alarm actions."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudwatch.IAlarmAction"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, alarm: "IAlarm") -> AlarmActionConfig:
        """Return the properties required to send alarm actions to this CloudWatch alarm.

        :param scope: root Construct that allows creating new Constructs.
        :param alarm: CloudWatch alarm that the action will target.
        """
        return jsii.invoke(self, "bind", [scope, alarm])


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarmRule")
class IAlarmRule(typing_extensions.Protocol):
    """Interface for Alarm Rule."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAlarmRuleProxy

    @jsii.member(jsii_name="renderAlarmRule")
    def render_alarm_rule(self) -> builtins.str:
        """serialized representation of Alarm Rule to be used when building the Composite Alarm resource."""
        ...


class _IAlarmRuleProxy:
    """Interface for Alarm Rule."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudwatch.IAlarmRule"

    @jsii.member(jsii_name="renderAlarmRule")
    def render_alarm_rule(self) -> builtins.str:
        """serialized representation of Alarm Rule to be used when building the Composite Alarm resource."""
        return jsii.invoke(self, "renderAlarmRule", [])


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IMetric")
class IMetric(typing_extensions.Protocol):
    """Interface for metrics."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IMetricProxy

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """(deprecated) Turn this metric object into an alarm configuration.

        :deprecated: Use ``toMetricsConfig()`` instead.

        :stability: deprecated
        """
        ...

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """(deprecated) Turn this metric object into a graph configuration.

        :deprecated: Use ``toMetricsConfig()`` instead.

        :stability: deprecated
        """
        ...

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        ...


class _IMetricProxy:
    """Interface for metrics."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudwatch.IMetric"

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """(deprecated) Turn this metric object into an alarm configuration.

        :deprecated: Use ``toMetricsConfig()`` instead.

        :stability: deprecated
        """
        return jsii.invoke(self, "toAlarmConfig", [])

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """(deprecated) Turn this metric object into a graph configuration.

        :deprecated: Use ``toMetricsConfig()`` instead.

        :stability: deprecated
        """
        return jsii.invoke(self, "toGraphConfig", [])

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        return jsii.invoke(self, "toMetricConfig", [])


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IWidget")
class IWidget(typing_extensions.Protocol):
    """A single dashboard widget."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IWidgetProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        ...

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        ...

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        ...


class _IWidgetProxy:
    """A single dashboard widget."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudwatch.IWidget"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.LegendPosition")
class LegendPosition(enum.Enum):
    """The position of the legend on a GraphWidget."""

    BOTTOM = "BOTTOM"
    """Legend appears below the graph (default)."""
    RIGHT = "RIGHT"
    """Add shading above the annotation."""
    HIDDEN = "HIDDEN"
    """Add shading below the annotation."""


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.LogQueryVisualizationType")
class LogQueryVisualizationType(enum.Enum):
    """Types of view."""

    TABLE = "TABLE"
    """Table view."""
    LINE = "LINE"
    """Line view."""
    STACKEDAREA = "STACKEDAREA"
    """Stacked area view."""
    BAR = "BAR"
    """Bar view."""
    PIE = "PIE"
    """Pie view."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.LogQueryWidgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_names": "logGroupNames",
        "height": "height",
        "query_lines": "queryLines",
        "query_string": "queryString",
        "region": "region",
        "title": "title",
        "view": "view",
        "width": "width",
    },
)
class LogQueryWidgetProps:
    def __init__(
        self,
        *,
        log_group_names: typing.List[builtins.str],
        height: typing.Optional[jsii.Number] = None,
        query_lines: typing.Optional[typing.List[builtins.str]] = None,
        query_string: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        view: typing.Optional[LogQueryVisualizationType] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for a Query widget.

        :param log_group_names: Names of log groups to query.
        :param height: Height of the widget. Default: 6
        :param query_lines: A sequence of lines to use to build the query. The query will be built by joining the lines together using ``\\n|``. Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param query_string: Full query string for log insights. Be sure to prepend every new line with a newline and pipe character (``\\n|``). Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param region: The region the metrics of this widget should be taken from. Default: Current region
        :param title: Title for the widget. Default: No title
        :param view: The type of view to use. Default: LogQueryVisualizationType.TABLE
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        self._values: typing.Dict[str, typing.Any] = {
            "log_group_names": log_group_names,
        }
        if height is not None:
            self._values["height"] = height
        if query_lines is not None:
            self._values["query_lines"] = query_lines
        if query_string is not None:
            self._values["query_string"] = query_string
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if view is not None:
            self._values["view"] = view
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def log_group_names(self) -> typing.List[builtins.str]:
        """Names of log groups to query."""
        result = self._values.get("log_group_names")
        assert result is not None, "Required property 'log_group_names' is missing"
        return result

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        :default: 6
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def query_lines(self) -> typing.Optional[typing.List[builtins.str]]:
        """A sequence of lines to use to build the query.

        The query will be built by joining the lines together using ``\\n|``.

        :default: - Exactly one of ``queryString``, ``queryLines`` is required.
        """
        result = self._values.get("query_lines")
        return result

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        """Full query string for log insights.

        Be sure to prepend every new line with a newline and pipe character
        (``\\n|``).

        :default: - Exactly one of ``queryString``, ``queryLines`` is required.
        """
        result = self._values.get("query_string")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region the metrics of this widget should be taken from.

        :default: Current region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        """Title for the widget.

        :default: No title
        """
        result = self._values.get("title")
        return result

    @builtins.property
    def view(self) -> typing.Optional[LogQueryVisualizationType]:
        """The type of view to use.

        :default: LogQueryVisualizationType.TABLE
        """
        result = self._values.get("view")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        :default: 6
        """
        result = self._values.get("width")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogQueryWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMetric)
class MathExpression(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.MathExpression",
):
    """A math expression built with metric(s) emitted by a service.

    The math expression is a combination of an expression (x+y) and metrics to apply expression on.
    It also contains metadata which is used only in graphs, such as color and label.
    It makes sense to embed this in here, so that compound constructs can attach
    that metadata to metrics they expose.

    This class does not represent a resource, so hence is not a construct. Instead,
    MathExpression is an abstraction that makes it easy to specify metrics for use in both
    alarms and graphs.
    """

    def __init__(
        self,
        *,
        expression: builtins.str,
        using_metrics: typing.Mapping[builtins.str, IMetric],
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param expression: The expression defining the metric.
        :param using_metrics: The metrics used in the expression, in a map. The key is the identifier that represents the given metric in the expression, and the value is the actual Metric object.
        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        """
        props = MathExpressionProps(
            expression=expression,
            using_metrics=using_metrics,
            color=color,
            label=label,
            period=period,
        )

        jsii.create(MathExpression, self, [props])

    @jsii.member(jsii_name="createAlarm")
    def create_alarm(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional["TreatMissingData"] = None,
    ) -> "Alarm":
        """Make a new Alarm for this metric.

        Combines both properties that may adjust the metric (aggregation) as well
        as alarm properties.

        :param scope: -
        :param id: -
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props = CreateAlarmOptions(
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            comparison_operator=comparison_operator,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            period=period,
            statistic=statistic,
            treat_missing_data=treat_missing_data,
        )

        return jsii.invoke(self, "createAlarm", [scope, id, props])

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """Turn this metric object into an alarm configuration."""
        return jsii.invoke(self, "toAlarmConfig", [])

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """Turn this metric object into a graph configuration."""
        return jsii.invoke(self, "toGraphConfig", [])

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        return jsii.invoke(self, "toMetricConfig", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="with")
    def with_(
        self,
        *,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "MathExpression":
        """Return a copy of Metric with properties changed.

        All properties except namespace and metricName can be changed.

        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        """
        props = MathExpressionOptions(color=color, label=label, period=period)

        return jsii.invoke(self, "with", [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        """The expression defining the metric."""
        return jsii.get(self, "expression")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="period")
    def period(self) -> aws_cdk.core.Duration:
        """Aggregation period of this metric."""
        return jsii.get(self, "period")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="usingMetrics")
    def using_metrics(self) -> typing.Mapping[builtins.str, IMetric]:
        """The metrics used in the expression as KeyValuePair <id, metric>."""
        return jsii.get(self, "usingMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[builtins.str]:
        """The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here."""
        return jsii.get(self, "color")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[builtins.str]:
        """Label for this metric when added to a Graph."""
        return jsii.get(self, "label")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MathExpressionOptions",
    jsii_struct_bases=[],
    name_mapping={"color": "color", "label": "label", "period": "period"},
)
class MathExpressionOptions:
    def __init__(
        self,
        *,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Configurable options for MathExpressions.

        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if color is not None:
            self._values["color"] = color
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """Color for this metric when added to a Graph in a Dashboard.

        :default: - Automatic color
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """Label for this metric when added to a Graph in a Dashboard.

        :default: - Expression value is used as label
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the expression's statistics are applied.

        This period overrides all periods in the metrics used in this
        math expression.

        :default: Duration.minutes(5)
        """
        result = self._values.get("period")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MathExpressionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MathExpressionProps",
    jsii_struct_bases=[MathExpressionOptions],
    name_mapping={
        "color": "color",
        "label": "label",
        "period": "period",
        "expression": "expression",
        "using_metrics": "usingMetrics",
    },
)
class MathExpressionProps(MathExpressionOptions):
    def __init__(
        self,
        *,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        expression: builtins.str,
        using_metrics: typing.Mapping[builtins.str, IMetric],
    ) -> None:
        """Properties for a MathExpression.

        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - Expression value is used as label
        :param period: The period over which the expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        :param expression: The expression defining the metric.
        :param using_metrics: The metrics used in the expression, in a map. The key is the identifier that represents the given metric in the expression, and the value is the actual Metric object.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "expression": expression,
            "using_metrics": using_metrics,
        }
        if color is not None:
            self._values["color"] = color
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """Color for this metric when added to a Graph in a Dashboard.

        :default: - Automatic color
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """Label for this metric when added to a Graph in a Dashboard.

        :default: - Expression value is used as label
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the expression's statistics are applied.

        This period overrides all periods in the metrics used in this
        math expression.

        :default: Duration.minutes(5)
        """
        result = self._values.get("period")
        return result

    @builtins.property
    def expression(self) -> builtins.str:
        """The expression defining the metric."""
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return result

    @builtins.property
    def using_metrics(self) -> typing.Mapping[builtins.str, IMetric]:
        """The metrics used in the expression, in a map.

        The key is the identifier that represents the given metric in the
        expression, and the value is the actual Metric object.
        """
        result = self._values.get("using_metrics")
        assert result is not None, "Required property 'using_metrics' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MathExpressionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IMetric)
class Metric(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Metric"):
    """A metric emitted by a service.

    The metric is a combination of a metric identifier (namespace, name and dimensions)
    and an aggregation function (statistic, period and unit).

    It also contains metadata which is used only in graphs, such as color and label.
    It makes sense to embed this in here, so that compound constructs can attach
    that metadata to metrics they expose.

    This class does not represent a resource, so hence is not a construct. Instead,
    Metric is an abstraction that makes it easy to specify metrics for use in both
    alarms and graphs.
    """

    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        """
        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        props = MetricProps(
            metric_name=metric_name,
            namespace=namespace,
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        jsii.create(Metric, self, [props])

    @jsii.member(jsii_name="grantPutMetricData")
    @builtins.classmethod
    def grant_put_metric_data(
        cls,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant permissions to the given identity to write metrics.

        :param grantee: The IAM identity to give permissions to.
        """
        return jsii.sinvoke(cls, "grantPutMetricData", [grantee])

    @jsii.member(jsii_name="attachTo")
    def attach_to(self, scope: aws_cdk.core.Construct) -> "Metric":
        """Attach the metric object to the given construct scope.

        Returns a Metric object that uses the account and region from the Stack
        the given construct is defined in. If the metric is subsequently used
        in a Dashboard or Alarm in a different Stack defined in a different
        account or region, the appropriate 'region' and 'account' fields
        will be added to it.

        If the scope we attach to is in an environment-agnostic stack,
        nothing is done and the same Metric object is returned.

        :param scope: -
        """
        return jsii.invoke(self, "attachTo", [scope])

    @jsii.member(jsii_name="createAlarm")
    def create_alarm(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional["TreatMissingData"] = None,
    ) -> "Alarm":
        """Make a new Alarm for this metric.

        Combines both properties that may adjust the metric (aggregation) as well
        as alarm properties.

        :param scope: -
        :param id: -
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props = CreateAlarmOptions(
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            comparison_operator=comparison_operator,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            period=period,
            statistic=statistic,
            treat_missing_data=treat_missing_data,
        )

        return jsii.invoke(self, "createAlarm", [scope, id, props])

    @jsii.member(jsii_name="toAlarmConfig")
    def to_alarm_config(self) -> "MetricAlarmConfig":
        """Turn this metric object into an alarm configuration."""
        return jsii.invoke(self, "toAlarmConfig", [])

    @jsii.member(jsii_name="toGraphConfig")
    def to_graph_config(self) -> "MetricGraphConfig":
        """Turn this metric object into a graph configuration."""
        return jsii.invoke(self, "toGraphConfig", [])

    @jsii.member(jsii_name="toMetricConfig")
    def to_metric_config(self) -> "MetricConfig":
        """Inspect the details of the metric object."""
        return jsii.invoke(self, "toMetricConfig", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="with")
    def with_(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> "Metric":
        """Return a copy of Metric ``with`` properties changed.

        All properties except namespace and metricName can be changed.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        props = MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "with", [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        """Name of this metric."""
        return jsii.get(self, "metricName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        """Namespace of this metric."""
        return jsii.get(self, "namespace")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="period")
    def period(self) -> aws_cdk.core.Duration:
        """Period of this metric."""
        return jsii.get(self, "period")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> builtins.str:
        """Statistic of this metric."""
        return jsii.get(self, "statistic")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        """Account which this metric comes from."""
        return jsii.get(self, "account")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[builtins.str]:
        """The hex color code used when this metric is rendered on a graph."""
        return jsii.get(self, "color")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Dimensions of this metric."""
        return jsii.get(self, "dimensions")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[builtins.str]:
        """Label for this metric when added to a Graph in a Dashboard."""
        return jsii.get(self, "label")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        """Region which this metric comes from."""
        return jsii.get(self, "region")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional["Unit"]:
        """Unit of the metric."""
        return jsii.get(self, "unit")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricAlarmConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "period": "period",
        "dimensions": "dimensions",
        "extended_statistic": "extendedStatistic",
        "statistic": "statistic",
        "unit": "unit",
    },
)
class MetricAlarmConfig:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        period: jsii.Number,
        dimensions: typing.Optional[typing.List[Dimension]] = None,
        extended_statistic: typing.Optional[builtins.str] = None,
        statistic: typing.Optional["Statistic"] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        """(deprecated) Properties used to construct the Metric identifying part of an Alarm.

        :param metric_name: (deprecated) Name of the metric.
        :param namespace: (deprecated) Namespace of the metric.
        :param period: (deprecated) How many seconds to aggregate over.
        :param dimensions: (deprecated) The dimensions to apply to the alarm.
        :param extended_statistic: (deprecated) Percentile aggregation function to use.
        :param statistic: (deprecated) Simple aggregation function to use.
        :param unit: (deprecated) The unit of the alarm.

        :deprecated: Replaced by MetricConfig

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
            "period": period,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if extended_statistic is not None:
            self._values["extended_statistic"] = extended_statistic
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def metric_name(self) -> builtins.str:
        """(deprecated) Name of the metric.

        :stability: deprecated
        """
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return result

    @builtins.property
    def namespace(self) -> builtins.str:
        """(deprecated) Namespace of the metric.

        :stability: deprecated
        """
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return result

    @builtins.property
    def period(self) -> jsii.Number:
        """(deprecated) How many seconds to aggregate over.

        :stability: deprecated
        """
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return result

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List[Dimension]]:
        """(deprecated) The dimensions to apply to the alarm.

        :stability: deprecated
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def extended_statistic(self) -> typing.Optional[builtins.str]:
        """(deprecated) Percentile aggregation function to use.

        :stability: deprecated
        """
        result = self._values.get("extended_statistic")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional["Statistic"]:
        """(deprecated) Simple aggregation function to use.

        :stability: deprecated
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """(deprecated) The unit of the alarm.

        :stability: deprecated
        """
        result = self._values.get("unit")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricConfig",
    jsii_struct_bases=[],
    name_mapping={
        "math_expression": "mathExpression",
        "metric_stat": "metricStat",
        "rendering_properties": "renderingProperties",
    },
)
class MetricConfig:
    def __init__(
        self,
        *,
        math_expression: typing.Optional["MetricExpressionConfig"] = None,
        metric_stat: typing.Optional["MetricStatConfig"] = None,
        rendering_properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """Properties of a rendered metric.

        :param math_expression: In case the metric is a math expression, the details of the math expression. Default: - None
        :param metric_stat: In case the metric represents a query, the details of the query. Default: - None
        :param rendering_properties: Additional properties which will be rendered if the metric is used in a dashboard. Examples are 'label' and 'color', but any key in here will be added to dashboard graphs. Default: - None
        """
        if isinstance(math_expression, dict):
            math_expression = MetricExpressionConfig(**math_expression)
        if isinstance(metric_stat, dict):
            metric_stat = MetricStatConfig(**metric_stat)
        self._values: typing.Dict[str, typing.Any] = {}
        if math_expression is not None:
            self._values["math_expression"] = math_expression
        if metric_stat is not None:
            self._values["metric_stat"] = metric_stat
        if rendering_properties is not None:
            self._values["rendering_properties"] = rendering_properties

    @builtins.property
    def math_expression(self) -> typing.Optional["MetricExpressionConfig"]:
        """In case the metric is a math expression, the details of the math expression.

        :default: - None
        """
        result = self._values.get("math_expression")
        return result

    @builtins.property
    def metric_stat(self) -> typing.Optional["MetricStatConfig"]:
        """In case the metric represents a query, the details of the query.

        :default: - None
        """
        result = self._values.get("metric_stat")
        return result

    @builtins.property
    def rendering_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Additional properties which will be rendered if the metric is used in a dashboard.

        Examples are 'label' and 'color', but any key in here will be
        added to dashboard graphs.

        :default: - None
        """
        result = self._values.get("rendering_properties")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricExpressionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "period": "period",
        "using_metrics": "usingMetrics",
    },
)
class MetricExpressionConfig:
    def __init__(
        self,
        *,
        expression: builtins.str,
        period: jsii.Number,
        using_metrics: typing.Mapping[builtins.str, IMetric],
    ) -> None:
        """Properties for a concrete metric.

        :param expression: Math expression for the metric.
        :param period: How many seconds to aggregate over.
        :param using_metrics: Metrics used in the math expression.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "expression": expression,
            "period": period,
            "using_metrics": using_metrics,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        """Math expression for the metric."""
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return result

    @builtins.property
    def period(self) -> jsii.Number:
        """How many seconds to aggregate over."""
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return result

    @builtins.property
    def using_metrics(self) -> typing.Mapping[builtins.str, IMetric]:
        """Metrics used in the math expression."""
        result = self._values.get("using_metrics")
        assert result is not None, "Required property 'using_metrics' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricExpressionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricGraphConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "period": "period",
        "rendering_properties": "renderingProperties",
        "color": "color",
        "dimensions": "dimensions",
        "label": "label",
        "statistic": "statistic",
        "unit": "unit",
    },
)
class MetricGraphConfig:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        period: jsii.Number,
        rendering_properties: "MetricRenderingProperties",
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.List[Dimension]] = None,
        label: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        """(deprecated) Properties used to construct the Metric identifying part of a Graph.

        :param metric_name: (deprecated) Name of the metric.
        :param namespace: (deprecated) Namespace of the metric.
        :param period: (deprecated) How many seconds to aggregate over.
        :param rendering_properties: (deprecated) Rendering properties override yAxis parameter of the widget object.
        :param color: (deprecated) Color for the graph line.
        :param dimensions: (deprecated) The dimensions to apply to the alarm.
        :param label: (deprecated) Label for the metric.
        :param statistic: (deprecated) Aggregation function to use (can be either simple or a percentile).
        :param unit: (deprecated) The unit of the alarm.

        :deprecated: Replaced by MetricConfig

        :stability: deprecated
        """
        if isinstance(rendering_properties, dict):
            rendering_properties = MetricRenderingProperties(**rendering_properties)
        self._values: typing.Dict[str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
            "period": period,
            "rendering_properties": rendering_properties,
        }
        if color is not None:
            self._values["color"] = color
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if label is not None:
            self._values["label"] = label
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def metric_name(self) -> builtins.str:
        """(deprecated) Name of the metric.

        :stability: deprecated
        """
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return result

    @builtins.property
    def namespace(self) -> builtins.str:
        """(deprecated) Namespace of the metric.

        :stability: deprecated
        """
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return result

    @builtins.property
    def period(self) -> jsii.Number:
        """(deprecated) How many seconds to aggregate over.

        :deprecated: Use ``period`` in ``renderingProperties``

        :stability: deprecated
        """
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return result

    @builtins.property
    def rendering_properties(self) -> "MetricRenderingProperties":
        """(deprecated) Rendering properties override yAxis parameter of the widget object.

        :stability: deprecated
        """
        result = self._values.get("rendering_properties")
        assert result is not None, "Required property 'rendering_properties' is missing"
        return result

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """(deprecated) Color for the graph line.

        :deprecated: Use ``color`` in ``renderingProperties``

        :stability: deprecated
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List[Dimension]]:
        """(deprecated) The dimensions to apply to the alarm.

        :stability: deprecated
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """(deprecated) Label for the metric.

        :deprecated: Use ``label`` in ``renderingProperties``

        :stability: deprecated
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        """(deprecated) Aggregation function to use (can be either simple or a percentile).

        :deprecated: Use ``stat`` in ``renderingProperties``

        :stability: deprecated
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """(deprecated) The unit of the alarm.

        :deprecated: not used in dashboard widgets

        :stability: deprecated
        """
        result = self._values.get("unit")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricGraphConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricOptions",
    jsii_struct_bases=[CommonMetricOptions],
    name_mapping={
        "account": "account",
        "color": "color",
        "dimensions": "dimensions",
        "label": "label",
        "period": "period",
        "region": "region",
        "statistic": "statistic",
        "unit": "unit",
    },
)
class MetricOptions(CommonMetricOptions):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
    ) -> None:
        """Properties of a metric that can be changed.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if color is not None:
            self._values["color"] = color
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period
        if region is not None:
            self._values["region"] = region
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """Account which this metric comes from.

        :default: - Deployment account.
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.

        :default: - Automatic color
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Dimensions of the metric.

        :default: - No dimensions.
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """Label for this metric when added to a Graph in a Dashboard.

        :default: - No label
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        :default: Duration.minutes(5)
        """
        result = self._values.get("period")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """Region which this metric comes from.

        :default: - Deployment region.
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        :default: Average
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        The default is to use all matric datums in the stream, regardless of unit,
        which is recommended in nearly all cases.

        CloudWatch does not honor this property for graphs.

        :default: - All metric datums in the given metric stream
        """
        result = self._values.get("unit")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricProps",
    jsii_struct_bases=[CommonMetricOptions],
    name_mapping={
        "account": "account",
        "color": "color",
        "dimensions": "dimensions",
        "label": "label",
        "period": "period",
        "region": "region",
        "statistic": "statistic",
        "unit": "unit",
        "metric_name": "metricName",
        "namespace": "namespace",
    },
)
class MetricProps(CommonMetricOptions):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["Unit"] = None,
        metric_name: builtins.str,
        namespace: builtins.str,
    ) -> None:
        """Properties for a metric.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
        }
        if account is not None:
            self._values["account"] = account
        if color is not None:
            self._values["color"] = color
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if label is not None:
            self._values["label"] = label
        if period is not None:
            self._values["period"] = period
        if region is not None:
            self._values["region"] = region
        if statistic is not None:
            self._values["statistic"] = statistic
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """Account which this metric comes from.

        :default: - Deployment account.
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.

        :default: - Automatic color
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Dimensions of the metric.

        :default: - No dimensions.
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """Label for this metric when added to a Graph in a Dashboard.

        :default: - No label
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period over which the specified statistic is applied.

        :default: Duration.minutes(5)
        """
        result = self._values.get("period")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """Region which this metric comes from.

        :default: - Deployment region.
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        """What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        :default: Average
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        The default is to use all matric datums in the stream, regardless of unit,
        which is recommended in nearly all cases.

        CloudWatch does not honor this property for graphs.

        :default: - All metric datums in the given metric stream
        """
        result = self._values.get("unit")
        return result

    @builtins.property
    def metric_name(self) -> builtins.str:
        """Name of the metric."""
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return result

    @builtins.property
    def namespace(self) -> builtins.str:
        """Namespace of the metric."""
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricRenderingProperties",
    jsii_struct_bases=[],
    name_mapping={
        "period": "period",
        "color": "color",
        "label": "label",
        "stat": "stat",
    },
)
class MetricRenderingProperties:
    def __init__(
        self,
        *,
        period: jsii.Number,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        stat: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Custom rendering properties that override the default rendering properties specified in the yAxis parameter of the widget object.

        :param period: (deprecated) How many seconds to aggregate over.
        :param color: (deprecated) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.
        :param label: (deprecated) Label for the metric.
        :param stat: (deprecated) Aggregation function to use (can be either simple or a percentile).

        :deprecated: Replaced by MetricConfig.

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "period": period,
        }
        if color is not None:
            self._values["color"] = color
        if label is not None:
            self._values["label"] = label
        if stat is not None:
            self._values["stat"] = stat

    @builtins.property
    def period(self) -> jsii.Number:
        """(deprecated) How many seconds to aggregate over.

        :stability: deprecated
        """
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return result

    @builtins.property
    def color(self) -> typing.Optional[builtins.str]:
        """(deprecated) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here.

        :stability: deprecated
        """
        result = self._values.get("color")
        return result

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """(deprecated) Label for the metric.

        :stability: deprecated
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def stat(self) -> typing.Optional[builtins.str]:
        """(deprecated) Aggregation function to use (can be either simple or a percentile).

        :stability: deprecated
        """
        result = self._values.get("stat")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricRenderingProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricStatConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "namespace": "namespace",
        "period": "period",
        "statistic": "statistic",
        "account": "account",
        "dimensions": "dimensions",
        "region": "region",
        "unit_filter": "unitFilter",
    },
)
class MetricStatConfig:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        namespace: builtins.str,
        period: aws_cdk.core.Duration,
        statistic: builtins.str,
        account: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.List[Dimension]] = None,
        region: typing.Optional[builtins.str] = None,
        unit_filter: typing.Optional["Unit"] = None,
    ) -> None:
        """Properties for a concrete metric.

        NOTE: ``unit`` is no longer on this object since it is only used for ``Alarms``, and doesn't mean what one
        would expect it to mean there anyway. It is most likely to be misused.

        :param metric_name: Name of the metric.
        :param namespace: Namespace of the metric.
        :param period: How many seconds to aggregate over.
        :param statistic: Aggregation function to use (can be either simple or a percentile).
        :param account: Account which this metric comes from. Default: Deployment account.
        :param dimensions: The dimensions to apply to the alarm. Default: []
        :param region: Region which this metric comes from. Default: Deployment region.
        :param unit_filter: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. This field has been renamed from plain ``unit`` to clearly communicate its purpose. Default: - Refer to all metric datums
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metric_name": metric_name,
            "namespace": namespace,
            "period": period,
            "statistic": statistic,
        }
        if account is not None:
            self._values["account"] = account
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if region is not None:
            self._values["region"] = region
        if unit_filter is not None:
            self._values["unit_filter"] = unit_filter

    @builtins.property
    def metric_name(self) -> builtins.str:
        """Name of the metric."""
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return result

    @builtins.property
    def namespace(self) -> builtins.str:
        """Namespace of the metric."""
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return result

    @builtins.property
    def period(self) -> aws_cdk.core.Duration:
        """How many seconds to aggregate over."""
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return result

    @builtins.property
    def statistic(self) -> builtins.str:
        """Aggregation function to use (can be either simple or a percentile)."""
        result = self._values.get("statistic")
        assert result is not None, "Required property 'statistic' is missing"
        return result

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """Account which this metric comes from.

        :default: Deployment account.
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List[Dimension]]:
        """The dimensions to apply to the alarm.

        :default: []
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """Region which this metric comes from.

        :default: Deployment region.
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def unit_filter(self) -> typing.Optional["Unit"]:
        """Unit used to filter the metric stream.

        Only refer to datums emitted to the metric stream with the given unit and
        ignore all others. Only useful when datums are being emitted to the same
        metric stream under different units.

        This field has been renamed from plain ``unit`` to clearly communicate
        its purpose.

        :default: - Refer to all metric datums
        """
        result = self._values.get("unit_filter")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricStatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.MetricWidgetProps",
    jsii_struct_bases=[],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
    },
)
class MetricWidgetProps:
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Basic properties for widgets that display metrics.

        :param height: Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: The region the metrics of this graph should be taken from. Default: - Current region
        :param title: Title for the graph. Default: - None
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region the metrics of this graph should be taken from.

        :default: - Current region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        """Title for the graph.

        :default: - None
        """
        result = self._values.get("title")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        :default: 6
        """
        result = self._values.get("width")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.PeriodOverride")
class PeriodOverride(enum.Enum):
    """Specify the period for graphs when the CloudWatch dashboard loads."""

    AUTO = "AUTO"
    """Period of all graphs on the dashboard automatically adapt to the time range of the dashboard."""
    INHERIT = "INHERIT"
    """Period set for each graph will be used."""


@jsii.implements(IWidget)
class Row(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Row"):
    """A widget that contains other widgets in a horizontal row.

    Widgets will be laid out next to each other
    """

    def __init__(self, *widgets: IWidget) -> None:
        """
        :param widgets: -
        """
        jsii.create(Row, self, [*widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Shading")
class Shading(enum.Enum):
    """Fill shading options that will be used with an annotation."""

    NONE = "NONE"
    """Don't add shading."""
    ABOVE = "ABOVE"
    """Add shading above the annotation."""
    BELOW = "BELOW"
    """Add shading below the annotation."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidgetProps",
    jsii_struct_bases=[MetricWidgetProps],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
        "metrics": "metrics",
        "set_period_to_time_range": "setPeriodToTimeRange",
    },
)
class SingleValueWidgetProps(MetricWidgetProps):
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        metrics: typing.List[IMetric],
        set_period_to_time_range: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Properties for a SingleValueWidget.

        :param height: Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: The region the metrics of this graph should be taken from. Default: - Current region
        :param title: Title for the graph. Default: - None
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        :param metrics: Metrics to display.
        :param set_period_to_time_range: Whether to show the value from the entire time range. Default: false
        """
        self._values: typing.Dict[str, typing.Any] = {
            "metrics": metrics,
        }
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width
        if set_period_to_time_range is not None:
            self._values["set_period_to_time_range"] = set_period_to_time_range

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region the metrics of this graph should be taken from.

        :default: - Current region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        """Title for the graph.

        :default: - None
        """
        result = self._values.get("title")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        :default: 6
        """
        result = self._values.get("width")
        return result

    @builtins.property
    def metrics(self) -> typing.List[IMetric]:
        """Metrics to display."""
        result = self._values.get("metrics")
        assert result is not None, "Required property 'metrics' is missing"
        return result

    @builtins.property
    def set_period_to_time_range(self) -> typing.Optional[builtins.bool]:
        """Whether to show the value from the entire time range.

        :default: false
        """
        result = self._values.get("set_period_to_time_range")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SingleValueWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWidget)
class Spacer(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Spacer"):
    """A widget that doesn't display anything but takes up space."""

    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param height: Height of the spacer. Default: : 1
        :param width: Width of the spacer. Default: 1
        """
        props = SpacerProps(height=height, width=width)

        jsii.create(Spacer, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, _x: jsii.Number, _y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param _x: -
        :param _y: -
        """
        return jsii.invoke(self, "position", [_x, _y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.SpacerProps",
    jsii_struct_bases=[],
    name_mapping={"height": "height", "width": "width"},
)
class SpacerProps:
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Props of the spacer.

        :param height: Height of the spacer. Default: : 1
        :param width: Width of the spacer. Default: 1
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the spacer.

        :default: : 1
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the spacer.

        :default: 1
        """
        result = self._values.get("width")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpacerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Statistic")
class Statistic(enum.Enum):
    """Statistic to use over the aggregation period."""

    SAMPLE_COUNT = "SAMPLE_COUNT"
    """The count (number) of data points used for the statistical calculation."""
    AVERAGE = "AVERAGE"
    """The value of Sum / SampleCount during the specified period."""
    SUM = "SUM"
    """All values submitted for the matching metric added together.

    This statistic can be useful for determining the total volume of a metric.
    """
    MINIMUM = "MINIMUM"
    """The lowest value observed during the specified period.

    You can use this value to determine low volumes of activity for your application.
    """
    MAXIMUM = "MAXIMUM"
    """The highest value observed during the specified period.

    You can use this value to determine high volumes of activity for your application.
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.TextWidgetProps",
    jsii_struct_bases=[],
    name_mapping={"markdown": "markdown", "height": "height", "width": "width"},
)
class TextWidgetProps:
    def __init__(
        self,
        *,
        markdown: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for a Text widget.

        :param markdown: The text to display, in MarkDown format.
        :param height: Height of the widget. Default: 2
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        self._values: typing.Dict[str, typing.Any] = {
            "markdown": markdown,
        }
        if height is not None:
            self._values["height"] = height
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def markdown(self) -> builtins.str:
        """The text to display, in MarkDown format."""
        result = self._values.get("markdown")
        assert result is not None, "Required property 'markdown' is missing"
        return result

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        :default: 2
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        :default: 6
        """
        result = self._values.get("width")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.TreatMissingData")
class TreatMissingData(enum.Enum):
    """Specify how missing data points are treated during alarm evaluation."""

    BREACHING = "BREACHING"
    """Missing data points are treated as breaching the threshold."""
    NOT_BREACHING = "NOT_BREACHING"
    """Missing data points are treated as being within the threshold."""
    IGNORE = "IGNORE"
    """The current alarm state is maintained."""
    MISSING = "MISSING"
    """The alarm does not consider missing data points when evaluating whether to change state."""


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Unit")
class Unit(enum.Enum):
    """Unit for metric."""

    SECONDS = "SECONDS"
    """Seconds."""
    MICROSECONDS = "MICROSECONDS"
    """Microseconds."""
    MILLISECONDS = "MILLISECONDS"
    """Milliseconds."""
    BYTES = "BYTES"
    """Bytes."""
    KILOBYTES = "KILOBYTES"
    """Kilobytes."""
    MEGABYTES = "MEGABYTES"
    """Megabytes."""
    GIGABYTES = "GIGABYTES"
    """Gigabytes."""
    TERABYTES = "TERABYTES"
    """Terabytes."""
    BITS = "BITS"
    """Bits."""
    KILOBITS = "KILOBITS"
    """Kilobits."""
    MEGABITS = "MEGABITS"
    """Megabits."""
    GIGABITS = "GIGABITS"
    """Gigabits."""
    TERABITS = "TERABITS"
    """Terabits."""
    PERCENT = "PERCENT"
    """Percent."""
    COUNT = "COUNT"
    """Count."""
    BYTES_PER_SECOND = "BYTES_PER_SECOND"
    """Bytes/second (B/s)."""
    KILOBYTES_PER_SECOND = "KILOBYTES_PER_SECOND"
    """Kilobytes/second (kB/s)."""
    MEGABYTES_PER_SECOND = "MEGABYTES_PER_SECOND"
    """Megabytes/second (MB/s)."""
    GIGABYTES_PER_SECOND = "GIGABYTES_PER_SECOND"
    """Gigabytes/second (GB/s)."""
    TERABYTES_PER_SECOND = "TERABYTES_PER_SECOND"
    """Terabytes/second (TB/s)."""
    BITS_PER_SECOND = "BITS_PER_SECOND"
    """Bits/second (b/s)."""
    KILOBITS_PER_SECOND = "KILOBITS_PER_SECOND"
    """Kilobits/second (kb/s)."""
    MEGABITS_PER_SECOND = "MEGABITS_PER_SECOND"
    """Megabits/second (Mb/s)."""
    GIGABITS_PER_SECOND = "GIGABITS_PER_SECOND"
    """Gigabits/second (Gb/s)."""
    TERABITS_PER_SECOND = "TERABITS_PER_SECOND"
    """Terabits/second (Tb/s)."""
    COUNT_PER_SECOND = "COUNT_PER_SECOND"
    """Count/second."""
    NONE = "NONE"
    """No unit."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.YAxisProps",
    jsii_struct_bases=[],
    name_mapping={
        "label": "label",
        "max": "max",
        "min": "min",
        "show_units": "showUnits",
    },
)
class YAxisProps:
    def __init__(
        self,
        *,
        label: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        show_units: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Properties for a Y-Axis.

        :param label: The label. Default: - No label
        :param max: The max value. Default: - No maximum value
        :param min: The min value. Default: 0
        :param show_units: Whether to show units. Default: true
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if label is not None:
            self._values["label"] = label
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min
        if show_units is not None:
            self._values["show_units"] = show_units

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        """The label.

        :default: - No label
        """
        result = self._values.get("label")
        return result

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        """The max value.

        :default: - No maximum value
        """
        result = self._values.get("max")
        return result

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        """The min value.

        :default: 0
        """
        result = self._values.get("min")
        return result

    @builtins.property
    def show_units(self) -> typing.Optional[builtins.bool]:
        """Whether to show units.

        :default: true
        """
        result = self._values.get("show_units")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YAxisProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.AlarmProps",
    jsii_struct_bases=[CreateAlarmOptions],
    name_mapping={
        "evaluation_periods": "evaluationPeriods",
        "threshold": "threshold",
        "actions_enabled": "actionsEnabled",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "comparison_operator": "comparisonOperator",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluate_low_sample_count_percentile": "evaluateLowSampleCountPercentile",
        "period": "period",
        "statistic": "statistic",
        "treat_missing_data": "treatMissingData",
        "metric": "metric",
    },
)
class AlarmProps(CreateAlarmOptions):
    def __init__(
        self,
        *,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[TreatMissingData] = None,
        metric: IMetric,
    ) -> None:
        """Properties for Alarms.

        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        :param metric: The metric to add the alarm on. Metric objects can be obtained from most resources, or you can construct custom Metric objects by instantiating one.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "evaluation_periods": evaluation_periods,
            "threshold": threshold,
            "metric": metric,
        }
        if actions_enabled is not None:
            self._values["actions_enabled"] = actions_enabled
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if comparison_operator is not None:
            self._values["comparison_operator"] = comparison_operator
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluate_low_sample_count_percentile is not None:
            self._values["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        if period is not None:
            self._values["period"] = period
        if statistic is not None:
            self._values["statistic"] = statistic
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def evaluation_periods(self) -> jsii.Number:
        """The number of periods over which data is compared to the specified threshold."""
        result = self._values.get("evaluation_periods")
        assert result is not None, "Required property 'evaluation_periods' is missing"
        return result

    @builtins.property
    def threshold(self) -> jsii.Number:
        """The value against which the specified statistic is compared."""
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return result

    @builtins.property
    def actions_enabled(self) -> typing.Optional[builtins.bool]:
        """Whether the actions for this alarm are enabled.

        :default: true
        """
        result = self._values.get("actions_enabled")
        return result

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        """Description for the alarm.

        :default: No description
        """
        result = self._values.get("alarm_description")
        return result

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        """Name of the alarm.

        :default: Automatically generated name
        """
        result = self._values.get("alarm_name")
        return result

    @builtins.property
    def comparison_operator(self) -> typing.Optional[ComparisonOperator]:
        """Comparison to use to check if metric is breaching.

        :default: GreaterThanOrEqualToThreshold
        """
        result = self._values.get("comparison_operator")
        return result

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        """The number of datapoints that must be breaching to trigger the alarm.

        This is used only if you are setting an "M
        out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon
        CloudWatch User Guide.

        :default: ``evaluationPeriods``

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation
        """
        result = self._values.get("datapoints_to_alarm")
        return result

    @builtins.property
    def evaluate_low_sample_count_percentile(self) -> typing.Optional[builtins.str]:
        """Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant.

        Used only for alarms that are based on percentiles.

        :default: - Not configured.
        """
        result = self._values.get("evaluate_low_sample_count_percentile")
        return result

    @builtins.property
    def period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) The period over which the specified statistic is applied.

        Cannot be used with ``MathExpression`` objects.

        :default: - The period from the metric

        :deprecated: Use ``metric.with({ period: ... })`` to encode the period into the Metric object

        :stability: deprecated
        """
        result = self._values.get("period")
        return result

    @builtins.property
    def statistic(self) -> typing.Optional[builtins.str]:
        """(deprecated) What function to use for aggregating.

        Can be one of the following:

        - "Minimum" | "min"
        - "Maximum" | "max"
        - "Average" | "avg"
        - "Sum" | "sum"
        - "SampleCount | "n"
        - "pNN.NN"

        Cannot be used with ``MathExpression`` objects.

        :default: - The statistic from the metric

        :deprecated: Use ``metric.with({ statistic: ... })`` to encode the period into the Metric object

        :stability: deprecated
        """
        result = self._values.get("statistic")
        return result

    @builtins.property
    def treat_missing_data(self) -> typing.Optional[TreatMissingData]:
        """Sets how this alarm is to handle missing data points.

        :default: TreatMissingData.Missing
        """
        result = self._values.get("treat_missing_data")
        return result

    @builtins.property
    def metric(self) -> IMetric:
        """The metric to add the alarm on.

        Metric objects can be obtained from most resources, or you can construct
        custom Metric objects by instantiating one.
        """
        result = self._values.get("metric")
        assert result is not None, "Required property 'metric' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidgetProps",
    jsii_struct_bases=[MetricWidgetProps],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
        "alarm": "alarm",
        "left_y_axis": "leftYAxis",
    },
)
class AlarmWidgetProps(MetricWidgetProps):
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        alarm: "IAlarm",
        left_y_axis: typing.Optional[YAxisProps] = None,
    ) -> None:
        """Properties for an AlarmWidget.

        :param height: Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: The region the metrics of this graph should be taken from. Default: - Current region
        :param title: Title for the graph. Default: - None
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        :param alarm: The alarm to show.
        :param left_y_axis: Left Y axis. Default: - No minimum or maximum values for the left Y-axis
        """
        if isinstance(left_y_axis, dict):
            left_y_axis = YAxisProps(**left_y_axis)
        self._values: typing.Dict[str, typing.Any] = {
            "alarm": alarm,
        }
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width
        if left_y_axis is not None:
            self._values["left_y_axis"] = left_y_axis

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region the metrics of this graph should be taken from.

        :default: - Current region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        """Title for the graph.

        :default: - None
        """
        result = self._values.get("title")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        :default: 6
        """
        result = self._values.get("width")
        return result

    @builtins.property
    def alarm(self) -> "IAlarm":
        """The alarm to show."""
        result = self._values.get("alarm")
        assert result is not None, "Required property 'alarm' is missing"
        return result

    @builtins.property
    def left_y_axis(self) -> typing.Optional[YAxisProps]:
        """Left Y axis.

        :default: - No minimum or maximum values for the left Y-axis
        """
        result = self._values.get("left_y_axis")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWidget)
class Column(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Column"):
    """A widget that contains other widgets in a vertical column.

    Widgets will be laid out next to each other
    """

    def __init__(self, *widgets: IWidget) -> None:
        """
        :param widgets: -
        """
        jsii.create(Column, self, [*widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.implements(IWidget)
class ConcreteWidget(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-cloudwatch.ConcreteWidget",
):
    """A real CloudWatch widget that has its own fixed size and remembers its position.

    This is in contrast to other widgets which exist for layout purposes.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ConcreteWidgetProxy

    def __init__(self, width: jsii.Number, height: jsii.Number) -> None:
        """
        :param width: -
        :param height: -
        """
        jsii.create(ConcreteWidget, self, [width, height])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    @abc.abstractmethod
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="x")
    def _x(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "x")

    @_x.setter # type: ignore
    def _x(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "x", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="y")
    def _y(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "y")

    @_y.setter # type: ignore
    def _y(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "y", value)


class _ConcreteWidgetProxy(ConcreteWidget):
    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class GraphWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.GraphWidget",
):
    """A dashboard widget that displays metrics."""

    def __init__(
        self,
        *,
        left: typing.Optional[typing.List[IMetric]] = None,
        left_annotations: typing.Optional[typing.List[HorizontalAnnotation]] = None,
        left_y_axis: typing.Optional[YAxisProps] = None,
        legend_position: typing.Optional[LegendPosition] = None,
        live_data: typing.Optional[builtins.bool] = None,
        right: typing.Optional[typing.List[IMetric]] = None,
        right_annotations: typing.Optional[typing.List[HorizontalAnnotation]] = None,
        right_y_axis: typing.Optional[YAxisProps] = None,
        stacked: typing.Optional[builtins.bool] = None,
        view: typing.Optional[GraphWidgetView] = None,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param left: Metrics to display on left Y axis. Default: - No metrics
        :param left_annotations: Annotations for the left Y axis. Default: - No annotations
        :param left_y_axis: Left Y axis. Default: - None
        :param legend_position: Position of the legend. Default: - bottom
        :param live_data: Whether the graph should show live data. Default: false
        :param right: Metrics to display on right Y axis. Default: - No metrics
        :param right_annotations: Annotations for the right Y axis. Default: - No annotations
        :param right_y_axis: Right Y axis. Default: - None
        :param stacked: Whether the graph should be shown as stacked lines. Default: false
        :param view: Display this metric. Default: TimeSeries
        :param height: Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: The region the metrics of this graph should be taken from. Default: - Current region
        :param title: Title for the graph. Default: - None
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = GraphWidgetProps(
            left=left,
            left_annotations=left_annotations,
            left_y_axis=left_y_axis,
            legend_position=legend_position,
            live_data=live_data,
            right=right,
            right_annotations=right_annotations,
            right_y_axis=right_y_axis,
            stacked=stacked,
            view=view,
            height=height,
            region=region,
            title=title,
            width=width,
        )

        jsii.create(GraphWidget, self, [props])

    @jsii.member(jsii_name="addLeftMetric")
    def add_left_metric(self, metric: IMetric) -> None:
        """Add another metric to the left Y axis of the GraphWidget.

        :param metric: the metric to add.
        """
        return jsii.invoke(self, "addLeftMetric", [metric])

    @jsii.member(jsii_name="addRightMetric")
    def add_right_metric(self, metric: IMetric) -> None:
        """Add another metric to the right Y axis of the GraphWidget.

        :param metric: the metric to add.
        """
        return jsii.invoke(self, "addRightMetric", [metric])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudwatch.GraphWidgetProps",
    jsii_struct_bases=[MetricWidgetProps],
    name_mapping={
        "height": "height",
        "region": "region",
        "title": "title",
        "width": "width",
        "left": "left",
        "left_annotations": "leftAnnotations",
        "left_y_axis": "leftYAxis",
        "legend_position": "legendPosition",
        "live_data": "liveData",
        "right": "right",
        "right_annotations": "rightAnnotations",
        "right_y_axis": "rightYAxis",
        "stacked": "stacked",
        "view": "view",
    },
)
class GraphWidgetProps(MetricWidgetProps):
    def __init__(
        self,
        *,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
        left: typing.Optional[typing.List[IMetric]] = None,
        left_annotations: typing.Optional[typing.List[HorizontalAnnotation]] = None,
        left_y_axis: typing.Optional[YAxisProps] = None,
        legend_position: typing.Optional[LegendPosition] = None,
        live_data: typing.Optional[builtins.bool] = None,
        right: typing.Optional[typing.List[IMetric]] = None,
        right_annotations: typing.Optional[typing.List[HorizontalAnnotation]] = None,
        right_y_axis: typing.Optional[YAxisProps] = None,
        stacked: typing.Optional[builtins.bool] = None,
        view: typing.Optional[GraphWidgetView] = None,
    ) -> None:
        """Properties for a GraphWidget.

        :param height: Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: The region the metrics of this graph should be taken from. Default: - Current region
        :param title: Title for the graph. Default: - None
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        :param left: Metrics to display on left Y axis. Default: - No metrics
        :param left_annotations: Annotations for the left Y axis. Default: - No annotations
        :param left_y_axis: Left Y axis. Default: - None
        :param legend_position: Position of the legend. Default: - bottom
        :param live_data: Whether the graph should show live data. Default: false
        :param right: Metrics to display on right Y axis. Default: - No metrics
        :param right_annotations: Annotations for the right Y axis. Default: - No annotations
        :param right_y_axis: Right Y axis. Default: - None
        :param stacked: Whether the graph should be shown as stacked lines. Default: false
        :param view: Display this metric. Default: TimeSeries
        """
        if isinstance(left_y_axis, dict):
            left_y_axis = YAxisProps(**left_y_axis)
        if isinstance(right_y_axis, dict):
            right_y_axis = YAxisProps(**right_y_axis)
        self._values: typing.Dict[str, typing.Any] = {}
        if height is not None:
            self._values["height"] = height
        if region is not None:
            self._values["region"] = region
        if title is not None:
            self._values["title"] = title
        if width is not None:
            self._values["width"] = width
        if left is not None:
            self._values["left"] = left
        if left_annotations is not None:
            self._values["left_annotations"] = left_annotations
        if left_y_axis is not None:
            self._values["left_y_axis"] = left_y_axis
        if legend_position is not None:
            self._values["legend_position"] = legend_position
        if live_data is not None:
            self._values["live_data"] = live_data
        if right is not None:
            self._values["right"] = right
        if right_annotations is not None:
            self._values["right_annotations"] = right_annotations
        if right_y_axis is not None:
            self._values["right_y_axis"] = right_y_axis
        if stacked is not None:
            self._values["stacked"] = stacked
        if view is not None:
            self._values["view"] = view

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        """Height of the widget.

        :default:

        - 6 for Alarm and Graph widgets.
        3 for single value widgets where most recent value of a metric is displayed.
        """
        result = self._values.get("height")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region the metrics of this graph should be taken from.

        :default: - Current region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        """Title for the graph.

        :default: - None
        """
        result = self._values.get("title")
        return result

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        """Width of the widget, in a grid of 24 units wide.

        :default: 6
        """
        result = self._values.get("width")
        return result

    @builtins.property
    def left(self) -> typing.Optional[typing.List[IMetric]]:
        """Metrics to display on left Y axis.

        :default: - No metrics
        """
        result = self._values.get("left")
        return result

    @builtins.property
    def left_annotations(self) -> typing.Optional[typing.List[HorizontalAnnotation]]:
        """Annotations for the left Y axis.

        :default: - No annotations
        """
        result = self._values.get("left_annotations")
        return result

    @builtins.property
    def left_y_axis(self) -> typing.Optional[YAxisProps]:
        """Left Y axis.

        :default: - None
        """
        result = self._values.get("left_y_axis")
        return result

    @builtins.property
    def legend_position(self) -> typing.Optional[LegendPosition]:
        """Position of the legend.

        :default: - bottom
        """
        result = self._values.get("legend_position")
        return result

    @builtins.property
    def live_data(self) -> typing.Optional[builtins.bool]:
        """Whether the graph should show live data.

        :default: false
        """
        result = self._values.get("live_data")
        return result

    @builtins.property
    def right(self) -> typing.Optional[typing.List[IMetric]]:
        """Metrics to display on right Y axis.

        :default: - No metrics
        """
        result = self._values.get("right")
        return result

    @builtins.property
    def right_annotations(self) -> typing.Optional[typing.List[HorizontalAnnotation]]:
        """Annotations for the right Y axis.

        :default: - No annotations
        """
        result = self._values.get("right_annotations")
        return result

    @builtins.property
    def right_y_axis(self) -> typing.Optional[YAxisProps]:
        """Right Y axis.

        :default: - None
        """
        result = self._values.get("right_y_axis")
        return result

    @builtins.property
    def stacked(self) -> typing.Optional[builtins.bool]:
        """Whether the graph should be shown as stacked lines.

        :default: false
        """
        result = self._values.get("stacked")
        return result

    @builtins.property
    def view(self) -> typing.Optional[GraphWidgetView]:
        """Display this metric.

        :default: TimeSeries
        """
        result = self._values.get("view")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphWidgetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarm")
class IAlarm(IAlarmRule, aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents a CloudWatch Alarm."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAlarmProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        """Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        """Name of the alarm.

        :attribute: true
        """
        ...


class _IAlarmProxy(
    jsii.proxy_for(IAlarmRule), # type: ignore
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore
):
    """Represents a CloudWatch Alarm."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudwatch.IAlarm"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        """Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :attribute: true
        """
        return jsii.get(self, "alarmArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        """Name of the alarm.

        :attribute: true
        """
        return jsii.get(self, "alarmName")


class LogQueryWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.LogQueryWidget",
):
    """Display query results from Logs Insights."""

    def __init__(
        self,
        *,
        log_group_names: typing.List[builtins.str],
        height: typing.Optional[jsii.Number] = None,
        query_lines: typing.Optional[typing.List[builtins.str]] = None,
        query_string: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        view: typing.Optional[LogQueryVisualizationType] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param log_group_names: Names of log groups to query.
        :param height: Height of the widget. Default: 6
        :param query_lines: A sequence of lines to use to build the query. The query will be built by joining the lines together using ``\\n|``. Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param query_string: Full query string for log insights. Be sure to prepend every new line with a newline and pipe character (``\\n|``). Default: - Exactly one of ``queryString``, ``queryLines`` is required.
        :param region: The region the metrics of this widget should be taken from. Default: Current region
        :param title: Title for the widget. Default: No title
        :param view: The type of view to use. Default: LogQueryVisualizationType.TABLE
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = LogQueryWidgetProps(
            log_group_names=log_group_names,
            height=height,
            query_lines=query_lines,
            query_string=query_string,
            region=region,
            title=title,
            view=view,
            width=width,
        )

        jsii.create(LogQueryWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class SingleValueWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidget",
):
    """A dashboard widget that displays the most recent value for every metric."""

    def __init__(
        self,
        *,
        metrics: typing.List[IMetric],
        set_period_to_time_range: typing.Optional[builtins.bool] = None,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param metrics: Metrics to display.
        :param set_period_to_time_range: Whether to show the value from the entire time range. Default: false
        :param height: Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: The region the metrics of this graph should be taken from. Default: - Current region
        :param title: Title for the graph. Default: - None
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = SingleValueWidgetProps(
            metrics=metrics,
            set_period_to_time_range=set_period_to_time_range,
            height=height,
            region=region,
            title=title,
            width=width,
        )

        jsii.create(SingleValueWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class TextWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.TextWidget",
):
    """A dashboard widget that displays MarkDown."""

    def __init__(
        self,
        *,
        markdown: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param markdown: The text to display, in MarkDown format.
        :param height: Height of the widget. Default: 2
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = TextWidgetProps(markdown=markdown, height=height, width=width)

        jsii.create(TextWidget, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.implements(IAlarm)
class AlarmBase(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-cloudwatch.AlarmBase",
):
    """The base class for Alarm and CompositeAlarm resources."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _AlarmBaseProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        """
        props = aws_cdk.core.ResourceProps(
            account=account, physical_name=physical_name, region=region
        )

        jsii.create(AlarmBase, self, [scope, id, props])

    @jsii.member(jsii_name="addAlarmAction")
    def add_alarm_action(self, *actions: IAlarmAction) -> None:
        """Trigger this action if the alarm fires.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -
        """
        return jsii.invoke(self, "addAlarmAction", [*actions])

    @jsii.member(jsii_name="addInsufficientDataAction")
    def add_insufficient_data_action(self, *actions: IAlarmAction) -> None:
        """Trigger this action if there is insufficient data to evaluate the alarm.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -
        """
        return jsii.invoke(self, "addInsufficientDataAction", [*actions])

    @jsii.member(jsii_name="addOkAction")
    def add_ok_action(self, *actions: IAlarmAction) -> None:
        """Trigger this action if the alarm returns from breaching state into ok state.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        :param actions: -
        """
        return jsii.invoke(self, "addOkAction", [*actions])

    @jsii.member(jsii_name="renderAlarmRule")
    def render_alarm_rule(self) -> builtins.str:
        """AlarmRule indicating ALARM state for Alarm."""
        return jsii.invoke(self, "renderAlarmRule", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmArn")
    @abc.abstractmethod
    def alarm_arn(self) -> builtins.str:
        """Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmName")
    @abc.abstractmethod
    def alarm_name(self) -> builtins.str:
        """Name of the alarm."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmActionArns")
    def _alarm_action_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        return jsii.get(self, "alarmActionArns")

    @_alarm_action_arns.setter # type: ignore
    def _alarm_action_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "alarmActionArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="insufficientDataActionArns")
    def _insufficient_data_action_arns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return jsii.get(self, "insufficientDataActionArns")

    @_insufficient_data_action_arns.setter # type: ignore
    def _insufficient_data_action_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "insufficientDataActionArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="okActionArns")
    def _ok_action_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        return jsii.get(self, "okActionArns")

    @_ok_action_arns.setter # type: ignore
    def _ok_action_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "okActionArns", value)


class _AlarmBaseProxy(
    AlarmBase, jsii.proxy_for(aws_cdk.core.Resource) # type: ignore
):
    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        """Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).

        :attribute: true
        """
        return jsii.get(self, "alarmArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        """Name of the alarm."""
        return jsii.get(self, "alarmName")


class AlarmStatusWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.AlarmStatusWidget",
):
    """A dashboard widget that displays alarms in a grid view."""

    def __init__(
        self,
        *,
        alarms: typing.List[IAlarm],
        height: typing.Optional[jsii.Number] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param alarms: CloudWatch Alarms to show in widget.
        :param height: Height of the widget. Default: 3
        :param title: The title of the widget. Default: 'Alarm Status'
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = AlarmStatusWidgetProps(
            alarms=alarms, height=height, title=title, width=width
        )

        jsii.create(AlarmStatusWidget, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        :param x: -
        :param y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class AlarmWidget(
    ConcreteWidget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidget",
):
    """Display the metric associated with an alarm, including the alarm line."""

    def __init__(
        self,
        *,
        alarm: IAlarm,
        left_y_axis: typing.Optional[YAxisProps] = None,
        height: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param alarm: The alarm to show.
        :param left_y_axis: Left Y axis. Default: - No minimum or maximum values for the left Y-axis
        :param height: Height of the widget. Default: - 6 for Alarm and Graph widgets. 3 for single value widgets where most recent value of a metric is displayed.
        :param region: The region the metrics of this graph should be taken from. Default: - Current region
        :param title: Title for the graph. Default: - None
        :param width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props = AlarmWidgetProps(
            alarm=alarm,
            left_y_axis=left_y_axis,
            height=height,
            region=region,
            title=title,
            width=width,
        )

        jsii.create(AlarmWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class CompositeAlarm(
    AlarmBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.CompositeAlarm",
):
    """A Composite Alarm based on Alarm Rule."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alarm_rule: IAlarmRule,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        composite_alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param alarm_rule: Expression that specifies which other alarms are to be evaluated to determine this composite alarm's state.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param composite_alarm_name: Name of the alarm. Default: Automatically generated name
        """
        props = CompositeAlarmProps(
            alarm_rule=alarm_rule,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            composite_alarm_name=composite_alarm_name,
        )

        jsii.create(CompositeAlarm, self, [scope, id, props])

    @jsii.member(jsii_name="fromCompositeAlarmArn")
    @builtins.classmethod
    def from_composite_alarm_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        composite_alarm_arn: builtins.str,
    ) -> IAlarm:
        """Import an existing CloudWatch composite alarm provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param composite_alarm_arn: Composite Alarm ARN (i.e. arn:aws:cloudwatch:::alarm/CompositeAlarmName).
        """
        return jsii.sinvoke(cls, "fromCompositeAlarmArn", [scope, id, composite_alarm_arn])

    @jsii.member(jsii_name="fromCompositeAlarmName")
    @builtins.classmethod
    def from_composite_alarm_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        composite_alarm_name: builtins.str,
    ) -> IAlarm:
        """Import an existing CloudWatch composite alarm provided an Name.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param composite_alarm_name: Composite Alarm Name.
        """
        return jsii.sinvoke(cls, "fromCompositeAlarmName", [scope, id, composite_alarm_name])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        """ARN of this alarm.

        :attribute: true
        """
        return jsii.get(self, "alarmArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        """Name of this alarm.

        :attribute: true
        """
        return jsii.get(self, "alarmName")


class Alarm(
    AlarmBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudwatch.Alarm",
):
    """An alarm on a CloudWatch metric."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        metric: IMetric,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        actions_enabled: typing.Optional[builtins.bool] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        statistic: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional[TreatMissingData] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param metric: The metric to add the alarm on. Metric objects can be obtained from most resources, or you can construct custom Metric objects by instantiating one.
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param threshold: The value against which the specified statistic is compared.
        :param actions_enabled: Whether the actions for this alarm are enabled. Default: true
        :param alarm_description: Description for the alarm. Default: No description
        :param alarm_name: Name of the alarm. Default: Automatically generated name
        :param comparison_operator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
        :param datapoints_to_alarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
        :param evaluate_low_sample_count_percentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
        :param period: (deprecated) The period over which the specified statistic is applied. Cannot be used with ``MathExpression`` objects. Default: - The period from the metric
        :param statistic: (deprecated) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Cannot be used with ``MathExpression`` objects. Default: - The statistic from the metric
        :param treat_missing_data: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props = AlarmProps(
            metric=metric,
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            actions_enabled=actions_enabled,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            comparison_operator=comparison_operator,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            period=period,
            statistic=statistic,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(Alarm, self, [scope, id, props])

    @jsii.member(jsii_name="fromAlarmArn")
    @builtins.classmethod
    def from_alarm_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        alarm_arn: builtins.str,
    ) -> IAlarm:
        """Import an existing CloudWatch alarm provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param alarm_arn: Alarm ARN (i.e. arn:aws:cloudwatch:::alarm:Foo).
        """
        return jsii.sinvoke(cls, "fromAlarmArn", [scope, id, alarm_arn])

    @jsii.member(jsii_name="toAnnotation")
    def to_annotation(self) -> HorizontalAnnotation:
        """Turn this alarm into a horizontal annotation.

        This is useful if you want to represent an Alarm in a non-AlarmWidget.
        An ``AlarmWidget`` can directly show an alarm, but it can only show a
        single alarm and no other metrics. Instead, you can convert the alarm to
        a HorizontalAnnotation and add it as an annotation to another graph.

        This might be useful if:

        - You want to show multiple alarms inside a single graph, for example if
          you have both a "small margin/long period" alarm as well as a
          "large margin/short period" alarm.
        - You want to show an Alarm line in a graph with multiple metrics in it.
        """
        return jsii.invoke(self, "toAnnotation", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> builtins.str:
        """ARN of this alarm.

        :attribute: true
        """
        return jsii.get(self, "alarmArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        """Name of this alarm.

        :attribute: true
        """
        return jsii.get(self, "alarmName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metric")
    def metric(self) -> IMetric:
        """The metric object this alarm was based on."""
        return jsii.get(self, "metric")


__all__ = [
    "Alarm",
    "AlarmActionConfig",
    "AlarmBase",
    "AlarmProps",
    "AlarmRule",
    "AlarmState",
    "AlarmStatusWidget",
    "AlarmStatusWidgetProps",
    "AlarmWidget",
    "AlarmWidgetProps",
    "CfnAlarm",
    "CfnAlarmProps",
    "CfnAnomalyDetector",
    "CfnAnomalyDetectorProps",
    "CfnCompositeAlarm",
    "CfnCompositeAlarmProps",
    "CfnDashboard",
    "CfnDashboardProps",
    "CfnInsightRule",
    "CfnInsightRuleProps",
    "CfnMetricStream",
    "CfnMetricStreamProps",
    "Color",
    "Column",
    "CommonMetricOptions",
    "ComparisonOperator",
    "CompositeAlarm",
    "CompositeAlarmProps",
    "ConcreteWidget",
    "CreateAlarmOptions",
    "Dashboard",
    "DashboardProps",
    "Dimension",
    "GraphWidget",
    "GraphWidgetProps",
    "GraphWidgetView",
    "HorizontalAnnotation",
    "IAlarm",
    "IAlarmAction",
    "IAlarmRule",
    "IMetric",
    "IWidget",
    "LegendPosition",
    "LogQueryVisualizationType",
    "LogQueryWidget",
    "LogQueryWidgetProps",
    "MathExpression",
    "MathExpressionOptions",
    "MathExpressionProps",
    "Metric",
    "MetricAlarmConfig",
    "MetricConfig",
    "MetricExpressionConfig",
    "MetricGraphConfig",
    "MetricOptions",
    "MetricProps",
    "MetricRenderingProperties",
    "MetricStatConfig",
    "MetricWidgetProps",
    "PeriodOverride",
    "Row",
    "Shading",
    "SingleValueWidget",
    "SingleValueWidgetProps",
    "Spacer",
    "SpacerProps",
    "Statistic",
    "TextWidget",
    "TextWidgetProps",
    "TreatMissingData",
    "Unit",
    "YAxisProps",
]

publication.publish()
