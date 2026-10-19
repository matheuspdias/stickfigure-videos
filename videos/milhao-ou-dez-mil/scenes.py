"""R$ 1 milhão agora ou R$ 10 mil por mês pra sempre? Só TikTok: vertical nativo 1080x1920, 81,6 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout vertical (antes do SHIFT de 60): título y~250, palco y 360-1230, legendas em y~1400.
Premissas (19/10/2026): 0,8% a.m. líquido (10,03% a.a.); inflação 4% a.a. (Focus 13/10: 5,22% 2026, 4,30% 2027,
3,79% 2028, 3,50% 2029). Juro real 5,80% a.a. -> 0,471% a.m. -> saque real de R$ 4.711/mês.
10 mil fixos em dinheiro de hoje: 10a 6.756 | 20a 4.564 | 30a 3.083. Cruzamento: ano 19,2.
VP de 10 mil/mês perpétuo a 0,8% = 10.000/0,008 = R$ 1.250.000. Gasto real sustentável: 1,25 mi x 0,471% = R$ 5.889.
Gastando 5.889 corrigidos e investindo a sobra: fundo de R$ 864 mil (dinheiro de hoje) no ano 30, nunca zera."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)

SFX = [(11.1, "tum"), (18.0, "tum"), (48.4, "tum"), (70.3, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- personagens e helpers
def rico(c, t, x, s, poses, exprs, **kw):
    """o dono do milhão"""
    kw.setdefault("shirt", GREEN); kw.setdefault("fid", 2)
    other(c, t, x, FY, s, poses, exprs, **kw)


def mensal(c, t, x, s, poses, exprs, **kw):
    """quem recebe os 10 mil por mês"""
    kw.setdefault("shirt", ORANGE); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, FY, s, poses=poses, exprs=exprs, **kw)


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def vault(c, label="R$ 1 MILHÃO"):
    """cofre com o milhão"""
    rrect(c, -150, -130, 300, 260, 22); fs(c, DGRAY, 6)
    rrect(c, -125, -105, 250, 210, 14); fs(c, GRAY, 5)
    circle(c, 0, -15, 48, LGRAY, 6)
    for k in range(6):
        a = k * math.pi / 3
        line(c, 0, -15, 40 * math.cos(a), -15 + 40 * math.sin(a), 4)
    if label:
        text(c, label, 0, 185, 50, MARKER, NAVY)
    rrect(c, -120, 128, 40, 22, 4); fs(c, DGRAY, 4)
    rrect(c, 80, 128, 40, 22, 4); fs(c, DGRAY, 4)


def note10(c, k=1.0, label=None, col=GREEN):
    """nota de 10 mil encolhendo (k = poder de compra relativo)"""
    c.save(); c.scale(k * 2.0, k * 2.0); bill(c); c.restore()
    if label:
        text(c, label, 0, 46 * k * 2 + 50, 54, MARKER, col)


def wave_bills(c, t, x0, y0, n=5):
    for i in range(n):
        ph = (t * 1.3 + i * 0.37) % 1.0
        c.save(); c.translate(x0 + (i - n / 2) * 60, y0 - ph * 90); c.rotate(-0.3 + i * 0.15)
        c.push_group(); c.scale(0.55, 0.55); bill(c); c.pop_group_to_source()
        c.paint_with_alpha(1 - ph)
        c.restore()


def cross_chart(c, t, t0):
    """10 mil fixos (vermelho, caindo com a inflação) x saque real do milhão (verde, R$ 4.711 constantes), 30 anos"""
    x0, x1, yb, H = 150, 900, 1000, 560
    vy = lambda v: yb - v / 10000 * H
    yx = lambda yr: x0 + (x1 - x0) * yr / 30
    line(c, x0, yb, x1 + 20, yb, 6)
    line(c, x0, yb, x0, yb - H - 40, 6)
    for yr in (0, 10, 20, 30):
        text(c, str(yr), yx(yr), yb + 42, 40, HAND, DGRAY)
    text(c, "anos", x1 + 10, yb + 92, 40, HAND, DGRAY, align="r")
    k = ease_io(prog(t, t0, 2.6))
    n = max(2, int(120 * k))
    pts_r = [(yx(30 * i / 120), vy(10000 / 1.04 ** (30 * i / 120))) for i in range(n + 1)]
    c.move_to(*pts_r[0])
    for p in pts_r[1:]:
        c.line_to(*p)
    rgb(c, RED); c.set_line_width(11); c.stroke()
    line(c, x0, vy(4711), x0 + (x1 - x0) * k * (n / 120), vy(4711), 11, GREEN)
    text(c, "R$ 10 mil fixos", x0 + 40, vy(10000) - 30, 44, MARKER, RED, align="l")
    text(c, "milhão: R$ 4.700", x0 + 20, vy(4711) - 40, 42, MARKER, GREEN, align="l")
    if k > 19.2 / 30:
        a = clamp01((t - t0 - 1.6) / 0.3)
        cx, cy = yx(19.2), vy(4711)
        c.push_group()
        circle(c, cx, cy, 26, GOLD, 6)
        c.save(); c.set_dash([16, 12]); line(c, cx, cy + 28, cx, yb, 5, GOLD); c.restore()
        c.pop_group_to_source(); c.paint_with_alpha(a)


def vbar(x, h, col, label, top, t, t0, base=1000):
    def f(c):
        hh = h * ease_out(prog(t, t0, 0.5))
        c.save(); c.translate(x, base); bar(c, hh, 190, col, label, top if hh > h * 0.95 else None, 46); c.restore()
    return f


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.3  gancho
    floor(c)
    show(c, t, 0.0, 280, 380, group(sc(vault, "1 MILHÃO", s=0.9), at(0, 240, M("AGORA", 52, RED))), anim="stamp", d=0.35)
    show(c, t, 0.0, 780, 380, group(sc(calendar, "10 mil", GREEN, 44, s=1.5), at(0, 170, M("TODO MÊS", 52, NAVY))),
         anim="stamp", d=0.35)
    show(c, t, 0.2, CX + 10, 380, lambda c: hl(c, "OU", 0, 0, 80, LYELLOW), anim="pop")
    show(c, t, 3.7, 780, 640, lambda c: hl(c, "pra sempre", 0, 0, 60, LGREEN), anim="stamp")
    show(c, t, 4.5, CX, 770, stamp_txt("ESCOLHE!", RED, 92), anim="stamp")
    hero(c, t, CX, FY, 0.72, [(0, "think"), (4.5, "point_r")], [(0, "think"), (4.5, "confident")], appear=0.0, look=0)


def s02(c, t):  # 6.3 - 14.4  primeira conta: 0,8% de 1 milhão = 8 mil
    floor(c)
    title(c, t, 6.5, "Primeira conta", y=250, size=80)
    show(c, t, 7.9, 300, 520, sc(vault, s=0.8), anim="pop")
    show(c, t, 9.1, 760, 430, M("x 0,8%", 84, NAVY), anim="up")
    show(c, t, 10.2, 760, 520, T("ao mês", 54), anim="up")
    show(c, t, 11.1, 760, 680, lambda c: hl(c, "R$ 8 mil/mês", 0, 0, 76, LGREEN), anim="stamp")
    if t > 11.2:
        wave_bills(c, t, 330, 420)
    show(c, t, 13.1, 300, 820, T("sem mexer no milhão", 50, DGRAY), anim="up")
    hero(c, t, 830, FY, 0.65, [(0, "present_l"), (11.1, "thumb")], [(0, "neutral"), (11.1, "happy")],
         prop=("r", prop_calculator), look=-1)


def s03(c, t):  # 14.4 - 17.0  10 mil é mais
    floor(c)
    show(c, t, 14.5, 330, 1000, vbar(0, 320, GREEN, "milhão", "R$ 8 mil", t, 14.5, 0), anim="fade", d=0.1)
    show(c, t, 14.7, 710, 1000, vbar(0, 400, GOLD, "mensal", "R$ 10 mil", t, 14.7, 0), anim="fade", d=0.1)
    show(c, t, 15.3, CX, 300, M("10 mil é mais...", 80, NAVY), anim="up")
    show(c, t, 16.0, CX, 420, T("fácil, né?", 64, DGRAY), anim="up")
    hero(c, t, 920, FY, 0.55, [(0, "shrug")], [(0, "happy")], look=-1)


def s04(c, t):  # 17.0 - 31.8  a inflação encolhe os 10 mil
    floor(c)
    show(c, t, 17.6, CX, 240, stamp_txt("INFLAÇÃO", RED, 90), anim="stamp")
    show(c, t, 21.5, CX, 345, T("4% ao ano, e os 10 mil nunca sobem", 48, DGRAY), anim="up")
    # nota "hoje" grande e as três notas encolhendo
    stops = [(18.7, 0, 1.0, "R$ 10.000", GREEN), (23.4, 10, 0.6756, "R$ 6.750", ORANGE),
             (27.5, 20, 0.4564, "R$ 4.550", RED), (29.9, 30, 0.3083, "R$ 3.100", RED)]
    pos = [(290, 580), (760, 580), (290, 1000), (760, 1000)]
    for (t0, yr, k, lab, col), (x, y) in zip(stops, pos):
        tag = "hoje" if yr == 0 else f"daqui a {yr} anos"
        show(c, t, t0, x, y, group(sc(note10, math.sqrt(k), None), at(0, 150, M(lab, 58, col)),
                                   at(0, -140, T(tag, 46, DGRAY))), anim="pop")
    hero(c, t, 990, FY, 0.45, [(0, "relax"), (18.0, "head"), (27.5, "shrug")],
         [(0, "neutral"), (18.0, "shocked"), (27.5, "worried")], look=-1)


def s05(c, t):  # 31.8 - 41.3  o milhão: saque do juro real, corrigido pra sempre
    floor(c)
    show(c, t, 31.9, CX, 250, M("E o milhão?", 84, NAVY), anim="up")
    show(c, t, 32.9, 280, 560, sc(vault, s=0.85), anim="pop")
    show(c, t, 33.7, 740, 440, T("saca só o juro real", 54), anim="up")
    show(c, t, 35.2, 740, 560, lambda c: hl(c, "R$ 4.700/mês", 0, 0, 70, LGREEN), anim="stamp")
    show(c, t, 37.2, 740, 670, T("corrigidos pela inflação", 48, DGRAY), anim="up")
    show(c, t, 38.9, 740, 770, M("pra sempre", 64, GREEN), anim="pop")
    show(c, t, 39.8, 300, 830, lambda c: ribbon(c, "o milhão fica", NAVY, 44), anim="stamp")
    rico(c, t, 160, 0.55, [(0, "relax"), (35.2, "thumb")], [(0, "neutral"), (35.2, "happy")], look=1)
    hero(c, t, 900, FY, 0.55, [(0, "present_l")], [(0, "neutral"), (39.8, "confident")], look=-1)


def s06(c, t):  # 41.3 - 45.1  cruzamento no ano 19
    floor(c)
    title(c, t, 41.3, "O cruzamento", y=250, size=78)
    cross_chart(c, t, 41.4)
    show(c, t, 42.1, 740, 930, lambda c: hl(c, "ano 19", 0, 0, 70, LYELLOW), anim="stamp")
    hero(c, t, 960, FY, 0.42, [(0, "point_lu")], [(0, "confident")], look=-1)


def s07(c, t):  # 45.1 - 49.2  então o milhão ganha? calma, segunda virada
    floor(c)
    show(c, t, 45.2, CX, 330, M("Então o milhão ganha?", 70, NAVY), anim="up")
    show(c, t, 46.8, CX, 540, M("CALMA", 120, INK), anim="stamp")
    show(c, t, 48.4, CX, 760, stamp_txt("2ª VIRADA", RED, 96), anim="stamp")
    rico(c, t, 220, 0.6, [(0, "arms_up"), (46.8, "relax")], [(0, "grin"), (46.8, "neutral")], look=1)
    hero(c, t, 830, FY, 0.6, [(0, "think"), (46.8, "finger_up")], [(0, "think"), (46.8, "confident")], look=-1)


def s08(c, t):  # 49.2 - 56.6  10 mil por mês pra sempre valem 1,25 milhão hoje
    floor(c)
    show(c, t, 49.3, CX, 250, T("10 mil/mês pra sempre, a 0,8%...", 54), anim="up")
    show(c, t, 53.0, CX, 380, T("valem hoje", 60, DGRAY), anim="up")
    show(c, t, 53.6, CX, 520, lambda c: hl(c, "R$ 1.250.000", 0, 0, 100, LGREEN), anim="stamp")
    show(c, t, 54.4, CX, 790, lambda c: balance(c, 0.7,
                                                lambda c: hl(c, "1 mi", 0, -45, 42, WHITE, NAVY),
                                                lambda c: hl(c, "1,25 mi", 0, -45, 42, LGREEN, INK)),
         anim="pop")
    mensal(c, t, 900, 0.5, [(0, "relax"), (53.6, "arms_up")], [(0, "neutral"), (53.6, "grin")], look=-1)
    hero(c, t, 150, FY, 0.5, [(0, "present")], [(0, "neutral"), (53.6, "confident")], look=1)


def s09(c, t):  # 56.6 - 64.3  gasta quase 6 mil corrigidos e investe o resto
    floor(c)
    show(c, t, 56.8, CX, 250, T("recebe os 10 mil...", 60), anim="up")
    show(c, t, 58.2, 300, 380, lambda c: hl(c, "gasta R$ 5.900", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, 59.4, 300, 460, T("corrigidos", 44, DGRAY), anim="up")
    show(c, t, 60.4, 760, 380, lambda c: hl(c, "investe o resto", 0, 0, 52, LGREEN), anim="stamp")
    show(c, t, 61.5, 350, 1000, vbar(0, 471 * 0.6, NAVY, "milhão", "R$ 4.700", t, 61.5, 0), anim="fade", d=0.1)
    show(c, t, 61.8, 690, 1000, vbar(0, 589 * 0.6, ORANGE, "mensal", "R$ 5.900", t, 61.8, 0), anim="fade", d=0.1)
    show(c, t, 63.6, CX, 1120, M("pra sempre", 60, GREEN), anim="pop")
    mensal(c, t, 930, 0.45, [(0, "hold"), (61.8, "arms_up")], [(0, "happy"), (61.8, "grin")], look=-1)
    hero(c, t, 110, FY, 0.45, [(0, "point_r")], [(0, "confident")], look=1)


def s10(c, t):  # 64.3 - 69.2  e em 30 anos ainda tem mais de 800 mil guardados
    floor(c)
    show(c, t, 64.5, CX, 260, M("em 30 anos...", 84, NAVY), anim="up")
    show(c, t, 65.5, 250, 620, sc(piggy, s=1.25), anim="pop")
    show(c, t, 66.3, 720, 560, lambda c: hl(c, "+R$ 800 mil", 0, 0, 84, LGREEN), anim="stamp")
    show(c, t, 67.4, 720, 680, T("guardados", 56), anim="up")
    show(c, t, 68.2, 720, 780, T("em dinheiro de hoje", 48, DGRAY), anim="up")
    mensal(c, t, 330, 0.55, [(0, "arms_up")], [(0, "grin")], look=0.5)
    hero(c, t, 880, FY, 0.55, [(0, "thumb")], [(0, "happy")], look=-1)


def s11(c, t):  # 69.2 - 78.2  a resposta é disciplina
    floor(c)
    show(c, t, 69.3, CX, 240, T("a resposta é...", 60), anim="up")
    show(c, t, 70.3, CX, 370, lambda c: hl(c, "DISCIPLINA", 0, 0, 104, LYELLOW), anim="stamp")
    show(c, t, 71.4, 280, 560, T("guarda a sobra", 52), anim="up")
    show(c, t, 73.8, 280, 660, lambda c: hl(c, "10 mil/mês", 0, 0, 58, LGREEN), anim="stamp")
    show(c, t, 74.8, 770, 560, T("gasta tudo", 52), anim="up")
    show(c, t, 77.5, 770, 660, lambda c: hl(c, "o milhão", 0, 0, 58, LGREEN), anim="stamp")
    mensal(c, t, 280, 0.5, [(0, "relax"), (73.8, "thumb")], [(0, "neutral"), (73.8, "happy")], look=0.5)
    rico(c, t, 770, 0.5, [(0, "relax"), (77.5, "thumb")], [(0, "neutral"), (77.5, "happy")], look=-0.5)
    hero(c, t, CX, FY, 0.42, [(0, "present"), (70.3, "finger_up")], [(0, "neutral"), (70.3, "confident")], look=0)


def s12(c, t):  # 78.2 - fim  pergunta final
    floor(c)
    show(c, t, 78.3, 280, 360, group(sc(vault, "1 MILHÃO", s=0.65)), anim="pop")
    show(c, t, 78.3, 760, 360, sc(calendar, "10 mil", GREEN, 44, s=1.2), anim="pop")
    show(c, t, 78.9, CX, 600, M("Qual você escolheu?", 74, NAVY), anim="stamp")
    show(c, t, 80.0, CX, 700, T("mudou de ideia?", 60), anim="up")
    show(c, t, 81.0, CX + 120, 880, group(lambda c: speech(c, 480, 130, -160, 110), T("Comenta!", 64)), anim="pop")
    hero(c, t, 280, FY, 0.72, [(0, "point_r"), (81.0, "wave")], [(0, "happy"), (81.0, "grin")], look=1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 6.3, s01), (6.3, 14.4, s02), (14.4, 17.0, s03), (17.0, 31.8, s04), (31.8, 41.3, s05),
    (41.3, 45.1, s06), (45.1, 49.2, s07), (49.2, 56.6, s08), (56.6, 64.3, s09), (64.3, 69.2, s10),
    (69.2, 78.2, s11), (78.2, 999.0, s12),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
