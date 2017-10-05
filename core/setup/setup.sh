echo "Installing Docker"
curl -sSL https://get.docker.com | sh
usermod -aG docker $USER
sudo reboot

echo "Pulling nginx web server"
#docker pull tiangolo/uwsgi-nginx-flask:flask-upload
#mount socket to use docker in docker.
#also install docker in container.
docker run \
        -e TH_ROLE='NODE' \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -d funkit/apiGateway
