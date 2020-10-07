# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:41:15 2020

@author: Usuario
"""

from raytracing import *


path = ImagingPath()

# path.fanAngle = 0.1        # full fan angle for rays
# path.fanNumber = 100        # number of rays in fan
# path.rayNumber = 100        # number of points on object

path.append(Space(d=508))
path.append(CurvedMirror(2000, diameter=127, label='Espejo Primario'))
path.append(Space(d=450))
path.append(Aperture(40.64, 'Espejo Secundario'))

# path.append(Space(d=25))
# path.append(Lens(2,5))
path.display()