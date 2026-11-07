"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/pov-role-barato/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, INK); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "POV: o rolê", 540, 360, 96, MARKER, INK)
    c.save(); c.translate(540, 480); hl(c, "\"barato\" de sábado", 0, 0, 70, LYELLOW); c.restore()
    # plano x realidade
    text(c, "plano", 280, 610, 48, HAND, DGRAY)
    text(c, "R$ 50", 280, 700, 110, MARKER, GREEN)
    line(c, 170, 712, 390, 688, 8, RED)
    c.save(); c.translate(505, 690); arrow(c, -45, 0, 45, 0, INK, 10); c.restore()
    text(c, "às 3h", 800, 610, 48, HAND, DGRAY)
    text(c, "R$ 430", 805, 700, 104, MARKER, RED)
    c.save(); c.translate(300, 1000); c.scale(1.2, 1.2); beer_mug(c); c.restore()
    figure(c, 10, 720, 1300, 1.15, poses=[(0, "head")], exprs=[(0, "shocked")], look=-0.4, shirt=ORANGE,
           hair="spiky", fid=2)
    line(c, 120, 1306, 960, 1306, 5, LGRAY)
    text(c, "e era \"só uma\"", 540, 1450, 70, HAND, INK)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
