import numpy as np

# Входные данные блока стистики
amount_attack_mage, amount_healer_mage, amount_attack_of_dragon = map(int, input().split())
amount_mage = amount_attack_mage+amount_healer_mage
healpoint_mage, speed_of_mage, healpoint_dragon = map(int, input().split())

# Статблок ауры магов: 0 - макс. мощность ауры, 1 - скорость роста мощности ауры, 2 - скорость уменьшения мощности ауры
statblock_aura = [[int (i) for i in input().split()] for j in range(amount_mage)]

# Статблок текущих хп и мощности ауры (текущие хп, мощность аура)
statblock_real_mage = []
for i in range((amount_mage)):
    if i < amount_mage:
        statblock_real_mage.append([healpoint_mage, 0])
    else:
        statblock_real_mage.append([healpoint_mage, statblock_aura[i][0]])

# Позиция магов (3 столбец (0 или 1) обозначает, находятся ли маги в безопасной зоне ( 0 - нет, 1 - да)
position_of_mage = [[0] * 3 for i in range(amount_mage)]

# Событие - Атака "Огненный смерч"
def storm_attack():
    damage, time_attack = map(int, input().split())
    safe_zone_x, safe_zone_y = map(int, input().split())
    while time_attack > 0:
        # Проверка "Маг в сейф зоне? Если да - то урон дракону/хилл магов. Если нет - передвижение и урон магам"
        for i in range(amount_mage):
            max_aura, speed_up_aura, speed_down_aura = statblock_aura[i][0], statblock_aura[i][1], statblock_aura[i][2]
            position_of_mage[i][2] = 0 # Обнуление условия "Маг в сейф зоне"
            if (position_of_mage[i][2] == 1) | ((position_of_mage[i][0] == safe_zone_x) & (position_of_mage[i][1] == safe_zone_y)):
                position_of_mage[i][2] = 1
                #  Повышение мощности ауры атак. магов
                if statblock_real_mage[i][1] < max_aura:
                    if (statblock_real_mage[i][1] + speed_up_aura) > max_aura:
                        statblock_real_mage[i][1] = max_aura
                    else:
                        statblock_real_mage[i][1]


            else:
                statblock_real_mage[i][0] -= damage


        time_attack -= 1



# Событие - Атака "Дыхание дракона"
def breath_attack():





while type_attack <> "Tail":
    if type_attack == "Storm": storm_attack()
    if type_attack == "Breath": breath_attack()
