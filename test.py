from core import OpticalSystem
import numpy as np

image_name = 'marte.jpg' 
output_name = 'marte_output.jpg'

reflector = OpticalSystem()
reflector.load(image_name)

reflector.add_space(70, n = [1,1,1])

reflector.trace()
reflector.plot()


#np.savetxt('matrixR.txt', reflector.transformed[:,:,0])
#np.savetxt('matrixG.txt', reflector.transformed[:,:,1])
#np.savetxt('matrixB.txt', reflector.transformed[:,:,2])