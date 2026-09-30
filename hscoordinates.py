import math

"""
Формула для расчёта расстояния между двумя точками на Земле с использованием Хаверсинуса выглядит следующим образом:
ACOS(COS(RADIANS(90 - Lat_1)) * COS(RADIANS(90 - Lat_2)) + SIN(RADIANS(90 - Lat_1)) * SIN(RADIANS(90 - Lat_2)) * COS(RADIANS(Lon_2 - Lon_1))) * R

Формула Хаверсинуса использует следующие переменные:
lat_1 — широта начальной точки Latitude ;
lon_1 — долгота начальной точки longitude;
lat_2 — широта конечной точки Latitude;
lon_2 — долгота конечной точки longitude;
R — радиус Земли (обычно принимается равным 6371 км);
wiki:
• Экваториальный радиус: 6 378,1 км (расстояние от центра до экватора).
• Полярный радиус: 6 356,8 км (расстояние от центра до полюсов).

d — расстояние между двумя точками.

"""

#Функция-Деаоратор вывода дистанции в км. и м.
def hspresentation(hs):
    # Внутренная фукнция-обертка, которая принимает любые аргументы
    def wrapper(*args, **kwargs):
        value = hs(*args, **kwargs)
        km = int(value)
        m = str(round(value % km,3))[2:]
        return f'расстояние между точками {km} км. и {m} м.'
    return wrapper

@hspresentation
def haversin(pos1, pos2):
    lat_1, lon_1 = pos1
    lat_2, lon_2 = pos2
    R = 6371
    cos_lat = math.cos(math.radians(90-lat_1)) * math.cos(math.radians(90 - lat_2))
    sin_lat = math.sin(math.radians(90-lat_1)) * math.sin(math.radians(90 - lat_2))
    cos_lon = math.cos(math.radians(lon_2 - lon_1))
    distance = math.acos(cos_lat + sin_lat * cos_lon) * R
    return round(distance,5)

# Функционал самотестирования
if __name__ == '__main__':
    moscow = (55.751667, 37.617778)
    spb = (59.938784, 30.314997)
    newyork = (40.714627, -74.002863)

    print(haversin(moscow,spb))
    print(haversin(spb, moscow))
    print(haversin(newyork,moscow))
    print(haversin(newyork,spb))