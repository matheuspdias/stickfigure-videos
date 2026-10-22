"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/clt-ou-pj/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def _tag(c, s, x, y, col, size):
    w = text_w(c, s, size) + 50
    rrect(c, x - w / 2, y - size * 0.7, w, size * 1.4, 18); fs(c, col, 7)
    text(c, s, x, y + 4, size, MARKER, WHITE)


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "R$ 5 MIL", 285, 400, 80, MARKER, BLUE)
    _tag(c, "CLT", 290, 520, BLUE, 70)
    text(c, "x", 540, 410, 70, MARKER, INK)
    text(c, "R$ 7 MIL", 795, 400, 80, MARKER, ORANGE)
    _tag(c, "PJ", 790, 520, ORANGE, 70)
    c.save(); c.translate(540, 720); hl(c, "QUASE IGUAL?", 0, 0, 110, LYELLOW); c.restore()
    other(c, 10, 250, 1520, 1.15, [(0, "hips")], [(0, "confident")], shirt=BLUE, fid=2, look=0.5)
    figure(c, 10, 830, 1520, 1.15, poses=[(0, "shrug")], exprs=[(0, "think")], shirt=ORANGE, hair="tuft", fid=3, look=-0.5)
    hero(c, 10, 540, 1520, 0.95, [(0, "head")], [(0, "shocked")], look=0)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
