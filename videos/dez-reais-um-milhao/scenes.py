"""R$ 10 por dia vira R$ 1 milhão? A conta completa (Faz a Conta, vídeo longo 16:9).
Narração Calm Carlos (HeyGen, ElevenLabs v4), 3 blocos, 0,4 s entre blocos.
Tempos absolutos: bloco1 0,000 | bloco2 158,049 | bloco3 334,906 | fim da fala 536,180 | +5 s de tela final.
Premissas (01/11/2026): R$ 300 por mês (R$ 10 x 30 dias) no fim de cada mês, 0,8% a.m. líquido (~10,03% a.a.),
inflação de 4% a.a. (IPCA 12 meses até set/2026: 4,58%; meta 3%), Selic 13,75% (Copom 16/09/2026), CDB 100% CDI
líquido ~11,6% a.a., poupança 0,5% + TR (~0,167%) = 8,32% a.a. Contas em contas.py."""
import json
import math
import os

from engine import *  # noqa

O2, O3 = 158.049, 334.906
END = 536.180

_PAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras.json"), encoding="utf-8"))


def w(word, after=0.0, d=0.0):
    """início (s) da primeira palavra que começa com `word` depois de `after` (tempo absoluto), mais d"""
    word = word.lower()
    for p in _PAL:
        if p["t0"] >= after - 0.01 and p["w"].lower().strip(",.:?!\"").startswith(word):
            return p["t0"] + d
    raise KeyError((word, after))


PINKISH = (1, 0.8, 0.76)
ANAC = PURPLE
BRUC = BLUE
R = 0.008
P = 300.0


def fv(m, p=P, r=R):
    return p * ((1 + r) ** m - 1) / r


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def row(label, val, vcol=INK, wd=760, size=54):
    """linha de extrato: rótulo à esquerda, valor à direita (centrada em 0)"""
    def f(c):
        text(c, label, -wd / 2, 0, size, HAND, DGRAY, align="l")
        text(c, val, wd / 2, 0, size + 4, MARKER, vcol, align="r")
    return f


def tag(s, col, size=54):
    def f(c):
        wd = text_w(c, s, size) + 44
        rrect(c, -wd / 2, -size * 0.7, wd, size * 1.4, 14); fs(c, col, 5)
        text(c, s, 0, 2, size, MARKER, WHITE)
    return f


def panel(wd, h, col=WHITE, lw=5):
    def f(c):
        rrect(c, -wd / 2, -h / 2, wd, h, 22); fs(c, col, lw)
    return f


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def step(c, t, t0, num, head, col=LYELLOW):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"{num}. {head}", 0, 0, 70, col), anim="stamp")


def detalhe(c, t, t0, num, head, col=LYELLOW):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"Detalhe {num}: {head}", 0, 0, 70, col), anim="stamp")


def money_bar(c, t, t0, x, base, h, wd, col, top, label, d=0.9, tsize=56, lsize=42, tcol=None):
    k = grow(t, t0, d)
    if t < t0:
        return
    c.save(); c.translate(x, base)
    bar(c, max(4, h * k), wd, col)
    c.restore()
    if k > 0.6:
        if top:
            text(c, top, x, base - h * k - 42, tsize, MARKER, tcol or col)
        if label:
            text(c, label, x, base + 46, lsize, HAND, DGRAY)


def ana(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", ANAC); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def bruno(c, t, x, y, s, poses, exprs, **kw):
    other(c, t, x, y, s, poses, exprs, **kw)


def coffee(c):
    """xícara de café com pão de queijo"""
    rrect(c, -60, -40, 110, 100, 18); fs(c, WHITE, 6)
    c.new_sub_path(); c.arc(58, 8, 26, -math.pi / 2, math.pi / 2); rgb(c, INK); c.set_line_width(8); c.stroke()
    ellipse(c, -5, -40, 55, 12); fs(c, (0.45, 0.28, 0.15), 5)
    circle(c, 110, 50, 30, (0.98, 0.85, 0.5), 5)
    circle(c, 150, 55, 24, (0.98, 0.85, 0.5), 5)


def pin(c):
    """marcador de corrida de aplicativo (pino de mapa)"""
    c.move_to(0, 70)
    c.curve_to(-70, -10, -60, -90, 0, -90)
    c.curve_to(60, -90, 70, -10, 0, 70)
    fs(c, NAVY, 6)
    circle(c, 0, -35, 24, WHITE, 5)


# ---------------------------------------------------------------- gráfico da curva (cenas 7 a 9)
GX0, GX1, GY0, GY1 = 200, 1120, 960, 330
VMAX = fv(420)


def gx(m):
    return GX0 + (GX1 - GX0) * m / 420


def gy(v):
    return GY0 - (GY0 - GY1) * v / VMAX


CURVE_KEYS = [(77.3, 0), (81.4, 60), (92.8, 60), (93.6, 120), (98.2, 120), (99.1, 240), (101.5, 240), (102.4, 360),
              (105.2, 360), (106.7, 420)]


def curve_month(t):
    if t <= CURVE_KEYS[0][0]:
        return 0
    for (t0, m0), (t1, m1) in zip(CURVE_KEYS, CURVE_KEYS[1:]):
        if t <= t1:
            return m0 + (m1 - m0) * ease_io((t - t0) / (t1 - t0)) if t1 > t0 else m1
    return 420


def axes(c):
    line(c, GX0, GY0, GX1 + 40, GY0, 6)
    line(c, GX0, GY0, GX0, GY1 - 40, 6)
    for m, lab in ((60, "5"), (120, "10"), (240, "20"), (360, "30"), (420, "35")):
        line(c, gx(m), GY0 - 10, gx(m), GY0 + 10, 5)
        text(c, lab, gx(m), GY0 + 45, 44, MARKER, DGRAY)
    text(c, "anos", GX0 - 10, GY0 + 45, 40, HAND, DGRAY, align="r")


def draw_curve(c, m0, m1, col=GREEN, lw=11):
    if m1 - m0 <= 0:
        return
    n = max(2, int((m1 - m0) / 3))
    c.move_to(gx(m0), gy(fv(m0)))
    for i in range(1, n + 1):
        m = m0 + (m1 - m0) * i / n
        c.line_to(gx(m), gy(fv(m)))
    rgb(c, col); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1); c.stroke()


def chart(c, t, title_t=None):
    if title_t is not None:
        show(c, t, title_t, 660, 150, M("R$ 300 por mês, todo mês", 62, NAVY), anim="up")
    axes(c)
    m = curve_month(t)
    draw_curve(c, 0, m)
    if 0 < m < 420:
        circle(c, gx(m), gy(fv(m)), 14, GREEN, 5)


def point_label(c, t, t0, m, s, size=52, dx=-30, dy=-70, col=INK):
    show(c, t, t0, gx(m) + dx, gy(fv(m)) + dy, M(s, size, col), anim="pop")


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 9.2  R$ 10 por dia: lanche, café, corrida
    show(c, t, 0.05, 820, 170, lambda c: hl(c, "R$ 10 por dia", 0, 0, 110, LYELLOW), anim="stamp", d=0.35)
    show(c, t, w("lanche"), 330, 560, group(sc(sandwich, s=1.15), at(0, 170, T("um lanche", 50, DGRAY))), anim="pop")
    show(c, t, w("café"), 790, 560, group(sc(coffee, s=1.2), at(30, 170, T("um café", 50, DGRAY))), anim="pop")
    show(c, t, w("corrida"), 1240, 560, group(sc(pin, s=1.0), at(0, 170, T("uma corrida", 50, DGRAY))), anim="pop")
    show(c, t, w("quase", 5.0), 790, 900, T("quase todo mundo gasta sem perceber", 56, RED), anim="up")
    hero(c, t, 1690, 1050, 0.95, [(0, "present_l"), (w("quase", 5.0), "shrug")], [(0, "neutral"), (w("quase", 5.0), "think")],
         appear=0.05, look=-1)


def s02(c, t):  # 9.2 - 16.8  e se guardasse todo dia? vira um milhão? Viram.
    show(c, t, 9.3, 560, 520, sc(piggy, s=1.4), anim="drop")
    for i in range(4):
        show(c, t, w("guardados") + i * 0.35, 560, 300, sc(coin, s=0.6), anim="drop", t1=w("guardados") + i * 0.35 + 0.45)
    show(c, t, w("guardados"), 560, 760, T("todo dia", 56, DGRAY), anim="fade")
    show(c, t, w("milhão", 13.0), 1180, 380, M("R$ 1 MILHÃO?", 104, GREEN), anim="stamp")
    show(c, t, w("viram", 16.0), 1180, 560, lambda c: hl(c, "VIRAM.", 0, 0, 96, LGREEN, GREEN), anim="stamp")
    hero(c, t, 1640, 1050, 0.95, [(0, "think"), (16.3, "thumb")], [(0, "think"), (16.3, "confident")], appear=9.3, look=-1)


def s03(c, t):  # 16.8 - 37.6  três detalhes: inflação, tempo, Ana x Bruno
    show(c, t, 16.9, 760, 130, M("3 detalhes que quase ninguém conta", 66, NAVY), anim="up")
    t1 = w("inflação", 21.0)
    t2 = w("tempo", 25.0)
    t3 = w("terceiro", 29.0)
    show(c, t, t1, 300, 470, sc(cart, s=0.9), anim="pop")
    show(c, t, t1 + 0.2, 300, 650, M("1. inflação", 56, RED), anim="fade")
    show(c, t, t1 + 1.6, 300, 730, T("come o milhão", 46, DGRAY), anim="fade")
    show(c, t, t2, 720, 470, lambda c: clock(c, t), anim="pop")
    show(c, t, t2 + 0.2, 720, 650, M("2. tempo", 56, NAVY), anim="fade")
    show(c, t, t2 + 1.4, 720, 730, T("pesa mais que o valor", 46, DGRAY), anim="fade")
    ana(c, t, 1080, 590, 0.5, [(0, "wave")], [(0, "happy")], appear=w("ana", 32.0))
    bruno(c, t, 1260, 590, 0.5, [(0, "stand")], [(0, "neutral")], appear=w("bruno", 33.0))
    show(c, t, w("ana", 32.0), 1170, 700 - 50, M("3. Ana x Bruno", 56, PURPLE), anim="fade")
    show(c, t, w("errado", 35.0), 1170, 760, T("parece errado...", 46, DGRAY), anim="fade")
    show(c, t, w("não", 36.8), 1170, 840, M("mas não é", 52, GREEN), anim="pop")
    hero(c, t, 1690, 1050, 0.85, [(0, "finger_up"), (t2, "present_l"), (t3, "point_l")], [(0, "confident"), (t3, "happy")],
         appear=16.9, look=-1)


def s04(c, t):  # 37.6 - 43.8  a conta completa, do jeito honesto; regras do jogo
    show(c, t, 37.7, 820, 330, M("a conta completa", 100, NAVY), anim="stamp")
    show(c, t, w("honesto"), 820, 480, lambda c: hl(c, "do jeito honesto", 0, 0, 72, LYELLOW), anim="stamp")
    show(c, t, w("regras", 41.0), 820, 700, sc(clipboard, "REGRAS", 3, False, s=0.9), anim="pop")
    hero(c, t, 1600, 1050, 1.0, [(0, "present_l"), (w("regras", 41.0), "point_l")], [(0, "confident")], appear=37.7,
         look=-1, prop=("r", prop_calculator))


def s05(c, t):  # 43.8 - 57.3  R$ 10 x 30 = R$ 300/mês; 0,8% a.m. líquido = ~10% a.a.
    show(c, t, 43.9, 760, 170, M("R$ 10 x 30 dias", 86, NAVY), anim="up")
    show(c, t, w("trezentos", 44.5), 760, 310, lambda c: hl(c, "= R$ 300 por mês", 0, 0, 84, LGREEN), anim="stamp")
    show(c, t, w("investimento", 47.5), 300, 640, sc(bank, s=0.9), anim="pop")
    show(c, t, w("renda", 49.0), 300, 820, T("renda fixa", 52, DGRAY), anim="fade")
    show(c, t, w("zero", 50.5), 860, 560, lambda c: hl(c, "0,8% ao mês", 0, 0, 84, LYELLOW), anim="stamp")
    show(c, t, w("descontado", 52.8), 860, 680, T("já sem o imposto de renda", 52, DGRAY), anim="up")
    show(c, t, w("dez", 55.5), 860, 830, M("uns 10% ao ano", 76, GREEN), anim="pop")
    hero(c, t, 1640, 1050, 0.95, [(0, "relax"), (w("trezentos", 44.5), "thumb"), (w("zero", 50.5), "present_l")],
         [(0, "neutral"), (w("trezentos", 44.5), "happy")], appear=43.9, look=-1, prop=("r", prop_calculator))


def s06(c, t):  # 57.3 - 76.3  por que 10%? Selic 13,75%, CDB 100% CDI ~11,5% líquido; juro alto não dura 35 anos
    show(c, t, 57.4, 760, 130, M("Por que 10%?", 76, NAVY), anim="up")
    show(c, t, w("selic", 59.5), 470, 330, T("Selic hoje", 52, DGRAY), anim="fade")
    show(c, t, w("treze", 60.5), 470, 430, M("13,75%", 96, NAVY), anim="stamp")
    show(c, t, w("cdb", 63.0), 1050, 330, T("CDB 100% do CDI, sem IR", 50, DGRAY), anim="fade")
    show(c, t, w("onze", 66.5), 1050, 430, M("~11,5% ao ano", 84, GREEN), anim="stamp")
    show(c, t, w("juro", 70.5), 760, 610, T("juro alto assim não dura 35 anos", 56, RED), anim="up")
    show(c, t, w("pé", 75.4), 760, 780, lambda c: hl(c, "na conta: 10% ao ano", 0, 0, 72, LYELLOW), anim="stamp")
    show(c, t, w("pé", 75.4, 0.3), 760, 890, T("(um número pé no chão)", 46, DGRAY), anim="fade")
    hero(c, t, 1660, 1050, 0.95, [(0, "think"), (w("selic", 59.5), "present_l"), (w("juro", 70.5), "shrug"),
                                  (w("pé", 75.4), "thumb")],
         [(0, "think"), (w("selic", 59.5), "neutral"), (w("juro", 70.5), "worried"), (w("pé", 75.4), "confident")],
         appear=57.4, look=-1)


def s07(c, t):  # 76.3 - 92.6  5 anos: R$ 23 mil (bolso 18 mil, juros 5 mil); aqui a maioria desiste
    chart(c, t, 76.4)
    point_label(c, t, w("vinte", 82.5), 60, "R$ 23 mil", 54, dx=40, dy=-80)
    show(c, t, w("saíram", 84.5), 1420, 330, row("do bolso", "R$ 18 mil", NAVY, wd=520, size=48), anim="left")
    show(c, t, w("juros", 87.0), 1420, 420, row("juros", "R$ 5 mil", GREEN, wd=520, size=48), anim="left")
    show(c, t, w("maioria", 91.0), 1420, 560, lambda c: hl(c, "a maioria desiste aqui", 0, 0, 52, PINKISH, RED), anim="stamp")
    hero(c, t, 1640, 1050, 0.62, [(0, "present_l"), (w("pouco", 89.6), "shrug")], [(0, "neutral"), (w("pouco", 89.6), "sad")],
         appear=76.4, look=-1)


def s08(c, t):  # 92.6 - 116.9  10, 20, 30, 35 anos: R$ 1,03 milhão; a curva dispara
    chart(c, t, None)
    show(c, t, 92.7, 660, 150, M("R$ 300 por mês, todo mês", 62, NAVY), anim="fade", d=0.2)
    point_label(c, t, w("sessenta", 93.5), 120, "R$ 60 mil", 50, dx=10, dy=-75)
    show(c, t, w("trinta", 96.5), 1450, 330, row("do bolso (10 anos)", "R$ 36 mil", NAVY, wd=560, size=44), anim="left",
         t1=w("vinte", 98.2))
    point_label(c, t, w("duzentos", 99.2), 240, "R$ 216 mil", 54, dx=-170, dy=-60)
    point_label(c, t, w("seiscentos", 102.6), 360, "R$ 623 mil", 58, dx=-200, dy=-40)
    show(c, t, w("milhão", 106.8), 760, 260, lambda c: hl(c, "R$ 1,03 MILHÃO", 0, 0, 90, LGREEN), anim="stamp")
    show(c, t, w("chão", 114.2), 470, 640, T("quase não sai do chão", 48, DGRAY), anim="fade")
    show(c, t, w("dispara", 115.8), 1250, 480, M("dispara!", 64, GREEN), anim="stamp")
    hero(c, t, 1640, 1050, 0.62, [(0, "present_l"), (w("milhão", 106.8), "arms_up"), (w("repara", 109.6), "point_l")],
         [(0, "neutral"), (w("milhão", 106.8), "grin"), (w("repara", 109.6), "happy")], appear=92.7, look=-1)


def s09(c, t):  # 116.9 - 128.7  os últimos 5 anos colocaram R$ 405 mil: mais que os primeiros 25 juntos
    show(c, t, 117.0, 660, 150, M("Só os últimos 5 anos...", 62, NAVY), anim="up")
    axes(c)
    k = grow(t, w("colocaram", 120.8), 1.2)
    draw_curve(c, 0, 300, col=LGRAY if t > w("primeiros", 125.4) else GREEN)
    draw_curve(c, 300, 360)
    draw_curve(c, 360, 360 + 60 * k, col=GOLD, lw=16)
    if t > w("primeiros", 125.4):
        draw_curve(c, 0, 300, col=BLUE, lw=11)
    show(c, t, w("quatrocentos", 121.5), 760, 300, lambda c: hl(c, "+ R$ 405 mil", 0, 0, 84, LYELLOW, GOLD), anim="stamp")
    show(c, t, w("quatrocentos", 121.5, 0.2), 760, 400, T("do ano 30 ao 35", 48, DGRAY), anim="fade")
    show(c, t, w("primeiros", 125.4), 620, 560, M("primeiros 25 anos: R$ 372 mil", 46, BLUE), anim="up")
    hero(c, t, 1600, 1050, 0.9, [(0, "point_l"), (w("quatrocentos", 121.5), "arms_up"), (w("primeiros", 125.4), "present_l")],
         [(0, "happy"), (w("quatrocentos", 121.5), "shocked"), (w("primeiros", 125.4), "grin")], appear=117.0, look=-1)


def s10(c, t):  # 128.7 - 135.4  perto do fim: + de R$ 8 mil por mês sozinho
    show(c, t, 128.8, 800, 160, T("perto do fim, esse dinheiro rende", 60, DGRAY), anim="up")
    show(c, t, w("oito", 131.2), 800, 330, lambda c: hl(c, "+ de R$ 8 mil por mês", 0, 0, 92, LGREEN, GREEN), anim="stamp")
    show(c, t, w("sozinho", 132.9), 800, 470, M("sozinho", 70, NAVY), anim="pop")
    show(c, t, 128.9, 640, 900, sc(beach_chair, s=0.95), anim="pop")
    hero(c, t, 1350, 1050, 1.0, [(0, "relax"), (w("nada", 134.7), "thumb")], [(0, "happy"), (w("nada", 134.7), "grin")],
         appear=128.8, look=-1)


def s11(c, t):  # 135.4 - 151.6  do bolso: R$ 126 mil; juros: R$ 898 mil = quase 90% (cena do gancho "milhao-bolso")
    show(c, t, 135.5, 760, 120, M("De onde veio esse milhão?", 66, NAVY), anim="up")
    k = grow(t, w("oitocentos", 145.4), 1.4)
    show(c, t, w("bolso", 140.4), 600, 560, lambda c: donut(c, 0.123, r=230, lw=90, col=NAVY), anim="pop")
    if t > w("oitocentos", 145.4):
        c.save(); c.translate(600, 560)
        c.new_sub_path()
        c.arc(0, 0, 230, -math.pi / 2 + 2 * math.pi * 0.123, -math.pi / 2 + 2 * math.pi * (0.123 + 0.877 * k))
        rgb(c, GREEN); c.set_line_width(90); c.set_line_cap(0); c.stroke(); c.set_line_cap(1)
        for rr in (230 - 45, 230 + 45):
            c.new_sub_path(); c.arc(0, 0, rr, 0, 2 * math.pi); rgb(c, INK); c.set_line_width(6); c.stroke()
        c.restore()
    show(c, t, w("isso", 143.7), 600, 560, M("R$ 1 mi", 64, INK), anim="fade")
    show(c, t, w("cento", 141.3), 1250, 380, row("do seu bolso", "R$ 126 mil", NAVY, wd=560, size=52), anim="left")
    show(c, t, w("oitocentos", 145.4), 1250, 500, row("juros", "R$ 898 mil", GREEN, wd=560, size=52), anim="left")
    show(c, t, w("noventa", 149.7), 1220, 640, lambda c: hl(c, "quase 90% são juros", 0, 0, 64, LGREEN, GREEN), anim="stamp")
    hero(c, t, 1720, 1050, 0.62, [(0, "think"), (w("cento", 141.3), "point_l"), (w("oitocentos", 145.4), "arms_up")],
         [(0, "think"), (w("cento", 141.3), "neutral"), (w("oitocentos", 145.4), "shocked")], appear=135.5, look=-1)


def s12(c, t):  # 151.6 - O2  sim, vira um milhão... mas agora vêm os três detalhes
    show(c, t, 151.7, 760, 330, lambda c: hl(c, "R$ 10 por dia = R$ 1 milhão", 0, 0, 84, LGREEN), anim="stamp")
    show(c, t, w("mas", 155.3), 760, 560, M("mas...", 90, RED), anim="pop")
    show(c, t, w("três", 156.4), 520, 800, sc(cart, s=0.6), anim="pop")
    show(c, t, w("três", 156.4, 0.15), 760, 800, lambda c: clock(c, t), anim="pop")
    show(c, t, w("três", 156.4, 0.3), 1000, 800, sc(qmark, 140, PURPLE), anim="pop")
    hero(c, t, 1600, 1050, 0.95, [(0, "thumb"), (w("mas", 155.3), "finger_up")], [(0, "happy"), (w("mas", 155.3), "think")],
         appear=151.7, look=-1)


# ======================================================================= BLOCO 2
def s13(c, t):  # O2 - 166.3  detalhe 1: inflação; R$ 1 milhão daqui a 35 anos não compra o que compra hoje
    detalhe(c, t, O2 + 0.1, 1, "a inflação", PINKISH)
    show(c, t, w("daqui", 160.0), 520, 470, M("R$ 1 milhão", 80, GREEN), anim="pop")
    show(c, t, w("daqui", 160.0, 0.2), 520, 560, T("daqui a 35 anos", 48, DGRAY), anim="fade")
    show(c, t, w("comprar", 163.0), 900, 500, sc(neq, 70), anim="stamp")
    show(c, t, w("compra", 165.2), 1260, 470, M("R$ 1 milhão", 80, NAVY), anim="pop")
    show(c, t, w("hoje", 165.5), 1260, 560, T("de hoje", 48, DGRAY), anim="fade")
    show(c, t, w("comprar", 163.0), 900, 820, sc(cart, s=0.8), anim="pop")
    hero(c, t, 1720, 1050, 0.6, [(0, "present_l"), (w("comprar", 163.0), "shrug")], [(0, "neutral"), (w("comprar", 163.0), "worried")],
         appear=O2 + 0.1, look=-1)


def s14(c, t):  # 166.3 - 177.1  inflação de 4% ao ano (IPCA 12 meses 4,5%; meta 3%)
    show(c, t, 166.4, 760, 300, lambda c: hl(c, "inflação: 4% ao ano", 0, 0, 92, LYELLOW), anim="stamp")
    show(c, t, w("abaixo", 170.0), 470, 560, T("últimos 12 meses", 48, DGRAY), anim="fade")
    show(c, t, w("quatro", 170.7), 470, 650, M("4,58%", 84, RED), anim="pop")
    show(c, t, w("meta", 174.5), 1060, 560, T("meta do Banco Central", 48, DGRAY), anim="fade")
    show(c, t, w("três", 175.5), 1060, 650, M("3%", 84, NAVY), anim="pop")
    show(c, t, w("três", 175.5, 0.4), 760, 830, T("4% fica no meio do caminho", 52, DGRAY), anim="up")
    hero(c, t, 1660, 1050, 0.9, [(0, "present_l"), (w("três", 175.5), "thumb")], [(0, "neutral"), (w("três", 175.5), "confident")],
         appear=166.4, look=-1, prop=("r", prop_calculator))


def s15(c, t):  # 177.1 - 187.7  preços quase quadruplicam; lanche de R$ 10 vai custar ~R$ 39,50
    show(c, t, 177.2, 760, 130, M("Os preços quase quadruplicam", 70, NAVY), anim="up")
    show(c, t, w("quadruplicam", 178.0), 760, 480, M("x 4", 160, RED), anim="stamp", t1=w("aquele", 182.0))
    show(c, t, w("aquele", 182.0), 420, 560, sc(sandwich, s=1.2), anim="pop")
    show(c, t, w("dez", 182.6), 420, 760, sc(price_tag, "R$ 10", LYELLOW, 52, s=1.0), anim="pop")
    show(c, t, w("dez", 182.6, 0.1), 420, 880, T("hoje", 48, DGRAY), anim="fade")
    arrow_draw(c, t, w("custar", 183.5), 640, 600, 900, 600)
    show(c, t, w("custar", 183.5), 1140, 560, sc(sandwich, s=1.2), anim="pop")
    show(c, t, w("trinta", 184.0), 1140, 760, sc(price_tag, "R$ 39,50", PINKISH, 52, s=1.1), anim="stamp")
    show(c, t, w("trinta", 184.0, 0.1), 1140, 880, T("daqui a 35 anos", 48, DGRAY), anim="fade")
    hero(c, t, 1690, 1050, 0.85, [(0, "present_l"), (w("trinta", 184.0), "head")], [(0, "neutral"), (w("trinta", 184.0), "shocked")],
         appear=177.2, look=-1)


def s16(c, t):  # 187.7 - 202.6  R$ 1,03 milhão = ~R$ 260 mil de hoje; não é um milhão (cena do gancho "milhao-inflacao")
    show(c, t, 187.8, 760, 120, M("Em dinheiro de hoje", 70, NAVY), anim="up")
    k = 1.0 - 0.75 * grow(t, w("duzentos", 192.5), 1.3)
    show(c, t, w("milhão", 188.5), 560, 470, lambda c: text(c, "R$ 1,03 milhão", 0, 0, 80, MARKER, LGRAY if k < 0.9 else GREEN),
         anim="pop")
    if t > w("duzentos", 192.5):
        line(c, 330, 478, 790, 462, 10, RED)
    money_bar(c, t, w("milhão", 188.5), 400, 940, 360, 170, GREEN, None, "daqui a 35 anos", d=0.7)
    money_bar(c, t, w("duzentos", 192.5), 760, 940, 92, 170, NAVY, "R$ 260 mil", "de hoje", d=0.7, tsize=60)
    show(c, t, w("duzentos", 192.5), 1180, 470, lambda c: hl(c, "~R$ 260 mil", 0, 0, 96, PINKISH, RED), anim="stamp")
    show(c, t, w("não", 197.0), 1180, 640, M("não é um milhão", 66, RED), anim="pop")
    show(c, t, w("metade", 201.2), 1180, 760, T("é metade da história", 52, DGRAY), anim="fade")
    hero(c, t, 1690, 1050, 0.62, [(0, "present_l"), (w("duzentos", 192.5), "shrug"), (w("quem", 198.0), "finger_up")],
         [(0, "neutral"), (w("duzentos", 192.5), "worried"), (w("quem", 198.0), "think")], appear=187.8, look=-1)


def s17(c, t):  # 202.6 - 219.9  corrige os R$ 10 pela inflação uma vez por ano
    show(c, t, 202.7, 760, 130, M("O jeito simples de resolver", 70, NAVY), anim="up")
    show(c, t, w("corrige", 207.5), 760, 290, lambda c: hl(c, "corrija os R$ 10 pela inflação, 1 vez por ano", 0, 0, 56, LYELLOW),
         anim="stamp")
    steps = [(w("corrige", 207.5), "ano 1", "R$ 10,00"), (w("quarenta", 213.0), "ano 2", "R$ 10,40"),
             (w("oitenta", 216.8), "ano 3", "R$ 10,82"), (w("diante", 218.8), "...", "e assim por diante")]
    for i, (t0, lab, val) in enumerate(steps):
        x = 250 + i * 350
        y = 760 - i * 90
        show(c, t, t0, x, y, M(val, 76 if i < 3 else 44, GREEN if i < 3 else DGRAY), anim="pop")
        show(c, t, t0, x, y + 85, T(lab, 48, DGRAY), anim="fade")
        if 0 < i < 3:
            arrow_draw(c, t, t0, x - 250, y + 20, x - 150, y - 30, d=0.3)
    hero(c, t, 1690, 1050, 0.85, [(0, "finger_up"), (w("corrige", 207.5), "present_l")], [(0, "confident"), (w("corrige", 207.5), "happy")],
         appear=202.7, look=-1)


def s18(c, t):  # 219.9 - 242.4  o esforço é o mesmo (um lanche); R$ 1,5 milhão = R$ 387 mil de hoje (+ R$ 126 mil)
    show(c, t, 220.0, 420, 360, sc(sandwich, s=0.9), anim="pop", t1=w("fazendo", 226.0))
    show(c, t, w("esforço", 221.0), 420, 520, T("o esforço é o mesmo", 50, DGRAY), anim="fade", t1=w("fazendo", 226.0))
    show(c, t, w("fazendo", 226.0), 760, 130, M("Corrigindo todo ano, em 35 anos:", 64, NAVY), anim="up")
    show(c, t, w("milhão", 230.0), 760, 270, M("R$ 1,5 milhão", 80, GREEN), anim="pop")
    show(c, t, w("milhão", 230.0, 0.2), 760, 350, T("(no dinheiro de daqui a 35 anos)", 44, DGRAY), anim="fade")
    money_bar(c, t, w("dinheiro", 233.4), 520, 960, 260 * 1.2, 190, LGRAY, "R$ 260 mil", "sempre R$ 10", d=0.6, tcol=DGRAY)
    money_bar(c, t, w("trezentos", 235.2), 860, 960, 387 * 1.2, 190, GREEN, "R$ 387 mil", "corrigindo", d=0.8, tsize=64)
    show(c, t, w("dinheiro", 233.4), 1250, 640, T("em dinheiro de hoje", 50, DGRAY), anim="fade")
    show(c, t, w("cento", 238.2), 1250, 750, lambda c: hl(c, "+ R$ 126 mil", 0, 0, 76, LGREEN, GREEN), anim="stamp")
    hero(c, t, 1690, 1050, 0.62, [(0, "present_l"), (w("trezentos", 235.2), "arms_up")],
         [(0, "neutral"), (w("trezentos", 235.2), "grin")], appear=220.0, look=-1)


def s19(c, t):  # 242.4 - 254.3  1 milhão de verdade (poder de compra de hoje): ~R$ 26 por dia, corrigidos, por 35 anos
    show(c, t, 242.5, 760, 160, M("E R$ 1 milhão de verdade?", 70, NAVY), anim="up")
    show(c, t, w("poder", 244.8), 760, 270, T("com o poder de compra de hoje", 52, DGRAY), anim="fade")
    show(c, t, w("vinte", 248.6), 760, 470, lambda c: hl(c, "~R$ 26 por dia", 0, 0, 120, LYELLOW), anim="stamp")
    show(c, t, w("corrigidos", 249.9), 760, 640, T("corrigidos todo ano pela inflação", 54, DGRAY), anim="up")
    show(c, t, w("trinta", 252.5), 760, 740, M("por 35 anos", 62, NAVY), anim="pop")
    hero(c, t, 1640, 1050, 0.95, [(0, "think"), (w("vinte", 248.6), "present_l")], [(0, "think"), (w("vinte", 248.6), "confident")],
         appear=242.5, look=-1, prop=("r", prop_calculator))


def s20(c, t):  # 254.3 - 275.8  detalhe 2: o tempo; por dia pra chegar a R$ 1 milhão: 35a R$ 10, 30a 16, 25a 27, 20a 46
    detalhe(c, t, 254.4, 2, "o tempo", LYELLOW)
    show(c, t, w("olha", 258.0), 700, 250, T("quanto guardar por dia pra chegar a R$ 1 milhão", 50, DGRAY), anim="fade")
    data = [(w("trinta", 263.8), "35 anos", 9.73, "R$ 10"), (w("trinta", 267.0), "30 anos", 16.05, "R$ 16"),
            (w("vinte", 269.3), "25 anos", 26.89, "R$ 27"), (w("vinte", 272.0), "20 anos", 46.22, "R$ 46")]
    for i, (t0, lab, v, top) in enumerate(data):
        col = GREEN if i == 0 else (ORANGE if i < 3 else RED)
        money_bar(c, t, t0, 300 + i * 270, 960, v * 11, 170, col, top, lab, d=0.6, tsize=60)
    hero(c, t, 1640, 1050, 0.85, [(0, "present_l"), (w("vinte", 272.0), "head")], [(0, "neutral"), (w("vinte", 272.0), "shocked")],
         appear=254.4, look=-1)


def s21(c, t):  # 275.8 - 287.7  -5 anos de prazo: +65% por dia; -15 anos: quase 5x
    show(c, t, 275.9, 760, 130, M("Repara:", 72, NAVY), anim="up")
    show(c, t, w("tirar", 276.5), 520, 330, T("35 anos", 56, DGRAY), anim="fade")
    show(c, t, w("tirar", 276.5), 520, 420, M("R$ 10/dia", 70, GREEN), anim="pop")
    arrow_draw(c, t, w("trinta", 278.5), 720, 380, 900, 380)
    show(c, t, w("trinta", 279.5), 1100, 330, T("30 anos", 56, DGRAY), anim="fade")
    show(c, t, w("subir", 281.5), 1100, 420, M("R$ 16/dia", 70, ORANGE), anim="pop")
    show(c, t, w("sessenta", 282.0), 810, 560, lambda c: hl(c, "+65% por dia", 0, 0, 80, PINKISH, RED), anim="stamp")
    show(c, t, w("quinze", 284.5), 810, 740, T("com 15 anos a menos:", 54, DGRAY), anim="fade")
    show(c, t, w("quintuplica", 286.4), 810, 850, M("quase 5x mais", 80, RED), anim="stamp")
    hero(c, t, 1660, 1050, 0.9, [(0, "point_l"), (w("quintuplica", 286.4), "head")], [(0, "neutral"), (w("quintuplica", 286.4), "shocked")],
         appear=275.9, look=-1)


def s22(c, t):  # 287.7 - 302.2  o começo dá tempo pra curva disparar; começar 5 anos depois = R$ 405 mil a menos
    show(c, t, 287.8, 760, 130, M("O começo que parece não render nada", 64, NAVY), anim="up")
    show(c, t, w("curva", 291.8), 380, 600, sc(tree, 0.25, s=0.6), anim="pop")
    show(c, t, w("curva", 291.8), 380, 720, T("hoje", 46, DGRAY), anim="fade")
    arrow_draw(c, t, w("disparar", 292.2), 520, 540, 720, 540)
    show(c, t, w("frente", 293.2), 880, 600, sc(tree, 1.0, s=0.6), anim="pop")
    show(c, t, w("frente", 293.2), 880, 720, T("lá na frente", 46, DGRAY), anim="fade")
    show(c, t, w("começar", 294.0), 1330, 380, T("começar 5 anos depois", 50, DGRAY), anim="fade")
    show(c, t, w("quatrocentos", 298.8), 1330, 500, lambda c: hl(c, "- R$ 405 mil", 0, 0, 84, PINKISH, RED), anim="stamp")
    show(c, t, w("quatrocentos", 298.8, 0.5), 1330, 610, T("no final", 50, DGRAY), anim="fade")
    hero(c, t, 1690, 1050, 0.7, [(0, "think"), (w("curva", 291.8), "present_l"), (w("quatrocentos", 298.8), "shrug")],
         [(0, "think"), (w("curva", 291.8), "happy"), (w("quatrocentos", 298.8), "worried")], appear=287.8, look=-1)


def s23(c, t):  # 302.2 - 320.4  na poupança (~8,3% a.a.): ~R$ 690 mil em 35 anos; R$ 337 mil a menos
    show(c, t, 302.3, 760, 130, M("Onde o dinheiro fica também pesa", 66, NAVY), anim="up")
    money_bar(c, t, 302.6, 470, 960, 1028 * 0.52, 200, GREEN, "R$ 1,03 mi", "renda fixa ~10%", d=0.7)
    show(c, t, w("poupança", 308.1), 900, 440, sc(piggy, s=0.6), anim="drop")
    money_bar(c, t, w("seiscentos", 315.0), 900, 960, 690 * 0.52, 200, LGRAY, "R$ 690 mil", "poupança ~8,3%", d=0.8, tcol=DGRAY)
    show(c, t, w("trezentos", 317.5), 1300, 500, lambda c: hl(c, "- R$ 337 mil", 0, 0, 80, PINKISH, RED), anim="stamp")
    show(c, t, w("trezentos", 317.5, 0.2), 1300, 600, T("em 35 anos", 48, DGRAY), anim="fade")
    hero(c, t, 1700, 1050, 0.6, [(0, "present_l"), (w("trezentos", 317.5), "shrug")], [(0, "neutral"), (w("trezentos", 317.5), "worried")],
         appear=302.3, look=-1)


def s24(c, t):  # 320.4 - O3  menos de 2 pontos por ano = 1/3 do resultado; renda fixa simples, segura, >= CDI
    show(c, t, 320.5, 760, 260, M("menos de 2 pontos por ano", 76, NAVY), anim="up")
    show(c, t, w("terço", 324.8), 760, 400, lambda c: hl(c, "= 1/3 do resultado", 0, 0, 84, PINKISH, RED), anim="stamp")
    items = [(w("simples", 329.5), "simples"), (w("segura", 330.4), "segura"), (w("cdi", 332.2), "rende pelo menos o CDI")]
    for i, (t0, lab) in enumerate(items):
        y = 600 + i * 110
        show(c, t, t0, 360, y, sc(check_icon, 34), anim="pop")
        show(c, t, t0 + 0.1, 420, y, L(lab, 56, INK), anim="left")
    show(c, t, w("sofisticado", 327.0), 760, 520, T("não precisa ser nada sofisticado:", 50, DGRAY), anim="fade")
    hero(c, t, 1660, 1050, 0.9, [(0, "finger_up"), (w("sofisticado", 327.0), "present_l")], [(0, "think"), (w("sofisticado", 327.0), "confident")],
         appear=320.5, look=-1)


# ======================================================================= BLOCO 3
def s25(c, t):  # O3 - 339.9  detalhe 3: o que mais surpreende, Ana e Bruno
    detalhe(c, t, O3 + 0.1, 3, "o que mais surpreende", LYELLOW)
    ana(c, t, 620, 1000, 1.0, [(0, "wave")], [(0, "happy")], appear=O3 + 0.6)
    bruno(c, t, 1060, 1000, 1.0, [(0, "wave")], [(0, "happy")], appear=O3 + 1.0)
    show(c, t, O3 + 0.6, 620, 330, M("Ana", 80, ANAC), anim="pop")
    show(c, t, O3 + 1.0, 1060, 330, M("Bruno", 80, BRUC), anim="pop")
    hero(c, t, 1640, 1050, 0.75, [(0, "present_l")], [(0, "happy")], appear=O3 + 0.1, look=-1)


def timeline(c, t, t0, y, col, a0, a1, lab, tlab=None, stop=None):
    """linha do tempo de idade 25 a 60 (x 260-1300), com trecho pintado de a0 a a1"""
    def xa(a):
        return 300 + (a - 25) * 28
    if t < t0:
        return
    line(c, xa(25), y, xa(60), y, 6, LGRAY)
    for a in (25, 35, 60):
        line(c, xa(a), y - 14, xa(a), y + 14, 5)
        text(c, f"{a}", xa(a), y + 50, 40, MARKER, DGRAY)
    k = grow(t, t0, 1.2)
    line(c, xa(a0), y, xa(a0 + (a1 - a0) * k), y, 18, col)
    if stop is not None and t > stop:
        line(c, xa(a1), y, xa(60), y, 8, (0.75, 0.9, 0.75))
        text(c, "rendendo", (xa(a1) + xa(60)) / 2, y - 34, 40, HAND, GREEN)
    if tlab:
        text(c, tlab, (xa(a0) + xa(a1)) / 2, y - 36, 42, HAND, col)


def s26(c, t):  # 339.9 - 357.8  Ana: R$ 10/dia dos 25 aos 35, depois para e só deixa rendendo
    show(c, t, 340.0, 760, 130, M("A Ana", 74, ANAC), anim="up")
    timeline(c, t, w("guardar", 340.8), 360, ANAC, 25, 35, None, "guarda R$ 10/dia", stop=w("rendendo", 355.0))
    show(c, t, w("aperta", 348.3), 360, 620, sc(gift, s=0.8), anim="pop")
    show(c, t, w("filho", 350.1), 620, 620, sc(moving_box, s=0.9), anim="pop")
    show(c, t, w("financiamento", 350.6), 880, 620, sc(house, s=0.9), anim="pop")
    show(c, t, w("para", 352.5), 620, 840, lambda c: hl(c, "para de guardar", 0, 0, 66, PINKISH, RED), anim="stamp")
    ana(c, t, 1300, 1050, 0.9, [(0, "wave"), (w("aperta", 348.3), "shrug"), (w("rendendo", 355.0), "relax")],
        [(0, "happy"), (w("aperta", 348.3), "worried"), (w("rendendo", 355.0), "happy")], appear=340.0, look=-1)
    hero(c, t, 1700, 1050, 0.55, [(0, "present_l")], [(0, "neutral")], appear=340.0, look=-1)


def s27(c, t):  # 357.8 - 371.5  Bruno: nada até os 35; R$ 10/dia dos 35 aos 60 (25 anos)
    show(c, t, 357.9, 760, 130, M("O Bruno", 74, BRUC), anim="up")
    timeline(c, t, 357.9, 360, ANAC, 25, 35, None, "Ana", stop=357.9)
    timeline(c, t, w("começa", 363.5), 580, BRUC, 35, 60, None, "Bruno: R$ 10/dia")
    show(c, t, w("nada", 360.0), 440, 700, T("nada até os 35", 46, DGRAY), anim="fade")
    show(c, t, w("vinte", 369.6), 760, 800, lambda c: hl(c, "25 anos guardando", 0, 0, 70, LYELLOW), anim="stamp")
    bruno(c, t, 1470, 1050, 0.9, [(0, "relax"), (w("acorda", 362.5), "arms_up"), (w("dez", 364.4), "thumb")],
          [(0, "neutral"), (w("acorda", 362.5), "happy")], appear=357.9, look=-1)
    hero(c, t, 1760, 1050, 0.55, [(0, "present_l")], [(0, "neutral")], appear=357.9, look=-1)


def s28(c, t):  # 371.5 - 383.6  do bolso: Ana R$ 36 mil x Bruno R$ 90 mil; quem chega com mais? A Ana, com folga
    show(c, t, 371.6, 760, 130, M("Do bolso", 74, NAVY), anim="up")
    money_bar(c, t, w("trinta", 372.5), 480, 860, 36 * 4.5, 200, ANAC, "R$ 36 mil", "Ana (10 anos)", d=0.6)
    money_bar(c, t, w("noventa", 376.0), 820, 860, 90 * 4.5, 200, BRUC, "R$ 90 mil", "Bruno (25 anos)", d=0.6)
    show(c, t, w("quem", 379.3), 1240, 330, M("Quem chega aos 60", 56, NAVY), anim="up")
    show(c, t, w("quem", 379.3, 0.4), 1240, 410, M("com mais?", 56, NAVY), anim="up")
    show(c, t, w("ana", 381.6), 1240, 560, lambda c: hl(c, "A ANA!", 0, 0, 100, LGREEN, GREEN), anim="stamp")
    show(c, t, w("folga", 382.5), 1240, 690, T("e com folga", 54, DGRAY), anim="fade")
    hero(c, t, 1690, 1050, 0.6, [(0, "present_l"), (w("quem", 379.3), "think"), (w("ana", 381.6), "arms_up")],
         [(0, "neutral"), (w("quem", 379.3), "think"), (w("ana", 381.6), "grin")], appear=371.6, look=-1)


def s29(c, t):  # 383.6 - 399.7  aos 60: Bruno R$ 372 mil, Ana R$ 656 mil: + R$ 284 mil (cena do gancho "ana-bruno")
    show(c, t, 383.7, 760, 120, M("Aos 60 anos", 74, NAVY), anim="up")
    money_bar(c, t, w("trezentos", 385.2), 520, 960, 372 * 0.95, 220, BRUC, "R$ 372 mil", "Bruno", d=0.7, tsize=62)
    money_bar(c, t, w("seiscentos", 391.5), 900, 960, 656 * 0.95, 220, ANAC, "R$ 656 mil", "Ana", d=0.9, tsize=66)
    show(c, t, w("duzentos", 394.0), 1290, 420, lambda c: hl(c, "+ R$ 284 mil", 0, 0, 80, LGREEN, GREEN), anim="stamp")
    show(c, t, w("menos", 398.0), 1290, 540, T("colocando menos da metade", 46, DGRAY), anim="fade")
    ana(c, t, 1300, 1050, 0.6, [(0, "stand"), (w("seiscentos", 391.5), "arms_up")], [(0, "happy"), (w("seiscentos", 391.5), "grin")],
        appear=w("ana", 388.0))
    hero(c, t, 1690, 1050, 0.6, [(0, "present_l"), (w("seiscentos", 391.5), "point_l")],
         [(0, "neutral"), (w("seiscentos", 391.5), "shocked")], appear=383.7, look=-1)


def s30(c, t):  # 399.7 - 409.1  por quê? os R$ 60 mil da Ana tiveram 25 anos sozinhos pra crescer
    show(c, t, 399.8, 760, 130, M("Por quê?", 80, NAVY), anim="up")
    show(c, t, w("sessenta", 401.0), 420, 640, sc(tree, 0.3, s=0.6), anim="pop")
    show(c, t, w("sessenta", 401.0), 420, 780, M("R$ 60 mil", 60, ANAC), anim="fade")
    show(c, t, w("vinte", 402.8), 760, 480, lambda c: hl(c, "25 anos", 0, 0, 84, LYELLOW), anim="stamp")
    arrow_draw(c, t, w("crescer", 404.5), 610, 600, 900, 600)
    show(c, t, w("crescer", 404.5), 1200, 640, sc(tree, 1.0, s=0.6), anim="pop")
    show(c, t, w("crescer", 404.5), 1200, 780, M("R$ 656 mil", 60, GREEN), anim="fade")
    show(c, t, w("mais", 406.2), 760, 900, T("o Bruno pôs mais dinheiro, mas deu menos tempo", 50, BRUC), anim="up")
    hero(c, t, 1640, 1050, 0.8, [(0, "think"), (w("vinte", 402.8), "present_l")], [(0, "think"), (w("vinte", 402.8), "happy")],
         appear=399.8, look=-1)


def s31(c, t):  # 409.1 - 420.6  pra empatar, Bruno: ~R$ 18/dia; se a Ana não tivesse parado: R$ 1,03 milhão
    show(c, t, 409.2, 520, 200, T("pra empatar com a Ana, o Bruno precisaria de", 46, DGRAY), anim="fade")
    show(c, t, w("dezoito", 411.5), 520, 340, lambda c: hl(c, "~R$ 18 por dia", 0, 0, 84, LYELLOW), anim="stamp")
    show(c, t, w("dez", 413.5), 520, 450, T("em vez de R$ 10", 50, DGRAY), anim="fade")
    bruno(c, t, 520, 1040, 0.6, [(0, "shrug")], [(0, "worried")], appear=409.2)
    show(c, t, w("parado", 415.8), 1150, 300, T("e se a Ana não tivesse parado?", 46, DGRAY), anim="fade")
    show(c, t, w("milhão", 418.0), 1150, 440, lambda c: hl(c, "R$ 1,03 milhão", 0, 0, 80, LGREEN, GREEN), anim="stamp")
    ana(c, t, 1150, 1040, 0.6, [(0, "stand"), (w("milhão", 418.0), "arms_up")], [(0, "happy"), (w("milhão", 418.0), "grin")],
        appear=w("parado", 415.8))
    hero(c, t, 1720, 1050, 0.55, [(0, "present_l")], [(0, "neutral")], appear=409.2, look=-1)


def s32(c, t):  # 420.6 - 440.3  não é pra desanimar: Bruno R$ 372 mil x quem não começa: zero; comece o mais cedo possível
    show(c, t, 420.7, 760, 130, M("Passou dos 35? Não desanima", 70, NAVY), anim="up")
    money_bar(c, t, w("trezentos", 428.0), 500, 880, 372 * 1.2, 220, BRUC, "R$ 372 mil", "Bruno", d=0.7)
    money_bar(c, t, w("zero", 432.5), 860, 880, 0, 220, LGRAY, "R$ 0", "quem não começa", d=0.4, tcol=RED)
    show(c, t, w("lição", 434.3), 1240, 380, T("a lição não é que é tarde", 48, DGRAY), anim="fade")
    show(c, t, w("melhor", 436.3), 1240, 500, lambda c: hl(c, "comece o mais cedo", 0, 0, 62, LGREEN, GREEN), anim="stamp")
    show(c, t, w("conseguir", 437.8), 1240, 600, T("que você conseguir", 52, GREEN), anim="fade")
    hero(c, t, 1690, 1050, 0.6, [(0, "finger_up"), (w("melhor", 436.3), "thumb")], [(0, "confident"), (w("melhor", 436.3), "happy")],
         appear=420.7, look=-1)


def s33(c, t):  # 440.3 - 455.0  R$ 10 parece muito? comece com R$ 5: ~R$ 514 mil em 35 anos
    show(c, t, 440.4, 760, 130, M("R$ 10 por dia parece muito?", 70, NAVY), anim="up")
    show(c, t, w("cinco", 443.4), 520, 330, lambda c: hl(c, "comece com R$ 5", 0, 0, 90, LYELLOW), anim="stamp")
    show(c, t, w("quinhentos", 447.7), 520, 560, M("~R$ 514 mil", 96, GREEN), anim="stamp")
    show(c, t, w("quinhentos", 447.7, 0.2), 520, 670, T("em 35 anos", 52, DGRAY), anim="fade")
    show(c, t, w("metade", 449.8), 520, 820, T("metade do milhão, com metade do esforço", 52, NAVY), anim="up")
    show(c, t, w("curva", 453.0), 1150, 720, sc(tree, 0.35, s=0.9), anim="pop")
    hero(c, t, 1640, 1050, 0.85, [(0, "think"), (w("cinco", 443.4), "present_l"), (w("curva", 453.0), "thumb")],
         [(0, "think"), (w("cinco", 443.4), "happy")], appear=440.4, look=-1, prop=("r", prop_coin))


def s34(c, t):  # 455.0 - 467.2  1. automatize: transferência de R$ 300 no dia do salário
    show(c, t, 455.1, 1300, 300, M("3 atitudes práticas", 54, DGRAY), anim="fade", t1=w("automatize", 458.0))
    step(c, t, w("automatize", 458.0), 1, "automatize")
    show(c, t, w("programa", 459.0), 420, 500, lambda c: calendar(c, "5", NAVY), anim="pop")
    show(c, t, w("salário", 461.5), 420, 680, T("dia do salário", 50, DGRAY), anim="fade")
    arrow_draw(c, t, w("trezentos", 460.0), 600, 500, 820, 500)
    show(c, t, w("trezentos", 460.0), 1020, 500, sc(piggy, s=0.8), anim="drop")
    show(c, t, w("trezentos", 460.0, 0.2), 1020, 680, M("R$ 300", 64, GREEN), anim="pop")
    show(c, t, w("dinheiro", 463.0), 760, 860, T("dinheiro parado na conta corrente some", 52, RED), anim="up")
    hero(c, t, 1640, 1050, 0.85, [(0, "finger_up"), (w("programa", 459.0), "present_l")], [(0, "confident")],
         appear=455.1, look=-1)


def s35(c, t):  # 467.2 - 479.8  2. corrija o valor todo ano: R$ 260 mil x R$ 387 mil (em dinheiro de hoje)
    step(c, t, 467.3, 2, "corrija o valor todo ano")
    show(c, t, w("reajuste", 470.5), 760, 280, T("veio o reajuste? aumente o aporte pela inflação", 50, DGRAY), anim="fade")
    money_bar(c, t, w("duzentos", 475.9), 560, 960, 260 * 1.25, 200, LGRAY, "R$ 260 mil", "sempre R$ 10", d=0.6, tcol=DGRAY)
    money_bar(c, t, w("trezentos", 477.6), 960, 960, 387 * 1.25, 200, GREEN, "R$ 387 mil", "corrigindo", d=0.6)
    show(c, t, w("trezentos", 477.6, 0.3), 1300, 600, T("em dinheiro de hoje", 46, DGRAY), anim="fade")
    hero(c, t, 1690, 1050, 0.6, [(0, "present_l"), (w("trezentos", 477.6), "thumb")], [(0, "happy")], appear=467.3, look=-1)


def s36(c, t):  # 479.8 - 494.7  3. não mexa: o melhor da curva está no fim; reserva de emergência primeiro
    step(c, t, 479.9, 3, "não mexa", PINKISH)
    show(c, t, w("parte", 481.6), 520, 440, sc(padlock, GOLD, False, s=1.0), anim="pop")
    show(c, t, w("fim", 483.0), 520, 650, T("o melhor da curva está no fim", 50, DGRAY), anim="fade")
    show(c, t, w("saca", 484.6), 520, 760, T("sacar no meio corta os anos que mais rendem", 46, RED), anim="up")
    show(c, t, w("reserva", 489.5), 1170, 520, sc(video_card, "Demitido hoje?", "a conta da reserva de emergência", s=0.6),
         anim="pop")
    show(c, t, w("reserva", 489.5, 0.2), 1170, 700, T("comece pela reserva", 48, NAVY), anim="fade")
    hero(c, t, 1680, 1050, 0.62, [(0, "finger_up"), (w("reserva", 489.5), "point_l")], [(0, "confident")], appear=479.9, look=-1)


def s37(c, t):  # 494.7 - 523.7  recapitulando
    show(c, t, 494.8, 960, 120, M("Recapitulando", 74, NAVY), anim="up")
    rows = [(w("dez", 495.8), "R$ 10/dia a ~10% ao ano: R$ 1 milhão em 35 anos", GREEN),
            (w("bolso", 501.5), "do seu bolso: só R$ 126 mil", NAVY),
            (w("inflação", 505.5), "com a inflação: ~R$ 260 mil de hoje", RED),
            (w("corrigindo", 510.3), "corrigindo todo ano: ~R$ 387 mil de hoje", GREEN),
            (w("ana", 516.1), "Ana (10 anos) termina com R$ 284 mil a mais que o Bruno (25)", ANAC)]
    for i, (t0, lab, col) in enumerate(rows):
        y = 270 + i * 135
        show(c, t, t0, 560, y, lambda c, n=i + 1, col=col: (circle(c, 0, 0, 34, col, 5),
                                                         text(c, str(n), 0, 2, 44, MARKER, WHITE)), anim="pop")
        show(c, t, t0 + 0.1, 620, y, L(lab, 48, INK), anim="left")
    hero(c, t, 290, 1040, 0.8, [(0, "present")], [(0, "happy")], appear=494.8, look=1)


def s38(c, t):  # 523.7 - END  comentários + inscreva-se
    show(c, t, 523.8, 1080, 400, lambda c: speech(c, 1000, 300, -360, 190), anim="pop")
    show(c, t, 524.0, 1080, 340, T("Me conta nos comentários:", 52, DGRAY), anim="fade")
    show(c, t, 524.2, 1080, 430, M("começaria com quantos anos?", 54, NAVY), anim="fade")
    show(c, t, w("inscreve", 529.0), 1080, 700, sc(subscribe_btn, s=1.0), anim="pop")
    hero(c, t, 340, 1010, 1.1, [(0, "wave")], [(0, "happy")], appear=523.8, look=1)
    show(c, t, 524.0, 1080, 900, T("conteúdo educativo, não é recomendação de investimento", 36, DGRAY), anim="fade")


def s39(c, t):  # END - fim (5 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres: vídeo à esquerda (x 170-950, y 300-740) e inscrever-se à direita (~1450, 520).
    show(c, t, END + 0.1, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, END + 0.4, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, END + 0.4, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (END + 2.5, "relax")], [(0, "happy")], appear=END + 0.1)


SCENES = [
    (0.0, 9.2, s01), (9.2, 16.8, s02), (16.8, 37.6, s03), (37.6, 43.8, s04), (43.8, 57.3, s05),
    (57.3, 76.3, s06), (76.3, 92.6, s07), (92.6, 116.9, s08), (116.9, 128.7, s09), (128.7, 135.4, s10),
    (135.4, 151.6, s11), (151.6, O2, s12),
    (O2, 166.3, s13), (166.3, 177.1, s14), (177.1, 187.7, s15), (187.7, 202.6, s16), (202.6, 219.9, s17),
    (219.9, 242.4, s18), (242.4, 254.3, s19), (254.3, 275.8, s20), (275.8, 287.7, s21), (287.7, 302.2, s22),
    (302.2, 320.4, s23), (320.4, O3, s24),
    (O3, 339.9, s25), (339.9, 357.8, s26), (357.8, 371.5, s27), (371.5, 383.6, s28), (383.6, 399.7, s29),
    (399.7, 409.1, s30), (409.1, 420.6, s31), (420.6, 440.3, s32), (440.3, 455.0, s33), (455.0, 467.2, s34),
    (467.2, 479.8, s35), (479.8, 494.7, s36), (494.7, 523.7, s37), (523.7, END, s38), (END, 999.0, s39),
]

# só toques pontuais, sem ruído: R$ 1 milhão / 90% juros / R$ 260 mil / a Ana!
SFX = [(w("milhão", 106.8), "soft_ding"), (w("noventa", 149.7), "tum"), (w("duzentos", 192.5), "tum"),
       (w("ana", 381.6), "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")
