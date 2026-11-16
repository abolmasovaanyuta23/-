def minmax(x, y):
    if x < y:
        return x, y
    return y, x

a = float(input())
b = float(input())
c = float(input())
d = float(input())

min_ab, max_ab = minmax(a, b)
min_cd, max_cd = minmax(c, d)

final_min, _ = minmax(min_ab, min_cd)
_, final_max = minmax(max_ab, max_cd)

print(final_min)
print(final_max)