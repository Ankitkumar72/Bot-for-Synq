import math

a, b = map(int, input().split())

g = math.gcd(a, b)
count = 0
for i in range(1, int(g ** 0.5) + 1):
    if g % i == 0:
        count += 1
        if i != g // i:
            count += 1

print(count)
