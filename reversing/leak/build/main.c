#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define BUFFER_SIZE 1024

void encrypt(unsigned char *data, size_t data_len, const unsigned char *key,
             size_t key_len) {
  unsigned char state[256];
  unsigned char x, y, tmp;
  unsigned int i, j;

  // 初期化
  for (i = 0; i < 256; i++) {
    state[i] = (i + 53) % 256; // custom RC4 +53 into init state
  }

  // 鍵スケジュール
  for (i = 0, j = 0; i < 256; i++) {
    j = (j + key[i % key_len] + state[i]) & 0xFF;
    tmp = state[i];
    state[i] = state[j];
    state[j] = tmp;
  }

  // 暗号化
  x = y = 0;
  for (i = 0; i < data_len; i++) {
    x = (x + 1) & 0xFF;
    y = (y + state[x]) & 0xFF;
    tmp = state[x];
    state[x] = state[y];
    state[y] = tmp;
    data[i] ^= state[(state[x] + state[y]) & 0xFF];
  }
}

int main() {
  // IPアドレスの入力
  char ipAddress[16];
  printf("Enter IP address: ");
  if (fgets(ipAddress, sizeof(ipAddress), stdin) == NULL) {
    perror("Failed to read IP address");
    return 1;
  }
  // 改行文字の削除
  size_t len = strlen(ipAddress);
  if (len > 0 && ipAddress[len - 1] == '\n') {
    ipAddress[len - 1] = '\0';
  }

  // ファイルの読み込み
  FILE *file = fopen("/tmp/flag", "r");
  if (file == NULL) {
    perror("Failed to open file");
    return 1;
  }

  // ファイル内容の取得
  char buffer[BUFFER_SIZE];
  size_t bytesRead = fread(buffer, 1, BUFFER_SIZE, file);
  fclose(file);

  // RC4キーと暗号化処理の初期化
  const char *rc4Key = "KEY{th1s_1s_n0t_f1ag_y0u_need_t0_f1nd_rea1_f1ag}";
  size_t rc4KeyLen = strlen(rc4Key);

  // バッファの内容をRC4で暗号化
  encrypt((unsigned char *)buffer, bytesRead, (const unsigned char *)rc4Key,
          rc4KeyLen);

  // ソケットの作成
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd == -1) {
    perror("Failed to create socket");
    return 1;
  }

  // 送信先のアドレスとポートの設定
  struct sockaddr_in serverAddr;
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(5000);
  if (inet_pton(AF_INET, ipAddress, &(serverAddr.sin_addr)) <= 0) {
    perror("Invalid address/Address not supported");
    return 1;
  }

  // サーバに接続
  if (connect(sockfd, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) ==
      -1) {
    perror("Failed to connect to server");
    return 1;
  }

  // データの送信
  ssize_t bytesSent = send(sockfd, buffer, bytesRead, 0);
  if (bytesSent == -1) {
    perror("Failed to send data");
    return 1;
  }

  printf("Data sent successfully\n");

  // ソケットのクローズ
  close(sockfd);

  return 0;
}
