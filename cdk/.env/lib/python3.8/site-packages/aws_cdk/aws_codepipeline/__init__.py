"""
## AWS CodePipeline Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

### Pipeline

To construct an empty Pipeline:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codepipeline as codepipeline

pipeline = codepipeline.Pipeline(self, "MyFirstPipeline")
```

To give the Pipeline a nice, human-readable name:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
    pipeline_name="MyPipeline"
)
```

Be aware that in the default configuration, the `Pipeline` construct creates
an AWS Key Management Service (AWS KMS) Customer Master Key (CMK) for you to
encrypt the artifacts in the artifact bucket, which incurs a cost of
**$1/month**. This default configuration is necessary to allow cross-account
actions.

If you do not intend to perform cross-account deployments, you can disable
the creation of the Customer Master Keys by passing `crossAccountKeys: false`
when defining the Pipeline:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
    cross_account_keys=False
)
```

### Stages

You can provide Stages when creating the Pipeline:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
    stages=[{
        "stage_name": "Source",
        "actions": []
    }
    ]
)
```

Or append a Stage to an existing Pipeline:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
source_stage = pipeline.add_stage(
    stage_name="Source",
    actions=[]
)
```

You can insert the new Stage at an arbitrary point in the Pipeline:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
some_stage = pipeline.add_stage(
    stage_name="SomeStage",
    placement={
        # note: you can only specify one of the below properties
        "right_before": another_stage,
        "just_after": another_stage
    }
)
```

### Actions

Actions live in a separate package, `@aws-cdk/aws-codepipeline-actions`.

To add an Action to a Stage, you can provide it when creating the Stage,
in the `actions` property,
or you can use the `IStage.addAction()` method to mutate an existing Stage:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
source_stage.add_action(some_action)
```

### Cross-account CodePipelines

> Cross-account Pipeline actions require that the Pipeline has *not* been
> created with `crossAccountKeys: false`.

Most pipeline Actions accept an AWS resource object to operate on. For example:

* `S3DeployAction` accepts an `s3.IBucket`.
* `CodeBuildAction` accepts a `codebuild.IProject`.
* etc.

These resources can be either newly defined (`new s3.Bucket(...)`) or imported
(`s3.Bucket.fromBucketAttributes(...)`) and identify the resource that should
be changed.

These resources can be in different accounts than the pipeline itself. For
example, the following action deploys to an imported S3 bucket from a
different account:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stage.add_action(codepipeline_actions.S3DeployAction(
    bucket=s3.Bucket.from_bucket_attributes(self, "Bucket",
        account="123456789012"
    )
))
```

Actions that don't accept a resource object accept an explicit `account` parameter:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stage.add_action(codepipeline_actions.CloudFormationCreateUpdateStackAction(
    account="123456789012"
))
```

The `Pipeline` construct automatically defines an **IAM Role** for you in the
target account which the pipeline will assume to perform that action. This
Role will be defined in a **support stack** named
`<PipelineStackName>-support-<account>`, that will automatically be deployed
before the stack containing the pipeline.

If you do not want to use the generated role, you can also explicitly pass a
`role` when creating the action. In that case, the action will operate in the
account the role belongs to:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stage.add_action(codepipeline_actions.CloudFormationCreateUpdateStackAction(
    # ...
    role=iam.Role.from_role_arn(self, "ActionRole", "...")
))
```

### Cross-region CodePipelines

Similar to how you set up a cross-account Action, the AWS resource object you
pass to actions can also be in different *Regions*. For example, the
following Action deploys to an imported S3 bucket from a different Region:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stage.add_action(codepipeline_actions.S3DeployAction(
    bucket=s3.Bucket.from_bucket_attributes(self, "Bucket",
        region="us-west-1"
    )
))
```

Actions that don't take an AWS resource will accept an explicit `region`
parameter:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stage.add_action(codepipeline_actions.CloudFormationCreateUpdateStackAction(
    # ...
    region="us-west-1"
))
```

The `Pipeline` construct automatically defines a **replication bucket** for
you in the target region, which the pipeline will replicate artifacts to and
from. This Bucket will be defined in a **support stack** named
`<PipelineStackName>-support-<region>`, that will automatically be deployed
before the stack containing the pipeline.

If you don't want to use these support stacks, and already have buckets in
place to serve as replication buckets, you can supply these at Pipeline definition
time using the `crossRegionReplicationBuckets` parameter. Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pipeline = codepipeline.Pipeline(self, "MyFirstPipeline")crossRegionReplicationBuckets: {
    // note that a physical name of the replication Bucket must be known at synthesis time
    'us-west-1': s3.Bucket.fromBucketAttributes(this, 'UsWest1ReplicationBucket', {
      bucketName: 'my-us-west-1-replication-bucket',
      // optional KMS key
      encryptionKey: kms.Key.fromKeyArn(this, 'UsWest1ReplicationKey',
        'arn:aws:kms:us-west-1:123456789012:key/1234-5678-9012'
      ),
    }),
  }
```

See [the AWS docs here](https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-create-cross-region.html)
for more information on cross-region CodePipelines.

#### Creating an encrypted replication bucket

If you're passing a replication bucket created in a different stack,
like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
replication_stack = Stack(app, "ReplicationStack",
    env={
        "region": "us-west-1"
    }
)
key = kms.Key(replication_stack, "ReplicationKey")
replication_bucket = s3.Bucket(replication_stack, "ReplicationBucket",
    # like was said above - replication buckets need a set physical name
    bucket_name=PhysicalName.GENERATE_IF_NEEDED,
    encryption_key=key
)

# later...
codepipeline.Pipeline(pipeline_stack, "Pipeline",
    cross_region_replication_buckets={
        "us-west-1": replication_bucket
    }
)
```

When trying to encrypt it
(and note that if any of the cross-region actions happen to be cross-account as well,
the bucket *has to* be encrypted - otherwise the pipeline will fail at runtime),
you cannot use a key directly - KMS keys don't have physical names,
and so you can't reference them across environments.

In this case, you need to use an alias in place of the key when creating the bucket:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
key = kms.Key(replication_stack, "ReplicationKey")
alias = kms.Alias(replication_stack, "ReplicationAlias",
    # aliasName is required
    alias_name=PhysicalName.GENERATE_IF_NEEDED,
    target_key=key
)
replication_bucket = s3.Bucket(replication_stack, "ReplicationBucket",
    bucket_name=PhysicalName.GENERATE_IF_NEEDED,
    encryption_key=alias
)
```

### Variables

The library supports the CodePipeline Variables feature.
Each action class that emits variables has a separate variables interface,
accessed as a property of the action instance called `variables`.
You instantiate the action class and assign it to a local variable;
when you want to use a variable in the configuration of a different action,
you access the appropriate property of the interface returned from `variables`,
which represents a single variable.
Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# MyAction is some action type that produces variables
my_action = MyAction()
OtherAction(
    # ...
    config=my_action.variables.my_variable
)
```

The namespace name that will be used will be automatically generated by the pipeline construct,
based on the stage and action name;
you can pass a custom name when creating the action instance:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_action = MyAction(
    # ...
    variables_namespace="MyNamespace"
)
```

There are also global variables available,
not tied to any action;
these are accessed through static properties of the `GlobalVariables` class:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
OtherAction(
    # ...
    config=codepipeline.GlobalVariables.execution_id
)
```

Check the documentation of the `@aws-cdk/aws-codepipeline-actions`
for details on how to use the variables for each action class.

See the [CodePipeline documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html)
for more details on how to use the variables feature.

### Events

#### Using a pipeline as an event target

A pipeline can be used as a target for a CloudWatch event rule:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_events as events

# kick off the pipeline every day
rule = events.Rule(self, "Daily",
    schedule=events.Schedule.rate(Duration.days(1))
)

rule.add_target(targets.CodePipeline(pipeline))
```

When a pipeline is used as an event target, the
"codepipeline:StartPipelineExecution" permission is granted to the AWS
CloudWatch Events service.

#### Event sources

Pipelines emit CloudWatch events. To define event rules for events emitted by
the pipeline, stages or action, use the `onXxx` methods on the respective
construct:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_pipeline.on_state_change("MyPipelineStateChange", target)
my_stage.on_state_change("MyStageStateChange", target)
my_action.on_state_change("MyActionStateChange", target)
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

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.ActionArtifactBounds",
    jsii_struct_bases=[],
    name_mapping={
        "max_inputs": "maxInputs",
        "max_outputs": "maxOutputs",
        "min_inputs": "minInputs",
        "min_outputs": "minOutputs",
    },
)
class ActionArtifactBounds:
    def __init__(
        self,
        *,
        max_inputs: jsii.Number,
        max_outputs: jsii.Number,
        min_inputs: jsii.Number,
        min_outputs: jsii.Number,
    ) -> None:
        """Specifies the constraints on the number of input and output artifacts an action can have.

        The constraints for each action type are documented on the
        {@link https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html Pipeline Structure Reference} page.

        :param max_inputs: 
        :param max_outputs: 
        :param min_inputs: 
        :param min_outputs: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "max_inputs": max_inputs,
            "max_outputs": max_outputs,
            "min_inputs": min_inputs,
            "min_outputs": min_outputs,
        }

    @builtins.property
    def max_inputs(self) -> jsii.Number:
        result = self._values.get("max_inputs")
        assert result is not None, "Required property 'max_inputs' is missing"
        return result

    @builtins.property
    def max_outputs(self) -> jsii.Number:
        result = self._values.get("max_outputs")
        assert result is not None, "Required property 'max_outputs' is missing"
        return result

    @builtins.property
    def min_inputs(self) -> jsii.Number:
        result = self._values.get("min_inputs")
        assert result is not None, "Required property 'min_inputs' is missing"
        return result

    @builtins.property
    def min_outputs(self) -> jsii.Number:
        result = self._values.get("min_outputs")
        assert result is not None, "Required property 'min_outputs' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionArtifactBounds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.ActionBindOptions",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "role": "role"},
)
class ActionBindOptions:
    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        role: aws_cdk.aws_iam.IRole,
    ) -> None:
        """
        :param bucket: 
        :param role: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "role": role,
        }

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return result

    @builtins.property
    def role(self) -> aws_cdk.aws_iam.IRole:
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline.ActionCategory")
class ActionCategory(enum.Enum):
    SOURCE = "SOURCE"
    BUILD = "BUILD"
    TEST = "TEST"
    APPROVAL = "APPROVAL"
    DEPLOY = "DEPLOY"
    INVOKE = "INVOKE"


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.ActionConfig",
    jsii_struct_bases=[],
    name_mapping={"configuration": "configuration"},
)
class ActionConfig:
    def __init__(self, *, configuration: typing.Any = None) -> None:
        """
        :param configuration: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration

    @builtins.property
    def configuration(self) -> typing.Any:
        result = self._values.get("configuration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.ActionProperties",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "artifact_bounds": "artifactBounds",
        "category": "category",
        "provider": "provider",
        "account": "account",
        "inputs": "inputs",
        "outputs": "outputs",
        "owner": "owner",
        "region": "region",
        "resource": "resource",
        "role": "role",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "version": "version",
    },
)
class ActionProperties:
    def __init__(
        self,
        *,
        action_name: builtins.str,
        artifact_bounds: ActionArtifactBounds,
        category: ActionCategory,
        provider: builtins.str,
        account: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.List["Artifact"]] = None,
        outputs: typing.Optional[typing.List["Artifact"]] = None,
        owner: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource: typing.Optional[aws_cdk.core.IResource] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param action_name: 
        :param artifact_bounds: 
        :param category: The category of the action. The category defines which action type the owner (the entity that performs the action) performs.
        :param provider: The service provider that the action calls.
        :param account: The account the Action is supposed to live in. For Actions backed by resources, this is inferred from the Stack {@link resource} is part of. However, some Actions, like the CloudFormation ones, are not backed by any resource, and they still might want to be cross-account. In general, a concrete Action class should specify either {@link resource}, or {@link account} - but not both.
        :param inputs: 
        :param outputs: 
        :param owner: 
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param resource: The optional resource that is backing this Action. This is used for automatically handling Actions backed by resources from a different account and/or region.
        :param role: 
        :param run_order: The order in which AWS CodePipeline runs this action. For more information, see the AWS CodePipeline User Guide. https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names
        :param version: 
        """
        if isinstance(artifact_bounds, dict):
            artifact_bounds = ActionArtifactBounds(**artifact_bounds)
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "artifact_bounds": artifact_bounds,
            "category": category,
            "provider": provider,
        }
        if account is not None:
            self._values["account"] = account
        if inputs is not None:
            self._values["inputs"] = inputs
        if outputs is not None:
            self._values["outputs"] = outputs
        if owner is not None:
            self._values["owner"] = owner
        if region is not None:
            self._values["region"] = region
        if resource is not None:
            self._values["resource"] = resource
        if role is not None:
            self._values["role"] = role
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def action_name(self) -> builtins.str:
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return result

    @builtins.property
    def artifact_bounds(self) -> ActionArtifactBounds:
        result = self._values.get("artifact_bounds")
        assert result is not None, "Required property 'artifact_bounds' is missing"
        return result

    @builtins.property
    def category(self) -> ActionCategory:
        """The category of the action.

        The category defines which action type the owner
        (the entity that performs the action) performs.
        """
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return result

    @builtins.property
    def provider(self) -> builtins.str:
        """The service provider that the action calls."""
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return result

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """The account the Action is supposed to live in.

        For Actions backed by resources,
        this is inferred from the Stack {@link resource} is part of.
        However, some Actions, like the CloudFormation ones,
        are not backed by any resource, and they still might want to be cross-account.
        In general, a concrete Action class should specify either {@link resource},
        or {@link account} - but not both.
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def inputs(self) -> typing.Optional[typing.List["Artifact"]]:
        result = self._values.get("inputs")
        return result

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List["Artifact"]]:
        result = self._values.get("outputs")
        return result

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        result = self._values.get("owner")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        :default: the Action resides in the same region as the Pipeline
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def resource(self) -> typing.Optional[aws_cdk.core.IResource]:
        """The optional resource that is backing this Action.

        This is used for automatically handling Actions backed by
        resources from a different account and/or region.
        """
        result = self._values.get("resource")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        result = self._values.get("role")
        return result

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The order in which AWS CodePipeline runs this action. For more information, see the AWS CodePipeline User Guide.

        https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements
        """
        result = self._values.get("run_order")
        return result

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        """The name of the namespace to use for variables emitted by this action.

        :default: - a name will be generated, based on the stage and action names
        """
        result = self._values.get("variables_namespace")
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Artifact(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.Artifact"):
    """An output artifact of an action.

    Artifacts can be used as input by some actions.
    """

    def __init__(self, artifact_name: typing.Optional[builtins.str] = None) -> None:
        """
        :param artifact_name: -
        """
        jsii.create(Artifact, self, [artifact_name])

    @jsii.member(jsii_name="artifact")
    @builtins.classmethod
    def artifact(cls, name: builtins.str) -> "Artifact":
        """A static factory method used to create instances of the Artifact class.

        Mainly meant to be used from ``decdk``.

        :param name: the (required) name of the Artifact.
        """
        return jsii.sinvoke(cls, "artifact", [name])

    @jsii.member(jsii_name="atPath")
    def at_path(self, file_name: builtins.str) -> "ArtifactPath":
        """Returns an ArtifactPath for a file within this artifact.

        CfnOutput is in the form "::"

        :param file_name: The name of the file.
        """
        return jsii.invoke(self, "atPath", [file_name])

    @jsii.member(jsii_name="getMetadata")
    def get_metadata(self, key: builtins.str) -> typing.Any:
        """Retrieve the metadata stored in this artifact under the given key.

        If there is no metadata stored under the given key,
        null will be returned.

        :param key: -
        """
        return jsii.invoke(self, "getMetadata", [key])

    @jsii.member(jsii_name="getParam")
    def get_param(
        self,
        json_file: builtins.str,
        key_name: builtins.str,
    ) -> builtins.str:
        """Returns a token for a value inside a JSON file within this artifact.

        :param json_file: The JSON file name.
        :param key_name: The hash key.
        """
        return jsii.invoke(self, "getParam", [json_file, key_name])

    @jsii.member(jsii_name="setMetadata")
    def set_metadata(self, key: builtins.str, value: typing.Any) -> None:
        """Add arbitrary extra payload to the artifact under a given key.

        This can be used by CodePipeline actions to communicate data between themselves.
        If metadata was already present under the given key,
        it will be overwritten with the new value.

        :param key: -
        :param value: -
        """
        return jsii.invoke(self, "setMetadata", [key, value])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> typing.Optional[builtins.str]:
        return jsii.invoke(self, "toString", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        """The artifact attribute for the name of the S3 bucket where the artifact is stored."""
        return jsii.get(self, "bucketName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="objectKey")
    def object_key(self) -> builtins.str:
        """The artifact attribute for The name of the .zip file that contains the artifact that is generated by AWS CodePipeline, such as 1ABCyZZ.zip."""
        return jsii.get(self, "objectKey")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="s3Location")
    def s3_location(self) -> aws_cdk.aws_s3.Location:
        """Returns the location of the .zip file in S3 that this Artifact represents. Used by Lambda's ``CfnParametersCode`` when being deployed in a CodePipeline."""
        return jsii.get(self, "s3Location")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        """The artifact attribute of the Amazon Simple Storage Service (Amazon S3) URL of the artifact, such as https://s3-us-west-2.amazonaws.com/artifactstorebucket-yivczw8jma0c/test/TemplateSo/1ABCyZZ.zip."""
        return jsii.get(self, "url")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="artifactName")
    def artifact_name(self) -> typing.Optional[builtins.str]:
        return jsii.get(self, "artifactName")


class ArtifactPath(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codepipeline.ArtifactPath",
):
    """A specific file within an output artifact.

    The most common use case for this is specifying the template file
    for a CloudFormation action.
    """

    def __init__(self, artifact: Artifact, file_name: builtins.str) -> None:
        """
        :param artifact: -
        :param file_name: -
        """
        jsii.create(ArtifactPath, self, [artifact, file_name])

    @jsii.member(jsii_name="artifactPath")
    @builtins.classmethod
    def artifact_path(
        cls,
        artifact_name: builtins.str,
        file_name: builtins.str,
    ) -> "ArtifactPath":
        """
        :param artifact_name: -
        :param file_name: -
        """
        return jsii.sinvoke(cls, "artifactPath", [artifact_name, file_name])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="artifact")
    def artifact(self) -> Artifact:
        return jsii.get(self, "artifact")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return jsii.get(self, "fileName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return jsii.get(self, "location")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCustomActionType(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType",
):
    """A CloudFormation ``AWS::CodePipeline::CustomActionType``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html
    :cloudformationResource: AWS::CodePipeline::CustomActionType
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        category: builtins.str,
        input_artifact_details: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable],
        output_artifact_details: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable],
        provider: builtins.str,
        version: builtins.str,
        configuration_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.ConfigurationPropertiesProperty"]]]] = None,
        settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.SettingsProperty"]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::CodePipeline::CustomActionType``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param category: ``AWS::CodePipeline::CustomActionType.Category``.
        :param input_artifact_details: ``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.
        :param output_artifact_details: ``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.
        :param provider: ``AWS::CodePipeline::CustomActionType.Provider``.
        :param version: ``AWS::CodePipeline::CustomActionType.Version``.
        :param configuration_properties: ``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.
        :param settings: ``AWS::CodePipeline::CustomActionType.Settings``.
        :param tags: ``AWS::CodePipeline::CustomActionType.Tags``.
        """
        props = CfnCustomActionTypeProps(
            category=category,
            input_artifact_details=input_artifact_details,
            output_artifact_details=output_artifact_details,
            provider=provider,
            version=version,
            configuration_properties=configuration_properties,
            settings=settings,
            tags=tags,
        )

        jsii.create(CfnCustomActionType, self, [scope, id, props])

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
        """``AWS::CodePipeline::CustomActionType.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        """``AWS::CodePipeline::CustomActionType.Category``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-category
        """
        return jsii.get(self, "category")

    @category.setter # type: ignore
    def category(self, value: builtins.str) -> None:
        jsii.set(self, "category", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="inputArtifactDetails")
    def input_artifact_details(
        self,
    ) -> typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-inputartifactdetails
        """
        return jsii.get(self, "inputArtifactDetails")

    @input_artifact_details.setter # type: ignore
    def input_artifact_details(
        self,
        value: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "inputArtifactDetails", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outputArtifactDetails")
    def output_artifact_details(
        self,
    ) -> typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-outputartifactdetails
        """
        return jsii.get(self, "outputArtifactDetails")

    @output_artifact_details.setter # type: ignore
    def output_artifact_details(
        self,
        value: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "outputArtifactDetails", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        """``AWS::CodePipeline::CustomActionType.Provider``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-provider
        """
        return jsii.get(self, "provider")

    @provider.setter # type: ignore
    def provider(self, value: builtins.str) -> None:
        jsii.set(self, "provider", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        """``AWS::CodePipeline::CustomActionType.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-version
        """
        return jsii.get(self, "version")

    @version.setter # type: ignore
    def version(self, value: builtins.str) -> None:
        jsii.set(self, "version", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="configurationProperties")
    def configuration_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.ConfigurationPropertiesProperty"]]]]:
        """``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-configurationproperties
        """
        return jsii.get(self, "configurationProperties")

    @configuration_properties.setter # type: ignore
    def configuration_properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.ConfigurationPropertiesProperty"]]]],
    ) -> None:
        jsii.set(self, "configurationProperties", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="settings")
    def settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.SettingsProperty"]]:
        """``AWS::CodePipeline::CustomActionType.Settings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-settings
        """
        return jsii.get(self, "settings")

    @settings.setter # type: ignore
    def settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.SettingsProperty"]],
    ) -> None:
        jsii.set(self, "settings", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.ArtifactDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_count": "maximumCount",
            "minimum_count": "minimumCount",
        },
    )
    class ArtifactDetailsProperty:
        def __init__(
            self,
            *,
            maximum_count: jsii.Number,
            minimum_count: jsii.Number,
        ) -> None:
            """
            :param maximum_count: ``CfnCustomActionType.ArtifactDetailsProperty.MaximumCount``.
            :param minimum_count: ``CfnCustomActionType.ArtifactDetailsProperty.MinimumCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "maximum_count": maximum_count,
                "minimum_count": minimum_count,
            }

        @builtins.property
        def maximum_count(self) -> jsii.Number:
            """``CfnCustomActionType.ArtifactDetailsProperty.MaximumCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html#cfn-codepipeline-customactiontype-artifactdetails-maximumcount
            """
            result = self._values.get("maximum_count")
            assert result is not None, "Required property 'maximum_count' is missing"
            return result

        @builtins.property
        def minimum_count(self) -> jsii.Number:
            """``CfnCustomActionType.ArtifactDetailsProperty.MinimumCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html#cfn-codepipeline-customactiontype-artifactdetails-minimumcount
            """
            result = self._values.get("minimum_count")
            assert result is not None, "Required property 'minimum_count' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.ConfigurationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "name": "name",
            "required": "required",
            "secret": "secret",
            "description": "description",
            "queryable": "queryable",
            "type": "type",
        },
    )
    class ConfigurationPropertiesProperty:
        def __init__(
            self,
            *,
            key: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            name: builtins.str,
            required: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            secret: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            description: typing.Optional[builtins.str] = None,
            queryable: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param key: ``CfnCustomActionType.ConfigurationPropertiesProperty.Key``.
            :param name: ``CfnCustomActionType.ConfigurationPropertiesProperty.Name``.
            :param required: ``CfnCustomActionType.ConfigurationPropertiesProperty.Required``.
            :param secret: ``CfnCustomActionType.ConfigurationPropertiesProperty.Secret``.
            :param description: ``CfnCustomActionType.ConfigurationPropertiesProperty.Description``.
            :param queryable: ``CfnCustomActionType.ConfigurationPropertiesProperty.Queryable``.
            :param type: ``CfnCustomActionType.ConfigurationPropertiesProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "name": name,
                "required": required,
                "secret": secret,
            }
            if description is not None:
                self._values["description"] = description
            if queryable is not None:
                self._values["queryable"] = queryable
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def key(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def required(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Required``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-required
            """
            result = self._values.get("required")
            assert result is not None, "Required property 'required' is missing"
            return result

        @builtins.property
        def secret(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Secret``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-secret
            """
            result = self._values.get("secret")
            assert result is not None, "Required property 'secret' is missing"
            return result

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Description``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-description
            """
            result = self._values.get("description")
            return result

        @builtins.property
        def queryable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Queryable``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-queryable
            """
            result = self._values.get("queryable")
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-type
            """
            result = self._values.get("type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.SettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "entity_url_template": "entityUrlTemplate",
            "execution_url_template": "executionUrlTemplate",
            "revision_url_template": "revisionUrlTemplate",
            "third_party_configuration_url": "thirdPartyConfigurationUrl",
        },
    )
    class SettingsProperty:
        def __init__(
            self,
            *,
            entity_url_template: typing.Optional[builtins.str] = None,
            execution_url_template: typing.Optional[builtins.str] = None,
            revision_url_template: typing.Optional[builtins.str] = None,
            third_party_configuration_url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param entity_url_template: ``CfnCustomActionType.SettingsProperty.EntityUrlTemplate``.
            :param execution_url_template: ``CfnCustomActionType.SettingsProperty.ExecutionUrlTemplate``.
            :param revision_url_template: ``CfnCustomActionType.SettingsProperty.RevisionUrlTemplate``.
            :param third_party_configuration_url: ``CfnCustomActionType.SettingsProperty.ThirdPartyConfigurationUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if entity_url_template is not None:
                self._values["entity_url_template"] = entity_url_template
            if execution_url_template is not None:
                self._values["execution_url_template"] = execution_url_template
            if revision_url_template is not None:
                self._values["revision_url_template"] = revision_url_template
            if third_party_configuration_url is not None:
                self._values["third_party_configuration_url"] = third_party_configuration_url

        @builtins.property
        def entity_url_template(self) -> typing.Optional[builtins.str]:
            """``CfnCustomActionType.SettingsProperty.EntityUrlTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-entityurltemplate
            """
            result = self._values.get("entity_url_template")
            return result

        @builtins.property
        def execution_url_template(self) -> typing.Optional[builtins.str]:
            """``CfnCustomActionType.SettingsProperty.ExecutionUrlTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-executionurltemplate
            """
            result = self._values.get("execution_url_template")
            return result

        @builtins.property
        def revision_url_template(self) -> typing.Optional[builtins.str]:
            """``CfnCustomActionType.SettingsProperty.RevisionUrlTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-revisionurltemplate
            """
            result = self._values.get("revision_url_template")
            return result

        @builtins.property
        def third_party_configuration_url(self) -> typing.Optional[builtins.str]:
            """``CfnCustomActionType.SettingsProperty.ThirdPartyConfigurationUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-thirdpartyconfigurationurl
            """
            result = self._values.get("third_party_configuration_url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionTypeProps",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "input_artifact_details": "inputArtifactDetails",
        "output_artifact_details": "outputArtifactDetails",
        "provider": "provider",
        "version": "version",
        "configuration_properties": "configurationProperties",
        "settings": "settings",
        "tags": "tags",
    },
)
class CfnCustomActionTypeProps:
    def __init__(
        self,
        *,
        category: builtins.str,
        input_artifact_details: typing.Union[CfnCustomActionType.ArtifactDetailsProperty, aws_cdk.core.IResolvable],
        output_artifact_details: typing.Union[CfnCustomActionType.ArtifactDetailsProperty, aws_cdk.core.IResolvable],
        provider: builtins.str,
        version: builtins.str,
        configuration_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnCustomActionType.ConfigurationPropertiesProperty]]]] = None,
        settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCustomActionType.SettingsProperty]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodePipeline::CustomActionType``.

        :param category: ``AWS::CodePipeline::CustomActionType.Category``.
        :param input_artifact_details: ``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.
        :param output_artifact_details: ``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.
        :param provider: ``AWS::CodePipeline::CustomActionType.Provider``.
        :param version: ``AWS::CodePipeline::CustomActionType.Version``.
        :param configuration_properties: ``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.
        :param settings: ``AWS::CodePipeline::CustomActionType.Settings``.
        :param tags: ``AWS::CodePipeline::CustomActionType.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "category": category,
            "input_artifact_details": input_artifact_details,
            "output_artifact_details": output_artifact_details,
            "provider": provider,
            "version": version,
        }
        if configuration_properties is not None:
            self._values["configuration_properties"] = configuration_properties
        if settings is not None:
            self._values["settings"] = settings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def category(self) -> builtins.str:
        """``AWS::CodePipeline::CustomActionType.Category``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-category
        """
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return result

    @builtins.property
    def input_artifact_details(
        self,
    ) -> typing.Union[CfnCustomActionType.ArtifactDetailsProperty, aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-inputartifactdetails
        """
        result = self._values.get("input_artifact_details")
        assert result is not None, "Required property 'input_artifact_details' is missing"
        return result

    @builtins.property
    def output_artifact_details(
        self,
    ) -> typing.Union[CfnCustomActionType.ArtifactDetailsProperty, aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-outputartifactdetails
        """
        result = self._values.get("output_artifact_details")
        assert result is not None, "Required property 'output_artifact_details' is missing"
        return result

    @builtins.property
    def provider(self) -> builtins.str:
        """``AWS::CodePipeline::CustomActionType.Provider``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-provider
        """
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return result

    @builtins.property
    def version(self) -> builtins.str:
        """``AWS::CodePipeline::CustomActionType.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-version
        """
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    @builtins.property
    def configuration_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnCustomActionType.ConfigurationPropertiesProperty]]]]:
        """``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-configurationproperties
        """
        result = self._values.get("configuration_properties")
        return result

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCustomActionType.SettingsProperty]]:
        """``AWS::CodePipeline::CustomActionType.Settings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-settings
        """
        result = self._values.get("settings")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodePipeline::CustomActionType.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomActionTypeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPipeline(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline",
):
    """A CloudFormation ``AWS::CodePipeline::Pipeline``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
    :cloudformationResource: AWS::CodePipeline::Pipeline
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        role_arn: builtins.str,
        stages: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageDeclarationProperty"]]],
        artifact_store: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreProperty"]] = None,
        artifact_stores: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreMapProperty"]]]] = None,
        disable_inbound_stage_transitions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageTransitionProperty"]]]] = None,
        name: typing.Optional[builtins.str] = None,
        restart_execution_on_update: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::CodePipeline::Pipeline``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role_arn: ``AWS::CodePipeline::Pipeline.RoleArn``.
        :param stages: ``AWS::CodePipeline::Pipeline.Stages``.
        :param artifact_store: ``AWS::CodePipeline::Pipeline.ArtifactStore``.
        :param artifact_stores: ``AWS::CodePipeline::Pipeline.ArtifactStores``.
        :param disable_inbound_stage_transitions: ``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.
        :param name: ``AWS::CodePipeline::Pipeline.Name``.
        :param restart_execution_on_update: ``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.
        :param tags: ``AWS::CodePipeline::Pipeline.Tags``.
        """
        props = CfnPipelineProps(
            role_arn=role_arn,
            stages=stages,
            artifact_store=artifact_store,
            artifact_stores=artifact_stores,
            disable_inbound_stage_transitions=disable_inbound_stage_transitions,
            name=name,
            restart_execution_on_update=restart_execution_on_update,
            tags=tags,
        )

        jsii.create(CfnPipeline, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        """
        :cloudformationAttribute: Version
        """
        return jsii.get(self, "attrVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CodePipeline::Pipeline.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        """``AWS::CodePipeline::Pipeline.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stages")
    def stages(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageDeclarationProperty"]]]:
        """``AWS::CodePipeline::Pipeline.Stages``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-stages
        """
        return jsii.get(self, "stages")

    @stages.setter # type: ignore
    def stages(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageDeclarationProperty"]]],
    ) -> None:
        jsii.set(self, "stages", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="artifactStore")
    def artifact_store(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreProperty"]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStore``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstore
        """
        return jsii.get(self, "artifactStore")

    @artifact_store.setter # type: ignore
    def artifact_store(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreProperty"]],
    ) -> None:
        jsii.set(self, "artifactStore", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="artifactStores")
    def artifact_stores(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreMapProperty"]]]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStores``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstores
        """
        return jsii.get(self, "artifactStores")

    @artifact_stores.setter # type: ignore
    def artifact_stores(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreMapProperty"]]]],
    ) -> None:
        jsii.set(self, "artifactStores", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="disableInboundStageTransitions")
    def disable_inbound_stage_transitions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageTransitionProperty"]]]]:
        """``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-disableinboundstagetransitions
        """
        return jsii.get(self, "disableInboundStageTransitions")

    @disable_inbound_stage_transitions.setter # type: ignore
    def disable_inbound_stage_transitions(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageTransitionProperty"]]]],
    ) -> None:
        jsii.set(self, "disableInboundStageTransitions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodePipeline::Pipeline.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="restartExecutionOnUpdate")
    def restart_execution_on_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-restartexecutiononupdate
        """
        return jsii.get(self, "restartExecutionOnUpdate")

    @restart_execution_on_update.setter # type: ignore
    def restart_execution_on_update(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "restartExecutionOnUpdate", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ActionDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_type_id": "actionTypeId",
            "name": "name",
            "configuration": "configuration",
            "input_artifacts": "inputArtifacts",
            "namespace": "namespace",
            "output_artifacts": "outputArtifacts",
            "region": "region",
            "role_arn": "roleArn",
            "run_order": "runOrder",
        },
    )
    class ActionDeclarationProperty:
        def __init__(
            self,
            *,
            action_type_id: typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionTypeIdProperty"],
            name: builtins.str,
            configuration: typing.Any = None,
            input_artifacts: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.InputArtifactProperty"]]]] = None,
            namespace: typing.Optional[builtins.str] = None,
            output_artifacts: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.OutputArtifactProperty"]]]] = None,
            region: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            run_order: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param action_type_id: ``CfnPipeline.ActionDeclarationProperty.ActionTypeId``.
            :param name: ``CfnPipeline.ActionDeclarationProperty.Name``.
            :param configuration: ``CfnPipeline.ActionDeclarationProperty.Configuration``.
            :param input_artifacts: ``CfnPipeline.ActionDeclarationProperty.InputArtifacts``.
            :param namespace: ``CfnPipeline.ActionDeclarationProperty.Namespace``.
            :param output_artifacts: ``CfnPipeline.ActionDeclarationProperty.OutputArtifacts``.
            :param region: ``CfnPipeline.ActionDeclarationProperty.Region``.
            :param role_arn: ``CfnPipeline.ActionDeclarationProperty.RoleArn``.
            :param run_order: ``CfnPipeline.ActionDeclarationProperty.RunOrder``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "action_type_id": action_type_id,
                "name": name,
            }
            if configuration is not None:
                self._values["configuration"] = configuration
            if input_artifacts is not None:
                self._values["input_artifacts"] = input_artifacts
            if namespace is not None:
                self._values["namespace"] = namespace
            if output_artifacts is not None:
                self._values["output_artifacts"] = output_artifacts
            if region is not None:
                self._values["region"] = region
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if run_order is not None:
                self._values["run_order"] = run_order

        @builtins.property
        def action_type_id(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionTypeIdProperty"]:
            """``CfnPipeline.ActionDeclarationProperty.ActionTypeId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid
            """
            result = self._values.get("action_type_id")
            assert result is not None, "Required property 'action_type_id' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnPipeline.ActionDeclarationProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def configuration(self) -> typing.Any:
            """``CfnPipeline.ActionDeclarationProperty.Configuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-configuration
            """
            result = self._values.get("configuration")
            return result

        @builtins.property
        def input_artifacts(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.InputArtifactProperty"]]]]:
            """``CfnPipeline.ActionDeclarationProperty.InputArtifacts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-inputartifacts
            """
            result = self._values.get("input_artifacts")
            return result

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            """``CfnPipeline.ActionDeclarationProperty.Namespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-actiondeclaration-namespace
            """
            result = self._values.get("namespace")
            return result

        @builtins.property
        def output_artifacts(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.OutputArtifactProperty"]]]]:
            """``CfnPipeline.ActionDeclarationProperty.OutputArtifacts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-outputartifacts
            """
            result = self._values.get("output_artifacts")
            return result

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            """``CfnPipeline.ActionDeclarationProperty.Region``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-region
            """
            result = self._values.get("region")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnPipeline.ActionDeclarationProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def run_order(self) -> typing.Optional[jsii.Number]:
            """``CfnPipeline.ActionDeclarationProperty.RunOrder``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-runorder
            """
            result = self._values.get("run_order")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ActionTypeIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "category": "category",
            "owner": "owner",
            "provider": "provider",
            "version": "version",
        },
    )
    class ActionTypeIdProperty:
        def __init__(
            self,
            *,
            category: builtins.str,
            owner: builtins.str,
            provider: builtins.str,
            version: builtins.str,
        ) -> None:
            """
            :param category: ``CfnPipeline.ActionTypeIdProperty.Category``.
            :param owner: ``CfnPipeline.ActionTypeIdProperty.Owner``.
            :param provider: ``CfnPipeline.ActionTypeIdProperty.Provider``.
            :param version: ``CfnPipeline.ActionTypeIdProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "category": category,
                "owner": owner,
                "provider": provider,
                "version": version,
            }

        @builtins.property
        def category(self) -> builtins.str:
            """``CfnPipeline.ActionTypeIdProperty.Category``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-category
            """
            result = self._values.get("category")
            assert result is not None, "Required property 'category' is missing"
            return result

        @builtins.property
        def owner(self) -> builtins.str:
            """``CfnPipeline.ActionTypeIdProperty.Owner``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-owner
            """
            result = self._values.get("owner")
            assert result is not None, "Required property 'owner' is missing"
            return result

        @builtins.property
        def provider(self) -> builtins.str:
            """``CfnPipeline.ActionTypeIdProperty.Provider``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-provider
            """
            result = self._values.get("provider")
            assert result is not None, "Required property 'provider' is missing"
            return result

        @builtins.property
        def version(self) -> builtins.str:
            """``CfnPipeline.ActionTypeIdProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-version
            """
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionTypeIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ArtifactStoreMapProperty",
        jsii_struct_bases=[],
        name_mapping={"artifact_store": "artifactStore", "region": "region"},
    )
    class ArtifactStoreMapProperty:
        def __init__(
            self,
            *,
            artifact_store: typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreProperty"],
            region: builtins.str,
        ) -> None:
            """
            :param artifact_store: ``CfnPipeline.ArtifactStoreMapProperty.ArtifactStore``.
            :param region: ``CfnPipeline.ArtifactStoreMapProperty.Region``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "artifact_store": artifact_store,
                "region": region,
            }

        @builtins.property
        def artifact_store(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreProperty"]:
            """``CfnPipeline.ArtifactStoreMapProperty.ArtifactStore``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html#cfn-codepipeline-pipeline-artifactstoremap-artifactstore
            """
            result = self._values.get("artifact_store")
            assert result is not None, "Required property 'artifact_store' is missing"
            return result

        @builtins.property
        def region(self) -> builtins.str:
            """``CfnPipeline.ArtifactStoreMapProperty.Region``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html#cfn-codepipeline-pipeline-artifactstoremap-region
            """
            result = self._values.get("region")
            assert result is not None, "Required property 'region' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactStoreMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ArtifactStoreProperty",
        jsii_struct_bases=[],
        name_mapping={
            "location": "location",
            "type": "type",
            "encryption_key": "encryptionKey",
        },
    )
    class ArtifactStoreProperty:
        def __init__(
            self,
            *,
            location: builtins.str,
            type: builtins.str,
            encryption_key: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.EncryptionKeyProperty"]] = None,
        ) -> None:
            """
            :param location: ``CfnPipeline.ArtifactStoreProperty.Location``.
            :param type: ``CfnPipeline.ArtifactStoreProperty.Type``.
            :param encryption_key: ``CfnPipeline.ArtifactStoreProperty.EncryptionKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "location": location,
                "type": type,
            }
            if encryption_key is not None:
                self._values["encryption_key"] = encryption_key

        @builtins.property
        def location(self) -> builtins.str:
            """``CfnPipeline.ArtifactStoreProperty.Location``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-location
            """
            result = self._values.get("location")
            assert result is not None, "Required property 'location' is missing"
            return result

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnPipeline.ArtifactStoreProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def encryption_key(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.EncryptionKeyProperty"]]:
            """``CfnPipeline.ArtifactStoreProperty.EncryptionKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-encryptionkey
            """
            result = self._values.get("encryption_key")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactStoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.BlockerDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type"},
    )
    class BlockerDeclarationProperty:
        def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
            """
            :param name: ``CfnPipeline.BlockerDeclarationProperty.Name``.
            :param type: ``CfnPipeline.BlockerDeclarationProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-blockers.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "type": type,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnPipeline.BlockerDeclarationProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-blockers.html#cfn-codepipeline-pipeline-stages-blockers-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnPipeline.BlockerDeclarationProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-blockers.html#cfn-codepipeline-pipeline-stages-blockers-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockerDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.EncryptionKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "type": "type"},
    )
    class EncryptionKeyProperty:
        def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
            """
            :param id: ``CfnPipeline.EncryptionKeyProperty.Id``.
            :param type: ``CfnPipeline.EncryptionKeyProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore-encryptionkey.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
                "type": type,
            }

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnPipeline.EncryptionKeyProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore-encryptionkey.html#cfn-codepipeline-pipeline-artifactstore-encryptionkey-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnPipeline.EncryptionKeyProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore-encryptionkey.html#cfn-codepipeline-pipeline-artifactstore-encryptionkey-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.InputArtifactProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class InputArtifactProperty:
        def __init__(self, *, name: builtins.str) -> None:
            """
            :param name: ``CfnPipeline.InputArtifactProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-inputartifacts.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnPipeline.InputArtifactProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-inputartifacts.html#cfn-codepipeline-pipeline-stages-actions-inputartifacts-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputArtifactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.OutputArtifactProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class OutputArtifactProperty:
        def __init__(self, *, name: builtins.str) -> None:
            """
            :param name: ``CfnPipeline.OutputArtifactProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-outputartifacts.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnPipeline.OutputArtifactProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-outputartifacts.html#cfn-codepipeline-pipeline-stages-actions-outputartifacts-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputArtifactProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.StageDeclarationProperty",
        jsii_struct_bases=[],
        name_mapping={"actions": "actions", "name": "name", "blockers": "blockers"},
    )
    class StageDeclarationProperty:
        def __init__(
            self,
            *,
            actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionDeclarationProperty"]]],
            name: builtins.str,
            blockers: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.BlockerDeclarationProperty"]]]] = None,
        ) -> None:
            """
            :param actions: ``CfnPipeline.StageDeclarationProperty.Actions``.
            :param name: ``CfnPipeline.StageDeclarationProperty.Name``.
            :param blockers: ``CfnPipeline.StageDeclarationProperty.Blockers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "actions": actions,
                "name": name,
            }
            if blockers is not None:
                self._values["blockers"] = blockers

        @builtins.property
        def actions(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionDeclarationProperty"]]]:
            """``CfnPipeline.StageDeclarationProperty.Actions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html#cfn-codepipeline-pipeline-stages-actions
            """
            result = self._values.get("actions")
            assert result is not None, "Required property 'actions' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnPipeline.StageDeclarationProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html#cfn-codepipeline-pipeline-stages-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def blockers(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.BlockerDeclarationProperty"]]]]:
            """``CfnPipeline.StageDeclarationProperty.Blockers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html#cfn-codepipeline-pipeline-stages-blockers
            """
            result = self._values.get("blockers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageDeclarationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.StageTransitionProperty",
        jsii_struct_bases=[],
        name_mapping={"reason": "reason", "stage_name": "stageName"},
    )
    class StageTransitionProperty:
        def __init__(self, *, reason: builtins.str, stage_name: builtins.str) -> None:
            """
            :param reason: ``CfnPipeline.StageTransitionProperty.Reason``.
            :param stage_name: ``CfnPipeline.StageTransitionProperty.StageName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-disableinboundstagetransitions.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "reason": reason,
                "stage_name": stage_name,
            }

        @builtins.property
        def reason(self) -> builtins.str:
            """``CfnPipeline.StageTransitionProperty.Reason``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-disableinboundstagetransitions.html#cfn-codepipeline-pipeline-disableinboundstagetransitions-reason
            """
            result = self._values.get("reason")
            assert result is not None, "Required property 'reason' is missing"
            return result

        @builtins.property
        def stage_name(self) -> builtins.str:
            """``CfnPipeline.StageTransitionProperty.StageName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-disableinboundstagetransitions.html#cfn-codepipeline-pipeline-disableinboundstagetransitions-stagename
            """
            result = self._values.get("stage_name")
            assert result is not None, "Required property 'stage_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageTransitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.CfnPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "stages": "stages",
        "artifact_store": "artifactStore",
        "artifact_stores": "artifactStores",
        "disable_inbound_stage_transitions": "disableInboundStageTransitions",
        "name": "name",
        "restart_execution_on_update": "restartExecutionOnUpdate",
        "tags": "tags",
    },
)
class CfnPipelineProps:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        stages: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.StageDeclarationProperty]]],
        artifact_store: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.ArtifactStoreProperty]] = None,
        artifact_stores: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.ArtifactStoreMapProperty]]]] = None,
        disable_inbound_stage_transitions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.StageTransitionProperty]]]] = None,
        name: typing.Optional[builtins.str] = None,
        restart_execution_on_update: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodePipeline::Pipeline``.

        :param role_arn: ``AWS::CodePipeline::Pipeline.RoleArn``.
        :param stages: ``AWS::CodePipeline::Pipeline.Stages``.
        :param artifact_store: ``AWS::CodePipeline::Pipeline.ArtifactStore``.
        :param artifact_stores: ``AWS::CodePipeline::Pipeline.ArtifactStores``.
        :param disable_inbound_stage_transitions: ``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.
        :param name: ``AWS::CodePipeline::Pipeline.Name``.
        :param restart_execution_on_update: ``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.
        :param tags: ``AWS::CodePipeline::Pipeline.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "role_arn": role_arn,
            "stages": stages,
        }
        if artifact_store is not None:
            self._values["artifact_store"] = artifact_store
        if artifact_stores is not None:
            self._values["artifact_stores"] = artifact_stores
        if disable_inbound_stage_transitions is not None:
            self._values["disable_inbound_stage_transitions"] = disable_inbound_stage_transitions
        if name is not None:
            self._values["name"] = name
        if restart_execution_on_update is not None:
            self._values["restart_execution_on_update"] = restart_execution_on_update
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def role_arn(self) -> builtins.str:
        """``AWS::CodePipeline::Pipeline.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-rolearn
        """
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return result

    @builtins.property
    def stages(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.StageDeclarationProperty]]]:
        """``AWS::CodePipeline::Pipeline.Stages``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-stages
        """
        result = self._values.get("stages")
        assert result is not None, "Required property 'stages' is missing"
        return result

    @builtins.property
    def artifact_store(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.ArtifactStoreProperty]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStore``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstore
        """
        result = self._values.get("artifact_store")
        return result

    @builtins.property
    def artifact_stores(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.ArtifactStoreMapProperty]]]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStores``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstores
        """
        result = self._values.get("artifact_stores")
        return result

    @builtins.property
    def disable_inbound_stage_transitions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnPipeline.StageTransitionProperty]]]]:
        """``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-disableinboundstagetransitions
        """
        result = self._values.get("disable_inbound_stage_transitions")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodePipeline::Pipeline.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def restart_execution_on_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-restartexecutiononupdate
        """
        result = self._values.get("restart_execution_on_update")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodePipeline::Pipeline.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWebhook(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook",
):
    """A CloudFormation ``AWS::CodePipeline::Webhook``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html
    :cloudformationResource: AWS::CodePipeline::Webhook
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        authentication: builtins.str,
        authentication_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookAuthConfigurationProperty"],
        filters: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookFilterRuleProperty"]]],
        target_action: builtins.str,
        target_pipeline: builtins.str,
        target_pipeline_version: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        register_with_third_party: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Create a new ``AWS::CodePipeline::Webhook``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authentication: ``AWS::CodePipeline::Webhook.Authentication``.
        :param authentication_configuration: ``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.
        :param filters: ``AWS::CodePipeline::Webhook.Filters``.
        :param target_action: ``AWS::CodePipeline::Webhook.TargetAction``.
        :param target_pipeline: ``AWS::CodePipeline::Webhook.TargetPipeline``.
        :param target_pipeline_version: ``AWS::CodePipeline::Webhook.TargetPipelineVersion``.
        :param name: ``AWS::CodePipeline::Webhook.Name``.
        :param register_with_third_party: ``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.
        """
        props = CfnWebhookProps(
            authentication=authentication,
            authentication_configuration=authentication_configuration,
            filters=filters,
            target_action=target_action,
            target_pipeline=target_pipeline,
            target_pipeline_version=target_pipeline_version,
            name=name,
            register_with_third_party=register_with_third_party,
        )

        jsii.create(CfnWebhook, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrUrl")
    def attr_url(self) -> builtins.str:
        """
        :cloudformationAttribute: Url
        """
        return jsii.get(self, "attrUrl")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> builtins.str:
        """``AWS::CodePipeline::Webhook.Authentication``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authentication
        """
        return jsii.get(self, "authentication")

    @authentication.setter # type: ignore
    def authentication(self, value: builtins.str) -> None:
        jsii.set(self, "authentication", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authenticationConfiguration")
    def authentication_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookAuthConfigurationProperty"]:
        """``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authenticationconfiguration
        """
        return jsii.get(self, "authenticationConfiguration")

    @authentication_configuration.setter # type: ignore
    def authentication_configuration(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookAuthConfigurationProperty"],
    ) -> None:
        jsii.set(self, "authenticationConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="filters")
    def filters(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookFilterRuleProperty"]]]:
        """``AWS::CodePipeline::Webhook.Filters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-filters
        """
        return jsii.get(self, "filters")

    @filters.setter # type: ignore
    def filters(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookFilterRuleProperty"]]],
    ) -> None:
        jsii.set(self, "filters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetAction")
    def target_action(self) -> builtins.str:
        """``AWS::CodePipeline::Webhook.TargetAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetaction
        """
        return jsii.get(self, "targetAction")

    @target_action.setter # type: ignore
    def target_action(self, value: builtins.str) -> None:
        jsii.set(self, "targetAction", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetPipeline")
    def target_pipeline(self) -> builtins.str:
        """``AWS::CodePipeline::Webhook.TargetPipeline``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipeline
        """
        return jsii.get(self, "targetPipeline")

    @target_pipeline.setter # type: ignore
    def target_pipeline(self, value: builtins.str) -> None:
        jsii.set(self, "targetPipeline", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetPipelineVersion")
    def target_pipeline_version(self) -> jsii.Number:
        """``AWS::CodePipeline::Webhook.TargetPipelineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipelineversion
        """
        return jsii.get(self, "targetPipelineVersion")

    @target_pipeline_version.setter # type: ignore
    def target_pipeline_version(self, value: jsii.Number) -> None:
        jsii.set(self, "targetPipelineVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodePipeline::Webhook.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="registerWithThirdParty")
    def register_with_third_party(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-registerwiththirdparty
        """
        return jsii.get(self, "registerWithThirdParty")

    @register_with_third_party.setter # type: ignore
    def register_with_third_party(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "registerWithThirdParty", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook.WebhookAuthConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_ip_range": "allowedIpRange",
            "secret_token": "secretToken",
        },
    )
    class WebhookAuthConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_ip_range: typing.Optional[builtins.str] = None,
            secret_token: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param allowed_ip_range: ``CfnWebhook.WebhookAuthConfigurationProperty.AllowedIPRange``.
            :param secret_token: ``CfnWebhook.WebhookAuthConfigurationProperty.SecretToken``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if allowed_ip_range is not None:
                self._values["allowed_ip_range"] = allowed_ip_range
            if secret_token is not None:
                self._values["secret_token"] = secret_token

        @builtins.property
        def allowed_ip_range(self) -> typing.Optional[builtins.str]:
            """``CfnWebhook.WebhookAuthConfigurationProperty.AllowedIPRange``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html#cfn-codepipeline-webhook-webhookauthconfiguration-allowediprange
            """
            result = self._values.get("allowed_ip_range")
            return result

        @builtins.property
        def secret_token(self) -> typing.Optional[builtins.str]:
            """``CfnWebhook.WebhookAuthConfigurationProperty.SecretToken``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html#cfn-codepipeline-webhook-webhookauthconfiguration-secrettoken
            """
            result = self._values.get("secret_token")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebhookAuthConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook.WebhookFilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"json_path": "jsonPath", "match_equals": "matchEquals"},
    )
    class WebhookFilterRuleProperty:
        def __init__(
            self,
            *,
            json_path: builtins.str,
            match_equals: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param json_path: ``CfnWebhook.WebhookFilterRuleProperty.JsonPath``.
            :param match_equals: ``CfnWebhook.WebhookFilterRuleProperty.MatchEquals``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "json_path": json_path,
            }
            if match_equals is not None:
                self._values["match_equals"] = match_equals

        @builtins.property
        def json_path(self) -> builtins.str:
            """``CfnWebhook.WebhookFilterRuleProperty.JsonPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html#cfn-codepipeline-webhook-webhookfilterrule-jsonpath
            """
            result = self._values.get("json_path")
            assert result is not None, "Required property 'json_path' is missing"
            return result

        @builtins.property
        def match_equals(self) -> typing.Optional[builtins.str]:
            """``CfnWebhook.WebhookFilterRuleProperty.MatchEquals``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html#cfn-codepipeline-webhook-webhookfilterrule-matchequals
            """
            result = self._values.get("match_equals")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebhookFilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.CfnWebhookProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication": "authentication",
        "authentication_configuration": "authenticationConfiguration",
        "filters": "filters",
        "target_action": "targetAction",
        "target_pipeline": "targetPipeline",
        "target_pipeline_version": "targetPipelineVersion",
        "name": "name",
        "register_with_third_party": "registerWithThirdParty",
    },
)
class CfnWebhookProps:
    def __init__(
        self,
        *,
        authentication: builtins.str,
        authentication_configuration: typing.Union[aws_cdk.core.IResolvable, CfnWebhook.WebhookAuthConfigurationProperty],
        filters: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnWebhook.WebhookFilterRuleProperty]]],
        target_action: builtins.str,
        target_pipeline: builtins.str,
        target_pipeline_version: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        register_with_third_party: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodePipeline::Webhook``.

        :param authentication: ``AWS::CodePipeline::Webhook.Authentication``.
        :param authentication_configuration: ``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.
        :param filters: ``AWS::CodePipeline::Webhook.Filters``.
        :param target_action: ``AWS::CodePipeline::Webhook.TargetAction``.
        :param target_pipeline: ``AWS::CodePipeline::Webhook.TargetPipeline``.
        :param target_pipeline_version: ``AWS::CodePipeline::Webhook.TargetPipelineVersion``.
        :param name: ``AWS::CodePipeline::Webhook.Name``.
        :param register_with_third_party: ``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "authentication": authentication,
            "authentication_configuration": authentication_configuration,
            "filters": filters,
            "target_action": target_action,
            "target_pipeline": target_pipeline,
            "target_pipeline_version": target_pipeline_version,
        }
        if name is not None:
            self._values["name"] = name
        if register_with_third_party is not None:
            self._values["register_with_third_party"] = register_with_third_party

    @builtins.property
    def authentication(self) -> builtins.str:
        """``AWS::CodePipeline::Webhook.Authentication``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authentication
        """
        result = self._values.get("authentication")
        assert result is not None, "Required property 'authentication' is missing"
        return result

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnWebhook.WebhookAuthConfigurationProperty]:
        """``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authenticationconfiguration
        """
        result = self._values.get("authentication_configuration")
        assert result is not None, "Required property 'authentication_configuration' is missing"
        return result

    @builtins.property
    def filters(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnWebhook.WebhookFilterRuleProperty]]]:
        """``AWS::CodePipeline::Webhook.Filters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-filters
        """
        result = self._values.get("filters")
        assert result is not None, "Required property 'filters' is missing"
        return result

    @builtins.property
    def target_action(self) -> builtins.str:
        """``AWS::CodePipeline::Webhook.TargetAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetaction
        """
        result = self._values.get("target_action")
        assert result is not None, "Required property 'target_action' is missing"
        return result

    @builtins.property
    def target_pipeline(self) -> builtins.str:
        """``AWS::CodePipeline::Webhook.TargetPipeline``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipeline
        """
        result = self._values.get("target_pipeline")
        assert result is not None, "Required property 'target_pipeline' is missing"
        return result

    @builtins.property
    def target_pipeline_version(self) -> jsii.Number:
        """``AWS::CodePipeline::Webhook.TargetPipelineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipelineversion
        """
        result = self._values.get("target_pipeline_version")
        assert result is not None, "Required property 'target_pipeline_version' is missing"
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodePipeline::Webhook.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def register_with_third_party(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-registerwiththirdparty
        """
        result = self._values.get("register_with_third_party")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebhookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.CommonActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
    },
)
class CommonActionProps:
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        """Common properties shared by all Actions.

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace

    @builtins.property
    def action_name(self) -> builtins.str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.
        """
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return result

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        result = self._values.get("run_order")
        return result

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        """The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set
        """
        result = self._values.get("variables_namespace")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.CommonAwsActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
    },
)
class CommonAwsActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """Common properties shared by all Actions whose {@link ActionProperties.owner} field is 'AWS' (or unset, as 'AWS' is the default).

        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def action_name(self) -> builtins.str:
        """The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.
        """
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return result

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        result = self._values.get("run_order")
        return result

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        """The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set
        """
        result = self._values.get("variables_namespace")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated
        """
        result = self._values.get("role")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonAwsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.CrossRegionSupport",
    jsii_struct_bases=[],
    name_mapping={"replication_bucket": "replicationBucket", "stack": "stack"},
)
class CrossRegionSupport:
    def __init__(
        self,
        *,
        replication_bucket: aws_cdk.aws_s3.IBucket,
        stack: aws_cdk.core.Stack,
    ) -> None:
        """(experimental) An interface representing resources generated in order to support the cross-region capabilities of CodePipeline.

        You get instances of this interface from the {@link Pipeline#crossRegionSupport} property.

        :param replication_bucket: (experimental) The replication Bucket used by CodePipeline to operate in this region. Belongs to {@link stack}.
        :param stack: (experimental) The Stack that has been created to house the replication Bucket required for this region.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "replication_bucket": replication_bucket,
            "stack": stack,
        }

    @builtins.property
    def replication_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """(experimental) The replication Bucket used by CodePipeline to operate in this region.

        Belongs to {@link stack}.

        :stability: experimental
        """
        result = self._values.get("replication_bucket")
        assert result is not None, "Required property 'replication_bucket' is missing"
        return result

    @builtins.property
    def stack(self) -> aws_cdk.core.Stack:
        """(experimental) The Stack that has been created to house the replication Bucket required for this  region.

        :stability: experimental
        """
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossRegionSupport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlobalVariables(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codepipeline.GlobalVariables",
):
    """The CodePipeline variables that are global, not bound to a specific action.

    This class defines a bunch of static fields that represent the different variables.
    These can be used can be used in any action configuration.
    """

    def __init__(self) -> None:
        jsii.create(GlobalVariables, self, [])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="executionId")
    def EXECUTION_ID(cls) -> builtins.str:
        """The identifier of the current pipeline execution."""
        return jsii.sget(cls, "executionId")


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IAction")
class IAction(typing_extensions.Protocol):
    """A Pipeline Action."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IActionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> ActionProperties:
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        stage: "IStage",
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        role: aws_cdk.aws_iam.IRole,
    ) -> ActionConfig:
        """
        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        ...


class _IActionProxy:
    """A Pipeline Action."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codepipeline.IAction"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> ActionProperties:
        return jsii.get(self, "actionProperties")

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        stage: "IStage",
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        role: aws_cdk.aws_iam.IRole,
    ) -> ActionConfig:
        """
        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 
        """
        options = ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        options = aws_cdk.aws_events.RuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return jsii.invoke(self, "onStateChange", [name, target, options])


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IPipeline")
class IPipeline(aws_cdk.core.IResource, typing_extensions.Protocol):
    """The abstract view of an AWS CodePipeline as required and used by Actions.

    It extends {@link events.IRuleTarget},
    so this interface can be used as a Target for CloudWatch Events.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPipelineProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> builtins.str:
        """The ARN of the Pipeline.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> builtins.str:
        """The name of the Pipeline.

        :attribute: true
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by this CodePipeline.

        :param id: Identifier for this event handler.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by the "CodePipeline Pipeline Execution State Change" event emitted from this pipeline.

        :param id: Identifier for this event handler.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...


class _IPipelineProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """The abstract view of an AWS CodePipeline as required and used by Actions.

    It extends {@link events.IRuleTarget},
    so this interface can be used as a Target for CloudWatch Events.
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codepipeline.IPipeline"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> builtins.str:
        """The ARN of the Pipeline.

        :attribute: true
        """
        return jsii.get(self, "pipelineArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> builtins.str:
        """The name of the Pipeline.

        :attribute: true
        """
        return jsii.get(self, "pipelineName")

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by this CodePipeline.

        :param id: Identifier for this event handler.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by the "CodePipeline Pipeline Execution State Change" event emitted from this pipeline.

        :param id: Identifier for this event handler.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onStateChange", [id, options])


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IStage")
class IStage(typing_extensions.Protocol):
    """The abstract interface of a Pipeline Stage that is used by Actions."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStageProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[IAction]:
        """The actions belonging to this stage."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> IPipeline:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        """The physical, human-readable name of this Pipeline Stage."""
        ...

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: IAction) -> None:
        """
        :param action: -
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        ...


class _IStageProxy:
    """The abstract interface of a Pipeline Stage that is used by Actions."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codepipeline.IStage"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[IAction]:
        """The actions belonging to this stage."""
        return jsii.get(self, "actions")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> IPipeline:
        return jsii.get(self, "pipeline")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        """The physical, human-readable name of this Pipeline Stage."""
        return jsii.get(self, "stageName")

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: IAction) -> None:
        """
        :param action: -
        """
        return jsii.invoke(self, "addAction", [action])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]] = None,
    ) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        options = aws_cdk.aws_events.RuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return jsii.invoke(self, "onStateChange", [name, target, options])


@jsii.implements(IPipeline)
class Pipeline(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codepipeline.Pipeline",
):
    """An AWS CodePipeline pipeline with its associated IAM role and S3 bucket.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # create a pipeline
        pipeline = Pipeline(self, "Pipeline")
        
        # add a stage
        source_stage = pipeline.add_stage(stage_name="Source")
        
        # add a source action to the stage
        source_stage.add_action(codepipeline_actions.CodeCommitSourceAction(
            action_name="Source",
            output_artifact_name="SourceArtifact",
            repository=repo
        ))
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        artifact_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_s3.IBucket]] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        restart_execution_on_update: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        stages: typing.Optional[typing.List["StageProps"]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param artifact_bucket: The S3 bucket used by this Pipeline to store artifacts. Default: - A new S3 bucket will be created.
        :param cross_account_keys: Create KMS keys for cross-account deployments. This controls whether the pipeline is enabled for cross-account deployments. By default cross-account deployments are enabled, but this feature requires that KMS Customer Master Keys are created which have a cost of $1/month. If you do not need cross-account deployments, you can set this to ``false`` to not create those keys and save on that cost (the artifact bucket will be encrypted with an AWS-managed key). However, cross-account deployments will no longer be possible. Default: true
        :param cross_region_replication_buckets: (experimental) A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Default: - None.
        :param pipeline_name: Name of the pipeline. Default: - AWS CloudFormation generates an ID and uses that for the pipeline name.
        :param restart_execution_on_update: Indicates whether to rerun the AWS CodePipeline pipeline after you update it. Default: false
        :param role: The IAM role to be assumed by this Pipeline. Default: a new IAM role will be created.
        :param stages: The list of Stages, in order, to create this Pipeline with. You can always add more Stages later by calling {@link Pipeline#addStage}. Default: - None.
        """
        props = PipelineProps(
            artifact_bucket=artifact_bucket,
            cross_account_keys=cross_account_keys,
            cross_region_replication_buckets=cross_region_replication_buckets,
            pipeline_name=pipeline_name,
            restart_execution_on_update=restart_execution_on_update,
            role=role,
            stages=stages,
        )

        jsii.create(Pipeline, self, [scope, id, props])

    @jsii.member(jsii_name="fromPipelineArn")
    @builtins.classmethod
    def from_pipeline_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        pipeline_arn: builtins.str,
    ) -> IPipeline:
        """Import a pipeline into this app.

        :param scope: the scope into which to import this pipeline.
        :param id: the logical ID of the returned pipeline construct.
        :param pipeline_arn: The ARN of the pipeline (e.g. ``arn:aws:codepipeline:us-east-1:123456789012:MyDemoPipeline``).
        """
        return jsii.sinvoke(cls, "fromPipelineArn", [scope, id, pipeline_arn])

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        *,
        placement: typing.Optional["StagePlacement"] = None,
        stage_name: builtins.str,
        actions: typing.Optional[typing.List[IAction]] = None,
    ) -> IStage:
        """Creates a new Stage, and adds it to this Pipeline.

        :param placement: 
        :param stage_name: The physical, human-readable name to assign to this Pipeline Stage.
        :param actions: The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}.

        :return: the newly created Stage
        """
        props = StageOptions(
            placement=placement, stage_name=stage_name, actions=actions
        )

        return jsii.invoke(self, "addStage", [props])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the pipeline role.

        :param statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule triggered by this CodePipeline.

        :param id: Identifier for this event handler.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an event rule triggered by the "CodePipeline Pipeline Execution State Change" event emitted from this pipeline.

        :param id: Identifier for this event handler.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onStateChange", [id, options])

    @jsii.member(jsii_name="stage")
    def stage(self, stage_name: builtins.str) -> IStage:
        """Access one of the pipeline's stages by stage name.

        :param stage_name: -
        """
        return jsii.invoke(self, "stage", [stage_name])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the pipeline structure.

        Validation happens according to the rules documented at

        https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#pipeline-requirements

        :override: true
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="artifactBucket")
    def artifact_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """Bucket used to store output artifacts."""
        return jsii.get(self, "artifactBucket")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="crossRegionSupport")
    def cross_region_support(self) -> typing.Mapping[builtins.str, CrossRegionSupport]:
        """(experimental) Returns all of the {@link CrossRegionSupportStack}s that were generated automatically when dealing with Actions that reside in a different region than the Pipeline itself.

        :stability: experimental
        """
        return jsii.get(self, "crossRegionSupport")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> builtins.str:
        """ARN of this pipeline."""
        return jsii.get(self, "pipelineArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> builtins.str:
        """The name of the pipeline."""
        return jsii.get(self, "pipelineName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pipelineVersion")
    def pipeline_version(self) -> builtins.str:
        """The version of the pipeline.

        :attribute: true
        """
        return jsii.get(self, "pipelineVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The IAM role AWS CodePipeline will use to perform actions or assume roles for actions with a more specific IAM role."""
        return jsii.get(self, "role")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stageCount")
    def stage_count(self) -> jsii.Number:
        """Get the number of Stages in this Pipeline."""
        return jsii.get(self, "stageCount")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List[IStage]:
        """Returns the stages that comprise the pipeline.

        **Note**: the returned array is a defensive copy,
        so adding elements to it has no effect.
        Instead, use the {@link addStage} method if you want to add more stages
        to the pipeline.
        """
        return jsii.get(self, "stages")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.PipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_bucket": "artifactBucket",
        "cross_account_keys": "crossAccountKeys",
        "cross_region_replication_buckets": "crossRegionReplicationBuckets",
        "pipeline_name": "pipelineName",
        "restart_execution_on_update": "restartExecutionOnUpdate",
        "role": "role",
        "stages": "stages",
    },
)
class PipelineProps:
    def __init__(
        self,
        *,
        artifact_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        cross_region_replication_buckets: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_s3.IBucket]] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        restart_execution_on_update: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        stages: typing.Optional[typing.List["StageProps"]] = None,
    ) -> None:
        """
        :param artifact_bucket: The S3 bucket used by this Pipeline to store artifacts. Default: - A new S3 bucket will be created.
        :param cross_account_keys: Create KMS keys for cross-account deployments. This controls whether the pipeline is enabled for cross-account deployments. By default cross-account deployments are enabled, but this feature requires that KMS Customer Master Keys are created which have a cost of $1/month. If you do not need cross-account deployments, you can set this to ``false`` to not create those keys and save on that cost (the artifact bucket will be encrypted with an AWS-managed key). However, cross-account deployments will no longer be possible. Default: true
        :param cross_region_replication_buckets: (experimental) A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Default: - None.
        :param pipeline_name: Name of the pipeline. Default: - AWS CloudFormation generates an ID and uses that for the pipeline name.
        :param restart_execution_on_update: Indicates whether to rerun the AWS CodePipeline pipeline after you update it. Default: false
        :param role: The IAM role to be assumed by this Pipeline. Default: a new IAM role will be created.
        :param stages: The list of Stages, in order, to create this Pipeline with. You can always add more Stages later by calling {@link Pipeline#addStage}. Default: - None.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if artifact_bucket is not None:
            self._values["artifact_bucket"] = artifact_bucket
        if cross_account_keys is not None:
            self._values["cross_account_keys"] = cross_account_keys
        if cross_region_replication_buckets is not None:
            self._values["cross_region_replication_buckets"] = cross_region_replication_buckets
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if restart_execution_on_update is not None:
            self._values["restart_execution_on_update"] = restart_execution_on_update
        if role is not None:
            self._values["role"] = role
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def artifact_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """The S3 bucket used by this Pipeline to store artifacts.

        :default: - A new S3 bucket will be created.
        """
        result = self._values.get("artifact_bucket")
        return result

    @builtins.property
    def cross_account_keys(self) -> typing.Optional[builtins.bool]:
        """Create KMS keys for cross-account deployments.

        This controls whether the pipeline is enabled for cross-account deployments.

        By default cross-account deployments are enabled, but this feature requires
        that KMS Customer Master Keys are created which have a cost of $1/month.

        If you do not need cross-account deployments, you can set this to ``false`` to
        not create those keys and save on that cost (the artifact bucket will be
        encrypted with an AWS-managed key). However, cross-account deployments will
        no longer be possible.

        :default: true
        """
        result = self._values.get("cross_account_keys")
        return result

    @builtins.property
    def cross_region_replication_buckets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_s3.IBucket]]:
        """(experimental) A map of region to S3 bucket name used for cross-region CodePipeline.

        For every Action that you specify targeting a different region than the Pipeline itself,
        if you don't provide an explicit Bucket for that region using this property,
        the construct will automatically create a Stack containing an S3 Bucket in that region.

        :default: - None.

        :stability: experimental
        """
        result = self._values.get("cross_region_replication_buckets")
        return result

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        """Name of the pipeline.

        :default: - AWS CloudFormation generates an ID and uses that for the pipeline name.
        """
        result = self._values.get("pipeline_name")
        return result

    @builtins.property
    def restart_execution_on_update(self) -> typing.Optional[builtins.bool]:
        """Indicates whether to rerun the AWS CodePipeline pipeline after you update it.

        :default: false
        """
        result = self._values.get("restart_execution_on_update")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role to be assumed by this Pipeline.

        :default: a new IAM role will be created.
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def stages(self) -> typing.Optional[typing.List["StageProps"]]:
        """The list of Stages, in order, to create this Pipeline with.

        You can always add more Stages later by calling {@link Pipeline#addStage}.

        :default: - None.
        """
        result = self._values.get("stages")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.StagePlacement",
    jsii_struct_bases=[],
    name_mapping={"just_after": "justAfter", "right_before": "rightBefore"},
)
class StagePlacement:
    def __init__(
        self,
        *,
        just_after: typing.Optional[IStage] = None,
        right_before: typing.Optional[IStage] = None,
    ) -> None:
        """Allows you to control where to place a new Stage when it's added to the Pipeline.

        Note that you can provide only one of the below properties -
        specifying more than one will result in a validation error.

        :param just_after: Inserts the new Stage as a child of the given Stage (changing its current child Stage, if it had one).
        :param right_before: Inserts the new Stage as a parent of the given Stage (changing its current parent Stage, if it had one).

        :see: #justAfter
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if just_after is not None:
            self._values["just_after"] = just_after
        if right_before is not None:
            self._values["right_before"] = right_before

    @builtins.property
    def just_after(self) -> typing.Optional[IStage]:
        """Inserts the new Stage as a child of the given Stage (changing its current child Stage, if it had one)."""
        result = self._values.get("just_after")
        return result

    @builtins.property
    def right_before(self) -> typing.Optional[IStage]:
        """Inserts the new Stage as a parent of the given Stage (changing its current parent Stage, if it had one)."""
        result = self._values.get("right_before")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StagePlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.StageProps",
    jsii_struct_bases=[],
    name_mapping={"stage_name": "stageName", "actions": "actions"},
)
class StageProps:
    def __init__(
        self,
        *,
        stage_name: builtins.str,
        actions: typing.Optional[typing.List[IAction]] = None,
    ) -> None:
        """Construction properties of a Pipeline Stage.

        :param stage_name: The physical, human-readable name to assign to this Pipeline Stage.
        :param actions: The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "stage_name": stage_name,
        }
        if actions is not None:
            self._values["actions"] = actions

    @builtins.property
    def stage_name(self) -> builtins.str:
        """The physical, human-readable name to assign to this Pipeline Stage."""
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return result

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[IAction]]:
        """The list of Actions to create this Stage with.

        You can always add more Actions later by calling {@link IStage#addAction}.
        """
        result = self._values.get("actions")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codepipeline.StageOptions",
    jsii_struct_bases=[StageProps],
    name_mapping={
        "stage_name": "stageName",
        "actions": "actions",
        "placement": "placement",
    },
)
class StageOptions(StageProps):
    def __init__(
        self,
        *,
        stage_name: builtins.str,
        actions: typing.Optional[typing.List[IAction]] = None,
        placement: typing.Optional[StagePlacement] = None,
    ) -> None:
        """
        :param stage_name: The physical, human-readable name to assign to this Pipeline Stage.
        :param actions: The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}.
        :param placement: 
        """
        if isinstance(placement, dict):
            placement = StagePlacement(**placement)
        self._values: typing.Dict[str, typing.Any] = {
            "stage_name": stage_name,
        }
        if actions is not None:
            self._values["actions"] = actions
        if placement is not None:
            self._values["placement"] = placement

    @builtins.property
    def stage_name(self) -> builtins.str:
        """The physical, human-readable name to assign to this Pipeline Stage."""
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return result

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[IAction]]:
        """The list of Actions to create this Stage with.

        You can always add more Actions later by calling {@link IStage#addAction}.
        """
        result = self._values.get("actions")
        return result

    @builtins.property
    def placement(self) -> typing.Optional[StagePlacement]:
        result = self._values.get("placement")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ActionArtifactBounds",
    "ActionBindOptions",
    "ActionCategory",
    "ActionConfig",
    "ActionProperties",
    "Artifact",
    "ArtifactPath",
    "CfnCustomActionType",
    "CfnCustomActionTypeProps",
    "CfnPipeline",
    "CfnPipelineProps",
    "CfnWebhook",
    "CfnWebhookProps",
    "CommonActionProps",
    "CommonAwsActionProps",
    "CrossRegionSupport",
    "GlobalVariables",
    "IAction",
    "IPipeline",
    "IStage",
    "Pipeline",
    "PipelineProps",
    "StageOptions",
    "StagePlacement",
    "StageProps",
]

publication.publish()
