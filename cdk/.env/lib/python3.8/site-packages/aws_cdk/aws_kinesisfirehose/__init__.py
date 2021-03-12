"""
## Amazon Kinesis Data Firehose Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

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

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeliveryStream(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream",
):
    """A CloudFormation ``AWS::KinesisFirehose::DeliveryStream``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html
    :cloudformationResource: AWS::KinesisFirehose::DeliveryStream
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        delivery_stream_encryption_configuration_input: typing.Optional[typing.Union["CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty", aws_cdk.core.IResolvable]] = None,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        delivery_stream_type: typing.Optional[builtins.str] = None,
        elasticsearch_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty"]] = None,
        extended_s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty"]] = None,
        http_endpoint_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty"]] = None,
        kinesis_stream_source_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.KinesisStreamSourceConfigurationProperty"]] = None,
        redshift_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.RedshiftDestinationConfigurationProperty"]] = None,
        s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]] = None,
        splunk_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SplunkDestinationConfigurationProperty"]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::KinesisFirehose::DeliveryStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param delivery_stream_encryption_configuration_input: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamEncryptionConfigurationInput``.
        :param delivery_stream_name: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamName``.
        :param delivery_stream_type: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamType``.
        :param elasticsearch_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.ElasticsearchDestinationConfiguration``.
        :param extended_s3_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.ExtendedS3DestinationConfiguration``.
        :param http_endpoint_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.HttpEndpointDestinationConfiguration``.
        :param kinesis_stream_source_configuration: ``AWS::KinesisFirehose::DeliveryStream.KinesisStreamSourceConfiguration``.
        :param redshift_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.RedshiftDestinationConfiguration``.
        :param s3_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.S3DestinationConfiguration``.
        :param splunk_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.SplunkDestinationConfiguration``.
        :param tags: ``AWS::KinesisFirehose::DeliveryStream.Tags``.
        """
        props = CfnDeliveryStreamProps(
            delivery_stream_encryption_configuration_input=delivery_stream_encryption_configuration_input,
            delivery_stream_name=delivery_stream_name,
            delivery_stream_type=delivery_stream_type,
            elasticsearch_destination_configuration=elasticsearch_destination_configuration,
            extended_s3_destination_configuration=extended_s3_destination_configuration,
            http_endpoint_destination_configuration=http_endpoint_destination_configuration,
            kinesis_stream_source_configuration=kinesis_stream_source_configuration,
            redshift_destination_configuration=redshift_destination_configuration,
            s3_destination_configuration=s3_destination_configuration,
            splunk_destination_configuration=splunk_destination_configuration,
            tags=tags,
        )

        jsii.create(CfnDeliveryStream, self, [scope, id, props])

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
        """``AWS::KinesisFirehose::DeliveryStream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deliveryStreamEncryptionConfigurationInput")
    def delivery_stream_encryption_configuration_input(
        self,
    ) -> typing.Optional[typing.Union["CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty", aws_cdk.core.IResolvable]]:
        """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamEncryptionConfigurationInput``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput
        """
        return jsii.get(self, "deliveryStreamEncryptionConfigurationInput")

    @delivery_stream_encryption_configuration_input.setter # type: ignore
    def delivery_stream_encryption_configuration_input(
        self,
        value: typing.Optional[typing.Union["CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "deliveryStreamEncryptionConfigurationInput", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> typing.Optional[builtins.str]:
        """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamname
        """
        return jsii.get(self, "deliveryStreamName")

    @delivery_stream_name.setter # type: ignore
    def delivery_stream_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "deliveryStreamName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deliveryStreamType")
    def delivery_stream_type(self) -> typing.Optional[builtins.str]:
        """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamtype
        """
        return jsii.get(self, "deliveryStreamType")

    @delivery_stream_type.setter # type: ignore
    def delivery_stream_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "deliveryStreamType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticsearchDestinationConfiguration")
    def elasticsearch_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty"]]:
        """``AWS::KinesisFirehose::DeliveryStream.ElasticsearchDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration
        """
        return jsii.get(self, "elasticsearchDestinationConfiguration")

    @elasticsearch_destination_configuration.setter # type: ignore
    def elasticsearch_destination_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "elasticsearchDestinationConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="extendedS3DestinationConfiguration")
    def extended_s3_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty"]]:
        """``AWS::KinesisFirehose::DeliveryStream.ExtendedS3DestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration
        """
        return jsii.get(self, "extendedS3DestinationConfiguration")

    @extended_s3_destination_configuration.setter # type: ignore
    def extended_s3_destination_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "extendedS3DestinationConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpEndpointDestinationConfiguration")
    def http_endpoint_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty"]]:
        """``AWS::KinesisFirehose::DeliveryStream.HttpEndpointDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration
        """
        return jsii.get(self, "httpEndpointDestinationConfiguration")

    @http_endpoint_destination_configuration.setter # type: ignore
    def http_endpoint_destination_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "httpEndpointDestinationConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kinesisStreamSourceConfiguration")
    def kinesis_stream_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.KinesisStreamSourceConfigurationProperty"]]:
        """``AWS::KinesisFirehose::DeliveryStream.KinesisStreamSourceConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration
        """
        return jsii.get(self, "kinesisStreamSourceConfiguration")

    @kinesis_stream_source_configuration.setter # type: ignore
    def kinesis_stream_source_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.KinesisStreamSourceConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "kinesisStreamSourceConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="redshiftDestinationConfiguration")
    def redshift_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.RedshiftDestinationConfigurationProperty"]]:
        """``AWS::KinesisFirehose::DeliveryStream.RedshiftDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration
        """
        return jsii.get(self, "redshiftDestinationConfiguration")

    @redshift_destination_configuration.setter # type: ignore
    def redshift_destination_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.RedshiftDestinationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "redshiftDestinationConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="s3DestinationConfiguration")
    def s3_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]]:
        """``AWS::KinesisFirehose::DeliveryStream.S3DestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration
        """
        return jsii.get(self, "s3DestinationConfiguration")

    @s3_destination_configuration.setter # type: ignore
    def s3_destination_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "s3DestinationConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="splunkDestinationConfiguration")
    def splunk_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SplunkDestinationConfigurationProperty"]]:
        """``AWS::KinesisFirehose::DeliveryStream.SplunkDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration
        """
        return jsii.get(self, "splunkDestinationConfiguration")

    @splunk_destination_configuration.setter # type: ignore
    def splunk_destination_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SplunkDestinationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "splunkDestinationConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.BufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class BufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param interval_in_seconds: ``CfnDeliveryStream.BufferingHintsProperty.IntervalInSeconds``.
            :param size_in_m_bs: ``CfnDeliveryStream.BufferingHintsProperty.SizeInMBs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.BufferingHintsProperty.IntervalInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html#cfn-kinesisfirehose-deliverystream-bufferinghints-intervalinseconds
            """
            result = self._values.get("interval_in_seconds")
            return result

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.BufferingHintsProperty.SizeInMBs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html#cfn-kinesisfirehose-deliverystream-bufferinghints-sizeinmbs
            """
            result = self._values.get("size_in_m_bs")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "log_group_name": "logGroupName",
            "log_stream_name": "logStreamName",
        },
    )
    class CloudWatchLoggingOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            log_group_name: typing.Optional[builtins.str] = None,
            log_stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enabled: ``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.Enabled``.
            :param log_group_name: ``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.LogGroupName``.
            :param log_stream_name: ``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.LogStreamName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_stream_name is not None:
                self._values["log_stream_name"] = log_stream_name

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.LogGroupName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-loggroupname
            """
            result = self._values.get("log_group_name")
            return result

        @builtins.property
        def log_stream_name(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.LogStreamName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-logstreamname
            """
            result = self._values.get("log_stream_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLoggingOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.CopyCommandProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_table_name": "dataTableName",
            "copy_options": "copyOptions",
            "data_table_columns": "dataTableColumns",
        },
    )
    class CopyCommandProperty:
        def __init__(
            self,
            *,
            data_table_name: builtins.str,
            copy_options: typing.Optional[builtins.str] = None,
            data_table_columns: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param data_table_name: ``CfnDeliveryStream.CopyCommandProperty.DataTableName``.
            :param copy_options: ``CfnDeliveryStream.CopyCommandProperty.CopyOptions``.
            :param data_table_columns: ``CfnDeliveryStream.CopyCommandProperty.DataTableColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "data_table_name": data_table_name,
            }
            if copy_options is not None:
                self._values["copy_options"] = copy_options
            if data_table_columns is not None:
                self._values["data_table_columns"] = data_table_columns

        @builtins.property
        def data_table_name(self) -> builtins.str:
            """``CfnDeliveryStream.CopyCommandProperty.DataTableName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-datatablename
            """
            result = self._values.get("data_table_name")
            assert result is not None, "Required property 'data_table_name' is missing"
            return result

        @builtins.property
        def copy_options(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.CopyCommandProperty.CopyOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-copyoptions
            """
            result = self._values.get("copy_options")
            return result

        @builtins.property
        def data_table_columns(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.CopyCommandProperty.DataTableColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-datatablecolumns
            """
            result = self._values.get("data_table_columns")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CopyCommandProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.DataFormatConversionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "input_format_configuration": "inputFormatConfiguration",
            "output_format_configuration": "outputFormatConfiguration",
            "schema_configuration": "schemaConfiguration",
        },
    )
    class DataFormatConversionConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            input_format_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.InputFormatConfigurationProperty"]] = None,
            output_format_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.OutputFormatConfigurationProperty"]] = None,
            schema_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SchemaConfigurationProperty"]] = None,
        ) -> None:
            """
            :param enabled: ``CfnDeliveryStream.DataFormatConversionConfigurationProperty.Enabled``.
            :param input_format_configuration: ``CfnDeliveryStream.DataFormatConversionConfigurationProperty.InputFormatConfiguration``.
            :param output_format_configuration: ``CfnDeliveryStream.DataFormatConversionConfigurationProperty.OutputFormatConfiguration``.
            :param schema_configuration: ``CfnDeliveryStream.DataFormatConversionConfigurationProperty.SchemaConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if input_format_configuration is not None:
                self._values["input_format_configuration"] = input_format_configuration
            if output_format_configuration is not None:
                self._values["output_format_configuration"] = output_format_configuration
            if schema_configuration is not None:
                self._values["schema_configuration"] = schema_configuration

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDeliveryStream.DataFormatConversionConfigurationProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def input_format_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.InputFormatConfigurationProperty"]]:
            """``CfnDeliveryStream.DataFormatConversionConfigurationProperty.InputFormatConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-inputformatconfiguration
            """
            result = self._values.get("input_format_configuration")
            return result

        @builtins.property
        def output_format_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.OutputFormatConfigurationProperty"]]:
            """``CfnDeliveryStream.DataFormatConversionConfigurationProperty.OutputFormatConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-outputformatconfiguration
            """
            result = self._values.get("output_format_configuration")
            return result

        @builtins.property
        def schema_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SchemaConfigurationProperty"]]:
            """``CfnDeliveryStream.DataFormatConversionConfigurationProperty.SchemaConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-dataformatconversionconfiguration.html#cfn-kinesisfirehose-deliverystream-dataformatconversionconfiguration-schemaconfiguration
            """
            result = self._values.get("schema_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataFormatConversionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={"key_type": "keyType", "key_arn": "keyArn"},
    )
    class DeliveryStreamEncryptionConfigurationInputProperty:
        def __init__(
            self,
            *,
            key_type: builtins.str,
            key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param key_type: ``CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty.KeyType``.
            :param key_arn: ``CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty.KeyARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key_type": key_type,
            }
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def key_type(self) -> builtins.str:
            """``CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty.KeyType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput.html#cfn-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput-keytype
            """
            result = self._values.get("key_type")
            assert result is not None, "Required property 'key_type' is missing"
            return result

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty.KeyARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput.html#cfn-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput-keyarn
            """
            result = self._values.get("key_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeliveryStreamEncryptionConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.DeserializerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hive_json_ser_de": "hiveJsonSerDe",
            "open_x_json_ser_de": "openXJsonSerDe",
        },
    )
    class DeserializerProperty:
        def __init__(
            self,
            *,
            hive_json_ser_de: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HiveJsonSerDeProperty"]] = None,
            open_x_json_ser_de: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.OpenXJsonSerDeProperty"]] = None,
        ) -> None:
            """
            :param hive_json_ser_de: ``CfnDeliveryStream.DeserializerProperty.HiveJsonSerDe``.
            :param open_x_json_ser_de: ``CfnDeliveryStream.DeserializerProperty.OpenXJsonSerDe``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deserializer.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if hive_json_ser_de is not None:
                self._values["hive_json_ser_de"] = hive_json_ser_de
            if open_x_json_ser_de is not None:
                self._values["open_x_json_ser_de"] = open_x_json_ser_de

        @builtins.property
        def hive_json_ser_de(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HiveJsonSerDeProperty"]]:
            """``CfnDeliveryStream.DeserializerProperty.HiveJsonSerDe``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deserializer.html#cfn-kinesisfirehose-deliverystream-deserializer-hivejsonserde
            """
            result = self._values.get("hive_json_ser_de")
            return result

        @builtins.property
        def open_x_json_ser_de(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.OpenXJsonSerDeProperty"]]:
            """``CfnDeliveryStream.DeserializerProperty.OpenXJsonSerDe``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-deserializer.html#cfn-kinesisfirehose-deliverystream-deserializer-openxjsonserde
            """
            result = self._values.get("open_x_json_ser_de")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeserializerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchBufferingHintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interval_in_seconds": "intervalInSeconds",
            "size_in_m_bs": "sizeInMBs",
        },
    )
    class ElasticsearchBufferingHintsProperty:
        def __init__(
            self,
            *,
            interval_in_seconds: typing.Optional[jsii.Number] = None,
            size_in_m_bs: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param interval_in_seconds: ``CfnDeliveryStream.ElasticsearchBufferingHintsProperty.IntervalInSeconds``.
            :param size_in_m_bs: ``CfnDeliveryStream.ElasticsearchBufferingHintsProperty.SizeInMBs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if interval_in_seconds is not None:
                self._values["interval_in_seconds"] = interval_in_seconds
            if size_in_m_bs is not None:
                self._values["size_in_m_bs"] = size_in_m_bs

        @builtins.property
        def interval_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.ElasticsearchBufferingHintsProperty.IntervalInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html#cfn-kinesisfirehose-deliverystream-elasticsearchbufferinghints-intervalinseconds
            """
            result = self._values.get("interval_in_seconds")
            return result

        @builtins.property
        def size_in_m_bs(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.ElasticsearchBufferingHintsProperty.SizeInMBs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html#cfn-kinesisfirehose-deliverystream-elasticsearchbufferinghints-sizeinmbs
            """
            result = self._values.get("size_in_m_bs")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchBufferingHintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "index_name": "indexName",
            "role_arn": "roleArn",
            "s3_configuration": "s3Configuration",
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "cluster_endpoint": "clusterEndpoint",
            "domain_arn": "domainArn",
            "index_rotation_period": "indexRotationPeriod",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "s3_backup_mode": "s3BackupMode",
            "type_name": "typeName",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class ElasticsearchDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            index_name: builtins.str,
            role_arn: builtins.str,
            s3_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"],
            buffering_hints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ElasticsearchBufferingHintsProperty"]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]] = None,
            cluster_endpoint: typing.Optional[builtins.str] = None,
            domain_arn: typing.Optional[builtins.str] = None,
            index_rotation_period: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]] = None,
            retry_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ElasticsearchRetryOptionsProperty"]] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
            type_name: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.VpcConfigurationProperty"]] = None,
        ) -> None:
            """
            :param index_name: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.IndexName``.
            :param role_arn: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.RoleARN``.
            :param s3_configuration: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.S3Configuration``.
            :param buffering_hints: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.BufferingHints``.
            :param cloud_watch_logging_options: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.CloudWatchLoggingOptions``.
            :param cluster_endpoint: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.ClusterEndpoint``.
            :param domain_arn: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.DomainARN``.
            :param index_rotation_period: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.IndexRotationPeriod``.
            :param processing_configuration: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.ProcessingConfiguration``.
            :param retry_options: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.RetryOptions``.
            :param s3_backup_mode: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.S3BackupMode``.
            :param type_name: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.TypeName``.
            :param vpc_configuration: ``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.VpcConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "index_name": index_name,
                "role_arn": role_arn,
                "s3_configuration": s3_configuration,
            }
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if cluster_endpoint is not None:
                self._values["cluster_endpoint"] = cluster_endpoint
            if domain_arn is not None:
                self._values["domain_arn"] = domain_arn
            if index_rotation_period is not None:
                self._values["index_rotation_period"] = index_rotation_period
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode
            if type_name is not None:
                self._values["type_name"] = type_name
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def index_name(self) -> builtins.str:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.IndexName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-indexname
            """
            result = self._values.get("index_name")
            assert result is not None, "Required property 'index_name' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.S3Configuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-s3configuration
            """
            result = self._values.get("s3_configuration")
            assert result is not None, "Required property 's3_configuration' is missing"
            return result

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ElasticsearchBufferingHintsProperty"]]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.BufferingHints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-bufferinghints
            """
            result = self._values.get("buffering_hints")
            return result

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.CloudWatchLoggingOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-cloudwatchloggingoptions
            """
            result = self._values.get("cloud_watch_logging_options")
            return result

        @builtins.property
        def cluster_endpoint(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.ClusterEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-clusterendpoint
            """
            result = self._values.get("cluster_endpoint")
            return result

        @builtins.property
        def domain_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.DomainARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-domainarn
            """
            result = self._values.get("domain_arn")
            return result

        @builtins.property
        def index_rotation_period(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.IndexRotationPeriod``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-indexrotationperiod
            """
            result = self._values.get("index_rotation_period")
            return result

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.ProcessingConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-processingconfiguration
            """
            result = self._values.get("processing_configuration")
            return result

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ElasticsearchRetryOptionsProperty"]]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.RetryOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-retryoptions
            """
            result = self._values.get("retry_options")
            return result

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-s3backupmode
            """
            result = self._values.get("s3_backup_mode")
            return result

        @builtins.property
        def type_name(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.TypeName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-typename
            """
            result = self._values.get("type_name")
            return result

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.VpcConfigurationProperty"]]:
            """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.VpcConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-vpcconfiguration
            """
            result = self._values.get("vpc_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class ElasticsearchRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param duration_in_seconds: ``CfnDeliveryStream.ElasticsearchRetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchretryoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.ElasticsearchRetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchretryoptions.html#cfn-kinesisfirehose-deliverystream-elasticsearchretryoptions-durationinseconds
            """
            result = self._values.get("duration_in_seconds")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_encryption_config": "kmsEncryptionConfig",
            "no_encryption_config": "noEncryptionConfig",
        },
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_encryption_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.KMSEncryptionConfigProperty"]] = None,
            no_encryption_config: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param kms_encryption_config: ``CfnDeliveryStream.EncryptionConfigurationProperty.KMSEncryptionConfig``.
            :param no_encryption_config: ``CfnDeliveryStream.EncryptionConfigurationProperty.NoEncryptionConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if kms_encryption_config is not None:
                self._values["kms_encryption_config"] = kms_encryption_config
            if no_encryption_config is not None:
                self._values["no_encryption_config"] = no_encryption_config

        @builtins.property
        def kms_encryption_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.KMSEncryptionConfigProperty"]]:
            """``CfnDeliveryStream.EncryptionConfigurationProperty.KMSEncryptionConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html#cfn-kinesisfirehose-deliverystream-encryptionconfiguration-kmsencryptionconfig
            """
            result = self._values.get("kms_encryption_config")
            return result

        @builtins.property
        def no_encryption_config(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.EncryptionConfigurationProperty.NoEncryptionConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html#cfn-kinesisfirehose-deliverystream-encryptionconfiguration-noencryptionconfig
            """
            result = self._values.get("no_encryption_config")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "role_arn": "roleArn",
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "compression_format": "compressionFormat",
            "data_format_conversion_configuration": "dataFormatConversionConfiguration",
            "encryption_configuration": "encryptionConfiguration",
            "error_output_prefix": "errorOutputPrefix",
            "prefix": "prefix",
            "processing_configuration": "processingConfiguration",
            "s3_backup_configuration": "s3BackupConfiguration",
            "s3_backup_mode": "s3BackupMode",
        },
    )
    class ExtendedS3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_arn: builtins.str,
            role_arn: builtins.str,
            buffering_hints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.BufferingHintsProperty"]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]] = None,
            compression_format: typing.Optional[builtins.str] = None,
            data_format_conversion_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.DataFormatConversionConfigurationProperty"]] = None,
            encryption_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.EncryptionConfigurationProperty"]] = None,
            error_output_prefix: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            processing_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]] = None,
            s3_backup_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket_arn: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.BucketARN``.
            :param role_arn: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.RoleARN``.
            :param buffering_hints: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.BufferingHints``.
            :param cloud_watch_logging_options: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.CloudWatchLoggingOptions``.
            :param compression_format: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.CompressionFormat``.
            :param data_format_conversion_configuration: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.DataFormatConversionConfiguration``.
            :param encryption_configuration: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.EncryptionConfiguration``.
            :param error_output_prefix: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.ErrorOutputPrefix``.
            :param prefix: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.Prefix``.
            :param processing_configuration: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.ProcessingConfiguration``.
            :param s3_backup_configuration: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.S3BackupConfiguration``.
            :param s3_backup_mode: ``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_arn": bucket_arn,
                "role_arn": role_arn,
            }
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if compression_format is not None:
                self._values["compression_format"] = compression_format
            if data_format_conversion_configuration is not None:
                self._values["data_format_conversion_configuration"] = data_format_conversion_configuration
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if error_output_prefix is not None:
                self._values["error_output_prefix"] = error_output_prefix
            if prefix is not None:
                self._values["prefix"] = prefix
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if s3_backup_configuration is not None:
                self._values["s3_backup_configuration"] = s3_backup_configuration
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode

        @builtins.property
        def bucket_arn(self) -> builtins.str:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.BucketARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-bucketarn
            """
            result = self._values.get("bucket_arn")
            assert result is not None, "Required property 'bucket_arn' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.BufferingHintsProperty"]]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.BufferingHints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-bufferinghints
            """
            result = self._values.get("buffering_hints")
            return result

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.CloudWatchLoggingOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-cloudwatchloggingoptions
            """
            result = self._values.get("cloud_watch_logging_options")
            return result

        @builtins.property
        def compression_format(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.CompressionFormat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-compressionformat
            """
            result = self._values.get("compression_format")
            return result

        @builtins.property
        def data_format_conversion_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.DataFormatConversionConfigurationProperty"]]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.DataFormatConversionConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-dataformatconversionconfiguration
            """
            result = self._values.get("data_format_conversion_configuration")
            return result

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.EncryptionConfigurationProperty"]]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.EncryptionConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-encryptionconfiguration
            """
            result = self._values.get("encryption_configuration")
            return result

        @builtins.property
        def error_output_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.ErrorOutputPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-erroroutputprefix
            """
            result = self._values.get("error_output_prefix")
            return result

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-prefix
            """
            result = self._values.get("prefix")
            return result

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.ProcessingConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-processingconfiguration
            """
            result = self._values.get("processing_configuration")
            return result

        @builtins.property
        def s3_backup_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.S3BackupConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-s3backupconfiguration
            """
            result = self._values.get("s3_backup_configuration")
            return result

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-s3backupmode
            """
            result = self._values.get("s3_backup_mode")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtendedS3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.HiveJsonSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={"timestamp_formats": "timestampFormats"},
    )
    class HiveJsonSerDeProperty:
        def __init__(
            self,
            *,
            timestamp_formats: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param timestamp_formats: ``CfnDeliveryStream.HiveJsonSerDeProperty.TimestampFormats``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-hivejsonserde.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if timestamp_formats is not None:
                self._values["timestamp_formats"] = timestamp_formats

        @builtins.property
        def timestamp_formats(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDeliveryStream.HiveJsonSerDeProperty.TimestampFormats``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-hivejsonserde.html#cfn-kinesisfirehose-deliverystream-hivejsonserde-timestampformats
            """
            result = self._values.get("timestamp_formats")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HiveJsonSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.HttpEndpointCommonAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_value": "attributeValue",
        },
    )
    class HttpEndpointCommonAttributeProperty:
        def __init__(
            self,
            *,
            attribute_name: builtins.str,
            attribute_value: builtins.str,
        ) -> None:
            """
            :param attribute_name: ``CfnDeliveryStream.HttpEndpointCommonAttributeProperty.AttributeName``.
            :param attribute_value: ``CfnDeliveryStream.HttpEndpointCommonAttributeProperty.AttributeValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointcommonattribute.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "attribute_name": attribute_name,
                "attribute_value": attribute_value,
            }

        @builtins.property
        def attribute_name(self) -> builtins.str:
            """``CfnDeliveryStream.HttpEndpointCommonAttributeProperty.AttributeName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointcommonattribute.html#cfn-kinesisfirehose-deliverystream-httpendpointcommonattribute-attributename
            """
            result = self._values.get("attribute_name")
            assert result is not None, "Required property 'attribute_name' is missing"
            return result

        @builtins.property
        def attribute_value(self) -> builtins.str:
            """``CfnDeliveryStream.HttpEndpointCommonAttributeProperty.AttributeValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointcommonattribute.html#cfn-kinesisfirehose-deliverystream-httpendpointcommonattribute-attributevalue
            """
            result = self._values.get("attribute_value")
            assert result is not None, "Required property 'attribute_value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointCommonAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.HttpEndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"url": "url", "access_key": "accessKey", "name": "name"},
    )
    class HttpEndpointConfigurationProperty:
        def __init__(
            self,
            *,
            url: builtins.str,
            access_key: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param url: ``CfnDeliveryStream.HttpEndpointConfigurationProperty.Url``.
            :param access_key: ``CfnDeliveryStream.HttpEndpointConfigurationProperty.AccessKey``.
            :param name: ``CfnDeliveryStream.HttpEndpointConfigurationProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "url": url,
            }
            if access_key is not None:
                self._values["access_key"] = access_key
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def url(self) -> builtins.str:
            """``CfnDeliveryStream.HttpEndpointConfigurationProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointconfiguration-url
            """
            result = self._values.get("url")
            assert result is not None, "Required property 'url' is missing"
            return result

        @builtins.property
        def access_key(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.HttpEndpointConfigurationProperty.AccessKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointconfiguration-accesskey
            """
            result = self._values.get("access_key")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.HttpEndpointConfigurationProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointconfiguration-name
            """
            result = self._values.get("name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_configuration": "endpointConfiguration",
            "s3_configuration": "s3Configuration",
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "processing_configuration": "processingConfiguration",
            "request_configuration": "requestConfiguration",
            "retry_options": "retryOptions",
            "role_arn": "roleArn",
            "s3_backup_mode": "s3BackupMode",
        },
    )
    class HttpEndpointDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointConfigurationProperty"],
            s3_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"],
            buffering_hints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.BufferingHintsProperty"]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]] = None,
            processing_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]] = None,
            request_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointRequestConfigurationProperty"]] = None,
            retry_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.RetryOptionsProperty"]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param endpoint_configuration: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.EndpointConfiguration``.
            :param s3_configuration: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.S3Configuration``.
            :param buffering_hints: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.BufferingHints``.
            :param cloud_watch_logging_options: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.CloudWatchLoggingOptions``.
            :param processing_configuration: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.ProcessingConfiguration``.
            :param request_configuration: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.RequestConfiguration``.
            :param retry_options: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.RetryOptions``.
            :param role_arn: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.RoleARN``.
            :param s3_backup_mode: ``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint_configuration": endpoint_configuration,
                "s3_configuration": s3_configuration,
            }
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if request_configuration is not None:
                self._values["request_configuration"] = request_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode

        @builtins.property
        def endpoint_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointConfigurationProperty"]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.EndpointConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-endpointconfiguration
            """
            result = self._values.get("endpoint_configuration")
            assert result is not None, "Required property 'endpoint_configuration' is missing"
            return result

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.S3Configuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-s3configuration
            """
            result = self._values.get("s3_configuration")
            assert result is not None, "Required property 's3_configuration' is missing"
            return result

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.BufferingHintsProperty"]]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.BufferingHints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-bufferinghints
            """
            result = self._values.get("buffering_hints")
            return result

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.CloudWatchLoggingOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-cloudwatchloggingoptions
            """
            result = self._values.get("cloud_watch_logging_options")
            return result

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.ProcessingConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-processingconfiguration
            """
            result = self._values.get("processing_configuration")
            return result

        @builtins.property
        def request_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointRequestConfigurationProperty"]]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.RequestConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-requestconfiguration
            """
            result = self._values.get("request_configuration")
            return result

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.RetryOptionsProperty"]]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.RetryOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-retryoptions
            """
            result = self._values.get("retry_options")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration-s3backupmode
            """
            result = self._values.get("s3_backup_mode")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.HttpEndpointRequestConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_attributes": "commonAttributes",
            "content_encoding": "contentEncoding",
        },
    )
    class HttpEndpointRequestConfigurationProperty:
        def __init__(
            self,
            *,
            common_attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointCommonAttributeProperty"]]]] = None,
            content_encoding: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param common_attributes: ``CfnDeliveryStream.HttpEndpointRequestConfigurationProperty.CommonAttributes``.
            :param content_encoding: ``CfnDeliveryStream.HttpEndpointRequestConfigurationProperty.ContentEncoding``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointrequestconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if common_attributes is not None:
                self._values["common_attributes"] = common_attributes
            if content_encoding is not None:
                self._values["content_encoding"] = content_encoding

        @builtins.property
        def common_attributes(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.HttpEndpointCommonAttributeProperty"]]]]:
            """``CfnDeliveryStream.HttpEndpointRequestConfigurationProperty.CommonAttributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointrequestconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointrequestconfiguration-commonattributes
            """
            result = self._values.get("common_attributes")
            return result

        @builtins.property
        def content_encoding(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.HttpEndpointRequestConfigurationProperty.ContentEncoding``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-httpendpointrequestconfiguration.html#cfn-kinesisfirehose-deliverystream-httpendpointrequestconfiguration-contentencoding
            """
            result = self._values.get("content_encoding")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpEndpointRequestConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"deserializer": "deserializer"},
    )
    class InputFormatConfigurationProperty:
        def __init__(
            self,
            *,
            deserializer: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.DeserializerProperty"]] = None,
        ) -> None:
            """
            :param deserializer: ``CfnDeliveryStream.InputFormatConfigurationProperty.Deserializer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-inputformatconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if deserializer is not None:
                self._values["deserializer"] = deserializer

        @builtins.property
        def deserializer(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.DeserializerProperty"]]:
            """``CfnDeliveryStream.InputFormatConfigurationProperty.Deserializer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-inputformatconfiguration.html#cfn-kinesisfirehose-deliverystream-inputformatconfiguration-deserializer
            """
            result = self._values.get("deserializer")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputFormatConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.KMSEncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"awskms_key_arn": "awskmsKeyArn"},
    )
    class KMSEncryptionConfigProperty:
        def __init__(self, *, awskms_key_arn: builtins.str) -> None:
            """
            :param awskms_key_arn: ``CfnDeliveryStream.KMSEncryptionConfigProperty.AWSKMSKeyARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kmsencryptionconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "awskms_key_arn": awskms_key_arn,
            }

        @builtins.property
        def awskms_key_arn(self) -> builtins.str:
            """``CfnDeliveryStream.KMSEncryptionConfigProperty.AWSKMSKeyARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kmsencryptionconfig.html#cfn-kinesisfirehose-deliverystream-kmsencryptionconfig-awskmskeyarn
            """
            result = self._values.get("awskms_key_arn")
            assert result is not None, "Required property 'awskms_key_arn' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KMSEncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kinesis_stream_arn": "kinesisStreamArn", "role_arn": "roleArn"},
    )
    class KinesisStreamSourceConfigurationProperty:
        def __init__(
            self,
            *,
            kinesis_stream_arn: builtins.str,
            role_arn: builtins.str,
        ) -> None:
            """
            :param kinesis_stream_arn: ``CfnDeliveryStream.KinesisStreamSourceConfigurationProperty.KinesisStreamARN``.
            :param role_arn: ``CfnDeliveryStream.KinesisStreamSourceConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "kinesis_stream_arn": kinesis_stream_arn,
                "role_arn": role_arn,
            }

        @builtins.property
        def kinesis_stream_arn(self) -> builtins.str:
            """``CfnDeliveryStream.KinesisStreamSourceConfigurationProperty.KinesisStreamARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration-kinesisstreamarn
            """
            result = self._values.get("kinesis_stream_arn")
            assert result is not None, "Required property 'kinesis_stream_arn' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnDeliveryStream.KinesisStreamSourceConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.OpenXJsonSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "case_insensitive": "caseInsensitive",
            "column_to_json_key_mappings": "columnToJsonKeyMappings",
            "convert_dots_in_json_keys_to_underscores": "convertDotsInJsonKeysToUnderscores",
        },
    )
    class OpenXJsonSerDeProperty:
        def __init__(
            self,
            *,
            case_insensitive: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            column_to_json_key_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            convert_dots_in_json_keys_to_underscores: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param case_insensitive: ``CfnDeliveryStream.OpenXJsonSerDeProperty.CaseInsensitive``.
            :param column_to_json_key_mappings: ``CfnDeliveryStream.OpenXJsonSerDeProperty.ColumnToJsonKeyMappings``.
            :param convert_dots_in_json_keys_to_underscores: ``CfnDeliveryStream.OpenXJsonSerDeProperty.ConvertDotsInJsonKeysToUnderscores``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if case_insensitive is not None:
                self._values["case_insensitive"] = case_insensitive
            if column_to_json_key_mappings is not None:
                self._values["column_to_json_key_mappings"] = column_to_json_key_mappings
            if convert_dots_in_json_keys_to_underscores is not None:
                self._values["convert_dots_in_json_keys_to_underscores"] = convert_dots_in_json_keys_to_underscores

        @builtins.property
        def case_insensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDeliveryStream.OpenXJsonSerDeProperty.CaseInsensitive``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html#cfn-kinesisfirehose-deliverystream-openxjsonserde-caseinsensitive
            """
            result = self._values.get("case_insensitive")
            return result

        @builtins.property
        def column_to_json_key_mappings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnDeliveryStream.OpenXJsonSerDeProperty.ColumnToJsonKeyMappings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html#cfn-kinesisfirehose-deliverystream-openxjsonserde-columntojsonkeymappings
            """
            result = self._values.get("column_to_json_key_mappings")
            return result

        @builtins.property
        def convert_dots_in_json_keys_to_underscores(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDeliveryStream.OpenXJsonSerDeProperty.ConvertDotsInJsonKeysToUnderscores``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-openxjsonserde.html#cfn-kinesisfirehose-deliverystream-openxjsonserde-convertdotsinjsonkeystounderscores
            """
            result = self._values.get("convert_dots_in_json_keys_to_underscores")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenXJsonSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.OrcSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_size_bytes": "blockSizeBytes",
            "bloom_filter_columns": "bloomFilterColumns",
            "bloom_filter_false_positive_probability": "bloomFilterFalsePositiveProbability",
            "compression": "compression",
            "dictionary_key_threshold": "dictionaryKeyThreshold",
            "enable_padding": "enablePadding",
            "format_version": "formatVersion",
            "padding_tolerance": "paddingTolerance",
            "row_index_stride": "rowIndexStride",
            "stripe_size_bytes": "stripeSizeBytes",
        },
    )
    class OrcSerDeProperty:
        def __init__(
            self,
            *,
            block_size_bytes: typing.Optional[jsii.Number] = None,
            bloom_filter_columns: typing.Optional[typing.List[builtins.str]] = None,
            bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
            compression: typing.Optional[builtins.str] = None,
            dictionary_key_threshold: typing.Optional[jsii.Number] = None,
            enable_padding: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            format_version: typing.Optional[builtins.str] = None,
            padding_tolerance: typing.Optional[jsii.Number] = None,
            row_index_stride: typing.Optional[jsii.Number] = None,
            stripe_size_bytes: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param block_size_bytes: ``CfnDeliveryStream.OrcSerDeProperty.BlockSizeBytes``.
            :param bloom_filter_columns: ``CfnDeliveryStream.OrcSerDeProperty.BloomFilterColumns``.
            :param bloom_filter_false_positive_probability: ``CfnDeliveryStream.OrcSerDeProperty.BloomFilterFalsePositiveProbability``.
            :param compression: ``CfnDeliveryStream.OrcSerDeProperty.Compression``.
            :param dictionary_key_threshold: ``CfnDeliveryStream.OrcSerDeProperty.DictionaryKeyThreshold``.
            :param enable_padding: ``CfnDeliveryStream.OrcSerDeProperty.EnablePadding``.
            :param format_version: ``CfnDeliveryStream.OrcSerDeProperty.FormatVersion``.
            :param padding_tolerance: ``CfnDeliveryStream.OrcSerDeProperty.PaddingTolerance``.
            :param row_index_stride: ``CfnDeliveryStream.OrcSerDeProperty.RowIndexStride``.
            :param stripe_size_bytes: ``CfnDeliveryStream.OrcSerDeProperty.StripeSizeBytes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if block_size_bytes is not None:
                self._values["block_size_bytes"] = block_size_bytes
            if bloom_filter_columns is not None:
                self._values["bloom_filter_columns"] = bloom_filter_columns
            if bloom_filter_false_positive_probability is not None:
                self._values["bloom_filter_false_positive_probability"] = bloom_filter_false_positive_probability
            if compression is not None:
                self._values["compression"] = compression
            if dictionary_key_threshold is not None:
                self._values["dictionary_key_threshold"] = dictionary_key_threshold
            if enable_padding is not None:
                self._values["enable_padding"] = enable_padding
            if format_version is not None:
                self._values["format_version"] = format_version
            if padding_tolerance is not None:
                self._values["padding_tolerance"] = padding_tolerance
            if row_index_stride is not None:
                self._values["row_index_stride"] = row_index_stride
            if stripe_size_bytes is not None:
                self._values["stripe_size_bytes"] = stripe_size_bytes

        @builtins.property
        def block_size_bytes(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.OrcSerDeProperty.BlockSizeBytes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-blocksizebytes
            """
            result = self._values.get("block_size_bytes")
            return result

        @builtins.property
        def bloom_filter_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDeliveryStream.OrcSerDeProperty.BloomFilterColumns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-bloomfiltercolumns
            """
            result = self._values.get("bloom_filter_columns")
            return result

        @builtins.property
        def bloom_filter_false_positive_probability(
            self,
        ) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.OrcSerDeProperty.BloomFilterFalsePositiveProbability``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-bloomfilterfalsepositiveprobability
            """
            result = self._values.get("bloom_filter_false_positive_probability")
            return result

        @builtins.property
        def compression(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.OrcSerDeProperty.Compression``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-compression
            """
            result = self._values.get("compression")
            return result

        @builtins.property
        def dictionary_key_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.OrcSerDeProperty.DictionaryKeyThreshold``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-dictionarykeythreshold
            """
            result = self._values.get("dictionary_key_threshold")
            return result

        @builtins.property
        def enable_padding(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDeliveryStream.OrcSerDeProperty.EnablePadding``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-enablepadding
            """
            result = self._values.get("enable_padding")
            return result

        @builtins.property
        def format_version(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.OrcSerDeProperty.FormatVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-formatversion
            """
            result = self._values.get("format_version")
            return result

        @builtins.property
        def padding_tolerance(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.OrcSerDeProperty.PaddingTolerance``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-paddingtolerance
            """
            result = self._values.get("padding_tolerance")
            return result

        @builtins.property
        def row_index_stride(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.OrcSerDeProperty.RowIndexStride``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-rowindexstride
            """
            result = self._values.get("row_index_stride")
            return result

        @builtins.property
        def stripe_size_bytes(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.OrcSerDeProperty.StripeSizeBytes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-orcserde.html#cfn-kinesisfirehose-deliverystream-orcserde-stripesizebytes
            """
            result = self._values.get("stripe_size_bytes")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrcSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"serializer": "serializer"},
    )
    class OutputFormatConfigurationProperty:
        def __init__(
            self,
            *,
            serializer: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SerializerProperty"]] = None,
        ) -> None:
            """
            :param serializer: ``CfnDeliveryStream.OutputFormatConfigurationProperty.Serializer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-outputformatconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if serializer is not None:
                self._values["serializer"] = serializer

        @builtins.property
        def serializer(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SerializerProperty"]]:
            """``CfnDeliveryStream.OutputFormatConfigurationProperty.Serializer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-outputformatconfiguration.html#cfn-kinesisfirehose-deliverystream-outputformatconfiguration-serializer
            """
            result = self._values.get("serializer")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputFormatConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ParquetSerDeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_size_bytes": "blockSizeBytes",
            "compression": "compression",
            "enable_dictionary_compression": "enableDictionaryCompression",
            "max_padding_bytes": "maxPaddingBytes",
            "page_size_bytes": "pageSizeBytes",
            "writer_version": "writerVersion",
        },
    )
    class ParquetSerDeProperty:
        def __init__(
            self,
            *,
            block_size_bytes: typing.Optional[jsii.Number] = None,
            compression: typing.Optional[builtins.str] = None,
            enable_dictionary_compression: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            max_padding_bytes: typing.Optional[jsii.Number] = None,
            page_size_bytes: typing.Optional[jsii.Number] = None,
            writer_version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param block_size_bytes: ``CfnDeliveryStream.ParquetSerDeProperty.BlockSizeBytes``.
            :param compression: ``CfnDeliveryStream.ParquetSerDeProperty.Compression``.
            :param enable_dictionary_compression: ``CfnDeliveryStream.ParquetSerDeProperty.EnableDictionaryCompression``.
            :param max_padding_bytes: ``CfnDeliveryStream.ParquetSerDeProperty.MaxPaddingBytes``.
            :param page_size_bytes: ``CfnDeliveryStream.ParquetSerDeProperty.PageSizeBytes``.
            :param writer_version: ``CfnDeliveryStream.ParquetSerDeProperty.WriterVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if block_size_bytes is not None:
                self._values["block_size_bytes"] = block_size_bytes
            if compression is not None:
                self._values["compression"] = compression
            if enable_dictionary_compression is not None:
                self._values["enable_dictionary_compression"] = enable_dictionary_compression
            if max_padding_bytes is not None:
                self._values["max_padding_bytes"] = max_padding_bytes
            if page_size_bytes is not None:
                self._values["page_size_bytes"] = page_size_bytes
            if writer_version is not None:
                self._values["writer_version"] = writer_version

        @builtins.property
        def block_size_bytes(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.ParquetSerDeProperty.BlockSizeBytes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-blocksizebytes
            """
            result = self._values.get("block_size_bytes")
            return result

        @builtins.property
        def compression(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ParquetSerDeProperty.Compression``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-compression
            """
            result = self._values.get("compression")
            return result

        @builtins.property
        def enable_dictionary_compression(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDeliveryStream.ParquetSerDeProperty.EnableDictionaryCompression``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-enabledictionarycompression
            """
            result = self._values.get("enable_dictionary_compression")
            return result

        @builtins.property
        def max_padding_bytes(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.ParquetSerDeProperty.MaxPaddingBytes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-maxpaddingbytes
            """
            result = self._values.get("max_padding_bytes")
            return result

        @builtins.property
        def page_size_bytes(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.ParquetSerDeProperty.PageSizeBytes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-pagesizebytes
            """
            result = self._values.get("page_size_bytes")
            return result

        @builtins.property
        def writer_version(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.ParquetSerDeProperty.WriterVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-parquetserde.html#cfn-kinesisfirehose-deliverystream-parquetserde-writerversion
            """
            result = self._values.get("writer_version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParquetSerDeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "processors": "processors"},
    )
    class ProcessingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            processors: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessorProperty"]]]] = None,
        ) -> None:
            """
            :param enabled: ``CfnDeliveryStream.ProcessingConfigurationProperty.Enabled``.
            :param processors: ``CfnDeliveryStream.ProcessingConfigurationProperty.Processors``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if processors is not None:
                self._values["processors"] = processors

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDeliveryStream.ProcessingConfigurationProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html#cfn-kinesisfirehose-deliverystream-processingconfiguration-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def processors(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessorProperty"]]]]:
            """``CfnDeliveryStream.ProcessingConfigurationProperty.Processors``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html#cfn-kinesisfirehose-deliverystream-processingconfiguration-processors
            """
            result = self._values.get("processors")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessorParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ProcessorParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: builtins.str,
            parameter_value: builtins.str,
        ) -> None:
            """
            :param parameter_name: ``CfnDeliveryStream.ProcessorParameterProperty.ParameterName``.
            :param parameter_value: ``CfnDeliveryStream.ProcessorParameterProperty.ParameterValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "parameter_name": parameter_name,
                "parameter_value": parameter_value,
            }

        @builtins.property
        def parameter_name(self) -> builtins.str:
            """``CfnDeliveryStream.ProcessorParameterProperty.ParameterName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html#cfn-kinesisfirehose-deliverystream-processorparameter-parametername
            """
            result = self._values.get("parameter_name")
            assert result is not None, "Required property 'parameter_name' is missing"
            return result

        @builtins.property
        def parameter_value(self) -> builtins.str:
            """``CfnDeliveryStream.ProcessorParameterProperty.ParameterValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html#cfn-kinesisfirehose-deliverystream-processorparameter-parametervalue
            """
            result = self._values.get("parameter_value")
            assert result is not None, "Required property 'parameter_value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "parameters": "parameters"},
    )
    class ProcessorProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessorParameterProperty"]]]] = None,
        ) -> None:
            """
            :param type: ``CfnDeliveryStream.ProcessorProperty.Type``.
            :param parameters: ``CfnDeliveryStream.ProcessorProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnDeliveryStream.ProcessorProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html#cfn-kinesisfirehose-deliverystream-processor-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessorParameterProperty"]]]]:
            """``CfnDeliveryStream.ProcessorProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html#cfn-kinesisfirehose-deliverystream-processor-parameters
            """
            result = self._values.get("parameters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cluster_jdbcurl": "clusterJdbcurl",
            "copy_command": "copyCommand",
            "password": "password",
            "role_arn": "roleArn",
            "s3_configuration": "s3Configuration",
            "username": "username",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "s3_backup_configuration": "s3BackupConfiguration",
            "s3_backup_mode": "s3BackupMode",
        },
    )
    class RedshiftDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            cluster_jdbcurl: builtins.str,
            copy_command: typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CopyCommandProperty"],
            password: builtins.str,
            role_arn: builtins.str,
            s3_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"],
            username: builtins.str,
            cloud_watch_logging_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]] = None,
            processing_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]] = None,
            retry_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.RedshiftRetryOptionsProperty"]] = None,
            s3_backup_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param cluster_jdbcurl: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.ClusterJDBCURL``.
            :param copy_command: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.CopyCommand``.
            :param password: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.Password``.
            :param role_arn: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.RoleARN``.
            :param s3_configuration: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.S3Configuration``.
            :param username: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.Username``.
            :param cloud_watch_logging_options: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.CloudWatchLoggingOptions``.
            :param processing_configuration: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.ProcessingConfiguration``.
            :param retry_options: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.RetryOptions``.
            :param s3_backup_configuration: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.S3BackupConfiguration``.
            :param s3_backup_mode: ``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cluster_jdbcurl": cluster_jdbcurl,
                "copy_command": copy_command,
                "password": password,
                "role_arn": role_arn,
                "s3_configuration": s3_configuration,
                "username": username,
            }
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if s3_backup_configuration is not None:
                self._values["s3_backup_configuration"] = s3_backup_configuration
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode

        @builtins.property
        def cluster_jdbcurl(self) -> builtins.str:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.ClusterJDBCURL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-clusterjdbcurl
            """
            result = self._values.get("cluster_jdbcurl")
            assert result is not None, "Required property 'cluster_jdbcurl' is missing"
            return result

        @builtins.property
        def copy_command(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CopyCommandProperty"]:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.CopyCommand``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-copycommand
            """
            result = self._values.get("copy_command")
            assert result is not None, "Required property 'copy_command' is missing"
            return result

        @builtins.property
        def password(self) -> builtins.str:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.Password``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-password
            """
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.S3Configuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-s3configuration
            """
            result = self._values.get("s3_configuration")
            assert result is not None, "Required property 's3_configuration' is missing"
            return result

        @builtins.property
        def username(self) -> builtins.str:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-username
            """
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return result

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]]:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.CloudWatchLoggingOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-cloudwatchloggingoptions
            """
            result = self._values.get("cloud_watch_logging_options")
            return result

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]]:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.ProcessingConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-processingconfiguration
            """
            result = self._values.get("processing_configuration")
            return result

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.RedshiftRetryOptionsProperty"]]:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.RetryOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-retryoptions
            """
            result = self._values.get("retry_options")
            return result

        @builtins.property
        def s3_backup_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]]:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.S3BackupConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-s3backupconfiguration
            """
            result = self._values.get("s3_backup_configuration")
            return result

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-s3backupmode
            """
            result = self._values.get("s3_backup_mode")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.RedshiftRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class RedshiftRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param duration_in_seconds: ``CfnDeliveryStream.RedshiftRetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftretryoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.RedshiftRetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftretryoptions.html#cfn-kinesisfirehose-deliverystream-redshiftretryoptions-durationinseconds
            """
            result = self._values.get("duration_in_seconds")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.RetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class RetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param duration_in_seconds: ``CfnDeliveryStream.RetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-retryoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.RetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-retryoptions.html#cfn-kinesisfirehose-deliverystream-retryoptions-durationinseconds
            """
            result = self._values.get("duration_in_seconds")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "role_arn": "roleArn",
            "buffering_hints": "bufferingHints",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "compression_format": "compressionFormat",
            "encryption_configuration": "encryptionConfiguration",
            "error_output_prefix": "errorOutputPrefix",
            "prefix": "prefix",
        },
    )
    class S3DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_arn: builtins.str,
            role_arn: builtins.str,
            buffering_hints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.BufferingHintsProperty"]] = None,
            cloud_watch_logging_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]] = None,
            compression_format: typing.Optional[builtins.str] = None,
            encryption_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.EncryptionConfigurationProperty"]] = None,
            error_output_prefix: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket_arn: ``CfnDeliveryStream.S3DestinationConfigurationProperty.BucketARN``.
            :param role_arn: ``CfnDeliveryStream.S3DestinationConfigurationProperty.RoleARN``.
            :param buffering_hints: ``CfnDeliveryStream.S3DestinationConfigurationProperty.BufferingHints``.
            :param cloud_watch_logging_options: ``CfnDeliveryStream.S3DestinationConfigurationProperty.CloudWatchLoggingOptions``.
            :param compression_format: ``CfnDeliveryStream.S3DestinationConfigurationProperty.CompressionFormat``.
            :param encryption_configuration: ``CfnDeliveryStream.S3DestinationConfigurationProperty.EncryptionConfiguration``.
            :param error_output_prefix: ``CfnDeliveryStream.S3DestinationConfigurationProperty.ErrorOutputPrefix``.
            :param prefix: ``CfnDeliveryStream.S3DestinationConfigurationProperty.Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_arn": bucket_arn,
                "role_arn": role_arn,
            }
            if buffering_hints is not None:
                self._values["buffering_hints"] = buffering_hints
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if compression_format is not None:
                self._values["compression_format"] = compression_format
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if error_output_prefix is not None:
                self._values["error_output_prefix"] = error_output_prefix
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_arn(self) -> builtins.str:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.BucketARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-bucketarn
            """
            result = self._values.get("bucket_arn")
            assert result is not None, "Required property 'bucket_arn' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def buffering_hints(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.BufferingHintsProperty"]]:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.BufferingHints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-bufferinghints
            """
            result = self._values.get("buffering_hints")
            return result

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]]:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.CloudWatchLoggingOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-cloudwatchloggingoptions
            """
            result = self._values.get("cloud_watch_logging_options")
            return result

        @builtins.property
        def compression_format(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.CompressionFormat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-compressionformat
            """
            result = self._values.get("compression_format")
            return result

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.EncryptionConfigurationProperty"]]:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.EncryptionConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-encryptionconfiguration
            """
            result = self._values.get("encryption_configuration")
            return result

        @builtins.property
        def error_output_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.ErrorOutputPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-erroroutputprefix
            """
            result = self._values.get("error_output_prefix")
            return result

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.S3DestinationConfigurationProperty.Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-prefix
            """
            result = self._values.get("prefix")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SchemaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "region": "region",
            "role_arn": "roleArn",
            "table_name": "tableName",
            "version_id": "versionId",
        },
    )
    class SchemaConfigurationProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            version_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param catalog_id: ``CfnDeliveryStream.SchemaConfigurationProperty.CatalogId``.
            :param database_name: ``CfnDeliveryStream.SchemaConfigurationProperty.DatabaseName``.
            :param region: ``CfnDeliveryStream.SchemaConfigurationProperty.Region``.
            :param role_arn: ``CfnDeliveryStream.SchemaConfigurationProperty.RoleARN``.
            :param table_name: ``CfnDeliveryStream.SchemaConfigurationProperty.TableName``.
            :param version_id: ``CfnDeliveryStream.SchemaConfigurationProperty.VersionId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if region is not None:
                self._values["region"] = region
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if table_name is not None:
                self._values["table_name"] = table_name
            if version_id is not None:
                self._values["version_id"] = version_id

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.SchemaConfigurationProperty.CatalogId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-catalogid
            """
            result = self._values.get("catalog_id")
            return result

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.SchemaConfigurationProperty.DatabaseName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-databasename
            """
            result = self._values.get("database_name")
            return result

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.SchemaConfigurationProperty.Region``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-region
            """
            result = self._values.get("region")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.SchemaConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.SchemaConfigurationProperty.TableName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-tablename
            """
            result = self._values.get("table_name")
            return result

        @builtins.property
        def version_id(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.SchemaConfigurationProperty.VersionId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-schemaconfiguration.html#cfn-kinesisfirehose-deliverystream-schemaconfiguration-versionid
            """
            result = self._values.get("version_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SerializerProperty",
        jsii_struct_bases=[],
        name_mapping={"orc_ser_de": "orcSerDe", "parquet_ser_de": "parquetSerDe"},
    )
    class SerializerProperty:
        def __init__(
            self,
            *,
            orc_ser_de: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.OrcSerDeProperty"]] = None,
            parquet_ser_de: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ParquetSerDeProperty"]] = None,
        ) -> None:
            """
            :param orc_ser_de: ``CfnDeliveryStream.SerializerProperty.OrcSerDe``.
            :param parquet_ser_de: ``CfnDeliveryStream.SerializerProperty.ParquetSerDe``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-serializer.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if orc_ser_de is not None:
                self._values["orc_ser_de"] = orc_ser_de
            if parquet_ser_de is not None:
                self._values["parquet_ser_de"] = parquet_ser_de

        @builtins.property
        def orc_ser_de(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.OrcSerDeProperty"]]:
            """``CfnDeliveryStream.SerializerProperty.OrcSerDe``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-serializer.html#cfn-kinesisfirehose-deliverystream-serializer-orcserde
            """
            result = self._values.get("orc_ser_de")
            return result

        @builtins.property
        def parquet_ser_de(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ParquetSerDeProperty"]]:
            """``CfnDeliveryStream.SerializerProperty.ParquetSerDe``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-serializer.html#cfn-kinesisfirehose-deliverystream-serializer-parquetserde
            """
            result = self._values.get("parquet_ser_de")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SerializerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SplunkDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hec_endpoint": "hecEndpoint",
            "hec_endpoint_type": "hecEndpointType",
            "hec_token": "hecToken",
            "s3_configuration": "s3Configuration",
            "cloud_watch_logging_options": "cloudWatchLoggingOptions",
            "hec_acknowledgment_timeout_in_seconds": "hecAcknowledgmentTimeoutInSeconds",
            "processing_configuration": "processingConfiguration",
            "retry_options": "retryOptions",
            "s3_backup_mode": "s3BackupMode",
        },
    )
    class SplunkDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            hec_endpoint: builtins.str,
            hec_endpoint_type: builtins.str,
            hec_token: builtins.str,
            s3_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"],
            cloud_watch_logging_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]] = None,
            hec_acknowledgment_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            processing_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]] = None,
            retry_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SplunkRetryOptionsProperty"]] = None,
            s3_backup_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param hec_endpoint: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECEndpoint``.
            :param hec_endpoint_type: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECEndpointType``.
            :param hec_token: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECToken``.
            :param s3_configuration: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.S3Configuration``.
            :param cloud_watch_logging_options: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.CloudWatchLoggingOptions``.
            :param hec_acknowledgment_timeout_in_seconds: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECAcknowledgmentTimeoutInSeconds``.
            :param processing_configuration: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.ProcessingConfiguration``.
            :param retry_options: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.RetryOptions``.
            :param s3_backup_mode: ``CfnDeliveryStream.SplunkDestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "hec_endpoint": hec_endpoint,
                "hec_endpoint_type": hec_endpoint_type,
                "hec_token": hec_token,
                "s3_configuration": s3_configuration,
            }
            if cloud_watch_logging_options is not None:
                self._values["cloud_watch_logging_options"] = cloud_watch_logging_options
            if hec_acknowledgment_timeout_in_seconds is not None:
                self._values["hec_acknowledgment_timeout_in_seconds"] = hec_acknowledgment_timeout_in_seconds
            if processing_configuration is not None:
                self._values["processing_configuration"] = processing_configuration
            if retry_options is not None:
                self._values["retry_options"] = retry_options
            if s3_backup_mode is not None:
                self._values["s3_backup_mode"] = s3_backup_mode

        @builtins.property
        def hec_endpoint(self) -> builtins.str:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecendpoint
            """
            result = self._values.get("hec_endpoint")
            assert result is not None, "Required property 'hec_endpoint' is missing"
            return result

        @builtins.property
        def hec_endpoint_type(self) -> builtins.str:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECEndpointType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecendpointtype
            """
            result = self._values.get("hec_endpoint_type")
            assert result is not None, "Required property 'hec_endpoint_type' is missing"
            return result

        @builtins.property
        def hec_token(self) -> builtins.str:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECToken``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hectoken
            """
            result = self._values.get("hec_token")
            assert result is not None, "Required property 'hec_token' is missing"
            return result

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.S3DestinationConfigurationProperty"]:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.S3Configuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-s3configuration
            """
            result = self._values.get("s3_configuration")
            assert result is not None, "Required property 's3_configuration' is missing"
            return result

        @builtins.property
        def cloud_watch_logging_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]]:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.CloudWatchLoggingOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-cloudwatchloggingoptions
            """
            result = self._values.get("cloud_watch_logging_options")
            return result

        @builtins.property
        def hec_acknowledgment_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECAcknowledgmentTimeoutInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecacknowledgmenttimeoutinseconds
            """
            result = self._values.get("hec_acknowledgment_timeout_in_seconds")
            return result

        @builtins.property
        def processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.ProcessingConfigurationProperty"]]:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.ProcessingConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-processingconfiguration
            """
            result = self._values.get("processing_configuration")
            return result

        @builtins.property
        def retry_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDeliveryStream.SplunkRetryOptionsProperty"]]:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.RetryOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-retryoptions
            """
            result = self._values.get("retry_options")
            return result

        @builtins.property
        def s3_backup_mode(self) -> typing.Optional[builtins.str]:
            """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.S3BackupMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-s3backupmode
            """
            result = self._values.get("s3_backup_mode")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SplunkDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SplunkRetryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class SplunkRetryOptionsProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param duration_in_seconds: ``CfnDeliveryStream.SplunkRetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkretryoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnDeliveryStream.SplunkRetryOptionsProperty.DurationInSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkretryoptions.html#cfn-kinesisfirehose-deliverystream-splunkretryoptions-durationinseconds
            """
            result = self._values.get("duration_in_seconds")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SplunkRetryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            role_arn: builtins.str,
            security_group_ids: typing.List[builtins.str],
            subnet_ids: typing.List[builtins.str],
        ) -> None:
            """
            :param role_arn: ``CfnDeliveryStream.VpcConfigurationProperty.RoleARN``.
            :param security_group_ids: ``CfnDeliveryStream.VpcConfigurationProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnDeliveryStream.VpcConfigurationProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "role_arn": role_arn,
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnDeliveryStream.VpcConfigurationProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html#cfn-kinesisfirehose-deliverystream-vpcconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            """``CfnDeliveryStream.VpcConfigurationProperty.SecurityGroupIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html#cfn-kinesisfirehose-deliverystream-vpcconfiguration-securitygroupids
            """
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return result

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            """``CfnDeliveryStream.VpcConfigurationProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-vpcconfiguration.html#cfn-kinesisfirehose-deliverystream-vpcconfiguration-subnetids
            """
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_encryption_configuration_input": "deliveryStreamEncryptionConfigurationInput",
        "delivery_stream_name": "deliveryStreamName",
        "delivery_stream_type": "deliveryStreamType",
        "elasticsearch_destination_configuration": "elasticsearchDestinationConfiguration",
        "extended_s3_destination_configuration": "extendedS3DestinationConfiguration",
        "http_endpoint_destination_configuration": "httpEndpointDestinationConfiguration",
        "kinesis_stream_source_configuration": "kinesisStreamSourceConfiguration",
        "redshift_destination_configuration": "redshiftDestinationConfiguration",
        "s3_destination_configuration": "s3DestinationConfiguration",
        "splunk_destination_configuration": "splunkDestinationConfiguration",
        "tags": "tags",
    },
)
class CfnDeliveryStreamProps:
    def __init__(
        self,
        *,
        delivery_stream_encryption_configuration_input: typing.Optional[typing.Union[CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty, aws_cdk.core.IResolvable]] = None,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        delivery_stream_type: typing.Optional[builtins.str] = None,
        elasticsearch_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty]] = None,
        extended_s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty]] = None,
        http_endpoint_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty]] = None,
        kinesis_stream_source_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.KinesisStreamSourceConfigurationProperty]] = None,
        redshift_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.RedshiftDestinationConfigurationProperty]] = None,
        s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.S3DestinationConfigurationProperty]] = None,
        splunk_destination_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.SplunkDestinationConfigurationProperty]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::KinesisFirehose::DeliveryStream``.

        :param delivery_stream_encryption_configuration_input: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamEncryptionConfigurationInput``.
        :param delivery_stream_name: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamName``.
        :param delivery_stream_type: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamType``.
        :param elasticsearch_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.ElasticsearchDestinationConfiguration``.
        :param extended_s3_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.ExtendedS3DestinationConfiguration``.
        :param http_endpoint_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.HttpEndpointDestinationConfiguration``.
        :param kinesis_stream_source_configuration: ``AWS::KinesisFirehose::DeliveryStream.KinesisStreamSourceConfiguration``.
        :param redshift_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.RedshiftDestinationConfiguration``.
        :param s3_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.S3DestinationConfiguration``.
        :param splunk_destination_configuration: ``AWS::KinesisFirehose::DeliveryStream.SplunkDestinationConfiguration``.
        :param tags: ``AWS::KinesisFirehose::DeliveryStream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if delivery_stream_encryption_configuration_input is not None:
            self._values["delivery_stream_encryption_configuration_input"] = delivery_stream_encryption_configuration_input
        if delivery_stream_name is not None:
            self._values["delivery_stream_name"] = delivery_stream_name
        if delivery_stream_type is not None:
            self._values["delivery_stream_type"] = delivery_stream_type
        if elasticsearch_destination_configuration is not None:
            self._values["elasticsearch_destination_configuration"] = elasticsearch_destination_configuration
        if extended_s3_destination_configuration is not None:
            self._values["extended_s3_destination_configuration"] = extended_s3_destination_configuration
        if http_endpoint_destination_configuration is not None:
            self._values["http_endpoint_destination_configuration"] = http_endpoint_destination_configuration
        if kinesis_stream_source_configuration is not None:
            self._values["kinesis_stream_source_configuration"] = kinesis_stream_source_configuration
        if redshift_destination_configuration is not None:
            self._values["redshift_destination_configuration"] = redshift_destination_configuration
        if s3_destination_configuration is not None:
            self._values["s3_destination_configuration"] = s3_destination_configuration
        if splunk_destination_configuration is not None:
            self._values["splunk_destination_configuration"] = splunk_destination_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def delivery_stream_encryption_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[CfnDeliveryStream.DeliveryStreamEncryptionConfigurationInputProperty, aws_cdk.core.IResolvable]]:
        """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamEncryptionConfigurationInput``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamencryptionconfigurationinput
        """
        result = self._values.get("delivery_stream_encryption_configuration_input")
        return result

    @builtins.property
    def delivery_stream_name(self) -> typing.Optional[builtins.str]:
        """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamname
        """
        result = self._values.get("delivery_stream_name")
        return result

    @builtins.property
    def delivery_stream_type(self) -> typing.Optional[builtins.str]:
        """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamtype
        """
        result = self._values.get("delivery_stream_type")
        return result

    @builtins.property
    def elasticsearch_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty]]:
        """``AWS::KinesisFirehose::DeliveryStream.ElasticsearchDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration
        """
        result = self._values.get("elasticsearch_destination_configuration")
        return result

    @builtins.property
    def extended_s3_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty]]:
        """``AWS::KinesisFirehose::DeliveryStream.ExtendedS3DestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration
        """
        result = self._values.get("extended_s3_destination_configuration")
        return result

    @builtins.property
    def http_endpoint_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty]]:
        """``AWS::KinesisFirehose::DeliveryStream.HttpEndpointDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-httpendpointdestinationconfiguration
        """
        result = self._values.get("http_endpoint_destination_configuration")
        return result

    @builtins.property
    def kinesis_stream_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.KinesisStreamSourceConfigurationProperty]]:
        """``AWS::KinesisFirehose::DeliveryStream.KinesisStreamSourceConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration
        """
        result = self._values.get("kinesis_stream_source_configuration")
        return result

    @builtins.property
    def redshift_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.RedshiftDestinationConfigurationProperty]]:
        """``AWS::KinesisFirehose::DeliveryStream.RedshiftDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration
        """
        result = self._values.get("redshift_destination_configuration")
        return result

    @builtins.property
    def s3_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.S3DestinationConfigurationProperty]]:
        """``AWS::KinesisFirehose::DeliveryStream.S3DestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration
        """
        result = self._values.get("s3_destination_configuration")
        return result

    @builtins.property
    def splunk_destination_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnDeliveryStream.SplunkDestinationConfigurationProperty]]:
        """``AWS::KinesisFirehose::DeliveryStream.SplunkDestinationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration
        """
        result = self._values.get("splunk_destination_configuration")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::KinesisFirehose::DeliveryStream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeliveryStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDeliveryStream",
    "CfnDeliveryStreamProps",
]

publication.publish()
