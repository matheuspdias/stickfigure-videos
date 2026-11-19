"""Capa do TikTok: R$ 100 por mês desde que o filho nasce, quanto ele tem aos 18."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "R$ 100 POR MÊS", 540, 330, 120, GOLD)
    numero_i(c, "PRO SEU FILHO", 540, 460, 100, CREME)
    linhas = (("GAVETA", "R$ 15 MIL", VERMELHO), ("POUPANÇA", "R$ 25 MIL", NAVY), ("TESOURO IPCA+", "R$ 37 MIL", VERDE))
    for i, (a, b, cor) in enumerate(linhas):
        y = 550 + i * 104
        rr(c, 110, y, 860, 88, 22); rgb(c, CREME); c.fill()
        text(c, a, 150, y + 60, 48, MARKER, NAVY, align="l")
        text(c, b, 930, y + 60, 50, MARKER, cor, align="r")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 110, 1570, 860, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "AOS 18 ANOS, EM DINHEIRO DE HOJE", 540, 1640, 40, MARKER, CREME)


SCENES = [(0, 999, capa)]
