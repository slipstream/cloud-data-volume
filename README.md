
# Cloud Data Volume

The container built from this repository will allow other container to
mount the volume exposed by this container. This volume contains the
S3 objects that have been specified in a SlipStream deployment.

As input, the container requires the following information:

 * `serviceurl`: defaults to https://nuv.la
 * `api_key`: API key to be used to access deployment information
 * `api_secret`: secret value paired with the API key
 * `deployment_id`: identifier for the deployment

The container will do the following:

 * Download the deployment information from the SlipStream server.
 * Extract S3 bucket/object information from deployment.
 * Mount necessary S3 buckets (read only mode) on container.
 * Provide symbolic links in the `/data` directory to specified
   objects.
 * Export `/data` as a volume for use by other containers.

Client containers can simply reference the volume with the standard
Docker command line options.

## License

Copyright 2018, SixSq Sàrl

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.
