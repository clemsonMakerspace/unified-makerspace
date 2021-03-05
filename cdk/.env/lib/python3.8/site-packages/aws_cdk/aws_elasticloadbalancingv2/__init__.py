"""
## Amazon Elastic Load Balancing V2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

The `@aws-cdk/aws-elasticloadbalancingv2` package provides constructs for
configuring application and network load balancers.

For more information, see the AWS documentation for
[Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
and [Network Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html).

### Defining an Application Load Balancer

You define an application load balancer by creating an instance of
`ApplicationLoadBalancer`, adding a Listener to the load balancer
and adding Targets to the Listener:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
from aws_cdk.aws_autoscaling import AutoScalingGroup

# ...

vpc = ec2.Vpc(...)

# Create the load balancer in a VPC. 'internetFacing' is 'false'
# by default, which creates an internal load balancer.
lb = elbv2.ApplicationLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)

# Add a listener and open up the load balancer's security group
# to the world.
listener = lb.add_listener("Listener",
    port=80,

    # 'open: true' is the default, you can leave it out if you want. Set it
    # to 'false' and use `listener.connections` if you want to be selective
    # about who can access the load balancer.
    open=True
)

# Create an AutoScaling group and add it as a load balancing
# target to the listener.
asg = AutoScalingGroup(...)
listener.add_targets("ApplicationFleet",
    port=8080,
    targets=[asg]
)
```

The security groups of the load balancer and the target are automatically
updated to allow the network traffic.

One (or more) security groups can be associated with the load balancer;
if a security group isn't provided, one will be automatically created.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
security_group1 = ec2.SecurityGroup(stack, "SecurityGroup1", vpc=vpc)
lb = elbv2.ApplicationLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True,
    security_group=security_group1
)

security_group2 = ec2.SecurityGroup(stack, "SecurityGroup2", vpc=vpc)
lb.add_security_group(security_group2)
```

#### Conditions

It's possible to route traffic to targets based on conditions in the incoming
HTTP request. For example, the following will route requests to the indicated
AutoScalingGroup only if the requested host in the request is either for
`example.com/ok` or `example.com/path`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("Example.Com Fleet",
    priority=10,
    conditions=[
        ListenerCondition.host_headers(["example.com"]),
        ListenerCondition.path_patterns(["/ok", "/path"])
    ],
    port=8080,
    targets=[asg]
)
```

A target with a condition contains either `pathPatterns` or `hostHeader`, or
both. If both are specified, both conditions must be met for the requests to
be routed to the given target. `priority` is a required field when you add
targets with conditions. The lowest number wins.

Every listener must have at least one target without conditions, which is
where all requests that didn't match any of the conditions will be sent.

#### Convenience methods and more complex Actions

Routing traffic from a Load Balancer to a Target involves the following steps:

* Create a Target Group, register the Target into the Target Group
* Add an Action to the Listener which forwards traffic to the Target Group.

Various methods on the `Listener` take care of this work for you to a greater
or lesser extent:

* `addTargets()` performs both steps: automatically creates a Target Group and the
  required Action.
* `addTargetGroups()` gives you more control: you create the Target Group (or
  Target Groups) yourself and the method creates Action that routes traffic to
  the Target Groups.
* `addAction()` gives you full control: you supply the Action and wire it up
  to the Target Groups yourself (or access one of the other ELB routing features).

Using `addAction()` gives you access to some of the features of an Elastic Load
Balancer that the other two convenience methods don't:

* **Routing stickiness**: use `ListenerAction.forward()` and supply a
  `stickinessDuration` to make sure requests are routed to the same target group
  for a given duration.
* **Weighted Target Groups**: use `ListenerAction.weightedForward()`
  to give different weights to different target groups.
* **Fixed Responses**: use `ListenerAction.fixedResponse()` to serve
  a static response (ALB only).
* **Redirects**: use `ListenerAction.redirect()` to serve an HTTP
  redirect response (ALB only).
* **Authentication**: use `ListenerAction.authenticateOidc()` to
  perform OpenID authentication before serving a request (see the
  `@aws-cdk/aws-elasticloadbalancingv2-actions` package for direct authentication
  integration with Cognito) (ALB only).

Here's an example of serving a fixed response at the `/ok` URL:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_action("Fixed",
    priority=10,
    conditions=[
        ListenerCondition.path_patterns(["/ok"])
    ],
    action=ListenerAction.fixed_response(200,
        content_type=elbv2.ContentType.TEXT_PLAIN,
        message_body="OK"
    )
)
```

Here's an example of using OIDC authentication before forwarding to a TargetGroup:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_action("DefaultAction",
    action=ListenerAction.authenticate_oidc(
        authorization_endpoint="https://example.com/openid",
        # Other OIDC properties here
        # ...
        next=ListenerAction.forward([my_target_group])
    )
)
```

If you just want to redirect all incoming traffic on one port to another port, you can use the following code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lb.add_redirect(
    source_protocol=elbv2.ApplicationProtocol.HTTPS,
    source_port=8443,
    target_protocol=elbv2.ApplicationProtocol.HTTP,
    target_port=8080
)
```

If you do not provide any options for this method, it redirects HTTP port 80 to HTTPS port 443.

### Defining a Network Load Balancer

Network Load Balancers are defined in a similar way to Application Load
Balancers:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_autoscaling as autoscaling

# Create the load balancer in a VPC. 'internetFacing' is 'false'
# by default, which creates an internal load balancer.
lb = elbv2.NetworkLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)

# Add a listener on a particular port.
listener = lb.add_listener("Listener",
    port=443
)

# Add targets on a particular port.
listener.add_targets("AppFleet",
    port=443,
    targets=[asg]
)
```

One thing to keep in mind is that network load balancers do not have security
groups, and no automatic security group configuration is done for you. You will
have to configure the security groups of the target yourself to allow traffic by
clients and/or load balancer instances, depending on your target types.  See
[Target Groups for your Network Load
Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html)
and [Register targets with your Target
Group](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-register-targets.html)
for more information.

### Targets and Target Groups

Application and Network Load Balancers organize load balancing targets in Target
Groups. If you add your balancing targets (such as AutoScalingGroups, ECS
services or individual instances) to your listener directly, the appropriate
`TargetGroup` will be automatically created for you.

If you need more control over the Target Groups created, create an instance of
`ApplicationTargetGroup` or `NetworkTargetGroup`, add the members you desire,
and add it to the listener by calling `addTargetGroups` instead of `addTargets`.

`addTargets()` will always return the Target Group it just created for you:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
group = listener.add_targets("AppFleet",
    port=443,
    targets=[asg1]
)

group.add_target(asg2)
```

### Using Lambda Targets

To use a Lambda Function as a target, use the integration class in the
`@aws-cdk/aws-elasticloadbalancingv2-targets` package:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_elasticloadbalancingv2_targets as targets

lambda_function = lambda_.Function(...)
lb = elbv2.ApplicationLoadBalancer(...)

listener = lb.add_listener("Listener", port=80)
listener.add_targets("Targets",
    targets=[targets.LambdaTarget(lambda_function)],

    # For Lambda Targets, you need to explicitly enable health checks if you
    # want them.
    health_check=HealthCheck(
        enabled=True
    )
)
```

Only a single Lambda function can be added to a single listener rule.

### Configuring Health Checks

Health checks are configured upon creation of a target group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("AppFleet",
    port=8080,
    targets=[asg],
    health_check={
        "path": "/ping",
        "interval": cdk.Duration.minutes(1)
    }
)
```

The health check can also be configured after creation by calling
`configureHealthCheck()` on the created object.

No attempts are made to configure security groups for the port you're
configuring a health check for, but if the health check is on the same port
you're routing traffic to, the security group already allows the traffic.
If not, you will have to configure the security groups appropriately:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("AppFleet",
    port=8080,
    targets=[asg],
    health_check={
        "port": 8088
    }
)

listener.connections.allow_from(lb, ec2.Port.tcp(8088))
```

### Using a Load Balancer from a different Stack

If you want to put your Load Balancer and the Targets it is load balancing to in
different stacks, you may not be able to use the convenience methods
`loadBalancer.addListener()` and `listener.addTargets()`.

The reason is that these methods will create resources in the same Stack as the
object they're called on, which may lead to cyclic references between stacks.
Instead, you will have to create an `ApplicationListener` in the target stack,
or an empty `TargetGroup` in the load balancer stack that you attach your
service to.

For an example of the alternatives while load balancing to an ECS service, see the
[ecs/cross-stack-load-balancer
example](https://github.com/aws-samples/aws-cdk-examples/tree/master/typescript/ecs/cross-stack-load-balancer/).

### Protocol for Load Balancer Targets

Constructs that want to be a load balancer target should implement
`IApplicationLoadBalancerTarget` and/or `INetworkLoadBalancerTarget`, and
provide an implementation for the function `attachToXxxTargetGroup()`, which can
call functions on the load balancer and should return metadata about the
load balancing target:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
attach_to_application_target_group(target_group, ApplicationTargetGroup)LoadBalancerTargetProps
    target_group.register_connectable(...)return {
        "target_type": TargetType.Instance | TargetType.Ip,
        "target_json": {"id": , ..., "port": , ...}
    }
```

`targetType` should be one of `Instance` or `Ip`. If the target can be
directly added to the target group, `targetJson` should contain the `id` of
the target (either instance ID or IP address depending on the type) and
optionally a `port` or `availabilityZone` override.

Application load balancer targets can call `registerConnectable()` on the
target group to register themselves for addition to the load balancer's security
group rules.

If your load balancer target requires that the TargetGroup has been
associated with a LoadBalancer before registration can happen (such as is the
case for ECS Services for example), take a resource dependency on
`targetGroup.loadBalancerDependency()` as follows:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Make sure that the listener has been created, and so the TargetGroup
# has been associated with the LoadBalancer, before 'resource' is created.
resourced.add_dependency(target_group.load_balancer_dependency())
```

## Looking up Load Balancers and Listeners

You may look up load balancers and load balancer listeners by using one of the
following lookup methods:

* `ApplicationLoadBalancer.fromlookup(options)` - Look up an application load
  balancer.
* `ApplicationListener.fromLookup(options)` - Look up an application load
  balancer listener.
* `NetworkLoadBalancer.fromLookup(options)` - Look up a network load balancer.
* `NetworkListener.fromLookup(options)` - Look up a network load balancer
  listener.

### Load Balancer lookup options

You may look up a load balancer by ARN or by associated tags. When you look a
load balancer up by ARN, that load balancer will be returned unless CDK detects
that the load balancer is of the wrong type. When you look up a load balancer by
tags, CDK will return the load balancer matching all specified tags. If more
than one load balancer matches, CDK will throw an error requesting that you
provide more specific criteria.

**Look up a Application Load Balancer by ARN**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balancer = ApplicationLoadBalancer.from_lookup(stack, "ALB",
    load_balancer_arn=YOUR_ALB_ARN
)
```

**Look up an Application Load Balancer by tags**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balancer = ApplicationLoadBalancer.from_lookup(stack, "ALB",
    load_balancer_tags={
        # Finds a load balancer matching all tags.
        "some": "tag",
        "someother": "tag"
    }
)
```

## Load Balancer Listener lookup options

You may look up a load balancer listener by the following criteria:

* Associated load balancer ARN
* Associated load balancer tags
* Listener ARN
* Listener port
* Listener protocol

The lookup method will return the matching listener. If more than one listener
matches, CDK will throw an error requesting that you specify additional
criteria.

**Look up a Listener by associated Load Balancer, Port, and Protocol**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener = ApplicationListener.from_lookup(stack, "ALBListener",
    load_balancer_arn=YOUR_ALB_ARN,
    listener_protocol=ApplicationProtocol.HTTPS,
    listener_port=443
)
```

**Look up a Listener by associated Load Balancer Tag, Port, and Protocol**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener = ApplicationListener.from_lookup(stack, "ALBListener",
    load_balancer_tags={
        "Cluster": "MyClusterName"
    },
    listener_protocol=ApplicationProtocol.HTTPS,
    listener_port=443
)
```

**Look up a Network Listener by associated Load Balancer Tag, Port, and Protocol**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener = NetworkListener.from_lookup(stack, "ALBListener",
    load_balancer_tags={
        "Cluster": "MyClusterName"
    },
    listener_protocol=Protocol.TCP,
    listener_port=12345
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
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_s3
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddNetworkActionProps",
    jsii_struct_bases=[],
    name_mapping={"action": "action"},
)
class AddNetworkActionProps:
    def __init__(self, *, action: "NetworkListenerAction") -> None:
        """Properties for adding a new action to a listener.

        :param action: Action to perform.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
        }

    @builtins.property
    def action(self) -> "NetworkListenerAction":
        """Action to perform."""
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddNetworkActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddNetworkTargetsProps",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "protocol": "protocol",
        "proxy_protocol_v2": "proxyProtocolV2",
        "target_group_name": "targetGroupName",
        "targets": "targets",
    },
)
class AddNetworkTargetsProps:
    def __init__(
        self,
        *,
        port: jsii.Number,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional["HealthCheck"] = None,
        protocol: typing.Optional["Protocol"] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]] = None,
    ) -> None:
        """Properties for adding new network targets to a listener.

        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param protocol: Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - inherits the protocol of the listener
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.
        """
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if protocol is not None:
            self._values["protocol"] = protocol
        if proxy_protocol_v2 is not None:
            self._values["proxy_protocol_v2"] = proxy_protocol_v2
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests.

        :default: Determined from protocol if known
        """
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return result

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: Duration.minutes(5)
        """
        result = self._values.get("deregistration_delay")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check configuration.

        :default: No health check
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - inherits the protocol of the listener
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def proxy_protocol_v2(self) -> typing.Optional[builtins.bool]:
        """Indicates whether Proxy Protocol version 2 is enabled.

        :default: false
        """
        result = self._values.get("proxy_protocol_v2")
        return result

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: Automatically generated
        """
        result = self._values.get("target_group_name")
        return result

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["INetworkLoadBalancerTarget"]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.
        """
        result = self._values.get("targets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddNetworkTargetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "conditions": "conditions",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "priority": "priority",
    },
)
class AddRuleProps:
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.List["ListenerCondition"]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for adding a conditional load balancing rule.

        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List["ListenerCondition"]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No host condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No path condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults
        """
        result = self._values.get("priority")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "listener_arn": "listenerArn",
        "default_port": "defaultPort",
        "security_group": "securityGroup",
        "security_group_allows_all_outbound": "securityGroupAllowsAllOutbound",
        "security_group_id": "securityGroupId",
    },
)
class ApplicationListenerAttributes:
    def __init__(
        self,
        *,
        listener_arn: builtins.str,
        default_port: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        security_group_allows_all_outbound: typing.Optional[builtins.bool] = None,
        security_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties to reference an existing listener.

        :param listener_arn: ARN of the listener.
        :param default_port: The default port on which this listener is listening.
        :param security_group: Security group of the load balancer this listener is associated with.
        :param security_group_allows_all_outbound: (deprecated) Whether the imported security group allows all outbound traffic or not when imported using ``securityGroupId``. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param security_group_id: (deprecated) Security group ID of the load balancer this listener is associated with.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "listener_arn": listener_arn,
        }
        if default_port is not None:
            self._values["default_port"] = default_port
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_group_allows_all_outbound is not None:
            self._values["security_group_allows_all_outbound"] = security_group_allows_all_outbound
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id

    @builtins.property
    def listener_arn(self) -> builtins.str:
        """ARN of the listener."""
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return result

    @builtins.property
    def default_port(self) -> typing.Optional[jsii.Number]:
        """The default port on which this listener is listening."""
        result = self._values.get("default_port")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security group of the load balancer this listener is associated with."""
        result = self._values.get("security_group")
        return result

    @builtins.property
    def security_group_allows_all_outbound(self) -> typing.Optional[builtins.bool]:
        """(deprecated) Whether the imported security group allows all outbound traffic or not when imported using ``securityGroupId``.

        Unless set to ``false``, no egress rules will be added to the security group.

        :default: true

        :deprecated: use ``securityGroup`` instead

        :stability: deprecated
        """
        result = self._values.get("security_group_allows_all_outbound")
        return result

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        """(deprecated) Security group ID of the load balancer this listener is associated with.

        :deprecated: use ``securityGroup`` instead

        :stability: deprecated
        """
        result = self._values.get("security_group_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationListenerCertificate(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificate",
):
    """Add certificates to a listener."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener: "IApplicationListener",
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List["IListenerCertificate"]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param listener: The listener to attach the rule to.
        :param certificate_arns: (deprecated) ARNs of certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        :param certificates: Certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        """
        props = ApplicationListenerCertificateProps(
            listener=listener,
            certificate_arns=certificate_arns,
            certificates=certificates,
        )

        jsii.create(ApplicationListenerCertificate, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "listener": "listener",
        "certificate_arns": "certificateArns",
        "certificates": "certificates",
    },
)
class ApplicationListenerCertificateProps:
    def __init__(
        self,
        *,
        listener: "IApplicationListener",
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List["IListenerCertificate"]] = None,
    ) -> None:
        """Properties for adding a set of certificates to a listener.

        :param listener: The listener to attach the rule to.
        :param certificate_arns: (deprecated) ARNs of certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        :param certificates: Certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if certificate_arns is not None:
            self._values["certificate_arns"] = certificate_arns
        if certificates is not None:
            self._values["certificates"] = certificates

    @builtins.property
    def listener(self) -> "IApplicationListener":
        """The listener to attach the rule to."""
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return result

    @builtins.property
    def certificate_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) ARNs of certificates to attach.

        Duplicates are not allowed.

        :default: - One of 'certificates' and 'certificateArns' is required.

        :deprecated: Use ``certificates`` instead.

        :stability: deprecated
        """
        result = self._values.get("certificate_arns")
        return result

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificates to attach.

        Duplicates are not allowed.

        :default: - One of 'certificates' and 'certificateArns' is required.
        """
        result = self._values.get("certificates")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationListenerRule(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRule",
):
    """Define a new listener rule."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener: "IApplicationListener",
        priority: jsii.Number,
        action: typing.Optional["ListenerAction"] = None,
        conditions: typing.Optional[typing.List["ListenerCondition"]] = None,
        fixed_response: typing.Optional["FixedResponse"] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        redirect_response: typing.Optional["RedirectResponse"] = None,
        target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param listener: The listener to attach the rule to.
        :param priority: Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param action: Action to perform when requests are received. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No action
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param fixed_response: (deprecated) Fixed response to return. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No fixed response.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Default: - No host condition.
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. Default: - No path condition.
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. Paths may contain up to three '*' wildcards. Default: - No path conditions.
        :param redirect_response: (deprecated) Redirect response to return. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No redirect response.
        :param target_groups: Target groups to forward requests to. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Implies a ``forward`` action. Default: - No target groups.
        """
        props = ApplicationListenerRuleProps(
            listener=listener,
            priority=priority,
            action=action,
            conditions=conditions,
            fixed_response=fixed_response,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            redirect_response=redirect_response,
            target_groups=target_groups,
        )

        jsii.create(ApplicationListenerRule, self, [scope, id, props])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, condition: "ListenerCondition") -> None:
        """Add a non-standard condition to this rule.

        :param condition: -
        """
        return jsii.invoke(self, "addCondition", [condition])

    @jsii.member(jsii_name="addFixedResponse")
    def add_fixed_response(
        self,
        *,
        status_code: builtins.str,
        content_type: typing.Optional["ContentType"] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Add a fixed response.

        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message

        :deprecated: Use configureAction instead

        :stability: deprecated
        """
        fixed_response = FixedResponse(
            status_code=status_code,
            content_type=content_type,
            message_body=message_body,
        )

        return jsii.invoke(self, "addFixedResponse", [fixed_response])

    @jsii.member(jsii_name="addRedirectResponse")
    def add_redirect_response(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Add a redirect response.

        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request

        :deprecated: Use configureAction instead

        :stability: deprecated
        """
        redirect_response = RedirectResponse(
            status_code=status_code,
            host=host,
            path=path,
            port=port,
            protocol=protocol,
            query=query,
        )

        return jsii.invoke(self, "addRedirectResponse", [redirect_response])

    @jsii.member(jsii_name="addTargetGroup")
    def add_target_group(self, target_group: "IApplicationTargetGroup") -> None:
        """(deprecated) Add a TargetGroup to load balance to.

        :param target_group: -

        :deprecated: Use configureAction instead

        :stability: deprecated
        """
        return jsii.invoke(self, "addTargetGroup", [target_group])

    @jsii.member(jsii_name="configureAction")
    def configure_action(self, action: "ListenerAction") -> None:
        """Configure the action to perform for this rule.

        :param action: -
        """
        return jsii.invoke(self, "configureAction", [action])

    @jsii.member(jsii_name="setCondition")
    def set_condition(
        self,
        field: builtins.str,
        values: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """(deprecated) Add a non-standard condition to this rule.

        If the condition conflicts with an already set condition, it will be overwritten by the one you specified.

        :param field: -
        :param values: -

        :deprecated: use ``addCondition`` instead.

        :stability: deprecated
        """
        return jsii.invoke(self, "setCondition", [field, values])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the rule."""
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerRuleArn")
    def listener_rule_arn(self) -> builtins.str:
        """The ARN of this rule."""
        return jsii.get(self, "listenerRuleArn")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "security_group_id": "securityGroupId",
        "load_balancer_canonical_hosted_zone_id": "loadBalancerCanonicalHostedZoneId",
        "load_balancer_dns_name": "loadBalancerDnsName",
        "security_group_allows_all_outbound": "securityGroupAllowsAllOutbound",
        "vpc": "vpc",
    },
)
class ApplicationLoadBalancerAttributes:
    def __init__(
        self,
        *,
        load_balancer_arn: builtins.str,
        security_group_id: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        security_group_allows_all_outbound: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """Properties to reference an existing load balancer.

        :param load_balancer_arn: ARN of the load balancer.
        :param security_group_id: ID of the load balancer's security group.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param security_group_allows_all_outbound: Whether the security group allows all outbound traffic or not. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param vpc: The VPC this load balancer has been created in, if available. Default: - If the Load Balancer was imported and a VPC was not specified, the VPC is not available.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_arn": load_balancer_arn,
            "security_group_id": security_group_id,
        }
        if load_balancer_canonical_hosted_zone_id is not None:
            self._values["load_balancer_canonical_hosted_zone_id"] = load_balancer_canonical_hosted_zone_id
        if load_balancer_dns_name is not None:
            self._values["load_balancer_dns_name"] = load_balancer_dns_name
        if security_group_allows_all_outbound is not None:
            self._values["security_group_allows_all_outbound"] = security_group_allows_all_outbound
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        """ARN of the load balancer."""
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return result

    @builtins.property
    def security_group_id(self) -> builtins.str:
        """ID of the load balancer's security group."""
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return result

    @builtins.property
    def load_balancer_canonical_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        """The canonical hosted zone ID of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        result = self._values.get("load_balancer_canonical_hosted_zone_id")
        return result

    @builtins.property
    def load_balancer_dns_name(self) -> typing.Optional[builtins.str]:
        """The DNS name of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        result = self._values.get("load_balancer_dns_name")
        return result

    @builtins.property
    def security_group_allows_all_outbound(self) -> typing.Optional[builtins.bool]:
        """Whether the security group allows all outbound traffic or not.

        Unless set to ``false``, no egress rules will be added to the security group.

        :default: true
        """
        result = self._values.get("security_group_allows_all_outbound")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in, if available.

        :default:

        - If the Load Balancer was imported and a VPC was not specified,
        the VPC is not available.
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerRedirectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "source_port": "sourcePort",
        "source_protocol": "sourceProtocol",
        "target_port": "targetPort",
        "target_protocol": "targetProtocol",
    },
)
class ApplicationLoadBalancerRedirectConfig:
    def __init__(
        self,
        *,
        source_port: typing.Optional[jsii.Number] = None,
        source_protocol: typing.Optional["ApplicationProtocol"] = None,
        target_port: typing.Optional[jsii.Number] = None,
        target_protocol: typing.Optional["ApplicationProtocol"] = None,
    ) -> None:
        """Properties for a redirection config.

        :param source_port: The port number to listen to. Default: 80
        :param source_protocol: The protocol of the listener being created. Default: HTTP
        :param target_port: The port number to redirect to. Default: 443
        :param target_protocol: The protocol of the redirection target. Default: HTTPS
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if source_port is not None:
            self._values["source_port"] = source_port
        if source_protocol is not None:
            self._values["source_protocol"] = source_protocol
        if target_port is not None:
            self._values["target_port"] = target_port
        if target_protocol is not None:
            self._values["target_protocol"] = target_protocol

    @builtins.property
    def source_port(self) -> typing.Optional[jsii.Number]:
        """The port number to listen to.

        :default: 80
        """
        result = self._values.get("source_port")
        return result

    @builtins.property
    def source_protocol(self) -> typing.Optional["ApplicationProtocol"]:
        """The protocol of the listener being created.

        :default: HTTP
        """
        result = self._values.get("source_protocol")
        return result

    @builtins.property
    def target_port(self) -> typing.Optional[jsii.Number]:
        """The port number to redirect to.

        :default: 443
        """
        result = self._values.get("target_port")
        return result

    @builtins.property
    def target_protocol(self) -> typing.Optional["ApplicationProtocol"]:
        """The protocol of the redirection target.

        :default: HTTPS
        """
        result = self._values.get("target_protocol")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerRedirectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationProtocol")
class ApplicationProtocol(enum.Enum):
    """Load balancing protocol for application load balancers."""

    HTTP = "HTTP"
    """HTTP."""
    HTTPS = "HTTPS"
    """HTTPS."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AuthenticateOidcOptions",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_endpoint": "authorizationEndpoint",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer": "issuer",
        "next": "next",
        "token_endpoint": "tokenEndpoint",
        "user_info_endpoint": "userInfoEndpoint",
        "authentication_request_extra_params": "authenticationRequestExtraParams",
        "on_unauthenticated_request": "onUnauthenticatedRequest",
        "scope": "scope",
        "session_cookie_name": "sessionCookieName",
        "session_timeout": "sessionTimeout",
    },
)
class AuthenticateOidcOptions:
    def __init__(
        self,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: aws_cdk.core.SecretValue,
        issuer: builtins.str,
        next: "ListenerAction",
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional["UnauthenticatedAction"] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Options for ``ListenerAction.authenciateOidc()``.

        :param authorization_endpoint: The authorization endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param client_id: The OAuth 2.0 client identifier.
        :param client_secret: The OAuth 2.0 client secret.
        :param issuer: The OIDC issuer identifier of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param next: What action to execute next.
        :param token_endpoint: The token endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param user_info_endpoint: The user info endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint. Default: - No extra parameters
        :param on_unauthenticated_request: The behavior if the user is not authenticated. Default: UnauthenticatedAction.AUTHENTICATE
        :param scope: The set of user claims to be requested from the IdP. To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP. Default: "openid"
        :param session_cookie_name: The name of the cookie used to maintain session information. Default: "AWSELBAuthSessionCookie"
        :param session_timeout: The maximum duration of the authentication session. Default: Duration.days(7)
        """
        self._values: typing.Dict[str, typing.Any] = {
            "authorization_endpoint": authorization_endpoint,
            "client_id": client_id,
            "client_secret": client_secret,
            "issuer": issuer,
            "next": next,
            "token_endpoint": token_endpoint,
            "user_info_endpoint": user_info_endpoint,
        }
        if authentication_request_extra_params is not None:
            self._values["authentication_request_extra_params"] = authentication_request_extra_params
        if on_unauthenticated_request is not None:
            self._values["on_unauthenticated_request"] = on_unauthenticated_request
        if scope is not None:
            self._values["scope"] = scope
        if session_cookie_name is not None:
            self._values["session_cookie_name"] = session_cookie_name
        if session_timeout is not None:
            self._values["session_timeout"] = session_timeout

    @builtins.property
    def authorization_endpoint(self) -> builtins.str:
        """The authorization endpoint of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.
        """
        result = self._values.get("authorization_endpoint")
        assert result is not None, "Required property 'authorization_endpoint' is missing"
        return result

    @builtins.property
    def client_id(self) -> builtins.str:
        """The OAuth 2.0 client identifier."""
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return result

    @builtins.property
    def client_secret(self) -> aws_cdk.core.SecretValue:
        """The OAuth 2.0 client secret."""
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return result

    @builtins.property
    def issuer(self) -> builtins.str:
        """The OIDC issuer identifier of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.
        """
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return result

    @builtins.property
    def next(self) -> "ListenerAction":
        """What action to execute next."""
        result = self._values.get("next")
        assert result is not None, "Required property 'next' is missing"
        return result

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        """The token endpoint of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.
        """
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return result

    @builtins.property
    def user_info_endpoint(self) -> builtins.str:
        """The user info endpoint of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.
        """
        result = self._values.get("user_info_endpoint")
        assert result is not None, "Required property 'user_info_endpoint' is missing"
        return result

    @builtins.property
    def authentication_request_extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """The query parameters (up to 10) to include in the redirect request to the authorization endpoint.

        :default: - No extra parameters
        """
        result = self._values.get("authentication_request_extra_params")
        return result

    @builtins.property
    def on_unauthenticated_request(self) -> typing.Optional["UnauthenticatedAction"]:
        """The behavior if the user is not authenticated.

        :default: UnauthenticatedAction.AUTHENTICATE
        """
        result = self._values.get("on_unauthenticated_request")
        return result

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        """The set of user claims to be requested from the IdP.

        To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.

        :default: "openid"
        """
        result = self._values.get("scope")
        return result

    @builtins.property
    def session_cookie_name(self) -> typing.Optional[builtins.str]:
        """The name of the cookie used to maintain session information.

        :default: "AWSELBAuthSessionCookie"
        """
        result = self._values.get("session_cookie_name")
        return result

    @builtins.property
    def session_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum duration of the authentication session.

        :default: Duration.days(7)
        """
        result = self._values.get("session_timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthenticateOidcOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arns": "certificateArns",
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "open": "open",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class BaseApplicationListenerProps:
    def __init__(
        self,
        *,
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List["IListenerCertificate"]] = None,
        default_action: typing.Optional["ListenerAction"] = None,
        default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> None:
        """Basic properties for an ApplicationListener.

        :param certificate_arns: (deprecated) The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if certificate_arns is not None:
            self._values["certificate_arns"] = certificate_arns
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if open is not None:
            self._values["open"] = open
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def certificate_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) The certificates to use on this listener.

        :default: - No certificates.

        :deprecated: Use the ``certificates`` property instead

        :stability: deprecated
        """
        result = self._values.get("certificate_arns")
        return result

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificate list of ACM cert ARNs.

        :default: - No certificates.
        """
        result = self._values.get("certificates")
        return result

    @builtins.property
    def default_action(self) -> typing.Optional["ListenerAction"]:
        """Default action to take for requests to this listener.

        This allows full control of the default action of the load balancer,
        including Action chaining, fixed responses and redirect responses.

        See the ``ListenerAction`` class for all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.
        """
        result = self._values.get("default_action")
        return result

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.
        """
        result = self._values.get("default_target_groups")
        return result

    @builtins.property
    def open(self) -> typing.Optional[builtins.bool]:
        """Allow anyone to connect to this listener.

        If this is specified, the listener will be opened up to anyone who can reach it.
        For internal load balancers this is anyone in the same VPC. For public load
        balancers, this is anyone on the internet.

        If you want to be more selective about who can access this load
        balancer, set this to ``false`` and use the listener's ``connections``
        object to selectively grant access to the listener.

        :default: true
        """
        result = self._values.get("open")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        :default: - Determined from protocol if known.
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        """The protocol to use.

        :default: - Determined from port if known.
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        """The security policy that defines which ciphers and protocols are supported.

        :default: - The current predefined security policy.
        """
        result = self._values.get("ssl_policy")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseApplicationListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "action": "action",
        "conditions": "conditions",
        "fixed_response": "fixedResponse",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "redirect_response": "redirectResponse",
        "target_groups": "targetGroups",
    },
)
class BaseApplicationListenerRuleProps:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        action: typing.Optional["ListenerAction"] = None,
        conditions: typing.Optional[typing.List["ListenerCondition"]] = None,
        fixed_response: typing.Optional["FixedResponse"] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        redirect_response: typing.Optional["RedirectResponse"] = None,
        target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
    ) -> None:
        """Basic properties for defining a rule on a listener.

        :param priority: Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param action: Action to perform when requests are received. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No action
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param fixed_response: (deprecated) Fixed response to return. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No fixed response.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Default: - No host condition.
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. Default: - No path condition.
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. Paths may contain up to three '*' wildcards. Default: - No path conditions.
        :param redirect_response: (deprecated) Redirect response to return. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No redirect response.
        :param target_groups: Target groups to forward requests to. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Implies a ``forward`` action. Default: - No target groups.
        """
        if isinstance(fixed_response, dict):
            fixed_response = FixedResponse(**fixed_response)
        if isinstance(redirect_response, dict):
            redirect_response = RedirectResponse(**redirect_response)
        self._values: typing.Dict[str, typing.Any] = {
            "priority": priority,
        }
        if action is not None:
            self._values["action"] = action
        if conditions is not None:
            self._values["conditions"] = conditions
        if fixed_response is not None:
            self._values["fixed_response"] = fixed_response
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if redirect_response is not None:
            self._values["redirect_response"] = redirect_response
        if target_groups is not None:
            self._values["target_groups"] = target_groups

    @builtins.property
    def priority(self) -> jsii.Number:
        """Priority of the rule.

        The rule with the lowest priority will be used for every request.

        Priorities must be unique.
        """
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return result

    @builtins.property
    def action(self) -> typing.Optional["ListenerAction"]:
        """Action to perform when requests are received.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No action
        """
        result = self._values.get("action")
        return result

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List["ListenerCondition"]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def fixed_response(self) -> typing.Optional["FixedResponse"]:
        """(deprecated) Fixed response to return.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No fixed response.

        :deprecated: Use ``action`` instead.

        :stability: deprecated
        """
        result = self._values.get("fixed_response")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        :default: - No host condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        Paths may contain up to three '*' wildcards.

        :default: - No path conditions.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def redirect_response(self) -> typing.Optional["RedirectResponse"]:
        """(deprecated) Redirect response to return.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No redirect response.

        :deprecated: Use ``action`` instead.

        :stability: deprecated
        """
        result = self._values.get("redirect_response")
        return result

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Target groups to forward requests to.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        Implies a ``forward`` action.

        :default: - No target groups.
        """
        result = self._values.get("target_groups")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseApplicationListenerRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseListener(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseListener",
):
    """Base class for listeners."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BaseListenerProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        additional_props: typing.Any,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param additional_props: -
        """
        jsii.create(BaseListener, self, [scope, id, additional_props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate this listener."""
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        """
        :attribute: true
        """
        return jsii.get(self, "listenerArn")


class _BaseListenerProxy(
    BaseListener, jsii.proxy_for(aws_cdk.core.Resource) # type: ignore
):
    pass


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseListenerLookupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "listener_port": "listenerPort",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class BaseListenerLookupOptions:
    def __init__(
        self,
        *,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Options for listener lookup.

        :param listener_port: Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Filter listeners by listener port.

        :default: - does not filter by listener port
        """
        result = self._values.get("listener_port")
        return result

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Filter listeners by associated load balancer arn.

        :default: - does not filter by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Filter listeners by associated load balancer tags.

        :default: - does not filter by load balancer tags
        """
        result = self._values.get("load_balancer_tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseListenerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseLoadBalancer(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancer",
):
    """Base class for both Application and Network Load Balancers."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BaseLoadBalancerProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        base_props: "BaseLoadBalancerProps",
        additional_props: typing.Any,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param base_props: -
        :param additional_props: -
        """
        jsii.create(BaseLoadBalancer, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(
        self,
        bucket: aws_cdk.aws_s3.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        """Enable access logging for this load balancer.

        A region must be specified on the stack containing the load balancer; you cannot enable logging on
        environment-agnostic stacks. See https://docs.aws.amazon.com/cdk/latest/guide/environments.html

        :param bucket: -
        :param prefix: -
        """
        return jsii.invoke(self, "logAccessLogs", [bucket, prefix])

    @jsii.member(jsii_name="removeAttribute")
    def remove_attribute(self, key: builtins.str) -> None:
        """Remove an attribute from the load balancer.

        :param key: -
        """
        return jsii.invoke(self, "removeAttribute", [key])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(
        self,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        """Set a non-standard attribute on the load balancer.

        :param key: -
        :param value: -

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#load-balancer-attributes
        """
        return jsii.invoke(self, "setAttribute", [key, value])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        """The ARN of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            arn:aws:elasticloadbalancing:us-west-2123456789012loadbalancer / app / my - internal - load - balancer / 50dc6c495c0c9188
        """
        return jsii.get(self, "loadBalancerArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> builtins.str:
        """The canonical hosted zone ID of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        """The DNS name of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        """
        return jsii.get(self, "loadBalancerDnsName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerFullName")
    def load_balancer_full_name(self) -> builtins.str:
        """The full name of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 50dc6c495c0c9188
        """
        return jsii.get(self, "loadBalancerFullName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> builtins.str:
        """The name of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer
        """
        return jsii.get(self, "loadBalancerName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerSecurityGroups")
    def load_balancer_security_groups(self) -> typing.List[builtins.str]:
        """
        :attribute: true
        """
        return jsii.get(self, "loadBalancerSecurityGroups")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC this load balancer has been created in."""
        return jsii.get(self, "vpc")


class _BaseLoadBalancerProxy(
    BaseLoadBalancer, jsii.proxy_for(aws_cdk.core.Resource) # type: ignore
):
    pass


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancerLookupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class BaseLoadBalancerLookupOptions:
    def __init__(
        self,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Options for looking up load balancers.

        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Find by load balancer's ARN.

        :default: - does not search by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
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
        return "BaseLoadBalancerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "deletion_protection": "deletionProtection",
        "internet_facing": "internetFacing",
        "load_balancer_name": "loadBalancerName",
        "vpc_subnets": "vpcSubnets",
    },
)
class BaseLoadBalancerProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Shared properties of both Application and Network Load Balancers.

        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Which subnets place the load balancer in. Default: - the Vpc default strategy.
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC network to place the load balancer in."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        """Indicates whether deletion protection is enabled.

        :default: false
        """
        result = self._values.get("deletion_protection")
        return result

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        """Whether the load balancer has an internet-routable address.

        :default: false
        """
        result = self._values.get("internet_facing")
        return result

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        """Name of the load balancer.

        :default: - Automatically generated name.
        """
        result = self._values.get("load_balancer_name")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Which subnets place the load balancer in.

        :default: - the Vpc default strategy.
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseNetworkListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class BaseNetworkListenerProps:
    def __init__(
        self,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.List["IListenerCertificate"]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> None:
        """Basic properties for a Network Listener.

        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests."""
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return result

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        """Certificate list of ACM cert ARNs.

        :default: - No certificates.
        """
        result = self._values.get("certificates")
        return result

    @builtins.property
    def default_action(self) -> typing.Optional["NetworkListenerAction"]:
        """Default action to take for requests to this listener.

        This allows full control of the default Action of the load balancer,
        including weighted forwarding. See the ``NetworkListenerAction`` class for
        all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.
        """
        result = self._values.get("default_action")
        return result

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["INetworkTargetGroup"]]:
        """Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.
        """
        result = self._values.get("default_target_groups")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - TLS if certificates are provided. TCP otherwise.
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        """SSL Policy.

        :default: - Current predefined security policy.
        """
        result = self._values.get("ssl_policy")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseNetworkListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseTargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "target_group_name": "targetGroupName",
        "target_type": "targetType",
        "vpc": "vpc",
    },
)
class BaseTargetGroupProps:
    def __init__(
        self,
        *,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional["HealthCheck"] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional["TargetType"] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """Basic properties of both Application and Network Target Groups.

        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        """
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if target_type is not None:
            self._values["target_type"] = target_type
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: 300
        """
        result = self._values.get("deregistration_delay")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check configuration.

        :default: - None.
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: - Automatically generated.
        """
        result = self._values.get("target_group_name")
        return result

    @builtins.property
    def target_type(self) -> typing.Optional["TargetType"]:
        """The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        :default: - Determined automatically.
        """
        result = self._values.get("target_type")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        :default: - undefined
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListener(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener",
):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::Listener``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::Listener
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        default_actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnListener.ActionProperty", aws_cdk.core.IResolvable]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.CertificateProperty"]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_actions: ``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.
        :param load_balancer_arn: ``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.
        :param alpn_policy: ``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.
        :param certificates: ``AWS::ElasticLoadBalancingV2::Listener.Certificates``.
        :param port: ``AWS::ElasticLoadBalancingV2::Listener.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::Listener.Protocol``.
        :param ssl_policy: ``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.
        """
        props = CfnListenerProps(
            default_actions=default_actions,
            load_balancer_arn=load_balancer_arn,
            alpn_policy=alpn_policy,
            certificates=certificates,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        jsii.create(CfnListener, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrListenerArn")
    def attr_listener_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ListenerArn
        """
        return jsii.get(self, "attrListenerArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultActions")
    def default_actions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnListener.ActionProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
        """
        return jsii.get(self, "defaultActions")

    @default_actions.setter # type: ignore
    def default_actions(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnListener.ActionProperty", aws_cdk.core.IResolvable]]],
    ) -> None:
        jsii.set(self, "defaultActions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        """``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
        """
        return jsii.get(self, "loadBalancerArn")

    @load_balancer_arn.setter # type: ignore
    def load_balancer_arn(self, value: builtins.str) -> None:
        jsii.set(self, "loadBalancerArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="alpnPolicy")
    def alpn_policy(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-alpnpolicy
        """
        return jsii.get(self, "alpnPolicy")

    @alpn_policy.setter # type: ignore
    def alpn_policy(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "alpnPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificates")
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.CertificateProperty"]]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.Certificates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
        """
        return jsii.get(self, "certificates")

    @certificates.setter # type: ignore
    def certificates(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.CertificateProperty"]]]],
    ) -> None:
        jsii.set(self, "certificates", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::Listener.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
        """
        return jsii.get(self, "port")

    @port.setter # type: ignore
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::Listener.Protocol``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter # type: ignore
    def protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
        """
        return jsii.get(self, "sslPolicy")

    @ssl_policy.setter # type: ignore
    def ssl_policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sslPolicy", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "authenticate_cognito_config": "authenticateCognitoConfig",
            "authenticate_oidc_config": "authenticateOidcConfig",
            "fixed_response_config": "fixedResponseConfig",
            "forward_config": "forwardConfig",
            "order": "order",
            "redirect_config": "redirectConfig",
            "target_group_arn": "targetGroupArn",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            authenticate_cognito_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.AuthenticateCognitoConfigProperty"]] = None,
            authenticate_oidc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.AuthenticateOidcConfigProperty"]] = None,
            fixed_response_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.FixedResponseConfigProperty"]] = None,
            forward_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.ForwardConfigProperty"]] = None,
            order: typing.Optional[jsii.Number] = None,
            redirect_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.RedirectConfigProperty"]] = None,
            target_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param type: ``CfnListener.ActionProperty.Type``.
            :param authenticate_cognito_config: ``CfnListener.ActionProperty.AuthenticateCognitoConfig``.
            :param authenticate_oidc_config: ``CfnListener.ActionProperty.AuthenticateOidcConfig``.
            :param fixed_response_config: ``CfnListener.ActionProperty.FixedResponseConfig``.
            :param forward_config: ``CfnListener.ActionProperty.ForwardConfig``.
            :param order: ``CfnListener.ActionProperty.Order``.
            :param redirect_config: ``CfnListener.ActionProperty.RedirectConfig``.
            :param target_group_arn: ``CfnListener.ActionProperty.TargetGroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if authenticate_cognito_config is not None:
                self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None:
                self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None:
                self._values["fixed_response_config"] = fixed_response_config
            if forward_config is not None:
                self._values["forward_config"] = forward_config
            if order is not None:
                self._values["order"] = order
            if redirect_config is not None:
                self._values["redirect_config"] = redirect_config
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnListener.ActionProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def authenticate_cognito_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.AuthenticateCognitoConfigProperty"]]:
            """``CfnListener.ActionProperty.AuthenticateCognitoConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-authenticatecognitoconfig
            """
            result = self._values.get("authenticate_cognito_config")
            return result

        @builtins.property
        def authenticate_oidc_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.AuthenticateOidcConfigProperty"]]:
            """``CfnListener.ActionProperty.AuthenticateOidcConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-authenticateoidcconfig
            """
            result = self._values.get("authenticate_oidc_config")
            return result

        @builtins.property
        def fixed_response_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.FixedResponseConfigProperty"]]:
            """``CfnListener.ActionProperty.FixedResponseConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-fixedresponseconfig
            """
            result = self._values.get("fixed_response_config")
            return result

        @builtins.property
        def forward_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.ForwardConfigProperty"]]:
            """``CfnListener.ActionProperty.ForwardConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-forwardconfig
            """
            result = self._values.get("forward_config")
            return result

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            """``CfnListener.ActionProperty.Order``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-order
            """
            result = self._values.get("order")
            return result

        @builtins.property
        def redirect_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.RedirectConfigProperty"]]:
            """``CfnListener.ActionProperty.RedirectConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-redirectconfig
            """
            result = self._values.get("redirect_config")
            return result

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            """``CfnListener.ActionProperty.TargetGroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-targetgrouparn
            """
            result = self._values.get("target_group_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateCognitoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "user_pool_arn": "userPoolArn",
            "user_pool_client_id": "userPoolClientId",
            "user_pool_domain": "userPoolDomain",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
        },
    )
    class AuthenticateCognitoConfigProperty:
        def __init__(
            self,
            *,
            user_pool_arn: builtins.str,
            user_pool_client_id: builtins.str,
            user_pool_domain: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param user_pool_arn: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolArn``.
            :param user_pool_client_id: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolClientId``.
            :param user_pool_domain: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolDomain``.
            :param authentication_request_extra_params: ``CfnListener.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListener.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListener.AuthenticateCognitoConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListener.AuthenticateCognitoConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListener.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "user_pool_arn": user_pool_arn,
                "user_pool_client_id": user_pool_client_id,
                "user_pool_domain": user_pool_domain,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout

        @builtins.property
        def user_pool_arn(self) -> builtins.str:
            """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolarn
            """
            result = self._values.get("user_pool_arn")
            assert result is not None, "Required property 'user_pool_arn' is missing"
            return result

        @builtins.property
        def user_pool_client_id(self) -> builtins.str:
            """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolClientId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolclientid
            """
            result = self._values.get("user_pool_client_id")
            assert result is not None, "Required property 'user_pool_client_id' is missing"
            return result

        @builtins.property
        def user_pool_domain(self) -> builtins.str:
            """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolDomain``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpooldomain
            """
            result = self._values.get("user_pool_domain")
            assert result is not None, "Required property 'user_pool_domain' is missing"
            return result

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnListener.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-authenticationrequestextraparams
            """
            result = self._values.get("authentication_request_extra_params")
            return result

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-onunauthenticatedrequest
            """
            result = self._values.get("on_unauthenticated_request")
            return result

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateCognitoConfigProperty.Scope``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-scope
            """
            result = self._values.get("scope")
            return result

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateCognitoConfigProperty.SessionCookieName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessioncookiename
            """
            result = self._values.get("session_cookie_name")
            return result

        @builtins.property
        def session_timeout(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessiontimeout
            """
            result = self._values.get("session_timeout")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateCognitoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateOidcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_endpoint": "authorizationEndpoint",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "issuer": "issuer",
            "token_endpoint": "tokenEndpoint",
            "user_info_endpoint": "userInfoEndpoint",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
        },
    )
    class AuthenticateOidcConfigProperty:
        def __init__(
            self,
            *,
            authorization_endpoint: builtins.str,
            client_id: builtins.str,
            client_secret: builtins.str,
            issuer: builtins.str,
            token_endpoint: builtins.str,
            user_info_endpoint: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param authorization_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.
            :param client_id: ``CfnListener.AuthenticateOidcConfigProperty.ClientId``.
            :param client_secret: ``CfnListener.AuthenticateOidcConfigProperty.ClientSecret``.
            :param issuer: ``CfnListener.AuthenticateOidcConfigProperty.Issuer``.
            :param token_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.TokenEndpoint``.
            :param user_info_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.UserInfoEndpoint``.
            :param authentication_request_extra_params: ``CfnListener.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListener.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListener.AuthenticateOidcConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListener.AuthenticateOidcConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListener.AuthenticateOidcConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "authorization_endpoint": authorization_endpoint,
                "client_id": client_id,
                "client_secret": client_secret,
                "issuer": issuer,
                "token_endpoint": token_endpoint,
                "user_info_endpoint": user_info_endpoint,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout

        @builtins.property
        def authorization_endpoint(self) -> builtins.str:
            """``CfnListener.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authorizationendpoint
            """
            result = self._values.get("authorization_endpoint")
            assert result is not None, "Required property 'authorization_endpoint' is missing"
            return result

        @builtins.property
        def client_id(self) -> builtins.str:
            """``CfnListener.AuthenticateOidcConfigProperty.ClientId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientid
            """
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return result

        @builtins.property
        def client_secret(self) -> builtins.str:
            """``CfnListener.AuthenticateOidcConfigProperty.ClientSecret``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientsecret
            """
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return result

        @builtins.property
        def issuer(self) -> builtins.str:
            """``CfnListener.AuthenticateOidcConfigProperty.Issuer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-issuer
            """
            result = self._values.get("issuer")
            assert result is not None, "Required property 'issuer' is missing"
            return result

        @builtins.property
        def token_endpoint(self) -> builtins.str:
            """``CfnListener.AuthenticateOidcConfigProperty.TokenEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-tokenendpoint
            """
            result = self._values.get("token_endpoint")
            assert result is not None, "Required property 'token_endpoint' is missing"
            return result

        @builtins.property
        def user_info_endpoint(self) -> builtins.str:
            """``CfnListener.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-userinfoendpoint
            """
            result = self._values.get("user_info_endpoint")
            assert result is not None, "Required property 'user_info_endpoint' is missing"
            return result

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnListener.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authenticationrequestextraparams
            """
            result = self._values.get("authentication_request_extra_params")
            return result

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-onunauthenticatedrequest
            """
            result = self._values.get("on_unauthenticated_request")
            return result

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateOidcConfigProperty.Scope``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-scope
            """
            result = self._values.get("scope")
            return result

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateOidcConfigProperty.SessionCookieName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessioncookiename
            """
            result = self._values.get("session_cookie_name")
            return result

        @builtins.property
        def session_timeout(self) -> typing.Optional[builtins.str]:
            """``CfnListener.AuthenticateOidcConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessiontimeout
            """
            result = self._values.get("session_timeout")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateOidcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.CertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param certificate_arn: ``CfnListener.CertificateProperty.CertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            """``CfnListener.CertificateProperty.CertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificate.html#cfn-elasticloadbalancingv2-listener-certificate-certificatearn
            """
            result = self._values.get("certificate_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.FixedResponseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "content_type": "contentType",
            "message_body": "messageBody",
        },
    )
    class FixedResponseConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            content_type: typing.Optional[builtins.str] = None,
            message_body: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param status_code: ``CfnListener.FixedResponseConfigProperty.StatusCode``.
            :param content_type: ``CfnListener.FixedResponseConfigProperty.ContentType``.
            :param message_body: ``CfnListener.FixedResponseConfigProperty.MessageBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if content_type is not None:
                self._values["content_type"] = content_type
            if message_body is not None:
                self._values["message_body"] = message_body

        @builtins.property
        def status_code(self) -> builtins.str:
            """``CfnListener.FixedResponseConfigProperty.StatusCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-statuscode
            """
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return result

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            """``CfnListener.FixedResponseConfigProperty.ContentType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-contenttype
            """
            result = self._values.get("content_type")
            return result

        @builtins.property
        def message_body(self) -> typing.Optional[builtins.str]:
            """``CfnListener.FixedResponseConfigProperty.MessageBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-messagebody
            """
            result = self._values.get("message_body")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.ForwardConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_groups": "targetGroups",
            "target_group_stickiness_config": "targetGroupStickinessConfig",
        },
    )
    class ForwardConfigProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.TargetGroupTupleProperty"]]]] = None,
            target_group_stickiness_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.TargetGroupStickinessConfigProperty"]] = None,
        ) -> None:
            """
            :param target_groups: ``CfnListener.ForwardConfigProperty.TargetGroups``.
            :param target_group_stickiness_config: ``CfnListener.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if target_group_stickiness_config is not None:
                self._values["target_group_stickiness_config"] = target_group_stickiness_config

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.TargetGroupTupleProperty"]]]]:
            """``CfnListener.ForwardConfigProperty.TargetGroups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html#cfn-elasticloadbalancingv2-listener-forwardconfig-targetgroups
            """
            result = self._values.get("target_groups")
            return result

        @builtins.property
        def target_group_stickiness_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListener.TargetGroupStickinessConfigProperty"]]:
            """``CfnListener.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html#cfn-elasticloadbalancingv2-listener-forwardconfig-targetgroupstickinessconfig
            """
            result = self._values.get("target_group_stickiness_config")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.RedirectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "host": "host",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "query": "query",
        },
    )
    class RedirectConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            host: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            query: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param status_code: ``CfnListener.RedirectConfigProperty.StatusCode``.
            :param host: ``CfnListener.RedirectConfigProperty.Host``.
            :param path: ``CfnListener.RedirectConfigProperty.Path``.
            :param port: ``CfnListener.RedirectConfigProperty.Port``.
            :param protocol: ``CfnListener.RedirectConfigProperty.Protocol``.
            :param query: ``CfnListener.RedirectConfigProperty.Query``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if host is not None:
                self._values["host"] = host
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if query is not None:
                self._values["query"] = query

        @builtins.property
        def status_code(self) -> builtins.str:
            """``CfnListener.RedirectConfigProperty.StatusCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-statuscode
            """
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return result

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            """``CfnListener.RedirectConfigProperty.Host``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-host
            """
            result = self._values.get("host")
            return result

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            """``CfnListener.RedirectConfigProperty.Path``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-path
            """
            result = self._values.get("path")
            return result

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            """``CfnListener.RedirectConfigProperty.Port``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-port
            """
            result = self._values.get("port")
            return result

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            """``CfnListener.RedirectConfigProperty.Protocol``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-protocol
            """
            result = self._values.get("protocol")
            return result

        @builtins.property
        def query(self) -> typing.Optional[builtins.str]:
            """``CfnListener.RedirectConfigProperty.Query``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-query
            """
            result = self._values.get("query")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.TargetGroupStickinessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_seconds": "durationSeconds", "enabled": "enabled"},
    )
    class TargetGroupStickinessConfigProperty:
        def __init__(
            self,
            *,
            duration_seconds: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param duration_seconds: ``CfnListener.TargetGroupStickinessConfigProperty.DurationSeconds``.
            :param enabled: ``CfnListener.TargetGroupStickinessConfigProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_seconds is not None:
                self._values["duration_seconds"] = duration_seconds
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def duration_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnListener.TargetGroupStickinessConfigProperty.DurationSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listener-targetgroupstickinessconfig-durationseconds
            """
            result = self._values.get("duration_seconds")
            return result

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnListener.TargetGroupStickinessConfigProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listener-targetgroupstickinessconfig-enabled
            """
            result = self._values.get("enabled")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupStickinessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.TargetGroupTupleProperty",
        jsii_struct_bases=[],
        name_mapping={"target_group_arn": "targetGroupArn", "weight": "weight"},
    )
    class TargetGroupTupleProperty:
        def __init__(
            self,
            *,
            target_group_arn: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param target_group_arn: ``CfnListener.TargetGroupTupleProperty.TargetGroupArn``.
            :param weight: ``CfnListener.TargetGroupTupleProperty.Weight``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            """``CfnListener.TargetGroupTupleProperty.TargetGroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html#cfn-elasticloadbalancingv2-listener-targetgrouptuple-targetgrouparn
            """
            result = self._values.get("target_group_arn")
            return result

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            """``CfnListener.TargetGroupTupleProperty.Weight``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html#cfn-elasticloadbalancingv2-listener-targetgrouptuple-weight
            """
            result = self._values.get("weight")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListenerCertificate(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate",
):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::ListenerCertificate
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificates: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerCertificate.CertificateProperty"]]],
        listener_arn: builtins.str,
    ) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificates: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.
        """
        props = CfnListenerCertificateProps(
            certificates=certificates, listener_arn=listener_arn
        )

        jsii.create(CfnListenerCertificate, self, [scope, id, props])

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
    @jsii.member(jsii_name="certificates")
    def certificates(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerCertificate.CertificateProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
        """
        return jsii.get(self, "certificates")

    @certificates.setter # type: ignore
    def certificates(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerCertificate.CertificateProperty"]]],
    ) -> None:
        jsii.set(self, "certificates", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
        """
        return jsii.get(self, "listenerArn")

    @listener_arn.setter # type: ignore
    def listener_arn(self, value: builtins.str) -> None:
        jsii.set(self, "listenerArn", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate.CertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param certificate_arn: ``CfnListenerCertificate.CertificateProperty.CertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            """``CfnListenerCertificate.CertificateProperty.CertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html#cfn-elasticloadbalancingv2-listener-certificates-certificatearn
            """
            result = self._values.get("certificate_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificateProps",
    jsii_struct_bases=[],
    name_mapping={"certificates": "certificates", "listener_arn": "listenerArn"},
)
class CfnListenerCertificateProps:
    def __init__(
        self,
        *,
        certificates: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListenerCertificate.CertificateProperty]]],
        listener_arn: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        :param certificates: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "certificates": certificates,
            "listener_arn": listener_arn,
        }

    @builtins.property
    def certificates(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListenerCertificate.CertificateProperty]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
        """
        result = self._values.get("certificates")
        assert result is not None, "Required property 'certificates' is missing"
        return result

    @builtins.property
    def listener_arn(self) -> builtins.str:
        """``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
        """
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_actions": "defaultActions",
        "load_balancer_arn": "loadBalancerArn",
        "alpn_policy": "alpnPolicy",
        "certificates": "certificates",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class CfnListenerProps:
    def __init__(
        self,
        *,
        default_actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnListener.ActionProperty, aws_cdk.core.IResolvable]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListener.CertificateProperty]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::Listener``.

        :param default_actions: ``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.
        :param load_balancer_arn: ``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.
        :param alpn_policy: ``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.
        :param certificates: ``AWS::ElasticLoadBalancingV2::Listener.Certificates``.
        :param port: ``AWS::ElasticLoadBalancingV2::Listener.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::Listener.Protocol``.
        :param ssl_policy: ``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "default_actions": default_actions,
            "load_balancer_arn": load_balancer_arn,
        }
        if alpn_policy is not None:
            self._values["alpn_policy"] = alpn_policy
        if certificates is not None:
            self._values["certificates"] = certificates
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def default_actions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnListener.ActionProperty, aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
        """
        result = self._values.get("default_actions")
        assert result is not None, "Required property 'default_actions' is missing"
        return result

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        """``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
        """
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return result

    @builtins.property
    def alpn_policy(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-alpnpolicy
        """
        result = self._values.get("alpn_policy")
        return result

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListener.CertificateProperty]]]]:
        """``AWS::ElasticLoadBalancingV2::Listener.Certificates``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
        """
        result = self._values.get("certificates")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::Listener.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::Listener.Protocol``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
        """
        result = self._values.get("ssl_policy")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListenerRule(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule",
):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerRule``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::ListenerRule
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.ActionProperty"]]],
        conditions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.RuleConditionProperty"]]],
        listener_arn: builtins.str,
        priority: jsii.Number,
    ) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param actions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.
        :param conditions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.
        :param priority: ``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.
        """
        props = CfnListenerRuleProps(
            actions=actions,
            conditions=conditions,
            listener_arn=listener_arn,
            priority=priority,
        )

        jsii.create(CfnListenerRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.ActionProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
        """
        return jsii.get(self, "actions")

    @actions.setter # type: ignore
    def actions(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.ActionProperty"]]],
    ) -> None:
        jsii.set(self, "actions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.RuleConditionProperty"]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
        """
        return jsii.get(self, "conditions")

    @conditions.setter # type: ignore
    def conditions(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.RuleConditionProperty"]]],
    ) -> None:
        jsii.set(self, "conditions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
        """
        return jsii.get(self, "listenerArn")

    @listener_arn.setter # type: ignore
    def listener_arn(self, value: builtins.str) -> None:
        jsii.set(self, "listenerArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
        """
        return jsii.get(self, "priority")

    @priority.setter # type: ignore
    def priority(self, value: jsii.Number) -> None:
        jsii.set(self, "priority", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "authenticate_cognito_config": "authenticateCognitoConfig",
            "authenticate_oidc_config": "authenticateOidcConfig",
            "fixed_response_config": "fixedResponseConfig",
            "forward_config": "forwardConfig",
            "order": "order",
            "redirect_config": "redirectConfig",
            "target_group_arn": "targetGroupArn",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            authenticate_cognito_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.AuthenticateCognitoConfigProperty"]] = None,
            authenticate_oidc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.AuthenticateOidcConfigProperty"]] = None,
            fixed_response_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.FixedResponseConfigProperty"]] = None,
            forward_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.ForwardConfigProperty"]] = None,
            order: typing.Optional[jsii.Number] = None,
            redirect_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.RedirectConfigProperty"]] = None,
            target_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param type: ``CfnListenerRule.ActionProperty.Type``.
            :param authenticate_cognito_config: ``CfnListenerRule.ActionProperty.AuthenticateCognitoConfig``.
            :param authenticate_oidc_config: ``CfnListenerRule.ActionProperty.AuthenticateOidcConfig``.
            :param fixed_response_config: ``CfnListenerRule.ActionProperty.FixedResponseConfig``.
            :param forward_config: ``CfnListenerRule.ActionProperty.ForwardConfig``.
            :param order: ``CfnListenerRule.ActionProperty.Order``.
            :param redirect_config: ``CfnListenerRule.ActionProperty.RedirectConfig``.
            :param target_group_arn: ``CfnListenerRule.ActionProperty.TargetGroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if authenticate_cognito_config is not None:
                self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None:
                self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None:
                self._values["fixed_response_config"] = fixed_response_config
            if forward_config is not None:
                self._values["forward_config"] = forward_config
            if order is not None:
                self._values["order"] = order
            if redirect_config is not None:
                self._values["redirect_config"] = redirect_config
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnListenerRule.ActionProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listener-actions-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def authenticate_cognito_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.AuthenticateCognitoConfigProperty"]]:
            """``CfnListenerRule.ActionProperty.AuthenticateCognitoConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticatecognitoconfig
            """
            result = self._values.get("authenticate_cognito_config")
            return result

        @builtins.property
        def authenticate_oidc_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.AuthenticateOidcConfigProperty"]]:
            """``CfnListenerRule.ActionProperty.AuthenticateOidcConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticateoidcconfig
            """
            result = self._values.get("authenticate_oidc_config")
            return result

        @builtins.property
        def fixed_response_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.FixedResponseConfigProperty"]]:
            """``CfnListenerRule.ActionProperty.FixedResponseConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-fixedresponseconfig
            """
            result = self._values.get("fixed_response_config")
            return result

        @builtins.property
        def forward_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.ForwardConfigProperty"]]:
            """``CfnListenerRule.ActionProperty.ForwardConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-forwardconfig
            """
            result = self._values.get("forward_config")
            return result

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.ActionProperty.Order``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-order
            """
            result = self._values.get("order")
            return result

        @builtins.property
        def redirect_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.RedirectConfigProperty"]]:
            """``CfnListenerRule.ActionProperty.RedirectConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-redirectconfig
            """
            result = self._values.get("redirect_config")
            return result

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.ActionProperty.TargetGroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listener-actions-targetgrouparn
            """
            result = self._values.get("target_group_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateCognitoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "user_pool_arn": "userPoolArn",
            "user_pool_client_id": "userPoolClientId",
            "user_pool_domain": "userPoolDomain",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
        },
    )
    class AuthenticateCognitoConfigProperty:
        def __init__(
            self,
            *,
            user_pool_arn: builtins.str,
            user_pool_client_id: builtins.str,
            user_pool_domain: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param user_pool_arn: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolArn``.
            :param user_pool_client_id: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolClientId``.
            :param user_pool_domain: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolDomain``.
            :param authentication_request_extra_params: ``CfnListenerRule.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListenerRule.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListenerRule.AuthenticateCognitoConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "user_pool_arn": user_pool_arn,
                "user_pool_client_id": user_pool_client_id,
                "user_pool_domain": user_pool_domain,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout

        @builtins.property
        def user_pool_arn(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolarn
            """
            result = self._values.get("user_pool_arn")
            assert result is not None, "Required property 'user_pool_arn' is missing"
            return result

        @builtins.property
        def user_pool_client_id(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolClientId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolclientid
            """
            result = self._values.get("user_pool_client_id")
            assert result is not None, "Required property 'user_pool_client_id' is missing"
            return result

        @builtins.property
        def user_pool_domain(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolDomain``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpooldomain
            """
            result = self._values.get("user_pool_domain")
            assert result is not None, "Required property 'user_pool_domain' is missing"
            return result

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-authenticationrequestextraparams
            """
            result = self._values.get("authentication_request_extra_params")
            return result

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-onunauthenticatedrequest
            """
            result = self._values.get("on_unauthenticated_request")
            return result

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.Scope``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-scope
            """
            result = self._values.get("scope")
            return result

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionCookieName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessioncookiename
            """
            result = self._values.get("session_cookie_name")
            return result

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessiontimeout
            """
            result = self._values.get("session_timeout")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateCognitoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateOidcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_endpoint": "authorizationEndpoint",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "issuer": "issuer",
            "token_endpoint": "tokenEndpoint",
            "user_info_endpoint": "userInfoEndpoint",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
        },
    )
    class AuthenticateOidcConfigProperty:
        def __init__(
            self,
            *,
            authorization_endpoint: builtins.str,
            client_id: builtins.str,
            client_secret: builtins.str,
            issuer: builtins.str,
            token_endpoint: builtins.str,
            user_info_endpoint: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param authorization_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.
            :param client_id: ``CfnListenerRule.AuthenticateOidcConfigProperty.ClientId``.
            :param client_secret: ``CfnListenerRule.AuthenticateOidcConfigProperty.ClientSecret``.
            :param issuer: ``CfnListenerRule.AuthenticateOidcConfigProperty.Issuer``.
            :param token_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.TokenEndpoint``.
            :param user_info_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.UserInfoEndpoint``.
            :param authentication_request_extra_params: ``CfnListenerRule.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListenerRule.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListenerRule.AuthenticateOidcConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListenerRule.AuthenticateOidcConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListenerRule.AuthenticateOidcConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "authorization_endpoint": authorization_endpoint,
                "client_id": client_id,
                "client_secret": client_secret,
                "issuer": issuer,
                "token_endpoint": token_endpoint,
                "user_info_endpoint": user_info_endpoint,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout

        @builtins.property
        def authorization_endpoint(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authorizationendpoint
            """
            result = self._values.get("authorization_endpoint")
            assert result is not None, "Required property 'authorization_endpoint' is missing"
            return result

        @builtins.property
        def client_id(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.ClientId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientid
            """
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return result

        @builtins.property
        def client_secret(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.ClientSecret``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientsecret
            """
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return result

        @builtins.property
        def issuer(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.Issuer``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-issuer
            """
            result = self._values.get("issuer")
            assert result is not None, "Required property 'issuer' is missing"
            return result

        @builtins.property
        def token_endpoint(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.TokenEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-tokenendpoint
            """
            result = self._values.get("token_endpoint")
            assert result is not None, "Required property 'token_endpoint' is missing"
            return result

        @builtins.property
        def user_info_endpoint(self) -> builtins.str:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-userinfoendpoint
            """
            result = self._values.get("user_info_endpoint")
            assert result is not None, "Required property 'user_info_endpoint' is missing"
            return result

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authenticationrequestextraparams
            """
            result = self._values.get("authentication_request_extra_params")
            return result

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-onunauthenticatedrequest
            """
            result = self._values.get("on_unauthenticated_request")
            return result

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.Scope``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-scope
            """
            result = self._values.get("scope")
            return result

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.SessionCookieName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessioncookiename
            """
            result = self._values.get("session_cookie_name")
            return result

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.AuthenticateOidcConfigProperty.SessionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessiontimeout
            """
            result = self._values.get("session_timeout")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateOidcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.FixedResponseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "content_type": "contentType",
            "message_body": "messageBody",
        },
    )
    class FixedResponseConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            content_type: typing.Optional[builtins.str] = None,
            message_body: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param status_code: ``CfnListenerRule.FixedResponseConfigProperty.StatusCode``.
            :param content_type: ``CfnListenerRule.FixedResponseConfigProperty.ContentType``.
            :param message_body: ``CfnListenerRule.FixedResponseConfigProperty.MessageBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if content_type is not None:
                self._values["content_type"] = content_type
            if message_body is not None:
                self._values["message_body"] = message_body

        @builtins.property
        def status_code(self) -> builtins.str:
            """``CfnListenerRule.FixedResponseConfigProperty.StatusCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-statuscode
            """
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return result

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.FixedResponseConfigProperty.ContentType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-contenttype
            """
            result = self._values.get("content_type")
            return result

        @builtins.property
        def message_body(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.FixedResponseConfigProperty.MessageBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-messagebody
            """
            result = self._values.get("message_body")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.ForwardConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_groups": "targetGroups",
            "target_group_stickiness_config": "targetGroupStickinessConfig",
        },
    )
    class ForwardConfigProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.TargetGroupTupleProperty"]]]] = None,
            target_group_stickiness_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.TargetGroupStickinessConfigProperty"]] = None,
        ) -> None:
            """
            :param target_groups: ``CfnListenerRule.ForwardConfigProperty.TargetGroups``.
            :param target_group_stickiness_config: ``CfnListenerRule.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if target_group_stickiness_config is not None:
                self._values["target_group_stickiness_config"] = target_group_stickiness_config

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.TargetGroupTupleProperty"]]]]:
            """``CfnListenerRule.ForwardConfigProperty.TargetGroups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html#cfn-elasticloadbalancingv2-listenerrule-forwardconfig-targetgroups
            """
            result = self._values.get("target_groups")
            return result

        @builtins.property
        def target_group_stickiness_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.TargetGroupStickinessConfigProperty"]]:
            """``CfnListenerRule.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html#cfn-elasticloadbalancingv2-listenerrule-forwardconfig-targetgroupstickinessconfig
            """
            result = self._values.get("target_group_stickiness_config")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.HostHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class HostHeaderConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param values: ``CfnListenerRule.HostHeaderConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnListenerRule.HostHeaderConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-hostheaderconfig-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.HttpHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"http_header_name": "httpHeaderName", "values": "values"},
    )
    class HttpHeaderConfigProperty:
        def __init__(
            self,
            *,
            http_header_name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param http_header_name: ``CfnListenerRule.HttpHeaderConfigProperty.HttpHeaderName``.
            :param values: ``CfnListenerRule.HttpHeaderConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if http_header_name is not None:
                self._values["http_header_name"] = http_header_name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def http_header_name(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.HttpHeaderConfigProperty.HttpHeaderName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-httpheadername
            """
            result = self._values.get("http_header_name")
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnListenerRule.HttpHeaderConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.HttpRequestMethodConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class HttpRequestMethodConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param values: ``CfnListenerRule.HttpRequestMethodConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnListenerRule.HttpRequestMethodConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html#cfn-elasticloadbalancingv2-listenerrule-httprequestmethodconfig-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRequestMethodConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.PathPatternConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class PathPatternConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param values: ``CfnListenerRule.PathPatternConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnListenerRule.PathPatternConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html#cfn-elasticloadbalancingv2-listenerrule-pathpatternconfig-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathPatternConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.QueryStringConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class QueryStringConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.QueryStringKeyValueProperty"]]]] = None,
        ) -> None:
            """
            :param values: ``CfnListenerRule.QueryStringConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.QueryStringKeyValueProperty"]]]]:
            """``CfnListenerRule.QueryStringConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html#cfn-elasticloadbalancingv2-listenerrule-querystringconfig-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.QueryStringKeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class QueryStringKeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param key: ``CfnListenerRule.QueryStringKeyValueProperty.Key``.
            :param value: ``CfnListenerRule.QueryStringKeyValueProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.QueryStringKeyValueProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-key
            """
            result = self._values.get("key")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.QueryStringKeyValueProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringKeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RedirectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "host": "host",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "query": "query",
        },
    )
    class RedirectConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            host: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            query: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param status_code: ``CfnListenerRule.RedirectConfigProperty.StatusCode``.
            :param host: ``CfnListenerRule.RedirectConfigProperty.Host``.
            :param path: ``CfnListenerRule.RedirectConfigProperty.Path``.
            :param port: ``CfnListenerRule.RedirectConfigProperty.Port``.
            :param protocol: ``CfnListenerRule.RedirectConfigProperty.Protocol``.
            :param query: ``CfnListenerRule.RedirectConfigProperty.Query``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if host is not None:
                self._values["host"] = host
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if query is not None:
                self._values["query"] = query

        @builtins.property
        def status_code(self) -> builtins.str:
            """``CfnListenerRule.RedirectConfigProperty.StatusCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-statuscode
            """
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return result

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.RedirectConfigProperty.Host``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-host
            """
            result = self._values.get("host")
            return result

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.RedirectConfigProperty.Path``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-path
            """
            result = self._values.get("path")
            return result

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.RedirectConfigProperty.Port``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-port
            """
            result = self._values.get("port")
            return result

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.RedirectConfigProperty.Protocol``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-protocol
            """
            result = self._values.get("protocol")
            return result

        @builtins.property
        def query(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.RedirectConfigProperty.Query``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-query
            """
            result = self._values.get("query")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RuleConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field": "field",
            "host_header_config": "hostHeaderConfig",
            "http_header_config": "httpHeaderConfig",
            "http_request_method_config": "httpRequestMethodConfig",
            "path_pattern_config": "pathPatternConfig",
            "query_string_config": "queryStringConfig",
            "source_ip_config": "sourceIpConfig",
            "values": "values",
        },
    )
    class RuleConditionProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            host_header_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.HostHeaderConfigProperty"]] = None,
            http_header_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.HttpHeaderConfigProperty"]] = None,
            http_request_method_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.HttpRequestMethodConfigProperty"]] = None,
            path_pattern_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.PathPatternConfigProperty"]] = None,
            query_string_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.QueryStringConfigProperty"]] = None,
            source_ip_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.SourceIpConfigProperty"]] = None,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param field: ``CfnListenerRule.RuleConditionProperty.Field``.
            :param host_header_config: ``CfnListenerRule.RuleConditionProperty.HostHeaderConfig``.
            :param http_header_config: ``CfnListenerRule.RuleConditionProperty.HttpHeaderConfig``.
            :param http_request_method_config: ``CfnListenerRule.RuleConditionProperty.HttpRequestMethodConfig``.
            :param path_pattern_config: ``CfnListenerRule.RuleConditionProperty.PathPatternConfig``.
            :param query_string_config: ``CfnListenerRule.RuleConditionProperty.QueryStringConfig``.
            :param source_ip_config: ``CfnListenerRule.RuleConditionProperty.SourceIpConfig``.
            :param values: ``CfnListenerRule.RuleConditionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if host_header_config is not None:
                self._values["host_header_config"] = host_header_config
            if http_header_config is not None:
                self._values["http_header_config"] = http_header_config
            if http_request_method_config is not None:
                self._values["http_request_method_config"] = http_request_method_config
            if path_pattern_config is not None:
                self._values["path_pattern_config"] = path_pattern_config
            if query_string_config is not None:
                self._values["query_string_config"] = query_string_config
            if source_ip_config is not None:
                self._values["source_ip_config"] = source_ip_config
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.RuleConditionProperty.Field``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-conditions-field
            """
            result = self._values.get("field")
            return result

        @builtins.property
        def host_header_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.HostHeaderConfigProperty"]]:
            """``CfnListenerRule.RuleConditionProperty.HostHeaderConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-hostheaderconfig
            """
            result = self._values.get("host_header_config")
            return result

        @builtins.property
        def http_header_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.HttpHeaderConfigProperty"]]:
            """``CfnListenerRule.RuleConditionProperty.HttpHeaderConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httpheaderconfig
            """
            result = self._values.get("http_header_config")
            return result

        @builtins.property
        def http_request_method_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.HttpRequestMethodConfigProperty"]]:
            """``CfnListenerRule.RuleConditionProperty.HttpRequestMethodConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httprequestmethodconfig
            """
            result = self._values.get("http_request_method_config")
            return result

        @builtins.property
        def path_pattern_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.PathPatternConfigProperty"]]:
            """``CfnListenerRule.RuleConditionProperty.PathPatternConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-pathpatternconfig
            """
            result = self._values.get("path_pattern_config")
            return result

        @builtins.property
        def query_string_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.QueryStringConfigProperty"]]:
            """``CfnListenerRule.RuleConditionProperty.QueryStringConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-querystringconfig
            """
            result = self._values.get("query_string_config")
            return result

        @builtins.property
        def source_ip_config(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnListenerRule.SourceIpConfigProperty"]]:
            """``CfnListenerRule.RuleConditionProperty.SourceIpConfig``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-sourceipconfig
            """
            result = self._values.get("source_ip_config")
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnListenerRule.RuleConditionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-conditions-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.SourceIpConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class SourceIpConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param values: ``CfnListenerRule.SourceIpConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnListenerRule.SourceIpConfigProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html#cfn-elasticloadbalancingv2-listenerrule-sourceipconfig-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceIpConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.TargetGroupStickinessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_seconds": "durationSeconds", "enabled": "enabled"},
    )
    class TargetGroupStickinessConfigProperty:
        def __init__(
            self,
            *,
            duration_seconds: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param duration_seconds: ``CfnListenerRule.TargetGroupStickinessConfigProperty.DurationSeconds``.
            :param enabled: ``CfnListenerRule.TargetGroupStickinessConfigProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_seconds is not None:
                self._values["duration_seconds"] = duration_seconds
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def duration_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.TargetGroupStickinessConfigProperty.DurationSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig-durationseconds
            """
            result = self._values.get("duration_seconds")
            return result

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnListenerRule.TargetGroupStickinessConfigProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig-enabled
            """
            result = self._values.get("enabled")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupStickinessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.TargetGroupTupleProperty",
        jsii_struct_bases=[],
        name_mapping={"target_group_arn": "targetGroupArn", "weight": "weight"},
    )
    class TargetGroupTupleProperty:
        def __init__(
            self,
            *,
            target_group_arn: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param target_group_arn: ``CfnListenerRule.TargetGroupTupleProperty.TargetGroupArn``.
            :param weight: ``CfnListenerRule.TargetGroupTupleProperty.Weight``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            """``CfnListenerRule.TargetGroupTupleProperty.TargetGroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html#cfn-elasticloadbalancingv2-listenerrule-targetgrouptuple-targetgrouparn
            """
            result = self._values.get("target_group_arn")
            return result

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            """``CfnListenerRule.TargetGroupTupleProperty.Weight``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html#cfn-elasticloadbalancingv2-listenerrule-targetgrouptuple-weight
            """
            result = self._values.get("weight")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "conditions": "conditions",
        "listener_arn": "listenerArn",
        "priority": "priority",
    },
)
class CfnListenerRuleProps:
    def __init__(
        self,
        *,
        actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListenerRule.ActionProperty]]],
        conditions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListenerRule.RuleConditionProperty]]],
        listener_arn: builtins.str,
        priority: jsii.Number,
    ) -> None:
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        :param actions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.
        :param conditions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.
        :param priority: ``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "actions": actions,
            "conditions": conditions,
            "listener_arn": listener_arn,
            "priority": priority,
        }

    @builtins.property
    def actions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListenerRule.ActionProperty]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
        """
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return result

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListenerRule.RuleConditionProperty]]]:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
        """
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return result

    @builtins.property
    def listener_arn(self) -> builtins.str:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
        """
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return result

    @builtins.property
    def priority(self) -> jsii.Number:
        """``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
        """
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLoadBalancer(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer",
):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::LoadBalancer
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        ip_address_type: typing.Optional[builtins.str] = None,
        load_balancer_attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LoadBalancerAttributeProperty"]]]] = None,
        name: typing.Optional[builtins.str] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        subnet_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.SubnetMappingProperty"]]]] = None,
        subnets: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ip_address_type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.
        :param load_balancer_attributes: ``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.
        :param name: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.
        :param scheme: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.
        :param subnet_mappings: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.
        :param subnets: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.
        :param type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.
        """
        props = CfnLoadBalancerProps(
            ip_address_type=ip_address_type,
            load_balancer_attributes=load_balancer_attributes,
            name=name,
            scheme=scheme,
            security_groups=security_groups,
            subnet_mappings=subnet_mappings,
            subnets=subnets,
            tags=tags,
            type=type,
        )

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCanonicalHostedZoneId")
    def attr_canonical_hosted_zone_id(self) -> builtins.str:
        """
        :cloudformationAttribute: CanonicalHostedZoneID
        """
        return jsii.get(self, "attrCanonicalHostedZoneId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> builtins.str:
        """
        :cloudformationAttribute: DNSName
        """
        return jsii.get(self, "attrDnsName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrLoadBalancerFullName")
    def attr_load_balancer_full_name(self) -> builtins.str:
        """
        :cloudformationAttribute: LoadBalancerFullName
        """
        return jsii.get(self, "attrLoadBalancerFullName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrLoadBalancerName")
    def attr_load_balancer_name(self) -> builtins.str:
        """
        :cloudformationAttribute: LoadBalancerName
        """
        return jsii.get(self, "attrLoadBalancerName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrSecurityGroups")
    def attr_security_groups(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: SecurityGroups
        """
        return jsii.get(self, "attrSecurityGroups")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
        """
        return jsii.get(self, "ipAddressType")

    @ip_address_type.setter # type: ignore
    def ip_address_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ipAddressType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerAttributes")
    def load_balancer_attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LoadBalancerAttributeProperty"]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
        """
        return jsii.get(self, "loadBalancerAttributes")

    @load_balancer_attributes.setter # type: ignore
    def load_balancer_attributes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LoadBalancerAttributeProperty"]]]],
    ) -> None:
        jsii.set(self, "loadBalancerAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
        """
        return jsii.get(self, "scheme")

    @scheme.setter # type: ignore
    def scheme(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scheme", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter # type: ignore
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetMappings")
    def subnet_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.SubnetMappingProperty"]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
        """
        return jsii.get(self, "subnetMappings")

    @subnet_mappings.setter # type: ignore
    def subnet_mappings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.SubnetMappingProperty"]]]],
    ) -> None:
        jsii.set(self, "subnetMappings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
        """
        return jsii.get(self, "subnets")

    @subnets.setter # type: ignore
    def subnets(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "subnets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.LoadBalancerAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class LoadBalancerAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param key: ``CfnLoadBalancer.LoadBalancerAttributeProperty.Key``.
            :param value: ``CfnLoadBalancer.LoadBalancerAttributeProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.LoadBalancerAttributeProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-key
            """
            result = self._values.get("key")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.LoadBalancerAttributeProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBalancerAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.SubnetMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subnet_id": "subnetId",
            "allocation_id": "allocationId",
            "i_pv6_address": "iPv6Address",
            "private_i_pv4_address": "privateIPv4Address",
        },
    )
    class SubnetMappingProperty:
        def __init__(
            self,
            *,
            subnet_id: builtins.str,
            allocation_id: typing.Optional[builtins.str] = None,
            i_pv6_address: typing.Optional[builtins.str] = None,
            private_i_pv4_address: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param subnet_id: ``CfnLoadBalancer.SubnetMappingProperty.SubnetId``.
            :param allocation_id: ``CfnLoadBalancer.SubnetMappingProperty.AllocationId``.
            :param i_pv6_address: ``CfnLoadBalancer.SubnetMappingProperty.IPv6Address``.
            :param private_i_pv4_address: ``CfnLoadBalancer.SubnetMappingProperty.PrivateIPv4Address``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "subnet_id": subnet_id,
            }
            if allocation_id is not None:
                self._values["allocation_id"] = allocation_id
            if i_pv6_address is not None:
                self._values["i_pv6_address"] = i_pv6_address
            if private_i_pv4_address is not None:
                self._values["private_i_pv4_address"] = private_i_pv4_address

        @builtins.property
        def subnet_id(self) -> builtins.str:
            """``CfnLoadBalancer.SubnetMappingProperty.SubnetId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-subnetid
            """
            result = self._values.get("subnet_id")
            assert result is not None, "Required property 'subnet_id' is missing"
            return result

        @builtins.property
        def allocation_id(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.SubnetMappingProperty.AllocationId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-allocationid
            """
            result = self._values.get("allocation_id")
            return result

        @builtins.property
        def i_pv6_address(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.SubnetMappingProperty.IPv6Address``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-ipv6address
            """
            result = self._values.get("i_pv6_address")
            return result

        @builtins.property
        def private_i_pv4_address(self) -> typing.Optional[builtins.str]:
            """``CfnLoadBalancer.SubnetMappingProperty.PrivateIPv4Address``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-privateipv4address
            """
            result = self._values.get("private_i_pv4_address")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address_type": "ipAddressType",
        "load_balancer_attributes": "loadBalancerAttributes",
        "name": "name",
        "scheme": "scheme",
        "security_groups": "securityGroups",
        "subnet_mappings": "subnetMappings",
        "subnets": "subnets",
        "tags": "tags",
        "type": "type",
    },
)
class CfnLoadBalancerProps:
    def __init__(
        self,
        *,
        ip_address_type: typing.Optional[builtins.str] = None,
        load_balancer_attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.LoadBalancerAttributeProperty]]]] = None,
        name: typing.Optional[builtins.str] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        subnet_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.SubnetMappingProperty]]]] = None,
        subnets: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param ip_address_type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.
        :param load_balancer_attributes: ``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.
        :param name: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.
        :param scheme: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.
        :param subnet_mappings: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.
        :param subnets: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.
        :param type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if load_balancer_attributes is not None:
            self._values["load_balancer_attributes"] = load_balancer_attributes
        if name is not None:
            self._values["name"] = name
        if scheme is not None:
            self._values["scheme"] = scheme
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_mappings is not None:
            self._values["subnet_mappings"] = subnet_mappings
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
        """
        result = self._values.get("ip_address_type")
        return result

    @builtins.property
    def load_balancer_attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.LoadBalancerAttributeProperty]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
        """
        result = self._values.get("load_balancer_attributes")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
        """
        result = self._values.get("scheme")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnet_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLoadBalancer.SubnetMappingProperty]]]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
        """
        result = self._values.get("subnet_mappings")
        return result

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
        """
        result = self._values.get("subnets")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
        """
        result = self._values.get("type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTargetGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup",
):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::TargetGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::TargetGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[builtins.str] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        matcher: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.MatcherProperty"]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        target_group_attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetGroupAttributeProperty"]]]] = None,
        targets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetDescriptionProperty"]]]] = None,
        target_type: typing.Optional[builtins.str] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param health_check_enabled: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.
        :param health_check_interval_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.
        :param health_check_timeout_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.
        :param healthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.
        :param matcher: ``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.
        :param name: ``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.
        :param port: ``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.
        :param tags: ``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.
        :param target_group_attributes: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.
        :param targets: ``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.
        :param target_type: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.
        :param unhealthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.
        :param vpc_id: ``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.
        """
        props = CfnTargetGroupProps(
            health_check_enabled=health_check_enabled,
            health_check_interval_seconds=health_check_interval_seconds,
            health_check_path=health_check_path,
            health_check_port=health_check_port,
            health_check_protocol=health_check_protocol,
            health_check_timeout_seconds=health_check_timeout_seconds,
            healthy_threshold_count=healthy_threshold_count,
            matcher=matcher,
            name=name,
            port=port,
            protocol=protocol,
            tags=tags,
            target_group_attributes=target_group_attributes,
            targets=targets,
            target_type=target_type,
            unhealthy_threshold_count=unhealthy_threshold_count,
            vpc_id=vpc_id,
        )

        jsii.create(CfnTargetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrLoadBalancerArns")
    def attr_load_balancer_arns(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: LoadBalancerArns
        """
        return jsii.get(self, "attrLoadBalancerArns")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrTargetGroupFullName")
    def attr_target_group_full_name(self) -> builtins.str:
        """
        :cloudformationAttribute: TargetGroupFullName
        """
        return jsii.get(self, "attrTargetGroupFullName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrTargetGroupName")
    def attr_target_group_name(self) -> builtins.str:
        """
        :cloudformationAttribute: TargetGroupName
        """
        return jsii.get(self, "attrTargetGroupName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckEnabled")
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
        """
        return jsii.get(self, "healthCheckEnabled")

    @health_check_enabled.setter # type: ignore
    def health_check_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "healthCheckEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
        """
        return jsii.get(self, "healthCheckIntervalSeconds")

    @health_check_interval_seconds.setter # type: ignore
    def health_check_interval_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
        """
        return jsii.get(self, "healthCheckPath")

    @health_check_path.setter # type: ignore
    def health_check_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckPath", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
        """
        return jsii.get(self, "healthCheckPort")

    @health_check_port.setter # type: ignore
    def health_check_port(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckPort", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
        """
        return jsii.get(self, "healthCheckProtocol")

    @health_check_protocol.setter # type: ignore
    def health_check_protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheckTimeoutSeconds")
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
        """
        return jsii.get(self, "healthCheckTimeoutSeconds")

    @health_check_timeout_seconds.setter # type: ignore
    def health_check_timeout_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckTimeoutSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthyThresholdCount")
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
        """
        return jsii.get(self, "healthyThresholdCount")

    @healthy_threshold_count.setter # type: ignore
    def healthy_threshold_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthyThresholdCount", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="matcher")
    def matcher(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.MatcherProperty"]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
        """
        return jsii.get(self, "matcher")

    @matcher.setter # type: ignore
    def matcher(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.MatcherProperty"]],
    ) -> None:
        jsii.set(self, "matcher", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
        """
        return jsii.get(self, "port")

    @port.setter # type: ignore
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter # type: ignore
    def protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupAttributes")
    def target_group_attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetGroupAttributeProperty"]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
        """
        return jsii.get(self, "targetGroupAttributes")

    @target_group_attributes.setter # type: ignore
    def target_group_attributes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetGroupAttributeProperty"]]]],
    ) -> None:
        jsii.set(self, "targetGroupAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetDescriptionProperty"]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
        """
        return jsii.get(self, "targets")

    @targets.setter # type: ignore
    def targets(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTargetGroup.TargetDescriptionProperty"]]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
        """
        return jsii.get(self, "targetType")

    @target_type.setter # type: ignore
    def target_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "targetType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="unhealthyThresholdCount")
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
        """
        return jsii.get(self, "unhealthyThresholdCount")

    @unhealthy_threshold_count.setter # type: ignore
    def unhealthy_threshold_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "unhealthyThresholdCount", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
        """
        return jsii.get(self, "vpcId")

    @vpc_id.setter # type: ignore
    def vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "vpcId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.MatcherProperty",
        jsii_struct_bases=[],
        name_mapping={"http_code": "httpCode"},
    )
    class MatcherProperty:
        def __init__(self, *, http_code: typing.Optional[builtins.str] = None) -> None:
            """
            :param http_code: ``CfnTargetGroup.MatcherProperty.HttpCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if http_code is not None:
                self._values["http_code"] = http_code

        @builtins.property
        def http_code(self) -> typing.Optional[builtins.str]:
            """``CfnTargetGroup.MatcherProperty.HttpCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html#cfn-elasticloadbalancingv2-targetgroup-matcher-httpcode
            """
            result = self._values.get("http_code")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatcherProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "availability_zone": "availabilityZone",
            "port": "port",
        },
    )
    class TargetDescriptionProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            availability_zone: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param id: ``CfnTargetGroup.TargetDescriptionProperty.Id``.
            :param availability_zone: ``CfnTargetGroup.TargetDescriptionProperty.AvailabilityZone``.
            :param port: ``CfnTargetGroup.TargetDescriptionProperty.Port``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
            }
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnTargetGroup.TargetDescriptionProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            """``CfnTargetGroup.TargetDescriptionProperty.AvailabilityZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-availabilityzone
            """
            result = self._values.get("availability_zone")
            return result

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnTargetGroup.TargetDescriptionProperty.Port``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-port
            """
            result = self._values.get("port")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetGroupAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TargetGroupAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param key: ``CfnTargetGroup.TargetGroupAttributeProperty.Key``.
            :param value: ``CfnTargetGroup.TargetGroupAttributeProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            """``CfnTargetGroup.TargetGroupAttributeProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-key
            """
            result = self._values.get("key")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnTargetGroup.TargetGroupAttributeProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "health_check_enabled": "healthCheckEnabled",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "health_check_timeout_seconds": "healthCheckTimeoutSeconds",
        "healthy_threshold_count": "healthyThresholdCount",
        "matcher": "matcher",
        "name": "name",
        "port": "port",
        "protocol": "protocol",
        "tags": "tags",
        "target_group_attributes": "targetGroupAttributes",
        "targets": "targets",
        "target_type": "targetType",
        "unhealthy_threshold_count": "unhealthyThresholdCount",
        "vpc_id": "vpcId",
    },
)
class CfnTargetGroupProps:
    def __init__(
        self,
        *,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[builtins.str] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        matcher: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnTargetGroup.MatcherProperty]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        target_group_attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTargetGroup.TargetGroupAttributeProperty]]]] = None,
        targets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTargetGroup.TargetDescriptionProperty]]]] = None,
        target_type: typing.Optional[builtins.str] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        :param health_check_enabled: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.
        :param health_check_interval_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.
        :param health_check_timeout_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.
        :param healthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.
        :param matcher: ``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.
        :param name: ``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.
        :param port: ``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.
        :param tags: ``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.
        :param target_group_attributes: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.
        :param targets: ``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.
        :param target_type: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.
        :param unhealthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.
        :param vpc_id: ``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if health_check_enabled is not None:
            self._values["health_check_enabled"] = health_check_enabled
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if health_check_timeout_seconds is not None:
            self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
        if healthy_threshold_count is not None:
            self._values["healthy_threshold_count"] = healthy_threshold_count
        if matcher is not None:
            self._values["matcher"] = matcher
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if tags is not None:
            self._values["tags"] = tags
        if target_group_attributes is not None:
            self._values["target_group_attributes"] = target_group_attributes
        if targets is not None:
            self._values["targets"] = targets
        if target_type is not None:
            self._values["target_type"] = target_type
        if unhealthy_threshold_count is not None:
            self._values["unhealthy_threshold_count"] = unhealthy_threshold_count
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
        """
        result = self._values.get("health_check_enabled")
        return result

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
        """
        result = self._values.get("health_check_interval_seconds")
        return result

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
        """
        result = self._values.get("health_check_path")
        return result

    @builtins.property
    def health_check_port(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
        """
        result = self._values.get("health_check_port")
        return result

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
        """
        result = self._values.get("health_check_protocol")
        return result

    @builtins.property
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
        """
        result = self._values.get("health_check_timeout_seconds")
        return result

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
        """
        result = self._values.get("healthy_threshold_count")
        return result

    @builtins.property
    def matcher(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnTargetGroup.MatcherProperty]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
        """
        result = self._values.get("matcher")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def target_group_attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTargetGroup.TargetGroupAttributeProperty]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
        """
        result = self._values.get("target_group_attributes")
        return result

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTargetGroup.TargetDescriptionProperty]]]]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
        """
        result = self._values.get("targets")
        return result

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
        """
        result = self._values.get("target_type")
        return result

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
        """
        result = self._values.get("unhealthy_threshold_count")
        return result

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
        """
        result = self._values.get("vpc_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ContentType")
class ContentType(enum.Enum):
    """The content type for a fixed response."""

    TEXT_PLAIN = "TEXT_PLAIN"
    TEXT_CSS = "TEXT_CSS"
    TEXT_HTML = "TEXT_HTML"
    APPLICATION_JAVASCRIPT = "APPLICATION_JAVASCRIPT"
    APPLICATION_JSON = "APPLICATION_JSON"


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.FixedResponse",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "content_type": "contentType",
        "message_body": "messageBody",
    },
)
class FixedResponse:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        content_type: typing.Optional[ContentType] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        """A fixed response.

        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message
        """
        self._values: typing.Dict[str, typing.Any] = {
            "status_code": status_code,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if message_body is not None:
            self._values["message_body"] = message_body

    @builtins.property
    def status_code(self) -> builtins.str:
        """The HTTP response code (2XX, 4XX or 5XX)."""
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return result

    @builtins.property
    def content_type(self) -> typing.Optional[ContentType]:
        """The content type.

        :default: text/plain
        """
        result = self._values.get("content_type")
        return result

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        """The message.

        :default: no message
        """
        result = self._values.get("message_body")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FixedResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.FixedResponseOptions",
    jsii_struct_bases=[],
    name_mapping={"content_type": "contentType", "message_body": "messageBody"},
)
class FixedResponseOptions:
    def __init__(
        self,
        *,
        content_type: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options for ``ListenerAction.fixedResponse()``.

        :param content_type: Content Type of the response. Valid Values: text/plain | text/css | text/html | application/javascript | application/json Default: - Automatically determined
        :param message_body: The response body. Default: - No body
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if content_type is not None:
            self._values["content_type"] = content_type
        if message_body is not None:
            self._values["message_body"] = message_body

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        """Content Type of the response.

        Valid Values: text/plain | text/css | text/html | application/javascript | application/json

        :default: - Automatically determined
        """
        result = self._values.get("content_type")
        return result

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        """The response body.

        :default: - No body
        """
        result = self._values.get("message_body")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FixedResponseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ForwardOptions",
    jsii_struct_bases=[],
    name_mapping={"stickiness_duration": "stickinessDuration"},
)
class ForwardOptions:
    def __init__(
        self,
        *,
        stickiness_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Options for ``ListenerAction.forward()``.

        :param stickiness_duration: For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if stickiness_duration is not None:
            self._values["stickiness_duration"] = stickiness_duration

    @builtins.property
    def stickiness_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """For how long clients should be directed to the same target group.

        Range between 1 second and 7 days.

        :default: - No stickiness
        """
        result = self._values.get("stickiness_duration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForwardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "healthy_http_codes": "healthyHttpCodes",
        "healthy_threshold_count": "healthyThresholdCount",
        "interval": "interval",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold_count": "unhealthyThresholdCount",
    },
)
class HealthCheck:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        healthy_http_codes: typing.Optional[builtins.str] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[aws_cdk.core.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional["Protocol"] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for configuring a health check.

        :param enabled: Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance or ip, health checks are always enabled and cannot be disabled. Default: - Determined automatically.
        :param healthy_http_codes: HTTP code to use when checking for a successful response from a target. For Application Load Balancers, you can specify values between 200 and 499, and the default value is 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
        :param healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3. Default: 5 for ALBs, 3 for NLBs
        :param interval: The approximate number of seconds between health checks for an individual target. Default: Duration.seconds(30)
        :param path: The ping path destination where Elastic Load Balancing sends health check requests. Default: /
        :param port: The port that the load balancer uses when performing health checks on the targets. Default: 'traffic-port'
        :param protocol: The protocol the load balancer uses when performing health checks on targets. The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP. The TLS, UDP, and TCP_UDP protocols are not supported for health checks. Default: HTTP for ALBs, TCP for NLBs
        :param timeout: The amount of time, in seconds, during which no response from a target means a failed health check. For Application Load Balancers, the range is 2-60 seconds and the default is 5 seconds. For Network Load Balancers, this is 10 seconds for TCP and HTTPS health checks and 6 seconds for HTTP health checks. Default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        :param unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. For Application Load Balancers, the default is 2. For Network Load Balancers, this value must be the same as the healthy threshold count. Default: 2
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if healthy_http_codes is not None:
            self._values["healthy_http_codes"] = healthy_http_codes
        if healthy_threshold_count is not None:
            self._values["healthy_threshold_count"] = healthy_threshold_count
        if interval is not None:
            self._values["interval"] = interval
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold_count is not None:
            self._values["unhealthy_threshold_count"] = unhealthy_threshold_count

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        """Indicates whether health checks are enabled.

        If the target type is lambda,
        health checks are disabled by default but can be enabled. If the target type
        is instance or ip, health checks are always enabled and cannot be disabled.

        :default: - Determined automatically.
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def healthy_http_codes(self) -> typing.Optional[builtins.str]:
        """HTTP code to use when checking for a successful response from a target.

        For Application Load Balancers, you can specify values between 200 and
        499, and the default value is 200. You can specify multiple values (for
        example, "200,202") or a range of values (for example, "200-299").
        """
        result = self._values.get("healthy_http_codes")
        return result

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """The number of consecutive health checks successes required before considering an unhealthy target healthy.

        For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3.

        :default: 5 for ALBs, 3 for NLBs
        """
        result = self._values.get("healthy_threshold_count")
        return result

    @builtins.property
    def interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The approximate number of seconds between health checks for an individual target.

        :default: Duration.seconds(30)
        """
        result = self._values.get("interval")
        return result

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        """The ping path destination where Elastic Load Balancing sends health check requests.

        :default: /
        """
        result = self._values.get("path")
        return result

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        """The port that the load balancer uses when performing health checks on the targets.

        :default: 'traffic-port'
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol the load balancer uses when performing health checks on targets.

        The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP.
        The TLS, UDP, and TCP_UDP protocols are not supported for health checks.

        :default: HTTP for ALBs, TCP for NLBs
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time, in seconds, during which no response from a target means a failed health check.

        For Application Load Balancers, the range is 2-60 seconds and the
        default is 5 seconds. For Network Load Balancers, this is 10 seconds for
        TCP and HTTPS health checks and 6 seconds for HTTP health checks.

        :default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        """The number of consecutive health check failures required before considering a target unhealthy.

        For Application Load Balancers, the default is 2. For Network Load
        Balancers, this value must be the same as the healthy threshold count.

        :default: 2
        """
        result = self._values.get("unhealthy_threshold_count")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeElb")
class HttpCodeElb(enum.Enum):
    """Count of HTTP status originating from the load balancer.

    This count does not include any response codes generated by the targets.
    """

    ELB_3XX_COUNT = "ELB_3XX_COUNT"
    """The number of HTTP 3XX redirection codes that originate from the load balancer."""
    ELB_4XX_COUNT = "ELB_4XX_COUNT"
    """The number of HTTP 4XX client error codes that originate from the load balancer.

    Client errors are generated when requests are malformed or incomplete.
    These requests have not been received by the target. This count does not
    include any response codes generated by the targets.
    """
    ELB_5XX_COUNT = "ELB_5XX_COUNT"
    """The number of HTTP 5XX server error codes that originate from the load balancer."""


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeTarget")
class HttpCodeTarget(enum.Enum):
    """Count of HTTP status originating from the targets."""

    TARGET_2XX_COUNT = "TARGET_2XX_COUNT"
    """The number of 2xx response codes from targets."""
    TARGET_3XX_COUNT = "TARGET_3XX_COUNT"
    """The number of 3xx response codes from targets."""
    TARGET_4XX_COUNT = "TARGET_4XX_COUNT"
    """The number of 4xx response codes from targets."""
    TARGET_5XX_COUNT = "TARGET_5XX_COUNT"
    """The number of 5xx response codes from targets."""


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener")
class IApplicationListener(
    aws_cdk.core.IResource,
    aws_cdk.aws_ec2.IConnectable,
    typing_extensions.Protocol,
):
    """Properties to reference an existing listener."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationListenerProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        """ARN of the listener.

        :attribute: true
        """
        ...

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(
        self,
        id: builtins.str,
        arns: typing.List[builtins.str],
    ) -> None:
        """Add one or more certificates to this listener.

        :param id: -
        :param arns: -
        """
        ...

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        id: builtins.str,
        *,
        target_groups: typing.List["IApplicationTargetGroup"],
        conditions: typing.Optional[typing.List["ListenerCondition"]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        :param id: -
        :param target_groups: Target groups to forward requests to.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        ...

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        slow_start: typing.Optional[aws_cdk.core.Duration] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]] = None,
        conditions: typing.Optional[typing.List["ListenerCondition"]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :return: The newly created target group
        """
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
        port_range: aws_cdk.aws_ec2.Port,
    ) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -
        """
        ...


class _IApplicationListenerProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), # type: ignore
):
    """Properties to reference an existing listener."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        """ARN of the listener.

        :attribute: true
        """
        return jsii.get(self, "listenerArn")

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(
        self,
        id: builtins.str,
        arns: typing.List[builtins.str],
    ) -> None:
        """Add one or more certificates to this listener.

        :param id: -
        :param arns: -
        """
        return jsii.invoke(self, "addCertificateArns", [id, arns])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        id: builtins.str,
        *,
        target_groups: typing.List["IApplicationTargetGroup"],
        conditions: typing.Optional[typing.List["ListenerCondition"]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        :param id: -
        :param target_groups: Target groups to forward requests to.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props = AddApplicationTargetGroupsProps(
            target_groups=target_groups,
            conditions=conditions,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            priority=priority,
        )

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        slow_start: typing.Optional[aws_cdk.core.Duration] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]] = None,
        conditions: typing.Optional[typing.List["ListenerCondition"]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :return: The newly created target group
        """
        props = AddApplicationTargetsProps(
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            port=port,
            protocol=protocol,
            slow_start=slow_start,
            stickiness_cookie_duration=stickiness_cookie_duration,
            target_group_name=target_group_name,
            targets=targets,
            conditions=conditions,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            priority=priority,
        )

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
        port_range: aws_cdk.aws_ec2.Port,
    ) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])


@jsii.interface(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget"
)
class IApplicationLoadBalancerTarget(typing_extensions.Protocol):
    """Interface for constructs that can be targets of an application load balancer."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: "IApplicationTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        ...


class _IApplicationLoadBalancerTargetProxy:
    """Interface for constructs that can be targets of an application load balancer."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget"

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: "IApplicationTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IListenerAction")
class IListenerAction(typing_extensions.Protocol):
    """Interface for listener actions."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListenerActionProxy

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        """Render the actions in this chain."""
        ...


class _IListenerActionProxy:
    """Interface for listener actions."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.IListenerAction"

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        """Render the actions in this chain."""
        return jsii.invoke(self, "renderActions", [])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IListenerCertificate")
class IListenerCertificate(typing_extensions.Protocol):
    """A certificate source for an ELBv2 listener."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListenerCertificateProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        """The ARN of the certificate to use."""
        ...


class _IListenerCertificateProxy:
    """A certificate source for an ELBv2 listener."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.IListenerCertificate"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        """The ARN of the certificate to use."""
        return jsii.get(self, "certificateArn")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ILoadBalancerV2")
class ILoadBalancerV2(aws_cdk.core.IResource, typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerV2Proxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> builtins.str:
        """The canonical hosted zone ID of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        """The DNS name of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        """
        ...


class _ILoadBalancerV2Proxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.ILoadBalancerV2"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> builtins.str:
        """The canonical hosted zone ID of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        """The DNS name of this load balancer.

        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        """
        return jsii.get(self, "loadBalancerDnsName")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkListener")
class INetworkListener(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Properties to reference an existing listener."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkListenerProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        """ARN of the listener.

        :attribute: true
        """
        ...


class _INetworkListenerProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Properties to reference an existing listener."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.INetworkListener"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        """ARN of the listener.

        :attribute: true
        """
        return jsii.get(self, "listenerArn")


@jsii.interface(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkListenerCertificateProps"
)
class INetworkListenerCertificateProps(
    IListenerCertificate,
    typing_extensions.Protocol,
):
    """(deprecated) Properties for adding a certificate to a listener.

    This interface exists for backwards compatibility.

    :deprecated: Use IListenerCertificate instead

    :stability: deprecated
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkListenerCertificatePropsProxy


class _INetworkListenerCertificatePropsProxy(
    jsii.proxy_for(IListenerCertificate) # type: ignore
):
    """(deprecated) Properties for adding a certificate to a listener.

    This interface exists for backwards compatibility.

    :deprecated: Use IListenerCertificate instead

    :stability: deprecated
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.INetworkListenerCertificateProps"
    pass


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer")
class INetworkLoadBalancer(
    ILoadBalancerV2,
    aws_cdk.aws_ec2.IVpcEndpointServiceLoadBalancer,
    typing_extensions.Protocol,
):
    """A network load balancer."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> "NetworkListener":
        """Add a listener to this load balancer.

        :param id: -
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.

        :return: The newly created listener
        """
        ...


class _INetworkLoadBalancerProxy(
    jsii.proxy_for(ILoadBalancerV2), # type: ignore
    jsii.proxy_for(aws_cdk.aws_ec2.IVpcEndpointServiceLoadBalancer), # type: ignore
):
    """A network load balancer."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> "NetworkListener":
        """Add a listener to this load balancer.

        :param id: -
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.

        :return: The newly created listener
        """
        props = BaseNetworkListenerProps(
            port=port,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return jsii.invoke(self, "addListener", [id, props])


@jsii.interface(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget"
)
class INetworkLoadBalancerTarget(typing_extensions.Protocol):
    """Interface for constructs that can be targets of an network load balancer."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: "INetworkTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        ...


class _INetworkLoadBalancerTargetProxy:
    """Interface for constructs that can be targets of an network load balancer."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget"

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: "INetworkTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup")
class ITargetGroup(aws_cdk.core.IConstruct, typing_extensions.Protocol):
    """A target group."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITargetGroupProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> builtins.str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.core.IDependable:
        """Return an object to depend on the listeners added to this target group."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        """ARN of the target group."""
        ...


class _ITargetGroupProxy(
    jsii.proxy_for(aws_cdk.core.IConstruct) # type: ignore
):
    """A target group."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> builtins.str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        return jsii.get(self, "loadBalancerArns")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.core.IDependable:
        """Return an object to depend on the listeners added to this target group."""
        return jsii.get(self, "loadBalancerAttached")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        """ARN of the target group."""
        return jsii.get(self, "targetGroupArn")


@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class InstanceTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.InstanceTarget",
):
    """(deprecated) An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.

    :deprecated: Use IpTarget from the

    :stability: deprecated
    :aws-cdk: /aws-elasticloadbalancingv2-targets package instead.
    """

    def __init__(
        self,
        instance_id: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        """(deprecated) Create a new Instance target.

        :param instance_id: Instance ID of the instance to register to.
        :param port: Override the default port for the target group.

        :stability: deprecated
        """
        jsii.create(InstanceTarget, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: "IApplicationTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """(deprecated) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: deprecated
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: "INetworkTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """(deprecated) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: deprecated
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpAddressType")
class IpAddressType(enum.Enum):
    """What kind of addresses to allocate to the load balancer."""

    IPV4 = "IPV4"
    """Allocate IPv4 addresses."""
    DUAL_STACK = "DUAL_STACK"
    """Allocate both IPv4 and IPv6 addresses."""


@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class IpTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpTarget",
):
    """(deprecated) An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.

    :deprecated: Use IpTarget from the

    :stability: deprecated
    :aws-cdk: /aws-elasticloadbalancingv2-targets package instead.
    """

    def __init__(
        self,
        ip_address: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        :param ip_address: The IP Address to load balance to.
        :param port: Override the group's default port.
        :param availability_zone: Availability zone to send traffic from.

        :stability: deprecated
        """
        jsii.create(IpTarget, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: "IApplicationTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """(deprecated) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: deprecated
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: "INetworkTargetGroup",
    ) -> "LoadBalancerTargetProps":
        """(deprecated) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: deprecated
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.implements(IListenerAction)
class ListenerAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ListenerAction",
):
    """What to do when a client makes a request to a listener.

    Some actions can be combined with other ones (specifically,
    you can perform authentication before serving the request).

    Multiple actions form a linked chain; the chain must always terminate in a
    *(weighted)forward*, *fixedResponse* or *redirect* action.

    If an action supports chaining, the next action can be indicated
    by passing it in the ``next`` property.

    (Called ``ListenerAction`` instead of the more strictly correct
    ``ListenerAction`` because this is the class most users interact
    with, and we want to make it not too visually overwhelming).
    """

    def __init__(
        self,
        action_json: CfnListener.ActionProperty,
        next: typing.Optional["ListenerAction"] = None,
    ) -> None:
        """Create an instance of ListenerAction.

        The default class should be good enough for most cases and
        should be created by using one of the static factory functions,
        but allow overriding to make sure we allow flexibility for the future.

        :param action_json: -
        :param next: -
        """
        jsii.create(ListenerAction, self, [action_json, next])

    @jsii.member(jsii_name="authenticateOidc")
    @builtins.classmethod
    def authenticate_oidc(
        cls,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: aws_cdk.core.SecretValue,
        issuer: builtins.str,
        next: "ListenerAction",
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional["UnauthenticatedAction"] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "ListenerAction":
        """Authenticate using an identity provider (IdP) that is compliant with OpenID Connect (OIDC).

        :param authorization_endpoint: The authorization endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param client_id: The OAuth 2.0 client identifier.
        :param client_secret: The OAuth 2.0 client secret.
        :param issuer: The OIDC issuer identifier of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param next: What action to execute next.
        :param token_endpoint: The token endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param user_info_endpoint: The user info endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint. Default: - No extra parameters
        :param on_unauthenticated_request: The behavior if the user is not authenticated. Default: UnauthenticatedAction.AUTHENTICATE
        :param scope: The set of user claims to be requested from the IdP. To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP. Default: "openid"
        :param session_cookie_name: The name of the cookie used to maintain session information. Default: "AWSELBAuthSessionCookie"
        :param session_timeout: The maximum duration of the authentication session. Default: Duration.days(7)

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html#oidc-requirements
        """
        options = AuthenticateOidcOptions(
            authorization_endpoint=authorization_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            issuer=issuer,
            next=next,
            token_endpoint=token_endpoint,
            user_info_endpoint=user_info_endpoint,
            authentication_request_extra_params=authentication_request_extra_params,
            on_unauthenticated_request=on_unauthenticated_request,
            scope=scope,
            session_cookie_name=session_cookie_name,
            session_timeout=session_timeout,
        )

        return jsii.sinvoke(cls, "authenticateOidc", [options])

    @jsii.member(jsii_name="fixedResponse")
    @builtins.classmethod
    def fixed_response(
        cls,
        status_code: jsii.Number,
        *,
        content_type: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> "ListenerAction":
        """Return a fixed response.

        :param status_code: -
        :param content_type: Content Type of the response. Valid Values: text/plain | text/css | text/html | application/javascript | application/json Default: - Automatically determined
        :param message_body: The response body. Default: - No body

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#fixed-response-actions
        """
        options = FixedResponseOptions(
            content_type=content_type, message_body=message_body
        )

        return jsii.sinvoke(cls, "fixedResponse", [status_code, options])

    @jsii.member(jsii_name="forward")
    @builtins.classmethod
    def forward(
        cls,
        target_groups: typing.List["IApplicationTargetGroup"],
        *,
        stickiness_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "ListenerAction":
        """Forward to one or more Target Groups.

        :param target_groups: -
        :param stickiness_duration: For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#forward-actions
        """
        options = ForwardOptions(stickiness_duration=stickiness_duration)

        return jsii.sinvoke(cls, "forward", [target_groups, options])

    @jsii.member(jsii_name="redirect")
    @builtins.classmethod
    def redirect(
        cls,
        *,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[builtins.bool] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> "ListenerAction":
        """Redirect to a different URI.

        A URI consists of the following components:
        protocol://hostname:port/path?query. You must modify at least one of the
        following components to avoid a redirect loop: protocol, hostname, port, or
        path. Any components that you do not modify retain their original values.

        You can reuse URI components using the following reserved keywords:

        - ``#{protocol}``
        - ``#{host}``
        - ``#{port}``
        - ``#{path}`` (the leading "/" is removed)
        - ``#{query}``

        For example, you can change the path to "/new/#{path}", the hostname to
        "example.#{host}", or the query to "#{query}&value=xyz".

        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: - No change
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: - No change
        :param permanent: The HTTP redirect code. The redirect is either permanent (HTTP 301) or temporary (HTTP 302). Default: false
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: - No change
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: - No change
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: - No change

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#redirect-actions
        """
        options = RedirectOptions(
            host=host,
            path=path,
            permanent=permanent,
            port=port,
            protocol=protocol,
            query=query,
        )

        return jsii.sinvoke(cls, "redirect", [options])

    @jsii.member(jsii_name="weightedForward")
    @builtins.classmethod
    def weighted_forward(
        cls,
        target_groups: typing.List["WeightedTargetGroup"],
        *,
        stickiness_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "ListenerAction":
        """Forward to one or more Target Groups which are weighted differently.

        :param target_groups: -
        :param stickiness_duration: For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#forward-actions
        """
        options = ForwardOptions(stickiness_duration=stickiness_duration)

        return jsii.sinvoke(cls, "weightedForward", [target_groups, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: aws_cdk.core.Construct,
        listener: IApplicationListener,
        associating_construct: typing.Optional[aws_cdk.core.IConstruct] = None,
    ) -> None:
        """Called when the action is being used in a listener.

        :param scope: -
        :param listener: -
        :param associating_construct: -
        """
        return jsii.invoke(self, "bind", [scope, listener, associating_construct])

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        """Render the actions in this chain."""
        return jsii.invoke(self, "renderActions", [])

    @jsii.member(jsii_name="renumber")
    def _renumber(
        self,
        actions: typing.List[CfnListener.ActionProperty],
    ) -> typing.List[CfnListener.ActionProperty]:
        """Renumber the "order" fields in the actions array.

        We don't number for 0 or 1 elements, but otherwise number them 1...#actions
        so ELB knows about the right order.

        Do this in ``ListenerAction`` instead of in ``Listener`` so that we give
        users the opportunity to override by subclassing and overriding ``renderActions``.

        :param actions: -
        """
        return jsii.invoke(self, "renumber", [actions])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="next")
    def _next(self) -> typing.Optional["ListenerAction"]:
        return jsii.get(self, "next")


@jsii.implements(IListenerCertificate)
class ListenerCertificate(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ListenerCertificate",
):
    """A certificate source for an ELBv2 listener."""

    def __init__(self, certificate_arn: builtins.str) -> None:
        """
        :param certificate_arn: -
        """
        jsii.create(ListenerCertificate, self, [certificate_arn])

    @jsii.member(jsii_name="fromArn")
    @builtins.classmethod
    def from_arn(cls, certificate_arn: builtins.str) -> "ListenerCertificate":
        """Use any certificate, identified by its ARN, as a listener certificate.

        :param certificate_arn: -
        """
        return jsii.sinvoke(cls, "fromArn", [certificate_arn])

    @jsii.member(jsii_name="fromCertificateManager")
    @builtins.classmethod
    def from_certificate_manager(
        cls,
        acm_certificate: aws_cdk.aws_certificatemanager.ICertificate,
    ) -> "ListenerCertificate":
        """Use an ACM certificate as a listener certificate.

        :param acm_certificate: -
        """
        return jsii.sinvoke(cls, "fromCertificateManager", [acm_certificate])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        """The ARN of the certificate to use."""
        return jsii.get(self, "certificateArn")


class ListenerCondition(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ListenerCondition",
):
    """ListenerCondition providers definition."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ListenerConditionProxy

    def __init__(self) -> None:
        jsii.create(ListenerCondition, self, [])

    @jsii.member(jsii_name="hostHeaders")
    @builtins.classmethod
    def host_headers(cls, values: typing.List[builtins.str]) -> "ListenerCondition":
        """Create a host-header listener rule condition.

        :param values: Hosts for host headers.
        """
        return jsii.sinvoke(cls, "hostHeaders", [values])

    @jsii.member(jsii_name="httpHeader")
    @builtins.classmethod
    def http_header(
        cls,
        name: builtins.str,
        values: typing.List[builtins.str],
    ) -> "ListenerCondition":
        """Create a http-header listener rule condition.

        :param name: HTTP header name.
        :param values: HTTP header values.
        """
        return jsii.sinvoke(cls, "httpHeader", [name, values])

    @jsii.member(jsii_name="httpRequestMethods")
    @builtins.classmethod
    def http_request_methods(
        cls,
        values: typing.List[builtins.str],
    ) -> "ListenerCondition":
        """Create a http-request-method listener rule condition.

        :param values: HTTP request methods.
        """
        return jsii.sinvoke(cls, "httpRequestMethods", [values])

    @jsii.member(jsii_name="pathPatterns")
    @builtins.classmethod
    def path_patterns(cls, values: typing.List[builtins.str]) -> "ListenerCondition":
        """Create a path-pattern listener rule condition.

        :param values: Path patterns.
        """
        return jsii.sinvoke(cls, "pathPatterns", [values])

    @jsii.member(jsii_name="queryStrings")
    @builtins.classmethod
    def query_strings(
        cls,
        values: typing.List["QueryStringCondition"],
    ) -> "ListenerCondition":
        """Create a query-string listener rule condition.

        :param values: Query string key/value pairs.
        """
        return jsii.sinvoke(cls, "queryStrings", [values])

    @jsii.member(jsii_name="sourceIps")
    @builtins.classmethod
    def source_ips(cls, values: typing.List[builtins.str]) -> "ListenerCondition":
        """Create a source-ip listener rule condition.

        :param values: Source ips.
        """
        return jsii.sinvoke(cls, "sourceIps", [values])

    @jsii.member(jsii_name="renderRawCondition")
    @abc.abstractmethod
    def render_raw_condition(self) -> typing.Any:
        """Render the raw Cfn listener rule condition object."""
        ...


class _ListenerConditionProxy(ListenerCondition):
    @jsii.member(jsii_name="renderRawCondition")
    def render_raw_condition(self) -> typing.Any:
        """Render the raw Cfn listener rule condition object."""
        return jsii.invoke(self, "renderRawCondition", [])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.LoadBalancerTargetProps",
    jsii_struct_bases=[],
    name_mapping={"target_type": "targetType", "target_json": "targetJson"},
)
class LoadBalancerTargetProps:
    def __init__(
        self,
        *,
        target_type: "TargetType",
        target_json: typing.Any = None,
    ) -> None:
        """Result of attaching a target to load balancer.

        :param target_type: What kind of target this is.
        :param target_json: JSON representing the target's direct addition to the TargetGroup list. May be omitted if the target is going to register itself later.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_type": target_type,
        }
        if target_json is not None:
            self._values["target_json"] = target_json

    @builtins.property
    def target_type(self) -> "TargetType":
        """What kind of target this is."""
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return result

    @builtins.property
    def target_json(self) -> typing.Any:
        """JSON representing the target's direct addition to the TargetGroup list.

        May be omitted if the target is going to register itself later.
        """
        result = self._values.get("target_json")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkForwardOptions",
    jsii_struct_bases=[],
    name_mapping={"stickiness_duration": "stickinessDuration"},
)
class NetworkForwardOptions:
    def __init__(
        self,
        *,
        stickiness_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Options for ``NetworkListenerAction.forward()``.

        :param stickiness_duration: For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if stickiness_duration is not None:
            self._values["stickiness_duration"] = stickiness_duration

    @builtins.property
    def stickiness_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """For how long clients should be directed to the same target group.

        Range between 1 second and 7 days.

        :default: - No stickiness
        """
        result = self._values.get("stickiness_duration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkForwardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INetworkListener)
class NetworkListener(
    BaseListener,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListener",
):
    """Define a Network Listener.

    :resource: AWS::ElasticLoadBalancingV2::Listener
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer: INetworkLoadBalancer,
        port: jsii.Number,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param load_balancer: The load balancer to attach this listener to.
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.
        """
        props = NetworkListenerProps(
            load_balancer=load_balancer,
            port=port,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        jsii.create(NetworkListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromLookup")
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener_protocol: typing.Optional["Protocol"] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> INetworkListener:
        """Looks up a network listener.

        :param scope: -
        :param id: -
        :param listener_protocol: Protocol of the listener port. Default: - listener is not filtered by protocol
        :param listener_port: Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags
        """
        options = NetworkListenerLookupOptions(
            listener_protocol=listener_protocol,
            listener_port=listener_port,
            load_balancer_arn=load_balancer_arn,
            load_balancer_tags=load_balancer_tags,
        )

        return jsii.sinvoke(cls, "fromLookup", [scope, id, options])

    @jsii.member(jsii_name="fromNetworkListenerArn")
    @builtins.classmethod
    def from_network_listener_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        network_listener_arn: builtins.str,
    ) -> INetworkListener:
        """Import an existing listener.

        :param scope: -
        :param id: -
        :param network_listener_arn: -
        """
        return jsii.sinvoke(cls, "fromNetworkListenerArn", [scope, id, network_listener_arn])

    @jsii.member(jsii_name="addAction")
    def add_action(self, _id: builtins.str, *, action: "NetworkListenerAction") -> None:
        """Perform the given Action on incoming requests.

        This allows full control of the default Action of the load balancer,
        including weighted forwarding. See the ``NetworkListenerAction`` class for
        all options.

        :param _id: -
        :param action: Action to perform.
        """
        props = AddNetworkActionProps(action=action)

        return jsii.invoke(self, "addAction", [_id, props])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        _id: builtins.str,
        *target_groups: "INetworkTargetGroup",
    ) -> None:
        """Load balance incoming requests to the given target groups.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use ``addAction()``.

        :param _id: -
        :param target_groups: -
        """
        return jsii.invoke(self, "addTargetGroups", [_id, *target_groups])

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        protocol: typing.Optional["Protocol"] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.List[INetworkLoadBalancerTarget]] = None,
    ) -> "NetworkTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates a NetworkTargetGroup for the targets
        involved, and a 'forward' action to route traffic to the given TargetGroup.

        If you want more control over the precise setup, create the TargetGroup
        and use ``addAction`` yourself.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param protocol: Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - inherits the protocol of the listener
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.

        :return: The newly created target group
        """
        props = AddNetworkTargetsProps(
            port=port,
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            protocol=protocol,
            proxy_protocol_v2=proxy_protocol_v2,
            target_group_name=target_group_name,
            targets=targets,
        )

        return jsii.invoke(self, "addTargets", [id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> INetworkLoadBalancer:
        """The load balancer this listener is attached to."""
        return jsii.get(self, "loadBalancer")


@jsii.implements(IListenerAction)
class NetworkListenerAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListenerAction",
):
    """What to do when a client makes a request to a listener.

    Some actions can be combined with other ones (specifically,
    you can perform authentication before serving the request).

    Multiple actions form a linked chain; the chain must always terminate in a
    *(weighted)forward*, *fixedResponse* or *redirect* action.

    If an action supports chaining, the next action can be indicated
    by passing it in the ``next`` property.
    """

    def __init__(
        self,
        action_json: CfnListener.ActionProperty,
        next: typing.Optional["NetworkListenerAction"] = None,
    ) -> None:
        """Create an instance of NetworkListenerAction.

        The default class should be good enough for most cases and
        should be created by using one of the static factory functions,
        but allow overriding to make sure we allow flexibility for the future.

        :param action_json: -
        :param next: -
        """
        jsii.create(NetworkListenerAction, self, [action_json, next])

    @jsii.member(jsii_name="forward")
    @builtins.classmethod
    def forward(
        cls,
        target_groups: typing.List["INetworkTargetGroup"],
        *,
        stickiness_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "NetworkListenerAction":
        """Forward to one or more Target Groups.

        :param target_groups: -
        :param stickiness_duration: For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness
        """
        options = NetworkForwardOptions(stickiness_duration=stickiness_duration)

        return jsii.sinvoke(cls, "forward", [target_groups, options])

    @jsii.member(jsii_name="weightedForward")
    @builtins.classmethod
    def weighted_forward(
        cls,
        target_groups: typing.List["NetworkWeightedTargetGroup"],
        *,
        stickiness_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> "NetworkListenerAction":
        """Forward to one or more Target Groups which are weighted differently.

        :param target_groups: -
        :param stickiness_duration: For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness
        """
        options = NetworkForwardOptions(stickiness_duration=stickiness_duration)

        return jsii.sinvoke(cls, "weightedForward", [target_groups, options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, listener: INetworkListener) -> None:
        """Called when the action is being used in a listener.

        :param scope: -
        :param listener: -
        """
        return jsii.invoke(self, "bind", [scope, listener])

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        """Render the actions in this chain."""
        return jsii.invoke(self, "renderActions", [])

    @jsii.member(jsii_name="renumber")
    def _renumber(
        self,
        actions: typing.List[CfnListener.ActionProperty],
    ) -> typing.List[CfnListener.ActionProperty]:
        """Renumber the "order" fields in the actions array.

        We don't number for 0 or 1 elements, but otherwise number them 1...#actions
        so ELB knows about the right order.

        Do this in ``NetworkListenerAction`` instead of in ``Listener`` so that we give
        users the opportunity to override by subclassing and overriding ``renderActions``.

        :param actions: -
        """
        return jsii.invoke(self, "renumber", [actions])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="next")
    def _next(self) -> typing.Optional["NetworkListenerAction"]:
        return jsii.get(self, "next")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListenerLookupOptions",
    jsii_struct_bases=[BaseListenerLookupOptions],
    name_mapping={
        "listener_port": "listenerPort",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "listener_protocol": "listenerProtocol",
    },
)
class NetworkListenerLookupOptions(BaseListenerLookupOptions):
    def __init__(
        self,
        *,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        listener_protocol: typing.Optional["Protocol"] = None,
    ) -> None:
        """Options for looking up a network listener.

        :param listener_port: Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags
        :param listener_protocol: Protocol of the listener port. Default: - listener is not filtered by protocol
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags
        if listener_protocol is not None:
            self._values["listener_protocol"] = listener_protocol

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Filter listeners by listener port.

        :default: - does not filter by listener port
        """
        result = self._values.get("listener_port")
        return result

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Filter listeners by associated load balancer arn.

        :default: - does not filter by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Filter listeners by associated load balancer tags.

        :default: - does not filter by load balancer tags
        """
        result = self._values.get("load_balancer_tags")
        return result

    @builtins.property
    def listener_protocol(self) -> typing.Optional["Protocol"]:
        """Protocol of the listener port.

        :default: - listener is not filtered by protocol
        """
        result = self._values.get("listener_protocol")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkListenerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListenerProps",
    jsii_struct_bases=[BaseNetworkListenerProps],
    name_mapping={
        "port": "port",
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
        "load_balancer": "loadBalancer",
    },
)
class NetworkListenerProps(BaseNetworkListenerProps):
    def __init__(
        self,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional[NetworkListenerAction] = None,
        default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
        load_balancer: INetworkLoadBalancer,
    ) -> None:
        """Properties for a Network Listener attached to a Load Balancer.

        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.
        :param load_balancer: The load balancer to attach this listener to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
            "load_balancer": load_balancer,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests."""
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return result

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List[IListenerCertificate]]:
        """Certificate list of ACM cert ARNs.

        :default: - No certificates.
        """
        result = self._values.get("certificates")
        return result

    @builtins.property
    def default_action(self) -> typing.Optional[NetworkListenerAction]:
        """Default action to take for requests to this listener.

        This allows full control of the default Action of the load balancer,
        including weighted forwarding. See the ``NetworkListenerAction`` class for
        all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.
        """
        result = self._values.get("default_action")
        return result

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["INetworkTargetGroup"]]:
        """Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.
        """
        result = self._values.get("default_target_groups")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - TLS if certificates are provided. TCP otherwise.
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        """SSL Policy.

        :default: - Current predefined security policy.
        """
        result = self._values.get("ssl_policy")
        return result

    @builtins.property
    def load_balancer(self) -> INetworkLoadBalancer:
        """The load balancer to attach this listener to."""
        result = self._values.get("load_balancer")
        assert result is not None, "Required property 'load_balancer' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INetworkLoadBalancer)
class NetworkLoadBalancer(
    BaseLoadBalancer,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancer",
):
    """Define a new network load balancer.

    :resource: AWS::ElasticLoadBalancingV2::LoadBalancer
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cross_zone_enabled: typing.Optional[builtins.bool] = None,
        vpc: aws_cdk.aws_ec2.IVpc,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cross_zone_enabled: Indicates whether cross-zone load balancing is enabled. Default: false
        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Which subnets place the load balancer in. Default: - the Vpc default strategy.
        """
        props = NetworkLoadBalancerProps(
            cross_zone_enabled=cross_zone_enabled,
            vpc=vpc,
            deletion_protection=deletion_protection,
            internet_facing=internet_facing,
            load_balancer_name=load_balancer_name,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(NetworkLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromLookup")
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> INetworkLoadBalancer:
        """Looks up the network load balancer.

        :param scope: -
        :param id: -
        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        """
        options = NetworkLoadBalancerLookupOptions(
            load_balancer_arn=load_balancer_arn, load_balancer_tags=load_balancer_tags
        )

        return jsii.sinvoke(cls, "fromLookup", [scope, id, options])

    @jsii.member(jsii_name="fromNetworkLoadBalancerAttributes")
    @builtins.classmethod
    def from_network_load_balancer_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> INetworkLoadBalancer:
        """
        :param scope: -
        :param id: -
        :param load_balancer_arn: ARN of the load balancer.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param vpc: The VPC to associate with the load balancer. Default: - When not provided, listeners cannot be created on imported load balancers.
        """
        attrs = NetworkLoadBalancerAttributes(
            load_balancer_arn=load_balancer_arn,
            load_balancer_canonical_hosted_zone_id=load_balancer_canonical_hosted_zone_id,
            load_balancer_dns_name=load_balancer_dns_name,
            vpc=vpc,
        )

        return jsii.sinvoke(cls, "fromNetworkLoadBalancerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional[NetworkListenerAction] = None,
        default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> NetworkListener:
        """Add a listener to this load balancer.

        :param id: -
        :param port: The port on which the listener listens for requests.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: SSL Policy. Default: - Current predefined security policy.

        :return: The newly created listener
        """
        props = BaseNetworkListenerProps(
            port=port,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(
        self,
        bucket: aws_cdk.aws_s3.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        """Enable access logging for this load balancer.

        A region must be specified on the stack containing the load balancer; you cannot enable logging on
        environment-agnostic stacks. See https://docs.aws.amazon.com/cdk/latest/guide/environments.html

        This is extending the BaseLoadBalancer.logAccessLogs method to match the bucket permissions described
        at https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-access-logs.html#access-logging-bucket-requirements

        :param bucket: -
        :param prefix: -
        """
        return jsii.invoke(self, "logAccessLogs", [bucket, prefix])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Network Load Balancer.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveFlowCount")
    def metric_active_flow_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of concurrent TCP flows (or connections) from clients to targets.

        This metric includes connections in the SYN_SENT and ESTABLISHED states.
        TCP connections are not terminated at the load balancer, so a client
        opening a TCP connection to a target counts as a single flow.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricActiveFlowCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of load balancer capacity units (LCU) used by your load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(deprecated) The number of targets that are considered healthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :deprecated: use ``NetworkTargetGroup.metricHealthyHostCount`` instead

        :stability: deprecated
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricNewFlowCount")
    def metric_new_flow_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of new TCP flows (or connections) established from clients to targets in the time period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNewFlowCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer, including TCP/IP headers.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricTcpClientResetCount")
    def metric_tcp_client_reset_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets sent from a client to a target.

        These resets are generated by the client and forwarded by the load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTcpClientResetCount", [props])

    @jsii.member(jsii_name="metricTcpElbResetCount")
    def metric_tcp_elb_reset_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets generated by the load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTcpElbResetCount", [props])

    @jsii.member(jsii_name="metricTcpTargetResetCount")
    def metric_tcp_target_reset_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets sent from a target to a client.

        These resets are generated by the target and forwarded by the load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTcpTargetResetCount", [props])

    @jsii.member(jsii_name="metricUnHealthyHostCount")
    def metric_un_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """(deprecated) The number of targets that are considered unhealthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :deprecated: use ``NetworkTargetGroup.metricUnHealthyHostCount`` instead

        :stability: deprecated
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricUnHealthyHostCount", [props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_canonical_hosted_zone_id": "loadBalancerCanonicalHostedZoneId",
        "load_balancer_dns_name": "loadBalancerDnsName",
        "vpc": "vpc",
    },
)
class NetworkLoadBalancerAttributes:
    def __init__(
        self,
        *,
        load_balancer_arn: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """Properties to reference an existing load balancer.

        :param load_balancer_arn: ARN of the load balancer.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param vpc: The VPC to associate with the load balancer. Default: - When not provided, listeners cannot be created on imported load balancers.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_arn": load_balancer_arn,
        }
        if load_balancer_canonical_hosted_zone_id is not None:
            self._values["load_balancer_canonical_hosted_zone_id"] = load_balancer_canonical_hosted_zone_id
        if load_balancer_dns_name is not None:
            self._values["load_balancer_dns_name"] = load_balancer_dns_name
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        """ARN of the load balancer."""
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return result

    @builtins.property
    def load_balancer_canonical_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        """The canonical hosted zone ID of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        result = self._values.get("load_balancer_canonical_hosted_zone_id")
        return result

    @builtins.property
    def load_balancer_dns_name(self) -> typing.Optional[builtins.str]:
        """The DNS name of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        result = self._values.get("load_balancer_dns_name")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC to associate with the load balancer.

        :default:

        - When not provided, listeners cannot be created on imported load
        balancers.
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerLookupOptions",
    jsii_struct_bases=[BaseLoadBalancerLookupOptions],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class NetworkLoadBalancerLookupOptions(BaseLoadBalancerLookupOptions):
    def __init__(
        self,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Options for looking up an NetworkLoadBalancer.

        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Find by load balancer's ARN.

        :default: - does not search by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
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
        return "NetworkLoadBalancerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerProps",
    jsii_struct_bases=[BaseLoadBalancerProps],
    name_mapping={
        "vpc": "vpc",
        "deletion_protection": "deletionProtection",
        "internet_facing": "internetFacing",
        "load_balancer_name": "loadBalancerName",
        "vpc_subnets": "vpcSubnets",
        "cross_zone_enabled": "crossZoneEnabled",
    },
)
class NetworkLoadBalancerProps(BaseLoadBalancerProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        cross_zone_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Properties for a network load balancer.

        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Which subnets place the load balancer in. Default: - the Vpc default strategy.
        :param cross_zone_enabled: Indicates whether cross-zone load balancing is enabled. Default: false
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if cross_zone_enabled is not None:
            self._values["cross_zone_enabled"] = cross_zone_enabled

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC network to place the load balancer in."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        """Indicates whether deletion protection is enabled.

        :default: false
        """
        result = self._values.get("deletion_protection")
        return result

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        """Whether the load balancer has an internet-routable address.

        :default: false
        """
        result = self._values.get("internet_facing")
        return result

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        """Name of the load balancer.

        :default: - Automatically generated name.
        """
        result = self._values.get("load_balancer_name")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Which subnets place the load balancer in.

        :default: - the Vpc default strategy.
        """
        result = self._values.get("vpc_subnets")
        return result

    @builtins.property
    def cross_zone_enabled(self) -> typing.Optional[builtins.bool]:
        """Indicates whether cross-zone load balancing is enabled.

        :default: false
        """
        result = self._values.get("cross_zone_enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroupProps",
    jsii_struct_bases=[BaseTargetGroupProps],
    name_mapping={
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "target_group_name": "targetGroupName",
        "target_type": "targetType",
        "vpc": "vpc",
        "port": "port",
        "protocol": "protocol",
        "proxy_protocol_v2": "proxyProtocolV2",
        "targets": "targets",
    },
)
class NetworkTargetGroupProps(BaseTargetGroupProps):
    def __init__(
        self,
        *,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional["TargetType"] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        port: jsii.Number,
        protocol: typing.Optional["Protocol"] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        targets: typing.Optional[typing.List[INetworkLoadBalancerTarget]] = None,
    ) -> None:
        """Properties for a new Network Target Group.

        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        :param port: The port on which the listener listens for requests.
        :param protocol: Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - TCP
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        """
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if target_type is not None:
            self._values["target_type"] = target_type
        if vpc is not None:
            self._values["vpc"] = vpc
        if protocol is not None:
            self._values["protocol"] = protocol
        if proxy_protocol_v2 is not None:
            self._values["proxy_protocol_v2"] = proxy_protocol_v2
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: 300
        """
        result = self._values.get("deregistration_delay")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        """Health check configuration.

        :default: - None.
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: - Automatically generated.
        """
        result = self._values.get("target_group_name")
        return result

    @builtins.property
    def target_type(self) -> typing.Optional["TargetType"]:
        """The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        :default: - Determined automatically.
        """
        result = self._values.get("target_type")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        :default: - undefined
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def port(self) -> jsii.Number:
        """The port on which the listener listens for requests."""
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return result

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - TCP
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def proxy_protocol_v2(self) -> typing.Optional[builtins.bool]:
        """Indicates whether Proxy Protocol version 2 is enabled.

        :default: false
        """
        result = self._values.get("proxy_protocol_v2")
        return result

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[INetworkLoadBalancerTarget]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        :default: - No targets.
        """
        result = self._values.get("targets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkWeightedTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"target_group": "targetGroup", "weight": "weight"},
)
class NetworkWeightedTargetGroup:
    def __init__(
        self,
        *,
        target_group: "INetworkTargetGroup",
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        """A Target Group and weight combination.

        :param target_group: The target group.
        :param weight: The target group's weight. Range is [0..1000). Default: 1
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_group": target_group,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def target_group(self) -> "INetworkTargetGroup":
        """The target group."""
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return result

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        """The target group's weight.

        Range is [0..1000).

        :default: 1
        """
        result = self._values.get("weight")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkWeightedTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.Protocol")
class Protocol(enum.Enum):
    """Backend protocol for network load balancers and health checks."""

    HTTP = "HTTP"
    """HTTP (ALB health checks and NLB health checks)."""
    HTTPS = "HTTPS"
    """HTTPS (ALB health checks and NLB health checks)."""
    TCP = "TCP"
    """TCP (NLB, NLB health checks)."""
    TLS = "TLS"
    """TLS (NLB)."""
    UDP = "UDP"
    """UDP (NLB)."""
    TCP_UDP = "TCP_UDP"
    """Listen to both TCP and UDP on the same port (NLB)."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.QueryStringCondition",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "key": "key"},
)
class QueryStringCondition:
    def __init__(
        self,
        *,
        value: builtins.str,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for the key/value pair of the query string.

        :param value: The query string value for the condition.
        :param key: The query string key for the condition. Default: - Any key can be matched.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def value(self) -> builtins.str:
        """The query string value for the condition."""
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        """The query string key for the condition.

        :default: - Any key can be matched.
        """
        result = self._values.get("key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryStringCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.RedirectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "path": "path",
        "permanent": "permanent",
        "port": "port",
        "protocol": "protocol",
        "query": "query",
    },
)
class RedirectOptions:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[builtins.bool] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options for ``ListenerAction.redirect()``.

        A URI consists of the following components:
        protocol://hostname:port/path?query. You must modify at least one of the
        following components to avoid a redirect loop: protocol, hostname, port, or
        path. Any components that you do not modify retain their original values.

        You can reuse URI components using the following reserved keywords:

        - ``#{protocol}``
        - ``#{host}``
        - ``#{port}``
        - ``#{path}`` (the leading "/" is removed)
        - ``#{query}``

        For example, you can change the path to "/new/#{path}", the hostname to
        "example.#{host}", or the query to "#{query}&value=xyz".

        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: - No change
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: - No change
        :param permanent: The HTTP redirect code. The redirect is either permanent (HTTP 301) or temporary (HTTP 302). Default: false
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: - No change
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: - No change
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: - No change
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if path is not None:
            self._values["path"] = path
        if permanent is not None:
            self._values["permanent"] = permanent
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        """The hostname.

        This component is not percent-encoded. The hostname can contain #{host}.

        :default: - No change
        """
        result = self._values.get("host")
        return result

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        """The absolute path, starting with the leading "/".

        This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}.

        :default: - No change
        """
        result = self._values.get("path")
        return result

    @builtins.property
    def permanent(self) -> typing.Optional[builtins.bool]:
        """The HTTP redirect code.

        The redirect is either permanent (HTTP 301) or temporary (HTTP 302).

        :default: false
        """
        result = self._values.get("permanent")
        return result

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        """The port.

        You can specify a value from 1 to 65535 or #{port}.

        :default: - No change
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        """The protocol.

        You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP.

        :default: - No change
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        """The query parameters, URL-encoded when necessary, but not percent-encoded.

        Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords.

        :default: - No change
        """
        result = self._values.get("query")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedirectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.RedirectResponse",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "host": "host",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "query": "query",
    },
)
class RedirectResponse:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        """A redirect response.

        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request
        """
        self._values: typing.Dict[str, typing.Any] = {
            "status_code": status_code,
        }
        if host is not None:
            self._values["host"] = host
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def status_code(self) -> builtins.str:
        """The HTTP redirect code (HTTP_301 or HTTP_302)."""
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return result

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        """The hostname.

        This component is not percent-encoded. The hostname can contain #{host}.

        :default: origin host of request
        """
        result = self._values.get("host")
        return result

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        """The absolute path, starting with the leading "/".

        This component is not percent-encoded.
        The path can contain #{host}, #{path}, and #{port}.

        :default: origin path of request
        """
        result = self._values.get("path")
        return result

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        """The port.

        You can specify a value from 1 to 65535 or #{port}.

        :default: origin port of request
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        """The protocol.

        You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP,
        HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP.

        :default: origin protocol of request
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        """The query parameters, URL-encoded when necessary, but not percent-encoded.

        Do not include the leading "?", as it is automatically added.
        You can specify any of the reserved keywords.

        :default: origin query string of request
        """
        result = self._values.get("query")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedirectResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.SslPolicy")
class SslPolicy(enum.Enum):
    """Elastic Load Balancing provides the following security policies for Application Load Balancers.

    We recommend the Recommended policy for general use. You can
    use the ForwardSecrecy policy if you require Forward Secrecy
    (FS).

    You can use one of the TLS policies to meet compliance and security
    standards that require disabling certain TLS protocol versions, or to
    support legacy clients that require deprecated ciphers.

    :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html
    """

    RECOMMENDED = "RECOMMENDED"
    """The recommended security policy."""
    FORWARD_SECRECY_TLS12_RES = "FORWARD_SECRECY_TLS12_RES"
    """Strong forward secrecy ciphers and TLS1.2 only."""
    FORWARD_SECRECY_TLS12 = "FORWARD_SECRECY_TLS12"
    """Forward secrecy ciphers and TLS1.2 only."""
    FORWARD_SECRECY_TLS11 = "FORWARD_SECRECY_TLS11"
    """Forward secrecy ciphers only with TLS1.1 and higher."""
    FORWARD_SECRECY = "FORWARD_SECRECY"
    """Forward secrecy ciphers only."""
    TLS12 = "TLS12"
    """TLS1.2 only and no SHA ciphers."""
    TLS12_EXT = "TLS12_EXT"
    """TLS1.2 only with all ciphers."""
    TLS11 = "TLS11"
    """TLS1.1 and higher with all ciphers."""
    LEGACY = "LEGACY"
    """Support for DES-CBC3-SHA.

    Do not use this security policy unless you must support a legacy client
    that requires the DES-CBC3-SHA cipher, which is a weak cipher.
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "target_group_arn": "targetGroupArn",
        "default_port": "defaultPort",
        "load_balancer_arns": "loadBalancerArns",
    },
)
class TargetGroupAttributes:
    def __init__(
        self,
        *,
        target_group_arn: builtins.str,
        default_port: typing.Optional[builtins.str] = None,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties to reference an existing target group.

        :param target_group_arn: ARN of the target group.
        :param default_port: (deprecated) Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_group_arn": target_group_arn,
        }
        if default_port is not None:
            self._values["default_port"] = default_port
        if load_balancer_arns is not None:
            self._values["load_balancer_arns"] = load_balancer_arns

    @builtins.property
    def target_group_arn(self) -> builtins.str:
        """ARN of the target group."""
        result = self._values.get("target_group_arn")
        assert result is not None, "Required property 'target_group_arn' is missing"
        return result

    @builtins.property
    def default_port(self) -> typing.Optional[builtins.str]:
        """(deprecated) Port target group is listening on.

        :deprecated: - This property is unused and the wrong type. No need to use it.

        :stability: deprecated
        """
        result = self._values.get("default_port")
        return result

    @builtins.property
    def load_balancer_arns(self) -> typing.Optional[builtins.str]:
        """A Token representing the list of ARNs for the load balancer routing to this target group."""
        result = self._values.get("load_balancer_arns")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITargetGroup)
class TargetGroupBase(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupBase",
):
    """Define the target of a load balancer."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TargetGroupBaseProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        base_props: BaseTargetGroupProps,
        additional_props: typing.Any,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param base_props: -
        :param additional_props: -
        """
        jsii.create(TargetGroupBase, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="addLoadBalancerTarget")
    def _add_load_balancer_target(
        self,
        *,
        target_type: "TargetType",
        target_json: typing.Any = None,
    ) -> None:
        """Register the given load balancing target as part of this group.

        :param target_type: What kind of target this is.
        :param target_json: JSON representing the target's direct addition to the TargetGroup list. May be omitted if the target is going to register itself later.
        """
        props = LoadBalancerTargetProps(
            target_type=target_type, target_json=target_json
        )

        return jsii.invoke(self, "addLoadBalancerTarget", [props])

    @jsii.member(jsii_name="configureHealthCheck")
    def configure_health_check(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        healthy_http_codes: typing.Optional[builtins.str] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[aws_cdk.core.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[Protocol] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Set/replace the target group's health check.

        :param enabled: Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance or ip, health checks are always enabled and cannot be disabled. Default: - Determined automatically.
        :param healthy_http_codes: HTTP code to use when checking for a successful response from a target. For Application Load Balancers, you can specify values between 200 and 499, and the default value is 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
        :param healthy_threshold_count: The number of consecutive health checks successes required before considering an unhealthy target healthy. For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3. Default: 5 for ALBs, 3 for NLBs
        :param interval: The approximate number of seconds between health checks for an individual target. Default: Duration.seconds(30)
        :param path: The ping path destination where Elastic Load Balancing sends health check requests. Default: /
        :param port: The port that the load balancer uses when performing health checks on the targets. Default: 'traffic-port'
        :param protocol: The protocol the load balancer uses when performing health checks on targets. The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP. The TLS, UDP, and TCP_UDP protocols are not supported for health checks. Default: HTTP for ALBs, TCP for NLBs
        :param timeout: The amount of time, in seconds, during which no response from a target means a failed health check. For Application Load Balancers, the range is 2-60 seconds and the default is 5 seconds. For Network Load Balancers, this is 10 seconds for TCP and HTTPS health checks and 6 seconds for HTTP health checks. Default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        :param unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. For Application Load Balancers, the default is 2. For Network Load Balancers, this value must be the same as the healthy threshold count. Default: 2
        """
        health_check = HealthCheck(
            enabled=enabled,
            healthy_http_codes=healthy_http_codes,
            healthy_threshold_count=healthy_threshold_count,
            interval=interval,
            path=path,
            port=port,
            protocol=protocol,
            timeout=timeout,
            unhealthy_threshold_count=unhealthy_threshold_count,
        )

        return jsii.invoke(self, "configureHealthCheck", [health_check])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(
        self,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        """Set a non-standard attribute on the target group.

        :param key: -
        :param value: -

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#target-group-attributes
        """
        return jsii.invoke(self, "setAttribute", [key, value])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultPort")
    def _default_port(self) -> jsii.Number:
        """Default port configured for members of this target group."""
        return jsii.get(self, "defaultPort")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    @abc.abstractmethod
    def first_load_balancer_full_name(self) -> builtins.str:
        """Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 123456789
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> builtins.str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        return jsii.get(self, "loadBalancerArns")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.core.IDependable:
        """List of constructs that need to be depended on to ensure the TargetGroup is associated to a load balancer."""
        return jsii.get(self, "loadBalancerAttached")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerAttachedDependencies")
    def _load_balancer_attached_dependencies(self) -> aws_cdk.core.ConcreteDependable:
        """Configurable dependable with all resources that lead to load balancer attachment."""
        return jsii.get(self, "loadBalancerAttachedDependencies")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        """The ARN of the target group."""
        return jsii.get(self, "targetGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupFullName")
    def target_group_full_name(self) -> builtins.str:
        """The full name of the target group."""
        return jsii.get(self, "targetGroupFullName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupLoadBalancerArns")
    def target_group_load_balancer_arns(self) -> typing.List[builtins.str]:
        """ARNs of load balancers load balancing to this TargetGroup."""
        return jsii.get(self, "targetGroupLoadBalancerArns")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> builtins.str:
        """The name of the target group."""
        return jsii.get(self, "targetGroupName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> HealthCheck:
        return jsii.get(self, "healthCheck")

    @health_check.setter # type: ignore
    def health_check(self, value: HealthCheck) -> None:
        jsii.set(self, "healthCheck", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetType")
    def _target_type(self) -> typing.Optional["TargetType"]:
        """The types of the directly registered members of this target group."""
        return jsii.get(self, "targetType")

    @_target_type.setter # type: ignore
    def _target_type(self, value: typing.Optional["TargetType"]) -> None:
        jsii.set(self, "targetType", value)


class _TargetGroupBaseProxy(TargetGroupBase):
    @builtins.property # type: ignore
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> builtins.str:
        """Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 123456789
        """
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupImportProps",
    jsii_struct_bases=[TargetGroupAttributes],
    name_mapping={
        "target_group_arn": "targetGroupArn",
        "default_port": "defaultPort",
        "load_balancer_arns": "loadBalancerArns",
    },
)
class TargetGroupImportProps(TargetGroupAttributes):
    def __init__(
        self,
        *,
        target_group_arn: builtins.str,
        default_port: typing.Optional[builtins.str] = None,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties to reference an existing target group.

        :param target_group_arn: ARN of the target group.
        :param default_port: (deprecated) Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.

        :deprecated: Use TargetGroupAttributes instead

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_group_arn": target_group_arn,
        }
        if default_port is not None:
            self._values["default_port"] = default_port
        if load_balancer_arns is not None:
            self._values["load_balancer_arns"] = load_balancer_arns

    @builtins.property
    def target_group_arn(self) -> builtins.str:
        """ARN of the target group."""
        result = self._values.get("target_group_arn")
        assert result is not None, "Required property 'target_group_arn' is missing"
        return result

    @builtins.property
    def default_port(self) -> typing.Optional[builtins.str]:
        """(deprecated) Port target group is listening on.

        :deprecated: - This property is unused and the wrong type. No need to use it.

        :stability: deprecated
        """
        result = self._values.get("default_port")
        return result

    @builtins.property
    def load_balancer_arns(self) -> typing.Optional[builtins.str]:
        """A Token representing the list of ARNs for the load balancer routing to this target group."""
        result = self._values.get("load_balancer_arns")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGroupImportProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetType")
class TargetType(enum.Enum):
    """How to interpret the load balancing target identifiers."""

    INSTANCE = "INSTANCE"
    """Targets identified by instance ID."""
    IP = "IP"
    """Targets identified by IP address."""
    LAMBDA = "LAMBDA"
    """Target is a single Lambda Function."""


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.UnauthenticatedAction")
class UnauthenticatedAction(enum.Enum):
    """What to do with unauthenticated requests."""

    DENY = "DENY"
    """Return an HTTP 401 Unauthorized error."""
    ALLOW = "ALLOW"
    """Allow the request to be forwarded to the target."""
    AUTHENTICATE = "AUTHENTICATE"
    """Redirect the request to the IdP authorization endpoint."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.WeightedTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"target_group": "targetGroup", "weight": "weight"},
)
class WeightedTargetGroup:
    def __init__(
        self,
        *,
        target_group: "IApplicationTargetGroup",
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        """A Target Group and weight combination.

        :param target_group: The target group.
        :param weight: The target group's weight. Range is [0..1000). Default: 1
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_group": target_group,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def target_group(self) -> "IApplicationTargetGroup":
        """The target group."""
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return result

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        """The target group's weight.

        Range is [0..1000).

        :default: 1
        """
        result = self._values.get("weight")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WeightedTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationActionProps",
    jsii_struct_bases=[AddRuleProps],
    name_mapping={
        "conditions": "conditions",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "priority": "priority",
        "action": "action",
    },
)
class AddApplicationActionProps(AddRuleProps):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        action: ListenerAction,
    ) -> None:
        """Properties for adding a new action to a listener.

        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param action: Action to perform.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No host condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No path condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults
        """
        result = self._values.get("priority")
        return result

    @builtins.property
    def action(self) -> ListenerAction:
        """Action to perform."""
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddApplicationActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetGroupsProps",
    jsii_struct_bases=[AddRuleProps],
    name_mapping={
        "conditions": "conditions",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "priority": "priority",
        "target_groups": "targetGroups",
    },
)
class AddApplicationTargetGroupsProps(AddRuleProps):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        target_groups: typing.List["IApplicationTargetGroup"],
    ) -> None:
        """Properties for adding a new target group to a listener.

        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param target_groups: Target groups to forward requests to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "target_groups": target_groups,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No host condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No path condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults
        """
        result = self._values.get("priority")
        return result

    @builtins.property
    def target_groups(self) -> typing.List["IApplicationTargetGroup"]:
        """Target groups to forward requests to."""
        result = self._values.get("target_groups")
        assert result is not None, "Required property 'target_groups' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddApplicationTargetGroupsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetsProps",
    jsii_struct_bases=[AddRuleProps],
    name_mapping={
        "conditions": "conditions",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "priority": "priority",
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "port": "port",
        "protocol": "protocol",
        "slow_start": "slowStart",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "target_group_name": "targetGroupName",
        "targets": "targets",
    },
)
class AddApplicationTargetsProps(AddRuleProps):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        slow_start: typing.Optional[aws_cdk.core.Duration] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.List[IApplicationLoadBalancerTarget]] = None,
    ) -> None:
        """Properties for adding new targets to a listener.

        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        """
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if priority is not None:
            self._values["priority"] = priority
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if slow_start is not None:
            self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No host condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No path condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults
        """
        result = self._values.get("priority")
        return result

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: Duration.minutes(5)
        """
        result = self._values.get("deregistration_delay")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        """Health check configuration.

        :default: No health check
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        :default: Determined from protocol if known
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        """The protocol to use.

        :default: Determined from port if known
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def slow_start(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

        The range is 30-900 seconds (15 minutes).

        :default: 0
        """
        result = self._values.get("slow_start")
        return result

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The stickiness cookie expiration period.

        Setting this value enables load balancer stickiness.

        After this period, the cookie is considered stale. The minimum value is
        1 second and the maximum value is 7 days (604800 seconds).

        :default: Stickiness disabled
        """
        result = self._values.get("stickiness_cookie_duration")
        return result

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: Automatically generated
        """
        result = self._values.get("target_group_name")
        return result

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[IApplicationLoadBalancerTarget]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. All target must be of the same type.
        """
        result = self._values.get("targets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddApplicationTargetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddFixedResponseProps",
    jsii_struct_bases=[AddRuleProps, FixedResponse],
    name_mapping={
        "conditions": "conditions",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "priority": "priority",
        "status_code": "statusCode",
        "content_type": "contentType",
        "message_body": "messageBody",
    },
)
class AddFixedResponseProps(AddRuleProps, FixedResponse):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        status_code: builtins.str,
        content_type: typing.Optional[ContentType] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties for adding a fixed response to a listener.

        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message

        :deprecated: Use ``ApplicationListener.addAction`` instead.

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "status_code": status_code,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if priority is not None:
            self._values["priority"] = priority
        if content_type is not None:
            self._values["content_type"] = content_type
        if message_body is not None:
            self._values["message_body"] = message_body

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No host condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No path condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults
        """
        result = self._values.get("priority")
        return result

    @builtins.property
    def status_code(self) -> builtins.str:
        """The HTTP response code (2XX, 4XX or 5XX)."""
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return result

    @builtins.property
    def content_type(self) -> typing.Optional[ContentType]:
        """The content type.

        :default: text/plain
        """
        result = self._values.get("content_type")
        return result

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        """The message.

        :default: no message
        """
        result = self._values.get("message_body")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddFixedResponseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddRedirectResponseProps",
    jsii_struct_bases=[AddRuleProps, RedirectResponse],
    name_mapping={
        "conditions": "conditions",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "priority": "priority",
        "status_code": "statusCode",
        "host": "host",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "query": "query",
    },
)
class AddRedirectResponseProps(AddRuleProps, RedirectResponse):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties for adding a redirect response to a listener.

        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request

        :deprecated: Use ``ApplicationListener.addAction`` instead.

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "status_code": status_code,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if priority is not None:
            self._values["priority"] = priority
        if host is not None:
            self._values["host"] = host
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No host condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No path condition

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults
        """
        result = self._values.get("priority")
        return result

    @builtins.property
    def status_code(self) -> builtins.str:
        """The HTTP redirect code (HTTP_301 or HTTP_302)."""
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return result

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        """The hostname.

        This component is not percent-encoded. The hostname can contain #{host}.

        :default: origin host of request
        """
        result = self._values.get("host")
        return result

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        """The absolute path, starting with the leading "/".

        This component is not percent-encoded.
        The path can contain #{host}, #{path}, and #{port}.

        :default: origin path of request
        """
        result = self._values.get("path")
        return result

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        """The port.

        You can specify a value from 1 to 65535 or #{port}.

        :default: origin port of request
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        """The protocol.

        You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP,
        HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP.

        :default: origin protocol of request
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        """The query parameters, URL-encoded when necessary, but not percent-encoded.

        Do not include the leading "?", as it is automatically added.
        You can specify any of the reserved keywords.

        :default: origin query string of request
        """
        result = self._values.get("query")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRedirectResponseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApplicationListener)
class ApplicationListener(
    BaseListener,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListener",
):
    """Define an ApplicationListener.

    :resource: AWS::ElasticLoadBalancingV2::Listener
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer: "IApplicationLoadBalancer",
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param load_balancer: The load balancer to attach this listener to.
        :param certificate_arns: (deprecated) The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props = ApplicationListenerProps(
            load_balancer=load_balancer,
            certificate_arns=certificate_arns,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            open=open,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        jsii.create(ApplicationListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationListenerAttributes")
    @builtins.classmethod
    def from_application_listener_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener_arn: builtins.str,
        default_port: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        security_group_allows_all_outbound: typing.Optional[builtins.bool] = None,
        security_group_id: typing.Optional[builtins.str] = None,
    ) -> IApplicationListener:
        """Import an existing listener.

        :param scope: -
        :param id: -
        :param listener_arn: ARN of the listener.
        :param default_port: The default port on which this listener is listening.
        :param security_group: Security group of the load balancer this listener is associated with.
        :param security_group_allows_all_outbound: (deprecated) Whether the imported security group allows all outbound traffic or not when imported using ``securityGroupId``. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param security_group_id: (deprecated) Security group ID of the load balancer this listener is associated with.
        """
        attrs = ApplicationListenerAttributes(
            listener_arn=listener_arn,
            default_port=default_port,
            security_group=security_group,
            security_group_allows_all_outbound=security_group_allows_all_outbound,
            security_group_id=security_group_id,
        )

        return jsii.sinvoke(cls, "fromApplicationListenerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromLookup")
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener_arn: typing.Optional[builtins.str] = None,
        listener_protocol: typing.Optional[ApplicationProtocol] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> IApplicationListener:
        """Look up an ApplicationListener.

        :param scope: -
        :param id: -
        :param listener_arn: ARN of the listener to look up. Default: - does not filter by listener arn
        :param listener_protocol: Filter listeners by listener protocol. Default: - does not filter by listener protocol
        :param listener_port: Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags
        """
        options = ApplicationListenerLookupOptions(
            listener_arn=listener_arn,
            listener_protocol=listener_protocol,
            listener_port=listener_port,
            load_balancer_arn=load_balancer_arn,
            load_balancer_tags=load_balancer_tags,
        )

        return jsii.sinvoke(cls, "fromLookup", [scope, id, options])

    @jsii.member(jsii_name="addAction")
    def add_action(
        self,
        id: builtins.str,
        *,
        action: ListenerAction,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Perform the given default action on incoming requests.

        This allows full control of the default action of the load balancer,
        including Action chaining, fixed responses and redirect responses. See
        the ``ListenerAction`` class for all options.

        It's possible to add routing conditions to the Action added in this way.
        At least one Action must be added without conditions (which becomes the
        default Action).

        :param id: -
        :param action: Action to perform.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props = AddApplicationActionProps(
            action=action,
            conditions=conditions,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            priority=priority,
        )

        return jsii.invoke(self, "addAction", [id, props])

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(
        self,
        id: builtins.str,
        arns: typing.List[builtins.str],
    ) -> None:
        """(deprecated) Add one or more certificates to this listener.

        After the first certificate, this creates ApplicationListenerCertificates
        resources since cloudformation requires the certificates array on the
        listener resource to have a length of 1.

        :param id: -
        :param arns: -

        :deprecated: Use ``addCertificates`` instead.

        :stability: deprecated
        """
        return jsii.invoke(self, "addCertificateArns", [id, arns])

    @jsii.member(jsii_name="addCertificates")
    def add_certificates(
        self,
        id: builtins.str,
        certificates: typing.List[IListenerCertificate],
    ) -> None:
        """Add one or more certificates to this listener.

        After the first certificate, this creates ApplicationListenerCertificates
        resources since cloudformation requires the certificates array on the
        listener resource to have a length of 1.

        :param id: -
        :param certificates: -
        """
        return jsii.invoke(self, "addCertificates", [id, certificates])

    @jsii.member(jsii_name="addFixedResponse")
    def add_fixed_response(
        self,
        id: builtins.str,
        *,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        status_code: builtins.str,
        content_type: typing.Optional[ContentType] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Add a fixed response.

        :param id: -
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP response code (2XX, 4XX or 5XX).
        :param content_type: The content type. Default: text/plain
        :param message_body: The message. Default: no message

        :deprecated: Use ``addAction()`` instead

        :stability: deprecated
        """
        props = AddFixedResponseProps(
            conditions=conditions,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            priority=priority,
            status_code=status_code,
            content_type=content_type,
            message_body=message_body,
        )

        return jsii.invoke(self, "addFixedResponse", [id, props])

    @jsii.member(jsii_name="addRedirectResponse")
    def add_redirect_response(
        self,
        id: builtins.str,
        *,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
        status_code: builtins.str,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Add a redirect response.

        :param id: -
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param status_code: The HTTP redirect code (HTTP_301 or HTTP_302).
        :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: origin host of request
        :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: origin path of request
        :param port: The port. You can specify a value from 1 to 65535 or #{port}. Default: origin port of request
        :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: origin protocol of request
        :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: origin query string of request

        :deprecated: Use ``addAction()`` instead

        :stability: deprecated
        """
        props = AddRedirectResponseProps(
            conditions=conditions,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            priority=priority,
            status_code=status_code,
            host=host,
            path=path,
            port=port,
            protocol=protocol,
            query=query,
        )

        return jsii.invoke(self, "addRedirectResponse", [id, props])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        id: builtins.str,
        *,
        target_groups: typing.List["IApplicationTargetGroup"],
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Load balance incoming requests to the given target groups.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use ``addAction()``.

        It's possible to add routing conditions to the TargetGroups added in this
        way. At least one TargetGroup must be added without conditions (which will
        become the default Action for this listener).

        :param id: -
        :param target_groups: Target groups to forward requests to.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props = AddApplicationTargetGroupsProps(
            target_groups=target_groups,
            conditions=conditions,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            priority=priority,
        )

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        slow_start: typing.Optional[aws_cdk.core.Duration] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.List[IApplicationLoadBalancerTarget]] = None,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved, and a 'forward' action to route traffic to the given TargetGroup.

        If you want more control over the precise setup, create the TargetGroup
        and use ``addAction`` yourself.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :return: The newly created target group
        """
        props = AddApplicationTargetsProps(
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            port=port,
            protocol=protocol,
            slow_start=slow_start,
            stickiness_cookie_duration=stickiness_cookie_duration,
            target_group_name=target_group_name,
            targets=targets,
            conditions=conditions,
            host_header=host_header,
            path_pattern=path_pattern,
            path_patterns=path_patterns,
            priority=priority,
        )

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
        port_range: aws_cdk.aws_ec2.Port,
    ) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate this listener."""
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage connections to this ApplicationListener."""
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "IApplicationLoadBalancer":
        """Load balancer this listener is associated with."""
        return jsii.get(self, "loadBalancer")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerLookupOptions",
    jsii_struct_bases=[BaseListenerLookupOptions],
    name_mapping={
        "listener_port": "listenerPort",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "listener_arn": "listenerArn",
        "listener_protocol": "listenerProtocol",
    },
)
class ApplicationListenerLookupOptions(BaseListenerLookupOptions):
    def __init__(
        self,
        *,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        listener_arn: typing.Optional[builtins.str] = None,
        listener_protocol: typing.Optional[ApplicationProtocol] = None,
    ) -> None:
        """Options for ApplicationListener lookup.

        :param listener_port: Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags
        :param listener_arn: ARN of the listener to look up. Default: - does not filter by listener arn
        :param listener_protocol: Filter listeners by listener protocol. Default: - does not filter by listener protocol
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags
        if listener_arn is not None:
            self._values["listener_arn"] = listener_arn
        if listener_protocol is not None:
            self._values["listener_protocol"] = listener_protocol

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Filter listeners by listener port.

        :default: - does not filter by listener port
        """
        result = self._values.get("listener_port")
        return result

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Filter listeners by associated load balancer arn.

        :default: - does not filter by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Filter listeners by associated load balancer tags.

        :default: - does not filter by load balancer tags
        """
        result = self._values.get("load_balancer_tags")
        return result

    @builtins.property
    def listener_arn(self) -> typing.Optional[builtins.str]:
        """ARN of the listener to look up.

        :default: - does not filter by listener arn
        """
        result = self._values.get("listener_arn")
        return result

    @builtins.property
    def listener_protocol(self) -> typing.Optional[ApplicationProtocol]:
        """Filter listeners by listener protocol.

        :default: - does not filter by listener protocol
        """
        result = self._values.get("listener_protocol")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerProps",
    jsii_struct_bases=[BaseApplicationListenerProps],
    name_mapping={
        "certificate_arns": "certificateArns",
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "open": "open",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
        "load_balancer": "loadBalancer",
    },
)
class ApplicationListenerProps(BaseApplicationListenerProps):
    def __init__(
        self,
        *,
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
        load_balancer: "IApplicationLoadBalancer",
    ) -> None:
        """Properties for defining a standalone ApplicationListener.

        :param certificate_arns: (deprecated) The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        :param load_balancer: The load balancer to attach this listener to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer": load_balancer,
        }
        if certificate_arns is not None:
            self._values["certificate_arns"] = certificate_arns
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if open is not None:
            self._values["open"] = open
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def certificate_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) The certificates to use on this listener.

        :default: - No certificates.

        :deprecated: Use the ``certificates`` property instead

        :stability: deprecated
        """
        result = self._values.get("certificate_arns")
        return result

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List[IListenerCertificate]]:
        """Certificate list of ACM cert ARNs.

        :default: - No certificates.
        """
        result = self._values.get("certificates")
        return result

    @builtins.property
    def default_action(self) -> typing.Optional[ListenerAction]:
        """Default action to take for requests to this listener.

        This allows full control of the default action of the load balancer,
        including Action chaining, fixed responses and redirect responses.

        See the ``ListenerAction`` class for all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.
        """
        result = self._values.get("default_action")
        return result

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.
        """
        result = self._values.get("default_target_groups")
        return result

    @builtins.property
    def open(self) -> typing.Optional[builtins.bool]:
        """Allow anyone to connect to this listener.

        If this is specified, the listener will be opened up to anyone who can reach it.
        For internal load balancers this is anyone in the same VPC. For public load
        balancers, this is anyone on the internet.

        If you want to be more selective about who can access this load
        balancer, set this to ``false`` and use the listener's ``connections``
        object to selectively grant access to the listener.

        :default: true
        """
        result = self._values.get("open")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        :default: - Determined from protocol if known.
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        """The protocol to use.

        :default: - Determined from port if known.
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def ssl_policy(self) -> typing.Optional[SslPolicy]:
        """The security policy that defines which ciphers and protocols are supported.

        :default: - The current predefined security policy.
        """
        result = self._values.get("ssl_policy")
        return result

    @builtins.property
    def load_balancer(self) -> "IApplicationLoadBalancer":
        """The load balancer to attach this listener to."""
        result = self._values.get("load_balancer")
        assert result is not None, "Required property 'load_balancer' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRuleProps",
    jsii_struct_bases=[BaseApplicationListenerRuleProps],
    name_mapping={
        "priority": "priority",
        "action": "action",
        "conditions": "conditions",
        "fixed_response": "fixedResponse",
        "host_header": "hostHeader",
        "path_pattern": "pathPattern",
        "path_patterns": "pathPatterns",
        "redirect_response": "redirectResponse",
        "target_groups": "targetGroups",
        "listener": "listener",
    },
)
class ApplicationListenerRuleProps(BaseApplicationListenerRuleProps):
    def __init__(
        self,
        *,
        priority: jsii.Number,
        action: typing.Optional[ListenerAction] = None,
        conditions: typing.Optional[typing.List[ListenerCondition]] = None,
        fixed_response: typing.Optional[FixedResponse] = None,
        host_header: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        path_patterns: typing.Optional[typing.List[builtins.str]] = None,
        redirect_response: typing.Optional[RedirectResponse] = None,
        target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
        listener: IApplicationListener,
    ) -> None:
        """Properties for defining a listener rule.

        :param priority: Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param action: Action to perform when requests are received. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No action
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param fixed_response: (deprecated) Fixed response to return. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No fixed response.
        :param host_header: (deprecated) Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Default: - No host condition.
        :param path_pattern: (deprecated) Rule applies if the requested path matches the given path pattern. Default: - No path condition.
        :param path_patterns: (deprecated) Rule applies if the requested path matches any of the given patterns. Paths may contain up to three '*' wildcards. Default: - No path conditions.
        :param redirect_response: (deprecated) Redirect response to return. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No redirect response.
        :param target_groups: Target groups to forward requests to. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Implies a ``forward`` action. Default: - No target groups.
        :param listener: The listener to attach the rule to.
        """
        if isinstance(fixed_response, dict):
            fixed_response = FixedResponse(**fixed_response)
        if isinstance(redirect_response, dict):
            redirect_response = RedirectResponse(**redirect_response)
        self._values: typing.Dict[str, typing.Any] = {
            "priority": priority,
            "listener": listener,
        }
        if action is not None:
            self._values["action"] = action
        if conditions is not None:
            self._values["conditions"] = conditions
        if fixed_response is not None:
            self._values["fixed_response"] = fixed_response
        if host_header is not None:
            self._values["host_header"] = host_header
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if path_patterns is not None:
            self._values["path_patterns"] = path_patterns
        if redirect_response is not None:
            self._values["redirect_response"] = redirect_response
        if target_groups is not None:
            self._values["target_groups"] = target_groups

    @builtins.property
    def priority(self) -> jsii.Number:
        """Priority of the rule.

        The rule with the lowest priority will be used for every request.

        Priorities must be unique.
        """
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return result

    @builtins.property
    def action(self) -> typing.Optional[ListenerAction]:
        """Action to perform when requests are received.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No action
        """
        result = self._values.get("action")
        return result

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        """Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        """
        result = self._values.get("conditions")
        return result

    @builtins.property
    def fixed_response(self) -> typing.Optional[FixedResponse]:
        """(deprecated) Fixed response to return.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No fixed response.

        :deprecated: Use ``action`` instead.

        :stability: deprecated
        """
        result = self._values.get("fixed_response")
        return result

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        :default: - No host condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        :stability: deprecated
        """
        result = self._values.get("host_header")
        return result

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        """(deprecated) Rule applies if the requested path matches the given path pattern.

        :default: - No path condition.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_pattern")
        return result

    @builtins.property
    def path_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        """(deprecated) Rule applies if the requested path matches any of the given patterns.

        Paths may contain up to three '*' wildcards.

        :default: - No path conditions.

        :deprecated: Use ``conditions`` instead.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        :stability: deprecated
        """
        result = self._values.get("path_patterns")
        return result

    @builtins.property
    def redirect_response(self) -> typing.Optional[RedirectResponse]:
        """(deprecated) Redirect response to return.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No redirect response.

        :deprecated: Use ``action`` instead.

        :stability: deprecated
        """
        result = self._values.get("redirect_response")
        return result

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        """Target groups to forward requests to.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        Implies a ``forward`` action.

        :default: - No target groups.
        """
        result = self._values.get("target_groups")
        return result

    @builtins.property
    def listener(self) -> IApplicationListener:
        """The listener to attach the rule to."""
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerLookupOptions",
    jsii_struct_bases=[BaseLoadBalancerLookupOptions],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class ApplicationLoadBalancerLookupOptions(BaseLoadBalancerLookupOptions):
    def __init__(
        self,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Options for looking up an ApplicationLoadBalancer.

        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        """Find by load balancer's ARN.

        :default: - does not search by load balancer arn
        """
        result = self._values.get("load_balancer_arn")
        return result

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
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
        return "ApplicationLoadBalancerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerProps",
    jsii_struct_bases=[BaseLoadBalancerProps],
    name_mapping={
        "vpc": "vpc",
        "deletion_protection": "deletionProtection",
        "internet_facing": "internetFacing",
        "load_balancer_name": "loadBalancerName",
        "vpc_subnets": "vpcSubnets",
        "http2_enabled": "http2Enabled",
        "idle_timeout": "idleTimeout",
        "ip_address_type": "ipAddressType",
        "security_group": "securityGroup",
    },
)
class ApplicationLoadBalancerProps(BaseLoadBalancerProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        http2_enabled: typing.Optional[builtins.bool] = None,
        idle_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        ip_address_type: typing.Optional[IpAddressType] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
    ) -> None:
        """Properties for defining an Application Load Balancer.

        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Which subnets place the load balancer in. Default: - the Vpc default strategy.
        :param http2_enabled: Indicates whether HTTP/2 is enabled. Default: true
        :param idle_timeout: The load balancer idle timeout, in seconds. Default: 60
        :param ip_address_type: The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param security_group: Security group to associate with this load balancer. Default: A security group is created
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if http2_enabled is not None:
            self._values["http2_enabled"] = http2_enabled
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC network to place the load balancer in."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        """Indicates whether deletion protection is enabled.

        :default: false
        """
        result = self._values.get("deletion_protection")
        return result

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        """Whether the load balancer has an internet-routable address.

        :default: false
        """
        result = self._values.get("internet_facing")
        return result

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        """Name of the load balancer.

        :default: - Automatically generated name.
        """
        result = self._values.get("load_balancer_name")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Which subnets place the load balancer in.

        :default: - the Vpc default strategy.
        """
        result = self._values.get("vpc_subnets")
        return result

    @builtins.property
    def http2_enabled(self) -> typing.Optional[builtins.bool]:
        """Indicates whether HTTP/2 is enabled.

        :default: true
        """
        result = self._values.get("http2_enabled")
        return result

    @builtins.property
    def idle_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The load balancer idle timeout, in seconds.

        :default: 60
        """
        result = self._values.get("idle_timeout")
        return result

    @builtins.property
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        """The type of IP addresses to use.

        Only applies to application load balancers.

        :default: IpAddressType.Ipv4
        """
        result = self._values.get("ip_address_type")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security group to associate with this load balancer.

        :default: A security group is created
        """
        result = self._values.get("security_group")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroupProps",
    jsii_struct_bases=[BaseTargetGroupProps],
    name_mapping={
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "target_group_name": "targetGroupName",
        "target_type": "targetType",
        "vpc": "vpc",
        "port": "port",
        "protocol": "protocol",
        "slow_start": "slowStart",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "targets": "targets",
    },
)
class ApplicationTargetGroupProps(BaseTargetGroupProps):
    def __init__(
        self,
        *,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[TargetType] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        slow_start: typing.Optional[aws_cdk.core.Duration] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        targets: typing.Optional[typing.List[IApplicationLoadBalancerTarget]] = None,
    ) -> None:
        """Properties for defining an Application Target Group.

        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known, optional for Lambda targets.
        :param protocol: The protocol to use. Default: - Determined from port if known, optional for Lambda targets.
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        """
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if target_type is not None:
            self._values["target_type"] = target_type
        if vpc is not None:
            self._values["vpc"] = vpc
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if slow_start is not None:
            self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: 300
        """
        result = self._values.get("deregistration_delay")
        return result

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        """Health check configuration.

        :default: - None.
        """
        result = self._values.get("health_check")
        return result

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        """The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: - Automatically generated.
        """
        result = self._values.get("target_group_name")
        return result

    @builtins.property
    def target_type(self) -> typing.Optional[TargetType]:
        """The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        :default: - Determined automatically.
        """
        result = self._values.get("target_type")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        :default: - undefined
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        :default: - Determined from protocol if known, optional for Lambda targets.
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        """The protocol to use.

        :default: - Determined from port if known, optional for Lambda targets.
        """
        result = self._values.get("protocol")
        return result

    @builtins.property
    def slow_start(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

        The range is 30-900 seconds (15 minutes).

        :default: 0
        """
        result = self._values.get("slow_start")
        return result

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The stickiness cookie expiration period.

        Setting this value enables load balancer stickiness.

        After this period, the cookie is considered stale. The minimum value is
        1 second and the maximum value is 7 days (604800 seconds).

        :default: Duration.days(1)
        """
        result = self._values.get("stickiness_cookie_duration")
        return result

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[IApplicationLoadBalancerTarget]]:
        """The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        :default: - No targets.
        """
        result = self._values.get("targets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer"
)
class IApplicationLoadBalancer(
    ILoadBalancerV2,
    aws_cdk.aws_ec2.IConnectable,
    typing_extensions.Protocol,
):
    """An application load balancer."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        """The ARN of this load balancer."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        """The IP Address Type for this load balancer.

        :default: IpAddressType.IPV4
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available).

        If this interface is the result of an import call to fromApplicationLoadBalancerAttributes,
        the vpc attribute will be undefined unless specified in the optional properties of that method.
        """
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> ApplicationListener:
        """Add a new listener to this load balancer.

        :param id: -
        :param certificate_arns: (deprecated) The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        ...


class _IApplicationLoadBalancerProxy(
    jsii.proxy_for(ILoadBalancerV2), # type: ignore
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), # type: ignore
):
    """An application load balancer."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        """The ARN of this load balancer."""
        return jsii.get(self, "loadBalancerArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        """The IP Address Type for this load balancer.

        :default: IpAddressType.IPV4
        """
        return jsii.get(self, "ipAddressType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available).

        If this interface is the result of an import call to fromApplicationLoadBalancerAttributes,
        the vpc attribute will be undefined unless specified in the optional properties of that method.
        """
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> ApplicationListener:
        """Add a new listener to this load balancer.

        :param id: -
        :param certificate_arns: (deprecated) The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props = BaseApplicationListenerProps(
            certificate_arns=certificate_arns,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            open=open,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return jsii.invoke(self, "addListener", [id, props])


@jsii.interface(
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup"
)
class IApplicationTargetGroup(ITargetGroup, typing_extensions.Protocol):
    """A Target Group for Application Load Balancers."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IApplicationTargetGroupProxy

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: IApplicationLoadBalancerTarget) -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
        port_range: typing.Optional[aws_cdk.aws_ec2.Port] = None,
    ) -> None:
        """Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -
        """
        ...

    @jsii.member(jsii_name="registerListener")
    def register_listener(
        self,
        listener: IApplicationListener,
        associating_construct: typing.Optional[constructs.IConstruct] = None,
    ) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -
        """
        ...


class _IApplicationTargetGroupProxy(
    jsii.proxy_for(ITargetGroup) # type: ignore
):
    """A Target Group for Application Load Balancers."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup"

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: IApplicationLoadBalancerTarget) -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
        port_range: typing.Optional[aws_cdk.aws_ec2.Port] = None,
    ) -> None:
        """Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="registerListener")
    def register_listener(
        self,
        listener: IApplicationListener,
        associating_construct: typing.Optional[constructs.IConstruct] = None,
    ) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -
        """
        return jsii.invoke(self, "registerListener", [listener, associating_construct])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup")
class INetworkTargetGroup(ITargetGroup, typing_extensions.Protocol):
    """A network target group."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INetworkTargetGroupProxy

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: INetworkLoadBalancerTarget) -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        ...

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: INetworkListener) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        """
        ...


class _INetworkTargetGroupProxy(
    jsii.proxy_for(ITargetGroup) # type: ignore
):
    """A network target group."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup"

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: INetworkLoadBalancerTarget) -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: INetworkListener) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        """
        return jsii.invoke(self, "registerListener", [listener])


@jsii.implements(INetworkTargetGroup)
class NetworkTargetGroup(
    TargetGroupBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroup",
):
    """Define a Network Target Group."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        port: jsii.Number,
        protocol: typing.Optional[Protocol] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        targets: typing.Optional[typing.List[INetworkLoadBalancerTarget]] = None,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[TargetType] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param port: The port on which the listener listens for requests.
        :param protocol: Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - TCP
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        """
        props = NetworkTargetGroupProps(
            port=port,
            protocol=protocol,
            proxy_protocol_v2=proxy_protocol_v2,
            targets=targets,
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            target_group_name=target_group_name,
            target_type=target_type,
            vpc=vpc,
        )

        jsii.create(NetworkTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromTargetGroupAttributes")
    @builtins.classmethod
    def from_target_group_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_group_arn: builtins.str,
        default_port: typing.Optional[builtins.str] = None,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> INetworkTargetGroup:
        """Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: (deprecated) Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        attrs = TargetGroupAttributes(
            target_group_arn=target_group_arn,
            default_port=default_port,
            load_balancer_arns=load_balancer_arns,
        )

        return jsii.sinvoke(cls, "fromTargetGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="import")
    @builtins.classmethod
    def import_(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_group_arn: builtins.str,
        default_port: typing.Optional[builtins.str] = None,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> INetworkTargetGroup:
        """(deprecated) Import an existing listener.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: (deprecated) Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.

        :deprecated: Use ``fromTargetGroupAttributes`` instead

        :stability: deprecated
        """
        props = TargetGroupImportProps(
            target_group_arn=target_group_arn,
            default_port=default_port,
            load_balancer_arns=load_balancer_arns,
        )

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: INetworkLoadBalancerTarget) -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of targets that are considered healthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricUnHealthyHostCount")
    def metric_un_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of targets that are considered unhealthy.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricUnHealthyHostCount", [props])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: INetworkListener) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        """
        return jsii.invoke(self, "registerListener", [listener])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> builtins.str:
        """Full name of first load balancer."""
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.implements(IApplicationLoadBalancer)
class ApplicationLoadBalancer(
    BaseLoadBalancer,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancer",
):
    """Define an Application Load Balancer.

    :resource: AWS::ElasticLoadBalancingV2::LoadBalancer
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http2_enabled: typing.Optional[builtins.bool] = None,
        idle_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        ip_address_type: typing.Optional[IpAddressType] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc: aws_cdk.aws_ec2.IVpc,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param http2_enabled: Indicates whether HTTP/2 is enabled. Default: true
        :param idle_timeout: The load balancer idle timeout, in seconds. Default: 60
        :param ip_address_type: The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param security_group: Security group to associate with this load balancer. Default: A security group is created
        :param vpc: The VPC network to place the load balancer in.
        :param deletion_protection: Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: Which subnets place the load balancer in. Default: - the Vpc default strategy.
        """
        props = ApplicationLoadBalancerProps(
            http2_enabled=http2_enabled,
            idle_timeout=idle_timeout,
            ip_address_type=ip_address_type,
            security_group=security_group,
            vpc=vpc,
            deletion_protection=deletion_protection,
            internet_facing=internet_facing,
            load_balancer_name=load_balancer_name,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(ApplicationLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationLoadBalancerAttributes")
    @builtins.classmethod
    def from_application_load_balancer_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: builtins.str,
        security_group_id: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        security_group_allows_all_outbound: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> IApplicationLoadBalancer:
        """Import an existing Application Load Balancer.

        :param scope: -
        :param id: -
        :param load_balancer_arn: ARN of the load balancer.
        :param security_group_id: ID of the load balancer's security group.
        :param load_balancer_canonical_hosted_zone_id: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param security_group_allows_all_outbound: Whether the security group allows all outbound traffic or not. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param vpc: The VPC this load balancer has been created in, if available. Default: - If the Load Balancer was imported and a VPC was not specified, the VPC is not available.
        """
        attrs = ApplicationLoadBalancerAttributes(
            load_balancer_arn=load_balancer_arn,
            security_group_id=security_group_id,
            load_balancer_canonical_hosted_zone_id=load_balancer_canonical_hosted_zone_id,
            load_balancer_dns_name=load_balancer_dns_name,
            security_group_allows_all_outbound=security_group_allows_all_outbound,
            vpc=vpc,
        )

        return jsii.sinvoke(cls, "fromApplicationLoadBalancerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromLookup")
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> IApplicationLoadBalancer:
        """Look up an application load balancer.

        :param scope: -
        :param id: -
        :param load_balancer_arn: Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: Match load balancer tags. Default: - does not match load balancers by tags
        """
        options = ApplicationLoadBalancerLookupOptions(
            load_balancer_arn=load_balancer_arn, load_balancer_tags=load_balancer_tags
        )

        return jsii.sinvoke(cls, "fromLookup", [scope, id, options])

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        certificate_arns: typing.Optional[typing.List[builtins.str]] = None,
        certificates: typing.Optional[typing.List[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.List[IApplicationTargetGroup]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> ApplicationListener:
        """Add a new listener to this load balancer.

        :param id: -
        :param certificate_arns: (deprecated) The certificates to use on this listener. Default: - No certificates.
        :param certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props = BaseApplicationListenerProps(
            certificate_arns=certificate_arns,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            open=open,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="addRedirect")
    def add_redirect(
        self,
        *,
        source_port: typing.Optional[jsii.Number] = None,
        source_protocol: typing.Optional[ApplicationProtocol] = None,
        target_port: typing.Optional[jsii.Number] = None,
        target_protocol: typing.Optional[ApplicationProtocol] = None,
    ) -> ApplicationListener:
        """Add a redirection listener to this load balancer.

        :param source_port: The port number to listen to. Default: 80
        :param source_protocol: The protocol of the listener being created. Default: HTTP
        :param target_port: The port number to redirect to. Default: 443
        :param target_protocol: The protocol of the redirection target. Default: HTTPS
        """
        props = ApplicationLoadBalancerRedirectConfig(
            source_port=source_port,
            source_protocol=source_protocol,
            target_port=target_port,
            target_protocol=target_protocol,
        )

        return jsii.invoke(self, "addRedirect", [props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
    ) -> None:
        """Add a security group to this load balancer.

        :param security_group: -
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Application Load Balancer.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveConnectionCount")
    def metric_active_connection_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of concurrent TCP connections active from clients to the load balancer and from the load balancer to targets.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricActiveConnectionCount", [props])

    @jsii.member(jsii_name="metricClientTlsNegotiationErrorCount")
    def metric_client_tls_negotiation_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the client that did not establish a session with the load balancer.

        Possible causes include a
        mismatch of ciphers or protocols.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricClientTlsNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of load balancer capacity units (LCU) used by your load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricElbAuthError")
    def metric_elb_auth_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of user authentications that could not be completed.

        Because an authenticate action was misconfigured, the load balancer
        couldn't establish a connection with the IdP, or the load balancer
        couldn't complete the authentication flow due to an internal error.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricElbAuthError", [props])

    @jsii.member(jsii_name="metricElbAuthFailure")
    def metric_elb_auth_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of user authentications that could not be completed because the IdP denied access to the user or an authorization code was used more than once.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricElbAuthFailure", [props])

    @jsii.member(jsii_name="metricElbAuthLatency")
    def metric_elb_auth_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in milliseconds, to query the IdP for the ID token and user info.

        If one or more of these operations fail, this is the time to failure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricElbAuthLatency", [props])

    @jsii.member(jsii_name="metricElbAuthSuccess")
    def metric_elb_auth_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of authenticate actions that were successful.

        This metric is incremented at the end of the authentication workflow,
        after the load balancer has retrieved the user claims from the IdP.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricElbAuthSuccess", [props])

    @jsii.member(jsii_name="metricHttpCodeElb")
    def metric_http_code_elb(
        self,
        code: HttpCodeElb,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 3xx/4xx/5xx codes that originate from the load balancer.

        This does not include any response codes generated by the targets.

        :param code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHttpCodeElb", [code, props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(
        self,
        code: HttpCodeTarget,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in the load balancer.

        This does not include any response codes generated by the load balancer.

        :param code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricHttpFixedResponseCount")
    def metric_http_fixed_response_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of fixed-response actions that were successful.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHttpFixedResponseCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectCount")
    def metric_http_redirect_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of redirect actions that were successful.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHttpRedirectCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectUrlLimitExceededCount")
    def metric_http_redirect_url_limit_exceeded_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of redirect actions that couldn't be completed because the URL in the response location header is larger than 8K.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHttpRedirectUrlLimitExceededCount", [props])

    @jsii.member(jsii_name="metricIpv6ProcessedBytes")
    def metric_ipv6_processed_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer over IPv6.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricIpv6ProcessedBytes", [props])

    @jsii.member(jsii_name="metricIpv6RequestCount")
    def metric_ipv6_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of IPv6 requests received by the load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricIpv6RequestCount", [props])

    @jsii.member(jsii_name="metricNewConnectionCount")
    def metric_new_connection_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of new TCP connections established from clients to the load balancer and from the load balancer to targets.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricNewConnectionCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer over IPv4 and IPv6.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricRejectedConnectionCount")
    def metric_rejected_connection_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were rejected because the load balancer had reached its maximum number of connections.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricRejectedConnectionCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRuleEvaluations")
    def metric_rule_evaluations(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of rules processed by the load balancer given a request rate averaged over an hour.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricRuleEvaluations", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were not successfully established between the load balancer and target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        """The IP Address Type for this load balancer."""
        return jsii.get(self, "ipAddressType")


@jsii.implements(IApplicationTargetGroup)
class ApplicationTargetGroup(
    TargetGroupBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroup",
):
    """Define an Application Target Group."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        slow_start: typing.Optional[aws_cdk.core.Duration] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        targets: typing.Optional[typing.List[IApplicationLoadBalancerTarget]] = None,
        deregistration_delay: typing.Optional[aws_cdk.core.Duration] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[TargetType] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known, optional for Lambda targets.
        :param protocol: The protocol to use. Default: - Determined from port if known, optional for Lambda targets.
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: Health check configuration. Default: - None.
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        """
        props = ApplicationTargetGroupProps(
            port=port,
            protocol=protocol,
            slow_start=slow_start,
            stickiness_cookie_duration=stickiness_cookie_duration,
            targets=targets,
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            target_group_name=target_group_name,
            target_type=target_type,
            vpc=vpc,
        )

        jsii.create(ApplicationTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromTargetGroupAttributes")
    @builtins.classmethod
    def from_target_group_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_group_arn: builtins.str,
        default_port: typing.Optional[builtins.str] = None,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> IApplicationTargetGroup:
        """Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: (deprecated) Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        attrs = TargetGroupAttributes(
            target_group_arn=target_group_arn,
            default_port=default_port,
            load_balancer_arns=load_balancer_arns,
        )

        return jsii.sinvoke(cls, "fromTargetGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="import")
    @builtins.classmethod
    def import_(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_group_arn: builtins.str,
        default_port: typing.Optional[builtins.str] = None,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> IApplicationTargetGroup:
        """(deprecated) Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: ARN of the target group.
        :param default_port: (deprecated) Port target group is listening on.
        :param load_balancer_arns: A Token representing the list of ARNs for the load balancer routing to this target group.

        :deprecated: Use ``fromTargetGroupAttributes`` instead

        :stability: deprecated
        """
        props = TargetGroupImportProps(
            target_group_arn=target_group_arn,
            default_port=default_port,
            load_balancer_arns=load_balancer_arns,
        )

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: IApplicationLoadBalancerTarget) -> None:
        """Add a load balancing target to this target group.

        :param targets: -
        """
        return jsii.invoke(self, "addTarget", [*targets])

    @jsii.member(jsii_name="enableCookieStickiness")
    def enable_cookie_stickiness(self, duration: aws_cdk.core.Duration) -> None:
        """Enable sticky routing via a cookie to members of this target group.

        :param duration: -
        """
        return jsii.invoke(self, "enableCookieStickiness", [duration])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Application Load Balancer Target Group.

        Returns the metric for this target group from the point of view of the first
        load balancer load balancing to it. If you have multiple load balancers load
        sending traffic to the same target group, you will have to override the dimensions
        on this metric.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of healthy hosts in the target group.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(
        self,
        code: HttpCodeTarget,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in this target group.

        This does not include any response codes generated by the load balancer.

        :param code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricIpv6RequestCount")
    def metric_ipv6_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of IPv6 requests received by the target group.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricIpv6RequestCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRequestCountPerTarget")
    def metric_request_count_per_target(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The average number of requests received by each target in a target group.

        The only valid statistic is Sum. Note that this represents the average not the sum.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricRequestCountPerTarget", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were not successfully established between the load balancer and target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricUnhealthyHostCount")
    def metric_unhealthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.core.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of unhealthy hosts in the target group.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricUnhealthyHostCount", [props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: aws_cdk.aws_ec2.IConnectable,
        port_range: typing.Optional[aws_cdk.aws_ec2.Port] = None,
    ) -> None:
        """Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="registerListener")
    def register_listener(
        self,
        listener: IApplicationListener,
        associating_construct: typing.Optional[constructs.IConstruct] = None,
    ) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -
        """
        return jsii.invoke(self, "registerListener", [listener, associating_construct])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> builtins.str:
        """Full name of first load balancer."""
        return jsii.get(self, "firstLoadBalancerFullName")


__all__ = [
    "AddApplicationActionProps",
    "AddApplicationTargetGroupsProps",
    "AddApplicationTargetsProps",
    "AddFixedResponseProps",
    "AddNetworkActionProps",
    "AddNetworkTargetsProps",
    "AddRedirectResponseProps",
    "AddRuleProps",
    "ApplicationListener",
    "ApplicationListenerAttributes",
    "ApplicationListenerCertificate",
    "ApplicationListenerCertificateProps",
    "ApplicationListenerLookupOptions",
    "ApplicationListenerProps",
    "ApplicationListenerRule",
    "ApplicationListenerRuleProps",
    "ApplicationLoadBalancer",
    "ApplicationLoadBalancerAttributes",
    "ApplicationLoadBalancerLookupOptions",
    "ApplicationLoadBalancerProps",
    "ApplicationLoadBalancerRedirectConfig",
    "ApplicationProtocol",
    "ApplicationTargetGroup",
    "ApplicationTargetGroupProps",
    "AuthenticateOidcOptions",
    "BaseApplicationListenerProps",
    "BaseApplicationListenerRuleProps",
    "BaseListener",
    "BaseListenerLookupOptions",
    "BaseLoadBalancer",
    "BaseLoadBalancerLookupOptions",
    "BaseLoadBalancerProps",
    "BaseNetworkListenerProps",
    "BaseTargetGroupProps",
    "CfnListener",
    "CfnListenerCertificate",
    "CfnListenerCertificateProps",
    "CfnListenerProps",
    "CfnListenerRule",
    "CfnListenerRuleProps",
    "CfnLoadBalancer",
    "CfnLoadBalancerProps",
    "CfnTargetGroup",
    "CfnTargetGroupProps",
    "ContentType",
    "FixedResponse",
    "FixedResponseOptions",
    "ForwardOptions",
    "HealthCheck",
    "HttpCodeElb",
    "HttpCodeTarget",
    "IApplicationListener",
    "IApplicationLoadBalancer",
    "IApplicationLoadBalancerTarget",
    "IApplicationTargetGroup",
    "IListenerAction",
    "IListenerCertificate",
    "ILoadBalancerV2",
    "INetworkListener",
    "INetworkListenerCertificateProps",
    "INetworkLoadBalancer",
    "INetworkLoadBalancerTarget",
    "INetworkTargetGroup",
    "ITargetGroup",
    "InstanceTarget",
    "IpAddressType",
    "IpTarget",
    "ListenerAction",
    "ListenerCertificate",
    "ListenerCondition",
    "LoadBalancerTargetProps",
    "NetworkForwardOptions",
    "NetworkListener",
    "NetworkListenerAction",
    "NetworkListenerLookupOptions",
    "NetworkListenerProps",
    "NetworkLoadBalancer",
    "NetworkLoadBalancerAttributes",
    "NetworkLoadBalancerLookupOptions",
    "NetworkLoadBalancerProps",
    "NetworkTargetGroup",
    "NetworkTargetGroupProps",
    "NetworkWeightedTargetGroup",
    "Protocol",
    "QueryStringCondition",
    "RedirectOptions",
    "RedirectResponse",
    "SslPolicy",
    "TargetGroupAttributes",
    "TargetGroupBase",
    "TargetGroupImportProps",
    "TargetType",
    "UnauthenticatedAction",
    "WeightedTargetGroup",
]

publication.publish()
