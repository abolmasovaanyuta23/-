def sum_range(a, b):
    """Возвращает сумму целых чисел от a до b включительно; если a > b, возвращает 0."""
    if a > b:
        return 0
    total = 0
    for i in range(a, b + 1):
        total += i
    return total

a = int(input())
b = int(input())
c = int(input())
print(sum_range(a, b))
print(sum_range(b, c))