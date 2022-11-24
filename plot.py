import matplotlib.pyplot as plot


def plot_solution(city_matrix: list[list[int]], best: list[list[int]]):  # Kirajzolás matplotlib segítségével
    plot.plot(city_matrix[0][0], city_matrix[0][1], 'ro')
    plot.annotate('Depot', (city_matrix[0][0], city_matrix[0][1]))
    for i in range(1, len(city_matrix)):
        plot.plot(city_matrix[i][0], city_matrix[i][1], 'bo')
        plot.annotate(i, (city_matrix[i][0], city_matrix[i][1]))
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
    for i in range(len(best)):
        for k in range(len(best[i])):
            if k == len(best[i]) - 1:
                plot.plot([city_matrix[best[i][k]][0], city_matrix[best[i][0]][0]],
                          [city_matrix[best[i][k]][1], city_matrix[best[i][0]][1]], colors[i % 10])
            else:
                plot.plot([city_matrix[best[i][k]][0], city_matrix[best[i][k + 1]][0]],
                          [city_matrix[best[i][k]][1], city_matrix[best[i][k + 1]][1]], colors[i % 10])
    plot.show()
