from core import OpticalSystem

image_name = 'marte.jpg' 
output_name = 'marte_output.jpg'

# Load settings
reflector = OpticalSystem() # Instanciar la clase
reflector.load(image_name)  # Cargar la imagen



reflector.add_space(2, n = [1.30,1.32,1.35]) # Añadir espacio de 2 m con n = 1 (aire)
reflector.add_plane_mirror()

reflector.trace() # Hacer el trazado matricial de rayos
reflector.plot(save = output_name) # Graficar
