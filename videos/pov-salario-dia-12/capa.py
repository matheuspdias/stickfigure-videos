"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/pov-salario-dia-12/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, INK); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "POV: caiu dia 5", 540, 360, 90, MARKER, INK)
    c.save(); c.translate(540, 480); hl(c, "acabou dia 12", 0, 0, 72, LYELLOW); c.restore()
    for x, d, col in ((300, "5", GREEN), (780, "12", RED)):
        c.save(); c.translate(x, 680); c.scale(1.3, 1.3); calendar(c, d, col, 78); c.restore()
    c.save(); c.translate(540, 690); arrow(c, -120, 0, 120, 0, INK, 10); c.restore()
    text(c, "-R$ 50", 540, 940, 190, MARKER, RED, outline=WHITE, ow=16)
    c.save(); c.translate(800, 1440); c.rotate(-1.52)
    figure(c, 10, 0, 0, 1.2, poses=[(0, "arms_up")], exprs=[(0, "shocked")], look=0, shirt=ORANGE,
           hair="spiky", fid=2)
    c.restore()
    line(c, 120, 1530, 960, 1530, 5, LGRAY)
    text(c, "e o mês nem chegou na metade", 540, 1120, 64, HAND, INK)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
