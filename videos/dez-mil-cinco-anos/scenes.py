"""R$ 10 mil há 5 anos: onde você estaria mais rico hoje? Só TikTok: vertical nativo 1080x1920, 88,5 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Período 15/10/2021 -> 16/10/2026, valores líquidos de IR (premissas no roteiro.txt).
Layout: desenhado com pés em FY=1230 e deslocado SHIFT=60 (pés no quadro final em 1290); nada importante em x > 930."""
from engine import *  # noqa

VERTICAL = True

CX = 500
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)

SFX = [(18.6, "tum"), (31.8, "tum"), (53.8, "soft_ding"), (64.2, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- ícones dos seis investimentos
def btc_coin(c):
    circle(c, 0, 0, 92, GOLD, 7)
    circle(c, 0, 0, 70, None, 4)
    for dx in (-14, 12):
        line(c, dx, -66, dx, -44, 8)
        line(c, dx, 44, dx, 66, 8)
    text(c, "B", 4, 4, 104, MARKER, INK)


def stock_chart(c):
    rrect(c, -110, -90, 220, 180, 14); fs(c, WHITE, 6)
    pts = [(-85, 55), (-50, 15), (-20, 35), (15, -15), (45, 0), (85, -60)]
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    rgb(c, GREEN); c.set_line_width(10); c.stroke()
    poly(c, [(85, -60), (58, -58), (82, -36)]); fs(c, GREEN, 4)


def fii_icon(c):
    c.save(); c.translate(0, 100); c.scale(0.55, 0.55); apartment(c, LYELLOW, None, 4); c.restore()


def tesouro_icon(c):
    document(c, "IPCA+", NAVY, 40)


def poup_icon(c):
    c.save(); c.scale(0.8, 0.8); piggy(c); c.restore()


def cdb_icon(c):
    c.save(); c.scale(0.95, 0.95); bank(c); c.restore()


def trophy(c, col=GOLD, label="1"):
    poly(c, [(-80, -110), (80, -110), (60, -10), (0, 30), (-60, -10)]); fs(c, col, 7)
    for s in (-1, 1):
        c.move_to(s * 78, -95); c.curve_to(s * 140, -95, s * 130, -20, s * 52, -20)
        rgb(c, INK); c.set_line_width(7); c.stroke()
    c.rectangle(-14, 28, 28, 50); fs(c, col, 6)
    rrect(c, -62, 76, 124, 34, 6); fs(c, BROWN, 6)
    text(c, label, 0, -55, 70, MARKER, INK)


ICONS = {"btc": btc_coin, "ifix": fii_icon, "poup": poup_icon, "tes": tesouro_icon, "ibov": stock_chart, "cdb": cdb_icon}
ORDER = ["btc", "ifix", "poup", "tes", "ibov", "cdb"]
LABEL = {"btc": "bitcoin", "ifix": "FIIs", "poup": "poupança", "tes": "Tesouro IPCA+", "ibov": "Ibovespa", "cdb": "CDB 100% CDI"}
VAL = {"btc": 12.3, "ifix": 14.4, "poup": 14.6, "tes": 15.3, "ibov": 16.7, "cdb": 17.0}


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def badge(rank, col=NAVY):
    def f(c):
        w = text_w(c, f"{rank}º LUGAR", 76) + 70
        rrect(c, -w / 2, -62, w, 124, 30); fs(c, col, 6)
        text(c, f"{rank}º LUGAR", 0, 4, 76, MARKER, WHITE)
    return f


def money(s, bg=LGREEN, size=112):
    return lambda c: hl(c, s, 0, 0, size, bg)


def ladder(c, t, shown):
    """placar lateral: os lugares já revelados, do 6º (embaixo) ao 1º (em cima)"""
    for i, k in enumerate(ORDER):
        if k not in shown:
            continue
        y = 1020 - i * 64
        rank = 6 - i
        rrect(c, 40, y - 26, 250, 52, 10); fs(c, WHITE if rank > 1 else LYELLOW, 4)
        text(c, f"{rank}º", 70, y + 2, 34, MARKER, NAVY)
        text(c, f"{VAL[k]:.1f}".replace(".", ",") + " mil", 270, y + 2, 34, HAND, INK, align="r")


# ======================================================================= CENAS
def s01(c, t):  # 0 - 8.0 gancho
    floor(c)
    show(c, t, 0.0, CX, 300, money("R$ 10.000", LGREEN, 130), anim="stamp", d=0.35)
    show(c, t, 1.4, CX, 440, M("5 anos atrás", 80, NAVY), anim="up")
    for i, k in enumerate(ORDER):
        x = 200 + (i % 3) * 300
        y = 640 + (i // 3) * 230
        show(c, t, 3.0 + i * 0.22, x, y, sc(ICONS[k], s=0.85), anim="pop")
    if t > 5.0:
        show(c, t, 5.3, CX, 1080, lambda c: hl(c, "quem ganhou?", 0, 0, 64, LYELLOW), anim="stamp", t1=6.4)
        show(c, t, 6.5, CX, 1080, lambda c: hl(c, "o mais sem graça", 0, 0, 64, PINKISH), anim="stamp")
    hero(c, t, 880, FY, 0.55, [(0, "present_l"), (5.0, "think"), (6.6, "shrug")],
         [(0, "happy"), (5.0, "think"), (6.6, "grin")], look=-1)


def s02(c, t):  # 8.0 - 15.9 período, IR, do pior pro melhor
    floor(c)
    show(c, t, 8.6, 260, 380, group(sc(calendar, "21", NAVY, 72, s=1.2), at(0, 130, T("out/2021", 52))), anim="pop")
    arrow_draw(c, t, 10.2, 390, 380, 600, 380, col=NAVY, lw=9)
    show(c, t, 10.6, 740, 380, group(sc(calendar, "26", GREEN, 72, s=1.2), at(0, 130, T("hoje", 52))), anim="pop")
    show(c, t, 11.8, CX, 650, lambda c: hl(c, "IR já descontado", 0, 0, 70, LYELLOW), anim="stamp")
    show(c, t, 14.3, CX, 820, M("do pior", 66, RED), anim="up")
    arrow_draw(c, t, 14.9, 330, 900, 670, 900, col=INK, lw=8, bend=0)
    show(c, t, 15.3, CX, 980, M("pro melhor", 66, GREEN), anim="up")
    hero(c, t, 880, FY, 0.55, [(0, "relax"), (11.8, "finger_up"), (14.3, "present_l")],
         [(0, "neutral"), (11.8, "confident"), (14.3, "happy")], prop=("l", prop_calculator), look=-1)


def rank_scene(c, t, key, rank, t_rank, t_icon, t_val, val, pct, label, sub=None, t_sub=None, hero_kw=None):
    floor(c)
    show(c, t, t_rank, CX, 260, badge(rank, GOLD if rank == 1 else NAVY), anim="stamp")
    show(c, t, t_icon, CX, 520, sc(ICONS[key], s=1.35), anim="pop")
    show(c, t, t_icon + 0.2, CX, 710, M(label, 70, NAVY), anim="up")
    if sub:
        show(c, t, t_sub, CX, 790, T(sub, 48, DGRAY), anim="up")
    show(c, t, t_val, CX, 920, money(val, LGREEN if rank > 1 else LYELLOW), anim="stamp")
    show(c, t, t_val + 0.5, CX, 1040, T(pct, 54, GREEN), anim="up")
    hero(c, t, 860, FY, 0.55, **(hero_kw or {}))


def s03(c, t):  # 15.9 - 20.7 6º bitcoin
    rank_scene(c, t, "btc", 6, 16.1, 17.8, 18.6, "R$ 12.300", "+23% em 5 anos", "bitcoin",
               hero_kw=dict(poses=[(0, "relax"), (18.6, "head")], exprs=[(0, "neutral"), (18.6, "shocked")], look=-1))


def s04(c, t):  # 20.7 - 28.7 5º IFIX
    rank_scene(c, t, "ifix", 5, 20.9, 21.9, 26.7, "R$ 14.400", "+44%", "fundos imobiliários",
               sub="média do mercado (IFIX), com rendimentos", t_sub=24.6,
               hero_kw=dict(poses=[(0, "think"), (26.7, "thumb")], exprs=[(0, "think"), (26.7, "happy")], look=-1))


def s05(c, t):  # 28.7 - 36.1 4º poupança, na frente dos FIIs
    floor(c)
    show(c, t, 28.8, CX, 260, badge(4), anim="stamp")
    show(c, t, 30.6, CX, 500, sc(poup_icon, s=1.5), anim="pop", t1=33.6)
    show(c, t, 30.8, CX, 690, M("poupança", 76, NAVY), anim="up", t1=33.6)
    show(c, t, 31.8, CX, 850, money("R$ 14.600"), anim="stamp", t1=33.7)
    if t > 33.8:
        base = 1080
        for i, (lab, v, col) in enumerate((("poupança", 14.6, GREEN), ("FIIs", 14.4, LGRAY))):
            x = 330 + i * 330
            k = ease_out(prog(t, 33.9 + i * 0.25, 0.5))
            h = (v - 10) * 60 * k
            c.save(); c.translate(x, base); bar(c, h, 170, col, lab, f"{v:.1f}".replace(".", ",") + " mil" if k > 0.95 else None, 44); c.restore()
        show(c, t, 34.9, CX, 520, lambda c: hl(c, "passou os FIIs!", 0, 0, 72, LYELLOW), anim="stamp")
    hero(c, t, 880, FY, 0.55, [(0, "relax"), (29.7, "point_l"), (33.9, "hips")],
         [(0, "neutral"), (29.7, "shocked"), (33.9, "grin")], look=-1)


def s06(c, t):  # 36.1 - 43.0 3º Tesouro IPCA+
    rank_scene(c, t, "tes", 3, 36.3, 37.4, 41.3, "R$ 15.300", "+53%", "Tesouro IPCA+",
               sub="o que venceu em 2026", t_sub=39.4,
               hero_kw=dict(poses=[(0, "present_l"), (41.3, "thumb")], exprs=[(0, "neutral"), (41.3, "happy")], look=-1))


def s07(c, t):  # 43.0 - 49.0 2º Ibovespa
    rank_scene(c, t, "ibov", 2, 43.2, 44.2, 47.0, "R$ 16.700", "+67%", "Ibovespa",
               sub="média da bolsa (Ibovespa), com dividendos", t_sub=45.8,
               hero_kw=dict(poses=[(0, "relax"), (47.0, "arms_up")], exprs=[(0, "neutral"), (47.0, "grin")], look=-1))


def s08(c, t):  # 49.0 - 58.8 1º CDB 100% CDI, renda fixa > bolsa
    floor(c)
    show(c, t, 49.3, CX, 260, badge(1, GOLD), anim="stamp")
    if t < 55.6:
        show(c, t, 49.6, CX - 170, 520, sc(trophy, s=1.2), anim="drop")
        show(c, t, 50.8, CX + 170, 520, sc(cdb_icon, s=1.2), anim="pop")
        show(c, t, 51.0, CX, 720, M("CDB 100% do CDI", 72, NAVY), anim="up")
        show(c, t, 53.8, CX, 880, money("R$ 17.000", LYELLOW, 120), anim="stamp")
        show(c, t, 54.3, CX, 1010, T("+70%", 58, GREEN), anim="up")
        for i in range(5):
            show(c, t, 53.9 + i * 0.08, CX - 330 + i * 165, 360 + (i % 2) * 30, sc(sparkle, 22, GOLD), anim="pop")
    else:
        show(c, t, 55.7, CX, 420, M("renda fixa básica", 66, NAVY), anim="up")
        base = 1000
        for i, (lab, v, col) in enumerate((("CDI", 17.0, GREEN), ("bolsa", 16.7, BLUE))):
            x = 330 + i * 340
            k = ease_out(prog(t, 55.9 + i * 0.3, 0.5))
            h = (v - 10) * 40 * k
            c.save(); c.translate(x, base); bar(c, h, 180, col, lab, (f"{v:.1f}".replace(".", ",") + " mil") if k > 0.95 else None, 48); c.restore()
        show(c, t, 57.6, CX, 530, lambda c: hl(c, "ganhou da bolsa", 0, 0, 70, LYELLOW), anim="stamp")
    hero(c, t, 880, FY, 0.55, [(0, "relax"), (53.8, "arms_up"), (55.7, "present_l")],
         [(0, "neutral"), (53.8, "grin"), (55.7, "confident")], look=-1)


def btc_path(c, t):
    """linha dos R$ 10 mil em bitcoin: out/21 10k -> nov/22 2,5k -> out/25 20k -> hoje 12,3k"""
    x0, x1, ytop, ybot = 90, 900, 380, 1000
    def Y(v):
        return ybot - (v / 22.0) * (ybot - ytop)
    def X(year):
        return x0 + (year - 2021.8) / 5.0 * (x1 - x0)
    line(c, x0, ybot, x1, ybot, 5, DGRAY)
    c.save(); c.set_dash([16, 12]); line(c, x0, Y(10), x1, Y(10), 4, LGRAY); c.restore()
    text(c, "10 mil", x0 + 10, Y(10) - 28, 38, HAND, DGRAY, align="l")
    for yr in (2022, 2023, 2024, 2025, 2026):
        text(c, str(yr), X(yr), ybot + 40, 34, HAND, DGRAY)
    pts = [(2021.8, 10.0, 62.1), (2022.2, 6.2, 63.0), (2022.6, 3.6, 63.6), (2022.88, 2.5, 64.2),
           (2023.5, 5.5, 66.9), (2024.2, 11.5, 67.4), (2024.95, 16.5, 67.9), (2025.77, 20.0, 68.2),
           (2026.2, 13.0, 70.2), (2026.79, 12.3, 71.0)]
    c.move_to(X(pts[0][0]), Y(pts[0][1]))
    drawn = False
    for (ya, va, ta), (yb, vb, tb) in zip(pts, pts[1:]):
        if t < ta:
            break
        k = clamp01((t - ta) / max(0.05, tb - ta))
        c.line_to(X(ya) + (X(yb) - X(ya)) * k, Y(va) + (Y(vb) - Y(va)) * k)
        drawn = True
        if k < 1:
            break
    if drawn:
        rgb(c, ORANGE); c.set_line_width(11); c.stroke()
    else:
        c.new_path()
    if t > 64.2:
        circle(c, X(2022.88), Y(2.5), 14, RED, 4)
        show(c, t, 64.3, X(2022.88) + 170, Y(2.5) - 40, lambda c: hl(c, "R$ 2.500", 0, 0, 52, PINKISH), anim="stamp")
    if t > 68.1:
        circle(c, X(2025.77), Y(20.0), 14, GREEN, 4)
        show(c, t, 68.2, X(2025.77) - 160, Y(20.0) - 10, lambda c: hl(c, "~R$ 20.000", 0, 0, 52, LGREEN), anim="stamp")
    if t > 71.0:
        circle(c, X(2026.79), Y(12.3), 14, NAVY, 4)
        show(c, t, 71.1, X(2026.79) - 120, Y(12.3) + 75, lambda c: hl(c, "R$ 12.300", 0, 0, 52, LYELLOW), anim="stamp")


def s09(c, t):  # 58.8 - 72.6 o caminho do bitcoin
    show(c, t, 59.0, CX, 250, sc(btc_coin, s=0.55), anim="pop", t1=60.3)
    show(c, t, 60.4, CX, 250, M("o caminho do bitcoin", 70, NAVY), anim="up")
    show(c, t, 62.0, 0, 0, lambda c: btc_path(c, t), anim="fade", d=0.2)
    hero(c, t, 880, FY, 0.42, [(0, "point_lu"), (64.2, "head"), (68.1, "arms_up"), (71.0, "shrug")],
         [(0, "neutral"), (64.2, "desperate"), (68.1, "grin"), (71.0, "worried")], look=-1)


def wave_line(amp, col, label):
    def f(c):
        c.move_to(-180, 0)
        for i in range(1, 47):
            x = -180 + i * 7.8
            c.line_to(x, -math.sin(i * 0.55) * amp - i * 1.6)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, label, 0, 150, 46, HAND, INK)
    return f


def s10(c, t):  # 72.6 - 85.3 detalhe honesto
    floor(c)
    show(c, t, 72.9, CX, 260, lambda c: ribbon(c, "DETALHE HONESTO", NAVY, 60), anim="stamp")
    if t < 78.6:
        show(c, t, 75.6, CX, 450, M("o que aconteceu", 66, INK), anim="up")
        show(c, t, 76.8, CX, 560, sc(neq, 50, RED), anim="pop")
        show(c, t, 77.4, CX, 670, M("o que vai acontecer", 66, INK), anim="up")
    elif t < 82.3:
        show(c, t, 78.7, CX, 470, group(T("venceu nesses 5 anos", 58, GREEN)), anim="up")
        arrow_draw(c, t, 80.3, CX, 540, CX, 700, col=RED, lw=10, bend=0)
        show(c, t, 80.6, CX, 770, M("pode perder nos próximos", 62, RED), anim="up")
    else:
        show(c, t, 82.3, 290, 560, wave_line(18, GREEN, "risco menor"), anim="fade")
        show(c, t, 83.4, 720, 560, wave_line(110, RED, "risco maior"), anim="fade")
        show(c, t, 84.1, CX, 880, lambda c: hl(c, "queda maior no caminho", 0, 0, 60, PINKISH), anim="stamp")
    hero(c, t, 880, FY, 0.52, [(0, "finger_up"), (78.7, "present_l"), (82.3, "think")],
         [(0, "confident"), (78.7, "neutral"), (82.3, "think")], prop=("l", prop_pointer), look=-1)


def s11(c, t):  # 85.3 - fim pergunta final
    floor(c)
    show(c, t, 85.5, CX, 260, M("Em qual você", 84, NAVY), anim="stamp")
    show(c, t, 86.2, CX, 360, M("colocaria os 10 mil?", 70, NAVY), anim="up")
    for i, k in enumerate(ORDER):
        x = 200 + (i % 3) * 300
        y = 560 + (i // 3) * 250
        show(c, t, 86.0 + i * 0.12, x, y, group(sc(ICONS[k], s=0.7), at(0, 110, T(LABEL[k], 40))), anim="pop")
    show(c, t, 87.7, CX - 60, 1080, group(lambda c: speech(c, 500, 120, -150, 100), T("Comenta aí!", 62)), anim="pop")
    hero(c, t, 880, FY, 0.55, [(0, "present_l"), (87.7, "wave")], [(0, "happy"), (87.7, "grin")], look=-1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 8.0, s01), (8.0, 15.9, s02), (15.9, 20.7, s03), (20.7, 28.7, s04), (28.7, 36.1, s05),
    (36.1, 43.0, s06), (43.0, 49.0, s07), (49.0, 58.8, s08), (58.8, 72.6, s09), (72.6, 85.3, s10),
    (85.3, 999.0, s11),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
