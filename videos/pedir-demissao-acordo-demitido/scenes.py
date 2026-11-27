"""Pedir demissão (Ana) x acordo (Carla) x demitido sem justa causa (Bruno). Salário R$ 3 mil, 2 anos de casa.
Só TikTok: vertical 1080x1920, ~79,5 s, ESTILO CADERNO. Contas em contas.py (valores antes de INSS/IR).
Quadro 0: três colunas com a caixa da demissão e os três valores já subindo.
Layout: título y~250, palco y 360-1290 (pés em 1280), legendas y~1400-1460, nada abaixo de 1500 nem em x > 930."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
LX, BX = 270, 770
X1, X2, X3 = 180, 520, 860   # Ana, Carla, Bruno
PINKISH = (1, 0.8, 0.76)
PINKD = (0.85, 0.30, 0.52)
ORANGED = (0.85, 0.45, 0.10)

SFX = [(8.3, "tum"), (22.9, "tum"), (70.9, "tum"), (78.6, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, m(s) if font == MARKER else s, 0, 0, size, font, col, align="l")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def MM(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


def brlk(v):
    return "R$ %d mil" % round(v / 1000)


def ana(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", 0.4)
    other(c, t, x, FY, s, poses, exprs, shirt=PINK, fid=4, hair="long", **kw)


def bruno(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", -0.4)
    other(c, t, x, FY, s, poses, exprs, shirt=GREEN, fid=3, hair="tuft", **kw)


def nome(c, x, s, col):
    text(c, s, x, FY + 60, 46, MARKER, col)


def divisoria(c):
    line(c, CX, 340, CX, FY - 20, 4, LGRAY)


def contador(c, t, t0, d, v0, v1, x, y, size, col):
    if t < t0:
        v = v0
    else:
        v = v0 + (v1 - v0) * ease_io(prog(t, t0, d))
    text(c, m(brlk(v)), x, y, size, MARKER, col)



def barras(c, t, t0, va, vb, rot, base=1000, scl=None, k=1000):
    scl = scl or 520 / max(va, vb)
    for tt, x, v, col in ((t0, 330, va, PINK), (t0 + 0.4, 710, vb, GREEN)):
        if t > tt:
            h = v * scl * ease_out(prog(t, tt, 0.6))
            rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
            show(c, t, tt + 0.6, x, base - v * scl - 45, MM(rot(v), 56, INK), anim="pop")
    line(c, 160, base, 860, base, 6)
    text(c, "ANA", 330, base + 50, 44, MARKER, PINKD)
    text(c, "BRUNO", 710, base + 50, 44, MARKER, GREEN)




def carla(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("look", 0)
    other(c, t, x, FY, s, poses, exprs, shirt=ORANGE, fid=5, hair="long", **kw)


def item(c, t, t0, y, s, ok=True, col=NAVY):
    def f(c):
        if ok:
            check_icon(c, 26)
        else:
            c.save(); c.scale(0.55, 0.55); x_icon(c, 46); c.restore()
        text(c, s, 50, 0, 50, MARKER, col if ok else GRAY, align="l")
    show(c, t, t0, 110, y, f, anim="pop")


def tres(c):
    line(c, 350, 340, 350, FY - 20, 4, LGRAY)
    line(c, 690, 340, 690, FY - 20, 4, LGRAY)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 10.6  gancho
    floor(c); tres(c)
    show(c, t, -1.0, CX, 250, lambda c: ribbon(c, "SAÍRAM DA MESMA EMPRESA", NAVY, 50), anim="stamp")
    for x, d, v, col in ((X1, 4.5, 10400, RED), (X2, 6.5, 19000, ORANGED), (X3, 8.5, 34200, GREEN)):
        show(c, t, -1.0, x, 470, sc(moving_box, s=0.6), anim="drop")
        contador(c, t, 0.0, d, 0, v, x, 640, 58, col)
    show(c, t, 9.1, CX, 840, lambda c: hl(c, "O JEITO DE SAIR", 0, 0, 70, PINKISH, RED), anim="stamp")
    ana(c, t, X1, 0.45, [(0, "hold"), (4.5, "head")], [(0, "worried"), (4.5, "worried")], look=0.2)
    carla(c, t, X2, 0.45, [(0, "hold"), (6.5, "stand")], [(0, "worried"), (6.5, "neutral")])
    bruno(c, t, X3, 0.45, [(0, "hold"), (8.5, "arms_up")], [(0, "worried"), (8.5, "grin")], look=-0.2)


def s02(c, t):  # 10.6 - 14.3  quem são
    floor(c); tres(c)
    show(c, t, 10.7, CX, 250, lambda c: ribbon(c, "MESMO SALÁRIO", NAVY, 60), anim="stamp")
    for x in (X1, X2, X3):
        show(c, t, 11.6, x, 470, MM("R$ 3 mil", 54, NAVY), anim="stamp")
        show(c, t, 12.9, x, 600, sc(calendar, "2", NAVY, 46), anim="pop")
        show(c, t, 13.3, x, 710, T("anos de casa", 38, DGRAY), anim="up")
    ana(c, t, X1, 0.5, [(0, "stand")], [(0, "happy")]); nome(c, X1, "ANA", PINKD)
    carla(c, t, X2, 0.5, [(0, "stand")], [(0, "happy")]); nome(c, X2, "CARLA", ORANGED)
    bruno(c, t, X3, 0.5, [(0, "stand")], [(0, "happy")]); nome(c, X3, "BRUNO", GREEN)


def s03(c, t):  # 14.3 - 26.4  Ana pede demissão
    floor(c)
    show(c, t, 14.4, CX, 250, lambda c: ribbon(c, "ANA: PEDIU DEMISSÃO", PINKD, 54), anim="stamp")
    item(c, t, 16.3, 400, "salário do mês")
    item(c, t, 17.4, 480, "férias + 1/3")
    item(c, t, 18.9, 560, "13º")
    show(c, t, 19.8, CX, 680, MM("~R$ 10.400", 84, NAVY), anim="stamp")
    item(c, t, 22.9, 820, "saque do FGTS", ok=False)
    item(c, t, 24.1, 900, "multa", ok=False)
    item(c, t, 25.1, 980, "seguro-desemprego", ok=False)
    ana(c, t, 800, 0.55, [(0, "stand"), (22.9, "head")], [(0, "neutral"), (22.9, "worried")], look=-0.6)


def s04(c, t):  # 26.4 - 40.2  Carla faz acordo
    floor(c)
    show(c, t, 26.5, CX, 250, lambda c: ribbon(c, "CARLA: FEZ ACORDO", ORANGED, 56), anim="stamp")
    item(c, t, 28.8, 400, "metade do aviso")
    item(c, t, 30.4, 480, "férias e 13º inteiros")
    item(c, t, 33.3, 560, "80% do FGTS")
    item(c, t, 35.5, 640, "multa de 20%")
    show(c, t, 37.0, CX, 780, MM("~R$ 19 mil", 90, ORANGED), anim="stamp")
    item(c, t, 38.3, 900, "seguro-desemprego", ok=False)
    carla(c, t, 840, 0.55, [(0, "stand"), (37.0, "thumb")], [(0, "neutral"), (37.0, "happy")], look=-0.6)


def s05(c, t):  # 40.2 - 53.8  Bruno demitido
    floor(c)
    show(c, t, 40.3, CX, 250, lambda c: ribbon(c, "BRUNO: DEMITIDO", GREEN, 58), anim="stamp")
    item(c, t, 42.7, 400, "aviso prévio inteiro")
    item(c, t, 44.0, 480, "FGTS todo")
    item(c, t, 45.3, 560, "multa de 40%")
    show(c, t, 47.3, CX, 700, MM("R$ 23 mil na saída", 76, GREEN), anim="stamp")
    show(c, t, 49.3, CX, 830, T("+ seguro-desemprego:", 50), anim="up")
    show(c, t, 51.4, CX, 930, MM("5x ~R$ 2.160", 70, GREEN), anim="stamp")
    bruno(c, t, 840, 0.55, [(0, "stand"), (47.3, "arms_up")], [(0, "neutral"), (47.3, "grin")], look=-0.6)


def s06(c, t):  # 53.8 - 56.2  tudo somado
    floor(c)
    show(c, t, 53.9, CX, 250, lambda c: ribbon(c, "SOMANDO TUDO", NAVY, 60), anim="stamp")
    base, scl = 1040, 560 / 34200
    for tt, x, v, col, nm, nc in ((54.0, X1, 10400, PINK, "ANA", PINKD), (54.2, X2, 19000, ORANGE, "CARLA", ORANGED),
                                  (54.4, X3, 34200, GREEN, "BRUNO", GREEN)):
        h = v * scl * ease_out(prog(t, tt, 0.6))
        if t > tt:
            rrect(c, x - 90, base - h, 180, h, 12); fs(c, col, 6)
            show(c, t, tt + 0.5, x, base - v * scl - 40, MM("R$ %d mil" % round(v / 1000), 46, INK), anim="pop")
        text(c, nm, x, base + 50, 42, MARKER, nc)
    line(c, 60, base, 960, base, 6)


def s07(c, t):  # 56.2 - 65.1  mas calma: o FGTS da Ana não sumiu
    floor(c)
    show(c, t, 56.3, CX, 250, lambda c: ribbon(c, "MAS CALMA", NAVY, 60), anim="stamp")
    show(c, t, 57.3, CX, 400, T("o FGTS da Ana não sumiu", 56), anim="up")
    show(c, t, 59.3, 300, 560, sc(piggy, GOLD, s=0.8), anim="pop")
    show(c, t, 59.4, 480, 540, L("R$ 6 mil", 76, GREEN, MARKER), anim="stamp", d=0.3)
    show(c, t, 60.1, 480, 620, L("continuam na conta", 44, DGRAY), anim="up")
    show(c, t, 62.7, 300, 840, sc(house, s=1.0), anim="pop")
    show(c, t, 62.7, 480, 820, L("pra comprar casa", 50, NAVY, MARKER), anim="left", d=0.3)
    show(c, t, 63.5, 480, 900, L("ou sacar mais pra frente", 44, DGRAY), anim="up")
    ana(c, t, 830, 0.55, [(0, "stand"), (59.4, "thumb")], [(0, "neutral"), (59.4, "happy")], look=-0.6)


def s08(c, t):  # 65.1 - 71.6  acordo só se a empresa topar; mentira é fraude
    floor(c)
    show(c, t, 65.2, CX, 250, lambda c: ribbon(c, "E O ACORDO...", ORANGED, 60), anim="stamp")
    show(c, t, 65.9, CX, 420, T("só existe se a empresa topar", 54), anim="up")
    show(c, t, 67.9, CX, 580, T("demissão de mentira pra sacar FGTS", 46, DGRAY), anim="up")
    show(c, t, 70.6, CX, 720, lambda c: hl(c, "É FRAUDE", 0, 0, 100, PINKISH, RED), anim="stamp")
    hero(c, t, CX, FY, 0.5, [(0, "present"), (70.6, "finger_up")], [(0, "neutral"), (70.6, "confident")], look=0)


def s09(c, t):  # 71.6 - fim  faz essa conta / comenta
    floor(c)
    show(c, t, 71.7, CX, 300, M("ANTES DE PEDIR AS CONTAS", 60, NAVY), anim="stamp")
    show(c, t, 73.8, CX, 420, lambda c: hl(c, "FAZ ESSA CONTA", 0, 0, 74, LYELLOW), anim="stamp")
    for tt, x, s, col in ((75.6, X1, "pedir?", PINKD), (76.7, X2, "acordo?", ORANGED), (77.6, X3, "esperar?", GREEN)):
        show(c, t, tt, x, 600, MM(s, 52, col), anim="pop")
    show(c, t, 78.6, CX, 760, lambda c: hl(c, "COMENTA AÍ", 0, 0, 70, LYELLOW), anim="stamp")
    ana(c, t, X1, 0.45, [(0, "think")], [(0, "think")]); carla(c, t, X2, 0.45, [(0, "think")], [(0, "think")])
    bruno(c, t, X3, 0.45, [(0, "think")], [(0, "think")], look=-0.2)


SCENES = [
    (0.0, 10.6, s01), (10.6, 14.3, s02), (14.3, 26.4, s03), (26.4, 40.2, s04), (40.2, 53.8, s05),
    (53.8, 56.2, s06), (56.2, 65.1, s07), (65.1, 71.6, s08), (71.6, 999.0, s09),
]
