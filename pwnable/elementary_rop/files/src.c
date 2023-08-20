#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <err.h>

void gadget() {
    asm("pop %rdi; ret");
}

int main() {
    char buf[0x20];
    printf("content: ");
    gets(buf);
    return 0;
}

__attribute__((constructor))
void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(60);
}
