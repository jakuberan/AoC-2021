def read_data(data_path):
    """
    Reads data
    """
    instr = []
    f = open(data_path, "r")
    for x in f:
        instr.append(x.strip().split(" "))
    return instr


def convert_instr(instr, memory):
    """
    Convert all terms in instruction to memory parts
    """
    for line in instr:
        if line[0] != "inp":
            try:
                term = memory[line[1]]
            except:
                memory[line[1]] = int(line[1])
            try:
                term = memory[line[2]]
            except:
                memory[line[2]] = int(line[2])
    return memory


def get_instr_nums(instr):
    """
    Count number of input instructions
    """
    instr_num = []
    for num, i in enumerate(instr):
        if i[0] == "inp":
            instr_num.append(num)
    return instr_num


def pre_calculate(inputs, memory, instr_nums, instr):
    """
    Precalculates instructions given inputs
    """
    if len(inputs) == 14:
        to_instr = len(instr)
    else:
        to_instr = instr_nums[len(inputs)]
    for i in instr[:to_instr]:
        if i[0] == "inp":
            memory[i[1]] = inputs.pop(0)
        elif i[0] == "add":
            memory[i[1]] = memory[i[1]] + memory[i[2]]
        elif i[0] == "mul":
            memory[i[1]] = memory[i[1]] * memory[i[2]]
        elif i[0] == "div":
            memory[i[1]] = memory[i[1]] // memory[i[2]]
        elif i[0] == "mod":
            memory[i[1]] = memory[i[1]] % memory[i[2]]
        elif i[0] == "eql":
            memory[i[1]] = 1 * (memory[i[1]] == memory[i[2]])

    return {k: [memory[k]] for k in memory}


def process_lists(ins, m1, m2):
    """
    Evaluates instruction given two list memory variables
    """
    if ins == "add":
        out = [a + b for a in m1 for b in m2]
    elif ins == "mul":
        out = [a * b for a in m1 for b in m2]
    elif ins == "div":
        out = [a // b for a in m1 for b in m2]
    elif ins == "mod":
        out = [a % b for a in m1 for b in m2]
    elif ins == "eql":
        out = [1 * (a == b) for a in m1 for b in m2]
    else:
        print(f"Unknown instruction {ins}")
    return list(set(out))


def check_zero_result(inputs, memory, instr_nums, instr):
    """
    Takes pre-calculated input and estimates output ranges
    """
    if len(inputs) == 14:
        to_instr = len(instr)
    else:
        to_instr = instr_nums[len(inputs)]
    for i in instr[to_instr:]:
        if i[0] == "inp":
            memory[i[1]] = list(range(1, 10))
        else:
            memory[i[1]] = process_lists(i[0], memory[i[1]], memory[i[2]])
    return memory


if __name__ == "__main__":

    # Read data
    data_path = "input"
    instr = read_data(data_path)

    # Convert string numbers to numbers
    instr_nums = get_instr_nums(instr)

    # Get extended memory
    memory_zero = {"x": 0, "y": 0, "z": 0, "w": 0}
    memory_zero = convert_instr(instr, memory_zero)

    for part in [1, 2]:
        # Select variables according to the part solved
        limit = 17 - part * 8
        inputs = [limit]
        step = part * 2 - 3

        # Search for possible inputs
        while True:
            print(inputs)
            memory = pre_calculate(inputs.copy(), memory_zero.copy(), instr_nums, instr)
            output = check_zero_result(inputs.copy(), memory.copy(), instr_nums, instr)
            if 0 in output["z"]:
                if len(inputs) == 14:
                    print("".join([str(i) for i in inputs]))
                    break
                else:
                    inputs.append(limit)
            else:
                if part == 1:
                    while inputs[-1] <= 10 - limit:
                        inputs.pop()
                else:
                    while inputs[-1] >= 10 - limit:
                        inputs.pop()
                inputs[-1] += step
