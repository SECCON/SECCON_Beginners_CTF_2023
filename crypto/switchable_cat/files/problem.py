from Crypto.Util.number import *
from secret import seed, flag
from random import getrandbits
from os import urandom


class LFSR:
    def __init__(self):
        self.bits = 128
        self.rr = seed
        self.switch = 0
    def next(self):
        r = self.rr
        if self.switch == 0:
            b = ((r >> 0) & 1) ^ \
                ((r >> 2) & 1) ^ \
                ((r >> 4) & 1) ^ \
                ((r >> 6) & 1) ^ \
                ((r >> 9) & 1)
        if self.switch == 1:
            b = ((r >> 1) & 1) ^ \
                ((r >> 5) & 1) ^ \
                ((r >> 7) & 1) ^ \
                ((r >> 8) & 1)
        r = (r >> 1) + (b << (self.bits - 1))
        self.rr = r
        self.switch = 1 - self.switch
        return r & 1
    
    def gen_randbits(self, bits):
        key = 0
        for i in range(bits):
            key <<= 1
            key += self.next()
        return key


lfsr = LFSR()

neko = urandom(ord("🐈")*ord("🐈")*ord("🐈"))
key = lfsr.gen_randbits(len(neko) * 8)
cipher = bytes_to_long(neko) ^ key

#   📄🐈💨💨💨💨
# ╭─^────────╮
# │  cipher  │
# ╰──────────╯

key = lfsr.gen_randbits(len(flag) * 8)
cipher = bytes_to_long(flag) ^ key

print("seed =", seed)
print("cipher =", cipher)
