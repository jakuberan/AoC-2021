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
    
def inflate_map(data):
    # Add right
    data_add = data
    for i in range(1, 5):
        data_add = data_add + 1
        data_add[data_add > 9] = 1
        data = np.concatenate((data, data_add), axis=1)
        
    # Add down
    data_add = data
    for i in range(1, 5):
        data_add = data_add + 1
        data_add[data_add > 9] = 1
        data = np.concatenate((data, data_add), axis=0)
    
    return data
    
if part == 2:
    data = inflate_map(data)

# Initiate arrays
length = np.zeros(data.shape)
status = [tuple(a) for a in np.transpose(np.where(length == 0))]

# Initiate total length array
length[length == 0] = np.inf
length[0,0] = 0

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

while len(status) > 0:
    
    # Identify minimum and remove from stack
    all_vals = [length[crd] for crd in status]
    coord_val = min(all_vals)
    coord_min = status.pop(all_vals.index(coord_val))
    
    # Search around for possible improvements
    coord_check = [
        (coord_min[0]+1, coord_min[1]), (coord_min[0]-1, coord_min[1]),
        (coord_min[0], coord_min[1]+1), (coord_min[0], coord_min[1]-1)
        ]
    for coord in coord_check:
        if coord_ok(data, coord):
            if coord in status:
                if coord_val + data[coord] < length[coord]:
                    length[coord] = coord_val + data[coord]
            
print(f"Lowest risk path has risk {length[-1, -1]}")
