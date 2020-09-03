import os

from PIL import Image
import numpy as np

from core.ray_tracing_single_lens import ray_tracing


image_name = 'saturn.jpg' 
output_name = 'saturn_output.jpg'

#Lente biconvexa
R1 = 0.3
R2 = -0.3
dl = 0.01
nl = 1.5

#calculamos la focal de la lente
f = R1*R2/((R2-R1)*(nl-1))
print("focal: ", f)

#Propagaciones en el aire antes y despues de la lente
#Después
si = 0.526 #Distancia desde el verticce del lente hasta el plano imagen
#si = 0.751
n2 = 1 #Indice de refracción del aire 

so = 0.7 #Distancia desde el verticce del lente hasta el plano objeto
#so = 0.5
so = 1.2

#to guarantee image plane
si = (f*so)/(so-f)
print("si: ", si)

n1 = 1 #Indice de refracción del aire 

#Magnification
Mt = -si/so
print ("Mt: ", Mt)

#load image (Object!)
obj = Image.open(os.path.join('images',image_name) , 'r')
width, height = obj.size

width_output = int(width*(abs(Mt)))
height_output = int(height*(abs(Mt)))

# Create new Image and a Pixel Map
image = Image.new("RGB", (width_output, height_output), 'black')
pixels = image.load()
                
pixels = ray_tracing(width, height, 0, so, n1,nl ,si , obj, pixels)
pixels = ray_tracing(width, height, 1, so, n1,nl ,si , obj, pixels)

#Save Images to File
image.save(os.path.join('outputs', output_name), format='PNG')