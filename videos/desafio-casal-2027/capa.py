"""Capa do TikTok: Desafio do casal 2027 (R$ 10 mil em 12 meses)."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "DESAFIO DO", 540, 330, 100, CREME)
    numero_i(c, "CASAL 2027", 540, 460, 125, GOLD)
    numero_i(c, "R$ 10 MIL", 540, 620, 150, VERDE)
    for i, s in enumerate(("JAN-ABR  R$ 600", "MAI-AGO  R$ 800", "SET-DEZ  R$ 1.100")):
        rr(c, 150, 700 + i * 108, 780, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 540, 764 + i * 108, 52, MARKER, TINTA)
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "arms_up"),), exprs=((0, "grin"),), look=0.0)
    rr(c, 240, 1560, 600, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "MANDA PRO SEU AMOR", 540, 1632, 50, MARKER, CREME)


SCENES = [(0, 999, capa)]
