"""
--- Day 17: Conway Cubes ---
https://adventofcode.com/2020/day/17

As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following rules:

    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###

Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......

After the full six-cycle boot process completes, 112 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?
"""
from copy import deepcopy

NUM_CYCLES = 6
ACTIVE_STATE = "#"
INACTIVE_STATE = "."


def change_state(current_state, matrix, current_pos, dims=3):
    num_active_neighbours = get_num_active_neighbours(matrix, current_pos, dims)
    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    if current_state == ACTIVE_STATE:
        if num_active_neighbours in [2, 3]:
            return ACTIVE_STATE
        else:
            return INACTIVE_STATE

    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
    elif current_state == INACTIVE_STATE:
        if num_active_neighbours == 3:
            return ACTIVE_STATE
        else:
            return INACTIVE_STATE


# Part one
DIRECTIONS_PART_ONE = [
    # z - 1
    (-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
    (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
    (-1, 1, -1), (-1, 1, 0), (-1, 1, 1),
    # z 0
    (0, -1, -1), (0, -1, 0), (0, -1, 1),
    (0, 0, -1), (0, 0, 1),
    (0, 1, -1), (0, 1, 0), (0, 1, 1),
    # z + 1
    (1, -1, -1), (1, -1, 0), (1, -1, 1),
    (1, 0, -1), (1, 0, 0), (1, 0, 1),
    (1, 1, -1), (1, 1, 0), (1, 1, 1),
]

pocket_dimension = [[]]

with open('input.txt') as f:
    for line in f:
        pocket_dimension[0].append(list(line.strip()))
del line, f


def print_pocket_dimension(dims=3):
    if dims == 3:
        for z_dim, _ in enumerate(pocket_dimension):
            print("z=", z_dim)
            for state_line in pocket_dimension[z_dim]:
                print(state_line)
    elif dims == 4:
        for z_dim, _ in enumerate(pocket_dimension):
            for y_dim, _ in enumerate(pocket_dimension[z_dim]):
                print("z=", z_dim, "y=", y_dim)
                for state_line in pocket_dimension[z_dim][y_dim]:
                    print(state_line)


def expand_pocket_dimension(matrix, dims=3):
    if dims == 3:
        # add two new x dims (at start and end)
        for z, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[z]):
                matrix[z][y].insert(0, ".")
                matrix[z][y].append(".")

        # add two new y dims (at start and end)
        for z, _ in enumerate(matrix):
            matrix[z].insert(0, [INACTIVE_STATE for _ in range(0, len(matrix[z][0]))])
            matrix[z].append([INACTIVE_STATE for _ in range(0, len(matrix[z][0]))])

        # add two new z dims (at start and end)
        matrix.insert(0, [[INACTIVE_STATE for _ in range(0, len(matrix[0][0]))] for _ in range(0, len(matrix[0]))])
        matrix.append([[INACTIVE_STATE for _ in range(0, len(matrix[0][0]))] for _ in range(0, len(matrix[0]))])

    if dims == 4:
        # add two new w dims (at start and end)
        for z, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[z]):
                for x, _ in enumerate(matrix[z][y]):
                    matrix[z][y][x].insert(0, ".")
                    matrix[z][y][x].append(".")

        # add two new x dims (at start and end)
        inactive_state_line = [INACTIVE_STATE for _ in range(0, len(matrix[0][0][0]))]
        for z, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[z]):
                matrix[z][y].insert(0, deepcopy(inactive_state_line))
                matrix[z][y].append(deepcopy(inactive_state_line))

        # add two new y dims (at start and end)
        inactive_state_matrix = [deepcopy(inactive_state_line) for _ in range(0, len(matrix[0][0]))]
        for z, _ in enumerate(matrix):
            matrix[z].insert(0, deepcopy(inactive_state_matrix))
            matrix[z].append(deepcopy(inactive_state_matrix))

        # add two new z dims (at start and end)
        inactive_state_cube = [deepcopy(inactive_state_matrix) for _ in range(0, len(matrix[0]))]
        matrix.insert(0, deepcopy(inactive_state_cube))
        matrix.append(deepcopy(inactive_state_cube))


def is_pos_valid(other_pos, matrix, dims=3):
    if dims == 3:
        return ((0 < other_pos[0] < len(matrix)) and
                (0 < other_pos[1] < len(matrix[0])) and
                (0 < other_pos[2] < len(matrix[0][0])))
    elif dims == 4:
        return ((0 < other_pos[0] < len(matrix)) and
                (0 < other_pos[1] < len(matrix[0])) and
                (0 < other_pos[2] < len(matrix[0][0])) and
                (0 < other_pos[3] < len(matrix[0][0][0])))


def get_num_active_neighbours(matrix, current_pos, dims=3):
    num_active = 0

    if dims == 3:
        for direction in DIRECTIONS_PART_ONE:
            other_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1], current_pos[2] + direction[2])
            if is_pos_valid(other_pos, matrix):
                other_state = matrix[other_pos[0]][other_pos[1]][other_pos[2]]
                num_active += other_state == ACTIVE_STATE
    elif dims == 4:
        for z in range(current_pos[0] - 1, current_pos[0] + 2):
            for y in range(current_pos[1] - 1, current_pos[1] + 2):
                for x in range(current_pos[2] - 1, current_pos[2] + 2):
                    for w in range(current_pos[3] - 1, current_pos[3] + 2):
                        other_pos = (z, y, x, w)
                        if other_pos != current_pos and is_pos_valid(other_pos, matrix, dims):
                            other_state = matrix[other_pos[0]][other_pos[1]][other_pos[2]][other_pos[3]]
                            num_active += other_state == ACTIVE_STATE
    return num_active


def change_states(matrix, dims=3):
    # for every cell, check its 3D neighbours and change the state accordingly
    new_state = deepcopy(matrix)
    if dims == 3:
        for z, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[z]):
                for x, _ in enumerate(matrix[z][y]):
                    current_pos = (z, y, x)
                    new_state[z][y][x] = change_state(matrix[z][y][x], matrix, current_pos)
    elif dims == 4:
        for z, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[z]):
                for x, _ in enumerate(matrix[z][y]):
                    for w, _ in enumerate(matrix[z][y][x]):
                        current_pos = (z, y, x, w)
                        new_state[z][y][x][w] = change_state(matrix[z][y][x][w], matrix, current_pos, 4)
    return new_state


def count_num_active(matrix, dims=3):
    num_active = 0
    if dims == 3:
        for z, _ in enumerate(matrix):
            for x in matrix[z]:
                num_active += sum([c == ACTIVE_STATE for c in x])
    elif dims == 4:
        for z, _ in enumerate(matrix):
            for y, _ in enumerate(matrix[z]):
                for x in matrix[z][y]:
                    num_active += sum([c == ACTIVE_STATE for c in x])
    return num_active


for cycle in range(0, NUM_CYCLES):
    expand_pocket_dimension(pocket_dimension)
    pocket_dimension = change_states(pocket_dimension)

print(count_num_active(pocket_dimension))

# Part two

pocket_dimension = [[[]]]

with open('input.txt') as f:
    for line in f:
        pocket_dimension[0][0].append(list(line.strip()))
del line, f


for cycle in range(0, NUM_CYCLES):
    expand_pocket_dimension(pocket_dimension, 4)
    pocket_dimension = change_states(pocket_dimension, 4)

print(count_num_active(pocket_dimension, 4))
