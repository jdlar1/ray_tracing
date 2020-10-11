from core import OpticalSystem

image_name = 'marte.jpg'

n_glass = [1.517, 1.520, 1.526] # Vídrio óptico
n_air = [1, 1, 1] # Aire

reflecting = OpticalSystem()
reflecting.load(image_name, image_height = 0.01)

reflecting.add_space(1.2)
reflecting.add_single_lens(0.3, -0.3, n_glass, 0)
reflecting.add_space(0.4)

reflecting.trace(ray_count = 3, magnification = 1, save_rays =True) # Hacer el trazado matricial de rayos
reflecting.plot(save = True) # Graficar


