"""
## Amazon Kinesis Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

[Amazon Kinesis](https://docs.aws.amazon.com/streams/latest/dev/introduction.html) provides collection and processing of large
[streams](https://aws.amazon.com/streaming-data/) of data records in real time. Kinesis data streams can be used for rapid and continuous data
intake and aggregation.

## Table Of Contents

* [Streams](#streams)

  * [Encryption](#encryption)
  * [Import](#import)
  * [Permission Grants](#permission-grants)

    * [Read Permissions](#read-permissions)
    * [Write Permissions](#write-permissions)
    * [Custom Permissions](#custom-permissions)

## Streams

Amazon Kinesis Data Streams ingests a large amount of data in real time, durably stores the data, and makes the data available for consumption.

Using the CDK, a new Kinesis stream can be created as part of the stack using the construct's constructor. You may specify the `streamName` to give
your own identifier to the stream. If not, CloudFormation will generate a name.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Stream(self, "MyFirstStream",
    stream_name="my-awesome-stream"
)
```

You can also specify properties such as `shardCount` to indicate how many shards the stream should choose and a `retentionPeriod`
to specify how long the data in the shards should remain accessible.
Read more at [Creating and Managing Streams](https://docs.aws.amazon.com/streams/latest/dev/working-with-streams.html)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Stream(self, "MyFirstStream",
    stream_name="my-awesome-stream",
    shard_count=3,
    retention_period=Duration.hours(48)
)
```

### Encryption

[Stream encryption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html) enables
server-side encryption using an AWS KMS key for a specified stream.

Encryption is enabled by default on your stream with the master key owned by Kinesis Data Streams in regions where it is supported.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Stream(self, "MyEncryptedStream")
```

You can enable encryption on your stream with a user-managed key by specifying the `encryption` property.
A KMS key will be created for you and associated with the stream.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.KMS
)
```

You can also supply your own external KMS key to use for stream encryption by specifying the `encryptionKey` property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_kms as kms

key = kms.Key(self, "MyKey")

Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.KMS,
    encryption_key=key
)
```

### Import

Any Kinesis stream that has been created outside the stack can be imported into your CDK app.

Streams can be imported by their ARN via the `Stream.fromStreamArn()` API

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stack = Stack(app, "MyStack")

imported_stream = Stream.from_stream_arn(stack, "ImportedStream", "arn:aws:kinesis:us-east-2:123456789012:stream/f3j09j2230j")
```

Encrypted Streams can also be imported by their attributes via the `Stream.fromStreamAttributes()` API

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_kms import Key

stack = Stack(app, "MyStack")

imported_stream = Stream.from_stream_attributes(stack, "ImportedEncryptedStream",
    stream_arn="arn:aws:kinesis:us-east-2:123456789012:stream/f3j09j2230j",
    encryption_key=kms.Key.from_key_arn("arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012")
)
```

### Permission Grants

IAM roles, users or groups which need to be able to work with Amazon Kinesis streams at runtime should be granted IAM permissions.

Any object that implements the `IGrantable` interface (has an associated principal) can be granted permissions by calling:

* `grantRead(principal)` - grants the principal read access
* `grantWrite(principal)` - grants the principal write permissions to a Stream
* `grantReadWrite(principal)` - grants principal read and write permissions

#### Read Permissions

Grant `read` access to a stream by calling the `grantRead()` API.
If the stream has an encryption key, read permissions will also be granted to the key.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
    description="Example role..."
)

stream = Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.KMS
)

# give lambda permissions to read stream
stream.grant_read(lambda_role)
```

The following read permissions are provided to a service principal by the `grantRead()` API:

* `kinesis:DescribeStreamSummary`
* `kinesis:GetRecords`
* `kinesis:GetShardIterator`
* `kinesis:ListShards`
* `kinesis:SubscribeToShard`

#### Write Permissions

Grant `write` permissions to a stream is provided by calling the `grantWrite()` API.
If the stream has an encryption key, write permissions will also be granted to the key.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
    description="Example role..."
)

stream = Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.KMS
)

# give lambda permissions to write to stream
stream.grant_write(lambda_role)
```

The following write permissions are provided to a service principal by the `grantWrite()` API:

* `kinesis:ListShards`
* `kinesis:PutRecord`
* `kinesis:PutRecords`

#### Custom Permissions

You can add any set of permissions to a stream by calling the `grant()` API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user = iam.User(stack, "MyUser")

stream = Stream(stack, "MyStream")

# give my user permissions to list shards
stream.grant(user, "kinesis:ListShards")
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
import aws_cdk.aws_kms
import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStream(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesis.CfnStream",
):
    """A CloudFormation ``AWS::Kinesis::Stream``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
    :cloudformationResource: AWS::Kinesis::Stream
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        shard_count: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        retention_period_hours: typing.Optional[jsii.Number] = None,
        stream_encryption: typing.Optional[typing.Union["CfnStream.StreamEncryptionProperty", aws_cdk.core.IResolvable]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::Kinesis::Stream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param shard_count: ``AWS::Kinesis::Stream.ShardCount``.
        :param name: ``AWS::Kinesis::Stream.Name``.
        :param retention_period_hours: ``AWS::Kinesis::Stream.RetentionPeriodHours``.
        :param stream_encryption: ``AWS::Kinesis::Stream.StreamEncryption``.
        :param tags: ``AWS::Kinesis::Stream.Tags``.
        """
        props = CfnStreamProps(
            shard_count=shard_count,
            name=name,
            retention_period_hours=retention_period_hours,
            stream_encryption=stream_encryption,
            tags=tags,
        )

        jsii.create(CfnStream, self, [scope, id, props])

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
        """``AWS::Kinesis::Stream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        """``AWS::Kinesis::Stream.ShardCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-shardcount
        """
        return jsii.get(self, "shardCount")

    @shard_count.setter # type: ignore
    def shard_count(self, value: jsii.Number) -> None:
        jsii.set(self, "shardCount", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Kinesis::Stream.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="retentionPeriodHours")
    def retention_period_hours(self) -> typing.Optional[jsii.Number]:
        """``AWS::Kinesis::Stream.RetentionPeriodHours``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-retentionperiodhours
        """
        return jsii.get(self, "retentionPeriodHours")

    @retention_period_hours.setter # type: ignore
    def retention_period_hours(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "retentionPeriodHours", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamEncryption")
    def stream_encryption(
        self,
    ) -> typing.Optional[typing.Union["CfnStream.StreamEncryptionProperty", aws_cdk.core.IResolvable]]:
        """``AWS::Kinesis::Stream.StreamEncryption``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-streamencryption
        """
        return jsii.get(self, "streamEncryption")

    @stream_encryption.setter # type: ignore
    def stream_encryption(
        self,
        value: typing.Optional[typing.Union["CfnStream.StreamEncryptionProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "streamEncryption", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kinesis.CfnStream.StreamEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "key_id": "keyId"},
    )
    class StreamEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_type: builtins.str,
            key_id: builtins.str,
        ) -> None:
            """
            :param encryption_type: ``CfnStream.StreamEncryptionProperty.EncryptionType``.
            :param key_id: ``CfnStream.StreamEncryptionProperty.KeyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "encryption_type": encryption_type,
                "key_id": key_id,
            }

        @builtins.property
        def encryption_type(self) -> builtins.str:
            """``CfnStream.StreamEncryptionProperty.EncryptionType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-encryptiontype
            """
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return result

        @builtins.property
        def key_id(self) -> builtins.str:
            """``CfnStream.StreamEncryptionProperty.KeyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-keyid
            """
            result = self._values.get("key_id")
            assert result is not None, "Required property 'key_id' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStreamConsumer(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesis.CfnStreamConsumer",
):
    """A CloudFormation ``AWS::Kinesis::StreamConsumer``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
    :cloudformationResource: AWS::Kinesis::StreamConsumer
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        consumer_name: builtins.str,
        stream_arn: builtins.str,
    ) -> None:
        """Create a new ``AWS::Kinesis::StreamConsumer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param consumer_name: ``AWS::Kinesis::StreamConsumer.ConsumerName``.
        :param stream_arn: ``AWS::Kinesis::StreamConsumer.StreamARN``.
        """
        props = CfnStreamConsumerProps(
            consumer_name=consumer_name, stream_arn=stream_arn
        )

        jsii.create(CfnStreamConsumer, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrConsumerArn")
    def attr_consumer_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ConsumerARN
        """
        return jsii.get(self, "attrConsumerArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConsumerCreationTimestamp")
    def attr_consumer_creation_timestamp(self) -> builtins.str:
        """
        :cloudformationAttribute: ConsumerCreationTimestamp
        """
        return jsii.get(self, "attrConsumerCreationTimestamp")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConsumerName")
    def attr_consumer_name(self) -> builtins.str:
        """
        :cloudformationAttribute: ConsumerName
        """
        return jsii.get(self, "attrConsumerName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConsumerStatus")
    def attr_consumer_status(self) -> builtins.str:
        """
        :cloudformationAttribute: ConsumerStatus
        """
        return jsii.get(self, "attrConsumerStatus")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrStreamArn")
    def attr_stream_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: StreamARN
        """
        return jsii.get(self, "attrStreamArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="consumerName")
    def consumer_name(self) -> builtins.str:
        """``AWS::Kinesis::StreamConsumer.ConsumerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-consumername
        """
        return jsii.get(self, "consumerName")

    @consumer_name.setter # type: ignore
    def consumer_name(self, value: builtins.str) -> None:
        jsii.set(self, "consumerName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        """``AWS::Kinesis::StreamConsumer.StreamARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-streamarn
        """
        return jsii.get(self, "streamArn")

    @stream_arn.setter # type: ignore
    def stream_arn(self, value: builtins.str) -> None:
        jsii.set(self, "streamArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesis.CfnStreamConsumerProps",
    jsii_struct_bases=[],
    name_mapping={"consumer_name": "consumerName", "stream_arn": "streamArn"},
)
class CfnStreamConsumerProps:
    def __init__(
        self,
        *,
        consumer_name: builtins.str,
        stream_arn: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::Kinesis::StreamConsumer``.

        :param consumer_name: ``AWS::Kinesis::StreamConsumer.ConsumerName``.
        :param stream_arn: ``AWS::Kinesis::StreamConsumer.StreamARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "consumer_name": consumer_name,
            "stream_arn": stream_arn,
        }

    @builtins.property
    def consumer_name(self) -> builtins.str:
        """``AWS::Kinesis::StreamConsumer.ConsumerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-consumername
        """
        result = self._values.get("consumer_name")
        assert result is not None, "Required property 'consumer_name' is missing"
        return result

    @builtins.property
    def stream_arn(self) -> builtins.str:
        """``AWS::Kinesis::StreamConsumer.StreamARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-streamarn
        """
        result = self._values.get("stream_arn")
        assert result is not None, "Required property 'stream_arn' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamConsumerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesis.CfnStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "shard_count": "shardCount",
        "name": "name",
        "retention_period_hours": "retentionPeriodHours",
        "stream_encryption": "streamEncryption",
        "tags": "tags",
    },
)
class CfnStreamProps:
    def __init__(
        self,
        *,
        shard_count: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        retention_period_hours: typing.Optional[jsii.Number] = None,
        stream_encryption: typing.Optional[typing.Union[CfnStream.StreamEncryptionProperty, aws_cdk.core.IResolvable]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Kinesis::Stream``.

        :param shard_count: ``AWS::Kinesis::Stream.ShardCount``.
        :param name: ``AWS::Kinesis::Stream.Name``.
        :param retention_period_hours: ``AWS::Kinesis::Stream.RetentionPeriodHours``.
        :param stream_encryption: ``AWS::Kinesis::Stream.StreamEncryption``.
        :param tags: ``AWS::Kinesis::Stream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "shard_count": shard_count,
        }
        if name is not None:
            self._values["name"] = name
        if retention_period_hours is not None:
            self._values["retention_period_hours"] = retention_period_hours
        if stream_encryption is not None:
            self._values["stream_encryption"] = stream_encryption
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def shard_count(self) -> jsii.Number:
        """``AWS::Kinesis::Stream.ShardCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-shardcount
        """
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Kinesis::Stream.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def retention_period_hours(self) -> typing.Optional[jsii.Number]:
        """``AWS::Kinesis::Stream.RetentionPeriodHours``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-retentionperiodhours
        """
        result = self._values.get("retention_period_hours")
        return result

    @builtins.property
    def stream_encryption(
        self,
    ) -> typing.Optional[typing.Union[CfnStream.StreamEncryptionProperty, aws_cdk.core.IResolvable]]:
        """``AWS::Kinesis::Stream.StreamEncryption``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-streamencryption
        """
        result = self._values.get("stream_encryption")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Kinesis::Stream.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-kinesis.IStream")
class IStream(aws_cdk.core.IResource, typing_extensions.Protocol):
    """A Kinesis Stream."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStreamProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        """The ARN of the stream.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        """The name of the stream.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this stream."""
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the indicated permissions on this stream to the provided IAM principal.

        :param grantee: -
        :param actions: -
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -
        """
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param grantee: -
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to encrypt the
        contents of the stream will also be granted.

        :param grantee: -
        """
        ...


class _IStreamProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """A Kinesis Stream."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-kinesis.IStream"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        """The ARN of the stream.

        :attribute: true
        """
        return jsii.get(self, "streamArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        """The name of the stream.

        :attribute: true
        """
        return jsii.get(self, "streamName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this stream."""
        return jsii.get(self, "encryptionKey")

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the indicated permissions on this stream to the provided IAM principal.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param grantee: -
        """
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to encrypt the
        contents of the stream will also be granted.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])


@jsii.implements(IStream)
class Stream(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesis.Stream",
):
    """A Kinesis stream.

    Can be encrypted with a KMS key.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        encryption: typing.Optional["StreamEncryption"] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        retention_period: typing.Optional[aws_cdk.core.Duration] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param encryption: The kind of server-side encryption to apply to this stream. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - StreamEncryption.KMS if encrypted Streams are supported in the region or StreamEncryption.UNENCRYPTED otherwise. StreamEncryption.KMS if an encryption key is supplied through the encryptionKey property
        :param encryption_key: External KMS key to use for stream encryption. The 'encryption' property must be set to "Kms". Default: - Kinesis Data Streams master key ('/alias/aws/kinesis'). If encryption is set to StreamEncryption.KMS and this property is undefined, a new KMS key will be created and associated with this stream.
        :param retention_period: The number of hours for the data records that are stored in shards to remain accessible. Default: Duration.hours(24)
        :param shard_count: The number of shards for the stream. Default: 1
        :param stream_name: Enforces a particular physical stream name. Default: 
        """
        props = StreamProps(
            encryption=encryption,
            encryption_key=encryption_key,
            retention_period=retention_period,
            shard_count=shard_count,
            stream_name=stream_name,
        )

        jsii.create(Stream, self, [scope, id, props])

    @jsii.member(jsii_name="fromStreamArn")
    @builtins.classmethod
    def from_stream_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        stream_arn: builtins.str,
    ) -> IStream:
        """Import an existing Kinesis Stream provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param stream_arn: Stream ARN (i.e. arn:aws:kinesis:::stream/Foo).
        """
        return jsii.sinvoke(cls, "fromStreamArn", [scope, id, stream_arn])

    @jsii.member(jsii_name="fromStreamAttributes")
    @builtins.classmethod
    def from_stream_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        stream_arn: builtins.str,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> IStream:
        """Creates a Stream construct that represents an external stream.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param stream_arn: The ARN of the stream.
        :param encryption_key: The KMS key securing the contents of the stream if encryption is enabled. Default: - No encryption
        """
        attrs = StreamAttributes(stream_arn=stream_arn, encryption_key=encryption_key)

        return jsii.sinvoke(cls, "fromStreamAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the indicated permissions on this stream to the given IAM principal (Role/Group/User).

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param grantee: -
        """
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        """The ARN of the stream."""
        return jsii.get(self, "streamArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        """The name of the stream."""
        return jsii.get(self, "streamName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this stream."""
        return jsii.get(self, "encryptionKey")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesis.StreamAttributes",
    jsii_struct_bases=[],
    name_mapping={"stream_arn": "streamArn", "encryption_key": "encryptionKey"},
)
class StreamAttributes:
    def __init__(
        self,
        *,
        stream_arn: builtins.str,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """A reference to a stream.

        The easiest way to instantiate is to call
        ``stream.export()``. Then, the consumer can use ``Stream.import(this, ref)`` and
        get a ``Stream``.

        :param stream_arn: The ARN of the stream.
        :param encryption_key: The KMS key securing the contents of the stream if encryption is enabled. Default: - No encryption
        """
        self._values: typing.Dict[str, typing.Any] = {
            "stream_arn": stream_arn,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def stream_arn(self) -> builtins.str:
        """The ARN of the stream."""
        result = self._values.get("stream_arn")
        assert result is not None, "Required property 'stream_arn' is missing"
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key securing the contents of the stream if encryption is enabled.

        :default: - No encryption
        """
        result = self._values.get("encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-kinesis.StreamEncryption")
class StreamEncryption(enum.Enum):
    """What kind of server-side encryption to apply to this stream."""

    UNENCRYPTED = "UNENCRYPTED"
    """Records in the stream are not encrypted."""
    KMS = "KMS"
    """Server-side encryption with a KMS key managed by the user.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.
    """
    MANAGED = "MANAGED"
    """Server-side encryption with a master key managed by Amazon Kinesis."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesis.StreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "retention_period": "retentionPeriod",
        "shard_count": "shardCount",
        "stream_name": "streamName",
    },
)
class StreamProps:
    def __init__(
        self,
        *,
        encryption: typing.Optional[StreamEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        retention_period: typing.Optional[aws_cdk.core.Duration] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for a Kinesis Stream.

        :param encryption: The kind of server-side encryption to apply to this stream. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - StreamEncryption.KMS if encrypted Streams are supported in the region or StreamEncryption.UNENCRYPTED otherwise. StreamEncryption.KMS if an encryption key is supplied through the encryptionKey property
        :param encryption_key: External KMS key to use for stream encryption. The 'encryption' property must be set to "Kms". Default: - Kinesis Data Streams master key ('/alias/aws/kinesis'). If encryption is set to StreamEncryption.KMS and this property is undefined, a new KMS key will be created and associated with this stream.
        :param retention_period: The number of hours for the data records that are stored in shards to remain accessible. Default: Duration.hours(24)
        :param shard_count: The number of shards for the stream. Default: 1
        :param stream_name: Enforces a particular physical stream name. Default: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if shard_count is not None:
            self._values["shard_count"] = shard_count
        if stream_name is not None:
            self._values["stream_name"] = stream_name

    @builtins.property
    def encryption(self) -> typing.Optional[StreamEncryption]:
        """The kind of server-side encryption to apply to this stream.

        If you choose KMS, you can specify a KMS key via ``encryptionKey``. If
        encryption key is not specified, a key will automatically be created.

        :default:

        - StreamEncryption.KMS if encrypted Streams are supported in the region
        or StreamEncryption.UNENCRYPTED otherwise.
        StreamEncryption.KMS if an encryption key is supplied through the encryptionKey property
        """
        result = self._values.get("encryption")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """External KMS key to use for stream encryption.

        The 'encryption' property must be set to "Kms".

        :default:

        - Kinesis Data Streams master key ('/alias/aws/kinesis').
        If encryption is set to StreamEncryption.KMS and this property is undefined, a new KMS key
        will be created and associated with this stream.
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def retention_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of hours for the data records that are stored in shards to remain accessible.

        :default: Duration.hours(24)
        """
        result = self._values.get("retention_period")
        return result

    @builtins.property
    def shard_count(self) -> typing.Optional[jsii.Number]:
        """The number of shards for the stream.

        :default: 1
        """
        result = self._values.get("shard_count")
        return result

    @builtins.property
    def stream_name(self) -> typing.Optional[builtins.str]:
        """Enforces a particular physical stream name.

        :default:
        """
        result = self._values.get("stream_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnStream",
    "CfnStreamConsumer",
    "CfnStreamConsumerProps",
    "CfnStreamProps",
    "IStream",
    "Stream",
    "StreamAttributes",
    "StreamEncryption",
    "StreamProps",
]

publication.publish()
