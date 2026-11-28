"""Financiar carro pra rodar de Uber: Lucas (financia popular de R$ 80 mil) x Bruno (aluga de locadora).
Só TikTok: vertical 1080x1920, ~75,9 s, ESTILO CADERNO. Faturamento de R$ 7 mil/mês, 10 h/dia, 5 dias, ~4.000 km. Contas em contas.py.
Quadro 0: o carro e o faturamento do Lucas já subindo para R$ 7 mil; gancho v2 (27/11): "quanto você acha que sobrou?"
sem revelar os R$ 1.550 até os ~33 s. Narração = gancho_v2.mp3 + bloco1.mp3 a partir de 7,45 s (palavras.json já deslocado).
Layout: título y~250, palco y 360-1290 (pés em 1280), legendas y~1400-1460, nada abaixo de 1500 nem em x > 930."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
LX, BX = 270, 770
PINKISH = (1, 0.8, 0.76)

D = 0.587   # o novo gancho (v2, curiosidade) ficou 0,587 s mais longo: as cenas 2 em diante andam D
SFX = [(5.25, "tum"), (32.6 + D, "tum"), (47.8 + D, "tum"), (74.9 + D, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def reais(v):
    s = "%d" % round(v)
    if len(s) > 3:
        s = s[:-3] + "." + s[-3:]
    return "R$ " + s


def valor(c, t, keys, x, y, size, col_fn):
    """valor que anda entre pontos (t, v) com easing"""
    v = keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t >= t0:
            v = v0 + (v1 - v0) * ease_io(prog(t, t0, max(0.01, t1 - t0)))
    text(c, reais(v), x, y, size, MARKER, col_fn(v))


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
def s01(c, t):  # 0 - 8.2  gancho de curiosidade: faturou 7 mil... quanto sobrou?
    floor(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "FINANCIOU PRA RODAR DE APP", NAVY, 46), anim="stamp")
    show(c, t, -1.0, 300, 520, sc(car, RED, s=0.8), anim="left")
    show(c, t, -1.0, 690, 500, sc(phone, NAVY, s=0.9), anim="pop")
    show(c, t, 2.9, CX, 700, T("faturou no mês:", 50, DGRAY), anim="up")
    valor(c, t, [(0.0, 0), (4.3, 7000)], CX, 810, 110, lambda v: GREEN)
    if t > 5.25:
        show(c, t, 5.25, CX, 950, M("QUANTO SOBROU?", 76, RED), anim="stamp")
        show(c, t, 5.6, 860, 820, sc(qmark, 110, RED), anim="pop")
    show(c, t, 6.66, 600, 1070, lambda c: hl(c, "faz a conta comigo", 0, 0, 56, LYELLOW), anim="stamp")
    lucas(c, t, 170, 0.45, [(0, "stand"), (4.3, "arms_up"), (5.25, "think")], [(0, "neutral"), (4.3, "grin"), (5.25, "think")], look=0.5)


def s02(c, t):  # 7.6 - 15.9  a rotina do Lucas
    floor(c)
    show(c, t, 7.7, CX, 250, lambda c: ribbon(c, "A ROTINA DO LUCAS", ORANGE, 56), anim="stamp")
    show(c, t, 8.5, 170, 420, sc(clock, t, s=0.55), anim="pop")
    show(c, t, 8.7, 260, 420, L("10 horas por dia", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 10.1, 260, 560, L("5 dias por semana", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 11.6, 170, 700, sc(car, RED, s=0.35), anim="pop")
    show(c, t, 11.8, 260, 700, L("~4.000 km por mês", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 13.5, CX, 820, T("no aplicativo, fatura", 52), anim="up")
    show(c, t, 14.8, CX, 940, MM("R$ 7.000", 110, GREEN), anim="stamp")
    lucas(c, t, 850, 0.45, [(0, "stand"), (14.8, "thumb")], [(0, "neutral"), (14.8, "happy")], look=-0.6)


def s03(c, t):  # 15.9 - 32.6  o que sai: o saldo derrete
    floor(c)
    show(c, t, 16.0, CX, 250, lambda c: ribbon(c, "AGORA, O QUE SAI", RED, 58), anim="stamp")
    rows = ((17.5, 20.3, sc(gas_pump, s=0.35), "gasolina", "- R$ 2.160", 2160),
            (22.0, 23.8, sc(wrench, s=0.45), "manutenção", "- R$ 720", 720),
            (25.0, 26.2, sc(document, s=0.35), "seguro e IPVA", "- R$ 600", 600),
            (27.7, 31.3, sc(car, RED, s=0.3), "parcela", "- R$ 1.970", 1970))
    keys, saldo = [(16.0, 7000)], 7000
    for i, (ta, tb, ic, nm, val, v) in enumerate(rows):
        y = 420 + i * 110
        show(c, t, ta, 140, y, ic, anim="pop")
        show(c, t, ta + 0.1, 220, y, L(nm, 50, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, tb, 900, y, lambda c, val=val: text(c, val, 0, 0, 52, MARKER, RED, align="r"), anim="stamp")
        saldo -= v
        keys += [(tb, keys[-1][1]), (tb + 0.6, saldo)]
    line(c, 120, 880, 920, 880, 5)
    text(c, "sobra:", 300, 990, 56, HAND, DGRAY)
    valor(c, t, keys, 640, 990, 90, lambda v: GREEN if v > 4000 else (GOLD if v > 2500 else RED))


def s04(c, t):  # 32.6 - 37.4  sobram 1.550, ~7 por hora
    floor(c)
    show(c, t, 32.6, CX, 300, M("SOBRAM", 90, NAVY), anim="stamp")
    show(c, t, 33.0, CX, 450, MM("R$ 1.550", 150, RED), anim="stamp")
    show(c, t, 35.1, 280, 680, sc(clock, t, s=0.6), anim="pop")
    show(c, t, 35.3, 420, 660, L("~R$ 7", 90, RED, MARKER), anim="stamp", d=0.3)
    show(c, t, 36.0, 420, 740, L("por hora trabalhada", 44, DGRAY), anim="up")
    lucas(c, t, CX, 0.5, [(0, "head")], [(0, "desperate")], look=0)


def s05(c, t):  # 37.4 - 47.8  Bruno aluga
    floor(c)
    show(c, t, 37.5, CX, 250, lambda c: ribbon(c, "BRUNO: ALUGA O CARRO", GREEN, 54), anim="stamp")
    show(c, t, 38.9, 280, 460, sc(car, LBLUE, s=0.75), anim="left")
    show(c, t, 39.8, 520, 440, L("~R$ 800/semana", 60, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 42.0, 520, 530, lambda c: (check_icon(c, 22), text(c, "seguro", 40, 0, 44, HAND, INK, align="l")), anim="pop")
    show(c, t, 42.6, 520, 600, lambda c: (check_icon(c, 22), text(c, "manutenção", 40, 0, 44, HAND, INK, align="l")), anim="pop")
    show(c, t, 44.1, 140, 720, sc(gas_pump, s=0.35), anim="pop")
    show(c, t, 44.3, 220, 720, L("+ a mesma gasolina", 54, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 45.9, CX, 860, T("sobram uns", 52), anim="up")
    show(c, t, 46.4, CX, 970, MM("R$ 1.400", 110, RED), anim="stamp")
    bruno(c, t, 860, 0.45, [(0, "stand"), (46.4, "shrug")], [(0, "neutral"), (46.4, "neutral")], look=-0.6)


def s06(c, t):  # 47.8 - 53.8  quase o mesmo, sem dívida
    floor(c); divisoria(c)
    show(c, t, 47.8, CX, 250, lambda c: ribbon(c, "QUASE O MESMO", NAVY, 60), anim="stamp")
    show(c, t, 48.0, LX, 440, MM("R$ 1.550", 70, RED), anim="pop")
    show(c, t, 48.2, BX, 440, MM("R$ 1.400", 70, RED), anim="pop")
    show(c, t, 48.0, LX, 540, T("financiou", 44, DGRAY), anim="up")
    show(c, t, 48.2, BX, 540, T("alugou", 44, DGRAY), anim="up")
    show(c, t, 49.5, BX, 680, MM("sem entrada", 46, GREEN), anim="pop")
    show(c, t, 50.5, BX, 750, MM("sem dívida", 46, GREEN), anim="pop")
    show(c, t, 52.6, BX, 860, T("não deu certo? devolve", 36, DGRAY), anim="up")
    lucas(c, t, LX, 0.5, [(0, "stand")], [(0, "worried")]); nome(c, LX, "LUCAS", ORANGE)
    bruno(c, t, BX, 0.5, [(0, "stand"), (49.5, "thumb")], [(0, "neutral"), (49.5, "happy")]); nome(c, BX, "BRUNO", GREEN)


def s07(c, t):  # 53.8 - 63.7  o detalhe: Lucas fica com o carro, mas desvalorizado
    floor(c)
    show(c, t, 53.9, CX, 250, lambda c: ribbon(c, "MAS TEM UM DETALHE", NAVY, 56), anim="stamp")
    show(c, t, 55.2, CX, 400, T("no fim do financiamento", 52), anim="up")
    show(c, t, 56.6, CX, 500, lambda c: hl(c, "o carro é do Lucas", 0, 0, 60, LGREEN, GREEN), anim="stamp")
    show(c, t, 57.4, 300, 720, sc(car, RED, s=0.75), anim="pop")
    show(c, t, 58.9, 560, 660, L("rodando 4.000 km", 50, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 60.5, 560, 730, L("por mês...", 50, NAVY, MARKER), anim="left", d=0.3)
    if t > 62.7:
        show(c, t, 62.7, 300, 880, MM("R$ 80 mil", 70, GRAY), anim="pop")
        k = ease_out(prog(t, 62.9, 0.3))
        line(c, 160, 895, 160 + 280 * k, 865, 9, RED)
    show(c, t, 62.0, 560, 1000, lambda c: hl(c, "vale bem menos", 0, 0, 56, PINKISH, RED), anim="stamp")
    lucas(c, t, 860, 0.45, [(0, "stand"), (62.0, "head")], [(0, "neutral"), (62.0, "worried")], look=-0.6)


def s08(c, t):  # 63.7 - 71.4  então, vale a pena?
    floor(c)
    show(c, t, 63.8, CX, 300, M("VALE A PENA?", 110, NAVY), anim="stamp")
    show(c, t, 66.6, CX, 460, lambda c: hl(c, "DEPENDE", 0, 0, 80, LYELLOW), anim="stamp")
    show(c, t, 67.1, CX, 580, T("de quanto você fatura na sua cidade", 48), anim="up")
    show(c, t, 69.6, CX, 720, M("FAZ ESSA CONTA", 80, RED), anim="stamp")
    show(c, t, 70.5, CX, 820, T("antes de assinar", 52, DGRAY), anim="up")
    hero(c, t, CX, FY, 0.5, [(0, "think"), (66.6, "finger_up")], [(0, "think"), (66.6, "confident")], look=0)


def s09(c, t):  # 71.4 - fim  comenta
    floor(c)
    show(c, t, 71.5, CX, 300, M("VOCÊ RODA DE APP?", 80, NAVY), anim="stamp")
    show(c, t, 73.0, CX, 420, T("quanto sobra pra você no fim do mês?", 46), anim="up")
    show(c, t, 74.9, CX, 560, lambda c: hl(c, "COMENTA AÍ", 0, 0, 84, LYELLOW), anim="stamp")
    show(c, t, 71.6, 300, 820, sc(car, RED, s=0.6), anim="left")
    show(c, t, 71.8, 720, 800, sc(phone, NAVY, s=0.8), anim="pop")
    hero(c, t, CX, FY, 0.45, [(0, "point_ru")], [(0, "happy")], look=0)


_SCENES = [
    (0.0, 7.6, s01), (7.6, 15.9, s02), (15.9, 32.6, s03), (32.6, 37.4, s04), (37.4, 47.8, s05),
    (47.8, 53.8, s06), (53.8, 63.7, s07), (63.7, 71.4, s08), (71.4, 999.0, s09),
]


def _desloca(fn):
    return lambda c, t: fn(c, t - D)


SCENES = [(0.0, 7.6 + D, s01)] + [(a + D, b + D if b < 900 else b, _desloca(fn)) for a, b, fn in _SCENES[1:]]
