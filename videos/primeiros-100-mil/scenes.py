"""Quanto tempo leva pra juntar R$ 100 mil (e por que os primeiros são os mais difíceis).
Narração Calm Carlos (HeyGen, ElevenLabs v4), 4 blocos. Tempos absolutos do áudio juntado
(bloco1 0,00 | bloco2 157,68 | bloco3 322,08 | bloco4 394,71 | fim 515,06)."""
from engine import *  # noqa

PINKISH = (1, 0.8, 0.76)


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def gbar(c, t, t0, x, y, h, w=150, col=GREEN, label=None, top=None, size=44, top_t=None):
    """barra que cresce a partir de t0; o valor de cima aparece em top_t (padrão: fim do crescimento)"""
    if t < t0:
        return
    k = grow(t, t0)
    tt = top if (top_t is None and k > 0.95) or (top_t is not None and t >= top_t) else None
    c.save(); c.translate(x, y); bar(c, h * k, w, col, label, tt, size); c.restore()


def ana(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", PINK); kw.setdefault("hair", "long"); kw.setdefault("fid", 3)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def bruno(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", ORANGE); kw.setdefault("fid", 4)
    other(c, t, x, y, s, poses, exprs, **kw)


def curve(c, t, t0, x0, y0, w, h, d=2.5, col=GREEN, lw=9, n=80, power=3.2):
    """curva exponencial que se desenha da esquerda pra direita"""
    if t < t0:
        return
    k = clamp01((t - t0) / d)
    c.move_to(x0, y0)
    for i in range(1, int(n * k) + 1):
        u = i / n
        c.line_to(x0 + u * w, y0 - h * (u ** power))
    rgb(c, col); c.set_line_width(lw); c.stroke()


def axes(c, x0, y0, w, h):
    arrow(c, x0, y0, x0 + w + 40, y0, INK, 6, 0, 22)
    arrow(c, x0, y0, x0, y0 - h - 40, INK, 6, 0, 22)


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 12.8  gancho: os três blocos de 100 mil
    title(c, t, 0.3, "Guardando R$ 1.000 por mês...", y=120, size=60)
    hero(c, t, 300, 990, 1.1, [(0, "stand"), (2.8, "present"), (10.2, "shrug")],
         [(0, "happy"), (2.8, "confident"), (10.2, "shocked")], appear=0.1, look=0.8)
    base = 900
    gbar(c, t, 2.9, 780, base, 300, 230, NAVY, "1º R$ 100 mil", None, 46)
    show(c, t, 4.8, 780, base - 360, lambda c: hl(c, "6 anos +", 0, 0, 52, LYELLOW))
    gbar(c, t, 7.1, 1180, base, 300, 230, BLUE, "2º R$ 100 mil", None, 46)
    show(c, t, 8.6, 1180, base - 360, lambda c: hl(c, "menos de 4", 0, 0, 52, LGREEN))
    gbar(c, t, 10.3, 1580, base, 300, 230, GREEN, "3º R$ 100 mil", None, 46)
    show(c, t, 11.4, 1580, base - 360, lambda c: hl(c, "menos de 3", 0, 0, 52, LGREEN))


def s02(c, t):  # 12.8 - 24.8  mesmo valor, nada diferente, cada vez mais rápido
    title(c, t, 12.9, "O mesmo valor, todo mês", y=120, size=62)
    for i in range(5):
        show(c, t, 13.3 + i * 0.25, 360 + i * 300, 330,
             group(sc(calendar, str(i + 1), s=0.8), at(0, 115, M("R$ 1.000", 38, GREEN))))
    items = [("aumento", 16.6, 560), ("ação certeira", 17.7, 960), ("nada diferente", 19.3, 1360)]
    for lab, t0, x in items:
        show(c, t, t0, x, 640, group(sc(x_icon, 40), at(0, 80, T(lab, 46))))
    hero(c, t, 230, 1010, 0.95, [(0, "stand"), (16.5, "think"), (21.4, "arms_up")],
         [(0, "neutral"), (16.5, "think"), (21.4, "grin")], appear=12.9)
    show(c, t, 22.4, 1080, 880, lambda c: hl(c, "...e fica cada vez mais rápido", 0, 0, 62, LGREEN))


def s03(c, t):  # 24.8 - 34.96  o que você vai ver hoje
    title(c, t, 24.9, "Hoje você vai ver:", y=130, size=64)
    hero(c, t, 360, 1000, 1.15, [(0, "present")], [(0, "happy")], appear=24.9, look=1, prop=("l", prop_pointer))
    rows = [("Por que isso acontece", 25.6, qmark), ("Quanto tempo leva pra juntar R$ 100 mil", 27.5, clock),
            ("O momento em que o dinheiro trabalha mais que você", 30.6, gear)]
    for i, (lab, t0, ic) in enumerate(rows):
        y = 340 + i * 210
        show(c, t, t0, 760, y, sc(ic, s=0.55) if ic is not qmark else lambda c: qmark(c, 90, BLUE))
        show(c, t, t0 + 0.15, 860, y, lambda c, lab=lab: text(c, lab, 0, 0, 52, HAND, INK, align="l"), anim="left")
    if t > 32.8:
        show(c, t, 32.8, 1230, 930, lambda c: hl(c, "o ponto de virada", 0, 0, 54, LYELLOW), anim="up")


def s04(c, t):  # 34.96 - 45.4  as regras da conta
    show(c, t, 35.0, 960, 120, lambda c: ribbon(c, "AS REGRAS DA CONTA", NAVY), anim="pop")
    other(c, t, 420, 1040, 0.9, [(0, "stand"), (39.2, "hips")], [(0, "happy")], appear=37.8, look=0.5, shirt=ORANGE)
    show(c, t, 39.2, 420, 300, group(sc(bills, 3, s=1.0), at(0, 120, M("R$ 5.000", 62, GREEN)), at(0, 180, T("de salário por mês", 42))))
    show(c, t, 41.3, 960, 560, group(sc(piggy, s=1.1), at(0, 150, T("guarda uma parte", 46))))
    arrow_draw(c, t, 44.2, 1110, 560, 1320, 560)
    show(c, t, 44.4, 1560, 540, group(sc(prop_tablet, 0, None, s=3.2), at(0, 250, T("e investe", 46))))


def s05(c, t):  # 45.4 - 64.8  0,8% ao mês
    title(c, t, 45.5, "Pra simplificar:", y=120, size=60)
    hero(c, t, 300, 1000, 1.1, [(0, "stand"), (48.6, "present"), (61.9, "shrug")],
         [(0, "neutral"), (48.6, "confident"), (61.9, "think")], appear=45.5, look=1, prop=("l", prop_calculator))
    show(c, t, 48.7, 960, 330, lambda c: text(c, "0,8% ao mês", 0, 0, 120, MARKER, GREEN), anim="stamp")
    show(c, t, 51.0, 960, 445, T("(já descontado o imposto)", 48, DGRAY), anim="up")
    show(c, t, 53.5, 960, 560, lambda c: hl(c, "uns 10% ao ano", 0, 0, 66, LGREEN))
    show(c, t, 55.6, 1520, 640, group(at(0, 0, T("renda fixa hoje:", 44)), at(0, 60, M("paga um pouco mais", 42, BLUE))), anim="up")
    show(c, t, 59.6, 900, 760, lambda c: hl(c, "número pé no chão", 0, 0, 56, LYELLOW))
    if t > 62.0:
        show(c, t, 62.0, 1520, 880, group(lambda c: arrow(c, -60, 40, -60, -60, GREEN, 9, 0, 24),
                                          lambda c: arrow(c, 60, -60, 60, 40, RED, 9, 0, 24),
                                          at(0, 110, T("juros sobem e descem", 44))), anim="fade")


def s06(c, t):  # 64.8 - 74.04  detalhe honesto
    title(c, t, 64.9, "Um detalhe honesto", y=120, size=64)
    hero(c, t, 1550, 1000, 1.15, [(0, "stand"), (66.3, "finger_up"), (72.2, "thumb")],
         [(0, "neutral"), (66.3, "confident"), (72.2, "grin")], appear=64.9, look=-1)
    show(c, t, 66.5, 700, 330, lambda c: hl(c, "sem descontar a inflação", 0, 0, 62, PINKISH))
    show(c, t, 69.1, 600, 560, group(sc(x_icon, 44), at(330, 0, T("prever o futuro", 56))))
    show(c, t, 72.2, 600, 760, group(sc(check_icon, 44), at(400, 0, T("entender o mecanismo", 56))))
    show(c, t, 72.8, 1340, 760, sc(gear, 50, GOLD, s=1.0), rot=t * 0.8)


def s07(c, t):  # 74.04 - 87.6  juros compostos: mês 1
    show(c, t, 76.0, 960, 130, lambda c: hl(c, "JUROS COMPOSTOS", 0, 0, 76, LYELLOW), anim="stamp")
    hero(c, t, 300, 1000, 1.1, [(0, "stand"), (78.8, "present"), (86.2, "shrug")],
         [(0, "happy"), (78.8, "confident"), (86.2, "worried")], appear=74.1, look=1)
    show(c, t, 78.9, 960, 300, M("1º mês", 64))
    show(c, t, 80.5, 820, 560, group(sc(bills, 3, s=1.1), at(0, 130, M("R$ 1.000", 58, NAVY))))
    show(c, t, 81.7, 1140, 560, lambda c: text(c, "x 0,8%", 0, 0, 60, MARKER, DGRAY), anim="left")
    show(c, t, 85.0, 1500, 560, lambda c: text(c, "+ R$ 8", 0, 0, 96, MARKER, GREEN), anim="stamp")
    show(c, t, 86.3, 1500, 720, T("parece piada...", 52, RED), anim="up")


def s08(c, t):  # 87.6 - 96.2  mês 2
    hero(c, t, 300, 1000, 1.1, [(0, "present")], [(0, "happy")], appear=87.7, look=1)
    show(c, t, 87.8, 960, 300, M("2º mês", 64))
    show(c, t, 89.4, 760, 560, group(sc(bills, 3, s=0.9), at(0, 110, T("+ R$ 1.000", 48))))
    show(c, t, 91.1, 1110, 560, lambda c: text(c, "R$ 2.008", 0, 0, 74, MARKER, NAVY), anim="pop")
    show(c, t, 94.6, 1550, 560, lambda c: text(c, "+ R$ 16", 0, 0, 96, MARKER, GREEN), anim="stamp")


def s09(c, t):  # 96.2 - 111.0  fim do 1º ano: desanimador
    title(c, t, 96.3, "Depois de 1 ano", y=120, size=64)
    gbar(c, t, 98.4, 640, 860, 480, 240, NAVY, "do seu bolso", "R$ 12.000", 48)
    gbar(c, t, 101.8, 980, 860, 22, 240, GREEN, "juros", "R$ 540", 48)
    hero(c, t, 1500, 1000, 1.1, [(0, "stand"), (103.8, "head")], [(0, "neutral"), (103.8, "sad")], appear=96.3, look=-1)
    show(c, t, 103.9, 1500, 380, lambda c: hl(c, "Desanimador...", 0, 0, 58, PINKISH))
    if t > 105.3:
        other(c, t, 1180, 1000, 0.8, [(0, "shrug")], [(0, "worried")], appear=105.3, shirt=ORANGE)
        show(c, t, 106.2, 1200, 520, lambda c: speech(c, 470, 150, -60, 110), anim="pop")
        show(c, t, 109.0, 1200, 520, T("investir não vale a pena", 44), anim="fade")


def s10(c, t):  # 111.0 - 126.0  bola de neve
    title(c, t, 111.1, "Uma bola de neve descendo a montanha", y=110, size=58)
    poly(c, [(0, 330), (1920, 1000), (0, 1000)])
    fs(c, (0.93, 0.96, 1.0), 6)
    if t >= 112.9:
        u = clamp01((t - 112.9) / 13.0)
        x = 180 + u * 1450
        yline = 330 + (x / 1920) * 670
        r = 30 + 150 * (u ** 2.2)
        c.save(); c.translate(x, yline - r - 3); c.rotate(t * 2.2); snowball(c, r); c.restore()
    show(c, t, 115.3, 820, 270, lambda c: hl(c, "no começo: pequena e devagar", 0, 0, 50, LBLUE))
    show(c, t, 118.2, 820, 370, lambda c: hl(c, "cada volta: mais neve", 0, 0, 50, LYELLOW))
    show(c, t, 121.6, 820, 470, lambda c: hl(c, "quanto maior, mais rápido cresce", 0, 0, 50, LGREEN))
    hero(c, t, 260, 1000, 0.85, [(0, "point_r")], [(0, "happy"), (121.6, "shocked")], appear=111.2, look=1)


def split_scene(c, t, head, val_t, val, mon_t, sub_t, colchao, inv_t, inv):
    """cenário: colchão x investindo"""
    show(c, t, head[1], 960, 120, lambda c: ribbon(c, head[0], NAVY), anim="pop")
    show(c, t, val_t, 960, 230, M(val, 56, GREEN), anim="up")
    line(c, 960, 300, 960, 1040, 5, LGRAY)
    show(c, t, mon_t, 480, 470, group(sc(mattress, s=1.1), at(0, -130, T("debaixo do colchão", 46))))
    show(c, t, sub_t, 480, 720, lambda c: text(c, colchao[0], 0, 0, colchao[2], MARKER, RED), anim="stamp")
    if colchao[1]:
        show(c, t, colchao[3], 480, 830, lambda c: hl(c, colchao[1], 0, 0, 52, PINKISH))
    show(c, t, inv_t, 1440, 470, group(sc(prop_tablet, 0, None, s=3.0), at(0, -200, T("investindo", 46))))
    show(c, t, inv_t + 1.2, 1440, 720, lambda c: text(c, inv, 0, 0, 90, MARKER, GREEN), anim="stamp")


def s11(c, t):  # 126.0 - 145.8  cenário 10%
    split_scene(c, t, ("CENÁRIO 1: GUARDANDO 10%", 127.9), 131.2, "R$ 500 por mês", 135.2, 137.7,
                ("200 meses", "quase 17 anos", 84, 140.7), 142.6, "10 anos")


def s12(c, t):  # 145.8 - 157.68  divisão 60/40
    title(c, t, 145.9, "Dos R$ 100 mil...", y=120, size=64)
    show(c, t, 147.2, 620, 580, lambda c: donut(c, 1.0, 230, 90, NAVY), anim="pop")
    if t > 150.7:
        k = grow(t, 150.7, 1.0)
        c.save(); c.translate(620, 580)
        c.new_sub_path(); c.arc(0, 0, 230, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 0.4 * k)
        rgb(c, GREEN); c.set_line_width(84); c.set_line_cap(cairo.LINE_CAP_BUTT); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.restore()
    show(c, t, 148.3, 1300, 420, group(at(-200, 0, lambda c: circle(c, 0, 0, 26, NAVY, 5)),
                                       at(60, 0, T("R$ 60 mil do seu bolso", 54))), anim="left")
    show(c, t, 151.1, 1300, 560, group(at(-200, 0, lambda c: circle(c, 0, 0, 26, GREEN, 5)),
                                       at(60, 0, T("R$ 40 mil de juros", 54))), anim="left")
    show(c, t, 153.3, 1300, 800, lambda c: hl(c, "7 anos de vida a menos!", 0, 0, 60, LGREEN))
    hero(c, t, 1720, 1030, 0.75, [(0, "stand"), (153.3, "arms_up")], [(0, "happy"), (153.3, "grin")], appear=146.0)


# ======================================================================= BLOCO 2
def s13(c, t):  # 157.68 - 170.96  cenário 20%
    split_scene(c, t, ("CENÁRIO 2: GUARDANDO 20%", 157.8), 161.1, "R$ 1.000 por mês", 162.6, 164.0,
                ("100 meses", "8 anos e 4 meses", 84, 165.2), 167.4, "6 anos e 2 m")


def s14(c, t):  # 170.96 - 182.16  cenário 30%
    split_scene(c, t, ("CENÁRIO 3: GUARDANDO 30%", 171.0), 174.0, "R$ 1.500 por mês", 176.0, 177.1,
                ("5 anos e 7 m", None, 84, 0), 179.3, "4 anos e meio")


def s15(c, t):  # 182.16 - 190.56  10 -> 20 corta quase pela metade
    title(c, t, 182.2, "Repara numa coisa", y=120, size=64)
    base = 900
    gbar(c, t, 182.6, 560, base, 480, 200, NAVY, "guardando 10%", "10 anos", 46)
    gbar(c, t, 183.0, 960, base, 296, 200, BLUE, "guardando 20%", "6 anos", 46)
    gbar(c, t, 183.4, 1360, base, 216, 200, GREEN, "guardando 30%", "4,5 anos", 46)
    arrow_draw(c, t, 186.3, 660, 400, 860, 560, col=RED)
    show(c, t, 189.0, 1350, 330, lambda c: hl(c, "quase pela metade!", 0, 0, 58, LYELLOW))
    hero(c, t, 1730, 1010, 0.85, [(0, "point_l")], [(0, "shocked")], appear=182.3, look=-1)


def s16(c, t):  # 190.56 - 198.56  nenhum investimento faz isso
    title(c, t, 190.6, "Nenhum investimento faz isso por você", y=120, size=58)
    items = [("ação milagrosa", 193.8, 440, coin), ("criptomoeda", 195.4, 960, coin), ("curso de trader", 196.9, 1480, bulb)]
    for lab, t0, x, ic in items:
        show(c, t, t0, x, 400, group(sc(ic, s=1.1), at(0, 160, T(lab, 50))))
        show(c, t, t0 + 0.3, x, 400, lambda c: big_x(c, 110), anim="stamp")
    hero(c, t, 960, 1050, 0.7, [(0, "finger_up")], [(0, "confident")], appear=190.7)


def s17(c, t):  # 198.56 - 209.52  1º motor: o aporte
    show(c, t, 198.6, 960, 130, lambda c: hl(c, "1º MOTOR DA RIQUEZA", 0, 0, 70, LYELLOW), anim="stamp")
    show(c, t, 199.0, 380, 420, sc(gear, 120, NAVY), rot=(t - 199) * 0.6)
    show(c, t, 200.5, 960, 330, lambda c: text(c, "o APORTE", 0, 0, 100, MARKER, NAVY), anim="stamp")
    show(c, t, 201.5, 960, 450, T("quanto você coloca todo mês", 56), anim="up")
    if t > 203.9:
        u = clamp01((t - 203.9) / 5.5)
        x = 760 + u * 380
        c.save(); c.translate(x + 230, 905); c.rotate(u * 5); snowball(c, 85); c.restore()
        hero(c, t, x, 1000, 1.0, [(0, "present")], [(0, "confident")], appear=203.9, look=1)
    show(c, t, 207.5, 1560, 470, lambda c: hl(c, "quem empurra é você", 0, 0, 56, LGREEN))


def s18(c, t):  # 209.52 - 230.16  100 mil rendem 800 sozinhos
    title(c, t, 209.6, "Agora a parte bonita", y=120, size=64)
    show(c, t, 211.6, 480, 340, group(sc(calendar, "6", s=1.0), at(0, 130, T("6 anos e 2 meses", 46))))
    show(c, t, 214.5, 480, 660, lambda c: price_tag(c, "R$ 100.000", GREEN, 52, WHITE))
    if t > 218.2:
        show(c, t, 218.2, 480, 820, T("difícil, com disciplina", 46, DGRAY), anim="up")
    show(c, t, 222.8, 1180, 380, group(sc(piggy, GOLD, s=1.0), at(0, 140, T("sozinhos, rendem", 50))))
    show(c, t, 225.6, 1180, 650, lambda c: text(c, "R$ 800/mês", 0, 0, 92, MARKER, GREEN), anim="stamp")
    show(c, t, 227.6, 1180, 800, lambda c: hl(c, "quase o que você guarda!", 0, 0, 52, LYELLOW))
    hero(c, t, 1700, 1010, 1.0, [(0, "stand"), (220.6, "point_l"), (227.6, "arms_up")],
         [(0, "happy"), (220.6, "think"), (225.6, "shocked"), (227.6, "grin")], appear=209.7, look=-1)


def s19(c, t):  # 230.16 - 238.0  dois motores
    title(c, t, 230.2, "Dois motores empurrando a bola", y=120, size=62)
    show(c, t, 230.6, 960, 640, sc(snowball, 150), rot=t * 0.9)
    show(c, t, 233.5, 420, 520, group(sc(gear, 110, NAVY), at(0, 180, M("Você", 56, NAVY)), at(0, 245, T("R$ 1.000", 50))), rot=0)
    show(c, t, 235.6, 1500, 520, group(sc(gear, 110, GREEN), at(0, 180, M("O dinheiro", 56, GREEN)), at(0, 245, T("R$ 800", 50))))
    arrow_draw(c, t, 234.0, 560, 640, 780, 640)
    arrow_draw(c, t, 236.0, 1360, 640, 1140, 640)


def s20(c, t):  # 238.0 - 252.4  escada: cada bloco mais rápido
    title(c, t, 238.0, "Guardando os mesmos R$ 1.000", y=110, size=58)
    base = 900
    gbar(c, t, 238.2, 480, base, 150, 280, NAVY, "1º R$ 100 mil", "6a 2m", 46)
    gbar(c, t, 241.2, 860, base, 300, 280, BLUE, "2º R$ 100 mil", "3a 10m", 46)
    gbar(c, t, 244.1, 1240, base, 450, 280, GREEN, "3º R$ 100 mil", "2a 10m", 46)
    show(c, t, 246.3, 680, 240, T("você não mudou nada", 48), anim="up")
    show(c, t, 250.4, 680, 330, lambda c: hl(c, "quem acelerou foi o dinheiro", 0, 0, 52, LGREEN))
    hero(c, t, 1700, 900, 0.85, [(0, "present_l"), (250.4, "arms_up")], [(0, "happy"), (250.4, "grin")], appear=238.3, look=-1)


def s21(c, t):  # 252.4 - 262.32  ponto de virada
    hero(c, t, 400, 1000, 1.2, [(0, "stand"), (252.6, "finger_up")], [(0, "neutral"), (252.6, "confident")], appear=252.5, look=1)
    show(c, t, 257.1, 1150, 360, lambda c: ribbon(c, "PONTO DE VIRADA", GOLD, 76, INK), anim="stamp")
    show(c, t, 258.5, 1150, 560, T("o mês em que os juros", 58), anim="up")
    show(c, t, 259.4, 1150, 650, T("rendem mais do que você guarda", 58), anim="up")


def s22(c, t):  # 262.32 - 287.56  juros = aporte em 125 mil; 7 anos e 3 meses
    title(c, t, 262.4, "No nosso cenário...", y=110, size=58)
    show(c, t, 265.6, 960, 230, lambda c: price_tag(c, "patrimônio: R$ 125.000", GREEN, 50, WHITE))
    base = 880
    gbar(c, t, 266.0, 620, base, 380, 230, NAVY, "você guarda", "R$ 1.000", 46)
    # barra dos juros: chega a 1.000 em 270 e passa depois de 273.5
    if t >= 266.6:
        hj = 380 * grow(t, 266.6, 3.4) + 140 * grow(t, 273.6, 2.0)
        top = "R$ 1.000" if t < 273.6 else "mais!"
        c.save(); c.translate(1000, base); bar(c, hj, 230, GREEN, "juros do mês", top if t >= 270.0 else None, 46); c.restore()
    show(c, t, 271.1, 810, 560, sc(eq, 40), t1=273.5)
    show(c, t, 273.6, 810, 560, lambda c: text(c, "<", 0, 0, 90, MARKER, RED))
    show(c, t, 279.8, 1520, 420, group(sc(calendar, "7", s=1.0), at(0, 130, T("7 anos e 3 meses", 48))))
    show(c, t, 282.8, 1520, 680, lambda c: hl(c, "7 anos de esforço", 0, 0, 52, PINKISH))
    show(c, t, 285.4, 1520, 800, lambda c: hl(c, "depois, o jogo vira", 0, 0, 52, LGREEN))


def s23(c, t):  # 287.56 - 297.24  até 1 milhão
    title(c, t, 287.6, "E se fosse até R$ 1 milhão?", y=110, size=62)
    axes(c, 300, 900, 1100, 560)
    curve(c, t, 291.3, 300, 900, 1100, 560, d=4.4)
    show(c, t, 291.4, 760, 300, T("R$ 1.000 por mês...", 50), anim="up")
    if t > 295.8:
        show(c, t, 295.8, 1400, 340, lambda c: price_tag(c, "R$ 1 milhão", GOLD, 52))
        show(c, t, 296.0, 1400, 960, M("23 anos", 60, NAVY), anim="up")
    hero(c, t, 1720, 1010, 0.9, [(0, "think"), (295.8, "point_l")], [(0, "think"), (295.8, "shocked")], appear=287.7, look=-1)


def s24(c, t):  # 297.24 - 314.44  72% foi juros
    title(c, t, 297.3, "A parte que assusta", y=110, size=64)
    show(c, t, 298.0, 600, 580, lambda c: donut(c, 0.276, 240, 92, NAVY), anim="pop")
    if t > 303.8:
        k = grow(t, 303.8, 1.2)
        c.save(); c.translate(600, 580)
        c.new_sub_path(); c.arc(0, 0, 240, -math.pi / 2 + 2 * math.pi * 0.276, -math.pi / 2 + 2 * math.pi * (0.276 + 0.724 * k))
        rgb(c, GREEN); c.set_line_width(86); c.set_line_cap(cairo.LINE_CAP_BUTT); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.restore()
    show(c, t, 301.0, 1300, 380, group(at(-260, 0, lambda c: circle(c, 0, 0, 26, NAVY, 5)),
                                       at(40, 0, T("do seu bolso: R$ 276 mil", 52))), anim="left")
    show(c, t, 303.8, 1300, 500, group(at(-260, 0, lambda c: circle(c, 0, 0, 26, GREEN, 5)),
                                       at(40, 0, T("juros: R$ 724 mil", 52))), anim="left")
    show(c, t, 307.2, 600, 580, lambda c: text(c, "72%", 0, 0, 96, MARKER, GREEN), anim="stamp")
    show(c, t, 307.4, 1300, 680, lambda c: hl(c, "o dinheiro trabalhando", 0, 0, 58, LGREEN))
    show(c, t, 311.4, 1300, 820, lambda c: text(c, "Não você.", 0, 0, 70, MARKER, NAVY), anim="stamp")


def s25(c, t):  # 314.44 - 322.08  25 -> 48 anos
    line(c, 260, 600, 1660, 600, 8, INK)
    show(c, t, 314.5, 300, 600, group(lambda c: circle(c, 0, 0, 26, NAVY, 5), at(0, -90, M("25 anos", 54))))
    if t > 314.6:
        k = grow(t, 314.6, 2.0)
        line(c, 300, 600, 300 + 1320 * k, 600, 14, GREEN)
    show(c, t, 316.4, 1620, 600, group(lambda c: circle(c, 0, 0, 26, GOLD, 5), at(0, -90, M("48 anos", 54)),
                                       at(0, 120, lambda c: price_tag(c, "R$ 1 milhão", GOLD, 50))))
    show(c, t, 319.1, 960, 880, lambda c: hl(c, "guardando R$ 1.000 por mês", 0, 0, 58, LYELLOW))
    hero(c, t, 960, 520, 0.7, [(0, "arms_up")], [(0, "grin")], appear=314.5)


# ======================================================================= BLOCO 3 (Ana x Bruno)
def s26(c, t):  # 322.08 - 330.48  o ingrediente: tempo
    show(c, t, 322.2, 960, 160, T("o ingrediente que ninguém compra depois:", 58), anim="up")
    show(c, t, 326.3, 960, 450, group(sc(clock, t, s=1.4), at(0, 210, M("O TEMPO", 80, NAVY))))
    hero(c, t, 360, 1000, 1.1, [(0, "think"), (326.3, "present")], [(0, "think"), (326.3, "confident")], appear=322.2, look=1)
    if t > 327.7:
        ana(c, t, 1380, 1000, 0.9, [(0, "wave")], [(0, "happy")], appear=327.8, look=-0.5)
        bruno(c, t, 1640, 1000, 0.9, [(0, "stand")], [(0, "happy")], appear=328.1, look=-0.5)


def s27(c, t):  # 330.48 - 346.8  Ana
    show(c, t, 330.5, 960, 110, lambda c: hl(c, "A ANA", 0, 0, 72, PINK), anim="stamp")
    ana(c, t, 330, 1000, 1.1, [(0, "wave"), (333.1, "present"), (337.5, "hips"), (344.5, "thumb")],
        [(0, "happy"), (333.1, "confident"), (337.5, "happy")], appear=330.5, look=1)
    show(c, t, 330.9, 760, 300, M("começou aos 25", 56))
    show(c, t, 333.2, 1080, 470, lambda c: hl(c, "R$ 1.000/mês por 10 anos", 0, 0, 58, LGREEN))
    show(c, t, 337.5, 1080, 600, group(sc(x_icon, 36), at(260, 0, T("aos 35, parou", 54))))
    show(c, t, 340.9, 1080, 720, group(sc(prop_tablet, 0, None, s=1.6), at(260, 0, T("deixou rendendo", 54))))
    show(c, t, 344.5, 1260, 900, lambda c: price_tag(c, "do bolso: R$ 120 mil", NAVY, 50, WHITE))


def s28(c, t):  # 346.8 - 365.84  Bruno
    show(c, t, 346.9, 960, 110, lambda c: hl(c, "O BRUNO", 0, 0, 72, ORANGE), anim="stamp")
    bruno(c, t, 330, 1000, 1.1, [(0, "shrug"), (349.2, "stand"), (353.8, "hips"), (360.9, "present")],
          [(0, "happy"), (349.2, "neutral"), (353.8, "confident")], appear=346.9, look=1)
    show(c, t, 347.4, 760, 300, T("\"ainda é cedo...\"", 54, DGRAY))
    show(c, t, 349.2, 1080, 440, M("começou aos 35", 56))
    show(c, t, 353.9, 1080, 560, group(sc(check_icon, 36), at(260, 0, T("não parou", 54))))
    show(c, t, 355.4, 1080, 680, lambda c: hl(c, "30 anos, até os 65", 0, 0, 58, LYELLOW))
    show(c, t, 360.9, 1260, 850, lambda c: price_tag(c, "do bolso: R$ 360 mil", NAVY, 50, WHITE))
    show(c, t, 363.8, 1260, 970, lambda c: text(c, "3x mais que a Ana", 0, 0, 52, MARKER, RED), anim="up")


def s29(c, t):  # 365.84 - 385.68  aos 65 anos
    title(c, t, 365.9, "Aos 65 anos, quem tem mais?", y=110, size=62)
    base = 880
    gbar(c, t, 368.0, 760, base, 330, 260, ORANGE, "Bruno", None, 52)
    show(c, t, 370.9, 760, base - 390, lambda c: text(c, "R$ 2,08 mi", 0, 0, 62, MARKER, INK), anim="pop")
    gbar(c, t, 375.0, 1160, base, 560, 260, PINK, "Ana", None, 52)
    show(c, t, 378.5, 1160, base - 620, lambda c: text(c, "R$ 3,5 mi", 0, 0, 68, MARKER, GREEN), anim="stamp")
    bruno(c, t, 300, 1000, 0.85, [(0, "stand"), (378.5, "head")], [(0, "happy"), (378.5, "shocked")], appear=366.0, look=1)
    ana(c, t, 1700, 1000, 0.85, [(0, "stand"), (378.5, "arms_up")], [(0, "happy"), (378.5, "grin")], appear=366.0, look=-1)
    show(c, t, 380.2, 1560, 300, T("colocou 3x menos", 46), anim="up")
    show(c, t, 383.6, 1560, 400, lambda c: hl(c, "+ quase R$ 1,5 mi", 0, 0, 50, LGREEN))


def s30(c, t):  # 385.68 - 394.71  a diferença foi o tempo
    title(c, t, 385.7, "A diferença entre os dois", y=120, size=62)
    show(c, t, 385.9, 640, 380, group(sc(x_icon, 40), at(220, 0, T("o salário", 58))))
    show(c, t, 386.6, 640, 520, group(sc(x_icon, 40), at(260, 0, T("o investimento", 58))))
    show(c, t, 389.8, 820, 720, group(sc(check_icon, 44), at(360, 0, M("10 anos a mais", 66, GREEN))))
    show(c, t, 390.0, 1560, 520, sc(clock, t, s=1.3))
    hero(c, t, 300, 1010, 0.9, [(0, "finger_up")], [(0, "confident")], appear=385.8, look=1)


# ======================================================================= BLOCO 4
def s31(c, t):  # 394.71 - 416.02  por que desistem
    title(c, t, 394.8, "Por que tão pouca gente chega lá?", y=110, size=60)
    show(c, t, 397.7, 960, 220, lambda c: hl(c, "desistem na fase mais lenta", 0, 0, 54, PINKISH))
    other(c, t, 420, 1000, 1.05, [(0, "hold"), (408.4, "think"), (414.7, "shrug")],
          [(0, "neutral"), (404.7, "sad"), (408.4, "think"), (414.7, "desperate")], appear=401.9, shirt=ORANGE, look=0.6)
    show(c, t, 404.7, 730, 700, group(sc(document, "EXTRATO", BLUE, 30, s=1.0), at(0, 30, M("+ R$ 40", 34, GREEN))))
    show(c, t, 408.5, 900, 420, lambda c: thought(c, 560, 200, -260, 140))
    show(c, t, 408.8, 900, 420, T("pra que tanto sacrifício?", 46), anim="fade")
    tempt = [("viagem", 411.8, 1180, lambda c: card(c, BLUE)), ("celular novo", 412.7, 1450, lambda c: card(c, PURPLE)),
             ("carro", 414.0, 1720, lambda c: car(c, RED))]
    for lab, t0, x, ic in tempt:
        show(c, t, t0, x, 720, group(sc(ic, s=0.7), at(0, 110, T(lab, 44))))
    if t > 414.7:
        for i in range(4):
            ph = ((t - 414.7) * 0.7 + i * 0.25) % 1.0
            x = 520 + ph * 900 + i * 40
            y = 640 - ph * 380 + math.sin(ph * 6 + i) * 30
            c.save(); c.translate(x, y); c.rotate(ph * 4 + i); c.scale(0.45, 0.45)
            c.push_group(); bill(c); c.pop_group_to_source(); c.paint_with_alpha(1 - ph)
            c.restore()


def s32(c, t):  # 416.02 - 422.47  a parte boa da curva vem depois
    axes(c, 260, 900, 1300, 600)
    curve(c, t, 416.1, 260, 900, 1300, 600, d=3.0, power=3.6)
    show(c, t, 416.6, 1280, 330, lambda c: hl(c, "a parte boa vem depois", 0, 0, 52, LGREEN))
    show(c, t, 419.6, 560, 760, lambda c: hl(c, "a parte chata", 0, 0, 50, PINKISH))
    hero(c, t, 1730, 1010, 0.85, [(0, "point_l")], [(0, "confident")], appear=416.1, look=-1)


def s33(c, t):  # 422.47 - 429.95  plantar uma árvore
    title(c, t, 422.5, "É como plantar uma árvore", y=110, size=62)
    k = 0.1 if t < 425.0 else 0.1 + 0.9 * grow(t, 425.0, 4.0)
    c.save(); c.translate(1100, 960); tree(c, k); c.restore()
    show(c, t, 424.0, 1100, 1030, T("nos primeiros anos, parece que nada acontece", 46, DGRAY), t1=426.6)
    show(c, t, 426.8, 1320, 270, lambda c: hl(c, "ninguém arranca antes do fruto", 0, 0, 46, LYELLOW))
    hero(c, t, 400, 1000, 1.0, [(0, "stand"), (424.0, "think"), (426.8, "present")],
         [(0, "happy"), (424.0, "think"), (426.8, "grin")], appear=422.6, look=1)


def tip(c, t, t0, num, head, col):
    show(c, t, t0, 960, 130, lambda c: hl(c, f"{num}. {head}", 0, 0, 72, col), anim="stamp")


def s34(c, t):  # 429.95 - 444.63  1. comece agora
    if t < 434.4:
        title(c, t, 430.0, "Como atravessar essa fase?", y=300, size=70)
        show(c, t, 432.5, 960, 480, M("3 atitudes práticas", 64, NAVY), anim="up")
    else:
        tip(c, t, 434.4, 1, "Comece agora", LGREEN)
        show(c, t, 435.0, 700, 450, lambda c: tree(c, 0.05), s=1.6)
        show(c, t, 437.0, 1200, 380, T("mesmo que seja pouco", 56), anim="up")
        show(c, t, 439.3, 1200, 520, group(at(-180, 0, M("R$ 1.000", 56, GRAY)),
                                           at(-180, 0, lambda c: line(c, -130, 0, 130, 0, 8, RED)),
                                           at(180, 0, M("R$ 200", 64, GREEN))))
        show(c, t, 440.2, 1200, 720, lambda c: hl(c, "tempo parado não volta", 0, 0, 54, PINKISH))
        hero(c, t, 300, 1010, 0.95, [(0, "point_r")], [(0, "confident")], appear=434.5, look=1, prop=("l", prop_coin))


def s35(c, t):  # 444.63 - 456.63  2. aumente o percentual
    tip(c, t, 444.7, 2, "Aumente o percentual", LYELLOW)
    show(c, t, 448.4, 960, 360, M("ganhou + R$ 500?", 64), anim="up")
    show(c, t, 450.2, 760, 500, group(sc(prop_tablet, 0, None, s=2.0), at(420, 0, T("metade vai pro investimento", 52))))
    show(c, t, 452.0, 960, 720, lambda c: hl(c, "10% -> 20%  =  anos a menos", 0, 0, 58, LGREEN))
    hero(c, t, 300, 1010, 0.95, [(0, "finger_up"), (452.0, "thumb")], [(0, "confident"), (452.0, "grin")], appear=444.8, look=1)


def s36(c, t):  # 456.63 - 468.59  3. no automático
    tip(c, t, 456.7, 3, "Deixe no automático", LBLUE)
    show(c, t, 459.1, 620, 450, group(sc(calendar, "5", GREEN, s=1.2), at(0, 160, T("dia do pagamento", 48))))
    arrow_draw(c, t, 459.8, 820, 450, 1080, 450)
    show(c, t, 460.2, 1300, 450, group(sc(piggy, s=1.0), at(0, 140, T("transferência automática", 48))))
    show(c, t, 463.4, 960, 760, T("não dependa da força de vontade...", 52), anim="up")
    show(c, t, 466.1, 960, 880, lambda c: hl(c, "fim do mês: sobra R$ 0", 0, 0, 56, PINKISH))
    hero(c, t, 1720, 1010, 0.9, [(0, "present_l"), (466.1, "shrug")], [(0, "happy"), (466.1, "worried")], appear=456.8, look=-1)


def s37(c, t):  # 468.59 - 481.67  bônus: reserva de emergência
    show(c, t, 468.7, 960, 130, lambda c: ribbon(c, "BÔNUS", GOLD, 64, INK), anim="stamp")
    show(c, t, 472.2, 960, 260, M("reserva de emergência", 66, NAVY), anim="up")
    show(c, t, 472.6, 620, 560, sc(shield, NAVY, s=1.6))
    show(c, t, 473.6, 1220, 490, group(sc(check_icon, 32), at(200, 0, T("conservador", 50))))
    show(c, t, 474.6, 1220, 600, group(sc(check_icon, 32), at(220, 0, T("liquidez diária", 50))))
    show(c, t, 476.8, 1100, 800, lambda c: hl(c, "não vende tudo no 1º imprevisto", 0, 0, 52, LYELLOW))
    hero(c, t, 1730, 1010, 0.85, [(0, "finger_up")], [(0, "confident")], appear=468.8, look=-1)


def s38(c, t):  # 481.67 - 495.27  recapitulando
    title(c, t, 481.7, "Recapitulando", y=110, size=66)
    base = 820
    gbar(c, t, 482.6, 460, base, 150, 220, NAVY, "1º", "o mais difícil", 40)
    gbar(c, t, 483.2, 760, base, 300, 220, BLUE, "2º", None, 40)
    gbar(c, t, 483.8, 1060, base, 450, 220, GREEN, "3º", None, 40)
    show(c, t, 485.6, 1360, 360, group(sc(gear, 50, NAVY), at(80, 0, lambda c: text(c, "começo: você", 0, 0, 50, HAND, INK, align="l"))))
    show(c, t, 488.0, 1360, 500, group(sc(gear, 50, GREEN), at(80, 0, lambda c: text(c, "depois: o dinheiro", 0, 0, 50, HAND, INK, align="l"))))
    show(c, t, 490.7, 1500, 650, lambda c: ribbon(c, "PONTO DE VIRADA", GOLD, 48, INK))
    hero(c, t, 1760, 1040, 0.62, [(0, "present_l"), (490.7, "thumb")], [(0, "happy"), (490.7, "grin")], appear=481.8, look=-1)


def s39(c, t):  # 495.27 - 503.86  comentários
    show(c, t, 495.4, 1060, 380, lambda c: speech(c, 900, 260, -330, 170), anim="pop")
    show(c, t, 495.6, 1060, 330, T("Me conta nos comentários:", 52, DGRAY), anim="fade")
    show(c, t, 497.3, 1060, 420, M("quanto você guarda por mês?", 58, NAVY), anim="fade")
    show(c, t, 499.8, 1100, 760, group(sc(calculator, "R$ ?", s=0.8), at(300, 0, T("faço a conta de alguns!", 52))))
    hero(c, t, 340, 1010, 1.1, [(0, "wave"), (499.8, "present")], [(0, "happy"), (499.8, "grin")], appear=495.4, look=1)


def s40(c, t):  # 503.86 - 511.27  vídeo do carro
    show(c, t, 503.9, 960, 140, T("pensando em trocar de carro?", 58), anim="up")
    if t > 505.9:
        show(c, t, 505.9, 1180, 540, lambda c: (rrect(c, -380, -230, 760, 460, 24), fs(c, WHITE, 7)), anim="pop")
        show(c, t, 506.2, 1180, 470, sc(car, BLUE, s=1.0))
        show(c, t, 506.5, 1180, 660, M("Quanto gastar num carro?", 44, NAVY))
    hero(c, t, 400, 1010, 1.05, [(0, "think"), (505.9, "point_r")], [(0, "think"), (505.9, "happy")], appear=504.0, look=1)


def s41(c, t):  # 511.27 - fim  assinatura
    show(c, t, 511.3, 960, 300, lambda c: text(c, "FAZ A CONTA", 0, 0, 120, MARKER, NAVY), anim="stamp")
    show(c, t, 512.6, 960, 430, lambda c: hl(c, "a gente faz a conta", 0, 0, 60, LYELLOW))
    show(c, t, 513.0, 1300, 740, sc(subscribe_btn, t > 514.6, s=1.2))
    hero(c, t, 700, 1010, 1.05, [(0, "present"), (514.2, "wave")], [(0, "happy"), (514.2, "grin")], appear=511.4, look=0.6)


SCENES = [
    (0.0, 12.8, s01), (12.8, 24.8, s02), (24.8, 34.96, s03), (34.96, 45.4, s04), (45.4, 64.8, s05),
    (64.8, 74.04, s06), (74.04, 87.6, s07), (87.6, 96.2, s08), (96.2, 111.0, s09), (111.0, 126.0, s10),
    (126.0, 145.8, s11), (145.8, 157.68, s12), (157.68, 170.96, s13), (170.96, 182.16, s14),
    (182.16, 190.56, s15), (190.56, 198.56, s16), (198.56, 209.52, s17), (209.52, 230.16, s18),
    (230.16, 238.0, s19), (238.0, 252.4, s20), (252.4, 262.32, s21), (262.32, 287.56, s22),
    (287.56, 297.24, s23), (297.24, 314.44, s24), (314.44, 322.08, s25), (322.08, 330.48, s26),
    (330.48, 346.8, s27), (346.8, 365.84, s28), (365.84, 385.68, s29), (385.68, 394.71, s30),
    (394.71, 416.02, s31), (416.02, 422.47, s32), (422.47, 429.95, s33), (429.95, 444.63, s34),
    (444.63, 456.63, s35), (456.63, 468.59, s36), (468.59, 481.67, s37), (481.67, 495.27, s38),
    (495.27, 503.86, s39), (503.86, 511.27, s40), (511.27, 999.0, s41),
]

# só toques pontuais, sem ruído: 2º bloco mais rápido, ponto de virada, 72% de juros, Ana 3,5 mi
SFX = [(241.2, "tum"), (285.4, "soft_ding"), (303.8, "tum"), (378.5, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key")
