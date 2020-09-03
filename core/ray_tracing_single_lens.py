"""
Created on Mon Sep 23 14:33:38 2019
@author: catrujilla
"""

import numpy as np
import math 
from PIL import Image

#Ray tracing function
def ray_tracing(width, height, rayo, so, n1, nl, si, obj, pixels):
    
    #Potencia de la superficie
    D1 = (nl - 1)/R1
    D2 = (nl - 1)/(-R2)
    
    #Matriz dela lente
    a1 = (1 - (D2*dl)/nl)
    a2 = -D1-D2+(D1*D2*dl/nl)
    a3 = dl/nl
    a4 = (1 - (D1*dl)/nl)
    A = np.array([[a1,a2],[a3,a4]])

    #Propagaciones despues y antes de la lente
    P2 = np.array([[1,0],[si/n2,1]])
    P1 = np.array([[1,0],[-so/n1,1]])

    for i in range(width):
        for j in range(height):
            
            #Get pixel value
            pos_x = i
            pos_y = j
            pixel = obj.getpixel((pos_x, pos_y))
            
            x = pos_x - width/2
            y = pos_y - height/2
            
            #we must measure the distance from the particular pixel to the center of the object (in pixels)
            #each pixel equals 1 mm
            r = math.sqrt( x*x + y*y ) + 1 #Corrección de redondeo
        
            #Vector rayo de entrada (punto en el objeto)
            y_objeto = r*0.0001 #each pixel equals 0.1 mm

            if rayo == 0: #principal
                alpha_entrada = math.atan(y_objeto/so) #Entra en dirección del centro de la lente
            elif rayo == 1: #paralelo
                alpha_entrada = 0 #Entra paralelo al eje del sistemna óptico
            V_entrada = np.array([n1*alpha_entrada,y_objeto]) 
        
            #Cálculo del vector del rayo de salida
            V_salida = P2.dot(A.dot(P1.dot(V_entrada)))
        
            #Transversal magnification
            y_imagen = V_salida[1]
            if rayo == 0: #principal
                Mt = (-1)*y_imagen/y_objeto #atan correction
            elif rayo == 1: #paralelo
                Mt = y_imagen/y_objeto                

            #Conversion from image coordintes to lens coordinates        
            x_prime = Mt*x
            y_prime = Mt*y
            
            pos_x_prime = int(x_prime + width_output/2)
            pos_y_prime = int(y_prime + height_output/2)
            
            if  pos_x_prime < 0 or pos_x_prime >= width_output:
            	continue
            	
            if  pos_y_prime < 0 or pos_y_prime >= height_output:
            	continue
                     
            if rayo == 0: #principal   
                pixels[pos_x_prime, pos_y_prime] = (int(pixel), int(pixel), int(pixel))
            elif rayo == 1: #paralelo    
                new_gray = (int(pixel) + pixels[pos_x_prime, pos_y_prime][0])/2
                pix_fin = ( int(new_gray), int(new_gray), int(new_gray) )        
                pixels[pos_x_prime, pos_y_prime] = pix_fin

    return pixels
