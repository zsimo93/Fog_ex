generate_post_data()
{
  cat <<EOF
{
"type": "node",
"setup": false,
"ip": "$localip",
"architecture": "arm",
"name": "$name",
"role": "NODE"
}
EOF
}


echo "Enter role [ENTER]:"
read role

docker run --name mongoDB --network host -d zsimo/rpi-mongo --replSet foo

echo "Enter MASTER IP [ENTER]:"
read ip
echo "Enter name for node [ENTER]:"
read name

if [ "$TH_ROLE" = "MASTER" ]; then
    echo "running Master"
else
    echo "Enter local ip [ENTER]:"
    read localip
    curl -i \
        -H "Accept: application/json" \
        -H "Content-Type:application/json" \
        -X POST --data "$(generate_post_data)" "$ip:8080/api/nodes"

docker run --name coreGateway --network host \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e TH_ROLE=$role -e TH_MASTERIP=$ip -e BASE_DIR="/app" \
    -e TH_NODENAME=$name \
    -p 8080:8008 -p 9999:9999 \
    zsimo/thesis
