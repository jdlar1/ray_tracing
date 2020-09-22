import os
import time

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

class OpticalSystem:

    def __init__(self):
        self.A = None
        self.d0 = None

    def load(self, image_name):
        self.image = img.imread(os.path.join('images', image_name))  # Cargar la imagen
        self.image = self.image.astype(np.int16)
        self.ishape = self.image.shape  # Tamaño de la imagen

        self.x_abs = self.ishape[1] # Tamaño de x
        self.y_abs = self.ishape[0] # Tamaño de y

        self.x_mid = self.x_abs/2
        self.y_mid = self.y_abs/2

        self.pixel_height = 0.127/np.min([self.x_abs, self.y_abs])

        print()
        print(f'Imagen {image_name} cargada')

        self.output_name = f'{image_name[:image_name.find(".")]}_output.jpg'  # Nombre del archivo de salida

    def add_space(self, d, n = 1):
        # Transfer matrix

        if type(n) in [int, float]:
            n0 = np.array([n,n,n])
        else:
            n0 = np.array(n)

        if self.A is None:
            self.A = [0,0,0]
            self.A[0] = np.array([[1, 0],[d/n0[0], 1]])
            self.A[1] = np.array([[1, 0],[d/n0[1], 1]])
            self.A[2] = np.array([[1, 0],[d/n0[2], 1]])
        else:
            self.A[0] = np.array([[1, 0],[d/n0[0], 1]]).dot(self.A[0])
            self.A[1] = np.array([[1, 0],[d/n0[1], 1]]).dot(self.A[1])
            self.A[2] = np.array([[1, 0],[d/n0[2], 1]]).dot(self.A[2])

        if self.d0 == None:
            self.d0 = d 
            self.n0 = n0

    def add_plane_mirror(self):

        # Matriz del espejo
        self.A[0] = np.array([[-1, 0], [1, 0]]).dot(self.A[0])
        self.A[1] = np.array([[-1, 0], [1, 0]]).dot(self.A[1])
        self.A[2] = np.array([[-1, 0], [1, 0]]).dot(self.A[2])

    def add_single_lens(self, R1, R2, nl, dl):

        if type(nl) in [int, float]:
            n0 = np.array([nl,nl,nl])
        else:
            n0 = np.array(nl)

        # Poder de las superficies
        D1 = (n0 - 1)/R1
        D2 = (n0 - 1)/(-R2)

        # Términos de la matriz de lentes
        a1 = (1 - (D2*dl)/n0)
        a2 = -D1-D2+(D1*D2*dl/n0)
        a3 = dl/n0
        a4 = (1 - (D1*dl)/n0)

        # Modificar la A global 
        self.A[0] = np.array([[a1[0],a2[0]],[a3[0],a4[0]]]).dot(self.A[0])
        self.A[1] = np.array([[a1[1],a2[1]],[a3[1],a4[1]]]).dot(self.A[1])
        self.A[2] = np.array([[a1[2],a2[2]],[a3[2],a4[2]]]).dot(self.A[2])

    def add_curved_mirror(self, R, n = 1):

        if type(n) in [int, float]:
            n0 = [n,n,n]
        else:
            n0 = n.copy()
        
        self.A[0] = np.array([[-1, -2*n0[0]/R], [0, 1]]).dot(self.A[0])
        self.A[1] = np.array([[-1, -2*n0[1]/R], [0, 1]]).dot(self.A[1])
        self.A[2] = np.array([[-1, -2*n0[2]/R], [0, 1]]).dot(self.A[2])

    def trace(self, output_size = None ):

        if output_size is None:
            self.transformed = np.full((self.y_abs, self.y_abs, 3), fill_value= 0, dtype=np.int16) # Crear la matriz de salida
        else:
            self.transformed = np.full((output_size[1], output_size[0], 3), fill_value= 0, dtype=np.int16) # Crear la matriz de salida
            # output_size debe ser (width, height)

        self.output_size = self.transformed.shape

        print(self.output_size)

        print()
        print('Comienza trazado de rayos')
        start = time.time() # Tiempo al empezar

        for rayo in [0,1]:
            for idx, pixel in np.ndenumerate(self.image):

                x = idx[1] - self.x_mid  # Conversión a coordenadas centradas
                y = idx[0] - self.y_mid

                r = np.sqrt(x**2+y**2) # Distancia desde el origen al punto
                y_obj = r*self.pixel_height  # Multiplicación por la unidad en metros de cada píxel

                if rayo == 0: # Rayo principal
                    alpha_entrada = np.arctan(y_obj/self.d0)
                elif rayo == 1: # Rayo paralelo
                    alpha_entrada = 0

                if y_obj == 0:
                    continue

                v_in = np.array([self.n0[idx[2]]*alpha_entrada,y_obj])
                v_out = self.A[idx[2]].dot(v_in)

                y_image = v_out[0]
                mt = y_image/y_obj

                x_ = mt*x
                y_ = mt*y

                pos_x_prime = int(x_ + self.output_size[1]/2)
                pos_y_prime = int(y_ + self.output_size[0]/2)

                pixel_coords = (x + (self.x_abs/2), y + (self.y_abs/2))

                pixel = self.image[int(pixel_coords[0]), int(pixel_coords[1]), idx[2]]

                if  pos_x_prime < 0 or pos_x_prime >= self.output_size[1]:
                    continue
                
                if  pos_y_prime < 0 or pos_y_prime >= self.output_size[0]:
                    continue
                        
                if rayo == 0: #principal   
                    self.transformed[pos_x_prime, pos_y_prime, idx[2]] = int(pixel)

                elif rayo == 1: #paralelo    
                    new_value = int((self.transformed[pos_x_prime, pos_y_prime, idx[2]]+pixel)/2)
                    self.transformed[pos_x_prime, pos_y_prime, idx[2]] = new_value
        
        center_color1 = self.image[int(self.y_mid+1), int(self.x_mid+1), :]
        center_color2 = self.image[int(self.y_mid-1), int(self.x_mid-1), :]

        self.transformed[int(self.y_mid), int(self.x_mid), :] = (center_color1+ center_color2)/2
    
        stop = time.time()  # Tiempo al terminar


    def plot(self, save = False):
        fig, ax = plt.subplots(1, 2, figsize = (14,6))

        ax[0].imshow(self.image)
        ax[0].set_title('Imagen original', fontsize = 14)

        ax[1].imshow(self.transformed)
        ax[1].set_title('Imagen final', fontsize = 14)

        if save:
            fig.savefig(os.path.join('outputs', self.output_name))

        plt.show(block = True)
        