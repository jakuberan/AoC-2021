def count_bins(binary, bin_counter):
    """
    Count the bins
    """

    # Initialize counter, calculate
    if bin_counter is None:
        bin_counter = [0] * len(binary)

    for i, bit in enumerate(binary):
        if bit == "1":
            bin_counter[i] += 1
        else:
            bin_counter[i] -= 1

    return bin_counter


def reduce_list(full, more=True, pos=0):
    """
    Reduces a list by rules for support rating
    """
    while len(full) > 1:
        pos += 1
        memory = [[], []]
        for binary in full:
            memory[int(binary[pos])].append(binary)
        if more:
            full = memory[len(memory[1]) >= len(memory[0])]
        else:
            full = memory[len(memory[1]) < len(memory[0])]
    return full[0]


if __name__ == "__main__":

    # Define parameters
    bin_counter = None
    data_path = "input"
    mem = [[], []]

    # Process input
    f = open(data_path, "r")
    for x in f:
        binary = x.strip()
        bin_counter = count_bins(binary, bin_counter)
        mem[int(binary[0])].append(binary)

    gamma = int("".join(["1" if b > 0 else "0" for b in bin_counter]), 2)
    epsilon = 2 ** len(bin_counter) - gamma - 1
    print(f"Power consumption is {gamma * epsilon}")

    # Part 2
    more_last = reduce_list(mem[len(mem[1]) >= len(mem[0])])
    less_last = reduce_list(mem[len(mem[1]) < len(mem[0])], more=False)

    print(f"Support rating {int(less_last, 2) * int(more_last, 2)}")
