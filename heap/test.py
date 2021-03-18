from itertools import combinations
f = open('27-B.txt')
n = int(f.readline())
a = []
for _ in range(n):
    a.append(int(f.readline()))

a.sort(reverse=True)

a1 = []
a2 = []
a3 = []

for x in a:
    if x % 3 == 1:
        if len(a1) < 3:
            a1.append(x)
    if x % 3 == 2:
        if len(a1) < 3:
            a2.append(x)
    if x % 3 == 0:
        if len(a1) < 3:
            a3.append(x)
    if len(a1) == len(a2) == len(a3) == 3:
        break

b = a1 + a2 + a3
s = 0
for x in combinations(b, 3):
    if sum(x) % 3 == 0:
        s = max(s, sum(x))
print(s)