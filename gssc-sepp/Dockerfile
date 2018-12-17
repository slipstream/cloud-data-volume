
FROM sixsq/gssc-sepp:latest

RUN apt-get update && apt-get install -y python python-pip

RUN mkdir -p /opt/slipstream/bin
ADD link-data.py /opt/slipstream/bin/link-data.py
RUN chmod a+x /opt/slipstream/bin/link-data.py

ADD tailf.sh /tailf.sh
RUN chmod a+x /tailf.sh
ENTRYPOINT ["/tailf.sh"]
