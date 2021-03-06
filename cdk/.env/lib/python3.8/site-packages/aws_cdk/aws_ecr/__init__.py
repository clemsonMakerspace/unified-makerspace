"""
## Amazon ECR Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This package contains constructs for working with Amazon Elastic Container Registry.

### Repositories

Define a repository by creating a new instance of `Repository`. A repository
holds multiple verions of a single container image.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository = ecr.Repository(self, "Repository")
```

### Image scanning

Amazon ECR image scanning helps in identifying software vulnerabilities in your container images. You can manually scan container images stored in Amazon ECR, or you can configure your repositories to scan images when you push them to a repository. To create a new repository to scan on push, simply enable `imageScanOnPush` in the properties

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository = ecr.Repository(stack, "Repo",
    image_scan_on_push=True
)
```

To create an `onImageScanCompleted` event rule and trigger the event target

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository.on_image_scan_completed("ImageScanComplete").add_target(...)
```

### Automatically clean up repositories

You can set life cycle rules to automatically clean up old images from your
repository. The first life cycle rule that matches an image will be applied
against that image. For example, the following deletes images older than
30 days, while keeping all images tagged with prod (note that the order
is important here):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository.add_lifecycle_rule(tag_prefix_list=["prod"], max_image_count=9999)
repository.add_lifecycle_rule(max_image_age=cdk.Duration.days(30))
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
import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRepository(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.CfnRepository",
):
    """A CloudFormation ``AWS::ECR::Repository``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
    :cloudformationResource: AWS::ECR::Repository
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        image_scanning_configuration: typing.Any = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        lifecycle_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.LifecyclePolicyProperty"]] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::ECR::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param image_scanning_configuration: ``AWS::ECR::Repository.ImageScanningConfiguration``.
        :param image_tag_mutability: ``AWS::ECR::Repository.ImageTagMutability``.
        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.
        """
        props = CfnRepositoryProps(
            image_scanning_configuration=image_scanning_configuration,
            image_tag_mutability=image_tag_mutability,
            lifecycle_policy=lifecycle_policy,
            repository_name=repository_name,
            repository_policy_text=repository_policy_text,
            tags=tags,
        )

        jsii.create(CfnRepository, self, [scope, id, props])

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
        """``AWS::ECR::Repository.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageScanningConfiguration")
    def image_scanning_configuration(self) -> typing.Any:
        """``AWS::ECR::Repository.ImageScanningConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagescanningconfiguration
        """
        return jsii.get(self, "imageScanningConfiguration")

    @image_scanning_configuration.setter # type: ignore
    def image_scanning_configuration(self, value: typing.Any) -> None:
        jsii.set(self, "imageScanningConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryPolicyText")
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::Repository.RepositoryPolicyText``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        """
        return jsii.get(self, "repositoryPolicyText")

    @repository_policy_text.setter # type: ignore
    def repository_policy_text(self, value: typing.Any) -> None:
        jsii.set(self, "repositoryPolicyText", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageTagMutability")
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.ImageTagMutability``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutability
        """
        return jsii.get(self, "imageTagMutability")

    @image_tag_mutability.setter # type: ignore
    def image_tag_mutability(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageTagMutability", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lifecyclePolicy")
    def lifecycle_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.LifecyclePolicyProperty"]]:
        """``AWS::ECR::Repository.LifecyclePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        """
        return jsii.get(self, "lifecyclePolicy")

    @lifecycle_policy.setter # type: ignore
    def lifecycle_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.LifecyclePolicyProperty"]],
    ) -> None:
        jsii.set(self, "lifecyclePolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.RepositoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        """
        return jsii.get(self, "repositoryName")

    @repository_name.setter # type: ignore
    def repository_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "repositoryName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ecr.CfnRepository.LifecyclePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lifecycle_policy_text": "lifecyclePolicyText",
            "registry_id": "registryId",
        },
    )
    class LifecyclePolicyProperty:
        def __init__(
            self,
            *,
            lifecycle_policy_text: typing.Optional[builtins.str] = None,
            registry_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param lifecycle_policy_text: ``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.
            :param registry_id: ``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if lifecycle_policy_text is not None:
                self._values["lifecycle_policy_text"] = lifecycle_policy_text
            if registry_id is not None:
                self._values["registry_id"] = registry_id

        @builtins.property
        def lifecycle_policy_text(self) -> typing.Optional[builtins.str]:
            """``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-lifecyclepolicytext
            """
            result = self._values.get("lifecycle_policy_text")
            return result

        @builtins.property
        def registry_id(self) -> typing.Optional[builtins.str]:
            """``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-registryid
            """
            result = self._values.get("registry_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecyclePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.CfnRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_scanning_configuration": "imageScanningConfiguration",
        "image_tag_mutability": "imageTagMutability",
        "lifecycle_policy": "lifecyclePolicy",
        "repository_name": "repositoryName",
        "repository_policy_text": "repositoryPolicyText",
        "tags": "tags",
    },
)
class CfnRepositoryProps:
    def __init__(
        self,
        *,
        image_scanning_configuration: typing.Any = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        lifecycle_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.LifecyclePolicyProperty]] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ECR::Repository``.

        :param image_scanning_configuration: ``AWS::ECR::Repository.ImageScanningConfiguration``.
        :param image_tag_mutability: ``AWS::ECR::Repository.ImageTagMutability``.
        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if image_scanning_configuration is not None:
            self._values["image_scanning_configuration"] = image_scanning_configuration
        if image_tag_mutability is not None:
            self._values["image_tag_mutability"] = image_tag_mutability
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_policy_text is not None:
            self._values["repository_policy_text"] = repository_policy_text
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def image_scanning_configuration(self) -> typing.Any:
        """``AWS::ECR::Repository.ImageScanningConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagescanningconfiguration
        """
        result = self._values.get("image_scanning_configuration")
        return result

    @builtins.property
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.ImageTagMutability``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutability
        """
        result = self._values.get("image_tag_mutability")
        return result

    @builtins.property
    def lifecycle_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.LifecyclePolicyProperty]]:
        """``AWS::ECR::Repository.LifecyclePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        """
        result = self._values.get("lifecycle_policy")
        return result

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.RepositoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        """
        result = self._values.get("repository_name")
        return result

    @builtins.property
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::Repository.RepositoryPolicyText``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        """
        result = self._values.get("repository_policy_text")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ECR::Repository.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-ecr.IRepository")
class IRepository(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents an ECR repository."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """The ARN of the repository.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """The name of the repository.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        """The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        :attribute: true
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        """
        ...

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull images in this repository.

        :param grantee: -
        """
        ...

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        """
        ...

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
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
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).
        """
        ...


class _IRepositoryProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Represents an ECR repository."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ecr.IRepository"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """The ARN of the repository.

        :attribute: true
        """
        return jsii.get(self, "repositoryArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """The name of the repository.

        :attribute: true
        """
        return jsii.get(self, "repositoryName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        """The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        :attribute: true
        """
        return jsii.get(self, "repositoryUri")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull images in this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
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

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailImagePushedOptions(
            image_tag=image_tag,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onCloudTrailImagePushed", [id, options])

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
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
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

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnImageScanCompletedOptions(
            image_tags=image_tags,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onImageScanCompleted", [id, options])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).
        """
        return jsii.invoke(self, "repositoryUriForTag", [tag])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.LifecycleRule",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "max_image_age": "maxImageAge",
        "max_image_count": "maxImageCount",
        "rule_priority": "rulePriority",
        "tag_prefix_list": "tagPrefixList",
        "tag_status": "tagStatus",
    },
)
class LifecycleRule:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        max_image_age: typing.Optional[aws_cdk.core.Duration] = None,
        max_image_count: typing.Optional[jsii.Number] = None,
        rule_priority: typing.Optional[jsii.Number] = None,
        tag_prefix_list: typing.Optional[typing.List[builtins.str]] = None,
        tag_status: typing.Optional["TagStatus"] = None,
    ) -> None:
        """An ECR life cycle rule.

        :param description: Describes the purpose of the rule. Default: No description
        :param max_image_age: The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAge.
        :param rule_priority: Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if max_image_age is not None:
            self._values["max_image_age"] = max_image_age
        if max_image_count is not None:
            self._values["max_image_count"] = max_image_count
        if rule_priority is not None:
            self._values["rule_priority"] = rule_priority
        if tag_prefix_list is not None:
            self._values["tag_prefix_list"] = tag_prefix_list
        if tag_status is not None:
            self._values["tag_status"] = tag_status

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """Describes the purpose of the rule.

        :default: No description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def max_image_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum age of images to retain. The value must represent a number of days.

        Specify exactly one of maxImageCount and maxImageAge.
        """
        result = self._values.get("max_image_age")
        return result

    @builtins.property
    def max_image_count(self) -> typing.Optional[jsii.Number]:
        """The maximum number of images to retain.

        Specify exactly one of maxImageCount and maxImageAge.
        """
        result = self._values.get("max_image_count")
        return result

    @builtins.property
    def rule_priority(self) -> typing.Optional[jsii.Number]:
        """Controls the order in which rules are evaluated (low to high).

        All rules must have a unique priority, where lower numbers have
        higher precedence. The first rule that matches is applied to an image.

        There can only be one rule with a tagStatus of Any, and it must have
        the highest rulePriority.

        All rules without a specified priority will have incrementing priorities
        automatically assigned to them, higher than any rules that DO have priorities.

        :default: Automatically assigned
        """
        result = self._values.get("rule_priority")
        return result

    @builtins.property
    def tag_prefix_list(self) -> typing.Optional[typing.List[builtins.str]]:
        """Select images that have ALL the given prefixes in their tag.

        Only if tagStatus == TagStatus.Tagged
        """
        result = self._values.get("tag_prefix_list")
        return result

    @builtins.property
    def tag_status(self) -> typing.Optional["TagStatus"]:
        """Select images based on tags.

        Only one rule is allowed to select untagged images, and it must
        have the highest rulePriority.

        :default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        """
        result = self._values.get("tag_status")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.OnCloudTrailImagePushedOptions",
    jsii_struct_bases=[aws_cdk.aws_events.OnEventOptions],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "image_tag": "imageTag",
    },
)
class OnCloudTrailImagePushedOptions(aws_cdk.aws_events.OnEventOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        image_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options for the onCloudTrailImagePushed method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        """
        if isinstance(event_pattern, dict):
            event_pattern = aws_cdk.aws_events.EventPattern(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if image_tag is not None:
            self._values["image_tag"] = image_tag

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """A description of the rule's purpose.

        :default: - No description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Optional[aws_cdk.aws_events.EventPattern]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        """A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.
        """
        result = self._values.get("rule_name")
        return result

    @builtins.property
    def target(self) -> typing.Optional[aws_cdk.aws_events.IRuleTarget]:
        """The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        result = self._values.get("target")
        return result

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        """Only watch changes to this image tag.

        :default: - Watch changes to all tags
        """
        result = self._values.get("image_tag")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCloudTrailImagePushedOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.OnImageScanCompletedOptions",
    jsii_struct_bases=[aws_cdk.aws_events.OnEventOptions],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "image_tags": "imageTags",
    },
)
class OnImageScanCompletedOptions(aws_cdk.aws_events.OnEventOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Options for the OnImageScanCompleted method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        """
        if isinstance(event_pattern, dict):
            event_pattern = aws_cdk.aws_events.EventPattern(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if image_tags is not None:
            self._values["image_tags"] = image_tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """A description of the rule's purpose.

        :default: - No description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Optional[aws_cdk.aws_events.EventPattern]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        """A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.
        """
        result = self._values.get("rule_name")
        return result

    @builtins.property
    def target(self) -> typing.Optional[aws_cdk.aws_events.IRuleTarget]:
        """The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        result = self._values.get("target")
        return result

    @builtins.property
    def image_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        """Only watch changes to the image tags spedified.

        Leave it undefined to watch the full repository.

        :default: - Watch the changes to the repository with all image tags
        """
        result = self._values.get("image_tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnImageScanCompletedOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.RepositoryAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "repository_arn": "repositoryArn",
        "repository_name": "repositoryName",
    },
)
class RepositoryAttributes:
    def __init__(
        self,
        *,
        repository_arn: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        """
        :param repository_arn: 
        :param repository_name: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "repository_arn": repository_arn,
            "repository_name": repository_name,
        }

    @builtins.property
    def repository_arn(self) -> builtins.str:
        result = self._values.get("repository_arn")
        assert result is not None, "Required property 'repository_arn' is missing"
        return result

    @builtins.property
    def repository_name(self) -> builtins.str:
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRepository)
class RepositoryBase(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecr.RepositoryBase",
):
    """Base class for ECR repository.

    Reused between imported repositories and owned repositories.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _RepositoryBaseProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        """
        props = aws_cdk.core.ResourceProps(
            account=account, physical_name=physical_name, region=region
        )

        jsii.create(RepositoryBase, self, [scope, id, props])

    @jsii.member(jsii_name="addToResourcePolicy")
    @abc.abstractmethod
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to use the images in this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
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

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailImagePushedOptions(
            image_tag=image_tag,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onCloudTrailImagePushed", [id, options])

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
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
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

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image scan is completed.

        :param id: The id of the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnImageScanCompletedOptions(
            image_tags=image_tags,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onImageScanCompleted", [id, options])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """Returns the URL of the repository. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Optional image tag.
        """
        return jsii.invoke(self, "repositoryUriForTag", [tag])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    @abc.abstractmethod
    def repository_arn(self) -> builtins.str:
        """The ARN of the repository."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    @abc.abstractmethod
    def repository_name(self) -> builtins.str:
        """The name of the repository."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        """The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY
        """
        return jsii.get(self, "repositoryUri")


class _RepositoryBaseProxy(
    RepositoryBase, jsii.proxy_for(aws_cdk.core.Resource) # type: ignore
):
    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """The ARN of the repository."""
        return jsii.get(self, "repositoryArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """The name of the repository."""
        return jsii.get(self, "repositoryName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.RepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_scan_on_push": "imageScanOnPush",
        "lifecycle_registry_id": "lifecycleRegistryId",
        "lifecycle_rules": "lifecycleRules",
        "removal_policy": "removalPolicy",
        "repository_name": "repositoryName",
    },
)
class RepositoryProps:
    def __init__(
        self,
        *,
        image_scan_on_push: typing.Optional[builtins.bool] = None,
        lifecycle_registry_id: typing.Optional[builtins.str] = None,
        lifecycle_rules: typing.Optional[typing.List[LifecycleRule]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param image_scan_on_push: Enable the scan on push when creating the repository. Default: false
        :param lifecycle_registry_id: The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: Name for this repository. Default: Automatically generated name.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if image_scan_on_push is not None:
            self._values["image_scan_on_push"] = image_scan_on_push
        if lifecycle_registry_id is not None:
            self._values["lifecycle_registry_id"] = lifecycle_registry_id
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def image_scan_on_push(self) -> typing.Optional[builtins.bool]:
        """Enable the scan on push when creating the repository.

        :default: false
        """
        result = self._values.get("image_scan_on_push")
        return result

    @builtins.property
    def lifecycle_registry_id(self) -> typing.Optional[builtins.str]:
        """The AWS account ID associated with the registry that contains the repository.

        :default: The default registry is assumed.

        :see: https://docs.aws.amazon.com/AmazonECR/latest/APIReference/API_PutLifecyclePolicy.html
        """
        result = self._values.get("lifecycle_registry_id")
        return result

    @builtins.property
    def lifecycle_rules(self) -> typing.Optional[typing.List[LifecycleRule]]:
        """Life cycle rules to apply to this registry.

        :default: No life cycle rules
        """
        result = self._values.get("lifecycle_rules")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """Determine what happens to the repository when the resource/stack is deleted.

        :default: RemovalPolicy.Retain
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        """Name for this repository.

        :default: Automatically generated name.
        """
        result = self._values.get("repository_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ecr.TagStatus")
class TagStatus(enum.Enum):
    """Select images based on tags."""

    ANY = "ANY"
    """Rule applies to all images."""
    TAGGED = "TAGGED"
    """Rule applies to tagged images."""
    UNTAGGED = "UNTAGGED"
    """Rule applies to untagged images."""


class Repository(
    RepositoryBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.Repository",
):
    """Define an ECR repository."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        image_scan_on_push: typing.Optional[builtins.bool] = None,
        lifecycle_registry_id: typing.Optional[builtins.str] = None,
        lifecycle_rules: typing.Optional[typing.List[LifecycleRule]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param image_scan_on_push: Enable the scan on push when creating the repository. Default: false
        :param lifecycle_registry_id: The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: Name for this repository. Default: Automatically generated name.
        """
        props = RepositoryProps(
            image_scan_on_push=image_scan_on_push,
            lifecycle_registry_id=lifecycle_registry_id,
            lifecycle_rules=lifecycle_rules,
            removal_policy=removal_policy,
            repository_name=repository_name,
        )

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLocalRepository")
    @builtins.classmethod
    def arn_for_local_repository(
        cls,
        repository_name: builtins.str,
        scope: constructs.IConstruct,
        account: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """Returns an ECR ARN for a repository that resides in the same account/region as the current stack.

        :param repository_name: -
        :param scope: -
        :param account: -
        """
        return jsii.sinvoke(cls, "arnForLocalRepository", [repository_name, scope, account])

    @jsii.member(jsii_name="fromRepositoryArn")
    @builtins.classmethod
    def from_repository_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        repository_arn: builtins.str,
    ) -> IRepository:
        """
        :param scope: -
        :param id: -
        :param repository_arn: -
        """
        return jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn])

    @jsii.member(jsii_name="fromRepositoryAttributes")
    @builtins.classmethod
    def from_repository_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        repository_arn: builtins.str,
        repository_name: builtins.str,
    ) -> IRepository:
        """Import a repository.

        :param scope: -
        :param id: -
        :param repository_arn: 
        :param repository_name: 
        """
        attrs = RepositoryAttributes(
            repository_arn=repository_arn, repository_name=repository_name
        )

        return jsii.sinvoke(cls, "fromRepositoryAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromRepositoryName")
    @builtins.classmethod
    def from_repository_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        repository_name: builtins.str,
    ) -> IRepository:
        """
        :param scope: -
        :param id: -
        :param repository_name: -
        """
        return jsii.sinvoke(cls, "fromRepositoryName", [scope, id, repository_name])

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        max_image_age: typing.Optional[aws_cdk.core.Duration] = None,
        max_image_count: typing.Optional[jsii.Number] = None,
        rule_priority: typing.Optional[jsii.Number] = None,
        tag_prefix_list: typing.Optional[typing.List[builtins.str]] = None,
        tag_status: typing.Optional[TagStatus] = None,
    ) -> None:
        """Add a life cycle rule to the repository.

        Life cycle rules automatically expire images from the repository that match
        certain conditions.

        :param description: Describes the purpose of the rule. Default: No description
        :param max_image_age: The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAge.
        :param rule_priority: Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        """
        rule = LifecycleRule(
            description=description,
            max_image_age=max_image_age,
            max_image_count=max_image_count,
            rule_priority=rule_priority,
            tag_prefix_list=tag_prefix_list,
            tag_status=tag_status,
        )

        return jsii.invoke(self, "addLifecycleRule", [rule])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """The ARN of the repository."""
        return jsii.get(self, "repositoryArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """The name of the repository."""
        return jsii.get(self, "repositoryName")


__all__ = [
    "CfnRepository",
    "CfnRepositoryProps",
    "IRepository",
    "LifecycleRule",
    "OnCloudTrailImagePushedOptions",
    "OnImageScanCompletedOptions",
    "Repository",
    "RepositoryAttributes",
    "RepositoryBase",
    "RepositoryProps",
    "TagStatus",
]

publication.publish()
