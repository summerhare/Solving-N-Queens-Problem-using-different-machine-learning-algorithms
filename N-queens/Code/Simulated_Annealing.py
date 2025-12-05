import random
import math
import time
import tracemalloc

class NQueensSolver:
    def __init__(self, size):
        self.size = size
        self.max_attempts = 500000  # Number of maximum random restarts
        self.solution = list(range(size))  # Initial permutation
        random.shuffle(self.solution)  # Randomly shuffle the initial solution
        self.col_conflicts = [0] * size
        self.diag1_conflicts = [0] * (2 * size - 1)  # row + col
        self.diag2_conflicts = [0] * (2 * size - 1)  # row - col + size - 1
        self.T = 1
        cooling_rate = 1.0 - (1.0 / (10 * N))  # Adaptive cooling
        self.T *= cooling_rate
        for row, col in enumerate(self.solution):
            self.col_conflicts[col] += 1
            self.diag1_conflicts[row + col] += 1
            self.diag2_conflicts[row - col + self.size - 1] += 1

    def random_restart(self):
        random.shuffle(self.solution)  # Randomly shuffle the initial solution
        size = self.size
        self.col_conflicts = [0] * size
        self.diag1_conflicts = [0] * (2 * size - 1)  # row + col
        self.diag2_conflicts = [0] * (2 * size - 1)  # row - col + size - 1
        self.T = 1
        cooling_rate = 1.0 - (1.0 / (10 * N))  # Adaptive cooling
        self.T *= cooling_rate
        
        for row, col in enumerate(self.solution):
            self.col_conflicts[col] += 1
            self.diag1_conflicts[row + col] += 1
            self.diag2_conflicts[row - col + self.size - 1] += 1
        

    def calculate_delta_conflicts(self, row, old_col, new_col):
        #Calculate conflict change 
        old_conflicts = (
            self.col_conflicts[old_col] + 
            self.diag1_conflicts[row + old_col] + 
            self.diag2_conflicts[row - old_col + self.size - 1] - 3
        )
        new_conflicts = (
            self.col_conflicts[new_col] + 
            self.diag1_conflicts[row + new_col] + 
            self.diag2_conflicts[row - new_col + self.size - 1]
        )
        return new_conflicts - old_conflicts

    def solve(self):        
            
        while (1):

            self.max_attempts -= 1
            if self.max_attempts <= 0:
                self.max_attempts = 500000
                self.random_restart()  # Restart if maximum attempts reached
                print("Restarting with a new random solution.")

            row = random.randint(0, self.size - 1)  # Select a random row
            current_col = self.solution[row] # Current column of the queen in the selected row
            new_col = random.randint(0, self.size - 1)  # Randomly select a new column
            if new_col == current_col:
                continue  # Skip if the new column is the same as the current one
            else:
                # Calculate the change in conflicts
                delta_conflicts = self.calculate_delta_conflicts(row, current_col, new_col)
                
                if delta_conflicts <= 0 or random.random() < math.exp(-delta_conflicts / self.T):
                    # Accept the move if it reduces conflicts or with a probability based on temperature
                    self.col_conflicts[current_col] -= 1
                    self.diag1_conflicts[row + current_col] -= 1
                    self.diag2_conflicts[row - current_col + self.size - 1] -= 1 # Reduce conflicts for the current position
                    
                    self.solution[row] = new_col
                    
                    self.col_conflicts[new_col] += 1
                    self.diag1_conflicts[row + new_col] += 1
                    self.diag2_conflicts[row - new_col + self.size - 1] += 1 # Increase conflicts for the new position
            self.T= self.T * 0.999  # Cool down the temperature
            if max(self.col_conflicts) <=1 and max(self.diag1_conflicts) <=1 and max(self.diag2_conflicts) <=1:  # Check if all queens are placed without conflicts
                return self.solution
            if self.T < 0.1:
                self.T = float(2 * self.size)

# Get input
N = int(input("Enter number of queens: "))

# Start tracking memory and time
tracemalloc.start()
start_time = time.time()

solver = NQueensSolver(N)
solution = solver.solve()

# Get memory and time
current, _ = tracemalloc.get_traced_memory()
end_time = time.time()

# Calculate metrics
execution_time = end_time - start_time
memory_used = current / 1024  # Convert to KB

print("\nFirst solution found:")
print(solution)

print(f"\nPerformance Metrics (Simulated Annealing):")
print(f"Time taken: {execution_time:.2f} seconds")
print(f"Memory used: {memory_used:.2f} KB")

# Stop tracking
tracemalloc.stop()