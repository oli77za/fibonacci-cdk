from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
)

class Network(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self, 'VPC',
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public', subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name='private', subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
            ]
        )

        self.security_group = ec2.SecurityGroup(
            self, 'SecurityGroup',
            vpc=self.vpc,
            allow_all_outbound=True
        )


