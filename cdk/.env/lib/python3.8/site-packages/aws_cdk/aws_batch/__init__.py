"""
## AWS Batch Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

AWS Batch is a batch processing tool for efficiently running hundreds of thousands computing jobs in AWS. Batch can dynamically provision different types of compute resources based on the resource requirements of submitted jobs.

AWS Batch simplifies the planning, scheduling, and executions of your batch workloads across a full range of compute services like [Amazon EC2](https://aws.amazon.com/ec2/) and [Spot Resources](https://aws.amazon.com/ec2/spot/).

Batch achieves this by utilizing queue processing of batch job requests. To successfully submit a job for execution, you need the following resources:

1. [Job Definition](#job-definition) - *Group various job properties (container image, resource requirements, env variables...) into a single definition. These definitions are used at job submission time.*
2. [Compute Environment](#compute-environment) - *the execution runtime of submitted batch jobs*
3. [Job Queue](#job-queue) - *the queue where batch jobs can be submitted to via AWS SDK/CLI*

For more information on **AWS Batch** visit the [AWS Docs for Batch](https://docs.aws.amazon.com/batch/index.html).

## Compute Environment

At the core of AWS Batch is the compute environment. All batch jobs are processed within a compute environment, which uses resource like OnDemand or Spot EC2 instances.

In **MANAGED** mode, AWS will handle the provisioning of compute resources to accommodate the demand. Otherwise, in **UNMANAGED** mode, you will need to manage the provisioning of those resources.

Below is an example of each available type of compute environment:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
default_vpc = ec2.Vpc(self, "VPC")

# default is managed
aws_managed_environment = batch.ComputeEnvironment(stack, "AWS-Managed-Compute-Env",
    compute_resources={
        "vpc": vpc
    }
)

customer_managed_environment = batch.ComputeEnvironment(stack, "Customer-Managed-Compute-Env",
    managed=False
)
```

### Spot-Based Compute Environment

It is possible to have AWS Batch submit spotfleet requests for obtaining compute resources. Below is an example of how this can be done:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(self, "VPC")

spot_environment = batch.ComputeEnvironment(stack, "MySpotEnvironment",
    compute_resources={
        "type": batch.ComputeResourceType.SPOT,
        "bid_percentage": 75, # Bids for resources at 75% of the on-demand price
        "vpc": vpc
    }
)
```

### Understanding Progressive Allocation Strategies

AWS Batch uses an [allocation strategy](https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html) to determine what compute resource will efficiently handle incoming job requests. By default, **BEST_FIT** will pick an available compute instance based on vCPU requirements. If none exist, the job will wait until resources become available. However, with this strategy, you may have jobs waiting in the queue unnecessarily despite having more powerful instances available. Below is an example of how that situation might look like:

```
Compute Environment:

1. m5.xlarge => 4 vCPU
2. m5.2xlarge => 8 vCPU
```

```
Job Queue:
---------
| A | B |
---------

Job Requirements:
A => 4 vCPU - ALLOCATED TO m5.xlarge
B => 2 vCPU - WAITING
```

In this situation, Batch will allocate **Job A** to compute resource #1 because it is the most cost efficient resource that matches the vCPU requirement. However, with this `BEST_FIT` strategy, **Job B** will not be allocated to our other available compute resource even though it is strong enough to handle it. Instead, it will wait until the first job is finished processing or wait a similar `m5.xlarge` resource to be provisioned.

The alternative would be to use the `BEST_FIT_PROGRESSIVE` strategy in order for the remaining job to be handled in larger containers regardless of vCPU requirement and costs.

### Launch template support

Simply define your Launch Template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_launch_template = ec2.CfnLaunchTemplate(self, "LaunchTemplate",
    launch_template_name="extra-storage-template",
    launch_template_data={
        "block_device_mappings": [{
            "device_name": "/dev/xvdcz",
            "ebs": {
                "encrypted": True,
                "volume_size": 100,
                "volume_type": "gp2"
            }
        }
        ]
    }
)
```

and use it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources={
        "launch_template": {
            "launch_template_name": my_launch_template.launch_template_name
        },
        "vpc": vpc
    },
    compute_environment_name="MyStorageCapableComputeEnvironment"
)
```

### Importing an existing Compute Environment

To import an existing batch compute environment, call `ComputeEnvironment.fromComputeEnvironmentArn()`.

Below is an example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
compute_env = batch.ComputeEnvironment.from_compute_environment_arn(self, "imported-compute-env", "arn:aws:batch:us-east-1:555555555555:compute-environment/My-Compute-Env")
```

### Change the baseline AMI of the compute resources

Ocassionally, you will need to deviate from the default processing AMI.

ECS Optimized Amazon Linux 2 example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources={
        "image": ecs.EcsOptimizedAmi(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        ),
        "vpc": vpc
    }
)
```

Custom based AMI example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources={
        "image": ec2.MachineImage.generic_linux(
            [aws-region]="[ami-ID]"
        ),
        "vpc": vpc
    }
)
```

## Job Queue

Jobs are always submitted to a specific queue. This means that you have to create a queue before you can start submitting jobs. Each queue is mapped to at least one (and no more than three) compute environment. When the job is scheduled for execution, AWS Batch will select the compute environment based on ordinal priority and available capacity in each environment.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
job_queue = batch.JobQueue(stack, "JobQueue",
    compute_environments=[{
        # Defines a collection of compute resources to handle assigned batch jobs
        "compute_environment": compute_environment,
        # Order determines the allocation order for jobs (i.e. Lower means higher preferance for job assignment)
        "order": 1
    }
    ]
)
```

### Priorty-Based Queue Example

Sometimes you might have jobs that are more important than others, and when submitted, should take precedence over the existing jobs. To achieve this, you can create a priority based execution strategy, by assigning each queue its own priority:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
high_prio_queue = batch.JobQueue(stack, "JobQueue",
    compute_environments=shared_compute_envs,
    priority=2
)

low_prio_queue = batch.JobQueue(stack, "JobQueue",
    compute_environments=shared_compute_envs,
    priority=1
)
```

By making sure to use the same compute environments between both job queues, we will give precedence to the `highPrioQueue` for the assigning of jobs to available compute environments.

### Importing an existing Job Queue

To import an existing batch job queue, call `JobQueue.fromJobQueueArn()`.

Below is an example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
job_queue = batch.JobQueue.from_job_queue_arn(self, "imported-job-queue", "arn:aws:batch:us-east-1:555555555555:job-queue/High-Prio-Queue")
```

## Job Definition

A Batch Job definition helps AWS Batch understand important details about how to run your application in the scope of a Batch Job. This involves key information like resource requirements, what containers to run, how the compute environment should be prepared, and more. Below is a simple example of how to create a job definition:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repo = ecr.Repository.from_repository_name(stack, "batch-job-repo", "todo-list")

batch.JobDefinition(stack, "batch-job-def-from-ecr",
    container={
        "image": ecs.EcrImage(repo, "latest")
    }
)
```

### Using a local Docker project

Below is an example of how you can create a Batch Job Definition from a local Docker application.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
batch.JobDefinition(stack, "batch-job-def-from-local",
    container={
        # todo-list is a directory containing a Dockerfile to build the application
        "image": ecs.ContainerImage.from_asset("../todo-list")
    }
)
```

### Importing an existing Job Definition

#### From ARN

To import an existing batch job definition from its ARN, call `JobDefinition.fromJobDefinitionArn()`.

Below is an example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
job = batch.JobDefinition.from_job_definition_arn(self, "imported-job-definition", "arn:aws:batch:us-east-1:555555555555:job-definition/my-job-definition")
```

#### From Name

To import an existing batch job definition from its name, call `JobDefinition.fromJobDefinitionName()`.
If name is specified without a revision then the latest active revision is used.

Below is an example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Without revision
job = batch.JobDefinition.from_job_definition_name(self, "imported-job-definition", "my-job-definition")

# With revision
job = batch.JobDefinition.from_job_definition_name(self, "imported-job-definition", "my-job-definition:3")
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
import aws_cdk.aws_ecs
import aws_cdk.aws_iam
import aws_cdk.core
import constructs


@jsii.enum(jsii_type="@aws-cdk/aws-batch.AllocationStrategy")
class AllocationStrategy(enum.Enum):
    """(experimental) Properties for how to prepare compute resources that are provisioned for a compute environment.

    :stability: experimental
    """

    BEST_FIT = "BEST_FIT"
    """(experimental) Batch will use the best fitting instance type will be used when assigning a batch job in this compute environment.

    :stability: experimental
    """
    BEST_FIT_PROGRESSIVE = "BEST_FIT_PROGRESSIVE"
    """(experimental) Batch will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types with a lower cost per unit vCPU.

    :stability: experimental
    """
    SPOT_CAPACITY_OPTIMIZED = "SPOT_CAPACITY_OPTIMIZED"
    """(experimental) This is only available for Spot Instance compute resources and will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types that are less likely to be interrupted.

    :stability: experimental
    """


@jsii.implements(aws_cdk.core.IInspectable)
class CfnComputeEnvironment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment",
):
    """A CloudFormation ``AWS::Batch::ComputeEnvironment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
    :cloudformationResource: AWS::Batch::ComputeEnvironment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        service_role: builtins.str,
        type: builtins.str,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComputeEnvironment.ComputeResourcesProperty"]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::Batch::ComputeEnvironment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param service_role: ``AWS::Batch::ComputeEnvironment.ServiceRole``.
        :param type: ``AWS::Batch::ComputeEnvironment.Type``.
        :param compute_environment_name: ``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.
        :param compute_resources: ``AWS::Batch::ComputeEnvironment.ComputeResources``.
        :param state: ``AWS::Batch::ComputeEnvironment.State``.
        :param tags: ``AWS::Batch::ComputeEnvironment.Tags``.
        """
        props = CfnComputeEnvironmentProps(
            service_role=service_role,
            type=type,
            compute_environment_name=compute_environment_name,
            compute_resources=compute_resources,
            state=state,
            tags=tags,
        )

        jsii.create(CfnComputeEnvironment, self, [scope, id, props])

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
        """``AWS::Batch::ComputeEnvironment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> builtins.str:
        """``AWS::Batch::ComputeEnvironment.ServiceRole``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole
        """
        return jsii.get(self, "serviceRole")

    @service_role.setter # type: ignore
    def service_role(self, value: builtins.str) -> None:
        jsii.set(self, "serviceRole", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::Batch::ComputeEnvironment.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeenvironmentname
        """
        return jsii.get(self, "computeEnvironmentName")

    @compute_environment_name.setter # type: ignore
    def compute_environment_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "computeEnvironmentName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeResources")
    def compute_resources(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComputeEnvironment.ComputeResourcesProperty"]]:
        """``AWS::Batch::ComputeEnvironment.ComputeResources``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeresources
        """
        return jsii.get(self, "computeResources")

    @compute_resources.setter # type: ignore
    def compute_resources(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComputeEnvironment.ComputeResourcesProperty"]],
    ) -> None:
        jsii.set(self, "computeResources", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::ComputeEnvironment.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-state
        """
        return jsii.get(self, "state")

    @state.setter # type: ignore
    def state(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "state", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.ComputeResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_role": "instanceRole",
            "instance_types": "instanceTypes",
            "maxv_cpus": "maxvCpus",
            "minv_cpus": "minvCpus",
            "subnets": "subnets",
            "type": "type",
            "allocation_strategy": "allocationStrategy",
            "bid_percentage": "bidPercentage",
            "desiredv_cpus": "desiredvCpus",
            "ec2_key_pair": "ec2KeyPair",
            "image_id": "imageId",
            "launch_template": "launchTemplate",
            "placement_group": "placementGroup",
            "security_group_ids": "securityGroupIds",
            "spot_iam_fleet_role": "spotIamFleetRole",
            "tags": "tags",
        },
    )
    class ComputeResourcesProperty:
        def __init__(
            self,
            *,
            instance_role: builtins.str,
            instance_types: typing.List[builtins.str],
            maxv_cpus: jsii.Number,
            minv_cpus: jsii.Number,
            subnets: typing.List[builtins.str],
            type: builtins.str,
            allocation_strategy: typing.Optional[builtins.str] = None,
            bid_percentage: typing.Optional[jsii.Number] = None,
            desiredv_cpus: typing.Optional[jsii.Number] = None,
            ec2_key_pair: typing.Optional[builtins.str] = None,
            image_id: typing.Optional[builtins.str] = None,
            launch_template: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComputeEnvironment.LaunchTemplateSpecificationProperty"]] = None,
            placement_group: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            spot_iam_fleet_role: typing.Optional[builtins.str] = None,
            tags: typing.Any = None,
        ) -> None:
            """
            :param instance_role: ``CfnComputeEnvironment.ComputeResourcesProperty.InstanceRole``.
            :param instance_types: ``CfnComputeEnvironment.ComputeResourcesProperty.InstanceTypes``.
            :param maxv_cpus: ``CfnComputeEnvironment.ComputeResourcesProperty.MaxvCpus``.
            :param minv_cpus: ``CfnComputeEnvironment.ComputeResourcesProperty.MinvCpus``.
            :param subnets: ``CfnComputeEnvironment.ComputeResourcesProperty.Subnets``.
            :param type: ``CfnComputeEnvironment.ComputeResourcesProperty.Type``.
            :param allocation_strategy: ``CfnComputeEnvironment.ComputeResourcesProperty.AllocationStrategy``.
            :param bid_percentage: ``CfnComputeEnvironment.ComputeResourcesProperty.BidPercentage``.
            :param desiredv_cpus: ``CfnComputeEnvironment.ComputeResourcesProperty.DesiredvCpus``.
            :param ec2_key_pair: ``CfnComputeEnvironment.ComputeResourcesProperty.Ec2KeyPair``.
            :param image_id: ``CfnComputeEnvironment.ComputeResourcesProperty.ImageId``.
            :param launch_template: ``CfnComputeEnvironment.ComputeResourcesProperty.LaunchTemplate``.
            :param placement_group: ``CfnComputeEnvironment.ComputeResourcesProperty.PlacementGroup``.
            :param security_group_ids: ``CfnComputeEnvironment.ComputeResourcesProperty.SecurityGroupIds``.
            :param spot_iam_fleet_role: ``CfnComputeEnvironment.ComputeResourcesProperty.SpotIamFleetRole``.
            :param tags: ``CfnComputeEnvironment.ComputeResourcesProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "instance_role": instance_role,
                "instance_types": instance_types,
                "maxv_cpus": maxv_cpus,
                "minv_cpus": minv_cpus,
                "subnets": subnets,
                "type": type,
            }
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if bid_percentage is not None:
                self._values["bid_percentage"] = bid_percentage
            if desiredv_cpus is not None:
                self._values["desiredv_cpus"] = desiredv_cpus
            if ec2_key_pair is not None:
                self._values["ec2_key_pair"] = ec2_key_pair
            if image_id is not None:
                self._values["image_id"] = image_id
            if launch_template is not None:
                self._values["launch_template"] = launch_template
            if placement_group is not None:
                self._values["placement_group"] = placement_group
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if spot_iam_fleet_role is not None:
                self._values["spot_iam_fleet_role"] = spot_iam_fleet_role
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def instance_role(self) -> builtins.str:
            """``CfnComputeEnvironment.ComputeResourcesProperty.InstanceRole``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole
            """
            result = self._values.get("instance_role")
            assert result is not None, "Required property 'instance_role' is missing"
            return result

        @builtins.property
        def instance_types(self) -> typing.List[builtins.str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.InstanceTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes
            """
            result = self._values.get("instance_types")
            assert result is not None, "Required property 'instance_types' is missing"
            return result

        @builtins.property
        def maxv_cpus(self) -> jsii.Number:
            """``CfnComputeEnvironment.ComputeResourcesProperty.MaxvCpus``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus
            """
            result = self._values.get("maxv_cpus")
            assert result is not None, "Required property 'maxv_cpus' is missing"
            return result

        @builtins.property
        def minv_cpus(self) -> jsii.Number:
            """``CfnComputeEnvironment.ComputeResourcesProperty.MinvCpus``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus
            """
            result = self._values.get("minv_cpus")
            assert result is not None, "Required property 'minv_cpus' is missing"
            return result

        @builtins.property
        def subnets(self) -> typing.List[builtins.str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Subnets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets
            """
            result = self._values.get("subnets")
            assert result is not None, "Required property 'subnets' is missing"
            return result

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.AllocationStrategy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy
            """
            result = self._values.get("allocation_strategy")
            return result

        @builtins.property
        def bid_percentage(self) -> typing.Optional[jsii.Number]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.BidPercentage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage
            """
            result = self._values.get("bid_percentage")
            return result

        @builtins.property
        def desiredv_cpus(self) -> typing.Optional[jsii.Number]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.DesiredvCpus``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-desiredvcpus
            """
            result = self._values.get("desiredv_cpus")
            return result

        @builtins.property
        def ec2_key_pair(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Ec2KeyPair``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair
            """
            result = self._values.get("ec2_key_pair")
            return result

        @builtins.property
        def image_id(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.ImageId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid
            """
            result = self._values.get("image_id")
            return result

        @builtins.property
        def launch_template(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComputeEnvironment.LaunchTemplateSpecificationProperty"]]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.LaunchTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate
            """
            result = self._values.get("launch_template")
            return result

        @builtins.property
        def placement_group(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.PlacementGroup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup
            """
            result = self._values.get("placement_group")
            return result

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.SecurityGroupIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def spot_iam_fleet_role(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.ComputeResourcesProperty.SpotIamFleetRole``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-spotiamfleetrole
            """
            result = self._values.get("spot_iam_fleet_role")
            return result

        @builtins.property
        def tags(self) -> typing.Any:
            """``CfnComputeEnvironment.ComputeResourcesProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags
            """
            result = self._values.get("tags")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "version": "version",
        },
    )
    class LaunchTemplateSpecificationProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param launch_template_id: ``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateId``.
            :param launch_template_name: ``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateName``.
            :param version: ``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplateid
            """
            result = self._values.get("launch_template_id")
            return result

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplatename
            """
            result = self._values.get("launch_template_name")
            return result

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            """``CfnComputeEnvironment.LaunchTemplateSpecificationProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-version
            """
            result = self._values.get("version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "service_role": "serviceRole",
        "type": "type",
        "compute_environment_name": "computeEnvironmentName",
        "compute_resources": "computeResources",
        "state": "state",
        "tags": "tags",
    },
)
class CfnComputeEnvironmentProps:
    def __init__(
        self,
        *,
        service_role: builtins.str,
        type: builtins.str,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnComputeEnvironment.ComputeResourcesProperty]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::Batch::ComputeEnvironment``.

        :param service_role: ``AWS::Batch::ComputeEnvironment.ServiceRole``.
        :param type: ``AWS::Batch::ComputeEnvironment.Type``.
        :param compute_environment_name: ``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.
        :param compute_resources: ``AWS::Batch::ComputeEnvironment.ComputeResources``.
        :param state: ``AWS::Batch::ComputeEnvironment.State``.
        :param tags: ``AWS::Batch::ComputeEnvironment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "service_role": service_role,
            "type": type,
        }
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if compute_resources is not None:
            self._values["compute_resources"] = compute_resources
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def service_role(self) -> builtins.str:
        """``AWS::Batch::ComputeEnvironment.ServiceRole``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole
        """
        result = self._values.get("service_role")
        assert result is not None, "Required property 'service_role' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::Batch::ComputeEnvironment.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::ComputeEnvironment.ComputeEnvironmentName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeenvironmentname
        """
        result = self._values.get("compute_environment_name")
        return result

    @builtins.property
    def compute_resources(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnComputeEnvironment.ComputeResourcesProperty]]:
        """``AWS::Batch::ComputeEnvironment.ComputeResources``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeresources
        """
        result = self._values.get("compute_resources")
        return result

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::ComputeEnvironment.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-state
        """
        result = self._values.get("state")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Batch::ComputeEnvironment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnJobDefinition(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.CfnJobDefinition",
):
    """A CloudFormation ``AWS::Batch::JobDefinition``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
    :cloudformationResource: AWS::Batch::JobDefinition
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        type: builtins.str,
        container_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        node_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.NodePropertiesProperty"]] = None,
        parameters: typing.Any = None,
        retry_strategy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.RetryStrategyProperty"]] = None,
        tags: typing.Any = None,
        timeout: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.TimeoutProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::Batch::JobDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: ``AWS::Batch::JobDefinition.Type``.
        :param container_properties: ``AWS::Batch::JobDefinition.ContainerProperties``.
        :param job_definition_name: ``AWS::Batch::JobDefinition.JobDefinitionName``.
        :param node_properties: ``AWS::Batch::JobDefinition.NodeProperties``.
        :param parameters: ``AWS::Batch::JobDefinition.Parameters``.
        :param retry_strategy: ``AWS::Batch::JobDefinition.RetryStrategy``.
        :param tags: ``AWS::Batch::JobDefinition.Tags``.
        :param timeout: ``AWS::Batch::JobDefinition.Timeout``.
        """
        props = CfnJobDefinitionProps(
            type=type,
            container_properties=container_properties,
            job_definition_name=job_definition_name,
            node_properties=node_properties,
            parameters=parameters,
            retry_strategy=retry_strategy,
            tags=tags,
            timeout=timeout,
        )

        jsii.create(CfnJobDefinition, self, [scope, id, props])

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
        """``AWS::Batch::JobDefinition.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        """``AWS::Batch::JobDefinition.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter # type: ignore
    def parameters(self, value: typing.Any) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::Batch::JobDefinition.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="containerProperties")
    def container_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]]:
        """``AWS::Batch::JobDefinition.ContainerProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-containerproperties
        """
        return jsii.get(self, "containerProperties")

    @container_properties.setter # type: ignore
    def container_properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]],
    ) -> None:
        jsii.set(self, "containerProperties", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::JobDefinition.JobDefinitionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-jobdefinitionname
        """
        return jsii.get(self, "jobDefinitionName")

    @job_definition_name.setter # type: ignore
    def job_definition_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "jobDefinitionName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="nodeProperties")
    def node_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.NodePropertiesProperty"]]:
        """``AWS::Batch::JobDefinition.NodeProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-nodeproperties
        """
        return jsii.get(self, "nodeProperties")

    @node_properties.setter # type: ignore
    def node_properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.NodePropertiesProperty"]],
    ) -> None:
        jsii.set(self, "nodeProperties", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="retryStrategy")
    def retry_strategy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.RetryStrategyProperty"]]:
        """``AWS::Batch::JobDefinition.RetryStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-retrystrategy
        """
        return jsii.get(self, "retryStrategy")

    @retry_strategy.setter # type: ignore
    def retry_strategy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.RetryStrategyProperty"]],
    ) -> None:
        jsii.set(self, "retryStrategy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeout")
    def timeout(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.TimeoutProperty"]]:
        """``AWS::Batch::JobDefinition.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter # type: ignore
    def timeout(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.TimeoutProperty"]],
    ) -> None:
        jsii.set(self, "timeout", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ContainerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image": "image",
            "command": "command",
            "environment": "environment",
            "execution_role_arn": "executionRoleArn",
            "instance_type": "instanceType",
            "job_role_arn": "jobRoleArn",
            "linux_parameters": "linuxParameters",
            "log_configuration": "logConfiguration",
            "memory": "memory",
            "mount_points": "mountPoints",
            "privileged": "privileged",
            "readonly_root_filesystem": "readonlyRootFilesystem",
            "resource_requirements": "resourceRequirements",
            "secrets": "secrets",
            "ulimits": "ulimits",
            "user": "user",
            "vcpus": "vcpus",
            "volumes": "volumes",
        },
    )
    class ContainerPropertiesProperty:
        def __init__(
            self,
            *,
            image: builtins.str,
            command: typing.Optional[typing.List[builtins.str]] = None,
            environment: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.EnvironmentProperty"]]]] = None,
            execution_role_arn: typing.Optional[builtins.str] = None,
            instance_type: typing.Optional[builtins.str] = None,
            job_role_arn: typing.Optional[builtins.str] = None,
            linux_parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.LinuxParametersProperty"]] = None,
            log_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.LogConfigurationProperty"]] = None,
            memory: typing.Optional[jsii.Number] = None,
            mount_points: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.MountPointsProperty"]]]] = None,
            privileged: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            readonly_root_filesystem: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            resource_requirements: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ResourceRequirementProperty"]]]] = None,
            secrets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.SecretProperty"]]]] = None,
            ulimits: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.UlimitProperty"]]]] = None,
            user: typing.Optional[builtins.str] = None,
            vcpus: typing.Optional[jsii.Number] = None,
            volumes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.VolumesProperty"]]]] = None,
        ) -> None:
            """
            :param image: ``CfnJobDefinition.ContainerPropertiesProperty.Image``.
            :param command: ``CfnJobDefinition.ContainerPropertiesProperty.Command``.
            :param environment: ``CfnJobDefinition.ContainerPropertiesProperty.Environment``.
            :param execution_role_arn: ``CfnJobDefinition.ContainerPropertiesProperty.ExecutionRoleArn``.
            :param instance_type: ``CfnJobDefinition.ContainerPropertiesProperty.InstanceType``.
            :param job_role_arn: ``CfnJobDefinition.ContainerPropertiesProperty.JobRoleArn``.
            :param linux_parameters: ``CfnJobDefinition.ContainerPropertiesProperty.LinuxParameters``.
            :param log_configuration: ``CfnJobDefinition.ContainerPropertiesProperty.LogConfiguration``.
            :param memory: ``CfnJobDefinition.ContainerPropertiesProperty.Memory``.
            :param mount_points: ``CfnJobDefinition.ContainerPropertiesProperty.MountPoints``.
            :param privileged: ``CfnJobDefinition.ContainerPropertiesProperty.Privileged``.
            :param readonly_root_filesystem: ``CfnJobDefinition.ContainerPropertiesProperty.ReadonlyRootFilesystem``.
            :param resource_requirements: ``CfnJobDefinition.ContainerPropertiesProperty.ResourceRequirements``.
            :param secrets: ``CfnJobDefinition.ContainerPropertiesProperty.Secrets``.
            :param ulimits: ``CfnJobDefinition.ContainerPropertiesProperty.Ulimits``.
            :param user: ``CfnJobDefinition.ContainerPropertiesProperty.User``.
            :param vcpus: ``CfnJobDefinition.ContainerPropertiesProperty.Vcpus``.
            :param volumes: ``CfnJobDefinition.ContainerPropertiesProperty.Volumes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "image": image,
            }
            if command is not None:
                self._values["command"] = command
            if environment is not None:
                self._values["environment"] = environment
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if job_role_arn is not None:
                self._values["job_role_arn"] = job_role_arn
            if linux_parameters is not None:
                self._values["linux_parameters"] = linux_parameters
            if log_configuration is not None:
                self._values["log_configuration"] = log_configuration
            if memory is not None:
                self._values["memory"] = memory
            if mount_points is not None:
                self._values["mount_points"] = mount_points
            if privileged is not None:
                self._values["privileged"] = privileged
            if readonly_root_filesystem is not None:
                self._values["readonly_root_filesystem"] = readonly_root_filesystem
            if resource_requirements is not None:
                self._values["resource_requirements"] = resource_requirements
            if secrets is not None:
                self._values["secrets"] = secrets
            if ulimits is not None:
                self._values["ulimits"] = ulimits
            if user is not None:
                self._values["user"] = user
            if vcpus is not None:
                self._values["vcpus"] = vcpus
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def image(self) -> builtins.str:
            """``CfnJobDefinition.ContainerPropertiesProperty.Image``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-image
            """
            result = self._values.get("image")
            assert result is not None, "Required property 'image' is missing"
            return result

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Command``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-command
            """
            result = self._values.get("command")
            return result

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.EnvironmentProperty"]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Environment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-environment
            """
            result = self._values.get("environment")
            return result

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.ContainerPropertiesProperty.ExecutionRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-executionrolearn
            """
            result = self._values.get("execution_role_arn")
            return result

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.ContainerPropertiesProperty.InstanceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-instancetype
            """
            result = self._values.get("instance_type")
            return result

        @builtins.property
        def job_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.ContainerPropertiesProperty.JobRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-jobrolearn
            """
            result = self._values.get("job_role_arn")
            return result

        @builtins.property
        def linux_parameters(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.LinuxParametersProperty"]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.LinuxParameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-linuxparameters
            """
            result = self._values.get("linux_parameters")
            return result

        @builtins.property
        def log_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.LogConfigurationProperty"]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.LogConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-logconfiguration
            """
            result = self._values.get("log_configuration")
            return result

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Memory``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-memory
            """
            result = self._values.get("memory")
            return result

        @builtins.property
        def mount_points(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.MountPointsProperty"]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.MountPoints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-mountpoints
            """
            result = self._values.get("mount_points")
            return result

        @builtins.property
        def privileged(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Privileged``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-privileged
            """
            result = self._values.get("privileged")
            return result

        @builtins.property
        def readonly_root_filesystem(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.ReadonlyRootFilesystem``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-readonlyrootfilesystem
            """
            result = self._values.get("readonly_root_filesystem")
            return result

        @builtins.property
        def resource_requirements(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ResourceRequirementProperty"]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.ResourceRequirements``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-resourcerequirements
            """
            result = self._values.get("resource_requirements")
            return result

        @builtins.property
        def secrets(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.SecretProperty"]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Secrets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-secrets
            """
            result = self._values.get("secrets")
            return result

        @builtins.property
        def ulimits(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.UlimitProperty"]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Ulimits``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-ulimits
            """
            result = self._values.get("ulimits")
            return result

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.ContainerPropertiesProperty.User``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-user
            """
            result = self._values.get("user")
            return result

        @builtins.property
        def vcpus(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Vcpus``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-vcpus
            """
            result = self._values.get("vcpus")
            return result

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.VolumesProperty"]]]]:
            """``CfnJobDefinition.ContainerPropertiesProperty.Volumes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-volumes
            """
            result = self._values.get("volumes")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.DeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "host_path": "hostPath",
            "permissions": "permissions",
        },
    )
    class DeviceProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            host_path: typing.Optional[builtins.str] = None,
            permissions: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param container_path: ``CfnJobDefinition.DeviceProperty.ContainerPath``.
            :param host_path: ``CfnJobDefinition.DeviceProperty.HostPath``.
            :param permissions: ``CfnJobDefinition.DeviceProperty.Permissions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if host_path is not None:
                self._values["host_path"] = host_path
            if permissions is not None:
                self._values["permissions"] = permissions

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.DeviceProperty.ContainerPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-containerpath
            """
            result = self._values.get("container_path")
            return result

        @builtins.property
        def host_path(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.DeviceProperty.HostPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-hostpath
            """
            result = self._values.get("host_path")
            return result

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnJobDefinition.DeviceProperty.Permissions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-permissions
            """
            result = self._values.get("permissions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param name: ``CfnJobDefinition.EnvironmentProperty.Name``.
            :param value: ``CfnJobDefinition.EnvironmentProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.EnvironmentProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.EnvironmentProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EvaluateOnExitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "on_exit_code": "onExitCode",
            "on_reason": "onReason",
            "on_status_reason": "onStatusReason",
        },
    )
    class EvaluateOnExitProperty:
        def __init__(
            self,
            *,
            action: builtins.str,
            on_exit_code: typing.Optional[builtins.str] = None,
            on_reason: typing.Optional[builtins.str] = None,
            on_status_reason: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param action: ``CfnJobDefinition.EvaluateOnExitProperty.Action``.
            :param on_exit_code: ``CfnJobDefinition.EvaluateOnExitProperty.OnExitCode``.
            :param on_reason: ``CfnJobDefinition.EvaluateOnExitProperty.OnReason``.
            :param on_status_reason: ``CfnJobDefinition.EvaluateOnExitProperty.OnStatusReason``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
            }
            if on_exit_code is not None:
                self._values["on_exit_code"] = on_exit_code
            if on_reason is not None:
                self._values["on_reason"] = on_reason
            if on_status_reason is not None:
                self._values["on_status_reason"] = on_status_reason

        @builtins.property
        def action(self) -> builtins.str:
            """``CfnJobDefinition.EvaluateOnExitProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-action
            """
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return result

        @builtins.property
        def on_exit_code(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.EvaluateOnExitProperty.OnExitCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onexitcode
            """
            result = self._values.get("on_exit_code")
            return result

        @builtins.property
        def on_reason(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.EvaluateOnExitProperty.OnReason``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onreason
            """
            result = self._values.get("on_reason")
            return result

        @builtins.property
        def on_status_reason(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.EvaluateOnExitProperty.OnStatusReason``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onstatusreason
            """
            result = self._values.get("on_status_reason")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluateOnExitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.LinuxParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "devices": "devices",
            "init_process_enabled": "initProcessEnabled",
            "max_swap": "maxSwap",
            "shared_memory_size": "sharedMemorySize",
            "swappiness": "swappiness",
            "tmpfs": "tmpfs",
        },
    )
    class LinuxParametersProperty:
        def __init__(
            self,
            *,
            devices: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.DeviceProperty"]]]] = None,
            init_process_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            max_swap: typing.Optional[jsii.Number] = None,
            shared_memory_size: typing.Optional[jsii.Number] = None,
            swappiness: typing.Optional[jsii.Number] = None,
            tmpfs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.TmpfsProperty"]]]] = None,
        ) -> None:
            """
            :param devices: ``CfnJobDefinition.LinuxParametersProperty.Devices``.
            :param init_process_enabled: ``CfnJobDefinition.LinuxParametersProperty.InitProcessEnabled``.
            :param max_swap: ``CfnJobDefinition.LinuxParametersProperty.MaxSwap``.
            :param shared_memory_size: ``CfnJobDefinition.LinuxParametersProperty.SharedMemorySize``.
            :param swappiness: ``CfnJobDefinition.LinuxParametersProperty.Swappiness``.
            :param tmpfs: ``CfnJobDefinition.LinuxParametersProperty.Tmpfs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if devices is not None:
                self._values["devices"] = devices
            if init_process_enabled is not None:
                self._values["init_process_enabled"] = init_process_enabled
            if max_swap is not None:
                self._values["max_swap"] = max_swap
            if shared_memory_size is not None:
                self._values["shared_memory_size"] = shared_memory_size
            if swappiness is not None:
                self._values["swappiness"] = swappiness
            if tmpfs is not None:
                self._values["tmpfs"] = tmpfs

        @builtins.property
        def devices(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.DeviceProperty"]]]]:
            """``CfnJobDefinition.LinuxParametersProperty.Devices``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-devices
            """
            result = self._values.get("devices")
            return result

        @builtins.property
        def init_process_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnJobDefinition.LinuxParametersProperty.InitProcessEnabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-initprocessenabled
            """
            result = self._values.get("init_process_enabled")
            return result

        @builtins.property
        def max_swap(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.LinuxParametersProperty.MaxSwap``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-maxswap
            """
            result = self._values.get("max_swap")
            return result

        @builtins.property
        def shared_memory_size(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.LinuxParametersProperty.SharedMemorySize``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-sharedmemorysize
            """
            result = self._values.get("shared_memory_size")
            return result

        @builtins.property
        def swappiness(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.LinuxParametersProperty.Swappiness``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-swappiness
            """
            result = self._values.get("swappiness")
            return result

        @builtins.property
        def tmpfs(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.TmpfsProperty"]]]]:
            """``CfnJobDefinition.LinuxParametersProperty.Tmpfs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-tmpfs
            """
            result = self._values.get("tmpfs")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinuxParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_driver": "logDriver",
            "options": "options",
            "secret_options": "secretOptions",
        },
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_driver: builtins.str,
            options: typing.Any = None,
            secret_options: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.SecretProperty"]]]] = None,
        ) -> None:
            """
            :param log_driver: ``CfnJobDefinition.LogConfigurationProperty.LogDriver``.
            :param options: ``CfnJobDefinition.LogConfigurationProperty.Options``.
            :param secret_options: ``CfnJobDefinition.LogConfigurationProperty.SecretOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "log_driver": log_driver,
            }
            if options is not None:
                self._values["options"] = options
            if secret_options is not None:
                self._values["secret_options"] = secret_options

        @builtins.property
        def log_driver(self) -> builtins.str:
            """``CfnJobDefinition.LogConfigurationProperty.LogDriver``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html#cfn-batch-jobdefinition-containerproperties-logconfiguration-logdriver
            """
            result = self._values.get("log_driver")
            assert result is not None, "Required property 'log_driver' is missing"
            return result

        @builtins.property
        def options(self) -> typing.Any:
            """``CfnJobDefinition.LogConfigurationProperty.Options``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html#cfn-batch-jobdefinition-containerproperties-logconfiguration-options
            """
            result = self._values.get("options")
            return result

        @builtins.property
        def secret_options(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.SecretProperty"]]]]:
            """``CfnJobDefinition.LogConfigurationProperty.SecretOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html#cfn-batch-jobdefinition-containerproperties-logconfiguration-secretoptions
            """
            result = self._values.get("secret_options")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.MountPointsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "read_only": "readOnly",
            "source_volume": "sourceVolume",
        },
    )
    class MountPointsProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            source_volume: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param container_path: ``CfnJobDefinition.MountPointsProperty.ContainerPath``.
            :param read_only: ``CfnJobDefinition.MountPointsProperty.ReadOnly``.
            :param source_volume: ``CfnJobDefinition.MountPointsProperty.SourceVolume``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if read_only is not None:
                self._values["read_only"] = read_only
            if source_volume is not None:
                self._values["source_volume"] = source_volume

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.MountPointsProperty.ContainerPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-containerpath
            """
            result = self._values.get("container_path")
            return result

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnJobDefinition.MountPointsProperty.ReadOnly``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-readonly
            """
            result = self._values.get("read_only")
            return result

        @builtins.property
        def source_volume(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.MountPointsProperty.SourceVolume``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-sourcevolume
            """
            result = self._values.get("source_volume")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountPointsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "main_node": "mainNode",
            "node_range_properties": "nodeRangeProperties",
            "num_nodes": "numNodes",
        },
    )
    class NodePropertiesProperty:
        def __init__(
            self,
            *,
            main_node: jsii.Number,
            node_range_properties: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.NodeRangePropertyProperty"]]],
            num_nodes: jsii.Number,
        ) -> None:
            """
            :param main_node: ``CfnJobDefinition.NodePropertiesProperty.MainNode``.
            :param node_range_properties: ``CfnJobDefinition.NodePropertiesProperty.NodeRangeProperties``.
            :param num_nodes: ``CfnJobDefinition.NodePropertiesProperty.NumNodes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "main_node": main_node,
                "node_range_properties": node_range_properties,
                "num_nodes": num_nodes,
            }

        @builtins.property
        def main_node(self) -> jsii.Number:
            """``CfnJobDefinition.NodePropertiesProperty.MainNode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-mainnode
            """
            result = self._values.get("main_node")
            assert result is not None, "Required property 'main_node' is missing"
            return result

        @builtins.property
        def node_range_properties(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.NodeRangePropertyProperty"]]]:
            """``CfnJobDefinition.NodePropertiesProperty.NodeRangeProperties``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-noderangeproperties
            """
            result = self._values.get("node_range_properties")
            assert result is not None, "Required property 'node_range_properties' is missing"
            return result

        @builtins.property
        def num_nodes(self) -> jsii.Number:
            """``CfnJobDefinition.NodePropertiesProperty.NumNodes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-numnodes
            """
            result = self._values.get("num_nodes")
            assert result is not None, "Required property 'num_nodes' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodeRangePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"target_nodes": "targetNodes", "container": "container"},
    )
    class NodeRangePropertyProperty:
        def __init__(
            self,
            *,
            target_nodes: builtins.str,
            container: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]] = None,
        ) -> None:
            """
            :param target_nodes: ``CfnJobDefinition.NodeRangePropertyProperty.TargetNodes``.
            :param container: ``CfnJobDefinition.NodeRangePropertyProperty.Container``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "target_nodes": target_nodes,
            }
            if container is not None:
                self._values["container"] = container

        @builtins.property
        def target_nodes(self) -> builtins.str:
            """``CfnJobDefinition.NodeRangePropertyProperty.TargetNodes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-targetnodes
            """
            result = self._values.get("target_nodes")
            assert result is not None, "Required property 'target_nodes' is missing"
            return result

        @builtins.property
        def container(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]]:
            """``CfnJobDefinition.NodeRangePropertyProperty.Container``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-container
            """
            result = self._values.get("container")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeRangePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ResourceRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ResourceRequirementProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param type: ``CfnJobDefinition.ResourceRequirementProperty.Type``.
            :param value: ``CfnJobDefinition.ResourceRequirementProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.ResourceRequirementProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-type
            """
            result = self._values.get("type")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.ResourceRequirementProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.RetryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"attempts": "attempts", "evaluate_on_exit": "evaluateOnExit"},
    )
    class RetryStrategyProperty:
        def __init__(
            self,
            *,
            attempts: typing.Optional[jsii.Number] = None,
            evaluate_on_exit: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.EvaluateOnExitProperty"]]]] = None,
        ) -> None:
            """
            :param attempts: ``CfnJobDefinition.RetryStrategyProperty.Attempts``.
            :param evaluate_on_exit: ``CfnJobDefinition.RetryStrategyProperty.EvaluateOnExit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attempts is not None:
                self._values["attempts"] = attempts
            if evaluate_on_exit is not None:
                self._values["evaluate_on_exit"] = evaluate_on_exit

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.RetryStrategyProperty.Attempts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html#cfn-batch-jobdefinition-retrystrategy-attempts
            """
            result = self._values.get("attempts")
            return result

        @builtins.property
        def evaluate_on_exit(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.EvaluateOnExitProperty"]]]]:
            """``CfnJobDefinition.RetryStrategyProperty.EvaluateOnExit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html#cfn-batch-jobdefinition-retrystrategy-evaluateonexit
            """
            result = self._values.get("evaluate_on_exit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.SecretProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value_from": "valueFrom"},
    )
    class SecretProperty:
        def __init__(self, *, name: builtins.str, value_from: builtins.str) -> None:
            """
            :param name: ``CfnJobDefinition.SecretProperty.Name``.
            :param value_from: ``CfnJobDefinition.SecretProperty.ValueFrom``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value_from": value_from,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnJobDefinition.SecretProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html#cfn-batch-jobdefinition-secret-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def value_from(self) -> builtins.str:
            """``CfnJobDefinition.SecretProperty.ValueFrom``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html#cfn-batch-jobdefinition-secret-valuefrom
            """
            result = self._values.get("value_from")
            assert result is not None, "Required property 'value_from' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.TimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"attempt_duration_seconds": "attemptDurationSeconds"},
    )
    class TimeoutProperty:
        def __init__(
            self,
            *,
            attempt_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param attempt_duration_seconds: ``CfnJobDefinition.TimeoutProperty.AttemptDurationSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attempt_duration_seconds is not None:
                self._values["attempt_duration_seconds"] = attempt_duration_seconds

        @builtins.property
        def attempt_duration_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnJobDefinition.TimeoutProperty.AttemptDurationSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html#cfn-batch-jobdefinition-timeout-attemptdurationseconds
            """
            result = self._values.get("attempt_duration_seconds")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.TmpfsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "size": "size",
            "mount_options": "mountOptions",
        },
    )
    class TmpfsProperty:
        def __init__(
            self,
            *,
            container_path: builtins.str,
            size: jsii.Number,
            mount_options: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param container_path: ``CfnJobDefinition.TmpfsProperty.ContainerPath``.
            :param size: ``CfnJobDefinition.TmpfsProperty.Size``.
            :param mount_options: ``CfnJobDefinition.TmpfsProperty.MountOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "container_path": container_path,
                "size": size,
            }
            if mount_options is not None:
                self._values["mount_options"] = mount_options

        @builtins.property
        def container_path(self) -> builtins.str:
            """``CfnJobDefinition.TmpfsProperty.ContainerPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-containerpath
            """
            result = self._values.get("container_path")
            assert result is not None, "Required property 'container_path' is missing"
            return result

        @builtins.property
        def size(self) -> jsii.Number:
            """``CfnJobDefinition.TmpfsProperty.Size``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-size
            """
            result = self._values.get("size")
            assert result is not None, "Required property 'size' is missing"
            return result

        @builtins.property
        def mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnJobDefinition.TmpfsProperty.MountOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-mountoptions
            """
            result = self._values.get("mount_options")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TmpfsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.UlimitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hard_limit": "hardLimit",
            "name": "name",
            "soft_limit": "softLimit",
        },
    )
    class UlimitProperty:
        def __init__(
            self,
            *,
            hard_limit: jsii.Number,
            name: builtins.str,
            soft_limit: jsii.Number,
        ) -> None:
            """
            :param hard_limit: ``CfnJobDefinition.UlimitProperty.HardLimit``.
            :param name: ``CfnJobDefinition.UlimitProperty.Name``.
            :param soft_limit: ``CfnJobDefinition.UlimitProperty.SoftLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "hard_limit": hard_limit,
                "name": name,
                "soft_limit": soft_limit,
            }

        @builtins.property
        def hard_limit(self) -> jsii.Number:
            """``CfnJobDefinition.UlimitProperty.HardLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-hardlimit
            """
            result = self._values.get("hard_limit")
            assert result is not None, "Required property 'hard_limit' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnJobDefinition.UlimitProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def soft_limit(self) -> jsii.Number:
            """``CfnJobDefinition.UlimitProperty.SoftLimit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-softlimit
            """
            result = self._values.get("soft_limit")
            assert result is not None, "Required property 'soft_limit' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UlimitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesHostProperty",
        jsii_struct_bases=[],
        name_mapping={"source_path": "sourcePath"},
    )
    class VolumesHostProperty:
        def __init__(
            self,
            *,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param source_path: ``CfnJobDefinition.VolumesHostProperty.SourcePath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.VolumesHostProperty.SourcePath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html#cfn-batch-jobdefinition-volumeshost-sourcepath
            """
            result = self._values.get("source_path")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumesHostProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesProperty",
        jsii_struct_bases=[],
        name_mapping={"host": "host", "name": "name"},
    )
    class VolumesProperty:
        def __init__(
            self,
            *,
            host: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.VolumesHostProperty"]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param host: ``CfnJobDefinition.VolumesProperty.Host``.
            :param name: ``CfnJobDefinition.VolumesProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if host is not None:
                self._values["host"] = host
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def host(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnJobDefinition.VolumesHostProperty"]]:
            """``CfnJobDefinition.VolumesProperty.Host``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-host
            """
            result = self._values.get("host")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnJobDefinition.VolumesProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-name
            """
            result = self._values.get("name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.CfnJobDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "container_properties": "containerProperties",
        "job_definition_name": "jobDefinitionName",
        "node_properties": "nodeProperties",
        "parameters": "parameters",
        "retry_strategy": "retryStrategy",
        "tags": "tags",
        "timeout": "timeout",
    },
)
class CfnJobDefinitionProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        container_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.ContainerPropertiesProperty]] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        node_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.NodePropertiesProperty]] = None,
        parameters: typing.Any = None,
        retry_strategy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.RetryStrategyProperty]] = None,
        tags: typing.Any = None,
        timeout: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.TimeoutProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Batch::JobDefinition``.

        :param type: ``AWS::Batch::JobDefinition.Type``.
        :param container_properties: ``AWS::Batch::JobDefinition.ContainerProperties``.
        :param job_definition_name: ``AWS::Batch::JobDefinition.JobDefinitionName``.
        :param node_properties: ``AWS::Batch::JobDefinition.NodeProperties``.
        :param parameters: ``AWS::Batch::JobDefinition.Parameters``.
        :param retry_strategy: ``AWS::Batch::JobDefinition.RetryStrategy``.
        :param tags: ``AWS::Batch::JobDefinition.Tags``.
        :param timeout: ``AWS::Batch::JobDefinition.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if container_properties is not None:
            self._values["container_properties"] = container_properties
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if node_properties is not None:
            self._values["node_properties"] = node_properties
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::Batch::JobDefinition.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def container_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.ContainerPropertiesProperty]]:
        """``AWS::Batch::JobDefinition.ContainerProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-containerproperties
        """
        result = self._values.get("container_properties")
        return result

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::JobDefinition.JobDefinitionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-jobdefinitionname
        """
        result = self._values.get("job_definition_name")
        return result

    @builtins.property
    def node_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.NodePropertiesProperty]]:
        """``AWS::Batch::JobDefinition.NodeProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-nodeproperties
        """
        result = self._values.get("node_properties")
        return result

    @builtins.property
    def parameters(self) -> typing.Any:
        """``AWS::Batch::JobDefinition.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-parameters
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def retry_strategy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.RetryStrategyProperty]]:
        """``AWS::Batch::JobDefinition.RetryStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-retrystrategy
        """
        result = self._values.get("retry_strategy")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Batch::JobDefinition.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def timeout(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnJobDefinition.TimeoutProperty]]:
        """``AWS::Batch::JobDefinition.Timeout``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-timeout
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnJobQueue(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.CfnJobQueue",
):
    """A CloudFormation ``AWS::Batch::JobQueue``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
    :cloudformationResource: AWS::Batch::JobQueue
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        compute_environment_order: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnJobQueue.ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]],
        priority: jsii.Number,
        job_queue_name: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::Batch::JobQueue``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compute_environment_order: ``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.
        :param priority: ``AWS::Batch::JobQueue.Priority``.
        :param job_queue_name: ``AWS::Batch::JobQueue.JobQueueName``.
        :param state: ``AWS::Batch::JobQueue.State``.
        :param tags: ``AWS::Batch::JobQueue.Tags``.
        """
        props = CfnJobQueueProps(
            compute_environment_order=compute_environment_order,
            priority=priority,
            job_queue_name=job_queue_name,
            state=state,
            tags=tags,
        )

        jsii.create(CfnJobQueue, self, [scope, id, props])

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
        """``AWS::Batch::JobQueue.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentOrder")
    def compute_environment_order(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnJobQueue.ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-computeenvironmentorder
        """
        return jsii.get(self, "computeEnvironmentOrder")

    @compute_environment_order.setter # type: ignore
    def compute_environment_order(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnJobQueue.ComputeEnvironmentOrderProperty", aws_cdk.core.IResolvable]]],
    ) -> None:
        jsii.set(self, "computeEnvironmentOrder", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        """``AWS::Batch::JobQueue.Priority``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-priority
        """
        return jsii.get(self, "priority")

    @priority.setter # type: ignore
    def priority(self, value: jsii.Number) -> None:
        jsii.set(self, "priority", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::JobQueue.JobQueueName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuename
        """
        return jsii.get(self, "jobQueueName")

    @job_queue_name.setter # type: ignore
    def job_queue_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "jobQueueName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::JobQueue.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-state
        """
        return jsii.get(self, "state")

    @state.setter # type: ignore
    def state(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "state", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobQueue.ComputeEnvironmentOrderProperty",
        jsii_struct_bases=[],
        name_mapping={"compute_environment": "computeEnvironment", "order": "order"},
    )
    class ComputeEnvironmentOrderProperty:
        def __init__(
            self,
            *,
            compute_environment: builtins.str,
            order: jsii.Number,
        ) -> None:
            """
            :param compute_environment: ``CfnJobQueue.ComputeEnvironmentOrderProperty.ComputeEnvironment``.
            :param order: ``CfnJobQueue.ComputeEnvironmentOrderProperty.Order``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "compute_environment": compute_environment,
                "order": order,
            }

        @builtins.property
        def compute_environment(self) -> builtins.str:
            """``CfnJobQueue.ComputeEnvironmentOrderProperty.ComputeEnvironment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-computeenvironment
            """
            result = self._values.get("compute_environment")
            assert result is not None, "Required property 'compute_environment' is missing"
            return result

        @builtins.property
        def order(self) -> jsii.Number:
            """``CfnJobQueue.ComputeEnvironmentOrderProperty.Order``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-order
            """
            result = self._values.get("order")
            assert result is not None, "Required property 'order' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeEnvironmentOrderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.CfnJobQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environment_order": "computeEnvironmentOrder",
        "priority": "priority",
        "job_queue_name": "jobQueueName",
        "state": "state",
        "tags": "tags",
    },
)
class CfnJobQueueProps:
    def __init__(
        self,
        *,
        compute_environment_order: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnJobQueue.ComputeEnvironmentOrderProperty, aws_cdk.core.IResolvable]]],
        priority: jsii.Number,
        job_queue_name: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::Batch::JobQueue``.

        :param compute_environment_order: ``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.
        :param priority: ``AWS::Batch::JobQueue.Priority``.
        :param job_queue_name: ``AWS::Batch::JobQueue.JobQueueName``.
        :param state: ``AWS::Batch::JobQueue.State``.
        :param tags: ``AWS::Batch::JobQueue.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "compute_environment_order": compute_environment_order,
            "priority": priority,
        }
        if job_queue_name is not None:
            self._values["job_queue_name"] = job_queue_name
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def compute_environment_order(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnJobQueue.ComputeEnvironmentOrderProperty, aws_cdk.core.IResolvable]]]:
        """``AWS::Batch::JobQueue.ComputeEnvironmentOrder``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-computeenvironmentorder
        """
        result = self._values.get("compute_environment_order")
        assert result is not None, "Required property 'compute_environment_order' is missing"
        return result

    @builtins.property
    def priority(self) -> jsii.Number:
        """``AWS::Batch::JobQueue.Priority``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-priority
        """
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return result

    @builtins.property
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::JobQueue.JobQueueName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuename
        """
        result = self._values.get("job_queue_name")
        return result

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::Batch::JobQueue.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-state
        """
        result = self._values.get("state")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Batch::JobQueue.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.ComputeEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "compute_resources": "computeResources",
        "enabled": "enabled",
        "managed": "managed",
        "service_role": "serviceRole",
    },
)
class ComputeEnvironmentProps:
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional["ComputeResources"] = None,
        enabled: typing.Optional[builtins.bool] = None,
        managed: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """(experimental) Properties for creating a new Compute Environment.

        :param compute_environment_name: (experimental) A name for the compute environment. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - CloudFormation-generated name
        :param compute_resources: (experimental) The details of the required compute resources for the managed compute environment. If specified, and this is an unmanaged compute environment, will throw an error. By default, AWS Batch managed compute environments use a recent, approved version of the Amazon ECS-optimized AMI for compute resources. Default: - CloudFormation defaults
        :param enabled: (experimental) The state of the compute environment. If the state is set to true, then the compute environment accepts jobs from a queue and can scale out automatically based on queues. Default: true
        :param managed: (experimental) Determines if AWS should manage the allocation of compute resources for processing jobs. If set to false, then you are in charge of providing the compute resource details. Default: true
        :param service_role: (experimental) The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service. By default, this role is created for you using the AWS managed service policy for Batch. Default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        :stability: experimental
        """
        if isinstance(compute_resources, dict):
            compute_resources = ComputeResources(**compute_resources)
        self._values: typing.Dict[str, typing.Any] = {}
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if compute_resources is not None:
            self._values["compute_resources"] = compute_resources
        if enabled is not None:
            self._values["enabled"] = enabled
        if managed is not None:
            self._values["managed"] = managed
        if service_role is not None:
            self._values["service_role"] = service_role

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A name for the compute environment.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :default: - CloudFormation-generated name

        :stability: experimental
        """
        result = self._values.get("compute_environment_name")
        return result

    @builtins.property
    def compute_resources(self) -> typing.Optional["ComputeResources"]:
        """(experimental) The details of the required compute resources for the managed compute environment.

        If specified, and this is an unmanaged compute environment, will throw an error.

        By default, AWS Batch managed compute environments use a recent, approved version of the
        Amazon ECS-optimized AMI for compute resources.

        :default: - CloudFormation defaults

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html
        """
        result = self._values.get("compute_resources")
        return result

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        """(experimental) The state of the compute environment.

        If the state is set to true, then the compute
        environment accepts jobs from a queue and can scale out automatically based on queues.

        :default: true

        :stability: experimental
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def managed(self) -> typing.Optional[builtins.bool]:
        """(experimental) Determines if AWS should manage the allocation of compute resources for processing jobs.

        If set to false, then you are in charge of providing the compute resource details.

        :default: true

        :stability: experimental
        """
        result = self._values.get("managed")
        return result

    @builtins.property
    def service_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service.

        By default, this role is created for you using
        the AWS managed service policy for Batch.

        :default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html
        """
        result = self._values.get("service_role")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch.ComputeResourceType")
class ComputeResourceType(enum.Enum):
    """(experimental) Property to specify if the compute environment uses On-Demand or SpotFleet compute resources.

    :stability: experimental
    """

    ON_DEMAND = "ON_DEMAND"
    """(experimental) Resources will be EC2 On-Demand resources.

    :stability: experimental
    """
    SPOT = "SPOT"
    """(experimental) Resources will be EC2 SpotFleet resources.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.ComputeResources",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "allocation_strategy": "allocationStrategy",
        "bid_percentage": "bidPercentage",
        "compute_resources_tags": "computeResourcesTags",
        "desiredv_cpus": "desiredvCpus",
        "ec2_key_pair": "ec2KeyPair",
        "image": "image",
        "instance_role": "instanceRole",
        "instance_types": "instanceTypes",
        "launch_template": "launchTemplate",
        "maxv_cpus": "maxvCpus",
        "minv_cpus": "minvCpus",
        "security_groups": "securityGroups",
        "spot_fleet_role": "spotFleetRole",
        "type": "type",
        "vpc_subnets": "vpcSubnets",
    },
)
class ComputeResources:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        allocation_strategy: typing.Optional[AllocationStrategy] = None,
        bid_percentage: typing.Optional[jsii.Number] = None,
        compute_resources_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        desiredv_cpus: typing.Optional[jsii.Number] = None,
        ec2_key_pair: typing.Optional[builtins.str] = None,
        image: typing.Optional[aws_cdk.aws_ec2.IMachineImage] = None,
        instance_role: typing.Optional[builtins.str] = None,
        instance_types: typing.Optional[typing.List[aws_cdk.aws_ec2.InstanceType]] = None,
        launch_template: typing.Optional["LaunchTemplateSpecification"] = None,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        minv_cpus: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        spot_fleet_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        type: typing.Optional[ComputeResourceType] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """(experimental) Properties for defining the structure of the batch compute cluster.

        :param vpc: (experimental) The VPC network that all compute resources will be connected to.
        :param allocation_strategy: (experimental) The allocation strategy to use for the compute resource in case not enough instances of the best fitting instance type can be allocated. This could be due to availability of the instance type in the region or Amazon EC2 service limits. If this is not specified, the default for the EC2 ComputeResourceType is BEST_FIT, which will use only the best fitting instance type, waiting for additional capacity if it's not available. This allocation strategy keeps costs lower but can limit scaling. If you are using Spot Fleets with BEST_FIT then the Spot Fleet IAM Role must be specified. BEST_FIT_PROGRESSIVE will select an additional instance type that is large enough to meet the requirements of the jobs in the queue, with a preference for an instance type with a lower cost. The default value for the SPOT instance type is SPOT_CAPACITY_OPTIMIZED, which is only available for for this type of compute resources and will select an additional instance type that is large enough to meet the requirements of the jobs in the queue, with a preference for an instance type that is less likely to be interrupted. Default: AllocationStrategy.BEST_FIT
        :param bid_percentage: (experimental) This property will be ignored if you set the environment type to ON_DEMAND. The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, then the Spot price must be below 20% of the current On-Demand price for that EC2 instance. You always pay the lowest (market) price and never more than your maximum percentage. If you leave this field empty, the default value is 100% of the On-Demand price. Default: 100
        :param compute_resources_tags: (experimental) Key-value pair tags to be applied to resources that are launched in the compute environment. For AWS Batch, these take the form of "String1": "String2", where String1 is the tag key and String2 is the tag value—for example, { "Name": "AWS Batch Instance - C4OnDemand" }. Default: - no tags will be assigned on compute resources.
        :param desiredv_cpus: (experimental) The desired number of EC2 vCPUS in the compute environment. Default: - no desired vcpu value will be used.
        :param ec2_key_pair: (experimental) The EC2 key pair that is used for instances launched in the compute environment. If no key is defined, then SSH access is not allowed to provisioned compute resources. Default: - no SSH access will be possible.
        :param image: (experimental) The Amazon Machine Image (AMI) ID used for instances launched in the compute environment. Default: - no image will be used.
        :param instance_role: (experimental) The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment. You can specify the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ecsInstanceRole or arn:aws:iam::<aws_account_id>:instance-profile/ecsInstanceRole . For more information, see Amazon ECS Instance Role in the AWS Batch User Guide. Default: - a new role will be created.
        :param instance_types: (experimental) The types of EC2 instances that may be launched in the compute environment. You can specify instance families to launch any instance type within those families (for example, c4 or p3), or you can specify specific sizes within a family (such as c4.8xlarge). You can also choose optimal to pick instance types (from the C, M, and R instance families) on the fly that match the demand of your job queues. Default: optimal
        :param launch_template: (experimental) An optional launch template to associate with your compute resources. For more information, see README file. Default: - no custom launch template will be used
        :param maxv_cpus: (experimental) The maximum number of EC2 vCPUs that an environment can reach. Each vCPU is equivalent to 1,024 CPU shares. You must specify at least one vCPU. Default: 256
        :param minv_cpus: (experimental) The minimum number of EC2 vCPUs that an environment should maintain (even if the compute environment state is DISABLED). Each vCPU is equivalent to 1,024 CPU shares. By keeping this set to 0 you will not have instance time wasted when there is no work to be run. If you set this above zero you will maintain that number of vCPUs at all times. Default: 0
        :param security_groups: (experimental) The EC2 security group(s) associated with instances launched in the compute environment. Default: - AWS default security group.
        :param spot_fleet_role: (experimental) This property will be ignored if you set the environment type to ON_DEMAND. The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a SPOT compute environment. For more information, see Amazon EC2 Spot Fleet Role in the AWS Batch User Guide. Default: - no fleet role will be used.
        :param type: (experimental) The type of compute environment: ON_DEMAND or SPOT. Default: ON_DEMAND
        :param vpc_subnets: (experimental) The VPC subnets into which the compute resources are launched. Default: - private subnets of the supplied VPC.

        :stability: experimental
        """
        if isinstance(launch_template, dict):
            launch_template = LaunchTemplateSpecification(**launch_template)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if allocation_strategy is not None:
            self._values["allocation_strategy"] = allocation_strategy
        if bid_percentage is not None:
            self._values["bid_percentage"] = bid_percentage
        if compute_resources_tags is not None:
            self._values["compute_resources_tags"] = compute_resources_tags
        if desiredv_cpus is not None:
            self._values["desiredv_cpus"] = desiredv_cpus
        if ec2_key_pair is not None:
            self._values["ec2_key_pair"] = ec2_key_pair
        if image is not None:
            self._values["image"] = image
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if maxv_cpus is not None:
            self._values["maxv_cpus"] = maxv_cpus
        if minv_cpus is not None:
            self._values["minv_cpus"] = minv_cpus
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot_fleet_role is not None:
            self._values["spot_fleet_role"] = spot_fleet_role
        if type is not None:
            self._values["type"] = type
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """(experimental) The VPC network that all compute resources will be connected to.

        :stability: experimental
        """
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        """(experimental) The allocation strategy to use for the compute resource in case not enough instances of the best fitting instance type can be allocated.

        This could be due to availability of the instance type in
        the region or Amazon EC2 service limits. If this is not specified, the default for the EC2
        ComputeResourceType is BEST_FIT, which will use only the best fitting instance type, waiting for
        additional capacity if it's not available. This allocation strategy keeps costs lower but can limit
        scaling. If you are using Spot Fleets with BEST_FIT then the Spot Fleet IAM Role must be specified.
        BEST_FIT_PROGRESSIVE will select an additional instance type that is large enough to meet the
        requirements of the jobs in the queue, with a preference for an instance type with a lower cost.
        The default value for the SPOT instance type is SPOT_CAPACITY_OPTIMIZED, which is only available for
        for this type of compute resources and will select an additional instance type that is large enough
        to meet the requirements of the jobs in the queue, with a preference for an instance type that is
        less likely to be interrupted.

        :default: AllocationStrategy.BEST_FIT

        :stability: experimental
        """
        result = self._values.get("allocation_strategy")
        return result

    @builtins.property
    def bid_percentage(self) -> typing.Optional[jsii.Number]:
        """(experimental) This property will be ignored if you set the environment type to ON_DEMAND.

        The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for
        that instance type before instances are launched. For example, if your maximum percentage is 20%,
        then the Spot price must be below 20% of the current On-Demand price for that EC2 instance. You always
        pay the lowest (market) price and never more than your maximum percentage. If you leave this field empty,
        the default value is 100% of the On-Demand price.

        :default: 100

        :stability: experimental
        """
        result = self._values.get("bid_percentage")
        return result

    @builtins.property
    def compute_resources_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Key-value pair tags to be applied to resources that are launched in the compute environment.

        For AWS Batch, these take the form of "String1": "String2", where String1 is the tag key and
        String2 is the tag value—for example, { "Name": "AWS Batch Instance - C4OnDemand" }.

        :default: - no tags will be assigned on compute resources.

        :stability: experimental
        """
        result = self._values.get("compute_resources_tags")
        return result

    @builtins.property
    def desiredv_cpus(self) -> typing.Optional[jsii.Number]:
        """(experimental) The desired number of EC2 vCPUS in the compute environment.

        :default: - no desired vcpu value will be used.

        :stability: experimental
        """
        result = self._values.get("desiredv_cpus")
        return result

    @builtins.property
    def ec2_key_pair(self) -> typing.Optional[builtins.str]:
        """(experimental) The EC2 key pair that is used for instances launched in the compute environment.

        If no key is defined, then SSH access is not allowed to provisioned compute resources.

        :default: - no SSH access will be possible.

        :stability: experimental
        """
        result = self._values.get("ec2_key_pair")
        return result

    @builtins.property
    def image(self) -> typing.Optional[aws_cdk.aws_ec2.IMachineImage]:
        """(experimental) The Amazon Machine Image (AMI) ID used for instances launched in the compute environment.

        :default: - no image will be used.

        :stability: experimental
        """
        result = self._values.get("image")
        return result

    @builtins.property
    def instance_role(self) -> typing.Optional[builtins.str]:
        """(experimental) The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment.

        You can specify
        the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ecsInstanceRole or
        arn:aws:iam::<aws_account_id>:instance-profile/ecsInstanceRole . For more information, see Amazon ECS
        Instance Role in the AWS Batch User Guide.

        :default: - a new role will be created.

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html
        """
        result = self._values.get("instance_role")
        return result

    @builtins.property
    def instance_types(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.InstanceType]]:
        """(experimental) The types of EC2 instances that may be launched in the compute environment.

        You can specify instance
        families to launch any instance type within those families (for example, c4 or p3), or you can specify
        specific sizes within a family (such as c4.8xlarge). You can also choose optimal to pick instance types
        (from the C, M, and R instance families) on the fly that match the demand of your job queues.

        :default: optimal

        :stability: experimental
        """
        result = self._values.get("instance_types")
        return result

    @builtins.property
    def launch_template(self) -> typing.Optional["LaunchTemplateSpecification"]:
        """(experimental) An optional launch template to associate with your compute resources.

        For more information, see README file.

        :default: - no custom launch template will be used

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html
        """
        result = self._values.get("launch_template")
        return result

    @builtins.property
    def maxv_cpus(self) -> typing.Optional[jsii.Number]:
        """(experimental) The maximum number of EC2 vCPUs that an environment can reach.

        Each vCPU is equivalent to
        1,024 CPU shares. You must specify at least one vCPU.

        :default: 256

        :stability: experimental
        """
        result = self._values.get("maxv_cpus")
        return result

    @builtins.property
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        """(experimental) The minimum number of EC2 vCPUs that an environment should maintain (even if the compute environment state is DISABLED).

        Each vCPU is equivalent to 1,024 CPU shares. By keeping this set to 0 you will not have instance time wasted when
        there is no work to be run. If you set this above zero you will maintain that number of vCPUs at all times.

        :default: 0

        :stability: experimental
        """
        result = self._values.get("minv_cpus")
        return result

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """(experimental) The EC2 security group(s) associated with instances launched in the compute environment.

        :default: - AWS default security group.

        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def spot_fleet_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) This property will be ignored if you set the environment type to ON_DEMAND.

        The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a SPOT compute environment.
        For more information, see Amazon EC2 Spot Fleet Role in the AWS Batch User Guide.

        :default: - no fleet role will be used.

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html
        """
        result = self._values.get("spot_fleet_role")
        return result

    @builtins.property
    def type(self) -> typing.Optional[ComputeResourceType]:
        """(experimental) The type of compute environment: ON_DEMAND or SPOT.

        :default: ON_DEMAND

        :stability: experimental
        """
        result = self._values.get("type")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """(experimental) The VPC subnets into which the compute resources are launched.

        :default: - private subnets of the supplied VPC.

        :stability: experimental
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IComputeEnvironment")
class IComputeEnvironment(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Properties of a compute environment.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IComputeEnvironmentProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        """(experimental) The ARN of this compute environment.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        """(experimental) The name of this compute environment.

        :stability: experimental
        :attribute: true
        """
        ...


class _IComputeEnvironmentProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Properties of a compute environment.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IComputeEnvironment"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        """(experimental) The ARN of this compute environment.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "computeEnvironmentArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        """(experimental) The name of this compute environment.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "computeEnvironmentName")


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IJobDefinition")
class IJobDefinition(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) An interface representing a job definition - either a new one, created with the CDK, *using the {@link JobDefinition} class, or existing ones, referenced using the {@link JobDefinition.fromJobDefinitionArn} method.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IJobDefinitionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        """(experimental) The ARN of this batch job definition.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        """(experimental) The name of the batch job definition.

        :stability: experimental
        :attribute: true
        """
        ...


class _IJobDefinitionProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) An interface representing a job definition - either a new one, created with the CDK, *using the {@link JobDefinition} class, or existing ones, referenced using the {@link JobDefinition.fromJobDefinitionArn} method.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IJobDefinition"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        """(experimental) The ARN of this batch job definition.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "jobDefinitionArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        """(experimental) The name of the batch job definition.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "jobDefinitionName")


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IJobQueue")
class IJobQueue(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Properties of a Job Queue.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IJobQueueProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        """(experimental) The ARN of this batch job queue.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        """(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :stability: experimental
        :attribute: true
        """
        ...


class _IJobQueueProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Properties of a Job Queue.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IJobQueue"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        """(experimental) The ARN of this batch job queue.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "jobQueueArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        """(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "jobQueueName")


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IMultiNodeProps")
class IMultiNodeProps(typing_extensions.Protocol):
    """(experimental) Properties for specifying multi-node properties for compute resources.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IMultiNodePropsProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        """(experimental) The number of nodes associated with a multi-node parallel job.

        :stability: experimental
        """
        ...

    @count.setter # type: ignore
    def count(self, value: jsii.Number) -> None:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mainNode")
    def main_node(self) -> jsii.Number:
        """(experimental) Specifies the node index for the main node of a multi-node parallel job.

        This node index value must be fewer than the number of nodes.

        :stability: experimental
        """
        ...

    @main_node.setter # type: ignore
    def main_node(self, value: jsii.Number) -> None:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rangeProps")
    def range_props(self) -> typing.List["INodeRangeProps"]:
        """(experimental) A list of node ranges and their properties associated with a multi-node parallel job.

        :stability: experimental
        """
        ...

    @range_props.setter # type: ignore
    def range_props(self, value: typing.List["INodeRangeProps"]) -> None:
        ...


class _IMultiNodePropsProxy:
    """(experimental) Properties for specifying multi-node properties for compute resources.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IMultiNodeProps"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        """(experimental) The number of nodes associated with a multi-node parallel job.

        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter # type: ignore
    def count(self, value: jsii.Number) -> None:
        jsii.set(self, "count", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mainNode")
    def main_node(self) -> jsii.Number:
        """(experimental) Specifies the node index for the main node of a multi-node parallel job.

        This node index value must be fewer than the number of nodes.

        :stability: experimental
        """
        return jsii.get(self, "mainNode")

    @main_node.setter # type: ignore
    def main_node(self, value: jsii.Number) -> None:
        jsii.set(self, "mainNode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rangeProps")
    def range_props(self) -> typing.List["INodeRangeProps"]:
        """(experimental) A list of node ranges and their properties associated with a multi-node parallel job.

        :stability: experimental
        """
        return jsii.get(self, "rangeProps")

    @range_props.setter # type: ignore
    def range_props(self, value: typing.List["INodeRangeProps"]) -> None:
        jsii.set(self, "rangeProps", value)


@jsii.interface(jsii_type="@aws-cdk/aws-batch.INodeRangeProps")
class INodeRangeProps(typing_extensions.Protocol):
    """(experimental) Properties for a multi-node batch job.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INodeRangePropsProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="container")
    def container(self) -> "JobDefinitionContainer":
        """(experimental) The container details for the node range.

        :stability: experimental
        """
        ...

    @container.setter # type: ignore
    def container(self, value: "JobDefinitionContainer") -> None:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fromNodeIndex")
    def from_node_index(self) -> typing.Optional[jsii.Number]:
        """(experimental) The minimum node index value to apply this container definition against.

        You may nest node ranges, for example 0:10 and 4:5, in which case the 4:5 range properties override the 0:10 properties.

        :default: 0

        :stability: experimental
        """
        ...

    @from_node_index.setter # type: ignore
    def from_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="toNodeIndex")
    def to_node_index(self) -> typing.Optional[jsii.Number]:
        """(experimental) The maximum node index value to apply this container definition against. If omitted, the highest value is used relative.

        to the number of nodes associated with the job. You may nest node ranges, for example 0:10 and 4:5,
        in which case the 4:5 range properties override the 0:10 properties.

        :default: {@link IMultiNodeprops.count}

        :stability: experimental
        """
        ...

    @to_node_index.setter # type: ignore
    def to_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _INodeRangePropsProxy:
    """(experimental) Properties for a multi-node batch job.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.INodeRangeProps"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="container")
    def container(self) -> "JobDefinitionContainer":
        """(experimental) The container details for the node range.

        :stability: experimental
        """
        return jsii.get(self, "container")

    @container.setter # type: ignore
    def container(self, value: "JobDefinitionContainer") -> None:
        jsii.set(self, "container", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fromNodeIndex")
    def from_node_index(self) -> typing.Optional[jsii.Number]:
        """(experimental) The minimum node index value to apply this container definition against.

        You may nest node ranges, for example 0:10 and 4:5, in which case the 4:5 range properties override the 0:10 properties.

        :default: 0

        :stability: experimental
        """
        return jsii.get(self, "fromNodeIndex")

    @from_node_index.setter # type: ignore
    def from_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "fromNodeIndex", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="toNodeIndex")
    def to_node_index(self) -> typing.Optional[jsii.Number]:
        """(experimental) The maximum node index value to apply this container definition against. If omitted, the highest value is used relative.

        to the number of nodes associated with the job. You may nest node ranges, for example 0:10 and 4:5,
        in which case the 4:5 range properties override the 0:10 properties.

        :default: {@link IMultiNodeprops.count}

        :stability: experimental
        """
        return jsii.get(self, "toNodeIndex")

    @to_node_index.setter # type: ignore
    def to_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "toNodeIndex", value)


@jsii.implements(IJobDefinition)
class JobDefinition(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.JobDefinition",
):
    """(experimental) Batch Job Definition.

    Defines a batch job definition to execute a specific batch job.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        container: "JobDefinitionContainer",
        job_definition_name: typing.Optional[builtins.str] = None,
        node_props: typing.Optional[IMultiNodeProps] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param container: (experimental) An object with various properties specific to container-based jobs.
        :param job_definition_name: (experimental) The name of the job definition. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: Cloudformation-generated name
        :param node_props: (experimental) An object with various properties specific to multi-node parallel jobs. Default: - undefined
        :param parameters: (experimental) When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters. Parameters in job submission requests take precedence over the defaults in a job definition. This allows you to use the same job definition for multiple jobs that use the same format, and programmatically change values in the command at submission time. Default: - undefined
        :param retry_attempts: (experimental) The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param timeout: (experimental) The timeout configuration for jobs that are submitted with this job definition. You can specify a timeout duration after which AWS Batch terminates your jobs if they have not finished. Default: - undefined

        :stability: experimental
        """
        props = JobDefinitionProps(
            container=container,
            job_definition_name=job_definition_name,
            node_props=node_props,
            parameters=parameters,
            retry_attempts=retry_attempts,
            timeout=timeout,
        )

        jsii.create(JobDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobDefinitionArn")
    @builtins.classmethod
    def from_job_definition_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        job_definition_arn: builtins.str,
    ) -> IJobDefinition:
        """(experimental) Imports an existing batch job definition by its amazon resource name.

        :param scope: -
        :param id: -
        :param job_definition_arn: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJobDefinitionArn", [scope, id, job_definition_arn])

    @jsii.member(jsii_name="fromJobDefinitionName")
    @builtins.classmethod
    def from_job_definition_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        job_definition_name: builtins.str,
    ) -> IJobDefinition:
        """(experimental) Imports an existing batch job definition by its name.

        If name is specified without a revision then the latest active revision is used.

        :param scope: -
        :param id: -
        :param job_definition_name: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJobDefinitionName", [scope, id, job_definition_name])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        """(experimental) The ARN of this batch job definition.

        :stability: experimental
        """
        return jsii.get(self, "jobDefinitionArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        """(experimental) The name of the batch job definition.

        :stability: experimental
        """
        return jsii.get(self, "jobDefinitionName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobDefinitionContainer",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "command": "command",
        "environment": "environment",
        "gpu_count": "gpuCount",
        "instance_type": "instanceType",
        "job_role": "jobRole",
        "linux_params": "linuxParams",
        "memory_limit_mib": "memoryLimitMiB",
        "mount_points": "mountPoints",
        "privileged": "privileged",
        "read_only": "readOnly",
        "ulimits": "ulimits",
        "user": "user",
        "vcpus": "vcpus",
        "volumes": "volumes",
    },
)
class JobDefinitionContainer:
    def __init__(
        self,
        *,
        image: aws_cdk.aws_ecs.ContainerImage,
        command: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        gpu_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        job_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        linux_params: typing.Optional[aws_cdk.aws_ecs.LinuxParameters] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        mount_points: typing.Optional[typing.List[aws_cdk.aws_ecs.MountPoint]] = None,
        privileged: typing.Optional[builtins.bool] = None,
        read_only: typing.Optional[builtins.bool] = None,
        ulimits: typing.Optional[typing.List[aws_cdk.aws_ecs.Ulimit]] = None,
        user: typing.Optional[builtins.str] = None,
        vcpus: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.List[aws_cdk.aws_ecs.Volume]] = None,
    ) -> None:
        """(experimental) Properties of a job definition container.

        :param image: (experimental) The image used to start a container.
        :param command: (experimental) The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: (experimental) The environment variables to pass to the container. Default: none
        :param gpu_count: (experimental) The number of physical GPUs to reserve for the container. The number of GPUs reserved for all containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on. Default: - No GPU reservation.
        :param instance_type: (experimental) The instance type to use for a multi-node parallel job. Currently all node groups in a multi-node parallel job must use the same instance type. This parameter is not valid for single-node container jobs. Default: - None
        :param job_role: (experimental) The IAM role that the container can assume for AWS permissions. Default: - An IAM role will created.
        :param linux_params: (experimental) Linux-specific modifications that are applied to the container, such as details for device mappings. For now, only the ``devices`` property is supported. Default: - None will be used.
        :param memory_limit_mib: (experimental) The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the memory specified here, the container is killed. You must specify at least 4 MiB of memory for a job. Default: 4
        :param mount_points: (experimental) The mount points for data volumes in your container. Default: - No mount points will be used.
        :param privileged: (experimental) When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param read_only: (experimental) When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param ulimits: (experimental) A list of ulimits to set in the container. Default: - No limits.
        :param user: (experimental) The user name to use inside the container. Default: - None will be used.
        :param vcpus: (experimental) The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. You must specify at least one vCPU. Default: 1
        :param volumes: (experimental) A list of data volumes used in a job. Default: - No data volumes will be used.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "image": image,
        }
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if gpu_count is not None:
            self._values["gpu_count"] = gpu_count
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if job_role is not None:
            self._values["job_role"] = job_role
        if linux_params is not None:
            self._values["linux_params"] = linux_params
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if mount_points is not None:
            self._values["mount_points"] = mount_points
        if privileged is not None:
            self._values["privileged"] = privileged
        if read_only is not None:
            self._values["read_only"] = read_only
        if ulimits is not None:
            self._values["ulimits"] = ulimits
        if user is not None:
            self._values["user"] = user
        if vcpus is not None:
            self._values["vcpus"] = vcpus
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """(experimental) The image used to start a container.

        :stability: experimental
        """
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return result

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.

        :stability: experimental
        """
        result = self._values.get("command")
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) The environment variables to pass to the container.

        :default: none

        :stability: experimental
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """(experimental) The number of physical GPUs to reserve for the container.

        The number of GPUs reserved for all
        containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on.

        :default: - No GPU reservation.

        :stability: experimental
        """
        result = self._values.get("gpu_count")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """(experimental) The instance type to use for a multi-node parallel job.

        Currently all node groups in a
        multi-node parallel job must use the same instance type. This parameter is not valid
        for single-node container jobs.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def job_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) The IAM role that the container can assume for AWS permissions.

        :default: - An IAM role will created.

        :stability: experimental
        """
        result = self._values.get("job_role")
        return result

    @builtins.property
    def linux_params(self) -> typing.Optional[aws_cdk.aws_ecs.LinuxParameters]:
        """(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        For now, only the ``devices`` property is supported.

        :default: - None will be used.

        :stability: experimental
        """
        result = self._values.get("linux_params")
        return result

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """(experimental) The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed
        the memory specified here, the container is killed. You must specify at least 4 MiB of memory for a job.

        :default: 4

        :stability: experimental
        """
        result = self._values.get("memory_limit_mib")
        return result

    @builtins.property
    def mount_points(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.MountPoint]]:
        """(experimental) The mount points for data volumes in your container.

        :default: - No mount points will be used.

        :stability: experimental
        """
        result = self._values.get("mount_points")
        return result

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        """(experimental) When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        :default: false

        :stability: experimental
        """
        result = self._values.get("privileged")
        return result

    @builtins.property
    def read_only(self) -> typing.Optional[builtins.bool]:
        """(experimental) When this parameter is true, the container is given read-only access to its root file system.

        :default: false

        :stability: experimental
        """
        result = self._values.get("read_only")
        return result

    @builtins.property
    def ulimits(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.Ulimit]]:
        """(experimental) A list of ulimits to set in the container.

        :default: - No limits.

        :stability: experimental
        """
        result = self._values.get("ulimits")
        return result

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        """(experimental) The user name to use inside the container.

        :default: - None will be used.

        :stability: experimental
        """
        result = self._values.get("user")
        return result

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        """(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to
        1,024 CPU shares. You must specify at least one vCPU.

        :default: 1

        :stability: experimental
        """
        result = self._values.get("vcpus")
        return result

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[aws_cdk.aws_ecs.Volume]]:
        """(experimental) A list of data volumes used in a job.

        :default: - No data volumes will be used.

        :stability: experimental
        """
        result = self._values.get("volumes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefinitionContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "job_definition_name": "jobDefinitionName",
        "node_props": "nodeProps",
        "parameters": "parameters",
        "retry_attempts": "retryAttempts",
        "timeout": "timeout",
    },
)
class JobDefinitionProps:
    def __init__(
        self,
        *,
        container: JobDefinitionContainer,
        job_definition_name: typing.Optional[builtins.str] = None,
        node_props: typing.Optional[IMultiNodeProps] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(experimental) Construction properties of the {@link JobDefinition} construct.

        :param container: (experimental) An object with various properties specific to container-based jobs.
        :param job_definition_name: (experimental) The name of the job definition. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: Cloudformation-generated name
        :param node_props: (experimental) An object with various properties specific to multi-node parallel jobs. Default: - undefined
        :param parameters: (experimental) When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters. Parameters in job submission requests take precedence over the defaults in a job definition. This allows you to use the same job definition for multiple jobs that use the same format, and programmatically change values in the command at submission time. Default: - undefined
        :param retry_attempts: (experimental) The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param timeout: (experimental) The timeout configuration for jobs that are submitted with this job definition. You can specify a timeout duration after which AWS Batch terminates your jobs if they have not finished. Default: - undefined

        :stability: experimental
        """
        if isinstance(container, dict):
            container = JobDefinitionContainer(**container)
        self._values: typing.Dict[str, typing.Any] = {
            "container": container,
        }
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if node_props is not None:
            self._values["node_props"] = node_props
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def container(self) -> JobDefinitionContainer:
        """(experimental) An object with various properties specific to container-based jobs.

        :stability: experimental
        """
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return result

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the job definition.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :default: Cloudformation-generated name

        :stability: experimental
        """
        result = self._values.get("job_definition_name")
        return result

    @builtins.property
    def node_props(self) -> typing.Optional[IMultiNodeProps]:
        """(experimental) An object with various properties specific to multi-node parallel jobs.

        :default: - undefined

        :stability: experimental
        """
        result = self._values.get("node_props")
        return result

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters.

        Parameters
        in job submission requests take precedence over the defaults in a job definition.
        This allows you to use the same job definition for multiple jobs that use the same
        format, and programmatically change values in the command at submission time.

        :default: - undefined

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """(experimental) The number of times to move a job to the RUNNABLE status.

        You may specify between 1 and
        10 attempts. If the value of attempts is greater than one, the job is retried on failure
        the same number of attempts as the value.

        :default: 1

        :stability: experimental
        """
        result = self._values.get("retry_attempts")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The timeout configuration for jobs that are submitted with this job definition.

        You can specify
        a timeout duration after which AWS Batch terminates your jobs if they have not finished.

        :default: - undefined

        :stability: experimental
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IJobQueue)
class JobQueue(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.JobQueue",
):
    """(experimental) Batch Job Queue.

    Defines a batch job queue to define how submitted batch jobs
    should be ran based on specified batch compute environments.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        compute_environments: typing.List["JobQueueComputeEnvironment"],
        enabled: typing.Optional[builtins.bool] = None,
        job_queue_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param compute_environments: (experimental) The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue.
        :param enabled: (experimental) The state of the job queue. If set to true, it is able to accept jobs. Default: true
        :param job_queue_name: (experimental) A name for the job queue. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - Cloudformation-generated name
        :param priority: (experimental) The priority of the job queue. Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1. Default: 1

        :stability: experimental
        """
        props = JobQueueProps(
            compute_environments=compute_environments,
            enabled=enabled,
            job_queue_name=job_queue_name,
            priority=priority,
        )

        jsii.create(JobQueue, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobQueueArn")
    @builtins.classmethod
    def from_job_queue_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        job_queue_arn: builtins.str,
    ) -> IJobQueue:
        """(experimental) Fetches an existing batch job queue by its amazon resource name.

        :param scope: -
        :param id: -
        :param job_queue_arn: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJobQueueArn", [scope, id, job_queue_arn])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        """(experimental) The ARN of this batch job queue.

        :stability: experimental
        """
        return jsii.get(self, "jobQueueArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        """(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :stability: experimental
        """
        return jsii.get(self, "jobQueueName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobQueueComputeEnvironment",
    jsii_struct_bases=[],
    name_mapping={"compute_environment": "computeEnvironment", "order": "order"},
)
class JobQueueComputeEnvironment:
    def __init__(
        self,
        *,
        compute_environment: IComputeEnvironment,
        order: jsii.Number,
    ) -> None:
        """(experimental) Properties for mapping a compute environment to a job queue.

        :param compute_environment: (experimental) The batch compute environment to use for processing submitted jobs to this queue.
        :param order: (experimental) The order in which this compute environment will be selected for dynamic allocation of resources to process submitted jobs.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "compute_environment": compute_environment,
            "order": order,
        }

    @builtins.property
    def compute_environment(self) -> IComputeEnvironment:
        """(experimental) The batch compute environment to use for processing submitted jobs to this queue.

        :stability: experimental
        """
        result = self._values.get("compute_environment")
        assert result is not None, "Required property 'compute_environment' is missing"
        return result

    @builtins.property
    def order(self) -> jsii.Number:
        """(experimental) The order in which this compute environment will be selected for dynamic allocation of resources to process submitted jobs.

        :stability: experimental
        """
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobQueueComputeEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environments": "computeEnvironments",
        "enabled": "enabled",
        "job_queue_name": "jobQueueName",
        "priority": "priority",
    },
)
class JobQueueProps:
    def __init__(
        self,
        *,
        compute_environments: typing.List[JobQueueComputeEnvironment],
        enabled: typing.Optional[builtins.bool] = None,
        job_queue_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        """(experimental) Properties of a batch job queue.

        :param compute_environments: (experimental) The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue.
        :param enabled: (experimental) The state of the job queue. If set to true, it is able to accept jobs. Default: true
        :param job_queue_name: (experimental) A name for the job queue. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - Cloudformation-generated name
        :param priority: (experimental) The priority of the job queue. Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1. Default: 1

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "compute_environments": compute_environments,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if job_queue_name is not None:
            self._values["job_queue_name"] = job_queue_name
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def compute_environments(self) -> typing.List[JobQueueComputeEnvironment]:
        """(experimental) The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to
        determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them
        with a job queue. You can associate up to three compute environments with a job queue.

        :stability: experimental
        """
        result = self._values.get("compute_environments")
        assert result is not None, "Required property 'compute_environments' is missing"
        return result

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        """(experimental) The state of the job queue.

        If set to true, it is able to accept jobs.

        :default: true

        :stability: experimental
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :default: - Cloudformation-generated name

        :stability: experimental
        """
        result = self._values.get("job_queue_name")
        return result

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """(experimental) The priority of the job queue.

        Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first
        when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value
        of 10 is given scheduling preference over a job queue with a priority value of 1.

        :default: 1

        :stability: experimental
        """
        result = self._values.get("priority")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.LaunchTemplateSpecification",
    jsii_struct_bases=[],
    name_mapping={"launch_template_name": "launchTemplateName", "version": "version"},
)
class LaunchTemplateSpecification:
    def __init__(
        self,
        *,
        launch_template_name: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Launch template property specification.

        :param launch_template_name: (experimental) The Launch template name.
        :param version: (experimental) The launch template version to be used (optional). Default: - the default version of the launch template

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "launch_template_name": launch_template_name,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def launch_template_name(self) -> builtins.str:
        """(experimental) The Launch template name.

        :stability: experimental
        """
        result = self._values.get("launch_template_name")
        assert result is not None, "Required property 'launch_template_name' is missing"
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """(experimental) The launch template version to be used (optional).

        :default: - the default version of the launch template

        :stability: experimental
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LaunchTemplateSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IComputeEnvironment)
class ComputeEnvironment(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.ComputeEnvironment",
):
    """(experimental) Batch Compute Environment.

    Defines a batch compute environment to run batch jobs on.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[ComputeResources] = None,
        enabled: typing.Optional[builtins.bool] = None,
        managed: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param compute_environment_name: (experimental) A name for the compute environment. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - CloudFormation-generated name
        :param compute_resources: (experimental) The details of the required compute resources for the managed compute environment. If specified, and this is an unmanaged compute environment, will throw an error. By default, AWS Batch managed compute environments use a recent, approved version of the Amazon ECS-optimized AMI for compute resources. Default: - CloudFormation defaults
        :param enabled: (experimental) The state of the compute environment. If the state is set to true, then the compute environment accepts jobs from a queue and can scale out automatically based on queues. Default: true
        :param managed: (experimental) Determines if AWS should manage the allocation of compute resources for processing jobs. If set to false, then you are in charge of providing the compute resource details. Default: true
        :param service_role: (experimental) The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service. By default, this role is created for you using the AWS managed service policy for Batch. Default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        :stability: experimental
        """
        props = ComputeEnvironmentProps(
            compute_environment_name=compute_environment_name,
            compute_resources=compute_resources,
            enabled=enabled,
            managed=managed,
            service_role=service_role,
        )

        jsii.create(ComputeEnvironment, self, [scope, id, props])

    @jsii.member(jsii_name="fromComputeEnvironmentArn")
    @builtins.classmethod
    def from_compute_environment_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        compute_environment_arn: builtins.str,
    ) -> IComputeEnvironment:
        """(experimental) Fetches an existing batch compute environment by its amazon resource name.

        :param scope: -
        :param id: -
        :param compute_environment_arn: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromComputeEnvironmentArn", [scope, id, compute_environment_arn])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        """(experimental) The ARN of this compute environment.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "computeEnvironmentArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        """(experimental) The name of this compute environment.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "computeEnvironmentName")


__all__ = [
    "AllocationStrategy",
    "CfnComputeEnvironment",
    "CfnComputeEnvironmentProps",
    "CfnJobDefinition",
    "CfnJobDefinitionProps",
    "CfnJobQueue",
    "CfnJobQueueProps",
    "ComputeEnvironment",
    "ComputeEnvironmentProps",
    "ComputeResourceType",
    "ComputeResources",
    "IComputeEnvironment",
    "IJobDefinition",
    "IJobQueue",
    "IMultiNodeProps",
    "INodeRangeProps",
    "JobDefinition",
    "JobDefinitionContainer",
    "JobDefinitionProps",
    "JobQueue",
    "JobQueueComputeEnvironment",
    "JobQueueProps",
    "LaunchTemplateSpecification",
]

publication.publish()
