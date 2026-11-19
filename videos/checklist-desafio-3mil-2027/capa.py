"""Capa do TikTok: Checklist do Consultor · Desafio R$ 3 mil em 2027 pra quem ganha pouco."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "R$ 3 MIL EM 2027", 540, 340, 96, GOLD)
    numero_i(c, "GANHANDO POUCO", 540, 470, 90, CREME)
    for i, s in enumerate(("1. R$ 8 POR DIA", "2. FIXO, NÃO 52 SEMANAS", "3. PIX NO AUTOMÁTICO", "4. A REGRA DE MARÇO")):
        rr(c, 110, 560 + i * 108, 860, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, 624 + i * 108, 48, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 250, 1560, 580, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA PRA JANEIRO", 540, 1632, 54, MARKER, CREME)


SCENES = [(0, 999, capa)]
