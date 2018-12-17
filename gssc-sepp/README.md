
# Cloud Data Volume

The container built from this repository will allow other container to
mount the volume exposed by this container. This volume contains the
S3 objects that have been specified in a SlipStream deployment.

As input, the container requires the following information:

 * `serviceurl`: defaults to https://nuv.la
 * `api_key`: API key to be used to access deployment information
 * `api_secret`: secret value paired with the API key
 * `deployment_id`: identifier for the deployment

The container will do (ideally) the following:

 * Download the deployment information from the SlipStream server.
 * Extract S3 bucket/object information from deployment.
 * Mount necessary S3 buckets (read only mode) on container.
 * Provide symbolic links in the `/data` directory to specified
   objects.
 * Export `/data` as a volume for use by other containers.

Client containers can simply reference the volume with the standard
Docker command line options.

# Starting the Container

To run the container use the following command:
```
docker build --tag s3data .

docker run --cap-add SYS_ADMIN --device /dev/fuse \
           s3data \
           --key ... \
           --secret ... \
           --id ... \
           --server-url ...
```

The `--key`, `--secret`, and `--id` options are required.  The
`--server-url` option will default to "https://nuv.la" if not
provided.

# Results

Tests were run to see if the container can provide the required
functionality.  The main conclusions are:

 * The s3fs fuse filesystem **can** be used to access the S3 objects
   within a container.
   
 * Doing so requires flags to add system administrator privileges to
   the container (SYS_ADMIN) and access to the FUSE device.  This may
   not be possible on a shared container infrastructure.

 * As noted in some other attempts to use s3fs with Docker, the
   mounted s3fs filesystem **cannot** be exported (usefully) as a
   volume. The volume is created and can be seen by other containers,
   but the actual objects cannot be accessed.

A demonstration of this implementation could be done on a private
container infrastructure (to allow for increased permissions) and on
containers that directly include and mount the s3fs filesystem.

Overall, this implementation does not provide a convenient, general
mechanism for accessing S3 objects via containers.

# Alternatives

 * Use the same scheme, but share the data via NFS (or GFS) instead of
   via Docker volumes.  This would work identically on both VMs and
   containers. However, it still has the disadvantage of needing
   increased privileges on container infrastructures.

 * Move to the s3fs RexRay Docker plugin.  This would provide the
   mounted S3 filesystem to containers as Docker volumes. Refactoring
   of the plugin could make it more object-oriented (rather than
   bucket-oriented) and less AWS-specific. As with the previous case,
   this would still require enhanced privileges for the plugin on the
   container infrastructure.

 * Investigate the use of external object URLs to provide access to
   the data. This would provide a lighter-weight client, but exposing
   the data via POSIX would still have the same privilege problems as
   for the other solutions using the FUSE filesystem.


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
