FROM cseelye/rpi-nginx-uwsgi-flask

#Run mounting -v /var/run/docker.sock:/var/run/docker.sock

RUN wget -qO- https://get.docker.com | sh

RUN pip install \
            docker \
            pymongo \
            

EXPOSE 8080
