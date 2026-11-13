"""Capa do TikTok: Seu 13º já tem dono (o essencial entre y 260 e 1660)."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1100))
    numero_i(c, "SEU 13º", 540, 400, 170, GOLD)
    numero_i(c, "JÁ TEM DONO", 540, 570, 110, CREME)
    numero_i(c, "R$ 1.430 SÓ NO NATAL", 540, 720, 66, CREME, contorno=NAVY)
    pessoa(c, t, 540, 1640, 1.7, "lucas", poses=((0, "head"),), exprs=((0, "desperate"),), look=0.0)
    from math import pi
    for x, cor in ((190, VERDE), (900, BLUE)):
        c.save(); c.translate(x, 1520)
        rr(c, -90, -70, 180, 150, 12); rgb(c, cor); c.fill(); c.rectangle(-14, -100, 28, 180); rgb(c, GOLD); c.fill()
        rr(c, -100, -100, 200, 44, 10); rgb(c, cor); c.fill(); c.rectangle(-14, -100, 28, 44); rgb(c, GOLD); c.fill()
        c.restore()
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
