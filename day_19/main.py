import numpy as np
from scipy.spatial.distance import pdist
from itertools import combinations, compress


def read_data(data_path):
    """
    Reads data
    """

    # Define read parameters
    data = {}
    read = False
    sc_num = None
    scanner = None

    # Read input
    f = open(data_path, "r")
    for x in f:
        if len(x.strip()) == 0:
            read = False
            data[sc_num] = np.array(scanner)
        if read:
            scanner.append([int(i) for i in x.strip().split(",")])
        if x.strip().startswith("---"):
            read = True
            sc_num = int(x.strip().split(" ")[2])
            scanner = []

    # Save last scanner data
    data[sc_num] = np.array(scanner)
    return data, scanner


def get_comb_search(max_beacons):
    """
    Calculates dictionary of combination numbers C(n, 2) for search
    """
    comb = {}
    for i in range(1, max_beacons + 1):
        comb[int(i * (i - 1) / 2)] = i
    return comb


def calculate_distances(data):
    """
    Calculates distances between beacons per scanner
    """
    # calculate distances
    distances = {}
    for sc in data:
        distances[sc] = pdist(data[sc])
    return distances


def get_common_beacons(distances, comb):
    """
    Calculate number of beacons in common between two scanners
    """
    similarities = {}
    for i in distances:
        for j in distances:
            if i > j:
                simil = [di in distances[j] for di in distances[i]]
                if sum(simil) in comb:
                    similarities[(i, j)] = comb[sum(simil)]
    return similarities


def beacons_map(i, j, distant, data):
    """
    Get mappings between beacons from the point of view of scanners i and j
    """

    # Get combinations for distances
    dist_idx_i = list(combinations(range(data[i].shape[0]), 2))
    dist_idx_j = list(combinations(range(data[j].shape[0]), 2))

    # Create mappings
    mappings = []
    for sc_i in range(data[i].shape[0]):
        dists_sc_i = distant[i][[sc_i in idx_i for idx_i in dist_idx_i]]
        mask_j = [dist_j in dists_sc_i for dist_j in distant[j]]
        if sum(mask_j) > 0:
            maps_j = list(sum(list(compress(dist_idx_j, mask_j)), ()))
            map_sc_i = [k for k in set(maps_j) if maps_j.count(k) > 1]
            if len(map_sc_i) > 1:
                print(f"More than 1 point to map: {i}:{sc_i}, {j}:{map_sc_i}")
            else:
                mappings.append((sc_i, map_sc_i[0]))
    return mappings


def get_coordinates(i, j, bmap, data):
    """
    Get ordered coordinates for scanners i and j
    """
    # Get positions
    pos_i = [bmap[map_id][0] for map_id in range(len(bmap))]
    pos_j = [bmap[map_id][1] for map_id in range(len(bmap))]
    crd_i = data[i][pos_i]
    crd_j = data[j][pos_j]
    return [crd_i, crd_j]


def get_coord_mapping(coord_pairs):
    """
    Get coordinates mapping between scanners i and j
    """
    # Search for appropriate pair difference
    was_matched = False
    for i in range(1, len(coord_pairs[0])):
        diff0 = coord_pairs[0][i] - coord_pairs[0][i - 1]
        diff1 = coord_pairs[1][i] - coord_pairs[1][i - 1]
        crd0 = [abs(a) for a in diff0]
        crd1 = [abs(a) for a in diff1]
        if len(set(crd0)) == 3 and set(crd0) == set(crd1) and (0 not in set(crd1)):
            was_matched = True
            break

    # Get order and sign mapping for selected scanners
    if not was_matched:
        print("Trouble getting coordinate mapping")
    else:
        order = [crd1.index(k) for k in crd0]
        diff1_ord = diff1[order]
        sign = [1 if diff0[k] == diff1_ord[k] else -1 for k in range(3)]

    return [order, sign]


def recalculate_data(data, i, j, order, sign, bc):
    """
    Recalculates data (reorders and changes sign), returns scanner position
    """
    data[j] = data[j][:, order]
    for k in range(3):
        data[j][:, k] = data[j][:, k] * sign[k]

    # Calculates scanner coordinates
    scanner = data[i][bc[0]] - data[j][bc[1]]

    # Recalculation to first scanner
    for k in range(3):
        data[j][:, k] = data[j][:, k] + scanner[k]

    return data, scanner


def relativise_data(common, limit_pairs, data, distant):
    """
    Identify relative positions of scanners to scanner 0
    """

    known = [0]
    scanners = {0: [0, 0, 0]}
    pairs = [c for c in common if common[c] >= limit_pairs]

    while len(known) < len(data):
        for (p1, p2) in pairs:
            if sum([p1 in known, p2 in known]) == 1:
                p_unkno = p1 if p2 in known else p2
                p_known = p1 if p1 in known else p2
                known.append(p_unkno)

                # Get mappings between beacons
                beacon_map = beacons_map(p_known, p_unkno, distant, data)
                coord_pairs = get_coordinates(p_known, p_unkno, beacon_map, data)
                order, sign = get_coord_mapping(coord_pairs)

                # Rearrange and transform the data of the scanner to be added
                data, scanners[p_unkno] = recalculate_data(
                    data, p_known, p_unkno, order, sign, beacon_map[0]
                )

    return scanners, data


if __name__ == "__main__":

    # Read data
    data_path = "input"
    limit_pairs = 12
    data, scanner = read_data(data_path)
    max_beacons = max([len(i) for i in data.values()])

    # Get beacons in common between two scanners
    comb = get_comb_search(max_beacons)
    distant = calculate_distances(data)
    common = get_common_beacons(distant, comb)

    # Recalculate data
    scanners, data = relativise_data(common, limit_pairs, data, distant)

    # Get unique beacons from recalculated coordinates
    output = set()
    for i in range(len(data)):
        output = output.union(set([tuple(a) for a in data[i]]))

    print(f"There are {len(output)} different beacons on the map")

    # Get max scanner distance
    max_dist = 0
    for i in scanners:
        for j in scanners:
            if i > j:
                dist = sum([abs(scanners[i][k] - scanners[j][k]) for k in range(3)])
                max_dist = max(max_dist, dist)

    print(f"Farthest scanners are {max_dist} units apart")
