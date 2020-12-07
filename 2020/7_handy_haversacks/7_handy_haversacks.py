"""
--- Day 7: Handy Haversacks ---
https://adventofcode.com/2020/day/7

You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

    A bright white bag, which can hold your shiny gold bag directly.
    A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
    A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
    A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.

So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
--- Part Two ---

It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

    faded blue bags contain 0 other bags.
    dotted black bags contain 0 other bags.
    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?

"""


def get_bags_and_values_dict(bag_quantities_str):
    if bag_quantities_str == "no other bags.":
        return {}
    bag_quantities_str = bag_quantities_str.replace(".", "").replace(" bags", "").replace(" bag", "").strip()
    bags_quantities = bag_quantities_str.split(", ")
    bag_quantity_dict = {}
    for bag_quantity in bags_quantities:
        bag_name = ''.join([c for c in bag_quantity if not c.isdigit()]).strip()
        value = int(bag_quantity.replace(bag_name, "").strip())
        bag_quantity_dict[bag_name] = value
    return bag_quantity_dict


def add_rule(rule, rule_dict):
    rule_key_value = rule.split(" bags contain ")
    rule_dict[rule_key_value[0]] = get_bags_and_values_dict(rule_key_value[1])

    return rule_dict


rules = {}

# read file
with open('input.txt') as f:
    for line in f:
        rules = add_rule(line.strip(), rules)

# Part One
possible_bag_colors = set()
bags_to_find = ["shiny gold"]

new_added = 1
while new_added > 0:
    new_added = 0
    for bag_to_find in bags_to_find:
        for key, values in rules.items():
            if bag_to_find in values and key not in possible_bag_colors and key not in bags_to_find:
                possible_bag_colors.add(key)
                bags_to_find.append(key)
                new_added += 1

print(len(possible_bag_colors))


# Part Two

def compute_required_bags(bag_name, level=0):
    total_bags = 1

    if rules[bag_name] != {}:
        for key, value in rules[bag_name].items():
            total_bags += value * compute_required_bags(key, level=level + 1)
    if level == 0:
        # if we are on the first 'level' we subtract 1 from the count because we do not count the original bag itself
        return total_bags - 1
    return total_bags


print(compute_required_bags("shiny gold"))
