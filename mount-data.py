#!/usr/bin/python

import argparse
import ConfigParser
import sys
from slipstream.api import Api
import os

s3_mount_cmd = 's3fs {0} {1} -o ro -o nonempty -o passwd_file={2} -o url={3} -o use_path_request_style'

deployment_params_filter="deployment/href='{}' and name='{}'"

#
# Define parser and parse command line arguments.
#

parser = argparse.ArgumentParser(description='Create and serve directory with mounted S3 objects.')

parser.add_argument('--service-url', dest='service_url', metavar='URL',
                    default='https://nuv.la',
                    help='SlipStream service url')
parser.add_argument('--key', dest='api_key', metavar='KEY',
                    required=True,
                    help='API key')
parser.add_argument('--secret', dest='api_secret', metavar='SECRET',
                    required=True,
                    help='API secret')
parser.add_argument('--id', dest='deployment_id', metavar='ID',
                    required=True,
                    help='deployment identifier')

args = parser.parse_args()

#
# Setup the SlipStream API.
#

api = Api(endpoint=args.service_url)
api.login_apikey(args.api_key, args.api_secret)

# Recover deployment information. 

deployment = api.cimi_get(args.deployment_id)
service_offers = deployment.json['serviceOffers']

# Recover credential for mounting buckets.

depl_params = api.cimi_search('deploymentParameters',
                              filter=deployment_params_filter.format(args.deployment_id, 'credential.id'))


credential_id = depl_params.resources_list[0].json['value']

credential = api.cimi_get(credential_id)
credential_key = credential.key
credential_secret = credential.secret

connector_ref = credential.json['connector']['href']

connector = api.cimi_get(connector_ref)

object_store_endpoint = connector.json['objectStoreEndpoint']

#
# create password file for s3fs
#

tmp_path = '/tmp/slipstream/'
if not os.path.exists(tmp_path):
  os.makedirs(tmp_path)

passwd_file_path = tmp_path + 'passwd-s3fs'
passwd = '{}:{}'.format(credential_key, credential_secret)
passwd_file = open(passwd_file_path, 'w+')
passwd_file.write(passwd)
passwd_file.close()
os.chmod(passwd_file_path, 0600)

#
# setup directories for mounts and object links
#

buckets_base_path = '/buckets/'
if not os.path.exists(buckets_base_path):
  os.makedirs(buckets_base_path)

data_path='/data/'
if not os.path.exists(data_path):
  os.makedirs(data_path)

#
# mount the buckets containing the requested objects
#

for so in service_offers:
  so_doc = api.cimi_get(so)
  so_bucket = so_doc.json['resource:bucket']
  so_object = so_doc.json['resource:object']

  bucket_mount_point = buckets_base_path + so_bucket
  
  if not os.path.exists(bucket_mount_point):
    os.makedirs(bucket_mount_point)
    cmd = s3_mnt_cmd.format(so_bucket, bucket_mount_point, passwd_file_path, object_store_endpoint)
    os.system(cmd)
  os.system('ln -s {0}/{1} {3}{2}__{1}'.format(bucket_mount_point, so_object, so_bucket, data_path))
  
#
# FIXME: attach to s3fs foreground process instead
#

# os.chdir('tail /dev/null')
