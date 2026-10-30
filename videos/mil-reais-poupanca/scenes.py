"""Mil reais na poupança por um ano. Só TikTok: vertical nativo 1080x1920, 45 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco com pausa de 1 s depois do gancho.
Premissas (29/10/2026): Selic 13,75%, CDI 13,65%, TR ~0,167% a.m., IR 17,5% (365 dias), Tesouro Selic + 0,07%,
custódia B3 0,20% isenta até R$ 10 mil no Tesouro Selic. Contas em roteiro.txt.
Layout vertical como em videos/reserva-emergencia (desenho em y-60, SHIFT desce tudo 60 px)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
TS = " "  # espaço fino: na Permanent Marker o ponto de milhar some depois do "2"

SFX = [(4.9, "tum"), (19.7, "soft_ding"), (33.9, "tum"), (42.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def big_q(c, t, t0):
    """? enorme pulsando"""
    k = 1 + 0.05 * math.sin((t - t0) * 9)
    c.save(); c.scale(k, k)
    text(c, "?", 0, 0, 520, MARKER, GOLD, outline=INK, ow=14)
    c.restore()


def grow_bar(t, t0, h, col, label, top, w=200):
    return lambda c: bar(c, h * ease_out(prog(t, t0, 0.6)), w, col, label,
                         top if t > t0 + 0.5 else None, 52)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 3.8  gancho: mil reais parados na poupança, um ano. Chuta.
    floor(c)
    show(c, t, 0.0, CX, 290, lambda c: hl(c, "R$ 1.000", 0, 0, 130, LGREEN), anim="stamp", d=0.3)
    show(c, t, 1.2, CX - 200, 540, sc(piggy, s=1.1), anim="pop")
    show(c, t, 1.25, CX - 200, 690, T("poupança", 60), anim="up")
    show(c, t, 2.0, CX + 220, 530, sc(calendar, "365", NAVY, 64, s=1.5), anim="pop")
    show(c, t, 2.05, CX + 220, 690, T("1 ano parado", 60), anim="up")
    show(c, t, 2.8, CX, 820, lambda c: hl(c, "CHUTA: QUANTO RENDEU?", 0, 0, 62, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.6, [(0, "present"), (2.8, "think")], [(0, "neutral"), (2.8, "think")], appear=0.0, look=0)


def s02(c, t):  # 3.8 - 4.84  pausa: ? gigante
    show(c, t, 3.8, CX, 640, lambda c: big_q(c, t, 3.8), anim="stamp", d=0.25)
    show(c, t, 3.9, CX, 1000, T("pensa num número...", 64, DGRAY), anim="up")


def s03(c, t):  # 4.84 - 8.5  oitenta e três reais
    floor(c)
    show(c, t, 4.85, CX, 270, T("na poupança rendeu", 64), anim="up", d=0.25)
    show(c, t, 4.9, CX, 480, M("R$ 83", 230, GREEN), anim="stamp", d=0.3)
    show(c, t, 6.9, CX, 720, lambda c: hl(c, "com os juros de hoje", 0, 0, 56, LYELLOW), anim="up")
    show(c, t, 7.4, CX, 820, T("Selic 13,75% · sem IR", 46, DGRAY), anim="fade")
    hero(c, t, CX, FY, 0.72, [(0, "present_l"), (5.0, "shrug")], [(0, "neutral"), (5.0, "neutral")], look=0)


BASE = 1080  # base das barras


def s04(c, t):  # 8.5 - 24.1  barras lado a lado: poupança 83, CDB 112, Tesouro Selic 113
    title(c, t, 8.6, "Os mesmos R$ 1.000, 1 ano", y=230, size=66)
    xs = (215, 520, 825)
    show(c, t, 8.7, xs[0], BASE, grow_bar(t, 8.7, 83 * 3.6, (0.55, 0.62, 0.72), "poupança", "R$ 83"), anim="fade", d=0.1)
    # CDB
    show(c, t, 10.8, xs[1], 440, M("CDB", 64, NAVY), anim="pop")
    show(c, t, 12.8, xs[1], 505, T("100% do CDI", 44), anim="up")
    show(c, t, 11.4, xs[1], 555, T("liquidez diária", 40, DGRAY), anim="up")
    show(c, t, 15.0, CX, 330, lambda c: hl(c, "já sem o IR (17,5%)", 0, 0, 48, PINKISH), anim="stamp", t1=18.1)
    show(c, t, 16.4, xs[1], BASE, grow_bar(t, 16.4, 112 * 3.6, GREEN, "CDB", "R$ 112"), anim="fade", d=0.1)
    # Tesouro Selic
    show(c, t, 18.3, xs[2], 440, M("TESOURO", 50, NAVY), anim="pop")
    show(c, t, 18.5, xs[2], 500, M("SELIC", 50, NAVY), anim="pop")
    show(c, t, 19.6, xs[2], BASE, grow_bar(t, 19.6, 113 * 3.6, GREEN, "Tesouro", "R$ 113"), anim="fade", d=0.1)
    show(c, t, 21.3, CX, 330, lambda c: hl(c, "custódia R$ 0 até R$ 10 mil", 0, 0, 48, LYELLOW), anim="stamp")


def s05(c, t):  # 24.1 - 27.4  parece pouca diferença: uns trinta reais
    floor(c)
    show(c, t, 24.2, CX, 280, T("parece pouca diferença...", 64), anim="up")
    show(c, t, 26.1, CX, 520, M("+ R$ 30", 180, GREEN), anim="stamp")
    show(c, t, 26.5, CX, 690, T("por ano, em R$ 1.000", 52, DGRAY), anim="up")
    hero(c, t, CX, FY, 0.75, [(0, "shrug")], [(0, "neutral")], prop=("l", prop_coin), look=0)


def s06(c, t):  # 27.4 - 31.5  com dez mil, quase trezentos por ano
    floor(c)
    show(c, t, 27.5, CX, 280, M("MAS COM", 80, NAVY), anim="up", d=0.25)
    show(c, t, 27.9, CX, 430, lambda c: hl(c, "R$ 10.000", 0, 0, 120, LGREEN), anim="stamp")
    show(c, t, 28.9, CX, 650, T("quase", 60), anim="up")
    show(c, t, 29.2, CX, 810, M("+ R$ 300", 180, GREEN), anim="stamp")
    show(c, t, 30.4, CX, 960, T("a mais por ano", 60), anim="up")
    hero(c, t, 880, FY, 0.55, [(0, "relax"), (29.2, "point_lu")], [(0, "neutral"), (29.2, "shocked")], look=-1)


def s07(c, t):  # 31.5 - 35.8  em cinco anos passa de dois mil e quinhentos
    floor(c)
    show(c, t, 31.7, CX, 270, M("EM 5 ANOS", 96, NAVY), anim="stamp", d=0.3)
    if t > 32.0:
        for i in range(5):
            show(c, t, 32.0 + i * 0.15, 200 + i * 160, 470, sc(calendar, str(i + 1), GOLD, 60, s=0.7), anim="pop")
    show(c, t, 33.0, CX, 650, T("a diferença passa de", 60), anim="up")
    show(c, t, 33.9, CX, 830, lambda c: hl(c, "R$ 2" + TS + ".500", 0, 0, 150, LGREEN), anim="stamp")
    hero(c, t, 880, FY, 0.55, [(0, "relax"), (33.9, "arms_up")], [(0, "think"), (33.9, "grin")], look=-1)


def s08(c, t):  # 35.8 - 40.4  os três são seguros; a diferença é onde você deixa
    floor(c)
    show(c, t, 36.0, CX, 260, T("os 3 servem pra reserva", 64), anim="up")
    names = (("poupança", 215, 36.3), ("CDB", 520, 36.6), ("Tesouro", 825, 36.9))
    for nm, x, t0 in names:
        show(c, t, t0, x, 470, sc(shield, NAVY, s=0.7), anim="pop")
        show(c, t, t0 + 0.4, x + 70, 540, sc(check_icon, 34), anim="pop")
        show(c, t, t0, x, 630, T(nm, 50), anim="up")
    show(c, t, 38.3, CX, 760, T("a diferença é só", 60), anim="up")
    show(c, t, 39.4, CX, 880, lambda c: hl(c, "ONDE VOCÊ DEIXA", 0, 0, 74, LYELLOW), anim="stamp")
    hero(c, t, 880, FY, 0.5, [(0, "present_l"), (39.4, "finger_up")], [(0, "neutral"), (39.4, "confident")], look=-1)


def s09(c, t):  # 40.4 - fim  CTA: comenta + segue
    floor(c)
    show(c, t, 40.6, CX, 270, M("Seu dinheiro", 86, NAVY), anim="up", d=0.25)
    show(c, t, 40.9, CX, 380, M("tá onde?", 86, NAVY), anim="up", d=0.25)
    show(c, t, 41.9, CX - 60, 520, group(lambda c: speech(c, 460, 120, -130, 100), T("Comenta!", 64)), anim="pop")
    show(c, t, 42.8, 420, 690, lambda c: ribbon(c, "SEGUE PRA MAIS CONTAS", NAVY, 50, GOLD), anim="stamp")
    if t > 42.9:
        arrow_draw(c, t, 42.9, 520, 900, 900, 560, d=0.4, lw=11, col=GOLD)
    hero(c, t, 360, FY, 0.72, [(0, "point_r"), (42.8, "point_ru")], [(0, "happy"), (42.8, "grin")], look=1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 3.8, s01), (3.8, 4.84, s02), (4.84, 8.5, s03), (8.5, 24.1, s04), (24.1, 27.4, s05),
    (27.4, 31.5, s06), (31.5, 35.8, s07), (35.8, 40.4, s08), (40.4, 999.0, s09),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
