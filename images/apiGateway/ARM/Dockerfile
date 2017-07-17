FROM cseelye/rpi-nginx-uwsgi-flask

#Run mounting -v /var/run/docker.sock:/var/run/docker.sock
# -e TH_ROLE='MASTER'|'NODE'

RUN wget -qO- https://get.docker.com | sh
RUN pip install \
            docker \
            pymongo \
            boto3 \
            psutils
            

EXPOSE 8080, 9999

