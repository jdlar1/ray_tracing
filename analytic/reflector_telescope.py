# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:41:15 2020

@author: Usuario
"""

from raytracing import *


path = ImagingPath()
path.name = "Telescopio reflector"

# path.objectHeight = 500
# path.fanAngle = 0.5        # full fan angle for rays
# path.fanNumber = 0        # number of rays in fan
# path.rayNumber = 1000        # number of points on object

showEntrancePupil = True
path.append(Space(d=508))
path.append(CurvedMirror(2000, diameter=127, label='Espejo Primario'))
path.append(Space(d=450))
path.append(Aperture(40.64, 'Espejo Secundario'))
path.append(Space(d=63.5))
path.append(Lens(25,13))

path.display()
