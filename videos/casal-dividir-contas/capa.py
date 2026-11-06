"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/casal-dividir-contas/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True
HIM, HER = BLUE, ORANGE


def tagc(c, s, x, y, col, size=64):
    w = text_w(c, s, size) + 44
    rrect(c, x - w / 2, y - size * 0.7, w, size * 1.4, 14); fs(c, col, 5)
    text(c, s, x, y + 3, size, MARKER, WHITE)


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "CONTAS DO CASAL", 540, 370, 92, MARKER, INK)
    c.save(); c.translate(540, 530); hl(c, "50/50", 0, 0, 170, NAVY, WHITE); c.restore()
    text(c, "ou", 540, 690, 80, HAND, INK)
    c.save(); c.translate(540, 820); hl(c, "PROPORCIONAL?", 0, 0, 104, LYELLOW); c.restore()
    figure(c, 10, 250, 1560, 0.85, [(0, "think")], [(0, "think")], shirt=HIM, hair="spiky", fid=2, look=0.6)
    figure(c, 10, 830, 1560, 0.85, [(0, "think_l")], [(0, "think")], shirt=HER, hair="long", fid=3, look=-0.6)
    tagc(c, "R$ 5 mil", 250, 1110, HIM)
    tagc(c, "R$ 2 mil", 830, 1110, HER)
    text(c, "?", 540, 1300, 260, MARKER, GOLD, outline=INK, ow=12)
    line(c, 60, 1566, 1020, 1566, 5, LGRAY)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
