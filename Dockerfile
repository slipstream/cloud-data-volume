FROM sixsq/gssc-sepp:latest
RUN apt-get update && apt-get install -y s3fs python python-pip virtualenv
RUN virtualenv -p python2.7 /root/slipstream-env
RUN . /root/slipstream-env/bin/activate && pip install slipstream-api slipstream-client
RUN mkdir -p /opt/slipstream/bin
ADD mount-data.py /opt/slipstream/bin/mount-data.py
RUN chmod a+x /opt/slipstream/bin/mount-data.py
ADD startup.sh /opt/slipstream/bin/startup.sh
RUN chmod a+x /opt/slipstream/bin/startup.sh
RUN mkdir -p /opt/python/bin/
RUN ln -s /usr/bin/python2.7 /opt/python/bin/python

#ENTRYPOINT ["/opt/slipstream/bin/startup.sh"]
ENTRYPOINT ["tail" "-f" "/dev/null"]
