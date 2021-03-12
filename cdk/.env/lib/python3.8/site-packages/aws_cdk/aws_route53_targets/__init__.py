"""
# Route53 Alias Record Targets for the CDK Route53 Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains Route53 Alias Record targets for:

* API Gateway custom domains

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ApiGateway(rest_api))
  )
  ```
* API Gateway V2 custom domains

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ApiGatewayv2Domain(domain_name))
  )
  ```
* CloudFront distributions

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.CloudFrontTarget(distribution))
  )
  ```
* ELBv2 load balancers

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.LoadBalancerTarget(elbv2))
  )
  ```
* Classic load balancers

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ClassicLoadBalancerTarget(elb))
  )
  ```

**Important:** Based on [AWS documentation](https://aws.amazon.com/de/premiumsupport/knowledge-center/alias-resource-record-set-route53-cli/), all alias record in Route 53 that points to a Elastic Load Balancer will always include *dualstack* for the DNSName to resolve IPv4/IPv6 addresses (without *dualstack* IPv6 will not resolve).

For example, if the Amazon-provided DNS for the load balancer is `ALB-xxxxxxx.us-west-2.elb.amazonaws.com`, CDK will create alias target in Route 53 will be `dualstack.ALB-xxxxxxx.us-west-2.elb.amazonaws.com`.

* InterfaceVpcEndpoints

**Important:** Based on the CFN docs for VPCEndpoints - [see here](attrDnsEntries) - the attributes returned for DnsEntries in CloudFormation is a combination of the hosted zone ID and the DNS name. The entries are ordered as follows: regional public DNS, zonal public DNS, private DNS, and wildcard DNS. This order is not enforced for AWS Marketplace services, and therefore this CDK construct is ONLY guaranteed to work with non-marketplace services.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
route53.ARecord(stack, "AliasRecord",
    zone=zone,
    target=route53.RecordTarget.from_alias(alias.InterfaceVpcEndpointTarget(interface_vpc_endpoint))
)
```

* S3 Bucket Website:

**Important:** The Bucket name must strictly match the full DNS name.
See [the Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html) for more info.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
[recordName, domainName] = ["www", "example.com"]

bucket_website = Bucket(self, "BucketWebsite",
    bucket_name=[record_name, domain_name].join("."), # www.example.com
    public_read_access=True,
    website_index_document="index.html"
)

zone = HostedZone.from_lookup(self, "Zone", domain_name=domain_name)# example.com

route53.ARecord(self, "AliasRecord",
    zone=zone,
    record_name=record_name, # www
    target=route53.RecordTarget.from_alias(alias.BucketWebsiteTarget(bucket))
)
```

* User pool domain

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.UserPoolDomainTarget(domain))
  )
  ```

See the documentation of `@aws-cdk/aws-route53` for more information.
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

import aws_cdk.aws_apigateway
import aws_cdk.aws_apigatewayv2
import aws_cdk.aws_cloudfront
import aws_cdk.aws_cognito
import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_route53
import aws_cdk.aws_s3
import aws_cdk.core


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class ApiGatewayDomain(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.ApiGatewayDomain",
):
    """Defines an API Gateway domain name as the alias target.

    Use the ``ApiGateway`` class if you wish to map the alias to an REST API with a
    domain name defined through the ``RestApiProps.domainName`` prop.
    """

    def __init__(self, domain_name: aws_cdk.aws_apigateway.IDomainName) -> None:
        """
        :param domain_name: -
        """
        jsii.create(ApiGatewayDomain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class ApiGatewayv2Domain(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.ApiGatewayv2Domain",
):
    """Defines an API Gateway V2 domain name as the alias target."""

    def __init__(self, domain_name: aws_cdk.aws_apigatewayv2.IDomainName) -> None:
        """
        :param domain_name: -
        """
        jsii.create(ApiGatewayv2Domain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class BucketWebsiteTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.BucketWebsiteTarget",
):
    """Use a S3 as an alias record target."""

    def __init__(self, bucket: aws_cdk.aws_s3.IBucket) -> None:
        """
        :param bucket: -
        """
        jsii.create(BucketWebsiteTarget, self, [bucket])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class ClassicLoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.ClassicLoadBalancerTarget",
):
    """Use a classic ELB as an alias record target."""

    def __init__(
        self,
        load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer,
    ) -> None:
        """
        :param load_balancer: -
        """
        jsii.create(ClassicLoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class CloudFrontTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.CloudFrontTarget",
):
    """Use a CloudFront Distribution as an alias record target."""

    def __init__(self, distribution: aws_cdk.aws_cloudfront.IDistribution) -> None:
        """
        :param distribution: -
        """
        jsii.create(CloudFrontTarget, self, [distribution])

    @jsii.member(jsii_name="getHostedZoneId")
    @builtins.classmethod
    def get_hosted_zone_id(cls, scope: aws_cdk.core.IConstruct) -> builtins.str:
        """Get the hosted zone id for the current scope.

        :param scope: - scope in which this resource is defined.
        """
        return jsii.sinvoke(cls, "getHostedZoneId", [scope])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CLOUDFRONT_ZONE_ID")
    def CLOUDFRONT_ZONE_ID(cls) -> builtins.str:
        """The hosted zone Id if using an alias record in Route53.

        This value never changes.
        """
        return jsii.sget(cls, "CLOUDFRONT_ZONE_ID")


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class InterfaceVpcEndpointTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.InterfaceVpcEndpointTarget",
):
    """Set an InterfaceVpcEndpoint as a target for an ARecord."""

    def __init__(self, vpc_endpoint: aws_cdk.aws_ec2.IInterfaceVpcEndpoint) -> None:
        """
        :param vpc_endpoint: -
        """
        jsii.create(InterfaceVpcEndpointTarget, self, [vpc_endpoint])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class LoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.LoadBalancerTarget",
):
    """Use an ELBv2 as an alias record target."""

    def __init__(
        self,
        load_balancer: aws_cdk.aws_elasticloadbalancingv2.ILoadBalancerV2,
    ) -> None:
        """
        :param load_balancer: -
        """
        jsii.create(LoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class UserPoolDomainTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.UserPoolDomainTarget",
):
    """Use a user pool domain as an alias record target."""

    def __init__(self, domain: aws_cdk.aws_cognito.UserPoolDomain) -> None:
        """
        :param domain: -
        """
        jsii.create(UserPoolDomainTarget, self, [domain])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: aws_cdk.aws_route53.IRecordSet,
    ) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


class ApiGateway(
    ApiGatewayDomain,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53-targets.ApiGateway",
):
    """Defines an API Gateway REST API as the alias target. Requires that the domain name will be defined through ``RestApiProps.domainName``.

    You can direct the alias to any ``apigateway.DomainName`` resource through the
    ``ApiGatewayDomain`` class.
    """

    def __init__(self, api: aws_cdk.aws_apigateway.RestApi) -> None:
        """
        :param api: -
        """
        jsii.create(ApiGateway, self, [api])


__all__ = [
    "ApiGateway",
    "ApiGatewayDomain",
    "ApiGatewayv2Domain",
    "BucketWebsiteTarget",
    "ClassicLoadBalancerTarget",
    "CloudFrontTarget",
    "InterfaceVpcEndpointTarget",
    "LoadBalancerTarget",
    "UserPoolDomainTarget",
]

publication.publish()
