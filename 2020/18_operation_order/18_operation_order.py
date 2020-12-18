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

"""

# Part one

total_sum = 0


def evaluate_operation(expression):
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



def evaluate_expression(expression):
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
            inner_expression = expression[innermost_open_parenth:innermost_close_parenth+1]
            result = evaluate_operation(expression[innermost_open_parenth + 1:innermost_close_parenth])
            expression = expression.replace(inner_expression, str(result))
            innermost_open_parenth = -1
            innermost_close_parenth = -1
        else:
            return evaluate_operation(expression)


print(evaluate_operation("1 + 6 + 44"))

with open('input.txt') as f:
    for line in f:
        total_sum += evaluate_expression(line.strip())
del line, f

print(total_sum)
