# Three

「中身をちょっと見ただけではフラグは分からないみたい！」とは言われているものの、まずは表層解析を行います。

```bash
$ file three
three: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV),
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=5f0a7f4053ff33a4a013bbe5c58ea4dc2973ed54,
for GNU/Linux 3.2.0, not stripped
```

ELFファイルであると分かります。次に`strings`コマンドで可読文字列を取得します。

```bash
$ strings three
/lib64/ld-linux-x86-64.so.2
libc.so.6
__isoc99_scanf
puts
printf
strlen
...
u+UH
VUUUH
VUUUH
VUUUH
VUUUH
VUUUH
[]A\A]A^A_
Invalid FLAG
Correct!
Enter the FLAG:
%49s
:*3$"
```

フラグにつながるような文字列は見当たりません。ここでELFファイルに含まれる機械語の命令を逆アセンブル・逆コンパイルする専門のツールとしてGhidraを使用し解析をします。

> Ghidraの使い方については[Reversing基礎編 / Basics of Reversing - SECCON Beginners Live 2022](https://speakerdeck.com/hi120ki/basics-of-reversing-seccon-beginners-live-2022)を参考にしてください。

Ghidraで`three`を開き、`main`関数を見てみます。

```cpp
void main(void)

{
  undefined local_48 [64];

  printf("Enter the FLAG: ");
  __isoc99_scanf(&DAT_00102127,local_48);
  validate_flag(local_48);
  return;
}
```

入力された文字列を`local_48`に格納し、`validate_flag`関数に渡しています。`validate_flag`関数を見てみます。

```cpp
undefined8 validate_flag(char *param_1)

{
  char cVar1;
  size_t sVar2;
  undefined8 uVar3;
  int local_c;

  sVar2 = strlen(param_1);
  if (sVar2 == 0x31) {
    for (local_c = 0; local_c < 0x31; local_c = local_c + 1) {
      if (local_c % 3 == 0) {
        cVar1 = (char)*(undefined4 *)(flag_0 + (long)(local_c / 3) * 4);
      }
      else if (local_c % 3 == 1) {
        cVar1 = (char)*(undefined4 *)(flag_1 + (long)(local_c / 3) * 4);
      }
      else {
        cVar1 = (char)*(undefined4 *)(flag_2 + (long)(local_c / 3) * 4);
      }
      if (cVar1 != param_1[local_c]) {
        puts("Invalid FLAG");
        return 1;
      }
    }
    puts("Correct!");
    uVar3 = 0;
  }
  else {
    puts("Invalid FLAG");
    uVar3 = 1;
  }
  return uVar3;
}
```

これを変数名を変更することで読みやすくすると

```cpp
undefined8 validate_flag(char *input_text)

{
  char c;
  size_t sVar2;
  undefined8 ret;
  int i;

  input_text_length = strlen(input_text);
  if (input_text_length == 0x31) {
    for (i = 0; i < 0x31; i = i + 1) {
      if (i % 3 == 0) {
        c = (char)*(undefined4 *)(flag_0 + (long)(i / 3) * 4);
      }
      else if (i % 3 == 1) {
        c = (char)*(undefined4 *)(flag_1 + (long)(i / 3) * 4);
      }
      else {
        c = (char)*(undefined4 *)(flag_2 + (long)(i / 3) * 4);
      }
      if (c != input_text[i]) {
        puts("Invalid FLAG");
        return 1;
      }
    }
    puts("Correct!");
    ret = 0;
  }
  else {
    puts("Invalid FLAG");
    ret = 1;
  }
  return ret;
}
```

入力された文字列の長さが`0x31`であることを確認し、文字のインデックスを3で割った余りで`flag_0`、`flag_1`、`flag_2`という配列に格納された文字列と比較しています。

Ghidraでその文字列を確認すると

```python
flag_0 = [0x63, 0x34, 0x63, 0x5F, 0x75, 0x62, 0x5F, 0x5F, 0x64, 0x74, 0x5F, 0x72, 0x5F, 0x31, 0x5F, 0x34, 0x7D]
flag_1 = [0x74, 0x62, 0x34, 0x79, 0x5F, 0x31, 0x74, 0x75, 0x30, 0x34, 0x74, 0x65, 0x73, 0x69, 0x66, 0x67]
flag_2 = [0x66, 0x7B, 0x6E, 0x30, 0x61, 0x65, 0x30, 0x6E, 0x5F, 0x65, 0x34, 0x65, 0x70, 0x74, 0x31, 0x33]
```

となります。これを復元するPythonのコードを記述すると

```python
flag_0 = [0x63, 0x34, 0x63, 0x5F, 0x75, 0x62, 0x5F, 0x5F, 0x64, 0x74, 0x5F, 0x72, 0x5F, 0x31, 0x5F, 0x34, 0x7D]
flag_1 = [0x74, 0x62, 0x34, 0x79, 0x5F, 0x31, 0x74, 0x75, 0x30, 0x34, 0x74, 0x65, 0x73, 0x69, 0x66, 0x67]
flag_2 = [0x66, 0x7B, 0x6E, 0x30, 0x61, 0x65, 0x30, 0x6E, 0x5F, 0x65, 0x34, 0x65, 0x70, 0x74, 0x31, 0x33]

flag = ""
for i in range(0x31):
    if i % 3 == 0:
        flag += chr(flag_0[i // 3])
    elif i % 3 == 1:
        flag += chr(flag_1[i // 3])
    elif i % 3 == 2:
        flag += chr(flag_2[i // 3])
print(flag)
```

となりフラグは`ctf4b{c4n_y0u_ab1e_t0_und0_t4e_t4ree_sp1it_f14g3}`となります。

```bash
$ ./three
Enter the FLAG: ctf4b{c4n_y0u_ab1e_t0_und0_t4e_t4ree_sp1it_f14g3}
Correct!
```
