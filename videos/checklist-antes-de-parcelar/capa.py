"""Capa do TikTok: Checklist do Consultor · 3 passos antes de parcelar qualquer coisa."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "ANTES DE", 540, 300, 110, CREME)
    numero_i(c, "PARCELAR", 540, 440, 120, GOLD)
    for i, s in enumerate(("1. SOMA O QUE JÁ PARCELA", "2. COMPARA COM O SALÁRIO", "3. E SE A RENDA PARAR?")):
        rr(c, 90, 520 + i * 108, 900, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 130, 584 + i * 108, 48, MARKER, TINTA, align="l")
    rr(c, 150, 860, 780, 100, 26); rgb(c, VERDE); c.fill()
    text(c, "TETO: 1/5 DO SALÁRIO", 540, 928, 52, MARKER, CREME)
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 100, 1560, 880, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA ANTES DA BLACK FRIDAY", 540, 1632, 46, MARKER, CREME)


SCENES = [(0, 999, capa)]
