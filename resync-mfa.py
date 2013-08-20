#!/usr/bin/python

import boto
from sys import argv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('<username>')
parser.add_argument('<auth_code_1>')
parser.add_argument('<auth_code_2>')
args = parser.parse_args()

user = argv[1]
auth_code_1 = argv[2]
auth_code_2 = argv[3]
conn = boto.connect_iam()
mfa = conn.get_all_mfa_devices(user)
serial = mfa["list_mfa_devices_response"]["list_mfa_devices_result"]["mfa_devices"][0]["serial_number"]
print "your username: " + user
print "Serial number of your mfa device: " + serial
if conn.resync_mfa_device(user,serial, auth_code_1,auth_code_2):
	print "Resync MFA device successfull"
else:
	print "Resync MFA device failed"
