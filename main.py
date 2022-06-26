# Входные данные блока стистики
amount_attack_mage, amount_healer_mage, amount_attack_of_dragon = map(int, input().split())
amount_mage = amount_attack_mage+amount_healer_mage
healpoint_mage, speed_of_mage, healpoint_dragon = map(int, input().split())

# Статблок ауры магов: 0 - макс. мощность ауры, 1 - скорость роста мощности ауры, 2 - скорость уменьшения мощности ауры
statblock_aura = [list(map(int, input().split())) for i in range((amount_mage))]

# Статблок текущих хп и мощности ауры (текущие хп, мощность аура)
statblock_real_hp_aura = []
for i in range((amount_mage)):
    if i < amount_mage:
        statblock_real_hp_aura.append([healpoint_mage, 0])
    else:
        statblock_real_hp_aura.append([healpoint_mage, statblock_aura[i][0]])

# Позиция магов (3 столбец (0 или 1) обозначает, находятся ли маги в безопасной зоне ( 0 - нет, 1 - да)
position_of_mage = [[0] * 3 for i in range((amount_mage))]

# Событие - Атака "Огненный смерч"
def storm_attack():
    damage, time_attack = int(input().split())
    safe_zone_x, safe_zone_y = int(input().split())
    while time_attack > 0:
        time_attack -= 1
        # Если маг находится вне безопасной зоны - ему наносится урон
        for i in range(amount_mage):
            if (position_of_mage[i][0] != safe_zone_x) | (position_of_mage[i][1] != safe_zone_y):
                statblock_real_hp_aura[i][0] -= damage

        #



# Событие - Атака "Дыхание дракона"
def breath_attack():





while type_attack <> "Tail":
    if type_attack = "Storm": storm_attack()
    if type_attack = "Breath": breath_attack()
