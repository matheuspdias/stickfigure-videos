"""Ganha até R$ 5 mil e pode pagar IR em 2027: duas fontes de renda. Só TikTok: vertical 1080x1920, ~74,4 s, ESTILO CADERNO (palito).
1º item [18h] da Fila do Matheus (25/11/2026). Modelo: videos/dolar-6-reais-no-bolso. Contas em contas.py (Lei 15.270/2025):
2 x R$ 3.000 = R$ 72 mil/ano; simplificado 20% -> base R$ 57.600; tabela ~R$ 4.934; redução anual 8.429,73 - 0,095575 x 72.000 = ~R$ 1.548;
a pagar ~R$ 3.385 (~R$ 282/mês). Layout: título y~250, palco y 360-1290 (pés em 1280), legendas ~1400-1460, nada importante em x > 930.
Quadro 0: os dois contracheques já entrando e o "IR R$ 0" carimbando."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(7.3, "tum"), (30.4, "tum"), (49.3, "tum"), (73.3, "soft_ding")]
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


def X(s=46):
    return lambda c: x_icon(c, s)


def holerite(empresa, sal="R$ 3.000"):
    def f(c):
        rrect(c, -180, -150, 360, 300, 18); fs(c, WHITE, 6)
        text(c, empresa, 0, -95, 44, MARKER, NAVY)
        line(c, -140, -60, 140, -60, 4, LGRAY)
        text(c, "salário", -150, -20, 34, HAND, DGRAY, align="l")
        text(c, sal, 150, 30, 50, MARKER, INK, align="r")
        text(c, "IR", -150, 95, 34, HAND, DGRAY, align="l")
    return f


def ir_zero(c):
    text(c, "R$ 0", 0, 0, 52, MARKER, GREEN)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.9  gancho
    floor(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "IR 2027", NAVY, 60), anim="stamp", d=0.3)
    show(c, t, -0.4, 255, 540, holerite("EMPRESA A"), s=1.1, anim="left")
    show(c, t, 0.4, 735, 540, holerite("EMPRESA B"), s=1.1, anim="right")
    show(c, t, 2.7, 335, 640, ir_zero, anim="stamp")
    show(c, t, 3.2, 815, 640, ir_zero, anim="stamp")
    show(c, t, 3.6, CX, 790, T("nenhum desconta imposto", 58, DGRAY), anim="up")
    show(c, t, 5.0, 150, 1000, sc(calendar, "2027", RED, 44, s=1.2), anim="pop")
    show(c, t, 6.4, 330, 950, L("o Leão cobra", 58, INK), anim="left", d=0.3)
    show(c, t, 7.3, 530, 1090, lambda c: hl(c, m("~R$ 3.400"), 0, 0, 110, PINKISH, RED), anim="stamp")
    hero(c, t, 890, FY, 0.75, [(0, "present_l"), (7.3, "head")], [(0, "neutral"), (7.3, "shocked")], look=-0.8)


def s02(c, t):  # 9.9 - 17.1  a regra
    floor(c)
    show(c, t, 10.0, CX, 250, lambda c: ribbon(c, "DESDE JANEIRO", NAVY, 60), anim="stamp")
    show(c, t, 11.1, CX, 390, T("quem ganha até", 56, DGRAY), anim="up")
    show(c, t, 11.8, CX, 510, MM("R$ 5 mil por mês", 90, NAVY), anim="stamp")
    show(c, t, 12.8, CX, 640, lambda c: hl(c, "IR retido: R$ 0", 0, 0, 70, LGREEN, GREEN), anim="stamp")
    show(c, t, 14.4, CX, 760, T("só que a regra olha", 56), anim="up")
    show(c, t, 15.6, CX, 870, lambda c: hl(c, "CADA FONTE SEPARADA", 0, 0, 64, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.7, [(0, "present"), (14.4, "finger_up")], [(0, "neutral"), (14.4, "think")], look=0.0)


def s03(c, t):  # 17.1 - 23.0  ninguém vê o todo
    floor(c)
    show(c, t, 17.2, 250, 490, sc(bank, s=1.3), anim="pop")
    show(c, t, 17.4, 250, 300, M("EMPRESA A", 56, NAVY), anim="stamp")
    show(c, t, 18.5, 250, 690, MM("vê R$ 3 mil", 64, INK), anim="up")
    show(c, t, 19.3, 790, 490, sc(bank, s=1.3), anim="pop")
    show(c, t, 19.5, 790, 300, M("EMPRESA B", 56, NAVY), anim="stamp")
    show(c, t, 20.5, 790, 690, MM("vê R$ 3 mil", 64, INK), anim="up")
    show(c, t, 21.6, CX, 830, lambda c: hl(c, "ninguém desconta nada", 0, 0, 72, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.75, [(0, "shrug")], [(0, "think"), (21.6, "worried")], look=0.0)


def s04(c, t):  # 23.0 - 35.4  a declaração soma tudo
    floor(c)
    show(c, t, 23.1, CX, 250, lambda c: ribbon(c, "DECLARAÇÃO 2027", NAVY, 58), anim="stamp")
    show(c, t, 23.4, 200, 450, sc(document, "IR", RED, 44, s=1.3), anim="drop")
    show(c, t, 24.4, 330, 410, L("entregue em 2027", 46, DGRAY), anim="left", d=0.3)
    show(c, t, 26.0, 330, 490, L("sobre o que ganhou em 2026", 46, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 28.0, CX, 630, lambda c: hl(c, "SOMA TUDO", 0, 0, 80, LYELLOW), anim="stamp")
    show(c, t, 29.2, 80, 780, L("R$ 6.000 x 12", 64, INK, MARKER), anim="left", d=0.3)
    show(c, t, 30.4, 80, 900, L("= R$ 72 mil no ano", 76, RED, MARKER), anim="stamp", d=0.3)
    show(c, t, 32.6, 80, 1030, L("isenção completa:", 48, DGRAY), anim="left", d=0.3)
    show(c, t, 33.9, 80, 1120, lambda c: hl(c, "só até R$ 60 mil", 0, 0, 62, LGREEN, GREEN, rot=0) if False else text(c, "só até R$ 60 mil", 0, 0, 62, MARKER, GREEN, align="l"), anim="stamp", d=0.3)
    hero(c, t, 880, FY, 0.75, [(0, "present_l"), (30.4, "head")], [(0, "neutral"), (30.4, "shocked")], look=-0.8)


def s05(c, t):  # 35.4 - 52.4  a conta
    floor(c)
    show(c, t, 35.5, CX, 250, lambda c: ribbon(c, "A CONTA", RED, 66), anim="stamp")
    x = 80
    show(c, t, 35.6, x, 390, L("R$ 72.000", 64, INK, MARKER), anim="left", d=0.3)
    show(c, t, 36.2, x, 470, L("- 20% (desconto simplificado)", 44, DGRAY), anim="left", d=0.3)
    show(c, t, 38.0, x, 560, L("= R$ 57.600 na tabela", 58, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 41.2, x, 670, L("imposto: ~R$ 4.900", 62, RED, MARKER), anim="stamp", d=0.3)
    show(c, t, 43.7, x, 770, L("- lei nova: ~R$ 1.500", 58, GREEN, MARKER), anim="left", d=0.3)
    show(c, t, 46.5, x, 840, L("(quem fica entre 60 e 88 mil/ano)", 38, GRAY), anim="fade")
    if t > 48.9:
        line(c, x, 880, x + 560 * ease_out(prog(t, 48.9, 0.4)), 880, 6, INK)
    show(c, t, 49.3, 450, 990, lambda c: hl(c, "A PAGAR: ~R$ 3.400", 0, 0, 72, PINKISH, RED), anim="stamp")
    show(c, t, 51.3, 450, 1110, T("até o fim de maio de 2027", 46, DGRAY), anim="up")
    hero(c, t, 900, FY, 0.7, [(0, "point_l"), (49.3, "head")], [(0, "neutral"), (41.2, "worried"), (49.3, "shocked")], look=-1)


def s06(c, t):  # 52.4 - 61.8  a virada
    floor(c)
    show(c, t, 52.5, CX, 300, M("PARECE MULTA?", 84, NAVY), anim="stamp")
    show(c, t, 53.6, 900, 380, X(40), anim="pop")
    show(c, t, 54.5, CX, 440, T("é o imposto que", 56), anim="up")
    show(c, t, 55.3, CX, 550, lambda c: hl(c, "NINGUÉM RETEVE", 0, 0, 84, LYELLOW), anim="stamp")
    show(c, t, 56.1, CX, 660, T("durante o ano", 52, DGRAY), anim="up")
    show(c, t, 57.3, CX, 780, T("vale pra quem tem:", 48, DGRAY), anim="up")
    show(c, t, 58.0, 110, 875, sc(check_icon, 30), anim="pop")
    show(c, t, 58.0, 160, 895, L("dois empregos", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 59.4, 110, 975, sc(check_icon, 30), anim="pop")
    show(c, t, 59.4, 160, 995, L("aposentado que trabalha", 50, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 60.5, 160, 1070, L("com carteira", 50, NAVY, MARKER), anim="left", d=0.3)
    hero(c, t, 900, FY, 0.7, [(0, "finger_up"), (58.0, "point_l")], [(0, "think"), (55.3, "confident")], look=-0.8)


def s07(c, t):  # 61.8 - 71.2  a saída
    floor(c)
    show(c, t, 61.9, CX, 250, lambda c: ribbon(c, "A SAÍDA", GREEN, 70), anim="stamp")
    show(c, t, 62.9, 230, 470, sc(piggy, s=1.0), anim="pop")
    show(c, t, 63.3, 400, 430, L("guarda uns", 52, DGRAY), anim="left", d=0.3)
    show(c, t, 63.5, 400, 530, L("R$ 300/mês", 76, GREEN, MARKER), anim="stamp", d=0.3)
    show(c, t, 64.8, 400, 610, L("a partir de agora", 46, DGRAY), anim="up")
    show(c, t, 66.2, 230, 830, sc(document, "RECIBO", NAVY, 26, s=1.1), anim="drop")
    show(c, t, 66.9, 400, 790, L("médico e dentista", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 68.4, 400, 880, L("podem baixar a conta", 46, DGRAY), anim="up")
    show(c, t, 69.7, 470, 1000, lambda c: hl(c, "na declaração completa", 0, 0, 56, LGREEN), anim="stamp")
    hero(c, t, 900, FY, 0.7, [(0, "present_l"), (63.5, "thumb")], [(0, "neutral"), (63.5, "happy")], look=-0.8)


def s08(c, t):  # 71.2 - fim  comenta
    floor(c)
    show(c, t, 71.3, CX, 330, M("TEM MAIS DE UMA", 74, NAVY), anim="stamp")
    show(c, t, 72.2, CX, 440, M("FONTE DE RENDA?", 82, RED), anim="stamp")
    show(c, t, 71.6, 310, 640, holerite("EMPRESA A"), s=0.8, anim="pop")
    show(c, t, 71.9, 730, 640, holerite("EMPRESA B"), s=0.8, anim="pop")
    show(c, t, 73.3, CX, 860, lambda c: hl(c, "COMENTA AÍ", 0, 0, 84, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.7, [(0, "point_ru")], [(0, "happy"), (73.3, "grin")], look=0.3)


SCENES = [
    (0.0, 9.9, s01), (9.9, 17.1, s02), (17.1, 23.0, s03), (23.0, 35.4, s04),
    (35.4, 52.4, s05), (52.4, 61.8, s06), (61.8, 71.2, s07), (71.2, 999.0, s08),
]
