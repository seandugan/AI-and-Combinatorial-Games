
def has_right_options(position: str) -> bool:
    """
    Returns True if Right (Frogs) has at least one valid move.
    Frogs move left: _F (step) or _TF (jump).
    """


    for i in range(len(position)):
        if position[i] == 'F':

            # previous cell is empty (step left)
            if i - 1 >= 0 and position[i - 1] == ' ':
                return True
            
            # previous cell is a Toad, cell before that is empty (jump left)
            if i - 2 >= 0 and position[i - 1] == 'T' and position[i - 2] == ' ':
                return True
            
    return False


def get_right_options(position: str) -> list:
    """
    Returns a list of all board positions reachable by Right (Frogs).
    Frogs move left: _F (step) or _TF (jump).
    """

    options = []

    for i in range(len(position)):
        if position[i] == 'F':


            # previous cell is empty (step left)
            if i - 1 >= 0 and position[i - 1] == ' ':
                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i - 1] = 'F'
                options.append(''.join(new_pos))


            # previous cell is a Toad, cell before that is empty (jump left)
            if i - 2 >= 0 and position[i - 1] == 'T' and position[i - 2] == ' ':
                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i - 2] = 'F'
                options.append(''.join(new_pos))


    return options


# Tests for has_right_options
assert has_right_options(' F') == True     # F can step left into empty
assert has_right_options(' TF') == True    # F can jump left over T
assert has_right_options('FTT') == False   # F blocked, no empty cell to left
print("All has_right_options tests passed!")


# Tests for get_right_options
assert get_right_options(' F') == ['F ']           # single step left
assert get_right_options(' TF') == ['FT ']         # single jump left
assert get_right_options('FT') == []               # F blocked on left edge
print("All get_right_options tests passed!")