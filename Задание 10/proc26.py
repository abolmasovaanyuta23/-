def is_power5(k):
    """Возвращает True, если k (> 0) является степенью пятёрки."""
    if k <= 0:
        return False
    while k > 1:
        if k % 5 != 0:
            return False
        k //= 5
    return True

count = 0
for i in range(10):
    k = int(input())
    if is_power5(k):
        count += 1
print(count)