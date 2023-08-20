#include <stdio.h>
#include <unistd.h>

char *flag = "ctf4b{***CENSORED***}";
char *poem[] = {
    "In the depths of silence, the universe speaks.",
    "Raindrops dance on windows, nature's lullaby.",
    "Time weaves stories with the threads of existence.",
    "Hearts entwined, two souls become one symphony.",
    "A single candle's glow can conquer the darkest room.",
};

int main() {
  int n;
  printf("Number[0-4]: ");
  scanf("%d", &n);
  if (n < 5) {
    printf("%s\n", poem[n]);
  }
  return 0;
}

__attribute__((constructor)) void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);
}
