# Define path
data_path = "data/input01"

# Read line-by-line
f = open(data_path, "r")
prev = 1000
cnt = 0
for x in f:
    # Convert to int and append
    now = int(x)
    if now > prev:
        cnt += 1
    prev = now

print(f"Increased {cnt} times")
