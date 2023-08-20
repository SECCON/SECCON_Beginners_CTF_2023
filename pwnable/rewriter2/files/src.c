#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_SIZE 0x20
#define READ_SIZE 0x100

void __show_stack(void *stack);

int main() {
  char buf[BUF_SIZE];
  __show_stack(buf);

  printf("What's your name? ");
  read(0, buf, READ_SIZE);
  printf("Hello, %s\n", buf);

  __show_stack(buf);

  printf("How old are you? ");
  read(0, buf, READ_SIZE);
  puts("Thank you!");

  __show_stack(buf);
  return 0;
}

void win() {
  puts("Congratulations!");
  system("/bin/sh");
}

void __show_stack(void *stack) {
  unsigned long *ptr = stack;
  printf("\n %-19s| %-19s\n", "[Addr]", "[Value]");
  puts("====================+===================");
  for (int i = 0; i < 10; i++) {
    if (&ptr[i] == stack + BUF_SIZE + 0x8) {
      printf(" 0x%016lx | xxxxx hidden xxxxx  <- canary\n",
             (unsigned long)&ptr[i]);
      continue;
    }

    printf(" 0x%016lx | 0x%016lx ", (unsigned long)&ptr[i], ptr[i]);
    if (&ptr[i] == stack)
      printf(" <- buf");
    if (&ptr[i] == stack + BUF_SIZE + 0x10)
      printf(" <- saved rbp");
    if (&ptr[i] == stack + BUF_SIZE + 0x18)
      printf(" <- saved ret addr");
    puts("");
  }
  puts("");
}

__attribute__((constructor)) void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);
}
