from core import OpticalSystem

image_name = 'marte.jpg'

n_vidrio = [1.51, 1.52, 1.53]
n_aire = [1, 1, 1]

reflector = OpticalSystem()
reflector.load(image_name)

reflector.add_space(d = 5.756e10) # Distancia Tierra - Marte


reflector.trace(ray_count = 2) # Hacer el trazado matricial de rayos
reflector.plot(save = True) # Graficar

