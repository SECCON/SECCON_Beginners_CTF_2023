import string
from pwn import *

table = dict()
for c in string.printable:
  p = process('./heaven', env={'LD_LIBRARY_PATH': '.', 'LD_PRELOAD': 'getrandom.so'})
  p.sendline(b'0')
  p.sendline(c)
  p.recvuntil(b': ca')
  enc = p.recvline()[:-1].decode()
  table[enc] = c
  p.kill()
print(table)

flag = ''
cipher = 'ca6ae6e83d63c90bed34a8be8a0bfd3ded34f25034ec508ae8ec0b7f'
for i in range(1, len(cipher)//2):
  flag += table[cipher[i*2:i*2+2]]
print(flag)
