import numpy as np
from bisect import bisect

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
length = np.zeros(data.shape)
status = [tuple(a) for a in np.transpose(np.where(length == 0))]

# Initiate total length array
length[length == 0] = np.inf
length[0,0] = 0
length_flat = list(length.ravel())

def coord_ok(data, coord):
    """
    Verifies if the selected coordinate is ok
    """
    if (coord[0] < 0) or (coord[1] < 0):
        return False
    elif (coord[0] >= data.shape[0]) or (coord[1] >= data.shape[1]):
        return False
    else:
        return True
    
def change_order(coord, status, len_flat, len_new):
    """
    Reinserts the changed length and coordinate position
    """
    idx_old = status.index(coord)
    idx_new = bisect(len_flat[:(idx_old + 1)], len_new)

    # Nothing changes
    if idx_new == idx_old:
        return status, len_flat
    else:
        # Remove old elements
        status.pop(idx_old)
        len_flat.pop(idx_old)
        
        # First vs. other element is added
        if idx_new == 0:
            return [coord] + status, [len_new] + len_flat
        else:
            return status[:idx_new] + [coord] + status[idx_new:], \
                len_flat[:idx_new] + [len_new] + len_flat[idx_new:]
        

while len(status) > 0:
    
    # Identify minimum and remove from stack
    coord_val = length_flat.pop(0)
    coord_min = status.pop(0)
    
    # Search around for possible improvements
    coord_check = [
        (coord_min[0]+1, coord_min[1]), (coord_min[0], coord_min[1]+1)
        #(coord_min[0]-1, coord_min[1]), (coord_min[0], coord_min[1]-1)
        ]
    for coord in coord_check:
        if coord_ok(data, coord):
            if coord in status:
                if coord_val + data[coord] < length[coord]:
                    length_new = coord_val + data[coord]
                    length[coord] = length_new
                    status, length_flat = change_order(
                        coord, status, length_flat, length_new
                        )
            
print(f"Lowest risk path has risk {length[-1, -1]}")
