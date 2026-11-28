"""Consórcio é dinheiro jogado fora? Só TikTok: vertical 1080x1920, ~87,3 s, ESTILO CADERNO.
Ana (rosa) faz consórcio, Bruno (verde) financia o mesmo carro de R$ 80 mil. Contas em contas.py.
Layout: título y~250, palco y 360-1290 (pés em 1280), legendas y~1400-1460, nada abaixo de 1500 nem em x > 930."""
from engine import *  # noqa
import math

VERTICAL = True

CX = 520
FY = 1280
AX, BX = 270, 770          # colunas da Ana e do Bruno
PINKISH = (1, 0.8, 0.76)
PINKD = (0.85, 0.30, 0.52)

SFX = [(9.34, "tum"), (27.2, "tum"), (48.56, "soft_ding"), (51.98, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def MM(s, size=60, col=INK):
    return lambda c: text(c, s, 0, 0, size, MARKER, col)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def brlk(v):
    return "R$ %d mil" % int(v / 1000)


def ana(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", 0.4)
    other(c, t, x, FY, s, poses, exprs, shirt=PINK, fid=4, hair="long", **kw)


def bruno(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", -0.4)
    other(c, t, x, FY, s, poses, exprs, shirt=GREEN, fid=3, hair="tuft", **kw)


def nome(c, x, s, col):
    text(c, s, x, FY + 60, 46, MARKER, col)


def divisoria(c, y0=400):
    line(c, CX, y0, CX, FY - 20, 4, LGRAY)


def contador(c, t, t0, d, v0, v1, x, y, size, col, fmt=brlk):
    v = v0 if t < t0 else v0 + (v1 - v0) * ease_io(prog(t, t0, d))
    text(c, fmt(v), x, y, size, MARKER, col)


def onibus(c):
    """ônibus de lado, centrado em (0,0)"""
    rrect(c, -170, -80, 340, 140, 22); fs(c, YELLOW, 6)
    for i in range(4):
        rrect(c, -150 + i * 72, -60, 58, 50, 8); fs(c, LBLUE, 4)
    rrect(c, 140, -60, 22, 90, 6); fs(c, LBLUE, 4)
    for wx in (-100, 100):
        circle(c, wx, 62, 26); fs(c, INK, 4)
        circle(c, wx, 62, 10); fs(c, LGRAY, 3)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 12.3  gancho: o mesmo carro, o preço já subindo no quadro 0
    floor(c)
    show(c, t, -1.0, CX, 230, M("CONSÓRCIO É", 64, NAVY), anim="stamp")
    show(c, t, -1.0, CX, 310, lambda c: hl(c, "DINHEIRO JOGADO FORA?", 0, 0, 60, PINKISH, RED), anim="stamp")
    show(c, t, -1.0, CX, 520, sc(car, LBLUE, s=0.8), anim="pop")
    contador(c, t, 0.0, 5.9, 0, 80000, CX, 680, 90, INK)
    if t > 2.9:
        show(c, t, 6.8, AX, 790, lambda c: hl(c, "CONSÓRCIO", 0, 0, 54, (1, 0.85, 0.92), PINKD), anim="stamp")
        show(c, t, 8.2, BX, 790, lambda c: hl(c, "FINANCIOU", 0, 0, 54, LGREEN, GREEN), anim="stamp")
    show(c, t, 9.34, CX, 900, lambda c: hl(c, "QUEM PAGOU MAIS?", 0, 0, 66, LYELLOW), anim="stamp")
    show(c, t, 9.6, CX, 1110, sc(qmark, 90, RED), anim="pop")
    ana(c, t, AX, 0.55, [(0, "stand"), (6.8, "thumb"), (9.34, "think")], [(0, "neutral"), (6.8, "happy"), (9.34, "think")])
    bruno(c, t, BX, 0.55, [(0, "stand"), (8.2, "thumb"), (9.34, "think_l")], [(0, "neutral"), (8.2, "happy"), (9.34, "think")])
    if t > 3.0:
        nome(c, AX, "ANA", PINKD); nome(c, BX, "BRUNO", GREEN)


def s02(c, t):  # 12.3 - 30.0  Bruno financia
    floor(c)
    show(c, t, 12.4, CX, 250, lambda c: ribbon(c, "BRUNO: FINANCIOU", GREEN, 58), anim="stamp")
    show(c, t, 12.7, 250, 450, sc(car, LBLUE, s=0.7), anim="left")
    show(c, t, 12.9, 250, 580, MM("R$ 80 mil", 62, INK), anim="stamp")
    show(c, t, 13.6, 500, 430, L("em 60x", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 15.2, 500, 510, L("juros de", 46, DGRAY), anim="up")
    show(c, t, 16.5, 680, 590, lambda c: hl(c, "1,9% ao mês", 0, 0, 56, PINKISH, RED), anim="stamp")
    show(c, t, 18.3, 500, 670, L("a média de hoje", 42, DGRAY), anim="up")
    show(c, t, 19.9, CX, 790, T("parcela:", 46, DGRAY), anim="up")
    show(c, t, 20.6, CX, 880, MM("R$ 2.246/mês", 78, RED), anim="stamp")
    show(c, t, 23.6, 300, 1010, T("total pago:", 46, DGRAY), anim="up")
    if t > 24.3:
        contador(c, t, 24.5, 1.8, 80000, 134763, 300, 1100, 72, RED)
    show(c, t, 27.2, 620, 1010, lambda c: hl(c, "R$ 55 mil", 0, 0, 58, PINKISH, RED), anim="stamp")
    show(c, t, 28.7, 620, 1090, T("só de juros", 46, RED), anim="up")
    bruno(c, t, 860, 0.5, [(0, "thumb"), (27.2, "head")], [(0, "happy"), (27.2, "shocked")], look=-0.6)


def s03(c, t):  # 30.0 - 45.5  Ana no consórcio
    floor(c)
    show(c, t, 30.1, CX, 250, lambda c: ribbon(c, "ANA: CONSÓRCIO", PINKD, 58), anim="stamp")
    show(c, t, 30.4, 250, 450, sc(car, LBLUE, s=0.7), anim="left")
    show(c, t, 30.6, 250, 580, MM("R$ 80 mil", 62, INK), anim="stamp")
    show(c, t, 31.4, 500, 430, L("em 60 meses", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 33.4, 500, 520, L("sem juros...", 50, GREEN, MARKER), anim="left", d=0.3)
    show(c, t, 34.7, 500, 600, L("mas tem taxa de", 44, DGRAY), anim="up")
    show(c, t, 35.2, 500, 660, L("administração", 44, DGRAY), anim="up")
    show(c, t, 37.2, 640, 740, lambda c: hl(c, "~18%", 0, 0, 58, LYELLOW), anim="stamp")
    show(c, t, 38.5, CX, 840, T("parcela:", 46, DGRAY), anim="up")
    show(c, t, 39.0, CX, 930, MM("R$ 1.573/mês", 78, GREEN), anim="stamp")
    if t > 41.8:
        k = ease_out(prog(t, 41.8, 0.8))
        arrow(c, 200, 1120, 200, 1120 - 120 * k, RED, 10, 0.0)
    show(c, t, 42.7, 250, 1040, L("sobe todo ano", 50, RED, MARKER), anim="left", d=0.3)
    show(c, t, 44.5, 250, 1110, L("com o preço do carro", 40, DGRAY), anim="up")
    ana(c, t, 860, 0.5, [(0, "stand"), (33.4, "thumb"), (42.7, "shrug")], [(0, "neutral"), (33.4, "happy"), (42.7, "worried")], look=-0.6)


def s04(c, t):  # 45.5 - 50.2  total: as duas barras
    floor(c)
    show(c, t, 45.6, CX, 250, lambda c: ribbon(c, "TOTAL PAGO", NAVY, 60), anim="stamp")
    base, scl = 1080, 4.2 / 1000
    for t0, x, v, col in ((45.7, 330, 134763, GREEN), (46.4, 710, 103287, PINKD)):
        if t > t0:
            h = v * scl * ease_out(prog(t, t0, 0.8))
            rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
            show(c, t, t0 + 0.8, x, base - v * scl - 45, MM(brlk(v), 56, INK), anim="pop")
    line(c, 160, base, 860, base, 6)
    text(c, "BRUNO", 330, base + 50, 44, MARKER, GREEN)
    text(c, "ANA", 710, base + 50, 44, MARKER, PINKD)
    show(c, t, 48.56, CX, 370, lambda c: hl(c, "R$ 30 mil a menos", 0, 0, 52, LGREEN, GREEN), anim="stamp")


def s05(c, t):  # 50.2 - 58.9  tem um detalhe: Bruno dirige hoje, Ana espera o sorteio
    floor(c)
    if t < 51.9:
        show(c, t, 50.3, CX, 400, M("ENTÃO CONSÓRCIO", 70, NAVY), anim="stamp")
        show(c, t, 50.9, CX, 500, M("É MELHOR?", 90, NAVY), anim="stamp")
        show(c, t, 51.1, CX, 760, sc(qmark, 200, RED), anim="pop")
        return
    show(c, t, 51.98, CX, 250, lambda c: ribbon(c, "TEM UM DETALHE", RED, 60), anim="stamp")
    divisoria(c)
    # Bruno: sai dirigindo
    x = 200 + 180 * ease_io(prog(t, 53.5, 2.5))
    show(c, t, 53.1, x, 520, sc(car, LBLUE, s=0.55), anim="pop")
    show(c, t, 53.7, AX - 30, 680, MM("HOJE", 70, GREEN), anim="stamp")
    show(c, t, 54.2, AX + 130, 680, sc(check_icon, 60), anim="pop")
    # Ana: sorteio ou lance
    show(c, t, 55.6, BX, 500, sc(qmark, 110, PINKD), anim="pop")
    show(c, t, 56.9, BX, 680, MM("SORTEIO", 60, PINKD), anim="stamp")
    show(c, t, 58.0, BX, 760, T("ou lance", 50, DGRAY), anim="up")
    bruno(c, t, AX, 0.55, [(0, "arms_up")], [(0, "grin")])
    ana(c, t, BX, 0.55, [(0, "stand"), (55.6, "think_l")], [(0, "neutral"), (55.6, "think")], look=-0.4)
    nome(c, AX, "BRUNO", GREEN); nome(c, BX, "ANA", PINKD)


def s06(c, t):  # 58.9 - 65.0  pode ser no mês 1 ou no 60; enquanto isso, ônibus
    floor(c)
    show(c, t, 59.0, CX, 250, lambda c: ribbon(c, "QUANDO SAI O CARRO?", PINKD, 56), anim="stamp")
    show(c, t, 59.4, 300, 500, sc(calendar, "1", GREEN, 110), anim="pop")
    show(c, t, 59.7, 300, 660, T("mês 1?", 50, GREEN), anim="up")
    show(c, t, 60.8, 740, 500, sc(calendar, "60", RED, 110), anim="pop")
    show(c, t, 61.0, 740, 660, T("mês 60?", 50, RED), anim="up")
    show(c, t, 62.5, 680, 900, sc(onibus, s=0.9), anim="left")
    show(c, t, 64.2, 680, 1060, T("continua de ônibus", 46, DGRAY), anim="up")
    ana(c, t, 250, 0.55, [(0, "think"), (62.5, "shrug")], [(0, "think"), (62.5, "sad")])


def s07(c, t):  # 65.0 - 73.1  a conta fica assim
    floor(c); divisoria(c, 360)
    show(c, t, 65.1, CX, 250, lambda c: ribbon(c, "A CONTA FICA ASSIM", NAVY, 58), anim="stamp")
    show(c, t, 66.2, AX, 430, T("precisa agora?", 50, INK), anim="up")
    show(c, t, 67.8, AX, 540, lambda c: hl(c, "FINANCIA", 0, 0, 60, LGREEN, GREEN), anim="stamp")
    show(c, t, 68.4, AX, 640, T("custa caro...", 44, RED), anim="up")
    show(c, t, 69.4, AX, 710, T("mas resolve", 44, DGRAY), anim="up")
    show(c, t, 70.1, BX, 430, T("pode esperar?", 50, INK), anim="up")
    show(c, t, 71.1, BX, 540, lambda c: hl(c, "CONSÓRCIO", 0, 0, 56, (1, 0.85, 0.92), PINKD), anim="stamp")
    show(c, t, 72.0, BX, 640, T("bem mais barato", 44, GREEN), anim="up")
    bruno(c, t, AX, 0.55, [(0, "stand"), (67.8, "thumb")], [(0, "neutral"), (67.8, "happy")])
    ana(c, t, BX, 0.55, [(0, "stand"), (71.1, "thumb")], [(0, "neutral"), (71.1, "happy")], look=-0.4)


def s08(c, t):  # 73.1 - 82.9  e se tiver disciplina: guardar a parcela
    floor(c)
    show(c, t, 73.2, CX, 250, lambda c: ribbon(c, "E SE VOCÊ TEM DISCIPLINA?", GOLD, 52), anim="stamp")
    show(c, t, 74.7, 230, 480, sc(piggy, GOLD, s=0.9), anim="pop")
    show(c, t, 75.3, 400, 440, L("guarda", 46, DGRAY), anim="up")
    show(c, t, 75.7, 400, 520, L("R$ 1.573/mês", 62, GREEN, MARKER), anim="left", d=0.3)
    show(c, t, 77.1, 400, 600, L("rendendo", 46, DGRAY), anim="up")
    if t > 77.1:
        contador(c, t, 77.3, 2.6, 0, 95752, CX, 740, 84, GREEN)
    show(c, t, 79.4, 320, 860, sc(calendar, "4", NAVY, 90), anim="pop")
    show(c, t, 79.7, 420, 840, L("anos: à vista", 54, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 80.96, CX, 990, lambda c: hl(c, "SEM JUROS E SEM TAXA", 0, 0, 52, LGREEN, GREEN), anim="stamp")
    hero(c, t, 850, FY, 0.45, [(0, "present_l"), (80.96, "finger_up")], [(0, "neutral"), (80.96, "confident")], look=-0.6)


def s09(c, t):  # 82.9 - fim  pergunta final
    floor(c); divisoria(c, 700)
    show(c, t, 83.0, CX, 300, M("CONSÓRCIO", 96, PINKD), anim="stamp")
    show(c, t, 83.3, CX, 400, M("OU", 70, NAVY), anim="stamp")
    show(c, t, 84.9, CX, 500, M("FINANCIAMENTO?", 86, GREEN), anim="stamp")
    show(c, t, 85.87, CX, 640, lambda c: hl(c, "COMENTA AÍ", 0, 0, 76, LYELLOW), anim="stamp")
    ana(c, t, AX, 0.6, [(0, "think")], [(0, "think")]); nome(c, AX, "ANA", PINKD)
    bruno(c, t, BX, 0.6, [(0, "shrug")], [(0, "neutral")]); nome(c, BX, "BRUNO", GREEN)


SCENES = [
    (0.0, 12.3, s01), (12.3, 30.0, s02), (30.0, 45.5, s03), (45.5, 50.2, s04), (50.2, 58.9, s05),
    (58.9, 65.0, s06), (65.0, 73.1, s07), (73.1, 82.9, s08), (82.9, 999.0, s09),
]
