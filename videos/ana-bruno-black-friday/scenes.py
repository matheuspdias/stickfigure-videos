"""Black Friday: à vista com 10% ou 10x sem juros com o dinheiro rendendo? Ana x Bruno. Só TikTok: vertical nativo 1080x1920, 81,8 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: TV de R$ 3.000; Bruno deixa R$ 3.000 num CDB ~100% do CDI (Selic 13,75%) e paga 10x R$ 300:
sobram ~R$ 188 brutos, ~R$ 146 líquidos (IR 22,5%) -> "uns R$ 150". Ana paga R$ 2.700 (economiza R$ 300).
Com 3% de desconto: R$ 90 < R$ 150. Empate perto de 5% (146/3000 = 4,9%)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(31.4, "tum"), (39.4, "soft_ding"), (46.2, "tum"), (80.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ANA_COR = PURPLE
BRUNO_COR = BLUE
PRETO_BF = (0.10, 0.10, 0.12)

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

def tv(c, s=1.0, etiqueta=None):
    """TV na estante (origem = base) com etiqueta de preço opcional"""
    c.save(); c.scale(s, s)
    tv_i(c, 420, True, 0)
    c.restore()
    if etiqueta:
        c.save(); c.translate(150 * s, -330 * s); c.rotate(0.12); etiqueta_preco(c, etiqueta, GOLD, 44); c.restore()


def faixa_bf(c, t, y=180):
    """faixa preta "BLACK FRIDAY" atravessada"""
    c.save(); c.translate(540, y); c.rotate(-0.05)
    c.rectangle(-700, -60, 1400, 120); rgb(c, PRETO_BF); c.fill()
    numero_i(c, "BLACK FRIDAY", 0, 0, 90, GOLD, contorno=PRETO_BF)
    c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.6  gancho
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "PARCELAR", 520, 240, 120, CREME)
    numero_i(c, "SEM JUROS", 520, 370, 110, GOLD)
    if t > 2.8:
        entra(c, t, 2.8, 520, 510, selo("OU À VISTA?", VERMELHO, 90, CREME), anim="stamp")
    entra(c, t, 4.9, 600, 640, selo("DIVIDE MUITA GENTE", NAVY, 50, GOLD), anim="stamp")
    entra(c, t, 0.5, 740, 1270, lambda c: tv(c, 0.8), anim="up")
    consultor_i(c, t, 230, 1300, 1.25, poses=((0, "think"), (2.8, "point_r")), exprs=((0, "think"), (2.8, "confident")), look=0.6)


def s02(c, t):  # 6.6 - 11.6  Black Friday: TV de 3 mil; Ana e Bruno compram a mesma
    cena_mercado(c, t, carrinho=False)
    faixa_bf(c, t, 230)
    entra(c, t, 7.9, 540, 900, lambda c: tv(c, 1.0, "R$ 3.000"), anim="up")
    pessoa(c, t, 190, 1300, 1.3, "ana", poses=((0, "stand"), (9.9, "point_r")), exprs=((0, "happy"), (9.9, "grin")), look=0.5)
    pessoa(c, t, 880, 1300, 1.3, "bruno", poses=((0, "stand"), (10.3, "point_l")), exprs=((0, "happy"), (10.3, "grin")), look=-0.5)


def s03(c, t):  # 11.6 - 18.9  duas opções: 10x de 300 sem juros ou à vista com 10%
    fundo_marca(c, t, "creme")
    numero_i(c, "DUAS OPÇÕES", 520, 240, 104, NAVY, contorno=CREME)
    entra(c, t, 13.5, 600, 440, cartao("10x de R$ 300", "SEM JUROS", BLUE, 680, 120), anim="right")
    if t > 16.1:
        numero_i(c, "OU", 600, 570, 70, VERMELHO, contorno=CREME)
    entra(c, t, 16.3, 600, 700, cartao("À vista", "- 10%", VERDE, 680, 120), anim="right")
    pessoa(c, t, 190, 1300, 1.3, "vendedor", poses=((0, "present"), (13.5, "point_r"), (16.3, "thumb")),
           exprs=((0, "happy"), (13.5, "grin"), (16.3, "confident")), look=0.6)
    entra(c, t, 12.0, 830, 1280, lambda c: tv(c, 0.6), anim="up")


def s04(c, t):  # 18.9 - 22.6  Bruno pensa: sem juros, deixo rendendo
    cena_sala(c, t, "tarde")
    numero_i(c, "O BRUNO PENSA", 520, 240, 96, CREME)
    entra(c, t, 20.1, 620, 420, cartao("Sem juros?", "", TINTA, 560, 100), anim="right")
    entra(c, t, 21.0, 620, 560, selo("DEIXO RENDENDO", VERDE, 60, CREME), anim="stamp")
    pessoa(c, t, 220, 1300, 1.35, "bruno", poses=((0, "think"), (21.0, "thumb")), exprs=((0, "think"), (21.0, "grin")), look=0.6)


def s05(c, t):  # 22.6 - 29.8  guarda 3 mil rendendo ~1% ao mês, tira 300 por mês
    fundo_marca(c, t, "navy", holofote=(250, 1100))
    numero_i(c, "O DINHEIRO RENDE", 520, 230, 84, CREME)
    entra(c, t, 23.3, 680, 720, lambda c: celular_app(c, t, 0, 0, 0.95, "Investido", "R$ 3.000", "rendendo",
                                                     curva=lambda k: k ** 1.4, t0=23.6, d=2.5), anim="up")
    entra(c, t, 25.5, 520, 335, selo("~1% AO MÊS", VERDE, 56, CREME), anim="stamp")
    entra(c, t, 27.1, 640, 1130, selo("- R$ 300 POR MÊS", VERMELHO, 54, CREME), anim="stamp")
    pessoa(c, t, 210, 1300, 1.3, "bruno", poses=((0, "present"), (27.1, "point_r")), exprs=((0, "happy"), (27.1, "neutral")), look=0.6)


def s06(c, t):  # 29.8 - 34.0  Ana pega o desconto: paga 2.700 na hora
    cena_mercado(c, t, carrinho=False)
    numero_i(c, "A ANA PAGA", 520, 240, 100, CREME)
    numero_i(c, "À VISTA", 520, 350, 84, GOLD)
    if t < 31.4:
        numero_i(c, "R$ 3.000", 620, 520, 130, CREME)
    else:
        contador(c, t, 31.4, 3000, 2700, 620, 520, 130, d=0.9, col=VERDE)
    entra(c, t, 33.1, 640, 680, selo("NA HORA", NAVY, 64, GOLD), anim="stamp")
    entra(c, t, 30.0, 820, 1280, lambda c: tv(c, 0.6), anim="up")
    pessoa(c, t, 210, 1300, 1.35, "ana", poses=((0, "stand"), (31.4, "thumb")), exprs=((0, "happy"), (31.4, "grin")), look=0.6)


def s07(c, t):  # 34.0 - 42.9  10 meses depois: Bruno pagou tudo e sobrou ~150
    fundo_marca(c, t, "verde", holofote=(250, 1100))
    numero_i(c, "10 MESES DEPOIS", 520, 230, 90, CREME)
    entra(c, t, 36.8, 600, 380, selo("SOBROU O RENDIMENTO", NAVY, 50, CREME), anim="stamp")
    if 38.4 < t < 39.4:
        numero_i(c, "QUANTO?", 620, 560, 120, GOLD)
    contador(c, t, 39.4, 0, 150, 620, 560, 150, d=0.9, col=GOLD)
    entra(c, t, 41.0, 640, 720, cartao("já sem o imposto", "", TINTA, 520, 90), anim="right")
    pessoa(c, t, 210, 1300, 1.35, "bruno", poses=((0, "stand"), (36.8, "think"), (39.6, "arms_up")),
           exprs=((0, "neutral"), (36.8, "think"), (39.6, "grin")), look=0.6)


def s08(c, t):  # 42.9 - 47.1  Ana economizou 300: o dobro
    fundo_marca(c, t, "creme")
    numero_i(c, "QUEM GANHOU?", 520, 230, 100, NAVY, contorno=CREME)
    barras_i(c, t, 43.3, 330, 1000, 600, 560, dados=(("Ana", 300, ANA_COR), ("Bruno", 150, BRUNO_COR)), d=1.0, intervalo=0.3)
    entra(c, t, 46.1, 640, 1170, selo("O DOBRO", VERDE, 70, CREME), anim="stamp")
    pessoa(c, t, 150, 1300, 1.05, "ana", poses=((0, "stand"), (46.1, "arms_up")), exprs=((0, "happy"), (46.1, "grin")), look=0.6)


def s09(c, t):  # 47.1 - 51.4  mas tem um detalhe: desconto pequeno, a conta vira
    fundo_marca(c, t, "navy", holofote=(520, 1100))
    numero_i(c, "MAS TEM", 520, 240, 110, CREME)
    numero_i(c, "UM DETALHE", 520, 370, 110, GOLD)
    entra(c, t, 48.4, 520, 530, cartao("Desconto pequeno?", "", TINTA, 620, 100), anim="right")
    entra(c, t, 50.4, 520, 670, selo("A CONTA VIRA", VERMELHO, 70, CREME), anim="stamp")
    consultor_i(c, t, 520, 1300, 1.05, poses=((0, "finger_up"), (50.4, "shrug")), exprs=((0, "think"), (50.4, "shocked")), look=0.0)


def s10(c, t):  # 51.4 - 57.5  com 3%: Ana economiza 90; Bruno ganha
    fundo_marca(c, t, "creme")
    numero_i(c, "DESCONTO DE 3%", 520, 230, 96, NAVY, contorno=CREME)
    barras_i(c, t, 53.3, 330, 1000, 600, 520, dados=(("Ana", 90, ANA_COR), ("Bruno", 150, BRUNO_COR)), d=1.0, intervalo=0.3)
    entra(c, t, 56.0, 640, 1170, selo("BRUNO GANHA", BRUNO_COR, 64, CREME), anim="stamp")
    pessoa(c, t, 150, 1300, 1.05, "bruno", poses=((0, "stand"), (56.0, "arms_up")), exprs=((0, "neutral"), (56.0, "grin")), look=0.6)


def s11(c, t):  # 57.5 - 66.1  regra de bolso: desconto acima de ~5% vale mais
    fundo_marca(c, t, "navy", holofote=(250, 1100))
    numero_i(c, "REGRA DE BOLSO", 520, 230, 96, GOLD)
    if t > 59.0:
        numero_i(c, "COM OS JUROS DE HOJE", 520, 340, 56, CREME)
    entra(c, t, 60.6, 620, 480, cartao("Desconto à vista", "", TINTA, 600, 100), anim="right")
    if t > 62.4:
        numero_i(c, "+ DE 5%", 640, 650, 150, VERDE, contorno=CREME)
    entra(c, t, 63.6, 600, 790, selo("VALE MAIS QUE PARCELAR", VERDE, 44, CREME), anim="stamp")
    consultor_i(c, t, 200, 1300, 1.1, poses=((0, "finger_up"), (62.4, "point_r")), exprs=((0, "think"), (62.4, "confident")),
                look=0.6, prop=("l", prop_calc_i))


def s12(c, t):  # 66.1 - 73.9  só funciona se guardar de verdade; se gastar, sobram as parcelas
    cena_sala(c, t, "dia")
    numero_i(c, "SÓ FUNCIONA SE", 520, 240, 96, CREME)
    numero_i(c, "FICAR GUARDADO", 520, 350, 90, GOLD) if t > 67.8 else None
    if t > 70.2:
        entra(c, t, 70.2, 640, 520, cartao("Gastou o rendimento?", "", VERMELHO, 640, 110), anim="right")
    entra(c, t, 72.1, 640, 680, selo("SOBRAM AS PARCELAS", VERMELHO, 50, CREME), anim="stamp")
    pessoa(c, t, 220, 1300, 1.35, "bruno", poses=((0, "stand"), (70.2, "hold"), (72.1, "head")),
           exprs=((0, "neutral"), (70.2, "happy"), (72.1, "desperate")), look=0.6, prop=("r", prop_celular_i) if 70.2 < t < 72.1 else None)


def s13(c, t):  # 73.9 - 78.0  na Black Friday, pergunta: quanto é à vista?
    cena_mercado(c, t, carrinho=False)
    faixa_bf(c, t, 230)
    numero_i(c, "PERGUNTA SEMPRE:", 520, 400, 76, CREME)
    entra(c, t, 76.8, 560, 540, selo("QUANTO É À VISTA?", VERMELHO, 66, CREME), anim="stamp")
    consultor_i(c, t, 260, 1300, 1.35, poses=((0, "present"), (76.8, "point_r")), exprs=((0, "happy"), (76.8, "confident")), look=0.6)
    entra(c, t, 74.2, 800, 1280, lambda c: tv(c, 0.6), anim="up")


def s14(c, t):  # 78.0 - fim  time Ana ou time Bruno?
    fundo_marca(c, t, "navy", holofote=(520, 1100))
    numero_i(c, "À VISTA OU", 520, 250, 100, CREME)
    numero_i(c, "PARCELADO?", 520, 370, 110, GOLD)
    entra(c, t, 79.1, 270, 540, selo("TIME ANA", ANA_COR, 54, CREME), anim="stamp")
    entra(c, t, 80.0, 770, 540, selo("TIME BRUNO", BRUNO_COR, 54, CREME), anim="stamp")
    entra(c, t, 80.9, 520, 680, selo("COMENTA", VERMELHO, 62, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.2, "ana", poses=((0, "stand"), (79.1, "thumb")), exprs=((0, "happy"), (79.1, "grin")), look=0.4)
    pessoa(c, t, 790, 1300, 1.2, "bruno", poses=((0, "stand"), (80.0, "thumb")), exprs=((0, "happy"), (80.0, "grin")), look=-0.4)
    consultor_i(c, t, 520, 1330, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.0)


SCENES = [(0, 6.6, s01), (6.6, 11.6, s02), (11.6, 18.9, s03), (18.9, 22.6, s04), (22.6, 29.8, s05),
          (29.8, 34.0, s06), (34.0, 42.9, s07), (42.9, 47.1, s08), (47.1, 51.4, s09), (51.4, 57.5, s10),
          (57.5, 66.1, s11), (66.1, 73.9, s12), (73.9, 78.0, s13), (78.0, 999.0, s14)]
