"""Capa do TikTok: Checklist do Consultor · 4 passos pra juntar os primeiros R$ 10 mil."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "OS PRIMEIROS", 540, 330, 96, CREME)
    numero_i(c, "R$ 10 MIL", 540, 470, 130, GOLD)
    for i, s in enumerate(("1. O VALOR QUE CABE", "2. ONDE DEIXAR", "3. ACELERA COM O 13º", "4. COMEMORA AS METAS")):
        rr(c, 110, 560 + i * 108, 860, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, 624 + i * 108, 48, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 100, 1560, 880, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA PRO DIA DO SALÁRIO", 540, 1632, 48, MARKER, CREME)


SCENES = [(0, 999, capa)]
