FROM ubuntu:18.04
RUN apt update && apt install -y s3fs python python-pip
RUN pip install slipstream-api
RUN pip install slipstream-client
ADD mount-data.py
RUN chmod a+x mount-data.py
Run ./mount-data.py 
VOLUME /data
WORKDIR / 
ENTRYPOINT ["mount-data.py"]
