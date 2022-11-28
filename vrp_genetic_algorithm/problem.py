import random


def generate_city_locations(iterations: int) -> list[list[int]]:
    # Random x,y koordináták generálása a városoknak
    routes = []
    # végigmegyünk minden iteráción
    for _ in range(iterations):
        # addig megyünk, amíg nem generálunk olyan város pozíciót, ami még nem volt
        while True:
            # új város koordináták generálása
            random_route = [random.randint(1, 100), random.randint(1, 100)]
            # nem lehet 1 koordinátán 2 város
            if random_route in routes:
                continue
            routes.append(random_route)
            break

    return routes


def get_all_city_distance(city_matrix: list[list[int]]) -> dict[tuple[int, int]]:  # TSP alapkód alapján
    # Megkapja a városokat, visszaadja a távolságmátrixot
    city_distance_matrix = {}

    for x in range(len(city_matrix)):
        for y in range(len(city_matrix)):
            city_distance_matrix[(x, y)] = get_manhattan_distance(city_matrix[x], city_matrix[y])

    return city_distance_matrix


def get_manhattan_distance(x: list[int], y: list[int]) -> int:  # TSP alapkód alapján
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def create_routes(car_count: int, city_distance_matrix: dict[tuple[int, int]], city_matrix: list[list[int]]) \
        -> list[list[int]]:
    # útvonalak generálása, az egymáshoz legközelebbi városok megkeresésével
    visited_cities = []  # már meglátogatott városok
    routes = [[] for _ in range(car_count)]  # autók száma hosszúságú lista létrehozása

    for i in range(car_count):
        routes[i].append(0)
    visited_cities.append(0)

    current_city = [0 for _ in range(car_count)]
    while len(city_matrix) != len(visited_cities):  # addig megyünk, amíg ki nem osztottunk minden várost 1-1 autóhoz
        for i in range(car_count):  # végigmegyünk minden autón
            if len(city_matrix) != len(visited_cities): # ellenőrizzük a kiosztott városok számát végtelen ciklus miatt
                position = get_nearest_city(city_distance_matrix, current_city[i], city_matrix,
                                            visited_cities)  # új város megkeresése
                routes[i].append(position)
                visited_cities.append(position)

    return routes


def get_nearest_city(city_distance_matrix: dict[tuple[int, int]], current_city: int, city_matrix: list[list[int]],
                     visited_cities) -> float:
    # adott városhoz legközelebbi, még ki nem osztott város megkeresése
    minimum_distance = float("inf")
    minimum_index = 0
    # végigmegyünk minden városon
    for i in range(len(city_matrix)):
        # nem lehet a jelenlegi pozíció
        if i == current_city:
            continue
        # nem lehet már kiosztva
        if i in visited_cities:
            continue
        # nem lehet a jelenlegi város messzebb, mint az eddigi legjobb
        if minimum_distance <= city_distance_matrix[i, current_city]:
            continue
        # kiválasztjuk új legjobb pozíciónak
        minimum_distance = city_distance_matrix[i, current_city]
        minimum_index = i

    return minimum_index
