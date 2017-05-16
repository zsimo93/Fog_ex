echo "Installing Docker"
curl -sSL https://get.docker.com | sh

echo "Pulling Mosquitto"
docker pull docker pull ffaerber/mqtt-broker-on-arm

echo "Pulling nginx web server"
docker pull tiangolo/uwsgi-nginx-flask:flask-upload

