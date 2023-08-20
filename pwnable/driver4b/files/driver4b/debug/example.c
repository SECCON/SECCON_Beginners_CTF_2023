#include "../src/ctf4b.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

void fatal(const char *msg) {
  perror(msg);
  exit(1);
}

int main() {
  char *buf;
  int fd;

  fd = open("/dev/ctf4b", O_RDWR);
  if (fd == -1)
    fatal("/dev/ctf4b");

  buf = (char*)malloc(CTF4B_MSG_SIZE);
  if (!buf) {
    close(fd);
    fatal("malloc");
  }

  /* Get message */
  memset(buf, 0, CTF4B_MSG_SIZE);
  ioctl(fd, CTF4B_IOCTL_LOAD, buf);
  printf("Message from ctf4b: %s\n", buf);

  /* Update message */
  strcpy(buf, "Enjoy it!");
  ioctl(fd, CTF4B_IOCTL_STORE, buf);

  /* Get message again */
  memset(buf, 0, CTF4B_MSG_SIZE);
  ioctl(fd, CTF4B_IOCTL_LOAD, buf);
  printf("Message from ctf4b: %s\n", buf);

  free(buf);
  close(fd);
  return 0;
}
