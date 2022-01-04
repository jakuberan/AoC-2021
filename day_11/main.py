import numpy as np
from numpy import asarray as ar


def read_data(data_path):
    """
    Reads data
    """
    data = []
    f = open(data_path, "r")
    for x in f:
        data.append([int(c) for c in x.strip()])

    # Convert to numpy and return
    return np.array(data)


def do_step(data, l=10):
    cnt = 0
    data = data + 1
    while sum(sum(data > 9)) > 0:
        cnt += sum(sum(data > 9))
        indices10 = np.where(data > 9)
        data[np.where(data > 9)] = -100
        for (i, j) in list(zip(*indices10)):
            ia = (
                np.array([i - 1, i - 1, i - 1, i, i, i + 1, i + 1, i + 1]),
                np.array([j - 1, j, j + 1, j - 1, j + 1, j - 1, j, j + 1]),
            )
            keep = ar(ia[0] >= 0) & ar(ia[1] >= 0) & ar(ia[0] < l) & ar(ia[1] < l)
            indices_clean = (ia[0][keep], ia[1][keep])
            data[indices_clean] += 1
    data[np.where(data < 0)] = 0
    return data, cnt


if __name__ == "__main__":

    # Read data
    data_path = "input"
    data = read_data(data_path)
    dim = len(data)

    steps = 100
    count = 0
    for i in range(steps):
        data, count_step = do_step(data, l=dim)
        count += count_step

    print(f"There were {count} flashes after {steps} steps")

    count = 0
    step = 100
    while count < 100:
        step += 1
        data, count = do_step(data, l=dim)

    print(f"All octopuses flash simultaneously in step {step}")
