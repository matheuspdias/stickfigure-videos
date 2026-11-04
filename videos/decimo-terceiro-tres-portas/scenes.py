"""O que fazer com o 13º antes do dia 30 (parte 2 de videos/decimo-terceiro-quanto-cai). Só TikTok: 1080x1920.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco de 87,7 s acelerado 8% (atempo 1.08) = 81,2 s.
palavras.json já está na escala acelerada (palavras_heygen_1x.json guarda os tempos originais).
Números conferidos em contas.py (04/11/2026, BC set/2026). Mesma Ana do videos/decimo-terceiro."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
PINKISH = (1, 0.8, 0.76)
ANA = dict(shirt=PINK, hair="long")

SFX = [(0.1, "tum"), (34.5, "tum"), (57.5, "soft_ding"), (64.7, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


def m(s):
    """Permanent Marker apaga o ponto de milhar depois do 2: espaço finíssimo"""
    return s.replace("2.", "2 .")


def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def M(s, size=60, col=INK):
    return lambda c: text(c, m(s), 0, 0, size, MARKER, col)


def H(s, size=60, bg=LYELLOW, col=INK):
    return lambda c: hl(c, m(s), 0, 0, size, bg, col)


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 8, w / 2, -8, 10, col)


def porta(num, col, t, t_open=None, s=1.0):
    """porta que abre a partir de t_open"""
    k = 0.0 if t_open is None else ease_out(prog(t, t_open, 0.6))
    def f(c):
        c.save(); c.scale(s, s); door(c, num, col, k); c.restore()
    return f


def envelope13(s=1.0, col=GOLD):
    def f(c):
        c.save(); c.scale(s, s)
        envelope(c)
        circle(c, 0, 18, 36, col, 5)
        text(c, "13º", 0, 22, 30, MARKER, WHITE)
        c.restore()
    return f


DOOR_COLS = {1: RED, 2: BLUE, 3: GREEN}


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.1  gancho: dívida ou patrimônio
    floor(c)
    show(c, t, 0.0, CX, 250, M("O MESMO 13º", 110, NAVY), anim="stamp", d=0.3)
    show(c, t, 0.1, 270, 470, sc(card, RED), anim="pop", d=0.3)
    show(c, t, 0.2, 270, 640, H("R$ 5.500", 74, PINKISH, RED), anim="stamp", d=0.3)
    show(c, t, 0.4, 270, 735, T("de dívida", 50, RED), anim="up")
    show(c, t, 0.3, CX, 480, T("ou", 60, DGRAY), anim="pop")
    show(c, t, 0.5, 760, 470, sc(piggy, GREEN), anim="pop", d=0.3)
    show(c, t, 0.6, 760, 640, H("R$ 180 MIL", 70, LGREEN, GREEN), anim="stamp", d=0.3)
    show(c, t, 0.8, 760, 735, T("investido", 50, GREEN), anim="up")
    # texto mudo entre 3 e 5 s
    if 3.0 <= t < 5.3:
        k = ease_out(prog(t, 3.0, 0.3)) * (1 - ease_out(prog(t, 5.0, 0.3)))
        c.save(); c.translate(CX, 880); c.scale(0.6 + 0.4 * k, 0.6 + 0.4 * k)
        rrect(c, -440, -78, 880, 156, 24); fs(c, NAVY, 7)
        text(c, "PARTE 2", -230, -6, 70, MARKER, GOLD)
        text(c, "prometido no", 140, -28, 40, HAND, WHITE)
        text(c, "vídeo do 13º", 140, 24, 40, HAND, WHITE)
        c.save(); c.translate(380, 0); check_icon(c, 40); c.restore()
        c.restore()
    show(c, t, 6.7, 330, 900, group(sc(calendar, "30", RED, 72), at(0, 130, T("antes do dia 30", 54))), anim="pop")
    hero(c, t, 800, FY, 0.62, [(0, "think"), (6.7, "finger_up")], [(0, "shocked"), (6.7, "confident")], look=-0.5)


def s02(c, t):  # 9.1 - 17.0  Ana e o 13º líquido
    floor(c)
    show(c, t, 9.2, CX, 250, lambda c: ribbon(c, "A ANA", NAVY, 72), anim="stamp")
    show(c, t, 10.0, 280, 420, M("R$ 3.000", 72, NAVY), anim="pop")
    show(c, t, 10.3, 280, 500, T("de salário", 48), anim="up")
    show(c, t, 11.4, 700, 470, envelope13(1.6), anim="pop")
    if t > 13.6:
        show(c, t, 13.6, 700, 620, lambda c: (line(c, -150, 0, -110, 0, 9, RED),
                                              text(c, "INSS", -90, 0, 60, HAND, RED, align="l")), anim="left")
    show(c, t, 14.8, 640, 800, group(H("R$ 2.750", 90, LGREEN, GREEN), at(-260, 0, T("uns", 50, DGRAY))), anim="stamp")
    show(c, t, 15.6, 640, 900, T("no bolso", 48, GREEN), anim="up")
    other(c, t, 260, FY, 0.6, [(0, "wave"), (11.4, "present"), (14.8, "thumb")],
          [(0, "happy"), (11.4, "neutral"), (14.8, "grin")], look=0.5, **ANA)
    hero(c, t, 880, FY, 0.42, [(0, "present_l")], [(0, "neutral")], look=-1)


def s03(c, t):  # 17.0 - 21.1  três portas, a ordem importa
    floor(c)
    show(c, t, 17.1, CX, 250, M("3 PORTAS", 110, NAVY), anim="stamp")
    for i, t0 in enumerate((18.5, 18.75, 19.0)):
        show(c, t, t0, 200 + i * 320, 640, porta(i + 1, DOOR_COLS[i + 1], t, s=0.85), anim="pop", d=0.35)
    show(c, t, 19.8, CX, 940, stamp_txt("A ORDEM IMPORTA", RED, 66), anim="stamp")
    if t > 20.1:
        arrow_draw(c, t, 20.1, 170, 990, 870, 990, col=NAVY, lw=9)
    hero(c, t, CX, FY, 0.4, [(0, "present"), (19.8, "finger_up")], [(0, "happy"), (19.8, "confident")], look=0)


def s04(c, t):  # 21.1 - 30.3  porta 1: dívida, quite primeiro, 15% ao mês
    floor(c)
    show(c, t, 21.15, 210, 470, porta(1, RED, t, 21.4, 0.8), anim="pop")
    show(c, t, 22.0, 640, 340, M("Dívida no", 64), anim="up")
    show(c, t, 22.6, 560, 450, sc(card, RED, s=0.8), anim="pop")
    show(c, t, 23.3, 790, 450, group(lambda c: (rrect(c, -100, -55, 200, 110, 14), fs(c, WHITE, 6)),
                                     at(0, 0, T("cheque esp.", 34))), anim="pop")
    show(c, t, 24.5, CX, 700, stamp_txt("QUITE PRIMEIRO", GREEN, 74), anim="stamp")
    show(c, t, 26.0, CX, 840, T("rotativo do cartão (BC, set/2026):", 42, DGRAY), anim="fade")
    show(c, t, 28.7, CX, 960, H("~15% AO MÊS", 92, PINKISH, RED), anim="stamp")
    hero(c, t, 880, FY, 0.42, [(0, "point_l"), (24.5, "finger_up"), (28.7, "head")],
         [(0, "neutral"), (24.5, "confident"), (28.7, "shocked")], look=-1)


def s05(c, t):  # 30.3 - 38.9  nenhum investimento paga isso; a dívida pode dobrar
    floor(c)
    show(c, t, 30.4, CX, 250, T("nenhum investimento seguro", 58), anim="up")
    show(c, t, 31.3, CX, 330, T("paga isso", 58), anim="up")
    base = 1000
    sc_ = 400 / 5500
    for x, t0, v, val, col in ((300, 33.8, 2750, "R$ 2.750", NAVY), (700, 35.0, 5500, "R$ 5.500", RED)):
        if t > t0:
            k = ease_out(prog(t, t0, 0.7))
            h = v * sc_ * k
            rrect(c, x - 110, base - h, 220, h, 12); fs(c, col, 6)
            show(c, t, t0 + 0.5, x, base - v * sc_ - 50, M(val, 62, col), anim="pop")
    line(c, 120, base, 900, base, 6)
    show(c, t, 34.4, CX, 440, lambda c: hl(c, "PODE DOBRAR", 0, 0, 80, PINKISH, RED), anim="stamp")
    if t > 36.9:
        arrow_draw(c, t, 36.9, 430, 800, 590, 650, col=RED, lw=9)
    show(c, t, 37.3, CX, 1080, T("(a lei limita os juros ao valor da dívida)", 36, GRAY), anim="fade")
    hero(c, t, 910, FY, 0.38, [(0, "shrug"), (34.4, "head")], [(0, "worried"), (34.4, "desperate")], look=-1)


def s06(c, t):  # 38.9 - 42.9  dica: peça desconto à vista
    floor(c)
    show(c, t, 38.95, CX, 250, lambda c: ribbon(c, "DICA", GOLD, 76, INK), anim="stamp")
    show(c, t, 39.8, 300, 560, sc(bills, 3, s=1.1), anim="pop")
    show(c, t, 40.0, 300, 690, T("dinheiro na mão", 46), anim="up")
    show(c, t, 40.8, 720, 520, sc(phone, s=1.2), anim="pop")
    show(c, t, 41.1, CX, 880, H("PEÇA DESCONTO", 82, LGREEN, GREEN), anim="stamp")
    show(c, t, 41.8, CX, 990, T("pra quitar à vista", 56), anim="up")
    hero(c, t, CX, FY, 0.42, [(0, "finger_up"), (41.1, "thumb")], [(0, "confident"), (41.1, "grin")],
         prop=("l", prop_coin), look=0)


def s07(c, t):  # 42.9 - 50.7  porta 2: reserva
    floor(c)
    show(c, t, 42.95, 210, 470, porta(2, BLUE, t, 43.2, 0.8), anim="pop")
    show(c, t, 44.0, 650, 360, M("Sem reserva", 66), anim="up")
    show(c, t, 44.6, 650, 440, M("de emergência?", 54, DGRAY), anim="up")
    show(c, t, 45.6, CX, 680, stamp_txt("COMECE OU COMPLETE", BLUE, 64), anim="stamp")
    show(c, t, 47.6, 260, 900, group(sc(padlock, GOLD, s=0.75), at(0, 120, T("lugar seguro", 44))), anim="pop")
    show(c, t, 48.7, 640, 900, group(sc(calendar, "", GREEN, 60), at(70, 40, sc(check_icon, 34)),
                                     at(0, 130, T("liquidez diária", 44))), anim="pop")
    hero(c, t, 900, FY, 0.4, [(0, "point_l"), (45.6, "present_l")], [(0, "think"), (45.6, "confident")], look=-1)


def s08(c, t):  # 50.7 - 55.4  sem reserva o imprevisto vai pro cartão e volta pra porta 1
    floor(c)
    show(c, t, 50.75, CX, 250, M("Sem reserva...", 84, NAVY), anim="stamp")
    show(c, t, 52.0, 230, 520, group(sc(wrench_tire, s=0.8), at(0, -150, sc(exclaim, 90))), anim="pop")
    show(c, t, 52.0, 230, 690, T("imprevisto", 48), anim="up")
    if t > 52.7:
        arrow_draw(c, t, 52.7, 370, 520, 560, 520, col=RED, lw=9)
    show(c, t, 53.0, 690, 520, sc(card, RED), anim="pop")
    show(c, t, 53.2, 690, 650, T("cartão", 48, RED), anim="up")
    if t > 54.0:
        arrow_draw(c, t, 54.0, 690, 720, 520, 860, col=RED, lw=9)
    show(c, t, 54.2, 290, 930, porta(1, RED, t, s=0.45), anim="pop")
    show(c, t, 54.4, 650, 930, M("volta pra porta 1", 48, RED), anim="up")
    hero(c, t, 900, FY, 0.4, [(0, "shrug"), (52.0, "head")], [(0, "worried"), (52.0, "desperate")], look=-1)


def s09(c, t):  # 55.4 - 68.1  porta 3: invista, 183 mil em 30 anos
    floor(c)
    show(c, t, 55.45, 190, 450, porta(3, GREEN, t, 55.7, 0.7), anim="pop")
    show(c, t, 56.4, 620, 330, M("Já tem as duas?", 62), anim="up")
    show(c, t, 56.8, 520, 420, group(sc(check_icon, 34), at(40, 0, L_("sem dívida", 42))), anim="left", t1=57.5)
    show(c, t, 57.0, 520, 480, group(sc(check_icon, 34), at(40, 0, L_("reserva", 42))), anim="left", t1=57.5)
    show(c, t, 57.5, 600, 570, stamp_txt("INVISTA", GREEN, 92), anim="stamp")
    show(c, t, 58.6, CX, 680, T("todo ano o 13º, a +5% acima da inflação", 40, DGRAY), anim="fade", t1=66.6)
    base = 1150
    sc_ = 340 / 183000
    for i, (yrs, v, val, t0) in enumerate(((10, 34600, "R$ 35 mil", 60.4), (20, 90900, "R$ 91 mil", 62.0),
                                          (30, 182700, "R$ 183 MIL", 64.6))):
        x = 330 + i * 220
        if t > t0:
            k = ease_out(prog(t, t0, 0.6))
            c.save(); c.translate(x, base)
            bar(c, v * sc_ * k, 150, GREEN if i == 2 else LGREEN, f"{yrs} anos", None, 42)
            c.restore()
            show(c, t, t0 + 0.4, x, base - v * sc_ - 45, M(val, 60 if i == 2 else 44, GREEN if i == 2 else INK), anim="pop")
    show(c, t, 66.7, CX, 690, H("SÓ COM O 13º", 76, LYELLOW), anim="stamp")
    hero(c, t, 110, FY, 0.34, [(0, "point_r"), (57.5, "arms_up"), (64.6, "thumb")],
         [(0, "neutral"), (57.5, "grin"), (64.6, "grin")], look=1)


def L_(s, size=50, col=INK):
    return lambda c: text(c, s, 0, 0, size, HAND, col, align="l")


def s10(c, t):  # 68.1 - 75.4  alívio: 80% investe, 20% curte
    floor(c)
    show(c, t, 68.2, CX, 250, M("Não precisa gastar zero", 64, NAVY), anim="stamp")
    if t > 69.9:
        k = ease_out(prog(t, 69.9, 0.9))
        c.save(); c.translate(330, 600)
        donut(c, 1.0, 170, 70, GOLD)
        donut(c, 0.8 * k, 170, 70, GREEN)
        text(c, "80/20", 0, 4, 64, MARKER, INK)
        c.restore()
    show(c, t, 70.5, 720, 520, group(lambda c: (rrect(c, -22, -22, 44, 44, 8), fs(c, GREEN, 5)),
                                     at(40, 0, L_("80% investe", 50))), anim="left")
    show(c, t, 71.4, 720, 640, group(lambda c: (rrect(c, -22, -22, 44, 44, 8), fs(c, GOLD, 5)),
                                     at(40, 0, L_("20% curte", 50))), anim="left")
    show(c, t, 71.8, 900, 760, sc(gift, RED, GOLD, s=0.6), anim="pop")
    show(c, t, 72.7, CX, 900, T("ainda chega a", 54), anim="up")
    show(c, t, 73.8, CX, 1010, H("R$ 146 MIL", 96, LGREEN, GREEN), anim="stamp")
    other(c, t, 160, FY, 0.42, [(0, "relax"), (73.8, "arms_up")], [(0, "happy"), (73.8, "grin")], look=1, **ANA)
    hero(c, t, 900, FY, 0.42, [(0, "present_l"), (73.8, "thumb")], [(0, "neutral"), (73.8, "grin")], look=-1)


def s11(c, t):  # 75.4 - fim  em qual porta você tá? comenta; segue pra mais
    floor(c)
    show(c, t, 75.45, CX, 250, M("Em qual porta você tá?", 66, NAVY), anim="stamp", t1=79.1)
    for i, t0 in enumerate((76.0, 76.15, 76.3)):
        show(c, t, t0, 200 + i * 320, 540, porta(i + 1, DOOR_COLS[i + 1], t, s=0.6), anim="pop", d=0.3, t1=79.1)
    show(c, t, 76.9, CX, 830, H("COMENTA 1, 2 OU 3", 78, LYELLOW), anim="stamp", t1=79.1)
    # final: SEGUE PRA MAIS com O Consultor apontando pra cima
    show(c, t, 79.15, CX, 330, H("SEGUE PRA MAIS", 100, LYELLOW), anim="stamp")
    show(c, t, 79.9, CX, 470, T("essa semana tem mais", 54), anim="up")
    if t > 79.3:
        arrow_draw(c, t, 79.3, 760, 860, 760, 580, col=NAVY, lw=11)
    hero(c, t, 560, FY, 0.55,
         [(0, "present"), (76.9, "finger_up"), (79.15, "point_ru")],
         [(0, "think"), (76.9, "happy"), (79.15, "grin")], look=0.5)


SCENES = [
    (0.0, 9.1, s01), (9.1, 17.0, s02), (17.0, 21.1, s03), (21.1, 30.3, s04), (30.3, 38.9, s05),
    (38.9, 42.9, s06), (42.9, 50.7, s07), (50.7, 55.4, s08), (55.4, 68.1, s09), (68.1, 75.4, s10),
    (75.4, 999.0, s11),
]
