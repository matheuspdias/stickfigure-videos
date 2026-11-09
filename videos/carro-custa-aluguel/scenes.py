"""Seu carro custa mais que um aluguel. Só TikTok: vertical nativo 1080x1920, 71,7 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: carro de R$ 60 mil = R$ 21 mil/ano = R$ 1.750/mês; + R$ 500/mês de rendimento perdido
= mais de R$ 2.200/mês; aplicativo (2 corridas por dia útil + 8 no fim de semana) ~ R$ 1.340/mês."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(31.9, "tum"), (42.5, "tum"), (55.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

VERM_CARRO = (0.86, 0.26, 0.22)


# ---------------------------------------------------------------- helpers
def selo(s, cor=VERMELHO, size=64, tcol=CREME):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(-0.06)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def custo(lab, val, cor, w=600):
    """cartão de custo: bolinha colorida, nome e valor por ano"""
    def f(c):
        h = 100
        rr(c, -w / 2 + 6, -h / 2 + 8, w, h, 22); rgb(c, (0, 0, 0), 0.20); c.fill()
        rr(c, -w / 2, -h / 2, w, h, 22); rgb(c, (0.99, 0.99, 0.98)); c.fill()
        c.new_sub_path(); c.arc(-w / 2 + 52, 0, 26, 0, 6.283); rgb(c, cor); c.fill()
        text(c, lab, -w / 2 + 96, 2, 44, HAND, (0.2, 0.2, 0.25), align="l")
        text(c, val, w / 2 - 24, 2, 48, MARKER, TINTA, align="r")
    return f


def carro(c, x, y, s=1.0, cor=VERM_CARRO, t=0):
    c.save(); c.translate(x, y); c.scale(s, s); carro_i(c, t, cor); c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 3.9  gancho: frase enorme já no 1º quadro
    cena_rua(c, t, "tarde", carros=False)
    numero_i(c, "SEU CARRO CUSTA", 520, 240, 88, CREME)
    numero_i(c, "MAIS QUE UM", 520, 350, 88, CREME)
    numero_i(c, "ALUGUEL", 520, 480, 130, GOLD)
    carro(c, 640, 1280, 1.25)
    entra(c, t, 0.6, 650, 900, lambda c: etiqueta_preco(c, "ALUGUEL?", VERMELHO, 56), anim="drop")
    consultor_i(c, t, 220, 1300, 1.35, poses=((0, "point_r"), (2.6, "head")), exprs=((0, "confident"), (2.6, "shocked")), look=0.7)


def s02(c, t):  # 3.9 - 7.0  um carro de R$ 60 mil
    fundo_marca(c, t, "navy", holofote=(560, 1100))
    numero_i(c, "VAMOS FAZER A CONTA", 520, 250, 72, GOLD)
    entra(c, t, 4.6, 600, 1180, lambda c: (c.scale(1.3, 1.3), carro_i(c, t, VERM_CARRO)), anim="left")
    contador(c, t, 5.4, 0, 60000, 560, 560, 150, d=1.0, col=GOLD)
    consultor_i(c, t, 200, 1300, 1.2, poses=((0, "present"),), exprs=((0, "neutral"),), look=0.8)


CUSTOS = [  # (rótulo, valor, cor, t)
    ("IPVA", "R$ 2.400", (0.30, 0.42, 0.80), 7.0),
    ("Seguro", "R$ 3.000", (0.20, 0.62, 0.40), 9.8),
    ("Gasolina", "R$ 6.700", (0.86, 0.56, 0.20), 11.7),
    ("Revisão e pneu", "R$ 1.800", (0.55, 0.40, 0.70), 16.5),
    ("Estacionamento", "R$ 1.200", (0.45, 0.66, 0.90), 20.5),
]


def s03(c, t):  # 7.0 - 23.0  os custos, um a um (somando)
    fundo_marca(c, t, "creme")
    numero_i(c, "POR ANO", 520, 240, 96, NAVY, contorno=CREME)
    soma = 0
    for i, (lab, val, cor, t0) in enumerate(CUSTOS):
        entra(c, t, t0, 610, 400 + i * 118, custo(lab, val, cor, 600), anim="right")
        if t > t0 + 1.2:
            soma += int(val.replace("R$ ", "").replace(".", ""))
    if t > 8.2:
        numero_i(c, "SOMA: " + brl(soma), 610, 1060, 84, VERMELHO, contorno=CREME)
    consultor_i(c, t, 190, 1300, 1.2, poses=((0, "point_r"), (11.7, "finger_up"), (16.5, "point_r"), (20.5, "shrug")),
                exprs=((0, "neutral"), (11.7, "worried"), (16.5, "neutral"), (20.5, "worried")), look=0.8)


def s04(c, t):  # 23.0 - 30.6  o custo que ninguém vê: perde 10% por ano
    fundo_marca(c, t, "vermelho", holofote=(560, 1100))
    numero_i(c, "O CUSTO QUE", 520, 240, 92, CREME)
    numero_i(c, "NINGUÉM VÊ", 520, 350, 104, GOLD)
    carro(c, 600, 1180, 1.2)
    if t < 27.7:
        contador(c, t, 24.4, 60000, 54000, 560, 560, 130, d=3.0, col=CREME)
    else:
        numero_i(c, brl(54000), 560, 560, 130, CREME)
    entra(c, t, 25.6, 600, 730, selo("- 10% POR ANO", NAVY, 58, GOLD), anim="stamp")
    entra(c, t, 27.7, 600, 900, selo("R$ 6 MIL SOMEM", CREME, 58, VERMELHO), anim="pop")
    consultor_i(c, t, 210, 1300, 1.25, poses=((0, "finger_up"), (27.7, "head")), exprs=((0, "think"), (27.7, "shocked")), look=0.7)


def s05(c, t):  # 30.6 - 35.8  total: R$ 21 mil por ano = R$ 1.750 por mês
    fundo_marca(c, t, "navy", holofote=(270, 1000))
    numero_i(c, "SOMANDO TUDO", 520, 240, 88, CREME)
    contador(c, t, 31.9, 0, 21000, 520, 420, 160, d=1.0, col=GOLD)
    numero_i(c, "POR ANO", 520, 540, 72, CREME) if t > 32.8 else None
    entra(c, t, 33.8, 620, 680, selo("R$ 1.750/MÊS", VERMELHO, 64, CREME), anim="stamp")
    if t > 34.2:
        c.save(); c.translate(820, 1260); pilha_moedas(c, 12, 50, t, 34.2, 0.05); c.restore()
    consultor_i(c, t, 220, 1300, 1.15, poses=((0, "present"), (33.8, "head")), exprs=((0, "worried"), (33.8, "shocked")), look=0.5)


def s06(c, t):  # 35.8 - 42.4  os R$ 60 mil parados, se rendessem
    cena_sala(c, t, "tarde")
    numero_i(c, "E TEM MAIS", 520, 240, 100, GOLD)
    entra(c, t, 37.0, 690, 760, lambda c: celular_app(c, t, 0, 0, 1.15, "Se estivesse rendendo", "R$ 60.000",
                                                     "por mês: + R$ 500", curva=lambda k: k ** 1.4, t0=37.4), anim="drop")
    entra(c, t, 40.0, 690, 1180, selo("+ R$ 500/MÊS", VERDE, 56, CREME), anim="stamp")
    consultor_i(c, t, 230, 1300, 1.35, poses=((0, "finger_up"), (38.2, "point_r")), exprs=((0, "think"), (38.2, "confident")), look=0.8)


def s07(c, t):  # 42.4 - 45.2  passa de R$ 2.200 por mês
    fundo_marca(c, t, "vermelho", holofote=(520, 1050))
    numero_i(c, "O CARRO PASSA DE", 520, 260, 80, CREME)
    contador(c, t, 42.6, 1750, 2250, 520, 420, 170, d=1.2, col=GOLD)
    numero_i(c, "POR MÊS", 520, 560, 80, CREME) if t > 43.6 else None
    consultor_i(c, t, 520, 1300, 1.3, poses=((0, "head"),), exprs=((0, "desperate"),), look=0.0)


def s08(c, t):  # 45.2 - 50.9  agora compara: aplicativo
    cena_rua(c, t, "dia", carros=False)
    numero_i(c, "AGORA COMPARA", 520, 240, 92, GOLD)
    entra(c, t, 46.4, 700, 640, lambda c: notificacao(c, 0, 0, 1.15, "Motorista chegando", "2 por dia útil", NAVY, "APP"), anim="drop")
    entra(c, t, 49.2, 700, 860, lambda c: notificacao(c, 0, 0, 1.15, "+ 8 no fim de semana", "R$ 25 a R$ 30 cada", VERDE, "APP"), anim="drop")
    if t > 46.8:
        k = ease_out(prog(t, 46.8, 1.6))
        c.save(); c.translate(1200 - k * 450, 1290); carro_i(c, t, (0.95, 0.95, 0.95)); c.restore()
    consultor_i(c, t, 220, 1300, 1.35, poses=((0, "hold"), (49.2, "point_r")), exprs=((0, "neutral"), (49.2, "happy")),
                look=0.7, prop=("r", prop_celular_i))


def s09(c, t):  # 50.9 - 53.4  barras: carro x aplicativo
    fundo_marca(c, t, "creme")
    numero_i(c, "POR MÊS", 520, 240, 96, NAVY, contorno=CREME)
    barras_i(c, t, 51.0, 140, 1200, 800, 700, dados=(("Carro", 2250, VERMELHO), ("App", 1340, VERDE)), d=1.0, intervalo=0.4, size_val=84)


def s10(c, t):  # 53.4 - 61.4  ter carro é burrice? não
    cena_sala(c, t, "tarde")
    numero_i(c, "TER CARRO", 520, 230, 96, CREME)
    numero_i(c, "É BURRICE?", 520, 345, 110, GOLD)
    entra(c, t, 55.5, 700, 520, selo("NÃO!", VERDE, 90, CREME), anim="stamp")
    for i, (lab, t0) in enumerate((("roda muito", 56.6), ("filho pequeno", 57.6), ("mora longe", 58.9))):
        def f(c, lab=lab):
            check_icon(c, 30)
            text(c, lab, 50, 4, 56, HAND, NAVY, align="l")
        entra(c, t, t0, 520, 700 + i * 110, f, anim="right")
    entra(c, t, 60.2, 660, 1050, selo("SE PAGA", NAVY, 64, GOLD), anim="pop")
    consultor_i(c, t, 210, 1300, 1.3, poses=((0, "think"), (55.5, "finger_up"), (60.2, "thumb")),
                exprs=((0, "think"), (55.5, "confident"), (60.2, "happy")), look=0.7)


def s11(c, t):  # 61.4 - 66.7  parado na garagem = pagando aluguel pra ele
    cena_rua(c, t, "noite", carros=False)
    numero_i(c, "PARADO A SEMANA?", 520, 240, 80, GOLD)
    carro(c, 640, 1270, 1.25)
    entra(c, t, 63.0, 650, 820, lambda c: placa_preco(c, (("ALUGUEL", "R$ 2.200"), ("DO CARRO", "/mês"))), anim="drop")
    entra(c, t, 65.0, 600, 520, selo("MORA NA GARAGEM", VERMELHO, 52, CREME), anim="stamp")
    consultor_i(c, t, 210, 1300, 1.3, poses=((0, "point_r"), (65.0, "shrug")), exprs=((0, "neutral"), (65.0, "worried")), look=0.7)


def s12(c, t):  # 66.7 - fim  pergunta: carro ou aplicativo?
    fundo_marca(c, t, "navy", holofote=(520, 1050))
    numero_i(c, "CARRO PRÓPRIO", 520, 240, 92, CREME)
    numero_i(c, "OU APLICATIVO?", 520, 360, 92, GOLD)
    entra(c, t, 69.7, 520, 540, selo("DEFENDE SEU LADO", VERMELHO, 56, CREME), anim="stamp")
    consultor_i(c, t, 300, 1300, 1.35, poses=((0, "present"),), exprs=((0, "happy"),), look=0.6)
    pessoa(c, t, 740, 1300, 1.3, "bruno", poses=((0, "think_l"), (68.5, "point_ru")), exprs=((0, "think"), (68.5, "happy")),
           look=-0.5, prop=("r", prop_celular_i))


SCENES = [(0, 3.9, s01), (3.9, 7.0, s02), (7.0, 23.0, s03), (23.0, 30.6, s04), (30.6, 35.8, s05),
          (35.8, 42.4, s06), (42.4, 45.2, s07), (45.2, 50.9, s08), (50.9, 53.4, s09), (53.4, 61.4, s10),
          (61.4, 66.7, s11), (66.7, 999.0, s12)]
