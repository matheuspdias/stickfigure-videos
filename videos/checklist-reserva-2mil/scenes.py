"""CHECKLIST DO CONSULTOR: "3 passos pra montar a reserva com salário de R$ 2 mil". Só TikTok: vertical 1080x1920, ~74 s, ESTILO CADERNO.
Modelo: videos/checklist-sair-do-rotativo/. Contas (contas.py): gastos essenciais R$ 1.500 -> 1ª meta 1 mês (R$ 1.500), depois 3 meses (R$ 4.500);
Pix de R$ 100 (5% de R$ 2.000) no dia do salário + R$ 500 da 2ª parcela do 13º (~R$ 844 com salário de R$ 2 mil) -> R$ 1.500 em 10 meses;
rotativo ~15%/mês: R$ 1.500 -> ~R$ 1.725 em 1 mês.
Layout: lista de 3 passos (y 280-500), marcador da reserva (y ~610), palco y 700-1280 (pés em 1280), legendas ~1400-1460, nada em x > 930.
Quadro 0: notificação do salário contando R$ 0 -> R$ 2.000 e a reserva em R$ 0."""
from engine import *  # noqa

VERTICAL = True

CX = 400
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(5.5, "tum"), (11.4, "tum"), (26.9, "tum"), (49.8, "tum"), (73.1, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(11.4, "descobre o seu número", 26.8), (26.9, "paga você primeiro", 49.7), (49.8, "define a emergência", 70.3)]
LIN0, LINH = 325, 82


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


def fmt(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def reais(c, t, t0, a, b, x, y, size, col, d=0.8, pre="R$ ", suf="", align="c"):
    v = a + (b - a) * ease_out(prog(t, t0, d))
    s = f"{v:,.0f}".replace(",", ".")
    text(c, m(pre + s + suf), x, y, size, MARKER, col, align=align)


def lista(c, t):
    show(c, t, -1.0, 540, 205, lambda c: ribbon(c, "RESERVA COM R$ 2 MIL", NAVY, 54), anim="stamp", d=0.3)
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = LIN0 + i * LINH
        if t0 - 0.6 <= t < t1:
            rrect(c, 70, y - 38, 880, 76, 14); fs(c, LYELLOW, 0)
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


# ======================================================================= MARCADOR DA RESERVA (valor que atravessa o vídeo)
SALDO = [(31.7, 0, 100, 0.6), (43.0, 100, 600, 0.8), (45.9, 600, 1500, 3.0)]
SELOS = [(31.7, 37.0, "+R$ 100"), (43.0, 45.9, "+R$ 500"), (45.9, 49.0, "+100/mês")]


def marcador(c, t):
    ouro = t >= 48.9
    rrect(c, 60, 560, 880, 104, 22); fs(c, (1, 0.97, 0.85) if ouro else WHITE, 5)
    c.save(); c.translate(130, 612); c.scale(0.42, 0.42); piggy(c); c.restore()
    text(c, "reserva", 190, 626, 44, HAND, DGRAY, align="l")
    v = 0
    for t0, a, b, d in SALDO:
        if t >= t0:
            v = a + (b - a) * ease_out(prog(t, t0, d))
    text(c, m(fmt(v)), 340, 640, 68, MARKER, GOLD if ouro else (GREEN if v > 0 else RED), align="l")
    if t >= 23.9 and not ouro:
        text(c, m("/ R$ 1.500"), 890, 630, 40, MARKER, GRAY, align="r")
    if ouro:
        show(c, t, 48.9, 830, 625, HL("10 MESES", 38, LYELLOW), anim="stamp")
    for t0, t1, s in SELOS:
        if t0 <= t < t1:
            show(c, t, t0, 820, 548, HL(s, 34, LGREEN, GREEN), anim="pop", d=0.3)


# ======================================================================= PALCO (y 720-1280)
def palco(c, t):
    if t < 11.4:  # gancho
        if t < 3.9:
            show(c, t, -1.0, 150, 860, sc(phone, s=0.9), anim="pop")
            text(c, "salário caiu!", 260, 800, 52, HAND, DGRAY, align="l")
            reais(c, t, -0.4, 0, 2000, 260, 905, 100, INK, d=1.4, align="l")
            show(c, t, 1.9, 420, 1060, HL("guardado: R$ 0", 66, PINKISH, RED), anim="stamp")
        elif t < 6.8:
            show(c, t, 3.9, 190, 1000, sc(fridge, s=1.0), anim="drop")
            show(c, t, 4.4, 300, 820, sc(exclaim, 90), anim="pop")
            if t >= 5.5:
                arrow_draw(c, t, 5.5, 300, 1000, 470, 1000, d=0.4)
            show(c, t, 5.6, 590, 990, sc(card, RED, s=1.3), anim="pop")
            show(c, t, 5.9, 420, 1220, MM("vai pro cartão", 62, RED), anim="up")
        else:
            show(c, t, 6.8, CX, 830, HL("3 PASSOS", 90, LYELLOW), anim="stamp")
            show(c, t, 7.9, CX, 950, MM("pra sua reserva", 64, NAVY), anim="up")
            show(c, t, 9.4, 200, 1130, sc(calendar, "5", NAVY, 56, s=1.0), anim="pop")
            show(c, t, 9.6, 320, 1120, L("salva pro dia", 56, DGRAY), anim="left", d=0.3)
            show(c, t, 9.9, 320, 1190, L("do salário", 56, DGRAY), anim="left", d=0.3)
        hero(c, t, 860, FY, 0.9, [(0, "head"), (3.9, "shrug"), (6.8, "finger_up")], [(0, "worried"), (3.9, "shocked"), (6.8, "confident")], look=-0.6)
    elif t < 26.9:  # 1
        if t < 16.5:
            show(c, t, 12.2, CX, 790, T("o seu número", 58, DGRAY), anim="up")
            show(c, t, 13.6, CX, 920, MM("R$ 2.000", 100, GRAY), anim="fade")
            if t > 14.0:
                show(c, t, 14.0, CX, 905, strike(440), anim="fade", d=0.2)
            show(c, t, 14.9, CX, 1030, MM("é o que você não", 56, NAVY), anim="up")
            show(c, t, 15.4, CX, 1130, HL("CONSEGUE CORTAR", 62, LYELLOW), anim="stamp")
        elif t < 22.0:
            for k, (t0, nome, ic) in enumerate(((16.6, "aluguel", lambda c: house(c)), (17.5, "contas", lambda c: boleto(c, "LUZ", ORANGE)),
                                                (18.3, "mercado", lambda c: cart(c)), (19.1, "transporte", lambda c: car(c, BLUE)))):
                x, y = 130 + (k % 2) * 340, 800 + (k // 2) * 170
                show(c, t, t0, x - 60, y + 10, sc(ic, s=0.32), anim="pop")
                show(c, t, t0 + 0.1, x + 10, y + 25, L(nome, 46, NAVY, MARKER), anim="left", d=0.3)
            if t >= 20.0:
                reais(c, t, 20.3, 0, 1500, CX, 1180, 96, NAVY, d=0.9, pre="= R$ ", suf="")
        else:
            show(c, t, 22.0, CX, 800, T("1ª meta: 1 mês", 60, DGRAY), anim="up")
            show(c, t, 23.9, CX, 930, HL("R$ 1.500", 110, LGREEN, GREEN), anim="stamp")
            show(c, t, 25.1, CX, 1090, T("depois: 3 meses", 54, DGRAY), anim="up")
            show(c, t, 25.8, CX, 1180, MM("R$ 4.500", 70, NAVY), anim="up")
        hero(c, t, 860, FY, 0.9, [(0, "finger_up"), (16.6, "present_l"), (22.0, "point_l")], [(0, "think"), (14.0, "confident"), (23.9, "happy")], look=-0.8)
    elif t < 49.8:  # 2
        if t < 39.9:
            show(c, t, 27.8, CX, 790, HL("PAGA VOCÊ PRIMEIRO", 54, LYELLOW), anim="stamp")
            show(c, t, 29.3, 140, 935, sc(calendar, "5", NAVY, 52, s=0.9), anim="pop")
            show(c, t, 30.7, 300, 930, sc(pix_tag, "PIX", GREEN, 50), anim="pop")
            show(c, t, 31.7, 400, 960, L("R$ 100", 84, GREEN, MARKER), anim="stamp", d=0.3)
            show(c, t, 32.7, CX, 1060, MM("conta separada", 60, NAVY), anim="up")
            show(c, t, 33.9, CX, 1130, T("100% do CDI · saca na hora", 48, DGRAY), anim="up")
            show(c, t, 37.0, CX, 1220, HL("só 5% do salário", 58, LGREEN), anim="stamp")
        else:
            show(c, t, 40.1, CX, 790, MM("2ª parcela do 13º", 60, NAVY), anim="up")
            show(c, t, 42.7, CX, 895, HL("+R$ 500", 84, LGREEN, GREEN), anim="stamp")
            show(c, t, 44.6, CX, 1000, MM("R$ 500 + R$ 100/mês", 56, INK), anim="up")
            if t > 45.9:
                for k in range(10):
                    t0 = 45.9 + k * 0.3
                    if t > t0:
                        v = 600 + 100 * k
                        h = v * 0.085 * ease_out(prog(t, t0, 0.25))
                        rrect(c, 110 + k * 58, 1240 - h, 42, h, 6); fs(c, LGREEN if k < 9 else GREEN, 4)
                line(c, 90, 1240, 700, 1240, 5)
            if t > 47.2:
                show(c, t, 47.2, CX, 1080, HL("10 MESES", 56, LYELLOW), anim="stamp")
        hero(c, t, 860, FY, 0.9, [(0, "finger_up"), (29.3, "present_l"), (37.0, "thumb"), (40.1, "point_l"), (48.9, "arms_up")],
             [(0, "confident"), (37.0, "happy"), (48.9, "grin")], look=-0.8)
    elif t < 70.4:  # 3
        if t < 61.3:
            show(c, t, 50.8, CX, 790, HL("O QUE É EMERGÊNCIA", 60, LYELLOW), anim="stamp")
            for k, (t0, s) in enumerate(((52.6, "saúde"), (53.4, "demissão"), (54.3, "conserto pra trabalhar"))):
                y = 885 + k * 72
                show(c, t, t0, 110, y, sc(check_icon, 26), anim="pop")
                show(c, t, t0, 160, y + 18, L(s, 48, NAVY, MARKER), anim="left", d=0.3)
            if t >= 56.5:
                show(c, t, 56.5, 110, 1101, sc(x_icon, 26), anim="pop")
                show(c, t, 56.5, 160, 1119, L("promoção", 48, RED, MARKER), anim="left", d=0.3)
            show(c, t, 58.2, CX, 1215, HL("usou? repõe primeiro", 58, PINKISH, RED), anim="stamp")
        else:
            show(c, t, 61.5, CX, 790, T("R$ 1.500 em 1 mês", 58, DGRAY), anim="up")
            base, scl = 1180, 0.15
            for t0, x, v, lab, top, col in ((64.0, 220, 1725, "no rotativo", "~R$ 1.725", RED), (68.0, 580, 1515, "na reserva", "rende", GREEN)):
                if t > t0:
                    h = v * scl * ease_out(prog(t, t0, 0.6))
                    rrect(c, x - 95, base - h, 190, h, 12); fs(c, PINKISH if col == RED else LGREEN, 6)
                    show(c, t, t0 + 0.5, x, base - v * scl - 30, MM(top, 58, col), anim="pop")
                    show(c, t, t0 + 0.2, x, base + 50, T(lab, 46, DGRAY), anim="up")
            line(c, 100, base, 720, base, 6)
        hero(c, t, 860, FY, 0.9, [(0, "finger_up"), (52.6, "present_l"), (56.5, "hips"), (61.3, "point_l"), (68.0, "thumb")],
             [(0, "confident"), (56.5, "angry"), (61.3, "worried"), (68.0, "happy")], look=-0.8)
    else:  # fim
        show(c, t, 70.5, 380, 820, MM("QUANTO VOCÊ SEPARA", 58, NAVY), anim="stamp")
        show(c, t, 71.3, 380, 920, MM("NO DIA DO SALÁRIO?", 60, RED), anim="stamp")
        show(c, t, 72.4, 170, 1100, sc(phone, s=0.9), anim="pop")
        show(c, t, 73.1, 460, 1100, HL("COMENTA AÍ", 74, LYELLOW), anim="stamp")
        hero(c, t, 860, FY, 0.9, [(0, "point_l")], [(0, "happy"), (73.1, "grin")], look=-0.8)


def cena(c, t):
    floor(c)
    lista(c, t)
    marcador(c, t)
    palco(c, t)


SCENES = [(0, 999.0, cena)]
