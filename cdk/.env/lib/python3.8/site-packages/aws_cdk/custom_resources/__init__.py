"""
# AWS CDK Custom Resources

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

## Provider Framework

AWS CloudFormation [custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) are extension points to the provisioning
engine. When CloudFormation needs to create, update or delete a custom resource,
it sends a lifecycle event notification to a **custom resource provider**. The provider
handles the event (e.g. creates a resource) and sends back a response to CloudFormation.

The `@aws-cdk/custom-resources.Provider` construct is a "mini-framework" for
implementing providers for AWS CloudFormation custom resources. The framework offers a high-level API which makes it easier to implement robust
and powerful custom resources and includes the following capabilities:

* Handles responses to AWS CloudFormation and protects against blocked
  deployments
* Validates handler return values to help with correct handler implementation
* Supports asynchronous handlers to enable operations that require a long waiting period for a resource, which can exceed the AWS Lambda timeout
* Implements default behavior for physical resource IDs.

The following code shows how the `Provider` construct is used in conjunction
with a `CustomResource` and a user-provided AWS Lambda function which implements
the actual handler.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import CustomResource
import aws_cdk.aws_logs as logs
import aws_cdk.custom_resources as cr

on_event = lambda_.Function(self, "MyHandler")

my_provider = cr.Provider(self, "MyProvider",
    on_event_handler=on_event,
    is_complete_handler=is_complete, # optional async "waiter"
    log_retention=logs.RetentionDays.ONE_DAY
)

CustomResource(self, "Resource1", service_token=my_provider.service_token)
CustomResource(self, "Resource2", service_token=my_provider.service_token)
```

Providers are implemented through AWS Lambda functions that are triggered by the
provider framework in response to lifecycle events.

At the minimum, users must define the `onEvent` handler, which is invoked by the
framework for all resource lifecycle events (`Create`, `Update` and `Delete`)
and returns a result which is then submitted to CloudFormation.

The following example is a skeleton for a Python implementation of `onEvent`:

```py
def on_event(event, context):
  print(event)
  request_type = event['RequestType']
  if request_type == 'Create': return on_create(event)
  if request_type == 'Update': return on_update(event)
  if request_type == 'Delete': return on_delete(event)
  raise Exception("Invalid request type: %s" % request_type)

def on_create(event):
  props = event["ResourceProperties"]
  print("create new resource with props %s" % props)

  # add your create code here...
  physical_id = ...

  return { 'PhysicalResourceId': physical_id }

def on_update(event):
  physical_id = event["PhysicalResourceId"]
  props = event["ResourceProperties"]
  print("update resource %s with props %s" % (physical_id, props))
  # ...

def on_delete(event):
  physical_id = event["PhysicalResourceId"]
  print("delete resource %s" % physical_id)
  # ...
```

Users may also provide an additional handler called `isComplete`, for cases
where the lifecycle operation cannot be completed immediately. The
`isComplete` handler will be retried asynchronously after `onEvent` until it
returns `IsComplete: true`, or until the total provider timeout has expired.

The following example is a skeleton for a Python implementation of `isComplete`:

```py
def is_complete(event, context):
  physical_id = event["PhysicalResourceId"]
  request_type = event["RequestType"]

  # check if resource is stable based on request_type
  is_ready = ...

  return { 'IsComplete': is_ready }
```

### Handling Lifecycle Events: onEvent

The user-defined `onEvent` AWS Lambda function is invoked whenever a resource
lifecycle event occurs. The function is expected to handle the event and return
a response to the framework that, at least, includes the physical resource ID.

If `onEvent` returns successfully, the framework will submit a "SUCCESS" response
to AWS CloudFormation for this resource operation.  If the provider is
[asynchronous](#asynchronous-providers-iscomplete) (`isCompleteHandler` is
defined), the framework will only submit a response based on the result of
`isComplete`.

If `onEvent` throws an error, the framework will submit a "FAILED" response to
AWS CloudFormation.

The input event includes the following fields derived from the [Custom Resource
Provider Request]:

|Field|Type|Description
|-----|----|----------------
|`RequestType`|String|The type of lifecycle event: `Create`, `Update` or `Delete`.
|`LogicalResourceId`|String|The template developer-chosen name (logical ID) of the custom resource in the AWS CloudFormation template.
|`PhysicalResourceId`|String|This field will only be present for `Update` and `Delete` events and includes the value returned in `PhysicalResourceId` of the previous operation.
|`ResourceProperties`|JSON|This field contains the properties defined in the template for this custom resource.
|`OldResourceProperties`|JSON|This field will only be present for `Update` events and contains the resource properties that were declared previous to the update request.
|`ResourceType`|String|The resource type defined for this custom resource in the template. A provider may handle any number of custom resource types.
|`RequestId`|String|A unique ID for the request.
|`StackId`|String|The ARN that identifies the stack that contains the custom resource.

The return value from `onEvent` must be a JSON object with the following fields:

|Field|Type|Required|Description
|-----|----|--------|-----------
|`PhysicalResourceId`|String|No|The allocated/assigned physical ID of the resource. If omitted for `Create` events, the event's `RequestId` will be used. For `Update`, the current physical ID will be used. If a different value is returned, CloudFormation will follow with a subsequent `Delete` for the previous ID (resource replacement). For `Delete`, it will always return the current physical resource ID, and if the user returns a different one, an error will occur.
|`Data`|JSON|No|Resource attributes, which can later be retrieved through `Fn::GetAtt` on the custom resource object.
|*any*|*any*|No|Any other field included in the response will be passed through to `isComplete`. This can sometimes be useful to pass state between the handlers.

### Asynchronous Providers: isComplete

It is not uncommon for the provisioning of resources to be an asynchronous
operation, which means that the operation does not immediately finish, and we
need to "wait" until the resource stabilizes.

The provider framework makes it easy to implement "waiters" by allowing users to
specify an additional AWS Lambda function in `isCompleteHandler`.

The framework will repeatedly invoke the handler every `queryInterval`. When
`isComplete` returns with `IsComplete: true`, the framework will submit a
"SUCCESS" response to AWS CloudFormation. If `totalTimeout` expires and the
operation has not yet completed, the framework will submit a "FAILED" response
with the message "Operation timed out".

If an error is thrown, the framework will submit a "FAILED" response to AWS
CloudFormation.

The input event to `isComplete` includes all request fields, combined with all
fields returned from `onEvent`. If `PhysicalResourceId` has not been explicitly
returned from `onEvent`, it's value will be calculated based on the heuristics
described above.

The return value must be a JSON object with the following fields:

|Field|Type|Required|Description
|-----|----|--------|-----------
|`IsComplete`|Boolean|Yes|Indicates if the operation has finished or not.
|`Data`|JSON|No|May only be sent if `IsComplete` is `true` and includes additional resource attributes. These attributes will be **merged** with the ones returned from `onEvent`

### Physical Resource IDs

Every resource in CloudFormation has a physical resource ID. When a resource is
created, the `PhysicalResourceId` returned from the `Create` operation is stored
by AWS CloudFormation and assigned to the logical ID defined for this resource
in the template. If a `Create` operation returns without a `PhysicalResourceId`,
the framework will use `RequestId` as the default. This is sufficient for
various cases such as "pseudo-resources" which only query data.

For `Update` and `Delete` operations, the resource event will always include the
current `PhysicalResourceId` of the resource.

When an `Update` operation occurs, the default behavior is to return the current
physical resource ID. if the `onEvent` returns a `PhysicalResourceId` which is
different from the current one, AWS CloudFormation will treat this as a
**resource replacement**, and it will issue a subsequent `Delete` operation for
the old resource.

As a rule of thumb, if your custom resource supports configuring a physical name
(e.g. you can specify a `BucketName` when you define an `AWS::S3::Bucket`), you
must return this name in `PhysicalResourceId` and make sure to handle
replacement properly. The `S3File` example demonstrates this
through the `objectKey` property.

### Error Handling

As mentioned above, if any of the user handlers fail (i.e. throws an exception)
or times out (due to their AWS Lambda timing out), the framework will trap these
errors and submit a "FAILED" response to AWS CloudFormation, along with the error
message.

Since errors can occur in multiple places in the provider (framework, `onEvent`,
`isComplete`), it is important to know that there could situations where a
resource operation fails even though the operation technically succeeded (i.e.
isComplete throws an error).

When AWS CloudFormation receives a "FAILED" response, it will attempt to roll
back the stack to it's last state. This has different meanings for different
lifecycle events:

* If a `Create` event fails, the resource provider framework will automatically
  ignore the subsequent `Delete` operation issued by AWS CloudFormation. The
  framework currently does not support customizing this behavior (see
  https://github.com/aws/aws-cdk/issues/5524).
* If an `Update` event fails, CloudFormation will issue an additional `Update`
  with the previous properties.
* If a `Delete` event fails, CloudFormation will abandon this resource.

### Execution Policy

Similarly to any AWS Lambda function, if the user-defined handlers require
access to AWS resources, you will have to define these permissions
by calling "grant" methods such as `myBucket.grantRead(myHandler)`), using `myHandler.addToRolePolicy`
or specifying an `initialPolicy` when defining the function.

Bear in mind that in most cases, a single provider will be used for multiple
resource instances. This means that the execution policy of the provider must
have the appropriate privileges.

The following example grants the `onEvent` handler `s3:GetObject*` permissions
to all buckets:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.Function(self, "OnEventHandler",
    # ...
    initial_policy=[
        iam.PolicyStatement(actions=["s3:GetObject*"], resources=["*"])
    ]
)
```

### Timeouts

Users are responsible to define the timeouts for the AWS Lambda functions for
user-defined handlers. It is recommended not to exceed a **14 minutes** timeout,
since all framework functions are configured to time out after 15 minutes, which
is the maximal AWS Lambda timeout.

If your operation takes over **14 minutes**, the recommended approach is to
implement an [asynchronous provider](#asynchronous-providers-iscomplete), and
then configure the timeouts for the asynchronous retries through the
`queryInterval` and the `totalTimeout` options.

### Examples

This module includes a few examples for custom resource implementations:

#### S3File

Provisions an object in an S3 bucket with textual contents. See the source code
for the
[construct](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/custom-resources/test/provider-framework/integration-test-fixtures/s3-file.ts) and
[handler](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/custom-resources/test/provider-framework/integration-test-fixtures/s3-file-handler/index.ts).

The following example will create the file `folder/file1.txt` inside `myBucket`
with the contents `hello!`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
S3File(self, "MyFile",
    bucket=my_bucket,
    object_key="folder/file1.txt", # optional
    content="hello!",
    public=True
)
```

This sample demonstrates the following concepts:

* Synchronous implementation (`isComplete` is not defined)
* Automatically generates the physical name if `objectKey` is not defined
* Handles physical name changes
* Returns resource attributes
* Handles deletions
* Implemented in TypeScript

#### S3Assert

Checks that the textual contents of an S3 object matches a certain value. The check will be retried for 5 minutes as long as the object is not found or the value is different. See the source code for the [construct](test/provider-framework/integration-test-fixtures/s3-assert.ts) and [handler](test/provider-framework/integration-test-fixtures/s3-assert-handler/index.py).

The following example defines an `S3Assert` resource which waits until
`myfile.txt` in `myBucket` exists and includes the contents `foo bar`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
S3Assert(self, "AssertMyFile",
    bucket=my_bucket,
    object_key="myfile.txt",
    expected_content="foo bar"
)
```

This sample demonstrates the following concepts:

* Asynchronous implementation
* Non-intrinsic physical IDs
* Implemented in Python

## Custom Resources for AWS APIs

Sometimes a single API call can fill the gap in the CloudFormation coverage. In
this case you can use the `AwsCustomResource` construct. This construct creates
a custom resource that can be customized to make specific API calls for the
`CREATE`, `UPDATE` and `DELETE` events. Additionally, data returned by the API
call can be extracted and used in other constructs/resources (creating a real
CloudFormation dependency using `Fn::GetAtt` under the hood).

The physical id of the custom resource can be specified or derived from the data
returned by the API call.

The `AwsCustomResource` uses the AWS SDK for JavaScript. Services, actions and
parameters can be found in the [API documentation](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html).

Path to data must be specified using a dot notation, e.g. to get the string value
of the `Title` attribute for the first item returned by `dynamodb.query` it should
be `Items.0.Title.S`.

To make sure that the newest API calls are available the latest AWS SDK v2 is installed
in the Lambda function implementing the custom resource. The installation takes around 60
seconds. If you prefer to optimize for speed, you can disable the installation by setting
the `installLatestAwsSdk` prop to `false`.

### Execution Policy

You must provide the `policy` property defining the IAM Policy that will be applied to the API calls.
The library provides two factory methods to quickly configure this:

* **`AwsCustomResourcePolicy.fromSdkCalls`** - Use this to auto-generate IAM Policy statements based on the configured SDK calls.
  Note that you will have to either provide specific ARN's, or explicitly use `AwsCustomResourcePolicy.ANY_RESOURCE` to allow access to any resource.
* **`AwsCustomResourcePolicy.fromStatements`** - Use this to specify your own custom statements.

The custom resource also implements `iam.IGrantable`, making it possible to use the `grantXxx()` methods.

As this custom resource uses a singleton Lambda function, it's important to note
that the function's role will eventually accumulate the permissions/grants from all
resources.

Chained API calls can be achieved by creating dependencies:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
aws_custom1 = AwsCustomResource(self, "API1",
    on_create={
        "service": "...",
        "action": "...",
        "physical_resource_id": PhysicalResourceId.of("...")
    },
    policy=AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)
)

aws_custom2 = AwsCustomResource(self, "API2",
    on_create={
        "service": "...",
        "action": "...",
        "parameters": {
            "text": aws_custom1.get_response_field("Items.0.text")
        },
        "physical_resource_id": PhysicalResourceId.of("...")
    },
    policy=AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)
)
```

### Physical Resource Id Parameter

Some AWS APIs may require passing the physical resource id in as a parameter for doing updates and deletes. You can pass it by using `PhysicalResourceIdReference`.

```
const awsCustom = new AwsCustomResource(this, '...', {
  onCreate: {
    service: '...',
    action: '...'
    parameters: {
      text: '...'
    },
    physicalResourceId: PhysicalResourceId.of('...')
  },
  onUpdate: {
    service: '...',
    action: '...'.
    parameters: {
      text: '...',
      resourceId: new PhysicalResourceIdReference()
    }
  },
  policy: AwsCustomResourcePolicy.fromSdkCalls({resources: AwsCustomResourcePolicy.ANY_RESOURCE})
})
```

### Error Handling

Every error produced by the API call is treated as is and will cause a "FAILED" response to be submitted to CloudFormation.
You can ignore some errors by specifying the `ignoreErrorCodesMatching` property, which accepts a regular expression that is
tested against the `code` property of the response. If matched, a "SUCCESS" response is submitted.
Note that in such a case, the call response data and the `Data` key submitted to CloudFormation would both be an empty JSON object.
Since a successful resource provisioning might or might not produce outputs, this presents us with some limitations:

* `PhysicalResourceId.fromResponse` - Since the call response data might be empty, we cannot use it to extract the physical id.
* `getResponseField` and `getResponseFieldReference` - Since the `Data` key is empty, the resource will not have any attributes, and therefore, invoking these functions will result in an error.

In both the cases, you will get a synth time error if you attempt to use it in conjunction with `ignoreErrorCodesMatching`.

### Customizing the Lambda function implementing the custom resource

Use the `role`, `timeout`, `logRetention` and `functionName` properties to customize
the Lambda function implementing the custom resource:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
AwsCustomResource(self, "Customized",
    # other props here
    role=my_role, # must be assumable by the `lambda.amazonaws.com` service principal
    timeout=cdk.Duration.minutes(10), # defaults to 2 minutes
    log_retention=logs.RetentionDays.ONE_WEEK, # defaults to never delete logs
    function_name="my-custom-name"
)
```

### Examples

#### Verify a domain with SES

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
verify_domain_identity = AwsCustomResource(self, "VerifyDomainIdentity",
    on_create={
        "service": "SES",
        "action": "verifyDomainIdentity",
        "parameters": {
            "Domain": "example.com"
        },
        "physical_resource_id": PhysicalResourceId.from_response("VerificationToken")
    },
    policy=AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)
)

route53.TxtRecord(self, "SESVerificationRecord",
    zone=zone,
    record_name="_amazonses.example.com",
    values=[verify_domain_identity.get_response_field("VerificationToken")]
)
```

#### Get the latest version of a secure SSM parameter

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
get_parameter = AwsCustomResource(self, "GetParameter",
    on_update={# will also be called for a CREATE event
        "service": "SSM",
        "action": "getParameter",
        "parameters": {
            "Name": "my-parameter",
            "WithDecryption": True
        },
        "physical_resource_id": PhysicalResourceId.of(Date.now().to_string())},
    policy=AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)
)

# Use the value in another construct with
get_parameter.get_response_field("Parameter.Value")
```

---


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

import aws_cdk.aws_cloudformation
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.aws_iam.IGrantable)
class AwsCustomResource(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/custom-resources.AwsCustomResource",
):
    """Defines a custom resource that is materialized using specific AWS API calls.

    Use this to bridge any gap that might exist in the CloudFormation Coverage.
    You can specify exactly which calls are invoked for the 'CREATE', 'UPDATE' and 'DELETE' life cycle events.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        policy: "AwsCustomResourcePolicy",
        function_name: typing.Optional[builtins.str] = None,
        install_latest_aws_sdk: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        on_create: typing.Optional["AwsSdkCall"] = None,
        on_delete: typing.Optional["AwsSdkCall"] = None,
        on_update: typing.Optional["AwsSdkCall"] = None,
        resource_type: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param policy: The policy that will be added to the execution role of the Lambda function implementing this custom resource provider. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources.
        :param function_name: A name for the Lambda function implementing this custom resource. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param install_latest_aws_sdk: Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html. The installation takes around 60 seconds. Default: true
        :param log_retention: The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. Default: logs.RetentionDays.INFINITE
        :param on_create: The AWS SDK call to make when the resource is created. Default: - the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: - no call
        :param resource_type: Cloudformation Resource type. Default: - Custom::AWS
        :param role: The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)
        """
        props = AwsCustomResourceProps(
            policy=policy,
            function_name=function_name,
            install_latest_aws_sdk=install_latest_aws_sdk,
            log_retention=log_retention,
            on_create=on_create,
            on_delete=on_delete,
            on_update=on_update,
            resource_type=resource_type,
            role=role,
            timeout=timeout,
        )

        jsii.create(AwsCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="getResponseField")
    def get_response_field(self, data_path: builtins.str) -> builtins.str:
        """Returns response data for the AWS SDK call as string.

        Example for S3 / listBucket : 'Buckets.0.Name'

        Note that you cannot use this method if ``ignoreErrorCodesMatching``
        is configured for any of the SDK calls. This is because in such a case,
        the response data might not exist, and will cause a CloudFormation deploy time error.

        :param data_path: the path to the data.
        """
        return jsii.invoke(self, "getResponseField", [data_path])

    @jsii.member(jsii_name="getResponseFieldReference")
    def get_response_field_reference(
        self,
        data_path: builtins.str,
    ) -> aws_cdk.core.Reference:
        """Returns response data for the AWS SDK call.

        Example for S3 / listBucket : 'Buckets.0.Name'

        Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getDataString`` for string attributes.

        Note that you cannot use this method if ``ignoreErrorCodesMatching``
        is configured for any of the SDK calls. This is because in such a case,
        the response data might not exist, and will cause a CloudFormation deploy time error.

        :param data_path: the path to the data.
        """
        return jsii.invoke(self, "getResponseFieldReference", [data_path])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")


class AwsCustomResourcePolicy(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/custom-resources.AwsCustomResourcePolicy",
):
    """The IAM Policy that will be applied to the different calls."""

    @jsii.member(jsii_name="fromSdkCalls")
    @builtins.classmethod
    def from_sdk_calls(
        cls,
        *,
        resources: typing.List[builtins.str],
    ) -> "AwsCustomResourcePolicy":
        """Generate IAM Policy Statements from the configured SDK calls.

        Each SDK call with be translated to an IAM Policy Statement in the form of: ``call.service:call.action`` (e.g ``s3:PutObject``).

        :param resources: The resources that the calls will have access to. It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE`` to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't know the physical name of in advance. Note that will apply to ALL SDK calls.
        """
        options = SdkCallsPolicyOptions(resources=resources)

        return jsii.sinvoke(cls, "fromSdkCalls", [options])

    @jsii.member(jsii_name="fromStatements")
    @builtins.classmethod
    def from_statements(
        cls,
        statements: typing.List[aws_cdk.aws_iam.PolicyStatement],
    ) -> "AwsCustomResourcePolicy":
        """Explicit IAM Policy Statements.

        :param statements: the statements to propagate to the SDK calls.
        """
        return jsii.sinvoke(cls, "fromStatements", [statements])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ANY_RESOURCE")
    def ANY_RESOURCE(cls) -> typing.List[builtins.str]:
        """Use this constant to configure access to any resource."""
        return jsii.sget(cls, "ANY_RESOURCE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="statements")
    def statements(self) -> typing.List[aws_cdk.aws_iam.PolicyStatement]:
        """statements for explicit policy."""
        return jsii.get(self, "statements")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        """resources for auto-generated from SDK calls."""
        return jsii.get(self, "resources")


@jsii.data_type(
    jsii_type="@aws-cdk/custom-resources.AwsCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "function_name": "functionName",
        "install_latest_aws_sdk": "installLatestAwsSdk",
        "log_retention": "logRetention",
        "on_create": "onCreate",
        "on_delete": "onDelete",
        "on_update": "onUpdate",
        "resource_type": "resourceType",
        "role": "role",
        "timeout": "timeout",
    },
)
class AwsCustomResourceProps:
    def __init__(
        self,
        *,
        policy: AwsCustomResourcePolicy,
        function_name: typing.Optional[builtins.str] = None,
        install_latest_aws_sdk: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        on_create: typing.Optional["AwsSdkCall"] = None,
        on_delete: typing.Optional["AwsSdkCall"] = None,
        on_update: typing.Optional["AwsSdkCall"] = None,
        resource_type: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Properties for AwsCustomResource.

        Note that at least onCreate, onUpdate or onDelete must be specified.

        :param policy: The policy that will be added to the execution role of the Lambda function implementing this custom resource provider. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources.
        :param function_name: A name for the Lambda function implementing this custom resource. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param install_latest_aws_sdk: Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html. The installation takes around 60 seconds. Default: true
        :param log_retention: The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. Default: logs.RetentionDays.INFINITE
        :param on_create: The AWS SDK call to make when the resource is created. Default: - the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: - no call
        :param resource_type: Cloudformation Resource type. Default: - Custom::AWS
        :param role: The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)
        """
        if isinstance(on_create, dict):
            on_create = AwsSdkCall(**on_create)
        if isinstance(on_delete, dict):
            on_delete = AwsSdkCall(**on_delete)
        if isinstance(on_update, dict):
            on_update = AwsSdkCall(**on_update)
        self._values: typing.Dict[str, typing.Any] = {
            "policy": policy,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if install_latest_aws_sdk is not None:
            self._values["install_latest_aws_sdk"] = install_latest_aws_sdk
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if on_create is not None:
            self._values["on_create"] = on_create
        if on_delete is not None:
            self._values["on_delete"] = on_delete
        if on_update is not None:
            self._values["on_update"] = on_update
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if role is not None:
            self._values["role"] = role
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def policy(self) -> AwsCustomResourcePolicy:
        """The policy that will be added to the execution role of the Lambda function implementing this custom resource provider.

        The custom resource also implements ``iam.IGrantable``, making it possible
        to use the ``grantXxx()`` methods.

        As this custom resource uses a singleton Lambda function, it's important
        to note the that function's role will eventually accumulate the
        permissions/grants from all resources.

        :see: Policy.fromSdkCalls
        """
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return result

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        """A name for the Lambda function implementing this custom resource.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.
        """
        result = self._values.get("function_name")
        return result

    @builtins.property
    def install_latest_aws_sdk(self) -> typing.Optional[builtins.bool]:
        """Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html.

        The installation takes around 60 seconds.

        :default: true
        """
        result = self._values.get("install_latest_aws_sdk")
        return result

    @builtins.property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        """The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs.

        :default: logs.RetentionDays.INFINITE
        """
        result = self._values.get("log_retention")
        return result

    @builtins.property
    def on_create(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is created.

        :default: - the call when the resource is updated
        """
        result = self._values.get("on_create")
        return result

    @builtins.property
    def on_delete(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is deleted.

        :default: - no call
        """
        result = self._values.get("on_delete")
        return result

    @builtins.property
    def on_update(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is updated.

        :default: - no call
        """
        result = self._values.get("on_update")
        return result

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        """Cloudformation Resource type.

        :default: - Custom::AWS
        """
        result = self._values.get("resource_type")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The execution role for the Lambda function implementing this custom resource provider.

        This role will apply to all ``AwsCustomResource``
        instances in the stack. The role must be assumable by the
        ``lambda.amazonaws.com`` service principal.

        :default: - a new role is created
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The timeout for the Lambda function implementing this custom resource.

        :default: Duration.minutes(2)
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/custom-resources.AwsSdkCall",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "ignore_error_codes_matching": "ignoreErrorCodesMatching",
        "output_path": "outputPath",
        "parameters": "parameters",
        "physical_resource_id": "physicalResourceId",
        "region": "region",
    },
)
class AwsSdkCall:
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        ignore_error_codes_matching: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        physical_resource_id: typing.Optional["PhysicalResourceId"] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """An AWS SDK call.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param ignore_error_codes_matching: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param output_path: Restrict the data returned by the custom resource to a specific path in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent' Default: - return all data
        :param parameters: The parameters for the service action. Default: - no parameters
        :param physical_resource_id: The physical resource id of the custom resource for this call. Mandatory for onCreate or onUpdate calls. Default: - no physical resource id
        :param region: The region to send service requests to. **Note: Cross-region operations are generally considered an anti-pattern.** **Consider first deploying a stack in that region.** Default: - the region where this custom resource is deployed
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if ignore_error_codes_matching is not None:
            self._values["ignore_error_codes_matching"] = ignore_error_codes_matching
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if physical_resource_id is not None:
            self._values["physical_resource_id"] = physical_resource_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def action(self) -> builtins.str:
        """The service action to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return result

    @builtins.property
    def service(self) -> builtins.str:
        """The service to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return result

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        """API version to use for the service.

        :default: - use latest available API version

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        """
        result = self._values.get("api_version")
        return result

    @builtins.property
    def ignore_error_codes_matching(self) -> typing.Optional[builtins.str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors
        """
        result = self._values.get("ignore_error_codes_matching")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """Restrict the data returned by the custom resource to a specific path in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent'

        :default: - return all data
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        :default: - no parameters

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def physical_resource_id(self) -> typing.Optional["PhysicalResourceId"]:
        """The physical resource id of the custom resource for this call.

        Mandatory for onCreate or onUpdate calls.

        :default: - no physical resource id
        """
        result = self._values.get("physical_resource_id")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The region to send service requests to.

        **Note: Cross-region operations are generally considered an anti-pattern.**
        **Consider first deploying a stack in that region.**

        :default: - the region where this custom resource is deployed
        """
        result = self._values.get("region")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsSdkCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PhysicalResourceId(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/custom-resources.PhysicalResourceId",
):
    """Physical ID of the custom resource."""

    @jsii.member(jsii_name="fromResponse")
    @builtins.classmethod
    def from_response(cls, response_path: builtins.str) -> "PhysicalResourceId":
        """Extract the physical resource id from the path (dot notation) to the data in the API call response.

        :param response_path: -
        """
        return jsii.sinvoke(cls, "fromResponse", [response_path])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, id: builtins.str) -> "PhysicalResourceId":
        """Explicit physical resource id.

        :param id: -
        """
        return jsii.sinvoke(cls, "of", [id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[builtins.str]:
        """Literal string to be used as the physical id."""
        return jsii.get(self, "id")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="responsePath")
    def response_path(self) -> typing.Optional[builtins.str]:
        """Path to a response data element to be used as the physical id."""
        return jsii.get(self, "responsePath")


class PhysicalResourceIdReference(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/custom-resources.PhysicalResourceIdReference",
):
    """Reference to the physical resource id that can be passed to the AWS operation as a parameter."""

    def __init__(self) -> None:
        jsii.create(PhysicalResourceIdReference, self, [])

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        """toJSON serialization to replace ``PhysicalResourceIdReference`` with a magic string."""
        return jsii.invoke(self, "toJSON", [])


@jsii.implements(aws_cdk.aws_cloudformation.ICustomResourceProvider)
class Provider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/custom-resources.Provider",
):
    """Defines an AWS CloudFormation custom resource provider."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        on_event_handler: aws_cdk.aws_lambda.IFunction,
        is_complete_handler: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        query_interval: typing.Optional[aws_cdk.core.Duration] = None,
        total_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param on_event_handler: The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param log_retention: The number of days framework log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param query_interval: Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param total_timeout: Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)
        """
        props = ProviderProps(
            on_event_handler=on_event_handler,
            is_complete_handler=is_complete_handler,
            log_retention=log_retention,
            query_interval=query_interval,
            total_timeout=total_timeout,
        )

        jsii.create(Provider, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_cloudformation.CustomResourceProviderConfig:
        """(deprecated) Called by ``CustomResource`` which uses this provider.

        :param _: -

        :deprecated: use ``provider.serviceToken`` instead

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="onEventHandler")
    def on_event_handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The user-defined AWS Lambda function which is invoked for all resource lifecycle operations (CREATE/UPDATE/DELETE)."""
        return jsii.get(self, "onEventHandler")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        """The service token to use in order to define custom resources that are backed by this provider."""
        return jsii.get(self, "serviceToken")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="isCompleteHandler")
    def is_complete_handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """The user-defined AWS Lambda function which is invoked asynchronously in order to determine if the operation is complete."""
        return jsii.get(self, "isCompleteHandler")


@jsii.data_type(
    jsii_type="@aws-cdk/custom-resources.ProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "on_event_handler": "onEventHandler",
        "is_complete_handler": "isCompleteHandler",
        "log_retention": "logRetention",
        "query_interval": "queryInterval",
        "total_timeout": "totalTimeout",
    },
)
class ProviderProps:
    def __init__(
        self,
        *,
        on_event_handler: aws_cdk.aws_lambda.IFunction,
        is_complete_handler: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        query_interval: typing.Optional[aws_cdk.core.Duration] = None,
        total_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Initialization properties for the ``Provider`` construct.

        :param on_event_handler: The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param log_retention: The number of days framework log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param query_interval: Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param total_timeout: Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)
        """
        self._values: typing.Dict[str, typing.Any] = {
            "on_event_handler": on_event_handler,
        }
        if is_complete_handler is not None:
            self._values["is_complete_handler"] = is_complete_handler
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if query_interval is not None:
            self._values["query_interval"] = query_interval
        if total_timeout is not None:
            self._values["total_timeout"] = total_timeout

    @builtins.property
    def on_event_handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE).

        This function is responsible to begin the requested resource operation
        (CREATE/UPDATE/DELETE) and return any additional properties to add to the
        event, which will later be passed to ``isComplete``. The ``PhysicalResourceId``
        property must be included in the response.
        """
        result = self._values.get("on_event_handler")
        assert result is not None, "Required property 'on_event_handler' is missing"
        return result

    @builtins.property
    def is_complete_handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """The AWS Lambda function to invoke in order to determine if the operation is complete.

        This function will be called immediately after ``onEvent`` and then
        periodically based on the configured query interval as long as it returns
        ``false``. If the function still returns ``false`` and the alloted timeout has
        passed, the operation will fail.

        :default:

        - provider is synchronous. This means that the ``onEvent`` handler
        is expected to finish all lifecycle operations within the initial invocation.
        """
        result = self._values.get("is_complete_handler")
        return result

    @builtins.property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        """The number of days framework log events are kept in CloudWatch Logs.

        When
        updating this property, unsetting it doesn't remove the log retention policy.
        To remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE
        """
        result = self._values.get("log_retention")
        return result

    @builtins.property
    def query_interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized.

        The first ``isComplete`` will be called immediately after ``handler`` and then
        every ``queryInterval`` seconds, and until ``timeout`` has been reached or until
        ``isComplete`` returns ``true``.

        :default: Duration.seconds(5)
        """
        result = self._values.get("query_interval")
        return result

    @builtins.property
    def total_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Total timeout for the entire operation.

        The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes)

        :default: Duration.minutes(30)
        """
        result = self._values.get("total_timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/custom-resources.SdkCallsPolicyOptions",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources"},
)
class SdkCallsPolicyOptions:
    def __init__(self, *, resources: typing.List[builtins.str]) -> None:
        """Options for the auto-generation of policies based on the configured SDK calls.

        :param resources: The resources that the calls will have access to. It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE`` to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't know the physical name of in advance. Note that will apply to ALL SDK calls.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "resources": resources,
        }

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        """The resources that the calls will have access to.

        It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE``
        to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't
        know the physical name of in advance.

        Note that will apply to ALL SDK calls.
        """
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SdkCallsPolicyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCustomResource",
    "AwsCustomResourcePolicy",
    "AwsCustomResourceProps",
    "AwsSdkCall",
    "PhysicalResourceId",
    "PhysicalResourceIdReference",
    "Provider",
    "ProviderProps",
    "SdkCallsPolicyOptions",
]

publication.publish()
