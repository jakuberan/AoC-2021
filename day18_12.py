import numpy as np
import ast
# Define path
data_path = "data/input18"

# Define parameters
data = []

def process_input(line):
    out = []
    for c in line:
        try:
            out.append(int(c))
        except:
            out.append(c)
    return out
    
# Read line-by-line
f = open(data_path, "r")
for x in f:
    #data.append(ast.literal_eval(x.strip()))
    data.append(process_input(x.strip()))

def add_nums(num1, num2):
    return ['['] + num1 + [','] + num2 + [']']

def search_explode(num):
    cnt = 0
    for i, c in enumerate(num):
        if c == '[':
            cnt += 1
        elif c == ']':
            cnt -= 1
        if cnt > 4:
            break
    if cnt > 4:
        while num[i] != '[' or num[i + 4] != ']':
            i += 1
        return i + 2
    return 0

def do_explode(num, i):
    i_left = i - 3
    i_right = i + 3
    length = len(num)
    while i_left > 0 and type(num[i_left]) == str:
        i_left -= 1
    while length > i_right and type(num[i_right]) == str:
        i_right += 1
    if i_left > 0:
        num[i_left] += num[i - 1]
    if length > i_right:
        num[i_right] += num[i + 1]
    num = num[:(i - 2)] + [0] + num[(i + 3):]
    return num

def search_split(num):
    for i in range(len(num)):
        if type(num[i]) == int:
            if num[i] > 9:
                return True, i
    return False, 0

def do_split(num, i):
    n = num[i] // 2
    return num[:i] + ['[', n, ',', num[i] - n,']'] + num[(i+1):]

def calc_magnitude(num):
    i_replace = [0]
    while len(i_replace) > 0:
        i_replace = []
        for i in range(len(num) - 4):
            if num[i] == '[' and num[i + 4] == ']':
                i_replace.append(i)
        if len(i_replace) > 0:
            num_new = []
            for i, i_rep in enumerate(i_replace):
                if i == 0:
                    num_new += num[:i_rep]
                else:
                    num_new += num[(i_replace[i-1]+5):i_rep]
                num_new += [3 * num[i_rep + 1] + 2 * num[i_rep + 3]]
            num_new += num[(i_rep+5):]
            num = num_new
    return num[0]

def reduce(num):
    repeat = True
    while repeat:
        repeat = False
        i_expl = search_explode(num)  
        if i_expl > 0:
            num = do_explode(num, i_expl)
            repeat = True
        else:
            to_split, i_split = search_split(num)
            if to_split:
                num = do_split(num, i_split)
                repeat = True  
    return num
    
        
# Perform steps of calculation        
out = data[0]
for new_num in data[1:]:
    out = add_nums(out, new_num)
    out = reduce(out)
                
print(f'Total magnitude is {calc_magnitude(out)}')

max_mag = 0
for i in range(len(data)):
    for j in range(len(data)):
        if i != j:
            out = reduce(add_nums(data[i], data[j]))
            out_mag = calc_magnitude(out)
            if out_mag > max_mag:
                max_mag = out_mag
        
print(f'Maximum magnitude is {max_mag}')