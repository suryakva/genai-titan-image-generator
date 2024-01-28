#!/usr/bin/env python3
import aws_cdk as cdk
import boto3

from stack.vpc_network_stack import VpcNetworkStack
from stack.application_stack import ApplicationStack



region_name = boto3.Session().region_name
env={"region": region_name}


app = cdk.App()

network_stack = VpcNetworkStack(app, "VpcNetworkStack", env=env)
ApplicationStack(app, "ApplicationStack", vpc=network_stack.vpc, env=env)

app.synth()
