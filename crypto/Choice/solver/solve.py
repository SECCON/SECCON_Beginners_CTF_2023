from typing import Tuple, Iterator, Iterable, Optional
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, getPrime
import sys

sys.setrecursionlimit(10000)
from number import n, s1, s2, s3, s4, c, s, e


def extGCD(a: int, b: int) -> Tuple[int, int, int]:
    if b != 0:
        d, y, x = extGCD(b, a % b)
        y -= (a // b) * x
        return d, x, y
    return a, 1, 0


def gcd(a: int, b: int) -> int:
    while b != 0:
        t = a % b
        a, b = b, t
    return a


def modinv(a: int, m: int) -> int:
    if gcd(a, m) != 1:
        return 0
    if a < 0:
        a %= m
    return extGCD(a, m)[1] % m


def main():
    while True:
        k = n
        # s1 = (pow(p, k+3, n) + pow(q, k+3, n) + pow(r, k+3, n)) % n
        # s2 = (pow(p, k+2, n) + pow(q, k +2, n) + pow(r, k +2, n)) % n
        # s3 = (pow(p, k+1, n) + pow(q, k +1, n) + pow(r, k+1, n)) % n
        # s4 = (pow(p, k, n) + pow(q, k, n) + pow(r, k, n)) % n
        X = (s1 + s * s3 - n * s4) % n
        Y = (modinv(s2, n) * X) % n
        phi = (n + Y - s - 1) % n
        d = modinv(e, phi)
        m = pow(c, d, n)
        print(long_to_bytes(m))
        break


if __name__ == "__main__":
    main()
