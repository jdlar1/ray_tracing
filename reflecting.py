from core import OpticalSystem

image_name = 'marte.jpg'

n_glass = [1.517, 1.520, 1.526] # Vídrio óptico
n_air = [1, 1, 1] # Aire

reflecting = OpticalSystem()
reflecting.load(image_name, image_height = 0.1)

reflecting.add_space(d = 5.756e10)
reflecting.add_curved_mirror(R = -2)
reflecting.add_space(d = -2.2)
reflecting.add_single_lens(-0.3, 0.3 , n_glass, 0.01)
reflecting.add_space(d = -0.40)

reflecting.trace(ray_count = 5, magnification = 7) # Hacer el trazado matricial de rayos
reflecting.plot(save = True) # Graficar


