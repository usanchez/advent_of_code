"""
--- Day 12: Rain Risk ---
https://adventofcode.com/2020/day/12

Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

    Action N means to move north by the given value.
    Action S means to move south by the given value.
    Action E means to move east by the given value.
    Action W means to move west by the given value.
    Action L means to turn left the given number of degrees.
    Action R means to turn right the given number of degrees.
    Action F means to move forward by the given value in the direction the ship is currently facing.

The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11

These instructions would be handled as follows:

    F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
    N3 would move the ship 3 units north to east 10, north 3.
    F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
    R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
    F11 would move the ship 11 units south to east 17, south 8.

At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
--- Part Two ---

Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

    Action N means to move the waypoint north by the given value.
    Action S means to move the waypoint south by the given value.
    Action E means to move the waypoint east by the given value.
    Action W means to move the waypoint west by the given value.
    Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
    Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
    Action F means to move forward to the waypoint a number of times equal to the given value.

The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

For example, using the same instructions as above:

    F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
    N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
    F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
    R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
    F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.

After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?

"""
from copy import deepcopy

starting_state = [0, 0, 0]

instructions = []


def read_instruction(instruction):
    return instruction[:1], int(instruction[1:])


# read file
with open('input.txt') as f:
    for line in f:
        instructions.append(read_instruction(line.strip()))
del line, f


def get_manhattan_distance(first_state, second_state):
    x = second_state[0] - first_state[0]
    y = second_state[1] - first_state[1]
    return abs(x) + abs(y)


# Part one
def process_turn(current_degree, turn_direction, turn_degrees):
    multiplier = -1 if turn_direction == "R" else 1
    return (current_degree + (multiplier * turn_degrees)) % 360


def process_forward(x, y, current_degrees, move_units):
    if current_degrees == 0:
        x += move_units
    elif current_degrees == 90:
        y += move_units
    elif current_degrees == 180:
        x -= move_units
    elif current_degrees == 270:
        y -= move_units
    else:
        print("Unknown instruction")

    return x, y


def process_instruction_part_one(instruction, ship_state):
    if instruction[0] == "E":
        ship_state[0] = ship_state[0] + instruction[1]
    elif instruction[0] == "W":
        ship_state[0] = ship_state[0] - instruction[1]
    elif instruction[0] == "N":
        ship_state[1] = ship_state[1] + instruction[1]
    elif instruction[0] == "S":
        ship_state[1] = ship_state[1] - instruction[1]
    elif instruction[0] in ["R", "L"]:
        ship_state[2] = process_turn(ship_state[2], instruction[0], instruction[1])
    elif instruction[0] == "F":
        ship_state[0], ship_state[1] = process_forward(ship_state[0], ship_state[1], ship_state[2], instruction[1])
    else:
        print("Unknown instruction")

    return ship_state


current_state = deepcopy(starting_state)
for step in instructions:
    current_state = process_instruction_part_one(step, current_state)

print(get_manhattan_distance(starting_state, current_state))
del starting_state, current_state

# Part two

current_ship_state = [0, 0]
current_waypoint_state = [10, 1]


def move_waypoint(instruction, waypoint_state):
    if instruction[0] == "E":
        waypoint_state[0] = waypoint_state[0] + instruction[1]
    elif instruction[0] == "W":
        waypoint_state[0] = waypoint_state[0] - instruction[1]
    elif instruction[0] == "N":
        waypoint_state[1] = waypoint_state[1] + instruction[1]
    elif instruction[0] == "S":
        waypoint_state[1] = waypoint_state[1] - instruction[1]
    else:
        print("Unknown instruction")
    return waypoint_state


def move_ship(units, ship_state, waypoint_state):
    ship_state[0] += waypoint_state[0] * units
    ship_state[1] += waypoint_state[1] * units
    return ship_state


def rotate_waypoint(instruction, waypoint_state):
    degrees = instruction[1]
    turns = degrees / 90  # degrees / 90
    assert 0 < turns <= 3
    if turns % 2 == 1:
        # swap coords and change the sign of the first coord
        temp = waypoint_state[0]
        waypoint_state[0] = waypoint_state[1]
        waypoint_state[1] = temp
        multiplier = -1 if instruction[0] == "R" else 1
        if turns == 1:
            waypoint_state[0] = -multiplier * waypoint_state[0]
            waypoint_state[1] = multiplier * waypoint_state[1]
        elif turns == 3:
            waypoint_state[0] = multiplier * waypoint_state[0]
            waypoint_state[1] = -multiplier * waypoint_state[1]

    else:
        if turns == 2:
            # swap signs
            waypoint_state[0] = -waypoint_state[0]
            waypoint_state[1] = -waypoint_state[1]

    return waypoint_state


def process_instruction_part_two(instruction, ship_state, waypoint_state):
    if instruction[0] in ["N", "S", "E", "W"]:
        waypoint_state = move_waypoint(instruction, waypoint_state)
    elif instruction[0] in ["L", "R"]:
        waypoint_state = rotate_waypoint(instruction, waypoint_state)
    elif instruction[0] == "F":
        ship_state = move_ship(instruction[1], ship_state, waypoint_state)
    else:
        print("Unknown instruction")

    return ship_state, waypoint_state


for step in instructions:
    current_ship_state, current_waypoint_state = process_instruction_part_two(step, current_ship_state,
                                                                              current_waypoint_state)

print(get_manhattan_distance([0, 0], current_ship_state))
