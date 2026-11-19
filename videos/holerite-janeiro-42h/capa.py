"""Capa do TikTok: Holerite de janeiro, confira 3 coisas (jornada de 42 h)."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    rr(c, 330, 225, 420, 70, 20); rgb(c, VERMELHO); c.fill()
    text(c, "JORNADA 42h", 540, 275, 46, MARKER, CREME)
    numero_i(c, "HOLERITE DE", 540, 390, 100, CREME)
    numero_i(c, "JANEIRO", 540, 520, 130, GOLD)
    for i, s in enumerate(("1. O SALÁRIO", "2. AS HORAS EXTRAS", "3. O VALOR DA HORA")):
        rr(c, 140, 600 + i * 108, 800, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 180, 664 + i * 108, 52, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 270, 1560, 540, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "CONFIRA 3 COISAS", 540, 1632, 54, MARKER, CREME)


SCENES = [(0, 999, capa)]
