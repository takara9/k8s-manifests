FROM ubuntu:20.04

RUN apt-get -y update && apt install -y python3 python3-pip

WORKDIR /webapp
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt 

COPY webapp /webapp

CMD [ "python3", "/webapp/app.py" ]
