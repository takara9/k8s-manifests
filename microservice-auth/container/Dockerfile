FROM ubuntu:18.04
WORKDIR /
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    python3 python3-pip \
    emacs25-nox git curl

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/fai555/Istio-and-JWT

COPY apl.py ./
CMD [ "python3", "./apl.py" ]
