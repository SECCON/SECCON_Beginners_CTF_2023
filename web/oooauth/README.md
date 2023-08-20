# oooauth
## 題材とする脆弱性

- リダイレクト先URLの不適切な検証
- HTMLインジェクション

## 実現するためのテーマ

guest用に発行された認可コードをadminに使用させ、HTMLインジェクションを介してadminの認可コードを含むURLを窃取する。

## 想定する参加者が解答までに至る思考経路

1. リダイレクト先のURLである`redirect_uri`の検証処理が不適切であり、クエリパラメータの部分を自由に操作することができる。
2. report機能を使用すると、adminが認証情報を入力し、OAuthを用いてアクセストークンを発行する。
3. 認可サーバ側で`body-parser`の`urlencoded()`メソッドの`extended`オプションが`true`になっていることがわかる。
4. `redirect_uri`にクエリパラメータとして認可コードが追加され、認可コードとして配列が渡される場合は一番最後の要素が使用される。
5. 認可コードは一回のみ使用できるが、ここでadmin用に発行された認可コードではなく、guest用に発行された認可コードを使用させるようにする。
6. OAuthクライアントにHTMLインジェクションの脆弱性があり、RefererリクエストヘッダとしてフルのURLが送信される。
7. adminの認可コードを窃取し、使用することでadminのアクセストークンを発行する。

## 想定する難易度

Hard

## 参考資料
- https://www.rfc-editor.org/rfc/rfc6749
- https://github.com/expressjs/body-parser#extended
- https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Referrer-Policy