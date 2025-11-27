#include <netdb.h>
#include <netinet/in.h>
#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define BSIZE 1024
#define PORT "8888"

void sigchld_handler(int sig) {
  while (waitpid(-1, NULL, WNOHANG) > 0)
    ;
}

void compute_sha256(char *msg, size_t msg_size, char *hash_hex) {
  unsigned char hash[SHA256_DIGEST_LENGTH];
  SHA256((unsigned char *)msg, msg_size, hash);

  int i;
  for (i = 0; i < SHA256_DIGEST_LENGTH; i++) {
    sprintf(hash_hex + (i * 2), "%02x", hash[i]);
  }
  hash_hex[SHA256_DIGEST_LENGTH * 2] = '\0';
}

int main(int argc, char *argv[]) {
  int sock, msgsock, rval, ListenQueueSize = 5;
  socklen_t length;
  struct addrinfo *bindto_address;
  struct addrinfo hints;
  struct sockaddr_in server;
  char buf[BSIZE];

  signal(
      SIGCHLD,
      sigchld_handler); // kernel signals parent to delete handled child process

  // Server info
  memset(&hints, 0, sizeof(hints)); // clear hints to avoid rubish memory data
  hints.ai_family = AF_INET;        // IPv4
  hints.ai_socktype = SOCK_STREAM;  // TCP
  hints.ai_flags = AI_PASSIVE;      // listen on all interfaces
  if (getaddrinfo(0, PORT, &hints, &bindto_address) == -1) {
    perror("getting local address");
    exit(1);
  }

  // Create socket from server info
  sock = socket(bindto_address->ai_family, bindto_address->ai_socktype,
                bindto_address->ai_protocol);
  if (sock == -1) {
    perror("opening TCP socket");
    exit(1);
  }

  // bind socket to ip address (Give the socket FD the local address ADDR)
  // bind(sock, (struct sockaddr *)&server, sizeof(server));
  if (bind(sock, bindto_address->ai_addr, bindto_address->ai_addrlen) == -1) {
    perror("binding TCP socket");
    exit(1);
  }

  freeaddrinfo(bindto_address); // bindto_address is no longer needed
  listen(sock, ListenQueueSize);
  printf("Server listening on port %s\n", PORT);

  // server accepts clients in the loop
  while (1) {
    msgsock = accept(sock, (struct sockaddr *)0,
                     (socklen_t *)0); // accept client's connection
    if (msgsock < 0) {
      perror("client connection");
      continue;
    }
    if (fork() == 0) { // client should be handled in child process
      close(sock);     // close unused socket so noone connects to this process
      printf("[PID %d] Connected\n", getpid());

      char *msg = NULL;
      size_t msg_size = 0;

      do { // until clients sends data, read it
        memset(buf, 0, BSIZE);
        if ((rval = recv(msgsock, buf, BSIZE, 0)) == -1) {
          perror("reading stream message");
          exit(1);
        }
        if (rval == 0)
          printf("[PID %d] Client disconnected after sending data\n", getpid());
        else {
          // accumulate all received data in msg
          msg = realloc(msg, msg_size + rval);
          memcpy(msg + msg_size, buf, rval);
          msg_size += rval;
        }
      } while (rval != 0);

      char hash_hex[SHA256_DIGEST_LENGTH * 2 + 1];
      compute_sha256(msg, msg_size, hash_hex);
      send(msgsock, hash_hex, strlen(hash_hex), 0);
      printf("[PID %d] Finished, hash sent\n", getpid());

      free(msg);
      close(msgsock);
      fflush(stdout);
      exit(0);
    }
    close(msgsock); // client is not using child's socket
  }
  close(sock);
  exit(0);
}
