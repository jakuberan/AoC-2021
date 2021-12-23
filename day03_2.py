# Define data path
data_path = "data/input03"

# Data storage
mem = [[], []]

# Read line-by-line
f = open(data_path, "r")
for x in f:
    binary = x.strip()
    mem[int(binary[0])].append(binary)


def reduce_list(full, more=True, pos=0):
    # Reduces a list by rules for support rating
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


more_last = reduce_list(mem[len(mem[1]) >= len(mem[0])])
less_last = reduce_list(mem[len(mem[1]) < len(mem[0])], more=False)

print(f"Support rating {int(less_last, 2) * int(more_last, 2)}")
