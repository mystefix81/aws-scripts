#!/usr/bin/python

import boto.iam, boto.exception
import argparse

parser = argparse.ArgumentParser(description="Rotate Access Keys.")
parser.add_argument(
        "-u",
        "--user",
        required=True,
        help="The IAM user to rotate the key for."
        )
parser.add_argument(
        "-a",
        "--access_key_id",
        help="The access key to rotate and use for authentication."
        )
parser.add_argument(
        "-s",
        "--secret_access_key",
        help="The secret key to rotate and use for authentication."
        )

args = parser.parse_args()

if not args.access_key_id:
    args.access_key_id = raw_input("Enter Access Key: ")
if not args.secret_access_key:
    args.secret_access_key = raw_input("Enter Secret Key: ")

iam = boto.iam.connection.IAMConnection(
        aws_access_key_id=args.access_key_id,
        aws_secret_access_key=args.secret_access_key
        )

try:
    response = iam.create_access_key(args.user)
except boto.exception.BotoServerError as e:
    print "Cannot create new keys: %s" % e
    raise

access_key = response['create_access_key_response']['create_access_key_result']['access_key']
print """Access Key: %s
Secret Key. %s""" % (
        access_key['access_key_id'],
        access_key['secret_access_key']
        )

ans = raw_input("Ready to delete Access Key %s? (yes/no) " % args.access_key_id)

if ans == "yes":
    try:
        iam.delete_access_key(args.access_key_id, args.user)
    except boto.exception.BotoServerError as e:
        print "Cannot remove old key: %s" % e
        raise
else:
    print "Warning: your old Access Key was kept.  Be sure to clean up the mess."
