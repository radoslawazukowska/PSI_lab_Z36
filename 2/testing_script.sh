#!/bin/bash

docker network create z36_network # !LOKALNIE!

cd Server
docker build -t tcp_server_image .
docker run -dit --network z36_network --name server tcp_server_image:latest

sleep(2)

cd ../Client
docker build -t tcp_parallel_clients_image .
docker run -it --network z36_network --name parallel_clients tcp_parallel_clients_image server 8888

echo -e "\n--- SERVER LOGS ---"
docker logs server

docker rm -f server parallel_clients
docker rmi tcp_server_image tcp_parallel_clients_image
