"""
## AWS::CodeGuruProfiler Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they become stable. We will only make breaking changes to address unforeseen API issues. Therefore, these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes will be announced in release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Amazon CodeGuru Profiler collects runtime performance data from your live applications, and provides recommendations that can help you fine-tune your application performance.

### Installation

Import to your project:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codeguruprofiler as codeguruprofiler
```

### Basic usage

Here's how to setup a profiling group and give your compute role permissions to publish to the profiling group to the profiling agent can publish profiling information:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# The execution role of your application that publishes to the ProfilingGroup via CodeGuru Profiler Profiling Agent. (the following is merely an example)
publish_app_role = Role(stack, "PublishAppRole",
    assumed_by=AccountRootPrincipal()
)

profiling_group = ProfilingGroup(stack, "MyProfilingGroup")
profiling_group.grant_publish(publish_app_role)
```

### Compute Platform configuration

Code Guru Profiler supports multiple compute environments.
They can be configured when creating a Profiling Group by using the `computePlatform` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
profiling_group = ProfilingGroup(stack, "MyProfilingGroup",
    compute_platform=ComputePlatform.AWS_LAMBDA
)
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

import aws_cdk.aws_iam
import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.core.IInspectable)
class CfnProfilingGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroup",
):
    """A CloudFormation ``AWS::CodeGuruProfiler::ProfilingGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
    :cloudformationResource: AWS::CodeGuruProfiler::ProfilingGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        profiling_group_name: builtins.str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProfilingGroup.ChannelProperty"]]]] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param profiling_group_name: ``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.
        :param agent_permissions: ``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.
        :param anomaly_detection_notification_configuration: ``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.
        :param compute_platform: ``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.
        :param tags: ``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.
        """
        props = CfnProfilingGroupProps(
            profiling_group_name=profiling_group_name,
            agent_permissions=agent_permissions,
            anomaly_detection_notification_configuration=anomaly_detection_notification_configuration,
            compute_platform=compute_platform,
            tags=tags,
        )

        jsii.create(CfnProfilingGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="agentPermissions")
    def agent_permissions(self) -> typing.Any:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        """
        return jsii.get(self, "agentPermissions")

    @agent_permissions.setter # type: ignore
    def agent_permissions(self, value: typing.Any) -> None:
        jsii.set(self, "agentPermissions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        """
        return jsii.get(self, "profilingGroupName")

    @profiling_group_name.setter # type: ignore
    def profiling_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "profilingGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="anomalyDetectionNotificationConfiguration")
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProfilingGroup.ChannelProperty"]]]]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        """
        return jsii.get(self, "anomalyDetectionNotificationConfiguration")

    @anomaly_detection_notification_configuration.setter # type: ignore
    def anomaly_detection_notification_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProfilingGroup.ChannelProperty"]]]],
    ) -> None:
        jsii.set(self, "anomalyDetectionNotificationConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        """
        return jsii.get(self, "computePlatform")

    @compute_platform.setter # type: ignore
    def compute_platform(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "computePlatform", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroup.ChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_uri": "channelUri", "channel_id": "channelId"},
    )
    class ChannelProperty:
        def __init__(
            self,
            *,
            channel_uri: builtins.str,
            channel_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param channel_uri: ``CfnProfilingGroup.ChannelProperty.channelUri``.
            :param channel_id: ``CfnProfilingGroup.ChannelProperty.channelId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "channel_uri": channel_uri,
            }
            if channel_id is not None:
                self._values["channel_id"] = channel_id

        @builtins.property
        def channel_uri(self) -> builtins.str:
            """``CfnProfilingGroup.ChannelProperty.channelUri``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channeluri
            """
            result = self._values.get("channel_uri")
            assert result is not None, "Required property 'channel_uri' is missing"
            return result

        @builtins.property
        def channel_id(self) -> typing.Optional[builtins.str]:
            """``CfnProfilingGroup.ChannelProperty.channelId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channelid
            """
            result = self._values.get("channel_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codeguruprofiler.CfnProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "profiling_group_name": "profilingGroupName",
        "agent_permissions": "agentPermissions",
        "anomaly_detection_notification_configuration": "anomalyDetectionNotificationConfiguration",
        "compute_platform": "computePlatform",
        "tags": "tags",
    },
)
class CfnProfilingGroupProps:
    def __init__(
        self,
        *,
        profiling_group_name: builtins.str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnProfilingGroup.ChannelProperty]]]] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param profiling_group_name: ``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.
        :param agent_permissions: ``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.
        :param anomaly_detection_notification_configuration: ``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.
        :param compute_platform: ``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.
        :param tags: ``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "profiling_group_name": profiling_group_name,
        }
        if agent_permissions is not None:
            self._values["agent_permissions"] = agent_permissions
        if anomaly_detection_notification_configuration is not None:
            self._values["anomaly_detection_notification_configuration"] = anomaly_detection_notification_configuration
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def profiling_group_name(self) -> builtins.str:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        """
        result = self._values.get("profiling_group_name")
        assert result is not None, "Required property 'profiling_group_name' is missing"
        return result

    @builtins.property
    def agent_permissions(self) -> typing.Any:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        """
        result = self._values.get("agent_permissions")
        return result

    @builtins.property
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnProfilingGroup.ChannelProperty]]]]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        """
        result = self._values.get("anomaly_detection_notification_configuration")
        return result

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        """
        result = self._values.get("compute_platform")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codeguruprofiler.ComputePlatform")
class ComputePlatform(enum.Enum):
    """(experimental) The compute platform of the profiling group.

    :stability: experimental
    """

    AWS_LAMBDA = "AWS_LAMBDA"
    """(experimental) Use AWS_LAMBDA if your application runs on AWS Lambda.

    :stability: experimental
    """
    DEFAULT = "DEFAULT"
    """(experimental) Use Default if your application runs on a compute platform that is not AWS Lambda, such an Amazon EC2 instance, an on-premises server, or a different platform.

    :stability: experimental
    """


@jsii.interface(jsii_type="@aws-cdk/aws-codeguruprofiler.IProfilingGroup")
class IProfilingGroup(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) IResource represents a Profiling Group.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IProfilingGroupProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        """(experimental) A name for the profiling group.

        :stability: experimental
        :attribute: true
        """
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """(experimental) Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """(experimental) Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        :stability: experimental
        """
        ...


class _IProfilingGroupProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) IResource represents a Profiling Group.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codeguruprofiler.IProfilingGroup"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        """(experimental) A name for the profiling group.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "profilingGroupName")

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """(experimental) Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """(experimental) Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])


@jsii.implements(IProfilingGroup)
class ProfilingGroup(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codeguruprofiler.ProfilingGroup",
):
    """(experimental) A new Profiling Group.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        compute_platform: typing.Optional[ComputePlatform] = None,
        profiling_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param compute_platform: (experimental) The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: (experimental) A name for the profiling group. Default: - automatically generated name.

        :stability: experimental
        """
        props = ProfilingGroupProps(
            compute_platform=compute_platform,
            profiling_group_name=profiling_group_name,
        )

        jsii.create(ProfilingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromProfilingGroupArn")
    @builtins.classmethod
    def from_profiling_group_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        profiling_group_arn: builtins.str,
    ) -> IProfilingGroup:
        """(experimental) Import an existing Profiling Group provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_arn: Profiling Group ARN.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromProfilingGroupArn", [scope, id, profiling_group_arn])

    @jsii.member(jsii_name="fromProfilingGroupName")
    @builtins.classmethod
    def from_profiling_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        profiling_group_name: builtins.str,
    ) -> IProfilingGroup:
        """(experimental) Import an existing Profiling Group provided a Profiling Group Name.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_name: Profiling Group Name.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromProfilingGroupName", [scope, id, profiling_group_name])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """(experimental) Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """(experimental) Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="profilingGroupArn")
    def profiling_group_arn(self) -> builtins.str:
        """(experimental) The ARN of the Profiling Group.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "profilingGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        """(experimental) The name of the Profiling Group.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "profilingGroupName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codeguruprofiler.ProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_platform": "computePlatform",
        "profiling_group_name": "profilingGroupName",
    },
)
class ProfilingGroupProps:
    def __init__(
        self,
        *,
        compute_platform: typing.Optional[ComputePlatform] = None,
        profiling_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties for creating a new Profiling Group.

        :param compute_platform: (experimental) The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: (experimental) A name for the profiling group. Default: - automatically generated name.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if profiling_group_name is not None:
            self._values["profiling_group_name"] = profiling_group_name

    @builtins.property
    def compute_platform(self) -> typing.Optional[ComputePlatform]:
        """(experimental) The compute platform of the profiling group.

        :default: ComputePlatform.DEFAULT

        :stability: experimental
        """
        result = self._values.get("compute_platform")
        return result

    @builtins.property
    def profiling_group_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A name for the profiling group.

        :default: - automatically generated name.

        :stability: experimental
        """
        result = self._values.get("profiling_group_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProfilingGroup",
    "CfnProfilingGroupProps",
    "ComputePlatform",
    "IProfilingGroup",
    "ProfilingGroup",
    "ProfilingGroupProps",
]

publication.publish()
