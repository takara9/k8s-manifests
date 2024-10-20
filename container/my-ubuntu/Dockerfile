FROM ubuntu:18.04
RUN apt update -y && apt install -y net-tools iputils-ping iputils-tracepath dnsutils iproute2 traceroute
RUN apt install -y --no-install-recommends mysql-client
RUN apt install -y s3cmd
CMD ["/usr/bin/tail","-f", "/dev/null" ]
