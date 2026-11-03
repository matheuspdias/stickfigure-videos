"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/decimo-terceiro-quanto-cai/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def env(c, n, col, s):
    c.save(); c.scale(s, s); envelope(c); circle(c, 0, 18, 34, col, 5); text(c, n, 0, 22, 40, MARKER, WHITE); c.restore()


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "QUANTO CAI", 540, 390, 120, MARKER, INK)
    text(c, "DE VERDADE", 540, 530, 120, MARKER, RED)
    c.save(); c.translate(540, 680); hl(c, "no seu 13º", 0, 0, 80, LYELLOW); c.restore()
    c.save(); c.translate(300, 960); env(c, "1ª", GOLD, 1.3); c.restore()
    c.save(); c.translate(300, 1090); text(c, "R$ ?", 0, 0, 64, MARKER, INK); c.restore()
    c.save(); c.translate(720, 930); env(c, "2ª", GREEN, 2.0); c.restore()
    c.save(); c.translate(720, 1120); hl(c, "MAIOR?", 0, 0, 72, LGREEN); c.restore()
    hero(c, 10, 540, 1640, 0.75, [(0, "point_ru")], [(0, "shocked")], look=0.4)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
