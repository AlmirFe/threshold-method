import cv2 as cv
import argparse
import numpy as np
from PIL import Image as im

max_value = 255
max_type = 4
max_binary_value = 255


parser = argparse.ArgumentParser(description='Code for Basic Thresholding Operations tutorial.')
parser.add_argument('--input', help='Path to input image.', default='stuff.jpg')
args = parser.parse_args()
src = cv.imread(cv.samples.findFile(args.input))

if src is None:
    print('Could not open or find the image: ', args.input)
    exit(0)

# Convert the image to Gray
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

def get_thresholding_image(diference):
    position_255 = []
    position_0 = []

    pixelsValues = cv.split(src_gray)[0]

    max_pixel_value = np.max(pixelsValues)
    min_pixel_value = np.min(pixelsValues)
    T = (max_pixel_value + min_pixel_value)/2

    final_threshold = get_final_T(pixelsValues, T, diference, position_255, position_0)

    do_threshold(pixelsValues, final_threshold, position_255, position_0)
    return pixelsValues

def get_final_T(pixelsValues, T, diference, position_255, position_0):
    threshold(T, position_255, position_0, pixelsValues)

    mean_255 = get_mean(position_255, pixelsValues)
    mean_0 = get_mean(position_0, pixelsValues)

    new_T = (mean_0 + mean_255)/2

    while abs(T - new_T) >= diference:
        T = new_T
        position_255.clear()
        position_0.clear()
        threshold(new_T, position_255, position_0, pixelsValues)
        mean_255 = get_mean(position_255, pixelsValues)
        mean_0 = get_mean(position_0, pixelsValues)
        new_T = (mean_0 + mean_255)/2
    
    return new_T

def threshold(T, position_255, position_0, pixelsValues):
    for line in range(len(pixelsValues)):
        for column in range(len(pixelsValues[line])):
            if (pixelsValues[line][column] >= T):
                position_255.append((line, column))
            else :
                position_0.append((line, column))

def get_mean(array, pixelsValues):
    count_array = []
    for i in array:
        line = i[0]
        column = i[1]
        count_array.append(pixelsValues[line][column])
    return np.mean(count_array)

    
def do_threshold(pixelsValues, midle_point, position_255, position_0):
    for line in range(len(pixelsValues)):
        for column in range(len(pixelsValues[line])):
            if (pixelsValues[line][column] >= midle_point):
                pixelsValues[line][column] = 255
            else :
                pixelsValues[line][column] = 0

thresholding_image = get_thresholding_image(0.001)

print(thresholding_image)
data = im.fromarray(thresholding_image)
data.save('image_threshold.png')