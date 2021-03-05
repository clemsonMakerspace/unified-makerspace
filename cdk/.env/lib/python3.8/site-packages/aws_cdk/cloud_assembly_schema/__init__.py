"""
## Cloud Assembly Schema

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Cloud Assembly

The *Cloud Assembly* is the output of the synthesis operation. It is produced as part of the
[`cdk synth`](https://github.com/aws/aws-cdk/tree/master/packages/aws-cdk#cdk-synthesize)
command, or the [`app.synth()`](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/core/lib/app.ts#L135) method invocation.

Its essentially a set of files and directories, one of which is the `manifest.json` file. It defines the set of instructions that are
needed in order to deploy the assembly directory.

> For example, when `cdk deploy` is executed, the CLI reads this file and performs its instructions:
>
> * Build container images.
> * Upload assets.
> * Deploy CloudFormation templates.

Therefore, the assembly is how the CDK class library and CDK CLI (or any other consumer) communicate. To ensure compatibility
between the assembly and its consumers, we treat the manifest file as a well defined, versioned schema.

## Schema

This module contains the typescript structs that comprise the `manifest.json` file, as well as the
generated [*json-schema*](./schema/cloud-assembly.schema.json).

## Versioning

The schema version is specified in the [`cloud-assembly.version.json`](./schema/cloud-assembly.schema.json) file, under the `version` property.
It follows semantic versioning, but with a small twist.

When we add instructions to the assembly, they are reflected in the manifest file and the *json-schema* accordingly.
Every such instruction, is crucial for ensuring the correct deployment behavior. This means that to properly deploy a cloud assembly,
consumers must be aware of every such instruction modification.

For this reason, every change to the schema, even though it might not strictly break validation of the *json-schema* format,
is considered `major` version bump.

## How to consume

If you'd like to consume the [schema file](./schema/cloud-assembly.schema.json) in order to do validations on `manifest.json` files,
simply download it from this repo and run it against standard *json-schema* validators, such as [jsonschema](https://www.npmjs.com/package/jsonschema).

Consumers must take into account the `major` version of the schema they are consuming. They should reject cloud assemblies
with a `major` version that is higher than what they expect. While schema validation might pass on such assemblies, the deployment integrity
cannot be guaranteed because some instructions will be ignored.

> For example, if your consumer was built when the schema version was 2.0.0, you should reject deploying cloud assemblies with a
> manifest version of 3.0.0.

## Contributing

See [Contribution Guide](./CONTRIBUTING.md)
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


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.AmiContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "filters": "filters",
        "region": "region",
        "owners": "owners",
    },
)
class AmiContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        filters: typing.Mapping[builtins.str, typing.List[builtins.str]],
        region: builtins.str,
        owners: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Query to AMI context provider.

        :param account: Account to query.
        :param filters: Filters to DescribeImages call.
        :param region: Region to query.
        :param owners: Owners to DescribeImages call. Default: - All owners
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "filters": filters,
            "region": region,
        }
        if owners is not None:
            self._values["owners"] = owners

    @builtins.property
    def account(self) -> builtins.str:
        """Account to query."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def filters(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        """Filters to DescribeImages call."""
        result = self._values.get("filters")
        assert result is not None, "Required property 'filters' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Region to query."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[builtins.str]]:
        """Owners to DescribeImages call.

        :default: - All owners
        """
        result = self._values.get("owners")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.ArtifactManifest",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "dependencies": "dependencies",
        "environment": "environment",
        "metadata": "metadata",
        "properties": "properties",
    },
)
class ArtifactManifest:
    def __init__(
        self,
        *,
        type: "ArtifactType",
        dependencies: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.List["MetadataEntry"]]] = None,
        properties: typing.Optional[typing.Union["AwsCloudFormationStackProperties", "AssetManifestProperties", "TreeArtifactProperties", "NestedCloudAssemblyProperties"]] = None,
    ) -> None:
        """A manifest for a single artifact within the cloud assembly.

        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param environment: The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: Associated metadata. Default: - no metadata.
        :param properties: The set of properties for this artifact (depends on type). Default: - no properties.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if environment is not None:
            self._values["environment"] = environment
        if metadata is not None:
            self._values["metadata"] = metadata
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def type(self) -> "ArtifactType":
        """The type of artifact."""
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        """IDs of artifacts that must be deployed before this artifact.

        :default: - no dependencies.
        """
        result = self._values.get("dependencies")
        return result

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        """The environment into which this artifact is deployed.

        :default: - no envrionment.
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List["MetadataEntry"]]]:
        """Associated metadata.

        :default: - no metadata.
        """
        result = self._values.get("metadata")
        return result

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union["AwsCloudFormationStackProperties", "AssetManifestProperties", "TreeArtifactProperties", "NestedCloudAssemblyProperties"]]:
        """The set of properties for this artifact (depends on type).

        :default: - no properties.
        """
        result = self._values.get("properties")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/cloud-assembly-schema.ArtifactMetadataEntryType")
class ArtifactMetadataEntryType(enum.Enum):
    """Type of artifact metadata entry."""

    ASSET = "ASSET"
    """Asset in metadata."""
    INFO = "INFO"
    """Metadata key used to print INFO-level messages by the toolkit when an app is syntheized."""
    WARN = "WARN"
    """Metadata key used to print WARNING-level messages by the toolkit when an app is syntheized."""
    ERROR = "ERROR"
    """Metadata key used to print ERROR-level messages by the toolkit when an app is syntheized."""
    LOGICAL_ID = "LOGICAL_ID"
    """Represents the CloudFormation logical ID of a resource at a certain path."""
    STACK_TAGS = "STACK_TAGS"
    """Represents tags of a stack."""


@jsii.enum(jsii_type="@aws-cdk/cloud-assembly-schema.ArtifactType")
class ArtifactType(enum.Enum):
    """Type of cloud artifact."""

    NONE = "NONE"
    """Stub required because of JSII."""
    AWS_CLOUDFORMATION_STACK = "AWS_CLOUDFORMATION_STACK"
    """The artifact is an AWS CloudFormation stack."""
    CDK_TREE = "CDK_TREE"
    """The artifact contains the CDK application's construct tree."""
    ASSET_MANIFEST = "ASSET_MANIFEST"
    """Manifest for all assets in the Cloud Assembly."""
    NESTED_CLOUD_ASSEMBLY = "NESTED_CLOUD_ASSEMBLY"
    """Nested Cloud Assembly."""


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.AssemblyManifest",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "artifacts": "artifacts",
        "missing": "missing",
        "runtime": "runtime",
    },
)
class AssemblyManifest:
    def __init__(
        self,
        *,
        version: builtins.str,
        artifacts: typing.Optional[typing.Mapping[builtins.str, ArtifactManifest]] = None,
        missing: typing.Optional[typing.List["MissingContext"]] = None,
        runtime: typing.Optional["RuntimeInfo"] = None,
    ) -> None:
        """A manifest which describes the cloud assembly.

        :param version: Protocol version.
        :param artifacts: The set of artifacts in this assembly. Default: - no artifacts.
        :param missing: Missing context information. If this field has values, it means that the cloud assembly is not complete and should not be deployed. Default: - no missing context.
        :param runtime: Runtime information. Default: - no info.
        """
        if isinstance(runtime, dict):
            runtime = RuntimeInfo(**runtime)
        self._values: typing.Dict[str, typing.Any] = {
            "version": version,
        }
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if missing is not None:
            self._values["missing"] = missing
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def version(self) -> builtins.str:
        """Protocol version."""
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    @builtins.property
    def artifacts(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ArtifactManifest]]:
        """The set of artifacts in this assembly.

        :default: - no artifacts.
        """
        result = self._values.get("artifacts")
        return result

    @builtins.property
    def missing(self) -> typing.Optional[typing.List["MissingContext"]]:
        """Missing context information.

        If this field has values, it means that the
        cloud assembly is not complete and should not be deployed.

        :default: - no missing context.
        """
        result = self._values.get("missing")
        return result

    @builtins.property
    def runtime(self) -> typing.Optional["RuntimeInfo"]:
        """Runtime information.

        :default: - no info.
        """
        result = self._values.get("runtime")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssemblyManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.AssetManifest",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "docker_images": "dockerImages",
        "files": "files",
    },
)
class AssetManifest:
    def __init__(
        self,
        *,
        version: builtins.str,
        docker_images: typing.Optional[typing.Mapping[builtins.str, "DockerImageAsset"]] = None,
        files: typing.Optional[typing.Mapping[builtins.str, "FileAsset"]] = None,
    ) -> None:
        """Definitions for the asset manifest.

        :param version: Version of the manifest.
        :param docker_images: The Docker image assets in this manifest. Default: - No Docker images
        :param files: The file assets in this manifest. Default: - No files
        """
        self._values: typing.Dict[str, typing.Any] = {
            "version": version,
        }
        if docker_images is not None:
            self._values["docker_images"] = docker_images
        if files is not None:
            self._values["files"] = files

    @builtins.property
    def version(self) -> builtins.str:
        """Version of the manifest."""
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    @builtins.property
    def docker_images(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "DockerImageAsset"]]:
        """The Docker image assets in this manifest.

        :default: - No Docker images
        """
        result = self._values.get("docker_images")
        return result

    @builtins.property
    def files(self) -> typing.Optional[typing.Mapping[builtins.str, "FileAsset"]]:
        """The file assets in this manifest.

        :default: - No files
        """
        result = self._values.get("files")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.AssetManifestProperties",
    jsii_struct_bases=[],
    name_mapping={
        "file": "file",
        "requires_bootstrap_stack_version": "requiresBootstrapStackVersion",
    },
)
class AssetManifestProperties:
    def __init__(
        self,
        *,
        file: builtins.str,
        requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Artifact properties for the Asset Manifest.

        :param file: Filename of the asset manifest.
        :param requires_bootstrap_stack_version: Version of bootstrap stack required to deploy this stack. Default: - Version 1 (basic modern bootstrap stack)
        """
        self._values: typing.Dict[str, typing.Any] = {
            "file": file,
        }
        if requires_bootstrap_stack_version is not None:
            self._values["requires_bootstrap_stack_version"] = requires_bootstrap_stack_version

    @builtins.property
    def file(self) -> builtins.str:
        """Filename of the asset manifest."""
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return result

    @builtins.property
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        """Version of bootstrap stack required to deploy this stack.

        :default: - Version 1 (basic modern bootstrap stack)
        """
        result = self._values.get("requires_bootstrap_stack_version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetManifestProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.AvailabilityZonesContextQuery",
    jsii_struct_bases=[],
    name_mapping={"account": "account", "region": "region"},
)
class AvailabilityZonesContextQuery:
    def __init__(self, *, account: builtins.str, region: builtins.str) -> None:
        """Query to availability zone context provider.

        :param account: Query account.
        :param region: Query region.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "region": region,
        }

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AvailabilityZonesContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.AwsCloudFormationStackProperties",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "assume_role_arn": "assumeRoleArn",
        "cloud_formation_execution_role_arn": "cloudFormationExecutionRoleArn",
        "parameters": "parameters",
        "requires_bootstrap_stack_version": "requiresBootstrapStackVersion",
        "stack_name": "stackName",
        "stack_template_asset_object_url": "stackTemplateAssetObjectUrl",
        "tags": "tags",
        "termination_protection": "terminationProtection",
    },
)
class AwsCloudFormationStackProperties:
    def __init__(
        self,
        *,
        template_file: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
        cloud_formation_execution_role_arn: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stack_template_asset_object_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Artifact properties for CloudFormation stacks.

        :param template_file: A file relative to the assembly root which contains the CloudFormation template for this stack.
        :param assume_role_arn: The role that needs to be assumed to deploy the stack. Default: - No role is assumed (current credentials are used)
        :param cloud_formation_execution_role_arn: The role that is passed to CloudFormation to execute the change set. Default: - No role is passed (currently assumed role/credentials are used)
        :param parameters: Values for CloudFormation stack parameters that should be passed when the stack is deployed. Default: - No parameters
        :param requires_bootstrap_stack_version: Version of bootstrap stack required to deploy this stack. Default: - No bootstrap stack required
        :param stack_name: The name to use for the CloudFormation stack. Default: - name derived from artifact ID
        :param stack_template_asset_object_url: If the stack template has already been included in the asset manifest, its asset URL. Default: - Not uploaded yet, upload just before deploying
        :param tags: Values for CloudFormation stack tags that should be passed when the stack is deployed. Default: - No tags
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        """
        self._values: typing.Dict[str, typing.Any] = {
            "template_file": template_file,
        }
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if cloud_formation_execution_role_arn is not None:
            self._values["cloud_formation_execution_role_arn"] = cloud_formation_execution_role_arn
        if parameters is not None:
            self._values["parameters"] = parameters
        if requires_bootstrap_stack_version is not None:
            self._values["requires_bootstrap_stack_version"] = requires_bootstrap_stack_version
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if stack_template_asset_object_url is not None:
            self._values["stack_template_asset_object_url"] = stack_template_asset_object_url
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection

    @builtins.property
    def template_file(self) -> builtins.str:
        """A file relative to the assembly root which contains the CloudFormation template for this stack."""
        result = self._values.get("template_file")
        assert result is not None, "Required property 'template_file' is missing"
        return result

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        """The role that needs to be assumed to deploy the stack.

        :default: - No role is assumed (current credentials are used)
        """
        result = self._values.get("assume_role_arn")
        return result

    @builtins.property
    def cloud_formation_execution_role_arn(self) -> typing.Optional[builtins.str]:
        """The role that is passed to CloudFormation to execute the change set.

        :default: - No role is passed (currently assumed role/credentials are used)
        """
        result = self._values.get("cloud_formation_execution_role_arn")
        return result

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Values for CloudFormation stack parameters that should be passed when the stack is deployed.

        :default: - No parameters
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        """Version of bootstrap stack required to deploy this stack.

        :default: - No bootstrap stack required
        """
        result = self._values.get("requires_bootstrap_stack_version")
        return result

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        """The name to use for the CloudFormation stack.

        :default: - name derived from artifact ID
        """
        result = self._values.get("stack_name")
        return result

    @builtins.property
    def stack_template_asset_object_url(self) -> typing.Optional[builtins.str]:
        """If the stack template has already been included in the asset manifest, its asset URL.

        :default: - Not uploaded yet, upload just before deploying
        """
        result = self._values.get("stack_template_asset_object_url")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Values for CloudFormation stack tags that should be passed when the stack is deployed.

        :default: - No tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        """Whether to enable termination protection for this stack.

        :default: false
        """
        result = self._values.get("termination_protection")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCloudFormationStackProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.AwsDestination",
    jsii_struct_bases=[],
    name_mapping={
        "assume_role_arn": "assumeRoleArn",
        "assume_role_external_id": "assumeRoleExternalId",
        "region": "region",
    },
)
class AwsDestination:
    def __init__(
        self,
        *,
        assume_role_arn: typing.Optional[builtins.str] = None,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """Destination for assets that need to be uploaded to AWS.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        """The role that needs to be assumed while publishing this asset.

        :default: - No role will be assumed
        """
        result = self._values.get("assume_role_arn")
        return result

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        """The ExternalId that needs to be supplied while assuming this role.

        :default: - No ExternalId will be supplied
        """
        result = self._values.get("assume_role_external_id")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region where this asset will need to be published.

        :default: - Current region
        """
        result = self._values.get("region")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.ContainerImageAssetMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "packaging": "packaging",
        "path": "path",
        "source_hash": "sourceHash",
        "build_args": "buildArgs",
        "file": "file",
        "image_name_parameter": "imageNameParameter",
        "image_tag": "imageTag",
        "repository_name": "repositoryName",
        "target": "target",
    },
)
class ContainerImageAssetMetadataEntry:
    def __init__(
        self,
        *,
        id: builtins.str,
        packaging: builtins.str,
        path: builtins.str,
        source_hash: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        image_name_parameter: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        """Metadata Entry spec for container images.

        :param id: Logical identifier for the asset.
        :param packaging: Type of asset.
        :param path: Path on disk to the asset.
        :param source_hash: The hash of the asset source.
        :param build_args: Build args to pass to the ``docker build`` command. Default: no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: - no file is passed
        :param image_name_parameter: (deprecated) ECR Repository name and repo digest (separated by "@sha256:") where this image is stored. Default: undefined If not specified, ``repositoryName`` and ``imageTag`` are required because otherwise how will the stack know where to find the asset, ha?
        :param image_tag: The docker image tag to use for tagging pushed images. This field is required if ``imageParameterName`` is ommited (otherwise, the app won't be able to find the image). Default: - this parameter is REQUIRED after 1.21.0
        :param repository_name: ECR repository name, if omitted a default name based on the asset's ID is used instead. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - this parameter is REQUIRED after 1.21.0
        :param target: Docker target to build to. Default: no build target
        """
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
            "packaging": packaging,
            "path": path,
            "source_hash": source_hash,
        }
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if image_name_parameter is not None:
            self._values["image_name_parameter"] = image_name_parameter
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def id(self) -> builtins.str:
        """Logical identifier for the asset."""
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return result

    @builtins.property
    def packaging(self) -> builtins.str:
        """Type of asset."""
        result = self._values.get("packaging")
        assert result is not None, "Required property 'packaging' is missing"
        return result

    @builtins.property
    def path(self) -> builtins.str:
        """Path on disk to the asset."""
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return result

    @builtins.property
    def source_hash(self) -> builtins.str:
        """The hash of the asset source."""
        result = self._values.get("source_hash")
        assert result is not None, "Required property 'source_hash' is missing"
        return result

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Build args to pass to the ``docker build`` command.

        :default: no build args are passed
        """
        result = self._values.get("build_args")
        return result

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        """Path to the Dockerfile (relative to the directory).

        :default: - no file is passed
        """
        result = self._values.get("file")
        return result

    @builtins.property
    def image_name_parameter(self) -> typing.Optional[builtins.str]:
        """(deprecated) ECR Repository name and repo digest (separated by "@sha256:") where this image is stored.

        :default:

        undefined If not specified, ``repositoryName`` and ``imageTag`` are
        required because otherwise how will the stack know where to find the asset,
        ha?

        :deprecated:

        specify ``repositoryName`` and ``imageTag`` instead, and then you
        know where the image will go.

        :stability: deprecated
        """
        result = self._values.get("image_name_parameter")
        return result

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        """The docker image tag to use for tagging pushed images.

        This field is
        required if ``imageParameterName`` is ommited (otherwise, the app won't be
        able to find the image).

        :default: - this parameter is REQUIRED after 1.21.0
        """
        result = self._values.get("image_tag")
        return result

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        """ECR repository name, if omitted a default name based on the asset's ID is used instead.

        Specify this property if you need to statically address the
        image, e.g. from a Kubernetes Pod. Note, this is only the repository name,
        without the registry and the tag parts.

        :default: - this parameter is REQUIRED after 1.21.0
        """
        result = self._values.get("repository_name")
        return result

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        """Docker target to build to.

        :default: no build target
        """
        result = self._values.get("target")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerImageAssetMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/cloud-assembly-schema.ContextProvider")
class ContextProvider(enum.Enum):
    """Identifier for the context provider."""

    AMI_PROVIDER = "AMI_PROVIDER"
    """AMI provider."""
    AVAILABILITY_ZONE_PROVIDER = "AVAILABILITY_ZONE_PROVIDER"
    """AZ provider."""
    HOSTED_ZONE_PROVIDER = "HOSTED_ZONE_PROVIDER"
    """Route53 Hosted Zone provider."""
    SSM_PARAMETER_PROVIDER = "SSM_PARAMETER_PROVIDER"
    """SSM Parameter Provider."""
    VPC_PROVIDER = "VPC_PROVIDER"
    """VPC Provider."""
    ENDPOINT_SERVICE_AVAILABILITY_ZONE_PROVIDER = "ENDPOINT_SERVICE_AVAILABILITY_ZONE_PROVIDER"
    """VPC Endpoint Service AZ Provider."""
    LOAD_BALANCER_PROVIDER = "LOAD_BALANCER_PROVIDER"
    """Load balancer provider."""
    LOAD_BALANCER_LISTENER_PROVIDER = "LOAD_BALANCER_LISTENER_PROVIDER"
    """Load balancer listener provider."""
    SECURITY_GROUP_PROVIDER = "SECURITY_GROUP_PROVIDER"
    """Security group provider."""


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.DockerImageAsset",
    jsii_struct_bases=[],
    name_mapping={"destinations": "destinations", "source": "source"},
)
class DockerImageAsset:
    def __init__(
        self,
        *,
        destinations: typing.Mapping[builtins.str, "DockerImageDestination"],
        source: "DockerImageSource",
    ) -> None:
        """A file asset.

        :param destinations: Destinations for this file asset.
        :param source: Source description for file assets.
        """
        if isinstance(source, dict):
            source = DockerImageSource(**source)
        self._values: typing.Dict[str, typing.Any] = {
            "destinations": destinations,
            "source": source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[builtins.str, "DockerImageDestination"]:
        """Destinations for this file asset."""
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return result

    @builtins.property
    def source(self) -> "DockerImageSource":
        """Source description for file assets."""
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.DockerImageDestination",
    jsii_struct_bases=[AwsDestination],
    name_mapping={
        "assume_role_arn": "assumeRoleArn",
        "assume_role_external_id": "assumeRoleExternalId",
        "region": "region",
        "image_tag": "imageTag",
        "repository_name": "repositoryName",
    },
)
class DockerImageDestination(AwsDestination):
    def __init__(
        self,
        *,
        assume_role_arn: typing.Optional[builtins.str] = None,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        image_tag: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        """Where to publish docker images.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        :param image_tag: Tag of the image to publish.
        :param repository_name: Name of the ECR repository to publish to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "image_tag": image_tag,
            "repository_name": repository_name,
        }
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        """The role that needs to be assumed while publishing this asset.

        :default: - No role will be assumed
        """
        result = self._values.get("assume_role_arn")
        return result

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        """The ExternalId that needs to be supplied while assuming this role.

        :default: - No ExternalId will be supplied
        """
        result = self._values.get("assume_role_external_id")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region where this asset will need to be published.

        :default: - Current region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def image_tag(self) -> builtins.str:
        """Tag of the image to publish."""
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return result

    @builtins.property
    def repository_name(self) -> builtins.str:
        """Name of the ECR repository to publish to."""
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.DockerImageSource",
    jsii_struct_bases=[],
    name_mapping={
        "directory": "directory",
        "docker_build_args": "dockerBuildArgs",
        "docker_build_target": "dockerBuildTarget",
        "docker_file": "dockerFile",
    },
)
class DockerImageSource:
    def __init__(
        self,
        *,
        directory: builtins.str,
        docker_build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_build_target: typing.Optional[builtins.str] = None,
        docker_file: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for how to produce a Docker image from a source.

        :param directory: The directory containing the Docker image build instructions. This path is relative to the asset manifest location.
        :param docker_build_args: Additional build arguments. Default: - No additional build arguments
        :param docker_build_target: Target build stage in a Dockerfile with multiple build stages. Default: - The last stage in the Dockerfile
        :param docker_file: The name of the file with build instructions. Default: "Dockerfile"
        """
        self._values: typing.Dict[str, typing.Any] = {
            "directory": directory,
        }
        if docker_build_args is not None:
            self._values["docker_build_args"] = docker_build_args
        if docker_build_target is not None:
            self._values["docker_build_target"] = docker_build_target
        if docker_file is not None:
            self._values["docker_file"] = docker_file

    @builtins.property
    def directory(self) -> builtins.str:
        """The directory containing the Docker image build instructions.

        This path is relative to the asset manifest location.
        """
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return result

    @builtins.property
    def docker_build_args(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Additional build arguments.

        :default: - No additional build arguments
        """
        result = self._values.get("docker_build_args")
        return result

    @builtins.property
    def docker_build_target(self) -> typing.Optional[builtins.str]:
        """Target build stage in a Dockerfile with multiple build stages.

        :default: - The last stage in the Dockerfile
        """
        result = self._values.get("docker_build_target")
        return result

    @builtins.property
    def docker_file(self) -> typing.Optional[builtins.str]:
        """The name of the file with build instructions.

        :default: "Dockerfile"
        """
        result = self._values.get("docker_file")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.EndpointServiceAvailabilityZonesContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "region": "region",
        "service_name": "serviceName",
    },
)
class EndpointServiceAvailabilityZonesContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        region: builtins.str,
        service_name: builtins.str,
    ) -> None:
        """Query to endpoint service context provider.

        :param account: Query account.
        :param region: Query region.
        :param service_name: Query service name.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "region": region,
            "service_name": service_name,
        }

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    @builtins.property
    def service_name(self) -> builtins.str:
        """Query service name."""
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointServiceAvailabilityZonesContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.FileAsset",
    jsii_struct_bases=[],
    name_mapping={"destinations": "destinations", "source": "source"},
)
class FileAsset:
    def __init__(
        self,
        *,
        destinations: typing.Mapping[builtins.str, "FileDestination"],
        source: "FileSource",
    ) -> None:
        """A file asset.

        :param destinations: Destinations for this file asset.
        :param source: Source description for file assets.
        """
        if isinstance(source, dict):
            source = FileSource(**source)
        self._values: typing.Dict[str, typing.Any] = {
            "destinations": destinations,
            "source": source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[builtins.str, "FileDestination"]:
        """Destinations for this file asset."""
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return result

    @builtins.property
    def source(self) -> "FileSource":
        """Source description for file assets."""
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.FileAssetMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_hash_parameter": "artifactHashParameter",
        "id": "id",
        "packaging": "packaging",
        "path": "path",
        "s3_bucket_parameter": "s3BucketParameter",
        "s3_key_parameter": "s3KeyParameter",
        "source_hash": "sourceHash",
    },
)
class FileAssetMetadataEntry:
    def __init__(
        self,
        *,
        artifact_hash_parameter: builtins.str,
        id: builtins.str,
        packaging: builtins.str,
        path: builtins.str,
        s3_bucket_parameter: builtins.str,
        s3_key_parameter: builtins.str,
        source_hash: builtins.str,
    ) -> None:
        """Metadata Entry spec for files.

        :param artifact_hash_parameter: The name of the parameter where the hash of the bundled asset should be passed in.
        :param id: Logical identifier for the asset.
        :param packaging: Requested packaging style.
        :param path: Path on disk to the asset.
        :param s3_bucket_parameter: Name of parameter where S3 bucket should be passed in.
        :param s3_key_parameter: Name of parameter where S3 key should be passed in.
        :param source_hash: The hash of the asset source.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "artifact_hash_parameter": artifact_hash_parameter,
            "id": id,
            "packaging": packaging,
            "path": path,
            "s3_bucket_parameter": s3_bucket_parameter,
            "s3_key_parameter": s3_key_parameter,
            "source_hash": source_hash,
        }

    @builtins.property
    def artifact_hash_parameter(self) -> builtins.str:
        """The name of the parameter where the hash of the bundled asset should be passed in."""
        result = self._values.get("artifact_hash_parameter")
        assert result is not None, "Required property 'artifact_hash_parameter' is missing"
        return result

    @builtins.property
    def id(self) -> builtins.str:
        """Logical identifier for the asset."""
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return result

    @builtins.property
    def packaging(self) -> builtins.str:
        """Requested packaging style."""
        result = self._values.get("packaging")
        assert result is not None, "Required property 'packaging' is missing"
        return result

    @builtins.property
    def path(self) -> builtins.str:
        """Path on disk to the asset."""
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return result

    @builtins.property
    def s3_bucket_parameter(self) -> builtins.str:
        """Name of parameter where S3 bucket should be passed in."""
        result = self._values.get("s3_bucket_parameter")
        assert result is not None, "Required property 's3_bucket_parameter' is missing"
        return result

    @builtins.property
    def s3_key_parameter(self) -> builtins.str:
        """Name of parameter where S3 key should be passed in."""
        result = self._values.get("s3_key_parameter")
        assert result is not None, "Required property 's3_key_parameter' is missing"
        return result

    @builtins.property
    def source_hash(self) -> builtins.str:
        """The hash of the asset source."""
        result = self._values.get("source_hash")
        assert result is not None, "Required property 'source_hash' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileAssetMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/cloud-assembly-schema.FileAssetPackaging")
class FileAssetPackaging(enum.Enum):
    """Packaging strategy for file assets."""

    FILE = "FILE"
    """Upload the given path as a file."""
    ZIP_DIRECTORY = "ZIP_DIRECTORY"
    """The given path is a directory, zip it and upload."""


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.FileDestination",
    jsii_struct_bases=[AwsDestination],
    name_mapping={
        "assume_role_arn": "assumeRoleArn",
        "assume_role_external_id": "assumeRoleExternalId",
        "region": "region",
        "bucket_name": "bucketName",
        "object_key": "objectKey",
    },
)
class FileDestination(AwsDestination):
    def __init__(
        self,
        *,
        assume_role_arn: typing.Optional[builtins.str] = None,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: builtins.str,
        object_key: builtins.str,
    ) -> None:
        """Where in S3 a file asset needs to be published.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        :param bucket_name: The name of the bucket.
        :param object_key: The destination object key.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_name": bucket_name,
            "object_key": object_key,
        }
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        """The role that needs to be assumed while publishing this asset.

        :default: - No role will be assumed
        """
        result = self._values.get("assume_role_arn")
        return result

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        """The ExternalId that needs to be supplied while assuming this role.

        :default: - No ExternalId will be supplied
        """
        result = self._values.get("assume_role_external_id")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region where this asset will need to be published.

        :default: - Current region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def bucket_name(self) -> builtins.str:
        """The name of the bucket."""
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return result

    @builtins.property
    def object_key(self) -> builtins.str:
        """The destination object key."""
        result = self._values.get("object_key")
        assert result is not None, "Required property 'object_key' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.FileSource",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "packaging": "packaging"},
)
class FileSource:
    def __init__(
        self,
        *,
        path: builtins.str,
        packaging: typing.Optional[FileAssetPackaging] = None,
    ) -> None:
        """Describe the source of a file asset.

        :param path: The filesystem object to upload. This path is relative to the asset manifest location.
        :param packaging: Packaging method. Default: FILE
        """
        self._values: typing.Dict[str, typing.Any] = {
            "path": path,
        }
        if packaging is not None:
            self._values["packaging"] = packaging

    @builtins.property
    def path(self) -> builtins.str:
        """The filesystem object to upload.

        This path is relative to the asset manifest location.
        """
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return result

    @builtins.property
    def packaging(self) -> typing.Optional[FileAssetPackaging]:
        """Packaging method.

        :default: FILE
        """
        result = self._values.get("packaging")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.HostedZoneContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "domain_name": "domainName",
        "region": "region",
        "private_zone": "privateZone",
        "vpc_id": "vpcId",
    },
)
class HostedZoneContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        domain_name: builtins.str,
        region: builtins.str,
        private_zone: typing.Optional[builtins.bool] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Query to hosted zone context provider.

        :param account: Query account.
        :param domain_name: The domain name e.g. example.com to lookup.
        :param region: Query region.
        :param private_zone: True if the zone you want to find is a private hosted zone. Default: false
        :param vpc_id: The VPC ID to that the private zone must be associated with. If you provide VPC ID and privateZone is false, this will return no results and raise an error. Default: - Required if privateZone=true
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "domain_name": domain_name,
            "region": region,
        }
        if private_zone is not None:
            self._values["private_zone"] = private_zone
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def domain_name(self) -> builtins.str:
        """The domain name e.g. example.com to lookup."""
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    @builtins.property
    def private_zone(self) -> typing.Optional[builtins.bool]:
        """True if the zone you want to find is a private hosted zone.

        :default: false
        """
        result = self._values.get("private_zone")
        return result

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        """The VPC ID to that the private zone must be associated with.

        If you provide VPC ID and privateZone is false, this will return no results
        and raise an error.

        :default: - Required if privateZone=true
        """
        result = self._values.get("vpc_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostedZoneContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.LoadBalancerFilter",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_type": "loadBalancerType",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class LoadBalancerFilter:
    def __init__(
        self,
        *,
        load_balancer_type: "LoadBalancerType",
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.List["Tag"]] = None,
    ) -> None:
        """Filters for selecting load balancers.

        :param load_balancer_type: Filter load balancers by their type.
        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        """
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_type": load_balancer_type,
        }
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_type(self) -> "LoadBalancerType":
        """Filter load balancers by their type."""
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return result

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Find by load balancer's ARN.

        :default: - does not search by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(self) -> typing.Optional[typing.List["Tag"]]:
        """Match load balancer tags.

        :default: - does not match load balancers by tags
        """
        result = self._values.get("load_balancer_tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.LoadBalancerListenerContextQuery",
    jsii_struct_bases=[LoadBalancerFilter],
    name_mapping={
        "load_balancer_type": "loadBalancerType",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "account": "account",
        "region": "region",
        "listener_arn": "listenerArn",
        "listener_port": "listenerPort",
        "listener_protocol": "listenerProtocol",
    },
)
class LoadBalancerListenerContextQuery(LoadBalancerFilter):
    def __init__(
        self,
        *,
        load_balancer_type: "LoadBalancerType",
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.List["Tag"]] = None,
        account: builtins.str,
        region: builtins.str,
        listener_arn: typing.Optional[builtins.str] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        listener_protocol: typing.Optional["LoadBalancerListenerProtocol"] = None,
    ) -> None:
        """Query input for looking up a load balancer listener.

        :param load_balancer_type: Filter load balancers by their type.
        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        :param account: Query account.
        :param region: Query region.
        :param listener_arn: Find by listener's arn. Default: - does not find by listener arn
        :param listener_port: Filter listeners by listener port. Default: - does not filter by a listener port
        :param listener_protocol: Filter by listener protocol. Default: - does not filter by listener protocol
        """
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_type": load_balancer_type,
            "account": account,
            "region": region,
        }
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags
        if listener_arn is not None:
            self._values["listener_arn"] = listener_arn
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if listener_protocol is not None:
            self._values["listener_protocol"] = listener_protocol

    @builtins.property
    def load_balancer_type(self) -> "LoadBalancerType":
        """Filter load balancers by their type."""
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return result

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Find by load balancer's ARN.

        :default: - does not search by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(self) -> typing.Optional[typing.List["Tag"]]:
        """Match load balancer tags.

        :default: - does not match load balancers by tags
        """
        result = self._values.get("load_balancer_tags")
        return result

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    @builtins.property
    def listener_arn(self) -> typing.Optional[builtins.str]:
        """Find by listener's arn.

        :default: - does not find by listener arn
        """
        result = self._values.get("listener_arn")
        return result

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Filter listeners by listener port.

        :default: - does not filter by a listener port
        """
        result = self._values.get("listener_port")
        return result

    @builtins.property
    def listener_protocol(self) -> typing.Optional["LoadBalancerListenerProtocol"]:
        """Filter by listener protocol.

        :default: - does not filter by listener protocol
        """
        result = self._values.get("listener_protocol")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerListenerContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/cloud-assembly-schema.LoadBalancerListenerProtocol")
class LoadBalancerListenerProtocol(enum.Enum):
    """The protocol for connections from clients to the load balancer."""

    HTTP = "HTTP"
    """HTTP protocol."""
    HTTPS = "HTTPS"
    """HTTPS protocol."""
    TCP = "TCP"
    """TCP protocol."""
    TLS = "TLS"
    """TLS protocol."""
    UDP = "UDP"
    """UDP protocol."""
    TCP_UDP = "TCP_UDP"
    """TCP and UDP protocol."""


@jsii.enum(jsii_type="@aws-cdk/cloud-assembly-schema.LoadBalancerType")
class LoadBalancerType(enum.Enum):
    """Type of load balancer."""

    NETWORK = "NETWORK"
    """Network load balancer."""
    APPLICATION = "APPLICATION"
    """Application load balancer."""


class Manifest(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/cloud-assembly-schema.Manifest",
):
    """Protocol utility class."""

    @jsii.member(jsii_name="load")
    @builtins.classmethod
    def load(cls, file_path: builtins.str) -> AssemblyManifest:
        """(deprecated) Deprecated.

        :param file_path: -

        :deprecated: use ``loadAssemblyManifest()``

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "load", [file_path])

    @jsii.member(jsii_name="loadAssemblyManifest")
    @builtins.classmethod
    def load_assembly_manifest(cls, file_path: builtins.str) -> AssemblyManifest:
        """Load and validates the cloud assembly manifest from file.

        :param file_path: - path to the manifest file.
        """
        return jsii.sinvoke(cls, "loadAssemblyManifest", [file_path])

    @jsii.member(jsii_name="loadAssetManifest")
    @builtins.classmethod
    def load_asset_manifest(cls, file_path: builtins.str) -> AssetManifest:
        """Load and validates the asset manifest from file.

        :param file_path: - path to the manifest file.
        """
        return jsii.sinvoke(cls, "loadAssetManifest", [file_path])

    @jsii.member(jsii_name="save")
    @builtins.classmethod
    def save(cls, manifest: AssemblyManifest, file_path: builtins.str) -> None:
        """(deprecated) Deprecated.

        :param manifest: -
        :param file_path: -

        :deprecated: use ``saveAssemblyManifest()``

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "save", [manifest, file_path])

    @jsii.member(jsii_name="saveAssemblyManifest")
    @builtins.classmethod
    def save_assembly_manifest(
        cls,
        manifest: AssemblyManifest,
        file_path: builtins.str,
    ) -> None:
        """Validates and saves the cloud assembly manifest to file.

        :param manifest: - manifest.
        :param file_path: - output file path.
        """
        return jsii.sinvoke(cls, "saveAssemblyManifest", [manifest, file_path])

    @jsii.member(jsii_name="saveAssetManifest")
    @builtins.classmethod
    def save_asset_manifest(
        cls,
        manifest: AssetManifest,
        file_path: builtins.str,
    ) -> None:
        """Validates and saves the asset manifest to file.

        :param manifest: - manifest.
        :param file_path: - output file path.
        """
        return jsii.sinvoke(cls, "saveAssetManifest", [manifest, file_path])

    @jsii.member(jsii_name="version")
    @builtins.classmethod
    def version(cls) -> builtins.str:
        """Fetch the current schema version number."""
        return jsii.sinvoke(cls, "version", [])


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.MetadataEntry",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "data": "data", "trace": "trace"},
)
class MetadataEntry:
    def __init__(
        self,
        *,
        type: builtins.str,
        data: typing.Optional[typing.Union[builtins.str, FileAssetMetadataEntry, ContainerImageAssetMetadataEntry, typing.List["Tag"]]] = None,
        trace: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """A metadata entry in a cloud assembly artifact.

        :param type: The type of the metadata entry.
        :param data: The data. Default: - no data.
        :param trace: A stack trace for when the entry was created. Default: - no trace.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if data is not None:
            self._values["data"] = data
        if trace is not None:
            self._values["trace"] = trace

    @builtins.property
    def type(self) -> builtins.str:
        """The type of the metadata entry."""
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def data(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, FileAssetMetadataEntry, ContainerImageAssetMetadataEntry, typing.List["Tag"]]]:
        """The data.

        :default: - no data.
        """
        result = self._values.get("data")
        return result

    @builtins.property
    def trace(self) -> typing.Optional[typing.List[builtins.str]]:
        """A stack trace for when the entry was created.

        :default: - no trace.
        """
        result = self._values.get("trace")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.MissingContext",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "props": "props", "provider": "provider"},
)
class MissingContext:
    def __init__(
        self,
        *,
        key: builtins.str,
        props: typing.Union[AmiContextQuery, AvailabilityZonesContextQuery, HostedZoneContextQuery, "SSMParameterContextQuery", "VpcContextQuery", EndpointServiceAvailabilityZonesContextQuery, "LoadBalancerContextQuery", LoadBalancerListenerContextQuery, "SecurityGroupContextQuery"],
        provider: ContextProvider,
    ) -> None:
        """Represents a missing piece of context.

        :param key: The missing context key.
        :param props: A set of provider-specific options.
        :param provider: The provider from which we expect this context key to be obtained.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "props": props,
            "provider": provider,
        }

    @builtins.property
    def key(self) -> builtins.str:
        """The missing context key."""
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return result

    @builtins.property
    def props(
        self,
    ) -> typing.Union[AmiContextQuery, AvailabilityZonesContextQuery, HostedZoneContextQuery, "SSMParameterContextQuery", "VpcContextQuery", EndpointServiceAvailabilityZonesContextQuery, "LoadBalancerContextQuery", LoadBalancerListenerContextQuery, "SecurityGroupContextQuery"]:
        """A set of provider-specific options."""
        result = self._values.get("props")
        assert result is not None, "Required property 'props' is missing"
        return result

    @builtins.property
    def provider(self) -> ContextProvider:
        """The provider from which we expect this context key to be obtained."""
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MissingContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.NestedCloudAssemblyProperties",
    jsii_struct_bases=[],
    name_mapping={"directory_name": "directoryName", "display_name": "displayName"},
)
class NestedCloudAssemblyProperties:
    def __init__(
        self,
        *,
        directory_name: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Artifact properties for nested cloud assemblies.

        :param directory_name: Relative path to the nested cloud assembly.
        :param display_name: Display name for the cloud assembly. Default: - The artifact ID
        """
        self._values: typing.Dict[str, typing.Any] = {
            "directory_name": directory_name,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def directory_name(self) -> builtins.str:
        """Relative path to the nested cloud assembly."""
        result = self._values.get("directory_name")
        assert result is not None, "Required property 'directory_name' is missing"
        return result

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        """Display name for the cloud assembly.

        :default: - The artifact ID
        """
        result = self._values.get("display_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NestedCloudAssemblyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.RuntimeInfo",
    jsii_struct_bases=[],
    name_mapping={"libraries": "libraries"},
)
class RuntimeInfo:
    def __init__(
        self,
        *,
        libraries: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        """Information about the application's runtime components.

        :param libraries: The list of libraries loaded in the application, associated with their versions.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "libraries": libraries,
        }

    @builtins.property
    def libraries(self) -> typing.Mapping[builtins.str, builtins.str]:
        """The list of libraries loaded in the application, associated with their versions."""
        result = self._values.get("libraries")
        assert result is not None, "Required property 'libraries' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.SSMParameterContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "parameter_name": "parameterName",
        "region": "region",
    },
)
class SSMParameterContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        parameter_name: builtins.str,
        region: builtins.str,
    ) -> None:
        """Query to SSM Parameter Context Provider.

        :param account: Query account.
        :param parameter_name: Parameter name to query.
        :param region: Query region.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "parameter_name": parameter_name,
            "region": region,
        }

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def parameter_name(self) -> builtins.str:
        """Parameter name to query."""
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SSMParameterContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.SecurityGroupContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "region": "region",
        "security_group_id": "securityGroupId",
    },
)
class SecurityGroupContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        region: builtins.str,
        security_group_id: builtins.str,
    ) -> None:
        """Query input for looking up a security group.

        :param account: Query account.
        :param region: Query region.
        :param security_group_id: Security group id.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "region": region,
            "security_group_id": security_group_id,
        }

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    @builtins.property
    def security_group_id(self) -> builtins.str:
        """Security group id."""
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.Tag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Tag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        """Metadata Entry spec for stack tag.

        :param key: Tag key. (In the actual file on disk this will be cased as "Key", and the structure is patched to match this structure upon loading: https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)
        :param value: Tag value. (In the actual file on disk this will be cased as "Value", and the structure is patched to match this structure upon loading: https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        """Tag key.

        (In the actual file on disk this will be cased as "Key", and the structure is
        patched to match this structure upon loading:
        https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)
        """
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return result

    @builtins.property
    def value(self) -> builtins.str:
        """Tag value.

        (In the actual file on disk this will be cased as "Value", and the structure is
        patched to match this structure upon loading:
        https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)
        """
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.TreeArtifactProperties",
    jsii_struct_bases=[],
    name_mapping={"file": "file"},
)
class TreeArtifactProperties:
    def __init__(self, *, file: builtins.str) -> None:
        """Artifact properties for the Construct Tree Artifact.

        :param file: Filename of the tree artifact.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "file": file,
        }

    @builtins.property
    def file(self) -> builtins.str:
        """Filename of the tree artifact."""
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TreeArtifactProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.VpcContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "filter": "filter",
        "region": "region",
        "return_asymmetric_subnets": "returnAsymmetricSubnets",
        "subnet_group_name_tag": "subnetGroupNameTag",
    },
)
class VpcContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        filter: typing.Mapping[builtins.str, builtins.str],
        region: builtins.str,
        return_asymmetric_subnets: typing.Optional[builtins.bool] = None,
        subnet_group_name_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        """Query input for looking up a VPC.

        :param account: Query account.
        :param filter: Filters to apply to the VPC. Filter parameters are the same as passed to DescribeVpcs.
        :param region: Query region.
        :param return_asymmetric_subnets: Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups. Default: false
        :param subnet_group_name_tag: Optional tag for subnet group name. If not provided, we'll look at the aws-cdk:subnet-name tag. If the subnet does not have the specified tag, we'll use its type as the name. Default: 'aws-cdk:subnet-name'
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "filter": filter,
            "region": region,
        }
        if return_asymmetric_subnets is not None:
            self._values["return_asymmetric_subnets"] = return_asymmetric_subnets
        if subnet_group_name_tag is not None:
            self._values["subnet_group_name_tag"] = subnet_group_name_tag

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def filter(self) -> typing.Mapping[builtins.str, builtins.str]:
        """Filters to apply to the VPC.

        Filter parameters are the same as passed to DescribeVpcs.

        :see: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html
        """
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    @builtins.property
    def return_asymmetric_subnets(self) -> typing.Optional[builtins.bool]:
        """Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups.

        :default: false
        """
        result = self._values.get("return_asymmetric_subnets")
        return result

    @builtins.property
    def subnet_group_name_tag(self) -> typing.Optional[builtins.str]:
        """Optional tag for subnet group name.

        If not provided, we'll look at the aws-cdk:subnet-name tag.
        If the subnet does not have the specified tag,
        we'll use its type as the name.

        :default: 'aws-cdk:subnet-name'
        """
        result = self._values.get("subnet_group_name_tag")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/cloud-assembly-schema.LoadBalancerContextQuery",
    jsii_struct_bases=[LoadBalancerFilter],
    name_mapping={
        "load_balancer_type": "loadBalancerType",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "account": "account",
        "region": "region",
    },
)
class LoadBalancerContextQuery(LoadBalancerFilter):
    def __init__(
        self,
        *,
        load_balancer_type: LoadBalancerType,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.List[Tag]] = None,
        account: builtins.str,
        region: builtins.str,
    ) -> None:
        """Query input for looking up a load balancer.

        :param load_balancer_type: Filter load balancers by their type.
        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        :param account: Query account.
        :param region: Query region.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_type": load_balancer_type,
            "account": account,
            "region": region,
        }
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_type(self) -> LoadBalancerType:
        """Filter load balancers by their type."""
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return result

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Find by load balancer's ARN.

        :default: - does not search by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(self) -> typing.Optional[typing.List[Tag]]:
        """Match load balancer tags.

        :default: - does not match load balancers by tags
        """
        result = self._values.get("load_balancer_tags")
        return result

    @builtins.property
    def account(self) -> builtins.str:
        """Query account."""
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return result

    @builtins.property
    def region(self) -> builtins.str:
        """Query region."""
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmiContextQuery",
    "ArtifactManifest",
    "ArtifactMetadataEntryType",
    "ArtifactType",
    "AssemblyManifest",
    "AssetManifest",
    "AssetManifestProperties",
    "AvailabilityZonesContextQuery",
    "AwsCloudFormationStackProperties",
    "AwsDestination",
    "ContainerImageAssetMetadataEntry",
    "ContextProvider",
    "DockerImageAsset",
    "DockerImageDestination",
    "DockerImageSource",
    "EndpointServiceAvailabilityZonesContextQuery",
    "FileAsset",
    "FileAssetMetadataEntry",
    "FileAssetPackaging",
    "FileDestination",
    "FileSource",
    "HostedZoneContextQuery",
    "LoadBalancerContextQuery",
    "LoadBalancerFilter",
    "LoadBalancerListenerContextQuery",
    "LoadBalancerListenerProtocol",
    "LoadBalancerType",
    "Manifest",
    "MetadataEntry",
    "MissingContext",
    "NestedCloudAssemblyProperties",
    "RuntimeInfo",
    "SSMParameterContextQuery",
    "SecurityGroupContextQuery",
    "Tag",
    "TreeArtifactProperties",
    "VpcContextQuery",
]

publication.publish()
