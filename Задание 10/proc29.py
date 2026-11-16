def digit_count(k):
    """Возвращает количество цифр числа k (> 0)."""
    if k == 0:
        return 1
    count = 0
    while k > 0:
        count += 1
        k //= 10
    return count

for i in range(5):
    k = int(input())
    print(digit_count(k))