#!/usr/bin/python

import ConfigParser
import sys
from slipstream.api import Api
import os

context_file = "/opt/slipstream/client/bin/slipstream.context"

deployment_params_filter="deployment/href='{}' and name='{}'"

#
# Read the configuration.
#

config = ConfigParser.RawConfigParser()
config.read(context_file)

api_key = config.get('contextualization', 'api_key')
api_secret = config.get('contextualization', 'api_secret')
service_url = config.get('contextualization', 'serviceurl')
deployment_id = config.get('contextualization', 'diid')

#
# Setup the SlipStream API.
#

api = Api(endpoint=service_url)
api.login_apikey(api_key, api_secret)

# Recover deployment information. 

deployment = api.cimi_get(deployment_id)

try:
  service_offers = deployment.json['serviceOffers']
except KeyError:
  service_offers = []
  
#
# setup directories for object links
#

buckets_base_path = '/mnt/'
if not os.path.exists(buckets_base_path):
  os.makedirs(buckets_base_path)

data_path='/usr/share/nginx/html/'
if not os.path.exists(data_path):
  os.makedirs(data_path)

#
# mount the buckets containing the requested objects
#

for so in service_offers:
  so_doc = api.cimi_get(so)
  so_bucket = so_doc.json['data:bucket']
  so_object = so_doc.json['data:object']

  bucket_mount_point = buckets_base_path + so_bucket
  
  if not os.path.exists(bucket_mount_point):
    os.makedirs(bucket_mount_point)

  os.system('ln -s {0}/{1} {3}{2}__{1}'.format(bucket_mount_point, so_object, so_bucket, data_path))
