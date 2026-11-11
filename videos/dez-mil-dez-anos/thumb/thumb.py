"""Thumbnails do vídeo "Poupança, CDB ou Bolsa? R$ 10 mil em 2016". Rodar da raiz:
python videos/dez-mil-dez-anos/thumb/thumb.py"""
import sys, os
sys.path.insert(0, os.getcwd())
from engine import *
from ilustrado import *

OUT = os.path.dirname(os.path.abspath(__file__))


def a(c, t):  # dilema: poupança x bolsa, o resultado de cada lado
    thumb_versus(c, t, "POUPANÇA", "BOLSA",
                 fn_esq=lambda c: numero_i(c, "R$ 18 MIL", -70, -20, 128, GOLD),
                 fn_dir=lambda c: numero_i(c, "R$ 25 MIL", 70, -20, 128, GOLD),
                 y_rot=270, y_meio=H * 0.45)
    thumb_close(c, t, 960, 1830, 2.3, "shocked", "think", 0.0)


def b(c, t):  # resultado: os R$ 10 mil de 2016 viraram R$ 25 mil
    fundo_marca(c, t, "verde")
    rglow(c, 1300, 560, 760, GOLD, 0.30)
    c.save(); c.translate(700, 640); c.scale(2.2, 2.2); etiqueta_preco(c, "R$ 25 MIL", GOLD, 64, riscado="R$ 10 MIL"); c.restore()
    thumb_close(c, t, 380, 1560, 2.4, "shocked", "point_r", 0.8)
    thumb_texto(c, ["10 ANOS", "DEPOIS"], 1220, 20, 150, cores=[CREME, GOLD])


def cc(c, t):  # pergunta: quem ganhou? pódio com 1-2-3
    fundo_marca(c, t, "navy")
    rglow(c, 1250, 650, 700, GOLD, 0.35)
    for x, h, lab, col in ((880, 260, "2", (0.75, 0.77, 0.82)), (1180, 380, "1", GOLD), (1480, 180, "3", (0.80, 0.52, 0.26))):
        rr(c, x - 140 + 10, 1000 - h + 12, 280, h, 18); rgb(c, (0, 0, 0), 0.35); c.fill()
        rr(c, x - 140, 1000 - h, 280, h, 18); rgb(c, col); c.fill()
        numero_i(c, lab, x, 1000 - h + 90, 130, CREME)
    numero_i(c, "?", 1180, 1000 - 380 - 110, 200, GOLD)
    thumb_close(c, t, 380, 1560, 2.4, "think", "think", 0.8)
    thumb_texto(c, ["R$ 10 MIL:", "QUEM GANHOU?"], 1180, 20, 140, cores=[CREME, GOLD])


for nome, fn in (("dez_mil_thumb_A", a), ("dez_mil_thumb_B", b), ("dez_mil_thumb_C", cc)):
    print(salvar_thumb(lambda c, t, fn=fn: fn(c, t), f"{OUT}/{nome}.png"))
