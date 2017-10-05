git pull
#docker pull zsimo/python-image:imageProc
#docker pull zsimo/python-image:base
#docker pull zsimo/python-image:ffmpeg

echo "Enter role [ENTER]:"
read role
export TH_ROLE=$role

docker run --name mongoDB --network host -d zsimo/rpi-mongo --replSet foo

echo "Enter MASTER IP [ENTER]:"
read ip
export TH_MASTERIP=$ip

echo "Enter name for node [ENTER]:"
read name
export TH_NODENAME=$name

export BASE_DIR=`pwd`

if [ "$TH_ROLE" = "MASTER" ]; then
    python main.py $ip
else
    echo "Enter local ip [ENTER]:"
    read localip
    curl -i \
        -H "Accept: application/json" \
        -H "Content-Type:application/json" \
        -X POST --data '{"type": "node", "setup": false, "ip": '"$localip"'", "architecture": "arm", "name": '"$name"'", "role": "NODE" }' \
        "$ip:8080/api/nodes"

    python main.py
fi

docker stop mongoDB
docker rm -v mongoDB
rm -rf /tmp/*
