"""Capa do TikTok milhao-no-pix. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "verde", holofote=(540, 1100))
    numero_i(c, "R$ 1 MILHÃO", 540, 380, 150, GOLD)
    numero_i(c, "NO SEU PIX", 540, 540, 110, CREME)
    numero_i(c, "QUANTO TEMPO DURA?", 540, 680, 72, CREME, contorno=NAVY)
    chuva_dinheiro(c, 1.0, 0.0, n=18, seed=5)
    pessoa(c, t, 540, 1640, 1.6, "lucas", poses=((0, "arms_up"),), exprs=((0, "shocked"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
