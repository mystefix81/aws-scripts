#!/usr/bin/python
#
#
#requires python boto libary
#
#script which will fetch the private ips of all instances within the autoscaling, where the instance belongs to.
#
#No ACCEES or SECRET_KEY needed as this script will use the credentials from the IAM role from the instance. 
#
#The following rights needs to be granted via role:
#
#DescribeInstances
#DescribeAutoScalingInstances
#
#

import os
import boto
from boto import ec2
import boto.ec2.autoscale
import boto.utils

# Path where the file for the private ips will be written
ipfile = '/tmp/private_ips.txt'

# Find the region where the instance is running
region = boto.utils.get_instance_metadata()['local-hostname'].split('.')[1]

# Connect to ec2 and autoscale api
ec2_conn = boto.ec2.connect_to_region(region)
as_conn = boto.ec2.autoscale.connect_to_region(region)

# Findout the asg, where the instance is part of
def get_asg_name():
    metadata = boto.utils.get_instance_metadata()
    own_instance_id = metadata['instance-id']
    instance_list = as_conn.get_all_autoscaling_instances()
    instance_list = [ i for i in instance_list if i.lifecycle_state == "InService" ]
    asgroup = [ i for i in instance_list if i.instance_id == own_instance_id ][0].group_name
    return asgroup

# Fetch private ips of the instances within the asg
def get_private_ips():
    group = as_conn.get_all_groups([get_asg_name()])[0]
    instance_ids = [i.instance_id for i in group.instances]
    reservations = ec2_conn.get_all_instances(instance_ids)
    instances = [i.private_ip_address for r in reservations for i in r.instances]
    return instances

# Write private instance ips to file
datafile = open(ipfile, "w")
for eachitem in get_private_ips():
    datafile.write(str(eachitem)+'\n')
datafile.close()

