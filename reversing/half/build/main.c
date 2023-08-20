#include <stdio.h>
#include <string.h>

/* ctf4b{ge4_t0_kn0w_the_bin4ry_fi1e_with_s4ring3} */

int main() {
  char str[100];
  printf("Enter the FLAG: ");
  scanf("%99s%*[^\n]", str);

  if (strlen(str) != 47) {
    printf("Invalid FLAG\n");
    return 1;
  }

  if (strncmp(str, "ctf4b{ge4_t0_kn0w_the", 21) == 0 &&
      strcmp(str + strlen(str) - 26, "_bin4ry_fi1e_with_s4ring3}") == 0) {
    printf("Correct!\n");
  } else {
    printf("Invalid FLAG\n");
    return 1;
  }
  return 0;
}
