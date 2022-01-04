def read_data(data_path):
    """
    Reads data
    """
    heightmap = []
    f = open(data_path, "r")
    for x in f:
        heightmap.append([int(h) for h in x.strip()])
    return heightmap


def is_lowest(heightmap, i, j):
    """
    Searches for lowest poi nt
    """
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


def basin_size(hmap, i, j):
    """
    Calculates basin size
    """

    # Initialize sets and add first point
    basin = set()
    current = set()
    basin.add((i, j))
    current.add((i, j))
    new = current

    # Do while there are new points
    while len(new) > 0:
        new = set()
        # Look around the points in new and add them to basin and new
        for point in current:
            for [x, y] in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                if point[0] + y >= 0 and point[1] + x >= 0:
                    if point[0] + y < len(hmap):
                        if point[1] + x < len(hmap[point[0] + y]):
                            if hmap[point[0] + y][point[1] + x] < 9:
                                point_new = (point[0] + y, point[1] + x)
                                if point_new not in basin:
                                    basin.add(point_new)
                                    new.add(point_new)
        # Update sets
        current = new
    return len(basin)


if __name__ == "__main__":

    # Read data
    data_path = "input"
    heightmap = read_data(data_path)

    # Basin evaluation
    risk = 0
    basins = []

    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if is_lowest(heightmap, i, j):
                risk += heightmap[i][j] + 1
                basins.append(basin_size(heightmap, i, j))

    print(f"Total risk is {risk}")
    basins.sort()
    print(f"Multiplied sizes {basins[-1] * basins[-2] * basins[-3]}")
