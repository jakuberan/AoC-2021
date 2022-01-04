import numpy as np


def read_data(data_path):
    """
    Reads data
    """
    data = []
    f = open(data_path, "r")
    for x in f:
        data.append([1 if c == ">" else 2 if c == "v" else 0 for c in x.strip()])
    return np.array(data)


def move(data, east):
    """
    Performs move
    """
    if east:
        data = np.transpose(data)
        num = 1
    else:
        num = 2

    width = len(data)
    was_change = False
    data_new = data.copy()

    for idx in range(width):
        idx_new = 0 if (idx == (width - 1)) else idx + 1
        is_empty = data[idx_new] == 0
        to_move = data[idx] == num
        changed = is_empty & to_move
        data_new[idx][changed] = 0
        data_new[idx_new][changed] = num
        was_change = was_change | np.any(changed)

    if east:
        data_new = np.transpose(data_new)

    return data_new, was_change


if __name__ == "__main__":

    # Read data
    data_path = "input"
    data = read_data(data_path)

    # Run program
    was_change = True
    step = 0
    while was_change:
        data, was_change_east = move(data, east=True)
        data, was_change_south = move(data, east=False)
        was_change = was_change_east | was_change_south
        step += 1

    print(f"No move after {step} steps")
