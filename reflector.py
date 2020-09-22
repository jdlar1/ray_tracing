from core import OpticalSystem

image_name = 'cielo_nocturno.jpg'

n_vidrio = [1.51, 1.52, 1.53]
n_aire = [1, 1, 1]

reflector = OpticalSystem()
reflector.load(image_name)

reflector.add_space(1.2, n_aire)
reflector.add_plane_mirror()

reflector.trace() # Hacer el trazado matricial de rayos
reflector.plot(save = True) # Graficar

