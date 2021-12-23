import numpy as np

# Define path
data_path = "data/input06"

# Defien the number of days
days = 256

# Read line-by-line
f = open(data_path, "r")
for x in f:
    states_list = [int(a) for a in x.split(",")]

matrix = np.zeros((9, 9))
state = np.zeros(9)

# Fill in matrix
matrix[0, 6] = 1
matrix[0, 8] = 1
for i in range(8):
    matrix[i + 1, i] = 1

# Fill in initial conditions
for i in range(9):
    state[i] = states_list.count(i)

# Iterate
for i in range(days):
    state = np.matmul(state, matrix)

print(f"There are {sum(state)} lanternfish at day 80")
