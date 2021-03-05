"""
## Amazon CloudFront Construct Library

<!--BEGIN STABILITY BANNER-->---


| Features | Stability |
| --- | --- |
| CFN Resources | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge) |
| Higher level constructs for Distribution | ![Developer Preview](https://img.shields.io/badge/developer--preview-informational.svg?style=for-the-badge) |
| Higher level constructs for CloudFrontWebDistribution | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge) |

> **CFN Resources:** All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

> **Developer Preview:** Higher level constructs in this module that are marked as developer preview have completed their phase of active development and are looking for adoption and feedback. While the same caveats around non-backward compatible as Experimental constructs apply, they will undergo fewer breaking changes. Just as with Experimental constructs, these are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes.

> **Stable:** Higher level constructs in this module that are marked stable will not undergo any breaking changes. They will strictly follow the [Semantic Versioning](https://semver.org/) model.

---
<!--END STABILITY BANNER-->

Amazon CloudFront is a web service that speeds up distribution of your static and dynamic web content, such as .html, .css, .js, and image files, to
your users. CloudFront delivers your content through a worldwide network of data centers called edge locations. When a user requests content that
you're serving with CloudFront, the user is routed to the edge location that provides the lowest latency, so that content is delivered with the best
possible performance.

## Distribution API - Developer Preview

![Developer Preview](https://img.shields.io/badge/developer--preview-informational.svg?style=for-the-badge)

The `Distribution` API is currently being built to replace the existing `CloudFrontWebDistribution` API. The `Distribution` API is optimized for the
most common use cases of CloudFront distributions (e.g., single origin and behavior, few customizations) while still providing the ability for more
advanced use cases. The API focuses on simplicity for the common use cases, and convenience methods for creating the behaviors and origins necessary
for more complex use cases.

### Creating a distribution

CloudFront distributions deliver your content from one or more origins; an origin is the location where you store the original version of your
content. Origins can be created from S3 buckets or a custom origin (HTTP server). Constructs to define origins are in the `@aws-cdk/aws-cloudfront-origins` module.

Each distribution has a default behavior which applies to all requests to that distribution, and routes requests to a primary origin.
Additional behaviors may be specified for an origin with a given URL path pattern. Behaviors allow routing with multiple origins,
controlling which HTTP methods to support, whether to require users to use HTTPS, and what query strings or cookies to forward to your origin,
among other settings.

#### From an S3 Bucket

An S3 bucket can be added as an origin. If the bucket is configured as a website endpoint, the distribution can use S3 redirects and S3 custom error
documents.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins

# Creates a distribution for a S3 bucket.
my_bucket = s3.Bucket(self, "myBucket")
cloudfront.Distribution(self, "myDist",
    default_behavior=BehaviorOptions(origin=origins.S3Origin(my_bucket))
)
```

The above will treat the bucket differently based on if `IBucket.isWebsite` is set or not. If the bucket is configured as a website, the bucket is
treated as an HTTP origin, and the built-in S3 redirects and error pages can be used. Otherwise, the bucket is handled as a bucket origin and
CloudFront's redirect and error handling will be used. In the latter case, the Origin wil create an origin access identity and grant it access to the
underlying bucket. This can be used in conjunction with a bucket that is not public to require that your users access your content using CloudFront
URLs and not S3 URLs directly.

#### ELBv2 Load Balancer

An Elastic Load Balancing (ELB) v2 load balancer may be used as an origin. In order for a load balancer to serve as an origin, it must be publicly
accessible (`internetFacing` is true). Both Application and Network load balancers are supported.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

vpc = ec2.Vpc(...)
# Create an application load balancer in a VPC. 'internetFacing' must be 'true'
# for CloudFront to access the load balancer and use it as an origin.
lb = elbv2.ApplicationLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": origins.LoadBalancerV2Origin(lb)}
)
```

#### From an HTTP endpoint

Origins can also be created from any other HTTP endpoint, given the domain name, and optionally, other origin properties.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": origins.HttpOrigin("www.example.com")}
)
```

### Domain Names and Certificates

When you create a distribution, CloudFront assigns a domain name for the distribution, for example: `d111111abcdef8.cloudfront.net`; this value can
be retrieved from `distribution.distributionDomainName`. CloudFront distributions use a default certificate (`*.cloudfront.net`) to support HTTPS by
default. If you want to use your own domain name, such as `www.example.com`, you must associate a certificate with your distribution that contains
your domain name, and provide one (or more) domain names from the certificate for the distribution.

The certificate must be present in the AWS Certificate Manager (ACM) service in the US East (N. Virginia) region; the certificate
may either be created by ACM, or created elsewhere and imported into ACM. When a certificate is used, the distribution will support HTTPS connections
from SNI only and a minimum protocol version of TLSv1.2_2019.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_certificate = acm.DnsValidatedCertificate(self, "mySiteCert",
    domain_name="www.example.com",
    hosted_zone=hosted_zone
)
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": origins.S3Origin(my_bucket)},
    domain_names=["www.example.com"],
    certificate=my_certificate
)
```

### Multiple Behaviors & Origins

Each distribution has a default behavior which applies to all requests to that distribution; additional behaviors may be specified for a
given URL path pattern. Behaviors allow routing with multiple origins, controlling which HTTP methods to support, whether to require users to
use HTTPS, and what query strings or cookies to forward to your origin, among others.

The properties of the default behavior can be adjusted as part of the distribution creation. The following example shows configuring the HTTP
methods and viewer protocol policy of the cache.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_web_distribution = cloudfront.Distribution(self, "myDist",
    default_behavior={
        "origin": origins.S3Origin(my_bucket),
        "allowed_methods": AllowedMethods.ALLOW_ALL,
        "viewer_protocol_policy": ViewerProtocolPolicy.REDIRECT_TO_HTTPS
    }
)
```

Additional behaviors can be specified at creation, or added after the initial creation. Each additional behavior is associated with an origin,
and enable customization for a specific set of resources based on a URL path pattern. For example, we can add a behavior to `myWebDistribution` to
override the default viewer protocol policy for all of the images.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_web_distribution.add_behavior("/images/*.jpg", origins.S3Origin(my_bucket),
    viewer_protocol_policy=ViewerProtocolPolicy.REDIRECT_TO_HTTPS
)
```

These behaviors can also be specified at distribution creation time.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket_origin = origins.S3Origin(my_bucket)
cloudfront.Distribution(self, "myDist",
    default_behavior={
        "origin": bucket_origin,
        "allowed_methods": AllowedMethods.ALLOW_ALL,
        "viewer_protocol_policy": ViewerProtocolPolicy.REDIRECT_TO_HTTPS
    },
    additional_behaviors={
        "/images/*.jpg": {
            "origin": bucket_origin,
            "viewer_protocol_policy": ViewerProtocolPolicy.REDIRECT_TO_HTTPS
        }
    }
)
```

### Customizing Cache Keys and TTLs with Cache Policies

You can use a cache policy to improve your cache hit ratio by controlling the values (URL query strings, HTTP headers, and cookies)
that are included in the cache key, and/or adjusting how long items remain in the cache via the time-to-live (TTL) settings.
CloudFront provides some predefined cache policies, known as managed policies, for common use cases. You can use these managed policies,
or you can create your own cache policy that’s specific to your needs.
See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html for more details.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Using an existing cache policy
cloudfront.Distribution(self, "myDistManagedPolicy",
    default_behavior={
        "origin": bucket_origin,
        "cache_policy": cloudfront.CachePolicy.CACHING_OPTIMIZED
    }
)

# Creating a custom cache policy  -- all parameters optional
my_cache_policy = cloudfront.CachePolicy(self, "myCachePolicy",
    cache_policy_name="MyPolicy",
    comment="A default policy",
    default_ttl=Duration.days(2),
    min_ttl=Duration.minutes(1),
    max_ttl=Duration.days(10),
    cookie_behavior=cloudfront.CacheCookieBehavior.all(),
    header_behavior=cloudfront.CacheHeaderBehavior.allow_list("X-CustomHeader"),
    query_string_behavior=cloudfront.CacheQueryStringBehavior.deny_list("username"),
    enable_accept_encoding_gzip=True,
    enable_accept_encoding_brotli=True
)
cloudfront.Distribution(self, "myDistCustomPolicy",
    default_behavior={
        "origin": bucket_origin,
        "cache_policy": my_cache_policy
    }
)
```

### Customizing Origin Requests with Origin Request Policies

When CloudFront makes a request to an origin, the URL path, request body (if present), and a few standard headers are included.
Other information from the viewer request, such as URL query strings, HTTP headers, and cookies, is not included in the origin request by default.
You can use an origin request policy to control the information that’s included in an origin request.
CloudFront provides some predefined origin request policies, known as managed policies, for common use cases. You can use these managed policies,
or you can create your own origin request policy that’s specific to your needs.
See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-origin-requests.html for more details.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Using an existing origin request policy
cloudfront.Distribution(self, "myDistManagedPolicy",
    default_behavior={
        "origin": bucket_origin,
        "origin_request_policy": cloudfront.OriginRequestPolicy.CORS_S3_ORIGIN
    }
)
# Creating a custom origin request policy -- all parameters optional
my_origin_request_policy = cloudfront.OriginRequestPolicy(stack, "OriginRequestPolicy",
    origin_request_policy_name="MyPolicy",
    comment="A default policy",
    cookie_behavior=cloudfront.OriginRequestCookieBehavior.none(),
    header_behavior=cloudfront.OriginRequestHeaderBehavior.all("CloudFront-Is-Android-Viewer"),
    query_string_behavior=cloudfront.OriginRequestQueryStringBehavior.allow_list("username")
)
cloudfront.Distribution(self, "myDistCustomPolicy",
    default_behavior={
        "origin": bucket_origin,
        "cache_policy": my_cache_policy,
        "origin_request_policy": my_origin_request_policy
    }
)
```

### Lambda@Edge

Lambda@Edge is an extension of AWS Lambda, a compute service that lets you execute functions that customize the content that CloudFront delivers.
You can author Node.js or Python functions in the US East (N. Virginia) region,
and then execute them in AWS locations globally that are closer to the viewer,
without provisioning or managing servers.
Lambda@Edge functions are associated with a specific behavior and event type.
Lambda@Edge can be used rewrite URLs,
alter responses based on headers or cookies,
or authorize requests based on headers or authorization tokens.

The following shows a Lambda@Edge function added to the default behavior and triggered on every request:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_func = lambda_.Function(...)
cloudfront.Distribution(self, "myDist",
    default_behavior={
        "origin": origins.S3Origin(my_bucket),
        "edge_lambdas": [{
            "function_version": my_func.current_version,
            "event_type": cloudfront.LambdaEdgeEventType.VIEWER_REQUEST
        }
        ]
    }
)
```

Lambda@Edge functions can also be associated with additional behaviors,
either at Distribution creation time,
or after.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# assigning at Distribution creation
my_origin = origins.S3Origin(my_bucket)
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": my_origin},
    additional_behaviors={
        "images/*": {
            "origin": my_origin,
            "edge_lambdas": [{
                "function_version": my_func.current_version,
                "event_type": cloudfront.LambdaEdgeEventType.ORIGIN_REQUEST,
                "include_body": True
            }
            ]
        }
    }
)

# assigning after creation
my_distribution.add_behavior("images/*", my_origin,
    edge_lambdas=[{
        "function_version": my_func.current_version,
        "event_type": cloudfront.LambdaEdgeEventType.VIEWER_RESPONSE
    }
    ]
)
```

Adding an existing Lambda@Edge function created in a different stack to a CloudFront distribution.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
function_version = lambda_.Version.from_version_arn(self, "Version", "arn:aws:lambda:us-east-1:123456789012:function:functionName:1")

cloudfront.Distribution(self, "distro",
    default_behavior={
        "origin": origins.S3Origin(s3_bucket),
        "edge_lambdas": [{
            "function_version": function_version,
            "event_type": cloudfront.LambdaEdgeEventType.VIEWER_REQUEST
        }
        ]
    }
)
```

### Logging

You can configure CloudFront to create log files that contain detailed information about every user request that CloudFront receives.
The logs can go to either an existing bucket, or a bucket will be created for you.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Simplest form - creates a new bucket and logs to it.
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": origins.HttpOrigin("www.example.com")},
    enable_logging=True
)

# You can optionally log to a specific bucket, configure whether cookies are logged, and give the log files a prefix.
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": origins.HttpOrigin("www.example.com")},
    enable_logging=True, # Optional, this is implied if loggingBucket is specified
    logging_bucket=s3.Bucket(self, "LoggingBucket"),
    logging_file_prefix="distribution-access-logs/",
    logging_includes_cookies=True
)
```

### Importing Distributions

Existing distributions can be imported as well; note that like most imported constructs, an imported distribution cannot be modified.
However, it can be used as a reference for other higher-level constructs.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
distribution = cloudfront.Distribution.from_distribution_attributes(scope, "ImportedDist",
    domain_name="d111111abcdef8.cloudfront.net",
    distribution_id="012345ABCDEF"
)
```

## CloudFrontWebDistribution API - Stable

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

A CloudFront construct - for setting up the AWS CDN with ease!

Example usage:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
source_bucket = Bucket(self, "Bucket")

distribution = CloudFrontWebDistribution(self, "MyDistribution",
    origin_configs=[{
        "s3_origin_source": {
            "s3_bucket_source": source_bucket
        },
        "behaviors": [{"is_default_behavior": True}]
    }
    ]
)
```

### Viewer certificate

By default, CloudFront Web Distributions will answer HTTPS requests with CloudFront's default certificate, only containing the distribution `domainName` (e.g. d111111abcdef8.cloudfront.net).
You can customize the viewer certificate property to provide a custom certificate and/or list of domain name aliases to fit your needs.

See [Using Alternate Domain Names and HTTPS](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https-alternate-domain-names.html) in the CloudFront User Guide.

#### Default certificate

You can customize the default certificate aliases. This is intended to be used in combination with CNAME records in your DNS zone.

Example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
s3_bucket_source = s3.Bucket(self, "Bucket")

distribution = cloudfront.CloudFrontWebDistribution(self, "AnAmazingWebsiteProbably",
    origin_configs=[SourceConfiguration(
        s3_origin_source=S3OriginConfig(s3_bucket_source=s3_bucket_source),
        behaviors=[Behavior(is_default_behavior=True)]
    )],
    viewer_certificate=cloudfront.ViewerCertificate.from_cloud_front_default_certificate("www.example.com")
)
```

#### ACM certificate

You can change the default certificate by one stored AWS Certificate Manager, or ACM.
Those certificate can either be generated by AWS, or purchased by another CA imported into ACM.

For more information, see [the aws-certificatemanager module documentation](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-certificatemanager-readme.html) or [Importing Certificates into AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html) in the AWS Certificate Manager User Guide.

Example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
s3_bucket_source = s3.Bucket(self, "Bucket")

certificate = certificatemanager.Certificate(self, "Certificate",
    domain_name="example.com",
    subject_alternative_names=["*.example.com"]
)

distribution = cloudfront.CloudFrontWebDistribution(self, "AnAmazingWebsiteProbably",
    origin_configs=[SourceConfiguration(
        s3_origin_source=S3OriginConfig(s3_bucket_source=s3_bucket_source),
        behaviors=[Behavior(is_default_behavior=True)]
    )],
    viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(certificate,
        aliases=["example.com", "www.example.com"],
        security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1, # default
        ssl_method=cloudfront.SSLMethod.SNI
    )
)
```

#### IAM certificate

You can also import a certificate into the IAM certificate store.

See [Importing an SSL/TLS Certificate](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-procedures.html#cnames-and-https-uploading-certificates) in the CloudFront User Guide.

Example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
s3_bucket_source = s3.Bucket(self, "Bucket")

distribution = cloudfront.CloudFrontWebDistribution(self, "AnAmazingWebsiteProbably",
    origin_configs=[SourceConfiguration(
        s3_origin_source=S3OriginConfig(s3_bucket_source=s3_bucket_source),
        behaviors=[Behavior(is_default_behavior=True)]
    )],
    viewer_certificate=cloudfront.ViewerCertificate.from_iam_certificate("certificateId",
        aliases=["example.com"],
        security_policy=cloudfront.SecurityPolicyProtocol.SSL_V3, # default
        ssl_method=cloudfront.SSLMethod.SNI
    )
)
```

### Restrictions

CloudFront supports adding restrictions to your distribution.

See [Restricting the Geographic Distribution of Your Content](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/georestrictions.html) in the CloudFront User Guide.

Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudfront.CloudFrontWebDistribution(stack, "MyDistribution",
    # ...
    geo_restriction=GeoRestriction.whitelist("US", "UK")
)
```

### Connection behaviors between CloudFront and your origin

CloudFront provides you even more control over the connection behaviors between CloudFront and your origin. You can now configure the number of connection attempts CloudFront will make to your origin and the origin connection timeout for each attempt.

See [Origin Connection Attempts](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html#origin-connection-attempts)

See [Origin Connection Timeout](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html#origin-connection-timeout)

Example usage:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
distribution = CloudFrontWebDistribution(self, "MyDistribution",
    origin_configs=[{...,
        "connection_attempts": 3,
        "connection_timeout": cdk.Duration.seconds(10)
    }
    ]
)
```

#### Origin Fallback

In case the origin source is not available and answers with one of the
specified status code the failover origin source will be used.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CloudFrontWebDistribution(stack, "ADistribution",
    origin_configs=[{
        "s3_origin_source": {
            "s3_bucket_source": s3.Bucket.from_bucket_name(stack, "aBucket", "myoriginbucket"),
            "origin_path": "/",
            "origin_headers": {
                "my_header": "42"
            }
        },
        "failover_s3_origin_source": {
            "s3_bucket_source": s3.Bucket.from_bucket_name(stack, "aBucketFallback", "myoriginbucketfallback"),
            "origin_path": "/somwhere",
            "origin_headers": {
                "my_header2": "21"
            }
        },
        "failover_criteria_status_codes": [FailoverStatusCode.INTERNAL_SERVER_ERROR],
        "behaviors": [{
            "is_default_behavior": True
        }
        ]
    }
    ]
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

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.AddBehaviorOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "cache_policy": "cachePolicy",
        "compress": "compress",
        "edge_lambdas": "edgeLambdas",
        "origin_request_policy": "originRequestPolicy",
        "smooth_streaming": "smoothStreaming",
        "viewer_protocol_policy": "viewerProtocolPolicy",
    },
)
class AddBehaviorOptions:
    def __init__(
        self,
        *,
        allowed_methods: typing.Optional["AllowedMethods"] = None,
        cached_methods: typing.Optional["CachedMethods"] = None,
        cache_policy: typing.Optional["ICachePolicy"] = None,
        compress: typing.Optional[builtins.bool] = None,
        edge_lambdas: typing.Optional[typing.List["EdgeLambda"]] = None,
        origin_request_policy: typing.Optional["IOriginRequestPolicy"] = None,
        smooth_streaming: typing.Optional[builtins.bool] = None,
        viewer_protocol_policy: typing.Optional["ViewerProtocolPolicy"] = None,
    ) -> None:
        """(experimental) Options for adding a new behavior to a Distribution.

        :param allowed_methods: (experimental) HTTP methods to allow for this behavior. Default: AllowedMethods.ALLOW_GET_HEAD
        :param cached_methods: (experimental) HTTP methods to cache for this behavior. Default: CachedMethods.CACHE_GET_HEAD
        :param cache_policy: (experimental) The cache policy for this behavior. The cache policy determines what values are included in the cache key, and the time-to-live (TTL) values for the cache. Default: CachePolicy.CACHING_OPTIMIZED
        :param compress: (experimental) Whether you want CloudFront to automatically compress certain files for this cache behavior. See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types for file types CloudFront will compress. Default: true
        :param edge_lambdas: (experimental) The Lambda@Edge functions to invoke before serving the contents. Default: - no Lambda functions will be invoked
        :param origin_request_policy: (experimental) The origin request policy for this behavior. The origin request policy determines which values (e.g., headers, cookies) are included in requests that CloudFront sends to the origin. Default: - none
        :param smooth_streaming: (experimental) Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior. Default: false
        :param viewer_protocol_policy: (experimental) The protocol that viewers can use to access the files controlled by this behavior. Default: ViewerProtocolPolicy.ALLOW_ALL

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cached_methods is not None:
            self._values["cached_methods"] = cached_methods
        if cache_policy is not None:
            self._values["cache_policy"] = cache_policy
        if compress is not None:
            self._values["compress"] = compress
        if edge_lambdas is not None:
            self._values["edge_lambdas"] = edge_lambdas
        if origin_request_policy is not None:
            self._values["origin_request_policy"] = origin_request_policy
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming
        if viewer_protocol_policy is not None:
            self._values["viewer_protocol_policy"] = viewer_protocol_policy

    @builtins.property
    def allowed_methods(self) -> typing.Optional["AllowedMethods"]:
        """(experimental) HTTP methods to allow for this behavior.

        :default: AllowedMethods.ALLOW_GET_HEAD

        :stability: experimental
        """
        result = self._values.get("allowed_methods")
        return result

    @builtins.property
    def cached_methods(self) -> typing.Optional["CachedMethods"]:
        """(experimental) HTTP methods to cache for this behavior.

        :default: CachedMethods.CACHE_GET_HEAD

        :stability: experimental
        """
        result = self._values.get("cached_methods")
        return result

    @builtins.property
    def cache_policy(self) -> typing.Optional["ICachePolicy"]:
        """(experimental) The cache policy for this behavior.

        The cache policy determines what values are included in the cache key,
        and the time-to-live (TTL) values for the cache.

        :default: CachePolicy.CACHING_OPTIMIZED

        :see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html.
        :stability: experimental
        """
        result = self._values.get("cache_policy")
        return result

    @builtins.property
    def compress(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether you want CloudFront to automatically compress certain files for this cache behavior.

        See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types
        for file types CloudFront will compress.

        :default: true

        :stability: experimental
        """
        result = self._values.get("compress")
        return result

    @builtins.property
    def edge_lambdas(self) -> typing.Optional[typing.List["EdgeLambda"]]:
        """(experimental) The Lambda@Edge functions to invoke before serving the contents.

        :default: - no Lambda functions will be invoked

        :see: https://aws.amazon.com/lambda/edge
        :stability: experimental
        """
        result = self._values.get("edge_lambdas")
        return result

    @builtins.property
    def origin_request_policy(self) -> typing.Optional["IOriginRequestPolicy"]:
        """(experimental) The origin request policy for this behavior.

        The origin request policy determines which values (e.g., headers, cookies)
        are included in requests that CloudFront sends to the origin.

        :default: - none

        :stability: experimental
        """
        result = self._values.get("origin_request_policy")
        return result

    @builtins.property
    def smooth_streaming(self) -> typing.Optional[builtins.bool]:
        """(experimental) Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior.

        :default: false

        :stability: experimental
        """
        result = self._values.get("smooth_streaming")
        return result

    @builtins.property
    def viewer_protocol_policy(self) -> typing.Optional["ViewerProtocolPolicy"]:
        """(experimental) The protocol that viewers can use to access the files controlled by this behavior.

        :default: ViewerProtocolPolicy.ALLOW_ALL

        :stability: experimental
        """
        result = self._values.get("viewer_protocol_policy")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddBehaviorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.AliasConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "acm_cert_ref": "acmCertRef",
        "names": "names",
        "security_policy": "securityPolicy",
        "ssl_method": "sslMethod",
    },
)
class AliasConfiguration:
    def __init__(
        self,
        *,
        acm_cert_ref: builtins.str,
        names: typing.List[builtins.str],
        security_policy: typing.Optional["SecurityPolicyProtocol"] = None,
        ssl_method: typing.Optional["SSLMethod"] = None,
    ) -> None:
        """(experimental) Configuration for custom domain names.

        CloudFront can use a custom domain that you provide instead of a
        "cloudfront.net" domain. To use this feature you must provide the list of
        additional domains, and the ACM Certificate that CloudFront should use for
        these additional domains.

        :param acm_cert_ref: (experimental) ARN of an AWS Certificate Manager (ACM) certificate.
        :param names: (experimental) Domain names on the certificate. Both main domain name and Subject Alternative Names.
        :param security_policy: (experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI
        :param ssl_method: (experimental) How CloudFront should serve HTTPS requests. See the notes on SSLMethod if you wish to use other SSL termination types. Default: SSLMethod.SNI

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "acm_cert_ref": acm_cert_ref,
            "names": names,
        }
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if ssl_method is not None:
            self._values["ssl_method"] = ssl_method

    @builtins.property
    def acm_cert_ref(self) -> builtins.str:
        """(experimental) ARN of an AWS Certificate Manager (ACM) certificate.

        :stability: experimental
        """
        result = self._values.get("acm_cert_ref")
        assert result is not None, "Required property 'acm_cert_ref' is missing"
        return result

    @builtins.property
    def names(self) -> typing.List[builtins.str]:
        """(experimental) Domain names on the certificate.

        Both main domain name and Subject Alternative Names.

        :stability: experimental
        """
        result = self._values.get("names")
        assert result is not None, "Required property 'names' is missing"
        return result

    @builtins.property
    def security_policy(self) -> typing.Optional["SecurityPolicyProtocol"]:
        """(experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

        CloudFront serves your objects only to browsers or devices that support at
        least the SSL version that you specify.

        :default: - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI

        :stability: experimental
        """
        result = self._values.get("security_policy")
        return result

    @builtins.property
    def ssl_method(self) -> typing.Optional["SSLMethod"]:
        """(experimental) How CloudFront should serve HTTPS requests.

        See the notes on SSLMethod if you wish to use other SSL termination types.

        :default: SSLMethod.SNI

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_ViewerCertificate.html
        :stability: experimental
        """
        result = self._values.get("ssl_method")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AliasConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AllowedMethods(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.AllowedMethods",
):
    """(experimental) The HTTP methods that the Behavior will accept requests on.

    :stability: experimental
    """

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ALLOW_ALL")
    def ALLOW_ALL(cls) -> "AllowedMethods":
        """(experimental) All supported HTTP methods.

        :stability: experimental
        """
        return jsii.sget(cls, "ALLOW_ALL")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ALLOW_GET_HEAD")
    def ALLOW_GET_HEAD(cls) -> "AllowedMethods":
        """(experimental) HEAD and GET.

        :stability: experimental
        """
        return jsii.sget(cls, "ALLOW_GET_HEAD")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ALLOW_GET_HEAD_OPTIONS")
    def ALLOW_GET_HEAD_OPTIONS(cls) -> "AllowedMethods":
        """(experimental) HEAD, GET, and OPTIONS.

        :stability: experimental
        """
        return jsii.sget(cls, "ALLOW_GET_HEAD_OPTIONS")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        """(experimental) HTTP methods supported.

        :stability: experimental
        """
        return jsii.get(self, "methods")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.Behavior",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "compress": "compress",
        "default_ttl": "defaultTtl",
        "forwarded_values": "forwardedValues",
        "is_default_behavior": "isDefaultBehavior",
        "lambda_function_associations": "lambdaFunctionAssociations",
        "max_ttl": "maxTtl",
        "min_ttl": "minTtl",
        "path_pattern": "pathPattern",
        "trusted_signers": "trustedSigners",
    },
)
class Behavior:
    def __init__(
        self,
        *,
        allowed_methods: typing.Optional["CloudFrontAllowedMethods"] = None,
        cached_methods: typing.Optional["CloudFrontAllowedCachedMethods"] = None,
        compress: typing.Optional[builtins.bool] = None,
        default_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        forwarded_values: typing.Optional["CfnDistribution.ForwardedValuesProperty"] = None,
        is_default_behavior: typing.Optional[builtins.bool] = None,
        lambda_function_associations: typing.Optional[typing.List["LambdaFunctionAssociation"]] = None,
        max_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        min_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        trusted_signers: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """(experimental) A CloudFront behavior wrapper.

        :param allowed_methods: (experimental) The method this CloudFront distribution responds do. Default: GET_HEAD
        :param cached_methods: (experimental) Which methods are cached by CloudFront by default. Default: GET_HEAD
        :param compress: (experimental) If CloudFront should automatically compress some content types. Default: true
        :param default_ttl: (experimental) The default amount of time CloudFront will cache an object. This value applies only when your custom origin does not add HTTP headers, such as Cache-Control max-age, Cache-Control s-maxage, and Expires to objects. Default: 86400 (1 day)
        :param forwarded_values: (experimental) The values CloudFront will forward to the origin when making a request. Default: none (no cookies - no headers)
        :param is_default_behavior: (experimental) If this behavior is the default behavior for the distribution. You must specify exactly one default distribution per CloudFront distribution. The default behavior is allowed to omit the "path" property.
        :param lambda_function_associations: (experimental) Declares associated lambda@edge functions for this distribution behaviour. Default: No lambda function associated
        :param max_ttl: (experimental) The max amount of time you want objects to stay in the cache before CloudFront queries your origin. Default: Duration.seconds(31536000) (one year)
        :param min_ttl: (experimental) The minimum amount of time that you want objects to stay in the cache before CloudFront queries your origin.
        :param path_pattern: (experimental) The path this behavior responds to. Required for all non-default behaviors. (The default behavior implicitly has "*" as the path pattern. )
        :param trusted_signers: (experimental) Trusted signers is how CloudFront allows you to serve private content. The signers are the account IDs that are allowed to sign cookies/presigned URLs for this distribution. If you pass a non empty value, all requests for this behavior must be signed (no public access will be allowed)

        :stability: experimental
        """
        if isinstance(forwarded_values, dict):
            forwarded_values = CfnDistribution.ForwardedValuesProperty(**forwarded_values)
        self._values: typing.Dict[str, typing.Any] = {}
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cached_methods is not None:
            self._values["cached_methods"] = cached_methods
        if compress is not None:
            self._values["compress"] = compress
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if forwarded_values is not None:
            self._values["forwarded_values"] = forwarded_values
        if is_default_behavior is not None:
            self._values["is_default_behavior"] = is_default_behavior
        if lambda_function_associations is not None:
            self._values["lambda_function_associations"] = lambda_function_associations
        if max_ttl is not None:
            self._values["max_ttl"] = max_ttl
        if min_ttl is not None:
            self._values["min_ttl"] = min_ttl
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if trusted_signers is not None:
            self._values["trusted_signers"] = trusted_signers

    @builtins.property
    def allowed_methods(self) -> typing.Optional["CloudFrontAllowedMethods"]:
        """(experimental) The method this CloudFront distribution responds do.

        :default: GET_HEAD

        :stability: experimental
        """
        result = self._values.get("allowed_methods")
        return result

    @builtins.property
    def cached_methods(self) -> typing.Optional["CloudFrontAllowedCachedMethods"]:
        """(experimental) Which methods are cached by CloudFront by default.

        :default: GET_HEAD

        :stability: experimental
        """
        result = self._values.get("cached_methods")
        return result

    @builtins.property
    def compress(self) -> typing.Optional[builtins.bool]:
        """(experimental) If CloudFront should automatically compress some content types.

        :default: true

        :stability: experimental
        """
        result = self._values.get("compress")
        return result

    @builtins.property
    def default_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The default amount of time CloudFront will cache an object.

        This value applies only when your custom origin does not add HTTP headers,
        such as Cache-Control max-age, Cache-Control s-maxage, and Expires to objects.

        :default: 86400 (1 day)

        :stability: experimental
        """
        result = self._values.get("default_ttl")
        return result

    @builtins.property
    def forwarded_values(
        self,
    ) -> typing.Optional["CfnDistribution.ForwardedValuesProperty"]:
        """(experimental) The values CloudFront will forward to the origin when making a request.

        :default: none (no cookies - no headers)

        :stability: experimental
        """
        result = self._values.get("forwarded_values")
        return result

    @builtins.property
    def is_default_behavior(self) -> typing.Optional[builtins.bool]:
        """(experimental) If this behavior is the default behavior for the distribution.

        You must specify exactly one default distribution per CloudFront distribution.
        The default behavior is allowed to omit the "path" property.

        :stability: experimental
        """
        result = self._values.get("is_default_behavior")
        return result

    @builtins.property
    def lambda_function_associations(
        self,
    ) -> typing.Optional[typing.List["LambdaFunctionAssociation"]]:
        """(experimental) Declares associated lambda@edge functions for this distribution behaviour.

        :default: No lambda function associated

        :stability: experimental
        """
        result = self._values.get("lambda_function_associations")
        return result

    @builtins.property
    def max_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The max amount of time you want objects to stay in the cache before CloudFront queries your origin.

        :default: Duration.seconds(31536000) (one year)

        :stability: experimental
        """
        result = self._values.get("max_ttl")
        return result

    @builtins.property
    def min_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The minimum amount of time that you want objects to stay in the cache before CloudFront queries your origin.

        :stability: experimental
        """
        result = self._values.get("min_ttl")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(experimental) The path this behavior responds to.

        Required for all non-default behaviors. (The default behavior implicitly has "*" as the path pattern. )

        :stability: experimental
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def trusted_signers(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Trusted signers is how CloudFront allows you to serve private content.

        The signers are the account IDs that are allowed to sign cookies/presigned URLs for this distribution.

        If you pass a non empty value, all requests for this behavior must be signed (no public access will be allowed)

        :stability: experimental
        """
        result = self._values.get("trusted_signers")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Behavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.BehaviorOptions",
    jsii_struct_bases=[AddBehaviorOptions],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "cache_policy": "cachePolicy",
        "compress": "compress",
        "edge_lambdas": "edgeLambdas",
        "origin_request_policy": "originRequestPolicy",
        "smooth_streaming": "smoothStreaming",
        "viewer_protocol_policy": "viewerProtocolPolicy",
        "origin": "origin",
    },
)
class BehaviorOptions(AddBehaviorOptions):
    def __init__(
        self,
        *,
        allowed_methods: typing.Optional[AllowedMethods] = None,
        cached_methods: typing.Optional["CachedMethods"] = None,
        cache_policy: typing.Optional["ICachePolicy"] = None,
        compress: typing.Optional[builtins.bool] = None,
        edge_lambdas: typing.Optional[typing.List["EdgeLambda"]] = None,
        origin_request_policy: typing.Optional["IOriginRequestPolicy"] = None,
        smooth_streaming: typing.Optional[builtins.bool] = None,
        viewer_protocol_policy: typing.Optional["ViewerProtocolPolicy"] = None,
        origin: "IOrigin",
    ) -> None:
        """(experimental) Options for creating a new behavior.

        :param allowed_methods: (experimental) HTTP methods to allow for this behavior. Default: AllowedMethods.ALLOW_GET_HEAD
        :param cached_methods: (experimental) HTTP methods to cache for this behavior. Default: CachedMethods.CACHE_GET_HEAD
        :param cache_policy: (experimental) The cache policy for this behavior. The cache policy determines what values are included in the cache key, and the time-to-live (TTL) values for the cache. Default: CachePolicy.CACHING_OPTIMIZED
        :param compress: (experimental) Whether you want CloudFront to automatically compress certain files for this cache behavior. See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types for file types CloudFront will compress. Default: true
        :param edge_lambdas: (experimental) The Lambda@Edge functions to invoke before serving the contents. Default: - no Lambda functions will be invoked
        :param origin_request_policy: (experimental) The origin request policy for this behavior. The origin request policy determines which values (e.g., headers, cookies) are included in requests that CloudFront sends to the origin. Default: - none
        :param smooth_streaming: (experimental) Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior. Default: false
        :param viewer_protocol_policy: (experimental) The protocol that viewers can use to access the files controlled by this behavior. Default: ViewerProtocolPolicy.ALLOW_ALL
        :param origin: (experimental) The origin that you want CloudFront to route requests to when they match this behavior.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "origin": origin,
        }
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cached_methods is not None:
            self._values["cached_methods"] = cached_methods
        if cache_policy is not None:
            self._values["cache_policy"] = cache_policy
        if compress is not None:
            self._values["compress"] = compress
        if edge_lambdas is not None:
            self._values["edge_lambdas"] = edge_lambdas
        if origin_request_policy is not None:
            self._values["origin_request_policy"] = origin_request_policy
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming
        if viewer_protocol_policy is not None:
            self._values["viewer_protocol_policy"] = viewer_protocol_policy

    @builtins.property
    def allowed_methods(self) -> typing.Optional[AllowedMethods]:
        """(experimental) HTTP methods to allow for this behavior.

        :default: AllowedMethods.ALLOW_GET_HEAD

        :stability: experimental
        """
        result = self._values.get("allowed_methods")
        return result

    @builtins.property
    def cached_methods(self) -> typing.Optional["CachedMethods"]:
        """(experimental) HTTP methods to cache for this behavior.

        :default: CachedMethods.CACHE_GET_HEAD

        :stability: experimental
        """
        result = self._values.get("cached_methods")
        return result

    @builtins.property
    def cache_policy(self) -> typing.Optional["ICachePolicy"]:
        """(experimental) The cache policy for this behavior.

        The cache policy determines what values are included in the cache key,
        and the time-to-live (TTL) values for the cache.

        :default: CachePolicy.CACHING_OPTIMIZED

        :see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html.
        :stability: experimental
        """
        result = self._values.get("cache_policy")
        return result

    @builtins.property
    def compress(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether you want CloudFront to automatically compress certain files for this cache behavior.

        See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types
        for file types CloudFront will compress.

        :default: true

        :stability: experimental
        """
        result = self._values.get("compress")
        return result

    @builtins.property
    def edge_lambdas(self) -> typing.Optional[typing.List["EdgeLambda"]]:
        """(experimental) The Lambda@Edge functions to invoke before serving the contents.

        :default: - no Lambda functions will be invoked

        :see: https://aws.amazon.com/lambda/edge
        :stability: experimental
        """
        result = self._values.get("edge_lambdas")
        return result

    @builtins.property
    def origin_request_policy(self) -> typing.Optional["IOriginRequestPolicy"]:
        """(experimental) The origin request policy for this behavior.

        The origin request policy determines which values (e.g., headers, cookies)
        are included in requests that CloudFront sends to the origin.

        :default: - none

        :stability: experimental
        """
        result = self._values.get("origin_request_policy")
        return result

    @builtins.property
    def smooth_streaming(self) -> typing.Optional[builtins.bool]:
        """(experimental) Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior.

        :default: false

        :stability: experimental
        """
        result = self._values.get("smooth_streaming")
        return result

    @builtins.property
    def viewer_protocol_policy(self) -> typing.Optional["ViewerProtocolPolicy"]:
        """(experimental) The protocol that viewers can use to access the files controlled by this behavior.

        :default: ViewerProtocolPolicy.ALLOW_ALL

        :stability: experimental
        """
        result = self._values.get("viewer_protocol_policy")
        return result

    @builtins.property
    def origin(self) -> "IOrigin":
        """(experimental) The origin that you want CloudFront to route requests to when they match this behavior.

        :stability: experimental
        """
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BehaviorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CacheCookieBehavior(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CacheCookieBehavior",
):
    """(experimental) Determines whether any cookies in viewer requests are included in the cache key and automatically included in requests that CloudFront sends to the origin.

    :stability: experimental
    """

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "CacheCookieBehavior":
        """(experimental) All cookies in viewer requests are included in the cache key and are automatically included in requests that CloudFront sends to the origin.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "all", [])

    @jsii.member(jsii_name="allowList")
    @builtins.classmethod
    def allow_list(cls, *cookies: builtins.str) -> "CacheCookieBehavior":
        """(experimental) Only the provided ``cookies`` are included in the cache key and automatically included in requests that CloudFront sends to the origin.

        :param cookies: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "allowList", [*cookies])

    @jsii.member(jsii_name="denyList")
    @builtins.classmethod
    def deny_list(cls, *cookies: builtins.str) -> "CacheCookieBehavior":
        """(experimental) All cookies except the provided ``cookies`` are included in the cache key and automatically included in requests that CloudFront sends to the origin.

        :param cookies: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "denyList", [*cookies])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "CacheCookieBehavior":
        """(experimental) Cookies in viewer requests are not included in the cache key and are not automatically included in requests that CloudFront sends to the origin.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "none", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        """(experimental) The behavior of cookies: allow all, none, an allow list, or a deny list.

        :stability: experimental
        """
        return jsii.get(self, "behavior")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cookies")
    def cookies(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The cookies to allow or deny, if the behavior is an allow or deny list.

        :stability: experimental
        """
        return jsii.get(self, "cookies")


class CacheHeaderBehavior(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CacheHeaderBehavior",
):
    """(experimental) Determines whether any HTTP headers are included in the cache key and automatically included in requests that CloudFront sends to the origin.

    :stability: experimental
    """

    @jsii.member(jsii_name="allowList")
    @builtins.classmethod
    def allow_list(cls, *headers: builtins.str) -> "CacheHeaderBehavior":
        """(experimental) Listed headers are included in the cache key and are automatically included in requests that CloudFront sends to the origin.

        :param headers: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "allowList", [*headers])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "CacheHeaderBehavior":
        """(experimental) HTTP headers are not included in the cache key and are not automatically included in requests that CloudFront sends to the origin.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "none", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        """(experimental) If the no headers will be passed, or an allow list of headers.

        :stability: experimental
        """
        return jsii.get(self, "behavior")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The headers for the allow/deny list, if applicable.

        :stability: experimental
        """
        return jsii.get(self, "headers")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CachePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_policy_name": "cachePolicyName",
        "comment": "comment",
        "cookie_behavior": "cookieBehavior",
        "default_ttl": "defaultTtl",
        "enable_accept_encoding_brotli": "enableAcceptEncodingBrotli",
        "enable_accept_encoding_gzip": "enableAcceptEncodingGzip",
        "header_behavior": "headerBehavior",
        "max_ttl": "maxTtl",
        "min_ttl": "minTtl",
        "query_string_behavior": "queryStringBehavior",
    },
)
class CachePolicyProps:
    def __init__(
        self,
        *,
        cache_policy_name: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        cookie_behavior: typing.Optional[CacheCookieBehavior] = None,
        default_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        enable_accept_encoding_brotli: typing.Optional[builtins.bool] = None,
        enable_accept_encoding_gzip: typing.Optional[builtins.bool] = None,
        header_behavior: typing.Optional[CacheHeaderBehavior] = None,
        max_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        min_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        query_string_behavior: typing.Optional["CacheQueryStringBehavior"] = None,
    ) -> None:
        """(experimental) Properties for creating a Cache Policy.

        :param cache_policy_name: (experimental) A unique name to identify the cache policy. The name must only include '-', '_', or alphanumeric characters. Default: - generated from the ``id``
        :param comment: (experimental) A comment to describe the cache policy. Default: - no comment
        :param cookie_behavior: (experimental) Determines whether any cookies in viewer requests are included in the cache key and automatically included in requests that CloudFront sends to the origin. Default: CacheCookieBehavior.none()
        :param default_ttl: (experimental) The default amount of time for objects to stay in the CloudFront cache. Only used when the origin does not send Cache-Control or Expires headers with the object. Default: - The greater of 1 day and ``minTtl``
        :param enable_accept_encoding_brotli: (experimental) Whether to normalize and include the ``Accept-Encoding`` header in the cache key when the ``Accept-Encoding`` header is 'br'. Default: false
        :param enable_accept_encoding_gzip: (experimental) Whether to normalize and include the ``Accept-Encoding`` header in the cache key when the ``Accept-Encoding`` header is 'gzip'. Default: false
        :param header_behavior: (experimental) Determines whether any HTTP headers are included in the cache key and automatically included in requests that CloudFront sends to the origin. Default: CacheHeaderBehavior.none()
        :param max_ttl: (experimental) The maximum amount of time for objects to stay in the CloudFront cache. CloudFront uses this value only when the origin sends Cache-Control or Expires headers with the object. Default: - The greater of 1 year and ``defaultTtl``
        :param min_ttl: (experimental) The minimum amount of time for objects to stay in the CloudFront cache. Default: Duration.seconds(0)
        :param query_string_behavior: (experimental) Determines whether any query strings are included in the cache key and automatically included in requests that CloudFront sends to the origin. Default: CacheQueryStringBehavior.none()

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if cache_policy_name is not None:
            self._values["cache_policy_name"] = cache_policy_name
        if comment is not None:
            self._values["comment"] = comment
        if cookie_behavior is not None:
            self._values["cookie_behavior"] = cookie_behavior
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if enable_accept_encoding_brotli is not None:
            self._values["enable_accept_encoding_brotli"] = enable_accept_encoding_brotli
        if enable_accept_encoding_gzip is not None:
            self._values["enable_accept_encoding_gzip"] = enable_accept_encoding_gzip
        if header_behavior is not None:
            self._values["header_behavior"] = header_behavior
        if max_ttl is not None:
            self._values["max_ttl"] = max_ttl
        if min_ttl is not None:
            self._values["min_ttl"] = min_ttl
        if query_string_behavior is not None:
            self._values["query_string_behavior"] = query_string_behavior

    @builtins.property
    def cache_policy_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A unique name to identify the cache policy.

        The name must only include '-', '_', or alphanumeric characters.

        :default: - generated from the ``id``

        :stability: experimental
        """
        result = self._values.get("cache_policy_name")
        return result

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """(experimental) A comment to describe the cache policy.

        :default: - no comment

        :stability: experimental
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def cookie_behavior(self) -> typing.Optional[CacheCookieBehavior]:
        """(experimental) Determines whether any cookies in viewer requests are included in the cache key and automatically included in requests that CloudFront sends to the origin.

        :default: CacheCookieBehavior.none()

        :stability: experimental
        """
        result = self._values.get("cookie_behavior")
        return result

    @builtins.property
    def default_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The default amount of time for objects to stay in the CloudFront cache.

        Only used when the origin does not send Cache-Control or Expires headers with the object.

        :default: - The greater of 1 day and ``minTtl``

        :stability: experimental
        """
        result = self._values.get("default_ttl")
        return result

    @builtins.property
    def enable_accept_encoding_brotli(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to normalize and include the ``Accept-Encoding`` header in the cache key when the ``Accept-Encoding`` header is 'br'.

        :default: false

        :stability: experimental
        """
        result = self._values.get("enable_accept_encoding_brotli")
        return result

    @builtins.property
    def enable_accept_encoding_gzip(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to normalize and include the ``Accept-Encoding`` header in the cache key when the ``Accept-Encoding`` header is 'gzip'.

        :default: false

        :stability: experimental
        """
        result = self._values.get("enable_accept_encoding_gzip")
        return result

    @builtins.property
    def header_behavior(self) -> typing.Optional[CacheHeaderBehavior]:
        """(experimental) Determines whether any HTTP headers are included in the cache key and automatically included in requests that CloudFront sends to the origin.

        :default: CacheHeaderBehavior.none()

        :stability: experimental
        """
        result = self._values.get("header_behavior")
        return result

    @builtins.property
    def max_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The maximum amount of time for objects to stay in the CloudFront cache.

        CloudFront uses this value only when the origin sends Cache-Control or Expires headers with the object.

        :default: - The greater of 1 year and ``defaultTtl``

        :stability: experimental
        """
        result = self._values.get("max_ttl")
        return result

    @builtins.property
    def min_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The minimum amount of time for objects to stay in the CloudFront cache.

        :default: Duration.seconds(0)

        :stability: experimental
        """
        result = self._values.get("min_ttl")
        return result

    @builtins.property
    def query_string_behavior(self) -> typing.Optional["CacheQueryStringBehavior"]:
        """(experimental) Determines whether any query strings are included in the cache key and automatically included in requests that CloudFront sends to the origin.

        :default: CacheQueryStringBehavior.none()

        :stability: experimental
        """
        result = self._values.get("query_string_behavior")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CachePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CacheQueryStringBehavior(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CacheQueryStringBehavior",
):
    """(experimental) Determines whether any URL query strings in viewer requests are included in the cache key and automatically included in requests that CloudFront sends to the origin.

    :stability: experimental
    """

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "CacheQueryStringBehavior":
        """(experimental) All query strings in viewer requests are included in the cache key and are automatically included in requests that CloudFront sends to the origin.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "all", [])

    @jsii.member(jsii_name="allowList")
    @builtins.classmethod
    def allow_list(cls, *query_strings: builtins.str) -> "CacheQueryStringBehavior":
        """(experimental) Only the provided ``queryStrings`` are included in the cache key and automatically included in requests that CloudFront sends to the origin.

        :param query_strings: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "allowList", [*query_strings])

    @jsii.member(jsii_name="denyList")
    @builtins.classmethod
    def deny_list(cls, *query_strings: builtins.str) -> "CacheQueryStringBehavior":
        """(experimental) All query strings except the provided ``queryStrings`` are included in the cache key and automatically included in requests that CloudFront sends to the origin.

        :param query_strings: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "denyList", [*query_strings])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "CacheQueryStringBehavior":
        """(experimental) Query strings in viewer requests are not included in the cache key and are not automatically included in requests that CloudFront sends to the origin.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "none", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        """(experimental) The behavior of query strings -- allow all, none, only an allow list, or a deny list.

        :stability: experimental
        """
        return jsii.get(self, "behavior")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="queryStrings")
    def query_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The query strings to allow or deny, if the behavior is an allow or deny list.

        :stability: experimental
        """
        return jsii.get(self, "queryStrings")


class CachedMethods(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CachedMethods",
):
    """(experimental) The HTTP methods that the Behavior will cache requests on.

    :stability: experimental
    """

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CACHE_GET_HEAD")
    def CACHE_GET_HEAD(cls) -> "CachedMethods":
        """(experimental) HEAD and GET.

        :stability: experimental
        """
        return jsii.sget(cls, "CACHE_GET_HEAD")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CACHE_GET_HEAD_OPTIONS")
    def CACHE_GET_HEAD_OPTIONS(cls) -> "CachedMethods":
        """(experimental) HEAD, GET, and OPTIONS.

        :stability: experimental
        """
        return jsii.sget(cls, "CACHE_GET_HEAD_OPTIONS")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        """(experimental) HTTP methods supported.

        :stability: experimental
        """
        return jsii.get(self, "methods")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCachePolicy(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CfnCachePolicy",
):
    """A CloudFormation ``AWS::CloudFront::CachePolicy``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cachepolicy.html
    :cloudformationResource: AWS::CloudFront::CachePolicy
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cache_policy_config: typing.Union["CfnCachePolicy.CachePolicyConfigProperty", aws_cdk.core.IResolvable],
    ) -> None:
        """Create a new ``AWS::CloudFront::CachePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_policy_config: ``AWS::CloudFront::CachePolicy.CachePolicyConfig``.
        """
        props = CfnCachePolicyProps(cache_policy_config=cache_policy_config)

        jsii.create(CfnCachePolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrLastModifiedTime")
    def attr_last_modified_time(self) -> builtins.str:
        """
        :cloudformationAttribute: LastModifiedTime
        """
        return jsii.get(self, "attrLastModifiedTime")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cachePolicyConfig")
    def cache_policy_config(
        self,
    ) -> typing.Union["CfnCachePolicy.CachePolicyConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::CloudFront::CachePolicy.CachePolicyConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cachepolicy.html#cfn-cloudfront-cachepolicy-cachepolicyconfig
        """
        return jsii.get(self, "cachePolicyConfig")

    @cache_policy_config.setter # type: ignore
    def cache_policy_config(
        self,
        value: typing.Union["CfnCachePolicy.CachePolicyConfigProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "cachePolicyConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnCachePolicy.CachePolicyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_ttl": "defaultTtl",
            "max_ttl": "maxTtl",
            "min_ttl": "minTtl",
            "name": "name",
            "parameters_in_cache_key_and_forwarded_to_origin": "parametersInCacheKeyAndForwardedToOrigin",
            "comment": "comment",
        },
    )
    class CachePolicyConfigProperty:
        def __init__(
            self,
            *,
            default_ttl: jsii.Number,
            max_ttl: jsii.Number,
            min_ttl: jsii.Number,
            name: builtins.str,
            parameters_in_cache_key_and_forwarded_to_origin: typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty"],
            comment: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param default_ttl: ``CfnCachePolicy.CachePolicyConfigProperty.DefaultTTL``.
            :param max_ttl: ``CfnCachePolicy.CachePolicyConfigProperty.MaxTTL``.
            :param min_ttl: ``CfnCachePolicy.CachePolicyConfigProperty.MinTTL``.
            :param name: ``CfnCachePolicy.CachePolicyConfigProperty.Name``.
            :param parameters_in_cache_key_and_forwarded_to_origin: ``CfnCachePolicy.CachePolicyConfigProperty.ParametersInCacheKeyAndForwardedToOrigin``.
            :param comment: ``CfnCachePolicy.CachePolicyConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cachepolicyconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "default_ttl": default_ttl,
                "max_ttl": max_ttl,
                "min_ttl": min_ttl,
                "name": name,
                "parameters_in_cache_key_and_forwarded_to_origin": parameters_in_cache_key_and_forwarded_to_origin,
            }
            if comment is not None:
                self._values["comment"] = comment

        @builtins.property
        def default_ttl(self) -> jsii.Number:
            """``CfnCachePolicy.CachePolicyConfigProperty.DefaultTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cachepolicyconfig.html#cfn-cloudfront-cachepolicy-cachepolicyconfig-defaultttl
            """
            result = self._values.get("default_ttl")
            assert result is not None, "Required property 'default_ttl' is missing"
            return result

        @builtins.property
        def max_ttl(self) -> jsii.Number:
            """``CfnCachePolicy.CachePolicyConfigProperty.MaxTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cachepolicyconfig.html#cfn-cloudfront-cachepolicy-cachepolicyconfig-maxttl
            """
            result = self._values.get("max_ttl")
            assert result is not None, "Required property 'max_ttl' is missing"
            return result

        @builtins.property
        def min_ttl(self) -> jsii.Number:
            """``CfnCachePolicy.CachePolicyConfigProperty.MinTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cachepolicyconfig.html#cfn-cloudfront-cachepolicy-cachepolicyconfig-minttl
            """
            result = self._values.get("min_ttl")
            assert result is not None, "Required property 'min_ttl' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnCachePolicy.CachePolicyConfigProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cachepolicyconfig.html#cfn-cloudfront-cachepolicy-cachepolicyconfig-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def parameters_in_cache_key_and_forwarded_to_origin(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty"]:
            """``CfnCachePolicy.CachePolicyConfigProperty.ParametersInCacheKeyAndForwardedToOrigin``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cachepolicyconfig.html#cfn-cloudfront-cachepolicy-cachepolicyconfig-parametersincachekeyandforwardedtoorigin
            """
            result = self._values.get("parameters_in_cache_key_and_forwarded_to_origin")
            assert result is not None, "Required property 'parameters_in_cache_key_and_forwarded_to_origin' is missing"
            return result

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            """``CfnCachePolicy.CachePolicyConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cachepolicyconfig.html#cfn-cloudfront-cachepolicy-cachepolicyconfig-comment
            """
            result = self._values.get("comment")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CachePolicyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnCachePolicy.CookiesConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cookie_behavior": "cookieBehavior", "cookies": "cookies"},
    )
    class CookiesConfigProperty:
        def __init__(
            self,
            *,
            cookie_behavior: builtins.str,
            cookies: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param cookie_behavior: ``CfnCachePolicy.CookiesConfigProperty.CookieBehavior``.
            :param cookies: ``CfnCachePolicy.CookiesConfigProperty.Cookies``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cookiesconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cookie_behavior": cookie_behavior,
            }
            if cookies is not None:
                self._values["cookies"] = cookies

        @builtins.property
        def cookie_behavior(self) -> builtins.str:
            """``CfnCachePolicy.CookiesConfigProperty.CookieBehavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cookiesconfig.html#cfn-cloudfront-cachepolicy-cookiesconfig-cookiebehavior
            """
            result = self._values.get("cookie_behavior")
            assert result is not None, "Required property 'cookie_behavior' is missing"
            return result

        @builtins.property
        def cookies(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnCachePolicy.CookiesConfigProperty.Cookies``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-cookiesconfig.html#cfn-cloudfront-cachepolicy-cookiesconfig-cookies
            """
            result = self._values.get("cookies")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CookiesConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnCachePolicy.HeadersConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"header_behavior": "headerBehavior", "headers": "headers"},
    )
    class HeadersConfigProperty:
        def __init__(
            self,
            *,
            header_behavior: builtins.str,
            headers: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param header_behavior: ``CfnCachePolicy.HeadersConfigProperty.HeaderBehavior``.
            :param headers: ``CfnCachePolicy.HeadersConfigProperty.Headers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-headersconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "header_behavior": header_behavior,
            }
            if headers is not None:
                self._values["headers"] = headers

        @builtins.property
        def header_behavior(self) -> builtins.str:
            """``CfnCachePolicy.HeadersConfigProperty.HeaderBehavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-headersconfig.html#cfn-cloudfront-cachepolicy-headersconfig-headerbehavior
            """
            result = self._values.get("header_behavior")
            assert result is not None, "Required property 'header_behavior' is missing"
            return result

        @builtins.property
        def headers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnCachePolicy.HeadersConfigProperty.Headers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-headersconfig.html#cfn-cloudfront-cachepolicy-headersconfig-headers
            """
            result = self._values.get("headers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeadersConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cookies_config": "cookiesConfig",
            "enable_accept_encoding_gzip": "enableAcceptEncodingGzip",
            "headers_config": "headersConfig",
            "query_strings_config": "queryStringsConfig",
            "enable_accept_encoding_brotli": "enableAcceptEncodingBrotli",
        },
    )
    class ParametersInCacheKeyAndForwardedToOriginProperty:
        def __init__(
            self,
            *,
            cookies_config: typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.CookiesConfigProperty"],
            enable_accept_encoding_gzip: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            headers_config: typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.HeadersConfigProperty"],
            query_strings_config: typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.QueryStringsConfigProperty"],
            enable_accept_encoding_brotli: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param cookies_config: ``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.CookiesConfig``.
            :param enable_accept_encoding_gzip: ``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.EnableAcceptEncodingGzip``.
            :param headers_config: ``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.HeadersConfig``.
            :param query_strings_config: ``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.QueryStringsConfig``.
            :param enable_accept_encoding_brotli: ``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.EnableAcceptEncodingBrotli``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cookies_config": cookies_config,
                "enable_accept_encoding_gzip": enable_accept_encoding_gzip,
                "headers_config": headers_config,
                "query_strings_config": query_strings_config,
            }
            if enable_accept_encoding_brotli is not None:
                self._values["enable_accept_encoding_brotli"] = enable_accept_encoding_brotli

        @builtins.property
        def cookies_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.CookiesConfigProperty"]:
            """``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.CookiesConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin.html#cfn-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin-cookiesconfig
            """
            result = self._values.get("cookies_config")
            assert result is not None, "Required property 'cookies_config' is missing"
            return result

        @builtins.property
        def enable_accept_encoding_gzip(
            self,
        ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.EnableAcceptEncodingGzip``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin.html#cfn-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin-enableacceptencodinggzip
            """
            result = self._values.get("enable_accept_encoding_gzip")
            assert result is not None, "Required property 'enable_accept_encoding_gzip' is missing"
            return result

        @builtins.property
        def headers_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.HeadersConfigProperty"]:
            """``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.HeadersConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin.html#cfn-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin-headersconfig
            """
            result = self._values.get("headers_config")
            assert result is not None, "Required property 'headers_config' is missing"
            return result

        @builtins.property
        def query_strings_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCachePolicy.QueryStringsConfigProperty"]:
            """``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.QueryStringsConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin.html#cfn-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin-querystringsconfig
            """
            result = self._values.get("query_strings_config")
            assert result is not None, "Required property 'query_strings_config' is missing"
            return result

        @builtins.property
        def enable_accept_encoding_brotli(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCachePolicy.ParametersInCacheKeyAndForwardedToOriginProperty.EnableAcceptEncodingBrotli``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin.html#cfn-cloudfront-cachepolicy-parametersincachekeyandforwardedtoorigin-enableacceptencodingbrotli
            """
            result = self._values.get("enable_accept_encoding_brotli")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParametersInCacheKeyAndForwardedToOriginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnCachePolicy.QueryStringsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_string_behavior": "queryStringBehavior",
            "query_strings": "queryStrings",
        },
    )
    class QueryStringsConfigProperty:
        def __init__(
            self,
            *,
            query_string_behavior: builtins.str,
            query_strings: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param query_string_behavior: ``CfnCachePolicy.QueryStringsConfigProperty.QueryStringBehavior``.
            :param query_strings: ``CfnCachePolicy.QueryStringsConfigProperty.QueryStrings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-querystringsconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "query_string_behavior": query_string_behavior,
            }
            if query_strings is not None:
                self._values["query_strings"] = query_strings

        @builtins.property
        def query_string_behavior(self) -> builtins.str:
            """``CfnCachePolicy.QueryStringsConfigProperty.QueryStringBehavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-querystringsconfig.html#cfn-cloudfront-cachepolicy-querystringsconfig-querystringbehavior
            """
            result = self._values.get("query_string_behavior")
            assert result is not None, "Required property 'query_string_behavior' is missing"
            return result

        @builtins.property
        def query_strings(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnCachePolicy.QueryStringsConfigProperty.QueryStrings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cachepolicy-querystringsconfig.html#cfn-cloudfront-cachepolicy-querystringsconfig-querystrings
            """
            result = self._values.get("query_strings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CfnCachePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"cache_policy_config": "cachePolicyConfig"},
)
class CfnCachePolicyProps:
    def __init__(
        self,
        *,
        cache_policy_config: typing.Union[CfnCachePolicy.CachePolicyConfigProperty, aws_cdk.core.IResolvable],
    ) -> None:
        """Properties for defining a ``AWS::CloudFront::CachePolicy``.

        :param cache_policy_config: ``AWS::CloudFront::CachePolicy.CachePolicyConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cachepolicy.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cache_policy_config": cache_policy_config,
        }

    @builtins.property
    def cache_policy_config(
        self,
    ) -> typing.Union[CfnCachePolicy.CachePolicyConfigProperty, aws_cdk.core.IResolvable]:
        """``AWS::CloudFront::CachePolicy.CachePolicyConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cachepolicy.html#cfn-cloudfront-cachepolicy-cachepolicyconfig
        """
        result = self._values.get("cache_policy_config")
        assert result is not None, "Required property 'cache_policy_config' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCachePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCloudFrontOriginAccessIdentity(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity",
):
    """A CloudFormation ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html
    :cloudformationResource: AWS::CloudFront::CloudFrontOriginAccessIdentity
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cloud_front_origin_access_identity_config: typing.Union[aws_cdk.core.IResolvable, "CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty"],
    ) -> None:
        """Create a new ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cloud_front_origin_access_identity_config: ``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.
        """
        props = CfnCloudFrontOriginAccessIdentityProps(
            cloud_front_origin_access_identity_config=cloud_front_origin_access_identity_config,
        )

        jsii.create(CfnCloudFrontOriginAccessIdentity, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrS3CanonicalUserId")
    def attr_s3_canonical_user_id(self) -> builtins.str:
        """
        :cloudformationAttribute: S3CanonicalUserId
        """
        return jsii.get(self, "attrS3CanonicalUserId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cloudFrontOriginAccessIdentityConfig")
    def cloud_front_origin_access_identity_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty"]:
        """``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig
        """
        return jsii.get(self, "cloudFrontOriginAccessIdentityConfig")

    @cloud_front_origin_access_identity_config.setter # type: ignore
    def cloud_front_origin_access_identity_config(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty"],
    ) -> None:
        jsii.set(self, "cloudFrontOriginAccessIdentityConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"comment": "comment"},
    )
    class CloudFrontOriginAccessIdentityConfigProperty:
        def __init__(self, *, comment: builtins.str) -> None:
            """
            :param comment: ``CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "comment": comment,
            }

        @builtins.property
        def comment(self) -> builtins.str:
            """``CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig-comment
            """
            result = self._values.get("comment")
            assert result is not None, "Required property 'comment' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudFrontOriginAccessIdentityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentityProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_front_origin_access_identity_config": "cloudFrontOriginAccessIdentityConfig",
    },
)
class CfnCloudFrontOriginAccessIdentityProps:
    def __init__(
        self,
        *,
        cloud_front_origin_access_identity_config: typing.Union[aws_cdk.core.IResolvable, CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty],
    ) -> None:
        """Properties for defining a ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

        :param cloud_front_origin_access_identity_config: ``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_front_origin_access_identity_config": cloud_front_origin_access_identity_config,
        }

    @builtins.property
    def cloud_front_origin_access_identity_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty]:
        """``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig
        """
        result = self._values.get("cloud_front_origin_access_identity_config")
        assert result is not None, "Required property 'cloud_front_origin_access_identity_config' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudFrontOriginAccessIdentityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDistribution(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution",
):
    """A CloudFormation ``AWS::CloudFront::Distribution``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html
    :cloudformationResource: AWS::CloudFront::Distribution
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        distribution_config: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.DistributionConfigProperty"],
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::CloudFront::Distribution``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param distribution_config: ``AWS::CloudFront::Distribution.DistributionConfig``.
        :param tags: ``AWS::CloudFront::Distribution.Tags``.
        """
        props = CfnDistributionProps(
            distribution_config=distribution_config, tags=tags
        )

        jsii.create(CfnDistribution, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        """
        :cloudformationAttribute: DomainName
        """
        return jsii.get(self, "attrDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudFront::Distribution.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionConfig")
    def distribution_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.DistributionConfigProperty"]:
        """``AWS::CloudFront::Distribution.DistributionConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-distributionconfig
        """
        return jsii.get(self, "distributionConfig")

    @distribution_config.setter # type: ignore
    def distribution_config(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.DistributionConfigProperty"],
    ) -> None:
        jsii.set(self, "distributionConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CacheBehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "path_pattern": "pathPattern",
            "target_origin_id": "targetOriginId",
            "viewer_protocol_policy": "viewerProtocolPolicy",
            "allowed_methods": "allowedMethods",
            "cached_methods": "cachedMethods",
            "cache_policy_id": "cachePolicyId",
            "compress": "compress",
            "default_ttl": "defaultTtl",
            "field_level_encryption_id": "fieldLevelEncryptionId",
            "forwarded_values": "forwardedValues",
            "lambda_function_associations": "lambdaFunctionAssociations",
            "max_ttl": "maxTtl",
            "min_ttl": "minTtl",
            "origin_request_policy_id": "originRequestPolicyId",
            "realtime_log_config_arn": "realtimeLogConfigArn",
            "smooth_streaming": "smoothStreaming",
            "trusted_signers": "trustedSigners",
        },
    )
    class CacheBehaviorProperty:
        def __init__(
            self,
            *,
            path_pattern: builtins.str,
            target_origin_id: builtins.str,
            viewer_protocol_policy: builtins.str,
            allowed_methods: typing.Optional[typing.List[builtins.str]] = None,
            cached_methods: typing.Optional[typing.List[builtins.str]] = None,
            cache_policy_id: typing.Optional[builtins.str] = None,
            compress: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            default_ttl: typing.Optional[jsii.Number] = None,
            field_level_encryption_id: typing.Optional[builtins.str] = None,
            forwarded_values: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.ForwardedValuesProperty"]] = None,
            lambda_function_associations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LambdaFunctionAssociationProperty"]]]] = None,
            max_ttl: typing.Optional[jsii.Number] = None,
            min_ttl: typing.Optional[jsii.Number] = None,
            origin_request_policy_id: typing.Optional[builtins.str] = None,
            realtime_log_config_arn: typing.Optional[builtins.str] = None,
            smooth_streaming: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            trusted_signers: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param path_pattern: ``CfnDistribution.CacheBehaviorProperty.PathPattern``.
            :param target_origin_id: ``CfnDistribution.CacheBehaviorProperty.TargetOriginId``.
            :param viewer_protocol_policy: ``CfnDistribution.CacheBehaviorProperty.ViewerProtocolPolicy``.
            :param allowed_methods: ``CfnDistribution.CacheBehaviorProperty.AllowedMethods``.
            :param cached_methods: ``CfnDistribution.CacheBehaviorProperty.CachedMethods``.
            :param cache_policy_id: ``CfnDistribution.CacheBehaviorProperty.CachePolicyId``.
            :param compress: ``CfnDistribution.CacheBehaviorProperty.Compress``.
            :param default_ttl: ``CfnDistribution.CacheBehaviorProperty.DefaultTTL``.
            :param field_level_encryption_id: ``CfnDistribution.CacheBehaviorProperty.FieldLevelEncryptionId``.
            :param forwarded_values: ``CfnDistribution.CacheBehaviorProperty.ForwardedValues``.
            :param lambda_function_associations: ``CfnDistribution.CacheBehaviorProperty.LambdaFunctionAssociations``.
            :param max_ttl: ``CfnDistribution.CacheBehaviorProperty.MaxTTL``.
            :param min_ttl: ``CfnDistribution.CacheBehaviorProperty.MinTTL``.
            :param origin_request_policy_id: ``CfnDistribution.CacheBehaviorProperty.OriginRequestPolicyId``.
            :param realtime_log_config_arn: ``CfnDistribution.CacheBehaviorProperty.RealtimeLogConfigArn``.
            :param smooth_streaming: ``CfnDistribution.CacheBehaviorProperty.SmoothStreaming``.
            :param trusted_signers: ``CfnDistribution.CacheBehaviorProperty.TrustedSigners``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "path_pattern": path_pattern,
                "target_origin_id": target_origin_id,
                "viewer_protocol_policy": viewer_protocol_policy,
            }
            if allowed_methods is not None:
                self._values["allowed_methods"] = allowed_methods
            if cached_methods is not None:
                self._values["cached_methods"] = cached_methods
            if cache_policy_id is not None:
                self._values["cache_policy_id"] = cache_policy_id
            if compress is not None:
                self._values["compress"] = compress
            if default_ttl is not None:
                self._values["default_ttl"] = default_ttl
            if field_level_encryption_id is not None:
                self._values["field_level_encryption_id"] = field_level_encryption_id
            if forwarded_values is not None:
                self._values["forwarded_values"] = forwarded_values
            if lambda_function_associations is not None:
                self._values["lambda_function_associations"] = lambda_function_associations
            if max_ttl is not None:
                self._values["max_ttl"] = max_ttl
            if min_ttl is not None:
                self._values["min_ttl"] = min_ttl
            if origin_request_policy_id is not None:
                self._values["origin_request_policy_id"] = origin_request_policy_id
            if realtime_log_config_arn is not None:
                self._values["realtime_log_config_arn"] = realtime_log_config_arn
            if smooth_streaming is not None:
                self._values["smooth_streaming"] = smooth_streaming
            if trusted_signers is not None:
                self._values["trusted_signers"] = trusted_signers

        @builtins.property
        def path_pattern(self) -> builtins.str:
            """``CfnDistribution.CacheBehaviorProperty.PathPattern``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-pathpattern
            """
            result = self._values.get("path_pattern")
            assert result is not None, "Required property 'path_pattern' is missing"
            return result

        @builtins.property
        def target_origin_id(self) -> builtins.str:
            """``CfnDistribution.CacheBehaviorProperty.TargetOriginId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-targetoriginid
            """
            result = self._values.get("target_origin_id")
            assert result is not None, "Required property 'target_origin_id' is missing"
            return result

        @builtins.property
        def viewer_protocol_policy(self) -> builtins.str:
            """``CfnDistribution.CacheBehaviorProperty.ViewerProtocolPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-viewerprotocolpolicy
            """
            result = self._values.get("viewer_protocol_policy")
            assert result is not None, "Required property 'viewer_protocol_policy' is missing"
            return result

        @builtins.property
        def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.CacheBehaviorProperty.AllowedMethods``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-allowedmethods
            """
            result = self._values.get("allowed_methods")
            return result

        @builtins.property
        def cached_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.CacheBehaviorProperty.CachedMethods``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-cachedmethods
            """
            result = self._values.get("cached_methods")
            return result

        @builtins.property
        def cache_policy_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.CacheBehaviorProperty.CachePolicyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-cachepolicyid
            """
            result = self._values.get("cache_policy_id")
            return result

        @builtins.property
        def compress(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.CacheBehaviorProperty.Compress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-compress
            """
            result = self._values.get("compress")
            return result

        @builtins.property
        def default_ttl(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CacheBehaviorProperty.DefaultTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-defaultttl
            """
            result = self._values.get("default_ttl")
            return result

        @builtins.property
        def field_level_encryption_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.CacheBehaviorProperty.FieldLevelEncryptionId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-fieldlevelencryptionid
            """
            result = self._values.get("field_level_encryption_id")
            return result

        @builtins.property
        def forwarded_values(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.ForwardedValuesProperty"]]:
            """``CfnDistribution.CacheBehaviorProperty.ForwardedValues``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-forwardedvalues
            """
            result = self._values.get("forwarded_values")
            return result

        @builtins.property
        def lambda_function_associations(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LambdaFunctionAssociationProperty"]]]]:
            """``CfnDistribution.CacheBehaviorProperty.LambdaFunctionAssociations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-lambdafunctionassociations
            """
            result = self._values.get("lambda_function_associations")
            return result

        @builtins.property
        def max_ttl(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CacheBehaviorProperty.MaxTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-maxttl
            """
            result = self._values.get("max_ttl")
            return result

        @builtins.property
        def min_ttl(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CacheBehaviorProperty.MinTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-minttl
            """
            result = self._values.get("min_ttl")
            return result

        @builtins.property
        def origin_request_policy_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.CacheBehaviorProperty.OriginRequestPolicyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-originrequestpolicyid
            """
            result = self._values.get("origin_request_policy_id")
            return result

        @builtins.property
        def realtime_log_config_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.CacheBehaviorProperty.RealtimeLogConfigArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-realtimelogconfigarn
            """
            result = self._values.get("realtime_log_config_arn")
            return result

        @builtins.property
        def smooth_streaming(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.CacheBehaviorProperty.SmoothStreaming``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-smoothstreaming
            """
            result = self._values.get("smooth_streaming")
            return result

        @builtins.property
        def trusted_signers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.CacheBehaviorProperty.TrustedSigners``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-trustedsigners
            """
            result = self._values.get("trusted_signers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheBehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CookiesProperty",
        jsii_struct_bases=[],
        name_mapping={"forward": "forward", "whitelisted_names": "whitelistedNames"},
    )
    class CookiesProperty:
        def __init__(
            self,
            *,
            forward: builtins.str,
            whitelisted_names: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param forward: ``CfnDistribution.CookiesProperty.Forward``.
            :param whitelisted_names: ``CfnDistribution.CookiesProperty.WhitelistedNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "forward": forward,
            }
            if whitelisted_names is not None:
                self._values["whitelisted_names"] = whitelisted_names

        @builtins.property
        def forward(self) -> builtins.str:
            """``CfnDistribution.CookiesProperty.Forward``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html#cfn-cloudfront-distribution-cookies-forward
            """
            result = self._values.get("forward")
            assert result is not None, "Required property 'forward' is missing"
            return result

        @builtins.property
        def whitelisted_names(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.CookiesProperty.WhitelistedNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html#cfn-cloudfront-distribution-cookies-whitelistednames
            """
            result = self._values.get("whitelisted_names")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CookiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomErrorResponseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_code": "errorCode",
            "error_caching_min_ttl": "errorCachingMinTtl",
            "response_code": "responseCode",
            "response_page_path": "responsePagePath",
        },
    )
    class CustomErrorResponseProperty:
        def __init__(
            self,
            *,
            error_code: jsii.Number,
            error_caching_min_ttl: typing.Optional[jsii.Number] = None,
            response_code: typing.Optional[jsii.Number] = None,
            response_page_path: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param error_code: ``CfnDistribution.CustomErrorResponseProperty.ErrorCode``.
            :param error_caching_min_ttl: ``CfnDistribution.CustomErrorResponseProperty.ErrorCachingMinTTL``.
            :param response_code: ``CfnDistribution.CustomErrorResponseProperty.ResponseCode``.
            :param response_page_path: ``CfnDistribution.CustomErrorResponseProperty.ResponsePagePath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "error_code": error_code,
            }
            if error_caching_min_ttl is not None:
                self._values["error_caching_min_ttl"] = error_caching_min_ttl
            if response_code is not None:
                self._values["response_code"] = response_code
            if response_page_path is not None:
                self._values["response_page_path"] = response_page_path

        @builtins.property
        def error_code(self) -> jsii.Number:
            """``CfnDistribution.CustomErrorResponseProperty.ErrorCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-errorcode
            """
            result = self._values.get("error_code")
            assert result is not None, "Required property 'error_code' is missing"
            return result

        @builtins.property
        def error_caching_min_ttl(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CustomErrorResponseProperty.ErrorCachingMinTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-errorcachingminttl
            """
            result = self._values.get("error_caching_min_ttl")
            return result

        @builtins.property
        def response_code(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CustomErrorResponseProperty.ResponseCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-responsecode
            """
            result = self._values.get("response_code")
            return result

        @builtins.property
        def response_page_path(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.CustomErrorResponseProperty.ResponsePagePath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-responsepagepath
            """
            result = self._values.get("response_page_path")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomErrorResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomOriginConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "origin_protocol_policy": "originProtocolPolicy",
            "http_port": "httpPort",
            "https_port": "httpsPort",
            "origin_keepalive_timeout": "originKeepaliveTimeout",
            "origin_read_timeout": "originReadTimeout",
            "origin_ssl_protocols": "originSslProtocols",
        },
    )
    class CustomOriginConfigProperty:
        def __init__(
            self,
            *,
            origin_protocol_policy: builtins.str,
            http_port: typing.Optional[jsii.Number] = None,
            https_port: typing.Optional[jsii.Number] = None,
            origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
            origin_read_timeout: typing.Optional[jsii.Number] = None,
            origin_ssl_protocols: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param origin_protocol_policy: ``CfnDistribution.CustomOriginConfigProperty.OriginProtocolPolicy``.
            :param http_port: ``CfnDistribution.CustomOriginConfigProperty.HTTPPort``.
            :param https_port: ``CfnDistribution.CustomOriginConfigProperty.HTTPSPort``.
            :param origin_keepalive_timeout: ``CfnDistribution.CustomOriginConfigProperty.OriginKeepaliveTimeout``.
            :param origin_read_timeout: ``CfnDistribution.CustomOriginConfigProperty.OriginReadTimeout``.
            :param origin_ssl_protocols: ``CfnDistribution.CustomOriginConfigProperty.OriginSSLProtocols``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "origin_protocol_policy": origin_protocol_policy,
            }
            if http_port is not None:
                self._values["http_port"] = http_port
            if https_port is not None:
                self._values["https_port"] = https_port
            if origin_keepalive_timeout is not None:
                self._values["origin_keepalive_timeout"] = origin_keepalive_timeout
            if origin_read_timeout is not None:
                self._values["origin_read_timeout"] = origin_read_timeout
            if origin_ssl_protocols is not None:
                self._values["origin_ssl_protocols"] = origin_ssl_protocols

        @builtins.property
        def origin_protocol_policy(self) -> builtins.str:
            """``CfnDistribution.CustomOriginConfigProperty.OriginProtocolPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originprotocolpolicy
            """
            result = self._values.get("origin_protocol_policy")
            assert result is not None, "Required property 'origin_protocol_policy' is missing"
            return result

        @builtins.property
        def http_port(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CustomOriginConfigProperty.HTTPPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-httpport
            """
            result = self._values.get("http_port")
            return result

        @builtins.property
        def https_port(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CustomOriginConfigProperty.HTTPSPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-httpsport
            """
            result = self._values.get("https_port")
            return result

        @builtins.property
        def origin_keepalive_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CustomOriginConfigProperty.OriginKeepaliveTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originkeepalivetimeout
            """
            result = self._values.get("origin_keepalive_timeout")
            return result

        @builtins.property
        def origin_read_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.CustomOriginConfigProperty.OriginReadTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originreadtimeout
            """
            result = self._values.get("origin_read_timeout")
            return result

        @builtins.property
        def origin_ssl_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.CustomOriginConfigProperty.OriginSSLProtocols``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originsslprotocols
            """
            result = self._values.get("origin_ssl_protocols")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomOriginConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DefaultCacheBehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_origin_id": "targetOriginId",
            "viewer_protocol_policy": "viewerProtocolPolicy",
            "allowed_methods": "allowedMethods",
            "cached_methods": "cachedMethods",
            "cache_policy_id": "cachePolicyId",
            "compress": "compress",
            "default_ttl": "defaultTtl",
            "field_level_encryption_id": "fieldLevelEncryptionId",
            "forwarded_values": "forwardedValues",
            "lambda_function_associations": "lambdaFunctionAssociations",
            "max_ttl": "maxTtl",
            "min_ttl": "minTtl",
            "origin_request_policy_id": "originRequestPolicyId",
            "realtime_log_config_arn": "realtimeLogConfigArn",
            "smooth_streaming": "smoothStreaming",
            "trusted_signers": "trustedSigners",
        },
    )
    class DefaultCacheBehaviorProperty:
        def __init__(
            self,
            *,
            target_origin_id: builtins.str,
            viewer_protocol_policy: builtins.str,
            allowed_methods: typing.Optional[typing.List[builtins.str]] = None,
            cached_methods: typing.Optional[typing.List[builtins.str]] = None,
            cache_policy_id: typing.Optional[builtins.str] = None,
            compress: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            default_ttl: typing.Optional[jsii.Number] = None,
            field_level_encryption_id: typing.Optional[builtins.str] = None,
            forwarded_values: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.ForwardedValuesProperty"]] = None,
            lambda_function_associations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LambdaFunctionAssociationProperty"]]]] = None,
            max_ttl: typing.Optional[jsii.Number] = None,
            min_ttl: typing.Optional[jsii.Number] = None,
            origin_request_policy_id: typing.Optional[builtins.str] = None,
            realtime_log_config_arn: typing.Optional[builtins.str] = None,
            smooth_streaming: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            trusted_signers: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param target_origin_id: ``CfnDistribution.DefaultCacheBehaviorProperty.TargetOriginId``.
            :param viewer_protocol_policy: ``CfnDistribution.DefaultCacheBehaviorProperty.ViewerProtocolPolicy``.
            :param allowed_methods: ``CfnDistribution.DefaultCacheBehaviorProperty.AllowedMethods``.
            :param cached_methods: ``CfnDistribution.DefaultCacheBehaviorProperty.CachedMethods``.
            :param cache_policy_id: ``CfnDistribution.DefaultCacheBehaviorProperty.CachePolicyId``.
            :param compress: ``CfnDistribution.DefaultCacheBehaviorProperty.Compress``.
            :param default_ttl: ``CfnDistribution.DefaultCacheBehaviorProperty.DefaultTTL``.
            :param field_level_encryption_id: ``CfnDistribution.DefaultCacheBehaviorProperty.FieldLevelEncryptionId``.
            :param forwarded_values: ``CfnDistribution.DefaultCacheBehaviorProperty.ForwardedValues``.
            :param lambda_function_associations: ``CfnDistribution.DefaultCacheBehaviorProperty.LambdaFunctionAssociations``.
            :param max_ttl: ``CfnDistribution.DefaultCacheBehaviorProperty.MaxTTL``.
            :param min_ttl: ``CfnDistribution.DefaultCacheBehaviorProperty.MinTTL``.
            :param origin_request_policy_id: ``CfnDistribution.DefaultCacheBehaviorProperty.OriginRequestPolicyId``.
            :param realtime_log_config_arn: ``CfnDistribution.DefaultCacheBehaviorProperty.RealtimeLogConfigArn``.
            :param smooth_streaming: ``CfnDistribution.DefaultCacheBehaviorProperty.SmoothStreaming``.
            :param trusted_signers: ``CfnDistribution.DefaultCacheBehaviorProperty.TrustedSigners``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "target_origin_id": target_origin_id,
                "viewer_protocol_policy": viewer_protocol_policy,
            }
            if allowed_methods is not None:
                self._values["allowed_methods"] = allowed_methods
            if cached_methods is not None:
                self._values["cached_methods"] = cached_methods
            if cache_policy_id is not None:
                self._values["cache_policy_id"] = cache_policy_id
            if compress is not None:
                self._values["compress"] = compress
            if default_ttl is not None:
                self._values["default_ttl"] = default_ttl
            if field_level_encryption_id is not None:
                self._values["field_level_encryption_id"] = field_level_encryption_id
            if forwarded_values is not None:
                self._values["forwarded_values"] = forwarded_values
            if lambda_function_associations is not None:
                self._values["lambda_function_associations"] = lambda_function_associations
            if max_ttl is not None:
                self._values["max_ttl"] = max_ttl
            if min_ttl is not None:
                self._values["min_ttl"] = min_ttl
            if origin_request_policy_id is not None:
                self._values["origin_request_policy_id"] = origin_request_policy_id
            if realtime_log_config_arn is not None:
                self._values["realtime_log_config_arn"] = realtime_log_config_arn
            if smooth_streaming is not None:
                self._values["smooth_streaming"] = smooth_streaming
            if trusted_signers is not None:
                self._values["trusted_signers"] = trusted_signers

        @builtins.property
        def target_origin_id(self) -> builtins.str:
            """``CfnDistribution.DefaultCacheBehaviorProperty.TargetOriginId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-targetoriginid
            """
            result = self._values.get("target_origin_id")
            assert result is not None, "Required property 'target_origin_id' is missing"
            return result

        @builtins.property
        def viewer_protocol_policy(self) -> builtins.str:
            """``CfnDistribution.DefaultCacheBehaviorProperty.ViewerProtocolPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-viewerprotocolpolicy
            """
            result = self._values.get("viewer_protocol_policy")
            assert result is not None, "Required property 'viewer_protocol_policy' is missing"
            return result

        @builtins.property
        def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.AllowedMethods``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-allowedmethods
            """
            result = self._values.get("allowed_methods")
            return result

        @builtins.property
        def cached_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.CachedMethods``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-cachedmethods
            """
            result = self._values.get("cached_methods")
            return result

        @builtins.property
        def cache_policy_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.CachePolicyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-cachepolicyid
            """
            result = self._values.get("cache_policy_id")
            return result

        @builtins.property
        def compress(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.Compress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-compress
            """
            result = self._values.get("compress")
            return result

        @builtins.property
        def default_ttl(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.DefaultTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-defaultttl
            """
            result = self._values.get("default_ttl")
            return result

        @builtins.property
        def field_level_encryption_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.FieldLevelEncryptionId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-fieldlevelencryptionid
            """
            result = self._values.get("field_level_encryption_id")
            return result

        @builtins.property
        def forwarded_values(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.ForwardedValuesProperty"]]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.ForwardedValues``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-forwardedvalues
            """
            result = self._values.get("forwarded_values")
            return result

        @builtins.property
        def lambda_function_associations(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LambdaFunctionAssociationProperty"]]]]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.LambdaFunctionAssociations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-lambdafunctionassociations
            """
            result = self._values.get("lambda_function_associations")
            return result

        @builtins.property
        def max_ttl(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.MaxTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-maxttl
            """
            result = self._values.get("max_ttl")
            return result

        @builtins.property
        def min_ttl(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.MinTTL``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-minttl
            """
            result = self._values.get("min_ttl")
            return result

        @builtins.property
        def origin_request_policy_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.OriginRequestPolicyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-originrequestpolicyid
            """
            result = self._values.get("origin_request_policy_id")
            return result

        @builtins.property
        def realtime_log_config_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.RealtimeLogConfigArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-realtimelogconfigarn
            """
            result = self._values.get("realtime_log_config_arn")
            return result

        @builtins.property
        def smooth_streaming(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.SmoothStreaming``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-smoothstreaming
            """
            result = self._values.get("smooth_streaming")
            return result

        @builtins.property
        def trusted_signers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.DefaultCacheBehaviorProperty.TrustedSigners``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-trustedsigners
            """
            result = self._values.get("trusted_signers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultCacheBehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DistributionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "aliases": "aliases",
            "cache_behaviors": "cacheBehaviors",
            "comment": "comment",
            "custom_error_responses": "customErrorResponses",
            "default_cache_behavior": "defaultCacheBehavior",
            "default_root_object": "defaultRootObject",
            "http_version": "httpVersion",
            "ipv6_enabled": "ipv6Enabled",
            "logging": "logging",
            "origin_groups": "originGroups",
            "origins": "origins",
            "price_class": "priceClass",
            "restrictions": "restrictions",
            "viewer_certificate": "viewerCertificate",
            "web_acl_id": "webAclId",
        },
    )
    class DistributionConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            aliases: typing.Optional[typing.List[builtins.str]] = None,
            cache_behaviors: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CacheBehaviorProperty"]]]] = None,
            comment: typing.Optional[builtins.str] = None,
            custom_error_responses: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CustomErrorResponseProperty"]]]] = None,
            default_cache_behavior: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.DefaultCacheBehaviorProperty"]] = None,
            default_root_object: typing.Optional[builtins.str] = None,
            http_version: typing.Optional[builtins.str] = None,
            ipv6_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            logging: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LoggingProperty"]] = None,
            origin_groups: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupsProperty"]] = None,
            origins: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnDistribution.OriginProperty", aws_cdk.core.IResolvable]]]] = None,
            price_class: typing.Optional[builtins.str] = None,
            restrictions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.RestrictionsProperty"]] = None,
            viewer_certificate: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.ViewerCertificateProperty"]] = None,
            web_acl_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enabled: ``CfnDistribution.DistributionConfigProperty.Enabled``.
            :param aliases: ``CfnDistribution.DistributionConfigProperty.Aliases``.
            :param cache_behaviors: ``CfnDistribution.DistributionConfigProperty.CacheBehaviors``.
            :param comment: ``CfnDistribution.DistributionConfigProperty.Comment``.
            :param custom_error_responses: ``CfnDistribution.DistributionConfigProperty.CustomErrorResponses``.
            :param default_cache_behavior: ``CfnDistribution.DistributionConfigProperty.DefaultCacheBehavior``.
            :param default_root_object: ``CfnDistribution.DistributionConfigProperty.DefaultRootObject``.
            :param http_version: ``CfnDistribution.DistributionConfigProperty.HttpVersion``.
            :param ipv6_enabled: ``CfnDistribution.DistributionConfigProperty.IPV6Enabled``.
            :param logging: ``CfnDistribution.DistributionConfigProperty.Logging``.
            :param origin_groups: ``CfnDistribution.DistributionConfigProperty.OriginGroups``.
            :param origins: ``CfnDistribution.DistributionConfigProperty.Origins``.
            :param price_class: ``CfnDistribution.DistributionConfigProperty.PriceClass``.
            :param restrictions: ``CfnDistribution.DistributionConfigProperty.Restrictions``.
            :param viewer_certificate: ``CfnDistribution.DistributionConfigProperty.ViewerCertificate``.
            :param web_acl_id: ``CfnDistribution.DistributionConfigProperty.WebACLId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if aliases is not None:
                self._values["aliases"] = aliases
            if cache_behaviors is not None:
                self._values["cache_behaviors"] = cache_behaviors
            if comment is not None:
                self._values["comment"] = comment
            if custom_error_responses is not None:
                self._values["custom_error_responses"] = custom_error_responses
            if default_cache_behavior is not None:
                self._values["default_cache_behavior"] = default_cache_behavior
            if default_root_object is not None:
                self._values["default_root_object"] = default_root_object
            if http_version is not None:
                self._values["http_version"] = http_version
            if ipv6_enabled is not None:
                self._values["ipv6_enabled"] = ipv6_enabled
            if logging is not None:
                self._values["logging"] = logging
            if origin_groups is not None:
                self._values["origin_groups"] = origin_groups
            if origins is not None:
                self._values["origins"] = origins
            if price_class is not None:
                self._values["price_class"] = price_class
            if restrictions is not None:
                self._values["restrictions"] = restrictions
            if viewer_certificate is not None:
                self._values["viewer_certificate"] = viewer_certificate
            if web_acl_id is not None:
                self._values["web_acl_id"] = web_acl_id

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnDistribution.DistributionConfigProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.DistributionConfigProperty.Aliases``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-aliases
            """
            result = self._values.get("aliases")
            return result

        @builtins.property
        def cache_behaviors(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CacheBehaviorProperty"]]]]:
            """``CfnDistribution.DistributionConfigProperty.CacheBehaviors``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-cachebehaviors
            """
            result = self._values.get("cache_behaviors")
            return result

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DistributionConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-comment
            """
            result = self._values.get("comment")
            return result

        @builtins.property
        def custom_error_responses(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CustomErrorResponseProperty"]]]]:
            """``CfnDistribution.DistributionConfigProperty.CustomErrorResponses``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-customerrorresponses
            """
            result = self._values.get("custom_error_responses")
            return result

        @builtins.property
        def default_cache_behavior(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.DefaultCacheBehaviorProperty"]]:
            """``CfnDistribution.DistributionConfigProperty.DefaultCacheBehavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-defaultcachebehavior
            """
            result = self._values.get("default_cache_behavior")
            return result

        @builtins.property
        def default_root_object(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DistributionConfigProperty.DefaultRootObject``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-defaultrootobject
            """
            result = self._values.get("default_root_object")
            return result

        @builtins.property
        def http_version(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DistributionConfigProperty.HttpVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-httpversion
            """
            result = self._values.get("http_version")
            return result

        @builtins.property
        def ipv6_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.DistributionConfigProperty.IPV6Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-ipv6enabled
            """
            result = self._values.get("ipv6_enabled")
            return result

        @builtins.property
        def logging(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LoggingProperty"]]:
            """``CfnDistribution.DistributionConfigProperty.Logging``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-logging
            """
            result = self._values.get("logging")
            return result

        @builtins.property
        def origin_groups(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupsProperty"]]:
            """``CfnDistribution.DistributionConfigProperty.OriginGroups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-origingroups
            """
            result = self._values.get("origin_groups")
            return result

        @builtins.property
        def origins(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnDistribution.OriginProperty", aws_cdk.core.IResolvable]]]]:
            """``CfnDistribution.DistributionConfigProperty.Origins``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-origins
            """
            result = self._values.get("origins")
            return result

        @builtins.property
        def price_class(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DistributionConfigProperty.PriceClass``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-priceclass
            """
            result = self._values.get("price_class")
            return result

        @builtins.property
        def restrictions(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.RestrictionsProperty"]]:
            """``CfnDistribution.DistributionConfigProperty.Restrictions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-restrictions
            """
            result = self._values.get("restrictions")
            return result

        @builtins.property
        def viewer_certificate(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.ViewerCertificateProperty"]]:
            """``CfnDistribution.DistributionConfigProperty.ViewerCertificate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-viewercertificate
            """
            result = self._values.get("viewer_certificate")
            return result

        @builtins.property
        def web_acl_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.DistributionConfigProperty.WebACLId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-webaclid
            """
            result = self._values.get("web_acl_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DistributionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ForwardedValuesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_string": "queryString",
            "cookies": "cookies",
            "headers": "headers",
            "query_string_cache_keys": "queryStringCacheKeys",
        },
    )
    class ForwardedValuesProperty:
        def __init__(
            self,
            *,
            query_string: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            cookies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CookiesProperty"]] = None,
            headers: typing.Optional[typing.List[builtins.str]] = None,
            query_string_cache_keys: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param query_string: ``CfnDistribution.ForwardedValuesProperty.QueryString``.
            :param cookies: ``CfnDistribution.ForwardedValuesProperty.Cookies``.
            :param headers: ``CfnDistribution.ForwardedValuesProperty.Headers``.
            :param query_string_cache_keys: ``CfnDistribution.ForwardedValuesProperty.QueryStringCacheKeys``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "query_string": query_string,
            }
            if cookies is not None:
                self._values["cookies"] = cookies
            if headers is not None:
                self._values["headers"] = headers
            if query_string_cache_keys is not None:
                self._values["query_string_cache_keys"] = query_string_cache_keys

        @builtins.property
        def query_string(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnDistribution.ForwardedValuesProperty.QueryString``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-querystring
            """
            result = self._values.get("query_string")
            assert result is not None, "Required property 'query_string' is missing"
            return result

        @builtins.property
        def cookies(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CookiesProperty"]]:
            """``CfnDistribution.ForwardedValuesProperty.Cookies``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-cookies
            """
            result = self._values.get("cookies")
            return result

        @builtins.property
        def headers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.ForwardedValuesProperty.Headers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-headers
            """
            result = self._values.get("headers")
            return result

        @builtins.property
        def query_string_cache_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.ForwardedValuesProperty.QueryStringCacheKeys``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-querystringcachekeys
            """
            result = self._values.get("query_string_cache_keys")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardedValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.GeoRestrictionProperty",
        jsii_struct_bases=[],
        name_mapping={"restriction_type": "restrictionType", "locations": "locations"},
    )
    class GeoRestrictionProperty:
        def __init__(
            self,
            *,
            restriction_type: builtins.str,
            locations: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param restriction_type: ``CfnDistribution.GeoRestrictionProperty.RestrictionType``.
            :param locations: ``CfnDistribution.GeoRestrictionProperty.Locations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "restriction_type": restriction_type,
            }
            if locations is not None:
                self._values["locations"] = locations

        @builtins.property
        def restriction_type(self) -> builtins.str:
            """``CfnDistribution.GeoRestrictionProperty.RestrictionType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html#cfn-cloudfront-distribution-georestriction-restrictiontype
            """
            result = self._values.get("restriction_type")
            assert result is not None, "Required property 'restriction_type' is missing"
            return result

        @builtins.property
        def locations(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnDistribution.GeoRestrictionProperty.Locations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html#cfn-cloudfront-distribution-georestriction-locations
            """
            result = self._values.get("locations")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoRestrictionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LambdaFunctionAssociationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_type": "eventType",
            "include_body": "includeBody",
            "lambda_function_arn": "lambdaFunctionArn",
        },
    )
    class LambdaFunctionAssociationProperty:
        def __init__(
            self,
            *,
            event_type: typing.Optional[builtins.str] = None,
            include_body: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            lambda_function_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param event_type: ``CfnDistribution.LambdaFunctionAssociationProperty.EventType``.
            :param include_body: ``CfnDistribution.LambdaFunctionAssociationProperty.IncludeBody``.
            :param lambda_function_arn: ``CfnDistribution.LambdaFunctionAssociationProperty.LambdaFunctionARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if event_type is not None:
                self._values["event_type"] = event_type
            if include_body is not None:
                self._values["include_body"] = include_body
            if lambda_function_arn is not None:
                self._values["lambda_function_arn"] = lambda_function_arn

        @builtins.property
        def event_type(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.LambdaFunctionAssociationProperty.EventType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html#cfn-cloudfront-distribution-lambdafunctionassociation-eventtype
            """
            result = self._values.get("event_type")
            return result

        @builtins.property
        def include_body(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.LambdaFunctionAssociationProperty.IncludeBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html#cfn-cloudfront-distribution-lambdafunctionassociation-includebody
            """
            result = self._values.get("include_body")
            return result

        @builtins.property
        def lambda_function_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.LambdaFunctionAssociationProperty.LambdaFunctionARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html#cfn-cloudfront-distribution-lambdafunctionassociation-lambdafunctionarn
            """
            result = self._values.get("lambda_function_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaFunctionAssociationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LoggingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "include_cookies": "includeCookies",
            "prefix": "prefix",
        },
    )
    class LoggingProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            include_cookies: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket: ``CfnDistribution.LoggingProperty.Bucket``.
            :param include_cookies: ``CfnDistribution.LoggingProperty.IncludeCookies``.
            :param prefix: ``CfnDistribution.LoggingProperty.Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
            }
            if include_cookies is not None:
                self._values["include_cookies"] = include_cookies
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket(self) -> builtins.str:
            """``CfnDistribution.LoggingProperty.Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-bucket
            """
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return result

        @builtins.property
        def include_cookies(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.LoggingProperty.IncludeCookies``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-includecookies
            """
            result = self._values.get("include_cookies")
            return result

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.LoggingProperty.Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-prefix
            """
            result = self._values.get("prefix")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginCustomHeaderProperty",
        jsii_struct_bases=[],
        name_mapping={"header_name": "headerName", "header_value": "headerValue"},
    )
    class OriginCustomHeaderProperty:
        def __init__(
            self,
            *,
            header_name: builtins.str,
            header_value: builtins.str,
        ) -> None:
            """
            :param header_name: ``CfnDistribution.OriginCustomHeaderProperty.HeaderName``.
            :param header_value: ``CfnDistribution.OriginCustomHeaderProperty.HeaderValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "header_name": header_name,
                "header_value": header_value,
            }

        @builtins.property
        def header_name(self) -> builtins.str:
            """``CfnDistribution.OriginCustomHeaderProperty.HeaderName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html#cfn-cloudfront-distribution-origincustomheader-headername
            """
            result = self._values.get("header_name")
            assert result is not None, "Required property 'header_name' is missing"
            return result

        @builtins.property
        def header_value(self) -> builtins.str:
            """``CfnDistribution.OriginCustomHeaderProperty.HeaderValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html#cfn-cloudfront-distribution-origincustomheader-headervalue
            """
            result = self._values.get("header_value")
            assert result is not None, "Required property 'header_value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginCustomHeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginGroupFailoverCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"status_codes": "statusCodes"},
    )
    class OriginGroupFailoverCriteriaProperty:
        def __init__(
            self,
            *,
            status_codes: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.StatusCodesProperty"],
        ) -> None:
            """
            :param status_codes: ``CfnDistribution.OriginGroupFailoverCriteriaProperty.StatusCodes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroupfailovercriteria.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "status_codes": status_codes,
            }

        @builtins.property
        def status_codes(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.StatusCodesProperty"]:
            """``CfnDistribution.OriginGroupFailoverCriteriaProperty.StatusCodes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroupfailovercriteria.html#cfn-cloudfront-distribution-origingroupfailovercriteria-statuscodes
            """
            result = self._values.get("status_codes")
            assert result is not None, "Required property 'status_codes' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginGroupFailoverCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginGroupMemberProperty",
        jsii_struct_bases=[],
        name_mapping={"origin_id": "originId"},
    )
    class OriginGroupMemberProperty:
        def __init__(self, *, origin_id: builtins.str) -> None:
            """
            :param origin_id: ``CfnDistribution.OriginGroupMemberProperty.OriginId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroupmember.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "origin_id": origin_id,
            }

        @builtins.property
        def origin_id(self) -> builtins.str:
            """``CfnDistribution.OriginGroupMemberProperty.OriginId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroupmember.html#cfn-cloudfront-distribution-origingroupmember-originid
            """
            result = self._values.get("origin_id")
            assert result is not None, "Required property 'origin_id' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginGroupMemberProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginGroupMembersProperty",
        jsii_struct_bases=[],
        name_mapping={"items": "items", "quantity": "quantity"},
    )
    class OriginGroupMembersProperty:
        def __init__(
            self,
            *,
            items: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupMemberProperty"]]],
            quantity: jsii.Number,
        ) -> None:
            """
            :param items: ``CfnDistribution.OriginGroupMembersProperty.Items``.
            :param quantity: ``CfnDistribution.OriginGroupMembersProperty.Quantity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroupmembers.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "items": items,
                "quantity": quantity,
            }

        @builtins.property
        def items(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupMemberProperty"]]]:
            """``CfnDistribution.OriginGroupMembersProperty.Items``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroupmembers.html#cfn-cloudfront-distribution-origingroupmembers-items
            """
            result = self._values.get("items")
            assert result is not None, "Required property 'items' is missing"
            return result

        @builtins.property
        def quantity(self) -> jsii.Number:
            """``CfnDistribution.OriginGroupMembersProperty.Quantity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroupmembers.html#cfn-cloudfront-distribution-origingroupmembers-quantity
            """
            result = self._values.get("quantity")
            assert result is not None, "Required property 'quantity' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginGroupMembersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failover_criteria": "failoverCriteria",
            "id": "id",
            "members": "members",
        },
    )
    class OriginGroupProperty:
        def __init__(
            self,
            *,
            failover_criteria: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupFailoverCriteriaProperty"],
            id: builtins.str,
            members: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupMembersProperty"],
        ) -> None:
            """
            :param failover_criteria: ``CfnDistribution.OriginGroupProperty.FailoverCriteria``.
            :param id: ``CfnDistribution.OriginGroupProperty.Id``.
            :param members: ``CfnDistribution.OriginGroupProperty.Members``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroup.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "failover_criteria": failover_criteria,
                "id": id,
                "members": members,
            }

        @builtins.property
        def failover_criteria(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupFailoverCriteriaProperty"]:
            """``CfnDistribution.OriginGroupProperty.FailoverCriteria``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroup.html#cfn-cloudfront-distribution-origingroup-failovercriteria
            """
            result = self._values.get("failover_criteria")
            assert result is not None, "Required property 'failover_criteria' is missing"
            return result

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnDistribution.OriginGroupProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroup.html#cfn-cloudfront-distribution-origingroup-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def members(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupMembersProperty"]:
            """``CfnDistribution.OriginGroupProperty.Members``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroup.html#cfn-cloudfront-distribution-origingroup-members
            """
            result = self._values.get("members")
            assert result is not None, "Required property 'members' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginGroupsProperty",
        jsii_struct_bases=[],
        name_mapping={"quantity": "quantity", "items": "items"},
    )
    class OriginGroupsProperty:
        def __init__(
            self,
            *,
            quantity: jsii.Number,
            items: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupProperty"]]]] = None,
        ) -> None:
            """
            :param quantity: ``CfnDistribution.OriginGroupsProperty.Quantity``.
            :param items: ``CfnDistribution.OriginGroupsProperty.Items``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroups.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "quantity": quantity,
            }
            if items is not None:
                self._values["items"] = items

        @builtins.property
        def quantity(self) -> jsii.Number:
            """``CfnDistribution.OriginGroupsProperty.Quantity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroups.html#cfn-cloudfront-distribution-origingroups-quantity
            """
            result = self._values.get("quantity")
            assert result is not None, "Required property 'quantity' is missing"
            return result

        @builtins.property
        def items(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginGroupProperty"]]]]:
            """``CfnDistribution.OriginGroupsProperty.Items``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origingroups.html#cfn-cloudfront-distribution-origingroups-items
            """
            result = self._values.get("items")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginGroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "id": "id",
            "connection_attempts": "connectionAttempts",
            "connection_timeout": "connectionTimeout",
            "custom_origin_config": "customOriginConfig",
            "origin_custom_headers": "originCustomHeaders",
            "origin_path": "originPath",
            "origin_shield": "originShield",
            "s3_origin_config": "s3OriginConfig",
        },
    )
    class OriginProperty:
        def __init__(
            self,
            *,
            domain_name: builtins.str,
            id: builtins.str,
            connection_attempts: typing.Optional[jsii.Number] = None,
            connection_timeout: typing.Optional[jsii.Number] = None,
            custom_origin_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CustomOriginConfigProperty"]] = None,
            origin_custom_headers: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginCustomHeaderProperty"]]]] = None,
            origin_path: typing.Optional[builtins.str] = None,
            origin_shield: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginShieldProperty"]] = None,
            s3_origin_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.S3OriginConfigProperty"]] = None,
        ) -> None:
            """
            :param domain_name: ``CfnDistribution.OriginProperty.DomainName``.
            :param id: ``CfnDistribution.OriginProperty.Id``.
            :param connection_attempts: ``CfnDistribution.OriginProperty.ConnectionAttempts``.
            :param connection_timeout: ``CfnDistribution.OriginProperty.ConnectionTimeout``.
            :param custom_origin_config: ``CfnDistribution.OriginProperty.CustomOriginConfig``.
            :param origin_custom_headers: ``CfnDistribution.OriginProperty.OriginCustomHeaders``.
            :param origin_path: ``CfnDistribution.OriginProperty.OriginPath``.
            :param origin_shield: ``CfnDistribution.OriginProperty.OriginShield``.
            :param s3_origin_config: ``CfnDistribution.OriginProperty.S3OriginConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "domain_name": domain_name,
                "id": id,
            }
            if connection_attempts is not None:
                self._values["connection_attempts"] = connection_attempts
            if connection_timeout is not None:
                self._values["connection_timeout"] = connection_timeout
            if custom_origin_config is not None:
                self._values["custom_origin_config"] = custom_origin_config
            if origin_custom_headers is not None:
                self._values["origin_custom_headers"] = origin_custom_headers
            if origin_path is not None:
                self._values["origin_path"] = origin_path
            if origin_shield is not None:
                self._values["origin_shield"] = origin_shield
            if s3_origin_config is not None:
                self._values["s3_origin_config"] = s3_origin_config

        @builtins.property
        def domain_name(self) -> builtins.str:
            """``CfnDistribution.OriginProperty.DomainName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-domainname
            """
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return result

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnDistribution.OriginProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def connection_attempts(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.OriginProperty.ConnectionAttempts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-connectionattempts
            """
            result = self._values.get("connection_attempts")
            return result

        @builtins.property
        def connection_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnDistribution.OriginProperty.ConnectionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-connectiontimeout
            """
            result = self._values.get("connection_timeout")
            return result

        @builtins.property
        def custom_origin_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CustomOriginConfigProperty"]]:
            """``CfnDistribution.OriginProperty.CustomOriginConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-customoriginconfig
            """
            result = self._values.get("custom_origin_config")
            return result

        @builtins.property
        def origin_custom_headers(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginCustomHeaderProperty"]]]]:
            """``CfnDistribution.OriginProperty.OriginCustomHeaders``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-origincustomheaders
            """
            result = self._values.get("origin_custom_headers")
            return result

        @builtins.property
        def origin_path(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.OriginProperty.OriginPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-originpath
            """
            result = self._values.get("origin_path")
            return result

        @builtins.property
        def origin_shield(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginShieldProperty"]]:
            """``CfnDistribution.OriginProperty.OriginShield``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-originshield
            """
            result = self._values.get("origin_shield")
            return result

        @builtins.property
        def s3_origin_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.S3OriginConfigProperty"]]:
            """``CfnDistribution.OriginProperty.S3OriginConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-s3originconfig
            """
            result = self._values.get("s3_origin_config")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginShieldProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "origin_shield_region": "originShieldRegion",
        },
    )
    class OriginShieldProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            origin_shield_region: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enabled: ``CfnDistribution.OriginShieldProperty.Enabled``.
            :param origin_shield_region: ``CfnDistribution.OriginShieldProperty.OriginShieldRegion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-originshield.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if origin_shield_region is not None:
                self._values["origin_shield_region"] = origin_shield_region

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnDistribution.OriginShieldProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-originshield.html#cfn-cloudfront-distribution-originshield-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def origin_shield_region(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.OriginShieldProperty.OriginShieldRegion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-originshield.html#cfn-cloudfront-distribution-originshield-originshieldregion
            """
            result = self._values.get("origin_shield_region")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginShieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.RestrictionsProperty",
        jsii_struct_bases=[],
        name_mapping={"geo_restriction": "geoRestriction"},
    )
    class RestrictionsProperty:
        def __init__(
            self,
            *,
            geo_restriction: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.GeoRestrictionProperty"],
        ) -> None:
            """
            :param geo_restriction: ``CfnDistribution.RestrictionsProperty.GeoRestriction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-restrictions.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "geo_restriction": geo_restriction,
            }

        @builtins.property
        def geo_restriction(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.GeoRestrictionProperty"]:
            """``CfnDistribution.RestrictionsProperty.GeoRestriction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-restrictions.html#cfn-cloudfront-distribution-restrictions-georestriction
            """
            result = self._values.get("geo_restriction")
            assert result is not None, "Required property 'geo_restriction' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RestrictionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.S3OriginConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"origin_access_identity": "originAccessIdentity"},
    )
    class S3OriginConfigProperty:
        def __init__(
            self,
            *,
            origin_access_identity: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param origin_access_identity: ``CfnDistribution.S3OriginConfigProperty.OriginAccessIdentity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-s3originconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if origin_access_identity is not None:
                self._values["origin_access_identity"] = origin_access_identity

        @builtins.property
        def origin_access_identity(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.S3OriginConfigProperty.OriginAccessIdentity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-s3originconfig.html#cfn-cloudfront-distribution-s3originconfig-originaccessidentity
            """
            result = self._values.get("origin_access_identity")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OriginConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.StatusCodesProperty",
        jsii_struct_bases=[],
        name_mapping={"items": "items", "quantity": "quantity"},
    )
    class StatusCodesProperty:
        def __init__(
            self,
            *,
            items: typing.Union[aws_cdk.core.IResolvable, typing.List[jsii.Number]],
            quantity: jsii.Number,
        ) -> None:
            """
            :param items: ``CfnDistribution.StatusCodesProperty.Items``.
            :param quantity: ``CfnDistribution.StatusCodesProperty.Quantity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-statuscodes.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "items": items,
                "quantity": quantity,
            }

        @builtins.property
        def items(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[jsii.Number]]:
            """``CfnDistribution.StatusCodesProperty.Items``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-statuscodes.html#cfn-cloudfront-distribution-statuscodes-items
            """
            result = self._values.get("items")
            assert result is not None, "Required property 'items' is missing"
            return result

        @builtins.property
        def quantity(self) -> jsii.Number:
            """``CfnDistribution.StatusCodesProperty.Quantity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-statuscodes.html#cfn-cloudfront-distribution-statuscodes-quantity
            """
            result = self._values.get("quantity")
            assert result is not None, "Required property 'quantity' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusCodesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ViewerCertificateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acm_certificate_arn": "acmCertificateArn",
            "cloud_front_default_certificate": "cloudFrontDefaultCertificate",
            "iam_certificate_id": "iamCertificateId",
            "minimum_protocol_version": "minimumProtocolVersion",
            "ssl_support_method": "sslSupportMethod",
        },
    )
    class ViewerCertificateProperty:
        def __init__(
            self,
            *,
            acm_certificate_arn: typing.Optional[builtins.str] = None,
            cloud_front_default_certificate: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            iam_certificate_id: typing.Optional[builtins.str] = None,
            minimum_protocol_version: typing.Optional[builtins.str] = None,
            ssl_support_method: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param acm_certificate_arn: ``CfnDistribution.ViewerCertificateProperty.AcmCertificateArn``.
            :param cloud_front_default_certificate: ``CfnDistribution.ViewerCertificateProperty.CloudFrontDefaultCertificate``.
            :param iam_certificate_id: ``CfnDistribution.ViewerCertificateProperty.IamCertificateId``.
            :param minimum_protocol_version: ``CfnDistribution.ViewerCertificateProperty.MinimumProtocolVersion``.
            :param ssl_support_method: ``CfnDistribution.ViewerCertificateProperty.SslSupportMethod``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if acm_certificate_arn is not None:
                self._values["acm_certificate_arn"] = acm_certificate_arn
            if cloud_front_default_certificate is not None:
                self._values["cloud_front_default_certificate"] = cloud_front_default_certificate
            if iam_certificate_id is not None:
                self._values["iam_certificate_id"] = iam_certificate_id
            if minimum_protocol_version is not None:
                self._values["minimum_protocol_version"] = minimum_protocol_version
            if ssl_support_method is not None:
                self._values["ssl_support_method"] = ssl_support_method

        @builtins.property
        def acm_certificate_arn(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.ViewerCertificateProperty.AcmCertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-acmcertificatearn
            """
            result = self._values.get("acm_certificate_arn")
            return result

        @builtins.property
        def cloud_front_default_certificate(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnDistribution.ViewerCertificateProperty.CloudFrontDefaultCertificate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-cloudfrontdefaultcertificate
            """
            result = self._values.get("cloud_front_default_certificate")
            return result

        @builtins.property
        def iam_certificate_id(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.ViewerCertificateProperty.IamCertificateId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-iamcertificateid
            """
            result = self._values.get("iam_certificate_id")
            return result

        @builtins.property
        def minimum_protocol_version(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.ViewerCertificateProperty.MinimumProtocolVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-minimumprotocolversion
            """
            result = self._values.get("minimum_protocol_version")
            return result

        @builtins.property
        def ssl_support_method(self) -> typing.Optional[builtins.str]:
            """``CfnDistribution.ViewerCertificateProperty.SslSupportMethod``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-sslsupportmethod
            """
            result = self._values.get("ssl_support_method")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ViewerCertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CfnDistributionProps",
    jsii_struct_bases=[],
    name_mapping={"distribution_config": "distributionConfig", "tags": "tags"},
)
class CfnDistributionProps:
    def __init__(
        self,
        *,
        distribution_config: typing.Union[aws_cdk.core.IResolvable, CfnDistribution.DistributionConfigProperty],
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CloudFront::Distribution``.

        :param distribution_config: ``AWS::CloudFront::Distribution.DistributionConfig``.
        :param tags: ``AWS::CloudFront::Distribution.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "distribution_config": distribution_config,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def distribution_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnDistribution.DistributionConfigProperty]:
        """``AWS::CloudFront::Distribution.DistributionConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-distributionconfig
        """
        result = self._values.get("distribution_config")
        assert result is not None, "Required property 'distribution_config' is missing"
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CloudFront::Distribution.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnOriginRequestPolicy(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CfnOriginRequestPolicy",
):
    """A CloudFormation ``AWS::CloudFront::OriginRequestPolicy``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-originrequestpolicy.html
    :cloudformationResource: AWS::CloudFront::OriginRequestPolicy
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        origin_request_policy_config: typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty"],
    ) -> None:
        """Create a new ``AWS::CloudFront::OriginRequestPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param origin_request_policy_config: ``AWS::CloudFront::OriginRequestPolicy.OriginRequestPolicyConfig``.
        """
        props = CfnOriginRequestPolicyProps(
            origin_request_policy_config=origin_request_policy_config
        )

        jsii.create(CfnOriginRequestPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrLastModifiedTime")
    def attr_last_modified_time(self) -> builtins.str:
        """
        :cloudformationAttribute: LastModifiedTime
        """
        return jsii.get(self, "attrLastModifiedTime")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="originRequestPolicyConfig")
    def origin_request_policy_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty"]:
        """``AWS::CloudFront::OriginRequestPolicy.OriginRequestPolicyConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-originrequestpolicy.html#cfn-cloudfront-originrequestpolicy-originrequestpolicyconfig
        """
        return jsii.get(self, "originRequestPolicyConfig")

    @origin_request_policy_config.setter # type: ignore
    def origin_request_policy_config(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty"],
    ) -> None:
        jsii.set(self, "originRequestPolicyConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnOriginRequestPolicy.CookiesConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cookie_behavior": "cookieBehavior", "cookies": "cookies"},
    )
    class CookiesConfigProperty:
        def __init__(
            self,
            *,
            cookie_behavior: builtins.str,
            cookies: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param cookie_behavior: ``CfnOriginRequestPolicy.CookiesConfigProperty.CookieBehavior``.
            :param cookies: ``CfnOriginRequestPolicy.CookiesConfigProperty.Cookies``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-cookiesconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cookie_behavior": cookie_behavior,
            }
            if cookies is not None:
                self._values["cookies"] = cookies

        @builtins.property
        def cookie_behavior(self) -> builtins.str:
            """``CfnOriginRequestPolicy.CookiesConfigProperty.CookieBehavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-cookiesconfig.html#cfn-cloudfront-originrequestpolicy-cookiesconfig-cookiebehavior
            """
            result = self._values.get("cookie_behavior")
            assert result is not None, "Required property 'cookie_behavior' is missing"
            return result

        @builtins.property
        def cookies(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnOriginRequestPolicy.CookiesConfigProperty.Cookies``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-cookiesconfig.html#cfn-cloudfront-originrequestpolicy-cookiesconfig-cookies
            """
            result = self._values.get("cookies")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CookiesConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnOriginRequestPolicy.HeadersConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"header_behavior": "headerBehavior", "headers": "headers"},
    )
    class HeadersConfigProperty:
        def __init__(
            self,
            *,
            header_behavior: builtins.str,
            headers: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param header_behavior: ``CfnOriginRequestPolicy.HeadersConfigProperty.HeaderBehavior``.
            :param headers: ``CfnOriginRequestPolicy.HeadersConfigProperty.Headers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-headersconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "header_behavior": header_behavior,
            }
            if headers is not None:
                self._values["headers"] = headers

        @builtins.property
        def header_behavior(self) -> builtins.str:
            """``CfnOriginRequestPolicy.HeadersConfigProperty.HeaderBehavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-headersconfig.html#cfn-cloudfront-originrequestpolicy-headersconfig-headerbehavior
            """
            result = self._values.get("header_behavior")
            assert result is not None, "Required property 'header_behavior' is missing"
            return result

        @builtins.property
        def headers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnOriginRequestPolicy.HeadersConfigProperty.Headers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-headersconfig.html#cfn-cloudfront-originrequestpolicy-headersconfig-headers
            """
            result = self._values.get("headers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeadersConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cookies_config": "cookiesConfig",
            "headers_config": "headersConfig",
            "name": "name",
            "query_strings_config": "queryStringsConfig",
            "comment": "comment",
        },
    )
    class OriginRequestPolicyConfigProperty:
        def __init__(
            self,
            *,
            cookies_config: typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.CookiesConfigProperty"],
            headers_config: typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.HeadersConfigProperty"],
            name: builtins.str,
            query_strings_config: typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.QueryStringsConfigProperty"],
            comment: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param cookies_config: ``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.CookiesConfig``.
            :param headers_config: ``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.HeadersConfig``.
            :param name: ``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.Name``.
            :param query_strings_config: ``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.QueryStringsConfig``.
            :param comment: ``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-originrequestpolicyconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cookies_config": cookies_config,
                "headers_config": headers_config,
                "name": name,
                "query_strings_config": query_strings_config,
            }
            if comment is not None:
                self._values["comment"] = comment

        @builtins.property
        def cookies_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.CookiesConfigProperty"]:
            """``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.CookiesConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-originrequestpolicyconfig.html#cfn-cloudfront-originrequestpolicy-originrequestpolicyconfig-cookiesconfig
            """
            result = self._values.get("cookies_config")
            assert result is not None, "Required property 'cookies_config' is missing"
            return result

        @builtins.property
        def headers_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.HeadersConfigProperty"]:
            """``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.HeadersConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-originrequestpolicyconfig.html#cfn-cloudfront-originrequestpolicy-originrequestpolicyconfig-headersconfig
            """
            result = self._values.get("headers_config")
            assert result is not None, "Required property 'headers_config' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-originrequestpolicyconfig.html#cfn-cloudfront-originrequestpolicy-originrequestpolicyconfig-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def query_strings_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnOriginRequestPolicy.QueryStringsConfigProperty"]:
            """``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.QueryStringsConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-originrequestpolicyconfig.html#cfn-cloudfront-originrequestpolicy-originrequestpolicyconfig-querystringsconfig
            """
            result = self._values.get("query_strings_config")
            assert result is not None, "Required property 'query_strings_config' is missing"
            return result

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            """``CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-originrequestpolicyconfig.html#cfn-cloudfront-originrequestpolicy-originrequestpolicyconfig-comment
            """
            result = self._values.get("comment")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginRequestPolicyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnOriginRequestPolicy.QueryStringsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_string_behavior": "queryStringBehavior",
            "query_strings": "queryStrings",
        },
    )
    class QueryStringsConfigProperty:
        def __init__(
            self,
            *,
            query_string_behavior: builtins.str,
            query_strings: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param query_string_behavior: ``CfnOriginRequestPolicy.QueryStringsConfigProperty.QueryStringBehavior``.
            :param query_strings: ``CfnOriginRequestPolicy.QueryStringsConfigProperty.QueryStrings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-querystringsconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "query_string_behavior": query_string_behavior,
            }
            if query_strings is not None:
                self._values["query_strings"] = query_strings

        @builtins.property
        def query_string_behavior(self) -> builtins.str:
            """``CfnOriginRequestPolicy.QueryStringsConfigProperty.QueryStringBehavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-querystringsconfig.html#cfn-cloudfront-originrequestpolicy-querystringsconfig-querystringbehavior
            """
            result = self._values.get("query_string_behavior")
            assert result is not None, "Required property 'query_string_behavior' is missing"
            return result

        @builtins.property
        def query_strings(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnOriginRequestPolicy.QueryStringsConfigProperty.QueryStrings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-originrequestpolicy-querystringsconfig.html#cfn-cloudfront-originrequestpolicy-querystringsconfig-querystrings
            """
            result = self._values.get("query_strings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CfnOriginRequestPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"origin_request_policy_config": "originRequestPolicyConfig"},
)
class CfnOriginRequestPolicyProps:
    def __init__(
        self,
        *,
        origin_request_policy_config: typing.Union[aws_cdk.core.IResolvable, CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty],
    ) -> None:
        """Properties for defining a ``AWS::CloudFront::OriginRequestPolicy``.

        :param origin_request_policy_config: ``AWS::CloudFront::OriginRequestPolicy.OriginRequestPolicyConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-originrequestpolicy.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "origin_request_policy_config": origin_request_policy_config,
        }

    @builtins.property
    def origin_request_policy_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnOriginRequestPolicy.OriginRequestPolicyConfigProperty]:
        """``AWS::CloudFront::OriginRequestPolicy.OriginRequestPolicyConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-originrequestpolicy.html#cfn-cloudfront-originrequestpolicy-originrequestpolicyconfig
        """
        result = self._values.get("origin_request_policy_config")
        assert result is not None, "Required property 'origin_request_policy_config' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOriginRequestPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRealtimeLogConfig(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CfnRealtimeLogConfig",
):
    """A CloudFormation ``AWS::CloudFront::RealtimeLogConfig``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html
    :cloudformationResource: AWS::CloudFront::RealtimeLogConfig
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        end_points: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRealtimeLogConfig.EndPointProperty"]]],
        fields: typing.List[builtins.str],
        name: builtins.str,
        sampling_rate: jsii.Number,
    ) -> None:
        """Create a new ``AWS::CloudFront::RealtimeLogConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param end_points: ``AWS::CloudFront::RealtimeLogConfig.EndPoints``.
        :param fields: ``AWS::CloudFront::RealtimeLogConfig.Fields``.
        :param name: ``AWS::CloudFront::RealtimeLogConfig.Name``.
        :param sampling_rate: ``AWS::CloudFront::RealtimeLogConfig.SamplingRate``.
        """
        props = CfnRealtimeLogConfigProps(
            end_points=end_points,
            fields=fields,
            name=name,
            sampling_rate=sampling_rate,
        )

        jsii.create(CfnRealtimeLogConfig, self, [scope, id, props])

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
    @jsii.member(jsii_name="endPoints")
    def end_points(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRealtimeLogConfig.EndPointProperty"]]]:
        """``AWS::CloudFront::RealtimeLogConfig.EndPoints``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-endpoints
        """
        return jsii.get(self, "endPoints")

    @end_points.setter # type: ignore
    def end_points(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRealtimeLogConfig.EndPointProperty"]]],
    ) -> None:
        jsii.set(self, "endPoints", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[builtins.str]:
        """``AWS::CloudFront::RealtimeLogConfig.Fields``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-fields
        """
        return jsii.get(self, "fields")

    @fields.setter # type: ignore
    def fields(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "fields", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::CloudFront::RealtimeLogConfig.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="samplingRate")
    def sampling_rate(self) -> jsii.Number:
        """``AWS::CloudFront::RealtimeLogConfig.SamplingRate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-samplingrate
        """
        return jsii.get(self, "samplingRate")

    @sampling_rate.setter # type: ignore
    def sampling_rate(self, value: jsii.Number) -> None:
        jsii.set(self, "samplingRate", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnRealtimeLogConfig.EndPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kinesis_stream_config": "kinesisStreamConfig",
            "stream_type": "streamType",
        },
    )
    class EndPointProperty:
        def __init__(
            self,
            *,
            kinesis_stream_config: typing.Union[aws_cdk.core.IResolvable, "CfnRealtimeLogConfig.KinesisStreamConfigProperty"],
            stream_type: builtins.str,
        ) -> None:
            """
            :param kinesis_stream_config: ``CfnRealtimeLogConfig.EndPointProperty.KinesisStreamConfig``.
            :param stream_type: ``CfnRealtimeLogConfig.EndPointProperty.StreamType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-realtimelogconfig-endpoint.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "kinesis_stream_config": kinesis_stream_config,
                "stream_type": stream_type,
            }

        @builtins.property
        def kinesis_stream_config(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnRealtimeLogConfig.KinesisStreamConfigProperty"]:
            """``CfnRealtimeLogConfig.EndPointProperty.KinesisStreamConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-realtimelogconfig-endpoint.html#cfn-cloudfront-realtimelogconfig-endpoint-kinesisstreamconfig
            """
            result = self._values.get("kinesis_stream_config")
            assert result is not None, "Required property 'kinesis_stream_config' is missing"
            return result

        @builtins.property
        def stream_type(self) -> builtins.str:
            """``CfnRealtimeLogConfig.EndPointProperty.StreamType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-realtimelogconfig-endpoint.html#cfn-cloudfront-realtimelogconfig-endpoint-streamtype
            """
            result = self._values.get("stream_type")
            assert result is not None, "Required property 'stream_type' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnRealtimeLogConfig.KinesisStreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "stream_arn": "streamArn"},
    )
    class KinesisStreamConfigProperty:
        def __init__(self, *, role_arn: builtins.str, stream_arn: builtins.str) -> None:
            """
            :param role_arn: ``CfnRealtimeLogConfig.KinesisStreamConfigProperty.RoleArn``.
            :param stream_arn: ``CfnRealtimeLogConfig.KinesisStreamConfigProperty.StreamArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-realtimelogconfig-kinesisstreamconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "role_arn": role_arn,
                "stream_arn": stream_arn,
            }

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnRealtimeLogConfig.KinesisStreamConfigProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-realtimelogconfig-kinesisstreamconfig.html#cfn-cloudfront-realtimelogconfig-kinesisstreamconfig-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def stream_arn(self) -> builtins.str:
            """``CfnRealtimeLogConfig.KinesisStreamConfigProperty.StreamArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-realtimelogconfig-kinesisstreamconfig.html#cfn-cloudfront-realtimelogconfig-kinesisstreamconfig-streamarn
            """
            result = self._values.get("stream_arn")
            assert result is not None, "Required property 'stream_arn' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CfnRealtimeLogConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "end_points": "endPoints",
        "fields": "fields",
        "name": "name",
        "sampling_rate": "samplingRate",
    },
)
class CfnRealtimeLogConfigProps:
    def __init__(
        self,
        *,
        end_points: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnRealtimeLogConfig.EndPointProperty]]],
        fields: typing.List[builtins.str],
        name: builtins.str,
        sampling_rate: jsii.Number,
    ) -> None:
        """Properties for defining a ``AWS::CloudFront::RealtimeLogConfig``.

        :param end_points: ``AWS::CloudFront::RealtimeLogConfig.EndPoints``.
        :param fields: ``AWS::CloudFront::RealtimeLogConfig.Fields``.
        :param name: ``AWS::CloudFront::RealtimeLogConfig.Name``.
        :param sampling_rate: ``AWS::CloudFront::RealtimeLogConfig.SamplingRate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "end_points": end_points,
            "fields": fields,
            "name": name,
            "sampling_rate": sampling_rate,
        }

    @builtins.property
    def end_points(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnRealtimeLogConfig.EndPointProperty]]]:
        """``AWS::CloudFront::RealtimeLogConfig.EndPoints``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-endpoints
        """
        result = self._values.get("end_points")
        assert result is not None, "Required property 'end_points' is missing"
        return result

    @builtins.property
    def fields(self) -> typing.List[builtins.str]:
        """``AWS::CloudFront::RealtimeLogConfig.Fields``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-fields
        """
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::CloudFront::RealtimeLogConfig.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def sampling_rate(self) -> jsii.Number:
        """``AWS::CloudFront::RealtimeLogConfig.SamplingRate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-realtimelogconfig.html#cfn-cloudfront-realtimelogconfig-samplingrate
        """
        result = self._values.get("sampling_rate")
        assert result is not None, "Required property 'sampling_rate' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRealtimeLogConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStreamingDistribution(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution",
):
    """A CloudFormation ``AWS::CloudFront::StreamingDistribution``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html
    :cloudformationResource: AWS::CloudFront::StreamingDistribution
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        streaming_distribution_config: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.StreamingDistributionConfigProperty"],
        tags: typing.List[aws_cdk.core.CfnTag],
    ) -> None:
        """Create a new ``AWS::CloudFront::StreamingDistribution``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param streaming_distribution_config: ``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.
        :param tags: ``AWS::CloudFront::StreamingDistribution.Tags``.
        """
        props = CfnStreamingDistributionProps(
            streaming_distribution_config=streaming_distribution_config, tags=tags
        )

        jsii.create(CfnStreamingDistribution, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        """
        :cloudformationAttribute: DomainName
        """
        return jsii.get(self, "attrDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudFront::StreamingDistribution.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamingDistributionConfig")
    def streaming_distribution_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.StreamingDistributionConfigProperty"]:
        """``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig
        """
        return jsii.get(self, "streamingDistributionConfig")

    @streaming_distribution_config.setter # type: ignore
    def streaming_distribution_config(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.StreamingDistributionConfigProperty"],
    ) -> None:
        jsii.set(self, "streamingDistributionConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.LoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "enabled": "enabled", "prefix": "prefix"},
    )
    class LoggingProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            prefix: builtins.str,
        ) -> None:
            """
            :param bucket: ``CfnStreamingDistribution.LoggingProperty.Bucket``.
            :param enabled: ``CfnStreamingDistribution.LoggingProperty.Enabled``.
            :param prefix: ``CfnStreamingDistribution.LoggingProperty.Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "enabled": enabled,
                "prefix": prefix,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            """``CfnStreamingDistribution.LoggingProperty.Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-bucket
            """
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return result

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnStreamingDistribution.LoggingProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def prefix(self) -> builtins.str:
            """``CfnStreamingDistribution.LoggingProperty.Prefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-prefix
            """
            result = self._values.get("prefix")
            assert result is not None, "Required property 'prefix' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.S3OriginProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "origin_access_identity": "originAccessIdentity",
        },
    )
    class S3OriginProperty:
        def __init__(
            self,
            *,
            domain_name: builtins.str,
            origin_access_identity: builtins.str,
        ) -> None:
            """
            :param domain_name: ``CfnStreamingDistribution.S3OriginProperty.DomainName``.
            :param origin_access_identity: ``CfnStreamingDistribution.S3OriginProperty.OriginAccessIdentity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "domain_name": domain_name,
                "origin_access_identity": origin_access_identity,
            }

        @builtins.property
        def domain_name(self) -> builtins.str:
            """``CfnStreamingDistribution.S3OriginProperty.DomainName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html#cfn-cloudfront-streamingdistribution-s3origin-domainname
            """
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return result

        @builtins.property
        def origin_access_identity(self) -> builtins.str:
            """``CfnStreamingDistribution.S3OriginProperty.OriginAccessIdentity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html#cfn-cloudfront-streamingdistribution-s3origin-originaccessidentity
            """
            result = self._values.get("origin_access_identity")
            assert result is not None, "Required property 'origin_access_identity' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OriginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.StreamingDistributionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comment": "comment",
            "enabled": "enabled",
            "s3_origin": "s3Origin",
            "trusted_signers": "trustedSigners",
            "aliases": "aliases",
            "logging": "logging",
            "price_class": "priceClass",
        },
    )
    class StreamingDistributionConfigProperty:
        def __init__(
            self,
            *,
            comment: builtins.str,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            s3_origin: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.S3OriginProperty"],
            trusted_signers: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.TrustedSignersProperty"],
            aliases: typing.Optional[typing.List[builtins.str]] = None,
            logging: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.LoggingProperty"]] = None,
            price_class: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param comment: ``CfnStreamingDistribution.StreamingDistributionConfigProperty.Comment``.
            :param enabled: ``CfnStreamingDistribution.StreamingDistributionConfigProperty.Enabled``.
            :param s3_origin: ``CfnStreamingDistribution.StreamingDistributionConfigProperty.S3Origin``.
            :param trusted_signers: ``CfnStreamingDistribution.StreamingDistributionConfigProperty.TrustedSigners``.
            :param aliases: ``CfnStreamingDistribution.StreamingDistributionConfigProperty.Aliases``.
            :param logging: ``CfnStreamingDistribution.StreamingDistributionConfigProperty.Logging``.
            :param price_class: ``CfnStreamingDistribution.StreamingDistributionConfigProperty.PriceClass``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "comment": comment,
                "enabled": enabled,
                "s3_origin": s3_origin,
                "trusted_signers": trusted_signers,
            }
            if aliases is not None:
                self._values["aliases"] = aliases
            if logging is not None:
                self._values["logging"] = logging
            if price_class is not None:
                self._values["price_class"] = price_class

        @builtins.property
        def comment(self) -> builtins.str:
            """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-comment
            """
            result = self._values.get("comment")
            assert result is not None, "Required property 'comment' is missing"
            return result

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def s3_origin(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.S3OriginProperty"]:
            """``CfnStreamingDistribution.StreamingDistributionConfigProperty.S3Origin``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-s3origin
            """
            result = self._values.get("s3_origin")
            assert result is not None, "Required property 's3_origin' is missing"
            return result

        @builtins.property
        def trusted_signers(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.TrustedSignersProperty"]:
            """``CfnStreamingDistribution.StreamingDistributionConfigProperty.TrustedSigners``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-trustedsigners
            """
            result = self._values.get("trusted_signers")
            assert result is not None, "Required property 'trusted_signers' is missing"
            return result

        @builtins.property
        def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Aliases``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-aliases
            """
            result = self._values.get("aliases")
            return result

        @builtins.property
        def logging(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.LoggingProperty"]]:
            """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Logging``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-logging
            """
            result = self._values.get("logging")
            return result

        @builtins.property
        def price_class(self) -> typing.Optional[builtins.str]:
            """``CfnStreamingDistribution.StreamingDistributionConfigProperty.PriceClass``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-priceclass
            """
            result = self._values.get("price_class")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingDistributionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.TrustedSignersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "aws_account_numbers": "awsAccountNumbers",
        },
    )
    class TrustedSignersProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            aws_account_numbers: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param enabled: ``CfnStreamingDistribution.TrustedSignersProperty.Enabled``.
            :param aws_account_numbers: ``CfnStreamingDistribution.TrustedSignersProperty.AwsAccountNumbers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if aws_account_numbers is not None:
                self._values["aws_account_numbers"] = aws_account_numbers

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnStreamingDistribution.TrustedSignersProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html#cfn-cloudfront-streamingdistribution-trustedsigners-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def aws_account_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnStreamingDistribution.TrustedSignersProperty.AwsAccountNumbers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html#cfn-cloudfront-streamingdistribution-trustedsigners-awsaccountnumbers
            """
            result = self._values.get("aws_account_numbers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrustedSignersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistributionProps",
    jsii_struct_bases=[],
    name_mapping={
        "streaming_distribution_config": "streamingDistributionConfig",
        "tags": "tags",
    },
)
class CfnStreamingDistributionProps:
    def __init__(
        self,
        *,
        streaming_distribution_config: typing.Union[aws_cdk.core.IResolvable, CfnStreamingDistribution.StreamingDistributionConfigProperty],
        tags: typing.List[aws_cdk.core.CfnTag],
    ) -> None:
        """Properties for defining a ``AWS::CloudFront::StreamingDistribution``.

        :param streaming_distribution_config: ``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.
        :param tags: ``AWS::CloudFront::StreamingDistribution.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "streaming_distribution_config": streaming_distribution_config,
            "tags": tags,
        }

    @builtins.property
    def streaming_distribution_config(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnStreamingDistribution.StreamingDistributionConfigProperty]:
        """``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig
        """
        result = self._values.get("streaming_distribution_config")
        assert result is not None, "Required property 'streaming_distribution_config' is missing"
        return result

    @builtins.property
    def tags(self) -> typing.List[aws_cdk.core.CfnTag]:
        """``AWS::CloudFront::StreamingDistribution.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-tags
        """
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamingDistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedCachedMethods")
class CloudFrontAllowedCachedMethods(enum.Enum):
    """(experimental) Enums for the methods CloudFront can cache.

    :stability: experimental
    """

    GET_HEAD = "GET_HEAD"
    """
    :stability: experimental
    """
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"
    """
    :stability: experimental
    """


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedMethods")
class CloudFrontAllowedMethods(enum.Enum):
    """(experimental) An enum for the supported methods to a CloudFront distribution.

    :stability: experimental
    """

    GET_HEAD = "GET_HEAD"
    """
    :stability: experimental
    """
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"
    """
    :stability: experimental
    """
    ALL = "ALL"
    """
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistributionAttributes",
    jsii_struct_bases=[],
    name_mapping={"distribution_id": "distributionId", "domain_name": "domainName"},
)
class CloudFrontWebDistributionAttributes:
    def __init__(
        self,
        *,
        distribution_id: builtins.str,
        domain_name: builtins.str,
    ) -> None:
        """(experimental) Attributes used to import a Distribution.

        :param distribution_id: (experimental) The distribution ID for this distribution.
        :param domain_name: (experimental) The generated domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "distribution_id": distribution_id,
            "domain_name": domain_name,
        }

    @builtins.property
    def distribution_id(self) -> builtins.str:
        """(experimental) The distribution ID for this distribution.

        :stability: experimental
        :attribute: true
        """
        result = self._values.get("distribution_id")
        assert result is not None, "Required property 'distribution_id' is missing"
        return result

    @builtins.property
    def domain_name(self) -> builtins.str:
        """(experimental) The generated domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        :attribute: true
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontWebDistributionAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistributionProps",
    jsii_struct_bases=[],
    name_mapping={
        "origin_configs": "originConfigs",
        "alias_configuration": "aliasConfiguration",
        "comment": "comment",
        "default_root_object": "defaultRootObject",
        "enable_ip_v6": "enableIpV6",
        "error_configurations": "errorConfigurations",
        "geo_restriction": "geoRestriction",
        "http_version": "httpVersion",
        "logging_config": "loggingConfig",
        "price_class": "priceClass",
        "viewer_certificate": "viewerCertificate",
        "viewer_protocol_policy": "viewerProtocolPolicy",
        "web_acl_id": "webACLId",
    },
)
class CloudFrontWebDistributionProps:
    def __init__(
        self,
        *,
        origin_configs: typing.List["SourceConfiguration"],
        alias_configuration: typing.Optional[AliasConfiguration] = None,
        comment: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        enable_ip_v6: typing.Optional[builtins.bool] = None,
        error_configurations: typing.Optional[typing.List[CfnDistribution.CustomErrorResponseProperty]] = None,
        geo_restriction: typing.Optional["GeoRestriction"] = None,
        http_version: typing.Optional["HttpVersion"] = None,
        logging_config: typing.Optional["LoggingConfiguration"] = None,
        price_class: typing.Optional["PriceClass"] = None,
        viewer_certificate: typing.Optional["ViewerCertificate"] = None,
        viewer_protocol_policy: typing.Optional["ViewerProtocolPolicy"] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param origin_configs: (experimental) The origin configurations for this distribution. Behaviors are a part of the origin.
        :param alias_configuration: (deprecated) AliasConfiguration is used to configured CloudFront to respond to requests on custom domain names. Default: - None.
        :param comment: (experimental) A comment for this distribution in the CloudFront console. Default: - No comment is added to distribution.
        :param default_root_object: (experimental) The default object to serve. Default: - "index.html" is served.
        :param enable_ip_v6: (experimental) If your distribution should have IPv6 enabled. Default: true
        :param error_configurations: (experimental) How CloudFront should handle requests that are not successful (eg PageNotFound). By default, CloudFront does not replace HTTP status codes in the 4xx and 5xx range with custom error messages. CloudFront does not cache HTTP status codes. Default: - No custom error configuration.
        :param geo_restriction: (experimental) Controls the countries in which your content is distributed. Default: No geo restriction
        :param http_version: (experimental) The max supported HTTP Versions. Default: HttpVersion.HTTP2
        :param logging_config: (experimental) Optional - if we should enable logging. You can pass an empty object ({}) to have us auto create a bucket for logging. Omission of this property indicates no logging is to be enabled. Default: - no logging is enabled by default.
        :param price_class: (experimental) The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing). Default: PriceClass.PRICE_CLASS_100 the cheapest option for CloudFront is picked by default.
        :param viewer_certificate: (experimental) Specifies whether you want viewers to use HTTP or HTTPS to request your objects, whether you're using an alternate domain name with HTTPS, and if so, if you're using AWS Certificate Manager (ACM) or a third-party certificate authority. Default: ViewerCertificate.fromCloudFrontDefaultCertificate()
        :param viewer_protocol_policy: (experimental) The default viewer policy for incoming clients. Default: RedirectToHTTPs
        :param web_acl_id: (experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).

        :stability: experimental
        """
        if isinstance(alias_configuration, dict):
            alias_configuration = AliasConfiguration(**alias_configuration)
        if isinstance(logging_config, dict):
            logging_config = LoggingConfiguration(**logging_config)
        self._values: typing.Dict[str, typing.Any] = {
            "origin_configs": origin_configs,
        }
        if alias_configuration is not None:
            self._values["alias_configuration"] = alias_configuration
        if comment is not None:
            self._values["comment"] = comment
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if enable_ip_v6 is not None:
            self._values["enable_ip_v6"] = enable_ip_v6
        if error_configurations is not None:
            self._values["error_configurations"] = error_configurations
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if http_version is not None:
            self._values["http_version"] = http_version
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if price_class is not None:
            self._values["price_class"] = price_class
        if viewer_certificate is not None:
            self._values["viewer_certificate"] = viewer_certificate
        if viewer_protocol_policy is not None:
            self._values["viewer_protocol_policy"] = viewer_protocol_policy
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def origin_configs(self) -> typing.List["SourceConfiguration"]:
        """(experimental) The origin configurations for this distribution.

        Behaviors are a part of the origin.

        :stability: experimental
        """
        result = self._values.get("origin_configs")
        assert result is not None, "Required property 'origin_configs' is missing"
        return result

    @builtins.property
    def alias_configuration(self) -> typing.Optional[AliasConfiguration]:
        """(deprecated) AliasConfiguration is used to configured CloudFront to respond to requests on custom domain names.

        :default: - None.

        :deprecated: see {@link CloudFrontWebDistributionProps#viewerCertificate} with {@link ViewerCertificate#acmCertificate}

        :stability: deprecated
        """
        result = self._values.get("alias_configuration")
        return result

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """(experimental) A comment for this distribution in the CloudFront console.

        :default: - No comment is added to distribution.

        :stability: experimental
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        """(experimental) The default object to serve.

        :default: - "index.html" is served.

        :stability: experimental
        """
        result = self._values.get("default_root_object")
        return result

    @builtins.property
    def enable_ip_v6(self) -> typing.Optional[builtins.bool]:
        """(experimental) If your distribution should have IPv6 enabled.

        :default: true

        :stability: experimental
        """
        result = self._values.get("enable_ip_v6")
        return result

    @builtins.property
    def error_configurations(
        self,
    ) -> typing.Optional[typing.List[CfnDistribution.CustomErrorResponseProperty]]:
        """(experimental) How CloudFront should handle requests that are not successful (eg PageNotFound).

        By default, CloudFront does not replace HTTP status codes in the 4xx and 5xx range
        with custom error messages. CloudFront does not cache HTTP status codes.

        :default: - No custom error configuration.

        :stability: experimental
        """
        result = self._values.get("error_configurations")
        return result

    @builtins.property
    def geo_restriction(self) -> typing.Optional["GeoRestriction"]:
        """(experimental) Controls the countries in which your content is distributed.

        :default: No geo restriction

        :stability: experimental
        """
        result = self._values.get("geo_restriction")
        return result

    @builtins.property
    def http_version(self) -> typing.Optional["HttpVersion"]:
        """(experimental) The max supported HTTP Versions.

        :default: HttpVersion.HTTP2

        :stability: experimental
        """
        result = self._values.get("http_version")
        return result

    @builtins.property
    def logging_config(self) -> typing.Optional["LoggingConfiguration"]:
        """(experimental) Optional - if we should enable logging.

        You can pass an empty object ({}) to have us auto create a bucket for logging.
        Omission of this property indicates no logging is to be enabled.

        :default: - no logging is enabled by default.

        :stability: experimental
        """
        result = self._values.get("logging_config")
        return result

    @builtins.property
    def price_class(self) -> typing.Optional["PriceClass"]:
        """(experimental) The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing).

        :default: PriceClass.PRICE_CLASS_100 the cheapest option for CloudFront is picked by default.

        :stability: experimental
        """
        result = self._values.get("price_class")
        return result

    @builtins.property
    def viewer_certificate(self) -> typing.Optional["ViewerCertificate"]:
        """(experimental) Specifies whether you want viewers to use HTTP or HTTPS to request your objects, whether you're using an alternate domain name with HTTPS, and if so, if you're using AWS Certificate Manager (ACM) or a third-party certificate authority.

        :default: ViewerCertificate.fromCloudFrontDefaultCertificate()

        :see: https://aws.amazon.com/premiumsupport/knowledge-center/custom-ssl-certificate-cloudfront/
        :stability: experimental
        """
        result = self._values.get("viewer_certificate")
        return result

    @builtins.property
    def viewer_protocol_policy(self) -> typing.Optional["ViewerProtocolPolicy"]:
        """(experimental) The default viewer policy for incoming clients.

        :default: RedirectToHTTPs

        :stability: experimental
        """
        result = self._values.get("viewer_protocol_policy")
        return result

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        """(experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

        To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example
        ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``.

        To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``.

        :default: - No AWS Web Application Firewall web access control list (web ACL).

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_CreateDistribution.html#API_CreateDistribution_RequestParameters.
        :stability: experimental
        """
        result = self._values.get("web_acl_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontWebDistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.CustomOriginConfig",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "allowed_origin_ssl_versions": "allowedOriginSSLVersions",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "origin_headers": "originHeaders",
        "origin_keepalive_timeout": "originKeepaliveTimeout",
        "origin_path": "originPath",
        "origin_protocol_policy": "originProtocolPolicy",
        "origin_read_timeout": "originReadTimeout",
    },
)
class CustomOriginConfig:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        allowed_origin_ssl_versions: typing.Optional[typing.List["OriginSslPolicy"]] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        origin_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        origin_keepalive_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        origin_path: typing.Optional[builtins.str] = None,
        origin_protocol_policy: typing.Optional["OriginProtocolPolicy"] = None,
        origin_read_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(experimental) A custom origin configuration.

        :param domain_name: (experimental) The domain name of the custom origin. Should not include the path - that should be in the parent SourceConfiguration
        :param allowed_origin_ssl_versions: (experimental) The SSL versions to use when interacting with the origin. Default: OriginSslPolicy.TLS_V1_2
        :param http_port: (experimental) The origin HTTP port. Default: 80
        :param https_port: (experimental) The origin HTTPS port. Default: 443
        :param origin_headers: (experimental) Any additional headers to pass to the origin. Default: - No additional headers are passed.
        :param origin_keepalive_timeout: (experimental) The keep alive timeout when making calls in seconds. Default: Duration.seconds(5)
        :param origin_path: (experimental) The relative path to the origin root to use for sources. Default: /
        :param origin_protocol_policy: (experimental) The protocol (http or https) policy to use when interacting with the origin. Default: OriginProtocolPolicy.HttpsOnly
        :param origin_read_timeout: (experimental) The read timeout when calling the origin in seconds. Default: Duration.seconds(30)

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if allowed_origin_ssl_versions is not None:
            self._values["allowed_origin_ssl_versions"] = allowed_origin_ssl_versions
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port
        if origin_headers is not None:
            self._values["origin_headers"] = origin_headers
        if origin_keepalive_timeout is not None:
            self._values["origin_keepalive_timeout"] = origin_keepalive_timeout
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if origin_protocol_policy is not None:
            self._values["origin_protocol_policy"] = origin_protocol_policy
        if origin_read_timeout is not None:
            self._values["origin_read_timeout"] = origin_read_timeout

    @builtins.property
    def domain_name(self) -> builtins.str:
        """(experimental) The domain name of the custom origin.

        Should not include the path - that should be in the parent SourceConfiguration

        :stability: experimental
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def allowed_origin_ssl_versions(
        self,
    ) -> typing.Optional[typing.List["OriginSslPolicy"]]:
        """(experimental) The SSL versions to use when interacting with the origin.

        :default: OriginSslPolicy.TLS_V1_2

        :stability: experimental
        """
        result = self._values.get("allowed_origin_ssl_versions")
        return result

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        """(experimental) The origin HTTP port.

        :default: 80

        :stability: experimental
        """
        result = self._values.get("http_port")
        return result

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        """(experimental) The origin HTTPS port.

        :default: 443

        :stability: experimental
        """
        result = self._values.get("https_port")
        return result

    @builtins.property
    def origin_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Any additional headers to pass to the origin.

        :default: - No additional headers are passed.

        :stability: experimental
        """
        result = self._values.get("origin_headers")
        return result

    @builtins.property
    def origin_keepalive_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The keep alive timeout when making calls in seconds.

        :default: Duration.seconds(5)

        :stability: experimental
        """
        result = self._values.get("origin_keepalive_timeout")
        return result

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        """(experimental) The relative path to the origin root to use for sources.

        :default: /

        :stability: experimental
        """
        result = self._values.get("origin_path")
        return result

    @builtins.property
    def origin_protocol_policy(self) -> typing.Optional["OriginProtocolPolicy"]:
        """(experimental) The protocol (http or https) policy to use when interacting with the origin.

        :default: OriginProtocolPolicy.HttpsOnly

        :stability: experimental
        """
        result = self._values.get("origin_protocol_policy")
        return result

    @builtins.property
    def origin_read_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The read timeout when calling the origin in seconds.

        :default: Duration.seconds(30)

        :stability: experimental
        """
        result = self._values.get("origin_read_timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.DistributionAttributes",
    jsii_struct_bases=[],
    name_mapping={"distribution_id": "distributionId", "domain_name": "domainName"},
)
class DistributionAttributes:
    def __init__(
        self,
        *,
        distribution_id: builtins.str,
        domain_name: builtins.str,
    ) -> None:
        """(experimental) Attributes used to import a Distribution.

        :param distribution_id: (experimental) The distribution ID for this distribution.
        :param domain_name: (experimental) The generated domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "distribution_id": distribution_id,
            "domain_name": domain_name,
        }

    @builtins.property
    def distribution_id(self) -> builtins.str:
        """(experimental) The distribution ID for this distribution.

        :stability: experimental
        :attribute: true
        """
        result = self._values.get("distribution_id")
        assert result is not None, "Required property 'distribution_id' is missing"
        return result

    @builtins.property
    def domain_name(self) -> builtins.str:
        """(experimental) The generated domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        :attribute: true
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistributionAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.DistributionProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_behavior": "defaultBehavior",
        "additional_behaviors": "additionalBehaviors",
        "certificate": "certificate",
        "comment": "comment",
        "default_root_object": "defaultRootObject",
        "domain_names": "domainNames",
        "enabled": "enabled",
        "enable_ipv6": "enableIpv6",
        "enable_logging": "enableLogging",
        "error_responses": "errorResponses",
        "geo_restriction": "geoRestriction",
        "http_version": "httpVersion",
        "log_bucket": "logBucket",
        "log_file_prefix": "logFilePrefix",
        "log_includes_cookies": "logIncludesCookies",
        "price_class": "priceClass",
        "web_acl_id": "webAclId",
    },
)
class DistributionProps:
    def __init__(
        self,
        *,
        default_behavior: BehaviorOptions,
        additional_behaviors: typing.Optional[typing.Mapping[builtins.str, BehaviorOptions]] = None,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.List[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_responses: typing.Optional[typing.List["ErrorResponse"]] = None,
        geo_restriction: typing.Optional["GeoRestriction"] = None,
        http_version: typing.Optional["HttpVersion"] = None,
        log_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        price_class: typing.Optional["PriceClass"] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties for a Distribution.

        :param default_behavior: (experimental) The default behavior for the distribution.
        :param additional_behaviors: (experimental) Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to. Default: - no additional behaviors are added.
        :param certificate: (experimental) A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param comment: (experimental) Any comments you want to include about the distribution. Default: - no comment
        :param default_root_object: (experimental) The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/). Default: - no default root object
        :param domain_names: (experimental) Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you must add (at least one of) the domain names of the certificate to this list. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        :param enabled: (experimental) Enable or disable the distribution. Default: true
        :param enable_ipv6: (experimental) Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address. If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second request, for an IPv4 address for your distribution. Default: true
        :param enable_logging: (experimental) Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param error_responses: (experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: (experimental) Controls the countries in which your content is distributed. Default: - No geographic restrictions
        :param http_version: (experimental) Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront. For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI). Default: HttpVersion.HTTP2
        :param log_bucket: (experimental) The Amazon S3 bucket to store the access logs in. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: (experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: (experimental) Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param price_class: (experimental) The price class that corresponds with the maximum price that you want to pay for CloudFront service. If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations. If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location that has the lowest latency among the edge locations in your price class. Default: PriceClass.PRICE_CLASS_ALL
        :param web_acl_id: (experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).

        :stability: experimental
        """
        if isinstance(default_behavior, dict):
            default_behavior = BehaviorOptions(**default_behavior)
        self._values: typing.Dict[str, typing.Any] = {
            "default_behavior": default_behavior,
        }
        if additional_behaviors is not None:
            self._values["additional_behaviors"] = additional_behaviors
        if certificate is not None:
            self._values["certificate"] = certificate
        if comment is not None:
            self._values["comment"] = comment
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if error_responses is not None:
            self._values["error_responses"] = error_responses
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if http_version is not None:
            self._values["http_version"] = http_version
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_file_prefix is not None:
            self._values["log_file_prefix"] = log_file_prefix
        if log_includes_cookies is not None:
            self._values["log_includes_cookies"] = log_includes_cookies
        if price_class is not None:
            self._values["price_class"] = price_class
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def default_behavior(self) -> BehaviorOptions:
        """(experimental) The default behavior for the distribution.

        :stability: experimental
        """
        result = self._values.get("default_behavior")
        assert result is not None, "Required property 'default_behavior' is missing"
        return result

    @builtins.property
    def additional_behaviors(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, BehaviorOptions]]:
        """(experimental) Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to.

        :default: - no additional behaviors are added.

        :stability: experimental
        """
        result = self._values.get("additional_behaviors")
        return result

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """(experimental) A certificate to associate with the distribution.

        The certificate must be located in N. Virginia (us-east-1).

        :default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.

        :stability: experimental
        """
        result = self._values.get("certificate")
        return result

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """(experimental) Any comments you want to include about the distribution.

        :default: - no comment

        :stability: experimental
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        """(experimental) The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/).

        :default: - no default root object

        :stability: experimental
        """
        result = self._values.get("default_root_object")
        return result

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Alternative domain names for this distribution.

        If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name,
        you can add an alternate domain name to your distribution. If you attach a certificate to the distribution,
        you must add (at least one of) the domain names of the certificate to this list.

        :default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)

        :stability: experimental
        """
        result = self._values.get("domain_names")
        return result

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        """(experimental) Enable or disable the distribution.

        :default: true

        :stability: experimental
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def enable_ipv6(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address.

        If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses.
        This allows viewers to submit a second request, for an IPv4 address for your distribution.

        :default: true

        :stability: experimental
        """
        result = self._values.get("enable_ipv6")
        return result

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        """(experimental) Enable access logging for the distribution.

        :default: - false, unless ``logBucket`` is specified.

        :stability: experimental
        """
        result = self._values.get("enable_logging")
        return result

    @builtins.property
    def error_responses(self) -> typing.Optional[typing.List["ErrorResponse"]]:
        """(experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound).

        :default: - No custom error responses.

        :stability: experimental
        """
        result = self._values.get("error_responses")
        return result

    @builtins.property
    def geo_restriction(self) -> typing.Optional["GeoRestriction"]:
        """(experimental) Controls the countries in which your content is distributed.

        :default: - No geographic restrictions

        :stability: experimental
        """
        result = self._values.get("geo_restriction")
        return result

    @builtins.property
    def http_version(self) -> typing.Optional["HttpVersion"]:
        """(experimental) Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront.

        For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI).

        :default: HttpVersion.HTTP2

        :stability: experimental
        """
        result = self._values.get("http_version")
        return result

    @builtins.property
    def log_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """(experimental) The Amazon S3 bucket to store the access logs in.

        :default: - A bucket is created if ``enableLogging`` is true

        :stability: experimental
        """
        result = self._values.get("log_bucket")
        return result

    @builtins.property
    def log_file_prefix(self) -> typing.Optional[builtins.str]:
        """(experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution.

        :default: - no prefix

        :stability: experimental
        """
        result = self._values.get("log_file_prefix")
        return result

    @builtins.property
    def log_includes_cookies(self) -> typing.Optional[builtins.bool]:
        """(experimental) Specifies whether you want CloudFront to include cookies in access logs.

        :default: false

        :stability: experimental
        """
        result = self._values.get("log_includes_cookies")
        return result

    @builtins.property
    def price_class(self) -> typing.Optional["PriceClass"]:
        """(experimental) The price class that corresponds with the maximum price that you want to pay for CloudFront service.

        If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations.
        If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location
        that has the lowest latency among the edge locations in your price class.

        :default: PriceClass.PRICE_CLASS_ALL

        :stability: experimental
        """
        result = self._values.get("price_class")
        return result

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        """(experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

        To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example
        ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``.
        To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``.

        :default: - No AWS Web Application Firewall web access control list (web ACL).

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_CreateDistribution.html#API_CreateDistribution_RequestParameters.
        :stability: experimental
        """
        result = self._values.get("web_acl_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.EdgeLambda",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "function_version": "functionVersion",
        "include_body": "includeBody",
    },
)
class EdgeLambda:
    def __init__(
        self,
        *,
        event_type: "LambdaEdgeEventType",
        function_version: aws_cdk.aws_lambda.IVersion,
        include_body: typing.Optional[builtins.bool] = None,
    ) -> None:
        """(experimental) Represents a Lambda function version and event type when using Lambda@Edge.

        The type of the {@link AddBehaviorOptions.edgeLambdas} property.

        :param event_type: (experimental) The type of event in response to which should the function be invoked.
        :param function_version: (experimental) The version of the Lambda function that will be invoked. **Note**: it's not possible to use the '$LATEST' function version for Lambda@Edge!
        :param include_body: (experimental) Allows a Lambda function to have read access to the body content. Only valid for "request" event types (``ORIGIN_REQUEST`` or ``VIEWER_REQUEST``). See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-include-body-access.html Default: false

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "event_type": event_type,
            "function_version": function_version,
        }
        if include_body is not None:
            self._values["include_body"] = include_body

    @builtins.property
    def event_type(self) -> "LambdaEdgeEventType":
        """(experimental) The type of event in response to which should the function be invoked.

        :stability: experimental
        """
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return result

    @builtins.property
    def function_version(self) -> aws_cdk.aws_lambda.IVersion:
        """(experimental) The version of the Lambda function that will be invoked.

        **Note**: it's not possible to use the '$LATEST' function version for Lambda@Edge!

        :stability: experimental
        """
        result = self._values.get("function_version")
        assert result is not None, "Required property 'function_version' is missing"
        return result

    @builtins.property
    def include_body(self) -> typing.Optional[builtins.bool]:
        """(experimental) Allows a Lambda function to have read access to the body content.

        Only valid for "request" event types (``ORIGIN_REQUEST`` or ``VIEWER_REQUEST``).
        See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-include-body-access.html

        :default: false

        :stability: experimental
        """
        result = self._values.get("include_body")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgeLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.ErrorResponse",
    jsii_struct_bases=[],
    name_mapping={
        "http_status": "httpStatus",
        "response_http_status": "responseHttpStatus",
        "response_page_path": "responsePagePath",
        "ttl": "ttl",
    },
)
class ErrorResponse:
    def __init__(
        self,
        *,
        http_status: jsii.Number,
        response_http_status: typing.Optional[jsii.Number] = None,
        response_page_path: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(experimental) Options for configuring custom error responses.

        :param http_status: (experimental) The HTTP status code for which you want to specify a custom error page and/or a caching duration.
        :param response_http_status: (experimental) The HTTP status code that you want CloudFront to return to the viewer along with the custom error page. If you specify a value for ``responseHttpStatus``, you must also specify a value for ``responsePagePath``. Default: - not set, the error code will be returned as the response code.
        :param response_page_path: (experimental) The path to the custom error page that you want CloudFront to return to a viewer when your origin returns the ``httpStatus``, for example, /4xx-errors/403-forbidden.html. Default: - the default CloudFront response is shown.
        :param ttl: (experimental) The minimum amount of time, in seconds, that you want CloudFront to cache the HTTP status code specified in ErrorCode. Default: - the default caching TTL behavior applies

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "http_status": http_status,
        }
        if response_http_status is not None:
            self._values["response_http_status"] = response_http_status
        if response_page_path is not None:
            self._values["response_page_path"] = response_page_path
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def http_status(self) -> jsii.Number:
        """(experimental) The HTTP status code for which you want to specify a custom error page and/or a caching duration.

        :stability: experimental
        """
        result = self._values.get("http_status")
        assert result is not None, "Required property 'http_status' is missing"
        return result

    @builtins.property
    def response_http_status(self) -> typing.Optional[jsii.Number]:
        """(experimental) The HTTP status code that you want CloudFront to return to the viewer along with the custom error page.

        If you specify a value for ``responseHttpStatus``, you must also specify a value for ``responsePagePath``.

        :default: - not set, the error code will be returned as the response code.

        :stability: experimental
        """
        result = self._values.get("response_http_status")
        return result

    @builtins.property
    def response_page_path(self) -> typing.Optional[builtins.str]:
        """(experimental) The path to the custom error page that you want CloudFront to return to a viewer when your origin returns the ``httpStatus``, for example, /4xx-errors/403-forbidden.html.

        :default: - the default CloudFront response is shown.

        :stability: experimental
        """
        result = self._values.get("response_page_path")
        return result

    @builtins.property
    def ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The minimum amount of time, in seconds, that you want CloudFront to cache the HTTP status code specified in ErrorCode.

        :default: - the default caching TTL behavior applies

        :stability: experimental
        """
        result = self._values.get("ttl")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ErrorResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.FailoverStatusCode")
class FailoverStatusCode(enum.Enum):
    """(experimental) HTTP status code to failover to second origin.

    :stability: experimental
    """

    FORBIDDEN = "FORBIDDEN"
    """(experimental) Forbidden (403).

    :stability: experimental
    """
    NOT_FOUND = "NOT_FOUND"
    """(experimental) Not found (404).

    :stability: experimental
    """
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    """(experimental) Internal Server Error (500).

    :stability: experimental
    """
    BAD_GATEWAY = "BAD_GATEWAY"
    """(experimental) Bad Gateway (502).

    :stability: experimental
    """
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    """(experimental) Service Unavailable (503).

    :stability: experimental
    """
    GATEWAY_TIMEOUT = "GATEWAY_TIMEOUT"
    """(experimental) Gateway Timeout (504).

    :stability: experimental
    """


class GeoRestriction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.GeoRestriction",
):
    """(experimental) Controls the countries in which content is distributed.

    :stability: experimental
    """

    @jsii.member(jsii_name="blacklist")
    @builtins.classmethod
    def blacklist(cls, *locations: builtins.str) -> "GeoRestriction":
        """(experimental) Blacklist specific countries which you don't want CloudFront to distribute your content.

        :param locations: Two-letter, uppercase country code for a country that you want to blacklist. Include one element for each country. See ISO 3166-1-alpha-2 code on the *International Organization for Standardization* website

        :stability: experimental
        """
        return jsii.sinvoke(cls, "blacklist", [*locations])

    @jsii.member(jsii_name="whitelist")
    @builtins.classmethod
    def whitelist(cls, *locations: builtins.str) -> "GeoRestriction":
        """(experimental) Whitelist specific countries which you want CloudFront to distribute your content.

        :param locations: Two-letter, uppercase country code for a country that you want to whitelist. Include one element for each country. See ISO 3166-1-alpha-2 code on the *International Organization for Standardization* website

        :stability: experimental
        """
        return jsii.sinvoke(cls, "whitelist", [*locations])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        """(experimental) Two-letter, uppercase country code for a country that you want to whitelist/blacklist.

        Include one element for each country.
        See ISO 3166-1-alpha-2 code on the *International Organization for Standardization* website

        :stability: experimental
        """
        return jsii.get(self, "locations")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="restrictionType")
    def restriction_type(self) -> builtins.str:
        """(experimental) Specifies the restriction type to impose (whitelist or blacklist).

        :stability: experimental
        """
        return jsii.get(self, "restrictionType")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.HttpVersion")
class HttpVersion(enum.Enum):
    """(experimental) Maximum HTTP version to support.

    :stability: experimental
    """

    HTTP1_1 = "HTTP1_1"
    """(experimental) HTTP 1.1.

    :stability: experimental
    """
    HTTP2 = "HTTP2"
    """(experimental) HTTP 2.

    :stability: experimental
    """


@jsii.interface(jsii_type="@aws-cdk/aws-cloudfront.ICachePolicy")
class ICachePolicy(typing_extensions.Protocol):
    """(experimental) Represents a Cache Policy.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICachePolicyProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cachePolicyId")
    def cache_policy_id(self) -> builtins.str:
        """(experimental) The ID of the cache policy.

        :stability: experimental
        :attribute: true
        """
        ...


class _ICachePolicyProxy:
    """(experimental) Represents a Cache Policy.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudfront.ICachePolicy"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cachePolicyId")
    def cache_policy_id(self) -> builtins.str:
        """(experimental) The ID of the cache policy.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "cachePolicyId")


@jsii.interface(jsii_type="@aws-cdk/aws-cloudfront.IDistribution")
class IDistribution(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Interface for CloudFront distributions.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDistributionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        """(experimental) The domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        """(experimental) The distribution ID for this distribution.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """(deprecated) The domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :deprecated: - Use ``distributionDomainName`` instead.

        :stability: deprecated
        :attribute: true
        """
        ...


class _IDistributionProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Interface for CloudFront distributions.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudfront.IDistribution"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        """(experimental) The domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "distributionDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        """(experimental) The distribution ID for this distribution.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "distributionId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """(deprecated) The domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :deprecated: - Use ``distributionDomainName`` instead.

        :stability: deprecated
        :attribute: true
        """
        return jsii.get(self, "domainName")


@jsii.interface(jsii_type="@aws-cdk/aws-cloudfront.IOrigin")
class IOrigin(typing_extensions.Protocol):
    """(experimental) Represents the concept of a CloudFront Origin.

    You provide one or more origins when creating a Distribution.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IOriginProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        *,
        origin_id: builtins.str,
    ) -> "OriginBindConfig":
        """(experimental) The method called when a given Origin is added (for the first time) to a Distribution.

        :param scope: -
        :param origin_id: (experimental) The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        :stability: experimental
        """
        ...


class _IOriginProxy:
    """(experimental) Represents the concept of a CloudFront Origin.

    You provide one or more origins when creating a Distribution.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudfront.IOrigin"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        *,
        origin_id: builtins.str,
    ) -> "OriginBindConfig":
        """(experimental) The method called when a given Origin is added (for the first time) to a Distribution.

        :param scope: -
        :param origin_id: (experimental) The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        :stability: experimental
        """
        options = OriginBindOptions(origin_id=origin_id)

        return jsii.invoke(self, "bind", [scope, options])


@jsii.interface(jsii_type="@aws-cdk/aws-cloudfront.IOriginAccessIdentity")
class IOriginAccessIdentity(
    aws_cdk.core.IResource,
    aws_cdk.aws_iam.IGrantable,
    typing_extensions.Protocol,
):
    """(experimental) Interface for CloudFront OriginAccessIdentity.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IOriginAccessIdentityProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="originAccessIdentityName")
    def origin_access_identity_name(self) -> builtins.str:
        """(experimental) The Origin Access Identity Name.

        :stability: experimental
        """
        ...


class _IOriginAccessIdentityProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore
    jsii.proxy_for(aws_cdk.aws_iam.IGrantable), # type: ignore
):
    """(experimental) Interface for CloudFront OriginAccessIdentity.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudfront.IOriginAccessIdentity"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="originAccessIdentityName")
    def origin_access_identity_name(self) -> builtins.str:
        """(experimental) The Origin Access Identity Name.

        :stability: experimental
        """
        return jsii.get(self, "originAccessIdentityName")


@jsii.interface(jsii_type="@aws-cdk/aws-cloudfront.IOriginRequestPolicy")
class IOriginRequestPolicy(typing_extensions.Protocol):
    """(experimental) Represents a Origin Request Policy.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IOriginRequestPolicyProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="originRequestPolicyId")
    def origin_request_policy_id(self) -> builtins.str:
        """(experimental) The ID of the origin request policy.

        :stability: experimental
        :attribute: true
        """
        ...


class _IOriginRequestPolicyProxy:
    """(experimental) Represents a Origin Request Policy.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloudfront.IOriginRequestPolicy"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="originRequestPolicyId")
    def origin_request_policy_id(self) -> builtins.str:
        """(experimental) The ID of the origin request policy.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "originRequestPolicyId")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.LambdaEdgeEventType")
class LambdaEdgeEventType(enum.Enum):
    """(experimental) The type of events that a Lambda@Edge function can be invoked in response to.

    :stability: experimental
    """

    ORIGIN_REQUEST = "ORIGIN_REQUEST"
    """(experimental) The origin-request specifies the request to the origin location (e.g. S3).

    :stability: experimental
    """
    ORIGIN_RESPONSE = "ORIGIN_RESPONSE"
    """(experimental) The origin-response specifies the response from the origin location (e.g. S3).

    :stability: experimental
    """
    VIEWER_REQUEST = "VIEWER_REQUEST"
    """(experimental) The viewer-request specifies the incoming request.

    :stability: experimental
    """
    VIEWER_RESPONSE = "VIEWER_RESPONSE"
    """(experimental) The viewer-response specifies the outgoing reponse.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.LambdaFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "lambda_function": "lambdaFunction",
        "include_body": "includeBody",
    },
)
class LambdaFunctionAssociation:
    def __init__(
        self,
        *,
        event_type: LambdaEdgeEventType,
        lambda_function: aws_cdk.aws_lambda.IVersion,
        include_body: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param event_type: (experimental) The lambda event type defines at which event the lambda is called during the request lifecycle.
        :param lambda_function: (experimental) A version of the lambda to associate.
        :param include_body: (experimental) Allows a Lambda function to have read access to the body content. Only valid for "request" event types (``ORIGIN_REQUEST`` or ``VIEWER_REQUEST``). See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-include-body-access.html Default: false

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "event_type": event_type,
            "lambda_function": lambda_function,
        }
        if include_body is not None:
            self._values["include_body"] = include_body

    @builtins.property
    def event_type(self) -> LambdaEdgeEventType:
        """(experimental) The lambda event type defines at which event the lambda is called during the request lifecycle.

        :stability: experimental
        """
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return result

    @builtins.property
    def lambda_function(self) -> aws_cdk.aws_lambda.IVersion:
        """(experimental) A version of the lambda to associate.

        :stability: experimental
        """
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return result

    @builtins.property
    def include_body(self) -> typing.Optional[builtins.bool]:
        """(experimental) Allows a Lambda function to have read access to the body content.

        Only valid for "request" event types (``ORIGIN_REQUEST`` or ``VIEWER_REQUEST``).
        See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-include-body-access.html

        :default: false

        :stability: experimental
        """
        result = self._values.get("include_body")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.LoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "include_cookies": "includeCookies",
        "prefix": "prefix",
    },
)
class LoggingConfiguration:
    def __init__(
        self,
        *,
        bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        include_cookies: typing.Optional[builtins.bool] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Logging configuration for incoming requests.

        :param bucket: (experimental) Bucket to log requests to. Default: - A logging bucket is automatically created.
        :param include_cookies: (experimental) Whether to include the cookies in the logs. Default: false
        :param prefix: (experimental) Where in the bucket to store logs. Default: - No prefix.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if include_cookies is not None:
            self._values["include_cookies"] = include_cookies
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """(experimental) Bucket to log requests to.

        :default: - A logging bucket is automatically created.

        :stability: experimental
        """
        result = self._values.get("bucket")
        return result

    @builtins.property
    def include_cookies(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to include the cookies in the logs.

        :default: false

        :stability: experimental
        """
        result = self._values.get("include_cookies")
        return result

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        """(experimental) Where in the bucket to store logs.

        :default: - No prefix.

        :stability: experimental
        """
        result = self._values.get("prefix")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IOriginAccessIdentity)
class OriginAccessIdentity(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.OriginAccessIdentity",
):
    """(experimental) An origin access identity is a special CloudFront user that you can associate with Amazon S3 origins, so that you can secure all or just some of your Amazon S3 content.

    :stability: experimental
    :resource: AWS::CloudFront::CloudFrontOriginAccessIdentity
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: (experimental) Any comments you want to include about the origin access identity. Default: "Allows CloudFront to reach the bucket"

        :stability: experimental
        """
        props = OriginAccessIdentityProps(comment=comment)

        jsii.create(OriginAccessIdentity, self, [scope, id, props])

    @jsii.member(jsii_name="fromOriginAccessIdentityName")
    @builtins.classmethod
    def from_origin_access_identity_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        origin_access_identity_name: builtins.str,
    ) -> IOriginAccessIdentity:
        """(experimental) Creates a OriginAccessIdentity by providing the OriginAccessIdentityName.

        :param scope: -
        :param id: -
        :param origin_access_identity_name: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromOriginAccessIdentityName", [scope, id, origin_access_identity_name])

    @jsii.member(jsii_name="arn")
    def _arn(self) -> builtins.str:
        """(experimental) The ARN to include in S3 bucket policy to allow CloudFront access.

        :stability: experimental
        """
        return jsii.invoke(self, "arn", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cloudFrontOriginAccessIdentityS3CanonicalUserId")
    def cloud_front_origin_access_identity_s3_canonical_user_id(self) -> builtins.str:
        """(experimental) The Amazon S3 canonical user ID for the origin access identity, used when giving the origin access identity read permission to an object in Amazon S3.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "cloudFrontOriginAccessIdentityS3CanonicalUserId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """(experimental) Derived principal value for bucket access.

        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="originAccessIdentityName")
    def origin_access_identity_name(self) -> builtins.str:
        """(experimental) The Origin Access Identity Name (physical id).

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "originAccessIdentityName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.OriginAccessIdentityProps",
    jsii_struct_bases=[],
    name_mapping={"comment": "comment"},
)
class OriginAccessIdentityProps:
    def __init__(self, *, comment: typing.Optional[builtins.str] = None) -> None:
        """(experimental) Properties of CloudFront OriginAccessIdentity.

        :param comment: (experimental) Any comments you want to include about the origin access identity. Default: "Allows CloudFront to reach the bucket"

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """(experimental) Any comments you want to include about the origin access identity.

        :default: "Allows CloudFront to reach the bucket"

        :stability: experimental
        """
        result = self._values.get("comment")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginAccessIdentityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IOrigin)
class OriginBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-cloudfront.OriginBase",
):
    """(experimental) Represents a distribution origin, that describes the Amazon S3 bucket, HTTP server (for example, a web server), Amazon MediaStore, or other server from which CloudFront gets your files.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _OriginBaseProxy

    def __init__(
        self,
        domain_name: builtins.str,
        *,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        custom_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        origin_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param domain_name: -
        :param connection_attempts: (experimental) The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: (experimental) The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: (experimental) A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: (experimental) An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        :stability: experimental
        """
        props = OriginProps(
            connection_attempts=connection_attempts,
            connection_timeout=connection_timeout,
            custom_headers=custom_headers,
            origin_path=origin_path,
        )

        jsii.create(OriginBase, self, [domain_name, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: aws_cdk.core.Construct,
        *,
        origin_id: builtins.str,
    ) -> "OriginBindConfig":
        """(experimental) Binds the origin to the associated Distribution.

        Can be used to grant permissions, create dependent resources, etc.

        :param _scope: -
        :param origin_id: (experimental) The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        :stability: experimental
        """
        options = OriginBindOptions(origin_id=origin_id)

        return jsii.invoke(self, "bind", [_scope, options])

    @jsii.member(jsii_name="renderCustomOriginConfig")
    def _render_custom_origin_config(
        self,
    ) -> typing.Optional[CfnDistribution.CustomOriginConfigProperty]:
        """
        :stability: experimental
        """
        return jsii.invoke(self, "renderCustomOriginConfig", [])

    @jsii.member(jsii_name="renderS3OriginConfig")
    def _render_s3_origin_config(
        self,
    ) -> typing.Optional[CfnDistribution.S3OriginConfigProperty]:
        """
        :stability: experimental
        """
        return jsii.invoke(self, "renderS3OriginConfig", [])


class _OriginBaseProxy(OriginBase):
    pass


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.OriginBindConfig",
    jsii_struct_bases=[],
    name_mapping={
        "failover_config": "failoverConfig",
        "origin_property": "originProperty",
    },
)
class OriginBindConfig:
    def __init__(
        self,
        *,
        failover_config: typing.Optional["OriginFailoverConfig"] = None,
        origin_property: typing.Optional[CfnDistribution.OriginProperty] = None,
    ) -> None:
        """(experimental) The struct returned from {@link IOrigin.bind}.

        :param failover_config: (experimental) The failover configuration for this Origin. Default: - nothing is returned
        :param origin_property: (experimental) The CloudFormation OriginProperty configuration for this Origin. Default: - nothing is returned

        :stability: experimental
        """
        if isinstance(failover_config, dict):
            failover_config = OriginFailoverConfig(**failover_config)
        if isinstance(origin_property, dict):
            origin_property = CfnDistribution.OriginProperty(**origin_property)
        self._values: typing.Dict[str, typing.Any] = {}
        if failover_config is not None:
            self._values["failover_config"] = failover_config
        if origin_property is not None:
            self._values["origin_property"] = origin_property

    @builtins.property
    def failover_config(self) -> typing.Optional["OriginFailoverConfig"]:
        """(experimental) The failover configuration for this Origin.

        :default: - nothing is returned

        :stability: experimental
        """
        result = self._values.get("failover_config")
        return result

    @builtins.property
    def origin_property(self) -> typing.Optional[CfnDistribution.OriginProperty]:
        """(experimental) The CloudFormation OriginProperty configuration for this Origin.

        :default: - nothing is returned

        :stability: experimental
        """
        result = self._values.get("origin_property")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginBindConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.OriginBindOptions",
    jsii_struct_bases=[],
    name_mapping={"origin_id": "originId"},
)
class OriginBindOptions:
    def __init__(self, *, origin_id: builtins.str) -> None:
        """(experimental) Options passed to Origin.bind().

        :param origin_id: (experimental) The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "origin_id": origin_id,
        }

    @builtins.property
    def origin_id(self) -> builtins.str:
        """(experimental) The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        :stability: experimental
        """
        result = self._values.get("origin_id")
        assert result is not None, "Required property 'origin_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.OriginFailoverConfig",
    jsii_struct_bases=[],
    name_mapping={"failover_origin": "failoverOrigin", "status_codes": "statusCodes"},
)
class OriginFailoverConfig:
    def __init__(
        self,
        *,
        failover_origin: IOrigin,
        status_codes: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> None:
        """(experimental) The failover configuration used for Origin Groups, returned in {@link OriginBindConfig.failoverConfig}.

        :param failover_origin: (experimental) The origin to use as the fallback origin.
        :param status_codes: (experimental) The HTTP status codes of the response that trigger querying the failover Origin. Default: - 500, 502, 503 and 504

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "failover_origin": failover_origin,
        }
        if status_codes is not None:
            self._values["status_codes"] = status_codes

    @builtins.property
    def failover_origin(self) -> IOrigin:
        """(experimental) The origin to use as the fallback origin.

        :stability: experimental
        """
        result = self._values.get("failover_origin")
        assert result is not None, "Required property 'failover_origin' is missing"
        return result

    @builtins.property
    def status_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        """(experimental) The HTTP status codes of the response that trigger querying the failover Origin.

        :default: - 500, 502, 503 and 504

        :stability: experimental
        """
        result = self._values.get("status_codes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginFailoverConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.OriginProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_headers": "customHeaders",
        "origin_path": "originPath",
    },
)
class OriginProps:
    def __init__(
        self,
        *,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        custom_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        origin_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties to define an Origin.

        :param connection_attempts: (experimental) The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: (experimental) The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: (experimental) A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: (experimental) An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if connection_attempts is not None:
            self._values["connection_attempts"] = connection_attempts
        if connection_timeout is not None:
            self._values["connection_timeout"] = connection_timeout
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if origin_path is not None:
            self._values["origin_path"] = origin_path

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        """(experimental) The number of times that CloudFront attempts to connect to the origin;

        valid values are 1, 2, or 3 attempts.

        :default: 3

        :stability: experimental
        """
        result = self._values.get("connection_attempts")
        return result

    @builtins.property
    def connection_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The number of seconds that CloudFront waits when trying to establish a connection to the origin.

        Valid values are 1-10 seconds, inclusive.

        :default: Duration.seconds(10)

        :stability: experimental
        """
        result = self._values.get("connection_timeout")
        return result

    @builtins.property
    def custom_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) A list of HTTP header names and values that CloudFront adds to requests it sends to the origin.

        :default: {}

        :stability: experimental
        """
        result = self._values.get("custom_headers")
        return result

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        """(experimental) An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.

        Must begin, but not end, with '/' (e.g., '/production/images').

        :default: '/'

        :stability: experimental
        """
        result = self._values.get("origin_path")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginProtocolPolicy")
class OriginProtocolPolicy(enum.Enum):
    """(experimental) Defines what protocols CloudFront will use to connect to an origin.

    :stability: experimental
    """

    HTTP_ONLY = "HTTP_ONLY"
    """(experimental) Connect on HTTP only.

    :stability: experimental
    """
    MATCH_VIEWER = "MATCH_VIEWER"
    """(experimental) Connect with the same protocol as the viewer.

    :stability: experimental
    """
    HTTPS_ONLY = "HTTPS_ONLY"
    """(experimental) Connect on HTTPS only.

    :stability: experimental
    """


class OriginRequestCookieBehavior(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.OriginRequestCookieBehavior",
):
    """(experimental) Ddetermines whether any cookies in viewer requests (and if so, which cookies) are included in requests that CloudFront sends to the origin.

    :stability: experimental
    """

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "OriginRequestCookieBehavior":
        """(experimental) All cookies in viewer requests are included in requests that CloudFront sends to the origin.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "all", [])

    @jsii.member(jsii_name="allowList")
    @builtins.classmethod
    def allow_list(cls, *cookies: builtins.str) -> "OriginRequestCookieBehavior":
        """(experimental) Only the provided ``cookies`` are included in requests that CloudFront sends to the origin.

        :param cookies: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "allowList", [*cookies])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "OriginRequestCookieBehavior":
        """(experimental) Cookies in viewer requests are not included in requests that CloudFront sends to the origin.

        Any cookies that are listed in a CachePolicy are still included in origin requests.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "none", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        """(experimental) The behavior of cookies: allow all, none or an allow list.

        :stability: experimental
        """
        return jsii.get(self, "behavior")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cookies")
    def cookies(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The cookies to allow, if the behavior is an allow list.

        :stability: experimental
        """
        return jsii.get(self, "cookies")


class OriginRequestHeaderBehavior(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.OriginRequestHeaderBehavior",
):
    """(experimental) Determines whether any HTTP headers (and if so, which headers) are included in requests that CloudFront sends to the origin.

    :stability: experimental
    """

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls, *cloudfront_headers: builtins.str) -> "OriginRequestHeaderBehavior":
        """(experimental) All HTTP headers in viewer requests are included in requests that CloudFront sends to the origin.

        Additionally, any additional CloudFront headers provided are included; the additional headers are added by CloudFront.

        :param cloudfront_headers: -

        :see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-cloudfront-headers.html
        :stability: experimental
        """
        return jsii.sinvoke(cls, "all", [*cloudfront_headers])

    @jsii.member(jsii_name="allowList")
    @builtins.classmethod
    def allow_list(cls, *headers: builtins.str) -> "OriginRequestHeaderBehavior":
        """(experimental) Listed headers are included in requests that CloudFront sends to the origin.

        :param headers: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "allowList", [*headers])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "OriginRequestHeaderBehavior":
        """(experimental) HTTP headers are not included in requests that CloudFront sends to the origin.

        Any headers that are listed in a CachePolicy are still included in origin requests.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "none", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        """(experimental) The behavior of headers: allow all, none or an allow list.

        :stability: experimental
        """
        return jsii.get(self, "behavior")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The headers for the allow list or the included CloudFront headers, if applicable.

        :stability: experimental
        """
        return jsii.get(self, "headers")


@jsii.implements(IOriginRequestPolicy)
class OriginRequestPolicy(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.OriginRequestPolicy",
):
    """(experimental) A Origin Request Policy configuration.

    :stability: experimental
    :resource: AWS::CloudFront::OriginRequestPolicy
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        cookie_behavior: typing.Optional[OriginRequestCookieBehavior] = None,
        header_behavior: typing.Optional[OriginRequestHeaderBehavior] = None,
        origin_request_policy_name: typing.Optional[builtins.str] = None,
        query_string_behavior: typing.Optional["OriginRequestQueryStringBehavior"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param comment: (experimental) A comment to describe the origin request policy. Default: - no comment
        :param cookie_behavior: (experimental) The cookies from viewer requests to include in origin requests. Default: OriginRequestCookieBehavior.none()
        :param header_behavior: (experimental) The HTTP headers to include in origin requests. These can include headers from viewer requests and additional headers added by CloudFront. Default: OriginRequestHeaderBehavior.none()
        :param origin_request_policy_name: (experimental) A unique name to identify the origin request policy. The name must only include '-', '_', or alphanumeric characters. Default: - generated from the ``id``
        :param query_string_behavior: (experimental) The URL query strings from viewer requests to include in origin requests. Default: OriginRequestQueryStringBehavior.none()

        :stability: experimental
        """
        props = OriginRequestPolicyProps(
            comment=comment,
            cookie_behavior=cookie_behavior,
            header_behavior=header_behavior,
            origin_request_policy_name=origin_request_policy_name,
            query_string_behavior=query_string_behavior,
        )

        jsii.create(OriginRequestPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="fromOriginRequestPolicyId")
    @builtins.classmethod
    def from_origin_request_policy_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        origin_request_policy_id: builtins.str,
    ) -> IOriginRequestPolicy:
        """(experimental) Imports a Origin Request Policy from its id.

        :param scope: -
        :param id: -
        :param origin_request_policy_id: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromOriginRequestPolicyId", [scope, id, origin_request_policy_id])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ALL_VIEWER")
    def ALL_VIEWER(cls) -> IOriginRequestPolicy:
        """(experimental) This policy includes all values (query strings, headers, and cookies) in the viewer request.

        :stability: experimental
        """
        return jsii.sget(cls, "ALL_VIEWER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CORS_CUSTOM_ORIGIN")
    def CORS_CUSTOM_ORIGIN(cls) -> IOriginRequestPolicy:
        """(experimental) This policy includes the header that enables cross-origin resource sharing (CORS) requests when the origin is a custom origin.

        :stability: experimental
        """
        return jsii.sget(cls, "CORS_CUSTOM_ORIGIN")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CORS_S3_ORIGIN")
    def CORS_S3_ORIGIN(cls) -> IOriginRequestPolicy:
        """(experimental) This policy includes the headers that enable cross-origin resource sharing (CORS) requests when the origin is an Amazon S3 bucket.

        :stability: experimental
        """
        return jsii.sget(cls, "CORS_S3_ORIGIN")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ELEMENTAL_MEDIA_TAILOR")
    def ELEMENTAL_MEDIA_TAILOR(cls) -> IOriginRequestPolicy:
        """(experimental) This policy is designed for use with an origin that is an AWS Elemental MediaTailor endpoint.

        :stability: experimental
        """
        return jsii.sget(cls, "ELEMENTAL_MEDIA_TAILOR")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="USER_AGENT_REFERER_HEADERS")
    def USER_AGENT_REFERER_HEADERS(cls) -> IOriginRequestPolicy:
        """(experimental) This policy includes only the User-Agent and Referer headers.

        It doesn’t include any query strings or cookies.

        :stability: experimental
        """
        return jsii.sget(cls, "USER_AGENT_REFERER_HEADERS")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="originRequestPolicyId")
    def origin_request_policy_id(self) -> builtins.str:
        """(experimental) The ID of the origin request policy.

        :stability: experimental
        """
        return jsii.get(self, "originRequestPolicyId")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.OriginRequestPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "cookie_behavior": "cookieBehavior",
        "header_behavior": "headerBehavior",
        "origin_request_policy_name": "originRequestPolicyName",
        "query_string_behavior": "queryStringBehavior",
    },
)
class OriginRequestPolicyProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        cookie_behavior: typing.Optional[OriginRequestCookieBehavior] = None,
        header_behavior: typing.Optional[OriginRequestHeaderBehavior] = None,
        origin_request_policy_name: typing.Optional[builtins.str] = None,
        query_string_behavior: typing.Optional["OriginRequestQueryStringBehavior"] = None,
    ) -> None:
        """(experimental) Properties for creating a Origin Request Policy.

        :param comment: (experimental) A comment to describe the origin request policy. Default: - no comment
        :param cookie_behavior: (experimental) The cookies from viewer requests to include in origin requests. Default: OriginRequestCookieBehavior.none()
        :param header_behavior: (experimental) The HTTP headers to include in origin requests. These can include headers from viewer requests and additional headers added by CloudFront. Default: OriginRequestHeaderBehavior.none()
        :param origin_request_policy_name: (experimental) A unique name to identify the origin request policy. The name must only include '-', '_', or alphanumeric characters. Default: - generated from the ``id``
        :param query_string_behavior: (experimental) The URL query strings from viewer requests to include in origin requests. Default: OriginRequestQueryStringBehavior.none()

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if cookie_behavior is not None:
            self._values["cookie_behavior"] = cookie_behavior
        if header_behavior is not None:
            self._values["header_behavior"] = header_behavior
        if origin_request_policy_name is not None:
            self._values["origin_request_policy_name"] = origin_request_policy_name
        if query_string_behavior is not None:
            self._values["query_string_behavior"] = query_string_behavior

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """(experimental) A comment to describe the origin request policy.

        :default: - no comment

        :stability: experimental
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def cookie_behavior(self) -> typing.Optional[OriginRequestCookieBehavior]:
        """(experimental) The cookies from viewer requests to include in origin requests.

        :default: OriginRequestCookieBehavior.none()

        :stability: experimental
        """
        result = self._values.get("cookie_behavior")
        return result

    @builtins.property
    def header_behavior(self) -> typing.Optional[OriginRequestHeaderBehavior]:
        """(experimental) The HTTP headers to include in origin requests.

        These can include headers from viewer requests and additional headers added by CloudFront.

        :default: OriginRequestHeaderBehavior.none()

        :stability: experimental
        """
        result = self._values.get("header_behavior")
        return result

    @builtins.property
    def origin_request_policy_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A unique name to identify the origin request policy.

        The name must only include '-', '_', or alphanumeric characters.

        :default: - generated from the ``id``

        :stability: experimental
        """
        result = self._values.get("origin_request_policy_name")
        return result

    @builtins.property
    def query_string_behavior(
        self,
    ) -> typing.Optional["OriginRequestQueryStringBehavior"]:
        """(experimental) The URL query strings from viewer requests to include in origin requests.

        :default: OriginRequestQueryStringBehavior.none()

        :stability: experimental
        """
        result = self._values.get("query_string_behavior")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginRequestPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OriginRequestQueryStringBehavior(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.OriginRequestQueryStringBehavior",
):
    """(experimental) Determines whether any URL query strings in viewer requests (and if so, which query strings) are included in requests that CloudFront sends to the origin.

    :stability: experimental
    """

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "OriginRequestQueryStringBehavior":
        """(experimental) All query strings in viewer requests are included in requests that CloudFront sends to the origin.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "all", [])

    @jsii.member(jsii_name="allowList")
    @builtins.classmethod
    def allow_list(
        cls,
        *query_strings: builtins.str,
    ) -> "OriginRequestQueryStringBehavior":
        """(experimental) Only the provided ``queryStrings`` are included in requests that CloudFront sends to the origin.

        :param query_strings: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "allowList", [*query_strings])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "OriginRequestQueryStringBehavior":
        """(experimental) Query strings in viewer requests are not included in requests that CloudFront sends to the origin.

        Any query strings that are listed in a CachePolicy are still included in origin requests.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "none", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        """(experimental) The behavior of query strings -- allow all, none, or only an allow list.

        :stability: experimental
        """
        return jsii.get(self, "behavior")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="queryStrings")
    def query_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) The query strings to allow, if the behavior is an allow list.

        :stability: experimental
        """
        return jsii.get(self, "queryStrings")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginSslPolicy")
class OriginSslPolicy(enum.Enum):
    """
    :stability: experimental
    """

    SSL_V3 = "SSL_V3"
    """
    :stability: experimental
    """
    TLS_V1 = "TLS_V1"
    """
    :stability: experimental
    """
    TLS_V1_1 = "TLS_V1_1"
    """
    :stability: experimental
    """
    TLS_V1_2 = "TLS_V1_2"
    """
    :stability: experimental
    """


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.PriceClass")
class PriceClass(enum.Enum):
    """(experimental) The price class determines how many edge locations CloudFront will use for your distribution.

    See https://aws.amazon.com/cloudfront/pricing/ for full list of supported regions.

    :stability: experimental
    """

    PRICE_CLASS_100 = "PRICE_CLASS_100"
    """(experimental) USA, Canada, Europe, & Israel.

    :stability: experimental
    """
    PRICE_CLASS_200 = "PRICE_CLASS_200"
    """(experimental) PRICE_CLASS_100 + South Africa, Kenya, Middle East, Japan, Singapore, South Korea, Taiwan, Hong Kong, & Philippines.

    :stability: experimental
    """
    PRICE_CLASS_ALL = "PRICE_CLASS_ALL"
    """(experimental) All locations.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.S3OriginConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_bucket_source": "s3BucketSource",
        "origin_access_identity": "originAccessIdentity",
        "origin_headers": "originHeaders",
        "origin_path": "originPath",
    },
)
class S3OriginConfig:
    def __init__(
        self,
        *,
        s3_bucket_source: aws_cdk.aws_s3.IBucket,
        origin_access_identity: typing.Optional[IOriginAccessIdentity] = None,
        origin_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        origin_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) S3 origin configuration for CloudFront.

        :param s3_bucket_source: (experimental) The source bucket to serve content from.
        :param origin_access_identity: (experimental) The optional Origin Access Identity of the origin identity cloudfront will use when calling your s3 bucket. Default: No Origin Access Identity which requires the S3 bucket to be public accessible
        :param origin_headers: (experimental) Any additional headers to pass to the origin. Default: - No additional headers are passed.
        :param origin_path: (experimental) The relative path to the origin root to use for sources. Default: /

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "s3_bucket_source": s3_bucket_source,
        }
        if origin_access_identity is not None:
            self._values["origin_access_identity"] = origin_access_identity
        if origin_headers is not None:
            self._values["origin_headers"] = origin_headers
        if origin_path is not None:
            self._values["origin_path"] = origin_path

    @builtins.property
    def s3_bucket_source(self) -> aws_cdk.aws_s3.IBucket:
        """(experimental) The source bucket to serve content from.

        :stability: experimental
        """
        result = self._values.get("s3_bucket_source")
        assert result is not None, "Required property 's3_bucket_source' is missing"
        return result

    @builtins.property
    def origin_access_identity(self) -> typing.Optional[IOriginAccessIdentity]:
        """(experimental) The optional Origin Access Identity of the origin identity cloudfront will use when calling your s3 bucket.

        :default: No Origin Access Identity which requires the S3 bucket to be public accessible

        :stability: experimental
        """
        result = self._values.get("origin_access_identity")
        return result

    @builtins.property
    def origin_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Any additional headers to pass to the origin.

        :default: - No additional headers are passed.

        :stability: experimental
        """
        result = self._values.get("origin_headers")
        return result

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        """(experimental) The relative path to the origin root to use for sources.

        :default: /

        :stability: experimental
        """
        result = self._values.get("origin_path")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3OriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SSLMethod")
class SSLMethod(enum.Enum):
    """(experimental) The SSL method CloudFront will use for your distribution.

    Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates
    which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present
    multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites
    (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate.

    CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support.

    If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for
    using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP).

    See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/

    :stability: experimental
    """

    SNI = "SNI"
    """
    :stability: experimental
    """
    VIP = "VIP"
    """
    :stability: experimental
    """


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SecurityPolicyProtocol")
class SecurityPolicyProtocol(enum.Enum):
    """(experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

    CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify.

    :stability: experimental
    """

    SSL_V3 = "SSL_V3"
    """
    :stability: experimental
    """
    TLS_V1 = "TLS_V1"
    """
    :stability: experimental
    """
    TLS_V1_2016 = "TLS_V1_2016"
    """
    :stability: experimental
    """
    TLS_V1_1_2016 = "TLS_V1_1_2016"
    """
    :stability: experimental
    """
    TLS_V1_2_2018 = "TLS_V1_2_2018"
    """
    :stability: experimental
    """
    TLS_V1_2_2019 = "TLS_V1_2_2019"
    """
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.SourceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "behaviors": "behaviors",
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_origin_source": "customOriginSource",
        "failover_criteria_status_codes": "failoverCriteriaStatusCodes",
        "failover_custom_origin_source": "failoverCustomOriginSource",
        "failover_s3_origin_source": "failoverS3OriginSource",
        "origin_headers": "originHeaders",
        "origin_path": "originPath",
        "s3_origin_source": "s3OriginSource",
    },
)
class SourceConfiguration:
    def __init__(
        self,
        *,
        behaviors: typing.List[Behavior],
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        custom_origin_source: typing.Optional[CustomOriginConfig] = None,
        failover_criteria_status_codes: typing.Optional[typing.List[FailoverStatusCode]] = None,
        failover_custom_origin_source: typing.Optional[CustomOriginConfig] = None,
        failover_s3_origin_source: typing.Optional[S3OriginConfig] = None,
        origin_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        origin_path: typing.Optional[builtins.str] = None,
        s3_origin_source: typing.Optional[S3OriginConfig] = None,
    ) -> None:
        """(experimental) A source configuration is a wrapper for CloudFront origins and behaviors.

        An origin is what CloudFront will "be in front of" - that is, CloudFront will pull it's assets from an origin.

        If you're using s3 as a source - pass the ``s3Origin`` property, otherwise, pass the ``customOriginSource`` property.

        One or the other must be passed, and it is invalid to pass both in the same SourceConfiguration.

        :param behaviors: (experimental) The behaviors associated with this source. At least one (default) behavior must be included.
        :param connection_attempts: (experimental) The number of times that CloudFront attempts to connect to the origin. You can specify 1, 2, or 3 as the number of attempts. Default: 3
        :param connection_timeout: (experimental) The number of seconds that CloudFront waits when trying to establish a connection to the origin. You can specify a number of seconds between 1 and 10 (inclusive). Default: cdk.Duration.seconds(10)
        :param custom_origin_source: (experimental) A custom origin source - for all non-s3 sources.
        :param failover_criteria_status_codes: (experimental) HTTP status code to failover to second origin. Default: [500, 502, 503, 504]
        :param failover_custom_origin_source: (experimental) A custom origin source for failover in case the s3OriginSource returns invalid status code. Default: - no failover configuration
        :param failover_s3_origin_source: (experimental) An s3 origin source for failover in case the s3OriginSource returns invalid status code. Default: - no failover configuration
        :param origin_headers: (deprecated) Any additional headers to pass to the origin. Default: - No additional headers are passed.
        :param origin_path: (deprecated) The relative path to the origin root to use for sources. Default: /
        :param s3_origin_source: (experimental) An s3 origin source - if you're using s3 for your assets.

        :stability: experimental
        """
        if isinstance(custom_origin_source, dict):
            custom_origin_source = CustomOriginConfig(**custom_origin_source)
        if isinstance(failover_custom_origin_source, dict):
            failover_custom_origin_source = CustomOriginConfig(**failover_custom_origin_source)
        if isinstance(failover_s3_origin_source, dict):
            failover_s3_origin_source = S3OriginConfig(**failover_s3_origin_source)
        if isinstance(s3_origin_source, dict):
            s3_origin_source = S3OriginConfig(**s3_origin_source)
        self._values: typing.Dict[str, typing.Any] = {
            "behaviors": behaviors,
        }
        if connection_attempts is not None:
            self._values["connection_attempts"] = connection_attempts
        if connection_timeout is not None:
            self._values["connection_timeout"] = connection_timeout
        if custom_origin_source is not None:
            self._values["custom_origin_source"] = custom_origin_source
        if failover_criteria_status_codes is not None:
            self._values["failover_criteria_status_codes"] = failover_criteria_status_codes
        if failover_custom_origin_source is not None:
            self._values["failover_custom_origin_source"] = failover_custom_origin_source
        if failover_s3_origin_source is not None:
            self._values["failover_s3_origin_source"] = failover_s3_origin_source
        if origin_headers is not None:
            self._values["origin_headers"] = origin_headers
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if s3_origin_source is not None:
            self._values["s3_origin_source"] = s3_origin_source

    @builtins.property
    def behaviors(self) -> typing.List[Behavior]:
        """(experimental) The behaviors associated with this source.

        At least one (default) behavior must be included.

        :stability: experimental
        """
        result = self._values.get("behaviors")
        assert result is not None, "Required property 'behaviors' is missing"
        return result

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        """(experimental) The number of times that CloudFront attempts to connect to the origin.

        You can specify 1, 2, or 3 as the number of attempts.

        :default: 3

        :stability: experimental
        """
        result = self._values.get("connection_attempts")
        return result

    @builtins.property
    def connection_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The number of seconds that CloudFront waits when trying to establish a connection to the origin.

        You can specify a number of seconds between 1 and 10 (inclusive).

        :default: cdk.Duration.seconds(10)

        :stability: experimental
        """
        result = self._values.get("connection_timeout")
        return result

    @builtins.property
    def custom_origin_source(self) -> typing.Optional[CustomOriginConfig]:
        """(experimental) A custom origin source - for all non-s3 sources.

        :stability: experimental
        """
        result = self._values.get("custom_origin_source")
        return result

    @builtins.property
    def failover_criteria_status_codes(
        self,
    ) -> typing.Optional[typing.List[FailoverStatusCode]]:
        """(experimental) HTTP status code to failover to second origin.

        :default: [500, 502, 503, 504]

        :stability: experimental
        """
        result = self._values.get("failover_criteria_status_codes")
        return result

    @builtins.property
    def failover_custom_origin_source(self) -> typing.Optional[CustomOriginConfig]:
        """(experimental) A custom origin source for failover in case the s3OriginSource returns invalid status code.

        :default: - no failover configuration

        :stability: experimental
        """
        result = self._values.get("failover_custom_origin_source")
        return result

    @builtins.property
    def failover_s3_origin_source(self) -> typing.Optional[S3OriginConfig]:
        """(experimental) An s3 origin source for failover in case the s3OriginSource returns invalid status code.

        :default: - no failover configuration

        :stability: experimental
        """
        result = self._values.get("failover_s3_origin_source")
        return result

    @builtins.property
    def origin_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(deprecated) Any additional headers to pass to the origin.

        :default: - No additional headers are passed.

        :deprecated: Use originHeaders on s3OriginSource or customOriginSource

        :stability: deprecated
        """
        result = self._values.get("origin_headers")
        return result

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        """(deprecated) The relative path to the origin root to use for sources.

        :default: /

        :deprecated: Use originPath on s3OriginSource or customOriginSource

        :stability: deprecated
        """
        result = self._values.get("origin_path")
        return result

    @builtins.property
    def s3_origin_source(self) -> typing.Optional[S3OriginConfig]:
        """(experimental) An s3 origin source - if you're using s3 for your assets.

        :stability: experimental
        """
        result = self._values.get("s3_origin_source")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewerCertificate(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.ViewerCertificate",
):
    """(experimental) Viewer certificate configuration class.

    :stability: experimental
    """

    @jsii.member(jsii_name="fromAcmCertificate")
    @builtins.classmethod
    def from_acm_certificate(
        cls,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        *,
        aliases: typing.Optional[typing.List[builtins.str]] = None,
        security_policy: typing.Optional[SecurityPolicyProtocol] = None,
        ssl_method: typing.Optional[SSLMethod] = None,
    ) -> "ViewerCertificate":
        """(experimental) Generate an AWS Certificate Manager (ACM) viewer certificate configuration.

        :param certificate: AWS Certificate Manager (ACM) certificate. Your certificate must be located in the us-east-1 (US East (N. Virginia)) region to be accessed by CloudFront
        :param aliases: (experimental) Domain names on the certificate (both main domain name and Subject Alternative names).
        :param security_policy: (experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI
        :param ssl_method: (experimental) How CloudFront should serve HTTPS requests. See the notes on SSLMethod if you wish to use other SSL termination types. Default: SSLMethod.SNI

        :stability: experimental
        """
        options = ViewerCertificateOptions(
            aliases=aliases, security_policy=security_policy, ssl_method=ssl_method
        )

        return jsii.sinvoke(cls, "fromAcmCertificate", [certificate, options])

    @jsii.member(jsii_name="fromCloudFrontDefaultCertificate")
    @builtins.classmethod
    def from_cloud_front_default_certificate(
        cls,
        *aliases: builtins.str,
    ) -> "ViewerCertificate":
        """(experimental) Generate a viewer certifcate configuration using the CloudFront default certificate (e.g. d111111abcdef8.cloudfront.net) and a {@link SecurityPolicyProtocol.TLS_V1} security policy.

        :param aliases: Alternative CNAME aliases You also must create a CNAME record with your DNS service to route queries.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCloudFrontDefaultCertificate", [*aliases])

    @jsii.member(jsii_name="fromIamCertificate")
    @builtins.classmethod
    def from_iam_certificate(
        cls,
        iam_certificate_id: builtins.str,
        *,
        aliases: typing.Optional[typing.List[builtins.str]] = None,
        security_policy: typing.Optional[SecurityPolicyProtocol] = None,
        ssl_method: typing.Optional[SSLMethod] = None,
    ) -> "ViewerCertificate":
        """(experimental) Generate an IAM viewer certificate configuration.

        :param iam_certificate_id: Identifier of the IAM certificate.
        :param aliases: (experimental) Domain names on the certificate (both main domain name and Subject Alternative names).
        :param security_policy: (experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI
        :param ssl_method: (experimental) How CloudFront should serve HTTPS requests. See the notes on SSLMethod if you wish to use other SSL termination types. Default: SSLMethod.SNI

        :stability: experimental
        """
        options = ViewerCertificateOptions(
            aliases=aliases, security_policy=security_policy, ssl_method=ssl_method
        )

        return jsii.sinvoke(cls, "fromIamCertificate", [iam_certificate_id, options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliases")
    def aliases(self) -> typing.List[builtins.str]:
        """
        :stability: experimental
        """
        return jsii.get(self, "aliases")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="props")
    def props(self) -> CfnDistribution.ViewerCertificateProperty:
        """
        :stability: experimental
        """
        return jsii.get(self, "props")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront.ViewerCertificateOptions",
    jsii_struct_bases=[],
    name_mapping={
        "aliases": "aliases",
        "security_policy": "securityPolicy",
        "ssl_method": "sslMethod",
    },
)
class ViewerCertificateOptions:
    def __init__(
        self,
        *,
        aliases: typing.Optional[typing.List[builtins.str]] = None,
        security_policy: typing.Optional[SecurityPolicyProtocol] = None,
        ssl_method: typing.Optional[SSLMethod] = None,
    ) -> None:
        """
        :param aliases: (experimental) Domain names on the certificate (both main domain name and Subject Alternative names).
        :param security_policy: (experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI
        :param ssl_method: (experimental) How CloudFront should serve HTTPS requests. See the notes on SSLMethod if you wish to use other SSL termination types. Default: SSLMethod.SNI

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if aliases is not None:
            self._values["aliases"] = aliases
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if ssl_method is not None:
            self._values["ssl_method"] = ssl_method

    @builtins.property
    def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Domain names on the certificate (both main domain name and Subject Alternative names).

        :stability: experimental
        """
        result = self._values.get("aliases")
        return result

    @builtins.property
    def security_policy(self) -> typing.Optional[SecurityPolicyProtocol]:
        """(experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

        CloudFront serves your objects only to browsers or devices that support at
        least the SSL version that you specify.

        :default: - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI

        :stability: experimental
        """
        result = self._values.get("security_policy")
        return result

    @builtins.property
    def ssl_method(self) -> typing.Optional[SSLMethod]:
        """(experimental) How CloudFront should serve HTTPS requests.

        See the notes on SSLMethod if you wish to use other SSL termination types.

        :default: SSLMethod.SNI

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_ViewerCertificate.html
        :stability: experimental
        """
        result = self._values.get("ssl_method")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewerCertificateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.ViewerProtocolPolicy")
class ViewerProtocolPolicy(enum.Enum):
    """(experimental) How HTTPs should be handled with your distribution.

    :stability: experimental
    """

    HTTPS_ONLY = "HTTPS_ONLY"
    """(experimental) HTTPS only.

    :stability: experimental
    """
    REDIRECT_TO_HTTPS = "REDIRECT_TO_HTTPS"
    """(experimental) Will redirect HTTP requests to HTTPS.

    :stability: experimental
    """
    ALLOW_ALL = "ALLOW_ALL"
    """(experimental) Both HTTP and HTTPS supported.

    :stability: experimental
    """


@jsii.implements(ICachePolicy)
class CachePolicy(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CachePolicy",
):
    """(experimental) A Cache Policy configuration.

    :stability: experimental
    :resource: AWS::CloudFront::CachePolicy
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cache_policy_name: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        cookie_behavior: typing.Optional[CacheCookieBehavior] = None,
        default_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        enable_accept_encoding_brotli: typing.Optional[builtins.bool] = None,
        enable_accept_encoding_gzip: typing.Optional[builtins.bool] = None,
        header_behavior: typing.Optional[CacheHeaderBehavior] = None,
        max_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        min_ttl: typing.Optional[aws_cdk.core.Duration] = None,
        query_string_behavior: typing.Optional[CacheQueryStringBehavior] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cache_policy_name: (experimental) A unique name to identify the cache policy. The name must only include '-', '_', or alphanumeric characters. Default: - generated from the ``id``
        :param comment: (experimental) A comment to describe the cache policy. Default: - no comment
        :param cookie_behavior: (experimental) Determines whether any cookies in viewer requests are included in the cache key and automatically included in requests that CloudFront sends to the origin. Default: CacheCookieBehavior.none()
        :param default_ttl: (experimental) The default amount of time for objects to stay in the CloudFront cache. Only used when the origin does not send Cache-Control or Expires headers with the object. Default: - The greater of 1 day and ``minTtl``
        :param enable_accept_encoding_brotli: (experimental) Whether to normalize and include the ``Accept-Encoding`` header in the cache key when the ``Accept-Encoding`` header is 'br'. Default: false
        :param enable_accept_encoding_gzip: (experimental) Whether to normalize and include the ``Accept-Encoding`` header in the cache key when the ``Accept-Encoding`` header is 'gzip'. Default: false
        :param header_behavior: (experimental) Determines whether any HTTP headers are included in the cache key and automatically included in requests that CloudFront sends to the origin. Default: CacheHeaderBehavior.none()
        :param max_ttl: (experimental) The maximum amount of time for objects to stay in the CloudFront cache. CloudFront uses this value only when the origin sends Cache-Control or Expires headers with the object. Default: - The greater of 1 year and ``defaultTtl``
        :param min_ttl: (experimental) The minimum amount of time for objects to stay in the CloudFront cache. Default: Duration.seconds(0)
        :param query_string_behavior: (experimental) Determines whether any query strings are included in the cache key and automatically included in requests that CloudFront sends to the origin. Default: CacheQueryStringBehavior.none()

        :stability: experimental
        """
        props = CachePolicyProps(
            cache_policy_name=cache_policy_name,
            comment=comment,
            cookie_behavior=cookie_behavior,
            default_ttl=default_ttl,
            enable_accept_encoding_brotli=enable_accept_encoding_brotli,
            enable_accept_encoding_gzip=enable_accept_encoding_gzip,
            header_behavior=header_behavior,
            max_ttl=max_ttl,
            min_ttl=min_ttl,
            query_string_behavior=query_string_behavior,
        )

        jsii.create(CachePolicy, self, [scope, id, props])

    @jsii.member(jsii_name="fromCachePolicyId")
    @builtins.classmethod
    def from_cache_policy_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        cache_policy_id: builtins.str,
    ) -> ICachePolicy:
        """(experimental) Imports a Cache Policy from its id.

        :param scope: -
        :param id: -
        :param cache_policy_id: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCachePolicyId", [scope, id, cache_policy_id])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CACHING_DISABLED")
    def CACHING_DISABLED(cls) -> ICachePolicy:
        """(experimental) Disables caching.

        This policy is useful for dynamic content and for requests that are not cacheable.

        :stability: experimental
        """
        return jsii.sget(cls, "CACHING_DISABLED")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CACHING_OPTIMIZED")
    def CACHING_OPTIMIZED(cls) -> ICachePolicy:
        """(experimental) Optimize cache efficiency by minimizing the values that CloudFront includes in the cache key.

        Query strings and cookies are not included in the cache key, and only the normalized 'Accept-Encoding' header is included.

        :stability: experimental
        """
        return jsii.sget(cls, "CACHING_OPTIMIZED")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CACHING_OPTIMIZED_FOR_UNCOMPRESSED_OBJECTS")
    def CACHING_OPTIMIZED_FOR_UNCOMPRESSED_OBJECTS(cls) -> ICachePolicy:
        """(experimental) Optimize cache efficiency by minimizing the values that CloudFront includes in the cache key.

        Query strings and cookies are not included in the cache key, and only the normalized 'Accept-Encoding' header is included.
        Disables cache compression.

        :stability: experimental
        """
        return jsii.sget(cls, "CACHING_OPTIMIZED_FOR_UNCOMPRESSED_OBJECTS")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="ELEMENTAL_MEDIA_PACKAGE")
    def ELEMENTAL_MEDIA_PACKAGE(cls) -> ICachePolicy:
        """(experimental) Designed for use with an origin that is an AWS Elemental MediaPackage endpoint.

        :stability: experimental
        """
        return jsii.sget(cls, "ELEMENTAL_MEDIA_PACKAGE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cachePolicyId")
    def cache_policy_id(self) -> builtins.str:
        """(experimental) The ID of the cache policy.

        :stability: experimental
        """
        return jsii.get(self, "cachePolicyId")


@jsii.implements(IDistribution)
class CloudFrontWebDistribution(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistribution",
):
    """(experimental) Amazon CloudFront is a global content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to your viewers with low latency and high transfer speeds.

    CloudFront fronts user provided content and caches it at edge locations across the world.

    Here's how you can use this construct::

       # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
       from aws_cdk.aws_cloudfront import CloudFrontWebDistribution

       source_bucket = Bucket(self, "Bucket")

       distribution = CloudFrontWebDistribution(self, "MyDistribution",
           origin_configs=[SourceConfiguration(
               s3_origin_source=S3OriginConfig(
                   s3_bucket_source=source_bucket
               ),
               behaviors=[Behavior(is_default_behavior=True)]
           )
           ]
       )

    This will create a CloudFront distribution that uses your S3Bucket as it's origin.

    You can customize the distribution using additional properties from the CloudFrontWebDistributionProps interface.

    :stability: experimental
    :resource: AWS::CloudFront::Distribution
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        origin_configs: typing.List[SourceConfiguration],
        alias_configuration: typing.Optional[AliasConfiguration] = None,
        comment: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        enable_ip_v6: typing.Optional[builtins.bool] = None,
        error_configurations: typing.Optional[typing.List[CfnDistribution.CustomErrorResponseProperty]] = None,
        geo_restriction: typing.Optional[GeoRestriction] = None,
        http_version: typing.Optional[HttpVersion] = None,
        logging_config: typing.Optional[LoggingConfiguration] = None,
        price_class: typing.Optional[PriceClass] = None,
        viewer_certificate: typing.Optional[ViewerCertificate] = None,
        viewer_protocol_policy: typing.Optional[ViewerProtocolPolicy] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param origin_configs: (experimental) The origin configurations for this distribution. Behaviors are a part of the origin.
        :param alias_configuration: (deprecated) AliasConfiguration is used to configured CloudFront to respond to requests on custom domain names. Default: - None.
        :param comment: (experimental) A comment for this distribution in the CloudFront console. Default: - No comment is added to distribution.
        :param default_root_object: (experimental) The default object to serve. Default: - "index.html" is served.
        :param enable_ip_v6: (experimental) If your distribution should have IPv6 enabled. Default: true
        :param error_configurations: (experimental) How CloudFront should handle requests that are not successful (eg PageNotFound). By default, CloudFront does not replace HTTP status codes in the 4xx and 5xx range with custom error messages. CloudFront does not cache HTTP status codes. Default: - No custom error configuration.
        :param geo_restriction: (experimental) Controls the countries in which your content is distributed. Default: No geo restriction
        :param http_version: (experimental) The max supported HTTP Versions. Default: HttpVersion.HTTP2
        :param logging_config: (experimental) Optional - if we should enable logging. You can pass an empty object ({}) to have us auto create a bucket for logging. Omission of this property indicates no logging is to be enabled. Default: - no logging is enabled by default.
        :param price_class: (experimental) The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing). Default: PriceClass.PRICE_CLASS_100 the cheapest option for CloudFront is picked by default.
        :param viewer_certificate: (experimental) Specifies whether you want viewers to use HTTP or HTTPS to request your objects, whether you're using an alternate domain name with HTTPS, and if so, if you're using AWS Certificate Manager (ACM) or a third-party certificate authority. Default: ViewerCertificate.fromCloudFrontDefaultCertificate()
        :param viewer_protocol_policy: (experimental) The default viewer policy for incoming clients. Default: RedirectToHTTPs
        :param web_acl_id: (experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).

        :stability: experimental
        """
        props = CloudFrontWebDistributionProps(
            origin_configs=origin_configs,
            alias_configuration=alias_configuration,
            comment=comment,
            default_root_object=default_root_object,
            enable_ip_v6=enable_ip_v6,
            error_configurations=error_configurations,
            geo_restriction=geo_restriction,
            http_version=http_version,
            logging_config=logging_config,
            price_class=price_class,
            viewer_certificate=viewer_certificate,
            viewer_protocol_policy=viewer_protocol_policy,
            web_acl_id=web_acl_id,
        )

        jsii.create(CloudFrontWebDistribution, self, [scope, id, props])

    @jsii.member(jsii_name="fromDistributionAttributes")
    @builtins.classmethod
    def from_distribution_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        distribution_id: builtins.str,
        domain_name: builtins.str,
    ) -> IDistribution:
        """(experimental) Creates a construct that represents an external (imported) distribution.

        :param scope: -
        :param id: -
        :param distribution_id: (experimental) The distribution ID for this distribution.
        :param domain_name: (experimental) The generated domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        """
        attrs = CloudFrontWebDistributionAttributes(
            distribution_id=distribution_id, domain_name=domain_name
        )

        return jsii.sinvoke(cls, "fromDistributionAttributes", [scope, id, attrs])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        """(experimental) The domain name created by CloudFront for this distribution.

        If you are using aliases for your distribution, this is the domainName your DNS records should point to.
        (In Route53, you could create an ALIAS record to this value, for example.)

        :stability: experimental
        """
        return jsii.get(self, "distributionDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        """(experimental) The distribution ID for this distribution.

        :stability: experimental
        """
        return jsii.get(self, "distributionId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """(deprecated) The domain name created by CloudFront for this distribution.

        If you are using aliases for your distribution, this is the domainName your DNS records should point to.
        (In Route53, you could create an ALIAS record to this value, for example.)

        :deprecated: - Use ``distributionDomainName`` instead.

        :stability: deprecated
        """
        return jsii.get(self, "domainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loggingBucket")
    def logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """(experimental) The logging bucket for this CloudFront distribution.

        If logging is not enabled for this distribution - this property will be undefined.

        :stability: experimental
        """
        return jsii.get(self, "loggingBucket")


@jsii.implements(IDistribution)
class Distribution(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront.Distribution",
):
    """(experimental) A CloudFront distribution with associated origin(s) and caching behavior(s).

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        default_behavior: BehaviorOptions,
        additional_behaviors: typing.Optional[typing.Mapping[builtins.str, BehaviorOptions]] = None,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.List[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_responses: typing.Optional[typing.List[ErrorResponse]] = None,
        geo_restriction: typing.Optional[GeoRestriction] = None,
        http_version: typing.Optional[HttpVersion] = None,
        log_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        price_class: typing.Optional[PriceClass] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param default_behavior: (experimental) The default behavior for the distribution.
        :param additional_behaviors: (experimental) Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to. Default: - no additional behaviors are added.
        :param certificate: (experimental) A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param comment: (experimental) Any comments you want to include about the distribution. Default: - no comment
        :param default_root_object: (experimental) The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/). Default: - no default root object
        :param domain_names: (experimental) Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you must add (at least one of) the domain names of the certificate to this list. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        :param enabled: (experimental) Enable or disable the distribution. Default: true
        :param enable_ipv6: (experimental) Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address. If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second request, for an IPv4 address for your distribution. Default: true
        :param enable_logging: (experimental) Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param error_responses: (experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: (experimental) Controls the countries in which your content is distributed. Default: - No geographic restrictions
        :param http_version: (experimental) Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront. For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI). Default: HttpVersion.HTTP2
        :param log_bucket: (experimental) The Amazon S3 bucket to store the access logs in. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: (experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: (experimental) Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param price_class: (experimental) The price class that corresponds with the maximum price that you want to pay for CloudFront service. If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations. If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location that has the lowest latency among the edge locations in your price class. Default: PriceClass.PRICE_CLASS_ALL
        :param web_acl_id: (experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).

        :stability: experimental
        """
        props = DistributionProps(
            default_behavior=default_behavior,
            additional_behaviors=additional_behaviors,
            certificate=certificate,
            comment=comment,
            default_root_object=default_root_object,
            domain_names=domain_names,
            enabled=enabled,
            enable_ipv6=enable_ipv6,
            enable_logging=enable_logging,
            error_responses=error_responses,
            geo_restriction=geo_restriction,
            http_version=http_version,
            log_bucket=log_bucket,
            log_file_prefix=log_file_prefix,
            log_includes_cookies=log_includes_cookies,
            price_class=price_class,
            web_acl_id=web_acl_id,
        )

        jsii.create(Distribution, self, [scope, id, props])

    @jsii.member(jsii_name="fromDistributionAttributes")
    @builtins.classmethod
    def from_distribution_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        distribution_id: builtins.str,
        domain_name: builtins.str,
    ) -> IDistribution:
        """(experimental) Creates a Distribution construct that represents an external (imported) distribution.

        :param scope: -
        :param id: -
        :param distribution_id: (experimental) The distribution ID for this distribution.
        :param domain_name: (experimental) The generated domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        """
        attrs = DistributionAttributes(
            distribution_id=distribution_id, domain_name=domain_name
        )

        return jsii.sinvoke(cls, "fromDistributionAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addBehavior")
    def add_behavior(
        self,
        path_pattern: builtins.str,
        origin: IOrigin,
        *,
        allowed_methods: typing.Optional[AllowedMethods] = None,
        cached_methods: typing.Optional[CachedMethods] = None,
        cache_policy: typing.Optional[ICachePolicy] = None,
        compress: typing.Optional[builtins.bool] = None,
        edge_lambdas: typing.Optional[typing.List[EdgeLambda]] = None,
        origin_request_policy: typing.Optional[IOriginRequestPolicy] = None,
        smooth_streaming: typing.Optional[builtins.bool] = None,
        viewer_protocol_policy: typing.Optional[ViewerProtocolPolicy] = None,
    ) -> None:
        """(experimental) Adds a new behavior to this distribution for the given pathPattern.

        :param path_pattern: the path pattern (e.g., 'images/*') that specifies which requests to apply the behavior to.
        :param origin: the origin to use for this behavior.
        :param allowed_methods: (experimental) HTTP methods to allow for this behavior. Default: AllowedMethods.ALLOW_GET_HEAD
        :param cached_methods: (experimental) HTTP methods to cache for this behavior. Default: CachedMethods.CACHE_GET_HEAD
        :param cache_policy: (experimental) The cache policy for this behavior. The cache policy determines what values are included in the cache key, and the time-to-live (TTL) values for the cache. Default: CachePolicy.CACHING_OPTIMIZED
        :param compress: (experimental) Whether you want CloudFront to automatically compress certain files for this cache behavior. See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types for file types CloudFront will compress. Default: true
        :param edge_lambdas: (experimental) The Lambda@Edge functions to invoke before serving the contents. Default: - no Lambda functions will be invoked
        :param origin_request_policy: (experimental) The origin request policy for this behavior. The origin request policy determines which values (e.g., headers, cookies) are included in requests that CloudFront sends to the origin. Default: - none
        :param smooth_streaming: (experimental) Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior. Default: false
        :param viewer_protocol_policy: (experimental) The protocol that viewers can use to access the files controlled by this behavior. Default: ViewerProtocolPolicy.ALLOW_ALL

        :stability: experimental
        """
        behavior_options = AddBehaviorOptions(
            allowed_methods=allowed_methods,
            cached_methods=cached_methods,
            cache_policy=cache_policy,
            compress=compress,
            edge_lambdas=edge_lambdas,
            origin_request_policy=origin_request_policy,
            smooth_streaming=smooth_streaming,
            viewer_protocol_policy=viewer_protocol_policy,
        )

        return jsii.invoke(self, "addBehavior", [path_pattern, origin, behavior_options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        """(experimental) The domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        """
        return jsii.get(self, "distributionDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        """(experimental) The distribution ID for this distribution.

        :stability: experimental
        """
        return jsii.get(self, "distributionId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """(experimental) The domain name of the Distribution, such as d111111abcdef8.cloudfront.net.

        :stability: experimental
        """
        return jsii.get(self, "domainName")


__all__ = [
    "AddBehaviorOptions",
    "AliasConfiguration",
    "AllowedMethods",
    "Behavior",
    "BehaviorOptions",
    "CacheCookieBehavior",
    "CacheHeaderBehavior",
    "CachePolicy",
    "CachePolicyProps",
    "CacheQueryStringBehavior",
    "CachedMethods",
    "CfnCachePolicy",
    "CfnCachePolicyProps",
    "CfnCloudFrontOriginAccessIdentity",
    "CfnCloudFrontOriginAccessIdentityProps",
    "CfnDistribution",
    "CfnDistributionProps",
    "CfnOriginRequestPolicy",
    "CfnOriginRequestPolicyProps",
    "CfnRealtimeLogConfig",
    "CfnRealtimeLogConfigProps",
    "CfnStreamingDistribution",
    "CfnStreamingDistributionProps",
    "CloudFrontAllowedCachedMethods",
    "CloudFrontAllowedMethods",
    "CloudFrontWebDistribution",
    "CloudFrontWebDistributionAttributes",
    "CloudFrontWebDistributionProps",
    "CustomOriginConfig",
    "Distribution",
    "DistributionAttributes",
    "DistributionProps",
    "EdgeLambda",
    "ErrorResponse",
    "FailoverStatusCode",
    "GeoRestriction",
    "HttpVersion",
    "ICachePolicy",
    "IDistribution",
    "IOrigin",
    "IOriginAccessIdentity",
    "IOriginRequestPolicy",
    "LambdaEdgeEventType",
    "LambdaFunctionAssociation",
    "LoggingConfiguration",
    "OriginAccessIdentity",
    "OriginAccessIdentityProps",
    "OriginBase",
    "OriginBindConfig",
    "OriginBindOptions",
    "OriginFailoverConfig",
    "OriginProps",
    "OriginProtocolPolicy",
    "OriginRequestCookieBehavior",
    "OriginRequestHeaderBehavior",
    "OriginRequestPolicy",
    "OriginRequestPolicyProps",
    "OriginRequestQueryStringBehavior",
    "OriginSslPolicy",
    "PriceClass",
    "S3OriginConfig",
    "SSLMethod",
    "SecurityPolicyProtocol",
    "SourceConfiguration",
    "ViewerCertificate",
    "ViewerCertificateOptions",
    "ViewerProtocolPolicy",
]

publication.publish()
