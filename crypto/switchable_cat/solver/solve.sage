from Crypto.Util.number import *
from random import getrandbits


seed = 219857298424504813337494024829602082766
cipher = int(38366804914662571886103192955255674055487701488717997084670307464411166461113108822142059)

neko = 8*ord("🐈")*ord("🐈")*ord("🐈")
human = cipher.bit_length()+1
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

flag = cipher ^^ key
print(long_to_bytes(flag))

