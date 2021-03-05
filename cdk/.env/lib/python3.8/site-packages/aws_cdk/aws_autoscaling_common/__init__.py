"""
## AWS AutoScaling Common Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This is a sister package to `@aws-cdk/aws-autoscaling` and
`@aws-cdk/aws-applicationautoscaling`. It contains shared implementation
details between them.

It does not need to be used directly.
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


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling-common.Alarms",
    jsii_struct_bases=[],
    name_mapping={
        "lower_alarm_interval_index": "lowerAlarmIntervalIndex",
        "upper_alarm_interval_index": "upperAlarmIntervalIndex",
    },
)
class Alarms:
    def __init__(
        self,
        *,
        lower_alarm_interval_index: typing.Optional[jsii.Number] = None,
        upper_alarm_interval_index: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param lower_alarm_interval_index: 
        :param upper_alarm_interval_index: 

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if lower_alarm_interval_index is not None:
            self._values["lower_alarm_interval_index"] = lower_alarm_interval_index
        if upper_alarm_interval_index is not None:
            self._values["upper_alarm_interval_index"] = upper_alarm_interval_index

    @builtins.property
    def lower_alarm_interval_index(self) -> typing.Optional[jsii.Number]:
        """
        :stability: experimental
        """
        result = self._values.get("lower_alarm_interval_index")
        return result

    @builtins.property
    def upper_alarm_interval_index(self) -> typing.Optional[jsii.Number]:
        """
        :stability: experimental
        """
        result = self._values.get("upper_alarm_interval_index")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Alarms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling-common.ArbitraryIntervals",
    jsii_struct_bases=[],
    name_mapping={"absolute": "absolute", "intervals": "intervals"},
)
class ArbitraryIntervals:
    def __init__(
        self,
        *,
        absolute: builtins.bool,
        intervals: typing.List["ScalingInterval"],
    ) -> None:
        """
        :param absolute: 
        :param intervals: 

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "absolute": absolute,
            "intervals": intervals,
        }

    @builtins.property
    def absolute(self) -> builtins.bool:
        """
        :stability: experimental
        """
        result = self._values.get("absolute")
        assert result is not None, "Required property 'absolute' is missing"
        return result

    @builtins.property
    def intervals(self) -> typing.List["ScalingInterval"]:
        """
        :stability: experimental
        """
        result = self._values.get("intervals")
        assert result is not None, "Required property 'intervals' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArbitraryIntervals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling-common.CompleteScalingInterval",
    jsii_struct_bases=[],
    name_mapping={"lower": "lower", "upper": "upper", "change": "change"},
)
class CompleteScalingInterval:
    def __init__(
        self,
        *,
        lower: jsii.Number,
        upper: jsii.Number,
        change: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param lower: 
        :param upper: 
        :param change: 

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "lower": lower,
            "upper": upper,
        }
        if change is not None:
            self._values["change"] = change

    @builtins.property
    def lower(self) -> jsii.Number:
        """
        :stability: experimental
        """
        result = self._values.get("lower")
        assert result is not None, "Required property 'lower' is missing"
        return result

    @builtins.property
    def upper(self) -> jsii.Number:
        """
        :stability: experimental
        """
        result = self._values.get("upper")
        assert result is not None, "Required property 'upper' is missing"
        return result

    @builtins.property
    def change(self) -> typing.Optional[jsii.Number]:
        """
        :stability: experimental
        """
        result = self._values.get("change")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompleteScalingInterval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-common.IRandomGenerator")
class IRandomGenerator(typing_extensions.Protocol):
    """
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRandomGeneratorProxy

    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> builtins.bool:
        """
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        """
        :param min: -
        :param max: -

        :stability: experimental
        """
        ...


class _IRandomGeneratorProxy:
    """
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-autoscaling-common.IRandomGenerator"

    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> builtins.bool:
        """
        :stability: experimental
        """
        return jsii.invoke(self, "nextBoolean", [])

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        """
        :param min: -
        :param max: -

        :stability: experimental
        """
        return jsii.invoke(self, "nextInt", [min, max])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-autoscaling-common.ScalingInterval",
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
        """(experimental) A range of metric values in which to apply a certain scaling operation.

        :param change: (experimental) The capacity adjustment to apply in this interval. The number is interpreted differently based on AdjustmentType: - ChangeInCapacity: add the adjustment to the current capacity. The number can be positive or negative. - PercentChangeInCapacity: add or remove the given percentage of the current capacity to itself. The number can be in the range [-100..100]. - ExactCapacity: set the capacity to this number. The number must be positive.
        :param lower: (experimental) The lower bound of the interval. The scaling adjustment will be applied if the metric is higher than this value. Default: Threshold automatically derived from neighbouring intervals
        :param upper: (experimental) The upper bound of the interval. The scaling adjustment will be applied if the metric is lower than this value. Default: Threshold automatically derived from neighbouring intervals

        :stability: experimental
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
        """(experimental) The capacity adjustment to apply in this interval.

        The number is interpreted differently based on AdjustmentType:

        - ChangeInCapacity: add the adjustment to the current capacity.
          The number can be positive or negative.
        - PercentChangeInCapacity: add or remove the given percentage of the current
          capacity to itself. The number can be in the range [-100..100].
        - ExactCapacity: set the capacity to this number. The number must
          be positive.

        :stability: experimental
        """
        result = self._values.get("change")
        assert result is not None, "Required property 'change' is missing"
        return result

    @builtins.property
    def lower(self) -> typing.Optional[jsii.Number]:
        """(experimental) The lower bound of the interval.

        The scaling adjustment will be applied if the metric is higher than this value.

        :default: Threshold automatically derived from neighbouring intervals

        :stability: experimental
        """
        result = self._values.get("lower")
        return result

    @builtins.property
    def upper(self) -> typing.Optional[jsii.Number]:
        """(experimental) The upper bound of the interval.

        The scaling adjustment will be applied if the metric is lower than this value.

        :default: Threshold automatically derived from neighbouring intervals

        :stability: experimental
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


__all__ = [
    "Alarms",
    "ArbitraryIntervals",
    "CompleteScalingInterval",
    "IRandomGenerator",
    "ScalingInterval",
]

publication.publish()
