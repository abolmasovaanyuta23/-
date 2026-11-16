"""Игра «Подземелье: Тихий колодец» (Финальная сборка v1.0).
Выполнила: Аболмасова Анна Владимировна, группа 2ИП-9.
"""

import json
import os
import random

try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False

VERSION = "1.0"
SAVE_FILE = "save.json"

prices = {
    "potion": 10,
    "torch_oil": 15,
    "war_elixir": 40,
}

ITEM_NAMES_RU = {
    "potion": "зелье лечения",
    "torch_oil": "масло для факела",
    "war_elixir": "боевой эликсир",
}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "ghoul": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}

ENEMY_NAMES_RU = {
    "skeleton": "скелет",
    "ghoul": "упырь",
    "spider": "паук",
    "bat": "летучая мышь",
}

MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]

DIRECTIONS = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1),
}

DIR_ALIASES = {
    "north": "north", "север": "north",
    "south": "south", "юг": "south",
    "west": "west", "запад": "west",
    "east": "east", "восток": "east",
}

DIR_NAMES_RU = {
    "north": "на север",
    "south": "на юг",
    "west": "на запад",
    "east": "на восток",
}

LOOT = {
    (1, 1): "старинная монета",
    (2, 3): "пыльное зелье",
    (3, 3): "самоцвет стража",
}

commands = [
    "осмотреться (look)", "идти [направление] (go)", "отдохнуть (rest)",
    "прислушаться (listen)", "факел (torch)", "тренироваться (train)",
    "спуститься (descend)", "лидеры (leaders)", "лавка (shop)",
    "рюкзак (backpack)", "выпить (drink)", "купить <товар> [кол-во] (buy)",
    "карта (map)", "разведка (scout)", "новая игра (newgame)",
    "помощь (help)", "выход (exit)"
]

MENU = [
    "Что будешь делать? (номер или команда; помощь — справка)",
    "1 - осмотреться (look)",
    "2 - идти вперёд (go)",
    "3 - отдохнуть (rest)",
    "4 - прислушаться (listen)",
    "5 - зажечь факел (torch)",
    "6 - потренироваться (train)",
    "7 - спуститься глубже (descend)",
    "8 - таблица лидеров (leaders)",
    "9 - лавка (shop)",
    "10 - рюкзак (backpack)",
    "11 - выпить зелье (drink)",
    "0 - выйти из подземелья (exit)",
]

num_to_verb = {
    "1": "look", "осмотреться": "look", "осмотр": "look",
    "2": "go", "идти": "go",
    "3": "rest", "отдохнуть": "rest", "отдых": "rest",
    "4": "listen", "прислушаться": "listen", "слушать": "listen",
    "5": "torch", "факел": "torch",
    "6": "train", "тренироваться": "train", "тренировка": "train",
    "7": "descend", "спуститься": "descend", "спуск": "descend",
    "8": "leaders", "лидеры": "leaders",
    "9": "shop", "лавка": "shop", "магазин": "shop",
    "10": "backpack", "рюкзак": "backpack", "инвентарь": "backpack",
    "11": "drink", "выпить": "drink",
    "0": "exit", "выход": "exit", "выйти": "exit",
    "помощь": "help", "справка": "help",
    "карта": "map",
    "разведка": "scout",
    "купить": "buy",
    "новая": "newgame", "сброс": "newgame",
}

SHOP_ALIASES = {
    "potion": "potion", "зелье": "potion",
    "torch_oil": "torch_oil", "масло": "torch_oil",
    "war_elixir": "war_elixir", "эликсир": "war_elixir",
}


class Hero:
    """Класс героя с характеристиками, методами действия и сериализацией в словарь."""

    def __init__(self, name, health, strength, agility, endurance):
        """Создаёт объект героя и вычисляет его производные характеристики."""
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        self.damage = 10 + strength * 1.5
        self.crit_damage = self.damage * 2
        self.stamina = health // endurance

    def __str__(self):
        """Возвращает формуляр героя одной строкой для print(hero)."""
        return f"{self.name}: здоровье {self.health}, урон {self.damage:.1f}, запас сил {self.stamina}"

    def strike(self, n):
        """Считает урон героя на ударе номер n (каждый третий удар — критический).
        Возвращает кортеж (hit, crit).
        """
        if n % 3 == 0:
            return self.crit_damage, True
        return self.damage, False

    def spend_stamina(self, cost):
        """Тратит запас сил; если сил не хватает, списывает разницу из здоровья.
        Возвращает True, если пришлось идти на одном упорстве, иначе False.
        """
        if self.stamina >= cost:
            self.stamina -= cost
            return False
        self.health -= (cost - self.stamina)
        self.stamina = 0
        return True

    def heal(self, amount, cap):
        """Восстанавливает здоровье на amount, не превышая потолок cap."""
        self.health = min(self.health + amount, cap)

    def to_dict(self):
        """Собирает состояние героя в словарь для сохранения в JSON."""
        return {
            "name": self.name,
            "health": self.health,
            "stamina": self.stamina,
            "strength": self.strength,
            "agility": self.agility,
            "endurance": self.endurance,
        }

    @staticmethod
    def from_dict(data):
        """Восстанавливает объект Hero из словаря сохранения."""
        hero = Hero(
            data["name"],
            data["health"],
            data["strength"],
            data["agility"],
            data["endurance"],
        )
        hero.stamina = data["stamina"]
        return hero


class Enemy:
    """Класс врага, создаваемый из словаря характеристик enemy_stats."""

    def __init__(self, name, stats):
        """Инициализирует врага по имени и словарю характеристик."""
        self.name = name
        self.hp = float(stats["hp"])
        self.damage = stats["damage"]
        self.loot = stats["loot"]


def fight(enemy, hero, bonus=0):
    """Проводит бой между объектами enemy и hero до гибели одного из них.
    bonus — надбавка к урону героя (по умолчанию 0).
    Печатает строки раундов. Возвращает кортеж (rounds, won, loot).
    """
    rounds = []
    round_n = 0
    enemy_ru = ENEMY_NAMES_RU.get(enemy.name, enemy.name)
    print(f"Ты спускаешься по ступеням. Из темноты появляется {enemy_ru}!")
    while enemy.hp > 0 and hero.health > 0:
        round_n += 1
        hit, crit = hero.strike(round_n)
        hit += bonus
        enemy.hp -= hit
        line = f"Раунд {round_n}: герой наносит {hit:.1f} урона"
        if crit:
            line += " — критический удар!"

        if enemy.hp <= 0:
            line += " Враг повержен."
            rounds.append([round_n, hit, 0])
            print(line)
            break
        else:
            blow = enemy.damage
            hero.health -= blow
            line += f" (у врага осталось {enemy.hp:.1f} ОЗ). {enemy_ru.capitalize()} бьёт на {blow}."
            rounds.append([round_n, hit, blow])
            print(line)

    won = enemy.hp <= 0
    loot = enemy.loot if won else 0
    return rounds, won, loot


def buy(price, gold, quantity=1):
    """Покупает quantity штук товара ценой price за золото gold (quantity по умолчанию 1).
    Возвращает (gold_left, ok). Ничего не печатает.
    """
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False


def scout(r, c, seen):
    """Рекурсивно считает количество доступных комнат на карте от клетки (r, c)."""
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total


def print_leaderboard(log):
    """Печатает топ-3 раундов по урону героя и самый сильный удар врага. Возвращает None."""
    if not log:
        print("Ты ещё ни разу не сражался.")
        return
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Таблица лидеров (урон героя):")
    for i in range(len(top)):
        print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
    worst = max(log, key=lambda r: r[2])
    print(f"Самый сильный удар врага: {worst[2]} (раунд {worst[0]}).")


def print_run_summary(log):
    """Печатает итоговый суммарный и средний урон героя за забег. Возвращает None."""
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Урон: {total:.1f} за {rounds} раундов, в среднем {total / rounds:.1f}.")
    else:
        print("В этом забеге боёв не было.")


def parse_command(line):
    """Нормализует ввод игрока и возвращает пару (verb, words): глагол и список слов."""
    cmd = line.strip().lower()
    words = cmd.split()
    if not words:
        return "", []
    verb = words[0]
    if verb in num_to_verb:
        verb = num_to_verb[verb]
    return verb, words


def write_save(hero, max_health, max_stamina, gold_total, ability_bonus, actions,
               enemies, hero_r, hero_c, visited, found_loot, inventory, log):
    """Записывает текущее состояние забега в JSON-файл. Возвращает None."""
    save_data = {
        "hero": hero.to_dict(),
        "max_health": max_health,
        "max_stamina": max_stamina,
        "gold": gold_total,
        "ability_bonus": ability_bonus,
        "actions": actions,
        "enemies": enemies,
        "position": [hero_r, hero_c],
        "visited": [list(p) for p in visited],
        "loot": sorted(found_loot),
        "inventory": inventory,
        "log": log,
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)


title = "   ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ   "
frame = "=" * 33
print(frame)
print(title)
print(f"              v{VERSION}")
print(frame)

loaded = None
if os.path.exists(SAVE_FILE):
    print("Найдено сохранение. Продолжить забег? (да/нет)")
    answer = input().strip().lower()
    if answer in ("да", "д", "yes", "y"):
        try:
            with open(SAVE_FILE, encoding="utf-8") as f:
                loaded = json.load(f)
        except (json.JSONDecodeError, KeyError):
            print("Файл сохранения повреждён. Начинаем новый забег.")
            loaded = None

if loaded is None:
    print("Как зовут героя?")
    hero_name = input().strip() or "Аня"
    print(f"Добро пожаловать, {hero_name}!")
    print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
    print()
    print("Настройка героя.")
    print("Введи здоровье, силу, ловкость и выносливость (по одному числу в строке):")
    while True:
        try:
            h_val = int(input())
            s_val = int(input())
            a_val = int(input())
            e_val = int(input())
            if h_val <= 0:
                raise ValueError(f"здоровье должно быть больше нуля, получено {h_val}")
            if s_val < 0 or a_val < 0 or e_val <= 0:
                raise ValueError("некорректные характеристики (выносливость > 0, остальные >= 0)")
            break
        except ValueError as e:
            print(f"Ошибка ввода: {e}. Введи все четыре числа заново:")

    hero = Hero(hero_name, h_val, s_val, a_val, e_val)
    max_health = hero.health
    max_stamina = hero.stamina
    gold_total = 0
    ability_bonus = 0
    actions = 0
    enemies = ["skeleton", "ghoul", "spider", "bat"]
    hero_r, hero_c = 4, 2
    visited = {(4, 2)}
    found_loot = set()
    inventory = {}
    log = []
    print()
    print(hero)
    print()
else:
    hero = Hero.from_dict(loaded["hero"])
    max_health = loaded.get("max_health", hero.health)
    max_stamina = loaded.get("max_stamina", hero.stamina)
    gold_total = loaded.get("gold", 0)
    ability_bonus = loaded.get("ability_bonus", 0)
    actions = loaded.get("actions", 0)
    enemies = loaded.get("enemies", ["skeleton", "ghoul", "spider", "bat"])
    hero_r, hero_c = loaded.get("position", [4, 2])
    visited = {tuple(p) for p in loaded.get("visited", [[4, 2]])}
    found_loot = set(loaded.get("loot", []))
    inventory = loaded.get("inventory", {})
    log = loaded.get("log", [])
    print(f"Забег продолжен: здоровье {hero.health}, золото {gold_total}, осталось врагов: {len(enemies)}.")
    print()

running = True
outcome = "interrupt"

try:
    while running:
        print("\n".join(MENU))
        print()

        line = input()
        verb, words = parse_command(line)
        while verb == "":
            print("Пустая команда. Введи команду или номер.")
            line = input()
            verb, words = parse_command(line)

        if verb == "help":
            print("Доступные команды: " + ", ".join(commands) + ".")
            print("Цифры 0–11 также работают.")

        elif verb == "newgame":
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
                print("Сохранение удалено. Следующий забег начнётся с чистого листа.")
            else:
                print("Сохранений для удаления нет.")
            continue

        elif verb == "look":
            print("Ты осматриваешься. Комната пуста, только пыль на полу.")

        elif verb == "go":
            if len(words) > 1 and words[1] in DIR_ALIASES:
                direction = DIR_ALIASES[words[1]]
                dr, dc = DIRECTIONS[direction]
                nr, nc = hero_r + dr, hero_c + dc
                if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                    hero_r, hero_c = nr, nc
                    visited.add((hero_r, hero_c))
                    if (hero_r, hero_c) in LOOT:
                        found_item = LOOT[(hero_r, hero_c)]
                        if found_item not in found_loot:
                            found_loot.add(found_item)
                            print(f"Находка: {found_item}! Уникальных находок: {len(found_loot)}.")
                    print(f"Ты идёшь {DIR_NAMES_RU[direction]}. Комната ({hero_r}, {hero_c}).")
                else:
                    print(f"Нельзя пройти {DIR_NAMES_RU[direction]}: стена или край карты.")
            else:
                exhausted = hero.spend_stamina(2)
                if not exhausted:
                    print("Ты осторожно продвигаешься вперёд. Пол скрипит под ногами.")
                else:
                    print("Запас сил иссяк — ты идёшь вперёд на одном упорстве.")

        elif verb == "rest":
            hero.stamina = min(hero.stamina + 2, max_stamina)
            print("Ты отдыхаешь и восстанавливаешь немного сил.")

        elif verb == "listen":
            print("Ты замираешь и прислушиваешься: вокруг слышен лишь глухой гул.")

        elif verb == "torch":
            hero.spend_stamina(1)
            print("Ты зажигаешь факел, вокруг становится светлее.")

        elif verb == "train":
            strikes = 5
            hero.spend_stamina(3)
            print("Ты подходишь к тренировочному чучелу.")
            print("Оно стоит здесь со времён прошлого искателя.")
            print()
            print(f"Ты наносишь {strikes} ударов.")
            total_dmg = 0.0
            crit_cnt = 0
            for i in range(1, strikes + 1):
                hit_dmg, crit = hero.strike(i)
                hit_dmg += ability_bonus
                if crit:
                    print(f"Удар {i}: {hit_dmg:.1f} — критический!")
                    crit_cnt += 1
                else:
                    print(f"Удар {i}: {hit_dmg:.1f}")
                total_dmg += hit_dmg
            print()
            print(f"Итого: {strikes} ударов, критических: {crit_cnt}.")
            print(f"Общий урон: {total_dmg:.1f}")
            print(f"Средний урон: {total_dmg / strikes:.1f}")

        elif verb == "descend":
            if not enemies:
                print("Ты спускаешься по ступеням, но подземелье пусто.")
            else:
                enemy_name = random.choice(enemies)
                foe = Enemy(enemy_name, enemy_stats[enemy_name])
                rounds, won, loot = fight(foe, hero, bonus=ability_bonus)
                for r in rounds:
                    log.append(r)
                if won:
                    gold_total += loot
                    enemies.remove(enemy_name)
                    enemy_ru = ENEMY_NAMES_RU.get(enemy_name, enemy_name).capitalize()
                    win_msg = f"{enemy_ru} повержен! В подземелье осталось врагов: {len(enemies)}. Добыча: {loot} золота."
                    if COLOR:
                        print(Fore.YELLOW + win_msg + Style.RESET_ALL)
                    else:
                        print(win_msg)
                print(f"Бой длился раундов: {len(rounds)}.")

        elif verb == "leaders":
            print_leaderboard(log)

        elif verb == "shop":
            print("Лавка:")
            for item_key, item_price in prices.items():
                print(f"{ITEM_NAMES_RU[item_key]} ({item_key}): {item_price} золота")
            print("Введи 'купить <товар> [количество]' для покупки.")

        elif verb == "buy":
            if len(words) > 1 and words[-1].isdigit():
                qty = int(words[-1])
                raw_name = "_".join(words[1:-1])
            else:
                qty = 1
                raw_name = "_".join(words[1:])

            if raw_name == "":
                print("Что купить? Введи: купить <товар>.")
                continue

            item_name = SHOP_ALIASES.get(raw_name, raw_name)
            if item_name not in prices:
                print("Такого товара нет в лавке.")
                continue

            item_price = prices[item_name]
            gold_total, ok = buy(item_price, gold_total, quantity=qty)
            if ok:
                if item_name == "war_elixir":
                    ability_bonus += 2 * qty
                elif item_name == "torch_oil":
                    hero.stamina = min(hero.stamina + 5 * qty, max_stamina)
                else:
                    inventory[item_name] = inventory.get(item_name, 0) + qty
                print(f"Куплено: {ITEM_NAMES_RU[item_name]} ({qty} шт.) за {item_price * qty} золота. Осталось золота: {gold_total}.")
            else:
                print(f"Недостаточно золота: нужно {item_price * qty}, есть {gold_total}.")

        elif verb == "backpack":
            if not inventory:
                print("Рюкзак пуст.")
            else:
                print("Рюкзак:")
                for item_key, qty in inventory.items():
                    print(f"{ITEM_NAMES_RU.get(item_key, item_key)}: {qty} шт.")

        elif verb == "drink":
            raw_name = "_".join(words[1:]) or "potion"
            item_name = SHOP_ALIASES.get(raw_name, raw_name)
            if inventory.get(item_name, 0) == 0:
                print(f"В рюкзаке нет предмета «{ITEM_NAMES_RU.get(item_name, item_name)}».")
            else:
                hero.heal(10, max_health)
                inventory[item_name] -= 1
                if inventory[item_name] == 0:
                    del inventory[item_name]
                print(f"Ты выпиваешь зелье. Здоровье: {hero.health}. Осталось зелий: {inventory.get(item_name, 0)}.")

        elif verb == "map":
            print("Карта:")
            for i in range(len(MAP)):
                cells = []
                for j in range(len(MAP[i])):
                    cell = "@" if (i, j) == (hero_r, hero_c) else MAP[i][j]
                    cells.append(cell)
                print(" ".join(cells))

        elif verb == "scout":
            seen = set()
            reachable = scout(hero_r, hero_c, seen)
            print(f"Разведка: доступно комнат — {reachable}.")

        elif verb == "exit":
            print("Ты поднимаешься обратно к свету. Подземелье остаётся позади.")
            write_save(hero, max_health, max_stamina, gold_total, ability_bonus, actions,
                       enemies, hero_r, hero_c, visited, found_loot, inventory, log)
            print("Прогресс сохранён.")
            outcome = "exit"
            running = False

        else:
            print(f"Непонятная команда: «{line.strip()}». Введи «помощь».")
            continue

        if hero.health <= 0:
            print(f"{hero.name} падает без сил. Подземелье забирает ещё одного искателя.")
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            outcome = "death"
            running = False

        if running:
            actions += 1

        print()
        state = f"Здоровье: {hero.health} | Запас сил: {hero.stamina} | Врагов: {len(enemies)} | Золото: {gold_total}"
        if COLOR:
            print(Fore.GREEN + state + Style.RESET_ALL)
        else:
            print(state)
        print()

except KeyboardInterrupt:
    print()
    print("Игрок прервал сессию.")
    write_save(hero, max_health, max_stamina, gold_total, ability_bonus, actions,
               enemies, hero_r, hero_c, visited, found_loot, inventory, log)

finally:
    if inventory:
        print("Осталось в рюкзаке:")
        for item_key, qty in inventory.items():
            print(f"{ITEM_NAMES_RU.get(item_key, item_key)}: {qty} шт.")
    else:
        print("В рюкзаке ничего не осталось.")

    print(frame)
    if outcome == "death":
        print(f"Ты не справился, {hero.name}. Сделано ходов: {actions}.")
    elif outcome == "exit":
        print(f"Забег завершён, {hero.name}. Сделано ходов: {actions}.")
    else:
        print(f"Сессия прервана, {hero.name}. Сделано ходов: {actions}.")

    print_run_summary(log)
    print(frame)
