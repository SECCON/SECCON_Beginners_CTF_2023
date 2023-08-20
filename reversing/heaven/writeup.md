# writeup - Heaven

## 解法1

配布されたバイナリを実行すると、以下のように任意のメッセージを暗号化する機能をもっていることがわかる。また、同じメッセージを複数回暗号化すると異なる出力が得られ、暗号化にメッセージ以外の何らかのパラメータが使用されていると推測できる。
```
$ ./heaven
------ menu ------
0: encrypt message
1: decrypt message
2: exit
> 0
message: hoge
encrypted message: f334810d93
```

同様に復号もできるかのように見えるが、実際には未実装のため使用できない。
```
$ ./heaven
------ menu ------
0: encrypt message
1: decrypt message
2: exit
> 1
TODO: implement decrypt_message()
```

Ghidraを使ってバイナリをデコンパイルすると、以下のmain関数が得られる。
```
undefined8 main(void)

{
  int iVar1;
  char *pcVar2;
  long lVar3;
  size_t sVar4;
  undefined local_11;
  char local_10 [8];
  
  getrandom(&local_11,1,0);
  while( true ) {
    while( true ) {
      puts("------ menu ------");
      puts("0: encrypt message");
      puts("1: decrypt message");
      puts("2: exit");
      printf(0x402045);
      pcVar2 = fgets(local_10,8,stdin);
      if (pcVar2 == (char *)0x0) {
        return 0;
      }
      lVar3 = strtol(local_10,(char **)0x0,10);
      iVar1 = (int)lVar3;
      if (iVar1 != 1) break;
      puts("TODO: implement decrypt_message()");
    }
    if (iVar1 == 2) break;
    if (iVar1 == 0) {
      printf(0x402048);
      fgets(message,0x100,stdin);
      sVar4 = strlen(message);
      if (sVar4 != 0) {
        encrypt_message(local_11,message,sVar4 - 1);
        printf(0x402052);
        print_hexdump(message,sVar4 - 1);
      }
    }
  }
  return 0;
}
```
関数の名前からencrypt_message関数が暗号化を行っていると推測でき、その引数には3つの値が与えられている。`local_11`はgetrandom関数を使って初期化されており、これは乱数である。また`message`は入力したメッセージ、`sVar4 - 1`はメッセージの長さである。その後、printf関数とprint_hexdump関数により何らかの出力を行っている。printf関数の引数に与えられている`0x402052`は文字列"encrypted message: %02x"へのポインタであり、`local_11`を16進数2桁で表示している。そしてprint_hexdump関数には`message`および`sVar4 - 1`が引数に与えられており、暗号化したメッセージを16進数で出力している。つまり、出力の形式は`<1byteの乱数> + <暗号化されたメッセージ>`になっている。

次にencrypt_message関数をデコンパイルする。
```
void encrypt_message(undefined param_1,undefined *param_2,long param_3)

{
  undefined *puVar1;
  byte bVar2;
  undefined *puVar3;
  
  puVar1 = param_2 + param_3;
  if (param_3 != 0) {
    do {
      puVar3 = param_2 + 1;
      bVar2 = calc_xor(*param_2,param_1);
      *param_2 = sbox[bVar2];
      param_2 = puVar3;
    } while (puVar1 != puVar3);
  }
  return;
}
```
コードを読むと、入力されたメッセージのi文字目に関して`sbox[calc_xor(param_2[i], param_1)]`を計算し、これを暗号文としていることがわかる。先述したとおり引数のparam_1には乱数が与えられており、これは鍵の役割を持っているようである。

さて、仮に関数名から推測してcalc_xor関数がXOR演算を行う関数であるならば、ある文字を暗号化した結果は鍵が同一のとき常に同じになるはずである。つまり、フラグの暗号化に使われた鍵と同じ鍵を用いて、ある文字を暗号化した結果を収集することで、暗号化されたフラグを復号できると考えられる。

#### フラグの暗号化に使われた鍵の特定

暗号化されたメッセージの形式は`<1byteの乱数> + <暗号化されたメッセージ>`であるから、与えられた暗号文`ca6ae6e83d63c90bed34a8be8a0bfd3ded34f25034ec508ae8ec0b7f`より暗号化に使われた鍵は`0xca`である。

#### 暗号化に使われる鍵の固定

つぎに、鍵を固定した状態で暗号化を行いたい。しかしバイナリではgetrandom関数から得られた乱数を鍵として使っているため、このままでは鍵が0xcaになるまで回す必要があり非効率である。そこで環境変数LD_PRELOADを使用してライブラリ関数getrandomを置換することで鍵の固定を実現する。そのために、次のようなC言語のプログラムを用意する。
```
// getrandom.c
#include <stdlib.h>

size_t getrandom(void *buf, size_t buflen, unsigned int flags) {
  *(char *)buf = 0xca;
}
```
そしてこれを共有ライブラリとして使用できるようにコンパイルする。
```
$ gcec -fPIC -shared -o getrandom.so getrandom.c
```
最後に、コンパイルした共有ライブラリを環境変数LD_PRELOADに指定してバイナリを実行する。すると常に鍵が0xcaの状態で暗号化が行われ、鍵を固定することができた。
```
$ LD_LIBRARY_PATH=. LD_PRELOAD=getrandom.so ./heaven
------ menu ------
0: encrypt message
1: decrypt message
2: exit
> 0
message: hoge
encrypted message: ca4c5d2fcb

$ LD_LIBRARY_PATH=. LD_PRELOAD=getrandom.so ./heaven
------ menu ------
0: encrypt message
1: decrypt message
2: exit
> 0
message: hoge
encrypted message: ca4c5d2fcb
```

#### 平文と暗号文の対応付け

鍵を固定して暗号化できるようになったので、以下のプログラムのように平文と暗号文の対応を収集する。
```
# solve.py
import string
from pwn import *

table = dict()
for c in string.printable:
  p = process('./heaven', env={'LD_LIBRARY_PATH': '.', 'LD_PRELOAD': 'getrandom.so'})
  p.sendline(b'0')
  p.sendline(c)
  p.recvuntil(b': ca')
  enc = p.recvline()[:-1].decode()
  table[enc] = c
  p.kill()
print(table)
```
このプログラムを実行すると以下のような辞書が得られる。
```
$ python3 solve.py
(...)
{'fd': '0', 'f2': '1', '76': '2', '8a': '3', '3d': '4', '50': '5', '58': '6', 'd0': '7', '42': '8', '7c': '9', '2b': 'a', '63': 'b', '6a': 'c', 'ed': 'd', 'cb': 'e', 'e8': 'f', '2f': 'g', '4c': 'h', '1f': 'i', '5e': 'j', '9d': 'k', '0b': 'l', 'e7': 'm', '05': 'n', '5d': 'o', 'a8': 'p', '57': 'q', 'be': 'r', '06': 's', 'e6': 't', 'ec': 'u', '59': 'v', 'bd': 'w', 'c1': 'x', 'dc': 'y', 'c4': 'z', 'cc': 'A', 'e2': 'B', '4f': 'C', 'c8': 'D', 'd4': 'E', '04': 'F', 'e4': 'G', 'f7': 'H', '29': 'I', '01': 'J', 'fc': 'K', 'b4': 'L', '75': 'M', 'ce': 'N', '9b': 'O', '60': 'P', 'dd': 'Q', '13': 'R', '2c': 'S', 'd5': 'T', '88': 'U', '47': 'V', '95': 'W', '81': 'X', 'e5': 'Y', 'c7': 'Z', 'ee': '!', 'e0': '"', '87': '#', 'ef': '$', '3f': '%', '6c': '&', '2d': "'", '4e': '(', '78': ')', 'b6': '*', 'ae': '+', '51': ',', 'fa': '-', 'd3': '.', 'b2': '/', '10': ':', '66': ';', '5c': '<', '48': '=', '21': '>', 'cf': '?', '49': '@', '67': '[', '92': '\\', 'f0': ']', '93': '^', '34': '_', '0d': '`', 'c9': '{', '5a': '|', '7f': '}', '9f': '~', 'd6': ' ', 'b1': '\t', '': '\n', '70': '\r', '26': '\x0b', 'f4': '\x0c'}
```
この辞書を用いてフラグを復元するプログラムを書く。
```
# solve.py (続き)
flag = ''
cipher = 'ca6ae6e83d63c90bed34a8be8a0bfd3ded34f25034ec508ae8ec0b7f'
for i in range(1, len(cipher)//2):
  flag += table[cipher[i*2:i*2+2]]
print(flag)
```
プログラムを実行するとフラグが得られる。
```
$ python3 solve.py
(...)
ctf4b{ld_pr3l04d_15_u53ful}
```

## 解法2

暗号化の処理で使用されているcalc_xor関数をディスアセンブルすると以下のようになる。
```
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined calc_xor()
             undefined         AL:1           <RETURN>
                             calc_xor                                        XREF[2]:     Entry Point(*), 
                                                                                          encrypt_message:004012d1(c)  
        0040133a 55              PUSH       RBP
        0040133b 48 89 e5        MOV        RBP,RSP
        0040133e 8d 24 25        LEA        ESP,[DAT_00404161]                               = 00401346h
        00401345 cb              RETF                                                        = 00401346h
        00401346 89 f8           MOV        EAX,EDI
        00401348 48 31 f0        XOR        RAX,RSI
        0040134b 8d 24 25        LEA        ESP,[DAT_00404169]                               = 00401353h
        00401352 cb              RETF                                                        = 00401353h
        00401353 48 89 ec        MOV        RSP,RBP
        00401356 5d              POP        RBP
        00401357 c3              RET
```
一見`XOR RAX,RSI`を実行しているだけのように見えるが、デバッガで処理を追うとそうではないことがわかる。XORの前後のコードによってCSレジスタが変更されるため、これは32bitの機械語として解釈される。つまり実際には`DEC RAX; XOR EAX, ESI`が実行されている。
以上の情報から暗号化アルゴリズムが推測できるため、以下のような復号処理を書くと暗号文からフラグが得られる。
```
sbox = [
    194, 83,  187, 128, 46,  95,  30,  181, 23,  17,  0,   158, 36,  197, 205,
    210, 126, 57,  198, 26,  65,  82,  169, 153, 3,   105, 139, 115, 111, 160,
    241, 216, 245, 67,  125, 14,  25,  148, 185, 54,  123, 48,  37,  24,  2,
    167, 219, 179, 144, 152, 116, 170, 163, 32,  234, 114, 162, 142, 20,  91,
    35,  150, 98,  164, 70,  34,  101, 122, 8,   246, 18,  172, 68,  233, 40,
    141, 254, 132, 195, 227, 251, 21,  145, 58,  143, 86,  235, 51,  109, 10,
    49,  39,  84,  249, 74,  243, 191, 75,  218, 104, 161, 60,  255, 56,  166,
    62,  183, 192, 154, 53,  202, 9,   184, 140, 222, 28,  12,  50,  42,  15,
    130, 173, 100, 69,  133, 209, 175, 217, 252, 180, 41,  1,   155, 96,  117,
    206, 79,  200, 204, 226, 228, 247, 212, 4,   103, 146, 229, 199, 52,  13,
    240, 147, 44,  213, 221, 19,  149, 129, 136, 71,  157, 11,  31,  94,  93,
    168, 231, 5,   106, 237, 43,  99,  47,  76,  203, 232, 201, 90,  220, 196,
    176, 225, 127, 159, 6,   230, 87,  190, 189, 193, 236, 89,  38,  244, 177,
    22,  134, 215, 112, 55,  77,  113, 119, 223, 186, 248, 59,  85,  156, 121,
    7,   131, 151, 214, 110, 97,  29,  27,  165, 64,  171, 188, 107, 137, 174,
    81,  120, 182, 178, 253, 250, 211, 135, 239, 238, 224, 45,  78,  63,  108,
    102, 92,  124, 16,  207, 73,  72,  33,  138, 61,  242, 118, 208, 66,  80,
    88]

def uint8_t(n: int) -> int:
  return (n + 0x100) & 0xff

def decrypt(key: str, cipher: bytes) -> str:
  message = ""
  for i in range(len(cipher)):
    message += chr((sbox.index(cipher[i]) ^ key) + 1)
  return message

flag = "ca6ae6e83d63c90bed34a8be8a0bfd3ded34f25034ec508ae8ec0b7f"
key = int(flag[:2], 16)
cipher = bytes.fromhex(flag[2:])
message = decrypt(key, cipher)
print(message)
```
