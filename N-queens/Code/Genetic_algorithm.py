import random
import time
import tracemalloc

class NQueensGeneticSolver:
    def __init__(self, size, population_size=100):
        self.size = size
        self.population_size = population_size
        self.max_generations = 50000000  #maximum amount of generations 
        self.mutation_rate = 0.1  #I chose 0.1 because it is a good balance between exploration and exploitation
        self.stagnation_limit = 1000  # Reset if no improvement for this many generations
        self.best_fitness_seen = float('-inf')
        self.generations_without_improvement = 0
        
        # Initialize population
        self.population = []
        for _ in range(population_size):
            solution = list(range(size))  
            random.shuffle(solution) 
            self.population.append({    #Adding random solutions to the population
                'solution': solution,
                'col_conflicts': [0] * size,
                'diag1_conflicts': [0] * (2 * size - 1),  # row + col
                'diag2_conflicts': [0] * (2 * size - 1)   # row - col + size - 1
            })
            
            self.update_conflicts(self.population[-1]) #Calculate conflicts for the last added value

    def update_conflicts(self, individual):
        # Reset conflicts
        individual['col_conflicts'] = [0] * self.size
        individual['diag1_conflicts'] = [0] * (2 * self.size - 1)
        individual['diag2_conflicts'] = [0] * (2 * self.size - 1)
        
        # Calculate conflicts
        for row, col in enumerate(individual['solution']):
            individual['col_conflicts'][col] += 1
            individual['diag1_conflicts'][row + col] += 1
            individual['diag2_conflicts'][row - col + self.size - 1] += 1

    def fitness(self, individual):
        # Calculate total conflicts
        total_conflicts = (
            sum(c - 1 for c in individual['col_conflicts'] if c > 1) +
            sum(c - 1 for c in individual['diag1_conflicts'] if c > 1) +
            sum(c - 1 for c in individual['diag2_conflicts'] if c > 1)    #count every conflicting queen
        )
        return -total_conflicts  # Higher fitness is better (0 is best)

    def select_parent(self):
        # Tournament selection
        tournament_size = 5
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=self.fitness) #select the best individual from the tournament 

    def crossover(self, parent1, parent2):
        # Order Crossover (OX)
        n = self.size
        start, end = sorted(random.sample(range(n), 2))
        
        # Create child structure
        child = {
            'solution': [None] * n,
            'col_conflicts': [0] * n,
            'diag1_conflicts': [0] * (2 * n - 1),
            'diag2_conflicts': [0] * (2 * n - 1)
        }
        
        # Copy segment from parent1
        child['solution'][start:end] = parent1['solution'][start:end]
        
        # Fill remaining positions with values from parent2 that aren't used yet
        remaining_values = [x for x in parent2['solution'] if x not in parent1['solution'][start:end]]
        child['solution'][:start] = remaining_values[:start]
        child['solution'][end:] = remaining_values[start:]
        
        # Update conflicts for child
        self.update_conflicts(child)
        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            # Swap two random positions
            i, j = random.sample(range(self.size), 2) #chooses two random positions
            individual['solution'][i], individual['solution'][j] = individual['solution'][j], individual['solution'][i]
            # Update conflicts after mutation
            self.update_conflicts(individual)
        return individual

    def is_solution(self, individual): #checks if the solution is valid
        return (max(individual['col_conflicts']) <= 1 and 
                max(individual['diag1_conflicts']) <= 1 and 
                max(individual['diag2_conflicts']) <= 1)

    def solve(self): #main function that solves the problem
        generation = 0 
        while generation < self.max_generations:
            # Check current population for solution
            for individual in self.population:
                if self.is_solution(individual):
                    return individual['solution']
            
            # Create new generation
            new_population = []
            for _ in range(self.population_size):
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            self.population = new_population
            
            # Check for improvement
            current_best_fitness = max(self.fitness(ind) for ind in self.population)
            if current_best_fitness > self.best_fitness_seen:
                self.best_fitness_seen = current_best_fitness
                self.generations_without_improvement = 0
            else:
                self.generations_without_improvement += 1
            
            # Reset if stuck
            if self.generations_without_improvement >= self.stagnation_limit:
                print(f"Restarting at generation {generation} due to stagnation")
                self.population = []
                for _ in range(self.population_size):
                    solution = list(range(self.size))  
                    random.shuffle(solution) 
                    self.population.append({    #Adding random solutions to the population
                        'solution': solution,
                        'col_conflicts': [0] * self.size,
                        'diag1_conflicts': [0] * (2 * self.size - 1),  # row + col
                        'diag2_conflicts': [0] * (2 * self.size - 1)   # row - col + size - 1
                    })
                    
                    self.update_conflicts(self.population[-1]) #Calculate conflicts for the last added value
                self.best_fitness_seen = float('-inf')
                self.generations_without_improvement = 0
                self.mutation_rate = 0.1  # Reset mutation rate
            
            generation += 1
            
            # Print progress every 1000 generations
            if generation % 1000 == 0:
                print(f"Generation {generation}, Best Fitness: {current_best_fitness}")
            
            # If stuck, introduce more diversity
            if generation % 10000 == 0:
                self.mutation_rate = min(0.5, self.mutation_rate * 1.1)
        
        # If no solution found, return best individual
        return max(self.population, key=self.fitness)['solution']

# Get input
N = int(input("Enter number of queens: "))

# Start tracking memory and time
tracemalloc.start()
start_time = time.time()

solver = NQueensGeneticSolver(N)
solution = solver.solve()

# Get memory and time
current, _ = tracemalloc.get_traced_memory()
end_time = time.time()

# Calculate metrics
execution_time = end_time - start_time
memory_used = current / 1024  # Convert to KB

print("\nSolution found:")
print(solution)

print(f"\nPerformance Metrics (Genetic Algorithm):")
print(f"Time taken: {execution_time:.2f} seconds")
print(f"Memory used: {memory_used:.2f} KB")

# Stop tracking
tracemalloc.stop()
