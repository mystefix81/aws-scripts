#!/usr/bin/python

from boto import ec2, exception
import json

regions = dict()
for region in ec2.regions():
    if not region.name in [ "us-east-1", "us-west-1", "sa-east-1", "eu-west-1" ]:
        print "Skipping %s..." % region.name
        continue
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
