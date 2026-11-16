try:
    a = float(input())
    b = float(input())
    print(round(a / b, 1))
except ZeroDivisionError:
    print("Делить на ноль нельзя")