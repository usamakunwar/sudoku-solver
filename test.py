
from utils import *

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a,b):
    return [r+c for r in a for c in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#print(square_units)
unitlist = row_units + column_units + square_units
#print(unitlist)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

def grid_values(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

values = grid_values(grid2)
#print(values)
#print(row_units)

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values



def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

puzzle = reduce_puzzle(values)

def search(values):
    un_solved = dict((k,v) for k,v in values.items() if len(v) > 1)
    #print 'Unsolved :',len(un_solved)
    if len(un_solved) == 0:
        print("DONE")
        print display(values)
        return
    start = ()
    for k,v in un_solved.items():
        if not start or len(v) < len(start[1]):
            start = (k,v)
    #print 'Starting at',start

    for i in start[1]:
        print("Trying "+start[0]+" "+start[1]+" "+i)
        values[start[0]] = i

        newValues = reduce_puzzle(values.copy())
        if newValues:
            search(newValues)


search(puzzle)





# wanker = eliminate(values)
# print(values)
