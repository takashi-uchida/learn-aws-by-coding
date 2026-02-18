from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_cognito as cognito,
)

class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create Cognito user pool
        user_pool = cognito.UserPool(
            self, "UserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                username=False, email=True,
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=False,
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
        self.user_pool = user_pool

        client = user_pool.add_client(
            "UserClient",
            auth_flows=cognito.AuthFlow(
                user_password=True
            ),
        )

        cdk.CfnOutput(self, "User Pool ID", value=user_pool.user_pool_id)
        cdk.CfnOutput(self, "Pool Client ID", value=client.user_pool_client_id)
