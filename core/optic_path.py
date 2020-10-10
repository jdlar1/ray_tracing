import os
import time

import matplotlib.pyplot as plt
import matplotlib.image as img
from matplotlib_scalebar.scalebar import ScaleBar, SI_LENGTH
import numpy as np

class OpticalSystem:

    def __init__(self):
        self.A = None
        self.d0 = None

    def load(self, image_name, image_height = 3389500):
        self.image = img.imread(os.path.join('images', image_name))  # Cargar la imagen
        self.image = self.image.astype(np.uint8)
        self.ishape = self.image.shape  # Tamaño de la imagen

        self.x_abs = self.ishape[1] # Tamaño de x
        self.y_abs = self.ishape[0] # Tamaño de y

        self.x_mid = self.x_abs/2
        self.y_mid = self.y_abs/2

        self.pixel_height = image_height/self.y_abs

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

            self.d0 = d 
            self.n0 = n0
        else:
            self.A[0] = np.array([[1, 0],[d/n0[0], 1]]).dot(self.A[0])
            self.A[1] = np.array([[1, 0],[d/n0[1], 1]]).dot(self.A[1])
            self.A[2] = np.array([[1, 0],[d/n0[2], 1]]).dot(self.A[2])

    def add_plane_mirror(self):

        # Matriz del espejo
        self.A[0] = np.array([[-1, 0], [0, 1]]).dot(self.A[0])
        self.A[1] = np.array([[-1, 0], [0, 1]]).dot(self.A[1])
        self.A[2] = np.array([[-1, 0], [0, 1]]).dot(self.A[2])

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

    def trace(self, ray_count = 2, output_size = None, save_rays = False, magnification = 1):

        if output_size is None:
            self.transformed = np.zeros((self.y_abs, self.y_abs, 3), dtype=np.uint8) # Crear la matriz de salida
        else:
            self.transformed = np.zeros((output_size[1], output_size[0], 3), dtype=np.uint8) # Crear la matriz de salida
            # output_size debe ser (width, height)

        self.output_size = self.transformed.shape
        self.magnification = magnification

        print(self.output_size)

        print()
        print('Comienza trazado de rayos')
        print()

        start = time.time() # Tiempo al empezar
        
        temporal_matrix = np.zeros((*self.output_size, ray_count), dtype=np.uint8)
        progress, total_progress = 0, self.image.size

        for index, pixel in np.ndenumerate(self.image):

            progress_bar(progress, total_progress, prefix = 'Progreso:', suffix = 'Completado', length = 70)
            progress += 1
            
            x = index[1] - self.x_mid  # Conversión a coordenadas centradas
            y = index[0] - self.y_mid

            r = np.sqrt(x**2+y**2) # Distancia desde el origen al punto
            y_obj = (r*self.pixel_height)  # Multiplicación por la unidad en metros de cada píxel

            if y_obj == 0:
                continue

            alpha_principal = -np.arctan(y_obj/self.d0)

            for ray_num, alpha in enumerate(np.linspace(alpha_principal, 0, ray_count, )):

                v_in = np.array([self.n0[index[2]]*alpha, y_obj])
                v_out = self.A[index[2]].dot(v_in)

                y_image = v_out[1]
                mg = (y_image/y_obj)*magnification

                x_ = mg*x
                y_ = mg*y

                pos_x_prime = int(x_ + self.output_size[1]/2)
                pos_y_prime = int(y_ + self.output_size[0]/2)

                if (pos_x_prime < 0) or (pos_x_prime >= self.output_size[1]):
                    continue
                
                if (pos_y_prime < 0) or (pos_y_prime >= self.output_size[0]):
                    continue

                temporal_matrix[pos_y_prime, pos_x_prime, index[2], ray_num] = pixel

        self.transformed = temporal_matrix/255
        
        center_color1 = self.image[int(self.y_mid+1), int(self.x_mid+1), :] # Correción del píxel central
        center_color2 = self.image[int(self.y_mid-1), int(self.x_mid-1), :]
    
        stop = time.time()  # Tiempo al terminar
        print()
        print(f'Trazado de rayos finalizado en {(stop-start):.2f} segundos')
        print()

        if save_rays == True:
            np.save(f'{image_name[:image_name.find(".")]}_matrix_output.npy', self.transformed)

    def plot(self, save = False):
        fig, ax = plt.subplots(1, 2, figsize = (14,6))

        ax[0].imshow(self.image)
        ax[0].set_title('Imagen original', fontsize = 14)
        ax[0].add_artist(ScaleBar(self.pixel_height, 'm')) # Barra de escala


        ax[1].imshow(self.transformed.mean(3))
        ax[1].set_title('Imagen final', fontsize = 14)
        ax[1].add_artist(ScaleBar(self.pixel_height/self.magnification, 'm'))

        if save:
            fig.savefig(os.path.join('outputs', self.output_name))

        plt.show(block = True)
        

def progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()