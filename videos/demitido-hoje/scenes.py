"""Se você fosse demitido hoje, quanto receberia? Só TikTok: vertical nativo 1080x1920, ~80,3 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco de 89,97 s acelerado 1,12x (atempo) -> 80,3 s.
Os tempos daqui e do palavras.json já estão na velocidade final.
Contas e premissas em contas.py (conferidas em 05/11/2026)."""
from engine import *  # noqa

VERTICAL = True

CX = 520          # centro útil (à esquerda por causa dos botões do TikTok)
FY = 1230         # pés dos bonecos (no quadro final ficam em 1290: SHIFT)
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
TS = ""
import engine as _eng
_text0, _tw0 = _eng.text, _eng.text_w
GAP = 0.13        # na Permanent Marker o ponto some embaixo do "2": abre um vão de 13% do tamanho


def _split(s):
    return s.split("2.", 1) if "2." in s else None


def _tw(c, s, size, font=MARKER):
    sp = _split(s) if font == MARKER else None
    if not sp:
        return _tw0(c, s, size, font)
    return _tw0(c, sp[0] + "2", size, font) + size * GAP + _tw(c, "." + sp[1], size, font)


def _text(c, s, x=0, y=0, size=60, font=MARKER, col=INK, align="c", **kw):
    sp = _split(s) if font == MARKER else None
    if not sp:
        return _text0(c, s, x, y, size, font, col, align, **kw)
    w = _tw(c, s, size, font)
    x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    a = _text0(c, sp[0] + "2", x0, y, size, font, col, "l", **kw)
    _text(c, "." + sp[1], x0 + a + size * GAP, y, size, font, col, "l", **kw)
    return w


_eng.text, _eng.text_w = _text, _tw
text, text_w = _text, _tw

SFX = [(16.9, "tum"), (35.8, "soft_ding"), (53.4, "tum"), (65.0, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def brl(v):
    s = f"{int(round(v)):,}".replace(",", ".")
    return "R$ " + s


# ---------------------------------------------------------------- helpers
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def R(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="r")


def worker(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 2)
    other(c, t, x, FY, s, poses, exprs, **kw)


def counter(c, t, val_keys, y=330, label="RESCISÃO"):
    """placar fixo no topo: soma da rescisão contando para cima quando um item entra"""
    v, prev, t_last = 0, 0, -1
    for tk, vk in val_keys:
        if t >= tk:
            prev, v, t_last = v, vk, tk
    k = ease_out(prog(t, t_last, 0.6)) if t_last >= 0 else 1
    cur = prev + (v - prev) * k
    rrect(c, 90, y - 55, 860, 110, 22); fs(c, NAVY, 6)
    text(c, label, 130, y, 50, MARKER, WHITE, align="l")
    text(c, brl(cur), 910, y, 68, MARKER, GOLD, align="r")


ITEMS = [(14.4, 1500), (18.4, 5100), (25.5, 10100), (30.8, 13100)]


def eq_line(parts, size=62):
    """linha de conta: lista de (texto, cor)"""
    def f(c):
        ws = [text_w(c, s, size) for s, _ in parts]
        x = -sum(ws) / 2
        for (s, col), w in zip(parts, ws):
            text(c, s, x, 0, size, MARKER, col, align="l")
            x += w
    return f


def beach(c):
    beach_chair(c)


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def safe_box(c, label="FGTS", col=GREEN):
    rrect(c, -150, -130, 300, 260, 24); fs(c, LGRAY, 7)
    rrect(c, -120, -100, 240, 200, 16); fs(c, WHITE, 5)
    circle(c, 60, 0, 34, GRAY, 6)
    line(c, 60, 0, 80, -18, 6)
    text(c, label, -40, 0, 54, MARKER, col)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.8  gancho
    floor(c)
    show(c, t, 0.0, CX, 260, lambda c: hl(c, "DEMITIDO HOJE?", 0, 0, 96, PINKISH), anim="stamp", d=0.35)
    show(c, t, 1.8, CX, 380, T("sem justa causa", 60, RED), anim="up")
    show(c, t, 2.9, CX + 170, 620, group(lambda c: speech(c, 470, 170, -150, 120), M("R$ ???", 96, GREEN)), anim="pop")
    show(c, t, 4.6, CX + 170, 860, lambda c: hl(c, "a maioria não sabe", 0, 0, 56, LYELLOW), anim="stamp")
    worker(c, t, 220, 0.85, [(0, "think"), (4.6, "shrug")], [(0, "think"), (4.6, "worried")], appear=0.0, look=0.5)
    hero(c, t, 880, FY, 0.55, [(0, "relax"), (4.7, "finger_up")], [(0, "neutral"), (4.7, "confident")], appear=1.0, look=-1)


def s02(c, t):  # 6.8 - 14.1  o exemplo
    floor(c)
    show(c, t, 6.9, CX, 250, M("Vamos fazer a conta", 76, NAVY), anim="up")
    show(c, t, 8.0, 640, 430, group(lambda c: rrect(c, -270, -60, 540, 120, 20), lambda c: fs(c, WHITE, 6),
                                    M("salário R$ 3.000", 62, GREEN)), anim="left")
    show(c, t, 9.8, 640, 580, group(lambda c: rrect(c, -270, -60, 540, 120, 20), lambda c: fs(c, WHITE, 6),
                                    M("2 anos de empresa", 58)), anim="left")
    show(c, t, 11.1, 640, 790, group(sc(calendar, "15", RED, 72, s=1.0), at(0, 135, T("meio de novembro", 48))), anim="pop")
    show(c, t, 12.7, 600, 1010, lambda c: ribbon(c, "EXEMPLO SIMPLIFICADO", NAVY, 40), anim="stamp")
    worker(c, t, 170, 0.75, [(0, "wave"), (11.2, "head")], [(0, "happy"), (11.2, "shocked")], appear=7.0, look=0.4)


def s03(c, t):  # 14.1 - 18.1  saldo de salário
    floor(c)
    counter(c, t, ITEMS)
    show(c, t, 14.2, CX, 480, M("1. Saldo de salário", 72, NAVY), anim="up")
    show(c, t, 15.3, 330, 720, group(sc(calendar, "15", RED, 72, s=1.1), at(0, 145, T("dias trabalhados", 46))), anim="pop")
    show(c, t, 16.8, 720, 720, lambda c: hl(c, "R$ 1.500", 0, 0, 100, LGREEN), anim="stamp")
    hero(c, t, 760, FY, 0.6, [(0, "present_l"), (16.8, "thumb")], [(0, "neutral"), (16.8, "happy")], look=-0.6)


def s04(c, t):  # 18.1 - 25.2  aviso prévio
    floor(c)
    counter(c, t, ITEMS)
    show(c, t, 18.1, CX, 480, M("2. Aviso prévio", 76, NAVY), anim="up")
    show(c, t, 18.9, CX, 565, T("indenizado (você não trabalha)", 46, DGRAY), anim="up")
    show(c, t, 19.8, CX, 690, eq_line([("30 dias", INK), (" + 3 por ano", BLUE)], 62), anim="up")
    show(c, t, 22.3, CX, 810, eq_line([("30 + 3 + 3 = ", INK), ("36 dias", RED)], 66), anim="pop")
    show(c, t, 23.6, CX, 960, lambda c: hl(c, "R$ 3.600", 0, 0, 100, LGREEN), anim="stamp")
    hero(c, t, 900, FY, 0.5, [(0, "relax"), (19.8, "finger_up"), (23.6, "thumb")],
         [(0, "neutral"), (19.8, "think"), (23.6, "grin")], look=-1)


def s05(c, t):  # 25.2 - 30.5  férias
    floor(c)
    counter(c, t, ITEMS)
    show(c, t, 25.2, CX, 480, M("3. Férias + 1/3", 76, NAVY), anim="up")
    show(c, t, 25.9, 220, 720, sc(beach, s=0.65), anim="pop")
    show(c, t, 26.2, 470, 640, L("1 período vencido", 50), anim="left")
    show(c, t, 27.2, 470, 730, L("+ 3 meses proporcionais", 50), anim="left")
    show(c, t, 28.7, 470, 820, L("+ 1/3 em tudo", 50, BLUE), anim="left")
    show(c, t, 29.6, CX + 120, 980, lambda c: hl(c, "R$ 5.000", 0, 0, 100, LGREEN), anim="stamp")
    hero(c, t, 170, FY, 0.5, [(0, "relax"), (29.7, "arms_up")], [(0, "neutral"), (29.7, "grin")], look=1)


def s06(c, t):  # 30.5 - 35.7  13º
    floor(c)
    counter(c, t, ITEMS)
    show(c, t, 30.5, CX, 480, M("4. Décimo terceiro", 76, NAVY), anim="up")
    show(c, t, 31.6, 320, 720, group(sc(calendar, "DEZ", NAVY, 56, s=1.1), at(0, 145, T("contrato vai até", 46))), anim="pop")
    show(c, t, 32.4, 330, 600, T("com o aviso,", 46, DGRAY), anim="up")
    show(c, t, 33.8, 720, 650, sc(gift, s=1.0), anim="drop")
    show(c, t, 34.2, 720, 860, lambda c: hl(c, "R$ 3.000", 0, 0, 96, LGREEN), anim="stamp")
    show(c, t, 34.3, 720, 960, T("inteiro!", 54, GREEN), anim="up")
    hero(c, t, 920, FY, 0.48, [(0, "think"), (34.2, "arms_up")], [(0, "think"), (34.2, "grin")], look=-1)


def s07(c, t):  # 35.7 - 40.2  rescisão: 13.100, prazo de 10 dias
    floor(c)
    show(c, t, 35.7, CX, 270, M("RESCISÃO", 80, NAVY), anim="up")
    rows = [("saldo de salário", 1500), ("aviso prévio", 3600), ("férias + 1/3", 5000), ("13º", 3000)]
    for i, (lab, v) in enumerate(rows):
        show(c, t, 35.8 + i * 0.12, CX, 400 + i * 78, group(at(-330, 0, L(lab, 50)), at(330, 0, R(brl(v), 52, INK, MARKER))),
             anim="left", d=0.3)
    if t > 36.4:
        line(c, CX - 340, 715, CX + 340, 715, 6, INK)
    show(c, t, 36.0, CX, 800, lambda c: hl(c, "R$ 13.100", 0, 0, 110, LGREEN), anim="stamp")
    show(c, t, 38.1, 330, 1010, group(sc(calendar, "10", RED, 72, s=0.85), at(0, 120, T("dias", 44))), anim="pop")
    show(c, t, 38.4, 450, 1000, L("pra empresa pagar", 52), anim="left")
    hero(c, t, 930, FY, 0.42, [(0, "present_l"), (38.2, "finger_up")], [(0, "happy"), (38.2, "confident")], look=-1)


def s08(c, t):  # 40.2 - 47.8  FGTS: 8% x 24 meses
    floor(c)
    show(c, t, 40.2, CX, 260, M("E o FGTS, à parte", 76, GREEN), anim="up")
    show(c, t, 41.0, 270, 560, sc(safe_box, s=1.0), anim="pop")
    show(c, t, 42.8, 690, 470, M("8% de R$ 3.000", 52), anim="left")
    show(c, t, 44.0, 690, 560, M("= R$ 240/mês", 58, GREEN), anim="left")
    show(c, t, 45.0, 690, 670, M("x 24 meses", 58, BLUE), anim="left")
    show(c, t, 46.0, CX, 860, lambda c: hl(c, "R$ 5.760", 0, 0, 110, LGREEN), anim="stamp")
    show(c, t, 46.6, CX, 980, T("sem contar rendimento", 44, DGRAY), anim="up")
    hero(c, t, 170, FY, 0.5, [(0, "present"), (46.0, "thumb")], [(0, "neutral"), (46.0, "happy")],
         prop=("l", prop_calculator), look=1)


def s09(c, t):  # 47.8 - 52.6  multa de 40%
    floor(c)
    show(c, t, 47.9, CX, 260, M("+ multa de 40%", 84, RED), anim="stamp")
    show(c, t, 48.6, CX, 380, T("paga pela empresa", 56), anim="up")
    show(c, t, 48.8, 280, 640, group(sc(bank, s=1.0), at(0, 150, T("empresa", 46))), anim="pop")
    if t > 49.4:
        arrow_draw(c, t, 49.4, 420, 620, 640, 620, d=0.4, col=GREEN)
    show(c, t, 49.6, 780, 620, sc(safe_box, s=0.7), anim="pop")
    show(c, t, 50.2, CX, 860, M("40% de R$ 5.760", 58), anim="up")
    show(c, t, 50.9, CX - 60, 990, lambda c: hl(c, "+ R$ 2.304", 0, 0, 100, LGREEN), anim="stamp")
    hero(c, t, 900, FY, 0.48, [(0, "relax"), (50.9, "arms_up")], [(0, "neutral"), (50.9, "grin")], look=-1)


def s10(c, t):  # 52.6 - 62.7  total + descontos
    floor(c)
    show(c, t, 52.6, CX, 260, M("TOTAL", 90, NAVY), anim="up", t1=55.7)
    rows = [("rescisão", 13100, INK), ("FGTS", 5760, GREEN), ("multa 40%", 2304, GREEN)]
    for i, (lab, v, col) in enumerate(rows):
        show(c, t, 52.7 + i * 0.12, CX, 380 + i * 74, group(at(-300, 0, L(lab, 50)), at(300, 0, R(brl(v), 52, col, MARKER))),
             anim="left", d=0.3, t1=55.7)
    show(c, t, 53.3, CX, 650, lambda c: hl(c, "R$ 21.164", 0, 0, 140, LGREEN), anim="stamp")
    # descontos
    show(c, t, 55.8, CX, 300, M("Descontos?", 80, RED), anim="up")
    show(c, t, 56.8, 360, 860, group(lambda c: rrect(c, -230, -110, 460, 220, 20), lambda c: fs(c, PINKISH, 6),
                                     M("INSS e IR", 54, RED), at(0, 60, T("(conforme o salário)", 40))), anim="pop")
    show(c, t, 60.5, 360, 1010, T("só no saldo e no 13º", 46, INK), anim="up")
    show(c, t, 61.3, 760, 860, group(sc(check_icon, 50), at(0, 95, T("aviso e férias:", 42)),
                                     at(0, 140, T("sem desconto", 42, GREEN))), anim="pop")
    hero(c, t, 900, FY, 0.42, [(0, "arms_up"), (55.8, "finger_up"), (60.5, "present_l")],
         [(0, "grin"), (55.8, "think"), (60.5, "confident")], look=-1)


def parcels(c, t, t0):
    for i in range(5):
        x = -340 + i * 170
        if t < t0 + i * 0.18:
            continue
        c.save(); c.translate(x, 0); c.scale(0.85, 0.85); envelope(c); c.restore()
        text(c, f"{i + 1}ª", x, 105, 46, MARKER, INK)


def s11(c, t):  # 62.7 - 70.2  seguro-desemprego
    floor(c)
    show(c, t, 62.7, CX, 260, M("+ Seguro-desemprego", 72, BLUE), anim="up")
    show(c, t, 64.4, CX, 380, T("1º pedido, 2 anos de trabalho", 50, DGRAY), anim="up")
    show(c, t, 66.7, CX, 580, lambda c: parcels(c, t, 66.7), anim="fade", d=0.1)
    show(c, t, 67.7, CX, 820, lambda c: hl(c, "5x R$ 2.166", 0, 0, 100, LGREEN), anim="stamp")
    show(c, t, 68.6, CX, 950, T("quase R$ 11 mil no total", 50), anim="up")
    hero(c, t, 880, FY, 0.48, [(0, "present_l"), (67.7, "thumb")], [(0, "neutral"), (67.7, "happy")], look=-1)


def s12(c, t):  # 70.2 - 76.3  alerta saque-aniversário
    floor(c)
    show(c, t, 70.2, CX, 260, lambda c: hl(c, "ATENÇÃO", 0, 0, 90, PINKISH, RED), anim="stamp")
    show(c, t, 71.0, CX, 380, T("optou pelo saque-aniversário?", 58), anim="up")
    show(c, t, 72.6, 280, 650, group(sc(safe_box, s=0.85), at(0, 160, M("R$ 5.760", 52))), anim="pop")
    show(c, t, 73.9, 280, 640, sc(padlock, RED, s=0.7), anim="drop")
    show(c, t, 74.3, 280, 910, M("BLOQUEADO", 54, RED), anim="stamp")
    show(c, t, 75.3, 740, 650, group(at(0, -10, M("multa", 56)), at(0, 80, M("R$ 2.304", 56, GREEN))), anim="pop")
    show(c, t, 75.6, 740, 540, sc(check_icon, 50), anim="pop")
    show(c, t, 75.8, 740, 910, M("SACA", 54, GREEN), anim="stamp")
    hero(c, t, CX, FY, 0.5, [(0, "finger_up"), (73.9, "head")], [(0, "worried"), (73.9, "shocked")], look=0)


def s13(c, t):  # 76.3 - fim  salva, manda, segue
    floor(c)
    show(c, t, 76.4, 320, 320, group(sc(bookmark_icon), at(0, 110, T("salva", 52))), anim="pop")
    show(c, t, 77.7, 700, 320, group(sc(send_icon), at(0, 110, T("manda pra quem precisa", 46))), anim="pop")
    show(c, t, 79.0, CX - 40, 620, lambda c: hl(c, "SEGUE PRA MAIS CONTAS", 0, 0, 72, LYELLOW), anim="stamp")
    if t > 79.1:
        k = ease_out(prog(t, 79.1, 0.4))
        arrow(c, CX + 130, 920, CX + 130, 920 - 180 * k, GOLD, 12, 0.0, 34)
    hero(c, t, CX + 30, FY, 0.85, [(0, "thumb"), (79.0, "point_ru")], [(0, "happy"), (79.0, "grin")], look=0.3)


def bookmark_icon(c):
    poly(c, [(-45, -70), (45, -70), (45, 70), (0, 35), (-45, 70)])
    fs(c, GOLD, 6)


def send_icon(c):
    poly(c, [(-70, -50), (75, 0), (-70, 55), (-45, 0)])
    fs(c, LBLUE, 6)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 6.8, s01), (6.8, 14.1, s02), (14.1, 18.1, s03), (18.1, 25.2, s04), (25.2, 30.5, s05),
    (30.5, 35.7, s06), (35.7, 40.2, s07), (40.2, 47.8, s08), (47.8, 52.6, s09), (52.6, 62.7, s10),
    (62.7, 70.2, s11), (70.2, 76.3, s12), (76.3, 999.0, s13),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
