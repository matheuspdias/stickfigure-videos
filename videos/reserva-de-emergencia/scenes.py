"""Se você fosse demitido hoje, quanto tempo aguentaria? A conta da reserva de emergência.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 3 blocos, 0,4 s entre blocos.
Tempos absolutos: bloco1 0,000 | bloco2 161,079 | bloco3 324,823 | fim da fala 558,410 | +5 s de tela final.
Premissas (25/10/2026): Selic 13,75% (Copom 16/9/2026), CDI 13,65%, IR regressivo da renda fixa; seguro-desemprego 2026
(teto R$ 2.518,65 acima de R$ 3.703,99; 5 parcelas com 24+ meses); cheque especial 8% ao mês e empréstimo pessoal 8,55%
(Procon-SP, 2/10/2026); PNAD 1º tri/2026 (6,6 mi desocupados; 21,2% < 1 mês, 51,4% 1 mês a 1 ano, 27,4% 1 ano ou mais);
IPCA 4,58% em 12 meses (set/2026). Contas em contas.py."""
import json
import os

from engine import *  # noqa

O2, O3 = 161.079, 324.823
END = 558.41

_PAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras.json"), encoding="utf-8"))


def w(word, after=0.0, d=0.0):
    """início (s) da primeira palavra que começa com `word` depois de `after` (tempo absoluto), mais d"""
    word = word.lower()
    for p in _PAL:
        if p["t0"] >= after - 0.01 and p["w"].lower().strip(",.:?!").startswith(word):
            return p["t0"] + d
    raise KeyError((word, after))


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def lv(label, val, lsize=50, vsize=60, vcol=GREEN, lcol=DGRAY):
    def f(c):
        text(c, label, 0, 0, lsize, HAND, lcol, align="l")
        x = text_w(c, label, lsize, HAND) + 18
        text(c, val, x, 0, vsize, MARKER, vcol, align="l")
    return f


def strike(wd=260, col=RED):
    return lambda c: line(c, -wd / 2, 8, wd / 2, -8, 10, col)


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def camila(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", PURPLE); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def bruno(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 4)
    other(c, t, x, y, s, poses, exprs, **kw)


def money_bar(c, t, t0, x, base, h, wd, col, top, label, d=0.9, tsize=56, lsize=42):
    k = grow(t, t0, d)
    if t < t0:
        return
    c.save(); c.translate(x, base)
    bar(c, max(4, h * k), wd, col)
    c.restore()
    if k > 0.6:
        if top:
            text(c, top, x, base - h * k - 42, tsize, MARKER, col if col != LGRAY else DGRAY)
        if label:
            text(c, label, x, base + 46, lsize, HAND, DGRAY)


def step(c, t, t0, num, head, col=LYELLOW):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"{num}. {head}", 0, 0, 70, col), anim="stamp")


def empty_pockets(c):
    """bolso vazio virado (sem dinheiro guardado)"""
    for dx in (-70, 70):
        poly(c, [(dx - 50, -40), (dx + 50, -40), (dx + 38, 50), (dx - 38, 50)]); fs(c, WHITE, 5)
    text(c, "R$ 0", 0, 130, 60, MARKER, RED)


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 4.7  se você fosse demitido hoje, quantos meses pagaria as contas?
    show(c, t, 0.05, 1180, 300, lambda c: hl(c, "DEMITIDO HOJE", 0, 0, 90, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("quantos"), 1180, 520, M("quantos meses você", 72, NAVY), anim="up")
    show(c, t, w("pagar"), 1180, 630, M("pagaria as contas?", 72, NAVY), anim="up")
    show(c, t, w("contas"), 1180, 830, sc(qmark, s=1.0), anim="pop")
    hero(c, t, 400, 1040, 1.05, [(0, "stand"), (w("quantos"), "think")], [(0, "shocked"), (w("quantos"), "think")],
         appear=0.05, look=1)


def s02(c, t):  # 4.7 - 14.8  aluguel, mercado, luz, internet, transporte; e se o salário parasse?
    show(c, t, 4.8, 960, 130, T("pensa rápido", 60, DGRAY), anim="up")
    items = [("aluguel", sc(house, s=0.85)), ("mercado", sc(cart, s=0.9)), ("luz", sc(bulb, s=1.0)),
             ("internet", sc(cursor, s=1.6)), ("transporte", sc(car, BLUE, s=0.7))]
    for i, (lab, fn) in enumerate(items):
        x = 300 + i * 330
        show(c, t, w(lab, 5.0), x, 360, fn, anim="pop")
        show(c, t, w(lab, 5.0, 0.1), x, 520, T(lab, 48), anim="fade")
    show(c, t, w("salário", 9.8), 420, 760, group(sc(bill, s=1.2), at(0, 0, sc(big_x, 70, s=1.0))), anim="pop")
    show(c, t, w("parasse", 9.8), 1060, 730, M("e se o salário parasse?", 60, RED), anim="up")
    show(c, t, w("até", 12.5), 1060, 830, T("até quando você aguentaria?", 52, DGRAY), anim="fade")
    hero(c, t, 1740, 1050, 0.5, [(0, "present_l"), (w("parasse", 9.8), "head")], [(0, "neutral"), (w("parasse", 9.8), "worried")],
         appear=4.8, look=-1)


def s03(c, t):  # 14.8 - 25.9  nem um mês; não é falta de esforço; quase ninguém fez a conta
    show(c, t, 14.9, 620, 200, T("pra muita gente, a resposta é", 54, DGRAY), anim="up")
    show(c, t, w("nem", 17.0), 620, 380, lambda c: text(c, "nem 1 mês", 0, 0, 130, MARKER, RED), anim="stamp")
    show(c, t, w("esforço", 19.0), 620, 560, group(sc(strike(520), s=1.0), at(0, 0, T("falta de esforço", 56, DGRAY))), anim="fade")
    show(c, t, w("ninguém", 21.0), 620, 720, lambda c: hl(c, "ninguém fez a conta com calma", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, w("hoje", 23.5), 620, 880, M("hoje a gente faz", 64, NAVY), anim="up")
    hero(c, t, 1480, 1040, 1.0, [(0, "stand"), (w("nem", 17.0), "head"), (w("hoje", 23.5), "present_l")],
         [(0, "neutral"), (w("nem", 17.0), "worried"), (w("hoje", 23.5), "confident")],
         appear=14.9, look=-1, prop=None)


def s04(c, t):  # 25.9 - 37.2  o roteiro: tempo pra voltar, seguro, quanto guardar, quanto tempo leva
    title(c, t, 26.0, "Hoje no vídeo", y=120, size=74)
    rows = [(w("quanto", 26.5), sc(clock, 0, s=0.45), "quanto tempo leva pra voltar ao trabalho"),
            (w("seguro", 29.5), sc(document, "SEGURO", BLUE, 28, s=0.45), "quanto o seguro-desemprego paga"),
            (w("guardado", 33.0), sc(piggy, s=0.4), "quanto você precisa ter guardado"),
            (w("juntar", 35.0), sc(calendar, "?", RED, 50, s=0.45), "quanto tempo leva pra juntar")]
    for i, (t0, fn, lab) in enumerate(rows):
        y = 290 + i * 175
        show(c, t, t0, 760, y, fn, anim="pop")
        show(c, t, t0 + 0.1, 880, y, L(lab, 56, NAVY), anim="left")
    hero(c, t, 330, 1040, 0.95, [(0, "present")], [(0, "happy")], appear=26.0, look=1)


def s05(c, t):  # 37.2 - 48.8  no final: mesmo salário, mesma demissão; uma sobra, outra deve +R$ 15 mil
    show(c, t, 37.3, 960, 130, T("no final: mesmo salário, demitidos no mesmo dia", 54, DGRAY), anim="up")
    camila(c, t, 560, 900, 0.75, [(0, "stand"), (w("sobrando"), "arms_up")], [(0, "neutral"), (w("sobrando"), "grin")],
           appear=w("pessoas"), look=0.5)
    bruno(c, t, 1360, 900, 0.75, [(0, "stand"), (w("devendo"), "head")], [(0, "neutral"), (w("devendo"), "desperate")],
          appear=w("pessoas", d=0.2), look=-0.5)
    show(c, t, w("sobrando"), 560, 990, lambda c: hl(c, "dinheiro sobrando", 0, 0, 52, LGREEN, GREEN), anim="stamp")
    show(c, t, w("devendo"), 1360, 990, lambda c: hl(c, "devendo +R$ 15 mil", 0, 0, 52, (1, 0.8, 0.76), RED), anim="stamp")
    hero(c, t, 960, 1000, 0.6, [(0, "shrug")], [(0, "think")], appear=w("final", 37.0), look=0)


def s06(c, t):  # 48.8 - 58.8  IBGE: 6,6 milhões de desempregados
    show(c, t, 48.9, 1100, 160, T("um número que pouca gente conhece", 54, DGRAY), anim="up")
    show(c, t, w("ibge"), 1100, 290, T("IBGE, começo de 2026", 50, DGRAY), anim="fade")
    show(c, t, w("seis", 55.0), 1100, 470, lambda c: text(c, "6,6 milhões", 0, 0, 130, MARKER, NAVY), anim="stamp")
    show(c, t, w("desempregados", 57.0), 1100, 620, M("de desempregados", 66, NAVY), anim="up")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("seis", 55.0), "point_r")], [(0, "neutral"), (w("seis", 55.0), "shocked")],
         appear=48.9, look=1)


def s07(c, t):  # 58.8 - 71.3  há quanto tempo procuram: <1 mês 21% | 1 mês a 1 ano 51% | 1 ano ou mais 27%
    show(c, t, 58.9, 960, 120, M("Há quanto tempo procuram emprego?", 64, NAVY), anim="up")
    base = 820
    money_bar(c, t, w("cinco", 59.5), 560, base, 21.2 * 9, 220, BLUE, "21%", "menos de 1 mês", tsize=64, lsize=46)
    money_bar(c, t, w("metade", 63.0), 960, base, 51.4 * 9, 220, ORANGE, "51%", "1 mês a 1 ano", tsize=64, lsize=46)
    money_bar(c, t, w("quatro", 67.5), 1360, base, 27.4 * 9, 220, RED, "27%", "mais de 1 ano", tsize=64, lsize=46)
    show(c, t, w("cinco", 59.5, 0.5), 560, 930, T("1 em cada 5", 44, BLUE), anim="fade")
    show(c, t, w("metade", 63.0, 0.5), 960, 930, T("metade", 44, ORANGE), anim="fade")
    show(c, t, w("quatro", 67.5, 0.5), 1360, 930, T("mais de 1 em cada 4", 44, RED), anim="fade")
    hero(c, t, 1720, 1050, 0.55, [(0, "present_l"), (w("quatro", 67.5), "head")], [(0, "neutral"), (w("quatro", 67.5), "shocked")],
         appear=58.9, look=-1)


def s08(c, t):  # 71.3 - 80.2  voltar no mês seguinte é a exceção; o comum é passar meses sem salário
    show(c, t, 71.4, 1140, 260, T("perder o emprego e voltar no mês seguinte", 52, DGRAY), anim="up")
    show(c, t, w("exceção"), 1140, 390, lambda c: hl(c, "é a exceção", 0, 0, 76, LYELLOW), anim="stamp")
    show(c, t, w("comum", 76.5), 1140, 580, T("o mais comum:", 54, DGRAY), anim="up")
    show(c, t, w("meses", 78.5), 1140, 710, M("alguns meses sem salário", 72, RED), anim="up")
    for i in range(3):
        show(c, t, w("meses", 78.5, 0.2 + i * 0.25), 940 + i * 200, 880, sc(calendar, "", GRAY, 40, s=0.55), anim="drop")
    hero(c, t, 330, 1040, 0.95, [(0, "finger_up"), (w("comum", 76.5), "shrug")], [(0, "confident"), (w("comum", 76.5), "worried")],
         appear=71.4, look=1)


def s09(c, t):  # 80.2 - 87.2  mas tem o seguro-desemprego; ajuda, mas tem limite
    show(c, t, 80.3, 1150, 220, T("\"mas tem o seguro-desemprego...\"", 58, DGRAY), anim="up")
    show(c, t, w("seguro", 81.5), 1150, 470, sc(document, "SEGURO", BLUE, 30, s=1.3), anim="pop")
    show(c, t, w("ajuda", 84.0), 870, 740, lambda c: hl(c, "ajuda bastante", 0, 0, 56, LGREEN, GREEN), anim="stamp")
    show(c, t, w("limite", 86.0), 1450, 740, lambda c: hl(c, "mas tem limite", 0, 0, 56, (1, 0.8, 0.76), RED), anim="stamp")
    other(c, t, 380, 1040, 0.9, [(0, "finger_up")], [(0, "confident")], appear=80.3, look=1)


def s10(c, t):  # 87.2 - 99.9  Camila: salário R$ 4.000, custo de vida R$ 3.200, 2+ anos de carteira
    show(c, t, 87.3, 1250, 130, M("Exemplo: a Camila", 70, PURPLE), anim="up")
    camila(c, t, 420, 1040, 1.0, [(0, "wave"), (w("custo", 91.5), "present")], [(0, "happy")], appear=87.4, look=1)
    show(c, t, w("quatro", 89.5), 850, 330, lv("salário:", "R$ 4.000", 56, 80, GREEN), anim="left")
    show(c, t, w("custo", 91.5), 850, 500, lv("custo de vida:", "R$ 3.200", 56, 80, RED), anim="left")
    show(c, t, w("somado", 93.5), 1250, 590, T("(tudo somado, por mês)", 44, DGRAY), anim="fade")
    show(c, t, w("carteira", 98.5), 1250, 760, lambda c: hl(c, "2+ anos de carteira assinada", 0, 0, 54, LBLUE), anim="stamp")


def s11(c, t):  # 99.9 - 114.1  ganhava mais de R$ 3.700 → teto: R$ 2.518 por mês (4 mil ou 10 mil: igual)
    show(c, t, 100.0, 1150, 140, T("seguro-desemprego 2026", 56, DGRAY), anim="up")
    show(c, t, w("ganhava", 101.0), 900, 270, lv("salário acima de", "R$ 3.700", 52, 66, NAVY), anim="left")
    show(c, t, w("máximo", 105.0), 1150, 380, T("recebe o valor máximo:", 52, DGRAY), anim="fade")
    show(c, t, w("dois", 106.5), 1150, 550, lambda c: text(c, "R$ 2.518", 0, 0, 150, MARKER, BLUE), anim="stamp")
    show(c, t, w("mês", 108.8), 1150, 680, T("por mês", 52, DGRAY), anim="fade")
    show(c, t, w("quatro", 110.9), 820, 830, M("R$ 4.000", 56, DGRAY), anim="pop")
    show(c, t, w("dez", 112.0), 1500, 830, M("R$ 10.000", 56, DGRAY), anim="pop")
    show(c, t, w("teto", 113.0), 1150, 830, lambda c: hl(c, "= teto", 0, 0, 52, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("dois", 106.5), "point_r")], [(0, "neutral"), (w("dois", 106.5), "shocked")],
         appear=100.0, look=1)


def s12(c, t):  # 114.1 - 120.6  5 parcelas; cinco meses e acabou
    show(c, t, 114.2, 960, 150, M("5 parcelas", 90, NAVY), anim="up")
    for i in range(5):
        show(c, t, w("cinco", 117.0, 0.15 * i), 450 + i * 255, 430, sc(calendar, str(i + 1), BLUE, 70, s=0.8), anim="drop")
    show(c, t, w("acabou", 119.5), 960, 680, lambda c: hl(c, "5 meses... e acabou", 0, 0, 70, (1, 0.8, 0.76), RED), anim="stamp")
    hero(c, t, 960, 1050, 0.55, [(0, "present"), (w("acabou", 119.5), "shrug")], [(0, "neutral"), (w("acabou", 119.5), "worried")],
         appear=114.2)


def s13(c, t):  # 120.6 - 135.3  custo R$ 3.200 - seguro R$ 2.518 = faltam ~R$ 680/mês; do 6º mês: falta tudo
    show(c, t, 120.7, 960, 120, M("Faz a conta", 72, NAVY), anim="up")
    base = 820
    money_bar(c, t, w("custo", 121.5), 520, base, 3200 * 0.15, 230, RED, "R$ 3.200", "custo de vida", tsize=58)
    money_bar(c, t, w("seguro", 124.5), 900, base, 2518 * 0.15, 230, BLUE, "R$ 2.518", "seguro", tsize=58)
    if t > w("faltam", 127.5):
        k = grow(t, w("faltam", 127.5), 0.6)
        c.save(); rrect(c, 900 - 115, base - 480, 230, (480 - 2518 * 0.15) * k, 8)
        c.set_dash([14, 10]); fs(c, (1, 0.8, 0.76), 5); c.restore()
    show(c, t, w("faltam", 127.5), 900, 285, M("faltam ~R$ 680", 50, RED), anim="stamp")
    show(c, t, w("sexto", 130.5), 1450, 380, T("do 6º mês em diante:", 52, DGRAY), anim="up")
    show(c, t, w("tudo", 132.5), 1450, 520, lambda c: hl(c, "falta tudo", 0, 0, 72, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("três", 133.2), 1450, 650, M("R$ 3.200 por mês", 60, RED), anim="up")
    hero(c, t, 1700, 1050, 0.5, [(0, "present_l"), (w("tudo", 132.5), "head")], [(0, "neutral"), (w("tudo", 132.5), "desperate")],
         appear=120.7, look=-1, prop=("r", prop_calculator))


def s14(c, t):  # 135.3 - 145.6  e essa é a situação boa: sem seguro pra quem pede demissão, justa causa, autônomo/PJ
    show(c, t, 135.4, 1100, 140, lambda c: hl(c, "e essa é a situação boa", 0, 0, 66, LYELLOW), anim="stamp")
    show(c, t, w("seguro", 141.5), 1100, 270, T("não recebem seguro:", 52, DGRAY), anim="up")
    rows = [(w("pede", 138.0), "quem pede demissão"), (w("justa", 140.0), "demitido por justa causa"),
            (w("autônomo", 143.0), "autônomo ou PJ")]
    for i, (t0, lab) in enumerate(rows):
        y = 410 + i * 150
        show(c, t, t0, 760, y, sc(x_icon, 40, s=1.0), anim="pop")
        show(c, t, t0 + 0.1, 840, y, L(lab, 60, INK), anim="left")
    hero(c, t, 330, 1040, 0.95, [(0, "finger_up"), (w("autônomo", 143.0), "shrug")], [(0, "confident"), (w("autônomo", 143.0), "worried")],
         appear=135.4, look=1)


def s15(c, t):  # 145.6 - O2  FGTS: pode ajudar, mas não dá pra contar; saque-aniversário; fica fora da conta
    show(c, t, 145.7, 1150, 140, M("E o FGTS?", 80, NAVY), anim="up")
    show(c, t, w("ajudar", 147.0), 1150, 270, T("pode ajudar, mas não dá pra contar com ele", 52, DGRAY), anim="fade")
    show(c, t, w("usou", 150.5), 900, 440, group(sc(bank, s=0.55), at(0, 140, T("muita gente já usou", 46))), anim="pop")
    show(c, t, w("saque", 152.0), 1440, 440, group(sc(calendar, "ANIV.", ORANGE, 40, s=0.7), at(0, 140, T("saque-aniversário:", 46))),
         anim="pop")
    show(c, t, w("saldo", 154.0), 1440, 650, lambda c: hl(c, "saldo preso na demissão", 0, 0, 46, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("fora", 156.5), 1150, 820, lambda c: hl(c, "nesta conta: FGTS e rescisão fora", 0, 0, 52, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "think"), (w("fora", 156.5), "present")], [(0, "think"), (w("fora", 156.5), "neutral")],
         appear=145.7, look=1)


# ======================================================================= BLOCO 2
def s16(c, t):  # O2 - 177.2  quanto guardar: 3 a 6 meses do CUSTO DE VIDA (não o salário)
    show(c, t, O2, 1150, 140, M("Quanto ter guardado?", 74, NAVY), anim="up")
    show(c, t, w("três", 165.0), 1150, 330, lambda c: text(c, "3 a 6 meses", 0, 0, 120, MARKER, GREEN), anim="stamp")
    show(c, t, w("custo", 167.5), 1150, 470, M("do seu custo de vida", 64, NAVY), anim="up")
    show(c, t, w("salário", 173.5), 950, 650, group(sc(strike(300), s=1.0), at(0, 0, M("salário", 60, DGRAY))), anim="fade")
    show(c, t, w("gasta", 175.5), 1400, 650, lambda c: hl(c, "o que você gasta", 0, 0, 58, LYELLOW), anim="stamp")
    show(c, t, w("emergência", 168.5), 1150, 840, sc(piggy, s=0.8), anim="drop")
    hero(c, t, 330, 1040, 0.95, [(0, "think"), (w("três", 165.0), "present"), (w("palavra", 170.0), "finger_up")],
         [(0, "think"), (w("três", 165.0), "happy"), (w("palavra", 170.0), "confident")], appear=O2, look=1)


def s17(c, t):  # 177.2 - 183.9  6 x R$ 3.200 = R$ 19.200
    show(c, t, 177.3, 800, 200, lv("custo de vida:", "R$ 3.200", 56, 72, RED), anim="left")
    show(c, t, w("seis", 179.5), 1150, 350, M("x 6 meses", 76, NAVY), anim="up")
    show(c, t, w("dezenove", 180.5), 1150, 560, lambda c: hl(c, "R$ 19.200", 0, 0, 130, LGREEN, GREEN), anim="stamp")
    show(c, t, w("dezenove", 180.5, 0.6), 1150, 800, sc(piggy, s=0.9), anim="drop")
    camila(c, t, 380, 1040, 0.9, [(0, "stand"), (w("dezenove", 180.5), "arms_up")], [(0, "neutral"), (w("dezenove", 180.5), "shocked")],
           appear=177.3, look=1)


def s18(c, t):  # 183.9 - 194.6  renda instável (autônomo, PJ, comissão): 12 meses
    show(c, t, 184.0, 1150, 150, T("renda instável?", 60, DGRAY), anim="up")
    for i, (lab, t0) in enumerate([("autônomo", w("autônomo", 185.0)), ("PJ", w("pj", 186.0)), ("comissão", w("comissão", 187.0))]):
        show(c, t, t0, 820 + i * 330, 300, lambda c, lab=lab: hl(c, lab, 0, 0, 54, LBLUE), anim="stamp")
    show(c, t, w("doze", 190.5), 1150, 520, lambda c: text(c, "12 meses", 0, 0, 130, MARKER, ORANGE), anim="stamp")
    show(c, t, w("ninguém", 192.5), 1150, 720, T("ninguém te paga seguro-desemprego", 54, RED), anim="fade")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("doze", 190.5), "finger_up")], [(0, "neutral"), (w("doze", 190.5), "confident")],
         appear=184.0, look=1)


def s19(c, t):  # 194.6 - 200.5  a parte que assusta: quanto tempo leva pra juntar R$ 19.200?
    show(c, t, 194.7, 1150, 200, T("a parte que assusta", 60, RED), anim="up")
    show(c, t, w("quanto", 196.5), 1150, 380, M("quanto tempo leva", 80, NAVY), anim="up")
    show(c, t, w("juntar", 197.5), 1150, 500, M("pra juntar R$ 19.200?", 80, NAVY), anim="up")
    show(c, t, w("dezenove", 198.5), 1150, 760, group(sc(clock, 0, s=0.9), at(190, -40, sc(qmark, s=0.7))), anim="pop")
    hero(c, t, 330, 1040, 0.95, [(0, "think")], [(0, "think")], appear=194.7, look=1)


def s20(c, t):  # 200.5 - 210.3  guarda R$ 400/mês (10%); sem render: 48 meses = 4 anos
    show(c, t, 200.6, 720, 170, lv("a Camila guarda", "R$ 400 por mês", 56, 74, GREEN), anim="left")
    show(c, t, w("dez", 203.5), 1150, 280, T("(10% do salário)", 48, DGRAY), anim="fade")
    show(c, t, w("render", 205.0), 1150, 430, T("sem render nada:", 56, DGRAY), anim="up")
    show(c, t, w("quarenta", 206.5), 1150, 590, lambda c: text(c, "48 meses", 0, 0, 120, MARKER, RED), anim="stamp")
    show(c, t, w("quatro", 208.0), 1150, 750, lambda c: hl(c, "4 anos", 0, 0, 90, (1, 0.8, 0.76), RED), anim="stamp")
    camila(c, t, 380, 1040, 0.9, [(0, "present"), (w("quatro", 208.0), "head")], [(0, "happy"), (w("quatro", 208.0), "shocked")],
           appear=200.6, look=1, )


def s21(c, t):  # 210.3 - 227.4  rendendo 100% do CDI (Selic 13,75%), já sem IR: 40 meses = 3 anos e 4 meses
    show(c, t, 210.4, 1150, 140, T("mas ela não deixa parado", 56, DGRAY), anim="up")
    show(c, t, w("aplicação", 212.0), 1150, 250, lambda c: hl(c, "liquidez diária, 100% do CDI", 0, 0, 56, LBLUE), anim="stamp")
    show(c, t, w("selic", 217.0), 1150, 360, T("Selic 13,75% ao ano, já sem o imposto", 50, DGRAY), anim="fade")
    show(c, t, w("quarenta", 223.0), 1150, 520, M("40 meses", 90, NAVY), anim="up")
    show(c, t, w("três", 225.2), 1150, 700, lambda c: hl(c, "3 anos e 4 meses", 0, 0, 110, LYELLOW, INK), anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("três", 225.2), "arms_up")], [(0, "happy"), (w("três", 225.2), "shocked")],
         appear=210.4, look=1, prop=("l", prop_tablet))


def s22(c, t):  # 227.4 - 238.8  R$ 19.200 = R$ 16.000 do bolso + R$ 3.200 de juros = 1 mês de reserva
    show(c, t, 227.5, 960, 120, M("De onde vieram os R$ 19.200", 66, NAVY), anim="up")
    base, x, wd = 900, 760, 300
    k1 = grow(t, w("dezesseis", 228.0), 0.9)
    if t > w("dezesseis", 228.0):
        c.save(); c.translate(x, base); bar(c, max(4, 16000 * 0.033 * k1), wd, NAVY); c.restore()
        if k1 > 0.6:
            text(c, "R$ 16.000", x + 330, base - 270, 64, MARKER, NAVY)
            text(c, "do bolso", x + 330, base - 200, 48, HAND, DGRAY)
    k2 = grow(t, w("três", 231.5), 0.7)
    if t > w("três", 231.5):
        h1 = 16000 * 0.033
        c.save(); c.translate(x, base - h1); bar(c, max(4, 3200 * 0.033 * k2), wd, GREEN); c.restore()
        if k2 > 0.6:
            text(c, "R$ 3.200", x + 330, base - h1 - 60, 64, MARKER, GREEN)
            text(c, "de juros", x + 330, base - h1 + 5, 48, HAND, DGRAY)
    show(c, t, w("sozinhos", 234.5), 1500, 820, lambda c: hl(c, "= 1 mês de reserva", 0, 0, 56, LGREEN, GREEN), anim="stamp")
    hero(c, t, 330, 1040, 0.8, [(0, "point_r"), (w("sozinhos", 234.5), "thumb")], [(0, "neutral"), (w("sozinhos", 234.5), "grin")],
         appear=227.5, look=1)


def s23(c, t):  # 238.8 - 255.4  parece muito, mas: 8 meses = 1 mês; 1 ano e 10 meses = 3 meses; 40 meses = 6
    show(c, t, 238.9, 960, 120, T("parece muito... mas olha o caminho", 56, DGRAY), anim="up")
    x0, x1, y = 300, 1620, 520
    if t > w("olha", 244.0):
        k = grow(t, w("olha", 244.0), 1.2)
        line(c, x0, y, x0 + (x1 - x0) * k, y, 10, NAVY)
    marks = [(w("oito", 245.5), 8, "8 meses", "1 mês guardado"),
             (w("ano", 251.5), 22, "1 ano e 10 meses", "3 meses"),
             (w("olha", 244.0, 0.3), 40, "3 anos e 4 meses", "6 meses")]
    for t0, m, top, lab in marks:
        xx = x0 + (x1 - x0) * m / 40
        show(c, t, t0, xx, y, lambda c: circle(c, 0, 0, 22, GOLD, 5), anim="pop")
        show(c, t, t0, xx, y - 80, M(top, 46, NAVY), anim="up")
        show(c, t, t0 + 0.2, xx, y + 90, lambda c, lab=lab: hl(c, lab, 0, 0, 46, LGREEN, GREEN), anim="stamp")
    show(c, t, 238.9, x0, y + 90, T("hoje", 46, DGRAY), anim="fade")
    camila(c, t, 960, 1050, 0.55, [(0, "think"), (w("oito", 245.5), "arms_up")], [(0, "think"), (w("oito", 245.5), "grin")],
           appear=238.9)


def s24(c, t):  # 255.4 - 262.3  cada mês guardado = um mês de tranquilidade; já protege
    show(c, t, 255.5, 1150, 260, M("cada mês guardado", 78, NAVY), anim="up")
    show(c, t, w("tranquilidade"), 1150, 400, lambda c: hl(c, "= 1 mês de tranquilidade", 0, 0, 72, LGREEN, GREEN), anim="stamp")
    show(c, t, w("proteger"), 1150, 680, sc(shield, GREEN, s=1.1), anim="pop")
    hero(c, t, 330, 1040, 0.95, [(0, "relax")], [(0, "happy")], appear=255.5, look=1)


def s25(c, t):  # 262.3 - 276.6  acelerar: 13º inteiro na reserva → pouco mais de 2 anos; vídeo do 13º
    show(c, t, 262.4, 520, 150, M("Dá pra acelerar", 74, NAVY), anim="up")
    show(c, t, w("décimo", 263.0), 170, 330, lv("+ o 13º inteiro", "todo ano", 56, 66, GREEN), anim="left")
    show(c, t, w("pouco", 268.0), 520, 500, lambda c: hl(c, "pouco mais de 2 anos", 0, 0, 72, LGREEN, GREEN), anim="stamp")
    show(c, t, w("vídeo", 271.0), 1350, 480, lambda c: video_card(c, "O que fazer com o 13º", "a ordem certa", w=640, h=380,
                                                                  icon=lambda c: play_btn(c, 60)), anim="pop")
    show(c, t, w("quitar", 274.0), 1350, 760, T("reserva vinha logo depois de quitar dívida cara", 42, DGRAY), anim="fade")
    camila(c, t, 520, 1050, 0.55, [(0, "stand"), (w("pouco", 268.0), "arms_up")], [(0, "happy"), (w("pouco", 268.0), "grin")],
           appear=262.4)


def s26(c, t):  # 276.6 - 281.9  onde deixar esse dinheiro? 3 regras
    show(c, t, 276.7, 1150, 340, M("Onde deixar a reserva?", 80, NAVY), anim="up")
    show(c, t, w("regras", 279.5), 1150, 560, lambda c: hl(c, "3 regras", 0, 0, 110, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "think"), (w("regras", 279.5), "finger_up")], [(0, "think"), (w("regras", 279.5), "confident")],
         appear=276.7, look=1)


def s27(c, t):  # 281.9 - 289.0  1. liquidez diária: sacar no mesmo dia, sem multa, sem vencimento
    step(c, t, 281.9, 1, "liquidez diária")
    show(c, t, w("sacar", 284.0), 760, 480, sc(calendar, "HOJE", GREEN, 50, s=1.3), anim="drop")
    show(c, t, w("dia", 284.8), 1350, 360, L("sacar no mesmo dia", 58, NAVY), anim="left")
    show(c, t, w("multa", 285.5), 1350, 490, L("sem multa", 58, NAVY), anim="left")
    show(c, t, w("vencimento", 286.5), 1350, 620, L("sem esperar vencimento", 58, NAVY), anim="left")
    for i, t0 in enumerate([w("dia", 284.8), w("multa", 285.5), w("vencimento", 286.5)]):
        show(c, t, t0, 1300, 360 + i * 130, sc(check_icon, 30, s=1.0), anim="pop")
    hero(c, t, 330, 1040, 0.9, [(0, "present")], [(0, "happy")], appear=282.0, look=1)


def s28(c, t):  # 289.0 - 299.0  2. baixo risco: nada de ações, cripto, coisa que oscila
    step(c, t, 289.0, 2, "baixo risco")
    show(c, t, w("cair", 291.0), 1100, 280, T("não pode cair justo quando você precisa", 54, DGRAY), anim="up")
    items = [(w("ações", 294.5), "ações"), (w("cripto", 295.5), "cripto"), (w("oscila", 296.5), "o que oscila")]
    for i, (t0, lab) in enumerate(items):
        x = 700 + i * 380
        show(c, t, t0, x, 500, lambda c, i=i: _zigzag(c), anim="pop")
        show(c, t, t0 + 0.1, x, 500, sc(big_x, 70, s=1.0), anim="stamp")
        show(c, t, t0, x, 650, T(lab, 54), anim="fade")
    hero(c, t, 260, 1050, 0.75, [(0, "finger_up"), (w("ações", 294.5), "shrug")], [(0, "confident"), (w("ações", 294.5), "worried")],
         appear=289.1, look=1)


def _zigzag(c):
    rrect(c, -130, -95, 260, 190, 14); fs(c, WHITE, 5)
    c.save(); c.move_to(-105, 40)
    for p in [(-65, -20), (-30, 50), (10, -55), (45, 10), (80, -40), (105, 60)]:
        c.line_to(*p)
    rgb(c, ORANGE); c.set_line_width(9); c.stroke(); c.restore()


def s29(c, t):  # 299.0 - 315.7  3. render pelo menos o CDI: Tesouro Selic, renda fixa com liquidez diária e FGC; conta parada perde
    step(c, t, 299.0, 3, "render pelo menos o CDI")
    show(c, t, w("títulos", 301.5), 1150, 300, lambda c: hl(c, "títulos públicos atrelados à Selic", 0, 0, 56, LBLUE), anim="stamp")
    show(c, t, w("aplicações", 303.0), 1150, 420, lambda c: hl(c, "renda fixa com liquidez diária + FGC", 0, 0, 56, LBLUE), anim="stamp")
    show(c, t, w("parado", 310.0), 1050, 620, group(sc(bank, s=0.5), at(250, 0, L("parado na conta corrente", 52, DGRAY))), anim="left")
    show(c, t, w("inflação", 311.8), 1150, 790, lambda c: hl(c, "perde pra inflação (4,58% ao ano)", 0, 0, 56, (1, 0.8, 0.76), RED),
         anim="stamp")
    hero(c, t, 300, 1040, 0.85, [(0, "present"), (w("parado", 310.0), "shrug")], [(0, "happy"), (w("parado", 310.0), "worried")],
         appear=299.1, look=1, prop=None)


def s30(c, t):  # 315.7 - O3  deixe separada da conta do dia a dia
    show(c, t, 315.8, 1150, 150, M("Deixe separada", 80, NAVY), anim="up")
    show(c, t, w("conta", 318.5), 850, 470, group(sc(card, BLUE, s=1.1), at(0, 160, T("conta do dia a dia", 48))), anim="pop")
    show(c, t, w("separada", 317.5), 1450, 470, group(sc(piggy, s=0.8), at(0, 160, T("reserva", 48, GREEN))), anim="pop")
    show(c, t, w("vê", 320.8), 1150, 800, T("dinheiro que você vê todo dia vira gasto", 54, RED), anim="fade")
    hero(c, t, 330, 1040, 0.95, [(0, "point_r")], [(0, "confident")], appear=315.8, look=1)


# ======================================================================= BLOCO 3
def s31(c, t):  # O3 - 339.2  Camila e Bruno: mesma empresa, R$ 4.000, gastam R$ 3.200, demitidos no mesmo dia
    show(c, t, O3, 960, 120, M("A história: Camila x Bruno", 70, NAVY), anim="up")
    camila(c, t, 560, 900, 0.8, [(0, "stand"), (w("demitidos", 336.0), "head")], [(0, "happy"), (w("demitidos", 336.0), "shocked")],
           appear=w("camila", O3), look=0.6)
    bruno(c, t, 1360, 900, 0.8, [(0, "stand"), (w("demitidos", 336.0), "head")], [(0, "happy"), (w("demitidos", 336.0), "shocked")],
          appear=w("bruno", O3), look=-0.6)
    show(c, t, w("ganham", 330.0), 960, 330, lv("salário:", "R$ 4.000", 46, 58, GREEN), anim="fade")
    show(c, t, w("gastam", 333.0), 960, 440, lv("gastos:", "R$ 3.200", 46, 58, RED), anim="fade")
    show(c, t, w("demitidos", 336.0), 960, 600, sc(moving_box, s=0.8), anim="drop")
    show(c, t, w("demitidos", 336.0, 0.4), 960, 990, lambda c: hl(c, "demitidos no mesmo dia", 0, 0, 52, (1, 0.8, 0.76), RED),
         anim="stamp")


def s32(c, t):  # 339.2 - 347.9  Camila tem a reserva de R$ 19.200; Bruno não tem nada guardado
    show(c, t, 339.3, 960, 120, T("a única diferença", 58, DGRAY), anim="up")
    camila(c, t, 520, 1040, 0.8, [(0, "present")], [(0, "happy")], appear=339.3, look=0.6)
    show(c, t, w("reserva", 341.0), 700, 420, group(sc(piggy, s=0.8), at(0, 170, M("R$ 19.200", 66, GREEN))), anim="pop")
    bruno(c, t, 1440, 1040, 0.8, [(0, "shrug")], [(0, "worried")], appear=339.4, look=-0.6)
    show(c, t, w("nada", 345.5), 1250, 420, empty_pockets, anim="pop")


def s33(c, t):  # 347.9 - 356.4  os dois levam 8 meses pra conseguir emprego; dentro do caso mais comum
    show(c, t, 348.0, 1150, 200, T("os dois levam", 58, DGRAY), anim="up")
    show(c, t, w("oito", 349.0), 1150, 360, lambda c: text(c, "8 meses", 0, 0, 130, MARKER, ORANGE), anim="stamp")
    show(c, t, w("emprego", 350.5), 1150, 480, T("pra conseguir um emprego novo", 52, DGRAY), anim="fade")
    for i in range(8):
        show(c, t, w("oito", 349.0, 0.15 * i), 700 + i * 130, 880, sc(calendar, str(i + 1), ORANGE, 50, s=0.5), anim="drop")
    show(c, t, w("comum", 353.5), 1150, 680, lambda c: hl(c, "o caso mais comum: 1 mês a 1 ano", 0, 0, 56, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("lembra", 351.0), "finger_up")], [(0, "neutral"), (w("lembra", 351.0), "confident")],
         appear=348.0, look=1)


def s34(c, t):  # 356.4 - 373.7  meses 1-5: faltam ~R$ 680; meses 6-8: faltam R$ 3.200; total ~R$ 13 mil
    show(c, t, 356.5, 960, 120, M("Quanto falta a cada mês", 66, NAVY), anim="up")
    base = 900
    for m in range(8):
        x = 330 + m * 180
        if m < 5:
            t0 = w("primeiros", 356.5, 0.2 + m * 0.25)
            money_bar(c, t, t0, x, base, 681 * 0.17, 120, RED, "680" if m == 0 else None, f"mês {m + 1}", tsize=44, lsize=38)
        else:
            t0 = w("três", 363.5, 0.2 + (m - 5) * 0.3)
            money_bar(c, t, t0, x, base, 3200 * 0.17, 120, RED, "3.200" if m == 5 else None, f"mês {m + 1}", tsize=44, lsize=38)
    show(c, t, w("seguro", 356.5), 690, 230, lambda c: hl(c, "com o seguro", 0, 0, 48, LBLUE), anim="stamp")
    show(c, t, w("tudo", 364.0), 1410, 230, lambda c: hl(c, "sem seguro", 0, 0, 48, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("treze", 370.5), 960, 1010, lambda c: hl(c, "total: ~R$ 13 mil pra cada um", 0, 0, 58, LYELLOW), anim="stamp")


def s35(c, t):  # 373.7 - 385.5  Bruno cobre no cheque especial: já está ali... 8% ao mês
    show(c, t, 373.8, 1150, 150, T("o Bruno cobre o buraco no", 56, DGRAY), anim="up")
    show(c, t, w("cheque", 376.0), 1150, 290, M("cheque especial", 90, RED), anim="stamp")
    show(c, t, w("ali", 378.5), 1150, 450, T("já está ali, na conta, sem pedir nada", 52, DGRAY), anim="fade")
    show(c, t, w("oito", 383.0), 1150, 640, lambda c: hl(c, "8% ao mês", 0, 0, 110, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("oito", 383.0, 0.5), 1150, 790, T("(151% ao ano)", 50, RED), anim="fade")
    bruno(c, t, 380, 1040, 0.95, [(0, "shrug"), (w("oito", 383.0), "head")], [(0, "neutral"), (w("oito", 383.0), "shocked")],
          appear=373.8, look=1)


def s36(c, t):  # 385.5 - 401.8  dívida: 5º mês R$ 4.000 | 6º R$ 7.500 | 8º R$ 15.423
    show(c, t, 385.6, 1150, 120, M("A dívida do Bruno", 70, RED), anim="up")
    base = 880
    money_bar(c, t, w("quinto", 385.6), 720, base, 4000 * 0.036, 220, ORANGE, "R$ 4.000", "5º mês", tsize=56, lsize=46)
    money_bar(c, t, w("sete", 391.0), 1060, base, 7500 * 0.036, 220, RED, "R$ 7.500", "6º mês", tsize=56, lsize=46)
    money_bar(c, t, w("quinze", 397.5), 1440, base, 15423 * 0.036, 240, RED, None, "8º mês", tsize=56, lsize=46)
    show(c, t, w("quinze", 397.5, 0.5), 1440, base - 15423 * 0.036 - 60, M("R$ 15.423", 76, RED), anim="stamp")
    bruno(c, t, 330, 1040, 0.85, [(0, "stand"), (w("sexto", 388.0), "head"), (w("quinze", 397.5), "head")],
          [(0, "worried"), (w("quinze", 397.5), "desperate")], appear=385.6, look=1)


def s37(c, t):  # 401.8 - 411.1  usou R$ 13 mil, deve R$ 15.400: +R$ 2.400 só de juros em 8 meses
    show(c, t, 401.9, 880, 260, lv("usou:", "R$ 13.000", 60, 84, ORANGE), anim="left")
    show(c, t, w("deve", 403.5), 880, 420, lv("deve:", "R$ 15.400", 60, 84, RED), anim="left")
    show(c, t, w("dois", 406.5), 1150, 640, lambda c: hl(c, "+R$ 2.400 só de juros", 0, 0, 80, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("oito", 409.0), 1150, 780, T("em 8 meses", 54, DGRAY), anim="fade")
    bruno(c, t, 380, 1040, 0.95, [(0, "head")], [(0, "desperate")], appear=401.9, look=1)


def s38(c, t):  # 411.1 - 429.9  juros de R$ 1.234 por mês = 3x o que ele guardava; pagando R$ 400 a dívida cresce
    show(c, t, 411.2, 960, 120, T("e o pior vem agora", 58, RED), anim="up")
    show(c, t, w("mil", 415.0), 640, 330, lambda c: text(c, "R$ 1.234", 0, 0, 110, MARKER, RED), anim="stamp")
    show(c, t, w("juros", 418.0), 640, 450, T("de juros por mês", 54, DGRAY), anim="fade")
    show(c, t, w("três", 420.0), 640, 600, lambda c: hl(c, "3x o que ele guardava (R$ 400)", 0, 0, 50, LYELLOW), anim="stamp")
    show(c, t, w("quatrocentos", 423.5), 1400, 330, lv("paga", "R$ 400", 54, 70, GREEN), anim="left")
    show(c, t, w("diminui", 426.0), 1400, 450, T("e a dívida não diminui", 52, DGRAY), anim="fade")
    if t > w("crescendo", 427.5):
        k = grow(t, w("crescendo", 427.5), 1.0)
        arrow(c, 1250, 760, 1250 + 300 * k, 760 - 170 * k, RED, 12, 0, 36)
    show(c, t, w("crescendo", 427.5), 1450, 820, M("cresce", 70, RED), anim="stamp")
    bruno(c, t, 960, 1050, 0.55, [(0, "head")], [(0, "desperate")], appear=411.2)


def s39(c, t):  # 429.9 - 446.1  empréstimo pessoal ~8,5%: pagando R$ 1.500/mês, +2 anos e ~R$ 39 mil pagos
    show(c, t, 430.0, 1150, 140, T("trocando por um empréstimo pessoal", 56, DGRAY), anim="up")
    show(c, t, w("oito", 432.5), 1150, 260, lambda c: hl(c, "~8,5% ao mês", 0, 0, 66, (1, 0.8, 0.76), RED), anim="stamp")
    show(c, t, w("pagando", 435.0), 820, 390, lv("pagando", "R$ 1.500 por mês", 54, 66, NAVY), anim="left")
    show(c, t, w("anos", 438.5), 1150, 510, M("mais de 2 anos pra quitar", 64, ORANGE), anim="up")
    show(c, t, w("trinta", 441.5), 1150, 680, lambda c: text(c, "~R$ 39 mil pagos", 0, 0, 100, MARKER, RED), anim="stamp")
    show(c, t, w("treze", 444.5), 1150, 820, T("por um buraco de R$ 13 mil", 54, DGRAY), anim="fade")
    bruno(c, t, 330, 1040, 0.9, [(0, "think"), (w("trinta", 441.5), "head")], [(0, "worried"), (w("trinta", 441.5), "desperate")],
          appear=430.0, look=1)


def s40(c, t):  # 446.1 - 462.4  Camila: tirou o mesmo dinheiro, o resto rendeu; volta com R$ 7.390 e nenhuma dívida
    show(c, t, 446.2, 1150, 130, M("E a Camila?", 76, PURPLE), anim="up")
    base, x = 900, 1000
    k = grow(t, w("tirando", 447.5), 4.0)
    if t > 446.3:
        h = (19200 - (19200 - 7392) * k) * 0.028
        c.save(); c.translate(x, base); bar(c, max(4, h), 260, GREEN); c.restore()
        text(c, "reserva", x, base + 46, 44, HAND, DGRAY)
        if t < w("sete", 456.0):
            text(c, f"R$ {int(round((19200 - (19200 - 7392) * k) / 10) * 10):,}".replace(",", "."), x, base - h - 45, 56, MARKER, GREEN)
    show(c, t, w("rendendo", 452.0), 1450, 360, T("o que ficou continuou rendendo", 48, DGRAY), anim="fade")
    show(c, t, w("sete", 456.0), 1000, base - 7392 * 0.028 - 50, M("R$ 7.390", 76, GREEN), anim="stamp")
    show(c, t, w("nenhuma", 460.0), 1450, 560, lambda c: hl(c, "e nenhuma dívida", 0, 0, 64, LGREEN, GREEN), anim="stamp")
    camila(c, t, 380, 1040, 0.95, [(0, "present"), (w("nenhuma", 460.0), "arms_up")], [(0, "neutral"), (w("nenhuma", 460.0), "grin")],
           appear=446.2, look=1)


def s41(c, t):  # 462.4 - 471.6  mesmo salário, gastos e demissão: diferença de patrimônio > R$ 22 mil
    show(c, t, 462.5, 960, 120, T("mesmo salário, mesmos gastos, mesma demissão", 54, DGRAY), anim="up")
    camila(c, t, 420, 1040, 0.75, [(0, "arms_up")], [(0, "grin")], appear=462.5, look=1)
    bruno(c, t, 1500, 1040, 0.75, [(0, "head")], [(0, "desperate")], appear=462.6, look=-1)
    show(c, t, 462.7, 420, 330, M("+R$ 7.390", 70, GREEN), anim="up")
    show(c, t, 462.8, 1500, 330, M("-R$ 15.423", 70, RED), anim="up")
    show(c, t, w("diferença", 466.5), 960, 480, T("diferença de patrimônio", 54, DGRAY), anim="fade")
    show(c, t, w("vinte", 469.5), 960, 620, lambda c: hl(c, "+ de R$ 22 mil", 0, 0, 100, LYELLOW), anim="stamp")


def s42(c, t):  # 471.6 - 480.9  a reserva não deixou rica: impediu que 8 meses virassem anos de dívida
    show(c, t, 471.7, 1150, 260, group(sc(strike(560), s=1.0), at(0, 0, M("deixar rica", 76, DGRAY))), anim="fade")
    show(c, t, w("impediu", 476.0), 1150, 440, T("impediu que 8 meses difíceis", 60, NAVY), anim="up")
    show(c, t, w("virassem", 477.8), 1150, 560, lambda c: hl(c, "virassem anos de dívida", 0, 0, 72, LGREEN, GREEN), anim="stamp")
    show(c, t, w("importante", 474.5), 1150, 790, sc(shield, GREEN, s=0.9), anim="pop")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("impediu", 476.0), "finger_up")], [(0, "neutral"), (w("impediu", 476.0), "confident")],
         appear=471.7, look=1)


def s43(c, t):  # 480.9 - 484.9  pra começar a sua: 3 atitudes práticas
    show(c, t, 481.0, 1150, 340, M("Pra começar a sua", 84, NAVY), anim="up")
    show(c, t, w("três", 482.5), 1150, 560, lambda c: hl(c, "3 atitudes práticas", 0, 0, 90, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "present"), (w("três", 482.5), "finger_up")], [(0, "happy"), (w("três", 482.5), "confident")],
         appear=481.0, look=1)


def s44(c, t):  # 484.9 - 496.4  1. descubra o custo de vida de verdade: extratos de 3 meses, some tudo
    step(c, t, 484.9, 1, "descubra seu custo de vida")
    for i in range(3):
        show(c, t, w("extratos", 488.0, 0.2 * i), 640 + i * 70, 480 + i * 30, sc(document, "EXTRATO", NAVY, 26, s=0.8), anim="drop")
    show(c, t, w("some", 491.0), 1300, 400, sc(calculator, "R$ ?", s=1.1), anim="pop")
    show(c, t, w("salário", 493.5), 1300, 680, group(sc(strike(260), s=1.0), at(0, 0, M("salário", 56, DGRAY))), anim="fade")
    show(c, t, w("meta", 494.5), 1300, 800, lambda c: hl(c, "o custo define a meta", 0, 0, 56, LYELLOW), anim="stamp")
    hero(c, t, 1680, 1050, 0.55, [(0, "present_l")], [(0, "happy")], appear=485.0, look=-1, prop=("r", prop_calculator))


def s45(c, t):  # 496.4 - 505.6  2. automatize: transferência no dia do salário
    step(c, t, 496.4, 2, "automatize")
    show(c, t, w("transferência", 498.5), 620, 480, group(sc(calendar, "5", BLUE, 70, s=1.2), at(0, 170, T("dia do salário", 48))),
         anim="drop")
    if t > w("transferência", 498.5, 0.5):
        arrow_draw(c, t, w("transferência", 498.5, 0.5), 820, 480, 1180, 480)
    show(c, t, w("reserva", 500.0), 1380, 480, group(sc(piggy, s=0.8), at(0, 170, T("reserva", 48, GREEN))), anim="pop")
    show(c, t, w("sobra", 503.0), 1000, 800, T("o que sobra no fim do mês quase nunca sobra", 54, RED), anim="fade")
    hero(c, t, 260, 1050, 0.6, [(0, "point_r")], [(0, "confident")], appear=496.5, look=1)


def s46(c, t):  # 505.6 - 515.5  3. comece pela meta de 1 mês; depois 3; depois 6
    step(c, t, 505.6, 3, "comece pela meta de 1 mês")
    stairs = [(w("meta", 506.5), "1 mês", 0), (w("três", 513.0), "3 meses", 1), (w("seis", 514.4), "6 meses", 2)]
    for t0, lab, i in stairs:
        x, top = 760 + i * 300, 760 - i * 150
        show(c, t, t0, x, top + (920 - top) / 2, lambda c, h=920 - top: (rrect(c, -140, -h / 2, 280, h, 10), fs(c, LGREEN, 5)),
             anim="up")
        show(c, t, t0 + 0.1, x, top - 50, M(lab, 56, GREEN), anim="stamp")
    show(c, t, w("dorme", 511.5), 760, 450, T("já muda o seu sono", 48, DGRAY), anim="fade")
    hero(c, t, 330, 1040, 0.85, [(0, "present"), (w("seis", 514.4), "arms_up")], [(0, "happy"), (w("seis", 514.4), "grin")],
         appear=505.7, look=1)


def s47(c, t):  # 515.5 - 526.6  reserva é pra emergência: emprego, saúde, conserto; Black Friday não é
    show(c, t, 515.6, 1150, 130, M("Reserva é pra emergência", 72, NAVY), anim="up")
    rows = [(w("perder", 519.0), "perder o emprego"), (w("saúde", 520.5), "um problema de saúde"),
            (w("conserto", 521.5), "um conserto urgente")]
    for i, (t0, lab) in enumerate(rows):
        y = 300 + i * 130
        show(c, t, t0, 820, y, sc(check_icon, 34, s=1.0), anim="pop")
        show(c, t, t0 + 0.1, 900, y, L(lab, 56), anim="left")
    show(c, t, w("black", 523.5), 820, 720, sc(x_icon, 34, s=1.0), anim="pop")
    show(c, t, w("black", 523.5, 0.1), 900, 720, L("promoção de Black Friday", 56, RED), anim="left")
    hero(c, t, 330, 1040, 0.95, [(0, "finger_up"), (w("black", 523.5), "shrug")], [(0, "confident"), (w("black", 523.5), "grin")],
         appear=515.6, look=1)


def s48(c, t):  # 526.6 - 548.8  recapitulando
    show(c, t, 526.7, 960, 120, M("Recapitulando", 74, NAVY), anim="up")
    rows = [(w("um", 527.5), "1 em cada 4 desempregados procura há mais de 1 ano", NAVY),
            (w("seguro", 531.5), "seguro: no máximo R$ 2.518, por até 5 meses", BLUE),
            (w("reserva", 537.5), "reserva: 3 a 6 meses do custo de vida", GREEN),
            (w("transformar", 541.5), "sem reserva: R$ 13 mil viram ~R$ 39 mil pagos", RED)]
    for i, (t0, lab, col) in enumerate(rows):
        y = 290 + i * 150
        show(c, t, t0, 610, y, lambda c, n=i + 1, col=col: (circle(c, 0, 0, 34, col, 5),
                                                         text(c, str(n), 0, 2, 44, MARKER, WHITE)), anim="pop")
        show(c, t, t0 + 0.1, 670, y, L(lab, 50, INK), anim="left")
    hero(c, t, 300, 1040, 0.8, [(0, "present")], [(0, "happy")], appear=526.7, look=1)


def s49(c, t):  # 548.8 - END  comentários + inscreva-se
    show(c, t, 548.9, 1080, 400, lambda c: speech(c, 1000, 300, -360, 190), anim="pop")
    show(c, t, 549.1, 1080, 340, T("Me conta nos comentários:", 52, DGRAY), anim="fade")
    show(c, t, w("quantos", 550.0), 1080, 430, M("quantos meses você aguentaria?", 52, NAVY), anim="fade")
    show(c, t, w("inscreve", 554.0), 1080, 700, sc(subscribe_btn, s=1.0), anim="pop")
    hero(c, t, 340, 1010, 1.1, [(0, "wave")], [(0, "happy")], appear=548.9, look=1)
    show(c, t, 549.1, 1080, 900, T("conteúdo educativo, não é recomendação de investimento", 36, DGRAY), anim="fade")


def s50(c, t):  # END - fim (5 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres: vídeo à esquerda (x 170-950, y 300-740) e inscrever-se à direita (~1450, 520).
    show(c, t, END + 0.1, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, END + 0.4, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, END + 0.4, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (END + 2.5, "relax")], [(0, "happy")], appear=END + 0.1)


SCENES = [
    (0.0, 4.7, s01), (4.7, 14.8, s02), (14.8, 25.9, s03), (25.9, 37.2, s04), (37.2, 48.8, s05),
    (48.8, 58.8, s06), (58.8, 71.3, s07), (71.3, 80.2, s08), (80.2, 87.2, s09), (87.2, 99.9, s10),
    (99.9, 114.1, s11), (114.1, 120.6, s12), (120.6, 135.3, s13), (135.3, 145.6, s14), (145.6, 160.9, s15),
    (160.9, 177.2, s16), (177.2, 183.9, s17), (183.9, 194.6, s18), (194.6, 200.5, s19), (200.5, 210.3, s20),
    (210.3, 227.4, s21), (227.4, 238.8, s22), (238.8, 255.4, s23), (255.4, 262.3, s24), (262.3, 276.6, s25),
    (276.6, 281.9, s26), (281.9, 289.0, s27), (289.0, 299.0, s28), (299.0, 315.7, s29), (315.7, 324.6, s30),
    (324.6, 339.2, s31), (339.2, 347.9, s32), (347.9, 356.4, s33), (356.4, 373.7, s34), (373.7, 385.5, s35),
    (385.5, 401.8, s36), (401.8, 411.1, s37), (411.1, 429.9, s38), (429.9, 446.1, s39), (446.1, 462.4, s40),
    (462.4, 471.6, s41), (471.6, 480.9, s42), (480.9, 484.9, s43), (484.9, 496.4, s44), (496.4, 505.6, s45),
    (505.6, 515.5, s46), (515.5, 526.6, s47), (526.6, 548.8, s48), (548.8, END, s49), (END, 999.0, s50),
]

# só toques pontuais, sem ruído: teto R$ 2.518 / 3 anos e 4 meses / dívida R$ 15.423 / Camila R$ 7.390
SFX = [(w("dois", 106.5), "tum"), (w("três", 225.2), "tum"), (w("quinze", 397.5), "tum"), (w("sete", 456.0), "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key")
