# drmsaw

## 題材とする脆弱性

Localで実行されるDRM

## 実現するためのテーマ

サーバとHTTP Live Streamingで動画を暗号化した上で配信するサービスにおいて、wasm上で復号してユーザへ提供する。動画のダウンロードができたらフラグが手に入る。

## 想定する参加者が解答までに至る思考経路

1. 動画をダウンロードできればフラグが取れることがわかる
2. 動画はhlsで分割し、暗号化された状態で送信される
3. 暗号化の鍵はenc.keyやm3u8ファイルに記載されていない
4. wasmの中で鍵が動的に変更されていると予想される
5. `context = window.gContext`を見て、contextに鍵が入っていると考えられる
6. ブラウザでHTMLをダンロードする際にcontextを表示するスクリプトを挿入し、鍵を手にいれる
7. 鍵を元に、ffmpegを使用して動画を復元する

## 想定する難易度

Medium

## 参考資料

* https://github.com/video-dev/hls.js/issues/5044
* https://note.com/tsubasa_nanoda/n/na6b855683a59
* https://github.com/video-dev/hls.js/