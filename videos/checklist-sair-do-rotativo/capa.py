"""Capa do TikTok: Checklist do Consultor · 5 passos pra sair do rotativo do cartão."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1350))
    numero_i(c, "SAIR DO", 540, 290, 110, CREME)
    numero_i(c, "ROTATIVO", 540, 430, 130, GOLD)
    for i, s in enumerate(("1. GUARDA O CARTÃO", "2. OLHA O TAMANHO", "3. NÃO PAGA SÓ O MÍNIMO", "4. TROCA POR UMA MAIS BARATA", "5. CONHECE O TETO")):
        rr(c, 90, 520 + i * 86, 900, 76, 20); rgb(c, CREME); c.fill()
        text(c, s, 125, 572 + i * 86, 40, MARKER, TINTA, align="l")
    rr(c, 150, 965, 780, 96, 26); rgb(c, VERMELHO); c.fill()
    text(c, "~15% DE JUROS POR MÊS", 540, 1030, 52, MARKER, CREME)
    consultor_i(c, t, 540, 2170, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 100, 1560, 880, 110, 26); rgb(c, GOLD); c.fill()
    text(c, "SALVA PRO DIA DA FATURA", 540, 1632, 46, MARKER, TINTA)


SCENES = [(0, 999, capa)]
