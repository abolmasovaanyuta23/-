n = int(input())
s = []
for i in range(n):
    s.append(input())
letter = input()
matched = [line for line in s if line and line[0] == letter]
print(matched)