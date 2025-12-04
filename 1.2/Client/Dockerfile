FROM gcc:4.9

WORKDIR /app
COPY . .

RUN gcc -o udp_client udp_client.c -lcrypto

ENTRYPOINT ["./udp_client"]