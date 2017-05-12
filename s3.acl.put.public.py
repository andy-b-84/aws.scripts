#!/usr/bin/env python

#s3.acl.put.public.py

import sys, getopt, boto3, ssl, datetime
from datetime import datetime

# @see https://github.com/boto/boto/issues/2836#issuecomment-68608362
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

class bcolors:
    LIGHT_CYAN = '\033[96m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    YELLOW = '\033[33m'
    LIGHT_RED = '\033[91m'
    RED = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def usage():
    print bcolors.YELLOW + 'Usage:' + bcolors.ENDC
    print '  ./s3.acl.put.public.py <bucket> -p <prefix> -i <access_key_id> -k <secret_access_key>'
    print '  browse every file in <bucket> to add a "PUBLIC_READ" ACL on them.'
    print bcolors.YELLOW + 'Arguments:' + bcolors.ENDC
    print '  bucket' + bcolors.ENDC + "\t\t\tThe bucket to browse"
    print bcolors.YELLOW + 'Options:' + bcolors.ENDC
    print '  -p|--prefix\t\t\tprefix objects must have in their keys (folder name if S3 was seen as a FS)'
    print '  -i|--access_key_id\t\tboth -i and -k must be set at the same time, or none'
    print '  -k|--secret_access_key\tboth -i and -k must be set at the same time, or none'

def main(bucket_name, argv):
    try:
        opts, args = getopt.getopt(argv, "hp:i:k:", ["help", "prefix=", "access_key_id=", "secret_access_key="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if bucket_name in ('-h', '--help'):
        usage()
        sys.exit(0)

    access_key_id = ''
    secret_access_key = ''
    prefix = ''

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-p', '--prefix'):
            prefix = arg
        elif opt in ('-i', '--access_key_id'):
            access_key_id = arg
        elif opt in ('-k', '--secret_access_key'):
            secret_access_key = arg

    if (secret_access_key != '') != (access_key_id != ''):
        print bcolors.RED + 'Error: ' + bcolors.ENDC + 'Either access_key_id and secret_access_key cannot be set separately,'
        print '  both must be set at the same time, or none.'
        usage()
        sys.exit(2)

    # @see https://github.com/wavycloud/pyboto3
    if secret_access_key != '':
        client = boto3.client(
            's3',
            aws_access_key_id = access_key_id,
            aws_secret_access_key = secret_access_key,
            region_name = 'eu-west-1'
        )
        """ :type : pyboto3.s3 """
    else:
        client = boto3.client('s3')
        """ :type : pyboto3.s3 """

    s3 = boto3.resource('s3')
    """ :type : pyboto3.resource """
    api_client = s3.meta.client

    isTruncated = True
    lastKey = ''
    total = 0
    start = datetime.now()

    while isTruncated:
        files = client.list_objects(
            Bucket = bucket_name,
            Prefix = prefix,
            Marker = lastKey#,
            #MaxKeys=10
        )
        for content in files['Contents']:
            lastKey = content['Key'].replace(' ', '+')
            print lastKey
            total += 1
            api_client.put_object_acl(
                ACL = 'public_read',
                Bucket = bucket_name,
                Key = lastKey
            )
        end = datetime.now()
        delta = end - start
        print "{} fichiers mis a jour. Duree : {}".format(total, delta.total_seconds())

    end = datetime.now()
    delta = end - start

    print "{} fichiers mis a jour, au total. Duree totale : {}".format(total, delta.total_seconds())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print bcolors.RED + 'Error: ' + bcolors.ENDC + 'need a bucket name'
        usage()
        sys.exit(2)
    main(sys.argv[1], sys.argv[2:])