#!/bin/bash -xe

# create links for requested data objects
/root/link-data.py

# generate random access token
token=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

# FIXME: use fixed string until feedback is possible
token=sesame

# start service in the foreground with logging to console
cd /gssc
jupyter lab --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.token=$token
