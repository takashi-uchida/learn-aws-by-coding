from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_dynamodb as ddb,
    aws_s3 as s3,
)

class DbBucketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # dynamoDB table to store job
        table = ddb.Table(
            self, "Table",
            partition_key=ddb.Attribute(
                name="job_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # S3 bucket to store image data
        bucket = s3.Bucket(
            self, "Bucket",
            auto_delete_objects=False,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        bucket.add_cors_rule(
            allowed_methods=[
                s3.HttpMethods.GET,
                s3.HttpMethods.POST,
                s3.HttpMethods.PUT,
                s3.HttpMethods.HEAD,
                s3.HttpMethods.DELETE,
            ],
            allowed_origins=["*"],
            allowed_headers=["*"],
            max_age=600,
        )

        self.table = table
        self.bucket = bucket
