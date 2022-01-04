import numpy as np
import re


def read_data(data_path):
    """
    Reads data
    """
    status = []
    coords = []
    f = open(data_path, "r")
    for x in f:
        tmp = re.split("\\.|=|,| ", x.strip())
        status.append(1 if tmp[0] == "on" else 0)
        new_coord = [
            [int(tmp[2]), int(tmp[4])],
            [int(tmp[6]), int(tmp[8])],
            [int(tmp[10]), int(tmp[12])],
        ]
        coords.append(new_coord)

    return coords, status


def adjust_coordinates_part1(coords, status, dim, part):
    """
    Adjust coordinates according to the part
    """
    coords_new = []
    status_new = []
    if part == 1:
        for i in range(len(coords)):
            coord_new = []
            for d in range(dim):
                if (coords[i][d][0] <= 50) and (coords[i][d][1] >= -50):
                    c0 = max(-50, coords[i][d][0])
                    c1 = min(50, coords[i][d][1])
                    coord_new.append([c0, c1])
            if len(coord_new) == 3:
                coords_new.append(coord_new)
                status_new.append(status[i])

        coords = coords_new
        status = status_new

    # Change orders of coordinates
    coords = list(reversed(coords))
    status = list(reversed(status))

    return coords, status


def get_size(crd, dim):
    """
    Evaluates the size of the cuboid
    """
    out = 1
    for i in range(dim):
        out *= crd[i][1] - crd[i][0] + 1
    return out


def is_intersection(crd, crd_off):
    """
    Evaluates if two cuboids intersect
    """
    if (crd[0][0] <= crd_off[0][1]) and (crd[0][1] >= crd_off[0][0]):
        if (crd[1][0] <= crd_off[1][1]) and (crd[1][1] >= crd_off[1][0]):
            if (crd[2][0] <= crd_off[2][1]) and (crd[2][1] >= crd_off[2][0]):
                return True
    return False


def get_intersection_1d(c, c_off):
    """
    Returns intersection 1d
    """
    if c[0] <= c_off[0]:
        if c[1] >= c_off[1]:
            return [c_off[0], c_off[1]]
        else:
            return [c_off[0], c[1]]
    else:
        if c[1] >= c_off[1]:
            return [c[0], c_off[1]]
        else:
            return [c[0], c[1]]


def get_intersection_3d(crd, crd_off):
    """
    Returns intersection 1d
    """
    x = get_intersection_1d(crd[0], crd_off[0])
    y = get_intersection_1d(crd[1], crd_off[1])
    z = get_intersection_1d(crd[2], crd_off[2])
    return [x, y, z]


def get_subtraction_3d(crd, crd_off, dim):
    """
    Returns intersection
    """
    out = []
    c_inter = get_intersection_3d(crd, crd_off)

    # Create intervals for final construction
    mids = []
    for i in range(dim):
        to_append = []
        if crd[i][0] < c_inter[i][0]:
            to_append.append([crd[i][0], c_inter[i][0] - 1])
        to_append.append([c_inter[i][0], c_inter[i][1]])
        if crd[i][1] > c_inter[i][1]:
            to_append.append([c_inter[i][1] + 1, crd[i][1]])
        mids.append(to_append)

    # Output cuboids
    for xi in mids[0]:
        for yi in mids[1]:
            for zi in mids[2]:
                new_crd = [xi, yi, zi]
                if new_crd != c_inter:
                    out.append(new_crd)
    return out


def subtract_3d(crds, crd_off, dim):
    """
    Performs 3d subtraction
    """
    crd_out = []
    for crd in crds:
        if is_intersection(crd, crd_off):
            new_coords = get_subtraction_3d(crd, crd_off, dim)
            for new_coord in new_coords:
                crd_out.append(new_coord)
        else:
            crd_out.append(crd)
    return crd_out


if __name__ == "__main__":

    # Read data
    data_path = "input"
    coords_in, status_in = read_data(data_path)
    dim = 3
    size = 0
    coords_off = []

    for part in [1, 2]:
        coords, status = adjust_coordinates_part1(coords_in, status_in, dim, part)

        # Count last after subtracting off coordinates
        for i, crd in enumerate(coords):
            crds = [crd]
            size_add = 0
            if status[i] == 1:
                # Perform 3d subtraction
                for crd_off in coords_off:
                    crds = subtract_3d(crds, crd_off, dim)
                # Calculate size for all resulting cuboinds
                for c in crds:
                    size += get_size(c, dim)
            # Append to 3d subtraction from further cuboids
            coords_off.append(crd)

        print(f"There are {size} cubes turned on in part {part}")
