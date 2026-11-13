"""Capa do TikTok segunda-parcela-13-menor. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1100))
    numero_i(c, "2ª PARCELA", 540, 380, 150, GOLD)
    numero_i(c, "DO 13º", 540, 530, 120, CREME)
    numero_i(c, "POR QUE VEM MENOR?", 540, 680, 74, CREME, contorno=NAVY)
    for x, h, cor, v in ((210, 420, VERDE, "R$ 1.500"), (870, 340, NAVY, "R$ 1.251")):
        rr(c, x - 95, 1400 - h, 190, h, 18); rgb(c, cor); c.fill()
        numero_i(c, v, x, 1400 - h - 45, 54, CREME)
    consultor_i(c, t, 540, 1640, 1.3, poses=((0, "shrug"),), exprs=((0, "shocked"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
