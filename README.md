
Container Integration
=====================

This repository shows the changes that must be added to standard
Docker containers to integrate them with SlipStream.

Generally the process is simple:

 1. Add a layer to the target container that installs Python 2.7 and
    `pip`.
 2. Change the entry point to `tail -f /dev/null` to prevent the
    modified container from exiting.

Once the modified container has been published to a registry, then do
the following within SlipStream (Nuvla):

 1. Create an image module for the modified container.
 2. Create a component module that references the image module and
    that uses the SlipStream client to get or to set parameters values
    via SlipStream.
 3. Launch the component from SlipStream to a configured Docker Swarm
    infrastructure.  

You can view the status of the container from SlipStream and access
any services that are running within it.

This repository contains the following example containers:

 - **gssc-sepp**: A Jupyter notebook application with many
   dependencies for GNSS signal analysis included.  This is a
   derivative of an Ubuntu container.
 - **nginx**: A standard Nginx web server that exposes the requested
   GNSS data.  This is a derivative of a Debian container.
 - **registry**: A Docker registry which is derived from an Alpine
   container.

The SlipStream modules (and "recipes") can be found in the `apps/GNSS`
directory of Nuvla.


    