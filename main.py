import math
import random
import time
import pandas as pd
from Genetic.PyeasygaExtend import PayeasygaExtend
import matplotlib.pyplot as plt
from colorama import Fore, Style


def metric(x, y):
    return math.sqrt(pow(x - end_x, 2) + pow(y - end_y, 2))


def loadData(fileName):
    try:
        file = open(fileName, 'r')
        for index, line in enumerate(file):
            maze_map[index] = [int(n) for n in line.split()]
        file.close()
    except FileNotFoundError:
        print("File not exist!")


def printMap():
    for row in maze_map:
        for val in row:
            if val == 5:
                print(Fore.YELLOW + str(val), sep=' ', end=' ', flush=False)
            if val == 0:
                print(Fore.BLUE + str(val), sep=' ', end=' ', flush=False)
            if val == 3:
                print(Fore.RED + str(val), sep=' ', end=' ', flush=False)
        print()
    print(Style.RESET_ALL)


def checkMove(x, y, map_x, map_y):
    if x == 0 and y == 0:  # dol
        map_y += 1  # robimy krok w dol
        # sprawdzamy czy wspolrzedna nie wykracza poza zakres mapy
        # sprawdzamy czy pod wskazanymi wspolrzednymi znajduje się dozwolona wartosc (0 - mozemy isc)
        if 0 <= map_y < len(maze_map[0]) and (maze_map[map_y][map_x] == 0 or maze_map[map_y][map_x] == 3):
            return map_x, map_y
        else:
            map_y -= 1  # cofamy sie do punktu wejsciowego
    if x == 1 and y == 1:  # gora
        map_y -= 1  # robimy krok w gore
        if 0 <= map_y < len(maze_map[0]) and (maze_map[map_y][map_x] == 0 or maze_map[map_y][map_x] == 3):
            return map_x, map_y
        else:
            map_y += 1  # cofamy sie do punktu wejsciowego
    if x == 0 and y == 1:  # prawo
        map_x += 1  # robimy krok w prawo
        if 0 <= map_x < len(maze_map) and (maze_map[map_y][map_x] == 0 or maze_map[map_y][map_x] == 3):
            return map_x, map_y
        else:
            map_x -= 1  # cofamy sie do punktu wejsciowego
    if x == 1 and y == 0:  # lewo
        map_x -= 1  # robimy krok w lewo
        if 0 <= map_x < len(maze_map) and (maze_map[map_y][map_x] == 0 or maze_map[map_y][map_x] == 3):
            return map_x, map_y
        else:
            map_x += 1  # cofamy sie do punktu wejsciowego
    return map_x, map_y


# Fitness z mozliwoscia powrotu do punktu, który już odwiedziliśmy
def fitness(individual, data):
    it = iter(individual)
    map_x = 0  # wspolrzedna x punktu startowego
    map_y = 0  # wspolrzedna y punktu startowego
    for x, y in zip(it, it):
        map_x, map_y = checkMove(x, y, map_x, map_y)  # sprawdzamy czy jest mozliwy nastepny ruch
    if map_x == end_x and map_y == end_y:  # jezeli osiągneliśmy cel
        return 0  # zwracamy maxymalna wartosc funkcji
    else:  # jezeli nie osiagnelismy celu
        return metric(map_x, map_y) * -1  # zwracamy odleglosc do celu za pomoca metryki Euklidesowskiej


# Fitness v2 bez mozliwosci powrotu do punktu , w którym już byliśmy
def fitnessV2(individual, data):
    it = iter(individual)
    map_x = 0  # wspolrzedna x punktu startowego
    map_y = 0  # wspolrzedna y punktu startowego
    visited_points = []  # tablica przetrzymujaca odwiedzone punkty
    for x, y in zip(it, it):
        tmp_x, tmp_y = checkMove(x, y, map_x, map_y)  # sprawdzamy czy jest mozliwy nastepny ruch
        if (tmp_x, tmp_y) not in visited_points:  # jezeli nie odwiedzilismy punktu
            visited_points.append((tmp_x, tmp_y))  # dodajemy ten punkt do listy odiwedzonych punktow
            map_x = tmp_x  # zmieniamy polozenie
            map_y = tmp_y
    if map_x == end_x and map_y == end_y:  # jezeli osiągneliśmy cel
        return 0  # zwracamy maxymalna wartosc funkcji
    else:  # jezeli nie osiagnelismy celu
        return metric(map_x, map_y) * -1  # zwracamy odleglosc do celu za pomoca metryki Euklidesowskiej


def create_individual(data):
    return [random.randint(0, 1) for _ in range(chromosome_length)]


def showPath(individual):
    it = iter(individual)
    map_x = 0
    map_y = 0
    maze_map[map_x][map_y] = 3
    maze_map[end_x][end_y] = 3
    visited_points = []
    for x, y in zip(it, it):
        tmp_x, tmp_y = checkMove(x, y, map_x, map_y)
        if ga.fitness_function == fitnessV2:
            if (tmp_x, tmp_y) not in visited_points:
                visited_points.append((tmp_x, tmp_y))
                map_x = tmp_x
                map_y = tmp_y
        else:
            map_x = tmp_x
            map_y = tmp_y
        maze_map[map_y][map_x] = 3
    printMap()


def generateGeneticAlgorithmPlot():
    plt.plot(list(range(ga.generations)), [round(i, 2) for i in average_fitness], label='srednia')
    plt.plot(list(range(ga.generations)), [round(i, 2) for i in best_fitness], label='maksymalne')
    plt.legend()
    plt.title('Dzialanie Alg. Genetycznego')
    plt.xlabel('pokolenie')
    plt.ylabel('fitness (ocena)')
    plt.show()


def generateTimePlot():
    time_a_star = [(0.0953, 0.0987), (0.2764, 0.2685), (1.0319, 0.8363), (5.7661, 3.2631)]
    time_fitness_v1 = [(0.1785, 0.3343), (0.8008, 64.150), (1.1772, 30.5265), (7.8310, 75.0808)]
    time_fitness_v2 = [(0.1606, 0.2458), (0.7955, 3.2012), (1.5664, 48.3100), (65.5038, 42.0875)]
    labels = ['10x10', '25x25', '50x50', '100x100']
    fig, axs = plt.subplots(1, 2)
    df1 = pd.DataFrame({
        "A*": [el[0] for el in time_a_star],
        "Fitness V1": [el[0] for el in time_fitness_v1],
        "Fitness V2": [el[0] for el in time_fitness_v2]
    }, index=labels)
    df2 = pd.DataFrame({
        "A*": [el[1] for el in time_a_star],
        "Fitness V1": [el[1] for el in time_fitness_v1],
        "Fitness V2": [el[1] for el in time_fitness_v2]
    }, index=labels)
    ax1 = df1.plot(rot=0, ax=axs[0], title="Czas działania - inputy otwarte")
    ax2 = df2.plot(rot=0, ax=axs[1], title="Czas działania - inputy zamknięte")
    ax1.set_xlabel("Wielkość inputów")
    ax1.set_ylabel("Czas [s]")
    ax2.set_xlabel("Wielkość inputów")
    ax2.set_ylabel("Czas [s]")
    plt.show()


map_size = 25
end_x = map_size - 1
end_y = map_size - 1
maze_map = [[0 for y in range(map_size)] for x in range(map_size)]
chromosome_length = 150

loadData("inputs/25x25-open.txt")
example_chr = [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0]
print(f"Przykladowy chromosom : {example_chr} i jego wartosc fitnessV1: {fitness(example_chr, maze_map)}")
print(f"Przykladowy chromosom : {example_chr} i jego wartosc fitnessV2: {fitnessV2(example_chr, maze_map)}")

ga = PayeasygaExtend(maze_map, population_size=180, generations=35, mutation_probability=0.55, elitism=True)
ga.fitness_function = fitness
ga.create_individual = create_individual
start = time.perf_counter()
average_fitness, best_fitness = ga.run()
stop = time.perf_counter()
if 0 in best_fitness:
    print(f"Osiągnięto cel w  {stop - start:0.4f} sekund")
    showPath(ga.best_individual()[1])
else:
    print("Nie znaleziono rozwiązania")

generateGeneticAlgorithmPlot()
generateTimePlot()
