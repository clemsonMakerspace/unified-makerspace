"""
## AWS::APIGatewayv2 Construct Library

<!--BEGIN STABILITY BANNER-->---


| Features | Stability |
| --- | --- |
| CFN Resources | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge) |
| Higher level constructs for HTTP APIs | ![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge) |
| Higher level constructs for Websocket APIs | ![Not Implemented](https://img.shields.io/badge/not--implemented-black.svg?style=for-the-badge) |

> **CFN Resources:** All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

> **Experimental:** Higher level constructs in this module that are marked as experimental are under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Table of Contents

* [Introduction](#introduction)
* [HTTP API](#http-api)

  * [Defining HTTP APIs](#defining-http-apis)
  * [Cross Origin Resource Sharing (CORS)](#cross-origin-resource-sharing-cors)
  * [Publishing HTTP APIs](#publishing-http-apis)
  * [Custom Domain](#custom-domain)
  * [Metrics](#metrics)
  * [VPC Link](#vpc-link)
  * [Private Integration](#private-integration)

## Introduction

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket
APIs at any scale. API developers can create APIs that access AWS or other web services, as well as data stored in the AWS Cloud.
As an API Gateway API developer, you can create APIs for use in your own client applications. Read the
[Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html).

This module supports features under [API Gateway v2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html)
that lets users set up Websocket and HTTP APIs.
REST APIs can be created using the `@aws-cdk/aws-apigateway` module.

## HTTP API

HTTP APIs enable creation of RESTful APIs that integrate with AWS Lambda functions, known as Lambda proxy integration,
or to any routable HTTP endpoint, known as HTTP proxy integration.

### Defining HTTP APIs

HTTP APIs have two fundamental concepts - Routes and Integrations.

Routes direct incoming API requests to backend resources. Routes consist of two parts: an HTTP method and a resource
path, such as, `GET /books`. Learn more at [Working with
routes](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-routes.html). Use the `ANY` method
to match any methods for a route that are not explicitly defined.

Integrations define how the HTTP API responds when a client reaches a specific Route. HTTP APIs support Lambda proxy
integration, HTTP proxy integration and, AWS service integrations, also known as private integrations. Learn more at
[Configuring integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations.html).

Integrations are available at the `aws-apigatewayv2-integrations` module and more information is available in that module.
As an early example, the following code snippet configures a route `GET /books` with an HTTP proxy integration all
configures all other HTTP method calls to `/books` to a lambda proxy.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
get_books_integration = HttpProxyIntegration(
    url="https://get-books-proxy.myproxy.internal"
)

books_default_fn = lambda_.Function(stack, "BooksDefaultFn", ...)
books_default_integration = LambdaProxyIntegration(
    handler=books_default_fn
)

http_api = HttpApi(stack, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[HttpMethod.GET],
    integration=get_books_integration
)
http_api.add_routes(
    path="/books",
    methods=[HttpMethod.ANY],
    integration=books_default_integration
)
```

The URL to the endpoint can be retrieved via the `apiEndpoint` attribute.

The `defaultIntegration` option while defining HTTP APIs lets you create a default catch-all integration that is
matched when a client reaches a route that is not explicitly defined.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpApi(stack, "HttpProxyApi",
    default_integration=HttpProxyIntegration(
        url="http://example.com"
    )
)
```

### Cross Origin Resource Sharing (CORS)

[Cross-origin resource sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a browser security
feature that restricts HTTP requests that are initiated from scripts running in the browser. Enabling CORS will allow
requests to your API from a web application hosted in a domain different from your API domain.

When configured CORS for an HTTP API, API Gateway automatically sends a response to preflight `OPTIONS` requests, even
if there isn't an `OPTIONS` route configured. Note that, when this option is used, API Gateway will ignore CORS headers
returned from your backend integration. Learn more about [Configuring CORS for an HTTP
API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html).

The `corsPreflight` option lets you specify a CORS configuration for an API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpApi(stack, "HttpProxyApi",
    cors_preflight={
        "allow_headers": ["Authorization"],
        "allow_methods": [HttpMethod.GET, HttpMethod.HEAD, HttpMethod.OPTIONS, HttpMethod.POST],
        "allow_origins": ["*"],
        "max_age": Duration.days(10)
    }
)
```

### Publishing HTTP APIs

A Stage is a logical reference to a lifecycle state of your API (for example, `dev`, `prod`, `beta`, or `v2`). API
stages are identified by their stage name. Each stage is a named reference to a deployment of the API made available for
client applications to call.

Use `HttpStage` to create a Stage resource for HTTP APIs. The following code sets up a Stage, whose URL is available at
`https://{api_id}.execute-api.{region}.amazonaws.com/beta`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpStage(stack, "Stage",
    http_api=api,
    stage_name="beta"
)
```

If you omit the `stageName` will create a `$default` stage. A `$default` stage is one that is served from the base of
the API's URL - `https://{api_id}.execute-api.{region}.amazonaws.com/`.

Note that, `HttpApi` will always creates a `$default` stage, unless the `createDefaultStage` property is unset.

### Custom Domain

Custom domain names are simpler and more intuitive URLs that you can provide to your API users. Custom domain name are associated to API stages.

The code snippet below creates a custom domain and configures a default domain mapping for your API that maps the
custom domain to the `$default` stage of the API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cert_arn = "arn:aws:acm:us-east-1:111111111111:certificate"
domain_name = "example.com"

dn = DomainName(stack, "DN",
    domain_name=domain_name,
    certificate=acm.Certificate.from_certificate_arn(stack, "cert", cert_arn)
)

api = HttpApi(stack, "HttpProxyProdApi",
    default_integration=LambdaProxyIntegration(handler=handler),
    # https://${dn.domainName}/foo goes to prodApi $default stage
    default_domain_mapping={
        "domain_name": dn,
        "mapping_key": "foo"
    }
)
```

To associate a specifc `Stage` to a custom domain mapping -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
api.add_stage("beta",
    stage_name="beta",
    auto_deploy=True,
    # https://${dn.domainName}/bar goes to the beta stage
    domain_mapping={
        "domain_name": dn,
        "mapping_key": "bar"
    }
)
```

The same domain name can be associated with stages across different `HttpApi` as so -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
api_demo = HttpApi(stack, "DemoApi",
    default_integration=LambdaProxyIntegration(handler=handler),
    # https://${dn.domainName}/demo goes to apiDemo $default stage
    default_domain_mapping={
        "domain_name": dn,
        "mapping_key": "demo"
    }
)
```

The `mappingKey` determines the base path of the URL with the custom domain. Each custom domain is only allowed
to have one API mapping with undefined `mappingKey`. If more than one API mappings are specified, `mappingKey` will be required for all of them. In the sample above, the custom domain is associated
with 3 API mapping resources across different APIs and Stages.

|        API     |     Stage   |   URL  |
| :------------: | :---------: | :----: |
| api | $default  |   `https://${domainName}/foo`  |
| api | beta  |   `https://${domainName}/bar`  |
| apiDemo | $default  |   `https://${domainName}/demo`  |

## Metrics

The API Gateway v2 service sends metrics around the performance of HTTP APIs to Amazon CloudWatch.
These metrics can be referred to using the metric APIs available on the `HttpApi` construct.
The APIs with the `metric` prefix can be used to get reference to specific metrics for this API. For example,
the method below refers to the client side errors metric for this API.

```
const api = new apigw.HttpApi(stack, 'my-api');
const clientErrorMetric = api.metricClientError();

```

Please note that this will return a metric for all the stages defined in the api. It is also possible to refer to metrics for a specific Stage using
the `metric` methods from the `Stage` construct.

```
const api = new apigw.HttpApi(stack, 'my-api');
const stage = new HttpStage(stack, 'Stage', {
   httpApi: api,
});
const clientErrorMetric = stage.metricClientError();
```

### VPC Link

Private integrations let HTTP APIs connect with AWS resources that are placed behind a VPC. These are usually Application
Load Balancers, Network Load Balancers or a Cloud Map service. The `VpcLink` construct enables this integration.
The following code creates a `VpcLink` to a private VPC.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(stack, "VPC")
vpc_link = VpcLink(stack, "VpcLink", vpc=vpc)
```

Any existing `VpcLink` resource can be imported into the CDK app via the `VpcLink.fromVpcLinkId()`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
awesome_link = VpcLink.from_vpc_link_id(stack, "awesome-vpc-link", "us-east-1_oiuR12Abd")
```

### Private Integration

Private integrations enable integrating an HTTP API route with private resources in a VPC, such as Application Load Balancers or
Amazon ECS container-based applications.  Using private integrations, resources in a VPC can be exposed for access by
clients outside of the VPC.

These integrations can be found in the [APIGatewayV2-Integrations](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigatewayv2-integrations-readme.html) constructs library.
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

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.BatchHttpRouteOptions",
    jsii_struct_bases=[],
    name_mapping={"integration": "integration"},
)
class BatchHttpRouteOptions:
    def __init__(self, *, integration: "IHttpRouteIntegration") -> None:
        """(experimental) Options used when configuring multiple routes, at once.

        The options here are the ones that would be configured for all being set up.

        :param integration: (experimental) The integration to be configured on this route.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
        }

    @builtins.property
    def integration(self) -> "IHttpRouteIntegration":
        """(experimental) The integration to be configured on this route.

        :stability: experimental
        """
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchHttpRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApi(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi",
):
    """A CloudFormation ``AWS::ApiGatewayV2::Api``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
    :cloudformationResource: AWS::ApiGatewayV2::Api
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_key_selection_expression: typing.Optional[builtins.str] = None,
        base_path: typing.Optional[builtins.str] = None,
        body: typing.Any = None,
        body_s3_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]] = None,
        cors_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        disable_schema_validation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        route_key: typing.Optional[builtins.str] = None,
        route_selection_expression: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        target: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::Api``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key_selection_expression: ``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.
        :param base_path: ``AWS::ApiGatewayV2::Api.BasePath``.
        :param body: ``AWS::ApiGatewayV2::Api.Body``.
        :param body_s3_location: ``AWS::ApiGatewayV2::Api.BodyS3Location``.
        :param cors_configuration: ``AWS::ApiGatewayV2::Api.CorsConfiguration``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Api.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Api.Description``.
        :param disable_execute_api_endpoint: ``AWS::ApiGatewayV2::Api.DisableExecuteApiEndpoint``.
        :param disable_schema_validation: ``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.
        :param fail_on_warnings: ``AWS::ApiGatewayV2::Api.FailOnWarnings``.
        :param name: ``AWS::ApiGatewayV2::Api.Name``.
        :param protocol_type: ``AWS::ApiGatewayV2::Api.ProtocolType``.
        :param route_key: ``AWS::ApiGatewayV2::Api.RouteKey``.
        :param route_selection_expression: ``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.
        :param tags: ``AWS::ApiGatewayV2::Api.Tags``.
        :param target: ``AWS::ApiGatewayV2::Api.Target``.
        :param version: ``AWS::ApiGatewayV2::Api.Version``.
        """
        props = CfnApiProps(
            api_key_selection_expression=api_key_selection_expression,
            base_path=base_path,
            body=body,
            body_s3_location=body_s3_location,
            cors_configuration=cors_configuration,
            credentials_arn=credentials_arn,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            disable_schema_validation=disable_schema_validation,
            fail_on_warnings=fail_on_warnings,
            name=name,
            protocol_type=protocol_type,
            route_key=route_key,
            route_selection_expression=route_selection_expression,
            tags=tags,
            target=target,
            version=version,
        )

        jsii.create(CfnApi, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrApiEndpoint")
    def attr_api_endpoint(self) -> builtins.str:
        """
        :cloudformationAttribute: ApiEndpoint
        """
        return jsii.get(self, "attrApiEndpoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::Api.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="body")
    def body(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Body``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        """
        return jsii.get(self, "body")

    @body.setter # type: ignore
    def body(self, value: typing.Any) -> None:
        jsii.set(self, "body", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiKeySelectionExpression")
    def api_key_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        """
        return jsii.get(self, "apiKeySelectionExpression")

    @api_key_selection_expression.setter # type: ignore
    def api_key_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "apiKeySelectionExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="basePath")
    def base_path(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.BasePath``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        """
        return jsii.get(self, "basePath")

    @base_path.setter # type: ignore
    def base_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "basePath", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bodyS3Location")
    def body_s3_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]]:
        """``AWS::ApiGatewayV2::Api.BodyS3Location``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        """
        return jsii.get(self, "bodyS3Location")

    @body_s3_location.setter # type: ignore
    def body_s3_location(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]],
    ) -> None:
        jsii.set(self, "bodyS3Location", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]]:
        """``AWS::ApiGatewayV2::Api.CorsConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        """
        return jsii.get(self, "corsConfiguration")

    @cors_configuration.setter # type: ignore
    def cors_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]],
    ) -> None:
        jsii.set(self, "corsConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.CredentialsArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        """
        return jsii.get(self, "credentialsArn")

    @credentials_arn.setter # type: ignore
    def credentials_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "credentialsArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="disableExecuteApiEndpoint")
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.DisableExecuteApiEndpoint``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableexecuteapiendpoint
        """
        return jsii.get(self, "disableExecuteApiEndpoint")

    @disable_execute_api_endpoint.setter # type: ignore
    def disable_execute_api_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "disableExecuteApiEndpoint", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="disableSchemaValidation")
    def disable_schema_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        """
        return jsii.get(self, "disableSchemaValidation")

    @disable_schema_validation.setter # type: ignore
    def disable_schema_validation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "disableSchemaValidation", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="failOnWarnings")
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.FailOnWarnings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        """
        return jsii.get(self, "failOnWarnings")

    @fail_on_warnings.setter # type: ignore
    def fail_on_warnings(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "failOnWarnings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.ProtocolType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        """
        return jsii.get(self, "protocolType")

    @protocol_type.setter # type: ignore
    def protocol_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "protocolType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.RouteKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        """
        return jsii.get(self, "routeKey")

    @route_key.setter # type: ignore
    def route_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "routeKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeSelectionExpression")
    def route_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        """
        return jsii.get(self, "routeSelectionExpression")

    @route_selection_expression.setter # type: ignore
    def route_selection_expression(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "routeSelectionExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Target``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        """
        return jsii.get(self, "target")

    @target.setter # type: ignore
    def target(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "target", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        """
        return jsii.get(self, "version")

    @version.setter # type: ignore
    def version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi.BodyS3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "etag": "etag",
            "key": "key",
            "version": "version",
        },
    )
    class BodyS3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            etag: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket: ``CfnApi.BodyS3LocationProperty.Bucket``.
            :param etag: ``CfnApi.BodyS3LocationProperty.Etag``.
            :param key: ``CfnApi.BodyS3LocationProperty.Key``.
            :param version: ``CfnApi.BodyS3LocationProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if etag is not None:
                self._values["etag"] = etag
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            """``CfnApi.BodyS3LocationProperty.Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-bucket
            """
            result = self._values.get("bucket")
            return result

        @builtins.property
        def etag(self) -> typing.Optional[builtins.str]:
            """``CfnApi.BodyS3LocationProperty.Etag``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-etag
            """
            result = self._values.get("etag")
            return result

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnApi.BodyS3LocationProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-key
            """
            result = self._values.get("key")
            return result

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            """``CfnApi.BodyS3LocationProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-version
            """
            result = self._values.get("version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BodyS3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi.CorsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "allow_origins": "allowOrigins",
            "expose_headers": "exposeHeaders",
            "max_age": "maxAge",
        },
    )
    class CorsProperty:
        def __init__(
            self,
            *,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            allow_headers: typing.Optional[typing.List[builtins.str]] = None,
            allow_methods: typing.Optional[typing.List[builtins.str]] = None,
            allow_origins: typing.Optional[typing.List[builtins.str]] = None,
            expose_headers: typing.Optional[typing.List[builtins.str]] = None,
            max_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param allow_credentials: ``CfnApi.CorsProperty.AllowCredentials``.
            :param allow_headers: ``CfnApi.CorsProperty.AllowHeaders``.
            :param allow_methods: ``CfnApi.CorsProperty.AllowMethods``.
            :param allow_origins: ``CfnApi.CorsProperty.AllowOrigins``.
            :param expose_headers: ``CfnApi.CorsProperty.ExposeHeaders``.
            :param max_age: ``CfnApi.CorsProperty.MaxAge``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if allow_origins is not None:
                self._values["allow_origins"] = allow_origins
            if expose_headers is not None:
                self._values["expose_headers"] = expose_headers
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnApi.CorsProperty.AllowCredentials``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowcredentials
            """
            result = self._values.get("allow_credentials")
            return result

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnApi.CorsProperty.AllowHeaders``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowheaders
            """
            result = self._values.get("allow_headers")
            return result

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnApi.CorsProperty.AllowMethods``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowmethods
            """
            result = self._values.get("allow_methods")
            return result

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnApi.CorsProperty.AllowOrigins``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-alloworigins
            """
            result = self._values.get("allow_origins")
            return result

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnApi.CorsProperty.ExposeHeaders``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-exposeheaders
            """
            result = self._values.get("expose_headers")
            return result

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            """``CfnApi.CorsProperty.MaxAge``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-maxage
            """
            result = self._values.get("max_age")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiGatewayManagedOverrides(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides",
):
    """A CloudFormation ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html
    :cloudformationResource: AWS::ApiGatewayV2::ApiGatewayManagedOverrides
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        integration: typing.Optional[typing.Union["CfnApiGatewayManagedOverrides.IntegrationOverridesProperty", aws_cdk.core.IResolvable]] = None,
        route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteOverridesProperty"]] = None,
        stage: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.StageOverridesProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.ApiId``.
        :param integration: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Integration``.
        :param route: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Route``.
        :param stage: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Stage``.
        """
        props = CfnApiGatewayManagedOverridesProps(
            api_id=api_id, integration=integration, route=route, stage=stage
        )

        jsii.create(CfnApiGatewayManagedOverrides, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integration")
    def integration(
        self,
    ) -> typing.Optional[typing.Union["CfnApiGatewayManagedOverrides.IntegrationOverridesProperty", aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Integration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integration
        """
        return jsii.get(self, "integration")

    @integration.setter # type: ignore
    def integration(
        self,
        value: typing.Optional[typing.Union["CfnApiGatewayManagedOverrides.IntegrationOverridesProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "integration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="route")
    def route(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteOverridesProperty"]]:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Route``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-route
        """
        return jsii.get(self, "route")

    @route.setter # type: ignore
    def route(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteOverridesProperty"]],
    ) -> None:
        jsii.set(self, "route", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stage")
    def stage(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.StageOverridesProperty"]]:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Stage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stage
        """
        return jsii.get(self, "stage")

    @stage.setter # type: ignore
    def stage(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.StageOverridesProperty"]],
    ) -> None:
        jsii.set(self, "stage", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.AccessLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingsProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param destination_arn: ``CfnApiGatewayManagedOverrides.AccessLogSettingsProperty.DestinationArn``.
            :param format: ``CfnApiGatewayManagedOverrides.AccessLogSettingsProperty.Format``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.AccessLogSettingsProperty.DestinationArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings-destinationarn
            """
            result = self._values.get("destination_arn")
            return result

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.AccessLogSettingsProperty.Format``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-accesslogsettings-format
            """
            result = self._values.get("format")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.IntegrationOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "integration_method": "integrationMethod",
            "payload_format_version": "payloadFormatVersion",
            "timeout_in_millis": "timeoutInMillis",
        },
    )
    class IntegrationOverridesProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            integration_method: typing.Optional[builtins.str] = None,
            payload_format_version: typing.Optional[builtins.str] = None,
            timeout_in_millis: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param description: ``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.Description``.
            :param integration_method: ``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.IntegrationMethod``.
            :param payload_format_version: ``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.PayloadFormatVersion``.
            :param timeout_in_millis: ``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.TimeoutInMillis``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if integration_method is not None:
                self._values["integration_method"] = integration_method
            if payload_format_version is not None:
                self._values["payload_format_version"] = payload_format_version
            if timeout_in_millis is not None:
                self._values["timeout_in_millis"] = timeout_in_millis

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.Description``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-description
            """
            result = self._values.get("description")
            return result

        @builtins.property
        def integration_method(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.IntegrationMethod``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-integrationmethod
            """
            result = self._values.get("integration_method")
            return result

        @builtins.property
        def payload_format_version(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.PayloadFormatVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-payloadformatversion
            """
            result = self._values.get("payload_format_version")
            return result

        @builtins.property
        def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
            """``CfnApiGatewayManagedOverrides.IntegrationOverridesProperty.TimeoutInMillis``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integrationoverrides-timeoutinmillis
            """
            result = self._values.get("timeout_in_millis")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegrationOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.RouteOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_scopes": "authorizationScopes",
            "authorization_type": "authorizationType",
            "authorizer_id": "authorizerId",
            "operation_name": "operationName",
            "target": "target",
        },
    )
    class RouteOverridesProperty:
        def __init__(
            self,
            *,
            authorization_scopes: typing.Optional[typing.List[builtins.str]] = None,
            authorization_type: typing.Optional[builtins.str] = None,
            authorizer_id: typing.Optional[builtins.str] = None,
            operation_name: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param authorization_scopes: ``CfnApiGatewayManagedOverrides.RouteOverridesProperty.AuthorizationScopes``.
            :param authorization_type: ``CfnApiGatewayManagedOverrides.RouteOverridesProperty.AuthorizationType``.
            :param authorizer_id: ``CfnApiGatewayManagedOverrides.RouteOverridesProperty.AuthorizerId``.
            :param operation_name: ``CfnApiGatewayManagedOverrides.RouteOverridesProperty.OperationName``.
            :param target: ``CfnApiGatewayManagedOverrides.RouteOverridesProperty.Target``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if authorization_scopes is not None:
                self._values["authorization_scopes"] = authorization_scopes
            if authorization_type is not None:
                self._values["authorization_type"] = authorization_type
            if authorizer_id is not None:
                self._values["authorizer_id"] = authorizer_id
            if operation_name is not None:
                self._values["operation_name"] = operation_name
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnApiGatewayManagedOverrides.RouteOverridesProperty.AuthorizationScopes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-authorizationscopes
            """
            result = self._values.get("authorization_scopes")
            return result

        @builtins.property
        def authorization_type(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.RouteOverridesProperty.AuthorizationType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-authorizationtype
            """
            result = self._values.get("authorization_type")
            return result

        @builtins.property
        def authorizer_id(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.RouteOverridesProperty.AuthorizerId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-authorizerid
            """
            result = self._values.get("authorizer_id")
            return result

        @builtins.property
        def operation_name(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.RouteOverridesProperty.OperationName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-operationname
            """
            result = self._values.get("operation_name")
            return result

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.RouteOverridesProperty.Target``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routeoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routeoverrides-target
            """
            result = self._values.get("target")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param data_trace_enabled: ``CfnApiGatewayManagedOverrides.RouteSettingsProperty.DataTraceEnabled``.
            :param detailed_metrics_enabled: ``CfnApiGatewayManagedOverrides.RouteSettingsProperty.DetailedMetricsEnabled``.
            :param logging_level: ``CfnApiGatewayManagedOverrides.RouteSettingsProperty.LoggingLevel``.
            :param throttling_burst_limit: ``CfnApiGatewayManagedOverrides.RouteSettingsProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnApiGatewayManagedOverrides.RouteSettingsProperty.ThrottlingRateLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnApiGatewayManagedOverrides.RouteSettingsProperty.DataTraceEnabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-datatraceenabled
            """
            result = self._values.get("data_trace_enabled")
            return result

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnApiGatewayManagedOverrides.RouteSettingsProperty.DetailedMetricsEnabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-detailedmetricsenabled
            """
            result = self._values.get("detailed_metrics_enabled")
            return result

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.RouteSettingsProperty.LoggingLevel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-logginglevel
            """
            result = self._values.get("logging_level")
            return result

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnApiGatewayManagedOverrides.RouteSettingsProperty.ThrottlingBurstLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-throttlingburstlimit
            """
            result = self._values.get("throttling_burst_limit")
            return result

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnApiGatewayManagedOverrides.RouteSettingsProperty.ThrottlingRateLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-routesettings.html#cfn-apigatewayv2-apigatewaymanagedoverrides-routesettings-throttlingratelimit
            """
            result = self._values.get("throttling_rate_limit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverrides.StageOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_log_settings": "accessLogSettings",
            "auto_deploy": "autoDeploy",
            "default_route_settings": "defaultRouteSettings",
            "description": "description",
            "route_settings": "routeSettings",
            "stage_variables": "stageVariables",
        },
    )
    class StageOverridesProperty:
        def __init__(
            self,
            *,
            access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.AccessLogSettingsProperty"]] = None,
            auto_deploy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteSettingsProperty"]] = None,
            description: typing.Optional[builtins.str] = None,
            route_settings: typing.Any = None,
            stage_variables: typing.Any = None,
        ) -> None:
            """
            :param access_log_settings: ``CfnApiGatewayManagedOverrides.StageOverridesProperty.AccessLogSettings``.
            :param auto_deploy: ``CfnApiGatewayManagedOverrides.StageOverridesProperty.AutoDeploy``.
            :param default_route_settings: ``CfnApiGatewayManagedOverrides.StageOverridesProperty.DefaultRouteSettings``.
            :param description: ``CfnApiGatewayManagedOverrides.StageOverridesProperty.Description``.
            :param route_settings: ``CfnApiGatewayManagedOverrides.StageOverridesProperty.RouteSettings``.
            :param stage_variables: ``CfnApiGatewayManagedOverrides.StageOverridesProperty.StageVariables``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if access_log_settings is not None:
                self._values["access_log_settings"] = access_log_settings
            if auto_deploy is not None:
                self._values["auto_deploy"] = auto_deploy
            if default_route_settings is not None:
                self._values["default_route_settings"] = default_route_settings
            if description is not None:
                self._values["description"] = description
            if route_settings is not None:
                self._values["route_settings"] = route_settings
            if stage_variables is not None:
                self._values["stage_variables"] = stage_variables

        @builtins.property
        def access_log_settings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.AccessLogSettingsProperty"]]:
            """``CfnApiGatewayManagedOverrides.StageOverridesProperty.AccessLogSettings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-accesslogsettings
            """
            result = self._values.get("access_log_settings")
            return result

        @builtins.property
        def auto_deploy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnApiGatewayManagedOverrides.StageOverridesProperty.AutoDeploy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-autodeploy
            """
            result = self._values.get("auto_deploy")
            return result

        @builtins.property
        def default_route_settings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApiGatewayManagedOverrides.RouteSettingsProperty"]]:
            """``CfnApiGatewayManagedOverrides.StageOverridesProperty.DefaultRouteSettings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-defaultroutesettings
            """
            result = self._values.get("default_route_settings")
            return result

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            """``CfnApiGatewayManagedOverrides.StageOverridesProperty.Description``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-description
            """
            result = self._values.get("description")
            return result

        @builtins.property
        def route_settings(self) -> typing.Any:
            """``CfnApiGatewayManagedOverrides.StageOverridesProperty.RouteSettings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-routesettings
            """
            result = self._values.get("route_settings")
            return result

        @builtins.property
        def stage_variables(self) -> typing.Any:
            """``CfnApiGatewayManagedOverrides.StageOverridesProperty.StageVariables``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-apigatewaymanagedoverrides-stageoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stageoverrides-stagevariables
            """
            result = self._values.get("stage_variables")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiGatewayManagedOverridesProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "integration": "integration",
        "route": "route",
        "stage": "stage",
    },
)
class CfnApiGatewayManagedOverridesProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        integration: typing.Optional[typing.Union[CfnApiGatewayManagedOverrides.IntegrationOverridesProperty, aws_cdk.core.IResolvable]] = None,
        route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.RouteOverridesProperty]] = None,
        stage: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.StageOverridesProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides``.

        :param api_id: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.ApiId``.
        :param integration: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Integration``.
        :param route: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Route``.
        :param stage: ``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Stage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
        }
        if integration is not None:
            self._values["integration"] = integration
        if route is not None:
            self._values["route"] = route
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def integration(
        self,
    ) -> typing.Optional[typing.Union[CfnApiGatewayManagedOverrides.IntegrationOverridesProperty, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Integration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-integration
        """
        result = self._values.get("integration")
        return result

    @builtins.property
    def route(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.RouteOverridesProperty]]:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Route``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-route
        """
        result = self._values.get("route")
        return result

    @builtins.property
    def stage(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApiGatewayManagedOverrides.StageOverridesProperty]]:
        """``AWS::ApiGatewayV2::ApiGatewayManagedOverrides.Stage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apigatewaymanagedoverrides.html#cfn-apigatewayv2-apigatewaymanagedoverrides-stage
        """
        result = self._values.get("stage")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiGatewayManagedOverridesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiMapping(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiMapping",
):
    """A CloudFormation ``AWS::ApiGatewayV2::ApiMapping``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    :cloudformationResource: AWS::ApiGatewayV2::ApiMapping
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        domain_name: builtins.str,
        stage: builtins.str,
        api_mapping_key: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::ApiMapping``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::ApiMapping.ApiId``.
        :param domain_name: ``AWS::ApiGatewayV2::ApiMapping.DomainName``.
        :param stage: ``AWS::ApiGatewayV2::ApiMapping.Stage``.
        :param api_mapping_key: ``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.
        """
        props = CfnApiMappingProps(
            api_id=api_id,
            domain_name=domain_name,
            stage=stage,
            api_mapping_key=api_mapping_key,
        )

        jsii.create(CfnApiMapping, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiMapping.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiMapping.DomainName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter # type: ignore
    def domain_name(self, value: builtins.str) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiMapping.Stage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        """
        return jsii.get(self, "stage")

    @stage.setter # type: ignore
    def stage(self, value: builtins.str) -> None:
        jsii.set(self, "stage", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiMappingKey")
    def api_mapping_key(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        """
        return jsii.get(self, "apiMappingKey")

    @api_mapping_key.setter # type: ignore
    def api_mapping_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "apiMappingKey", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiMappingProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "domain_name": "domainName",
        "stage": "stage",
        "api_mapping_key": "apiMappingKey",
    },
)
class CfnApiMappingProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        domain_name: builtins.str,
        stage: builtins.str,
        api_mapping_key: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::ApiMapping``.

        :param api_id: ``AWS::ApiGatewayV2::ApiMapping.ApiId``.
        :param domain_name: ``AWS::ApiGatewayV2::ApiMapping.DomainName``.
        :param stage: ``AWS::ApiGatewayV2::ApiMapping.Stage``.
        :param api_mapping_key: ``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "domain_name": domain_name,
            "stage": stage,
        }
        if api_mapping_key is not None:
            self._values["api_mapping_key"] = api_mapping_key

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiMapping.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def domain_name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiMapping.DomainName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def stage(self) -> builtins.str:
        """``AWS::ApiGatewayV2::ApiMapping.Stage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        """
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return result

    @builtins.property
    def api_mapping_key(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        """
        result = self._values.get("api_mapping_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiMappingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_selection_expression": "apiKeySelectionExpression",
        "base_path": "basePath",
        "body": "body",
        "body_s3_location": "bodyS3Location",
        "cors_configuration": "corsConfiguration",
        "credentials_arn": "credentialsArn",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "disable_schema_validation": "disableSchemaValidation",
        "fail_on_warnings": "failOnWarnings",
        "name": "name",
        "protocol_type": "protocolType",
        "route_key": "routeKey",
        "route_selection_expression": "routeSelectionExpression",
        "tags": "tags",
        "target": "target",
        "version": "version",
    },
)
class CfnApiProps:
    def __init__(
        self,
        *,
        api_key_selection_expression: typing.Optional[builtins.str] = None,
        base_path: typing.Optional[builtins.str] = None,
        body: typing.Any = None,
        body_s3_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.BodyS3LocationProperty]] = None,
        cors_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.CorsProperty]] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        disable_schema_validation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        route_key: typing.Optional[builtins.str] = None,
        route_selection_expression: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        target: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Api``.

        :param api_key_selection_expression: ``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.
        :param base_path: ``AWS::ApiGatewayV2::Api.BasePath``.
        :param body: ``AWS::ApiGatewayV2::Api.Body``.
        :param body_s3_location: ``AWS::ApiGatewayV2::Api.BodyS3Location``.
        :param cors_configuration: ``AWS::ApiGatewayV2::Api.CorsConfiguration``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Api.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Api.Description``.
        :param disable_execute_api_endpoint: ``AWS::ApiGatewayV2::Api.DisableExecuteApiEndpoint``.
        :param disable_schema_validation: ``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.
        :param fail_on_warnings: ``AWS::ApiGatewayV2::Api.FailOnWarnings``.
        :param name: ``AWS::ApiGatewayV2::Api.Name``.
        :param protocol_type: ``AWS::ApiGatewayV2::Api.ProtocolType``.
        :param route_key: ``AWS::ApiGatewayV2::Api.RouteKey``.
        :param route_selection_expression: ``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.
        :param tags: ``AWS::ApiGatewayV2::Api.Tags``.
        :param target: ``AWS::ApiGatewayV2::Api.Target``.
        :param version: ``AWS::ApiGatewayV2::Api.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if api_key_selection_expression is not None:
            self._values["api_key_selection_expression"] = api_key_selection_expression
        if base_path is not None:
            self._values["base_path"] = base_path
        if body is not None:
            self._values["body"] = body
        if body_s3_location is not None:
            self._values["body_s3_location"] = body_s3_location
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if credentials_arn is not None:
            self._values["credentials_arn"] = credentials_arn
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if disable_schema_validation is not None:
            self._values["disable_schema_validation"] = disable_schema_validation
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if name is not None:
            self._values["name"] = name
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if route_key is not None:
            self._values["route_key"] = route_key
        if route_selection_expression is not None:
            self._values["route_selection_expression"] = route_selection_expression
        if tags is not None:
            self._values["tags"] = tags
        if target is not None:
            self._values["target"] = target
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def api_key_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        """
        result = self._values.get("api_key_selection_expression")
        return result

    @builtins.property
    def base_path(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.BasePath``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        """
        result = self._values.get("base_path")
        return result

    @builtins.property
    def body(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Body``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        """
        result = self._values.get("body")
        return result

    @builtins.property
    def body_s3_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.BodyS3LocationProperty]]:
        """``AWS::ApiGatewayV2::Api.BodyS3Location``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        """
        result = self._values.get("body_s3_location")
        return result

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApi.CorsProperty]]:
        """``AWS::ApiGatewayV2::Api.CorsConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        """
        result = self._values.get("cors_configuration")
        return result

    @builtins.property
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.CredentialsArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        """
        result = self._values.get("credentials_arn")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.DisableExecuteApiEndpoint``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableexecuteapiendpoint
        """
        result = self._values.get("disable_execute_api_endpoint")
        return result

    @builtins.property
    def disable_schema_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        """
        result = self._values.get("disable_schema_validation")
        return result

    @builtins.property
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.FailOnWarnings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        """
        result = self._values.get("fail_on_warnings")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.ProtocolType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        """
        result = self._values.get("protocol_type")
        return result

    @builtins.property
    def route_key(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.RouteKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        """
        result = self._values.get("route_key")
        return result

    @builtins.property
    def route_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        """
        result = self._values.get("route_selection_expression")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Target``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        """
        result = self._values.get("target")
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Api.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAuthorizer(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizer",
):
    """A CloudFormation ``AWS::ApiGatewayV2::Authorizer``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
    :cloudformationResource: AWS::ApiGatewayV2::Authorizer
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        authorizer_type: builtins.str,
        identity_source: typing.List[builtins.str],
        name: builtins.str,
        authorizer_credentials_arn: typing.Optional[builtins.str] = None,
        authorizer_payload_format_version: typing.Optional[builtins.str] = None,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
        enable_simple_responses: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
        jwt_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::Authorizer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Authorizer.ApiId``.
        :param authorizer_type: ``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.
        :param identity_source: ``AWS::ApiGatewayV2::Authorizer.IdentitySource``.
        :param name: ``AWS::ApiGatewayV2::Authorizer.Name``.
        :param authorizer_credentials_arn: ``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.
        :param authorizer_payload_format_version: ``AWS::ApiGatewayV2::Authorizer.AuthorizerPayloadFormatVersion``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.
        :param enable_simple_responses: ``AWS::ApiGatewayV2::Authorizer.EnableSimpleResponses``.
        :param identity_validation_expression: ``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.
        :param jwt_configuration: ``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.
        """
        props = CfnAuthorizerProps(
            api_id=api_id,
            authorizer_type=authorizer_type,
            identity_source=identity_source,
            name=name,
            authorizer_credentials_arn=authorizer_credentials_arn,
            authorizer_payload_format_version=authorizer_payload_format_version,
            authorizer_result_ttl_in_seconds=authorizer_result_ttl_in_seconds,
            authorizer_uri=authorizer_uri,
            enable_simple_responses=enable_simple_responses,
            identity_validation_expression=identity_validation_expression,
            jwt_configuration=jwt_configuration,
        )

        jsii.create(CfnAuthorizer, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Authorizer.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizerType")
    def authorizer_type(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        """
        return jsii.get(self, "authorizerType")

    @authorizer_type.setter # type: ignore
    def authorizer_type(self, value: builtins.str) -> None:
        jsii.set(self, "authorizerType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identitySource")
    def identity_source(self) -> typing.List[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentitySource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        """
        return jsii.get(self, "identitySource")

    @identity_source.setter # type: ignore
    def identity_source(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "identitySource", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Authorizer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizerCredentialsArn")
    def authorizer_credentials_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        """
        return jsii.get(self, "authorizerCredentialsArn")

    @authorizer_credentials_arn.setter # type: ignore
    def authorizer_credentials_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authorizerCredentialsArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizerPayloadFormatVersion")
    def authorizer_payload_format_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerPayloadFormatVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerpayloadformatversion
        """
        return jsii.get(self, "authorizerPayloadFormatVersion")

    @authorizer_payload_format_version.setter # type: ignore
    def authorizer_payload_format_version(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "authorizerPayloadFormatVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        """
        return jsii.get(self, "authorizerResultTtlInSeconds")

    @authorizer_result_ttl_in_seconds.setter # type: ignore
    def authorizer_result_ttl_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "authorizerResultTtlInSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        """
        return jsii.get(self, "authorizerUri")

    @authorizer_uri.setter # type: ignore
    def authorizer_uri(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authorizerUri", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enableSimpleResponses")
    def enable_simple_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Authorizer.EnableSimpleResponses``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-enablesimpleresponses
        """
        return jsii.get(self, "enableSimpleResponses")

    @enable_simple_responses.setter # type: ignore
    def enable_simple_responses(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "enableSimpleResponses", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        """
        return jsii.get(self, "identityValidationExpression")

    @identity_validation_expression.setter # type: ignore
    def identity_validation_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "identityValidationExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jwtConfiguration")
    def jwt_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]]:
        """``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        """
        return jsii.get(self, "jwtConfiguration")

    @jwt_configuration.setter # type: ignore
    def jwt_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "jwtConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizer.JWTConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"audience": "audience", "issuer": "issuer"},
    )
    class JWTConfigurationProperty:
        def __init__(
            self,
            *,
            audience: typing.Optional[typing.List[builtins.str]] = None,
            issuer: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param audience: ``CfnAuthorizer.JWTConfigurationProperty.Audience``.
            :param issuer: ``CfnAuthorizer.JWTConfigurationProperty.Issuer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if audience is not None:
                self._values["audience"] = audience
            if issuer is not None:
                self._values["issuer"] = issuer

        @builtins.property
        def audience(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnAuthorizer.JWTConfigurationProperty.Audience``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-audience
            """
            result = self._values.get("audience")
            return result

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            """``CfnAuthorizer.JWTConfigurationProperty.Issuer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-issuer
            """
            result = self._values.get("issuer")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JWTConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "authorizer_type": "authorizerType",
        "identity_source": "identitySource",
        "name": "name",
        "authorizer_credentials_arn": "authorizerCredentialsArn",
        "authorizer_payload_format_version": "authorizerPayloadFormatVersion",
        "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
        "authorizer_uri": "authorizerUri",
        "enable_simple_responses": "enableSimpleResponses",
        "identity_validation_expression": "identityValidationExpression",
        "jwt_configuration": "jwtConfiguration",
    },
)
class CfnAuthorizerProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        authorizer_type: builtins.str,
        identity_source: typing.List[builtins.str],
        name: builtins.str,
        authorizer_credentials_arn: typing.Optional[builtins.str] = None,
        authorizer_payload_format_version: typing.Optional[builtins.str] = None,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
        enable_simple_responses: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
        jwt_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAuthorizer.JWTConfigurationProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Authorizer``.

        :param api_id: ``AWS::ApiGatewayV2::Authorizer.ApiId``.
        :param authorizer_type: ``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.
        :param identity_source: ``AWS::ApiGatewayV2::Authorizer.IdentitySource``.
        :param name: ``AWS::ApiGatewayV2::Authorizer.Name``.
        :param authorizer_credentials_arn: ``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.
        :param authorizer_payload_format_version: ``AWS::ApiGatewayV2::Authorizer.AuthorizerPayloadFormatVersion``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.
        :param enable_simple_responses: ``AWS::ApiGatewayV2::Authorizer.EnableSimpleResponses``.
        :param identity_validation_expression: ``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.
        :param jwt_configuration: ``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "authorizer_type": authorizer_type,
            "identity_source": identity_source,
            "name": name,
        }
        if authorizer_credentials_arn is not None:
            self._values["authorizer_credentials_arn"] = authorizer_credentials_arn
        if authorizer_payload_format_version is not None:
            self._values["authorizer_payload_format_version"] = authorizer_payload_format_version
        if authorizer_result_ttl_in_seconds is not None:
            self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if authorizer_uri is not None:
            self._values["authorizer_uri"] = authorizer_uri
        if enable_simple_responses is not None:
            self._values["enable_simple_responses"] = enable_simple_responses
        if identity_validation_expression is not None:
            self._values["identity_validation_expression"] = identity_validation_expression
        if jwt_configuration is not None:
            self._values["jwt_configuration"] = jwt_configuration

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Authorizer.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def authorizer_type(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        """
        result = self._values.get("authorizer_type")
        assert result is not None, "Required property 'authorizer_type' is missing"
        return result

    @builtins.property
    def identity_source(self) -> typing.List[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentitySource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        """
        result = self._values.get("identity_source")
        assert result is not None, "Required property 'identity_source' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Authorizer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def authorizer_credentials_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        """
        result = self._values.get("authorizer_credentials_arn")
        return result

    @builtins.property
    def authorizer_payload_format_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerPayloadFormatVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerpayloadformatversion
        """
        result = self._values.get("authorizer_payload_format_version")
        return result

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        """
        result = self._values.get("authorizer_result_ttl_in_seconds")
        return result

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        """
        result = self._values.get("authorizer_uri")
        return result

    @builtins.property
    def enable_simple_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Authorizer.EnableSimpleResponses``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-enablesimpleresponses
        """
        result = self._values.get("enable_simple_responses")
        return result

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        """
        result = self._values.get("identity_validation_expression")
        return result

    @builtins.property
    def jwt_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAuthorizer.JWTConfigurationProperty]]:
        """``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        """
        result = self._values.get("jwt_configuration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeployment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDeployment",
):
    """A CloudFormation ``AWS::ApiGatewayV2::Deployment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
    :cloudformationResource: AWS::ApiGatewayV2::Deployment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Deployment.ApiId``.
        :param description: ``AWS::ApiGatewayV2::Deployment.Description``.
        :param stage_name: ``AWS::ApiGatewayV2::Deployment.StageName``.
        """
        props = CfnDeploymentProps(
            api_id=api_id, description=description, stage_name=stage_name
        )

        jsii.create(CfnDeployment, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Deployment.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Deployment.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Deployment.StageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        """
        return jsii.get(self, "stageName")

    @stage_name.setter # type: ignore
    def stage_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "stageName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "description": "description",
        "stage_name": "stageName",
    },
)
class CfnDeploymentProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Deployment``.

        :param api_id: ``AWS::ApiGatewayV2::Deployment.ApiId``.
        :param description: ``AWS::ApiGatewayV2::Deployment.Description``.
        :param stage_name: ``AWS::ApiGatewayV2::Deployment.StageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
        }
        if description is not None:
            self._values["description"] = description
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Deployment.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Deployment.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Deployment.StageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        """
        result = self._values.get("stage_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDomainName(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName",
):
    """A CloudFormation ``AWS::ApiGatewayV2::DomainName``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    :cloudformationResource: AWS::ApiGatewayV2::DomainName
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        domain_name_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.DomainNameConfigurationProperty"]]]] = None,
        mutual_tls_authentication: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.MutualTlsAuthenticationProperty"]] = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::DomainName``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::ApiGatewayV2::DomainName.DomainName``.
        :param domain_name_configurations: ``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.
        :param mutual_tls_authentication: ``AWS::ApiGatewayV2::DomainName.MutualTlsAuthentication``.
        :param tags: ``AWS::ApiGatewayV2::DomainName.Tags``.
        """
        props = CfnDomainNameProps(
            domain_name=domain_name,
            domain_name_configurations=domain_name_configurations,
            mutual_tls_authentication=mutual_tls_authentication,
            tags=tags,
        )

        jsii.create(CfnDomainName, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrRegionalDomainName")
    def attr_regional_domain_name(self) -> builtins.str:
        """
        :cloudformationAttribute: RegionalDomainName
        """
        return jsii.get(self, "attrRegionalDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrRegionalHostedZoneId")
    def attr_regional_hosted_zone_id(self) -> builtins.str:
        """
        :cloudformationAttribute: RegionalHostedZoneId
        """
        return jsii.get(self, "attrRegionalHostedZoneId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::DomainName.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::DomainName.DomainName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter # type: ignore
    def domain_name(self, value: builtins.str) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainNameConfigurations")
    def domain_name_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.DomainNameConfigurationProperty"]]]]:
        """``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        """
        return jsii.get(self, "domainNameConfigurations")

    @domain_name_configurations.setter # type: ignore
    def domain_name_configurations(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.DomainNameConfigurationProperty"]]]],
    ) -> None:
        jsii.set(self, "domainNameConfigurations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mutualTlsAuthentication")
    def mutual_tls_authentication(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.MutualTlsAuthenticationProperty"]]:
        """``AWS::ApiGatewayV2::DomainName.MutualTlsAuthentication``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-mutualtlsauthentication
        """
        return jsii.get(self, "mutualTlsAuthentication")

    @mutual_tls_authentication.setter # type: ignore
    def mutual_tls_authentication(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDomainName.MutualTlsAuthenticationProperty"]],
    ) -> None:
        jsii.set(self, "mutualTlsAuthentication", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName.DomainNameConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "certificate_name": "certificateName",
            "endpoint_type": "endpointType",
            "security_policy": "securityPolicy",
        },
    )
    class DomainNameConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            certificate_name: typing.Optional[builtins.str] = None,
            endpoint_type: typing.Optional[builtins.str] = None,
            security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param certificate_arn: ``CfnDomainName.DomainNameConfigurationProperty.CertificateArn``.
            :param certificate_name: ``CfnDomainName.DomainNameConfigurationProperty.CertificateName``.
            :param endpoint_type: ``CfnDomainName.DomainNameConfigurationProperty.EndpointType``.
            :param security_policy: ``CfnDomainName.DomainNameConfigurationProperty.SecurityPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if certificate_name is not None:
                self._values["certificate_name"] = certificate_name
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if security_policy is not None:
                self._values["security_policy"] = security_policy

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDomainName.DomainNameConfigurationProperty.CertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatearn
            """
            result = self._values.get("certificate_arn")
            return result

        @builtins.property
        def certificate_name(self) -> typing.Optional[builtins.str]:
            """``CfnDomainName.DomainNameConfigurationProperty.CertificateName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatename
            """
            result = self._values.get("certificate_name")
            return result

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            """``CfnDomainName.DomainNameConfigurationProperty.EndpointType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-endpointtype
            """
            result = self._values.get("endpoint_type")
            return result

        @builtins.property
        def security_policy(self) -> typing.Optional[builtins.str]:
            """``CfnDomainName.DomainNameConfigurationProperty.SecurityPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-securitypolicy
            """
            result = self._values.get("security_policy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainNameConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param truststore_uri: ``CfnDomainName.MutualTlsAuthenticationProperty.TruststoreUri``.
            :param truststore_version: ``CfnDomainName.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            """``CfnDomainName.MutualTlsAuthenticationProperty.TruststoreUri``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreuri
            """
            result = self._values.get("truststore_uri")
            return result

        @builtins.property
        def truststore_version(self) -> typing.Optional[builtins.str]:
            """``CfnDomainName.MutualTlsAuthenticationProperty.TruststoreVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-mutualtlsauthentication.html#cfn-apigatewayv2-domainname-mutualtlsauthentication-truststoreversion
            """
            result = self._values.get("truststore_version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainNameProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "domain_name_configurations": "domainNameConfigurations",
        "mutual_tls_authentication": "mutualTlsAuthentication",
        "tags": "tags",
    },
)
class CfnDomainNameProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        domain_name_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.DomainNameConfigurationProperty]]]] = None,
        mutual_tls_authentication: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.MutualTlsAuthenticationProperty]] = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::DomainName``.

        :param domain_name: ``AWS::ApiGatewayV2::DomainName.DomainName``.
        :param domain_name_configurations: ``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.
        :param mutual_tls_authentication: ``AWS::ApiGatewayV2::DomainName.MutualTlsAuthentication``.
        :param tags: ``AWS::ApiGatewayV2::DomainName.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if domain_name_configurations is not None:
            self._values["domain_name_configurations"] = domain_name_configurations
        if mutual_tls_authentication is not None:
            self._values["mutual_tls_authentication"] = mutual_tls_authentication
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::DomainName.DomainName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def domain_name_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.DomainNameConfigurationProperty]]]]:
        """``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        """
        result = self._values.get("domain_name_configurations")
        return result

    @builtins.property
    def mutual_tls_authentication(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDomainName.MutualTlsAuthenticationProperty]]:
        """``AWS::ApiGatewayV2::DomainName.MutualTlsAuthentication``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-mutualtlsauthentication
        """
        result = self._values.get("mutual_tls_authentication")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::DomainName.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegration(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration",
):
    """A CloudFormation ``AWS::ApiGatewayV2::Integration``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
    :cloudformationResource: AWS::ApiGatewayV2::Integration
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        integration_type: builtins.str,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[builtins.str] = None,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        integration_method: typing.Optional[builtins.str] = None,
        integration_subtype: typing.Optional[builtins.str] = None,
        integration_uri: typing.Optional[builtins.str] = None,
        passthrough_behavior: typing.Optional[builtins.str] = None,
        payload_format_version: typing.Optional[builtins.str] = None,
        request_parameters: typing.Any = None,
        request_templates: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
        timeout_in_millis: typing.Optional[jsii.Number] = None,
        tls_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::Integration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Integration.ApiId``.
        :param integration_type: ``AWS::ApiGatewayV2::Integration.IntegrationType``.
        :param connection_id: ``AWS::ApiGatewayV2::Integration.ConnectionId``.
        :param connection_type: ``AWS::ApiGatewayV2::Integration.ConnectionType``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Integration.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Integration.Description``.
        :param integration_method: ``AWS::ApiGatewayV2::Integration.IntegrationMethod``.
        :param integration_subtype: ``AWS::ApiGatewayV2::Integration.IntegrationSubtype``.
        :param integration_uri: ``AWS::ApiGatewayV2::Integration.IntegrationUri``.
        :param passthrough_behavior: ``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.
        :param payload_format_version: ``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.
        :param request_parameters: ``AWS::ApiGatewayV2::Integration.RequestParameters``.
        :param request_templates: ``AWS::ApiGatewayV2::Integration.RequestTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.
        :param timeout_in_millis: ``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.
        :param tls_config: ``AWS::ApiGatewayV2::Integration.TlsConfig``.
        """
        props = CfnIntegrationProps(
            api_id=api_id,
            integration_type=integration_type,
            connection_id=connection_id,
            connection_type=connection_type,
            content_handling_strategy=content_handling_strategy,
            credentials_arn=credentials_arn,
            description=description,
            integration_method=integration_method,
            integration_subtype=integration_subtype,
            integration_uri=integration_uri,
            passthrough_behavior=passthrough_behavior,
            payload_format_version=payload_format_version,
            request_parameters=request_parameters,
            request_templates=request_templates,
            template_selection_expression=template_selection_expression,
            timeout_in_millis=timeout_in_millis,
            tls_config=tls_config,
        )

        jsii.create(CfnIntegration, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Integration.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Integration.IntegrationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        """
        return jsii.get(self, "integrationType")

    @integration_type.setter # type: ignore
    def integration_type(self, value: builtins.str) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        """
        return jsii.get(self, "requestParameters")

    @request_parameters.setter # type: ignore
    def request_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "requestParameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="requestTemplates")
    def request_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestTemplates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        """
        return jsii.get(self, "requestTemplates")

    @request_templates.setter # type: ignore
    def request_templates(self, value: typing.Any) -> None:
        jsii.set(self, "requestTemplates", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectionid
        """
        return jsii.get(self, "connectionId")

    @connection_id.setter # type: ignore
    def connection_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "connectionId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        """
        return jsii.get(self, "connectionType")

    @connection_type.setter # type: ignore
    def connection_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        """
        return jsii.get(self, "contentHandlingStrategy")

    @content_handling_strategy.setter # type: ignore
    def content_handling_strategy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.CredentialsArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        """
        return jsii.get(self, "credentialsArn")

    @credentials_arn.setter # type: ignore
    def credentials_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "credentialsArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationMethod")
    def integration_method(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        """
        return jsii.get(self, "integrationMethod")

    @integration_method.setter # type: ignore
    def integration_method(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "integrationMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationSubtype")
    def integration_subtype(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationSubtype``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationsubtype
        """
        return jsii.get(self, "integrationSubtype")

    @integration_subtype.setter # type: ignore
    def integration_subtype(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "integrationSubtype", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationUri")
    def integration_uri(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationUri``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        """
        return jsii.get(self, "integrationUri")

    @integration_uri.setter # type: ignore
    def integration_uri(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "integrationUri", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="passthroughBehavior")
    def passthrough_behavior(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        """
        return jsii.get(self, "passthroughBehavior")

    @passthrough_behavior.setter # type: ignore
    def passthrough_behavior(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "passthroughBehavior", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="payloadFormatVersion")
    def payload_format_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        """
        return jsii.get(self, "payloadFormatVersion")

    @payload_format_version.setter # type: ignore
    def payload_format_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "payloadFormatVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        """
        return jsii.get(self, "templateSelectionExpression")

    @template_selection_expression.setter # type: ignore
    def template_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "templateSelectionExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeoutInMillis")
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        """
        return jsii.get(self, "timeoutInMillis")

    @timeout_in_millis.setter # type: ignore
    def timeout_in_millis(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMillis", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tlsConfig")
    def tls_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]]:
        """``AWS::ApiGatewayV2::Integration.TlsConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-tlsconfig
        """
        return jsii.get(self, "tlsConfig")

    @tls_config.setter # type: ignore
    def tls_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]],
    ) -> None:
        jsii.set(self, "tlsConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration.TlsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"server_name_to_verify": "serverNameToVerify"},
    )
    class TlsConfigProperty:
        def __init__(
            self,
            *,
            server_name_to_verify: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param server_name_to_verify: ``CfnIntegration.TlsConfigProperty.ServerNameToVerify``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if server_name_to_verify is not None:
                self._values["server_name_to_verify"] = server_name_to_verify

        @builtins.property
        def server_name_to_verify(self) -> typing.Optional[builtins.str]:
            """``CfnIntegration.TlsConfigProperty.ServerNameToVerify``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html#cfn-apigatewayv2-integration-tlsconfig-servernametoverify
            """
            result = self._values.get("server_name_to_verify")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "integration_type": "integrationType",
        "connection_id": "connectionId",
        "connection_type": "connectionType",
        "content_handling_strategy": "contentHandlingStrategy",
        "credentials_arn": "credentialsArn",
        "description": "description",
        "integration_method": "integrationMethod",
        "integration_subtype": "integrationSubtype",
        "integration_uri": "integrationUri",
        "passthrough_behavior": "passthroughBehavior",
        "payload_format_version": "payloadFormatVersion",
        "request_parameters": "requestParameters",
        "request_templates": "requestTemplates",
        "template_selection_expression": "templateSelectionExpression",
        "timeout_in_millis": "timeoutInMillis",
        "tls_config": "tlsConfig",
    },
)
class CfnIntegrationProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        integration_type: builtins.str,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[builtins.str] = None,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        credentials_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        integration_method: typing.Optional[builtins.str] = None,
        integration_subtype: typing.Optional[builtins.str] = None,
        integration_uri: typing.Optional[builtins.str] = None,
        passthrough_behavior: typing.Optional[builtins.str] = None,
        payload_format_version: typing.Optional[builtins.str] = None,
        request_parameters: typing.Any = None,
        request_templates: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
        timeout_in_millis: typing.Optional[jsii.Number] = None,
        tls_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIntegration.TlsConfigProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Integration``.

        :param api_id: ``AWS::ApiGatewayV2::Integration.ApiId``.
        :param integration_type: ``AWS::ApiGatewayV2::Integration.IntegrationType``.
        :param connection_id: ``AWS::ApiGatewayV2::Integration.ConnectionId``.
        :param connection_type: ``AWS::ApiGatewayV2::Integration.ConnectionType``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Integration.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Integration.Description``.
        :param integration_method: ``AWS::ApiGatewayV2::Integration.IntegrationMethod``.
        :param integration_subtype: ``AWS::ApiGatewayV2::Integration.IntegrationSubtype``.
        :param integration_uri: ``AWS::ApiGatewayV2::Integration.IntegrationUri``.
        :param passthrough_behavior: ``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.
        :param payload_format_version: ``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.
        :param request_parameters: ``AWS::ApiGatewayV2::Integration.RequestParameters``.
        :param request_templates: ``AWS::ApiGatewayV2::Integration.RequestTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.
        :param timeout_in_millis: ``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.
        :param tls_config: ``AWS::ApiGatewayV2::Integration.TlsConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "integration_type": integration_type,
        }
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if content_handling_strategy is not None:
            self._values["content_handling_strategy"] = content_handling_strategy
        if credentials_arn is not None:
            self._values["credentials_arn"] = credentials_arn
        if description is not None:
            self._values["description"] = description
        if integration_method is not None:
            self._values["integration_method"] = integration_method
        if integration_subtype is not None:
            self._values["integration_subtype"] = integration_subtype
        if integration_uri is not None:
            self._values["integration_uri"] = integration_uri
        if passthrough_behavior is not None:
            self._values["passthrough_behavior"] = passthrough_behavior
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version
        if request_parameters is not None:
            self._values["request_parameters"] = request_parameters
        if request_templates is not None:
            self._values["request_templates"] = request_templates
        if template_selection_expression is not None:
            self._values["template_selection_expression"] = template_selection_expression
        if timeout_in_millis is not None:
            self._values["timeout_in_millis"] = timeout_in_millis
        if tls_config is not None:
            self._values["tls_config"] = tls_config

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Integration.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def integration_type(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Integration.IntegrationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        """
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return result

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectionid
        """
        result = self._values.get("connection_id")
        return result

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        """
        result = self._values.get("connection_type")
        return result

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        """
        result = self._values.get("content_handling_strategy")
        return result

    @builtins.property
    def credentials_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.CredentialsArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        """
        result = self._values.get("credentials_arn")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def integration_method(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        """
        result = self._values.get("integration_method")
        return result

    @builtins.property
    def integration_subtype(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationSubtype``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationsubtype
        """
        result = self._values.get("integration_subtype")
        return result

    @builtins.property
    def integration_uri(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationUri``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        """
        result = self._values.get("integration_uri")
        return result

    @builtins.property
    def passthrough_behavior(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        """
        result = self._values.get("passthrough_behavior")
        return result

    @builtins.property
    def payload_format_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        """
        result = self._values.get("payload_format_version")
        return result

    @builtins.property
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        """
        result = self._values.get("request_parameters")
        return result

    @builtins.property
    def request_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestTemplates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        """
        result = self._values.get("request_templates")
        return result

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        """
        result = self._values.get("template_selection_expression")
        return result

    @builtins.property
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        """
        result = self._values.get("timeout_in_millis")
        return result

    @builtins.property
    def tls_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIntegration.TlsConfigProperty]]:
        """``AWS::ApiGatewayV2::Integration.TlsConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-tlsconfig
        """
        result = self._values.get("tls_config")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegrationResponse(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationResponse",
):
    """A CloudFormation ``AWS::ApiGatewayV2::IntegrationResponse``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
    :cloudformationResource: AWS::ApiGatewayV2::IntegrationResponse
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        integration_id: builtins.str,
        integration_response_key: builtins.str,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        response_parameters: typing.Any = None,
        response_templates: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::IntegrationResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.
        :param integration_id: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.
        :param integration_response_key: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.
        :param response_parameters: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.
        """
        props = CfnIntegrationResponseProps(
            api_id=api_id,
            integration_id=integration_id,
            integration_response_key=integration_response_key,
            content_handling_strategy=content_handling_strategy,
            response_parameters=response_parameters,
            response_templates=response_templates,
            template_selection_expression=template_selection_expression,
        )

        jsii.create(CfnIntegrationResponse, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        """
        return jsii.get(self, "integrationId")

    @integration_id.setter # type: ignore
    def integration_id(self, value: builtins.str) -> None:
        jsii.set(self, "integrationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationResponseKey")
    def integration_response_key(self) -> builtins.str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        """
        return jsii.get(self, "integrationResponseKey")

    @integration_response_key.setter # type: ignore
    def integration_response_key(self, value: builtins.str) -> None:
        jsii.set(self, "integrationResponseKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        """
        return jsii.get(self, "responseParameters")

    @response_parameters.setter # type: ignore
    def response_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "responseParameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="responseTemplates")
    def response_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        """
        return jsii.get(self, "responseTemplates")

    @response_templates.setter # type: ignore
    def response_templates(self, value: typing.Any) -> None:
        jsii.set(self, "responseTemplates", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        """
        return jsii.get(self, "contentHandlingStrategy")

    @content_handling_strategy.setter # type: ignore
    def content_handling_strategy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        """
        return jsii.get(self, "templateSelectionExpression")

    @template_selection_expression.setter # type: ignore
    def template_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "templateSelectionExpression", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationResponseProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "integration_id": "integrationId",
        "integration_response_key": "integrationResponseKey",
        "content_handling_strategy": "contentHandlingStrategy",
        "response_parameters": "responseParameters",
        "response_templates": "responseTemplates",
        "template_selection_expression": "templateSelectionExpression",
    },
)
class CfnIntegrationResponseProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        integration_id: builtins.str,
        integration_response_key: builtins.str,
        content_handling_strategy: typing.Optional[builtins.str] = None,
        response_parameters: typing.Any = None,
        response_templates: typing.Any = None,
        template_selection_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::IntegrationResponse``.

        :param api_id: ``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.
        :param integration_id: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.
        :param integration_response_key: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.
        :param response_parameters: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "integration_id": integration_id,
            "integration_response_key": integration_response_key,
        }
        if content_handling_strategy is not None:
            self._values["content_handling_strategy"] = content_handling_strategy
        if response_parameters is not None:
            self._values["response_parameters"] = response_parameters
        if response_templates is not None:
            self._values["response_templates"] = response_templates
        if template_selection_expression is not None:
            self._values["template_selection_expression"] = template_selection_expression

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def integration_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        """
        result = self._values.get("integration_id")
        assert result is not None, "Required property 'integration_id' is missing"
        return result

    @builtins.property
    def integration_response_key(self) -> builtins.str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        """
        result = self._values.get("integration_response_key")
        assert result is not None, "Required property 'integration_response_key' is missing"
        return result

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        """
        result = self._values.get("content_handling_strategy")
        return result

    @builtins.property
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        """
        result = self._values.get("response_parameters")
        return result

    @builtins.property
    def response_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        """
        result = self._values.get("response_templates")
        return result

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        """
        result = self._values.get("template_selection_expression")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationResponseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModel(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnModel",
):
    """A CloudFormation ``AWS::ApiGatewayV2::Model``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
    :cloudformationResource: AWS::ApiGatewayV2::Model
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        name: builtins.str,
        schema: typing.Any,
        content_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::Model``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Model.ApiId``.
        :param name: ``AWS::ApiGatewayV2::Model.Name``.
        :param schema: ``AWS::ApiGatewayV2::Model.Schema``.
        :param content_type: ``AWS::ApiGatewayV2::Model.ContentType``.
        :param description: ``AWS::ApiGatewayV2::Model.Description``.
        """
        props = CfnModelProps(
            api_id=api_id,
            name=name,
            schema=schema,
            content_type=content_type,
            description=description,
        )

        jsii.create(CfnModel, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Model.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Model.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Model.Schema``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        """
        return jsii.get(self, "schema")

    @schema.setter # type: ignore
    def schema(self, value: typing.Any) -> None:
        jsii.set(self, "schema", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Model.ContentType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        """
        return jsii.get(self, "contentType")

    @content_type.setter # type: ignore
    def content_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "contentType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Model.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "name": "name",
        "schema": "schema",
        "content_type": "contentType",
        "description": "description",
    },
)
class CfnModelProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        name: builtins.str,
        schema: typing.Any,
        content_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Model``.

        :param api_id: ``AWS::ApiGatewayV2::Model.ApiId``.
        :param name: ``AWS::ApiGatewayV2::Model.Name``.
        :param schema: ``AWS::ApiGatewayV2::Model.Schema``.
        :param content_type: ``AWS::ApiGatewayV2::Model.ContentType``.
        :param description: ``AWS::ApiGatewayV2::Model.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "name": name,
            "schema": schema,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Model.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Model.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def schema(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Model.Schema``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        """
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return result

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Model.ContentType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        """
        result = self._values.get("content_type")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Model.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        """
        result = self._values.get("description")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRoute(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRoute",
):
    """A CloudFormation ``AWS::ApiGatewayV2::Route``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
    :cloudformationResource: AWS::ApiGatewayV2::Route
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        route_key: builtins.str,
        api_key_required: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        authorization_scopes: typing.Optional[typing.List[builtins.str]] = None,
        authorization_type: typing.Optional[builtins.str] = None,
        authorizer_id: typing.Optional[builtins.str] = None,
        model_selection_expression: typing.Optional[builtins.str] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Any = None,
        request_parameters: typing.Any = None,
        route_response_selection_expression: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Route.ApiId``.
        :param route_key: ``AWS::ApiGatewayV2::Route.RouteKey``.
        :param api_key_required: ``AWS::ApiGatewayV2::Route.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGatewayV2::Route.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGatewayV2::Route.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGatewayV2::Route.AuthorizerId``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.
        :param operation_name: ``AWS::ApiGatewayV2::Route.OperationName``.
        :param request_models: ``AWS::ApiGatewayV2::Route.RequestModels``.
        :param request_parameters: ``AWS::ApiGatewayV2::Route.RequestParameters``.
        :param route_response_selection_expression: ``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.
        :param target: ``AWS::ApiGatewayV2::Route.Target``.
        """
        props = CfnRouteProps(
            api_id=api_id,
            route_key=route_key,
            api_key_required=api_key_required,
            authorization_scopes=authorization_scopes,
            authorization_type=authorization_type,
            authorizer_id=authorizer_id,
            model_selection_expression=model_selection_expression,
            operation_name=operation_name,
            request_models=request_models,
            request_parameters=request_parameters,
            route_response_selection_expression=route_response_selection_expression,
            target=target,
        )

        jsii.create(CfnRoute, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Route.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="requestModels")
    def request_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestModels``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        """
        return jsii.get(self, "requestModels")

    @request_models.setter # type: ignore
    def request_models(self, value: typing.Any) -> None:
        jsii.set(self, "requestModels", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        """
        return jsii.get(self, "requestParameters")

    @request_parameters.setter # type: ignore
    def request_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "requestParameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Route.RouteKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        """
        return jsii.get(self, "routeKey")

    @route_key.setter # type: ignore
    def route_key(self, value: builtins.str) -> None:
        jsii.set(self, "routeKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiKeyRequired")
    def api_key_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Route.ApiKeyRequired``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        """
        return jsii.get(self, "apiKeyRequired")

    @api_key_required.setter # type: ignore
    def api_key_required(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "apiKeyRequired", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizationScopes")
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ApiGatewayV2::Route.AuthorizationScopes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        """
        return jsii.get(self, "authorizationScopes")

    @authorization_scopes.setter # type: ignore
    def authorization_scopes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "authorizationScopes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.AuthorizationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        """
        return jsii.get(self, "authorizationType")

    @authorization_type.setter # type: ignore
    def authorization_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authorizationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.AuthorizerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        """
        return jsii.get(self, "authorizerId")

    @authorizer_id.setter # type: ignore
    def authorizer_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authorizerId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        """
        return jsii.get(self, "modelSelectionExpression")

    @model_selection_expression.setter # type: ignore
    def model_selection_expression(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "modelSelectionExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.OperationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        """
        return jsii.get(self, "operationName")

    @operation_name.setter # type: ignore
    def operation_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "operationName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeResponseSelectionExpression")
    def route_response_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        """
        return jsii.get(self, "routeResponseSelectionExpression")

    @route_response_selection_expression.setter # type: ignore
    def route_response_selection_expression(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "routeResponseSelectionExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.Target``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        """
        return jsii.get(self, "target")

    @target.setter # type: ignore
    def target(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "target", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnRoute.ParameterConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"required": "required"},
    )
    class ParameterConstraintsProperty:
        def __init__(
            self,
            *,
            required: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        ) -> None:
            """
            :param required: ``CfnRoute.ParameterConstraintsProperty.Required``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "required": required,
            }

        @builtins.property
        def required(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnRoute.ParameterConstraintsProperty.Required``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html#cfn-apigatewayv2-route-parameterconstraints-required
            """
            result = self._values.get("required")
            assert result is not None, "Required property 'required' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "route_key": "routeKey",
        "api_key_required": "apiKeyRequired",
        "authorization_scopes": "authorizationScopes",
        "authorization_type": "authorizationType",
        "authorizer_id": "authorizerId",
        "model_selection_expression": "modelSelectionExpression",
        "operation_name": "operationName",
        "request_models": "requestModels",
        "request_parameters": "requestParameters",
        "route_response_selection_expression": "routeResponseSelectionExpression",
        "target": "target",
    },
)
class CfnRouteProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        route_key: builtins.str,
        api_key_required: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        authorization_scopes: typing.Optional[typing.List[builtins.str]] = None,
        authorization_type: typing.Optional[builtins.str] = None,
        authorizer_id: typing.Optional[builtins.str] = None,
        model_selection_expression: typing.Optional[builtins.str] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Any = None,
        request_parameters: typing.Any = None,
        route_response_selection_expression: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Route``.

        :param api_id: ``AWS::ApiGatewayV2::Route.ApiId``.
        :param route_key: ``AWS::ApiGatewayV2::Route.RouteKey``.
        :param api_key_required: ``AWS::ApiGatewayV2::Route.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGatewayV2::Route.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGatewayV2::Route.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGatewayV2::Route.AuthorizerId``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.
        :param operation_name: ``AWS::ApiGatewayV2::Route.OperationName``.
        :param request_models: ``AWS::ApiGatewayV2::Route.RequestModels``.
        :param request_parameters: ``AWS::ApiGatewayV2::Route.RequestParameters``.
        :param route_response_selection_expression: ``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.
        :param target: ``AWS::ApiGatewayV2::Route.Target``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "route_key": route_key,
        }
        if api_key_required is not None:
            self._values["api_key_required"] = api_key_required
        if authorization_scopes is not None:
            self._values["authorization_scopes"] = authorization_scopes
        if authorization_type is not None:
            self._values["authorization_type"] = authorization_type
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if model_selection_expression is not None:
            self._values["model_selection_expression"] = model_selection_expression
        if operation_name is not None:
            self._values["operation_name"] = operation_name
        if request_models is not None:
            self._values["request_models"] = request_models
        if request_parameters is not None:
            self._values["request_parameters"] = request_parameters
        if route_response_selection_expression is not None:
            self._values["route_response_selection_expression"] = route_response_selection_expression
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Route.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def route_key(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Route.RouteKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        """
        result = self._values.get("route_key")
        assert result is not None, "Required property 'route_key' is missing"
        return result

    @builtins.property
    def api_key_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Route.ApiKeyRequired``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        """
        result = self._values.get("api_key_required")
        return result

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ApiGatewayV2::Route.AuthorizationScopes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        """
        result = self._values.get("authorization_scopes")
        return result

    @builtins.property
    def authorization_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.AuthorizationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        """
        result = self._values.get("authorization_type")
        return result

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.AuthorizerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        """
        result = self._values.get("authorizer_id")
        return result

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        """
        result = self._values.get("model_selection_expression")
        return result

    @builtins.property
    def operation_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.OperationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        """
        result = self._values.get("operation_name")
        return result

    @builtins.property
    def request_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestModels``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        """
        result = self._values.get("request_models")
        return result

    @builtins.property
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        """
        result = self._values.get("request_parameters")
        return result

    @builtins.property
    def route_response_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        """
        result = self._values.get("route_response_selection_expression")
        return result

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Route.Target``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        """
        result = self._values.get("target")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRouteResponse(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponse",
):
    """A CloudFormation ``AWS::ApiGatewayV2::RouteResponse``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
    :cloudformationResource: AWS::ApiGatewayV2::RouteResponse
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        route_id: builtins.str,
        route_response_key: builtins.str,
        model_selection_expression: typing.Optional[builtins.str] = None,
        response_models: typing.Any = None,
        response_parameters: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::RouteResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::RouteResponse.ApiId``.
        :param route_id: ``AWS::ApiGatewayV2::RouteResponse.RouteId``.
        :param route_response_key: ``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.
        :param response_models: ``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.
        :param response_parameters: ``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.
        """
        props = CfnRouteResponseProps(
            api_id=api_id,
            route_id=route_id,
            route_response_key=route_response_key,
            model_selection_expression=model_selection_expression,
            response_models=response_models,
            response_parameters=response_parameters,
        )

        jsii.create(CfnRouteResponse, self, [scope, id, props])

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
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::RouteResponse.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="responseModels")
    def response_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        """
        return jsii.get(self, "responseModels")

    @response_models.setter # type: ignore
    def response_models(self, value: typing.Any) -> None:
        jsii.set(self, "responseModels", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        """
        return jsii.get(self, "responseParameters")

    @response_parameters.setter # type: ignore
    def response_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "responseParameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        """
        return jsii.get(self, "routeId")

    @route_id.setter # type: ignore
    def route_id(self, value: builtins.str) -> None:
        jsii.set(self, "routeId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeResponseKey")
    def route_response_key(self) -> builtins.str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        """
        return jsii.get(self, "routeResponseKey")

    @route_response_key.setter # type: ignore
    def route_response_key(self, value: builtins.str) -> None:
        jsii.set(self, "routeResponseKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        """
        return jsii.get(self, "modelSelectionExpression")

    @model_selection_expression.setter # type: ignore
    def model_selection_expression(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "modelSelectionExpression", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponse.ParameterConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"required": "required"},
    )
    class ParameterConstraintsProperty:
        def __init__(
            self,
            *,
            required: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        ) -> None:
            """
            :param required: ``CfnRouteResponse.ParameterConstraintsProperty.Required``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "required": required,
            }

        @builtins.property
        def required(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnRouteResponse.ParameterConstraintsProperty.Required``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html#cfn-apigatewayv2-routeresponse-parameterconstraints-required
            """
            result = self._values.get("required")
            assert result is not None, "Required property 'required' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponseProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "route_id": "routeId",
        "route_response_key": "routeResponseKey",
        "model_selection_expression": "modelSelectionExpression",
        "response_models": "responseModels",
        "response_parameters": "responseParameters",
    },
)
class CfnRouteResponseProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        route_id: builtins.str,
        route_response_key: builtins.str,
        model_selection_expression: typing.Optional[builtins.str] = None,
        response_models: typing.Any = None,
        response_parameters: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::RouteResponse``.

        :param api_id: ``AWS::ApiGatewayV2::RouteResponse.ApiId``.
        :param route_id: ``AWS::ApiGatewayV2::RouteResponse.RouteId``.
        :param route_response_key: ``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.
        :param response_models: ``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.
        :param response_parameters: ``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "route_id": route_id,
            "route_response_key": route_response_key,
        }
        if model_selection_expression is not None:
            self._values["model_selection_expression"] = model_selection_expression
        if response_models is not None:
            self._values["response_models"] = response_models
        if response_parameters is not None:
            self._values["response_parameters"] = response_parameters

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::RouteResponse.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def route_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        """
        result = self._values.get("route_id")
        assert result is not None, "Required property 'route_id' is missing"
        return result

    @builtins.property
    def route_response_key(self) -> builtins.str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        """
        result = self._values.get("route_response_key")
        assert result is not None, "Required property 'route_response_key' is missing"
        return result

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        """
        result = self._values.get("model_selection_expression")
        return result

    @builtins.property
    def response_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        """
        result = self._values.get("response_models")
        return result

    @builtins.property
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        """
        result = self._values.get("response_parameters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteResponseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStage(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage",
):
    """A CloudFormation ``AWS::ApiGatewayV2::Stage``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
    :cloudformationResource: AWS::ApiGatewayV2::Stage
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_id: builtins.str,
        stage_name: builtins.str,
        access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]] = None,
        auto_deploy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        client_certificate_id: typing.Optional[builtins.str] = None,
        default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        route_settings: typing.Any = None,
        stage_variables: typing.Any = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::Stage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Stage.ApiId``.
        :param stage_name: ``AWS::ApiGatewayV2::Stage.StageName``.
        :param access_log_settings: ``AWS::ApiGatewayV2::Stage.AccessLogSettings``.
        :param auto_deploy: ``AWS::ApiGatewayV2::Stage.AutoDeploy``.
        :param client_certificate_id: ``AWS::ApiGatewayV2::Stage.ClientCertificateId``.
        :param default_route_settings: ``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.
        :param deployment_id: ``AWS::ApiGatewayV2::Stage.DeploymentId``.
        :param description: ``AWS::ApiGatewayV2::Stage.Description``.
        :param route_settings: ``AWS::ApiGatewayV2::Stage.RouteSettings``.
        :param stage_variables: ``AWS::ApiGatewayV2::Stage.StageVariables``.
        :param tags: ``AWS::ApiGatewayV2::Stage.Tags``.
        """
        props = CfnStageProps(
            api_id=api_id,
            stage_name=stage_name,
            access_log_settings=access_log_settings,
            auto_deploy=auto_deploy,
            client_certificate_id=client_certificate_id,
            default_route_settings=default_route_settings,
            deployment_id=deployment_id,
            description=description,
            route_settings=route_settings,
            stage_variables=stage_variables,
            tags=tags,
        )

        jsii.create(CfnStage, self, [scope, id, props])

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
        """``AWS::ApiGatewayV2::Stage.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Stage.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter # type: ignore
    def api_id(self, value: builtins.str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeSettings")
    def route_settings(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.RouteSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        """
        return jsii.get(self, "routeSettings")

    @route_settings.setter # type: ignore
    def route_settings(self, value: typing.Any) -> None:
        jsii.set(self, "routeSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Stage.StageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        """
        return jsii.get(self, "stageName")

    @stage_name.setter # type: ignore
    def stage_name(self, value: builtins.str) -> None:
        jsii.set(self, "stageName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageVariables")
    def stage_variables(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.StageVariables``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        """
        return jsii.get(self, "stageVariables")

    @stage_variables.setter # type: ignore
    def stage_variables(self, value: typing.Any) -> None:
        jsii.set(self, "stageVariables", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accessLogSettings")
    def access_log_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]]:
        """``AWS::ApiGatewayV2::Stage.AccessLogSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        """
        return jsii.get(self, "accessLogSettings")

    @access_log_settings.setter # type: ignore
    def access_log_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]],
    ) -> None:
        jsii.set(self, "accessLogSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoDeploy")
    def auto_deploy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Stage.AutoDeploy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        """
        return jsii.get(self, "autoDeploy")

    @auto_deploy.setter # type: ignore
    def auto_deploy(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "autoDeploy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clientCertificateId")
    def client_certificate_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Stage.ClientCertificateId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        """
        return jsii.get(self, "clientCertificateId")

    @client_certificate_id.setter # type: ignore
    def client_certificate_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientCertificateId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultRouteSettings")
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]]:
        """``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        """
        return jsii.get(self, "defaultRouteSettings")

    @default_route_settings.setter # type: ignore
    def default_route_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]],
    ) -> None:
        jsii.set(self, "defaultRouteSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Stage.DeploymentId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        """
        return jsii.get(self, "deploymentId")

    @deployment_id.setter # type: ignore
    def deployment_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "deploymentId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Stage.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage.AccessLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingsProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param destination_arn: ``CfnStage.AccessLogSettingsProperty.DestinationArn``.
            :param format: ``CfnStage.AccessLogSettingsProperty.Format``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            """``CfnStage.AccessLogSettingsProperty.DestinationArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-destinationarn
            """
            result = self._values.get("destination_arn")
            return result

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            """``CfnStage.AccessLogSettingsProperty.Format``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-format
            """
            result = self._values.get("format")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage.RouteSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_trace_enabled": "dataTraceEnabled",
            "detailed_metrics_enabled": "detailedMetricsEnabled",
            "logging_level": "loggingLevel",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class RouteSettingsProperty:
        def __init__(
            self,
            *,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            detailed_metrics_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            logging_level: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param data_trace_enabled: ``CfnStage.RouteSettingsProperty.DataTraceEnabled``.
            :param detailed_metrics_enabled: ``CfnStage.RouteSettingsProperty.DetailedMetricsEnabled``.
            :param logging_level: ``CfnStage.RouteSettingsProperty.LoggingLevel``.
            :param throttling_burst_limit: ``CfnStage.RouteSettingsProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnStage.RouteSettingsProperty.ThrottlingRateLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None:
                self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnStage.RouteSettingsProperty.DataTraceEnabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-datatraceenabled
            """
            result = self._values.get("data_trace_enabled")
            return result

        @builtins.property
        def detailed_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnStage.RouteSettingsProperty.DetailedMetricsEnabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-detailedmetricsenabled
            """
            result = self._values.get("detailed_metrics_enabled")
            return result

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            """``CfnStage.RouteSettingsProperty.LoggingLevel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-logginglevel
            """
            result = self._values.get("logging_level")
            return result

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.RouteSettingsProperty.ThrottlingBurstLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingburstlimit
            """
            result = self._values.get("throttling_burst_limit")
            return result

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.RouteSettingsProperty.ThrottlingRateLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingratelimit
            """
            result = self._values.get("throttling_rate_limit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RouteSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnStageProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "stage_name": "stageName",
        "access_log_settings": "accessLogSettings",
        "auto_deploy": "autoDeploy",
        "client_certificate_id": "clientCertificateId",
        "default_route_settings": "defaultRouteSettings",
        "deployment_id": "deploymentId",
        "description": "description",
        "route_settings": "routeSettings",
        "stage_variables": "stageVariables",
        "tags": "tags",
    },
)
class CfnStageProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        stage_name: builtins.str,
        access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.AccessLogSettingsProperty]] = None,
        auto_deploy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        client_certificate_id: typing.Optional[builtins.str] = None,
        default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.RouteSettingsProperty]] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        route_settings: typing.Any = None,
        stage_variables: typing.Any = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Stage``.

        :param api_id: ``AWS::ApiGatewayV2::Stage.ApiId``.
        :param stage_name: ``AWS::ApiGatewayV2::Stage.StageName``.
        :param access_log_settings: ``AWS::ApiGatewayV2::Stage.AccessLogSettings``.
        :param auto_deploy: ``AWS::ApiGatewayV2::Stage.AutoDeploy``.
        :param client_certificate_id: ``AWS::ApiGatewayV2::Stage.ClientCertificateId``.
        :param default_route_settings: ``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.
        :param deployment_id: ``AWS::ApiGatewayV2::Stage.DeploymentId``.
        :param description: ``AWS::ApiGatewayV2::Stage.Description``.
        :param route_settings: ``AWS::ApiGatewayV2::Stage.RouteSettings``.
        :param stage_variables: ``AWS::ApiGatewayV2::Stage.StageVariables``.
        :param tags: ``AWS::ApiGatewayV2::Stage.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_id": api_id,
            "stage_name": stage_name,
        }
        if access_log_settings is not None:
            self._values["access_log_settings"] = access_log_settings
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if client_certificate_id is not None:
            self._values["client_certificate_id"] = client_certificate_id
        if default_route_settings is not None:
            self._values["default_route_settings"] = default_route_settings
        if deployment_id is not None:
            self._values["deployment_id"] = deployment_id
        if description is not None:
            self._values["description"] = description
        if route_settings is not None:
            self._values["route_settings"] = route_settings
        if stage_variables is not None:
            self._values["stage_variables"] = stage_variables
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def api_id(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Stage.ApiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        """
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return result

    @builtins.property
    def stage_name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::Stage.StageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        """
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return result

    @builtins.property
    def access_log_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.AccessLogSettingsProperty]]:
        """``AWS::ApiGatewayV2::Stage.AccessLogSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        """
        result = self._values.get("access_log_settings")
        return result

    @builtins.property
    def auto_deploy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Stage.AutoDeploy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        """
        result = self._values.get("auto_deploy")
        return result

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Stage.ClientCertificateId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        """
        result = self._values.get("client_certificate_id")
        return result

    @builtins.property
    def default_route_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStage.RouteSettingsProperty]]:
        """``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        """
        result = self._values.get("default_route_settings")
        return result

    @builtins.property
    def deployment_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Stage.DeploymentId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        """
        result = self._values.get("deployment_id")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ApiGatewayV2::Stage.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def route_settings(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.RouteSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        """
        result = self._values.get("route_settings")
        return result

    @builtins.property
    def stage_variables(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.StageVariables``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        """
        result = self._values.get("stage_variables")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVpcLink(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnVpcLink",
):
    """A CloudFormation ``AWS::ApiGatewayV2::VpcLink``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html
    :cloudformationResource: AWS::ApiGatewayV2::VpcLink
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        subnet_ids: typing.List[builtins.str],
        security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::ApiGatewayV2::VpcLink``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::ApiGatewayV2::VpcLink.Name``.
        :param subnet_ids: ``AWS::ApiGatewayV2::VpcLink.SubnetIds``.
        :param security_group_ids: ``AWS::ApiGatewayV2::VpcLink.SecurityGroupIds``.
        :param tags: ``AWS::ApiGatewayV2::VpcLink.Tags``.
        """
        props = CfnVpcLinkProps(
            name=name,
            subnet_ids=subnet_ids,
            security_group_ids=security_group_ids,
            tags=tags,
        )

        jsii.create(CfnVpcLink, self, [scope, id, props])

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
        """``AWS::ApiGatewayV2::VpcLink.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::VpcLink.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::ApiGatewayV2::VpcLink.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter # type: ignore
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ApiGatewayV2::VpcLink.SecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter # type: ignore
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroupIds", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CfnVpcLinkProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "subnet_ids": "subnetIds",
        "security_group_ids": "securityGroupIds",
        "tags": "tags",
    },
)
class CfnVpcLinkProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        subnet_ids: typing.List[builtins.str],
        security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::VpcLink``.

        :param name: ``AWS::ApiGatewayV2::VpcLink.Name``.
        :param subnet_ids: ``AWS::ApiGatewayV2::VpcLink.SubnetIds``.
        :param security_group_ids: ``AWS::ApiGatewayV2::VpcLink.SecurityGroupIds``.
        :param tags: ``AWS::ApiGatewayV2::VpcLink.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "subnet_ids": subnet_ids,
        }
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::ApiGatewayV2::VpcLink.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::ApiGatewayV2::VpcLink.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-subnetids
        """
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return result

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ApiGatewayV2::VpcLink.SecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-securitygroupids
        """
        result = self._values.get("security_group_ids")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::VpcLink.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-vpclink.html#cfn-apigatewayv2-vpclink-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcLinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CommonStageOptions",
    jsii_struct_bases=[],
    name_mapping={"auto_deploy": "autoDeploy", "stage_name": "stageName"},
)
class CommonStageOptions:
    def __init__(
        self,
        *,
        auto_deploy: typing.Optional[builtins.bool] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Options required to create a new stage.

        Options that are common between HTTP and Websocket APIs.

        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def auto_deploy(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether updates to an API automatically trigger a new deployment.

        :default: false

        :stability: experimental
        """
        result = self._values.get("auto_deploy")
        return result

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the stage.

        See ``StageName`` class for more details.

        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        """
        result = self._values.get("stage_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.CorsPreflightOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allow_credentials": "allowCredentials",
        "allow_headers": "allowHeaders",
        "allow_methods": "allowMethods",
        "allow_origins": "allowOrigins",
        "expose_headers": "exposeHeaders",
        "max_age": "maxAge",
    },
)
class CorsPreflightOptions:
    def __init__(
        self,
        *,
        allow_credentials: typing.Optional[builtins.bool] = None,
        allow_headers: typing.Optional[typing.List[builtins.str]] = None,
        allow_methods: typing.Optional[typing.List["HttpMethod"]] = None,
        allow_origins: typing.Optional[typing.List[builtins.str]] = None,
        expose_headers: typing.Optional[typing.List[builtins.str]] = None,
        max_age: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(experimental) Options for the CORS Configuration.

        :param allow_credentials: (experimental) Specifies whether credentials are included in the CORS request. Default: false
        :param allow_headers: (experimental) Represents a collection of allowed headers. Default: - No Headers are allowed.
        :param allow_methods: (experimental) Represents a collection of allowed HTTP methods. Default: - No Methods are allowed.
        :param allow_origins: (experimental) Represents a collection of allowed origins. Default: - No Origins are allowed.
        :param expose_headers: (experimental) Represents a collection of exposed headers. Default: - No Expose Headers are allowed.
        :param max_age: (experimental) The duration that the browser should cache preflight request results. Default: Duration.seconds(0)

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_credentials is not None:
            self._values["allow_credentials"] = allow_credentials
        if allow_headers is not None:
            self._values["allow_headers"] = allow_headers
        if allow_methods is not None:
            self._values["allow_methods"] = allow_methods
        if allow_origins is not None:
            self._values["allow_origins"] = allow_origins
        if expose_headers is not None:
            self._values["expose_headers"] = expose_headers
        if max_age is not None:
            self._values["max_age"] = max_age

    @builtins.property
    def allow_credentials(self) -> typing.Optional[builtins.bool]:
        """(experimental) Specifies whether credentials are included in the CORS request.

        :default: false

        :stability: experimental
        """
        result = self._values.get("allow_credentials")
        return result

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Represents a collection of allowed headers.

        :default: - No Headers are allowed.

        :stability: experimental
        """
        result = self._values.get("allow_headers")
        return result

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List["HttpMethod"]]:
        """(experimental) Represents a collection of allowed HTTP methods.

        :default: - No Methods are allowed.

        :stability: experimental
        """
        result = self._values.get("allow_methods")
        return result

    @builtins.property
    def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Represents a collection of allowed origins.

        :default: - No Origins are allowed.

        :stability: experimental
        """
        result = self._values.get("allow_origins")
        return result

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Represents a collection of exposed headers.

        :default: - No Expose Headers are allowed.

        :stability: experimental
        """
        result = self._values.get("expose_headers")
        return result

    @builtins.property
    def max_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The duration that the browser should cache preflight request results.

        :default: Duration.seconds(0)

        :stability: experimental
        """
        result = self._values.get("max_age")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CorsPreflightOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.DefaultDomainMappingOptions",
    jsii_struct_bases=[],
    name_mapping={"domain_name": "domainName", "mapping_key": "mappingKey"},
)
class DefaultDomainMappingOptions:
    def __init__(
        self,
        *,
        domain_name: "IDomainName",
        mapping_key: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Options for defaultDomainMapping.

        :param domain_name: (experimental) The domain name for the mapping.
        :param mapping_key: (experimental) The API mapping key. Leave it undefined for the root path mapping. Default: - empty key for the root path mapping

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if mapping_key is not None:
            self._values["mapping_key"] = mapping_key

    @builtins.property
    def domain_name(self) -> "IDomainName":
        """(experimental) The domain name for the mapping.

        :stability: experimental
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def mapping_key(self) -> typing.Optional[builtins.str]:
        """(experimental) The API mapping key.

        Leave it undefined for the root path mapping.

        :default: - empty key for the root path mapping

        :stability: experimental
        """
        result = self._values.get("mapping_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultDomainMappingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainMappingOptions",
    jsii_struct_bases=[DefaultDomainMappingOptions],
    name_mapping={
        "domain_name": "domainName",
        "mapping_key": "mappingKey",
        "stage": "stage",
    },
)
class DomainMappingOptions(DefaultDomainMappingOptions):
    def __init__(
        self,
        *,
        domain_name: "IDomainName",
        mapping_key: typing.Optional[builtins.str] = None,
        stage: typing.Optional["IStage"] = None,
    ) -> None:
        """(experimental) Options for DomainMapping.

        :param domain_name: (experimental) The domain name for the mapping.
        :param mapping_key: (experimental) The API mapping key. Leave it undefined for the root path mapping. Default: - empty key for the root path mapping
        :param stage: (experimental) The API Stage. Default: - the $default stage

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if mapping_key is not None:
            self._values["mapping_key"] = mapping_key
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def domain_name(self) -> "IDomainName":
        """(experimental) The domain name for the mapping.

        :stability: experimental
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def mapping_key(self) -> typing.Optional[builtins.str]:
        """(experimental) The API mapping key.

        Leave it undefined for the root path mapping.

        :default: - empty key for the root path mapping

        :stability: experimental
        """
        result = self._values.get("mapping_key")
        return result

    @builtins.property
    def stage(self) -> typing.Optional["IStage"]:
        """(experimental) The API Stage.

        :default: - the $default stage

        :stability: experimental
        """
        result = self._values.get("stage")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainMappingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainNameAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "regional_domain_name": "regionalDomainName",
        "regional_hosted_zone_id": "regionalHostedZoneId",
    },
)
class DomainNameAttributes:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        regional_domain_name: builtins.str,
        regional_hosted_zone_id: builtins.str,
    ) -> None:
        """(experimental) custom domain name attributes.

        :param domain_name: (experimental) domain name string.
        :param regional_domain_name: (experimental) The domain name associated with the regional endpoint for this custom domain name.
        :param regional_hosted_zone_id: (experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
            "regional_domain_name": regional_domain_name,
            "regional_hosted_zone_id": regional_hosted_zone_id,
        }

    @builtins.property
    def domain_name(self) -> builtins.str:
        """(experimental) domain name string.

        :stability: experimental
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def regional_domain_name(self) -> builtins.str:
        """(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        """
        result = self._values.get("regional_domain_name")
        assert result is not None, "Required property 'regional_domain_name' is missing"
        return result

    @builtins.property
    def regional_hosted_zone_id(self) -> builtins.str:
        """(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        """
        result = self._values.get("regional_hosted_zone_id")
        assert result is not None, "Required property 'regional_hosted_zone_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainNameAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainNameProps",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "domain_name": "domainName"},
)
class DomainNameProps:
    def __init__(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        domain_name: builtins.str,
    ) -> None:
        """(experimental) properties used for creating the DomainName.

        :param certificate: (experimental) The ACM certificate for this domain name.
        :param domain_name: (experimental) The custom domain name.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "domain_name": domain_name,
        }

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        """(experimental) The ACM certificate for this domain name.

        :stability: experimental
        """
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return result

    @builtins.property
    def domain_name(self) -> builtins.str:
        """(experimental) The custom domain name.

        :stability: experimental
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApiMappingAttributes",
    jsii_struct_bases=[],
    name_mapping={"api_mapping_id": "apiMappingId"},
)
class HttpApiMappingAttributes:
    def __init__(self, *, api_mapping_id: builtins.str) -> None:
        """(experimental) The attributes used to import existing HttpApiMapping.

        :param api_mapping_id: (experimental) The API mapping ID.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_mapping_id": api_mapping_id,
        }

    @builtins.property
    def api_mapping_id(self) -> builtins.str:
        """(experimental) The API mapping ID.

        :stability: experimental
        """
        result = self._values.get("api_mapping_id")
        assert result is not None, "Required property 'api_mapping_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpApiMappingAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApiMappingProps",
    jsii_struct_bases=[],
    name_mapping={
        "api": "api",
        "domain_name": "domainName",
        "api_mapping_key": "apiMappingKey",
        "stage": "stage",
    },
)
class HttpApiMappingProps:
    def __init__(
        self,
        *,
        api: "IHttpApi",
        domain_name: "IDomainName",
        api_mapping_key: typing.Optional[builtins.str] = None,
        stage: typing.Optional["IHttpStage"] = None,
    ) -> None:
        """(experimental) Properties used to create the HttpApiMapping resource.

        :param api: (experimental) The HttpApi to which this mapping is applied.
        :param domain_name: (experimental) custom domain name of the mapping target.
        :param api_mapping_key: (experimental) Api mapping key. The path where this stage should be mapped to on the domain Default: - undefined for the root path mapping.
        :param stage: (experimental) stage for the HttpApiMapping resource. Default: - the $default stage

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api": api,
            "domain_name": domain_name,
        }
        if api_mapping_key is not None:
            self._values["api_mapping_key"] = api_mapping_key
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def api(self) -> "IHttpApi":
        """(experimental) The HttpApi to which this mapping is applied.

        :stability: experimental
        """
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return result

    @builtins.property
    def domain_name(self) -> "IDomainName":
        """(experimental) custom domain name of the mapping target.

        :stability: experimental
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def api_mapping_key(self) -> typing.Optional[builtins.str]:
        """(experimental) Api mapping key.

        The path where this stage should be mapped to on the domain

        :default: - undefined for the root path mapping.

        :stability: experimental
        """
        result = self._values.get("api_mapping_key")
        return result

    @builtins.property
    def stage(self) -> typing.Optional["IHttpStage"]:
        """(experimental) stage for the HttpApiMapping resource.

        :default: - the $default stage

        :stability: experimental
        """
        result = self._values.get("stage")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpApiMappingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_name": "apiName",
        "cors_preflight": "corsPreflight",
        "create_default_stage": "createDefaultStage",
        "default_domain_mapping": "defaultDomainMapping",
        "default_integration": "defaultIntegration",
        "description": "description",
    },
)
class HttpApiProps:
    def __init__(
        self,
        *,
        api_name: typing.Optional[builtins.str] = None,
        cors_preflight: typing.Optional[CorsPreflightOptions] = None,
        create_default_stage: typing.Optional[builtins.bool] = None,
        default_domain_mapping: typing.Optional[DefaultDomainMappingOptions] = None,
        default_integration: typing.Optional["IHttpRouteIntegration"] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties to initialize an instance of ``HttpApi``.

        :param api_name: (experimental) Name for the HTTP API resoruce. Default: - id of the HttpApi construct.
        :param cors_preflight: (experimental) Specifies a CORS configuration for an API. Default: - CORS disabled.
        :param create_default_stage: (experimental) Whether a default stage and deployment should be automatically created. Default: true
        :param default_domain_mapping: (experimental) Configure a custom domain with the API mapping resource to the HTTP API. Default: - no default domain mapping configured. meaningless if ``createDefaultStage`` is ``false``.
        :param default_integration: (experimental) An integration that will be configured on the catch-all route ($default). Default: - none
        :param description: (experimental) The description of the API. Default: - none

        :stability: experimental
        """
        if isinstance(cors_preflight, dict):
            cors_preflight = CorsPreflightOptions(**cors_preflight)
        if isinstance(default_domain_mapping, dict):
            default_domain_mapping = DefaultDomainMappingOptions(**default_domain_mapping)
        self._values: typing.Dict[str, typing.Any] = {}
        if api_name is not None:
            self._values["api_name"] = api_name
        if cors_preflight is not None:
            self._values["cors_preflight"] = cors_preflight
        if create_default_stage is not None:
            self._values["create_default_stage"] = create_default_stage
        if default_domain_mapping is not None:
            self._values["default_domain_mapping"] = default_domain_mapping
        if default_integration is not None:
            self._values["default_integration"] = default_integration
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def api_name(self) -> typing.Optional[builtins.str]:
        """(experimental) Name for the HTTP API resoruce.

        :default: - id of the HttpApi construct.

        :stability: experimental
        """
        result = self._values.get("api_name")
        return result

    @builtins.property
    def cors_preflight(self) -> typing.Optional[CorsPreflightOptions]:
        """(experimental) Specifies a CORS configuration for an API.

        :default: - CORS disabled.

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html
        :stability: experimental
        """
        result = self._values.get("cors_preflight")
        return result

    @builtins.property
    def create_default_stage(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether a default stage and deployment should be automatically created.

        :default: true

        :stability: experimental
        """
        result = self._values.get("create_default_stage")
        return result

    @builtins.property
    def default_domain_mapping(self) -> typing.Optional[DefaultDomainMappingOptions]:
        """(experimental) Configure a custom domain with the API mapping resource to the HTTP API.

        :default: - no default domain mapping configured. meaningless if ``createDefaultStage`` is ``false``.

        :stability: experimental
        """
        result = self._values.get("default_domain_mapping")
        return result

    @builtins.property
    def default_integration(self) -> typing.Optional["IHttpRouteIntegration"]:
        """(experimental) An integration that will be configured on the catch-all route ($default).

        :default: - none

        :stability: experimental
        """
        result = self._values.get("default_integration")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """(experimental) The description of the API.

        :default: - none

        :stability: experimental
        """
        result = self._values.get("description")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpConnectionType")
class HttpConnectionType(enum.Enum):
    """(experimental) Supported connection types.

    :stability: experimental
    """

    VPC_LINK = "VPC_LINK"
    """(experimental) For private connections between API Gateway and resources in a VPC.

    :stability: experimental
    """
    INTERNET = "INTERNET"
    """(experimental) For connections through public routable internet.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "http_api": "httpApi",
        "integration_type": "integrationType",
        "integration_uri": "integrationUri",
        "connection_id": "connectionId",
        "connection_type": "connectionType",
        "method": "method",
        "payload_format_version": "payloadFormatVersion",
    },
)
class HttpIntegrationProps:
    def __init__(
        self,
        *,
        http_api: "IHttpApi",
        integration_type: "HttpIntegrationType",
        integration_uri: builtins.str,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[HttpConnectionType] = None,
        method: typing.Optional["HttpMethod"] = None,
        payload_format_version: typing.Optional["PayloadFormatVersion"] = None,
    ) -> None:
        """(experimental) The integration properties.

        :param http_api: (experimental) The HTTP API to which this integration should be bound.
        :param integration_type: (experimental) Integration type.
        :param integration_uri: (experimental) Integration URI. This will be the function ARN in the case of ``HttpIntegrationType.LAMBDA_PROXY``, or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``.
        :param connection_id: (experimental) The ID of the VPC link for a private integration. Supported only for HTTP APIs. Default: - undefined
        :param connection_type: (experimental) The type of the network connection to the integration endpoint. Default: HttpConnectionType.INTERNET
        :param method: (experimental) The HTTP method to use when calling the underlying HTTP proxy. Default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.
        :param payload_format_version: (experimental) The version of the payload format. Default: - defaults to latest in the case of HttpIntegrationType.LAMBDA_PROXY`, irrelevant otherwise.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "http_api": http_api,
            "integration_type": integration_type,
            "integration_uri": integration_uri,
        }
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if method is not None:
            self._values["method"] = method
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version

    @builtins.property
    def http_api(self) -> "IHttpApi":
        """(experimental) The HTTP API to which this integration should be bound.

        :stability: experimental
        """
        result = self._values.get("http_api")
        assert result is not None, "Required property 'http_api' is missing"
        return result

    @builtins.property
    def integration_type(self) -> "HttpIntegrationType":
        """(experimental) Integration type.

        :stability: experimental
        """
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return result

    @builtins.property
    def integration_uri(self) -> builtins.str:
        """(experimental) Integration URI.

        This will be the function ARN in the case of ``HttpIntegrationType.LAMBDA_PROXY``,
        or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``.

        :stability: experimental
        """
        result = self._values.get("integration_uri")
        assert result is not None, "Required property 'integration_uri' is missing"
        return result

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        """(experimental) The ID of the VPC link for a private integration.

        Supported only for HTTP APIs.

        :default: - undefined

        :stability: experimental
        """
        result = self._values.get("connection_id")
        return result

    @builtins.property
    def connection_type(self) -> typing.Optional[HttpConnectionType]:
        """(experimental) The type of the network connection to the integration endpoint.

        :default: HttpConnectionType.INTERNET

        :stability: experimental
        """
        result = self._values.get("connection_type")
        return result

    @builtins.property
    def method(self) -> typing.Optional["HttpMethod"]:
        """(experimental) The HTTP method to use when calling the underlying HTTP proxy.

        :default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.

        :stability: experimental
        """
        result = self._values.get("method")
        return result

    @builtins.property
    def payload_format_version(self) -> typing.Optional["PayloadFormatVersion"]:
        """(experimental) The version of the payload format.

        :default: - defaults to latest in the case of HttpIntegrationType.LAMBDA_PROXY`, irrelevant otherwise.

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        """
        result = self._values.get("payload_format_version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegrationType")
class HttpIntegrationType(enum.Enum):
    """(experimental) Supported integration types.

    :stability: experimental
    """

    LAMBDA_PROXY = "LAMBDA_PROXY"
    """(experimental) Integration type is a Lambda proxy.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    :stability: experimental
    """
    HTTP_PROXY = "HTTP_PROXY"
    """(experimental) Integration type is an HTTP proxy.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    :stability: experimental
    """


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpMethod")
class HttpMethod(enum.Enum):
    """(experimental) Supported HTTP methods.

    :stability: experimental
    """

    ANY = "ANY"
    """(experimental) HTTP ANY.

    :stability: experimental
    """
    DELETE = "DELETE"
    """(experimental) HTTP DELETE.

    :stability: experimental
    """
    GET = "GET"
    """(experimental) HTTP GET.

    :stability: experimental
    """
    HEAD = "HEAD"
    """(experimental) HTTP HEAD.

    :stability: experimental
    """
    OPTIONS = "OPTIONS"
    """(experimental) HTTP OPTIONS.

    :stability: experimental
    """
    PATCH = "PATCH"
    """(experimental) HTTP PATCH.

    :stability: experimental
    """
    POST = "POST"
    """(experimental) HTTP POST.

    :stability: experimental
    """
    PUT = "PUT"
    """(experimental) HTTP PUT.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteIntegrationBindOptions",
    jsii_struct_bases=[],
    name_mapping={"route": "route", "scope": "scope"},
)
class HttpRouteIntegrationBindOptions:
    def __init__(self, *, route: "IHttpRoute", scope: aws_cdk.core.Construct) -> None:
        """(experimental) Options to the HttpRouteIntegration during its bind operation.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "route": route,
            "scope": scope,
        }

    @builtins.property
    def route(self) -> "IHttpRoute":
        """(experimental) The route to which this is being bound.

        :stability: experimental
        """
        result = self._values.get("route")
        assert result is not None, "Required property 'route' is missing"
        return result

    @builtins.property
    def scope(self) -> aws_cdk.core.Construct:
        """(experimental) The current scope in which the bind is occurring.

        If the ``HttpRouteIntegration`` being bound creates additional constructs,
        this will be used as their parent scope.

        :stability: experimental
        """
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteIntegrationBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteIntegrationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "payload_format_version": "payloadFormatVersion",
        "type": "type",
        "uri": "uri",
        "connection_id": "connectionId",
        "connection_type": "connectionType",
        "method": "method",
    },
)
class HttpRouteIntegrationConfig:
    def __init__(
        self,
        *,
        payload_format_version: "PayloadFormatVersion",
        type: HttpIntegrationType,
        uri: builtins.str,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[HttpConnectionType] = None,
        method: typing.Optional[HttpMethod] = None,
    ) -> None:
        """(experimental) Config returned back as a result of the bind.

        :param payload_format_version: (experimental) Payload format version in the case of lambda proxy integration. Default: - undefined
        :param type: (experimental) Integration type.
        :param uri: (experimental) Integration URI.
        :param connection_id: (experimental) The ID of the VPC link for a private integration. Supported only for HTTP APIs. Default: - undefined
        :param connection_type: (experimental) The type of the network connection to the integration endpoint. Default: HttpConnectionType.INTERNET
        :param method: (experimental) The HTTP method that must be used to invoke the underlying proxy. Required for ``HttpIntegrationType.HTTP_PROXY`` Default: - undefined

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "payload_format_version": payload_format_version,
            "type": type,
            "uri": uri,
        }
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if method is not None:
            self._values["method"] = method

    @builtins.property
    def payload_format_version(self) -> "PayloadFormatVersion":
        """(experimental) Payload format version in the case of lambda proxy integration.

        :default: - undefined

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        """
        result = self._values.get("payload_format_version")
        assert result is not None, "Required property 'payload_format_version' is missing"
        return result

    @builtins.property
    def type(self) -> HttpIntegrationType:
        """(experimental) Integration type.

        :stability: experimental
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def uri(self) -> builtins.str:
        """(experimental) Integration URI.

        :stability: experimental
        """
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return result

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        """(experimental) The ID of the VPC link for a private integration.

        Supported only for HTTP APIs.

        :default: - undefined

        :stability: experimental
        """
        result = self._values.get("connection_id")
        return result

    @builtins.property
    def connection_type(self) -> typing.Optional[HttpConnectionType]:
        """(experimental) The type of the network connection to the integration endpoint.

        :default: HttpConnectionType.INTERNET

        :stability: experimental
        """
        result = self._values.get("connection_type")
        return result

    @builtins.property
    def method(self) -> typing.Optional[HttpMethod]:
        """(experimental) The HTTP method that must be used to invoke the underlying proxy.

        Required for ``HttpIntegrationType.HTTP_PROXY``

        :default: - undefined

        :stability: experimental
        """
        result = self._values.get("method")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpRouteKey(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteKey",
):
    """(experimental) HTTP route in APIGateway is a combination of the HTTP method and the path component.

    This class models that combination.

    :stability: experimental
    """

    @jsii.member(jsii_name="with")
    @builtins.classmethod
    def with_(
        cls,
        path: builtins.str,
        method: typing.Optional[HttpMethod] = None,
    ) -> "HttpRouteKey":
        """(experimental) Create a route key with the combination of the path and the method.

        :param path: -
        :param method: default is 'ANY'.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "with", [path, method])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DEFAULT")
    def DEFAULT(cls) -> "HttpRouteKey":
        """(experimental) The catch-all route of the API, i.e., when no other routes match.

        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        """(experimental) The key to the RouteKey as recognized by APIGateway.

        :stability: experimental
        """
        return jsii.get(self, "key")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        """(experimental) The path part of this RouteKey.

        Returns ``undefined`` when ``RouteKey.DEFAULT`` is used.

        :stability: experimental
        """
        return jsii.get(self, "path")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteProps",
    jsii_struct_bases=[BatchHttpRouteOptions],
    name_mapping={
        "integration": "integration",
        "http_api": "httpApi",
        "route_key": "routeKey",
    },
)
class HttpRouteProps(BatchHttpRouteOptions):
    def __init__(
        self,
        *,
        integration: "IHttpRouteIntegration",
        http_api: "IHttpApi",
        route_key: HttpRouteKey,
    ) -> None:
        """(experimental) Properties to initialize a new Route.

        :param integration: (experimental) The integration to be configured on this route.
        :param http_api: (experimental) the API the route is associated with.
        :param route_key: (experimental) The key to this route. This is a combination of an HTTP method and an HTTP path.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
            "http_api": http_api,
            "route_key": route_key,
        }

    @builtins.property
    def integration(self) -> "IHttpRouteIntegration":
        """(experimental) The integration to be configured on this route.

        :stability: experimental
        """
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return result

    @builtins.property
    def http_api(self) -> "IHttpApi":
        """(experimental) the API the route is associated with.

        :stability: experimental
        """
        result = self._values.get("http_api")
        assert result is not None, "Required property 'http_api' is missing"
        return result

    @builtins.property
    def route_key(self) -> HttpRouteKey:
        """(experimental) The key to this route.

        This is a combination of an HTTP method and an HTTP path.

        :stability: experimental
        """
        result = self._values.get("route_key")
        assert result is not None, "Required property 'route_key' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpStageOptions",
    jsii_struct_bases=[CommonStageOptions],
    name_mapping={
        "auto_deploy": "autoDeploy",
        "stage_name": "stageName",
        "domain_mapping": "domainMapping",
    },
)
class HttpStageOptions(CommonStageOptions):
    def __init__(
        self,
        *,
        auto_deploy: typing.Optional[builtins.bool] = None,
        stage_name: typing.Optional[builtins.str] = None,
        domain_mapping: typing.Optional[DomainMappingOptions] = None,
    ) -> None:
        """(experimental) Options to create a new stage for an HTTP API.

        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration

        :stability: experimental
        """
        if isinstance(domain_mapping, dict):
            domain_mapping = DomainMappingOptions(**domain_mapping)
        self._values: typing.Dict[str, typing.Any] = {}
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if domain_mapping is not None:
            self._values["domain_mapping"] = domain_mapping

    @builtins.property
    def auto_deploy(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether updates to an API automatically trigger a new deployment.

        :default: false

        :stability: experimental
        """
        result = self._values.get("auto_deploy")
        return result

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the stage.

        See ``StageName`` class for more details.

        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        """
        result = self._values.get("stage_name")
        return result

    @builtins.property
    def domain_mapping(self) -> typing.Optional[DomainMappingOptions]:
        """(experimental) The options for custom domain and api mapping.

        :default: - no custom domain and api mapping configuration

        :stability: experimental
        """
        result = self._values.get("domain_mapping")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpStageProps",
    jsii_struct_bases=[HttpStageOptions],
    name_mapping={
        "auto_deploy": "autoDeploy",
        "stage_name": "stageName",
        "domain_mapping": "domainMapping",
        "http_api": "httpApi",
    },
)
class HttpStageProps(HttpStageOptions):
    def __init__(
        self,
        *,
        auto_deploy: typing.Optional[builtins.bool] = None,
        stage_name: typing.Optional[builtins.str] = None,
        domain_mapping: typing.Optional[DomainMappingOptions] = None,
        http_api: "IHttpApi",
    ) -> None:
        """(experimental) Properties to initialize an instance of ``HttpStage``.

        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param http_api: (experimental) The HTTP API to which this stage is associated.

        :stability: experimental
        """
        if isinstance(domain_mapping, dict):
            domain_mapping = DomainMappingOptions(**domain_mapping)
        self._values: typing.Dict[str, typing.Any] = {
            "http_api": http_api,
        }
        if auto_deploy is not None:
            self._values["auto_deploy"] = auto_deploy
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if domain_mapping is not None:
            self._values["domain_mapping"] = domain_mapping

    @builtins.property
    def auto_deploy(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether updates to an API automatically trigger a new deployment.

        :default: false

        :stability: experimental
        """
        result = self._values.get("auto_deploy")
        return result

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the stage.

        See ``StageName`` class for more details.

        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        """
        result = self._values.get("stage_name")
        return result

    @builtins.property
    def domain_mapping(self) -> typing.Optional[DomainMappingOptions]:
        """(experimental) The options for custom domain and api mapping.

        :default: - no custom domain and api mapping configuration

        :stability: experimental
        """
        result = self._values.get("domain_mapping")
        return result

    @builtins.property
    def http_api(self) -> "IHttpApi":
        """(experimental) The HTTP API to which this stage is associated.

        :stability: experimental
        """
        result = self._values.get("http_api")
        assert result is not None, "Required property 'http_api' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IApiMapping")
class IApiMapping(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Represents an ApiGatewayV2 ApiMapping resource.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApiMappingProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiMappingId")
    def api_mapping_id(self) -> builtins.str:
        """(experimental) ID of the api mapping.

        :stability: experimental
        :attribute: true
        """
        ...


class _IApiMappingProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Represents an ApiGatewayV2 ApiMapping resource.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IApiMapping"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiMappingId")
    def api_mapping_id(self) -> builtins.str:
        """(experimental) ID of the api mapping.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "apiMappingId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IDomainName")
class IDomainName(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Represents an APIGatewayV2 DomainName.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDomainNameProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """(experimental) The custom domain name.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        """(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="regionalHostedZoneId")
    def regional_hosted_zone_id(self) -> builtins.str:
        """(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        :attribute: true
        """
        ...


class _IDomainNameProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Represents an APIGatewayV2 DomainName.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IDomainName"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """(experimental) The custom domain name.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "domainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        """(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "regionalDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="regionalHostedZoneId")
    def regional_hosted_zone_id(self) -> builtins.str:
        """(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "regionalHostedZoneId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpApi")
class IHttpApi(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Represents an HTTP API.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpApiProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> builtins.str:
        """(experimental) The identifier of this API Gateway HTTP API.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultStage")
    def default_stage(self) -> typing.Optional["HttpStage"]:
        """(experimental) The default stage.

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addVpcLink")
    def add_vpc_link(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.ISubnet]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> "VpcLink":
        """(experimental) Add a new VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Return the given named metric for this HTTP Api Gateway.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - SampleCount over 5 minutes

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        ...


class _IHttpApiProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Represents an HTTP API.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpApi"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> builtins.str:
        """(experimental) The identifier of this API Gateway HTTP API.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "httpApiId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultStage")
    def default_stage(self) -> typing.Optional["HttpStage"]:
        """(experimental) The default stage.

        :stability: experimental
        """
        return jsii.get(self, "defaultStage")

    @jsii.member(jsii_name="addVpcLink")
    def add_vpc_link(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.ISubnet]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> "VpcLink":
        """(experimental) Add a new VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        """
        options = VpcLinkProps(
            vpc=vpc,
            security_groups=security_groups,
            subnets=subnets,
            vpc_link_name=vpc_link_name,
        )

        return jsii.invoke(self, "addVpcLink", [options])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Return the given named metric for this HTTP Api Gateway.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricClientError", [props])

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - SampleCount over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricCount", [props])

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDataProcessed", [props])

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricIntegrationLatency", [props])

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricLatency", [props])

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricServerError", [props])


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpRouteIntegration")
class IHttpRouteIntegration(typing_extensions.Protocol):
    """(experimental) The interface that various route integration classes will inherit.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpRouteIntegrationProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: "IHttpRoute",
        scope: aws_cdk.core.Construct,
    ) -> HttpRouteIntegrationConfig:
        """(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        """
        ...


class _IHttpRouteIntegrationProxy:
    """(experimental) The interface that various route integration classes will inherit.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpRouteIntegration"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: "IHttpRoute",
        scope: aws_cdk.core.Construct,
    ) -> HttpRouteIntegrationConfig:
        """(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        """
        options = HttpRouteIntegrationBindOptions(route=route, scope=scope)

        return jsii.invoke(self, "bind", [options])


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IIntegration")
class IIntegration(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Represents an integration to an API Route.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IIntegrationProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        """(experimental) Id of the integration.

        :stability: experimental
        :attribute: true
        """
        ...


class _IIntegrationProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Represents an integration to an API Route.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IIntegration"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        """(experimental) Id of the integration.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "integrationId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IRoute")
class IRoute(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Represents a route.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRouteProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        """(experimental) Id of the Route.

        :stability: experimental
        :attribute: true
        """
        ...


class _IRouteProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Represents a route.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IRoute"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        """(experimental) Id of the Route.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "routeId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IStage")
class IStage(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Represents a Stage.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStageProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        """(experimental) The name of the stage;

        its primary identifier.

        :stability: experimental
        :attribute: true
        """
        ...


class _IStageProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Represents a Stage.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IStage"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        """(experimental) The name of the stage;

        its primary identifier.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "stageName")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IVpcLink")
class IVpcLink(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Represents an API Gateway VpcLink.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IVpcLinkProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> builtins.str:
        """(experimental) Physical ID of the VpcLink resource.

        :stability: experimental
        :attribute: true
        """
        ...


class _IVpcLinkProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Represents an API Gateway VpcLink.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IVpcLink"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> builtins.str:
        """(experimental) Physical ID of the VpcLink resource.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "vpcLinkId")


class PayloadFormatVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.PayloadFormatVersion",
):
    """(experimental) Payload format version for lambda proxy integration.

    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    :stability: experimental
    """

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, version: builtins.str) -> "PayloadFormatVersion":
        """(experimental) A custom payload version.

        Typically used if there is a version number that the CDK doesn't support yet

        :param version: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "custom", [version])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="VERSION_1_0")
    def VERSION_1_0(cls) -> "PayloadFormatVersion":
        """(experimental) Version 1.0.

        :stability: experimental
        """
        return jsii.sget(cls, "VERSION_1_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="VERSION_2_0")
    def VERSION_2_0(cls) -> "PayloadFormatVersion":
        """(experimental) Version 2.0.

        :stability: experimental
        """
        return jsii.sget(cls, "VERSION_2_0")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        """(experimental) version as a string.

        :stability: experimental
        """
        return jsii.get(self, "version")


@jsii.implements(IVpcLink)
class VpcLink(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.VpcLink",
):
    """(experimental) Define a new VPC Link Specifies an API Gateway VPC link for a HTTP API to access resources in an Amazon Virtual Private Cloud (VPC).

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.ISubnet]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        """
        props = VpcLinkProps(
            vpc=vpc,
            security_groups=security_groups,
            subnets=subnets,
            vpc_link_name=vpc_link_name,
        )

        jsii.create(VpcLink, self, [scope, id, props])

    @jsii.member(jsii_name="fromVpcLinkId")
    @builtins.classmethod
    def from_vpc_link_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        vpc_link_id: builtins.str,
    ) -> IVpcLink:
        """(experimental) Import a VPC Link by its Id.

        :param scope: -
        :param id: -
        :param vpc_link_id: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVpcLinkId", [scope, id, vpc_link_id])

    @jsii.member(jsii_name="addSecurityGroups")
    def add_security_groups(self, *groups: aws_cdk.aws_ec2.ISecurityGroup) -> None:
        """(experimental) Adds the provided security groups to the vpc link.

        :param groups: -

        :stability: experimental
        """
        return jsii.invoke(self, "addSecurityGroups", [*groups])

    @jsii.member(jsii_name="addSubnets")
    def add_subnets(self, *subnets: aws_cdk.aws_ec2.ISubnet) -> None:
        """(experimental) Adds the provided subnets to the vpc link.

        :param subnets: -

        :stability: experimental
        """
        return jsii.invoke(self, "addSubnets", [*subnets])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcLinkId")
    def vpc_link_id(self) -> builtins.str:
        """(experimental) Physical ID of the VpcLink resource.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "vpcLinkId")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.VpcLinkProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "vpc_link_name": "vpcLinkName",
    },
)
class VpcLinkProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.ISubnet]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties for a VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if vpc_link_name is not None:
            self._values["vpc_link_name"] = vpc_link_name

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """(experimental) The VPC in which the private resources reside.

        :stability: experimental
        """
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """(experimental) A list of security groups for the VPC link.

        :default: - no security groups. Use ``addSecurityGroups`` to add security groups

        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISubnet]]:
        """(experimental) A list of subnets for the VPC link.

        :default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets

        :stability: experimental
        """
        result = self._values.get("subnets")
        return result

    @builtins.property
    def vpc_link_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name used to label and identify the VPC link.

        :default: - automatically generated name

        :stability: experimental
        """
        result = self._values.get("vpc_link_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcLinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2.AddRoutesOptions",
    jsii_struct_bases=[BatchHttpRouteOptions],
    name_mapping={"integration": "integration", "path": "path", "methods": "methods"},
)
class AddRoutesOptions(BatchHttpRouteOptions):
    def __init__(
        self,
        *,
        integration: IHttpRouteIntegration,
        path: builtins.str,
        methods: typing.Optional[typing.List[HttpMethod]] = None,
    ) -> None:
        """(experimental) Options for the Route with Integration resoruce.

        :param integration: (experimental) The integration to be configured on this route.
        :param path: (experimental) The path at which all of these routes are configured.
        :param methods: (experimental) The HTTP methods to be configured. Default: HttpMethod.ANY

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "integration": integration,
            "path": path,
        }
        if methods is not None:
            self._values["methods"] = methods

    @builtins.property
    def integration(self) -> IHttpRouteIntegration:
        """(experimental) The integration to be configured on this route.

        :stability: experimental
        """
        result = self._values.get("integration")
        assert result is not None, "Required property 'integration' is missing"
        return result

    @builtins.property
    def path(self) -> builtins.str:
        """(experimental) The path at which all of these routes are configured.

        :stability: experimental
        """
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return result

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[HttpMethod]]:
        """(experimental) The HTTP methods to be configured.

        :default: HttpMethod.ANY

        :stability: experimental
        """
        result = self._values.get("methods")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRoutesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDomainName)
class DomainName(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.DomainName",
):
    """(experimental) Custom domain resource for the API.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        domain_name: builtins.str,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param certificate: (experimental) The ACM certificate for this domain name.
        :param domain_name: (experimental) The custom domain name.

        :stability: experimental
        """
        props = DomainNameProps(certificate=certificate, domain_name=domain_name)

        jsii.create(DomainName, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainNameAttributes")
    @builtins.classmethod
    def from_domain_name_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        regional_domain_name: builtins.str,
        regional_hosted_zone_id: builtins.str,
    ) -> IDomainName:
        """(experimental) import from attributes.

        :param scope: -
        :param id: -
        :param domain_name: (experimental) domain name string.
        :param regional_domain_name: (experimental) The domain name associated with the regional endpoint for this custom domain name.
        :param regional_hosted_zone_id: (experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        """
        attrs = DomainNameAttributes(
            domain_name=domain_name,
            regional_domain_name=regional_domain_name,
            regional_hosted_zone_id=regional_hosted_zone_id,
        )

        return jsii.sinvoke(cls, "fromDomainNameAttributes", [scope, id, attrs])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """(experimental) The custom domain name for your API in Amazon API Gateway.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "domainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        """(experimental) The domain name associated with the regional endpoint for this custom domain name.

        :stability: experimental
        """
        return jsii.get(self, "regionalDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="regionalHostedZoneId")
    def regional_hosted_zone_id(self) -> builtins.str:
        """(experimental) The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        """
        return jsii.get(self, "regionalHostedZoneId")


@jsii.implements(IHttpApi)
class HttpApi(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApi",
):
    """(experimental) Create a new API Gateway HTTP API endpoint.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Api
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_name: typing.Optional[builtins.str] = None,
        cors_preflight: typing.Optional[CorsPreflightOptions] = None,
        create_default_stage: typing.Optional[builtins.bool] = None,
        default_domain_mapping: typing.Optional[DefaultDomainMappingOptions] = None,
        default_integration: typing.Optional[IHttpRouteIntegration] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param api_name: (experimental) Name for the HTTP API resoruce. Default: - id of the HttpApi construct.
        :param cors_preflight: (experimental) Specifies a CORS configuration for an API. Default: - CORS disabled.
        :param create_default_stage: (experimental) Whether a default stage and deployment should be automatically created. Default: true
        :param default_domain_mapping: (experimental) Configure a custom domain with the API mapping resource to the HTTP API. Default: - no default domain mapping configured. meaningless if ``createDefaultStage`` is ``false``.
        :param default_integration: (experimental) An integration that will be configured on the catch-all route ($default). Default: - none
        :param description: (experimental) The description of the API. Default: - none

        :stability: experimental
        """
        props = HttpApiProps(
            api_name=api_name,
            cors_preflight=cors_preflight,
            create_default_stage=create_default_stage,
            default_domain_mapping=default_domain_mapping,
            default_integration=default_integration,
            description=description,
        )

        jsii.create(HttpApi, self, [scope, id, props])

    @jsii.member(jsii_name="fromApiId")
    @builtins.classmethod
    def from_api_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        http_api_id: builtins.str,
    ) -> IHttpApi:
        """(experimental) Import an existing HTTP API into this CDK app.

        :param scope: -
        :param id: -
        :param http_api_id: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromApiId", [scope, id, http_api_id])

    @jsii.member(jsii_name="addRoutes")
    def add_routes(
        self,
        *,
        path: builtins.str,
        methods: typing.Optional[typing.List[HttpMethod]] = None,
        integration: IHttpRouteIntegration,
    ) -> typing.List["HttpRoute"]:
        """(experimental) Add multiple routes that uses the same configuration.

        The routes all go to the same path, but for different
        methods.

        :param path: (experimental) The path at which all of these routes are configured.
        :param methods: (experimental) The HTTP methods to be configured. Default: HttpMethod.ANY
        :param integration: (experimental) The integration to be configured on this route.

        :stability: experimental
        """
        options = AddRoutesOptions(path=path, methods=methods, integration=integration)

        return jsii.invoke(self, "addRoutes", [options])

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        id: builtins.str,
        *,
        domain_mapping: typing.Optional[DomainMappingOptions] = None,
        auto_deploy: typing.Optional[builtins.bool] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> "HttpStage":
        """(experimental) Add a new stage.

        :param id: -
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        """
        options = HttpStageOptions(
            domain_mapping=domain_mapping,
            auto_deploy=auto_deploy,
            stage_name=stage_name,
        )

        return jsii.invoke(self, "addStage", [id, options])

    @jsii.member(jsii_name="addVpcLink")
    def add_vpc_link(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.ISubnet]] = None,
        vpc_link_name: typing.Optional[builtins.str] = None,
    ) -> VpcLink:
        """(experimental) Add a new VpcLink.

        :param vpc: (experimental) The VPC in which the private resources reside.
        :param security_groups: (experimental) A list of security groups for the VPC link. Default: - no security groups. Use ``addSecurityGroups`` to add security groups
        :param subnets: (experimental) A list of subnets for the VPC link. Default: - private subnets of the provided VPC. Use ``addSubnets`` to add more subnets
        :param vpc_link_name: (experimental) The name used to label and identify the VPC link. Default: - automatically generated name

        :stability: experimental
        """
        options = VpcLinkProps(
            vpc=vpc,
            security_groups=security_groups,
            subnets=subnets,
            vpc_link_name=vpc_link_name,
        )

        return jsii.invoke(self, "addVpcLink", [options])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Return the given named metric for this HTTP Api Gateway.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricClientError", [props])

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricCount", [props])

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDataProcessed", [props])

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricIntegrationLatency", [props])

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricLatency", [props])

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricServerError", [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiEndpoint")
    def api_endpoint(self) -> builtins.str:
        """(experimental) The default endpoint for an API.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "apiEndpoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> builtins.str:
        """(experimental) The identifier of this API Gateway HTTP API.

        :stability: experimental
        """
        return jsii.get(self, "httpApiId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultStage")
    def default_stage(self) -> typing.Optional["HttpStage"]:
        """(experimental) default stage of the api resource.

        :stability: experimental
        """
        return jsii.get(self, "defaultStage")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApiName")
    def http_api_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A human friendly name for this HTTP API.

        Note that this is different from ``httpApiId``.

        :stability: experimental
        """
        return jsii.get(self, "httpApiName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="url")
    def url(self) -> typing.Optional[builtins.str]:
        """(experimental) Get the URL to the default stage of this API.

        Returns ``undefined`` if ``createDefaultStage`` is unset.

        :stability: experimental
        """
        return jsii.get(self, "url")


@jsii.implements(IApiMapping)
class HttpApiMapping(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpApiMapping",
):
    """(experimental) Create a new API mapping for API Gateway HTTP API endpoint.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::ApiMapping
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api: IHttpApi,
        domain_name: IDomainName,
        api_mapping_key: typing.Optional[builtins.str] = None,
        stage: typing.Optional["IHttpStage"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param api: (experimental) The HttpApi to which this mapping is applied.
        :param domain_name: (experimental) custom domain name of the mapping target.
        :param api_mapping_key: (experimental) Api mapping key. The path where this stage should be mapped to on the domain Default: - undefined for the root path mapping.
        :param stage: (experimental) stage for the HttpApiMapping resource. Default: - the $default stage

        :stability: experimental
        """
        props = HttpApiMappingProps(
            api=api,
            domain_name=domain_name,
            api_mapping_key=api_mapping_key,
            stage=stage,
        )

        jsii.create(HttpApiMapping, self, [scope, id, props])

    @jsii.member(jsii_name="fromHttpApiMappingAttributes")
    @builtins.classmethod
    def from_http_api_mapping_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_mapping_id: builtins.str,
    ) -> IApiMapping:
        """(experimental) import from API ID.

        :param scope: -
        :param id: -
        :param api_mapping_id: (experimental) The API mapping ID.

        :stability: experimental
        """
        attrs = HttpApiMappingAttributes(api_mapping_id=api_mapping_id)

        return jsii.sinvoke(cls, "fromHttpApiMappingAttributes", [scope, id, attrs])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiMappingId")
    def api_mapping_id(self) -> builtins.str:
        """(experimental) ID of the API Mapping.

        :stability: experimental
        """
        return jsii.get(self, "apiMappingId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mappingKey")
    def mapping_key(self) -> typing.Optional[builtins.str]:
        """(experimental) API Mapping key.

        :stability: experimental
        """
        return jsii.get(self, "mappingKey")


@jsii.implements(IStage)
class HttpStage(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpStage",
):
    """(experimental) Represents a stage where an instance of the API is deployed.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Stage
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api: IHttpApi,
        domain_mapping: typing.Optional[DomainMappingOptions] = None,
        auto_deploy: typing.Optional[builtins.bool] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param http_api: (experimental) The HTTP API to which this stage is associated.
        :param domain_mapping: (experimental) The options for custom domain and api mapping. Default: - no custom domain and api mapping configuration
        :param auto_deploy: (experimental) Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: (experimental) The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        :stability: experimental
        """
        props = HttpStageProps(
            http_api=http_api,
            domain_mapping=domain_mapping,
            auto_deploy=auto_deploy,
            stage_name=stage_name,
        )

        jsii.create(HttpStage, self, [scope, id, props])

    @jsii.member(jsii_name="fromStageName")
    @builtins.classmethod
    def from_stage_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        stage_name: builtins.str,
    ) -> IStage:
        """(experimental) Import an existing stage into this CDK app.

        :param scope: -
        :param id: -
        :param stage_name: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromStageName", [scope, id, stage_name])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Return the given named metric for this HTTP Api Gateway Stage.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of client-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricClientError", [props])

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the total number API requests in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - SampleCount over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricCount", [props])

    @jsii.member(jsii_name="metricDataProcessed")
    def metric_data_processed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the amount of data processed in bytes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDataProcessed", [props])

    @jsii.member(jsii_name="metricIntegrationLatency")
    def metric_integration_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the time between when API Gateway relays a request to the backend and when it receives a response from the backend.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricIntegrationLatency", [props])

    @jsii.member(jsii_name="metricLatency")
    def metric_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) The time between when API Gateway receives a request from a client and when it returns a response to the client.

        The latency includes the integration latency and other API Gateway overhead.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - no statistic

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricLatency", [props])

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(experimental) Metric for the number of server-side errors captured in a given period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricServerError", [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        """(experimental) The name of the stage;

        its primary identifier.

        :stability: experimental
        """
        return jsii.get(self, "stageName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        """(experimental) The URL to this stage.

        :stability: experimental
        """
        return jsii.get(self, "url")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpIntegration")
class IHttpIntegration(IIntegration, typing_extensions.Protocol):
    """(experimental) Represents an Integration for an HTTP API.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpIntegrationProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        """(experimental) The HTTP API associated with this integration.

        :stability: experimental
        """
        ...


class _IHttpIntegrationProxy(
    jsii.proxy_for(IIntegration) # type: ignore
):
    """(experimental) Represents an Integration for an HTTP API.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpIntegration"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        """(experimental) The HTTP API associated with this integration.

        :stability: experimental
        """
        return jsii.get(self, "httpApi")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpRoute")
class IHttpRoute(IRoute, typing_extensions.Protocol):
    """(experimental) Represents a Route for an HTTP API.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpRouteProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        """(experimental) The HTTP API associated with this route.

        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        """(experimental) Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        :stability: experimental
        """
        ...


class _IHttpRouteProxy(
    jsii.proxy_for(IRoute) # type: ignore
):
    """(experimental) Represents a Route for an HTTP API.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpRoute"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        """(experimental) The HTTP API associated with this route.

        :stability: experimental
        """
        return jsii.get(self, "httpApi")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        """(experimental) Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        :stability: experimental
        """
        return jsii.get(self, "path")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpStage")
class IHttpStage(IStage, typing_extensions.Protocol):
    """(experimental) Represents the HttpStage.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpStageProxy


class _IHttpStageProxy(
    jsii.proxy_for(IStage) # type: ignore
):
    """(experimental) Represents the HttpStage.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-apigatewayv2.IHttpStage"
    pass


@jsii.implements(IHttpIntegration)
class HttpIntegration(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegration",
):
    """(experimental) The integration for an API route.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Integration
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api: IHttpApi,
        integration_type: HttpIntegrationType,
        integration_uri: builtins.str,
        connection_id: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[HttpConnectionType] = None,
        method: typing.Optional[HttpMethod] = None,
        payload_format_version: typing.Optional[PayloadFormatVersion] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param http_api: (experimental) The HTTP API to which this integration should be bound.
        :param integration_type: (experimental) Integration type.
        :param integration_uri: (experimental) Integration URI. This will be the function ARN in the case of ``HttpIntegrationType.LAMBDA_PROXY``, or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``.
        :param connection_id: (experimental) The ID of the VPC link for a private integration. Supported only for HTTP APIs. Default: - undefined
        :param connection_type: (experimental) The type of the network connection to the integration endpoint. Default: HttpConnectionType.INTERNET
        :param method: (experimental) The HTTP method to use when calling the underlying HTTP proxy. Default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.
        :param payload_format_version: (experimental) The version of the payload format. Default: - defaults to latest in the case of HttpIntegrationType.LAMBDA_PROXY`, irrelevant otherwise.

        :stability: experimental
        """
        props = HttpIntegrationProps(
            http_api=http_api,
            integration_type=integration_type,
            integration_uri=integration_uri,
            connection_id=connection_id,
            connection_type=connection_type,
            method=method,
            payload_format_version=payload_format_version,
        )

        jsii.create(HttpIntegration, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        """(experimental) The HTTP API associated with this integration.

        :stability: experimental
        """
        return jsii.get(self, "httpApi")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> builtins.str:
        """(experimental) Id of the integration.

        :stability: experimental
        """
        return jsii.get(self, "integrationId")


@jsii.implements(IHttpRoute)
class HttpRoute(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2.HttpRoute",
):
    """(experimental) Route class that creates the Route for API Gateway HTTP API.

    :stability: experimental
    :resource: AWS::ApiGatewayV2::Route
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http_api: IHttpApi,
        route_key: HttpRouteKey,
        integration: IHttpRouteIntegration,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param http_api: (experimental) the API the route is associated with.
        :param route_key: (experimental) The key to this route. This is a combination of an HTTP method and an HTTP path.
        :param integration: (experimental) The integration to be configured on this route.

        :stability: experimental
        """
        props = HttpRouteProps(
            http_api=http_api, route_key=route_key, integration=integration
        )

        jsii.create(HttpRoute, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> IHttpApi:
        """(experimental) The HTTP API associated with this route.

        :stability: experimental
        """
        return jsii.get(self, "httpApi")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> builtins.str:
        """(experimental) Id of the Route.

        :stability: experimental
        """
        return jsii.get(self, "routeId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        """(experimental) Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        :stability: experimental
        """
        return jsii.get(self, "path")


__all__ = [
    "AddRoutesOptions",
    "BatchHttpRouteOptions",
    "CfnApi",
    "CfnApiGatewayManagedOverrides",
    "CfnApiGatewayManagedOverridesProps",
    "CfnApiMapping",
    "CfnApiMappingProps",
    "CfnApiProps",
    "CfnAuthorizer",
    "CfnAuthorizerProps",
    "CfnDeployment",
    "CfnDeploymentProps",
    "CfnDomainName",
    "CfnDomainNameProps",
    "CfnIntegration",
    "CfnIntegrationProps",
    "CfnIntegrationResponse",
    "CfnIntegrationResponseProps",
    "CfnModel",
    "CfnModelProps",
    "CfnRoute",
    "CfnRouteProps",
    "CfnRouteResponse",
    "CfnRouteResponseProps",
    "CfnStage",
    "CfnStageProps",
    "CfnVpcLink",
    "CfnVpcLinkProps",
    "CommonStageOptions",
    "CorsPreflightOptions",
    "DefaultDomainMappingOptions",
    "DomainMappingOptions",
    "DomainName",
    "DomainNameAttributes",
    "DomainNameProps",
    "HttpApi",
    "HttpApiMapping",
    "HttpApiMappingAttributes",
    "HttpApiMappingProps",
    "HttpApiProps",
    "HttpConnectionType",
    "HttpIntegration",
    "HttpIntegrationProps",
    "HttpIntegrationType",
    "HttpMethod",
    "HttpRoute",
    "HttpRouteIntegrationBindOptions",
    "HttpRouteIntegrationConfig",
    "HttpRouteKey",
    "HttpRouteProps",
    "HttpStage",
    "HttpStageOptions",
    "HttpStageProps",
    "IApiMapping",
    "IDomainName",
    "IHttpApi",
    "IHttpIntegration",
    "IHttpRoute",
    "IHttpRouteIntegration",
    "IHttpStage",
    "IIntegration",
    "IRoute",
    "IStage",
    "IVpcLink",
    "PayloadFormatVersion",
    "VpcLink",
    "VpcLinkProps",
]

publication.publish()
