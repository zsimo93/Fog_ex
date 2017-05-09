cd /media/sf_Simone/workspace_thesis
docker run -it -p 1883:1883 -p 9001:9001 \
    -v /media/sf_Simone/workspace_thesis/mosquitto/config/mosquitto.conf:/mosquitto/config/mosquitto.conf \
    -v /mosquitto/data \
    -v /mosquitto/log eclipse-mosquitto