echo "Enter role [ENTER]:"
read role

TH_ROLE=$role
export TH_ROLE

docker run --name mongoDB --network host -d zsimo/rpi-mongo --replSet foo

echo "Enter local IP if MASTER [ENTER]:"
read ip
python main.py $ip

docker stop mongoDB
docker rm mongoDB
rm -rf /tmp/*
