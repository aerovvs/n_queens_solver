import random
import math
import time

# calculate the number of conflicts for a given board
def calculate_heuristic(board):
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

# display the board in a grid format
def display_board(board):
    n = len(board)
    for row in range(n):
        line = ["Q" if board[col] == row else "." for col in range(n)]
        print(" ".join(line))
    print()

# steepest-ascent hill climbing algorithm
def hill_climbing(n):
    # generate a random initial board
    board = [random.randint(0, n - 1) for _ in range(n)]
    steps = 0
    while True:
        heuristic = calculate_heuristic(board)
        if heuristic == 0:
            return board, heuristic, steps

        neighbors = []
        for i in range(n):
            for j in range(n):
                if board[i] != j:
                    new_board = board[:]
                    new_board[i] = j
                    neighbors.append((new_board, calculate_heuristic(new_board)))

        # choose the neighbor with the lowest heuristic
        best_neighbor = min(neighbors, key=lambda x: x[1])

        if best_neighbor[1] >= heuristic:
            return board, heuristic, steps  # return current board if no improvement

        board = best_neighbor[0]
        steps += 1

# simulated annealing algorithm
def simulated_annealing(n, initial_temp=2000, cooling_rate=0.95, max_steps=1000):
    # generate a random initial board
    board = [random.randint(0, n - 1) for _ in range(n)]
    temp = initial_temp
    steps = 0

    while temp > 1 and steps < max_steps:
        heuristic = calculate_heuristic(board)
        if heuristic == 0:
            return board, heuristic, steps

        # generate multiple neighbors and pick one
        neighbors = []
        for _ in range(10):  # generate 10 random neighbors
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            new_board = board[:]
            new_board[i] = j
            neighbors.append((new_board, calculate_heuristic(new_board)))

        # select a neighbor probabilistically based on heuristic
        chosen_neighbor = min(neighbors, key=lambda x: x[1])
        new_board, new_heuristic = chosen_neighbor

        # decide whether to accept the new state
        delta_e = new_heuristic - heuristic
        if delta_e < 0 or random.random() < math.exp(-delta_e / temp):
            board = new_board

        temp *= cooling_rate  # cool down
        steps += 1

    return board, calculate_heuristic(board), steps

# min-conflicts algorithm with adaptive restarts and dynamic steps
def min_conflicts(n, max_steps_multiplier=10, max_restarts=5):
    max_steps = max_steps_multiplier * n
    for restart in range(max_restarts):
        # generate a random initial board
        board = [random.randint(0, n - 1) for _ in range(n)]
        for steps in range(max_steps):
            heuristic = calculate_heuristic(board)
            if heuristic == 0:
                return board, heuristic, steps

            # select a random conflicted queen
            conflicted = [i for i in range(n) if sum(
                1 for j in range(n) if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j)
            ) > 1]
            if not conflicted:
                break

            col = random.choice(conflicted)
            min_conflicts_val = min(range(n), key=lambda row: calculate_heuristic(
                board[:col] + [row] + board[col + 1:]
            ))
            board[col] = min_conflicts_val

    return board, calculate_heuristic(board), max_steps * max_restarts

# run the algorithms and analyze results
def main():
    n = 8
    instances = 100

    # analyze hill climbing
    hill_climbing_solutions = 0
    hill_climbing_steps = 0
    hill_climbing_time = 0
    final_hill_climbing_solution = None
    for _ in range(instances):
        start_time = time.time()
        solution, heuristic, steps = hill_climbing(n)
        hill_climbing_time += time.time() - start_time
        hill_climbing_steps += steps
        if heuristic == 0:
            hill_climbing_solutions += 1
            final_hill_climbing_solution = solution

    print(f"hill climbing success rate: {hill_climbing_solutions / instances * 100}%")
    print(f"hill climbing average steps: {hill_climbing_steps / instances}")
    print(f"hill climbing average time: {hill_climbing_time / instances:.4f} seconds")
    if final_hill_climbing_solution:
        print("\nfinal hill climbing solution:")
        display_board(final_hill_climbing_solution)

    # analyze simulated annealing
    sa_solutions = 0
    sa_steps = 0
    sa_time = 0
    final_sa_solution = None
    for _ in range(instances):
        start_time = time.time()
        solution, heuristic, steps = simulated_annealing(n)
        sa_time += time.time() - start_time
        sa_steps += steps
        if heuristic == 0:
            sa_solutions += 1
            final_sa_solution = solution

    print(f"simulated annealing success rate: {sa_solutions / instances * 100}%")
    print(f"simulated annealing average steps: {sa_steps / instances}")
    print(f"simulated annealing average time: {sa_time / instances:.4f} seconds")
    if final_sa_solution:
        print("\nfinal simulated annealing solution:")
        display_board(final_sa_solution)

    # analyze min-conflicts
    mc_solutions = 0
    mc_steps = 0
    mc_time = 0
    final_mc_solution = None
    for _ in range(instances):
        start_time = time.time()
        solution, heuristic, steps = min_conflicts(n)
        mc_time += time.time() - start_time
        mc_steps += steps
        if heuristic == 0:
            mc_solutions += 1
            final_mc_solution = solution

    print(f"min-conflicts success rate: {mc_solutions / instances * 100}%")
    print(f"min-conflicts average steps: {mc_steps / instances}")
    print(f"min-conflicts average time: {mc_time / instances:.4f} seconds")
    if final_mc_solution:
        print("\nfinal min-conflicts solution:")
        display_board(final_mc_solution)

if __name__ == "__main__":
    main()
