"""Quanto vai cair de verdade no seu 13º (continuação de videos/decimo-terceiro). Só TikTok: vertical 1080x1920, 87,7 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout vertical: título y~250, palco y 360-1290 (pés em 1280), legendas em y~1400-1460, abaixo de 1500 a interface
do TikTok, nada importante em x > 930. Números conferidos em contas.py (02/11/2026)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(36.7, "tum"), (40.2, "tum"), (73.1, "soft_ding"), (84.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s.replace("2.", "2 .")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="l")


def R(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="r")


def MM(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


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


def parcela(n, s=1.0, col=GREEN, val=None):
    """envelope da parcela com o número grande"""
    def f(c):
        c.save(); c.scale(s, s)
        envelope(c)
        circle(c, 0, 18, 34, col, 5)
        text(c, n, 0, 22, 40 if len(n) < 3 else 28, MARKER, WHITE)
        c.restore()
        if val:
            text(c, m(val), 0, 95 * s, 46, MARKER, col)
    return f


def cal(num, mes, col=RED, s=1.0):
    def f(c):
        c.save(); c.scale(s, s); calendar(c, num, col, 72); c.restore()
        text(c, mes, 0, -50 * s, 30 * s, MARKER, WHITE)
    return f


def minus_row(label, col=RED, size=58):
    """linha '− rótulo' com sinal desenhado (a fonte tem o hífen, mas o traço fica mais claro)"""
    def f(c):
        line(c, -20, 0, 20, 0, 9, col)
        text(c, label, 40, 0, size, HAND, col, align="l")
    return f


def plus_row(label, col=GREEN, size=56):
    def f(c):
        line(c, -18, 0, 18, 0, 8, col); line(c, 0, -18, 0, 18, 8, col)
        text(c, label, 40, 0, size, HAND, INK, align="l")
    return f


# ======================================================================= CENAS
def s01(c, t):  # 0 - 8.0  gancho
    floor(c)
    show(c, t, 0.0, CX, 270, lambda c: text(c, "SEU 13º", 0, 0, 150, MARKER, NAVY), anim="stamp", d=0.3)
    show(c, t, 1.3, CX, 420, lambda c: hl(c, "NÃO VEM INTEIRO", 0, 0, 74, PINKISH, RED), anim="stamp", d=0.3)
    show(c, t, 1.7, CX, 680, group(parcela("13º", 1.9, NAVY), at(0, 0, sc(big_x, 120))), anim="pop", t1=3.9)
    show(c, t, 4.2, 300, 680, parcela("1ª", 1.0, GOLD), anim="pop")
    show(c, t, 4.5, 700, 660, parcela("2ª", 1.6, GREEN), anim="pop")
    show(c, t, 5.7, 700, 850, lambda c: hl(c, "MAIOR?", 0, 0, 70, LGREEN), anim="stamp")
    show(c, t, 7.1, 300, 850, sc(qmark, 90, NAVY), anim="pop")
    hero(c, t, CX, FY, 0.62, [(0, "think"), (4.4, "point_r"), (7.1, "finger_up")],
         [(0, "think"), (4.4, "shocked"), (7.1, "confident")], look=0.4)


def s02(c, t):  # 8.0 - 13.2  1ª parcela
    floor(c)
    show(c, t, 8.1, CX, 250, lambda c: ribbon(c, "1ª PARCELA", GOLD, 70, INK), anim="stamp")
    show(c, t, 9.3, 280, 520, cal("30", "NOV", RED, 1.5), anim="pop")
    show(c, t, 9.4, 280, 690, T("até 30/11", 54), anim="up")
    show(c, t, 10.8, 700, 520, group(sc(bills, 2, s=0.9), at(0, 130, T("metade do salário", 50))), anim="pop")
    show(c, t, 12.2, CX, 870, group(lambda c: hl(c, "sem desconto", 0, 0, 72, LGREEN), at(260, -8, sc(check_icon, 36))),
         anim="stamp")
    hero(c, t, CX, FY, 0.6, [(0, "present"), (12.2, "thumb")], [(0, "neutral"), (12.2, "happy")], look=0)


def s03(c, t):  # 13.2 - 20.3  2ª parcela
    floor(c)
    show(c, t, 13.3, CX, 250, lambda c: ribbon(c, "2ª PARCELA", NAVY, 70), anim="stamp")
    show(c, t, 14.5, 280, 520, cal("18", "DEZ", RED, 1.5), anim="pop")
    show(c, t, 14.6, 280, 690, T("até 18/12", 54), anim="up")
    show(c, t, 16.2, 560, 500, minus_row("INSS", RED, 72), anim="left")
    show(c, t, 17.7, 560, 620, minus_row("Imposto de Renda", RED, 60), anim="left")
    show(c, t, 18.9, 820, 700, T("acima de R$ 5 mil", 46, DGRAY), anim="up")
    show(c, t, 17.0, CX, 880, parcela("2ª", 1.1, NAVY), anim="pop")
    hero(c, t, 190, FY, 0.6, [(0, "point_r"), (16.3, "head")], [(0, "neutral"), (16.3, "worried")], look=1)


ROWS = [  # (t0, salário, 1ª, 2ª, total, nota)
    (23.2, "Mínimo R$ 1.621", "810,50", "688,92", "R$ 1.499,42", None),
    (26.55, "R$ 2.000", "1.000,00", "844,31", "R$ 1.844,31", None),
    (29.68, "R$ 3.000", "1.500,00", "1.251,40", "R$ 2.751,40", None),
    (33.1, "R$ 5.000", "2.500,00", "1.998,49", "R$ 4.498,49", "sem IR"),
    (36.62, "R$ 8.000", "4.000,00", "2.040,64", "R$ 6.040,64", "IR R$ 1.037"),
]


def s04(c, t):  # 20.3 - 39.2  tabela, uma linha por vez
    title(c, t, 20.5, "Salário fixo: quanto cai", y=250, size=66)
    show(c, t, 21.6, CX, 335, T("1ª + 2ª parcela = total líquido", 44, DGRAY), anim="up")
    y0, rh = 440, 140
    for i, (t0, sal, p1, p2, tot, nota) in enumerate(ROWS):
        if t < t0:
            continue
        y = y0 + i * rh
        cur = (i == len(ROWS) - 1 or t < ROWS[i + 1][0])
        k = ease_out(prog(t, t0, 0.35))
        if cur:
            rrect(c, 50, y - 62, 940 * k, 128, 16); rgb(c, LYELLOW); c.fill()
        show(c, t, t0, 80, y - 18, L(sal, 52, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, t0 + 0.6, 80, y + 34, L(f"1ª {p1}  ·  2ª {p2}", 36, DGRAY), anim="up", d=0.3)
        show(c, t, t0 + 1.0, 960, y - 10, R(tot, 72 if cur else 60, GREEN, MARKER), anim="stamp", d=0.3)
        if nota:
            show(c, t, t0 + 1.6, 960, y + 40, R(nota, 36, RED if "IR R$" in nota else GREEN), anim="pop")
    show(c, t, 24.0, 380, 1115, T("12 meses trabalhados, sem dependentes", 36, GRAY), anim="fade")
    hero(c, t, 850, FY, 0.34, [(0, "present"), (33.6, "thumb"), (37.0, "head")],
         [(0, "neutral"), (33.6, "happy"), (37.0, "shocked")], look=0)


def s05(c, t):  # 39.2 - 52.2  a virada: como o 13º cheio é calculado
    floor(c)
    show(c, t, 39.3, CX, 250, lambda c: ribbon(c, "A VIRADA", RED, 72), anim="stamp")
    show(c, t, 41.0, CX, 380, T("13º cheio = salário de", 60), anim="up")
    show(c, t, 44.2, 860, 380, cal("31", "DEZ", NAVY, 0.75), anim="pop")
    show(c, t, 45.2, 120, 500, L("com a média do ano de:", 46, DGRAY), anim="up")
    items = [(46.3, "horas extras"), (47.3, "adicional noturno"), (48.5, "comissões")]
    for i, (t0, s) in enumerate(items):
        show(c, t, t0, 150, 590 + i * 85, plus_row(s), anim="left", d=0.3)
    items2 = [(49.8, "insalubridade"), (51.0, "periculosidade")]
    for i, (t0, s) in enumerate(items2):
        show(c, t, t0, 150, 880 + i * 85, plus_row(s, NAVY), anim="left", d=0.3)
    hero(c, t, 830, FY, 0.6, [(0, "arms_up"), (41.0, "present_l"), (46.3, "point_l")],
         [(0, "grin"), (41.0, "neutral"), (46.3, "confident")], look=-1)


def s06(c, t):  # 52.2 - 59.7  aumento no ano; só depois os descontos
    floor(c)
    show(c, t, 52.3, CX, 260, M("Teve aumento?", 84, NAVY), anim="stamp")
    if t > 52.6:
        for i, h in enumerate((150, 150, 150, 230)):
            k = ease_out(prog(t, 52.6 + i * 0.15, 0.3))
            x = 200 + i * 110
            col = GREEN if i == 3 else LGRAY
            rrect(c, x - 40, 640 - h * k, 80, h * k, 8); fs(c, col, 5)
        arrow_draw(c, t, 53.2, 170, 450, 430, 370, col=GREEN, lw=9)
    show(c, t, 53.7, 780, 560, group(parcela("2ª", 1.0, GREEN), at(0, 125, T("a diferença vem aqui", 42, GREEN))), anim="pop")
    show(c, t, 55.4, CX, 790, M("Só depois descontam:", 56), anim="up")
    for i, (t0, s) in enumerate(((56.6, "1ª parcela"), (57.5, "INSS"), (58.7, "IR"))):
        show(c, t, t0, 110 + i * 300, 900, minus_row(s, RED, 58), anim="left", d=0.3)
    hero(c, t, CX, FY, 0.5, [(0, "think"), (53.7, "point_r"), (56.6, "finger_up")],
         [(0, "think"), (53.7, "happy"), (56.6, "neutral")], look=0.5)


def s07(c, t):  # 59.7 - 73.9  exemplo
    floor(c)
    show(c, t, 59.8, CX, 250, lambda c: ribbon(c, "EXEMPLO", NAVY, 64), anim="stamp")
    show(c, t, 60.6, 90, 360, L("salário R$ 2.500", 50, INK, MARKER), anim="left", d=0.3)
    show(c, t, 62.7, 90, 425, L("+ insalubridade R$ 324", 44), anim="left", d=0.3)
    show(c, t, 63.8, 90, 485, L("+ hora extra: média R$ 500/mês", 44), anim="left", d=0.3)
    base = 1100
    # barras 1ª x 2ª (escala: 1.700 = 360 px)
    sc_ = 360 / 1700
    for x, t0, v, val, lab, col, sub in ((290, 66.1, 1412.10, "R$ 1.412,10", "1ª", GOLD, "metade do mês anterior"),
                                         (730, 68.9, 1624.60, "R$ 1.624,60", "2ª", GREEN, "já descontada")):
        if t > t0:
            k = ease_out(prog(t, t0, 0.6))
            h = v * sc_ * k
            rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
            text(c, lab, x, base - h / 2, 70, MARKER, WHITE)
            show(c, t, t0 + 0.9, x, base - v * sc_ - 50, MM(val, 54, INK), anim="pop")
            show(c, t, t0 + 0.4, x, base + 45, T(sub, 40, DGRAY), anim="up")
    line(c, 120, base, 880, base, 6)
    show(c, t, 71.6, 470, 1200, T("2ª = 13º cheio 3.324,20 - 1ª - INSS 287,50", 32, GRAY), anim="fade")
    show(c, t, 73.0, 730, 600, stamp_txt("MAIOR", GREEN, 72), anim="stamp")
    hero(c, t, 975, FY, 0.42, [(0, "present_l"), (73.0, "arms_up")], [(0, "neutral"), (73.0, "grin")], look=-1)


def s08(c, t):  # 73.9 - 77.1  comissão: ajuste em janeiro
    floor(c)
    show(c, t, 74.0, CX, 260, M("Ganha comissão?", 80, NAVY), anim="stamp")
    show(c, t, 75.9, 330, 560, cal("10", "JAN", GOLD, 1.6), anim="pop")
    show(c, t, 76.0, 700, 520, T("pode ter ajuste", 56), anim="up")
    show(c, t, 76.3, 700, 600, T("até 10 de janeiro", 56, GOLD), anim="up")
    hero(c, t, CX, FY, 0.6, [(0, "point_r"), (75.9, "finger_up")], [(0, "neutral"), (75.9, "think")], look=-0.3)


def s09(c, t):  # 77.1 - 80.6  o alerta
    floor(c)
    show(c, t, 77.2, CX, 260, lambda c: ribbon(c, "ALERTA", RED, 68), anim="stamp")
    show(c, t, 77.4, CX, 450, M("Planeje com o", 70), anim="up")
    show(c, t, 78.4, CX, 580, lambda c: hl(c, "VALOR LÍQUIDO", 0, 0, 92, LGREEN), anim="stamp")
    show(c, t, 79.5, CX, 780, group(T("salário cheio", 64, DGRAY), at(0, 4, strike(380))), anim="up")
    hero(c, t, CX, FY, 0.6, [(0, "finger_up")], [(0, "confident")], prop=("l", prop_calculator), look=0)


def s10(c, t):  # 80.6 - fim  salva, manda no grupo, segue pra parte 2
    floor(c)
    show(c, t, 80.8, 280, 360, M("SALVA", 110, NAVY), anim="stamp", t1=84.3)
    show(c, t, 81.4, 280, 480, T("pra conferir quando cair", 46), anim="up", t1=84.3)
    show(c, t, 82.8, 760, 420, group(sc(phone, s=1.4), at(0, 180, T("manda no grupo", 46)), at(0, 230, T("da família", 46))),
         anim="pop", t1=84.3)
    show(c, t, 84.5, CX, 330, lambda c: hl(c, "SEGUE PRA PARTE 2", 0, 0, 92, LYELLOW), anim="stamp")
    show(c, t, 85.3, CX, 470, T("o que fazer com ele antes do dia 30", 50), anim="up")
    if t > 84.5:
        arrow_draw(c, t, 84.6, 700, 900, 700, 560, col=NAVY, lw=10)
    hero(c, t, 500, FY, 0.75, [(0, "present"), (84.5, "point_ru")], [(0, "happy"), (84.5, "grin")], look=0.5)


SCENES = [
    (0.0, 8.0, s01), (8.0, 13.2, s02), (13.2, 20.3, s03), (20.3, 39.2, s04), (39.2, 52.2, s05),
    (52.2, 59.7, s06), (59.7, 73.9, s07), (73.9, 77.1, s08), (77.1, 80.6, s09), (80.6, 999.0, s10),
]
