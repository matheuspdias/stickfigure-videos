"""Amortizar o financiamento ou investir? A conta completa (Faz a Conta, vídeo longo 16:9).
Narração Calm Carlos (HeyGen, ElevenLabs v4), 3 blocos, 0,4 s entre blocos.
Tempos absolutos: bloco1 0,000 | bloco2 167,636 | bloco3 323,125 | fim da fala 576,565 | +5 s de tela final.
Premissas (04/11/2026): imóvel R$ 300 mil, entrada 20%, R$ 240 mil em 360 meses SAC, MCMV faixa 3 7,66% a.a. + TR
(0,165% a.m., ~2% a.a.) = ~9,81% a.a.; investimento 10% a.a. líquido; poupança ~8,3%; CDB 100% CDI ~11,6% líquido;
financiamento comum ~11,5% a.a. + TR = ~13,7%. Contas em contas.py."""
import json
import os

from engine import *  # noqa

O2, O3 = 167.636, 323.125
END = 576.565

_PAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras.json"), encoding="utf-8"))


def w(word, after=0.0, d=0.0):
    """início (s) da primeira palavra que começa com `word` depois de `after` (tempo absoluto), mais d"""
    word = word.lower()
    for p in _PAL:
        if p["t0"] >= after - 0.01 and p["w"].lower().strip(",.:?!\"").startswith(word):
            return p["t0"] + d
    raise KeyError((word, after))


PINKISH = (1, 0.8, 0.76)
CARC = PURPLE   # Carla
DIEC = BLUE     # Diego


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def row(label, val, vcol=INK, wd=760, size=54):
    """linha de extrato: rótulo à esquerda, valor à direita (centrada em 0)"""
    def f(c):
        text(c, label, -wd / 2, 0, size, HAND, DGRAY, align="l")
        text(c, val, wd / 2, 0, size + 4, MARKER, vcol, align="r")
    return f


def tag(s, col, size=54):
    def f(c):
        wd = text_w(c, s, size) + 44
        rrect(c, -wd / 2, -size * 0.7, wd, size * 1.4, 14); fs(c, col, 5)
        text(c, s, 0, 2, size, MARKER, WHITE)
    return f


def panel(wd, h, col=WHITE, lw=5):
    def f(c):
        rrect(c, -wd / 2, -h / 2, wd, h, 22); fs(c, col, lw)
    return f


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def step(c, t, t0, num, head, col=LYELLOW):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"{num}. {head}", 0, 0, 66, col), anim="stamp")


def money_bar(c, t, t0, x, base, h, wd, col, top, label, d=0.9, tsize=56, lsize=42, tcol=None):
    k = grow(t, t0, d)
    if t < t0:
        return
    c.save(); c.translate(x, base)
    bar(c, max(4, h * k), wd, col)
    c.restore()
    if k > 0.6:
        if top:
            text(c, top, x, base - h * k - 42, tsize, MARKER, tcol or col)
        if label:
            text(c, label, x, base + 46, lsize, HAND, DGRAY)


def carla(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", CARC); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def diego(c, t, x, y, s, poses, exprs, **kw):
    other(c, t, x, y, s, poses, exprs, **kw)


def name_tag(s, col, size=46):
    return tag(s, col, size)


def saldo_bar(c, x, y, wd, h, k, col=RED, label=None):
    """barra horizontal de saldo devedor: k de 0 a 1 (fração restante)"""
    rrect(c, x, y, wd, h, 12); fs(c, WHITE, 5)
    if k > 0.005:
        rrect(c, x, y, wd * k, h, 12); fs(c, col, 5)
    if label:
        text(c, label, x + wd / 2, y + h + 40, 40, HAND, DGRAY)


def timeline(c, t, t0, x0, x1, y, years_cut=None, cut_t=None):
    """linha do tempo de 30 anos; years_cut marca a quitação"""
    k = grow(t, t0, 0.8)
    if t < t0:
        return
    xe = x0 + (x1 - x0) * k
    rrect(c, x0, y - 22, xe - x0, 44, 20); fs(c, LGRAY, 5)
    for yr in (0, 10, 20, 30):
        xx = x0 + (x1 - x0) * yr / 30
        if xx <= xe + 1:
            line(c, xx, y + 26, xx, y + 46, 5)
            text(c, f"{yr}", xx, y + 82, 40, MARKER, DGRAY)
    text(c, "anos", x1 + 70, y + 82, 38, HAND, DGRAY)
    if years_cut is not None and cut_t is not None and t >= cut_t:
        kk = grow(t, cut_t, 1.0)
        xc = x0 + (x1 - x0) * years_cut / 30 * kk
        rrect(c, x0, y - 22, xc - x0, 44, 20); fs(c, CARC, 5)


def doc_contract(c):
    document(c, "CONTRATO", NAVY, 22)


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 11.7  sobrou R$ 300; financiamento; amortizar ou investir?
    show(c, t, 0.05, 520, 200, lambda c: hl(c, "Sobrou R$ 300", 0, 0, 96, LGREEN, GREEN), anim="stamp", d=0.35)
    show(c, t, w("financiamento"), 520, 640, group(sc(house, True, s=1.0), at(0, 200, T("financiamento do imóvel", 46, DGRAY))),
         anim="pop")
    show(c, t, w("amortizar"), 1060, 360, group(sc(brick, s=0.9), at(0, 110, M("AMORTIZAR?", 60, NAVY))), anim="pop")
    show(c, t, w("ou", 10.3), 1060, 560, M("ou", 56, DGRAY), anim="fade")
    show(c, t, w("investir"), 1060, 760, group(sc(piggy, s=0.7), at(0, 140, M("INVESTIR?", 60, GREEN))), anim="pop")
    hero(c, t, 1620, 1050, 0.95, [(0, "relax"), (w("amortizar"), "think")], [(0, "happy"), (w("amortizar"), "think")],
         appear=0.05, look=-1)


def s02(c, t):  # 11.7 - 29.4  pergunta dos comentários; quem decide é um número do contrato
    show(c, t, 11.8, 560, 290, lambda c: speech(c, 820, 230, -250, 150), anim="pop")
    show(c, t, 12.0, 560, 270, T("amortizo ou invisto??", 60, NAVY), anim="fade")
    show(c, t, w("alugar"), 560, 640, sc(video_card, "Alugar ou comprar?", None, s=0.62,
                                         icon=sc(apartment, LYELLOW, "ALUGA-SE", 3, s=0.55)), anim="pop")
    show(c, t, w("opinião"), 1180, 300, M("não é opinião", 54, RED), anim="pop")
    show(c, t, w("gerente"), 1180, 380, M("nem o gerente", 54, RED), anim="pop")
    show(c, t, w("único", 25.0), 1180, 610, sc(doc_contract, s=1.5), anim="pop")
    show(c, t, w("único", 25.0, 0.3), 1180, 820, lambda c: hl(c, "1 número do contrato", 0, 0, 56, LYELLOW), anim="stamp")
    hero(c, t, 1660, 1050, 0.85, [(0, "present_l"), (w("opinião"), "finger_up"), (w("único", 25.0), "point_l")],
         [(0, "neutral"), (w("opinião"), "confident")], appear=11.8, look=-1)


def s03(c, t):  # 29.4 - 49.0  Carla e Diego: mesmo apê, mesmo financiamento, mesmos R$ 300
    show(c, t, 29.5, 960, 130, M("A conta completa, com duas pessoas", 66, NAVY), anim="up")
    carla(c, t, 380, 900, 0.75, [(0, "wave"), (w("amortiza", 41.0), "hold")], [(0, "happy")], appear=w("carla", 33.0), look=0.5)
    diego(c, t, 1080, 900, 0.75, [(0, "wave"), (w("investe", 43.0), "thumb")], [(0, "happy")], appear=w("diego", 34.0), look=-0.5)
    show(c, t, w("carla", 33.0), 380, 960, name_tag("CARLA", CARC), anim="pop")
    show(c, t, w("diego", 34.0), 1080, 960, name_tag("DIEGO", DIEC), anim="pop")
    show(c, t, w("apartamento", 35.5), 730, 560, sc(apartment, LYELLOW, None, 4, s=0.8), anim="drop")
    show(c, t, w("apartamento", 35.5, 0.2), 730, 610, T("mesmo apê", 42, DGRAY), anim="fade")
    show(c, t, w("financiamento", 37.0), 730, 670, T("mesmo financiamento", 42, DGRAY), anim="fade")
    show(c, t, w("trezentos", 39.0), 730, 740, M("mesmos R$ 300", 50, GREEN), anim="pop")
    show(c, t, w("amortiza", 41.0), 380, 330, lambda c: hl(c, "AMORTIZA", 0, 0, 60, PINKISH, CARC), anim="stamp")
    show(c, t, w("investe", 43.0), 1080, 330, lambda c: hl(c, "INVESTE", 0, 0, 60, LBLUE, DIEC), anim="stamp")
    show(c, t, w("trinta", 45.0), 1340, 640, group(sc(finish_flag, 160, s=0.9), at(0, 50, T("daqui a 30 anos", 42, DGRAY))), anim="pop")
    hero(c, t, 1640, 1050, 0.75, [(0, "present_l"), (w("dinheiro", 47.5), "think")], [(0, "happy"), (w("dinheiro", 47.5), "think")],
         appear=29.5, look=-1)


def s04(c, t):  # 49.0 - 66.1  cenário: R$ 300 mil, MCMV faixa 3, entrada R$ 60 mil, R$ 240 mil em 30 anos, SAC
    show(c, t, 49.1, 960, 130, M("O cenário", 76, NAVY), anim="up")
    show(c, t, w("apartamento", 50.5), 400, 700, sc(apartment, LYELLOW, None, 5, s=1.15), anim="drop")
    show(c, t, w("trezentos", 51.5), 400, 300, sc(price_tag, "R$ 300 mil", LYELLOW, 52, s=1.0), anim="pop")
    show(c, t, w("minha", 53.0), 400, 800, T("Minha Casa Minha Vida, faixa 3", 42, DGRAY), anim="fade")
    rows_ = [(w("entrada", 56.5), "entrada (20%)", "R$ 60 mil", NAVY),
             (w("duzentos", 59.5), "financiado", "R$ 240 mil", RED),
             (w("trinta", 62.0), "prazo", "30 anos", INK),
             (w("sac", 63.5), "tabela", "SAC", INK)]
    for i, (t0, lab, val, col) in enumerate(rows_):
        show(c, t, t0, 1040, 330 + i * 120, row(lab, val, col, wd=620, size=52), anim="left")
    show(c, t, w("comum", 64.5), 1040, 830, T("(a mais comum no Brasil)", 42, DGRAY), anim="fade")
    hero(c, t, 1680, 1050, 0.62, [(0, "present_l")], [(0, "neutral")], appear=49.1, look=-1, prop=("r", prop_calculator))


def s05(c, t):  # 66.1 - 82.5  7,66% ao ano (FGTS) + TR corrigindo o saldo todo mês
    show(c, t, 66.2, 960, 130, M("Os juros", 76, NAVY), anim="up")
    show(c, t, w("sete", 68.0), 520, 380, lambda c: hl(c, "7,66% ao ano", 0, 0, 96, LYELLOW), anim="stamp")
    show(c, t, w("fgts", 71.0), 520, 500, T("faixa 3, pra quem tem FGTS", 46, DGRAY), anim="fade")
    show(c, t, w("detalhe", 73.0), 520, 650, M("+ TR", 120, RED), anim="stamp")
    show(c, t, w("saldo", 77.2), 1160, 420, lambda c: saldo_bar(c, -230, -30, 460, 60, 0.85 + 0.05 * min(1, max(0, (t - 78.4) / 2)),
                                                                RED, "saldo da dívida"), anim="pop")
    show(c, t, w("corrigido", 78.3), 1160, 300, T("corrigido todo mês", 50, RED), anim="fade")
    show(c, t, w("referencial"), 520, 760, T("taxa referencial", 46, DGRAY), anim="fade")
    hero(c, t, 1620, 1050, 0.85, [(0, "present_l"), (w("detalhe", 73.0), "finger_up")],
         [(0, "neutral"), (w("detalhe", 73.0), "think")], appear=66.2, look=-1)


def s06(c, t):  # 82.5 - 94.1  TR 2026: 0,16% a 0,17% ao mês; parece pouco; ~2% ao ano
    show(c, t, 82.6, 960, 130, M("A TR em 2026", 72, NAVY), anim="up")
    show(c, t, w("zero", 85.0), 620, 380, M("0,16% a 0,17%", 96, RED), anim="stamp")
    show(c, t, w("mês", 88.9), 620, 480, T("ao mês", 52, DGRAY), anim="fade")
    show(c, t, w("parece", 89.6), 620, 600, T("parece pouco...", 52, DGRAY), anim="fade")
    show(c, t, w("dois", 92.3), 620, 760, lambda c: hl(c, "~2% a mais por ano", 0, 0, 80, PINKISH, RED), anim="stamp")
    hero(c, t, 1500, 1050, 1.0, [(0, "present_l"), (w("parece", 89.6), "shrug"), (w("dois", 92.3), "point_l")],
         [(0, "neutral"), (w("parece", 89.6), "neutral"), (w("dois", 92.3), "worried")], appear=82.6, look=-1)


def s07(c, t):  # 94.1 - 104.3  custo de verdade ~9,8% ao ano; a chave do vídeo
    show(c, t, 94.2, 960, 130, M("O custo de verdade", 76, NAVY), anim="up")
    show(c, t, 94.3, 330, 400, M("7,66%", 76, INK), anim="pop")
    show(c, t, 94.5, 520, 400, M("+", 76, INK), anim="pop")
    show(c, t, 94.7, 700, 400, M("TR", 76, RED), anim="pop")
    show(c, t, w("custo", 95.3), 860, 400, sc(eq, 50), anim="pop")
    show(c, t, w("nove", 98.2), 600, 640, lambda c: hl(c, "~9,8% ao ano", 0, 0, 120, LYELLOW, NAVY), anim="stamp")
    show(c, t, w("chave", 102.4), 1260, 420, sc(house_key, GOLD, s=1.2), anim="pop", rot=-0.3)
    show(c, t, w("chave", 102.4, 0.2), 1260, 580, T("a chave do vídeo", 50, DGRAY), anim="fade")
    hero(c, t, 1640, 1050, 0.95, [(0, "present_l"), (w("guarda", 100.9), "finger_up")],
         [(0, "neutral"), (w("guarda", 100.9), "confident")], appear=94.2, look=-1)


def s08(c, t):  # 104.3 - 126.5  1ª parcela R$ 2.150; devolve R$ 657 mil; R$ 417 mil de juros e TR
    show(c, t, 104.4, 960, 130, M("Sem amortizar", 76, NAVY), anim="up")
    show(c, t, w("primeira", 105.4), 1250, 260, row("1ª parcela", "~R$ 2.150", NAVY, wd=560, size=50), anim="left")
    money_bar(c, t, w("duzentos", 116.6), 360, 960, 240 * 0.82, 200, NAVY, "R$ 240 mil", "emprestado", d=0.7)
    money_bar(c, t, w("seiscentos", 113.1), 680, 960, 657 * 0.82, 200, RED, "R$ 657 mil", "devolvido", d=1.0, tsize=64)
    show(c, t, w("três", 120.0), 1180, 440, M("quase 3x", 90, RED), anim="stamp")
    show(c, t, w("juros", 122.1), 1180, 600, T("só de juros e TR:", 50, DGRAY), anim="fade")
    show(c, t, w("quatrocentos", 123.4), 1180, 700, lambda c: hl(c, "R$ 417 mil", 0, 0, 90, PINKISH, RED), anim="stamp")
    hero(c, t, 1700, 1050, 0.6, [(0, "present_l"), (w("três", 120.0), "head")], [(0, "neutral"), (w("três", 120.0), "shocked")],
         appear=104.4, look=-1)


def s09(c, t):  # 126.5 - 142.4  o que é amortizar: extra direto no saldo; nunca mais paga juros nem TR
    show(c, t, 126.6, 960, 130, M("O que é amortizar?", 76, NAVY), anim="up")
    k = 0.8 - 0.25 * grow(t, w("abate", 135.5), 1.0)
    show(c, t, w("saldo", 131.3), 700, 450, lambda c: saldo_bar(c, -400, -35, 800, 70, k, RED, "saldo da dívida"), anim="pop")
    show(c, t, w("extra", 129.7), 300, 300, group(sc(bills, 2, s=0.8), at(0, 90, M("+ extra", 50, GREEN))), anim="drop")
    arrow_draw(c, t, w("direto", 130.6), 380, 330, 560, 410)
    show(c, t, w("não", 132.8), 700, 640, T("não paga juros, não paga parcela futura", 48, DGRAY), anim="fade")
    show(c, t, w("abate", 135.8), 700, 720, M("abate o que você deve", 60, NAVY), anim="pop")
    show(c, t, w("nunca", 139.5), 700, 860, lambda c: hl(c, "nunca mais paga juros nem TR", 0, 0, 58, LGREEN, GREEN), anim="stamp")
    hero(c, t, 1600, 1050, 0.95, [(0, "think"), (w("pagar", 129.0), "present_l"), (w("nunca", 139.5), "thumb")],
         [(0, "think"), (w("pagar", 129.0), "neutral"), (w("nunca", 139.5), "happy")], appear=126.6, look=-1)


def s10(c, t):  # 142.4 - 150.7  prazo ou parcela? reduzir o prazo economiza mais
    show(c, t, 142.5, 760, 160, M("O banco pergunta:", 70, NAVY), anim="up")
    show(c, t, w("prazo", 145.6), 480, 420, panel(420, 200, LBLUE), anim="pop")
    show(c, t, w("prazo", 145.6), 480, 420, M("PRAZO", 80, NAVY), anim="pop")
    show(c, t, w("parcela", 146.5), 1040, 420, panel(420, 200, WHITE), anim="pop")
    show(c, t, w("parcela", 146.5), 1040, 420, M("PARCELA", 80, NAVY), anim="pop")
    show(c, t, w("ou", 146.3), 760, 420, T("ou", 56, DGRAY), anim="fade")
    show(c, t, w("economiza", 149.4), 480, 600, sc(check_icon, 50), anim="stamp")
    show(c, t, w("economiza", 149.4, 0.2), 480, 720, T("quase sempre economiza mais", 46, GREEN), anim="fade")
    hero(c, t, 1620, 1050, 0.95, [(0, "think"), (w("reduzir", 147.6), "point_l")], [(0, "think"), (w("reduzir", 147.6), "confident")],
         appear=142.5, look=-1)


def s11(c, t):  # 150.7 - O2  R$ 10 mil no 1º mês: prazo -R$ 37 mil x parcela -R$ 17 mil; a Carla reduz o prazo
    show(c, t, 150.8, 760, 130, M("R$ 10 mil amortizados no 1º mês", 64, NAVY), anim="up")
    money_bar(c, t, w("prazo", 155.6), 420, 900, 37 * 12, 210, GREEN, "- R$ 37 mil", "reduzindo o PRAZO", d=0.8, tsize=64)
    money_bar(c, t, w("parcela", 159.8), 820, 900, 17 * 12, 210, GRAY, "- R$ 17 mil", "reduzindo a PARCELA", d=0.8, tcol=DGRAY)
    show(c, t, w("metade", 162.6), 1260, 480, M("menos da metade", 58, RED), anim="pop")
    show(c, t, w("carla", 165.3), 1260, 640, lambda c: hl(c, "a Carla reduz o prazo", 0, 0, 52, PINKISH, CARC), anim="stamp")
    carla(c, t, 1420, 1040, 0.5, [(0, "thumb")], [(0, "happy")], appear=w("carla", 165.3), look=-1)
    hero(c, t, 1720, 1050, 0.6, [(0, "present_l"), (w("metade", 162.6), "point_l")], [(0, "neutral"), (w("metade", 162.6), "confident")],
         appear=150.8, look=-1)


# ======================================================================= BLOCO 2
def s12(c, t):  # O2 - 190.0  o plano da Carla: parcela normal + R$ 300; o que sobra vai pro saldo
    show(c, t, O2 + 0.1, 960, 130, M("O plano da Carla", 76, CARC), anim="up")
    carla(c, t, 330, 1000, 0.95, [(0, "present"), (w("regra", 176.0), "point_ru")], [(0, "confident")], appear=O2 + 0.1, look=0.6)
    show(c, t, w("financiou", 169.5), 960, 290, T("R$ 240 mil em 30 anos   |   sobram R$ 300 por mês", 50, DGRAY), anim="fade")
    show(c, t, w("simples", 177.0), 960, 420, T("todo mês ela paga:", 54, DGRAY), anim="fade")
    show(c, t, w("parcela", 179.5), 740, 540, lambda c: hl(c, "parcela normal", 0, 0, 70, WHITE, NAVY), anim="pop")
    show(c, t, w("trezentos", 181.8), 1250, 540, lambda c: hl(c, "+ R$ 300", 0, 0, 74, LGREEN, GREEN), anim="stamp")
    show(c, t, w("encolhe", 184.5), 1000, 720, T("a dívida encolhe mais rápido, os juros também", 48, DGRAY), anim="fade")
    show(c, t, w("sobra", 188.3), 1000, 830, M("o que sobra vai pro saldo", 56, CARC), anim="pop")
    hero(c, t, 1720, 1050, 0.6, [(0, "present_l")], [(0, "neutral")], appear=O2 + 0.1, look=-1, prop=("r", prop_calculator))


def s13(c, t):  # 190.0 - 198.2  quita em 16 anos e 11 meses: 13 anos antes do prazo
    show(c, t, 190.1, 960, 130, M("O resultado assusta", 76, NAVY), anim="up")
    timeline(c, t, 190.3, 230, 1330, 760, years_cut=16.92, cut_t=w("dezesseis", 193.0))
    show(c, t, w("dezesseis", 193.0), 840, 320, lambda c: hl(c, "quitado em 16 anos e 11 meses", 0, 0, 62, PINKISH, CARC),
         anim="stamp")
    show(c, t, w("treze", 195.5), 840, 470, M("13 ANOS ANTES", 110, GREEN), anim="stamp")
    show(c, t, w("dezesseis", 193.5), 230 + 1100 * 16.92 / 30, 650, sc(house_key, GOLD, s=0.7), anim="drop")
    carla(c, t, 1560, 1050, 0.8, [(0, "stand"), (w("treze", 195.5), "arms_up")], [(0, "happy"), (w("treze", 195.5), "grin")],
          appear=190.1, look=-1)


def s14(c, t):  # 198.2 - 211.6  devolve R$ 471 mil x R$ 657 mil: R$ 186 mil a menos de juros (cena do gancho "treze-anos")
    show(c, t, 198.3, 760, 130, M("No total, ela devolve ao banco", 64, NAVY), anim="up")
    money_bar(c, t, w("quatrocentos", 200.0), 380, 960, 471 * 0.9, 210, CARC, "R$ 471 mil", "Carla", d=0.9, tsize=62)
    money_bar(c, t, w("seiscentos", 203.0), 720, 960, 657 * 0.9, 210, LGRAY, "R$ 657 mil", "sem amortizar", d=0.7, tcol=DGRAY)
    show(c, t, w("cento", 205.8), 1210, 420, lambda c: hl(c, "- R$ 186 mil", 0, 0, 100, LGREEN, GREEN), anim="stamp")
    show(c, t, w("cento", 205.8, 0.3), 1210, 540, T("de juros", 56, DGRAY), anim="fade")
    show(c, t, w("só", 209.3), 1210, 680, M("com só R$ 300/mês", 58, NAVY), anim="pop")
    show(c, t, w("só", 209.3), 1210, 790, T("e 13 anos antes", 50, CARC), anim="fade")
    hero(c, t, 1690, 1050, 0.6, [(0, "present_l"), (w("cento", 205.8), "arms_up")], [(0, "neutral"), (w("cento", 205.8), "shocked")],
         appear=198.3, look=-1)


def s15(c, t):  # 211.6 - 217.3  parece óbvio? calma: agora vem o Diego
    show(c, t, 211.7, 700, 360, M("amortizar = melhor negócio?", 72, NAVY), anim="pop")
    show(c, t, w("calma", 214.8), 700, 520, lambda c: hl(c, "Calma.", 0, 0, 100, LYELLOW), anim="stamp")
    diego(c, t, 1100, 960, 0.85, [(0, "wave")], [(0, "happy")], appear=w("diego", 215.7), look=-1)
    show(c, t, w("diego", 215.7), 1100, 1010, name_tag("DIEGO", DIEC), anim="pop")
    hero(c, t, 450, 1050, 0.9, [(0, "think"), (w("calma", 214.8), "hips")], [(0, "think"), (w("calma", 214.8), "confident")],
         appear=211.7, look=1)


def s16(c, t):  # 217.3 - 232.9  Diego: parcela normal e investe R$ 300 a 10% ao ano líquido
    show(c, t, 217.4, 960, 130, M("O plano do Diego", 76, DIEC), anim="up")
    diego(c, t, 330, 1000, 0.95, [(0, "present"), (w("investe", 225.3), "hold")], [(0, "confident")], appear=217.4, look=0.6)
    show(c, t, w("parcela", 224.0), 690, 330, lambda c: hl(c, "parcela normal", 0, 0, 60, WHITE, NAVY), anim="pop")
    show(c, t, w("investe", 225.3), 1260, 330, lambda c: hl(c, "+ investe R$ 300", 0, 0, 60, LGREEN, GREEN), anim="stamp")
    show(c, t, w("renda", 227.9), 860, 600, sc(bank, s=0.9), anim="pop")
    show(c, t, w("dez", 229.2), 1220, 560, M("10% ao ano", 84, GREEN), anim="stamp")
    show(c, t, w("descontado", 230.9), 1220, 660, T("já sem imposto de renda", 48, DGRAY), anim="fade")
    show(c, t, w("premissa", 233.3), 1020, 820, T("a mesma premissa pé no chão do canal", 46, DGRAY), anim="fade")
    hero(c, t, 1720, 1050, 0.6, [(0, "present_l")], [(0, "neutral")], appear=217.4, look=-1)


def s17(c, t):  # 236.5 - 243.4  Selic 13,75% hoje, mas juro alto não dura 30 anos
    show(c, t, 236.6, 960, 130, M("Por que 10%?", 72, NAVY), anim="up")
    show(c, t, w("selic", 236.6), 520, 330, T("Selic hoje", 52, DGRAY), anim="fade")
    show(c, t, w("treze", 237.7), 520, 440, M("13,75%", 110, NAVY), anim="stamp")
    show(c, t, w("juro", 240.5), 760, 640, T("juro alto assim não dura 30 anos", 60, RED), anim="up")
    show(c, t, w("juro", 240.5, 0.5), 1120, 440, lambda c: clock(c, t), anim="pop")
    hero(c, t, 1640, 1050, 0.95, [(0, "present_l"), (w("juro", 240.5), "shrug")], [(0, "neutral"), (w("juro", 240.5), "worried")],
         appear=236.6, look=-1)


def s18(c, t):  # 243.4 - 252.2  regra justa: os dois gastam o mesmo todo mês; quem tiver mais em 30 anos ganha
    show(c, t, 243.5, 960, 130, M("A regra é justa", 76, NAVY), anim="up")
    show(c, t, w("gastam", 245.0), 680, 560, sc(balance, 0.0,
                                                lambda c: carla(c, 1.0, 0, 0, 0.32, [(0, "stand")], [(0, "happy")]),
                                                lambda c: diego(c, 1.0, 0, 0, 0.32, [(0, "stand")], [(0, "happy")]), s=1.15), anim="pop")
    show(c, t, w("valor", 246.9), 680, 880, lambda c: hl(c, "mesmo valor por mês", 0, 0, 62, LYELLOW), anim="stamp")
    show(c, t, w("quem", 248.4), 1330, 520, group(sc(finish_flag, 200, s=0.8), at(0, 60, T("30 anos", 44, DGRAY))), anim="pop")
    show(c, t, w("ganha", 251.3), 1330, 700, M("quem tiver mais, ganha", 50, GREEN), anim="pop")
    hero(c, t, 1680, 1050, 0.6, [(0, "present_l")], [(0, "confident")], appear=243.5, look=-1)


def s19(c, t):  # 252.2 - 262.9  o dia em que a Carla quita: livre da dívida, nada investido
    show(c, t, 252.3, 960, 130, M("16 anos e 11 meses depois", 72, NAVY), anim="up")
    carla(c, t, 520, 980, 1.0, [(0, "arms_up")], [(0, "grin")], appear=252.3, look=0.5)
    show(c, t, w("livre", 259.7), 520, 320, lambda c: hl(c, "QUITADO!", 0, 0, 80, PINKISH, CARC), anim="stamp")
    show(c, t, w("livre", 259.7), 920, 640, sc(house_key, GOLD, s=0.9), anim="pop")
    show(c, t, w("nada", 261.4), 1180, 420, row("investido", "R$ 0", DGRAY, wd=480, size=56), anim="left")
    hero(c, t, 1680, 1050, 0.62, [(0, "present_l")], [(0, "happy")], appear=252.3, look=-1)


def s20(c, t):  # 262.9 - 271.6  Diego nesse dia: R$ 151 mil investidos, deve R$ 146 mil
    show(c, t, 263.0, 960, 130, M("E o Diego, nesse mesmo dia?", 70, DIEC), anim="up")
    diego(c, t, 330, 1000, 0.95, [(0, "think"), (w("cento", 265.5), "present")], [(0, "think"), (w("cento", 265.5), "happy")],
          appear=263.0, look=0.6)
    money_bar(c, t, w("cento", 265.5), 820, 900, 151 * 2.6, 220, GREEN, "R$ 151 mil", "investido", d=0.8, tsize=62)
    money_bar(c, t, w("deve", 268.7), 1180, 900, 146 * 2.6, 220, RED, "R$ 146 mil", "ainda deve", d=0.8, tsize=62)
    hero(c, t, 1690, 1050, 0.6, [(0, "present_l")], [(0, "think")], appear=263.0, look=-1)


def s21(c, t):  # 271.6 - 280.6  ele poderia sacar e quitar no mesmo dia; sobravam R$ 5 mil
    show(c, t, 271.7, 960, 130, M("Repara:", 76, NAVY), anim="up")
    show(c, t, w("sacava", 273.4), 420, 450, M("R$ 151 mil", 80, GREEN), anim="pop")
    show(c, t, w("quitava", 275.0), 700, 450, M("-", 80, INK), anim="pop")
    show(c, t, w("quitava", 275.0), 980, 450, M("R$ 146 mil", 80, RED), anim="pop")
    show(c, t, w("sobravam", 278.2), 700, 640, lambda c: hl(c, "= sobram R$ 5 mil", 0, 0, 84, LGREEN, GREEN), anim="stamp")
    show(c, t, w("mesmo", 276.4), 700, 820, T("e quitava no mesmo dia que a Carla", 52, DGRAY), anim="fade")
    diego(c, t, 1400, 1040, 0.6, [(0, "thumb")], [(0, "happy")], appear=271.7, look=-1)
    hero(c, t, 1700, 1050, 0.6, [(0, "point_l"), (w("sobravam", 278.2), "thumb")], [(0, "confident"), (w("sobravam", 278.2), "grin")],
         appear=271.7, look=-1)


def s22(c, t):  # 280.6 - 298.2  segunda metade: Carla investe ~R$ 2.100/mês; Diego segue parcela + R$ 300
    show(c, t, 280.7, 960, 130, M("A segunda metade da corrida", 70, NAVY), anim="up")
    carla(c, t, 320, 1000, 0.8, [(0, "present"), (w("investir", 290.5), "hold")], [(0, "happy")], appear=280.7, look=0.5)
    show(c, t, w("parcela", 284.0), 520, 330, M("sem parcela", 56, CARC), anim="pop")
    show(c, t, w("dois", 287.9), 620, 500, lambda c: hl(c, "investe ~R$ 2 .100/mês", 0, 0, 60, PINKISH, CARC), anim="stamp")
    show(c, t, w("investir", 290.5, 0.4), 620, 680, sc(piggy, s=0.7), anim="drop")
    diego(c, t, 1180, 1000, 0.8, [(0, "stand")], [(0, "neutral")], appear=w("diego", 293.0), look=-0.5)
    show(c, t, w("continua", 294.5), 1240, 330, M("parcela", 56, NAVY), anim="pop")
    show(c, t, w("trezentos", 296.8), 1240, 430, M("+ investe R$ 300", 52, GREEN), anim="pop")
    hero(c, t, 1720, 1050, 0.55, [(0, "present_l")], [(0, "neutral")], appear=280.7, look=-1)


def s23(c, t):  # 298.2 - 316.6  ano 30: Carla R$ 605 mil x Diego R$ 619 mil; R$ 14 mil, ~2%: empate (cena do gancho "carla-diego")
    show(c, t, 298.3, 960, 130, M("Ano 30: os dois com o apê quitado", 64, NAVY), anim="up")
    money_bar(c, t, w("seiscentos", 302.0), 360, 940, 605 * 0.85, 220, CARC, "R$ 605 mil", "Carla (amortizou)", d=0.9, tsize=58)
    money_bar(c, t, w("seiscentos", 305.9), 760, 940, 619 * 0.85, 220, DIEC, "R$ 619 mil", "Diego (investiu)", d=0.9, tsize=58)
    show(c, t, w("diferença", 307.9), 1270, 360, row("diferença", "R$ 14 mil", INK, wd=520, size=52), anim="left")
    show(c, t, w("pouco", 312.4), 1270, 460, T("pouco mais de 2%", 50, DGRAY), anim="fade")
    show(c, t, w("empate", 315.4), 1270, 610, lambda c: hl(c, "EMPATE", 0, 0, 110, LYELLOW, NAVY), anim="stamp")
    hero(c, t, 1690, 1050, 0.6, [(0, "present_l"), (w("empate", 315.4), "arms_up")], [(0, "neutral"), (w("empate", 315.4), "grin")],
         appear=298.3, look=-1)


def s24(c, t):  # 316.6 - O3  não é coincidência: tem uma explicação
    show(c, t, 316.7, 760, 380, M("não é coincidência", 84, NAVY), anim="pop")
    show(c, t, w("explicação", 318.7), 760, 620, sc(bulb, s=1.4), anim="pop")
    show(c, t, w("importante", 321.0), 760, 860, T("a parte mais importante do vídeo", 54, DGRAY), anim="fade")
    hero(c, t, 1500, 1050, 1.0, [(0, "finger_up")], [(0, "confident")], appear=316.7, look=-1)


# ======================================================================= BLOCO 3
def s25(c, t):  # O3 - 343.9  amortizar é um investimento que rende o juro do contrato: 9,8%, garantido, sem risco, sem IR
    show(c, t, O3 + 0.1, 760, 150, lambda c: hl(c, "Amortizar é um investimento", 0, 0, 74, LYELLOW), anim="stamp")
    show(c, t, w("exatamente", 326.0), 760, 270, T("e rende exatamente o juro do seu financiamento", 50, DGRAY), anim="fade")
    show(c, t, w("abate", 330.0), 400, 520, sc(brick, s=1.1), anim="drop")
    show(c, t, w("abate", 330.0, 0.2), 400, 640, T("R$ 1 abatido", 48, DGRAY), anim="fade")
    arrow_draw(c, t, w("nove", 332.0), 560, 520, 760, 520)
    show(c, t, w("nove", 337.5), 1020, 520, M("9,8% ao ano", 90, GREEN), anim="stamp")
    for i, (wd, lab) in enumerate((("garantido", "garantido"), ("risco", "sem risco"), ("imposto", "sem imposto de renda"))):
        t0 = w(wd, 339.0)
        show(c, t, t0, 380 + i * 380, 800, group(sc(check_icon, 34), at(0, 80, T(lab, 42, GREEN))), anim="pop")
    hero(c, t, 1640, 1050, 0.95, [(0, "present_l"), (w("garantido", 339.0), "thumb")],
         [(0, "confident"), (w("garantido", 339.0), "happy")], appear=O3 + 0.1, look=-1)


def s26(c, t):  # 343.9 - 359.0  Diego a 10%, um pouquinho acima; a 9,8%, empate centavo por centavo
    show(c, t, 344.0, 960, 130, M("Por isso deu quase empate", 70, NAVY), anim="up")
    show(c, t, w("dez", 344.9), 420, 400, group(T("Diego investiu a", 46, DIEC), at(0, 90, M("10%", 100, DIEC))), anim="pop")
    show(c, t, w("pouquinho", 346.0), 760, 420, M(">", 100, INK), anim="pop")
    show(c, t, w("pouquinho", 346.0), 1100, 400, group(T("amortizar rende", 46, CARC), at(0, 90, M("9,8%", 100, CARC))), anim="pop")
    show(c, t, w("ganhou", 348.0), 760, 610, T("ele ganhou por pouquinho", 54, DGRAY), anim="fade")
    show(c, t, w("nove", 352.0), 760, 760, lambda c: hl(c, "a 9,8%: empate", 0, 0, 74, LYELLOW), anim="stamp")
    show(c, t, w("centavo", 357.0), 760, 880, T("centavo por centavo", 52, NAVY), anim="fade")
    hero(c, t, 1660, 1050, 0.85, [(0, "present_l"), (w("nove", 352.0), "finger_up")], [(0, "neutral"), (w("nove", 352.0), "confident")],
         appear=344.0, look=-1)


def s27(c, t):  # 359.0 - 377.1  a regra: compare dois números (cena do gancho "regra-contrato")
    show(c, t, 359.1, 960, 130, lambda c: hl(c, "A regra: compare 2 números", 0, 0, 74, LYELLOW), anim="stamp")
    show(c, t, w("custo", 363.0), 470, 360, panel(560, 230, PINKISH), anim="pop")
    show(c, t, w("custo", 363.0), 470, 320, M("custo da dívida", 56, RED), anim="pop")
    show(c, t, w("juros", 365.5), 470, 400, T("juros + TR", 50, DGRAY), anim="fade")
    show(c, t, w("quanto", 367.6), 1110, 360, panel(560, 230, LGREEN), anim="pop")
    show(c, t, w("quanto", 367.6), 1110, 320, M("rendimento", 56, GREEN), anim="pop")
    show(c, t, w("descontado", 369.9), 1110, 400, T("já sem imposto", 50, DGRAY), anim="fade")
    show(c, t, w("amortize", 373.2), 560, 640, L("dívida custa mais  =  AMORTIZE", 54, CARC, MARKER), anim="left")
    show(c, t, w("invista", 376.2), 560, 760, L("investimento rende mais  =  INVISTA", 54, DIEC, MARKER), anim="left")
    show(c, t, w("amortize", 373.2), 490, 640, sc(check_icon, 30), anim="pop")
    show(c, t, w("invista", 376.2), 490, 760, sc(check_icon, 30), anim="pop")
    hero(c, t, 1680, 1050, 0.6, [(0, "present_l"), (w("amortize", 373.2), "point_l")], [(0, "confident")], appear=359.1, look=-1)


def s28(c, t):  # 377.1 - 389.9  poupança ~8,3%: a Carla termina com R$ 85 mil a mais
    show(c, t, 377.2, 960, 130, M("Testando: poupança", 72, NAVY), anim="up")
    show(c, t, w("poupança", 380.6), 420, 480, sc(piggy, s=1.0), anim="pop")
    show(c, t, w("oito", 382.2), 420, 700, M("~8,3% ao ano", 64, DIEC), anim="pop")
    show(c, t, w("oito", 382.2, 0.3), 760, 480, M("<", 100, INK), anim="pop")
    show(c, t, w("oito", 382.2, 0.3), 1050, 480, M("9,8%", 100, CARC), anim="pop")
    show(c, t, w("perderia", 384.5), 1050, 580, T("(amortizar)", 46, DGRAY), anim="fade")
    show(c, t, w("oitenta", 387.0), 760, 840, lambda c: hl(c, "Carla: + R$ 85 mil", 0, 0, 80, PINKISH, CARC), anim="stamp")
    hero(c, t, 1640, 1050, 0.85, [(0, "present_l"), (w("perderia", 384.5), "shrug")], [(0, "neutral")], appear=377.2, look=-1)


def s29(c, t):  # 389.9 - 403.5  juros de hoje por 30 anos (CDB ~11,5% líquido): Diego + R$ 164 mil
    show(c, t, 389.95, 960, 130, M("E com os juros de hoje?", 72, NAVY), anim="up")
    show(c, t, w("cdb", 394.5), 520, 340, T("CDB 100% do CDI, sem imposto", 48, DGRAY), anim="fade")
    show(c, t, w("onze", 397.8), 520, 440, M("~11,5% ao ano", 84, DIEC), anim="stamp")
    show(c, t, w("trinta", 392.8), 520, 540, T("(se durasse 30 anos seguidos)", 44, DGRAY), anim="fade")
    show(c, t, w("ganharia", 400.4), 1100, 700, lambda c: hl(c, "Diego: + R$ 164 mil", 0, 0, 80, LBLUE, DIEC), anim="stamp")
    diego(c, t, 1300, 1040, 0.55, [(0, "stand"), (w("ganharia", 400.4), "arms_up")], [(0, "neutral"), (w("ganharia", 400.4), "grin")],
          appear=389.95, look=-1)
    hero(c, t, 1700, 1050, 0.6, [(0, "present_l")], [(0, "neutral")], appear=389.95, look=-1)


def s30(c, t):  # 403.4 - 411.9  juro de hoje não dura 30 anos; Selic cai, TR cai, custo cai
    show(c, t, 403.6, 760, 200, lambda c: hl(c, "juro de hoje não dura 30 anos", 0, 0, 70, PINKISH, RED), anim="stamp")
    items = [(w("selic", 407.0), "Selic"), (w("cai", 408.5), "TR"), (w("custo", 409.5), "custo do financiamento")]
    for i, (t0, lab) in enumerate(items):
        x = 300 + i * 420
        show(c, t, t0, x, 520, M(lab, 56 if i < 2 else 44, NAVY), anim="pop")
        show(c, t, t0 + 0.15, x, 640, sc(arrow_down_icon, s=1.0), anim="drop")
    show(c, t, w("também", 411.0), 720, 840, T("cai tudo junto", 54, DGRAY), anim="fade")
    hero(c, t, 1620, 1050, 0.95, [(0, "finger_up"), (w("selic", 407.0), "present_l")], [(0, "think")], appear=403.6, look=-1)


def arrow_down_icon(c):
    line(c, 0, -60, 0, 50, 12, RED)
    poly(c, [(-36, 30), (36, 30), (0, 80)]); fs(c, RED, 0)


def s31(c, t):  # 411.9 - 433.1  financiamento comum: ~11,5% + TR = mais de 13,5%; amortizar ganha de quase tudo
    show(c, t, 412.0, 960, 130, M("O caso que muda tudo", 74, RED), anim="up")
    show(c, t, w("comum", 418.4), 470, 330, T("financiamento comum dos bancos", 50, DGRAY), anim="fade")
    show(c, t, w("onze", 421.7), 470, 440, M("~11,5% + TR", 84, NAVY), anim="pop")
    show(c, t, w("treze", 426.6), 470, 600, lambda c: hl(c, "+ de 13,5% ao ano", 0, 0, 74, PINKISH, RED), anim="stamp")
    show(c, t, w("amortizar", 429.0), 1120, 420, sc(balance, -0.9,
                                                    sc(brick, s=0.55), sc(piggy, s=0.4), s=0.95), anim="pop")
    show(c, t, w("amortizar", 429.0, 0.3), 1120, 220, M("amortizar pesa mais", 52, CARC), anim="fade")
    show(c, t, w("qualquer", 430.3), 1120, 780, T("ganha de quase qualquer renda fixa", 48, CARC), anim="fade")
    hero(c, t, 1720, 1050, 0.55, [(0, "present_l"), (w("treze", 426.6), "head")], [(0, "neutral"), (w("treze", 426.6), "shocked")],
         appear=412.0, look=-1)


def s32(c, t):  # 433.2 - 447.6  mesma corrida: Carla + R$ 306 mil; só mudou a taxa do contrato
    show(c, t, 433.3, 960, 130, M("A mesma corrida, a 13,7%", 72, NAVY), anim="up")
    money_bar(c, t, w("carla", 437.2), 420, 940, 925 * 0.55, 220, CARC, "R$ 925 mil", "Carla", d=0.9, tsize=60)
    money_bar(c, t, w("carla", 437.2, 0.3), 760, 940, 619 * 0.55, 220, DIEC, "R$ 619 mil", "Diego (10%)", d=0.9, tsize=60)
    show(c, t, w("trezentos", 438.3), 1250, 380, lambda c: hl(c, "Carla: + R$ 306 mil", 0, 0, 70, PINKISH, CARC), anim="stamp")
    show(c, t, w("mesmo", 441.0), 1250, 540, T("mesmo apê, mesma pessoa, mesmos R$ 300", 40, DGRAY), anim="fade")
    show(c, t, w("mudou", 445.6), 1250, 660, M("só mudou a taxa", 64, NAVY), anim="pop")
    show(c, t, w("contrato", 446.7), 1250, 800, sc(doc_contract, s=0.6), anim="pop")
    hero(c, t, 1720, 1050, 0.55, [(0, "present_l"), (w("mudou", 445.6), "finger_up")], [(0, "neutral"), (w("mudou", 445.6), "confident")],
         appear=433.3, look=-1)


def s33(c, t):  # 447.6 - 451.2  o que a conta não mostra
    show(c, t, 447.7, 760, 300, M("o que a conta não mostra", 84, NAVY), anim="pop")
    show(c, t, w("importam"), 760, 620, sc(clipboard, "IMPORTA", 4, False, s=0.9), anim="pop")
    hero(c, t, 1450, 1050, 1.0, [(0, "finger_up")], [(0, "think")], appear=447.7, look=-1)


def s34(c, t):  # 451.2 - 472.6  1. reserva de emergência antes: dinheiro amortizado não volta
    step(c, t, 451.3, 1, "a reserva de emergência vem antes", PINKISH)
    show(c, t, w("amortizado", 454.5), 360, 430, group(sc(brick, s=1.1), at(0, 130, T("dinheiro amortizado", 46, DGRAY))), anim="pop")
    show(c, t, w("volta", 456.0), 360, 680, M("NÃO VOLTA", 70, RED), anim="stamp")
    show(c, t, w("emprego", 457.5), 880, 340, T("perdeu o emprego?", 52, DGRAY), anim="fade")
    show(c, t, w("vencendo", 461.8), 880, 420, T("a parcela continua vencendo", 50, RED), anim="fade")
    show(c, t, w("disponível"), 880, 640, group(sc(piggy, s=0.8), at(0, 150, T("o do Diego está ali, disponível", 46, DIEC))), anim="pop")
    show(c, t, w("vídeo", 469.0), 1360, 470, sc(video_card, "Demitido hoje?", None, s=0.42, icon=sc(calendar, "?", RED, s=0.9)), anim="pop")
    show(c, t, w("monte", 468.4), 1360, 680, lambda c: hl(c, "monte a reserva primeiro", 0, 0, 48, LYELLOW), anim="stamp")
    hero(c, t, 1720, 1050, 0.6, [(0, "finger_up"), (w("monte", 468.4), "point_l")], [(0, "confident")], appear=451.3, look=-1)


def s35(c, t):  # 472.6 - 486.2  2. disciplina: o Diego precisa investir todo mês por 30 anos
    step(c, t, 472.7, 2, "disciplina")
    diego(c, t, 330, 1000, 0.85, [(0, "hold")], [(0, "neutral")], appear=472.7, look=0.6)
    for i in range(6):
        show(c, t, w("todo", 478.0) + i * 0.25, 640 + i * 140, 420, lambda c, n=i: calendar(c, str(n + 1), NAVY, 48), s=0.55, anim="pop")
    show(c, t, w("trinta", 479.4), 990, 580, M("360 meses, sem falhar", 60, DIEC), anim="pop")
    show(c, t, w("gastar", 480.6), 990, 670, T("e sem gastar", 48, RED), anim="fade")
    show(c, t, w("sozinha"), 990, 830, lambda c: hl(c, "a da Carla funciona sozinha", 0, 0, 56, PINKISH, CARC), anim="stamp")
    hero(c, t, 1700, 1050, 0.6, [(0, "present_l")], [(0, "neutral")], appear=472.7, look=-1)


def s36(c, t):  # 486.2 - 501.4  3. seguro de morte e invalidez sobre o saldo: quem amortiza paga menos
    step(c, t, 486.3, 3, "o seguro também cai")
    show(c, t, w("seguro", 488.0), 420, 520, sc(shield, NAVY, s=1.2), anim="pop")
    show(c, t, w("morte", 490.4), 420, 720, T("morte e invalidez", 48, DGRAY), anim="fade")
    show(c, t, w("saldo", 493.4), 980, 440, T("calculado sobre o saldo devedor", 52, DGRAY), anim="fade")
    show(c, t, w("menos", 496.0), 980, 560, M("amortizou = menos seguro", 58, GREEN), anim="pop")
    show(c, t, w("pontinho"), 980, 720, lambda c: hl(c, "+1 ponto pra Carla", 0, 0, 62, PINKISH, CARC), anim="stamp")
    show(c, t, w("fora", 500.0), 980, 830, T("(fora da conta)", 44, DGRAY), anim="fade")
    hero(c, t, 1680, 1050, 0.62, [(0, "present_l")], [(0, "neutral")], appear=486.3, look=-1)


def s37(c, t):  # 501.4 - 514.8  4. FGTS pode amortizar a cada 2 anos (SFH)
    step(c, t, 501.5, 4, "o FGTS")
    show(c, t, w("fgts", 502.5), 450, 520, sc(document, "FGTS", GREEN, 40, s=1.1), anim="pop")
    show(c, t, w("amortizar", 504.4), 960, 380, M("pode amortizar", 60, NAVY), anim="pop")
    show(c, t, w("dois", 505.6), 960, 520, lambda c: hl(c, "a cada 2 anos", 0, 0, 72, LYELLOW), anim="stamp")
    show(c, t, w("regras", 507.2), 960, 630, T("(regras do sistema financeiro da habitação)", 42, DGRAY), anim="fade")
    show(c, t, w("pouco", 510.8), 960, 790, T("rende pouco parado; pode virar anos a menos de dívida", 44, GREEN), anim="fade")
    hero(c, t, 1680, 1050, 0.62, [(0, "present_l"), (w("virar", 512.0), "thumb")], [(0, "neutral"), (w("virar", 512.0), "happy")],
         appear=501.5, look=-1)


def s38(c, t):  # 514.8 - 531.1  3 atitudes: 1. descubra a taxa de verdade (+TR); 2. reserva antes
    show(c, t, 514.9, 960, 130, M("Na prática: 3 atitudes", 72, NAVY), anim="up")
    show(c, t, w("contrato", 518.6), 420, 560, sc(doc_contract, s=1.6), anim="pop")
    show(c, t, w("um", 517.4), 870, 330, L("1. descubra a taxa de verdade", 54, INK, MARKER), anim="left")
    show(c, t, w("some", 523.6), 900, 420, L("juros efetivos + TR", 48, RED), anim="left")
    show(c, t, w("dois", 526.0), 870, 560, L("2. reserva de emergência antes", 54, INK, MARKER), anim="left")
    hero(c, t, 1700, 1050, 0.6, [(0, "finger_up"), (w("contrato", 518.6), "present_l")], [(0, "confident")], appear=514.9, look=-1)


def s39(c, t):  # 531.1 - 549.9  3. compare as taxas: amortize (prazo) / invista / empate: dormir tranquilo
    step(c, t, 531.2, 3, "compare as duas taxas")
    show(c, t, w("dívida", 533.5), 760, 330, L("dívida custa mais: amortize, reduzindo o prazo", 50, CARC), anim="left", s=1.0)
    show(c, t, w("menos", 540.6), 760, 430, L("custa menos: investir pode valer", 50, DIEC), anim="left")
    show(c, t, w("empate", 543.1), 760, 560, M("deu empate?", 64, NAVY), anim="pop")
    show(c, t, w("dormir", 544.8), 760, 680, lambda c: hl(c, "escolha o que te deixa dormir tranquilo", 0, 0, 54, LYELLOW), anim="stamp")
    show(c, t, w("quitada", 547.5), 1380, 880, sc(house, False, s=1.0), anim="pop")
    hero(c, t, 1700, 1050, 0.62, [(0, "present_l"), (w("dormir", 544.8), "thumb")], [(0, "neutral"), (w("dormir", 544.8), "happy")],
         appear=531.2, look=-1)


def s40(c, t):  # 549.9 - 565.3  recapitulando
    show(c, t, 550.0, 960, 120, M("Recapitulando", 74, NAVY), anim="up")
    rows_ = [(w("trezentos", 550.8), "R$ 300/mês: a Carla quita 13 anos antes", CARC),
             (w("diego", 555.0), "o Diego, investindo os R$ 300, praticamente empata", DIEC),
             (w("porque", 559.0), "amortizar rende o juro do contrato (juros + TR)", GREEN),
             (w("quem", 562.8), "quem decide é esse número", NAVY)]
    for i, (t0, lab, col) in enumerate(rows_):
        y = 300 + i * 150
        show(c, t, t0, 560, y, lambda c, n=i + 1, col=col: (circle(c, 0, 0, 34, col, 5),
                                                         text(c, str(n), 0, 2, 44, MARKER, WHITE)), anim="pop")
        show(c, t, t0 + 0.1, 620, y, L(lab, 48, INK), anim="left")
    hero(c, t, 290, 1040, 0.8, [(0, "present")], [(0, "happy")], appear=550.0, look=1)


def s41(c, t):  # 565.3 - END  comentários: qual a taxa do seu financiamento? + alugar ou comprar
    show(c, t, 565.4, 1080, 320, lambda c: speech(c, 1000, 260, -360, 170), anim="pop")
    show(c, t, 565.6, 1080, 270, T("Amortiza ou investe?", 52, DGRAY), anim="fade")
    show(c, t, w("taxa", 568.0), 1080, 350, M("qual a taxa do seu financiamento?", 50, NAVY), anim="fade")
    show(c, t, w("alugar", 572.0), 1080, 700, sc(video_card, "Alugar ou comprar?", "onde essa história começou", s=0.6), anim="pop")
    hero(c, t, 340, 1010, 1.1, [(0, "wave"), (w("alugar", 572.0), "point_r")], [(0, "happy")], appear=565.4, look=1)
    show(c, t, 565.6, 1080, 960, T("conteúdo educativo, não é recomendação de investimento", 36, DGRAY), anim="fade")


def s42(c, t):  # END - fim (5 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres: vídeo à esquerda (x 170-950, y 300-740) e inscrever-se à direita (~1450, 520).
    show(c, t, END + 0.1, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, END + 0.4, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, END + 0.4, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (END + 2.5, "relax")], [(0, "happy")], appear=END + 0.1)


SCENES = [
    (0.0, 11.7, s01), (11.7, 29.4, s02), (29.4, 49.0, s03), (49.0, 66.1, s04), (66.1, 82.5, s05),
    (82.5, 94.1, s06), (94.1, 104.3, s07), (104.3, 126.5, s08), (126.5, 142.4, s09), (142.4, 150.7, s10),
    (150.7, O2, s11),
    (O2, 190.0, s12), (190.0, 198.2, s13), (198.2, 211.6, s14), (211.6, 217.3, s15), (217.3, 236.5, s16),
    (236.5, 243.4, s17), (243.4, 252.2, s18), (252.2, 262.9, s19), (262.9, 271.6, s20), (271.6, 280.6, s21),
    (280.6, 298.2, s22), (298.2, 316.6, s23), (316.6, O3, s24),
    (O3, 343.8, s25), (343.8, 358.9, s26), (358.9, 377.0, s27), (377.0, 389.8, s28), (389.8, 403.4, s29),
    (403.4, 411.9, s30), (411.9, 433.1, s31), (433.1, 447.5, s32), (447.5, 451.1, s33), (451.1, 472.5, s34),
    (472.5, 486.1, s35), (486.1, 501.3, s36), (501.3, 514.7, s37), (514.7, 531.0, s38), (531.0, 549.8, s39),
    (549.8, 565.2, s40), (565.2, END, s41), (END, 999.0, s42),
]

# só toques pontuais, sem ruído: 9,8% / R$ 186 mil / EMPATE / + R$ 306 mil
SFX = [(w("nove", 98.0), "tum"), (w("cento", 205.8), "soft_ding"), (w("empate", 315.4), "tum"),
       (w("trezentos", 438.3), "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")
