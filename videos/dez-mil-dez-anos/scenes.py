"""Poupança, CDB ou Bolsa? R$ 10 mil em 2016: quem ganhou em 10 anos (Faz a Conta, vídeo longo 16:9, estilo ilustrado).
Narração Calm Carlos (HeyGen Voice), 3 blocos, 0,4 s entre blocos.
Tempos absolutos: bloco1 0,000 | bloco2 175,058 | bloco3 344,596 | fim da fala 560,215 | +5 s de tela final.
Premissas (11/11/2026): aplicação em 10/11/2016, resgate em 10/11/2026; CDI e poupança mês a mês (nov/16 a out/26);
IPCA nov/16 a set/26 + IPCA-15 de out/26; Ibovespa 61.200,95 -> 171.336,99; dólar 3,3615 -> 5,586; IFIX 1.816,56 (out/16)
-> 3.573,50; bitcoin US$ 715,53 -> US$ 73.796. IR de 15% sobre o ganho no CDB e na bolsa. Contas em contas.py."""
import json
import os

from engine import *  # noqa
from ilustrado import *  # noqa

STYLE = "ilustrado"

O2, O3 = 175.058, 344.596
END = 560.215

_PAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras.json"), encoding="utf-8"))


def w(word, after=0.0, d=0.0):
    """início (s) da primeira palavra que começa com `word` depois de `after` (tempo absoluto), mais d"""
    word = word.lower()
    for p in _PAL:
        if p["t0"] >= after - 0.01 and p["w"].lower().strip(",.:?!\"").startswith(word):
            return p["t0"] + d
    raise KeyError((word, after))


# ---------------------------------------------------------------- valores (contas.py)
INFL = 16244
DOLAR, POUP, FII, CDB_B, CDB, BOLSA_B, BOLSA = 16618, 17903, 19672, 24440, 22274, 27996, 25296
BRUNO_20, ANA_20, CARLA_20, CARLA = 10387, 11872, 11589, 23785
CINZA = (0.55, 0.56, 0.60)
CREME_T = (0.99, 0.96, 0.89)
AZUL_D = (0.24, 0.46, 0.78)
R100 = lambda v: brl(round(v / 100) * 100)


# ---------------------------------------------------------------- helpers de desenho
def painel(c, x, y, w_, h, a=0.92, r=26):
    rr(c, x - w_ / 2 + 8, y - h / 2 + 10, w_, h, r); rgb(c, (0, 0, 0), 0.18); c.fill()
    rr(c, x - w_ / 2, y - h / 2, w_, h, r); rgb(c, (1, 1, 1), a); c.fill()


def txt(c, s, x, y, size=48, col=TINTA, font=None, align="c"):
    c.select_font_face(font or HAND); c.set_font_size(size)
    e = c.text_extents(s)
    tx = x - e.x_advance / 2 if align == "c" else (x - e.x_advance if align == "r" else x)
    c.move_to(tx, y + size * 0.35); rgb(c, col); c.show_text(s)


def N(s, size=90, col=GOLD, contorno=TINTA):
    return lambda c: numero_i(c, s, 0, 0, size, col, contorno=contorno)


def titulo(c, t, t0, s, y=120, size=78, col=NAVY, contorno=(1, 1, 1)):
    entra(c, t, t0, 960, y, lambda c: numero_i(c, s, 0, 0, size, col, contorno=contorno), anim="fade")


def cartao(s, sub=None, w_=620, col=NAVY, size=52):
    """cartão branco com texto em Marker (e subtítulo opcional)"""
    def f(c):
        h = 120 if not sub else 170
        painel(c, 0, 0, w_, h, 0.96, 22)
        fs_ = size
        c.select_font_face(MARKER); c.set_font_size(fs_)
        while c.text_extents(s).x_advance > w_ - 50 and fs_ > 20:
            fs_ -= 2; c.set_font_size(fs_)
        if sub:
            txt(c, s, 0, -26, fs_, col, MARKER)
            txt(c, sub, 0, 42, size * 0.62, (0.35, 0.35, 0.4))
        else:
            txt(c, s, 0, 0, fs_, col, MARKER)
    return f


def selo_lugar(s, col=GOLD):
    """medalha redonda com a posição no ranking"""
    def f(c):
        c.new_sub_path(); c.arc(4, 6, 78, 0, 6.283); rgb(c, (0, 0, 0), 0.22); c.fill()
        c.new_sub_path(); c.arc(0, 0, 78, 0, 6.283); rgb(c, col); c.fill()
        c.new_sub_path(); c.arc(0, 0, 62, 0, 6.283); rgb(c, (1, 1, 1), 0.25); c.set_line_width(5); c.stroke()
        txt(c, s, 0, -10, 70, (1, 1, 1), MARKER)
        txt(c, "LUGAR", 0, 40, 22, (1, 1, 1), MARKER)
    return f


def moeda_btc(c, r=70):
    """moeda dourada genérica de cripto (sem logo), com 'BTC' escrito"""
    c.new_sub_path(); c.arc(5, 7, r, 0, 6.283); rgb(c, (0, 0, 0), 0.22); c.fill()
    c.new_sub_path(); c.arc(0, 0, r, 0, 6.283); rgb(c, (0.95, 0.66, 0.18)); c.fill()
    c.new_sub_path(); c.arc(0, 0, r * 0.78, 0, 6.283); rgb(c, (1, 0.82, 0.38)); c.fill()
    txt(c, "BTC", 0, 0, r * 0.62, (0.55, 0.32, 0.05), MARKER)


def tracejada(c, x0, x1, y, col=TINTA, a=0.8, larg=4):
    for k in range(int(x0), int(x1), 30):
        c.rectangle(k, y - larg / 2, 18, larg); rgb(c, col, a); c.fill()


def linha_regua(c, t, t0, x0, x1, yb, h, maxv, lab="inflação: R$ 16.200", col=VERMELHO):
    """linha tracejada da inflação por cima de um barras_i"""
    if t < t0:
        return
    p = ease_out(prog(t, t0, 0.6))
    y = yb - h * INFL / maxv
    tracejada(c, x0, x0 + (x1 - x0) * p, y, col, 0.9, 6)
    if p > 0.9 and lab:
        txt(c, lab, x1, y - 30, 34, col, MARKER, "r")


IBOV = [(0.0, 61201), (0.31, 119528), (0.335, 63570), (0.52, 125000), (0.62, 104000), (0.80, 134000), (0.88, 120000),
        (0.97, 209000), (1.0, 171337)]
EIXO10 = ((0.0, "2016"), (0.335, "2020"), (0.73, "2024"), (1.0, "2026"))


# ================================================================ BLOCO 1
def s01(c, t):  # Ana na poupança, Bruno na bolsa
    cena_sala(c, t, "tarde")
    entra(c, t, 0.3, 960, 190, N("R$ 10.000", 120, GOLD))
    entra(c, t, w("novembro"), 960, 330, cartao("NOVEMBRO DE 2016", w_=520, col=NAVY, size=46), anim="drop")
    pessoa(c, t, 520, 1050, 1.05, "ana", poses=((0, "stand"), (w("deixou"), "present")), exprs=((0, "happy"),), look=0.5,
           appear=w("ana"))
    entra(c, t, w("poupança"), 520, 470, cartao("POUPANÇA", w_=380, col=VERDE), anim="pop")
    pessoa(c, t, 1400, 1050, 1.05, "bruno", poses=((0, "stand"), (w("colocou"), "present_l")), exprs=((0, "confident"),), look=-0.5,
           appear=w("bruno"))
    entra(c, t, w("bolsa"), 1400, 470, cartao("BOLSA", w_=380, col=AZUL_D), anim="pop")


def s02(c, t):  # 10 anos depois: Bruno com 7 mil a mais
    t0 = 7.0
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "10 ANOS DEPOIS", 120, 84)
    barras_i(c, t, t0 + 0.6, 760, 900, 820, 520, (("Ana", POUP, VERDE), ("Bruno", BOLSA, AZUL_D)), maxv=28000, size_val=60, fmt=R100)
    entra(c, t, w("sete", 7), 1170, 250, lambda c: numero_i(c, "+ DE R$ 7 MIL", 0, 0, 74, GOLD), anim="stamp")
    consultor_i(c, t, 330, 1040, 1.05, poses=((0, "present"),), exprs=((0, "happy"),), look=0.7)


def s03(c, t):  # mas em 2020...
    t0 = 11.67
    fundo_marca(c, t, "vermelho", holofote=(1450, 700))
    entra(c, t, t0 + 0.2, 640, 220, N("MAS EM 2020...", 110, CREME_T))
    celular_app(c, t, 640, 640, 1.05, "Bolsa · março/2020", "R$ 10.387", sub="", curva=lambda k: 0.45 + 0.6 * k if k < 0.55 else 0.78 - 1.3 * (k - 0.55),
                cor=VERMELHO, t0=w("menos", t0), d=1.6)
    pessoa(c, t, 1600, 1050, 1.1, "bruno", poses=((0, "stand"), (w("menos", t0), "head")), exprs=((0, "worried"), (w("menos", t0), "desperate")), look=-0.6)
    entra(c, t, w("desistido", t0), 1170, 1000, cartao("QUASE TODO MUNDO DESISTIRIA", w_=700, col=VERMELHO, size=46), anim="up")


def s04(c, t):  # 10 mil, 10 anos, 5 lugares
    t0 = 20.93
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "R$ 10 MIL · 10 ANOS · 5 LUGARES", 120, 70)
    itens = (("poupança", "POUPANÇA", VERDE), ("cdb", "CDB 100% DO CDI", NAVY), ("fundos", "FUNDOS IMOBILIÁRIOS", (0.55, 0.36, 0.20)),
             ("bolsa", "BOLSA (IBOVESPA)", AZUL_D), ("dólar", "DÓLAR", (0.30, 0.50, 0.32)))
    for i, (pal, lab, col) in enumerate(itens):
        x = 820 + (i % 2) * 560
        y = 290 + (i // 2) * 170
        entra(c, t, w(pal, 24), x, y, cartao(lab, w_=520, col=col, size=46), anim="pop")
    entra(c, t, w("sexto", 33), 1100, 820, cartao("SEXTO: FORA DA DISPUTA", "por um motivo que fica pro fim", w_=700, col=VERMELHO, size=50), anim="drop")
    entra(c, t, w("sexto", 33), 1560, 820, lambda c: qmark(c), anim="stamp")
    consultor_i(c, t, 290, 1040, 1.0, poses=((0, "present"), (w("sexto", 33), "think")), exprs=((0, "happy"), (w("sexto", 33), "think")), look=0.7)


def s05(c, t):  # as regras
    t0 = 39.87
    cena_agencia(c, t)
    entra(c, t, t0, 1150, 900, N("AS REGRAS DA CONTA", 70, CREME_T), anim="fade")
    entra(c, t, w("entra", t0), 1150, 300, cartao("ENTRA: 10/11/2016", w_=560, col=VERDE), anim="left")
    entra(c, t, w("sai", t0), 1150, 450, cartao("SAI: 10/11/2026", w_=560, col=VERMELHO), anim="left")
    entra(c, t, w("ninguém", t0), 1150, 600, cartao("NINGUÉM MEXE NO MEIO", w_=560, col=NAVY), anim="left")
    entra(c, t, w("imposto", t0), 1150, 750, cartao("IR JÁ DESCONTADO", w_=560, col=GOLD), anim="left")
    consultor_i(c, t, 360, 1050, 1.05, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.6, prop=("r", prop_calc_i))


def s06(c, t):  # a régua
    t0 = 53.28
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.7)
    entra(c, t, t0 + 0.2, 1200, 220, N("ANTES: A RÉGUA", 100, GOLD))
    entra(c, t, w("subir", t0), 1200, 460, cartao("O SALDO SUBIR", w_=600, col=CINZA, size=56), anim="pop")
    entra(c, t, w("preços", t0), 1200, 640, cartao("SUBIR MAIS QUE OS PREÇOS", w_=760, col=VERDE, size=56), anim="pop")
    if t >= w("preços", t0) + 0.3:
        c.set_line_width(10); rgb(c, VERMELHO)
        c.move_to(930, 460); c.line_to(1470, 460); c.stroke()


def s07(c, t):  # inflação: 10 mil de 2016 = 16.200 hoje
    t0 = 60.85
    cena_mercado(c, t)
    titulo(c, t, t0, "INFLAÇÃO (IPCA) DESDE NOV/2016", 120, 64, CREME_T, TINTA)
    contador(c, t, w("sessenta", t0), 0, 62, 1250, 300, 150, d=1.4, col=VERMELHO, prefixo="+ ", sufixo="%")
    entra(c, t, w("precisa", t0), 1250, 560, lambda c: etiqueta_preco(c, "R$ 16.200", VERMELHO, 70, riscado="R$ 10.000"), anim="drop")
    consultor_i(c, t, 380, 1050, 1.08, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.6)
    rotulo(c, t, w("compra", t0), "O MESMO CARRINHO", "custa R$ 16.200 em 2026", x=620, y=960)


def s08(c, t):  # guarda esse número
    t0 = 75.82
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.7)
    entra(c, t, t0 + 0.2, 1200, 200, N("GUARDA ESSE NÚMERO", 70, CREME_T))
    entra(c, t, w("dezesseis", t0), 1200, 400, N("R$ 16.200", 190, GOLD), anim="stamp")
    entra(c, t, w("abaixo", t0), 1200, 680, cartao("ABAIXO DISSO = PERDEU", "poder de compra, mesmo com saldo maior", w_=820, col=VERMELHO, size=58), anim="up")


def s09(c, t):  # o ranking
    t0 = 83.36
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "O RANKING", 110, 100)
    entra(c, t, w("dez", t0), 1060, 240, N("R$ 10 MIL EM NOV/2016", 60, NAVY, (1, 1, 1)), anim="fade")
    cores = (CINZA, CINZA, CINZA, CINZA, GOLD)
    for i in range(5):
        x = 640 + i * 250
        hh = 120 + i * 70
        ti = 86.0 + i * 0.6
        if t >= ti:
            p = ease_out(prog(t, ti, 0.5))
            rr(c, x - 100, 900 - hh * p, 200, hh * p, 14); rgb(c, P(cores[i])); c.fill()
            if p > 0.8:
                txt(c, f"{5 - i}", x, 900 - hh * p + 44, 64, (1, 1, 1), MARKER)
                entra(c, t, ti + 0.3, x, 900 - hh - 90, lambda c: qmark(c), anim="pop")
    entra(c, t, w("pior", t0), 1140, 960, N("DO PIOR PRO MELHOR", 52, NAVY, (1, 1, 1)), anim="fade")
    consultor_i(c, t, 290, 1040, 1.0, poses=((0, "present"),), exprs=((0, "think"),), look=0.7)


def s10(c, t):  # 5º: dólar (cotação)
    t0 = 94.13
    cena_rua(c, t, "dia")
    entra(c, t, t0 + 0.1, 1450, 200, selo_lugar("5", CINZA), anim="stamp")
    entra(c, t, t0 + 0.3, 1000, 200, N("DÓLAR", 120, (0.30, 0.55, 0.34)))
    entra(c, t, w("custava", t0), 900, 450, lambda c: etiqueta_preco(c, "2016: R$ 3,36", CINZA, 56), anim="drop")
    entra(c, t, w("hoje", t0), 1300, 600, lambda c: etiqueta_preco(c, "HOJE: R$ 5,59", GOLD, 56), anim="drop")
    entra(c, t, w("sessenta", t0), 1100, 820, N("+ 66%", 130, VERDE), anim="stamp")
    consultor_i(c, t, 330, 1050, 1.05, poses=((0, "point_r"), (w("parece", t0), "shrug")), exprs=((0, "neutral"), (w("parece", t0), "think")), look=0.6)


def s11(c, t):  # dólar: 16.600, quase empatou com a inflação
    t0 = 107.12
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "DÓLAR PARADO NÃO RENDE", 110, 76)
    barras_i(c, t, w("viraram", t0), 700, 880, 760, 520, (("Inflação", INFL, VERMELHO), ("Dólar", DOLAR, (0.30, 0.55, 0.34))),
             maxv=18000, size_val=56, fmt=R100)
    entra(c, t, w("empatou", t0), 1600, 520, cartao("QUASE EMPATE", w_=360, col=VERMELHO, size=44), anim="stamp")
    entra(c, t, w("ganho", t0), 1600, 700, N("+ R$ 370", 80, VERDE), anim="pop")
    entra(c, t, w("ganho", t0), 1600, 790, N("de ganho real", 40, NAVY, (1, 1, 1)), anim="fade")
    consultor_i(c, t, 290, 1040, 1.0, poses=((0, "shrug"),), exprs=((0, "worried"),), look=0.7)


def s12(c, t):  # 4º: poupança
    t0 = 119.69
    cena_agencia(c, t)
    entra(c, t, t0 + 0.1, 1610, 190, selo_lugar("4", CINZA), anim="stamp")
    entra(c, t, t0 + 0.3, 1150, 250, N("POUPANÇA", 100, VERDE))
    celular_app(c, t, 1120, 650, 0.95, "Poupança · 10 anos", "R$ 17.900", t0=w("dezessete", t0),
                linhas=(("Guardou", "10.000", NAVY), ("Rendeu", "+ 7.900", VERDE), ("Inflação", "16.200", VERMELHO)), d=1.4)
    entra(c, t, w("pouco", t0), 1580, 520, cartao("+ R$ 1.600", "acima da inflação", w_=380, col=VERDE, size=52), anim="pop")
    entra(c, t, w("anos", t0 + 9), 1580, 760, cartao("2020: 2,1%", "e a inflação: 4,5%", w_=380, col=VERMELHO, size=52), anim="pop")
    consultor_i(c, t, 380, 1050, 1.05, poses=((0, "present"),), exprs=((0, "neutral"),), look=0.6)


def s13(c, t):  # 3º: fundos imobiliários
    t0 = 134.88
    cena_rua(c, t, "tarde")
    entra(c, t, t0 + 0.1, 1700, 330, selo_lugar("3", (0.80, 0.52, 0.26)), anim="stamp")
    entra(c, t, t0 + 0.3, 1080, 200, N("FUNDOS IMOBILIÁRIOS", 88, CREME_T))
    entra(c, t, w("ifix", t0), 1080, 320, N("índice IFIX, rendimentos reinvestidos", 40, CREME_T), anim="fade")
    contador(c, t, w("dezenove", t0), 10000, 19700, 1080, 520, 160, d=1.4, col=GOLD)
    entra(c, t, w("isentos", t0), 1080, 740, cartao("RENDIMENTO MENSAL ISENTO DE IR", w_=760, col=VERDE, size=46), anim="up")
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "present"),), exprs=((0, "happy"),), look=0.6)


def s14(c, t):  # 2º: CDB
    t0 = 146.68
    fundo_marca(c, t, "verde", holofote=(330, 700))
    entra(c, t, t0 + 0.1, 1640, 190, selo_lugar("2", (0.72, 0.74, 0.78)), anim="stamp")
    entra(c, t, t0 + 0.3, 1070, 190, N("CDB 100% DO CDI", 100, CREME_T))
    contador(c, t, w("vinte", t0), 10000, 24400, 1070, 410, 120, d=1.2, col=CREME_T, sufixo=" bruto")
    entra(c, t, w("tirando", t0), 1070, 600, lambda c: numero_i(c, "LÍQUIDO: " + brl(22300), 0, 0, 110, GOLD), anim="stamp")
    entra(c, t, w("deixou", t0), 1070, 820, cartao("+ R$ 4.400 QUE A POUPANÇA", w_=760, col=VERDE, size=50), anim="up")
    consultor_i(c, t, 330, 1040, 1.05, poses=((0, "point_r"),), exprs=((0, "grin"),), look=0.7, prop=("r", prop_calc_i))


def s15(c, t):  # 1º: bolsa
    t0 = 162.15
    fundo_marca(c, t, "verde", holofote=(1560, 700))
    entra(c, t, t0 + 0.1, 300, 190, selo_lugar("1", GOLD), anim="stamp")
    entra(c, t, t0 + 0.3, 800, 190, N("BOLSA", 130, GOLD))
    entra(c, t, w("ibovespa", t0), 800, 320, N("Ibovespa, com dividendos", 44, CREME_T), anim="fade")
    contador(c, t, w("vinte", t0), 10000, 28000, 800, 470, 110, d=1.2, col=CREME_T, sufixo=" bruto")
    entra(c, t, w("descontado", t0), 800, 660, lambda c: numero_i(c, "LÍQUIDO: " + brl(25300), 0, 0, 96, GOLD), anim="stamp")
    entra(c, t, w("duas", t0), 800, 860, N("2,5x O DINHEIRO", 90, CREME_T), anim="pop")
    consultor_i(c, t, 1560, 1040, 1.1, poses=((0, "point_l"), (w("duas", t0), "arms_up")), exprs=((0, "happy"), (w("duas", t0), "grin")), look=-0.7)
    chuva_dinheiro(c, t, w("duas", t0), 10, area=(1350, 1780))


# ================================================================ BLOCO 2
def s16(c, t):  # foto x filme
    t0 = 175.31
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "think"), (w("calma", t0), "finger_up")), exprs=((0, "think"), (w("calma", t0), "confident")), look=0.7)
    entra(c, t, t0 + 0.2, 1180, 200, N("RESOLVIDO?", 120, GOLD))
    entra(c, t, w("foto", t0), 960, 560, cartao("A FOTO DO FIM", w_=480, col=CINZA), anim="pop")
    entra(c, t, w("filme", t0), 1480, 560, cartao("O FILME", w_=400, col=GOLD), anim="pop")
    if t >= w("filme", t0) + 0.2:
        c.set_line_width(9); rgb(c, VERMELHO); c.move_to(740, 560); c.line_to(1180, 560); c.stroke()


def s17(c, t):  # Ana e Bruno começaram com 10 mil
    t0 = 183.33
    cena_sala(c, t, "dia")
    entra(c, t, t0 + 0.2, 960, 180, N("NOV/2016: R$ 10 MIL CADA", 76, GOLD))
    pessoa(c, t, 560, 1050, 1.05, "ana", poses=((0, "stand"), (w("deixou", t0), "present")), exprs=((0, "happy"),), look=0.5)
    entra(c, t, w("poupança", t0), 560, 450, cartao("POUPANÇA", w_=380, col=VERDE), anim="pop")
    pessoa(c, t, 1360, 1050, 1.05, "bruno", poses=((0, "stand"), (w("colocou", t0), "present_l")), exprs=((0, "confident"),), look=-0.5)
    entra(c, t, w("bolsa", t0 + 5), 1360, 450, cartao("BOLSA", w_=380, col=AZUL_D), anim="pop")


def s18(c, t):  # pandemia: a bolsa despenca
    t0 = 191.70
    cena_rua(c, t, "nublado", carros=False)
    entra(c, t, t0 + 0.2, 960, 130, N("PANDEMIA", 110, VERMELHO, (1, 1, 1)))
    grafico_linha(c, t, t0 + 0.6, 560, 840, 1000, 480, [(k / 0.335, v) for k, v in IBOV[:3]], d=w("despencou", t0) - t0 - 0.2, cor=AZUL_D,
                  vmin=40000, vmax=135000, eixo=((0.04, "nov/2016"), (0.96, "mar/2020")),
                  rotulos=((0, "61 mil", NAVY, 50), (1, "119 mil", AZUL_D), (2, "63 mil", VERMELHO, 56)))
    entra(c, t, w("vinte", t0 + 3), 1700, 330, cartao("23/03/2020", w_=300, col=VERMELHO, size=44), anim="drop")
    consultor_i(c, t, 250, 1060, 0.9, poses=((0, "stand"), (w("despencou", t0), "head")), exprs=((0, "worried"), (w("despencou", t0), "shocked")), look=0.6)


def s19(c, t):  # 23/03/2020: Bruno 10.400 x Ana 11.900
    t0 = 201.58
    fundo_marca(c, t, "vermelho")
    titulo(c, t, t0, "23 DE MARÇO DE 2020", 110, 76, CREME_T, TINTA)
    celular_app(c, t, 1260, 560, 1.0, "Bolsa (Bruno)", "R$ 10.387", curva=lambda k: 0.55 + 0.35 * math.sin(k * 3) - 0.6 * max(0, k - 0.75) * 4,
                cor=VERMELHO, t0=w("valiam", t0), d=1.2)
    pessoa(c, t, 1640, 1060, 1.0, "bruno", poses=((0, "head"),), exprs=((0, "desperate"),), look=-0.6)
    celular_app(c, t, 660, 560, 1.0, "Poupança (Ana)", "R$ 11.872", curva=lambda k: 0.2 + 0.5 * k, cor=VERDE, t0=w("tinha", t0), d=1.2)
    pessoa(c, t, 280, 1060, 1.0, "ana", poses=((0, "stand"), (w("tinha", t0), "hips")), exprs=((0, "neutral"), (w("tinha", t0), "happy")), look=0.6)
    entra(c, t, w("praticamente", t0), 1260, 960, cartao("3,5 ANOS: QUASE O MESMO", w_=600, col=VERMELHO, size=44), anim="up")


def s20(c, t):  # Bruno abrindo o app
    t0 = 217.33
    cena_sala(c, t, "noite")
    pessoa(c, t, 760, 1050, 1.1, "bruno", poses=((0, "hold"), (w("piorar", t0), "head")), exprs=((0, "worried"), (w("piorar", t0), "desperate")), look=0.5,
           prop=("r", prop_celular_i))
    entra(c, t, w("aplicativo", t0), 1300, 330, lambda c: notificacao(c, 0, 0, 1.15, "Bolsa despenca de novo", "Ibovespa · março de 2020", VERMELHO, "NOTÍCIAS"), anim="drop")
    entra(c, t, w("espera", t0), 1300, 560, cartao("3,5 ANOS DE ESPERA", w_=560, col=NAVY), anim="pop")
    entra(c, t, w("parando", t0), 1300, 720, cartao("O MUNDO PARANDO", w_=560, col=VERMELHO), anim="pop")
    consultor_i(c, t, 250, 1060, 0.9, poses=((0, "think"),), exprs=((0, "worried"),), look=0.6)


def s21(c, t):  # muita gente vendeu
    t0 = 227.06
    fundo_marca(c, t, "vermelho", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "point_r"),), exprs=((0, "worried"),), look=0.7)
    entra(c, t, t0 + 0.2, 1180, 300, N("MUITA GENTE VENDEU", 96, CREME_T), anim="stamp")
    entra(c, t, w("saiu", t0), 1180, 540, N("SAIU COM R$ 10.400", 92, GOLD))
    entra(c, t, w("perdeu", t0), 1180, 780, cartao("E PERDEU TODA A SUBIDA", "que veio depois", w_=760, col=VERMELHO, size=56), anim="up")


def s22(c, t):  # o Bruno não vendeu
    t0 = 234.84
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "O BRUNO NÃO VENDEU", 110, 86)
    barras_i(c, t, w("hoje", t0), 520, 880, 820, 520, (("Ana", POUP, VERDE), ("Bruno", BOLSA, AZUL_D)), maxv=28000, size_val=60, fmt=R100)
    pessoa(c, t, 1620, 1050, 1.05, "bruno", poses=((0, "stand"), (w("hoje", t0), "arms_up")), exprs=((0, "confident"), (w("hoje", t0), "grin")), look=-0.6)


def s23(c, t):  # montanha-russa até 2026
    t0 = 242.93
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "A MONTANHA-RUSSA DA BOLSA", 110, 74)
    grafico_linha(c, t, t0 + 0.4, 560, 880, 1150, 560, IBOV, d=w("recorde", t0) - t0, cor=AZUL_D, vmin=40000, vmax=225000,
                  eixo=EIXO10, rotulos=((2, "2020", VERMELHO, 56), (7, "209 mil", VERDE), (8, "171 mil", VERMELHO, 60)))
    entra(c, t, w("momento", t0), 900, 330, cartao("NO TOPO: R$ 34 MIL", w_=520, col=VERDE, size=50), anim="pop")
    entra(c, t, w("valem", t0), 900, 470, cartao("UM MÊS DEPOIS: R$ 28 MIL", w_=600, col=VERMELHO, size=50), anim="pop")
    consultor_i(c, t, 250, 1060, 0.9, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.6)


def s24(c, t):  # 6 mil em semanas; o preço do susto
    t0 = 262.70
    cena_sala(c, t, "tarde")
    entra(c, t, t0 + 0.2, 1200, 200, N("- R$ 6 MIL EM SEMANAS", 90, VERMELHO, (1, 1, 1)), anim="stamp")
    pessoa(c, t, 1500, 1050, 1.0, "ana", poses=((0, "relax"),), exprs=((0, "happy"),), look=-0.5)
    entra(c, t, w("poupança", t0), 1500, 420, cartao("POUPANÇA: SEM SUSTO", "nem pra cima, nem pra baixo", w_=560, col=VERDE, size=44), anim="pop")
    entra(c, t, w("susto", t0 + 7), 860, 560, cartao("O PREÇO DO SUSTO", "é o que a bolsa cobra pra pagar mais", w_=660, col=GOLD, size=60), anim="drop")
    consultor_i(c, t, 330, 1060, 1.0, poses=((0, "present"), (w("susto", t0 + 7), "finger_up")), exprs=((0, "think"), (w("susto", t0 + 7), "confident")), look=0.6)


def s25(c, t):  # 5 anos x 10 anos
    t0 = 277.27
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "O VENCEDOR MUDA COM A JANELA", 110, 72)
    def coluna(c, x, t1, cab, linhas):
        entra(c, t, t1, x, 330, cartao(cab, w_=600, col=NAVY, size=50), anim="drop")
        for i, (lab, val, col) in enumerate(linhas):
            entra(c, t, t1 + 0.6 + i * 0.5, x, 540 + i * 200, cartao(f"{i + 1}. {lab}: {val}", w_=600, col=col, size=58), anim="pop")
    coluna(c, 850, w("cinco", t0), "5 ANOS (out/21 a out/26)", (("CDB", "R$ 17.000", VERDE), ("BOLSA", "R$ 16.700", AZUL_D)))
    coluna(c, 1490, w("dez", t0 + 18), "10 ANOS (nov/16 a nov/26)", (("BOLSA", "R$ 25.300", AZUL_D), ("CDB", "R$ 22.300", VERDE)))
    consultor_i(c, t, 280, 1040, 1.0, poses=((0, "present"),), exprs=((0, "think"),), look=0.7)


def s26(c, t):  # depende do prazo e de aguentar
    t0 = 303.49
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "present"), (w("melhor", t0), "finger_up")), exprs=((0, "think"), (w("melhor", t0), "confident")), look=0.7)
    entra(c, t, t0 + 0.2, 1180, 200, cartao("SÓ MUDOU O DIA DE ENTRAR E DE SAIR", w_=1000, col=NAVY, size=52), anim="drop")
    entra(c, t, w("sempre", t0), 1180, 420, N("\"SEMPRE O MELHOR\"?", 96, GOLD), anim="pop")
    if t >= w("janela", t0 + 5):
        p = ease_out(prog(t, w("janela", t0 + 5), 0.4))
        c.set_line_width(14); rgb(c, VERMELHO); c.move_to(760, 420); c.line_to(760 + 840 * p, 420); c.stroke()
    entra(c, t, w("tempo", t0 + 10), 1180, 680, cartao("QUANTO TEMPO PODE FICAR", w_=760, col=VERDE, size=52), anim="pop")
    entra(c, t, w("aguentar", t0 + 13), 1180, 840, cartao("E SE VOCÊ AGUENTA FICAR", w_=760, col=GOLD, size=52), anim="pop")


def s27(c, t):  # 6º lugar: bitcoin
    t0 = 320.32
    cena_escritorio(c, t, "dia")
    entra(c, t, t0 + 0.2, 1100, 180, N("SEXTO LUGAR: FORA DA DISPUTA", 76, CREME_T))
    entra(c, t, w("bitcoin", t0), 1100, 330, N("BITCOIN", 110, (0.95, 0.66, 0.18)), anim="stamp")
    entra(c, t, w("bitcoin", t0), 1580, 330, lambda c: moeda_btc(c, 80), anim="drop")
    entra(c, t, w("custava", t0), 900, 560, lambda c: etiqueta_preco(c, "2016: R$ 2.400", CINZA, 54), anim="drop")
    entra(c, t, w("vale", t0 + 10), 1100, 760, lambda c: etiqueta_preco(c, "HOJE: R$ 412 MIL", GOLD, 54), anim="drop")
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "present"),), exprs=((0, "think"),), look=0.6)


def s28(c, t):  # 1,7 milhão antes do imposto
    t0 = 338.47
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "stand"), (w("antes", t0), "finger_up")), exprs=((0, "shocked"), (w("antes", t0), "think")), look=0.7)
    entra(c, t, t0 + 0.1, 1180, 200, N("OS MESMOS R$ 10 MIL", 70, CREME_T))
    contador(c, t, t0 + 0.6, 10000, 1713859, 1180, 430, 150, d=2.2, col=GOLD)
    entra(c, t, w("antes", t0), 1180, 660, cartao("ANTES DO IMPOSTO", w_=520, col=VERMELHO, size=52), anim="stamp")


# ================================================================ BLOCO 3
def s29(c, t):  # por que ficou de fora: as quedas
    t0 = 344.85
    fundo_marca(c, t, "vermelho", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "think"), (w("primeiro", t0), "finger_up")), exprs=((0, "think"),), look=0.7)
    entra(c, t, t0 + 0.2, 1180, 170, N("POR QUE FICOU DE FORA?", 84, CREME_T))
    entra(c, t, w("primeiro", t0), 1180, 300, cartao("1. O CAMINHO", w_=420, col=VERMELHO), anim="drop")
    for i, (pal, ano, pct) in enumerate((("oitenta", "2018", "- 84%"), ("setenta", "2022", "- 77%"), ("quarenta", "HOJE x RECORDE", "- 40%"))):
        ti = w(pal, t0)
        entra(c, t, ti, 1180, 470 + i * 170, lambda c, ano=ano, pct=pct: (painel(c, 0, 0, 760, 140, 0.95, 22),
              txt(c, ano, -340, 0, 50, NAVY, MARKER, "l"), numero_i(c, pct, 260, 0, 92, VERMELHO, contorno=(1, 1, 1))), anim="left")


def s30(c, t):  # o caminho dos 10 mil no bitcoin (escala log)
    t0 = 361.00
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "OS R$ 10 MIL NO BITCOIN", 110, 76)
    pts = [(0.0, 10000), (0.11, 267000), (0.21, 52000), (0.50, 1590000), (0.60, 342000), (0.89, 2790000), (1.0, 1714000)]
    grafico_linha(c, t, t0 + 0.3, 560, 900, 1150, 600, pts, d=w("trezentos", t0) - t0, cor=(0.90, 0.58, 0.12), log=True,
                  vmin=6000, vmax=6000000, eixo=((0, "2016"), (0.21, "2018"), (0.6, "2022"), (1.0, "2026")),
                  rotulos=((1, "R$ 267 mil", VERDE), (2, "R$ 52 mil", VERMELHO, 56), (3, "R$ 1,6 mi", VERDE),
                           (4, "R$ 342 mil", VERMELHO, 56), (5, "R$ 2,8 mi", VERDE), (6, "R$ 1,7 mi", NAVY, 56)))
    entra(c, t, w("pouquíssima", t0), 1130, 1010, cartao("POUQUÍSSIMA GENTE AGUENTOU SEM VENDER", w_=900, col=VERMELHO, size=44), anim="up")
    consultor_i(c, t, 250, 1060, 0.9, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.6)


def s31(c, t):  # centenas de moedas, a maioria sumiu
    t0 = 377.61
    cena_sala(c, t, "noite")
    entra(c, t, t0 + 0.2, 1120, 160, cartao("2. HOJE A GENTE SABE QUEM GANHOU", w_=980, col=NAVY, size=50), anim="drop")
    ti = w("centenas", t0)
    for i in range(18):
        cx_, cy_ = 760 + (i % 6) * 150, 330 + (i // 6) * 150
        if t >= ti + i * 0.06:
            p = ease_out(prog(t, ti + i * 0.06, 0.3))
            c.save(); c.translate(cx_, cy_); c.scale(p, p)
            c.new_sub_path(); c.arc(0, 0, 52, 0, 6.283); rgb(c, (0.80, 0.80, 0.82) if i != 7 else (0.95, 0.66, 0.18)); c.fill()
            txt(c, "?" if i != 7 else "BTC", 0, 0, 34 if i == 7 else 44, (1, 1, 1), MARKER)
            c.restore()
            if i != 7 and t >= w("sumiu", t0):
                c.save(); c.translate(cx_, cy_); c.scale(0.35, 0.35); x_icon(c); c.restore()
    entra(c, t, w("olhar", t0), 1220, 830, cartao("PRA TRÁS: FÁCIL · ANTES: OUTRA HISTÓRIA", w_=900, col=GOLD, size=44), anim="up")
    consultor_i(c, t, 330, 1060, 1.0, poses=((0, "think"),), exprs=((0, "think"),), look=0.6)


def s32(c, t):  # retrovisor
    t0 = 393.67
    cena_rua(c, t, "tarde")
    entra(c, t, t0 + 0.2, 1150, 200, cartao("CURIOSIDADE, NÃO RECOMENDAÇÃO", w_=900, col=VERMELHO, size=54), anim="stamp")
    entra(c, t, w("retrovisor", t0), 1150, 380, N("ISSO É O RETROVISOR", 84, GOLD))
    entra(c, t, w("aconteceu", t0), 1150, 560, cartao("O QUE ACONTECEU", w_=560, col=NAVY), anim="pop")
    entra(c, t, w("vai", t0 + 6), 1150, 700, cartao("NÃO É O QUE VAI ACONTECER", w_=700, col=NAVY), anim="pop")
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.6)


def s33(c, t):  # lição 1: a régua é a inflação
    t0 = 405.33
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "4 LIÇÕES DA CONTA", 100, 70)
    entra(c, t, w("primeira", t0), 1100, 210, cartao("1. A RÉGUA É A INFLAÇÃO", w_=760, col=VERMELHO, size=52), anim="drop")
    barras_i(c, t, w("dólar", t0), 640, 900, 900, 460, (("Dólar", DOLAR, (0.30, 0.55, 0.34)), ("Poupança", POUP, VERDE)), maxv=20000, size_val=50, fmt=R100)
    linha_regua(c, t, w("dólar", t0) + 1.2, 600, 1580, 900, 460, 20000, lab=None)
    entra(c, t, w("dólar", t0) + 1.6, 1100, 330, N("- - -  inflação: R$ 16.200", 46, VERMELHO, (1, 1, 1)), anim="fade")
    entra(c, t, w("andando", t0), 1660, 640, cartao("ANDANDO", "quase no mesmo lugar", w_=300, col=NAVY, size=40), anim="pop")
    consultor_i(c, t, 280, 1040, 1.0, poses=((0, "present"),), exprs=((0, "think"),), look=0.7)


def s34(c, t):  # lição 2: o prazo escolhe o risco
    t0 = 422.49
    cena_escritorio(c, t, "dia")
    entra(c, t, t0 + 0.2, 1120, 200, cartao("2. O PRAZO ESCOLHE O RISCO", w_=820, col=NAVY, size=52), anim="drop")
    entra(c, t, w("precisar", t0), 1120, 450, cartao("PRECISA EM 1 OU 2 ANOS?", "reserva: nada que caiu quase pela metade", w_=900, col=VERMELHO, size=58), anim="left")
    entra(c, t, w("dez", t0 + 10), 1120, 720, cartao("FICA 10 ANOS PARADO?", "aguenta mais sobe e desce", w_=900, col=VERDE, size=58), anim="left")
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.6)


def s35(c, t):  # lição 3: imposto e custo
    t0 = 440.26
    fundo_marca(c, t, "creme")
    entra(c, t, t0 + 0.2, 1100, 140, cartao("3. IMPOSTO E CUSTO CONTAM", w_=820, col=NAVY, size=52), anim="drop")
    entra(c, t, w("cdb", t0), 860, 420, cartao("CDB: - R$ 2.200 de IR", "de R$ 24.400 para R$ 22.300", w_=560, col=NAVY, size=50), anim="up")
    entra(c, t, w("bolsa", t0 + 3), 1460, 600, cartao("BOLSA: - R$ 2.700 de IR", "de R$ 28.000 para R$ 25.300", w_=560, col=AZUL_D, size=50), anim="up")
    entra(c, t, w("dólar", t0), 1150, 760, cartao("DÓLAR: R$ 0 DE IR... E R$ 0 DE RENDIMENTO", w_=980, col=CINZA, size=44), anim="pop")
    entra(c, t, w("compare", t0), 1150, 920, cartao("COMPARE O QUE SOBRA NO BOLSO", w_=820, col=VERDE, size=50), anim="up")
    consultor_i(c, t, 270, 1040, 0.95, poses=((0, "present"),), exprs=((0, "think"),), look=0.7, prop=("r", prop_calc_i))


def s36(c, t):  # lição 4: Ana, Bruno e Carla
    t0 = 458.19
    cena_sala(c, t, "dia")
    entra(c, t, t0 + 0.2, 960, 150, cartao("4. NÃO PRECISA ESCOLHER UM SÓ", w_=880, col=NAVY, size=52), anim="drop")
    for x, quem, lab, col, pal in ((420, "ana", "TUDO NA POUPANÇA", VERDE, "deixou"), (960, "bruno", "TUDO NA BOLSA", AZUL_D, "colocou"),
                                   (1500, "carla", "METADE E METADE", GOLD, "dividiu")):
        ti = w(pal, t0 + 4)
        pessoa(c, t, x, 1050, 0.95, quem, poses=((0, "stand"), (ti, "present")), exprs=((0, "happy"),), look=0.0, appear=w("três", t0) + (x - 420) / 2000)
        entra(c, t, ti, x, 400, cartao(lab, w_=420, col=col, size=40), anim="pop")
    if t >= w("dividiu", t0 + 4):
        rosca_i(c, t, w("metade", t0 + 4), 1500, 270, 70, 0.5, AZUL_D, fundo=VERDE)


def s37(c, t):  # resultado dos três
    t0 = 476.39
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "10 ANOS DEPOIS", 110, 84)
    barras_i(c, t, t0 + 0.4, 520, 900, 900, 560, (("Ana", POUP, VERDE), ("Carla", CARLA, GOLD), ("Bruno", BOLSA, AZUL_D)),
             maxv=28000, size_val=56, intervalo=w("bruno", t0) - t0 - 0.4, fmt=R100)
    entra(c, t, w("menos", t0 + 8), 1610, 560, cartao("CARLA: + R$ 5.900", "a mais que a Ana", w_=320, col=GOLD, size=36), anim="pop")
    consultor_i(c, t, 260, 1040, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.7)


def s38(c, t):  # março de 2020: o susto menor
    t0 = 489.21
    fundo_marca(c, t, "vermelho", holofote=(1560, 700))
    titulo(c, t, t0, "NO PIOR DIA DA PANDEMIA", 110, 80, CREME_T, TINTA)
    barras_i(c, t, w("bruno", t0), 420, 900, 880, 560, (("Bruno", BRUNO_20, AZUL_D), ("Carla", CARLA_20, GOLD)),
             maxv=13000, size_val=58, fmt=R100, intervalo=w("carla", t0 + 10) - w("bruno", t0))
    entra(c, t, w("susto", t0 + 15), 1560, 280, cartao("SUSTO MENOR", w_=380, col=GOLD, size=52), anim="stamp")
    pessoa(c, t, 1560, 1050, 1.0, "carla", poses=((0, "stand"), (w("susto", t0 + 15), "hips")), exprs=((0, "worried"), (w("susto", t0 + 15), "confident")), look=-0.6)


def s39(c, t):  # quem não vende chega no fim
    t0 = 511.06
    cena_rua(c, t, "crepusculo")
    entra(c, t, t0 + 0.2, 1150, 170, cartao("SUSTO MENOR", w_=480, col=GOLD), anim="drop")
    entra(c, t, w("chance", t0), 1150, 320, cartao("= MAIS CHANCE DE NÃO VENDER", w_=820, col=NAVY), anim="pop")
    entra(c, t, w("chega", t0), 1150, 480, N("QUEM NÃO VENDE CHEGA NO FIM", 70, GOLD), anim="pop")
    entra(c, t, w("chega", t0), 1600, 900, lambda c: finish_flag(c, 260), anim="drop")
    pessoa(c, t, 1250, 1060, 0.9, "carla", poses=((0, "stand"),), exprs=((0, "happy"),), look=0.5, andar=True)
    consultor_i(c, t, 330, 1060, 1.0, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.6)


def s40(c, t):  # resumo: todas as barras + régua da inflação
    t0 = 521.32
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "R$ 10 MIL EM 2016 VIRARAM...", 100, 70)
    dados = (("Dólar", DOLAR, (0.30, 0.55, 0.34)), ("Poupança", POUP, VERDE), ("FIIs", FII, (0.80, 0.52, 0.26)),
             ("CDB", CDB, NAVY), ("Bolsa", BOLSA, AZUL_D))
    t1 = w("dezesseis", t0)
    barras_i(c, t, t1, 520, 920, 1200, 620, dados, maxv=27000, size_val=46, intervalo=(w("bolsa", t0) - t1) / 4, fmt=R100)
    linha_regua(c, t, w("inflação", t0), 500, 1740, 920, 620, 27000, lab=None)
    entra(c, t, w("inflação", t0), 1400, 230, N("- - -  inflação pedia R$ 16.200", 44, VERMELHO, (1, 1, 1)), anim="fade")
    entra(c, t, w("bolsa", t0), 1400, 175, N("valores líquidos", 36, NAVY, (1, 1, 1)), anim="fade")
    consultor_i(c, t, 240, 1060, 0.85, poses=((0, "present"),), exprs=((0, "happy"),), look=0.7)


def s41(c, t):  # quem ficou e aguentou
    t0 = 541.90
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "present"), (w("acertou", t0), "finger_up")), exprs=((0, "grin"), (w("acertou", t0), "confident")), look=0.7)
    entra(c, t, t0 + 0.2, 1180, 400, N("GANHOU QUEM FICOU", 100, GOLD))
    entra(c, t, w("aguentou", t0), 1180, 570, N("E AGUENTOU O CAMINHO", 84, CREME_T))
    entra(c, t, w("acertou", t0), 1180, 800, cartao("NÃO QUEM ACERTOU O DIA", w_=700, col=VERMELHO, size=56), anim="stamp")


def s42(c, t):  # comenta aí + vídeo dos 100 mil
    t0 = 546.19
    cena_escritorio(c, t, "crepusculo")
    pessoa(c, t, 1620, 1060, 0.95, "ana", poses=((0, "stand"),), exprs=((0, "happy"),), look=-0.5)
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "present"), (w("quiser", t0), "point_r")), exprs=((0, "happy"),), look=0.6)
    entra(c, t, t0 + 0.4, 1000, 220, cartao("ONDE ESTARIAM SEUS 10 MIL DE 2016?", "e onde você colocaria pros próximos 10 anos?", w_=1050, col=NAVY, size=52), anim="drop")
    entra(c, t, w("comenta", t0), 1000, 400, N("COMENTA AÍ", 80, GOLD), anim="pop")
    entra(c, t, w("quiser", t0), 1000, 650, lambda c: video_card(c, "PRIMEIROS R$ 100 MIL", "quanto tempo leva?", w=760, h=360), anim="up")
    entra(c, t, t0 + 1, 960, 1035, lambda c: txt(c, "conteúdo educativo, não é recomendação de investimento", 0, 0, 30, (1, 1, 1)), anim="fade")


def s43(c, t):  # Tela final (5 s sem narração)
    tela_final_i(c, t, END)


SCENES = [
    (0.0, 7.0, s01), (7.0, 11.67, s02), (11.67, 20.93, s03), (20.93, 39.87, s04), (39.87, 53.28, s05),
    (53.28, 60.85, s06), (60.85, 75.82, s07), (75.82, 83.36, s08), (83.36, 94.13, s09), (94.13, 107.12, s10),
    (107.12, 119.69, s11), (119.69, 134.88, s12), (134.88, 146.68, s13), (146.68, 162.15, s14), (162.15, 175.31, s15),
    (175.31, 183.33, s16), (183.33, 191.70, s17), (191.70, 201.58, s18), (201.58, 217.33, s19), (217.33, 227.06, s20),
    (227.06, 234.84, s21), (234.84, 242.93, s22), (242.93, 262.70, s23), (262.70, 277.27, s24), (277.27, 303.49, s25),
    (303.49, 320.32, s26), (320.32, 338.47, s27), (338.47, 344.85, s28),
    (344.85, 361.00, s29), (361.00, 377.61, s30), (377.61, 393.67, s31), (393.67, 405.33, s32), (405.33, 422.49, s33),
    (422.49, 440.26, s34), (440.26, 458.19, s35), (458.19, 476.39, s36), (476.39, 489.21, s37), (489.21, 511.06, s38),
    (511.06, 521.32, s39), (521.32, 541.90, s40), (541.90, 546.19, s41), (546.19, END, s42), (END, 999.0, s43),
]

# só toques pontuais, sem ruído: régua 16.200 / 1º lugar / fundo de 2020 / resumo
SFX = [(w("dezesseis", 75.82), "tum"), (w("vinte", 166.0), "soft_ding"), (w("dez", 201.58), "tum"),
       (w("inflação", 538.0), "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")
