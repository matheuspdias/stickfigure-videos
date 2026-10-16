"""R$ 10 por dia te deixa milionário? Só TikTok: vertical nativo 1080x1920, 72,3 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Premissa do vídeo "primeiros 100 mil": 0,8% a.m. líquido, R$ 300 por mês (contas no roteiro.txt).
Layout como o de amortizacao-mcmv: pés em y=1230 e tudo deslocado +60 (SHIFT)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60

SFX = [(3.85, "tum"), (27.6, "tum"), (41.6, "tum"), (67.45, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


# --------------------------------------------------------------- gráfico da curva
R = 0.008
P = 300.0


def fv(m):
    return P * ((1 + R) ** m - 1) / R


GX0, GX1, GY0, GY1 = 110, 790, 1100, 470   # eixo: x de 0 a 420 meses, y de 0 a 1,03 milhão
VMAX = fv(420)


def gx(m):
    return GX0 + (GX1 - GX0) * m / 420


def gy(v):
    return GY0 - (GY0 - GY1) * v / VMAX


# (t, mês): a curva anda junto com a narração e para em cada degrau
CURVE_KEYS = [(15.7, 0), (16.6, 120), (19.1, 120), (19.9, 240), (22.3, 240), (23.3, 360), (25.6, 360), (27.5, 420)]


def curve_month(t):
    if t <= CURVE_KEYS[0][0]:
        return 0
    for (t0, m0), (t1, m1) in zip(CURVE_KEYS, CURVE_KEYS[1:]):
        if t <= t1:
            return m0 + (m1 - m0) * ease_io((t - t0) / (t1 - t0)) if t1 > t0 else m1
    return 420


def axes(c):
    line(c, GX0, GY0, GX1 + 40, GY0, 6)
    line(c, GX0, GY0, GX0, GY1 - 40, 6)
    for m, lab in ((120, "10"), (240, "20"), (360, "30"), (420, "35")):
        line(c, gx(m), GY0 - 10, gx(m), GY0 + 10, 5)
        text(c, lab, gx(m), GY0 + 45, 44, MARKER, DGRAY)
    text(c, "anos", GX0 + 20, GY0 + 45, 40, HAND, DGRAY, align="l")


def draw_curve(c, m_end, col=GREEN, lw=11):
    if m_end <= 0:
        return
    n = max(2, int(m_end / 3))
    c.move_to(gx(0), gy(0))
    for i in range(1, n + 1):
        m = m_end * i / n
        c.line_to(gx(m), gy(fv(m)))
    rgb(c, col); c.set_line_width(lw); c.set_line_cap(1); c.set_line_join(1); c.stroke()


def dot(m, col=GREEN):
    return lambda c: circle(c, 0, 0, 16, col, 5)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.3  gancho
    floor(c)
    show(c, t, 0.0, CX, 290, lambda c: hl(c, "R$ 10 por dia", 0, 0, 96, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 1.6, 300, 930, group(sc(sandwich, s=1.1), at(0, 150, T("um lanche", 52, DGRAY))), anim="pop")
    show(c, t, 3.85, CX, 500, M("R$ 1 MILHÃO", 128, GREEN), anim="stamp", d=0.35)
    show(c, t, 4.3, CX, 630, T("pode virar isso?", 56, DGRAY), anim="up")
    hero(c, t, 760, FY, 0.85, [(0, "present_l"), (3.85, "arms_up")], [(0, "confident"), (3.85, "shocked")],
         appear=0.0, look=-0.4)


def s02(c, t):  # 5.3 - 15.6  R$ 300 por mês, 0,8% ao mês
    floor(c)
    show(c, t, 5.5, CX, 260, M("R$ 10 x 30 dias", 78, NAVY), anim="up")
    show(c, t, 7.0, CX, 390, lambda c: hl(c, "= R$ 300 por mês", 0, 0, 80, LGREEN), anim="stamp")
    show(c, t, 6.4, 230, 690, lambda c: calendar(c, "30"), anim="pop")
    show(c, t, 9.3, 590, 600, T("investindo, rendendo:", 46, DGRAY), anim="fade")
    show(c, t, 10.5, 590, 700, lambda c: hl(c, "0,8% ao mês", 0, 0, 72, LYELLOW), anim="stamp")
    show(c, t, 12.6, 590, 800, T("(já sem o imposto)", 44, DGRAY), anim="up")
    show(c, t, 14.0, 590, 920, M("uns 10% ao ano", 62, GREEN), anim="pop")
    hero(c, t, 870, FY, 0.5, [(0, "relax"), (7.0, "thumb"), (10.5, "present_l")], [(0, "neutral"), (7.0, "happy")],
         prop=("r", prop_calculator), look=-1)


def s03(c, t):  # 15.6 - 29.1  a escada: 10, 20, 30 e 35 anos
    floor(c)
    title(c, t, 15.7, "R$ 300 por mês, investidos", y=260, size=62)
    axes(c)
    m = curve_month(t)
    draw_curve(c, m)
    if m > 0:
        circle(c, gx(m), gy(fv(m)), 14, GREEN, 5)
    show(c, t, 16.4, gx(120) - 30, gy(fv(120)) - 80, M("R$ 60 mil", 52), anim="pop")
    show(c, t, 19.7, gx(240) - 150, gy(fv(240)) - 75, M("R$ 216 mil", 56), anim="pop")
    show(c, t, 23.4, gx(360) - 230, gy(fv(360)) - 60, M("R$ 620 mil", 62), anim="pop")
    show(c, t, 27.6, 480, 400, lambda c: hl(c, "R$ 1 MILHÃO", 0, 0, 92, LGREEN), anim="stamp", d=0.35)
    hero(c, t, 920, FY, 0.45, [(0, "present_l"), (19.7, "point_lu"), (27.6, "arms_up")],
         [(0, "neutral"), (19.7, "happy"), (27.6, "grin")], look=-1)


def s04(c, t):  # 29.1 - 37.6  a curva acelera
    floor(c)
    show(c, t, 29.3, CX, 260, M("Repara na curva", 76, NAVY), anim="up")
    axes(c)
    draw_curve(c, 420)
    # últimos 5 anos: de 623 mil para 1,03 milhão
    if t > 30.8:
        k = ease_out(prog(t, 30.8, 0.7))
        y0, y1 = gy(fv(360)), gy(fv(420))
        c.save(); c.set_dash([14, 10])
        line(c, gx(360), y0, GX1 + 20, y0, 4, GREEN)
        c.restore()
        line(c, GX1 + 20, y0, GX1 + 20, y0 + (y1 - y0) * k, 12, GREEN)
    show(c, t, 33.2, 480, 520, group(M("+ R$ 405 mil", 68, GREEN), at(0, 65, T("só nos últimos 5 anos", 44, GREEN))),
         anim="pop")
    # primeiros 25 anos: de 0 a 372 mil
    if t > 35.2:
        k = ease_out(prog(t, 35.2, 0.6))
        yt = gy(fv(300))
        line(c, gx(300), GY0, gx(300), GY0 + (yt - GY0) * k, 12, NAVY)
        if t > 35.6:
            circle(c, gx(300), yt, 13, NAVY, 5)
    show(c, t, 35.7, 330, gy(fv(300)) - 20, group(M("R$ 372 mil", 54, NAVY), at(0, 58, T("em 25 anos", 42, NAVY))),
         anim="pop")
    hero(c, t, 920, FY, 0.45, [(0, "think"), (33.2, "point_lu"), (36.8, "head")],
         [(0, "think"), (33.2, "happy"), (36.8, "shocked")], look=-1)


def s05(c, t):  # 37.6 - 47.1  a virada: do bolso x juros
    floor(c)
    show(c, t, 37.8, CX, 260, stamp_txt("A PARTE QUE ASSUSTA", RED, 62), anim="stamp")
    bx, bw, base, htot = 270, 230, 1110, 600
    hb = htot * 126000 / VMAX
    line(c, bx - bw / 2 - 30, base, bx + bw / 2 + 30, base, 6)
    if t > 39.3:   # contorno do milhão inteiro, esperando ser preenchido
        c.save(); c.set_dash([18, 12])
        rrect(c, bx - bw / 2, base - htot, bw, htot, 8); rgb(c, GRAY); c.set_line_width(5); c.stroke()
        c.restore()
        text(c, "R$ 1 milhão", bx, base - htot - 45, 50, MARKER, DGRAY)
    if t > 39.7:
        k = ease_out(prog(t, 39.7, 0.5))
        rrect(c, bx - bw / 2, base - hb * k, bw, hb * k, 8); fs(c, NAVY, 6)
    if t > 43.9:
        k = ease_out(prog(t, 43.9, 1.0))
        hj = (htot - hb) * k
        rrect(c, bx - bw / 2, base - hb - hj, bw, hj, 8); fs(c, GREEN, 6)
    show(c, t, 41.0, 440, base - hb / 2 - 10, group(L("do seu bolso", 44, NAVY), at(0, 52, lambda c: text(
        c, "R$ 126 mil", 0, 0, 56, MARKER, NAVY, align="l"))), anim="left", d=0.3)
    show(c, t, 44.9, 440, base - hb - (htot - hb) / 2 - 20, group(L("juros", 46, GREEN), at(0, 58, lambda c: text(
        c, "R$ 902 mil", 0, 0, 62, MARKER, GREEN, align="l"))), anim="left", d=0.3)
    show(c, t, 45.6, 560, 370, lambda c: hl(c, "quase 90% = JUROS", 0, 0, 66, LGREEN), anim="stamp")
    hero(c, t, 920, FY, 0.45, [(0, "relax"), (41.6, "head"), (45.6, "arms_up")],
         [(0, "neutral"), (41.6, "shocked"), (45.6, "grin")], look=-1)


def s06(c, t):  # 47.1 - 53.7  o detalhe honesto
    floor(c)
    show(c, t, 47.3, CX, 260, M("Sendo honesto...", 78, NAVY), anim="up")
    show(c, t, 49.0, 260, 620, group(lambda c: calendar(c, "35"), at(0, 160, T("anos", 50, DGRAY))), anim="pop")
    show(c, t, 50.9, 650, 620, group(sc(cart, s=1.2), at(0, 160, M("inflação", 54, RED))), anim="pop")
    show(c, t, 52.3, 450, 900, lambda c: hl(c, "R$ 1 milhão", 0, 0, 70, LYELLOW), anim="stamp")
    show(c, t, 52.7, 450, 1000, T("vai comprar bem menos que hoje", 44, RED), anim="up")
    hero(c, t, 900, FY, 0.45, [(0, "present_l"), (51.0, "shrug")], [(0, "neutral"), (51.0, "worried")], look=-1)


def s07(c, t):  # 53.7 - 68.2  quem não começa tem zero
    floor(c)
    show(c, t, 54.4, 420, 620, group(lambda c: speech(c, 560, 150, -200, 110), T("então não vale a pena", 50)),
         anim="pop", d=0.3, t1=59.3)
    show(c, t, 59.7, CX, 260, M("daqui a 35 anos:", 74, NAVY), anim="up")
    rows = [(63.45, "R$ 1 milhão", 63.85), (64.45, "R$ 600 mil", 65.0), (66.15, "R$ 60 mil", 66.75)]
    for i, (t0, s, tx) in enumerate(rows):
        y = 440 + i * 120
        show(c, t, t0, 600, y, M(s, 64, DGRAY), anim="pop", d=0.3)
        if t > tx:
            k = ease_out(prog(t, tx, 0.25))
            w = 360
            line(c, 600 - w / 2, y + 18, 600 - w / 2 + w * k, y - 18, 11, RED)
    show(c, t, 61.85, 600, 860, stamp_txt("R$ 0", RED, 150), anim="stamp", d=0.35)
    show(c, t, 67.45, 600, 1010, lambda c: hl(c, "TEM ZERO", 0, 0, 70, (1, 0.8, 0.76)), anim="stamp")
    other(c, t, 230, FY, 0.6, [(0, "shrug"), (59.7, "relax"), (61.85, "head")],
          [(0, "confident"), (59.7, "neutral"), (61.85, "shocked")], look=0.6)


def s08(c, t):  # 68.2 - fim  pergunta final
    floor(c)
    show(c, t, 68.4, CX, 280, M("Quantos anos", 92, NAVY), anim="up")
    show(c, t, 68.9, CX, 400, M("você tem?", 92, NAVY), anim="up")
    show(c, t, 69.8, 640, 720, group(lambda c: speech(c, 470, 140, -160, 110), M("Comenta aí!", 62, NAVY)), anim="pop")
    show(c, t, 70.6, 640, 880, T("eu te digo com quantos", 46, DGRAY), anim="fade")
    show(c, t, 71.0, 640, 940, T("você chega no milhão", 46, DGRAY), anim="fade")
    hero(c, t, 260, FY, 0.75, [(0, "think"), (69.8, "point_r")], [(0, "think"), (69.8, "grin")], look=1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 5.3, s01), (5.3, 15.6, s02), (15.6, 29.1, s03), (29.1, 37.6, s04), (37.6, 47.1, s05),
    (47.1, 53.7, s06), (53.7, 68.2, s07), (68.2, 999.0, s08),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
