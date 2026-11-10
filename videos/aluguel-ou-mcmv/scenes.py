"""Pagar aluguel é jogar dinheiro fora? Minha Casa Minha Vida, Ana x Bruno. Só TikTok: 1080x1920, 79,3 s, estilo ilustrado.
Refeito a pedido do Matheus (a versão com juro de banco tinha parcela alta demais; o dele: R$ 298 mil, parcela ~R$ 1.900).
Contas em contas.py: MCMV ~8% a.a., Price, 35 anos, entrada R$ 30 mil -> parcela ~R$ 1.900; aluguel R$ 1.500 (+4,5%/ano)
passa da parcela no 6º ano. Em 10 anos: Bruno ~R$ 240 mil (imóvel ~485 mil - dívida ~245 mil), Ana ~R$ 100 mil."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(38.4, "tum"), (52.3, "tum"), (57.8, "tum"), (64.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ROXO = PURPLE
AZUL = BLUE


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


def grafico_cruza(c, t, t0, x, y, w=720, h=440):
    """aluguel (roxo, sobe 4,5% ao ano) x parcela (azul, quase reta) em 10 anos; marca o cruzamento no 6º ano"""
    vmin, vmax = 1300, 2350
    Y = lambda v: y - (v - vmin) / (vmax - vmin) * h
    X = lambda a: x + a / 10 * w
    c.rectangle(x - 10, y, w + 20, 5); rgb(c, (0.3, 0.3, 0.35)); c.fill()
    for a in (0, 5, 10):
        text(c, f"{a} anos" if a else "hoje", X(a), y + 40, 34, HAND, CREME)
    k = ease_io(prog(t, t0, 2.2))
    # parcela: reta
    line(c, X(0), Y(1900), X(10 * k), Y(1900), 10, AZUL)
    # aluguel: degraus de 4,5% ao ano
    c.set_line_width(10); rgb(c, ROXO)
    c.move_to(X(0), Y(1500))
    for a in range(10):
        a1 = min(a + 1, 10 * k)
        if a > 10 * k:
            break
        v = 1500 * 1.045 ** a
        c.line_to(X(a1), Y(v))
        if a + 1 <= 10 * k:
            c.line_to(X(a + 1), Y(1500 * 1.045 ** (a + 1)))
    c.stroke()
    if k > 0.15:
        text(c, "parcela R$ 1.900", X(0) + 10, Y(1900) - 34, 38, HAND, (0.55, 0.75, 1.0), align="l")
        text(c, "aluguel R$ 1.500", X(0) + 10, Y(1500) + 44, 38, HAND, (0.80, 0.70, 1.0), align="l")
    if k > 0.62:
        c.new_sub_path(); c.arc(X(6), Y(1953), 22, 0, 6.283); rgb(c, GOLD); c.fill()
        text(c, "6º ano", X(6), Y(1953) - 50, 44, MARKER, GOLD)
    if k > 0.98:
        text(c, "R$ 2.229", X(10) - 10, Y(2229) - 40, 40, MARKER, (0.80, 0.70, 1.0), align="r")


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.0  gancho
    cena_rua(c, t, "tarde", carros=False)
    numero_i(c, "PAGAR ALUGUEL", 520, 240, 96, CREME)
    numero_i(c, "É JOGAR DINHEIRO", 520, 350, 84, CREME)
    numero_i(c, "FORA?", 520, 480, 140, GOLD)
    entra(c, t, 2.5, 650, 700, selo("NO MINHA CASA MINHA VIDA", VERDE, 42, CREME), anim="stamp")
    entra(c, t, 4.4, 660, 860, selo("VAI SURPREENDER", NAVY, 54, GOLD), anim="pop")
    consultor_i(c, t, 230, 1300, 1.35, poses=((0, "think"), (2.5, "present")), exprs=((0, "think"), (2.5, "confident")), look=0.7)
    chuva_dinheiro(c, t, 0.2, 8, area=(560, 900), area_y=1250)


def s02(c, t):  # 6.0 - 12.9  apê de R$ 298 mil: Ana aluga, Bruno financia no MCMV
    cena_rua(c, t, "dia", carros=False)
    numero_i(c, "UM APÊ DE", 520, 230, 80, CREME)
    contador(c, t, 6.6, 0, 298000, 520, 360, 130, d=1.4, col=GOLD)
    entra(c, t, 9.3, 250, 600, selo("ALUGA", ROXO, 60, CREME), anim="stamp")
    entra(c, t, 10.4, 750, 600, selo("MCMV", AZUL, 60, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.35, "ana", poses=((0, "stand"), (9.3, "point_ru")), exprs=((0, "neutral"), (9.3, "happy")), look=0.4)
    pessoa(c, t, 760, 1300, 1.35, "bruno", poses=((0, "stand"), (10.4, "thumb")), exprs=((0, "neutral"), (10.4, "confident")), look=-0.4)


def s03(c, t):  # 12.9 - 21.9  Bruno: entrada, 35 anos, ~8% ao ano, parcela R$ 1.900
    fundo_marca(c, t, "navy", holofote=(220, 1050))
    numero_i(c, "O BRUNO", 520, 230, 104, CREME)
    entra(c, t, 13.5, 620, 400, cartao("Entrada", "R$ 30 mil", NAVY, 560), anim="right")
    entra(c, t, 16.1, 620, 520, cartao("Prazo", "35 anos", NAVY, 560), anim="right")
    entra(c, t, 17.8, 620, 640, cartao("Juros", "~8% ao ano", NAVY, 560), anim="right")
    if t > 19.2:
        numero_i(c, "PARCELA", 620, 790, 64, CREME)
    contador(c, t, 20.2, 0, 1900, 620, 920, 130, d=1.0, col=GOLD)
    pessoa(c, t, 210, 1300, 1.3, "bruno", poses=((0, "stand"), (13.5, "point_r"), (20.2, "thumb")),
           exprs=((0, "neutral"), (13.5, "confident"), (20.2, "happy")), look=0.7)


def s04(c, t):  # 21.9 - 30.0  Ana: aluguel R$ 1.500, investe a entrada e R$ 400 por mês
    cena_sala(c, t, "tarde")
    numero_i(c, "A ANA", 520, 230, 104, GOLD)
    entra(c, t, 22.5, 640, 390, selo("ALUGUEL R$ 1.500", ROXO, 50, CREME), anim="drop")
    entra(c, t, 24.3, 700, 800, lambda c: celular_app(c, t, 0, 0, 1.0, "Investido", "R$ 30.000",
                                                     "a entrada que ela não deu", curva=lambda k: k ** 1.3, t0=24.6), anim="drop")
    entra(c, t, 27.8, 680, 1180, selo("+ R$ 400 TODO MÊS", VERDE, 50, CREME), anim="stamp")
    pessoa(c, t, 230, 1300, 1.35, "ana", poses=((0, "present"), (24.3, "point_r")), exprs=((0, "neutral"), (24.3, "confident")), look=0.7)


def s05(c, t):  # 30.0 - 37.2  o detalhe: o aluguel sobe todo ano, a parcela quase não
    fundo_marca(c, t, "creme")
    numero_i(c, "TEM UM DETALHE", 520, 230, 88, NAVY, contorno=CREME)
    entra(c, t, 32.9, 520, 420, cartao("Aluguel", "sobe todo ano", ROXO, 640), anim="right")
    if t > 33.4:
        if t < 36.0:
            contador(c, t, 33.6, 1500, 2229, 520, 580, 110, d=2.4, col=ROXO)
        else:
            numero_i(c, brl(2229), 520, 580, 110, ROXO, contorno=CREME)
        text(c, "em 10 anos", 520, 670, 42, HAND, (0.35, 0.35, 0.4))
    entra(c, t, 35.2, 520, 780, cartao("Parcela do Bruno", "quase fixa", AZUL, 640), anim="right")
    consultor_i(c, t, 520, 1330, 0.85, poses=((0, "finger_up"), (35.2, "present")), exprs=((0, "think"), (35.2, "confident")), look=0.0)


def s06(c, t):  # 37.2 - 44.3  no 6º ano o aluguel passa da parcela
    fundo_marca(c, t, "navy")
    numero_i(c, "NO 6º ANO", 520, 230, 110, GOLD)
    grafico_cruza(c, t, 37.4, 150, 1000, 660, 580)
    entra(c, t, 41.2, 540, 1190, lambda c: notificacao(c, 0, 0, 1.1, "Resgate do investimento", "para pagar o aluguel", VERMELHO, "BANCO"), anim="drop")
    if t > 41.2:
        pessoa(c, t, 950, 1330, 0.8, "ana", poses=((0, "head"),), exprs=((0, "worried"),), look=-0.4)


def s07(c, t):  # 44.3 - 55.1  dez anos depois: Bruno
    fundo_marca(c, t, "creme")
    numero_i(c, "10 ANOS DEPOIS", 520, 230, 96, NAVY, contorno=CREME)
    entra(c, t, 46.9, 640, 420, cartao("Apê", "R$ 485 mil", VERDE, 560), anim="right")
    entra(c, t, 49.6, 640, 545, cartao("Dívida", "- R$ 245 mil", VERMELHO, 560), anim="right")
    if t > 52.0:
        line(c, 380, 618, 900, 618, 6, TINTA)
    entra(c, t, 52.3, 640, 760, selo("R$ 240 MIL", AZUL, 92, CREME), anim="stamp")
    pessoa(c, t, 200, 1300, 1.2, "bruno", poses=((0, "point_r"), (49.6, "shrug"), (52.3, "arms_up")),
           exprs=((0, "happy"), (49.6, "worried"), (52.3, "grin")), look=0.8)


def s08(c, t):  # 55.1 - 59.2  e a Ana? cem mil: menos da metade
    fundo_marca(c, t, "vermelho")
    numero_i(c, "E A ANA?", 520, 230, 104, GOLD)
    barras_i(c, t, 55.3, 160, 1000, 720, 520, dados=(("Bruno", 240000, AZUL), ("Ana", 100000, ROXO)), d=0.9, intervalo=0.5,
             size_val=58, fmt=lambda v: f"R$ {v / 1000:.0f} MIL")
    entra(c, t, 57.8, 540, 1150, selo("MENOS DA METADE", CREME, 60, VERMELHO), anim="stamp")


def s09(c, t):  # 59.2 - 69.3  no MCMV comprar costuma ganhar, se a parcela couber
    cena_sala(c, t, "tarde")
    numero_i(c, "NO MINHA CASA", 520, 230, 84, CREME)
    numero_i(c, "MINHA VIDA", 520, 330, 92, GOLD)
    for i, (lab, t0) in enumerate((("juro mais baixo", 61.3), ("parcela quase fixa", 62.6))):
        def f(c, lab=lab):
            check_icon(c, 30)
            text(c, lab, 50, 4, 56, HAND, NAVY, align="l")
        entra(c, t, t0, 470, 480 + i * 100, f, anim="right")
    entra(c, t, 64.5, 670, 740, selo("COMPRAR COSTUMA GANHAR", VERDE, 40, CREME), anim="stamp")
    entra(c, t, 66.1, 670, 900, selo("SE A PARCELA COUBER", VERMELHO, 46, CREME), anim="pop")
    consultor_i(c, t, 210, 1300, 1.3, poses=((0, "present"), (64.5, "thumb"), (66.1, "finger_up")),
                exprs=((0, "neutral"), (64.5, "happy"), (66.1, "think")), look=0.7)


def s10(c, t):  # 69.3 - 73.9  fora do programa, com juro de banco
    cena_agencia(c, t)
    numero_i(c, "FORA DO PROGRAMA", 520, 320, 84, GOLD)
    entra(c, t, 70.5, 640, 500, selo("JURO DE BANCO", VERMELHO, 56, CREME), anim="drop")
    entra(c, t, 72.0, 640, 680, selo("CONTA APERTADA", NAVY, 56, GOLD), anim="stamp")
    consultor_i(c, t, 230, 1300, 1.35, poses=((0, "point_r"), (72.0, "shrug")), exprs=((0, "neutral"), (72.0, "worried")), look=0.7)


def s11(c, t):  # 73.9 - fim  time Ana ou time Bruno?
    fundo_marca(c, t, "navy", holofote=(520, 1050))
    numero_i(c, "ALUGUEL OU MINHA", 520, 230, 80, CREME)
    numero_i(c, "CASA MINHA VIDA?", 520, 340, 84, GOLD)
    entra(c, t, 76.9, 250, 520, selo("TIME ANA", ROXO, 56, CREME), anim="stamp")
    entra(c, t, 77.5, 760, 520, selo("TIME BRUNO", AZUL, 56, CREME), anim="stamp")
    entra(c, t, 78.5, 510, 690, selo("COMENTA", VERMELHO, 62, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.3, "ana", poses=((0, "stand"), (76.9, "thumb")), exprs=((0, "happy"), (76.9, "grin")), look=0.4)
    pessoa(c, t, 760, 1300, 1.3, "bruno", poses=((0, "stand"), (77.5, "thumb")), exprs=((0, "happy"), (77.5, "grin")), look=-0.4)
    consultor_i(c, t, 505, 1330, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.0)


SCENES = [(0, 6.0, s01), (6.0, 12.9, s02), (12.9, 21.9, s03), (21.9, 30.0, s04), (30.0, 37.2, s05),
          (37.2, 44.3, s06), (44.3, 55.1, s07), (55.1, 59.2, s08), (59.2, 69.3, s09), (69.3, 73.9, s10),
          (73.9, 999.0, s11)]
