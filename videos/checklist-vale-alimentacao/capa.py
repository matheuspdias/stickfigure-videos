"""Capa do TikTok checklist-vale-alimentacao, estilo caderno (modelo videos/checklist-sair-do-rotativo/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "VALE-ALIMENTAÇÃO", 540, 380, 80, MARKER, NAVY)
    c.save(); c.translate(540, 505); hl(c, "3 PASSOS", 0, 0, 80, (1, 0.8, 0.76), RED); c.restore()
    for i, s in enumerate(("compra só o básico", "separa o carrinho", "divide por semana")):
        y = 650 + i * 100
        circle(c, 130, y - 16, 32, WHITE, 5)
        text(c, str(i + 1), 130, y - 2, 40, MARKER, NAVY)
        text(c, s, 190, y, 60, MARKER, INK, align="l")
    text(c, "VA de R$ 600", 330, 1060, 52, HAND, DGRAY)
    text(c, "R$ 87", 330, 1190, 110, MARKER, GOLD)
    text(c, "por semana", 330, 1280, 56, MARKER, NAVY)
    hero(c, 10, 830, 1380, 0.85, [(0, "finger_up")], [(0, "confident")], look=-0.4)
    c.save(); c.translate(540, 1530); hl(c, "SALVA PRO DIA QUE O VALE CAIR", 0, 0, 54, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
