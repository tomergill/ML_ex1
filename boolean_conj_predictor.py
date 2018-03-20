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
    """
    Get a data numpy matrix and the corresponding tags from the file.
    :param file_path: Path to a file holding the data and tags
    :return: X, Y where X is a numpy matrix where each row is an example, and Y is a numpy vector where each element
        is the tag of the corresponding row in X.
    """
    training_examples = np.loadtxt(file_path)
    X, Y = training_examples[:, :-1], training_examples[:, -1]
    return X, Y


def assign_example_to_hypothesis(t, h):
    """
    Puts the values of t in the variables of h.
    :param t: A d-sized numpy vector holding binary values that will be the input to h
    :param h: The hypothesis conjunction, with d variables. It is a d-sized numpy vector where the i-th cell holds the
        info for variable i: is it in h (LITERAL), is the negation in h (NEGATION), is both there (BOTH) or none of them
        are in h (NOT_IN).
    :return: The result of assigning t to h (True/False)
    """
    for i, x in enumerate(t):
        if h[i] == LITERAL and x == 0:
            return False
        elif h[i] == NEGATION and x == 1:
            return False
        elif h[i] == BOTH:
            return False
    return True


def consistency_algorithm(X, Y):
    """
    Applies the consistency algorithm.
    :param X: The data matrix, each row is an example.
    :param Y: The tags vector, each element is the appropriate row in X's tag
    :return: A vector describing the conjunction that is shared by the examples.
    """
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
    """
    Representing a result vector to a string describing the conjunction.
    :param result: A d-sized numpy vector where each element describes a variable in the conjunction (with values
        LITERAL/NEGATION/BOTH/NOT_IN).
    :return: A string where teh variable x_i is represented as "xi" and it's negation is "not(xi)". Conjunctions are
        represented with ",".
    """
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
    """
    Main function.
    Reads the data, applieng the consistency algorithm on it and receiving the conjunction and writing it to a file.
    :param input_file: Path to the data file, holding the data and the tags of the examples.
    :param output_file: Path to the output file to be created.
    :return: The output written to the file.
    """
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
    result = main(in_file, out_file)
    # print result
