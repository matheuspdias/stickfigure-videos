"""Capa do TikTok imovel-2027-o-que-muda. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1150))
    numero_i(c, "COMPRAR IMÓVEL", 540, 350, 100, CREME)
    numero_i(c, "EM 2027", 540, 490, 150, GOLD)
    numero_i(c, "JUROS ATÉ", 540, 650, 80, CREME, contorno=NAVY)
    numero_i(c, "15% AO ANO", 540, 790, 130, GOLD)
    consultor_i(c, t, 380, 1620, 1.4, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.3)
    c.save(); c.translate(760, 1250); c.rotate(0.05)
    rr(c, -210, -60, 420, 120, 20); rgb(c, NAVY); c.fill()
    numero_i(c, "O QUE MUDA", 0, 0, 52, GOLD); c.restore()
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
