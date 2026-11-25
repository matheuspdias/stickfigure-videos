"""Janeiro de 2027: a dívida que já vem todo ano. Só TikTok (extra pedido pelo Matheus em 25/11/2026): vertical 1080x1920, ~72,7 s, ESTILO CADERNO.
Exemplo (contas.py): salário R$ 3 mil, carro de R$ 40 mil em SP (IPVA 4% = R$ 1.600; 2027: -3% em janeiro ou 5x), IPTU ~R$ 1.000,
material ~R$ 500 por filho (estimativa; Procon-SP: mesmo item varia até ~270%), fatura do Natal/Black Friday ~R$ 1.000. Total R$ 4.100.
2ª parcela do 13º de R$ 3 mil ~R$ 1.251. Layout: título y~250, palco 360-1290 (pés em 1280), legendas ~1400-1460, nada em x > 930.
Quadro 0: boletos já caindo no calendário de janeiro e a dívida contando."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(6.9, "tum"), (34.6, "tum"), (46.0, "tum"), (72.0, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s.replace("2.", "2 .")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="l")


def R(s, size=56, col=RED):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col, align="r")


def MM(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


def HL(s, size=60, bg=LYELLOW, col=INK):
    return lambda c: hl(c, m(s), 0, 0, size, bg, col)


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def reais(c, t, t0, a, b, x, y, size, col, d=0.8, pre="R$ ", align="c"):
    v = a + (b - a) * ease_out(prog(t, t0, d))
    s = f"{v:,.0f}".replace(",", ".")
    text(c, m(pre + s), x, y, size, MARKER, col, align=align)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.1  gancho
    floor(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "JANEIRO DE 2027", NAVY, 60), anim="stamp", d=0.3)
    show(c, t, -1.0, 190, 520, sc(calendar, "JAN", RED, 60, s=1.4), anim="pop")
    for i, (tit, col) in enumerate((("IPVA", RED), ("IPTU", ORANGE), ("ESCOLA", BLUE), ("FATURA", PURPLE))):
        show(c, t, -0.6 + i * 0.6, 430 + i * 130, 520 - i * 18, sc(boleto, tit, col, s=0.55), anim="drop")
    show(c, t, 3.4, CX, 740, T("você, trabalhador, já deve", 56, DGRAY), anim="up")
    if t > 5.0:
        reais(c, t, 5.0, 0, 4000, 420, 880, 120, RED, d=1.1, pre="~R$ ")
    show(c, t, 6.9, 420, 1020, HL("CUIDADO!", 84, PINKISH, RED), anim="stamp")
    show(c, t, 7.6, 420, 1140, T("a conta que vem todo ano", 52, NAVY), anim="up")
    hero(c, t, 880, FY, 0.75, [(0, "present_l"), (6.9, "head")], [(0, "worried"), (6.9, "shocked")], look=-0.8)


ITENS = [  # (t_entra, icone, titulo, t_sub, sub, t_val, valor, v)
    (9.1, lambda c: car(c, BLUE), "IPVA", 10.6, "carro de R$ 40 mil x 4% (SP)", 14.0, "R$ 1.600", 1600),
    (15.6, lambda c: house(c), "IPTU", 17.2, "casa simples", 18.3, "~R$ 1.000", 1000),
    (19.5, lambda c: pencil(c), "MATERIAL", 21.6, "escolar, lista básica, por filho", 22.7, "~R$ 500", 500),
    (28.6, lambda c: card(c, PURPLE), "FATURA", 29.9, "de janeiro: Natal + Black Friday", 32.4, "~R$ 1.000", 1000),
]


def s02(c, t):  # 9.1 - 33.7  a lista de janeiro
    floor(c)
    show(c, t, 9.2, CX, 250, lambda c: ribbon(c, "O QUE VEM EM JANEIRO", NAVY, 56), anim="stamp")
    total_ant, total = 0, 0
    for i, (t0, ic, tit, ts, sub, tv, val, v) in enumerate(ITENS):
        y = 400 + i * 150
        if t < t0:
            continue
        show(c, t, t0, 120, y + 10, sc(ic, s=0.5), anim="pop")
        show(c, t, t0 + 0.2, 220, y, L(tit, 54, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, ts, 220, y + 55, L(sub, 40, DGRAY), anim="up")
        show(c, t, tv, 920, y + 10, R(val, 58, RED), anim="stamp")
        if t >= tv:
            total_ant, total = total, total + v
            t_ult = tv
        line(c, 60, y + 85, 1020, y + 85, 3, LGRAY)
    if 24.6 <= t < 28.6:
        show(c, t, 24.6, 400, 1000, T("o mesmo item custa", 50, DGRAY), anim="up")
        show(c, t, 26.0, 400, 1100, HL("ATÉ 3x MAIS", 70, PINKISH, RED), anim="stamp")
        show(c, t, 27.1, 400, 1190, T("de uma papelaria pra outra", 44, DGRAY), anim="up")
    elif total:
        text(c, "dívida de janeiro", 80, 1010, 46, HAND, DGRAY, align="l")
        reais(c, t, t_ult, total_ant, total, 80, 1120, 96, RED, d=0.6, align="l")
    hero(c, t, 900, FY, 0.6, [(0, "point_l"), (14.0, "head"), (15.6, "point_l"), (24.6, "shrug"), (28.6, "point_l")],
         [(0, "neutral"), (14.0, "worried"), (15.6, "neutral"), (26.0, "shocked"), (28.6, "worried")], look=-0.8)


def s03(c, t):  # 33.7 - 39.6  somando
    floor(c)
    show(c, t, 33.8, CX, 260, M("SOMANDO", 80, NAVY), anim="stamp")
    if t > 34.4:
        reais(c, t, 34.4, 0, 4100, CX, 420, 140, RED, d=1.0)
    base, scl = 1000, 0.11
    for t0, x, v, lab, top, col in ((36.3, 250, 3000, "seu salário", "R$ 3.000", LGREEN), (36.9, 560, 4100, "janeiro", "R$ 4.100", PINKISH)):
        if t > t0:
            h = v * scl * ease_out(prog(t, t0, 0.6))
            rrect(c, x - 100, base - h, 200, h, 12); fs(c, col, 6)
            show(c, t, t0 + 0.5, x, base - v * scl - 30, MM(top, 52, GREEN if col == LGREEN else RED), anim="pop")
            show(c, t, t0 + 0.2, x, base + 50, T(lab, 46, DGRAY), anim="up")
    line(c, 120, base, 700, base, 6)
    show(c, t, 37.6, 400, 1170, HL("MAIS DE 1 SALÁRIO INTEIRO", 46, PINKISH, RED), anim="stamp")
    hero(c, t, 880, FY, 0.65, [(0, "present_l"), (37.6, "head")], [(0, "neutral"), (37.6, "shocked")], look=-0.8)


def s04(c, t):  # 39.6 - 48.1  a virada: a 2ª parcela do 13º
    floor(c)
    show(c, t, 39.7, CX, 250, lambda c: ribbon(c, "E A VIRADA", RED, 64), anim="stamp")
    show(c, t, 40.7, CX, 380, MM("2ª parcela do 13º", 72, NAVY), anim="stamp")
    show(c, t, 42.8, 300, 530, sc(calendar, "20", RED, 56), anim="pop")
    show(c, t, 43.1, 400, 545, L("cai em dezembro", 50, DGRAY), anim="left", d=0.3)
    if t > 44.3:
        reais(c, t, 44.3, 0, 1250, 420, 680, 110, GREEN, d=0.9, pre="~R$ ")
    if t > 45.6:
        x0, w, y = 100, 640, 800
        rrect(c, x0, y, w, 70, 14); fs(c, PINKISH, 5)
        k = ease_out(prog(t, 45.6, 0.6))
        rrect(c, x0, y, w * 0.305 * k, 70, 14); fs(c, GREEN, 5)
        text(c, m("R$ 4.100"), x0 + w - 20, y + 52, 44, MARKER, RED, align="r")
    show(c, t, 46.2, 420, 960, HL("não paga nem 1/3", 72, PINKISH, RED), anim="stamp")
    hero(c, t, 880, FY, 0.65, [(0, "finger_up"), (46.2, "shrug")], [(0, "think"), (46.2, "worried")], look=-0.8)


PLANO = [
    (49.0, "2ª parcela vai pra janeiro", 51.4, "sem gastar no Natal"),
    (53.0, "IPVA à vista: -3% = R$ 48", 57.6, "não coube? 5x de R$ 320 sem juros"),
    (62.0, "IPTU: compara", 63.5, "em muitas cidades parcelar sai melhor"),
    (66.5, "material: reaproveita", 69.1, "e pesquisa preço"),
]


def s05(c, t):  # 48.1 - 70.4  o plano
    floor(c)
    show(c, t, 48.2, CX, 250, lambda c: ribbon(c, "FAZ ASSIM", GREEN, 66), anim="stamp")
    for i, (t0, tit, ts, sub) in enumerate(PLANO):
        y = 390 + i * 165
        show(c, t, t0, 110, y - 15, sc(check_icon, 34), anim="pop")
        show(c, t, t0 + 0.1, 170, y, L(tit, 54, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, ts, 170, y + 62, L(sub, 44, DGRAY), anim="up")
    hero(c, t, 900, FY, 0.55, [(0, "finger_up"), (53.0, "present_l"), (57.6, "point_l"), (66.5, "thumb")],
         [(0, "confident"), (66.5, "happy")], look=-0.8)


def s06(c, t):  # 70.4 - fim  comenta
    floor(c)
    show(c, t, 70.5, CX, 330, M("QUANTO VAI SER", 80, NAVY), anim="stamp")
    show(c, t, 71.1, CX, 450, M("O SEU JANEIRO?", 88, RED), anim="stamp")
    show(c, t, 70.8, CX, 640, sc(calendar, "JAN", RED, 60, s=1.3), anim="pop")
    show(c, t, 71.8, CX, 850, HL("COMENTA AÍ", 84, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.55, [(0, "point_ru")], [(0, "happy"), (71.8, "grin")], look=0.3)


SCENES = [
    (0.0, 9.1, s01), (9.1, 33.7, s02), (33.7, 39.6, s03), (39.6, 48.1, s04),
    (48.1, 70.4, s05), (70.4, 999.0, s06),
]
