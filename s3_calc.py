#!/usr/bin/python

import sys
import ssl
import boto
import time
import operator
from collections import defaultdict

def convert_to_gb(size):
    return float(size)/(1024*1024*1024)

def convert_to_mb(size):
    return float(size)/(1024*1024)

def main():
    start_time = time.time()

    if hasattr(ssl, '_create_unverified_context'):
       ssl._create_default_https_context = ssl._create_unverified_context

    s3_bucket = sys.argv[1]
    key_prefix = sys.argv[2]
    s3conn = boto.connect_s3()
    bucket = s3conn.get_bucket(s3_bucket)

    rs = bucket.list(key_prefix)

    total_size = 0
    dir_data = defaultdict(int)

    print "\nDirectory List for  %s:\n" % key_prefix 

    for key in rs:
        total_size += key.size
        key_path = str(key.name).split(key_prefix)[1]
        split_key_path = key_path.split('/')
        if len(split_key_path) > 2:
            dir_name = split_key_path[1]
            dir_data[dir_name] += key.size
    
    dir_data_sorted = sorted(dir_data.items(), key=operator.itemgetter(1), \
        reverse=True)
    for dir_name, dir_size in dir_data_sorted:
        dir_size_mb = convert_to_mb(dir_size)
        if dir_size_mb > 50:
            print "%s: %.2f MB" % (dir_name, dir_size_mb)

    print "\nSummary\n" + "-" * 30 + "\n"
    print "Total size: %s (%.2f GB)" % (total_size, convert_to_gb(total_size))
    print "Time taken: %s seconds" % (time.time() - start_time) 

    return 0

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: {0} \"S3_BUCKET\" \"KEY_PREFIX\" (Ex:{0} my_bucket production/new_customer)".format(sys.argv[0])
        sys.exit(0)
    sys.exit(main())
