"""Capa do TikTok decimo-terceiro-3mil-de-verdade. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    numero_i(c, "SEU 13º", 540, 360, 150, GOLD)
    numero_i(c, "VAI VIR MENOR", 540, 510, 100, CREME)
    numero_i(c, "R$ 3.000", 540, 680, 110, CREME)
    c.rectangle(300, 668, 480, 16); rgb(c, VERMELHO); c.fill()
    numero_i(c, "R$ 2.751", 540, 850, 150, VERDE)
    consultor_i(c, t, 540, 1640, 1.25, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
