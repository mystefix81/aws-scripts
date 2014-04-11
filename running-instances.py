#!/usr/bin/python

import boto.ec2
from boto.ec2.connection import EC2Connection
from prettytable import PrettyTable
from threading import Thread

def get_region_instances(region, tables):
    x = PrettyTable(["Name", "Key-Name", "Type", "Placement", "Public-DNS", "Instance-ID", "State", "Launch Time"])
    x.padding_width = 1
    ec2 = boto.ec2.connect_to_region(region.name)
    reservations = ec2.get_all_instances()
    if reservations:
        for r in reservations:
            for i in r.instances:
                try:
                    instance_name = i.tags['Name']
                except KeyError as e:
                    instance_name = "N/A"
                    pass
                x.add_row([
                    instance_name,
                    i.key_name,
                    i.instance_type,
                    i.placement,
                    i.public_dns_name,
                    i.id,
                    i.state,
                    i.launch_time
                    ])
        tables[region.name] = x
    return

conn = boto.ec2.connection.EC2Connection()
regions = conn.get_all_regions()

threads = {}
tables = {}

for region in regions:
    threads[region.name] = Thread(target=get_region_instances, args=[region, tables])
    threads[region.name].daemon = True
    threads[region.name].start()

for region in regions:
    threads[region.name].join()

for region in sorted(tables.keys()):
    print region
    print tables[region]
