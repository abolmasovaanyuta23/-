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

max_health = health
max_stamina = stamina

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

def fight(enemy, hero_health, bonus=0):
    """Бой с врагом до гибели одного из двоих.
    bonus — надбавка к урону героя, по умолчанию 0: без эликсира
    бой идёт как прежде. Печатает строки раундов.
    Возвращает (rounds, won, hero_health, loot).
    """
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"You descend the stairs. Out of the darkness comes {enemy}!")
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        hit = hit + bonus
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
            
    won = (enemy_hp <= 0)
    loot = 25 if won else 0
    return rounds, won, hero_health, loot

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

def buy(price, gold, quantity=1):
    """Покупает quantity штук товара ценой price за золото gold.
    quantity по умолчанию 1. Возвращает (gold_left, ok): остаток
    золота и признак успешной покупки. Ничего не печатает.
    """
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False

running = True
actions = 0
menu_last = 9
outcome = "прерывание"
log = []
enemies = ["скелет", "гоблин", "орки"]
gold_total = 0
ability_bonus = 0

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
        print("9 - магазин")
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
                hit_damage += ability_bonus
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
                rounds, won, health, loot = fight(enemy, health, bonus=ability_bonus)
                for r in rounds:
                    log.append(r)
                if won:
                    gold_total += loot
                    enemies.remove(enemy)
                    print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon. Loot: {loot} gold.")
                print(f"Battle: {len(rounds)} rounds.")
        elif choice == "8":
            print_leaderboard(log)
        elif choice == "9":
            print("Shop:")
            print("1 - potion (+10 health): 10 gold")
            print("2 - torch oil (+5 stamina): 15 gold")
            print("3 - war elixir (+2 damage for the run): 40 gold")
            print("Item number (0 not buying):")
            item = input()
            prices = (10, 15, 40)
            names = ("potion", "torch oil", "war elixir")
            if item in ("1", "2", "3"):
                price = prices[int(item) - 1]
                name = names[int(item) - 1]
                print("Quantity (Enter for one):")
                qty_line = input()
                if qty_line == "":
                    qty = 1
                    gold_total, ok = buy(price, gold_total)
                else:
                    qty = int(qty_line)
                    gold_total, ok = buy(price, gold_total, quantity=qty)
                
                if ok:
                    if item == "1":
                        health = min(health + 10 * qty, max_health)
                    elif item == "2":
                        stamina = min(stamina + 5 * qty, max_stamina)
                    else:
                        ability_bonus += 2 * qty
                    print(f"Bought {qty} {name} for {price * qty} gold. Gold left: {gold_total}.")
                else:
                    print(f"Not enough gold: need {price * qty}, have {gold_total}.")
            elif item != "0":
                print("No such item in the shop.")
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
        print(f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)} Gold: {gold_total}")
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
