try:
    number = int(input())
except ValueError:
    print("Ошибка ввода")
else:
    if number > 0:
        number += 1
    elif number < 0:
        number -= 2
    else:
        number = 10
    print(number)