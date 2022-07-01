import math
import numpy as np

# Входные данные блока стистики
amount_damager_mage, amount_healer_mage, amount_attack_of_dragon = map(int, input().split())
print()
# amount_damager_mage, amount_healer_mage, amount_attack_of_dragon = 1, 1, 2
amount_mage = amount_damager_mage + amount_healer_mage

healpoint_mage, speed_of_mage, healpoint_dragon = map(int, input().split())
print()
# healpoint_mage, speed_of_mage, healpoint_dragon = 1, 5, 10
# Статблок ауры магов.
# Столбцы: 0 - макс. мощность ауры, 1 - скорость роста мощности ауры, 2 - скорость уменьшения мощности ауры
# Дамагеры
statblock_damager_mage_aura = [list(map(int, input().split())) for i in range(amount_damager_mage)]
print()
# statblock_damager_mage_aura = [[1,3,2]]
statblock_damager_mage_aura = np.array(statblock_damager_mage_aura)
# print(statblock_damager_mage_aura)
# Хилеры
statblock_healer_mage_aura = [list(map(int, input().split())) for j in range(amount_healer_mage)]
print()
# statblock_healer_mage_aura = [[1,1,1]]
statblock_healer_mage_aura = np.array(statblock_healer_mage_aura)
# print(statblock_healer_mage_aura)
# Статблок текущих хп и текущей ауры магов
statblock_real_damager_mage = np.array([[healpoint_mage, 0] * amount_damager_mage])
statblock_real_healer_mage = np.hstack((np.array([[healpoint_mage] * amount_healer_mage], dtype=int), statblock_healer_mage_aura[:, 1].reshape(1, amount_healer_mage)))
# print(statblock_real_damager_mage)
# print(statblock_real_healer_mage)

# Позиция магов в виде векторов
position_damager_mage = np.zeros((amount_damager_mage, 2))
position_healer_mage = np.zeros((amount_healer_mage, 2))


# Действие магов - Атака и Лечение
def aura_online(i, k, current_aura, mage_not_full_aura, max_aura, speed_up_aura, total_damage, total_heal,
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
            mage_not_full_aura = np.delete(mage_not_full_aura, i)
            k += 1
    # Нанесение урона и лечение магов
    if type_of_action == 'Damage':
        return [mage_not_full_aura, k, current_aura, total_damage]
    if type_of_action == 'Heal':
        return [mage_not_full_aura, k, current_aura, total_heal]


# Действие магов - Передвижение
def aura_offline(finish_position, damage_dragon, current_hp, position_of_mage, current_aura, speed_down_aura):
    # Передвижение
    direct_vector = finish_position - position_of_mage  # Вектор направления мага
    k = (np.sqrt(direct_vector.dot(direct_vector))) / speed_of_mage  # Коэф. пропорциональности
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
    global healpoint_dragon, position_damager_mage, position_healer_mage, statblock_real_damager_mage, statblock_real_healer_mage
    damage_dragon, time_attack = map(int, input().split())
    time_attack -= 1
    print()
    finish_position = np.array(list(map(int, input().split())))  # Точка безопасной зоны
    # finish_position = np.array([0, 0])
    print()
    total_damage = 0  # Общий урон магов, имеющие полную ауру
    total_heal = 0  # Общий хил магов, имеющие полную ауру
    mage_damager_aura_not_full, mage_damager_not_in_safe_zone = np.arange(amount_damager_mage), np.arange(amount_damager_mage)
    mage_healer_aura_not_full, mage_healer_not_in_safe_zone = np.arange(amount_healer_mage), np.arange(amount_healer_mage)
    # /|\ 1 -ый Список, в котором хранятся индексы магов, аура которых не полная
    #  |  2 -ый Список, где лежат индексы магов вне сейф зоны
    while time_attack > 0:
        # Проверка "Маг с полной аурой? Если да - то запуск цикла с проверка "Маг в сейф зоне?"
        # Если да - то урон дракону/лечение магов. Если нет - передвижение и урон магам"
        counter = 0
        if (mage_damager_aura_not_full.size > 0) | (mage_healer_aura_not_full.size > 0):
            amount_damager_in_safezone, amount_healer_in_safezone = 0, 0
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
                    if np.all(position_healer_mage[i] == finish_position):
                        mage_healer_not_in_safe_zone = np.delete(mage_healer_not_in_safe_zone, i)
                    # Если маг в сейф зоне, то усиление ауры и лечение магов, если нет - то урон по магам, передвижение, и снижение мощности ауры
                    if i not in mage_healer_not_in_safe_zone:
                        mage_healer_aura_not_full, amount_healer_in_safezone, statblock_real_healer_mage[
                            i, 1], total_heal = aura_online(i, amount_healer_in_safezone,
                                                            statblock_real_healer_mage[i, 1], mage_healer_aura_not_full,
                                                            max_aura, speed_up_aura, total_damage, total_heal, "Heal")
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
                    if np.all(position_damager_mage[i] == finish_position):
                        mage_damager_not_in_safe_zone = np.delete(mage_damager_not_in_safe_zone, i)
                    # Если маг в сейф зоне, то урон магов и усиление ауры, если нет - то урон по магам, передвижение, и снижение мощности ауры
                    if i not in mage_damager_not_in_safe_zone:
                        mage_damager_aura_not_full, amount_damager_in_safezone, statblock_real_healer_mage[
                            i, 1], total_damage = aura_online(i, amount_healer_in_safezone,
                                                              statblock_real_healer_mage[i, 1],
                                                              mage_damager_aura_not_full, max_aura,
                                                              speed_up_aura, total_damage, total_heal, "Damage")
                    else:
                        statblock_real_damager_mage[i, 0], position_damager_mage[i], statblock_real_damager_mage[
                            i, 1] = aura_offline(finish_position, damage_dragon, statblock_real_damager_mage[i, 0],
                                                 position_damager_mage[i], statblock_real_damager_mage[i, 1],
                                                 speed_down_aura)

                counter += 1
        # Нанесение урона по дракону дамагеров с полной аурой
        healpoint_dragon -= total_damage

        # Лечение дамагеров теми, у кого полная аура
        statblock_real_damager_mage += np.array([total_heal, 0] * amount_damager_mage)
        statblock_real_damager_mage = np.clip(statblock_real_damager_mage, 0, healpoint_mage)

        # Лечение хилеров теми, у кого полная аура
        statblock_real_healer_mage += np.array([total_heal, 0] * amount_healer_mage)
        statblock_real_healer_mage = np.clip(statblock_real_healer_mage, 0, healpoint_mage)

        if (0 in statblock_real_healer_mage[:, 0] ) | (0 in statblock_real_damager_mage[:, 0]):
            print("You are not prepared")
            exit()

        if healpoint_dragon <= 0 & ((mage_damager_not_in_safe_zone.size == 0) & (mage_damager_not_in_safe_zone.size == 0)):
            print("No useful loot again")
            print(counter_of_attack)
            exit()
        time_attack -= 1


# Событие - Атака "Дыхание дракона"
def breath_attack():
    global healpoint_dragon, position_damager_mage, position_healer_mage, statblock_real_damager_mage, statblock_real_healer_mage
    damage_dragon, time_attack = map(int, input().split())
    time_attack =- 1
    print()
    safe_positions = [list(map(int, input().split())) for j in range(amount_mage)]
    print()
    safe_positions = np.array(safe_positions)
    total_damage = 0  # Общий урон магов, имеющие полную ауру
    total_heal = 0  # Общий хил магов, имеющие полную ауру
    mage_damager_aura_not_full, mage_damager_not_in_safe_zone = np.arange(amount_damager_mage), np.arange(amount_damager_mage)
    mage_healer_aura_not_full, mage_healer_not_in_safe_zone = np.arange(amount_healer_mage), np.arange(amount_healer_mage)
    # /|\ 1 -ый Список, в котором хранятся индексы магов, аура которых не полная
    #  |  2 -ый Список, где лежат индексы магов вне сейф зоны

    # Если это послдняя атака перед Tail - то проигрыш.
    if (counter_of_attack + 1) == amount_attack_of_dragon:
        print("You are not prepared")
        exit()

    maximum_heal = sum(statblock_healer_mage_aura[:, 0])
    # Условие, что если даже с максимальным хиллом чел не выживает - то выход из программы.
    for i in mage_damager_not_in_safe_zone:
        if 0 in (statblock_real_damager_mage[i, 0] + maximum_heal - damage_dragon):
            print("You are not prepared")
            exit()
    for i in mage_healer_not_in_safe_zone:
        if 0 in (statblock_real_healer_mage[i, 0] + maximum_heal - damage_dragon):
            print("You are not prepared")
            exit()

    booked_safe_position = []
    maximum_moves = int(math.ceil(2000 * math.sqrt(2) / speed_of_mage))
    # Алгоритм для распределения магов по точкам
    for number_of_moves in range(1, maximum_moves):
        # Алгоритм заключается в следующем:
        # Формируем массив точек, ближайшие к магу. Если до точки может добраться только один маг, то отдаём ему
        # Если одна точка на два или более мага, то приоритеты ниже:
        #   1. Заполняем самыми раненными.
        #       2. Заполняем самыми сильными хилерами.

        amount_mage_not_in_safe_zone = []
        amount_mage_not_in_safe_zone.extend(mage_healer_not_in_safe_zone)
        amount_mage_not_in_safe_zone.extend(mage_damager_not_in_safe_zone)
        amount_mage_not_in_safe_zone = np.array(amount_mage_not_in_safe_zone)
        amount_mage_not_in_safe_zone.reshape(1, len(amount_mage_not_in_safe_zone))
        amount_mage_not_in_safe_zone.tolist()
        temp_list_positions = amount_mage_not_in_safe_zone.copy()

        # Список тех, кто может добежать до определённой точки в number_moves - ходов.
        for i in temp_list_positions:
            for safe_position in safe_positions:
                if i < amount_damager_mage:
                    direct_vector = safe_position - position_damager_mage[i]  # Вектор направления маг
                    k = (np.sqrt(direct_vector.dot(direct_vector))) / speed_of_mage  # Коэф. пропорциональности
                    if k <= number_of_moves:
                        temp_list_positions[i].append(safe_position)
                else:
                    direct_vector = safe_position - position_healer_mage[i]  # Вектор направления маг
                    k = (np.sqrt(direct_vector.dor(direct_vector))) / speed_of_mage  # Коэф. пропорциональности
                    if k <= number_of_moves:
                        temp_list_positions[i].append(safe_position)

        # Раздаём точки магам
        def distribute_points(i, recursive_boolean):
            nonlocal safe_positions
            number_not_in_safe = len(temp_list_positions)
            while i < number_not_in_safe:
                try:
                    current_mage = temp_list_positions[i][1:]
                except IndexError:
                    i += 1
                    continue

                # Если для данного мага имеется точка, до которой не добегают другие, то он её бронирует
                exitFlag = False
                for k in current_mage:
                    if temp_list_positions.count(k) == 1:
                        # Удаление из исходного списка этой точки
                        for temp in range(safe_positions.size):
                            if safe_positions[temp].all == k:
                                safe_positions = np.delete(safe_positions, temp, axis=0)
                                booked_safe_position.append([temp_list_positions[i][:1], k])
                                temp_list_positions.pop(i)
                                for j in range(temp_list_positions.count(k)):
                                    temp_list_positions.remove(k)
                                break
                        exitFlag = True
                        break
                if exitFlag:
                    if recursive_boolean:
                        return True
                    i += 1
                    continue

                # Расставляем приоритеты
                for k in current_mage:
                    for row in temp_list_positions:
                        if row.count(k) > 0:
                            if temp_list_positions[row, 0] != temp_list_positions[i, 0]:
                                # Вызов рекурсии. Если другой маг с той же точкой, смог освободить эту точку, то занимаем
                                if distribute_points(temp_list_positions[row, 0], True):
                                    for temp in range(safe_positions.size):
                                        if safe_positions[temp].all == k:
                                            safe_positions = np.delete(safe_positions, temp, axis=0)
                                            booked_safe_position.append([temp_list_positions[i][:1], k])
                                            temp_list_positions.pop(i)
                                            for j in range(temp_list_positions.count(k)):
                                                temp_list_positions.remove(k)
                                            break
                                    exitFlag = True

                                # Если нет, то действуем в порядке приоритетов: хп < damage_dragon, healer > damager, healer max.
                                else:
                                    mage_one = temp_list_positions[i, 0]
                                    mage_two = temp_list_positions[row, 0]

                                    # Записываем текущие хп магов
                                    if mage_one < amount_damager_mage:
                                        hp_mage_one = statblock_real_damager_mage[mage_one, 0]
                                    else:
                                        hp_mage_one = statblock_real_healer_mage[mage_one, 0]
                                    if mage_two < amount_damager_mage:
                                        hp_mage_two = statblock_real_damager_mage[mage_two, 0]
                                    else:
                                        hp_mage_two = statblock_real_healer_mage[mage_two, 0]
                                    # Сравнение хп (выживет ли после атаки дракона)
                                    if hp_mage_two - damage_dragon > 0:
                                        if hp_mage_one - damage_dragon <= 0:
                                            for temp in range(safe_positions.size):
                                                if safe_positions[temp].all == k:
                                                    safe_positions = np.delete(safe_positions, temp, axis=0)
                                                    booked_safe_position.append([temp_list_positions[i][:1], k])
                                                    temp_list_positions.pop(i)
                                                    for j in range(temp_list_positions.count(k)):
                                                        temp_list_positions.remove(k)
                                                    break
                                            exitFlag = True
                                        else:
                                            # Отдаём приоритет на хилеров
                                            # Если проверяемый маг хиллер, а другой дамагер
                                            if (mage_two < amount_damager_mage) & (mage_one >= amount_damager_mage):
                                                for temp in range(safe_positions.size):
                                                    if safe_positions[temp].all == k:
                                                        safe_positions = np.delete(safe_positions, temp, axis=0)
                                                        booked_safe_position.append([temp_list_positions[i][:1], k])
                                                        temp_list_positions.pop(i)
                                                        for j in range(temp_list_positions.count(k)):
                                                            temp_list_positions.remove(k)
                                                        break
                                                exitFlag = True
                                            # Если оба мага хиллеры
                                            elif (mage_two >= amount_damager_mage) & (mage_one >= amount_damager_mage):
                                                # Отдаём приоритет на самый сильный хилл по метрике: итоговый хилл с учётом увеличения ауры за 1 секунду
                                                heal_mage_one = statblock_real_healer_mage[mage_one, 1] + \
                                                                statblock_healer_mage_aura[mage_one, 1]
                                                if heal_mage_one > statblock_healer_mage_aura[mage_one, 0]:
                                                    heal_mage_one = statblock_healer_mage_aura[mage_one, 0]
                                                heal_mage_two = statblock_real_healer_mage[mage_two, 1] + \
                                                                statblock_healer_mage_aura[mage_two, 2]
                                                if heal_mage_two > statblock_healer_mage_aura[mage_two, 0]:
                                                    heal_mage_two = statblock_healer_mage_aura[mage_two, 0]

                                                # Сравниваем
                                                # Если первый маг сильнее по хиллу
                                                if heal_mage_one >= heal_mage_two:
                                                    for temp in range(safe_positions.size):
                                                        if safe_positions[temp].all == k:
                                                            safe_positions = np.delete(safe_positions, temp, axis=0)
                                                            booked_safe_position.append([temp_list_positions[i][:1], k])
                                                            temp_list_positions.pop(i)
                                                            for j in range(temp_list_positions.count(k)):
                                                                temp_list_positions.remove(k)
                                                            break
                                                    exitFlag = True
                                                # Иначе, если проверяемый маг слабее по хиллу, то ищем следующую точку
                                                else:
                                                    continue
                                            # Если проверяемый маг дамагер, а другой хиллер или  оба дамагера, то ищем дальше
                                            else:
                                                continue
                                                # Если второй маг не выживает по хп, то ищем следующую точку
                                    else:
                                        continue

                                if exitFlag:
                                    if recursive_boolean:
                                        return True

                i += 1

        i = 0
        while temp_list_positions:
            distribute_points(i, False)

    safe_positions = np.array(booked_safe_position)
    # Ежесекундные ходы
    while time_attack > 0:
        # Проверка "Маг с полной аурой? Если да - то запуск цикла с проверка "Маг в сейф зоне?"
        # Если да - то урон дракону/лечение магов. Если нет - передвижение и урон магам"
        counter = 0
        if (mage_damager_aura_not_full.size > 0) | (mage_healer_aura_not_full.size > 0):
            amount_damager_in_safezone, amount_healer_in_safezone = 0, 0
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
                    if np.all(position_healer_mage[i] == safe_positions[i]):
                        mage_healer_not_in_safe_zone = np.delete(mage_healer_not_in_safe_zone, i)
                    # Если маг в сейф зоне, то усиление ауры и лечение магов, если нет - то урон по магам, передвижение, и снижение мощности ауры
                    if i not in mage_healer_not_in_safe_zone:
                        mage_healer_aura_not_full, amount_healer_in_safezone, statblock_real_healer_mage[
                            i, 1], total_heal = aura_online(i, amount_healer_in_safezone,
                                                            statblock_real_healer_mage[i, 1], mage_healer_aura_not_full,
                                                            max_aura, speed_up_aura, total_damage, total_heal, "Heal")
                    else:
                        statblock_real_healer_mage[i, 0], position_healer_mage[i], statblock_real_healer_mage[
                            i, 1] = aura_offline(safe_positions[i], damage_dragon, statblock_real_healer_mage[i, 0],
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
                    if np.all(position_damager_mage[i] == safe_positions[i]):
                        mage_damager_not_in_safe_zone = np.delete(mage_damager_not_in_safe_zone, i)
                    # Если маг в сейф зоне, то урон магов и усиление ауры, если нет - то урон по магам, передвижение, и снижение мощности ауры
                    if i not in mage_damager_not_in_safe_zone:
                        mage_damager_aura_not_full, amount_damager_in_safezone, statblock_real_healer_mage[
                            i, 1], total_damage = aura_online(i, amount_healer_in_safezone,
                                                              statblock_real_healer_mage[i, 1],
                                                              mage_damager_aura_not_full, max_aura,
                                                              speed_up_aura, total_damage, total_heal, "Damage")
                    else:
                        statblock_real_damager_mage[i, 0], position_damager_mage[i], statblock_real_damager_mage[
                            i, 1] = aura_offline(safe_positions[i], damage_dragon, statblock_real_damager_mage[i, 0],
                                                 position_damager_mage[i], statblock_real_damager_mage[i, 1],
                                                 speed_down_aura)

                counter += 1
        # Нанесение урона по дракону дамагеров с полной аурой
        healpoint_dragon -= total_damage

        # Лечение дамагеров теми, у кого полная аура
        statblock_real_damager_mage += np.array([total_heal, 0] * amount_damager_mage)
        statblock_real_damager_mage = np.clip(statblock_real_damager_mage, 0, healpoint_mage)

        # Лечение хилеров теми, у кого полная аура
        statblock_real_healer_mage += np.array([total_heal, 0] * amount_healer_mage)
        statblock_real_healer_mage = np.clip(statblock_real_healer_mage, 0, healpoint_mage)

        if (0 in statblock_real_healer_mage[:, 0]) | (0 in statblock_real_damager_mage[:, 0]):
            print("You are not prepared")
            exit()

        if healpoint_dragon <= 0 & (
                (mage_damager_not_in_safe_zone.size == 0) & (mage_damager_not_in_safe_zone.size == 0)):
            print("No useful loot again")
            print(counter_of_attack)
            exit()
        time_attack -= 1


# Событие - Атака "Удар хвостом"
def tail():
    print("You are not prepared")
    exit()


# Блок с вводом типа атаки
counter_of_attack = 0
for kill_the_mage in range(amount_attack_of_dragon):
    counter_of_attack += 1
    type_attack = input()
    print()
    if type_attack == "Tail":
        tail()
    if type_attack == "Storm":
        storm_attack()
    if type_attack == "Breath":
        breath_attack()
