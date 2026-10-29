"""O que ninguém te conta antes de pegar um empréstimo consignado (série ep. 3). Só TikTok: vertical nativo 1080x1920, 151,6 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout igual ao de planta-mcmv e financiar-carro: coordenadas desenhadas com pés em y=1230 e deslocadas +60 (SHIFT).
Contas em contas.py: R$ 5 mil em 24x a 3,79% a.m. (média BCB do consignado CLT, ago/2026)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
LORANGE = (1.0, 0.86, 0.70)

SFX = [(40.1, "tum"), (56.9, "tum"), (84.8, "tum"), (145.7, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers (mesmos do ep. 2)
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def block(lab, col, w=520, h=86, size=44):
    def f(c):
        rrect(c, -w / 2, -h / 2, w, h, 12); fs(c, col, 5)
        text(c, lab, 0, 0, size, MARKER, INK)
    return f


def notif(c):
    """notificação de app: 'consignado liberado'"""
    rrect(c, -230, -80, 460, 160, 26); fs(c, WHITE, 6)
    rrect(c, -205, -50, 70, 70, 16); fs(c, GREEN, 4)
    text(c, "$", -170, -14, 54, MARKER, WHITE)
    text(c, "CONSIGNADO", -115, -32, 40, MARKER, NAVY, align="l")
    text(c, "LIBERADO!", -115, 18, 40, MARKER, GREEN, align="l")
    text(c, "toque para aceitar", 0, 58, 30, HAND, DGRAY)


def big_phone(c, t, t0, x, y, s=2.1):
    c.save(); c.translate(x, y); c.scale(s, s); phone(c, NAVY); c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.6  gancho
    floor(c)
    show(c, t, 0.0, CX, 250, lambda c: hl(c, "CONSIGNADO", 0, 0, 96, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 0.0, CX, 380, lambda c: hl(c, "LIBERADO?", 0, 0, 96, LYELLOW, rot=0.015), anim="stamp", d=0.3)
    show(c, t, 0.1, 330, 760, lambda c: (c.save(), c.scale(1.8, 1.8), phone(c, NAVY), c.restore()), anim="pop")
    show(c, t, 0.9, 400, 600, notif, anim="drop")
    show(c, t, 3.4, 400, 1070, stamp_txt("ANTES DE ACEITAR", RED, 54), anim="stamp")
    show(c, t, 4.6, 400, 1180, M("saiba disso", 60, NAVY), anim="up")
    hero(c, t, 900, FY, 0.5, [(0, "point_l"), (3.4, "finger_up")], [(0, "happy"), (3.4, "worried")], look=-1)


def s02(c, t):  # 6.6 - 15.8  o que é
    floor(c)
    show(c, t, 6.8, CX, 240, lambda c: ribbon(c, "O QUE É", NAVY, 64), anim="stamp")
    show(c, t, 8.4, 230, 520, sc(bills, 3, s=1.2), anim="pop")
    show(c, t, 8.6, 230, 660, M("salário", 52, GREEN), anim="up")
    show(c, t, 9.2, 700, 470, sc(bank, s=0.7), anim="drop")
    if t > 9.4:
        arrow_draw(c, t, 9.4, 340, 500, 590, 450, col=RED)
    show(c, t, 9.8, 470, 400, M("parcela", 46, RED), anim="pop")
    show(c, t, 10.9, 700, 760, block("sua conta", LBLUE, 300, 86, 46), anim="pop")
    if t > 11.1:
        arrow_draw(c, t, 11.1, 330, 640, 540, 740, col=GREEN)
    show(c, t, 11.6, 520, 840, M("o que sobra", 44, DGRAY), anim="up")
    show(c, t, 12.5, CX, 980, M("você não escolhe pagar", 54, INK), anim="up")
    show(c, t, 14.4, CX, 1110, stamp_txt("JÁ VEM DESCONTADO", RED, 54), anim="stamp")
    hero(c, t, 940, FY, 0.4, [(0, "present_l"), (12.5, "head")], [(0, "neutral"), (12.5, "worried")], look=-1)


def s03(c, t):  # 15.8 - 31.6  juro menor, mas não barato
    floor(c)
    show(c, t, 16.0, CX, 240, lambda c: hl(c, "POR QUE O JURO É MENOR?", 0, 0, 56, LYELLOW), anim="stamp")
    show(c, t, 17.7, 260, 470, sc(bank, s=0.6), anim="drop", t1=20.4)
    show(c, t, 18.5, 640, 430, M("risco de calote:", 46, NAVY), anim="up", t1=20.4)
    show(c, t, 19.6, 640, 510, stamp_txt("PEQUENO", GREEN, 50), anim="stamp", t1=20.4)
    base, px, bw = 1000, 75, 220
    bars = [(300, 20.8, 3.79, NAVY, "~3,8%", "consignado CLT", 22.0),
            (680, 26.1, 6.39, RED, "+ de 6%", "pessoal comum", 26.6)]
    if t > 20.6:
        show(c, t, 20.6, CX, 360, M("taxa média ao mês (BC)", 48, NAVY), anim="up")
    for x, t0, v, col, lab, nome, tl in bars:
        if t > t0:
            k = ease_out(prog(t, t0, 0.6))
            h = v * px * k
            rrect(c, x - bw / 2, base - h, bw, h, 10); fs(c, col, 6)
            show(c, t, t0 + 0.1, x, base + 50, T(nome, 42), anim="up")
        show(c, t, tl, x, base - v * px - 50, M(lab, 62, col), anim="stamp")
    if t > 20.8:
        line(c, 150, base, 830, base, 6)
    show(c, t, 29.2, 290, 1150, M("menor", 60, GREEN), anim="pop")
    show(c, t, 29.9, 450, 1150, lambda c: neq(c, 40, RED, 11), anim="pop")
    show(c, t, 30.9, 640, 1150, M("barato", 60, RED), anim="stamp")
    hero(c, t, 960, FY, 0.36, [(0, "think"), (20.8, "point_l"), (29.2, "finger_up")],
         [(0, "think"), (20.8, "neutral"), (29.2, "confident")], look=-1)


def s04(c, t):  # 31.6 - 46.4  o exemplo
    floor(c)
    show(c, t, 31.8, CX, 240, lambda c: ribbon(c, "UM EXEMPLO", NAVY, 60), anim="stamp")
    rows = [(31.9, "você pega", "R$ 5.000", NAVY),
            (33.0, "prazo", "24x", NAVY),
            (34.3, "taxa média", "3,79% a.m.", RED)]
    for i, (t0, lab, val, col) in enumerate(rows):
        y = 380 + i * 90
        show(c, t, t0, 110, y, L(lab, 48), anim="left", d=0.3)
        show(c, t, t0 + 0.2, 800, y, lambda c, v=val, col=col: text(c, v, 0, 0, 54, MARKER, col, align="r"), anim="pop")
    show(c, t, 35.4, CX, 680, lambda c: hl(c, "parcela: ~R$ 321", 0, 0, 62, LYELLOW), anim="stamp", t1=38.0)
    show(c, t, 38.0, CX, 640, M("No fim, você pagou:", 54, NAVY), anim="up")
    show(c, t, 40.1, CX, 760, lambda c: hl(c, "R$ 7.700", 0, 0, 120, LYELLOW), anim="stamp")
    PXB, x0 = 0.095, 110
    if t > 41.2:
        k = ease_out(prog(t, 41.2, 0.6))
        w1 = 5000 * PXB * k
        rrect(c, x0, 950, w1, 100, 10); fs(c, NAVY, 6)
        show(c, t, 41.4, x0 + 5000 * PXB / 2, 1000, M("5.000", 50, WHITE), anim="pop")
    if t > 42.2:
        k = ease_out(prog(t, 42.2, 0.6))
        w2 = 2700 * PXB * k
        xs = x0 + 5000 * PXB
        rrect(c, xs, 950, w2, 100, 10); fs(c, RED, 6)
        show(c, t, 42.5, xs + 2700 * PXB / 2, 1000, M("2.700", 46, WHITE), anim="pop")
        show(c, t, 43.4, xs + 2700 * PXB / 2, 1095, T("de juros", 42, RED), anim="up")
    show(c, t, 44.4, 330, 1150, stamp_txt("MAIS DA METADE", RED, 48), anim="stamp")
    hero(c, t, 960, FY, 0.36, [(0, "present_l"), (40.1, "head")], [(0, "neutral"), (40.1, "shocked")],
         prop=("r", prop_calculator), look=-1)


def s05(c, t):  # 46.4 - 66.9  margem consignável
    floor(c)
    show(c, t, 46.6, CX, 240, lambda c: ribbon(c, "MARGEM CONSIGNÁVEL", NAVY, 54), anim="stamp")
    show(c, t, 49.2, CX, 350, M("o limite do salário pra parcelas", 44, DGRAY), anim="up")
    show(c, t, 52.0, CX, 450, lambda c: hl(c, "até 35%", 0, 0, 90, LYELLOW), anim="stamp")
    # barra do salário de 2.500 (horizontal)
    X0, W, Y, H = 110, 800, 640, 130
    if t > 54.2:
        k = ease_out(prog(t, 54.2, 0.5))
        rrect(c, X0, Y, W * k, H, 14); fs(c, LGREEN, 6)
        show(c, t, 54.4, X0 + W / 2, Y - 40, M("salário de R$ 2.500 na mão", 44, NAVY), anim="up")
    if t > 56.5:
        k = ease_out(prog(t, 56.5, 0.5))
        rrect(c, X0, Y, W * 0.35 * k, H, 14); fs(c, RED, 6)
        show(c, t, 56.9, X0 + W * 0.175, Y + H / 2, M("R$ 875", 52, WHITE), anim="stamp")
        show(c, t, 59.6, X0 + W * 0.175, Y + H + 50, T("sai antes", 40, RED), anim="up")
        show(c, t, 60.2, X0 + W * 0.175, Y + H + 95, T("de você ver", 40, RED), anim="up")
    show(c, t, 62.1, X0 + W * 0.675, Y + H / 2, M("R$ 1.625", 52, GREEN), anim="stamp")
    show(c, t, 62.6, X0 + W * 0.675, Y + H + 50, T("sobra pro resto", 40, GREEN), anim="up")
    items = [(64.4, "aluguel", lambda c: house(c)), (65.2, "comida", sandwich), (65.9, "todo o resto", lambda c: boleto(c, "CONTAS", NAVY))]
    for i, (t0, lab, ic) in enumerate(items):
        x = 230 + i * 270
        show(c, t, t0, x, 1030, group(sc(ic, s=0.5), at(0, 110, T(lab, 38))), anim="drop")
    hero(c, t, 980, FY, 0.32, [(0, "present_l"), (56.9, "head"), (64.4, "think")],
         [(0, "neutral"), (56.9, "shocked"), (64.4, "worried")], look=-1)


def s06(c, t):  # 66.9 - 90.1  garantia do FGTS
    floor(c)
    show(c, t, 67.1, CX, 240, lambda c: ribbon(c, "E O FGTS?", RED, 64), anim="stamp")
    show(c, t, 68.2, 230, 480, sc(piggy, GOLD, s=0.95), anim="pop")
    show(c, t, 68.4, 230, 600, M("FGTS", 54, NAVY), anim="up")
    show(c, t, 72.2, 640, 400, M("como garantia:", 48, NAVY), anim="up")
    show(c, t, 73.2, 640, 490, lambda c: hl(c, "até 10% do saldo", 0, 0, 50, LYELLOW), anim="stamp")
    show(c, t, 76.1, 640, 590, lambda c: hl(c, "+ até 100% da multa", 0, 0, 50, PINKISH), anim="stamp")
    show(c, t, 77.3, 640, 650, T("rescisória (os 40%)", 38, DGRAY), anim="up")
    show(c, t, 78.6, 190, 770, M("em troca:", 46, GREEN), anim="up")
    show(c, t, 80.0, 610, 770, lambda c: hl(c, "teto de 1,99% a.m.", 0, 0, 50, LGREEN), anim="stamp")
    show(c, t, 81.5, 330, 920, stamp_txt("DEMITIDO DEVENDO?", RED, 46), anim="stamp")
    show(c, t, 84.8, 720, 950, sc(padlock, GOLD, s=0.8), anim="stamp")
    show(c, t, 85.0, 720, 1080, M("bloqueado", 48, RED), anim="up")
    show(c, t, 85.6, 720, 1140, T("pra quitar a dívida", 38, RED), anim="up")
    show(c, t, 86.9, 330, 1060, T("o dinheiro que", 42, NAVY), anim="up")
    show(c, t, 87.4, 330, 1115, T("te seguraria", 42, NAVY), anim="up")
    show(c, t, 88.6, 330, 1170, T("sem emprego", 42, NAVY), anim="up")
    hero(c, t, 965, FY, 0.32, [(0, "point_l"), (78.6, "thumb"), (81.5, "head")],
         [(0, "neutral"), (78.6, "happy"), (81.5, "shocked")], look=-1)


def s07(c, t):  # 90.1 - 108.1  demissão ou troca de emprego
    floor(c)
    show(c, t, 90.3, CX, 240, M("demitido ou mudou de emprego?", 52, NAVY), anim="up")
    show(c, t, 93.2, CX, 360, stamp_txt("A DÍVIDA NÃO SOME", RED, 60), anim="stamp")
    show(c, t, 95.1, 220, 600, sc(document, "RESCISÃO", NAVY, 24, s=1.1), anim="drop")
    show(c, t, 96.0, 360, 520, L("- parcela do mês", 46, RED, MARKER), anim="left")
    show(c, t, 99.1, 220, 880, sc(boleto, "BOLETO", RED, s=0.7), anim="drop")
    show(c, t, 99.3, 360, 810, L("o que sobrar:", 44, INK, MARKER), anim="left")
    show(c, t, 100.5, 360, 870, L("boleto", 46, RED), anim="left")
    show(c, t, 101.4, 360, 930, L("ou negocia com o banco", 44, DGRAY), anim="left")
    show(c, t, 103.0, 360, 1010, L("novo emprego com carteira?", 42, INK, MARKER), anim="left")
    show(c, t, 104.3, 220, 1110, sc(document, "CARTEIRA", BLUE, 24, s=0.7), anim="pop")
    show(c, t, 105.1, 360, 1080, L("o desconto volta", 46, NAVY, MARKER), anim="left")
    show(c, t, 106.5, 360, 1140, L("no novo salário", 46, NAVY), anim="left")
    hero(c, t, 950, FY, 0.36, [(0, "think"), (93.2, "head"), (99.1, "present_l")],
         [(0, "think"), (93.2, "worried"), (99.1, "neutral")], look=-1)


def s08(c, t):  # 108.1 - 125.8  golpes
    floor(c)
    show(c, t, 108.3, CX, 240, lambda c: ribbon(c, "CUIDADO: GOLPE", RED, 62), anim="stamp")
    show(c, t, 109.9, 230, 560, lambda c: (c.save(), c.scale(1.5, 1.5), phone(c, RED), c.restore()), anim="pop")
    if 110.0 < t < 117.0:
        for i in range(3):
            ph = (t * 3 + i * 0.33) % 1.0
            c.save(); c.translate(230, 560)
            c.new_sub_path(); c.arc(0, 0, 200 + ph * 60, -0.6, 0.6)
            rgb(c, RED, 1 - ph); c.set_line_width(6); c.stroke(); c.restore()
    show(c, t, 111.4, 620, 420, group(lambda c: speech(c, 400, 110, -150, 90), T("consignado liberado!", 40)), anim="pop")
    show(c, t, 112.9, 640, 590, lambda c: hl(c, "seus dados?", 0, 0, 50, PINKISH), anim="stamp")
    show(c, t, 114.5, 640, 690, lambda c: hl(c, "depósito antes?", 0, 0, 50, PINKISH), anim="stamp")
    show(c, t, 117.0, CX, 860, stamp_txt("BANCO NÃO PEDE", RED, 52), anim="stamp")
    show(c, t, 118.1, CX, 950, M("pagamento pra liberar", 46, RED), anim="up")
    show(c, t, 120.4, 140, 1060, sc(check_icon, s=0.5), anim="stamp")
    show(c, t, 121.1, 195, 1060, L("entre você mesmo:", 44, INK, MARKER), anim="left")
    show(c, t, 122.7, 195, 1125, L("app Carteira de Trabalho Digital", 40, NAVY), anim="left")
    show(c, t, 124.7, 195, 1185, L("ou app do seu banco", 40, NAVY), anim="left")
    hero(c, t, 965, FY - 120, 0.3, [(0, "head"), (117.0, "finger_up")], [(0, "shocked"), (117.0, "confident")], look=-1)


def s09(c, t):  # 125.8 - 147.0  checklist
    floor(c)
    show(c, t, 126.0, CX, 250, lambda c: ribbon(c, "ANTES DE ACEITAR", NAVY, 58), anim="stamp")
    items = [(127.4, "compare pelo CET", True),
             (130.9, "simule em mais de um lugar", True),
             (133.0, "some ao orçamento real", True),
             (135.8, "troque dívida cara", True),
             (139.8, "não pra consumo", False)]
    for i, (t0, s, ok) in enumerate(items):
        y = 400 + i * 115
        show(c, t, t0, 140, y, lambda c: (rrect(c, -34, -34, 68, 68, 10), fs(c, WHITE, 6)), anim="pop")
        show(c, t, t0 + 0.5, 140, y, sc(check_icon if ok else x_icon, s=0.6), anim="stamp")
        show(c, t, t0, 200, y, L(s, 50, INK if ok else RED), anim="left", d=0.3)
    show(c, t, 137.8, 600, 745, L("(cartão, cheque especial)", 34, DGRAY), anim="up")
    show(c, t, 141.3, 230, 1090, sc(bank, s=0.4), anim="pop")
    show(c, t, 143.5, 620, 1090, sc(bank, s=0.4), anim="pop")
    if t > 142.5:
        arrow_draw(c, t, 142.5, 330, 1060, 520, 1060, col=GREEN)
    show(c, t, 144.6, 425, 990, T("juro menor", 38, GREEN), anim="up")
    show(c, t, 145.7, 425, 1190, lambda c: hl(c, "PORTABILIDADE", 0, 0, 52, LGREEN), anim="stamp")
    hero(c, t, 960, FY, 0.36, [(0, "present_l"), (145.7, "thumb")], [(0, "confident"), (145.7, "grin")],
         prop=("l", prop_pointer), look=-1)


def s10(c, t):  # 147.0 - fim  pergunta final
    floor(c)
    show(c, t, 147.1, CX, 280, M("Já pegou consignado?", 76, NAVY), anim="stamp")
    show(c, t, 148.9, CX, 420, T("te ajudou", 62, GREEN), anim="up")
    show(c, t, 149.6, CX, 500, T("ou te apertou?", 62, RED), anim="up")
    show(c, t, 147.4, 260, FY - 120, lambda c: (c.save(), c.scale(1.3, 1.3), phone(c, NAVY), c.restore()), anim="pop")
    show(c, t, 150.7, 690, 720, group(lambda c: speech(c, 460, 130, -140, 110), T("Comenta aí!", 62)), anim="pop")
    hero(c, t, 720, FY, 0.7, [(0, "point_l"), (150.7, "wave")], [(0, "happy"), (150.7, "grin")], look=-0.5)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 6.6, s01), (6.6, 15.8, s02), (15.8, 31.6, s03), (31.6, 46.4, s04), (46.4, 66.9, s05),
    (66.9, 90.1, s06), (90.1, 108.1, s07), (108.1, 125.8, s08), (125.8, 147.0, s09),
    (147.0, 999.0, s10),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
