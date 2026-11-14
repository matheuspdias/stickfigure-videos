"""Capa do TikTok ipva-2027-vista-ou-parcelado. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "IPVA 2027", 540, 380, 150, GOLD)
    numero_i(c, "À VISTA OU 5X?", 540, 540, 100, CREME)
    numero_i(c, "A CONTA (PARTE 1)", 540, 670, 64, CREME, contorno=NAVY)
    c.save(); c.translate(760, 1500); carro_i(c, 0, (0.86, 0.26, 0.22)); c.restore()
    consultor_i(c, t, 330, 1640, 1.6, poses=((0, "think"),), exprs=((0, "think"),), look=0.5)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
