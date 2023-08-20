import os
import requests

def solve(url):
    res = requests.get(url)
    return res.text

if __name__ == "__main__":
    flag = solve("https://{}:{}/FLAG".format(os.getenv("CTF4B_HOST"), os.getenv("CTF4B_PORT")))
    print(flag)
