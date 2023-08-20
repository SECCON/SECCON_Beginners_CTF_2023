# Half

「どうやって中身を見るんだろう...？」ということで、バイナリ解析の基本的な解析手法である表層解析を行う問題です。

まずは`file`コマンドでファイルの種類を確認します。

```sh
$ file half
half: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV),
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=e2b1484a1db68e68d01130084882316fb34d86ad,
for GNU/Linux 3.2.0, not stripped
```

すると、ELFファイルであることがわかります。ELFファイルは、Linuxで実行可能なバイナリファイルのフォーマットです。

このファイルを実行してみます。

```sh
$ chmod +x half
$ ./half
Enter the FLAG: ctf4b{flag}
Invalid FLAG
```

フラグの入力を促されるので、`ctf4b{flag}`と入力してみますが、`Invalid FLAG`と表示されてしまいます。

ということでこの問題の趣旨は、このバイナリファイルがどのような動作をしているのかを調べ、正しいと判定されるフラグの文字列を取得することです。

しかし、バイナリファイルは機械語の命令からなるため、そのままでは中身を見ることができません。しかし、固定の文字列等はバイナリファイルの中にそのまま埋め込まれていることがあります。そこで、`strings`コマンドを用いて、バイナリファイルの中に存在する可読文字列を取得してみます。

```sh
$ strings half
```

```
/lib64/ld-linux-x86-64.so.2
libc.so.6
strncmp
__isoc99_scanf
puts
printf
strlen
...
Enter the FLAG:
...
Invalid FLAG
ctf4b{ge4_t0_kn0w_the
_bin4ry_fi1e_with_s4ring3}
...
```

すると、このELFファイルに動的リンクされているライブラリや関数名に加えて、`ctf4b{ge4_t0_kn0w_the_bin4ry_fi1e_with_s4ring3}`というフラグが表示されました。

このフラグを入力してみると、正解となります。

```
$ ./half
Enter the FLAG: ctf4b{ge4_t0_kn0w_the_bin4ry_fi1e_with_s4ring3}
Correct!
```

> このバイナリファイルは入力された文字列と`ctf4b{ge4_t0_kn0w_the`及び`_bin4ry_fi1e_with_s4ring3}`とを比較し、一致した場合に正解と判定しています。
