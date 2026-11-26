"""CHECKLIST DO CONSULTOR: "3 passos no dia que o vale-alimentação cai". Só TikTok: vertical 1080x1920, ~75 s, ESTILO CADERNO (palito).
Modelo: videos/checklist-sair-do-rotativo/. Contas (contas.py): VA de R$ 600 = R$ 20 por dia; básico do mês ~R$ 250;
sobram R$ 350 / 4 semanas = ~R$ 87 por semana. VA só para alimentos (PAT, Lei 14.442/2022): limpeza e higiene fora.
Layout: lista de 3 passos na folha (y 300-560) escrita passo a passo; marcador do saldo do VA y ~650; palco da conta y 740-1280
(pés em 1280); legendas ~1400-1460; nada importante em x > 930. Quadro 0: o vale já contando de R$ 0 para R$ 600."""
from engine import *  # noqa

VERTICAL = True

CX = 400
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(4.7, "tum"), (12.1, "tum"), (27.5, "tum"), (44.3, "tum"), (73.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(12.1, "compra só o básico", 27.4), (27.5, "separa o carrinho", 44.2), (44.3, "divide por semana", 63.9)]
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
    show(c, t, -1.0, 540, 205, lambda c: ribbon(c, "QUANDO O VALE CAIR", NAVY, 54), anim="stamp", d=0.3)
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
            text(c, nome, 190, y + 18, 60, MARKER, NAVY if t < t1 else DGRAY, align="l")
            c.restore()
    line(c, 60, 580, 1020, 580, 4, LGRAY)


def marcador(c, t):
    """o saldo do VA que atravessa o vídeo"""
    text(c, "saldo do vale:", 80, 668, 50, HAND, DGRAY, align="l")
    if t < 20.4:
        reais(c, t, -0.6, 0, 600, 390, 672, 76, GREEN, d=2.6, align="l")
    elif t < 53.8:
        reais(c, t, 20.4, 600, 350, 390, 672, 76, NAVY, d=1.0, align="l")
        show(c, t, 20.4, 760, 640, HL("-R$ 250", 44, PINKISH, RED), anim="pop", t1=26.0)
    else:
        text(c, m("R$ 87"), 390, 672, 76, MARKER, GOLD, align="l")
        show(c, t, 53.8, 760, 645, HL("/semana", 44, LYELLOW), anim="pop")


# ======================================================================= PALCO (y 740-1280)
def palco(c, t):
    if t < 12.1:  # gancho
        show(c, t, -1.0, 170, 850, sc(card, GREEN, s=1.3), anim="pop")
        text(c, "VA", 170, 868, 50, MARKER, WHITE)
        show(c, t, -1.0, 320, 820, L("caiu!", 70, GREEN, MARKER), anim="stamp", d=0.3)
        show(c, t, 3.5, 320, 900, L("parece muito...", 52, DGRAY), anim="left", d=0.3)
        show(c, t, 4.7, CX, 1010, HL("= R$ 20 POR DIA", 76, PINKISH, RED), anim="stamp")
        show(c, t, 8.4, CX, 1120, MM("3 PASSOS", 72, NAVY), anim="stamp")
        show(c, t, 9.8, CX, 1205, T("salva pro dia que o vale cair", 50, NAVY), anim="up")
        hero(c, t, 860, FY, 0.9, [(0, "head"), (4.7, "shrug"), (8.2, "finger_up")], [(0, "happy"), (4.7, "worried"), (8.2, "confident")], look=-0.6)
    elif t < 27.5:  # 1
        show(c, t, 13.2, 190, 870, sc(cart, s=1.0), anim="pop")
        show(c, t, 13.6, 340, 830, L("compra do mês", 60, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 14.6, 340, 900, L("o que não estraga", 50, DGRAY), anim="left", d=0.3)
        itens = ((15.8, "arroz"), (16.5, "feijão"), (17.4, "óleo"), (17.9, "café"), (18.6, "macarrão"), (19.2, "leite"))
        for k, (t0, s) in enumerate(itens):
            x, y = 70 + (k % 3) * 240, 1000 + (k // 3) * 70
            show(c, t, t0, x, y, L(s, 44, NAVY, MARKER), anim="left", d=0.25, t1=23.0)
        if t >= 20.0:
            show(c, t, 20.0, CX, 1180, HL("~R$ 250 no dia 1", 70, LYELLOW), anim="stamp", t1=23.0)
        show(c, t, 23.0, CX, 1050, MM("o essencial", 76, NAVY), anim="stamp")
        show(c, t, 24.4, CX, 1160, HL("GARANTIDO", 80, LGREEN, GREEN), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (13.2, "point_l"), (24.4, "thumb")], [(0, "confident"), (24.4, "happy")], look=-0.8)
    elif t < 44.3:  # 2
        if t < 39.4:
            show(c, t, 28.5, 180, 840, sc(cart, LGREEN, s=0.8), anim="pop")
            show(c, t, 28.9, 180, 960, MM("comida", 56, GREEN), anim="up")
            show(c, t, 29.1, 520, 840, sc(cart, PINKISH, s=0.8), anim="pop")
            show(c, t, 29.5, 520, 960, MM("limpeza", 56, RED), anim="up")
            show(c, t, 30.9, 180, 1040, HL("VA", 56, LGREEN, GREEN), anim="stamp")
            for k, (t0, s) in enumerate(((36.0, "sabão"), (36.7, "papel higiênico"), (37.6, "xampu"))):
                show(c, t, t0, 520, 1030 + k * 60, T(s, 46, DGRAY), anim="up")
            if t > 38.2:
                show(c, t, 38.2, 520, 860, sc(big_x, 80), anim="stamp")
                show(c, t, 38.4, CX, 1230, HL("NÃO ENTRA NO VALE", 58, PINKISH, RED), anim="stamp")
        else:
            show(c, t, 39.4, 170, 880, sc(dollar_bill, s=0.9), anim="pop")
            show(c, t, 39.7, 290, 850, L("paga com o salário", 46, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 41.3, 290, 925, L("numa compra separada", 50, DGRAY), anim="left", d=0.3)
            show(c, t, 42.5, CX, 1090, HL("SEM SUSTO NO CAIXA", 56, LGREEN, GREEN), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (28.5, "present_l"), (38.2, "head"), (39.4, "point_l"), (42.5, "thumb")],
             [(0, "confident"), (33.1, "think"), (38.2, "shocked"), (39.4, "confident"), (42.5, "happy")], look=-0.8)
    elif t < 64.0:  # 3
        if t < 55.6:
            show(c, t, 47.6, 80, 830, L("R$ 600", 76, INK, MARKER), anim="left", d=0.3)
            show(c, t, 48.4, 370, 830, L("- R$ 250", 76, RED, MARKER), anim="left", d=0.3)
            show(c, t, 50.1, 80, 940, L("= R$ 350", 80, NAVY, MARKER), anim="stamp", d=0.3)
            show(c, t, 52.3, 460, 940, L("÷ 4", 80, NAVY, MARKER), anim="stamp", d=0.3)
            show(c, t, 53.8, CX, 1120, HL("~R$ 87 POR SEMANA", 74, LYELLOW, INK), anim="stamp")
        elif t < 58.4:
            for k, (t0, s) in enumerate(((55.8, "fruta"), (56.5, "verdura"), (57.3, "carne"), (57.8, "pão"))):
                x, y = 90 + (k % 2) * 320, 860 + (k // 2) * 110
                show(c, t, t0, x, y, L("+ " + s, 66, GREEN, MARKER), anim="left", d=0.3)
            show(c, t, 55.6, CX, 1150, MM("R$ 87 por semana", 62, NAVY), anim="fade")
        else:
            show(c, t, 58.4, 160, 880, sc(calendar, "SEG", BLUE, 48, s=1.0), anim="pop")
            show(c, t, 59.3, 360, 880, sc(phone, s=0.8), anim="pop")
            show(c, t, 59.8, 460, 860, L("olha o saldo", 54, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 61.1, 70, 1070, L("passou numa semana?", 54, DGRAY), anim="left", d=0.3)
            show(c, t, 62.5, CX, 1170, HL("a próxima é menor", 62, PINKISH, RED), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "finger_up"), (47.6, "present_l"), (53.8, "arms_up"), (55.6, "point_l"), (58.4, "finger_up")],
             [(0, "think"), (53.8, "grin"), (55.6, "happy"), (61.1, "confident")], look=-0.8)
    elif t < 71.8:  # conclusão
        show(c, t, 64.1, 60, 820, L("gasta tudo na 1ª semana", 52, DGRAY), anim="left", d=0.3)
        show(c, t, 65.8, CX, 920, HL("come do salário", 66, PINKISH, RED), anim="stamp")
        show(c, t, 67.8, 60, 1060, L("divide", 60, DGRAY, MARKER), anim="left", d=0.3)
        show(c, t, 68.6, 330, 1060, sc(calendar, "30", GREEN, 60, s=0.8), anim="pop")
        show(c, t, 69.8, CX, 1200, HL("vale ainda pagando", 62, LGREEN, GREEN), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "shrug"), (67.8, "thumb")], [(0, "worried"), (67.8, "happy")], look=-0.8)
    else:  # fim
        show(c, t, 71.8, 370, 830, MM("QUANTO DÁ O SEU", 70, NAVY), anim="stamp")
        show(c, t, 72.4, 370, 940, MM("VALE POR SEMANA?", 70, RED), anim="stamp")
        show(c, t, 73.5, 190, 1110, sc(phone, s=1.0), anim="pop")
        show(c, t, 74.1, 470, 1110, HL("COMENTA AÍ", 76, LYELLOW), anim="stamp")
        hero(c, t, 880, FY, 0.9, [(0, "point_l")], [(0, "happy"), (74.2, "grin")], look=-0.8)


def cena(c, t):
    floor(c)
    lista(c, t)
    marcador(c, t)
    palco(c, t)


SCENES = [(0, 999.0, cena)]
