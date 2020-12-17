"""
--- Day 16: Ticket Translation ---

As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'

Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12

It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
--- Part Two ---

Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9

Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?

"""

# Part one

line_num = 0
rules = {}
ticket_scanning_error_rate = 0


def process_field(field_line):
    field_splits = field_line.split(": ")
    field_dict = {
        "name": field_splits[0]
    }
    ranges = field_splits[1].strip().split(" or ")
    field_dict["low_range"] = [int(val) for val in ranges[0].strip().split("-")]
    field_dict["high_range"] = [int(val) for val in ranges[1].strip().split("-")]
    return field_dict


def process_ticket_line(ticket_line):
    return [int(val.strip()) for val in ticket_line.split(",")]


def is_value_in_ranges(value, rule_ranges):
    return 1 if (rule_ranges[0][0] <= value <= rule_ranges[0][1] or rule_ranges[1][0] <= value <= rule_ranges[1][
        1]) else 0


def is_value_correct(value, rules_dict):
    return any([is_value_in_ranges(value, rule_ranges) for rule_name, rule_ranges in rules_dict.items()])


def check_ticket(ticket, rules_dict):
    ticket_values_errors_list = [not is_value_correct(ticket_value, rules_dict) for ticket_value in ticket]
    sum_invalid_values = sum(
        [ticket[value_idx] for value_idx, value_has_errors in enumerate(ticket_values_errors_list) if value_has_errors])
    return sum_invalid_values, any(ticket_values_errors_list)


valid_nearby_tickets = []

with open('input.txt') as f:
    for line in f:
        line_str = line.strip()
        if 0 <= line_num < 20:
            # read field line
            field = process_field(line_str)
            rules[field["name"]] = (field["low_range"], field["high_range"])
        elif line_num == 22:
            # process my ticket
            my_ticket = process_ticket_line(line_str)

        elif line_num >= 25:
            # process other tickets
            ticket_value_list = process_ticket_line(line_str)
            ticket_scanning_error, has_errors = check_ticket(ticket_value_list, rules)
            if has_errors:
                ticket_scanning_error_rate += ticket_scanning_error
            else:
                valid_nearby_tickets.append(ticket_value_list)
        line_num += 1
del line, f

print(ticket_scanning_error_rate)


# Part two

def is_value_correct(ticket_value, rule_ranges):
    return 1 if (rule_ranges[0][0] <= ticket_value <= rule_ranges[0][1] or
                 rule_ranges[1][0] <= ticket_value <= rule_ranges[1][1]) else 0


def get_field_order(tickets, rules_dict):
    num_tickets = len(tickets)
    num_values = len(tickets[0])
    range_vals = range(0, num_values)

    field_order = ["" for _ in range_vals]

    # initialize scores
    scores = {rule_name: [0 for _ in range_vals] for rule_name, rules_ranges in rules_dict.items()}
    for rule_name, rules_ranges in rules_dict.items():
        for score_idx, _ in enumerate(scores):
            for ticket in tickets:
                scores[rule_name][score_idx] += is_value_correct(ticket[score_idx], rules_ranges)

    num_rules_correct = compute_rules_scores(num_tickets, range_vals, scores)

    print_rules_scores(num_rules_correct, range_vals, scores)
    # try to get as many rules in place
    field_restricted_to_idx = [total_score == 1 for total_score in num_rules_correct]
    while any(field_restricted_to_idx):
        for field_idx, is_restricted in enumerate(field_restricted_to_idx):
            if is_restricted:
                for field_name, score_list in scores.items():
                    if score_list[field_idx] == num_tickets:
                        field_order[field_idx] = field_name
                        scores.pop(field_name, None)
                        num_rules_correct = compute_rules_scores(num_tickets, range_vals, scores)
                        print_rules_scores(num_rules_correct, range_vals, scores)
                        break
        field_restricted_to_idx = [total_score == 1 for total_score in num_rules_correct]
    return field_order


def print_rules_scores(num_rules_correct, range_vals, scores):
    # print scores
    print(f"{'field index'.rjust(18)}: ", end='')
    print([str(s).rjust(3) for s in range_vals])
    for field_name, score_list in scores.items():
        print(f"{field_name.rjust(18)}: ", end='')
        print([str(s).rjust(3) for s in score_list])
    print(f"{'num rules correct'.rjust(18)}: ", end='')
    print([str(s).rjust(3) for s in num_rules_correct])


def compute_rules_scores(num_tickets, range_vals, scores):
    num_rules_correct = [sum([1 for field_name, score_list in scores.items() if score_list[value_idx] == num_tickets])
                         for value_idx
                         in range_vals]
    return num_rules_correct


field_name_order = get_field_order(valid_nearby_tickets, rules)

departure_multiplication = 1

for idx, value in enumerate(my_ticket):
    if field_name_order[idx].startswith("departure"):
        departure_multiplication *= value
print(departure_multiplication)
