from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np


image = img.imread('images/arrow_1.jpg')

print(f'Image size: {image.shape}')
print()
# print(f'Red: \n {image[:,:,0]}')
# print(f'Green: \n {image[:,:,1]}')
# print(f'Blue: \n {image[:,:,2]}')

