flag = "ctf4b{4ll_w3_h4v3_70_d3cide_1s_wh4t_t0_d0_w1th_7he_71m3_7h47_i5_g1v3n_u5}\0"

res = [0] * len(flag)

for i in range(0, 5):
    res[i] = ord(flag[i]) ^ 0x23

for i in range(5, 25):
    res[i] = ord(flag[i]) ^ 0x27

for i in range(25, 35):
    res[i] = ord(flag[i]) ^ 0x21

for i in range(35, len(flag)):
    res[i] = ord(flag[i]) ^ 0x16

print(len(flag))
print(res)
