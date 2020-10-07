from core import OpticalSystem

image_name = 'cielo_nocturno.jpg'

n_vidrio = [1.51, 1.52, 1.53]
n_aire = [1, 1, 1]

reflector = OpticalSystem()
reflector.load(image_name)

reflector.add_space(d = 5.756e10)   # Distancia Tierra - Marte
reflector.add_curved_mirror(R = 2)  # Curvatura del espejo
reflector.add_space(d = 0.508)
reflector.add_single_lens()

reflector.trace(ray_count = 15) # Hacer el trazado matricial de rayos
reflector.plot(save = True) # Graficar

