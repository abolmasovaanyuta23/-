def roots_count(a, b, c):
    """Возвращает число корней квадратного уравнения по дискриминанту."""
    d = b**2 - 4 * a * c
    if abs(d) < 1e-9:
        return 1
    elif d > 0:
        return 2
    else:
        return 0

for i in range(3):
    a = float(input())
    b = float(input())
    c = float(input())
    print(roots_count(a, b, c))