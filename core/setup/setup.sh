echo "Installing Docker"
#curl -sSL https://get.docker.com | sh
groupadd docker &&
usermod -aG docker $USER
echo "Pulling nginx web server"
#docker pull tiangolo/uwsgi-nginx-flask:flask-upload
#mount socket to use docker in docker.
#also install docker in container.
#docker run -v /var/run/docker.sock:/var/run/docker.sock -d apiGateway
