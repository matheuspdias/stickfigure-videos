"""Com quanto você está entre os 10% que mais ganham no Brasil? Só TikTok: vertical nativo 1080x1920, ~68 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Dados: IBGE, PNAD Contínua anual 2025, SIDRA tabela 7536 (limites dos percentis do rendimento habitual de
todos os trabalhos, pessoas de 14+ ocupadas com rendimento, a preços médios de 2025):
P50 R$ 2.037 | P60 R$ 2.546 | P70 R$ 3.055 | P80 R$ 4.470 | P90 R$ 6.985 | P95 R$ 10.174 | P99 R$ 24.839.
Salário mínimo 2025: R$ 1.518 (entre P20 R$ 1.504 e P30 R$ 1.536)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
TS = ""

SFX = [(6.95, "tum"), (31.75, "tum"), (36.45, "tum"), (65.8, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

FONTE = "Fonte: IBGE, PNAD Contínua 2025 · pessoas que trabalham"


def mk_w(c, s, size):
    parts = s.split("2.")
    w = sum(text_w(c, p, size) for p in parts) + (len(parts) - 1) * (text_w(c, "2", size) + text_w(c, ".", size) + size * 0.07)
    return w


def mk_text(c, s, x, y, size, col=INK):
    """Permanent Marker: o ponto de milhar depois do "2" encosta no pé do 2; desenha com um respiro só antes do ponto"""
    w = mk_w(c, s, size)
    cx = x - w / 2
    parts = s.split("2.")
    for i, p in enumerate(parts):
        cx += text(c, p, cx, y, size, MARKER, col, align="l")
        if i < len(parts) - 1:
            cx += text(c, "2", cx, y, size, MARKER, col, align="l") + size * 0.07
            cx += text(c, ".", cx, y, size, MARKER, col, align="l")


def mhl(s, size, bg=LYELLOW, pad=22):
    def f(c):
        w = mk_w(c, s, size)
        c.save(); c.rotate(-0.015)
        rrect(c, -w / 2 - pad, -size * 0.62, w + 2 * pad, size * 1.24, 14); rgb(c, bg); c.fill()
        mk_text(c, s, 0, 0, size)
        c.restore()
    return f


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def fonte(c, t, t0=0.0):
    show(c, t, t0, CX, 1300, T(FONTE, 34, DGRAY), anim="fade")


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def R(s, size=50, col=INK, font=MARKER):
    return lambda c: text(c, s, 0, 0, size, font, col, align="r")


def card(lines, w=640, h=None, fill=WHITE, border=NAVY):
    """cartão branco com linhas (texto, tamanho, cor, fonte)"""
    hh = h or sum(l[1] * 1.25 for l in lines) + 50

    def f(c):
        rrect(c, -w / 2, -hh / 2, w, hh, 24); fs(c, fill, 6)
        c.rectangle(-w / 2 + 3, -hh / 2 + 3, 16, hh - 6); rgb(c, border); c.fill()
        y = -hh / 2 + 25
        for s, size, col, font in lines:
            y += size * 0.62
            text(c, s, 15, y, size, font, col)
            y += size * 0.63
    return f


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.84  gancho: chuta
    floor(c)
    show(c, t, 0.0, CX, 290, lambda c: hl(c, "CHUTA:", 0, 0, 110, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 0.0, CX, 470, M("quanto por mês pra", 66, INK), anim="fade", d=0.2)
    show(c, t, 0.0, CX, 570, M("estar nos", 66, INK), anim="fade", d=0.2)
    show(c, t, 0.15, CX, 730, lambda c: hl(c, "10% QUE MAIS GANHAM", 0, 0, 74, NAVY, WHITE), anim="stamp", d=0.3)
    show(c, t, 0.3, CX, 860, M("no Brasil?", 66, INK), anim="fade", d=0.2)
    hero(c, t, CX, FY, 0.62, [(0, "think"), (3.5, "think_l")], [(0, "think")], appear=0.0, look=0)


def s02(c, t):  # 5.84 - 6.96  pausa com "?" grande
    floor(c)
    k = 1 + 0.06 * math.sin((t - 5.84) * 9)
    show(c, t, 5.84, CX, 640, lambda c: qmark(c, 640 * k, NAVY), anim="pop", d=0.3)
    hero(c, t, 860, FY, 0.5, [(0, "shrug")], [(0, "think")], look=-1)


def s03(c, t):  # 6.96 - 11.4  a resposta
    floor(c)
    show(c, t, 6.96, CX, 300, T("os 10% do topo começam em", 58), anim="up", d=0.3)
    show(c, t, 6.96, CX, 500, lambda c: hl(c, "R$ 6.985", 0, 0, 180, LGREEN), anim="stamp", d=0.35)
    show(c, t, 9.2, CX, 680, M("por mês", 72, NAVY), anim="up")
    show(c, t, 10.1, CX, 830, lambda c: hl(c, "quase R$ 7 mil", 0, 0, 70, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.6, [(0, "head"), (9.3, "present")], [(0, "shocked"), (9.3, "confident")], look=0)
    fonte(c, t, 7.2)


def s04(c, t):  # 11.4 - 22.0  a base: quem trabalha, rendimento de todos os trabalhos
    floor(c)
    show(c, t, 11.6, CX, 270, M("De onde vem?", 74, NAVY), anim="up")
    show(c, t, 12.4, CX, 420, card([("IBGE", 70, NAVY, MARKER), ("PNAD Contínua 2025", 54, INK, HAND)], w=600), anim="pop")
    show(c, t, 16.3, 300, 640, lambda c: hl(c, "só quem trabalha", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, 18.0, CX, 790, T("o que costuma ganhar por mês,", 50), anim="up")
    show(c, t, 20.2, CX, 860, T("somando todos os trabalhos (bruto)", 50), anim="up")
    other(c, t, 260, FY, 0.55, [(0, "wave"), (18.0, "hold")], [(0, "happy")], appear=16.5, look=0.5)
    show(c, t, 18.3, 370, 1080, sc(bills, 3, s=0.6), anim="pop")
    hero(c, t, 800, FY, 0.55, [(0, "relax"), (12.4, "point_lu"), (16.3, "present_l")], [(0, "neutral"), (12.4, "confident")], look=-1)
    fonte(c, t, 11.6)


# escada: 3 degraus (metade, top 10%, top 1%)
STEPS = [  # (t, x_degrau, y_topo, rótulo, valor, cor)
    (24.0, 230, 1060, "METADE", "até R$ 2" + TS + ".037", BLUE),
    (29.1, 520, 870, "TOP 10%", "a partir de R$ 6.985", GREEN),
    (34.2, 810, 680, "TOP 1%", "a partir de R$ 24.839", GOLD),
]


def s05(c, t):  # 22.0 - 39.3  a escada
    floor(c)
    title(c, t, 22.1, "A ESCADA DA RENDA", y=250, size=72)
    for i, (t0, x, ytop, lab, val, col) in enumerate(STEPS):
        if t < t0 - 0.1:
            continue
        k = ease_out(prog(t, t0 - 0.1, 0.35))
        hgt = (FY - ytop) * k
        c.rectangle(x - 125, FY - hgt, 250, hgt); fs(c, col, 6)
        if k > 0.9:
            text(c, lab, x, ytop + 50, 48, MARKER, WHITE, outline=INK, ow=6)
            if i == 0:
                show(c, t, t0 + 0.6, x, ytop + 112, T(val, 38, WHITE), anim="fade")
            else:
                show(c, t, t0 + 0.6, x, ytop + 110, T(val.split(" R$")[0], 36, WHITE), anim="fade")
                show(c, t, t0 + 0.6, x, ytop + 155, T("R$" + val.split(" R$")[1], 40, WHITE), anim="fade")
    # valor grande em cima, um por vez
    for i, (t0, x, ytop, lab, val, col) in enumerate(STEPS):
        t1 = STEPS[i + 1][0] - 0.2 if i < 2 else None
        show(c, t, t0 + 1.8 if i == 0 else t0 + 2.5, CX, 370, mhl(val.upper() if False else val, 66), anim="stamp", t1=t1)
    # O Consultor sobe os degraus
    x, y = 110, FY
    for t0, xs, ytop, *_ in STEPS:
        if t > t0 + 0.2:
            k = ease_out(clamp01((t - t0 - 0.2) / 0.5))
            x, y = x + (xs - x) * k, y + (ytop - y) * k
    hero(c, t, x, y, 0.42, [(0, "relax"), (24.2, "point_ru"), (29.3, "arms_up"), (34.4, "head")],
         [(0, "happy"), (29.3, "grin"), (34.4, "shocked")], look=0.3)
    fonte(c, t, 22.1)


# régua por percentil: base (0%) em y 1210, topo (100%) em y 400
RY0, RY1, RX = 1210, 400, 250


def ry(p):
    return RY0 + (RY1 - RY0) * p / 100


def ruler(c, t):
    rrect(c, RX - 40, RY1, 80, RY0 - RY1, 20); fs(c, WHITE, 6)
    for p0, p1, col in ((0, 50, BLUE), (90, 99, GREEN), (99, 100, GOLD)):
        c.rectangle(RX - 34, ry(p1), 68, ry(p0) - ry(p1)); rgb(c, col, 0.55); c.fill()
    for p, lab in ((50, "metade"), (90, "top 10%")):
        line(c, RX - 50, ry(p), RX + 50, ry(p), 6, INK)
        text(c, lab, RX - 58, ry(p), 34, HAND, DGRAY, align="r")
    text(c, "0%", RX, RY0 + 40, 38, HAND, DGRAY)
    text(c, "100%", RX, RY1 - 40, 38, HAND, DGRAY)


SAL = [  # (t, percentil aproximado, rótulo, resultado, t_resultado, y da linha de texto)
    (41.3, 25, "Mínimo R$ 1.518", "metade de baixo", 45.7, 1000),
    (47.3, 65, "R$ 3 mil", "mais que 6 em 10", 49.2, 760),
    (50.9, 84, "R$ 5 mil", "mais que 8 em 10", 52.2, 580),
    (53.7, 93, "R$ 10 mil", "TOP 10%", 55.4, 400),
]


def s06(c, t):  # 39.3 - 57.4  onde fica cada salário
    floor(c)
    title(c, t, 39.4, "E O SEU SALÁRIO?", y=250, size=72)
    show(c, t, 39.6, 0, 0, lambda c: ruler(c, t), anim="fade", d=0.3)
    for i, (t0, p, lab, res, tr, ty) in enumerate(SAL):
        if t < t0:
            continue
        yy = ry(p)
        k = ease_out(prog(t, t0, 0.35))
        x2, y2 = RX + 50 + (360 - RX - 50) * k, yy + (ty - yy) * k
        line(c, RX + 20, yy, x2, y2, 5, NAVY)
        circle(c, RX, yy, 16, NAVY, 4)
        show(c, t, t0, 380, ty - 22, L(lab, 50, NAVY, MARKER), anim="left", d=0.3)
        if i == 3:
            show(c, t, tr, 380, ty + 40, L(res, 54, GREEN, MARKER), anim="stamp", d=0.3)
        else:
            show(c, t, tr, 380, ty + 36, L(res, 44, INK, HAND), anim="up", d=0.3)
    hero(c, t, 860, FY, 0.45, [(0, "point_l"), (53.8, "arms_up")], [(0, "neutral"), (53.8, "grin")], look=-1)
    fonte(c, t, 39.6)


LIMS = [("P10", 801), ("P20", 1504), ("P30", 1536), ("P40", 1829), ("P50", 2037), ("P60", 2546),
        ("P70", 3055), ("P80", 4470), ("P90", 6985), ("P99", 24839)]


def s07(c, t):  # 57.4 - 63.2  a virada: renda concentrada
    floor(c)
    show(c, t, 57.6, CX, 270, M("menor do que parece", 70, NAVY), anim="up")
    base, hmax = 1090, 600
    for i, (lab, v) in enumerate(LIMS):
        t0 = 58.2 + i * 0.12 + (0.6 if lab == "P99" else 0)
        if t < t0:
            continue
        h = hmax * v / 24839 * ease_out(prog(t, t0, 0.5))
        x = 110 + i * 84
        col = GOLD if lab == "P99" else (GREEN if lab == "P90" else BLUE)
        rrect(c, x - 32, base - h, 64, max(h, 2), 8); fs(c, col, 4)
        text(c, lab, x, base + 32, 30, HAND, DGRAY)
    line(c, 60, base, 980, base, 5)
    show(c, t, 59.0, 446, 1000, T("R$ 2.037", 36, INK), anim="up")
    show(c, t, 59.5, 832, 520, R("R$ 24.839", 46), anim="up")
    show(c, t, 61.9, CX, 380, lambda c: hl(c, "renda muito concentrada", 0, 0, 62, LYELLOW), anim="stamp")
    show(c, t, 59.6, CX, 1170, T("limite de cada faixa, em R$ por mês", 38, DGRAY), anim="fade")
    fonte(c, t, 57.6)


def s08(c, t):  # 63.2 - fim  pergunta + segue
    floor(c)
    show(c, t, 63.3, CX, 280, M("Em qual faixa", 86, NAVY), anim="stamp")
    show(c, t, 63.4, CX, 390, M("você ficou?", 86, NAVY), anim="stamp")
    show(c, t, 64.9, 640, 560, group(lambda c: speech(c, 460, 130, -170, 110), T("Comenta!", 66)), anim="pop")
    show(c, t, 65.7, CX, 760, lambda c: ribbon(c, "SEGUE PRA MAIS CONTAS", NAVY, 58), anim="stamp")
    hero(c, t, 330, FY, 0.7, [(0, "point_r"), (65.7, "finger_up")], [(0, "happy"), (65.7, "grin")], look=0.5)
    show(c, t, 66.0, 760, 1060, M("FAZ A CONTA", 60, GOLD), anim="up")


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 5.84, s01), (5.84, 6.96, s02), (6.96, 11.4, s03), (11.4, 22.0, s04), (22.0, 39.3, s05),
    (39.3, 57.4, s06), (57.4, 63.2, s07), (63.2, 999.0, s08),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
