import numpy as np


def read_data(data_path):
    """
    Reads data
    """
    f = open(data_path, "r")
    for x in f:
        target = x.strip().split("=")[1:]
        target = [a.replace(", y", "").split("..") for a in target]
        target = [[int(x) for x in target[0]], [int(y) for y in target[1]]]
    return target


def find_best_range(target):
    """
    Loop through all eligible ranges
    """
    cnt = 0
    height = 0
    for y_start in range(-target[1][0], target[1][0] - 1, -1):
        for x_start in range(target[0][1], 0, -1):
            y_step = -y_start - 1
            y = 0
            run = True
            if x_start >= 2 * y_start + 1:
                x_step = x_start - (2 * y_start + 1)
                x = (x_start - y_start) * (2 * y_start + 1)
            else:
                x_step = 0
                x = x_start * (x_start + 1) // 2
            while x <= target[0][1] and y >= target[1][0] and run:
                if x >= target[0][0] and y <= target[1][1]:
                    run = False
                    if cnt == 0:
                        height = y_start * (y_start + 1) // 2
                    cnt += 1
                x = x + x_step
                y = y + y_step
                x_step = 0 if x_step < 2 else x_step - 1
                y_step -= 1
                if x_step == 0 and x < target[0][0]:
                    run = False
    return height, cnt


if __name__ == "__main__":

    # Read data
    data_path = "input"
    target = read_data(data_path)

    # Perform steps of calculation
    height, cnt = find_best_range(target)
    print(f"Best probe reaches height {height}")
    print(f"There are {cnt} probes able to hit the target")
