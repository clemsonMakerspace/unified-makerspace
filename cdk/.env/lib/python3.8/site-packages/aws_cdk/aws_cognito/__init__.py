"""
## Amazon Cognito Construct Library

<!--BEGIN STABILITY BANNER-->---


| Features | Stability |
| --- | --- |
| CFN Resources | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge) |
| Higher level constructs for User Pools | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge) |
| Higher level constructs for Identity Pools | ![Not Implemented](https://img.shields.io/badge/not--implemented-black.svg?style=for-the-badge) |

> **CFN Resources:** All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

> **Stable:** Higher level constructs in this module that are marked stable will not undergo any breaking changes. They will strictly follow the [Semantic Versioning](https://semver.org/) model.

---
<!--END STABILITY BANNER-->

[Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html) provides
authentication, authorization, and user management for your web and mobile apps. Your users can sign in directly with a
user name and password, or through a third party such as Facebook, Amazon, Google or Apple.

The two main components of Amazon Cognito are [user
pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html) and [identity
pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html). User pools are user directories
that provide sign-up and sign-in options for your app users. Identity pools enable you to grant your users access to
other AWS services.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Table of Contents

* [User Pools](#user-pools)

  * [Sign Up](#sign-up)
  * [Sign In](#sign-in)
  * [Attributes](#attributes)
  * [Security](#security)

    * [Multi-factor Authentication](#multi-factor-authentication-mfa)
    * [Account Recovery Settings](#account-recovery-settings)
  * [Emails](#emails)
  * [Lambda Triggers](#lambda-triggers)

    * [Trigger Permissions](#trigger-permissions)
  * [Import](#importing-user-pools)
  * [Identity Providers](#identity-providers)
  * [App Clients](#app-clients)
  * [Resource Servers](#resource-servers)
  * [Domains](#domains)

## User Pools

User pools allow creating and managing your own directory of users that can sign up and sign in. They enable easy
integration with social identity providers such as Facebook, Google, Amazon, Microsoft Active Directory, etc. through
SAML.

Using the CDK, a new user pool can be created as part of the stack using the construct's constructor. You may specify
the `userPoolName` to give your own identifier to the user pool. If not, CloudFormation will generate a name.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    user_pool_name="myawesomeapp-userpool"
)
```

The default set up for the user pool is configured such that only administrators will be allowed
to create users. Features such as Multi-factor authentication (MFAs) and Lambda Triggers are not
configured by default.

### Sign Up

Users can either be signed up by the app's administrators or can sign themselves up. Once a user has signed up, their
account needs to be confirmed. Cognito provides several ways to sign users up and confirm their accounts. Learn more
about [user sign up here](https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html).

When a user signs up, email and SMS messages are used to verify their account and contact methods. The following code
snippet configures a user pool with properties relevant to these verification messages -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    self_sign_up_enabled=True,
    user_verification=UserVerificationConfig(
        email_subject="Verify your email for our awesome app!",
        email_body="Hello {username}, Thanks for signing up to our awesome app! Your verification code is {####}",
        email_style=cognito.VerificationEmailStyle.CODE,
        sms_message="Hello {username}, Thanks for signing up to our awesome app! Your verification code is {####}"
    )
)
```

By default, self sign up is disabled. Learn more about [email and SMS verification messages
here](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-customizations.html).

Besides users signing themselves up, an administrator of any user pool can sign users up. The user then receives an
invitation to join the user pool. The following code snippet configures a user pool with properties relevant to the
invitation messages -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    user_invitation=UserInvitationConfig(
        email_subject="Invite to join our awesome app!",
        email_body="Hello {username}, you have been invited to join our awesome app! Your temporary password is {####}",
        sms_message="Your temporary password for our awesome app is {####}"
    )
)
```

All email subjects, bodies and SMS messages for both invitation and verification support Cognito's message templating.
Learn more about [message templates
here](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html).

### Sign In

Users registering or signing in into your application can do so with multiple identifiers. There are 4 options
available:

* `username`: Allow signing in using the one time immutable user name that the user chose at the time of sign up.
* `email`: Allow signing in using the email address that is associated with the account.
* `phone`: Allow signing in using the phone number that is associated with the account.
* `preferredUsername`: Allow signing in with an alternate user name that the user can change at any time. However, this
  is not available if the `username` option is not chosen.

The following code sets up a user pool so that the user can sign in with either their username or their email address -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    # ...
    sign_in_aliases=SignInAliases(
        username=True,
        email=True
    )
)
```

User pools can either be configured so that user name is primary sign in form, but also allows for the other three to be
used additionally; or it can be configured so that email and/or phone numbers are the only ways a user can register and
sign in. Read more about this
[here](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases-settings).

⚠️ The Cognito service prevents changing the `signInAlias` property for an existing user pool.

To match with 'Option 1' in the above link, with a verified email, `signInAliases` should be set to
`{ username: true, email: true }`. To match with 'Option 2' in the above link with both a verified
email and phone number, this property should be set to `{ email: true, phone: true }`.

Cognito recommends that email and phone number be automatically verified, if they are one of the sign in methods for
the user pool. Read more about that
[here](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases).
The CDK does this by default, when email and/or phone number are specified as part of `signInAliases`. This can be
overridden by specifying the `autoVerify` property.

The following code snippet sets up only email as a sign in alias, but both email and phone number to be auto-verified.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    # ...
    sign_in_aliases=SignInAliases(username=True, email=True),
    auto_verify=AutoVerifiedAttrs(email=True, phone=True)
)
```

A user pool can optionally ignore case when evaluating sign-ins. When `signInCaseSensitive` is false, Cognito will not
check the capitalization of the alias when signing in. Default is true.

### Attributes

Attributes represent the various properties of each user that's collected and stored in the user pool. Cognito
provides a set of standard attributes that are available for all user pools. Users are allowed to select any of these
standard attributes to be required. Users will not be able to sign up to the user pool without providing the required
attributes. Besides these, additional attributes can be further defined, and are known as custom attributes.

Learn more on [attributes in Cognito's
documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html).

The following code configures a user pool with two standard attributes (name and address) as required and mutable, and adds
four custom attributes.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    standard_attributes=StandardAttributes(
        fullname=StandardAttribute(
            required=True,
            mutable=False
        ),
        address=StandardAttribute(
            required=False,
            mutable=True
        )
    ),
    custom_attributes={
        "myappid": cognito.StringAttribute(min_len=5, max_len=15, mutable=False),
        "callingcode": cognito.NumberAttribute(min=1, max=3, mutable=True),
        "is_employee": cognito.BooleanAttribute(mutable=True),
        "joined_on": cognito.DateTimeAttribute()
    }
)
```

As shown in the code snippet, there are data types that are available for custom attributes. The 'String' and 'Number'
data types allow for further constraints on their length and values, respectively.

Custom attributes cannot be marked as required.

All custom attributes share the property `mutable` that specifies whether the value of the attribute can be changed.
The default value is `false`.

### Security

Cognito sends various messages to its users via SMS, for different actions, ranging from account verification to
marketing. In order to send SMS messages, Cognito needs an IAM role that it can assume, with permissions that allow it
to send SMS messages.

By default, the CDK looks at all of the specified properties (and their defaults when not explicitly specified) and
automatically creates an SMS role, when needed. For example, if MFA second factor by SMS is enabled, the CDK will
create a new role. The `smsRole` property can be used to specify the user supplied role that should be used instead.
Additionally, the property `enableSmsRole` can be used to override the CDK's default behaviour to either enable or
suppress automatic role creation.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pool_sms_role = iam.Role(self, "userpoolsmsrole",
    assumed_by=iam.ServicePrincipal("foo")
)

cognito.UserPool(self, "myuserpool",
    # ...
    sms_role=pool_sms_role,
    sms_role_external_id="c87467be-4f34-11ea-b77f-2e728ce88125"
)
```

When the `smsRole` property is specified, the `smsRoleExternalId` may also be specified. The value of
`smsRoleExternalId` will be used as the `sts:ExternalId` when the Cognito service assumes the role. In turn, the role's
assume role policy should be configured to accept this value as the ExternalId. Learn more about [ExternalId
here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).

#### Multi-factor Authentication (MFA)

User pools can be configured to enable multi-factor authentication (MFA). It can either be turned off, set to optional
or made required. Setting MFA to optional means that individual users can choose to enable it.
Additionally, the MFA code can be sent either via SMS text message or via a time-based software token.
See the [documentation on MFA](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html) to
learn more.

The following code snippet marks MFA for the user pool as required. This means that all users are required to
configure an MFA token and use it for sign in. It also allows for the users to use both SMS based MFA, as well,
[time-based one time password
(TOTP)](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html).

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    mfa=cognito.Mfa.REQUIRED,
    mfa_second_factor=MfaSecondFactor(
        sms=True,
        otp=True
    )
)
```

User pools can be configured with policies around a user's password. This includes the password length and the
character sets that they must contain.

Further to this, it can also be configured with the validity of the auto-generated temporary password. A temporary
password is generated by the user pool either when an admin signs up a user or when a password reset is requested.
The validity of this password dictates how long to give the user to use this password before expiring it.

The following code snippet configures these properties -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    password_policy=PasswordPolicy(
        min_length=12,
        require_lowercase=True,
        require_uppercase=True,
        require_digits=True,
        require_symbols=True,
        temp_password_validity=Duration.days(3)
    )
)
```

Note that, `tempPasswordValidity` can be specified only in whole days. Specifying fractional days would throw an error.

#### Account Recovery Settings

User pools can be configured on which method a user should use when recovering the password for their account. This
can either be email and/or SMS. Read more at [Recovering User Accounts](https://docs.aws.amazon.com/cognito/latest/developerguide/how-to-recover-a-user-account.html)

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "UserPool",
    # ...
    account_recovery=cognito.AccountRecovery.EMAIL_ONLY
)
```

The default for account recovery is by phone if available and by email otherwise.
A user will not be allowed to reset their password via phone if they are also using it for MFA.

### Emails

Cognito sends emails to users in the user pool, when particular actions take place, such as welcome emails, invitation
emails, password resets, etc. The address from which these emails are sent can be configured on the user pool.
Read more about [email settings here](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-email.html).

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cognito.UserPool(self, "myuserpool",
    # ...
    email_settings=EmailSettings(
        from="noreply@myawesomeapp.com",
        reply_to="support@myawesomeapp.com"
    )
)
```

By default, user pools are configured to use Cognito's built-in email capability, but it can also be configured to use
Amazon SES, however, support for Amazon SES is not available in the CDK yet. If you would like this to be implemented,
give [this issue](https://github.com/aws/aws-cdk/issues/6768) a +1. Until then, you can use the [cfn
layer](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html) to configure this.

If an email address contains non-ASCII characters, it will be encoded using the [punycode
encoding](https://en.wikipedia.org/wiki/Punycode) when generating the template for Cloudformation.

### Lambda Triggers

User pools can be configured such that AWS Lambda functions can be triggered when certain user operations or actions
occur, such as, sign up, user confirmation, sign in, etc. They can also be used to add custom authentication
challenges, user migrations and custom verification messages. Learn more about triggers at [User Pool Workflows with
Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html).

Lambda triggers can either be specified as part of the `UserPool` initialization, or it can be added later, via methods
on the construct, as so -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
auth_challenge_fn = lambda_.Function(self, "authChallengeFn",
    runtime=lambda_.Runtime.NODEJS_10_X,
    handler="index.handler",
    code=lambda_.Code.from_inline("auth challenge")
)

userpool = cognito.UserPool(self, "myuserpool",
    # ...
    lambda_triggers=UserPoolTriggers(
        create_auth_challenge=auth_challenge_fn
    )
)

userpool.add_trigger(cognito.UserPoolOperation.USER_MIGRATION, lambda_.Function(self, "userMigrationFn",
    runtime=lambda_.Runtime.NODEJS_10_X,
    handler="index.handler",
    code=lambda_.Code.from_inline("user migration")
))
```

The following table lists the set of triggers available, and their corresponding method to add it to the user pool.
For more information on the function of these triggers and how to configure them, read [User Pool Workflows with
Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html).

#### Trigger Permissions

The `function.attachToRolePolicy()` API can be used to add additional IAM permissions to the lambda trigger
as necessary.

⚠️ Using the `attachToRolePolicy` API to provide permissions to your user pool will result in a circular dependency. See [aws/aws-cdk#7016](https://github.com/aws/aws-cdk/issues/7016).
Error message when running `cdk synth` or `cdk deploy`:

> Circular dependency between resources: [pool056F3F7E, fnPostAuthFnCognitoA630A2B1, ...]

To work around the circular dependency issue, use the `attachInlinePolicy()` API instead, as shown below.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# provide permissions to describe the user pool scoped to the ARN the user pool
post_auth_fn.role.attach_inline_policy(iam.Policy(self, "userpool-policy",
    statements=[iam.PolicyStatement(
        actions=["cognito-idp:DescribeUserPool"],
        resources=[userpool.user_pool_arn]
    )]
))
```

### Importing User Pools

Any user pool that has been created outside of this stack, can be imported into the CDK app. Importing a user pool
allows for it to be used in other parts of the CDK app that reference an `IUserPool`. However, imported user pools have
limited configurability. As a rule of thumb, none of the properties that are part of the
[`AWS::Cognito::UserPool`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html)
CloudFormation resource can be configured.

User pools can be imported either using their id via the `UserPool.fromUserPoolId()`, or by using their ARN, via the
`UserPool.fromUserPoolArn()` API.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
awesome_pool = cognito.UserPool.from_user_pool_id(self, "awesome-user-pool", "us-east-1_oiuR12Abd")

other_awesome_pool = cognito.UserPool.from_user_pool_arn(self, "other-awesome-user-pool", "arn:aws:cognito-idp:eu-west-1:123456789012:userpool/us-east-1_mtRyYQ14D")
```

### Identity Providers

Users that are part of a user pool can sign in either directly through a user pool, or federate through a third-party
identity provider. Once configured, the Cognito backend will take care of integrating with the third-party provider.
Read more about [Adding User Pool Sign-in Through a Third
Party](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-federation.html).

The following third-party identity providers are currently supported in the CDK -

* [Login With Amazon](https://developer.amazon.com/apps-and-games/login-with-amazon)
* [Facebook Login](https://developers.facebook.com/docs/facebook-login/)
* [Google Login](https://developers.google.com/identity/sign-in/web/sign-in)

The following code configures a user pool to federate with the third party provider, 'Login with Amazon'. The identity
provider needs to be configured with a set of credentials that the Cognito backend can use to federate with the
third-party identity provider.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
userpool = cognito.UserPool(self, "Pool")

provider = cognito.UserPoolIdentityProviderAmazon(self, "Amazon",
    client_id="amzn-client-id",
    client_secret="amzn-client-secret",
    user_pool=userpool
)
```

Attribute mapping allows mapping attributes provided by the third-party identity providers to [standard and custom
attributes](#Attributes) of the user pool. Learn more about [Specifying Identity Provider Attribute Mappings for Your
User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-specifying-attribute-mapping.html).

The following code shows how different attributes provided by 'Login With Amazon' can be mapped to standard and custom
user pool attributes.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
userpool = cognito.UserPool(self, "Pool")

cognito.UserPoolIdentityProviderAmazon(self, "Amazon",
    client_id="amzn-client-id",
    client_secret="amzn-client-secret",
    user_pool=userpool,
    attribute_mapping=AttributeMapping(
        email=cognito.ProviderAttribute.AMAZON_EMAIL,
        website=cognito.ProviderAttribute.other("url"), # use other() when an attribute is not pre-defined in the CDK
        custom={
            # custom user pool attributes go here
            "unique_id": cognito.ProviderAttribute.AMAZON_USER_ID
        }
    )
)
```

### App Clients

An app is an entity within a user pool that has permission to call unauthenticated APIs (APIs that do not have an
authenticated user), such as APIs to register, sign in, and handle forgotten passwords. To call these APIs, you need an
app client ID and an optional client secret. Read [Configuring a User Pool App
Client](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html) to learn more.

The following code creates an app client and retrieves the client id -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pool = cognito.UserPool(self, "pool")
client = pool.add_client("customer-app-client")
client_id = client.user_pool_client_id
```

Existing app clients can be imported into the CDK app using the `UserPoolClient.fromUserPoolClientId()` API. For new
and imported user pools, clients can also be created via the `UserPoolClient` constructor, as so -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
imported_pool = cognito.UserPool.from_user_pool_id(self, "imported-pool", "us-east-1_oiuR12Abd")
cognito.UserPoolClient(self, "customer-app-client",
    user_pool=imported_pool
)
```

Clients can be configured with authentication flows. Authentication flows allow users on a client to be authenticated
with a user pool. Cognito user pools provide several several different types of authentication, such as, SRP (Secure
Remote Password) authentication, username-and-password authentication, etc. Learn more about this at [UserPool Authentication
Flow](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html).

The following code configures a client to use both SRP and username-and-password authentication -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pool = cognito.UserPool(self, "pool")
pool.add_client("app-client",
    auth_flows=AuthFlow(
        user_password=True,
        user_srp=True
    )
)
```

Custom authentication protocols can be configured by setting the `custom` property under `authFlow` and defining lambda
functions for the corresponding user pool [triggers](#lambda-triggers). Learn more at [Custom Authentication
Flow](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html#amazon-cognito-user-pools-custom-authentication-flow).

In addition to these authentication mechanisms, Cognito user pools also support using OAuth 2.0 framework for
authenticating users. User pool clients can be configured with OAuth 2.0 authorization flows and scopes. Learn more
about the [OAuth 2.0 authorization framework](https://tools.ietf.org/html/rfc6749) and [Cognito user pool's
implementation of
OAuth2.0](https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/).

The following code configures an app client with the authorization code grant flow and registers the the app's welcome
page as a callback (or redirect) URL. It also configures the access token scope to 'openid'. All of these concepts can
be found in the [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749).

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pool = cognito.UserPool(self, "Pool")
pool.add_client("app-client",
    o_auth=OAuthSettings(
        flows=OAuthFlows(
            authorization_code_grant=True
        ),
        scopes=[cognito.OAuthScope.OPENID],
        callback_urls=["https://my-app-domain.com/welcome"],
        logout_urls=["https://my-app-domain.com/signin"]
    )
)
```

An app client can be configured to prevent user existence errors. This
instructs the Cognito authentication API to return generic authentication
failure responses instead of an UserNotFoundException. By default, the flag
is not set, which means different things for existing and new stacks. See the
[documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-managing-errors.html)
for the full details on the behavior of this flag.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pool = cognito.UserPool(self, "Pool")
pool.add_client("app-client",
    prevent_user_existence_errors=True
)
```

All identity providers created in the CDK app are automatically registered into the corresponding user pool. All app
clients created in the CDK have all of the identity providers enabled by default. The 'Cognito' identity provider,
that allows users to register and sign in directly with the Cognito user pool, is also enabled by default.
Alternatively, the list of supported identity providers for a client can be explicitly specified -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pool = cognito.UserPool(self, "Pool")
pool.add_client("app-client",
    # ...
    supported_identity_providers=[cognito.UserPoolClientIdentityProvider.AMAZON, cognito.UserPoolClientIdentityProvider.COGNITO
    ]
)
```

### Resource Servers

A resource server is a server for access-protected resources. It handles authenticated requests from an app that has an
access token. See [Defining Resource
Servers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html)
for more information.

An application may choose to model custom permissions via OAuth. Resource Servers provide this capability via custom scopes
that are attached to an app client. The following example sets up a resource server for the 'users' resource for two different
app clients and configures the clients to use these scopes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pool = cognito.UserPool(self, "Pool")

read_only_scope = ResourceServerScope(scope_name="read", scope_description="Read-only access")
full_access_scope = ResourceServerScope(scope_name="*", scope_description="Full access")

user_server = pool.add_resource_server("ResourceServer",
    identifier="users",
    scopes=[read_only_scope, full_access_scope]
)

read_only_client = pool.add_client("read-only-client",
    # ...
    o_auth=OAuthSettings(
        # ...
        scopes=[OAuthScope.resource_server(user_server, read_only_scope)]
    )
)

full_access_client = pool.add_client("full-access-client",
    # ...
    o_auth=OAuthSettings(
        # ...
        scopes=[OAuthScope.resource_server(user_server, full_access_scope)]
    )
)
```

### Domains

After setting up an [app client](#app-clients), the address for the user pool's sign-up and sign-in webpages can be
configured using domains. There are two ways to set up a domain - either the Amazon Cognito hosted domain can be chosen
with an available domain prefix, or a custom domain name can be chosen. The custom domain must be one that is already
owned, and whose certificate is registered in AWS Certificate Manager.

The following code sets up a user pool domain in Amazon Cognito hosted domain with the prefix 'my-awesome-app', and another domain with the custom domain 'user.myapp.com' -

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pool = cognito.UserPool(self, "Pool")

pool.add_domain("CognitoDomain",
    cognito_domain=CognitoDomainOptions(
        domain_prefix="my-awesome-app"
    )
)

certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/11-3336f1-44483d-adc7-9cd375c5169d"

domain_cert = certificatemanager.Certificate.from_certificate_arn(self, "domainCert", certificate_arn)
pool.add_domain("CustomDomain",
    custom_domain=CustomDomainOptions(
        domain_name="user.myapp.com",
        certificate=domain_cert
    )
)
```

Read more about [Using the Amazon Cognito
Domain](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html) and [Using Your Own
Domain](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html).

The `signInUrl()` methods returns the fully qualified URL to the login page for the user pool. This page comes from the
hosted UI configured with Cognito. Learn more at [Hosted UI with the Amazon Cognito
Console](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-integration.html#cognito-user-pools-create-an-app-integration).

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
userpool = cognito.UserPool(self, "UserPool")
client = userpool.add_client("Client",
    # ...
    o_auth=OAuthSettings(
        flows=OAuthFlows(
            implicit_code_grant=True
        ),
        callback_urls=["https://myapp.com/home", "https://myapp.com/users"
        ]
    )
)
domain = userpool.add_domain("Domain")
sign_in_url = domain.sign_in_url(client,
    redirect_uri="https://myapp.com/home"
)
```

Existing domains can be imported into CDK apps using `UserPoolDomain.fromDomainName()` API

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
my_user_pool_domain = cognito.UserPoolDomain.from_domain_name(self, "my-user-pool-domain", "domain-name")
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
import aws_cdk.core
import constructs


@jsii.enum(jsii_type="@aws-cdk/aws-cognito.AccountRecovery")
class AccountRecovery(enum.Enum):
    """How will a user be able to recover their account?

    When a user forgets their password, they can have a code sent to their verified email or verified phone to recover their account.
    You can choose the preferred way to send codes below.
    We recommend not allowing phone to be used for both password resets and multi-factor authentication (MFA).

    :see: https://docs.aws.amazon.com/cognito/latest/developerguide/how-to-recover-a-user-account.html
    """

    EMAIL_AND_PHONE_WITHOUT_MFA = "EMAIL_AND_PHONE_WITHOUT_MFA"
    """Email if available, otherwise phone, but don’t allow a user to reset their password via phone if they are also using it for MFA."""
    PHONE_WITHOUT_MFA_AND_EMAIL = "PHONE_WITHOUT_MFA_AND_EMAIL"
    """Phone if available, otherwise email, but don’t allow a user to reset their password via phone if they are also using it for MFA."""
    EMAIL_ONLY = "EMAIL_ONLY"
    """Email only."""
    PHONE_ONLY_WITHOUT_MFA = "PHONE_ONLY_WITHOUT_MFA"
    """Phone only, but don’t allow a user to reset their password via phone if they are also using it for MFA."""
    PHONE_AND_EMAIL = "PHONE_AND_EMAIL"
    """(Not Recommended) Phone if available, otherwise email, and do allow a user to reset their password via phone if they are also using it for MFA."""
    NONE = "NONE"
    """None – users will have to contact an administrator to reset their passwords."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.AttributeMapping",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "birthdate": "birthdate",
        "custom": "custom",
        "email": "email",
        "family_name": "familyName",
        "fullname": "fullname",
        "gender": "gender",
        "given_name": "givenName",
        "last_update_time": "lastUpdateTime",
        "locale": "locale",
        "middle_name": "middleName",
        "nickname": "nickname",
        "phone_number": "phoneNumber",
        "preferred_username": "preferredUsername",
        "profile_page": "profilePage",
        "profile_picture": "profilePicture",
        "timezone": "timezone",
        "website": "website",
    },
)
class AttributeMapping:
    def __init__(
        self,
        *,
        address: typing.Optional["ProviderAttribute"] = None,
        birthdate: typing.Optional["ProviderAttribute"] = None,
        custom: typing.Optional[typing.Mapping[builtins.str, "ProviderAttribute"]] = None,
        email: typing.Optional["ProviderAttribute"] = None,
        family_name: typing.Optional["ProviderAttribute"] = None,
        fullname: typing.Optional["ProviderAttribute"] = None,
        gender: typing.Optional["ProviderAttribute"] = None,
        given_name: typing.Optional["ProviderAttribute"] = None,
        last_update_time: typing.Optional["ProviderAttribute"] = None,
        locale: typing.Optional["ProviderAttribute"] = None,
        middle_name: typing.Optional["ProviderAttribute"] = None,
        nickname: typing.Optional["ProviderAttribute"] = None,
        phone_number: typing.Optional["ProviderAttribute"] = None,
        preferred_username: typing.Optional["ProviderAttribute"] = None,
        profile_page: typing.Optional["ProviderAttribute"] = None,
        profile_picture: typing.Optional["ProviderAttribute"] = None,
        timezone: typing.Optional["ProviderAttribute"] = None,
        website: typing.Optional["ProviderAttribute"] = None,
    ) -> None:
        """The mapping of user pool attributes to the attributes provided by the identity providers.

        :param address: The user's postal address is a required attribute. Default: - not mapped
        :param birthdate: The user's birthday. Default: - not mapped
        :param custom: Specify custom attribute mapping here and mapping for any standard attributes not supported yet. Default: - no custom attribute mapping
        :param email: The user's e-mail address. Default: - not mapped
        :param family_name: The surname or last name of user. Default: - not mapped
        :param fullname: The user's full name in displayable form. Default: - not mapped
        :param gender: The user's gender. Default: - not mapped
        :param given_name: The user's first name or give name. Default: - not mapped
        :param last_update_time: Time, the user's information was last updated. Default: - not mapped
        :param locale: The user's locale. Default: - not mapped
        :param middle_name: The user's middle name. Default: - not mapped
        :param nickname: The user's nickname or casual name. Default: - not mapped
        :param phone_number: The user's telephone number. Default: - not mapped
        :param preferred_username: The user's preferred username. Default: - not mapped
        :param profile_page: The URL to the user's profile page. Default: - not mapped
        :param profile_picture: The URL to the user's profile picture. Default: - not mapped
        :param timezone: The user's time zone. Default: - not mapped
        :param website: The URL to the user's web page or blog. Default: - not mapped
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if birthdate is not None:
            self._values["birthdate"] = birthdate
        if custom is not None:
            self._values["custom"] = custom
        if email is not None:
            self._values["email"] = email
        if family_name is not None:
            self._values["family_name"] = family_name
        if fullname is not None:
            self._values["fullname"] = fullname
        if gender is not None:
            self._values["gender"] = gender
        if given_name is not None:
            self._values["given_name"] = given_name
        if last_update_time is not None:
            self._values["last_update_time"] = last_update_time
        if locale is not None:
            self._values["locale"] = locale
        if middle_name is not None:
            self._values["middle_name"] = middle_name
        if nickname is not None:
            self._values["nickname"] = nickname
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if preferred_username is not None:
            self._values["preferred_username"] = preferred_username
        if profile_page is not None:
            self._values["profile_page"] = profile_page
        if profile_picture is not None:
            self._values["profile_picture"] = profile_picture
        if timezone is not None:
            self._values["timezone"] = timezone
        if website is not None:
            self._values["website"] = website

    @builtins.property
    def address(self) -> typing.Optional["ProviderAttribute"]:
        """The user's postal address is a required attribute.

        :default: - not mapped
        """
        result = self._values.get("address")
        return result

    @builtins.property
    def birthdate(self) -> typing.Optional["ProviderAttribute"]:
        """The user's birthday.

        :default: - not mapped
        """
        result = self._values.get("birthdate")
        return result

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "ProviderAttribute"]]:
        """Specify custom attribute mapping here and mapping for any standard attributes not supported yet.

        :default: - no custom attribute mapping
        """
        result = self._values.get("custom")
        return result

    @builtins.property
    def email(self) -> typing.Optional["ProviderAttribute"]:
        """The user's e-mail address.

        :default: - not mapped
        """
        result = self._values.get("email")
        return result

    @builtins.property
    def family_name(self) -> typing.Optional["ProviderAttribute"]:
        """The surname or last name of user.

        :default: - not mapped
        """
        result = self._values.get("family_name")
        return result

    @builtins.property
    def fullname(self) -> typing.Optional["ProviderAttribute"]:
        """The user's full name in displayable form.

        :default: - not mapped
        """
        result = self._values.get("fullname")
        return result

    @builtins.property
    def gender(self) -> typing.Optional["ProviderAttribute"]:
        """The user's gender.

        :default: - not mapped
        """
        result = self._values.get("gender")
        return result

    @builtins.property
    def given_name(self) -> typing.Optional["ProviderAttribute"]:
        """The user's first name or give name.

        :default: - not mapped
        """
        result = self._values.get("given_name")
        return result

    @builtins.property
    def last_update_time(self) -> typing.Optional["ProviderAttribute"]:
        """Time, the user's information was last updated.

        :default: - not mapped
        """
        result = self._values.get("last_update_time")
        return result

    @builtins.property
    def locale(self) -> typing.Optional["ProviderAttribute"]:
        """The user's locale.

        :default: - not mapped
        """
        result = self._values.get("locale")
        return result

    @builtins.property
    def middle_name(self) -> typing.Optional["ProviderAttribute"]:
        """The user's middle name.

        :default: - not mapped
        """
        result = self._values.get("middle_name")
        return result

    @builtins.property
    def nickname(self) -> typing.Optional["ProviderAttribute"]:
        """The user's nickname or casual name.

        :default: - not mapped
        """
        result = self._values.get("nickname")
        return result

    @builtins.property
    def phone_number(self) -> typing.Optional["ProviderAttribute"]:
        """The user's telephone number.

        :default: - not mapped
        """
        result = self._values.get("phone_number")
        return result

    @builtins.property
    def preferred_username(self) -> typing.Optional["ProviderAttribute"]:
        """The user's preferred username.

        :default: - not mapped
        """
        result = self._values.get("preferred_username")
        return result

    @builtins.property
    def profile_page(self) -> typing.Optional["ProviderAttribute"]:
        """The URL to the user's profile page.

        :default: - not mapped
        """
        result = self._values.get("profile_page")
        return result

    @builtins.property
    def profile_picture(self) -> typing.Optional["ProviderAttribute"]:
        """The URL to the user's profile picture.

        :default: - not mapped
        """
        result = self._values.get("profile_picture")
        return result

    @builtins.property
    def timezone(self) -> typing.Optional["ProviderAttribute"]:
        """The user's time zone.

        :default: - not mapped
        """
        result = self._values.get("timezone")
        return result

    @builtins.property
    def website(self) -> typing.Optional["ProviderAttribute"]:
        """The URL to the user's web page or blog.

        :default: - not mapped
        """
        result = self._values.get("website")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttributeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.AuthFlow",
    jsii_struct_bases=[],
    name_mapping={
        "admin_user_password": "adminUserPassword",
        "custom": "custom",
        "user_password": "userPassword",
        "user_srp": "userSrp",
    },
)
class AuthFlow:
    def __init__(
        self,
        *,
        admin_user_password: typing.Optional[builtins.bool] = None,
        custom: typing.Optional[builtins.bool] = None,
        user_password: typing.Optional[builtins.bool] = None,
        user_srp: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Types of authentication flow.

        :param admin_user_password: Enable admin based user password authentication flow. Default: false
        :param custom: Enable custom authentication flow. Default: false
        :param user_password: Enable auth using username & password. Default: false
        :param user_srp: Enable SRP based authentication. Default: false

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if admin_user_password is not None:
            self._values["admin_user_password"] = admin_user_password
        if custom is not None:
            self._values["custom"] = custom
        if user_password is not None:
            self._values["user_password"] = user_password
        if user_srp is not None:
            self._values["user_srp"] = user_srp

    @builtins.property
    def admin_user_password(self) -> typing.Optional[builtins.bool]:
        """Enable admin based user password authentication flow.

        :default: false
        """
        result = self._values.get("admin_user_password")
        return result

    @builtins.property
    def custom(self) -> typing.Optional[builtins.bool]:
        """Enable custom authentication flow.

        :default: false
        """
        result = self._values.get("custom")
        return result

    @builtins.property
    def user_password(self) -> typing.Optional[builtins.bool]:
        """Enable auth using username & password.

        :default: false
        """
        result = self._values.get("user_password")
        return result

    @builtins.property
    def user_srp(self) -> typing.Optional[builtins.bool]:
        """Enable SRP based authentication.

        :default: false
        """
        result = self._values.get("user_srp")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthFlow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.AutoVerifiedAttrs",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "phone": "phone"},
)
class AutoVerifiedAttrs:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.bool] = None,
        phone: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Attributes that can be automatically verified for users in a user pool.

        :param email: Whether the email address of the user should be auto verified at sign up. Note: If both ``email`` and ``phone`` is set, Cognito only verifies the phone number. To also verify email, see here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html Default: - true, if email is turned on for ``signIn``. false, otherwise.
        :param phone: Whether the phone number of the user should be auto verified at sign up. Default: - true, if phone is turned on for ``signIn``. false, otherwise.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if phone is not None:
            self._values["phone"] = phone

    @builtins.property
    def email(self) -> typing.Optional[builtins.bool]:
        """Whether the email address of the user should be auto verified at sign up.

        Note: If both ``email`` and ``phone`` is set, Cognito only verifies the phone number. To also verify email, see here -
        https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html

        :default: - true, if email is turned on for ``signIn``. false, otherwise.
        """
        result = self._values.get("email")
        return result

    @builtins.property
    def phone(self) -> typing.Optional[builtins.bool]:
        """Whether the phone number of the user should be auto verified at sign up.

        :default: - true, if phone is turned on for ``signIn``. false, otherwise.
        """
        result = self._values.get("phone")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoVerifiedAttrs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIdentityPool(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool",
):
    """A CloudFormation ``AWS::Cognito::IdentityPool``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html
    :cloudformationResource: AWS::Cognito::IdentityPool
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        allow_unauthenticated_identities: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        allow_classic_flow: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        cognito_events: typing.Any = None,
        cognito_identity_providers: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoIdentityProviderProperty"]]]] = None,
        cognito_streams: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoStreamsProperty"]] = None,
        developer_provider_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider_arns: typing.Optional[typing.List[builtins.str]] = None,
        push_sync: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.PushSyncProperty"]] = None,
        saml_provider_arns: typing.Optional[typing.List[builtins.str]] = None,
        supported_login_providers: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::Cognito::IdentityPool``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param allow_unauthenticated_identities: ``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.
        :param allow_classic_flow: ``AWS::Cognito::IdentityPool.AllowClassicFlow``.
        :param cognito_events: ``AWS::Cognito::IdentityPool.CognitoEvents``.
        :param cognito_identity_providers: ``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.
        :param cognito_streams: ``AWS::Cognito::IdentityPool.CognitoStreams``.
        :param developer_provider_name: ``AWS::Cognito::IdentityPool.DeveloperProviderName``.
        :param identity_pool_name: ``AWS::Cognito::IdentityPool.IdentityPoolName``.
        :param open_id_connect_provider_arns: ``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.
        :param push_sync: ``AWS::Cognito::IdentityPool.PushSync``.
        :param saml_provider_arns: ``AWS::Cognito::IdentityPool.SamlProviderARNs``.
        :param supported_login_providers: ``AWS::Cognito::IdentityPool.SupportedLoginProviders``.
        """
        props = CfnIdentityPoolProps(
            allow_unauthenticated_identities=allow_unauthenticated_identities,
            allow_classic_flow=allow_classic_flow,
            cognito_events=cognito_events,
            cognito_identity_providers=cognito_identity_providers,
            cognito_streams=cognito_streams,
            developer_provider_name=developer_provider_name,
            identity_pool_name=identity_pool_name,
            open_id_connect_provider_arns=open_id_connect_provider_arns,
            push_sync=push_sync,
            saml_provider_arns=saml_provider_arns,
            supported_login_providers=supported_login_providers,
        )

        jsii.create(CfnIdentityPool, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowUnauthenticatedIdentities")
    def allow_unauthenticated_identities(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowunauthenticatedidentities
        """
        return jsii.get(self, "allowUnauthenticatedIdentities")

    @allow_unauthenticated_identities.setter # type: ignore
    def allow_unauthenticated_identities(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "allowUnauthenticatedIdentities", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cognitoEvents")
    def cognito_events(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.CognitoEvents``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoevents
        """
        return jsii.get(self, "cognitoEvents")

    @cognito_events.setter # type: ignore
    def cognito_events(self, value: typing.Any) -> None:
        jsii.set(self, "cognitoEvents", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="supportedLoginProviders")
    def supported_login_providers(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.SupportedLoginProviders``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-supportedloginproviders
        """
        return jsii.get(self, "supportedLoginProviders")

    @supported_login_providers.setter # type: ignore
    def supported_login_providers(self, value: typing.Any) -> None:
        jsii.set(self, "supportedLoginProviders", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowClassicFlow")
    def allow_classic_flow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::IdentityPool.AllowClassicFlow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowclassicflow
        """
        return jsii.get(self, "allowClassicFlow")

    @allow_classic_flow.setter # type: ignore
    def allow_classic_flow(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "allowClassicFlow", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cognitoIdentityProviders")
    def cognito_identity_providers(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoIdentityProviderProperty"]]]]:
        """``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoidentityproviders
        """
        return jsii.get(self, "cognitoIdentityProviders")

    @cognito_identity_providers.setter # type: ignore
    def cognito_identity_providers(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoIdentityProviderProperty"]]]],
    ) -> None:
        jsii.set(self, "cognitoIdentityProviders", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cognitoStreams")
    def cognito_streams(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoStreamsProperty"]]:
        """``AWS::Cognito::IdentityPool.CognitoStreams``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitostreams
        """
        return jsii.get(self, "cognitoStreams")

    @cognito_streams.setter # type: ignore
    def cognito_streams(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.CognitoStreamsProperty"]],
    ) -> None:
        jsii.set(self, "cognitoStreams", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="developerProviderName")
    def developer_provider_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::IdentityPool.DeveloperProviderName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-developerprovidername
        """
        return jsii.get(self, "developerProviderName")

    @developer_provider_name.setter # type: ignore
    def developer_provider_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "developerProviderName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identityPoolName")
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::IdentityPool.IdentityPoolName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-identitypoolname
        """
        return jsii.get(self, "identityPoolName")

    @identity_pool_name.setter # type: ignore
    def identity_pool_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "identityPoolName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="openIdConnectProviderArns")
    def open_id_connect_provider_arns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-openidconnectproviderarns
        """
        return jsii.get(self, "openIdConnectProviderArns")

    @open_id_connect_provider_arns.setter # type: ignore
    def open_id_connect_provider_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "openIdConnectProviderArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pushSync")
    def push_sync(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.PushSyncProperty"]]:
        """``AWS::Cognito::IdentityPool.PushSync``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-pushsync
        """
        return jsii.get(self, "pushSync")

    @push_sync.setter # type: ignore
    def push_sync(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPool.PushSyncProperty"]],
    ) -> None:
        jsii.set(self, "pushSync", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="samlProviderArns")
    def saml_provider_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::IdentityPool.SamlProviderARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-samlproviderarns
        """
        return jsii.get(self, "samlProviderArns")

    @saml_provider_arns.setter # type: ignore
    def saml_provider_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "samlProviderArns", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.CognitoIdentityProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "provider_name": "providerName",
            "server_side_token_check": "serverSideTokenCheck",
        },
    )
    class CognitoIdentityProviderProperty:
        def __init__(
            self,
            *,
            client_id: typing.Optional[builtins.str] = None,
            provider_name: typing.Optional[builtins.str] = None,
            server_side_token_check: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param client_id: ``CfnIdentityPool.CognitoIdentityProviderProperty.ClientId``.
            :param provider_name: ``CfnIdentityPool.CognitoIdentityProviderProperty.ProviderName``.
            :param server_side_token_check: ``CfnIdentityPool.CognitoIdentityProviderProperty.ServerSideTokenCheck``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if client_id is not None:
                self._values["client_id"] = client_id
            if provider_name is not None:
                self._values["provider_name"] = provider_name
            if server_side_token_check is not None:
                self._values["server_side_token_check"] = server_side_token_check

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPool.CognitoIdentityProviderProperty.ClientId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-clientid
            """
            result = self._values.get("client_id")
            return result

        @builtins.property
        def provider_name(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPool.CognitoIdentityProviderProperty.ProviderName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-providername
            """
            result = self._values.get("provider_name")
            return result

        @builtins.property
        def server_side_token_check(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnIdentityPool.CognitoIdentityProviderProperty.ServerSideTokenCheck``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html#cfn-cognito-identitypool-cognitoidentityprovider-serversidetokencheck
            """
            result = self._values.get("server_side_token_check")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoIdentityProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.CognitoStreamsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "streaming_status": "streamingStatus",
            "stream_name": "streamName",
        },
    )
    class CognitoStreamsProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            streaming_status: typing.Optional[builtins.str] = None,
            stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param role_arn: ``CfnIdentityPool.CognitoStreamsProperty.RoleArn``.
            :param streaming_status: ``CfnIdentityPool.CognitoStreamsProperty.StreamingStatus``.
            :param stream_name: ``CfnIdentityPool.CognitoStreamsProperty.StreamName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if streaming_status is not None:
                self._values["streaming_status"] = streaming_status
            if stream_name is not None:
                self._values["stream_name"] = stream_name

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPool.CognitoStreamsProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def streaming_status(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPool.CognitoStreamsProperty.StreamingStatus``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-streamingstatus
            """
            result = self._values.get("streaming_status")
            return result

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPool.CognitoStreamsProperty.StreamName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitostreams.html#cfn-cognito-identitypool-cognitostreams-streamname
            """
            result = self._values.get("stream_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoStreamsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnIdentityPool.PushSyncProperty",
        jsii_struct_bases=[],
        name_mapping={"application_arns": "applicationArns", "role_arn": "roleArn"},
    )
    class PushSyncProperty:
        def __init__(
            self,
            *,
            application_arns: typing.Optional[typing.List[builtins.str]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param application_arns: ``CfnIdentityPool.PushSyncProperty.ApplicationArns``.
            :param role_arn: ``CfnIdentityPool.PushSyncProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if application_arns is not None:
                self._values["application_arns"] = application_arns
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def application_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnIdentityPool.PushSyncProperty.ApplicationArns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html#cfn-cognito-identitypool-pushsync-applicationarns
            """
            result = self._values.get("application_arns")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPool.PushSyncProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-pushsync.html#cfn-cognito-identitypool-pushsync-rolearn
            """
            result = self._values.get("role_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PushSyncProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_unauthenticated_identities": "allowUnauthenticatedIdentities",
        "allow_classic_flow": "allowClassicFlow",
        "cognito_events": "cognitoEvents",
        "cognito_identity_providers": "cognitoIdentityProviders",
        "cognito_streams": "cognitoStreams",
        "developer_provider_name": "developerProviderName",
        "identity_pool_name": "identityPoolName",
        "open_id_connect_provider_arns": "openIdConnectProviderArns",
        "push_sync": "pushSync",
        "saml_provider_arns": "samlProviderArns",
        "supported_login_providers": "supportedLoginProviders",
    },
)
class CfnIdentityPoolProps:
    def __init__(
        self,
        *,
        allow_unauthenticated_identities: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        allow_classic_flow: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        cognito_events: typing.Any = None,
        cognito_identity_providers: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnIdentityPool.CognitoIdentityProviderProperty]]]] = None,
        cognito_streams: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIdentityPool.CognitoStreamsProperty]] = None,
        developer_provider_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider_arns: typing.Optional[typing.List[builtins.str]] = None,
        push_sync: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIdentityPool.PushSyncProperty]] = None,
        saml_provider_arns: typing.Optional[typing.List[builtins.str]] = None,
        supported_login_providers: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::IdentityPool``.

        :param allow_unauthenticated_identities: ``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.
        :param allow_classic_flow: ``AWS::Cognito::IdentityPool.AllowClassicFlow``.
        :param cognito_events: ``AWS::Cognito::IdentityPool.CognitoEvents``.
        :param cognito_identity_providers: ``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.
        :param cognito_streams: ``AWS::Cognito::IdentityPool.CognitoStreams``.
        :param developer_provider_name: ``AWS::Cognito::IdentityPool.DeveloperProviderName``.
        :param identity_pool_name: ``AWS::Cognito::IdentityPool.IdentityPoolName``.
        :param open_id_connect_provider_arns: ``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.
        :param push_sync: ``AWS::Cognito::IdentityPool.PushSync``.
        :param saml_provider_arns: ``AWS::Cognito::IdentityPool.SamlProviderARNs``.
        :param supported_login_providers: ``AWS::Cognito::IdentityPool.SupportedLoginProviders``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "allow_unauthenticated_identities": allow_unauthenticated_identities,
        }
        if allow_classic_flow is not None:
            self._values["allow_classic_flow"] = allow_classic_flow
        if cognito_events is not None:
            self._values["cognito_events"] = cognito_events
        if cognito_identity_providers is not None:
            self._values["cognito_identity_providers"] = cognito_identity_providers
        if cognito_streams is not None:
            self._values["cognito_streams"] = cognito_streams
        if developer_provider_name is not None:
            self._values["developer_provider_name"] = developer_provider_name
        if identity_pool_name is not None:
            self._values["identity_pool_name"] = identity_pool_name
        if open_id_connect_provider_arns is not None:
            self._values["open_id_connect_provider_arns"] = open_id_connect_provider_arns
        if push_sync is not None:
            self._values["push_sync"] = push_sync
        if saml_provider_arns is not None:
            self._values["saml_provider_arns"] = saml_provider_arns
        if supported_login_providers is not None:
            self._values["supported_login_providers"] = supported_login_providers

    @builtins.property
    def allow_unauthenticated_identities(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::Cognito::IdentityPool.AllowUnauthenticatedIdentities``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowunauthenticatedidentities
        """
        result = self._values.get("allow_unauthenticated_identities")
        assert result is not None, "Required property 'allow_unauthenticated_identities' is missing"
        return result

    @builtins.property
    def allow_classic_flow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::IdentityPool.AllowClassicFlow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-allowclassicflow
        """
        result = self._values.get("allow_classic_flow")
        return result

    @builtins.property
    def cognito_events(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.CognitoEvents``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoevents
        """
        result = self._values.get("cognito_events")
        return result

    @builtins.property
    def cognito_identity_providers(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnIdentityPool.CognitoIdentityProviderProperty]]]]:
        """``AWS::Cognito::IdentityPool.CognitoIdentityProviders``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitoidentityproviders
        """
        result = self._values.get("cognito_identity_providers")
        return result

    @builtins.property
    def cognito_streams(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIdentityPool.CognitoStreamsProperty]]:
        """``AWS::Cognito::IdentityPool.CognitoStreams``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-cognitostreams
        """
        result = self._values.get("cognito_streams")
        return result

    @builtins.property
    def developer_provider_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::IdentityPool.DeveloperProviderName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-developerprovidername
        """
        result = self._values.get("developer_provider_name")
        return result

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::IdentityPool.IdentityPoolName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-identitypoolname
        """
        result = self._values.get("identity_pool_name")
        return result

    @builtins.property
    def open_id_connect_provider_arns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::IdentityPool.OpenIdConnectProviderARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-openidconnectproviderarns
        """
        result = self._values.get("open_id_connect_provider_arns")
        return result

    @builtins.property
    def push_sync(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnIdentityPool.PushSyncProperty]]:
        """``AWS::Cognito::IdentityPool.PushSync``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-pushsync
        """
        result = self._values.get("push_sync")
        return result

    @builtins.property
    def saml_provider_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::IdentityPool.SamlProviderARNs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-samlproviderarns
        """
        result = self._values.get("saml_provider_arns")
        return result

    @builtins.property
    def supported_login_providers(self) -> typing.Any:
        """``AWS::Cognito::IdentityPool.SupportedLoginProviders``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html#cfn-cognito-identitypool-supportedloginproviders
        """
        result = self._values.get("supported_login_providers")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIdentityPoolRoleAttachment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment",
):
    """A CloudFormation ``AWS::Cognito::IdentityPoolRoleAttachment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html
    :cloudformationResource: AWS::Cognito::IdentityPoolRoleAttachment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        identity_pool_id: builtins.str,
        role_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.RoleMappingProperty"]]]] = None,
        roles: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::Cognito::IdentityPoolRoleAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param identity_pool_id: ``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.
        :param role_mappings: ``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.
        :param roles: ``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.
        """
        props = CfnIdentityPoolRoleAttachmentProps(
            identity_pool_id=identity_pool_id, role_mappings=role_mappings, roles=roles
        )

        jsii.create(CfnIdentityPoolRoleAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        """``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-identitypoolid
        """
        return jsii.get(self, "identityPoolId")

    @identity_pool_id.setter # type: ignore
    def identity_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "identityPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Any:
        """``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-roles
        """
        return jsii.get(self, "roles")

    @roles.setter # type: ignore
    def roles(self, value: typing.Any) -> None:
        jsii.set(self, "roles", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleMappings")
    def role_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.RoleMappingProperty"]]]]:
        """``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-rolemappings
        """
        return jsii.get(self, "roleMappings")

    @role_mappings.setter # type: ignore
    def role_mappings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.RoleMappingProperty"]]]],
    ) -> None:
        jsii.set(self, "roleMappings", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.MappingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "claim": "claim",
            "match_type": "matchType",
            "role_arn": "roleArn",
            "value": "value",
        },
    )
    class MappingRuleProperty:
        def __init__(
            self,
            *,
            claim: builtins.str,
            match_type: builtins.str,
            role_arn: builtins.str,
            value: builtins.str,
        ) -> None:
            """
            :param claim: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Claim``.
            :param match_type: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.MatchType``.
            :param role_arn: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.RoleARN``.
            :param value: ``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "claim": claim,
                "match_type": match_type,
                "role_arn": role_arn,
                "value": value,
            }

        @builtins.property
        def claim(self) -> builtins.str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Claim``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-claim
            """
            result = self._values.get("claim")
            assert result is not None, "Required property 'claim' is missing"
            return result

        @builtins.property
        def match_type(self) -> builtins.str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.MatchType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-matchtype
            """
            result = self._values.get("match_type")
            assert result is not None, "Required property 'match_type' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.RoleARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnIdentityPoolRoleAttachment.MappingRuleProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-mappingrule.html#cfn-cognito-identitypoolroleattachment-mappingrule-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.RoleMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "ambiguous_role_resolution": "ambiguousRoleResolution",
            "identity_provider": "identityProvider",
            "rules_configuration": "rulesConfiguration",
        },
    )
    class RoleMappingProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            ambiguous_role_resolution: typing.Optional[builtins.str] = None,
            identity_provider: typing.Optional[builtins.str] = None,
            rules_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty"]] = None,
        ) -> None:
            """
            :param type: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.Type``.
            :param ambiguous_role_resolution: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.AmbiguousRoleResolution``.
            :param identity_provider: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.IdentityProvider``.
            :param rules_configuration: ``CfnIdentityPoolRoleAttachment.RoleMappingProperty.RulesConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if ambiguous_role_resolution is not None:
                self._values["ambiguous_role_resolution"] = ambiguous_role_resolution
            if identity_provider is not None:
                self._values["identity_provider"] = identity_provider
            if rules_configuration is not None:
                self._values["rules_configuration"] = rules_configuration

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def ambiguous_role_resolution(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.AmbiguousRoleResolution``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-ambiguousroleresolution
            """
            result = self._values.get("ambiguous_role_resolution")
            return result

        @builtins.property
        def identity_provider(self) -> typing.Optional[builtins.str]:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.IdentityProvider``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-identityprovider
            """
            result = self._values.get("identity_provider")
            return result

        @builtins.property
        def rules_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty"]]:
            """``CfnIdentityPoolRoleAttachment.RoleMappingProperty.RulesConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-rulesconfiguration
            """
            result = self._values.get("rules_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class RulesConfigurationTypeProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.MappingRuleProperty"]]],
        ) -> None:
            """
            :param rules: ``CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty.Rules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rulesconfigurationtype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIdentityPoolRoleAttachment.MappingRuleProperty"]]]:
            """``CfnIdentityPoolRoleAttachment.RulesConfigurationTypeProperty.Rules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rulesconfigurationtype.html#cfn-cognito-identitypoolroleattachment-rulesconfigurationtype-rules
            """
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnIdentityPoolRoleAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_id": "identityPoolId",
        "role_mappings": "roleMappings",
        "roles": "roles",
    },
)
class CfnIdentityPoolRoleAttachmentProps:
    def __init__(
        self,
        *,
        identity_pool_id: builtins.str,
        role_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnIdentityPoolRoleAttachment.RoleMappingProperty]]]] = None,
        roles: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::IdentityPoolRoleAttachment``.

        :param identity_pool_id: ``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.
        :param role_mappings: ``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.
        :param roles: ``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "identity_pool_id": identity_pool_id,
        }
        if role_mappings is not None:
            self._values["role_mappings"] = role_mappings
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        """``AWS::Cognito::IdentityPoolRoleAttachment.IdentityPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-identitypoolid
        """
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return result

    @builtins.property
    def role_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnIdentityPoolRoleAttachment.RoleMappingProperty]]]]:
        """``AWS::Cognito::IdentityPoolRoleAttachment.RoleMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-rolemappings
        """
        result = self._values.get("role_mappings")
        return result

    @builtins.property
    def roles(self) -> typing.Any:
        """``AWS::Cognito::IdentityPoolRoleAttachment.Roles``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html#cfn-cognito-identitypoolroleattachment-roles
        """
        result = self._values.get("roles")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityPoolRoleAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPool(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPool",
):
    """A CloudFormation ``AWS::Cognito::UserPool``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html
    :cloudformationResource: AWS::Cognito::UserPool
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        account_recovery_setting: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.AccountRecoverySettingProperty"]] = None,
        admin_create_user_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.AdminCreateUserConfigProperty"]] = None,
        alias_attributes: typing.Optional[typing.List[builtins.str]] = None,
        auto_verified_attributes: typing.Optional[typing.List[builtins.str]] = None,
        device_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.DeviceConfigurationProperty"]] = None,
        email_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.EmailConfigurationProperty"]] = None,
        email_verification_message: typing.Optional[builtins.str] = None,
        email_verification_subject: typing.Optional[builtins.str] = None,
        enabled_mfas: typing.Optional[typing.List[builtins.str]] = None,
        lambda_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.LambdaConfigProperty"]] = None,
        mfa_configuration: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.PoliciesProperty"]] = None,
        schema: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SchemaAttributeProperty"]]]] = None,
        sms_authentication_message: typing.Optional[builtins.str] = None,
        sms_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SmsConfigurationProperty"]] = None,
        sms_verification_message: typing.Optional[builtins.str] = None,
        username_attributes: typing.Optional[typing.List[builtins.str]] = None,
        username_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.UsernameConfigurationProperty"]] = None,
        user_pool_add_ons: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.UserPoolAddOnsProperty"]] = None,
        user_pool_name: typing.Optional[builtins.str] = None,
        user_pool_tags: typing.Any = None,
        verification_message_template: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.VerificationMessageTemplateProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPool``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_recovery_setting: ``AWS::Cognito::UserPool.AccountRecoverySetting``.
        :param admin_create_user_config: ``AWS::Cognito::UserPool.AdminCreateUserConfig``.
        :param alias_attributes: ``AWS::Cognito::UserPool.AliasAttributes``.
        :param auto_verified_attributes: ``AWS::Cognito::UserPool.AutoVerifiedAttributes``.
        :param device_configuration: ``AWS::Cognito::UserPool.DeviceConfiguration``.
        :param email_configuration: ``AWS::Cognito::UserPool.EmailConfiguration``.
        :param email_verification_message: ``AWS::Cognito::UserPool.EmailVerificationMessage``.
        :param email_verification_subject: ``AWS::Cognito::UserPool.EmailVerificationSubject``.
        :param enabled_mfas: ``AWS::Cognito::UserPool.EnabledMfas``.
        :param lambda_config: ``AWS::Cognito::UserPool.LambdaConfig``.
        :param mfa_configuration: ``AWS::Cognito::UserPool.MfaConfiguration``.
        :param policies: ``AWS::Cognito::UserPool.Policies``.
        :param schema: ``AWS::Cognito::UserPool.Schema``.
        :param sms_authentication_message: ``AWS::Cognito::UserPool.SmsAuthenticationMessage``.
        :param sms_configuration: ``AWS::Cognito::UserPool.SmsConfiguration``.
        :param sms_verification_message: ``AWS::Cognito::UserPool.SmsVerificationMessage``.
        :param username_attributes: ``AWS::Cognito::UserPool.UsernameAttributes``.
        :param username_configuration: ``AWS::Cognito::UserPool.UsernameConfiguration``.
        :param user_pool_add_ons: ``AWS::Cognito::UserPool.UserPoolAddOns``.
        :param user_pool_name: ``AWS::Cognito::UserPool.UserPoolName``.
        :param user_pool_tags: ``AWS::Cognito::UserPool.UserPoolTags``.
        :param verification_message_template: ``AWS::Cognito::UserPool.VerificationMessageTemplate``.
        """
        props = CfnUserPoolProps(
            account_recovery_setting=account_recovery_setting,
            admin_create_user_config=admin_create_user_config,
            alias_attributes=alias_attributes,
            auto_verified_attributes=auto_verified_attributes,
            device_configuration=device_configuration,
            email_configuration=email_configuration,
            email_verification_message=email_verification_message,
            email_verification_subject=email_verification_subject,
            enabled_mfas=enabled_mfas,
            lambda_config=lambda_config,
            mfa_configuration=mfa_configuration,
            policies=policies,
            schema=schema,
            sms_authentication_message=sms_authentication_message,
            sms_configuration=sms_configuration,
            sms_verification_message=sms_verification_message,
            username_attributes=username_attributes,
            username_configuration=username_configuration,
            user_pool_add_ons=user_pool_add_ons,
            user_pool_name=user_pool_name,
            user_pool_tags=user_pool_tags,
            verification_message_template=verification_message_template,
        )

        jsii.create(CfnUserPool, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrProviderName")
    def attr_provider_name(self) -> builtins.str:
        """
        :cloudformationAttribute: ProviderName
        """
        return jsii.get(self, "attrProviderName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrProviderUrl")
    def attr_provider_url(self) -> builtins.str:
        """
        :cloudformationAttribute: ProviderURL
        """
        return jsii.get(self, "attrProviderUrl")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Cognito::UserPool.UserPoolTags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooltags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accountRecoverySetting")
    def account_recovery_setting(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.AccountRecoverySettingProperty"]]:
        """``AWS::Cognito::UserPool.AccountRecoverySetting``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-accountrecoverysetting
        """
        return jsii.get(self, "accountRecoverySetting")

    @account_recovery_setting.setter # type: ignore
    def account_recovery_setting(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.AccountRecoverySettingProperty"]],
    ) -> None:
        jsii.set(self, "accountRecoverySetting", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="adminCreateUserConfig")
    def admin_create_user_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.AdminCreateUserConfigProperty"]]:
        """``AWS::Cognito::UserPool.AdminCreateUserConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-admincreateuserconfig
        """
        return jsii.get(self, "adminCreateUserConfig")

    @admin_create_user_config.setter # type: ignore
    def admin_create_user_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.AdminCreateUserConfigProperty"]],
    ) -> None:
        jsii.set(self, "adminCreateUserConfig", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliasAttributes")
    def alias_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.AliasAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-aliasattributes
        """
        return jsii.get(self, "aliasAttributes")

    @alias_attributes.setter # type: ignore
    def alias_attributes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "aliasAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoVerifiedAttributes")
    def auto_verified_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.AutoVerifiedAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-autoverifiedattributes
        """
        return jsii.get(self, "autoVerifiedAttributes")

    @auto_verified_attributes.setter # type: ignore
    def auto_verified_attributes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "autoVerifiedAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deviceConfiguration")
    def device_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.DeviceConfigurationProperty"]]:
        """``AWS::Cognito::UserPool.DeviceConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-deviceconfiguration
        """
        return jsii.get(self, "deviceConfiguration")

    @device_configuration.setter # type: ignore
    def device_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.DeviceConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "deviceConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="emailConfiguration")
    def email_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.EmailConfigurationProperty"]]:
        """``AWS::Cognito::UserPool.EmailConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailconfiguration
        """
        return jsii.get(self, "emailConfiguration")

    @email_configuration.setter # type: ignore
    def email_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.EmailConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "emailConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="emailVerificationMessage")
    def email_verification_message(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.EmailVerificationMessage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationmessage
        """
        return jsii.get(self, "emailVerificationMessage")

    @email_verification_message.setter # type: ignore
    def email_verification_message(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "emailVerificationMessage", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="emailVerificationSubject")
    def email_verification_subject(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.EmailVerificationSubject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationsubject
        """
        return jsii.get(self, "emailVerificationSubject")

    @email_verification_subject.setter # type: ignore
    def email_verification_subject(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "emailVerificationSubject", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabledMfas")
    def enabled_mfas(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.EnabledMfas``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-enabledmfas
        """
        return jsii.get(self, "enabledMfas")

    @enabled_mfas.setter # type: ignore
    def enabled_mfas(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "enabledMfas", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lambdaConfig")
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.LambdaConfigProperty"]]:
        """``AWS::Cognito::UserPool.LambdaConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-lambdaconfig
        """
        return jsii.get(self, "lambdaConfig")

    @lambda_config.setter # type: ignore
    def lambda_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.LambdaConfigProperty"]],
    ) -> None:
        jsii.set(self, "lambdaConfig", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mfaConfiguration")
    def mfa_configuration(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.MfaConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-mfaconfiguration
        """
        return jsii.get(self, "mfaConfiguration")

    @mfa_configuration.setter # type: ignore
    def mfa_configuration(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "mfaConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.PoliciesProperty"]]:
        """``AWS::Cognito::UserPool.Policies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-policies
        """
        return jsii.get(self, "policies")

    @policies.setter # type: ignore
    def policies(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.PoliciesProperty"]],
    ) -> None:
        jsii.set(self, "policies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="schema")
    def schema(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SchemaAttributeProperty"]]]]:
        """``AWS::Cognito::UserPool.Schema``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-schema
        """
        return jsii.get(self, "schema")

    @schema.setter # type: ignore
    def schema(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SchemaAttributeProperty"]]]],
    ) -> None:
        jsii.set(self, "schema", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="smsAuthenticationMessage")
    def sms_authentication_message(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.SmsAuthenticationMessage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsauthenticationmessage
        """
        return jsii.get(self, "smsAuthenticationMessage")

    @sms_authentication_message.setter # type: ignore
    def sms_authentication_message(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "smsAuthenticationMessage", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="smsConfiguration")
    def sms_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SmsConfigurationProperty"]]:
        """``AWS::Cognito::UserPool.SmsConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsconfiguration
        """
        return jsii.get(self, "smsConfiguration")

    @sms_configuration.setter # type: ignore
    def sms_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.SmsConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "smsConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="smsVerificationMessage")
    def sms_verification_message(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.SmsVerificationMessage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsverificationmessage
        """
        return jsii.get(self, "smsVerificationMessage")

    @sms_verification_message.setter # type: ignore
    def sms_verification_message(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "smsVerificationMessage", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="usernameAttributes")
    def username_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.UsernameAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameattributes
        """
        return jsii.get(self, "usernameAttributes")

    @username_attributes.setter # type: ignore
    def username_attributes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "usernameAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="usernameConfiguration")
    def username_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.UsernameConfigurationProperty"]]:
        """``AWS::Cognito::UserPool.UsernameConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameconfiguration
        """
        return jsii.get(self, "usernameConfiguration")

    @username_configuration.setter # type: ignore
    def username_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.UsernameConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "usernameConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolAddOns")
    def user_pool_add_ons(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.UserPoolAddOnsProperty"]]:
        """``AWS::Cognito::UserPool.UserPoolAddOns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooladdons
        """
        return jsii.get(self, "userPoolAddOns")

    @user_pool_add_ons.setter # type: ignore
    def user_pool_add_ons(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.UserPoolAddOnsProperty"]],
    ) -> None:
        jsii.set(self, "userPoolAddOns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolName")
    def user_pool_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.UserPoolName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpoolname
        """
        return jsii.get(self, "userPoolName")

    @user_pool_name.setter # type: ignore
    def user_pool_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "userPoolName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="verificationMessageTemplate")
    def verification_message_template(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.VerificationMessageTemplateProperty"]]:
        """``AWS::Cognito::UserPool.VerificationMessageTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-verificationmessagetemplate
        """
        return jsii.get(self, "verificationMessageTemplate")

    @verification_message_template.setter # type: ignore
    def verification_message_template(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.VerificationMessageTemplateProperty"]],
    ) -> None:
        jsii.set(self, "verificationMessageTemplate", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.AccountRecoverySettingProperty",
        jsii_struct_bases=[],
        name_mapping={"recovery_mechanisms": "recoveryMechanisms"},
    )
    class AccountRecoverySettingProperty:
        def __init__(
            self,
            *,
            recovery_mechanisms: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.RecoveryOptionProperty"]]]] = None,
        ) -> None:
            """
            :param recovery_mechanisms: ``CfnUserPool.AccountRecoverySettingProperty.RecoveryMechanisms``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-accountrecoverysetting.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if recovery_mechanisms is not None:
                self._values["recovery_mechanisms"] = recovery_mechanisms

        @builtins.property
        def recovery_mechanisms(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.RecoveryOptionProperty"]]]]:
            """``CfnUserPool.AccountRecoverySettingProperty.RecoveryMechanisms``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-accountrecoverysetting.html#cfn-cognito-userpool-accountrecoverysetting-recoverymechanisms
            """
            result = self._values.get("recovery_mechanisms")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountRecoverySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.AdminCreateUserConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_admin_create_user_only": "allowAdminCreateUserOnly",
            "invite_message_template": "inviteMessageTemplate",
            "unused_account_validity_days": "unusedAccountValidityDays",
        },
    )
    class AdminCreateUserConfigProperty:
        def __init__(
            self,
            *,
            allow_admin_create_user_only: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            invite_message_template: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.InviteMessageTemplateProperty"]] = None,
            unused_account_validity_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param allow_admin_create_user_only: ``CfnUserPool.AdminCreateUserConfigProperty.AllowAdminCreateUserOnly``.
            :param invite_message_template: ``CfnUserPool.AdminCreateUserConfigProperty.InviteMessageTemplate``.
            :param unused_account_validity_days: ``CfnUserPool.AdminCreateUserConfigProperty.UnusedAccountValidityDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if allow_admin_create_user_only is not None:
                self._values["allow_admin_create_user_only"] = allow_admin_create_user_only
            if invite_message_template is not None:
                self._values["invite_message_template"] = invite_message_template
            if unused_account_validity_days is not None:
                self._values["unused_account_validity_days"] = unused_account_validity_days

        @builtins.property
        def allow_admin_create_user_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.AdminCreateUserConfigProperty.AllowAdminCreateUserOnly``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-allowadmincreateuseronly
            """
            result = self._values.get("allow_admin_create_user_only")
            return result

        @builtins.property
        def invite_message_template(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.InviteMessageTemplateProperty"]]:
            """``CfnUserPool.AdminCreateUserConfigProperty.InviteMessageTemplate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-invitemessagetemplate
            """
            result = self._values.get("invite_message_template")
            return result

        @builtins.property
        def unused_account_validity_days(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.AdminCreateUserConfigProperty.UnusedAccountValidityDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-admincreateuserconfig.html#cfn-cognito-userpool-admincreateuserconfig-unusedaccountvaliditydays
            """
            result = self._values.get("unused_account_validity_days")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdminCreateUserConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.DeviceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "challenge_required_on_new_device": "challengeRequiredOnNewDevice",
            "device_only_remembered_on_user_prompt": "deviceOnlyRememberedOnUserPrompt",
        },
    )
    class DeviceConfigurationProperty:
        def __init__(
            self,
            *,
            challenge_required_on_new_device: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            device_only_remembered_on_user_prompt: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param challenge_required_on_new_device: ``CfnUserPool.DeviceConfigurationProperty.ChallengeRequiredOnNewDevice``.
            :param device_only_remembered_on_user_prompt: ``CfnUserPool.DeviceConfigurationProperty.DeviceOnlyRememberedOnUserPrompt``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if challenge_required_on_new_device is not None:
                self._values["challenge_required_on_new_device"] = challenge_required_on_new_device
            if device_only_remembered_on_user_prompt is not None:
                self._values["device_only_remembered_on_user_prompt"] = device_only_remembered_on_user_prompt

        @builtins.property
        def challenge_required_on_new_device(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.DeviceConfigurationProperty.ChallengeRequiredOnNewDevice``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html#cfn-cognito-userpool-deviceconfiguration-challengerequiredonnewdevice
            """
            result = self._values.get("challenge_required_on_new_device")
            return result

        @builtins.property
        def device_only_remembered_on_user_prompt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.DeviceConfigurationProperty.DeviceOnlyRememberedOnUserPrompt``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-deviceconfiguration.html#cfn-cognito-userpool-deviceconfiguration-deviceonlyrememberedonuserprompt
            """
            result = self._values.get("device_only_remembered_on_user_prompt")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.EmailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_set": "configurationSet",
            "email_sending_account": "emailSendingAccount",
            "from_": "from",
            "reply_to_email_address": "replyToEmailAddress",
            "source_arn": "sourceArn",
        },
    )
    class EmailConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_set: typing.Optional[builtins.str] = None,
            email_sending_account: typing.Optional[builtins.str] = None,
            from_: typing.Optional[builtins.str] = None,
            reply_to_email_address: typing.Optional[builtins.str] = None,
            source_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param configuration_set: ``CfnUserPool.EmailConfigurationProperty.ConfigurationSet``.
            :param email_sending_account: ``CfnUserPool.EmailConfigurationProperty.EmailSendingAccount``.
            :param from_: ``CfnUserPool.EmailConfigurationProperty.From``.
            :param reply_to_email_address: ``CfnUserPool.EmailConfigurationProperty.ReplyToEmailAddress``.
            :param source_arn: ``CfnUserPool.EmailConfigurationProperty.SourceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if configuration_set is not None:
                self._values["configuration_set"] = configuration_set
            if email_sending_account is not None:
                self._values["email_sending_account"] = email_sending_account
            if from_ is not None:
                self._values["from_"] = from_
            if reply_to_email_address is not None:
                self._values["reply_to_email_address"] = reply_to_email_address
            if source_arn is not None:
                self._values["source_arn"] = source_arn

        @builtins.property
        def configuration_set(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.EmailConfigurationProperty.ConfigurationSet``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-configurationset
            """
            result = self._values.get("configuration_set")
            return result

        @builtins.property
        def email_sending_account(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.EmailConfigurationProperty.EmailSendingAccount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-emailsendingaccount
            """
            result = self._values.get("email_sending_account")
            return result

        @builtins.property
        def from_(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.EmailConfigurationProperty.From``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-from
            """
            result = self._values.get("from_")
            return result

        @builtins.property
        def reply_to_email_address(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.EmailConfigurationProperty.ReplyToEmailAddress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-replytoemailaddress
            """
            result = self._values.get("reply_to_email_address")
            return result

        @builtins.property
        def source_arn(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.EmailConfigurationProperty.SourceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-emailconfiguration.html#cfn-cognito-userpool-emailconfiguration-sourcearn
            """
            result = self._values.get("source_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.InviteMessageTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_message": "emailMessage",
            "email_subject": "emailSubject",
            "sms_message": "smsMessage",
        },
    )
    class InviteMessageTemplateProperty:
        def __init__(
            self,
            *,
            email_message: typing.Optional[builtins.str] = None,
            email_subject: typing.Optional[builtins.str] = None,
            sms_message: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param email_message: ``CfnUserPool.InviteMessageTemplateProperty.EmailMessage``.
            :param email_subject: ``CfnUserPool.InviteMessageTemplateProperty.EmailSubject``.
            :param sms_message: ``CfnUserPool.InviteMessageTemplateProperty.SMSMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if email_message is not None:
                self._values["email_message"] = email_message
            if email_subject is not None:
                self._values["email_subject"] = email_subject
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def email_message(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.InviteMessageTemplateProperty.EmailMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-emailmessage
            """
            result = self._values.get("email_message")
            return result

        @builtins.property
        def email_subject(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.InviteMessageTemplateProperty.EmailSubject``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-emailsubject
            """
            result = self._values.get("email_subject")
            return result

        @builtins.property
        def sms_message(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.InviteMessageTemplateProperty.SMSMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-invitemessagetemplate.html#cfn-cognito-userpool-invitemessagetemplate-smsmessage
            """
            result = self._values.get("sms_message")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InviteMessageTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.LambdaConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "create_auth_challenge": "createAuthChallenge",
            "custom_message": "customMessage",
            "define_auth_challenge": "defineAuthChallenge",
            "post_authentication": "postAuthentication",
            "post_confirmation": "postConfirmation",
            "pre_authentication": "preAuthentication",
            "pre_sign_up": "preSignUp",
            "pre_token_generation": "preTokenGeneration",
            "user_migration": "userMigration",
            "verify_auth_challenge_response": "verifyAuthChallengeResponse",
        },
    )
    class LambdaConfigProperty:
        def __init__(
            self,
            *,
            create_auth_challenge: typing.Optional[builtins.str] = None,
            custom_message: typing.Optional[builtins.str] = None,
            define_auth_challenge: typing.Optional[builtins.str] = None,
            post_authentication: typing.Optional[builtins.str] = None,
            post_confirmation: typing.Optional[builtins.str] = None,
            pre_authentication: typing.Optional[builtins.str] = None,
            pre_sign_up: typing.Optional[builtins.str] = None,
            pre_token_generation: typing.Optional[builtins.str] = None,
            user_migration: typing.Optional[builtins.str] = None,
            verify_auth_challenge_response: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param create_auth_challenge: ``CfnUserPool.LambdaConfigProperty.CreateAuthChallenge``.
            :param custom_message: ``CfnUserPool.LambdaConfigProperty.CustomMessage``.
            :param define_auth_challenge: ``CfnUserPool.LambdaConfigProperty.DefineAuthChallenge``.
            :param post_authentication: ``CfnUserPool.LambdaConfigProperty.PostAuthentication``.
            :param post_confirmation: ``CfnUserPool.LambdaConfigProperty.PostConfirmation``.
            :param pre_authentication: ``CfnUserPool.LambdaConfigProperty.PreAuthentication``.
            :param pre_sign_up: ``CfnUserPool.LambdaConfigProperty.PreSignUp``.
            :param pre_token_generation: ``CfnUserPool.LambdaConfigProperty.PreTokenGeneration``.
            :param user_migration: ``CfnUserPool.LambdaConfigProperty.UserMigration``.
            :param verify_auth_challenge_response: ``CfnUserPool.LambdaConfigProperty.VerifyAuthChallengeResponse``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if create_auth_challenge is not None:
                self._values["create_auth_challenge"] = create_auth_challenge
            if custom_message is not None:
                self._values["custom_message"] = custom_message
            if define_auth_challenge is not None:
                self._values["define_auth_challenge"] = define_auth_challenge
            if post_authentication is not None:
                self._values["post_authentication"] = post_authentication
            if post_confirmation is not None:
                self._values["post_confirmation"] = post_confirmation
            if pre_authentication is not None:
                self._values["pre_authentication"] = pre_authentication
            if pre_sign_up is not None:
                self._values["pre_sign_up"] = pre_sign_up
            if pre_token_generation is not None:
                self._values["pre_token_generation"] = pre_token_generation
            if user_migration is not None:
                self._values["user_migration"] = user_migration
            if verify_auth_challenge_response is not None:
                self._values["verify_auth_challenge_response"] = verify_auth_challenge_response

        @builtins.property
        def create_auth_challenge(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.CreateAuthChallenge``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-createauthchallenge
            """
            result = self._values.get("create_auth_challenge")
            return result

        @builtins.property
        def custom_message(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.CustomMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-custommessage
            """
            result = self._values.get("custom_message")
            return result

        @builtins.property
        def define_auth_challenge(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.DefineAuthChallenge``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-defineauthchallenge
            """
            result = self._values.get("define_auth_challenge")
            return result

        @builtins.property
        def post_authentication(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.PostAuthentication``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-postauthentication
            """
            result = self._values.get("post_authentication")
            return result

        @builtins.property
        def post_confirmation(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.PostConfirmation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-postconfirmation
            """
            result = self._values.get("post_confirmation")
            return result

        @builtins.property
        def pre_authentication(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.PreAuthentication``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-preauthentication
            """
            result = self._values.get("pre_authentication")
            return result

        @builtins.property
        def pre_sign_up(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.PreSignUp``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-presignup
            """
            result = self._values.get("pre_sign_up")
            return result

        @builtins.property
        def pre_token_generation(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.PreTokenGeneration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-pretokengeneration
            """
            result = self._values.get("pre_token_generation")
            return result

        @builtins.property
        def user_migration(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.UserMigration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-usermigration
            """
            result = self._values.get("user_migration")
            return result

        @builtins.property
        def verify_auth_challenge_response(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.LambdaConfigProperty.VerifyAuthChallengeResponse``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-lambdaconfig.html#cfn-cognito-userpool-lambdaconfig-verifyauthchallengeresponse
            """
            result = self._values.get("verify_auth_challenge_response")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.NumberAttributeConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_value": "maxValue", "min_value": "minValue"},
    )
    class NumberAttributeConstraintsProperty:
        def __init__(
            self,
            *,
            max_value: typing.Optional[builtins.str] = None,
            min_value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param max_value: ``CfnUserPool.NumberAttributeConstraintsProperty.MaxValue``.
            :param min_value: ``CfnUserPool.NumberAttributeConstraintsProperty.MinValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value

        @builtins.property
        def max_value(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.NumberAttributeConstraintsProperty.MaxValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html#cfn-cognito-userpool-numberattributeconstraints-maxvalue
            """
            result = self._values.get("max_value")
            return result

        @builtins.property
        def min_value(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.NumberAttributeConstraintsProperty.MinValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-numberattributeconstraints.html#cfn-cognito-userpool-numberattributeconstraints-minvalue
            """
            result = self._values.get("min_value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NumberAttributeConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.PasswordPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "minimum_length": "minimumLength",
            "require_lowercase": "requireLowercase",
            "require_numbers": "requireNumbers",
            "require_symbols": "requireSymbols",
            "require_uppercase": "requireUppercase",
            "temporary_password_validity_days": "temporaryPasswordValidityDays",
        },
    )
    class PasswordPolicyProperty:
        def __init__(
            self,
            *,
            minimum_length: typing.Optional[jsii.Number] = None,
            require_lowercase: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            require_numbers: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            require_symbols: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            require_uppercase: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            temporary_password_validity_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param minimum_length: ``CfnUserPool.PasswordPolicyProperty.MinimumLength``.
            :param require_lowercase: ``CfnUserPool.PasswordPolicyProperty.RequireLowercase``.
            :param require_numbers: ``CfnUserPool.PasswordPolicyProperty.RequireNumbers``.
            :param require_symbols: ``CfnUserPool.PasswordPolicyProperty.RequireSymbols``.
            :param require_uppercase: ``CfnUserPool.PasswordPolicyProperty.RequireUppercase``.
            :param temporary_password_validity_days: ``CfnUserPool.PasswordPolicyProperty.TemporaryPasswordValidityDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if minimum_length is not None:
                self._values["minimum_length"] = minimum_length
            if require_lowercase is not None:
                self._values["require_lowercase"] = require_lowercase
            if require_numbers is not None:
                self._values["require_numbers"] = require_numbers
            if require_symbols is not None:
                self._values["require_symbols"] = require_symbols
            if require_uppercase is not None:
                self._values["require_uppercase"] = require_uppercase
            if temporary_password_validity_days is not None:
                self._values["temporary_password_validity_days"] = temporary_password_validity_days

        @builtins.property
        def minimum_length(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.PasswordPolicyProperty.MinimumLength``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-minimumlength
            """
            result = self._values.get("minimum_length")
            return result

        @builtins.property
        def require_lowercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireLowercase``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requirelowercase
            """
            result = self._values.get("require_lowercase")
            return result

        @builtins.property
        def require_numbers(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireNumbers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requirenumbers
            """
            result = self._values.get("require_numbers")
            return result

        @builtins.property
        def require_symbols(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireSymbols``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requiresymbols
            """
            result = self._values.get("require_symbols")
            return result

        @builtins.property
        def require_uppercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.PasswordPolicyProperty.RequireUppercase``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-requireuppercase
            """
            result = self._values.get("require_uppercase")
            return result

        @builtins.property
        def temporary_password_validity_days(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.PasswordPolicyProperty.TemporaryPasswordValidityDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-passwordpolicy.html#cfn-cognito-userpool-passwordpolicy-temporarypasswordvaliditydays
            """
            result = self._values.get("temporary_password_validity_days")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PasswordPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.PoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={"password_policy": "passwordPolicy"},
    )
    class PoliciesProperty:
        def __init__(
            self,
            *,
            password_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.PasswordPolicyProperty"]] = None,
        ) -> None:
            """
            :param password_policy: ``CfnUserPool.PoliciesProperty.PasswordPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-policies.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if password_policy is not None:
                self._values["password_policy"] = password_policy

        @builtins.property
        def password_policy(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.PasswordPolicyProperty"]]:
            """``CfnUserPool.PoliciesProperty.PasswordPolicy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-policies.html#cfn-cognito-userpool-policies-passwordpolicy
            """
            result = self._values.get("password_policy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.RecoveryOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "priority": "priority"},
    )
    class RecoveryOptionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param name: ``CfnUserPool.RecoveryOptionProperty.Name``.
            :param priority: ``CfnUserPool.RecoveryOptionProperty.Priority``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if priority is not None:
                self._values["priority"] = priority

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.RecoveryOptionProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html#cfn-cognito-userpool-recoveryoption-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            """``CfnUserPool.RecoveryOptionProperty.Priority``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-recoveryoption.html#cfn-cognito-userpool-recoveryoption-priority
            """
            result = self._values.get("priority")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecoveryOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.SchemaAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_data_type": "attributeDataType",
            "developer_only_attribute": "developerOnlyAttribute",
            "mutable": "mutable",
            "name": "name",
            "number_attribute_constraints": "numberAttributeConstraints",
            "required": "required",
            "string_attribute_constraints": "stringAttributeConstraints",
        },
    )
    class SchemaAttributeProperty:
        def __init__(
            self,
            *,
            attribute_data_type: typing.Optional[builtins.str] = None,
            developer_only_attribute: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            mutable: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            number_attribute_constraints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.NumberAttributeConstraintsProperty"]] = None,
            required: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            string_attribute_constraints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.StringAttributeConstraintsProperty"]] = None,
        ) -> None:
            """
            :param attribute_data_type: ``CfnUserPool.SchemaAttributeProperty.AttributeDataType``.
            :param developer_only_attribute: ``CfnUserPool.SchemaAttributeProperty.DeveloperOnlyAttribute``.
            :param mutable: ``CfnUserPool.SchemaAttributeProperty.Mutable``.
            :param name: ``CfnUserPool.SchemaAttributeProperty.Name``.
            :param number_attribute_constraints: ``CfnUserPool.SchemaAttributeProperty.NumberAttributeConstraints``.
            :param required: ``CfnUserPool.SchemaAttributeProperty.Required``.
            :param string_attribute_constraints: ``CfnUserPool.SchemaAttributeProperty.StringAttributeConstraints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attribute_data_type is not None:
                self._values["attribute_data_type"] = attribute_data_type
            if developer_only_attribute is not None:
                self._values["developer_only_attribute"] = developer_only_attribute
            if mutable is not None:
                self._values["mutable"] = mutable
            if name is not None:
                self._values["name"] = name
            if number_attribute_constraints is not None:
                self._values["number_attribute_constraints"] = number_attribute_constraints
            if required is not None:
                self._values["required"] = required
            if string_attribute_constraints is not None:
                self._values["string_attribute_constraints"] = string_attribute_constraints

        @builtins.property
        def attribute_data_type(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.SchemaAttributeProperty.AttributeDataType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-attributedatatype
            """
            result = self._values.get("attribute_data_type")
            return result

        @builtins.property
        def developer_only_attribute(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.SchemaAttributeProperty.DeveloperOnlyAttribute``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-developeronlyattribute
            """
            result = self._values.get("developer_only_attribute")
            return result

        @builtins.property
        def mutable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.SchemaAttributeProperty.Mutable``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-mutable
            """
            result = self._values.get("mutable")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.SchemaAttributeProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def number_attribute_constraints(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.NumberAttributeConstraintsProperty"]]:
            """``CfnUserPool.SchemaAttributeProperty.NumberAttributeConstraints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-numberattributeconstraints
            """
            result = self._values.get("number_attribute_constraints")
            return result

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.SchemaAttributeProperty.Required``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-required
            """
            result = self._values.get("required")
            return result

        @builtins.property
        def string_attribute_constraints(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPool.StringAttributeConstraintsProperty"]]:
            """``CfnUserPool.SchemaAttributeProperty.StringAttributeConstraints``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-schemaattribute.html#cfn-cognito-userpool-schemaattribute-stringattributeconstraints
            """
            result = self._values.get("string_attribute_constraints")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.SmsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"external_id": "externalId", "sns_caller_arn": "snsCallerArn"},
    )
    class SmsConfigurationProperty:
        def __init__(
            self,
            *,
            external_id: typing.Optional[builtins.str] = None,
            sns_caller_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param external_id: ``CfnUserPool.SmsConfigurationProperty.ExternalId``.
            :param sns_caller_arn: ``CfnUserPool.SmsConfigurationProperty.SnsCallerArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if external_id is not None:
                self._values["external_id"] = external_id
            if sns_caller_arn is not None:
                self._values["sns_caller_arn"] = sns_caller_arn

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.SmsConfigurationProperty.ExternalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html#cfn-cognito-userpool-smsconfiguration-externalid
            """
            result = self._values.get("external_id")
            return result

        @builtins.property
        def sns_caller_arn(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.SmsConfigurationProperty.SnsCallerArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-smsconfiguration.html#cfn-cognito-userpool-smsconfiguration-snscallerarn
            """
            result = self._values.get("sns_caller_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.StringAttributeConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_length": "maxLength", "min_length": "minLength"},
    )
    class StringAttributeConstraintsProperty:
        def __init__(
            self,
            *,
            max_length: typing.Optional[builtins.str] = None,
            min_length: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param max_length: ``CfnUserPool.StringAttributeConstraintsProperty.MaxLength``.
            :param min_length: ``CfnUserPool.StringAttributeConstraintsProperty.MinLength``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if max_length is not None:
                self._values["max_length"] = max_length
            if min_length is not None:
                self._values["min_length"] = min_length

        @builtins.property
        def max_length(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.StringAttributeConstraintsProperty.MaxLength``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html#cfn-cognito-userpool-stringattributeconstraints-maxlength
            """
            result = self._values.get("max_length")
            return result

        @builtins.property
        def min_length(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.StringAttributeConstraintsProperty.MinLength``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-stringattributeconstraints.html#cfn-cognito-userpool-stringattributeconstraints-minlength
            """
            result = self._values.get("min_length")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringAttributeConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.UserPoolAddOnsProperty",
        jsii_struct_bases=[],
        name_mapping={"advanced_security_mode": "advancedSecurityMode"},
    )
    class UserPoolAddOnsProperty:
        def __init__(
            self,
            *,
            advanced_security_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param advanced_security_mode: ``CfnUserPool.UserPoolAddOnsProperty.AdvancedSecurityMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userpooladdons.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if advanced_security_mode is not None:
                self._values["advanced_security_mode"] = advanced_security_mode

        @builtins.property
        def advanced_security_mode(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.UserPoolAddOnsProperty.AdvancedSecurityMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-userpooladdons.html#cfn-cognito-userpool-userpooladdons-advancedsecuritymode
            """
            result = self._values.get("advanced_security_mode")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPoolAddOnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.UsernameConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"case_sensitive": "caseSensitive"},
    )
    class UsernameConfigurationProperty:
        def __init__(
            self,
            *,
            case_sensitive: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param case_sensitive: ``CfnUserPool.UsernameConfigurationProperty.CaseSensitive``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-usernameconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPool.UsernameConfigurationProperty.CaseSensitive``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-usernameconfiguration.html#cfn-cognito-userpool-usernameconfiguration-casesensitive
            """
            result = self._values.get("case_sensitive")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UsernameConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPool.VerificationMessageTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_email_option": "defaultEmailOption",
            "email_message": "emailMessage",
            "email_message_by_link": "emailMessageByLink",
            "email_subject": "emailSubject",
            "email_subject_by_link": "emailSubjectByLink",
            "sms_message": "smsMessage",
        },
    )
    class VerificationMessageTemplateProperty:
        def __init__(
            self,
            *,
            default_email_option: typing.Optional[builtins.str] = None,
            email_message: typing.Optional[builtins.str] = None,
            email_message_by_link: typing.Optional[builtins.str] = None,
            email_subject: typing.Optional[builtins.str] = None,
            email_subject_by_link: typing.Optional[builtins.str] = None,
            sms_message: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param default_email_option: ``CfnUserPool.VerificationMessageTemplateProperty.DefaultEmailOption``.
            :param email_message: ``CfnUserPool.VerificationMessageTemplateProperty.EmailMessage``.
            :param email_message_by_link: ``CfnUserPool.VerificationMessageTemplateProperty.EmailMessageByLink``.
            :param email_subject: ``CfnUserPool.VerificationMessageTemplateProperty.EmailSubject``.
            :param email_subject_by_link: ``CfnUserPool.VerificationMessageTemplateProperty.EmailSubjectByLink``.
            :param sms_message: ``CfnUserPool.VerificationMessageTemplateProperty.SmsMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if default_email_option is not None:
                self._values["default_email_option"] = default_email_option
            if email_message is not None:
                self._values["email_message"] = email_message
            if email_message_by_link is not None:
                self._values["email_message_by_link"] = email_message_by_link
            if email_subject is not None:
                self._values["email_subject"] = email_subject
            if email_subject_by_link is not None:
                self._values["email_subject_by_link"] = email_subject_by_link
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def default_email_option(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.DefaultEmailOption``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-defaultemailoption
            """
            result = self._values.get("default_email_option")
            return result

        @builtins.property
        def email_message(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailmessage
            """
            result = self._values.get("email_message")
            return result

        @builtins.property
        def email_message_by_link(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailMessageByLink``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailmessagebylink
            """
            result = self._values.get("email_message_by_link")
            return result

        @builtins.property
        def email_subject(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailSubject``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailsubject
            """
            result = self._values.get("email_subject")
            return result

        @builtins.property
        def email_subject_by_link(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.EmailSubjectByLink``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-emailsubjectbylink
            """
            result = self._values.get("email_subject_by_link")
            return result

        @builtins.property
        def sms_message(self) -> typing.Optional[builtins.str]:
            """``CfnUserPool.VerificationMessageTemplateProperty.SmsMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpool-verificationmessagetemplate.html#cfn-cognito-userpool-verificationmessagetemplate-smsmessage
            """
            result = self._values.get("sms_message")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VerificationMessageTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolClient(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClient",
):
    """A CloudFormation ``AWS::Cognito::UserPoolClient``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
    :cloudformationResource: AWS::Cognito::UserPoolClient
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        user_pool_id: builtins.str,
        access_token_validity: typing.Optional[jsii.Number] = None,
        allowed_o_auth_flows: typing.Optional[typing.List[builtins.str]] = None,
        allowed_o_auth_flows_user_pool_client: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        allowed_o_auth_scopes: typing.Optional[typing.List[builtins.str]] = None,
        analytics_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolClient.AnalyticsConfigurationProperty"]] = None,
        callback_ur_ls: typing.Optional[typing.List[builtins.str]] = None,
        client_name: typing.Optional[builtins.str] = None,
        default_redirect_uri: typing.Optional[builtins.str] = None,
        explicit_auth_flows: typing.Optional[typing.List[builtins.str]] = None,
        generate_secret: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        id_token_validity: typing.Optional[jsii.Number] = None,
        logout_ur_ls: typing.Optional[typing.List[builtins.str]] = None,
        prevent_user_existence_errors: typing.Optional[builtins.str] = None,
        read_attributes: typing.Optional[typing.List[builtins.str]] = None,
        refresh_token_validity: typing.Optional[jsii.Number] = None,
        supported_identity_providers: typing.Optional[typing.List[builtins.str]] = None,
        token_validity_units: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolClient.TokenValidityUnitsProperty"]] = None,
        write_attributes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolClient``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_pool_id: ``AWS::Cognito::UserPoolClient.UserPoolId``.
        :param access_token_validity: ``AWS::Cognito::UserPoolClient.AccessTokenValidity``.
        :param allowed_o_auth_flows: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.
        :param allowed_o_auth_flows_user_pool_client: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.
        :param allowed_o_auth_scopes: ``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.
        :param analytics_configuration: ``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.
        :param callback_ur_ls: ``AWS::Cognito::UserPoolClient.CallbackURLs``.
        :param client_name: ``AWS::Cognito::UserPoolClient.ClientName``.
        :param default_redirect_uri: ``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.
        :param explicit_auth_flows: ``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.
        :param generate_secret: ``AWS::Cognito::UserPoolClient.GenerateSecret``.
        :param id_token_validity: ``AWS::Cognito::UserPoolClient.IdTokenValidity``.
        :param logout_ur_ls: ``AWS::Cognito::UserPoolClient.LogoutURLs``.
        :param prevent_user_existence_errors: ``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.
        :param read_attributes: ``AWS::Cognito::UserPoolClient.ReadAttributes``.
        :param refresh_token_validity: ``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.
        :param supported_identity_providers: ``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.
        :param token_validity_units: ``AWS::Cognito::UserPoolClient.TokenValidityUnits``.
        :param write_attributes: ``AWS::Cognito::UserPoolClient.WriteAttributes``.
        """
        props = CfnUserPoolClientProps(
            user_pool_id=user_pool_id,
            access_token_validity=access_token_validity,
            allowed_o_auth_flows=allowed_o_auth_flows,
            allowed_o_auth_flows_user_pool_client=allowed_o_auth_flows_user_pool_client,
            allowed_o_auth_scopes=allowed_o_auth_scopes,
            analytics_configuration=analytics_configuration,
            callback_ur_ls=callback_ur_ls,
            client_name=client_name,
            default_redirect_uri=default_redirect_uri,
            explicit_auth_flows=explicit_auth_flows,
            generate_secret=generate_secret,
            id_token_validity=id_token_validity,
            logout_ur_ls=logout_ur_ls,
            prevent_user_existence_errors=prevent_user_existence_errors,
            read_attributes=read_attributes,
            refresh_token_validity=refresh_token_validity,
            supported_identity_providers=supported_identity_providers,
            token_validity_units=token_validity_units,
            write_attributes=write_attributes,
        )

        jsii.create(CfnUserPoolClient, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrClientSecret")
    def attr_client_secret(self) -> builtins.str:
        """
        :cloudformationAttribute: ClientSecret
        """
        return jsii.get(self, "attrClientSecret")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolClient.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accessTokenValidity")
    def access_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.AccessTokenValidity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-accesstokenvalidity
        """
        return jsii.get(self, "accessTokenValidity")

    @access_token_validity.setter # type: ignore
    def access_token_validity(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "accessTokenValidity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowedOAuthFlows")
    def allowed_o_auth_flows(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflows
        """
        return jsii.get(self, "allowedOAuthFlows")

    @allowed_o_auth_flows.setter # type: ignore
    def allowed_o_auth_flows(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "allowedOAuthFlows", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowedOAuthFlowsUserPoolClient")
    def allowed_o_auth_flows_user_pool_client(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflowsuserpoolclient
        """
        return jsii.get(self, "allowedOAuthFlowsUserPoolClient")

    @allowed_o_auth_flows_user_pool_client.setter # type: ignore
    def allowed_o_auth_flows_user_pool_client(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "allowedOAuthFlowsUserPoolClient", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowedOAuthScopes")
    def allowed_o_auth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthscopes
        """
        return jsii.get(self, "allowedOAuthScopes")

    @allowed_o_auth_scopes.setter # type: ignore
    def allowed_o_auth_scopes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "allowedOAuthScopes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="analyticsConfiguration")
    def analytics_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolClient.AnalyticsConfigurationProperty"]]:
        """``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-analyticsconfiguration
        """
        return jsii.get(self, "analyticsConfiguration")

    @analytics_configuration.setter # type: ignore
    def analytics_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolClient.AnalyticsConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "analyticsConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="callbackUrLs")
    def callback_ur_ls(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.CallbackURLs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-callbackurls
        """
        return jsii.get(self, "callbackUrLs")

    @callback_ur_ls.setter # type: ignore
    def callback_ur_ls(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "callbackUrLs", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clientName")
    def client_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolClient.ClientName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-clientname
        """
        return jsii.get(self, "clientName")

    @client_name.setter # type: ignore
    def client_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultRedirectUri")
    def default_redirect_uri(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-defaultredirecturi
        """
        return jsii.get(self, "defaultRedirectUri")

    @default_redirect_uri.setter # type: ignore
    def default_redirect_uri(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultRedirectUri", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="explicitAuthFlows")
    def explicit_auth_flows(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-explicitauthflows
        """
        return jsii.get(self, "explicitAuthFlows")

    @explicit_auth_flows.setter # type: ignore
    def explicit_auth_flows(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "explicitAuthFlows", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="generateSecret")
    def generate_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::UserPoolClient.GenerateSecret``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-generatesecret
        """
        return jsii.get(self, "generateSecret")

    @generate_secret.setter # type: ignore
    def generate_secret(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "generateSecret", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="idTokenValidity")
    def id_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.IdTokenValidity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-idtokenvalidity
        """
        return jsii.get(self, "idTokenValidity")

    @id_token_validity.setter # type: ignore
    def id_token_validity(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "idTokenValidity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logoutUrLs")
    def logout_ur_ls(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.LogoutURLs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-logouturls
        """
        return jsii.get(self, "logoutUrLs")

    @logout_ur_ls.setter # type: ignore
    def logout_ur_ls(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "logoutUrLs", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preventUserExistenceErrors")
    def prevent_user_existence_errors(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-preventuserexistenceerrors
        """
        return jsii.get(self, "preventUserExistenceErrors")

    @prevent_user_existence_errors.setter # type: ignore
    def prevent_user_existence_errors(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preventUserExistenceErrors", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="readAttributes")
    def read_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.ReadAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-readattributes
        """
        return jsii.get(self, "readAttributes")

    @read_attributes.setter # type: ignore
    def read_attributes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "readAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="refreshTokenValidity")
    def refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-refreshtokenvalidity
        """
        return jsii.get(self, "refreshTokenValidity")

    @refresh_token_validity.setter # type: ignore
    def refresh_token_validity(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "refreshTokenValidity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="supportedIdentityProviders")
    def supported_identity_providers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-supportedidentityproviders
        """
        return jsii.get(self, "supportedIdentityProviders")

    @supported_identity_providers.setter # type: ignore
    def supported_identity_providers(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "supportedIdentityProviders", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenValidityUnits")
    def token_validity_units(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolClient.TokenValidityUnitsProperty"]]:
        """``AWS::Cognito::UserPoolClient.TokenValidityUnits``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-tokenvalidityunits
        """
        return jsii.get(self, "tokenValidityUnits")

    @token_validity_units.setter # type: ignore
    def token_validity_units(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolClient.TokenValidityUnitsProperty"]],
    ) -> None:
        jsii.set(self, "tokenValidityUnits", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="writeAttributes")
    def write_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.WriteAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-writeattributes
        """
        return jsii.get(self, "writeAttributes")

    @write_attributes.setter # type: ignore
    def write_attributes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "writeAttributes", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClient.AnalyticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_id": "applicationId",
            "external_id": "externalId",
            "role_arn": "roleArn",
            "user_data_shared": "userDataShared",
        },
    )
    class AnalyticsConfigurationProperty:
        def __init__(
            self,
            *,
            application_id: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            user_data_shared: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param application_id: ``CfnUserPoolClient.AnalyticsConfigurationProperty.ApplicationId``.
            :param external_id: ``CfnUserPoolClient.AnalyticsConfigurationProperty.ExternalId``.
            :param role_arn: ``CfnUserPoolClient.AnalyticsConfigurationProperty.RoleArn``.
            :param user_data_shared: ``CfnUserPoolClient.AnalyticsConfigurationProperty.UserDataShared``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if application_id is not None:
                self._values["application_id"] = application_id
            if external_id is not None:
                self._values["external_id"] = external_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if user_data_shared is not None:
                self._values["user_data_shared"] = user_data_shared

        @builtins.property
        def application_id(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.ApplicationId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-applicationid
            """
            result = self._values.get("application_id")
            return result

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.ExternalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-externalid
            """
            result = self._values.get("external_id")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def user_data_shared(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnUserPoolClient.AnalyticsConfigurationProperty.UserDataShared``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-analyticsconfiguration.html#cfn-cognito-userpoolclient-analyticsconfiguration-userdatashared
            """
            result = self._values.get("user_data_shared")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalyticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClient.TokenValidityUnitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "id_token": "idToken",
            "refresh_token": "refreshToken",
        },
    )
    class TokenValidityUnitsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            id_token: typing.Optional[builtins.str] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param access_token: ``CfnUserPoolClient.TokenValidityUnitsProperty.AccessToken``.
            :param id_token: ``CfnUserPoolClient.TokenValidityUnitsProperty.IdToken``.
            :param refresh_token: ``CfnUserPoolClient.TokenValidityUnitsProperty.RefreshToken``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if id_token is not None:
                self._values["id_token"] = id_token
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolClient.TokenValidityUnitsProperty.AccessToken``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html#cfn-cognito-userpoolclient-tokenvalidityunits-accesstoken
            """
            result = self._values.get("access_token")
            return result

        @builtins.property
        def id_token(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolClient.TokenValidityUnitsProperty.IdToken``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html#cfn-cognito-userpoolclient-tokenvalidityunits-idtoken
            """
            result = self._values.get("id_token")
            return result

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolClient.TokenValidityUnitsProperty.RefreshToken``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolclient-tokenvalidityunits.html#cfn-cognito-userpoolclient-tokenvalidityunits-refreshtoken
            """
            result = self._values.get("refresh_token")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TokenValidityUnitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolClientProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_id": "userPoolId",
        "access_token_validity": "accessTokenValidity",
        "allowed_o_auth_flows": "allowedOAuthFlows",
        "allowed_o_auth_flows_user_pool_client": "allowedOAuthFlowsUserPoolClient",
        "allowed_o_auth_scopes": "allowedOAuthScopes",
        "analytics_configuration": "analyticsConfiguration",
        "callback_ur_ls": "callbackUrLs",
        "client_name": "clientName",
        "default_redirect_uri": "defaultRedirectUri",
        "explicit_auth_flows": "explicitAuthFlows",
        "generate_secret": "generateSecret",
        "id_token_validity": "idTokenValidity",
        "logout_ur_ls": "logoutUrLs",
        "prevent_user_existence_errors": "preventUserExistenceErrors",
        "read_attributes": "readAttributes",
        "refresh_token_validity": "refreshTokenValidity",
        "supported_identity_providers": "supportedIdentityProviders",
        "token_validity_units": "tokenValidityUnits",
        "write_attributes": "writeAttributes",
    },
)
class CfnUserPoolClientProps:
    def __init__(
        self,
        *,
        user_pool_id: builtins.str,
        access_token_validity: typing.Optional[jsii.Number] = None,
        allowed_o_auth_flows: typing.Optional[typing.List[builtins.str]] = None,
        allowed_o_auth_flows_user_pool_client: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        allowed_o_auth_scopes: typing.Optional[typing.List[builtins.str]] = None,
        analytics_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolClient.AnalyticsConfigurationProperty]] = None,
        callback_ur_ls: typing.Optional[typing.List[builtins.str]] = None,
        client_name: typing.Optional[builtins.str] = None,
        default_redirect_uri: typing.Optional[builtins.str] = None,
        explicit_auth_flows: typing.Optional[typing.List[builtins.str]] = None,
        generate_secret: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        id_token_validity: typing.Optional[jsii.Number] = None,
        logout_ur_ls: typing.Optional[typing.List[builtins.str]] = None,
        prevent_user_existence_errors: typing.Optional[builtins.str] = None,
        read_attributes: typing.Optional[typing.List[builtins.str]] = None,
        refresh_token_validity: typing.Optional[jsii.Number] = None,
        supported_identity_providers: typing.Optional[typing.List[builtins.str]] = None,
        token_validity_units: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolClient.TokenValidityUnitsProperty]] = None,
        write_attributes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolClient``.

        :param user_pool_id: ``AWS::Cognito::UserPoolClient.UserPoolId``.
        :param access_token_validity: ``AWS::Cognito::UserPoolClient.AccessTokenValidity``.
        :param allowed_o_auth_flows: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.
        :param allowed_o_auth_flows_user_pool_client: ``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.
        :param allowed_o_auth_scopes: ``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.
        :param analytics_configuration: ``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.
        :param callback_ur_ls: ``AWS::Cognito::UserPoolClient.CallbackURLs``.
        :param client_name: ``AWS::Cognito::UserPoolClient.ClientName``.
        :param default_redirect_uri: ``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.
        :param explicit_auth_flows: ``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.
        :param generate_secret: ``AWS::Cognito::UserPoolClient.GenerateSecret``.
        :param id_token_validity: ``AWS::Cognito::UserPoolClient.IdTokenValidity``.
        :param logout_ur_ls: ``AWS::Cognito::UserPoolClient.LogoutURLs``.
        :param prevent_user_existence_errors: ``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.
        :param read_attributes: ``AWS::Cognito::UserPoolClient.ReadAttributes``.
        :param refresh_token_validity: ``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.
        :param supported_identity_providers: ``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.
        :param token_validity_units: ``AWS::Cognito::UserPoolClient.TokenValidityUnits``.
        :param write_attributes: ``AWS::Cognito::UserPoolClient.WriteAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool_id": user_pool_id,
        }
        if access_token_validity is not None:
            self._values["access_token_validity"] = access_token_validity
        if allowed_o_auth_flows is not None:
            self._values["allowed_o_auth_flows"] = allowed_o_auth_flows
        if allowed_o_auth_flows_user_pool_client is not None:
            self._values["allowed_o_auth_flows_user_pool_client"] = allowed_o_auth_flows_user_pool_client
        if allowed_o_auth_scopes is not None:
            self._values["allowed_o_auth_scopes"] = allowed_o_auth_scopes
        if analytics_configuration is not None:
            self._values["analytics_configuration"] = analytics_configuration
        if callback_ur_ls is not None:
            self._values["callback_ur_ls"] = callback_ur_ls
        if client_name is not None:
            self._values["client_name"] = client_name
        if default_redirect_uri is not None:
            self._values["default_redirect_uri"] = default_redirect_uri
        if explicit_auth_flows is not None:
            self._values["explicit_auth_flows"] = explicit_auth_flows
        if generate_secret is not None:
            self._values["generate_secret"] = generate_secret
        if id_token_validity is not None:
            self._values["id_token_validity"] = id_token_validity
        if logout_ur_ls is not None:
            self._values["logout_ur_ls"] = logout_ur_ls
        if prevent_user_existence_errors is not None:
            self._values["prevent_user_existence_errors"] = prevent_user_existence_errors
        if read_attributes is not None:
            self._values["read_attributes"] = read_attributes
        if refresh_token_validity is not None:
            self._values["refresh_token_validity"] = refresh_token_validity
        if supported_identity_providers is not None:
            self._values["supported_identity_providers"] = supported_identity_providers
        if token_validity_units is not None:
            self._values["token_validity_units"] = token_validity_units
        if write_attributes is not None:
            self._values["write_attributes"] = write_attributes

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolClient.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def access_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.AccessTokenValidity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-accesstokenvalidity
        """
        result = self._values.get("access_token_validity")
        return result

    @builtins.property
    def allowed_o_auth_flows(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlows``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflows
        """
        result = self._values.get("allowed_o_auth_flows")
        return result

    @builtins.property
    def allowed_o_auth_flows_user_pool_client(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthFlowsUserPoolClient``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthflowsuserpoolclient
        """
        result = self._values.get("allowed_o_auth_flows_user_pool_client")
        return result

    @builtins.property
    def allowed_o_auth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.AllowedOAuthScopes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthscopes
        """
        result = self._values.get("allowed_o_auth_scopes")
        return result

    @builtins.property
    def analytics_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolClient.AnalyticsConfigurationProperty]]:
        """``AWS::Cognito::UserPoolClient.AnalyticsConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-analyticsconfiguration
        """
        result = self._values.get("analytics_configuration")
        return result

    @builtins.property
    def callback_ur_ls(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.CallbackURLs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-callbackurls
        """
        result = self._values.get("callback_ur_ls")
        return result

    @builtins.property
    def client_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolClient.ClientName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-clientname
        """
        result = self._values.get("client_name")
        return result

    @builtins.property
    def default_redirect_uri(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolClient.DefaultRedirectURI``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-defaultredirecturi
        """
        result = self._values.get("default_redirect_uri")
        return result

    @builtins.property
    def explicit_auth_flows(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.ExplicitAuthFlows``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-explicitauthflows
        """
        result = self._values.get("explicit_auth_flows")
        return result

    @builtins.property
    def generate_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::UserPoolClient.GenerateSecret``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-generatesecret
        """
        result = self._values.get("generate_secret")
        return result

    @builtins.property
    def id_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.IdTokenValidity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-idtokenvalidity
        """
        result = self._values.get("id_token_validity")
        return result

    @builtins.property
    def logout_ur_ls(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.LogoutURLs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-logouturls
        """
        result = self._values.get("logout_ur_ls")
        return result

    @builtins.property
    def prevent_user_existence_errors(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolClient.PreventUserExistenceErrors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-preventuserexistenceerrors
        """
        result = self._values.get("prevent_user_existence_errors")
        return result

    @builtins.property
    def read_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.ReadAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-readattributes
        """
        result = self._values.get("read_attributes")
        return result

    @builtins.property
    def refresh_token_validity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolClient.RefreshTokenValidity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-refreshtokenvalidity
        """
        result = self._values.get("refresh_token_validity")
        return result

    @builtins.property
    def supported_identity_providers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.SupportedIdentityProviders``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-supportedidentityproviders
        """
        result = self._values.get("supported_identity_providers")
        return result

    @builtins.property
    def token_validity_units(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolClient.TokenValidityUnitsProperty]]:
        """``AWS::Cognito::UserPoolClient.TokenValidityUnits``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-tokenvalidityunits
        """
        result = self._values.get("token_validity_units")
        return result

    @builtins.property
    def write_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolClient.WriteAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-writeattributes
        """
        result = self._values.get("write_attributes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolClientProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolDomain(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolDomain",
):
    """A CloudFormation ``AWS::Cognito::UserPoolDomain``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html
    :cloudformationResource: AWS::Cognito::UserPoolDomain
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        domain: builtins.str,
        user_pool_id: builtins.str,
        custom_domain_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolDomain.CustomDomainConfigTypeProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolDomain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain: ``AWS::Cognito::UserPoolDomain.Domain``.
        :param user_pool_id: ``AWS::Cognito::UserPoolDomain.UserPoolId``.
        :param custom_domain_config: ``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.
        """
        props = CfnUserPoolDomainProps(
            domain=domain,
            user_pool_id=user_pool_id,
            custom_domain_config=custom_domain_config,
        )

        jsii.create(CfnUserPoolDomain, self, [scope, id, props])

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
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        """``AWS::Cognito::UserPoolDomain.Domain``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-domain
        """
        return jsii.get(self, "domain")

    @domain.setter # type: ignore
    def domain(self, value: builtins.str) -> None:
        jsii.set(self, "domain", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolDomain.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customDomainConfig")
    def custom_domain_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolDomain.CustomDomainConfigTypeProperty"]]:
        """``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-customdomainconfig
        """
        return jsii.get(self, "customDomainConfig")

    @custom_domain_config.setter # type: ignore
    def custom_domain_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolDomain.CustomDomainConfigTypeProperty"]],
    ) -> None:
        jsii.set(self, "customDomainConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolDomain.CustomDomainConfigTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CustomDomainConfigTypeProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param certificate_arn: ``CfnUserPoolDomain.CustomDomainConfigTypeProperty.CertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooldomain-customdomainconfigtype.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolDomain.CustomDomainConfigTypeProperty.CertificateArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooldomain-customdomainconfigtype.html#cfn-cognito-userpooldomain-customdomainconfigtype-certificatearn
            """
            result = self._values.get("certificate_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDomainConfigTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "user_pool_id": "userPoolId",
        "custom_domain_config": "customDomainConfig",
    },
)
class CfnUserPoolDomainProps:
    def __init__(
        self,
        *,
        domain: builtins.str,
        user_pool_id: builtins.str,
        custom_domain_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolDomain.CustomDomainConfigTypeProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolDomain``.

        :param domain: ``AWS::Cognito::UserPoolDomain.Domain``.
        :param user_pool_id: ``AWS::Cognito::UserPoolDomain.UserPoolId``.
        :param custom_domain_config: ``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain": domain,
            "user_pool_id": user_pool_id,
        }
        if custom_domain_config is not None:
            self._values["custom_domain_config"] = custom_domain_config

    @builtins.property
    def domain(self) -> builtins.str:
        """``AWS::Cognito::UserPoolDomain.Domain``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-domain
        """
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return result

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolDomain.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def custom_domain_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolDomain.CustomDomainConfigTypeProperty]]:
        """``AWS::Cognito::UserPoolDomain.CustomDomainConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html#cfn-cognito-userpooldomain-customdomainconfig
        """
        result = self._values.get("custom_domain_config")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolGroup",
):
    """A CloudFormation ``AWS::Cognito::UserPoolGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html
    :cloudformationResource: AWS::Cognito::UserPoolGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        user_pool_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        precedence: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_pool_id: ``AWS::Cognito::UserPoolGroup.UserPoolId``.
        :param description: ``AWS::Cognito::UserPoolGroup.Description``.
        :param group_name: ``AWS::Cognito::UserPoolGroup.GroupName``.
        :param precedence: ``AWS::Cognito::UserPoolGroup.Precedence``.
        :param role_arn: ``AWS::Cognito::UserPoolGroup.RoleArn``.
        """
        props = CfnUserPoolGroupProps(
            user_pool_id=user_pool_id,
            description=description,
            group_name=group_name,
            precedence=precedence,
            role_arn=role_arn,
        )

        jsii.create(CfnUserPoolGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolGroup.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolGroup.GroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-groupname
        """
        return jsii.get(self, "groupName")

    @group_name.setter # type: ignore
    def group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "groupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolGroup.Precedence``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-precedence
        """
        return jsii.get(self, "precedence")

    @precedence.setter # type: ignore
    def precedence(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "precedence", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolGroup.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_id": "userPoolId",
        "description": "description",
        "group_name": "groupName",
        "precedence": "precedence",
        "role_arn": "roleArn",
    },
)
class CfnUserPoolGroupProps:
    def __init__(
        self,
        *,
        user_pool_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        precedence: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolGroup``.

        :param user_pool_id: ``AWS::Cognito::UserPoolGroup.UserPoolId``.
        :param description: ``AWS::Cognito::UserPoolGroup.Description``.
        :param group_name: ``AWS::Cognito::UserPoolGroup.GroupName``.
        :param precedence: ``AWS::Cognito::UserPoolGroup.Precedence``.
        :param role_arn: ``AWS::Cognito::UserPoolGroup.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool_id": user_pool_id,
        }
        if description is not None:
            self._values["description"] = description
        if group_name is not None:
            self._values["group_name"] = group_name
        if precedence is not None:
            self._values["precedence"] = precedence
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolGroup.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolGroup.GroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-groupname
        """
        result = self._values.get("group_name")
        return result

    @builtins.property
    def precedence(self) -> typing.Optional[jsii.Number]:
        """``AWS::Cognito::UserPoolGroup.Precedence``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-precedence
        """
        result = self._values.get("precedence")
        return result

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolGroup.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html#cfn-cognito-userpoolgroup-rolearn
        """
        result = self._values.get("role_arn")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolIdentityProvider(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolIdentityProvider",
):
    """A CloudFormation ``AWS::Cognito::UserPoolIdentityProvider``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html
    :cloudformationResource: AWS::Cognito::UserPoolIdentityProvider
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        provider_name: builtins.str,
        provider_type: builtins.str,
        user_pool_id: builtins.str,
        attribute_mapping: typing.Any = None,
        idp_identifiers: typing.Optional[typing.List[builtins.str]] = None,
        provider_details: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolIdentityProvider``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param provider_name: ``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.
        :param provider_type: ``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.
        :param user_pool_id: ``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.
        :param attribute_mapping: ``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.
        :param idp_identifiers: ``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.
        :param provider_details: ``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.
        """
        props = CfnUserPoolIdentityProviderProps(
            provider_name=provider_name,
            provider_type=provider_type,
            user_pool_id=user_pool_id,
            attribute_mapping=attribute_mapping,
            idp_identifiers=idp_identifiers,
            provider_details=provider_details,
        )

        jsii.create(CfnUserPoolIdentityProvider, self, [scope, id, props])

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
    @jsii.member(jsii_name="attributeMapping")
    def attribute_mapping(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-attributemapping
        """
        return jsii.get(self, "attributeMapping")

    @attribute_mapping.setter # type: ignore
    def attribute_mapping(self, value: typing.Any) -> None:
        jsii.set(self, "attributeMapping", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerDetails")
    def provider_details(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providerdetails
        """
        return jsii.get(self, "providerDetails")

    @provider_details.setter # type: ignore
    def provider_details(self, value: typing.Any) -> None:
        jsii.set(self, "providerDetails", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providername
        """
        return jsii.get(self, "providerName")

    @provider_name.setter # type: ignore
    def provider_name(self, value: builtins.str) -> None:
        jsii.set(self, "providerName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> builtins.str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providertype
        """
        return jsii.get(self, "providerType")

    @provider_type.setter # type: ignore
    def provider_type(self, value: builtins.str) -> None:
        jsii.set(self, "providerType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="idpIdentifiers")
    def idp_identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-idpidentifiers
        """
        return jsii.get(self, "idpIdentifiers")

    @idp_identifiers.setter # type: ignore
    def idp_identifiers(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "idpIdentifiers", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolIdentityProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider_name": "providerName",
        "provider_type": "providerType",
        "user_pool_id": "userPoolId",
        "attribute_mapping": "attributeMapping",
        "idp_identifiers": "idpIdentifiers",
        "provider_details": "providerDetails",
    },
)
class CfnUserPoolIdentityProviderProps:
    def __init__(
        self,
        *,
        provider_name: builtins.str,
        provider_type: builtins.str,
        user_pool_id: builtins.str,
        attribute_mapping: typing.Any = None,
        idp_identifiers: typing.Optional[typing.List[builtins.str]] = None,
        provider_details: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolIdentityProvider``.

        :param provider_name: ``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.
        :param provider_type: ``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.
        :param user_pool_id: ``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.
        :param attribute_mapping: ``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.
        :param idp_identifiers: ``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.
        :param provider_details: ``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "provider_name": provider_name,
            "provider_type": provider_type,
            "user_pool_id": user_pool_id,
        }
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping
        if idp_identifiers is not None:
            self._values["idp_identifiers"] = idp_identifiers
        if provider_details is not None:
            self._values["provider_details"] = provider_details

    @builtins.property
    def provider_name(self) -> builtins.str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providername
        """
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return result

    @builtins.property
    def provider_type(self) -> builtins.str:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providertype
        """
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return result

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolIdentityProvider.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def attribute_mapping(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.AttributeMapping``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-attributemapping
        """
        result = self._values.get("attribute_mapping")
        return result

    @builtins.property
    def idp_identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolIdentityProvider.IdpIdentifiers``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-idpidentifiers
        """
        result = self._values.get("idp_identifiers")
        return result

    @builtins.property
    def provider_details(self) -> typing.Any:
        """``AWS::Cognito::UserPoolIdentityProvider.ProviderDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html#cfn-cognito-userpoolidentityprovider-providerdetails
        """
        result = self._values.get("provider_details")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolIdentityProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_recovery_setting": "accountRecoverySetting",
        "admin_create_user_config": "adminCreateUserConfig",
        "alias_attributes": "aliasAttributes",
        "auto_verified_attributes": "autoVerifiedAttributes",
        "device_configuration": "deviceConfiguration",
        "email_configuration": "emailConfiguration",
        "email_verification_message": "emailVerificationMessage",
        "email_verification_subject": "emailVerificationSubject",
        "enabled_mfas": "enabledMfas",
        "lambda_config": "lambdaConfig",
        "mfa_configuration": "mfaConfiguration",
        "policies": "policies",
        "schema": "schema",
        "sms_authentication_message": "smsAuthenticationMessage",
        "sms_configuration": "smsConfiguration",
        "sms_verification_message": "smsVerificationMessage",
        "username_attributes": "usernameAttributes",
        "username_configuration": "usernameConfiguration",
        "user_pool_add_ons": "userPoolAddOns",
        "user_pool_name": "userPoolName",
        "user_pool_tags": "userPoolTags",
        "verification_message_template": "verificationMessageTemplate",
    },
)
class CfnUserPoolProps:
    def __init__(
        self,
        *,
        account_recovery_setting: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.AccountRecoverySettingProperty]] = None,
        admin_create_user_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.AdminCreateUserConfigProperty]] = None,
        alias_attributes: typing.Optional[typing.List[builtins.str]] = None,
        auto_verified_attributes: typing.Optional[typing.List[builtins.str]] = None,
        device_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.DeviceConfigurationProperty]] = None,
        email_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.EmailConfigurationProperty]] = None,
        email_verification_message: typing.Optional[builtins.str] = None,
        email_verification_subject: typing.Optional[builtins.str] = None,
        enabled_mfas: typing.Optional[typing.List[builtins.str]] = None,
        lambda_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.LambdaConfigProperty]] = None,
        mfa_configuration: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.PoliciesProperty]] = None,
        schema: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.SchemaAttributeProperty]]]] = None,
        sms_authentication_message: typing.Optional[builtins.str] = None,
        sms_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.SmsConfigurationProperty]] = None,
        sms_verification_message: typing.Optional[builtins.str] = None,
        username_attributes: typing.Optional[typing.List[builtins.str]] = None,
        username_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.UsernameConfigurationProperty]] = None,
        user_pool_add_ons: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.UserPoolAddOnsProperty]] = None,
        user_pool_name: typing.Optional[builtins.str] = None,
        user_pool_tags: typing.Any = None,
        verification_message_template: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.VerificationMessageTemplateProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPool``.

        :param account_recovery_setting: ``AWS::Cognito::UserPool.AccountRecoverySetting``.
        :param admin_create_user_config: ``AWS::Cognito::UserPool.AdminCreateUserConfig``.
        :param alias_attributes: ``AWS::Cognito::UserPool.AliasAttributes``.
        :param auto_verified_attributes: ``AWS::Cognito::UserPool.AutoVerifiedAttributes``.
        :param device_configuration: ``AWS::Cognito::UserPool.DeviceConfiguration``.
        :param email_configuration: ``AWS::Cognito::UserPool.EmailConfiguration``.
        :param email_verification_message: ``AWS::Cognito::UserPool.EmailVerificationMessage``.
        :param email_verification_subject: ``AWS::Cognito::UserPool.EmailVerificationSubject``.
        :param enabled_mfas: ``AWS::Cognito::UserPool.EnabledMfas``.
        :param lambda_config: ``AWS::Cognito::UserPool.LambdaConfig``.
        :param mfa_configuration: ``AWS::Cognito::UserPool.MfaConfiguration``.
        :param policies: ``AWS::Cognito::UserPool.Policies``.
        :param schema: ``AWS::Cognito::UserPool.Schema``.
        :param sms_authentication_message: ``AWS::Cognito::UserPool.SmsAuthenticationMessage``.
        :param sms_configuration: ``AWS::Cognito::UserPool.SmsConfiguration``.
        :param sms_verification_message: ``AWS::Cognito::UserPool.SmsVerificationMessage``.
        :param username_attributes: ``AWS::Cognito::UserPool.UsernameAttributes``.
        :param username_configuration: ``AWS::Cognito::UserPool.UsernameConfiguration``.
        :param user_pool_add_ons: ``AWS::Cognito::UserPool.UserPoolAddOns``.
        :param user_pool_name: ``AWS::Cognito::UserPool.UserPoolName``.
        :param user_pool_tags: ``AWS::Cognito::UserPool.UserPoolTags``.
        :param verification_message_template: ``AWS::Cognito::UserPool.VerificationMessageTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if account_recovery_setting is not None:
            self._values["account_recovery_setting"] = account_recovery_setting
        if admin_create_user_config is not None:
            self._values["admin_create_user_config"] = admin_create_user_config
        if alias_attributes is not None:
            self._values["alias_attributes"] = alias_attributes
        if auto_verified_attributes is not None:
            self._values["auto_verified_attributes"] = auto_verified_attributes
        if device_configuration is not None:
            self._values["device_configuration"] = device_configuration
        if email_configuration is not None:
            self._values["email_configuration"] = email_configuration
        if email_verification_message is not None:
            self._values["email_verification_message"] = email_verification_message
        if email_verification_subject is not None:
            self._values["email_verification_subject"] = email_verification_subject
        if enabled_mfas is not None:
            self._values["enabled_mfas"] = enabled_mfas
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config
        if mfa_configuration is not None:
            self._values["mfa_configuration"] = mfa_configuration
        if policies is not None:
            self._values["policies"] = policies
        if schema is not None:
            self._values["schema"] = schema
        if sms_authentication_message is not None:
            self._values["sms_authentication_message"] = sms_authentication_message
        if sms_configuration is not None:
            self._values["sms_configuration"] = sms_configuration
        if sms_verification_message is not None:
            self._values["sms_verification_message"] = sms_verification_message
        if username_attributes is not None:
            self._values["username_attributes"] = username_attributes
        if username_configuration is not None:
            self._values["username_configuration"] = username_configuration
        if user_pool_add_ons is not None:
            self._values["user_pool_add_ons"] = user_pool_add_ons
        if user_pool_name is not None:
            self._values["user_pool_name"] = user_pool_name
        if user_pool_tags is not None:
            self._values["user_pool_tags"] = user_pool_tags
        if verification_message_template is not None:
            self._values["verification_message_template"] = verification_message_template

    @builtins.property
    def account_recovery_setting(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.AccountRecoverySettingProperty]]:
        """``AWS::Cognito::UserPool.AccountRecoverySetting``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-accountrecoverysetting
        """
        result = self._values.get("account_recovery_setting")
        return result

    @builtins.property
    def admin_create_user_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.AdminCreateUserConfigProperty]]:
        """``AWS::Cognito::UserPool.AdminCreateUserConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-admincreateuserconfig
        """
        result = self._values.get("admin_create_user_config")
        return result

    @builtins.property
    def alias_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.AliasAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-aliasattributes
        """
        result = self._values.get("alias_attributes")
        return result

    @builtins.property
    def auto_verified_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.AutoVerifiedAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-autoverifiedattributes
        """
        result = self._values.get("auto_verified_attributes")
        return result

    @builtins.property
    def device_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.DeviceConfigurationProperty]]:
        """``AWS::Cognito::UserPool.DeviceConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-deviceconfiguration
        """
        result = self._values.get("device_configuration")
        return result

    @builtins.property
    def email_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.EmailConfigurationProperty]]:
        """``AWS::Cognito::UserPool.EmailConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailconfiguration
        """
        result = self._values.get("email_configuration")
        return result

    @builtins.property
    def email_verification_message(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.EmailVerificationMessage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationmessage
        """
        result = self._values.get("email_verification_message")
        return result

    @builtins.property
    def email_verification_subject(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.EmailVerificationSubject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-emailverificationsubject
        """
        result = self._values.get("email_verification_subject")
        return result

    @builtins.property
    def enabled_mfas(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.EnabledMfas``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-enabledmfas
        """
        result = self._values.get("enabled_mfas")
        return result

    @builtins.property
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.LambdaConfigProperty]]:
        """``AWS::Cognito::UserPool.LambdaConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-lambdaconfig
        """
        result = self._values.get("lambda_config")
        return result

    @builtins.property
    def mfa_configuration(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.MfaConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-mfaconfiguration
        """
        result = self._values.get("mfa_configuration")
        return result

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.PoliciesProperty]]:
        """``AWS::Cognito::UserPool.Policies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-policies
        """
        result = self._values.get("policies")
        return result

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.SchemaAttributeProperty]]]]:
        """``AWS::Cognito::UserPool.Schema``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-schema
        """
        result = self._values.get("schema")
        return result

    @builtins.property
    def sms_authentication_message(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.SmsAuthenticationMessage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsauthenticationmessage
        """
        result = self._values.get("sms_authentication_message")
        return result

    @builtins.property
    def sms_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.SmsConfigurationProperty]]:
        """``AWS::Cognito::UserPool.SmsConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsconfiguration
        """
        result = self._values.get("sms_configuration")
        return result

    @builtins.property
    def sms_verification_message(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.SmsVerificationMessage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-smsverificationmessage
        """
        result = self._values.get("sms_verification_message")
        return result

    @builtins.property
    def username_attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPool.UsernameAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameattributes
        """
        result = self._values.get("username_attributes")
        return result

    @builtins.property
    def username_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.UsernameConfigurationProperty]]:
        """``AWS::Cognito::UserPool.UsernameConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-usernameconfiguration
        """
        result = self._values.get("username_configuration")
        return result

    @builtins.property
    def user_pool_add_ons(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.UserPoolAddOnsProperty]]:
        """``AWS::Cognito::UserPool.UserPoolAddOns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooladdons
        """
        result = self._values.get("user_pool_add_ons")
        return result

    @builtins.property
    def user_pool_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPool.UserPoolName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpoolname
        """
        result = self._values.get("user_pool_name")
        return result

    @builtins.property
    def user_pool_tags(self) -> typing.Any:
        """``AWS::Cognito::UserPool.UserPoolTags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-userpooltags
        """
        result = self._values.get("user_pool_tags")
        return result

    @builtins.property
    def verification_message_template(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPool.VerificationMessageTemplateProperty]]:
        """``AWS::Cognito::UserPool.VerificationMessageTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html#cfn-cognito-userpool-verificationmessagetemplate
        """
        result = self._values.get("verification_message_template")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolResourceServer(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolResourceServer",
):
    """A CloudFormation ``AWS::Cognito::UserPoolResourceServer``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html
    :cloudformationResource: AWS::Cognito::UserPoolResourceServer
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        identifier: builtins.str,
        name: builtins.str,
        user_pool_id: builtins.str,
        scopes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolResourceServer.ResourceServerScopeTypeProperty"]]]] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolResourceServer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param identifier: ``AWS::Cognito::UserPoolResourceServer.Identifier``.
        :param name: ``AWS::Cognito::UserPoolResourceServer.Name``.
        :param user_pool_id: ``AWS::Cognito::UserPoolResourceServer.UserPoolId``.
        :param scopes: ``AWS::Cognito::UserPoolResourceServer.Scopes``.
        """
        props = CfnUserPoolResourceServerProps(
            identifier=identifier, name=name, user_pool_id=user_pool_id, scopes=scopes
        )

        jsii.create(CfnUserPoolResourceServer, self, [scope, id, props])

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
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        """``AWS::Cognito::UserPoolResourceServer.Identifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-identifier
        """
        return jsii.get(self, "identifier")

    @identifier.setter # type: ignore
    def identifier(self, value: builtins.str) -> None:
        jsii.set(self, "identifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::Cognito::UserPoolResourceServer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolResourceServer.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scopes")
    def scopes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolResourceServer.ResourceServerScopeTypeProperty"]]]]:
        """``AWS::Cognito::UserPoolResourceServer.Scopes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-scopes
        """
        return jsii.get(self, "scopes")

    @scopes.setter # type: ignore
    def scopes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolResourceServer.ResourceServerScopeTypeProperty"]]]],
    ) -> None:
        jsii.set(self, "scopes", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolResourceServer.ResourceServerScopeTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "scope_description": "scopeDescription",
            "scope_name": "scopeName",
        },
    )
    class ResourceServerScopeTypeProperty:
        def __init__(
            self,
            *,
            scope_description: builtins.str,
            scope_name: builtins.str,
        ) -> None:
            """
            :param scope_description: ``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeDescription``.
            :param scope_name: ``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "scope_description": scope_description,
                "scope_name": scope_name,
            }

        @builtins.property
        def scope_description(self) -> builtins.str:
            """``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeDescription``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html#cfn-cognito-userpoolresourceserver-resourceserverscopetype-scopedescription
            """
            result = self._values.get("scope_description")
            assert result is not None, "Required property 'scope_description' is missing"
            return result

        @builtins.property
        def scope_name(self) -> builtins.str:
            """``CfnUserPoolResourceServer.ResourceServerScopeTypeProperty.ScopeName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolresourceserver-resourceserverscopetype.html#cfn-cognito-userpoolresourceserver-resourceserverscopetype-scopename
            """
            result = self._values.get("scope_name")
            assert result is not None, "Required property 'scope_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceServerScopeTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolResourceServerProps",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "name": "name",
        "user_pool_id": "userPoolId",
        "scopes": "scopes",
    },
)
class CfnUserPoolResourceServerProps:
    def __init__(
        self,
        *,
        identifier: builtins.str,
        name: builtins.str,
        user_pool_id: builtins.str,
        scopes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolResourceServer.ResourceServerScopeTypeProperty]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolResourceServer``.

        :param identifier: ``AWS::Cognito::UserPoolResourceServer.Identifier``.
        :param name: ``AWS::Cognito::UserPoolResourceServer.Name``.
        :param user_pool_id: ``AWS::Cognito::UserPoolResourceServer.UserPoolId``.
        :param scopes: ``AWS::Cognito::UserPoolResourceServer.Scopes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "identifier": identifier,
            "name": name,
            "user_pool_id": user_pool_id,
        }
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def identifier(self) -> builtins.str:
        """``AWS::Cognito::UserPoolResourceServer.Identifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-identifier
        """
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::Cognito::UserPoolResourceServer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolResourceServer.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def scopes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolResourceServer.ResourceServerScopeTypeProperty]]]]:
        """``AWS::Cognito::UserPoolResourceServer.Scopes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html#cfn-cognito-userpoolresourceserver-scopes
        """
        result = self._values.get("scopes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolResourceServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolRiskConfigurationAttachment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment",
):
    """A CloudFormation ``AWS::Cognito::UserPoolRiskConfigurationAttachment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html
    :cloudformationResource: AWS::Cognito::UserPoolRiskConfigurationAttachment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        client_id: builtins.str,
        user_pool_id: builtins.str,
        account_takeover_risk_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty"]] = None,
        compromised_credentials_risk_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty"]] = None,
        risk_exception_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolRiskConfigurationAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param client_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.
        :param account_takeover_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.
        :param compromised_credentials_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.
        :param risk_exception_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.
        """
        props = CfnUserPoolRiskConfigurationAttachmentProps(
            client_id=client_id,
            user_pool_id=user_pool_id,
            account_takeover_risk_configuration=account_takeover_risk_configuration,
            compromised_credentials_risk_configuration=compromised_credentials_risk_configuration,
            risk_exception_configuration=risk_exception_configuration,
        )

        jsii.create(CfnUserPoolRiskConfigurationAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-clientid
        """
        return jsii.get(self, "clientId")

    @client_id.setter # type: ignore
    def client_id(self, value: builtins.str) -> None:
        jsii.set(self, "clientId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty"]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfiguration
        """
        return jsii.get(self, "accountTakeoverRiskConfiguration")

    @account_takeover_risk_configuration.setter # type: ignore
    def account_takeover_risk_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty"]],
    ) -> None:
        jsii.set(self, "accountTakeoverRiskConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty"]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfiguration
        """
        return jsii.get(self, "compromisedCredentialsRiskConfiguration")

    @compromised_credentials_risk_configuration.setter # type: ignore
    def compromised_credentials_risk_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty"]],
    ) -> None:
        jsii.set(self, "compromisedCredentialsRiskConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="riskExceptionConfiguration")
    def risk_exception_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty"]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfiguration
        """
        return jsii.get(self, "riskExceptionConfiguration")

    @risk_exception_configuration.setter # type: ignore
    def risk_exception_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty"]],
    ) -> None:
        jsii.set(self, "riskExceptionConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"event_action": "eventAction", "notify": "notify"},
    )
    class AccountTakeoverActionTypeProperty:
        def __init__(
            self,
            *,
            event_action: builtins.str,
            notify: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        ) -> None:
            """
            :param event_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.EventAction``.
            :param notify: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.Notify``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "event_action": event_action,
                "notify": notify,
            }

        @builtins.property
        def event_action(self) -> builtins.str:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.EventAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype-eventaction
            """
            result = self._values.get("event_action")
            assert result is not None, "Required property 'event_action' is missing"
            return result

        @builtins.property
        def notify(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty.Notify``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractiontype-notify
            """
            result = self._values.get("notify")
            assert result is not None, "Required property 'notify' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountTakeoverActionTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "high_action": "highAction",
            "low_action": "lowAction",
            "medium_action": "mediumAction",
        },
    )
    class AccountTakeoverActionsTypeProperty:
        def __init__(
            self,
            *,
            high_action: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]] = None,
            low_action: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]] = None,
            medium_action: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]] = None,
        ) -> None:
            """
            :param high_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.HighAction``.
            :param low_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.LowAction``.
            :param medium_action: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.MediumAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if high_action is not None:
                self._values["high_action"] = high_action
            if low_action is not None:
                self._values["low_action"] = low_action
            if medium_action is not None:
                self._values["medium_action"] = medium_action

        @builtins.property
        def high_action(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.HighAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-highaction
            """
            result = self._values.get("high_action")
            return result

        @builtins.property
        def low_action(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.LowAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-lowaction
            """
            result = self._values.get("low_action")
            return result

        @builtins.property
        def medium_action(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionTypeProperty"]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty.MediumAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoveractionstype-mediumaction
            """
            result = self._values.get("medium_action")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountTakeoverActionsTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "notify_configuration": "notifyConfiguration",
        },
    )
    class AccountTakeoverRiskConfigurationTypeProperty:
        def __init__(
            self,
            *,
            actions: typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty"],
            notify_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty"]] = None,
        ) -> None:
            """
            :param actions: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.Actions``.
            :param notify_configuration: ``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.NotifyConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "actions": actions,
            }
            if notify_configuration is not None:
                self._values["notify_configuration"] = notify_configuration

        @builtins.property
        def actions(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.AccountTakeoverActionsTypeProperty"]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.Actions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype-actions
            """
            result = self._values.get("actions")
            assert result is not None, "Required property 'actions' is missing"
            return result

        @builtins.property
        def notify_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty"]]:
            """``CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty.NotifyConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfigurationtype-notifyconfiguration
            """
            result = self._values.get("notify_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountTakeoverRiskConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"event_action": "eventAction"},
    )
    class CompromisedCredentialsActionsTypeProperty:
        def __init__(self, *, event_action: builtins.str) -> None:
            """
            :param event_action: ``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty.EventAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "event_action": event_action,
            }

        @builtins.property
        def event_action(self) -> builtins.str:
            """``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty.EventAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsactionstype-eventaction
            """
            result = self._values.get("event_action")
            assert result is not None, "Required property 'event_action' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompromisedCredentialsActionsTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"actions": "actions", "event_filter": "eventFilter"},
    )
    class CompromisedCredentialsRiskConfigurationTypeProperty:
        def __init__(
            self,
            *,
            actions: typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty"],
            event_filter: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param actions: ``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.Actions``.
            :param event_filter: ``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.EventFilter``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "actions": actions,
            }
            if event_filter is not None:
                self._values["event_filter"] = event_filter

        @builtins.property
        def actions(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsActionsTypeProperty"]:
            """``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.Actions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype-actions
            """
            result = self._values.get("actions")
            assert result is not None, "Required property 'actions' is missing"
            return result

        @builtins.property
        def event_filter(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty.EventFilter``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfigurationtype-eventfilter
            """
            result = self._values.get("event_filter")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompromisedCredentialsRiskConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_arn": "sourceArn",
            "block_email": "blockEmail",
            "from_": "from",
            "mfa_email": "mfaEmail",
            "no_action_email": "noActionEmail",
            "reply_to": "replyTo",
        },
    )
    class NotifyConfigurationTypeProperty:
        def __init__(
            self,
            *,
            source_arn: builtins.str,
            block_email: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]] = None,
            from_: typing.Optional[builtins.str] = None,
            mfa_email: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]] = None,
            no_action_email: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]] = None,
            reply_to: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param source_arn: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.SourceArn``.
            :param block_email: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.BlockEmail``.
            :param from_: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.From``.
            :param mfa_email: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.MfaEmail``.
            :param no_action_email: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.NoActionEmail``.
            :param reply_to: ``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.ReplyTo``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "source_arn": source_arn,
            }
            if block_email is not None:
                self._values["block_email"] = block_email
            if from_ is not None:
                self._values["from_"] = from_
            if mfa_email is not None:
                self._values["mfa_email"] = mfa_email
            if no_action_email is not None:
                self._values["no_action_email"] = no_action_email
            if reply_to is not None:
                self._values["reply_to"] = reply_to

        @builtins.property
        def source_arn(self) -> builtins.str:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.SourceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-sourcearn
            """
            result = self._values.get("source_arn")
            assert result is not None, "Required property 'source_arn' is missing"
            return result

        @builtins.property
        def block_email(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.BlockEmail``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-blockemail
            """
            result = self._values.get("block_email")
            return result

        @builtins.property
        def from_(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.From``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-from
            """
            result = self._values.get("from_")
            return result

        @builtins.property
        def mfa_email(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.MfaEmail``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-mfaemail
            """
            result = self._values.get("mfa_email")
            return result

        @builtins.property
        def no_action_email(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty"]]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.NoActionEmail``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-noactionemail
            """
            result = self._values.get("no_action_email")
            return result

        @builtins.property
        def reply_to(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyConfigurationTypeProperty.ReplyTo``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyconfigurationtype-replyto
            """
            result = self._values.get("reply_to")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotifyConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subject": "subject",
            "html_body": "htmlBody",
            "text_body": "textBody",
        },
    )
    class NotifyEmailTypeProperty:
        def __init__(
            self,
            *,
            subject: builtins.str,
            html_body: typing.Optional[builtins.str] = None,
            text_body: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param subject: ``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.Subject``.
            :param html_body: ``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.HtmlBody``.
            :param text_body: ``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.TextBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "subject": subject,
            }
            if html_body is not None:
                self._values["html_body"] = html_body
            if text_body is not None:
                self._values["text_body"] = text_body

        @builtins.property
        def subject(self) -> builtins.str:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.Subject``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-subject
            """
            result = self._values.get("subject")
            assert result is not None, "Required property 'subject' is missing"
            return result

        @builtins.property
        def html_body(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.HtmlBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-htmlbody
            """
            result = self._values.get("html_body")
            return result

        @builtins.property
        def text_body(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolRiskConfigurationAttachment.NotifyEmailTypeProperty.TextBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-notifyemailtype.html#cfn-cognito-userpoolriskconfigurationattachment-notifyemailtype-textbody
            """
            result = self._values.get("text_body")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotifyEmailTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "blocked_ip_range_list": "blockedIpRangeList",
            "skipped_ip_range_list": "skippedIpRangeList",
        },
    )
    class RiskExceptionConfigurationTypeProperty:
        def __init__(
            self,
            *,
            blocked_ip_range_list: typing.Optional[typing.List[builtins.str]] = None,
            skipped_ip_range_list: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param blocked_ip_range_list: ``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.BlockedIPRangeList``.
            :param skipped_ip_range_list: ``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.SkippedIPRangeList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if blocked_ip_range_list is not None:
                self._values["blocked_ip_range_list"] = blocked_ip_range_list
            if skipped_ip_range_list is not None:
                self._values["skipped_ip_range_list"] = skipped_ip_range_list

        @builtins.property
        def blocked_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.BlockedIPRangeList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype-blockediprangelist
            """
            result = self._values.get("blocked_ip_range_list")
            return result

        @builtins.property
        def skipped_ip_range_list(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty.SkippedIPRangeList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfigurationtype-skippediprangelist
            """
            result = self._values.get("skipped_ip_range_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RiskExceptionConfigurationTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolRiskConfigurationAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "user_pool_id": "userPoolId",
        "account_takeover_risk_configuration": "accountTakeoverRiskConfiguration",
        "compromised_credentials_risk_configuration": "compromisedCredentialsRiskConfiguration",
        "risk_exception_configuration": "riskExceptionConfiguration",
    },
)
class CfnUserPoolRiskConfigurationAttachmentProps:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        user_pool_id: builtins.str,
        account_takeover_risk_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty]] = None,
        compromised_credentials_risk_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty]] = None,
        risk_exception_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolRiskConfigurationAttachment``.

        :param client_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.
        :param account_takeover_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.
        :param compromised_credentials_risk_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.
        :param risk_exception_configuration: ``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "client_id": client_id,
            "user_pool_id": user_pool_id,
        }
        if account_takeover_risk_configuration is not None:
            self._values["account_takeover_risk_configuration"] = account_takeover_risk_configuration
        if compromised_credentials_risk_configuration is not None:
            self._values["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
        if risk_exception_configuration is not None:
            self._values["risk_exception_configuration"] = risk_exception_configuration

    @builtins.property
    def client_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.ClientId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-clientid
        """
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return result

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def account_takeover_risk_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfigurationTypeProperty]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.AccountTakeoverRiskConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-accounttakeoverriskconfiguration
        """
        result = self._values.get("account_takeover_risk_configuration")
        return result

    @builtins.property
    def compromised_credentials_risk_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfigurationTypeProperty]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.CompromisedCredentialsRiskConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-compromisedcredentialsriskconfiguration
        """
        result = self._values.get("compromised_credentials_risk_configuration")
        return result

    @builtins.property
    def risk_exception_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolRiskConfigurationAttachment.RiskExceptionConfigurationTypeProperty]]:
        """``AWS::Cognito::UserPoolRiskConfigurationAttachment.RiskExceptionConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html#cfn-cognito-userpoolriskconfigurationattachment-riskexceptionconfiguration
        """
        result = self._values.get("risk_exception_configuration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolRiskConfigurationAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolUICustomizationAttachment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUICustomizationAttachment",
):
    """A CloudFormation ``AWS::Cognito::UserPoolUICustomizationAttachment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html
    :cloudformationResource: AWS::Cognito::UserPoolUICustomizationAttachment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        client_id: builtins.str,
        user_pool_id: builtins.str,
        css: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolUICustomizationAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param client_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.
        :param css: ``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.
        """
        props = CfnUserPoolUICustomizationAttachmentProps(
            client_id=client_id, user_pool_id=user_pool_id, css=css
        )

        jsii.create(CfnUserPoolUICustomizationAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-clientid
        """
        return jsii.get(self, "clientId")

    @client_id.setter # type: ignore
    def client_id(self, value: builtins.str) -> None:
        jsii.set(self, "clientId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="css")
    def css(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-css
        """
        return jsii.get(self, "css")

    @css.setter # type: ignore
    def css(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "css", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUICustomizationAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "user_pool_id": "userPoolId", "css": "css"},
)
class CfnUserPoolUICustomizationAttachmentProps:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        user_pool_id: builtins.str,
        css: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolUICustomizationAttachment``.

        :param client_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.
        :param css: ``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "client_id": client_id,
            "user_pool_id": user_pool_id,
        }
        if css is not None:
            self._values["css"] = css

    @builtins.property
    def client_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.ClientId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-clientid
        """
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return result

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def css(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolUICustomizationAttachment.CSS``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html#cfn-cognito-userpooluicustomizationattachment-css
        """
        result = self._values.get("css")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolUICustomizationAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolUser(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUser",
):
    """A CloudFormation ``AWS::Cognito::UserPoolUser``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html
    :cloudformationResource: AWS::Cognito::UserPoolUser
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        user_pool_id: builtins.str,
        client_metadata: typing.Any = None,
        desired_delivery_mediums: typing.Optional[typing.List[builtins.str]] = None,
        force_alias_creation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        message_action: typing.Optional[builtins.str] = None,
        user_attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]] = None,
        username: typing.Optional[builtins.str] = None,
        validation_data: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]] = None,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolUser``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_pool_id: ``AWS::Cognito::UserPoolUser.UserPoolId``.
        :param client_metadata: ``AWS::Cognito::UserPoolUser.ClientMetadata``.
        :param desired_delivery_mediums: ``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.
        :param force_alias_creation: ``AWS::Cognito::UserPoolUser.ForceAliasCreation``.
        :param message_action: ``AWS::Cognito::UserPoolUser.MessageAction``.
        :param user_attributes: ``AWS::Cognito::UserPoolUser.UserAttributes``.
        :param username: ``AWS::Cognito::UserPoolUser.Username``.
        :param validation_data: ``AWS::Cognito::UserPoolUser.ValidationData``.
        """
        props = CfnUserPoolUserProps(
            user_pool_id=user_pool_id,
            client_metadata=client_metadata,
            desired_delivery_mediums=desired_delivery_mediums,
            force_alias_creation=force_alias_creation,
            message_action=message_action,
            user_attributes=user_attributes,
            username=username,
            validation_data=validation_data,
        )

        jsii.create(CfnUserPoolUser, self, [scope, id, props])

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
    @jsii.member(jsii_name="clientMetadata")
    def client_metadata(self) -> typing.Any:
        """``AWS::Cognito::UserPoolUser.ClientMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-clientmetadata
        """
        return jsii.get(self, "clientMetadata")

    @client_metadata.setter # type: ignore
    def client_metadata(self, value: typing.Any) -> None:
        jsii.set(self, "clientMetadata", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUser.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="desiredDeliveryMediums")
    def desired_delivery_mediums(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-desireddeliverymediums
        """
        return jsii.get(self, "desiredDeliveryMediums")

    @desired_delivery_mediums.setter # type: ignore
    def desired_delivery_mediums(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "desiredDeliveryMediums", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="forceAliasCreation")
    def force_alias_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::UserPoolUser.ForceAliasCreation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-forcealiascreation
        """
        return jsii.get(self, "forceAliasCreation")

    @force_alias_creation.setter # type: ignore
    def force_alias_creation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "forceAliasCreation", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="messageAction")
    def message_action(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolUser.MessageAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-messageaction
        """
        return jsii.get(self, "messageAction")

    @message_action.setter # type: ignore
    def message_action(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "messageAction", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userAttributes")
    def user_attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]]:
        """``AWS::Cognito::UserPoolUser.UserAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userattributes
        """
        return jsii.get(self, "userAttributes")

    @user_attributes.setter # type: ignore
    def user_attributes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]],
    ) -> None:
        jsii.set(self, "userAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolUser.Username``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-username
        """
        return jsii.get(self, "username")

    @username.setter # type: ignore
    def username(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "username", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="validationData")
    def validation_data(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]]:
        """``AWS::Cognito::UserPoolUser.ValidationData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-validationdata
        """
        return jsii.get(self, "validationData")

    @validation_data.setter # type: ignore
    def validation_data(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnUserPoolUser.AttributeTypeProperty"]]]],
    ) -> None:
        jsii.set(self, "validationData", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUser.AttributeTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class AttributeTypeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param name: ``CfnUserPoolUser.AttributeTypeProperty.Name``.
            :param value: ``CfnUserPoolUser.AttributeTypeProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolUser.AttributeTypeProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html#cfn-cognito-userpooluser-attributetype-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnUserPoolUser.AttributeTypeProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-userpooluser-attributetype.html#cfn-cognito-userpooluser-attributetype-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_id": "userPoolId",
        "client_metadata": "clientMetadata",
        "desired_delivery_mediums": "desiredDeliveryMediums",
        "force_alias_creation": "forceAliasCreation",
        "message_action": "messageAction",
        "user_attributes": "userAttributes",
        "username": "username",
        "validation_data": "validationData",
    },
)
class CfnUserPoolUserProps:
    def __init__(
        self,
        *,
        user_pool_id: builtins.str,
        client_metadata: typing.Any = None,
        desired_delivery_mediums: typing.Optional[typing.List[builtins.str]] = None,
        force_alias_creation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        message_action: typing.Optional[builtins.str] = None,
        user_attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolUser.AttributeTypeProperty]]]] = None,
        username: typing.Optional[builtins.str] = None,
        validation_data: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolUser.AttributeTypeProperty]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolUser``.

        :param user_pool_id: ``AWS::Cognito::UserPoolUser.UserPoolId``.
        :param client_metadata: ``AWS::Cognito::UserPoolUser.ClientMetadata``.
        :param desired_delivery_mediums: ``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.
        :param force_alias_creation: ``AWS::Cognito::UserPoolUser.ForceAliasCreation``.
        :param message_action: ``AWS::Cognito::UserPoolUser.MessageAction``.
        :param user_attributes: ``AWS::Cognito::UserPoolUser.UserAttributes``.
        :param username: ``AWS::Cognito::UserPoolUser.Username``.
        :param validation_data: ``AWS::Cognito::UserPoolUser.ValidationData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool_id": user_pool_id,
        }
        if client_metadata is not None:
            self._values["client_metadata"] = client_metadata
        if desired_delivery_mediums is not None:
            self._values["desired_delivery_mediums"] = desired_delivery_mediums
        if force_alias_creation is not None:
            self._values["force_alias_creation"] = force_alias_creation
        if message_action is not None:
            self._values["message_action"] = message_action
        if user_attributes is not None:
            self._values["user_attributes"] = user_attributes
        if username is not None:
            self._values["username"] = username
        if validation_data is not None:
            self._values["validation_data"] = validation_data

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUser.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    @builtins.property
    def client_metadata(self) -> typing.Any:
        """``AWS::Cognito::UserPoolUser.ClientMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-clientmetadata
        """
        result = self._values.get("client_metadata")
        return result

    @builtins.property
    def desired_delivery_mediums(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Cognito::UserPoolUser.DesiredDeliveryMediums``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-desireddeliverymediums
        """
        result = self._values.get("desired_delivery_mediums")
        return result

    @builtins.property
    def force_alias_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::Cognito::UserPoolUser.ForceAliasCreation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-forcealiascreation
        """
        result = self._values.get("force_alias_creation")
        return result

    @builtins.property
    def message_action(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolUser.MessageAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-messageaction
        """
        result = self._values.get("message_action")
        return result

    @builtins.property
    def user_attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolUser.AttributeTypeProperty]]]]:
        """``AWS::Cognito::UserPoolUser.UserAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-userattributes
        """
        result = self._values.get("user_attributes")
        return result

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        """``AWS::Cognito::UserPoolUser.Username``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-username
        """
        result = self._values.get("username")
        return result

    @builtins.property
    def validation_data(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnUserPoolUser.AttributeTypeProperty]]]]:
        """``AWS::Cognito::UserPoolUser.ValidationData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html#cfn-cognito-userpooluser-validationdata
        """
        result = self._values.get("validation_data")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserPoolUserToGroupAttachment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserToGroupAttachment",
):
    """A CloudFormation ``AWS::Cognito::UserPoolUserToGroupAttachment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html
    :cloudformationResource: AWS::Cognito::UserPoolUserToGroupAttachment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        group_name: builtins.str,
        username: builtins.str,
        user_pool_id: builtins.str,
    ) -> None:
        """Create a new ``AWS::Cognito::UserPoolUserToGroupAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: ``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.
        :param username: ``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.
        """
        props = CfnUserPoolUserToGroupAttachmentProps(
            group_name=group_name, username=username, user_pool_id=user_pool_id
        )

        jsii.create(CfnUserPoolUserToGroupAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-groupname
        """
        return jsii.get(self, "groupName")

    @group_name.setter # type: ignore
    def group_name(self, value: builtins.str) -> None:
        jsii.set(self, "groupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-username
        """
        return jsii.get(self, "username")

    @username.setter # type: ignore
    def username(self, value: builtins.str) -> None:
        jsii.set(self, "username", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-userpoolid
        """
        return jsii.get(self, "userPoolId")

    @user_pool_id.setter # type: ignore
    def user_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "userPoolId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CfnUserPoolUserToGroupAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "username": "username",
        "user_pool_id": "userPoolId",
    },
)
class CfnUserPoolUserToGroupAttachmentProps:
    def __init__(
        self,
        *,
        group_name: builtins.str,
        username: builtins.str,
        user_pool_id: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::Cognito::UserPoolUserToGroupAttachment``.

        :param group_name: ``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.
        :param username: ``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.
        :param user_pool_id: ``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "group_name": group_name,
            "username": username,
            "user_pool_id": user_pool_id,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.GroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-groupname
        """
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return result

    @builtins.property
    def username(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.Username``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-username
        """
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return result

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        """``AWS::Cognito::UserPoolUserToGroupAttachment.UserPoolId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html#cfn-cognito-userpoolusertogroupattachment-userpoolid
        """
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPoolUserToGroupAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CognitoDomainOptions",
    jsii_struct_bases=[],
    name_mapping={"domain_prefix": "domainPrefix"},
)
class CognitoDomainOptions:
    def __init__(self, *, domain_prefix: builtins.str) -> None:
        """Options while specifying a cognito prefix domain.

        :param domain_prefix: The prefix to the Cognito hosted domain name that will be associated with the user pool.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_prefix": domain_prefix,
        }

    @builtins.property
    def domain_prefix(self) -> builtins.str:
        """The prefix to the Cognito hosted domain name that will be associated with the user pool."""
        result = self._values.get("domain_prefix")
        assert result is not None, "Required property 'domain_prefix' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoDomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CustomAttributeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "data_type": "dataType",
        "mutable": "mutable",
        "number_constraints": "numberConstraints",
        "string_constraints": "stringConstraints",
    },
)
class CustomAttributeConfig:
    def __init__(
        self,
        *,
        data_type: builtins.str,
        mutable: typing.Optional[builtins.bool] = None,
        number_constraints: typing.Optional["NumberAttributeConstraints"] = None,
        string_constraints: typing.Optional["StringAttributeConstraints"] = None,
    ) -> None:
        """Configuration that will be fed into CloudFormation for any custom attribute type.

        :param data_type: The data type of the custom attribute.
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        :param number_constraints: The constraints for a custom attribute of the 'Number' data type. Default: - None.
        :param string_constraints: The constraints for a custom attribute of 'String' data type. Default: - None.
        """
        if isinstance(number_constraints, dict):
            number_constraints = NumberAttributeConstraints(**number_constraints)
        if isinstance(string_constraints, dict):
            string_constraints = StringAttributeConstraints(**string_constraints)
        self._values: typing.Dict[str, typing.Any] = {
            "data_type": data_type,
        }
        if mutable is not None:
            self._values["mutable"] = mutable
        if number_constraints is not None:
            self._values["number_constraints"] = number_constraints
        if string_constraints is not None:
            self._values["string_constraints"] = string_constraints

    @builtins.property
    def data_type(self) -> builtins.str:
        """The data type of the custom attribute.

        :see: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SchemaAttributeType.html#CognitoUserPools-Type-SchemaAttributeType-AttributeDataType
        """
        result = self._values.get("data_type")
        assert result is not None, "Required property 'data_type' is missing"
        return result

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        :default: false
        """
        result = self._values.get("mutable")
        return result

    @builtins.property
    def number_constraints(self) -> typing.Optional["NumberAttributeConstraints"]:
        """The constraints for a custom attribute of the 'Number' data type.

        :default: - None.
        """
        result = self._values.get("number_constraints")
        return result

    @builtins.property
    def string_constraints(self) -> typing.Optional["StringAttributeConstraints"]:
        """The constraints for a custom attribute of 'String' data type.

        :default: - None.
        """
        result = self._values.get("string_constraints")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAttributeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CustomAttributeProps",
    jsii_struct_bases=[],
    name_mapping={"mutable": "mutable"},
)
class CustomAttributeProps:
    def __init__(self, *, mutable: typing.Optional[builtins.bool] = None) -> None:
        """Constraints that can be applied to a custom attribute of any type.

        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if mutable is not None:
            self._values["mutable"] = mutable

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        :default: false
        """
        result = self._values.get("mutable")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAttributeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.CustomDomainOptions",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "domain_name": "domainName"},
)
class CustomDomainOptions:
    def __init__(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        domain_name: builtins.str,
    ) -> None:
        """Options while specifying custom domain.

        :param certificate: The certificate to associate with this domain.
        :param domain_name: The custom domain name that you would like to associate with this User Pool.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "domain_name": domain_name,
        }

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        """The certificate to associate with this domain."""
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return result

    @builtins.property
    def domain_name(self) -> builtins.str:
        """The custom domain name that you would like to associate with this User Pool."""
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomDomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.EmailSettings",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "reply_to": "replyTo"},
)
class EmailSettings:
    def __init__(
        self,
        *,
        from_: typing.Optional[builtins.str] = None,
        reply_to: typing.Optional[builtins.str] = None,
    ) -> None:
        """Email settings for the user pool.

        :param from_: The 'from' address on the emails received by the user. Default: noreply
        :param reply_to: The 'replyTo' address on the emails received by the user as defined by IETF RFC-5322. When set, most email clients recognize to change 'to' line to this address when a reply is drafted. Default: - Not set.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if from_ is not None:
            self._values["from_"] = from_
        if reply_to is not None:
            self._values["reply_to"] = reply_to

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        """The 'from' address on the emails received by the user.

        :default: noreply

        :verificationemail: .com
        """
        result = self._values.get("from_")
        return result

    @builtins.property
    def reply_to(self) -> typing.Optional[builtins.str]:
        """The 'replyTo' address on the emails received by the user as defined by IETF RFC-5322.

        When set, most email clients recognize to change 'to' line to this address when a reply is drafted.

        :default: - Not set.
        """
        result = self._values.get("reply_to")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.ICustomAttribute")
class ICustomAttribute(typing_extensions.Protocol):
    """Represents a custom attribute type."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICustomAttributeProxy

    @jsii.member(jsii_name="bind")
    def bind(self) -> CustomAttributeConfig:
        """Bind this custom attribute type to the values as expected by CloudFormation."""
        ...


class _ICustomAttributeProxy:
    """Represents a custom attribute type."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito.ICustomAttribute"

    @jsii.member(jsii_name="bind")
    def bind(self) -> CustomAttributeConfig:
        """Bind this custom attribute type to the values as expected by CloudFormation."""
        return jsii.invoke(self, "bind", [])


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPool")
class IUserPool(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents a Cognito UserPool."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identityProviders")
    def identity_providers(self) -> typing.List["IUserPoolIdentityProvider"]:
        """Get all identity providers registered with this user pool."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> builtins.str:
        """The ARN of this user pool resource.

        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """The physical ID of this user pool resource.

        :attribute: true
        """
        ...

    @jsii.member(jsii_name="addClient")
    def add_client(
        self,
        id: builtins.str,
        *,
        auth_flows: typing.Optional[AuthFlow] = None,
        disable_o_auth: typing.Optional[builtins.bool] = None,
        generate_secret: typing.Optional[builtins.bool] = None,
        o_auth: typing.Optional["OAuthSettings"] = None,
        prevent_user_existence_errors: typing.Optional[builtins.bool] = None,
        supported_identity_providers: typing.Optional[typing.List["UserPoolClientIdentityProvider"]] = None,
        user_pool_client_name: typing.Optional[builtins.str] = None,
    ) -> "UserPoolClient":
        """Add a new app client to this user pool.

        :param id: -
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param disable_o_auth: Turns off all OAuth interactions for this client. Default: false
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. An error is thrown when this is specified and ``disableOAuth`` is set. Default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param supported_identity_providers: The list of identity providers that users should be able to use to sign in using this client. Default: - supports all identity providers that are registered with the user pool. If the user pool and/or identity providers are imported, either specify this option explicitly or ensure that the identity providers are registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html
        """
        ...

    @jsii.member(jsii_name="addDomain")
    def add_domain(
        self,
        id: builtins.str,
        *,
        cognito_domain: typing.Optional[CognitoDomainOptions] = None,
        custom_domain: typing.Optional[CustomDomainOptions] = None,
    ) -> "UserPoolDomain":
        """Associate a domain to this user pool.

        :param id: -
        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain.html
        """
        ...

    @jsii.member(jsii_name="addResourceServer")
    def add_resource_server(
        self,
        id: builtins.str,
        *,
        identifier: builtins.str,
        scopes: typing.Optional[typing.List["ResourceServerScope"]] = None,
        user_pool_resource_server_name: typing.Optional[builtins.str] = None,
    ) -> "UserPoolResourceServer":
        """Add a new resource server to this user pool.

        :param id: -
        :param identifier: A unique resource server identifier for the resource server.
        :param scopes: Oauth scopes. Default: - No scopes will be added
        :param user_pool_resource_server_name: A friendly name for the resource server. Default: - same as ``identifier``

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-resource-servers.html
        """
        ...

    @jsii.member(jsii_name="registerIdentityProvider")
    def register_identity_provider(self, provider: "IUserPoolIdentityProvider") -> None:
        """Register an identity provider with this user pool.

        :param provider: -
        """
        ...


class _IUserPoolProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Represents a Cognito UserPool."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito.IUserPool"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identityProviders")
    def identity_providers(self) -> typing.List["IUserPoolIdentityProvider"]:
        """Get all identity providers registered with this user pool."""
        return jsii.get(self, "identityProviders")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> builtins.str:
        """The ARN of this user pool resource.

        :attribute: true
        """
        return jsii.get(self, "userPoolArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """The physical ID of this user pool resource.

        :attribute: true
        """
        return jsii.get(self, "userPoolId")

    @jsii.member(jsii_name="addClient")
    def add_client(
        self,
        id: builtins.str,
        *,
        auth_flows: typing.Optional[AuthFlow] = None,
        disable_o_auth: typing.Optional[builtins.bool] = None,
        generate_secret: typing.Optional[builtins.bool] = None,
        o_auth: typing.Optional["OAuthSettings"] = None,
        prevent_user_existence_errors: typing.Optional[builtins.bool] = None,
        supported_identity_providers: typing.Optional[typing.List["UserPoolClientIdentityProvider"]] = None,
        user_pool_client_name: typing.Optional[builtins.str] = None,
    ) -> "UserPoolClient":
        """Add a new app client to this user pool.

        :param id: -
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param disable_o_auth: Turns off all OAuth interactions for this client. Default: false
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. An error is thrown when this is specified and ``disableOAuth`` is set. Default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param supported_identity_providers: The list of identity providers that users should be able to use to sign in using this client. Default: - supports all identity providers that are registered with the user pool. If the user pool and/or identity providers are imported, either specify this option explicitly or ensure that the identity providers are registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html
        """
        options = UserPoolClientOptions(
            auth_flows=auth_flows,
            disable_o_auth=disable_o_auth,
            generate_secret=generate_secret,
            o_auth=o_auth,
            prevent_user_existence_errors=prevent_user_existence_errors,
            supported_identity_providers=supported_identity_providers,
            user_pool_client_name=user_pool_client_name,
        )

        return jsii.invoke(self, "addClient", [id, options])

    @jsii.member(jsii_name="addDomain")
    def add_domain(
        self,
        id: builtins.str,
        *,
        cognito_domain: typing.Optional[CognitoDomainOptions] = None,
        custom_domain: typing.Optional[CustomDomainOptions] = None,
    ) -> "UserPoolDomain":
        """Associate a domain to this user pool.

        :param id: -
        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain.html
        """
        options = UserPoolDomainOptions(
            cognito_domain=cognito_domain, custom_domain=custom_domain
        )

        return jsii.invoke(self, "addDomain", [id, options])

    @jsii.member(jsii_name="addResourceServer")
    def add_resource_server(
        self,
        id: builtins.str,
        *,
        identifier: builtins.str,
        scopes: typing.Optional[typing.List["ResourceServerScope"]] = None,
        user_pool_resource_server_name: typing.Optional[builtins.str] = None,
    ) -> "UserPoolResourceServer":
        """Add a new resource server to this user pool.

        :param id: -
        :param identifier: A unique resource server identifier for the resource server.
        :param scopes: Oauth scopes. Default: - No scopes will be added
        :param user_pool_resource_server_name: A friendly name for the resource server. Default: - same as ``identifier``

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-resource-servers.html
        """
        options = UserPoolResourceServerOptions(
            identifier=identifier,
            scopes=scopes,
            user_pool_resource_server_name=user_pool_resource_server_name,
        )

        return jsii.invoke(self, "addResourceServer", [id, options])

    @jsii.member(jsii_name="registerIdentityProvider")
    def register_identity_provider(self, provider: "IUserPoolIdentityProvider") -> None:
        """Register an identity provider with this user pool.

        :param provider: -
        """
        return jsii.invoke(self, "registerIdentityProvider", [provider])


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPoolClient")
class IUserPoolClient(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents a Cognito user pool client."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolClientProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> builtins.str:
        """Name of the application client.

        :attribute: true
        """
        ...


class _IUserPoolClientProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Represents a Cognito user pool client."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito.IUserPoolClient"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> builtins.str:
        """Name of the application client.

        :attribute: true
        """
        return jsii.get(self, "userPoolClientId")


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPoolDomain")
class IUserPoolDomain(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents a user pool domain."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolDomainProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """The domain that was specified to be created.

        If ``customDomain`` was selected, this holds the full domain name that was specified.
        If the ``cognitoDomain`` was used, it contains the prefix to the Cognito hosted domain.

        :attribute: true
        """
        ...


class _IUserPoolDomainProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Represents a user pool domain."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito.IUserPoolDomain"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """The domain that was specified to be created.

        If ``customDomain`` was selected, this holds the full domain name that was specified.
        If the ``cognitoDomain`` was used, it contains the prefix to the Cognito hosted domain.

        :attribute: true
        """
        return jsii.get(self, "domainName")


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPoolIdentityProvider")
class IUserPoolIdentityProvider(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents a UserPoolIdentityProvider."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolIdentityProviderProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        """The primary identifier of this identity provider.

        :attribute: true
        """
        ...


class _IUserPoolIdentityProviderProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Represents a UserPoolIdentityProvider."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito.IUserPoolIdentityProvider"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        """The primary identifier of this identity provider.

        :attribute: true
        """
        return jsii.get(self, "providerName")


@jsii.interface(jsii_type="@aws-cdk/aws-cognito.IUserPoolResourceServer")
class IUserPoolResourceServer(aws_cdk.core.IResource, typing_extensions.Protocol):
    """Represents a Cognito user pool resource server."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IUserPoolResourceServerProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolResourceServerId")
    def user_pool_resource_server_id(self) -> builtins.str:
        """Resource server id.

        :attribute: true
        """
        ...


class _IUserPoolResourceServerProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """Represents a Cognito user pool resource server."""

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito.IUserPoolResourceServer"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolResourceServerId")
    def user_pool_resource_server_id(self) -> builtins.str:
        """Resource server id.

        :attribute: true
        """
        return jsii.get(self, "userPoolResourceServerId")


@jsii.enum(jsii_type="@aws-cdk/aws-cognito.Mfa")
class Mfa(enum.Enum):
    """The different ways in which a user pool's MFA enforcement can be configured.

    :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html
    """

    OFF = "OFF"
    """Users are not required to use MFA for sign in, and cannot configure one."""
    OPTIONAL = "OPTIONAL"
    """Users are not required to use MFA for sign in, but can configure one if they so choose to."""
    REQUIRED = "REQUIRED"
    """Users are required to configure an MFA, and have to use it to sign in."""


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.MfaSecondFactor",
    jsii_struct_bases=[],
    name_mapping={"otp": "otp", "sms": "sms"},
)
class MfaSecondFactor:
    def __init__(self, *, otp: builtins.bool, sms: builtins.bool) -> None:
        """The different ways in which a user pool can obtain their MFA token for sign in.

        :param otp: The MFA token is a time-based one time password that is generated by a hardware or software token. Default: false
        :param sms: The MFA token is sent to the user via SMS to their verified phone numbers. Default: true

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "otp": otp,
            "sms": sms,
        }

    @builtins.property
    def otp(self) -> builtins.bool:
        """The MFA token is a time-based one time password that is generated by a hardware or software token.

        :default: false

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html
        """
        result = self._values.get("otp")
        assert result is not None, "Required property 'otp' is missing"
        return result

    @builtins.property
    def sms(self) -> builtins.bool:
        """The MFA token is sent to the user via SMS to their verified phone numbers.

        :default: true

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-sms-text-message.html
        """
        result = self._values.get("sms")
        assert result is not None, "Required property 'sms' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MfaSecondFactor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICustomAttribute)
class NumberAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.NumberAttribute",
):
    """The Number custom attribute type."""

    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param max: Maximum value of this attribute. Default: - no maximum value
        :param min: Minimum value of this attribute. Default: - no minimum value
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        """
        props = NumberAttributeProps(max=max, min=min, mutable=mutable)

        jsii.create(NumberAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> CustomAttributeConfig:
        """Bind this custom attribute type to the values as expected by CloudFormation."""
        return jsii.invoke(self, "bind", [])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.NumberAttributeConstraints",
    jsii_struct_bases=[],
    name_mapping={"max": "max", "min": "min"},
)
class NumberAttributeConstraints:
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Constraints that can be applied to a custom attribute of number type.

        :param max: Maximum value of this attribute. Default: - no maximum value
        :param min: Minimum value of this attribute. Default: - no minimum value
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        """Maximum value of this attribute.

        :default: - no maximum value
        """
        result = self._values.get("max")
        return result

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        """Minimum value of this attribute.

        :default: - no minimum value
        """
        result = self._values.get("min")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NumberAttributeConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.NumberAttributeProps",
    jsii_struct_bases=[NumberAttributeConstraints, CustomAttributeProps],
    name_mapping={"max": "max", "min": "min", "mutable": "mutable"},
)
class NumberAttributeProps(NumberAttributeConstraints, CustomAttributeProps):
    def __init__(
        self,
        *,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Props for NumberAttr.

        :param max: Maximum value of this attribute. Default: - no maximum value
        :param min: Minimum value of this attribute. Default: - no minimum value
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min
        if mutable is not None:
            self._values["mutable"] = mutable

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        """Maximum value of this attribute.

        :default: - no maximum value
        """
        result = self._values.get("max")
        return result

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        """Minimum value of this attribute.

        :default: - no minimum value
        """
        result = self._values.get("min")
        return result

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        :default: false
        """
        result = self._values.get("mutable")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NumberAttributeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.OAuthFlows",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_code_grant": "authorizationCodeGrant",
        "client_credentials": "clientCredentials",
        "implicit_code_grant": "implicitCodeGrant",
    },
)
class OAuthFlows:
    def __init__(
        self,
        *,
        authorization_code_grant: typing.Optional[builtins.bool] = None,
        client_credentials: typing.Optional[builtins.bool] = None,
        implicit_code_grant: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Types of OAuth grant flows.

        :param authorization_code_grant: Initiate an authorization code grant flow, which provides an authorization code as the response. Default: false
        :param client_credentials: Client should get the access token and ID token from the token endpoint using a combination of client and client_secret. Default: false
        :param implicit_code_grant: The client should get the access token and ID token directly. Default: false

        :see: - the 'Allowed OAuth Flows' section at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if authorization_code_grant is not None:
            self._values["authorization_code_grant"] = authorization_code_grant
        if client_credentials is not None:
            self._values["client_credentials"] = client_credentials
        if implicit_code_grant is not None:
            self._values["implicit_code_grant"] = implicit_code_grant

    @builtins.property
    def authorization_code_grant(self) -> typing.Optional[builtins.bool]:
        """Initiate an authorization code grant flow, which provides an authorization code as the response.

        :default: false
        """
        result = self._values.get("authorization_code_grant")
        return result

    @builtins.property
    def client_credentials(self) -> typing.Optional[builtins.bool]:
        """Client should get the access token and ID token from the token endpoint using a combination of client and client_secret.

        :default: false
        """
        result = self._values.get("client_credentials")
        return result

    @builtins.property
    def implicit_code_grant(self) -> typing.Optional[builtins.bool]:
        """The client should get the access token and ID token directly.

        :default: false
        """
        result = self._values.get("implicit_code_grant")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OAuthFlows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OAuthScope(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cognito.OAuthScope"):
    """OAuth scopes that are allowed with this client.

    :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
    """

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, name: builtins.str) -> "OAuthScope":
        """Custom scope is one that you define for your own resource server in the Resource Servers.

        The format is 'resource-server-identifier/scope'.

        :param name: -

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html
        """
        return jsii.sinvoke(cls, "custom", [name])

    @jsii.member(jsii_name="resourceServer")
    @builtins.classmethod
    def resource_server(
        cls,
        server: IUserPoolResourceServer,
        scope: "ResourceServerScope",
    ) -> "OAuthScope":
        """Adds a custom scope that's tied to a resource server in your stack.

        :param server: -
        :param scope: -
        """
        return jsii.sinvoke(cls, "resourceServer", [server, scope])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="COGNITO_ADMIN")
    def COGNITO_ADMIN(cls) -> "OAuthScope":
        """Grants access to Amazon Cognito User Pool API operations that require access tokens, such as UpdateUserAttributes and VerifyUserAttribute."""
        return jsii.sget(cls, "COGNITO_ADMIN")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="EMAIL")
    def EMAIL(cls) -> "OAuthScope":
        """Grants access to the 'email' and 'email_verified' claims.

        Automatically includes access to ``OAuthScope.OPENID``.
        """
        return jsii.sget(cls, "EMAIL")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="OPENID")
    def OPENID(cls) -> "OAuthScope":
        """Returns all user attributes in the ID token that are readable by the client."""
        return jsii.sget(cls, "OPENID")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PHONE")
    def PHONE(cls) -> "OAuthScope":
        """Grants access to the 'phone_number' and 'phone_number_verified' claims.

        Automatically includes access to ``OAuthScope.OPENID``.
        """
        return jsii.sget(cls, "PHONE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PROFILE")
    def PROFILE(cls) -> "OAuthScope":
        """Grants access to all user attributes that are readable by the client Automatically includes access to ``OAuthScope.OPENID``."""
        return jsii.sget(cls, "PROFILE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scopeName")
    def scope_name(self) -> builtins.str:
        """The name of this scope as recognized by CloudFormation.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html#cfn-cognito-userpoolclient-allowedoauthscopes
        """
        return jsii.get(self, "scopeName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.OAuthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "callback_urls": "callbackUrls",
        "flows": "flows",
        "logout_urls": "logoutUrls",
        "scopes": "scopes",
    },
)
class OAuthSettings:
    def __init__(
        self,
        *,
        callback_urls: typing.Optional[typing.List[builtins.str]] = None,
        flows: typing.Optional[OAuthFlows] = None,
        logout_urls: typing.Optional[typing.List[builtins.str]] = None,
        scopes: typing.Optional[typing.List[OAuthScope]] = None,
    ) -> None:
        """OAuth settings to configure the interaction between the app and this client.

        :param callback_urls: List of allowed redirect URLs for the identity providers. Default: - ['https://example.com'] if either authorizationCodeGrant or implicitCodeGrant flows are enabled, no callback URLs otherwise.
        :param flows: OAuth flows that are allowed with this client. Default: {authorizationCodeGrant:true,implicitCodeGrant:true}
        :param logout_urls: List of allowed logout URLs for the identity providers. Default: - no logout URLs
        :param scopes: OAuth scopes that are allowed with this client. Default: [OAuthScope.PHONE,OAuthScope.EMAIL,OAuthScope.OPENID,OAuthScope.PROFILE,OAuthScope.COGNITO_ADMIN]
        """
        if isinstance(flows, dict):
            flows = OAuthFlows(**flows)
        self._values: typing.Dict[str, typing.Any] = {}
        if callback_urls is not None:
            self._values["callback_urls"] = callback_urls
        if flows is not None:
            self._values["flows"] = flows
        if logout_urls is not None:
            self._values["logout_urls"] = logout_urls
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def callback_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        """List of allowed redirect URLs for the identity providers.

        :default: - ['https://example.com'] if either authorizationCodeGrant or implicitCodeGrant flows are enabled, no callback URLs otherwise.
        """
        result = self._values.get("callback_urls")
        return result

    @builtins.property
    def flows(self) -> typing.Optional[OAuthFlows]:
        """OAuth flows that are allowed with this client.

        :default: {authorizationCodeGrant:true,implicitCodeGrant:true}

        :see: - the 'Allowed OAuth Flows' section at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
        """
        result = self._values.get("flows")
        return result

    @builtins.property
    def logout_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        """List of allowed logout URLs for the identity providers.

        :default: - no logout URLs
        """
        result = self._values.get("logout_urls")
        return result

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[OAuthScope]]:
        """OAuth scopes that are allowed with this client.

        :default: [OAuthScope.PHONE,OAuthScope.EMAIL,OAuthScope.OPENID,OAuthScope.PROFILE,OAuthScope.COGNITO_ADMIN]

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-idp-settings.html
        """
        result = self._values.get("scopes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OAuthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.PasswordPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "min_length": "minLength",
        "require_digits": "requireDigits",
        "require_lowercase": "requireLowercase",
        "require_symbols": "requireSymbols",
        "require_uppercase": "requireUppercase",
        "temp_password_validity": "tempPasswordValidity",
    },
)
class PasswordPolicy:
    def __init__(
        self,
        *,
        min_length: typing.Optional[jsii.Number] = None,
        require_digits: typing.Optional[builtins.bool] = None,
        require_lowercase: typing.Optional[builtins.bool] = None,
        require_symbols: typing.Optional[builtins.bool] = None,
        require_uppercase: typing.Optional[builtins.bool] = None,
        temp_password_validity: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Password policy for User Pools.

        :param min_length: Minimum length required for a user's password. Default: 8
        :param require_digits: Whether the user is required to have digits in their password. Default: true
        :param require_lowercase: Whether the user is required to have lowercase characters in their password. Default: true
        :param require_symbols: Whether the user is required to have symbols in their password. Default: true
        :param require_uppercase: Whether the user is required to have uppercase characters in their password. Default: true
        :param temp_password_validity: The length of time the temporary password generated by an admin is valid. This must be provided as whole days, like Duration.days(3) or Duration.hours(48). Fractional days, such as Duration.hours(20), will generate an error. Default: Duration.days(7)
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if min_length is not None:
            self._values["min_length"] = min_length
        if require_digits is not None:
            self._values["require_digits"] = require_digits
        if require_lowercase is not None:
            self._values["require_lowercase"] = require_lowercase
        if require_symbols is not None:
            self._values["require_symbols"] = require_symbols
        if require_uppercase is not None:
            self._values["require_uppercase"] = require_uppercase
        if temp_password_validity is not None:
            self._values["temp_password_validity"] = temp_password_validity

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        """Minimum length required for a user's password.

        :default: 8
        """
        result = self._values.get("min_length")
        return result

    @builtins.property
    def require_digits(self) -> typing.Optional[builtins.bool]:
        """Whether the user is required to have digits in their password.

        :default: true
        """
        result = self._values.get("require_digits")
        return result

    @builtins.property
    def require_lowercase(self) -> typing.Optional[builtins.bool]:
        """Whether the user is required to have lowercase characters in their password.

        :default: true
        """
        result = self._values.get("require_lowercase")
        return result

    @builtins.property
    def require_symbols(self) -> typing.Optional[builtins.bool]:
        """Whether the user is required to have symbols in their password.

        :default: true
        """
        result = self._values.get("require_symbols")
        return result

    @builtins.property
    def require_uppercase(self) -> typing.Optional[builtins.bool]:
        """Whether the user is required to have uppercase characters in their password.

        :default: true
        """
        result = self._values.get("require_uppercase")
        return result

    @builtins.property
    def temp_password_validity(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time the temporary password generated by an admin is valid.

        This must be provided as whole days, like Duration.days(3) or Duration.hours(48).
        Fractional days, such as Duration.hours(20), will generate an error.

        :default: Duration.days(7)
        """
        result = self._values.get("temp_password_validity")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PasswordPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProviderAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.ProviderAttribute",
):
    """An attribute available from a third party identity provider."""

    @jsii.member(jsii_name="other")
    @builtins.classmethod
    def other(cls, attribute_name: builtins.str) -> "ProviderAttribute":
        """Use this to specify an attribute from the identity provider that is not pre-defined in the CDK.

        :param attribute_name: the attribute value string as recognized by the provider.
        """
        return jsii.sinvoke(cls, "other", [attribute_name])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_EMAIL")
    def AMAZON_EMAIL(cls) -> "ProviderAttribute":
        """The email attribute provided by Amazon."""
        return jsii.sget(cls, "AMAZON_EMAIL")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_NAME")
    def AMAZON_NAME(cls) -> "ProviderAttribute":
        """The name attribute provided by Amazon."""
        return jsii.sget(cls, "AMAZON_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_POSTAL_CODE")
    def AMAZON_POSTAL_CODE(cls) -> "ProviderAttribute":
        """The postal code attribute provided by Amazon."""
        return jsii.sget(cls, "AMAZON_POSTAL_CODE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_USER_ID")
    def AMAZON_USER_ID(cls) -> "ProviderAttribute":
        """The user id attribute provided by Amazon."""
        return jsii.sget(cls, "AMAZON_USER_ID")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_BIRTHDAY")
    def FACEBOOK_BIRTHDAY(cls) -> "ProviderAttribute":
        """The birthday attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_BIRTHDAY")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_EMAIL")
    def FACEBOOK_EMAIL(cls) -> "ProviderAttribute":
        """The email attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_EMAIL")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_FIRST_NAME")
    def FACEBOOK_FIRST_NAME(cls) -> "ProviderAttribute":
        """The first name attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_FIRST_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_GENDER")
    def FACEBOOK_GENDER(cls) -> "ProviderAttribute":
        """The gender attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_GENDER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_ID")
    def FACEBOOK_ID(cls) -> "ProviderAttribute":
        """The user id attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_ID")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_LAST_NAME")
    def FACEBOOK_LAST_NAME(cls) -> "ProviderAttribute":
        """The last name attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_LAST_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_LOCALE")
    def FACEBOOK_LOCALE(cls) -> "ProviderAttribute":
        """The locale attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_LOCALE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_MIDDLE_NAME")
    def FACEBOOK_MIDDLE_NAME(cls) -> "ProviderAttribute":
        """The middle name attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_MIDDLE_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK_NAME")
    def FACEBOOK_NAME(cls) -> "ProviderAttribute":
        """The name attribute provided by Facebook."""
        return jsii.sget(cls, "FACEBOOK_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_BIRTHDAYS")
    def GOOGLE_BIRTHDAYS(cls) -> "ProviderAttribute":
        """The birthday attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_BIRTHDAYS")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_EMAIL")
    def GOOGLE_EMAIL(cls) -> "ProviderAttribute":
        """The email attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_EMAIL")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_FAMILY_NAME")
    def GOOGLE_FAMILY_NAME(cls) -> "ProviderAttribute":
        """The email attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_FAMILY_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_GENDER")
    def GOOGLE_GENDER(cls) -> "ProviderAttribute":
        """The gender attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_GENDER")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_GIVEN_NAME")
    def GOOGLE_GIVEN_NAME(cls) -> "ProviderAttribute":
        """The email attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_GIVEN_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_NAME")
    def GOOGLE_NAME(cls) -> "ProviderAttribute":
        """The name attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_NAME")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_NAMES")
    def GOOGLE_NAMES(cls) -> "ProviderAttribute":
        """The name attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_NAMES")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_PHONE_NUMBERS")
    def GOOGLE_PHONE_NUMBERS(cls) -> "ProviderAttribute":
        """The birthday attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_PHONE_NUMBERS")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE_PICTURE")
    def GOOGLE_PICTURE(cls) -> "ProviderAttribute":
        """The email attribute provided by Google."""
        return jsii.sget(cls, "GOOGLE_PICTURE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributeName")
    def attribute_name(self) -> builtins.str:
        """The attribute value string as recognized by the provider."""
        return jsii.get(self, "attributeName")


class ResourceServerScope(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.ResourceServerScope",
):
    """A scope for ResourceServer."""

    def __init__(
        self,
        *,
        scope_description: builtins.str,
        scope_name: builtins.str,
    ) -> None:
        """
        :param scope_description: A description of the scope.
        :param scope_name: The name of the scope.
        """
        props = ResourceServerScopeProps(
            scope_description=scope_description, scope_name=scope_name
        )

        jsii.create(ResourceServerScope, self, [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scopeDescription")
    def scope_description(self) -> builtins.str:
        """A description of the scope."""
        return jsii.get(self, "scopeDescription")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scopeName")
    def scope_name(self) -> builtins.str:
        """The name of the scope."""
        return jsii.get(self, "scopeName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.ResourceServerScopeProps",
    jsii_struct_bases=[],
    name_mapping={"scope_description": "scopeDescription", "scope_name": "scopeName"},
)
class ResourceServerScopeProps:
    def __init__(
        self,
        *,
        scope_description: builtins.str,
        scope_name: builtins.str,
    ) -> None:
        """Props to initialize ResourceServerScope.

        :param scope_description: A description of the scope.
        :param scope_name: The name of the scope.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "scope_description": scope_description,
            "scope_name": scope_name,
        }

    @builtins.property
    def scope_description(self) -> builtins.str:
        """A description of the scope."""
        result = self._values.get("scope_description")
        assert result is not None, "Required property 'scope_description' is missing"
        return result

    @builtins.property
    def scope_name(self) -> builtins.str:
        """The name of the scope."""
        result = self._values.get("scope_name")
        assert result is not None, "Required property 'scope_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceServerScopeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.SignInAliases",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "phone": "phone",
        "preferred_username": "preferredUsername",
        "username": "username",
    },
)
class SignInAliases:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.bool] = None,
        phone: typing.Optional[builtins.bool] = None,
        preferred_username: typing.Optional[builtins.bool] = None,
        username: typing.Optional[builtins.bool] = None,
    ) -> None:
        """The different ways in which users of this pool can sign up or sign in.

        :param email: Whether a user is allowed to sign up or sign in with an email address. Default: false
        :param phone: Whether a user is allowed to sign up or sign in with a phone number. Default: false
        :param preferred_username: Whether a user is allowed to ign in with a secondary username, that can be set and modified after sign up. Can only be used in conjunction with ``USERNAME``. Default: false
        :param username: Whether user is allowed to sign up or sign in with a username. Default: true
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if phone is not None:
            self._values["phone"] = phone
        if preferred_username is not None:
            self._values["preferred_username"] = preferred_username
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def email(self) -> typing.Optional[builtins.bool]:
        """Whether a user is allowed to sign up or sign in with an email address.

        :default: false
        """
        result = self._values.get("email")
        return result

    @builtins.property
    def phone(self) -> typing.Optional[builtins.bool]:
        """Whether a user is allowed to sign up or sign in with a phone number.

        :default: false
        """
        result = self._values.get("phone")
        return result

    @builtins.property
    def preferred_username(self) -> typing.Optional[builtins.bool]:
        """Whether a user is allowed to ign in with a secondary username, that can be set and modified after sign up.

        Can only be used in conjunction with ``USERNAME``.

        :default: false
        """
        result = self._values.get("preferred_username")
        return result

    @builtins.property
    def username(self) -> typing.Optional[builtins.bool]:
        """Whether user is allowed to sign up or sign in with a username.

        :default: true
        """
        result = self._values.get("username")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignInAliases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.SignInUrlOptions",
    jsii_struct_bases=[],
    name_mapping={"redirect_uri": "redirectUri", "sign_in_path": "signInPath"},
)
class SignInUrlOptions:
    def __init__(
        self,
        *,
        redirect_uri: builtins.str,
        sign_in_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options to customize the behaviour of ``signInUrl()``.

        :param redirect_uri: Where to redirect to after sign in.
        :param sign_in_path: The path in the URI where the sign-in page is located. Default: '/login'
        """
        self._values: typing.Dict[str, typing.Any] = {
            "redirect_uri": redirect_uri,
        }
        if sign_in_path is not None:
            self._values["sign_in_path"] = sign_in_path

    @builtins.property
    def redirect_uri(self) -> builtins.str:
        """Where to redirect to after sign in."""
        result = self._values.get("redirect_uri")
        assert result is not None, "Required property 'redirect_uri' is missing"
        return result

    @builtins.property
    def sign_in_path(self) -> typing.Optional[builtins.str]:
        """The path in the URI where the sign-in page is located.

        :default: '/login'
        """
        result = self._values.get("sign_in_path")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignInUrlOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.StandardAttribute",
    jsii_struct_bases=[],
    name_mapping={"mutable": "mutable", "required": "required"},
)
class StandardAttribute:
    def __init__(
        self,
        *,
        mutable: typing.Optional[builtins.bool] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Standard attribute that can be marked as required or mutable.

        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, this must be set to ``true``. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: true
        :param required: Specifies whether the attribute is required upon user registration. If the attribute is required and the user does not provide a value, registration or sign-in will fail. Default: false

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#cognito-user-pools-standard-attributes
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if mutable is not None:
            self._values["mutable"] = mutable
        if required is not None:
            self._values["required"] = required

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, this must be set to ``true``.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        :default: true
        """
        result = self._values.get("mutable")
        return result

    @builtins.property
    def required(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the attribute is required upon user registration.

        If the attribute is required and the user does not provide a value, registration or sign-in will fail.

        :default: false
        """
        result = self._values.get("required")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardAttribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.StandardAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "birthdate": "birthdate",
        "email": "email",
        "family_name": "familyName",
        "fullname": "fullname",
        "gender": "gender",
        "given_name": "givenName",
        "last_update_time": "lastUpdateTime",
        "locale": "locale",
        "middle_name": "middleName",
        "nickname": "nickname",
        "phone_number": "phoneNumber",
        "preferred_username": "preferredUsername",
        "profile_page": "profilePage",
        "profile_picture": "profilePicture",
        "timezone": "timezone",
        "website": "website",
    },
)
class StandardAttributes:
    def __init__(
        self,
        *,
        address: typing.Optional[StandardAttribute] = None,
        birthdate: typing.Optional[StandardAttribute] = None,
        email: typing.Optional[StandardAttribute] = None,
        family_name: typing.Optional[StandardAttribute] = None,
        fullname: typing.Optional[StandardAttribute] = None,
        gender: typing.Optional[StandardAttribute] = None,
        given_name: typing.Optional[StandardAttribute] = None,
        last_update_time: typing.Optional[StandardAttribute] = None,
        locale: typing.Optional[StandardAttribute] = None,
        middle_name: typing.Optional[StandardAttribute] = None,
        nickname: typing.Optional[StandardAttribute] = None,
        phone_number: typing.Optional[StandardAttribute] = None,
        preferred_username: typing.Optional[StandardAttribute] = None,
        profile_page: typing.Optional[StandardAttribute] = None,
        profile_picture: typing.Optional[StandardAttribute] = None,
        timezone: typing.Optional[StandardAttribute] = None,
        website: typing.Optional[StandardAttribute] = None,
    ) -> None:
        """The set of standard attributes that can be marked as required or mutable.

        :param address: The user's postal address. Default: - see the defaults under ``StandardAttribute``
        :param birthdate: The user's birthday, represented as an ISO 8601:2004 format. Default: - see the defaults under ``StandardAttribute``
        :param email: The user's e-mail address, represented as an RFC 5322 [RFC5322] addr-spec. Default: - see the defaults under ``StandardAttribute``
        :param family_name: The surname or last name of the user. Default: - see the defaults under ``StandardAttribute``
        :param fullname: The user's full name in displayable form, including all name parts, titles and suffixes. Default: - see the defaults under ``StandardAttribute``
        :param gender: The user's gender. Default: - see the defaults under ``StandardAttribute``
        :param given_name: The user's first name or give name. Default: - see the defaults under ``StandardAttribute``
        :param last_update_time: The time, the user's information was last updated. Default: - see the defaults under ``StandardAttribute``
        :param locale: The user's locale, represented as a BCP47 [RFC5646] language tag. Default: - see the defaults under ``StandardAttribute``
        :param middle_name: The user's middle name. Default: - see the defaults under ``StandardAttribute``
        :param nickname: The user's nickname or casual name. Default: - see the defaults under ``StandardAttribute``
        :param phone_number: The user's telephone number. Default: - see the defaults under ``StandardAttribute``
        :param preferred_username: The user's preffered username, different from the immutable user name. Default: - see the defaults under ``StandardAttribute``
        :param profile_page: The URL to the user's profile page. Default: - see the defaults under ``StandardAttribute``
        :param profile_picture: The URL to the user's profile picture. Default: - see the defaults under ``StandardAttribute``
        :param timezone: The user's time zone. Default: - see the defaults under ``StandardAttribute``
        :param website: The URL to the user's web page or blog. Default: - see the defaults under ``StandardAttribute``

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#cognito-user-pools-standard-attributes
        """
        if isinstance(address, dict):
            address = StandardAttribute(**address)
        if isinstance(birthdate, dict):
            birthdate = StandardAttribute(**birthdate)
        if isinstance(email, dict):
            email = StandardAttribute(**email)
        if isinstance(family_name, dict):
            family_name = StandardAttribute(**family_name)
        if isinstance(fullname, dict):
            fullname = StandardAttribute(**fullname)
        if isinstance(gender, dict):
            gender = StandardAttribute(**gender)
        if isinstance(given_name, dict):
            given_name = StandardAttribute(**given_name)
        if isinstance(last_update_time, dict):
            last_update_time = StandardAttribute(**last_update_time)
        if isinstance(locale, dict):
            locale = StandardAttribute(**locale)
        if isinstance(middle_name, dict):
            middle_name = StandardAttribute(**middle_name)
        if isinstance(nickname, dict):
            nickname = StandardAttribute(**nickname)
        if isinstance(phone_number, dict):
            phone_number = StandardAttribute(**phone_number)
        if isinstance(preferred_username, dict):
            preferred_username = StandardAttribute(**preferred_username)
        if isinstance(profile_page, dict):
            profile_page = StandardAttribute(**profile_page)
        if isinstance(profile_picture, dict):
            profile_picture = StandardAttribute(**profile_picture)
        if isinstance(timezone, dict):
            timezone = StandardAttribute(**timezone)
        if isinstance(website, dict):
            website = StandardAttribute(**website)
        self._values: typing.Dict[str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if birthdate is not None:
            self._values["birthdate"] = birthdate
        if email is not None:
            self._values["email"] = email
        if family_name is not None:
            self._values["family_name"] = family_name
        if fullname is not None:
            self._values["fullname"] = fullname
        if gender is not None:
            self._values["gender"] = gender
        if given_name is not None:
            self._values["given_name"] = given_name
        if last_update_time is not None:
            self._values["last_update_time"] = last_update_time
        if locale is not None:
            self._values["locale"] = locale
        if middle_name is not None:
            self._values["middle_name"] = middle_name
        if nickname is not None:
            self._values["nickname"] = nickname
        if phone_number is not None:
            self._values["phone_number"] = phone_number
        if preferred_username is not None:
            self._values["preferred_username"] = preferred_username
        if profile_page is not None:
            self._values["profile_page"] = profile_page
        if profile_picture is not None:
            self._values["profile_picture"] = profile_picture
        if timezone is not None:
            self._values["timezone"] = timezone
        if website is not None:
            self._values["website"] = website

    @builtins.property
    def address(self) -> typing.Optional[StandardAttribute]:
        """The user's postal address.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("address")
        return result

    @builtins.property
    def birthdate(self) -> typing.Optional[StandardAttribute]:
        """The user's birthday, represented as an ISO 8601:2004 format.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("birthdate")
        return result

    @builtins.property
    def email(self) -> typing.Optional[StandardAttribute]:
        """The user's e-mail address, represented as an RFC 5322 [RFC5322] addr-spec.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("email")
        return result

    @builtins.property
    def family_name(self) -> typing.Optional[StandardAttribute]:
        """The surname or last name of the user.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("family_name")
        return result

    @builtins.property
    def fullname(self) -> typing.Optional[StandardAttribute]:
        """The user's full name in displayable form, including all name parts, titles and suffixes.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("fullname")
        return result

    @builtins.property
    def gender(self) -> typing.Optional[StandardAttribute]:
        """The user's gender.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("gender")
        return result

    @builtins.property
    def given_name(self) -> typing.Optional[StandardAttribute]:
        """The user's first name or give name.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("given_name")
        return result

    @builtins.property
    def last_update_time(self) -> typing.Optional[StandardAttribute]:
        """The time, the user's information was last updated.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("last_update_time")
        return result

    @builtins.property
    def locale(self) -> typing.Optional[StandardAttribute]:
        """The user's locale, represented as a BCP47 [RFC5646] language tag.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("locale")
        return result

    @builtins.property
    def middle_name(self) -> typing.Optional[StandardAttribute]:
        """The user's middle name.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("middle_name")
        return result

    @builtins.property
    def nickname(self) -> typing.Optional[StandardAttribute]:
        """The user's nickname or casual name.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("nickname")
        return result

    @builtins.property
    def phone_number(self) -> typing.Optional[StandardAttribute]:
        """The user's telephone number.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("phone_number")
        return result

    @builtins.property
    def preferred_username(self) -> typing.Optional[StandardAttribute]:
        """The user's preffered username, different from the immutable user name.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("preferred_username")
        return result

    @builtins.property
    def profile_page(self) -> typing.Optional[StandardAttribute]:
        """The URL to the user's profile page.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("profile_page")
        return result

    @builtins.property
    def profile_picture(self) -> typing.Optional[StandardAttribute]:
        """The URL to the user's profile picture.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("profile_picture")
        return result

    @builtins.property
    def timezone(self) -> typing.Optional[StandardAttribute]:
        """The user's time zone.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("timezone")
        return result

    @builtins.property
    def website(self) -> typing.Optional[StandardAttribute]:
        """The URL to the user's web page or blog.

        :default: - see the defaults under ``StandardAttribute``
        """
        result = self._values.get("website")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICustomAttribute)
class StringAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.StringAttribute",
):
    """The String custom attribute type."""

    def __init__(
        self,
        *,
        max_len: typing.Optional[jsii.Number] = None,
        min_len: typing.Optional[jsii.Number] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param max_len: Maximum length of this attribute. Default: 2048
        :param min_len: Minimum length of this attribute. Default: 0
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        """
        props = StringAttributeProps(max_len=max_len, min_len=min_len, mutable=mutable)

        jsii.create(StringAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> CustomAttributeConfig:
        """Bind this custom attribute type to the values as expected by CloudFormation."""
        return jsii.invoke(self, "bind", [])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.StringAttributeConstraints",
    jsii_struct_bases=[],
    name_mapping={"max_len": "maxLen", "min_len": "minLen"},
)
class StringAttributeConstraints:
    def __init__(
        self,
        *,
        max_len: typing.Optional[jsii.Number] = None,
        min_len: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Constraints that can be applied to a custom attribute of string type.

        :param max_len: Maximum length of this attribute. Default: 2048
        :param min_len: Minimum length of this attribute. Default: 0
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if max_len is not None:
            self._values["max_len"] = max_len
        if min_len is not None:
            self._values["min_len"] = min_len

    @builtins.property
    def max_len(self) -> typing.Optional[jsii.Number]:
        """Maximum length of this attribute.

        :default: 2048
        """
        result = self._values.get("max_len")
        return result

    @builtins.property
    def min_len(self) -> typing.Optional[jsii.Number]:
        """Minimum length of this attribute.

        :default: 0
        """
        result = self._values.get("min_len")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringAttributeConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.StringAttributeProps",
    jsii_struct_bases=[StringAttributeConstraints, CustomAttributeProps],
    name_mapping={"max_len": "maxLen", "min_len": "minLen", "mutable": "mutable"},
)
class StringAttributeProps(StringAttributeConstraints, CustomAttributeProps):
    def __init__(
        self,
        *,
        max_len: typing.Optional[jsii.Number] = None,
        min_len: typing.Optional[jsii.Number] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Props for constructing a StringAttr.

        :param max_len: Maximum length of this attribute. Default: 2048
        :param min_len: Minimum length of this attribute. Default: 0
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if max_len is not None:
            self._values["max_len"] = max_len
        if min_len is not None:
            self._values["min_len"] = min_len
        if mutable is not None:
            self._values["mutable"] = mutable

    @builtins.property
    def max_len(self) -> typing.Optional[jsii.Number]:
        """Maximum length of this attribute.

        :default: 2048
        """
        result = self._values.get("max_len")
        return result

    @builtins.property
    def min_len(self) -> typing.Optional[jsii.Number]:
        """Minimum length of this attribute.

        :default: 0
        """
        result = self._values.get("min_len")
        return result

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        """Specifies whether the value of the attribute can be changed.

        For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true.
        Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider.
        If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute.

        :default: false
        """
        result = self._values.get("mutable")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringAttributeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserInvitationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "email_body": "emailBody",
        "email_subject": "emailSubject",
        "sms_message": "smsMessage",
    },
)
class UserInvitationConfig:
    def __init__(
        self,
        *,
        email_body: typing.Optional[builtins.str] = None,
        email_subject: typing.Optional[builtins.str] = None,
        sms_message: typing.Optional[builtins.str] = None,
    ) -> None:
        """User pool configuration when administrators sign users up.

        :param email_body: The template to the email body that is sent to the user when an administrator signs them up to the user pool. Default: 'Your username is {username} and temporary password is {####}.'
        :param email_subject: The template to the email subject that is sent to the user when an administrator signs them up to the user pool. Default: 'Your temporary password'
        :param sms_message: The template to the SMS message that is sent to the user when an administrator signs them up to the user pool. Default: 'Your username is {username} and temporary password is {####}'
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if email_body is not None:
            self._values["email_body"] = email_body
        if email_subject is not None:
            self._values["email_subject"] = email_subject
        if sms_message is not None:
            self._values["sms_message"] = sms_message

    @builtins.property
    def email_body(self) -> typing.Optional[builtins.str]:
        """The template to the email body that is sent to the user when an administrator signs them up to the user pool.

        :default: 'Your username is {username} and temporary password is {####}.'
        """
        result = self._values.get("email_body")
        return result

    @builtins.property
    def email_subject(self) -> typing.Optional[builtins.str]:
        """The template to the email subject that is sent to the user when an administrator signs them up to the user pool.

        :default: 'Your temporary password'
        """
        result = self._values.get("email_subject")
        return result

    @builtins.property
    def sms_message(self) -> typing.Optional[builtins.str]:
        """The template to the SMS message that is sent to the user when an administrator signs them up to the user pool.

        :default: 'Your username is {username} and temporary password is {####}'
        """
        result = self._values.get("sms_message")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserInvitationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IUserPool)
class UserPool(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPool",
):
    """Define a Cognito User Pool."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account_recovery: typing.Optional[AccountRecovery] = None,
        auto_verify: typing.Optional[AutoVerifiedAttrs] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, ICustomAttribute]] = None,
        email_settings: typing.Optional[EmailSettings] = None,
        enable_sms_role: typing.Optional[builtins.bool] = None,
        lambda_triggers: typing.Optional["UserPoolTriggers"] = None,
        mfa: typing.Optional[Mfa] = None,
        mfa_second_factor: typing.Optional[MfaSecondFactor] = None,
        password_policy: typing.Optional[PasswordPolicy] = None,
        self_sign_up_enabled: typing.Optional[builtins.bool] = None,
        sign_in_aliases: typing.Optional[SignInAliases] = None,
        sign_in_case_sensitive: typing.Optional[builtins.bool] = None,
        sms_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        sms_role_external_id: typing.Optional[builtins.str] = None,
        standard_attributes: typing.Optional[StandardAttributes] = None,
        user_invitation: typing.Optional[UserInvitationConfig] = None,
        user_pool_name: typing.Optional[builtins.str] = None,
        user_verification: typing.Optional["UserVerificationConfig"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param account_recovery: How will a user be able to recover their account? Default: AccountRecovery.PHONE_WITHOUT_MFA_AND_EMAIL
        :param auto_verify: Attributes which Cognito will look to verify automatically upon user sign up. EMAIL and PHONE are the only available options. Default: - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default. If absent, no attributes will be auto-verified.
        :param custom_attributes: Define a set of custom attributes that can be configured for each user in the user pool. Default: - No custom attributes.
        :param email_settings: Email settings for a user pool. Default: - see defaults on each property of EmailSettings.
        :param enable_sms_role: Setting this would explicitly enable or disable SMS role creation. When left unspecified, CDK will determine based on other properties if a role is needed or not. Default: - CDK will determine based on other properties of the user pool if an SMS role should be created or not.
        :param lambda_triggers: Lambda functions to use for supported Cognito triggers. Default: - No Lambda triggers.
        :param mfa: Configure whether users of this user pool can or are required use MFA to sign in. Default: Mfa.OFF
        :param mfa_second_factor: Configure the MFA types that users can use in this user pool. Ignored if ``mfa`` is set to ``OFF``. Default: - { sms: true, oneTimePassword: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``. { sms: false, oneTimePassword: false }, otherwise
        :param password_policy: Password policy for this user pool. Default: - see defaults on each property of PasswordPolicy.
        :param self_sign_up_enabled: Whether self sign up should be enabled. This can be further configured via the ``selfSignUp`` property. Default: false
        :param sign_in_aliases: Methods in which a user registers or signs in to a user pool. Allows either username with aliases OR sign in with email, phone, or both. Read the sections on usernames and aliases to learn more - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html To match with 'Option 1' in the above link, with a verified email, this property should be set to ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone number, this property should be set to ``{ email: true, phone: true }``. Default: { username: true }
        :param sign_in_case_sensitive: Whether sign-in aliases should be evaluated with case sensitivity. For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``. Default: true
        :param sms_role: The IAM role that Cognito will assume while sending SMS messages. Default: - a new IAM role is created
        :param sms_role_external_id: The 'ExternalId' that Cognito service must using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional. Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html This property will be ignored if ``smsRole`` is not specified. Default: - No external id will be configured
        :param standard_attributes: The set of attributes that are required for every user in the user pool. Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html Default: - All standard attributes are optional and mutable.
        :param user_invitation: Configuration around admins signing up users into a user pool. Default: - see defaults in UserInvitationConfig
        :param user_pool_name: Name of the user pool. Default: - automatically generated name by CloudFormation at deploy time
        :param user_verification: Configuration around users signing themselves up to the user pool. Enable or disable self sign-up via the ``selfSignUpEnabled`` property. Default: - see defaults in UserVerificationConfig
        """
        props = UserPoolProps(
            account_recovery=account_recovery,
            auto_verify=auto_verify,
            custom_attributes=custom_attributes,
            email_settings=email_settings,
            enable_sms_role=enable_sms_role,
            lambda_triggers=lambda_triggers,
            mfa=mfa,
            mfa_second_factor=mfa_second_factor,
            password_policy=password_policy,
            self_sign_up_enabled=self_sign_up_enabled,
            sign_in_aliases=sign_in_aliases,
            sign_in_case_sensitive=sign_in_case_sensitive,
            sms_role=sms_role,
            sms_role_external_id=sms_role_external_id,
            standard_attributes=standard_attributes,
            user_invitation=user_invitation,
            user_pool_name=user_pool_name,
            user_verification=user_verification,
        )

        jsii.create(UserPool, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserPoolArn")
    @builtins.classmethod
    def from_user_pool_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        user_pool_arn: builtins.str,
    ) -> IUserPool:
        """Import an existing user pool based on its ARN.

        :param scope: -
        :param id: -
        :param user_pool_arn: -
        """
        return jsii.sinvoke(cls, "fromUserPoolArn", [scope, id, user_pool_arn])

    @jsii.member(jsii_name="fromUserPoolId")
    @builtins.classmethod
    def from_user_pool_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        user_pool_id: builtins.str,
    ) -> IUserPool:
        """Import an existing user pool based on its id.

        :param scope: -
        :param id: -
        :param user_pool_id: -
        """
        return jsii.sinvoke(cls, "fromUserPoolId", [scope, id, user_pool_id])

    @jsii.member(jsii_name="addClient")
    def add_client(
        self,
        id: builtins.str,
        *,
        auth_flows: typing.Optional[AuthFlow] = None,
        disable_o_auth: typing.Optional[builtins.bool] = None,
        generate_secret: typing.Optional[builtins.bool] = None,
        o_auth: typing.Optional[OAuthSettings] = None,
        prevent_user_existence_errors: typing.Optional[builtins.bool] = None,
        supported_identity_providers: typing.Optional[typing.List["UserPoolClientIdentityProvider"]] = None,
        user_pool_client_name: typing.Optional[builtins.str] = None,
    ) -> "UserPoolClient":
        """Add a new app client to this user pool.

        :param id: -
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param disable_o_auth: Turns off all OAuth interactions for this client. Default: false
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. An error is thrown when this is specified and ``disableOAuth`` is set. Default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param supported_identity_providers: The list of identity providers that users should be able to use to sign in using this client. Default: - supports all identity providers that are registered with the user pool. If the user pool and/or identity providers are imported, either specify this option explicitly or ensure that the identity providers are registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name
        """
        options = UserPoolClientOptions(
            auth_flows=auth_flows,
            disable_o_auth=disable_o_auth,
            generate_secret=generate_secret,
            o_auth=o_auth,
            prevent_user_existence_errors=prevent_user_existence_errors,
            supported_identity_providers=supported_identity_providers,
            user_pool_client_name=user_pool_client_name,
        )

        return jsii.invoke(self, "addClient", [id, options])

    @jsii.member(jsii_name="addDomain")
    def add_domain(
        self,
        id: builtins.str,
        *,
        cognito_domain: typing.Optional[CognitoDomainOptions] = None,
        custom_domain: typing.Optional[CustomDomainOptions] = None,
    ) -> "UserPoolDomain":
        """Associate a domain to this user pool.

        :param id: -
        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.
        """
        options = UserPoolDomainOptions(
            cognito_domain=cognito_domain, custom_domain=custom_domain
        )

        return jsii.invoke(self, "addDomain", [id, options])

    @jsii.member(jsii_name="addResourceServer")
    def add_resource_server(
        self,
        id: builtins.str,
        *,
        identifier: builtins.str,
        scopes: typing.Optional[typing.List[ResourceServerScope]] = None,
        user_pool_resource_server_name: typing.Optional[builtins.str] = None,
    ) -> "UserPoolResourceServer":
        """Add a new resource server to this user pool.

        :param id: -
        :param identifier: A unique resource server identifier for the resource server.
        :param scopes: Oauth scopes. Default: - No scopes will be added
        :param user_pool_resource_server_name: A friendly name for the resource server. Default: - same as ``identifier``
        """
        options = UserPoolResourceServerOptions(
            identifier=identifier,
            scopes=scopes,
            user_pool_resource_server_name=user_pool_resource_server_name,
        )

        return jsii.invoke(self, "addResourceServer", [id, options])

    @jsii.member(jsii_name="addTrigger")
    def add_trigger(
        self,
        operation: "UserPoolOperation",
        fn: aws_cdk.aws_lambda.IFunction,
    ) -> None:
        """Add a lambda trigger to a user pool operation.

        :param operation: -
        :param fn: -

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
        """
        return jsii.invoke(self, "addTrigger", [operation, fn])

    @jsii.member(jsii_name="registerIdentityProvider")
    def register_identity_provider(self, provider: IUserPoolIdentityProvider) -> None:
        """Register an identity provider with this user pool.

        :param provider: -
        """
        return jsii.invoke(self, "registerIdentityProvider", [provider])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identityProviders")
    def identity_providers(self) -> typing.List[IUserPoolIdentityProvider]:
        """Get all identity providers registered with this user pool."""
        return jsii.get(self, "identityProviders")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolArn")
    def user_pool_arn(self) -> builtins.str:
        """The ARN of the user pool."""
        return jsii.get(self, "userPoolArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        """The physical ID of this user pool resource."""
        return jsii.get(self, "userPoolId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolProviderName")
    def user_pool_provider_name(self) -> builtins.str:
        """User pool provider name.

        :attribute: true
        """
        return jsii.get(self, "userPoolProviderName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolProviderUrl")
    def user_pool_provider_url(self) -> builtins.str:
        """User pool provider URL.

        :attribute: true
        """
        return jsii.get(self, "userPoolProviderUrl")


@jsii.implements(IUserPoolClient)
class UserPoolClient(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolClient",
):
    """Define a UserPool App Client."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        user_pool: IUserPool,
        auth_flows: typing.Optional[AuthFlow] = None,
        disable_o_auth: typing.Optional[builtins.bool] = None,
        generate_secret: typing.Optional[builtins.bool] = None,
        o_auth: typing.Optional[OAuthSettings] = None,
        prevent_user_existence_errors: typing.Optional[builtins.bool] = None,
        supported_identity_providers: typing.Optional[typing.List["UserPoolClientIdentityProvider"]] = None,
        user_pool_client_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param user_pool: The UserPool resource this client will have access to.
        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param disable_o_auth: Turns off all OAuth interactions for this client. Default: false
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. An error is thrown when this is specified and ``disableOAuth`` is set. Default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param supported_identity_providers: The list of identity providers that users should be able to use to sign in using this client. Default: - supports all identity providers that are registered with the user pool. If the user pool and/or identity providers are imported, either specify this option explicitly or ensure that the identity providers are registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name
        """
        props = UserPoolClientProps(
            user_pool=user_pool,
            auth_flows=auth_flows,
            disable_o_auth=disable_o_auth,
            generate_secret=generate_secret,
            o_auth=o_auth,
            prevent_user_existence_errors=prevent_user_existence_errors,
            supported_identity_providers=supported_identity_providers,
            user_pool_client_name=user_pool_client_name,
        )

        jsii.create(UserPoolClient, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserPoolClientId")
    @builtins.classmethod
    def from_user_pool_client_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        user_pool_client_id: builtins.str,
    ) -> IUserPoolClient:
        """Import a user pool client given its id.

        :param scope: -
        :param id: -
        :param user_pool_client_id: -
        """
        return jsii.sinvoke(cls, "fromUserPoolClientId", [scope, id, user_pool_client_id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="oAuthFlows")
    def o_auth_flows(self) -> OAuthFlows:
        """The OAuth flows enabled for this client."""
        return jsii.get(self, "oAuthFlows")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolClientId")
    def user_pool_client_id(self) -> builtins.str:
        """Name of the application client."""
        return jsii.get(self, "userPoolClientId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolClientName")
    def user_pool_client_name(self) -> builtins.str:
        """The client name that was specified via the ``userPoolClientName`` property during initialization, throws an error otherwise."""
        return jsii.get(self, "userPoolClientName")


class UserPoolClientIdentityProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolClientIdentityProvider",
):
    """Identity providers supported by the UserPoolClient."""

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, name: builtins.str) -> "UserPoolClientIdentityProvider":
        """Specify a provider not yet supported by the CDK.

        :param name: name of the identity provider as recognized by CloudFormation property ``SupportedIdentityProviders``.
        """
        return jsii.sinvoke(cls, "custom", [name])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON")
    def AMAZON(cls) -> "UserPoolClientIdentityProvider":
        """Allow users to sign in using 'Login With Amazon'.

        A ``UserPoolIdentityProviderAmazon`` must be attached to the user pool.
        """
        return jsii.sget(cls, "AMAZON")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="COGNITO")
    def COGNITO(cls) -> "UserPoolClientIdentityProvider":
        """Allow users to sign in directly as a user of the User Pool."""
        return jsii.sget(cls, "COGNITO")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="FACEBOOK")
    def FACEBOOK(cls) -> "UserPoolClientIdentityProvider":
        """Allow users to sign in using 'Facebook Login'.

        A ``UserPoolIdentityProviderFacebook`` must be attached to the user pool.
        """
        return jsii.sget(cls, "FACEBOOK")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="GOOGLE")
    def GOOGLE(cls) -> "UserPoolClientIdentityProvider":
        """Allow users to sign in using 'Google Login'.

        A ``UserPoolIdentityProviderGoogle`` must be attached to the user pool.
        """
        return jsii.sget(cls, "GOOGLE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """The name of the identity provider as recognized by CloudFormation property ``SupportedIdentityProviders``."""
        return jsii.get(self, "name")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolClientOptions",
    jsii_struct_bases=[],
    name_mapping={
        "auth_flows": "authFlows",
        "disable_o_auth": "disableOAuth",
        "generate_secret": "generateSecret",
        "o_auth": "oAuth",
        "prevent_user_existence_errors": "preventUserExistenceErrors",
        "supported_identity_providers": "supportedIdentityProviders",
        "user_pool_client_name": "userPoolClientName",
    },
)
class UserPoolClientOptions:
    def __init__(
        self,
        *,
        auth_flows: typing.Optional[AuthFlow] = None,
        disable_o_auth: typing.Optional[builtins.bool] = None,
        generate_secret: typing.Optional[builtins.bool] = None,
        o_auth: typing.Optional[OAuthSettings] = None,
        prevent_user_existence_errors: typing.Optional[builtins.bool] = None,
        supported_identity_providers: typing.Optional[typing.List[UserPoolClientIdentityProvider]] = None,
        user_pool_client_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options to create a UserPoolClient.

        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param disable_o_auth: Turns off all OAuth interactions for this client. Default: false
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. An error is thrown when this is specified and ``disableOAuth`` is set. Default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param supported_identity_providers: The list of identity providers that users should be able to use to sign in using this client. Default: - supports all identity providers that are registered with the user pool. If the user pool and/or identity providers are imported, either specify this option explicitly or ensure that the identity providers are registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name
        """
        if isinstance(auth_flows, dict):
            auth_flows = AuthFlow(**auth_flows)
        if isinstance(o_auth, dict):
            o_auth = OAuthSettings(**o_auth)
        self._values: typing.Dict[str, typing.Any] = {}
        if auth_flows is not None:
            self._values["auth_flows"] = auth_flows
        if disable_o_auth is not None:
            self._values["disable_o_auth"] = disable_o_auth
        if generate_secret is not None:
            self._values["generate_secret"] = generate_secret
        if o_auth is not None:
            self._values["o_auth"] = o_auth
        if prevent_user_existence_errors is not None:
            self._values["prevent_user_existence_errors"] = prevent_user_existence_errors
        if supported_identity_providers is not None:
            self._values["supported_identity_providers"] = supported_identity_providers
        if user_pool_client_name is not None:
            self._values["user_pool_client_name"] = user_pool_client_name

    @builtins.property
    def auth_flows(self) -> typing.Optional[AuthFlow]:
        """The set of OAuth authentication flows to enable on the client.

        :default: - all auth flows disabled

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html
        """
        result = self._values.get("auth_flows")
        return result

    @builtins.property
    def disable_o_auth(self) -> typing.Optional[builtins.bool]:
        """Turns off all OAuth interactions for this client.

        :default: false
        """
        result = self._values.get("disable_o_auth")
        return result

    @builtins.property
    def generate_secret(self) -> typing.Optional[builtins.bool]:
        """Whether to generate a client secret.

        :default: false
        """
        result = self._values.get("generate_secret")
        return result

    @builtins.property
    def o_auth(self) -> typing.Optional[OAuthSettings]:
        """OAuth settings for this to client to interact with the app.

        An error is thrown when this is specified and ``disableOAuth`` is set.

        :default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        """
        result = self._values.get("o_auth")
        return result

    @builtins.property
    def prevent_user_existence_errors(self) -> typing.Optional[builtins.bool]:
        """Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence.

        :default: true for new stacks

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-managing-errors.html
        """
        result = self._values.get("prevent_user_existence_errors")
        return result

    @builtins.property
    def supported_identity_providers(
        self,
    ) -> typing.Optional[typing.List[UserPoolClientIdentityProvider]]:
        """The list of identity providers that users should be able to use to sign in using this client.

        :default:

        - supports all identity providers that are registered with the user pool. If the user pool and/or
        identity providers are imported, either specify this option explicitly or ensure that the identity providers are
        registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        """
        result = self._values.get("supported_identity_providers")
        return result

    @builtins.property
    def user_pool_client_name(self) -> typing.Optional[builtins.str]:
        """Name of the application client.

        :default: - cloudformation generated name
        """
        result = self._values.get("user_pool_client_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolClientOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolClientProps",
    jsii_struct_bases=[UserPoolClientOptions],
    name_mapping={
        "auth_flows": "authFlows",
        "disable_o_auth": "disableOAuth",
        "generate_secret": "generateSecret",
        "o_auth": "oAuth",
        "prevent_user_existence_errors": "preventUserExistenceErrors",
        "supported_identity_providers": "supportedIdentityProviders",
        "user_pool_client_name": "userPoolClientName",
        "user_pool": "userPool",
    },
)
class UserPoolClientProps(UserPoolClientOptions):
    def __init__(
        self,
        *,
        auth_flows: typing.Optional[AuthFlow] = None,
        disable_o_auth: typing.Optional[builtins.bool] = None,
        generate_secret: typing.Optional[builtins.bool] = None,
        o_auth: typing.Optional[OAuthSettings] = None,
        prevent_user_existence_errors: typing.Optional[builtins.bool] = None,
        supported_identity_providers: typing.Optional[typing.List[UserPoolClientIdentityProvider]] = None,
        user_pool_client_name: typing.Optional[builtins.str] = None,
        user_pool: IUserPool,
    ) -> None:
        """Properties for the UserPoolClient construct.

        :param auth_flows: The set of OAuth authentication flows to enable on the client. Default: - all auth flows disabled
        :param disable_o_auth: Turns off all OAuth interactions for this client. Default: false
        :param generate_secret: Whether to generate a client secret. Default: false
        :param o_auth: OAuth settings for this to client to interact with the app. An error is thrown when this is specified and ``disableOAuth`` is set. Default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        :param prevent_user_existence_errors: Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence. Default: true for new stacks
        :param supported_identity_providers: The list of identity providers that users should be able to use to sign in using this client. Default: - supports all identity providers that are registered with the user pool. If the user pool and/or identity providers are imported, either specify this option explicitly or ensure that the identity providers are registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        :param user_pool_client_name: Name of the application client. Default: - cloudformation generated name
        :param user_pool: The UserPool resource this client will have access to.
        """
        if isinstance(auth_flows, dict):
            auth_flows = AuthFlow(**auth_flows)
        if isinstance(o_auth, dict):
            o_auth = OAuthSettings(**o_auth)
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool": user_pool,
        }
        if auth_flows is not None:
            self._values["auth_flows"] = auth_flows
        if disable_o_auth is not None:
            self._values["disable_o_auth"] = disable_o_auth
        if generate_secret is not None:
            self._values["generate_secret"] = generate_secret
        if o_auth is not None:
            self._values["o_auth"] = o_auth
        if prevent_user_existence_errors is not None:
            self._values["prevent_user_existence_errors"] = prevent_user_existence_errors
        if supported_identity_providers is not None:
            self._values["supported_identity_providers"] = supported_identity_providers
        if user_pool_client_name is not None:
            self._values["user_pool_client_name"] = user_pool_client_name

    @builtins.property
    def auth_flows(self) -> typing.Optional[AuthFlow]:
        """The set of OAuth authentication flows to enable on the client.

        :default: - all auth flows disabled

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html
        """
        result = self._values.get("auth_flows")
        return result

    @builtins.property
    def disable_o_auth(self) -> typing.Optional[builtins.bool]:
        """Turns off all OAuth interactions for this client.

        :default: false
        """
        result = self._values.get("disable_o_auth")
        return result

    @builtins.property
    def generate_secret(self) -> typing.Optional[builtins.bool]:
        """Whether to generate a client secret.

        :default: false
        """
        result = self._values.get("generate_secret")
        return result

    @builtins.property
    def o_auth(self) -> typing.Optional[OAuthSettings]:
        """OAuth settings for this to client to interact with the app.

        An error is thrown when this is specified and ``disableOAuth`` is set.

        :default: - see defaults in ``OAuthSettings``. meaningless if ``disableOAuth`` is set.
        """
        result = self._values.get("o_auth")
        return result

    @builtins.property
    def prevent_user_existence_errors(self) -> typing.Optional[builtins.bool]:
        """Whether Cognito returns a UserNotFoundException exception when the user does not exist in the user pool (false), or whether it returns another type of error that doesn't reveal the user's absence.

        :default: true for new stacks

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-managing-errors.html
        """
        result = self._values.get("prevent_user_existence_errors")
        return result

    @builtins.property
    def supported_identity_providers(
        self,
    ) -> typing.Optional[typing.List[UserPoolClientIdentityProvider]]:
        """The list of identity providers that users should be able to use to sign in using this client.

        :default:

        - supports all identity providers that are registered with the user pool. If the user pool and/or
        identity providers are imported, either specify this option explicitly or ensure that the identity providers are
        registered with the user pool using the ``UserPool.registerIdentityProvider()`` API.
        """
        result = self._values.get("supported_identity_providers")
        return result

    @builtins.property
    def user_pool_client_name(self) -> typing.Optional[builtins.str]:
        """Name of the application client.

        :default: - cloudformation generated name
        """
        result = self._values.get("user_pool_client_name")
        return result

    @builtins.property
    def user_pool(self) -> IUserPool:
        """The UserPool resource this client will have access to."""
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolClientProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IUserPoolDomain)
class UserPoolDomain(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolDomain",
):
    """Define a user pool domain."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        user_pool: IUserPool,
        cognito_domain: typing.Optional[CognitoDomainOptions] = None,
        custom_domain: typing.Optional[CustomDomainOptions] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param user_pool: The user pool to which this domain should be associated.
        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.
        """
        props = UserPoolDomainProps(
            user_pool=user_pool,
            cognito_domain=cognito_domain,
            custom_domain=custom_domain,
        )

        jsii.create(UserPoolDomain, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainName")
    @builtins.classmethod
    def from_domain_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        user_pool_domain_name: builtins.str,
    ) -> IUserPoolDomain:
        """Import a UserPoolDomain given its domain name.

        :param scope: -
        :param id: -
        :param user_pool_domain_name: -
        """
        return jsii.sinvoke(cls, "fromDomainName", [scope, id, user_pool_domain_name])

    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        """The URL to the hosted UI associated with this domain."""
        return jsii.invoke(self, "baseUrl", [])

    @jsii.member(jsii_name="signInUrl")
    def sign_in_url(
        self,
        client: UserPoolClient,
        *,
        redirect_uri: builtins.str,
        sign_in_path: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """The URL to the sign in page in this domain using a specific UserPoolClient.

        :param client: [disable-awslint:ref-via-interface] the user pool client that the UI will use to interact with the UserPool.
        :param redirect_uri: Where to redirect to after sign in.
        :param sign_in_path: The path in the URI where the sign-in page is located. Default: '/login'
        """
        options = SignInUrlOptions(
            redirect_uri=redirect_uri, sign_in_path=sign_in_path
        )

        return jsii.invoke(self, "signInUrl", [client, options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cloudFrontDomainName")
    def cloud_front_domain_name(self) -> builtins.str:
        """The domain name of the CloudFront distribution associated with the user pool domain."""
        return jsii.get(self, "cloudFrontDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """The domain that was specified to be created.

        If ``customDomain`` was selected, this holds the full domain name that was specified.
        If the ``cognitoDomain`` was used, it contains the prefix to the Cognito hosted domain.
        """
        return jsii.get(self, "domainName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolDomainOptions",
    jsii_struct_bases=[],
    name_mapping={"cognito_domain": "cognitoDomain", "custom_domain": "customDomain"},
)
class UserPoolDomainOptions:
    def __init__(
        self,
        *,
        cognito_domain: typing.Optional[CognitoDomainOptions] = None,
        custom_domain: typing.Optional[CustomDomainOptions] = None,
    ) -> None:
        """Options to create a UserPoolDomain.

        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.
        """
        if isinstance(cognito_domain, dict):
            cognito_domain = CognitoDomainOptions(**cognito_domain)
        if isinstance(custom_domain, dict):
            custom_domain = CustomDomainOptions(**custom_domain)
        self._values: typing.Dict[str, typing.Any] = {}
        if cognito_domain is not None:
            self._values["cognito_domain"] = cognito_domain
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain

    @builtins.property
    def cognito_domain(self) -> typing.Optional[CognitoDomainOptions]:
        """Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        :default: - not set if ``customDomain`` is specified, otherwise, throws an error.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html
        """
        result = self._values.get("cognito_domain")
        return result

    @builtins.property
    def custom_domain(self) -> typing.Optional[CustomDomainOptions]:
        """Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        :default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html
        """
        result = self._values.get("custom_domain")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolDomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolDomainProps",
    jsii_struct_bases=[UserPoolDomainOptions],
    name_mapping={
        "cognito_domain": "cognitoDomain",
        "custom_domain": "customDomain",
        "user_pool": "userPool",
    },
)
class UserPoolDomainProps(UserPoolDomainOptions):
    def __init__(
        self,
        *,
        cognito_domain: typing.Optional[CognitoDomainOptions] = None,
        custom_domain: typing.Optional[CustomDomainOptions] = None,
        user_pool: IUserPool,
    ) -> None:
        """Props for UserPoolDomain construct.

        :param cognito_domain: Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``customDomain`` is specified, otherwise, throws an error.
        :param custom_domain: Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified. Default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.
        :param user_pool: The user pool to which this domain should be associated.
        """
        if isinstance(cognito_domain, dict):
            cognito_domain = CognitoDomainOptions(**cognito_domain)
        if isinstance(custom_domain, dict):
            custom_domain = CustomDomainOptions(**custom_domain)
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool": user_pool,
        }
        if cognito_domain is not None:
            self._values["cognito_domain"] = cognito_domain
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain

    @builtins.property
    def cognito_domain(self) -> typing.Optional[CognitoDomainOptions]:
        """Associate a cognito prefix domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        :default: - not set if ``customDomain`` is specified, otherwise, throws an error.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain-prefix.html
        """
        result = self._values.get("cognito_domain")
        return result

    @builtins.property
    def custom_domain(self) -> typing.Optional[CustomDomainOptions]:
        """Associate a custom domain with your user pool Either ``customDomain`` or ``cognitoDomain`` must be specified.

        :default: - not set if ``cognitoDomain`` is specified, otherwise, throws an error.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html
        """
        result = self._values.get("custom_domain")
        return result

    @builtins.property
    def user_pool(self) -> IUserPool:
        """The user pool to which this domain should be associated."""
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserPoolIdentityProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProvider",
):
    """User pool third-party identity providers."""

    @jsii.member(jsii_name="fromProviderName")
    @builtins.classmethod
    def from_provider_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        provider_name: builtins.str,
    ) -> IUserPoolIdentityProvider:
        """Import an existing UserPoolIdentityProvider.

        :param scope: -
        :param id: -
        :param provider_name: -
        """
        return jsii.sinvoke(cls, "fromProviderName", [scope, id, provider_name])


@jsii.implements(IUserPoolIdentityProvider)
class UserPoolIdentityProviderAmazon(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProviderAmazon",
):
    """Represents a identity provider that integrates with 'Login with Amazon'.

    :resource: AWS::Cognito::UserPoolIdentityProvider
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        scopes: typing.Optional[typing.List[builtins.str]] = None,
        user_pool: IUserPool,
        attribute_mapping: typing.Optional[AttributeMapping] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param client_id: The client id recognized by 'Login with Amazon' APIs.
        :param client_secret: The client secret to be accompanied with clientId for 'Login with Amazon' APIs to authenticate the client.
        :param scopes: The types of user profile data to obtain for the Amazon profile. Default: [ profile ]
        :param user_pool: The user pool to which this construct provides identities.
        :param attribute_mapping: Mapping attributes from the identity provider to standard and custom attributes of the user pool. Default: - no attribute mapping
        """
        props = UserPoolIdentityProviderAmazonProps(
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            user_pool=user_pool,
            attribute_mapping=attribute_mapping,
        )

        jsii.create(UserPoolIdentityProviderAmazon, self, [scope, id, props])

    @jsii.member(jsii_name="configureAttributeMapping")
    def _configure_attribute_mapping(self) -> typing.Any:
        return jsii.invoke(self, "configureAttributeMapping", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        """The primary identifier of this identity provider."""
        return jsii.get(self, "providerName")


@jsii.implements(IUserPoolIdentityProvider)
class UserPoolIdentityProviderFacebook(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProviderFacebook",
):
    """Represents a identity provider that integrates with 'Facebook Login'.

    :resource: AWS::Cognito::UserPoolIdentityProvider
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.List[builtins.str]] = None,
        user_pool: IUserPool,
        attribute_mapping: typing.Optional[AttributeMapping] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param client_id: The client id recognized by Facebook APIs.
        :param client_secret: The client secret to be accompanied with clientUd for Facebook to authenticate the client.
        :param api_version: The Facebook API version to use. Default: - to the oldest version supported by Facebook
        :param scopes: The list of facebook permissions to obtain for getting access to the Facebook profile. Default: [ public_profile ]
        :param user_pool: The user pool to which this construct provides identities.
        :param attribute_mapping: Mapping attributes from the identity provider to standard and custom attributes of the user pool. Default: - no attribute mapping
        """
        props = UserPoolIdentityProviderFacebookProps(
            client_id=client_id,
            client_secret=client_secret,
            api_version=api_version,
            scopes=scopes,
            user_pool=user_pool,
            attribute_mapping=attribute_mapping,
        )

        jsii.create(UserPoolIdentityProviderFacebook, self, [scope, id, props])

    @jsii.member(jsii_name="configureAttributeMapping")
    def _configure_attribute_mapping(self) -> typing.Any:
        return jsii.invoke(self, "configureAttributeMapping", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        """The primary identifier of this identity provider."""
        return jsii.get(self, "providerName")


@jsii.implements(IUserPoolIdentityProvider)
class UserPoolIdentityProviderGoogle(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProviderGoogle",
):
    """Represents a identity provider that integrates with 'Google'.

    :resource: AWS::Cognito::UserPoolIdentityProvider
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        scopes: typing.Optional[typing.List[builtins.str]] = None,
        user_pool: IUserPool,
        attribute_mapping: typing.Optional[AttributeMapping] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param client_id: The client id recognized by Google APIs.
        :param client_secret: The client secret to be accompanied with clientId for Google APIs to authenticate the client.
        :param scopes: The list of google permissions to obtain for getting access to the google profile. Default: [ profile ]
        :param user_pool: The user pool to which this construct provides identities.
        :param attribute_mapping: Mapping attributes from the identity provider to standard and custom attributes of the user pool. Default: - no attribute mapping
        """
        props = UserPoolIdentityProviderGoogleProps(
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            user_pool=user_pool,
            attribute_mapping=attribute_mapping,
        )

        jsii.create(UserPoolIdentityProviderGoogle, self, [scope, id, props])

    @jsii.member(jsii_name="configureAttributeMapping")
    def _configure_attribute_mapping(self) -> typing.Any:
        return jsii.invoke(self, "configureAttributeMapping", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        """The primary identifier of this identity provider."""
        return jsii.get(self, "providerName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProviderProps",
    jsii_struct_bases=[],
    name_mapping={"user_pool": "userPool", "attribute_mapping": "attributeMapping"},
)
class UserPoolIdentityProviderProps:
    def __init__(
        self,
        *,
        user_pool: IUserPool,
        attribute_mapping: typing.Optional[AttributeMapping] = None,
    ) -> None:
        """Properties to create a new instance of UserPoolIdentityProvider.

        :param user_pool: The user pool to which this construct provides identities.
        :param attribute_mapping: Mapping attributes from the identity provider to standard and custom attributes of the user pool. Default: - no attribute mapping
        """
        if isinstance(attribute_mapping, dict):
            attribute_mapping = AttributeMapping(**attribute_mapping)
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool": user_pool,
        }
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping

    @builtins.property
    def user_pool(self) -> IUserPool:
        """The user pool to which this construct provides identities."""
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return result

    @builtins.property
    def attribute_mapping(self) -> typing.Optional[AttributeMapping]:
        """Mapping attributes from the identity provider to standard and custom attributes of the user pool.

        :default: - no attribute mapping
        """
        result = self._values.get("attribute_mapping")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolIdentityProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserPoolOperation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolOperation",
):
    """User pool operations to which lambda triggers can be attached."""

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "UserPoolOperation":
        """A custom user pool operation.

        :param name: -
        """
        return jsii.sinvoke(cls, "of", [name])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CREATE_AUTH_CHALLENGE")
    def CREATE_AUTH_CHALLENGE(cls) -> "UserPoolOperation":
        """Creates a challenge in a custom auth flow.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-create-auth-challenge.html
        """
        return jsii.sget(cls, "CREATE_AUTH_CHALLENGE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CUSTOM_MESSAGE")
    def CUSTOM_MESSAGE(cls) -> "UserPoolOperation":
        """Advanced customization and localization of messages.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html
        """
        return jsii.sget(cls, "CUSTOM_MESSAGE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DEFINE_AUTH_CHALLENGE")
    def DEFINE_AUTH_CHALLENGE(cls) -> "UserPoolOperation":
        """Determines the next challenge in a custom auth flow.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-define-auth-challenge.html
        """
        return jsii.sget(cls, "DEFINE_AUTH_CHALLENGE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="POST_AUTHENTICATION")
    def POST_AUTHENTICATION(cls) -> "UserPoolOperation":
        """Event logging for custom analytics.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html
        """
        return jsii.sget(cls, "POST_AUTHENTICATION")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="POST_CONFIRMATION")
    def POST_CONFIRMATION(cls) -> "UserPoolOperation":
        """Custom welcome messages or event logging for custom analytics.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-confirmation.html
        """
        return jsii.sget(cls, "POST_CONFIRMATION")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PRE_AUTHENTICATION")
    def PRE_AUTHENTICATION(cls) -> "UserPoolOperation":
        """Custom validation to accept or deny the sign-in request.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html
        """
        return jsii.sget(cls, "PRE_AUTHENTICATION")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PRE_SIGN_UP")
    def PRE_SIGN_UP(cls) -> "UserPoolOperation":
        """Custom validation to accept or deny the sign-up request.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html
        """
        return jsii.sget(cls, "PRE_SIGN_UP")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="PRE_TOKEN_GENERATION")
    def PRE_TOKEN_GENERATION(cls) -> "UserPoolOperation":
        """Add or remove attributes in Id tokens.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html
        """
        return jsii.sget(cls, "PRE_TOKEN_GENERATION")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="USER_MIGRATION")
    def USER_MIGRATION(cls) -> "UserPoolOperation":
        """Migrate a user from an existing user directory to user pools.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html
        """
        return jsii.sget(cls, "USER_MIGRATION")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="VERIFY_AUTH_CHALLENGE_RESPONSE")
    def VERIFY_AUTH_CHALLENGE_RESPONSE(cls) -> "UserPoolOperation":
        """Determines if a response is correct in a custom auth flow.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-verify-auth-challenge-response.html
        """
        return jsii.sget(cls, "VERIFY_AUTH_CHALLENGE_RESPONSE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        """The key to use in ``CfnUserPool.LambdaConfigProperty``."""
        return jsii.get(self, "operationName")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_recovery": "accountRecovery",
        "auto_verify": "autoVerify",
        "custom_attributes": "customAttributes",
        "email_settings": "emailSettings",
        "enable_sms_role": "enableSmsRole",
        "lambda_triggers": "lambdaTriggers",
        "mfa": "mfa",
        "mfa_second_factor": "mfaSecondFactor",
        "password_policy": "passwordPolicy",
        "self_sign_up_enabled": "selfSignUpEnabled",
        "sign_in_aliases": "signInAliases",
        "sign_in_case_sensitive": "signInCaseSensitive",
        "sms_role": "smsRole",
        "sms_role_external_id": "smsRoleExternalId",
        "standard_attributes": "standardAttributes",
        "user_invitation": "userInvitation",
        "user_pool_name": "userPoolName",
        "user_verification": "userVerification",
    },
)
class UserPoolProps:
    def __init__(
        self,
        *,
        account_recovery: typing.Optional[AccountRecovery] = None,
        auto_verify: typing.Optional[AutoVerifiedAttrs] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, ICustomAttribute]] = None,
        email_settings: typing.Optional[EmailSettings] = None,
        enable_sms_role: typing.Optional[builtins.bool] = None,
        lambda_triggers: typing.Optional["UserPoolTriggers"] = None,
        mfa: typing.Optional[Mfa] = None,
        mfa_second_factor: typing.Optional[MfaSecondFactor] = None,
        password_policy: typing.Optional[PasswordPolicy] = None,
        self_sign_up_enabled: typing.Optional[builtins.bool] = None,
        sign_in_aliases: typing.Optional[SignInAliases] = None,
        sign_in_case_sensitive: typing.Optional[builtins.bool] = None,
        sms_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        sms_role_external_id: typing.Optional[builtins.str] = None,
        standard_attributes: typing.Optional[StandardAttributes] = None,
        user_invitation: typing.Optional[UserInvitationConfig] = None,
        user_pool_name: typing.Optional[builtins.str] = None,
        user_verification: typing.Optional["UserVerificationConfig"] = None,
    ) -> None:
        """Props for the UserPool construct.

        :param account_recovery: How will a user be able to recover their account? Default: AccountRecovery.PHONE_WITHOUT_MFA_AND_EMAIL
        :param auto_verify: Attributes which Cognito will look to verify automatically upon user sign up. EMAIL and PHONE are the only available options. Default: - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default. If absent, no attributes will be auto-verified.
        :param custom_attributes: Define a set of custom attributes that can be configured for each user in the user pool. Default: - No custom attributes.
        :param email_settings: Email settings for a user pool. Default: - see defaults on each property of EmailSettings.
        :param enable_sms_role: Setting this would explicitly enable or disable SMS role creation. When left unspecified, CDK will determine based on other properties if a role is needed or not. Default: - CDK will determine based on other properties of the user pool if an SMS role should be created or not.
        :param lambda_triggers: Lambda functions to use for supported Cognito triggers. Default: - No Lambda triggers.
        :param mfa: Configure whether users of this user pool can or are required use MFA to sign in. Default: Mfa.OFF
        :param mfa_second_factor: Configure the MFA types that users can use in this user pool. Ignored if ``mfa`` is set to ``OFF``. Default: - { sms: true, oneTimePassword: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``. { sms: false, oneTimePassword: false }, otherwise
        :param password_policy: Password policy for this user pool. Default: - see defaults on each property of PasswordPolicy.
        :param self_sign_up_enabled: Whether self sign up should be enabled. This can be further configured via the ``selfSignUp`` property. Default: false
        :param sign_in_aliases: Methods in which a user registers or signs in to a user pool. Allows either username with aliases OR sign in with email, phone, or both. Read the sections on usernames and aliases to learn more - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html To match with 'Option 1' in the above link, with a verified email, this property should be set to ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone number, this property should be set to ``{ email: true, phone: true }``. Default: { username: true }
        :param sign_in_case_sensitive: Whether sign-in aliases should be evaluated with case sensitivity. For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``. Default: true
        :param sms_role: The IAM role that Cognito will assume while sending SMS messages. Default: - a new IAM role is created
        :param sms_role_external_id: The 'ExternalId' that Cognito service must using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional. Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html This property will be ignored if ``smsRole`` is not specified. Default: - No external id will be configured
        :param standard_attributes: The set of attributes that are required for every user in the user pool. Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html Default: - All standard attributes are optional and mutable.
        :param user_invitation: Configuration around admins signing up users into a user pool. Default: - see defaults in UserInvitationConfig
        :param user_pool_name: Name of the user pool. Default: - automatically generated name by CloudFormation at deploy time
        :param user_verification: Configuration around users signing themselves up to the user pool. Enable or disable self sign-up via the ``selfSignUpEnabled`` property. Default: - see defaults in UserVerificationConfig
        """
        if isinstance(auto_verify, dict):
            auto_verify = AutoVerifiedAttrs(**auto_verify)
        if isinstance(email_settings, dict):
            email_settings = EmailSettings(**email_settings)
        if isinstance(lambda_triggers, dict):
            lambda_triggers = UserPoolTriggers(**lambda_triggers)
        if isinstance(mfa_second_factor, dict):
            mfa_second_factor = MfaSecondFactor(**mfa_second_factor)
        if isinstance(password_policy, dict):
            password_policy = PasswordPolicy(**password_policy)
        if isinstance(sign_in_aliases, dict):
            sign_in_aliases = SignInAliases(**sign_in_aliases)
        if isinstance(standard_attributes, dict):
            standard_attributes = StandardAttributes(**standard_attributes)
        if isinstance(user_invitation, dict):
            user_invitation = UserInvitationConfig(**user_invitation)
        if isinstance(user_verification, dict):
            user_verification = UserVerificationConfig(**user_verification)
        self._values: typing.Dict[str, typing.Any] = {}
        if account_recovery is not None:
            self._values["account_recovery"] = account_recovery
        if auto_verify is not None:
            self._values["auto_verify"] = auto_verify
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if email_settings is not None:
            self._values["email_settings"] = email_settings
        if enable_sms_role is not None:
            self._values["enable_sms_role"] = enable_sms_role
        if lambda_triggers is not None:
            self._values["lambda_triggers"] = lambda_triggers
        if mfa is not None:
            self._values["mfa"] = mfa
        if mfa_second_factor is not None:
            self._values["mfa_second_factor"] = mfa_second_factor
        if password_policy is not None:
            self._values["password_policy"] = password_policy
        if self_sign_up_enabled is not None:
            self._values["self_sign_up_enabled"] = self_sign_up_enabled
        if sign_in_aliases is not None:
            self._values["sign_in_aliases"] = sign_in_aliases
        if sign_in_case_sensitive is not None:
            self._values["sign_in_case_sensitive"] = sign_in_case_sensitive
        if sms_role is not None:
            self._values["sms_role"] = sms_role
        if sms_role_external_id is not None:
            self._values["sms_role_external_id"] = sms_role_external_id
        if standard_attributes is not None:
            self._values["standard_attributes"] = standard_attributes
        if user_invitation is not None:
            self._values["user_invitation"] = user_invitation
        if user_pool_name is not None:
            self._values["user_pool_name"] = user_pool_name
        if user_verification is not None:
            self._values["user_verification"] = user_verification

    @builtins.property
    def account_recovery(self) -> typing.Optional[AccountRecovery]:
        """How will a user be able to recover their account?

        :default: AccountRecovery.PHONE_WITHOUT_MFA_AND_EMAIL
        """
        result = self._values.get("account_recovery")
        return result

    @builtins.property
    def auto_verify(self) -> typing.Optional[AutoVerifiedAttrs]:
        """Attributes which Cognito will look to verify automatically upon user sign up.

        EMAIL and PHONE are the only available options.

        :default:

        - If ``signInAlias`` includes email and/or phone, they will be included in ``autoVerifiedAttributes`` by default.
        If absent, no attributes will be auto-verified.
        """
        result = self._values.get("auto_verify")
        return result

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ICustomAttribute]]:
        """Define a set of custom attributes that can be configured for each user in the user pool.

        :default: - No custom attributes.
        """
        result = self._values.get("custom_attributes")
        return result

    @builtins.property
    def email_settings(self) -> typing.Optional[EmailSettings]:
        """Email settings for a user pool.

        :default: - see defaults on each property of EmailSettings.
        """
        result = self._values.get("email_settings")
        return result

    @builtins.property
    def enable_sms_role(self) -> typing.Optional[builtins.bool]:
        """Setting this would explicitly enable or disable SMS role creation.

        When left unspecified, CDK will determine based on other properties if a role is needed or not.

        :default: - CDK will determine based on other properties of the user pool if an SMS role should be created or not.
        """
        result = self._values.get("enable_sms_role")
        return result

    @builtins.property
    def lambda_triggers(self) -> typing.Optional["UserPoolTriggers"]:
        """Lambda functions to use for supported Cognito triggers.

        :default: - No Lambda triggers.

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
        """
        result = self._values.get("lambda_triggers")
        return result

    @builtins.property
    def mfa(self) -> typing.Optional[Mfa]:
        """Configure whether users of this user pool can or are required use MFA to sign in.

        :default: Mfa.OFF
        """
        result = self._values.get("mfa")
        return result

    @builtins.property
    def mfa_second_factor(self) -> typing.Optional[MfaSecondFactor]:
        """Configure the MFA types that users can use in this user pool.

        Ignored if ``mfa`` is set to ``OFF``.

        :default:

        - { sms: true, oneTimePassword: false }, if ``mfa`` is set to ``OPTIONAL`` or ``REQUIRED``.
        { sms: false, oneTimePassword: false }, otherwise
        """
        result = self._values.get("mfa_second_factor")
        return result

    @builtins.property
    def password_policy(self) -> typing.Optional[PasswordPolicy]:
        """Password policy for this user pool.

        :default: - see defaults on each property of PasswordPolicy.
        """
        result = self._values.get("password_policy")
        return result

    @builtins.property
    def self_sign_up_enabled(self) -> typing.Optional[builtins.bool]:
        """Whether self sign up should be enabled.

        This can be further configured via the ``selfSignUp`` property.

        :default: false
        """
        result = self._values.get("self_sign_up_enabled")
        return result

    @builtins.property
    def sign_in_aliases(self) -> typing.Optional[SignInAliases]:
        """Methods in which a user registers or signs in to a user pool.

        Allows either username with aliases OR sign in with email, phone, or both.

        Read the sections on usernames and aliases to learn more -
        https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html

        To match with 'Option 1' in the above link, with a verified email, this property should be set to
        ``{ username: true, email: true }``. To match with 'Option 2' in the above link with both a verified email and phone
        number, this property should be set to ``{ email: true, phone: true }``.

        :default: { username: true }
        """
        result = self._values.get("sign_in_aliases")
        return result

    @builtins.property
    def sign_in_case_sensitive(self) -> typing.Optional[builtins.bool]:
        """Whether sign-in aliases should be evaluated with case sensitivity.

        For example, when this option is set to false, users will be able to sign in using either ``MyUsername`` or ``myusername``.

        :default: true
        """
        result = self._values.get("sign_in_case_sensitive")
        return result

    @builtins.property
    def sms_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role that Cognito will assume while sending SMS messages.

        :default: - a new IAM role is created
        """
        result = self._values.get("sms_role")
        return result

    @builtins.property
    def sms_role_external_id(self) -> typing.Optional[builtins.str]:
        """The 'ExternalId' that Cognito service must using when assuming the ``smsRole``, if the role is restricted with an 'sts:ExternalId' conditional.

        Learn more about ExternalId here - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html

        This property will be ignored if ``smsRole`` is not specified.

        :default: - No external id will be configured
        """
        result = self._values.get("sms_role_external_id")
        return result

    @builtins.property
    def standard_attributes(self) -> typing.Optional[StandardAttributes]:
        """The set of attributes that are required for every user in the user pool.

        Read more on attributes here - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html

        :default: - All standard attributes are optional and mutable.
        """
        result = self._values.get("standard_attributes")
        return result

    @builtins.property
    def user_invitation(self) -> typing.Optional[UserInvitationConfig]:
        """Configuration around admins signing up users into a user pool.

        :default: - see defaults in UserInvitationConfig
        """
        result = self._values.get("user_invitation")
        return result

    @builtins.property
    def user_pool_name(self) -> typing.Optional[builtins.str]:
        """Name of the user pool.

        :default: - automatically generated name by CloudFormation at deploy time
        """
        result = self._values.get("user_pool_name")
        return result

    @builtins.property
    def user_verification(self) -> typing.Optional["UserVerificationConfig"]:
        """Configuration around users signing themselves up to the user pool.

        Enable or disable self sign-up via the ``selfSignUpEnabled`` property.

        :default: - see defaults in UserVerificationConfig
        """
        result = self._values.get("user_verification")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IUserPoolResourceServer)
class UserPoolResourceServer(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.UserPoolResourceServer",
):
    """Defines a User Pool OAuth2.0 Resource Server."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        user_pool: IUserPool,
        identifier: builtins.str,
        scopes: typing.Optional[typing.List[ResourceServerScope]] = None,
        user_pool_resource_server_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param user_pool: The user pool to add this resource server to.
        :param identifier: A unique resource server identifier for the resource server.
        :param scopes: Oauth scopes. Default: - No scopes will be added
        :param user_pool_resource_server_name: A friendly name for the resource server. Default: - same as ``identifier``
        """
        props = UserPoolResourceServerProps(
            user_pool=user_pool,
            identifier=identifier,
            scopes=scopes,
            user_pool_resource_server_name=user_pool_resource_server_name,
        )

        jsii.create(UserPoolResourceServer, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserPoolResourceServerId")
    @builtins.classmethod
    def from_user_pool_resource_server_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        user_pool_resource_server_id: builtins.str,
    ) -> IUserPoolResourceServer:
        """Import a user pool resource client given its id.

        :param scope: -
        :param id: -
        :param user_pool_resource_server_id: -
        """
        return jsii.sinvoke(cls, "fromUserPoolResourceServerId", [scope, id, user_pool_resource_server_id])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userPoolResourceServerId")
    def user_pool_resource_server_id(self) -> builtins.str:
        """Resource server id."""
        return jsii.get(self, "userPoolResourceServerId")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolResourceServerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "scopes": "scopes",
        "user_pool_resource_server_name": "userPoolResourceServerName",
    },
)
class UserPoolResourceServerOptions:
    def __init__(
        self,
        *,
        identifier: builtins.str,
        scopes: typing.Optional[typing.List[ResourceServerScope]] = None,
        user_pool_resource_server_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Options to create a UserPoolResourceServer.

        :param identifier: A unique resource server identifier for the resource server.
        :param scopes: Oauth scopes. Default: - No scopes will be added
        :param user_pool_resource_server_name: A friendly name for the resource server. Default: - same as ``identifier``
        """
        self._values: typing.Dict[str, typing.Any] = {
            "identifier": identifier,
        }
        if scopes is not None:
            self._values["scopes"] = scopes
        if user_pool_resource_server_name is not None:
            self._values["user_pool_resource_server_name"] = user_pool_resource_server_name

    @builtins.property
    def identifier(self) -> builtins.str:
        """A unique resource server identifier for the resource server."""
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return result

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[ResourceServerScope]]:
        """Oauth scopes.

        :default: - No scopes will be added
        """
        result = self._values.get("scopes")
        return result

    @builtins.property
    def user_pool_resource_server_name(self) -> typing.Optional[builtins.str]:
        """A friendly name for the resource server.

        :default: - same as ``identifier``
        """
        result = self._values.get("user_pool_resource_server_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolResourceServerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolResourceServerProps",
    jsii_struct_bases=[UserPoolResourceServerOptions],
    name_mapping={
        "identifier": "identifier",
        "scopes": "scopes",
        "user_pool_resource_server_name": "userPoolResourceServerName",
        "user_pool": "userPool",
    },
)
class UserPoolResourceServerProps(UserPoolResourceServerOptions):
    def __init__(
        self,
        *,
        identifier: builtins.str,
        scopes: typing.Optional[typing.List[ResourceServerScope]] = None,
        user_pool_resource_server_name: typing.Optional[builtins.str] = None,
        user_pool: IUserPool,
    ) -> None:
        """Properties for the UserPoolResourceServer construct.

        :param identifier: A unique resource server identifier for the resource server.
        :param scopes: Oauth scopes. Default: - No scopes will be added
        :param user_pool_resource_server_name: A friendly name for the resource server. Default: - same as ``identifier``
        :param user_pool: The user pool to add this resource server to.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "identifier": identifier,
            "user_pool": user_pool,
        }
        if scopes is not None:
            self._values["scopes"] = scopes
        if user_pool_resource_server_name is not None:
            self._values["user_pool_resource_server_name"] = user_pool_resource_server_name

    @builtins.property
    def identifier(self) -> builtins.str:
        """A unique resource server identifier for the resource server."""
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return result

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[ResourceServerScope]]:
        """Oauth scopes.

        :default: - No scopes will be added
        """
        result = self._values.get("scopes")
        return result

    @builtins.property
    def user_pool_resource_server_name(self) -> typing.Optional[builtins.str]:
        """A friendly name for the resource server.

        :default: - same as ``identifier``
        """
        result = self._values.get("user_pool_resource_server_name")
        return result

    @builtins.property
    def user_pool(self) -> IUserPool:
        """The user pool to add this resource server to."""
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolResourceServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolTriggers",
    jsii_struct_bases=[],
    name_mapping={
        "create_auth_challenge": "createAuthChallenge",
        "custom_message": "customMessage",
        "define_auth_challenge": "defineAuthChallenge",
        "post_authentication": "postAuthentication",
        "post_confirmation": "postConfirmation",
        "pre_authentication": "preAuthentication",
        "pre_sign_up": "preSignUp",
        "pre_token_generation": "preTokenGeneration",
        "user_migration": "userMigration",
        "verify_auth_challenge_response": "verifyAuthChallengeResponse",
    },
)
class UserPoolTriggers:
    def __init__(
        self,
        *,
        create_auth_challenge: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        custom_message: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        define_auth_challenge: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        post_authentication: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        post_confirmation: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        pre_authentication: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        pre_sign_up: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        pre_token_generation: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        user_migration: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
        verify_auth_challenge_response: typing.Optional[aws_cdk.aws_lambda.IFunction] = None,
    ) -> None:
        """Triggers for a user pool.

        :param create_auth_challenge: Creates an authentication challenge. Default: - no trigger configured
        :param custom_message: A custom Message AWS Lambda trigger. Default: - no trigger configured
        :param define_auth_challenge: Defines the authentication challenge. Default: - no trigger configured
        :param post_authentication: A post-authentication AWS Lambda trigger. Default: - no trigger configured
        :param post_confirmation: A post-confirmation AWS Lambda trigger. Default: - no trigger configured
        :param pre_authentication: A pre-authentication AWS Lambda trigger. Default: - no trigger configured
        :param pre_sign_up: A pre-registration AWS Lambda trigger. Default: - no trigger configured
        :param pre_token_generation: A pre-token-generation AWS Lambda trigger. Default: - no trigger configured
        :param user_migration: A user-migration AWS Lambda trigger. Default: - no trigger configured
        :param verify_auth_challenge_response: Verifies the authentication challenge response. Default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if create_auth_challenge is not None:
            self._values["create_auth_challenge"] = create_auth_challenge
        if custom_message is not None:
            self._values["custom_message"] = custom_message
        if define_auth_challenge is not None:
            self._values["define_auth_challenge"] = define_auth_challenge
        if post_authentication is not None:
            self._values["post_authentication"] = post_authentication
        if post_confirmation is not None:
            self._values["post_confirmation"] = post_confirmation
        if pre_authentication is not None:
            self._values["pre_authentication"] = pre_authentication
        if pre_sign_up is not None:
            self._values["pre_sign_up"] = pre_sign_up
        if pre_token_generation is not None:
            self._values["pre_token_generation"] = pre_token_generation
        if user_migration is not None:
            self._values["user_migration"] = user_migration
        if verify_auth_challenge_response is not None:
            self._values["verify_auth_challenge_response"] = verify_auth_challenge_response

    @builtins.property
    def create_auth_challenge(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """Creates an authentication challenge.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-create-auth-challenge.html
        """
        result = self._values.get("create_auth_challenge")
        return result

    @builtins.property
    def custom_message(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A custom Message AWS Lambda trigger.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html
        """
        result = self._values.get("custom_message")
        return result

    @builtins.property
    def define_auth_challenge(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """Defines the authentication challenge.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-define-auth-challenge.html
        """
        result = self._values.get("define_auth_challenge")
        return result

    @builtins.property
    def post_authentication(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A post-authentication AWS Lambda trigger.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html
        """
        result = self._values.get("post_authentication")
        return result

    @builtins.property
    def post_confirmation(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A post-confirmation AWS Lambda trigger.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-confirmation.html
        """
        result = self._values.get("post_confirmation")
        return result

    @builtins.property
    def pre_authentication(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A pre-authentication AWS Lambda trigger.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html
        """
        result = self._values.get("pre_authentication")
        return result

    @builtins.property
    def pre_sign_up(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A pre-registration AWS Lambda trigger.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html
        """
        result = self._values.get("pre_sign_up")
        return result

    @builtins.property
    def pre_token_generation(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A pre-token-generation AWS Lambda trigger.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html
        """
        result = self._values.get("pre_token_generation")
        return result

    @builtins.property
    def user_migration(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """A user-migration AWS Lambda trigger.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html
        """
        result = self._values.get("user_migration")
        return result

    @builtins.property
    def verify_auth_challenge_response(
        self,
    ) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """Verifies the authentication challenge response.

        :default: - no trigger configured

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-verify-auth-challenge-response.html
        """
        result = self._values.get("verify_auth_challenge_response")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserVerificationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "email_body": "emailBody",
        "email_style": "emailStyle",
        "email_subject": "emailSubject",
        "sms_message": "smsMessage",
    },
)
class UserVerificationConfig:
    def __init__(
        self,
        *,
        email_body: typing.Optional[builtins.str] = None,
        email_style: typing.Optional["VerificationEmailStyle"] = None,
        email_subject: typing.Optional[builtins.str] = None,
        sms_message: typing.Optional[builtins.str] = None,
    ) -> None:
        """User pool configuration for user self sign up.

        :param email_body: The email body template for the verification email sent to the user upon sign up. See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to learn more about message templates. Default: - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen, 'Verify your account by clicking on {##Verify Email##}' if VerificationEmailStyle.LINK is chosen.
        :param email_style: Emails can be verified either using a code or a link. Learn more at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-email-verification-message-customization.html Default: VerificationEmailStyle.CODE
        :param email_subject: The email subject template for the verification email sent to the user upon sign up. See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to learn more about message templates. Default: 'Verify your new account'
        :param sms_message: The message template for the verification SMS sent to the user upon sign up. See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to learn more about message templates. Default: - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen, not configured if VerificationEmailStyle.LINK is chosen
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if email_body is not None:
            self._values["email_body"] = email_body
        if email_style is not None:
            self._values["email_style"] = email_style
        if email_subject is not None:
            self._values["email_subject"] = email_subject
        if sms_message is not None:
            self._values["sms_message"] = sms_message

    @builtins.property
    def email_body(self) -> typing.Optional[builtins.str]:
        """The email body template for the verification email sent to the user upon sign up.

        See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to
        learn more about message templates.

        :default:

        - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen,
        'Verify your account by clicking on {##Verify Email##}' if VerificationEmailStyle.LINK is chosen.
        """
        result = self._values.get("email_body")
        return result

    @builtins.property
    def email_style(self) -> typing.Optional["VerificationEmailStyle"]:
        """Emails can be verified either using a code or a link.

        Learn more at https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-email-verification-message-customization.html

        :default: VerificationEmailStyle.CODE
        """
        result = self._values.get("email_style")
        return result

    @builtins.property
    def email_subject(self) -> typing.Optional[builtins.str]:
        """The email subject template for the verification email sent to the user upon sign up.

        See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to
        learn more about message templates.

        :default: 'Verify your new account'
        """
        result = self._values.get("email_subject")
        return result

    @builtins.property
    def sms_message(self) -> typing.Optional[builtins.str]:
        """The message template for the verification SMS sent to the user upon sign up.

        See https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-message-templates.html to
        learn more about message templates.

        :default:

        - 'The verification code to your new account is {####}' if VerificationEmailStyle.CODE is chosen,
        not configured if VerificationEmailStyle.LINK is chosen
        """
        result = self._values.get("sms_message")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserVerificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cognito.VerificationEmailStyle")
class VerificationEmailStyle(enum.Enum):
    """The email verification style."""

    CODE = "CODE"
    """Verify email via code."""
    LINK = "LINK"
    """Verify email via link."""


@jsii.implements(ICustomAttribute)
class BooleanAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.BooleanAttribute",
):
    """The Boolean custom attribute type."""

    def __init__(self, *, mutable: typing.Optional[builtins.bool] = None) -> None:
        """
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        """
        props = CustomAttributeProps(mutable=mutable)

        jsii.create(BooleanAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> CustomAttributeConfig:
        """Bind this custom attribute type to the values as expected by CloudFormation."""
        return jsii.invoke(self, "bind", [])


@jsii.implements(ICustomAttribute)
class DateTimeAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito.DateTimeAttribute",
):
    """The DateTime custom attribute type."""

    def __init__(self, *, mutable: typing.Optional[builtins.bool] = None) -> None:
        """
        :param mutable: Specifies whether the value of the attribute can be changed. For any user pool attribute that's mapped to an identity provider attribute, you must set this parameter to true. Amazon Cognito updates mapped attributes when users sign in to your application through an identity provider. If an attribute is immutable, Amazon Cognito throws an error when it attempts to update the attribute. Default: false
        """
        props = CustomAttributeProps(mutable=mutable)

        jsii.create(DateTimeAttribute, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self) -> CustomAttributeConfig:
        """Bind this custom attribute type to the values as expected by CloudFormation."""
        return jsii.invoke(self, "bind", [])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProviderAmazonProps",
    jsii_struct_bases=[UserPoolIdentityProviderProps],
    name_mapping={
        "user_pool": "userPool",
        "attribute_mapping": "attributeMapping",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "scopes": "scopes",
    },
)
class UserPoolIdentityProviderAmazonProps(UserPoolIdentityProviderProps):
    def __init__(
        self,
        *,
        user_pool: IUserPool,
        attribute_mapping: typing.Optional[AttributeMapping] = None,
        client_id: builtins.str,
        client_secret: builtins.str,
        scopes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties to initialize UserPoolAmazonIdentityProvider.

        :param user_pool: The user pool to which this construct provides identities.
        :param attribute_mapping: Mapping attributes from the identity provider to standard and custom attributes of the user pool. Default: - no attribute mapping
        :param client_id: The client id recognized by 'Login with Amazon' APIs.
        :param client_secret: The client secret to be accompanied with clientId for 'Login with Amazon' APIs to authenticate the client.
        :param scopes: The types of user profile data to obtain for the Amazon profile. Default: [ profile ]
        """
        if isinstance(attribute_mapping, dict):
            attribute_mapping = AttributeMapping(**attribute_mapping)
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool": user_pool,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def user_pool(self) -> IUserPool:
        """The user pool to which this construct provides identities."""
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return result

    @builtins.property
    def attribute_mapping(self) -> typing.Optional[AttributeMapping]:
        """Mapping attributes from the identity provider to standard and custom attributes of the user pool.

        :default: - no attribute mapping
        """
        result = self._values.get("attribute_mapping")
        return result

    @builtins.property
    def client_id(self) -> builtins.str:
        """The client id recognized by 'Login with Amazon' APIs.

        :see: https://developer.amazon.com/docs/login-with-amazon/security-profile.html#client-identifier
        """
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return result

    @builtins.property
    def client_secret(self) -> builtins.str:
        """The client secret to be accompanied with clientId for 'Login with Amazon' APIs to authenticate the client.

        :see: https://developer.amazon.com/docs/login-with-amazon/security-profile.html#client-identifier
        """
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return result

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        """The types of user profile data to obtain for the Amazon profile.

        :default: [ profile ]

        :see: https://developer.amazon.com/docs/login-with-amazon/customer-profile.html
        """
        result = self._values.get("scopes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolIdentityProviderAmazonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProviderFacebookProps",
    jsii_struct_bases=[UserPoolIdentityProviderProps],
    name_mapping={
        "user_pool": "userPool",
        "attribute_mapping": "attributeMapping",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "api_version": "apiVersion",
        "scopes": "scopes",
    },
)
class UserPoolIdentityProviderFacebookProps(UserPoolIdentityProviderProps):
    def __init__(
        self,
        *,
        user_pool: IUserPool,
        attribute_mapping: typing.Optional[AttributeMapping] = None,
        client_id: builtins.str,
        client_secret: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties to initialize UserPoolFacebookIdentityProvider.

        :param user_pool: The user pool to which this construct provides identities.
        :param attribute_mapping: Mapping attributes from the identity provider to standard and custom attributes of the user pool. Default: - no attribute mapping
        :param client_id: The client id recognized by Facebook APIs.
        :param client_secret: The client secret to be accompanied with clientUd for Facebook to authenticate the client.
        :param api_version: The Facebook API version to use. Default: - to the oldest version supported by Facebook
        :param scopes: The list of facebook permissions to obtain for getting access to the Facebook profile. Default: [ public_profile ]
        """
        if isinstance(attribute_mapping, dict):
            attribute_mapping = AttributeMapping(**attribute_mapping)
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool": user_pool,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping
        if api_version is not None:
            self._values["api_version"] = api_version
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def user_pool(self) -> IUserPool:
        """The user pool to which this construct provides identities."""
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return result

    @builtins.property
    def attribute_mapping(self) -> typing.Optional[AttributeMapping]:
        """Mapping attributes from the identity provider to standard and custom attributes of the user pool.

        :default: - no attribute mapping
        """
        result = self._values.get("attribute_mapping")
        return result

    @builtins.property
    def client_id(self) -> builtins.str:
        """The client id recognized by Facebook APIs."""
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return result

    @builtins.property
    def client_secret(self) -> builtins.str:
        """The client secret to be accompanied with clientUd for Facebook to authenticate the client.

        :see: https://developers.facebook.com/docs/facebook-login/security#appsecret
        """
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return result

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        """The Facebook API version to use.

        :default: - to the oldest version supported by Facebook
        """
        result = self._values.get("api_version")
        return result

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        """The list of facebook permissions to obtain for getting access to the Facebook profile.

        :default: [ public_profile ]

        :see: https://developers.facebook.com/docs/facebook-login/permissions
        """
        result = self._values.get("scopes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolIdentityProviderFacebookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito.UserPoolIdentityProviderGoogleProps",
    jsii_struct_bases=[UserPoolIdentityProviderProps],
    name_mapping={
        "user_pool": "userPool",
        "attribute_mapping": "attributeMapping",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "scopes": "scopes",
    },
)
class UserPoolIdentityProviderGoogleProps(UserPoolIdentityProviderProps):
    def __init__(
        self,
        *,
        user_pool: IUserPool,
        attribute_mapping: typing.Optional[AttributeMapping] = None,
        client_id: builtins.str,
        client_secret: builtins.str,
        scopes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties to initialize UserPoolGoogleIdentityProvider.

        :param user_pool: The user pool to which this construct provides identities.
        :param attribute_mapping: Mapping attributes from the identity provider to standard and custom attributes of the user pool. Default: - no attribute mapping
        :param client_id: The client id recognized by Google APIs.
        :param client_secret: The client secret to be accompanied with clientId for Google APIs to authenticate the client.
        :param scopes: The list of google permissions to obtain for getting access to the google profile. Default: [ profile ]
        """
        if isinstance(attribute_mapping, dict):
            attribute_mapping = AttributeMapping(**attribute_mapping)
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool": user_pool,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if attribute_mapping is not None:
            self._values["attribute_mapping"] = attribute_mapping
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def user_pool(self) -> IUserPool:
        """The user pool to which this construct provides identities."""
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return result

    @builtins.property
    def attribute_mapping(self) -> typing.Optional[AttributeMapping]:
        """Mapping attributes from the identity provider to standard and custom attributes of the user pool.

        :default: - no attribute mapping
        """
        result = self._values.get("attribute_mapping")
        return result

    @builtins.property
    def client_id(self) -> builtins.str:
        """The client id recognized by Google APIs.

        :see: https://developers.google.com/identity/sign-in/web/sign-in#specify_your_apps_client_id
        """
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return result

    @builtins.property
    def client_secret(self) -> builtins.str:
        """The client secret to be accompanied with clientId for Google APIs to authenticate the client.

        :see: https://developers.google.com/identity/sign-in/web/sign-in
        """
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return result

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        """The list of google permissions to obtain for getting access to the google profile.

        :default: [ profile ]

        :see: https://developers.google.com/identity/sign-in/web/sign-in
        """
        result = self._values.get("scopes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolIdentityProviderGoogleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccountRecovery",
    "AttributeMapping",
    "AuthFlow",
    "AutoVerifiedAttrs",
    "BooleanAttribute",
    "CfnIdentityPool",
    "CfnIdentityPoolProps",
    "CfnIdentityPoolRoleAttachment",
    "CfnIdentityPoolRoleAttachmentProps",
    "CfnUserPool",
    "CfnUserPoolClient",
    "CfnUserPoolClientProps",
    "CfnUserPoolDomain",
    "CfnUserPoolDomainProps",
    "CfnUserPoolGroup",
    "CfnUserPoolGroupProps",
    "CfnUserPoolIdentityProvider",
    "CfnUserPoolIdentityProviderProps",
    "CfnUserPoolProps",
    "CfnUserPoolResourceServer",
    "CfnUserPoolResourceServerProps",
    "CfnUserPoolRiskConfigurationAttachment",
    "CfnUserPoolRiskConfigurationAttachmentProps",
    "CfnUserPoolUICustomizationAttachment",
    "CfnUserPoolUICustomizationAttachmentProps",
    "CfnUserPoolUser",
    "CfnUserPoolUserProps",
    "CfnUserPoolUserToGroupAttachment",
    "CfnUserPoolUserToGroupAttachmentProps",
    "CognitoDomainOptions",
    "CustomAttributeConfig",
    "CustomAttributeProps",
    "CustomDomainOptions",
    "DateTimeAttribute",
    "EmailSettings",
    "ICustomAttribute",
    "IUserPool",
    "IUserPoolClient",
    "IUserPoolDomain",
    "IUserPoolIdentityProvider",
    "IUserPoolResourceServer",
    "Mfa",
    "MfaSecondFactor",
    "NumberAttribute",
    "NumberAttributeConstraints",
    "NumberAttributeProps",
    "OAuthFlows",
    "OAuthScope",
    "OAuthSettings",
    "PasswordPolicy",
    "ProviderAttribute",
    "ResourceServerScope",
    "ResourceServerScopeProps",
    "SignInAliases",
    "SignInUrlOptions",
    "StandardAttribute",
    "StandardAttributes",
    "StringAttribute",
    "StringAttributeConstraints",
    "StringAttributeProps",
    "UserInvitationConfig",
    "UserPool",
    "UserPoolClient",
    "UserPoolClientIdentityProvider",
    "UserPoolClientOptions",
    "UserPoolClientProps",
    "UserPoolDomain",
    "UserPoolDomainOptions",
    "UserPoolDomainProps",
    "UserPoolIdentityProvider",
    "UserPoolIdentityProviderAmazon",
    "UserPoolIdentityProviderAmazonProps",
    "UserPoolIdentityProviderFacebook",
    "UserPoolIdentityProviderFacebookProps",
    "UserPoolIdentityProviderGoogle",
    "UserPoolIdentityProviderGoogleProps",
    "UserPoolIdentityProviderProps",
    "UserPoolOperation",
    "UserPoolProps",
    "UserPoolResourceServer",
    "UserPoolResourceServerOptions",
    "UserPoolResourceServerProps",
    "UserPoolTriggers",
    "UserVerificationConfig",
    "VerificationEmailStyle",
]

publication.publish()
