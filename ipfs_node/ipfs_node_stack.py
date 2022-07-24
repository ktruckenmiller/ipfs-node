from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_ecr as ecr,
)
from constructs import Construct


class IpfsNodeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc.from_lookup(
            self,
            "Vpc",
            vpc_id="vpc-849531e0",
        )
        self.cluster = ecs.Cluster.from_cluster_attributes(
            self,
            "cluster",
            cluster_name="test-btc",
            vpc=self.vpc,
            security_groups=[ec2.SecurityGroup(self, "sg", vpc=self.vpc)],
        )
        self.get_ipfs_service()

    def get_ipfs_service(self):
        task_definition = ecs.ExternalTaskDefinition(
            self, "ipfs-task-def", network_mode=ecs.NetworkMode.HOST
        )
        cfnExtTaskDef = task_definition.node.default_child
        cfnExtTaskDef.add_property_override(
            "Volumes",
            [
                {"Name": "staging", "Host": {"SourcePath": "/bigboy/ipfs/staging"}},
                {"Name": "data", "Host": {"SourcePath": "/bigboy/ipfs/data"}},
            ],
        )
        ipfs_node = task_definition.add_container(
            "ipfs-container",
            image=ecs.ContainerImage.from_ecr_repository(
                ecr.Repository.from_repository_name(
                    self,
                    "ipfs",
                    repository_name="ipfs",
                ),
                tag="latest",
            ),
            memory_reservation_mib=2048,
            port_mappings=[
                ecs.PortMapping(container_port=4001),
                ecs.PortMapping(container_port=8080),
                ecs.PortMapping(container_port=5001),
            ],
            logging=ecs.LogDrivers.aws_logs(
                log_retention=logs.RetentionDays.ONE_WEEK, stream_prefix="myip"
            ),
        )
        ipfs_node.add_mount_points(
            ecs.MountPoint(
                container_path="/export",
                read_only=False,
                source_volume="staging",
            )
        )
        ipfs_node.add_mount_points(
            ecs.MountPoint(
                container_path="/data/ipfs",
                read_only=False,
                source_volume="data",
            )
        )
        ecs.ExternalService(
            self,
            "local-ipfs",
            cluster=self.cluster,
            task_definition=task_definition,
            min_healthy_percent=0,
            max_healthy_percent=100,
        )
