"""Capa do TikTok carro-novo-usado-mesmo-salario, estilo caderno (modelo videos/ferias-mes-seguinte/capa.py).
    python render.py stills videos/carro-novo-usado-mesmo-salario/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "MESMO SALÁRIO", 540, 360, 104, MARKER, NAVY)
    c.save(); c.translate(540, 500); hl(c, "5 ANOS DEPOIS", 0, 0, 66, LYELLOW); c.restore()
    line(c, 540, 600, 540, 1330, 4, LGRAY)
    c.save(); c.translate(290, 700); c.scale(0.7, 0.7); car(c, RED); c.restore()
    text(c, "R$ 55 mil", 290, 850, 76, MARKER, RED)
    text(c, "o carro vale", 290, 925, 42, HAND, DGRAY)
    c.save(); c.translate(790, 700); bills(c, 3); c.restore()
    text(c, "R$ 172 mil", 790, 850, 76, MARKER, GREEN)
    text(c, "investidos", 790, 925, 42, HAND, DGRAY)
    other(c, 10, 290, 1320, 0.65, [(0, "head")], [(0, "desperate")], shirt=ORANGE, fid=2, look=0.3)
    other(c, 10, 790, 1320, 0.65, [(0, "arms_up")], [(0, "grin")], shirt=GREEN, fid=3, hair="tuft", look=-0.3)
    c.save(); c.translate(540, 1480); hl(c, "UMA DECISÃO SÓ", 0, 0, 70, (1, 0.8, 0.76), RED); c.restore()


SCENES = [(0, 999, capa)]
