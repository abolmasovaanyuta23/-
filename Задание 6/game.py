title = "ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ"
frame = "=" * 31
print(frame, f"   {title}   ", frame, sep="\n", end="\n\n")

print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!\nТы входишь в подземелье. Здесь темно и пахнет сыростью.\n")

print("Настройка героя.\nЗдоровье, сила, ловкость, выносливость по одному числу в строке:")
while True:
    try:
        health, strength, agility, endurance = int(input()), int(input()), int(input()), int(input())
        if health <= 0 or strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Неверные характеристики")
        break
    except ValueError:
        print("Ошибка. Введите четыре положительных числа снова:")

damage = 10 + strength * 1.5
crit_damage = damage * 2
stamina = health // endurance

print(
    f"\nХарактеристики героя:\nЗдоровье:     {health}\nСила:         {strength}\nЛовкость:     {agility}\nВыносливость: {endurance}\n")
print(f"Урон героя:       {damage:.1f}\nКритический урон: {crit_damage:.1f}\nЗапас сил:        {stamina}\n")

running, actions, outcome = True, 0, "прерывание"

try:
    while running:
        print(
            "Что делаешь?\n1 - осмотреться\n2 - идти вперёд\n3 - отдохнуть\n4 - прислушаться\n5 - зажечь факел\n6 - тренировка\n0 - выйти из подземелья\n")

        while True:
            try:
                p = int(input())
                if 0 <= p <= 6: break
            except ValueError:
                pass
            print("Такого пункта нет. Введи номер пункта из меню.")

        if p == 1:
            print("Вы осмотрелись. Комната пуста, только пыль на полу.")
        elif p == 2:
            if stamina >= 2:
                stamina -= 2
                print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
            else:
                health -= (2 - stamina)
                stamina = 0
                print("Сил больше нет — вы идёте на одном упорстве.")
        elif p == 3:
            stamina += 2
            print("Вы передохнули и восстановили немного сил.")
        elif p == 4:
            print("Вы замерли и прислушались: вокруг слышен лишь тихий гул.")
        elif p == 5:
            stamina -= 1
            print("Вы зажгли факел, стало светлее.")
        elif p == 6:
            stamina -= 3
            print(
                "Вы подходите к тренировочному чучелу.\nОно стоит здесь с тех пор, как сюда приходил последний искатель.\n\nНаносите 5 ударов.")
            tot, crit = 0.0, 0
            for i in range(1, 6):
                hit = crit_damage if i % 3 == 0 else damage
                if i % 3 == 0: crit += 1
                print(f"Удар {i}: {hit:.1f}" + (" — критический!" if i % 3 == 0 else ""))
                tot += hit
            print(f"\nИтог: 5 ударов, {crit} критических.\nОбщий урон: {tot:.1f}\nСредний урон: {tot / 5:.1f}")
        elif p == 0:
            print("Вы поднимаетесь обратно к свету. Подземелье остаётся позади.")
            outcome, running = "выход", False

        if health <= 0:
            print(f"{hero_name} падает без сил. Подземелье забирает ещё одного искателя.")
            outcome, running = "гибель", False

        if running: actions += 1
        print(f"\nЗдоровье: {health} Запас сил: {stamina}\n")

except KeyboardInterrupt:
    print("\nИгрок прервал сеанс.")

finally:
    print(frame)
    msg = "Ты не дошёл" if outcome == "гибель" else ("Забег окончен" if outcome == "выход" else "Сеанс прерван")
    print(f"{msg}, {hero_name}. Действий совершено: {actions}.")
    print(frame)