"""Vai tirar férias? Cuidado com o mês seguinte. Só TikTok: vertical 1080x1920, 77,1 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout vertical: título y~250, palco y 360-1290 (pés em 1280), legendas em y~1400-1460, abaixo de 1500 a interface
do TikTok, nada importante em x > 930. Números conferidos em contas.py (05/11/2026)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(2.0, "tum"), (30.9, "tum"), (47.3, "tum"), (75.8, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s.replace("2.", "2 .")


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


def cal(num, mes, col=RED, s=1.0, size=72):
    def f(c):
        c.save(); c.scale(s, s); calendar(c, num, col, size); c.restore()
        text(c, mes, 0, -50 * s, 30 * s, MARKER, WHITE)
    return f


def minus_row(label, col=RED, size=58):
    def f(c):
        line(c, -20, 0, 20, 0, 9, col)
        text(c, label, 40, 0, size, HAND, col, align="l")
    return f


def plus_row(label, col=GREEN, size=56, tcol=INK):
    def f(c):
        line(c, -18, 0, 18, 0, 8, col); line(c, 0, -18, 0, 18, 8, col)
        text(c, label, 40, 0, size, HAND, tcol, align="l")
    return f


def phone_money(val, col=GREEN):
    """celular com o saldo na tela"""
    def f(c):
        c.save(); c.scale(1.7, 1.7); phone(c); c.restore()
        text(c, "+", 0, -60, 60, MARKER, col)
        text(c, m(val), 0, 20, 40, MARKER, col)
    return f


def bar_v(c, t, t0, x, base, v, scale, col, lab, val, sub):
    if t <= t0:
        return
    k = ease_out(prog(t, t0, 0.6))
    h = v * scale * k
    rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
    show(c, t, t0 + 0.7, x, base - v * scale - 50, MM(val, 58, INK), anim="pop")
    show(c, t, t0 + 0.3, x, base + 50, T(lab, 44, DGRAY), anim="up")
    if sub:
        show(c, t, t0 + 0.5, x, base + 100, T(sub, 36, GRAY), anim="up")


# ======================================================================= CENAS
def s01(c, t):  # 0 - 7.0  gancho
    floor(c)
    show(c, t, 0.0, CX, 260, lambda c: text(c, "FÉRIAS", 0, 0, 150, MARKER, NAVY), anim="stamp", d=0.3)
    show(c, t, 0.0, 250, 560, sc(suitcase, ORANGE, s=1.1), anim="pop")
    show(c, t, 1.6, 760, 560, phone_money("R$ 3.631", GREEN), anim="pop")
    show(c, t, 2.0, 760, 800, lambda c: hl(c, "DINHEIRÃO", 0, 0, 64, LGREEN), anim="stamp", d=0.3)
    show(c, t, 3.6, CX, 930, lambda c: hl(c, "E NO MÊS SEGUINTE...", 0, 0, 62, PINKISH, RED), anim="stamp")
    show(c, t, 5.0, 820, 1080, MM("R$ ?", 96, RED), anim="drop")
    show(c, t, 6.2, 220, 1080, sc(qmark, 80, NAVY), anim="pop")
    hero(c, t, CX, FY, 0.6, [(0, "arms_up"), (3.6, "head"), (6.2, "finger_up")],
         [(0, "grin"), (3.6, "shocked"), (6.2, "confident")], look=0.3)


def s02(c, t):  # 7.0 - 16.5  como funciona
    floor(c)
    show(c, t, 7.1, CX, 250, lambda c: ribbon(c, "COMO FUNCIONA", NAVY, 64), anim="stamp")
    show(c, t, 8.5, 250, 470, cal("2", "DIAS", RED, 1.4), anim="pop")
    show(c, t, 9.4, 250, 640, T("antes de sair", 52), anim="up")
    show(c, t, 10.9, 520, 430, plus_row("salário dos 30 dias", NAVY, 50), anim="left", d=0.3)
    show(c, t, 12.5, 520, 530, plus_row("1/3 a mais", GREEN, 58, GREEN), anim="left", d=0.3)
    show(c, t, 14.3, 520, 650, minus_row("INSS", RED, 58), anim="left", d=0.3)
    show(c, t, 15.5, 520, 750, minus_row("Imposto de Renda", RED, 50), anim="left", d=0.3)
    show(c, t, 15.9, CX, 920, T("CLT, art. 145", 40, GRAY), anim="fade")
    hero(c, t, CX, FY, 0.65, [(0, "present"), (10.9, "point_ru"), (14.3, "head")],
         [(0, "neutral"), (10.9, "happy"), (14.3, "worried")], look=0.3)


ROWS = [  # (t0, salário, líquido, nota)
    (18.6, "Mínimo R$ 1.621", "R$ 1.991", None),
    (21.8, "R$ 2.000", "R$ 2.451", None),
    (25.0, "R$ 3.000", "R$ 3.631", None),
    (28.2, "R$ 5.000", "R$ 5.300", "tem IR: com o terço vai a 6.667"),
]


def s03(c, t):  # 16.5 - 34.7  tabela
    title(c, t, 16.6, "Férias de 30 dias: líquido", y=250, size=62)
    show(c, t, 17.6, CX, 335, T("salário + 1/3 - INSS - IR", 44, DGRAY), anim="up")
    y0, rh = 470, 170
    for i, (t0, sal, liq, nota) in enumerate(ROWS):
        if t < t0:
            continue
        y = y0 + i * rh
        cur = (i == len(ROWS) - 1 or t < ROWS[i + 1][0])
        k = ease_out(prog(t, t0, 0.35))
        if cur:
            rrect(c, 50, y - 70, 860 * k, 140, 16); rgb(c, LYELLOW); c.fill()
        show(c, t, t0, 80, y, L(sal, 54, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, t0 + 1.2, 890, y, R(liq, 76 if cur else 62, GREEN, MARKER), anim="stamp", d=0.3)
    if t > 30.8:
        y = y0 + 3 * rh + 105
        show(c, t, 30.8, 890, y, R("tem Imposto de Renda", 46, RED), anim="pop")
        show(c, t, 32.9, 890, y + 60, R("com o terço, o bruto vai a R$ 6.667", 38, DGRAY), anim="up")
    show(c, t, 19.4, CX, 385, T("30 dias de férias, sem dependentes", 34, GRAY), anim="fade")
    hero(c, t, 960, FY, 0.42, [(0, "present_l"), (30.8, "head")], [(0, "neutral"), (30.8, "shocked")], look=-1)


def s04(c, t):  # 34.7 - 40.6  a virada
    floor(c)
    show(c, t, 34.8, CX, 250, lambda c: ribbon(c, "MAS TEM UM DETALHE", RED, 60), anim="stamp")
    show(c, t, 36.1, CX, 440, T("esse dinheiro é o", 60), anim="up")
    show(c, t, 37.0, CX, 560, M("SALÁRIO DO MÊS", 84, NAVY), anim="stamp")
    show(c, t, 38.1, CX, 670, T("em que você está de férias,", 54), anim="up")
    show(c, t, 39.7, CX, 820, lambda c: hl(c, "ADIANTADO", 0, 0, 100, PINKISH, RED), anim="stamp")
    hero(c, t, CX, FY, 0.62, [(0, "finger_up"), (39.7, "point_ru")], [(0, "think"), (39.7, "shocked")], look=0.2)


def s05(c, t):  # 40.6 - 54.2  exemplo R$ 3 mil
    floor(c)
    show(c, t, 40.7, CX, 250, lambda c: ribbon(c, "EXEMPLO: R$ 3 MIL", NAVY, 60), anim="stamp")
    show(c, t, 41.9, 190, 430, cal("16", "VOLTA", GREEN, 1.1), anim="pop", t1=51.2)
    show(c, t, 43.5, 300, 400, L("próximo pagamento:", 48, DGRAY), anim="left", t1=51.2)
    show(c, t, 45.1, 300, 470, L("só 15 dias trabalhados", 52, INK, MARKER), anim="left", t1=51.2)
    base = 1020
    sc_ = 380 / 2751.4
    if t < 51.2:
        bar_v(c, t, 49.0, 680, base, 2751.40, sc_, LGRAY, "salário normal", "R$ 2.751", None)
        bar_v(c, t, 47.0, 330, base, 1375.70, sc_, RED, "próximo salário", "R$ 1.376", "aprox.")
        line(c, 150, base, 860, base, 6)
    else:
        show(c, t, 51.3, CX, 470, M("Tirou o mês inteiro?", 74, NAVY), anim="stamp")
        show(c, t, 52.6, CX, 650, MM("R$ 0,00...", 120, RED), anim="drop")
        show(c, t, 53.0, CX, 790, lambda c: hl(c, "vem quase nada", 0, 0, 70, PINKISH, RED), anim="stamp")
    hero(c, t, 930, FY, 0.5, [(0, "point_l"), (47.0, "head"), (51.3, "shrug")],
         [(0, "neutral"), (47.0, "shocked"), (51.3, "desperate")], look=-1)


def s06(c, t):  # 54.2 - 61.5  saída 1: vender 10 dias
    floor(c)
    show(c, t, 54.3, CX, 250, lambda c: ribbon(c, "SAÍDA 1", GREEN, 66), anim="stamp")
    show(c, t, 55.6, CX, 400, M("Vender 10 dias", 90, NAVY), anim="stamp")
    show(c, t, 56.2, CX, 490, T("abono pecuniário (CLT, art. 143)", 40, GRAY), anim="fade")
    show(c, t, 57.3, 250, 650, sc(bills, 2, s=0.9), anim="pop")
    show(c, t, 58.1, 420, 620, L("sem INSS", 60, GREEN, MARKER), anim="left", d=0.3)
    show(c, t, 59.4, 420, 710, L("sem imposto", 60, GREEN, MARKER), anim="left", d=0.3)
    show(c, t, 60.5, CX, 880, group(lambda c: hl(c, "e você volta antes", 0, 0, 64, LGREEN),
                                    at(365, -8, sc(check_icon, 36))), anim="stamp")
    hero(c, t, CX, FY, 0.62, [(0, "present"), (58.1, "thumb")], [(0, "neutral"), (58.1, "happy")], look=0.2)


def s07(c, t):  # 61.5 - 66.9  saída 2: 1ª parcela do 13º
    floor(c)
    show(c, t, 61.6, CX, 250, lambda c: ribbon(c, "SAÍDA 2", GREEN, 66), anim="stamp")
    show(c, t, 62.4, CX, 400, M("1ª parcela do 13º", 80, NAVY), anim="stamp")
    show(c, t, 64.4, CX, 500, T("junto com as férias", 56), anim="up")
    show(c, t, 64.8, 300, 720, group(sc(envelope, s=1.4), at(0, 140, T("+ metade do salário", 40, GREEN))), anim="pop")
    show(c, t, 65.7, 720, 700, cal("JAN", "PEÇA EM", GOLD, 1.4, 52), anim="pop")
    show(c, t, 66.1, 720, 860, T("pedido em janeiro", 44, GOLD), anim="up")
    hero(c, t, CX, FY, 0.62, [(0, "point_ru"), (65.7, "finger_up")], [(0, "happy"), (65.7, "think")], look=0.3)


def s08(c, t):  # 66.9 - 71.9  a dica
    floor(c)
    show(c, t, 67.0, CX, 250, lambda c: ribbon(c, "A DICA", GOLD, 70, INK), anim="stamp")
    show(c, t, 67.8, CX, 400, T("no dia que cair:", 60), anim="up")
    show(c, t, 68.9, CX, 530, lambda c: hl(c, "SEPARE", 0, 0, 110, LGREEN), anim="stamp")
    show(c, t, 69.6, 290, 780, sc(piggy, GOLD, s=1.1), anim="pop")
    show(c, t, 70.4, 680, 750, T("as contas do", 54), anim="up")
    show(c, t, 70.9, 680, 820, T("mês seguinte", 60, NAVY), anim="up")
    hero(c, t, CX, FY, 0.65, [(0, "finger_up"), (69.6, "point_l")], [(0, "confident")], look=-0.4)


def s09(c, t):  # 71.9 - fim  salva, manda, segue
    floor(c)
    show(c, t, 72.0, 280, 360, M("SALVA", 110, NAVY), anim="stamp", t1=75.6)
    show(c, t, 72.5, 280, 480, T("pra quando tirar as suas", 44), anim="up", t1=75.6)
    show(c, t, 73.9, 760, 420, group(sc(phone, s=1.4), at(0, 180, T("manda pra quem", 44)), at(0, 230, T("vai sair de férias", 44))),
         anim="pop", t1=75.6)
    show(c, t, 75.8, CX, 330, lambda c: hl(c, "SEGUE PRA MAIS CONTAS", 0, 0, 78, LYELLOW), anim="stamp")
    show(c, t, 76.4, CX, 460, T("Faz a Conta", 56, GOLD), anim="up")
    if t > 75.8:
        arrow_draw(c, t, 75.9, 700, 900, 700, 560, col=NAVY, lw=10)
    hero(c, t, 480, FY, 0.75, [(0, "present"), (75.8, "point_ru")], [(0, "happy"), (75.8, "grin")], look=0.5)


SCENES = [
    (0.0, 7.0, s01), (7.0, 16.5, s02), (16.5, 34.7, s03), (34.7, 40.6, s04), (40.6, 54.2, s05),
    (54.2, 61.5, s06), (61.5, 66.9, s07), (66.9, 71.9, s08), (71.9, 999.0, s09),
]
