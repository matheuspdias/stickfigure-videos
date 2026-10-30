"""O que ninguém te conta antes de entrar num consórcio (série ep. 4). Só TikTok: vertical nativo 1080x1920, 129,3 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout igual ao dos eps. 1 a 3: coordenadas desenhadas com pés em y=1230 e deslocadas +60 (SHIFT).
Contas em contas.py: carta de R$ 50 mil, 60 meses, 15% de administração + 2% de fundo de reserva.
Novo neste episódio: selo da série entre 3 e 5 s (sem narração) e fechamento pedindo para seguir."""
import random

from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)

SFX = [(21.1, "tum"), (37.3, "tum"), (80.6, "tum"), (122.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers (mesmos dos eps. 2 e 3)
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


def block(lab, col, w=520, h=86, size=44, tcol=INK):
    def f(c):
        rrect(c, -w / 2, -h / 2, w, h, 12); fs(c, col, 5)
        text(c, lab, 0, 0, size, MARKER, tcol)
    return f


def pin(c, col=RED):
    """alfinete (a fonte não tem o emoji 📌)"""
    c.save(); c.rotate(0.5)
    line(c, 0, 10, 0, 62, 6, DGRAY)
    rrect(c, -26, -14, 52, 26, 6); fs(c, col, 5)
    rrect(c, -16, -44, 32, 32, 6); fs(c, col, 5)
    rrect(c, -30, -54, 60, 16, 6); fs(c, col, 5)
    c.restore()


def series_card(c):
    """selo da série (3 a 5 s, sem narração)"""
    rrect(c, -470, -110, 940, 220, 30); fs(c, NAVY, 7)
    c.save(); c.translate(-390, -10); c.scale(1.1, 1.1); pin(c); c.restore()
    text(c, "SÉRIE:", -320, -50, 50, MARKER, GOLD, align="l")
    text(c, "O que ninguém te conta", -320, 18, 52, MARKER, WHITE, align="l")
    rrect(c, 230, -78, 210, 70, 14); fs(c, GOLD, 5)
    text(c, "EP. 4", 335, -43, 48, MARKER, NAVY)


def carta(c, val="R$ 50 mil", col=LGREEN, w=420, h=250):
    """carta de crédito"""
    rrect(c, -w / 2, -h / 2, w, h, 18); fs(c, WHITE, 6)
    rrect(c, -w / 2, -h / 2, w, 64, 18); fs(c, col, 6)
    text(c, "CARTA DE CRÉDITO", 0, -h / 2 + 32, 30, MARKER, INK)
    text(c, val, 0, 30, 70, MARKER, NAVY)


def ball(num, col=GOLD):
    def f(c):
        circle(c, 0, 0, 52, col, 6)
        circle(c, 0, 0, 30, WHITE, 0)
        text(c, num, 0, 2, 34, MARKER, INK)
    return f


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.1  gancho
    floor(c)
    show(c, t, 0.0, CX, 250, lambda c: hl(c, "CONSÓRCIO", 0, 0, 100, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 0.0, CX, 390, lambda c: hl(c, "NÃO TEM JUROS?", 0, 0, 80, LYELLOW, rot=0.015), anim="stamp", d=0.3)
    show(c, t, 0.1, 360, 720, carta, anim="pop")
    show(c, t, 0.9, 620, 560, sc(qmark, 140, RED), anim="pop")
    show(c, t, 2.0, 360, 960, stamp_txt("ANTES DE ASSINAR", RED, 56), anim="stamp")
    show(c, t, 3.4, 360, 1090, M("saiba disso", 60, NAVY), anim="up")
    hero(c, t, 900, FY, 0.5, [(0, "think"), (2.0, "finger_up")], [(0, "think"), (2.0, "worried")], look=-1)
    if 3.0 <= t < 5.1:  # selo da série, sem narração
        show(c, t, 3.0, CX, 600, series_card, anim="stamp", d=0.3, t1=5.0)


def s02(c, t):  # 5.1 - 13.1  não tem juros, tem taxa
    floor(c)
    show(c, t, 5.3, 300, 250, M("juros?", 70, DGRAY), anim="pop")
    show(c, t, 5.6, 300, 250, sc(big_x, 80, RED, 16), anim="stamp")
    show(c, t, 6.5, 700, 250, lambda c: hl(c, "TAXA, SIM", 0, 0, 70, PINKISH), anim="stamp")
    rows = [(7.9, "taxa de administração", LBLUE), (9.7, "fundo de reserva", LYELLOW), (11.9, "às vezes, seguro", LGRAY)]
    for i, (t0, lab, col) in enumerate(rows):
        show(c, t, t0, 430, 480 + i * 190, block(lab, col, 700, 130, 52), anim="left", d=0.3)
    show(c, t, 10.5, 430, 1080, M("tudo diluído na parcela", 54, NAVY), anim="up")
    hero(c, t, 940, FY, 0.45, [(0, "shrug"), (6.5, "present_l")], [(0, "neutral"), (6.5, "confident")], look=-1)


def s03(c, t):  # 13.1 - 26.9  o exemplo
    floor(c)
    show(c, t, 13.3, CX, 240, lambda c: ribbon(c, "UM EXEMPLO", NAVY, 60), anim="stamp")
    show(c, t, 13.5, 300, 470, sc(carta, s=0.8), anim="pop")
    show(c, t, 15.5, 720, 400, M("60 meses", 58, NAVY), anim="pop")
    show(c, t, 17.0, 590, 490, L("15% de administração", 40, INK, MARKER), anim="up")
    show(c, t, 19.1, 590, 560, L("+ 2% fundo de reserva", 40, INK, MARKER), anim="up")
    # barra: 50 mil + 8,5 mil
    PX, x0, y0 = 0.0135, 110, 700
    if t > 14.2:
        k = ease_out(prog(t, 14.2, 0.6))
        rrect(c, x0, y0, 50000 * PX * k, 110, 10); fs(c, NAVY, 6)
        show(c, t, 14.4, x0 + 50000 * PX / 2, y0 + 55, M("50.000", 52, WHITE), anim="pop")
    if t > 20.9:
        k = ease_out(prog(t, 20.9, 0.6))
        xs = x0 + 50000 * PX
        rrect(c, xs, y0, 8500 * PX * k, 110, 10); fs(c, RED, 6)
        show(c, t, 21.1, xs + 8500 * PX / 2, y0 + 170, lambda c: hl(c, "R$ 8.500", 0, 0, 60, PINKISH), anim="stamp")
        show(c, t, 22.8, xs + 8500 * PX / 2, y0 + 250, T("de taxa", 44, RED), anim="up")
    show(c, t, 23.7, 380, 1110, lambda c: hl(c, "parcela: ~R$ 975", 0, 0, 64, LYELLOW), anim="stamp")
    hero(c, t, 965, FY, 0.34, [(0, "present_l"), (21.1, "head"), (23.7, "point_l")],
         [(0, "neutral"), (21.1, "shocked"), (23.7, "neutral")], prop=None, look=-1)


def s04(c, t):  # 26.9 - 41.9  custo anual equivalente x financiamento
    floor(c)
    show(c, t, 27.1, CX, 240, M("Parece pouco...", 70, NAVY), anim="up", t1=34.6)
    show(c, t, 28.3, CX, 330, T("melhor caso: contemplado no 1º mês", 42, DGRAY), anim="up", t1=34.6)
    show(c, t, 34.6, CX, 240, lambda c: hl(c, "CUSTO POR ANO", 0, 0, 64, LYELLOW), anim="stamp")
    base, px, bw = 1000, 18, 230
    bars = [(300, 32.0, 7.0, GREEN, "~7%", "consórcio", 33.0),
            (690, 34.8, 26.4, RED, "~26%", "financiamento", 37.3)]
    for x, t0, v, col, lab, nome, tl in bars:
        if t > t0:
            k = ease_out(prog(t, t0, 0.6))
            h = v * px * k
            rrect(c, x - bw / 2, base - h, bw, h, 10); fs(c, col, 6)
            show(c, t, t0 + 0.1, x, base + 50, T(nome, 42), anim="up")
        show(c, t, tl, x, base - v * px - 50, M(lab, 64, col), anim="stamp")
    if t > 32.0:
        line(c, 150, base, 830, base, 6)
    show(c, t, 35.9, 690, 1120, T("de carro, média do BC", 36, DGRAY), anim="up")
    show(c, t, 39.4, 300, 1130, M("mais barato", 50, GREEN), anim="pop")
    show(c, t, 40.6, CX, 350, stamp_txt("NÃO É DE GRAÇA", RED, 56), anim="stamp")
    hero(c, t, 960, FY, 0.34, [(0, "think"), (32.0, "point_l"), (40.6, "finger_up")],
         [(0, "think"), (32.0, "neutral"), (40.6, "confident")], look=-1)


def s05(c, t):  # 41.9 - 57.8  correção
    floor(c)
    show(c, t, 42.1, CX, 240, lambda c: ribbon(c, "2. A CARTA É CORRIGIDA", NAVY, 52), anim="stamp")
    show(c, t, 44.6, CX, 350, M("geralmente 1 vez por ano", 46, DGRAY), anim="up")
    show(c, t, 46.6, 250, 480, sc(house, s=0.55), anim="drop")
    show(c, t, 47.5, 480, 480, L("imóvel:", 46, INK, MARKER), anim="left")
    show(c, t, 48.5, 760, 480, lambda c: hl(c, "INCC", 0, 0, 56, LYELLOW), anim="stamp")
    show(c, t, 49.8, 250, 640, sc(car, BLUE, s=0.45), anim="drop")
    show(c, t, 50.2, 480, 615, L("carro: preço do carro", 42, INK, MARKER), anim="left")
    show(c, t, 52.3, 480, 675, L("ou um índice, como o", 38, DGRAY), anim="left")
    show(c, t, 53.6, 900, 670, lambda c: hl(c, "IPCA", 0, 0, 48, LYELLOW), anim="stamp")
    # carta e parcela sobem
    show(c, t, 54.6, 250, 830, M("carta", 50, NAVY), anim="up")
    show(c, t, 54.8, 250, 900, M("R$ 50 mil", 46, NAVY), anim="pop")
    if t > 55.2:
        arrow_draw(c, t, 55.2, 250, 950, 250, 990, col=GREEN, d=0.3)
    show(c, t, 55.4, 250, 1040, M("R$ 52.500", 46, GREEN), anim="stamp")
    show(c, t, 56.3, 620, 830, M("parcela", 50, NAVY), anim="up")
    show(c, t, 56.5, 620, 900, M("R$ 975", 46, NAVY), anim="pop")
    if t > 56.9:
        arrow_draw(c, t, 56.9, 620, 950, 620, 990, col=RED, d=0.3)
    show(c, t, 57.1, 620, 1040, M("R$ 1.024", 46, RED), anim="stamp")
    show(c, t, 57.2, 430, 1140, T("(exemplo: +5% no ano)", 34, DGRAY), anim="up")
    hero(c, t, 965, FY, 0.32, [(0, "present_l"), (54.6, "head")], [(0, "neutral"), (54.6, "worried")], look=-1)


def s06(c, t):  # 57.8 - 67.9  sorteio: a fila
    floor(c)
    show(c, t, 58.0, CX, 240, lambda c: ribbon(c, "3. É SORTEIO", NAVY, 60), anim="stamp")
    show(c, t, 61.0, CX, 345, M("o grupo: 60 meses", 46, DGRAY), anim="up")
    cols, rows, cw, ch, x0, y0 = 10, 6, 78, 78, 130, 410
    if t > 61.0:
        rng = random.Random(4)
        order = list(range(60)); rng.shuffle(order)
        for k in range(60):
            r, cc = divmod(k, cols)
            x, y = x0 + cc * cw, y0 + r * ch
            tk = 61.0 + k * 0.02
            if t < tk:
                continue
            col = LGRAY
            if 63.7 <= t < 65.6 and k == 0:
                col = GREEN
            elif 65.6 <= t < 67.9 and k == 59:
                col = RED
            elif 61.6 < t < 63.6:  # destaque andando, como um sorteio
                if order[int((t - 61.6) * 12) % 60] == k:
                    col = GOLD
            rrect(c, x, y, cw - 10, ch - 10, 10); fs(c, col, 4)
            text(c, str(k + 1), x + (cw - 10) / 2, y + (ch - 10) / 2 + 2, 26, MARKER, INK)
    show(c, t, 63.7, 180, 930, lambda c: hl(c, "mês 1?", 0, 0, 52, LGREEN), anim="stamp")
    show(c, t, 65.6, 760, 930, lambda c: hl(c, "mês 60?", 0, 0, 52, PINKISH), anim="stamp")
    show(c, t, 66.9, 470, 1070, stamp_txt("NINGUÉM SABE", RED, 56), anim="stamp")
    hero(c, t, 965, FY, 0.3, [(0, "present_l"), (66.9, "shrug")], [(0, "neutral"), (66.9, "worried")], look=-1)


def s07(c, t):  # 67.9 - 82.1  o lance
    floor(c)
    show(c, t, 68.1, CX, 240, M("Quer sair antes?", 66, NAVY), anim="up")
    show(c, t, 69.3, CX, 350, lambda c: hl(c, "O LANCE", 0, 0, 64, LYELLOW), anim="stamp")
    show(c, t, 70.8, 220, 520, sc(bills, 3, s=0.9), anim="pop")
    show(c, t, 71.4, 220, 640, T("do seu bolso", 42, GREEN), anim="up")
    show(c, t, 72.6, 470, 540, M("ou", 52, DGRAY), anim="pop")
    show(c, t, 73.2, 720, 530, M("lance embutido", 46, RED), anim="pop")
    show(c, t, 74.4, 720, 600, T("usa parte da carta", 40, DGRAY), anim="up")
    # barra da carta 50 mil, embutido 15 mil sai
    X0, W, Y, H = 110, 760, 760, 130
    if t > 76.3:
        k = ease_out(prog(t, 76.3, 0.5))
        rrect(c, X0, Y, W * k, H, 14); fs(c, LGREEN, 6)
        show(c, t, 76.5, X0 + W / 2, Y - 40, M("carta de R$ 50 mil", 44, NAVY), anim="up")
    if t > 77.4:
        k = ease_out(prog(t, 77.4, 0.5))
        rrect(c, X0 + W * 0.7, Y, W * 0.3 * k, H, 14); fs(c, RED, 6)
        show(c, t, 77.8, X0 + W * 0.85, Y + H / 2, M("15 mil", 44, WHITE), anim="stamp")
        show(c, t, 78.0, X0 + W * 0.85, Y + H + 45, T("lance", 40, RED), anim="up")
    show(c, t, 79.8, X0 + W * 0.35, Y + H / 2, M("você recebe", 40, NAVY), anim="pop")
    show(c, t, 80.6, 330, 1110, lambda c: hl(c, "só R$ 35 mil", 0, 0, 66, PINKISH), anim="stamp")
    hero(c, t, 965, FY, 0.32, [(0, "think"), (69.3, "present_l"), (80.6, "head")],
         [(0, "think"), (69.3, "neutral"), (80.6, "shocked")], look=-1)


def s08(c, t):  # 82.1 - 98.3  desistência
    floor(c)
    show(c, t, 82.3, CX, 240, lambda c: ribbon(c, "E SE DESISTIR?", RED, 60), anim="stamp")
    show(c, t, 83.5, CX, 360, M("o dinheiro não volta na hora", 46, NAVY), anim="up")
    show(c, t, 85.5, 230, 540, ball("SUA"), anim="pop")
    show(c, t, 86.2, 330, 540, L("sua cota continua nos sorteios", 42, INK), anim="left")
    show(c, t, 88.0, 140, 660, sc(check_icon, s=0.5), anim="stamp")
    show(c, t, 88.3, 200, 660, L("sorteada: você recebe", 44, GREEN, MARKER), anim="left")
    show(c, t, 90.3, 140, 760, sc(clock, 0), anim="stamp", s=0.45)
    show(c, t, 90.7, 200, 760, L("se não: só no fim do grupo", 44, RED, MARKER), anim="left")
    show(c, t, 92.5, CX, 890, lambda c: hl(c, "E COM DESCONTO", 0, 0, 56, PINKISH), anim="stamp")
    show(c, t, 93.8, 140, 1010, sc(x_icon, s=0.5), anim="stamp")
    show(c, t, 93.9, 200, 1010, L("taxa de adm. não volta", 44, INK), anim="left")
    show(c, t, 96.3, 140, 1100, sc(exclaim, 70, RED), anim="stamp")
    show(c, t, 96.4, 200, 1100, L("contrato pode prever multa", 44, INK), anim="left")
    hero(c, t, 965, FY - 140, 0.28, [(0, "think"), (92.5, "head")], [(0, "think"), (92.5, "worried")], look=-1)


def s09(c, t):  # 98.3 - 110.9  golpe
    floor(c)
    show(c, t, 98.5, CX, 240, lambda c: ribbon(c, "CUIDADO: GOLPE", RED, 62), anim="stamp")
    show(c, t, 99.9, 230, 560, lambda c: (c.save(), c.scale(1.5, 1.5), phone(c, RED), c.restore()), anim="pop")
    if 100.0 < t < 107.6:
        for i in range(3):
            ph = (t * 3 + i * 0.33) % 1.0
            c.save(); c.translate(230, 560)
            c.new_sub_path(); c.arc(0, 0, 200 + ph * 60, -0.6, 0.6)
            rgb(c, RED, 1 - ph); c.set_line_width(6); c.stroke(); c.restore()
    show(c, t, 100.2, 650, 420, lambda c: hl(c, "contemplado garantido!", 0, 0, 42, PINKISH), anim="stamp")
    show(c, t, 102.8, 650, 520, lambda c: hl(c, "carta contemplada barata!", 0, 0, 40, PINKISH), anim="stamp")
    show(c, t, 105.3, 650, 630, group(sc(pix_tag, "PIX", RED, 40, s=1.0), at(0, 70, T("pra pessoa física", 38, RED))), anim="stamp")
    show(c, t, 107.7, CX, 860, M("consórcio sério", 54, NAVY), anim="up")
    show(c, t, 109.0, CX, 970, stamp_txt("NÃO GARANTE DATA", RED, 54), anim="stamp")
    show(c, t, 110.2, CX, 1080, T("de contemplação", 46, RED), anim="up")
    hero(c, t, 965, FY - 120, 0.28, [(0, "head"), (107.7, "finger_up")], [(0, "shocked"), (107.7, "confident")], look=-1)


def s10(c, t):  # 110.9 - 122.7  checklist
    floor(c)
    show(c, t, 111.1, CX, 250, lambda c: ribbon(c, "ANTES DE ASSINAR", NAVY, 58), anim="stamp")
    items = [(112.5, "autorizada pelo", "Banco Central"),
             (116.3, "some todas", "as taxas"),
             (118.1, "entenda o índice", "de correção"),
             (120.4, "leia as regras", "de desistência")]
    for i, (t0, a, b) in enumerate(items):
        y = 410 + i * 165
        show(c, t, t0, 140, y, lambda c: (rrect(c, -36, -36, 72, 72, 10), fs(c, WHITE, 6)), anim="pop")
        show(c, t, t0 + 0.5, 140, y, sc(check_icon, s=0.62), anim="stamp")
        show(c, t, t0, 205, y - 28, L(a, 50, INK, MARKER), anim="left", d=0.3)
        show(c, t, t0 + 0.2, 205, y + 32, L(b, 46, NAVY), anim="left", d=0.3)
    show(c, t, 114.2, 520, 1100, T("consulta grátis no site do BC", 38, DGRAY), anim="up")
    hero(c, t, 960, FY, 0.34, [(0, "present_l"), (120.4, "thumb")], [(0, "confident"), (120.4, "grin")],
         prop=("l", prop_pointer), look=-1)


def s11(c, t):  # 122.7 - fim  seguir pro ep. 5
    floor(c)
    # seta grande pra cima, rumo à coluna de botões (seguir)
    if t > 122.9:
        arrow_draw(c, t, 122.9, 640, 760, 900, 300, col=GOLD, d=0.5, lw=14, head=44)
    show(c, t, 122.9, 470, 300, stamp_txt("SEGUE PRO EP. 5", RED, 78), anim="stamp")
    show(c, t, 123.4, 430, 430, M("sai semana que vem", 52, NAVY), anim="up")
    show(c, t, 125.7, 430, 590, M("Qual você quer?", 64, NAVY), anim="stamp")
    show(c, t, 126.8, 240, 730, block("MEI", LYELLOW, 260, 120, 66), anim="pop")
    show(c, t, 127.3, 430, 730, M("ou", 46, DGRAY), anim="pop")
    show(c, t, 127.5, 650, 730, block("CARTÃO", LBLUE, 320, 120, 58), anim="pop")
    show(c, t, 128.5, 350, 900, group(lambda c: speech(c, 400, 120, 140, 100), T("Comenta!", 62)), anim="pop")
    hero(c, t, 760, FY, 0.62, [(0, "point_ru")], [(0, "happy"), (128.5, "grin")], look=0.6)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 5.1, s01), (5.1, 13.1, s02), (13.1, 26.9, s03), (26.9, 41.9, s04), (41.9, 57.8, s05),
    (57.8, 67.9, s06), (67.9, 82.1, s07), (82.1, 98.3, s08), (98.3, 110.9, s09), (110.9, 122.7, s10),
    (122.7, 999.0, s11),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
