from copy import deepcopy
from typing import Tuple
import random


def genetic_algorithm(initial_routes: list[list[int]], city_distance_matrix: dict[tuple[int, int]],
                      iterations: int, generations: int) -> Tuple[list[list[int]], int]:
    # a fő folyamat, a genetikus algoritmus
    population = []  # egy generálás által túlélt generáció
    best_solution_total_length = 0  # a túlélt generáció hossza
    age_of_best_routes = 0  # a túlélt generáció életkora

    for i in range(len(initial_routes)):  # feltöltjük a változókat a kiindulási adatokkal
        population.append(initial_routes[i])
        best_solution_total_length += fitness(city_distance_matrix, initial_routes[i])

    best_solution = population
    population_previous_length = best_solution_total_length  # kezdetben megkapja a generált útvonal hosszát

    all_routes = []  # egy generáláson belüli több generáció tömbje
    all_routes_lengths = []  # 1-1 generáció hossza
    for _ in range(generations):  # feltöltjük az alap adatokkal
        all_routes.append(population)
        all_routes_lengths.append(0)  # a hosszokat 0-ra állítjuk, mivel még nincsenek kiszámolva

    for _ in range(iterations):  # genetikus algoritmus ismétlése iterációszor (mutáció, rekombináció, majd túlélés)
        all_routes, order_of_generations, all_routes_lengths = genetic(all_routes_lengths, generations,
                                                                       all_routes, population,
                                                                       initial_routes, city_distance_matrix)
        # genetikus algoritmus után generációk alapján túlélési valség számítása
        population, best_solution, best_solution_total_length = get_route_from_survival_probability(
            all_routes_lengths, generations, all_routes, order_of_generations, population, best_solution_total_length,
            best_solution)

        if best_solution_total_length < population_previous_length:  # ha a túlélt generáció útvonalának hossza csökkent
            age_of_best_routes = 1
            population_previous_length = best_solution_total_length
        else:  # ha nem történt útvonalhosszbeli javulás
            age_of_best_routes += 1
            if age_of_best_routes > 350:
                print("The best solution did not get better for 350 iterations, therefore the algorithm stops.")
                break

        # túlélési esély alapján választunk új generáció alapot

    for i in range(len(best_solution)):
        best_solution[i].append(0)  # ha akarjuk a végére a 0-át, ettől függetlenül számolunk a visszaúttal
    return best_solution, best_solution_total_length


def fitness(city_distance_matrix: dict[tuple[int, int]], route: list[int]) -> int:  # TSP alapkód alapján
    # Megkapja a távolságokat és a vizsgálandó útvonalat, visszaadja az útvonal hosszát, ezt minimalizáljuk
    distance = 0
    prev = route[0]  # Ahol utoljára voltunk, az az első hely

    for i in route:
        distance += city_distance_matrix[(prev, i)]
        prev = i
    distance += city_distance_matrix[(route[-1], route[0])]

    return distance


def genetic(all_routes_lengths: list[int], generations: int, all_routes: list[list[list[int]]],
            population: list[list[int]], initial_routes: list[list[int]], city_distance_matrix: dict[tuple[int, int]]) \
        -> Tuple[list[list[list[int]]], list[int], list[int]]:  # genetikus algoritmus

    # route_current: a generációk ebben a tömbben tárolódnak el
    # route_current_length: a generációk hosszai
    # all_routes: ???
    order_of_generations = []  # a generációk sorrendje (később szükséges a növekvő sorrend alapján rendezésre)
    length = []  # a generációk ebben a tömbben tárolódnak el (rendezve)

    for i in range(generations):  # feltöltjük adatokkal a változókat
        all_routes[i] = deepcopy(population)  # ide kell a deepcopy!
        all_routes_lengths[i] = 0
        order_of_generations += [i]
        length += [0]

    for i in range(generations):  # mutáció elvégzése
        all_routes[i] = mutation(initial_routes, all_routes[i])

    for i in range(generations - 1):  # keresztezés elvégzése
        all_routes[i] = crossover(len(initial_routes), all_routes[i], all_routes[i + 1])
    all_routes[-1] = crossover(len(initial_routes), all_routes[-1], all_routes[0])

    for i in range(generations):  # minden generáció hosszának kiszámítása
        for k in range(len(initial_routes)):
            all_routes_lengths[i] += fitness(city_distance_matrix, all_routes[i][k])
    # rendezés
    length, order_of_generations = sort_array(all_routes_lengths, order_of_generations, generations)

    return all_routes, order_of_generations, all_routes_lengths


def mutation(route: list[list[int]], route_current: list[list[int]])\
        -> list[list[int]]:  # TSP alapkód alapján bővítve VRP-re

    if len(route) <= 1:  # Ha TSP a feladat
        x = 0
        y = 0
    else:  # ha VRP a feladat
        x = random.randint(0, len(route) - 1)  # egyik autó
        y = random.randint(0, len(route) - 1)  # másik autó

    if len(route[x]) <= 2 or len(route[y]) <= 2:
        return route_current

    a = random.randint(1, len(route[x]) - 1)  # egyik város
    b = random.randint(1, len(route[y]) - 1)  # másik város

    route_current[x][a], route_current[y][b] = route_current[y][b], route_current[x][a]  # csere

    return route_current


def crossover(route: int, routes1: list[list[int]], routes2: list[list[int]]) -> list[list[int]]:  # rekombináció
    routes1 = delete_depo_from_array(routes1)  # paraméterként megadott 1. útvonal
    routes2 = delete_depo_from_array(routes2)  # paraméterként megadott 2. útvonal
    # ezek tartalmaznak 1-1 teljes megoldást, azaz több autót, több várost

    route_sizes = []  # 1-1 autó által látogatott városok száma. Fontos a későbbiekben a depó visszaadásához
    route_all = []  # a route2 adatait tartalmazza, de 1 dimenziós vektorként, nem 2 dimenziós mátrixként
    # 2 dimenzióban nehéz a rekombináció, ezért alakítunk át

    for i in range(route):  # itt alakítunk át
        route_sizes.append(0)
        for k in range(len(routes2[i])):  # végigmegyünk a route2 minden elemén
            route_all += [routes2[i][k]]  # hozzáadjuk a vektorunkhoz a mátrix minden elemét sorban
            route_sizes[i] += 1  # az adott indexhez incrementálunk, így tudjuk hány város tartozik hozzá

    # random 2 pontot választunk a metszéshez
    if (int(route / 2)) == 0:  # ha TSP a feladat
        first_part = 0
    else:  # ha VRP a feladat
        first_part = random.randint(0, int(route / 2) - 1)
    second_part = random.randint(int(route / 2), int(route) - 1)

    pointer = 0  # a kivágott elemek kezdőpontja az első dimenzióban
    for i in range(first_part):
        pointer += route_sizes[i]

    pointer_length = 0  # a kivágott elemek hossza az első dimenzióban
    for i in range(second_part):
        pointer_length += route_sizes[i]
    pointer_length -= pointer

    intersection = get_intersection_vector(first_part, second_part, routes1)  # a kivágott rész tárolása 1 dimenzióban

    crossovered_array = get_crossovered_array(route_all, first_part, second_part, intersection)
    # a már rekombinált adat 1 dimenzióban, később alakítjuk vissza 2 dimenzióra

    final_array = get_final_array(route_sizes, crossovered_array)  # 1 dimenziós értékek visszaállítása 2 dimenzióssá

    return final_array


def get_intersection_vector(first_part: int, second_part: int, route: list[list[int]]) -> list[int]:
    # a metszés itt tárolódik, de 2 dimenzióban (mátrixként). Ezt itt átalakítjuk a függvényben 1 dimenzióra (vektorra).
    intersection_temp = route[first_part:second_part]
    intersection_vector = []  # vektor
    for i in range(len(intersection_temp)):  # mátrix átalakítása vektorrá
        for k in range(len(intersection_temp[i])):
            intersection_vector += [intersection_temp[i][k]]
    # pl: [[1,3],[4,6]] -> [1,3,4,6]
    return intersection_vector


def get_crossovered_array(route: list[list[int]], first_part: int, second_part: int, intersection: list[int]):
    #  Egydimenzióban végrehajtja a keresztezést
    index = 0
    crossovered_array = []
    # beillesztjük az adott generációba a kivágott elemeket
    while len(crossovered_array) < len(route):  # addig megyünk, amíg minden város ki nem lett újból osztva
        if first_part <= index < second_part:  # ha elértük a metszés pontját, akkor beleillesztjük
            for k in intersection:  # végigmegyünk a metszés minden elemén, és hozzáadjuk a tömbünkhöz
                crossovered_array.append(k)
            index = second_part  # kilépési feltétel állítása
        for k in range(len(route)):  # végigmegyünk minden városon
            # megnézzük, hogy a vizsgált város benne van-e a kivágásban, vagy már bele lett-e rakva 1x az új tömbbe
            if route[k] not in intersection and route[k] not in crossovered_array:
                crossovered_array.append(route[k])
                index += 1
                break
    # pl: [2,5,1,3,4,6] és [1,4,2,5,3,6] -> [4,2,1,3,5,6]
    return crossovered_array


def get_final_array(route_sizes: list[int], crossovered_array: list[int]) -> list[list[int]]:
    #  1 dimenziós értékek visszaállítása 2 dimenzióssá
    index = 0
    # vektor -> mátrix depóval
    temp_array = []  # 1-1 autó által tartalmazott városok vektora
    final_array = []  # a temp_array segítségével jön létre, így minden indexe 1-1 autót tartalmaz. Ez a változó tartalmazza a visszaalakított 2 dimenziós mátrixot az 1 dimenziós vektorból
    for i in range(len(route_sizes)):  # végigmegyünk az autók számán
        temp_array.append(0)  # visszarakjuk az első elemre a depót
        for k in range(route_sizes[i]):  # végigmegyünk az adott autó városszámán
            temp_array.append(crossovered_array[index])  # hozzáadjuk az ideiglenes változóhoz a várost
            index += 1
        final_array.append(temp_array)  # hozzáadjuk a mátrixhoz az autót és annak városait
        temp_array = []  # ürítjük az ideiglenes változót a következő autó számára
    # pl: [2,5,1,3,4,6] -> [[0,2,5],[0,1,3],[0,4,6]]
    return final_array


def sort_array(length_base: list[int], array_base: list[int], generations: int):
    # növekvő sorrendbe rendezzük a távolság alapján (minél kisebb a táv, annál jobb)
    length = length_base.copy()
    array = array_base.copy()

    for i in range(generations - 1):
        for k in range(i + 1, generations):
            if length[i] > length[k]:
                temp = length[i]
                length[i] = length[k]
                length[k] = temp
                temp = array[i]
                array[i] = array[k]
                array[k] = temp

    return length, array


def get_route_from_survival_probability(route_current_length: list[int], generations: int,
                                        route_current: list[list[list[int]]], order_of_generations: list[int],
                                        population, route_best_length: int, route_all_length_best) \
        -> Tuple[list[list[int]], list[int], int]:  # túlélési generáció kiszámítása
    # route_current_length: jelenlegi eredmény hossza
    # route_current: jelenlegi eredmény
    # order_of_generations: jelenlegi eredmény sorrendje
    # population: jelenlegi generáció által túlélt adat
    # route_best_length: jelenlegi generáció által túlélt adat hossza
    # route_all_length_best: összes generáció által megtalált legjobb hosszeredmény

    random_number = random.random()  # túlélési esélyhez random szám
    survival_probability = 0.82  # konstans: 0 < survival_probability < 1
    ok = 0  # kilépési feltétel, ha van visszatérési értékünk
    counter = 0  # kilépési feltétel, a túlélt generáció indexe #Pn-edik eset a counter

    # P1, P2, P3, Pn a rendezett generációk, a genetic() függvényben a legvégén rendeztük őket

    while ok == 0 and counter < generations:  # túlélési esély számítása (feladat PDF-ben szereplő képlet alapján)
        if counter == 0:  # ha ez első generáció (külön kell kezelnünk az elsőt és az utolsót)
            if random_number < survival_probability:  # ha kisebb a random szám -> túlélt generáció
                print("First (best) generation survived, routes: " + str(route_current[order_of_generations[counter]]) +
                      ", length: " + str(route_current_length[order_of_generations[counter]]) + "\n")
                ok = 1
                population = route_current[order_of_generations[counter]]
                continue
            else:  # ha nem kisebb, akkor kivonjuk belőle az esélyt
                random_number -= survival_probability
            counter += 1
        else:  # ha nem az első, de nem is az utolsó
            if random_number < (pow(1 - survival_probability, counter) * survival_probability):  # ha kisebb a random szám -> túlélt generáció
                print("Average generation survived, routes: " + str(route_current[order_of_generations[counter]]) +
                      ", length: " + str(route_current_length[order_of_generations[counter]]) + "\n")
                ok = 1
                population = route_current[order_of_generations[counter]]
                continue
            else:  # ha nem kisebb, akkor kivonjuk belőle az esélyt
                random_number -= (pow(1 - survival_probability, counter) * survival_probability)
            counter += 1

    # ha ok == 0, akkor a legrosszabb eredmény élte túl a generálást
    if ok == 0:
        print("Last (worst) generation survived, routes: " + str(route_current[order_of_generations[generations - 1]]) +
              ", length: " + str(route_current_length[order_of_generations[generations - 1]]) + "\n")
        population = route_current[order_of_generations[generations - 1]]
        counter -= 1

    # ha az új generáció jobb, mint a valaha megtalált legjobb eredmény, akkor elmentjük
    if route_current_length[order_of_generations[counter]] < route_best_length:
        route_best_length = route_current_length[order_of_generations[counter]]
        population = route_current[order_of_generations[counter]]
        route_all_length_best = route_current[order_of_generations[counter]]
        print("\nBest generation:", str(population) + "\n" + ", length:", str(route_best_length), )

    return population, route_all_length_best, route_best_length


def delete_depo_from_array(route_with_depot: list[list[int]]) -> list[list[int]]:
    # kiszedjük a depót a feladatból
    # pl: [[0,2,5],[0,1,3],[0,4,6]] -> [[2,5],[1,3],[4,6]]
    route_without_depot = []
    for i in range(len(route_with_depot)):
        temp = []
        for k in range(len(route_with_depot[i])):
            if route_with_depot[i][k] != 0:
                temp.append(route_with_depot[i][k])
        route_without_depot.append(temp)
    return route_without_depot
