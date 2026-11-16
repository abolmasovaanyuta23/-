def circle_s(r):
    """Возвращает площадь круга радиуса r (pi = 3.14)."""
    return 3.14 * r * r

for i in range(3):
    r = float(input())
    print(circle_s(r))