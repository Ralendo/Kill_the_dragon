import numpy as np

# Входные данные блока стистики
amount_damager_mage, amount_healer_mage, amount_attack_of_dragon = map(int, input().split())
amount_mage = amount_damager_mage + amount_healer_mage
healpoint_mage, speed_of_mage, healpoint_dragon = map(int, input().split())

# Статблок ауры магов. Столбцы: 0 - макс. мощность ауры, 1 - скорость роста мощности ауры, 2 - скорость уменьшения мощности ауры
# Дамагеры
statblock_damager_mage_aura = [list(map(int, input().split())) for j in range(amount_damager_mage)]
statblock_damager_mage_aura = np.array(statblock_damager_mage_aura)
# Хилеры
statblock_healer_mage_aura = [list(map(int, input().split())) for j in range(amount_healer_mage)]
statblock_healer_mage_aura = np.array(statblock_healer_mage_aura)

# Статблок текущих хп и текущей ауры магов
statblock_real_damager_mage = np.array([healpoint_mage, 0] * amount_damager_mage)
statblock_real_healer_mage = np.hstack((np.zeros((amount_healer_mage, 1), dtype=int), statblock_healer_mage_aura[:, 1]))

# Позиция магов в виде векторов
position_damager_mage = np.zeros(amount_damager_mage, 2)
position_healer_mage = np.zeros(amount_healer_mage, 2)


# Действие магов - Атака и Лечение
def aura_online(i, k, current_aura, mage_arrive_safezone, max_aura, speed_up_aura, total_damage, total_heal,
                type_of_action):
    global statblock_real_damager_mage, statblock_real_healer_mage, healpoint_dragon
    #  Повышение мощности ауры магов
    if current_aura <= max_aura:
        current_aura += speed_up_aura
        if ((current_aura + speed_up_aura) >= max_aura) | (current_aura >= max_aura):
            current_aura = max_aura
            if type_of_action == 'Damage':
                total_damage += max_aura
            if type_of_action == 'Heal':
                total_heal += max_aura
            mage_arrive_safezone.delete(mage_arrive_safezone, i)
            k += 1
    # Нанесение урона и лечение магов
    if type_of_action == 'Damage':
        healpoint_dragon -= current_aura
        return [mage_arrive_safezone, k, current_aura, total_damage]
    if type_of_action == 'Heal':
        statblock_real_damager_mage += np.array([current_aura, 0] * amount_damager_mage)
        statblock_real_healer_mage += np.array([current_aura, 0] * amount_healer_mage)
        return [mage_arrive_safezone, k, current_aura, total_heal]


def aura_offline(finish_position, damage_dragon, current_hp, position_of_mage, current_aura, speed_down_aura):
    if len(finish_position) == 1:
        # Передвижение
        direct_vector = finish_position - position_of_mage  # Вектор направления мага
        k = (np.sqrt(direct_vector.dor(direct_vector))) / speed_of_mage  # Коэф. пропорциональности
        position_of_mage = direct_vector / k  # Передвижение
        # Урон по магу
        current_hp -= damage_dragon
        # Понижение мощности ауры магов
        if current_aura > 0:
            if (current_aura - speed_down_aura) < 0:
                current_aura = 0
            else:
                current_aura -= speed_down_aura
        return [current_hp, position_of_mage, current_aura]


# Событие - Атака "Огненный смерч"
def storm_attack():
    global healpoint_dragon, position_of_mage, statblock_real_damager_mage, statblock_real_healer_mage
    damage_dragon, time_attack = map(int, input().split())
    finish_position = np.array(input().split().astype(int))  # Точка безопасной зоны
    total_damage = 0  # Общий урон магов, имеющие полную ауру
    total_heal = 0  # Общий хил магов, имеющие полную ауру
    mage_damager_aura_not_full, mage_damager_not_in_safe_zone = np.arange(amount_damager_mage)
    mage_healer_aura_not_full, mage_healer_not_in_safe_zone = np.arange(amount_healer_mage)
    # /|\ 1 -ый Список, в котором хранятся индексы магов, аура которых не полная
    #  |  2 -ый Список, где лежат индексы магов вне сейф зоны
    while time_attack > 0:
        # Проверка "Маг с полной аурой? Если да - то запуск цикла, где проверка "Маг в сейф зоне?" Если да - то урон дракону/лечение магов. Если нет - передвижение и урон магам"
        counter = 0
        if mage_damager_aura_not_full | mage_healer_aura_not_full:
            amount_damager_in_safezone, amount_healer_in_safezone = 0
            # Итерация сразу по двум спискам - дамагеры и хилеры
            while counter < max(mage_damager_aura_not_full.size, mage_healer_aura_not_full.size):
                # Итерация по хилерам
                j = counter - amount_healer_in_safezone
                if j < mage_healer_aura_not_full.size:
                    i = mage_healer_aura_not_full[j]
                    max_aura, speed_up_aura, speed_down_aura = statblock_healer_mage_aura[i, 0], \
                                                               statblock_healer_mage_aura[i, 1], \
                                                               statblock_healer_mage_aura[i, 2]
                    # Если маг в сейф зоне, то удаление из списка индексов магов вне сейф зоны
                    if position_healer_mage[:, i] == finish_position:
                        mage_healer_not_in_safe_zone.delete(mage_healer_not_in_safe_zone, i)
                    # Если маг в сейф зоне, то усиление ауры и лечение магов, если нет - то урон по магам, передвижение, и снижение мощности ауры
                    if i not in mage_healer_not_in_safe_zone:
                        mage_healer_aura_not_full, amount_healer_in_safezone, statblock_real_healer_mage[
                            i, 1], total_heal = aura_online(i, amount_healer_in_safezone,
                                                            statblock_real_healer_mage[i, 1], mage_healer_aura_not_full,
                                                            max_aura, speed_up_aura, None, total_heal, "Heal").split()
                    else:
                        statblock_real_healer_mage[i, 0], position_healer_mage[i], statblock_real_healer_mage[
                            i, 1] = aura_offline(finish_position, damage_dragon, statblock_real_healer_mage[i, 0],
                                                 position_healer_mage[i], statblock_real_healer_mage[i, 1],
                                                 speed_down_aura)
                # Итерация по дамагерам
                j = counter - amount_damager_in_safezone
                if j < mage_damager_aura_not_full.size:
                    i = mage_damager_aura_not_full[j]
                    max_aura, speed_up_aura, speed_down_aura = statblock_damager_mage_aura[i, 0], \
                                                               statblock_damager_mage_aura[i, 1], \
                                                               statblock_damager_mage_aura[i, 2]
                    # Если маг в сейф зоне, то удаление из списка индексов магов вне сейф зоны
                    if position_damager_mage[:, i] == finish_position:
                        mage_damager_not_in_safe_zone.delete(mage_damager_not_in_safe_zone, i)
                    # Если маг в сейф зоне, то урон магов и усиление ауры, если нет - то урон по магам, передвижение, и снижение мощности ауры
                    if i not in mage_damager_not_in_safe_zone:
                        mage_damager_aura_not_full, amount_damager_in_safezone, statblock_real_healer_mage[
                            i, 1], total_damage = aura_online(i, amount_healer_in_safezone,
                                                              statblock_real_healer_mage[i, 1],
                                                              mage_healer_aura_not_full, max_aura,
                                                              speed_up_aura, total_damage, None, "Damage").split()
                    else:
                        statblock_real_damager_mage[i, 0], position_damager_mage[i], statblock_real_damager_mage[
                            i, 1] = aura_offline(finish_position, damage_dragon, statblock_real_damager_mage[i, 0],
                                                 position_damager_mage[i], statblock_real_damager_mage[i, 1],
                                                 speed_down_aura).split()

                counter += 1
        # Нанесение урона по дракону дамагеров с полной аурой
        healpoint_dragon -= total_damage

        # Лечение дамагеров теми, у кого полная аура
        statblock_real_damager_mage += np.array([total_heal, 0] * amount_damager_mage)
        statblock_real_damager_mage = np.clip(statblock_real_damager_mage, 0, healpoint_mage)

        # Лечение хилеров теми, у кого полная аура
        statblock_real_healer_mage += np.array([total_heal, 0] * amount_healer_mage)
        statblock_real_healer_mage = np.clip(statblock_real_healer_mage, 0, healpoint_mage)

        if 0 in statblock_real_healer_mage | 0 in statblock_real_damager_mage:
            print("You are not prepared")
            exit()

        if healpoint_dragon <= 0 & (not (mage_healer_not_in_safe_zone | mage_damager_not_in_safe_zone)) :
            print("No useful loot again")
            print(counter_of_attack)
            exit()
        time_attack -= 1


# Событие - Атака "Дыхание дракона"
def breath_attack():
    global healpoint_dragon, position_of_mage
    damage_dragon, time_attack = map(int, input().split())
    safe_positions = [list(map(int, input().split())) for j in range(amount_mage)]
    safe_positions = np.array(safe_positions)


# Событие - Атака "Удар хвостом"
def tail():
    print("You are not prepared")
    exit()


# Блок с вводом типа атаки
counter_of_attack = 0
for kill_the_mage in amount_attack_of_dragon:
    counter_of_attack += 1
    type_attack = input()
    if type_attack == "Tail": tail()
    if type_attack == "Storm": storm_attack()
    if type_attack == "Breath": breath_attack()
