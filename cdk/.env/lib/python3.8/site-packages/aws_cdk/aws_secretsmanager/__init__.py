"""
## AWS Secrets Manager Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_secretsmanager as secretsmanager
```

### Create a new Secret in a Stack

In order to have SecretsManager generate a new secret value automatically,
you can get started with the following:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Default secret
secret = secretsmanager.Secret(self, "Secret")
secret.grant_read(role)

iam.User(self, "User",
    password=secret.secret_value
)

# Templated secret
templated_secret = secretsmanager.Secret(self, "TemplatedSecret",
    generate_secret_string=SecretStringGenerator(
        secret_string_template=JSON.stringify(username="user"),
        generate_string_key="password"
    )
)

iam.User(self, "OtherUser",
    user_name=templated_secret.secret_value_from_json("username").to_string(),
    password=templated_secret.secret_value_from_json("password")
)
```

The `Secret` construct does not allow specifying the `SecretString` property
of the `AWS::SecretsManager::Secret` resource (as this will almost always
lead to the secret being surfaced in plain text and possibly committed to
your source control).

If you need to use a pre-existing secret, the recommended way is to manually
provision the secret in *AWS SecretsManager* and use the `Secret.fromSecretArn`
or `Secret.fromSecretAttributes` method to make it available in your CDK Application:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
secret = secretsmanager.Secret.from_secret_attributes(scope, "ImportedSecret",
    secret_arn="arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name>-<random-6-characters>",
    # If the secret is encrypted using a KMS-hosted CMK, either import or reference that key:
    encryption_key=encryption_key
)
```

SecretsManager secret values can only be used in select set of properties. For the
list of properties, see [the CloudFormation Dynamic References documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html).

A secret can set `RemovalPolicy`. If it set to `RETAIN`, that removing a secret will fail.

### Grant permission to use the secret to a role

You must grant permission to a resource for that resource to be allowed to
use a secret. This can be achieved with the `Secret.grantRead` and/or `Secret.grantUpdate`
method, depending on your need:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
role = iam.Role(stack, "SomeRole", assumed_by=iam.AccountRootPrincipal())
secret = secretsmanager.Secret(stack, "Secret")
secret.grant_read(role)
secret.grant_write(role)
```

If, as in the following example, your secret was created with a KMS key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
key = kms.Key(stack, "KMS")
secret = secretsmanager.Secret(stack, "Secret", encryption_key=key)
secret.grant_read(role)
secret.grant_write(role)
```

then `Secret.grantRead` and `Secret.grantWrite` will also grant the role the
relevant encrypt and decrypt permissions to the KMS key through the
SecretsManager service principal.

### Rotating a Secret

#### Using a Custom Lambda Function

A rotation schedule can be added to a Secret using a custom Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fn = lambda_.Function(...)
secret = secretsmanager.Secret(self, "Secret")

secret.add_rotation_schedule("RotationSchedule",
    rotation_lambda=fn,
    automatically_after=Duration.days(15)
)
```

See [Overview of the Lambda Rotation Function](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-lambda-function-overview.html) on how to implement a Lambda Rotation Function.

#### Using a Hosted Lambda Function

Use the `hostedRotation` prop to rotate a secret with a hosted Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
secret = secretsmanager.Secret(self, "Secret")

secret.add_rotation_schedule("RotationSchedule",
    hosted_rotation=secretsmanager.HostedRotation.mysql_single_user()
)
```

Hosted rotation is available for secrets representing credentials for MySQL, PostgreSQL, Oracle,
MariaDB, SQLServer, Redshift and MongoDB (both for the single and multi user schemes).

When deployed in a VPC, the hosted rotation implements `ec2.IConnectable`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_hosted_rotation = secretsmanager.HostedRotation.mysql_single_user(vpc=my_vpc)
secret.add_rotation_schedule("RotationSchedule", hosted_rotation=my_hosted_rotation)
db_connections.allow_default_port_from(hosted_rotation)
```

See also [Automating secret creation in AWS CloudFormation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_cloudformation.html).

### Rotating database credentials

Define a `SecretRotation` to rotate database credentials:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
secretsmanager.SecretRotation(self, "SecretRotation",
    application=secretsmanager.SecretRotationApplication.MYSQL_ROTATION_SINGLE_USER, # MySQL single user scheme
    secret=my_secret,
    target=my_database, # a Connectable
    vpc=my_vpc, # The VPC where the secret rotation application will be deployed
    exclude_characters=" %+:;{}"
)
```

The secret must be a JSON string with the following format:

```json
{
  "engine": "<required: database engine>",
  "host": "<required: instance host name>",
  "username": "<required: username>",
  "password": "<required: password>",
  "dbname": "<optional: database name>",
  "port": "<optional: if not specified, default port will be used>",
  "masterarn": "<required for multi user rotation: the arn of the master secret which will be used to create users/change passwords>"
}
```

For the multi user scheme, a `masterSecret` must be specified:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
secretsmanager.SecretRotation(stack, "SecretRotation",
    application=secretsmanager.SecretRotationApplication.MYSQL_ROTATION_MULTI_USER,
    secret=my_user_secret, # The secret that will be rotated
    master_secret=my_master_secret, # The secret used for the rotation
    target=my_database,
    vpc=my_vpc
)
```

See also [aws-rds](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-rds/README.md) where
credentials generation and rotation is integrated.

### Importing Secrets

Existing secrets can be imported by ARN, name, and other attributes (including the KMS key used to encrypt the secret).
Secrets imported by name should use the short-form of the name (without the SecretsManager-provided suffx);
the secret name must exist in the same account and region as the stack.
Importing by name makes it easier to reference secrets created in different regions, each with their own suffix and ARN.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_kms as kms

secret_complete_arn = "arn:aws:secretsmanager:eu-west-1:111111111111:secret:MySecret-f3gDy9"
secret_partial_arn = "arn:aws:secretsmanager:eu-west-1:111111111111:secret:MySecret"# No Secrets Manager suffix
encryption_key = kms.Key.from_key_arn(stack, "MyEncKey", "arn:aws:kms:eu-west-1:111111111111:key/21c4b39b-fde2-4273-9ac0-d9bb5c0d0030")
my_secret_from_complete_arn = secretsmanager.Secret.from_secret_complete_arn(stack, "SecretFromCompleteArn", secret_complete_arn)
my_secret_from_partial_arn = secretsmanager.Secret.from_secret_partial_arn(stack, "SecretFromPartialArn", secret_partial_arn)
my_secret_from_name = secretsmanager.Secret.from_secret_name_v2(stack, "SecretFromName", "MySecret")
my_secret_from_attrs = secretsmanager.Secret.from_secret_attributes(stack, "SecretFromAttributes",
    secret_complete_arn=secret_complete_arn,
    encryption_key=encryption_key
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
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.AttachedSecretOptions",
    jsii_struct_bases=[],
    name_mapping={"target": "target"},
)
class AttachedSecretOptions:
    def __init__(self, *, target: "ISecretAttachmentTarget") -> None:
        """(deprecated) Options to add a secret attachment to a secret.

        :param target: (deprecated) The target to attach the secret to.

        :deprecated: use ``secret.attach()`` instead

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target": target,
        }

    @builtins.property
    def target(self) -> "ISecretAttachmentTarget":
        """(deprecated) The target to attach the secret to.

        :stability: deprecated
        """
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttachedSecretOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-secretsmanager.AttachmentTargetType")
class AttachmentTargetType(enum.Enum):
    """The type of service or database that's being associated with the secret."""

    INSTANCE = "INSTANCE"
    """(deprecated) A database instance.

    :deprecated: use RDS_DB_INSTANCE instead

    :stability: deprecated
    """
    CLUSTER = "CLUSTER"
    """(deprecated) A database cluster.

    :deprecated: use RDS_DB_CLUSTER instead

    :stability: deprecated
    """
    RDS_DB_PROXY = "RDS_DB_PROXY"
    """AWS::RDS::DBProxy."""
    REDSHIFT_CLUSTER = "REDSHIFT_CLUSTER"
    """AWS::Redshift::Cluster."""
    DOCDB_DB_INSTANCE = "DOCDB_DB_INSTANCE"
    """AWS::DocDB::DBInstance."""
    DOCDB_DB_CLUSTER = "DOCDB_DB_CLUSTER"
    """AWS::DocDB::DBCluster."""


@jsii.implements(aws_cdk.core.IInspectable)
class CfnResourcePolicy(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicy",
):
    """A CloudFormation ``AWS::SecretsManager::ResourcePolicy``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
    :cloudformationResource: AWS::SecretsManager::ResourcePolicy
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        resource_policy: typing.Any,
        secret_id: builtins.str,
        block_public_policy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Create a new ``AWS::SecretsManager::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_policy: ``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.
        :param secret_id: ``AWS::SecretsManager::ResourcePolicy.SecretId``.
        :param block_public_policy: ``AWS::SecretsManager::ResourcePolicy.BlockPublicPolicy``.
        """
        props = CfnResourcePolicyProps(
            resource_policy=resource_policy,
            secret_id=secret_id,
            block_public_policy=block_public_policy,
        )

        jsii.create(CfnResourcePolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="resourcePolicy")
    def resource_policy(self) -> typing.Any:
        """``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        """
        return jsii.get(self, "resourcePolicy")

    @resource_policy.setter # type: ignore
    def resource_policy(self, value: typing.Any) -> None:
        jsii.set(self, "resourcePolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        """``AWS::SecretsManager::ResourcePolicy.SecretId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter # type: ignore
    def secret_id(self, value: builtins.str) -> None:
        jsii.set(self, "secretId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="blockPublicPolicy")
    def block_public_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::SecretsManager::ResourcePolicy.BlockPublicPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-blockpublicpolicy
        """
        return jsii.get(self, "blockPublicPolicy")

    @block_public_policy.setter # type: ignore
    def block_public_policy(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "blockPublicPolicy", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_policy": "resourcePolicy",
        "secret_id": "secretId",
        "block_public_policy": "blockPublicPolicy",
    },
)
class CfnResourcePolicyProps:
    def __init__(
        self,
        *,
        resource_policy: typing.Any,
        secret_id: builtins.str,
        block_public_policy: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SecretsManager::ResourcePolicy``.

        :param resource_policy: ``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.
        :param secret_id: ``AWS::SecretsManager::ResourcePolicy.SecretId``.
        :param block_public_policy: ``AWS::SecretsManager::ResourcePolicy.BlockPublicPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "resource_policy": resource_policy,
            "secret_id": secret_id,
        }
        if block_public_policy is not None:
            self._values["block_public_policy"] = block_public_policy

    @builtins.property
    def resource_policy(self) -> typing.Any:
        """``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        """
        result = self._values.get("resource_policy")
        assert result is not None, "Required property 'resource_policy' is missing"
        return result

    @builtins.property
    def secret_id(self) -> builtins.str:
        """``AWS::SecretsManager::ResourcePolicy.SecretId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        """
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return result

    @builtins.property
    def block_public_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::SecretsManager::ResourcePolicy.BlockPublicPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-blockpublicpolicy
        """
        result = self._values.get("block_public_policy")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRotationSchedule(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule",
):
    """A CloudFormation ``AWS::SecretsManager::RotationSchedule``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
    :cloudformationResource: AWS::SecretsManager::RotationSchedule
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        secret_id: builtins.str,
        hosted_rotation_lambda: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRotationSchedule.HostedRotationLambdaProperty"]] = None,
        rotation_lambda_arn: typing.Optional[builtins.str] = None,
        rotation_rules: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRotationSchedule.RotationRulesProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::SecretsManager::RotationSchedule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param secret_id: ``AWS::SecretsManager::RotationSchedule.SecretId``.
        :param hosted_rotation_lambda: ``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.
        :param rotation_lambda_arn: ``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.
        :param rotation_rules: ``AWS::SecretsManager::RotationSchedule.RotationRules``.
        """
        props = CfnRotationScheduleProps(
            secret_id=secret_id,
            hosted_rotation_lambda=hosted_rotation_lambda,
            rotation_lambda_arn=rotation_lambda_arn,
            rotation_rules=rotation_rules,
        )

        jsii.create(CfnRotationSchedule, self, [scope, id, props])

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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        """``AWS::SecretsManager::RotationSchedule.SecretId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter # type: ignore
    def secret_id(self, value: builtins.str) -> None:
        jsii.set(self, "secretId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hostedRotationLambda")
    def hosted_rotation_lambda(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRotationSchedule.HostedRotationLambdaProperty"]]:
        """``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda
        """
        return jsii.get(self, "hostedRotationLambda")

    @hosted_rotation_lambda.setter # type: ignore
    def hosted_rotation_lambda(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRotationSchedule.HostedRotationLambdaProperty"]],
    ) -> None:
        jsii.set(self, "hostedRotationLambda", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rotationLambdaArn")
    def rotation_lambda_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        """
        return jsii.get(self, "rotationLambdaArn")

    @rotation_lambda_arn.setter # type: ignore
    def rotation_lambda_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "rotationLambdaArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rotationRules")
    def rotation_rules(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRotationSchedule.RotationRulesProperty"]]:
        """``AWS::SecretsManager::RotationSchedule.RotationRules``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        """
        return jsii.get(self, "rotationRules")

    @rotation_rules.setter # type: ignore
    def rotation_rules(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRotationSchedule.RotationRulesProperty"]],
    ) -> None:
        jsii.set(self, "rotationRules", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule.HostedRotationLambdaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rotation_type": "rotationType",
            "kms_key_arn": "kmsKeyArn",
            "master_secret_arn": "masterSecretArn",
            "master_secret_kms_key_arn": "masterSecretKmsKeyArn",
            "rotation_lambda_name": "rotationLambdaName",
            "vpc_security_group_ids": "vpcSecurityGroupIds",
            "vpc_subnet_ids": "vpcSubnetIds",
        },
    )
    class HostedRotationLambdaProperty:
        def __init__(
            self,
            *,
            rotation_type: builtins.str,
            kms_key_arn: typing.Optional[builtins.str] = None,
            master_secret_arn: typing.Optional[builtins.str] = None,
            master_secret_kms_key_arn: typing.Optional[builtins.str] = None,
            rotation_lambda_name: typing.Optional[builtins.str] = None,
            vpc_security_group_ids: typing.Optional[builtins.str] = None,
            vpc_subnet_ids: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param rotation_type: ``CfnRotationSchedule.HostedRotationLambdaProperty.RotationType``.
            :param kms_key_arn: ``CfnRotationSchedule.HostedRotationLambdaProperty.KmsKeyArn``.
            :param master_secret_arn: ``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretArn``.
            :param master_secret_kms_key_arn: ``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretKmsKeyArn``.
            :param rotation_lambda_name: ``CfnRotationSchedule.HostedRotationLambdaProperty.RotationLambdaName``.
            :param vpc_security_group_ids: ``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSecurityGroupIds``.
            :param vpc_subnet_ids: ``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "rotation_type": rotation_type,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if master_secret_arn is not None:
                self._values["master_secret_arn"] = master_secret_arn
            if master_secret_kms_key_arn is not None:
                self._values["master_secret_kms_key_arn"] = master_secret_kms_key_arn
            if rotation_lambda_name is not None:
                self._values["rotation_lambda_name"] = rotation_lambda_name
            if vpc_security_group_ids is not None:
                self._values["vpc_security_group_ids"] = vpc_security_group_ids
            if vpc_subnet_ids is not None:
                self._values["vpc_subnet_ids"] = vpc_subnet_ids

        @builtins.property
        def rotation_type(self) -> builtins.str:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.RotationType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationtype
            """
            result = self._values.get("rotation_type")
            assert result is not None, "Required property 'rotation_type' is missing"
            return result

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.KmsKeyArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-kmskeyarn
            """
            result = self._values.get("kms_key_arn")
            return result

        @builtins.property
        def master_secret_arn(self) -> typing.Optional[builtins.str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretarn
            """
            result = self._values.get("master_secret_arn")
            return result

        @builtins.property
        def master_secret_kms_key_arn(self) -> typing.Optional[builtins.str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.MasterSecretKmsKeyArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretkmskeyarn
            """
            result = self._values.get("master_secret_kms_key_arn")
            return result

        @builtins.property
        def rotation_lambda_name(self) -> typing.Optional[builtins.str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.RotationLambdaName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationlambdaname
            """
            result = self._values.get("rotation_lambda_name")
            return result

        @builtins.property
        def vpc_security_group_ids(self) -> typing.Optional[builtins.str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSecurityGroupIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsecuritygroupids
            """
            result = self._values.get("vpc_security_group_ids")
            return result

        @builtins.property
        def vpc_subnet_ids(self) -> typing.Optional[builtins.str]:
            """``CfnRotationSchedule.HostedRotationLambdaProperty.VpcSubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsubnetids
            """
            result = self._values.get("vpc_subnet_ids")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostedRotationLambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule.RotationRulesProperty",
        jsii_struct_bases=[],
        name_mapping={"automatically_after_days": "automaticallyAfterDays"},
    )
    class RotationRulesProperty:
        def __init__(
            self,
            *,
            automatically_after_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param automatically_after_days: ``CfnRotationSchedule.RotationRulesProperty.AutomaticallyAfterDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if automatically_after_days is not None:
                self._values["automatically_after_days"] = automatically_after_days

        @builtins.property
        def automatically_after_days(self) -> typing.Optional[jsii.Number]:
            """``CfnRotationSchedule.RotationRulesProperty.AutomaticallyAfterDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-automaticallyafterdays
            """
            result = self._values.get("automatically_after_days")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RotationRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "hosted_rotation_lambda": "hostedRotationLambda",
        "rotation_lambda_arn": "rotationLambdaArn",
        "rotation_rules": "rotationRules",
    },
)
class CfnRotationScheduleProps:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        hosted_rotation_lambda: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRotationSchedule.HostedRotationLambdaProperty]] = None,
        rotation_lambda_arn: typing.Optional[builtins.str] = None,
        rotation_rules: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRotationSchedule.RotationRulesProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SecretsManager::RotationSchedule``.

        :param secret_id: ``AWS::SecretsManager::RotationSchedule.SecretId``.
        :param hosted_rotation_lambda: ``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.
        :param rotation_lambda_arn: ``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.
        :param rotation_rules: ``AWS::SecretsManager::RotationSchedule.RotationRules``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "secret_id": secret_id,
        }
        if hosted_rotation_lambda is not None:
            self._values["hosted_rotation_lambda"] = hosted_rotation_lambda
        if rotation_lambda_arn is not None:
            self._values["rotation_lambda_arn"] = rotation_lambda_arn
        if rotation_rules is not None:
            self._values["rotation_rules"] = rotation_rules

    @builtins.property
    def secret_id(self) -> builtins.str:
        """``AWS::SecretsManager::RotationSchedule.SecretId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        """
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return result

    @builtins.property
    def hosted_rotation_lambda(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRotationSchedule.HostedRotationLambdaProperty]]:
        """``AWS::SecretsManager::RotationSchedule.HostedRotationLambda``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda
        """
        result = self._values.get("hosted_rotation_lambda")
        return result

    @builtins.property
    def rotation_lambda_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        """
        result = self._values.get("rotation_lambda_arn")
        return result

    @builtins.property
    def rotation_rules(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRotationSchedule.RotationRulesProperty]]:
        """``AWS::SecretsManager::RotationSchedule.RotationRules``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        """
        result = self._values.get("rotation_rules")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRotationScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSecret(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret",
):
    """A CloudFormation ``AWS::SecretsManager::Secret``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
    :cloudformationResource: AWS::SecretsManager::Secret
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        generate_secret_string: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnSecret.GenerateSecretStringProperty"]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        secret_string: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::SecretsManager::Secret``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::SecretsManager::Secret.Description``.
        :param generate_secret_string: ``AWS::SecretsManager::Secret.GenerateSecretString``.
        :param kms_key_id: ``AWS::SecretsManager::Secret.KmsKeyId``.
        :param name: ``AWS::SecretsManager::Secret.Name``.
        :param secret_string: ``AWS::SecretsManager::Secret.SecretString``.
        :param tags: ``AWS::SecretsManager::Secret.Tags``.
        """
        props = CfnSecretProps(
            description=description,
            generate_secret_string=generate_secret_string,
            kms_key_id=kms_key_id,
            name=name,
            secret_string=secret_string,
            tags=tags,
        )

        jsii.create(CfnSecret, self, [scope, id, props])

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
        """``AWS::SecretsManager::Secret.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="generateSecretString")
    def generate_secret_string(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnSecret.GenerateSecretStringProperty"]]:
        """``AWS::SecretsManager::Secret.GenerateSecretString``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        """
        return jsii.get(self, "generateSecretString")

    @generate_secret_string.setter # type: ignore
    def generate_secret_string(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnSecret.GenerateSecretStringProperty"]],
    ) -> None:
        jsii.set(self, "generateSecretString", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter # type: ignore
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretString")
    def secret_string(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.SecretString``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        """
        return jsii.get(self, "secretString")

    @secret_string.setter # type: ignore
    def secret_string(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "secretString", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret.GenerateSecretStringProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_characters": "excludeCharacters",
            "exclude_lowercase": "excludeLowercase",
            "exclude_numbers": "excludeNumbers",
            "exclude_punctuation": "excludePunctuation",
            "exclude_uppercase": "excludeUppercase",
            "generate_string_key": "generateStringKey",
            "include_space": "includeSpace",
            "password_length": "passwordLength",
            "require_each_included_type": "requireEachIncludedType",
            "secret_string_template": "secretStringTemplate",
        },
    )
    class GenerateSecretStringProperty:
        def __init__(
            self,
            *,
            exclude_characters: typing.Optional[builtins.str] = None,
            exclude_lowercase: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            exclude_numbers: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            exclude_punctuation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            exclude_uppercase: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            generate_string_key: typing.Optional[builtins.str] = None,
            include_space: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            password_length: typing.Optional[jsii.Number] = None,
            require_each_included_type: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            secret_string_template: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param exclude_characters: ``CfnSecret.GenerateSecretStringProperty.ExcludeCharacters``.
            :param exclude_lowercase: ``CfnSecret.GenerateSecretStringProperty.ExcludeLowercase``.
            :param exclude_numbers: ``CfnSecret.GenerateSecretStringProperty.ExcludeNumbers``.
            :param exclude_punctuation: ``CfnSecret.GenerateSecretStringProperty.ExcludePunctuation``.
            :param exclude_uppercase: ``CfnSecret.GenerateSecretStringProperty.ExcludeUppercase``.
            :param generate_string_key: ``CfnSecret.GenerateSecretStringProperty.GenerateStringKey``.
            :param include_space: ``CfnSecret.GenerateSecretStringProperty.IncludeSpace``.
            :param password_length: ``CfnSecret.GenerateSecretStringProperty.PasswordLength``.
            :param require_each_included_type: ``CfnSecret.GenerateSecretStringProperty.RequireEachIncludedType``.
            :param secret_string_template: ``CfnSecret.GenerateSecretStringProperty.SecretStringTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if exclude_characters is not None:
                self._values["exclude_characters"] = exclude_characters
            if exclude_lowercase is not None:
                self._values["exclude_lowercase"] = exclude_lowercase
            if exclude_numbers is not None:
                self._values["exclude_numbers"] = exclude_numbers
            if exclude_punctuation is not None:
                self._values["exclude_punctuation"] = exclude_punctuation
            if exclude_uppercase is not None:
                self._values["exclude_uppercase"] = exclude_uppercase
            if generate_string_key is not None:
                self._values["generate_string_key"] = generate_string_key
            if include_space is not None:
                self._values["include_space"] = include_space
            if password_length is not None:
                self._values["password_length"] = password_length
            if require_each_included_type is not None:
                self._values["require_each_included_type"] = require_each_included_type
            if secret_string_template is not None:
                self._values["secret_string_template"] = secret_string_template

        @builtins.property
        def exclude_characters(self) -> typing.Optional[builtins.str]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeCharacters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludecharacters
            """
            result = self._values.get("exclude_characters")
            return result

        @builtins.property
        def exclude_lowercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeLowercase``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludelowercase
            """
            result = self._values.get("exclude_lowercase")
            return result

        @builtins.property
        def exclude_numbers(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeNumbers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludenumbers
            """
            result = self._values.get("exclude_numbers")
            return result

        @builtins.property
        def exclude_punctuation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludePunctuation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludepunctuation
            """
            result = self._values.get("exclude_punctuation")
            return result

        @builtins.property
        def exclude_uppercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeUppercase``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludeuppercase
            """
            result = self._values.get("exclude_uppercase")
            return result

        @builtins.property
        def generate_string_key(self) -> typing.Optional[builtins.str]:
            """``CfnSecret.GenerateSecretStringProperty.GenerateStringKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-generatestringkey
            """
            result = self._values.get("generate_string_key")
            return result

        @builtins.property
        def include_space(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnSecret.GenerateSecretStringProperty.IncludeSpace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-includespace
            """
            result = self._values.get("include_space")
            return result

        @builtins.property
        def password_length(self) -> typing.Optional[jsii.Number]:
            """``CfnSecret.GenerateSecretStringProperty.PasswordLength``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-passwordlength
            """
            result = self._values.get("password_length")
            return result

        @builtins.property
        def require_each_included_type(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnSecret.GenerateSecretStringProperty.RequireEachIncludedType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-requireeachincludedtype
            """
            result = self._values.get("require_each_included_type")
            return result

        @builtins.property
        def secret_string_template(self) -> typing.Optional[builtins.str]:
            """``CfnSecret.GenerateSecretStringProperty.SecretStringTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-secretstringtemplate
            """
            result = self._values.get("secret_string_template")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GenerateSecretStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "generate_secret_string": "generateSecretString",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "secret_string": "secretString",
        "tags": "tags",
    },
)
class CfnSecretProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        generate_secret_string: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnSecret.GenerateSecretStringProperty]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        secret_string: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SecretsManager::Secret``.

        :param description: ``AWS::SecretsManager::Secret.Description``.
        :param generate_secret_string: ``AWS::SecretsManager::Secret.GenerateSecretString``.
        :param kms_key_id: ``AWS::SecretsManager::Secret.KmsKeyId``.
        :param name: ``AWS::SecretsManager::Secret.Name``.
        :param secret_string: ``AWS::SecretsManager::Secret.SecretString``.
        :param tags: ``AWS::SecretsManager::Secret.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if secret_string is not None:
            self._values["secret_string"] = secret_string
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def generate_secret_string(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnSecret.GenerateSecretStringProperty]]:
        """``AWS::SecretsManager::Secret.GenerateSecretString``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        """
        result = self._values.get("generate_secret_string")
        return result

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        """
        result = self._values.get("kms_key_id")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def secret_string(self) -> typing.Optional[builtins.str]:
        """``AWS::SecretsManager::Secret.SecretString``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        """
        result = self._values.get("secret_string")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SecretsManager::Secret.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSecretTargetAttachment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachment",
):
    """A CloudFormation ``AWS::SecretsManager::SecretTargetAttachment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    :cloudformationResource: AWS::SecretsManager::SecretTargetAttachment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        secret_id: builtins.str,
        target_id: builtins.str,
        target_type: builtins.str,
    ) -> None:
        """Create a new ``AWS::SecretsManager::SecretTargetAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param secret_id: ``AWS::SecretsManager::SecretTargetAttachment.SecretId``.
        :param target_id: ``AWS::SecretsManager::SecretTargetAttachment.TargetId``.
        :param target_type: ``AWS::SecretsManager::SecretTargetAttachment.TargetType``.
        """
        props = CfnSecretTargetAttachmentProps(
            secret_id=secret_id, target_id=target_id, target_type=target_type
        )

        jsii.create(CfnSecretTargetAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        """``AWS::SecretsManager::SecretTargetAttachment.SecretId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter # type: ignore
    def secret_id(self, value: builtins.str) -> None:
        jsii.set(self, "secretId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        """
        return jsii.get(self, "targetId")

    @target_id.setter # type: ignore
    def target_id(self, value: builtins.str) -> None:
        jsii.set(self, "targetId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> builtins.str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        """
        return jsii.get(self, "targetType")

    @target_type.setter # type: ignore
    def target_type(self, value: builtins.str) -> None:
        jsii.set(self, "targetType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "target_id": "targetId",
        "target_type": "targetType",
    },
)
class CfnSecretTargetAttachmentProps:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        target_id: builtins.str,
        target_type: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::SecretsManager::SecretTargetAttachment``.

        :param secret_id: ``AWS::SecretsManager::SecretTargetAttachment.SecretId``.
        :param target_id: ``AWS::SecretsManager::SecretTargetAttachment.TargetId``.
        :param target_type: ``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "secret_id": secret_id,
            "target_id": target_id,
            "target_type": target_type,
        }

    @builtins.property
    def secret_id(self) -> builtins.str:
        """``AWS::SecretsManager::SecretTargetAttachment.SecretId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        """
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return result

    @builtins.property
    def target_id(self) -> builtins.str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        """
        result = self._values.get("target_id")
        assert result is not None, "Required property 'target_id' is missing"
        return result

    @builtins.property
    def target_type(self) -> builtins.str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        """
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretTargetAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class HostedRotation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.HostedRotation",
):
    """A hosted rotation."""

    @jsii.member(jsii_name="mariaDbMultiUser")
    @builtins.classmethod
    def maria_db_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """MariaDB Multi User.

        :param master_secret: The master secret for a multi user rotation scheme.
        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "mariaDbMultiUser", [options])

    @jsii.member(jsii_name="mariaDbSingleUser")
    @builtins.classmethod
    def maria_db_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """MariaDB Single User.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "mariaDbSingleUser", [options])

    @jsii.member(jsii_name="mongoDbMultiUser")
    @builtins.classmethod
    def mongo_db_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """MongoDB Multi User.

        :param master_secret: The master secret for a multi user rotation scheme.
        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "mongoDbMultiUser", [options])

    @jsii.member(jsii_name="mongoDbSingleUser")
    @builtins.classmethod
    def mongo_db_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """MongoDB Single User.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "mongoDbSingleUser", [options])

    @jsii.member(jsii_name="mysqlMultiUser")
    @builtins.classmethod
    def mysql_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """MySQL Multi User.

        :param master_secret: The master secret for a multi user rotation scheme.
        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "mysqlMultiUser", [options])

    @jsii.member(jsii_name="mysqlSingleUser")
    @builtins.classmethod
    def mysql_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """MySQL Single User.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "mysqlSingleUser", [options])

    @jsii.member(jsii_name="oracleMultiUser")
    @builtins.classmethod
    def oracle_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """Oracle Multi User.

        :param master_secret: The master secret for a multi user rotation scheme.
        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "oracleMultiUser", [options])

    @jsii.member(jsii_name="oracleSingleUser")
    @builtins.classmethod
    def oracle_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """Oracle Single User.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "oracleSingleUser", [options])

    @jsii.member(jsii_name="postgreSqlMultiUser")
    @builtins.classmethod
    def postgre_sql_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """PostgreSQL Multi User.

        :param master_secret: The master secret for a multi user rotation scheme.
        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "postgreSqlMultiUser", [options])

    @jsii.member(jsii_name="postgreSqlSingleUser")
    @builtins.classmethod
    def postgre_sql_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """PostgreSQL Single User.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "postgreSqlSingleUser", [options])

    @jsii.member(jsii_name="redshiftMultiUser")
    @builtins.classmethod
    def redshift_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """Redshift Multi User.

        :param master_secret: The master secret for a multi user rotation scheme.
        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "redshiftMultiUser", [options])

    @jsii.member(jsii_name="redshiftSingleUser")
    @builtins.classmethod
    def redshift_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """Redshift Single User.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "redshiftSingleUser", [options])

    @jsii.member(jsii_name="sqlServerMultiUser")
    @builtins.classmethod
    def sql_server_multi_user(
        cls,
        *,
        master_secret: "ISecret",
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """SQL Server Multi User.

        :param master_secret: The master secret for a multi user rotation scheme.
        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = MultiUserHostedRotationOptions(
            master_secret=master_secret,
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "sqlServerMultiUser", [options])

    @jsii.member(jsii_name="sqlServerSingleUser")
    @builtins.classmethod
    def sql_server_single_user(
        cls,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "HostedRotation":
        """SQL Server Single User.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        options = SingleUserHostedRotationOptions(
            function_name=function_name,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.sinvoke(cls, "sqlServerSingleUser", [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        secret: "ISecret",
        scope: constructs.Construct,
    ) -> CfnRotationSchedule.HostedRotationLambdaProperty:
        """Binds this hosted rotation to a secret.

        :param secret: -
        :param scope: -
        """
        return jsii.invoke(self, "bind", [secret, scope])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Security group connections for this hosted rotation."""
        return jsii.get(self, "connections")


class HostedRotationType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.HostedRotationType",
):
    """Hosted rotation type."""

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MARIADB_MULTI_USER")
    def MARIADB_MULTI_USER(cls) -> "HostedRotationType":
        """MariaDB Multi User."""
        return jsii.sget(cls, "MARIADB_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MARIADB_SINGLE_USER")
    def MARIADB_SINGLE_USER(cls) -> "HostedRotationType":
        """MariaDB Single User."""
        return jsii.sget(cls, "MARIADB_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MONGODB_MULTI_USER")
    def MONGODB_MULTI_USER(cls) -> "HostedRotationType":
        """MongoDB Multi User."""
        return jsii.sget(cls, "MONGODB_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MONGODB_SINGLE_USER")
    def MONGODB_SINGLE_USER(cls) -> "HostedRotationType":
        """MongoDB Single User."""
        return jsii.sget(cls, "MONGODB_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MYSQL_MULTI_USER")
    def MYSQL_MULTI_USER(cls) -> "HostedRotationType":
        """MySQL Multi User."""
        return jsii.sget(cls, "MYSQL_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MYSQL_SINGLE_USER")
    def MYSQL_SINGLE_USER(cls) -> "HostedRotationType":
        """MySQL Single User."""
        return jsii.sget(cls, "MYSQL_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ORACLE_MULTI_USER")
    def ORACLE_MULTI_USER(cls) -> "HostedRotationType":
        """Oracle Multi User."""
        return jsii.sget(cls, "ORACLE_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ORACLE_SINGLE_USER")
    def ORACLE_SINGLE_USER(cls) -> "HostedRotationType":
        """Oracle Single User."""
        return jsii.sget(cls, "ORACLE_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="POSTGRESQL_MULTI_USER")
    def POSTGRESQL_MULTI_USER(cls) -> "HostedRotationType":
        """PostgreSQL Multi User."""
        return jsii.sget(cls, "POSTGRESQL_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="POSTGRESQL_SINGLE_USER")
    def POSTGRESQL_SINGLE_USER(cls) -> "HostedRotationType":
        """PostgreSQL Single User."""
        return jsii.sget(cls, "POSTGRESQL_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="REDSHIFT_MULTI_USER")
    def REDSHIFT_MULTI_USER(cls) -> "HostedRotationType":
        """Redshift Multi User."""
        return jsii.sget(cls, "REDSHIFT_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="REDSHIFT_SINGLE_USER")
    def REDSHIFT_SINGLE_USER(cls) -> "HostedRotationType":
        """Redshift Single User."""
        return jsii.sget(cls, "REDSHIFT_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="SQLSERVER_MULTI_USER")
    def SQLSERVER_MULTI_USER(cls) -> "HostedRotationType":
        """SQL Server Multi User."""
        return jsii.sget(cls, "SQLSERVER_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="SQLSERVER_SINGLE_USER")
    def SQLSERVER_SINGLE_USER(cls) -> "HostedRotationType":
        """SQL Server Single User."""
        return jsii.sget(cls, "SQLSERVER_SINGLE_USER")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """The type of rotation."""
        return jsii.get(self, "name")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="isMultiUser")
    def is_multi_user(self) -> typing.Optional[builtins.bool]:
        """Whether the rotation uses the mutli user scheme."""
        return jsii.get(self, "isMultiUser")


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecret")
class ISecret(aws_cdk.core.IResource, typing_extensions.Protocol):
    """A secret in AWS Secrets Manager."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISecretProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        """The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        """The name of the secret."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        """The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).
        """
        ...

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
    ) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -
        """
        ...

    @jsii.member(jsii_name="attach")
    def attach(self, target: "ISecretAttachmentTarget") -> "ISecret":
        """Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret
        """
        ...

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account."""
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        version_stages: typing.Optional[typing.List[builtins.str]] = None,
    ) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants writing and updating the secret value to some role.

        :param grantee: the principal being granted permission.
        """
        ...

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: builtins.str) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -
        """
        ...


class _ISecretProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """A secret in AWS Secrets Manager."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-secretsmanager.ISecret"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        """The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.

        :attribute: true
        """
        return jsii.get(self, "secretArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        """The name of the secret."""
        return jsii.get(self, "secretName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        :attribute: true
        """
        return jsii.get(self, "secretValue")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        """The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).
        """
        return jsii.get(self, "secretFullArn")

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
    ) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        options = RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="attach")
    def attach(self, target: "ISecretAttachmentTarget") -> ISecret:
        """Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret
        """
        return jsii.invoke(self, "attach", [target])

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account."""
        return jsii.invoke(self, "denyAccountRootDelete", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        version_stages: typing.Optional[typing.List[builtins.str]] = None,
    ) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants writing and updating the secret value to some role.

        :param grantee: the principal being granted permission.
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: builtins.str) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -
        """
        return jsii.invoke(self, "secretValueFromJson", [key])


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget")
class ISecretAttachmentTarget(typing_extensions.Protocol):
    """A secret attachment target."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISecretAttachmentTargetProxy

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications."""
        ...


class _ISecretAttachmentTargetProxy:
    """A secret attachment target."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget"

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications."""
        return jsii.invoke(self, "asSecretAttachmentTarget", [])


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecretTargetAttachment")
class ISecretTargetAttachment(ISecret, typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISecretTargetAttachmentProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> builtins.str:
        """Same as ``secretArn``.

        :attribute: true
        """
        ...


class _ISecretTargetAttachmentProxy(
    jsii.proxy_for(ISecret) # type: ignore
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-secretsmanager.ISecretTargetAttachment"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> builtins.str:
        """Same as ``secretArn``.

        :attribute: true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")


class ResourcePolicy(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.ResourcePolicy",
):
    """Secret Resource Policy."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        secret: ISecret,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param secret: The secret to attach a resource-based permissions policy.
        """
        props = ResourcePolicyProps(secret=secret)

        jsii.create(ResourcePolicy, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        """The IAM policy document for this policy."""
        return jsii.get(self, "document")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.ResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class ResourcePolicyProps:
    def __init__(self, *, secret: ISecret) -> None:
        """Construction properties for a ResourcePolicy.

        :param secret: The secret to attach a resource-based permissions policy.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> ISecret:
        """The secret to attach a resource-based permissions policy."""
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RotationSchedule(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.RotationSchedule",
):
    """A rotation schedule."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        secret: ISecret,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param secret: The secret to rotate. If hosted rotation is used, this must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        props = RotationScheduleProps(
            secret=secret,
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        jsii.create(RotationSchedule, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "automatically_after": "automaticallyAfter",
        "hosted_rotation": "hostedRotation",
        "rotation_lambda": "rotationLambda",
    },
)
class RotationScheduleOptions:
    def __init__(
        self,
        *,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
    ) -> None:
        """Options to add a rotation schedule to a secret.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after
        if hosted_rotation is not None:
            self._values["hosted_rotation"] = hosted_rotation
        if rotation_lambda is not None:
            self._values["rotation_lambda"] = rotation_lambda

    @builtins.property
    def automatically_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :default: Duration.days(30)
        """
        result = self._values.get("automatically_after")
        return result

    @builtins.property
    def hosted_rotation(self) -> typing.Optional[HostedRotation]:
        """Hosted rotation.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        result = self._values.get("hosted_rotation")
        return result

    @builtins.property
    def rotation_lambda(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A Lambda function that can rotate the secret.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        result = self._values.get("rotation_lambda")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleProps",
    jsii_struct_bases=[RotationScheduleOptions],
    name_mapping={
        "automatically_after": "automaticallyAfter",
        "hosted_rotation": "hostedRotation",
        "rotation_lambda": "rotationLambda",
        "secret": "secret",
    },
)
class RotationScheduleProps(RotationScheduleOptions):
    def __init__(
        self,
        *,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        secret: ISecret,
    ) -> None:
        """Construction properties for a RotationSchedule.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param secret: The secret to rotate. If hosted rotation is used, this must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "secret": secret,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after
        if hosted_rotation is not None:
            self._values["hosted_rotation"] = hosted_rotation
        if rotation_lambda is not None:
            self._values["rotation_lambda"] = rotation_lambda

    @builtins.property
    def automatically_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :default: Duration.days(30)
        """
        result = self._values.get("automatically_after")
        return result

    @builtins.property
    def hosted_rotation(self) -> typing.Optional[HostedRotation]:
        """Hosted rotation.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        result = self._values.get("hosted_rotation")
        return result

    @builtins.property
    def rotation_lambda(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A Lambda function that can rotate the secret.

        :default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        result = self._values.get("rotation_lambda")
        return result

    @builtins.property
    def secret(self) -> ISecret:
        """The secret to rotate.

        If hosted rotation is used, this must be a JSON string with the following format::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords>
           }

        This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment``
        or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        """
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecret)
class Secret(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.Secret",
):
    """Creates a new secret in AWS SecretsManager."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        generate_secret_string: typing.Optional["SecretStringGenerator"] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        """
        props = SecretProps(
            description=description,
            encryption_key=encryption_key,
            generate_secret_string=generate_secret_string,
            removal_policy=removal_policy,
            secret_name=secret_name,
        )

        jsii.create(Secret, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretArn")
    @builtins.classmethod
    def from_secret_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        secret_arn: builtins.str,
    ) -> ISecret:
        """
        :param scope: -
        :param id: -
        :param secret_arn: -

        :deprecated: use ``fromSecretCompleteArn`` or ``fromSecretPartialArn``

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "fromSecretArn", [scope, id, secret_arn])

    @jsii.member(jsii_name="fromSecretAttributes")
    @builtins.classmethod
    def from_secret_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        secret_arn: typing.Optional[builtins.str] = None,
        secret_complete_arn: typing.Optional[builtins.str] = None,
        secret_partial_arn: typing.Optional[builtins.str] = None,
    ) -> ISecret:
        """Import an existing secret into the Stack.

        :param scope: the scope of the import.
        :param id: the ID of the imported Secret in the construct tree.
        :param encryption_key: The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.
        :param secret_arn: (deprecated) The ARN of the secret in SecretsManager. Cannot be used with ``secretCompleteArn`` or ``secretPartialArn``.
        :param secret_complete_arn: The complete ARN of the secret in SecretsManager. This is the ARN including the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretPartialArn``.
        :param secret_partial_arn: The partial ARN of the secret in SecretsManager. This is the ARN without the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretCompleteArn``.
        """
        attrs = SecretAttributes(
            encryption_key=encryption_key,
            secret_arn=secret_arn,
            secret_complete_arn=secret_complete_arn,
            secret_partial_arn=secret_partial_arn,
        )

        return jsii.sinvoke(cls, "fromSecretAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromSecretCompleteArn")
    @builtins.classmethod
    def from_secret_complete_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        secret_complete_arn: builtins.str,
    ) -> ISecret:
        """Imports a secret by complete ARN.

        The complete ARN is the ARN with the Secrets Manager-supplied suffix.

        :param scope: -
        :param id: -
        :param secret_complete_arn: -
        """
        return jsii.sinvoke(cls, "fromSecretCompleteArn", [scope, id, secret_complete_arn])

    @jsii.member(jsii_name="fromSecretName")
    @builtins.classmethod
    def from_secret_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        secret_name: builtins.str,
    ) -> ISecret:
        """(deprecated) Imports a secret by secret name;

        the ARN of the Secret will be set to the secret name.
        A secret with this name must exist in the same account & region.

        :param scope: -
        :param id: -
        :param secret_name: -

        :deprecated: use ``fromSecretNameV2``

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "fromSecretName", [scope, id, secret_name])

    @jsii.member(jsii_name="fromSecretNameV2")
    @builtins.classmethod
    def from_secret_name_v2(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        secret_name: builtins.str,
    ) -> ISecret:
        """Imports a secret by secret name.

        A secret with this name must exist in the same account & region.
        Replaces the deprecated ``fromSecretName``.

        :param scope: -
        :param id: -
        :param secret_name: -
        """
        return jsii.sinvoke(cls, "fromSecretNameV2", [scope, id, secret_name])

    @jsii.member(jsii_name="fromSecretPartialArn")
    @builtins.classmethod
    def from_secret_partial_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        secret_partial_arn: builtins.str,
    ) -> ISecret:
        """Imports a secret by partial ARN.

        The partial ARN is the ARN without the Secrets Manager-supplied suffix.

        :param scope: -
        :param id: -
        :param secret_partial_arn: -
        """
        return jsii.sinvoke(cls, "fromSecretPartialArn", [scope, id, secret_partial_arn])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
    ) -> RotationSchedule:
        """Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        options = RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addTargetAttachment")
    def add_target_attachment(
        self,
        id: builtins.str,
        *,
        target: ISecretAttachmentTarget,
    ) -> "SecretTargetAttachment":
        """(deprecated) Adds a target attachment to the secret.

        :param id: -
        :param target: (deprecated) The target to attach the secret to.

        :return: an AttachedSecret

        :deprecated: use ``attach()`` instead

        :stability: deprecated
        """
        options = AttachedSecretOptions(target=target)

        return jsii.invoke(self, "addTargetAttachment", [id, options])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="attach")
    def attach(self, target: ISecretAttachmentTarget) -> ISecret:
        """Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret
        """
        return jsii.invoke(self, "attach", [target])

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account."""
        return jsii.invoke(self, "denyAccountRootDelete", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        version_stages: typing.Optional[typing.List[builtins.str]] = None,
    ) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants writing and updating the secret value to some role.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(
        self,
        json_field: builtins.str,
    ) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -
        """
        return jsii.invoke(self, "secretValueFromJson", [json_field])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="arnForPolicies")
    def _arn_for_policies(self) -> builtins.str:
        """Provides an identifier for this secret for use in IAM policies.

        Typically, this is just the secret ARN.
        However, secrets imported by name require a different format.
        """
        return jsii.get(self, "arnForPolicies")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        """The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.
        """
        return jsii.get(self, "secretArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        """The name of the secret."""
        return jsii.get(self, "secretName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``."""
        return jsii.get(self, "secretValue")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        """The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).
        """
        return jsii.get(self, "secretFullArn")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SecretAttachmentTargetProps",
    jsii_struct_bases=[],
    name_mapping={"target_id": "targetId", "target_type": "targetType"},
)
class SecretAttachmentTargetProps:
    def __init__(
        self,
        *,
        target_id: builtins.str,
        target_type: AttachmentTargetType,
    ) -> None:
        """Attachment target specifications.

        :param target_id: The id of the target to attach the secret to.
        :param target_type: The type of the target to attach the secret to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_id": target_id,
            "target_type": target_type,
        }

    @builtins.property
    def target_id(self) -> builtins.str:
        """The id of the target to attach the secret to."""
        result = self._values.get("target_id")
        assert result is not None, "Required property 'target_id' is missing"
        return result

    @builtins.property
    def target_type(self) -> AttachmentTargetType:
        """The type of the target to attach the secret to."""
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretAttachmentTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SecretAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "secret_arn": "secretArn",
        "secret_complete_arn": "secretCompleteArn",
        "secret_partial_arn": "secretPartialArn",
    },
)
class SecretAttributes:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        secret_arn: typing.Optional[builtins.str] = None,
        secret_complete_arn: typing.Optional[builtins.str] = None,
        secret_partial_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Attributes required to import an existing secret into the Stack.

        One ARN format (``secretArn``, ``secretCompleteArn``, ``secretPartialArn``) must be provided.

        :param encryption_key: The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.
        :param secret_arn: (deprecated) The ARN of the secret in SecretsManager. Cannot be used with ``secretCompleteArn`` or ``secretPartialArn``.
        :param secret_complete_arn: The complete ARN of the secret in SecretsManager. This is the ARN including the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretPartialArn``.
        :param secret_partial_arn: The partial ARN of the secret in SecretsManager. This is the ARN without the Secrets Manager 6-character suffix. Cannot be used with ``secretArn`` or ``secretCompleteArn``.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if secret_arn is not None:
            self._values["secret_arn"] = secret_arn
        if secret_complete_arn is not None:
            self._values["secret_complete_arn"] = secret_complete_arn
        if secret_partial_arn is not None:
            self._values["secret_partial_arn"] = secret_partial_arn

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used."""
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def secret_arn(self) -> typing.Optional[builtins.str]:
        """(deprecated) The ARN of the secret in SecretsManager.

        Cannot be used with ``secretCompleteArn`` or ``secretPartialArn``.

        :deprecated: use ``secretCompleteArn`` or ``secretPartialArn`` instead.

        :stability: deprecated
        """
        result = self._values.get("secret_arn")
        return result

    @builtins.property
    def secret_complete_arn(self) -> typing.Optional[builtins.str]:
        """The complete ARN of the secret in SecretsManager.

        This is the ARN including the Secrets Manager 6-character suffix.
        Cannot be used with ``secretArn`` or ``secretPartialArn``.
        """
        result = self._values.get("secret_complete_arn")
        return result

    @builtins.property
    def secret_partial_arn(self) -> typing.Optional[builtins.str]:
        """The partial ARN of the secret in SecretsManager.

        This is the ARN without the Secrets Manager 6-character suffix.
        Cannot be used with ``secretArn`` or ``secretCompleteArn``.
        """
        result = self._values.get("secret_partial_arn")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "encryption_key": "encryptionKey",
        "generate_secret_string": "generateSecretString",
        "removal_policy": "removalPolicy",
        "secret_name": "secretName",
    },
)
class SecretProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        generate_secret_string: typing.Optional["SecretStringGenerator"] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """The properties required to create a new secret in AWS Secrets Manager.

        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        """
        if isinstance(generate_secret_string, dict):
            generate_secret_string = SecretStringGenerator(**generate_secret_string)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """An optional, human-friendly description of the secret.

        :default: - No description.
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def generate_secret_string(self) -> typing.Optional["SecretStringGenerator"]:
        """Configuration for how to generate a secret value.

        :default:

        - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each
        category), per the default values of ``SecretStringGenerator``.
        """
        result = self._values.get("generate_secret_string")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """Policy to apply when the secret is removed from this stack.

        :default: - Not set.
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        """A name for the secret.

        Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to
        30 days blackout period. During that period, it is not possible to create another secret that shares the same name.

        :default: - A name is generated by CloudFormation.
        """
        result = self._values.get("secret_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecretRotation(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.SecretRotation",
):
    """Secret rotation for a service or database."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application: "SecretRotationApplication",
        secret: ISecret,
        target: aws_cdk.aws_ec2.IConnectable,
        vpc: aws_cdk.aws_ec2.IVpc,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        master_secret: typing.Optional[ISecret] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param application: The serverless application for the rotation.
        :param secret: The secret to rotate. It must be a JSON string with the following format:. Example:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param target: The target service or database.
        :param vpc: The VPC where the Lambda rotation function will run.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param exclude_characters: Characters which should not appear in the generated password. Default: - no additional characters are explicitly excluded
        :param master_secret: The master secret for a multi user rotation scheme. Default: - single user rotation scheme
        :param security_group: The security group for the Lambda rotation function. Default: - a new security group is created
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        props = SecretRotationProps(
            application=application,
            secret=secret,
            target=target,
            vpc=vpc,
            automatically_after=automatically_after,
            exclude_characters=exclude_characters,
            master_secret=master_secret,
            security_group=security_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(SecretRotation, self, [scope, id, props])


class SecretRotationApplication(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.SecretRotationApplication",
):
    """A secret rotation serverless application."""

    def __init__(
        self,
        application_id: builtins.str,
        semantic_version: builtins.str,
        *,
        is_multi_user: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param application_id: -
        :param semantic_version: -
        :param is_multi_user: Whether the rotation application uses the mutli user scheme. Default: false
        """
        options = SecretRotationApplicationOptions(is_multi_user=is_multi_user)

        jsii.create(SecretRotationApplication, self, [application_id, semantic_version, options])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MARIADB_ROTATION_MULTI_USER")
    def MARIADB_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MariaDB using the multi user rotation scheme."""
        return jsii.sget(cls, "MARIADB_ROTATION_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MARIADB_ROTATION_SINGLE_USER")
    def MARIADB_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MariaDB using the single user rotation scheme."""
        return jsii.sget(cls, "MARIADB_ROTATION_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MONGODB_ROTATION_MULTI_USER")
    def MONGODB_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for MongoDB using the multi user rotation scheme."""
        return jsii.sget(cls, "MONGODB_ROTATION_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MONGODB_ROTATION_SINGLE_USER")
    def MONGODB_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for MongoDB using the single user rotation scheme."""
        return jsii.sget(cls, "MONGODB_ROTATION_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MYSQL_ROTATION_MULTI_USER")
    def MYSQL_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MySQL using the multi user rotation scheme."""
        return jsii.sget(cls, "MYSQL_ROTATION_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MYSQL_ROTATION_SINGLE_USER")
    def MYSQL_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS MySQL using the single user rotation scheme."""
        return jsii.sget(cls, "MYSQL_ROTATION_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ORACLE_ROTATION_MULTI_USER")
    def ORACLE_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS Oracle using the multi user rotation scheme."""
        return jsii.sget(cls, "ORACLE_ROTATION_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ORACLE_ROTATION_SINGLE_USER")
    def ORACLE_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS Oracle using the single user rotation scheme."""
        return jsii.sget(cls, "ORACLE_ROTATION_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="POSTGRES_ROTATION_MULTI_USER")
    def POSTGRES_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS PostgreSQL using the multi user rotation scheme."""
        return jsii.sget(cls, "POSTGRES_ROTATION_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="POSTGRES_ROTATION_SINGLE_USER")
    def POSTGRES_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS PostgreSQL using the single user rotation scheme."""
        return jsii.sget(cls, "POSTGRES_ROTATION_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="REDSHIFT_ROTATION_MULTI_USER")
    def REDSHIFT_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for Amazon Redshift using the multi user rotation scheme."""
        return jsii.sget(cls, "REDSHIFT_ROTATION_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="REDSHIFT_ROTATION_SINGLE_USER")
    def REDSHIFT_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for Amazon Redshift using the single user rotation scheme."""
        return jsii.sget(cls, "REDSHIFT_ROTATION_SINGLE_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="SQLSERVER_ROTATION_MULTI_USER")
    def SQLSERVER_ROTATION_MULTI_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS SQL Server using the multi user rotation scheme."""
        return jsii.sget(cls, "SQLSERVER_ROTATION_MULTI_USER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="SQLSERVER_ROTATION_SINGLE_USER")
    def SQLSERVER_ROTATION_SINGLE_USER(cls) -> "SecretRotationApplication":
        """Conducts an AWS SecretsManager secret rotation for RDS SQL Server using the single user rotation scheme."""
        return jsii.sget(cls, "SQLSERVER_ROTATION_SINGLE_USER")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """The application identifier of the rotation application."""
        return jsii.get(self, "applicationId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="semanticVersion")
    def semantic_version(self) -> builtins.str:
        """The semantic version of the rotation application."""
        return jsii.get(self, "semanticVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="isMultiUser")
    def is_multi_user(self) -> typing.Optional[builtins.bool]:
        """Whether the rotation application uses the mutli user scheme."""
        return jsii.get(self, "isMultiUser")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SecretRotationApplicationOptions",
    jsii_struct_bases=[],
    name_mapping={"is_multi_user": "isMultiUser"},
)
class SecretRotationApplicationOptions:
    def __init__(self, *, is_multi_user: typing.Optional[builtins.bool] = None) -> None:
        """Options for a SecretRotationApplication.

        :param is_multi_user: Whether the rotation application uses the mutli user scheme. Default: false
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if is_multi_user is not None:
            self._values["is_multi_user"] = is_multi_user

    @builtins.property
    def is_multi_user(self) -> typing.Optional[builtins.bool]:
        """Whether the rotation application uses the mutli user scheme.

        :default: false
        """
        result = self._values.get("is_multi_user")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretRotationApplicationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SecretRotationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "secret": "secret",
        "target": "target",
        "vpc": "vpc",
        "automatically_after": "automaticallyAfter",
        "exclude_characters": "excludeCharacters",
        "master_secret": "masterSecret",
        "security_group": "securityGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class SecretRotationProps:
    def __init__(
        self,
        *,
        application: SecretRotationApplication,
        secret: ISecret,
        target: aws_cdk.aws_ec2.IConnectable,
        vpc: aws_cdk.aws_ec2.IVpc,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        master_secret: typing.Optional[ISecret] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Construction properties for a SecretRotation.

        :param application: The serverless application for the rotation.
        :param secret: The secret to rotate. It must be a JSON string with the following format:. Example:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords> } This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment`` or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.
        :param target: The target service or database.
        :param vpc: The VPC where the Lambda rotation function will run.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param exclude_characters: Characters which should not appear in the generated password. Default: - no additional characters are explicitly excluded
        :param master_secret: The master secret for a multi user rotation scheme. Default: - single user rotation scheme
        :param security_group: The security group for the Lambda rotation function. Default: - a new security group is created
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
            "secret": secret,
            "target": target,
            "vpc": vpc,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if master_secret is not None:
            self._values["master_secret"] = master_secret
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def application(self) -> SecretRotationApplication:
        """The serverless application for the rotation."""
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return result

    @builtins.property
    def secret(self) -> ISecret:
        """The secret to rotate. It must be a JSON string with the following format:.

        Example::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required for multi user rotation: the arn of the master secret which will be used to create users/change passwords>
           }

        This is typically the case for a secret referenced from an ``AWS::SecretsManager::SecretTargetAttachment``
        or an ``ISecret`` returned by the ``attach()`` method of ``Secret``.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        """
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return result

    @builtins.property
    def target(self) -> aws_cdk.aws_ec2.IConnectable:
        """The target service or database."""
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC where the Lambda rotation function will run."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def automatically_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :default: Duration.days(30)
        """
        result = self._values.get("automatically_after")
        return result

    @builtins.property
    def exclude_characters(self) -> typing.Optional[builtins.str]:
        """Characters which should not appear in the generated password.

        :default: - no additional characters are explicitly excluded
        """
        result = self._values.get("exclude_characters")
        return result

    @builtins.property
    def master_secret(self) -> typing.Optional[ISecret]:
        """The master secret for a multi user rotation scheme.

        :default: - single user rotation scheme
        """
        result = self._values.get("master_secret")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """The security group for the Lambda rotation function.

        :default: - a new security group is created
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The type of subnets in the VPC where the Lambda rotation function will run.

        :default: - the Vpc default strategy if not specified.
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretRotationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SecretStringGenerator",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_characters": "excludeCharacters",
        "exclude_lowercase": "excludeLowercase",
        "exclude_numbers": "excludeNumbers",
        "exclude_punctuation": "excludePunctuation",
        "exclude_uppercase": "excludeUppercase",
        "generate_string_key": "generateStringKey",
        "include_space": "includeSpace",
        "password_length": "passwordLength",
        "require_each_included_type": "requireEachIncludedType",
        "secret_string_template": "secretStringTemplate",
    },
)
class SecretStringGenerator:
    def __init__(
        self,
        *,
        exclude_characters: typing.Optional[builtins.str] = None,
        exclude_lowercase: typing.Optional[builtins.bool] = None,
        exclude_numbers: typing.Optional[builtins.bool] = None,
        exclude_punctuation: typing.Optional[builtins.bool] = None,
        exclude_uppercase: typing.Optional[builtins.bool] = None,
        generate_string_key: typing.Optional[builtins.str] = None,
        include_space: typing.Optional[builtins.bool] = None,
        password_length: typing.Optional[jsii.Number] = None,
        require_each_included_type: typing.Optional[builtins.bool] = None,
        secret_string_template: typing.Optional[builtins.str] = None,
    ) -> None:
        """Configuration to generate secrets such as passwords automatically.

        :param exclude_characters: A string that includes characters that shouldn't be included in the generated password. The string can be a minimum of ``0`` and a maximum of ``4096`` characters long. Default: no exclusions
        :param exclude_lowercase: Specifies that the generated password shouldn't include lowercase letters. Default: false
        :param exclude_numbers: Specifies that the generated password shouldn't include digits. Default: false
        :param exclude_punctuation: Specifies that the generated password shouldn't include punctuation characters. Default: false
        :param exclude_uppercase: Specifies that the generated password shouldn't include uppercase letters. Default: false
        :param generate_string_key: The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter. If you specify ``generateStringKey`` then ``secretStringTemplate`` must be also be specified.
        :param include_space: Specifies that the generated password can include the space character. Default: false
        :param password_length: The desired length of the generated password. Default: 32
        :param require_each_included_type: Specifies whether the generated password must include at least one of every allowed character type. Default: true
        :param secret_string_template: A properly structured JSON string that the generated password can be added to. The ``generateStringKey`` is combined with the generated random string and inserted into the JSON structure that's specified by this parameter. The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate`` then ``generateStringKey`` must be also be specified.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if exclude_lowercase is not None:
            self._values["exclude_lowercase"] = exclude_lowercase
        if exclude_numbers is not None:
            self._values["exclude_numbers"] = exclude_numbers
        if exclude_punctuation is not None:
            self._values["exclude_punctuation"] = exclude_punctuation
        if exclude_uppercase is not None:
            self._values["exclude_uppercase"] = exclude_uppercase
        if generate_string_key is not None:
            self._values["generate_string_key"] = generate_string_key
        if include_space is not None:
            self._values["include_space"] = include_space
        if password_length is not None:
            self._values["password_length"] = password_length
        if require_each_included_type is not None:
            self._values["require_each_included_type"] = require_each_included_type
        if secret_string_template is not None:
            self._values["secret_string_template"] = secret_string_template

    @builtins.property
    def exclude_characters(self) -> typing.Optional[builtins.str]:
        """A string that includes characters that shouldn't be included in the generated password.

        The string can be a minimum
        of ``0`` and a maximum of ``4096`` characters long.

        :default: no exclusions
        """
        result = self._values.get("exclude_characters")
        return result

    @builtins.property
    def exclude_lowercase(self) -> typing.Optional[builtins.bool]:
        """Specifies that the generated password shouldn't include lowercase letters.

        :default: false
        """
        result = self._values.get("exclude_lowercase")
        return result

    @builtins.property
    def exclude_numbers(self) -> typing.Optional[builtins.bool]:
        """Specifies that the generated password shouldn't include digits.

        :default: false
        """
        result = self._values.get("exclude_numbers")
        return result

    @builtins.property
    def exclude_punctuation(self) -> typing.Optional[builtins.bool]:
        """Specifies that the generated password shouldn't include punctuation characters.

        :default: false
        """
        result = self._values.get("exclude_punctuation")
        return result

    @builtins.property
    def exclude_uppercase(self) -> typing.Optional[builtins.bool]:
        """Specifies that the generated password shouldn't include uppercase letters.

        :default: false
        """
        result = self._values.get("exclude_uppercase")
        return result

    @builtins.property
    def generate_string_key(self) -> typing.Optional[builtins.str]:
        """The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter.

        If you specify ``generateStringKey`` then ``secretStringTemplate``
        must be also be specified.
        """
        result = self._values.get("generate_string_key")
        return result

    @builtins.property
    def include_space(self) -> typing.Optional[builtins.bool]:
        """Specifies that the generated password can include the space character.

        :default: false
        """
        result = self._values.get("include_space")
        return result

    @builtins.property
    def password_length(self) -> typing.Optional[jsii.Number]:
        """The desired length of the generated password.

        :default: 32
        """
        result = self._values.get("password_length")
        return result

    @builtins.property
    def require_each_included_type(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the generated password must include at least one of every allowed character type.

        :default: true
        """
        result = self._values.get("require_each_included_type")
        return result

    @builtins.property
    def secret_string_template(self) -> typing.Optional[builtins.str]:
        """A properly structured JSON string that the generated password can be added to.

        The ``generateStringKey`` is
        combined with the generated random string and inserted into the JSON structure that's specified by this parameter.
        The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate``
        then ``generateStringKey`` must be also be specified.
        """
        result = self._values.get("secret_string_template")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretStringGenerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISecretTargetAttachment, ISecret)
class SecretTargetAttachment(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-secretsmanager.SecretTargetAttachment",
):
    """An attached secret."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        secret: ISecret,
        target: ISecretAttachmentTarget,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param secret: The secret to attach to the target.
        :param target: (deprecated) The target to attach the secret to.
        """
        props = SecretTargetAttachmentProps(secret=secret, target=target)

        jsii.create(SecretTargetAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretTargetAttachmentSecretArn")
    @builtins.classmethod
    def from_secret_target_attachment_secret_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        secret_target_attachment_secret_arn: builtins.str,
    ) -> ISecretTargetAttachment:
        """
        :param scope: -
        :param id: -
        :param secret_target_attachment_secret_arn: -
        """
        return jsii.sinvoke(cls, "fromSecretTargetAttachmentSecretArn", [scope, id, secret_target_attachment_secret_arn])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[aws_cdk.core.Duration] = None,
        hosted_rotation: typing.Optional[HostedRotation] = None,
        rotation_lambda: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
    ) -> RotationSchedule:
        """Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        """
        options = RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotation_lambda=rotation_lambda,
        )

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="attach")
    def attach(self, target: ISecretAttachmentTarget) -> ISecret:
        """Attach a target to this secret.

        :param target: The target to attach.

        :return: An attached secret
        """
        return jsii.invoke(self, "attach", [target])

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        """Denies the ``DeleteSecret`` action to all principals within the current account."""
        return jsii.invoke(self, "denyAccountRootDelete", [])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        version_stages: typing.Optional[typing.List[builtins.str]] = None,
    ) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants writing and updating the secret value to some role.

        :param grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(
        self,
        json_field: builtins.str,
    ) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -
        """
        return jsii.invoke(self, "secretValueFromJson", [json_field])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="arnForPolicies")
    def _arn_for_policies(self) -> builtins.str:
        """Provides an identifier for this secret for use in IAM policies.

        Typically, this is just the secret ARN.
        However, secrets imported by name require a different format.
        """
        return jsii.get(self, "arnForPolicies")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        return jsii.get(self, "autoCreatePolicy")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        """The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.
        """
        return jsii.get(self, "secretArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        """The name of the secret."""
        return jsii.get(self, "secretName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> builtins.str:
        """Same as ``secretArn``.

        :attribute: true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``."""
        return jsii.get(self, "secretValue")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        """The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).
        """
        return jsii.get(self, "secretFullArn")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SecretTargetAttachmentProps",
    jsii_struct_bases=[AttachedSecretOptions],
    name_mapping={"target": "target", "secret": "secret"},
)
class SecretTargetAttachmentProps(AttachedSecretOptions):
    def __init__(self, *, target: ISecretAttachmentTarget, secret: ISecret) -> None:
        """Construction properties for an AttachedSecret.

        :param target: (deprecated) The target to attach the secret to.
        :param secret: The secret to attach to the target.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target": target,
            "secret": secret,
        }

    @builtins.property
    def target(self) -> ISecretAttachmentTarget:
        """(deprecated) The target to attach the secret to.

        :stability: deprecated
        """
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return result

    @builtins.property
    def secret(self) -> ISecret:
        """The secret to attach to the target."""
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretTargetAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.SingleUserHostedRotationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "security_groups": "securityGroups",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class SingleUserHostedRotationOptions:
    def __init__(
        self,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Single user hosted rotation options.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {}
        if function_name is not None:
            self._values["function_name"] = function_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        """A name for the Lambda created to rotate the secret.

        :default: - a CloudFormation generated name
        """
        result = self._values.get("function_name")
        return result

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """A list of security groups for the Lambda created to rotate the secret.

        :default: - a new security group is created
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the Lambda rotation function will run.

        :default: - the Lambda is not deployed in a VPC
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The type of subnets in the VPC where the Lambda rotation function will run.

        :default: - the Vpc default strategy if not specified.
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SingleUserHostedRotationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-secretsmanager.MultiUserHostedRotationOptions",
    jsii_struct_bases=[SingleUserHostedRotationOptions],
    name_mapping={
        "function_name": "functionName",
        "security_groups": "securityGroups",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "master_secret": "masterSecret",
    },
)
class MultiUserHostedRotationOptions(SingleUserHostedRotationOptions):
    def __init__(
        self,
        *,
        function_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        master_secret: ISecret,
    ) -> None:
        """Multi user hosted rotation options.

        :param function_name: A name for the Lambda created to rotate the secret. Default: - a CloudFormation generated name
        :param security_groups: A list of security groups for the Lambda created to rotate the secret. Default: - a new security group is created
        :param vpc: The VPC where the Lambda rotation function will run. Default: - the Lambda is not deployed in a VPC
        :param vpc_subnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - the Vpc default strategy if not specified.
        :param master_secret: The master secret for a multi user rotation scheme.
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "master_secret": master_secret,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        """A name for the Lambda created to rotate the secret.

        :default: - a CloudFormation generated name
        """
        result = self._values.get("function_name")
        return result

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """A list of security groups for the Lambda created to rotate the secret.

        :default: - a new security group is created
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the Lambda rotation function will run.

        :default: - the Lambda is not deployed in a VPC
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The type of subnets in the VPC where the Lambda rotation function will run.

        :default: - the Vpc default strategy if not specified.
        """
        result = self._values.get("vpc_subnets")
        return result

    @builtins.property
    def master_secret(self) -> ISecret:
        """The master secret for a multi user rotation scheme."""
        result = self._values.get("master_secret")
        assert result is not None, "Required property 'master_secret' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultiUserHostedRotationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AttachedSecretOptions",
    "AttachmentTargetType",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnRotationSchedule",
    "CfnRotationScheduleProps",
    "CfnSecret",
    "CfnSecretProps",
    "CfnSecretTargetAttachment",
    "CfnSecretTargetAttachmentProps",
    "HostedRotation",
    "HostedRotationType",
    "ISecret",
    "ISecretAttachmentTarget",
    "ISecretTargetAttachment",
    "MultiUserHostedRotationOptions",
    "ResourcePolicy",
    "ResourcePolicyProps",
    "RotationSchedule",
    "RotationScheduleOptions",
    "RotationScheduleProps",
    "Secret",
    "SecretAttachmentTargetProps",
    "SecretAttributes",
    "SecretProps",
    "SecretRotation",
    "SecretRotationApplication",
    "SecretRotationApplicationOptions",
    "SecretRotationProps",
    "SecretStringGenerator",
    "SecretTargetAttachment",
    "SecretTargetAttachmentProps",
    "SingleUserHostedRotationOptions",
]

publication.publish()
