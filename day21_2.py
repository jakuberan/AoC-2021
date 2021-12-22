# Define path
data_path = "data/input21"

# Define parameters
goal = 21
pos = []

# Read line-by-line
f = open(data_path, "r")
for x in f:
    pos.append(int(x.strip().split(' ')[-1]))
    
def count_outputs(out, a, mult):
    """
    Updates output list
    """
    for k in a:
        if k in out:
            out[k] += mult * a[k]
        else:
            out[k] = mult * a[k]
    return out

def get_steps(start, steps, score):
    """
    Counts number of steps needed to win for a single player 
    """
    if score >= goal:
        return {steps: 1}
    options = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    out = {}
    # Analyzing different options
    for k in options:
        start_in = (start + k - 1) % 10 + 1
        a = get_steps(start_in, steps + 1, score + start_in)
        out = count_outputs(out, a, options[k])

    return out
   
# Generate number of steps needed for a win     
wins_per_step = [get_steps(pos[0], 0, 0), get_steps(pos[1], 0, 0)]

# Align two parts
uni_left = [1, 1]
uni_wins = [0, 0]
i = 0
while sum(uni_left) > 0:
    i += 1
    player = 1 - i % 2
    step = (i + 1) // 2
    if step in wins_per_step[player]:
        wins = wins_per_step[player][step]
    else:
        wins = 0
    uni_wins[player] += uni_left[1 - player] * wins
    uni_left[player] = 27 * uni_left[player] - wins
    





