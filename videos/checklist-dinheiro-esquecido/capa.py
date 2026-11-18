"""Capa do TikTok: Checklist do Consultor · 3 lugares onde pode ter dinheiro seu esquecido."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "DINHEIRO SEU", 540, 340, 110, CREME)
    numero_i(c, "ESQUECIDO", 540, 480, 140, GOLD)
    for i, s in enumerate(("1. VALORES A RECEBER (BC)", "2. ABONO DO PIS", "3. FGTS DE EMPREGO ANTIGO")):
        rr(c, 110, 580 + i * 105, 860, 88, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, 642 + i * 105, 46, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 120, 1570, 840, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA PRA CONFERIR HOJE", 540, 1642, 48, MARKER, CREME)


SCENES = [(0, 999, capa)]
