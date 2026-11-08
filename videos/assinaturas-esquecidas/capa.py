"""Capa do TikTok assinaturas-esquecidas. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1080))
    numero_i(c, "R$ 1.560", 540, 400, 190, GOLD)
    numero_i(c, "POR ANO EM", 540, 570, 100, CREME)
    numero_i(c, "ASSINATURAS", 540, 690, 110, CREME)
    numero_i(c, "ESQUECIDAS", 540, 810, 110, GOLD)
    consultor_i(c, t, 540, 1640, 1.6, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.0)
    for x, n in ((170, 9), (910, 13)):
        c.save(); c.translate(x, 1600); pilha_moedas(c, n, 60); c.restore()
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
