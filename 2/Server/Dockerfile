FROM gcc:4.9
WORKDIR /app
COPY ./tcp_server.c .
RUN gcc -g ./tcp_server.c -o tcp_server -lssl -lcrypto
ENTRYPOINT [ "./tcp_server"]
