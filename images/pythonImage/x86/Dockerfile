FROM python:2.7-slim

RUN pip install --no-cache-dir gevent==1.2.1 flask==0.12 pymongo==3.4.0 Pillow

ENV FLASK_PROXY_PORT 8080

ADD fileModule.py /usr/local/lib/python2.7/
RUN mkdir -p /pythonAction
ADD actionproxy.py /pythonAction/
RUN mkdir -p /action

EXPOSE 8080

CMD ["/bin/bash", "-c", "cd pythonAction && python -u actionproxy.py"]