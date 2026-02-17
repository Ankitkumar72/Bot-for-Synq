n = int (input())
num = n
nod = len(str(n))
total = 0
while num > 0:
    ld = num %10 
    total = total + (ld ** nod)
    num = num // 10
print(total == n)
    