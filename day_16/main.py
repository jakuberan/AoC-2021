def hex_to_bin():
    """
    Basic mapping from hex to bin
    """
    htob = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    return htob


def read_data(data_path, htob):
    """
    Reads data
    """
    f = open(data_path, "r")
    for x in f:
        data = "".join([htob[c] for c in x.strip()])
    return data


def product(numbers):
    result = 1
    for n in numbers:
        result = result * n
    return result


def decode_data(data, subs=0, i=0):
    ver = 0
    nums = []

    while (
        (len(data) > i)
        and ((subs == 0) or (len(nums) < subs))
        and (int(data[i:], 2) > 0)
    ):
        ver += int(data[i : (i + 3)], 2)
        typ = int(data[(i + 3) : (i + 6)], 2)
        i += 6
        if typ == 4:
            num = ""
            while data[i] == "1":
                num += data[(i + 1) : (i + 5)]
                i += 5
            num += data[(i + 1) : (i + 5)]
            i += 5
            nums.append(int(num, 2))
        else:
            if data[i] == "0":
                if typ in [5, 6, 7]:
                    sub_num = 2
                else:
                    sub_num = 0
                sub_len = int(data[(i + 1) : (i + 16)], 2)
                n_sub, v_sub, _ = decode_data(
                    data[: (i + 16 + sub_len)], sub_num, i + 16
                )
                i += 16 + sub_len
            else:
                sub_num = int(data[(i + 1) : (i + 12)], 2)
                n_sub, v_sub, i = decode_data(data, sub_num, i + 12)
            ver += v_sub
            if typ == 0:
                nums.append(sum(n_sub))
            elif typ == 1:
                nums.append(product(n_sub))
            elif typ == 2:
                nums.append(min(n_sub))
            elif typ == 3:
                nums.append(max(n_sub))
            elif typ == 5:
                nums.append(1 if n_sub[0] > n_sub[1] else 0)
            elif typ == 6:
                nums.append(1 if n_sub[0] < n_sub[1] else 0)
            elif typ == 7:
                nums.append(1 if n_sub[0] == n_sub[1] else 0)
            else:
                print("Unknown type")

    return nums, ver, i


if __name__ == "__main__":

    # Read data
    data_path = "input"
    htob = hex_to_bin()
    data = read_data(data_path, htob)

    # Perform steps of calculation
    num, ver, i = decode_data(data)

    print(f"Sum of version numbers is {ver}")
    print(f"Evaluated package is {num[0]}")
