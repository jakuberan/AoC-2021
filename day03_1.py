# Define path
data_path = "data/input03"

# Counters
bin_counter = None

# Read line-by-line
f = open(data_path, "r")
for x in f:
    binary = x.strip()

    # Initialize counter
    if bin_counter is None:
        bin_counter = [0] * len(binary)

    # Count the bins
    for i, bit in enumerate(binary):
        if bit == "1":
            bin_counter[i] += 1
        else:
            bin_counter[i] -= 1

gamma = int("".join(["1" if b > 0 else "0" for b in bin_counter]), 2)
epsilon = 2 ** len(bin_counter) - gamma - 1

print(f"Power consumption is {gamma * epsilon}")
