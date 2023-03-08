FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y sudo
RUN apt install -y software-properties-common
RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
RUN apt-get install -y mosquitto
WORKDIR /app/

# Copy public key to folder
COPY ./rsa_pub_key.der ./rsa_pub_key.der

# Copy JWT_Mosquitto_Auth pre-built release
COPY ./libmosquitto_jwt_auth.so ./libmosquitto_jwt_auth.so

COPY ./mosquitto.conf ./mosquitto.conf

CMD sudo mosquitto -c mosquitto.conf
