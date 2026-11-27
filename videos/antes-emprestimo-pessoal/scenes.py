"""O QUE NINGUÉM TE CONTA ANTES DE PEGAR EMPRÉSTIMO PESSOAL (série, ep. 7). Só TikTok: vertical 1080x1920, ~103 s, ESTILO CADERNO.
Contas e fontes (contas.py): BC set/2026 crédito pessoal não consignado 6,42% a.m. = 110,94% a.a.; Procon-SP nov/2026 taxa máxima
não preferencial 6,29% a 9,99% a.m.; R$ 5.000 em 12x a 6,5% a.m. = parcela ~R$ 613, total ~R$ 7.354, juros ~R$ 2.354;
ranking BC 05-11/11/2026: 1º quartil 39,7% a.a., 3º quartil 265,8% a.a.; consignado INSS 23,9%, CLT 47,7%; cheque especial 144%, rotativo 451,7%.
Layout: título y~250, palco 360-1290 (pés em 1280), legendas ~1400-1460, nada em x > 930.
Quadro 0: o app já mostrando o valor aprovado contando de R$ 0 a R$ 5.000."""
from engine import *  # noqa

VERTICAL = True

CX = 420
FY = 1280
PINKISH = (1, 0.8, 0.76)

SFX = [(4.2, "tum"), (12.5, "tum"), (33.4, "tum"), (45.2, "tum"), (65.7, "tum"), (101.9, "soft_ding")]
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


def reais(c, t, t0, a, b, x, y, size, col, d=0.8, pre="R$ ", suf="", align="c"):
    v = a + (b - a) * ease_out(prog(t, t0, d))
    s = f"{v:,.0f}".replace(",", ".")
    text(c, m(pre + s + suf), x, y, size, MARKER, col, align=align)


def titulo(c, t, s, t0=-1.0):
    show(c, t, t0, 540, 250, lambda c: ribbon(c, s, NAVY, 54), anim="stamp", d=0.3)


def gbar(c, t, t0, x, y, h, col, label, top, w=150, size=46):
    if t < t0:
        return
    k = ease_out(prog(t, t0, 0.8))
    c.save(); c.translate(x, y)
    bar(c, h * k, w, col, label, top if k > 0.95 else None, size)
    c.restore()


def selo_ep(c, t):
    if 4.2 <= t < 6.9:
        show(c, t, 4.2, 400, 1190, HL("SÉRIE: O QUE NINGUÉM TE CONTA - EP. 7", 34, LYELLOW), anim="stamp")


def palco(c, t):
    floor(c)
    if t < 7.0:  # gancho
        titulo(c, t, "EMPRÉSTIMO PESSOAL")
        show(c, t, -1.0, 200, 580, sc(phone, s=1.5), anim="pop")
        text(c, "aprovado!", 470, 470, 54, HAND, GREEN, align="l")
        reais(c, t, -0.6, 0, 5000, 470, 580, 96, NAVY, d=2.2, align="l")
        show(c, t, 1.3, 470, 670, L("na hora", 60, GREEN, MARKER), anim="left", d=0.3)
        show(c, t, 3.5, CX, 900, T("antes de clicar em", 52, DGRAY), anim="up")
        show(c, t, 4.2, CX, 1010, HL("CONTRATAR", 80, LGREEN, GREEN), anim="stamp")
        show(c, t, 5.4, 560, 1050, sc(cursor, s=1.2), anim="drop")
        selo_ep(c, t)
        hero(c, t, 860, FY, 0.85, [(0, "point_l"), (3.5, "finger_up")], [(0, "happy"), (3.5, "worried")], look=-0.7)
    elif t < 23.9:  # 1 juros
        titulo(c, t, "1. OS JUROS", 6.9)
        show(c, t, 8.6, 120, 450, sc(bank, s=0.6), anim="pop")
        show(c, t, 9.0, 230, 440, L("Banco Central", 56, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 10.1, 230, 505, L("média, set/2026", 48, DGRAY), anim="left", d=0.3)
        show(c, t, 12.5, CX, 680, HL("110% AO ANO", 96, PINKISH, RED), anim="stamp")
        show(c, t, 15.7, CX, 810, MM("= ~6,5% ao mês", 72, NAVY), anim="stamp")
        if t > 17.9:
            show(c, t, 17.9, 80, 960, L("grandes bancos, taxa máxima:", 50, DGRAY), anim="left", d=0.3)
            show(c, t, 21.8, CX, 1100, HL("6% a 10% ao mês", 80, LYELLOW), anim="stamp")
        hero(c, t, 880, FY, 0.85, [(0, "finger_up"), (12.5, "head"), (15.7, "present_l"), (21.8, "shrug")],
             [(0, "confident"), (12.5, "shocked"), (15.7, "think"), (21.8, "worried")], look=-0.7)
    elif t < 38.3:  # conta
        titulo(c, t, "A CONTA", 23.9)
        show(c, t, 25.1, 80, 450, L("R$ 5.000 em 12x", 80, INK, MARKER), anim="left", d=0.3)
        show(c, t, 27.2, 80, 550, L("a 6,5% ao mês", 60, DGRAY, MARKER), anim="left", d=0.3)
        show(c, t, 29.4, 80, 680, L("parcela:", 56, DGRAY), anim="left", d=0.3)
        if t > 29.6:
            reais(c, t, 29.6, 0, 613, 300, 690, 90, NAVY, d=1.4, pre="~R$ ", align="l")
        line(c, 80, 740, 820, 740, 5, LGRAY)
        show(c, t, 32.8, 80, 850, L("devolve:", 56, DGRAY), anim="left", d=0.3)
        if t > 33.4:
            reais(c, t, 33.4, 5000, 7354, 300, 860, 90, RED, d=1.0, align="l")
        show(c, t, 35.3, CX, 1060, HL("R$ 2.354 SÓ DE JUROS", 58, PINKISH, RED), anim="stamp")
        hero(c, t, 910, FY, 0.8, [(0, "present_l"), (33.4, "head")], [(0, "think"), (33.4, "shocked")], look=-0.7)
    elif t < 55.9:  # 2 CET
        titulo(c, t, "2. A TAXA NÃO É TUDO", 38.2)
        if t < 50.7:
            show(c, t, 39.3, 120, 460, MM("taxa", 66, NAVY), anim="pop")
            show(c, t, 41.5, 330, 460, MM("+ IOF", 66, RED), anim="pop")
            show(c, t, 43.3, 600, 460, MM("+ seguro", 66, RED), anim="pop")
            show(c, t, 45.2, CX, 640, HL("OLHA O CET", 96, LYELLOW), anim="stamp")
            show(c, t, 46.2, CX, 770, T("custo efetivo total", 60, NAVY), anim="up")
            show(c, t, 47.6, CX, 900, MM("= quanto você paga", 62, GREEN), anim="stamp")
            show(c, t, 49.4, CX, 990, MM("de verdade", 62, GREEN), anim="stamp")
        else:
            show(c, t, 50.9, 80, 500, L("seguro obrigatório?", 66, NAVY, MARKER), anim="left", d=0.3)
            show(c, t, 51.3, 260, 660, sc(big_x, 80), anim="stamp")
            show(c, t, 51.5, 380, 660, L("NÃO", 100, RED, MARKER), anim="stamp", d=0.3)
            show(c, t, 52.6, 80, 840, L("condicionar o empréstimo", 50, DGRAY), anim="left", d=0.3)
            show(c, t, 54.3, 170, 990, sc(gavel, s=0.6), anim="pop")
            show(c, t, 54.5, 500, 990, HL("= VENDA CASADA", 62, PINKISH, RED), anim="stamp")
        hero(c, t, 880, FY, 0.85, [(0, "finger_up"), (45.2, "point_l"), (50.7, "head"), (51.5, "finger_up")],
             [(0, "think"), (45.2, "confident"), (51.3, "angry"), (54.5, "confident")], look=-0.7)
    elif t < 70.9:  # 3 taxas diferentes
        titulo(c, t, "3. A MESMA PESSOA", 55.8)
        show(c, t, 56.8, CX, 430, T("taxas muito diferentes", 58, DGRAY), anim="up")
        show(c, t, 61.0, CX, 510, T("(ranking do Banco Central)", 46, DGRAY), anim="up")
        gbar(c, t, 63.3, 220, 1040, 110, GREEN, "um banco", "< 40% a.a.", w=170)
        gbar(c, t, 65.7, 560, 1040, 400, RED, "outra financeira", "> 250% a.a.", w=170)
        if t > 68.2:
            show(c, t, 68.2, CX, 1200, HL("SIMULA EM 3 LUGARES", 60, LYELLOW), anim="stamp")
        hero(c, t, 880, FY, 0.85, [(0, "present_l"), (65.7, "head"), (68.2, "finger_up")], [(0, "think"), (65.7, "shocked"), (68.2, "confident")], look=-0.7)
    elif t < 81.6:  # 4 consignado
        titulo(c, t, "4. TEM MAIS BARATO", 70.8)
        gbar(c, t, 73.3, 160, 1100, 130, GREEN, "consig. INSS", "24%", w=150, size=42)
        gbar(c, t, 77.4, 400, 1100, 260, ORANGE, "consig. CLT", "48%", w=150, size=42)
        gbar(c, t, 79.9, 640, 1100, 590, RED, "pessoal", "110%", w=150, size=42)
        show(c, t, 73.1, CX, 380, T("juros ao ano", 48, DGRAY), anim="up")
        hero(c, t, 900, FY, 0.8, [(0, "finger_up"), (79.9, "point_l")], [(0, "confident"), (79.9, "think")], look=-0.8)
    elif t < 90.6:  # por outro lado
        titulo(c, t, "POR OUTRO LADO", 81.5)
        show(c, t, 82.8, 80, 470, L("pessoal: 110% a.a.", 66, NAVY, MARKER), anim="left", d=0.3)
        show(c, t, 85.0, 80, 580, L("rotativo: 451% a.a.", 66, RED, MARKER), anim="left", d=0.3)
        show(c, t, 86.2, 80, 690, L("cheque especial: 144% a.a.", 60, RED, MARKER), anim="left", d=0.3)
        show(c, t, 87.3, CX, 860, MM("trocar dívida cara", 66, NAVY), anim="stamp")
        show(c, t, 89.1, CX, 980, HL("PODE VALER A PENA", 70, LGREEN, GREEN), anim="stamp")
        hero(c, t, 880, FY, 0.85, [(0, "present_l"), (87.3, "thumb")], [(0, "think"), (87.3, "happy")], look=-0.7)
    elif t < 96.6:  # antes de contratar
        titulo(c, t, "ANTES DE CONTRATAR", 90.5)
        for k, (t0, s) in enumerate(((91.8, "compara o CET"), (92.9, "não aceita seguro empurrado"), (94.7, "a parcela cabe no salário?"))):
            y = 470 + k * 140
            show(c, t, t0, 120, y - 15, sc(check_icon, 36), anim="pop")
            show(c, t, t0 + 0.1, 180, y, L(s, 54, NAVY, MARKER), anim="left", d=0.3)
        hero(c, t, 860, FY, 0.85, [(0, "finger_up"), (94.7, "thumb")], [(0, "confident"), (94.7, "happy")], look=-0.7)
    else:  # fim
        titulo(c, t, "O QUE NINGUÉM TE CONTA", 96.5)
        show(c, t, 97.5, CX, 450, MM("EP. 8: FINANCIAR MOTO", 56, NAVY), anim="stamp")
        show(c, t, 100.0, CX, 640, MM("VOCÊ JÁ PEGOU", 62, NAVY), anim="stamp")
        show(c, t, 100.4, CX, 750, MM("EMPRÉSTIMO PESSOAL?", 60, RED), anim="stamp")
        show(c, t, 101.9, 200, 950, sc(phone, s=1.0), anim="pop")
        show(c, t, 101.9, 480, 950, HL("COMENTA AÍ", 76, LYELLOW), anim="stamp")
        hero(c, t, 880, FY, 0.85, [(0, "point_l")], [(0, "happy"), (101.9, "grin")], look=-0.7)


SCENES = [(0, 999.0, palco)]
