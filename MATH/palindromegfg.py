# Question: Check if the given number is a palindrome or not. But the catch is that the palindrome is of the numbers of the sums. 

n = int (input())
digit_sum = 0
num = n
while num > 0: 
    digit_sum = digit_sum + (num % 10)
    num = num // 10
    
original = digit_sum
reverse = 0 
temp = digit_sum
while temp > 0: 
    reverse = reverse * 10 + (temp % 10)
    temp = temp // 10
print( original == reverse)