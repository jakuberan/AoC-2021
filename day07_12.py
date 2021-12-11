import numpy as np

# Define path
data_path = "data/input07"

part = 2

# Read line-by-line
f = open(data_path, "r")
for x in f:
    crabs = [int(a) for a in x.strip().split(',')]

if part == 1:
    mid = np.median(crabs)
    fuel = sum([abs(a - mid) for a in crabs])
else:
    mean = sum(crabs) / len(crabs)
    mid1 = round(0.5 + mean)
    mid2 = round(-0.5 + mean)
    fuel1 = sum([(abs(a - mid1) + 1) * abs(a - mid1) / 2 for a in crabs])
    fuel2 = sum([(abs(a - mid2) + 1) * abs(a - mid2) / 2 for a in crabs])
    fuel = min(fuel1, fuel2)

print(f'Fuel spent: {fuel}')