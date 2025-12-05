import random
import time
import tracemalloc

class NQueensSolver:
    def __init__(self, size):
        self.size = size
        self.solution = list(range(size))  # Initial permutation
        self.col_conflicts = [0] * size
        self.diag1_conflicts = [0] * (2 * size - 1)  # row + col
        self.diag2_conflicts = [0] * (2 * size - 1)  # row - col + size - 1

    def random_restart(self): 
        random.shuffle(self.solution)  # Randomly shuffle the initial solution
        self.col_conflicts = [0] * self.size
        self.diag1_conflicts = [0] * (2 * self.size - 1)  # Formula for counting diagonal conflicts
        self.diag2_conflicts = [0] * (2 * self.size - 1)
        
        for row, col in enumerate(self.solution):
            self.col_conflicts[col] += 1
            self.diag1_conflicts[row + col] += 1
            self.diag2_conflicts[row - col + self.size - 1] += 1

    def find_conflicts(self, row, col):  # Count conflicts for a queen at the given position
        return (self.col_conflicts[col] + self.diag1_conflicts[row + col] + self.diag2_conflicts[row - col + self.size - 1] - 3)

    def solve(self):  
        max_attempts = 1000  # Number of maximum random restarts
        max_steps = 2 * self.size # Maximum steps per attempt so that it doesn't give up too early or spend too long
        
        for _ in range(max_attempts):
            self.random_restart()
            
            for _ in range(max_steps): # Find queen with maximum conflicts
                max_conflicts = -1
                candidates = []
                
                for row in range(self.size):
                    conflicts = self.find_conflicts(row, self.solution[row])
                    if conflicts > max_conflicts:
                        max_conflicts = conflicts
                        candidates = [row]
                    elif conflicts == max_conflicts:
                        candidates.append(row)
                
                if max_conflicts == 0:
                    return self.solution  # Solution found
                
                row = random.choice(candidates)
                current_col = self.solution[row] #Select a random queen with maximum conflicts
                
                # Find best move for this queen
                min_conflicts = float('inf')
                best_cols = []
                
                for col in range(self.size):
                    conflicts = (self.col_conflicts[col] + 
                               self.diag1_conflicts[row + col] + 
                               self.diag2_conflicts[row - col + self.size - 1])
                    if col == current_col:
                        conflicts -= 3
                    
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_cols = [col]
                    elif conflicts == min_conflicts:
                        best_cols.append(col)
                
                new_col = random.choice(best_cols)
                
                # Update conflicts
                self.col_conflicts[current_col] -= 1
                self.diag1_conflicts[row + current_col] -= 1
                self.diag2_conflicts[row - current_col + self.size - 1] -= 1
                
                self.solution[row] = new_col
                
                self.col_conflicts[new_col] += 1
                self.diag1_conflicts[row + new_col] += 1
                self.diag2_conflicts[row - new_col + self.size - 1] += 1
        
        return None  # No solution found (shouldn't happen for N > 3)

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

print(f"\nPerformance Metrics (Hill Climbing):")
print(f"Time taken: {execution_time:.2f} seconds")
print(f"Memory used: {memory_used:.2f} KB")

# Stop tracking
tracemalloc.stop()