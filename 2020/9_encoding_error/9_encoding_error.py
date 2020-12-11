"""
--- Day 9: Encoding Error ---
https://adventofcode.com/2020/day/9

With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen in the seat in front of you.

Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).

The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an old cypher with an important weakness.

XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.

For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number must be the sum of two of those numbers:

    26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
    49 would be a valid next number, as it is the sum of 24 and 25.
    100 would not be valid; no two of the previous 25 numbers sum to 100.
    50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.

Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:

    26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
    65 would not be valid, as no two of the available numbers sum to it.
    64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.

Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576

In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.

The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?
--- Part Two ---

The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

Again consider the above example:

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576

In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)

To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?

"""

xmas_numbers = []

# read file
with open('input.txt') as f:
    for line in f:
        xmas_numbers.append(int(line.strip()))

# Part One
PREAMBLE_SIZE = 25


def do_two_preamble_numbers_sum_to_number(preamble, number):
    for n1 in range(0, len(preamble)):
        for n2 in range(n1 + 1, len(preamble)):
            if n1 != n2 and sum([preamble[n1], preamble[n2]]) == number:
                return True
    return False


def first_number_not_sum_of_previous_n(numbers):
    preamble_start = 0
    preamble_end = PREAMBLE_SIZE
    preamble = numbers[:PREAMBLE_SIZE]
    for number in numbers[PREAMBLE_SIZE:]:
        if not do_two_preamble_numbers_sum_to_number(preamble, number):
            return number
        preamble_start += 1
        preamble_end += 1
        preamble = numbers[preamble_start:preamble_end]


vulnerable_num = first_number_not_sum_of_previous_n(xmas_numbers)
print(vulnerable_num)


# Part Two

def check_them_sum_of_all_possible_n_contiguous_numbers(num_of_numbers_to_sum, numbers, obj_number,
                                                        latest_pos_of_num_lower_than_obj_number,
                                                        selected_numbers=None, total_sum=-1):
    if selected_numbers is None:
        selected_numbers = list()
    for start_pos in range(0, latest_pos_of_num_lower_than_obj_number - num_of_numbers_to_sum):
        end_pos = start_pos + num_of_numbers_to_sum
        selected_numbers = numbers[start_pos:end_pos]
        total_sum = sum(selected_numbers)
        if total_sum >= obj_number:
            return selected_numbers, total_sum, start_pos + num_of_numbers_to_sum - 1
    return selected_numbers, total_sum, latest_pos_of_num_lower_than_obj_number


def get_contiguous_numbers_that_sum_up_to_number(numbers, obj_number):
    num_of_numbers_to_sum = 2
    latest_possible_pos = len(numbers)
    selected_numbers = []
    total_sum = -1
    while total_sum != obj_number and num_of_numbers_to_sum <= len(numbers):
        selected_numbers, total_sum, latest_possible_pos = check_them_sum_of_all_possible_n_contiguous_numbers(
            num_of_numbers_to_sum, numbers, obj_number, latest_possible_pos)
        num_of_numbers_to_sum += 1
    return selected_numbers


def get_encryption_weakness(numbers, obj_number):
    contiguous_nums = get_contiguous_numbers_that_sum_up_to_number(numbers, obj_number)
    if contiguous_nums:
        return min(contiguous_nums) + max(contiguous_nums)
    else:
        return -1


print(get_encryption_weakness(xmas_numbers, vulnerable_num))
