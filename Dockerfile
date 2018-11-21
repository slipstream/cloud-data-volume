FROM ubuntu:18.04
WORKDIR / 
RUN apt update && apt install -y s3fs python python-pip
RUN pip install slipstream-api
RUN pip install slipstream-client
ADD mount-data.py mount-data.py
RUN chmod a+x mount-data.py
#ENTRYPOINT ["/mount-data.py"]
VOLUME /data
