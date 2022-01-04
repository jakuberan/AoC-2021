def verify_line(line, match_map={")": "(", "]": "[", "}": "{", ">": "<"}):
    stack = []
    for c in line:
        if c in "([{<":
            stack.append(c)
        else:
            if match_map[c] != stack.pop():
                return c
    return "OK"


if __name__ == "__main__":

    # Define parameters
    data_path = "input"
    point_map = {")": 3, "]": 57, "}": 1197, ">": 25137, "OK": 0}
    match_map = {")": "(", "]": "[", "}": "{", ">": "<"}
    points = 0

    # Read data and process
    f = open(data_path, "r")
    for x in f:
        points += point_map[verify_line(x.strip())]

    print(f"Syntax error score {points}")
