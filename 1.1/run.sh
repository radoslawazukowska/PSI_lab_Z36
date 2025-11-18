#!/bin/bash

cd Server
docker build -t server1_docker .
docker run -dit --network z36_network --network-alias cserver1 --name cserver1 server1_docker:latest
cd ..
cd Client
docker build -t pclient1 .
docker run -it --network z36_network --name pclient1 pclient1 cserver1 54070
docker stop cserver1
docker container rm cserver1
docker container rm pclient1
