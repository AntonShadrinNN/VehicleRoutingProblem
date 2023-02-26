import math
import random
from copy import deepcopy
from random import shuffle, random, randint
import heapq


class PrioritySet:

    def __init__(self):
        self.heap = []
        self.set = set()

    def push(self, d):
        if d not in self.set:
            heapq.heappush(self.heap, d)
            self.set.add(d)

    def pop(self):
        d = heapq.heappop(self.heap)
        self.set.remove(d)
        return d

    def poop(self):
        d = self.heap[-1]
        self.heap = self.heap[:-1]
        self.set.remove(d)
        return d

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        op = ""
        for i in self.heap:
            op += f'{i[0]} : {i[1]}\n'
        return op

    def __getitem__(self, item):
        return self.heap[item]


class City:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        return f'({self._x}, {self._y})'


class Customer:

    def __init__(self, number: int, demand: int, pos: City = City(-1, -1)):
        self.number = number
        self.demand = demand
        self.pos = pos

    def __str__(self):
        return f'(n={self.number}, d={self.demand}, p={self.pos})'

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number

    def __hash__(self):
        return hash(self.number)


TRUCKS = 3
CAPACITY = 60
POPULATION_SIZE = 20
POPULATION = []
MUTATION_RATE = 0.7
CROSSOVER_RATE = 0.9
DEPOT = Customer(-1, 0, City(0, 0))
CUSTOMERS = []


def calculate_distance(city1, city2) -> float:
    return math.sqrt(((city1.pos.x - city2.pos.x) ** 2) + ((city1.pos.y - city2.pos.y) ** 2))


def get_fitness(chromosome: list):
    fitness = 0
    res = list(deepcopy(chromosome))
    res.insert(0, DEPOT)
    res.append(DEPOT)

    for i in range(len(chromosome) - 1):
        fitness += calculate_distance(chromosome[i], chromosome[i + 1])

    cur_demand = 0
    for city in res:
        if city == DEPOT and cur_demand > CAPACITY:
            fitness = math.inf
        elif city == DEPOT:
            cur_demand = 0
        else:
            cur_demand += city.demand

    return fitness


def get_population_fitness(p):
    h = PrioritySet()
    for i in p:
        h.push((get_fitness(i), i))

    return h


def create_chromosome():
    temp = deepcopy(CUSTOMERS)
    shuffle(temp)

    return temp


def initialize():
    while len(POPULATION) < POPULATION_SIZE:
        chromosome = create_chromosome()

        if get_fitness(chromosome) != math.inf:
            POPULATION.append(tuple(chromosome))


def random_borders(temp):
    left = randint(1, len(temp) - 2)
    right = randint(left, len(temp) - 1)
    return left, right


def mutate(chromosome):
    temp = list(deepcopy(chromosome))
    if random() < MUTATION_RATE:
        left, right = random_borders(temp)
        temp[left], temp[right] = temp[right], temp[left]

    return tuple(temp)


def crossover(chr1, chr2):
    if random() < CROSSOVER_RATE:
        left, right = random_borders(chr1)
        c1 = [c for c in chr1[0:] if c not in chr2[left:right + 1]]

        a1 = c1[:left] + list(chr2)[left:right + 1] + c1[left:]

        c2 = [c for c in chr2[0:] if c not in chr1[left:right + 1]]
        b1 = c2[:left] + list(chr1)[left:right + 1] + c2[left:]
        return a1, b1

    return chr1, chr2


def main_algo():
    minimum_chrom = h[0]
    count = 0
    while count < 1000:
        ax = h.pop()
        bx = h.pop()
        if ax[0] == 0 or bx[0] == 0:
            continue
        a, b = crossover(ax[1], bx[1])
        a = mutate(a)

        while get_fitness(a) == math.inf:
            a = create_chromosome()
        b = mutate(b)
        while get_fitness(b) == math.inf:
            b = create_chromosome()

        if get_fitness(a) != math.inf:
            h.push((get_fitness(a), tuple(a)))
        else:
            h.push(ax)
        if get_fitness(b) != math.inf:
            h.push((get_fitness(b), tuple(b)))
        else:
            h.push(bx)

        while len(h) < POPULATION_SIZE:
            temp = deepcopy(CUSTOMERS)
            count += 1
            shuffle(temp)
            h.push((get_fitness(temp), tuple(temp)))

        count += 1

        if count % 10 == 0:
            print(f"{count} - Generation done")

        if h[0][0] < minimum_chrom[0]:
            if h[0][0] == 0:
                print(h)
            minimum_chrom = h[0]
            print(f'Current minimum = {minimum_chrom[0]}')

    print()
    print(*minimum_chrom[1])
    print(count)


if __name__ == '__main__':
    test_locations = [(1, 2), (2, 3), (4, 5), (-1, -2), (-3, -4), (-2, 3)]
    test_demands = [20, 20, 20, 20, 20, 20]

    for i in range(0, len(test_locations)):
        CUSTOMERS.append(Customer(i, test_demands[i], City(*test_locations[i])))

    CUSTOMERS += [DEPOT] * TRUCKS
    shuffle(CUSTOMERS)

    initialize()
    h = get_population_fitness(POPULATION)
    main_algo()
