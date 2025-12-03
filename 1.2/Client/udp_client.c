#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define DATA "JAKIS SOBIE TEKST JSDnksanjndkdnfsdicuaa"
#define BSIZE 10000

void main(int argc, char *argv[])
{
    char *server_name = argv[1];
    int server_port = (argc > 2) ? atoi(argv[2]) : 8080;

    int sock, n, i;
    struct sockaddr_in server;
    char buf[BSIZE];
    struct hostent *hp;

    printf("Starting...\n");
    if ( (sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        perror("Socket creation failed");
        exit(1);
    }
    
    /* Server data */
    hp = gethostbyname(server_name);
    if (!hp)
    {
        fprintf(stderr, "%s: unknown host\n", argv[1]);
        exit(2);
    }

    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    memcpy((char *) &server.sin_addr, hp->h_addr_list[0], hp->h_length);
    server.sin_port = htons(server_port);

    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) < 0) {
        perror("connect");
        exit(1);
    }

    i = 0;
    while (i < 5)
    {
        printf("Przygotowanie do wyslania %d...\n", i);
        /* Send to server. */
        if (send(sock, DATA, strlen(DATA), 0) < 0)
            perror("error send");

        printf("Waiting for response...\n");

        n = recv(sock, buf, sizeof(buf)-1, 0);
        if (n < 0) {
            perror("Error in recv");
            continue;
        }
        buf[n] = '\0';
        printf("Got %d bytes from server -> %s\n", n, buf);
        i ++;
    }
    close(sock);
    exit(0);
}
