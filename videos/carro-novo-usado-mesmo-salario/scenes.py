"""Mesmo salário: carro zero x usado + investir a parcela. Só TikTok: vertical 1080x1920, ~71,7 s, ESTILO CADERNO.
Lucas (laranja) financia um zero de R$ 100 mil; Bruno (verde) compra um usado de R$ 20 mil e investe a mesma parcela.
Quadro 0: a página dividida, o carro do Lucas perdendo valor e o investimento do Bruno subindo. Contas em contas.py.
Layout: título y~250, palco y 360-1290 (pés em 1280), legendas y~1400-1460, nada abaixo de 1500 nem em x > 930."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
LX, BX = 270, 770          # colunas do Lucas e do Bruno
PINKISH = (1, 0.8, 0.76)

SFX = [(10.6, "tum"), (26.9, "tum"), (58.6, "tum"), (70.8, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def MM(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


def brlk(v):
    return "R$ %d mil" % round(v / 1000)


def lucas(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", 0.4)
    other(c, t, x, FY, s, poses, exprs, shirt=ORANGE, fid=2, **kw)


def bruno(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", -0.4)
    other(c, t, x, FY, s, poses, exprs, shirt=GREEN, fid=3, hair="tuft", **kw)


def nome(c, x, s, col):
    text(c, s, x, FY + 60, 46, MARKER, col)


def divisoria(c):
    line(c, CX, 340, CX, FY - 20, 4, LGRAY)


def contador(c, t, t0, d, v0, v1, x, y, size, col):
    if t < t0:
        v = v0
    else:
        v = v0 + (v1 - v0) * ease_io(prog(t, t0, d))
    text(c, m(brlk(v)), x, y, size, MARKER, col)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 11.8  gancho: página dividida, os dois números já correndo
    floor(c); divisoria(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "MESMO SALÁRIO", NAVY, 60), anim="stamp")
    show(c, t, 2.6, CX, 360, lambda c: hl(c, "5 ANOS DEPOIS", 0, 0, 56, LYELLOW), anim="stamp")
    # Bruno: investimento subindo
    show(c, t, -1.0, BX, 560, sc(bills, 3, s=1.0), anim="pop")
    contador(c, t, 0.0, 6.0, 0, 172000, BX, 700, 76, GREEN)
    show(c, t, 6.3, BX, 780, T("investidos", 46, DGRAY), anim="up")
    # Lucas: carro perdendo valor
    show(c, t, -1.0, LX, 560, sc(car, RED, s=0.7), anim="pop")
    contador(c, t, 0.0, 9.4, 100000, 55000, LX, 700, 76, RED)
    show(c, t, 8.4, LX, 780, T("o carro vale", 46, DGRAY), anim="up")
    show(c, t, 10.6, CX, 940, lambda c: hl(c, "UMA DECISÃO SÓ", 0, 0, 76, PINKISH, RED), anim="stamp")
    lucas(c, t, LX, 0.6, [(0, "stand"), (8.4, "head")], [(0, "neutral"), (8.4, "worried")])
    bruno(c, t, BX, 0.6, [(0, "stand"), (6.3, "arms_up")], [(0, "neutral"), (6.3, "grin")])


def s02(c, t):  # 11.8 - 15.3  os dois começam iguais
    floor(c); divisoria(c)
    show(c, t, 11.9, CX, 250, lambda c: ribbon(c, "O COMEÇO", NAVY, 60), anim="stamp")
    for x in (LX, BX):
        show(c, t, 12.8, x, 560, sc(piggy, GOLD, s=0.9), anim="pop")
        show(c, t, 13.3, x, 730, MM("R$ 20 mil", 70, NAVY), anim="stamp")
        show(c, t, 13.8, x, 810, T("guardados", 44, DGRAY), anim="up")
    lucas(c, t, LX, 0.6, [(0, "stand")], [(0, "happy")]); nome(c, LX, "LUCAS", ORANGE)
    bruno(c, t, BX, 0.6, [(0, "stand")], [(0, "happy")]); nome(c, BX, "BRUNO", GREEN)


def s03(c, t):  # 15.3 - 29.0  Lucas: zero financiado
    floor(c)
    show(c, t, 15.4, CX, 250, lambda c: ribbon(c, "LUCAS: CARRO ZERO", ORANGE, 58), anim="stamp")
    show(c, t, 16.2, 250, 470, sc(car, RED, s=0.75), anim="left")
    show(c, t, 17.0, 250, 610, MM("R$ 100 mil", 66, INK), anim="stamp")
    show(c, t, 17.8, 520, 430, L("entrada: R$ 20 mil", 44, DGRAY), anim="left", d=0.3)
    show(c, t, 19.3, 520, 510, L("financia R$ 80 mil", 46, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 20.9, 520, 590, L("em 60x", 54, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 22.3, CX, 760, T("juros médios de hoje:", 50), anim="up")
    show(c, t, 24.0, CX, 850, lambda c: hl(c, "quase 2% ao mês", 0, 0, 60, PINKISH, RED), anim="stamp")
    show(c, t, 26.0, CX, 960, T("parcela:", 48, DGRAY), anim="up")
    show(c, t, 26.9, CX, 1060, MM("R$ 2.250/mês", 80, RED), anim="stamp")
    lucas(c, t, 880, 0.55, [(0, "arms_up"), (24.0, "stand")], [(0, "grin"), (24.0, "neutral")], look=-0.6)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="l")


def s04(c, t):  # 29.0 - 36.8  Bruno: usado à vista + investe a parcela
    floor(c)
    show(c, t, 29.1, CX, 250, lambda c: ribbon(c, "BRUNO: USADO", GREEN, 58), anim="stamp")
    show(c, t, 29.9, 330, 470, sc(car, LBLUE, s=0.75), anim="left")
    show(c, t, 30.4, 330, 600, MM("R$ 20 mil", 66, INK), anim="stamp")
    show(c, t, 31.3, 650, 470, lambda c: hl(c, "À VISTA", 0, 0, 60, LGREEN), anim="stamp")
    show(c, t, 32.3, CX, 760, T("e todo mês investe", 52), anim="up")
    show(c, t, 33.9, CX, 870, MM("R$ 2.250", 100, GREEN), anim="stamp")
    show(c, t, 35.3, CX, 980, T("a parcela que o Lucas paga", 46, DGRAY), anim="up")
    show(c, t, 33.5, 180, 880, sc(piggy, GOLD, s=0.6), anim="pop")
    bruno(c, t, 880, 0.55, [(0, "stand"), (32.3, "thumb")], [(0, "neutral"), (32.3, "confident")], look=-0.6)


def s05(c, t):  # 36.8 - 38.2  passam cinco anos
    floor(c)
    show(c, t, 36.8, CX, 560, sc(calendar, "5", NAVY, 120), anim="pop")
    show(c, t, 37.2, CX, 800, M("ANOS DEPOIS", 100, NAVY), anim="stamp")


def s06(c, t):  # 38.2 - 47.6  Lucas cinco anos depois
    floor(c)
    show(c, t, 38.3, CX, 250, lambda c: ribbon(c, "LUCAS, 5 ANOS DEPOIS", ORANGE, 54), anim="stamp")
    show(c, t, 38.7, CX, 400, T("pagou no total:", 50, DGRAY), anim="up")
    show(c, t, 39.0, CX, 510, MM("R$ 155 mil", 100, RED), anim="stamp")
    show(c, t, 41.9, 300, 760, sc(car, RED, s=0.7), anim="pop")
    if t > 43.1:
        show(c, t, 43.4, 300, 640, lambda c: hl(c, "-45%", 0, 0, 70, PINKISH, RED), anim="stamp")
    show(c, t, 45.3, 680, 720, T("hoje vale", 50, DGRAY), anim="up")
    if t > 45.3:
        contador(c, t, 45.8, 1.2, 100000, 55000, 680, 820, 80, RED)
    lucas(c, t, CX, 0.6, [(0, "stand"), (43.4, "head")], [(0, "neutral"), (43.4, "desperate")], look=0)


def s07(c, t):  # 47.6 - 57.0  Bruno cinco anos depois
    floor(c)
    show(c, t, 47.7, CX, 250, lambda c: ribbon(c, "BRUNO, 5 ANOS DEPOIS", GREEN, 54), anim="stamp")
    show(c, t, 48.1, CX, 400, T("investido:", 50, DGRAY), anim="up")
    contador(c, t, 48.2, 1.8, 0, 172000, CX, 520, 110, GREEN)
    show(c, t, 50.6, CX, 630, T("10% ao ano, já sem imposto", 46, DGRAY), anim="up")
    show(c, t, 54.0, 230, 790, sc(car, LBLUE, s=0.55), anim="pop")
    show(c, t, 55.8, 400, 790, L("+ carro R$ 14 mil", 50, NAVY, MARKER), anim="left", d=0.3)
    bruno(c, t, CX, 0.6, [(0, "stand"), (49.5, "arms_up")], [(0, "neutral"), (49.5, "grin")], look=0)


def s08(c, t):  # 57.0 - 60.5  a diferença
    floor(c)
    show(c, t, 57.1, CX, 250, lambda c: ribbon(c, "PATRIMÔNIO", NAVY, 60), anim="stamp")
    base, scl = 1020, 3.4 / 1000
    for t0, x, v, col in ((57.2, 330, 55000, ORANGE), (57.6, 710, 186000, GREEN)):
        if t > t0:
            h = v * scl * ease_out(prog(t, t0, 0.6))
            rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
            show(c, t, t0 + 0.6, x, base - v * scl - 45, MM(brlk(v), 56, INK), anim="pop")
    line(c, 160, base, 860, base, 6)
    text(c, "LUCAS", 330, base + 50, 44, MARKER, ORANGE)
    text(c, "BRUNO", 710, base + 50, 44, MARKER, GREEN)
    show(c, t, 58.6, 330, 560, lambda c: hl(c, "+ R$ 131 mil", 0, 0, 66, LGREEN, GREEN), anim="stamp")


def s09(c, t):  # 60.5 - 69.4  o que ficou de fora
    floor(c)
    show(c, t, 60.6, CX, 250, lambda c: ribbon(c, "E NEM CONTEI...", RED, 58), anim="stamp")
    show(c, t, 61.6, 150, 430, sc(document, s=0.5), anim="pop")
    show(c, t, 61.6, 260, 430, L("seguro e IPVA", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 62.9, 260, 510, L("mais caros no zero", 46, RED), anim="up")
    show(c, t, 64.9, 150, 680, sc(wrench, s=0.6), anim="pop")
    show(c, t, 65.1, 260, 680, L("o usado vai mais", 50, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 66.1, 260, 760, L("na oficina...", 46, DGRAY), anim="up")
    show(c, t, 67.3, CX, 920, lambda c: hl(c, "mas nem de longe R$ 131 mil", 0, 0, 52, LYELLOW), anim="stamp")
    hero(c, t, 820, FY, 0.5, [(0, "present_l"), (67.3, "finger_up")], [(0, "neutral"), (67.3, "confident")], look=-0.6)


def s10(c, t):  # 69.4 - fim  qual dos dois é você?
    floor(c); divisoria(c)
    show(c, t, 69.5, CX, 300, M("QUAL DOS DOIS", 90, NAVY), anim="stamp")
    show(c, t, 69.9, CX, 410, M("É VOCÊ?", 110, RED), anim="stamp")
    show(c, t, 70.8, CX, 600, lambda c: hl(c, "COMENTA AÍ", 0, 0, 80, LYELLOW), anim="stamp")
    show(c, t, 69.6, LX, 800, sc(car, RED, s=0.55), anim="pop")
    show(c, t, 69.8, BX, 800, sc(bills, 3, s=0.8), anim="pop")
    lucas(c, t, LX, 0.6, [(0, "shrug")], [(0, "worried")]); nome(c, LX, "LUCAS", ORANGE)
    bruno(c, t, BX, 0.6, [(0, "thumb")], [(0, "grin")]); nome(c, BX, "BRUNO", GREEN)


SCENES = [
    (0.0, 11.8, s01), (11.8, 15.3, s02), (15.3, 29.0, s03), (29.0, 36.8, s04), (36.8, 38.2, s05),
    (38.2, 47.6, s06), (47.6, 57.0, s07), (57.0, 60.5, s08), (60.5, 69.4, s09), (69.4, 999.0, s10),
]
