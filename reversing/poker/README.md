# Poker

## 問題文

みんなでポーカーで遊ぼう！点数をたくさん獲得するとフラグがもらえるみたい！

でもこのバイナリファイル、よく見たら...？

## 難易度

**Medium**

## 作問にあたって

stripされたバイナリの動的解析

## 解法

```cpp
void FUN_001010b0(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 unaff_retaddr;
  undefined auStack_8 [8];

  __libc_start_main(main,unaff_retaddr,&stack0x00000008,FUN_001022e0,FUN_00102350,param_3,auStack_8)
  ;
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

```cpp
void welcome_message(void)

{
  puts("");
  puts(&DAT_00103240);
  puts(&DAT_00103320);
  puts(&DAT_00103418);
  puts(&DAT_00103508);
  puts(&DAT_001035f8);
  puts(&DAT_001036e0);
  return;
}
```

```cpp
void show_score(uint param_1)

{
  puts("\n================");
  printf("| Score : %3d  |\n",(ulong)param_1);
  puts("================\n");
  return;
}
```

```cpp
undefined4 read_choice(void)

{
  int local_c;

  do {
    printf("[?] Enter 1 or 2: ");
    __isoc99_scanf(&DAT_0010323c,&local_c);
    if (local_c == 1) {
      return 1;
    }
  } while (local_c != 2);
  return 2;
}
```

```cpp
int play_poker(int param_1,int param_2)

{
  undefined8 uVar1;
  int iVar2;
  time_t tVar3;
  int local_1dc;
  uint uStack_1c4;
  uint uStack_1bc;
  undefined8 local_1b8;
  undefined8 local_1b0;
  int local_18;
  int local_14;
  int local_10;
  int local_c;

  local_14 = 0;
  for (local_c = 0; local_c < 4; local_c = local_c + 1) {
    for (local_10 = 1; local_10 < 0xe; local_10 = local_10 + 1) {
      *(int *)(&local_1b8 + local_14) = local_c;
      *(int *)((long)&local_1b8 + (long)local_14 * 8 + 4) = local_10;
      local_14 = local_14 + 1;
    }
  }
  tVar3 = time((time_t *)0x0);
  srand((uint)tVar3);
  for (local_c = 0; local_c < 0x34; local_c = local_c + 1) {
    iVar2 = rand();
    local_18 = iVar2 % 0x34;
    uVar1 = (&local_1b8)[local_c];
    (&local_1b8)[local_c] = (&local_1b8)[iVar2 % 0x34];
    (&local_1b8)[local_18] = uVar1;
  }
  uStack_1bc = (uint)((ulong)local_1b8 >> 0x20);
  uStack_1c4 = (uint)((ulong)local_1b0 >> 0x20);
  if (uStack_1c4 < uStack_1bc) {
    if (param_2 == 1) {
      puts("[+] Player 1 wins! You got score!");
      local_1dc = param_1 + 1;
    }
    else {
      puts("[-] Player 1 wins! Your score is reseted...");
      local_1dc = 0;
    }
  }
  else if (uStack_1bc < uStack_1c4) {
    if (param_2 == 2) {
      puts("[+] Player 2 wins! You got score!");
      local_1dc = param_1 + 1;
    }
    else {
      puts("[-] Player 2 wins! Your score is reseted...");
      local_1dc = 0;
    }
  }
  else {
    puts("[+] It\'s a tie! Your score is reseted...");
    local_1dc = 0;
  }
  return local_1dc;
}
```

```cpp
undefined8 main(void)

{
  undefined4 choice;
  int i;
  int score;

  score = 0;
  FUN_001021c3();
  i = 0;
  while( true ) {
    if (98 < i) {
      return 0;
    }
    show_score(score);
    choice = read_choice();
    score = play_poker(score,choice);
    if (99 < score) break;
    i = i + 1;
  }
  show_flag();
  return 0;
}
```

```
$ chmod +x poker
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

# main関数からの30命令を逆アセンブルしてshow_flag関数を見つける
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
   0x5555555562b7:	call   0x5555555551a0 <- show_flag関数

# エントリーポイントで停止している状態から直接show_flag関数に遷移する
gef> jump *0x5555555562b7
Continuing at 0x5555555562b7.
[!] You got a FLAG! ctf4b{4ll_w3_h4v3_70_d3cide_1s_wh4t_t0_d0_w1th_7he_71m3_7h47_i5_g1v3n_u5}
```
