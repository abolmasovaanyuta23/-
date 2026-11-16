def is_power_n(k, n):
    """Возвращает True, если k (> 0) является степенью n (> 1)."""
    if k <= 0 or n <= 1:
        return False
    while k > 1:
        if k % n != 0:
            return False
        k //= n
    return True

n = int(input())
count = 0
for i in range(10):
    k = int(input())
    if is_power_n(k, n):
        count += 1
print(count)