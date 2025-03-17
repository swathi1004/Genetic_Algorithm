import random
import numpy as np
class JobSchedulingGA:
    def __init__(self, jobs, machines, population_size=10, generations=100, mutation_rate=0.1):
        self.jobs = jobs
        self.machines = machines
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()
    
    def initialize_population(self):
        return [np.random.randint(0, self.machines, size=len(self.jobs)).tolist() for _ in range(self.population_size)]
    
    def fitness(self, chromosome):
        machine_times = [0] * self.machines
        for job, machine in zip(self.jobs, chromosome):
            machine_times[machine] += job
        return max(machine_times)
    
    def selection(self):
        sorted_population = sorted(self.population, key=lambda x: self.fitness(x))
        return sorted_population[:self.population_size // 2]
    
    def crossover(self, parent1, parent2):
        point1, point2 = sorted(random.sample(range(len(self.jobs)), 2))
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        return child1, child2
    
    def mutate(self, chromosome):
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(self.jobs) - 1)
            chromosome[idx] = random.randint(0, self.machines - 1)
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
    
jobs = [5, 8, 2, 10, 7]  
machines = 3

ga = JobSchedulingGA(jobs, machines)
best_schedule = ga.evolve()
print("Best Job Schedule:", best_schedule)
print("Minimum Completion Time:", ga.fitness(best_schedule))
