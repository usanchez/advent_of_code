"""
--- Day 18: Operation Order ---
https://adventofcode.com/2020/day/18

As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71

Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51

Here are a few more examples:

    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?
--- Part Two ---

You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231

Here are the other examples from above:

    1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
    2 * 3 + (4 * 5) becomes 46.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

What do you get if you add up the results of evaluating the homework problems using these new rules?

"""

expressions = []

with open('input.txt') as f:
    for line in f:
        expressions.append(line.strip())
del line, f


def evaluate_expression(expression, part="one"):
    innermost_open_parenth = -1
    innermost_close_parenth = -1
    while True:
        for idx, c in enumerate(expression):
            if c == "(":
                innermost_open_parenth = idx
            elif c == ")":
                innermost_close_parenth = idx
                break
        if innermost_open_parenth > -1 and innermost_close_parenth > -1:
            inner_expression = expression[innermost_open_parenth:innermost_close_parenth + 1]
            if part == "one":
                result = evaluate_operation_part_one(expression[innermost_open_parenth + 1:innermost_close_parenth])
            else:
                result = evaluate_operation_part_two(expression[innermost_open_parenth + 1:innermost_close_parenth])
            expression = expression.replace(inner_expression, str(result))
            innermost_open_parenth = -1
            innermost_close_parenth = -1
        else:
            if part == "one":
                return evaluate_operation_part_one(expression)
            else:
                return evaluate_operation_part_two(expression)


# Part one


def evaluate_operation_part_one(expression):
    result = 0
    nums = [None, None]
    operation = None
    for c in expression.split(" "):
        if c not in ["*", "+"]:
            num = int(c)
            if nums[0] is None:
                nums[0] = num
            elif operation is not None:
                nums[1] = num
                if operation == "*":
                    result = nums[0] * nums[1]
                elif operation == "+":
                    result = nums[0] + nums[1]
                operation = None
                nums = [result, None]
        else:
            operation = c
    return nums[0]


total_sum = 0

for line in expressions:
    total_sum += evaluate_expression(line.strip())

print(total_sum)


# Part two

def evaluate_operation_part_two(expression):
    result = 0
    nums = [None, None]
    operation = None
    operation_elements = expression.split(" ")

    # Perform sums first
    idx_sums = [idx for idx, elem in enumerate(operation_elements) if elem == "+"]

    while idx_sums:
        i = idx_sums[0]
        second_num = operation_elements.pop(i + 1)
        first_num = operation_elements.pop(i - 1)
        operation_elements[i - 1] = int(first_num) + int(second_num)
        idx_sums = [idx for idx, elem in enumerate(operation_elements) if elem == "+"]

    # Perform the rest of operations
    for c in operation_elements:
        if c not in ["*", "+"]:
            num = int(c)
            if nums[0] is None:
                nums[0] = num
            elif operation is not None:
                nums[1] = num
                if operation == "*":
                    result = nums[0] * nums[1]
                elif operation == "+":
                    result = nums[0] + nums[1]
                operation = None
                nums = [result, None]
        else:
            operation = c
    return nums[0]


total_sum = 0

for line in expressions:
    total_sum += evaluate_expression(line.strip(), "two")

print(total_sum)
