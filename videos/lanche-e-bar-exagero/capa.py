"""Capa do TikTok lanche-e-bar-exagero. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1080))
    numero_i(c, "R$ 300/MÊS", 540, 400, 150, GOLD)
    numero_i(c, "EM LANCHE E BAR", 540, 560, 96, CREME)
    numero_i(c, "É EXAGERO?", 540, 720, 140, CREME)
    pessoa(c, t, 830, 1640, 1.45, "lucas", poses=((0, "shrug"),), exprs=((0, "grin"),), look=-0.4)
    consultor_i(c, t, 290, 1640, 1.5, poses=((0, "think"),), exprs=((0, "think"),), look=0.4)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
