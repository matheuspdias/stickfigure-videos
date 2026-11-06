"""Dividir as contas no casal: 50/50, proporcional ou tudo junto? Só TikTok: vertical nativo 1080x1920, ~76 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Tom neutro: mostra a conta dos três jeitos sem dizer qual é o certo; o debate fica pros comentários.
Contas: ele R$ 5.000, ela R$ 2.000 (renda R$ 7.000), casa R$ 3.000.
  50/50: 1.500 cada -> sobra 3.500 / 500 (30% / 75% do salário).
  Proporcional: 5/7 = 71,4% -> 2.142,86 (~2.140); 2/7 -> 857,14 (~860); os dois 42,86% (~43%); sobra 2.860 / 1.140.
  Tudo junto: 7.000 - 3.000 = 4.000 pra dividir como combinarem."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1290
HIM = BLUE      # camiseta dele
HER = ORANGE    # camiseta dela

SFX = [(22.15, "tum"), (42.65, "tum"), (61.0, "soft_ding"), (74.85, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def ele(c, t, x, s, poses, exprs, y=FY, **kw):
    kw.setdefault("shirt", HIM); kw.setdefault("hair", "spiky"); kw.setdefault("fid", 2)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def ela(c, t, x, s, poses, exprs, y=FY, **kw):
    kw.setdefault("shirt", HER); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def mk_w(c, s, size):
    parts = s.split("2.")
    return sum(text_w(c, p, size) for p in parts) + (len(parts) - 1) * (text_w(c, "2", size) + text_w(c, ".", size) + size * 0.07)


def mk_text(c, s, x, y, size, col=INK, align="c"):
    """Permanent Marker: o ponto de milhar depois do "2" encosta no pé do 2; desenha com um respiro antes do ponto"""
    w = mk_w(c, s, size)
    cx = x - w / 2 if align == "c" else x
    parts = s.split("2.")
    for i, p in enumerate(parts):
        cx += text(c, p, cx, y, size, MARKER, col, align="l")
        if i < len(parts) - 1:
            cx += text(c, "2", cx, y, size, MARKER, col, align="l") + size * 0.07
            cx += text(c, ".", cx, y, size, MARKER, col, align="l")


def MK(s, size=60, col=INK):
    return lambda c: mk_text(c, s, 0, 0, size, col)


def mhl(s, size, bg=LYELLOW, col=INK, pad=22):
    def f(c):
        w = mk_w(c, s, size)
        c.save(); c.rotate(-0.015)
        rrect(c, -w / 2 - pad, -size * 0.62, w + 2 * pad, size * 1.24, 14); rgb(c, bg); c.fill()
        mk_text(c, s, 0, 0, size, col)
        c.restore()
    return f


def tag(s, col, size=50, tcol=WHITE):
    """etiqueta colorida tipo crachá"""
    def f(c):
        w = mk_w(c, s, size) + 44
        rrect(c, -w / 2, -size * 0.7, w, size * 1.4, 14); fs(c, col, 5)
        mk_text(c, s, 0, 3, size, tcol)
    return f


def heart(c, r=50, col=RED):
    c.move_to(0, r * 0.95)
    c.curve_to(-r * 1.6, -r * 0.1, -r * 0.9, -r * 1.3, 0, -r * 0.45)
    c.curve_to(r * 0.9, -r * 1.3, r * 1.6, -r * 0.1, 0, r * 0.95)
    c.close_path(); fs(c, col, 5)


def wifi(c):
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for r in (40, 80, 120):
        c.new_sub_path(); c.arc(0, 50, r, math.pi * 1.25, math.pi * 1.75)
        rgb(c, NAVY); c.set_line_width(16); c.stroke()
    circle(c, 0, 50, 14, NAVY, 0)


def jeito(c, t, t0, n, s):
    """título do jeito: número num círculo dourado + nome"""
    def f(c):
        w = text_w(c, s, 70)
        x0 = -(w + 120) / 2
        circle(c, x0 + 45, 0, 48, GOLD, 6)
        text(c, str(n), x0 + 45, 4, 64, MARKER, INK)
        text(c, s, x0 + 120, 0, 70, MARKER, NAVY, align="l")
    show(c, t, t0, CX, 270, f, anim="stamp", d=0.3)


# barras de salário (base em BY; R$ 5.000 = 560 px)
BY = 1060
PX = 500 / 5000
BX = {"ele": 260, "ela": 780}
BW = 210


def sal_bar(c, t, who, sal, pay, t_bar, t_pay, t_sobra, pay_s, sobra_s, pct_s=None, t_pct=None):
    x = BX[who]
    col = HIM if who == "ele" else HER
    k = ease_out(prog(t, t_bar, 0.5))
    if k <= 0:
        return
    H = sal * PX * k
    # salário inteiro (contorno na cor da pessoa)
    rrect(c, x - BW / 2, BY - H, BW, H, 12); fs(c, WHITE, 6)
    # parte que vai pras contas (vermelho, de baixo pra cima)
    kp = ease_out(prog(t, t_pay, 0.45))
    hp = pay * PX * kp
    if hp > 1:
        c.rectangle(x - BW / 2 + 3, BY - hp, BW - 6, hp - 3); rgb(c, (1, 0.8, 0.76)); c.fill()
        line(c, x - BW / 2 + 3, BY - hp, x + BW / 2 - 3, BY - hp, 5, RED)
    # sobra (verde, em cima)
    ks = ease_out(prog(t, t_sobra, 0.45))
    if ks > 0:
        top = BY - sal * PX
        c.rectangle(x - BW / 2 + 3, top + 3, BW - 6, (sal - pay) * PX * ks - 3); rgb(c, LGREEN, 0.9); c.fill()
    rrect(c, x - BW / 2, BY - H, BW, H, 12); rgb(c, INK); c.set_line_width(6); c.stroke()
    line(c, x - BW / 2 - 20, BY, x + BW / 2 + 20, BY, 6)
    # rótulos
    hp_full = pay * PX
    one_line = hp_full < 140
    if pct_s and not one_line:
        show(c, t, t_pay + 0.2, x, BY - hp_full / 2 - 26, MK(pay_s, 46, RED), anim="pop")
        show(c, t, t_pct, x, BY - hp_full / 2 + 34, lambda c: hl(c, pct_s, 0, 0, 36, WHITE, INK, HAND, pad=12), anim="stamp")
    else:
        show(c, t, t_pay + 0.2, x, BY - hp_full / 2, MK(pay_s, 46 if not one_line else 42, RED), anim="pop")
    top = BY - sal * PX
    show(c, t, t_sobra, x, top - 40, mhl(sobra_s, 58, LGREEN), anim="stamp", d=0.3)
    text(c, ("ELE" if who == "ele" else "ELA") + " · " + ("R$ 5 mil" if sal == 5000 else "R$ 2 mil"),
         x, BY + 42, 40, MARKER, col)


def legend(c, t, t0):
    def f(c):
        c.rectangle(-300, -16, 32, 32); fs(c, (1, 0.8, 0.76), 4)
        text(c, "contas", -258, 0, 38, HAND, INK, align="l")
        c.rectangle(-60, -16, 32, 32); fs(c, LGREEN, 4)
        text(c, "sobra", -18, 0, 38, HAND, INK, align="l")
        c.rectangle(160, -16, 32, 32); fs(c, WHITE, 4)
        text(c, "salário", 202, 0, 38, HAND, INK, align="l")
    show(c, t, t0, CX - 20, 365, f, anim="fade")


def couple_small(c, t, exprs_him=((0, "neutral"),), exprs_her=((0, "neutral"),), poses_him=((0, "relax"),), poses_her=((0, "relax"),)):
    ele(c, t, BX["ele"], 0.33, poses_him, exprs_him, look=0.4)
    ela(c, t, BX["ela"], 0.33, poses_her, exprs_her, look=-0.4)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.5  gancho
    floor(c)
    show(c, t, 0.0, CX, 270, lambda c: hl(c, "QUEM PAGA O QUÊ?", 0, 0, 84, NAVY, WHITE), anim="stamp", d=0.25)
    ele(c, t, 290, 0.62, [(0, "present"), (2.4, "relax"), (6.1, "think")], [(0, "happy"), (6.1, "think")], appear=0.0, look=0.5)
    ela(c, t, 750, 0.62, [(0, "relax"), (1.6, "present_l"), (3.6, "relax"), (6.1, "think_l")], [(0, "happy"), (6.1, "think")], appear=0.0, look=-0.5)
    show(c, t, 0.55, 290, 950, tag("R$ 5 mil", HIM, 60), anim="drop", d=0.35)
    show(c, t, 2.5, 750, 950, tag("R$ 2 mil", HER, 60), anim="drop", d=0.35)
    # contas da casa
    def conta(c):
        rrect(c, -330, -110, 660, 220, 24); fs(c, WHITE, 6)
        c.rectangle(-327, -107, 18, 214); rgb(c, RED); c.fill()
        text(c, "contas da casa", 10, -50, 54, HAND, INK)
        if t < 4.85:
            text(c, "R$ ???", 10, 35, 96, MARKER, LGRAY)
        else:
            k = ease_out(prog(t, 4.85, 0.3))
            c.save(); c.translate(10, 35); c.scale(0.6 + 0.4 * k, 0.6 + 0.4 * k)
            mk_text(c, "R$ 3 mil", 0, 0, 96, RED); c.restore()
    show(c, t, 0.0, CX, 520, conta, anim="pop", d=0.25, t1=7.4)
    show(c, t, 6.05, CX, 720, lambda c: hl(c, "como vocês dividiriam?", 0, 0, 60, LYELLOW), anim="stamp", t1=7.4)
    # pausa: interrogação grande
    k = 1 + 0.06 * math.sin((t - 7.4) * 8)
    show(c, t, 7.4, CX, 620, lambda c: qmark(c, 520 * k, NAVY), anim="pop", d=0.3)


def s02(c, t):  # 9.5 - 14.6  as contas somam 3 mil
    floor(c)
    show(c, t, 9.55, CX, 270, M("AS CONTAS DA CASA", 74, NAVY), anim="up")
    items = [(9.6, 230, 520, lambda c: house(c), "aluguel", 0.62),
             (10.5, 560, 520, lambda c: cart(c), "mercado", 0.7),
             (11.28, 230, 820, lambda c: bulb(c), "luz", 0.75),
             (11.76, 560, 820, wifi, "internet", 0.9)]
    for t0, x, y, fn, lab, s in items:
        show(c, t, t0, x, y, icon_label(fn, lab, 48, 140, s=s), anim="pop")
    show(c, t, 12.8, 400, 1090, lambda c: hl(c, "= R$ 3 mil por mês", 0, 0, 64, (1, 0.8, 0.76)), anim="stamp", d=0.3)
    hero(c, t, 840, FY, 0.55, [(0, "present_l"), (12.8, "point_l")], [(0, "neutral"), (12.8, "confident")], appear=9.5, look=-1)


def s03(c, t):  # 14.6 - 28.0  jeito 1: 50/50
    floor(c)
    jeito(c, t, 14.75, 1, "50/50")
    legend(c, t, 15.0)
    sal_bar(c, t, "ele", 5000, 1500, 15.0, 17.35, 19.0, "R$ 1.500", "R$ 3.500", "30% do salário", 26.5)
    sal_bar(c, t, "ela", 2000, 1500, 15.2, 17.35, 21.6, "R$ 1.500", "R$ 500", "75% do salário", 23.3)
    show(c, t, 16.85, CX, 560, T("cada um paga", 46), anim="fade")
    show(c, t, 16.95, CX, 625, MK("R$ 1.500", 60, RED), anim="pop")
    couple_small(c, t, [(0, "neutral"), (19.4, "happy")], [(0, "neutral"), (22.2, "think")],
                 [(0, "relax"), (19.4, "thumb")], [(0, "relax"), (22.2, "think")])


def s04(c, t):  # 28.0 - 36.0  jeito 2: proporcional (a fatia de cada um na renda)
    floor(c)
    jeito(c, t, 28.25, 2, "PROPORCIONAL")
    show(c, t, 29.6, CX, 360, T("à renda", 52, DGRAY), anim="fade")
    # barra da renda do casal
    x0, x1, y = 120, 920, 640
    k = ease_out(prog(t, 31.15, 0.6))
    if k > 0:
        w = (x1 - x0) * k
        xm = x0 + (x1 - x0) * 5 / 7
        rrect(c, x0, y - 70, w, 140, 16); fs(c, WHITE, 6)
        c.rectangle(x0 + 3, y - 67, min(w, xm - x0) - 3, 134); rgb(c, HIM, 0.85); c.fill()
        if x0 + w > xm:
            c.rectangle(xm, y - 67, x0 + w - xm - 3, 134); rgb(c, HER, 0.85); c.fill()
            line(c, xm, y - 70, xm, y + 70, 6)
        rrect(c, x0, y - 70, w, 140, 16); rgb(c, INK); c.set_line_width(6); c.stroke()
        if k > 0.95:
            mk_text(c, "R$ 5 mil", (x0 + xm) / 2, y + 4, 60, WHITE)
            mk_text(c, "R$ 2 mil", (xm + x1) / 2, y + 4, 46, WHITE)
    show(c, t, 32.4, CX, 490, lambda c: hl(c, "juntos: R$ 7 mil", 0, 0, 60, LYELLOW), anim="stamp")
    show(c, t, 34.2, (x0 + x0 + (x1 - x0) * 5 / 7) / 2, 800, M("71%", 110, HIM), anim="stamp", d=0.3)
    show(c, t, 34.6, (x0 + (x1 - x0) * 5 / 7 + x1) / 2, 800, M("29%", 80, HER), anim="stamp", d=0.3)
    show(c, t, 34.9, CX, 905, T("da renda do casal", 46, DGRAY), anim="fade")
    ele(c, t, 230, 0.5, [(0, "relax"), (34.2, "hips")], [(0, "neutral"), (34.2, "confident")], look=0.5)
    ela(c, t, 810, 0.5, [(0, "relax")], [(0, "neutral")], look=-0.5)
    hero(c, t, CX, FY, 0.5, [(0, "relax"), (31.2, "point_ru"), (34.2, "present")], [(0, "neutral"), (31.2, "confident")], appear=28.3, look=0)


def s05(c, t):  # 36.0 - 49.65  jeito 2: as barras
    floor(c)
    jeito(c, t, 36.0, 2, "PROPORCIONAL")
    legend(c, t, 36.0)
    sal_bar(c, t, "ele", 5000, 2140, 36.0, 36.35, 44.85, "R$ 2.140", "R$ 2.860")
    sal_bar(c, t, "ela", 2000, 860, 36.1, 39.1, 47.95, "R$ 860", "R$ 1.140")
    # os dois comprometem ~43%
    def pct(c):
        circle(c, 0, 0, 105, GOLD, 7)
        text(c, "43%", 0, -12, 76, MARKER, INK)
        text(c, "pros dois", 0, 50, 34, HAND, INK)
    show(c, t, 42.65, CX, 860, pct, anim="stamp", d=0.35)
    show(c, t, 42.65, CX, 990, T("do salário", 40, DGRAY), anim="fade")
    couple_small(c, t, [(0, "neutral"), (42.7, "happy")], [(0, "neutral"), (42.7, "happy")],
                 [(0, "relax"), (42.7, "thumb")], [(0, "relax"), (42.7, "thumb")])


def s06(c, t):  # 49.65 - 54.4  e pode ser ao contrário
    floor(c)
    show(c, t, 49.75, CX, 270, M("PODE SER", 80, NAVY), anim="stamp", d=0.3)
    show(c, t, 50.4, CX, 380, lambda c: hl(c, "AO CONTRÁRIO", 0, 0, 88, NAVY, WHITE), anim="stamp", d=0.3)
    ele(c, t, 290, 0.62, [(0, "relax"), (51.3, "shrug")], [(0, "happy")], look=0.5)
    ela(c, t, 750, 0.62, [(0, "relax"), (51.3, "shrug")], [(0, "happy")], look=-0.5)
    # as etiquetas trocam de dono
    k = ease_in_out(prog(t, 50.5, 0.9)) if "ease_in_out" in globals() else ease_out(prog(t, 50.5, 0.9))
    lift = math.sin(k * math.pi) * 140
    for s, col, xa, xb in (("R$ 5 mil", GREEN, 290, 750), ("R$ 2 mil", GREEN, 750, 290)):
        x = xa + (xb - xa) * k
        c.save(); c.translate(x, 950 - lift * (1 if xa < xb else 0.4)); tag(s, NAVY, 60)(c); c.restore()
    show(c, t, 51.3, CX, 570, T("tanto faz quem ganha mais:", 54), anim="up")
    show(c, t, 53.0, CX, 680, lambda c: hl(c, "a conta é a mesma", 0, 0, 66, LYELLOW), anim="stamp")


def s07(c, t):  # 54.4 - 64.1  jeito 3: tudo junto
    floor(c)
    jeito(c, t, 54.55, 3, "TUDO JUNTO")
    show(c, t, 57.2, CX, 620, icon_label(lambda c: piggy(c, GOLD), "conta do casal", 46, 150, s=1.0), anim="pop")
    # salários entrando no cofre
    for t0, xa in ((57.3, 200), (57.7, 840)):
        k = ease_out(prog(t, t0, 0.8))
        if 0 < k < 1:
            x = xa + (CX - xa) * k
            y = 1000 + (580 - 1000) * k - math.sin(k * math.pi) * 160
            c.save(); c.translate(x, y); c.scale(0.5, 0.5); bill(c); c.restore()
    show(c, t, 58.5, CX, 420, mhl("R$ 7 mil", 72, LYELLOW), anim="stamp")
    show(c, t, 59.5, CX, 880, T("- R$ 3 mil de contas", 54, RED), anim="up")
    show(c, t, 61.0, CX, 980, mhl("= R$ 4 mil", 76, LGREEN), anim="stamp", d=0.3)
    show(c, t, 62.6, CX, 1090, T("vocês combinam como dividir", 44), anim="fade")
    ele(c, t, 190, 0.42, [(0, "relax"), (57.2, "point_ru"), (62.6, "thumb")], [(0, "neutral"), (61.0, "happy")], look=0.5)
    ela(c, t, 850, 0.42, [(0, "relax"), (57.6, "point_lu"), (62.6, "thumb")], [(0, "neutral"), (61.0, "happy")], look=-0.5)


def s08(c, t):  # 64.1 - 69.4  não existe jeito certo
    floor(c)
    show(c, t, 64.25, CX, 270, M("NÃO EXISTE", 84, NAVY), anim="stamp", d=0.3)
    show(c, t, 64.85, CX, 385, lambda c: hl(c, "JEITO CERTO", 0, 0, 92, NAVY, WHITE), anim="stamp", d=0.3)
    show(c, t, 66.7, CX, 540, lambda c: hl(c, "conversem", 0, 0, 66, LYELLOW), anim="stamp")
    show(c, t, 67.0, 300, 900, group(lambda c: speech(c, 200, 110, 40, 90), T("...", 70)), anim="pop")
    show(c, t, 67.4, 740, 900, group(lambda c: speech(c, 200, 110, -40, 90), T("...", 70)), anim="pop")
    show(c, t, 68.2, CX, 700, sc(balance, 0.0, s=0.55), anim="pop")
    show(c, t, 68.6, CX, 800, T("justo pros dois", 46), anim="fade")
    ele(c, t, 270, 0.55, [(0, "relax"), (66.7, "present")], [(0, "neutral"), (66.7, "happy")], look=0.6)
    ela(c, t, 770, 0.55, [(0, "relax"), (66.7, "present_l")], [(0, "neutral"), (66.7, "happy")], look=-0.6)


def s09(c, t):  # 69.4 - fim  pergunta + segue
    floor(c)
    show(c, t, 69.55, CX, 255, M("E NA SUA CASA,", 76, NAVY), anim="stamp", d=0.3)
    show(c, t, 70.55, CX, 355, M("COMO É?", 90, NAVY), anim="stamp", d=0.3)
    chips = [(71.7, "1", "50/50"), (72.2, "2", "PROPORCIONAL"), (72.9, "3", "TUDO JUNTO")]
    for i, (t0, n, s) in enumerate(chips):
        def f(c, n=n, s=s):
            rrect(c, -330, -48, 660, 96, 20); fs(c, WHITE, 5)
            circle(c, -270, 0, 36, GOLD, 5)
            text(c, n, -270, 3, 50, MARKER, INK)
            text(c, s, -210, 2, 54, MARKER, NAVY, align="l")
        show(c, t, t0, CX, 485 + i * 115, f, anim="left", d=0.3)
    def amor(c):
        heart(c, 34)
        text(c, "marca seu amor", 50, 0, 52, HAND, INK, align="l")
    show(c, t, 73.6, CX - 170, 830, amor, anim="pop")
    show(c, t, 74.8, CX, 950, lambda c: ribbon(c, "SEGUE PRA MAIS CONTAS", NAVY, 58), anim="stamp", d=0.3)
    hero(c, t, CX, FY, 0.6, [(0, "present"), (71.7, "point_lu"), (74.8, "finger_up")],
         [(0, "happy"), (74.8, "grin")], appear=69.5, look=0)


SCENES = [
    (0.0, 9.5, s01), (9.5, 14.6, s02), (14.6, 28.0, s03), (28.0, 36.0, s04), (36.0, 49.65, s05),
    (49.65, 54.4, s06), (54.4, 64.1, s07), (64.1, 69.4, s08), (69.4, 999.0, s09),
]
