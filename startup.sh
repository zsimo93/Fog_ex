git pull

arch=`uname -a`
if [[ $arch == *"arm"* ]];
then
    echo "ARM detected"
    #docker pull zsimo/python-image:imageProc
    #docker pull zsimo/python-image:base
    #docker pull zsimo/python-image:ffmpeg
    docker run --name mongoDB --network host -d zsimo/rpi-mongo --replSet foo
    arch="arm";
else
    echo "x86 detected"
    #docker pull zsimo/python-image:imageProc_x86
    #docker pull zsimo/python-image:base_x86
    #docker pull zsimo/python-image:ffmpeg_x86
    docker run --name mongoDB --network host -d mongo:3.0.15 --replSet foo
    arch="x86";
fi
export TH_ARCH=$arch

echo "Enter role [ENTER]:"
read role
export TH_ROLE=$role

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
    python attach_node.py "http://$ip:8080/api/nodes" $localip $name $arch

    python main.py
fi

docker stop mongoDB
docker rm -v mongoDB
rm -rf /tmp/*
