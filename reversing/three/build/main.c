#include <stdio.h>
#include <string.h>

/* ctf4b{c4n_y0u_ab1e_t0_und0_t4e_t4ree_sp1it_f14g3} */

#define FLAG_LENGTH 49

const int flag_0[17] = {99,  52, 99,  95, 117, 98, 95, 95, 100,
                        116, 95, 114, 95, 49,  95, 52, 125};
const int flag_1[16] = {116, 98, 52,  121, 95,  49,  116, 117,
                        48,  52, 116, 101, 115, 105, 102, 103};
const int flag_2[16] = {102, 123, 110, 48,  97,  101, 48, 110,
                        95,  101, 52,  101, 112, 116, 49, 51};

int validate_flag(const char *str) {
  if (strlen(str) != FLAG_LENGTH) {
    printf("Invalid FLAG\n");
    return 1;
  }

  for (int i = 0; i < FLAG_LENGTH; i++) {
    const char expected_char = (i % 3 == 0)   ? flag_0[i / 3]
                               : (i % 3 == 1) ? flag_1[i / 3]
                                              : flag_2[i / 3];
    if (str[i] != expected_char) {
      printf("Invalid FLAG\n");
      return 1;
    }
  }

  printf("Correct!\n");
  return 0;
}

int main() {
  char str[FLAG_LENGTH + 1]; // Allocate space for null terminator
  printf("Enter the FLAG: ");
  scanf("%49s", str);
  return validate_flag(str);
}
