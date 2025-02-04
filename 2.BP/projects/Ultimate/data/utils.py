
import struct
import numpy as np


def load_labels(file):
    with open(file, "rb") as f:
        data = f.read()
    
    magic_number, num_samples = struct.unpack(">ii", data[:8])
    if magic_number != 2049:   # 0x00000801
        print(f"magic number mismatch {magic_number} != 2049")
        return None
    
    labels = np.frombuffer(data[8:], dtype=np.uint8)
    return labels

def load_images(file):
    with open(file, "rb") as f:
        data = f.read()

    magic_number, num_samples, image_width, image_height = struct.unpack(">iiii", data[:16])
    if magic_number != 2051:   # 0x00000803
        print(f"magic number mismatch {magic_number} != 2051")
        return None
    
    image_data = np.frombuffer(data[16:], dtype=np.uint8).reshape(num_samples, -1)
    # return image_data.reshape(-1, image_height, image_width)
    return image_data


def one_hot(labels, classes=10, label_smoothing=0):
    n = len(labels)
    eoff = label_smoothing / classes
    output = np.ones((n, classes), dtype=np.float32) * eoff
    output[np.arange(n), labels] = 1 - label_smoothing + eoff
    return output

