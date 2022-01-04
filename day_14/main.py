import numpy as np


def read_data(data_path):
    """
    Reads data
    """
    line = 0
    insertions = {}
    f = open(data_path, "r")
    for x in f:
        if line == 0:
            template = x.strip()
        elif line > 1:
            ins = x.strip().split(" -> ")
            insertions[ins[0]] = ins[1]
        line += 1
    return insertions, template


def initialize(insertions, template):
    """
    Transition matrix and initial state
    """

    # Identify characters, set-up counter
    chars_ins = set(insertions.values())
    chars_tem = set([c for c in template])
    chars = chars_ins.union(chars_tem)
    chars_cnt = {c: 0 for c in chars}

    # Create empty transition matrix and state
    pairs = [c1 + c2 for c1 in chars for c2 in chars]
    trans = np.zeros((len(pairs), len(pairs)))
    state = np.zeros(len(pairs))

    # Fill in initial state
    for i in range(len(template) - 1):
        state[pairs.index(template[i : i + 2])] += 1

    # Fill in transition matrix
    for ins in insertions:
        row = pairs.index(ins)
        trans[row, pairs.index(ins[0] + insertions[ins])] += 1
        trans[row, pairs.index(insertions[ins] + ins[1])] += 1

    return state, trans, pairs, chars_cnt


if __name__ == "__main__":

    for part in [1, 2]:
        steps = 10 if part == 1 else 40

        # Read data
        data_path = "input"
        insertions, template = read_data(data_path)

        # Transition matrix and initial state
        state, trans, pairs, chars_cnt = initialize(insertions, template)

        # Iterate
        for i in range(steps):
            state = np.matmul(state, trans)

        # Count characters
        for i, cnt in enumerate(state):
            chars_cnt[pairs[i][0]] += cnt
            chars_cnt[pairs[i][1]] += cnt

        # Adjust for beginning and end
        chars_cnt[template[0]] += 1
        chars_cnt[template[-1]] += 1

        # Report outcome
        max_cnt = max(chars_cnt.values()) / 2
        min_cnt = min(chars_cnt.values()) / 2
        print(f"Result: {int(max_cnt - min_cnt)}")
