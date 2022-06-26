# Входные данные блока стистики
amount_attack_mage, amount_healer_mage, amount_attack_of_dragon = map(int, input().split())
amount_mage = amount_attack_mage+amount_healer_mage
healpoint_mage, speed_of_mage, healpoint_dragon = map(int, input().split())

# Статблок ауры магов: 0 - макс. мощность ауры, 1 - скорость роста мощности ауры, 2 - скорость уменьшения мощности ауры
statblock_aura = [[int (i) for i in input().split()] for j in range(amount_mage)]

# Статблок текущих хп и ауры [! В начале идут дамагеры, после - хиллеры !]
statblock_real_mage = []
for i in range(amount_mage):
    if i < amount_mage:
        statblock_real_mage.append([healpoint_mage, 0])
    else:
        statblock_real_mage.append([healpoint_mage, statblock_aura[i][0]])

# Позиция магов
position_of_mage = [[0] * 2 for i in range(amount_mage)]

# Событие - Атака "Огненный смерч"
def storm_attack():
    global healpoint_dragon
    damage_dragon, time_attack = map(int, input().split())
    safe_zone_x, safe_zone_y = map(int, input().split())
    heal = 0  # Общий хил магов
    damage_mage = 0 # Общий урон магов
    mage_aura_full = [i for i in range(amount_mage)] # Список, в котором хранятся индексы магов, аура которых не полная
    mage_in_safe_zone = [0 for i in range(amount_mage)] # Список, где лежит индекс состояния магов (0 - не в сейф зоне, 1 - в сейф зоне)
    max_aura, speed_up_aura, speed_down_aura = statblock_aura[i][0], statblock_aura[i][1], statblock_aura[i][2]
    while time_attack > 0:
        # Проверка "Маг в сейф зоне? Если да - то урон дракону/лечение магов. Если нет - передвижение и урон магам"
        j = 0
        if mage_in_safe_zone.count(0) > 0:
            while j < len(mage_aura_full):
                i = mage_aura_full[j]
                # Если маг в сейф зоне, то обновление индекса состояния
                if (position_of_mage[i][0] == safe_zone_x) & (position_of_mage[i][1] == safe_zone_y): mage_in_safe_zone[i] = 1
                # Если маг в сейф зоне, то урон дракону и лечение магов, если нет - то урон по магам, передвижение, и снижение мощности ауры
                if mage_in_safe_zone[i] == 1:
                    #  Повышение мощности ауры магов
                    if statblock_real_mage[i][1] < max_aura:
                        if (statblock_real_mage[i][1] + speed_up_aura) > max_aura:
                            statblock_real_mage[i][1] = max_aura
                            mage_aura_full.pop(j)
                            j -= 1
                        else:
                            statblock_real_mage[i][1] += speed_up_aura
                    # Подсчёт общего урона и лечения магов
                    if i < amount_attack_mage:
                        damage_mage += statblock_real_mage[i][1]
                    else:
                        heal += statblock_real_mage[i][1]
                    j += 1
                else:
                    # Урон по магу
                    statblock_real_mage[i][0] -= damage_dragon
                    # Понижение мощности ауры магов
                    if statblock_real_mage[i][1] > 0:
                        if (statblock_real_mage[i][1] - speed_down_aura) < 0:
                            statblock_real_mage[i][1] = 0
                        else:
                            statblock_real_mage[i][1] -= speed_down_aura
                    # Передвижение




        time_attack -= 1



# Событие - Атака "Дыхание дракона"
def breath_attack():





while type_attack <> "Tail":
    if type_attack == "Storm": storm_attack()
    if type_attack == "Breath": breath_attack()
