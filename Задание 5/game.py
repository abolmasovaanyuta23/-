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

running = True
actions = 0
valid = ("0", "1", "2", "3", "4", "5", "6")

while running:
    print("Что делаешь?")
    print("1 - осмотреться")
    print("2 - идти вперёд")
    print("3 - отдохнуть")
    print("4 - прислушаться")
    print("5 - зажечь факел")
    print("6 - тренировка")
    print("0 - выйти из подземелья")
    print()

    choice = input()
    while choice not in valid:
        print("Такого пункта нет. Введи номер пункта из меню.")
        choice = input()

    if choice == "1":
        print("Вы осмотрелись. Комната пуста, только пыль на полу.")
    elif choice == "2":
        cost = 2
        if stamina >= cost:
            stamina -= cost
            print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
        else:
            health -= (cost - stamina)
            stamina = 0
            print("Сил больше нет — вы идёте на одном упорстве.")
    elif choice == "3":
        stamina += 2
        print("Вы передохнули и восстановили немного сил.")
    elif choice == "4":
        print("Вы замерли и прислушались: вокруг слышен лишь тихий гул.")
    elif choice == "5":
        stamina -= 1
        print("Вы зажгли факел, стало светлее.")
    elif choice == "6":
        strikes = 5
        stamina -= 3
        print("Вы подходите к тренировочному чучелу.")
        print("Оно стоит здесь с тех пор, как сюда приходил последний искатель.")
        print()
        print(f"Наносите {strikes} ударов.")

        total_damage = 0.0
        crit_count = 0

        for i in range(1, strikes + 1):
            if i % 3 == 0:
                hit_damage = crit_damage
                print(f"Удар {i}: {hit_damage:.1f} — критический!")
                crit_count += 1
            else:
                hit_damage = damage
                print(f"Удар {i}: {hit_damage:.1f}")
            total_damage += hit_damage

        avg_damage = total_damage / strikes
        print()
        print(f"Итог: {strikes} ударов, {crit_count} критических.")
        print(f"Общий урон: {total_damage:.1f}")
        print(f"Средний урон: {avg_damage:.1f}")
    elif choice == "0":
        print("Вы поднимаетесь обратно к свету. Подземелье остаётся позади.")
        running = False

    if health <= 0:
        print(f"{hero_name} падает без сил. Подземелье забирает ещё одного искателя.")
        running = False

    if running:
        actions += 1

    print()
    print(f"Здоровье: {health} Запас сил: {stamina}")
    print()

print(frame)
if health <= 0:
    print(f"Ты не дошёл, {hero_name}. Действий совершено: {actions}.")
else:
    print(f"Забег окончен, {hero_name}. Действий совершено: {actions}.")
print(frame)