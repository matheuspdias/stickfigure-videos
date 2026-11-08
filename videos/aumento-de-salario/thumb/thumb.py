"""Thumbnails do vídeo "Ganhei R$ 1.000 de aumento e só vieram R$ 475". Rodar da raiz:
python videos/aumento-de-salario/thumb/thumb.py"""
import sys, os
sys.path.insert(0, os.getcwd())
from engine import *
from ilustrado import *

OUT = os.path.dirname(os.path.abspath(__file__))


def a(c, t):  # contracheque: +1.000 virou +475
    fundo_marca(c, t, "vermelho")
    rglow(c, 1400, 600, 700, GOLD, 0.25)
    contracheque(c, 1420, 640, 1.25, "R$ 6.000", (("INSS", "- R$ 641"), ("IR", "- R$ 385")), "R$ 4.973")
    thumb_close(c, t, 400, 1560, 2.4, "shocked", "point_r", 0.8)
    thumb_texto(c, ["+ R$ 1.000?", "VIERAM R$ 475"], 960, 40, 140, cores=[CREME, GOLD])


def b(c, t):  # etiqueta: aumento riscado
    fundo_marca(c, t, "navy")
    rglow(c, 1380, 620, 760, GOLD, 0.35)
    c.save(); c.translate(1000, 640); c.scale(2.5, 2.5); etiqueta_preco(c, "R$ 475    ", VERDE, 60, riscado="R$ 1.000"); c.restore()
    thumb_close(c, t, 400, 1560, 2.4, "desperate", "head", 0.8)
    thumb_texto(c, ["CADÊ MEU", "AUMENTO?"], 980, 30, 160, cores=[CREME, GOLD])


for nome, fn in (("aumento_thumb_A", a), ("aumento_thumb_B", b)):
    print(salvar_thumb(lambda c, t, fn=fn: fn(c, t), f"{OUT}/{nome}.png"))
