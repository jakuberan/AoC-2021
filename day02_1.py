# Define path
data_path = "data/input02"

# Counters
horizontal = 0
vertical = 0

# Read line-by-line
f = open(data_path, "r")
for x in f:
    command = x.strip().split()
    if command[0] == "forward":
        horizontal += int(command[1])
    elif command[0] == "up":
        vertical -= int(command[1])
    elif command[0] == "down":
        vertical += int(command[1])
    else:
        print(f"Unknown comand {command[0]}")

print(horizontal * vertical)
