"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/pov-fatura-janeiro/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, INK); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "POV: 10 de janeiro", 540, 360, 84, MARKER, INK)
    c.save(); c.translate(540, 470); hl(c, "você abriu a fatura", 0, 0, 64, LYELLOW); c.restore()
    text(c, "R$ 4.400", 540, 680, 190, MARKER, RED, outline=WHITE, ow=16)
    text(c, "e o 13º já foi", 540, 830, 70, HAND, INK)
    c.save(); c.translate(560, 1500); c.scale(1.5, 1.5); sofa_back(c); c.restore()
    figure(c, 10, 560, 1500, 1.0, poses=[(0, "head")], exprs=[(0, "desperate")], look=0, shirt=ORANGE,
           hair="spiky", fid=2)
    c.save(); c.translate(560, 1500); c.scale(1.5, 1.5); sofa_front(c); c.restore()
    for x, y, r, ti, col in ((250, 1060, -0.3, "IPVA", RED), (850, 1080, 0.25, "IPTU", ORANGE)):
        c.save(); c.translate(x, y); c.rotate(r); c.scale(0.7, 0.7); boleto(c, ti, col); c.restore()
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
