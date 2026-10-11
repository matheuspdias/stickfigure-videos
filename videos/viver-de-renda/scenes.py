"""Quanto você precisa ter pra viver de renda (e em quanto tempo chega lá).
Continuação de primeiros-100-mil. Narração Calm Carlos (HeyGen, ElevenLabs v4), 4 blocos.
Tempos absolutos: bloco1 0,00 | bloco2 133,91 | bloco3 285,12 | bloco4 428,06 | fim da fala 612,54 | +15 s de tela final.
Premissas: Selic 13,75% (Copom 16/9/2026), IPCA 12m 4,58% (set/2026), acumulação a 5% real líquido a.a., meta = gasto anual x 25."""
from engine import *  # noqa

PINKISH = (1, 0.8, 0.76)


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def L(s, size=50, col=INK, font=HAND):
    """texto alinhado à esquerda"""
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def lv(label, val, lsize=50, vsize=60, vcol=GREEN, lcol=DGRAY, after=None):
    """rótulo manuscrito + valor no marcador, em sequência (âncora na esquerda)"""
    def f(c):
        text(c, label, 0, 0, lsize, HAND, lcol, align="l")
        x = text_w(c, label, lsize, HAND) + 18
        text(c, val, x, 0, vsize, MARKER, vcol, align="l")
        if after:
            x += text_w(c, val, vsize, MARKER) + 18
            text(c, after, x, 0, lsize, HAND, lcol, align="l")
    return f


def diego(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 4)
    other(c, t, x, y, s, poses, exprs, **kw)


def julia(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", PURPLE); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 6, w / 2, -6, 9, col)


def down_arrow(col=RED, h=110):
    return lambda c: arrow(c, 0, -h / 2, 0, h / 2, col, 10, 0, 28)


def up_arrow(col=RED, h=110):
    return lambda c: arrow(c, 0, h / 2, 0, -h / 2, col, 10, 0, 28)


def tip(c, t, t0, num, head, col):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"{num}. {head}", 0, 0, 72, col), anim="stamp")


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 12.9  gancho: 5 mil por mês sem trabalhar
    title(c, t, 0.2, "Viver com R$ 5.000 por mês", y=120, size=66)
    show(c, t, 1.2, 960, 205, T("sem trabalhar", 52, DGRAY), anim="up")
    show(c, t, 2.0, 1560, 640, sc(beach_chair, s=1.25))
    hero(c, t, 300, 1000, 1.1, [(0, "stand"), (3.4, "point_r"), (8.5, "think"), (10.1, "present")],
         [(0, "happy"), (3.4, "confident"), (8.5, "think"), (10.1, "happy")], appear=0.1, look=1)
    show(c, t, 4.7, 800, 420, M("R$ 5 milhões", 76, NAVY), anim="pop")
    show(c, t, 5.3, 800, 420, strike(480), anim="fade")
    show(c, t, 6.1, 800, 580, M("R$ 2 milhões", 64, NAVY), anim="pop")
    show(c, t, 6.5, 800, 580, strike(400), anim="fade")
    show(c, t, 8.6, 560, 790, T("conta rápida:", 50, DGRAY), anim="up")
    show(c, t, 10.0, 1000, 790, lambda c: hl(c, "R$ 540 mil?", 0, 0, 70, LGREEN), anim="stamp")


def s02(c, t):  # 12.9 - 28.0  a pegadinha
    show(c, t, 13.5, 960, 140, lambda c: ribbon(c, "TEM UMA PEGADINHA", RED, 62), anim="stamp")
    hero(c, t, 960, 1010, 1.0, [(0, "think"), (16.1, "present"), (22.0, "present")],
         [(0, "think"), (16.1, "neutral"), (22.0, "confident")], appear=12.95, look=0)
    show(c, t, 16.2, 480, 440, group(sc(beach_chair, False, s=0.8), at(0, 150, T("vive de renda de verdade", 46))))
    show(c, t, 17.6, 480, 660, sc(check_icon, 46))
    show(c, t, 18.7, 1440, 440, group(sc(bills, 2, s=1.0), at(110, -40, down_arrow()), at(0, 150, T("fica mais pobre todo ano", 46))))
    show(c, t, 20.9, 1440, 660, T("...sem perceber", 46, RED), anim="up")
    if t > 21.9:
        show(c, t, 23.2, 480, 850, group(sc(calculator, "R$ ?", s=0.6), at(0, 120, T("quanto você precisa", 46))))
        show(c, t, 26.1, 1440, 850, group(sc(clock, t, s=0.9), at(0, 120, T("em quanto tempo chega", 46))))


def s03(c, t):  # 28.0 - 37.6  continuação do vídeo dos 100 mil
    title(c, t, 28.1, "Continuação de...", y=120, size=62)
    show(c, t, 29.0, 1050, 440, lambda c: video_card(c, "Os primeiros R$ 100 mil", "vídeo anterior",
                                                        icon=lambda c: play_btn(c, 70)), anim="pop")
    show(c, t, 33.1, 1050, 760, lambda c: ribbon(c, "PONTO DE VIRADA", GOLD, 54, INK), anim="stamp")
    show(c, t, 35.0, 1050, 900, T("o dinheiro passa a render mais do que você guarda", 46), anim="up")
    hero(c, t, 300, 1010, 1.05, [(0, "point_r"), (33.1, "thumb")], [(0, "happy"), (33.1, "grin")], appear=28.1, look=1)


def s04(c, t):  # 37.6 - 50.4  até a independência; agora com inflação
    title(c, t, 37.7, "Hoje: até o fim da estrada", y=120, size=62)
    k = grow(t, 38.6, 1.6)
    if t > 38.6:
        line(c, 260, 520, 260 + 1190 * k, 520, 10, DGRAY)
        for i in range(8):
            x = 300 + i * 165
            if x + 70 < 260 + 1190 * k:
                line(c, x, 520, x + 70, 520, 6, WHITE)
    show(c, t, 38.6, 300, 420, group(at(0, 0, M("R$ 100 mil", 44, NAVY)), at(0, 50, T("(ponto de virada)", 36, DGRAY))))
    show(c, t, 40.3, 1450, 515, sc(finish_flag, s=1.1), anim="drop")
    show(c, t, 40.6, 1300, 620, M("independência financeira", 48, GREEN), anim="up")
    show(c, t, 45.5, 680, 790, group(sc(x_icon, 38), at(64, 0, L("antes: sem inflação", 52))))
    show(c, t, 48.5, 680, 920, group(sc(check_icon, 38), at(64, 0, L("hoje: com inflação", 52))))
    hero(c, t, 1700, 1050, 0.75, [(0, "present_l"), (48.5, "finger_up")], [(0, "happy"), (48.5, "confident")], appear=42.5, look=-1)


def s05(c, t):  # 50.4 - 61.7  a conta básica: Selic
    show(c, t, 50.5, 960, 130, lambda c: ribbon(c, "A CONTA BÁSICA", NAVY), anim="pop")
    hero(c, t, 330, 1000, 1.1, [(0, "stand"), (52.5, "present"), (59.4, "point_r")],
         [(0, "neutral"), (52.5, "confident"), (59.4, "happy")], appear=50.5, look=1, prop=("l", prop_pointer))
    show(c, t, 52.9, 1060, 320, M("Taxa Selic", 66, NAVY), anim="up")
    show(c, t, 53.6, 1060, 400, T("(a taxa básica de juros do Brasil)", 44, DGRAY), anim="fade")
    show(c, t, 56.4, 1060, 570, lambda c: text(c, "13,75% ao ano", 0, 0, 120, MARKER, GREEN), anim="stamp")
    show(c, t, 59.7, 1060, 800, group(sc(calendar, "16", NAVY, s=0.75), at(140, 0, L("Copom, setembro de 2026", 46))))


def s06(c, t):  # 61.7 - 75.1  imposto: sobra 11,7% (0,93% ao mês)
    title(c, t, 61.8, "Num investimento de longo prazo", y=120, size=60)
    show(c, t, 62.2, 520, 380, group(M("13,75%", 84, GREEN), at(0, 70, T("rendimento bruto", 42, DGRAY))))
    show(c, t, 64.5, 960, 380, group(sc(document, "IR", RED, 40, s=0.9), at(0, 140, T("imposto: 15% do rendimento", 42))))
    arrow_draw(c, t, 67.7, 1160, 380, 1320, 380)
    show(c, t, 68.8, 1540, 380, group(M("11,7%", 96, GREEN), at(0, 70, T("ao ano, líquido", 42, DGRAY))), anim="stamp")
    show(c, t, 71.4, 1160, 700, lambda c: hl(c, "uns 0,93% ao mês", 0, 0, 74, LGREEN))
    hero(c, t, 300, 1010, 1.0, [(0, "stand"), (64.5, "point_r"), (71.4, "thumb")],
         [(0, "neutral"), (64.5, "worried"), (71.4, "happy")], appear=61.8, look=1, prop=("l", prop_calculator))


def s07(c, t):  # 75.1 - 95.1  dividindo: 325 mil, 540 mil, 1,08 milhão
    title(c, t, 75.2, "É só dividir:", y=120, size=64)
    show(c, t, 75.8, 1080, 220, T("renda por mês  /  0,93%  =  patrimônio", 50, DGRAY), anim="up")
    rows = [("R$ 3 mil/mês", 77.3, "R$ 325 mil", 80.0), ("R$ 5 mil/mês", 83.2, "R$ 540 mil", 84.2),
            ("R$ 10 mil/mês", 86.6, "R$ 1,08 milhão", 87.4)]
    for i, (a, ta, b, tb) in enumerate(rows):
        y = 380 + i * 150
        show(c, t, ta, 820, y, M(a, 58, NAVY), anim="left")
        arrow_draw(c, t, tb - 0.2, 1040, y, 1180, y)
        show(c, t, tb, 1430, y, lambda c, b=b: hl(c, b, 0, 0, 60, LGREEN), anim="pop")
    show(c, t, 89.4, 1100, 860, T("parece bem mais perto, né?", 54), anim="up")
    hero(c, t, 300, 1010, 1.0, [(0, "present"), (89.4, "shrug"), (93.4, "finger_up")],
         [(0, "happy"), (89.4, "grin"), (93.4, "think")], appear=75.2, look=1)
    show(c, t, 93.6, 1100, 960, M("agora vem a pegadinha...", 50, RED), anim="up")


def s08(c, t):  # 95.1 - 109.0  a pegadinha: inflação
    show(c, t, 95.2, 960, 130, lambda c: hl(c, "A PEGADINHA: INFLAÇÃO", 0, 0, 74, PINKISH), anim="stamp")
    show(c, t, 98.0, 560, 400, group(sc(cart, s=1.1), at(170, -90, up_arrow())))
    show(c, t, 100.4, 560, 590, group(M("+4,58%", 80, RED), at(0, 70, T("IPCA em 12 meses (set/2026)", 40, DGRAY))), anim="stamp")
    show(c, t, 103.4, 1300, 420, group(sc(piggy, s=1.0), at(0, 150, M("R$ 540 mil", 56, NAVY))))
    show(c, t, 106.5, 1300, 780, group(sc(bills, 2, s=0.8), at(0, 100, T("saca R$ 5 mil todo mês", 46))))
    arrow_draw(c, t, 106.8, 1300, 600, 1300, 690)
    hero(c, t, 1700, 1010, 0.9, [(0, "stand"), (106.5, "hold")], [(0, "neutral"), (106.5, "happy")], appear=103.2, look=-1)


def s09(c, t):  # 109.0 - 117.6  o patrimônio fica parado, os preços não
    title(c, t, 109.1, "O seu dinheiro fica parado...", y=120, size=60)
    show(c, t, 109.4, 420, 420, group(sc(piggy, s=0.9), at(0, 140, M("R$ 540 mil", 50, NAVY))))
    show(c, t, 111.0, 420, 660, T("parado", 52, DGRAY), anim="up")
    title(c, t, 113.1, "...os preços, não", y=260, size=54, col=RED)
    items = [(113.5, "pão", lambda c: (ellipse(c, 0, 0, 80, 45), fs(c, LYELLOW, 6))),
             (114.2, "aluguel", sc(house, s=0.8)), (115.4, "conta de luz", sc(bulb, s=0.9))]
    for i, (t0, lab, fn) in enumerate(items):
        x = 800 + i * 330
        show(c, t, t0, x, 480, group(fn, at(0, 130, T(lab, 46))))
        show(c, t, t0 + 1.4, x + 120, 420, up_arrow(RED, 90), anim="up")
    hero(c, t, 1700, 1030, 0.85, [(0, "shrug"), (116.2, "think")], [(0, "worried"), (116.2, "worried")], appear=109.1)


def s10(c, t):  # 117.6 - 133.9  perda de poder de compra
    title(c, t, 117.7, "O que os seus R$ 5 mil compram", y=120, size=58)
    cols = [(117.8, "hoje", "R$ 5.000", 1.0, GREEN), (118.2, "daqui a 10 anos", "R$ 3.200", 0.64, ORANGE),
            (123.4, "daqui a 20 anos", "R$ 2.000", 0.41, RED)]
    tops = [118.2, 121.0, 124.8]
    base = 780
    for i, ((t0, lab, val, k, col), tt) in enumerate(zip(cols, tops)):
        x = 520 + i * 420
        if t > t0:
            c.save(); c.translate(x, base); bar(c, 420 * k * grow(t, t0), 200, col, lab, val if t > tt else None, 46); c.restore()
    show(c, t, 126.6, 1300, 920, T("você não perdeu nenhum real...", 46), anim="up")
    show(c, t, 128.5, 1300, 1000, lambda c: hl(c, "perdeu PODER DE COMPRA", 0, 0, 50, PINKISH), anim="pop")
    hero(c, t, 180, 1010, 0.8, [(0, "present"), (130.4, "shrug")], [(0, "neutral"), (130.4, "sad")], appear=117.7, look=1)


# ======================================================================= BLOCO 2  (offset 133,91)
def s11(c, t):  # 133.9 - 145.5  dois juros: nominal x real
    title(c, t, 134.0, "Existem dois juros", y=120, size=66)
    show(c, t, 136.3, 560, 330, M("juro NOMINAL", 60, NAVY), anim="up")
    if t > 137.6:
        show(c, t, 137.6, 560, 560, lambda c: (rrect(c, -230, -150, 460, 300, 18), fs(c, WHITE, 6),
                                               text(c, "EXTRATO", 0, -105, 40, MARKER, DGRAY),
                                               line(c, -180, -70, 180, -70, 4, LGRAY)))
    show(c, t, 139.4, 560, 600, M("+11,7%", 92, GREEN), anim="stamp")
    show(c, t, 141.7, 1360, 330, M("juro REAL", 60, GREEN), anim="up")
    show(c, t, 143.2, 1360, 520, T("o que sobra depois", 52), anim="up")
    show(c, t, 144.0, 1360, 600, T("de descontar a inflação", 52), anim="up")
    hero(c, t, 960, 1030, 0.85, [(0, "present"), (141.7, "point_r")], [(0, "happy"), (141.7, "confident")], appear=134.0, look=0)


def s12(c, t):  # 145.5 - 154.0  só o juro real pode ser gasto
    title(c, t, 145.6, "Só esse pedaço pode ser gasto", y=120, size=62)
    x0, y0, w, h = 420, 340, 1080, 150
    if t > 146.0:
        k = grow(t, 146.0, 1.0)
        kr = 6.8 / 11.7
        rrect(c, x0, y0, w * kr * k, h, 14); fs(c, GREEN, 6)
        if t > 148.4:
            kk = grow(t, 148.4, 0.8)
            rrect(c, x0 + w * kr, y0, w * (1 - kr) * kk, h, 14); fs(c, LGRAY, 6)
    show(c, t, 146.6, x0 + w * 0.29, y0 + 75, M("juro real", 52, WHITE), anim="fade")
    show(c, t, 147.4, x0 + w * 0.29, y0 + 230, T("pode gastar", 50, GREEN), anim="up")
    show(c, t, 148.6, x0 + w * 0.79, y0 + 75, M("inflação", 46, DGRAY), anim="fade")
    show(c, t, 149.4, x0 + w * 0.79, y0 + 230, T("fica investido", 50, DGRAY), anim="up")
    show(c, t, 151.2, 960, 760, lambda c: hl(c, "pra corrigir o patrimônio", 0, 0, 58, LYELLOW))
    show(c, t, 152.9, 960, 880, T("e manter o seu poder de compra", 50), anim="up")
    hero(c, t, 210, 1010, 0.85, [(0, "point_r")], [(0, "confident")], appear=145.6, look=1)


def s13(c, t):  # 154.0 - 172.9  o juro real muda: 6,8% hoje, negativo em 2021
    title(c, t, 154.1, "Juro real", y=120, size=66)
    show(c, t, 155.0, 520, 330, T("hoje", 52, DGRAY), anim="up")
    show(c, t, 157.0, 520, 450, M("perto de 6,8%", 74, GREEN), anim="stamp")
    show(c, t, 159.4, 960, 600, lambda c: hl(c, "mas muda o tempo todo", 0, 0, 56, LYELLOW))
    show(c, t, 161.3, 1400, 330, T("em 2021", 52, DGRAY), anim="up")
    show(c, t, 163.5, 1400, 450, group(M("Selic: 2%", 74, NAVY)), anim="stamp")
    show(c, t, 166.1, 1400, 760, group(M("juro real negativo", 56, RED), at(0, -90, down_arrow(RED, 90))), anim="pop")
    hero(c, t, 400, 1010, 1.0, [(0, "present"), (159.4, "shrug"), (171.0, "head")],
         [(0, "happy"), (159.4, "think"), (171.0, "desperate")], appear=154.1, look=1)
    show(c, t, 167.3, 860, 920, T("plano montado em cima de juro alto...", 46), anim="up")
    show(c, t, 171.0, 1520, 920, M("a conta virou!", 52, RED), anim="stamp")


def s14(c, t):  # 172.9 - 181.3  a regra dos 4%
    show(c, t, 173.0, 960, 130, lambda c: T("A regra mais famosa do assunto:", 54, DGRAY)(c), anim="up")
    show(c, t, 176.9, 960, 330, lambda c: text(c, "REGRA DOS 4%", 0, 0, 130, MARKER, NAVY), anim="stamp")
    show(c, t, 178.5, 1250, 680, group(sc(document, "ESTUDO", NAVY, 32, s=1.2), at(0, 175, T("EUA, anos 90", 48))))
    hero(c, t, 500, 1010, 1.1, [(0, "stand"), (176.9, "arms_up"), (178.5, "point_r")],
         [(0, "happy"), (176.9, "grin"), (178.5, "confident")], appear=173.0, look=1)


def s15(c, t):  # 181.3 - 198.7  o que o estudo testou
    title(c, t, 181.4, "O que eles testaram", y=120, size=62)
    show(c, t, 184.2, 520, 400, group(sc(bank, s=1.2), at(0, 140, T("quanto sacar por ano", 48))))
    show(c, t, 186.9, 960, 400, group(sc(prop_tablet, 0, None, s=1.9), at(0, 160, T("ações e títulos", 48))))
    show(c, t, 189.9, 1420, 400, group(sc(calendar, "30", NAVY, s=1.0), at(0, 140, T("sem acabar em 30 anos", 48))))
    show(c, t, 192.7, 760, 740, lambda c: hl(c, "4% no 1º ano", 0, 0, 80, LGREEN), anim="stamp")
    show(c, t, 195.4, 1360, 740, group(L("+ correção pela", 46), at(0, 60, L("inflação depois", 46))), anim="left")
    hero(c, t, 180, 1030, 0.75, [(0, "present"), (192.7, "thumb")], [(0, "neutral"), (192.7, "grin")], appear=181.4, look=1)


def s16(c, t):  # 198.7 - 205.1  na prática: gasto anual x 25
    title(c, t, 198.8, "Na prática:", y=140, size=66)
    show(c, t, 201.0, 960, 420, M("gasto por ANO", 90, NAVY), anim="pop")
    show(c, t, 203.4, 960, 600, lambda c: text(c, "x 25", 0, 0, 170, MARKER, GREEN), anim="stamp")
    hero(c, t, 300, 1010, 1.05, [(0, "present"), (203.4, "finger_up")], [(0, "happy"), (203.4, "confident")],
         appear=198.8, look=1, prop=("l", prop_calculator))


def s17(c, t):  # 205.1 - 221.9  refazendo: 900 mil, 1,5 milhão, 3 milhões
    title(c, t, 205.2, "Refazendo a conta (x 25)", y=120, size=60)
    show(c, t, 205.6, 620, 230, T("renda", 44, DGRAY), anim="fade")
    show(c, t, 205.6, 1000, 230, T("por ano", 44, DGRAY), anim="fade")
    show(c, t, 205.6, 1420, 230, T("patrimônio", 44, DGRAY), anim="fade")
    rows = [("R$ 3 mil", 206.3, "R$ 36 mil", 207.7, "R$ 900 mil", 210.7),
            ("R$ 5 mil", 212.7, "R$ 60 mil", 214.1, "R$ 1,5 milhão", 217.0),
            ("R$ 10 mil", 218.5, "R$ 120 mil", 219.4, "R$ 3 milhões", 220.0)]
    for i, (a, ta, b, tb, d, td) in enumerate(rows):
        y = 380 + i * 190
        show(c, t, ta, 620, y, M(a, 56, NAVY), anim="left")
        show(c, t, tb, 1000, y, M(b, 52, DGRAY), anim="fade")
        show(c, t, td, 1420, y, lambda c, d=d: hl(c, d, 0, 0, 60, LGREEN), anim="stamp")
    hero(c, t, 230, 1030, 0.8, [(0, "present"), (217.0, "point_r")], [(0, "neutral"), (217.0, "shocked")], appear=205.2, look=1)


def s18(c, t):  # 221.9 - 230.8  a diferença: conta rápida x conta honesta
    title(c, t, 222.0, "Olha a diferença (R$ 5 mil por mês)", y=120, size=58)
    base = 860
    if t > 223.2:
        c.save(); c.translate(660, base); bar(c, 220 * grow(t, 223.2), 230, LGRAY, "conta rápida", "R$ 540 mil" if t > 224.4 else None, 50); c.restore()
    if t > 227.5:
        c.save(); c.translate(1160, base); bar(c, 610 * grow(t, 227.5), 230, GREEN, "conta honesta", "R$ 1,5 mi" if t > 228.4 else None, 50); c.restore()
    show(c, t, 229.2, 1560, 520, lambda c: hl(c, "quase 3x", 0, 0, 72, LYELLOW), anim="stamp")
    hero(c, t, 260, 1010, 0.95, [(0, "present"), (229.2, "shrug")], [(0, "neutral"), (229.2, "shocked")], appear=222.0, look=1)


def s19(c, t):  # 230.8 - 245.6  a versão brasileira
    show(c, t, 230.9, 960, 130, lambda c: ribbon(c, "E A VERSÃO BRASILEIRA?", NAVY, 58), anim="stamp")
    show(c, t, 233.1, 560, 430, group(sc(document, "IPCA+", GREEN, 36, s=1.3), at(0, 190, M("Tesouro IPCA+", 52, NAVY))))
    show(c, t, 238.5, 1150, 360, group(M("6% a 7%", 84, GREEN), at(0, 75, T("acima da inflação (5/10/2026)", 42, DGRAY))), anim="stamp")
    show(c, t, 241.5, 1150, 560, T("tirando o imposto...", 48), anim="up")
    show(c, t, 243.5, 1150, 680, lambda c: hl(c, "perto de 5% real", 0, 0, 66, LGREEN))
    hero(c, t, 1740, 1010, 0.9, [(0, "think"), (238.5, "point_l")], [(0, "think"), (238.5, "happy")], appear=231.0, look=-1)


def s20(c, t):  # 245.6 - 252.7  x 20: 1,2 milhão
    title(c, t, 245.7, "Daria pra multiplicar por 20", y=140, size=62)
    show(c, t, 246.6, 760, 420, group(M("x 25", 90, GRAY), at(0, 0, strike(220))), anim="fade")
    show(c, t, 247.6, 1160, 420, M("x 20", 110, GREEN), anim="stamp")
    show(c, t, 248.7, 960, 660, group(at(-260, 0, M("R$ 5 mil/mês", 54, NAVY)), at(-30, 0, lambda c: arrow(c, 0, 0, 90, 0, INK, 7, 0, 22)),
                                      at(300, 0, lambda c: hl(c, "R$ 1,2 milhão", 0, 0, 60, LGREEN))), anim="pop")
    hero(c, t, 300, 1010, 1.0, [(0, "present")], [(0, "happy")], appear=245.7, look=1)


def s21(c, t):  # 252.7 - 266.3  mas as taxas mudam e o dinheiro precisa durar mais
    title(c, t, 252.8, "Só que essas taxas mudam", y=120, size=62)
    # gráfico simples: queda brusca
    if t > 254.5:
        x0, y0 = 300, 560
        line(c, x0, y0 + 40, x0 + 620, y0 + 40, 5, DGRAY)
        k = grow(t, 254.5, 1.6)
        pts = [(0, -180), (200, -170), (300, -175), (420, -60), (620, -50)]
        c.move_to(x0 + pts[0][0], y0 + pts[0][1])
        for px, py in pts[1:]:
            if px <= 620 * k:
                c.line_to(x0 + px, y0 + py)
        rgb(c, RED); c.set_line_width(9); c.stroke()
    show(c, t, 255.0, 610, 300, T("segunda-feira passada", 48, DGRAY), anim="fade")
    show(c, t, 257.3, 720, 740, lambda c: hl(c, "quase -0,7 ponto num dia", 0, 0, 52, PINKISH), anim="stamp")
    show(c, t, 260.4, 1300, 360, group(sc(calendar, "40+", NAVY, 54, s=1.0), at(0, 140, T("quem para cedo:", 46))))
    show(c, t, 263.2, 1300, 640, M("40 a 50 anos", 64, NAVY), anim="pop")
    show(c, t, 265.4, 1300, 760, group(M("não 30", 52, GRAY), at(0, 0, strike(200))), anim="fade")
    hero(c, t, 1720, 1030, 0.8, [(0, "think"), (260.4, "point_l")], [(0, "worried"), (260.4, "confident")], appear=252.8, look=-1)


def s22(c, t):  # 266.3 - 285.1  as regras do canal
    show(c, t, 266.4, 960, 130, lambda c: ribbon(c, "AS REGRAS DA NOSSA CONTA", NAVY, 58), anim="stamp")
    show(c, t, 268.7, 760, 330, group(sc(piggy, s=0.7), at(110, 0, L("pra juntar:", 50, DGRAY))))
    show(c, t, 270.5, 1100, 420, lambda c: hl(c, "5% ao ano acima da inflação", 0, 0, 54, LGREEN), anim="left")
    show(c, t, 272.5, 1100, 510, T("(já descontado o imposto)", 42, DGRAY), anim="fade")
    show(c, t, 275.0, 760, 640, group(sc(finish_flag, 140, s=0.7), at(110, 0, L("pra meta:", 50, DGRAY))))
    show(c, t, 275.6, 1100, 720, lambda c: hl(c, "regra dos 4%  (x 25)", 0, 0, 54, LYELLOW), anim="left")
    show(c, t, 278.0, 1100, 810, T("com margem de segurança", 42, DGRAY), anim="fade")
    show(c, t, 279.6, 1100, 930, M("tudo em dinheiro de hoje", 46, NAVY), anim="up")
    show(c, t, 281.3, 1100, 1000, T("aporte corrigido pela inflação todo ano", 40), anim="up")
    hero(c, t, 260, 1010, 0.95, [(0, "present"), (275.0, "finger_up"), (281.3, "thumb")],
         [(0, "happy"), (275.0, "confident"), (281.3, "grin")], appear=266.4, look=1, prop=("l", prop_pointer))


# ======================================================================= BLOCO 3  (offset 285,12)
def s23(c, t):  # 285.1 - 295.6  quanto tempo leva? 3 aportes
    title(c, t, 285.2, "Quanto tempo leva?", y=130, size=72)
    show(c, t, 285.6, 960, 300, sc(clock, t, s=1.1))
    for i, (v, t0) in enumerate((("R$ 500", 290.5), ("R$ 1.000", 291.6), ("R$ 2.000", 292.4))):
        show(c, t, t0, 560 + i * 400, 560, group(sc(bills, i + 1, s=0.8), at(0, 120, M(v, 56, GREEN)), at(0, 180, T("por mês", 40))))
    show(c, t, 294.2, 960, 860, lambda c: hl(c, "começando do zero", 0, 0, 56, LYELLOW))
    hero(c, t, 210, 1030, 0.8, [(0, "think"), (290.5, "present")], [(0, "think"), (290.5, "happy")], appear=285.2, look=1)


TAB_X = [520, 990, 1320, 1650]          # colunas: meta | 500 | 1.000 | 2.000
TAB_Y = [250, 420, 590, 760]            # linhas: cabeçalho | 3 mil | 5 mil | 10 mil
CELLS = [  # (linha, coluna, texto, t)
    (1, 0, ("R$ 3 mil/mês", "R$ 900 mil"), (295.6, 298.4)),
    (1, 1, "43a 6m", 303.0), (1, 2, "31a 7m", 306.1), (1, 3, "21a 5m", 309.4),
    (2, 0, ("R$ 5 mil/mês", "R$ 1,5 milhão"), (311.8, 313.9)),
    (2, 1, "53 anos", 316.8), (2, 2, "40a 3m", 319.2), (2, 3, "28a 9m", 322.4),
    (3, 0, ("R$ 10 mil/mês", "R$ 3 milhões"), (324.9, 327.1)),
    (3, 1, "66a 5m", 330.0), (3, 2, "53 anos", 332.3), (3, 3, "40a 3m", 334.6),
]


def table(c, t, t0, hi=(), dim=False):
    """tabela de tempos (anos e meses) por meta de renda x aporte mensal"""
    if t < t0:
        return
    a = ease_out(prog(t, t0, 0.5))
    # grade
    for i, y in enumerate(TAB_Y[:-1]):
        line(c, 300, y + 85, 1800, y + 85, 3, LGRAY)
    for x in (760, 1160, 1490):
        line(c, x, 190, x, 850, 3, LGRAY)
    show(c, t, t0, TAB_X[0], TAB_Y[0], T("renda  >  meta", 42, DGRAY), anim="fade")
    for j, v in enumerate(("R$ 500", "R$ 1.000", "R$ 2.000")):
        show(c, t, t0 + 0.1 * j, TAB_X[j + 1], TAB_Y[0], M(v, 48, GREEN), anim="fade")
    for r, col, txt, tt in CELLS:
        x, y = TAB_X[col], TAB_Y[r]
        if col == 0:
            show(c, t, tt[0], x, y - 22, M(txt[0], 44, NAVY), anim="left")
            show(c, t, tt[1], x, y + 32, T(txt[1], 40, DGRAY), anim="fade")
        else:
            on = (r, col) in hi
            bg = LYELLOW if on else None
            if on and t > max(tt, 342.0):
                show(c, t, tt, x, y, lambda c, s=txt: hl(c, s, 0, 0, 50, LYELLOW), anim="fade")
            else:
                show(c, t, tt, x, y, M(txt, 50, GRAY if dim else INK), anim="pop")


def s24(c, t):  # 295.6 - 351.5  a tabela completa e a coincidência curiosa
    title(c, t, 295.7, "Viver de renda: quanto tempo leva", y=110, size=56)
    hi = set()
    if t > 342.0:
        hi.add((2, 2))
    if t > 346.6:
        hi.add((3, 3))
    table(c, t, 295.7, hi=hi)
    if t > 349.2:
        show(c, t, 349.2, 1150, 960, lambda c: hl(c, "mesmos 40 anos e 3 meses!", 0, 0, 56, LGREEN), anim="stamp")
    elif t > 339.5:
        show(c, t, 339.5, 1150, 960, T("tem uma coisa curiosa aqui...", 52), anim="up")
    hero(c, t, 150, 1040, 0.7, [(0, "present"), (339.5, "think"), (349.2, "arms_up")],
         [(0, "neutral"), (339.5, "think"), (349.2, "grin")], appear=295.7, look=1)


def s25(c, t):  # 351.5 - 368.4  duas alavancas
    show(c, t, 351.6, 960, 130, M("Não é coincidência", 66), anim="up")
    show(c, t, 353.0, 960, 260, lambda c: hl(c, "dobrar o aporte  =  cortar a meta pela metade", 0, 0, 52, LYELLOW), anim="pop")
    show(c, t, 359.4, 960, 390, T("existem duas alavancas", 54), anim="up")
    show(c, t, 360.6, 620, 690, sc(lever, grow(t, 361.0, 0.8), GREEN, "quanto você coloca"))
    show(c, t, 363.0, 1300, 690, sc(lever, 0.0, GOLD, "quanto você precisa"))
    show(c, t, 365.6, 960, 960, T("quase todo mundo só olha pra primeira", 50, RED), anim="up")
    if t > 365.6:
        show(c, t, 366.0, 1300, 480, lambda c: qmark(c, 90, GOLD))
    hero(c, t, 1720, 1030, 0.75, [(0, "present_l"), (365.6, "shrug")], [(0, "happy"), (365.6, "worried")], appear=351.6, look=-1)


def s26(c, t):  # 368.4 - 378.9  a virada: quem gasta 5 mil e investe mil
    show(c, t, 368.5, 960, 130, lambda c: ribbon(c, "A VIRADA", GOLD, 70, INK), anim="stamp")
    other(c, t, 420, 1010, 1.0, [(0, "stand"), (372.9, "hold")], [(0, "happy")], appear=370.3, look=0.6, shirt=ORANGE)
    show(c, t, 370.8, 760, 370, lv("gasta", "R$ 5.000", 52, 62, RED, after="por mês"), anim="left")
    show(c, t, 372.9, 760, 490, lv("investe", "R$ 1.000", 52, 62, GREEN, after="por mês"), anim="left")
    show(c, t, 374.2, 760, 650, lv("meta:", "R$ 1,5 milhão", 52, 64, NAVY), anim="left")
    show(c, t, 376.8, 1150, 840, lambda c: hl(c, "40 anos e 3 meses", 0, 0, 64, PINKISH), anim="stamp")


def s27(c, t):  # 378.9 - 391.9  corta mil reais do custo de vida
    title(c, t, 379.0, "Corta R$ 1.000 do custo de vida", y=120, size=60)
    other(c, t, 260, 1010, 0.9, [(0, "hips"), (388.6, "arms_up")], [(0, "confident"), (388.6, "grin")], appear=379.0, look=1, shirt=ORANGE)
    items = [(382.3, sc(car, BLUE, s=0.7), "carro mais barato"), (385.0, sc(house, s=0.75), "renegocia o aluguel"),
             (385.7, sc(card, s=0.8), "cancela o que não usa")]
    for i, (t0, fn, lab) in enumerate(items):
        x = 720 + i * 420
        show(c, t, t0, x, 400, group(fn, at(0, 130, T(lab, 44))))
    show(c, t, 388.6, 820, 680, lv("passa a viver bem com", "R$ 4.000", 52, 66, GREEN, INK), anim="left")
    show(c, t, 389.8, 1140, 860, lambda c: hl(c, "esse corte age DUAS vezes", 0, 0, 58, LYELLOW), anim="stamp")


def s28(c, t):  # 391.9 - 403.9  efeito 1: a meta cai 300 mil
    show(c, t, 392.0, 960, 130, lambda c: hl(c, "1. A meta cai", 0, 0, 72, LGREEN), anim="stamp")
    show(c, t, 394.0, 960, 330, M("R$ 4 mil  x 12  x 25", 70, NAVY), anim="up")
    show(c, t, 397.2, 960, 470, lambda c: hl(c, "= R$ 1,2 milhão", 0, 0, 72, LGREEN), anim="pop")
    show(c, t, 398.6, 1100, 700, group(M("R$ 1,5 mi", 54, GRAY), at(0, 0, strike(260)), at(160, 0, lambda c: arrow(c, 0, 0, 90, 0, INK, 7, 0, 22)),
                                       at(400, 0, M("R$ 1,2 mi", 60, GREEN))), anim="fade")
    show(c, t, 399.4, 1100, 860, lambda c: text(c, "- R$ 300 mil", 0, 0, 96, MARKER, GREEN), anim="stamp")
    hero(c, t, 280, 1010, 1.0, [(0, "present"), (399.4, "arms_up")], [(0, "happy"), (399.4, "grin")], appear=392.0, look=1)


def s29(c, t):  # 403.9 - 416.1  efeito 2: o aporte dobra
    show(c, t, 404.4, 960, 130, lambda c: hl(c, "2. O aporte dobra", 0, 0, 72, LGREEN), anim="stamp")
    show(c, t, 405.6, 560, 380, group(sc(bills, 2, s=0.9), at(230, 0, lambda c: arrow(c, 0, 0, 120, 0, GREEN, 8, 0, 24)),
                                      at(480, 0, sc(piggy, s=0.8))))
    show(c, t, 408.6, 1400, 330, M("R$ 1.000", 56, GRAY), anim="fade")
    show(c, t, 408.8, 1400, 330, strike(240), anim="fade")
    show(c, t, 410.6, 1400, 430, M("R$ 2.000", 72, GREEN), anim="stamp")
    show(c, t, 411.8, 680, 700, group(M("40 anos", 70, GRAY), at(0, 0, strike(300))), anim="fade")
    arrow_draw(c, t, 413.2, 860, 700, 1000, 700)
    show(c, t, 414.6, 1360, 700, lambda c: hl(c, "25 anos e 5 meses", 0, 0, 66, LGREEN), anim="stamp")
    hero(c, t, 1760, 1050, 0.7, [(0, "point_l"), (414.6, "thumb")], [(0, "happy"), (414.6, "grin")], appear=404.4, look=-1)


def s30(c, t):  # 416.1 - 428.1  15 anos de liberdade
    show(c, t, 417.0, 960, 260, lambda c: text(c, "15 ANOS", 0, 0, 170, MARKER, GREEN), anim="stamp")
    show(c, t, 418.0, 960, 400, M("de liberdade", 70, NAVY), anim="up")
    show(c, t, 419.6, 960, 490, T("comprados com R$ 1.000 de corte por mês", 50, DGRAY), anim="up")
    show(c, t, 421.5, 960, 700, group(M("cada R$ 1", 64, RED), at(0, 70, T("a menos de gasto por mês", 44))), anim="pop")
    show(c, t, 424.6, 960, 900, lambda c: hl(c, "= R$ 300 a menos na meta", 0, 0, 66, LYELLOW), anim="stamp")
    show(c, t, 417.4, 1580, 720, sc(beach_chair, s=0.95))
    hero(c, t, 330, 1010, 1.0, [(0, "arms_up"), (421.5, "finger_up")], [(0, "grin"), (421.5, "confident")], appear=416.2, look=1)


# ======================================================================= BLOCO 4  (offset 428,06)
def s31(c, t):  # 428.1 - 440.8  Diego e Júlia
    title(c, t, 428.2, "Duas pessoas", y=120, size=66)
    diego(c, t, 620, 1000, 1.05, [(0, "wave"), (434.4, "stand")], [(0, "happy")], appear=431.9, look=0.5)
    julia(c, t, 1300, 1000, 1.05, [(0, "wave"), (434.4, "stand")], [(0, "happy")], appear=432.9, look=-0.5)
    show(c, t, 432.2, 620, 380, M("Diego", 64, ORANGE), anim="up")
    show(c, t, 433.2, 1300, 380, M("Júlia", 64, PURPLE), anim="up")
    show(c, t, 434.4, 960, 250, group(at(-330, 0, T("30 anos", 48)), at(0, 0, T("R$ 10 mil líquidos", 48)),
                                      at(330, 0, T("do zero", 48))), anim="fade")
    show(c, t, 436.7, 960, 600, sc(eq, 70, NAVY, 16), anim="pop")


def s32(c, t):  # 440.8 - 461.3  padrões de vida diferentes
    line(c, 960, 220, 960, 1000, 5, LGRAY)
    diego(c, t, 230, 1010, 0.85, [(0, "hips"), (448.5, "hold")], [(0, "confident"), (448.5, "happy")], appear=440.9, look=1)
    show(c, t, 441.0, 480, 140, M("Diego", 66, ORANGE), anim="up")
    show(c, t, 443.9, 400, 360, lv("gasta", "R$ 8.000", 48, 62, RED, after="/mês"), anim="left")
    show(c, t, 445.9, 400, 465, L("e quer manter depois", 46), anim="up")
    show(c, t, 448.5, 400, 600, lv("investe", "R$ 2.000", 48, 62, GREEN, after="/mês"), anim="left")
    julia(c, t, 1150, 1010, 0.85, [(0, "stand"), (452.7, "thumb"), (457.7, "hold")], [(0, "happy"), (452.7, "grin")], appear=450.7, look=1)
    show(c, t, 450.8, 1440, 140, M("Júlia", 66, PURPLE), anim="up")
    show(c, t, 452.7, 1300, 360, lv("vive bem com", "R$ 4.000", 48, 62, GREEN), anim="left")
    show(c, t, 453.8, 1300, 465, L("sem passar aperto", 46), anim="up")
    show(c, t, 457.7, 1300, 600, lv("investe", "R$ 6.000", 48, 62, GREEN, after="/mês"), anim="left")
    show(c, t, 459.9, 960, 235, lambda c: hl(c, "quem chega primeiro?", 0, 0, 62, LYELLOW), anim="stamp")


def s33(c, t):  # 461.3 - 476.4  as metas
    title(c, t, 461.4, "A meta de cada um (x 25)", y=120, size=60)
    base = 840
    show(c, t, 461.4, 560, 980, M("Diego", 54, ORANGE), anim="fade")
    if t > 462.2:
        c.save(); c.translate(560, base); bar(c, 560 * grow(t, 462.2, 1.2), 260, ORANGE, None, "R$ 2,4 milhões" if t > 466.1 else None, 50); c.restore()
    show(c, t, 469.0, 1260, 980, M("Júlia", 54, PURPLE), anim="fade")
    if t > 469.0:
        c.save(); c.translate(1260, base); bar(c, 280 * grow(t, 469.0, 1.0), 260, PURPLE, None, "R$ 1,2 milhão" if t > 471.0 else None, 50); c.restore()
    show(c, t, 472.6, 1650, 420, group(M("3x", 90, GREEN), at(0, 80, T("mais aporte", 44))), anim="stamp")
    hero(c, t, 1700, 1040, 0.6, [(0, "point_l")], [(0, "confident")], appear=461.4, look=-1)


def s34(c, t):  # 476.4 - 493.5  a corrida: 66 x 42 anos
    title(c, t, 476.5, "Quem fica livre primeiro?", y=110, size=60)
    x0, x1 = 320, 1620
    for i, (who, y, t0, dur, age, col) in enumerate((("Diego", 450, 476.4, 36.42, 66, ORANGE), ("Júlia", 800, 482.0, 12.25, 42, PURPLE))):
        line(c, x0, y, x1, y, 8, LGRAY)
        k = grow(t, t0, 1.6)
        xe = x0 + (x1 - x0) * (dur / 40.0) * k
        line(c, x0, y, xe, y, 12, col)
        show(c, t, t0, x0 - 20, y - 70, M(who, 50, col), anim="fade")
        if t > t0 + 1.0:
            show(c, t, t0 + 1.0, xe, y - 90, lambda c, d=dur: hl(c, f"{int(d)}a {round((d % 1) * 12)}m", 0, 0, 44, LYELLOW))
        show(c, t, t0 + 3.3, xe + 70, y + 10, sc(finish_flag, 120, s=0.7), anim="drop")
        show(c, t, t0 + 3.3, xe, y + 80, M(f"livre aos {age}", 46, col), anim="up")
    if t > 476.4:
        for i, yy in enumerate((450, 800)):
            pass
    diego(c, t, 160, 560, 0.45, [(0, "run")], [(0, "worried")], appear=476.5)
    julia(c, t, 160, 910, 0.45, [(0, "run")], [(0, "happy")], appear=482.0)
    show(c, t, 487.3, 1320, 965, lambda c: hl(c, "24 anos de diferença", 0, 0, 62, PINKISH), anim="stamp")
    show(c, t, 489.9, 960, 1050, T("mesmo salário, mesma idade, mesmo investimento", 42, DGRAY), anim="up")


def s35(c, t):  # 493.5 - 502.3  quando a Júlia chega, o Diego tem 400 mil
    title(c, t, 493.6, "Quando a Júlia chega lá...", y=120, size=62)
    julia(c, t, 1600, 1010, 0.95, [(0, "arms_up")], [(0, "grin")], appear=493.6, look=-1)
    show(c, t, 494.0, 1600, 450, sc(beach_chair, s=0.7))
    diego(c, t, 420, 1010, 0.95, [(0, "stand"), (500.3, "head")], [(0, "neutral"), (500.3, "desperate")], appear=493.6, look=1)
    show(c, t, 495.9, 640, 360, lv("o Diego tem", "R$ 400 mil", 50, 64, NAVY), anim="left")
    show(c, t, 497.6, 640, 500, lv("dá uns", "R$ 1.300/mês", 50, 64, GREEN), anim="left")
    show(c, t, 500.3, 640, 660, lv("longe dos", "R$ 8.000", 50, 64, RED, after="que ele quer"), anim="left")


def s36(c, t):  # 502.3 - 521.6  não é miséria: quanto custa a vida que te faz bem
    title(c, t, 502.4, "Não é sobre viver na miséria", y=120, size=62)
    julia(c, t, 380, 1010, 0.95, [(0, "relax"), (507.9, "present")], [(0, "happy"), (507.9, "confident")], appear=502.4, look=1)
    show(c, t, 505.0, 420, 470, T("come bem, sai de casa, vive bem", 44), anim="up")
    show(c, t, 507.9, 1200, 330, lambda c: hl(c, "quanto custa a vida que te faz bem?", 0, 0, 56, LYELLOW), anim="pop")
    show(c, t, 511.5, 1200, 520, group(M("+ R$ 1.000/mês", 60, RED), at(0, 65, T("no padrão de vida", 44))), anim="up")
    show(c, t, 515.0, 1200, 690, T("não custa só mil reais...", 48), anim="up")
    show(c, t, 517.0, 1200, 820, lambda c: hl(c, "custa R$ 300 mil de patrimônio", 0, 0, 56, PINKISH), anim="stamp")
    show(c, t, 519.4, 1200, 940, M("+ anos de trabalho", 52, RED), anim="up")


def s37(c, t):  # 521.6 - 542.2  1. descubra o seu número
    if t < 525.3:
        title(c, t, 521.6, "Como colocar em prática?", y=300, size=70)
        show(c, t, 523.9, 960, 470, M("3 atitudes", 66, NAVY), anim="up")
        hero(c, t, 960, 1010, 1.0, [(0, "think")], [(0, "think")], appear=521.6)
        return
    tip(c, t, 525.3, 1, "Descubra o seu número", LGREEN)
    show(c, t, 527.9, 400, 440, group(sc(clipboard, "GASTOS", 3, False, s=0.9), at(0, 180, T("últimos 3 meses", 44))))
    steps = [("média", 530.6), ("x 12", 531.7), ("x 25", 533.3)]
    for i, (s, t0) in enumerate(steps):
        show(c, t, t0, 800 + i * 330, 420, M(s, 72, NAVY if i < 2 else GREEN), anim="pop")
        if i < 2:
            arrow_draw(c, t, t0 + 0.4, 905 + i * 330, 420, 1015 + i * 330, 420)
    show(c, t, 534.7, 1060, 660, lambda c: hl(c, "= o patrimônio que você precisa", 0, 0, 58, LYELLOW), anim="stamp")
    show(c, t, 538.9, 1000, 860, T("sem esse número, você não sabe pra onde está indo", 46, RED), anim="up")
    hero(c, t, 1720, 1030, 0.75, [(0, "present_l")], [(0, "confident")], appear=525.4, look=-1, prop=("r", prop_calculator))


def s38(c, t):  # 542.2 - 559.2  2. ataque os gastos fixos e proteja os aumentos
    tip(c, t, 542.2, 2, "Ataque os fixos, proteja os aumentos", LYELLOW)
    for i, (t0, fn, lab) in enumerate(((546.5, sc(house, s=0.7), "aluguel"), (547.6, sc(car, BLUE, s=0.6), "carro"),
                                       (548.4, sc(card, s=0.7), "assinaturas"))):
        show(c, t, t0, 480 + i * 330, 400, group(fn, at(0, 120, T(lab, 44))))
    show(c, t, 549.5, 1540, 400, lambda c: hl(c, "vale pra sempre", 0, 0, 56, LGREEN), anim="stamp")
    show(c, t, 552.7, 860, 700, group(M("ganhou aumento?", 56, NAVY)), anim="up")
    show(c, t, 554.2, 500, 840, lv("pelo menos", "METADE", 52, 64, GREEN, INK, after="do aumento vai pro investimento"), anim="left")
    hero(c, t, 230, 1010, 0.85, [(0, "finger_up"), (552.7, "point_r")], [(0, "confident"), (552.7, "happy")], appear=542.3, look=1)


def s39(c, t):  # 559.2 - 579.7  3. proteja da inflação e refaça a conta todo ano
    tip(c, t, 559.2, 3, "Proteja da inflação", LBLUE)
    show(c, t, 562.4, 380, 380, group(sc(calendar, "1x", NAVY, 60, s=0.9), at(0, 130, T("refaça a conta todo ano", 44))))
    show(c, t, 564.4, 860, 380, group(sc(bills, 2, s=0.8), at(0, 130, T("corrija o aporte", 44))))
    show(c, t, 566.5, 1390, 380, group(sc(shield, GREEN, s=1.0), at(0, 130, T("investimento que acompanha a inflação", 40))))
    show(c, t, 570.1, 960, 600, lambda c: hl(c, "a meta ainda faz sentido?", 0, 0, 54, LYELLOW))
    show(c, t, 572.8, 760, 840, sc(shield, NAVY, s=1.1), anim="pop")
    show(c, t, 574.9, 1180, 820, group(M("reserva de emergência", 52, NAVY), at(0, 70, T("antes de tudo", 44, DGRAY))), anim="left")
    hero(c, t, 1700, 1030, 0.8, [(0, "present_l"), (572.8, "finger_up")], [(0, "happy"), (572.8, "confident")], appear=559.3, look=-1)


def s40(c, t):  # 579.7 - 597.0  recapitulando
    title(c, t, 579.7, "Recapitulando", y=110, size=66)
    show(c, t, 580.8, 760, 280, group(sc(x_icon, 34), at(50, 0, L("conta rápida: esquece a inflação", 48))), anim="left")
    show(c, t, 584.3, 760, 400, group(sc(check_icon, 34), at(50, 0, L("conta honesta: gasto anual x 25", 48))), anim="left")
    show(c, t, 587.9, 960, 520, T("duas alavancas:", 50, DGRAY), anim="up")
    show(c, t, 591.0, 700, 760, sc(lever, 0.6, GREEN, "quanto você investe"), s=0.85)
    show(c, t, 592.6, 1220, 760, sc(lever, grow(t, 594.8, 0.8), GOLD, "quanto você precisa"), s=0.85)
    show(c, t, 594.8, 1220, 960, lambda c: hl(c, "a mais rápida!", 0, 0, 48, LYELLOW), anim="stamp")
    hero(c, t, 1700, 1030, 0.75, [(0, "present_l"), (594.8, "thumb")], [(0, "happy"), (594.8, "grin")], appear=579.8, look=-1)


def s41(c, t):  # 597.0 - 600.2  comentários: qual é o seu número?
    show(c, t, 597.1, 1060, 400, lambda c: speech(c, 900, 260, -330, 170), anim="pop")
    show(c, t, 597.3, 1060, 350, T("Me conta nos comentários:", 52, DGRAY), anim="fade")
    show(c, t, 599.1, 1060, 440, M("qual é o seu número?", 60, NAVY), anim="fade")
    hero(c, t, 340, 1010, 1.1, [(0, "wave")], [(0, "happy")], appear=597.1, look=1)


def s42(c, t):  # 600.2 - 608.6  vídeo dos 100 mil
    show(c, t, 600.3, 960, 140, T("ainda na fase dos primeiros R$ 100 mil?", 56), anim="up")
    show(c, t, 603.2, 1180, 540, lambda c: video_card(c, "Juntar R$ 100 mil", "quanto tempo leva?", icon=lambda c: play_btn(c, 70)), anim="pop")
    hero(c, t, 400, 1010, 1.05, [(0, "think"), (603.2, "point_r")], [(0, "think"), (603.2, "happy")], appear=600.3, look=1)


def s43(c, t):  # 608.6 - 612.6  assinatura
    show(c, t, 608.6, 960, 300, lambda c: text(c, "FAZ A CONTA", 0, 0, 120, MARKER, NAVY), anim="stamp")
    show(c, t, 609.6, 960, 430, lambda c: hl(c, "a gente faz a conta", 0, 0, 60, LYELLOW))
    hero(c, t, 960, 1010, 1.0, [(0, "present"), (611.5, "wave")], [(0, "happy"), (611.5, "grin")], appear=608.7)


def s44(c, t):  # 612.6 - fim (15 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres para os elementos da Tela final: vídeo à esquerda (x 170-950, y 300-740)
    # e botão inscrever-se à direita (círculo centrado em ~1450, 520).
    show(c, t, 612.7, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, 613.0, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, 613.0, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (615.0, "relax")], [(0, "happy")], appear=612.7)


SCENES = [
    (0.0, 12.9, s01), (12.9, 28.0, s02), (28.0, 37.6, s03), (37.6, 50.4, s04), (50.4, 61.7, s05),
    (61.7, 75.1, s06), (75.1, 95.1, s07), (95.1, 109.0, s08), (109.0, 117.6, s09), (117.6, 133.91, s10),
    (133.91, 145.5, s11), (145.5, 154.0, s12), (154.0, 172.9, s13), (172.9, 181.3, s14), (181.3, 198.7, s15),
    (198.7, 205.1, s16), (205.1, 221.9, s17), (221.9, 230.8, s18), (230.8, 245.6, s19), (245.6, 252.7, s20),
    (252.7, 266.3, s21), (266.3, 285.12, s22),
    (285.12, 295.6, s23), (295.6, 351.5, s24), (351.5, 368.4, s25), (368.4, 378.9, s26), (378.9, 391.9, s27),
    (391.9, 403.9, s28), (403.9, 416.1, s29), (416.1, 428.06, s30),
    (428.06, 440.8, s31), (440.8, 461.3, s32), (461.3, 476.4, s33), (476.4, 493.5, s34), (493.5, 502.3, s35),
    (502.3, 521.6, s36), (521.6, 542.2, s37), (542.2, 559.2, s38), (559.2, 579.7, s39), (579.7, 597.0, s40),
    (597.0, 600.2, s41), (600.2, 608.6, s42), (608.6, 612.6, s43), (612.6, 999.0, s44),
]

# só toques pontuais, sem ruído: R$ 540 mil? / quase 3x / 15 anos de liberdade / 24 anos de diferença
SFX = [(10.0, "tum"), (229.2, "tum"), (417.0, "soft_ding"), (487.3, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key")
