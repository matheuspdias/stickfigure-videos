"""POV: o salário caiu dia 5 e no dia 12 já acabou. Só TikTok: vertical nativo 1080x1920, 96,3 s.
Formato POV (modelo: videos/pov-fatura-janeiro): o bonequinho principal é VOCÊ (camiseta laranja);
O Consultor só entra na virada (60,4 s). Faixa POV fixa no topo, calendário no canto e saldo grande
caindo a cada cena (0 a 60,3 s).
Layout: faixa POV y 170-320, HUD (calendário + saldo) y 380-560, palco y 600-1280 (chão FY=1280),
legendas do tiktok.py em y~1460; nada importante em x > 930.
Contas: 3.000 -1.000 = 2.000 -700 = 1.300 -300 = 1.000 -500 = 500 -200 = 300 -250 = 50 -100 = -50.
Fixo 1.000+700+300+500 = 2.500 (sobravam 500). Vazamento 200+250+100 = 550/mês = 6.600/ano."""
import math

from engine import *  # noqa

VERTICAL = True

CX = 540
FY = 1280
YX = 270          # x de VOCÊ em pé
YS = 0.8
POV_END = 60.3
PINKISH = (1, 0.8, 0.76)

SFX = [(2.0, "soft_ding"), (55.11, "tum"), (79.67, "tum"), (85.87, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow",
            "appear", "key", "transition")

# (tempo em que o valor é falado, saldo depois)
SALDO = [(3.6, 3000), (10.8, 2000), (17.33, 1300), (23.99, 1000), (29.27, 500), (40.15, 300), (46.22, 50),
         (53.11, -50)]
DIAS = [(0.0, "5"), (14.24, "6"), (20.32, "7"), (26.96, "8"), (33.92, "9"), (42.88, "10"), (49.43, "11"),
        (49.67, "12")]


# ---------------------------------------------------------------- helpers
def brl(v, sign=False):
    s = f"{abs(int(v)):,}".replace(",", ".").replace("2.", "2 .")
    pre = "-" if v < 0 else ("+ " if sign else "")
    return f"{pre}R$ {s}"


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def pov_alpha(t):
    return 1.0 if t < POV_END else 1 - prog(t, POV_END, 0.35)


def pov_banner(c, t):
    a = pov_alpha(t)
    if a <= 0:
        return
    c.push_group()
    rrect(c, 50, 170, 980, 150, 22); fs(c, INK, 0)
    text(c, "POV: o salário caiu dia 5", 540, 222, 54, MARKER, WHITE)
    text(c, "e no dia 12 já acabou", 540, 282, 54, MARKER, GOLD)
    c.pop_group_to_source(); c.paint_with_alpha(a)


def saldo_at(t):
    """saldo exibido (rola do valor anterior ao novo em 0,5 s) e tempo da última queda"""
    prev, last = 0, None
    for tt, v in SALDO:
        if t < tt:
            break
        k = ease_out(prog(t, tt, 0.5))
        val = prev + (v - prev) * k
        prev, last = v, tt
    else:
        val = prev
    if last is None:
        return 0, None
    return val, last


def hud(c, t):
    """calendário (canto esquerdo) + saldo grande, só na parte POV"""
    a = pov_alpha(t)
    if a <= 0:
        return
    c.push_group()
    # calendário: pula a cada dia, com um 'pop'
    day, t_day = "5", 0.0
    for tt, d in DIAS:
        if t >= tt:
            day, t_day = d, tt
    k = 1 + 0.25 * (1 - ease_out(prog(t, t_day, 0.35))) if t_day > 0 else 1
    c.save(); c.translate(170, 478); c.scale(1.05 * k, 1.05 * k)
    calendar(c, day, RED, 78 if len(day) == 1 else 70)
    c.restore()
    text(c, "outubro", 170, 590, 34, HAND, DGRAY)
    # saldo
    val, last = saldo_at(t)
    neg = val < 0 or (last is not None and last >= 53.11 and t > 53.3)
    flash = last is not None and t - last < 0.9 and last > 4
    col = RED if (neg or flash) else (ORANGE if val <= 50 and last else (GREEN if last else INK))
    rrect(c, 330, 382, 590, 200, 26); fs(c, WHITE, 6 if not neg else 0)
    if neg:
        rrect(c, 330, 382, 590, 200, 26); rgb(c, RED); c.set_line_width(10); c.stroke()
    text(c, "saldo da conta", 625, 420, 40, HAND, DGRAY)
    shake = math.sin(t * 60) * 8 * (1 - prog(t, last, 0.4)) if (last and last > 4 and t - last < 0.4) else 0
    v = round(val / 10) * 10 if abs(val) > 60 else round(val)
    text(c, brl(v), 625 + shake, 505, 112, MARKER, col)
    c.pop_group_to_source(); c.paint_with_alpha(a)


def base(c, t):
    floor(c)
    pov_banner(c, t)
    hud(c, t)


def you(c, t, x, poses, exprs, s=YS, y=FY, **kw):
    """VOCÊ: pessoa comum (camiseta laranja, cabelo espetado)"""
    kw.setdefault("shirt", ORANGE); kw.setdefault("hair", "spiky"); kw.setdefault("fid", 2)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def you_floor(c, t, t0, s=YS):
    """VOCÊ caindo de costas no chão a partir de t0 (deitado depois de 0,7 s), cabeça para a esquerda"""
    k = ease_io(prog(t, t0, 0.7))
    c.save()
    c.translate(YX + 250 * k, FY - 52 * k * s / YS)
    c.rotate(-1.52 * k)
    you(c, t, 0, [(0, "head"), (t0, "arms_up")], [(0, "desperate"), (t0 + 0.7, "shocked")], s=s, y=0, look=0)
    c.restore()


def bubble(c, t, t0, x, y, s, w=380, h=110, tx=-60, ty=150, size=48, col=INK, t1=None):
    show(c, t, t0, x, y, group(lambda c: speech(c, w, h, tx, ty), T(s, size, col)), anim="pop", d=0.3, t1=t1)


def wifi(c, col=BLUE):
    for r in (30, 62, 94):
        c.new_sub_path(); c.arc(0, 40, r, math.pi * 1.25, math.pi * 1.75)
        rgb(c, col); c.set_line_width(14); c.set_line_cap(1); c.stroke()
    circle(c, 0, 40, 12, col, 0)


def minus(val):
    return lambda c: hl(c, "- " + brl(val), 0, 0, 84, PINKISH, RED)


def expense(c, t, label, t_lab, icon, val, t_val, t1=None, sub=None, t_sub=None):
    """rótulo da conta, ícone e o valor carimbado quando a narração chega nele"""
    show(c, t, t_lab, 620, 680, M(label, 62 if len(label) < 14 else 54, INK), anim="up", t1=t1)
    if sub:
        show(c, t, t_sub, 660, 752, T(sub, 46, DGRAY), anim="up", t1=t1)
    if icon:
        show(c, t, t_lab + 0.1, 680, 900, icon, anim="pop", t1=t1)
    show(c, t, t_val, 660, 1110, minus(val), anim="stamp", d=0.35, t1=t1)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 8.2  dia 5: plim, caiu o salário, você comemora
    base(c, t)
    def big_phone(c):
        c.save(); c.scale(1.5, 1.5); phone(c); c.restore()
        text(c, "BANCO", 0, -40, 32, MARKER, NAVY)
    show(c, t, 0.4, 640, 960, big_phone, anim="pop", t1=4.9)
    show(c, t, 1.2, 820, 790, M("plim!", 60, GOLD), anim="pop", d=0.3, t1=4.9)
    def notif(c):
        rrect(c, -290, -70, 580, 140, 26); fs(c, WHITE, 6)
        circle(c, -225, 0, 34, GREEN, 0); text(c, "$", -225, 0, 44, MARKER, WHITE)
        text(c, "Salário caiu!", -170, -28, 40, HAND, DGRAY, align="l")
        text(c, brl(3000, sign=True), -170, 26, 58, MARKER, GREEN, align="l")
    show(c, t, 2.0, 620, 760 if t < 5.0 else 760 - 60 * ease_out(prog(t, 5.0, 0.4)), notif, anim="drop", d=0.5)
    # comemoração: moedas e brilhos
    if t > 5.12:
        for i in range(9):
            kk = prog(t, 5.12 + i * 0.17, 1.6)
            if 0 < kk < 1:
                x = 420 + (i * 137) % 520
                y = 820 + 420 * kk - 160 * math.sin(kk * math.pi)
                c.save(); c.translate(x, y); c.rotate(kk * 5 + i); c.scale(0.32, 0.32)
                c.push_group(); coin(c); c.pop_group_to_source(); c.paint_with_alpha(1 - kk * kk); c.restore()
        for i, (x, y) in enumerate(((120, 860), (430, 880), (160, 1100), (460, 1040))):
            show(c, t, 5.2 + i * 0.12, x, y, sc(sparkle, 30 + 6 * (i % 2)), anim="pop", d=0.3)
        show(c, t, 6.9, 700, 1080, M("Mega-Sena!", 64, GREEN), anim="stamp", d=0.3)
    you(c, t, YX, [(0, "stand"), (2.0, "hold"), (5.12, "arms_up")],
        [(0, "neutral"), (2.0, "shocked"), (4.0, "happy"), (5.12, "grin")], look=0.6)


def s02(c, t):  # 8.2 - 14.1  mesmo dia: aluguel 1.000 -> sobram 2.000, tranquilo
    base(c, t)
    show(c, t, 8.32, 170, 650, T("mesmo dia", 40, RED), anim="pop", d=0.3)
    expense(c, t, "Aluguel", 9.44, sc(house, s=1.0), 1000, 10.8)
    you(c, t, YX, [(0, "stand"), (13.1, "thumb")], [(0, "happy"), (10.8, "neutral"), (13.1, "grin")], look=0.6)
    bubble(c, t, 13.12, 290, 760, "tranquilo", w=320)


def s03(c, t):  # 14.1 - 20.2  dia 6: fatura 700 -> 1.300
    base(c, t)
    expense(c, t, "Fatura do cartão", 15.36, sc(card, s=1.35), 700, 17.33)
    you(c, t, YX, [(0, "relax"), (17.4, "hips")], [(0, "neutral"), (17.4, "worried")], look=0.6)
    bubble(c, t, 18.4, 290, 760, "tá, previsto", w=330, size=44)


def s04(c, t):  # 20.2 - 26.8  dia 7: luz, internet, celular 300 -> 1.000, ainda dá
    base(c, t)
    show(c, t, 21.52, 600, 680, M("Luz, internet, celular", 50, INK), anim="up")
    show(c, t, 21.52, 510, 900, icon_label(bulb, "luz", 40, dy=110, s=0.95), anim="pop")
    show(c, t, 22.36, 680, 880, icon_label(wifi, "internet", 40, dy=130), anim="pop")
    show(c, t, 22.96, 850, 880, icon_label(phone, "celular", 40, dy=130, s=0.75), anim="pop")
    show(c, t, 23.99, 660, 1110, minus(300), anim="stamp", d=0.35)
    you(c, t, YX, [(0, "relax"), (25.9, "shrug")], [(0, "neutral"), (24.0, "worried"), (25.9, "neutral")], look=0.6)
    bubble(c, t, 25.92, 290, 760, "ainda dá", w=300)


def s05(c, t):  # 26.8 - 33.8  dia 8: mercado 500 -> 500, nem comprou besteira
    base(c, t)
    expense(c, t, "Mercado", 28.0, sc(cart, s=1.3), 500, 29.27)
    you(c, t, YX, [(0, "relax"), (29.3, "head"), (30.6, "hips")],
        [(0, "neutral"), (29.3, "shocked"), (30.6, "angry")], look=0.6)
    bubble(c, t, 30.6, 290, 760, "só o básico!", w=340, size=46)


def s06(c, t):  # 33.8 - 42.8  dia 9: "só hoje" delivery, Uber, de novo -> 200 -> 300
    base(c, t)
    show(c, t, 34.48, 660, 680, M('"Só hoje"', 70, INK), anim="up")
    show(c, t, 34.6, 530, 900, icon_label(sandwich, "delivery", 42, dy=120, s=0.85), anim="pop")
    show(c, t, 36.32, 800, 910, icon_label(lambda c: car(c, DGRAY), "Uber", 42, dy=120, s=0.55), anim="pop")
    if t >= 38.8:
        n = "x3"
        show(c, t, 38.8, 860, 760, lambda c: text(c, n, 0, 0, 90, MARKER, RED, outline=WHITE, ow=12),
             anim="pop", d=0.25, rot=0.1)
    show(c, t, 40.15, 660, 1110, minus(200), anim="stamp", d=0.35)
    you(c, t, YX, [(0, "thumb"), (40.15, "head")], [(0, "grin"), (38.8, "happy"), (40.15, "shocked")], look=0.6)
    bubble(c, t, 34.6, 290, 760, "só hoje!", w=300, t1=39.9)


def s07(c, t):  # 42.8 - 49.3  dia 10: parcela do celular novo 250 -> 50
    base(c, t)
    def celular(c):
        c.save(); c.scale(1.25, 1.25); phone(c, PURPLE); c.restore()
        sparkle(c, 22)
    expense(c, t, "Parcela do celular", 43.84, celular, 250, 46.22)
    show(c, t, 44.64, 830, 800, lambda c: hl(c, "7 de 12", 0, 0, 44, LYELLOW), anim="stamp", d=0.3, rot=0.08)
    you(c, t, YX, [(0, "relax"), (46.3, "head")], [(0, "worried"), (46.3, "desperate")], look=0.6)
    bubble(c, t, 47.7, 290, 760, "cinquenta...", w=320, size=46)


def s08(c, t):  # 49.3 - 60.3  dia 12: assinaturas 100 -> -50; você no chão
    base(c, t)
    show(c, t, 49.43, 170, 650, T("pulou o 11", 38, DGRAY), anim="pop", d=0.3, t1=52.0)
    t1 = 54.15
    expense(c, t, "Assinaturas", 50.39, sc(tv, s=0.75), 100, 53.11, t1=t1,
            sub="que você nem lembra", t_sub=51.27)
    for i, (lab, x, y, r) in enumerate((("streaming", 520, 820, -0.1), ("música", 860, 830, 0.12),
                                         ("app de treino", 690, 1000, -0.04))):
        show(c, t, 51.6 + i * 0.3, x, y, lambda c, lab=lab: hl(c, lab, 0, 0, 36, LBLUE), anim="pop", d=0.25,
             rot=r, t1=t1)
    # o saldo no vermelho, grande no meio
    show(c, t, 55.11, 560, 730, lambda c: text(c, "-R$ 50", 0, 0, 200, MARKER, RED, outline=WHITE, ow=18),
         anim="stamp", d=0.35)
    show(c, t, 55.6, 600, 875, M("no vermelho", 64, RED), anim="up")
    if t < 57.27:
        you(c, t, YX, [(0, "relax"), (53.2, "head")], [(0, "worried"), (53.2, "shocked"), (55.2, "desperate")],
            look=0.6)
    else:
        you_floor(c, t, 57.27)


# ---------------------------------------------------------------- virada: O Consultor
FIXO = [(63.99, "aluguel", 1000), (64.87, "cartão", 700), (65.55, "contas da casa", 300), (66.47, "mercado", 500)]
VAZA = [(72.87, "delivery+Uber", 200), (74.39, "celular novo", 250), (75.67, "assinaturas", 100)]
T_ANO = 78.71


def montes(c, t):
    """os dois montes: FIXO (esquerda) e VAZAMENTO (direita)"""
    t1 = T_ANO - 0.1
    show(c, t, 62.95, 280, 420, lambda c: ribbon(c, "FIXO", NAVY, 50), anim="stamp", d=0.3, t1=t1)
    show(c, t, 63.2, 735, 420, lambda c: ribbon(c, "VAZAMENTO", RED, 36), anim="stamp", d=0.3, t1=t1)
    for i, (tt, lab, v) in enumerate(FIXO):
        y = 530 + i * 82
        show(c, t, tt, 70, y, lambda c, lab=lab: text(c, lab, 0, 0, 46, HAND, INK, align="l"), anim="left", d=0.3, t1=t1)
        show(c, t, tt, 495, y, lambda c, v=v: text(c, brl(v).replace("R$ ", ""), 0, 0, 50, MARKER, NAVY, align="r"),
             anim="left", d=0.3, t1=t1)
    if 67.27 < t < t1 + 0.3:
        k = ease_out(prog(t, 67.27, 0.4))
        line(c, 70, 868, 70 + 425 * k, 868, 6, INK)
    show(c, t, 68.51, 280, 930, lambda c: text(c, brl(2500), 0, 0, 74, MARKER, NAVY), anim="stamp", d=0.3, t1=t1)
    show(c, t, 69.91, 280, 1040, lambda c: hl(c, "sobravam R$ 500", 0, 0, 46, LGREEN, GREEN), anim="stamp",
         d=0.3, t1=t1)
    # vazamento
    for i, (tt, lab, v) in enumerate(VAZA):
        y = 530 + i * 82
        show(c, t, tt, 565, y, lambda c, lab=lab: text(c, lab, 0, 0, 42, HAND, INK, align="l"), anim="right", d=0.3, t1=t1)
        show(c, t, tt, 920, y, lambda c, v=v: text(c, str(v), 0, 0, 50, MARKER, RED, align="r"), anim="right", d=0.3,
             t1=t1)
    if 76.5 < t < t1 + 0.3:
        k = ease_out(prog(t, 76.5, 0.4))
        line(c, 565, 786, 565 + 355 * k, 786, 6, INK)
    show(c, t, 76.98, 745, 850, lambda c: text(c, brl(550), 0, 0, 74, MARKER, RED), anim="stamp", d=0.3, t1=t1)
    show(c, t, 78.07, 745, 935, T("por mês", 46, RED), anim="up", t1=t1)
    # gotas pingando ao lado do VAZAMENTO
    if 63.2 < t < t1:
        for i in range(3):
            kk = ((t - 63.2) * 0.8 + i / 3) % 1
            y = 455 + 60 * kk
            c.save(); c.translate(905, y)
            c.push_group()
            c.move_to(0, -14); c.curve_to(10, 0, 10, 10, 0, 12); c.curve_to(-10, 10, -10, 0, 0, -14)
            rgb(c, BLUE); c.fill()
            c.pop_group_to_source(); c.paint_with_alpha(1 - kk); c.restore()


def s09(c, t):  # 60.3 - 81.6  chega O Consultor: fixo x vazamento; 550/mês, 6.600/ano
    floor(c)
    pov_banner(c, t)
    hud(c, t)
    montes(c, t)
    # um ano de vazamento
    show(c, t, T_ANO, 540, 470, M("Em 1 ano", 70, INK), anim="up")
    show(c, t, T_ANO + 0.1, 540, 590, T("R$ 550  x  12 meses", 54, DGRAY), anim="up")
    show(c, t, 79.67, 540, 770, lambda c: text(c, brl(6600), 0, 0, 190, MARKER, RED, outline=WHITE, ow=16),
         anim="stamp", d=0.35)
    show(c, t, 80.4, 540, 930, lambda c: hl(c, "vazando", 0, 0, 64, PINKISH, RED), anim="stamp", d=0.3)
    hero(c, t, 870, FY, 0.6, [(0, "wave"), (62.9, "present_l"), (64.0, "point_lu"), (69.9, "thumb"),
                              (71.3, "point_lu"), (76.9, "finger_up")],
         [(0, "happy"), (62.9, "neutral"), (69.9, "happy"), (71.3, "neutral"), (76.9, "confident")],
         appear=60.4, look=-1, prop=("r", prop_calculator) if t > 76.9 else None)
    if t < T_ANO:
        you_floor(c, t, 0)  # continua deitado
    else:
        you(c, t, 200, [(0, "head")], [(0, "shocked"), (80.0, "desperate")], s=0.62, look=1)


def s10(c, t):  # 81.6 - 91.6  a regra: dia 5, antes de tudo, separe pra você + limite nos vazamentos
    floor(c)
    show(c, t, 81.75, 540, 400, lambda c: ribbon(c, "A REGRA", NAVY, 60), anim="stamp")
    show(c, t, 83.71, 230, 540, sc(calendar, "5", GREEN, 78, s=0.85), anim="pop")
    show(c, t, 83.83, 610, 540, T("dia 5, antes de tudo", 56), anim="up")
    show(c, t, 85.87, 540, 680, lambda c: hl(c, "SEPARE uma parte pra você", 0, 0, 58, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 86.4, 340, 820, group(sc(envelope, s=1.1), at(0, 30, M("VOCÊ", 30, NAVY))), anim="pop")
    show(c, t, 88.35, 650, 815, group(T("nem que seja", 40, DGRAY), at(0, 60, M(brl(50), 64, GREEN))), anim="up")
    show(c, t, 89.59, 540, 960, lambda c: hl(c, "+ LIMITE nos vazamentos", 0, 0, 48, PINKISH, RED), anim="stamp",
         d=0.3)
    hero(c, t, 880, FY, 0.6, [(0, "present_l"), (85.9, "finger_up"), (89.6, "point_lu")],
         [(0, "neutral"), (85.9, "confident")], look=-1, prop=("r", prop_pointer))
    you(c, t, 180, [(0, "relax"), (85.9, "think"), (88.4, "thumb")], [(0, "think"), (88.4, "happy")], s=0.62, look=1)


def s11(c, t):  # 91.6 - fim  que dia o seu salário acaba? comenta + marca o amigo do dia 12
    floor(c)
    show(c, t, 91.75, 540, 420, M("Que dia o seu", 70, INK), anim="up")
    show(c, t, 92.39, 540, 525, lambda c: hl(c, "salário acaba?", 0, 0, 74, PINKISH), anim="stamp", d=0.3)
    show(c, t, 92.6, 540, 700, sc(calendar, "?", RED, 90, s=1.15), anim="pop")
    show(c, t, 93.35, 540, 850, M("Comenta aí", 66, NAVY), anim="stamp", d=0.3)
    show(c, t, 94.31, 540, 950, T("e marca aquele amigo", 54), anim="up")
    show(c, t, 95.35, 540, 1040, lambda c: hl(c, "do dia 12", 0, 0, 62, LYELLOW), anim="stamp", d=0.3)
    you(c, t, 170, [(0, "point_r"), (93.3, "think")], [(0, "grin"), (93.3, "think")], s=0.62, look=1)
    hero(c, t, 890, FY, 0.6, [(0, "wave")], [(0, "happy")], look=-1)


SCENES = [
    (0.0, 8.2, s01), (8.2, 14.1, s02), (14.1, 20.2, s03), (20.2, 26.8, s04), (26.8, 33.8, s05),
    (33.8, 42.8, s06), (42.8, 49.3, s07), (49.3, 60.3, s08), (60.3, 81.6, s09), (81.6, 91.6, s10),
    (91.6, 999.0, s11),
]
