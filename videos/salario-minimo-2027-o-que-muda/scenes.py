"""Salário mínimo 2027: o que muda além do salário. Só TikTok: vertical 1080x1920, ~77 s, ESTILO CADERNO.
Contas (contas.py): mínimo R$ 1.621 -> previsão R$ 1.741 (PLOA 2027; +R$ 120, 7,4%; valor final depende do INPC);
INSS 7,5%: R$ 121,58 -> R$ 130,58; líquido +R$ 111/mês, +R$ 1.443 no ano com o 13º; DAS do MEI 5% do mínimo: R$ 81,05 -> R$ 87,05 (+R$ 72/ano);
pisos atrelados: aposentadoria/pensão do INSS, BPC, seguro-desemprego, abono do PIS (até 1 mínimo).
Layout: título y~250, palco 360-1290 (pés em 1280), legendas ~1400-1460, nada em x > 930.
Quadro 0: o mínimo já contando de R$ 1.621 para R$ 1.741."""
from engine import *  # noqa

VERTICAL = True

CX = 420
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(2.9, "tum"), (19.7, "tum"), (39.8, "tum"), (52.3, "tum"), (75.0, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s.replace("2.", "2 .")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="l")


def MM(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


def HL(s, size=60, bg=LYELLOW, col=INK):
    return lambda c: hl(c, m(s), 0, 0, size, bg, col)


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def reais(c, t, t0, a, b, x, y, size, col, d=0.8, pre="R$ ", suf="", align="c", dec=0):
    v = a + (b - a) * ease_out(prog(t, t0, d))
    s = f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    text(c, m(pre + s + suf), x, y, size, MARKER, col, align=align)


def titulo(c, t, s):
    show(c, t, -1.0, 540, 250, lambda c: ribbon(c, s, NAVY, 56), anim="stamp", d=0.3)


def palco(c, t):
    floor(c)
    if t < 7.4:  # gancho
        titulo(c, t, "SALÁRIO MÍNIMO 2027")
        text(c, "salário mínimo", CX, 420, 54, HAND, DGRAY)
        reais(c, t, 0.0, 1621, 1741, CX, 560, 130, NAVY, d=3.2)
        show(c, t, 2.9, CX, 680, HL("+R$ 120", 80, LGREEN, GREEN), anim="stamp")
        for k, (t0, fn, lab) in enumerate(((4.7, lambda c: boleto(c, "DAS", ORANGE), "MEI"), (5.1, lambda c: bank(c), "aposentado"),
                                           (5.5, lambda c: card(c, GREEN), "abono PIS"))):
            x = 130 + k * 240
            show(c, t, t0, x, 890, sc(fn, s=0.55), anim="drop")
            show(c, t, t0 + 0.1, x, 1030, T(lab, 46, NAVY), anim="up")
        show(c, t, 6.6, CX, 1160, MM("olha a conta", 66, RED), anim="stamp")
        hero(c, t, 860, FY, 0.9, [(0, "point_l"), (4.6, "finger_up"), (6.6, "present_l")], [(0, "happy"), (4.6, "think"), (6.6, "confident")], look=-0.7)
    elif t < 19.6:
        titulo(c, t, "QUANTO VAI SER")
        show(c, t, 7.6, 120, 470, L("hoje", 56, DGRAY), anim="left", d=0.3)
        show(c, t, 8.2, 900, 480, lambda c: text(c, m("R$ 1.621"), 0, 0, 90, MARKER, INK, align="r"), anim="stamp")
        show(c, t, 10.1, 120, 610, L("previsão 2027", 56, DGRAY), anim="left", d=0.3)
        if t > 11.3:
            reais(c, t, 11.3, 1621, 1741, 900, 620, 90, GREEN, d=1.2, align="r")
        line(c, 100, 680, 920, 680, 5, LGRAY)
        show(c, t, 13.4, CX, 790, HL("+7,4%", 110, LGREEN, GREEN), anim="stamp")
        show(c, t, 16.2, CX, 950, T("valor final depende", 54, DGRAY), anim="up")
        show(c, t, 17.4, CX, 1030, T("da inflação, que sai em", 54, DGRAY), anim="up")
        show(c, t, 18.8, CX, 1175, sc(calendar, "DEZ", RED, 48, s=0.8), anim="pop")
        hero(c, t, 860, FY, 0.85, [(0, "present_l"), (13.4, "thumb"), (16.2, "finger_up")], [(0, "confident"), (13.4, "happy"), (16.2, "think")], look=-0.7)
    elif t < 34.0:
        titulo(c, t, "QUEM GANHA O MÍNIMO")
        show(c, t, 20.3, CX, 440, T("desconto do INSS (7,5%)", 54, DGRAY), anim="up")
        show(c, t, 23.3, 230, 560, MM("R$ 121", 84, GRAY), anim="stamp")
        if t > 23.8:
            arrow_draw(c, t, 23.8, 370, 550, 480, 550, d=0.3)
        show(c, t, 24.4, 620, 560, MM("R$ 130", 84, RED), anim="stamp")
        show(c, t, 25.8, CX, 700, T("no bolso, por mês", 56, DGRAY), anim="up")
        if t > 27.6:
            reais(c, t, 27.6, 0, 111, CX, 840, 130, GREEN, d=0.9, pre="+R$ ")
        show(c, t, 30.2, CX, 980, T("contando o 13º, no ano", 56, DGRAY), anim="up")
        if t > 31.7:
            show(c, t, 31.7, CX, 1110, HL("+R$ 1.443", 100, LGREEN, GREEN), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "finger_up"), (23.3, "present_l"), (27.6, "thumb"), (31.7, "arms_up")],
             [(0, "confident"), (23.3, "worried"), (27.6, "happy"), (31.7, "grin")], look=-0.7)
    elif t < 39.7:
        titulo(c, t, "ATENÇÃO")
        show(c, t, 34.6, CX, 460, T("o aumento vale em", 56, DGRAY), anim="up")
        show(c, t, 35.8, 220, 650, sc(calendar, "JAN", BLUE, 52, s=1.3), anim="pop")
        show(c, t, 36.6, 620, 650, sc(calendar, "FEV", GREEN, 52, s=1.3), anim="pop")
        if t > 36.6:
            arrow_draw(c, t, 36.6, 330, 650, 500, 650, d=0.4)
        show(c, t, 36.8, CX, 870, T("mas só aparece no salário", 54, DGRAY), anim="up")
        show(c, t, 38.2, CX, 990, HL("PAGO EM FEVEREIRO", 58, LYELLOW), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "finger_up"), (36.6, "present_l")], [(0, "think"), (38.2, "confident")], look=-0.7)
    elif t < 52.2:
        titulo(c, t, "A VIRADA: MEI")
        show(c, t, 41.4, 190, 520, sc(boleto, "DAS", ORANGE, s=0.75), anim="drop")
        show(c, t, 42.0, 380, 470, L("5% do mínimo", 60, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 43.5, 380, 550, L("pro INSS", 52, DGRAY), anim="left", d=0.3)
        show(c, t, 46.4, 250, 760, MM("R$ 81", 96, GRAY), anim="stamp")
        if t > 47.4:
            arrow_draw(c, t, 47.4, 380, 745, 480, 745, d=0.3)
        show(c, t, 48.0, 620, 760, MM("~R$ 87", 96, RED), anim="stamp")
        show(c, t, 49.1, CX, 920, HL("+R$ 6 por mês", 70, PINKISH, RED), anim="stamp")
        show(c, t, 50.6, CX, 1050, MM("R$ 72 no ano", 70, RED), anim="up")
        hero(c, t, 860, FY, 0.85, [(0, "finger_up"), (41.4, "point_l"), (49.1, "shrug")], [(0, "confident"), (46.4, "think"), (49.1, "worried")], look=-0.7)
    elif t < 65.5:
        titulo(c, t, "SOBE JUNTO")
        show(c, t, 53.0, CX, 430, T("nada disso pode ser menor que 1 mínimo", 46, DGRAY), anim="up")
        itens = ((56.2, "aposentadoria e pensão (piso)"), (59.4, "BPC"), (60.4, "seguro-desemprego"), (61.7, "abono do PIS"))
        for k, (t0, s) in enumerate(itens):
            y = 540 + k * 95
            show(c, t, t0, 120, y, sc(check_icon, 30), anim="pop")
            show(c, t, t0, 175, y + 20, L(s, 54, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 63.0, CX, 980, T("piso de", 56, DGRAY), anim="up")
        show(c, t, 63.6, CX, 1110, HL("R$ 1.741", 110, LGREEN, GREEN), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "present_l"), (56.2, "point_l"), (63.6, "thumb")], [(0, "confident"), (63.6, "happy")], look=-0.7)
    elif t < 71.6:
        titulo(c, t, "GANHA MAIS?")
        show(c, t, 66.2, CX, 520, MM("R$ 3.000, R$ 5.000...", 64, NAVY), anim="stamp")
        show(c, t, 67.5, CX, 660, T("o seu reajuste depende do", 56, DGRAY), anim="up")
        show(c, t, 68.6, CX, 790, HL("ACORDO DA CATEGORIA", 66, LYELLOW), anim="stamp")
        show(c, t, 70.4, CX, 930, MM("não desse número", 58, RED), anim="up")
        hero(c, t, 860, FY, 0.85, [(0, "finger_up"), (68.6, "present_l")], [(0, "think"), (68.6, "confident")], look=-0.7)
    else:
        titulo(c, t, "E VOCÊ?")
        for k, (t0, s, col) in enumerate(((72.3, "MÍNIMO", NAVY), (73.1, "MEI", ORANGE), (73.7, "APOSENTADO", GREEN))):
            show(c, t, t0, CX, 480 + k * 120, MM(s + ("?" if k == 2 else ","), 80, col), anim="stamp")
        show(c, t, 74.7, 170, 1000, sc(phone, s=0.9), anim="pop")
        show(c, t, 75.0, 440, 1000, HL("COMENTA AÍ", 64, LYELLOW), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "point_l")], [(0, "happy"), (75.0, "grin")], look=-0.7)


SCENES = [(0, 999.0, palco)]
