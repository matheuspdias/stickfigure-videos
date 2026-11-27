"""Saque-aniversário: Ana (saque-aniversário) e Bruno (saque-rescisão) demitidos no mesmo dia.
Só TikTok: vertical 1080x1920, ~72 s, ESTILO CADERNO. Salário R$ 3 mil, 5 anos de empresa. Contas em contas.py.
Quadro 0: página dividida, os dois com a caixa da demissão e o FGTS do Bruno já subindo.
Layout: título y~250, palco y 360-1290 (pés em 1280), legendas y~1400-1460, nada abaixo de 1500 nem em x > 930."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
LX, BX = 270, 770          # colunas da Ana e do Bruno
PINKISH = (1, 0.8, 0.76)
PINKD = (0.85, 0.30, 0.52)

SFX = [(5.9, "tum"), (8.4, "tum"), (45.1, "tum"), (71.0, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="l")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def MM(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


def brlk(v):
    return "R$ %d mil" % round(v / 1000)


def ana(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", 0.4)
    other(c, t, x, FY, s, poses, exprs, shirt=PINK, fid=4, hair="long", **kw)


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



def barras(c, t, t0, va, vb, rot, base=1000, scl=None, k=1000):
    scl = scl or 520 / max(va, vb)
    for tt, x, v, col in ((t0, 330, va, PINK), (t0 + 0.4, 710, vb, GREEN)):
        if t > tt:
            h = v * scl * ease_out(prog(t, tt, 0.6))
            rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
            show(c, t, tt + 0.6, x, base - v * scl - 45, MM(rot(v), 56, INK), anim="pop")
    line(c, 160, base, 860, base, 6)
    text(c, "ANA", 330, base + 50, 44, MARKER, PINKD)
    text(c, "BRUNO", 710, base + 50, 44, MARKER, GREEN)



def app_fgts(c, pressed=False):
    """celular com o app do FGTS e o botão do saque-aniversário"""
    c.save(); c.scale(1.6, 1.6); phone(c, NAVY); c.restore()
    text(c, "FGTS", 0, -100, 34, MARKER, NAVY)
    rrect(c, -70, -30, 140, 70, 14); fs(c, GREEN if pressed else WHITE, 4)
    text(c, "SAQUE-", 0, -8, 22, MARKER, WHITE if pressed else GREEN)
    text(c, "ANIVERSÁRIO", 0, 18, 18, MARKER, WHITE if pressed else GREEN)


def dedo(c, t, t0, x, y):
    """dedo apertando o botão em t0"""
    k = ease_out(prog(t, t0 - 0.5, 0.5))
    yy = y + 120 * (1 - k)
    c.save(); c.translate(x + 30, yy + 40); c.rotate(-0.4)
    rrect(c, -18, -10, 36, 110, 18); fs(c, (1, 0.86, 0.74), 5)
    c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.7  gancho
    floor(c); divisoria(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "DEMITIDOS NO MESMO DIA", NAVY, 52), anim="stamp")
    show(c, t, -1.0, LX, 470, sc(moving_box, s=0.8), anim="drop")
    show(c, t, -1.0, BX, 470, sc(moving_box, s=0.8), anim="drop")
    contador(c, t, 0.0, 4.5, 0, 24400, BX, 650, 80, GREEN)
    show(c, t, 4.6, BX, 730, T("de FGTS", 44, DGRAY), anim="up")
    if t > 5.9:
        contador(c, t, 5.9, 0.8, 0, 7000, LX, 650, 80, RED)
        show(c, t, 6.6, LX, 730, T("de FGTS", 44, DGRAY), anim="up")
    if t > 7.5:
        show(c, t, 7.5, CX, 900, sc(app_fgts, t > 8.4, s=0.75), anim="pop")
        dedo(c, t, 8.4, CX - 10, 900)
        show(c, t, 8.4, CX, 1110, lambda c: hl(c, "UM BOTÃO", 0, 0, 56, PINKISH, RED), anim="stamp")
    ana(c, t, LX, 0.5, [(0, "hold"), (5.9, "head")], [(0, "worried"), (5.9, "shocked")])
    bruno(c, t, BX, 0.5, [(0, "hold"), (4.5, "arms_up")], [(0, "worried"), (4.5, "grin")])


def s02(c, t):  # 9.7 - 14.4  quem são
    floor(c); divisoria(c)
    show(c, t, 9.8, CX, 250, lambda c: ribbon(c, "MESMA EMPRESA", NAVY, 60), anim="stamp")
    for x in (LX, BX):
        show(c, t, 10.8, x, 480, MM("R$ 3 mil/mês", 60, NAVY), anim="stamp")
        show(c, t, 12.4, x, 650, sc(calendar, "5", NAVY, 56), anim="pop")
        show(c, t, 12.9, x, 790, T("anos de casa", 44, DGRAY), anim="up")
    ana(c, t, LX, 0.6, [(0, "stand")], [(0, "happy")]); nome(c, LX, "ANA", PINKD)
    bruno(c, t, BX, 0.6, [(0, "stand")], [(0, "happy")]); nome(c, BX, "BRUNO", GREEN)


def s03(c, t):  # 14.4 - 28.3  Ana no saque-aniversário
    floor(c)
    show(c, t, 14.5, CX, 250, lambda c: ribbon(c, "A ANA APERTOU", PINKD, 60), anim="stamp")
    show(c, t, 14.6, 200, 520, sc(app_fgts, t > 15.2, s=0.8), anim="pop")
    dedo(c, t, 15.2, 190, 520)
    show(c, t, 16.6, 430, 400, L("todo aniversário:", 44, DGRAY), anim="left", d=0.3)
    show(c, t, 17.9, 870, 400, sc(gift, RED, GOLD, s=0.45), anim="pop")
    base = 820
    for i, (tt, v) in enumerate(((21.1, 1125), (21.9, 1740), (22.5, 2068), (23.1, 2340))):
        x = 430 + i * 125
        if t > tt:
            h = v * 0.11 * ease_out(prog(t, tt, 0.5))
            rrect(c, x - 45, base - h, 90, h, 8); fs(c, GREEN, 5)
            show(c, t, tt + 0.4, x, base - v * 0.11 - 30, MM("%.1f" % (v / 1000), 34, INK) if False else MM("R$ %d" % v, 26, INK), anim="pop")
            text(c, "%dº" % (i + 1), x, base + 35, 34, MARKER, DGRAY)
    if t > 21.0:
        line(c, 370, base, 920, base, 5)
    show(c, t, 24.6, CX, 980, T("em 4 anos, ela sacou", 50), anim="up")
    show(c, t, 26.6, CX, 1090, MM("R$ 7.300", 96, GREEN), anim="stamp")


def s04(c, t):  # 28.3 - 30.0  Bruno nunca mexeu
    floor(c)
    show(c, t, 28.4, CX, 250, lambda c: ribbon(c, "O BRUNO", GREEN, 60), anim="stamp")
    show(c, t, 28.6, CX, 520, MM("nunca mexeu", 96, NAVY), anim="stamp")
    bruno(c, t, CX, 0.6, [(0, "shrug")], [(0, "neutral")], look=0)


def s05(c, t):  # 30.0 - 31.6  demitidos
    floor(c); divisoria(c)
    show(c, t, 30.0, CX, 300, M("DEMITIDOS", 110, RED), anim="stamp")
    show(c, t, 30.3, LX, 620, sc(moving_box, s=0.8), anim="drop")
    show(c, t, 30.5, BX, 620, sc(moving_box, s=0.8), anim="drop")
    ana(c, t, LX, 0.55, [(0, "hold")], [(0, "worried")]); bruno(c, t, BX, 0.55, [(0, "hold")], [(0, "worried")])


def s06(c, t):  # 31.6 - 38.8  Bruno saca tudo
    floor(c)
    show(c, t, 31.7, CX, 250, lambda c: ribbon(c, "BRUNO SACA TUDO", GREEN, 58), anim="stamp")
    show(c, t, 33.1, 120, 430, L("saldo", 50, DGRAY), anim="left", d=0.3)
    show(c, t, 33.4, 560, 430, L("R$ 17.400", 64, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 35.3, 120, 530, L("+ multa 40%", 50, DGRAY), anim="left", d=0.3)
    show(c, t, 35.6, 560, 530, L("R$ 7.000", 64, NAVY, MARKER), anim="left", d=0.3)
    if t > 36.6:
        line(c, 120, 600, 900, 600, 5)
    show(c, t, 37.1, CX, 720, MM("R$ 24.400", 120, GREEN), anim="stamp")
    show(c, t, 38.0, CX, 830, T("na mão", 52, DGRAY), anim="up")
    show(c, t, 37.1, 820, 1050, sc(bills, 3, s=0.9), anim="pop")
    bruno(c, t, 300, 0.55, [(0, "stand"), (37.1, "arms_up")], [(0, "neutral"), (37.1, "grin")], look=0.4)


def s07(c, t):  # 38.8 - 46.0  Ana: só a multa, o resto preso
    floor(c)
    show(c, t, 38.9, CX, 250, lambda c: ribbon(c, "A ANA RECEBE", PINKD, 60), anim="stamp")
    show(c, t, 39.7, 120, 430, L("só a multa", 50, DGRAY), anim="left", d=0.3)
    show(c, t, 40.6, 560, 430, L("R$ 7.000", 64, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 42.0, 120, 560, L("e o resto do FGTS", 50, DGRAY), anim="left", d=0.3)
    show(c, t, 42.6, 420, 700, MM("R$ 9.600", 110, RED), anim="stamp")
    show(c, t, 45.1, 830, 690, sc(padlock, GOLD, s=0.8), anim="drop")
    show(c, t, 45.1, 420, 830, lambda c: hl(c, "FICA PRESO", 0, 0, 70, PINKISH, RED), anim="stamp")
    ana(c, t, 300, 0.55, [(0, "stand"), (45.1, "head")], [(0, "neutral"), (45.1, "desperate")], look=0.4)


def s08(c, t):  # 46.0 - 57.2  volta aos poucos; carência de 2 anos
    floor(c)
    show(c, t, 46.1, CX, 250, lambda c: ribbon(c, "NÃO SOME, MAS...", NAVY, 58), anim="stamp")
    show(c, t, 47.7, CX, 400, T("volta aos pouquinhos:", 52), anim="up")
    show(c, t, 49.5, 420, 520, MM("~R$ 2.500/ano", 76, NAVY), anim="stamp")
    show(c, t, 51.4, 860, 510, sc(gift, RED, GOLD, s=0.45), anim="pop")
    show(c, t, 51.7, CX, 610, T("só no mês do aniversário", 46, DGRAY), anim="up")
    show(c, t, 52.9, CX, 780, T("e se ela sair agora?", 54), anim="up")
    show(c, t, 55.7, 230, 920, sc(clock, t, s=0.7), anim="pop")
    show(c, t, 55.9, 360, 920, L("só vale daqui a", 50, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 56.4, 360, 1000, L("2 ANOS", 76, RED, MARKER), anim="stamp", d=0.3)
    ana(c, t, 820, 0.45, [(0, "stand"), (52.9, "think")], [(0, "neutral"), (52.9, "think")], look=-0.6)


def s09(c, t):  # 57.2 - 66.6  não perdeu: o problema é a hora
    floor(c)
    show(c, t, 57.3, CX, 250, lambda c: ribbon(c, "ENTÃO...", NAVY, 60), anim="stamp")
    show(c, t, 57.9, CX, 400, T("ela não perdeu dinheiro", 54), anim="up")
    show(c, t, 59.3, CX, 500, lambda c: hl(c, "recebeu ANTES", 0, 0, 64, LGREEN, GREEN), anim="stamp")
    show(c, t, 60.7, CX, 650, M("O PROBLEMA É A HORA", 70, RED), anim="stamp")
    show(c, t, 61.9, CX, 760, T("na demissão, quando mais precisa:", 46, DGRAY), anim="up")
    show(c, t, 64.2, CX, 880, MM("~R$ 10 mil travados", 76, RED), anim="stamp")
    ana(c, t, CX, 0.45, [(0, "stand"), (64.2, "head")], [(0, "neutral"), (64.2, "worried")], look=0)


def s10(c, t):  # 66.6 - fim  faz essa conta / comenta
    floor(c)
    show(c, t, 66.7, CX, 300, M("ANTES DE APERTAR", 82, NAVY), anim="stamp")
    show(c, t, 67.5, 300, 560, sc(app_fgts, False, s=0.8), anim="pop")
    show(c, t, 68.3, 520, 500, L("faz", 80, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 68.5, 520, 610, L("essa conta", 80, RED, MARKER), anim="left", d=0.3)
    show(c, t, 69.5, CX, 800, T("você tá no saque-aniversário?", 52), anim="up")
    show(c, t, 71.0, CX, 910, lambda c: hl(c, "COMENTA AÍ", 0, 0, 80, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.5, [(0, "finger_up"), (71.0, "point_ru")], [(0, "confident"), (71.0, "happy")], look=0)


SCENES = [
    (0.0, 9.7, s01), (9.7, 14.4, s02), (14.4, 28.3, s03), (28.3, 30.0, s04), (30.0, 31.6, s05),
    (31.6, 38.8, s06), (38.8, 46.0, s07), (46.0, 57.2, s08), (57.2, 66.6, s09), (66.6, 999.0, s10),
]
