import time


# Helper functions copied from daily 2 and daily 3.
# Toads ('T') move right.  Frogs ('F') move left.  ' ' is empty.
def get_left_options(position):
    """All positions reachable by Toads (move right)."""
    options = []
    for i in range(len(position)):
        if position[i] == 'T':
            # T_  ->  _T   (step right)
            if i + 1 < len(position) and position[i + 1] == ' ':
                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i + 1] = 'T'
                options.append(''.join(new_pos))
            # TF_ ->  _FT  (jump right over a Frog)
            if i + 2 < len(position) and position[i + 1] == 'F' and position[i + 2] == ' ':
                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i + 2] = 'T'
                options.append(''.join(new_pos))
    return options


def get_right_options(position):
    """All positions reachable by Frogs (move left)."""
    options = []
    for i in range(len(position)):
        if position[i] == 'F':
            # _F  ->  F_   (step left)
            if i - 1 >= 0 and position[i - 1] == ' ':
                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i - 1] = 'F'
                options.append(''.join(new_pos))
            # _TF ->  FT_  (jump left over a Toad)
            if i - 2 >= 0 and position[i - 1] == 'T' and position[i - 2] == ' ':
                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i - 2] = 'F'
                options.append(''.join(new_pos))
    return options



# Problem 1
# All possible Toads and Frogs positions of size n.
# Each cell is one of 'T', 'F', ' ' so there are 3**n positions.

def all_positions(n):
    if n == 0:
        return ['']
    smaller = all_positions(n - 1)
    result = []
    for pos in smaller:
        result.append(pos + 'T')
        result.append(pos + 'F')
        result.append(pos + ' ')
    return result



# Problem 2
# All positions of size n with exactly t Toads and f Frogs.
# At each step try putting 'T', 'F' or ' ' at the front 
# only if we still have room.

def positions_with_t_and_f(n, t, f):
    # impossible: too many pieces, or negative counts
    if t < 0 or f < 0 or t + f > n:
        return []
    # base case: empty board, only valid if t == 0 and f == 0
    if n == 0:
        return ['']

    result = []

    # put a 'T' first (only if we still need toads)
    if t > 0:
        for pos in positions_with_t_and_f(n - 1, t - 1, f):
            result.append('T' + pos)

    # put an 'F' first (only if we still need frogs)
    if f > 0:
        for pos in positions_with_t_and_f(n - 1, t, f - 1):
            result.append('F' + pos)

    # put a ' ' first (only if there is room for an empty)
    if n - t - f > 0:
        for pos in positions_with_t_and_f(n - 1, t, f):
            result.append(' ' + pos)

    return result



# Problem 3
# Build timing tables for problem 1 and problem 2.
# Stops automatically once a single iteration takes longer
# than 30 minutes

def time_problem_1(start_n=3, max_n=15):
    print("Problem 1: all positions of size n")
    print(" n  |    size     |  seconds")
    print("----+-------------+----------")
    for n in range(start_n, max_n + 1):
        start = time.time()
        positions = all_positions(n)
        elapsed = time.time() - start
        print(f" {n:<2} | {len(positions):>11} | {elapsed:.4f}")
        if elapsed > 1800:
            print("Stopping: last run exceeded 30 minutes.")
            break


def time_problem_2(start_n=3, max_n=20):
    print("Problem 2: positions with t = n//2 toads and f = n//2 frogs")
    print(" n  |  t  |  f  |    size     |  seconds")
    print("----+-----+-----+-------------+----------")
    for n in range(start_n, max_n + 1):
        t = n // 2
        f = n // 2
        start = time.time()
        positions = positions_with_t_and_f(n, t, f)
        elapsed = time.time() - start
        print(f" {n:<2} | {t:>3} | {f:>3} | {len(positions):>11} | {elapsed:.4f}")
        if elapsed > 1800:
            print("Stopping: last run exceeded 30 minutes.")
            break



# Problem 4
# Breadth-first search of the game tree starting at a given
# position. Use a 'visited' set so every position is counted exactly once.  
# Returns the total number of nodes visited.

def bfs_count(start_position):
    visited = set()
    visited.add(start_position)
    queue = [start_position]
    count = 0
    while len(queue) > 0:
        current = queue.pop(0)          # remove from the front
        count += 1
        children = get_left_options(current) + get_right_options(current)
        for child in children:
            if child not in visited:
                visited.add(child)
                queue.append(child)
    return count



# Problem 5
# Depth-first search.  Same idea as problem 4 but we use a
# stack instead of a queue.

def dfs_count(start_position):
    visited = set()
    visited.add(start_position)
    stack = [start_position]
    count = 0
    while len(stack) > 0:
        current = stack.pop()           # remove from the end
        count += 1
        children = get_left_options(current) + get_right_options(current)
        for child in children:
            if child not in visited:
                visited.add(child)
                stack.append(child)
    return count



# Tests
if __name__ == "__main__":

    # Problem 1 sanity checks: should be 3**n positions
    assert len(all_positions(0)) == 1
    assert len(all_positions(1)) == 3
    assert len(all_positions(2)) == 9
    assert len(all_positions(3)) == 27
    print("Problem 1 tests passed.")

    # Problem 2 sanity checks
    # n=2, t=1, f=1  -> 'TF', 'FT'                    -> 2
    assert len(positions_with_t_and_f(2, 1, 1)) == 2
    # n=3, t=1, f=1  -> 3 spots for T, then 2 for F   -> 6
    assert len(positions_with_t_and_f(3, 1, 1)) == 6
    # n=3, t=2, f=1  -> C(3,2)*C(1,1)                 -> 3
    assert len(positions_with_t_and_f(3, 2, 1)) == 3
    # impossible:    too many pieces                  -> 0
    assert len(positions_with_t_and_f(2, 2, 1)) == 0
    print("Problem 2 tests passed.")

    # Problem 4 / 5 sanity checks
    # 'TTFF' is fully blocked, no moves -> only 1 node visited
    assert bfs_count('TTFF') == 1
    assert dfs_count('TTFF') == 1
    # BFS and DFS visit the same set of nodes, so counts match
    for start in ['T F', 'TT FF', 'T  F', 'TF  ', '  TF']:
        assert bfs_count(start) == dfs_count(start)
    print("Problem 4/5 tests passed.")

    # A small demo of a real game tree size
    print(f"BFS from 'TT FF' visited {bfs_count('TT FF')} nodes.")
    print(f"DFS from 'TT FF' visited {dfs_count('TT FF')} nodes.")

    # Problem 3 timing tables
    print()
    time_problem_1(start_n=3, max_n=15)
    print()
    time_problem_2(start_n=3, max_n=20)
