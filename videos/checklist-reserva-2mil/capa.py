"""Capa do TikTok checklist-reserva-2mil, estilo caderno (modelo videos/checklist-sair-do-rotativo/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "RESERVA COM R$ 2 MIL", 540, 380, 74, MARKER, NAVY)
    c.save(); c.translate(540, 505); hl(c, "3 PASSOS", 0, 0, 80, LGREEN, GREEN); c.restore()
    for i, s in enumerate(("descobre o seu número", "paga você primeiro", "define a emergência")):
        y = 650 + i * 100
        circle(c, 130, y - 16, 32, WHITE, 5)
        text(c, str(i + 1), 130, y - 2, 40, MARKER, NAVY)
        text(c, s, 190, y, 56, MARKER, INK, align="l")
    text(c, "R$ 100 por mês", 360, 1070, 52, HAND, DGRAY)
    text(c, "R$ 1.500", 360, 1190, 100, MARKER, GOLD)
    text(c, "em 10 meses", 360, 1270, 52, HAND, DGRAY)
    hero(c, 10, 830, 1380, 0.85, [(0, "thumb")], [(0, "happy")], look=-0.4)
    c.save(); c.translate(540, 1530); hl(c, "SALVA PRO DIA DO SALÁRIO", 0, 0, 60, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
