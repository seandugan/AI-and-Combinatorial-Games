import time


# Helper functions copied from daily 2 and daily 3.
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
# Plain Min-Max search.
# Left (Toads) is the maximizing player, score +1 means Left wins.
# Right (Frogs) is the minimizing player, score -1 means Right wins.
# A player who cannot move loses (normal play).
def min_max_search(position, is_left_turn=True):

    # use a one-element list so the inner function can update it
    nodes = [0]

    def search(pos, left_turn):
        nodes[0] += 1

        if left_turn:
            options = get_left_options(pos)
            # Left has no moves -> Left loses
            if len(options) == 0:
                return -1, None

            best_score = -2          # smaller than any real score
            best_move = None
            for opt in options:
                result = search(opt, False)
                score = result[0]

                if score > best_score:
                    best_score = score
                    best_move = opt
                    
            return best_score, best_move

        else:
            options = get_right_options(pos)
            # Right has no moves -> Right loses
            if len(options) == 0:
                return 1, None

            best_score = 2           # larger than any real score
            best_move = None
            for opt in options:
                result = search(opt, True)
                score = result[0]

                if score < best_score:
                    best_score = score
                    best_move = opt

            return best_score, best_move

    score, best_move = search(position, is_left_turn)

    # Translate the +1 / -1 score into 'win' / 'loss' for the current player.
    if is_left_turn:
        result = 'win' if score == 1 else 'loss'
    else:
        result = 'win' if score == -1 else 'loss'

    return result, best_move, nodes[0]



# Problem 2
# Min-Max search with alpha-beta pruning.
# When beta <= alpha we can stop exploring the remaining siblings.
def alpha_beta_search(position, is_left_turn=True):

    nodes = [0]

    def search(pos, left_turn, alpha, beta):
        nodes[0] += 1

        if left_turn:
            options = get_left_options(pos)
            if len(options) == 0:
                return -1, None

            best_score = -2
            best_move = None

            for opt in options:
                result = search(opt, False, alpha, beta)
                score = result[0]
                
                if score > best_score:
                    best_score = score
                    best_move = opt
                if best_score > alpha:
                    alpha = best_score
                if beta <= alpha:
                    break            # prune the rest

            return best_score, best_move

        else:
            options = get_right_options(pos)
            if len(options) == 0:
                return 1, None

            best_score = 2
            best_move = None

            for opt in options:
                result = search(opt, True, alpha, beta)
                score = result[0]
                
                if score < best_score:
                    best_score = score
                    best_move = opt
                if best_score < beta:
                    beta = best_score
                if beta <= alpha:
                    break            # prune the rest

            return best_score, best_move
        

    score, best_move = search(position, is_left_turn, -2, 2)

    if is_left_turn:
        result = 'win' if score == 1 else 'loss'
    else:
        result = 'win' if score == -1 else 'loss'

    return result, best_move, nodes[0]



# Problem 3
# Test cases for both searches.
# For every starting position the two functions should agree on the
# 'result' and the 'best_move'.  Alpha-beta should visit no more nodes
# than plain min-max, and on at least one large board should visit far
# fewer.
if __name__ == "__main__":

    # Test 1: Left has no moves at all (loss for Left)
    # 'FFTT' = both Frogs are already left of both Toads,
    # no Toad has an empty cell to its right.
    result_mm, move_mm, nodes_mm = min_max_search('FFTT', True)
    result_ab, move_ab, nodes_ab = alpha_beta_search('FFTT', True)
    assert result_mm == 'loss'
    assert move_mm is None
    assert result_ab == 'loss'
    assert move_ab is None
    assert nodes_ab <= nodes_mm
    print(f"Test 1 (FFTT, Left to move): result={result_mm}, "
          f"mm_nodes={nodes_mm}, ab_nodes={nodes_ab}")



    # Test 2: tiny board with one forced move
    # 'T_F' : Left can step into the middle -> ' TF'
    # then Right must jump over the Toad   -> 'FT '
    # then Left has no moves               -> Left loses
    result_mm, move_mm, nodes_mm = min_max_search('T F', True)
    result_ab, move_ab, nodes_ab = alpha_beta_search('T F', True)
    assert result_mm == result_ab
    assert move_mm == move_ab
    assert nodes_ab <= nodes_mm
    print(f"Test 2 (T F, Left to move): result={result_mm}, "
          f"best_move='{move_mm}', mm_nodes={nodes_mm}, ab_nodes={nodes_ab}")



    # Test 3: Right to move first
    # Same board but Frogs go first.
    result_mm, move_mm, nodes_mm = min_max_search('T F', False)
    result_ab, move_ab, nodes_ab = alpha_beta_search('T F', False)
    assert result_mm == result_ab
    assert move_mm == move_ab
    assert nodes_ab <= nodes_mm
    print(f"Test 3 (T F, Right to move): result={result_mm}, "
          f"best_move='{move_mm}', mm_nodes={nodes_mm}, ab_nodes={nodes_ab}")



    # Test 4: standard 'TT_FF' start position
    # Normal Toads and Frogs opening with one empty in the middle.
    result_mm, move_mm, nodes_mm = min_max_search('TT FF', True)
    result_ab, move_ab, nodes_ab = alpha_beta_search('TT FF', True)
    assert result_mm == result_ab
    assert move_mm == move_ab
    assert nodes_ab <= nodes_mm
    print(f"Test 4 (TT FF, Left to move): result={result_mm}, "
          f"best_move='{move_mm}', mm_nodes={nodes_mm}, ab_nodes={nodes_ab}")



    # Test 5: extra empty in the middle, 'TT_ _FF'
    result_mm, move_mm, nodes_mm = min_max_search('TT  FF', True)
    result_ab, move_ab, nodes_ab = alpha_beta_search('TT  FF', True)
    assert result_mm == result_ab
    assert move_mm == move_ab
    assert nodes_ab <= nodes_mm
    print(f"Test 5 (TT  FF, Left to move): result={result_mm}, "
          f"best_move='{move_mm}', mm_nodes={nodes_mm}, ab_nodes={nodes_ab}")


    # Test 6 (LARGE): Showing a significant difference from pruning
    # 'TTT   FFF' has a deep game tree.  
    # Min-max will visit many nodes, but alpha-beta should prune most of them.
    start_position = 'TTT   FFF'

    t0 = time.time()
    result_mm, move_mm, nodes_mm = min_max_search(start_position, True)
    t_mm = time.time() - t0

    t0 = time.time()
    result_ab, move_ab, nodes_ab = alpha_beta_search(start_position, True)
    t_ab = time.time() - t0

    assert result_mm == result_ab
    assert nodes_ab <= nodes_mm
    print()
    print("Test 6 (LARGE): 'TTT   FFF', Left to move")
    print(f"  plain min-max : result={result_mm}, nodes={nodes_mm:>8}, "
          f"time={t_mm:.4f}s")
    print(f"  alpha-beta    : result={result_ab}, nodes={nodes_ab:>8}, "
          f"time={t_ab:.4f}s")
    print()
    print("All tests passed.")
