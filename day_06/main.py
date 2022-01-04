import numpy as np


def read_data(data_path):
    """
    Reads data
    """
    f = open(data_path, "r")
    for x in f:
        states_list = [int(a) for a in x.split(",")]

    return states_list


def init_matrix_state(states_list):
    """
    Initializes the transition matrix and the state
    """

    matrix = np.zeros((9, 9))
    state = np.zeros(9)

    # Fill in matrix
    matrix[0, 6] = 1
    matrix[0, 8] = 1
    for i in range(8):
        matrix[i + 1, i] = 1

    # Fill in initial conditions
    for i in range(9):
        state[i] = states_list.count(i)

    return matrix, state


if __name__ == "__main__":

    # Read data
    data_path = "input"
    states_list = read_data(data_path)

    # Get matrix and states
    matrix, state = init_matrix_state(states_list)

    # Iterate
    for i in range(256):
        state = np.matmul(state, matrix)

        if i in [79, 255]:
            print(f"There are {int(sum(state))} lanternfish at day {i+1}")
