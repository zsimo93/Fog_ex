FROM tgogos/ffmpeg

USER root

RUN apt-get update && \
    apt-get -qy install ca-certificates python python-pip && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get -qy clean all

RUN pip install --no-cache-dir gevent==1.2.1 flask==0.12 ffmpy
