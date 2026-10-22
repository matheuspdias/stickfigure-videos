"""À vista com desconto ou parcelado sem juros? A conta da Black Friday.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 3 blocos.
Tempos absolutos: bloco1 0,000 | bloco2 154,626 | bloco3 344,962 | fim da fala 524,084 | +5 s de tela final (era 15 s; reduzido a pedido em 22/10).
Premissas (21/10/2026): Selic 13,75% (Copom 16/9/2026), CDI 13,65%, IR regressivo da renda fixa (22,5% até 180 dias,
20% até 360), Abecs 1T26 (R$ 390,5 bi parcelados sem juros, 43,2% do cartão), rotativo ~15% ao mês (444,9% a.a., BC ago/2026).
Contas em contas.py."""
import json
import os

from engine import *  # noqa

O2, O3 = 154.626, 344.962
END = 524.084

_PAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras.json"), encoding="utf-8"))


def w(word, after=0.0, d=0.0):
    """início (s) da primeira palavra que começa com `word` depois de `after`, mais d"""
    word = word.lower()
    for p in _PAL:
        if p["t0"] >= after - 0.01 and p["w"].lower().strip(",.:?!").startswith(word):
            return p["t0"] + d
    raise KeyError((word, after))


def b2(x):
    return x + O2


def b3(x):
    return x + O3


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def lv(label, val, lsize=50, vsize=60, vcol=GREEN, lcol=DGRAY):
    def f(c):
        text(c, label, 0, 0, lsize, HAND, lcol, align="l")
        x = text_w(c, label, lsize, HAND) + 18
        text(c, val, x, 0, vsize, MARKER, vcol, align="l")
    return f


def strike(wd=260, col=RED):
    return lambda c: line(c, -wd / 2, 8, wd / 2, -8, 10, col)


def right_arrow(col=INK, wd=120):
    return lambda c: arrow(c, -wd / 2, 0, wd / 2, 0, col, 9, 0, 26)


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def carla(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", PURPLE); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def diego(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 4)
    other(c, t, x, y, s, poses, exprs, **kw)


def money_bar(c, t, t0, x, base, h, wd, col, top, label, d=0.9, tsize=56):
    k = grow(t, t0, d)
    if t < t0:
        return
    c.save(); c.translate(x, base)
    bar(c, max(4, h * k), wd, col)
    c.restore()
    if k > 0.6:
        text(c, top, x, base - h * k - 42, tsize, MARKER, col if col != LGRAY else DGRAY)
        text(c, label, x, base + 50, 42, HAND, DGRAY)


def tv_price(price, col=YELLOW):
    return group(sc(tv, LBLUE, s=1.0), at(150, -120, lambda c: price_tag(c, price, col)))


def step(c, t, t0, num, head, col=LYELLOW):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"{num}. {head}", 0, 0, 70, col), anim="stamp")


def ruler(c, t, t0, x0, y, wd, maxp=15, cut=4.53):
    """régua de desconto 0..maxp% com o ponto de virada"""
    if t < t0:
        return
    k = grow(t, t0, 0.7)
    xc = x0 + wd * cut / maxp
    c.save()
    rrect(c, x0, y - 30, (xc - x0) * k, 60, 12); fs(c, LBLUE, 5)
    if k > 0.99:
        rrect(c, xc, y - 30, x0 + wd - xc, 60, 12); fs(c, LGREEN, 5)
    for p in range(0, maxp + 1, 5):
        xx = x0 + wd * p / maxp
        line(c, xx, y + 30, xx, y + 50, 5)
        text(c, f"{p}%", xx, y + 85, 40, HAND, DGRAY)
    c.restore()


def ruler_mark(c, t, t0, x0, y, wd, p, col, lab, maxp=15):
    xx = x0 + wd * p / maxp
    show(c, t, t0, xx, y - 85, lambda c: (poly(c, [(-22, -30), (22, -30), (0, 10)]), fs(c, col, 5),
                                          text(c, lab, 0, -70, 46, MARKER, col)), anim="drop")


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 10.4  Black Friday, 27/11; TV de R$ 3.000
    title(c, t, 0.1, "Black Friday", y=120, size=80)
    show(c, t, w("vinte"), 560, 420, group(sc(calendar, "27", RED, s=1.4), at(0, -165, T("novembro", 50, DGRAY))), anim="drop")
    show(c, t, w("televisão"), 1230, 450, tv_price("R$ 3.000"), anim="pop")
    hero(c, t, 1700, 1040, 0.75, [(0, "wave"), (w("loja"), "present_l"), (w("televisão"), "point_l")],
         [(0, "happy"), (w("televisão"), "grin")], appear=0.1, look=-1)
    show(c, t, w("escolha"), 900, 830, lambda c: hl(c, "uma escolha", 0, 0, 58, LYELLOW), anim="stamp")


def s02(c, t):  # 10.4 - 18.96  10x R$ 300 sem juros x à vista no Pix -10% = R$ 2.700
    t0, t1 = 10.4, w("ou", 13.0)
    show(c, t, t0, 520, 150, M("PARCELADO", 64, NAVY), anim="up")
    show(c, t, t0 + 0.1, 520, 380, sc(card, NAVY, s=1.5), anim="pop")
    show(c, t, w("vezes"), 520, 560, M("10x de R$ 300", 66, INK), anim="up")
    show(c, t, w("sem", 12.0), 520, 670, lambda c: hl(c, "sem juros", 0, 0, 56, LBLUE), anim="stamp")
    show(c, t, t1, 1400, 150, M("À VISTA", 64, GREEN), anim="up")
    show(c, t, w("pix"), 1400, 380, sc(pix_tag, s=1.4), anim="pop")
    show(c, t, w("dez", 14.5), 1400, 540, lambda c: hl(c, "-10% de desconto", 0, 0, 54, LGREEN), anim="stamp")
    show(c, t, w("dois", 16.5), 1400, 680, M("R$ 2.700", 80, GREEN), anim="stamp")
    show(c, t, t1, 960, 420, M("ou", 70, DGRAY), anim="fade")
    hero(c, t, 960, 1050, 0.6, [(0, "point_l"), (t1, "point_r")], [(0, "neutral"), (t1, "happy")], appear=10.45, look=0)


def s03(c, t):  # 18.96 - 28.96  qual sai mais barato? cada um responde uma coisa
    show(c, t, 19.0, 960, 130, M("Qual sai mais barato?", 76, NAVY), anim="up")
    hero(c, t, 960, 1040, 0.85, [(0, "think")], [(0, "think")], appear=19.0, look=0)
    show(c, t, 19.3, 960, 300, sc(qmark, s=0.9), anim="pop")
    show(c, t, w("parcelado", 21.0), 430, 420, lambda c: (speech(c, 600, 200, 120, 130),
                                                       text(c, "parcelado: o dinheiro rende!", 0, -10, 48, HAND, NAVY)), anim="pop")
    diego(c, t, 330, 1040, 0.75, [(0, "stand"), (w("parcelado", 21.0), "finger_up")], [(0, "happy"), (w("parcelado", 21.0), "confident")],
          appear=21.0, look=1)
    show(c, t, w("vista", 26.0), 1490, 420, lambda c: (speech(c, 600, 200, -120, 130),
                                                    text(c, "à vista: desconto é desconto!", 0, -10, 48, HAND, GREEN)), anim="pop")
    carla(c, t, 1600, 1040, 0.75, [(0, "stand"), (w("vista", 26.0), "hips")], [(0, "happy"), (w("vista", 26.0), "confident")],
          appear=25.3, look=-1)


def s04(c, t):  # 28.96 - 38.32  hoje a conta, com os juros de hoje; regra de 10 segundos
    title(c, t, 29.0, "Hoje a gente faz a conta", y=130, size=70)
    show(c, t, w("conta", 29.5), 1150, 440, sc(calculator, "%", s=1.3), anim="pop")
    show(c, t, w("juros", 31.0), 1150, 660, T("com os juros de hoje", 52, DGRAY), anim="up")
    show(c, t, w("regra", 33.0), 1150, 820, group(sc(clock, 0, s=0.6), at(70, 0, L("uma regra de 10 segundos", 54, NAVY))),
         anim="left")
    hero(c, t, 400, 1030, 1.05, [(0, "present"), (w("regra", 33.0), "finger_up")], [(0, "happy"), (w("regra", 33.0), "confident")],
         appear=29.0, look=1, prop=("l", prop_calculator))


def s05(c, t):  # 38.32 - 52.68  Abecs: R$ 390 bilhões parcelados sem juros no 1º trimestre
    show(c, t, 38.4, 960, 130, T("o tamanho do assunto", 56, DGRAY), anim="up")
    show(c, t, w("abecs"), 1080, 270, T("Abecs (empresas de cartão), 1º trimestre de 2026", 46, DGRAY), anim="fade")
    show(c, t, w("parcelaram"), 1080, 420, M("parcelado sem juros:", 62, NAVY), anim="up")
    show(c, t, w("bilhões"), 1080, 580, lambda c: text(c, "R$ 390 bilhões", 0, 0, 120, MARKER, ORANGE), anim="stamp")
    show(c, t, w("bilhões", d=0.6), 1080, 780, sc(card, ORANGE, s=1.1), anim="pop")
    hero(c, t, 300, 1030, 0.9, [(0, "stand"), (w("bilhões"), "arms_up")], [(0, "neutral"), (w("bilhões"), "shocked")],
         appear=38.4, look=1)


def s06(c, t):  # 52.68 - 61.8  43% de tudo no cartão: quase metade
    show(c, t, 52.8, 700, 520, lambda c: donut(c, 0.432 * grow(t, w("quarenta"), 1.0), 230, 80, ORANGE), anim="fade")
    show(c, t, w("quarenta"), 700, 520, M("43%", 100, ORANGE), anim="stamp")
    show(c, t, w("tudo", 54.0), 1360, 400, T("de tudo o que passou", 52), anim="up")
    show(c, t, w("cartão", 55.5), 1360, 470, T("no cartão de crédito", 52), anim="up")
    show(c, t, w("quase", 56.5), 1360, 600, lambda c: hl(c, "quase metade", 0, 0, 66, LYELLOW), anim="stamp")
    show(c, t, w("parcelar", 58.0), 1180, 870, M("parcelar virou o normal", 58, NAVY), anim="up")
    hero(c, t, 1720, 1050, 0.6, [(0, "present_l"), (w("quase", 56.5), "head")], [(0, "neutral"), (w("quase", 56.5), "shocked")],
         appear=52.8, look=-1)


def s07(c, t):  # 61.8 - 68.08  o sem juros é mesmo sem juros?
    show(c, t, 61.9, 960, 150, T("a pergunta que quase ninguém faz", 54, DGRAY), anim="up")
    show(c, t, w("sem", 65.0), 1100, 430, lambda c: text(c, "o \"sem juros\"", 0, 0, 96, MARKER, NAVY), anim="up")
    show(c, t, w("mesmo", 66.0), 1100, 580, lambda c: text(c, "é mesmo sem juros?", 0, 0, 84, MARKER, RED), anim="stamp")
    show(c, t, w("mesmo", 66.0, 0.5), 1100, 790, sc(qmark, s=1.3), anim="pop")
    hero(c, t, 380, 1030, 1.05, [(0, "stand"), (w("sem", 65.0), "think")], [(0, "neutral"), (w("sem", 65.0), "think")],
         appear=61.9, look=1)


def s08(c, t):  # 68.08 - 79.72  preço de verdade: R$ 2.700
    show(c, t, 68.2, 620, 420, tv_price("R$ 3.000"), anim="pop")
    show(c, t, w("setecentos", 70.0), 620, 720, lv("à vista:", "R$ 2.700", 50, 62, GREEN), anim="left")
    show(c, t, w("verdade", 76.0), 1390, 300, T("o preço de verdade é", 54, DGRAY), anim="up")
    show(c, t, w("setecentos", 78.0), 1390, 450, lambda c: hl(c, "R$ 2.700", 0, 0, 110, LGREEN, GREEN), anim="stamp")
    hero(c, t, 1400, 1040, 0.75, [(0, "present_l"), (w("verdade", 76.0), "finger_up")], [(0, "neutral"), (w("verdade", 76.0), "confident")],
         appear=68.2, look=-1)


def s09(c, t):  # 79.72 - 88.04  parcelado paga R$ 3.000: R$ 300 a mais espalhados em 10 meses
    show(c, t, 79.8, 640, 140, lv("quem parcela paga", "R$ 3.000", 56, 70, NAVY), anim="up")
    show(c, t, w("trezentos", 82.0), 960, 300, lambda c: hl(c, "R$ 300 a mais", 0, 0, 80, (1, 0.8, 0.76), RED), anim="stamp")
    if t > w("espalhados"):
        for i in range(10):
            t0 = w("espalhados") + i * 0.12
            x = 260 + i * 155
            show(c, t, t0, x, 540, group(sc(calendar, str(i + 1), NAVY, 52, s=0.8), at(0, 115, T("+R$ 30", 44, RED))), anim="pop")
    show(c, t, w("ninguém", 86.0), 860, 820, T("pinga um pouquinho por mês... e ninguém sente", 52, DGRAY), anim="fade")
    hero(c, t, 1640, 1050, 0.5, [(0, "point_l"), (w("ninguém", 86.0), "shrug")], [(0, "neutral"), (w("ninguém", 86.0), "worried")],
         appear=79.8, look=-1)


def s10(c, t):  # 88.04 - 97.2  como se a loja te emprestasse R$ 2.700 e você devolvesse 10x R$ 300
    title(c, t, 88.1, "Vira uma taxa de juros", y=120, size=66)
    show(c, t, w("loja", 91.0), 460, 560, group(sc(bank, s=1.4), at(0, 140, T("a loja", 48, DGRAY))), anim="pop")
    show(c, t, w("emprestasse"), 960, 340, M("te empresta R$ 2.700", 56, GREEN), anim="up")
    arrow_draw(c, t, w("emprestasse", d=0.3), 660, 420, 1260, 420)
    show(c, t, w("devolvesse"), 960, 800, M("você devolve 10x R$ 300", 56, RED), anim="up")
    arrow_draw(c, t, w("devolvesse", d=0.3), 1260, 720, 660, 720)
    carla_x = 1480
    hero(c, t, carla_x, 1040, 0.8, [(0, "stand"), (w("devolvesse"), "shrug")], [(0, "neutral"), (w("devolvesse"), "worried")],
         appear=88.2, look=-1, prop=("r", prop_calculator))


def s11(c, t):  # 97.2 - 102.76  quase 2% ao mês = uns 26% ao ano
    show(c, t, 97.3, 960, 140, T("fazendo a conta...", 56, DGRAY), anim="up")
    show(c, t, w("dois", 98.8), 1060, 360, M("quase 2% ao mês", 90, RED), anim="up")
    show(c, t, w("vinte", 100.6), 1060, 600, lambda c: hl(c, "~26% ao ano", 0, 0, 130, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("vinte", 100.6, 0.4), 1060, 790, T("escondidos no \"sem juros\"", 54, DGRAY), anim="fade")
    hero(c, t, 330, 1040, 0.95, [(0, "point_r"), (w("vinte", 100.6), "head")], [(0, "neutral"), (w("vinte", 100.6), "shocked")],
         appear=97.3, look=1)


def s12(c, t):  # 102.76 - 119.25  quanto rende uma aplicação segura: menos de 0,9% ao mês líquido
    title(c, t, 102.8, "E o seu dinheiro rende quanto?", y=120, size=64)
    show(c, t, w("selic"), 1120, 290, lv("Selic:", "13,75% ao ano", 52, 64, NAVY), anim="left")
    show(c, t, w("liquidez"), 1120, 420, T("aplicação de liquidez diária, 100% do CDI", 48, DGRAY), anim="fade")
    show(c, t, w("descontado"), 1120, 510, T("já descontado o imposto de renda:", 48, DGRAY), anim="fade")
    show(c, t, w("menos", 115.0), 1120, 680, lambda c: hl(c, "menos de 0,9% ao mês", 0, 0, 86, LGREEN, GREEN), anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "think"), (w("selic"), "present"), (w("menos", 115.0), "point_r")],
         [(0, "think"), (w("selic"), "neutral"), (w("menos", 115.0), "happy")], appear=102.9, look=1, prop=("l", prop_tablet))


def s13(c, t):  # 119.25 - 130.44  mais do que o dobro; o juro foi escondido no preço
    base = 820
    show(c, t, 119.3, 960, 130, T("com 10% de desconto à vista", 54, DGRAY), anim="up")
    money_bar(c, t, w("sem", 122.0), 700, base, 470, 200, RED, "~2%", "juro escondido / mês")
    money_bar(c, t, w("seu", 124.5), 1060, base, 205, 200, GREEN, "<0,9%", "aplicação / mês")
    show(c, t, w("dobro"), 1430, 300, lambda c: hl(c, "mais do que o dobro", 0, 0, 54, LYELLOW), anim="stamp")
    show(c, t, w("escondido"), 1450, 580, lambda c: (text(c, "o juro não sumiu:", 0, -50, 46, HAND, DGRAY),
                                                   text(c, "foi escondido", 0, 20, 60, MARKER, RED),
                                                   text(c, "no preço", 0, 85, 60, MARKER, RED)), anim="pop")
    hero(c, t, 300, 1040, 0.8, [(0, "present"), (w("escondido"), "finger_up")], [(0, "neutral"), (w("escondido"), "confident")],
         appear=119.3, look=1)


def s14(c, t):  # 130.44 - 142.44  por que a loja faz isso: recebe aos poucos / antecipa / maquininha
    title(c, t, 130.5, "Por que a loja faz isso?", y=120, size=66)
    show(c, t, w("cartão", 133.5), 560, 470, sc(pos_machine, s=1.3), anim="pop")
    show(c, t, w("recebe", 134.8), 1220, 330, group(sc(x_icon, 32), at(55, 0, L("não recebe tudo na hora", 50))), anim="left")
    show(c, t, w("poucos"), 1220, 450, group(sc(clock, t, s=0.42), at(55, 0, L("recebe aos poucos", 50))), anim="left")
    show(c, t, w("taxa", 138.5), 1220, 570, group(sc(percent, s=0.42), at(55, 0, L("ou paga taxa pra adiantar", 50))), anim="left")
    show(c, t, w("maquininha"), 1220, 690, group(sc(percent, s=0.42), at(55, 0, L("+ taxa da maquininha", 50))), anim="left")
    hero(c, t, 1700, 1050, 0.55, [(0, "think"), (w("cartão", 133.5), "point_l")], [(0, "think"), (w("cartão", 133.5), "neutral")],
         appear=130.5, look=-1)


def s15(c, t):  # 142.44 - 154.63  no Pix cai na hora: receber hoje vale mais
    show(c, t, 142.5, 560, 330, sc(pix_tag, s=1.5), anim="pop")
    show(c, t, w("hora", 143.5), 560, 500, M("cai na hora", 62, GREEN), anim="up")
    show(c, t, w("custo", 144.8), 560, 600, T("e quase sem custo", 50, DGRAY), anim="up")
    show(c, t, w("desconto", 147.5), 1340, 330, T("por isso a loja topa dar", 50, DGRAY), anim="up")
    show(c, t, w("desconto", 147.5, 0.3), 1340, 420, M("desconto à vista", 66, GREEN), anim="stamp")
    show(c, t, w("receber", 149.5), 1340, 620, lambda c: hl(c, "receber hoje vale mais", 0, 0, 60, LYELLOW), anim="stamp")
    show(c, t, w("também", 151.5), 1340, 740, T("pra loja... e pra você também", 50, NAVY), anim="fade")
    hero(c, t, 960, 1050, 0.6, [(0, "present"), (w("também", 151.5), "thumb")], [(0, "happy"), (w("também", 151.5), "grin")],
         appear=142.5, look=0)


# ======================================================================= BLOCO 2
def s16(c, t):  # b2 0 - 10.68  o argumento do outro lado: o dinheiro fica rendendo
    show(c, t, b2(0.1), 960, 140, T("o argumento do outro lado (e ele é bom):", 54, DGRAY), anim="up")
    show(c, t, b2(4.0), 1120, 380, lambda c: (speech(c, 760, 220, -200, 150),
                                           text(c, "se eu parcelo, o dinheiro rende!", 0, -10, 52, HAND, NAVY)), anim="pop")
    show(c, t, b2(9.4), 1120, 720, lambda c: hl(c, "vamos pôr na conta", 0, 0, 56, LYELLOW), anim="stamp")
    hero(c, t, 400, 1040, 1.0, [(0, "stand"), (b2(4.0), "think"), (b2(7.4), "present")],
         [(0, "neutral"), (b2(4.0), "think"), (b2(7.4), "happy")], appear=b2(0.1), look=1, prop=("l", prop_tablet))


def s17(c, t):  # b2 10.68 - 21.64  Carla e Diego: a mesma TV, os dois com R$ 3.000 aplicados
    show(c, t, b2(10.7), 960, 120, M("Carla  x  Diego", 80, NAVY), anim="up")
    carla(c, t, 500, 1000, 1.0, [(0, "wave"), (b2(15.4), "stand")], [(0, "happy")], appear=b2(10.9), look=1)
    diego(c, t, 1420, 1000, 1.0, [(0, "wave"), (b2(15.4), "stand")], [(0, "happy")], appear=b2(11.5), look=-1)
    show(c, t, b2(12.9), 960, 330, tv_price("R$ 3.000"), s=0.75, anim="pop")
    for x in (500, 1420):
        show(c, t, b2(16.1), x, 380, lambda c: (piggy(c), text(c, "R$ 3.000", 0, -150, 56, MARKER, GREEN)), s=0.9, anim="drop")
    show(c, t, b2(19.4), 960, 620, T("aplicados a 100% do CDI", 48, DGRAY), anim="fade")
    hero(c, t, 960, 1050, 0.55, [(0, "present")], [(0, "happy")], appear=b2(10.8))


def s18(c, t):  # b2 21.64 - 29.4  Carla paga à vista: R$ 2.700; sobram R$ 300 aplicados
    show(c, t, b2(21.7), 600, 130, M("CARLA: à vista", 66, PURPLE), anim="up")
    carla(c, t, 300, 1030, 0.95, [(0, "present"), (b2(26.1), "thumb")], [(0, "happy"), (b2(26.1), "grin")], appear=b2(21.7), look=1)
    show(c, t, b2(23.4), 760, 330, sc(pix_tag, s=1.2), anim="pop")
    show(c, t, b2(24.2), 760, 470, lv("paga", "R$ 2.700", 52, 70, GREEN), anim="left")
    show(c, t, b2(26.1), 1350, 420, lambda c: (piggy(c), text(c, "sobram R$ 300", 0, -150, 58, MARKER, GREEN)), s=1.0, anim="drop")
    show(c, t, b2(28.2), 1350, 650, T("que ficam aplicados", 50, DGRAY), anim="fade")
    hero(c, t, 1700, 1050, 0.55, [(0, "present_l"), (b2(26.1), "thumb")], [(0, "happy")], appear=b2(21.8), look=-1)


def s19(c, t):  # b2 29.4 - 39.28  Diego parcela: 10x R$ 300, deixa os R$ 3.000 aplicados e tira R$ 300 por mês
    show(c, t, b2(29.5), 1320, 130, M("DIEGO: parcela", 66, ORANGE), anim="up")
    diego(c, t, 1700, 1030, 0.9, [(0, "present_l"), (b2(36.8), "point_l")], [(0, "happy"), (b2(36.8), "confident")],
          appear=b2(29.5), look=-1)
    show(c, t, b2(30.8), 1150, 330, M("10x de R$ 300", 66, NAVY), anim="up")
    show(c, t, b2(33.8), 700, 520, lambda c: (piggy(c), text(c, "R$ 3.000", 0, -150, 56, MARKER, GREEN)), s=1.0, anim="drop")
    show(c, t, b2(36.8), 1000, 520, group(sc(bills, 1, s=0.7), at(80, 0, L("- R$ 300 todo mês", 54, RED))), anim="left")
    arrow_draw(c, t, b2(37.4), 830, 540, 930, 530)
    hero(c, t, 300, 1050, 0.6, [(0, "present"), (b2(36.8), "point_r")], [(0, "neutral")], appear=b2(29.6), look=1)


def s20(c, t):  # b2 39.28 - 58.52  o saldo cai e o rendimento cai junto: R$ 32 no 1º mês, R$ 3 no último
    title(c, t, b2(39.3), "O saldo do Diego, mês a mês", y=110, size=60)
    base = 820
    saldos = [3000 - 300 * i for i in range(10)]
    for i, s in enumerate(saldos):
        t0 = b2(44.4) + i * 0.25
        x = 440 + i * 115
        k = grow(t, t0, 0.6)
        if t >= t0:
            c.save(); c.translate(x, base); bar(c, max(4, 520 * s / 3000 * k), 80, GREEN if i < 9 else LGREEN); c.restore()
            if k > 0.6:
                text(c, f"{i + 1}º", x, base + 45, 38, HAND, DGRAY)
    show(c, t, b2(49.5), 520, 230, lambda c: hl(c, "1º mês: rende ~R$ 32", 0, 0, 48, LGREEN), anim="stamp")
    show(c, t, b2(56.8), 1400, 560, lambda c: hl(c, "último: ~R$ 3", 0, 0, 48, LYELLOW), anim="stamp")
    show(c, t, b2(52.5), 960, 230, T("(antes do imposto)", 40, DGRAY), anim="fade")
    hero(c, t, 1720, 1050, 0.55, [(0, "present_l"), (b2(45.0), "point_l")], [(0, "neutral")], appear=b2(39.3), look=-1)


def s21(c, t):  # b2 58.52 - 68.48  IR sobre cada resgate: 22,5% até 6 meses, 20% até 1 ano
    title(c, t, b2(58.6), "E tem imposto de renda", y=120, size=66)
    show(c, t, b2(60.6), 1080, 300, T("sobre o rendimento de cada resgate", 52, DGRAY), anim="up")
    show(c, t, b2(62.2), 1080, 480, lv("até 6 meses:", "22,5%", 54, 80, RED), anim="left")
    show(c, t, b2(65.7), 1080, 640, lv("até 1 ano:", "20%", 54, 80, ORANGE), anim="left")
    hero(c, t, 330, 1040, 0.95, [(0, "stand"), (b2(62.2), "point_r")], [(0, "neutral"), (b2(62.2), "worried")], appear=b2(58.6), look=1)


def s22(c, t):  # b2 68.48 - 74.28  10 meses depois: TV paga. Quanto sobrou?
    show(c, t, b2(68.5), 960, 140, M("10 meses depois", 70, NAVY), anim="up")
    show(c, t, b2(69.9), 960, 420, group(sc(tv, LGREEN, "PAGA", s=1.0)), anim="pop")
    show(c, t, b2(72.5), 960, 700, lambda c: hl(c, "quanto sobrou pra cada um?", 0, 0, 62, LYELLOW), anim="stamp")
    carla(c, t, 380, 1030, 0.85, [(0, "stand"), (b2(72.5), "think")], [(0, "happy"), (b2(72.5), "think")], appear=b2(68.6), look=1)
    hero(c, t, 960, 1060, 0.5, [(0, "present")], [(0, "happy")], appear=b2(68.6))
    diego(c, t, 1540, 1030, 0.85, [(0, "stand"), (b2(72.5), "think_l")], [(0, "happy"), (b2(72.5), "think")], appear=b2(68.6), look=-1)


def s23(c, t):  # b2 74.28 - 91.04  Diego R$ 148, Carla R$ 327: quase R$ 180 a mais
    base = 840
    show(c, t, b2(74.3), 960, 120, T("o que sobrou depois de pagar a TV", 54, DGRAY), anim="up")
    money_bar(c, t, b2(77.4), 640, base, 250, 200, ORANGE, "R$ 148", "Diego (parcelou)", tsize=64)
    money_bar(c, t, b2(85.4), 980, base, 550, 200, PURPLE, "R$ 327", "Carla (à vista)", tsize=64)
    show(c, t, b2(88.6), 1520, 380, lambda c: hl(c, "+ R$ 179", 0, 0, 84, LGREEN, GREEN), anim="stamp")
    show(c, t, b2(88.9), 1520, 480, T("pra Carla", 50, DGRAY), anim="fade")
    diego(c, t, 300, 1040, 0.75, [(0, "stand"), (b2(85.4), "shrug")], [(0, "neutral"), (b2(85.4), "worried")], appear=b2(74.4), look=1)
    carla(c, t, 1300, 1040, 0.7, [(0, "stand"), (b2(88.6), "arms_up")], [(0, "neutral"), (b2(88.6), "grin")], appear=b2(74.4), look=-1)
    hero(c, t, 1620, 1040, 0.7, [(0, "present_l"), (b2(88.6), "thumb")], [(0, "neutral"), (b2(88.6), "grin")], appear=b2(74.4), look=-1)


def s24(c, t):  # b2 91.04 - 95.68  mesmo rendendo o tempo todo, o desconto ganhou
    show(c, t, b2(91.1), 960, 250, T("mesmo com o dinheiro do Diego rendendo o tempo todo...", 52, DGRAY), anim="up")
    show(c, t, b2(94.3), 960, 450, lambda c: hl(c, "o desconto ganhou", 0, 0, 100, LGREEN, GREEN), anim="stamp")
    carla(c, t, 760, 1030, 0.9, [(0, "stand"), (b2(94.3), "arms_up")], [(0, "happy"), (b2(94.3), "grin")], appear=b2(91.1), look=1)
    hero(c, t, 1180, 1030, 0.9, [(0, "present_l"), (b2(94.3), "thumb")], [(0, "happy"), (b2(94.3), "grin")], appear=b2(91.1), look=-1)


def s25(c, t):  # b2 95.68 - 101.64  à vista sempre ganha? Não: depende do desconto
    show(c, t, b2(95.7), 1100, 260, M("pagar à vista sempre ganha?", 70, NAVY), anim="up")
    show(c, t, b2(98.7), 1100, 450, lambda c: text(c, "NÃO.", 0, 0, 130, MARKER, RED), anim="stamp")
    show(c, t, b2(99.5), 1100, 650, lambda c: hl(c, "depende do tamanho do desconto", 0, 0, 58, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "think"), (b2(98.7), "finger_up")], [(0, "think"), (b2(98.7), "confident")], appear=b2(95.7), look=1)


def s26(c, t):  # b2 101.64 - 121.16  bastam R$ 2.864 aplicados hoje: desconto de equilíbrio ~4,5%
    show(c, t, b2(101.7), 960, 120, T("pra pagar 10 parcelas de R$ 300...", 56, DGRAY), anim="up")
    show(c, t, b2(105.4), 560, 380, group(sc(strike(320), s=1.0), at(0, 0, M("R$ 3.000", 70, DGRAY))), anim="fade")
    show(c, t, b2(110.0), 300, 530, lv("bastam", "R$ 2.864", 54, 80, GREEN), anim="left")
    show(c, t, b2(111.6), 560, 640, T("aplicados hoje", 50, DGRAY), anim="fade")
    show(c, t, b2(114.3), 560, 740, T("o rendimento cobre o resto", 50, NAVY), anim="fade")
    show(c, t, b2(116.6), 1400, 400, T("isso equivale a um desconto de", 48, DGRAY), anim="up")
    show(c, t, b2(117.6), 1400, 540, lambda c: text(c, "~4,5%", 0, 0, 130, MARKER, NAVY), anim="stamp")
    show(c, t, b2(119.9), 1400, 720, lambda c: hl(c, "o ponto de virada", 0, 0, 64, LYELLOW), anim="stamp")
    hero(c, t, 960, 1060, 0.5, [(0, "present"), (b2(117.6), "point_r")], [(0, "neutral"), (b2(117.6), "confident")],
         appear=b2(101.7), look=1, prop=("l", prop_calculator))


RX, RY, RW = 360, 330, 1200


def s27(c, t):  # b2 121.16 - 136.12  desconto de 3%: parcelar ganha (148 x 98)
    title(c, t, b2(121.2), "Régua do desconto à vista (em 10x)", y=110, size=56)
    ruler(c, t, b2(121.3), RX, RY, RW)
    show(c, t, b2(121.8), RX + RW * 4.53 / 15, RY + 140, T("virada: 4,5%", 46, NAVY), anim="fade")
    show(c, t, b2(122.0), RX + RW * 2.2 / 15, RY + 210, M("parcele", 60, BLUE), anim="fade")
    show(c, t, b2(122.0), RX + RW * 10 / 15, RY + 210, M("à vista", 60, GREEN), anim="fade")
    ruler_mark(c, t, b2(124.2), RX, RY, RW, 3, ORANGE, "3%")
    show(c, t, b2(129.7), 700, 720, lv("parcelou:", "R$ 148", 54, 72, ORANGE), anim="left")
    show(c, t, b2(133.1), 700, 840, lv("à vista:", "R$ 98", 54, 72, PURPLE), anim="left")
    show(c, t, b2(126.0), 1250, 760, group(sc(check_icon, 42), at(60, 0, L("parcelar ganha", 56, BLUE))), anim="pop")
    hero(c, t, 330, 1050, 0.6, [(0, "point_r"), (b2(126.0), "thumb")], [(0, "neutral"), (b2(126.0), "happy")], appear=b2(121.2), look=1)


def s28(c, t):  # b2 136.12 - 151.24  passou disso, à vista ganha; com 15%: R$ 491 x R$ 148
    title(c, t, b2(136.1), "Régua do desconto à vista (em 10x)", y=110, size=56)
    ruler(c, t, b2(136.1), RX, RY, RW)
    show(c, t, b2(136.1), RX + RW * 4.53 / 15, RY + 140, T("virada: 4,5%", 46, NAVY), anim="fade")
    show(c, t, b2(136.4), RX + RW * 10 / 15, RY + 210, lambda c: hl(c, "à vista ganha", 0, 0, 54, LGREEN, GREEN), anim="stamp")
    ruler_mark(c, t, b2(143.0), RX, RY, RW, 15, GREEN, "15%")
    show(c, t, b2(145.4), 700, 720, lv("à vista:", "R$ 491", 54, 72, PURPLE), anim="left")
    show(c, t, b2(148.4), 700, 840, lv("parcelou:", "R$ 148", 54, 72, ORANGE), anim="left")
    show(c, t, b2(140.3), 1450, 720, T("quanto maior o desconto,", 50, DGRAY), anim="fade")
    show(c, t, b2(141.3), 1450, 790, T("maior a vantagem", 50, DGRAY), anim="fade")
    hero(c, t, 330, 1050, 0.6, [(0, "point_r"), (b2(143.0), "arms_up")], [(0, "neutral"), (b2(143.0), "grin")], appear=b2(136.1), look=1)


def s29(c, t):  # b2 151.24 - 162.51  a regra: parcelas ÷ 2
    title(c, t, b2(151.3), "A regra pra usar na loja", y=120, size=70)
    show(c, t, b2(155.6), 1100, 360, lambda c: (text(c, "nº de parcelas", 0, 0, 80, MARKER, NAVY),
                                             line(c, -300, 60, 300, 60, 8),
                                             text(c, "2", 0, 130, 80, MARKER, NAVY)), anim="pop")
    show(c, t, b2(158.3), 1100, 700, T("= o desconto mínimo, em %,", 54, DGRAY), anim="up")
    show(c, t, b2(160.4), 1100, 790, lambda c: hl(c, "pra valer pagar à vista", 0, 0, 64, LGREEN, GREEN), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "present"), (b2(155.6), "finger_up")], [(0, "happy"), (b2(155.6), "confident")],
         appear=b2(151.3), look=1)


def s30(c, t):  # b2 162.51 - 178.67  10x: 5% | 6x: 3% | 12x: 6%
    title(c, t, b2(162.6), "Regra da metade", y=110, size=66)
    rows = [(b2(162.9), "10x", "5%"), (b2(169.9), "6x", "3%"), (b2(176.2), "12x", "6%")]
    for i, (t0, n, p) in enumerate(rows):
        y = 300 + i * 190
        show(c, t, t0, 760, y, M(n, 90, NAVY), anim="left")
        arrow_draw(c, t, t0 + 0.4, 900, y, 1080, y)
        show(c, t, t0 + 1.2, 1300, y, group(at(-40, 0, M(p, 90, GREEN)), at(70, 0, L("ou mais: à vista", 44, DGRAY))), anim="pop")
    hero(c, t, 330, 1050, 0.75, [(0, "present"), (b2(169.9), "point_r")], [(0, "happy")], appear=b2(162.6), look=1)


def s31(c, t):  # b2 178.67 - O3  funciona de 6 a 12 parcelas; quando manda à vista, confie
    show(c, t, b2(178.7), 1100, 260, T("com os juros de hoje, funciona muito bem", 54, DGRAY), anim="up")
    show(c, t, b2(182.4), 1100, 380, M("de 6 a 12 parcelas", 72, NAVY), anim="up")
    show(c, t, b2(185.5), 1100, 600, group(sc(check_icon, 46), at(70, 0, L("mandou pagar à vista?", 56))), anim="left")
    show(c, t, b2(187.6), 1100, 720, lambda c: hl(c, "o à vista ganha mesmo", 0, 0, 66, LGREEN, GREEN), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "present"), (b2(187.6), "thumb")], [(0, "happy"), (b2(187.6), "grin")], appear=b2(178.7), look=1)


# ======================================================================= BLOCO 3
def s32(c, t):  # b3 0 - 8.16  condição: o dinheiro já existe e está guardado
    show(c, t, b3(0.1), 960, 140, lambda c: ribbon(c, "ATENÇÃO", RED, 58), anim="stamp")
    show(c, t, b3(1.4), 1100, 340, M("essa conta tem uma condição", 66, NAVY), anim="up")
    show(c, t, b3(5.2), 1100, 560, lambda c: hl(c, "o dinheiro já existe e está guardado", 0, 0, 58, LYELLOW), anim="stamp")
    show(c, t, b3(6.8), 1100, 760, sc(piggy, s=0.9), anim="drop")
    hero(c, t, 330, 1040, 1.0, [(0, "finger_up")], [(0, "confident")], appear=b3(0.1), look=1)


def s33(c, t):  # b3 8.16 - 24.16  sem o dinheiro: compra com o salário dos próximos 10 meses; cabe no meu mês?
    show(c, t, b3(8.2), 560, 200, T("não tem os R$ 3.000?", 56, DGRAY), anim="up")
    show(c, t, b3(11.2), 560, 330, M("não rende nada", 64, RED), anim="up")
    show(c, t, b3(13.6), 560, 470, T("você compra com o salário", 50), anim="fade")
    show(c, t, b3(15.0), 520, 550, M("dos próximos 10 meses", 52, ORANGE), anim="up")
    show(c, t, b3(17.4), 1380, 300, T("a pergunta muda:", 54, DGRAY), anim="up")
    show(c, t, b3(18.5), 1380, 410, group(sc(strike(520), s=1.0), at(0, 0, T("à vista ou parcelado?", 52, DGRAY))), anim="fade")
    show(c, t, b3(21.8), 1360, 600, lambda c: hl(c, "essa compra cabe no meu mês?", 0, 0, 50, LYELLOW), anim="stamp")
    diego(c, t, 560, 1050, 0.6, [(0, "shrug"), (b3(21.8), "think")], [(0, "worried"), (b3(21.8), "think")], appear=b3(8.2))
    hero(c, t, 1360, 1050, 0.6, [(0, "stand"), (b3(21.8), "finger_up")], [(0, "neutral"), (b3(21.8), "confident")], appear=b3(8.3))


def s34(c, t):  # b3 24.16 - 33.12  a armadilha: a parcela parece pequena; Black Friday animada
    title(c, t, b3(24.2), "A armadilha", y=120, size=76, col=RED)
    show(c, t, b3(26.4), 900, 330, lv("parcela de", "R$ 300", 54, 70, NAVY), anim="left")
    show(c, t, b3(27.9), 1100, 440, T("parece pequena...", 54, DGRAY), anim="fade")
    show(c, t, b3(31.4), 1060, 680, sc(cart, s=1.2), anim="pop")
    show(c, t, b3(31.4), 1060, 870, M("Black Friday animada", 58, ORANGE), anim="up")
    diego(c, t, 420, 1040, 1.0, [(0, "stand"), (b3(31.4), "arms_up")], [(0, "happy"), (b3(31.4), "grin")], appear=b3(29.2), look=1)
    hero(c, t, 1640, 1040, 0.75, [(0, "present_l"), (b3(31.4), "head")], [(0, "neutral"), (b3(31.4), "worried")], appear=b3(24.3), look=-1)


def s35(c, t):  # b3 33.12 - 52.08  TV 300, celular 200, geladeira 300, air fryer 100, tênis 100
    items = [(b3(33.2), sc(tv, LBLUE, s=0.6), "TV", "R$ 300"),
             (b3(35.8), sc(phone, s=0.75), "celular", "R$ 200"),
             (b3(40.2), sc(fridge, s=0.6), "geladeira", "R$ 300"),
             (b3(45.3), sc(air_fryer, s=0.7), "air fryer", "R$ 100"),
             (b3(47.4), sc(sneaker, s=0.65), "tênis", "R$ 100")]
    show(c, t, b3(33.2), 960, 110, T("as parcelas do Diego, por mês", 54, DGRAY), anim="up")
    for i, (t0, fn, lab, val) in enumerate(items):
        x = 330 + i * 315
        show(c, t, t0, x, 360, fn, anim="pop")
        show(c, t, t0 + 0.1, x, 540, T(lab, 46), anim="fade")
        tv0 = {0: b3(34.2), 1: b3(39.2), 2: b3(44.0), 3: b3(46.6), 4: b3(48.4)}[i]
        show(c, t, tv0, x, 630, M(val, 62, RED), anim="stamp")
    show(c, t, b3(49.4), 960, 800, T("cada uma, sozinha, parece pouco", 54, NAVY), anim="up")
    hero(c, t, 1700, 1060, 0.5, [(0, "present_l"), (b3(49.4), "shrug")], [(0, "neutral"), (b3(49.4), "worried")], appear=b3(33.2), look=-1)


def s36(c, t):  # b3 52.08 - 61.68  juntas: R$ 1.000 por mês; com renda de R$ 4.000, 1/4 já tem dono
    show(c, t, b3(52.1), 640, 200, T("juntas:", 56, DGRAY), anim="up")
    show(c, t, b3(53.1), 640, 350, lambda c: text(c, "R$ 1.000", 0, 0, 130, MARKER, RED), anim="stamp")
    show(c, t, b3(54.1), 640, 480, T("por mês, por quase um ano", 52, DGRAY), anim="fade")
    show(c, t, b3(56.6), 1360, 470, lambda c: donut(c, 0.25 * grow(t, b3(57.9), 0.9), 190, 70, RED), anim="fade")
    show(c, t, b3(57.9), 1360, 470, M("1/4", 90, RED), anim="stamp")
    show(c, t, b3(56.6), 1360, 220, lv("renda:", "R$ 4.000", 48, 58, NAVY), anim="up")
    show(c, t, b3(59.4), 1360, 740, lambda c: hl(c, "já tem dono", 0, 0, 58, (1, 0.8, 0.76), RED), anim="stamp")
    diego(c, t, 640, 1040, 0.7, [(0, "stand"), (b3(57.9), "head")], [(0, "neutral"), (b3(57.9), "desperate")], appear=b3(52.1))


def s37(c, t):  # b3 61.68 - 75.68  imprevisto → rotativo ~15% ao mês → R$ 1.000 custa ~R$ 150 em 1 mês
    steps = [(b3(61.7), "um imprevisto", ORANGE), (b3(63.2), "a fatura não fecha", ORANGE),
             (b3(66.4), "rotativo do cartão: ~15% ao mês", RED)]
    for i, (t0, lab, col) in enumerate(steps):
        y = 160 + i * 150
        show(c, t, t0, 1080, y, M(lab, 56, col), anim="up")
        if i < 2:
            arrow_draw(c, t, t0 + 1.0, 1080, y + 40, 1080, y + 105)
    show(c, t, b3(70.2), 1080, 680, lv("R$ 1.000 por 1 mês =", "~R$ 150", 54, 84, RED), anim="left")
    show(c, t, b3(74.1), 1080, 790, T("só de juros", 52, DGRAY), anim="fade")
    hero(c, t, 330, 1040, 0.95, [(0, "stand"), (b3(66.4), "head")], [(0, "worried"), (b3(66.4), "desperate")], appear=b3(61.7), look=1)


def s38(c, t):  # b3 75.68 - 80.88  apaga todo o rendimento (R$ 148)
    show(c, t, b3(75.7), 960, 250, T("isso apaga, de uma vez,", 56, DGRAY), anim="up")
    show(c, t, b3(77.8), 960, 420, group(M("os R$ 148 de rendimento", 70, GREEN), at(0, 0, strike(820))), anim="fade")
    show(c, t, b3(79.3), 960, 560, T("que o Diego ganhou parcelando a TV", 52, DGRAY), anim="fade")
    diego(c, t, 960, 1050, 0.7, [(0, "head")], [(0, "desperate")], appear=b3(75.7))


def s39(c, t):  # b3 80.88 - 84.8  como decidir? 5 passos
    show(c, t, b3(80.9), 1100, 340, M("Como decidir na Black Friday?", 72, NAVY), anim="up")
    show(c, t, b3(83.6), 1100, 560, lambda c: hl(c, "5 passos", 0, 0, 100, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "present"), (b3(83.6), "finger_up")], [(0, "happy"), (b3(83.6), "confident")], appear=b3(80.9), look=1)


def s40(c, t):  # b3 84.8 - 96.56  1. pesquise o preço antes
    step(c, t, b3(84.8), 1, "pesquise o preço antes")
    show(c, t, b3(87.6), 700, 450, group(sc(calendar, "NOV", ORANGE, 46, s=1.2), at(0, 170, T("acompanhe semanas antes", 46, DGRAY))), anim="pop")
    # preço que sobe e cai
    if t > b3(94.1):
        k = grow(t, b3(94.1), 1.6)
        pts = [(1060, 640), (1250, 640), (1400, 430), (1580, 640)]
        c.save(); c.move_to(*pts[0])
        n = int(1 + k * 3)
        for p in pts[1:n + 1]:
            c.line_to(*p)
        rgb(c, RED); c.set_line_width(10); c.stroke(); c.restore()
    show(c, t, b3(94.1), 1330, 330, T("subiu em novembro...", 46, RED), anim="fade")
    show(c, t, b3(95.4), 1430, 740, T("...pra \"cair\" no dia", 46, RED), anim="fade")
    show(c, t, b3(91.6), 1330, 860, lambda c: hl(c, "o desconto é desconto mesmo?", 0, 0, 50, LYELLOW), anim="stamp")
    hero(c, t, 260, 1050, 0.75, [(0, "think")], [(0, "think")], appear=b3(84.9), look=1)


def s41(c, t):  # b3 96.56 - 111.92  2. pergunte o preço à vista; lei de 2017
    step(c, t, b3(96.56), 2, "pergunte o preço à vista")
    show(c, t, b3(99.8), 1150, 290, T("desde 2017, a lei permite preços diferentes", 50, DGRAY), anim="up")
    for i, (t0, fn) in enumerate([(b3(104.2), sc(pix_tag, s=0.9)), (b3(104.9), sc(bills, 2, s=0.7)), (b3(105.7), sc(card, NAVY, s=0.9))]):
        show(c, t, t0, 820 + i * 330, 470, fn, anim="pop")
    show(c, t, b3(106.5), 1150, 660, T("a loja não é obrigada a dar desconto...", 50, DGRAY), anim="fade")
    show(c, t, b3(108.8), 1150, 780, lambda c: hl(c, "mas muitas dão (pra quem pergunta)", 0, 0, 56, LGREEN, GREEN), anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (b3(108.8), "thumb")], [(0, "happy"), (b3(108.8), "grin")], appear=b3(96.6), look=1)


def s42(c, t):  # b3 111.92 - 120.96  3. regra da metade
    step(c, t, b3(111.92), 3, "regra da metade")
    show(c, t, b3(114.6), 680, 380, lv("desconto maior que", "parcelas ÷ 2", 52, 66, NAVY), anim="left")
    show(c, t, b3(117.7), 1100, 490, lambda c: hl(c, "pague à vista", 0, 0, 64, LGREEN, GREEN), anim="stamp")
    show(c, t, b3(118.7), 680, 650, lv("desconto menor:", "pode parcelar", 52, 60, BLUE), anim="left")
    hero(c, t, 330, 1040, 1.0, [(0, "present"), (b3(117.7), "point_r")], [(0, "happy")], appear=b3(112.0), look=1)


def s43(c, t):  # b3 120.96 - 139.84  cashback/pontos: +1 ponto; 10x: ~5,5%
    show(c, t, b3(121.0), 960, 130, T("um detalhe:", 56, DGRAY), anim="up")
    show(c, t, b3(122.3), 700, 360, group(sc(card, NAVY, s=1.2), at(0, -120, lambda c: hl(c, "cashback / pontos", 0, 0, 44, LYELLOW))), anim="pop")
    show(c, t, b3(125.7), 1360, 360, group(sc(pix_tag, s=1.0), at(0, 100, T("não devolve nada", 44, DGRAY))), anim="pop")
    show(c, t, b3(127.4), 960, 560, T("some isso ao lado do parcelado", 52, NAVY), anim="fade")
    show(c, t, b3(130.1), 560, 670, lv("devolve 1%?", "a régua sobe 1 ponto", 50, 56, ORANGE), anim="left")
    show(c, t, b3(134.6), 960, 800, lambda c: hl(c, "10x: à vista a partir de ~5,5%", 0, 0, 58, LGREEN, GREEN), anim="stamp")
    hero(c, t, 1720, 1050, 0.6, [(0, "finger_up"), (b3(130.1), "point_l")], [(0, "confident")], appear=b3(121.0), look=-1)


def s44(c, t):  # b3 139.84 - 149.44  4. só parcele com o dinheiro guardado
    step(c, t, b3(139.84), 4, "só parcele com o dinheiro guardado")
    show(c, t, b3(141.8), 700, 450, sc(piggy, s=1.2), anim="drop")
    show(c, t, b3(143.4), 700, 620, T("separado e rendendo", 50, GREEN), anim="fade")
    show(c, t, b3(145.3), 1300, 420, T("parcelar o que você não tem", 52, DGRAY), anim="up")
    show(c, t, b3(147.1), 1300, 540, group(sc(strike(380), s=1.0), at(0, 0, M("estratégia", 64, DGRAY))), anim="fade")
    show(c, t, b3(148.4), 1300, 680, lambda c: hl(c, "é dívida", 0, 0, 80, (1, 0.8, 0.76), RED), anim="stamp")
    hero(c, t, 1720, 1050, 0.6, [(0, "finger_up")], [(0, "confident")], appear=b3(139.9), look=-1)


def s45(c, t):  # b3 149.44 - 160.21  5. some as parcelas que você já tem
    step(c, t, b3(149.44), 5, "some as parcelas que já tem")
    show(c, t, b3(152.2), 700, 460, sc(calculator, "R$ 1.000", s=1.3), anim="pop")
    show(c, t, b3(154.1), 1300, 360, group(sc(strike(480), s=1.0), at(0, 0, T("quanto custa a parcela?", 52, DGRAY))), anim="fade")
    show(c, t, b3(157.3), 1300, 540, lambda c: (hl(c, "quanto do meu salário", 0, -45, 56, LYELLOW),
                                             hl(c, "já está comprometido?", 0, 45, 56, LYELLOW)), anim="stamp")
    hero(c, t, 1720, 1050, 0.6, [(0, "present_l"), (b3(157.3), "think_l")], [(0, "neutral"), (b3(157.3), "think")],
         appear=b3(149.5), look=-1, prop=("r", prop_calculator))


def s46(c, t):  # b3 160.21 - 170.77  vídeo do 13º
    show(c, t, b3(160.3), 960, 140, T("vai usar parte do 13º nas compras?", 56), anim="up")
    show(c, t, b3(164.0), 1180, 520, lambda c: video_card(c, "O que fazer com o 13º", "a ordem certa",
                                                       icon=lambda c: play_btn(c, 70)), anim="pop")
    show(c, t, b3(168.1), 1180, 850, T("quitar o cartão vem antes de tudo", 48, RED), anim="fade")
    hero(c, t, 380, 1030, 1.0, [(0, "think"), (b3(164.0), "point_r")], [(0, "think"), (b3(164.0), "happy")], appear=b3(160.3), look=1)


def s47(c, t):  # b3 170.77 - 177.85  comentários
    show(c, t, b3(170.8), 1080, 420, lambda c: speech(c, 1000, 300, -360, 190), anim="pop")
    show(c, t, b3(171.0), 1080, 350, T("Me conta nos comentários:", 52, DGRAY), anim="fade")
    show(c, t, b3(172.8), 1080, 440, M("qual o maior desconto que", 46, NAVY), anim="fade")
    show(c, t, b3(174.4), 1080, 510, M("você conseguiu só por perguntar?", 46, NAVY), anim="fade")
    hero(c, t, 340, 1010, 1.1, [(0, "wave")], [(0, "happy")], appear=b3(170.8), look=1)
    show(c, t, b3(171.0), 1080, 860, T("conteúdo educativo, não é recomendação de investimento", 36, DGRAY), anim="fade")


def s48(c, t):  # b3 177.85 - END  assinatura
    show(c, t, b3(177.9), 960, 300, lambda c: text(c, "FAZ A CONTA", 0, 0, 120, MARKER, NAVY), anim="stamp")
    show(c, t, b3(178.4), 960, 430, lambda c: hl(c, "a gente faz a conta", 0, 0, 60, LYELLOW))
    hero(c, t, 960, 1010, 1.0, [(0, "present"), (b3(178.5), "wave")], [(0, "happy"), (b3(178.5), "grin")], appear=b3(177.9))


def s49(c, t):  # END - fim (5 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres: vídeo à esquerda (x 170-950, y 300-740) e inscrever-se à direita (~1450, 520).
    show(c, t, END + 0.1, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, END + 0.4, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, END + 0.4, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (END + 2.5, "relax")], [(0, "happy")], appear=END + 0.1)


SCENES = [
    (0.0, 10.4, s01), (10.4, 18.96, s02), (18.96, 28.96, s03), (28.96, 38.32, s04), (38.32, 52.68, s05),
    (52.68, 61.8, s06), (61.8, 68.08, s07), (68.08, 79.72, s08), (79.72, 88.04, s09), (88.04, 97.2, s10),
    (97.2, 102.76, s11), (102.76, 119.25, s12), (119.25, 130.44, s13), (130.44, 142.44, s14), (142.44, O2, s15),
    (O2, b2(10.68), s16), (b2(10.68), b2(21.64), s17), (b2(21.64), b2(29.4), s18), (b2(29.4), b2(39.28), s19),
    (b2(39.28), b2(58.52), s20), (b2(58.52), b2(68.48), s21), (b2(68.48), b2(74.28), s22), (b2(74.28), b2(91.04), s23),
    (b2(91.04), b2(95.68), s24), (b2(95.68), b2(101.64), s25), (b2(101.64), b2(121.16), s26), (b2(121.16), b2(136.12), s27),
    (b2(136.12), b2(151.24), s28), (b2(151.24), b2(162.51), s29), (b2(162.51), b2(178.67), s30), (b2(178.67), O3, s31),
    (O3, b3(8.16), s32), (b3(8.16), b3(24.16), s33), (b3(24.16), b3(33.12), s34), (b3(33.12), b3(52.08), s35),
    (b3(52.08), b3(61.68), s36), (b3(61.68), b3(75.68), s37), (b3(75.68), b3(80.88), s38), (b3(80.88), b3(84.8), s39),
    (b3(84.8), b3(96.56), s40), (b3(96.56), b3(111.92), s41), (b3(111.92), b3(120.96), s42), (b3(120.96), b3(139.84), s43),
    (b3(139.84), b3(149.44), s44), (b3(149.44), b3(160.21), s45), (b3(160.21), b3(170.77), s46), (b3(170.77), b3(177.85), s47),
    (b3(177.85), END, s48), (END, 999.0, s49),
]

# só toques pontuais, sem ruído: 26% ao ano / Carla R$ 327 / regra ÷2 / R$ 1.000 por mês
SFX = [(100.9, "tum"), (b2(85.4), "tum"), (b2(155.6), "soft_ding"), (b3(53.1), "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key")
