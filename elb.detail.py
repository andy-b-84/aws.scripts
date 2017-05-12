#!/usr/bin/env python

#elb.ddetail.py
# don't forget to run aws configure before running that script

import boto3, pprint

elbclient = boto3.client('elb')

response = elbclient.describe_load_balancers(
    LoadBalancerNames = ["Service-Satis"]
)

pp = pprint.PrettyPrinter(indent=2)

pp.pprint(response)