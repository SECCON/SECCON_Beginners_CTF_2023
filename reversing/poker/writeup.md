# Poker

バイナリを実行するとインディアンポーカーで遊べるようです。

```bash
$ chmod +x poker
$ ./poker

...
================
| Score :   0  |
================

[?] Enter 1 or 2: 1
[+] Player 1 wins! You got score!

================
| Score :   1  |
================

[?] Enter 1 or 2: 2
[+] Player 2 wins! You got score!

================
| Score :   2  |
================

[?] Enter 1 or 2: 1
[-] Player 2 wins! Your score is reseted...

================
| Score :   0  |
================
```

プレイヤー1と2のどっちが勝つかを予想して、勝てばスコアが加算されます。しかし、予想が外れるとスコアがリセットされてしまいます。これを踏まえた上で解析を始めます。

まずは表層解析です。

```bash
$ file poker
poker: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV),
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=7d0fc5db7a8f299ccf155729cc1183f5f6cb1bb4,
for GNU/Linux 3.2.0, stripped
```

ここで`poker`はstrippedされたELFファイルであることが分かります。`stripped`とはシンボル情報が削除されていることを示しており、`main`や`printf`といった関数名が分からなくなっています。

その上で、Ghidraによる静的解析でバイナリの大まかな動作を把握しつつ、解析することが求められます。まずはGhidraで`poker`を開き、`__libc_start_main`関数を呼び出している関数がないか見てみます。すると

```cpp
void FUN_001010b0(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 unaff_retaddr;
  undefined auStack_8 [8];

  __libc_start_main(FUN_00102262,unaff_retaddr,&stack0x00000008,FUN_001022e0,FUN_00102350,param_3,
                    auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

strippedなELFファイルであるため関数名がGhidraによって補完され`FUN_001010b0`となっていますが、`__libc_start_main`関数を呼び出している関数を見つけることができました。

`__libc_start_main`関数は、`main`関数を呼び出す関数で、第1引数には`main`関数のアドレスが渡されています。つまり関数`FUN_00102262`が`main`関数であると分かります。

```cpp
undefined8 FUN_00102262(void)

{
  undefined4 uVar1;
  int local_10;
  int local_c;

  local_c = 0;
  FUN_001021c3();
  local_10 = 0;
  while( true ) {
    if (0x62 < local_10) {
      return 0;
    }
    FUN_00102222(local_c); // スコア表示
    uVar1 = FUN_00102179(); // 1 or 2を入力させる
    local_c = FUN_00101fb7(local_c,uVar1); // 勝敗を判定する
    if (99 < local_c) break;
    local_10 = local_10 + 1;
  }
  FUN_001011a0();
  return 0;
}
```

`main`関数の動作を見るとスコア表示の関数`FUN_00102222`、1 or 2を入力させる関数`FUN_00102179`、勝敗を判定する関数`FUN_00101fb7`があり、それらがwhileループによって繰り返し実行されていることが分かります。

そしてスコアが格納される変数`local_c`が99以上になったときに呼び出される関数`FUN_001011a0`があります。この関数を見てみると長大ではありますが

```cpp
printf("[!] You got a FLAG! %s\n",local_60);
```

という処理があることからフラグを表示する関数だと推察できます。

何度も挑戦して100回勝てばいいかと思いますが、`main`関数の処理に`local_10`が0x62つまり98より大きい場合終了するようになっているため、100回勝つことはできません。

そこでGDBを用いてスコア表示の関数や勝敗を判定する関数の実行を飛ばして、直接フラグを表示する関数`FUN_001011a0`を実行させます。

```
$ gdb-gef poker

# エントリーポイントまで実行して停止
gef> start

# エントリーポイントからの15命令を逆アセンブルしてmain関数を見つける
gef> x/15i 0x5555555550b0
=> 0x5555555550b0:	endbr64
   0x5555555550b4:	xor    ebp,ebp
   0x5555555550b6:	mov    r9,rdx
   0x5555555550b9:	pop    rsi
   0x5555555550ba:	mov    rdx,rsp
   0x5555555550bd:	and    rsp,0xfffffffffffffff0
   0x5555555550c1:	push   rax
   0x5555555550c2:	push   rsp
   0x5555555550c3:	lea    r8,[rip+0x1286]        # 0x555555556350
   0x5555555550ca:	lea    rcx,[rip+0x120f]        # 0x5555555562e0
   0x5555555550d1:	lea    rdi,[rip+0x118a]        # 0x555555556262 <- main関数
   0x5555555550d8:	call   QWORD PTR [rip+0x3f02]        # 0x555555558fe0 <- __libc_start_main関数
   0x5555555550de:	hlt
   0x5555555550df:	nop
   0x5555555550e0:	lea    rdi,[rip+0x3f29]        # 0x555555559010

# main関数からの30命令を逆アセンブルしてフラグ表示関数を見つける
gef> x/30i 0x555555556262
   0x555555556262:	endbr64
   0x555555556266:	push   rbp
   0x555555556267:	mov    rbp,rsp
   0x55555555626a:	sub    rsp,0x10
   0x55555555626e:	mov    DWORD PTR [rbp-0x4],0x0
   0x555555556275:	mov    eax,0x0
   0x55555555627a:	call   0x5555555561c3
   0x55555555627f:	mov    DWORD PTR [rbp-0x8],0x0
   0x555555556286:	jmp    0x5555555562c7
   0x555555556288:	mov    eax,DWORD PTR [rbp-0x4]
   0x55555555628b:	mov    edi,eax
   0x55555555628d:	call   0x555555556222
   0x555555556292:	mov    eax,0x0
   0x555555556297:	call   0x555555556179
   0x55555555629c:	mov    DWORD PTR [rbp-0xc],eax
   0x55555555629f:	mov    edx,DWORD PTR [rbp-0xc]
   0x5555555562a2:	mov    eax,DWORD PTR [rbp-0x4]
   0x5555555562a5:	mov    esi,edx
   0x5555555562a7:	mov    edi,eax
   0x5555555562a9:	call   0x555555555fb7
   0x5555555562ae:	mov    DWORD PTR [rbp-0x4],eax
   0x5555555562b1:	cmp    DWORD PTR [rbp-0x4],0x63
   0x5555555562b5:	jle    0x5555555562c3
   0x5555555562b7:	call   0x5555555551a0 <- フラグ表示関数

# エントリーポイントで停止している状態から直接フラグ表示関数に遷移する
gef> jump *0x5555555562b7
Continuing at 0x5555555562b7.
[!] You got a FLAG! ctf4b{4ll_w3_h4v3_70_d3cide_1s_wh4t_t0_d0_w1th_7he_71m3_7h47_i5_g1v3n_u5}
```

フラグが表示されました。jumpによって直接関数を実行させるだけでなく、breakによるブレークポイントの設定とsetによるレジスタの書き換えによって解くことも可能です。挑戦してみてください。
