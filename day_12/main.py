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


if __name__ == "__main__":

    # Read data
    data_path = "input"
    data = {}
    f = open(data_path, "r")
    for x in f:
        data = add_connection(data, x.strip().split("-"))

    for part in [1, 2]:
        total = search_next(data, path=["start"], part=part)
        print(f"There are {total} paths")
