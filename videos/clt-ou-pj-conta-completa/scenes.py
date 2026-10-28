"""CLT de R$ 5 mil ou PJ de R$ 7 mil? A conta completa (Faz a Conta, vídeo longo 16:9).
Narração Calm Carlos (HeyGen, ElevenLabs v4), 3 blocos, 0,4 s entre blocos.
Tempos absolutos: bloco1 0,000 | bloco2 172,416 | bloco3 345,616 | fim da fala 559,951 | +5 s de tela final.
Premissas (28/10/2026): INSS 2026 (teto 8.475,55; salário mínimo 1.621), IR 2026 com a Lei 15.270/2025 (isento até
R$ 5 mil, redutor até 7.350, vale para o 13º), Simples Nacional Anexo III 6% (fator R >= 28%) e Anexo V 15,5%,
pró-labore com INSS 11%, contador R$ 300 (ilustrativo), MEI teto R$ 81 mil em 2026, seguro-desemprego 2026 (teto
R$ 2.518,65, 5 parcelas). Contas em contas.py."""
import json
import os

from engine import *  # noqa

O2, O3 = 172.416, 345.616
END = 559.951

_PAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "palavras.json"), encoding="utf-8"))


def w(word, after=0.0, d=0.0):
    """início (s) da primeira palavra que começa com `word` depois de `after` (tempo absoluto), mais d"""
    word = word.lower()
    for p in _PAL:
        if p["t0"] >= after - 0.01 and p["w"].lower().strip(",.:?!\"").startswith(word):
            return p["t0"] + d
    raise KeyError((word, after))


PINKISH = (1, 0.8, 0.76)
CLTC = BLUE
PJC = ORANGE


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def lv(label, val, lsize=50, vsize=60, vcol=GREEN, lcol=DGRAY):
    def f(c):
        text(c, label, 0, 0, lsize, HAND, lcol, align="l")
        x = text_w(c, label, lsize, HAND) + 18
        text(c, val, x, 0, vsize, MARKER, vcol, align="l")
    return f


def row(label, val, vcol=INK, wd=760, size=54):
    """linha de extrato: rótulo à esquerda, valor à direita (centrada em 0)"""
    def f(c):
        text(c, label, -wd / 2, 0, size, HAND, DGRAY, align="l")
        text(c, val, wd / 2, 0, size + 4, MARKER, vcol, align="r")
    return f


def strike(wd=260, col=RED):
    return lambda c: line(c, -wd / 2, 8, wd / 2, -8, 10, col)


def tag(s, col, size=54):
    """etiqueta colorida tipo crachá"""
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


def marina(c, t, x, y, s, poses, exprs, kind="clt", **kw):
    kw.setdefault("shirt", CLTC if kind == "clt" else PJC)
    kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


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


def offer(kind, val):
    """cartão de proposta: CLT (azul) ou PJ (laranja)"""
    col = CLTC if kind == "CLT" else PJC
    def f(c):
        rrect(c, -230, -150, 460, 300, 26); fs(c, WHITE, 6)
        c.save(); c.translate(0, -80); tag(kind, col, 60)(c); c.restore()
        text(c, val, 0, 40, 84, MARKER, col)
        text(c, "por mês", 0, 112, 44, HAND, DGRAY)
    return f


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 11.5  Marina recebeu duas propostas: CLT R$ 5.000 x PJ R$ 7.000
    show(c, t, 0.05, 960, 120, M("Duas propostas, o mesmo trabalho", 66, NAVY), anim="up")
    marina(c, t, 960, 1040, 0.95, [(0, "stand"), (w("primeira"), "point_l"), (w("segunda"), "point_r")],
           [(0, "neutral"), (w("primeira"), "think"), (w("sete"), "happy")], appear=0.1,
           look=lambda tt: -1 if tt < w("segunda") else 1)
    show(c, t, w("primeira"), 520, 480, offer("CLT", "R$ 5.000"), anim="pop")
    show(c, t, w("segunda"), 1400, 480, offer("PJ", "R$ 7.000"), anim="pop")
    show(c, t, w("marina"), 960, 260, T("a Marina", 52, DGRAY), anim="fade")
    hero(c, t, 1740, 1050, 0.5, [(0, "present_l")], [(0, "neutral")], appear=0.3, look=-1)


def s02(c, t):  # 11.5 - 27.3  +R$ 2.000; conta do ano inteiro: imposto, férias, 13º, FGTS; a diferença quase some
    k = 1.0 - 0.55 * grow(t, w("encolhe"), 1.6)
    show(c, t, 11.6, 620, 360, lambda c: (c.scale(k, k), text(c, "+R$ 2.000", 0, 0, 150, MARKER, GREEN)), anim="stamp")
    show(c, t, w("parece"), 620, 500, T("nem tem o que pensar?", 56, DGRAY), anim="fade", t1=w("quando", 15.0))
    items = [("imposto", sc(document, "IMPOSTO", RED, 30, s=0.6)), ("férias", sc(beach_chair, s=0.42)),
             ("décimo", sc(gift, s=0.6)), ("fgts", sc(piggy, s=0.5))]
    labs = ["imposto", "férias", "13º", "FGTS"]
    for i, (key, fn) in enumerate(items):
        x = 300 + i * 250
        show(c, t, w(key, 18.0), x, 720, fn, anim="pop")
        show(c, t, w(key, 18.0, 0.1), x, 850, T(labs[i], 48), anim="fade")
    show(c, t, w("quase", 25.0), 620, 960, lambda c: hl(c, "a diferença quase some", 0, 0, 54, PINKISH, RED), anim="stamp")
    hero(c, t, 1500, 1040, 1.0, [(0, "present_l"), (w("quando", 15.0), "think"), (w("quase", 25.0), "shrug")],
         [(0, "happy"), (w("quando", 15.0), "think"), (w("quase", 25.0), "worried")], appear=11.6, look=-1)


def s03(c, t):  # 27.3 - 35.5  um detalhe: o PJ de 7 mil ganha menos que o CLT de 5
    show(c, t, 27.4, 1150, 200, T("e, dependendo de um detalhe...", 58, DGRAY), anim="up")
    show(c, t, w("pj", 31.0), 820, 470, group(tag("PJ", PJC, 60), at(0, 120, M("R$ 7.000", 76, PJC))), anim="pop")
    show(c, t, w("menos", 33.0), 1150, 480, lambda c: text(c, "<", 0, 0, 160, MARKER, RED), anim="stamp")
    show(c, t, w("clt", 33.8), 1480, 470, group(tag("CLT", CLTC, 60), at(0, 120, M("R$ 5.000", 76, CLTC))), anim="pop")
    show(c, t, w("menos", 33.0, 0.3), 1150, 800, lambda c: hl(c, "ganha MENOS no fim do ano", 0, 0, 60, PINKISH, RED), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "finger_up"), (w("menos", 33.0), "head")], [(0, "confident"), (w("menos", 33.0), "shocked")],
         appear=27.4, look=1)


def s04(c, t):  # 35.5 - 46.6  hoje: a conta do jeito certo, regras de 2026; no final, quanto pedir a mais
    title(c, t, 35.6, "Hoje no vídeo", y=120, size=74)
    rows = [(w("conta", 36.5), sc(calculator, "2026", s=0.5), "a conta do ano inteiro, com as regras de 2026"),
            (w("final", 40.8), sc(clipboard, "PROPOSTA", 2, s=0.38), "quanto a mais um PJ precisa pedir")]
    for i, (t0, fn, lab) in enumerate(rows):
        y = 360 + i * 260
        show(c, t, t0, 720, y, fn, anim="pop")
        show(c, t, t0 + 0.1, 850, y, L(lab, 56, NAVY), anim="left")
    hero(c, t, 330, 1040, 0.95, [(0, "present")], [(0, "happy")], appear=35.6, look=1, prop=("l", prop_calculator))


def s05(c, t):  # 46.6 - 70.4  regras do jogo: INSS 2026, IR isento até R$ 5 mil, Simples Nacional; benefícios depois
    show(c, t, 46.7, 1080, 120, M("As regras do jogo (2026)", 70, NAVY), anim="up")
    rows = [(w("inss", 49.5), CLTC, "INSS: tabela de 2026"),
            (w("isenta", 54.5), CLTC, "IR: isento até R$ 5 mil por mês"),
            (w("simples", 59.5), PJC, "PJ: Simples Nacional"),
            (w("fora", 64.5), GRAY, "fora, por enquanto: vale-refeição e plano de saúde")]
    for i, (t0, col, lab) in enumerate(rows):
        y = 290 + i * 160
        show(c, t, t0, 700, y, lambda c, col=col: circle(c, 0, 0, 26, col, 5), anim="pop")
        show(c, t, t0 + 0.1, 760, y, L(lab, 54, INK if col != GRAY else DGRAY), anim="left")
    show(c, t, w("frente", 69.0), 1200, 920, T("(eles entram mais pra frente)", 46, DGRAY), anim="fade")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("simples", 59.5), "point_r")], [(0, "neutral"), (w("isenta", 54.5), "happy")],
         appear=46.7, look=1, prop=("l", prop_pointer))


def s06(c, t):  # 70.4 - 90.8  contracheque CLT: 5.000 - INSS 501 - IR 0 = 4.498 líquido
    show(c, t, 70.5, 1150, 120, group(tag("CLT", CLTC, 60), at(330, 0, M("contracheque", 60, NAVY))), anim="up")
    show(c, t, 70.6, 1150, 560, panel(900, 640), anim="fade")
    show(c, t, w("cinco", 72.4), 1150, 320, row("salário", "R$ 5.000", INK), anim="left")
    show(c, t, w("inss", 75.5), 1150, 430, row("INSS", "- R$ 501", RED), anim="left")
    show(c, t, w("imposto", 79.3), 1150, 540, row("imposto de renda", "R$ 0", GREEN), anim="left")
    show(c, t, w("regra", 81.6), 1150, 620, T("isento até R$ 5 mil (regra nova)", 42, GREEN), anim="fade")
    if t > w("recebe", 86.0):
        line(c, 750, 690, 1550, 690, 5, INK)
    show(c, t, w("quatro", 87.8), 1150, 790, row("líquido por mês", "R$ 4.498", CLTC, size=60), anim="stamp")
    marina(c, t, 330, 1040, 0.95, [(0, "stand"), (w("zero", 80.7), "arms_up"), (w("recebe", 86.0), "hips")],
           [(0, "neutral"), (w("zero", 80.7), "grin"), (w("recebe", 86.0), "happy")], appear=70.5, look=1)


def s07(c, t):  # 90.8 - 103.2  os salários que ninguém põe na conta: 1) 13º = +R$ 4.498
    show(c, t, 90.9, 960, 130, M("Os salários que ninguém põe na conta", 66, NAVY), anim="up")
    show(c, t, w("primeiro", 95.8), 700, 250, tag("1", CLTC, 60), anim="pop")
    show(c, t, w("décimo", 96.5), 700, 580, sc(gift, s=1.3), anim="pop")
    show(c, t, w("décimo", 96.5, 0.2), 1220, 360, M("13º salário", 90, CLTC), anim="up")
    show(c, t, w("inteiro", 99.2), 1220, 500, T("mais um salário inteiro no fim do ano", 52, DGRAY), anim="fade")
    show(c, t, w("quatro", 101.0), 1220, 660, lambda c: hl(c, "+R$ 4.498", 0, 0, 100, LGREEN, GREEN), anim="stamp")
    hero(c, t, 1720, 1050, 0.55, [(0, "present_l")], [(0, "happy")], appear=91.0, look=-1)


def s08(c, t):  # 103.2 - 116.3  2) férias: salário + 1/3 → R$ 5.300 líquidos
    show(c, t, 103.3, 700, 200, tag("2", CLTC, 60), anim="pop")
    show(c, t, w("férias", 104.3), 700, 520, sc(beach_chair, s=1.0), anim="pop")
    show(c, t, w("férias", 104.3, 0.2), 1250, 230, M("férias", 100, CLTC), anim="up")
    show(c, t, w("trinta", 105.7), 1250, 380, T("30 dias + o salário normal", 54, DGRAY), anim="fade")
    show(c, t, w("terço", 109.4), 1250, 490, lambda c: hl(c, "+ 1/3 a mais", 0, 0, 70, LYELLOW), anim="stamp")
    show(c, t, w("cinco", 113.9), 1250, 680, lambda c: hl(c, "R$ 5.300 líquidos", 0, 0, 90, LGREEN, GREEN), anim="stamp")
    marina(c, t, 1720, 1050, 0.55, [(0, "stand"), (w("terço", 109.4), "arms_up")], [(0, "happy"), (w("terço", 109.4), "grin")],
           appear=103.3, look=-1)
    hero(c, t, 260, 1050, 0.5, [(0, "point_r")], [(0, "happy")], appear=103.4, look=1)


def s09(c, t):  # 116.3 - 134.1  3) FGTS: 8% do salário, também no 13º e férias → R$ 5.333 no ano; não aparece, mas é seu
    show(c, t, 116.4, 700, 200, tag("3", CLTC, 60), anim="pop")
    show(c, t, w("fgts", 117.6), 1250, 230, M("FGTS", 110, CLTC), anim="up")
    show(c, t, w("deposita", 120.1), 700, 520, sc(bank, s=1.0), anim="pop")
    show(c, t, w("oito", 120.8), 1250, 400, lambda c: hl(c, "8% do salário todo mês", 0, 0, 62, LYELLOW), anim="stamp")
    show(c, t, w("também", 124.1), 1250, 510, T("também sobre o 13º e as férias", 52, DGRAY), anim="fade")
    show(c, t, w("cinco", 128.1), 1250, 660, lambda c: hl(c, "R$ 5.333 por ano", 0, 0, 90, LGREEN, GREEN), anim="stamp")
    show(c, t, w("contracheque", 132.3), 1250, 820, T("não aparece no contracheque... mas é seu", 50, NAVY), anim="fade")
    hero(c, t, 260, 1050, 0.5, [(0, "point_r"), (w("contracheque", 132.3), "finger_up")], [(0, "confident")],
         appear=116.4, look=1)


def s10(c, t):  # 134.1 - 146.4  não são 12 salários: são 13 e 1/3 + FGTS
    show(c, t, 134.2, 960, 130, T("repara numa coisa", 58, DGRAY), anim="up")
    for i in range(12):
        x, y = 300 + (i % 6) * 165, 320 + (i // 6) * 190
        show(c, t, w("doze", 137.5, 0.05 * i), x, y, sc(calendar, str(i + 1), CLTC, 50, s=0.62), anim="drop")
    show(c, t, w("treze", 139.1), 300 + 6 * 165 + 40, 320, sc(calendar, "13º", GREEN, 44, s=0.62), anim="drop")
    show(c, t, w("terço", 140.7), 300 + 6 * 165 + 40, 510, M("+1/3", 60, GREEN), anim="stamp")
    show(c, t, w("fgts", 141.7), 1580, 420, group(sc(piggy, s=0.6), at(0, 120, T("+ FGTS", 48, GREEN))), anim="pop")
    show(c, t, w("treze", 139.1, 0.3), 960, 720, lambda c: hl(c, "13 salários e 1/3 + FGTS", 0, 0, 72, LYELLOW), anim="stamp")
    show(c, t, w("engana", 145.3), 960, 860, T("comparar só o mês engana", 54, RED), anim="fade")
    hero(c, t, 1700, 1050, 0.5, [(0, "present_l"), (w("engana", 145.3), "finger_up")], [(0, "think"), (w("treze", 139.1), "happy")],
         appear=134.2, look=-1)


def s11(c, t):  # 146.4 - 163.4  somando: 11 meses + férias + 13º + FGTS = R$ 64.615/ano = R$ 5.385/mês
    show(c, t, 146.5, 1150, 120, group(tag("CLT", CLTC, 60), at(240, 0, M("no ano", 60, NAVY))), anim="up")
    show(c, t, 146.6, 1150, 530, panel(900, 640), anim="fade")
    show(c, t, w("onze", 148.8), 1150, 290, row("11 meses de salário", "R$ 49.483"), anim="left")
    show(c, t, w("férias", 150.1), 1150, 380, row("férias + 1/3", "R$ 5.300"), anim="left")
    show(c, t, w("décimo", 150.8), 1150, 470, row("13º salário", "R$ 4.498"), anim="left")
    show(c, t, w("fgts", 152.2), 1150, 560, row("FGTS", "R$ 5.333"), anim="left")
    if t > w("leva", 154.6):
        line(c, 750, 620, 1550, 620, 5, INK)
    show(c, t, w("sessenta", 154.9), 1150, 700, row("total no ano", "R$ 64.615", CLTC, size=60), anim="stamp")
    show(c, t, w("cinco", 160.2), 1150, 940, lambda c: hl(c, "= R$ 5.385 por mês", 0, 0, 72, LGREEN, GREEN), anim="stamp")
    marina(c, t, 330, 1040, 0.95, [(0, "hips"), (w("cinco", 160.2), "arms_up")], [(0, "neutral"), (w("cinco", 160.2), "grin")],
           appear=146.5, look=1)


def s12(c, t):  # 163.4 - O2  5 mil de CLT não são 5 mil: valem quase R$ 5.400; guarda esse número
    show(c, t, 163.5, 1150, 200, M("R$ 5.000 de CLT", 76, CLTC), anim="up")
    show(c, t, w("não", 166.2), 1150, 290, T("não são R$ 5.000", 56, DGRAY), anim="fade")
    show(c, t, w("valem", 167.5), 1150, 400, T("valem quase", 60, DGRAY), anim="fade")
    show(c, t, w("quatrocentos", 169.2), 1150, 560, lambda c: hl(c, "R$ 5.400", 0, 0, 170, LGREEN, GREEN), anim="stamp")
    show(c, t, w("quatrocentos", 169.2, 0.2), 1150, 720, T("por mês", 56, DGRAY), anim="fade")
    show(c, t, w("guarda", 171.0), 1150, 870, M("guarda esse número", 60, NAVY), anim="up")
    hero(c, t, 360, 1040, 1.05, [(0, "present"), (w("quatrocentos", 169.2), "point_r"), (w("guarda", 171.0), "finger_up")],
         [(0, "confident"), (w("quatrocentos", 169.2), "grin")], appear=163.5, look=1)


# ======================================================================= BLOCO 2
def s13(c, t):  # O2 - 178.0  agora a proposta PJ: R$ 7.000 pelo mesmo trabalho
    show(c, t, O2 + 0.1, 1150, 300, tag("PJ", PJC, 90), anim="stamp")
    show(c, t, w("sete", O2), 1150, 520, M("R$ 7.000 por mês", 100, PJC), anim="up")
    show(c, t, w("mesmo", O2), 1150, 680, T("pelo mesmo trabalho", 58, DGRAY), anim="fade")
    marina(c, t, 380, 1040, 1.0, [(0, "wave")], [(0, "happy")], kind="pj", appear=O2 + 0.1, look=1)
    hero(c, t, 1740, 1050, 0.5, [(0, "present_l")], [(0, "neutral")], appear=O2 + 0.2, look=-1)


def s14(c, t):  # 178.0 - 204.6  dá pra ser MEI? teto R$ 81 mil x R$ 84 mil; profissões que nem podem ser MEI
    show(c, t, 178.1, 800, 120, M("Dá pra ser MEI?", 76, NAVY), anim="up")
    show(c, t, w("não", 183.0), 1460, 125, lambda c: hl(c, "na maioria, não", 0, 0, 52, PINKISH, RED), anim="stamp")
    base = 640
    money_bar(c, t, w("teto", 186.5), 760, base, 81 * 4.2, 240, NAVY, "R$ 81 mil", "teto do MEI (2026)", tsize=58)
    money_bar(c, t, w("oitenta", 191.5), 1120, base, 84 * 4.2, 240, PJC, "R$ 84 mil", "12 x R$ 7.000", tsize=58)
    show(c, t, w("profissões", 196.2), 1050, 800, T("e várias profissões nem podem ser MEI:", 50, DGRAY), anim="fade")
    jobs = [("programador", 199.5), ("designer", 200.9), ("advogado", 201.5), ("engenheiro", 202.3)]
    for i, (j, a) in enumerate(jobs):
        show(c, t, w(j, a - 2), 520 + i * 350, 900, group(T(j, 48, INK), at(0, 0, sc(strike(250), s=1.0))), anim="pop")
    hero(c, t, 270, 1050, 0.5, [(0, "think"), (w("não", 183.0), "shrug")], [(0, "think")], appear=178.1, look=1)


def s15(c, t):  # 204.6 - 212.5  Simples Nacional; o detalhe que muda tudo: o fator R
    show(c, t, 204.7, 1150, 220, T("então: empresa no", 56, DGRAY), anim="up")
    show(c, t, w("simples", 205.0), 1150, 330, M("Simples Nacional", 90, PJC), anim="up")
    show(c, t, w("detalhe", 208.5), 1150, 500, T("o detalhe que muda tudo:", 56, DGRAY), anim="fade")
    show(c, t, w("fator", 210.8), 1150, 700, lambda c: hl(c, "FATOR R", 0, 0, 160, LYELLOW), anim="stamp")
    marina(c, t, 380, 1040, 0.95, [(0, "stand"), (w("fator", 210.8), "think")], [(0, "neutral"), (w("fator", 210.8), "think")],
           kind="pj", appear=204.7, look=1)
    hero(c, t, 1750, 1050, 0.5, [(0, "finger_up")], [(0, "confident")], appear=204.8, look=-1)


def s16(c, t):  # 212.5 - 225.1  pró-labore >= 28% do faturamento → 6%; menos → 15,5%
    show(c, t, 212.6, 960, 120, M("Fator R: quanto a empresa paga pra dona", 62, NAVY), anim="up")
    show(c, t, w("pró-labore", 213.5), 960, 270, T("pró-labore (o \"salário\" da dona)", 52, DGRAY), anim="fade")
    # dois caminhos
    show(c, t, w("pelo", 215.0), 560, 430, lambda c: hl(c, "28% ou mais", 0, 0, 66, LGREEN, GREEN), anim="stamp")
    show(c, t, w("seis", 219.0), 560, 650, lambda c: text(c, "6%", 0, 0, 170, MARKER, GREEN), anim="stamp")
    show(c, t, w("seis", 219.0, 0.2), 560, 790, T("de imposto", 50, DGRAY), anim="fade")
    show(c, t, w("menos", 221.5), 1360, 430, lambda c: hl(c, "menos de 28%", 0, 0, 66, PINKISH, RED), anim="stamp")
    show(c, t, w("quinze", 223.5), 1360, 650, lambda c: text(c, "15,5%", 0, 0, 170, MARKER, RED), anim="stamp")
    show(c, t, w("quinze", 223.5, 0.2), 1360, 790, T("de imposto", 50, DGRAY), anim="fade")
    hero(c, t, 960, 1050, 0.55, [(0, "present"), (w("quinze", 223.5), "head")], [(0, "neutral"), (w("quinze", 223.5), "shocked")],
         appear=212.6)


def s17(c, t):  # 225.1 - 245.3  extrato PJ: pró-labore R$ 1.960 → INSS R$ 215; DAS 6% R$ 420; contador R$ 300
    show(c, t, 225.2, 1150, 120, group(tag("PJ", PJC, 60), at(240, 0, M("todo mês", 60, NAVY))), anim="up")
    show(c, t, 225.3, 1150, 485, panel(940, 520), anim="fade")
    show(c, t, 225.4, 1150, 290, row("faturamento", "R$ 7.000", INK, wd=800), anim="left")
    show(c, t, w("mil", 228.0), 1150, 380, row("pró-labore (28%)", "R$ 1.960", DGRAY, wd=800, size=48), anim="left")
    show(c, t, w("inss", 233.0), 1150, 480, row("INSS (11% do pró-labore)", "- R$ 215", RED, wd=800), anim="left")
    show(c, t, w("imposto", 236.5), 1150, 580, row("imposto da empresa (6%)", "- R$ 420", RED, wd=800), anim="left")
    show(c, t, w("contador", 241.5), 1150, 680, row("contador", "- R$ 300", RED, wd=800), anim="left")
    show(c, t, w("contador", 241.5, 0.3), 1150, 800, T("(contador: valor de exemplo)", 40, DGRAY), anim="fade")
    marina(c, t, 330, 1040, 0.95, [(0, "hold")], [(0, "think")], kind="pj", appear=225.2, look=1)


def s18(c, t):  # 245.3 - 256.4  e o IR? pró-labore abaixo de 5 mil: zero; o resto sai como lucro, isento
    show(c, t, 245.4, 1150, 160, M("E o imposto de renda?", 76, NAVY), anim="up")
    show(c, t, w("zero", 246.7), 1150, 360, row("sobre o pró-labore", "R$ 0", GREEN, wd=820, size=58), anim="left")
    show(c, t, w("abaixo", 249.0), 1150, 450, T("(fica abaixo de R$ 5 mil)", 46, DGRAY), anim="fade")
    show(c, t, w("distribuição", 252.5), 1150, 600, row("resto, como lucro", "isento", GREEN, wd=820, size=58), anim="left")
    show(c, t, w("isenta", 255.4), 1150, 780, lambda c: hl(c, "IR zero nos dois", 0, 0, 70, LGREEN, GREEN), anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "think"), (w("zero", 246.7), "present")], [(0, "think"), (w("zero", 246.7), "happy")],
         appear=245.4, look=1)


def s19(c, t):  # 256.4 - 274.2  sobram R$ 6.064/mês; R$ 72.800/ano x R$ 64.600 CLT; "o PJ ganhou fácil. Certo?"
    show(c, t, 256.5, 1050, 120, T("7.000 - 420 - 215 - 300", 64, DGRAY), anim="up")
    show(c, t, w("sobram", 261.9), 1050, 250, lambda c: hl(c, "sobram R$ 6.064 por mês", 0, 0, 70, LGREEN, GREEN), anim="stamp")
    base = 880
    money_bar(c, t, w("setenta", 265.3), 1250, base, 72.8 * 6.5, 260, PJC, "R$ 72.800", "PJ, 12 meses", tsize=60)
    money_bar(c, t, w("sessenta", 268.3), 850, base, 64.6 * 6.5, 260, CLTC, "R$ 64.600", "CLT, no ano", tsize=60)
    show(c, t, w("fácil", 271.5), 1560, 420, M("ganhou fácil?", 56, PJC), anim="pop")
    marina(c, t, 300, 1040, 0.9, [(0, "stand"), (w("fácil", 271.5), "arms_up")], [(0, "happy"), (w("fácil", 271.5), "grin")],
           kind="pj", appear=256.5, look=1)
    hero(c, t, 1690, 1050, 0.5, [(0, "present_l"), (w("certo", 273.0), "think")], [(0, "neutral"), (w("certo", 273.0), "think")],
         appear=256.6, look=-1)


def s20(c, t):  # 274.2 - 292.1  calma: faltou as férias; PJ não tem férias pagas; não fatura 1 mês; custos continuam
    show(c, t, 274.3, 960, 120, M("Calma. Faltaram as férias.", 72, NAVY), anim="up")
    show(c, t, w("pagas", 277.8), 560, 420, group(sc(beach_chair, s=0.8), at(0, 0, sc(big_x, 110, s=1.0))), anim="pop")
    show(c, t, w("pagas", 277.8, 0.2), 560, 640, T("PJ não tem férias pagas", 50, RED), anim="fade")
    show(c, t, w("fatura", 282.0), 1080, 330, group(sc(calendar, "0", RED, 60, s=0.8), at(0, 150, T("1 mês sem faturar", 46, RED))),
         anim="drop")
    rows = [(w("contador", 284.9), "contador"), (w("pró-labore", 285.8), "pró-labore"), (w("inss", 286.8), "INSS")]
    for i, (t0, lab) in enumerate(rows):
        show(c, t, t0, 1300, 270 + i * 85, L(lab + " continua", 50, DGRAY), anim="left")
    show(c, t, w("décimo", 289.5), 1450, 620, M("sem 13º", 60, RED), anim="pop")
    show(c, t, w("fgts", 290.8), 1450, 730, M("sem FGTS", 60, RED), anim="pop")
    hero(c, t, 960, 1050, 0.55, [(0, "finger_up"), (w("pagas", 277.8), "shrug")], [(0, "confident"), (w("pagas", 277.8), "worried")],
         appear=274.3)


def s21(c, t):  # 292.1 - 313.5  com 11 meses: R$ 66.193 x R$ 64.615 → R$ 1.577/ano = R$ 131/mês; 2 mil viraram 130
    show(c, t, 292.2, 960, 110, T("refazendo com 11 meses de faturamento", 56, DGRAY), anim="up")
    base = 760
    money_bar(c, t, w("sessenta", 296.5), 1250, base, 66.2 * 6.0, 260, PJC, "R$ 66.193", "PJ", tsize=60)
    money_bar(c, t, w("sessenta", 300.5), 850, base, 64.6 * 6.0, 260, CLTC, "R$ 64.615", "CLT", tsize=60)
    show(c, t, w("mil", 304.9), 1650, 300, T("diferença:", 50, DGRAY), anim="fade")
    show(c, t, w("mil", 304.9, 0.2), 1650, 400, M("R$ 1.577/ano", 54, INK), anim="up")
    show(c, t, w("cento", 308.2), 1650, 520, lambda c: hl(c, "R$ 131/mês", 0, 0, 70, LYELLOW), anim="stamp")
    show(c, t, w("aqueles", 310.0), 1050, 920, group(M("+R$ 2.000", 64, GRAY), at(0, 6, sc(strike(300), s=1.0))), anim="pop")
    show(c, t, w("trinta", 312.0), 1050, 920, at(330, 0, lambda c: text(c, "= R$ 130", 0, 0, 80, MARKER, RED)), anim="stamp")
    hero(c, t, 300, 1040, 0.9, [(0, "present"), (w("aqueles", 310.0), "head")], [(0, "neutral"), (w("aqueles", 310.0), "shocked")],
         appear=292.2, look=1)


def s22(c, t):  # 313.5 - 329.1  o detalhe: sem fator R, pró-labore de 1 salário mínimo → 15,5%: R$ 1.085 em vez de R$ 420
    show(c, t, 313.6, 960, 120, M("O detalhe: sem o fator R", 72, RED), anim="up")
    show(c, t, w("salário", 320.0), 1150, 320, row("pró-labore", "1 salário mínimo", DGRAY, wd=880, size=52), anim="left")
    show(c, t, w("quinze", 322.4), 1150, 470, lambda c: hl(c, "imposto: 15,5%", 0, 0, 80, PINKISH, RED), anim="stamp")
    show(c, t, w("mil", 323.8), 1000, 680, lambda c: text(c, "R$ 1.085", 0, 0, 120, MARKER, RED), anim="stamp")
    show(c, t, w("quatrocentos", 327.5), 1500, 680, group(M("R$ 420", 70, GRAY), at(0, 6, sc(strike(220), s=1.0))), anim="pop")
    show(c, t, w("mil", 323.8, 0.3), 1150, 800, T("por mês", 50, DGRAY), anim="fade")
    marina(c, t, 330, 1040, 0.95, [(0, "shrug"), (w("quinze", 322.4), "head")], [(0, "think"), (w("quinze", 322.4), "shocked")],
           kind="pj", appear=313.6, look=1)


def s23(c, t):  # 329.1 - O3  ano cai pra R$ 59.325: quase R$ 5.300 a menos que a CLT; ganha "2 mil a mais" e termina com menos
    show(c, t, 329.2, 960, 110, T("com 15,5% e um mês de férias", 56, DGRAY), anim="up")
    base = 760
    money_bar(c, t, 329.4, 850, base, 64.6 * 6.0, 260, CLTC, "R$ 64.615", "CLT", tsize=60, d=0.5)
    money_bar(c, t, w("cinquenta", 332.0), 1250, base, 59.3 * 6.0, 260, RED, "R$ 59.325", "PJ sem fator R", tsize=60)
    show(c, t, w("quase", 336.0), 1650, 420, lambda c: hl(c, "-R$ 5.290", 0, 0, 72, PINKISH, RED), anim="stamp")
    show(c, t, w("quase", 336.0, 0.2), 1650, 520, T("no ano", 46, DGRAY), anim="fade")
    show(c, t, w("ganha", 340.5), 1050, 930, T("\"2 mil a mais\"... e termina com menos", 56, RED), anim="fade")
    hero(c, t, 300, 1040, 0.9, [(0, "present"), (w("quase", 336.0), "head")], [(0, "neutral"), (w("quase", 336.0), "desperate")],
         appear=329.2, look=1)


# ======================================================================= BLOCO 3
def s24(c, t):  # O3 - 372.3  rede de proteção da CLT: multa 40% do FGTS (+R$ 4 mil) e 5 parcelas de R$ 2.518 (+R$ 12,5 mil)
    show(c, t, O3 + 0.1, 1100, 120, M("A rede de proteção", 74, NAVY), anim="up")
    show(c, t, w("proteção", O3), 1600, 140, sc(shield, CLTC, s=0.55), anim="pop")
    show(c, t, w("demitida", 352.0), 1150, 290, T("CLT demitida sem justa causa (após 2 anos):", 50, DGRAY), anim="fade")
    show(c, t, w("multa", 355.6), 1150, 420, row("multa de 40% do FGTS", "+R$ 4 mil", GREEN, wd=880), anim="left")
    show(c, t, w("parcelas", 362.8), 1150, 540, row("seguro-desemprego", "5 x R$ 2.518", GREEN, wd=880), anim="left")
    show(c, t, w("doze", 369.8), 1150, 720, lambda c: hl(c, "seguro: + de R$ 12.500 ao todo", 0, 0, 66, LGREEN, GREEN), anim="stamp")
    marina(c, t, 330, 1040, 0.95, [(0, "stand"), (w("multa", 355.6), "hips")], [(0, "neutral"), (w("multa", 355.6), "happy")],
           appear=O3 + 0.1, look=1)


def s25(c, t):  # 372.3 - 392.8  PJ: contrato acaba, recebe zero; aposentadoria: INSS sobre R$ 5.000 x R$ 1.960
    show(c, t, 372.4, 1150, 120, group(tag("PJ", PJC, 60), at(330, 0, M("contrato acabou", 60, NAVY))), anim="up")
    show(c, t, w("zero", 375.0), 1150, 270, lambda c: text(c, "R$ 0", 0, 0, 110, MARKER, RED), anim="stamp")
    show(c, t, w("aviso", 376.5), 1150, 400, T("sem aviso prévio, sem multa, sem seguro", 54, RED), anim="fade")
    show(c, t, w("aposentadoria", 379.5), 1150, 540, M("aposentadoria: contribui pro INSS sobre", 52, NAVY), anim="up")
    base = 960
    money_bar(c, t, w("salário", 383.0), 950, base, 5000 * 0.06, 220, CLTC, "R$ 5.000", "", tsize=52)
    money_bar(c, t, w("pró-labore", 386.0), 1350, base, 1960 * 0.06, 220, PJC, "R$ 1.960", "", tsize=52)
    show(c, t, w("salário", 383.0, 0.6), 950, 1010, T("CLT", 44, CLTC), anim="fade")
    show(c, t, w("pró-labore", 386.0, 0.6), 1350, 1010, T("PJ", 44, PJC), anim="fade")
    marina(c, t, 330, 1040, 0.95, [(0, "head")], [(0, "worried")], kind="pj", appear=372.4, look=1)


def s26(c, t):  # 392.8 - 416.0  quanto pedir pra empatar? R$ 6.840 (+37%); sem fator R R$ 7.570 (+51%)
    show(c, t, 392.9, 960, 120, M("Quanto o PJ precisa pedir?", 74, NAVY), anim="up")
    show(c, t, w("empatar", 396.5), 1150, 260, T("só pra empatar no dinheiro (6% e 1 mês de férias):", 48, DGRAY), anim="fade")
    show(c, t, w("seis", 403.0), 1000, 420, lambda c: text(c, "R$ 6.840", 0, 0, 140, MARKER, PJC), anim="stamp")
    show(c, t, w("trinta", 405.7), 1500, 420, lambda c: hl(c, "+37%", 0, 0, 90, LYELLOW), anim="stamp")
    show(c, t, w("sem", 409.0), 1150, 610, T("sem o fator R:", 50, DGRAY), anim="fade")
    show(c, t, w("sete", 411.4), 1000, 740, lambda c: text(c, "R$ 7.570", 0, 0, 120, MARKER, RED), anim="stamp")
    show(c, t, w("cinquenta", 413.6), 1500, 740, lambda c: hl(c, "+51%", 0, 0, 80, PINKISH, RED), anim="stamp")
    show(c, t, w("trinta", 405.7, 0.3), 1150, 880, T("a mais que o salário CLT de R$ 5.000", 46, DGRAY), anim="fade")
    hero(c, t, 300, 1040, 0.95, [(0, "think"), (w("seis", 403.0), "point_r")], [(0, "think"), (w("seis", 403.0), "confident")],
         appear=392.9, look=1, prop=("l", prop_calculator))


def s27(c, t):  # 416.0 - 434.9  com benefícios: VR R$ 600 + plano R$ 400 = R$ 1.000/mês → empate ~R$ 8.000 (+60%)
    show(c, t, 416.1, 1150, 120, M("E se a CLT tiver benefícios?", 72, NAVY), anim="up")
    show(c, t, w("seiscentos", 419.0), 1150, 270, row("vale-refeição", "R$ 600", CLTC, wd=760), anim="left")
    show(c, t, w("plano", 421.5), 1150, 370, row("plano de saúde", "R$ 400", CLTC, wd=760), anim="left")
    show(c, t, w("mil", 425.3), 1150, 470, row("PJ paga do bolso", "R$ 1.000/mês", RED, wd=760), anim="left")
    show(c, t, w("oito", 431.2), 1000, 660, lambda c: text(c, "R$ 8.000", 0, 0, 140, MARKER, PJC), anim="stamp")
    show(c, t, w("sessenta", 432.7), 1500, 660, lambda c: hl(c, "+60%", 0, 0, 90, PINKISH, RED), anim="stamp")
    show(c, t, w("oito", 431.2, 0.3), 1150, 800, T("pra empatar", 50, DGRAY), anim="fade")
    show(c, t, 416.2, 1150, 940, T("(valores de exemplo)", 40, DGRAY), anim="fade")
    marina(c, t, 330, 1040, 0.95, [(0, "think"), (w("oito", 431.2), "head")], [(0, "think"), (w("oito", 431.2), "shocked")],
           kind="pj", appear=416.1, look=1)


def s28(c, t):  # 434.9 - 452.1  regra de bolso: +35% a 40% só pra empatar; com benefícios bons, +50%
    show(c, t, 435.0, 1150, 150, M("Regra de bolso", 84, NAVY), anim="up")
    show(c, t, w("trinta", 439.6), 1150, 360, lambda c: hl(c, "PJ = +35% a 40%", 0, 0, 110, LYELLOW), anim="stamp")
    show(c, t, w("empatar", 442.8), 1150, 500, T("só pra empatar", 56, DGRAY), anim="fade")
    show(c, t, w("benefícios", 443.9), 1150, 640, M("com benefícios bons: + de 50%", 64, RED), anim="up")
    show(c, t, w("parece", 449.9), 1150, 820, T("abaixo disso, parece maior... mas não é", 56, DGRAY), anim="fade")
    hero(c, t, 330, 1040, 1.0, [(0, "finger_up"), (w("parece", 449.9), "shrug")], [(0, "confident")], appear=435.0, look=1)


def s29(c, t):  # 452.1 - 465.1  PJ é ruim? Não: mais dinheiro, vários clientes, liberdade; conta certa
    show(c, t, 452.2, 1150, 150, M("PJ é ruim?", 84, NAVY), anim="up")
    show(c, t, w("não", 454.3), 1580, 160, lambda c: hl(c, "NÃO", 0, 0, 80, LGREEN, GREEN), anim="stamp")
    rows = [(w("ganha", 455.9), "muita gente ganha bem mais como PJ"), (w("vários", 458.4), "atende vários clientes"),
            (w("liberdade", 459.8), "e gosta da liberdade")]
    for i, (t0, lab) in enumerate(rows):
        y = 330 + i * 120
        show(c, t, t0, 820, y, sc(check_icon, 30, s=1.0), anim="pop")
        show(c, t, t0 + 0.1, 890, y, L(lab, 54), anim="left")
    show(c, t, w("comparar", 461.5), 1150, 780, lambda c: hl(c, "proposta certa, conta certa", 0, 0, 66, LYELLOW), anim="stamp")
    marina(c, t, 330, 1040, 0.95, [(0, "stand"), (w("liberdade", 459.8), "arms_up")], [(0, "happy"), (w("liberdade", 459.8), "grin")],
           kind="pj", appear=452.2, look=1)


def s30(c, t):  # 465.1 - 479.1  a conta serve pra negociar: 7 mil de PJ ≈ pouco mais de 5 mil de CLT
    show(c, t, 465.2, 1150, 150, M("A conta serve pra negociar", 74, NAVY), anim="up")
    show(c, t, w("sete", 470.0), 760, 400, group(tag("PJ", PJC, 50), at(0, 110, M("R$ 7.000", 74, PJC))), anim="pop")
    show(c, t, w("equivalem", 472.0), 1080, 420, sc(eq, 50, s=1.0), anim="pop")
    show(c, t, w("cinco", 473.5), 1420, 400, group(tag("CLT", CLTC, 50), at(0, 110, M("pouco + de R$ 5.000", 50, CLTC))), anim="pop")
    show(c, t, w("argumento", 475.5), 1150, 720, lambda c: hl(c, "argumento forte na negociação", 0, 0, 62, LGREEN, GREEN),
         anim="stamp")
    hero(c, t, 330, 1040, 0.95, [(0, "present"), (w("argumento", 475.5), "thumb")], [(0, "happy"), (w("argumento", 475.5), "grin")],
         appear=465.2, look=1)


def s31(c, t):  # 479.1 - 481.7  3 atitudes práticas
    show(c, t, 479.2, 1150, 500, lambda c: hl(c, "3 atitudes práticas", 0, 0, 110, LYELLOW), anim="stamp")
    hero(c, t, 330, 1040, 1.0, [(0, "finger_up")], [(0, "confident")], appear=479.2, look=1)


def s32(c, t):  # 481.7 - 496.1  1. compare o ano, não o mês
    step(c, t, 481.7, 1, "compare o ano, não o mês")
    show(c, t, w("pegue", 484.7), 700, 470, sc(offer("CLT", "R$ 5.000"), s=0.8), anim="pop")
    show(c, t, w("pegue", 484.7, 0.2), 1200, 470, sc(offer("PJ", "R$ 7.000"), s=0.8), anim="pop")
    show(c, t, w("doze", 487.0), 950, 700, T("12 meses: férias, 13º, FGTS e benefícios", 54, NAVY), anim="fade")
    show(c, t, w("engana", 494.0), 950, 830, M("mês contra mês engana", 60, RED), anim="up")
    hero(c, t, 1700, 1050, 0.55, [(0, "present_l")], [(0, "confident")], appear=481.8, look=-1, prop=("r", prop_calculator))


def s33(c, t):  # 496.1 - 506.0  2. pergunte ao contador sobre o fator R antes da primeira nota: + de R$ 7 mil/ano
    step(c, t, 496.1, 2, "pergunte sobre o fator R")
    show(c, t, w("contador", 498.5), 620, 480, sc(document, "NOTA", PJC, 34, s=1.1), anim="pop")
    show(c, t, w("primeira", 501.0), 620, 700, T("antes da primeira nota", 50, DGRAY), anim="fade")
    show(c, t, w("sete", 504.0), 1250, 480, lambda c: hl(c, "+ de R$ 7 mil", 0, 0, 100, LGREEN, GREEN), anim="stamp")
    show(c, t, w("ano", 505.4), 1250, 620, T("por ano", 54, DGRAY), anim="fade")
    hero(c, t, 1720, 1050, 0.55, [(0, "finger_up")], [(0, "confident")], appear=496.2, look=-1)


def s34(c, t):  # 506.0 - 525.7  3. seja seu próprio RH: separe férias, 13º e reserva; vídeo da reserva
    step(c, t, 506.0, 3, "seja o seu próprio RH")
    pigs = [(w("férias", 512.3), "férias", BLUE), (w("décimo", 513.2), "13º", GOLD), (w("reserva", 514.8), "reserva", GREEN)]
    for i, (t0, lab, col) in enumerate(pigs):
        x = 560 + i * 330
        show(c, t, t0, x, 400, sc(piggy, s=0.7), anim="drop")
        show(c, t, t0 + 0.1, x, 530, M(lab, 54, col), anim="fade")
    show(c, t, w("ninguém", 516.4), 890, 620, T("ninguém vai depositar isso por você", 52, RED), anim="fade")
    show(c, t, w("assiste", 520.2), 1180, 850, sc(video_card, "Demitido hoje?", "a conta da reserva de emergência", s=0.5), anim="pop")
    hero(c, t, 1600, 1050, 0.75, [(0, "present_l"), (w("assiste", 520.2), "point_l")], [(0, "happy")], appear=506.1, look=-1)


def s35(c, t):  # 525.7 - 548.1  recapitulando
    show(c, t, 525.8, 960, 120, M("Recapitulando", 74, NAVY), anim="up")
    rows = [(w("cinco", 527.0), "R$ 5.000 de CLT valem ~R$ 5.400 por mês", CLTC),
            (w("sete", 534.8), "R$ 7.000 de PJ, com férias, viram ~R$ 5.500", PJC),
            (w("diferença", 539.6), "~R$ 130 por mês de diferença, sem rede de proteção", NAVY),
            (w("fator", 545.0), "sem o fator R, o PJ ganha menos que a CLT", RED)]
    for i, (t0, lab, col) in enumerate(rows):
        y = 290 + i * 150
        show(c, t, t0, 610, y, lambda c, n=i + 1, col=col: (circle(c, 0, 0, 34, col, 5),
                                                         text(c, str(n), 0, 2, 44, MARKER, WHITE)), anim="pop")
        show(c, t, t0 + 0.1, 670, y, L(lab, 50, INK), anim="left")
    hero(c, t, 300, 1040, 0.8, [(0, "present")], [(0, "happy")], appear=525.8, look=1)


def s36(c, t):  # 548.1 - END  comentários + inscreva-se
    show(c, t, 548.2, 1080, 400, lambda c: speech(c, 1000, 300, -360, 190), anim="pop")
    show(c, t, 548.4, 1080, 340, T("Me conta nos comentários:", 52, DGRAY), anim="fade")
    show(c, t, w("clt", 548.5), 1080, 430, M("você é CLT ou PJ? Trocaria?", 54, NAVY), anim="fade")
    show(c, t, w("inscreve", 553.0), 1080, 700, sc(subscribe_btn, s=1.0), anim="pop")
    hero(c, t, 340, 1010, 1.1, [(0, "wave")], [(0, "happy")], appear=548.2, look=1)
    show(c, t, 548.4, 1080, 900, T("conteúdo educativo, não é recomendação de investimento", 36, DGRAY), anim="fade")


def s37(c, t):  # END - fim (5 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres: vídeo à esquerda (x 170-950, y 300-740) e inscrever-se à direita (~1450, 520).
    show(c, t, END + 0.1, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, END + 0.4, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, END + 0.4, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (END + 2.5, "relax")], [(0, "happy")], appear=END + 0.1)


SCENES = [
    (0.0, 11.5, s01), (11.5, 27.3, s02), (27.3, 35.5, s03), (35.5, 46.6, s04), (46.6, 70.4, s05),
    (70.4, 90.8, s06), (90.8, 103.2, s07), (103.2, 116.3, s08), (116.3, 134.1, s09), (134.1, 146.4, s10),
    (146.4, 163.4, s11), (163.4, O2, s12),
    (O2, 178.0, s13), (178.0, 204.6, s14), (204.6, 212.5, s15), (212.5, 225.1, s16), (225.1, 245.3, s17),
    (245.3, 256.4, s18), (256.4, 274.2, s19), (274.2, 292.1, s20), (292.1, 313.5, s21), (313.5, 329.1, s22),
    (329.1, O3, s23),
    (O3, 372.3, s24), (372.3, 392.8, s25), (392.8, 416.0, s26), (416.0, 434.9, s27), (434.9, 452.1, s28),
    (452.1, 465.1, s29), (465.1, 479.1, s30), (479.1, 481.7, s31), (481.7, 496.1, s32), (496.1, 506.0, s33),
    (506.0, 525.7, s34), (525.7, 548.1, s35), (548.1, END, s36), (END, 999.0, s37),
]

# só toques pontuais, sem ruído: R$ 5.400 / R$ 130 por mês / R$ 59.325 / empate R$ 6.840
SFX = [(w("quatrocentos", 169.2), "soft_ding"), (w("trinta", 312.0), "tum"), (w("cinquenta", 332.0), "tum"),
       (w("seis", 403.0), "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")
