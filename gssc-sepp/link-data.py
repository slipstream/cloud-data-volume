#!/usr/bin/python

import ConfigParser
import sys
from slipstream.api import Api
import os
import re

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


def mkdirIfMissing(dirname):
  if not os.path.exists(dirname):
    os.makedirs(dirname)


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
mkdirIfMissing(buckets_base_path)

data_path='/gssc/data/slipstream/'


#
# mount the buckets containing the requested objects
#

for so in service_offers:
  so_doc = api.cimi_get(so)
  so_id = so_doc.json['id']

  for ds in service_offers[so_id]:
    dataset_folder = re.sub("/", "_", ds)
    mkdirIfMissing(data_path + dataset_folder)

    so_bucket = so_doc.json['data:bucket']
    so_object = so_doc.json['data:object']

    so_name = so_doc.json['name']

    folder = re.sub("[^a-z0-9]", "_", so_name.lower())

    full_data_path = '{0}{1}/{2}/'.format(data_path, dataset_folder, folder)

    bucket_mount_point = buckets_base_path + so_bucket

    mkdirIfMissing(bucket_mount_point)
    mkdirIfMissing(full_data_path)

    os.system('ln -s {0}/{1} {3}{2}__{1}'.format(bucket_mount_point, so_object, so_bucket, full_data_path))
