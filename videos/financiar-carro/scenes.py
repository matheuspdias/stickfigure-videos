"""O que ninguém te conta antes de financiar um carro (série ep. 2). Só TikTok: vertical nativo 1080x1920, 153,3 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout igual ao de planta-mcmv: coordenadas desenhadas com pés em y=1230 e deslocadas +60 (SHIFT).
Contas em contas.py: carro R$ 60 mil, 20% de entrada, R$ 48 mil a 1,973% a.m. (taxa média BCB ago/2026, 26,42% a.a.)."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
LORANGE = (1.0, 0.86, 0.70)

SFX = [(43.0, "tum"), (59.7, "tum"), (84.6, "tum"), (144.3, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- contas (mesmas de contas.py)
CARRO = 60_000
I_M = 1.2642 ** (1 / 12) - 1


def pmt(pv, n):
    return pv * I_M / (1 - (1 + I_M) ** -n)


def saldo(pv, n, k):
    p = pmt(pv, n)
    return pv * (1 + I_M) ** k - p * ((1 + I_M) ** k - 1) / I_M


def valor_carro(m):
    a = m / 12
    return CARRO * (1 - 0.15 * a) if a <= 1 else CARRO * 0.85 * 0.9 ** (a - 1)


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


def strike(fn, w=200):
    return group(fn, lambda c: line(c, -w, 14, w, -14, 10, RED))


def block(lab, col, w=520, h=86, size=44):
    def f(c):
        rrect(c, -w / 2, -h / 2, w, h, 12); fs(c, col, 5)
        text(c, lab, 0, 0, size, MARKER, INK)
    return f


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.3  gancho
    floor(c)
    show(c, t, 0.0, CX, 250, lambda c: hl(c, "VAI FINANCIAR", 0, 0, 96, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 0.0, CX, 380, lambda c: hl(c, "UM CARRO?", 0, 0, 96, LYELLOW, rot=0.015), anim="stamp", d=0.3)
    show(c, t, 0.1, 330, 700, sc(car, BLUE, s=1.5), anim="pop")
    show(c, t, 1.9, 330, 520, sc(bank, s=0.55), anim="drop", t1=3.4)
    show(c, t, 2.6, 760, 660, group(sc(boleto, "PARCELA", NAVY, "R$ ...", s=0.9)), anim="drop")
    show(c, t, 2.9, 760, 850, T("o banco te mostra", 44, NAVY), anim="up")
    if t > 3.5:
        for i, (lab, x, y) in enumerate([("IOF", 200, 960), ("JUROS", 450, 1010), ("IPVA", 700, 960), ("SEGURO", 300, 1130)]):
            show(c, t, 3.5 + i * 0.25, x, y, lambda c, lab=lab: hl(c, lab, 0, 0, 46, PINKISH), anim="drop")
        show(c, t, 4.3, 650, 1140, M("o resto?", 64, RED), anim="stamp")
    hero(c, t, 920, FY, 0.5, [(0, "point_l"), (3.6, "head")], [(0, "think"), (3.6, "shocked")], look=-1)


def s02(c, t):  # 5.3 - 24.4  taxa x CET
    floor(c)
    show(c, t, 5.5, CX, 240, lambda c: ribbon(c, "TAXA X CET", NAVY, 64), anim="stamp")
    show(c, t, 6.4, 370, 1090, block("taxa do anúncio", LBLUE, 520, 96, 50), anim="pop")
    show(c, t, 6.6, 120, 1090, sc(percent, s=0.5), anim="pop")
    show(c, t, 7.6, 750, 420, stamp_txt("NÃO É O QUE", RED, 50), anim="stamp", t1=9.0)
    show(c, t, 7.9, 750, 510, stamp_txt("VOCÊ PAGA", RED, 50), anim="stamp", t1=9.0)
    pile = [(10.4, "+ IOF", PINKISH), (11.4, "+ tarifa de cadastro", LORANGE),
            (13.0, "+ registro do contrato", LYELLOW), (15.6, "+ seguros embutidos", PINKISH)]
    for i, (t0, lab, col) in enumerate(pile):
        show(c, t, t0, 370, 990 - i * 100, block(lab, col, 520, 86, 42), anim="drop")
    if t > 17.7:
        k = ease_out(prog(t, 17.7, 0.4))
        x = 660
        line(c, x, 1135, x + 30 * k, 1135, 7); line(c, x + 30 * k, 1135, x + 30 * k, 645, 7); line(c, x, 645, x + 30 * k, 645, 7)
        show(c, t, 18.1, 820, 860, lambda c: hl(c, "= CET", 0, 0, 84, LGREEN), anim="stamp")
        show(c, t, 19.1, 830, 980, T("Custo Efetivo", 42), anim="up")
        show(c, t, 19.5, 830, 1035, T("Total", 42), anim="up")
    show(c, t, 20.8, 760, 430, group(sc(check_icon, s=0.6), at(70, 0, L("compare", 50, GREEN, MARKER))), anim="pop")
    show(c, t, 21.3, 830, 510, M("pelo CET", 50, GREEN), anim="up")
    show(c, t, 22.96, 370, 1090, lambda c: line(c, -270, 18, 270, -18, 11, RED), anim="pop")
    hero(c, t, 940, FY, 0.42, [(0, "present_l"), (7.6, "head"), (9.6, "point_l"), (20.8, "thumb")],
         [(0, "neutral"), (7.6, "shocked"), (9.6, "worried"), (20.8, "confident")], look=-1)


def s03(c, t):  # 24.4 - 39.5  o exemplo
    floor(c)
    show(c, t, 24.6, CX, 240, lambda c: ribbon(c, "UM EXEMPLO", NAVY, 60), anim="stamp")
    show(c, t, 25.5, 260, 520, sc(car, BLUE, s=1.15), anim="pop")
    show(c, t, 26.0, 700, 470, lambda c: price_tag(c, "R$ 60 mil", YELLOW, 60), anim="stamp")
    rows = [(27.1, "entrada (20%)", "R$ 12 mil", GREEN),
            (29.0, "financia", "R$ 48 mil", NAVY),
            (30.9, "prazo", "48x", NAVY),
            (32.5, "taxa média BC", "~26% a.a.", RED)]
    for i, (t0, lab, val, col) in enumerate(rows):
        y = 700 + i * 95
        show(c, t, t0, 110, y, L(lab, 48), anim="left", d=0.3)
        show(c, t, t0 + 0.2, 780, y, lambda c, v=val, col=col: text(c, v, 0, 0, 54, MARKER, col, align="r"), anim="pop")
    if t > 32.6:
        show(c, t, 32.6, 700, 1040, T("(~2% ao mês)", 38, DGRAY), anim="up")
    show(c, t, 36.6, 430, 1140, lambda c: hl(c, "parcela: R$ 1.560", 0, 0, 66, LYELLOW), anim="stamp")
    hero(c, t, 940, FY, 0.42, [(0, "present_l"), (36.6, "point_l")], [(0, "neutral"), (36.6, "happy")],
         prop=("r", prop_calculator), look=-1)


def s04(c, t):  # 39.5 - 49.6  o total pago
    floor(c)
    show(c, t, 39.7, CX, 250, M("No fim, você pagou:", 62, NAVY), anim="up")
    show(c, t, 41.0, CX, 400, lambda c: hl(c, "R$ 74.700", 0, 0, 130, LYELLOW), anim="stamp")
    base, px, x1, x2, bw = 1030, 0.0068, 280, 640, 220
    if t > 41.4:
        k = ease_out(prog(t, 41.4, 0.5))
        rrect(c, x1 - bw / 2, base - 48000 * px * k, bw, 48000 * px * k, 10); fs(c, NAVY, 6)
        show(c, t, 41.6, x1, base + 50, T("você pegou", 44), anim="up")
        show(c, t, 41.7, x1, base - 48000 * px / 2, M("48 mil", 54, WHITE), anim="pop")
        rrect(c, x2 - bw / 2, base - 48000 * px * k, bw, 48000 * px * k, 10); fs(c, NAVY, 6)
        show(c, t, 41.6, x2, base + 50, T("você pagou", 44), anim="up")
    if t > 43.0:
        k = ease_out(prog(t, 43.0, 0.6))
        h0, h = 48000 * px, 26700 * px * k
        rrect(c, x2 - bw / 2, base - h0 - h, bw, h, 10); fs(c, RED, 6)
        show(c, t, 43.3, x2, base - h0 - 26700 * px / 2, M("26.700", 52, WHITE), anim="pop")
        show(c, t, 44.6, 870, base - h0 - 140, M("só de", 50, RED), anim="pop")
        show(c, t, 44.9, 870, base - h0 - 70, M("juros", 64, RED), anim="pop")
    show(c, t, 46.5, 470, 1165, lambda c: hl(c, "+ IOF: ~R$ 1.500", 0, 0, 56, PINKISH), anim="stamp")
    hero(c, t, 950, FY, 0.4, [(0, "relax"), (41.0, "head")], [(0, "neutral"), (41.0, "shocked")], look=-1)


def s05(c, t):  # 49.6 - 65.6  seguro "obrigatório"
    floor(c)
    show(c, t, 49.8, 230, 470, sc(document, "CONTRATO", NAVY, 24, s=1.25), anim="drop")
    show(c, t, 50.2, 260, 650, T("na hora de assinar", 44), anim="up")
    show(c, t, 51.8, 640, 440, sc(shield, NAVY, s=1.0), anim="pop")
    show(c, t, 52.0, 690, 580, M("seguro prestamista", 50, NAVY), anim="up")
    show(c, t, 53.2, 690, 650, T("quita a dívida se acontecer", 40, DGRAY), anim="up")
    show(c, t, 53.5, 690, 700, T("algo com você", 40, DGRAY), anim="up")
    for i in range(3):
        show(c, t, 56.6 + i * 0.25, 110 + i * 110, 830, sc(gift, PURPLE, GOLD, s=0.45), anim="drop")
    show(c, t, 57.0, 680, 820, M("+ outros produtos", 46, PURPLE), anim="up")
    show(c, t, 58.2, CX, 260, stamp_txt("OBRIGATÓRIO?", RED, 66), anim="stamp", t1=59.5)
    show(c, t, 59.64, CX, 260, stamp_txt("NÃO É!", GREEN, 80), anim="stamp")
    show(c, t, 60.3, 170, 1010, sc(gavel, s=0.55), anim="pop")
    show(c, t, 60.5, 270, 980, L("venda casada", 54, INK, MARKER), anim="left")
    show(c, t, 61.4, 270, 1050, L("é proibida", 54, RED, MARKER), anim="left")
    show(c, t, 62.6, 150, 1160, sc(check_icon, s=0.5), anim="stamp")
    show(c, t, 62.8, 200, 1160, L("pode recusar", 46), anim="left")
    show(c, t, 63.8, 520, 1160, sc(check_icon, s=0.5), anim="stamp")
    show(c, t, 64.0, 570, 1160, L("outra seguradora", 46), anim="left")
    hero(c, t, 940, FY - 20, 0.38, [(0, "think"), (59.6, "finger_up")], [(0, "think"), (59.6, "confident")], look=-1)


def s06(c, t):  # 65.6 - 77.0  desvalorização
    floor(c)
    show(c, t, 65.8, CX, 250, lambda c: ribbon(c, "DESVALORIZAÇÃO", RED, 60), anim="stamp")
    show(c, t, 68.1, 300, 560, sc(car, BLUE, s=1.2), anim="pop")
    if t > 68.6:
        arrow_draw(c, t, 68.6, 560, 420, 640, 640, col=RED)
    show(c, t, 69.6, 800, 520, M("-10% a -20%", 60, RED), anim="stamp")
    show(c, t, 71.0, 800, 600, T("no primeiro ano", 44, RED), anim="up")
    show(c, t, 72.0, 300, 820, lambda c: hl(c, "20% de entrada", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, 73.6, 720, 820, stamp_txt("NO AZUL", GREEN, 58), anim="stamp")
    show(c, t, 74.9, 300, 1000, lambda c: hl(c, "pouca entrada", 0, 0, 52, PINKISH), anim="stamp")
    show(c, t, 76.0, 680, 1000, lambda c: hl(c, "+ prazo longo", 0, 0, 52, PINKISH), anim="stamp")
    show(c, t, 76.5, CX, 1130, M("?", 70, RED), anim="pop")
    hero(c, t, 940, FY, 0.38, [(0, "present_l"), (73.6, "thumb"), (74.9, "think")],
         [(0, "neutral"), (73.6, "happy"), (74.9, "worried")], look=-1)


# gráfico valor do carro x dívida (sem entrada, 60x), meses 0 a 48
GX0, GX1, GY0, GY1 = 140, 900, 960, 540
VMIN, VMAX = 30_000, 61_000


def gx(m):
    return GX0 + (GX1 - GX0) * m / 36


def gy(v):
    return GY0 - (GY0 - GY1) * (v - VMIN) / (VMAX - VMIN)


def s07(c, t):  # 77.0 - 93.6  as duas linhas se cruzam
    floor(c)
    show(c, t, 77.2, CX, 250, M("sem entrada, em 60x", 62, NAVY), anim="up")
    line(c, GX0, GY0, GX1 + 20, GY0, 6); line(c, GX0, GY0, GX0, GY1 - 40, 6)
    for m, lab in ((0, "hoje"), (12, "1 ano"), (24, "2 anos"), (36, "3 anos")):
        text(c, lab, gx(m), GY0 + 40, 36, HAND, DGRAY)
    kd = ease_io(clamp01((t - 77.4) / 2.0))
    kv = ease_io(clamp01((t - 79.2) / 2.0))
    mmax = 36
    # área de "devendo mais do que vale" (meses 0 a 19)
    if t > 82.7:
        a = 0.35 * ease_out(prog(t, 82.7, 0.6))
        c.move_to(gx(0), gy(saldo(CARRO, 60, 0)))
        for m in range(0, 20):
            c.line_to(gx(m), gy(saldo(CARRO, 60, m)))
        for m in range(19, -1, -1):
            c.line_to(gx(m), gy(valor_carro(m)))
        c.close_path(); rgb(c, RED, a); c.fill()
    for fn, col, k in ((lambda m: saldo(CARRO, 60, m), RED, kd), (valor_carro, BLUE, kv)):
        if k <= 0:
            continue
        c.move_to(gx(0), gy(fn(0)))
        for i in range(1, int(mmax * k) + 1):
            c.line_to(gx(i), gy(fn(i)))
        rgb(c, col); c.set_line_width(9); c.stroke()
    show(c, t, 77.6, 660, gy(saldo(CARRO, 60, 30)) + 40, M("dívida", 50, RED), anim="pop")
    show(c, t, 79.4, 800, gy(valor_carro(33)) - 50, M("carro", 50, BLUE), anim="pop")
    show(c, t, 83.0, gx(19), gy(valor_carro(19)), lambda c: circle(c, 0, 0, 16, GOLD, 5), anim="pop")
    show(c, t, 83.9, 470, 380, lambda c: hl(c, "~1 ano e meio devendo", 0, 0, 48, PINKISH), anim="stamp")
    show(c, t, 85.1, 470, 450, T("mais do que o carro vale", 44, RED), anim="up")
    show(c, t, 86.8, 120, 1080, L("vender?", 48, INK, MARKER), anim="left")
    show(c, t, 88.1, 480, 1080, stamp_txt("NÃO QUITA", RED, 44), anim="stamp")
    show(c, t, 89.5, 120, 1160, L("perda total?", 48, INK, MARKER), anim="left")
    show(c, t, 90.6, 450, 1160, L("seguro paga o carro,", 38, RED), anim="left")
    show(c, t, 92.4, 450, 1210, L("não a dívida", 38, RED), anim="left")
    hero(c, t, 975, FY - 30, 0.32, [(0, "point_l"), (84.6, "head")], [(0, "neutral"), (84.6, "shocked")], look=-1)


def s08(c, t):  # 93.6 - 110.0  o que não está na parcela
    floor(c)
    show(c, t, 93.8, CX, 250, lambda c: ribbon(c, "FORA DA PARCELA", NAVY, 60), anim="stamp")
    items = [(96.0, "seguro", lambda c: shield(c, BLUE)),
             (98.6, "IPVA", lambda c: document(c, "IPVA", RED, 34)),
             (99.5, "licenciamento", lambda c: document(c, "LICENC.", RED, 24)),
             (100.7, "emplacamento", lambda c: document(c, "PLACA", NAVY, 30)),
             (102.6, "manutenção", wrench_tire),
             (103.5, "combustível", gas_pump)]
    for i, (t0, lab, ic) in enumerate(items):
        x, y = 200 + (i % 3) * 300, 480 + (i // 3) * 290
        show(c, t, t0, x, y, group(sc(ic, s=0.75), at(0, 125, T(lab, 40))), anim="drop")
    show(c, t, 104.6, 300, 1020, sc(video_card, "ganho 5 mil, carro 60 mil", None, 760, 300,
                                    lambda c: c.save() or c.scale(0.7, 0.7) or car(c, BLUE) or c.restore(), s=0.6), anim="pop")
    show(c, t, 107.3, 720, 980, lambda c: hl(c, "+ R$ 1.000", 0, 0, 66, PINKISH), anim="stamp")
    show(c, t, 108.2, 720, 1070, T("por mês, além da parcela", 40, RED), anim="up")
    hero(c, t, 960, FY, 0.34, [(0, "present_l"), (107.3, "head")], [(0, "neutral"), (107.3, "worried")], look=-1)


def s09(c, t):  # 110.0 - 136.4  prazo longo: 36x x 60x
    floor(c)
    show(c, t, 110.2, CX, 230, M("a parcela que", 58, NAVY), anim="up")
    show(c, t, 110.6, CX, 310, lambda c: hl(c, "CABE NO BOLSO", 0, 0, 72, LYELLOW), anim="stamp")
    show(c, t, 112.1, 280, 420, T("prazo maior: parcela menor", 42, GREEN), anim="up", t1=115.9)
    show(c, t, 114.4, 760, 420, T("mas o total dispara", 42, RED), anim="up", t1=115.9)
    show(c, t, 112.3, 330, 760, sc(calendar, "36x", NAVY, 56, s=1.2), anim="pop", t1=115.9)
    show(c, t, 112.9, 700, 760, sc(calendar, "72x", RED, 56, s=1.2), anim="pop", t1=115.9)
    if 113.2 < t < 116.2:
        arrow_draw(c, t, 113.2, 440, 760, 590, 760)
    show(c, t, 116.3, CX, 420, M("os mesmos R$ 48 mil", 50, NAVY), anim="up")
    base, px, bw = 1080, 0.0085, 200
    cols = [(270, 118.0, "36x", 120.4, "R$ 1.875", 123.0, 19500, "R$ 19.500"),
            (680, 125.0, "60x", 127.5, "R$ 1.372", 129.6, 34300, "R$ 34.300")]
    for x, t0, lab, tp, parc, tj, jur, jlab in cols:
        show(c, t, t0, x, 540, lambda c, lab=lab: hl(c, lab, 0, 0, 70, LBLUE), anim="stamp")
        show(c, t, tp, x, 640, M(parc, 54, NAVY), anim="pop")
        show(c, t, tp + 0.3, x, 700, T("por mês", 38, DGRAY), anim="up")
        if t > tj:
            k = ease_out(prog(t, tj, 0.6))
            h = jur * px * k
            rrect(c, x - bw / 2, base - h, bw, h, 10); fs(c, RED, 6)
            show(c, t, tj + 0.3, x, base + 45, T("de juros", 40, RED), anim="up")
            show(c, t, tj + 0.3, x, base - jur * px - 40, M(jlab, 50, RED), anim="pop")
        if t > t0:
            line(c, x - bw / 2 - 20, base, x + bw / 2 + 20, base, 6)
    show(c, t, 132.1, 880, 540, M("-R$ 500", 48, GREEN), anim="stamp")
    show(c, t, 134.4, CX, 1190, lambda c: hl(c, "+ R$ 14.800 de juros", 0, 0, 62, PINKISH, RED), anim="stamp")
    hero(c, t, 975, FY, 0.32, [(0, "think"), (134.4, "head")], [(0, "think"), (134.4, "shocked")], look=-1)


def s10(c, t):  # 136.4 - 149.4  checklist
    floor(c)
    show(c, t, 136.6, CX, 250, lambda c: ribbon(c, "ANTES DE ASSINAR", NAVY, 58), anim="stamp")
    items = [(137.9, "peça o CET por escrito"),
             (140.1, "simule em mais de um banco"),
             (142.0, "recuse o que não quer"),
             (144.3, "some parcela + seguro"),
             (146.4, "+ IPVA + manutenção")]
    for i, (t0, s) in enumerate(items):
        y = 410 + i * 130
        if i < 4:
            show(c, t, t0, 140, y, lambda c: (rrect(c, -34, -34, 68, 68, 10), fs(c, WHITE, 6)), anim="pop")
            show(c, t, t0 + 0.6, 140, y, sc(check_icon, s=0.6), anim="stamp")
        show(c, t, t0, 200, y if i < 4 else y - 40, L(s, 52), anim="left", d=0.3)
    hero(c, t, CX, FY, 0.5, [(0, "present"), (144.3, "thumb")], [(0, "confident"), (144.3, "grin")],
         prop=("l", prop_pointer), look=0)


def s11(c, t):  # 149.4 - fim  pergunta final
    floor(c)
    show(c, t, 149.6, CX, 280, M("Já financiou carro?", 78, NAVY), anim="stamp")
    show(c, t, 151.0, CX, 420, T("o que te pegou", 62), anim="up")
    show(c, t, 151.4, CX, 500, T("de surpresa?", 62), anim="up")
    show(c, t, 150.0, 260, FY - 40, sc(car, BLUE, s=1.2), anim="pop")
    show(c, t, 152.6, 690, 720, group(lambda c: speech(c, 460, 130, -140, 110), T("Comenta aí!", 62)), anim="pop")
    hero(c, t, 720, FY, 0.7, [(0, "point_l"), (152.6, "wave")], [(0, "happy"), (152.6, "grin")], look=-0.5)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 5.3, s01), (5.3, 24.4, s02), (24.4, 39.5, s03), (39.5, 49.6, s04), (49.6, 65.6, s05),
    (65.6, 77.0, s06), (77.0, 93.6, s07), (93.6, 110.0, s08), (110.0, 136.4, s09), (136.4, 149.4, s10),
    (149.4, 999.0, s11),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
