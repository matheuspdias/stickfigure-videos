"""Amortização no Minha Casa Minha Vida. Só TikTok: vertical nativo 1080x1920, 78,3 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Responde aos comentários do vídeo "Alugar ou comprar?".
Layout como o de reserva-emergencia: coordenadas desenhadas com pés em y=1230 e deslocadas +60 (SHIFT).
Contas em contas.py: R$ 240 mil, 360 meses, SAC, 7,66% a.a., sem TR e seguros."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)

SFX = [(3.1, "tum"), (28.3, "tum"), (48.6, "soft_ding"), (66.1, "tum")]
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


def grow_bar(t, t0, h, w, col, label=None, top=None, t_top=None, size=46):
    """barra que cresce a partir de t0; o valor de cima aparece em t_top"""
    def f(c):
        k = ease_out(prog(t, t0, 0.6))
        bar(c, h * k, w, col, label, top if (top and t > (t_top or t0 + 0.6)) else None, size)
    return f


def button(s, col, size=70):
    def f(c):
        w = text_w(c, s, size) + 70
        rrect(c, -w / 2, -size * 0.8, w, size * 1.6, 26); fs(c, col, 7)
        text(c, s, 0, 0, size, MARKER, WHITE)
    return f


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.9  gancho
    floor(c)
    show(c, t, 0.0, CX, 290, lambda c: hl(c, "+ R$ 200 por mês", 0, 0, 86, LGREEN), anim="stamp", d=0.35)
    show(c, t, 0.15, 270, FY, sc(apartment, LYELLOW, None, 6, s=1.0), anim="pop")
    show(c, t, 3.1, CX, 470, lambda c: hl(c, "R$ 62 MIL", 0, 0, 120, LYELLOW), anim="stamp", d=0.35)
    show(c, t, 4.3, CX, 600, M("a menos", 80, GREEN), anim="up")
    hero(c, t, 760, FY, 0.85, [(0, "present_l"), (3.1, "arms_up")], [(0, "confident"), (3.1, "grin")], appear=0.0, look=-0.4)


def s02(c, t):  # 5.9 - 11.4  pedido dos comentários
    floor(c)
    show(c, t, 6.1, CX, 250, M("Vocês pediram...", 76, NAVY), anim="up")
    show(c, t, 7.7, CX, 520, lambda c: video_card(c, "ALUGAR OU COMPRAR?", None, w=720, h=400,
                                                    icon=sc(apartment, LYELLOW, "ALUGA-SE", 3, s=0.55)), anim="pop")
    show(c, t, 7.1, 330, 820, group(lambda c: speech(c, 470, 110, -120, 90), T("explica amortização!", 46)), anim="pop", d=0.3)
    show(c, t, 7.6, 600, 960, group(lambda c: speech(c, 470, 110, -150, 90), T("como amortizar?", 46)), anim="pop", d=0.3)
    hero(c, t, 880, FY, 0.62, [(0, "relax"), (9.8, "thumb")], [(0, "happy"), (9.8, "grin")],
         prop=("l", prop_calculator), look=-1)


def s03(c, t):  # 11.4 - 24.9  o cenário
    floor(c)
    show(c, t, 11.6, 230, 640, sc(apartment, LYELLOW, None, 5, s=0.85), anim="pop")
    show(c, t, 12.5, 230, 700, lambda c: price_tag(c, "R$ 300 mil", YELLOW, 50), anim="stamp")
    show(c, t, 13.7, 640, 380, lambda c: hl(c, "Minha Casa", 0, 0, 56, LGREEN), anim="left", d=0.3)
    show(c, t, 14.3, 640, 460, lambda c: hl(c, "Minha Vida", 0, 0, 56, LGREEN), anim="left", d=0.3)
    show(c, t, 15.2, 640, 560, M("faixa 3", 66, NAVY), anim="stamp")
    show(c, t, 16.3, 80, 820, L("entrada 20% = R$ 60 mil", 54), anim="left", d=0.3)
    show(c, t, 18.1, 80, 910, lambda c: (text(c, "financiado: ", 0, 0, 54, HAND, INK, align="l"),
                                         text(c, "R$ 240 mil", 290, 0, 64, MARKER, RED, align="l")), anim="left", d=0.3)
    show(c, t, 20.3, 80, 1000, L("30 anos, tabela SAC", 54), anim="left", d=0.3)
    show(c, t, 22.4, 80, 1090, lambda c: (text(c, "juros: ", 0, 0, 54, HAND, INK, align="l"),
                                          text(c, "7,66% ao ano", 160, 0, 64, MARKER, RED, align="l")), anim="left", d=0.3)
    show(c, t, 23.4, 80, 1160, L("(taxa com FGTS; sem FGTS é 8,16%)", 34, DGRAY), anim="fade")
    hero(c, t, 900, FY, 0.55, [(0, "present_l"), (18.1, "point_lu")], [(0, "neutral"), (18.1, "confident")],
         prop=("r", prop_pointer), look=-1)


def s04(c, t):  # 24.9 - 32.9  quanto paga no fim
    floor(c)
    title(c, t, 25.1, "No fim, você paga...", y=250, size=72)
    show(c, t, 26.0, CX, 330, T("(sem contar TR e seguro)", 40, DGRAY), anim="fade")
    base = 1060
    show(c, t, 25.3, 270, base, grow_bar(t, 25.3, 270, 200, NAVY, "emprestou", "R$ 240 mil", size=48), anim="fade", d=0.1)
    show(c, t, 28.3, 600, base, grow_bar(t, 28.3, 570, 220, RED, "paga", "R$ 507 mil", t_top=28.5, size=52), anim="fade", d=0.1)
    show(c, t, 30.7, 270, 540, lambda c: hl(c, "mais que", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, 31.2, 270, 620, lambda c: hl(c, "o DOBRO", 0, 0, 64, LYELLOW), anim="stamp")
    hero(c, t, 900, FY, 0.55, [(0, "relax"), (28.4, "head")], [(0, "neutral"), (28.4, "shocked")], look=-1)


def s05(c, t):  # 32.9 - 40.2  o que é amortizar
    floor(c)
    show(c, t, 33.0, CX, 250, lambda c: ribbon(c, "AMORTIZAR", NAVY, 72), anim="stamp")
    x0, y0, w, h = 110, 420, 640, 190
    cut = 140
    if t > 33.4:
        a = ease_out(prog(t, 33.4, 0.4))
        c.push_group()
        rrect(c, x0, y0, w - cut, h, 14); fs(c, PINKISH, 6)
        text(c, "DÍVIDA", x0 + (w - cut) / 2, y0 + h / 2, 70, MARKER, RED)
        c.pop_group_to_source(); c.paint_with_alpha(a)
        # pedaço do fim da dívida: vira "extra" e sai da dívida
        k = ease_io(prog(t, 35.6, 0.8))
        dx, dy = 40 * k, 330 * k
        col = PINKISH if t < 35.0 else LGREEN
        c.push_group()
        rrect(c, x0 + w - cut + dx, y0 + dy, cut, h, 14); fs(c, col, 6)
        if t > 35.0:
            text(c, "extra", x0 + w - cut / 2 + dx, y0 + h / 2 + dy, 44, MARKER, GREEN)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    show(c, t, 34.6, 330, 700, T("valor extra direto na dívida", 50), anim="up")
    show(c, t, 38.5, 470, 960, group(M("juros", 70, RED), lambda c: line(c, -110, 14, 110, -14, 12, RED)), anim="pop")
    show(c, t, 38.8, 470, 1060, lambda c: hl(c, "nunca mais", 0, 0, 56, LYELLOW), anim="stamp")
    hero(c, t, 900, FY, 0.55, [(0, "present_l"), (38.5, "finger_up")], [(0, "neutral"), (38.5, "confident")], look=-1)


def s06(c, t):  # 40.2 - 50.7  + R$ 200 por mês
    floor(c)
    title(c, t, 40.4, "Agora, a conta", y=250, size=78)
    show(c, t, 43.8, CX, 360, lambda c: hl(c, "+ R$ 200 por mês", 0, 0, 66, LGREEN), anim="stamp")
    x0, full = 110, 740
    # linha do tempo sem amortizar: 30 anos
    show(c, t, 41.2, x0, 480, L("sem extra", 46, DGRAY), anim="fade")
    if t > 41.2:
        k = ease_out(prog(t, 41.2, 0.7))
        rrect(c, x0, 510, full * k, 70, 12); fs(c, PINKISH, 5)
        if t > 41.8:
            text(c, "30 anos", x0 + full - 20, 545, 48, MARKER, RED, align="r")
    # com + 200: 277 meses (~23 anos)
    show(c, t, 44.0, x0, 650, L("com + R$ 200", 46, GREEN), anim="fade")
    w2 = full * 277 / 360
    if t > 44.6:
        k = ease_out(prog(t, 44.6, 0.7))
        rrect(c, x0, 680, w2 * k, 70, 12); fs(c, LGREEN, 5)
        if t > 45.3:
            text(c, "23 anos", x0 + w2 - 20, 715, 48, MARKER, GREEN, align="r")
    if t > 46.3:
        c.save(); c.set_dash([16, 12])
        rrect(c, x0 + w2 + 8, 680, full - w2 - 8, 70, 12); rgb(c, GREEN); c.set_line_width(5); c.stroke()
        c.restore()
    show(c, t, 46.4, x0 + w2 + (full - w2) / 2, 810, group(M("quase", 38, GREEN), at(0, 50, M("7 anos antes", 44, GREEN))),
         anim="pop")
    show(c, t, 48.6, 430, 1000, lambda c: hl(c, "R$ 62 mil a menos", 0, 0, 72, LYELLOW), anim="stamp")
    hero(c, t, 920, FY, 0.5, [(0, "think"), (44.0, "present_l"), (48.6, "arms_up")],
         [(0, "think"), (44.0, "happy"), (48.6, "grin")], look=-1)


def s07(c, t):  # 50.7 - 56.9  a pegadinha
    floor(c)
    show(c, t, 51.4, CX, 270, stamp_txt("PEGADINHA", RED, 86), anim="stamp")
    show(c, t, 52.4, 260, 700, sc(bank, s=1.3), anim="pop")
    show(c, t, 53.9, 640, 520, group(lambda c: speech(c, 500, 150, -210, 120), T("quer reduzir...", 50)), anim="pop", d=0.3)
    show(c, t, 55.4, 640, 760, button("PRAZO", GREEN, 66), anim="pop")
    show(c, t, 55.9, 640, 870, M("ou", 54, DGRAY), anim="fade")
    show(c, t, 56.2, 640, 980, button("PARCELA", BLUE, 66), anim="pop")
    hero(c, t, 230, FY, 0.55, [(0, "relax"), (54.0, "think")], [(0, "neutral"), (54.0, "think")], look=1)


def s08(c, t):  # 56.9 - 66.9  os mesmos 10 mil: prazo x parcela
    floor(c)
    show(c, t, 57.1, CX, 250, lambda c: hl(c, "R$ 10 mil extra", 0, 0, 72, LGREEN), anim="stamp")
    show(c, t, 59.2, CX, 340, T("logo no começo", 50, DGRAY), anim="up")
    base = 1040
    show(c, t, 60.3, 290, base, grow_bar(t, 60.3, 480, 210, GREEN, "reduz PRAZO", "R$ 22 mil", t_top=62.4, size=50),
         anim="fade", d=0.1)
    show(c, t, 63.6, 640, base, grow_bar(t, 63.6, 240, 210, BLUE, "reduz PARCELA", "R$ 11 mil", t_top=65.2, size=50),
         anim="fade", d=0.1)
    show(c, t, 61.6, 290, 440, T("economiza", 44, DGRAY), anim="fade")
    show(c, t, 66.1, 640, 600, stamp_txt("METADE", RED, 76), anim="stamp")
    hero(c, t, 920, FY, 0.5, [(0, "relax"), (62.4, "thumb"), (66.1, "shrug")], [(0, "neutral"), (62.4, "happy"), (66.1, "worried")],
         look=-1)


def s09(c, t):  # 66.9 - 74.9  quanto mais cedo, mais economiza
    floor(c)
    title(c, t, 67.0, "Quanto mais cedo,", y=250, size=72)
    show(c, t, 69.3, CX, 340, M("mais economiza", 66, GREEN), anim="stamp")
    show(c, t, 70.5, CX, 420, T("os mesmos R$ 10 mil, reduzindo prazo", 40, DGRAY), anim="fade")
    base = 1040
    show(c, t, 70.6, 290, base, grow_bar(t, 70.6, 480, 210, GREEN, "no ano 1", "R$ 22 mil", size=50), anim="fade", d=0.1)
    show(c, t, 72.3, 640, base, grow_bar(t, 72.3, 150, 210, ORANGE, "no ano 20", "R$ 7 mil", t_top=74.2, size=50),
         anim="fade", d=0.1)
    hero(c, t, 920, FY, 0.5, [(0, "finger_up"), (72.4, "point_l")], [(0, "confident"), (74.2, "worried")], look=-1)


def s10(c, t):  # 74.9 - fim  pergunta final
    floor(c)
    show(c, t, 75.1, CX, 270, M("Você escolheria...", 74, NAVY), anim="up")
    show(c, t, 76.0, 640, 450, button("PRAZO", GREEN, 70), anim="pop")
    show(c, t, 76.5, 640, 560, M("ou", 50, DGRAY), anim="fade")
    show(c, t, 76.6, 640, 670, button("PARCELA", BLUE, 70), anim="pop")
    show(c, t, 77.5, 640, 900, group(lambda c: speech(c, 440, 130, -150, 110), M("Comenta aí!", 58, NAVY)), anim="pop")
    hero(c, t, 280, FY, 0.75, [(0, "think"), (77.5, "point_r")], [(0, "think"), (77.5, "grin")], look=1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 5.9, s01), (5.9, 11.4, s02), (11.4, 24.9, s03), (24.9, 32.9, s04), (32.9, 40.2, s05),
    (40.2, 50.7, s06), (50.7, 56.9, s07), (56.9, 66.9, s08), (66.9, 74.9, s09), (74.9, 999.0, s10),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
