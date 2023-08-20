# coding: utf-8
import random
import os

flag = b"ctf4b{xxx___censored___xxx}"

# Please remove here if you wanna test this code in your environment :)
flag = os.getenv("FLAG").encode()

cipher = []

for i in range(len(flag)-1):
    c = ((flag[i] + flag[i+1]) ** 2 + i)
    cipher.append(c)

random.shuffle(cipher)

print(f"cipher = {cipher}")
