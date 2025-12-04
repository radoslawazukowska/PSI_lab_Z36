#!/bin/bash

USER_NAME="$USER"

SERVER_CONTAINER="z36_pserver1"
CLIENT_CONTAINER="z36_cclient1"

CLIENT_LOCAL_PATH="/home/users/$USER_NAME/PSI_lab_Z36/1.2/Client"
FILE_NAME="file.bin"

# Stworzenie pliku o 10000B
head -c 10000 /dev/urandom > $CLIENT_LOCAL_PATH/$FILE_NAME

# Usunięcie kontenera, jeśli istnieje
docker rm -f $SERVER_CONTAINER $CLIENT_CONTAINER 2>/dev/null || true

docker compose up --build
