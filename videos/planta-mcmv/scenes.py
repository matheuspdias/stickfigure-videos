"""Tudo que ninguém te conta antes de financiar na planta (MCMV). Só TikTok: vertical nativo 1080x1920, 152,3 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout como o de reserva-emergencia: coordenadas desenhadas com pés em y=1230 e deslocadas +60 (SHIFT).
Contas em contas.py: imóvel R$ 250 mil, renda R$ 4 mil, Caixa R$ 160 mil (SAC, 35 anos, 6% a.a.),
FGTS + subsídio R$ 54 mil, entrada 36 x R$ 1.000 corrigida pelo INCC, evolução de obra até ~R$ 850."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
LORANGE = (1.0, 0.86, 0.70)

SFX = [(7.5, "tum"), (75.4, "tum"), (91.5, "tum"), (145.6, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- contas (mesmas de contas.py)
FIN, I_M, SEG, N_OBRA = 160_000, 0.06 / 12, 50, 36
INCC_M = 1.066 ** (1 / 12) - 1


def lib(m):
    x = m / N_OBRA
    return 0.10 + 0.90 * (3 * x ** 2 - 2 * x ** 3)


def evol(m):
    return FIN * lib(m) * I_M + SEG * lib(m)


def entr(m):
    return 1000 * (1 + INCC_M) ** (m - 1)


MESES = list(range(3, 37, 3))       # 12 barras: mês 3, 6, ..., 36
PX = 0.3                            # px por real
BASE = 1080
BX0, BSTEP, BW = 165, 64, 48


# ---------------------------------------------------------------- helpers
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def stamp_txt(s, col=RED, size=78):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.08)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def obra(k):
    """prédio em construção: andares crescem com k (0..1) e grua ao lado"""
    def f(c):
        n = max(1, min(6, 1 + int(k * 5.99)))
        c.save(); c.translate(150, 0); crane(c); c.restore()
        apartment(c, LYELLOW, None, n)
    return f


def dashed(c, x1, y, x2, col=NAVY, w=7):
    c.save(); c.set_dash([20, 12]); line(c, x1, y, x2, y, w, col); c.restore()


def chart(c, t, t_ev, t_en=None, upto=None):
    """barras da evolução de obra (vermelho); com t_en, a parcela da entrada (laranja) empilhada em cima"""
    line(c, BX0 - 40, BASE, BX0 + BSTEP * 11 + 40, BASE, 6)
    text(c, "mês 1", BX0, BASE + 40, 40, HAND, DGRAY)
    text(c, "mês 36", BX0 + BSTEP * 11, BASE + 40, 40, HAND, DGRAY)
    for i, m in enumerate(MESES):
        x = BX0 + i * BSTEP
        t0 = t_ev + i * (upto or 0.33)
        if t < t0:
            continue
        k = ease_out(prog(t, t0, 0.35))
        he = evol(m) * PX * k
        rrect(c, x - BW / 2, BASE - he, BW, he, 6); fs(c, RED, 4)
        if t_en is not None and t > t_en + i * 0.12:
            k2 = ease_out(prog(t, t_en + i * 0.12, 0.35))
            hn = entr(m) * PX * k2
            rrect(c, x - BW / 2, BASE - he - hn, BW, hn, 6); fs(c, ORANGE, 4)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.7  gancho
    floor(c)
    show(c, t, 0.0, CX, 260, lambda c: hl(c, "NA PLANTA?", 0, 0, 110, LYELLOW), anim="stamp", d=0.35)
    show(c, t, 0.15, 250, FY, obra(0.55), anim="pop")
    show(c, t, 2.5, 690, 520, sc(boleto, "???", RED, None, s=0.95), anim="drop")
    show(c, t, 3.6, 690, 720, T("ninguém te conta", 52, RED), anim="up")
    # comparação do pior mês
    if t > 5.2:
        show(c, t, 5.2, CX, 760, lambda c: rrect(c, -440, -370, 880, 760, 30) or fs(c, PAPER, 6), anim="pop", d=0.3)
        show(c, t, 5.6, 330, 1040, lambda c: bar(c, 1230 * 0.24 * ease_out(prog(t, 5.6, 0.5)), 200, NAVY,
                                                  "financiamento", "R$ 1.230", 48), anim="fade", d=0.1)
        show(c, t, 7.3, 710, 1040, lambda c: bar(c, 2050 * 0.24 * ease_out(prog(t, 7.3, 0.5)), 200, RED,
                                                  "fim da obra", "R$ 2 .050", 56), anim="fade", d=0.1)
        show(c, t, 5.4, CX, 450, M("por mês", 60, NAVY), anim="up")
    hero(c, t, 900, FY, 0.6, [(0, "point_l"), (5.2, "relax"), (7.6, "head")],
         [(0, "think"), (5.2, "neutral"), (7.6, "shocked")], appear=0.0, look=-1)


def s02(c, t):  # 9.7 - 23.3  o caminho (linha do tempo)
    floor(c)
    show(c, t, 9.9, CX, 250, lambda c: ribbon(c, "O CAMINHO", NAVY, 64), anim="stamp")
    steps = [(11.5, "simulação e aprovação", lambda c: calculator(c, "OK")),
             (14.1, "assinatura", lambda c: document(c, "CONTRATO", NAVY, 24)),
             (15.6, "obra: 2 a 3 anos", lambda c: c.save() or c.scale(0.45, 0.45) or c.translate(-60, 230) or obra(0.6)(c) or c.restore()),
             (18.5, "entrega das chaves", lambda c: c.save() or c.scale(0.8, 0.8) or house_key(c) or c.restore()),
             (20.9, "financiamento de verdade", bank)]
    y0, dy, xl = 410, 180, 130
    if t > 11.4:
        k = clamp01((t - 11.4) / 10.0)
        line(c, xl, y0, xl, y0 + dy * 4 * ease_io(k), 8, LGRAY)
    for i, (t0, lab, ic) in enumerate(steps):
        y = y0 + i * dy
        if t < t0:
            continue
        active = (i == len(steps) - 1) or t < steps[i + 1][0]
        show(c, t, t0, xl, y, lambda c, a=active: circle(c, 0, 0, 30, GOLD if a else NAVY, 6), anim="pop", d=0.3)
        show(c, t, t0 + 0.1, xl + 120, y, sc(ic, s=0.6), anim="pop")
        col = INK if active else DGRAY
        show(c, t, t0 + 0.2, xl + 200, y, L(lab, 42 if active else 48, col, MARKER if active else HAND), anim="left", d=0.3)
    show(c, t, 21.8, 640, y0 + dy * 4 + 70, lambda c: hl(c, "só aqui começa", 0, 0, 44, LGREEN), anim="stamp")


def s03(c, t):  # 23.3 - 40.2  a entrada
    floor(c)
    show(c, t, 23.5, CX, 250, lambda c: ribbon(c, "A ENTRADA", NAVY, 64), anim="stamp")
    show(c, t, 26.8, 180, 470, group(sc(piggy, GOLD, s=0.75), at(0, 115, M("FGTS", 50, GREEN))), anim="pop")
    show(c, t, 28.0, 430, 470, group(sc(gift, GREEN, GOLD, s=0.75), at(0, 115, M("subsídio", 50, GREEN))), anim="pop")
    show(c, t, 29.2, 430, 630, T("conforme a faixa", 44, DGRAY), anim="up")
    show(c, t, 31.0, CX, 740, T("o que sobra: parcelado com a construtora", 50), anim="up")
    if t > 32.3:
        for i in range(6):
            x = 170 + i * 120
            t0 = 32.3 + i * 0.12
            grow = 1.0 + (0.22 * i / 5 if t > 38.8 else 0)
            show(c, t, t0, x, 960, lambda c, g=grow, i=i: (c.save(), c.translate(0, 0), c.scale(0.6, 0.6 * g),
                                                         calendar(c, f"{i + 1}x", ORANGE, 52), c.restore()), anim="pop")
    show(c, t, 34.9, 780, 470, stamp_txt("INCC", RED, 80), anim="stamp")
    show(c, t, 37.0, 780, 600, T("inflação da construção", 40, RED), anim="up")
    if t > 38.8:
        arrow_draw(c, t, 38.8, 160, 1080, 860, 860)
        show(c, t, 39.0, 860, 800, M("sobe todo mês", 50, RED), anim="pop")
    hero(c, t, 920, FY, 0.5, [(0, "present_l"), (34.9, "point_lu")], [(0, "neutral"), (34.9, "worried")], look=-1)


def s04(c, t):  # 40.2 - 55.6  o exemplo
    floor(c)
    show(c, t, 40.4, CX, 250, lambda c: ribbon(c, "UM EXEMPLO", NAVY, 60), anim="stamp")
    show(c, t, 41.5, 230, 790, sc(apartment, LYELLOW, None, 4, s=0.8), anim="pop")
    show(c, t, 42.2, 240, 410, lambda c: price_tag(c, "R$ 250 mil", YELLOW, 54), anim="stamp")
    show(c, t, 43.9, 720, 410, lambda c: hl(c, "renda: R$ 4 mil", 0, 0, 54, LGREEN), anim="stamp")
    # barra empilhada dos 250 mil
    x0, w, y, h = 100, 840, 860, 90
    segs = [(45.4, 160, BLUE, "Caixa financia", "R$ 160 mil"),
            (47.9, 54, GREEN, "FGTS + subsídio", "R$ 54 mil"),
            (51.5, 36, ORANGE, "construtora", "R$ 36 mil")]
    xc = x0
    for i, (t0, v, col, lab, val) in enumerate(segs):
        sw = w * v / 250
        if t > t0:
            k = ease_out(prog(t, t0, 0.5))
            rrect(c, xc, y, sw * k, h, 8); fs(c, col, 5)
            show(c, t, t0 + 0.2, 140, 1010 + i * 70, lambda c, col=col: (rrect(c, -18, -18, 36, 36, 6), fs(c, col, 4)), anim="pop")
            show(c, t, t0 + 0.2, 180, 1010 + i * 70, L(lab, 46), anim="left", d=0.3)
            show(c, t, t0 + 0.3, 800, 1010 + i * 70, lambda c, val=val: text(c, val, 0, 0, 50, MARKER, INK, align="r"), anim="pop")
        xc += sw
    show(c, t, 52.9, 640, 640, lambda c: hl(c, "36x de R$ 1.000", 0, 0, 62, LORANGE), anim="stamp")


def s05(c, t):  # 55.6 - 68.6  a surpresa: evolução de obra
    floor(c)
    show(c, t, 55.8, CX, 250, M("a surpresa:", 64, DGRAY), anim="up")
    show(c, t, 57.6, CX, 360, lambda c: hl(c, "EVOLUÇÃO DE OBRA", 0, 0, 80, PINKISH), anim="stamp")
    k = clamp01((t - 59.4) / 4.0)
    show(c, t, 59.4, 640, 1000, lambda c: obra(k)(c), anim="pop")
    show(c, t, 61.0, 200, 640, group(sc(bank, s=0.7), at(0, 100, M("Caixa", 44, NAVY))), anim="pop")
    if t > 61.6:
        for i in range(3):
            tt = (t - 61.6 - i * 0.6) % 1.8
            if t > 61.6 + i * 0.6:
                xx = 280 + 280 * ease_io(clamp01(tt / 1.4))
                c.save(); c.translate(xx, 600 - 40 * math.sin(math.pi * clamp01(tt / 1.4))); c.scale(0.4, 0.4); bill(c); c.restore()
    show(c, t, 63.6, CX, 1130, lambda c: hl(c, "juros sobre o que já foi liberado", 0, 0, 46, LYELLOW), anim="stamp")
    show(c, t, 66.7, 250, 900, group(M("abate a dívida", 46, DGRAY), at(0, 0, lambda c: line(c, -170, 10, 170, -10, 9, RED))), anim="pop")
    hero(c, t, 930, FY, 0.48, [(0, "relax"), (57.6, "head"), (63.6, "point_l")], [(0, "neutral"), (57.6, "shocked"), (63.6, "worried")], look=-1)


def s06(c, t):  # 68.6 - 82.2  sobe a cada etapa até ~R$ 850
    floor(c)
    show(c, t, 68.8, CX, 250, M("evolução de obra", 66, RED), anim="up")
    chart(c, t, 70.0, upto=0.42)
    show(c, t, 70.4, BX0 + 40, BASE - 90, L("< R$ 100", 44, RED, MARKER), anim="pop", t1=74.3)
    xl = BX0 + 11 * BSTEP
    show(c, t, 75.4, xl - 80, BASE - 850 * PX - 50, M("R$ 850", 60, RED), anim="stamp")
    if t > 78.0:
        k = ease_out(prog(t, 78.0, 0.5))
        dashed(c, BX0 - 40, BASE - 1230 * PX, BX0 - 40 + (11 * BSTEP + 80) * k)
        show(c, t, 79.4, 450, BASE - 1230 * PX - 50, L("parcela oficial ~R$ 1.230", 44, NAVY, MARKER), anim="pop")
    show(c, t, 77.9, 330, 470, lambda c: hl(c, "= 70% da parcela", 0, 0, 52, LYELLOW), anim="stamp")
    hero(c, t, 950, FY, 0.45, [(0, "point_l"), (75.4, "head")], [(0, "neutral"), (75.4, "worried")], look=-1)


def s07(c, t):  # 82.2 - 96.9  a dupla parcela
    floor(c)
    show(c, t, 82.4, CX, 250, lambda c: hl(c, "É AQUI QUE APERTA", 0, 0, 74, PINKISH), anim="stamp")
    chart(c, t, -10, t_en=84.1)
    dashed(c, BX0 - 40, BASE - 1230 * PX, BX0 + 11 * BSTEP + 40)
    if t > 84.2:
        dashed(c, 130, 450, 180, NAVY, 6)
    show(c, t, 84.2, 200, 450, L("parcela do financiamento", 42), anim="left")
    show(c, t, 84.2, 150, 370, lambda c: (rrect(c, -18, -18, 36, 36, 6), fs(c, ORANGE, 4)), anim="pop")
    show(c, t, 84.2, 190, 370, L("entrada (INCC)", 42), anim="left")
    show(c, t, 84.2, 550, 370, lambda c: (rrect(c, -18, -18, 36, 36, 6), fs(c, RED, 4)), anim="pop")
    show(c, t, 84.2, 590, 370, L("evolução", 42), anim="left")
    xl = BX0 + 11 * BSTEP
    show(c, t, 88.5, xl - 170, BASE - 850 * PX - 120, M("~R$ 1.200", 44, ORANGE), anim="pop", t1=90.8)
    show(c, t, 91.0, xl - 120, BASE - 2055 * PX - 45, M("R$ 2 .050", 58, RED), anim="stamp")
    show(c, t, 95.7, 450, 620, lambda c: hl(c, "METADE DA RENDA", 0, 0, 66, PINKISH, RED), anim="stamp")
    hero(c, t, 960, FY, 0.42, [(0, "head"), (91.0, "shrug")], [(0, "worried"), (91.0, "desperate")], look=-1)


def s08(c, t):  # 96.9 - 111.6  e se atrasar?
    floor(c)
    show(c, t, 97.0, CX, 250, M("E se a obra atrasar?", 70, NAVY), anim="up")
    show(c, t, 97.3, 230, 500, sc(calendar, "!", RED, 90, s=1.2), anim="pop")
    show(c, t, 98.6, 520, 520, sc(boleto, "OBRA", RED, None, s=0.85), anim="drop")
    show(c, t, 99.6, 520, 680, T("pode continuar vindo", 44, RED), anim="up")
    show(c, t, 103.3, 800, 510, group(sc(gavel, s=0.75), at(0, 160, M("STJ", 56, NAVY))), anim="pop")
    show(c, t, 105.4, CX, 820, lambda c: hl(c, "depois do prazo + tolerância", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, 108.6, CX, 950, stamp_txt("NÃO PODE", GREEN, 80), anim="stamp")
    show(c, t, 110.3, 230, 1070, sc(document, "ATRASO", RED, 26, s=1.1), anim="pop")
    hero(c, t, 880, FY, 0.48, [(0, "think"), (103.3, "point_lu"), (110.3, "present_l")],
         [(0, "think"), (103.3, "confident")], prop=None, look=-1)


def s09(c, t):  # 111.6 - 124.5  depois das chaves
    floor(c)
    show(c, t, 111.8, 260, 330, sc(house_key, s=0.9), anim="pop")
    show(c, t, 112.2, 640, 330, M("depois das chaves", 56, NAVY), anim="up")
    show(c, t, 113.4, 520, 440, group(M("evolução de obra", 48, DGRAY), at(0, 0, lambda c: line(c, -210, 12, 210, -12, 9, RED))), anim="pop")
    show(c, t, 114.4, 520, 520, M("começa o financiamento", 50, GREEN), anim="up")
    # SAC: parcela cai
    if t > 116.5:
        vals = [1231, 1100, 960, 820, 690, 560, 433]
        for i, v in enumerate(vals):
            t0 = 116.6 + i * 0.25
            if t > t0:
                k = ease_out(prog(t, t0, 0.35))
                x = 120 + i * 60
                h = v * 0.22 * k
                rrect(c, x - 22, 900 - h, 44, h, 6); fs(c, NAVY, 4)
        show(c, t, 117.0, 160, 600, L("SAC", 50, NAVY, MARKER), anim="pop")
        show(c, t, 118.5, 340, 940, T("cai com o tempo", 42), anim="up")
    items = [(120.8, "condomínio", lambda c: apartment(c, LBLUE, None, 2)),
             (121.8, "IPTU", lambda c: boleto(c, "IPTU", RED, None)),
             (122.8, "mudança", moving_box),
             (123.8, "móveis", lambda c: (sofa_back(c), sofa_front(c)))]
    for i, (t0, lab, ic) in enumerate(items):
        x, y = 650 + (i % 2) * 200, 690 + (i // 2) * 270
        show(c, t, t0, x, y, group(sc(ic, s=0.5), at(0, 115, T(lab, 44))), anim="drop")
    hero(c, t, 150, FY, 0.42, [(0, "relax"), (120.8, "shrug")], [(0, "happy"), (120.8, "worried")], look=1)


def s10(c, t):  # 124.5 - 135.7  ITBI, registro, seguros
    floor(c)
    show(c, t, 124.7, CX, 250, M("Tem mais:", 70, NAVY), anim="up")
    show(c, t, 125.6, 250, 540, sc(boleto, "ITBI", RED, None, s=0.95), anim="drop")
    show(c, t, 126.6, 760, 540, sc(document, "REGISTRO", NAVY, 22, s=1.4), anim="drop")
    show(c, t, 129.1, 760, 760, lambda c: hl(c, "desconto no MCMV", 0, 0, 40, LGREEN), anim="stamp")
    show(c, t, 130.4, 250, 760, lambda c: hl(c, "algumas cidades:", 0, 0, 38, LGREEN), anim="stamp")
    show(c, t, 130.9, 250, 830, T("desconto ou isenção", 42, GREEN), anim="up")
    show(c, t, 132.6, 150, 1030, group(sc(shield, NAVY, s=0.7)), anim="pop")
    show(c, t, 132.6, 230, 1030, L("seguros e taxas na parcela", 50), anim="left")
    hero(c, t, 930, FY, 0.42, [(0, "present_l")], [(0, "neutral")], look=-1)


def s11(c, t):  # 135.7 - 147.4  checklist
    floor(c)
    show(c, t, 135.9, CX, 250, lambda c: ribbon(c, "ANTES DE ASSINAR", NAVY, 58), anim="stamp")
    items = [(137.1, "simule a evolução mês a mês"),
             (140.6, "entrada + evolução no pior mês"),
             (143.7, "reserva pro período da obra"),
             (145.6, "leia a cláusula de atraso")]
    for i, (t0, s) in enumerate(items):
        y = 420 + i * 150
        show(c, t, t0, 140, y, lambda c: (rrect(c, -34, -34, 68, 68, 10), fs(c, WHITE, 6)), anim="pop")
        show(c, t, t0 + 0.6, 140, y, sc(check_icon, s=0.6), anim="stamp")
        show(c, t, t0, 200, y, L(s, 52), anim="left", d=0.3)
    hero(c, t, CX, FY, 0.55, [(0, "present"), (145.6, "thumb")], [(0, "confident"), (145.6, "grin")],
         prop=("l", prop_pointer), look=0)


def s12(c, t):  # 147.4 - fim  pergunta final
    floor(c)
    show(c, t, 147.6, CX, 280, M("Comprou na planta?", 80, NAVY), anim="stamp")
    show(c, t, 149.0, CX, 420, T("a evolução de obra", 62), anim="up")
    show(c, t, 149.6, CX, 500, T("te pegou de surpresa?", 62), anim="up")
    show(c, t, 150.0, 250, FY, obra(1.0), anim="pop")
    show(c, t, 151.4, 690, 700, group(lambda c: speech(c, 460, 130, -140, 110), T("Comenta aí!", 62)), anim="pop")
    hero(c, t, 720, FY, 0.7, [(0, "point_l"), (151.4, "wave")], [(0, "happy"), (151.4, "grin")], look=-0.5)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 9.7, s01), (9.7, 23.3, s02), (23.3, 40.2, s03), (40.2, 55.6, s04), (55.6, 68.6, s05),
    (68.6, 82.2, s06), (82.2, 96.9, s07), (96.9, 111.6, s08), (111.6, 124.5, s09), (124.5, 135.7, s10),
    (135.7, 147.4, s11), (147.4, 999.0, s12),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
