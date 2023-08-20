# Forbidden

## 題材とする脆弱性

Express における case insensitive routing

## 実現するためのテーマ

`/flag` にはアクセスできないが、`/Flag` や `/FLAG` だとアクセスできるようにする。

## 想定する参加者が解答までに至る思考経路

1. `/flag` へのアクセスはブロックされることに気づく。
2. 仕様を調べるか、あるいは適当に試行しているうちに大文字/小文字を入れ替えるとアクセスできることに気づく。

```sh
$ curl localhost/flag
:(

$ curl localhost/FLAG
ctf4b{403_forbidden_403_forbidden_403}
```

## 想定する難易度

Beginner

## 参考資料

https://expressjs.com/sk/api.html#:~:text=case%20sensitive%20routing
