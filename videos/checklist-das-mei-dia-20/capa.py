"""Capa do TikTok checklist-das-mei-dia-20, estilo caderno (modelo videos/checklist-vale-alimentacao/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "MEI: ANTES DO DIA 20", 540, 380, 78, MARKER, NAVY)
    c.save(); c.translate(540, 505); hl(c, "3 PASSOS", 0, 0, 80, (1, 0.8, 0.76), RED); c.restore()
    for i, s in enumerate(("paga o DAS até o 20", "procura mês atrasado", "separa no dia que entra")):
        y = 650 + i * 100
        circle(c, 110, y - 16, 32, WHITE, 5)
        text(c, str(i + 1), 110, y - 2, 40, MARKER, NAVY)
        text(c, s, 165, y, 56, MARKER, INK, align="l")
    text(c, "1 ano esquecido", 330, 1060, 52, HAND, DGRAY)
    text(c, "+R$ 1.200", 330, 1190, 110, MARKER, RED)
    text(c, "e pode perder o INSS", 330, 1280, 48, MARKER, NAVY)
    hero(c, 10, 830, 1380, 0.85, [(0, "head")], [(0, "shocked")], look=-0.4)
    c.save(); c.translate(540, 1530); hl(c, "SALVA PRO DIA 20", 0, 0, 60, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
