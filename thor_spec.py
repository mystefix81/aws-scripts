#!/usr/bin/python

from boto import ec2, exception
import json

regions = dict()
for region in ec2.connection.EC2Connection().get_all_regions():
    regions[region.name] = dict()
    ec2_conn = region.connect()
    reservations = ec2_conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for instance in instances:
        regions[region.name][instance.id] = dict(
                map(
                    lambda x: x.split("="),
                    [ts for ts in instance.tags['thor_spec'].split("&")]
                    )
                )

print json.dumps(regions, indent=4)
