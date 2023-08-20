#include <stdio.h>

// ctf4b{4ll_w3_h4v3_70_d3cide_1s_wh4t_t0_d0_w1th_7he_71m3_7h47_i5_g1v3n_u5}

int print_flag(void) {
  int enc[74] = {64, 87, 69, 23, 65, 92, 19, 75, 75, 120, 80, 20, 120, 79, 19, 81, 20, 120, 16, 23, 120, 67, 20, 68, 78, 69, 68, 126, 16, 82, 126, 86, 73, 21, 85, 73, 98, 38, 73, 114, 38, 73, 97, 39, 98, 126, 73, 33, 126, 115, 73, 33, 39, 123, 37, 73, 33, 126, 34, 33, 73, 127, 35, 73, 113, 39, 96, 37, 120, 73, 99, 35, 107, 22};

  char flag[74];

  for (int i = 0; i < 5; i++) {
    flag[i] = enc[i] ^ 0x23;
  }

  for (int i = 5; i < 25; i++) {
    flag[i] = enc[i] ^ 0x27;
  }

  for (int i = 25; i < 35; i++) {
    flag[i] = enc[i] ^ 0x21;
  }

  for (int i = 35; i < 74; i++) {
    flag[i] = enc[i] ^ 0x16;
  }

  printf("[!] You got a FLAG! %s\n", flag);
  return 0;
}
