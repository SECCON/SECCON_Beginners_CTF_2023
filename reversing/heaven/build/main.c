#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/random.h>

char message[256];
uint8_t sbox[] = {
    194, 83,  187, 128, 46,  95,  30,  181, 23,  17,  0,   158, 36,  197, 205,
    210, 126, 57,  198, 26,  65,  82,  169, 153, 3,   105, 139, 115, 111, 160,
    241, 216, 245, 67,  125, 14,  25,  148, 185, 54,  123, 48,  37,  24,  2,
    167, 219, 179, 144, 152, 116, 170, 163, 32,  234, 114, 162, 142, 20,  91,
    35,  150, 98,  164, 70,  34,  101, 122, 8,   246, 18,  172, 68,  233, 40,
    141, 254, 132, 195, 227, 251, 21,  145, 58,  143, 86,  235, 51,  109, 10,
    49,  39,  84,  249, 74,  243, 191, 75,  218, 104, 161, 60,  255, 56,  166,
    62,  183, 192, 154, 53,  202, 9,   184, 140, 222, 28,  12,  50,  42,  15,
    130, 173, 100, 69,  133, 209, 175, 217, 252, 180, 41,  1,   155, 96,  117,
    206, 79,  200, 204, 226, 228, 247, 212, 4,   103, 146, 229, 199, 52,  13,
    240, 147, 44,  213, 221, 19,  149, 129, 136, 71,  157, 11,  31,  94,  93,
    168, 231, 5,   106, 237, 43,  99,  47,  76,  203, 232, 201, 90,  220, 196,
    176, 225, 127, 159, 6,   230, 87,  190, 189, 193, 236, 89,  38,  244, 177,
    22,  134, 215, 112, 55,  77,  113, 119, 223, 186, 248, 59,  85,  156, 121,
    7,   131, 151, 214, 110, 97,  29,  27,  165, 64,  171, 188, 107, 137, 174,
    81,  120, 182, 178, 253, 250, 211, 135, 239, 238, 224, 45,  78,  63,  108,
    102, 92,  124, 16,  207, 73,  72,  33,  138, 61,  242, 118, 208, 66,  80,
    88,  0};

uint8_t calc_xor(uint8_t a, uint8_t b);

void encrypt_message(uint8_t key, char *s, size_t len) {
  for (size_t i = 0; i < len; i++) {
    s[i] = sbox[calc_xor(s[i], key)];
  }
}

void print_hexdump(char *s, size_t len) {
  for (size_t i = 0; i < len; i++) {
    printf("%02x", (uint8_t)s[i]);
  }
  printf("\n");
}

int main() {
  size_t len;
  uint8_t key;
  char buf_n[8];

  getrandom(&key, sizeof(key), 0);

  for (;;) {
    printf("------ menu ------\n");
    printf("0: encrypt message\n");
    printf("1: decrypt message\n");
    printf("2: exit\n");
    printf("> ");

    if (!fgets(buf_n, sizeof(buf_n), stdin)) {
      break;
    }
    switch (atoi(buf_n)) {
    case 0:
      printf("message: ");
      fgets(message, sizeof(message), stdin);
      len = strlen(message);
      if (len == 0) {
        break;
      }
      encrypt_message(key, message, len - 1);
      printf("encrypted message: %02x", key);
      print_hexdump(message, len - 1);
      break;
    case 1:
      printf("TODO: implement decrypt_message()\n");
      break;
    case 2:
      return 0;
    default:
      break;
    }
  }

  return 0;
}
