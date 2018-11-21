FROM ubuntu:18.04
RUN apt update && apt install -y s3fs
ADD mount-data.py
RUN chmod a+x mount-data.py
VOLUME /data
