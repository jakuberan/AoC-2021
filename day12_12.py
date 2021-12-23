import numpy as np
from numpy import asarray as ar

# Define path
data_path = "data/input12"
data = {}
part = 2


def add_connection(data, connection):
    for i in range(2):
        if connection[i] in data.keys():
            data[connection[i]].append(connection[1 - i])
        else:
            data[connection[i]] = [connection[1 - i]]

    return data


def eligible_node(node, path, part):
    if node == "start":
        return False, part
    if node not in path:
        return True, part
    else:
        if node.upper() == node:
            return True, part
        elif part == 2 and path.count(node) <= 1:
            return True, 1
    return False, part


def search_next(data, path, part):
    if path[-1] == "end":
        return 1
    total = 0
    path.append("")
    for node in data[path[-2]]:
        is_eligible, new_part = eligible_node(node, path, part)
        if is_eligible:
            path[-1] = node
            total += search_next(data, path.copy(), new_part)

    return total


# Read line-by-line
f = open(data_path, "r")
for x in f:
    data = add_connection(data, x.strip().split("-"))

total = search_next(data, path=["start"], part=part)

print(f"There are {total} paths")
