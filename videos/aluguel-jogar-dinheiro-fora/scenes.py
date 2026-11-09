"""Pagar aluguel é jogar dinheiro fora? Ana x Bruno. Só TikTok: vertical nativo 1080x1920, 77 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: apê de R$ 300 mil; Bruno: entrada 60 mil, SAC 30 anos a 12% a.a. (1ª parcela ~R$ 2.944);
Ana: aluguel R$ 1.500 (+4,5%/ano), investe a entrada e a diferença a 0,8%/mês. Em 10 anos: Bruno ~330 mil
(imóvel ~490 mil - dívida 160 mil), Ana ~325 mil; se Ana gastar a diferença, ~156 mil."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(38.6, "tum"), (45.4, "tum"), (60.1, "tum"), (76.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ROXO = PURPLE if "PURPLE" in globals() else (0.55, 0.36, 0.72)
AZUL = BLUE if "BLUE" in globals() else (0.25, 0.45, 0.80)


# ---------------------------------------------------------------- helpers
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


def predio_apto(c, x, y, s=1.0, t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    predio_moderno(c, -150, 0, 300, 560, (0.74, 0.70, 0.64), 0.0, seed=7)
    c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.6  gancho
    cena_rua(c, t, "tarde", carros=False)
    numero_i(c, "PAGAR ALUGUEL", 520, 240, 96, CREME)
    numero_i(c, "É JOGAR DINHEIRO", 520, 350, 84, CREME)
    numero_i(c, "FORA?", 520, 480, 140, GOLD)
    entra(c, t, 3.5, 600, 680, selo("FIZ A CONTA", NAVY, 60, GOLD), anim="stamp")
    entra(c, t, 4.3, 620, 840, selo("VAI IRRITAR MUITA GENTE", VERMELHO, 44, CREME), anim="pop")
    consultor_i(c, t, 230, 1300, 1.35, poses=((0, "think"), (2.5, "finger_up")), exprs=((0, "think"), (2.5, "confident")), look=0.7)
    chuva_dinheiro(c, t, 0.2, 8, area=(560, 900), area_y=1250)


def s02(c, t):  # 5.6 - 10.6  um apê de R$ 300 mil: Ana aluga, Bruno financia
    cena_rua(c, t, "dia", carros=False)
    numero_i(c, "UM APÊ DE", 520, 230, 80, CREME)
    contador(c, t, 6.4, 0, 300000, 520, 360, 130, d=1.0, col=GOLD)
    entra(c, t, 8.4, 250, 600, selo("ALUGA", ROXO, 60, CREME), anim="stamp")
    entra(c, t, 9.4, 760, 600, selo("FINANCIA", AZUL, 60, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.35, "ana", poses=((0, "stand"), (8.4, "point_ru")), exprs=((0, "neutral"), (8.4, "happy")), look=0.4)
    pessoa(c, t, 760, 1300, 1.35, "bruno", poses=((0, "stand"), (9.4, "thumb")), exprs=((0, "neutral"), (9.4, "confident")), look=-0.4)


def s03(c, t):  # 10.6 - 18.7  Bruno: entrada, 30 anos, parcela de quase R$ 3 mil
    fundo_marca(c, t, "navy", holofote=(220, 1050))
    numero_i(c, "O BRUNO", 520, 230, 104, CREME)
    entra(c, t, 11.6, 620, 420, cartao("Entrada", "R$ 60 mil", NAVY, 560), anim="right")
    entra(c, t, 14.0, 620, 545, cartao("Financia", "30 anos", NAVY, 560), anim="right")
    if t > 15.2:
        numero_i(c, "1ª PARCELA", 620, 710, 64, CREME)
    contador(c, t, 16.6, 0, 2944, 620, 850, 130, d=1.2, col=GOLD)
    numero_i(c, "POR MÊS", 620, 970, 60, CREME) if t > 17.8 else None
    pessoa(c, t, 210, 1300, 1.3, "bruno", poses=((0, "stand"), (11.6, "point_r"), (16.6, "head")),
           exprs=((0, "neutral"), (11.6, "confident"), (16.6, "worried")), look=0.7)


def s04(c, t):  # 18.7 - 29.8  Ana: aluguel R$ 1.500, investe a entrada e a diferença
    cena_sala(c, t, "tarde")
    numero_i(c, "A ANA", 520, 230, 104, GOLD)
    entra(c, t, 19.3, 640, 390, selo("ALUGUEL R$ 1.500", ROXO, 50, CREME), anim="drop")
    entra(c, t, 22.7, 700, 800, lambda c: celular_app(c, t, 0, 0, 1.0, "Investido", "R$ 60.000",
                                                     "a entrada que ela não deu", curva=lambda k: k ** 1.3, t0=23.0), anim="drop")
    entra(c, t, 26.6, 680, 1180, selo("+ A DIFERENÇA TODO MÊS", VERDE, 44, CREME), anim="stamp")
    pessoa(c, t, 230, 1300, 1.35, "ana", poses=((0, "present"), (22.7, "point_r")), exprs=((0, "neutral"), (22.7, "confident")),
           look=0.7, prop=None)


def s05(c, t):  # 29.8 - 35.6  dez anos depois: o apê valorizou
    cena_rua(c, t, "tarde", carros=False)
    numero_i(c, "10 ANOS DEPOIS", 520, 230, 96, GOLD)
    numero_i(c, "O APÊ DO BRUNO VALE", 520, 360, 58, CREME) if t > 31.7 else None
    contador(c, t, 32.7, 300000, 490000, 560, 490, 130, d=1.6, col=VERDE)
    entra(c, t, 33.0, 700, 760, selo("VALORIZOU", VERDE, 56, CREME), anim="pop")
    pessoa(c, t, 260, 1300, 1.35, "bruno", poses=((0, "stand"), (33.0, "arms_up")), exprs=((0, "neutral"), (33.0, "grin")), look=0.6)


def s06(c, t):  # 35.6 - 41.2  mas ainda deve 160 mil: sobra 330 mil
    fundo_marca(c, t, "creme")
    numero_i(c, "O BRUNO", 520, 230, 96, AZUL, contorno=CREME)
    entra(c, t, 35.7, 640, 420, cartao("Apê", "R$ 490 mil", VERDE, 560), anim="right")
    entra(c, t, 36.6, 640, 545, cartao("Dívida", "- R$ 160 mil", VERMELHO, 560), anim="right")
    if t > 38.4:
        line(c, 380, 618, 900, 618, 6, TINTA)
    entra(c, t, 38.6, 640, 760, selo("R$ 330 MIL", NAVY, 92, GOLD), anim="stamp")
    pessoa(c, t, 200, 1300, 1.2, "bruno", poses=((0, "point_r"), (36.6, "shrug"), (38.6, "thumb")),
           exprs=((0, "happy"), (36.6, "worried"), (38.6, "confident")), look=0.8)


def s07(c, t):  # 41.2 - 45.3  e a Ana? 325 mil investidos
    fundo_marca(c, t, "verde", holofote=(250, 1050))
    numero_i(c, "E A ANA?", 520, 230, 104, GOLD)
    entra(c, t, 42.0, 700, 750, lambda c: celular_app(c, t, 0, 0, 1.1, "Investido em 10 anos", "R$ 325.000", "",
                                                     curva=lambda k: k ** 1.6, t0=42.3), anim="drop")
    contador(c, t, 42.3, 60000, 325000, 520, 380, 120, d=1.6, col=CREME)
    pessoa(c, t, 230, 1300, 1.35, "ana", poses=((0, "think"), (43.7, "arms_up")), exprs=((0, "think"), (43.7, "grin")), look=0.6)


def s08(c, t):  # 45.3 - 51.0  praticamente empate; quem fala que é jogar fora está errado
    fundo_marca(c, t, "navy")
    numero_i(c, "PRATICAMENTE", 520, 230, 90, CREME)
    numero_i(c, "EMPATE", 520, 350, 120, GOLD)
    barras_i(c, t, 45.5, 160, 1150, 720, 520, dados=(("Bruno", 330000, AZUL), ("Ana", 325000, ROXO)), d=0.9, intervalo=0.2, size_val=58, fmt=lambda v: f"R$ {v / 1000:.0f} MIL")
    entra(c, t, 49.3, 540, 760, selo("\"JOGAR FORA\"? ERRADO", VERMELHO, 52, CREME), anim="stamp")


def s09(c, t):  # 51.0 - 54.6  juros também não voltam
    fundo_marca(c, t, "vermelho", holofote=(520, 1050))
    numero_i(c, "OS JUROS", 520, 240, 110, CREME)
    numero_i(c, "TAMBÉM NÃO VOLTAM", 520, 370, 72, GOLD)
    if t > 52.4:
        for i in range(7):
            tt = 52.4 + i * 0.2
            if t < tt:
                continue
            k = ease_out(prog(t, tt, 0.8))
            c.save(); c.translate(680 + (i % 3) * 80, 1180 - k * 420 - (i // 3) * 50); c.rotate(k * 0.6)
            nota_i(c, "100", 150); c.restore()
    consultor_i(c, t, 330, 1300, 1.4, poses=((0, "finger_up"), (53.0, "shrug")), exprs=((0, "think"), (53.0, "worried")), look=0.5)


def s10(c, t):  # 54.6 - 63.9  o detalhe: se a Ana gastar a diferença
    fundo_marca(c, t, "vermelho", holofote=(250, 1050))
    numero_i(c, "O DETALHE QUE", 520, 230, 88, CREME)
    numero_i(c, "MUDA TUDO", 520, 340, 104, GOLD)
    entra(c, t, 57.5, 640, 490, selo("SE A ANA GASTAR", NAVY, 56, CREME), anim="stamp")
    if t > 59.0:
        if t < 61.8:
            contador(c, t, 60.1, 325000, 156000, 660, 650, 110, d=1.6, col=CREME)
        else:
            numero_i(c, brl(156000), 660, 650, 110, CREME)
    entra(c, t, 62.4, 640, 820, selo("METADE DO BRUNO", CREME, 60, VERMELHO), anim="stamp")
    pessoa(c, t, 220, 1300, 1.35, "ana", poses=((0, "hold"), (60.1, "head")), exprs=((0, "happy"), (60.1, "shocked")),
           look=0.6, prop=("r", prop_celular_i))


def s11(c, t):  # 63.9 - 69.6  aluguel só ganha de quem tem disciplina
    cena_sala(c, t, "tarde")
    numero_i(c, "ALUGUEL SÓ GANHA", 520, 230, 80, CREME)
    numero_i(c, "COM DISCIPLINA", 520, 340, 92, GOLD)
    entra(c, t, 67.4, 650, 600, lambda c: notificacao(c, 0, 0, 1.1, "Parcela debitada", "o financiamento obriga a guardar", AZUL, "BANCO"), anim="drop")
    consultor_i(c, t, 240, 1300, 1.4, poses=((0, "finger_up"), (67.4, "point_r")), exprs=((0, "confident"), (67.4, "neutral")), look=0.7)


def s12(c, t):  # 69.6 - fim  time Ana ou time Bruno?
    fundo_marca(c, t, "navy", holofote=(520, 1050))
    numero_i(c, "ALUGAR E INVESTIR", 520, 230, 76, CREME)
    numero_i(c, "OU FINANCIAR?", 520, 340, 96, GOLD)
    entra(c, t, 74.4, 250, 520, selo("TIME ANA", ROXO, 56, CREME), anim="stamp")
    entra(c, t, 75.2, 760, 520, selo("TIME BRUNO", AZUL, 56, CREME), anim="stamp")
    entra(c, t, 76.2, 510, 690, selo("COMENTA", VERMELHO, 62, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.3, "ana", poses=((0, "stand"), (74.4, "thumb")), exprs=((0, "happy"), (74.4, "grin")), look=0.4)
    pessoa(c, t, 760, 1300, 1.3, "bruno", poses=((0, "stand"), (75.2, "thumb")), exprs=((0, "happy"), (75.2, "grin")), look=-0.4)
    consultor_i(c, t, 505, 1330, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.0)


SCENES = [(0, 5.6, s01), (5.6, 10.6, s02), (10.6, 18.7, s03), (18.7, 29.8, s04), (29.8, 35.6, s05),
          (35.6, 41.2, s06), (41.2, 45.3, s07), (45.3, 51.0, s08), (51.0, 54.6, s09), (54.6, 63.9, s10),
          (63.9, 69.6, s11), (69.6, 999.0, s12)]
