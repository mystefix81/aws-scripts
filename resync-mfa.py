#!/usr/bin/python

import boto, boto.exception
import argparse

def auth_code_check(ac):
    try:
        int(ac)
        if not len(ac) == 6:
            raise ValueError()
        else:
            return ac
    except ValueError as e:
        raise argparse.ArgumentTypeError("%s must have 6 digits" % ac)

parser = argparse.ArgumentParser(description="Resynchronizes a MFA device.")
parser.add_argument(
        'user',
        metavar="<user>",
        help='user name to resynchronize'
        )
parser.add_argument(
        'ac',
        metavar="<auth_code>",
        help="two consecutive authentication codes from the MFA device",
        type=auth_code_check,
        nargs=2)
args = parser.parse_args()

user = args.user
ac1 = args.ac[0]
ac2 = args.ac[1]
conn = boto.connect_iam()
try:
    mfa = conn.get_all_mfa_devices(user)
    serial = mfa["list_mfa_devices_response"]["list_mfa_devices_result"]["mfa_devices"][0]["serial_number"]
    print "your username: " + user
    print "Serial number of your mfa device: " + serial
    conn.resync_mfa_device(user, serial, ac1, ac2)
    print "Resync MFA device successfull"
except boto.exception.BotoServerError as e:
    print "Resync MFA device failed: %s" % e
