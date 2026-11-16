n = int(input())
s = []
for i in range(n):
    s.append(input())
lengths = [len(line) for line in s]
print(lengths)
print(sum(lengths))