"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/dez-mil-cinco-anos/capa.py out/capas 10"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *  # noqa
from scenes import ICONS, ORDER, trophy  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "R$ 10 MIL", 540, 390, 150, MARKER, GREEN)
    text(c, "HÁ 5 ANOS", 540, 540, 120, MARKER, INK)
    c.save(); c.translate(540, 700); hl(c, "6 lugares: quem ganhou?", 0, 0, 62, LYELLOW); c.restore()
    for i, k in enumerate(ORDER):
        c.save(); c.translate(160 + (i % 3) * 170 - (0 if i < 3 else 0), 900 + (i // 3) * 210); c.scale(0.6, 0.6); ICONS[k](c); c.restore()
    c.save(); c.translate(840, 990); c.scale(1.1, 1.1); trophy(c, GOLD, "?"); c.restore()
    hero(c, 10, 800, 1600, 0.8, [(0, "think")], [(0, "think")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
