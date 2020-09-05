from core import OpticalSystem

image_name = 'marte.jpg' 
output_name = 'marte_output.jpg'

reflector = OpticalSystem()
reflector.load(image_name)

reflector.add_space(0.7, n = [1,1,1])

reflector.trace()
reflector.plot()
