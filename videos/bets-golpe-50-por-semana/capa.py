"""Capa do TikTok bets-golpe-50-por-semana, estilo caderno (modelo videos/salario-minimo-2027-o-que-muda/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "BETS PROIBIDAS", 540, 390, 86, MARKER, NAVY)
    c.save(); c.translate(540, 520); hl(c, "MAS O GOLPE NÃO", 0, 0, 74, (1, 0.8, 0.76), RED); c.restore()
    text(c, "60 mil+", 540, 700, 130, MARKER, RED)
    text(c, "sites suspeitos", 540, 790, 60, HAND, DGRAY)
    text(c, "R$ 50 por semana", 330, 960, 60, MARKER, INK)
    text(c, "= R$ 2 .600", 330, 1080, 96, MARKER, RED)
    text(c, "por ano", 330, 1170, 58, MARKER, NAVY)
    hero(c, 10, 830, 1400, 0.85, [(0, "head")], [(0, "shocked")], look=-0.4)
    c.save(); c.translate(540, 1540); hl(c, "FAZ A CONTA ANTES", 0, 0, 64, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
