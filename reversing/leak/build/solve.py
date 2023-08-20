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
