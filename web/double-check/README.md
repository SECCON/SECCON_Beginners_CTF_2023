# double check
## 題材とする脆弱性

- RS256 の公開鍵を HS256 の共通鍵として使用する攻撃 
- Prototype pollution

## 実現するためのテーマ

jwtが改ざんでき、paylodを介してオブジェクトのprototypeを汚染できる。

## 想定する参加者が解答までに至る思考経路

1. flagを取得するためにjwtが送信されることがわかる。
2. jwtの検証アルゴリズムにHS256を使用させることで、公開鍵を用いた改ざんが可能であることがわかる。
3. セッションに保存されたユーザー情報とjwtのpayloadを見て、両方の`admin`パラメータがtrueであればflagが得られる。
4. jwtのpayloadは改ざん可能なので、`admin`パラメータをtrueにできる。
5. jwtのpayloadを介してセッションに保存されたユーザー情報を変更できるが、`admin`パラメータは直接書き換えできない。
6. `__proto__`を介して`admin`パラメータを書き換えできることがわかる。

## 想定する難易度

Medium

## 参考資料

- https://scgajge12.hatenablog.com/entry/jwt_security
- https://www.fastify.io/docs/latest/Guides/Prototype-Poisoning/