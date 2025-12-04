FROM gcc:4.9
COPY . /Client
WORKDIR /app
RUN gcc -o udp_client udp_client.c -lssl -lcrypto
ENTRYPOINT ["./udp_client"]