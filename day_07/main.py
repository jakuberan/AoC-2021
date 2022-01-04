import numpy as np

if __name__ == "__main__":

    # Read data
    data_path = "input"
    f = open(data_path, "r")
    for x in f:
        crabs = [int(a) for a in x.strip().split(",")]

    # Part 1 calculation
    mid = np.median(crabs)
    fuel = sum([abs(a - mid) for a in crabs])
    print(f"Fuel spent: {int(fuel)}")

    # Part 2 calculation
    mean = sum(crabs) / len(crabs)
    mid1 = round(0.5 + mean)
    mid2 = round(-0.5 + mean)
    fuel1 = sum([(abs(a - mid1) + 1) * abs(a - mid1) / 2 for a in crabs])
    fuel2 = sum([(abs(a - mid2) + 1) * abs(a - mid2) / 2 for a in crabs])
    fuel = min(fuel1, fuel2)

    print(f"Fuel spent: {int(fuel)}")
