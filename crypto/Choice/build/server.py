from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
from secret import p, q, r, flag


def main():
    n = p * q * r
    e = 65537
    m = bytes_to_long(flag)
    c = pow(m, e, n)
    s = p * q + q * r + r * p
    print("n =", n)
    print("e =", e)
    print("c =", c)
    print("s =", s)
    while True:
        a = int(input("input a(a>n) : "))
        if a < n:
            print("Reject")
            exit()
        result_a = (pow(p, a, n) + pow(q, a, n) + pow(r, a, n)) % n

        print("OK!!!!")
        print("result_a :", result_a)


if __name__ == "__main__":
    main()
