"""Capa do TikTok checklist-sair-do-rotativo, estilo caderno (modelo videos/dolar-6-reais-no-bolso/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "SAIR DO ROTATIVO", 540, 380, 84, MARKER, NAVY)
    c.save(); c.translate(540, 505); hl(c, "5 PASSOS", 0, 0, 80, (1, 0.8, 0.76), RED); c.restore()
    for i, s in enumerate(("guarda o cartão", "olha o tamanho", "não paga só o mínimo", "troca a dívida", "conhece o teto")):
        y = 640 + i * 92
        circle(c, 130, y - 16, 32, WHITE, 5)
        text(c, str(i + 1), 130, y - 2, 40, MARKER, NAVY)
        text(c, s, 190, y, 56, MARKER, INK, align="l")
    text(c, "fatura de R$ 1.000", 360, 1160, 48, HAND, DGRAY)
    text(c, "+R$ 150/mês", 370, 1270, 78, MARKER, RED)
    hero(c, 10, 830, 1380, 0.85, [(0, "head")], [(0, "shocked")], look=-0.4)
    c.save(); c.translate(540, 1530); hl(c, "SALVA PRO DIA DA FATURA", 0, 0, 62, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
