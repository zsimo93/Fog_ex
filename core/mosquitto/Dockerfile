FROM eclipse-mosquitto

RUN sed -ri 's/^mosquitto:x:100:101:/mosquitto:x:1000:1000:/' /etc/passwd
