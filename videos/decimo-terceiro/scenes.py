"""O que fazer com o 13º salário: a conta do melhor destino.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 4 blocos.
Tempos absolutos: bloco1 0,000 | bloco2 137,594 | bloco3 309,539 | bloco4 423,701 | fim da fala 510,872 | +15 s de tela final.
Premissas (19/10/2026): Selic 13,75% (Copom 16/9/2026), IPCA 12m 4,58% (set/2026), rotativo 444,9% a.a. e parcelado 192,1% a.a.
(BC, ago/2026), tabela INSS 2026, isenção de IR até R$ 5 mil, acumulação a 5% real líquido a.a. Contas em contas.py."""
from engine import *  # noqa

O2, O3, O4 = 137.594, 309.539, 423.701


def b2(x):
    return x + O2


def b3(x):
    return x + O3


def b4(x):
    return x + O4


def L(s, size=50, col=INK, font=HAND):
    """texto alinhado à esquerda"""
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 6, w / 2, -6, 9, col)


def right_arrow(col=INK, w=120):
    return lambda c: arrow(c, -w / 2, 0, w / 2, 0, col, 9, 0, 26)


def ana(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", PURPLE); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def bruno(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 4)
    other(c, t, x, y, s, poses, exprs, **kw)


def tip(c, t, t0, num, head, col):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"{num}. {head}", 0, 0, 72, col), anim="stamp")


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def money_bar(c, t, t0, x, base, h, w, col, top, label, d=0.9):
    k = grow(t, t0, d)
    if t < t0:
        return
    c.save(); c.translate(x, base)
    bar(c, max(4, h * k), w, col)
    c.restore()
    if k > 0.6:
        text(c, top, x, base - h * k - 40, 52, MARKER, col if col != LGRAY else DGRAY)
        text(c, label, x, base + 50, 42, HAND, DGRAY)


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 15.1  dinheiro extra que a maioria gasta sem conta
    title(c, t, 0.2, "O seu 13º salário", y=120, size=70)
    show(c, t, 2.5, 960, 215, T("dezenas de milhões de brasileiros", 50, DGRAY), anim="up")
    show(c, t, 4.4, 820, 470, sc(bills, 3, s=1.3), anim="drop")
    show(c, t, 5.3, 820, 650, M("dinheiro extra na conta", 54, GREEN), anim="up")
    show(c, t, 11.2, 1520, 470, sc(cart, s=1.0), anim="left")
    show(c, t, 12.4, 1520, 650, T("gasto em poucas semanas", 48, RED), anim="up")
    show(c, t, 13.7, 1180, 820, group(sc(x_icon, 36), at(60, 0, L("sem fazer conta nenhuma", 52))), anim="left")
    hero(c, t, 300, 1000, 1.1, [(0, "stand"), (4.4, "present"), (11.2, "point_r"), (13.7, "shrug")],
         [(0, "happy"), (4.4, "grin"), (11.2, "worried"), (13.7, "sad")], appear=0.1, look=1)


def s02(c, t):  # 15.1 - 26.2  o mesmo 13º pode...
    show(c, t, 15.3, 960, 130, T("o mesmo 13º pode...", 62), anim="up")
    items = [(18.1, sc(card, s=1.0), "te tirar de uma dívida", RED),
             (19.8, sc(shield, GREEN, s=1.0), "te proteger de um imprevisto", NAVY),
             (21.2, sc(tree, 1.0, s=0.5), "repetido todo ano...", GREEN)]
    for i, (t0, fn, lab, col) in enumerate(items):
        x = 640 + i * 480
        show(c, t, t0, x, 450, fn)
        show(c, t, t0 + 0.2, x, 650, T(lab, 46, col), anim="up")
    show(c, t, 23.7, 1500, 820, lambda c: hl(c, "quase R$ 180 mil", 0, 0, 70, LGREEN), anim="stamp")
    hero(c, t, 260, 1030, 0.75, [(0, "present"), (23.7, "thumb")], [(0, "happy"), (23.7, "grin")], appear=15.2, look=1)


def s03(c, t):  # 26.2 - 32.4  hoje: a conta
    title(c, t, 26.3, "Hoje a gente faz a conta", y=130, size=66)
    show(c, t, 27.3, 1150, 480, sc(calculator, "13º", s=1.2), anim="pop")
    show(c, t, 29.9, 1150, 760, lambda c: hl(c, "qual é o melhor destino?", 0, 0, 62, LYELLOW), anim="stamp")
    hero(c, t, 400, 1010, 1.1, [(0, "present"), (29.9, "think")], [(0, "happy"), (29.9, "think")], appear=26.3, look=1,
         prop=("l", prop_calculator))


def s04(c, t):  # 32.4 - 46.7  Dieese: R$ 369 bilhões, 90+ milhões de pessoas
    show(c, t, 32.5, 960, 130, T("No ano passado, o Dieese estimou:", 56, DGRAY), anim="up")
    show(c, t, 36.6, 1060, 340, lambda c: text(c, "até R$ 369 bilhões", 0, 0, 104, MARKER, GREEN), anim="stamp")
    show(c, t, 39.7, 1060, 440, T("na economia", 50, DGRAY), anim="fade")
    show(c, t, 41.0, 1060, 600, M("pra mais de 90 milhões de pessoas", 60, NAVY), anim="up")
    show(c, t, 43.4, 760, 760, T("trabalhadores", 48), anim="pop")
    show(c, t, 44.5, 1110, 760, T("aposentados", 48), anim="pop")
    show(c, t, 45.4, 1440, 760, T("pensionistas", 48), anim="pop")
    hero(c, t, 250, 1020, 0.85, [(0, "stand"), (36.6, "arms_up"), (41.0, "present")],
         [(0, "neutral"), (36.6, "shocked"), (41.0, "happy")], appear=32.5, look=1)


def s05(c, t):  # 46.7 - 53.4  chega de uma vez, vai embora de uma vez
    show(c, t, 46.8, 560, 300, T("chega de uma vez...", 58, GREEN), anim="up")
    show(c, t, 47.9, 560, 560, sc(bills, 4, s=1.2), anim="drop")
    show(c, t, 49.4, 1360, 300, T("...e vai embora de uma vez", 58, RED), anim="up")
    if t > 50.0:
        for i in range(4):
            k = grow(t, 50.0 + i * 0.35, 1.2)
            if k > 0:
                c.save(); c.translate(1180 + 120 * i + 240 * k, 640 - 120 * k + 40 * i); c.rotate(0.3 * i + k)
                c.scale(0.6, 0.6); bill(c); c.restore()
    hero(c, t, 960, 1030, 0.9, [(0, "present"), (49.4, "head")], [(0, "happy"), (49.4, "desperate")], appear=46.8, look=0)


def s06(c, t):  # 53.4 - 62.0  não vem inteiro: duas parcelas
    show(c, t, 53.5, 960, 140, lambda c: ribbon(c, "ATENÇÃO", RED, 58), anim="stamp")
    show(c, t, 57.2, 1080, 330, M("o seu 13º não vem inteiro", 70, NAVY), anim="up")
    show(c, t, 60.9, 820, 620, group(sc(bills, 2, s=1.0), at(0, 150, M("1ª parcela", 52, NAVY))), anim="left")
    show(c, t, 61.3, 1340, 620, group(sc(bills, 2, s=1.0), at(0, 150, M("2ª parcela", 52, NAVY))), anim="right")
    hero(c, t, 280, 1010, 1.0, [(0, "finger_up"), (57.2, "point_r")], [(0, "confident"), (57.2, "neutral")], appear=53.5, look=1)


def s07(c, t):  # 62.0 - 77.5  datas: 30/11 e 18/12, descontos na 2ª
    title(c, t, 62.1, "Quando cai", y=110, size=64)
    show(c, t, 63.6, 640, 400, group(sc(calendar, "30", NAVY, s=1.0), at(0, -150, T("novembro", 44, DGRAY))))
    show(c, t, 65.0, 640, 600, M("metade do salário", 50, GREEN), anim="up")
    show(c, t, 67.0, 640, 690, group(sc(check_icon, 30), at(46, 0, L("sem desconto", 46))), anim="fade")
    show(c, t, 69.1, 1300, 400, group(sc(calendar, "18", RED, s=1.0), at(0, -150, T("dezembro", 44, DGRAY))))
    show(c, t, 72.5, 1300, 600, T("(o dia 20 cai num domingo)", 42, DGRAY), anim="fade")
    show(c, t, 74.8, 1200, 720, lambda c: hl(c, "aqui entram os descontos", 0, 0, 46, (1, 0.8, 0.76)), anim="stamp")
    hero(c, t, 1720, 1040, 0.7, [(0, "present_l"), (74.8, "finger_up")], [(0, "happy"), (74.8, "worried")], appear=62.1, look=-1)


def s08(c, t):  # 77.5 - 98.6  exemplo da Ana
    title(c, t, 77.6, "Exemplo: a Ana", y=110, size=64)
    ana(c, t, 280, 1010, 1.05, [(0, "stand"), (82.8, "present"), (90.7, "shrug")],
        [(0, "happy"), (82.8, "grin"), (90.7, "worried")], appear=78.9, look=1)
    show(c, t, 79.9, 760, 260, lv("salário:", "R$ 3.000", 50, 62, NAVY), anim="left")
    show(c, t, 82.8, 760, 420, lv("novembro:", "R$ 1.500", 50, 62, GREEN, after="limpos"), anim="left")
    show(c, t, 87.6, 760, 580, lv("dezembro:", "R$ 1.500?", 50, 62, DGRAY), anim="left")
    show(c, t, 90.7, 1500, 600, sc(document, "INSS", RED, 40, s=1.0), anim="drop")
    show(c, t, 92.1, 1500, 760, T("sobre o 13º inteiro", 42, DGRAY), anim="fade")
    show(c, t, 96.6, 1150, 880, lambda c: text(c, "- R$ 250", 0, 0, 84, MARKER, RED), anim="stamp")


def lv(label, val, lsize=50, vsize=60, vcol=GREEN, lcol=DGRAY, after=None):
    """rótulo manuscrito + valor no marcador, em sequência (âncora na esquerda)"""
    def f(c):
        text(c, label, 0, 0, lsize, HAND, lcol, align="l")
        x = text_w(c, label, lsize, HAND) + 18
        text(c, val, x, 0, vsize, MARKER, vcol, align="l")
        if after:
            x += text_w(c, val, vsize, MARKER) + 18
            text(c, after, x, 0, lsize, HAND, lcol, align="l")
    return f


def s09(c, t):  # 98.6 - 108.84  total: R$ 2.750, não R$ 3.000
    show(c, t, 98.7, 560, 150, lv("2ª parcela:", "pouco mais de R$ 1.250", 54, 64, NAVY), anim="up")
    show(c, t, 103.1, 960, 330, T("no total, a Ana recebe", 56, DGRAY), anim="up")
    show(c, t, 105.4, 960, 500, lambda c: text(c, "R$ 2.750", 0, 0, 150, MARKER, GREEN), anim="stamp")
    show(c, t, 107.6, 960, 700, group(M("R$ 3.000", 70, DGRAY), strike(330)), anim="fade")
    ana(c, t, 300, 1010, 1.0, [(0, "stand"), (105.4, "hips")], [(0, "neutral"), (105.4, "worried")], appear=98.7, look=1)


def s10(c, t):  # 108.84 - 124.24  imposto de renda
    title(c, t, 108.9, "E o imposto de renda?", y=120, size=64)
    show(c, t, 109.3, 400, 470, sc(document, "IR", RED, 44, s=1.1), anim="drop")
    show(c, t, 112.6, 820, 380, lv("ganha até", "R$ 5 mil/mês", 52, 62, NAVY), anim="left")
    show(c, t, 114.4, 820, 500, group(sc(check_icon, 36), at(54, 0, L("isento em 2026", 56, GREEN))), anim="left")
    show(c, t, 116.6, 820, 640, lv("Ana:", "só o INSS", 52, 62, NAVY), anim="left")
    show(c, t, 119.6, 820, 800, L("ganha mais? o IR vem na 2ª parcela", 48, RED), anim="left")
    hero(c, t, 1720, 1040, 0.65, [(0, "think_l"), (114.4, "thumb")], [(0, "think"), (114.4, "happy")], appear=109.0, look=-1)


def s11(c, t):  # 124.24 - 137.594  faça a conta do que cai de verdade
    show(c, t, 124.3, 960, 130, lambda c: hl(c, "faça a conta do valor que vai cair", 0, 0, 62, LYELLOW), anim="stamp")
    show(c, t, 130.4, 600, 450, group(T("planejar com", 46, DGRAY), at(0, 90, M("R$ 3.000", 72, NAVY))), anim="left")
    show(c, t, 131.9, 1320, 450, group(T("e receber", 46, DGRAY), at(0, 90, M("R$ 2.700", 72, NAVY))), anim="right")
    show(c, t, 132.4, 960, 500, right_arrow(INK, 140), anim="fade")
    show(c, t, 134.0, 960, 650, lambda c: ribbon(c, "COMEÇAR O ANO NO VERMELHO", RED, 54), anim="stamp")
    hero(c, t, 960, 1060, 0.5, [(0, "present"), (134.0, "head")], [(0, "neutral"), (134.0, "desperate")], appear=124.4)


# ======================================================================= BLOCO 2
def s12(c, t):  # b2 0 - 16.64  três destinos, a ordem importa
    show(c, t, b2(0.1), 520, 130, lv("o que fazer com os", "R$ 2.750?", 56, 70, GREEN, INK), anim="up")
    items = [(b2(8.0), sc(card, s=0.9), "quitar dívida cara"), (b2(9.7), sc(shield, GREEN, s=0.9), "reserva de emergência"),
             (b2(11.7), sc(tree, 1.0, s=0.42), "investir pro longo prazo")]
    for i, (t0, fn, lab) in enumerate(items):
        x = 480 + i * 480
        show(c, t, t0, x, 470, fn)
        show(c, t, t0 + 0.2, x, 650, T(lab, 46), anim="up")
        show(c, t, b2(13.7) + 0.4 * i, x, 300, lambda c, n=i + 1: hl(c, str(n), 0, 0, 60, LYELLOW), anim="stamp")
    show(c, t, b2(13.7), 960, 800, M("a ordem importa", 64, NAVY), anim="up")
    hero(c, t, 1740, 1040, 0.6, [(0, "think_l"), (b2(13.7), "finger_up")], [(0, "think"), (b2(13.7), "confident")],
         appear=b2(0.2), look=-1)


def s13(c, t):  # b2 16.64 - 31.52  1. dívida cara: rotativo 444,9% a.a.
    tip(c, t, b2(16.7), 1, "Dívida cara", (1, 0.8, 0.76))
    show(c, t, b2(19.6), 560, 480, sc(card, RED, s=1.6), anim="drop")
    show(c, t, b2(20.6), 560, 690, T("a mais cara do Brasil", 48, RED), anim="up")
    show(c, t, b2(25.9), 1230, 330, M("rotativo do cartão", 58, NAVY), anim="up")
    show(c, t, b2(27.5), 1230, 500, lambda c: text(c, "444,9% ao ano", 0, 0, 108, MARKER, RED), anim="stamp")
    show(c, t, b2(24.1), 1230, 630, T("juro médio, Banco Central, agosto de 2026", 40, DGRAY), anim="fade")
    hero(c, t, 1100, 1040, 0.65, [(0, "stand"), (b2(27.5), "head")], [(0, "worried"), (b2(27.5), "shocked")], appear=b2(16.8), look=0)


def s14(c, t):  # b2 31.52 - 43.24  15% ao mês; parcelado 192% a.a. (9% ao mês)
    show(c, t, b2(31.6), 560, 200, M("rotativo", 56, NAVY), anim="up")
    show(c, t, b2(32.2), 560, 360, lambda c: hl(c, "~15% ao mês", 0, 0, 80, (1, 0.8, 0.76)), anim="stamp")
    show(c, t, b2(34.3), 1360, 200, M("parcelado da fatura", 56, NAVY), anim="up")
    show(c, t, b2(36.1), 1360, 290, T("(depois de 1 mês no rotativo)", 40, DGRAY), anim="fade")
    show(c, t, b2(39.3), 1360, 420, M("192% ao ano", 72, RED), anim="pop")
    show(c, t, b2(41.6), 1360, 560, lambda c: hl(c, "~9% ao mês", 0, 0, 72, (1, 0.8, 0.76)), anim="stamp")
    show(c, t, b2(32.0), 560, 600, sc(card, RED, s=1.0))
    hero(c, t, 960, 1040, 0.85, [(0, "shrug")], [(0, "desperate")], appear=b2(31.6), look=0)


def s15(c, t):  # b2 43.24 - 62.72  compara com a Selic
    title(c, t, b2(43.3), "Compara com um investimento seguro", y=110, size=58)
    base = 900
    money_bar(c, t, b2(45.8), 1560, base, 40, 170, GREEN, "~1%", "Selic / mês", 0.6)
    show(c, t, b2(46.8), 1560, 300, group(M("Selic 13,75% a.a.", 46, GREEN), at(0, 60, T("pouco mais de 1% ao mês", 40, DGRAY))))
    money_bar(c, t, b2(53.3), 470, base, 600, 170, RED, "15%", "rotativo / mês")
    money_bar(c, t, b2(54.0), 790, base, 360, 170, ORANGE, "9%", "parcelado / mês")
    show(c, t, b2(59.2), 1370, 620, lambda c: hl(c, "nenhum investimento seguro paga isso", 0, 0, 40, LYELLOW), anim="stamp")
    hero(c, t, 200, 1030, 0.6, [(0, "point_r"), (b2(59.2), "finger_up")], [(0, "neutral"), (b2(59.2), "confident")],
         appear=b2(43.3), look=1)


def s16(c, t):  # b2 62.72 - 70.84  quase 9x e 14x
    show(c, t, b2(62.8), 960, 150, M("Quitar a dívida rende...", 64, NAVY), anim="up")
    show(c, t, b2(65.1), 620, 450, lambda c: text(c, "~9x", 0, 0, 190, MARKER, ORANGE), anim="stamp")
    show(c, t, b2(65.6), 620, 620, T("parcelado x Tesouro Selic", 46, DGRAY), anim="fade")
    show(c, t, b2(69.3), 1300, 450, lambda c: text(c, "14x", 0, 0, 190, MARKER, RED), anim="stamp")
    show(c, t, b2(69.6), 1300, 620, T("rotativo x Tesouro Selic", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1050, 0.7, [(0, "present"), (b2(69.3), "arms_up")], [(0, "happy"), (b2(69.3), "grin")], appear=b2(62.8))


def s17(c, t):  # b2 70.84 - 84.72  R$ 2.750 no parcelado: R$ 250 de juros no 1º mês
    show(c, t, b2(70.9), 480, 140, lv("dívida de", "R$ 2.750", 54, 70, RED, INK, after="no parcelado"), anim="up")
    show(c, t, b2(71.5), 520, 520, sc(card, RED, s=1.3), anim="drop")
    show(c, t, b2(76.2), 1180, 380, T("só no primeiro mês:", 52, DGRAY), anim="up")
    show(c, t, b2(77.7), 1180, 530, lambda c: text(c, "~R$ 250 de juros", 0, 0, 96, MARKER, RED), anim="stamp")
    show(c, t, b2(80.8), 1180, 720, L("quase o desconto do INSS da Ana...", 48), anim="fade")
    show(c, t, b2(82.8), 1180, 820, T("todo mês, indo embora", 52, RED), anim="up")
    hero(c, t, 300, 1030, 0.75, [(0, "stand"), (b2(77.7), "head")], [(0, "worried"), (b2(77.7), "desperate")], appear=b2(70.9), look=1)


def s18(c, t):  # b2 84.72 - 100.12  a lei limita: no máximo dobra
    title(c, t, b2(84.8), "Desde 2024, a lei limita", y=110, size=62)
    show(c, t, b2(86.3), 330, 480, sc(document, "LEI", NAVY, 40, s=1.1), anim="drop")
    show(c, t, b2(87.2), 560, 330, L("juros e encargos do rotativo e do parcelado", 46), anim="left")
    show(c, t, b2(90.2), 560, 420, L("não passam do valor da dívida", 52, NAVY), anim="left")
    show(c, t, b2(92.7), 1000, 560, lambda c: hl(c, "no máximo, dobra", 0, 0, 62, LYELLOW), anim="stamp")
    show(c, t, b2(96.6), 900, 780, M("R$ 2.750", 72, NAVY), anim="left")
    arrow_draw(c, t, b2(97.6), 1080, 780, 1240, 780)
    show(c, t, b2(98.4), 1440, 780, M("R$ 5.500", 80, RED), anim="stamp")
    show(c, t, b2(95.0), 1440, 900, T("já é um desastre", 46, RED), anim="up")
    hero(c, t, 1740, 1050, 0.55, [(0, "think_l"), (b2(95.0), "head")], [(0, "think"), (b2(95.0), "shocked")], appear=b2(84.9), look=-1)


def s19(c, t):  # b2 100.12 - 116.48  quitar a dívida é o melhor investimento; peça desconto
    show(c, t, b2(100.2), 960, 140, L("tem dívida no cartão ou no cheque especial?", 56), anim="up")
    show(c, t, b2(103.8), 960, 300, lambda c: hl(c, "o melhor investimento do 13º é quitar", 0, 0, 62, LGREEN), anim="stamp")
    show(c, t, b2(108.2), 960, 470, M("dica:", 58, GOLD), anim="pop")
    show(c, t, b2(110.6), 1200, 650, lambda c: speech(c, 640, 200, -260, 120), anim="pop")
    show(c, t, b2(111.0), 1200, 650, T("tem desconto pra quitar à vista?", 46), anim="fade")
    show(c, t, b2(113.9), 900, 880, group(sc(bills, 2, s=0.6), at(110, 0, L("dinheiro na mão = negocia melhor", 46))), anim="left")
    hero(c, t, 420, 1040, 0.95, [(0, "stand"), (b2(103.8), "thumb"), (b2(110.6), "point_r")],
         [(0, "neutral"), (b2(103.8), "confident"), (b2(110.6), "happy")], appear=b2(100.2), look=1)


def s20(c, t):  # b2 116.48 - 136.51  2. reserva: sem ela, o imprevisto vai pro cartão
    tip(c, t, b2(116.5), 2, "Reserva de emergência", LGREEN)
    show(c, t, b2(119.8), 960, 260, T("por que antes de investir?", 52, DGRAY), anim="up")
    shocks = [(b2(125.5), sc(wrench_tire, s=0.7), "o carro quebra"), (b2(126.6), sc(qmark, 90, INK), "o celular cai"),
              (b2(128.2), sc(exclaim, 90), "dentista")]
    for i, (t0, fn, lab) in enumerate(shocks):
        y = 420 + i * 170
        show(c, t, t0, 420, y, fn)
        show(c, t, t0 + 0.1, 640, y, L(lab, 46), anim="left")
    arrow_draw(c, t, b2(131.0), 960, 590, 1180, 590)
    show(c, t, b2(131.4), 1400, 560, sc(card, RED, s=1.0), anim="drop")
    show(c, t, b2(131.6), 1400, 700, M("parcela", 52, RED), anim="up")
    show(c, t, b2(134.4), 1400, 830, lambda c: hl(c, "~9% ao mês", 0, 0, 56, (1, 0.8, 0.76)), anim="stamp")
    hero(c, t, 1740, 1050, 0.55, [(0, "think_l"), (b2(125.5), "shrug")], [(0, "think"), (b2(125.5), "worried")], appear=b2(116.6), look=-1)


def s21(c, t):  # b2 136.51 - 154.28  onde guardar e quanto rende
    title(c, t, b2(136.6), "Onde fica a reserva", y=110, size=62)
    show(c, t, b2(137.9), 960, 210, T("seguro e com saque a qualquer hora", 48, DGRAY), anim="up")
    show(c, t, b2(141.0), 600, 340, lambda c: hl(c, "Tesouro Selic", 0, 0, 56, LGREEN), anim="stamp")
    show(c, t, b2(142.4), 1320, 340, lambda c: hl(c, "CDB de liquidez diária", 0, 0, 52, LGREEN), anim="stamp")
    show(c, t, b2(144.9), 1320, 430, T("pagando pelo menos 100% do CDI", 42, DGRAY), anim="fade")
    show(c, t, b2(146.7), 560, 650, group(sc(piggy, s=0.8), at(0, 140, M("R$ 2.750", 52, NAVY))), anim="drop")
    show(c, t, b2(149.1), 960, 650, group(sc(calendar, "1", NAVY, 60, s=0.7), at(0, 110, T("1 ano", 42))))
    arrow_draw(c, t, b2(149.6), 1100, 650, 1240, 650)
    show(c, t, b2(150.9), 1460, 640, M("+ R$ 310", 84, GREEN), anim="stamp")
    show(c, t, b2(152.8), 1460, 740, T("já sem o imposto", 42, DGRAY), anim="fade")
    hero(c, t, 230, 1040, 0.6, [(0, "present")], [(0, "happy")], appear=b2(136.7), look=1)


def s22(c, t):  # b2 154.28 - 309.539  acima da inflação, dormir tranquilo, meta de 3 a 6 meses
    show(c, t, b2(154.4), 600, 250, lv("tirando a inflação:", "+ R$ 185", 50, 70, GREEN), anim="left")
    show(c, t, b2(158.3), 560, 430, group(sc(x_icon, 32), at(50, 0, L("não é pra ficar rico", 50))), anim="left")
    show(c, t, b2(159.9), 560, 540, group(sc(check_icon, 32), at(50, 0, L("é pra dormir tranquilo", 50, GREEN))), anim="left")
    show(c, t, b2(160.2), 1500, 420, sc(shield, GREEN, s=1.2), anim="pop")
    show(c, t, b2(162.5), 960, 720, lambda c: hl(c, "meta: 3 a 6 meses dos seus gastos", 0, 0, 58, LYELLOW), anim="stamp")
    show(c, t, b2(167.3), 960, 860, T("o 13º é um ótimo jeito de começar ou completar", 48, NAVY), anim="up")
    hero(c, t, 1720, 1050, 0.55, [(0, "relax"), (b2(162.5), "finger_up")], [(0, "happy"), (b2(162.5), "confident")],
         appear=b2(154.4), look=-1)


# ======================================================================= BLOCO 3
def s23(c, t):  # b3 0 - 11.28  3. investir: o 13º vem todo ano
    tip(c, t, b3(0.1), 3, "Investir pro longo prazo", LBLUE)
    show(c, t, b3(1.9), 560, 600, sc(tree, 1.0, s=0.6), anim="pop")
    show(c, t, b3(6.5), 1250, 330, T("o tamanho do 13º...", 52, DGRAY), anim="up")
    for i, yr in enumerate(("2026", "2027", "2028", "2029")):
        show(c, t, b3(9.5) + 0.25 * i, 980 + i * 190, 560, group(sc(calendar, "13º", GREEN, 50, s=0.6), at(0, 110, T(yr, 38, DGRAY))))
    show(c, t, b3(10.0), 1250, 780, M("ele vem todo ano", 64, GREEN), anim="up")
    hero(c, t, 230, 1040, 0.6, [(0, "present")], [(0, "happy")], appear=b3(0.2), look=1)


def s24(c, t):  # b3 11.28 - 31.92  Ana x Bruno; Bruno gasta tudo
    show(c, t, b3(11.3), 960, 120, lambda c: (text(c, "Ana", -170, 0, 72, MARKER, PURPLE), text(c, "x", 0, 0, 64, MARKER, GOLD), text(c, "Bruno", 190, 0, 72, MARKER, ORANGE)), anim="up")
    ana(c, t, 420, 1010, 1.0, [(0, "stand"), (b3(13.7), "wave")], [(0, "happy")], appear=b3(12.0), look=1)
    bruno(c, t, 1560, 1010, 1.0, [(0, "stand"), (b3(25.9), "arms_up")], [(0, "happy"), (b3(25.9), "grin")], appear=b3(13.0), look=-1)
    show(c, t, b3(14.4), 760, 280, T("25 anos", 50), anim="fade")
    show(c, t, b3(15.7), 760, 370, T("R$ 3.000 por mês", 50), anim="fade")
    show(c, t, b3(20.2), 600, 470, lv("13º:", "R$ 2.750", 48, 58, GREEN, DGRAY), anim="fade")
    if t > b3(25.9):
        show(c, t, b3(26.8), 1400, 260, M("gasta tudo em dezembro", 46, RED), anim="up")
        show(c, t, b3(27.6), 1230, 390, group(sc(cart, s=0.5), at(0, 80, T("presentes", 38))))
        show(c, t, b3(28.5), 1460, 400, T("viagem", 44), anim="pop")
        show(c, t, b3(29.7), 1680, 390, group(sc(card, s=0.45), at(0, 70, T("parcelas", 36))))
        show(c, t, b3(31.2), 1100, 640, lambda c: hl(c, "todo ano", 0, 0, 52, (1, 0.8, 0.76)), anim="stamp")


def s25(c, t):  # b3 31.92 - 51.44  Ana: dívida zero, reserva ok, investe o 13º inteiro a 5% real
    title(c, t, b3(32.0), "E a Ana?", y=110, size=64)
    ana(c, t, 280, 1010, 1.05, [(0, "present"), (b3(40.2), "point_r")], [(0, "happy"), (b3(40.2), "confident")],
        appear=b3(32.0), look=1)
    show(c, t, b3(32.6), 720, 260, group(sc(check_icon, 32), at(50, 0, L("cartão quitado", 50))), anim="left")
    show(c, t, b3(34.3), 1240, 260, group(sc(check_icon, 32), at(50, 0, L("reserva pronta", 50))), anim="left")
    show(c, t, b3(35.7), 1160, 420, M("investe o 13º inteiro, todo ano", 58, NAVY), anim="up")
    show(c, t, b3(40.2), 1160, 570, lambda c: hl(c, "~5% ao ano acima da inflação", 0, 0, 58, LGREEN), anim="stamp")
    show(c, t, b3(43.1), 1160, 660, T("já descontado o imposto", 42, DGRAY), anim="fade")
    show(c, t, b3(45.8), 1160, 780, L("aporte corrigido pela inflação", 46), anim="fade")
    show(c, t, b3(48.5), 1160, 880, lambda c: hl(c, "valores em dinheiro de hoje", 0, 0, 46, LYELLOW), anim="stamp")


def s26(c, t):  # b3 51.44 - 69.04  10, 20 e 30 anos
    title(c, t, b3(51.5), "Só com o 13º:", y=110, size=64)
    base = 880
    money_bar(c, t, b3(52.0), 760, base, 115, 200, GREEN, "R$ 34 mil", "10 anos")
    money_bar(c, t, b3(55.9), 1110, base, 300, 200, GREEN, "R$ 91 mil", "20 anos")
    money_bar(c, t, b3(59.1), 1460, base, 600, 200, GREEN, "R$ 183 mil", "30 anos")
    show(c, t, b3(60.2), 1460, 995, T("(aos 55 anos)", 36, DGRAY), anim="fade")
    show(c, t, b3(66.6), 400, 300, lambda c: hl(c, "sem mexer no salário", 0, 0, 50, LYELLOW), anim="stamp")
    ana(c, t, 330, 1010, 0.95, [(0, "point_r"), (b3(62.4), "arms_up")], [(0, "happy"), (b3(62.4), "grin")], appear=b3(51.5), look=1)


def s27(c, t):  # b3 69.04 - 75.0  colocou 82,5 mil; juros 100 mil
    show(c, t, b3(69.1), 620, 140, lv("dos", "R$ 183 mil", 56, 70, GREEN, INK, after="da Ana:"), anim="up")
    k1, k2 = grow(t, b3(70.0), 0.8), grow(t, b3(72.6), 0.9)
    x0, y0, w = 360, 420, 1200
    if t > b3(70.0):
        rrect(c, x0, y0, w * 0.45 * k1, 160, 18); fs(c, LBLUE, 6)
        if k1 > 0.7:
            text(c, "R$ 82,5 mil", x0 + w * 0.225, y0 + 80, 54, MARKER, NAVY)
            text(c, "ela colocou", x0 + w * 0.225, y0 + 220, 44, HAND, DGRAY)
    if t > b3(72.6):
        rrect(c, x0 + w * 0.45, y0, w * 0.55 * k2, 160, 18); fs(c, LGREEN, 6)
        if k2 > 0.7:
            text(c, "R$ 100 mil", x0 + w * 0.725, y0 + 80, 54, MARKER, GREEN)
            text(c, "vieram dos juros", x0 + w * 0.725, y0 + 220, 44, HAND, DGRAY)
    hero(c, t, 960, 1050, 0.6, [(0, "present"), (b3(73.0), "thumb")], [(0, "happy"), (b3(73.0), "grin")], appear=b3(69.1))


def s28(c, t):  # b3 75.0 - 92.64  e o Bruno? / renda de R$ 600 por mês
    title(c, t, b3(75.0), "E o Bruno?", y=110, size=64)
    bruno(c, t, 380, 1010, 1.0, [(0, "stand"), (b3(80.8), "shrug")], [(0, "neutral"), (b3(80.8), "sad")], appear=b3(75.1), look=1)
    show(c, t, b3(78.6), 380, 400, lambda c: thought(c, 420, 190, -60, 130), anim="pop")
    show(c, t, b3(78.9), 380, 400, T("lembranças de dezembro", 40), anim="fade")
    show(c, t, b3(81.4), 680, 640, M("R$ 0", 80, RED), anim="stamp")
    ana(c, t, 1560, 1010, 1.0, [(0, "stand"), (b3(87.6), "present_l")], [(0, "happy"), (b3(87.6), "grin")], appear=b3(80.9), look=-1)
    show(c, t, b3(82.0), 1560, 440, M("R$ 183 mil", 64, GREEN), anim="stamp")
    show(c, t, b3(85.2), 980, 380, T("regra dos 4%:", 48, DGRAY), anim="up")
    show(c, t, b3(88.2), 980, 520, lambda c: text(c, "~R$ 600/mês", 0, 0, 72, MARKER, GREEN), anim="stamp")
    show(c, t, b3(90.3), 980, 620, T("pra sempre, corrigido pela inflação", 40, DGRAY), anim="fade")


def s29(c, t):  # b3 92.64 - 95.76  um 14º salário
    show(c, t, b3(92.7), 1060, 420, lambda c: text(c, "um 14º salário", 0, 0, 120, MARKER, GREEN), anim="stamp")
    show(c, t, b3(94.9), 1060, 580, lambda c: hl(c, "todo mês", 0, 0, 70, LGREEN), anim="stamp")
    ana(c, t, 360, 1010, 1.05, [(0, "arms_up")], [(0, "grin")], appear=b3(92.7), look=1)


def s30(c, t):  # b3 95.76 - 107.28  80% investe, 20% curte: R$ 146 mil
    title(c, t, b3(95.8), "E aproveitar o fim de ano?", y=110, size=62)
    if t > b3(100.6):
        c.save(); c.translate(620, 560)
        donut(c, 0.8 * grow(t, b3(100.6), 1.0), 200, 80, GREEN)
        c.restore()
        text(c, "80%", 620, 560, 70, MARKER, GREEN)
    show(c, t, b3(100.8), 1250, 380, group(sc(check_icon, 30), at(50, 0, L("80% investe", 54, GREEN))), anim="left")
    show(c, t, b3(101.9), 1250, 500, group(sc(sparkle, 30, GOLD), at(50, 0, L("20% pra curtir", 54, GOLD))), anim="left")
    show(c, t, b3(103.6), 1000, 700, lv("em 30 anos:", "R$ 146 mil", 50, 72, GREEN), anim="left")
    hero(c, t, 1740, 1050, 0.55, [(0, "think_l"), (b3(103.6), "thumb")], [(0, "think"), (b3(103.6), "happy")], appear=b3(95.9), look=-1)


def s31(c, t):  # b3 107.28 - 423.701  curtir não é problema; gastar tudo é
    show(c, t, b3(107.4), 960, 330, group(sc(check_icon, 40), at(64, 0, L("curtir uma parte: tudo bem", 62, GREEN))), anim="left")
    show(c, t, b3(109.4), 960, 520, group(sc(x_icon, 40), at(64, 0, L("gastar tudo, todo ano, sem perceber", 62, RED))), anim="left")
    hero(c, t, 400, 1040, 0.9, [(0, "thumb"), (b3(109.4), "finger_up")], [(0, "happy"), (b3(109.4), "confident")], appear=b3(107.4), look=1)


# ======================================================================= BLOCO 4
def s32(c, t):  # b4 0 - 16.16  a armadilha: janeiro
    show(c, t, b4(0.5), 960, 130, lambda c: ribbon(c, "A ARMADILHA", RED, 60), anim="stamp")
    show(c, t, b4(3.8), 420, 480, group(sc(calendar, "JAN", RED, 64, s=1.3), at(0, 190, M("o mês mais caro", 48, RED))), anim="drop")
    docs = [(b4(8.1), "IPVA"), (b4(9.3), "IPTU"), (b4(10.4), "MATRÍC."), (b4(11.4), "ESCOLA")]
    for i, (t0, lab) in enumerate(docs):
        show(c, t, t0, 860 + i * 250, 420, sc(document, lab, RED, 26 if len(lab) > 5 else 34, s=1.0), anim="drop")
    show(c, t, b4(13.4), 860, 680, group(sc(card, s=0.6), at(110, 0, L("faturas da Black Friday e do Natal", 44))), anim="left")
    hero(c, t, 1720, 1050, 0.5, [(0, "stand"), (b4(8.1), "head")], [(0, "worried"), (b4(8.1), "desperate")], appear=b4(0.6), look=-1)


def s33(c, t):  # b4 16.16 - 27.2  gastou tudo → cheque especial/rotativo → 15% ao mês
    steps = [(b4(16.3), "gastou tudo em dezembro", NAVY), (b4(18.9), "janeiro sem dinheiro", ORANGE),
             (b4(21.6), "cheque especial ou rotativo", RED)]
    for i, (t0, lab, col) in enumerate(steps):
        y = 200 + i * 150
        show(c, t, t0, 960, y, M(lab, 52, col), anim="up")
        if i < 2:
            arrow_draw(c, t, t0 + 1.0, 960, y + 40, 960, y + 105)
    show(c, t, b4(24.0), 960, 640, lambda c: hl(c, "começa o ano pagando ~15% ao mês", 0, 0, 62, (1, 0.8, 0.76)), anim="stamp")
    hero(c, t, 960, 1050, 0.5, [(0, "shrug"), (b4(24.0), "head")], [(0, "worried"), (b4(24.0), "desperate")], appear=b4(16.3))


def s34(c, t):  # b4 27.2 - 36.48  separe as contas de janeiro
    show(c, t, b4(28.9), 960, 150, M("antes de tudo: separe as contas de janeiro", 60, NAVY), anim="up")
    show(c, t, b4(30.1), 820, 520, sc(envelope, s=1.6), anim="drop")
    show(c, t, b4(30.6), 820, 700, T("JANEIRO", 52, NAVY), anim="fade")
    show(c, t, b4(35.0), 1380, 520, lambda c: hl(c, "esse dinheiro já tem dono", 0, 0, 58, LYELLOW), anim="stamp")
    hero(c, t, 300, 1030, 0.8, [(0, "present"), (b4(35.0), "thumb")], [(0, "confident"), (b4(35.0), "happy")], appear=b4(27.3), look=1)


def s35(c, t):  # b4 36.48 - 62.0  recapitulando a ordem
    title(c, t, b4(36.5), "A ordem", y=110, size=66)
    rows = [(b4(38.6), "calcule quanto cai de verdade"), (b4(44.5), "separe as contas de janeiro"),
            (b4(47.3), "quite as dívidas caras"), (b4(52.6), "monte ou complete a reserva"),
            (b4(57.6), "invista e curta uma parte sem culpa")]
    for i, (t0, lab) in enumerate(rows):
        y = 250 + i * 150
        show(c, t, t0, 470, y, lambda c, n=i + 1: hl(c, str(n), 0, 0, 56, LYELLOW), anim="stamp")
        show(c, t, t0 + 0.1, 560, y, L(lab, 56), anim="left")
    hero(c, t, 1700, 1050, 0.6, [(0, "present_l"), (b4(57.6), "thumb")], [(0, "happy"), (b4(57.6), "grin")], appear=b4(36.6), look=-1)


def s36(c, t):  # b4 62.0 - 71.72  conteúdo educativo; refaça a conta
    show(c, t, b4(62.1), 960, 300, M("conteúdo educativo", 66, NAVY), anim="up")
    show(c, t, b4(64.7), 960, 420, T("não é recomendação de nenhum investimento", 50, DGRAY), anim="fade")
    show(c, t, b4(67.6), 680, 680, sc(calculator, "%", s=0.9), anim="pop")
    show(c, t, b4(68.9), 800, 680, L("refaça a conta com os seus números", 50), anim="left")
    hero(c, t, 300, 1030, 0.75, [(0, "stand"), (b4(67.6), "point_r")], [(0, "neutral"), (b4(67.6), "happy")], appear=b4(62.2), look=1,
         prop=("l", prop_calculator))


def s37(c, t):  # b4 71.72 - 76.92  comentários
    show(c, t, b4(71.8), 1080, 400, lambda c: speech(c, 960, 280, -350, 180), anim="pop")
    show(c, t, b4(72.0), 1080, 340, T("Me conta nos comentários:", 52, DGRAY), anim="fade")
    show(c, t, b4(74.5), 1080, 440, M("o que você vai fazer com o seu 13º?", 46, NAVY), anim="fade")
    hero(c, t, 340, 1010, 1.1, [(0, "wave")], [(0, "happy")], appear=b4(71.8), look=1)


def s38(c, t):  # b4 76.92 - 83.28  vídeo dos 100 mil
    show(c, t, b4(77.0), 960, 140, T("quer juntar os primeiros R$ 100 mil?", 56), anim="up")
    show(c, t, b4(81.6), 1180, 540, lambda c: video_card(c, "Juntar R$ 100 mil", "quanto tempo leva?",
                                                       icon=lambda c: play_btn(c, 70)), anim="pop")
    hero(c, t, 400, 1010, 1.05, [(0, "think"), (b4(81.6), "point_r")], [(0, "think"), (b4(81.6), "happy")], appear=b4(77.0), look=1)


def s39(c, t):  # b4 83.28 - 510.872  assinatura
    show(c, t, b4(83.3), 960, 300, lambda c: text(c, "FAZ A CONTA", 0, 0, 120, MARKER, NAVY), anim="stamp")
    show(c, t, b4(84.6), 960, 430, lambda c: hl(c, "a gente faz a conta", 0, 0, 60, LYELLOW))
    hero(c, t, 960, 1010, 1.0, [(0, "present"), (b4(86.2), "wave")], [(0, "happy"), (b4(86.2), "grin")], appear=b4(83.4))


def s40(c, t):  # 510.872 - fim (15 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres: vídeo à esquerda (x 170-950, y 300-740) e inscrever-se à direita (~1450, 520).
    show(c, t, 511.0, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, 511.3, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, 511.3, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (513.5, "relax")], [(0, "happy")], appear=511.0)


SCENES = [
    (0.0, 15.1, s01), (15.1, 26.2, s02), (26.2, 32.4, s03), (32.4, 46.7, s04), (46.7, 53.36, s05),
    (53.36, 62.0, s06), (62.0, 77.5, s07), (77.5, 98.6, s08), (98.6, 108.84, s09), (108.84, 124.24, s10),
    (124.24, O2, s11),
    (O2, b2(16.64), s12), (b2(16.64), b2(31.52), s13), (b2(31.52), b2(43.24), s14), (b2(43.24), b2(62.72), s15),
    (b2(62.72), b2(70.84), s16), (b2(70.84), b2(84.72), s17), (b2(84.72), b2(100.12), s18), (b2(100.12), b2(116.48), s19),
    (b2(116.48), b2(136.51), s20), (b2(136.51), b2(154.28), s21), (b2(154.28), O3, s22),
    (O3, b3(11.28), s23), (b3(11.28), b3(31.92), s24), (b3(31.92), b3(51.44), s25), (b3(51.44), b3(69.04), s26),
    (b3(69.04), b3(75.0), s27), (b3(75.0), b3(92.64), s28), (b3(92.64), b3(95.76), s29), (b3(95.76), b3(107.28), s30),
    (b3(107.28), O4, s31),
    (O4, b4(16.16), s32), (b4(16.16), b4(27.2), s33), (b4(27.2), b4(36.48), s34), (b4(36.48), b4(62.0), s35),
    (b4(62.0), b4(71.72), s36), (b4(71.72), b4(76.92), s37), (b4(76.92), b4(83.28), s38), (b4(83.28), 510.872, s39),
    (510.872, 999.0, s40),
]

# só toques pontuais, sem ruído: R$ 2.750 / 444,9% / 14x / R$ 183 mil
SFX = [(105.4, "tum"), (b2(27.5), "tum"), (b2(69.3), "tum"), (b3(62.4), "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key")
