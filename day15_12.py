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
dist = np.array([np.inf for i in range(goal+1)])
stack = np.array([i for i in range(goal+1)])
stack_dist = np.array([np.inf for i in range(goal+1)])
stack_dist[0] = 0
dist[0] = 0

def swap(sdist, stack, i, j):
    """
    Swaps elements at selected positions
    """
    sdist_temp = sdist[i]
    stack_temp = stack[i]
    sdist[i] = sdist[j]
    stack[i] = stack[j]
    sdist[j] = sdist_temp
    stack[j] = stack_temp
    return sdist, stack

def heapify(sdist, stack, i, length):
    """
    Performs heapify for a given position
    """
    if 2 * i + 1 < length:
        if 2 * i + 2 < length:
            if sdist[2 * i + 1] > sdist[2 * i + 2]:
                sml_idx = 2 * i + 2
            else: 
                sml_idx = 2 * i + 1
        else:
            sml_idx = 2 * i + 1
        if sdist[i] > sdist[sml_idx]:
            sdist, stack = swap(sdist, stack, i, sml_idx)
            return heapify(sdist, stack, sml_idx, length)        

    return sdist, stack

def decrease_key(sdist, stack, i):
    """
    Moves lenght up in the heap
    """
    if i == 0:
        return sdist, stack
    elif sdist[i] < sdist[(i-1)//2]:
        sdist, stack = swap(sdist, stack, i, (i-1)//2)
        return decrease_key(sdist, stack, (i-1)//2)
    else:
        return sdist, stack

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

while len(stack) > 1:
    if len(stack) % 10000 == 0:
        print(f"{len(stack)} remaining")
    
    # Identify minimum, remove and replace by last element
    coord_val = stack_dist[0]
    coord_min = stack[0]
    cur_len = len(stack) - 1
    
    if coord_min == goal:
        break

    stack_dist[0] = stack_dist[cur_len]
    stack_dist = stack_dist[:cur_len]
    stack[0] = stack[cur_len]
    stack = stack[:cur_len]
    stack_dist, stack = heapify(stack_dist, stack, 0, cur_len)
    
    # Search around for possible improvements
    coords = generate_coords(coord_min, nrow, ncol, goal+1)
    for coord in coords:
        idx = np.where(stack == coord)[0]
        if len(idx) > 0:
            if coord_val + data[coord] < dist[coord]:
                length_new = coord_val + data[coord]
                dist[coord] = length_new
                stack_dist[idx[0]] = length_new
                stack_dist, stack = decrease_key(stack_dist, stack, idx[0])
            
print(f"Lowest risk path has risk {dist[goal]}")
