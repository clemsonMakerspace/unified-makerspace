
from aws_cdk import (
    aws_cognito as cognito,
    CfnOutput
)
from constructs import Construct

class CognitoConstruct(Construct):
    """
    The CognitoConstruct is a reusable construct that sets up an AWS Cognito User Pool
    and a User Pool Client for user authentication and management.

    This construct performs the following tasks:
    - Creates a Cognito User Pool with customizable properties such as:
        - Sign-in aliases (username and email).
        - Self-signup disabled by default.
        - Password policy enforcing secure user credentials.
        - Optional Multi-Factor Authentication (MFA) using SMS or OTP.
        - Email-based account recovery.
    - Creates a User Pool Client associated with the User Pool.
    - Outputs key details such as the User Pool ID and User Pool Client ID.

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - id (str): The unique identifier for this construct.
    - user_pool_name (str): The name of the Cognito User Pool to be created.
    - kwargs: Additional optional arguments.

    Key Resources:
    - Cognito User Pool:
        - Provides secure user authentication and user management.
        - Configured with sign-in aliases for username and email.
        - Enforces a password policy (minimum length, lowercase, uppercase, digits).
        - Supports optional Multi-Factor Authentication (MFA).
        - Enables account recovery via email.
    - Cognito User Pool Client:
        - Allows applications to interact with the User Pool for authentication.

    Outputs:
    - UserPoolId: The unique identifier of the Cognito User Pool.
    - UserPoolClientId: The unique identifier of the Cognito User Pool Client.

    Notes:
    - This construct does not enable self-signup by default. If required, set `self_sign_up_enabled=True` during initialization.
    - The `password_policy` ensures compliance with security best practices by requiring strong passwords.
    - MFA is optional but can be configured to be required if needed.

    Documentation Links:
        - aws_cognito.UserPool:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/UserPool.html
        - aws_cognito.SignInAliases:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/SignInAliases.html
        - aws_cognito.PasswordPolicy:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/PasswordPolicy.html
        - aws_cognito.Mfa:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/Mfa.html
        - aws_cognito.AccountRecovery:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/AccountRecovery.html
        - aws_cognito.UserPoolClient:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/UserPoolClient.html
        - CfnOutput:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/CfnOutput.html
    """
    def __init__(self, scope: Construct, id: str, user_pool_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Cognito User Pool
        self.user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name=user_pool_name,
            self_sign_up_enabled=False,
            sign_in_aliases=cognito.SignInAliases(username=True, email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False
            ),
            mfa=cognito.Mfa.OPTIONAL,
            mfa_second_factor=cognito.MfaSecondFactor(
                sms=True,
                otp=True
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY
        )

        # Cognito User Pool Client
        self.user_pool_client = self.user_pool.add_client("AppClient")

        # Outputs
        CfnOutput(self, "UserPoolId", value=self.user_pool.user_pool_id)
        CfnOutput(self, "UserPoolClientId", value=self.user_pool_client.user_pool_client_id)
