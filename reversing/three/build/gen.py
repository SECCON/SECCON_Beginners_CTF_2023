flag = "ctf4b{c4n_y0u_ab1e_t0_und0_t4e_t4ree_sp1it_f14g3}"

flag_0 = []
flag_1 = []
flag_2 = []

for i in range(len(flag)):
    if i % 3 == 0:
        flag_0.append(ord(flag[i]))
    if i % 3 == 1:
        flag_1.append(ord(flag[i]))
    if i % 3 == 2:
        flag_2.append(ord(flag[i]))

print(flag_0)
print(flag_1)
print(flag_2)
