"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/decimo-terceiro-tres-portas/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "SEU 13º", 540, 380, 130, MARKER, INK)
    c.save(); c.translate(540, 530); hl(c, "ANTES DO DIA 30", 0, 0, 84, LYELLOW); c.restore()
    for i, col in enumerate((RED, BLUE, GREEN)):
        c.save(); c.translate(220 + i * 320, 920); c.scale(0.95, 0.95); door(c, i + 1, col, 0.0); c.restore()
    c.save(); c.translate(540, 1210); hl(c, "QUAL PORTA É A SUA?", 0, 0, 66, LGREEN, GREEN); c.restore()
    hero(c, 10, 540, 1640, 0.62, [(0, "think")], [(0, "think")], look=0.4)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
