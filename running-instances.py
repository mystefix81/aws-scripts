#!/usr/bin/python
#
#
#requires python boto libary and prettytable
#
#script will fetch all instances within the AWS account 

import boto.ec2
from boto.ec2.connection import EC2Connection 
from prettytable import PrettyTable
# EC2Connection() will pick up your key from .boto
conn = boto.ec2.connection.EC2Connection()
regions = conn.get_all_regions()
for region in sorted(regions):
    x = PrettyTable(["Name", "Key-Name", "Type", "Placement", "Public-DNS", "Instance-ID", "State", "Launch Time"])
    x.padding_width = 1
    ec2 = boto.ec2.connect_to_region(region.name) 
    instances = ec2.get_all_instances()
    if instances != []:
        print region.name
    for reservation in ec2.get_all_instances():
        for instance in reservation.instances:
            x.add_row([instance.tags['Name'],instance.key_name, instance.instance_type, instance.placement, instance.public_dns_name, instance.id, instance.state, instance.launch_time])
    if instances != []:
        print x
