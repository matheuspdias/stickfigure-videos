"""Pagar o mínimo da fatura: R$ 1.000 vira quase R$ 2.000. Só TikTok: vertical nativo 1080x1920, 67,2 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout vertical como em reserva-emergencia: título y~250, palco y 360-1230 (+SHIFT), nada em x > 930.
Premissas: BC ago/2026 rotativo 15,18% a.m., parcelado 9,34% a.m.; teto Lei 14.690/2023 (100% da dívida)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)

SFX = [(1.0, "tum"), (36.9, "tum"), (52.3, "tum"), (58.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- personagens e helpers
def voce(c, t, x, s, poses, exprs, **kw):
    """o espectador: pessoa comum de camiseta laranja"""
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 2)
    other(c, t, x, FY, s, poses, exprs, **kw)


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def fatura_app(val, sub=None, sub_col=GREEN, s=1.0):
    """celular grande com o app do banco mostrando a fatura"""
    def f(c):
        c.save(); c.scale(s, s)
        rrect(c, -170, -300, 340, 600, 40); fs(c, DGRAY, 7)
        rrect(c, -148, -262, 296, 500, 14); fs(c, WHITE, 0)
        c.rectangle(-148, -262, 296, 90); rgb(c, NAVY); c.fill()
        text(c, "FATURA", 0, -217, 50, MARKER, WHITE)
        text(c, "total", 0, -120, 40, HAND, DGRAY)
        text(c, val, 0, -50, 60, MARKER, INK)
        if sub:
            rrect(c, -120, 40, 240, 90, 16); fs(c, sub_col, 0)
            text(c, sub, 0, 85, 42, MARKER, WHITE)
        line(c, -110, 180, 110, 180, 6, LGRAY)
        circle(c, 0, 272, 10, WHITE, 3)
        c.restore()
    return f


def debt_bar(c, t, t0, x, base, h, w, col, label, top=None, size=44, d=0.6):
    k = ease_out(prog(t, t0, d))
    if k <= 0:
        return
    hh = h * k
    rrect(c, x - w / 2, base - hh, w, hh, 10); fs(c, col, 6)
    if label:
        text(c, label, x, base + 45, size, HAND, INK)
    if top and k > 0.95:
        text(c, top, x, base - hh - 40, 52, MARKER, col)


def parcel_grid(c, t, t0, n=12, cols=4, cell=150):
    for i in range(n):
        if t < t0 + i * 0.09:
            continue
        x = (i % cols - (cols - 1) / 2) * cell
        y = (i // cols) * 140
        c.save(); c.translate(x, y); c.scale(0.62, 0.62); envelope(c); c.restore()
        text(c, str(i + 1), x, y + 70, 36, MARKER, RED)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.3  gancho
    floor(c)
    show(c, t, 0.0, CX, 270, lambda c: hl(c, "PAGAR SÓ O MÍNIMO?", 0, 0, 66, LYELLOW), anim="stamp", d=0.35)
    show(c, t, 0.4, CX - 190, 560, sc(card, NAVY, s=1.5), anim="pop")
    show(c, t, 2.0, CX - 190, 720, T("parece que salva...", 50), anim="up")
    show(c, t, 0.3, CX + 200, 500, M("R$ 1.000", 80, INK), anim="pop")
    if t > 0.7:
        arrow_draw(c, t, 0.7, CX + 200, 560, CX + 200, 700, d=0.35, col=RED)
    show(c, t, 1.0, CX + 200, 790, lambda c: hl(c, "quase R$ 2 .000", 0, 0, 66, PINKISH, RED), anim="stamp")
    hero(c, t, CX, FY, 0.8, [(0, "think"), (3.4, "head")], [(0, "think"), (3.4, "shocked")], look=0)


def s02(c, t):  # 6.3 - 12.7  fatura de mil; paga o mínimo de 150 e respira aliviado
    floor(c)
    show(c, t, 6.4, 330, 560, fatura_app("R$ 1.000", s=1.0), anim="up")
    if t > 9.5:
        show(c, t, 9.5, 330, 560, fatura_app("R$ 1.000", "mín. R$ 150", GREEN, s=1.0), anim="fade", d=0.15)
    show(c, t, 10.2, 760, 430, group(lambda c: speech(c, 300, 130, -100, 110), T("paguei R$ 150", 48)), anim="pop")
    show(c, t, 11.4, 760, 620, M("ufa...", 72, GREEN), anim="pop")
    voce(c, t, 760, 0.8, [(0, "hold"), (11.4, "relax")], [(0, "worried"), (11.4, "happy")], look=-0.5)


def s03(c, t):  # 12.7 - 19.2  os 850 vão pro rotativo a 15% ao mês
    floor(c)
    show(c, t, 13.2, CX, 260, M("sobraram R$ 850", 80, INK), anim="up")
    show(c, t, 15.6, CX, 450, lambda c: ribbon(c, "ROTATIVO", RED, 70), anim="stamp")
    show(c, t, 17.6, CX, 650, lambda c: hl(c, "15% ao mês", 0, 0, 100, PINKISH, RED), anim="stamp")
    show(c, t, 18.3, CX, 770, T("taxa média do Banco Central", 46, DGRAY), anim="up")
    voce(c, t, 180, 0.62, [(0, "relax"), (17.6, "head")], [(0, "neutral"), (17.6, "worried")], look=1)
    hero(c, t, 870, FY, 0.62, [(0, "relax"), (15.6, "point_lu")], [(0, "neutral"), (15.6, "worried")], look=-1)


def s04(c, t):  # 19.2 - 23.1  no mês seguinte já são 980
    floor(c)
    title(c, t, 19.3, "No mês seguinte...", y=250, size=72)
    base = 900
    debt_bar(c, t, 19.6, 330, base, 400, 180, GOLD, "hoje", "R$ 850")
    debt_bar(c, t, 21.5, 680, base, 461, 180, RED, "1 mês depois", "R$ 980")
    if t > 21.0:
        arrow_draw(c, t, 21.0, 440, 520, 570, 470, d=0.4, col=RED)
    voce(c, t, 160, 0.55, [(0, "head")], [(0, "worried"), (21.6, "shocked")], look=1)
    hero(c, t, 900, FY, 0.55, [(0, "relax")], [(0, "worried")], look=-1)


def s05(c, t):  # 23.1 - 26.0  o rotativo só pode durar uma fatura
    floor(c)
    show(c, t, 23.2, CX, 270, M("Rotativo:", 84, RED), anim="up")
    show(c, t, 24.0, CX - 160, 560, sc(calendar, "1", RED, 90, s=1.7), anim="pop")
    show(c, t, 24.9, CX + 190, 560, lambda c: stamp_txt("SÓ 1 FATURA", NAVY, 62)(c), anim="stamp")
    hero(c, t, CX, FY, 0.75, [(0, "present"), (24.6, "finger_up")], [(0, "neutral"), (24.6, "confident")], look=0)


def s06(c, t):  # 26.0 - 31.4  o banco te passa pro parcelado da fatura, ~9% ao mês
    floor(c)
    show(c, t, 26.1, 260, 480, group(sc(bank, s=1.0), at(0, 150, T("banco", 50))), anim="pop")
    if t > 27.4:
        arrow_draw(c, t, 27.4, 380, 470, 560, 470, d=0.4, col=INK)
    show(c, t, 28.2, 760, 440, lambda c: ribbon(c, "PARCELADO", NAVY, 56), anim="stamp")
    show(c, t, 28.7, 760, 530, T("da fatura", 52), anim="up")
    show(c, t, 29.9, CX, 760, lambda c: hl(c, "~9% ao mês", 0, 0, 96, PINKISH, RED), anim="stamp")
    voce(c, t, 230, 0.55, [(0, "relax"), (29.9, "shrug")], [(0, "neutral"), (29.9, "worried")], look=1)
    hero(c, t, 850, FY, 0.55, [(0, "point_lu")], [(0, "neutral")], look=-1)


def s07(c, t):  # 31.4 - 34.5  12 parcelas de 139
    floor(c)
    show(c, t, 31.5, CX, 250, M("12x R$ 139", 100, RED), anim="stamp")
    show(c, t, 31.6, CX, 420, lambda c: parcel_grid(c, t, 31.6), anim="fade", d=0.1)
    voce(c, t, 220, 0.55, [(0, "head")], [(0, "worried")], look=1)
    hero(c, t, 830, FY, 0.55, [(0, "relax"), (33.0, "shrug")], [(0, "worried")], look=-1)


def s08(c, t):  # 34.5 - 40.9  total pago: 1.819, por uma fatura de mil
    floor(c)
    show(c, t, 34.6, CX, 250, T("somando tudo, você pagou", 60), anim="up")
    show(c, t, 35.3, CX, 360, T("R$ 150  +  12x R$ 139", 52, DGRAY), anim="up")
    show(c, t, 36.9, CX, 560, M("R$ 1.819", 190, RED), anim="stamp", d=0.35)
    show(c, t, 39.5, CX, 790, group(T("por uma fatura de R$ 1.000", 56), at(0, 6, lambda c: None)), anim="up")
    voce(c, t, 200, 0.62, [(0, "hold"), (36.9, "head")], [(0, "neutral"), (36.9, "desperate")], look=1)
    hero(c, t, 860, FY, 0.62, [(0, "relax"), (37.0, "head")], [(0, "neutral"), (37.0, "shocked")], look=-1)


def s09(c, t):  # 40.9 - 45.0  e em 24 vezes? passaria de 2.600
    floor(c)
    show(c, t, 41.0, CX, 260, M("E em 24x?", 100, NAVY), anim="stamp")
    base = 1000
    debt_bar(c, t, 41.3, 330, base, 330, 180, RED, "12x", "R$ 1.819")
    debt_bar(c, t, 42.6, 690, base, 480, 180, RED, "24x", "R$ 2 .636")
    hero(c, t, 920, FY, 0.5, [(0, "think"), (43.4, "head")], [(0, "think"), (43.4, "shocked")], look=-1)


def s10(c, t):  # 45.0 - 50.8  desde 2024, a lei limita juros e encargos ao valor da dívida
    floor(c)
    show(c, t, 45.1, CX, 260, M("Só que...", 84, INK), anim="up")
    show(c, t, 46.0, CX, 430, lambda c: ribbon(c, "LEI, DESDE 2024", NAVY, 62), anim="stamp")
    show(c, t, 47.7, 330, 640, group(sc(document, "LEI", NAVY, 40, s=1.3)), anim="pop")
    show(c, t, 48.5, 680, 600, T("juros + encargos", 56, RED), anim="up")
    show(c, t, 49.6, 680, 690, T("no máximo o valor", 52), anim="up")
    show(c, t, 50.1, 680, 760, T("da dívida", 52), anim="up")
    hero(c, t, CX, FY, 0.62, [(0, "present"), (47.6, "finger_up")], [(0, "neutral"), (47.6, "confident")],
         prop=("l", prop_pointer), look=0)


def s11(c, t):  # 50.8 - 55.1  no máximo dobra; e dobrar já é um desastre
    floor(c)
    base = 960
    x = 400
    # dívida que foi pro rotativo
    debt_bar(c, t, 50.9, x, base, 260, 220, GOLD, None, None)
    show(c, t, 51.2, x, base - 130, M("R$ 850", 48, WHITE), anim="fade")
    # juros em cima, até o teto
    if t > 51.6:
        k = ease_out(prog(t, 51.6, 0.6))
        hh = 260 * k
        rrect(c, x - 110, base - 260 - hh, 220, hh, 10); fs(c, RED, 6)
        if k > 0.9:
            text(c, "juros", x, base - 390, 48, MARKER, WHITE)
    if t > 52.3:
        k = ease_out(prog(t, 52.3, 0.4))
        c.save(); c.set_dash([22, 14]); line(c, x - 150, base - 520, x - 150 + 300 * k, base - 520, 8, INK); c.restore()
        show(c, t, 52.3, 740, base - 520, M("TETO: x2", 60, INK), anim="pop")
    show(c, t, 52.6, 760, base - 380, T("máx. R$ 1.700", 50, RED), anim="up")
    show(c, t, 53.1, CX, 290, lambda c: hl(c, "DOBRAR JÁ É UM DESASTRE", 0, 0, 64, PINKISH, RED), anim="stamp")
    hero(c, t, 860, FY, 0.55, [(0, "point_lu"), (53.1, "head")], [(0, "neutral"), (53.1, "desperate")], look=-1)


def s12(c, t):  # 55.1 - 63.7  o que fazer: negocie antes do rotativo e compare a taxa
    floor(c)
    show(c, t, 55.2, CX, 250, lambda c: ribbon(c, "O QUE FAZER?", GREEN, 66), anim="stamp")
    show(c, t, 56.3, CX, 400, T("não dá pra pagar tudo?", 56), anim="up")
    show(c, t, 58.2, 300, 600, group(sc(bank, s=0.8), at(0, 130, T("negocie direto", 48, GREEN))), anim="pop")
    show(c, t, 60.6, 720, 560, group(M("rotativo", 60, RED), at(0, 6, strike(260))), anim="up")
    show(c, t, 60.9, 720, 640, lambda c: hl(c, "ANTES dele", 0, 0, 56, LYELLOW), anim="stamp")
    show(c, t, 62.5, CX - 170, 850, group(sc(calculator, "% a.m.", s=0.6), at(250, 0, T("compare a taxa", 60, NAVY))), anim="pop")
    hero(c, t, 860, FY, 0.55, [(0, "present"), (58.2, "finger_up"), (62.5, "thumb")],
         [(0, "neutral"), (58.2, "confident"), (62.5, "grin")], look=-1)
    voce(c, t, 180, 0.55, [(0, "think"), (62.5, "thumb")], [(0, "think"), (62.5, "happy")], look=1)


def s13(c, t):  # 63.7 - fim  pergunta final
    floor(c)
    show(c, t, 63.8, CX, 290, M("Já pagou", 90, NAVY), anim="stamp")
    show(c, t, 64.4, CX, 420, M("só o mínimo?", 90, RED), anim="stamp")
    show(c, t, 65.6, CX + 120, 700, group(lambda c: speech(c, 560, 140, -170, 120), T("Comenta sem vergonha!", 52)),
         anim="pop")
    hero(c, t, 300, FY, 0.75, [(0, "point_r"), (65.6, "wave")], [(0, "happy"), (65.6, "grin")], look=1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 6.3, s01), (6.3, 12.7, s02), (12.7, 19.2, s03), (19.2, 23.1, s04), (23.1, 26.0, s05),
    (26.0, 31.4, s06), (31.4, 34.5, s07), (34.5, 40.9, s08), (40.9, 45.0, s09), (45.0, 50.8, s10),
    (50.8, 55.1, s11), (55.1, 63.7, s12), (63.7, 999.0, s13),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
