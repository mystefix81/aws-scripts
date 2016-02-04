#!/usr/bin/python
""" running-instances: Getting the runnning instances from a specific account"""

import boto.ec2
import argparse
from prettytable import PrettyTable
from threading import Thread

def get_region_instances(auth, region, tables):
    """Get running instances"""
    table = PrettyTable(["Name", "Key-Name", "Type", "Placement",
                     "Public-DNS", "Public-IP", "Private-IP",
                     "Instance-ID", "State", "Launch Time"])
    table.padding_width = 1
    ec2 = boto.ec2.connect_to_region(region.name,
                                     aws_access_key_id=auth.aws_access_key_id,
                                     aws_secret_access_key=
                                     auth.aws_secret_access_key)
    reservations = ec2.get_all_instances()
    if reservations:
        for reservation in reservations:
            for i in reservation.instances:
                try:
                    instance_name = i.tags['Name']
                except KeyError:
                    instance_name = "N/A"
                table.add_row([
                    instance_name,
                    i.key_name,
                    i.instance_type,
                    i.placement,
                    i.public_dns_name,
                    i.ip_address,
                    i.private_ip_address,
                    i.id,
                    i.state,
                    i.launch_time
                    ])
        tables[region.name] = table
    return

def main():
    """Main function"""

    parser = argparse.ArgumentParser(description="Show available ec2"
                                                 "instances in AWS account.")
    parser.add_argument(
            "-p",
            "--profile",
            required=False,
            default=None,
            help="The profile to use from .boto / .aws/credentials,"
                 "if not provided the default credentials will be used."
            )
    args = parser.parse_args()
    conn = boto.ec2.connection.EC2Connection()
    auth = boto.connection.AWSAuthConnection("ec2.eu-west-1.amazonaws.com",
                                         profile_name=args.profile)
    regions = conn.get_all_regions()


    threads = {}
    tables = {}

    for region in regions:
        threads[region.name] = Thread(target=get_region_instances,
                                      args=[auth, region, tables])
        threads[region.name].daemon = True
        threads[region.name].start()

    for region in regions:
        threads[region.name].join()

    for region in sorted(tables.keys()):
        print region
        print tables[region]

if __name__ == '__main__':
    main()

