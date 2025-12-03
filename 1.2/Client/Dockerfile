FROM gcc:4.9
COPY . /Client
WORKDIR /Client/
RUN gcc -o udp_client1 udp_client.c
ENTRYPOINT ["./udp_client1"]