"""
## AWS Systems Manager Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

### Installation

Install the module:

```console
$ npm i @aws-cdk/aws-ssm
```

Import it into your code:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ssm as ssm
```

### Using existing SSM Parameters in your CDK app

You can reference existing SSM Parameter Store values that you want to use in
your CDK app by using `ssm.ParameterStoreString`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Retrieve the latest value of the non-secret parameter
# with name "/My/String/Parameter".
string_value = ssm.StringParameter.from_string_parameter_attributes(self, "MyValue",
    parameter_name="/My/Public/Parameter"
).string_value

# Retrieve a specific version of the secret (SecureString) parameter.
# 'version' is always required.
secret_value = ssm.StringParameter.from_secure_string_parameter_attributes(self, "MySecureValue",
    parameter_name="/My/Secret/Parameter",
    version=5
)
```

### Creating new SSM Parameters in your CDK app

You can create either `ssm.StringParameter` or `ssm.StringListParameter`s in
a CDK app. These are public (not secret) values. Parameters of type
*SecretString* cannot be created directly from a CDK application; if you want
to provision secrets automatically, use Secrets Manager Secrets (see the
`@aws-cdk/aws-secretsmanager` package).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ssm.StringParameter(stack, "Parameter",
    allowed_pattern=".*",
    description="The value Foo",
    parameter_name="FooParameter",
    string_value="Foo",
    tier=ssm.ParameterTier.ADVANCED
)
```

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a new SSM Parameter holding a String
param = ssm.StringParameter(stack, "StringParameter",
    # description: 'Some user-friendly description',
    # name: 'ParameterName',
    string_value="Initial parameter value"
)

# Grant read access to some Role
param.grant_read(role)

# Create a new SSM Parameter holding a StringList
list_parameter = ssm.StringListParameter(stack, "StringListParameter",
    # description: 'Some user-friendly description',
    # name: 'ParameterName',
    string_list_value=["Initial parameter value A", "Initial parameter value B"]
)
```

When specifying an `allowedPattern`, the values provided as string literals
are validated against the pattern and an exception is raised if a value
provided does not comply.
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
import aws_cdk.aws_kms
import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAssociation(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnAssociation",
):
    """A CloudFormation ``AWS::SSM::Association``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html
    :cloudformationResource: AWS::SSM::Association
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        apply_only_at_cron_interval: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        association_name: typing.Optional[builtins.str] = None,
        automation_target_parameter_name: typing.Optional[builtins.str] = None,
        compliance_severity: typing.Optional[builtins.str] = None,
        document_version: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[builtins.str] = None,
        max_errors: typing.Optional[builtins.str] = None,
        output_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.InstanceAssociationOutputLocationProperty"]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        sync_compliance: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.TargetProperty"]]]] = None,
        wait_for_success_timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Create a new ``AWS::SSM::Association``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::SSM::Association.Name``.
        :param apply_only_at_cron_interval: ``AWS::SSM::Association.ApplyOnlyAtCronInterval``.
        :param association_name: ``AWS::SSM::Association.AssociationName``.
        :param automation_target_parameter_name: ``AWS::SSM::Association.AutomationTargetParameterName``.
        :param compliance_severity: ``AWS::SSM::Association.ComplianceSeverity``.
        :param document_version: ``AWS::SSM::Association.DocumentVersion``.
        :param instance_id: ``AWS::SSM::Association.InstanceId``.
        :param max_concurrency: ``AWS::SSM::Association.MaxConcurrency``.
        :param max_errors: ``AWS::SSM::Association.MaxErrors``.
        :param output_location: ``AWS::SSM::Association.OutputLocation``.
        :param parameters: ``AWS::SSM::Association.Parameters``.
        :param schedule_expression: ``AWS::SSM::Association.ScheduleExpression``.
        :param sync_compliance: ``AWS::SSM::Association.SyncCompliance``.
        :param targets: ``AWS::SSM::Association.Targets``.
        :param wait_for_success_timeout_seconds: ``AWS::SSM::Association.WaitForSuccessTimeoutSeconds``.
        """
        props = CfnAssociationProps(
            name=name,
            apply_only_at_cron_interval=apply_only_at_cron_interval,
            association_name=association_name,
            automation_target_parameter_name=automation_target_parameter_name,
            compliance_severity=compliance_severity,
            document_version=document_version,
            instance_id=instance_id,
            max_concurrency=max_concurrency,
            max_errors=max_errors,
            output_location=output_location,
            parameters=parameters,
            schedule_expression=schedule_expression,
            sync_compliance=sync_compliance,
            targets=targets,
            wait_for_success_timeout_seconds=wait_for_success_timeout_seconds,
        )

        jsii.create(CfnAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAssociationId")
    def attr_association_id(self) -> builtins.str:
        """
        :cloudformationAttribute: AssociationId
        """
        return jsii.get(self, "attrAssociationId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::SSM::Association.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="applyOnlyAtCronInterval")
    def apply_only_at_cron_interval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::SSM::Association.ApplyOnlyAtCronInterval``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-applyonlyatcroninterval
        """
        return jsii.get(self, "applyOnlyAtCronInterval")

    @apply_only_at_cron_interval.setter # type: ignore
    def apply_only_at_cron_interval(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "applyOnlyAtCronInterval", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="associationName")
    def association_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.AssociationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-associationname
        """
        return jsii.get(self, "associationName")

    @association_name.setter # type: ignore
    def association_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "associationName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="automationTargetParameterName")
    def automation_target_parameter_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.AutomationTargetParameterName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-automationtargetparametername
        """
        return jsii.get(self, "automationTargetParameterName")

    @automation_target_parameter_name.setter # type: ignore
    def automation_target_parameter_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "automationTargetParameterName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="complianceSeverity")
    def compliance_severity(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.ComplianceSeverity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-complianceseverity
        """
        return jsii.get(self, "complianceSeverity")

    @compliance_severity.setter # type: ignore
    def compliance_severity(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "complianceSeverity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="documentVersion")
    def document_version(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.DocumentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-documentversion
        """
        return jsii.get(self, "documentVersion")

    @document_version.setter # type: ignore
    def document_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "documentVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.InstanceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-instanceid
        """
        return jsii.get(self, "instanceId")

    @instance_id.setter # type: ignore
    def instance_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "instanceId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxConcurrency")
    def max_concurrency(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.MaxConcurrency``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-maxconcurrency
        """
        return jsii.get(self, "maxConcurrency")

    @max_concurrency.setter # type: ignore
    def max_concurrency(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "maxConcurrency", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxErrors")
    def max_errors(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.MaxErrors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-maxerrors
        """
        return jsii.get(self, "maxErrors")

    @max_errors.setter # type: ignore
    def max_errors(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "maxErrors", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outputLocation")
    def output_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.InstanceAssociationOutputLocationProperty"]]:
        """``AWS::SSM::Association.OutputLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-outputlocation
        """
        return jsii.get(self, "outputLocation")

    @output_location.setter # type: ignore
    def output_location(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.InstanceAssociationOutputLocationProperty"]],
    ) -> None:
        jsii.set(self, "outputLocation", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]]:
        """``AWS::SSM::Association.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter # type: ignore
    def parameters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]],
    ) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.ScheduleExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-scheduleexpression
        """
        return jsii.get(self, "scheduleExpression")

    @schedule_expression.setter # type: ignore
    def schedule_expression(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scheduleExpression", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="syncCompliance")
    def sync_compliance(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.SyncCompliance``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-synccompliance
        """
        return jsii.get(self, "syncCompliance")

    @sync_compliance.setter # type: ignore
    def sync_compliance(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "syncCompliance", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.TargetProperty"]]]]:
        """``AWS::SSM::Association.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-targets
        """
        return jsii.get(self, "targets")

    @targets.setter # type: ignore
    def targets(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.TargetProperty"]]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="waitForSuccessTimeoutSeconds")
    def wait_for_success_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SSM::Association.WaitForSuccessTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-waitforsuccesstimeoutseconds
        """
        return jsii.get(self, "waitForSuccessTimeoutSeconds")

    @wait_for_success_timeout_seconds.setter # type: ignore
    def wait_for_success_timeout_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "waitForSuccessTimeoutSeconds", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnAssociation.InstanceAssociationOutputLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_location": "s3Location"},
    )
    class InstanceAssociationOutputLocationProperty:
        def __init__(
            self,
            *,
            s3_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.S3OutputLocationProperty"]] = None,
        ) -> None:
            """
            :param s3_location: ``CfnAssociation.InstanceAssociationOutputLocationProperty.S3Location``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-instanceassociationoutputlocation.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def s3_location(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssociation.S3OutputLocationProperty"]]:
            """``CfnAssociation.InstanceAssociationOutputLocationProperty.S3Location``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-instanceassociationoutputlocation.html#cfn-ssm-association-instanceassociationoutputlocation-s3location
            """
            result = self._values.get("s3_location")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceAssociationOutputLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnAssociation.ParameterValuesProperty",
        jsii_struct_bases=[],
        name_mapping={"parameter_values": "parameterValues"},
    )
    class ParameterValuesProperty:
        def __init__(
            self,
            *,
            parameter_values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param parameter_values: ``CfnAssociation.ParameterValuesProperty.ParameterValues``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-parametervalues.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if parameter_values is not None:
                self._values["parameter_values"] = parameter_values

        @builtins.property
        def parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnAssociation.ParameterValuesProperty.ParameterValues``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-parametervalues.html#cfn-ssm-association-parametervalues-parametervalues
            """
            result = self._values.get("parameter_values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnAssociation.S3OutputLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "output_s3_bucket_name": "outputS3BucketName",
            "output_s3_key_prefix": "outputS3KeyPrefix",
            "output_s3_region": "outputS3Region",
        },
    )
    class S3OutputLocationProperty:
        def __init__(
            self,
            *,
            output_s3_bucket_name: typing.Optional[builtins.str] = None,
            output_s3_key_prefix: typing.Optional[builtins.str] = None,
            output_s3_region: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param output_s3_bucket_name: ``CfnAssociation.S3OutputLocationProperty.OutputS3BucketName``.
            :param output_s3_key_prefix: ``CfnAssociation.S3OutputLocationProperty.OutputS3KeyPrefix``.
            :param output_s3_region: ``CfnAssociation.S3OutputLocationProperty.OutputS3Region``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if output_s3_bucket_name is not None:
                self._values["output_s3_bucket_name"] = output_s3_bucket_name
            if output_s3_key_prefix is not None:
                self._values["output_s3_key_prefix"] = output_s3_key_prefix
            if output_s3_region is not None:
                self._values["output_s3_region"] = output_s3_region

        @builtins.property
        def output_s3_bucket_name(self) -> typing.Optional[builtins.str]:
            """``CfnAssociation.S3OutputLocationProperty.OutputS3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html#cfn-ssm-association-s3outputlocation-outputs3bucketname
            """
            result = self._values.get("output_s3_bucket_name")
            return result

        @builtins.property
        def output_s3_key_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnAssociation.S3OutputLocationProperty.OutputS3KeyPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html#cfn-ssm-association-s3outputlocation-outputs3keyprefix
            """
            result = self._values.get("output_s3_key_prefix")
            return result

        @builtins.property
        def output_s3_region(self) -> typing.Optional[builtins.str]:
            """``CfnAssociation.S3OutputLocationProperty.OutputS3Region``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html#cfn-ssm-association-s3outputlocation-outputs3region
            """
            result = self._values.get("output_s3_region")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnAssociation.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            values: typing.List[builtins.str],
        ) -> None:
            """
            :param key: ``CfnAssociation.TargetProperty.Key``.
            :param values: ``CfnAssociation.TargetProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-target.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "values": values,
            }

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnAssociation.TargetProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-target.html#cfn-ssm-association-target-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def values(self) -> typing.List[builtins.str]:
            """``CfnAssociation.TargetProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-target.html#cfn-ssm-association-target-values
            """
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
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
    jsii_type="@aws-cdk/aws-ssm.CfnAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "apply_only_at_cron_interval": "applyOnlyAtCronInterval",
        "association_name": "associationName",
        "automation_target_parameter_name": "automationTargetParameterName",
        "compliance_severity": "complianceSeverity",
        "document_version": "documentVersion",
        "instance_id": "instanceId",
        "max_concurrency": "maxConcurrency",
        "max_errors": "maxErrors",
        "output_location": "outputLocation",
        "parameters": "parameters",
        "schedule_expression": "scheduleExpression",
        "sync_compliance": "syncCompliance",
        "targets": "targets",
        "wait_for_success_timeout_seconds": "waitForSuccessTimeoutSeconds",
    },
)
class CfnAssociationProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        apply_only_at_cron_interval: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        association_name: typing.Optional[builtins.str] = None,
        automation_target_parameter_name: typing.Optional[builtins.str] = None,
        compliance_severity: typing.Optional[builtins.str] = None,
        document_version: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[builtins.str] = None,
        max_errors: typing.Optional[builtins.str] = None,
        output_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssociation.InstanceAssociationOutputLocationProperty]] = None,
        parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        sync_compliance: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAssociation.TargetProperty]]]] = None,
        wait_for_success_timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::Association``.

        :param name: ``AWS::SSM::Association.Name``.
        :param apply_only_at_cron_interval: ``AWS::SSM::Association.ApplyOnlyAtCronInterval``.
        :param association_name: ``AWS::SSM::Association.AssociationName``.
        :param automation_target_parameter_name: ``AWS::SSM::Association.AutomationTargetParameterName``.
        :param compliance_severity: ``AWS::SSM::Association.ComplianceSeverity``.
        :param document_version: ``AWS::SSM::Association.DocumentVersion``.
        :param instance_id: ``AWS::SSM::Association.InstanceId``.
        :param max_concurrency: ``AWS::SSM::Association.MaxConcurrency``.
        :param max_errors: ``AWS::SSM::Association.MaxErrors``.
        :param output_location: ``AWS::SSM::Association.OutputLocation``.
        :param parameters: ``AWS::SSM::Association.Parameters``.
        :param schedule_expression: ``AWS::SSM::Association.ScheduleExpression``.
        :param sync_compliance: ``AWS::SSM::Association.SyncCompliance``.
        :param targets: ``AWS::SSM::Association.Targets``.
        :param wait_for_success_timeout_seconds: ``AWS::SSM::Association.WaitForSuccessTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if apply_only_at_cron_interval is not None:
            self._values["apply_only_at_cron_interval"] = apply_only_at_cron_interval
        if association_name is not None:
            self._values["association_name"] = association_name
        if automation_target_parameter_name is not None:
            self._values["automation_target_parameter_name"] = automation_target_parameter_name
        if compliance_severity is not None:
            self._values["compliance_severity"] = compliance_severity
        if document_version is not None:
            self._values["document_version"] = document_version
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if max_errors is not None:
            self._values["max_errors"] = max_errors
        if output_location is not None:
            self._values["output_location"] = output_location
        if parameters is not None:
            self._values["parameters"] = parameters
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if sync_compliance is not None:
            self._values["sync_compliance"] = sync_compliance
        if targets is not None:
            self._values["targets"] = targets
        if wait_for_success_timeout_seconds is not None:
            self._values["wait_for_success_timeout_seconds"] = wait_for_success_timeout_seconds

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::SSM::Association.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def apply_only_at_cron_interval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::SSM::Association.ApplyOnlyAtCronInterval``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-applyonlyatcroninterval
        """
        result = self._values.get("apply_only_at_cron_interval")
        return result

    @builtins.property
    def association_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.AssociationName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-associationname
        """
        result = self._values.get("association_name")
        return result

    @builtins.property
    def automation_target_parameter_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.AutomationTargetParameterName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-automationtargetparametername
        """
        result = self._values.get("automation_target_parameter_name")
        return result

    @builtins.property
    def compliance_severity(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.ComplianceSeverity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-complianceseverity
        """
        result = self._values.get("compliance_severity")
        return result

    @builtins.property
    def document_version(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.DocumentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-documentversion
        """
        result = self._values.get("document_version")
        return result

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.InstanceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-instanceid
        """
        result = self._values.get("instance_id")
        return result

    @builtins.property
    def max_concurrency(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.MaxConcurrency``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-maxconcurrency
        """
        result = self._values.get("max_concurrency")
        return result

    @builtins.property
    def max_errors(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.MaxErrors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-maxerrors
        """
        result = self._values.get("max_errors")
        return result

    @builtins.property
    def output_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssociation.InstanceAssociationOutputLocationProperty]]:
        """``AWS::SSM::Association.OutputLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-outputlocation
        """
        result = self._values.get("output_location")
        return result

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]]:
        """``AWS::SSM::Association.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-parameters
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.ScheduleExpression``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-scheduleexpression
        """
        result = self._values.get("schedule_expression")
        return result

    @builtins.property
    def sync_compliance(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Association.SyncCompliance``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-synccompliance
        """
        result = self._values.get("sync_compliance")
        return result

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAssociation.TargetProperty]]]]:
        """``AWS::SSM::Association.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-targets
        """
        result = self._values.get("targets")
        return result

    @builtins.property
    def wait_for_success_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::SSM::Association.WaitForSuccessTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-waitforsuccesstimeoutseconds
        """
        result = self._values.get("wait_for_success_timeout_seconds")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDocument(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnDocument",
):
    """A CloudFormation ``AWS::SSM::Document``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html
    :cloudformationResource: AWS::SSM::Document
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        content: typing.Any,
        document_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::SSM::Document``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: ``AWS::SSM::Document.Content``.
        :param document_type: ``AWS::SSM::Document.DocumentType``.
        :param name: ``AWS::SSM::Document.Name``.
        :param tags: ``AWS::SSM::Document.Tags``.
        """
        props = CfnDocumentProps(
            content=content, document_type=document_type, name=name, tags=tags
        )

        jsii.create(CfnDocument, self, [scope, id, props])

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
        """``AWS::SSM::Document.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="content")
    def content(self) -> typing.Any:
        """``AWS::SSM::Document.Content``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-content
        """
        return jsii.get(self, "content")

    @content.setter # type: ignore
    def content(self, value: typing.Any) -> None:
        jsii.set(self, "content", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="documentType")
    def document_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Document.DocumentType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-documenttype
        """
        return jsii.get(self, "documentType")

    @document_type.setter # type: ignore
    def document_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "documentType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Document.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CfnDocumentProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "document_type": "documentType",
        "name": "name",
        "tags": "tags",
    },
)
class CfnDocumentProps:
    def __init__(
        self,
        *,
        content: typing.Any,
        document_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::Document``.

        :param content: ``AWS::SSM::Document.Content``.
        :param document_type: ``AWS::SSM::Document.DocumentType``.
        :param name: ``AWS::SSM::Document.Name``.
        :param tags: ``AWS::SSM::Document.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "content": content,
        }
        if document_type is not None:
            self._values["document_type"] = document_type
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> typing.Any:
        """``AWS::SSM::Document.Content``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-content
        """
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return result

    @builtins.property
    def document_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Document.DocumentType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-documenttype
        """
        result = self._values.get("document_type")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Document.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SSM::Document.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDocumentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMaintenanceWindow(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindow",
):
    """A CloudFormation ``AWS::SSM::MaintenanceWindow``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html
    :cloudformationResource: AWS::SSM::MaintenanceWindow
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        allow_unassociated_targets: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        cutoff: jsii.Number,
        duration: jsii.Number,
        name: builtins.str,
        schedule: builtins.str,
        description: typing.Optional[builtins.str] = None,
        end_date: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        schedule_timezone: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::SSM::MaintenanceWindow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param allow_unassociated_targets: ``AWS::SSM::MaintenanceWindow.AllowUnassociatedTargets``.
        :param cutoff: ``AWS::SSM::MaintenanceWindow.Cutoff``.
        :param duration: ``AWS::SSM::MaintenanceWindow.Duration``.
        :param name: ``AWS::SSM::MaintenanceWindow.Name``.
        :param schedule: ``AWS::SSM::MaintenanceWindow.Schedule``.
        :param description: ``AWS::SSM::MaintenanceWindow.Description``.
        :param end_date: ``AWS::SSM::MaintenanceWindow.EndDate``.
        :param schedule_offset: ``AWS::SSM::MaintenanceWindow.ScheduleOffset``.
        :param schedule_timezone: ``AWS::SSM::MaintenanceWindow.ScheduleTimezone``.
        :param start_date: ``AWS::SSM::MaintenanceWindow.StartDate``.
        :param tags: ``AWS::SSM::MaintenanceWindow.Tags``.
        """
        props = CfnMaintenanceWindowProps(
            allow_unassociated_targets=allow_unassociated_targets,
            cutoff=cutoff,
            duration=duration,
            name=name,
            schedule=schedule,
            description=description,
            end_date=end_date,
            schedule_offset=schedule_offset,
            schedule_timezone=schedule_timezone,
            start_date=start_date,
            tags=tags,
        )

        jsii.create(CfnMaintenanceWindow, self, [scope, id, props])

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
        """``AWS::SSM::MaintenanceWindow.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowUnassociatedTargets")
    def allow_unassociated_targets(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::SSM::MaintenanceWindow.AllowUnassociatedTargets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-allowunassociatedtargets
        """
        return jsii.get(self, "allowUnassociatedTargets")

    @allow_unassociated_targets.setter # type: ignore
    def allow_unassociated_targets(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "allowUnassociatedTargets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cutoff")
    def cutoff(self) -> jsii.Number:
        """``AWS::SSM::MaintenanceWindow.Cutoff``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-cutoff
        """
        return jsii.get(self, "cutoff")

    @cutoff.setter # type: ignore
    def cutoff(self, value: jsii.Number) -> None:
        jsii.set(self, "cutoff", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        """``AWS::SSM::MaintenanceWindow.Duration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-duration
        """
        return jsii.get(self, "duration")

    @duration.setter # type: ignore
    def duration(self, value: jsii.Number) -> None:
        jsii.set(self, "duration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindow.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindow.Schedule``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-schedule
        """
        return jsii.get(self, "schedule")

    @schedule.setter # type: ignore
    def schedule(self, value: builtins.str) -> None:
        jsii.set(self, "schedule", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.EndDate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-enddate
        """
        return jsii.get(self, "endDate")

    @end_date.setter # type: ignore
    def end_date(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "endDate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scheduleOffset")
    def schedule_offset(self) -> typing.Optional[jsii.Number]:
        """``AWS::SSM::MaintenanceWindow.ScheduleOffset``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-scheduleoffset
        """
        return jsii.get(self, "scheduleOffset")

    @schedule_offset.setter # type: ignore
    def schedule_offset(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "scheduleOffset", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scheduleTimezone")
    def schedule_timezone(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.ScheduleTimezone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-scheduletimezone
        """
        return jsii.get(self, "scheduleTimezone")

    @schedule_timezone.setter # type: ignore
    def schedule_timezone(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scheduleTimezone", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="startDate")
    def start_date(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.StartDate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-startdate
        """
        return jsii.get(self, "startDate")

    @start_date.setter # type: ignore
    def start_date(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "startDate", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_unassociated_targets": "allowUnassociatedTargets",
        "cutoff": "cutoff",
        "duration": "duration",
        "name": "name",
        "schedule": "schedule",
        "description": "description",
        "end_date": "endDate",
        "schedule_offset": "scheduleOffset",
        "schedule_timezone": "scheduleTimezone",
        "start_date": "startDate",
        "tags": "tags",
    },
)
class CfnMaintenanceWindowProps:
    def __init__(
        self,
        *,
        allow_unassociated_targets: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        cutoff: jsii.Number,
        duration: jsii.Number,
        name: builtins.str,
        schedule: builtins.str,
        description: typing.Optional[builtins.str] = None,
        end_date: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        schedule_timezone: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::MaintenanceWindow``.

        :param allow_unassociated_targets: ``AWS::SSM::MaintenanceWindow.AllowUnassociatedTargets``.
        :param cutoff: ``AWS::SSM::MaintenanceWindow.Cutoff``.
        :param duration: ``AWS::SSM::MaintenanceWindow.Duration``.
        :param name: ``AWS::SSM::MaintenanceWindow.Name``.
        :param schedule: ``AWS::SSM::MaintenanceWindow.Schedule``.
        :param description: ``AWS::SSM::MaintenanceWindow.Description``.
        :param end_date: ``AWS::SSM::MaintenanceWindow.EndDate``.
        :param schedule_offset: ``AWS::SSM::MaintenanceWindow.ScheduleOffset``.
        :param schedule_timezone: ``AWS::SSM::MaintenanceWindow.ScheduleTimezone``.
        :param start_date: ``AWS::SSM::MaintenanceWindow.StartDate``.
        :param tags: ``AWS::SSM::MaintenanceWindow.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "allow_unassociated_targets": allow_unassociated_targets,
            "cutoff": cutoff,
            "duration": duration,
            "name": name,
            "schedule": schedule,
        }
        if description is not None:
            self._values["description"] = description
        if end_date is not None:
            self._values["end_date"] = end_date
        if schedule_offset is not None:
            self._values["schedule_offset"] = schedule_offset
        if schedule_timezone is not None:
            self._values["schedule_timezone"] = schedule_timezone
        if start_date is not None:
            self._values["start_date"] = start_date
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allow_unassociated_targets(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::SSM::MaintenanceWindow.AllowUnassociatedTargets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-allowunassociatedtargets
        """
        result = self._values.get("allow_unassociated_targets")
        assert result is not None, "Required property 'allow_unassociated_targets' is missing"
        return result

    @builtins.property
    def cutoff(self) -> jsii.Number:
        """``AWS::SSM::MaintenanceWindow.Cutoff``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-cutoff
        """
        result = self._values.get("cutoff")
        assert result is not None, "Required property 'cutoff' is missing"
        return result

    @builtins.property
    def duration(self) -> jsii.Number:
        """``AWS::SSM::MaintenanceWindow.Duration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-duration
        """
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindow.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def schedule(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindow.Schedule``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-schedule
        """
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.EndDate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-enddate
        """
        result = self._values.get("end_date")
        return result

    @builtins.property
    def schedule_offset(self) -> typing.Optional[jsii.Number]:
        """``AWS::SSM::MaintenanceWindow.ScheduleOffset``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-scheduleoffset
        """
        result = self._values.get("schedule_offset")
        return result

    @builtins.property
    def schedule_timezone(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.ScheduleTimezone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-scheduletimezone
        """
        result = self._values.get("schedule_timezone")
        return result

    @builtins.property
    def start_date(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindow.StartDate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-startdate
        """
        result = self._values.get("start_date")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SSM::MaintenanceWindow.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMaintenanceWindowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMaintenanceWindowTarget(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTarget",
):
    """A CloudFormation ``AWS::SSM::MaintenanceWindowTarget``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html
    :cloudformationResource: AWS::SSM::MaintenanceWindowTarget
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        resource_type: builtins.str,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTarget.TargetsProperty"]]],
        window_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner_information: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::SSM::MaintenanceWindowTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_type: ``AWS::SSM::MaintenanceWindowTarget.ResourceType``.
        :param targets: ``AWS::SSM::MaintenanceWindowTarget.Targets``.
        :param window_id: ``AWS::SSM::MaintenanceWindowTarget.WindowId``.
        :param description: ``AWS::SSM::MaintenanceWindowTarget.Description``.
        :param name: ``AWS::SSM::MaintenanceWindowTarget.Name``.
        :param owner_information: ``AWS::SSM::MaintenanceWindowTarget.OwnerInformation``.
        """
        props = CfnMaintenanceWindowTargetProps(
            resource_type=resource_type,
            targets=targets,
            window_id=window_id,
            description=description,
            name=name,
            owner_information=owner_information,
        )

        jsii.create(CfnMaintenanceWindowTarget, self, [scope, id, props])

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
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTarget.ResourceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-resourcetype
        """
        return jsii.get(self, "resourceType")

    @resource_type.setter # type: ignore
    def resource_type(self, value: builtins.str) -> None:
        jsii.set(self, "resourceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTarget.TargetsProperty"]]]:
        """``AWS::SSM::MaintenanceWindowTarget.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-targets
        """
        return jsii.get(self, "targets")

    @targets.setter # type: ignore
    def targets(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTarget.TargetsProperty"]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="windowId")
    def window_id(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTarget.WindowId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-windowid
        """
        return jsii.get(self, "windowId")

    @window_id.setter # type: ignore
    def window_id(self, value: builtins.str) -> None:
        jsii.set(self, "windowId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTarget.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTarget.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ownerInformation")
    def owner_information(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTarget.OwnerInformation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-ownerinformation
        """
        return jsii.get(self, "ownerInformation")

    @owner_information.setter # type: ignore
    def owner_information(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ownerInformation", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTarget.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param key: ``CfnMaintenanceWindowTarget.TargetsProperty.Key``.
            :param values: ``CfnMaintenanceWindowTarget.TargetsProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtarget-targets.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
            }
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnMaintenanceWindowTarget.TargetsProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtarget-targets.html#cfn-ssm-maintenancewindowtarget-targets-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnMaintenanceWindowTarget.TargetsProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtarget-targets.html#cfn-ssm-maintenancewindowtarget-targets-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTargetProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_type": "resourceType",
        "targets": "targets",
        "window_id": "windowId",
        "description": "description",
        "name": "name",
        "owner_information": "ownerInformation",
    },
)
class CfnMaintenanceWindowTargetProps:
    def __init__(
        self,
        *,
        resource_type: builtins.str,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTarget.TargetsProperty]]],
        window_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner_information: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::MaintenanceWindowTarget``.

        :param resource_type: ``AWS::SSM::MaintenanceWindowTarget.ResourceType``.
        :param targets: ``AWS::SSM::MaintenanceWindowTarget.Targets``.
        :param window_id: ``AWS::SSM::MaintenanceWindowTarget.WindowId``.
        :param description: ``AWS::SSM::MaintenanceWindowTarget.Description``.
        :param name: ``AWS::SSM::MaintenanceWindowTarget.Name``.
        :param owner_information: ``AWS::SSM::MaintenanceWindowTarget.OwnerInformation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "resource_type": resource_type,
            "targets": targets,
            "window_id": window_id,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if owner_information is not None:
            self._values["owner_information"] = owner_information

    @builtins.property
    def resource_type(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTarget.ResourceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-resourcetype
        """
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return result

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTarget.TargetsProperty]]]:
        """``AWS::SSM::MaintenanceWindowTarget.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-targets
        """
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return result

    @builtins.property
    def window_id(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTarget.WindowId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-windowid
        """
        result = self._values.get("window_id")
        assert result is not None, "Required property 'window_id' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTarget.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTarget.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def owner_information(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTarget.OwnerInformation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-ownerinformation
        """
        result = self._values.get("owner_information")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMaintenanceWindowTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMaintenanceWindowTask(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask",
):
    """A CloudFormation ``AWS::SSM::MaintenanceWindowTask``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html
    :cloudformationResource: AWS::SSM::MaintenanceWindowTask
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        max_concurrency: builtins.str,
        max_errors: builtins.str,
        priority: jsii.Number,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.TargetProperty"]]],
        task_arn: builtins.str,
        task_type: builtins.str,
        window_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        logging_info: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.LoggingInfoProperty"]] = None,
        name: typing.Optional[builtins.str] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        task_invocation_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.TaskInvocationParametersProperty"]] = None,
        task_parameters: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::SSM::MaintenanceWindowTask``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param max_concurrency: ``AWS::SSM::MaintenanceWindowTask.MaxConcurrency``.
        :param max_errors: ``AWS::SSM::MaintenanceWindowTask.MaxErrors``.
        :param priority: ``AWS::SSM::MaintenanceWindowTask.Priority``.
        :param targets: ``AWS::SSM::MaintenanceWindowTask.Targets``.
        :param task_arn: ``AWS::SSM::MaintenanceWindowTask.TaskArn``.
        :param task_type: ``AWS::SSM::MaintenanceWindowTask.TaskType``.
        :param window_id: ``AWS::SSM::MaintenanceWindowTask.WindowId``.
        :param description: ``AWS::SSM::MaintenanceWindowTask.Description``.
        :param logging_info: ``AWS::SSM::MaintenanceWindowTask.LoggingInfo``.
        :param name: ``AWS::SSM::MaintenanceWindowTask.Name``.
        :param service_role_arn: ``AWS::SSM::MaintenanceWindowTask.ServiceRoleArn``.
        :param task_invocation_parameters: ``AWS::SSM::MaintenanceWindowTask.TaskInvocationParameters``.
        :param task_parameters: ``AWS::SSM::MaintenanceWindowTask.TaskParameters``.
        """
        props = CfnMaintenanceWindowTaskProps(
            max_concurrency=max_concurrency,
            max_errors=max_errors,
            priority=priority,
            targets=targets,
            task_arn=task_arn,
            task_type=task_type,
            window_id=window_id,
            description=description,
            logging_info=logging_info,
            name=name,
            service_role_arn=service_role_arn,
            task_invocation_parameters=task_invocation_parameters,
            task_parameters=task_parameters,
        )

        jsii.create(CfnMaintenanceWindowTask, self, [scope, id, props])

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
    @jsii.member(jsii_name="maxConcurrency")
    def max_concurrency(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.MaxConcurrency``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-maxconcurrency
        """
        return jsii.get(self, "maxConcurrency")

    @max_concurrency.setter # type: ignore
    def max_concurrency(self, value: builtins.str) -> None:
        jsii.set(self, "maxConcurrency", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxErrors")
    def max_errors(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.MaxErrors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-maxerrors
        """
        return jsii.get(self, "maxErrors")

    @max_errors.setter # type: ignore
    def max_errors(self, value: builtins.str) -> None:
        jsii.set(self, "maxErrors", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        """``AWS::SSM::MaintenanceWindowTask.Priority``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-priority
        """
        return jsii.get(self, "priority")

    @priority.setter # type: ignore
    def priority(self, value: jsii.Number) -> None:
        jsii.set(self, "priority", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.TargetProperty"]]]:
        """``AWS::SSM::MaintenanceWindowTask.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-targets
        """
        return jsii.get(self, "targets")

    @targets.setter # type: ignore
    def targets(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.TargetProperty"]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskArn")
    def task_arn(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.TaskArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskarn
        """
        return jsii.get(self, "taskArn")

    @task_arn.setter # type: ignore
    def task_arn(self, value: builtins.str) -> None:
        jsii.set(self, "taskArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskParameters")
    def task_parameters(self) -> typing.Any:
        """``AWS::SSM::MaintenanceWindowTask.TaskParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskparameters
        """
        return jsii.get(self, "taskParameters")

    @task_parameters.setter # type: ignore
    def task_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "taskParameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskType")
    def task_type(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.TaskType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-tasktype
        """
        return jsii.get(self, "taskType")

    @task_type.setter # type: ignore
    def task_type(self, value: builtins.str) -> None:
        jsii.set(self, "taskType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="windowId")
    def window_id(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.WindowId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-windowid
        """
        return jsii.get(self, "windowId")

    @window_id.setter # type: ignore
    def window_id(self, value: builtins.str) -> None:
        jsii.set(self, "windowId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTask.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loggingInfo")
    def logging_info(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.LoggingInfoProperty"]]:
        """``AWS::SSM::MaintenanceWindowTask.LoggingInfo``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-logginginfo
        """
        return jsii.get(self, "loggingInfo")

    @logging_info.setter # type: ignore
    def logging_info(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.LoggingInfoProperty"]],
    ) -> None:
        jsii.set(self, "loggingInfo", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTask.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTask.ServiceRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-servicerolearn
        """
        return jsii.get(self, "serviceRoleArn")

    @service_role_arn.setter # type: ignore
    def service_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "serviceRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskInvocationParameters")
    def task_invocation_parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.TaskInvocationParametersProperty"]]:
        """``AWS::SSM::MaintenanceWindowTask.TaskInvocationParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters
        """
        return jsii.get(self, "taskInvocationParameters")

    @task_invocation_parameters.setter # type: ignore
    def task_invocation_parameters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.TaskInvocationParametersProperty"]],
    ) -> None:
        jsii.set(self, "taskInvocationParameters", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.LoggingInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "region": "region",
            "s3_bucket": "s3Bucket",
            "s3_prefix": "s3Prefix",
        },
    )
    class LoggingInfoProperty:
        def __init__(
            self,
            *,
            region: builtins.str,
            s3_bucket: builtins.str,
            s3_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param region: ``CfnMaintenanceWindowTask.LoggingInfoProperty.Region``.
            :param s3_bucket: ``CfnMaintenanceWindowTask.LoggingInfoProperty.S3Bucket``.
            :param s3_prefix: ``CfnMaintenanceWindowTask.LoggingInfoProperty.S3Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "region": region,
                "s3_bucket": s3_bucket,
            }
            if s3_prefix is not None:
                self._values["s3_prefix"] = s3_prefix

        @builtins.property
        def region(self) -> builtins.str:
            """``CfnMaintenanceWindowTask.LoggingInfoProperty.Region``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html#cfn-ssm-maintenancewindowtask-logginginfo-region
            """
            result = self._values.get("region")
            assert result is not None, "Required property 'region' is missing"
            return result

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            """``CfnMaintenanceWindowTask.LoggingInfoProperty.S3Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html#cfn-ssm-maintenancewindowtask-logginginfo-s3bucket
            """
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return result

        @builtins.property
        def s3_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.LoggingInfoProperty.S3Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html#cfn-ssm-maintenancewindowtask-logginginfo-s3prefix
            """
            result = self._values.get("s3_prefix")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_version": "documentVersion",
            "parameters": "parameters",
        },
    )
    class MaintenanceWindowAutomationParametersProperty:
        def __init__(
            self,
            *,
            document_version: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
        ) -> None:
            """
            :param document_version: ``CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty.DocumentVersion``.
            :param parameters: ``CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowautomationparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if document_version is not None:
                self._values["document_version"] = document_version
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def document_version(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty.DocumentVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowautomationparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowautomationparameters-documentversion
            """
            result = self._values.get("document_version")
            return result

        @builtins.property
        def parameters(self) -> typing.Any:
            """``CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowautomationparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowautomationparameters-parameters
            """
            result = self._values.get("parameters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowAutomationParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_context": "clientContext",
            "payload": "payload",
            "qualifier": "qualifier",
        },
    )
    class MaintenanceWindowLambdaParametersProperty:
        def __init__(
            self,
            *,
            client_context: typing.Optional[builtins.str] = None,
            payload: typing.Optional[builtins.str] = None,
            qualifier: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param client_context: ``CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty.ClientContext``.
            :param payload: ``CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty.Payload``.
            :param qualifier: ``CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty.Qualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if client_context is not None:
                self._values["client_context"] = client_context
            if payload is not None:
                self._values["payload"] = payload
            if qualifier is not None:
                self._values["qualifier"] = qualifier

        @builtins.property
        def client_context(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty.ClientContext``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowlambdaparameters-clientcontext
            """
            result = self._values.get("client_context")
            return result

        @builtins.property
        def payload(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty.Payload``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowlambdaparameters-payload
            """
            result = self._values.get("payload")
            return result

        @builtins.property
        def qualifier(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty.Qualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowlambdaparameters-qualifier
            """
            result = self._values.get("qualifier")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowLambdaParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comment": "comment",
            "document_hash": "documentHash",
            "document_hash_type": "documentHashType",
            "notification_config": "notificationConfig",
            "output_s3_bucket_name": "outputS3BucketName",
            "output_s3_key_prefix": "outputS3KeyPrefix",
            "parameters": "parameters",
            "service_role_arn": "serviceRoleArn",
            "timeout_seconds": "timeoutSeconds",
        },
    )
    class MaintenanceWindowRunCommandParametersProperty:
        def __init__(
            self,
            *,
            comment: typing.Optional[builtins.str] = None,
            document_hash: typing.Optional[builtins.str] = None,
            document_hash_type: typing.Optional[builtins.str] = None,
            notification_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.NotificationConfigProperty"]] = None,
            output_s3_bucket_name: typing.Optional[builtins.str] = None,
            output_s3_key_prefix: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            service_role_arn: typing.Optional[builtins.str] = None,
            timeout_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param comment: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.Comment``.
            :param document_hash: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.DocumentHash``.
            :param document_hash_type: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.DocumentHashType``.
            :param notification_config: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.NotificationConfig``.
            :param output_s3_bucket_name: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.OutputS3BucketName``.
            :param output_s3_key_prefix: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.OutputS3KeyPrefix``.
            :param parameters: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.Parameters``.
            :param service_role_arn: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.ServiceRoleArn``.
            :param timeout_seconds: ``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.TimeoutSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if comment is not None:
                self._values["comment"] = comment
            if document_hash is not None:
                self._values["document_hash"] = document_hash
            if document_hash_type is not None:
                self._values["document_hash_type"] = document_hash_type
            if notification_config is not None:
                self._values["notification_config"] = notification_config
            if output_s3_bucket_name is not None:
                self._values["output_s3_bucket_name"] = output_s3_bucket_name
            if output_s3_key_prefix is not None:
                self._values["output_s3_key_prefix"] = output_s3_key_prefix
            if parameters is not None:
                self._values["parameters"] = parameters
            if service_role_arn is not None:
                self._values["service_role_arn"] = service_role_arn
            if timeout_seconds is not None:
                self._values["timeout_seconds"] = timeout_seconds

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-comment
            """
            result = self._values.get("comment")
            return result

        @builtins.property
        def document_hash(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.DocumentHash``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-documenthash
            """
            result = self._values.get("document_hash")
            return result

        @builtins.property
        def document_hash_type(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.DocumentHashType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-documenthashtype
            """
            result = self._values.get("document_hash_type")
            return result

        @builtins.property
        def notification_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.NotificationConfigProperty"]]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.NotificationConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-notificationconfig
            """
            result = self._values.get("notification_config")
            return result

        @builtins.property
        def output_s3_bucket_name(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.OutputS3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-outputs3bucketname
            """
            result = self._values.get("output_s3_bucket_name")
            return result

        @builtins.property
        def output_s3_key_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.OutputS3KeyPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-outputs3keyprefix
            """
            result = self._values.get("output_s3_key_prefix")
            return result

        @builtins.property
        def parameters(self) -> typing.Any:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-parameters
            """
            result = self._values.get("parameters")
            return result

        @builtins.property
        def service_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.ServiceRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-servicerolearn
            """
            result = self._values.get("service_role_arn")
            return result

        @builtins.property
        def timeout_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty.TimeoutSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-timeoutseconds
            """
            result = self._values.get("timeout_seconds")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowRunCommandParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"input": "input", "name": "name"},
    )
    class MaintenanceWindowStepFunctionsParametersProperty:
        def __init__(
            self,
            *,
            input: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param input: ``CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty.Input``.
            :param name: ``CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if input is not None:
                self._values["input"] = input
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty.Input``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters-input
            """
            result = self._values.get("input")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters-name
            """
            result = self._values.get("name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowStepFunctionsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.NotificationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "notification_arn": "notificationArn",
            "notification_events": "notificationEvents",
            "notification_type": "notificationType",
        },
    )
    class NotificationConfigProperty:
        def __init__(
            self,
            *,
            notification_arn: builtins.str,
            notification_events: typing.Optional[typing.List[builtins.str]] = None,
            notification_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param notification_arn: ``CfnMaintenanceWindowTask.NotificationConfigProperty.NotificationArn``.
            :param notification_events: ``CfnMaintenanceWindowTask.NotificationConfigProperty.NotificationEvents``.
            :param notification_type: ``CfnMaintenanceWindowTask.NotificationConfigProperty.NotificationType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "notification_arn": notification_arn,
            }
            if notification_events is not None:
                self._values["notification_events"] = notification_events
            if notification_type is not None:
                self._values["notification_type"] = notification_type

        @builtins.property
        def notification_arn(self) -> builtins.str:
            """``CfnMaintenanceWindowTask.NotificationConfigProperty.NotificationArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html#cfn-ssm-maintenancewindowtask-notificationconfig-notificationarn
            """
            result = self._values.get("notification_arn")
            assert result is not None, "Required property 'notification_arn' is missing"
            return result

        @builtins.property
        def notification_events(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnMaintenanceWindowTask.NotificationConfigProperty.NotificationEvents``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html#cfn-ssm-maintenancewindowtask-notificationconfig-notificationevents
            """
            result = self._values.get("notification_events")
            return result

        @builtins.property
        def notification_type(self) -> typing.Optional[builtins.str]:
            """``CfnMaintenanceWindowTask.NotificationConfigProperty.NotificationType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html#cfn-ssm-maintenancewindowtask-notificationconfig-notificationtype
            """
            result = self._values.get("notification_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param key: ``CfnMaintenanceWindowTask.TargetProperty.Key``.
            :param values: ``CfnMaintenanceWindowTask.TargetProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-target.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
            }
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnMaintenanceWindowTask.TargetProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-target.html#cfn-ssm-maintenancewindowtask-target-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnMaintenanceWindowTask.TargetProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-target.html#cfn-ssm-maintenancewindowtask-target-values
            """
            result = self._values.get("values")
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
        jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTask.TaskInvocationParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maintenance_window_automation_parameters": "maintenanceWindowAutomationParameters",
            "maintenance_window_lambda_parameters": "maintenanceWindowLambdaParameters",
            "maintenance_window_run_command_parameters": "maintenanceWindowRunCommandParameters",
            "maintenance_window_step_functions_parameters": "maintenanceWindowStepFunctionsParameters",
        },
    )
    class TaskInvocationParametersProperty:
        def __init__(
            self,
            *,
            maintenance_window_automation_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty"]] = None,
            maintenance_window_lambda_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty"]] = None,
            maintenance_window_run_command_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty"]] = None,
            maintenance_window_step_functions_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty"]] = None,
        ) -> None:
            """
            :param maintenance_window_automation_parameters: ``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowAutomationParameters``.
            :param maintenance_window_lambda_parameters: ``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowLambdaParameters``.
            :param maintenance_window_run_command_parameters: ``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowRunCommandParameters``.
            :param maintenance_window_step_functions_parameters: ``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowStepFunctionsParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if maintenance_window_automation_parameters is not None:
                self._values["maintenance_window_automation_parameters"] = maintenance_window_automation_parameters
            if maintenance_window_lambda_parameters is not None:
                self._values["maintenance_window_lambda_parameters"] = maintenance_window_lambda_parameters
            if maintenance_window_run_command_parameters is not None:
                self._values["maintenance_window_run_command_parameters"] = maintenance_window_run_command_parameters
            if maintenance_window_step_functions_parameters is not None:
                self._values["maintenance_window_step_functions_parameters"] = maintenance_window_step_functions_parameters

        @builtins.property
        def maintenance_window_automation_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowAutomationParametersProperty"]]:
            """``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowAutomationParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowautomationparameters
            """
            result = self._values.get("maintenance_window_automation_parameters")
            return result

        @builtins.property
        def maintenance_window_lambda_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowLambdaParametersProperty"]]:
            """``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowLambdaParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowlambdaparameters
            """
            result = self._values.get("maintenance_window_lambda_parameters")
            return result

        @builtins.property
        def maintenance_window_run_command_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowRunCommandParametersProperty"]]:
            """``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowRunCommandParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowruncommandparameters
            """
            result = self._values.get("maintenance_window_run_command_parameters")
            return result

        @builtins.property
        def maintenance_window_step_functions_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnMaintenanceWindowTask.MaintenanceWindowStepFunctionsParametersProperty"]]:
            """``CfnMaintenanceWindowTask.TaskInvocationParametersProperty.MaintenanceWindowStepFunctionsParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowstepfunctionsparameters
            """
            result = self._values.get("maintenance_window_step_functions_parameters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskInvocationParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CfnMaintenanceWindowTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrency": "maxConcurrency",
        "max_errors": "maxErrors",
        "priority": "priority",
        "targets": "targets",
        "task_arn": "taskArn",
        "task_type": "taskType",
        "window_id": "windowId",
        "description": "description",
        "logging_info": "loggingInfo",
        "name": "name",
        "service_role_arn": "serviceRoleArn",
        "task_invocation_parameters": "taskInvocationParameters",
        "task_parameters": "taskParameters",
    },
)
class CfnMaintenanceWindowTaskProps:
    def __init__(
        self,
        *,
        max_concurrency: builtins.str,
        max_errors: builtins.str,
        priority: jsii.Number,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTask.TargetProperty]]],
        task_arn: builtins.str,
        task_type: builtins.str,
        window_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        logging_info: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTask.LoggingInfoProperty]] = None,
        name: typing.Optional[builtins.str] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        task_invocation_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTask.TaskInvocationParametersProperty]] = None,
        task_parameters: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::MaintenanceWindowTask``.

        :param max_concurrency: ``AWS::SSM::MaintenanceWindowTask.MaxConcurrency``.
        :param max_errors: ``AWS::SSM::MaintenanceWindowTask.MaxErrors``.
        :param priority: ``AWS::SSM::MaintenanceWindowTask.Priority``.
        :param targets: ``AWS::SSM::MaintenanceWindowTask.Targets``.
        :param task_arn: ``AWS::SSM::MaintenanceWindowTask.TaskArn``.
        :param task_type: ``AWS::SSM::MaintenanceWindowTask.TaskType``.
        :param window_id: ``AWS::SSM::MaintenanceWindowTask.WindowId``.
        :param description: ``AWS::SSM::MaintenanceWindowTask.Description``.
        :param logging_info: ``AWS::SSM::MaintenanceWindowTask.LoggingInfo``.
        :param name: ``AWS::SSM::MaintenanceWindowTask.Name``.
        :param service_role_arn: ``AWS::SSM::MaintenanceWindowTask.ServiceRoleArn``.
        :param task_invocation_parameters: ``AWS::SSM::MaintenanceWindowTask.TaskInvocationParameters``.
        :param task_parameters: ``AWS::SSM::MaintenanceWindowTask.TaskParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "max_concurrency": max_concurrency,
            "max_errors": max_errors,
            "priority": priority,
            "targets": targets,
            "task_arn": task_arn,
            "task_type": task_type,
            "window_id": window_id,
        }
        if description is not None:
            self._values["description"] = description
        if logging_info is not None:
            self._values["logging_info"] = logging_info
        if name is not None:
            self._values["name"] = name
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if task_invocation_parameters is not None:
            self._values["task_invocation_parameters"] = task_invocation_parameters
        if task_parameters is not None:
            self._values["task_parameters"] = task_parameters

    @builtins.property
    def max_concurrency(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.MaxConcurrency``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-maxconcurrency
        """
        result = self._values.get("max_concurrency")
        assert result is not None, "Required property 'max_concurrency' is missing"
        return result

    @builtins.property
    def max_errors(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.MaxErrors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-maxerrors
        """
        result = self._values.get("max_errors")
        assert result is not None, "Required property 'max_errors' is missing"
        return result

    @builtins.property
    def priority(self) -> jsii.Number:
        """``AWS::SSM::MaintenanceWindowTask.Priority``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-priority
        """
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return result

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTask.TargetProperty]]]:
        """``AWS::SSM::MaintenanceWindowTask.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-targets
        """
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return result

    @builtins.property
    def task_arn(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.TaskArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskarn
        """
        result = self._values.get("task_arn")
        assert result is not None, "Required property 'task_arn' is missing"
        return result

    @builtins.property
    def task_type(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.TaskType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-tasktype
        """
        result = self._values.get("task_type")
        assert result is not None, "Required property 'task_type' is missing"
        return result

    @builtins.property
    def window_id(self) -> builtins.str:
        """``AWS::SSM::MaintenanceWindowTask.WindowId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-windowid
        """
        result = self._values.get("window_id")
        assert result is not None, "Required property 'window_id' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTask.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def logging_info(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTask.LoggingInfoProperty]]:
        """``AWS::SSM::MaintenanceWindowTask.LoggingInfo``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-logginginfo
        """
        result = self._values.get("logging_info")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTask.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::MaintenanceWindowTask.ServiceRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-servicerolearn
        """
        result = self._values.get("service_role_arn")
        return result

    @builtins.property
    def task_invocation_parameters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnMaintenanceWindowTask.TaskInvocationParametersProperty]]:
        """``AWS::SSM::MaintenanceWindowTask.TaskInvocationParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters
        """
        result = self._values.get("task_invocation_parameters")
        return result

    @builtins.property
    def task_parameters(self) -> typing.Any:
        """``AWS::SSM::MaintenanceWindowTask.TaskParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskparameters
        """
        result = self._values.get("task_parameters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMaintenanceWindowTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnParameter(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnParameter",
):
    """A CloudFormation ``AWS::SSM::Parameter``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html
    :cloudformationResource: AWS::SSM::Parameter
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        type: builtins.str,
        value: builtins.str,
        allowed_pattern: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        tier: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::SSM::Parameter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: ``AWS::SSM::Parameter.Type``.
        :param value: ``AWS::SSM::Parameter.Value``.
        :param allowed_pattern: ``AWS::SSM::Parameter.AllowedPattern``.
        :param data_type: ``AWS::SSM::Parameter.DataType``.
        :param description: ``AWS::SSM::Parameter.Description``.
        :param name: ``AWS::SSM::Parameter.Name``.
        :param policies: ``AWS::SSM::Parameter.Policies``.
        :param tags: ``AWS::SSM::Parameter.Tags``.
        :param tier: ``AWS::SSM::Parameter.Tier``.
        """
        props = CfnParameterProps(
            type=type,
            value=value,
            allowed_pattern=allowed_pattern,
            data_type=data_type,
            description=description,
            name=name,
            policies=policies,
            tags=tags,
            tier=tier,
        )

        jsii.create(CfnParameter, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrType")
    def attr_type(self) -> builtins.str:
        """
        :cloudformationAttribute: Type
        """
        return jsii.get(self, "attrType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrValue")
    def attr_value(self) -> builtins.str:
        """
        :cloudformationAttribute: Value
        """
        return jsii.get(self, "attrValue")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SSM::Parameter.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::SSM::Parameter.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        """``AWS::SSM::Parameter.Value``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-value
        """
        return jsii.get(self, "value")

    @value.setter # type: ignore
    def value(self, value: builtins.str) -> None:
        jsii.set(self, "value", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowedPattern")
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.AllowedPattern``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-allowedpattern
        """
        return jsii.get(self, "allowedPattern")

    @allowed_pattern.setter # type: ignore
    def allowed_pattern(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "allowedPattern", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.DataType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-datatype
        """
        return jsii.get(self, "dataType")

    @data_type.setter # type: ignore
    def data_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dataType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Policies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-policies
        """
        return jsii.get(self, "policies")

    @policies.setter # type: ignore
    def policies(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "policies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tier")
    def tier(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Tier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-tier
        """
        return jsii.get(self, "tier")

    @tier.setter # type: ignore
    def tier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tier", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CfnParameterProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "value": "value",
        "allowed_pattern": "allowedPattern",
        "data_type": "dataType",
        "description": "description",
        "name": "name",
        "policies": "policies",
        "tags": "tags",
        "tier": "tier",
    },
)
class CfnParameterProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        value: builtins.str,
        allowed_pattern: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        tier: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::Parameter``.

        :param type: ``AWS::SSM::Parameter.Type``.
        :param value: ``AWS::SSM::Parameter.Value``.
        :param allowed_pattern: ``AWS::SSM::Parameter.AllowedPattern``.
        :param data_type: ``AWS::SSM::Parameter.DataType``.
        :param description: ``AWS::SSM::Parameter.Description``.
        :param name: ``AWS::SSM::Parameter.Name``.
        :param policies: ``AWS::SSM::Parameter.Policies``.
        :param tags: ``AWS::SSM::Parameter.Tags``.
        :param tier: ``AWS::SSM::Parameter.Tier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
            "value": value,
        }
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if data_type is not None:
            self._values["data_type"] = data_type
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if policies is not None:
            self._values["policies"] = policies
        if tags is not None:
            self._values["tags"] = tags
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::SSM::Parameter.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def value(self) -> builtins.str:
        """``AWS::SSM::Parameter.Value``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-value
        """
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.AllowedPattern``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-allowedpattern
        """
        result = self._values.get("allowed_pattern")
        return result

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.DataType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-datatype
        """
        result = self._values.get("data_type")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def policies(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Policies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-policies
        """
        result = self._values.get("policies")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::SSM::Parameter.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::Parameter.Tier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-tier
        """
        result = self._values.get("tier")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPatchBaseline(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline",
):
    """A CloudFormation ``AWS::SSM::PatchBaseline``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html
    :cloudformationResource: AWS::SSM::PatchBaseline
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        approval_rules: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.RuleGroupProperty"]] = None,
        approved_patches: typing.Optional[typing.List[builtins.str]] = None,
        approved_patches_compliance_level: typing.Optional[builtins.str] = None,
        approved_patches_enable_non_security: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        global_filters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchFilterGroupProperty"]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        patch_groups: typing.Optional[typing.List[builtins.str]] = None,
        rejected_patches: typing.Optional[typing.List[builtins.str]] = None,
        rejected_patches_action: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchSourceProperty"]]]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::SSM::PatchBaseline``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::SSM::PatchBaseline.Name``.
        :param approval_rules: ``AWS::SSM::PatchBaseline.ApprovalRules``.
        :param approved_patches: ``AWS::SSM::PatchBaseline.ApprovedPatches``.
        :param approved_patches_compliance_level: ``AWS::SSM::PatchBaseline.ApprovedPatchesComplianceLevel``.
        :param approved_patches_enable_non_security: ``AWS::SSM::PatchBaseline.ApprovedPatchesEnableNonSecurity``.
        :param description: ``AWS::SSM::PatchBaseline.Description``.
        :param global_filters: ``AWS::SSM::PatchBaseline.GlobalFilters``.
        :param operating_system: ``AWS::SSM::PatchBaseline.OperatingSystem``.
        :param patch_groups: ``AWS::SSM::PatchBaseline.PatchGroups``.
        :param rejected_patches: ``AWS::SSM::PatchBaseline.RejectedPatches``.
        :param rejected_patches_action: ``AWS::SSM::PatchBaseline.RejectedPatchesAction``.
        :param sources: ``AWS::SSM::PatchBaseline.Sources``.
        :param tags: ``AWS::SSM::PatchBaseline.Tags``.
        """
        props = CfnPatchBaselineProps(
            name=name,
            approval_rules=approval_rules,
            approved_patches=approved_patches,
            approved_patches_compliance_level=approved_patches_compliance_level,
            approved_patches_enable_non_security=approved_patches_enable_non_security,
            description=description,
            global_filters=global_filters,
            operating_system=operating_system,
            patch_groups=patch_groups,
            rejected_patches=rejected_patches,
            rejected_patches_action=rejected_patches_action,
            sources=sources,
            tags=tags,
        )

        jsii.create(CfnPatchBaseline, self, [scope, id, props])

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
        """``AWS::SSM::PatchBaseline.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::SSM::PatchBaseline.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="approvalRules")
    def approval_rules(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.RuleGroupProperty"]]:
        """``AWS::SSM::PatchBaseline.ApprovalRules``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvalrules
        """
        return jsii.get(self, "approvalRules")

    @approval_rules.setter # type: ignore
    def approval_rules(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.RuleGroupProperty"]],
    ) -> None:
        jsii.set(self, "approvalRules", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="approvedPatches")
    def approved_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSM::PatchBaseline.ApprovedPatches``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatches
        """
        return jsii.get(self, "approvedPatches")

    @approved_patches.setter # type: ignore
    def approved_patches(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "approvedPatches", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="approvedPatchesComplianceLevel")
    def approved_patches_compliance_level(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.ApprovedPatchesComplianceLevel``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatchescompliancelevel
        """
        return jsii.get(self, "approvedPatchesComplianceLevel")

    @approved_patches_compliance_level.setter # type: ignore
    def approved_patches_compliance_level(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "approvedPatchesComplianceLevel", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="approvedPatchesEnableNonSecurity")
    def approved_patches_enable_non_security(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::SSM::PatchBaseline.ApprovedPatchesEnableNonSecurity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatchesenablenonsecurity
        """
        return jsii.get(self, "approvedPatchesEnableNonSecurity")

    @approved_patches_enable_non_security.setter # type: ignore
    def approved_patches_enable_non_security(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "approvedPatchesEnableNonSecurity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalFilters")
    def global_filters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchFilterGroupProperty"]]:
        """``AWS::SSM::PatchBaseline.GlobalFilters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-globalfilters
        """
        return jsii.get(self, "globalFilters")

    @global_filters.setter # type: ignore
    def global_filters(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchFilterGroupProperty"]],
    ) -> None:
        jsii.set(self, "globalFilters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.OperatingSystem``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-operatingsystem
        """
        return jsii.get(self, "operatingSystem")

    @operating_system.setter # type: ignore
    def operating_system(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "operatingSystem", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="patchGroups")
    def patch_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSM::PatchBaseline.PatchGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-patchgroups
        """
        return jsii.get(self, "patchGroups")

    @patch_groups.setter # type: ignore
    def patch_groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "patchGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rejectedPatches")
    def rejected_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSM::PatchBaseline.RejectedPatches``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-rejectedpatches
        """
        return jsii.get(self, "rejectedPatches")

    @rejected_patches.setter # type: ignore
    def rejected_patches(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "rejectedPatches", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rejectedPatchesAction")
    def rejected_patches_action(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.RejectedPatchesAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-rejectedpatchesaction
        """
        return jsii.get(self, "rejectedPatchesAction")

    @rejected_patches_action.setter # type: ignore
    def rejected_patches_action(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "rejectedPatchesAction", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchSourceProperty"]]]]:
        """``AWS::SSM::PatchBaseline.Sources``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-sources
        """
        return jsii.get(self, "sources")

    @sources.setter # type: ignore
    def sources(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchSourceProperty"]]]],
    ) -> None:
        jsii.set(self, "sources", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.PatchFilterGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"patch_filters": "patchFilters"},
    )
    class PatchFilterGroupProperty:
        def __init__(
            self,
            *,
            patch_filters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchFilterProperty"]]]] = None,
        ) -> None:
            """
            :param patch_filters: ``CfnPatchBaseline.PatchFilterGroupProperty.PatchFilters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfiltergroup.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if patch_filters is not None:
                self._values["patch_filters"] = patch_filters

        @builtins.property
        def patch_filters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchFilterProperty"]]]]:
            """``CfnPatchBaseline.PatchFilterGroupProperty.PatchFilters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfiltergroup.html#cfn-ssm-patchbaseline-patchfiltergroup-patchfilters
            """
            result = self._values.get("patch_filters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PatchFilterGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.PatchFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class PatchFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param key: ``CfnPatchBaseline.PatchFilterProperty.Key``.
            :param values: ``CfnPatchBaseline.PatchFilterProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfilter.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnPatchBaseline.PatchFilterProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfilter.html#cfn-ssm-patchbaseline-patchfilter-key
            """
            result = self._values.get("key")
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnPatchBaseline.PatchFilterProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfilter.html#cfn-ssm-patchbaseline-patchfilter-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PatchFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.PatchSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration": "configuration",
            "name": "name",
            "products": "products",
        },
    )
    class PatchSourceProperty:
        def __init__(
            self,
            *,
            configuration: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            products: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param configuration: ``CfnPatchBaseline.PatchSourceProperty.Configuration``.
            :param name: ``CfnPatchBaseline.PatchSourceProperty.Name``.
            :param products: ``CfnPatchBaseline.PatchSourceProperty.Products``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if configuration is not None:
                self._values["configuration"] = configuration
            if name is not None:
                self._values["name"] = name
            if products is not None:
                self._values["products"] = products

        @builtins.property
        def configuration(self) -> typing.Optional[builtins.str]:
            """``CfnPatchBaseline.PatchSourceProperty.Configuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html#cfn-ssm-patchbaseline-patchsource-configuration
            """
            result = self._values.get("configuration")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnPatchBaseline.PatchSourceProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html#cfn-ssm-patchbaseline-patchsource-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def products(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnPatchBaseline.PatchSourceProperty.Products``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html#cfn-ssm-patchbaseline-patchsource-products
            """
            result = self._values.get("products")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PatchSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.RuleGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"patch_rules": "patchRules"},
    )
    class RuleGroupProperty:
        def __init__(
            self,
            *,
            patch_rules: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.RuleProperty"]]]] = None,
        ) -> None:
            """
            :param patch_rules: ``CfnPatchBaseline.RuleGroupProperty.PatchRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rulegroup.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if patch_rules is not None:
                self._values["patch_rules"] = patch_rules

        @builtins.property
        def patch_rules(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.RuleProperty"]]]]:
            """``CfnPatchBaseline.RuleGroupProperty.PatchRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rulegroup.html#cfn-ssm-patchbaseline-rulegroup-patchrules
            """
            result = self._values.get("patch_rules")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnPatchBaseline.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approve_after_days": "approveAfterDays",
            "approve_until_date": "approveUntilDate",
            "compliance_level": "complianceLevel",
            "enable_non_security": "enableNonSecurity",
            "patch_filter_group": "patchFilterGroup",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            approve_after_days: typing.Optional[jsii.Number] = None,
            approve_until_date: typing.Optional[builtins.str] = None,
            compliance_level: typing.Optional[builtins.str] = None,
            enable_non_security: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            patch_filter_group: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchFilterGroupProperty"]] = None,
        ) -> None:
            """
            :param approve_after_days: ``CfnPatchBaseline.RuleProperty.ApproveAfterDays``.
            :param approve_until_date: ``CfnPatchBaseline.RuleProperty.ApproveUntilDate``.
            :param compliance_level: ``CfnPatchBaseline.RuleProperty.ComplianceLevel``.
            :param enable_non_security: ``CfnPatchBaseline.RuleProperty.EnableNonSecurity``.
            :param patch_filter_group: ``CfnPatchBaseline.RuleProperty.PatchFilterGroup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if approve_after_days is not None:
                self._values["approve_after_days"] = approve_after_days
            if approve_until_date is not None:
                self._values["approve_until_date"] = approve_until_date
            if compliance_level is not None:
                self._values["compliance_level"] = compliance_level
            if enable_non_security is not None:
                self._values["enable_non_security"] = enable_non_security
            if patch_filter_group is not None:
                self._values["patch_filter_group"] = patch_filter_group

        @builtins.property
        def approve_after_days(self) -> typing.Optional[jsii.Number]:
            """``CfnPatchBaseline.RuleProperty.ApproveAfterDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-approveafterdays
            """
            result = self._values.get("approve_after_days")
            return result

        @builtins.property
        def approve_until_date(self) -> typing.Optional[builtins.str]:
            """``CfnPatchBaseline.RuleProperty.ApproveUntilDate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-approveuntildate
            """
            result = self._values.get("approve_until_date")
            return result

        @builtins.property
        def compliance_level(self) -> typing.Optional[builtins.str]:
            """``CfnPatchBaseline.RuleProperty.ComplianceLevel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-compliancelevel
            """
            result = self._values.get("compliance_level")
            return result

        @builtins.property
        def enable_non_security(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnPatchBaseline.RuleProperty.EnableNonSecurity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-enablenonsecurity
            """
            result = self._values.get("enable_non_security")
            return result

        @builtins.property
        def patch_filter_group(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPatchBaseline.PatchFilterGroupProperty"]]:
            """``CfnPatchBaseline.RuleProperty.PatchFilterGroup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-patchfiltergroup
            """
            result = self._values.get("patch_filter_group")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CfnPatchBaselineProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "approval_rules": "approvalRules",
        "approved_patches": "approvedPatches",
        "approved_patches_compliance_level": "approvedPatchesComplianceLevel",
        "approved_patches_enable_non_security": "approvedPatchesEnableNonSecurity",
        "description": "description",
        "global_filters": "globalFilters",
        "operating_system": "operatingSystem",
        "patch_groups": "patchGroups",
        "rejected_patches": "rejectedPatches",
        "rejected_patches_action": "rejectedPatchesAction",
        "sources": "sources",
        "tags": "tags",
    },
)
class CfnPatchBaselineProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        approval_rules: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnPatchBaseline.RuleGroupProperty]] = None,
        approved_patches: typing.Optional[typing.List[builtins.str]] = None,
        approved_patches_compliance_level: typing.Optional[builtins.str] = None,
        approved_patches_enable_non_security: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        global_filters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnPatchBaseline.PatchFilterGroupProperty]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        patch_groups: typing.Optional[typing.List[builtins.str]] = None,
        rejected_patches: typing.Optional[typing.List[builtins.str]] = None,
        rejected_patches_action: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPatchBaseline.PatchSourceProperty]]]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::PatchBaseline``.

        :param name: ``AWS::SSM::PatchBaseline.Name``.
        :param approval_rules: ``AWS::SSM::PatchBaseline.ApprovalRules``.
        :param approved_patches: ``AWS::SSM::PatchBaseline.ApprovedPatches``.
        :param approved_patches_compliance_level: ``AWS::SSM::PatchBaseline.ApprovedPatchesComplianceLevel``.
        :param approved_patches_enable_non_security: ``AWS::SSM::PatchBaseline.ApprovedPatchesEnableNonSecurity``.
        :param description: ``AWS::SSM::PatchBaseline.Description``.
        :param global_filters: ``AWS::SSM::PatchBaseline.GlobalFilters``.
        :param operating_system: ``AWS::SSM::PatchBaseline.OperatingSystem``.
        :param patch_groups: ``AWS::SSM::PatchBaseline.PatchGroups``.
        :param rejected_patches: ``AWS::SSM::PatchBaseline.RejectedPatches``.
        :param rejected_patches_action: ``AWS::SSM::PatchBaseline.RejectedPatchesAction``.
        :param sources: ``AWS::SSM::PatchBaseline.Sources``.
        :param tags: ``AWS::SSM::PatchBaseline.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if approval_rules is not None:
            self._values["approval_rules"] = approval_rules
        if approved_patches is not None:
            self._values["approved_patches"] = approved_patches
        if approved_patches_compliance_level is not None:
            self._values["approved_patches_compliance_level"] = approved_patches_compliance_level
        if approved_patches_enable_non_security is not None:
            self._values["approved_patches_enable_non_security"] = approved_patches_enable_non_security
        if description is not None:
            self._values["description"] = description
        if global_filters is not None:
            self._values["global_filters"] = global_filters
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if patch_groups is not None:
            self._values["patch_groups"] = patch_groups
        if rejected_patches is not None:
            self._values["rejected_patches"] = rejected_patches
        if rejected_patches_action is not None:
            self._values["rejected_patches_action"] = rejected_patches_action
        if sources is not None:
            self._values["sources"] = sources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::SSM::PatchBaseline.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def approval_rules(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnPatchBaseline.RuleGroupProperty]]:
        """``AWS::SSM::PatchBaseline.ApprovalRules``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvalrules
        """
        result = self._values.get("approval_rules")
        return result

    @builtins.property
    def approved_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSM::PatchBaseline.ApprovedPatches``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatches
        """
        result = self._values.get("approved_patches")
        return result

    @builtins.property
    def approved_patches_compliance_level(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.ApprovedPatchesComplianceLevel``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatchescompliancelevel
        """
        result = self._values.get("approved_patches_compliance_level")
        return result

    @builtins.property
    def approved_patches_enable_non_security(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::SSM::PatchBaseline.ApprovedPatchesEnableNonSecurity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatchesenablenonsecurity
        """
        result = self._values.get("approved_patches_enable_non_security")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def global_filters(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnPatchBaseline.PatchFilterGroupProperty]]:
        """``AWS::SSM::PatchBaseline.GlobalFilters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-globalfilters
        """
        result = self._values.get("global_filters")
        return result

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.OperatingSystem``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-operatingsystem
        """
        result = self._values.get("operating_system")
        return result

    @builtins.property
    def patch_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSM::PatchBaseline.PatchGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-patchgroups
        """
        result = self._values.get("patch_groups")
        return result

    @builtins.property
    def rejected_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSM::PatchBaseline.RejectedPatches``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-rejectedpatches
        """
        result = self._values.get("rejected_patches")
        return result

    @builtins.property
    def rejected_patches_action(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::PatchBaseline.RejectedPatchesAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-rejectedpatchesaction
        """
        result = self._values.get("rejected_patches_action")
        return result

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPatchBaseline.PatchSourceProperty]]]]:
        """``AWS::SSM::PatchBaseline.Sources``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-sources
        """
        result = self._values.get("sources")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SSM::PatchBaseline.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPatchBaselineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnResourceDataSync(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.CfnResourceDataSync",
):
    """A CloudFormation ``AWS::SSM::ResourceDataSync``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html
    :cloudformationResource: AWS::SSM::ResourceDataSync
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        sync_name: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        s3_destination: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.S3DestinationProperty"]] = None,
        sync_format: typing.Optional[builtins.str] = None,
        sync_source: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.SyncSourceProperty"]] = None,
        sync_type: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::SSM::ResourceDataSync``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param sync_name: ``AWS::SSM::ResourceDataSync.SyncName``.
        :param bucket_name: ``AWS::SSM::ResourceDataSync.BucketName``.
        :param bucket_prefix: ``AWS::SSM::ResourceDataSync.BucketPrefix``.
        :param bucket_region: ``AWS::SSM::ResourceDataSync.BucketRegion``.
        :param kms_key_arn: ``AWS::SSM::ResourceDataSync.KMSKeyArn``.
        :param s3_destination: ``AWS::SSM::ResourceDataSync.S3Destination``.
        :param sync_format: ``AWS::SSM::ResourceDataSync.SyncFormat``.
        :param sync_source: ``AWS::SSM::ResourceDataSync.SyncSource``.
        :param sync_type: ``AWS::SSM::ResourceDataSync.SyncType``.
        """
        props = CfnResourceDataSyncProps(
            sync_name=sync_name,
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            bucket_region=bucket_region,
            kms_key_arn=kms_key_arn,
            s3_destination=s3_destination,
            sync_format=sync_format,
            sync_source=sync_source,
            sync_type=sync_type,
        )

        jsii.create(CfnResourceDataSync, self, [scope, id, props])

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
    @jsii.member(jsii_name="syncName")
    def sync_name(self) -> builtins.str:
        """``AWS::SSM::ResourceDataSync.SyncName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncname
        """
        return jsii.get(self, "syncName")

    @sync_name.setter # type: ignore
    def sync_name(self, value: builtins.str) -> None:
        jsii.set(self, "syncName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.BucketName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketname
        """
        return jsii.get(self, "bucketName")

    @bucket_name.setter # type: ignore
    def bucket_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bucketName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.BucketPrefix``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketprefix
        """
        return jsii.get(self, "bucketPrefix")

    @bucket_prefix.setter # type: ignore
    def bucket_prefix(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bucketPrefix", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bucketRegion")
    def bucket_region(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.BucketRegion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketregion
        """
        return jsii.get(self, "bucketRegion")

    @bucket_region.setter # type: ignore
    def bucket_region(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bucketRegion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.KMSKeyArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-kmskeyarn
        """
        return jsii.get(self, "kmsKeyArn")

    @kms_key_arn.setter # type: ignore
    def kms_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="s3Destination")
    def s3_destination(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.S3DestinationProperty"]]:
        """``AWS::SSM::ResourceDataSync.S3Destination``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-s3destination
        """
        return jsii.get(self, "s3Destination")

    @s3_destination.setter # type: ignore
    def s3_destination(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.S3DestinationProperty"]],
    ) -> None:
        jsii.set(self, "s3Destination", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="syncFormat")
    def sync_format(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.SyncFormat``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncformat
        """
        return jsii.get(self, "syncFormat")

    @sync_format.setter # type: ignore
    def sync_format(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "syncFormat", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="syncSource")
    def sync_source(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.SyncSourceProperty"]]:
        """``AWS::SSM::ResourceDataSync.SyncSource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncsource
        """
        return jsii.get(self, "syncSource")

    @sync_source.setter # type: ignore
    def sync_source(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.SyncSourceProperty"]],
    ) -> None:
        jsii.set(self, "syncSource", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="syncType")
    def sync_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.SyncType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-synctype
        """
        return jsii.get(self, "syncType")

    @sync_type.setter # type: ignore
    def sync_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "syncType", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnResourceDataSync.AwsOrganizationsSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "organization_source_type": "organizationSourceType",
            "organizational_units": "organizationalUnits",
        },
    )
    class AwsOrganizationsSourceProperty:
        def __init__(
            self,
            *,
            organization_source_type: builtins.str,
            organizational_units: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param organization_source_type: ``CfnResourceDataSync.AwsOrganizationsSourceProperty.OrganizationSourceType``.
            :param organizational_units: ``CfnResourceDataSync.AwsOrganizationsSourceProperty.OrganizationalUnits``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-awsorganizationssource.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "organization_source_type": organization_source_type,
            }
            if organizational_units is not None:
                self._values["organizational_units"] = organizational_units

        @builtins.property
        def organization_source_type(self) -> builtins.str:
            """``CfnResourceDataSync.AwsOrganizationsSourceProperty.OrganizationSourceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-awsorganizationssource.html#cfn-ssm-resourcedatasync-awsorganizationssource-organizationsourcetype
            """
            result = self._values.get("organization_source_type")
            assert result is not None, "Required property 'organization_source_type' is missing"
            return result

        @builtins.property
        def organizational_units(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnResourceDataSync.AwsOrganizationsSourceProperty.OrganizationalUnits``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-awsorganizationssource.html#cfn-ssm-resourcedatasync-awsorganizationssource-organizationalunits
            """
            result = self._values.get("organizational_units")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsOrganizationsSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnResourceDataSync.S3DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_region": "bucketRegion",
            "sync_format": "syncFormat",
            "bucket_prefix": "bucketPrefix",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class S3DestinationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            bucket_region: builtins.str,
            sync_format: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket_name: ``CfnResourceDataSync.S3DestinationProperty.BucketName``.
            :param bucket_region: ``CfnResourceDataSync.S3DestinationProperty.BucketRegion``.
            :param sync_format: ``CfnResourceDataSync.S3DestinationProperty.SyncFormat``.
            :param bucket_prefix: ``CfnResourceDataSync.S3DestinationProperty.BucketPrefix``.
            :param kms_key_arn: ``CfnResourceDataSync.S3DestinationProperty.KMSKeyArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
                "bucket_region": bucket_region,
                "sync_format": sync_format,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def bucket_name(self) -> builtins.str:
            """``CfnResourceDataSync.S3DestinationProperty.BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-bucketname
            """
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return result

        @builtins.property
        def bucket_region(self) -> builtins.str:
            """``CfnResourceDataSync.S3DestinationProperty.BucketRegion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-bucketregion
            """
            result = self._values.get("bucket_region")
            assert result is not None, "Required property 'bucket_region' is missing"
            return result

        @builtins.property
        def sync_format(self) -> builtins.str:
            """``CfnResourceDataSync.S3DestinationProperty.SyncFormat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-syncformat
            """
            result = self._values.get("sync_format")
            assert result is not None, "Required property 'sync_format' is missing"
            return result

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnResourceDataSync.S3DestinationProperty.BucketPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-bucketprefix
            """
            result = self._values.get("bucket_prefix")
            return result

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            """``CfnResourceDataSync.S3DestinationProperty.KMSKeyArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-kmskeyarn
            """
            result = self._values.get("kms_key_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ssm.CfnResourceDataSync.SyncSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_regions": "sourceRegions",
            "source_type": "sourceType",
            "aws_organizations_source": "awsOrganizationsSource",
            "include_future_regions": "includeFutureRegions",
        },
    )
    class SyncSourceProperty:
        def __init__(
            self,
            *,
            source_regions: typing.List[builtins.str],
            source_type: builtins.str,
            aws_organizations_source: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.AwsOrganizationsSourceProperty"]] = None,
            include_future_regions: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param source_regions: ``CfnResourceDataSync.SyncSourceProperty.SourceRegions``.
            :param source_type: ``CfnResourceDataSync.SyncSourceProperty.SourceType``.
            :param aws_organizations_source: ``CfnResourceDataSync.SyncSourceProperty.AwsOrganizationsSource``.
            :param include_future_regions: ``CfnResourceDataSync.SyncSourceProperty.IncludeFutureRegions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "source_regions": source_regions,
                "source_type": source_type,
            }
            if aws_organizations_source is not None:
                self._values["aws_organizations_source"] = aws_organizations_source
            if include_future_regions is not None:
                self._values["include_future_regions"] = include_future_regions

        @builtins.property
        def source_regions(self) -> typing.List[builtins.str]:
            """``CfnResourceDataSync.SyncSourceProperty.SourceRegions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-sourceregions
            """
            result = self._values.get("source_regions")
            assert result is not None, "Required property 'source_regions' is missing"
            return result

        @builtins.property
        def source_type(self) -> builtins.str:
            """``CfnResourceDataSync.SyncSourceProperty.SourceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-sourcetype
            """
            result = self._values.get("source_type")
            assert result is not None, "Required property 'source_type' is missing"
            return result

        @builtins.property
        def aws_organizations_source(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceDataSync.AwsOrganizationsSourceProperty"]]:
            """``CfnResourceDataSync.SyncSourceProperty.AwsOrganizationsSource``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-awsorganizationssource
            """
            result = self._values.get("aws_organizations_source")
            return result

        @builtins.property
        def include_future_regions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnResourceDataSync.SyncSourceProperty.IncludeFutureRegions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-includefutureregions
            """
            result = self._values.get("include_future_regions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SyncSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CfnResourceDataSyncProps",
    jsii_struct_bases=[],
    name_mapping={
        "sync_name": "syncName",
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "bucket_region": "bucketRegion",
        "kms_key_arn": "kmsKeyArn",
        "s3_destination": "s3Destination",
        "sync_format": "syncFormat",
        "sync_source": "syncSource",
        "sync_type": "syncType",
    },
)
class CfnResourceDataSyncProps:
    def __init__(
        self,
        *,
        sync_name: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        s3_destination: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnResourceDataSync.S3DestinationProperty]] = None,
        sync_format: typing.Optional[builtins.str] = None,
        sync_source: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnResourceDataSync.SyncSourceProperty]] = None,
        sync_type: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSM::ResourceDataSync``.

        :param sync_name: ``AWS::SSM::ResourceDataSync.SyncName``.
        :param bucket_name: ``AWS::SSM::ResourceDataSync.BucketName``.
        :param bucket_prefix: ``AWS::SSM::ResourceDataSync.BucketPrefix``.
        :param bucket_region: ``AWS::SSM::ResourceDataSync.BucketRegion``.
        :param kms_key_arn: ``AWS::SSM::ResourceDataSync.KMSKeyArn``.
        :param s3_destination: ``AWS::SSM::ResourceDataSync.S3Destination``.
        :param sync_format: ``AWS::SSM::ResourceDataSync.SyncFormat``.
        :param sync_source: ``AWS::SSM::ResourceDataSync.SyncSource``.
        :param sync_type: ``AWS::SSM::ResourceDataSync.SyncType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "sync_name": sync_name,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if bucket_region is not None:
            self._values["bucket_region"] = bucket_region
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if s3_destination is not None:
            self._values["s3_destination"] = s3_destination
        if sync_format is not None:
            self._values["sync_format"] = sync_format
        if sync_source is not None:
            self._values["sync_source"] = sync_source
        if sync_type is not None:
            self._values["sync_type"] = sync_type

    @builtins.property
    def sync_name(self) -> builtins.str:
        """``AWS::SSM::ResourceDataSync.SyncName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncname
        """
        result = self._values.get("sync_name")
        assert result is not None, "Required property 'sync_name' is missing"
        return result

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.BucketName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketname
        """
        result = self._values.get("bucket_name")
        return result

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.BucketPrefix``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketprefix
        """
        result = self._values.get("bucket_prefix")
        return result

    @builtins.property
    def bucket_region(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.BucketRegion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketregion
        """
        result = self._values.get("bucket_region")
        return result

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.KMSKeyArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-kmskeyarn
        """
        result = self._values.get("kms_key_arn")
        return result

    @builtins.property
    def s3_destination(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnResourceDataSync.S3DestinationProperty]]:
        """``AWS::SSM::ResourceDataSync.S3Destination``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-s3destination
        """
        result = self._values.get("s3_destination")
        return result

    @builtins.property
    def sync_format(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.SyncFormat``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncformat
        """
        result = self._values.get("sync_format")
        return result

    @builtins.property
    def sync_source(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnResourceDataSync.SyncSourceProperty]]:
        """``AWS::SSM::ResourceDataSync.SyncSource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncsource
        """
        result = self._values.get("sync_source")
        return result

    @builtins.property
    def sync_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSM::ResourceDataSync.SyncType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-synctype
        """
        result = self._values.get("sync_type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDataSyncProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.CommonStringParameterAttributes",
    jsii_struct_bases=[],
    name_mapping={"parameter_name": "parameterName", "simple_name": "simpleName"},
)
class CommonStringParameterAttributes:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        simple_name: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Common attributes for string parameters.

        :param parameter_name: The name of the parameter store value. This value can be a token or a concrete string. If it is a concrete string and includes "/" it must also be prefixed with a "/" (fully-qualified).
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        """
        self._values: typing.Dict[str, typing.Any] = {
            "parameter_name": parameter_name,
        }
        if simple_name is not None:
            self._values["simple_name"] = simple_name

    @builtins.property
    def parameter_name(self) -> builtins.str:
        """The name of the parameter store value.

        This value can be a token or a concrete string. If it is a concrete string
        and includes "/" it must also be prefixed with a "/" (fully-qualified).
        """
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return result

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        """Indicates of the parameter name is a simple name (i.e. does not include "/" separators).

        This is only required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        """
        result = self._values.get("simple_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonStringParameterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-ssm.IParameter")
class IParameter(aws_cdk.core.IResource, typing_extensions.Protocol):
    """An SSM Parameter reference."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IParameterProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> builtins.str:
        """The ARN of the SSM Parameter resource.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        """The name of the SSM Parameter resource.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        """The type of the SSM Parameter resource.

        :attribute: true
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read (DescribeParameter, GetParameter, GetParameterHistory) permissions on the SSM Parameter.

        :param grantee: the role to be granted read-only access to the parameter.
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants write (PutParameter) permissions on the SSM Parameter.

        :param grantee: the role to be granted write access to the parameter.
        """
        ...


class _IParameterProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """An SSM Parameter reference."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ssm.IParameter"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> builtins.str:
        """The ARN of the SSM Parameter resource.

        :attribute: true
        """
        return jsii.get(self, "parameterArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        """The name of the SSM Parameter resource.

        :attribute: true
        """
        return jsii.get(self, "parameterName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        """The type of the SSM Parameter resource.

        :attribute: true
        """
        return jsii.get(self, "parameterType")

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read (DescribeParameter, GetParameter, GetParameterHistory) permissions on the SSM Parameter.

        :param grantee: the role to be granted read-only access to the parameter.
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants write (PutParameter) permissions on the SSM Parameter.

        :param grantee: the role to be granted write access to the parameter.
        """
        return jsii.invoke(self, "grantWrite", [grantee])


@jsii.interface(jsii_type="@aws-cdk/aws-ssm.IStringListParameter")
class IStringListParameter(IParameter, typing_extensions.Protocol):
    """A StringList SSM Parameter."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStringListParameterProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        """The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value. Values in the array
        cannot contain commas (``,``).

        :attribute: Value
        """
        ...


class _IStringListParameterProxy(
    jsii.proxy_for(IParameter) # type: ignore
):
    """A StringList SSM Parameter."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ssm.IStringListParameter"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        """The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value. Values in the array
        cannot contain commas (``,``).

        :attribute: Value
        """
        return jsii.get(self, "stringListValue")


@jsii.interface(jsii_type="@aws-cdk/aws-ssm.IStringParameter")
class IStringParameter(IParameter, typing_extensions.Protocol):
    """A String SSM Parameter."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStringParameterProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        """The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value.

        :attribute: Value
        """
        ...


class _IStringParameterProxy(
    jsii.proxy_for(IParameter) # type: ignore
):
    """A String SSM Parameter."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ssm.IStringParameter"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        """The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value.

        :attribute: Value
        """
        return jsii.get(self, "stringValue")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.ParameterOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_pattern": "allowedPattern",
        "description": "description",
        "parameter_name": "parameterName",
        "simple_name": "simpleName",
        "tier": "tier",
    },
)
class ParameterOptions:
    def __init__(
        self,
        *,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional["ParameterTier"] = None,
    ) -> None:
        """Properties needed to create a new SSM Parameter.

        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if description is not None:
            self._values["description"] = description
        if parameter_name is not None:
            self._values["parameter_name"] = parameter_name
        if simple_name is not None:
            self._values["simple_name"] = simple_name
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        """A regular expression used to validate the parameter value.

        For example, for String types with values restricted to
        numbers, you can specify the following: ``^\\d+$``

        :default: no validation is performed
        """
        result = self._values.get("allowed_pattern")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """Information about the parameter that you want to add to the system.

        :default: none
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def parameter_name(self) -> typing.Optional[builtins.str]:
        """The name of the parameter.

        :default: - a name will be generated by CloudFormation
        """
        result = self._values.get("parameter_name")
        return result

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        """Indicates of the parameter name is a simple name (i.e. does not include "/" separators).

        This is only required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        """
        result = self._values.get("simple_name")
        return result

    @builtins.property
    def tier(self) -> typing.Optional["ParameterTier"]:
        """The tier of the string parameter.

        :default: - undefined
        """
        result = self._values.get("tier")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParameterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ssm.ParameterTier")
class ParameterTier(enum.Enum):
    """SSM parameter tier."""

    ADVANCED = "ADVANCED"
    """String."""
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    """String."""
    STANDARD = "STANDARD"
    """String."""


@jsii.enum(jsii_type="@aws-cdk/aws-ssm.ParameterType")
class ParameterType(enum.Enum):
    """SSM parameter type."""

    STRING = "STRING"
    """String."""
    SECURE_STRING = "SECURE_STRING"
    """Secure String Parameter Store uses an AWS Key Management Service (KMS) customer master key (CMK) to encrypt the parameter value."""
    STRING_LIST = "STRING_LIST"
    """String List."""
    AWS_EC2_IMAGE_ID = "AWS_EC2_IMAGE_ID"
    """An Amazon EC2 image ID, such as ami-0ff8a91507f77f867."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.SecureStringParameterAttributes",
    jsii_struct_bases=[CommonStringParameterAttributes],
    name_mapping={
        "parameter_name": "parameterName",
        "simple_name": "simpleName",
        "version": "version",
        "encryption_key": "encryptionKey",
    },
)
class SecureStringParameterAttributes(CommonStringParameterAttributes):
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        simple_name: typing.Optional[builtins.bool] = None,
        version: jsii.Number,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """Attributes for secure string parameters.

        :param parameter_name: The name of the parameter store value. This value can be a token or a concrete string. If it is a concrete string and includes "/" it must also be prefixed with a "/" (fully-qualified).
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param version: The version number of the value you wish to retrieve. This is required for secure strings.
        :param encryption_key: The encryption key that is used to encrypt this parameter. Default: - default master key
        """
        self._values: typing.Dict[str, typing.Any] = {
            "parameter_name": parameter_name,
            "version": version,
        }
        if simple_name is not None:
            self._values["simple_name"] = simple_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def parameter_name(self) -> builtins.str:
        """The name of the parameter store value.

        This value can be a token or a concrete string. If it is a concrete string
        and includes "/" it must also be prefixed with a "/" (fully-qualified).
        """
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return result

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        """Indicates of the parameter name is a simple name (i.e. does not include "/" separators).

        This is only required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        """
        result = self._values.get("simple_name")
        return result

    @builtins.property
    def version(self) -> jsii.Number:
        """The version number of the value you wish to retrieve.

        This is required for secure strings.
        """
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The encryption key that is used to encrypt this parameter.

        :default: - default master key
        """
        result = self._values.get("encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureStringParameterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IStringListParameter, IParameter)
class StringListParameter(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.StringListParameter",
):
    """Creates a new StringList SSM Parameter.

    :resource: AWS::SSM::Parameter
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        string_list_value: typing.List[builtins.str],
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[ParameterTier] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param string_list_value: The values of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        """
        props = StringListParameterProps(
            string_list_value=string_list_value,
            allowed_pattern=allowed_pattern,
            description=description,
            parameter_name=parameter_name,
            simple_name=simple_name,
            tier=tier,
        )

        jsii.create(StringListParameter, self, [scope, id, props])

    @jsii.member(jsii_name="fromStringListParameterName")
    @builtins.classmethod
    def from_string_list_parameter_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        string_list_parameter_name: builtins.str,
    ) -> IStringListParameter:
        """Imports an external parameter of type string list.

        Returns a token and should not be parsed.

        :param scope: -
        :param id: -
        :param string_list_parameter_name: -
        """
        return jsii.sinvoke(cls, "fromStringListParameterName", [scope, id, string_list_parameter_name])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read (DescribeParameter, GetParameter, GetParameterHistory) permissions on the SSM Parameter.

        :param grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants write (PutParameter) permissions on the SSM Parameter.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> builtins.str:
        """The ARN of the SSM Parameter resource."""
        return jsii.get(self, "parameterArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        """The name of the SSM Parameter resource."""
        return jsii.get(self, "parameterName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        """The type of the SSM Parameter resource."""
        return jsii.get(self, "parameterType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        """The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value. Values in the array
        cannot contain commas (``,``).
        """
        return jsii.get(self, "stringListValue")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The encryption key that is used to encrypt this parameter.

        - @default - default master key
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.StringListParameterProps",
    jsii_struct_bases=[ParameterOptions],
    name_mapping={
        "allowed_pattern": "allowedPattern",
        "description": "description",
        "parameter_name": "parameterName",
        "simple_name": "simpleName",
        "tier": "tier",
        "string_list_value": "stringListValue",
    },
)
class StringListParameterProps(ParameterOptions):
    def __init__(
        self,
        *,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[ParameterTier] = None,
        string_list_value: typing.List[builtins.str],
    ) -> None:
        """Properties needed to create a StringList SSM Parameter.

        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        :param string_list_value: The values of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "string_list_value": string_list_value,
        }
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if description is not None:
            self._values["description"] = description
        if parameter_name is not None:
            self._values["parameter_name"] = parameter_name
        if simple_name is not None:
            self._values["simple_name"] = simple_name
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        """A regular expression used to validate the parameter value.

        For example, for String types with values restricted to
        numbers, you can specify the following: ``^\\d+$``

        :default: no validation is performed
        """
        result = self._values.get("allowed_pattern")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """Information about the parameter that you want to add to the system.

        :default: none
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def parameter_name(self) -> typing.Optional[builtins.str]:
        """The name of the parameter.

        :default: - a name will be generated by CloudFormation
        """
        result = self._values.get("parameter_name")
        return result

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        """Indicates of the parameter name is a simple name (i.e. does not include "/" separators).

        This is only required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        """
        result = self._values.get("simple_name")
        return result

    @builtins.property
    def tier(self) -> typing.Optional[ParameterTier]:
        """The tier of the string parameter.

        :default: - undefined
        """
        result = self._values.get("tier")
        return result

    @builtins.property
    def string_list_value(self) -> typing.List[builtins.str]:
        """The values of the parameter.

        It may not reference another parameter and ``{{}}`` cannot be used in the value.
        """
        result = self._values.get("string_list_value")
        assert result is not None, "Required property 'string_list_value' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringListParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IStringParameter, IParameter)
class StringParameter(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ssm.StringParameter",
):
    """Creates a new String SSM Parameter.

    :resource: AWS::SSM::Parameter
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        string_value: builtins.str,
        type: typing.Optional[ParameterType] = None,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[ParameterTier] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param string_value: The value of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        :param type: The type of the string parameter. Default: ParameterType.STRING
        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        """
        props = StringParameterProps(
            string_value=string_value,
            type=type,
            allowed_pattern=allowed_pattern,
            description=description,
            parameter_name=parameter_name,
            simple_name=simple_name,
            tier=tier,
        )

        jsii.create(StringParameter, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecureStringParameterAttributes")
    @builtins.classmethod
    def from_secure_string_parameter_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        version: jsii.Number,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        parameter_name: builtins.str,
        simple_name: typing.Optional[builtins.bool] = None,
    ) -> IStringParameter:
        """Imports a secure string parameter from the SSM parameter store.

        :param scope: -
        :param id: -
        :param version: The version number of the value you wish to retrieve. This is required for secure strings.
        :param encryption_key: The encryption key that is used to encrypt this parameter. Default: - default master key
        :param parameter_name: The name of the parameter store value. This value can be a token or a concrete string. If it is a concrete string and includes "/" it must also be prefixed with a "/" (fully-qualified).
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        """
        attrs = SecureStringParameterAttributes(
            version=version,
            encryption_key=encryption_key,
            parameter_name=parameter_name,
            simple_name=simple_name,
        )

        return jsii.sinvoke(cls, "fromSecureStringParameterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromStringParameterAttributes")
    @builtins.classmethod
    def from_string_parameter_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        type: typing.Optional[ParameterType] = None,
        version: typing.Optional[jsii.Number] = None,
        parameter_name: builtins.str,
        simple_name: typing.Optional[builtins.bool] = None,
    ) -> IStringParameter:
        """Imports an external string parameter with name and optional version.

        :param scope: -
        :param id: -
        :param type: The type of the string parameter. Default: ParameterType.STRING
        :param version: The version number of the value you wish to retrieve. Default: The latest version will be retrieved.
        :param parameter_name: The name of the parameter store value. This value can be a token or a concrete string. If it is a concrete string and includes "/" it must also be prefixed with a "/" (fully-qualified).
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        """
        attrs = StringParameterAttributes(
            type=type,
            version=version,
            parameter_name=parameter_name,
            simple_name=simple_name,
        )

        return jsii.sinvoke(cls, "fromStringParameterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromStringParameterName")
    @builtins.classmethod
    def from_string_parameter_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        string_parameter_name: builtins.str,
    ) -> IStringParameter:
        """Imports an external string parameter by name.

        :param scope: -
        :param id: -
        :param string_parameter_name: -
        """
        return jsii.sinvoke(cls, "fromStringParameterName", [scope, id, string_parameter_name])

    @jsii.member(jsii_name="valueForSecureStringParameter")
    @builtins.classmethod
    def value_for_secure_string_parameter(
        cls,
        scope: constructs.Construct,
        parameter_name: builtins.str,
        version: jsii.Number,
    ) -> builtins.str:
        """Returns a token that will resolve (during deployment).

        :param scope: Some scope within a stack.
        :param parameter_name: The name of the SSM parameter.
        :param version: The parameter version (required for secure strings).
        """
        return jsii.sinvoke(cls, "valueForSecureStringParameter", [scope, parameter_name, version])

    @jsii.member(jsii_name="valueForStringParameter")
    @builtins.classmethod
    def value_for_string_parameter(
        cls,
        scope: constructs.Construct,
        parameter_name: builtins.str,
        version: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        """Returns a token that will resolve (during deployment) to the string value of an SSM string parameter.

        :param scope: Some scope within a stack.
        :param parameter_name: The name of the SSM parameter.
        :param version: The parameter version (recommended in order to ensure that the value won't change during deployment).
        """
        return jsii.sinvoke(cls, "valueForStringParameter", [scope, parameter_name, version])

    @jsii.member(jsii_name="valueForTypedStringParameter")
    @builtins.classmethod
    def value_for_typed_string_parameter(
        cls,
        scope: constructs.Construct,
        parameter_name: builtins.str,
        type: typing.Optional[ParameterType] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        """Returns a token that will resolve (during deployment) to the string value of an SSM string parameter.

        :param scope: Some scope within a stack.
        :param parameter_name: The name of the SSM parameter.
        :param type: The type of the SSM parameter.
        :param version: The parameter version (recommended in order to ensure that the value won't change during deployment).
        """
        return jsii.sinvoke(cls, "valueForTypedStringParameter", [scope, parameter_name, type, version])

    @jsii.member(jsii_name="valueFromLookup")
    @builtins.classmethod
    def value_from_lookup(
        cls,
        scope: aws_cdk.core.Construct,
        parameter_name: builtins.str,
    ) -> builtins.str:
        """Reads the value of an SSM parameter during synthesis through an environmental context provider.

        Requires that the stack this scope is defined in will have explicit
        account/region information. Otherwise, it will fail during synthesis.

        :param scope: -
        :param parameter_name: -
        """
        return jsii.sinvoke(cls, "valueFromLookup", [scope, parameter_name])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read (DescribeParameter, GetParameter, GetParameterHistory) permissions on the SSM Parameter.

        :param grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants write (PutParameter) permissions on the SSM Parameter.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> builtins.str:
        """The ARN of the SSM Parameter resource."""
        return jsii.get(self, "parameterArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        """The name of the SSM Parameter resource."""
        return jsii.get(self, "parameterName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        """The type of the SSM Parameter resource."""
        return jsii.get(self, "parameterType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        """The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value.
        """
        return jsii.get(self, "stringValue")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The encryption key that is used to encrypt this parameter.

        - @default - default master key
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.StringParameterAttributes",
    jsii_struct_bases=[CommonStringParameterAttributes],
    name_mapping={
        "parameter_name": "parameterName",
        "simple_name": "simpleName",
        "type": "type",
        "version": "version",
    },
)
class StringParameterAttributes(CommonStringParameterAttributes):
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        simple_name: typing.Optional[builtins.bool] = None,
        type: typing.Optional[ParameterType] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Attributes for parameters of various types of string.

        :param parameter_name: The name of the parameter store value. This value can be a token or a concrete string. If it is a concrete string and includes "/" it must also be prefixed with a "/" (fully-qualified).
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param type: The type of the string parameter. Default: ParameterType.STRING
        :param version: The version number of the value you wish to retrieve. Default: The latest version will be retrieved.

        :see: ParameterType
        """
        self._values: typing.Dict[str, typing.Any] = {
            "parameter_name": parameter_name,
        }
        if simple_name is not None:
            self._values["simple_name"] = simple_name
        if type is not None:
            self._values["type"] = type
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def parameter_name(self) -> builtins.str:
        """The name of the parameter store value.

        This value can be a token or a concrete string. If it is a concrete string
        and includes "/" it must also be prefixed with a "/" (fully-qualified).
        """
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return result

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        """Indicates of the parameter name is a simple name (i.e. does not include "/" separators).

        This is only required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        """
        result = self._values.get("simple_name")
        return result

    @builtins.property
    def type(self) -> typing.Optional[ParameterType]:
        """The type of the string parameter.

        :default: ParameterType.STRING
        """
        result = self._values.get("type")
        return result

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        """The version number of the value you wish to retrieve.

        :default: The latest version will be retrieved.
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringParameterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ssm.StringParameterProps",
    jsii_struct_bases=[ParameterOptions],
    name_mapping={
        "allowed_pattern": "allowedPattern",
        "description": "description",
        "parameter_name": "parameterName",
        "simple_name": "simpleName",
        "tier": "tier",
        "string_value": "stringValue",
        "type": "type",
    },
)
class StringParameterProps(ParameterOptions):
    def __init__(
        self,
        *,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[ParameterTier] = None,
        string_value: builtins.str,
        type: typing.Optional[ParameterType] = None,
    ) -> None:
        """Properties needed to create a String SSM parameter.

        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates of the parameter name is a simple name (i.e. does not include "/" separators). This is only required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        :param string_value: The value of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        :param type: The type of the string parameter. Default: ParameterType.STRING
        """
        self._values: typing.Dict[str, typing.Any] = {
            "string_value": string_value,
        }
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if description is not None:
            self._values["description"] = description
        if parameter_name is not None:
            self._values["parameter_name"] = parameter_name
        if simple_name is not None:
            self._values["simple_name"] = simple_name
        if tier is not None:
            self._values["tier"] = tier
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        """A regular expression used to validate the parameter value.

        For example, for String types with values restricted to
        numbers, you can specify the following: ``^\\d+$``

        :default: no validation is performed
        """
        result = self._values.get("allowed_pattern")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """Information about the parameter that you want to add to the system.

        :default: none
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def parameter_name(self) -> typing.Optional[builtins.str]:
        """The name of the parameter.

        :default: - a name will be generated by CloudFormation
        """
        result = self._values.get("parameter_name")
        return result

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        """Indicates of the parameter name is a simple name (i.e. does not include "/" separators).

        This is only required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        """
        result = self._values.get("simple_name")
        return result

    @builtins.property
    def tier(self) -> typing.Optional[ParameterTier]:
        """The tier of the string parameter.

        :default: - undefined
        """
        result = self._values.get("tier")
        return result

    @builtins.property
    def string_value(self) -> builtins.str:
        """The value of the parameter.

        It may not reference another parameter and ``{{}}`` cannot be used in the value.
        """
        result = self._values.get("string_value")
        assert result is not None, "Required property 'string_value' is missing"
        return result

    @builtins.property
    def type(self) -> typing.Optional[ParameterType]:
        """The type of the string parameter.

        :default: ParameterType.STRING
        """
        result = self._values.get("type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssociation",
    "CfnAssociationProps",
    "CfnDocument",
    "CfnDocumentProps",
    "CfnMaintenanceWindow",
    "CfnMaintenanceWindowProps",
    "CfnMaintenanceWindowTarget",
    "CfnMaintenanceWindowTargetProps",
    "CfnMaintenanceWindowTask",
    "CfnMaintenanceWindowTaskProps",
    "CfnParameter",
    "CfnParameterProps",
    "CfnPatchBaseline",
    "CfnPatchBaselineProps",
    "CfnResourceDataSync",
    "CfnResourceDataSyncProps",
    "CommonStringParameterAttributes",
    "IParameter",
    "IStringListParameter",
    "IStringParameter",
    "ParameterOptions",
    "ParameterTier",
    "ParameterType",
    "SecureStringParameterAttributes",
    "StringListParameter",
    "StringListParameterProps",
    "StringParameter",
    "StringParameterAttributes",
    "StringParameterProps",
]

publication.publish()
