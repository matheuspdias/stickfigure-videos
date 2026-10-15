"""Reserva de emergência contada como história. Só TikTok: vertical nativo 1080x1920, 76,4 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout vertical: título y~250, palco y 360-1230 (pés dos bonecos em y=1230), legendas em y~1400,
abaixo de y 1500 fica a interface do TikTok. Nada importante em x > 930 (botões da direita).
Premissas: seguro-desemprego 2026 teto R$ 2.518,65, 3 a 5 parcelas, 1a parcela em até 30 dias do pedido."""
from engine import *  # noqa

VERTICAL = True

CX = 520          # centro útil (um pouco à esquerda por causa dos botões do TikTok)
FY = 1230         # pés dos bonecos (no quadro final ficam em 1290: SHIFT)
SHIFT = 60
PINKISH = (1, 0.8, 0.76)

SFX = [(8.6, "tum"), (33.6, "tum"), (55.9, "soft_ding"), (67.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- personagens e helpers
def lucas(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 2)
    other(c, t, x, FY, s, poses, exprs, **kw)


def ana(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("shirt", PURPLE); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, FY, s, poses=poses, exprs=exprs, **kw)


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def R(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="r")


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def bill_row(label, val, icon, col=RED):
    """linha de conta: ícone + rótulo à esquerda, valor à direita"""
    def f(c):
        c.save(); c.translate(-330, 0); c.scale(0.45, 0.45); icon(c); c.restore()
        text(c, label, -250, 0, 54, HAND, INK, align="l")
        text(c, val, 360, 0, 60, MARKER, col, align="r")
    return f


def bolt(c):
    poly(c, [(-20, -70), (40, -70), (10, -10), (45, -10), (-30, 80), (-5, 10), (-40, 10)])
    fs(c, YELLOW, 6)


def phone(c):
    rrect(c, -48, -85, 96, 170, 16); fs(c, DGRAY, 6)
    rrect(c, -36, -66, 72, 120, 6); fs(c, LBLUE, 4)
    circle(c, 0, 70, 7, WHITE, 3)


def month(c, t, t_ok, t_red, days=30, red_from=21, cell=118):
    """calendário 6x5: dias 1..20 riscados em sequência a partir de t_ok, 21..30 ficam vermelhos a partir de t_red"""
    cols = 6
    x0 = -cols * cell / 2
    rrect(c, x0 - 18, -cell * 0.9 - 18, cols * cell + 36, cell * 5 + cell * 0.9 + 36, 18); fs(c, WHITE, 6)
    c.rectangle(x0 - 18 + 3, -cell * 0.9 - 15, cols * cell + 30, cell * 0.75); rgb(c, NAVY); c.fill()
    text(c, "MÊS SEM SALÁRIO", 0, -cell * 0.52, 46, MARKER, WHITE)
    for d in range(1, days + 1):
        i = d - 1
        cx = x0 + (i % cols + 0.5) * cell
        cy = (i // cols + 0.5) * cell
        fill = PAPER
        if d >= red_from:
            k = clamp01((t - (t_red + (d - red_from) * 0.2)) / 0.15)
            if k > 0:
                fill = tuple(PAPER[j] + (RED[j] - PAPER[j]) * k for j in range(3))
        rrect(c, cx - cell / 2 + 6, cy - cell / 2 + 6, cell - 12, cell - 12, 10); fs(c, fill, 4)
        tc = WHITE if (d >= red_from and t > t_red + (d - red_from) * 0.2 + 0.1) else INK
        text(c, str(d), cx, cy + 4, 44, HAND, tc)
        if d < red_from and t > t_ok + i * 0.06:
            line(c, cx - 34, cy - 34, cx + 34, cy + 34, 6, GREEN)


def coin_stack(n, col=GREEN, label=None):
    def f(c):
        for i in range(n):
            ellipse(c, 0, -i * 22, 62, 20); fs(c, GOLD, 5)
        if label:
            text(c, label, 0, 70, 44, HAND, col)
    return f


def parcels(c, t, t0):
    """5 envelopes de parcela: 3 sempre, 4 e 5 tracejadas (dependem do tempo de trabalho)"""
    for i in range(5):
        x = -320 + i * 160
        if t < t0 + i * 0.18:
            continue
        a = 1.0 if i < 3 else 0.35
        c.push_group()
        c.save(); c.translate(x, 0); c.scale(0.85, 0.85); envelope(c); c.restore()
        text(c, f"{i + 1}ª", x, 105, 46, MARKER, INK)
        c.pop_group_to_source(); c.paint_with_alpha(a)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 4.9  gancho
    floor(c)
    show(c, t, 0.0, CX, 300, lambda c: hl(c, "DEMITIDO HOJE?", 0, 0, 92, PINKISH), anim="stamp", d=0.35)
    show(c, t, 2.2, CX - 170, 640, sc(house, False, s=1.15), anim="pop")
    show(c, t, 3.8, CX + 210, 620, sc(calendar, "?", RED, 96, s=1.35), anim="pop")
    show(c, t, 2.4, CX - 170, 830, T("aluguel", 56), anim="up")
    show(c, t, 2.4, CX + 210, 830, T("quantos dias?", 56, RED), anim="up")
    hero(c, t, CX, FY, 0.85, [(0, "think"), (3.8, "shrug")], [(0, "think"), (3.8, "worried")], appear=0.0, look=0)


def s02(c, t):  # 4.9 - 9.6  Lucas, sexta 17h, demitido
    floor(c)
    show(c, t, 5.1, CX, 260, M("Esse é o Lucas", 80, NAVY), anim="up")
    lucas(c, t, CX - 140, 1.05, [(0, "wave"), (8.6, "hold")], [(0, "happy"), (8.6, "shocked")], appear=5.0, look=0.3)
    show(c, t, 6.3, CX + 250, 520, group(sc(clock, 6.0, s=1.0), at(0, 150, T("sexta, 17h", 52))), anim="pop")
    show(c, t, 8.6, CX - 140, 1035, sc(moving_box, s=0.85), anim="drop")
    show(c, t, 8.65, CX + 210, 830, stamp_txt("DEMITIDO", RED, 76), anim="stamp")
    hero(c, t, 900, FY, 0.62, [(0, "relax"), (8.7, "head")], [(0, "neutral"), (8.7, "shocked")], appear=5.3, look=-1)


def s03(c, t):  # 9.6 - 20.8  as contas continuam chegando
    floor(c)
    title(c, t, 9.8, "As contas não param", y=250, size=72)
    rows = [(12.1, "aluguel", "R$ 1.200", lambda c: house(c)),
            (14.0, "mercado", "R$ 800", cart),
            (15.9, "luz", "", bolt),
            (16.4, "internet", "", lambda c: text(c, "wi-fi", 0, 0, 70, MARKER, BLUE)),
            (17.2, "celular", "", phone)]
    for i, (t0, lab, val, ic) in enumerate(rows):
        show(c, t, t0, CX, 400 + i * 100, bill_row(lab, val, ic), anim="left", d=0.3)
    # luz + internet + celular juntos
    if t > 17.5:
        show(c, t, 17.5, 790, 700, M("R$ 1.000", 56, RED), anim="pop")
        k = ease_out(prog(t, 17.5, 0.3))
        line(c, 655, 575, 655, 575 + 250 * k, 6, RED)
    show(c, t, 18.2, CX, 900, lambda c: hl(c, "TOTAL: R$ 3.000/mês", 0, 0, 66, PINKISH), anim="stamp")
    lucas(c, t, 170, 0.6, [(0, "head")], [(0, "worried"), (18.3, "desperate")], look=1)
    hero(c, t, 880, FY, 0.6, [(0, "relax"), (18.3, "shrug")], [(0, "worried")], look=-1)


def s04(c, t):  # 20.8 - 28.3  2 mil guardados = 20 dias; calendário fica vermelho
    floor(c)
    show(c, t, 21.6, 150, 290, sc(piggy, s=0.6), anim="pop")
    show(c, t, 22.0, 250, 290, L("R$ 2.000", 60, GREEN, MARKER), anim="up")
    show(c, t, 23.4, 760, 290, lambda c: hl(c, "= uns 20 dias", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, 24.4, CX, 520, lambda c: month(c, t, 24.4, 26.0, cell=100), anim="up")
    lucas(c, t, 120, 0.55, [(0, "hold"), (26.2, "head")], [(0, "worried"), (26.2, "desperate")], look=0.5)
    hero(c, t, 930, FY, 0.55, [(0, "relax"), (26.5, "think")], [(0, "neutral"), (26.5, "worried")], look=-0.5)


def s05(c, t):  # 28.3 - 38.4  "mas tem o seguro-desemprego" -> teto
    floor(c)
    show(c, t, 28.3, 560, 300, group(lambda c: speech(c, 760, 150, -300, 150),
                                     T("Mas tem o seguro-desemprego!", 56)), anim="pop", d=0.3)
    lucas(c, t, 200, 0.62, [(0, "arms_up"), (31.0, "relax")], [(0, "grin"), (32.2, "neutral")], look=1)
    show(c, t, 30.6, 600, 480, sc(check_icon, 50), anim="pop", t1=32.0)
    # teto: barras de salários diferentes batendo no mesmo limite
    base, top = 1000, 640
    if t > 32.0:
        k = ease_out(prog(t, 32.0, 0.4))
        c.save(); c.set_dash([22, 14]); line(c, 330, top, 330 + 560 * k, top, 8, RED); c.restore()
        show(c, t, 32.1, 610, top - 45, T("TETO", 52, RED), anim="up")
    for i, (sal, h, t0) in enumerate((("R$ 3 mil", 420, 36.5), ("R$ 6 mil", 640, 36.8), ("R$ 10 mil", 900, 37.1))):
        if t > t0:
            x = 420 + i * 190
            k = ease_out(prog(t, t0, 0.4))
            hh = min(h, base - top) * k
            rrect(c, x - 60, base - hh, 120, hh, 10); fs(c, GREEN, 6)
            text(c, sal, x, base + 45, 40, HAND)
    show(c, t, 33.6, 600, 510, M("máx. R$ 2.518/mês", 64, NAVY), anim="stamp")
    hero(c, t, 920, FY, 0.55, [(0, "relax"), (32.1, "point_lu")], [(0, "neutral"), (32.1, "confident")], look=-1)


def s06(c, t):  # 38.4 - 42.1  3 a 5 parcelas
    floor(c)
    title(c, t, 38.5, "De 3 a 5 parcelas", y=270, size=80)
    show(c, t, 39.0, CX, 560, lambda c: parcels(c, t, 39.0), anim="fade", d=0.1)
    show(c, t, 40.7, CX, 790, T("depende do tempo de trabalho", 54, DGRAY), anim="up")
    hero(c, t, CX, FY, 0.75, [(0, "present"), (40.6, "finger_up")], [(0, "neutral"), (40.6, "think")], look=0.3)


def s07(c, t):  # 42.1 - 46.3  primeira parcela em até 30 dias
    floor(c)
    show(c, t, 42.3, CX, 280, T("a 1ª parcela cai em...", 62), anim="up")
    show(c, t, 43.7, CX - 120, 560, sc(calendar, "30", RED, 80, s=1.8), anim="pop")
    show(c, t, 44.2, CX + 230, 560, group(sc(clock, 44.0 + t * 2, s=0.9)), anim="pop")
    show(c, t, 44.3, CX, 820, lambda c: hl(c, "até 30 dias após o pedido", 0, 0, 58, LYELLOW), anim="stamp")
    lucas(c, t, 210, 0.6, [(0, "hips"), (44.0, "head")], [(0, "worried")], look=1)
    hero(c, t, 880, FY, 0.6, [(0, "think")], [(0, "think")], look=-1)


def s08(c, t):  # 46.3 - 48.8  ajuda, mas não cobre tudo
    floor(c)
    title(c, t, 46.3, "Ajuda, mas não cobre tudo", y=260, size=70)
    base = 960
    show(c, t, 46.5, 360, base, lambda c: bar(c, 520 * ease_out(prog(t, 46.5, 0.5)), 190, RED, "contas", "R$ 3.000", 46),
         anim="fade", d=0.1)
    show(c, t, 46.9, 700, base, lambda c: bar(c, 436 * ease_out(prog(t, 46.9, 0.5)), 190, GREEN, "seguro", None, 46),
         anim="fade", d=0.1)
    if t > 47.6:
        k = ease_out(prog(t, 47.6, 0.3))
        rrect(c, 605, base - 520, 190, 84 * k, 6); rgb(c, RED, 0.35); c.fill()
        show(c, t, 47.7, 700, base - 570, T("falta dinheiro", 46, RED), anim="pop")
    show(c, t, 47.2, 700, base - 380, M("R$ 2.518", 36, WHITE), anim="fade")
    hero(c, t, CX, FY, 0.5, [(0, "shrug")], [(0, "neutral")], look=0)


def s09(c, t):  # 48.8 - 57.3  a Ana: mesma demissão, 6 meses guardados
    floor(c)
    show(c, t, 49.0, CX, 260, M("Agora, a Ana", 80, PURPLE), anim="up")
    ana(c, t, 220, 1.0, [(0, "wave"), (51.8, "relax"), (55.9, "arms_up")], [(0, "happy"), (51.8, "neutral"), (55.9, "grin")],
        appear=49.6, look=0.4)
    show(c, t, 51.6, 640, 420, stamp_txt("DEMITIDA", RED, 64), anim="stamp", t1=53.0)
    if t > 53.2:
        for i in range(6):
            show(c, t, 53.3 + i * 0.22, 480 + (i % 3) * 170, 420 + (i // 3) * 190,
                 sc(calendar, str(i + 1), GREEN, 72, s=0.85), anim="pop")
        show(c, t, 54.2, 650, 790, T("6 meses de custo de vida", 50), anim="up")
    show(c, t, 55.9, 650, 900, lambda c: hl(c, "R$ 18.000", 0, 0, 92, LGREEN), anim="stamp")
    hero(c, t, 900, FY, 0.55, [(0, "relax"), (55.9, "thumb")], [(0, "neutral"), (55.9, "grin")], look=-1)


def s10(c, t):  # 57.3 - 61.8  procura emprego com calma, sem cartão e sem empréstimo
    floor(c)
    show(c, t, 57.5, CX, 270, T("procura emprego com calma", 64), anim="up")
    show(c, t, 57.7, 300, 560, group(sc(clipboard, "VAGAS", 3, True, s=0.9)), anim="pop")
    show(c, t, 59.3, 590, 520, group(sc(card, s=1.0), at(0, 130, T("cartão", 48))), anim="pop")
    show(c, t, 59.7, 590, 500, sc(big_x, 85), anim="stamp")
    show(c, t, 60.8, 840, 520, group(sc(bank, s=0.8), at(0, 130, T("empréstimo", 48))), anim="pop")
    show(c, t, 61.1, 840, 500, sc(big_x, 85), anim="stamp")
    ana(c, t, 330, 0.75, [(0, "relax"), (59.3, "hips")], [(0, "happy"), (59.3, "confident")], look=0.5)
    hero(c, t, 790, FY, 0.55, [(0, "thumb")], [(0, "grin")], look=-1)


def s11(c, t):  # 61.8 - 65.4  a diferença não é o salário, é a reserva
    floor(c)
    show(c, t, 61.9, 260, 330, M("Lucas", 60, ORANGE), anim="up")
    show(c, t, 61.9, 780, 330, M("Ana", 60, PURPLE), anim="up")
    show(c, t, 62.2, 260, 470, group(sc(piggy, s=0.5), at(0, 90, T("R$ 2 mil", 48, RED))), anim="pop")
    show(c, t, 62.2, 780, 470, group(sc(piggy, s=0.9), at(0, 130, T("R$ 18 mil", 48, GREEN))), anim="pop")
    show(c, t, 63.2, CX, 760, group(T("salário", 56), at(0, 6, strike(230))), anim="up")
    show(c, t, 64.4, CX, 880, lambda c: hl(c, "É A RESERVA", 0, 0, 90, LYELLOW), anim="stamp")
    lucas(c, t, 160, 0.55, [(0, "head")], [(0, "worried")], look=1)
    ana(c, t, 900, 0.55, [(0, "hips")], [(0, "happy")], look=-1)
    hero(c, t, CX, FY, 0.62, [(0, "present"), (64.4, "finger_up")], [(0, "neutral"), (64.4, "confident")], look=0)


def s12(c, t):  # 65.4 - 73.1  a regra
    floor(c)
    show(c, t, 65.6, CX, 250, lambda c: ribbon(c, "A REGRA", NAVY, 64), anim="stamp")
    show(c, t, 67.5, CX, 420, M("3 a 6 meses", 110, GREEN), anim="stamp")
    show(c, t, 69.5, CX, 545, T("do seu custo de vida", 62), anim="up")
    show(c, t, 70.5, 330, 760, group(sc(shield, NAVY, s=0.75), at(0, 130, T("lugar seguro", 50))), anim="pop")
    show(c, t, 71.7, 720, 760, group(sc(clock, 71.0, s=0.75), at(0, 130, T("liquidez diária", 50))), anim="pop")
    hero(c, t, CX, FY, 0.62, [(0, "present"), (67.5, "finger_up"), (70.5, "present")],
         [(0, "neutral"), (67.5, "confident"), (70.5, "happy")], prop=("l", prop_pointer), look=0)


def s13(c, t):  # 73.1 - fim  pergunta final
    floor(c)
    show(c, t, 73.3, CX, 290, M("E você?", 100, NAVY), anim="stamp")
    show(c, t, 74.0, CX, 470, T("quantos meses aguentaria?", 66), anim="up")
    if t > 74.5:
        for i in range(6):
            show(c, t, 74.5 + i * 0.12, 220 + i * 120, 640, sc(calendar, str(i + 1), GOLD, 64, s=0.6), anim="pop")
    show(c, t, 75.6, CX + 120, 860, group(lambda c: speech(c, 520, 130, -160, 110), T("Comenta aí!", 62)), anim="pop")
    hero(c, t, 300, FY, 0.75, [(0, "point_r"), (75.6, "wave")], [(0, "happy"), (75.6, "grin")], look=1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 4.9, s01), (4.9, 9.6, s02), (9.6, 20.8, s03), (20.8, 28.3, s04), (28.3, 38.4, s05),
    (38.4, 42.1, s06), (42.1, 46.3, s07), (46.3, 48.8, s08), (48.8, 57.3, s09), (57.3, 61.8, s10),
    (61.8, 65.4, s11), (65.4, 73.1, s12), (73.1, 999.0, s13),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
