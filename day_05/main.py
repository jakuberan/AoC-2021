def calc_start_end(a):
    """
    Calculates start and end
    """
    start = []
    end = []

    start.append(min(a[0][0], a[1][0]))
    start.append(min(a[0][1], a[1][1]))
    end.append(max(a[0][0], a[1][0]) + 1)
    end.append(max(a[0][1], a[1][1]) + 1)

    return start, end


def calc_step_dir(a):
    """
    Calculates the number of steps and the direction
    """
    dirs = [0, 0]
    dirs[0] = 1 if a[1][0] > a[0][0] else -1
    dirs[1] = 1 if a[1][1] > a[0][1] else -1
    steps = abs(a[1][0] - a[0][0]) + 1

    return dirs, steps


if __name__ == "__main__":

    # Define parameters
    data_path = "input"
    lines_1 = set()
    lines_2 = set()
    lines_1_repeat = set()
    lines_2_repeat = set()

    # Process input
    f = open(data_path, "r")
    for x in f:
        # Convert to int and append
        a = [[int(z) for z in y.split(",")] for y in x.strip().split(" -> ")]
        if a[0][0] == a[1][0] or a[0][1] == a[1][1]:
            start, end = calc_start_end(a)

            # Add horizontal adn vertical lines
            for coord_x in range(start[0], end[0]):
                for coord_y in range(start[1], end[1]):
                    if (coord_x, coord_y) not in lines_1:
                        lines_1.add((coord_x, coord_y))
                    else:
                        lines_1_repeat.add((coord_x, coord_y))
                    if (coord_x, coord_y) not in lines_2:
                        lines_2.add((coord_x, coord_y))
                    else:
                        lines_2_repeat.add((coord_x, coord_y))

        else:
            dirs, steps = calc_step_dir(a)
            for step in range(steps):
                coord = (a[0][0] + dirs[0] * step, a[0][1] + dirs[1] * step)
                if coord not in lines_2:
                    lines_2.add(coord)
                else:
                    lines_2_repeat.add(coord)

    print(f"Number of overlaps in part 1 {len(lines_1_repeat)}")
    print(f"Number of overlaps in part 2 {len(lines_2_repeat)}")
