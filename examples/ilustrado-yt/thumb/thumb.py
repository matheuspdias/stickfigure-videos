"""Modelo de thumbnail do Faz a Conta (estilo ilustrado). Rodar da raiz: python examples/ilustrado-yt/thumb/thumb.py
Fórmula: fundo escuro de contraste (some menos na página branca do YouTube), O Consultor em close com emoção forte,
2 a 4 palavras enormes, 1 objeto que conta a história (celular com o resultado, fatura, etiqueta) e no máximo 1 selo."""
import sys, os
sys.path.insert(0, os.getcwd())
from engine import *
from ilustrado import *

OUT = os.path.dirname(os.path.abspath(__file__))


def a(c, t):  # resultado positivo: celular com o milhão
    fundo_marca(c, t, "navy")
    rglow(c, 1420, 520, 760, GOLD, 0.35)
    celular_app(c, t, 1440, 600, 1.35, "Saldo investido", "R$ 1 MILHÃO", sub="em 35 anos")
    thumb_close(c, t, 400, 1560, 2.4, "shocked", "point_r", 0.8)
    thumb_texto(c, ["COM", "R$ 10/DIA?"], 760, 40, 160, cores=[CREME, GOLD])


def b(c, t):  # alerta: fatura vermelha
    fundo_marca(c, t, "vermelho")
    fatura(c, t, 1400, 560, 1.25, minimo="R$ 357")
    thumb_close(c, t, 400, 1560, 2.4, "desperate", "head", 0.8)
    thumb_texto(c, ["NUNCA PAGUE", "O MÍNIMO"], 900, 30, 150, cores=[CREME, GOLD])


def cc(c, t):  # dilema "X ou Y?": tela dividida, rótulo enorme em cada lado, O Consultor no meio
    thumb_versus(c, t, "ALUGAR", "COMPRAR",
                 fn_esq=lambda c: numero_i(c, "R$ 1.500", -40, 0, 140, GOLD),
                 fn_dir=lambda c: numero_i(c, "R$ 2.950", 40, 0, 140, GOLD))
    thumb_close(c, t, 960, 1820, 2.3, "shocked", "think", 0.0)


for nome, fn in (("thumb_A", a), ("thumb_B", b), ("thumb_C", cc)):
    print(salvar_thumb(lambda c, t, fn=fn: fn(c, t), f"{OUT}/{nome}.png"))
