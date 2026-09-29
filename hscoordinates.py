import math

"""
Формула для расчёта расстояния между двумя точками на Земле с использованием Хаверсинуса выглядит следующим образом:
ACOS(COS(RADIANS(90 - Lat_1)) * COS(RADIANS(90 - Lat_2)) + SIN(RADIANS(90 - Lat_1)) * SIN(RADIANS(90 - Lat_2)) * COS(RADIANS(Lon_2 - Lon_1))) * R

Формула Хаверсинуса использует следующие переменные:
lat_1 — широта начальной точки;
lon_1 — долгота начальной точки;
lat_2 — широта конечной точки;
lon_2 — долгота конечной точки;
R — радиус Земли (обычно принимается равным 6371 км);
d — расстояние между двумя точками.

"""

def haversin(pos1, pos2):
    lat_1, lon_1 = pos1
    lat_2, lon_2 = pos2
    R = 6371
    cos_lat = math.cos(math.radians(90-lat_1)) * math.cos(math.radians(90 - lat_2))
    sin_lat = math.sin(math.radians(90-lat_1)) * math.sin(math.radians(90 - lat_2))
    cos_lon = math.cos(math.radians(lon_2 - lon_1))
    distance = math.acos(cos_lat + sin_lat * cos_lon) * R
    return distance