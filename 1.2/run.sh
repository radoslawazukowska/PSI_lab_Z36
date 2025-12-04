#!/bin/bash

USER_NAME="$USER"

SERVER_CONTAINER="z36_pserver1"
SERVER_IMAGE="z36_pserver1:latest"
CLIENT_CONTAINER="z36_cclient1"
CLIENT_IMAGE="z36_cclient1"

CLIENT_LOCAL_PATH="/home/users/$USER_NAME/PSI_lab_Z36/1.2/Client"

FILE_NAME="file.bin"

# Stworzenie pliku o 10000B
head -c 10000 /dev/urandom > $CLIENT_LOCAL_PATH/$FILE_NAME

# Usunięcie kontenera, jeśli istnieje
remove_container() {
    if [ $(docker ps -a -q -f name=$1) ]; then
        echo "Removing existing container $1..."
        docker rm -f $1
    fi
}

remove_container $SERVER_CONTAINER
remove_container $CLIENT_CONTAINER

docker build -t $SERVER_IMAGE ./Server
docker build -t $CLIENT_IMAGE ./Client

# Uruchomienie serwera w tle
docker run -dit --network z36_network --network-alias z36_cserver1 --name $SERVER_CONTAINER $SERVER_IMAGE

# Czekamy aż serwer wystartuje
sleep 10

# Uruchomienie klienta w bieżącym terminalu
docker run -it --network z36_network --name $CLIENT_CONTAINER -v $CLIENT_LOCAL_PATH:/input $CLIENT_IMAGE z36_cserver1 8888 /input/$FILE_NAME
