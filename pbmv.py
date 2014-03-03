#!/usr/bin/python

from boto.s3.connection import S3Connection
import boto.exception
from Queue import Queue
from threading import Thread
from argparse import ArgumentParser
from sys import exit

def worker(queue):
    while True:
        srckey = queue.get()
        srcname = srckey.name
        dstname = "{}{}".format(args.dst_prefix, srcname)
        if not args.quiet:
            print "{} => {}".format(srcname, dstname)
        if not args.dry_run:
            bucket.copy_key(dstname, bucket.name, srcname)
            if args.move:
                srckey.delete()
        queue.task_done()

def main():
    parser = ArgumentParser(description="Parallel S3 copy/move.")
    parser.add_argument("-a", "--access_key_id", help="The access key to use for authentication.")
    parser.add_argument("-s", "--secret_access_key", help="The secret key to use for authentication.")
    parser.add_argument("-b", "--bucket", help="The bucket to work on.")
    parser.add_argument("-w", "--worker", type=int, default=16, help="The number of workers.")
    parser.add_argument("-m", "--move", action="store_true", help="Move files instead of copy.")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Do not actually touch the bucket.")
    parser.add_argument("-q", "--quiet", action="store_true", help="No output.")
    parser.add_argument("src_prefix", help="A key prefix to copy/move from.")
    parser.add_argument("dst_prefix", help="New key prefix.")

    args = parser.parse_args()

    if not args.access_key_id:
        args.access_key_id = raw_input("Enter Access Key: ")
    if not args.secret_access_key:
        args.secret_access_key = raw_input("Enter Secret Key: ")

    conn = S3Connection(
            args.access_key_id,
            args.secret_access_key
    )

    q = Queue(8*args.worker)

    for i in range(args.worker):
        t = Thread(target=worker, args=[q])
        t.daemon = True
        t.start()

    try:
        for bucket in conn.get_all_buckets():
            if bucket.name == args.bucket:
                break
    except boto.exception.S3ResponseError as e:
        print "Error: {} ({}/{}).".format(e.message, e.status, e.error_code)
        return 1


    for srckey in bucket.list(prefix=args.src_prefix):
        q.put(srckey)

    q.join()

if __name__ == "__main__":
    exit(main())
