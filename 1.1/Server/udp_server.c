#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>

#define resp "this is some confirmation"
#define DEFAULT_PORT 8001

void main(void)
{
    int sock, length;
    struct sockaddr_in server, client;
    socklen_t client_len;
    char buf[1024];

    sock = socket(AF_INET, SOCK_DGRAM, 0);

    if (sock == -1) {
        perror("opening datagram socket");
        exit(1);
    }

    /* Create server with wildcards. */
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = 0;

    if (bind(sock,(struct sockaddr *)&server, sizeof server) == -1) {
        perror("binding datagram socket");
        exit(1);
    }

    socklen_t slength = sizeof(server);
    if (getsockname(sock,(struct sockaddr *) &server, &slength) == -1) {
        perror("getting socket name");
        exit(1);
    }

    printf("Socket port #%d\n", ntohs( server.sin_port));

    while(1) {
        /* Read from the socket. */
        client_len = sizeof(client);
        int n = recvfrom(sock, buf, sizeof(buf), 0,
                        (struct sockaddr*) &client, &client_len);
        
        buf[n] = '\0';
        printf("-->%s\n", buf);
        /* Sending a confirmation. */
        if ( sendto(sock, resp, sizeof resp, 0,
            (struct sockaddr *) &client, sizeof(client)) == -1) {
            perror("receiving datagram packet");
        }
        printf("sent confirmation\n");
    }
    close(sock);
    exit(0);
}
