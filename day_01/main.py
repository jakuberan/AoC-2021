import numpy as np

if __name__ == "__main__":

    # Define parameters
    data_path = "input"
    last = np.inf
    prevs = []
    cnt_1 = 0
    cnt_2 = 0

    # Read and process
    f = open(data_path, "r")
    for x in f:
        now = int(x)

        # Simple comparison
        if now > last:
            cnt_1 += 1
        last = now

        # Compare with three values back
        prevs.append(int(x))
        if len(prevs) > 3:
            last_3 = prevs.pop(0)
            if last_3 < prevs[2]:
                cnt_2 += 1

    print(f"Increased {cnt_1} times")
    print(f"Smoothed and increased {cnt_2} times")
