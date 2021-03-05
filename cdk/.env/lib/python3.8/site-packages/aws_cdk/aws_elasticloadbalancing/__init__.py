"""
## Amazon Elastic Load Balancing Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

The `@aws-cdk/aws-elasticloadbalancing` package provides constructs for configuring
classic load balancers.

### Configuring a Load Balancer

Load balancers send traffic to one or more AutoScalingGroups. Create a load
balancer, set up listeners and a health check, and supply the fleet(s) you want
to load balance to in the `targets` property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lb = elb.LoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True,
    health_check={
        "port": 80
    }
)

lb.add_target(my_auto_scaling_group)
lb.add_listener(
    external_port=80
)
```

The load balancer allows all connections by default. If you want to change that,
pass the `allowConnectionsFrom` property while setting up the listener:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lb.add_listener(
    external_port=80,
    allow_connections_from=[my_security_group]
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

import aws_cdk.aws_ec2
import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLoadBalancer(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer",
):
    """A CloudFormation ``AWS::ElasticLoadBalancing::LoadBalancer``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html
    :cloudformationResource: AWS::ElasticLoadBalancing::LoadBalancer
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        listeners: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", aws_cdk.core.IResolvable]]],
        access_logging_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AccessLoggingPolicyProperty"]] = None,
        app_cookie_stickiness_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AppCookieStickinessPolicyProperty"]]]] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        connection_draining_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.ConnectionDrainingPolicyProperty"]] = None,
        connection_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.ConnectionSettingsProperty"]] = None,
        cross_zone: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        health_check: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.HealthCheckProperty"]] = None,
        instances: typing.Optional[typing.List[builtins.str]] = None,
        lb_cookie_stickiness_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LBCookieStickinessPolicyProperty"]]]] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.PoliciesProperty"]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        subnets: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::ElasticLoadBalancing::LoadBalancer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param listeners: ``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.
        :param access_logging_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.
        :param app_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.
        :param availability_zones: ``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.
        :param connection_draining_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.
        :param connection_settings: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.
        :param cross_zone: ``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.
        :param health_check: ``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.
        :param instances: ``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.
        :param lb_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.
        :param load_balancer_name: ``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.
        :param policies: ``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.
        :param scheme: ``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.
        :param subnets: ``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.
        """
        props = CfnLoadBalancerProps(
            listeners=listeners,
            access_logging_policy=access_logging_policy,
            app_cookie_stickiness_policy=app_cookie_stickiness_policy,
            availability_zones=availability_zones,
            connection_draining_policy=connection_draining_policy,
            connection_settings=connection_settings,
            cross_zone=cross_zone,
            health_check=health_check,
            instances=instances,
            lb_cookie_stickiness_policy=lb_cookie_stickiness_policy,
            load_balancer_name=load_balancer_name,
            policies=policies,
            scheme=scheme,
            security_groups=security_groups,
            subnets=subnets,
            tags=tags,
        )

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCanonicalHostedZoneName")
    def attr_canonical_hosted_zone_name(self) -> builtins.str:
        """
        :cloudformationAttribute: CanonicalHostedZoneName
        """
        return jsii.get(self, "attrCanonicalHostedZoneName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCanonicalHostedZoneNameId")
    def attr_canonical_hosted_zone_name_id(self) -> builtins.str:
        """
        :cloudformationAttribute: CanonicalHostedZoneNameID
        """
        return jsii.get(self, "attrCanonicalHostedZoneNameId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> builtins.str:
        """
        :cloudformationAttribute: DNSName
        """
        return jsii.get(self, "attrDnsName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrSourceSecurityGroupGroupName")
    def attr_source_security_group_group_name(self) -> builtins.str:
        """
        :cloudformationAttribute: SourceSecurityGroup.GroupName
        """
        return jsii.get(self, "attrSourceSecurityGroupGroupName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrSourceSecurityGroupOwnerAlias")
    def attr_source_security_group_owner_alias(self) -> builtins.str:
        """
        :cloudformationAttribute: SourceSecurityGroup.OwnerAlias
        """
        return jsii.get(self, "attrSourceSecurityGroupOwnerAlias")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-elasticloadbalancing-loadbalancer-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listeners")
    def listeners(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-listeners
        """
        return jsii.get(self, "listeners")

    @listeners.setter # type: ignore
    def listeners(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", aws_cdk.core.IResolvable]]],
    ) -> None:
        jsii.set(self, "listeners", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accessLoggingPolicy")
    def access_logging_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AccessLoggingPolicyProperty"]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-accessloggingpolicy
        """
        return jsii.get(self, "accessLoggingPolicy")

    @access_logging_policy.setter # type: ignore
    def access_logging_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AccessLoggingPolicyProperty"]],
    ) -> None:
        jsii.set(self, "accessLoggingPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="appCookieStickinessPolicy")
    def app_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AppCookieStickinessPolicyProperty"]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-appcookiestickinesspolicy
        """
        return jsii.get(self, "appCookieStickinessPolicy")

    @app_cookie_stickiness_policy.setter # type: ignore
    def app_cookie_stickiness_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AppCookieStickinessPolicyProperty"]]]],
    ) -> None:
        jsii.set(self, "appCookieStickinessPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter # type: ignore
    def availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "availabilityZones", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionDrainingPolicy")
    def connection_draining_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.ConnectionDrainingPolicyProperty"]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectiondrainingpolicy
        """
        return jsii.get(self, "connectionDrainingPolicy")

    @connection_draining_policy.setter # type: ignore
    def connection_draining_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.ConnectionDrainingPolicyProperty"]],
    ) -> None:
        jsii.set(self, "connectionDrainingPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionSettings")
    def connection_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.ConnectionSettingsProperty"]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectionsettings
        """
        return jsii.get(self, "connectionSettings")

    @connection_settings.setter # type: ignore
    def connection_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.ConnectionSettingsProperty"]],
    ) -> None:
        jsii.set(self, "connectionSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="crossZone")
    def cross_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-crosszone
        """
        return jsii.get(self, "crossZone")

    @cross_zone.setter # type: ignore
    def cross_zone(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "crossZone", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheck")
    def health_check(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.HealthCheckProperty"]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-healthcheck
        """
        return jsii.get(self, "healthCheck")

    @health_check.setter # type: ignore
    def health_check(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.HealthCheckProperty"]],
    ) -> None:
        jsii.set(self, "healthCheck", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-instances
        """
        return jsii.get(self, "instances")

    @instances.setter # type: ignore
    def instances(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "instances", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lbCookieStickinessPolicy")
    def lb_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LBCookieStickinessPolicyProperty"]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-lbcookiestickinesspolicy
        """
        return jsii.get(self, "lbCookieStickinessPolicy")

    @lb_cookie_stickiness_policy.setter # type: ignore
    def lb_cookie_stickiness_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LBCookieStickinessPolicyProperty"]]]],
    ) -> None:
        jsii.set(self, "lbCookieStickinessPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-elbname
        """
        return jsii.get(self, "loadBalancerName")

    @load_balancer_name.setter # type: ignore
    def load_balancer_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "loadBalancerName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.PoliciesProperty"]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-policies
        """
        return jsii.get(self, "policies")

    @policies.setter # type: ignore
    def policies(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.PoliciesProperty"]]]],
    ) -> None:
        jsii.set(self, "policies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-scheme
        """
        return jsii.get(self, "scheme")

    @scheme.setter # type: ignore
    def scheme(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scheme", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter # type: ignore
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-subnets
        """
        return jsii.get(self, "subnets")

    @subnets.setter # type: ignore
    def subnets(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "subnets", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.AccessLoggingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "s3_bucket_name": "s3BucketName",
            "emit_interval": "emitInterval",
            "s3_bucket_prefix": "s3BucketPrefix",
        },
    )
    class AccessLoggingPolicyProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            s3_bucket_name: builtins.str,
            emit_interval: typing.Optional[jsii.Number] = None,
            s3_bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enabled: ``CfnLoadBalancer.AccessLoggingPolicyProperty.Enabled``.
            :param s3_bucket_name: ``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketName``.
            :param emit_interval: ``CfnLoadBalancer.AccessLoggingPolicyProperty.EmitInterval``.
            :param s3_bucket_prefix: ``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
                "s3_bucket_name": s3_bucket_name,
            }
            if emit_interval is not None:
                self._values["emit_interval"] = emit_interval
            if s3_bucket_prefix is not None:
                self._values["s3_bucket_prefix"] = s3_bucket_prefix

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def s3_bucket_name(self) -> builtins.str:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-s3bucketname
            """
            result = self._values.get("s3_bucket_name")
            assert result is not None, "Required property 's3_bucket_name' is missing"
            return result

        @builtins.property
        def emit_interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.EmitInterval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-emitinterval
            """
            result = self._values.get("emit_interval")
            return result

        @builtins.property
        def s3_bucket_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-s3bucketprefix
            """
            result = self._values.get("s3_bucket_prefix")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLoggingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.AppCookieStickinessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cookie_name": "cookieName", "policy_name": "policyName"},
    )
    class AppCookieStickinessPolicyProperty:
        def __init__(
            self,
            *,
            cookie_name: builtins.str,
            policy_name: builtins.str,
        ) -> None:
            """
            :param cookie_name: ``CfnLoadBalancer.AppCookieStickinessPolicyProperty.CookieName``.
            :param policy_name: ``CfnLoadBalancer.AppCookieStickinessPolicyProperty.PolicyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cookie_name": cookie_name,
                "policy_name": policy_name,
            }

        @builtins.property
        def cookie_name(self) -> builtins.str:
            """``CfnLoadBalancer.AppCookieStickinessPolicyProperty.CookieName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html#cfn-elb-appcookiestickinesspolicy-cookiename
            """
            result = self._values.get("cookie_name")
            assert result is not None, "Required property 'cookie_name' is missing"
            return result

        @builtins.property
        def policy_name(self) -> builtins.str:
            """``CfnLoadBalancer.AppCookieStickinessPolicyProperty.PolicyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html#cfn-elb-appcookiestickinesspolicy-policyname
            """
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppCookieStickinessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ConnectionDrainingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "timeout": "timeout"},
    )
    class ConnectionDrainingPolicyProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param enabled: ``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Enabled``.
            :param timeout: ``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Timeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html#cfn-elb-connectiondrainingpolicy-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Timeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html#cfn-elb-connectiondrainingpolicy-timeout
            """
            result = self._values.get("timeout")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionDrainingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ConnectionSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"idle_timeout": "idleTimeout"},
    )
    class ConnectionSettingsProperty:
        def __init__(self, *, idle_timeout: jsii.Number) -> None:
            """
            :param idle_timeout: ``CfnLoadBalancer.ConnectionSettingsProperty.IdleTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectionsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "idle_timeout": idle_timeout,
            }

        @builtins.property
        def idle_timeout(self) -> jsii.Number:
            """``CfnLoadBalancer.ConnectionSettingsProperty.IdleTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectionsettings.html#cfn-elb-connectionsettings-idletimeout
            """
            result = self._values.get("idle_timeout")
            assert result is not None, "Required property 'idle_timeout' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.HealthCheckProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval": "interval",
            "target": "target",
            "timeout": "timeout",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class HealthCheckProperty:
        def __init__(
            self,
            *,
            healthy_threshold: builtins.str,
            interval: builtins.str,
            target: builtins.str,
            timeout: builtins.str,
            unhealthy_threshold: builtins.str,
        ) -> None:
            """
            :param healthy_threshold: ``CfnLoadBalancer.HealthCheckProperty.HealthyThreshold``.
            :param interval: ``CfnLoadBalancer.HealthCheckProperty.Interval``.
            :param target: ``CfnLoadBalancer.HealthCheckProperty.Target``.
            :param timeout: ``CfnLoadBalancer.HealthCheckProperty.Timeout``.
            :param unhealthy_threshold: ``CfnLoadBalancer.HealthCheckProperty.UnhealthyThreshold``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "healthy_threshold": healthy_threshold,
                "interval": interval,
                "target": target,
                "timeout": timeout,
                "unhealthy_threshold": unhealthy_threshold,
            }

        @builtins.property
        def healthy_threshold(self) -> builtins.str:
            """``CfnLoadBalancer.HealthCheckProperty.HealthyThreshold``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-healthythreshold
            """
            result = self._values.get("healthy_threshold")
            assert result is not None, "Required property 'healthy_threshold' is missing"
            return result

        @builtins.property
        def interval(self) -> builtins.str:
            """``CfnLoadBalancer.HealthCheckProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-interval
            """
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return result

        @builtins.property
        def target(self) -> builtins.str:
            """``CfnLoadBalancer.HealthCheckProperty.Target``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-target
            """
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return result

        @builtins.property
        def timeout(self) -> builtins.str:
            """``CfnLoadBalancer.HealthCheckProperty.Timeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-timeout
            """
            result = self._values.get("timeout")
            assert result is not None, "Required property 'timeout' is missing"
            return result

        @builtins.property
        def unhealthy_threshold(self) -> builtins.str:
            """``CfnLoadBalancer.HealthCheckProperty.UnhealthyThreshold``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-unhealthythreshold
            """
            result = self._values.get("unhealthy_threshold")
            assert result is not None, "Required property 'unhealthy_threshold' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.LBCookieStickinessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cookie_expiration_period": "cookieExpirationPeriod",
            "policy_name": "policyName",
        },
    )
    class LBCookieStickinessPolicyProperty:
        def __init__(
            self,
            *,
            cookie_expiration_period: typing.Optional[builtins.str] = None,
            policy_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param cookie_expiration_period: ``CfnLoadBalancer.LBCookieStickinessPolicyProperty.CookieExpirationPeriod``.
            :param policy_name: ``CfnLoadBalancer.LBCookieStickinessPolicyProperty.PolicyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cookie_expiration_period is not None:
                self._values["cookie_expiration_period"] = cookie_expiration_period
            if policy_name is not None:
                self._values["policy_name"] = policy_name

        @builtins.property
        def cookie_expiration_period(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.LBCookieStickinessPolicyProperty.CookieExpirationPeriod``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html#cfn-elb-lbcookiestickinesspolicy-cookieexpirationperiod
            """
            result = self._values.get("cookie_expiration_period")
            return result

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.LBCookieStickinessPolicyProperty.PolicyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html#cfn-elb-lbcookiestickinesspolicy-policyname
            """
            result = self._values.get("policy_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LBCookieStickinessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ListenersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_port": "instancePort",
            "load_balancer_port": "loadBalancerPort",
            "protocol": "protocol",
            "instance_protocol": "instanceProtocol",
            "policy_names": "policyNames",
            "ssl_certificate_id": "sslCertificateId",
        },
    )
    class ListenersProperty:
        def __init__(
            self,
            *,
            instance_port: builtins.str,
            load_balancer_port: builtins.str,
            protocol: builtins.str,
            instance_protocol: typing.Optional[builtins.str] = None,
            policy_names: typing.Optional[typing.List[builtins.str]] = None,
            ssl_certificate_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param instance_port: ``CfnLoadBalancer.ListenersProperty.InstancePort``.
            :param load_balancer_port: ``CfnLoadBalancer.ListenersProperty.LoadBalancerPort``.
            :param protocol: ``CfnLoadBalancer.ListenersProperty.Protocol``.
            :param instance_protocol: ``CfnLoadBalancer.ListenersProperty.InstanceProtocol``.
            :param policy_names: ``CfnLoadBalancer.ListenersProperty.PolicyNames``.
            :param ssl_certificate_id: ``CfnLoadBalancer.ListenersProperty.SSLCertificateId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "instance_port": instance_port,
                "load_balancer_port": load_balancer_port,
                "protocol": protocol,
            }
            if instance_protocol is not None:
                self._values["instance_protocol"] = instance_protocol
            if policy_names is not None:
                self._values["policy_names"] = policy_names
            if ssl_certificate_id is not None:
                self._values["ssl_certificate_id"] = ssl_certificate_id

        @builtins.property
        def instance_port(self) -> builtins.str:
            """``CfnLoadBalancer.ListenersProperty.InstancePort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-instanceport
            """
            result = self._values.get("instance_port")
            assert result is not None, "Required property 'instance_port' is missing"
            return result

        @builtins.property
        def load_balancer_port(self) -> builtins.str:
            """``CfnLoadBalancer.ListenersProperty.LoadBalancerPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-loadbalancerport
            """
            result = self._values.get("load_balancer_port")
            assert result is not None, "Required property 'load_balancer_port' is missing"
            return result

        @builtins.property
        def protocol(self) -> builtins.str:
            """``CfnLoadBalancer.ListenersProperty.Protocol``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-protocol
            """
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return result

        @builtins.property
        def instance_protocol(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.ListenersProperty.InstanceProtocol``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-instanceprotocol
            """
            result = self._values.get("instance_protocol")
            return result

        @builtins.property
        def policy_names(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLoadBalancer.ListenersProperty.PolicyNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames
            """
            result = self._values.get("policy_names")
            return result

        @builtins.property
        def ssl_certificate_id(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.ListenersProperty.SSLCertificateId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-sslcertificateid
            """
            result = self._values.get("ssl_certificate_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.PoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "policy_name": "policyName",
            "policy_type": "policyType",
            "instance_ports": "instancePorts",
            "load_balancer_ports": "loadBalancerPorts",
        },
    )
    class PoliciesProperty:
        def __init__(
            self,
            *,
            attributes: typing.Union[typing.List[typing.Any], aws_cdk.core.IResolvable],
            policy_name: builtins.str,
            policy_type: builtins.str,
            instance_ports: typing.Optional[typing.List[builtins.str]] = None,
            load_balancer_ports: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param attributes: ``CfnLoadBalancer.PoliciesProperty.Attributes``.
            :param policy_name: ``CfnLoadBalancer.PoliciesProperty.PolicyName``.
            :param policy_type: ``CfnLoadBalancer.PoliciesProperty.PolicyType``.
            :param instance_ports: ``CfnLoadBalancer.PoliciesProperty.InstancePorts``.
            :param load_balancer_ports: ``CfnLoadBalancer.PoliciesProperty.LoadBalancerPorts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "attributes": attributes,
                "policy_name": policy_name,
                "policy_type": policy_type,
            }
            if instance_ports is not None:
                self._values["instance_ports"] = instance_ports
            if load_balancer_ports is not None:
                self._values["load_balancer_ports"] = load_balancer_ports

        @builtins.property
        def attributes(
            self,
        ) -> typing.Union[typing.List[typing.Any], aws_cdk.core.IResolvable]:
            """``CfnLoadBalancer.PoliciesProperty.Attributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-attributes
            """
            result = self._values.get("attributes")
            assert result is not None, "Required property 'attributes' is missing"
            return result

        @builtins.property
        def policy_name(self) -> builtins.str:
            """``CfnLoadBalancer.PoliciesProperty.PolicyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-policyname
            """
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return result

        @builtins.property
        def policy_type(self) -> builtins.str:
            """``CfnLoadBalancer.PoliciesProperty.PolicyType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-policytype
            """
            result = self._values.get("policy_type")
            assert result is not None, "Required property 'policy_type' is missing"
            return result

        @builtins.property
        def instance_ports(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLoadBalancer.PoliciesProperty.InstancePorts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-instanceports
            """
            result = self._values.get("instance_ports")
            return result

        @builtins.property
        def load_balancer_ports(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLoadBalancer.PoliciesProperty.LoadBalancerPorts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-loadbalancerports
            """
            result = self._values.get("load_balancer_ports")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "listeners": "listeners",
        "access_logging_policy": "accessLoggingPolicy",
        "app_cookie_stickiness_policy": "appCookieStickinessPolicy",
        "availability_zones": "availabilityZones",
        "connection_draining_policy": "connectionDrainingPolicy",
        "connection_settings": "connectionSettings",
        "cross_zone": "crossZone",
        "health_check": "healthCheck",
        "instances": "instances",
        "lb_cookie_stickiness_policy": "lbCookieStickinessPolicy",
        "load_balancer_name": "loadBalancerName",
        "policies": "policies",
        "scheme": "scheme",
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "tags": "tags",
    },
)
class CfnLoadBalancerProps:
    def __init__(
        self,
        *,
        listeners: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnLoadBalancer.ListenersProperty, aws_cdk.core.IResolvable]]],
        access_logging_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.AccessLoggingPolicyProperty]] = None,
        app_cookie_stickiness_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.AppCookieStickinessPolicyProperty]]]] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        connection_draining_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.ConnectionDrainingPolicyProperty]] = None,
        connection_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.ConnectionSettingsProperty]] = None,
        cross_zone: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        health_check: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.HealthCheckProperty]] = None,
        instances: typing.Optional[typing.List[builtins.str]] = None,
        lb_cookie_stickiness_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.LBCookieStickinessPolicyProperty]]]] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.PoliciesProperty]]]] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        subnets: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticLoadBalancing::LoadBalancer``.

        :param listeners: ``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.
        :param access_logging_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.
        :param app_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.
        :param availability_zones: ``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.
        :param connection_draining_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.
        :param connection_settings: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.
        :param cross_zone: ``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.
        :param health_check: ``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.
        :param instances: ``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.
        :param lb_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.
        :param load_balancer_name: ``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.
        :param policies: ``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.
        :param scheme: ``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.
        :param subnets: ``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "listeners": listeners,
        }
        if access_logging_policy is not None:
            self._values["access_logging_policy"] = access_logging_policy
        if app_cookie_stickiness_policy is not None:
            self._values["app_cookie_stickiness_policy"] = app_cookie_stickiness_policy
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if connection_draining_policy is not None:
            self._values["connection_draining_policy"] = connection_draining_policy
        if connection_settings is not None:
            self._values["connection_settings"] = connection_settings
        if cross_zone is not None:
            self._values["cross_zone"] = cross_zone
        if health_check is not None:
            self._values["health_check"] = health_check
        if instances is not None:
            self._values["instances"] = instances
        if lb_cookie_stickiness_policy is not None:
            self._values["lb_cookie_stickiness_policy"] = lb_cookie_stickiness_policy
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if policies is not None:
            self._values["policies"] = policies
        if scheme is not None:
            self._values["scheme"] = scheme
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def listeners(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnLoadBalancer.ListenersProperty, aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-listeners
        """
        result = self._values.get("listeners")
        assert result is not None, "Required property 'listeners' is missing"
        return result

    @builtins.property
    def access_logging_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.AccessLoggingPolicyProperty]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-accessloggingpolicy
        """
        result = self._values.get("access_logging_policy")
        return result

    @builtins.property
    def app_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.AppCookieStickinessPolicyProperty]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-appcookiestickinesspolicy
        """
        result = self._values.get("app_cookie_stickiness_policy")
        return result

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-availabilityzones
        """
        result = self._values.get("availability_zones")
        return result

    @builtins.property
    def connection_draining_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.ConnectionDrainingPolicyProperty]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectiondrainingpolicy
        """
        result = self._values.get("connection_draining_policy")
        return result

    @builtins.property
    def connection_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.ConnectionSettingsProperty]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectionsettings
        """
        result = self._values.get("connection_settings")
        return result

    @builtins.property
    def cross_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-crosszone
        """
        result = self._values.get("cross_zone")
        return result

    @builtins.property
    def health_check(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.HealthCheckProperty]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-healthcheck
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-instances
        """
        result = self._values.get("instances")
        return result

    @builtins.property
    def lb_cookie_stickiness_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.LBCookieStickinessPolicyProperty]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-lbcookiestickinesspolicy
        """
        result = self._values.get("lb_cookie_stickiness_policy")
        return result

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-elbname
        """
        result = self._values.get("load_balancer_name")
        return result

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.PoliciesProperty]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-policies
        """
        result = self._values.get("policies")
        return result

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-scheme
        """
        result = self._values.get("scheme")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-securitygroups
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-subnets
        """
        result = self._values.get("subnets")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-elasticloadbalancing-loadbalancer-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancing.HealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "healthy_threshold": "healthyThreshold",
        "interval": "interval",
        "path": "path",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
    },
)
class HealthCheck:
    def __init__(
        self,
        *,
        port: jsii.Number,
        healthy_threshold: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[aws_cdk.core.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        protocol: typing.Optional["LoadBalancingProtocol"] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        unhealthy_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Describe the health check to a load balancer.

        :param port: What port number to health check on.
        :param healthy_threshold: After how many successful checks is an instance considered healthy. Default: 2
        :param interval: Number of seconds between health checks. Default: Duration.seconds(30)
        :param path: What path to use for HTTP or HTTPS health check (must return 200). For SSL and TCP health checks, accepting connections is enough to be considered healthy. Default: "/"
        :param protocol: What protocol to use for health checking. The protocol is automatically determined from the port if it's not supplied. Default: Automatic
        :param timeout: Health check timeout. Default: Duration.seconds(5)
        :param unhealthy_threshold: After how many unsuccessful checks is an instance considered unhealthy. Default: 5
        """
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if healthy_threshold is not None:
            self._values["healthy_threshold"] = healthy_threshold
        if interval is not None:
            self._values["interval"] = interval
        if path is not None:
            self._values["path"] = path
        if protocol is not None:
            self._values["protocol"] = protocol
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold is not None:
            self._values["unhealthy_threshold"] = unhealthy_threshold

    @builtins.property
    def port(self) -> jsii.Number:
        """What port number to health check on."""
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return result

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        """After how many successful checks is an instance considered healthy.

        :default: 2
        """
        result = self._values.get("healthy_threshold")
        return result

    @builtins.property
    def interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Number of seconds between health checks.

        :default: Duration.seconds(30)
        """
        result = self._values.get("interval")
        return result

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        """What path to use for HTTP or HTTPS health check (must return 200).

        For SSL and TCP health checks, accepting connections is enough to be considered
        healthy.

        :default: "/"
        """
        result = self._values.get("path")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        """What protocol to use for health checking.

        The protocol is automatically determined from the port if it's not supplied.

        :default: Automatic
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Health check timeout.

        :default: Duration.seconds(5)
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        """After how many unsuccessful checks is an instance considered unhealthy.

        :default: 5
        """
        result = self._values.get("unhealthy_threshold")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancing.ILoadBalancerTarget")
class ILoadBalancerTarget(aws_cdk.aws_ec2.IConnectable, typing_extensions.Protocol):
    """Interface that is going to be implemented by constructs that you can load balance to."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        """Attach load-balanced target to a classic ELB.

        :param load_balancer: [disable-awslint:ref-via-interface] The load balancer to attach the target to.
        """
        ...


class _ILoadBalancerTargetProxy(
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable) # type: ignore
):
    """Interface that is going to be implemented by constructs that you can load balance to."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancing.ILoadBalancerTarget"

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        """Attach load-balanced target to a classic ELB.

        :param load_balancer: [disable-awslint:ref-via-interface] The load balancer to attach the target to.
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class ListenerPort(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancing.ListenerPort",
):
    """Reference to a listener's port just created.

    This implements IConnectable with a default port (the port that an ELB
    listener was just created on) for a given security group so that it can be
    conveniently used just like any Connectable. E.g::

       const listener = elb.addListener(...);

       listener.connections.allowDefaultPortFromAnyIPv4();
       // or
       instance.connections.allowToDefaultPort(listener);
    """

    def __init__(
        self,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
        default_port: aws_cdk.aws_ec2.Port,
    ) -> None:
        """
        :param security_group: -
        :param default_port: -
        """
        jsii.create(ListenerPort, self, [security_group, default_port])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class LoadBalancer(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancer",
):
    """A load balancer with a single listener.

    Routes to a fleet of of instances in a VPC.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        cross_zone: typing.Optional[builtins.bool] = None,
        health_check: typing.Optional[HealthCheck] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        listeners: typing.Optional[typing.List["LoadBalancerListener"]] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        targets: typing.Optional[typing.List[ILoadBalancerTarget]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: VPC network of the fleet instances.
        :param cross_zone: Whether cross zone load balancing is enabled. This controls whether the load balancer evenly distributes requests across each availability zone Default: true
        :param health_check: Health check settings for the load balancing targets. Not required but recommended. Default: - None.
        :param internet_facing: Whether this is an internet-facing Load Balancer. This controls whether the LB has a public IP address assigned. It does not open up the Load Balancer's security groups to public internet access. Default: false
        :param listeners: What listeners to set up for the load balancer. Can also be added by .addListener() Default: -
        :param subnet_selection: Which subnets to deploy the load balancer. Can be used to define a specific set of subnets to deploy the load balancer to. Useful multiple public or private subnets are covering the same availability zone. Default: - Public subnets if internetFacing, Private subnets otherwise
        :param targets: What targets to load balance to. Can also be added by .addTarget() Default: - None.
        """
        props = LoadBalancerProps(
            vpc=vpc,
            cross_zone=cross_zone,
            health_check=health_check,
            internet_facing=internet_facing,
            listeners=listeners,
            subnet_selection=subnet_selection,
            targets=targets,
        )

        jsii.create(LoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        *,
        external_port: jsii.Number,
        allow_connections_from: typing.Optional[typing.List[aws_cdk.aws_ec2.IConnectable]] = None,
        external_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        internal_port: typing.Optional[jsii.Number] = None,
        internal_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        policy_names: typing.Optional[typing.List[builtins.str]] = None,
        ssl_certificate_id: typing.Optional[builtins.str] = None,
    ) -> ListenerPort:
        """Add a backend to the load balancer.

        :param external_port: External listening port.
        :param allow_connections_from: Allow connections to the load balancer from the given set of connection peers. By default, connections will be allowed from anywhere. Set this to an empty list to deny connections, or supply a custom list of peers to allow connections from (IP ranges or security groups). Default: Anywhere
        :param external_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the external port is either 80 or 443.
        :param internal_port: Instance listening port. Same as the externalPort if not specified. Default: externalPort
        :param internal_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the internal port is either 80 or 443. The instance protocol is 'tcp' if the front-end protocol is 'tcp' or 'ssl', the instance protocol is 'http' if the front-end protocol is 'https'.
        :param policy_names: SSL policy names.
        :param ssl_certificate_id: ID of SSL certificate.

        :return: A ListenerPort object that controls connections to the listener port
        """
        listener = LoadBalancerListener(
            external_port=external_port,
            allow_connections_from=allow_connections_from,
            external_protocol=external_protocol,
            internal_port=internal_port,
            internal_protocol=internal_protocol,
            policy_names=policy_names,
            ssl_certificate_id=ssl_certificate_id,
        )

        return jsii.invoke(self, "addListener", [listener])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: ILoadBalancerTarget) -> None:
        """
        :param target: -
        """
        return jsii.invoke(self, "addTarget", [target])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Control all connections from and to this load balancer."""
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerPorts")
    def listener_ports(self) -> typing.List[ListenerPort]:
        """An object controlling specifically the connections for each listener added to this load balancer."""
        return jsii.get(self, "listenerPorts")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneName")
    def load_balancer_canonical_hosted_zone_name(self) -> builtins.str:
        """
        :attribute: true
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneNameId")
    def load_balancer_canonical_hosted_zone_name_id(self) -> builtins.str:
        """
        :attribute: true
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneNameId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        """
        :attribute: true
        """
        return jsii.get(self, "loadBalancerDnsName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> builtins.str:
        """
        :attribute: true
        """
        return jsii.get(self, "loadBalancerName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupGroupName")
    def load_balancer_source_security_group_group_name(self) -> builtins.str:
        """
        :attribute: true
        """
        return jsii.get(self, "loadBalancerSourceSecurityGroupGroupName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupOwnerAlias")
    def load_balancer_source_security_group_owner_alias(self) -> builtins.str:
        """
        :attribute: true
        """
        return jsii.get(self, "loadBalancerSourceSecurityGroupOwnerAlias")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancerListener",
    jsii_struct_bases=[],
    name_mapping={
        "external_port": "externalPort",
        "allow_connections_from": "allowConnectionsFrom",
        "external_protocol": "externalProtocol",
        "internal_port": "internalPort",
        "internal_protocol": "internalProtocol",
        "policy_names": "policyNames",
        "ssl_certificate_id": "sslCertificateId",
    },
)
class LoadBalancerListener:
    def __init__(
        self,
        *,
        external_port: jsii.Number,
        allow_connections_from: typing.Optional[typing.List[aws_cdk.aws_ec2.IConnectable]] = None,
        external_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        internal_port: typing.Optional[jsii.Number] = None,
        internal_protocol: typing.Optional["LoadBalancingProtocol"] = None,
        policy_names: typing.Optional[typing.List[builtins.str]] = None,
        ssl_certificate_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Add a backend to the load balancer.

        :param external_port: External listening port.
        :param allow_connections_from: Allow connections to the load balancer from the given set of connection peers. By default, connections will be allowed from anywhere. Set this to an empty list to deny connections, or supply a custom list of peers to allow connections from (IP ranges or security groups). Default: Anywhere
        :param external_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the external port is either 80 or 443.
        :param internal_port: Instance listening port. Same as the externalPort if not specified. Default: externalPort
        :param internal_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the internal port is either 80 or 443. The instance protocol is 'tcp' if the front-end protocol is 'tcp' or 'ssl', the instance protocol is 'http' if the front-end protocol is 'https'.
        :param policy_names: SSL policy names.
        :param ssl_certificate_id: ID of SSL certificate.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "external_port": external_port,
        }
        if allow_connections_from is not None:
            self._values["allow_connections_from"] = allow_connections_from
        if external_protocol is not None:
            self._values["external_protocol"] = external_protocol
        if internal_port is not None:
            self._values["internal_port"] = internal_port
        if internal_protocol is not None:
            self._values["internal_protocol"] = internal_protocol
        if policy_names is not None:
            self._values["policy_names"] = policy_names
        if ssl_certificate_id is not None:
            self._values["ssl_certificate_id"] = ssl_certificate_id

    @builtins.property
    def external_port(self) -> jsii.Number:
        """External listening port."""
        result = self._values.get("external_port")
        assert result is not None, "Required property 'external_port' is missing"
        return result

    @builtins.property
    def allow_connections_from(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.IConnectable]]:
        """Allow connections to the load balancer from the given set of connection peers.

        By default, connections will be allowed from anywhere. Set this to an empty list
        to deny connections, or supply a custom list of peers to allow connections from
        (IP ranges or security groups).

        :default: Anywhere
        """
        result = self._values.get("allow_connections_from")
        return result

    @builtins.property
    def external_protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        """What public protocol to use for load balancing.

        Either 'tcp', 'ssl', 'http' or 'https'.

        May be omitted if the external port is either 80 or 443.
        """
        result = self._values.get("external_protocol")
        return result

    @builtins.property
    def internal_port(self) -> typing.Optional[jsii.Number]:
        """Instance listening port.

        Same as the externalPort if not specified.

        :default: externalPort
        """
        result = self._values.get("internal_port")
        return result

    @builtins.property
    def internal_protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        """What public protocol to use for load balancing.

        Either 'tcp', 'ssl', 'http' or 'https'.

        May be omitted if the internal port is either 80 or 443.

        The instance protocol is 'tcp' if the front-end protocol
        is 'tcp' or 'ssl', the instance protocol is 'http' if the
        front-end protocol is 'https'.
        """
        result = self._values.get("internal_protocol")
        return result

    @builtins.property
    def policy_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """SSL policy names."""
        result = self._values.get("policy_names")
        return result

    @builtins.property
    def ssl_certificate_id(self) -> typing.Optional[builtins.str]:
        """ID of SSL certificate."""
        result = self._values.get("ssl_certificate_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerListener(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "cross_zone": "crossZone",
        "health_check": "healthCheck",
        "internet_facing": "internetFacing",
        "listeners": "listeners",
        "subnet_selection": "subnetSelection",
        "targets": "targets",
    },
)
class LoadBalancerProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        cross_zone: typing.Optional[builtins.bool] = None,
        health_check: typing.Optional[HealthCheck] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        listeners: typing.Optional[typing.List[LoadBalancerListener]] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        targets: typing.Optional[typing.List[ILoadBalancerTarget]] = None,
    ) -> None:
        """Construction properties for a LoadBalancer.

        :param vpc: VPC network of the fleet instances.
        :param cross_zone: Whether cross zone load balancing is enabled. This controls whether the load balancer evenly distributes requests across each availability zone Default: true
        :param health_check: Health check settings for the load balancing targets. Not required but recommended. Default: - None.
        :param internet_facing: Whether this is an internet-facing Load Balancer. This controls whether the LB has a public IP address assigned. It does not open up the Load Balancer's security groups to public internet access. Default: false
        :param listeners: What listeners to set up for the load balancer. Can also be added by .addListener() Default: -
        :param subnet_selection: Which subnets to deploy the load balancer. Can be used to define a specific set of subnets to deploy the load balancer to. Useful multiple public or private subnets are covering the same availability zone. Default: - Public subnets if internetFacing, Private subnets otherwise
        :param targets: What targets to load balance to. Can also be added by .addTarget() Default: - None.
        """
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if cross_zone is not None:
            self._values["cross_zone"] = cross_zone
        if health_check is not None:
            self._values["health_check"] = health_check
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if listeners is not None:
            self._values["listeners"] = listeners
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC network of the fleet instances."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def cross_zone(self) -> typing.Optional[builtins.bool]:
        """Whether cross zone load balancing is enabled.

        This controls whether the load balancer evenly distributes requests
        across each availability zone

        :default: true
        """
        result = self._values.get("cross_zone")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        """Health check settings for the load balancing targets.

        Not required but recommended.

        :default: - None.
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        """Whether this is an internet-facing Load Balancer.

        This controls whether the LB has a public IP address assigned. It does
        not open up the Load Balancer's security groups to public internet access.

        :default: false
        """
        result = self._values.get("internet_facing")
        return result

    @builtins.property
    def listeners(self) -> typing.Optional[typing.List[LoadBalancerListener]]:
        """What listeners to set up for the load balancer.

        Can also be added by .addListener()

        :default: -
        """
        result = self._values.get("listeners")
        return result

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Which subnets to deploy the load balancer.

        Can be used to define a specific set of subnets to deploy the load balancer to.
        Useful multiple public or private subnets are covering the same availability zone.

        :default: - Public subnets if internetFacing, Private subnets otherwise
        """
        result = self._values.get("subnet_selection")
        return result

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[ILoadBalancerTarget]]:
        """What targets to load balance to.

        Can also be added by .addTarget()

        :default: - None.
        """
        result = self._values.get("targets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancingProtocol")
class LoadBalancingProtocol(enum.Enum):
    TCP = "TCP"
    SSL = "SSL"
    HTTP = "HTTP"
    HTTPS = "HTTPS"


__all__ = [
    "CfnLoadBalancer",
    "CfnLoadBalancerProps",
    "HealthCheck",
    "ILoadBalancerTarget",
    "ListenerPort",
    "LoadBalancer",
    "LoadBalancerListener",
    "LoadBalancerProps",
    "LoadBalancingProtocol",
]

publication.publish()
