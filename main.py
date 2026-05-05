import random
import math
import matplotlib.pyplot as plt

# =============================
# CIUDADES (coordenadas)
# =============================
cities = {
    0: (0,0),
    1: (1,5),
    2: (2,3),
    3: (5,2),
    4: (6,6),
    5: (8,3),
    6: (7,7),
    7: (3,8)
}

# =============================
# DISTANCIA Y FITNESS
# =============================
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def fitness(route):
    total = 0
    for i in range(len(route)-1):
        total += distance(cities[route[i]], cities[route[i+1]])
    return total

# =============================
# VALIDACIÓN DE INTEGRIDAD
# =============================
def is_valid(route):
    return len(route) == len(set(route))

# =============================
# CREAR POBLACIÓN
# =============================
def create_population(size):
    return [random.sample(list(cities.keys()), len(cities)) for _ in range(size)]

# =============================
# CRUZA
# =============================
def crossover(p1, p2):
    cut = len(p1)//2
    child = p1[:cut] + [c for c in p2 if c not in p1[:cut]]
    return child

# =============================
# MUTACIÓN
# =============================
def mutate(route, rate):
    if random.random() < rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

# =============================
# ALGORITMO ORIGINAL
# =============================
def genetic_original(generations=100, pop_size=20):
    population = create_population(pop_size)
    history = []

    for _ in range(generations):
        population = sorted(population, key=fitness)
        history.append(fitness(population[0]))

        selected = population[:10]
        new_pop = []

        while len(new_pop) < pop_size:
            p1, p2 = random.sample(selected, 2)
            child = crossover(p1, p2)
            child = mutate(child, 0.1)

            if is_valid(child):
                new_pop.append(child)

        population = new_pop

    return history

# =============================
# SELECCIÓN TORNEO
# =============================
def tournament(pop):
    k = 3
    selected = random.sample(pop, k)
    return min(selected, key=fitness)

# =============================
# ALGORITMO MEJORADO
# =============================
def genetic_improved(generations=100, pop_size=20):
    population = create_population(pop_size)
    history = []
    mutation_rate = 0.1
    best_prev = float("inf")

    for _ in range(generations):
        population = sorted(population, key=fitness)
        best = fitness(population[0])
        history.append(best)

        # ELITISMO
        new_pop = population[:2]

        # ADAPTATIVA
        if best >= best_prev:
            mutation_rate *= 1.2
        else:
            mutation_rate *= 0.9

        best_prev = best

        while len(new_pop) < pop_size:
            p1 = tournament(population)
            p2 = tournament(population)

            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)

            if is_valid(child):
                new_pop.append(child)

        population = new_pop

    return history

# =============================
# EJECUCIÓN
# =============================
original = genetic_original()
improved = genetic_improved()

# =============================
# GRÁFICA
# =============================
plt.plot(original, label="Original")
plt.plot(improved, label="Mejorado")

plt.xlabel("Generaciones")
plt.ylabel("Distancia")
plt.title("Comparación Algoritmo Genético")
plt.legend()

plt.show()