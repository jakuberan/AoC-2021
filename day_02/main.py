def command_part_1(command, horizontal, vertical):
    """
    Applies command according to part 1
    """
    if command[0] == "forward":
        horizontal += int(command[1])
    elif command[0] == "up":
        vertical -= int(command[1])
    elif command[0] == "down":
        vertical += int(command[1])
    else:
        print(f"Unknown comand {command[0]}")

    return horizontal, vertical


def command_part_2(command, horizontal, vertical, aim):
    """
    Applies command according to part 2
    """
    if command[0] == "forward":
        horizontal += int(command[1])
        vertical += aim * int(command[1])
    elif command[0] == "up":
        aim -= int(command[1])
    elif command[0] == "down":
        aim += int(command[1])
    else:
        print(f"Unknown comand {command[0]}")

    return horizontal, vertical, aim


if __name__ == "__main__":

    # Define parameters
    data_path = "input"
    hor = [0, 0]
    ver = [0, 0]
    aim = 0

    # Read and process
    f = open(data_path, "r")
    for x in f:
        command = x.strip().split()
        hor[0], ver[0] = command_part_1(command, hor[0], ver[0])
        hor[1], ver[1], aim = command_part_2(command, hor[1], ver[1], aim)

    print(f"Part 1 result is {hor[0] * ver[0]}")
    print(f"Part 2 result is {hor[1] * ver[1]}")
