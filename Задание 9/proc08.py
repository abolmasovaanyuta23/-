def add_right_digit(d, k):
    return k * 10 + d

k = int(input())
d1 = int(input())
k = add_right_digit(d1, k)
print(k)

d2 = int(input())
k = add_right_digit(d2, k)
print(k)