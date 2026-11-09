"""Capa do TikTok aluguel-jogar-dinheiro-fora. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1080))
    numero_i(c, "ALUGUEL É", 540, 380, 130, CREME)
    numero_i(c, "JOGAR DINHEIRO", 540, 520, 100, CREME)
    numero_i(c, "FORA?", 540, 680, 170, GOLD)
    pessoa(c, t, 220, 1640, 1.45, "ana", poses=((0, "point_ru"),), exprs=((0, "grin"),), look=0.4)
    pessoa(c, t, 860, 1640, 1.45, "bruno", poses=((0, "hips"),), exprs=((0, "confident"),), look=-0.4)
    consultor_i(c, t, 540, 1660, 1.15, poses=((0, "think"),), exprs=((0, "think"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
