import numpy as np

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

# Позиция магов в виде векторов
position_of_mage = np.zeros(amount_mage, 2)

# Событие - Атака "Огненный смерч"
def storm_attack():
    global healpoint_dragon, position_of_mage
    damage_dragon, time_attack = map(int, input().split())
    safe_zone_x, safe_zone_y = map(int, input().split())
    finish_position = np.array(safe_zone_x,safe_zone_y) # Вектор (точка) безопасной зоны
    damage_mage = 0 # Общий урон магов, имеющие полную ауру
    heal = 0 # Общий хил магов, имеющие полную ауру
    mage_aura_full = [i for i in range(amount_mage)] # Список, в котором хранятся индексы магов, аура которых не полная
    mage_not_in_safe_zone = [i for i in range(amount_mage)] # Список, где лежат индексы магов вне сейф зоны
    max_aura, speed_up_aura, speed_down_aura = statblock_aura[i][0], statblock_aura[i][1], statblock_aura[i][2]
    while time_attack > 0:
        # Проверка "Маг в сейф зоне? Если да - то урон дракону/лечение магов. Если нет - передвижение и урон магам"
        j = 0
        if mage_not_in_safe_zone:
            while j < len(mage_aura_full):
                i = mage_aura_full[j]
                # Если маг в сейф зоне, то обновление индекса состояния
                if position_of_mage[i:i+1] == finish_position: mage_not_in_safe_zone.pop(mage_not_in_safe_zone.index(i))
                # Если маг в сейф зоне, то урон дракону и лечение магов, если нет - то урон по магам, передвижение, и снижение мощности ауры
                if mage_not_in_safe_zone.count(i) == 0:
                    #  Повышение мощности ауры магов
                    if statblock_real_mage[i][1] <= max_aura:
                        if ((statblock_real_mage[i][1] + speed_up_aura) >= max_aura) | (statblock_real_mage[i][1] == max_aura):
                            statblock_real_mage[i][1] = max_aura
                            if i < amount_mage:
                                damage_mage += max_aura
                            if i >= amount_mage:
                                heal += max_aura
                            mage_aura_full.pop(j)
                            j -= 1
                        else:
                            statblock_real_mage[i][1] += speed_up_aura
                    # Нанесение урона и лечение магов
                    if i < amount_attack_mage:
                        healpoint_dragon -= statblock_real_mage[i][1]
                    else:
                        for k in range(amount_mage):
                            statblock_real_mage[k][0] += statblock_real_mage[i][1]
                            if statblock_real_mage[k][0] > healpoint_mage:
                                statblock_real_mage[k][0] = healpoint_mage
                    j += 1
                else:
                    # Передвижение
                    start_position = position_of_mage[i]
                    direct_vector = finish_position - start_position # Вектор направления мага
                    k = (np.sqrt(direct_vector.dor(direct_vector)))/ speed_of_mage # Коэф. пропорциональности
                    position_of_mage[i,:] = direct_vector / k # Передвижение
                    # Урон по магу
                    statblock_real_mage[i][0] -= damage_dragon
                    # Понижение мощности ауры магов
                    if statblock_real_mage[i][1] > 0:
                        if (statblock_real_mage[i][1] - speed_down_aura) < 0:
                            statblock_real_mage[i][1] = 0
                        else:
                            statblock_real_mage[i][1] -= speed_down_aura
        # Нанесение урона и хил от магов, кто с полной аурой
        healpoint_dragon -= damage_mage
        for i in amount_mage:
            statblock_real_mage[i][0] += heal
            if statblock_real_mage[i][0] > healpoint_mage:
                statblock_real_mage[i][0] = healpoint_mage
            if statblock_real_mage[i][0] <= 0:
                print("You are not prepared")
                exit()

        if healpoint_dragon <= 0:
            print("No useful loot again")
            print(counter_of_attack)
            exit()
        time_attack -= 1

# Событие - Атака "Дыхание дракона"
def breath_attack():


# Событие - Атака "Удар хвостом"
def tail():
    print("You are not prepared")
    exit()


# Блок с вводом типа атаки
counter_of_attack = 0
for kill_the_mage in amount_attack_of_dragon:
    counter_of_attack +=1
    type_attack = input()
    if type_attack == "Tail": tail()
    if type_attack == "Storm": storm_attack()
    if type_attack == "Breath": breath_attack()
