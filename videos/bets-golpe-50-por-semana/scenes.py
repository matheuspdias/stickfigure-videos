"""Bets proibidas, mas o golpe não (e a conta dos R$ 50 por semana). Só TikTok: vertical 1080x1920, ~73 s, ESTILO CADERNO.
Modelo: videos/salario-minimo-2027-o-que-muda/. Contas (contas.py): MP 1.394/2026 em vigor desde 06/10/2026;
60.477 endereços suspeitos (IBJR/LegitBet, até 27/10); operação da PCDF ~R$ 739 mi via Pix para empresas de fachada;
R$ 50/semana = R$ 216,67/mês = R$ 2.600/ano; CDB 100% CDI (13,65%) ~R$ 2.750 líquido em 1 ano, ~R$ 17.500 em 5 anos; metade = R$ 1.300/ano.
Ângulo só de dinheiro e risco, sem opinião sobre a proibição.
Layout: título y~250, palco 360-1290 (pés em 1280), legendas ~1400-1460, nada em x > 930.
Quadro 0: o contador de sites suspeitos já subindo."""
from engine import *  # noqa

VERTICAL = True

CX = 420
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(10.8, "tum"), (22.3, "tum"), (37.0, "tum"), (47.3, "tum"), (59.8, "tum"), (72.3, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


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


def reais(c, t, t0, a, b, x, y, size, col, d=0.8, pre="R$ ", suf="", align="c"):
    v = a + (b - a) * ease_out(prog(t, t0, d))
    s = f"{v:,.0f}".replace(",", ".")
    text(c, m(pre + s + suf), x, y, size, MARKER, col, align=align)


def titulo(c, t, s):
    show(c, t, -1.0, 540, 250, lambda c: ribbon(c, s, NAVY, 56), anim="stamp", d=0.3)


def palco(c, t):
    floor(c)
    if t < 13.3:  # gancho
        titulo(c, t, "BETS PROIBIDAS")
        show(c, t, -1.0, 170, 440, sc(calendar, "OUT", RED, 50, s=0.8), anim="pop")
        show(c, t, -1.0, 290, 440, L("proibidas desde outubro", 50, DGRAY), anim="left", d=0.3)
        reais(c, t, -0.5, 0, 60477, CX, 640, 150, RED, d=8.0, pre="")
        show(c, t, 7.1, CX, 760, T("endereços suspeitos de aposta", 54, DGRAY), anim="up")
        show(c, t, 9.3, 150, 960, sc(phone, s=0.9), anim="pop")
        show(c, t, 9.6, 270, 930, L("o seu dinheiro lá", 52, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 10.8, 270, 1010, L("reclamar pra quem?", 50, DGRAY), anim="left", d=0.3)
        show(c, t, 12.4, CX, 1170, HL("OLHA A CONTA", 70, LYELLOW), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "head"), (9.3, "point_l"), (12.4, "finger_up")], [(0, "shocked"), (9.3, "worried"), (12.4, "confident")], look=-0.7)
    elif t < 27.0:
        titulo(c, t, "LEGAL x CLANDESTINO")
        show(c, t, 13.4, 210, 430, MM("legalizado", 46, GREEN), anim="stamp")
        show(c, t, 14.8, 220, 540, sc(bank, s=0.6), anim="pop")
        show(c, t, 15.7, 220, 660, T("tinha que ter", 46, DGRAY), anim="up")
        show(c, t, 16.2, 220, 720, T("dinheiro pro prêmio", 46, DGRAY), anim="up")
        show(c, t, 17.8, 620, 430, MM("clandestino", 46, RED), anim="stamp")
        show(c, t, 19.3, 600, 560, sc(big_x, 70), anim="stamp")
        show(c, t, 19.4, 600, 690, T("regra nenhuma", 50, RED), anim="up")
        line(c, 410, 390, 410, 760, 4, LGRAY)
        show(c, t, 20.5, CX, 860, MM("ganhou?", 70, NAVY), anim="stamp")
        show(c, t, 22.3, CX, 970, HL("PODE NÃO RECEBER", 60, PINKISH, RED), anim="stamp")
        show(c, t, 23.3, 70, 1100, L("sem órgão pra reclamar", 50, DGRAY), anim="left", d=0.3)
        show(c, t, 24.8, 70, 1170, L("sem empresa no Brasil", 50, DGRAY), anim="left", d=0.3)
        hero(c, t, 860, FY, 0.85, [(0, "present_l"), (17.8, "point_l"), (22.3, "head"), (23.3, "shrug")],
             [(0, "confident"), (17.8, "think"), (22.3, "shocked"), (23.3, "worried")], look=-0.7)
    elif t < 39.7:
        titulo(c, t, "PRA ONDE VAI O PIX")
        show(c, t, 27.2, 200, 440, sc(pix_tag, s=1.0), anim="pop")
        show(c, t, 27.7, 340, 430, L("não vai pra", 50, DGRAY), anim="left", d=0.3)
        show(c, t, 28.4, 340, 500, L("casa de aposta", 56, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 29.7, CX, 590, T("operação da polícia do DF", 52, DGRAY), anim="up")
        for k, t0 in enumerate((33.7, 34.0, 34.3)):
            show(c, t, t0, 170 + k * 250, 810, sc(door, "?", NAVY, 0.0, 120, 160, s=0.9), anim="drop")
        show(c, t, 34.2, CX, 950, MM("empresas de fachada", 60, RED), anim="stamp")
        show(c, t, 35.0, CX, 1030, T("até uma clínica", 52, DGRAY), anim="up")
        if t > 36.6:
            reais(c, t, 36.6, 0, 740, CX, 1170, 100, RED, d=1.6, pre="~R$ ", suf=" MI")
        hero(c, t, 860, FY, 0.85, [(0, "point_l"), (29.7, "finger_up"), (36.6, "head")], [(0, "confident"), (29.7, "think"), (36.6, "shocked")], look=-0.7)
    elif t < 50.3:
        titulo(c, t, "A VIRADA")
        show(c, t, 41.0, CX, 440, T("se você apostava", 54, DGRAY), anim="up")
        show(c, t, 41.9, CX, 560, HL("R$ 50 POR SEMANA", 80, LYELLOW), anim="stamp")
        show(c, t, 43.7, CX, 700, MM("= ~R$ 217 por mês", 66, NAVY), anim="stamp")
        show(c, t, 46.2, 150, 880, sc(calendar, "1 ANO", RED, 40, s=1.0), anim="pop")
        if t > 47.3:
            reais(c, t, 47.3, 0, 2600, 270, 900, 92, RED, d=1.0, align="l")
        show(c, t, 48.8, CX, 1060, HL("SAÍRAM DA SUA CONTA", 54, PINKISH, RED), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "finger_up"), (41.9, "present_l"), (47.3, "head")], [(0, "think"), (41.9, "confident"), (47.3, "shocked")], look=-0.7)
    elif t < 61.9:
        titulo(c, t, "NUM CDB 100% DO CDI")
        if t < 57.5:
            base, scl = 960, 0.17
            for t0, x, v, lab, top, col in ((51.0, 220, 2600, "depositado", "R$ 2.600", GRAY), (54.1, 560, 2750, "no CDB", "~R$ 2.750", GREEN)):
                if t > t0:
                    h = v * scl * ease_out(prog(t, t0, 0.6))
                    rrect(c, x - 100, base - h, 200, h, 12); fs(c, LGREEN if col == GREEN else LGRAY, 6)
                    show(c, t, t0 + 0.4, x, base - v * scl - 40, MM(top, 58, col), anim="pop")
                    show(c, t, t0 + 0.2, x, base + 55, T(lab, 48, DGRAY), anim="up")
            line(c, 100, base, 720, base, 6)
            show(c, t, 56.3, CX, 1130, HL("já sem imposto", 62, LGREEN, GREEN), anim="stamp")
        else:
            show(c, t, 57.5, CX, 470, MM("em 5 anos", 76, NAVY), anim="stamp")
            show(c, t, 58.6, CX, 570, T("com a taxa de hoje", 52, DGRAY), anim="up")
            if t > 59.8:
                reais(c, t, 59.8, 2600, 17500, CX, 760, 140, GREEN, d=1.2, pre="~R$ ")
            show(c, t, 60.6, CX, 900, T("(R$ 13 mil depositados)", 50, DGRAY), anim="up")
        hero(c, t, 860, FY, 0.85, [(0, "present_l"), (54.1, "point_l"), (59.8, "arms_up")], [(0, "confident"), (54.1, "happy"), (59.8, "grin")], look=-0.7)
    elif t < 69.1:
        titulo(c, t, "NÃO PRECISA SER TUDO")
        show(c, t, 63.5, CX, 470, MM("só a metade:", 66, NAVY), anim="stamp")
        show(c, t, 64.2, CX, 580, HL("R$ 25 POR SEMANA", 70, LYELLOW), anim="stamp")
        show(c, t, 65.2, 190, 790, sc(piggy, s=1.0), anim="pop")
        show(c, t, 65.5, 340, 780, L("conta separada", 52, DGRAY), anim="left", d=0.3)
        show(c, t, 66.6, CX, 980, HL("R$ 1.300 NO ANO", 80, LGREEN, GREEN), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "finger_up"), (65.2, "point_l"), (66.6, "thumb")], [(0, "confident"), (66.6, "happy")], look=-0.7)
    else:
        titulo(c, t, "E VOCÊ?")
        show(c, t, 69.8, CX, 500, MM("QUANTO IA PRA", 74, NAVY), anim="stamp")
        show(c, t, 70.4, CX, 620, MM("APOSTA POR SEMANA?", 66, RED), anim="stamp")
        show(c, t, 71.6, 170, 860, sc(phone, s=0.9), anim="pop")
        show(c, t, 72.3, 440, 860, HL("COMENTA AÍ", 64, LYELLOW), anim="stamp")
        hero(c, t, 860, FY, 0.85, [(0, "point_l")], [(0, "happy"), (72.3, "grin")], look=-0.7)


SCENES = [(0, 999.0, palco)]
