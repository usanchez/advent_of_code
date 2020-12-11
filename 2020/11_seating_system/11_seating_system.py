"""
--- Day 11: Seating System ---
https://adventofcode.com/2020/day/11

Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##

This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##

#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##

#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##

At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
--- Part Two ---

As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....

The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

.............
.L.L.#.#.#.#.
.............

The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.

Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#

#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?

"""

from copy import deepcopy

seat_grid = []

# read file
with open('input.txt') as f:
    for line in f:
        seat_grid.append([c for c in line.strip()])

FLOOR = "."
EMPTY_SEAT_STATUS = "L"
OCCUPIED_SEAT_STATUS = "#"

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
]


def is_coord_in_grid(x_coord, y_coord, seat_matrix):
    if x_coord in range(0, len(seat_matrix)):
        if y_coord in range(0, len(seat_matrix[x_coord])):
            return True
    return False


def get_all_adjacent_coords(r, c, seat_matrix):
    adjacent_coords_template = [
        (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
        (r, c - 1), (r, c + 1),
        (r + 1, c - 1), (r + 1, c), (r + 1, c + 1),
    ]
    valid_adjacent_coords = []
    for idx, adjacent_coord in enumerate(adjacent_coords_template):
        if is_coord_in_grid(adjacent_coord[0], adjacent_coord[1], seat_matrix):
            valid_adjacent_coords.append(adjacent_coords_template[idx])
    return valid_adjacent_coords


def is_first_seat_in_direction_occupied(row, col, direction, seat_matrix):
    out_of_grid = False
    while not out_of_grid:
        row += direction[0]
        col += direction[1]
        if is_coord_in_grid(row, col, seat_matrix):
            seat_status = seat_matrix[row][col]
            if seat_status == OCCUPIED_SEAT_STATUS:
                return True
            elif seat_status == EMPTY_SEAT_STATUS:
                return False
        else:
            out_of_grid = True
    return False


def get_num_occupied_next_seats_in_any_direction(row, col, seat_matrix):
    num_occupied_seats = 0
    for direction in DIRECTIONS:
        num_occupied_seats += is_first_seat_in_direction_occupied(row, col, direction, seat_matrix)
    return num_occupied_seats


def get_num_occupied_adjacent_seats(coords_list, seat_matrix):
    num_occupied_adjacent_seats = 0
    for (r, c) in coords_list:
        if seat_matrix[r][c] == OCCUPIED_SEAT_STATUS:
            num_occupied_adjacent_seats += 1
    return num_occupied_adjacent_seats


def check_seat_state_change(row, col, seat_matrix, method):
    # Part one
    if method == "adjacent":
        coords_list = get_all_adjacent_coords(row, col, seat_matrix)
        num_occupied_seats = get_num_occupied_adjacent_seats(coords_list, seat_matrix)
    # Part two
    elif method == "first_seat":
        num_occupied_seats = get_num_occupied_next_seats_in_any_direction(row, col, seat_matrix)
    else:
        num_occupied_seats = 0
    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    if seat_matrix[row][col] == EMPTY_SEAT_STATUS and num_occupied_seats == 0:
        return OCCUPIED_SEAT_STATUS
    # Part one
    if method == "adjacent":
        max_tolerable_num_occupied_seats = 4
    # Part two
    elif method == "first_seat":
        max_tolerable_num_occupied_seats = 5
    else:
        max_tolerable_num_occupied_seats = 4
    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    if seat_matrix[row][col] == OCCUPIED_SEAT_STATUS and num_occupied_seats >= max_tolerable_num_occupied_seats:
        return EMPTY_SEAT_STATUS
    # Otherwise, the seat's state does not change.
    else:
        return seat_matrix[row][col]


def get_num_occupied_seats(seat_matrix):
    num_occupied_seats = 0
    for row in seat_matrix:
        num_occupied_seats += row.count(OCCUPIED_SEAT_STATUS)
    return num_occupied_seats


def print_grid(seat_matrix):
    print("seat_grid = [")
    for row in seat_matrix:
        print(row, ",")
    print("]")


def simulate_until_no_more_change(seat_matrix, method="adjacent"):
    num_seat_change = -1
    while num_seat_change != 0:
        num_seat_change = 0
        old_seat_grid = deepcopy(seat_matrix)

        for r, seat_row in enumerate(old_seat_grid):
            for c, _ in enumerate(seat_row):
                old_state = old_seat_grid[r][c]
                if old_state != FLOOR:
                    new_state = check_seat_state_change(r, c, old_seat_grid, method)
                    if old_state != new_state:
                        num_seat_change += 1
                        seat_matrix[r][c] = new_state
        print(num_seat_change)
    print(get_num_occupied_seats(seat_matrix))


# Part one
simulate_until_no_more_change(deepcopy(seat_grid), "adjacent")

# Part two
simulate_until_no_more_change(deepcopy(seat_grid), "first_seat")
