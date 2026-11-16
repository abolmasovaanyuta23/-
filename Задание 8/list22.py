n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
d = int(input())
multiplied = [x * d for x in a]
count_d = len([x for x in a if x == d])
print(multiplied)
print(count_d)