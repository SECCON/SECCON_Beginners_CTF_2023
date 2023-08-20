from Crypto.Util.number import *
from pwn import *
import sys

if len(sys.argv) == 3:
    io = remote(sys.argv[1], int(sys.argv[2]))

p = 2^1024 - 2^32
while True:
    p = next_prime(p)
    PR.<x> = PolynomialRing(GF(p))
    f = (x + 1)^3 - x^3
    gs = f.roots()
    gs = list(map(lambda x: x[0], gs))
    if len(gs) != 2:
        continue
    break
print("p", p)

io.sendline(str(p).encode())
io.recvuntil(b'This is meat: ')
m3 = int(io.recvline())
print(m3)

print(gs[0])
rs = []
for i in range(2):
    io.sendline(str(gs[i]).encode())
    io.recvuntil(b'Enjoy!')
    g0 = int(io.recvline())
    io.sendline(str(gs[i] + 1).encode())
    io.recvuntil(b'Enjoy!')
    g1 = int(io.recvline())
    rs.append((g0, g1))
print(rs)

PR.<x> = PolynomialRing(GF(p))
f1 = (rs[0][1] - (gs[0]+1)*x^3) - (rs[0][0] - gs[0]*x^3)*(x*gs[0]^3)^3
f2 = (rs[1][1] - (gs[1]+1)*x^3) - (rs[1][0] - gs[1]*x^3)*(x*gs[1]^3)^3
f1 = f1.monic()
f2 = f2.monic()
f = gcd(f1, f2)
c = - f[0]
print(f)

def franklinReiter(n, e, r, c1, c2):
    R.<x> = PolynomialRing(Zmod(n))
    f1 = x^e - c1
    f2 = (x + r)^e - c2
    return - polygcd(f1, f2).coefficients()[0]

def polygcd(a, b):
    if(b == 0):
        return a.monic()
    else:
        return polygcd(b, a % b)

def CoppersmithShortPadAttack(e, n, C1, C2, eps=1/30):
    P.<x,y> = PolynomialRing(ZZ)
    g1 = x^e - C1
    g2 = (x + y)^e - C2
    print(g1)
    res = g1.resultant(g2)

    Py.<y> = PolynomialRing(Zmod(n))
    res = res.univariate_polynomial()
    res = res.change_ring(Py).subs(y=y)
    res = res.monic()
    kbits = n.nbits()//(2*e*e)
    print(kbits)
    diff = res.small_roots(X=2^kbits, epsilon=eps)
    print(diff)

    return franklinReiter(n, e, diff[0], C1, C2)

print(m3)
print(p)
print(c)
k = CoppersmithShortPadAttack(3, p, m3, lift(c))
print(k)
