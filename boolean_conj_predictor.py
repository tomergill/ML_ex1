"""
Name:        Tomer Gill
I.D.:        318459450
U2 Username: gilltom
Group:       89511-06
Date:        20/03/18
"""

import numpy as np
from sys import argv


LITERAL = 1.0  # if the i-th cell in h is LITERAL, then x_i is in the conjunction
NEGATION = 0.0  # likewise, but with not(x_i)
BOTH = -1.0  # both x_i and not(x_i) are in the conjunction
NOT_IN = np.nan  # neither x_i nor not(x_i) are in the conjunction


def get_X_and_Y_from_file(file_path):
    training_examples = np.loadtxt(file_path)
    X, Y = training_examples[:, :-1], training_examples[:, -1]
    return X, Y


def assign_example_to_hypothesis(t, h):
    for i, x in enumerate(t):
        if h[i] == LITERAL and x == 0:
            return False
        elif h[i] == NEGATION and x == 1:
            return False
        elif h[i] == BOTH:
            return False
    return True


def consistency_algorithm(X, Y):
    d = X.shape[1]
    h = np.array([BOTH] * d)  # the all-negative hypothesis
    for t, y in zip(X, Y):
        if y == 1 and not assign_example_to_hypothesis(t, h):  # our hypothesis is no good any more
            for i in xrange(t.shape[0]):
                if t[i] == 1:
                    if h[i] == NEGATION:
                        h[i] = NOT_IN
                    if h[i] == BOTH:
                        h[i] = LITERAL
                else:
                    if h[i] == LITERAL:
                        h[i] = NOT_IN
                    if h[i] == BOTH:
                        h[i] = NEGATION
    return h


def result_to_string(result):
    output = ""
    for i in xrange(result.shape[0]):
        if result[i] == LITERAL:
            output += "x{}".format(i+1)
        elif result[i] == NEGATION:
            output += "not(x{})".format(i+1)
        elif result[i] == BOTH:
            output += "x{},not(x{})".format(i+1, i+1)
        else:
            continue
        output += ","
    return output[:-1] if len(output) > 0 and output[-1] == "," else output


# Unorthodox in python, but helps not getting confused with same name parameters "><
def main(input_file, output_file):
    X, Y = get_X_and_Y_from_file(input_file)
    result = consistency_algorithm(X, Y)
    output = result_to_string(result)
    with open(output_file, "w") as out:
        out.write(output)
    return output


if __name__ == '__main__':
    in_file = "./data.txt"
    out_file = "./output.txt"
    if len(argv) > 1:
        in_file = argv[1]
    print main(in_file, out_file)
