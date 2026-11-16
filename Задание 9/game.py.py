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

def hero_hit(strike_n):
    """Урон героя в удар номер strike_n.
    Возвращает пару (hit, crit): урон и признак критического удара.
    Читает глобальные правила damage и crit_damage, не меняет ничего.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False

def fight(enemy, hero_health):
    """Бой с врагом до гибели одного из двоих.
    Печатает строки раундов. Возвращает (rounds, won, hero_health):
    таблицу раундов, признак победы героя и здоровье после боя.
    Глобальные переменные не меняет: здоровье приходит параметром
    и возвращается новым значением.
    """
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"You descend the stairs. Out of the darkness comes {enemy}!")
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        enemy_hp -= hit
        line = f"Round {round_n}: hero deals {hit:.1f}"
        if crit:
            line += " critical!"
        
        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
            print(line)
            break
        else:
            blow = float(random.randint(2, 6))
            hero_health -= blow
            line += f" {enemy} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow:.0f}."
            rounds.append([round_n, hit, blow])
            print(line)
            
    return rounds, enemy_hp <= 0, hero_health

def print_leaderboard(log):
    """Печатает топ-3 раундов по урону героя и рекорд врага.
    Возвращает None: контракт функции — печать, а не данные.
    """
    if not log:
        print("You haven't fought yet.")
        return
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Leaderboard (hero damage):")
    for i in range(len(top)):
        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")
    worst = max(log, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]:.0f} (round {worst[0]}).")

def print_run_summary(log):
    """Печатает итог забега: суммарный и средний урон героя.
    Возвращает None. Безопасна на пустом журнале.
    """
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")

running = True
actions = 0
menu_last = 8
outcome = "прерывание"
log = []
enemies = ["скелет", "гоблин", "орки"]

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
            
            total_damage = 0.0
            crit_count = 0
            
            for i in range(1, strikes + 1):
                hit_damage, crit = hero_hit(i)
                if crit:
                    print(f"Удар {i}: {hit_damage:.1f} — критический!")
                    crit_count += 1
                else:
                    print(f"Удар {i}: {hit_damage:.1f}")
                total_damage += hit_damage
                
            avg_damage = total_damage / strikes
            print()
            print(f"Итог: {strikes} ударов, {crit_count} критических.")
            print(f"Общий урон: {total_damage:.1f}")
            print(f"Средний урон: {avg_damage:.1f}")
        elif choice == "7":
            if not enemies:
                print("You descend the stairs. But the dungeon is empty.")
            else:
                enemy = random.choice(enemies)
                rounds, won, health = fight(enemy, health)
                for r in rounds:
                    log.append(r)
                if won:
                    enemies.remove(enemy)
                    print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")
                print(f"Battle: {len(rounds)} rounds.")
        elif choice == "8":
            print_leaderboard(log)
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
        print(f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {len(enemies)}")
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
    
    print_run_summary(log)
    print(frame)
