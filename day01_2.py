# Define path
data_path = "data/input01"

# Read line-by-line
f = open(data_path, "r")
prevs = []
cnt = 0
for x in f:
    # Convert to int and append
    prevs.append(int(x))
    if len(prevs) > 3:
        prev2 = prevs.pop(0)
        if prev2 < prevs[2]:
            cnt += 1

print(f"Increased {cnt} times")
