"""POV: é 10 de janeiro e você abriu a fatura do cartão. Só TikTok: vertical nativo 1080x1920, 89,2 s.
Teste de formato POV: o bonequinho principal é VOCÊ (camiseta laranja, sentado no sofá); O Consultor só entra aos 55 s.
O texto POV fica fixo no topo durante a parte de cena (0 a 55 s).
Layout vertical (coordenadas finais, sem SHIFT): faixa POV y 170-310, palco y 360-1280 (chão em FY=1280),
legendas do tiktok.py em y~1460, abaixo de 1500 fica a interface do TikTok. Nada importante em x > 930.
Contas: fatura 700+350+280+500+270 = 2.100; IPVA 1.400 + IPTU 500 + material 400 = 2.300; janeiro 4.400;
13º da Ana (salário 3 mil) = 2.750; falta 1.650; sobra 450 se separar antes."""
import math

from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1280
YX = 330          # x do sofá / VOCÊ
POV_END = 55.1
PINKISH = (1, 0.8, 0.76)

SFX = [(36.97, "tum"), (52.66, "tum"), (69.63, "tum"), (81.31, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow",
            "appear", "key", "transition")

ITEMS = [("Presentes", "700", 8.0), ("Ceia", "350", 12.54), ("Roupa", "280", 18.87),
         ("Viagem 1/6", "500", 24.64), ("Delivery", "270", 31.88)]


# ---------------------------------------------------------------- helpers
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def pov_banner(c, t):
    """faixa fixa do POV no topo"""
    a = 1.0 if t < POV_END else 1 - prog(t, POV_END, 0.35)
    if a <= 0:
        return
    c.push_group()
    rrect(c, 50, 170, 980, 150, 22); fs(c, INK, 0)
    text(c, "POV: é 10 de janeiro e você", 540, 222, 54, MARKER, WHITE)
    text(c, "abriu a fatura do cartão", 540, 282, 54, MARKER, GOLD)
    c.pop_group_to_source(); c.paint_with_alpha(a)


YS = 0.8          # escala de VOCÊ no sofá
SOF = 1.25        # escala do sofá


def you(c, t, x, poses, exprs, s=YS, y=FY, **kw):
    """VOCÊ: pessoa comum (camiseta laranja, cabelo espetado)"""
    kw.setdefault("shirt", ORANGE); kw.setdefault("hair", "spiky"); kw.setdefault("fid", 2)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def phone_in_hand(c, x=YX, s=YS):
    """celular na mão, abaixo do queixo (pose hold)"""
    c.save(); c.translate(x, FY - 255 * s); c.scale(0.36, 0.36); phone(c); c.restore()


def on_sofa(c, t, poses, exprs, phone_on=True, x=YX, look=0.4, **kw):
    """VOCÊ sentado: encosto, boneco, frente do sofá (esconde as pernas)"""
    c.save(); c.translate(x, FY); c.scale(SOF, SOF); sofa_back(c); c.restore()
    you(c, t, x, poses, exprs, look=look, **kw)
    c.save(); c.translate(x, FY); c.scale(SOF, SOF); sofa_front(c); c.restore()
    if phone_on:
        phone_in_hand(c, x)


def fainted(c, t, t0, extra=None, x=YX):
    """VOCÊ desmaiando de costas no sofá a partir de t0 (deitado depois de 0,6 s)"""
    k = ease_io(prog(t, t0, 0.6))
    c.save(); c.translate(x, FY); c.scale(SOF, SOF); sofa_back(c); sofa_front(c); c.restore()
    c.save()
    c.translate(x + 175 * k, FY - 150 * k)
    c.rotate(-1.48 * k)
    you(c, t, 0, [(0, "relax"), (t0, "arms_up")], [(0, "desperate"), (t0 + 0.6, "shocked")], y=0, look=0)
    c.restore()
    if extra:
        extra(c, t)


def bubble(c, t, t0, x, y, s, w=420, h=120, tx=-120, ty=95, size=50, col=INK, t1=None):
    show(c, t, t0, x, y, group(lambda c: speech(c, w, h, tx, ty), T(s, size, col)), anim="pop", d=0.3, t1=t1)


def receipt(c, t, n_lines=5, w=270, total=False):
    """cartão da fatura (direita), uma linha por compra conforme a narração chega no valor"""
    h = 90 + 62 * n_lines + (90 if total else 0)
    rrect(c, -w / 2, 0, w, h, 16); fs(c, WHITE, 5)
    c.save(); rrect(c, -w / 2, 0, w, h, 16); c.clip()
    c.rectangle(-w / 2, 0, w, 66); rgb(c, NAVY); c.fill(); c.restore()
    rrect(c, -w / 2, 0, w, h, 16); rgb(c, INK); c.set_line_width(5); c.stroke()
    text(c, "FATURA", 0, 36, 40, MARKER, WHITE)
    for i, (lab, val, t0) in enumerate(ITEMS[:n_lines]):
        if t < t0:
            continue
        a = ease_out(prog(t, t0, 0.3))
        y = 105 + i * 62
        c.push_group()
        text(c, lab, -w / 2 + 16, y, 36, HAND, INK, align="l")
        text(c, val, w / 2 - 16, y, 38, MARKER, RED, align="r")
        c.pop_group_to_source(); c.paint_with_alpha(a)


def item_scene(c, t, label, t_lab, icon, val, t_val, poses, exprs, react=None, t_react=None, extra=None):
    """uma compra por cena: rótulo, ícone grande, valor depois da pausa, VOCÊ reagindo no sofá"""
    floor(c)
    pov_banner(c, t)
    show(c, t, t_lab, 335, 420, M(label, 64, INK), anim="up")
    show(c, t, t_lab + 0.1, 335, 610, icon, anim="pop")
    show(c, t, t_val, 335, 820, lambda c: hl(c, val, 0, 0, 92, PINKISH, RED), anim="stamp", d=0.35)
    show(c, t, 0, 790, 380, lambda c: receipt(c, t), anim="fade", d=0.01)
    if extra:
        extra(c, t)
    on_sofa(c, t, poses, exprs)
    if react:
        bubble(c, t, t_react, 770, 900, react, w=330, h=110, tx=-170, ty=80, size=46)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.9  dez de janeiro, abre o app, respira fundo, clica
    floor(c)
    pov_banner(c, t)
    show(c, t, 0.15, 300, 560, group(sc(calendar, "10", RED, 80, s=1.5), at(0, 150, T("janeiro", 56, RED))), anim="pop")
    # celular grande com o app do banco
    def big_phone(c):
        c.save(); c.scale(1.7, 1.7); phone(c); c.restore()
        text(c, "BANCO", 0, -90, 46, MARKER, NAVY)
        rrect(c, -70, 60, 140, 64, 14); fs(c, NAVY if t < 5.0 else GOLD, 4)
        text(c, "fatura", 0, 94, 40, HAND, WHITE if t < 5.0 else INK)
    show(c, t, 1.7, 720, 600, big_phone, anim="pop")
    show(c, t, 4.96, 760, 700, sc(cursor, s=1.3), anim="pop", d=0.25)
    show(c, t, 3.4, 640, 900, T("respira fundo...", 52, DGRAY), anim="up", t1=4.9)
    show(c, t, 4.96, 720, 900, M("CLICA.", 64, RED), anim="stamp", d=0.3)
    on_sofa(c, t, [(0, "hold")], [(0, "neutral"), (3.4, "worried"), (5.0, "shocked")], look=0.6)
    show(c, t, 0.6, 140, 980, group(T("você", 50, ORANGE), lambda c: arrow(c, 30, 20, 110, 90, ORANGE, 6)),
         anim="up", t1=4.5)


def s02(c, t):  # 5.9 - 11.4  presentes 700
    item_scene(c, t, "Presentes de Natal", 6.0, sc(gift, s=1.05), "R$ 700", 8.0,
               [(0, "hold"), (9.7, "shrug")], [(0, "worried"), (8.0, "shocked"), (9.7, "neutral")],
               "tá, era Natal", 9.7)


def s03(c, t):  # 11.4 - 16.9  ceia 350
    item_scene(c, t, "Ceia", 11.5, sc(roast, s=1.1), "R$ 350", 12.54,
               [(0, "hold"), (15.6, "hips")], [(0, "worried"), (12.6, "shocked"), (15.6, "angry")],
               "ninguém dividiu", 15.6)


def s04(c, t):  # 16.9 - 21.4  roupa do Ano Novo 280
    item_scene(c, t, "Roupa do Ano Novo", 17.0, sc(tshirt, s=1.05), "R$ 280", 18.87,
               [(0, "hold"), (20.2, "head")], [(0, "worried"), (18.9, "shocked"), (20.2, "sad")],
               "usei 1 vez...", 20.2)


def s05(c, t):  # 21.4 - 25.6  viagem parcelada 500
    def extra(c, t):
        show(c, t, 22.8, 470, 500, lambda c: hl(c, "1 de 6", 0, 0, 46, LYELLOW), anim="stamp", d=0.3)
    item_scene(c, t, "Viagem parcelada", 21.5, sc(suitcase, s=0.95), "R$ 500", 24.64,
               [(0, "hold"), (24.7, "head")], [(0, "worried"), (24.7, "desperate")],
               "e faltam 5...", 24.9, extra=extra)


def s06(c, t):  # 25.6 - 33.2  "só um lanchinho" 9 vezes = 270
    def extra(c, t):
        n = 0
        for tt, k in ((28.08, 1), (29.2, 2), (30.16, 9)):
            if t >= tt:
                n = k
        if n:
            show(c, t, 28.08, 505, 520, lambda c: text(c, f"x{n}", 0, 0, 84, MARKER, RED, outline=WHITE, ow=12),
                 anim="pop", d=0.25)
    item_scene(c, t, '"Só um lanchinho"', 25.7, sc(sandwich, s=0.95), "R$ 270", 31.88,
               [(0, "hold"), (30.2, "head")], [(0, "neutral"), (28.1, "worried"), (30.2, "shocked"), (31.9, "desperate")],
               extra=extra)


def s07(c, t):  # 33.2 - 41.2  total da fatura 2.100 e desmaio
    floor(c)
    pov_banner(c, t)
    # rola até o final: o cartão da fatura sobe e aparece a linha do total
    k = ease_io(prog(t, 33.6, 1.2))
    if k < 1:
        c.save(); c.rectangle(0, 330, W, 900); c.clip()
        c.push_group()
        c.save(); c.translate(540, 380 - 520 * k); receipt(c, t, 5, w=420); c.restore()
        c.pop_group_to_source(); c.paint_with_alpha(1 - k * k)
        c.restore()
    show(c, t, 34.93, 540, 470, M("TOTAL DA FATURA", 70, INK), anim="up")
    show(c, t, 36.97, 540, 680, lambda c: text(c, "R$ 2\u200a.100", 0, 0, 190, MARKER, RED, outline=WHITE, ow=16),
         anim="stamp", d=0.35)
    if t < 39.8:
        on_sofa(c, t, [(0, "hold"), (37.0, "head")], [(0, "worried"), (37.0, "shocked"), (38.4, "desperate")])
    else:
        fainted(c, t, 39.8)


def drop_boletos(c, t):
    """os três boletos caindo em cima de VOCÊ (deitado)"""
    for (tt, title_, col, val, x, y, r) in ((43.3, "IPVA", RED, "1.400", YX + 20, 1100, -0.25),
                                            (46.0, "IPTU", ORANGE, "500", YX + 190, 1090, 0.2),
                                            (48.1, "ESCOLA", PURPLE, "400", YX + 105, 1060, -0.05)):
        show(c, t, tt, x, y, sc(boleto, title_, col, val, s=0.55), anim="drop", d=0.5, rot=r)


def s08(c, t):  # 41.2 - 50.6  mas janeiro não acabou: IPVA, IPTU, material escolar
    floor(c)
    pov_banner(c, t)
    show(c, t, 41.3, 540, 395, M("Mas janeiro não acabou", 60, INK), anim="up")
    rows = ((43.23, 44.51, "IPVA", "R$ 1.400", lambda c: sc(car, RED, s=0.45)(c)),
            (45.99, 47.06, "IPTU", "R$ 500", lambda c: sc(house, s=0.45)(c)),
            (48.03, 49.51, "Material escolar", "R$ 400", lambda c: sc(pencil, s=0.55)(c)))
    for i, (tl, tv_, lab, val, ic) in enumerate(rows):
        y = 510 + i * 130
        show(c, t, tl, 150, y, ic, anim="pop")
        show(c, t, tl, 250, y, lambda c, lab=lab: text(c, lab, 0, 0, 56, HAND, INK, align="l"), anim="left", d=0.3)
        show(c, t, tv_, 900, y, lambda c, val=val: text(c, val, 0, 0, 64, MARKER, RED, align="r"), anim="stamp", d=0.3)
    fainted(c, t, 39.8, drop_boletos)


def s09(c, t):  # 50.6 - 55.1  janeiro inteiro 4.400
    floor(c)
    pov_banner(c, t)
    show(c, t, 50.72, 540, 395, M("Janeiro inteiro", 66, INK), anim="up")
    rows = (("fatura", "2\u200a.100"), ("IPVA", "1.400"), ("IPTU", "500"), ("escola", "400"))
    for i, (lab, val) in enumerate(rows):
        y = 490 + i * 72
        show(c, t, 50.9 + i * 0.18, 300, y, lambda c, lab=lab: text(c, lab, 0, 0, 50, HAND, INK, align="l"), anim="left", d=0.25)
        show(c, t, 50.9 + i * 0.18, 780, y, lambda c, val=val: text(c, val, 0, 0, 54, MARKER, INK, align="r"), anim="left", d=0.25)
    if t > 51.8:
        line(c, 280, 790, 280 + 520 * ease_out(prog(t, 51.8, 0.4)), 790, 7, INK)
    show(c, t, 52.66, 540, 890, lambda c: text(c, "R$ 4.400", 0, 0, 150, MARKER, RED, outline=WHITE, ow=16),
         anim="stamp", d=0.35)
    fainted(c, t, 39.8, drop_boletos)


def s10(c, t):  # 55.1 - 59.8  chega o Consultor: "E o seu 13º?"  "Já foi. Em dezembro."
    floor(c)
    pov_banner(c, t)
    hero(c, t, 790, FY, 0.66, [(0, "wave"), (56.3, "point_l")], [(0, "happy"), (56.3, "think")], appear=55.4, look=-1)
    bubble(c, t, 56.27, 700, 650, "E o seu 13º?", w=440, h=130, tx=80, ty=110, size=60, col=NAVY)
    # o 13º voando embora em dezembro
    show(c, t, 58.2, 250, 470, group(sc(calendar, "DEZ", RED, 58, s=1.1)), anim="pop")
    if t > 58.4:
        for i in range(4):
            k = prog(t, 58.5 + i * 0.25, 1.2)
            if k > 0:
                c.save(); c.translate(250 + 80 * k + i * 20, 470 - 260 * k - i * 30); c.rotate(0.3 * i - 0.4)
                c.scale(0.45, 0.45)
                c.push_group(); bill(c); c.pop_group_to_source(); c.paint_with_alpha(1 - 0.7 * k)
                c.restore()
    on_sofa(c, t, [(0, "head"), (55.6, "relax"), (58.2, "shrug")],
            [(0, "desperate"), (55.6, "worried"), (58.2, "sad")], phone_on=False, look=0.7)
    bubble(c, t, 58.19, 330, 820, "já foi... em dezembro", w=470, h=110, tx=-60, ty=95, size=48)


def s11(c, t):  # 59.8 - 71.3  13º inteiro 2.750 x janeiro 4.400: faltam 1.650
    floor(c)
    base, hmax = 1000, 540
    h13 = hmax * 2750 / 4400
    for x, h, t0, col, lab in ((330, h13, 61.95, GREEN, "seu 13º"), (680, hmax, 65.15, RED, "janeiro")):
        show(c, t, t0 - 1.6, x, base + 50, M(lab, 50, INK), anim="up")
        if t > t0:
            k = ease_out(prog(t, t0, 0.5))
            rrect(c, x - 110, base - h * k, 220, h * k, 12); fs(c, col, 6)
    show(c, t, 62.3, 330, base - h13 + 55, M("R$ 2\u200a.750", 40, WHITE), anim="pop")
    show(c, t, 65.5, 680, base - hmax - 45, M("R$ 4.400", 60, RED), anim="pop")
    # a parte de janeiro que passa do 13º
    if t > 67.0:
        k = ease_out(prog(t, 67.0, 0.5))
        c.save(); c.set_dash([20, 12]); line(c, 220, base - h13, 220 + 570 * k, base - h13, 7, INK); c.restore()
    if t > 69.15:
        k = ease_out(prog(t, 69.15, 0.4))
        rrect(c, 572, base - hmax, 216, (hmax - h13) * k, 10); rgb(c, WHITE, 0.45); c.fill()
    show(c, t, 69.63, 330, 560, group(lambda c: hl(c, "faltam", 0, -50, 52, PINKISH),
                                      lambda c: hl(c, "R$ 1.650", 0, 30, 74, PINKISH, RED)), anim="stamp", d=0.35)
    you(c, t, 120, [(0, "relax"), (69.7, "head")], [(0, "worried"), (69.7, "desperate")], s=0.62, look=1)
    hero(c, t, 900, FY, 0.62, [(0, "present_l"), (64.2, "point_l")], [(0, "neutral"), (64.2, "confident")],
         prop=("r", prop_calculator), look=-1)


def s12(c, t):  # 71.3 - 77.4  só impostos + material = 2.300: esse dinheiro já tinha dono
    floor(c)
    show(c, t, 71.4, 540, 395, M("Só os boletos de janeiro:", 58, INK), anim="up")
    for i, (tt, ti, col, val) in enumerate(((72.27, "IPVA", RED, "1.400"), (72.5, "IPTU", ORANGE, "500"),
                                             (72.99, "ESCOLA", PURPLE, "400"))):
        show(c, t, tt, 230 + i * 300, 600, sc(boleto, ti, col, val, s=0.75), anim="pop", rot=(i - 1) * 0.06)
    show(c, t, 74.15, 540, 820, lambda c: hl(c, "= R$ 2\u200a.300", 0, 0, 96, LYELLOW, INK), anim="stamp", d=0.35)
    def tag(c):
        c.save(); c.rotate(-0.12)
        w = text_w(c, "JÁ TINHA DONO", 66) + 50
        rrect(c, -w / 2, -55, w, 110, 14); fs(c, WHITE, 0); rrect(c, -w / 2, -55, w, 110, 14); rgb(c, NAVY); c.set_line_width(10); c.stroke()
        text(c, "JÁ TINHA DONO", 0, 0, 66, MARKER, NAVY)
        c.restore()
    show(c, t, 76.27, 540, 600, tag, anim="stamp", d=0.3)
    you(c, t, 180, [(0, "relax"), (76.3, "head")], [(0, "worried"), (76.3, "sad")], s=0.66, look=1)
    hero(c, t, 860, FY, 0.66, [(0, "point_lu"), (76.3, "finger_up")], [(0, "neutral"), (76.3, "confident")], look=-1)


def s13(c, t):  # 77.4 - 83.2  a regra: antes de gastar o 13º, separe o que janeiro vai cobrar
    floor(c)
    show(c, t, 77.5, 540, 400, lambda c: ribbon(c, "A REGRA", NAVY, 64), anim="stamp")
    show(c, t, 79.39, 540, 530, T("antes de gastar o 13º...", 64), anim="up")
    show(c, t, 81.31, 540, 660, lambda c: hl(c, "SEPARE o que", 0, 0, 76, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 81.6, 540, 770, lambda c: hl(c, "janeiro vai cobrar", 0, 0, 76, LYELLOW), anim="stamp", d=0.3)
    show(c, t, 82.1, 520, 920, group(sc(envelope, s=1.5), at(0, 40, M("JANEIRO", 34, NAVY))), anim="pop")
    show(c, t, 82.4, 520, 1030, lambda c: text(c, "R$ 2\u200a.300", 0, 0, 56, MARKER, GREEN), anim="pop")
    hero(c, t, 830, FY, 0.66, [(0, "present_l"), (81.3, "finger_up")], [(0, "neutral"), (81.3, "confident")],
         prop=("r", prop_pointer), look=-1)
    you(c, t, 170, [(0, "relax"), (81.4, "thumb")], [(0, "think"), (81.4, "happy")], s=0.66, look=1)


def s14(c, t):  # 83.2 - fim  marca o amigo + qual conta mais pesa
    floor(c)
    show(c, t, 83.39, 540, 400, M("Marca aquele amigo", 70, NAVY), anim="stamp", d=0.3)
    show(c, t, 84.0, 540, 490, T("que vai abrir essa fatura", 56), anim="up")
    show(c, t, 83.6, 780, 640, lambda c: text(c, "@", 0, 0, 150, MARKER, GOLD, outline=INK, ow=8), anim="pop")
    show(c, t, 85.75, 540, 790, T("Qual conta de janeiro", 62), anim="up")
    show(c, t, 86.2, 540, 870, lambda c: hl(c, "mais pesa pra você?", 0, 0, 70, PINKISH), anim="stamp", d=0.3)
    for i, (ti, col) in enumerate((("IPVA", RED), ("IPTU", ORANGE), ("ESCOLA", PURPLE))):
        show(c, t, 86.9 + i * 0.15, 360 + i * 170, 1050, sc(boleto, ti, col, None, s=0.42), anim="pop")
    show(c, t, 83.6, 300, 640, sc(card, s=0.9), anim="pop")
    you(c, t, 170, [(0, "point_r"), (85.7, "think")], [(0, "grin"), (85.7, "think")], s=0.66, look=1)
    hero(c, t, 880, FY, 0.62, [(0, "wave")], [(0, "happy")], look=-1)


SCENES = [
    (0.0, 5.9, s01), (5.9, 11.4, s02), (11.4, 16.9, s03), (16.9, 21.4, s04), (21.4, 25.6, s05),
    (25.6, 33.2, s06), (33.2, 41.2, s07), (41.2, 50.6, s08), (50.6, 55.1, s09), (55.1, 59.8, s10),
    (59.8, 71.3, s11), (71.3, 77.4, s12), (77.4, 83.2, s13), (83.2, 999.0, s14),
]
