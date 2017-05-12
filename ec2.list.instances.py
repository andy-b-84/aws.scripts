#!/usr/bin/env python

#ec2.list.instances.py
# don't forget to run aws configure before running that script

import boto3

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

response = ec2client.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        if instance["State"]["Code"] == 16: # Running
            # This will print will output the value of the Dictionary key 'InstanceId'
            has80 = False
            has443 = False
            name = ""
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    name = tag["Value"]
            for securityGroupTuple in instance["SecurityGroups"]:
                securityGroup = ec2resource.SecurityGroup(securityGroupTuple["GroupId"])
                securityGroup.load()
                for ipPermission in securityGroup.ip_permissions:
                    has80 = has80 or (("FromPort" in ipPermission) and (ipPermission["FromPort"] == 80))
                    has443 = has443 or (("FromPort" in ipPermission) and (ipPermission["FromPort"] == 443))
            if not has80 and not has443:
                print(instance["InstanceId"] + " - " + name)
            elif not has80:
                print(instance["InstanceId"] + " - " + name + " (!) 443 bound")