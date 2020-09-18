#from core import OpticalSystem
import numpy as np

image_name = 'marte.jpg' 
output_name = 'marte_output.jpg'

a = np.array([
    [[1, 3], [5, 9], [7, 7]],
    [[3, 9], [0, 1], [9, 1]],
    [[7, 2], [5, 4], [1, 6]]
])



#np.savetxt('matrixR.txt', reflector.transformed[:,:,0])
#np.savetxt('matrixG.txt', reflector.transformed[:,:,1])
#np.savetxt('matrixB.txt', reflector.transformed[:,:,2])