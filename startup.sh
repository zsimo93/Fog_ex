echo "Enter role [ENTER]:"
read role

TH_ROLE=$role
export TH_ROLE

docker run --name mongoDB --network host -d jixer/rpi-mongo --replSet foo

python main.py
