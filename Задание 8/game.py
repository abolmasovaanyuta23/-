import random

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
while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        endurance = int(input())
        
        if health <= 0:
            raise ValueError(f"Здоровье должно быть положительным, а введено {health}")
        if strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Характеристики не могут быть отрицательными")
        break
    except ValueError as e:
        print(f"Ой: {e}. Введите все четыре снова:")

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
menu_last = 8
outcome = "прерывание"
log = []
enemies_left = 3

try:
    while running:
        print("Что делаешь?")
        print("1 - осмотреться")
        print("2 - идти вперёд")
        print("3 - отдохнуть")
        print("4 - прислушаться")
        print("5 - зажечь факел")
        print("6 - тренировка")
        print("7 - спуститься глубже")
        print("8 - таблица лидеров")
        print("0 - выйти из подземелья")
        print()

        while True:
            choice_str = input()
            try:
                menu_number = int(choice_str)
            except ValueError:
                print("Такого пункта нет. Введи номер пункта из меню.")
                continue
            
            if 0 <= menu_number <= menu_last:
                choice = str(menu_number)
                break
            print("Такого пункта нет. Введи номер пункта из меню.")

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
            
            total_dmg = 0.0
            crit_cnt = 0
            
            for i in range(1, strikes + 1):
                if i % 3 == 0:
                    hit_dmg = crit_damage
                    print(f"Удар {i}: {hit_dmg:.1f} — критический!")
                    crit_cnt += 1
                else:
                    hit_dmg = damage
                    print(f"Удар {i}: {hit_dmg:.1f}")
                total_dmg += hit_dmg
                
            avg_dmg = total_dmg / strikes
            print()
            print(f"Итог: {strikes} ударов, {crit_cnt} критических.")
            print(f"Общий урон: {total_dmg:.1f}")
            print(f"Средний урон: {avg_dmg:.1f}")
        elif choice == "7":
            if enemies_left <= 0:
                print("В подземелье больше никого нет.")
            else:
                enemy = "скелет"
                enemy_hp = 45.0
                print(f"Вы спускаетесь глубже. Из темноты появляется {enemy}!")
                round_n = 0
                while enemy_hp > 0 and health > 0:
                    round_n += 1
                    is_crit = (round_n % 3 == 0)
                    hit = crit_damage if is_crit else damage
                    enemy_hp -= hit
                    line = f"Раунд {round_n}: герой наносит {hit:.1f}"
                    if is_crit:
                        line += " критический!"
                    
                    if enemy_hp <= 0:
                        line += " Враг повержен."
                        log.append([round_n, hit, 0.0])
                        print(line)
                        break
                    else:
                        blow = float(random.randint(2, 6))
                        health -= blow
                        line += f" Здоровье врага: {enemy_hp:.1f}. Враг бьёт на {blow:.0f}."
                        log.append([round_n, hit, blow])
                        print(line)
                
                if enemy_hp <= 0:
                    enemies_left -= 1
                    print(f"Победа! В подземелье осталось врагов: {enemies_left}.")
                print(f"Бой завершен за {round_n} раундов.")
        elif choice == "8":
            if not log:
                print("Вы ещё не сражались.")
            else:
                top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
                print("Таблица лидеров (урон героя):")
                for i in range(len(top)):
                    print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
                worst = max(log, key=lambda r: r[2])
                print(f"Самый сильный удар врага: {worst[2]:.0f} (раунд {worst[0]}).")
        elif choice == "0":
            print("Вы поднимаетесь обратно к свету. Подземелье остаётся позади.")
            outcome = "выход"
            running = False

        if health <= 0:
            print(f"{hero_name} падает без сил. Подземелье забирает ещё одного искателя.")
            outcome = "гибель"
            running = False

        if running:
            actions += 1

        print()
        print(f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {enemies_left}")
        print()

except KeyboardInterrupt:
    print()
    print("Игрок прервал сеанс.")

finally:
    print(frame)
    if outcome == "гибель":
        print(f"Ты не дошёл, {hero_name}. Действий совершено: {actions}.")
    elif outcome == "выход":
        print(f"Забег окончен, {hero_name}. Действий совершено: {actions}.")
    else:
        print(f"Сеанс прерван, {hero_name}. Действий совершено: {actions}.")
    
    total_battle_damage = sum(r[1] for r in log)
    rounds_total = len(log)
    if rounds_total > 0:
        avg_battle_damage = total_battle_damage / rounds_total
        print(f"Урон: {total_battle_damage:.1f} за {rounds_total} раундов, в среднем {avg_battle_damage:.1f}.")
    else:
        print("Боёв в этом забеге не было.")
    print(frame)
