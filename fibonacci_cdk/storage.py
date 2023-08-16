from aws_cdk import (
    aws_s3 as s3,
    aws_efs as efs,
    aws_ec2 as ec2,
    RemovalPolicy, Stack
)
from constructs import Construct

class Storage(Construct):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, security_group: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self, 'Bucket',
            bucket_name=f"{scope.stage}-fibonacci-cdk-bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        self.filesystem = efs.FileSystem(
            self, 'FileSystem',
            vpc=vpc,
            removal_policy=RemovalPolicy.DESTROY,
            security_group=security_group
        )
