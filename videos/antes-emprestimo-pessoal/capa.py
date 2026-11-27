"""Capa do TikTok antes-emprestimo-pessoal (série ep. 7), estilo caderno (modelo videos/salario-minimo-2027-o-que-muda/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "O QUE NINGUÉM TE CONTA", 540, 360, 60, MARKER, DGRAY)
    text(c, "EMPRÉSTIMO PESSOAL", 540, 470, 76, MARKER, NAVY)
    text(c, "pegou R$ 5.000", 540, 620, 62, HAND, DGRAY)
    text(c, "devolve R$ 7.354", 540, 760, 100, MARKER, RED)
    c.save(); c.translate(540, 900); hl(c, "110% AO ANO", 0, 0, 80, (1, 0.8, 0.76), RED); c.restore()
    for i, s in enumerate(("olha o CET", "seguro é opcional", "simula em 3 lugares")):
        y = 1060 + i * 90
        c.save(); c.translate(120, y - 18); check_icon(c, 28); c.restore()
        text(c, s, 170, y, 52, MARKER, INK, align="l")
    hero(c, 10, 870, 1500, 0.8, [(0, "head")], [(0, "shocked")], look=-0.4)
    c.save(); c.translate(420, 1560); hl(c, "EP. 7", 0, 0, 64, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
