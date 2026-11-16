try:
    a = float(input())
    b = float(input())
    result = (a + b) / 2
except ValueError:
    print("Ошибка ввода")
else:
    print(result)