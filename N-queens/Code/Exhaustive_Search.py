import time
import tracemalloc

N=int(input("Enter the number of Queens: "))

CurrentSolution = [0] * N   #Creating an empty list to store the current solution with the size of N

class NQueens_Exhaustive:
    def __init__(self, size):       #Initializing the Nqueens class
        self.size = size      
    
    def is_safe(self, Test_row, Test_col):   # Check if the current position is safe for placing a queen
        
        if Test_row == 0:    # If it's the first row, we can place the queen in any column
            return True

        for row in range(0, Test_row):
            
            if Test_col == CurrentSolution[row] :   # Check if there's another queen in the same column
                return False
            
            if abs(Test_col - CurrentSolution[row]) == abs(Test_row - row):   # Check if there's another queen in the same diagonal
                return False
        return True
    
    def Exhaustive_Search(self, row):   # Recursive function to find first solution for the N-Queens problem
        global CurrentSolution
        
        # If we've placed all queens successfully, we found a solution
        if row == self.size:
            return True
        
        for col in range(0, self.size):
            if self.is_safe(row, col):
                CurrentSolution[row] = col
                
                if row == self.size - 1:
                    return True    # First solution found
                
                else:
                    if self.Exhaustive_Search(row + 1):
                        return True    # Pass solution back up
        
        return False    # No solution found in this branch

# Start tracking memory and time
tracemalloc.start()
start_time = time.time()

solution = NQueens_Exhaustive(N)
found_solution = solution.Exhaustive_Search(0)

# Get memory and time
current, _ = tracemalloc.get_traced_memory()
end_time = time.time()

# Calculate metrics
execution_time = end_time - start_time
memory_used = current / 1024  # Convert to KB

if found_solution:
    print("\nFirst solution found:")
    print(CurrentSolution)
else:
    print("\nNo solution exists")

print(f"\nPerformance Metrics (Exhaustive Search):")
print(f"Time taken: {execution_time:.2f} seconds")
print(f"Memory used: {memory_used:.2f} KB")

# Stop tracking
tracemalloc.stop()