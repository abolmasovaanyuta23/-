n = int(input())
k = 0
while n > 1 and n % 2 == 0:
    n //= 2
    k += 1
print(k)