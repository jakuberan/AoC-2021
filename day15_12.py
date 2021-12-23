import numpy as np

# Define path
data_path = "data/input15"

# Define parameters
data = []
part = 2

# Read line-by-line
f = open(data_path, "r")
for x in f:
    data.append([int(c) for c in x.strip()])
data = np.array(data)


def inflate_map(data, factor=5):
    """
    Inflates the map
    """
    # Add right
    data_add = data
    for i in range(1, factor):
        data_add = data_add + 1
        data_add[data_add > 9] = 1
        data = np.concatenate((data, data_add), axis=1)

    # Add down
    data_add = data
    for i in range(1, factor):
        data_add = data_add + 1
        data_add[data_add > 9] = 1
        data = np.concatenate((data, data_add), axis=0)

    return data


# Inflate map in part 2
if part == 2:
    data = inflate_map(data)

# Initiate arrays
nrow = data.shape[0]
ncol = data.shape[1]
goal = nrow * ncol - 1
data = data.flatten()
dist = np.array([np.inf for i in range(goal + 1)])
stack = np.array([i for i in range(goal + 1)])
dist[0] = 0


def swap(stack, i, j):
    """
    Swaps elements at selected positions
    """
    temp = stack[i]
    stack[i] = stack[j]
    stack[j] = temp
    return stack


def heapify(stack, dist, i, length):
    """
    Performs heapify for a given position
    """
    child_left = 2 * i + 1
    child_right = 2 * i + 2
    child_smaller = child_left

    if child_right < length:
        if dist[stack[child_left]] > dist[stack[child_right]]:
            child_smaller = child_right
    if child_smaller < length:
        if dist[stack[i]] > dist[stack[child_smaller]]:
            stack = swap(stack, i, child_smaller)
            return heapify(stack, dist, child_smaller, length)

    return stack


def decrease_key(stack, dist, i):
    """
    Moves lenght up in the heap
    """
    parent = (i - 1) // 2
    if i == 0:
        return stack
    elif dist[stack[i]] < dist[stack[parent]]:
        stack = swap(stack, i, parent)
        return decrease_key(stack, dist, parent)
    else:
        return stack


def generate_coords(coord, nrow, ncol, total):
    """
    Generates all coordinates around
    """
    coords_out = []
    if coord % ncol > 0:
        coords_out.append(coord - 1)
    if coord % ncol < ncol - 1:
        coords_out.append(coord + 1)
    if coord >= nrow:
        coords_out.append(coord - nrow)
    if coord < total - nrow:
        coords_out.append(coord + nrow)
    return coords_out


stack_len = len(stack)
while stack_len > 1:
    if stack_len % 10000 == 0:
        print(f"{stack_len} remaining")

    # Remove minimum, replace by last element and heapify
    coord_min = stack[0]
    coord_val = dist[coord_min]
    stack_len -= 1
    stack[0] = stack[stack_len]
    stack = stack[:stack_len]
    stack = heapify(stack, dist, 0, stack_len)

    if coord_min == goal:
        break

    # Search around for possible improvements
    coords = generate_coords(coord_min, nrow, ncol, goal + 1)
    for coord in coords:
        idx = np.where(stack == coord)[0]
        if len(idx) > 0:
            if coord_val + data[coord] < dist[coord]:
                dist[coord] = coord_val + data[coord]
                stack = decrease_key(stack, dist, idx[0])

print(f"Lowest risk path has risk {dist[goal]}")
