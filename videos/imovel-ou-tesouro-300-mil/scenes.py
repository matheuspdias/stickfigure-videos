"""Imóvel é o melhor investimento? Apê de R$ 300 mil pra alugar (Ana) x R$ 300 mil no Tesouro Selic (Bruno).
Só TikTok: vertical 1080x1920, ~86 s, ESTILO CADERNO. Aluguel de R$ 1.900 = cenário favorável ao apê (média FipeZAP ~R$ 1.530).
Quadro 0: página dividida, o prédio da Ana e o banco do Bruno já entrando. Contas em contas.py.
Layout: título y~250, palco y 360-1290 (pés em 1280), legendas y~1400-1460, nada abaixo de 1500 nem em x > 930."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
LX, BX = 270, 770          # colunas da Ana e do Bruno
PINKISH = (1, 0.8, 0.76)
PINKD = (0.85, 0.30, 0.52)

SFX = [(6.0, "tum"), (42.5, "tum"), (55.9, "tum"), (85.3, "soft_ding")]
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


# ======================================================================= CENAS
def s01(c, t):  # 0 - 10.5  gancho
    floor(c); divisoria(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "R$ 300 MIL CADA", NAVY, 60), anim="stamp")
    show(c, t, -1.0, LX, 720, sc(apartment, LYELLOW, "ALUGA-SE", 4, s=0.75), anim="up")
    show(c, t, 1.6, LX, 790, MM("apê pra alugar", 46, PINKD), anim="pop")
    show(c, t, 3.7, BX, 640, sc(bank, s=1.1), anim="pop")
    show(c, t, 5.3, BX, 790, MM("Tesouro", 56, GREEN), anim="pop")
    show(c, t, 6.0, BX, 420, lambda c: hl(c, "+ R$ 1.100/mês", 0, 0, 52, LGREEN, GREEN), anim="stamp")
    show(c, t, 8.9, CX, 940, lambda c: hl(c, "MAS TEM UMA VIRADA", 0, 0, 64, PINKISH, RED), anim="stamp")
    ana(c, t, LX, 0.55, [(0, "present"), (6.0, "shrug")], [(0, "happy"), (6.0, "worried")])
    bruno(c, t, BX, 0.55, [(0, "stand"), (6.0, "thumb")], [(0, "neutral"), (6.0, "grin")])


def s02(c, t):  # 10.5 - 19.5  Ana aluga por 1.900
    floor(c)
    show(c, t, 10.6, CX, 250, lambda c: ribbon(c, "ANA: O APÊ", PINK, 60, INK), anim="stamp")
    show(c, t, 10.8, 260, 760, sc(apartment, LYELLOW, None, 5, s=0.8), anim="up")
    show(c, t, 11.9, 540, 420, L("aluga por", 50, DGRAY), anim="left", d=0.3)
    show(c, t, 12.5, 540, 510, L("R$ 1.900/mês", 70, PINKD, MARKER), anim="stamp", d=0.3)
    show(c, t, 14.4, 540, 620, lambda c: hl(c, "acima da média", 0, 0, 46, LYELLOW), anim="stamp")
    show(c, t, 15.4, 540, 720, L("média do Brasil:", 44, DGRAY), anim="up")
    show(c, t, 17.1, 540, 790, L("~R$ 1.500", 56, NAVY, MARKER), anim="left", d=0.3)
    ana(c, t, 820, 0.5, [(0, "present_l")], [(0, "happy")], look=-0.6)


def s03(c, t):  # 19.5 - 27.9  os custos
    floor(c)
    show(c, t, 19.6, CX, 250, lambda c: ribbon(c, "SÓ QUE...", RED, 60), anim="stamp")
    show(c, t, 20.6, 170, 440, sc(calendar, "0", RED, 56), anim="pop")
    show(c, t, 20.9, 270, 420, L("1 mês vazio por ano", 50, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 21.8, 270, 490, L("entre um inquilino e outro", 42, DGRAY), anim="up")
    show(c, t, 23.5, 170, 630, sc(wrench, s=0.6), anim="pop")
    show(c, t, 23.9, 270, 630, L("sempre um conserto", 50, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 25.0, CX, 800, T("na média, sobram", 50), anim="up")
    show(c, t, 26.3, CX, 910, MM("~R$ 1.600/mês", 90, PINKD), anim="stamp")
    ana(c, t, CX, 0.5, [(0, "stand"), (23.9, "head")], [(0, "neutral"), (23.9, "worried")], look=0)


def s04(c, t):  # 27.9 - 38.3  Bruno no Tesouro
    floor(c)
    show(c, t, 28.0, CX, 250, lambda c: ribbon(c, "BRUNO: O TESOURO", GREEN, 58), anim="stamp")
    show(c, t, 28.4, 250, 470, sc(bank, s=1.0), anim="pop")
    show(c, t, 30.3, 480, 440, L("Tesouro Selic", 60, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 32.4, 480, 520, L("já sem imposto e taxa", 42, DGRAY), anim="up")
    show(c, t, 34.1, CX, 680, T("rende", 52), anim="up")
    show(c, t, 34.6, CX, 790, MM("~R$ 2.700/mês", 90, GREEN), anim="stamp")
    show(c, t, 36.5, 300, 950, lambda c: (check_icon(c, 26), text(c, "sem inquilino", 50, 0, 44, HAND, INK, align="l")), anim="pop")
    show(c, t, 37.5, 300, 1030, lambda c: (check_icon(c, 26), text(c, "sem conserto", 50, 0, 44, HAND, INK, align="l")), anim="pop")
    bruno(c, t, 880, 0.5, [(0, "stand"), (34.6, "thumb")], [(0, "neutral"), (34.6, "grin")], look=-0.6)


def s05(c, t):  # 38.3 - 42.0  por mês
    floor(c)
    show(c, t, 38.4, CX, 250, lambda c: ribbon(c, "POR MÊS", NAVY, 60), anim="stamp")
    barras(c, t, 38.5, 1600, 2700, lambda v: "R$ " + ("%d" % v)[0] + "." + ("%d" % v)[1:])
    show(c, t, 40.1, 330, 520, lambda c: hl(c, "+ R$ 1.100", 0, 0, 56, LGREEN, GREEN), anim="stamp")


def s06(c, t):  # 42.0 - 53.4  a virada: valorização
    floor(c)
    show(c, t, 42.1, CX, 250, lambda c: ribbon(c, "A VIRADA", RED, 66), anim="stamp")
    show(c, t, 43.3, 260, 800, sc(apartment, LYELLOW, None, 5, s=0.8), anim="up")
    if t > 44.3:
        k = ease_out(prog(t, 44.3, 0.6))
        arrow(c, 430, 760, 430, 760 - 300 * k, GREEN, 10, 0.0)
    show(c, t, 44.3, 540, 420, L("o apê valoriza", 54, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 45.2, 540, 500, L("últimos 12 meses:", 42, DGRAY), anim="up")
    show(c, t, 47.9, 540, 590, L("+5,5%", 80, GREEN, MARKER), anim="stamp", d=0.3)
    show(c, t, 51.3, 540, 760, L("+ R$ 16 mil", 66, GREEN, MARKER), anim="stamp", d=0.3)
    show(c, t, 52.5, 540, 840, L("no ano", 44, DGRAY), anim="up")
    ana(c, t, 800, 0.45, [(0, "stand"), (47.9, "arms_up")], [(0, "neutral"), (47.9, "grin")], look=-0.6)


def s07(c, t):  # 53.4 - 59.3  no ano, a Ana passa
    floor(c)
    show(c, t, 53.5, CX, 250, lambda c: ribbon(c, "NO ANO (COM VALORIZAÇÃO)", NAVY, 46), anim="stamp")
    barras(c, t, 54.1, 35, 33, lambda v: "R$ %d mil" % v, scl=480 / 35)
    show(c, t, 55.9, 330, 350, lambda c: hl(c, "ANA PASSA!", 0, 0, 56, PINKISH, RED), anim="stamp")


def s08(c, t):  # 59.3 - 69.2  dois detalhes
    floor(c)
    show(c, t, 59.4, CX, 250, lambda c: ribbon(c, "MAS... 2 DETALHES", RED, 58), anim="stamp")
    show(c, t, 60.7, 100, 430, L("1. a valorização só vira", 48, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 61.8, 100, 500, L("dinheiro se ela vender", 48, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 64.1, 100, 660, L("2. o imposto do aluguel", 48, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 66.2, 100, 730, L("(depende do salário dela)", 42, DGRAY), anim="up")
    show(c, t, 67.8, CX, 880, lambda c: hl(c, "come a diferença", 0, 0, 60, PINKISH, RED), anim="stamp")
    hero(c, t, CX, FY, 0.5, [(0, "finger_up"), (64.1, "present")], [(0, "think"), (67.8, "confident")], look=0)


def s09(c, t):  # 69.2 - 76.1  quase empatam; juros caindo
    floor(c)
    show(c, t, 69.3, CX, 250, lambda c: ribbon(c, "NA PRÁTICA", NAVY, 60), anim="stamp")
    tilt = 0.0 if t < 74.4 else -ease_io(prog(t, 74.4, 1.0))
    if t > 69.5:
        c.save(); c.translate(CX, 620)
        balance(c, tilt, lambda c: sc(apartment, LYELLOW, None, 2, s=0.35)(c), lambda c: sc(bank, s=0.5)(c))
        c.restore()
    show(c, t, 70.6, CX, 880, lambda c: hl(c, "QUASE EMPATAM", 0, 0, 66, LYELLOW), anim="stamp", t1=71.8)
    show(c, t, 72.2, CX, 880, T("se os juros caírem...", 54), anim="up")
    show(c, t, 74.7, CX, 980, lambda c: hl(c, "o apê passa na frente", 0, 0, 56, PINKISH, PINKD), anim="stamp")


def s10(c, t):  # 76.1 - 82.5  depende
    floor(c)
    show(c, t, 76.2, CX, 300, M("IMÓVEL É O MELHOR", 78, NAVY), anim="stamp")
    show(c, t, 77.5, CX, 400, M("INVESTIMENTO?", 90, RED), anim="stamp")
    show(c, t, 78.9, CX, 540, lambda c: hl(c, "DEPENDE:", 0, 0, 66, LYELLOW), anim="stamp")
    for tt, y, s in ((79.5, 660, "dos juros"), (80.4, 740, "do imposto"), (81.2, 820, "do apê não ficar vazio")):
        show(c, t, tt, 260, y, L("- " + s, 52, NAVY, MARKER), anim="left", d=0.3)
    hero(c, t, CX, FY, 0.45, [(0, "think"), (78.9, "finger_up")], [(0, "think"), (78.9, "confident")], look=0)


def s11(c, t):  # 82.5 - fim  comenta
    floor(c); divisoria(c)
    show(c, t, 82.6, CX, 300, M("APÊ OU TESOURO?", 90, NAVY), anim="stamp")
    show(c, t, 85.3, CX, 450, lambda c: hl(c, "COMENTA AÍ", 0, 0, 80, LYELLOW), anim="stamp")
    show(c, t, 82.8, LX, 820, sc(apartment, LYELLOW, None, 3, s=0.55), anim="up")
    show(c, t, 83.0, BX, 760, sc(bank, s=0.8), anim="pop")
    ana(c, t, LX, 0.55, [(0, "present")], [(0, "happy")]); nome(c, LX, "ANA", PINKD)
    bruno(c, t, BX, 0.55, [(0, "thumb")], [(0, "grin")]); nome(c, BX, "BRUNO", GREEN)


SCENES = [
    (0.0, 10.5, s01), (10.5, 19.5, s02), (19.5, 27.9, s03), (27.9, 38.3, s04), (38.3, 42.0, s05),
    (42.0, 53.4, s06), (53.4, 59.3, s07), (59.3, 69.2, s08), (69.2, 76.1, s09), (76.1, 82.5, s10), (82.5, 999.0, s11),
]
