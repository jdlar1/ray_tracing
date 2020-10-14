from core import OpticalSystem

image_name = 'marte.jpg'

n_glass = [1.517, 1.520, 1.526] # Vídrio óptico
n_air = [1, 1, 1] # Aire

reflecting = OpticalSystem()
reflecting.load(image_name, image_height = 6.7e6)#image_height = 6.779e6

so = 6.2e10
si = (so)/(1-so)
print(f'si: {si}')
print(f'mg: {abs(si/so)}')

reflecting.add_space(d = so)
reflecting.add_curved_mirror(R = -2)
reflecting.add_space(si)
reflecting.add_space(d = -1.2)
reflecting.add_single_lens(-0.3, 0.3, n_glass, dl = -0.005)
reflecting.add_space(d = -0.4)

reflecting.trace(ray_count = 3, magnification = 1.0e10, save_rays = True) # Hacer el trazado matricial de rayos
reflecting.plot(save = True) # Graficar