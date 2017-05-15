#!/usr/bin/env python

#ec2.list.instances.py
# don't forget to run aws configure before running that script

import boto3, pprint

pp = pprint.PrettyPrinter(indent=2)

client = boto3.client('route53')
response = client.list_hosted_zones()

for hostedZone in response["HostedZones"]:
    id = hostedZone["Id"]
    name = hostedZone["Name"]
    print(">>> %(id)s - %(name)s :" % locals())
    rsResponse = client.list_resource_record_sets(HostedZoneId = id)
    for recordSet in rsResponse["ResourceRecordSets"]:
        pp.pprint(recordSet)