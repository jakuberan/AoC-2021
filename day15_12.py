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
length = np.zeros(data.shape)
status = [tuple(a) for a in np.transpose(np.where(length == 0))]

# Initiate total length array
length[length == 0] = np.inf
length[0,0] = 0
length_flat = list(length.ravel())

def swap(len_flat, status, i, j):
    """
    Swaps elements at selected positions
    """
    len_temp = len_flat[i]
    sts_temp = status[i]
    len_flat[i] = len_flat[j]
    status[i] = status[j]
    len_flat[j] = len_temp
    status[j] = sts_temp
    return len_flat, status

def heapify(len_flat, status, i, lenght):
    """
    Performs heapify for a given position
    """
    if 2 * i + 1 < lenght:
        if 2 * i + 2 < lenght:
            if len_flat[2 * i + 1] > len_flat[2 * i + 2]:
                sml_idx = 2 * i + 2
            else: 
                sml_idx = 2 * i + 1
        else:
            sml_idx = 2 * i + 1
        if len_flat[i] > len_flat[sml_idx]:
            len_flat, status = swap(len_flat, status, i, sml_idx)
            return heapify(len_flat, status, sml_idx, lenght)        

    return len_flat, status

def decrease_key(len_flat, status, i):
    """
    Moves lenght up in the heap
    """
    if i == 0:
        return len_flat, status
    elif len_flat[i] < len_flat[(i-1)//2]:
        len_flat, status = swap(len_flat, status, i, (i-1)//2)
        return decrease_key(len_flat, status, (i-1)//2)
    else:
        return len_flat, status

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

while len(status) > 1:
    if len(status) % 10000 == 0:
        print(f"{len(status)} remaining")
    
    # Identify minimum, remove and replace by last element
    coord_val = length_flat[0]
    coord_min = status[0]
    
    if coord_min == (data.shape[0] - 1, data.shape[1] - 1):
        break

    length_flat[0] = length_flat.pop()
    status[0] = status.pop()
    length_flat, status = heapify(length_flat, status, 0, len(length_flat))
    
    # Search around for possible improvements
    coord_check = [
        (coord_min[0]+1, coord_min[1]), (coord_min[0], coord_min[1]+1),
        (coord_min[0]-1, coord_min[1]), (coord_min[0], coord_min[1]-1)
        ]
    for coord in coord_check:
        if coord_ok(data, coord):
            if coord in status:
                if coord_val + data[coord] < length[coord]:
                    length_new = coord_val + data[coord]
                    idx = status.index(coord)
                    length[coord] = length_new
                    length_flat[idx] = length_new
                    length_flat, status = decrease_key(length_flat, status, idx)
            
print(f"Lowest risk path has risk {length[-1, -1]}")
