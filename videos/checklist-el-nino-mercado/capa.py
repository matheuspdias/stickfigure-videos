"""Capa do TikTok: Checklist do Consultor · El Niño vai encarecer o mercado: 3 passos."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "EL NIÑO NO", 540, 300, 110, CREME)
    numero_i(c, "MERCADO", 540, 440, 130, GOLD)
    for i, s in enumerate(("1. DESCOBRE QUANTO SOBE", "2. ADIANTA OS BÁSICOS", "3. MEXE NA CARNE")):
        rr(c, 90, 545 + i * 105, 900, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 130, 609 + i * 105, 48, MARKER, TINTA, align="l")
    rr(c, 150, 875, 780, 100, 26); rgb(c, VERDE); c.fill()
    text(c, "SOBRAM R$ 44 POR MÊS", 540, 943, 52, MARKER, CREME)
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 100, 1560, 880, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA PRO DIA DO MERCADO", 540, 1632, 46, MARKER, CREME)


SCENES = [(0, 999, capa)]
