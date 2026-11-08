"""Demo vertical (TikTok) do estilo ILUSTRADO do Faz a Conta (~24 s, sem narração).
Layout: título ~y 250, palco 360-1290 (pés ~1290), legendas ~1400-1460, nada abaixo de 1500 nem à direita de 930."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"
SFX_OFF = True


def v01(c, t):  # gancho: número enorme já no primeiro quadro
    cena_padaria(c, t, "dia")
    numero_i(c, "R$ 10", 500, 300, 230, GOLD)
    numero_i(c, "POR DIA VIRA...", 500, 450, 84, CREME)
    consultor_i(c, t, 330, 1300, 1.45, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.7)
    entra(c, t, 0.8, 720, 860, lambda c: etiqueta_preco(c, "R$ 10", GOLD, 70), anim="drop")


def v02(c, t):  # contador gigante
    t0 = 4
    fundo_marca(c, t, "verde", holofote=(300, 900))
    contador(c, t, t0 + 0.2, 0, 1000000, 500, 330, 130, d=2.2, col=GOLD)
    numero_i(c, "EM 35 ANOS", 500, 470, 80, CREME)
    consultor_i(c, t, 300, 1300, 1.45, poses=((0, "stand"), (t0 + 2.4, "arms_up")), exprs=((0, "neutral"), (t0 + 2.4, "grin")), look=0.6)
    for i, n in enumerate((8, 14)):
        c.save(); c.translate(680 + i * 170, 1270); pilha_moedas(c, n, 62, t, t0 + 0.4 + i * 0.5, 0.08); c.restore()
    chuva_dinheiro(c, t, t0 + 2.4, 10, area=(560, 1000), area_y=560)


def v03(c, t):  # app do banco
    t0 = 10
    fundo_marca(c, t, "navy", holofote=(270, 950))
    numero_i(c, "MAS TEM UM DETALHE", 500, 250, 76, GOLD)
    celular_app(c, t, 640, 830, 1.05, "Saldo investido", "R$ 1 MILHÃO", sub="em 35 anos", t0=t0 + 0.3)
    consultor_i(c, t, 250, 1300, 1.3, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.7)


def v04(c, t):  # mercado: inflação
    t0 = 16
    cena_mercado(c, t)
    numero_i(c, "A INFLAÇÃO", 500, 260, 120, VERMELHO)
    entra(c, t, t0 + 0.5, 600, 640, lambda c: etiqueta_preco(c, "R$ 16", VERMELHO, 80, riscado="R$ 10"), anim="drop")
    consultor_i(c, t, 300, 1300, 1.45, poses=((0, "head"),), exprs=((0, "desperate"),), look=0.6)


def v05(c, t):  # fechamento com pergunta
    t0 = 20
    cena_sala(c, t, "tarde")
    numero_i(c, "QUANTO VOCÊ", 500, 250, 96, CREME)
    numero_i(c, "GUARDA POR DIA?", 500, 370, 96, GOLD)
    consultor_i(c, t, 330, 1300, 1.45, poses=((0, "present"),), exprs=((0, "happy"),), look=0.6)
    pessoa(c, t, 760, 1300, 1.3, "ana", poses=((0, "think_l"),), exprs=((0, "think"),), look=-0.5)


SCENES = [(0, 4, v01), (4, 10, v02), (10, 16, v03), (16, 20, v04), (20, 999.0, v05)]
