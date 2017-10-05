FROM cseelye/rpi-nginx-uwsgi-flask

#Run mounting -v /var/run/docker.sock:/var/run/docker.sock
# -e TH_ROLE='MASTER'|'NODE'

RUN sudo apt-get update && sudo apt-get install wget
RUN wget -qO- https://get.docker.com | sh
RUN pip install \
            docker==2.4.2 \
            pymongo==3.4.0 \
            boto3==1.4.4
RUN sudo apt-get install python-psutil zip

ADD main_docker.py /app
ADD core /app/core
ADD uwsgi-app.ini /app

EXPOSE 8080
EXPOSE 9999
WORKDIR /app
CMD ["python", "main_docker.py", "&", "disown", "&&", "/usr/bin/supervisord"]
