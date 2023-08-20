# phisher2

## 題材とする脆弱性

Webページ上でユーザを騙す文字列が表示される攻撃

## 実現するためのテーマ

Webページを開いたときに見た文字列と、実際にWebページに含まれる文字列が異なる。

## 想定する参加者が解答までに至る思考経路

1. テキストを送信すると内容をHTMLとして保存し、adminが閲覧することがわかる。
2. adminは目視で見た文字列が`https://phisher2.beginners.seccon.games/`から始まれば安全なドメインと判断する。
3. 2022出題のphisherとは違い、ホモグラフ攻撃を行なっても上手くOCRしてくれない。
4. コメントアウトや、表示方向の制御文字を使用すればadminを騙せることが考えられる。

## 想定する難易度

Medium

## 参考資料

* https://owasp-skf.gitbook.io/asvs-write-ups/right-to-left-override-rtlo/rtlo
* https://zenn.dev/nobokko/articles/idea_unicode_bidi_strange-look
