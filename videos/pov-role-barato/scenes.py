"""POV: é sábado e você saiu pra 'só um rolê barato'. Só TikTok: vertical nativo 1080x1920, ~80 s.
Formato POV (modelo: videos/pov-salario-dia-12): o bonequinho principal é VOCÊ (camiseta laranja);
O Consultor só entra na virada (51,0 s). Faixa POV fixa no topo, relógio no canto (19h -> 3h) e o contador
"gasto da noite" subindo a cada cena (0 a 51,0 s).
Layout: faixa POV y 170-320, HUD (relógio + gasto) y 380-580, palco y 600-1280 (chão FY=1280),
legendas do tiktok.py em y~1460; nada importante em x > 930.
Contas: ida 30 | rodada 60 -> 90 | porção 90 -> 180 | rodada da galera 120 -> 300 | lanche 50 -> 350 |
volta com dinâmica 80 -> 430. 4 sábados = 1.720/mês; x 12 = 20.640/ano."""
import math

from engine import *  # noqa

VERTICAL = True

FY = 1280
YX = 260          # x de VOCÊ em pé
YS = 0.8
POV_END = 51.0
PINKISH = (1, 0.8, 0.76)
NIGHT = (0.20, 0.22, 0.36)

SFX = [(0.3, "soft_ding"), (49.27, "tum"), (63.44, "tum"), (77.28, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow",
            "appear", "key", "transition")

# (tempo em que o valor é falado, total da noite depois)
GASTO = [(6.87, 30), (12.12, 90), (19.84, 180), (27.92, 300), (35.09, 350), (41.8, 430)]
HORAS = [(0.0, "18:50"), (3.84, "19:00"), (8.16, "20:00"), (15.2, "22:00"), (22.72, "23:00"), (30.72, "01:00"),
         (37.68, "02:00"), (42.96, "03:00")]
TOTAL = 430


# ---------------------------------------------------------------- helpers
def brl(v, sign=False):
    s = f"{abs(int(v)):,}".replace(",", ".").replace("2.", "2 .")
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
    text(c, "POV: é sábado e você saiu", 540, 222, 52, MARKER, WHITE)
    text(c, "pra \"só um rolê barato\"", 540, 282, 52, MARKER, GOLD)
    c.pop_group_to_source(); c.paint_with_alpha(a)


def gasto_at(t):
    """valor exibido (rola do anterior ao novo em 0,5 s) e tempo do último aumento"""
    prev, last, val = 0, None, 0
    for tt, v in GASTO:
        if t < tt:
            break
        k = ease_out(prog(t, tt, 0.5))
        val = prev + (v - prev) * k
        prev, last = v, tt
    return val, last


def hud(c, t):
    """relógio digital (esquerda) + contador 'gasto da noite' (direita), só na parte POV"""
    a = pov_alpha(t)
    if a <= 0:
        return
    c.push_group()
    hora, t_h = HORAS[0][1], 0.0
    for tt, h in HORAS:
        if t >= tt:
            hora, t_h = h, tt
    k = 1 + 0.2 * (1 - ease_out(prog(t, t_h, 0.35))) if t_h > 0 else 1
    late = t >= 30.72
    c.save(); c.translate(175, 480); c.scale(k, k)
    rrect(c, -125, -95, 250, 190, 26); fs(c, NIGHT if t >= 15.2 else DGRAY, 6)
    text(c, hora, 0, 18, 76, MARKER, GOLD if late else WHITE)
    text(c, "sábado" if t < 30.72 else "domingo", 0, -58, 30, HAND, LGRAY)
    c.restore()
    if t >= 15.2:
        c.save(); c.translate(282, 400); c.scale(0.55, 0.55); moon(c); c.restore()
    # contador
    val, last = gasto_at(t)
    over = val > 50
    flash = last is not None and t - last < 0.9
    col = RED if (over or flash) else GREEN
    rrect(c, 330, 385, 590, 195, 26); fs(c, WHITE, 6)
    text(c, "gasto da noite", 625, 422, 40, HAND, DGRAY)
    shake = math.sin(t * 60) * 8 * (1 - prog(t, last, 0.4)) if (last and t - last < 0.4) else 0
    text(c, brl(round(val / 10) * 10 if val > 60 else round(val)), 625 + shake, 505, 108, MARKER, col)
    text(c, "plano: R$ 50", 625, 558, 30, HAND, GREEN if not over else RED)
    c.pop_group_to_source(); c.paint_with_alpha(a)


def base(c, t):
    floor(c)
    pov_banner(c, t)
    hud(c, t)


def you(c, t, x, poses, exprs, s=YS, y=FY, **kw):
    """VOCÊ: pessoa comum (camiseta laranja, cabelo espetado)"""
    kw.setdefault("shirt", ORANGE); kw.setdefault("hair", "spiky"); kw.setdefault("fid", 2)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def bubble(c, t, t0, x, y, s, w=380, h=110, tx=-60, ty=150, size=48, col=INK, t1=None):
    show(c, t, t0, x, y, group(lambda c: speech(c, w, h, tx, ty), T(s, size, col)), anim="pop", d=0.3, t1=t1)


def plus(val):
    return lambda c: hl(c, brl(val, sign=True), 0, 0, 84, PINKISH, RED)


def item(c, t, label, t_lab, icon, val, t_val, t1=None, ix=660, iy=900, sy=1110):
    """rótulo do gasto, ícone e o valor carimbado quando a narração chega nele"""
    show(c, t, t_lab, 640, 680, M(label, 60 if len(label) < 16 else 50, INK), anim="up", t1=t1)
    if icon:
        show(c, t, t_lab + 0.1, ix, iy, icon, anim="pop", t1=t1)
    show(c, t, t_val, 660, sy, plus(val), anim="stamp", d=0.35, t1=t1)


def ride(c, t, t0, col=DGRAY):
    """carro de aplicativo chegando pela direita"""
    k = ease_out(prog(t, t0, 0.7))
    if t < t0:
        return
    c.save(); c.translate(1200 - 550 * k, 935); c.scale(0.95, 0.95); car(c, col); c.restore()
    if k < 1:
        for i in range(3):
            line(c, 1200 - 550 * k + 170, 900 + i * 22, 1200 - 550 * k + 240 + 30 * i, 900 + i * 22, 5, LGRAY)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 3.8  "hoje é só uma saidinha, coisa de cinquenta reais"
    base(c, t)
    bubble(c, t, 0.0, 400, 700, "hoje é só uma saidinha", w=560, h=110, tx=-120, ty=150, size=46)
    show(c, t, 0.2, 680, 950, lambda c: text(c, "R$ 50", 0, 0, 170, MARKER, GREEN, outline=WHITE, ow=16),
         anim="stamp", d=0.3)
    show(c, t, 2.32, 680, 1090, T("coisa de cinquenta", 48, DGRAY), anim="up")
    you(c, t, YX, [(0, "thumb")], [(0, "grin")], look=0.6)


def s02(c, t):  # 3.8 - 8.1  19h: a corrida pra ir, 30
    base(c, t)
    show(c, t, 5.2, 640, 680, M("Corrida pra ir", 60, INK), anim="up")
    ride(c, t, 4.2)
    show(c, t, 6.87, 660, 1110, plus(30), anim="stamp", d=0.35)
    you(c, t, YX, [(0, "hold"), (6.9, "thumb")], [(0, "happy"), (6.9, "grin")], look=0.6)
    show(c, t, 0, YX + 10, 1080, sc(phone, s=0.35), anim="fade", t1=6.8) if t < 6.9 else None


def s03(c, t):  # 8.1 - 15.1  20h: a primeira rodada, "só uma", 60 (total 90)
    base(c, t)
    item(c, t, "A primeira rodada", 9.36, sc(beer_mug, s=1.3), 60, 12.12)
    bubble(c, t, 10.32, 330, 770, "só uma!", w=280, size=52)
    you(c, t, YX, [(0, "relax"), (10.3, "finger_up"), (12.2, "thumb")], [(0, "happy"), (10.3, "grin")], look=0.6)


def s04(c, t):  # 15.1 - 22.6  22h: a porção pra dividir que ninguém dividiu, 90 (total 180)
    base(c, t)
    item(c, t, "Porção pra dividir", 16.4, sc(fries_basket, s=1.25), 90, 19.84)
    show(c, t, 18.0, 700, 770, lambda c: hl(c, "ninguém dividiu", 0, 0, 46, LYELLOW), anim="stamp", d=0.3,
         rot=0.06)
    you(c, t, YX, [(0, "relax"), (18.0, "shrug"), (19.9, "head")],
        [(0, "happy"), (18.0, "worried"), (19.9, "shocked")], look=0.6)


def s05(c, t):  # 22.6 - 30.6  23h: chegou mais gente, mais uma rodada, 120 (total 300)
    base(c, t)
    show(c, t, 23.84, 640, 680, M("Chegou mais gente", 56, INK), anim="up")
    other(c, t, 600, FY, 0.66, [(0, "wave"), (26.4, "arms_up")], [(0, "happy"), (26.4, "grin")], appear=23.9, look=-1)
    other(c, t, 790, FY, 0.66, [(0, "wave"), (26.4, "arms_up")], [(0, "grin")], appear=24.2, look=-1,
          shirt=GREEN, hair="tuft")
    for i, x in enumerate((540, 690, 840)):
        show(c, t, 26.6 + i * 0.15, x, 775, sc(beer_mug, s=0.55), anim="pop", d=0.25)
    bubble(c, t, 25.0, 720, 1210 - 0, "mais uma!", w=280, h=90, tx=-40, ty=-90, size=44, t1=27.8)
    show(c, t, 27.92, 690, 915, plus(120), anim="stamp", d=0.35)
    you(c, t, YX, [(0, "relax"), (23.9, "thumb"), (28.0, "head")], [(0, "happy"), (23.9, "grin"), (28.0, "shocked")],
        look=0.6)


def s06(c, t):  # 30.6 - 37.6  1h: bateu a fome, lanche de madrugada, 50 (total 350)
    base(c, t)
    show(c, t, 33.2, 640, 680, M("Lanche de madrugada", 52, INK), anim="up")
    show(c, t, 31.76, 500, 770, T("bateu a fome", 44, DGRAY), anim="up", t1=33.1)
    show(c, t, 33.3, 660, 910, sc(sandwich, s=1.05), anim="pop")
    show(c, t, 35.09, 660, 1110, plus(50), anim="stamp", d=0.35)
    you(c, t, YX, [(0, "hold"), (33.3, "arms_up"), (35.2, "hips")],
        [(0, "worried"), (33.3, "grin"), (35.2, "neutral")], look=0.6)


def s07(c, t):  # 37.6 - 42.9  2h: a corrida de volta com tarifa dinâmica, 80 (total 430)
    base(c, t)
    show(c, t, 38.8, 640, 680, M("Corrida de volta", 58, INK), anim="up")
    ride(c, t, 38.8, RED)
    show(c, t, 40.48, 760, 790, lambda c: hl(c, "tarifa dinâmica", 0, 0, 46, PINKISH, RED), anim="stamp", d=0.3,
         rot=0.07)
    show(c, t, 40.6, 560, 800, lambda c: arrow(c, 0, 40, 0, -50, RED, 10), anim="pop", d=0.25)
    show(c, t, 41.8, 660, 1110, plus(80), anim="stamp", d=0.35)
    you(c, t, YX, [(0, "relax"), (40.5, "head")], [(0, "neutral"), (40.5, "shocked"), (41.9, "desperate")], look=0.6)


def bank_screen(c):
    rrect(c, -190, -300, 380, 600, 40); fs(c, INK, 0)
    rrect(c, -170, -270, 340, 540, 26); fs(c, WHITE, 0)
    text(c, "app do banco", 0, -225, 34, HAND, DGRAY)
    for i, (lab, v) in enumerate((("corrida", 30), ("bar", 60), ("bar", 90), ("bar", 120), ("lanche", 50),
                                  ("corrida", 80))):
        y = -160 + i * 50
        text(c, lab, -140, y, 30, HAND, INK, align="l")
        text(c, f"-{v}", 140, y, 32, MARKER, RED, align="r")
    line(c, -140, 150, 140, 150, 4, LGRAY)
    text(c, "total da noite", 0, 190, 30, HAND, DGRAY)
    text(c, "-430", 0, 240, 56, MARKER, RED)


def s08(c, t):  # 42.9 - 51.0  3h: na cama, app do banco, o rolê de 50 custou 430
    base(c, t)
    rise = 49.27
    if t < rise:
        c.save(); c.translate(330, FY); bed(c, w=520); c.restore()
        # VOCÊ deitado na cama (cabeça à esquerda), segurando o celular
        c.save(); c.translate(430, FY - 118); c.rotate(-1.52)
        you(c, t, 0, [(0, "relax"), (45.0, "hold")], [(0, "neutral"), (45.4, "worried")], s=0.72, y=0, look=0)
        c.restore()
        c.save(); c.translate(400, FY); blanket(c, BLUE, 330); c.restore()
    else:
        c.save(); c.translate(330, FY); c.push_group(); bed(c, w=520); c.pop_group_to_source(); c.paint_with_alpha(0.35)
        c.restore()
        you(c, t, 230, [(0, "head")], [(0, "shocked"), (50.0, "desperate")], s=0.72, look=0.6)
    show(c, t, 45.44, 760, 880, bank_screen, s=0.85, anim="pop", d=0.4, t1=rise)
    show(c, t, 46.64, 360, 700, group(M("rolê de R$ 50", 50, GREEN)), anim="up")
    # o total grande em vermelho
    show(c, t, rise, 600, 880, lambda c: text(c, "R$ 430", 0, 0, 185, MARKER, RED, outline=WHITE, ow=18),
         anim="stamp", d=0.35)
    show(c, t, 49.27, 360, 700, lambda c: line(c, -175, 4, 175, -4, 6, RED), anim="left", d=0.3)
    show(c, t, 49.8, 640, 1050, M("custou isso", 60, RED), anim="up")


# ---------------------------------------------------------------- virada: O Consultor
def s09(c, t):  # 51.0 - 65.6  sem bronca; 4 sábados = 1.720/mês (quase um aluguel); 20.640/ano
    floor(c)
    pov_banner(c, t)
    hud(c, t)
    t_conta = 56.6
    show(c, t, 53.44, 470, 520, lambda c: hl(c, "Não é pra parar de sair.", 0, 0, 52, LGREEN, INK), anim="stamp",
         d=0.3, t1=t_conta)
    show(c, t, 54.76, 470, 650, lambda c: hl(c, "É pra saber quanto custa.", 0, 0, 52, LYELLOW, INK), anim="stamp",
         d=0.3, t1=t_conta)
    # a conta
    show(c, t, 56.76, 460, 420, M("R$ 430  x  4 sábados", 58, INK), anim="up")
    show(c, t, 58.96, 460, 560, lambda c: text(c, "R$ 1.720", 0, 0, 130, MARKER, RED, outline=WHITE, ow=14),
         anim="stamp", d=0.35)
    show(c, t, 59.6, 460, 660, T("por mês", 48, RED), anim="up")
    show(c, t, 61.24, 460, 760, group(at(-150, 0, sc(house, s=0.5)), at(60, 0, T("quase um aluguel", 46, DGRAY))),
         anim="pop")
    show(c, t, 62.56, 460, 880, M("x 12 meses", 56, INK), anim="up")
    show(c, t, 63.44, 490, 990, lambda c: text(c, "R$ 20.640", 0, 0, 100, MARKER, RED, outline=WHITE, ow=14),
         anim="stamp", d=0.35)
    show(c, t, 64.2, 460, 1095, T("por ano", 48, RED), anim="up")
    hero(c, t, 830, FY, 0.62, [(0, "wave"), (52.5, "hips"), (53.44, "present_l"), (56.76, "point_lu"),
                               (61.24, "think"), (63.44, "finger_up")],
         [(0, "happy"), (53.44, "confident"), (56.76, "neutral"), (63.44, "confident")],
         appear=51.04, look=-1, prop=("r", prop_calculator) if t > 56.7 else None)
    you(c, t, 150, [(0, "head"), (53.44, "relax"), (63.5, "head")],
        [(0, "desperate"), (53.44, "happy"), (56.76, "neutral"), (63.5, "shocked")], s=0.55, look=1)


def s10(c, t):  # 65.6 - 72.3  a dica: antes de sair, defina quanto vai gastar e leve como limite
    floor(c)
    show(c, t, 65.72, 540, 400, lambda c: ribbon(c, "A DICA", NAVY, 60), anim="stamp")
    show(c, t, 67.76, 540, 540, M("Antes de sair,", 66, INK), anim="up")
    show(c, t, 68.76, 540, 660, lambda c: hl(c, "defina quanto vai gastar", 0, 0, 56, LYELLOW), anim="stamp",
         d=0.3)
    def limite(c):
        c.save(); c.scale(1.1, 1.1); envelope(c); c.restore()
        text(c, "LIMITE", 0, 36, 40, MARKER, NAVY)
    show(c, t, 70.64, 470, 870, limite, anim="pop")
    show(c, t, 71.0, 470, 1010, T("e leve só isso", 46, DGRAY), anim="up")
    hero(c, t, 830, FY, 0.62, [(0, "present_l"), (68.76, "finger_up"), (70.64, "point_lu")],
         [(0, "neutral"), (68.76, "confident")], look=-1, prop=("r", prop_pointer))
    you(c, t, 150, [(0, "relax"), (68.8, "think"), (71.1, "thumb")], [(0, "think"), (71.1, "happy")], s=0.55, look=1)


def s11(c, t):  # 72.3 - fim  quanto foi o seu? comenta, marca o amigo da rodada, segue pra mais POV
    floor(c)
    show(c, t, 72.44, 470, 400, M("Quanto foi o seu", 64, INK), anim="up")
    show(c, t, 73.6, 470, 500, lambda c: hl(c, "último rolê \"barato\"?", 0, 0, 60, PINKISH), anim="stamp", d=0.3)
    show(c, t, 74.64, 470, 640, M("Comenta", 66, NAVY), anim="stamp", d=0.3)
    show(c, t, 75.52, 400, 750, T("e marca o amigo da rodada", 50), anim="up")
    show(c, t, 75.9, 780, 760, sc(beer_mug, s=0.55), anim="pop", d=0.25)
    # SEGUE PRA MAIS
    show(c, t, 77.28, 470, 950, lambda c: ribbon(c, "SEGUE PRA MAIS", GOLD, 58, INK), anim="stamp", d=0.35)
    if t >= 77.4:
        bob = 14 * math.sin((t - 77.4) * 8)
        show(c, t, 77.4, 640, 1090 - bob, lambda c: arrow(c, 0, 50, 0, -60, GOLD, 12), anim="pop", d=0.25)
    hero(c, t, 830, FY, 0.62, [(0, "wave"), (74.64, "present_l"), (77.28, "finger_up")],
         [(0, "happy"), (77.28, "confident")], look=-1)
    you(c, t, 150, [(0, "think"), (74.64, "point_r")], [(0, "think"), (74.64, "grin")], s=0.55, look=1)


SCENES = [
    (0.0, 3.8, s01), (3.8, 8.1, s02), (8.1, 15.1, s03), (15.1, 22.6, s04), (22.6, 30.6, s05),
    (30.6, 37.6, s06), (37.6, 42.9, s07), (42.9, 51.0, s08), (51.0, 65.6, s09), (65.6, 72.3, s10),
    (72.3, 999.0, s11),
]
