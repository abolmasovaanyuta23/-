try:
    n = int(input())
except ValueError:
    print("Ошибка ввода")
else:
    total = 0
    k = 0
    while total < n:
        k += 1
        total += k
    print(k)
    print(total)