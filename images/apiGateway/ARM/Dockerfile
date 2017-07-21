FROM cseelye/rpi-nginx-uwsgi-flask

#Run mounting -v /var/run/docker.sock:/var/run/docker.sock
# -e TH_ROLE='MASTER'|'NODE'

RUN wget -qO- https://get.docker.com | sh
RUN pip install \
            docker==2.4.2 \
            pymongo==3.4.0 \
            boto3==1.4.4
run sudo apt-get install python-psutil
            

EXPOSE 8080, 9999

