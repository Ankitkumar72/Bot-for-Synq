arr = list(map(int, input().split()))
largest = -1
s_largest = -1
for x in arr:
    if x > largest:
        s_largest = largest 
        largest = x
    elif x < largest and x > s_largest:
        s_largest = x
print(s_largest)