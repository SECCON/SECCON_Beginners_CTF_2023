# Three

## 問題文

このファイル、中身をちょっと見ただけではフラグは分からないみたい！

バイナリファイルを解析する、専門のツールとか必要かな？

## 難易度

**Easy**

## 作問にあたって

静的解析

## 解法

```python
#!/usr/bin/env python3
enc_1 = 'c4c_ub__dt_r_1_4}'
enc_2 = 'tb4y_1tu04tesifgf{n0ae0n_e4ept13'

flag = ''

for i in range(0x31):
    if i%3 == 0:
        flag += enc_1[i//3]
    elif i%3 == 1:
        flag += enc_2[i//3]
    else:
        flag += enc_2[i//3 + 0x10]

print(flag)
```
