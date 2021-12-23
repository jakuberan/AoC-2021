from statistics import median

# Define path
data_path = "data/input10"

point_map = {"(": 1, "[": 2, "{": 3, "<": 4}
match_map = {")": "(", "]": "[", "}": "{", ">": "<"}
points = []


def verify_line(line, match_map):
    stack = []
    for c in line:
        if c in "([{<":
            stack.append(c)
        else:
            if match_map[c] != stack.pop():
                return "Error"
    if len(stack) == 0:
        return "OK"
    else:
        return stack


# Read line-by-line
f = open(data_path, "r")
for x in f:
    out = verify_line(x.strip(), match_map)
    if out not in ["Error", "OK"]:
        p_line = 0
        for i in range(len(out) - 1, -1, -1):
            p_line = 5 * p_line + point_map[out[i]]
        points.append(p_line)

print(f"Middle score is {median(points)}")
