import numpy as np
from scipy.signal import convolve2d


def read_data(data_path):
    """
    Reads data
    """
    mapping = None
    image = []
    f = open(data_path, "r")
    for x in f:
        if len(x.strip()) > 0:
            if mapping is None:
                mapping = [1 if c == "#" else 0 for c in x.strip()]
            else:
                image.append([1 if c == "#" else 0 for c in x.strip()])

    return np.array(mapping), np.array(image)


if __name__ == "__main__":

    kernel = np.reshape([2 ** i for i in range(9)], (3, 3))

    for part in [1, 2]:

        # Read data, define steps
        data_path = "input"
        mapping, image = read_data(data_path)
        steps = 50 if part == 2 else 2

        for i in range(steps):
            # Define fill value for convolution
            fillvalue = 0 if mapping[0] * (i % 2) == 0 else 1

            # 2D convolution from scipy
            image_conv = convolve2d(image, kernel, fillvalue=fillvalue)

            # Flatten, apply mapping and reshape
            image_flat = [int(pix) for pix in image_conv.flatten()]
            new_image_flat = mapping[image_flat]
            image = np.reshape(new_image_flat, image_conv.shape)

        print(f"There are {sum(sum(image))} pixels lit in resulting image")
