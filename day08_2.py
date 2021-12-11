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
    
empty_counts = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0}
final_count = 0

for i, nums_test in enumerate(trials):
    counts = empty_counts.copy()
    # Count the digits in test display
    for num_test in nums_test:
        for d in num_test:
            counts[d] += 1
    
    # Assign output digits
    output = ''
    for num_out in display[i]:
        if len(num_out) == 2:
            output += '1'
        elif len(num_out) == 3:
            output += '7'
        elif len(num_out) == 4:
            output += '4'
        elif len(num_out) == 7:
            output += '8'
        elif len(num_out) == 5:
            num_sum = sum([counts[d] for d in num_out])
            if num_sum == 39:
                output += '3'
            elif num_sum == 37:
                output += '5'
            elif num_sum == 34:
                output += '2'
            else:
                print(f'Pattern of length 5 {num_out} not recognized')
        elif len(num_out) == 6:
            num_sum = sum([counts[d] for d in num_out])
            if num_sum == 45:
                output += '9'
            elif num_sum == 42:
                output += '0'
            elif num_sum == 41:
                output += '6'
            else:
                print(f'Pattern of length 6 {num_out} not recognized')
        else:
            print(f'Number {num_out} not recognized')
    final_count += int(output)
    
print(f'Total sum is {final_count}')