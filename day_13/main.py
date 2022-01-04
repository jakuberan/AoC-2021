import numpy as np


def read_data(data_path, maxx=0, maxy=0):
    """
    Reads data
    """
    data = []
    read_status = 1
    folds = []
    f = open(data_path, "r")
    for x in f:
        if len(x.strip()) > 0:
            if read_status == 1:
                dot = x.strip().split(",")
                maxx = max(maxx, int(dot[0]))
                maxy = max(maxy, int(dot[1]))
                data.append((int(dot[1]), int(dot[0])))
            elif read_status == 2:
                a = x.strip().split()[-1].split("=")
                folds.append([a[0], int(a[1])])
        else:
            read_status = 2

    return folds, data, maxx, maxy


def fold_paper(paper, fold):
    """
    Performs a single fold
    """
    if fold[0] == "x":
        paper1 = paper[:, : fold[1]]
        paper2 = np.fliplr(paper[:, (fold[1] + 1) :])
        paper = paper1 + paper2
    else:
        paper1 = paper[: fold[1], :]
        paper2 = np.flipud(paper[(fold[1] + 1) :, :])
        paper = paper1 + paper2
    paper[paper > 1] = 1
    return paper


if __name__ == "__main__":

    # Read data
    data_path = "input"
    folds, data, maxx, maxy = read_data(data_path)

    # Initialize the array
    data = tuple(map(tuple, zip(*data)))
    paper = np.zeros((maxy + 1, maxx + 1))
    paper[data] = 1

    # Fold once
    paper = fold_paper(paper, folds[0])
    print(f"There are {int(sum(sum(paper)))} dots visible after the first fold")

    # Perform all remaining folds and print output
    for fold in folds[1:]:
        paper = fold_paper(paper, fold)

    # Print output
    for i in range(len(paper)):
        print("".join(["#" if int(b) == 1 else "." for b in paper[i]]))
