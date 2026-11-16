def add_left_digit(d, k):
    temp = k
    digits = 0
    if temp == 0:
        digits = 1
    while temp > 0:
        digits += 1
        temp //= 10
    return d * (10 ** digits) + k

k = int(input())
d1 = int(input())
k = add_left_digit(d1, k)
print(k)

d2 = int(input())
k = add_left_digit(d2, k)
print(k)