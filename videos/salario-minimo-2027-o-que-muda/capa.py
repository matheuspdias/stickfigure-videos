"""Capa do TikTok salario-minimo-2027-o-que-muda, estilo caderno (modelo videos/ferias-mes-seguinte/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "SALÁRIO MÍNIMO 2027", 540, 390, 72, MARKER, NAVY)
    text(c, "R$ 1.621", 300, 560, 80, MARKER, GRAY)
    line(c, 160, 545, 440, 525, 10, RED)
    text(c, "R$ 1.741", 720, 560, 90, MARKER, GREEN)
    c.save(); c.translate(540, 700); hl(c, "+R$ 120", 0, 0, 90, LGREEN, GREEN); c.restore()
    text(c, "não é só o seu salário", 540, 860, 60, HAND, DGRAY)
    for i, s in enumerate(("MEI: DAS sobe", "aposentado, BPC, PIS", "INSS do mínimo")):
        y = 980 + i * 90
        c.save(); c.translate(120, y - 18); check_icon(c, 28); c.restore()
        text(c, s, 170, y, 54, MARKER, INK, align="l")
    hero(c, 10, 860, 1460, 0.8, [(0, "point_l")], [(0, "confident")], look=-0.4)
    c.save(); c.translate(420, 1560); hl(c, "O QUE MUDA PRA VOCÊ", 0, 0, 58, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
