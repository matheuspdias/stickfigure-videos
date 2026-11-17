"""Capa do TikTok comprar-ou-alugar-2026-parte-2. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    numero_i(c, "COMPRAR OU", 540, 360, 110, CREME)
    numero_i(c, "ALUGAR?", 540, 500, 150, GOLD)
    numero_i(c, "A CONTA DE 10 ANOS", 540, 640, 74, CREME)
    # parcela x aluguel
    rr(c, 90, 720, 900, 230, 28); rgb(c, CREME); c.fill()
    text(c, "COMPROU", 310, 790, 40, MARKER, NAVY)
    numero_i(c, "R$ 329 MIL", 310, 880, 62, VERMELHO)
    text(c, "ALUGOU + INVESTIU", 770, 790, 36, MARKER, NAVY)
    numero_i(c, "R$ 404 MIL", 770, 880, 62, VERDE)
    consultor_i(c, t, 540, 1620, 1.45, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 680, 1180, 300, 100, 20); rgb(c, VERMELHO); c.fill()
    numero_i(c, "PARTE 2", 830, 1230, 56, CREME)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
