echo "Enter role [ENTER]:"
read role

TH_ROLE=$role
export TH_ROLE

docker run --name mongoDB --network host -d zsimo/rpi-mongo --replSet foo


if [ "$TH_ROLE" = "MASTER" ]; then
    echo "Enter local IP [ENTER]:"
    read ip
    python main.py $ip
else
    echo "Add the node to the system and when done press [ENTER]"
    read enter
    python main.py
fi

docker stop mongoDB
docker rm mongoDB
rm -rf /tmp/*
