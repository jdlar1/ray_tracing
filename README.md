# ray_tracing

This library is used to simulate the image forming of a simple optical instrument composed of:
- Spaces
- Gross lenses
- Plane and curved mirrors

## Installing

You will need other packages specified in `requirements.txt`. To install all of them run `pip install -r requirements.txt`

## Use

First create an instance of `OpticalSystem` then load an image and add all the elements your instrument has. Do the raytracing with `trace` method. Example:  

```python
from core import OpticalSystem

image_name = 'cielo_nocturno.jpg'

reflector = OpticalSystem()
reflector.load(image_name)

reflector.add_space(1.2)
reflector.add_single_lens(0.3, -0.3, n_vidrio,  0.01)
reflector.add_space(0.42)

reflector.trace(ray_count = 5)
reflector.plot(save = True) 
```
## Files

- **Reflector.py:** main file, run with  `python reflector.py`.
- **Analytics.py (folder):** All related with analytic ray tracing. Uses raytracing library.
- **Core(folder)**: The package where OpticalSystem is
- **Outputs(folder):** Is where all images are rendered.
- **Images(folder):** All images that main file will use must be here.
- **Files ended in .npy:** Are the processed images that has the information of each ray is composed of in a 4th-dimensional tensor. Can be opened with `prueba_de_rayos.ipynb`.
