#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define _USE_RESOLVER
#define DEFAULT_SRV_IP "127.0.0.1"

#define FILE_SIZE 10000
#define PACKAGE_SIZE 100
#define ACK_SIZE 4
#define TIMEOUT_SEC 1

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
  if (argc < 4) {
    fprintf(stderr, "Usage: %s <server_name> <server_port> <file_path>\n",
            argv[0]);
    exit(1);
  }

  int sock, seq_num = 0;
  struct sockaddr_in server;
  struct hostent *hp;
  struct timeval tv;
  char file_data[FILE_SIZE];
  char packet_data_buf[PACKAGE_SIZE];
  char packet_with_ack[PACKAGE_SIZE + ACK_SIZE];
  char received_ack_buf[ACK_SIZE];

  printf("Client starting...\n");
  if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
    perror("Socket creation failed");
    exit(1);
  }

  memset(&server, 0, sizeof(server));
#ifdef USE_RESOLVER
  hp = gethostbyname(argv[1]);
  if (!hp) {
    fprintf(stderr, "%s: unknown host\n", argv[1]);
    exit(2);
  }
  memcpy((char *)&server.sin_addr, (char *)hp->h_addr, hp->h_length);
#else
  inet_aton(DEFAULT_SRV_IP, &server.sin_addr);
#endif
  server.sin_family = AF_INET;
  server.sin_port = htons(atoi(argv[2]));

  tv.tv_sec = TIMEOUT_SEC;
  tv.tv_usec = 0;
  setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

  if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
    perror("connect");
    exit(1);
  }

  FILE *fptr = fopen(argv[3], "rb");
  if (fptr == NULL) {
    perror("Not able to open the file.");
  }

  size_t nread;
  while ((nread = fread(packet_data_buf, 1, PACKAGE_SIZE, fptr)) > 0) {
    memcpy(file_data + seq_num * PACKAGE_SIZE, packet_data_buf, nread);
    int netseq = htonl(seq_num);
    memcpy(packet_with_ack, &netseq, ACK_SIZE);
    memcpy(packet_with_ack + ACK_SIZE, packet_data_buf, nread);

    while (1) {
      printf("Sending %d package to the server...", seq_num);

      if (send(sock, packet_with_ack, nread + ACK_SIZE, 0) < 0) {
        perror("send");
        continue;
      }
      if (recv(sock, received_ack_buf, ACK_SIZE, 0) < 0) {
        printf("Timeout, packet lost. Trying once again...");
        continue;
      }
      int ack_seq;
      memcpy(&ack_seq, received_ack_buf, ACK_SIZE);
      if (ntohl(ack_seq) == seq_num) {
        break;
      } else {
        printf("Wrong ACK. Trying once again...");
      }
    }
    seq_num++;
    memset(packet_data_buf, 0, sizeof(packet_data_buf));
  }
  int netseq = htonl(seq_num);
  if (send(sock, &netseq, ACK_SIZE, 0) < 0)
    perror("EOF send");

  char hash_hex[SHA256_DIGEST_LENGTH * 2 + 1];
  compute_sha256(file_data, FILE_SIZE, hash_hex);

  printf("Client streaming ended");
  printf("Client's hash: %s", hash_hex);

  fclose(fptr);
  close(sock);
  exit(0);
}
