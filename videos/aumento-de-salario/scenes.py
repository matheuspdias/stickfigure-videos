"""Ganhei R$ 1.000 de aumento e só vieram R$ 475 (Faz a Conta, vídeo longo 16:9, estilo ilustrado).
Narração Calm Carlos (HeyGen, ElevenLabs v4), 3 blocos, 0,4 s entre blocos.
Tempos absolutos: bloco1 0,000 | bloco2 179,600 | bloco3 355,595 | fim da fala 543,024 | +5 s de tela final.
Premissas (08/11/2026): INSS 2026 (Portaria MPS/MF 13/2026, teto 8.475,55), IR 2026 (Lei 15.270/2025: isento até
5.000; redução 978,62 - 0,133145 x renda até 7.350), CLT, sem dependentes. Contas em contas.py."""
import json
import os

from engine import *  # noqa
from ilustrado import *  # noqa

STYLE = "ilustrado"

O2, O3 = 179.6, 355.595
END = 543.024

_PAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras.json"), encoding="utf-8"))


def w(word, after=0.0, d=0.0):
    """início (s) da primeira palavra que começa com `word` depois de `after` (tempo absoluto), mais d"""
    word = word.lower()
    for p in _PAL:
        if p["t0"] >= after - 0.01 and p["w"].lower().strip(",.:?!\"").startswith(word):
            return p["t0"] + d
    raise KeyError((word, after))


# ---------------------------------------------------------------- contas (as mesmas do contas.py)
FX = [(1621.00, .075), (2902.84, .09), (4354.27, .12), (8475.55, .14)]


def inss(s):
    tot, ant = 0.0, 0.0
    for lim, a in FX:
        if s > ant:
            tot += (min(s, lim) - ant) * a
        ant = lim
    return tot


def ir(s):
    base = s - max(inss(s), 607.20)
    imp = 0.0
    for lim, a, p in [(2428.80, 0, 0), (2826.65, .075, 182.16), (3751.05, .15, 394.16), (4664.68, .225, 675.49), (1e12, .275, 908.73)]:
        if base <= lim:
            imp = max(0.0, base * a - p); break
    red = imp if s <= 5000 else (max(0, 978.62 - 0.133145 * s) if s <= 7350 else 0)
    return max(0.0, imp - red)


# ---------------------------------------------------------------- helpers de desenho
CREME_T = (0.99, 0.96, 0.89)


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


def regua(c, t, t0, x0=260, y=560, w_=1400, marca=None, t_m=None, destaque=None):
    """régua do IR 2026: 0-5 mil isento | 5-7,35 mil desconto que diminui | acima tabela cheia"""
    smax = 10000.0
    xs = lambda s: x0 + w_ * s / smax
    segs = [(0, 5000, VERDE, "IMPOSTO ZERO"), (5000, 7350, GOLD, "DESCONTO"), (7350, smax, VERMELHO, "TABELA CHEIA")]
    for i, (a, b, col, lab) in enumerate(segs):
        ti = t0 + i * 0.9
        if t < ti:
            continue
        p = ease_out(prog(t, ti, 0.6))
        xa, xb = xs(a), xs(a) + (xs(b) - xs(a)) * p
        if i == 1:
            g = cairo.LinearGradient(xs(a), 0, xs(b), 0)
            g.add_color_stop_rgb(0, *GOLD); g.add_color_stop_rgb(1, *mix(GOLD, VERMELHO, 0.55))
            rr(c, xa, y - 45, xb - xa, 90, 14); c.set_source(g); c.fill()
        else:
            rr(c, xa, y - 45, xb - xa, 90, 14); rgb(c, col); c.fill()
        if p > 0.95:
            cx_ = (xs(a) + xs(b)) / 2
            fs_ = 34 if i != 1 else 30
            txt(c, lab, cx_, y, fs_, (1, 1, 1), MARKER)
    if t >= t0:
        for s_, lab in ((0, "R$ 0"), (5000, "R$ 5.000"), (7350, "R$ 7.350"), (10000, "R$ 10 mil")):
            if t >= t0 + (0 if s_ <= 5000 else 0.9 if s_ == 7350 else 1.8):
                c.rectangle(xs(s_) - 2, y + 48, 4, 26); rgb(c, TINTA); c.fill()
                txt(c, lab, xs(s_), y + 100, 38, TINTA, MARKER)
    if destaque and t >= destaque:
        p = ease_out(prog(t, destaque, 0.5))
        c.set_line_width(10); rgb(c, VERMELHO, p)
        rr(c, xs(5000) - 16, y - 66, xs(7350) - xs(5000) + 32, 132, 22); c.stroke()
    if marca is not None and t_m is not None and t >= t_m:
        p = ease_out(prog(t, t_m, 0.5))
        mx = xs(marca)
        c.save(); c.translate(mx, y - 70 - 30 * (1 - p))
        pg(c, [(-26, -40), (26, -40), (0, 0)]); rgb(c, NAVY, p); c.fill()
        c.restore()
        numero_i(c, brl(marca), mx, y - 150, 54, NAVY, contorno=(1, 1, 1), alpha=p)


def escada(c, t, tempos, x0=330, yb=880, w_=1440, h=520, foco=None):
    """aumento de R$ 1.000 a partir de cada salário: quanto fica no bolso (barras em posições fixas)"""
    dados = [("2 mil", 907), ("3 mil", 880), ("4 mil", 867), ("5 mil", 475), ("6 mil", 490), ("7 mil", 577),
             ("8 mil", 677), ("10 mil", 725)]
    n = len(dados)
    bw = w_ / n * 0.62
    c.rectangle(x0 - 20, yb, w_ + 40, 5); rgb(c, (0.3, 0.3, 0.35)); c.fill()
    # linha dos R$ 1.000
    yk = yb - h * 1000 / 1000
    for k in range(0, int(w_ + 40), 34):
        c.rectangle(x0 - 20 + k, yk, 18, 3); rgb(c, (0.45, 0.45, 0.5)); c.fill()
    txt(c, "R$ 1.000 de aumento", x0 - 16, yk - 26, 30, (0.4, 0.4, 0.45), HAND, "l")
    for i, ((lab, v), ti) in enumerate(zip(dados, tempos)):
        cx_ = x0 + w_ * (i + 0.5) / n
        col = VERMELHO if v < 500 else (VERDE if v > 800 else (GOLD if v < 700 else BLUE))
        txt(c, lab, cx_, yb + 44, 36, dk(col, 0.25), MARKER)
        if ti is None or t < ti:
            continue
        p = ease_out(prog(t, ti, 0.9))
        bh = h * v / 1000 * p
        a = 1.0 if (foco is None or i in foco) else 0.35
        rr(c, cx_ - bw / 2, yb - bh, bw, bh + 4, 12); rgb(c, P(col), a); c.fill()
        numero_i(c, brl(v * p), cx_, yb - bh - 34, 40, col, alpha=a)
    txt(c, "salário antes do aumento", x0 + w_ / 2, yb + 92, 32, (0.4, 0.4, 0.45))


# ================================================================ BLOCO 1
def s01(c, t):  # o Lucas ganha 5 mil
    cena_escritorio(c, t, "dia")
    pessoa(c, t, 1180, 1050, 1.08, "lucas", poses=((0, "stand"), (w("ganha"), "present_l")), exprs=((0, "neutral"), (w("ganha"), "happy")), look=-0.5)
    consultor_i(c, t, 330, 1050, 1.05, poses=((0, "present"),), exprs=((0, "happy"),), look=0.6)
    entra(c, t, w("carteira"), 1180, 300, cartao("CARTEIRA ASSINADA", w_=560), anim="drop")
    entra(c, t, w("cinco", 2), 1180, 440, N("R$ 5.000 /mês", 96, GOLD))
    entra(c, t, w("promoção", 7), 760, 720, lambda c: notificacao(c, 0, 0, 1.0, "Promoção aprovada!", "RH · novo salário", VERDE, "RH"), anim="drop")


def s02(c, t):  # salário vai pra 6 mil
    t0 = w("salário", 9.5)
    fundo_marca(c, t, "verde", holofote=(1380, 700))
    pessoa(c, t, 1380, 1040, 1.1, "lucas", poses=((0, "arms_up"),), exprs=((0, "grin"),), look=-0.4)
    consultor_i(c, t, 300, 1040, 1.0, poses=((0, "point_r"),), exprs=((0, "happy"),), look=0.7)
    titulo(c, t, t0, "PROMOÇÃO!", 130, 96, GOLD, TINTA)
    contador(c, t, w("seis", 10), 5000, 6000, 780, 420, 150, d=1.2, col=CREME_T)
    entra(c, t, w("mil", 12.5), 780, 640, N("+ R$ 1.000", 120, GOLD))
    entra(c, t, w("todo", 13.9), 780, 790, N("TODO MÊS", 60, CREME_T))
    chuva_dinheiro(c, t, w("mil", 12.5), 12, area=(1100, 1700))


def s03(c, t):  # os planos: carro com parcela de 800
    cena_rua(c, t, "tarde")
    pessoa(c, t, 760, 1050, 1.05, "lucas", poses=((0, "think"), (w("guardar", 20), "present")), exprs=((0, "happy"),), look=0.5)
    consultor_i(c, t, 260, 1050, 0.95, poses=((0, "stand"),), exprs=((0, "worried"),), look=0.6)
    entra(c, t, w("trocar"), 1360, 820, lambda c: carro_i(c, t, (0.20, 0.44, 0.74)), anim="right")
    entra(c, t, w("oitocentos"), 1080, 420, lambda c: etiqueta_preco(c, "PARCELA R$ 800", GOLD, 54), anim="drop")
    entra(c, t, w("guardar", 20), 760, 300, cartao("+ R$ 200 PRA GUARDAR", w_=600, col=VERDE), anim="pop")


def s04(c, t):  # os dois contracheques
    cena_sala(c, t, "tarde")
    pessoa(c, t, 260, 1060, 1.0, "lucas", poses=((0, "stand"), (w("diferença", 35), "head")), exprs=((0, "neutral"), (w("diferença", 35), "shocked")), look=0.6)
    entra(c, t, w("líquido", 27), 800, 500, lambda c: contracheque(c, 0, 0, 1.0, "R$ 5.000", (("INSS", "- R$ 501,51"), ("IR", "R$ 0,00")), "R$ 4.498,49"), anim="up")
    entra(c, t, w("novo", 31.5), 1410, 500, lambda c: contracheque(c, 0, 0, 1.0, "R$ 6.000", (("INSS", "- R$ 641,51"), ("IR", "- R$ 385,10")), "R$ 4.973,39"), anim="up")
    entra(c, t, w("líquido", 27), 800, 170, N("MÊS PASSADO", 52, CREME_T), anim="fade")
    entra(c, t, w("novo", 31.5), 1410, 170, N("SALÁRIO NOVO", 52, GOLD), anim="fade")


def s05(c, t):  # a diferença: 474,90
    t0 = w("diferença", 35)
    fundo_marca(c, t, "vermelho", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "stand"), (t0 + 2.0, "head")), exprs=((0, "worried"), (t0 + 2.0, "shocked")), look=0.7)
    titulo(c, t, t0, "A DIFERENÇA DE VERDADE", 120, 70, CREME_T, TINTA)
    contador(c, t, w("quatrocentos", 38), 0, 474.90, 1200, 360, 150, d=1.8, col=CREME_T, casas=2, prefixo="+ R$ ")
    entra(c, t, w("dos", 42), 1200, 540, lambda c: etiqueta_preco(c, "R$ 474,90", GOLD, 50, riscado="R$ 1.000"), anim="drop")
    if t >= w("metade", 44):
        rosca_i(c, t, w("metade", 44), 1200, 820, 130, 0.525, (0.98, 0.86, 0.40), fundo=(0.55, 0.20, 0.18), texto="-53%")
        entra(c, t, w("sumiu", 45), 1560, 820, N("SUMIU", 70, CREME_T), anim="stamp")


def s06(c, t):  # não foi erro do RH: a faixa escondida
    fundo_marca(c, t, "navy", holofote=(360, 700))
    consultor_i(c, t, 360, 1040, 1.1, poses=((0, "finger_up"), (w("esconde"), "present")), exprs=((0, "confident"), (w("esconde"), "think")), look=0.7)
    entra(c, t, w("não", 47.5), 1180, 260, cartao("NÃO FOI ERRO DO RH", w_=720, col=VERMELHO, size=56), anim="stamp")
    entra(c, t, w("certinha"), 1180, 450, N("É A CONTA DE 2026", 70, CREME_T, NAVY))
    entra(c, t, w("faixa", 52.5), 1180, 680, cartao("A FAIXA ESCONDIDA", "onde o aumento rende menos", w_=760, col=GOLD, size=60), anim="pop")


def s07(c, t):  # o que vem no vídeo
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 300, 1040, 1.05, poses=((0, "present"),), exprs=((0, "happy"),), look=0.7)
    titulo(c, t, w("hoje", 57), "A CONTA COMPLETA", 120, 80)
    itens = [("pra", 59.9, "PRA ONDE FOI O DINHEIRO"), ("quem", 62, "QUEM CAI NESSA FAIXA"),
             ("se", 63.9, "AUMENTO FAZ GANHAR MENOS?"), ("e", 66.7, "O QUE FAZER COM ISSO")]
    for i, (pal, aft, s_) in enumerate(itens):
        entra(c, t, w(pal, aft), 1140, 300 + i * 165, cartao(f"{i + 1}. {s_}", w_=980, size=50), anim="left")


def s08(c, t):  # a regra nova do IR
    t0 = w("desde", 68.9)
    fundo_marca(c, t, "creme")
    titulo(c, t, t0, "IMPOSTO DE RENDA 2026", 120, 80)
    entra(c, t, w("nova", 71), 960, 240, N("NOVA REGRA (LEI 15.270/2025)", 46, GOLD), anim="fade")
    regua(c, t, w("quem", 73), 260, 520)
    entra(c, t, w("diminuindo", 83), 1300, 820, cartao("o desconto diminui até sumir", w_=680, col=dk(GOLD, 0.3), size=44), anim="up")
    consultor_i(c, t, 220, 1060, 0.85, poses=((0, "point_r"),), exprs=((0, "confident"),), look=0.7)


def s09(c, t):  # com 5 mil: só INSS
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 330, 1040, 1.05, poses=((0, "present"), (w("zero", 92), "thumb")), exprs=((0, "neutral"), (w("zero", 92), "happy")), look=0.7)
    titulo(c, t, w("com", 85.8), "COM R$ 5.000", 120, 84)
    entra(c, t, w("inss", 88.5), 1000, 330, cartao("INSS: - R$ 501,51", w_=640, col=VERMELHO, size=56), anim="left")
    entra(c, t, w("imposto", 91.5), 1000, 500, cartao("IR: R$ 0,00", w_=640, col=VERDE, size=56), anim="left")
    entra(c, t, w("líquido", 94), 1000, 720, N("LÍQUIDO: R$ 4.498,49", 80, VERDE))
    entra(c, t, w("imposto", 91.5), 1450, 500, lambda c: check_icon(c, 40), anim="stamp")


def s10(c, t):  # com 6 mil: INSS sobe, IR aparece
    cena_escritorio(c, t, "tarde")
    pessoa(c, t, 1730, 1060, 0.95, "lucas", poses=((0, "stand"), (w("aparece", 109), "head")), exprs=((0, "neutral"), (w("aparece", 109), "worried")), look=-0.6)
    consultor_i(c, t, 280, 1060, 1.0, poses=((0, "point_r"),), exprs=((0, "think"),), look=0.7)
    titulo(c, t, w("com", 97.4), "COM R$ 6.000", 120, 84, NAVY, (1, 1, 1))
    entra(c, t, w("inss", 98.5), 900, 330, cartao("INSS: - R$ 641,51", w_=640, col=VERMELHO, size=56), anim="left")
    entra(c, t, w("cento", 102.6), 1340, 330, N("+ R$ 140", 70, VERMELHO, (1, 1, 1)), anim="pop")
    entra(c, t, w("quatorze", 105.8), 900, 470, cartao("14% de cada real nessa faixa", w_=640, col=NAVY, size=40), anim="fade")
    entra(c, t, w("aparece", 109), 900, 650, cartao("IR: - R$ 385,10", w_=640, col=VERMELHO, size=56), anim="left")
    entra(c, t, w("zero", 111.9), 1340, 650, lambda c: etiqueta_preco(c, "R$ 385", VERMELHO, 46, riscado="ERA R$ 0"), anim="drop")


def s11(c, t):  # somando: 525
    fundo_marca(c, t, "vermelho", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "point_r"), (w("quinhentos", 120), "head")), exprs=((0, "worried"), (w("quinhentos", 120), "desperate")), look=0.7)
    entra(c, t, w("cento", 115.9), 1180, 260, N("R$ 140 de INSS", 76, CREME_T))
    entra(c, t, w("trezentos", 118.4), 1180, 400, N("+ R$ 385 de IR", 76, CREME_T))
    if t >= w("quinhentos", 120.8):
        c.rectangle(820, 490, 720, 8); rgb(c, CREME_T); c.fill()
    contador(c, t, w("quinhentos", 120.8), 0, 525, 1180, 610, 150, d=1.0, col=(0.98, 0.86, 0.40), prefixo="= R$ ")
    entra(c, t, w("sumiu", 123.5), 1180, 820, N("SUMIU DOS R$ 1.000", 62, CREME_T), anim="stamp")


def s12(c, t):  # por quê? 1) alíquota de 27,5%
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 300, 1040, 1.05, poses=((0, "think"), (w("primeira", 132), "finger_up")), exprs=((0, "think"), (w("primeira", 132), "confident")), look=0.7)
    titulo(c, t, w("mas", 125.8), "POR QUE TANTO IMPOSTO?", 120, 80)
    entra(c, t, w("duas", 130.4), 1150, 260, N("DUAS COISAS AO MESMO TEMPO", 52, GOLD), anim="fade")
    entra(c, t, w("primeira", 132.3), 1150, 470, cartao("1. ALÍQUOTA MAIS ALTA", "a partir de uns R$ 5.200 de salário", w_=860, size=56), anim="left")
    if t >= w("vinte", 138.9):
        rosca_i(c, t, w("vinte", 138.9), 1150, 780, 120, 0.275, VERMELHO, texto="27,5%")


def s13(c, t):  # 2) o desconto encolhe 13 centavos por real
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 300, 1040, 1.05, poses=((0, "finger_up"), (w("treze", 148), "present")), exprs=((0, "confident"),), look=0.7)
    entra(c, t, w("segunda", 140.9), 1150, 200, cartao("2. O DESCONTO ENCOLHE", w_=860, size=56), anim="left")
    t0 = w("encolhendo", 144)
    # barra do desconto: R$ 312,89 em 5.000 -> 0 em 7.350
    x0, yb, ww, hh = 700, 760, 900, 360
    c.rectangle(x0 - 10, yb, ww + 20, 5); rgb(c, (0.3, 0.3, 0.35)); c.fill()
    txt(c, "R$ 5.000", x0, yb + 40, 34, TINTA, MARKER, "l")
    txt(c, "R$ 7.350", x0 + ww, yb + 40, 34, TINTA, MARKER, "r")
    if t >= t0:
        p = ease_io(prog(t, t0, 2.0))
        pg(c, [(x0, yb), (x0, yb - hh), (x0 + ww * p, yb - hh * (1 - p)), (x0 + ww * p, yb)])
        rgb(c, P(GOLD)); c.fill()
        numero_i(c, "R$ 312,89", x0 + 10, yb - hh - 40, 50, dk(GOLD, 0.2), alinhamento="l")
        if p > 0.98:
            numero_i(c, "R$ 0", x0 + ww, yb - 50, 50, VERMELHO, alinhamento="r")
    txt(c, "desconto no imposto", x0 + ww / 2, yb + 90, 34, (0.4, 0.4, 0.45))
    entra(c, t, w("treze", 148), 1380, 420, N("- R$ 0,13 por real", 54, VERMELHO, (1, 1, 1)), anim="stamp")


def s14(c, t):  # de cada 100, ficam 49
    t0 = w("de", 154.8)
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "present"), (w("embora", 164), "head")), exprs=((0, "think"), (w("embora", 164), "shocked")), look=0.7)
    titulo(c, t, t0, "DE CADA R$ 100 A MAIS", 120, 76, GOLD, TINTA)
    entra(c, t, t0 + 0.5, 1180, 230, N("entre R$ 5.000 e R$ 7.350", 46, CREME_T, NAVY), anim="fade")
    barras_i(c, t, w("só", 160.3), 760, 880, 860, 480, (("FICA", 49, VERDE), ("INSS", 14, GOLD), ("IR", 37, VERMELHO)),
             fmt=lambda v: brl(v), d=1.0, maxv=55, intervalo=0.35, size_val=60)
    entra(c, t, w("mais", 163), 1600, 400, N("51% VAI EMBORA", 50, CREME_T, VERMELHO), anim="stamp")


def s15(c, t):  # comparação: 4->5 mil x 5->6 mil
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 300, 1040, 1.05, poses=((0, "point_r"), (w("dobro", 175), "arms_up")), exprs=((0, "neutral"), (w("dobro", 175), "shocked")), look=0.7)
    titulo(c, t, w("pra", 164.8), "MESMO AUMENTO DE R$ 1.000", 120, 74)
    barras_i(c, t, w("quatro", 168.3), 760, 880, 900, 560,
             (("DE 4 PRA 5 MIL", 867, VERDE), ("DE 5 PRA 6 MIL", 475, VERMELHO)), d=1.2, maxv=900, intervalo=4.0, size_val=64)
    entra(c, t, w("dobro", 175.6), 1480, 270, N("QUASE O DOBRO", 54, VERDE, (1, 1, 1)), anim="stamp")
    if t < w("quatro", 168.3) + 4.0:
        pass


# ================================================================ BLOCO 2
def s16(c, t):  # a escada inteira: premissas
    cena_escritorio(c, t, "dia")
    consultor_i(c, t, 360, 1060, 1.08, poses=((0, "present"),), exprs=((0, "confident"),), look=0.6, prop=("l", prop_tablet_i))
    entra(c, t, O2 + 0.2, 1150, 260, cartao("QUANTO FICA DE R$ 1.000 DE AUMENTO?", w_=1100, size=52), anim="drop")
    for i, (pal, aft) in enumerate((("carteira", O2 + 6), ("dependentes", O2 + 7.5), ("tabelas", O2 + 8.8))):
        lab = ["carteira assinada (CLT)", "sem dependentes", "tabelas de 2026"][i]
        entra(c, t, w(pal, aft), 1150, 460 + i * 130, cartao(lab, w_=560, col=NAVY, size=46), anim="left")


def _tempos_escada():
    return [w("novecentos", O2 + 13), w("oitocentos", O2 + 16.5), w("oitocentos", O2 + 19.8), w("quatrocentos", O2 + 28.4),
            w("quatrocentos", O2 + 32.6), w("quinhentos", O2 + 44.7), w("seiscentos", O2 + 48.1), w("setecentos", O2 + 56.1)]


def s17(c, t):  # escada: 2, 3, 4 mil
    fundo_marca(c, t, "creme")
    titulo(c, t, O2 + 10.2, "AUMENTO DE R$ 1.000: QUANTO FICA", 110, 66)
    escada(c, t, _tempos_escada())
    if t >= w("quase", O2 + 22.8):
        entra(c, t, w("quase", O2 + 22.8), 690, 200, N("QUASE TUDO CHEGA", 46, VERDE, (1, 1, 1)), anim="pop")


def s18(c, t):  # escada: o tombo 5 e 6 mil
    fundo_marca(c, t, "creme")
    titulo(c, t, 0, "AUMENTO DE R$ 1.000: QUANTO FICA", 110, 66)
    escada(c, t, _tempos_escada())
    t0 = w("tombo", O2 + 26)
    entra(c, t, t0, 690, 200, N("QUASE TUDO CHEGA", 46, VERDE, (1, 1, 1)), anim="fade", d=0.01)
    if t >= w("faixa", O2 + 34.8):
        p = ease_out(prog(t, w("faixa", O2 + 34.8), 0.5))
        x0, w_, n = 330, 1440, 8
        xa = x0 + w_ * 3 / n + 10; xb = x0 + w_ * 5 / n - 10
        c.set_line_width(8); rgb(c, VERMELHO, p); rr(c, xa, 330, xb - xa, 560, 22); c.stroke()
        numero_i(c, "MENOS DA METADE", (xa + xb) / 2, 290, 44, VERMELHO, contorno=(1, 1, 1), alpha=p)
    entra(c, t, t0, 1400, 220, N("O TOMBO", 64, VERMELHO, (1, 1, 1)), anim="stamp")


def s19(c, t):  # escada: 7 e 8 mil, o desconto acaba
    fundo_marca(c, t, "creme")
    titulo(c, t, 0, "AUMENTO DE R$ 1.000: QUANTO FICA", 110, 66)
    escada(c, t, _tempos_escada())
    entra(c, t, w("desconto", O2 + 40.6), 1450, 220, cartao("acima de R$ 7.350: o desconto acaba", w_=640, col=NAVY, size=40), anim="drop")


def s20(c, t):  # a parte mais estranha: 10 mil fica com 725
    fundo_marca(c, t, "navy", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "think"), (w("setecentos", O2 + 56), "point_r")), exprs=((0, "think"), (w("setecentos", O2 + 56), "shocked")), look=0.7)
    titulo(c, t, w("parte", O2 + 51), "A PARTE MAIS ESTRANHA", 120, 76, GOLD, TINTA)
    entra(c, t, w("dez", O2 + 53.3), 1180, 280, N("DE R$ 10 MIL PRA R$ 11 MIL", 56, CREME_T, NAVY), anim="fade")
    contador(c, t, w("setecentos", O2 + 56), 0, 725, 1180, 450, 150, d=1.4, col=VERDE, prefixo="+ R$ ")
    entra(c, t, w("teto", O2 + 60), 1180, 690, cartao("TETO DO INSS: R$ 8.475,55", "acima dele, o INSS para de subir", w_=780, col=NAVY, size=52), anim="up")
    entra(c, t, w("sobra", O2 + 66.8), 1180, 880, N("SÓ O IR: 27,5%", 56, GOLD, TINTA), anim="pop")


def s21(c, t):  # duelo: 5 mil x 10 mil
    cena_escritorio(c, t, "crepusculo")
    pessoa(c, t, 560, 1060, 1.0, "lucas", poses=((0, "shrug"),), exprs=((0, "worried"),), look=0.4)
    pessoa(c, t, 1360, 1060, 1.0, "diego", poses=((0, "stand"), (w("duzentos", O2 + 77.9), "thumb")), exprs=((0, "happy"),), look=-0.4)
    entra(c, t, w("dez", O2 + 74.9), 1360, 220, cartao("GANHA R$ 10 MIL", "aumento de R$ 1.000", w_=500, col=NAVY, size=48), anim="drop")
    entra(c, t, w("cinco", O2 + 77), 560, 220, cartao("GANHA R$ 5 MIL", "aumento de R$ 1.000", w_=500, col=NAVY, size=48), anim="drop")
    entra(c, t, w("dez", O2 + 74.9), 1360, 390, N("+ R$ 725", 90, VERDE, (1, 1, 1)))
    entra(c, t, w("cinco", O2 + 77), 560, 390, N("+ R$ 475", 90, VERMELHO, (1, 1, 1)))
    entra(c, t, w("duzentos", O2 + 77.9), 960, 540, cartao("R$ 250 A MAIS, TODO MÊS", w_=700, col=VERDE, size=54), anim="stamp")


def s22(c, t):  # o imposto cresce mais rápido nessa faixa
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 250, 1050, 0.95, poses=((0, "finger_up"), (w("cresce", O2 + 91.5), "point_r")), exprs=((0, "confident"),), look=0.7)
    titulo(c, t, w("não", O2 + 81.4), "IMPOSTO DE RENDA POR MÊS", 110, 70)
    smin, smax = 3000.0, 11000.0
    irmax = ir(smax)
    f = lambda k: ir(smin + (smax - smin) * k) / irmax
    k5, k7 = (5000 - smin) / (smax - smin), (7350 - smin) / (smax - smin)
    x0, yb, gw, gh = 560, 900, 1180, 600
    grafico_curva(c, t, w("dez", O2 + 84.4), x0, yb, gw, gh, f=f, d=2.4, cor=NAVY, eixo_x=("R$ 3 mil", "R$ 11 mil"),
                  marcas=((k5, "R$ 5 mil"), (k7, "R$ 7.350")), valor_fim=None)
    if t >= w("cresce", O2 + 91.5):
        p = ease_out(prog(t, w("cresce", O2 + 91.5), 0.5))
        c.rectangle(x0 + gw * k5, yb - gh - 30, gw * (k7 - k5), gh + 30); rgb(c, VERMELHO, 0.16 * p); c.fill()
        numero_i(c, "CRESCE MAIS RÁPIDO", x0 + gw * (k5 + k7) / 2, yb - gh + 30, 36, VERMELHO, contorno=(1, 1, 1), alpha=p)
    if t >= w("dez", O2 + 84.4) + 2.4:
        txt(c, "quem ganha mais paga mais no total", x0 + gw, yb + 75, 32, (0.4, 0.4, 0.45), HAND, "r")
    entra(c, t, w("isenção", O2 + 96.6), 960, 1010, N("o preço de sair da isenção", 46, GOLD, TINTA), anim="fade")


def s23(c, t):  # mito: aumento faz ganhar menos?
    cena_sala(c, t, "tarde")
    pessoa(c, t, 1200, 1060, 1.05, "lucas", poses=((0, "think"),), exprs=((0, "worried"),), look=-0.5)
    consultor_i(c, t, 380, 1060, 1.05, poses=((0, "stand"), (w("tem", O2 + 107.8), "think")), exprs=((0, "think"),), look=0.6)
    entra(c, t, w("será", O2 + 104.8), 1200, 330, lambda c: (thought(c, 640, 230, 0, 0),
                                                            text(c, "E SE EU GANHAR MENOS?", 0, 10, 50, MARKER, NAVY)), anim="pop")
    entra(c, t, w("recusa", O2 + 108.4), 760, 620, cartao("medo de mudar de faixa", w_=560, col=VERMELHO, size=44), anim="up")


def s24(c, t):  # a resposta é não: 5.000 x 5.001
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 300, 1040, 1.05, poses=((0, "finger_up"), (w("líquido", O2 + 127.5), "thumb")), exprs=((0, "confident"), (w("líquido", O2 + 127.5), "grin")), look=0.7)
    entra(c, t, w("não", O2 + 113.5), 1150, 150, N("NÃO!", 110, VERMELHO, (1, 1, 1)), anim="stamp")
    entra(c, t, w("limite", O2 + 116.8), 1150, 290, N("TESTANDO NO LIMITE", 50, NAVY, (1, 1, 1)), anim="fade")
    entra(c, t, w("com", O2 + 117.6), 880, 520, cartao("R$ 5.000", "imposto: R$ 0,00", w_=440, col=NAVY, size=62), anim="up")
    entra(c, t, w("com", O2 + 120.3), 1420, 520, cartao("R$ 5.001", "imposto: R$ 0,35", w_=440, col=NAVY, size=62), anim="up")
    entra(c, t, w("um", O2 + 124), 1150, 720, N("+ R$ 1 DE AUMENTO = R$ 0,35 DE IR", 48, GOLD), anim="pop")
    entra(c, t, w("líquido", O2 + 127.5), 1150, 860, N("LÍQUIDO: R$ 4.498,49 > R$ 4.499,00", 46, VERDE, (1, 1, 1)), anim="pop")


def s25(c, t):  # não tem degrau
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 250, 1050, 0.95, poses=((0, "point_r"),), exprs=((0, "confident"),), look=0.7)
    titulo(c, t, w("isso", O2 + 129.4), "SALÁRIO LÍQUIDO x BRUTO", 110, 70)
    smin, smax = 3000.0, 11000.0
    liq = lambda s: s - inss(s) - ir(s)
    lmin, lmax = liq(smin), liq(smax)
    f = lambda k: (liq(smin + (smax - smin) * k) - lmin) / (lmax - lmin)
    grafico_curva(c, t, w("isso", O2 + 129.4) + 0.4, 560, 860, 1180, 560, f=f, d=2.6, cor=VERDE, eixo_x=("bruto R$ 3 mil", "R$ 11 mil"),
                  marcas=(((5000 - smin) / (smax - smin), "R$ 5 mil"), ((7350 - smin) / (smax - smin), "R$ 7.350")))
    entra(c, t, w("degrau", O2 + 138), 820, 320, cartao("NÃO TEM DEGRAU", w_=520, col=VERDE, size=56), anim="stamp")
    entra(c, t, w("alíquota", O2 + 142.9), 1150, 990, N("a alíquota maior só vale pra parte que passa da faixa", 36, NAVY, (1, 1, 1)), anim="fade")


def s26(c, t):  # testei real por real
    fundo_marca(c, t, "verde", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "present"), (w("sempre", O2 + 161.2), "arms_up")), exprs=((0, "confident"), (w("sempre", O2 + 161.2), "grin")), look=0.7, prop=("r", prop_calc_i))
    titulo(c, t, w("eu", O2 + 149.3), "REAL POR REAL", 120, 90, GOLD, TINTA)
    contador(c, t, w("mil", O2 + 151.5), 1600, 20000, 1180, 330, 120, d=2.4, col=CREME_T)
    entra(c, t, w("nenhum", O2 + 154.5), 1180, 560, cartao("O LÍQUIDO CAIU: 0 VEZES", w_=760, col=VERDE, size=60), anim="stamp")
    entra(c, t, w("pouco", O2 + 159), 1180, 740, N("pode render pouco...", 60, CREME_T, dk(VERDE, 0.4)), anim="fade")
    entra(c, t, w("sempre", O2 + 161.2), 1180, 880, N("MAS SEMPRE SOBE", 84, GOLD, TINTA), anim="stamp")


def s27(c, t):  # fique tranquilo: a pergunta certa
    cena_escritorio(c, t, "crepusculo")
    pessoa(c, t, 1400, 1060, 1.05, "lucas", poses=((0, "stand"), (w("aumento", O2 + 167.6), "thumb")), exprs=((0, "neutral"), (w("aumento", O2 + 167.6), "happy")), look=-0.5)
    consultor_i(c, t, 360, 1060, 1.05, poses=((0, "present"),), exprs=((0, "happy"),), look=0.6)
    entra(c, t, w("aumento", O2 + 167.6), 900, 300, cartao("AUMENTO SEMPRE DEIXA MAIS NO BOLSO", w_=900, col=VERDE, size=46), anim="drop")
    entra(c, t, w("pergunta", O2 + 170.8), 900, 500, cartao("A PERGUNTA CERTA:", "quanto chega de verdade?", w_=700, col=NAVY, size=54), anim="up")


# ================================================================ BLOCO 3
def s28(c, t):  # o ano inteiro: 13º, férias, FGTS
    cena_sala(c, t, "dia")
    pessoa(c, t, 1550, 1060, 1.0, "lucas", poses=((0, "think"),), exprs=((0, "think"),), look=-0.6)
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "present"),), exprs=((0, "confident"),), look=0.6)
    entra(c, t, w("ano", O3 + 5.9), 950, 230, N("E NO ANO INTEIRO?", 84, GOLD), anim="pop")
    for i, (pal, aft, s_) in enumerate((("décimo", O3 + 9.2, "13º SALÁRIO"), ("férias", O3 + 10.6, "FÉRIAS + 1/3"), ("fgts", O3 + 11.3, "FGTS"))):
        entra(c, t, w(pal, aft), 950, 420 + i * 150, cartao(s_, w_=480, col=NAVY, size=56), anim="left")


def s29(c, t):  # no papel: 13.333
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 300, 1040, 1.05, poses=((0, "present"),), exprs=((0, "neutral"),), look=0.7)
    titulo(c, t, w("no", O3 + 12.6), "NO PAPEL", 120, 96)
    contador(c, t, w("treze", O3 + 14.6), 0, 13333, 1150, 370, 150, d=1.8, col=GOLD, sufixo=" /ano")
    entra(c, t, w("doze", O3 + 18.3), 1150, 600, N("12 SALÁRIOS + 13º + 1/3 DE FÉRIAS", 50, NAVY, (1, 1, 1)), anim="fade")
    entra(c, t, w("doze", O3 + 18.3), 1150, 760, N("(R$ 1.000 x 13,33)", 46, (0.4, 0.4, 0.45), (1, 1, 1)), anim="fade")


def s30(c, t):  # na prática: 6.439 + 1.067 FGTS
    fundo_marca(c, t, "navy", holofote=(330, 700))
    consultor_i(c, t, 330, 1040, 1.05, poses=((0, "point_r"), (w("pouco", O3 + 42.8), "shrug")), exprs=((0, "neutral"), (w("pouco", O3 + 42.8), "worried")), look=0.7)
    titulo(c, t, w("na", O3 + 22.6), "NA PRÁTICA (POR ANO)", 120, 76, GOLD, TINTA)
    t0b = w("prática", O3 + 22.6)
    barras_i(c, t, t0b, 680, 900, 1100, 520,
             (("NO PAPEL", 13333, GOLD), ("NO BOLSO", 6439, VERDE), ("+ FGTS", 7506, BLUE)), d=1.2, maxv=13333,
             intervalo=w("seis", O3 + 31) - t0b, size_val=56)
    entra(c, t, w("pouco", O3 + 42.8), 1230, 230, N("POUCO MAIS DA METADE", 50, CREME_T, NAVY), anim="stamp")


def s31(c, t):  # pra empresa custa mais
    cena_escritorio(c, t, "dia")
    pessoa(c, t, 1560, 1060, 1.0, "gerente", poses=((0, "present_l"),), exprs=((0, "neutral"),), look=-0.6)
    pessoa(c, t, 300, 1060, 1.0, "lucas", poses=((0, "stand"), (w("recebe", O3 + 63), "shrug")), exprs=((0, "neutral"), (w("recebe", O3 + 63), "worried")), look=0.6)
    entra(c, t, w("empresa", O3 + 46), 960, 200, N("PRA EMPRESA", 72, NAVY, (1, 1, 1)), anim="fade")
    entra(c, t, w("fgts", O3 + 50.6), 960, 330, cartao("+ R$ 80 de FGTS", w_=500, col=NAVY, size=46), anim="left")
    entra(c, t, w("vinte", O3 + 54.5), 960, 480, cartao("+ 20% de INSS patronal", "empresas fora do Simples", w_=500, col=NAVY, size=46), anim="left")
    entra(c, t, w("mil", O3 + 60.5), 900, 790, lambda c: etiqueta_preco(c, "EMPRESA: R$ 1.280+", VERMELHO, 46), anim="drop")
    entra(c, t, w("recebe", O3 + 63), 430, 660, lambda c: etiqueta_preco(c, "LUCAS: R$ 475", VERDE, 46), anim="drop")


def s32(c, t):  # declaração anual
    cena_sala(c, t, "noite")
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.6)
    entra(c, t, w("declaração", O3 + 66.4), 1100, 260, cartao("DECLARAÇÃO DO IR", "no ano seguinte, a conta é refeita", w_=760, col=NAVY, size=60), anim="drop")
    entra(c, t, w("oitenta", O3 + 72.8), 1100, 470, cartao("desconto até R$ 88.200 por ano", w_=760, col=dk(GOLD, 0.3), size=48), anim="left")
    entra(c, t, w("pagar", O3 + 76.6), 1100, 640, cartao("pode sobrar a pagar ou a receber", w_=760, col=(0.35, 0.35, 0.4), size=44), anim="left")
    entra(c, t, w("tamanho", O3 + 79), 1100, 820, N("O TAMANHO DA CONTA É ESSE", 54, GOLD), anim="pop")


def s33(c, t):  # três coisas
    fundo_marca(c, t, "navy", holofote=(960, 760))
    consultor_i(c, t, 960, 1050, 1.1, poses=((0, "present"),), exprs=((0, "confident"),), look=0.0)
    entra(c, t, w("então", O3 + 80.8), 960, 200, N("O QUE FAZER?", 96, GOLD, TINTA), anim="pop")
    entra(c, t, w("três", O3 + 83.6), 960, 380, N("3 ATITUDES", 80, CREME_T, NAVY), anim="stamp")


def s34(c, t):  # 1) planos pelo líquido: a parcela de 800
    cena_rua(c, t, "dia")
    pessoa(c, t, 640, 1060, 1.0, "lucas", poses=((0, "stand"), (w("tira", O3 + 98.4), "head")), exprs=((0, "neutral"), (w("tira", O3 + 98.4), "desperate")), look=0.6)
    consultor_i(c, t, 230, 1060, 0.95, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.6)
    entra(c, t, w("primeira", O3 + 84.9), 960, 150, cartao("1. PLANEJE PELO LÍQUIDO", w_=760, size=58), anim="drop")
    entra(c, t, w("carro", O3 + 90.6), 1420, 840, lambda c: carro_i(c, t, (0.20, 0.44, 0.74)), anim="right")
    entra(c, t, w("oitocentos", O3 + 90.9), 1300, 360, lambda c: etiqueta_preco(c, "PARCELA: R$ 800", VERMELHO, 46), anim="drop")
    entra(c, t, w("quatrocentos", O3 + 94.1), 1300, 500, lambda c: etiqueta_preco(c, "AUMENTO: R$ 475", VERDE, 46), anim="drop")
    entra(c, t, w("trezentos", O3 + 98.7), 1080, 640, N("FALTAM R$ 325", 66, VERMELHO, (1, 1, 1)), anim="stamp")


def s35(c, t):  # 2) compare o líquido: 20% x 10,6%
    fundo_marca(c, t, "creme")
    consultor_i(c, t, 300, 1040, 1.05, poses=((0, "present"), (w("bolso", O3 + 117.8), "point_r")), exprs=((0, "neutral"), (w("bolso", O3 + 117.8), "confident")), look=0.7)
    entra(c, t, w("segunda", O3 + 106.8), 1150, 150, cartao("2. COMPARE O LÍQUIDO", w_=760, size=58), anim="drop")
    entra(c, t, w("proposta", O3 + 113.2), 880, 400, cartao("PROPOSTA A", "R$ 5.000 bruto", w_=420, col=NAVY, size=52), anim="up")
    entra(c, t, w("seis", O3 + 113.9), 1420, 400, cartao("PROPOSTA B", "R$ 6.000 bruto", w_=420, col=NAVY, size=52), anim="up")
    entra(c, t, w("vinte", O3 + 115), 1150, 600, lambda c: etiqueta_preco(c, "PARECE +20%", GOLD, 54), anim="drop")
    entra(c, t, w("bolso", O3 + 117.8), 1150, 800, N("NO BOLSO: +10,6%", 84, VERDE, (1, 1, 1)), anim="stamp")


def s36(c, t):  # benefícios: vale-refeição e plano de saúde
    cena_padaria(c, t, "dia", cardapio=(("PF", "R$ 28"), ("SUCO", "R$ 9")))
    consultor_i(c, t, 330, 1060, 1.05, poses=((0, "present"),), exprs=((0, "confident"),), look=0.6)
    entra(c, t, w("pacote", O3 + 121), 1150, 200, cartao("OLHE O PACOTE INTEIRO", w_=720, size=54), anim="drop")
    entra(c, t, w("vale-refeição", O3 + 123), 760, 400, lambda c: etiqueta_preco(c, "VALE-REFEIÇÃO", GOLD, 48), anim="drop")
    entra(c, t, w("plano", O3 + 124.2), 760, 540, lambda c: etiqueta_preco(c, "PLANO DE SAÚDE", GOLD, 48), anim="drop")
    entra(c, t, w("pagam", O3 + 127.7), 1350, 760, cartao("SEM INSS", "e sem IR (em geral)", w_=360, col=VERDE, size=52), anim="stamp")


def s37(c, t):  # 3) guarde o aumento: 5.699 em um ano
    fundo_marca(c, t, "verde", holofote=(380, 700))
    consultor_i(c, t, 380, 1040, 1.1, poses=((0, "present"), (w("reserva", O3 + 149.4), "arms_up")), exprs=((0, "confident"), (w("reserva", O3 + 149.4), "grin")), look=0.7, prop=("r", prop_moeda_i))
    entra(c, t, w("terceira", O3 + 134.7), 1180, 150, cartao("3. NÃO DEIXE O AUMENTO SUMIR", w_=860, size=54), anim="drop")
    entra(c, t, w("quatrocentos", O3 + 138.2), 1180, 300, N("R$ 475 POR MÊS", 66, CREME_T, dk(VERDE, 0.4)), anim="fade")
    contador(c, t, w("quase", O3 + 145.2), 0, 5699, 1180, 470, 140, d=1.8, col=GOLD, sufixo=" em 1 ano")
    for i, n in enumerate((6, 9, 12)):
        c.save(); c.translate(980 + i * 200, 860); pilha_moedas(c, n, 50, t, w("guardados", O3 + 142.7) + i * 0.4, 0.09); c.restore()
    entra(c, t, w("reserva", O3 + 149.4), 1180, 640, N("RESERVA DE EMERGÊNCIA", 52, CREME_T, dk(VERDE, 0.4)), anim="pop")


def s38(c, t):  # resumindo
    fundo_marca(c, t, "navy", holofote=(330, 700))
    consultor_i(c, t, 330, 1040, 1.05, poses=((0, "present"), (w("antes", 529), "finger_up")), exprs=((0, "confident"),), look=0.7)
    titulo(c, t, w("resumindo", O3 + 154.7), "RESUMINDO", 110, 90, GOLD, TINTA)
    regua(c, t, w("quem", O3 + 156.9), 620, 360, 1180, destaque=w("faixa", O3 + 162.2))
    entra(c, t, w("cada", O3 + 164.5), 1210, 610, cartao("DE CADA R$ 100 A MAIS, FICAM R$ 49", w_=960, col=VERMELHO, size=48), anim="left")
    entra(c, t, w("líquido", O3 + 170.5), 1210, 760, cartao("O LÍQUIDO SEMPRE SOBE", w_=960, col=VERDE, size=52), anim="left")
    entra(c, t, w("conta", O3 + 173.6), 1210, 910, N("FAÇA A CONTA ANTES DE GASTAR", 58, GOLD, TINTA), anim="stamp")


def s39(c, t):  # comenta aí
    cena_escritorio(c, t, "crepusculo")
    pessoa(c, t, 1550, 1060, 1.0, "lucas", poses=((0, "stand"),), exprs=((0, "happy"),), look=-0.5)
    consultor_i(c, t, 360, 1060, 1.08, poses=((0, "present"), (w("like", O3 + 184), "wave")), exprs=((0, "happy"),), look=0.6)
    entra(c, t, w("você", O3 + 175.5), 960, 260, cartao("QUANTO DO SEU ÚLTIMO AUMENTO", "chegou de verdade? conta nos comentários", w_=1000, col=NAVY, size=54), anim="drop")
    entra(c, t, w("like", O3 + 184), 960, 470, N("INSCREVA-SE NO FAZ A CONTA", 58, GOLD), anim="pop")
    entra(c, t, O3 + 176, 960, 1020, lambda c: txt(c, "conteúdo educativo, não é recomendação financeira", 0, 0, 32, (1, 1, 1)), anim="fade")


def s40(c, t):  # Tela final (5 s sem narração)
    tela_final_i(c, t, END)


SCENES = [
    (0.0, 9.84, s01), (9.84, 15.28, s02), (15.28, 23.76, s03), (23.76, 35.96, s04), (35.96, 47.6, s05),
    (47.6, 57.44, s06), (57.44, 68.96, s07), (68.96, 85.88, s08), (85.88, 97.48, s09), (97.48, 115.24, s10),
    (115.24, 125.84, s11), (125.84, 140.92, s12), (140.92, 149.56, s13), (149.56, 164.83, s14), (164.83, O2, s15),
    (O2, 189.96, s16), (189.96, 205.12, s17), (205.12, 217.84, s18), (217.84, 229.96, s19), (229.96, 249.97, s20),
    (249.97, 261.08, s21), (261.08, 281.88, s22), (281.88, 292.04, s23), (292.04, 309.09, s24), (309.09, 328.93, s25),
    (328.93, 341.87, s26), (341.87, O3, s27),
    (O3, 368.23, s28), (368.23, 378.23, s29), (378.23, 401.67, s30), (401.67, 421.07, s31), (421.07, 436.51, s32),
    (436.51, 440.55, s33), (440.55, 462.43, s34), (462.43, 476.27, s35), (476.27, 490.35, s36), (490.35, 510.35, s37),
    (510.35, 531.0, s38), (531.0, END, s39), (END, 999.0, s40),
]

# só toques pontuais, sem ruído: 474,90 / o tombo / + 725 / sempre sobe
SFX = [(w("quatrocentos", 38), "tum"), (w("tombo", O2 + 26), "tum"), (w("setecentos", O2 + 56), "soft_ding"),
       (w("sempre", O2 + 161.2), "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")
