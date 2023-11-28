from aws_cdk import core, aws_cognito as cognito

def setup_cognito(stack: core.Stack):
    # Cognito User Pool
    user_pool = cognito.UserPool(
        stack, "MakerspaceUserPool",
        user_pool_name="MakerspaceUserPool",
        self_sign_up_enabled=True,
        sign_in_aliases=cognito.SignInAliases(username=True, email=True),
        auto_verify=cognito.AutoVerifiedAttrs(email=True),
        password_policy=cognito.PasswordPolicy(
            min_length=12,
            require_lowercase=True,
            require_uppercase=True,
            require_digits=True,
            require_symbols=True
        ),
        mfa=cognito.Mfa.OPTIONAL,
        mfa_second_factor=cognito.MfaSecondFactor(
            sms=True,
            otp=True
        ),
        account_recovery=cognito.AccountRecovery.EMAIL_ONLY
    )

    # Cognito User Pool Client
    user_pool_client = user_pool.add_client(
        "AppClient",
        callback_uris=["https://visit.cumaker.space/callback"],
        logout_uris=["https://visit.cumaker.space/signout"],
        auth_flows={
            "user_password": True,
            "user_srp": True
        },
        generate_secret=False
    )

    # Cognito Hosted UI Domain
    user_pool_domain = user_pool.add_domain("CognitoDomain",
        cognito_domain={
            "domain_prefix": "cumakerspace"
        }
    )

    # Outputs for easy access in the AWS console or when running deploy
    core.CfnOutput(stack, "UserPoolId", value=user_pool.user_pool_id)
    core.CfnOutput(stack, "UserPoolClientId", value=user_pool_client.user_pool_client_id)
