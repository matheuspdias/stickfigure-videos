"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/ferias-mes-seguinte/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "FÉRIAS?", 540, 390, 140, MARKER, NAVY)
    c.save(); c.translate(540, 560); hl(c, "CUIDADO COM", 0, 0, 78, (1, 0.8, 0.76), RED); c.restore()
    text(c, "O MÊS SEGUINTE", 540, 690, 92, MARKER, RED)
    c.save(); c.translate(280, 960); c.scale(1.2, 1.2); suitcase(c, ORANGE); c.restore()
    text(c, "férias", 280, 1120, 52, HAND, DGRAY)
    text(c, "R$ 3.631", 280, 1190, 64, MARKER, GREEN)
    text(c, "mês seguinte", 760, 1120, 52, HAND, DGRAY)
    text(c, "R$ 1.376", 760, 1190, 72, MARKER, RED)
    hero(c, 10, 760, 1060, 0.55, [(0, "head")], [(0, "shocked")], look=-0.4)
    c.save(); c.translate(540, 1370); hl(c, "salário de R$ 3 mil", 0, 0, 70, LYELLOW); c.restore()
    text(c, "por que vem tão pouco?", 540, 1510, 60, HAND, NAVY)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
