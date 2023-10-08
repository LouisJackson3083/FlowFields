import cv2
import numpy as np
from perlin_noise import PerlinNoise

def get_perlin_flowfield(width, height, seed, octaves):
    noise = PerlinNoise(octaves=octaves, seed=seed)
    canvas = np.zeros(shape=[width, height, 3], dtype=np.uint8)  
    for i in range(height):
        for j in range(width):
            canvas[i, j] = (128 * noise([i/width, j/height]))+127

    return canvas

get_perlin_flowfield(width=128, height=128, seed=123, octaves=4)
