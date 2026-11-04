"""Black Friday: o truque do "metade do dobro". Só TikTok: vertical nativo 1080x1920, 69,1 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout vertical: título y~250, palco y 360-1230 (pés dos bonecos em y=1230, +SHIFT no quadro final),
abaixo de y 1500 fica a interface do TikTok. Nada importante em x > 930 (botões da direita).
Premissas (pesquisadas em 04/11/2026): Black Friday 2026 = sexta, 27/11; desconto falso = publicidade
enganosa (CDC art. 37); arrependimento de 7 dias em compra fora da loja/internet (CDC art. 49).
Sem nomes de loja, marca, site ou extensão."""
from engine import *  # noqa

VERTICAL = True

CX = 500
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
D2000 = "R$ 2 .000"   # Permanent Marker some o ponto depois do 2

SFX = [(4.45, "tum"), (22.4, "tum"), (51.4, "tum"), (66.95, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def buyer(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 2)
    other(c, t, x, FY, s, poses, exprs, **kw)


def strike(w=260, col=RED, lw=10):
    return lambda c: line(c, -w / 2, 10, w / 2, -10, lw, col)


def stamp_txt(s, col=RED, size=78, rot=-0.08):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(rot)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, PAPER, 0.85); c.fill_preserve()
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def badge(n, col=NAVY):
    def f(c):
        circle(c, 0, 0, 58, col, 6)
        text(c, str(n), 0, 4, 78, MARKER, WHITE)
    return f


def off_burst(s="50% OFF", col=RED, size=70):
    def f(c):
        pts = []
        for i in range(24):
            a = i * math.pi / 12
            r = 190 if i % 2 == 0 else 150
            pts.append((math.cos(a) * r, math.sin(a) * r * 0.62))
        poly(c, pts); fs(c, col, 6)
        text(c, s, 0, 4, size, MARKER, WHITE)
    return f


def mini_chart(c, t, t0, w=640, h=380):
    """cartão com gráfico de histórico de preço: plano, pico em novembro, volta ao mesmo valor"""
    rrect(c, -w / 2, -h / 2, w, h, 18); fs(c, WHITE, 6)
    text(c, "histórico de preço", -w / 2 + 30, -h / 2 + 42, 40, HAND, DGRAY, align="l")
    x0, x1 = -w / 2 + 50, w / 2 - 40
    yb = h / 2 - 70
    line(c, x0, yb, x1, yb, 4, LGRAY)
    pts = [(0.0, 0.35), (0.25, 0.35), (0.45, 0.36), (0.62, 0.35), (0.70, 0.85), (0.86, 0.85), (0.92, 0.35), (1.0, 0.35)]
    k = clamp01((t - t0) / 1.4)
    P = [(x0 + (x1 - x0) * px, yb - (h - 150) * py) for px, py in pts]
    c.save()
    c.rectangle(x0 - 10, -h / 2, (x1 - x0 + 20) * k, h); c.clip()
    c.move_to(*P[0])
    for p in P[1:]:
        c.line_to(*p)
    rgb(c, BLUE); c.set_line_width(8); c.set_line_join(1); c.stroke()
    c.restore()
    for lab, px in (("ago", 0.05), ("set", 0.3), ("out", 0.55), ("nov", 0.8)):
        text(c, lab, x0 + (x1 - x0) * px, yb + 36, 34, HAND, DGRAY)


def storefront(name, price, col=LBLUE, pcol=INK, s=1.0):
    def f(c):
        c.save(); c.scale(s, s)
        rrect(c, -110, -60, 220, 200, 8); fs(c, WHITE, 6)
        for i in range(5):
            c.rectangle(-120 + i * 48, -110, 48, 50)
            fs(c, col if i % 2 == 0 else WHITE, 4)
        rrect(c, -40, 40, 80, 100, 4); fs(c, LGRAY, 5)
        text(c, name, 0, -10, 40, MARKER, NAVY)
        c.restore()
        c.save(); c.translate(0, 205 * s); price_tag(c, price, YELLOW, 40, pcol); c.restore()
    return f


def flash(c, t, t0, d=0.35):
    k = (t - t0) / d
    if 0 <= k <= 1:
        c.save(); c.identity_matrix(); c.rectangle(0, 0, W, H)
        rgb(c, WHITE, 0.85 * (1 - k)); c.fill(); c.restore()


def phone_print(c, t, t0):
    """celular com o preço na tela e um carimbo de data (print)"""
    rrect(c, -150, -270, 300, 540, 34); fs(c, NAVY, 7)
    rrect(c, -128, -230, 256, 440, 10); fs(c, WHITE, 3)
    c.save(); c.translate(0, -120); c.scale(0.55, 0.55); tv(c); c.restore()
    text(c, "R$ 1.000", 0, 30, 48, MARKER, INK)
    if t > t0:
        text(c, "hoje", 0, 110, 44, HAND, BLUE)
        circle(c, 0, 230, 14, LGRAY, 3)


def parcel(c):
    """caixa de entrega simples (sem rótulo)"""
    rrect(c, -110, -80, 220, 160, 8); fs(c, (0.82, 0.66, 0.45), 6)
    c.rectangle(-22, -80, 44, 160); rgb(c, (0.93, 0.85, 0.66)); c.fill()
    line(c, -110, -80, 110, -80, 6)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 7.0  gancho: TV, 50% OFF ... custava 1.000 semana passada
    floor(c)
    show(c, t, 0.0, CX, 260, lambda c: hl(c, "BLACK FRIDAY", 0, 0, 92, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 0.0, CX, 590, sc(tv, LBLUE, s=1.35), anim="pop", d=0.3)
    show(c, t, 0.85, CX - 20, 595, lambda c: text(c, "R$ 1.000", 0, 0, 82, MARKER, INK), anim="pop")
    show(c, t, 2.2, CX + 230, 400, off_burst("50% OFF", RED, 58), anim="stamp", rot=0.12)
    if t > 4.4:
        show(c, t, 4.4, CX, 880, group(sc(calendar, "-7", NAVY, 60, s=0.8),
                                       at(150, 0, lambda c: text(c, "semana passada:", 0, -25, 46, HAND, INK, align="l")),
                                       at(150, 0, lambda c: text(c, "R$ 1.000", 0, 35, 66, MARKER, RED, align="l"))),
             anim="up")
    hero(c, t, 170, FY, 0.62, [(0, "point_r"), (4.4, "head")], [(0, "happy"), (4.4, "shocked")], look=1)
    buyer(c, t, 820, 0.62, [(0, "arms_up"), (5.0, "shrug")], [(0, "grin"), (5.0, "worried")], look=-1)


def s02(c, t):  # 7.0 - 9.3  nome do truque
    floor(c)
    show(c, t, 7.1, CX, 420, M("O truque da", 82, NAVY), anim="up")
    show(c, t, 7.7, CX, 590, lambda c: hl(c, "METADE DO DOBRO", 0, 0, 96, PINKISH), anim="stamp")
    show(c, t, 8.4, CX, 760, lambda c: text(c, "x2  depois  ÷2", 0, 0, 64, MARKER, RED), anim="up")
    hero(c, t, CX, FY, 0.75, [(0, "present"), (8.4, "finger_up")], [(0, "neutral"), (8.4, "confident")], look=0)


# linha do tempo do preço
GX = (190, 500, 790)
GBASE = 930
def gy(v):
    return GBASE - v * 0.24


def s03(c, t):  # 9.3 - 24.2  outubro 1.000 -> novembro 2.000 -> BF 50% = 1.000
    floor(c)
    title(c, t, 9.4, "O preço da mesma TV", y=250, size=66)
    line(c, 80, GBASE, 930, GBASE, 5, LGRAY)
    labs = (("OUTUBRO", 9.6), ("INÍCIO NOV", 12.2), ("BLACK FRIDAY", 16.2))
    for (lab, t0), x in zip(labs, GX):
        show(c, t, t0, x, GBASE + 45, lambda c, s=lab: text(c, s, 0, 0, 38, MARKER, NAVY), anim="up")
    pts = [(GX[0], gy(1000)), (GX[1], gy(2000)), (GX[2], gy(1000))]
    # pontos e linha
    if t > 10.6:
        circle(c, *pts[0], 16 * ease_out(prog(t, 10.6, 0.3)), GREEN, 5)
        show(c, t, 10.9, pts[0][0], pts[0][1] + 70, M("R$ 1.000", 58, INK), anim="pop")
    if t > 13.5:
        k = ease_out(prog(t, 13.5, 0.8))
        line(c, pts[0][0], pts[0][1], pts[0][0] + (pts[1][0] - pts[0][0]) * k, pts[0][1] + (pts[1][1] - pts[0][1]) * k, 8, RED)
        if k >= 1:
            circle(c, *pts[1], 16, RED, 5)
        show(c, t, 14.5, pts[1][0], pts[1][1] - 70, M(D2000, 58, RED), anim="pop")
        show(c, t, 13.7, 290, 520, lambda c: text(c, "sobe!", 0, 0, 52, MARKER, RED), anim="pop")
    if t > 16.2:
        k = ease_out(prog(t, 16.2, 0.8))
        line(c, pts[1][0], pts[1][1], pts[1][0] + (pts[2][0] - pts[1][0]) * k, pts[1][1] + (pts[2][1] - pts[1][1]) * k, 8, GREEN)
        if k >= 1:
            circle(c, *pts[2], 16, GREEN, 5)
        show(c, t, 17.3, pts[2][0], pts[1][1] - 40, off_burst("50% OFF", RED, 40), s=0.62, anim="stamp")
        show(c, t, 19.5, pts[2][0], pts[2][1] + 70, M("R$ 1.000", 58, INK), anim="pop")
    # mesmo preço: tracejado ligando outubro e Black Friday
    if t > 20.6:
        k = ease_out(prog(t, 20.6, 0.5))
        c.save(); c.set_dash([18, 12])
        line(c, pts[0][0] + 30, pts[0][1] + 135, pts[0][0] + 30 + (pts[2][0] - pts[0][0] - 60) * k, pts[0][1] + 135, 6, NAVY)
        c.restore()
        show(c, t, 20.9, CX, pts[0][1] + 180, lambda c: text(c, "mesmo preço", 0, 0, 50, HAND, NAVY), anim="up")
    show(c, t, 22.3, CX, 460, stamp_txt("DESCONTO FALSO", RED, 76), anim="stamp")
    hero(c, t, CX, FY, 0.5, [(0, "relax"), (13.6, "head"), (16.3, "think"), (22.3, "point_lu")],
         [(0, "neutral"), (13.6, "shocked"), (16.3, "think"), (22.3, "angry")], look=0)


def s04(c, t):  # 24.2 - 33.9  passo 1: histórico de preço
    floor(c)
    show(c, t, 24.3, CX, 250, M("Como descobrir", 82, NAVY), anim="up")
    show(c, t, 25.5, CX, 340, lambda c: text(c, "em 3 passos", 0, 0, 54, HAND, DGRAY), anim="up")
    show(c, t, 26.9, 140, 470, badge(1), anim="pop")
    show(c, t, 27.5, 220, 470, lambda c: text(c, "olhe o histórico", 0, 0, 60, MARKER, INK, align="l"), anim="left")
    show(c, t, 29.4, CX, 560, lambda c: text(c, "sites e extensões de navegador", 0, 0, 48, HAND, DGRAY), anim="up")
    show(c, t, 31.5, CX, 820, lambda c: mini_chart(c, t, 31.7), anim="pop")
    show(c, t, 32.9, CX + 150, 700, lambda c: text(c, "pico!", 0, 0, 46, MARKER, RED), anim="pop")
    hero(c, t, 830, FY, 0.48, [(0, "relax"), (26.9, "present_l")], [(0, "neutral"), (26.9, "confident")], look=-1)


def s05(c, t):  # 33.9 - 38.1  passo 2: print do preço agora
    floor(c)
    show(c, t, 34.0, 140, 300, badge(2), anim="pop")
    show(c, t, 34.6, 220, 300, lambda c: text(c, "tire print AGORA", 0, 0, 60, MARKER, INK, align="l"), anim="left")
    show(c, t, 34.8, CX - 60, 720, lambda c: phone_print(c, t, 35.2), anim="pop")
    show(c, t, 36.6, CX + 260, 650, lambda c: hl(c, "antes da", 0, 0, 44, LYELLOW), anim="up")
    show(c, t, 36.9, CX + 260, 730, lambda c: hl(c, "Black Friday", 0, 0, 44, LYELLOW), anim="up")
    hero(c, t, 800, FY, 0.48, [(0, "point_l")], [(0, "happy")], look=-1)
    flash(c, t, 35.2)


def s06(c, t):  # 38.1 - 41.6  passo 3: comparar em outras lojas
    floor(c)
    show(c, t, 38.2, 140, 300, badge(3), anim="pop")
    show(c, t, 38.8, 220, 300, lambda c: text(c, "compare as lojas", 0, 0, 60, MARKER, INK, align="l"), anim="left")
    show(c, t, 39.6, 200, 560, storefront("LOJA A", "R$ 1.000", LBLUE, s=0.85), anim="pop")
    show(c, t, 39.9, 500, 560, storefront("LOJA B", "R$ 980", LGREEN, s=0.85), anim="pop")
    show(c, t, 40.2, 800, 560, storefront("LOJA C", "R$ 1.050", PINKISH, s=0.85), anim="pop")
    show(c, t, 40.8, 500, 860, lambda c: text(c, "mesmo produto", 0, 0, 52, HAND, DGRAY), anim="up")
    hero(c, t, CX, FY, 0.45, [(0, "think")], [(0, "think")], look=0)


def s07(c, t):  # 41.6 - 46.9  pegadinha 1: "de/por" com o "de" inventado
    floor(c)
    show(c, t, 41.7, CX, 260, lambda c: hl(c, "+2 PEGADINHAS", 0, 0, 86, PINKISH), anim="stamp")
    def etiqueta(c):
        rrect(c, -300, -170, 600, 340, 24); fs(c, WHITE, 7)
        text(c, "de", -230, -80, 50, HAND, DGRAY, align="l")
        text(c, D2000, -150, -80, 64, MARKER, DGRAY, align="l")
        text(c, "por", -230, 70, 56, HAND, INK, align="l")
        text(c, "R$ 1.000", -140, 70, 92, MARKER, GREEN, align="l")
    show(c, t, 43.5, CX, 600, etiqueta, anim="pop")
    show(c, t, 44.9, CX - 10, 520, strike(330, RED, 9), anim="fade")
    show(c, t, 45.3, CX + 80, 840, stamp_txt('"DE" INVENTADO', RED, 58, rot=-0.12), anim="stamp")
    hero(c, t, 800, FY, 0.48, [(0, "relax"), (45.2, "point_lu")], [(0, "neutral"), (45.2, "angry")], look=-1)


def s08(c, t):  # 46.9 - 49.7  pegadinha 2: frete come o desconto
    floor(c)
    show(c, t, 47.0, CX, 280, M("e o FRETE...", 84, NAVY), anim="up")
    show(c, t, 47.3, 230, 560, group(parcel, at(0, 120, T("frete", 48))), anim="drop")
    show(c, t, 47.6, 660, 470, lambda c: text(c, "desconto  -R$ 100", 0, 0, 52, MARKER, GREEN), anim="left")
    show(c, t, 48.0, 660, 560, lambda c: text(c, "frete  +R$ 120", 0, 0, 52, MARKER, RED), anim="left")
    show(c, t, 48.5, 640, 720, lambda c: hl(c, "comeu o desconto", 0, 0, 56, PINKISH), anim="stamp")
    hero(c, t, CX, FY, 0.5, [(0, "shrug")], [(0, "worried")], look=0)


def s09(c, t):  # 49.7 - 58.8  direitos: propaganda enganosa, Procon, consumidor.gov.br
    floor(c)
    show(c, t, 49.8, CX, 260, lambda c: text(c, "desconto falso =", 0, 0, 62, HAND, INK), anim="up")
    show(c, t, 51.4, CX, 380, stamp_txt("PROPAGANDA ENGANOSA", RED, 64, rot=-0.04), anim="stamp")
    show(c, t, 52.8, 220, 600, sc(gavel, s=0.9), anim="drop")
    show(c, t, 52.9, 610, 570, lambda c: text(c, "Código de Defesa", 0, 0, 50, MARKER, NAVY), anim="left")
    show(c, t, 53.4, 610, 640, lambda c: text(c, "do Consumidor (art. 37)", 0, 0, 44, HAND, DGRAY), anim="left")
    show(c, t, 55.2, CX, 790, lambda c: text(c, "reclame no", 0, 0, 50, HAND, INK), anim="up")
    show(c, t, 55.7, 280, 900, lambda c: ribbon(c, "PROCON", NAVY, 54), anim="stamp")
    show(c, t, 56.6, 690, 900, lambda c: ribbon(c, "consumidor.gov.br", GREEN, 42), anim="stamp")
    hero(c, t, CX, FY, 0.5, [(0, "relax"), (51.4, "finger_up"), (55.2, "present")],
         [(0, "neutral"), (51.4, "confident"), (55.2, "happy")], look=0)


def s10(c, t):  # 58.8 - 63.2  arrependimento: 7 dias na compra pela internet
    floor(c)
    show(c, t, 59.0, CX, 270, lambda c: text(c, "comprou pela internet?", 0, 0, 62, MARKER, NAVY), anim="up")
    show(c, t, 59.7, 260, 600, group(sc(phone, NAVY, s=1.3), at(0, 0, sc(cart, s=0.35))), anim="pop")
    show(c, t, 61.1, 620, 580, sc(calendar, "7", GREEN, 120, s=1.9), anim="stamp")
    show(c, t, 61.9, 620, 820, lambda c: hl(c, "dias pra desistir", 0, 0, 56, LGREEN), anim="up")
    show(c, t, 62.3, 620, 900, lambda c: text(c, "(CDC, art. 49)", 0, 0, 40, HAND, DGRAY), anim="up")
    hero(c, t, 830, FY, 0.48, [(0, "thumb")], [(0, "grin")], look=-1)


def s11(c, t):  # 63.2 - fim  salva, manda, segue
    floor(c)
    show(c, t, 63.4, 230, 360, sc(calendar, "27", RED, 84, s=1.1), anim="pop")
    show(c, t, 63.5, 380, 320, lambda c: text(c, "SALVA", 0, 0, 72, MARKER, NAVY, align="l"), anim="left")
    show(c, t, 64.2, 380, 400, lambda c: text(c, "pra usar dia 27", 0, 0, 48, HAND, INK, align="l"), anim="left")
    show(c, t, 65.2, 230, 560, sc(envelope), s=0.9, anim="pop")
    show(c, t, 65.3, 380, 540, lambda c: text(c, "MANDA", 0, 0, 72, MARKER, NAVY, align="l"), anim="left")
    show(c, t, 65.6, 380, 615, lambda c: text(c, "pra quem vai às compras", 0, 0, 44, HAND, INK, align="l"), anim="left")
    # segue: O Consultor apontando pra cima + seta + faixa
    if t > 66.9:
        k = ease_out(prog(t, 66.9, 0.4))
        arrow(c, 640, 1080, 640, 1080 - 190 * k, NAVY, 12, bend=0.0, head=40)
    show(c, t, 66.9, CX, 760, lambda c: hl(c, "SEGUE PRA MAIS", 0, 0, 92, LYELLOW), anim="stamp")
    show(c, t, 67.7, CX, 845, lambda c: text(c, "até a Black Friday tem mais", 0, 0, 44, HAND, DGRAY), anim="up")
    hero(c, t, 420, FY, 0.62, [(0, "present"), (66.9, "finger_up")], [(0, "happy"), (66.9, "grin")], look=0.3)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 7.0, s01), (7.0, 9.3, s02), (9.3, 24.2, s03), (24.2, 33.9, s04), (33.9, 38.1, s05),
    (38.1, 41.6, s06), (41.6, 46.9, s07), (46.9, 49.7, s08), (49.7, 58.8, s09), (58.8, 63.2, s10),
    (63.2, 999.0, s11),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
