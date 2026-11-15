"""Capa do TikTok iptu-2027-vista-ou-parcelado. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "IPTU 2027", 540, 380, 150, GOLD)
    numero_i(c, "À VISTA OU 10X?", 540, 540, 100, CREME)
    numero_i(c, "A CONTA (PARTE 2)", 540, 670, 64, CREME, contorno=NAVY)
    c.save(); c.translate(780, 1480); c.scale(1.2, 1.2)
    rr(c, -150, -230, 300, 230, 6); rgb(c, (0.96, 0.90, 0.78)); c.fill()
    pg(c, [(-185, -220), (0, -360), (185, -220)]); rgb(c, VERMELHO); c.fill()
    rr(c, -40, -130, 80, 130, 6); rgb(c, (0.55, 0.38, 0.24)); c.fill()
    for x in (-110, 70):
        rr(c, x, -190, 50, 50, 4); rgb(c, (0.62, 0.80, 0.92)); c.fill()
    c.restore()
    consultor_i(c, t, 330, 1640, 1.6, poses=((0, "think"),), exprs=((0, "think"),), look=0.5)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
