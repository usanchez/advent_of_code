"""
--- Day 1: Report Repair ---
https://adventofcode.com/2020/day/1

After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.
To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?


--- Part Two ---

The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?

"""

input_numbers = []
REQUIRED_SUM_VALUE = 2020

# read file
with open('input.txt') as f:
    for line in f:
        number = int(line)
        if number <= REQUIRED_SUM_VALUE:
            input_numbers.append(int(line))

print(len(input_numbers))


def multiply_number_list(num_list):
    total_value = 1
    for element in num_list:
        total_value *= element
    return total_value


# FAST DEVELOPED CUSTOM SOLUTIONS

# Part One
def get_multiplication_of_two_numbers_that_add_up_to_2020(num_list):
    len_input = len(num_list)
    iteration_count = 0
    for i in range(0, len_input):
        for j in range(i + 1, len_input):
            element_list = [num_list[i], num_list[j]]
            if sum(element_list) == REQUIRED_SUM_VALUE:
                print(f"iteration count: {iteration_count}")
                return multiply_number_list(element_list)
            iteration_count += 1


print(get_multiplication_of_two_numbers_that_add_up_to_2020(input_numbers))


# Part Two
def get_multiplication_of_three_numbers_that_add_up_to_2020(num_list):
    len_input = len(num_list)
    iteration_count = 0
    for i in range(0, len_input):
        for j in range(i, len_input):
            element_list = [num_list[i], num_list[j]]
            if sum(element_list) >= REQUIRED_SUM_VALUE:
                continue
            for k in range(j, len_input):
                element_list = [num_list[i], num_list[j], num_list[k]]
                if sum(element_list) == REQUIRED_SUM_VALUE:
                    print(f"iteration count: {iteration_count}")
                    return multiply_number_list(element_list)
                iteration_count += 1


print(get_multiplication_of_three_numbers_that_add_up_to_2020(input_numbers))


# SOLUTION FOR ANY N OF SET OF VALUES (can be improved)

def get_index_to_increase_if_sum_does_not_add_up_to_required_value(element_list):
    total_value = 0
    for index, element in enumerate(element_list):
        total_value += element
        if total_value >= REQUIRED_SUM_VALUE and index != len(element_list) - 1:
            return index
    if total_value == REQUIRED_SUM_VALUE:
        return -1
    else:
        return len(element_list) - 1


def update_numbers_indexes(numbers_indexes, index_to_increase, len_input):
    for index in range(index_to_increase, -1, -1):
        # we check if we would overflow current index if we increase it
        if numbers_indexes[index] + 1 < len_input:
            # if not, we increase it, increase the other indices too and we exit
            numbers_indexes[index] += 1
            for other_index in range(index + 1, len(numbers_indexes)):
                if numbers_indexes[other_index - 1] + 1 < len_input:
                    numbers_indexes[other_index] = numbers_indexes[other_index - 1] + 1
            return 0
        else:
            # if so:
            if index > 0:
                # if we are not in the latest index we go to the next index
                continue
            else:
                # otherwise, we just return overflow error, there won't be any possible good values
                return -1


def get_multiplication_of_n_numbers_that_add_up_to_required_value(num_list, n) -> int:
    if n == 1:
        return REQUIRED_SUM_VALUE if REQUIRED_SUM_VALUE in num_list else -1
    elif n == 0:
        return -1
    iteration_count = 0
    final_value = -1
    len_input = len(num_list)
    # initialization of number indexes
    numbers_indexes = [i for i in range(0, n)]
    while 1:
        # create list of numbers to be checked
        element_list = [num_list[numbers_index] for numbers_index in numbers_indexes]
        # check which index to increment (-1 the answer is correct)
        index_to_increase = get_index_to_increase_if_sum_does_not_add_up_to_required_value(element_list)
        if index_to_increase == -1:
            # we return the value
            final_value = multiply_number_list(element_list)
            break
        else:
            # check if we would go out of bounds
            if update_numbers_indexes(numbers_indexes, index_to_increase, len_input) == -1:
                final_value = -1
                break
        iteration_count += 1
    print(f"iteration count: {iteration_count}")
    return final_value


# Part One
print(get_multiplication_of_n_numbers_that_add_up_to_required_value(input_numbers, 2))
# Part Two
print(get_multiplication_of_n_numbers_that_add_up_to_required_value(input_numbers, 3))
