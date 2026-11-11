"""Morar com os pais até os 30: vergonha ou estratégia? Carla x Lucas. Só TikTok: vertical nativo 1080x1920, 66,8 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: Carla paga R$ 1.200 de aluguel por 60 meses = R$ 72 mil; Lucas guarda R$ 1.000/mês por 60 meses
a ~10% a.a. (conservador), IR 15% -> ~R$ 74 mil ("mais de setenta mil")."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(26.8, "tum"), (30.6, "soft_ding"), (53.4, "tum"), (65.0, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

CARLA_COR = (0.86, 0.40, 0.36)
LUCAS_COR = ORANGE


def selo(s, cor=VERMELHO, size=64, tcol=CREME):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(-0.06)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def cartao(lab, val, cor_val=TINTA, w=600, h=104):
    def f(c):
        rr(c, -w / 2 + 6, -h / 2 + 8, w, h, 22); rgb(c, (0, 0, 0), 0.20); c.fill()
        rr(c, -w / 2, -h / 2, w, h, 22); rgb(c, (0.99, 0.99, 0.98)); c.fill()
        text(c, lab, -w / 2 + 30, 2, 46, HAND, (0.2, 0.2, 0.25), align="l")
        text(c, val, w / 2 - 26, 2, 52, MARKER, cor_val, align="r")
    return f


def check(c, x, y, ok=True, r=40):
    c.new_sub_path(); c.arc(x, y, r, 0, 6.283); rgb(c, VERDE if ok else VERMELHO); c.fill()
    c.set_line_width(r * 0.22); rgb(c, CREME)
    if ok:
        c.move_to(x - r * 0.45, y); c.line_to(x - r * 0.1, y + r * 0.38); c.line_to(x + r * 0.5, y - r * 0.38)
    else:
        c.move_to(x - r * 0.4, y - r * 0.4); c.line_to(x + r * 0.4, y + r * 0.4)
        c.move_to(x + r * 0.4, y - r * 0.4); c.line_to(x - r * 0.4, y + r * 0.4)
    c.stroke()


def casinha(c, s=1.0, cor=(0.93, 0.88, 0.78), telhado=(0.70, 0.30, 0.24)):
    """casa simples (origem = base central)"""
    c.save(); c.scale(s, s)
    rr(c, -150, -230, 300, 230, 6); rgb(c, cor); c.fill()
    c.move_to(-180, -225); c.line_to(0, -360); c.line_to(180, -225); c.close_path(); rgb(c, telhado); c.fill()
    rr(c, -40, -130, 80, 130, 6); rgb(c, (0.45, 0.30, 0.20)); c.fill()
    for dx in (-100, 100):
        rr(c, dx - 32, -190, 64, 56, 4); rgb(c, (0.98, 0.86, 0.50)); c.fill()
    c.set_line_width(6); rgb(c, TINTA)
    rr(c, -150, -230, 300, 230, 6); c.stroke()
    c.restore()


def chave(c, s=1.0):
    c.save(); c.scale(s, s); c.rotate(-0.5)
    c.new_sub_path(); c.arc(-60, 0, 38, 0, 6.283); rgb(c, GOLD); c.fill()
    c.new_sub_path(); c.arc(-60, 0, 14, 0, 6.283); rgb(c, NAVY); c.fill()
    c.rectangle(-26, -10, 110, 20); rgb(c, GOLD); c.fill()
    c.rectangle(58, 8, 14, 26); c.rectangle(80, 8, 12, 18); c.fill()
    c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.4  gancho
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "MORAR COM", 520, 250, 110, CREME)
    numero_i(c, "OS PAIS ATÉ OS 30", 520, 370, 84, CREME)
    numero_i(c, "VERGONHA?", 520, 520, 140, VERMELHO, contorno=CREME) if t < 2.9 else \
        entra(c, t, 2.9, 520, 520, selo("OU ESTRATÉGIA?", VERDE, 84, CREME), anim="stamp")
    entra(c, t, 0.6, 760, 1240, lambda c: casinha(c, 1.0), anim="up")
    consultor_i(c, t, 260, 1300, 1.4, poses=((0, "think"), (2.9, "point_r")), exprs=((0, "think"), (2.9, "confident")), look=0.6)


def s02(c, t):  # 5.4 - 8.9  dois amigos, 25 anos, mesmo salário
    cena_rua(c, t, "dia", carros=False)
    numero_i(c, "DOIS AMIGOS", 520, 240, 104, CREME)
    entra(c, t, 6.3, 520, 380, selo("25 ANOS", NAVY, 72, GOLD), anim="stamp")
    entra(c, t, 7.8, 520, 520, selo("MESMO SALÁRIO", VERDE, 60, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.35, "carla", poses=((0, "wave"), (7.8, "thumb")), exprs=((0, "happy"), (7.8, "grin")), look=0.4)
    pessoa(c, t, 790, 1300, 1.35, "lucas", poses=((0, "wave"), (7.8, "thumb")), exprs=((0, "happy"), (7.8, "grin")), look=-0.4)


def s03(c, t):  # 8.9 - 16.7  Carla sai de casa: aluguel 1.200 + luz, internet, mercado; liberdade
    cena_sala(c, t, "tarde")
    numero_i(c, "A CARLA", 520, 240, 100, GOLD)
    numero_i(c, "SAI DE CASA", 520, 350, 84, CREME) if t > 9.4 else None
    entra(c, t, 10.5, 640, 520, cartao("Aluguel", "R$ 1.200", VERMELHO, 600), anim="right")
    for i, (tt, s) in enumerate(((12.9, "+ LUZ"), (13.6, "+ INTERNET"), (14.3, "+ MERCADO"))):
        entra(c, t, tt, 640, 660 + i * 105, selo(s, ((0.25, 0.45, 0.80), NAVY, (0.55, 0.36, 0.72))[i], 50, CREME), anim="right")
    entra(c, t, 15.2, 620, 1010, selo("LIBERDADE TOTAL", VERDE, 56, CREME), anim="stamp")
    entra(c, t, 15.2, 230, 560, lambda c: chave(c, 1.0), anim="pop")
    pessoa(c, t, 230, 1300, 1.35, "carla", poses=((0, "stand"), (10.5, "present"), (15.2, "arms_up")),
           exprs=((0, "happy"), (10.5, "neutral"), (15.2, "grin")), look=0.6)




def s04(c, t):  # 16.7 - 23.2  Lucas fica com os pais: ajuda 300, guarda 1.000
    cena_cozinha(c, t, "dia")
    numero_i(c, "O LUCAS", 520, 240, 100, GOLD)
    numero_i(c, "FICA COM OS PAIS", 520, 350, 76, CREME) if t > 17.2 else None
    entra(c, t, 18.4, 600, 520, cartao("Ajuda em casa", "R$ 300", NAVY, 640), anim="right")
    entra(c, t, 20.9, 600, 650, cartao("Guarda todo mês", "R$ 1.000", VERDE, 640), anim="right")
    if t > 21.4:
        c.save(); c.translate(600, 1250); pilha_moedas(c, 6, 38, t, 21.4); c.restore()
    pessoa(c, t, 900, 1300, 1.1, "aposentado", poses=((0, "stand"), (18.4, "thumb")), exprs=((0, "happy"), (18.4, "grin")), look=-0.6)
    pessoa(c, t, 260, 1300, 1.35, "lucas", poses=((0, "stand"), (18.4, "present"), (21.1, "thumb")),
           exprs=((0, "happy"), (18.4, "neutral"), (21.1, "confident")), look=0.6, prop=("r", prop_moeda_i) if t > 21.1 else None)


def s05(c, t):  # 23.2 - 26.3  cinco anos depois, 30
    fundo_marca(c, t, "navy", holofote=(520, 1080))
    numero_i(c, "5 ANOS", 520, 260, 160, GOLD)
    numero_i(c, "DEPOIS", 520, 400, 100, CREME)
    if t > 24.8:
        contador(c, t, 24.8, 25, 30, 640, 560, 120, d=0.6, col=CREME, prefixo="", fmt=lambda v: f"{int(round(v))} ANOS")
    consultor_i(c, t, 260, 1300, 1.4, poses=((0, "present"),), exprs=((0, "neutral"),), look=0.0)


def s06(c, t):  # 26.3 - 29.5  Carla pagou 72 mil só de aluguel
    fundo_marca(c, t, "vermelho", holofote=(250, 1080))
    numero_i(c, "A CARLA PAGOU", 520, 250, 96, CREME)
    contador(c, t, 26.9, 0, 72000, 560, 450, 150, d=1.2, col=GOLD)
    entra(c, t, 28.4, 580, 620, selo("SÓ DE ALUGUEL", NAVY, 64, CREME), anim="stamp")
    for i in range(5):
        tt = 27.2 + i * 0.3
        if t < tt:
            continue
        k = ease_out(prog(t, tt, 0.8))
        c.save(); c.translate(700 + (i % 3) * 90, 1220 - k * 300 - (i // 3) * 60); c.rotate(k * 0.5)
        nota_i(c, "100", 150); c.restore()
    pessoa(c, t, 240, 1300, 1.3, "carla", poses=((0, "stand"), (28.4, "head")), exprs=((0, "neutral"), (28.4, "worried")), look=0.6)


def s07(c, t):  # 29.5 - 34.1  Lucas tem mais de 70 mil: entrada do apê
    fundo_marca(c, t, "verde", holofote=(250, 1080))
    numero_i(c, "O LUCAS TEM", 520, 250, 96, CREME)
    if t < 30.6:
        pass
    elif t < 31.6:
        contador(c, t, 30.6, 0, 70000, 560, 450, 150, d=0.9, col=GOLD)
    else:
        numero_i(c, "+ DE R$ 70 MIL", 530, 450, 104, GOLD)
    entra(c, t, 31.6, 640, 610, selo("GUARDADOS", NAVY, 60, CREME), anim="stamp")
    entra(c, t, 32.8, 640, 750, selo("ENTRADA DO APÊ", GOLD, 60, NAVY), anim="stamp")
    entra(c, t, 32.8, 800, 1240, lambda c: casinha(c, 0.75), anim="up")
    if t > 31.6:
        c.save(); c.translate(560, 1240); pilha_moedas(c, 7, 38, t, 31.6); c.restore()
    pessoa(c, t, 200, 1300, 1.35, "lucas", poses=((0, "stand"), (30.6, "arms_up")), exprs=((0, "happy"), (30.6, "grin")), look=0.6)


def s08(c, t):  # 34.1 - 37.7  ganhou de lavada? mas calma
    fundo_marca(c, t, "navy", holofote=(520, 1080))
    numero_i(c, "LUCAS GANHOU", 520, 250, 100, CREME)
    numero_i(c, "DE LAVADA?", 520, 370, 110, GOLD)
    entra(c, t, 36.7, 520, 550, selo("MAS CALMA", VERMELHO, 72, CREME), anim="stamp")
    consultor_i(c, t, 520, 1300, 1.5, poses=((0, "shrug"), (36.7, "finger_up")), exprs=((0, "think"), (36.7, "confident")), look=0.0)


def s09(c, t):  # 37.7 - 45.1  Carla aprendeu a se virar
    cena_mercado(c, t, carrinho=False)
    numero_i(c, "A CARLA APRENDEU", 520, 250, 80, CREME)
    numero_i(c, "A SE VIRAR", 520, 360, 100, GOLD) if t > 38.7 else None
    for tt, s, y in ((39.7, "Pagar conta", 520), (40.8, "Fazer mercado", 640), (42.0, "Resolver problema", 760)):
        if t > tt:
            k = ease_out(prog(t, tt, 0.35))
            c.save(); c.translate(640, y); c.scale(k, k)
            cartao(s, "", TINTA, 560, 96)(c); check(c, 220, 0, True, 34)
            c.restore()
    entra(c, t, 43.7, 680, 900, selo("ISSO TEM VALOR", VERDE, 60, CREME), anim="stamp")
    pessoa(c, t, 230, 1300, 1.35, "carla", poses=((0, "stand"), (39.7, "thumb"), (43.7, "hips")),
           exprs=((0, "neutral"), (39.7, "happy"), (43.7, "confident")), look=0.6)


def s10(c, t):  # 45.1 - 51.3  Lucas só ganha se guardar de verdade: celular, viagem, delivery
    cena_sala(c, t, "tarde")
    numero_i(c, "O LUCAS SÓ GANHA", 520, 240, 80, CREME)
    numero_i(c, "SE GUARDAR DE VERDADE", 520, 345, 64, GOLD) if t > 46.2 else None
    for i, (tt, s) in enumerate(((48.6, "CELULAR NOVO"), (49.8, "VIAGEM"), (50.5, "DELIVERY"))):
        entra(c, t, tt, 640, 520 + i * 125, selo(s, VERMELHO, 56, CREME), anim="right")
    pessoa(c, t, 240, 1300, 1.35, "lucas", poses=((0, "stand"), (48.6, "hold")), exprs=((0, "neutral"), (48.6, "happy")),
           look=0.6, prop=("r", prop_celular_i) if t > 48.6 else None)


def s11(c, t):  # 51.3 - 56.0  aos 30, zero; e mora no quarto de infância
    fundo_marca(c, t, "vermelho", holofote=(250, 1080))
    numero_i(c, "AOS 30, ELE TEM", 520, 250, 90, CREME)
    if t < 53.3:
        numero_i(c, "R$ 70 MIL", 560, 450, 150, GOLD)
    else:
        contador(c, t, 53.3, 70000, 0, 560, 450, 150, d=0.5, col=GOLD)
    entra(c, t, 53.4, 600, 590, selo("IGUAL À CARLA", NAVY, 58, CREME), anim="stamp")
    entra(c, t, 54.4, 640, 720, selo("NO QUARTO DE INFÂNCIA", ORANGE, 44, CREME), anim="stamp")
    pessoa(c, t, 190, 1300, 1.25, "lucas", poses=((0, "stand"), (53.4, "head")), exprs=((0, "neutral"), (53.4, "desperate")), look=0.6)


def s12(c, t):  # 56.0 - 62.9  a conta: não é vergonha; vergonha é não guardar nada
    fundo_marca(c, t, "creme")
    numero_i(c, "A CONTA É ESSA", 520, 240, 96, NAVY, contorno=CREME)
    entra(c, t, 57.4, 520, 370, cartao("Morar com os pais", "", TINTA, 760, 100), anim="right")
    entra(c, t, 58.5, 520, 475, selo("NÃO É VERGONHA", VERDE, 62, CREME), anim="stamp")
    entra(c, t, 60.5, 520, 590, cartao("...e não guardar nada", "", TINTA, 760, 100), anim="right")
    entra(c, t, 62.0, 560, 695, selo("ISSO É VERGONHA", VERMELHO, 62, CREME), anim="stamp")
    consultor_i(c, t, 230, 1300, 0.95, poses=((0, "present"), (58.5, "thumb"), (62.0, "finger_up")),
                exprs=((0, "neutral"), (58.5, "confident"), (62.0, "think")), look=0.6)


def s13(c, t):  # 62.9 - fim  time Carla ou time Lucas?
    fundo_marca(c, t, "navy", holofote=(520, 1100))
    numero_i(c, "VERGONHA OU", 520, 250, 100, CREME)
    numero_i(c, "ESTRATÉGIA?", 520, 370, 110, GOLD)
    entra(c, t, 63.1, 270, 540, selo("TIME CARLA", CARLA_COR, 52, CREME), anim="stamp")
    entra(c, t, 64.1, 770, 540, selo("TIME LUCAS", LUCAS_COR, 52, CREME), anim="stamp")
    entra(c, t, 65.0, 520, 680, selo("COMENTA", VERMELHO, 62, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.2, "carla", poses=((0, "stand"), (63.1, "thumb")), exprs=((0, "happy"), (63.1, "grin")), look=0.4)
    pessoa(c, t, 790, 1300, 1.2, "lucas", poses=((0, "stand"), (64.1, "thumb")), exprs=((0, "happy"), (64.1, "grin")), look=-0.4)
    consultor_i(c, t, 520, 1330, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.0)


SCENES = [(0, 5.4, s01), (5.4, 8.9, s02), (8.9, 16.7, s03), (16.7, 23.2, s04), (23.2, 26.3, s05),
          (26.3, 29.5, s06), (29.5, 34.1, s07), (34.1, 37.7, s08), (37.7, 45.1, s09), (45.1, 51.3, s10),
          (51.3, 56.0, s11), (56.0, 62.9, s12), (62.9, 999.0, s13)]
