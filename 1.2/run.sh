#!/bin/bash

SERVER_CONTAINER="z36_pserver1"
SERVER_IMAGE="z36_pserver1:latest"
CLIENT_CONTAINER="z36_cclient1"
CLIENT_IMAGE="z36_cclient1"

# Stworzenie pliku o 10000B
head -c 10000 /dev/urandom > Client/file.bin

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

# Uruchomienie serwera w tle
docker run -dit --network z36_network --network-alias z36_cserver1 --name $SERVER_CONTAINER $SERVER_IMAGE
