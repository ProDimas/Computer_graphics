from PIL import Image, ImageDraw
from math import cos, sin, radians, ceil, floor
import numpy as np
from itertools import product
import os

IMAGE_WIDTH = 960
IMAGE_HEIGHT = 960
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
ROT_CENTER = (480, 480)
LAST_DIGIT_OF_LOGIN = 7
θ = radians(-10 * (LAST_DIGIT_OF_LOGIN + 1))

def read_ds7_data() -> list[str]:
    data = []
    ds7 = open(os.path.dirname(__file__) + '/DS7.txt', 'r')
    for line in ds7:
        data.append(reverse_coordinate(tuple(map(int, line[:-1].split(' ')))))
    ds7.close()
    return data

def reverse_coordinate(coord: tuple[int]) -> tuple[int]:
    return (coord[1], IMAGE_HEIGHT - coord[0])


def transform(pixels: list[tuple[int]]) -> list[tuple[int]]:
    transform_matrix = get_transform_matrix()
    new_pixels = []
    funcs = list(product([ceil, floor], repeat=2))
    for pixel in pixels:
        pixel = np.array(pixel + (1, ))
        pixel_transformed = np.matmul(pixel, transform_matrix)
        rounded_pixels = [(f1(pixel_transformed[0]), f2(pixel_transformed[1])) for f1, f2 in funcs]
        new_pixels += rounded_pixels
    return new_pixels

def get_transform_matrix() -> np.ndarray:
    return np.array([[cos(θ), sin(θ), 0],
                     [-sin(θ), cos(θ), 0],
                     [ROT_CENTER[0] * (1 - cos(θ)) + ROT_CENTER[1] * sin(θ), ROT_CENTER[1] * (1 - cos(θ)) - ROT_CENTER[0] * sin(θ), 1]])

ds7image = Image.new(mode='RGB', size=IMAGE_SIZE, color=(255, 255, 255))
ds7draw = ImageDraw.Draw(ds7image, mode='RGB')
pixels = read_ds7_data()
for pixel in pixels:
    ds7draw.point(pixel, fill=(0, 0, 0))

try:
    ds7image.save(os.path.dirname(__file__) + '/before_transformation.' + input('Enter the format of an \'before_transformation\' image: '))
except ValueError as e:
    print(e)

ds7draw.rectangle(xy=((0, 0), IMAGE_SIZE), fill=(255, 255, 255))
for pixel in transform(pixels):
    ds7draw.point(pixel, fill=(70, 130, 180))

try:
    ds7image.save(os.path.dirname(__file__) + '/after_transformation.' + input('Enter the format of an \'after_transformation\' image: '))
except ValueError as e:
    print(e)