#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ipfs_node.ipfs_node_stack import IpfsNodeStack


app = cdk.App()
IpfsNodeStack(
    app,
    "ipfs-node",
    env=cdk.Environment(account="601394826940", region="us-west-2"),
)

app.synth()
