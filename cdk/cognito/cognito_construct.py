from aws_cdk import core, aws_cognito as cognito

class CognitoConstruct(core.Construct):
    def __init__(self, scope: core.Construct, id: str, user_pool_name: str, **kwargs):
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
        core.CfnOutput(self, "UserPoolId", value=self.user_pool.user_pool_id)
        core.CfnOutput(self, "UserPoolClientId", value=self.user_pool_client.user_pool_client_id)
