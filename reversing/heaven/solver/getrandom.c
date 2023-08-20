#include <stdlib.h>

size_t getrandom(void *buf, size_t buflen, unsigned int flags) {
  *(char *)buf = 0xca;
}
