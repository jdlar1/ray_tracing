# ray_tracing

This library is used to simulate the imaging of a simple optical instrument composed of:
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

reflector.add_space(d = 5.756e10)
reflector.add_curved_mirror(R = 2)
reflector.add_space(d = 0.508)
reflector.add_single_lens()

reflector.trace(ray_count = 15)
reflector.plot(save = True) 
```
