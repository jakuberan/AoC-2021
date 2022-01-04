import numpy as np


def read_data(data_path):
    """
    Reads data
    """
    burrow = []
    f = open(data_path, "r")
    for x in f:
        burrow.append(x.strip().split("#"))
    return burrow


def define_constants(part):
    """
    Defines constants needed for program run
    """
    amph_map = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }
    costs = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }
    hall = [h for h in burrow[1][1][:-4]]
    if part == 1:
        rooms = {
            0: [burrow[2][3], burrow[3][1]],
            1: [burrow[2][4], burrow[3][2]],
            2: [burrow[2][5], burrow[3][3]],
            3: [burrow[2][6], burrow[3][4]],
        }
    else:
        rooms = {
            0: [burrow[2][3], "D", "D", burrow[3][1]],
            1: [burrow[2][4], "C", "B", burrow[3][2]],
            2: [burrow[2][5], "B", "A", burrow[3][3]],
            3: [burrow[2][6], "A", "C", burrow[3][4]],
        }
    room_size = 2 * part
    return amph_map, costs, hall, rooms, room_size


def compress(hall, rooms):
    """
    Generates compressed hall and room representation
    """
    out = "".join(hall)
    for r in rooms.values():
        out += "".join(r)
    return out


def room_tops(situation, room_size, base=7):
    """
    Get first empty and first occupied position for each room
    """
    room_string = situation[base:]
    out_empty = []
    out_full = []
    for i in range(len(room_string) // room_size):
        # Search for last empty positions
        offset = room_size - 1
        while offset >= 0:
            if room_string[room_size * i + offset] == ".":
                out_empty.append(room_size * i + offset + base)
                break
            offset -= 1
        # Search for first occupied positions
        offset = 0
        while offset < room_size:
            if room_string[room_size * i + offset] != ".":
                out_full.append(room_size * i + offset + base)
                break
            offset += 1

    return out_empty, out_full


def get_steps(i, j, room_size, base=7):
    """
    Calculates number of steps needed to go from i to j
    """
    hall_map = {
        0: 0,
        1: 1,
        2: 3,
        3: 5,
        4: 7,
        5: 9,
        6: 10,
    }

    # Get precise positions
    hall_pos = hall_map[i]
    room_num = (j - base) // room_size
    room_pos = (j - base) % room_size
    entry = 2 + room_num * 2

    # Return final length
    return abs(hall_pos - entry) + 1 + room_pos


def path_blocked(situation, i, room_num):
    """
    Checks if a path to selected room from position i is blocked
    """

    if i < room_num + 2:
        if situation[(i + 1) : (room_num + 2)].count(".") != (room_num + 1 - i):
            return True
    if i > room_num + 1:
        if situation[(room_num + 2) : i].count(".") != (i - room_num - 2):
            return True
    return False


def can_leave_room(situation, i, j, room_size, amph_map, base=7):
    """
    Evaluates if the amphipod at position j can leave the room
    """
    room_pos = (j - base) % room_size
    room_num = (j - base) // room_size

    # Path blocked
    if path_blocked(situation, i, room_num):
        return False

    for pos in range(room_pos, room_size):
        if amph_map[situation[j]] != room_num:
            return True
        j += 1
    return False


def can_go_to_room(situation, i, j, room_size, amph_map, base=7):
    """
    Evaluates if the amphipod at position i can go to room at position j
    """
    room_pos = (j - base) % room_size
    room_num = (j - base) // room_size

    # Incorrect room
    if room_num != amph_map[situation[i]]:
        return False

    # Path blocked
    if path_blocked(situation, i, room_num):
        return False

    # Room filled with other amphipods
    allowed = [".", situation[i]]
    top_pos = j + room_size - room_pos
    occups = sum([0 if a in allowed else 1 for a in situation[(j + 1) : top_pos]])
    if occups > 0:
        return False
    else:
        return True


def pos_switch(sit, i, j, costs):
    """
    Returns new situation after i-j switch and associated costs
    """
    new_sit = sit[:i] + sit[j] + sit[(i + 1) : j] + sit[i] + sit[(j + 1) :]
    amph = sit[j] if sit[i] == "." else sit[i]
    steps = get_steps(i, j, room_size)
    return new_sit, steps * costs[amph]


def generate_moves(situation, cost, room_size, amph_map, costs, base=7):
    """
    Generates all new possible situations given current situation
    """
    new_costs = []
    new_situations = []
    room_empty_pos, room_full_pos = room_tops(situation, room_size)
    for i in range(base):
        if situation[i] == ".":
            for j in room_full_pos:
                if can_leave_room(situation, i, j, room_size, amph_map):
                    sit, cos = pos_switch(situation, i, j, costs)
                    new_costs.append(cos + cost)
                    new_situations.append(sit)
        else:
            for j in room_empty_pos:
                if can_go_to_room(situation, i, j, room_size, amph_map):
                    sit, cos = pos_switch(situation, i, j, costs)
                    new_costs.append(cos + cost)
                    new_situations.append(sit)
    return new_situations, new_costs


def all_not_home(situation, room_size, base=7):
    """
    Checks if all amphipods are already at their burrows
    """
    return situation[base:] != "".join([r * room_size for r in "ABCD"])


if __name__ == "__main__":

    # Read data
    data_path = "input"
    burrow = read_data(data_path)

    for part in [1, 2]:
        amph_map, costs, hall, rooms, room_size = define_constants(part)

        # Search graph of all available options
        situ_stack = []
        cost_stack = np.array([])
        situ_best = compress(hall, rooms)
        cost_best = 0
        situ_used = {situ_best}
        while all_not_home(situ_best, room_size):

            # Generate all possible moves from current situation
            situ_new, cost_new = generate_moves(
                situ_best, cost_best, room_size, amph_map, costs
            )
            situ_stack += situ_new
            cost_stack = np.concatenate([cost_stack, np.array(cost_new)])

            # Select next best situation + verify it has not been used so-far
            while situ_best in situ_used:
                pos = np.argmin(cost_stack)
                cost_best = cost_stack[pos]
                cost_stack = np.concatenate([cost_stack[:pos], cost_stack[(pos + 1) :]])
                situ_best = situ_stack.pop(pos)
            print(cost_best, situ_best)

            # Save new best to already tried
            situ_used.add(situ_best)

        print(f"Lowest cost is {cost_best}")
