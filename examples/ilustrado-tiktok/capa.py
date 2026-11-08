"""Capa do TikTok no estilo ilustrado. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "verde", holofote=(540, 1050))
    numero_i(c, "R$ 10/DIA", 540, 420, 170, GOLD)
    numero_i(c, "VIRA QUANTO?", 540, 600, 110, CREME)
    consultor_i(c, t, 540, 1640, 1.75, poses=((0, "arms_up"),), exprs=((0, "shocked"),), look=0.0)
    for x, n in ((170, 10), (910, 14)):
        c.save(); c.translate(x, 1600); pilha_moedas(c, n, 60); c.restore()
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
