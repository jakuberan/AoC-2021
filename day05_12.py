# Define path
data_path = "data/input05"

lines = {}
part = 2

# Read line-by-line
f = open(data_path, "r")
for x in f:
    # Convert to int and append
    a = [[int(z) for z in y.split(',')] for y in x.strip().split(' -> ')]
    if a[0][0] == a[1][0] or a[0][1] == a[1][1]:
        start_x = min(a[0][0], a[1][0])
        start_y = min(a[0][1], a[1][1])
        end_x = max(a[0][0], a[1][0]) + 1
        end_y = max(a[0][1], a[1][1]) + 1
        
        for coord_x in range(start_x, end_x):
            for coord_y in range(start_y, end_y):
                if (coord_x, coord_y) not in lines.keys():
                    lines[(coord_x, coord_y)] = 0
                else:
                    lines[(coord_x, coord_y)] += 1
    elif part == 2:
        dir_x = 1 if a[1][0] > a[0][0] else -1
        dir_y = 1 if a[1][1] > a[0][1] else -1
        steps = abs(a[1][0] - a[0][0]) + 1
        for step in range(steps):
            coord = (a[0][0] + dir_x * step, a[0][1] + dir_y * step)
            if coord not in lines.keys():
                lines[coord] = 0
            else:
                lines[coord] += 1
    
print(f'Number of overlaps {sum(v > 0 for v in lines.values())}')