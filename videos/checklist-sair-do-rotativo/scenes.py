"""CHECKLIST DO CONSULTOR: "5 passos pra sair do rotativo do cartão". Só TikTok: vertical 1080x1920, ~72,5 s, ESTILO CADERNO (palito).
Refeito em 24/11/2026 a pedido do Matheus ("quero todos os vídeos no formato de palitinho"); mesma narração (Consultor BR B, 1 bloco).
Contas (contas.py): rotativo 451,7% a.a. (BC, set/2026) = ~15,3% a.m.; R$ 1.000 -> ~R$ 1.150 em 1 mês; dobra em ~5 meses;
teto da Lei 14.690/2023 (desde 03/01/2024): juros e encargos até 100% da dívida; consignado ~R$ 20 a 30 por mês em R$ 1.000.
Layout: lista de 5 passos na folha (y 280-700) escrita passo a passo; palco da conta y 760-1280 (pés em 1280); legendas ~1400-1460;
nada importante em x > 930. Quadro 0: a fatura de R$ 1.000 já contando para R$ 1.150."""
from engine import *  # noqa

VERTICAL = True

CX = 420
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(4.4, "tum"), (10.4, "tum"), (16.2, "tum"), (29.0, "tum"), (40.3, "tum"), (52.6, "tum"), (68.7, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(10.4, "guarda o cartão", 16.1), (16.2, "olha o tamanho", 28.9), (29.0, "não paga só o mínimo", 40.2),
          (40.3, "troca a dívida", 52.5), (52.6, "conhece o teto", 68.6)]
LIN0, LINH = 325, 80


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s.replace("2.", "2 .")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="l")


def MM(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


def HL(s, size=60, bg=LYELLOW, col=INK):
    return lambda c: hl(c, m(s), 0, 0, size, bg, col)


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def reais(c, t, t0, a, b, x, y, size, col, d=0.8, pre="R$ ", suf=""):
    v = a + (b - a) * ease_out(prog(t, t0, d))
    s = f"{v:,.0f}".replace(",", ".")
    text(c, m(pre + s + suf), x, y, size, MARKER, col)


def lista(c, t):
    show(c, t, -1.0, 540, 205, lambda c: ribbon(c, "SAIR DO ROTATIVO", NAVY, 54), anim="stamp", d=0.3)
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = LIN0 + i * LINH
        if t0 - 0.6 <= t < t1:
            c.save(); c.translate(0, 0)
            rrect(c, 70, y - 38, 880, 76, 14); fs(c, LYELLOW, 0)
            c.restore()
        if t >= t1:
            c.save(); c.translate(130, y); check_icon(c, 32); c.restore()
        else:
            circle(c, 130, y, 32, WHITE, 5)
            text(c, str(i + 1), 130, y + 14, 40, MARKER, NAVY)
        if t < t0:
            c.move_to(185, y + 18); c.line_to(900, y + 18); rgb(c, INK, 0.2); c.set_line_width(4); c.set_dash([14, 12]); c.stroke(); c.set_dash([])
        else:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(180, y - 50, 740 * k, 100); c.clip()
            text(c, nome, 190, y + 18, 56, MARKER, NAVY if t < t1 else DGRAY, align="l")
            c.restore()
    line(c, 60, 715, 1020, 715, 4, LGRAY)


# ======================================================================= PALCO (y 770-1280)
def palco(c, t):
    if t < 10.4:  # gancho
        show(c, t, -1.0, 170, 880, sc(card, RED, s=1.4), anim="pop")
        text(c, "sua fatura", 330, 830, 52, HAND, DGRAY, align="l")
        if t < 4.4:
            reais(c, t, 0.0, 0, 1000, 500, 930, 100, INK, d=1.4)
        else:
            reais(c, t, 4.4, 1000, 1150, 500, 930, 100, RED, d=1.0)
        show(c, t, 3.0, 400, 1010, T("em 1 mês no rotativo", 52, DGRAY), anim="up", t1=6.3)
        show(c, t, 6.5, 340, 1060, HL("5 PASSOS PRA SAIR", 62, PINKISH, RED), anim="stamp")
        show(c, t, 8.4, 400, 1160, T("salva pro dia da fatura", 56, NAVY), anim="up")
        hero(c, t, 860, FY, 0.9, [(0, "head"), (6.3, "finger_up")], [(0, "shocked"), (6.3, "confident")], look=-0.6)
    elif t < 16.2:  # 1
        show(c, t, 11.2, 200, 900, sc(card, PURPLE, s=1.5), anim="pop")
        show(c, t, 11.6, 200, 900, sc(padlock, s=1.1), anim="drop")
        show(c, t, 12.2, 370, 860, L("compra nova", 62, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 13.3, 370, 950, L("cai na mesma conta", 54, DGRAY), anim="left", d=0.3)
        show(c, t, 14.8, 420, 1080, HL("= MAIS JUROS", 80, PINKISH, RED), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (12.2, "point_l")], [(0, "confident"), (14.8, "worried")], look=-0.8)
    elif t < 29.0:  # 2
        show(c, t, 17.3, CX, 820, T("o tamanho do buraco", 58, DGRAY), anim="up")
        if t < 22.6:
            if t >= 20.1:
                reais(c, t, 20.1, 0, 450, CX, 980, 150, RED, d=0.9, pre="~", suf="%")
                show(c, t, 21.0, CX, 1080, T("ao ano", 58, DGRAY), anim="up")
        else:
            show(c, t, 22.6, CX, 900, MM("450% ao ano", 50, GRAY), anim="fade")
            show(c, t, 22.6, CX, 900, strike(330, GRAY), anim="fade", d=0.2)
            show(c, t, 23.2, CX, 990, HL("~15% AO MÊS", 76, PINKISH, RED), anim="stamp")
            show(c, t, 24.9, 70, 1120, L("R$ 1.000", 70, INK, MARKER), anim="left", d=0.3)
            show(c, t, 25.9, 380, 1120, L("+R$ 150", 84, RED, MARKER), anim="stamp", d=0.3)
            show(c, t, 27.3, CX, 1210, T("em 30 dias", 56, DGRAY), anim="up")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (20.1, "head"), (22.6, "present_l")], [(0, "think"), (20.1, "shocked"), (22.6, "worried")], look=-0.8)
    elif t < 40.3:  # 3
        show(c, t, 30.1, CX, 900, MM("só o mínimo?", 90, NAVY), anim="stamp", t1=32.1)
        if 30.6 < t < 32.1:
            show(c, t, 30.6, CX, 900, strike(600), anim="fade", d=0.2)
        if t >= 32.1:
            show(c, t, 32.1, 150, 870, sc(calendar, "30", RED, 56, s=1.2), anim="pop")
            show(c, t, 32.5, 270, 850, L("1 mês no rotativo", 58, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 34.0, 270, 930, L("o banco tem que oferecer", 48, DGRAY), anim="left", d=0.3)
            show(c, t, 35.1, CX, 1040, HL("PARCELAR A FATURA", 72, LYELLOW), anim="stamp")
            show(c, t, 36.7, CX, 1130, T("costuma ter juros menores", 52, DGRAY), anim="up")
        if t >= 38.5:
            show(c, t, 38.5, CX, 1210, HL("compara antes de aceitar", 56, LGREEN), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (32.1, "present_l"), (38.5, "thumb")], [(0, "confident"), (38.5, "happy")], look=-0.8)
    elif t < 52.6:  # 4
        show(c, t, 41.4, CX, 810, HL("dívida mais barata", 68, LYELLOW), anim="stamp")
        base, scl = 1220, 1.3
        for t0, x, v, lab, top, col in ((44.6, 230, 150, "rotativo", "R$ 150", RED), (48.7, 560, 25, "consignado", "R$ 20 a 30", GREEN)):
            if t > t0:
                h = v * scl * ease_out(prog(t, t0, 0.6))
                rrect(c, x - 100, base - h, 200, h, 12); fs(c, col if col == GREEN else PINKISH, 6)
                show(c, t, t0 + 0.5, x, base - v * scl - 40, MM(top, 60, col), anim="pop")
                show(c, t, t0 + 0.2, x, base + 50, T(lab, 48, DGRAY), anim="up")
        line(c, 100, base, 720, base, 6)
        show(c, t, 47.7, CX, 890, T("juros de R$ 1.000 por mês", 50, DGRAY), anim="up")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (44.6, "point_l"), (49.0, "thumb")], [(0, "confident"), (49.0, "happy")], look=-0.8)
    elif t < 68.7:  # 5
        show(c, t, 53.6, CX, 810, HL("TETO DA LEI", 84, LYELLOW), anim="stamp")
        if t < 61.3:
            show(c, t, 55.1, CX, 900, T("desde 2024", 56, DGRAY), anim="up")
            show(c, t, 57.1, CX, 1000, MM("juros + encargos", 70, NAVY), anim="stamp")
            show(c, t, 59.4, CX, 1100, T("até o valor da dívida", 60, INK), anim="up")
        else:
            show(c, t, 61.3, 70, 930, L("R$ 1.000", 76, INK, MARKER), anim="left", d=0.3)
            show(c, t, 62.0, 410, 935, L("nunca passa de", 52, DGRAY), anim="left", d=0.3)
            show(c, t, 63.3, 70, 1030, L("R$ 2.000", 90, RED, MARKER), anim="stamp", d=0.3)
            if t > 64.2:
                # 5 meses de rotativo: barras subindo até o teto
                for k, v in enumerate((1153, 1329, 1533, 1767, 2000)):
                    t0 = 65.7 + k * 0.35
                    if t > t0:
                        h = (v - 900) * 0.10 * ease_out(prog(t, t0, 0.3))
                        rrect(c, 430 + k * 70, 1230 - h, 52, h, 8); fs(c, PINKISH if k < 4 else RED, 5)
                line(c, 410, 1230, 790, 1230, 5)
                show(c, t, 67.4, 230, 1180, MM("em 5 meses", 56, RED), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (61.3, "present_l"), (67.2, "head")], [(0, "confident"), (67.2, "shocked")], look=-0.8)
    else:  # fim
        show(c, t, 68.8, 370, 830, MM("QUAL É O JURO", 76, NAVY), anim="stamp")
        show(c, t, 69.5, 370, 950, MM("DO SEU CARTÃO?", 78, RED), anim="stamp")
        show(c, t, 70.7, 190, 1110, sc(phone, s=1.0), anim="pop")
        show(c, t, 71.4, 470, 1110, HL("COMENTA AÍ", 76, LYELLOW), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "point_l")], [(0, "happy"), (71.6, "grin")], look=-0.8)


def cena(c, t):
    floor(c)
    lista(c, t)
    palco(c, t)


SCENES = [(0, 999.0, cena)]
