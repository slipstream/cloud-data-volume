#!/usr/bin/env python

import sys
import os
from nuvla.api import Api

deployment_params_filter="deployment/href='{}' and name='{}'"

#
# Read the configuration from the environment.
#

endpoint = os.getenv('NUVLA_ENDPOINT')
api_key = os.getenv('NUVLA_API_KEY')
api_secret = os.getenv('NUVLA_API_SECRET')
deployment_id = os.getenv('NUVLA_DEPLOYMENT_ID')

#
# Ensure complete environment or bail out.
#

if (endpoint is None or
    api_key is None or
    api_secret is None or
    deployment_id is None):
  print("missing required configuration information; skipping data link configuration...")
  sys.exit()

#
# Setup the Nuvla API.
#

api = Api(endpoint=endpoint)
api.login_apikey(api_key, api_secret)

# Recover deployment information. 

deployment = api.get(deployment_id)

try:
  service_offers = deployment.data['service-offers']
except KeyError:
  service_offers = []
  
#
# setup directories for object links
#

buckets_base_path = '/mnt/'
if not os.path.exists(buckets_base_path):
  os.makedirs(buckets_base_path)

data_path='/gssc/data/nuvla/'
if not os.path.exists(data_path):
  os.makedirs(data_path)

#
# mount the buckets containing the requested objects
#

for so in service_offers:
  so_doc = api.get(so)
  so_bucket = so_doc.data['data:bucket']
  so_object = so_doc.data['data:object']

  bucket_mount_point = buckets_base_path + so_bucket
  
  if not os.path.exists(bucket_mount_point):
    os.makedirs(bucket_mount_point)

  os.system('ln -s {0}/{1} {3}{2}__{1}'.format(bucket_mount_point, so_object, so_bucket, data_path))
