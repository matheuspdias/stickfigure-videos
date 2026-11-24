"""Dólar a R$ 6: o que fica mais caro no seu bolso. Só TikTok: vertical 1080x1920, ~75,4 s, ESTILO CADERNO (palito).
Refeito em 24/11/2026 (a versão ilustrada de 23/11 não chegou a ser postada): o TikTok voltou ao caderno,
que fez 16 dos 18 vídeos mais vistos do perfil. Mesma narração (Consultor BR B, 1 bloco). Contas em contas.py.
Layout vertical: título y~250, palco y 360-1290 (pés em 1280), legendas em y~1400-1460, abaixo de 1500 a interface
do TikTok, nada importante em x > 930. Quadro 0: a cotação já subindo de R$ 5 para R$ 6."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(4.7, "tum"), (24.0, "tum"), (56.7, "tum"), (74.6, "soft_ding")]
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


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def cotacao(c, t, t0, x, y, size=150):
    """R$ 5,00 subindo até R$ 6,00 a partir de t0"""
    v = 5.0 + ease_io(prog(t, t0, 1.6))
    col = INK if v < 5.6 else RED
    pop = 1 + 0.10 * math.sin(clamp01((t - t0 - 1.6) / 0.25) * math.pi) if t > t0 + 1.6 else 1
    c.save(); c.translate(x, y); c.scale(pop, pop)
    text(c, ("R$ %.2f" % v).replace(".", ","), 0, 0, size, MARKER, col)
    c.restore()


def linha_item(c, t, t0, y, icon, titulo, t2, motivo):
    show(c, t, t0, 190, y, icon, anim="pop")
    show(c, t, t0 + 0.2, 330, y - 30, L(titulo, 54, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, t2, 330, y + 40, L(motivo, 44, DGRAY), anim="up")


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.3  gancho: a cotação sobe na tela
    floor(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "DÓLAR HOJE", NAVY, 60), anim="stamp", d=0.3)
    show(c, t, -1.0, 230, 470, sc(dollar_bill, s=1.3), anim="pop")
    show(c, t, -1.0, 420, 470, MM("=", 100, INK), anim="pop")
    cotacao(c, t, 0.0, 660, 480, 110)
    show(c, t, 2.3, CX, 680, T("um mês atrás:", 56, DGRAY), anim="up")
    show(c, t, 3.6, CX, 790, MM("R$ 5,00", 96, GRAY), anim="pop")
    show(c, t, 4.7, CX, 960, lambda c: hl(c, "+20%", 0, 0, 120, PINKISH, RED), anim="stamp")
    hero(c, t, 820, FY, 0.6, [(0, "present_l"), (4.7, "head")], [(0, "neutral"), (4.7, "shocked")], look=-0.6)


def s02(c, t):  # 6.3 - 11.6  a pergunta
    floor(c)
    show(c, t, 6.4, CX, 300, M("O QUE FICA", 96, NAVY), anim="stamp")
    show(c, t, 7.4, CX, 420, M("MAIS CARO", 110, RED), anim="stamp")
    show(c, t, 8.8, CX, 550, lambda c: hl(c, "no SEU bolso?", 0, 0, 84, LYELLOW), anim="stamp")
    show(c, t, 9.4, 780, 880, sc(qmark, 140, NAVY), anim="pop")
    show(c, t, 10.6, CX, 720, T("faz a conta comigo", 56, GOLD), anim="up")
    hero(c, t, CX, FY, 0.65, [(0, "think"), (10.6, "point_ru")], [(0, "think"), (10.6, "confident")], look=0.2)


def s03(c, t):  # 11.6 - 29.7  1. a viagem
    floor(c)
    show(c, t, 11.7, CX, 250, lambda c: ribbon(c, "1. A VIAGEM", NAVY, 62), anim="stamp")
    show(c, t, 12.5, 300, 420, sc(plane, s=0.9), anim="left")
    show(c, t, 13.2, 740, 420, group(sc(suitcase, ORANGE, s=0.55), at(0, 120, MM("US$ 1.000", 52, NAVY))), anim="pop")
    # um mês atrás
    show(c, t, 14.8, 80, 640, L("um mês atrás", 48, DGRAY), anim="left", d=0.3)
    show(c, t, 15.7, 80, 720, L("R$ 5.000", 60, INK, MARKER), anim="left", d=0.3)
    show(c, t, 17.0, 360, 720, L("+ IOF 3,5%", 48, DGRAY), anim="left", d=0.3)
    show(c, t, 19.3, 640, 720, L("= R$ 5.175", 60, NAVY, MARKER), anim="left", d=0.3)
    # hoje
    show(c, t, 21.4, 80, 840, L("hoje", 48, DGRAY), anim="left", d=0.3)
    show(c, t, 22.0, 80, 930, L("R$ 6.210", 96, RED, MARKER), anim="stamp", d=0.3)
    show(c, t, 24.0, 680, 920, lambda c: hl(c, "+ R$ 1.035", 0, 0, 64, PINKISH, RED), anim="stamp")
    show(c, t, 26.1, 680, 1010, T("pela mesma viagem", 42, DGRAY), anim="up")
    show(c, t, 27.5, CX, 1110, T("(e antes da taxa do banco)", 42, GRAY), anim="fade")
    hero(c, t, 860, FY, 0.55, [(0, "present_l"), (24.0, "head")], [(0, "neutral"), (24.0, "shocked")], look=-0.8)


def s04(c, t):  # 29.7 - 41.7  2. a comprinha na gringa
    floor(c)
    show(c, t, 29.8, CX, 250, lambda c: ribbon(c, "2. A COMPRINHA", NAVY, 62), anim="stamp")
    show(c, t, 31.4, 230, 440, sc(package, "US$ 40", s=1.2), anim="drop")
    show(c, t, 32.4, 520, 440, L("de 40 dólares", 56, NAVY, MARKER), anim="left", d=0.3)
    base, scl = 990, 1.6
    for t0, x, v, lab, col in ((33.5, 330, 200, "antes", LGRAY), (35.5, 690, 240, "hoje", RED)):
        if t > t0:
            h = v * scl * ease_out(prog(t, t0, 0.6))
            rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
            show(c, t, t0 + 0.6, x, base - v * scl - 50, MM("R$ %d" % v, 64, INK if col == LGRAY else RED), anim="pop")
            show(c, t, t0 + 0.2, x, base + 50, T(lab, 48, DGRAY), anim="up")
    line(c, 160, base, 820, base, 6)
    show(c, t, 37.4, CX, 1120, T("antes dos impostos", 44, GRAY), anim="fade", t1=38.9)
    show(c, t, 39.0, 420, 1110, lambda c: hl(c, "imposto em cima do valor maior", 0, 0, 42, PINKISH, RED), anim="stamp")
    hero(c, t, 920, FY, 0.5, [(0, "point_l"), (36.1, "head")], [(0, "neutral"), (36.1, "shocked")], look=-1)


def s05(c, t):  # 41.7 - 55.3  3. o que chega devagar
    floor(c)
    show(c, t, 41.8, CX, 250, lambda c: ribbon(c, "3. CHEGA DEVAGAR", NAVY, 60), anim="stamp")
    linha_item(c, t, 44.1, 440, sc(gas_pump, s=0.55), "gasolina e diesel", 45.4, "petróleo é em dólar")
    linha_item(c, t, 47.7, 660, sc(bread, s=0.7), "pão, macarrão, biscoito", 49.5, "o trigo vem de fora")
    linha_item(c, t, 52.0, 880, sc(phone, s=0.8), "celular e eletrônico", 53.3, "peças importadas")
    hero(c, t, CX, FY, 0.55, [(0, "present"), (52.0, "point_ru")], [(0, "neutral"), (47.7, "worried")], look=0.0)


def s06(c, t):  # 55.3 - 64.5  a virada
    floor(c)
    show(c, t, 55.4, CX, 250, lambda c: ribbon(c, "MAS TEM UM DETALHE", RED, 58), anim="stamp")
    show(c, t, 56.4, 440, 420, MM("+20% amanhã?", 84, INK), anim="stamp")
    if t > 56.7:
        show(c, t, 56.7, 860, 420, sc(x_icon, 46), anim="pop")
    show(c, t, 58.7, 240, 640, sc(moving_box, s=0.8), anim="drop")
    show(c, t, 59.3, 420, 620, L("as lojas têm", 50, DGRAY), anim="left", d=0.3)
    show(c, t, 59.4, 420, 690, L("estoque e contrato", 56, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 61.0, CX, 860, T("o que pesa é", 56), anim="up")
    show(c, t, 62.1, CX, 980, lambda c: hl(c, "QUANTO TEMPO", 0, 0, 90, LYELLOW), anim="stamp")
    show(c, t, 63.0, CX, 1090, T("o dólar fica lá em cima", 50, DGRAY), anim="up")
    hero(c, t, 860, FY, 0.55, [(0, "finger_up"), (62.1, "point_l")], [(0, "think"), (62.1, "confident")], look=-0.8)


def s07(c, t):  # 64.5 - 72.4  a dica
    floor(c)
    show(c, t, 64.6, CX, 250, lambda c: ribbon(c, "A DICA", GOLD, 70, INK), anim="stamp")
    show(c, t, 65.9, CX, 400, T("tem compra em dólar pra fazer?", 52), anim="up")
    show(c, t, 67.5, CX, 520, MM("tudo num dia só", 72, RED), anim="stamp", t1=69.4)
    if 68.0 < t < 69.4:
        show(c, t, 68.0, CX, 520, strike(560), anim="fade", d=0.2)
    if t > 69.6:
        show(c, t, 69.6, CX, 520, lambda c: hl(c, "DIVIDE EM PARTES", 0, 0, 80, LGREEN), anim="stamp")
        for i, x in enumerate((200, 410, 620, 830)):
            show(c, t, 69.9 + i * 0.2, x, 720, sc(calendar, str(5 + 7 * i), GOLD, 56), anim="pop")
    show(c, t, 70.8, CX, 900, lambda c: hl(c, "o preço fica na média", 0, 0, 60, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.6, [(0, "present"), (69.6, "thumb")], [(0, "neutral"), (69.6, "happy")], look=0.0)


def s08(c, t):  # 72.4 - fim  comenta
    floor(c)
    show(c, t, 72.5, CX, 330, M("TEM CONTA EM DÓLAR", 72, NAVY), anim="stamp")
    show(c, t, 73.4, CX, 440, M("PRA PAGAR?", 86, RED), anim="stamp")
    show(c, t, 72.8, CX, 620, sc(dollar_bill, s=1.4), anim="pop")
    show(c, t, 74.6, CX, 840, lambda c: hl(c, "COMENTA AÍ", 0, 0, 84, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.65, [(0, "point_ru")], [(0, "happy"), (74.6, "grin")], look=0.3)


SCENES = [
    (0.0, 6.3, s01), (6.3, 11.6, s02), (11.6, 29.7, s03), (29.7, 41.7, s04),
    (41.7, 55.3, s05), (55.3, 64.5, s06), (64.5, 72.4, s07), (72.4, 999.0, s08),
]
