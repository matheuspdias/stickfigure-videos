"""R$ 300 por mês com lanche e bar é exagero? Só TikTok: vertical nativo 1080x1920, 66 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: R$ 300/mês = R$ 3.600/ano; investindo a 0,8%/mês por 10 anos ~R$ 60 mil;
R$ 300 de R$ 5.000 = 6%; metade (R$ 150) por 10 anos ~R$ 30 mil."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(16.0, "tum"), (24.6, "tum"), (48.0, "tum"), (64.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ROXO = PURPLE if "PURPLE" in globals() else (0.55, 0.36, 0.72)
CARDAPIO = (("CERVEJA", "R$ 12"), ("AÇAÍ", "R$ 18"))


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


def etq(v, cor=GOLD, size=60):
    return lambda c: etiqueta_preco(c, v, cor, size)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.9  gancho
    cena_padaria(c, t, "tarde", cardapio=CARDAPIO)
    numero_i(c, "R$ 300 POR MÊS", 520, 240, 100, GOLD)
    numero_i(c, "EM LANCHE E BAR", 520, 360, 80, CREME)
    numero_i(c, "É EXAGERO?", 520, 490, 120, CREME)
    entra(c, t, 4.6, 640, 610, selo("METADE VAI DISCORDAR", VERMELHO, 44, CREME), anim="stamp")
    consultor_i(c, t, 230, 1300, 1.35, poses=((0, "think"), (4.6, "point_r")), exprs=((0, "think"), (4.6, "confident")), look=0.7)
    entra(c, t, 1.0, 720, 900, etq("R$ 300"), anim="drop")


def s02(c, t):  # 6.9 - 13.8  você ganha 5 mil; 300 vão pro lanche, cerveja, açaí
    cena_padaria(c, t, "tarde", cardapio=CARDAPIO)
    numero_i(c, "VOCÊ GANHA", 520, 230, 80, CREME)
    contador(c, t, 7.4, 0, 5000, 520, 350, 120, d=0.8, col=GOLD)
    entra(c, t, 9.0, 600, 500, selo("R$ 300 VÃO PRO...", NAVY, 56, GOLD), anim="stamp")
    entra(c, t, 10.0, 560, 680, etq("LANCHE", GOLD, 54), anim="drop")
    entra(c, t, 10.8, 600, 820, etq("CERVEJA", (0.95, 0.70, 0.20), 54), anim="drop")
    entra(c, t, 12.4, 640, 960, etq("AÇAÍ", ROXO, 54), anim="drop")
    pessoa(c, t, 250, 1300, 1.35, "lucas", poses=((0, "stand"), (10.0, "point_r"), (12.4, "thumb")),
           exprs=((0, "neutral"), (10.0, "happy"), (12.4, "grin")), look=0.6)


def s03(c, t):  # 13.8 - 17.1  em um ano: 3.600
    fundo_marca(c, t, "vermelho", holofote=(270, 1050))
    numero_i(c, "EM 1 ANO", 520, 240, 120, CREME)
    contador(c, t, 14.4, 0, 3600, 560, 470, 150, d=1.6, col=GOLD)
    for i in range(3):
        c.save(); c.translate(660 + i * 120, 1260); pilha_moedas(c, 5 + i * 3, 50, t, 14.6 + i * 0.4, 0.06); c.restore()
    consultor_i(c, t, 260, 1300, 1.4, poses=((0, "stand"), (16.0, "head")), exprs=((0, "neutral"), (16.0, "shocked")), look=0.6)


def s04(c, t):  # 17.1 - 25.9  a conta do "corta tudo": investindo, ~60 mil em 10 anos
    fundo_marca(c, t, "verde", holofote=(220, 1050))
    numero_i(c, "A CONTA DO", 520, 220, 80, CREME)
    numero_i(c, "\"CORTA TUDO\"", 520, 330, 104, GOLD)
    if t > 20.6:
        numero_i(c, "R$ 300 INVESTIDOS/MÊS", 560, 425, 50, CREME)
    grafico_curva(c, t, 21.6, 430, 1090, 520, 380, d=2.6, cor=VERDE, eixo_x=("hoje", "10 anos"), f=lambda k: k ** 1.5)
    contador(c, t, 24.6, 0, 60000, 640, 545, 104, d=1.0, col=GOLD)
    consultor_i(c, t, 200, 1300, 1.3, poses=((0, "present"), (24.6, "arms_up")), exprs=((0, "neutral"), (24.6, "shocked")), look=0.7)


def s05(c, t):  # 25.9 - 28.1  assusta, né? mas olha a virada
    fundo_marca(c, t, "navy", holofote=(520, 1050))
    numero_i(c, "ASSUSTA, NÉ?", 520, 260, 110, CREME)
    entra(c, t, 27.1, 520, 470, selo("MAS OLHA A VIRADA", GOLD, 70, NAVY), anim="stamp")
    consultor_i(c, t, 520, 1300, 1.5, poses=((0, "shrug"), (27.1, "finger_up")), exprs=((0, "think"), (27.1, "confident")), look=0.0)


def s06(c, t):  # 28.1 - 33.0  6% do salário: não é exagero
    fundo_marca(c, t, "creme")
    numero_i(c, "R$ 300 DE R$ 5 MIL", 520, 230, 76, NAVY, contorno=CREME)
    rosca_i(c, t, 29.4, 640, 640, r=210, pct=0.06, cor=VERDE, texto=None)
    numero_i(c, "DO SALÁRIO", 640, 930, 60, NAVY, contorno=CREME) if t > 30.3 else None
    entra(c, t, 31.6, 640, 1110, selo("NÃO É EXAGERO", VERDE, 62, CREME), anim="stamp")
    consultor_i(c, t, 210, 1300, 1.25, poses=((0, "point_r"), (31.6, "thumb")), exprs=((0, "neutral"), (31.6, "confident")), look=0.8)


def s07(c, t):  # 33.0 - 38.8  lazer faz parte da vida; quem corta tudo desiste
    cena_rua(c, t, "tarde", carros=False)
    numero_i(c, "LAZER FAZ PARTE", 520, 230, 88, CREME)
    numero_i(c, "DA VIDA", 520, 340, 100, GOLD)
    entra(c, t, 34.9, 540, 460, selo("QUEM CORTA TUDO...", NAVY, 54, CREME), anim="stamp")
    entra(c, t, 36.9, 540, 580, selo("DESISTE EM MESES", VERMELHO, 54, CREME), anim="stamp")
    pessoa(c, t, 760, 1300, 1.2, "lucas", poses=((0, "wave"), (36.9, "head")), exprs=((0, "grin"), (36.9, "desperate")), look=-0.5)
    consultor_i(c, t, 270, 1300, 1.2, poses=((0, "present"), (34.9, "point_r")), exprs=((0, "happy"), (34.9, "think")), look=0.5)


def s08(c, t):  # 38.8 - 45.5  o problema é o lanche que você não vê
    fundo_marca(c, t, "navy", holofote=(230, 1050))
    numero_i(c, "O PROBLEMA", 520, 220, 96, CREME)
    numero_i(c, "NÃO É O LANCHE", 520, 330, 84, GOLD)
    if t > 40.8:
        numero_i(c, "É O QUE VOCÊ NÃO VÊ", 520, 440, 56, CREME)
    linhas = [("Pix lanchonete", "- R$ 10", VERMELHO), ("Cartão bar", "- R$ 15", VERMELHO),
              ("Pix açaí", "- R$ 18", VERMELHO), ("Cartão lanche", "- R$ 22", VERMELHO), ("Pix bar", "- R$ 14", VERMELHO)]
    entra(c, t, 41.6, 680, 880, lambda c: celular_app(c, t, 0, 0, 1.05, "Extrato", "Pix e cartão", linhas=linhas, t0=42.4, d=2.6), anim="drop")
    consultor_i(c, t, 230, 1300, 1.3, poses=((0, "finger_up"), (42.5, "point_r")), exprs=((0, "think"), (42.5, "neutral")), look=0.8)


def s09(c, t):  # 45.5 - 49.3  quando soma, 300 viram 600
    fundo_marca(c, t, "vermelho", holofote=(260, 1050))
    numero_i(c, "QUANDO SOMA", 520, 230, 100, CREME)
    numero_i(c, "DE VERDADE...", 520, 340, 80, GOLD)
    if t < 47.5:
        numero_i(c, "R$ 300", 560, 520, 160, CREME)
    else:
        contador(c, t, 47.5, 300, 600, 560, 520, 160, d=0.9, col=GOLD)
    entra(c, t, 48.3, 640, 720, selo("O DOBRO", NAVY, 70, CREME), anim="stamp")
    consultor_i(c, t, 250, 1300, 1.3, poses=((0, "think"), (48.0, "head")), exprs=((0, "think"), (48.0, "shocked")), look=0.6)


def s10(c, t):  # 49.3 - 54.9  faz assim: decide o valor no começo do mês; corta só a metade
    cena_sala(c, t, "dia")
    numero_i(c, "FAZ ASSIM", 520, 230, 120, GOLD)
    entra(c, t, 50.3, 600, 440, cartao("1. Lazer do mês", "DIA 1", NAVY, 620), anim="right")
    entra(c, t, 53.8, 600, 580, cartao("2. Quer guardar?", "CORTA 1/2", VERDE, 620), anim="right")
    consultor_i(c, t, 260, 1300, 1.4, poses=((0, "present"), (50.3, "point_ru"), (53.8, "thumb")),
                exprs=((0, "happy"), (50.3, "neutral"), (53.8, "confident")), look=0.7)


def s11(c, t):  # 54.9 - 60.6  150 por mês, 10 anos: ~30 mil, e continua saindo
    fundo_marca(c, t, "verde", holofote=(250, 1050))
    numero_i(c, "R$ 150 POR MÊS", 520, 230, 96, CREME)
    numero_i(c, "EM 10 ANOS", 520, 340, 76, GOLD) if t > 56.7 else None
    contador(c, t, 57.8, 0, 30000, 600, 530, 140, d=1.0, col=GOLD)
    entra(c, t, 59.1, 640, 720, selo("E CONTINUA SAINDO", NAVY, 50, CREME), anim="stamp")
    consultor_i(c, t, 200, 1300, 1.3, poses=((0, "point_r"), (58.6, "arms_up")), exprs=((0, "neutral"), (58.6, "grin")), look=0.6)
    chuva_dinheiro(c, t, 58.6, 8, area=(560, 900), area_y=1250)


def s12(c, t):  # 60.6 - fim  exagero ou merecido? comenta
    cena_padaria(c, t, "tarde", cardapio=CARDAPIO)
    numero_i(c, "R$ 300 EM LANCHE E BAR", 520, 230, 66, CREME)
    entra(c, t, 62.6, 300, 400, selo("EXAGERO", VERMELHO, 52, CREME), anim="stamp")
    entra(c, t, 63.3, 755, 400, selo("MERECIDO", VERDE, 52, CREME), anim="stamp")
    if t > 63.2:
        numero_i(c, "OU", 528, 405, 50, GOLD)
    entra(c, t, 64.2, 520, 590, selo("DEFENDE NOS COMENTÁRIOS", NAVY, 48, GOLD), anim="stamp")
    pessoa(c, t, 760, 1300, 1.3, "lucas", poses=((0, "shrug"), (63.3, "thumb")), exprs=((0, "think"), (63.3, "grin")), look=-0.5)
    consultor_i(c, t, 270, 1300, 1.35, poses=((0, "think"), (64.2, "present")), exprs=((0, "think"), (64.2, "happy")), look=0.5)


SCENES = [(0, 6.9, s01), (6.9, 13.8, s02), (13.8, 17.1, s03), (17.1, 25.9, s04), (25.9, 28.1, s05),
          (28.1, 33.0, s06), (33.0, 38.8, s07), (38.8, 45.5, s08), (45.5, 49.3, s09), (49.3, 54.9, s10),
          (54.9, 60.6, s11), (60.6, 999.0, s12)]
