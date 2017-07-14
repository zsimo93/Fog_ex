FROM  resin/raspberry-pi-python:2.7-slim

RUN pip install --no-cache-dir gevent==1.2.1 flask==0.12 

ENV FLASK_PROXY_PORT 8080

RUN mkdir -p /pythonAction
ADD actionproxy.py /pythonAction/
RUN mkdir -p /action

CMD ["/bin/bash", "-c", "cd pythonAction && python -u actionproxy.py"]
