docker run --name mongoDB -v /home/$USER/mongo:/data/db:z --network host -d mongo --replSet foo


jixer/rpi-mongo