# Define path
data_path = "data/input21"

# Define parameters
goal = 1000
pos = []

# Read line-by-line
f = open(data_path, "r")
for x in f:
    pos.append(int(x.strip().split(' ')[-1]))
  
# Generate steps per player
steps1 = [((i + 1) * 3 % 10) for i in range(1, 60, 6)]
steps2 = [((i + 1) * 3 % 10) for i in range(4, 60, 6)]  
  
# Generate basic scores 
def gen_score10(pos0, steps):
    # Generates base score after 10 steps
    score = []
    for s in steps:
        pos0 = (pos0 + s - 1) % 10 + 1
        if len(score) == 0:
            score.append(pos0)
        else:
            score.append(pos0 + score[-1])
    return score

# Scores after 10 steps
score1 = gen_score10(pos[0], steps1)
score2 = gen_score10(pos[1], steps2)

# Number of 10 step rounds per player
rounds1 = goal // score1[-1]
rounds2 = goal // score2[-1]
rounds = min(rounds1, rounds2)

# Generate exact number of steps and score for the other player
score_final1 = score1[-1] * rounds
score_final2 = score2[-1] * rounds
i = 0

while max(score_final1, score_final2) < goal:
    score_temp = score_final2
    if i == 0:
        score_final1 += score1[i]
        score_final2 += score2[i]
    else:
        score_final1 += score1[i] - score1[i - 1]
        score_final2 += score2[i] - score2[i - 1]
    i += 1

score_min = min(score_final1, score_temp)
rolled = rounds * 60 + (i - 1) * 6 + 3 * (goal <= score_final1)
print(f'Result is {score_min * rolled}')
