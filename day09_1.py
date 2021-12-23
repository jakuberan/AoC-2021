# Define path
data_path = "data/input09"

heightmap = []

# Read line-by-line
f = open(data_path, "r")
for x in f:
    heightmap.append([int(h) for h in x.strip()])


def is_lowest(heightmap, i, j):
    height = heightmap[i][j]
    if (j > 0) and (heightmap[i][j - 1] <= height):
        return False
    if (j < len(heightmap[i]) - 1) and (heightmap[i][j + 1] <= height):
        return False
    if (i > 0) and (heightmap[i - 1][j] <= height):
        return False
    if (i < len(heightmap) - 1) and (heightmap[i + 1][j] <= height):
        return False
    return True


risk = 0

for i in range(len(heightmap)):
    for j in range(len(heightmap[i])):
        if is_lowest(heightmap, i, j):
            # print(i, j, heightmap[i][j])
            risk += heightmap[i][j] + 1

print(f"Total risk is {risk}")
