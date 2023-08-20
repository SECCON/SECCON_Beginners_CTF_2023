from Crypto.Util.number import isPrime, bytes_to_long
from secret import flag
import secrets

meat = bytes_to_long(secrets.token_bytes(256))
assert meat.bit_length() <= 2048
salt = bytes_to_long(secrets.token_bytes(8))
pepper = 3

def bake(meat: int, g: int, p: int):
    baked = (pow((meat ^ salt) * g**pepper, meat + g*pepper, p) + g * (meat ^ salt)**pepper) % p
    return baked

print("Let's cook together!")
print("Give me a prime to cook.")
p = int(input("p = "))
if not (128 < p.bit_length() <= 2048):
    print("p should be 2^128 <= p < 2^2048.")
    exit()
if not isPrime(p):
    print("p should be prime!")
    exit()
print("This is meat:", pow(meat, pepper, p))
for _ in range(16):
    g = int(input("g = "))
    g %= p
    if not (128 < g.bit_length()):
        print("g should be 2^128 <= g.")
        continue
    print("Here you are. Enjoy!", bake(meat, g, p))
print("You must be full.")
challenge = int(input("Thank you. By the way, where do you think this meat comes from?"))
if meat == challenge:
    print("Nice!", flag)
