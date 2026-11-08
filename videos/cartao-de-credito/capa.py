"""Capa do ep. 5 (cartão de crédito). O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1080))
    numero_i(c, "O QUE NINGUÉM", 540, 330, 96, CREME)
    numero_i(c, "TE CONTA DO", 540, 450, 96, CREME)
    numero_i(c, "CARTÃO", 540, 610, 190, GOLD)
    numero_i(c, "451% AO ANO", 540, 790, 110, CREME)
    consultor_i(c, t, 540, 1640, 1.55, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 760, 1290, 260, 70, 16); rgb(c, NAVY); c.fill()
    numero_i(c, "EP. 5", 890, 1325, 52, GOLD)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
