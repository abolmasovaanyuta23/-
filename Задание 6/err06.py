text = input()
try:
    index = int(input())
    print(text[index])
except ValueError:
    print("Ошибка ввода")
except IndexError:
    print("Нет такого символа")