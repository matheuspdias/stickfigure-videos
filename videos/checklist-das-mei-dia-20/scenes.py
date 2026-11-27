"""CHECKLIST DO CONSULTOR: "3 passos antes do dia 20" (DAS do MEI). Só TikTok: vertical 1080x1920, ~71 s, ESTILO CADERNO (palito).
Modelo: videos/checklist-vale-alimentacao/. Contas (contas.py): DAS serviços 2026 R$ 86,05; multa 0,33%/dia até 20% + juros Selic;
12 DAS esquecidos ~R$ 1.300 ("mais de R$ 1.200"); parcelamento até 60x, mínima R$ 50; qualidade de segurado 12 meses;
R$ 86 / 30 = R$ 2,87 por dia; DASN-SIMEI até 31/05.
Layout: lista de 3 passos y 300-560; marcador y ~650; palco 740-1280 (pés em 1280); legendas ~1400-1460; nada em x > 930.
Quadro 0: o boleto do DAS já na tela e o valor contando de R$ 0 a R$ 86."""
from engine import *  # noqa

VERTICAL = True

CX = 400
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(4.0, "tum"), (8.5, "tum"), (25.0, "tum"), (47.3, "tum"), (70.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(8.5, "paga até o dia 20", 24.9), (25.0, "procura mês atrasado", 47.2), (47.3, "separa no dia que entra", 64.5)]
LIN0, LINH = 320, 100


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


def reais(c, t, t0, a, b, x, y, size, col, d=0.8, pre="R$ ", suf="", align="c"):
    v = a + (b - a) * ease_out(prog(t, t0, d))
    s = f"{v:,.0f}".replace(",", ".")
    text(c, m(pre + s + suf), x, y, size, MARKER, col, align=align)


def lista(c, t):
    show(c, t, -1.0, 540, 205, lambda c: ribbon(c, "MEI: ANTES DO DIA 20", NAVY, 54), anim="stamp", d=0.3)
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = LIN0 + i * LINH
        if t0 - 0.6 <= t < t1:
            rrect(c, 70, y - 40, 880, 80, 14); fs(c, LYELLOW, 0)
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
            text(c, nome, 190, y + 18, 58, MARKER, NAVY if t < t1 else DGRAY, align="l")
            c.restore()
    line(c, 60, 580, 1020, 580, 4, LGRAY)


def marcador(c, t):
    """o DAS que atravessa o vídeo"""
    text(c, "atrasado:" if 21.0 <= t < 47.3 else "seu DAS:", 80, 668, 50, HAND, DGRAY, align="l")
    if t < 21.0:
        reais(c, t, -0.6, 0, 86, 290, 672, 76, NAVY, d=2.6, align="l")
        show(c, t, 6.0, 620, 640, HL("/mês", 44, LYELLOW), anim="pop")
    elif t < 47.3:
        reais(c, t, 21.0, 86, 1200, 290, 672, 76, RED, d=1.6, pre="+R$ ", align="l")
        show(c, t, 21.0, 810, 640, HL("1 ano", 44, PINKISH, RED), anim="pop")
    elif t < 56.5:
        text(c, m("R$ 86"), 290, 672, 76, MARKER, NAVY, align="l")
        show(c, t, 52.6, 620, 640, HL("separado", 44, LGREEN, GREEN), anim="pop")
    else:
        text(c, m("< R$ 3"), 290, 672, 76, MARKER, GOLD, align="l")
        show(c, t, 56.7, 620, 645, HL("/dia", 44, LYELLOW), anim="pop")


# ======================================================================= PALCO (y 740-1280)
def palco(c, t):
    if t < 8.5:  # gancho
        show(c, t, -1.0, 190, 900, sc(boleto, "DAS", ORANGE, s=0.75), anim="pop")
        show(c, t, -0.5, 360, 830, L("MEI", 76, NAVY, MARKER), anim="stamp", d=0.3)
        show(c, t, 1.6, 360, 910, L("boleto do mês", 50, DGRAY), anim="left", d=0.3)
        show(c, t, 4.0, 470, 1010, sc(calendar, "20", RED, 60, s=0.7), anim="pop")
        show(c, t, 5.2, CX, 1130, MM("3 PASSOS", 72, NAVY), anim="stamp")
        show(c, t, 6.7, CX, 1210, T("salva pra fazer todo mês", 50, NAVY), anim="up")
        hero(c, t, 860, FY, 0.9, [(0, "point_l"), (4.0, "finger_up"), (6.7, "thumb")], [(0, "confident"), (4.0, "think"), (6.7, "happy")], look=-0.6)
    elif t < 25.0:  # 1
        if t < 19.6:
            show(c, t, 9.3, 170, 880, sc(boleto, "DAS", ORANGE, s=0.6), anim="pop")
            show(c, t, 10.0, 300, 840, L("até o dia 20", 62, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 11.0, 300, 915, L("mesmo sem vender", 50, DGRAY), anim="left", d=0.3)
            show(c, t, 12.9, 70, 1010, L("atrasou?", 58, RED, MARKER), anim="left", d=0.3)
            show(c, t, 14.5, 70, 1090, L("multa de 0,33% por dia", 54, INK, MARKER), anim="left", d=0.3)
            show(c, t, 17.1, 70, 1180, L("até 20%", 62, RED, MARKER), anim="stamp", d=0.3)
            show(c, t, 18.5, 500, 1170, HL("+ JUROS", 60, PINKISH, RED), anim="stamp")
        else:
            show(c, t, 19.6, CX, 840, T("parece pouco...", 56, DGRAY), anim="up")
            show(c, t, 21.0, 110, 980, sc(calendar, "12", RED, 56, s=0.7), anim="pop")
            show(c, t, 21.4, 220, 960, L("meses esquecidos", 52, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 22.3, CX, 1150, HL("+ DE R$ 1.200", 80, PINKISH, RED), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (9.3, "point_l"), (12.9, "head"), (19.6, "shrug"), (22.3, "head")],
             [(0, "confident"), (12.9, "worried"), (19.6, "think"), (22.3, "shocked")], look=-0.8)
    elif t < 47.3:  # 2
        if t < 32.4:
            show(c, t, 25.8, 180, 900, sc(phone, s=1.0), anim="pop")
            show(c, t, 26.5, 320, 850, L("app do MEI", 62, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 27.6, 320, 925, L("procura atraso", 52, DGRAY), anim="left", d=0.3)
            show(c, t, 29.5, 120, 1080, sc(boleto, "DAS", ORANGE, s=0.45), anim="drop")
            show(c, t, 30.2, 250, 1080, sc(boleto, "DAS", ORANGE, s=0.45), anim="drop")
            show(c, t, 30.5, 380, 1050, sc(qmark, 90, RED), anim="pop")
            show(c, t, 31.2, 470, 1080, L("nem sabe", 56, RED, MARKER), anim="left", d=0.3)
        elif t < 40.8:
            show(c, t, 32.5, CX, 830, MM("achou?", 66, NAVY), anim="stamp")
            show(c, t, 33.7, 80, 950, L("parcela em até", 52, DGRAY), anim="left", d=0.3)
            show(c, t, 34.4, 460, 950, L("60x", 76, GREEN, MARKER), anim="stamp", d=0.3)
            show(c, t, 36.0, 80, 1050, L("mínima", 52, DGRAY), anim="left", d=0.3)
            show(c, t, 36.8, 290, 1050, L("R$ 50", 76, GREEN, MARKER), anim="stamp", d=0.3)
            show(c, t, 38.9, CX, 1180, HL("deixou? dívida ativa", 56, PINKISH, RED), anim="stamp")
        else:
            show(c, t, 40.8, 140, 880, sc(calendar, "12", RED, 56, s=0.7), anim="pop")
            show(c, t, 41.3, 260, 870, L("meses sem pagar", 54, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 43.2, 200, 1050, sc(shield, BLUE, s=0.8), anim="pop")
            show(c, t, 43.4, 200, 1050, sc(big_x, 70), anim="stamp")
            show(c, t, 43.6, 330, 1040, L("perde o INSS", 62, RED, MARKER), anim="left", d=0.3)
            show(c, t, 45.0, CX, 1190, HL("doente? sem auxílio", 58, PINKISH, RED), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (25.8, "point_l"), (30.5, "shrug"), (32.5, "present_l"), (38.0, "head"), (40.8, "finger_up"), (45.0, "head")],
             [(0, "confident"), (30.5, "worried"), (32.5, "happy"), (38.0, "worried"), (40.8, "think"), (45.0, "shocked")], look=-0.8)
    elif t < 64.5:  # 3
        if t < 55.3:
            show(c, t, 51.1, 170, 880, sc(pos_machine, s=0.8), anim="pop")
            show(c, t, 51.4, 300, 850, L("1ª venda do mês", 56, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 52.6, 120, 1060, sc(pix_tag, "PIX", GREEN, 50), anim="pop")
            show(c, t, 52.9, 250, 1060, L("R$ 86", 70, GREEN, MARKER), anim="left", d=0.3)
            arrow_draw(c, t, 53.6, 470, 1050, 560, 1050, d=0.3)
            show(c, t, 54.0, 640, 1060, sc(piggy, s=0.6), anim="pop")
            show(c, t, 54.4, CX, 1200, T("conta separada", 54, NAVY), anim="up")
        elif t < 59.0:
            show(c, t, 55.3, 80, 870, L("R$ 86 ÷ 30", 80, INK, MARKER), anim="left", d=0.3)
            show(c, t, 56.7, CX, 1060, HL("< R$ 3 POR DIA", 84, LYELLOW, INK), anim="stamp")
        else:
            show(c, t, 59.0, 160, 900, sc(calendar, "31", BLUE, 56, s=0.8), anim="pop")
            show(c, t, 60.2, 290, 860, L("31 de maio", 62, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 61.6, 290, 935, L("declaração anual", 52, DGRAY), anim="left", d=0.3)
            show(c, t, 62.8, CX, 1150, HL("mesmo sem faturar", 62, PINKISH, RED), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (51.1, "point_l"), (56.7, "arms_up"), (59.0, "finger_up")],
             [(0, "confident"), (52.6, "happy"), (56.7, "grin"), (59.0, "think")], look=-0.8)
    elif t < 69.1:  # conclusão
        show(c, t, 64.6, CX, 860, MM("< R$ 3 por dia", 76, GOLD), anim="stamp")
        show(c, t, 66.5, 120, 1030, sc(check_icon, 34), anim="pop")
        show(c, t, 66.7, 180, 1045, L("INSS em dia", 60, GREEN, MARKER), anim="left", d=0.3)
        show(c, t, 67.7, 120, 1150, sc(check_icon, 34), anim="pop")
        show(c, t, 67.8, 180, 1165, L("CNPJ em dia", 60, GREEN, MARKER), anim="left", d=0.3)
        hero(c, t, 880, FY, 0.9, [(0, "present_l"), (66.5, "thumb")], [(0, "confident"), (66.5, "happy")], look=-0.8)
    else:  # fim
        show(c, t, 69.2, 370, 830, MM("VOCÊ É MEI", 76, NAVY), anim="stamp")
        show(c, t, 69.7, 370, 940, MM("DE QUÊ?", 76, RED), anim="stamp")
        show(c, t, 70.2, 190, 1110, sc(phone, s=1.0), anim="pop")
        show(c, t, 70.4, 470, 1110, HL("COMENTA AÍ", 76, LYELLOW), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "point_l")], [(0, "happy"), (70.4, "grin")], look=-0.8)


def cena(c, t):
    floor(c)
    lista(c, t)
    marcador(c, t)
    palco(c, t)


SCENES = [(0, 999.0, cena)]
