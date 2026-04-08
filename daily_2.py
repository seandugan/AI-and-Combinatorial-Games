
def has_left_options(position: str) -> bool:
    """
    Returns True if Left (Toads) has at least one valid move.
    Toads move right: T_ (step) or TF_ (jump).
    """

    for i in range(len(position)):
        if position[i] == 'T':

            # next cell is empty
            if i + 1 < len(position) and position[i + 1] == ' ':
                return True
            
            # next cell is a Frog, cell after is empty
            if i + 2 < len(position) and position[i + 1] == 'F' and position[i + 2] == ' ':
                return True
            
    return False


def get_left_options(position: str) -> list:
    """
    Returns a list of all board positions reachable by Left (Toads).
    Toads move right: T_ (step) or TF_ (jump).
    """

    options = []

    for i in range(len(position)):
        if position[i] == 'T':

            # next cell is empty
            if i + 1 < len(position) and position[i + 1] == ' ':

                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i + 1] = 'T'
                options.append(''.join(new_pos))


            # next cell is a Frog, cell after is empty
            if i + 2 < len(position) and position[i + 1] == 'F' and position[i + 2] == ' ':


                new_pos = list(position)
                new_pos[i] = ' '
                new_pos[i + 2] = 'T'
                options.append(''.join(new_pos))

    return options


# Tests for has_left_options
assert has_left_options('T F') == True
assert has_left_options('TF ') == True
assert has_left_options('TFF') == False
print("All has_left_options tests passed!")

# Tests for get_left_options
assert get_left_options('T F') == [' TF']
assert get_left_options('TF ') == [' FT']
assert get_left_options('TFF') == []
print("All get_left_options tests passed!")