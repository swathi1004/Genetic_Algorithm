import random
import numpy as np

class BinPackingGA:
    def __init__(self, items, bin_capacity, population_size=10, generations=100, mutation_rate=0.1):
        self.items = items
        self.bin_capacity = bin_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()
    
    def initialize_population(self):
        return [np.random.permutation(len(self.items)).tolist() for _ in range(self.population_size)]
    
    def fitness(self, chromosome):
        bins = []
        for idx in chromosome:
            placed = False
            for bin in bins:
                if sum(bin) + self.items[idx] <= self.bin_capacity:
                    bin.append(self.items[idx])
                    placed = True
                    break
            if not placed:
                bins.append([self.items[idx]])
        return len(bins)
    
    def selection(self):
        sorted_population = sorted(self.population, key=lambda x: self.fitness(x))
        return sorted_population[:self.population_size // 2]
    
    def crossover(self, parent1, parent2):
        point = random.randint(1, len(self.items) - 1)
        child1 = parent1[:point] + [x for x in parent2 if x not in parent1[:point]]
        child2 = parent2[:point] + [x for x in parent1 if x not in parent2[:point]]
        return child1, child2
    
    def mutate(self, chromosome):
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(self.items)), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome
    
    def evolve(self):
        for _ in range(self.generations):
            selected = self.selection()
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)
                child1, child2 = self.crossover(parent1, parent2)
                new_population += [self.mutate(child1), self.mutate(child2)]
            self.population = new_population[:self.population_size]
        return min(self.population, key=lambda x: self.fitness(x))

# Example usage
items = [4, 8, 1, 4, 2, 6, 3]  # Item sizes
bin_capacity = 10

ga_bin = BinPackingGA(items, bin_capacity)
best_packing = ga_bin.evolve()
print("Best Bin Packing Order:", best_packing)
print("Minimum Number of Bins Used:", ga_bin.fitness(best_packing))
