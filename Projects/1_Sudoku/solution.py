
from utils import *
import itertools


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_1 = [r + c for r, c in zip(rows, cols)]
diag_2 = [r + c for r, c in zip(rows, cols[::-1])] # slice and step backward -1
diagonal_units = [diag_1, diag_2]
# diagonal_units = [[rows[i] + cols[i] for i in range(9)], [rows[::-1][i] + cols[i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diagonal_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)



    
    # TODO: Implement this function!
    


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        if values:
            values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def naked_twins_islam(values):
    new_sudoko = values.copy()
    applicable = 0
    for key in values.keys():
        if len(values[key]) == 2:
            applicable = applicable + 1
    if applicable > 2:
        for box_a in values.keys():
            for box_b in peers[box_a]:
                if values[box_a] == values[box_b] and len(values[box_a]) == 2 and len(values[box_b]) == 2:
                    intersect = [int_sect for int_sect in peers[box_a] if int_sect in peers[box_b]]
                    for peer in intersect:
                        for digit in values[box_a]:
                            new_sudoko[peer] = new_sudoko[peer].replace(digit, '')
    return new_sudoko

def naked_twins_sedar(values):
    for unit in unitlist:
    # Find all boxes with two digits remaining as possibilities
        pairs = [box for box in unit if len(values[box]) == 2]
    # Pairwise combinations
        poss_twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
        for pair in poss_twins:
            box1 = pair[0]
            box2 = pair[1]
        # Find the naked twins
            if values[box1] == values[box2]:
                for box in unit:
        # Eliminate the naked twins as possibilities for peers
                    if box != box1 and box != box2:
                        for digit in values[box1]:
                            values[box] = values[box].replace(digit,'')
    return values

def naked_twins(values):
    for unit in unitlist:
        twins = [box for box in unit if len(values[box]) == 2]
        poss_twins = [list(pair) for pair in itertools.combinations(twins, 2)]
        for item in poss_twins:
            box_a = item[0]
            box_b = item[1]
            if values[box_a] == values[box_b]:
                for box in unit:
                    if box != box_a and box != box_b:
                        for num in values[box_a]:
                            values[box] = values[box].replace(num, '')
    return values



def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt




def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
