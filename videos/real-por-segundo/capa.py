"""Capa do TikTok real-por-segundo. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "verde", holofote=(540, 1100))
    numero_i(c, "R$ 1", 540, 400, 220, GOLD)
    numero_i(c, "POR SEGUNDO", 540, 580, 110, CREME)
    numero_i(c, "QUANTO VOCÊ TERIA?", 540, 720, 72, CREME, contorno=NAVY)
    chuva_dinheiro(c, 1.0, 0.0, n=18, seed=7)
    c.save(); c.translate(800, 1420); pilha_moedas(c, 12, 100); c.restore()
    pessoa(c, t, 420, 1640, 1.6, "lucas", poses=((0, "arms_up"),), exprs=((0, "shocked"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
