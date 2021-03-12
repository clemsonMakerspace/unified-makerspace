"""
## AWS S3 Deployment Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

> **Status: Experimental**

This library allows populating an S3 bucket with the contents of .zip files
from other S3 buckets or from local disk.

The following example defines a publicly accessible S3 bucket with web hosting
enabled and populates it from a local directory on disk.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
website_bucket = s3.Bucket(self, "WebsiteBucket",
    website_index_document="index.html",
    public_read_access=True
)

s3deploy.BucketDeployment(self, "DeployWebsite",
    sources=[s3deploy.Source.asset("./website-dist")],
    destination_bucket=website_bucket,
    destination_key_prefix="web/static"
)
```

This is what happens under the hood:

1. When this stack is deployed (either via `cdk deploy` or via CI/CD), the
   contents of the local `website-dist` directory will be archived and uploaded
   to an intermediary assets bucket. If there is more than one source, they will
   be individually uploaded.
2. The `BucketDeployment` construct synthesizes a custom CloudFormation resource
   of type `Custom::CDKBucketDeployment` into the template. The source bucket/key
   is set to point to the assets bucket.
3. The custom resource downloads the .zip archive, extracts it and issues `aws s3 sync --delete` against the destination bucket (in this case
   `websiteBucket`). If there is more than one source, the sources will be
   downloaded and merged pre-deployment at this step.

## Supported sources

The following source types are supported for bucket deployments:

* Local .zip file: `s3deploy.Source.asset('/path/to/local/file.zip')`
* Local directory: `s3deploy.Source.asset('/path/to/local/directory')`
* Another bucket: `s3deploy.Source.bucket(bucket, zipObjectKey)`

To create a source from a single file, you can pass `AssetOptions` to exclude
all but a single file:

* Single file: `s3deploy.Source.asset('/path/to/local/directory', { exclude: ['**', '!onlyThisFile.txt'] })`

## Retain on Delete

By default, the contents of the destination bucket will **not** be deleted when the
`BucketDeployment` resource is removed from the stack or when the destination is
changed. You can use the option `retainOnDelete: false` to disable this behavior,
in which case the contents will be deleted.

## Prune

By default, files in the destination bucket that don't exist in the source will be deleted
when the `BucketDeployment` resource is created or updated. You can use the option `prune: false` to disable
this behavior, in which case the files will not be deleted.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
s3deploy.BucketDeployment(self, "DeployMeWithoutDeletingFilesOnDestination",
    sources=[s3deploy.Source.asset(path.join(__dirname, "my-website"))],
    destination_bucket=destination_bucket,
    prune=False
)
```

This option also enables you to specify multiple bucket deployments for the same destination bucket & prefix,
each with its own characteristics. For example, you can set different cache-control headers
based on file extensions:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
BucketDeployment(self, "BucketDeployment",
    sources=[Source.asset("./website", exclude=["index.html"])],
    destination_bucket=bucket,
    cache_control=[CacheControl.from_string("max-age=31536000,public,immutable")],
    prune=False
)

BucketDeployment(self, "HTMLBucketDeployment",
    sources=[Source.asset("./website", exclude=["*", "!index.html"])],
    destination_bucket=bucket,
    cache_control=[CacheControl.from_string("max-age=0,no-cache,no-store,must-revalidate")],
    prune=False
)
```

## Objects metadata

You can specify metadata to be set on all the objects in your deployment.
There are 2 types of metadata in S3: system-defined metadata and user-defined metadata.
System-defined metadata have a special purpose, for example cache-control defines how long to keep an object cached.
User-defined metadata are not used by S3 and keys always begin with `x-amzn-meta-` (if this is not provided, it is added automatically).

System defined metadata keys include the following:

* cache-control
* content-disposition
* content-encoding
* content-language
* content-type
* expires
* server-side-encryption
* storage-class
* website-redirect-location
* ssekms-key-id
* sse-customer-algorithm

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
website_bucket = s3.Bucket(self, "WebsiteBucket",
    website_index_document="index.html",
    public_read_access=True
)

s3deploy.BucketDeployment(self, "DeployWebsite",
    sources=[s3deploy.Source.asset("./website-dist")],
    destination_bucket=website_bucket,
    destination_key_prefix="web/static", # optional prefix in destination bucket
    metadata={"A": "1", "b": "2"}, # user-defined metadata

    # system-defined metadata
    content_type="text/html",
    content_language="en",
    storage_class=StorageClass.INTELLIGENT_TIERING,
    server_side_encryption=ServerSideEncryption.AES_256,
    cache_control=[CacheControl.set_public(), CacheControl.max_age(cdk.Duration.hours(1))]
)
```

## CloudFront Invalidation

You can provide a CloudFront distribution and optional paths to invalidate after the bucket deployment finishes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins

bucket = s3.Bucket(self, "Destination")

# Option 1 (Experimental): Handles buckets whether or not they are configured for website hosting.
distribution = cloudfront.Distribution(self, "Distribution",
    default_behavior=BehaviorOptions(origin=origins.S3Origin(bucket))
)

# Option 2 (Stable): Use this if the bucket has website hosting enabled.
distribution_for_website_bucket = cloudfront.CloudFrontWebDistribution(self, "DistributionForWebBucket",
    origin_configs=[SourceConfiguration(
        custom_origin_source=CustomOriginConfig(
            domain_name=bucket.bucket_website_domain_name
        ),
        behaviors=[Behavior(is_default_behavior=True)]
    )
    ]
)

# Option 3 (Stable): Use this version if the bucket does not have website hosting enabled.
distribution_for_bucket = cloudfront.CloudFrontWebDistribution(self, "DistributionForBucket",
    origin_configs=[SourceConfiguration(
        s3_origin_source=S3OriginConfig(
            s3_bucket_source=bucket
        ),
        behaviors=[Behavior(is_default_behavior=True)]
    )
    ]
)

s3deploy.BucketDeployment(self, "DeployWithInvalidation",
    sources=[s3deploy.Source.asset("./website-dist")],
    destination_bucket=bucket,
    distribution=distribution, # or distribution_for_website_bucket or distribution_for_bucket
    distribution_paths=["/images/*.png"]
)
```

## Memory Limit

The default memory limit for the deployment resource is 128MiB. If you need to
copy larger files, you can use the `memoryLimit` configuration to specify the
size of the AWS Lambda resource handler.

> NOTE: a new AWS Lambda handler will be created in your stack for each memory
> limit configuration.

## Notes

* This library uses an AWS CloudFormation custom resource which about 10MiB in
  size. The code of this resource is bundled with this library.
* AWS Lambda execution time is limited to 15min. This limits the amount of data which can
  be deployed into the bucket by this timeout.
* When the `BucketDeployment` is removed from the stack, the contents are retained
  in the destination bucket ([#952](https://github.com/aws/aws-cdk/issues/952)).
* Bucket deployment *only happens* during stack create/update. This means that
  if you wish to update the contents of the destination, you will need to
  change the source s3 key (or bucket), so that the resource will be updated.
  This is inline with best practices. If you use local disk assets, this will
  happen automatically whenever you modify the asset, since the S3 key is based
  on a hash of the asset contents.

## Development

The custom resource is implemented in Python 3.6 in order to be able to leverage
the AWS CLI for "aws sync". The code is under [`lambda/src`](./lambda/src) and
unit tests are under [`lambda/test`](./lambda/test).

This package requires Python 3.6 during build time in order to create the custom
resource Lambda bundle and test it. It also relies on a few bash scripts, so
might be tricky to build on Windows.

## Roadmap

* [ ] Support "progressive" mode (no `--delete`) ([#953](https://github.com/aws/aws-cdk/issues/953))
* [ ] Support "blue/green" deployments ([#954](https://github.com/aws/aws-cdk/issues/954))
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

import aws_cdk.assets
import aws_cdk.aws_cloudfront
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.aws_s3_assets
import aws_cdk.core
import constructs


class BucketDeployment(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3-deployment.BucketDeployment",
):
    """
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        destination_bucket: aws_cdk.aws_s3.IBucket,
        sources: typing.List["ISource"],
        cache_control: typing.Optional[typing.List["CacheControl"]] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        destination_key_prefix: typing.Optional[builtins.str] = None,
        distribution: typing.Optional[aws_cdk.aws_cloudfront.IDistribution] = None,
        distribution_paths: typing.Optional[typing.List[builtins.str]] = None,
        expires: typing.Optional[aws_cdk.core.Expiration] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional["UserDefinedObjectMetadata"] = None,
        prune: typing.Optional[builtins.bool] = None,
        retain_on_delete: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        server_side_encryption: typing.Optional["ServerSideEncryption"] = None,
        server_side_encryption_aws_kms_key_id: typing.Optional[builtins.str] = None,
        server_side_encryption_customer_algorithm: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional["StorageClass"] = None,
        website_redirect_location: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param destination_bucket: (experimental) The S3 bucket to sync the contents of the zip file to.
        :param sources: (experimental) The sources from which to deploy the contents of this bucket.
        :param cache_control: (experimental) System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: (experimental) System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: (experimental) System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: (experimental) System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: (experimental) System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_key_prefix: (experimental) Key prefix in the destination bucket. Default: "/" (unzip to root of the destination bucket)
        :param distribution: (experimental) The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: (experimental) The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param expires: (experimental) System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param memory_limit: (experimental) The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: (experimental) User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param prune: (experimental) If this is set to false, files in the destination bucket that do not exist in the asset, will NOT be deleted during deployment (create/update). Default: true
        :param retain_on_delete: (experimental) If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: if this is set to "false" and destination bucket/prefix is updated, all files in the previous destination will first be deleted and then uploaded to the new destination location. This could have availablity implications on your users. Default: true - when resource is deleted/updated, files are retained
        :param role: (experimental) Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: (experimental) System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: (experimental) System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: (experimental) System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080 Default: - Not set.
        :param storage_class: (experimental) System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param website_redirect_location: (experimental) System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.

        :stability: experimental
        """
        props = BucketDeploymentProps(
            destination_bucket=destination_bucket,
            sources=sources,
            cache_control=cache_control,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_language=content_language,
            content_type=content_type,
            destination_key_prefix=destination_key_prefix,
            distribution=distribution,
            distribution_paths=distribution_paths,
            expires=expires,
            memory_limit=memory_limit,
            metadata=metadata,
            prune=prune,
            retain_on_delete=retain_on_delete,
            role=role,
            server_side_encryption=server_side_encryption,
            server_side_encryption_aws_kms_key_id=server_side_encryption_aws_kms_key_id,
            server_side_encryption_customer_algorithm=server_side_encryption_customer_algorithm,
            storage_class=storage_class,
            website_redirect_location=website_redirect_location,
        )

        jsii.create(BucketDeployment, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3-deployment.BucketDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_bucket": "destinationBucket",
        "sources": "sources",
        "cache_control": "cacheControl",
        "content_disposition": "contentDisposition",
        "content_encoding": "contentEncoding",
        "content_language": "contentLanguage",
        "content_type": "contentType",
        "destination_key_prefix": "destinationKeyPrefix",
        "distribution": "distribution",
        "distribution_paths": "distributionPaths",
        "expires": "expires",
        "memory_limit": "memoryLimit",
        "metadata": "metadata",
        "prune": "prune",
        "retain_on_delete": "retainOnDelete",
        "role": "role",
        "server_side_encryption": "serverSideEncryption",
        "server_side_encryption_aws_kms_key_id": "serverSideEncryptionAwsKmsKeyId",
        "server_side_encryption_customer_algorithm": "serverSideEncryptionCustomerAlgorithm",
        "storage_class": "storageClass",
        "website_redirect_location": "websiteRedirectLocation",
    },
)
class BucketDeploymentProps:
    def __init__(
        self,
        *,
        destination_bucket: aws_cdk.aws_s3.IBucket,
        sources: typing.List["ISource"],
        cache_control: typing.Optional[typing.List["CacheControl"]] = None,
        content_disposition: typing.Optional[builtins.str] = None,
        content_encoding: typing.Optional[builtins.str] = None,
        content_language: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
        destination_key_prefix: typing.Optional[builtins.str] = None,
        distribution: typing.Optional[aws_cdk.aws_cloudfront.IDistribution] = None,
        distribution_paths: typing.Optional[typing.List[builtins.str]] = None,
        expires: typing.Optional[aws_cdk.core.Expiration] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional["UserDefinedObjectMetadata"] = None,
        prune: typing.Optional[builtins.bool] = None,
        retain_on_delete: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        server_side_encryption: typing.Optional["ServerSideEncryption"] = None,
        server_side_encryption_aws_kms_key_id: typing.Optional[builtins.str] = None,
        server_side_encryption_customer_algorithm: typing.Optional[builtins.str] = None,
        storage_class: typing.Optional["StorageClass"] = None,
        website_redirect_location: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param destination_bucket: (experimental) The S3 bucket to sync the contents of the zip file to.
        :param sources: (experimental) The sources from which to deploy the contents of this bucket.
        :param cache_control: (experimental) System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: (experimental) System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: (experimental) System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: (experimental) System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: (experimental) System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_key_prefix: (experimental) Key prefix in the destination bucket. Default: "/" (unzip to root of the destination bucket)
        :param distribution: (experimental) The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: (experimental) The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param expires: (experimental) System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param memory_limit: (experimental) The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: (experimental) User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param prune: (experimental) If this is set to false, files in the destination bucket that do not exist in the asset, will NOT be deleted during deployment (create/update). Default: true
        :param retain_on_delete: (experimental) If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: if this is set to "false" and destination bucket/prefix is updated, all files in the previous destination will first be deleted and then uploaded to the new destination location. This could have availablity implications on your users. Default: true - when resource is deleted/updated, files are retained
        :param role: (experimental) Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: (experimental) System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: (experimental) System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: (experimental) System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080 Default: - Not set.
        :param storage_class: (experimental) System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param website_redirect_location: (experimental) System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.

        :stability: experimental
        """
        if isinstance(metadata, dict):
            metadata = UserDefinedObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "destination_bucket": destination_bucket,
            "sources": sources,
        }
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if content_disposition is not None:
            self._values["content_disposition"] = content_disposition
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding
        if content_language is not None:
            self._values["content_language"] = content_language
        if content_type is not None:
            self._values["content_type"] = content_type
        if destination_key_prefix is not None:
            self._values["destination_key_prefix"] = destination_key_prefix
        if distribution is not None:
            self._values["distribution"] = distribution
        if distribution_paths is not None:
            self._values["distribution_paths"] = distribution_paths
        if expires is not None:
            self._values["expires"] = expires
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if metadata is not None:
            self._values["metadata"] = metadata
        if prune is not None:
            self._values["prune"] = prune
        if retain_on_delete is not None:
            self._values["retain_on_delete"] = retain_on_delete
        if role is not None:
            self._values["role"] = role
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if server_side_encryption_aws_kms_key_id is not None:
            self._values["server_side_encryption_aws_kms_key_id"] = server_side_encryption_aws_kms_key_id
        if server_side_encryption_customer_algorithm is not None:
            self._values["server_side_encryption_customer_algorithm"] = server_side_encryption_customer_algorithm
        if storage_class is not None:
            self._values["storage_class"] = storage_class
        if website_redirect_location is not None:
            self._values["website_redirect_location"] = website_redirect_location

    @builtins.property
    def destination_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """(experimental) The S3 bucket to sync the contents of the zip file to.

        :stability: experimental
        """
        result = self._values.get("destination_bucket")
        assert result is not None, "Required property 'destination_bucket' is missing"
        return result

    @builtins.property
    def sources(self) -> typing.List["ISource"]:
        """(experimental) The sources from which to deploy the contents of this bucket.

        :stability: experimental
        """
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return result

    @builtins.property
    def cache_control(self) -> typing.Optional[typing.List["CacheControl"]]:
        """(experimental) System-defined cache-control metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("cache_control")
        return result

    @builtins.property
    def content_disposition(self) -> typing.Optional[builtins.str]:
        """(experimental) System-defined cache-disposition metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("content_disposition")
        return result

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        """(experimental) System-defined content-encoding metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("content_encoding")
        return result

    @builtins.property
    def content_language(self) -> typing.Optional[builtins.str]:
        """(experimental) System-defined content-language metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("content_language")
        return result

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        """(experimental) System-defined content-type metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("content_type")
        return result

    @builtins.property
    def destination_key_prefix(self) -> typing.Optional[builtins.str]:
        """(experimental) Key prefix in the destination bucket.

        :default: "/" (unzip to root of the destination bucket)

        :stability: experimental
        """
        result = self._values.get("destination_key_prefix")
        return result

    @builtins.property
    def distribution(self) -> typing.Optional[aws_cdk.aws_cloudfront.IDistribution]:
        """(experimental) The CloudFront distribution using the destination bucket as an origin.

        Files in the distribution's edge caches will be invalidated after
        files are uploaded to the destination bucket.

        :default: - No invalidation occurs

        :stability: experimental
        """
        result = self._values.get("distribution")
        return result

    @builtins.property
    def distribution_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The file paths to invalidate in the CloudFront distribution.

        :default: - All files under the destination bucket key prefix will be invalidated.

        :stability: experimental
        """
        result = self._values.get("distribution_paths")
        return result

    @builtins.property
    def expires(self) -> typing.Optional[aws_cdk.core.Expiration]:
        """(experimental) System-defined expires metadata to be set on all objects in the deployment.

        :default: - The objects in the distribution will not expire.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("expires")
        return result

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """(experimental) The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket.

        If you are deploying large files, you will need to increase this number
        accordingly.

        :default: 128

        :stability: experimental
        """
        result = self._values.get("memory_limit")
        return result

    @builtins.property
    def metadata(self) -> typing.Optional["UserDefinedObjectMetadata"]:
        """(experimental) User-defined object metadata to be set on all objects in the deployment.

        :default: - No user metadata is set

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#UserMetadata
        :stability: experimental
        """
        result = self._values.get("metadata")
        return result

    @builtins.property
    def prune(self) -> typing.Optional[builtins.bool]:
        """(experimental) If this is set to false, files in the destination bucket that do not exist in the asset, will NOT be deleted during deployment (create/update).

        :default: true

        :see: https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html
        :stability: experimental
        """
        result = self._values.get("prune")
        return result

    @builtins.property
    def retain_on_delete(self) -> typing.Optional[builtins.bool]:
        """(experimental) If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated.

        NOTICE: if this is set to "false" and destination bucket/prefix is updated,
        all files in the previous destination will first be deleted and then
        uploaded to the new destination location. This could have availablity
        implications on your users.

        :default: true - when resource is deleted/updated, files are retained

        :stability: experimental
        """
        result = self._values.get("retain_on_delete")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) Execution role associated with this function.

        :default: - A role is automatically created

        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def server_side_encryption(self) -> typing.Optional["ServerSideEncryption"]:
        """(experimental) System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment.

        :default: - Server side encryption is not used.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("server_side_encryption")
        return result

    @builtins.property
    def server_side_encryption_aws_kms_key_id(self) -> typing.Optional[builtins.str]:
        """(experimental) System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment.

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("server_side_encryption_aws_kms_key_id")
        return result

    @builtins.property
    def server_side_encryption_customer_algorithm(
        self,
    ) -> typing.Optional[builtins.str]:
        """(experimental) System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment.

        Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080

        :default: - Not set.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html#sse-c-how-to-programmatically-intro
        :stability: experimental
        """
        result = self._values.get("server_side_encryption_customer_algorithm")
        return result

    @builtins.property
    def storage_class(self) -> typing.Optional["StorageClass"]:
        """(experimental) System-defined x-amz-storage-class metadata to be set on all objects in the deployment.

        :default: - Default storage-class for the bucket is used.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("storage_class")
        return result

    @builtins.property
    def website_redirect_location(self) -> typing.Optional[builtins.str]:
        """(experimental) System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment.

        :default: - No website redirection.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        :stability: experimental
        """
        result = self._values.get("website_redirect_location")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CacheControl(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3-deployment.CacheControl",
):
    """(experimental) Used for HTTP cache-control header, which influences downstream caches.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    :stability: experimental
    """

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, s: builtins.str) -> "CacheControl":
        """
        :param s: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromString", [s])

    @jsii.member(jsii_name="maxAge")
    @builtins.classmethod
    def max_age(cls, t: aws_cdk.core.Duration) -> "CacheControl":
        """
        :param t: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "maxAge", [t])

    @jsii.member(jsii_name="mustRevalidate")
    @builtins.classmethod
    def must_revalidate(cls) -> "CacheControl":
        """
        :stability: experimental
        """
        return jsii.sinvoke(cls, "mustRevalidate", [])

    @jsii.member(jsii_name="noCache")
    @builtins.classmethod
    def no_cache(cls) -> "CacheControl":
        """
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noCache", [])

    @jsii.member(jsii_name="noTransform")
    @builtins.classmethod
    def no_transform(cls) -> "CacheControl":
        """
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noTransform", [])

    @jsii.member(jsii_name="proxyRevalidate")
    @builtins.classmethod
    def proxy_revalidate(cls) -> "CacheControl":
        """
        :stability: experimental
        """
        return jsii.sinvoke(cls, "proxyRevalidate", [])

    @jsii.member(jsii_name="setPrivate")
    @builtins.classmethod
    def set_private(cls) -> "CacheControl":
        """
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPrivate", [])

    @jsii.member(jsii_name="setPublic")
    @builtins.classmethod
    def set_public(cls) -> "CacheControl":
        """
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPublic", [])

    @jsii.member(jsii_name="sMaxAge")
    @builtins.classmethod
    def s_max_age(cls, t: aws_cdk.core.Duration) -> "CacheControl":
        """
        :param t: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "sMaxAge", [t])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """
        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3-deployment.DeploymentSourceContext",
    jsii_struct_bases=[],
    name_mapping={"handler_role": "handlerRole"},
)
class DeploymentSourceContext:
    def __init__(self, *, handler_role: aws_cdk.aws_iam.IRole) -> None:
        """(experimental) Bind context for ISources.

        :param handler_role: (experimental) The role for the handler.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "handler_role": handler_role,
        }

    @builtins.property
    def handler_role(self) -> aws_cdk.aws_iam.IRole:
        """(experimental) The role for the handler.

        :stability: experimental
        """
        result = self._values.get("handler_role")
        assert result is not None, "Required property 'handler_role' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentSourceContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Expires(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.Expires"):
    """(deprecated) Used for HTTP expires header, which influences downstream caches.

    Does NOT influence deletion of the object.

    :deprecated: use core.Expiration

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    :stability: deprecated
    """

    @jsii.member(jsii_name="after")
    @builtins.classmethod
    def after(cls, t: aws_cdk.core.Duration) -> "Expires":
        """(deprecated) Expire once the specified duration has passed since deployment time.

        :param t: the duration to wait before expiring.

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "after", [t])

    @jsii.member(jsii_name="atDate")
    @builtins.classmethod
    def at_date(cls, d: datetime.datetime) -> "Expires":
        """(deprecated) Expire at the specified date.

        :param d: date to expire at.

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "atDate", [d])

    @jsii.member(jsii_name="atTimestamp")
    @builtins.classmethod
    def at_timestamp(cls, t: jsii.Number) -> "Expires":
        """(deprecated) Expire at the specified timestamp.

        :param t: timestamp in unix milliseconds.

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "atTimestamp", [t])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, s: builtins.str) -> "Expires":
        """
        :param s: -

        :stability: deprecated
        """
        return jsii.sinvoke(cls, "fromString", [s])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """
        :stability: deprecated
        """
        return jsii.get(self, "value")


@jsii.interface(jsii_type="@aws-cdk/aws-s3-deployment.ISource")
class ISource(typing_extensions.Protocol):
    """(experimental) Represents a source for bucket deployments.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        *,
        handler_role: aws_cdk.aws_iam.IRole,
    ) -> "SourceConfig":
        """(experimental) Binds the source to a bucket deployment.

        :param scope: The construct tree context.
        :param handler_role: (experimental) The role for the handler.

        :stability: experimental
        """
        ...


class _ISourceProxy:
    """(experimental) Represents a source for bucket deployments.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-s3-deployment.ISource"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        *,
        handler_role: aws_cdk.aws_iam.IRole,
    ) -> "SourceConfig":
        """(experimental) Binds the source to a bucket deployment.

        :param scope: The construct tree context.
        :param handler_role: (experimental) The role for the handler.

        :stability: experimental
        """
        context = DeploymentSourceContext(handler_role=handler_role)

        return jsii.invoke(self, "bind", [scope, context])


@jsii.enum(jsii_type="@aws-cdk/aws-s3-deployment.ServerSideEncryption")
class ServerSideEncryption(enum.Enum):
    """(experimental) Indicates whether server-side encryption is enabled for the object, and whether that encryption is from the AWS Key Management Service (AWS KMS) or from Amazon S3 managed encryption (SSE-S3).

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    :stability: experimental
    """

    AES_256 = "AES_256"
    """
    :stability: experimental
    """
    AWS_KMS = "AWS_KMS"
    """
    :stability: experimental
    """


class Source(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.Source"):
    """(experimental) Specifies bucket deployment source.

    Usage::

        Source.bucket(bucket, key)
        Source.asset('/local/path/to/directory')
        Source.asset('/local/path/to/a/file.zip')

    :stability: experimental
    """

    @jsii.member(jsii_name="asset")
    @builtins.classmethod
    def asset(
        cls,
        path: builtins.str,
        *,
        readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[aws_cdk.assets.FollowMode] = None,
        ignore_mode: typing.Optional[aws_cdk.core.IgnoreMode] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[aws_cdk.core.AssetHashType] = None,
        bundling: typing.Optional[aws_cdk.core.BundlingOptions] = None,
    ) -> ISource:
        """(experimental) Uses a local asset as the deployment source.

        :param path: The path to a local .zip file or a directory.
        :param readers: (experimental) A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: (experimental) Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        :stability: experimental
        """
        options = aws_cdk.aws_s3_assets.AssetOptions(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        return jsii.sinvoke(cls, "asset", [path, options])

    @jsii.member(jsii_name="bucket")
    @builtins.classmethod
    def bucket(
        cls,
        bucket: aws_cdk.aws_s3.IBucket,
        zip_object_key: builtins.str,
    ) -> ISource:
        """(experimental) Uses a .zip file stored in an S3 bucket as the source for the destination bucket contents.

        :param bucket: The S3 Bucket.
        :param zip_object_key: The S3 object key of the zip file with contents.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "bucket", [bucket, zip_object_key])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3-deployment.SourceConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "zip_object_key": "zipObjectKey"},
)
class SourceConfig:
    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        zip_object_key: builtins.str,
    ) -> None:
        """
        :param bucket: (experimental) The source bucket to deploy from.
        :param zip_object_key: (experimental) An S3 object key in the source bucket that points to a zip file.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "zip_object_key": zip_object_key,
        }

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """(experimental) The source bucket to deploy from.

        :stability: experimental
        """
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return result

    @builtins.property
    def zip_object_key(self) -> builtins.str:
        """(experimental) An S3 object key in the source bucket that points to a zip file.

        :stability: experimental
        """
        result = self._values.get("zip_object_key")
        assert result is not None, "Required property 'zip_object_key' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-s3-deployment.StorageClass")
class StorageClass(enum.Enum):
    """(experimental) Storage class used for storing the object.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    :stability: experimental
    """

    STANDARD = "STANDARD"
    """
    :stability: experimental
    """
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    """
    :stability: experimental
    """
    STANDARD_IA = "STANDARD_IA"
    """
    :stability: experimental
    """
    ONEZONE_IA = "ONEZONE_IA"
    """
    :stability: experimental
    """
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    """
    :stability: experimental
    """
    GLACIER = "GLACIER"
    """
    :stability: experimental
    """
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    """
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3-deployment.UserDefinedObjectMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserDefinedObjectMetadata:
    def __init__(self) -> None:
        """
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserDefinedObjectMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BucketDeployment",
    "BucketDeploymentProps",
    "CacheControl",
    "DeploymentSourceContext",
    "Expires",
    "ISource",
    "ServerSideEncryption",
    "Source",
    "SourceConfig",
    "StorageClass",
    "UserDefinedObjectMetadata",
]

publication.publish()
