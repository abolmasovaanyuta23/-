title = "ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ"
frame = "=" * 31
print(frame)
print(f"   {title}   ")
print(frame)
print()

print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость по одному числу в строке:")
health = int(input())
strength = int(input())
agility = int(input())
endurance = int(input())

base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = health // endurance

print()
print("Характеристики героя:")
print(f"Здоровье:     {health}")
print(f"Сила:         {strength}")
print(f"Ловкость:     {agility}")
print(f"Выносливость: {endurance}")
print()
print(f"Урон героя:       {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Запас сил:        {stamina}")
print()

print("Что делаешь?")
print("1 - осмотреться")
print("2 - идти вперёд")
print("3 - отдохнуть")
print("4 - прислушаться")
print("5 - зажечь факел")
print()

choice = input()

if choice == "1":
    print("Вы осмотрелись. Комната пуста, только пыль на полу.")
elif choice == "2":
    stamina -= 2
    print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
elif choice == "3":
    stamina += 2
    print("Вы передохнули и восстановили немного сил.")
elif choice == "4":
    print("Вы замерли и прислушались: вокруг слышен лишь тихий гул.")
elif choice == "5":
    stamina -= 1
    print("Вы зажгли факел, стало светлее.")
else:
    print("Такого действия нет.")

print()
print(f"Здоровье: {health} Запас сил: {stamina}")
print()

print(frame)
print(f"Удачи, {hero_name}!")
print(frame)