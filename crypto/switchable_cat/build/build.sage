from Crypto.Util.number import *
from secret import seed, flag
from random import getrandbits


neko = 8*ord("🐈")*ord("🐈")*ord("🐈")
human = len(flag) * 8
bits = 128
M = MatrixSpace(GF(2), bits, bits)
vec1, vec2 = [], []
v1, v2 = [0] * (bits - 10), [0] * (bits - 10)
vec1 += v1 + [1, 0, 0, 1, 0, 1, 0, 1, 0, 1]
vec2 += v2 + [0, 1, 1, 0, 1, 0, 0, 0, 1, 0]
for i in range(bits - 1):
    v = [0] * bits
    v[i] = 1
    vec1 += v[:]
    vec2 += v[:]

A1, A2 = M(vec1), M(vec2)
A = (A1*A2)^(neko // 2)*A1
B = vector(list(map(int, list(bin(seed)[2:]))))
B = A * B

switch = 1
key = 0
for i in range(human):
    key <<= 1
    key += int(list(B)[-1])
    if switch == 0:
        B = A1 * B
    if switch == 1:
        B = A2 * B
    switch = 1 - switch

cipher = bytes_to_long(flag) ^^ key
print("seed =", seed)
# print("key =", key)
print("cipher =", cipher)
