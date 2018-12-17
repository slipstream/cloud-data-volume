
FROM registry:latest

RUN apk add --update python py-pip

ADD tailf.sh /tailf.sh
RUN chmod a+x /tailf.sh
ENTRYPOINT ["/tailf.sh"]
