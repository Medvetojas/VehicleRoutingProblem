from plot import *
from problem import *
from genetic import *


def main():
    random.seed(int(input("Seed for RNG: ")))
    city_matrix = generate_city_locations(int(input("City amount (including depot): ")))  # Városok a koordinátákkal
    city_distance_matrix = get_all_city_distance(city_matrix)
    initial_routes = create_routes(int(input("Vehicle amount: ")), city_distance_matrix, city_matrix)
    print("Initial solution: " + str(initial_routes))  # Kiindulási útvonal printelése

    best, length = begin_algorithm(
        initial_routes,
        city_distance_matrix,
        int(input("Iteration amount: ")),
        int(input("Generation amount: ")))

    print("\nThe genetic algorithm's solution is the following: " + str(best) +
          "\nTotal length of solution: " + str(length) + " units."
          "\nPlotting the solution...")

    plot_solution(city_matrix, best)

    print("\nPlot has been generated, the program will now exit.")


if __name__ == "__main__":
    main()
