from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_batch as batch,
    aws_iam as iam,
    aws_ecr as ecr,
    aws_ecs as ecs,
)
import os
from dataclasses import dataclass

@dataclass
class AwsBatchStackProps:
    bucket: s3.Bucket

class AwsBatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, props: AwsBatchStackProps, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self, "vpc",
            max_azs=1,
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/23"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        managed_env = batch.FargateComputeEnvironment(
            self, "managed-env",
            vpc=vpc,
            maxv_cpus=16,
            compute_environment_name=self.stack_name + "compute-env"
        )

        job_queue = batch.JobQueue(
            self, "job-queue",
            compute_environments=[
                batch.OrderedComputeEnvironment(
                    compute_environment=managed_env,
                    order=100
                )
            ],
            job_queue_name=self.stack_name + "job-queue"
        )

        job_role = iam.Role(
            self, "job-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ecs-tasks.amazonaws.com")
            )
        )
        # allow read and write access to S3 bucket
        props.bucket.grant_read_write(job_role)

        # create a ECR repository to push docker image
        repo = ecr.Repository(
            self, "repository",
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        job_def = batch.EcsJobDefinition(
            self, "job-definition",
            container=batch.EcsFargateContainerDefinition(
                self, "container-definition",
                image=ecs.ContainerImage.from_ecr_repository(repo),
                command=["-s", "Ref::style_image", "-c", "Ref::content_image", "--save_path", "Ref::save_path", "--use_s3",
                         "--style_weight", "Ref::style_weight", "--content_weight", "Ref::content_weight"],
                cpu=4,
                memory=cdk.Size.mebibytes(8192),
                job_role=job_role,
                assign_public_ip=True,
                environment={
                    "BUCKET_NAME": props.bucket.bucket_name
                }
            ),
            job_definition_name=self.stack_name + "job-definition",
            timeout=cdk.Duration.hours(2),
        )

        self.job_queue = job_queue
        self.job_def = job_def
