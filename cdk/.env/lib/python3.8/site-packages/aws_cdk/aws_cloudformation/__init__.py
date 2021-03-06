"""
## AWS CloudFormation Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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

import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCustomResource(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResource",
):
    """A CloudFormation ``AWS::CloudFormation::CustomResource``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
    :cloudformationResource: AWS::CloudFormation::CustomResource
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        service_token: builtins.str,
    ) -> None:
        """Create a new ``AWS::CloudFormation::CustomResource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.
        """
        props = CfnCustomResourceProps(service_token=service_token)

        jsii.create(CfnCustomResource, self, [scope, id, props])

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
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        """``AWS::CloudFormation::CustomResource.ServiceToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        """
        return jsii.get(self, "serviceToken")

    @service_token.setter # type: ignore
    def service_token(self, value: builtins.str) -> None:
        jsii.set(self, "serviceToken", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={"service_token": "serviceToken"},
)
class CfnCustomResourceProps:
    def __init__(self, *, service_token: builtins.str) -> None:
        """Properties for defining a ``AWS::CloudFormation::CustomResource``.

        :param service_token: ``AWS::CloudFormation::CustomResource.ServiceToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "service_token": service_token,
        }

    @builtins.property
    def service_token(self) -> builtins.str:
        """``AWS::CloudFormation::CustomResource.ServiceToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#cfn-customresource-servicetoken
        """
        result = self._values.get("service_token")
        assert result is not None, "Required property 'service_token' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMacro(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnMacro",
):
    """A CloudFormation ``AWS::CloudFormation::Macro``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
    :cloudformationResource: AWS::CloudFormation::Macro
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        function_name: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::CloudFormation::Macro``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.
        """
        props = CfnMacroProps(
            function_name=function_name,
            name=name,
            description=description,
            log_group_name=log_group_name,
            log_role_arn=log_role_arn,
        )

        jsii.create(CfnMacro, self, [scope, id, props])

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
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        """``AWS::CloudFormation::Macro.FunctionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter # type: ignore
    def function_name(self, value: builtins.str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::CloudFormation::Macro.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::Macro.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::Macro.LogGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter # type: ignore
    def log_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logRoleArn")
    def log_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::Macro.LogRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        """
        return jsii.get(self, "logRoleArn")

    @log_role_arn.setter # type: ignore
    def log_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logRoleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnMacroProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "name": "name",
        "description": "description",
        "log_group_name": "logGroupName",
        "log_role_arn": "logRoleArn",
    },
)
class CfnMacroProps:
    def __init__(
        self,
        *,
        function_name: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudFormation::Macro``.

        :param function_name: ``AWS::CloudFormation::Macro.FunctionName``.
        :param name: ``AWS::CloudFormation::Macro.Name``.
        :param description: ``AWS::CloudFormation::Macro.Description``.
        :param log_group_name: ``AWS::CloudFormation::Macro.LogGroupName``.
        :param log_role_arn: ``AWS::CloudFormation::Macro.LogRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "function_name": function_name,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_role_arn is not None:
            self._values["log_role_arn"] = log_role_arn

    @builtins.property
    def function_name(self) -> builtins.str:
        """``AWS::CloudFormation::Macro.FunctionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        """
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::CloudFormation::Macro.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::Macro.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::Macro.LogGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        """
        result = self._values.get("log_group_name")
        return result

    @builtins.property
    def log_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::Macro.LogRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        """
        result = self._values.get("log_role_arn")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMacroProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStack(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnStack",
):
    """A CloudFormation ``AWS::CloudFormation::Stack``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
    :cloudformationResource: AWS::CloudFormation::Stack
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        template_url: builtins.str,
        notification_arns: typing.Optional[typing.List[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Create a new ``AWS::CloudFormation::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.
        """
        props = CfnStackProps(
            template_url=template_url,
            notification_arns=notification_arns,
            parameters=parameters,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
        )

        jsii.create(CfnStack, self, [scope, id, props])

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
        """``AWS::CloudFormation::Stack.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> builtins.str:
        """``AWS::CloudFormation::Stack.TemplateURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        """
        return jsii.get(self, "templateUrl")

    @template_url.setter # type: ignore
    def template_url(self, value: builtins.str) -> None:
        jsii.set(self, "templateUrl", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudFormation::Stack.NotificationARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        """
        return jsii.get(self, "notificationArns")

    @notification_arns.setter # type: ignore
    def notification_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "notificationArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::CloudFormation::Stack.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter # type: ignore
    def parameters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        """
        return jsii.get(self, "timeoutInMinutes")

    @timeout_in_minutes.setter # type: ignore
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMinutes", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_url": "templateUrl",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnStackProps:
    def __init__(
        self,
        *,
        template_url: builtins.str,
        notification_arns: typing.Optional[typing.List[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudFormation::Stack``.

        :param template_url: ``AWS::CloudFormation::Stack.TemplateURL``.
        :param notification_arns: ``AWS::CloudFormation::Stack.NotificationARNs``.
        :param parameters: ``AWS::CloudFormation::Stack.Parameters``.
        :param tags: ``AWS::CloudFormation::Stack.Tags``.
        :param timeout_in_minutes: ``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "template_url": template_url,
        }
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def template_url(self) -> builtins.str:
        """``AWS::CloudFormation::Stack.TemplateURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-templateurl
        """
        result = self._values.get("template_url")
        assert result is not None, "Required property 'template_url' is missing"
        return result

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudFormation::Stack.NotificationARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-notificationarns
        """
        result = self._values.get("notification_arns")
        return result

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::CloudFormation::Stack.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-parameters
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CloudFormation::Stack.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::Stack.TimeoutInMinutes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stack.html#cfn-cloudformation-stack-timeoutinminutes
        """
        result = self._values.get("timeout_in_minutes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStackSet(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet",
):
    """A CloudFormation ``AWS::CloudFormation::StackSet``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
    :cloudformationResource: AWS::CloudFormation::StackSet
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        administration_role_arn: typing.Optional[builtins.str] = None,
        auto_deployment: typing.Optional[typing.Union["CfnStackSet.AutoDeploymentProperty", aws_cdk.core.IResolvable]] = None,
        capabilities: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_name: typing.Optional[builtins.str] = None,
        operation_preferences: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.OperationPreferencesProperty"]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]] = None,
        permission_model: typing.Optional[builtins.str] = None,
        stack_instances_group: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.StackInstancesProperty"]]]] = None,
        stack_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_url: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::CloudFormation::StackSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param administration_role_arn: ``AWS::CloudFormation::StackSet.AdministrationRoleARN``.
        :param auto_deployment: ``AWS::CloudFormation::StackSet.AutoDeployment``.
        :param capabilities: ``AWS::CloudFormation::StackSet.Capabilities``.
        :param description: ``AWS::CloudFormation::StackSet.Description``.
        :param execution_role_name: ``AWS::CloudFormation::StackSet.ExecutionRoleName``.
        :param operation_preferences: ``AWS::CloudFormation::StackSet.OperationPreferences``.
        :param parameters: ``AWS::CloudFormation::StackSet.Parameters``.
        :param permission_model: ``AWS::CloudFormation::StackSet.PermissionModel``.
        :param stack_instances_group: ``AWS::CloudFormation::StackSet.StackInstancesGroup``.
        :param stack_set_name: ``AWS::CloudFormation::StackSet.StackSetName``.
        :param tags: ``AWS::CloudFormation::StackSet.Tags``.
        :param template_body: ``AWS::CloudFormation::StackSet.TemplateBody``.
        :param template_url: ``AWS::CloudFormation::StackSet.TemplateURL``.
        """
        props = CfnStackSetProps(
            administration_role_arn=administration_role_arn,
            auto_deployment=auto_deployment,
            capabilities=capabilities,
            description=description,
            execution_role_name=execution_role_name,
            operation_preferences=operation_preferences,
            parameters=parameters,
            permission_model=permission_model,
            stack_instances_group=stack_instances_group,
            stack_set_name=stack_set_name,
            tags=tags,
            template_body=template_body,
            template_url=template_url,
        )

        jsii.create(CfnStackSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrStackSetId")
    def attr_stack_set_id(self) -> builtins.str:
        """
        :cloudformationAttribute: StackSetId
        """
        return jsii.get(self, "attrStackSetId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudFormation::StackSet.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="administrationRoleArn")
    def administration_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.AdministrationRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-administrationrolearn
        """
        return jsii.get(self, "administrationRoleArn")

    @administration_role_arn.setter # type: ignore
    def administration_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "administrationRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoDeployment")
    def auto_deployment(
        self,
    ) -> typing.Optional[typing.Union["CfnStackSet.AutoDeploymentProperty", aws_cdk.core.IResolvable]]:
        """``AWS::CloudFormation::StackSet.AutoDeployment``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-autodeployment
        """
        return jsii.get(self, "autoDeployment")

    @auto_deployment.setter # type: ignore
    def auto_deployment(
        self,
        value: typing.Optional[typing.Union["CfnStackSet.AutoDeploymentProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "autoDeployment", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudFormation::StackSet.Capabilities``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-capabilities
        """
        return jsii.get(self, "capabilities")

    @capabilities.setter # type: ignore
    def capabilities(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "capabilities", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="executionRoleName")
    def execution_role_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.ExecutionRoleName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-executionrolename
        """
        return jsii.get(self, "executionRoleName")

    @execution_role_name.setter # type: ignore
    def execution_role_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "executionRoleName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="operationPreferences")
    def operation_preferences(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.OperationPreferencesProperty"]]:
        """``AWS::CloudFormation::StackSet.OperationPreferences``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-operationpreferences
        """
        return jsii.get(self, "operationPreferences")

    @operation_preferences.setter # type: ignore
    def operation_preferences(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.OperationPreferencesProperty"]],
    ) -> None:
        jsii.set(self, "operationPreferences", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]]:
        """``AWS::CloudFormation::StackSet.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter # type: ignore
    def parameters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]],
    ) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="permissionModel")
    def permission_model(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.PermissionModel``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-permissionmodel
        """
        return jsii.get(self, "permissionModel")

    @permission_model.setter # type: ignore
    def permission_model(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "permissionModel", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackInstancesGroup")
    def stack_instances_group(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.StackInstancesProperty"]]]]:
        """``AWS::CloudFormation::StackSet.StackInstancesGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stackinstancesgroup
        """
        return jsii.get(self, "stackInstancesGroup")

    @stack_instances_group.setter # type: ignore
    def stack_instances_group(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.StackInstancesProperty"]]]],
    ) -> None:
        jsii.set(self, "stackInstancesGroup", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackSetName")
    def stack_set_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.StackSetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stacksetname
        """
        return jsii.get(self, "stackSetName")

    @stack_set_name.setter # type: ignore
    def stack_set_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "stackSetName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateBody")
    def template_body(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.TemplateBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templatebody
        """
        return jsii.get(self, "templateBody")

    @template_body.setter # type: ignore
    def template_body(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateBody", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.TemplateURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templateurl
        """
        return jsii.get(self, "templateUrl")

    @template_url.setter # type: ignore
    def template_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateUrl", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.AutoDeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "retain_stacks_on_account_removal": "retainStacksOnAccountRemoval",
        },
    )
    class AutoDeploymentProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            retain_stacks_on_account_removal: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param enabled: ``CfnStackSet.AutoDeploymentProperty.Enabled``.
            :param retain_stacks_on_account_removal: ``CfnStackSet.AutoDeploymentProperty.RetainStacksOnAccountRemoval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if retain_stacks_on_account_removal is not None:
                self._values["retain_stacks_on_account_removal"] = retain_stacks_on_account_removal

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnStackSet.AutoDeploymentProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def retain_stacks_on_account_removal(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnStackSet.AutoDeploymentProperty.RetainStacksOnAccountRemoval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-retainstacksonaccountremoval
            """
            result = self._values.get("retain_stacks_on_account_removal")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoDeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.DeploymentTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accounts": "accounts",
            "organizational_unit_ids": "organizationalUnitIds",
        },
    )
    class DeploymentTargetsProperty:
        def __init__(
            self,
            *,
            accounts: typing.Optional[typing.List[builtins.str]] = None,
            organizational_unit_ids: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param accounts: ``CfnStackSet.DeploymentTargetsProperty.Accounts``.
            :param organizational_unit_ids: ``CfnStackSet.DeploymentTargetsProperty.OrganizationalUnitIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if accounts is not None:
                self._values["accounts"] = accounts
            if organizational_unit_ids is not None:
                self._values["organizational_unit_ids"] = organizational_unit_ids

        @builtins.property
        def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnStackSet.DeploymentTargetsProperty.Accounts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-accounts
            """
            result = self._values.get("accounts")
            return result

        @builtins.property
        def organizational_unit_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnStackSet.DeploymentTargetsProperty.OrganizationalUnitIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-organizationalunitids
            """
            result = self._values.get("organizational_unit_ids")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.OperationPreferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_tolerance_count": "failureToleranceCount",
            "failure_tolerance_percentage": "failureTolerancePercentage",
            "max_concurrent_count": "maxConcurrentCount",
            "max_concurrent_percentage": "maxConcurrentPercentage",
            "region_order": "regionOrder",
        },
    )
    class OperationPreferencesProperty:
        def __init__(
            self,
            *,
            failure_tolerance_count: typing.Optional[jsii.Number] = None,
            failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
            max_concurrent_count: typing.Optional[jsii.Number] = None,
            max_concurrent_percentage: typing.Optional[jsii.Number] = None,
            region_order: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param failure_tolerance_count: ``CfnStackSet.OperationPreferencesProperty.FailureToleranceCount``.
            :param failure_tolerance_percentage: ``CfnStackSet.OperationPreferencesProperty.FailureTolerancePercentage``.
            :param max_concurrent_count: ``CfnStackSet.OperationPreferencesProperty.MaxConcurrentCount``.
            :param max_concurrent_percentage: ``CfnStackSet.OperationPreferencesProperty.MaxConcurrentPercentage``.
            :param region_order: ``CfnStackSet.OperationPreferencesProperty.RegionOrder``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if failure_tolerance_count is not None:
                self._values["failure_tolerance_count"] = failure_tolerance_count
            if failure_tolerance_percentage is not None:
                self._values["failure_tolerance_percentage"] = failure_tolerance_percentage
            if max_concurrent_count is not None:
                self._values["max_concurrent_count"] = max_concurrent_count
            if max_concurrent_percentage is not None:
                self._values["max_concurrent_percentage"] = max_concurrent_percentage
            if region_order is not None:
                self._values["region_order"] = region_order

        @builtins.property
        def failure_tolerance_count(self) -> typing.Optional[jsii.Number]:
            """``CfnStackSet.OperationPreferencesProperty.FailureToleranceCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancecount
            """
            result = self._values.get("failure_tolerance_count")
            return result

        @builtins.property
        def failure_tolerance_percentage(self) -> typing.Optional[jsii.Number]:
            """``CfnStackSet.OperationPreferencesProperty.FailureTolerancePercentage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancepercentage
            """
            result = self._values.get("failure_tolerance_percentage")
            return result

        @builtins.property
        def max_concurrent_count(self) -> typing.Optional[jsii.Number]:
            """``CfnStackSet.OperationPreferencesProperty.MaxConcurrentCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentcount
            """
            result = self._values.get("max_concurrent_count")
            return result

        @builtins.property
        def max_concurrent_percentage(self) -> typing.Optional[jsii.Number]:
            """``CfnStackSet.OperationPreferencesProperty.MaxConcurrentPercentage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentpercentage
            """
            result = self._values.get("max_concurrent_percentage")
            return result

        @builtins.property
        def region_order(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnStackSet.OperationPreferencesProperty.RegionOrder``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-regionorder
            """
            result = self._values.get("region_order")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OperationPreferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_key": "parameterKey",
            "parameter_value": "parameterValue",
        },
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            parameter_key: builtins.str,
            parameter_value: builtins.str,
        ) -> None:
            """
            :param parameter_key: ``CfnStackSet.ParameterProperty.ParameterKey``.
            :param parameter_value: ``CfnStackSet.ParameterProperty.ParameterValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "parameter_key": parameter_key,
                "parameter_value": parameter_value,
            }

        @builtins.property
        def parameter_key(self) -> builtins.str:
            """``CfnStackSet.ParameterProperty.ParameterKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parameterkey
            """
            result = self._values.get("parameter_key")
            assert result is not None, "Required property 'parameter_key' is missing"
            return result

        @builtins.property
        def parameter_value(self) -> builtins.str:
            """``CfnStackSet.ParameterProperty.ParameterValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parametervalue
            """
            result = self._values.get("parameter_value")
            assert result is not None, "Required property 'parameter_value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudformation.CfnStackSet.StackInstancesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_targets": "deploymentTargets",
            "regions": "regions",
            "parameter_overrides": "parameterOverrides",
        },
    )
    class StackInstancesProperty:
        def __init__(
            self,
            *,
            deployment_targets: typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.DeploymentTargetsProperty"],
            regions: typing.List[builtins.str],
            parameter_overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]] = None,
        ) -> None:
            """
            :param deployment_targets: ``CfnStackSet.StackInstancesProperty.DeploymentTargets``.
            :param regions: ``CfnStackSet.StackInstancesProperty.Regions``.
            :param parameter_overrides: ``CfnStackSet.StackInstancesProperty.ParameterOverrides``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "deployment_targets": deployment_targets,
                "regions": regions,
            }
            if parameter_overrides is not None:
                self._values["parameter_overrides"] = parameter_overrides

        @builtins.property
        def deployment_targets(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.DeploymentTargetsProperty"]:
            """``CfnStackSet.StackInstancesProperty.DeploymentTargets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-deploymenttargets
            """
            result = self._values.get("deployment_targets")
            assert result is not None, "Required property 'deployment_targets' is missing"
            return result

        @builtins.property
        def regions(self) -> typing.List[builtins.str]:
            """``CfnStackSet.StackInstancesProperty.Regions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-regions
            """
            result = self._values.get("regions")
            assert result is not None, "Required property 'regions' is missing"
            return result

        @builtins.property
        def parameter_overrides(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStackSet.ParameterProperty"]]]]:
            """``CfnStackSet.StackInstancesProperty.ParameterOverrides``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-parameteroverrides
            """
            result = self._values.get("parameter_overrides")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackInstancesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnStackSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "administration_role_arn": "administrationRoleArn",
        "auto_deployment": "autoDeployment",
        "capabilities": "capabilities",
        "description": "description",
        "execution_role_name": "executionRoleName",
        "operation_preferences": "operationPreferences",
        "parameters": "parameters",
        "permission_model": "permissionModel",
        "stack_instances_group": "stackInstancesGroup",
        "stack_set_name": "stackSetName",
        "tags": "tags",
        "template_body": "templateBody",
        "template_url": "templateUrl",
    },
)
class CfnStackSetProps:
    def __init__(
        self,
        *,
        administration_role_arn: typing.Optional[builtins.str] = None,
        auto_deployment: typing.Optional[typing.Union[CfnStackSet.AutoDeploymentProperty, aws_cdk.core.IResolvable]] = None,
        capabilities: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_name: typing.Optional[builtins.str] = None,
        operation_preferences: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.OperationPreferencesProperty]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.ParameterProperty]]]] = None,
        permission_model: typing.Optional[builtins.str] = None,
        stack_instances_group: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.StackInstancesProperty]]]] = None,
        stack_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_url: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudFormation::StackSet``.

        :param administration_role_arn: ``AWS::CloudFormation::StackSet.AdministrationRoleARN``.
        :param auto_deployment: ``AWS::CloudFormation::StackSet.AutoDeployment``.
        :param capabilities: ``AWS::CloudFormation::StackSet.Capabilities``.
        :param description: ``AWS::CloudFormation::StackSet.Description``.
        :param execution_role_name: ``AWS::CloudFormation::StackSet.ExecutionRoleName``.
        :param operation_preferences: ``AWS::CloudFormation::StackSet.OperationPreferences``.
        :param parameters: ``AWS::CloudFormation::StackSet.Parameters``.
        :param permission_model: ``AWS::CloudFormation::StackSet.PermissionModel``.
        :param stack_instances_group: ``AWS::CloudFormation::StackSet.StackInstancesGroup``.
        :param stack_set_name: ``AWS::CloudFormation::StackSet.StackSetName``.
        :param tags: ``AWS::CloudFormation::StackSet.Tags``.
        :param template_body: ``AWS::CloudFormation::StackSet.TemplateBody``.
        :param template_url: ``AWS::CloudFormation::StackSet.TemplateURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if administration_role_arn is not None:
            self._values["administration_role_arn"] = administration_role_arn
        if auto_deployment is not None:
            self._values["auto_deployment"] = auto_deployment
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if description is not None:
            self._values["description"] = description
        if execution_role_name is not None:
            self._values["execution_role_name"] = execution_role_name
        if operation_preferences is not None:
            self._values["operation_preferences"] = operation_preferences
        if parameters is not None:
            self._values["parameters"] = parameters
        if permission_model is not None:
            self._values["permission_model"] = permission_model
        if stack_instances_group is not None:
            self._values["stack_instances_group"] = stack_instances_group
        if stack_set_name is not None:
            self._values["stack_set_name"] = stack_set_name
        if tags is not None:
            self._values["tags"] = tags
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_url is not None:
            self._values["template_url"] = template_url

    @builtins.property
    def administration_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.AdministrationRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-administrationrolearn
        """
        result = self._values.get("administration_role_arn")
        return result

    @builtins.property
    def auto_deployment(
        self,
    ) -> typing.Optional[typing.Union[CfnStackSet.AutoDeploymentProperty, aws_cdk.core.IResolvable]]:
        """``AWS::CloudFormation::StackSet.AutoDeployment``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-autodeployment
        """
        result = self._values.get("auto_deployment")
        return result

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::CloudFormation::StackSet.Capabilities``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-capabilities
        """
        result = self._values.get("capabilities")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def execution_role_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.ExecutionRoleName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-executionrolename
        """
        result = self._values.get("execution_role_name")
        return result

    @builtins.property
    def operation_preferences(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.OperationPreferencesProperty]]:
        """``AWS::CloudFormation::StackSet.OperationPreferences``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-operationpreferences
        """
        result = self._values.get("operation_preferences")
        return result

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.ParameterProperty]]]]:
        """``AWS::CloudFormation::StackSet.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-parameters
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def permission_model(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.PermissionModel``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-permissionmodel
        """
        result = self._values.get("permission_model")
        return result

    @builtins.property
    def stack_instances_group(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStackSet.StackInstancesProperty]]]]:
        """``AWS::CloudFormation::StackSet.StackInstancesGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stackinstancesgroup
        """
        result = self._values.get("stack_instances_group")
        return result

    @builtins.property
    def stack_set_name(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.StackSetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stacksetname
        """
        result = self._values.get("stack_set_name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CloudFormation::StackSet.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def template_body(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.TemplateBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templatebody
        """
        result = self._values.get("template_body")
        return result

    @builtins.property
    def template_url(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::StackSet.TemplateURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templateurl
        """
        result = self._values.get("template_url")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWaitCondition(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnWaitCondition",
):
    """A CloudFormation ``AWS::CloudFormation::WaitCondition``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
    :cloudformationResource: AWS::CloudFormation::WaitCondition
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        count: typing.Optional[jsii.Number] = None,
        handle: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::CloudFormation::WaitCondition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.
        """
        props = CfnWaitConditionProps(count=count, handle=handle, timeout=timeout)

        jsii.create(CfnWaitCondition, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrData")
    def attr_data(self) -> aws_cdk.core.IResolvable:
        """
        :cloudformationAttribute: Data
        """
        return jsii.get(self, "attrData")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::WaitCondition.Count``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        """
        return jsii.get(self, "count")

    @count.setter # type: ignore
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="handle")
    def handle(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::WaitCondition.Handle``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        """
        return jsii.get(self, "handle")

    @handle.setter # type: ignore
    def handle(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "handle", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::WaitCondition.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter # type: ignore
    def timeout(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "timeout", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWaitConditionHandle(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionHandle",
):
    """A CloudFormation ``AWS::CloudFormation::WaitConditionHandle``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitconditionhandle.html
    :cloudformationResource: AWS::CloudFormation::WaitConditionHandle
    """

    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        """Create a new ``AWS::CloudFormation::WaitConditionHandle``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        """
        jsii.create(CfnWaitConditionHandle, self, [scope, id])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CfnWaitConditionProps",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "handle": "handle", "timeout": "timeout"},
)
class CfnWaitConditionProps:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        handle: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudFormation::WaitCondition``.

        :param count: ``AWS::CloudFormation::WaitCondition.Count``.
        :param handle: ``AWS::CloudFormation::WaitCondition.Handle``.
        :param timeout: ``AWS::CloudFormation::WaitCondition.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if handle is not None:
            self._values["handle"] = handle
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """``AWS::CloudFormation::WaitCondition.Count``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-count
        """
        result = self._values.get("count")
        return result

    @builtins.property
    def handle(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::WaitCondition.Handle``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-handle
        """
        result = self._values.get("handle")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        """``AWS::CloudFormation::WaitCondition.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waitcondition.html#cfn-waitcondition-timeout
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWaitConditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudformation.CloudFormationCapabilities")
class CloudFormationCapabilities(enum.Enum):
    """(deprecated) Capabilities that affect whether CloudFormation is allowed to change IAM resources.

    :deprecated: use ``core.CfnCapabilities``

    :stability: deprecated
    """

    NONE = "NONE"
    """(deprecated) No IAM Capabilities.

    Pass this capability if you wish to block the creation IAM resources.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    ANONYMOUS_IAM = "ANONYMOUS_IAM"
    """(deprecated) Capability to create anonymous IAM resources.

    Pass this capability if you're only creating anonymous resources.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    NAMED_IAM = "NAMED_IAM"
    """(deprecated) Capability to create named IAM resources.

    Pass this capability if you're creating IAM resources that have physical
    names.

    ``CloudFormationCapabilities.NamedIAM`` implies ``CloudFormationCapabilities.IAM``; you don't have to pass both.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
    """
    AUTO_EXPAND = "AUTO_EXPAND"
    """(deprecated) Capability to run CloudFormation macros.

    Pass this capability if your template includes macros, for example AWS::Include or AWS::Serverless.

    :stability: deprecated
    :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStack.html
    """


class CustomResource(
    aws_cdk.core.CustomResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CustomResource",
):
    """(deprecated) Deprecated.

    :deprecated: use ``core.CustomResource``

    :stability: deprecated
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        provider: "ICustomResourceProvider",
        properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param provider: (deprecated) The provider which implements the custom resource. You can implement a provider by listening to raw AWS CloudFormation events through an SNS topic or an AWS Lambda function or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers:: // use the provider framework from aws-cdk/custom-resources: provider: new custom_resources.Provider({ onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); Example:: // invoke an AWS Lambda function when a lifecycle event occurs: provider: CustomResourceProvider.fromLambda(myFunction) Example:: // publish lifecycle events to an SNS topic: provider: CustomResourceProvider.fromTopic(myTopic)
        :param properties: (deprecated) Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: (deprecated) The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: (deprecated) For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        :stability: deprecated
        """
        props = CustomResourceProps(
            provider=provider,
            properties=properties,
            removal_policy=removal_policy,
            resource_type=resource_type,
        )

        jsii.create(CustomResource, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider": "provider",
        "properties": "properties",
        "removal_policy": "removalPolicy",
        "resource_type": "resourceType",
    },
)
class CustomResourceProps:
    def __init__(
        self,
        *,
        provider: "ICustomResourceProvider",
        properties: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties to provide a Lambda-backed custom resource.

        :param provider: (deprecated) The provider which implements the custom resource. You can implement a provider by listening to raw AWS CloudFormation events through an SNS topic or an AWS Lambda function or use the CDK's custom `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust providers:: // use the provider framework from aws-cdk/custom-resources: provider: new custom_resources.Provider({ onEventHandler: myOnEventLambda, isCompleteHandler: myIsCompleteLambda, // optional }); Example:: // invoke an AWS Lambda function when a lifecycle event occurs: provider: CustomResourceProvider.fromLambda(myFunction) Example:: // publish lifecycle events to an SNS topic: provider: CustomResourceProvider.fromTopic(myTopic)
        :param properties: (deprecated) Properties to pass to the Lambda. Default: - No properties.
        :param removal_policy: (deprecated) The policy to apply when this resource is removed from the application. Default: cdk.RemovalPolicy.Destroy
        :param resource_type: (deprecated) For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name. For example, you can use "Custom::MyCustomResourceTypeName". Custom resource type names must begin with "Custom::" and can include alphanumeric characters and the following characters: _@-. You can specify a custom resource type name up to a maximum length of 60 characters. You cannot change the type during an update. Using your own resource type names helps you quickly differentiate the types of custom resources in your stack. For example, if you had two custom resources that conduct two different ping tests, you could name their type as Custom::PingTester to make them easily identifiable as ping testers (instead of using AWS::CloudFormation::CustomResource). Default: - AWS::CloudFormation::CustomResource

        :deprecated: use ``core.CustomResourceProps``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "provider": provider,
        }
        if properties is not None:
            self._values["properties"] = properties
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if resource_type is not None:
            self._values["resource_type"] = resource_type

    @builtins.property
    def provider(self) -> "ICustomResourceProvider":
        """(deprecated) The provider which implements the custom resource.

        You can implement a provider by listening to raw AWS CloudFormation events
        through an SNS topic or an AWS Lambda function or use the CDK's custom
        `resource provider framework <https://docs.aws.amazon.com/cdk/api/latest/docs/custom-resources-readme.html>`_ which makes it easier to implement robust
        providers::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           provider: new custom_resources.Provider({
              onEventHandler: myOnEventLambda,
              isCompleteHandler: myIsCompleteLambda, // optional
           });

        Example::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           provider: CustomResourceProvider.fromLambda(myFunction)

        Example::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           provider: CustomResourceProvider.fromTopic(myTopic)

        :stability: deprecated
        """
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return result

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """(deprecated) Properties to pass to the Lambda.

        :default: - No properties.

        :stability: deprecated
        """
        result = self._values.get("properties")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """(deprecated) The policy to apply when this resource is removed from the application.

        :default: cdk.RemovalPolicy.Destroy

        :stability: deprecated
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        """(deprecated) For custom resources, you can specify AWS::CloudFormation::CustomResource (the default) as the resource type, or you can specify your own resource type name.

        For example, you can use "Custom::MyCustomResourceTypeName".

        Custom resource type names must begin with "Custom::" and can include
        alphanumeric characters and the following characters: _@-. You can specify
        a custom resource type name up to a maximum length of 60 characters. You
        cannot change the type during an update.

        Using your own resource type names helps you quickly differentiate the
        types of custom resources in your stack. For example, if you had two custom
        resources that conduct two different ping tests, you could name their type
        as Custom::PingTester to make them easily identifiable as ping testers
        (instead of using AWS::CloudFormation::CustomResource).

        :default: - AWS::CloudFormation::CustomResource

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html#aws-cfn-resource-type-name
        :stability: deprecated
        """
        result = self._values.get("resource_type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"service_token": "serviceToken"},
)
class CustomResourceProviderConfig:
    def __init__(self, *, service_token: builtins.str) -> None:
        """(deprecated) Configuration options for custom resource providers.

        :param service_token: (deprecated) The ARN of the SNS topic or the AWS Lambda function which implements this provider.

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "service_token": service_token,
        }

    @builtins.property
    def service_token(self) -> builtins.str:
        """(deprecated) The ARN of the SNS topic or the AWS Lambda function which implements this provider.

        :stability: deprecated
        """
        result = self._values.get("service_token")
        assert result is not None, "Required property 'service_token' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomResourceProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cloudformation.ICustomResourceProvider")
class ICustomResourceProvider(typing_extensions.Protocol):
    """(deprecated) Represents a provider for an AWS CloudFormation custom resources.

    :deprecated: use ``core.ICustomResourceProvider``

    :stability: deprecated
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICustomResourceProviderProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> CustomResourceProviderConfig:
        """(deprecated) Called when this provider is used by a ``CustomResource``.

        :param scope: The resource that uses this provider.

        :return: provider configuration

        :stability: deprecated
        """
        ...


class _ICustomResourceProviderProxy:
    """(deprecated) Represents a provider for an AWS CloudFormation custom resources.

    :deprecated: use ``core.ICustomResourceProvider``

    :stability: deprecated
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudformation.ICustomResourceProvider"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct) -> CustomResourceProviderConfig:
        """(deprecated) Called when this provider is used by a ``CustomResource``.

        :param scope: The resource that uses this provider.

        :return: provider configuration

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [scope])


class NestedStack(
    aws_cdk.core.NestedStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.NestedStack",
):
    """(experimental) A CloudFormation nested stack.

    When you apply template changes to update a top-level stack, CloudFormation
    updates the top-level stack and initiates an update to its nested stacks.
    CloudFormation updates the resources of modified nested stacks, but does not
    update the resources of unmodified nested stacks.

    Furthermore, this stack will not be treated as an independent deployment
    artifact (won't be listed in "cdk list" or deployable through "cdk deploy"),
    but rather only synthesized as a template and uploaded as an asset to S3.

    Cross references of resource attributes between the parent stack and the
    nested stack will automatically be translated to stack parameters and
    outputs.

    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        notifications: typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param notifications: (experimental) The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: (experimental) The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: (experimental) The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        :stability: experimental
        """
        props = NestedStackProps(
            notifications=notifications, parameters=parameters, timeout=timeout
        )

        jsii.create(NestedStack, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudformation.NestedStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "notifications": "notifications",
        "parameters": "parameters",
        "timeout": "timeout",
    },
)
class NestedStackProps:
    def __init__(
        self,
        *,
        notifications: typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(experimental) Initialization props for the ``NestedStack`` construct.

        :param notifications: (experimental) The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: (experimental) The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param timeout: (experimental) The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if notifications is not None:
            self._values["notifications"] = notifications
        if parameters is not None:
            self._values["parameters"] = parameters
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[aws_cdk.aws_sns.ITopic]]:
        """(experimental) The Simple Notification Service (SNS) topics to publish stack related events.

        :default: - notifications are not sent for this stack.

        :stability: experimental
        """
        result = self._values.get("notifications")
        return result

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding
        to a parameter defined in the embedded template and a value representing
        the value that you want to set for the parameter.

        The nested stack construct will automatically synthesize parameters in order
        to bind references from the parent stack(s) into the nested stack.

        :default: - no user-defined parameters are passed to the nested stack

        :stability: experimental
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state.

        When CloudFormation detects that the nested stack has reached the
        CREATE_COMPLETE state, it marks the nested stack resource as
        CREATE_COMPLETE in the parent stack and resumes creating the parent stack.
        If the timeout period expires before the nested stack reaches
        CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls
        back both the nested stack and parent stack.

        :default: - no timeout

        :stability: experimental
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NestedStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICustomResourceProvider)
class CustomResourceProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudformation.CustomResourceProvider",
):
    """(deprecated) Represents a provider for an AWS CloudFormation custom resources.

    :stability: deprecated
    """

    @jsii.member(jsii_name="fromLambda")
    @builtins.classmethod
    def from_lambda(
        cls,
        handler: aws_cdk.aws_lambda.IFunction,
    ) -> "CustomResourceProvider":
        """(deprecated) The Lambda provider that implements this custom resource.

        We recommend using a lambda.SingletonFunction for this.

        :param handler: -

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "fromLambda", [handler])

    @jsii.member(jsii_name="fromTopic")
    @builtins.classmethod
    def from_topic(cls, topic: aws_cdk.aws_sns.ITopic) -> "CustomResourceProvider":
        """(deprecated) The SNS Topic for the provider that implements this custom resource.

        :param topic: -

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "fromTopic", [topic])

    @jsii.member(jsii_name="lambda")
    @builtins.classmethod
    def lambda_(cls, handler: aws_cdk.aws_lambda.IFunction) -> "CustomResourceProvider":
        """(deprecated) Use AWS Lambda as a provider.

        :param handler: -

        :deprecated: use ``fromLambda``

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "lambda", [handler])

    @jsii.member(jsii_name="topic")
    @builtins.classmethod
    def topic(cls, topic: aws_cdk.aws_sns.ITopic) -> "CustomResourceProvider":
        """(deprecated) Use an SNS topic as the provider.

        :param topic: -

        :deprecated: use ``fromTopic``

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "topic", [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, _: aws_cdk.core.Construct) -> CustomResourceProviderConfig:
        """(deprecated) Called when this provider is used by a ``CustomResource``.

        :param _: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        """(deprecated) the ServiceToken which contains the ARN for this provider.

        :stability: deprecated
        """
        return jsii.get(self, "serviceToken")


__all__ = [
    "CfnCustomResource",
    "CfnCustomResourceProps",
    "CfnMacro",
    "CfnMacroProps",
    "CfnStack",
    "CfnStackProps",
    "CfnStackSet",
    "CfnStackSetProps",
    "CfnWaitCondition",
    "CfnWaitConditionHandle",
    "CfnWaitConditionProps",
    "CloudFormationCapabilities",
    "CustomResource",
    "CustomResourceProps",
    "CustomResourceProvider",
    "CustomResourceProviderConfig",
    "ICustomResourceProvider",
    "NestedStack",
    "NestedStackProps",
]

publication.publish()
