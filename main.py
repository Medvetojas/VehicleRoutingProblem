from plot import *
from problem import *
from genetic import *


def main():
    random.seed(int(input("Seed for RNG: ")))
    city_matrix = generate_city_locations(int(input("City amount (including depot): ")))  # Városok a koordinátákkal
    city_distance_matrix = get_all_city_distance(city_matrix)
    initial_routes = create_routes(int(input("Vehicle amount: ")), city_distance_matrix, city_matrix)
    print("Initial solution: " + str(initial_routes))  # Kiindulási útvonal printelése
    best, length = genetic_algorithm(
        initial_routes,
        city_distance_matrix,
        int(input("Iteration amount: ")),
        int(input("Generation amount: ")))
    print("The genetic algorithm's solution is the following:\n", str(best), "\nTotal length of solution:", length)
    plot_solution(city_matrix, best)


if __name__ == "__main__":
    main()
