import os
import time

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

class OpticalSystem:

    def __init__(self):
        self.A = None
        self.d0 = None

    def load(self, image_name, output_size = None):
        self.image = img.imread(os.path.join('images', image_name))
        self.ishape = self.image.shape

        self.x_abs = np.arange(self.ishape[1])
        self.y_abs = np.arange(self.ishape[0])

        self.x_rel = self.x_abs - self.ishape[1]/2
        self.y_rel = self.y_abs - self.ishape[0]/2


        if output_size is None:
            self.output_size = self.ishape
        else:
            self.output_size = output_size

        print()
        print(f'Imagen {image_name} cargada')

    def add_space(self, d, n = 1):
        # Transfer matrix

        if type(n) in [int, float]:
            n0 = [n,n,n]
        else:
            n0 = n.copy() 

        if self.A is None:
            self.A = [0,0,0]
            self.A[0] = np.array([[1, 0],[d/n0[0], 1]])
            self.A[1] = np.array([[1, 0],[d/n0[1], 1]])
            self.A[2] = np.array([[1, 0],[d/n0[2], 1]])
        else:
            self.A[0] = self.A[0].dot(np.array([[1, 0],[d/n0[0], 1]]))
            self.A[1] = self.A[1].dot(np.array([[1, 0],[d/n0[1], 1]]))
            self.A[2] = self.A[2].dot(np.array([[1, 0],[d/n0[2], 1]]))

        if self.d0 == None:
            self.d0 = d 
            self.n0 = n0

    def add_plane_mirror(self):
        # Mirror matrix
        self.A[0] = self.A[0].dot(np.array([[-1, 0], [1, 0]]))
        self.A[1] = self.A[1].dot(np.array([[-1, 0], [1, 0]]))
        self.A[2] = self.A[2].dot(np.array([[-1, 0], [1, 0]]))

    def add_single_lens(self, R1, R2, nl, dl):
        # Surfaces power
        nl_ = np.array(nl) 

        D1 = (nl_ - 1)/R1
        D2 = (nl_ - 1)/(-R2)

        # Lens Matrix
        a1 = (1 - (D2*dl)/nl_)
        a2 = -D1-D2+(D1*D2*dl/nl_)
        a3 = dl/nl_
        a4 = (1 - (D1*dl)/nl_)

        #Modify global A
        self.A[0] = self.A[0].dot(np.array([[a1[0],a2[0]],[a3[0],a4[0]]]))
        self.A[1] = self.A[1].dot(np.array([[a1[1],a2[1]],[a3[1],a4[1]]]))
        self.A[2] = self.A[2].dot(np.array([[a1[2],a2[2]],[a3[2],a4[2]]]))

    def trace(self, output_size = None ):

        if output_size is None:
            self.transformed = np.full((self.ishape[0], self.ishape[1], 3), fill_value= 255, dtype=np.uint8) # Crear la matriz de salida
        else:
            self.transformed = np.full((output_size[1], output_size[0], 3), fill_value= 255, dtype=np.uint8) # Crear la matriz de salida
            # output_size debe ser [width, height] 
        
        print()
        print('Comienza trazado de rayos')
        start = time.time() # Tiempo al empezar

        for index, A in enumerate([*self.A]):
            pixels = np.zeros((self.ishape[0], self.ishape[1]))
            for rayo in [0,1]:
                for x in self.x_rel:
                    for y in self.y_rel:

                        r = np.sqrt(x**2+y**2)

                        y_obj = r*0.0001

                        if rayo == 0:
                            alpha_entrada = np.arctan(y_obj/self.d0)
                        elif rayo == 1:
                            alpha_entrada = 0

                        v_in = np.array([self.n0[index]*alpha_entrada,y_obj])
                        v_out = A.dot(v_in)

                        y_image = v_out[0]

                        mt = y_image/y_obj

                        x_ = mt*x
                        y_ = mt*y

                        pos_x_prime = int(x_ + self.output_size[1]/2)
                        pos_y_prime = int(y_ + self.output_size[0]/2)

                        pixel_coords = (x + (self.ishape[1]/2), y + (self.ishape[0]/2))

                        pixel = self.image[int(pixel_coords[0]), int(pixel_coords[1]), index]

                        if  pos_x_prime < 0 or pos_x_prime >= self.output_size[1]:
                            continue
                        
                        if  pos_y_prime < 0 or pos_y_prime >= self.output_size[0]:
                            continue
                                
                        if rayo == 0: #principal   
                            pixels[pos_x_prime, pos_y_prime] = int(pixel)

                        elif rayo == 1: #paralelo    
                            new_value = int((pixels[pos_x_prime, pos_y_prime]+pixel)/2)
                            pixels[pos_x_prime, pos_y_prime] = new_value
            
            self.transformed[:, :, index] =  pixels
        
        stop = time.time()  # Tiempo al terminar
        print(f'Trazado de rayos hecho en {stop-start:.2f} segundos')
        print()

    def plot(self, save = False):
        fig, ax = plt.subplots(1, 2, figsize = (15,7))

        ax[0].imshow(self.image)
        ax[0].set_title('Imagen original', fontsize = 14)

        ax[1].imshow(self.transformed)
        ax[1].set_title('Imagen final', fontsize = 14)

        if save:
            fig.savefig(os.path.join('outputs', save))

        plt.show(block = True)
        