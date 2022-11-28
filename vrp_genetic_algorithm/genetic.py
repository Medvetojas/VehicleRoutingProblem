from copy import deepcopy
from typing import Tuple
import random


def begin_algorithm(initial_routes: list[list[int]], city_distance_matrix: dict[tuple[int, int]],
                    iterations: int, generations: int) -> Tuple[list[list[int]], int]:
    # a fő folyamat, a genetikus algoritmus
    best_routes = []  # egy generálás által túlélt generáció
    best_routes_total_length = 0  # a túlélt generáció hossza
    age_of_best_routes = 0  # a túlélt generáció életkora

    for i in range(len(initial_routes)):  # feltöltjük a változókat a kiindulási adatokkal
        best_routes.append(initial_routes[i])
        best_routes_total_length += fitness(city_distance_matrix, initial_routes[i])

    best_routes_previous_length = best_routes_total_length  # ...és a hosszát, hogy élettartamot számoljunk

    population = []  # egy generáláson belüli több generáció tömbje
    population_lengths = []  # 1-1 generáció hossza
    for _ in range(generations):  # feltöltjük az alap adatokkal
        population.append(best_routes)
        population_lengths.append(0)  # a hosszokat 0-ra állítjuk, mivel még nincsenek kiszámolva

    for _ in range(iterations):  # genetikus algoritmus ismétlése iterációszor (mutáció, rekombináció, majd túlélés)
        population, population_lengths, generation_order_in_population = genetic_algorithm(generations, population,
                                                                                           population_lengths,
                                                                                           best_routes, initial_routes,
                                                                                           city_distance_matrix)
        # genetikus algoritmus után generációk alapján túlélési valség számítása
        best_routes, best_routes_total_length = get_solution_from_survival_probability(
            population_lengths, generations, population, generation_order_in_population, best_routes,
            best_routes_total_length)  # túlélési esély alapján választunk új generáció alapot

        if best_routes_total_length < best_routes_previous_length:  # ha a túlélt generáció útvonalának hossza csökkent
            age_of_best_routes = 1
            best_routes_previous_length = best_routes_total_length
            print("\nA better all-time generation (solution) has been found!" +
                  "\nThe route is the following:", str(best_routes) +
                  "\nThe route's total length is", str(best_routes_total_length) + " units.\n")
        else:  # ha nem történt útvonalhosszbeli javulás
            age_of_best_routes += 1
            if age_of_best_routes > 350:
                print("\n----------------------------------------------------------------------------------------\n"
                      "The best solution did not get better for 350 iterations, therefore the algorithm stops."
                      "\n----------------------------------------------------------------------------------------\n")
                break

    for i in range(len(best_routes)):
        best_routes[i].append(0)  # ha akarjuk a végére a 0-át, ettől függetlenül számolunk a visszaúttal
    return best_routes, best_routes_total_length


def fitness(city_distance_matrix: dict[tuple[int, int]], route: list[int]) -> int:  # TSP alapkód alapján
    # Megkapja a távolságokat és a vizsgálandó útvonalat, visszaadja az útvonal hosszát, ezt minimalizáljuk
    distance = 0
    prev = route[0]  # Ahol utoljára voltunk, az az első hely

    for i in route:
        distance += city_distance_matrix[(prev, i)]
        prev = i
    distance += city_distance_matrix[(route[-1], route[0])]

    return distance


def genetic_algorithm(generations: int, population: list[list[list[int]]], population_lengths: list[int],
                      best_routes: list[list[int]], initial_routes: list[list[int]],
                      city_distance_matrix: dict[tuple[int, int]])\
        -> Tuple[list[list[list[int]]], list[int], list[int]]:  # genetikus algoritmus

    route_order_in_population = []  # a generációk sorrendje (később szükséges a növekvő sorrend alapján rendezésre)
    length = []  # a generációk ebben a tömbben tárolódnak el (rendezve)

    for i in range(generations):  # feltöltjük adatokkal a változókat
        population[i] = deepcopy(best_routes)  # ide kell a deepcopy, fú de utálom a Pythont
        population_lengths[i] = 0  # még nem számoltunk hosszt, így nullával töltjük fel mind
        route_order_in_population += [i]  # a generációk sorrendje
        length += [0]

    for i in range(generations):  # mutáció elvégzése
        population[i] = mutation(initial_routes, population[i])

    for i in range(generations - 1):  # keresztezés elvégzése
        population[i] = crossover(len(initial_routes), population[i], population[i + 1])
    population[-1] = crossover(len(initial_routes), population[-1], population[0])

    for i in range(generations):  # minden generáció hosszának kiszámítása
        for k in range(len(initial_routes)):
            population_lengths[i] += fitness(city_distance_matrix, population[i][k])
    # rendezés
    length, route_order_in_population = sort_array(population_lengths, route_order_in_population, generations)

    return population, population_lengths, route_order_in_population


def mutation(routes: list[list[int]], population: list[list[int]]) -> list[list[int]]:
    # TSP alapkód alapján bővítve VRP-re
    # Két random útvonal között megcserél egy-egy random várost
    if len(routes) <= 1:  # Ha TSP a feladat
        route1 = 0
        route2 = 0
    else:  # ha VRP a feladat
        route1 = random.randint(0, len(routes) - 1)  # egyik autó
        route2 = random.randint(0, len(routes) - 1)  # másik autó

    if len(routes[route1]) <= 2 or len(routes[route2]) <= 2:
        return population

    city1 = random.randint(1, len(routes[route1]) - 1)  # egyik város
    city2 = random.randint(1, len(routes[route2]) - 1)  # másik város

    population[route1][city1], population[route2][city2] = population[route2][city2], population[route1][city1]  # csere

    return population


def crossover(initial_routes_length: int, routes_1: list[list[int]], routes_2: list[list[int]]) -> list[list[int]]:  # rekombináció
    routes_1 = delete_depot_from_array(routes_1)  # paraméterként megadott 1. útvonalak
    routes_2 = delete_depot_from_array(routes_2)  # paraméterként megadott 2. útvonalak
    # ezek tartalmaznak 1-1 teljes megoldást, azaz több autót, több várost

    routes_2_size_counter = []  # 1-1 autó által látogatott városok száma. Fontos a későbbiekben a depó visszaadásához
    routes2_cities = []  # a routes_2 adatait tartalmazza, de 1 dimenziós vektorként, nem 2 dimenziós mátrixként
    # 2 dimenzióban nehéz a rekombináció, ezért alakítunk át

    for i in range(initial_routes_length):  # itt alakítunk mátrixból vektorrá
        routes_2_size_counter.append(0)
        for k in range(len(routes_2[i])):  # végigmegyünk a routes_2 minden elemén
            routes2_cities += [routes_2[i][k]]  # hozzáadjuk a vektorunkhoz a mátrix minden elemét sorban
            routes_2_size_counter[i] += 1  # az adott indexhez incrementálunk, így tudjuk hány város tartozik hozzá

    # random 2 pontot választunk a metszéshez
    if (int(initial_routes_length / 2)) == 0:  # ha TSP a feladat
        first_part = 0
    else:  # ha VRP a feladat
        first_part = random.randint(0, int(initial_routes_length / 2) - 1)
    second_part = random.randint(int(initial_routes_length / 2), int(initial_routes_length) - 1)

    pointer = 0  # a kivágott autók kezdőpontja az első dimenzióban
    for i in range(first_part):
        pointer += routes_2_size_counter[i]

    pointer_length = 0  # a kivágott autók "hossza" az első dimenzióban
    for i in range(second_part):
        pointer_length += routes_2_size_counter[i]
    pointer_length -= pointer  # ki kell vonni, hogy jó hosszúságban vágjunk ki

    intersection = get_intersection_vector(first_part, second_part, routes_1)  # a kivágott rész (1 dimenzióban)

    crossovered_array = get_crossovered_array(routes2_cities, first_part, second_part, intersection)
    # a már rekombinált adat 1 dimenzióban, később alakítjuk vissza 2 dimenzióra

    final_array = get_final_array(routes_2_size_counter, crossovered_array)  # vektor értékek visszaállítása mátrixsszá

    return final_array


def get_intersection_vector(first_part: int, second_part: int, routes_1: list[list[int]]) -> list[int]:
    # A metszés itt tárolódik, de 2 dimenzióban (mátrixként). Ezt itt átalakítjuk a függvényben 1 dimenzióra (vektorra).
    intersection_temp = routes_1[first_part:second_part]  # a kimetszett rész
    intersection_vector = []  # vektor
    for i in range(len(intersection_temp)):  # mátrix átalakítása vektorrá
        for k in range(len(intersection_temp[i])):
            intersection_vector += [intersection_temp[i][k]]
    # pl: [[1,3],[4,6]] -> [1,3,4,6]
    return intersection_vector


def get_crossovered_array(routes2_cities: list[list[int]], first_part: int, second_part: int, intersection: list[int]):
    # Egydimenzióban végrehajtja a keresztezést
    index = 0
    crossovered_array = []
    # beillesztjük az adott generációba a kivágott elemeket
    while len(crossovered_array) < len(routes2_cities):  # addig megyünk, amíg minden város ki nem lett újból osztva
        if first_part <= index < second_part:  # ha az index a first_p és second_p közt van, akkor a metszésben vagyunk
            for k in intersection:  # végigmegyünk a metszés minden elemén, és hozzáadjuk a tömbünkhöz
                crossovered_array.append(k)
            index = second_part  # kilépési feltétel állítása
        for k in range(len(routes2_cities)):  # végigmegyünk minden városon
            # megnézzük, hogy a vizsgált város benne van-e a kivágásban, vagy már bele lett-e rakva 1x az új tömbbe
            if routes2_cities[k] not in intersection and routes2_cities[k] not in crossovered_array:
                crossovered_array.append(routes2_cities[k])
                index += 1
                break
    # pl: [2,5,1,3,4,6] és [1,4,2,5,3,6] -> [4,2,1,3,5,6]
    return crossovered_array


def get_final_array(routes_2_size_counter: list[int], crossovered_array: list[int]) -> list[list[int]]:
    #  1 dimenziós értékek visszaállítása 2 dimenzióssá
    index = 0
    temp_array = []  # 1-1 autó által tartalmazott városok vektora
    final_array = []  # a temp_array segítségével jön létre, így minden indexe 1-1 autót tartalmaz.
    # Ez a változó tartalmazza a visszaalakított 2 dimenziós mátrixot az 1 dimenziós vektorból

    for i in range(len(routes_2_size_counter)):  # végigmegyünk az autók számán
        temp_array.append(0)  # visszarakjuk az első elemre a depót
        for k in range(routes_2_size_counter[i]):  # végigmegyünk az adott autó városszámán
            temp_array.append(crossovered_array[index])  # hozzáadjuk az ideiglenes változóhoz magát a várost
            index += 1
        final_array.append(temp_array)  # hozzáadjuk a mátrixhoz az autót (illetve a városokat, az útvonalat)
        temp_array = []  # ürítjük az ideiglenes változót a következő autó számára
    # pl: [2,5,1,3,4,6] -> [[0,2,5],[0,1,3],[0,4,6]]
    return final_array


def sort_array(length: list[int], order: list[int], generations: int):
    # növekvő sorrendbe rendezzük a távolság alapján (minél kisebb a táv, annál jobb)
    # két tömböt is rendezünk: magát a sorrendet tároló tömböt és a távolságokat tároló tömböt
    population_lengths = length.copy()
    population_order = order.copy()

    for i in range(generations - 1):
        for k in range(i + 1, generations):
            if population_lengths[i] > population_lengths[k]:
                temp_array = population_lengths[i]
                population_lengths[i] = population_lengths[k]
                population_lengths[k] = temp_array

                temp_array = population_order[i]
                population_order[i] = population_order[k]
                population_order[k] = temp_array

    return population_lengths, population_order


def get_solution_from_survival_probability(population_lengths: list[int], generations: int,
                                           population: list[list[list[int]]], generation_order_in_population: list[int],
                                           best_routes: list[list[int]], best_routes_total_length: int)\
        -> Tuple[list[list[int]], int]:  # túlélő generáció kiszámítása

    # population_lengths: jelenlegi populáció hosszai (az útvonalak hosszai amiket feldolgozunk)
    # generations: generációk száma
    # population: jelenlegi populáció (útvonalak amiket feldolgozunk)
    # generation_order_in_population: jelenlegi eredmény sorrendje
    # best_routes: jelenlegi legjobb útvonal
    # best_routes_total_length: jelenlegi legjobb útvonal hossza

    rand_num = random.random()  # túlélési esélyhez random szám
    survival_probability = 0.82  # konstans szám: 0 < survival_probability < 1
    ok = 0  # kilépési feltétel, ha van visszatérési értékünk
    counter = 0  # kilépési feltétel, a túlélt generáció indexe - egyben a Pn-edik eset

    # P1, P2, P3, Pn a rendezett generációk, a genetic() függvényben a legvégén rendeztük őket
    # ha kisebb a random szám -> túléli a generáció
    # ha nem kisebb, akkor kivonjuk belőle az esélyt és elvetjük

    while ok == 0 and counter < generations:  # túlélési esély számítása (feladat PDF-ben szereplő képlet alapján)
        if counter == 0:  # ha ez első generáció (külön kell kezelnünk az elsőt és az utolsót)
            if rand_num < survival_probability:
                ok = 1
                best_routes = population[generation_order_in_population[counter]]
                best_routes_total_length = population_lengths[generation_order_in_population[counter]]
                continue
            else:
                rand_num -= survival_probability
            counter += 1
        else:  # ha nem az első, de nem is az utolsó
            if rand_num < (pow(1 - survival_probability, counter) * survival_probability):
                ok = 1
                best_routes = population[generation_order_in_population[counter]]
                best_routes_total_length = population_lengths[generation_order_in_population[counter]]
                continue
            else:
                rand_num -= (pow(1 - survival_probability, counter) * survival_probability)
            counter += 1

    # ha ok == 0, akkor a legrosszabb eredmény élte túl a generálást
    if ok == 0:
        best_routes = population[generation_order_in_population[generations - 1]]
        best_routes_total_length = population_lengths[generations - 1]
        counter -= 1

    return best_routes, best_routes_total_length


def delete_depot_from_array(routes_with_depot: list[list[int]]) -> list[list[int]]:
    # kiszedjük a depót a feladatból
    # pl: [[0,2,5],[0,1,3],[0,4,6]] -> [[2,5],[1,3],[4,6]]
    route_without_depot = []
    for i in range(len(routes_with_depot)):
        temp = []
        for k in range(len(routes_with_depot[i])):
            if routes_with_depot[i][k] != 0:
                temp.append(routes_with_depot[i][k])
        route_without_depot.append(temp)
    return route_without_depot
