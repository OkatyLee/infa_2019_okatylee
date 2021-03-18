f = open('27-B.txt')

n = int(f.readline())
s = 0
r = []
nch1 = nch2 = 0
for _ in range(n):
    para = sorted(list(map(int, f.readline().split())))
    m = max(para)
    s += m
    nch1 += para[0] % 2
    nch2 += para[1] % 2
    if abs(para[0]- para[1]) % 2 == 1:
        r.append([abs(para[0]- para[1]), para])


r.sort()
ch1 = n - nch1
ch2 = n - nch2
i = 0
while abs(ch2 - ch1) > abs(ch2-ch1)%2:
    if r[i][1][0] % 2:
        ch1 += 1
        ch2 -= 1
    else:
        ch2 += 1
        ch1 -= 1
    s -= r[i][0]
print(s)