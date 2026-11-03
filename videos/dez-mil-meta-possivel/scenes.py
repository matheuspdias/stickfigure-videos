"""Disseram que R$ 100 mil é impossível. E R$ 10 mil? Só TikTok: vertical nativo 1080x1920, ~69 s.
Resposta aos comentários do vídeo "primeiros-100-mil". Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco.
Layout como o de reserva-emergencia: coordenadas com pés em y=1230 e deslocadas +60 (SHIFT).
Contas (0,8% a.m. líquido, aporte no começo do mês, como no vídeo dos 100 mil) em roteiro.txt."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)

SFX = [(3.6, "tum"), (31.9, "soft_ding"), (53.5, "tum"), (68.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def R(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="r")


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def comment_card(lines, w=880, size=52, likes=None):
    """comentário genérico de rede social: avatar cinza sem foto, barra cinza no lugar do nome, texto e coração"""
    def f(c):
        h = 120 + len(lines) * size * 1.15
        rrect(c, -w / 2, -h / 2, w, h, 26); fs(c, WHITE, 6)
        ax, ay = -w / 2 + 70, -h / 2 + 70
        circle(c, ax, ay, 42, LGRAY, 4)
        circle(c, ax, ay - 10, 15, DGRAY, 0)
        c.save(); c.arc(ax, ay + 30, 26, 3.4, 6.0); rgb(c, DGRAY); c.fill(); c.restore()
        rrect(c, ax + 65, ay - 22, 200, 22, 11); rgb(c, LGRAY); c.fill()
        rrect(c, ax + 285, ay - 22, 90, 22, 11); rgb(c, (0.9, 0.9, 0.9)); c.fill()
        for i, s in enumerate(lines):
            text(c, s, ax + 65, ay + 40 + i * size * 1.15, size, HAND, INK, align="l")
        hx, hy = w / 2 - 60, -h / 2 + 62
        c.save(); c.translate(hx, hy); c.scale(1.3, 1.3)
        c.move_to(0, 12); c.curve_to(-26, -6, -14, -26, 0, -12); c.curve_to(14, -26, 26, -6, 0, 12)
        rgb(c, RED); c.fill(); c.restore()
        if likes:
            text(c, likes, hx, hy + 45, 34, HAND, DGRAY)
    return f


def time_row(t, t0, money, when, months, col=GREEN, maxm=100, maxw=820, d=0.6):
    """linha da escada: 'R$ 100/mês' à esquerda, tempo à direita e uma barra proporcional ao número de meses"""
    def f(c):
        text(c, money, 0, 0, 60, MARKER, NAVY, align="l")
        if t > t0 + 0.35:
            text(c, when, maxw, 0, 58, MARKER, col, align="r")
        k = ease_out(prog(t, t0, d))
        rrect(c, 0, 40, max(maxw * months / maxm * k, 4), 46, 12); fs(c, col, 5)
    return f


def button(s, col, size=64):
    def f(c):
        w = text_w(c, s, size) + 70
        rrect(c, -w / 2, -size * 0.8, w, size * 1.6, 26); fs(c, col, 7)
        text(c, s, 0, 0, size, MARKER, WHITE)
    return f


def drawer(c):
    """gaveta aberta com notas paradas"""
    rrect(c, -150, -40, 300, 120, 10); fs(c, (0.72, 0.52, 0.32), 6)
    rrect(c, -40, 0, 80, 20, 8); fs(c, DGRAY, 4)
    rrect(c, -170, -150, 340, 110, 10); fs(c, (0.82, 0.62, 0.4), 6)
    c.save(); c.translate(0, -175); c.scale(0.7, 0.7); bills(c, 3); c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 4.9  gancho: o comentário + "você tem razão" + R$ 10 mil
    floor(c)
    show(c, t, 0.0, CX, 330, comment_card(["guardar 100 mil é impossível", "pra quem ganha pouco"]),
         anim="pop", d=0.3)
    show(c, t, 0.5, CX, 560, lambda c: hl(c, "Você tem razão.", 0, 0, 74, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 2.4, CX, 700, T("meta possível:", 64, DGRAY), anim="up")
    show(c, t, 3.6, CX, 860, lambda c: hl(c, "R$ 10 MIL", 0, 0, 150, LGREEN), anim="stamp", d=0.35)
    hero(c, t, 830, FY, 0.62, [(0, "relax"), (0.5, "thumb"), (3.6, "present_l")],
         [(0, "neutral"), (0.5, "happy"), (3.6, "grin")], appear=0.0, look=-0.6)


def s02(c, t):  # 4.9 - 13.4  muita gente comentou: mil por mês não cabe
    floor(c)
    show(c, t, 5.0, CX, 380, lambda c: video_card(c, "OS PRIMEIROS R$ 100 MIL", None, w=740, h=330,
                                                    icon=sc(snowball, 70)), anim="pop")
    for i, (s, x, y, t0) in enumerate((("impossível!", 260, 650, 6.5), ("não sobra nada...", 620, 740, 6.9),
                                       ("com que salário?", 330, 850, 7.3))):
        show(c, t, t0, x, y, group(lambda c: speech(c, 400, 100, -100, 80), T(s, 46)), anim="pop", d=0.3)
    show(c, t, 10.6, CX, 1000, group(M("R$ 1.000/mês", 76, NAVY), at(0, 4, strike(470))), anim="stamp")
    show(c, t, 12.1, CX, 1100, T("não cabe no salário", 56, RED), anim="up")
    hero(c, t, 880, FY, 0.55, [(0, "relax"), (8.3, "finger_up"), (12.1, "shrug")],
         [(0, "neutral"), (8.3, "confident"), (12.1, "worried")], look=-1)


def s03(c, t):  # 13.4 - 19.4  R$ 10 mil já é uma reserva de emergência de verdade
    floor(c)
    show(c, t, 13.6, CX, 270, M("R$ 10 mil é diferente", 72, NAVY), anim="up")
    show(c, t, 17.3, 330, 640, sc(shield, NAVY, s=1.5), anim="pop")
    show(c, t, 17.4, 330, 820, M("R$ 10 mil", 60, GREEN), anim="up")
    show(c, t, 17.6, 690, 560, T("reserva de", 58), anim="up")
    show(c, t, 17.9, 690, 650, T("emergência", 64, NAVY), anim="up")
    show(c, t, 18.6, 690, 760, lambda c: hl(c, "de verdade", 0, 0, 60, LGREEN), anim="stamp")
    hero(c, t, 520, FY, 0.62, [(0, "present"), (17.3, "point_lu")], [(0, "neutral"), (17.3, "confident")], look=-0.4)


def s04(c, t):  # 19.4 - 26.3  vive com 2 mil = 5 meses; imprevisto não vira dívida
    floor(c)
    show(c, t, 19.6, CX, 270, T("vive com R$ 2 mil por mês?", 64), anim="up")
    if t > 21.7:
        for i in range(5):
            show(c, t, 21.8 + i * 0.15, 150 + i * 185, 470, sc(calendar, str(i + 1), GREEN, 72, s=0.85), anim="pop")
    show(c, t, 22.8, CX, 640, lambda c: hl(c, "5 meses de contas pagas", 0, 0, 62, LGREEN), anim="stamp")
    show(c, t, 24.0, 300, 870, group(sc(wrench_tire, s=0.7), at(0, 120, T("imprevisto", 48))), anim="pop")
    show(c, t, 24.9, 520, 860, lambda c: arrow(c, -70, 0, 70, 0, INK, 8, 0), anim="left", d=0.3)
    show(c, t, 25.4, 740, 860, group(sc(card, RED, s=0.9), at(0, 120, T("dívida", 48, RED))), anim="pop")
    show(c, t, 25.7, 740, 860, sc(big_x, 95), anim="stamp")
    hero(c, t, 900, FY, 0.5, [(0, "relax"), (25.7, "thumb")], [(0, "neutral"), (25.7, "grin")], look=-1)


def s05(c, t):  # 26.3 - 31.1  a conta é a mesma
    floor(c)
    show(c, t, 26.5, CX, 280, M("A conta é a mesma", 76, NAVY), anim="up")
    show(c, t, 28.0, CX, 520, lambda c: hl(c, "0,8% ao mês", 0, 0, 120, LYELLOW), anim="stamp")
    show(c, t, 29.9, CX, 700, T("já sem imposto", 66, GREEN), anim="up")
    show(c, t, 30.3, CX, 800, T("(igual ao vídeo dos 100 mil)", 46, DGRAY), anim="fade")
    hero(c, t, CX, FY, 0.62, [(0, "present"), (28.0, "finger_up")], [(0, "neutral"), (28.0, "confident")],
         prop=("l", prop_calculator), look=0)


def s06(c, t):  # 31.1 - 44.3  a escada até os R$ 10 mil
    floor(c)
    show(c, t, 31.2, CX, 260, lambda c: ribbon(c, "ATÉ OS R$ 10 MIL", NAVY, 62), anim="stamp")
    rows = ((31.9, "R$ 100/mês", "6 anos e 2 m", 74), (36.8, "R$ 200/mês", "3 anos e 6 m", 42),
            (39.1, "R$ 300/mês", "2 anos e 6 m", 30), (41.6, "R$ 500/mês", "1 ano e 7 m", 19))
    for i, (t0, money, when, m) in enumerate(rows):
        show(c, t, t0, 90, 410 + i * 160, time_row(t, t0, money, when, m, GREEN, maxm=74, maxw=820),
             anim="left", d=0.3)
    show(c, t, 43.0, 330, 1080, T("quanto mais você guarda,", 46, DGRAY), anim="fade")
    show(c, t, 43.4, 330, 1140, T("mais cedo você chega", 46, DGRAY), anim="fade")
    hero(c, t, 860, FY, 0.48, [(0, "relax"), (31.9, "point_lu"), (41.6, "arms_up")],
         [(0, "neutral"), (31.9, "happy"), (41.6, "grin")], look=-1)


def s07(c, t):  # 44.3 - 51.9  a virada: parado na gaveta
    floor(c)
    show(c, t, 44.5, CX, 260, lambda c: hl(c, "A VIRADA", 0, 0, 96, PINKISH), anim="stamp")
    show(c, t, 46.4, 250, 620, sc(drawer, s=1.0), anim="pop")
    show(c, t, 47.8, 250, 760, T("parado na gaveta", 50, DGRAY), anim="up")
    show(c, t, 46.7, 680, 470, M("R$ 100/mês", 58, NAVY), anim="up")
    show(c, t, 49.9, 680, 620, M("8 anos", 100, RED), anim="stamp")
    show(c, t, 50.9, 680, 730, M("e 4 meses", 64, RED), anim="up")
    show(c, t, 51.0, 680, 830, T("(sem render nada)", 44, DGRAY), anim="fade")
    hero(c, t, 860, FY, 0.5, [(0, "think"), (49.9, "head")], [(0, "think"), (49.9, "shocked")], look=-1)


def s08(c, t):  # 51.9 - 59.5  investindo, chega 2 anos antes; 2.700 vieram dos juros
    floor(c)
    show(c, t, 52.0, 90, 330, time_row(t, 52.0, "parado", "8 anos e 4 m", 100, RED, maxm=100, maxw=820),
         anim="fade", d=0.1)
    show(c, t, 52.3, 90, 490, time_row(t, 52.4, "investindo", "6 anos e 2 m", 74, GREEN, maxm=100, maxw=820),
         anim="fade", d=0.1)
    show(c, t, 53.6, 760, 640, lambda c: hl(c, "~2 anos antes", 0, 0, 64, LYELLOW), anim="stamp")
    # de onde vieram os 10 mil
    if t > 55.0:
        base_y, x = 1040, 330
        k = ease_out(prog(t, 55.0, 0.5))
        hb = 300 * k                       # 7.400 do bolso
        rrect(c, x - 90, base_y - hb, 180, hb, 8); fs(c, NAVY, 6)
        if t > 55.0:
            k2 = ease_out(prog(t, 55.9, 0.5))
            hj = 110 * k2                  # ~2.700 de juros
            rrect(c, x - 90, base_y - 300 - hj, 180, hj, 8); fs(c, GREEN, 6)
    show(c, t, 55.3, 600, 960, L("R$ 7.400 do seu bolso", 46, NAVY, HAND), anim="left", d=0.3)
    show(c, t, 56.0, 600, 800, L("R$ 2.700 de juros", 52, GREEN, MARKER), anim="left", d=0.3)
    show(c, t, 55.0, 330, 1100, T("R$ 10 mil", 50), anim="fade")
    hero(c, t, 880, FY, 0.42, [(0, "relax"), (53.6, "arms_up")], [(0, "neutral"), (53.6, "grin")], look=-1)


def s09(c, t):  # 59.5 - 62.7  começar pequeno faz a bola de neve existir
    floor(c)
    show(c, t, 59.7, CX, 280, M("Começar pequeno", 86, NAVY), anim="up")
    r = 40 + 110 * ease_io(prog(t, 60.6, 1.8))
    if t > 60.0:
        x = 200 + 420 * ease_io(prog(t, 60.6, 1.8))
        c.save(); c.translate(x, 900 - r); c.rotate(t * 2.2); snowball(c, r); c.restore()
    show(c, t, 61.3, CX, 450, T("é o que faz a bola de neve existir", 54), anim="up")
    hero(c, t, 880, FY, 0.5, [(0, "present_l"), (61.4, "thumb")], [(0, "happy"), (61.4, "grin")], look=-1)


def s10(c, t):  # 62.7 - fim  pergunta + segue
    floor(c)
    show(c, t, 62.9, CX, 260, M("Quanto você guarda", 80, NAVY), anim="up")
    show(c, t, 63.6, CX, 360, M("por mês?", 80, NAVY), anim="up")
    show(c, t, 65.0, 600, 540, group(lambda c: speech(c, 640, 150, -200, 120), T("Comenta: R$ ___ por mês", 50)),
         anim="pop", d=0.3)
    show(c, t, 66.1, 600, 700, T("eu te digo a data dos seus 10 mil", 46, DGRAY), anim="up")
    show(c, t, 67.9, 450, 850, button("SEGUE PRA PRÓXIMA META", NAVY, 52), anim="stamp")
    hero(c, t, 760, FY, 0.65, [(0, "think"), (64.9, "point_l"), (67.9, "point_ru")],
         [(0, "think"), (64.9, "happy"), (67.9, "grin")], look=0.3)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 4.9, s01), (4.9, 13.4, s02), (13.4, 19.4, s03), (19.4, 26.3, s04), (26.3, 31.1, s05),
    (31.1, 44.3, s06), (44.3, 51.9, s07), (51.9, 59.5, s08), (59.5, 62.7, s09), (62.7, 999.0, s10),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
