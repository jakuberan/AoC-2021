import numpy as np

# Define path
data_path = "data/input08"

trials = []
display = []

# Read line-by-line
f = open(data_path, "r")
for x in f:
    data = x.strip().split(' | ')
    trials.append(data[0].split())
    display.append(data[1].split())
    
count = 0
for digits in display:
    for d in digits:
        if len(d) in [2, 3, 4, 7]:
            count += 1

print(f'There are {count} unique segment digits')