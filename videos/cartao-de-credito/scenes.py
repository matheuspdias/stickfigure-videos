"""O que ninguém te conta antes de usar o cartão de crédito (série ep. 5). Só TikTok: vertical nativo 1080x1920, 105,1 s.
Primeiro episódio da série no estilo ilustrado. Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco.
Contas em contas.py: rotativo 451,7% a.a. (BC, set/2026) ~ 15% a.m.; parcelado da fatura 193% a.a. ~ 9,4% a.m.;
R$ 1.000 no rotativo -> R$ 1.150 em 1 mês -> 12x de ~R$ 164 = ~R$ 1.963 (juros ~R$ 963, abaixo do teto de 100%)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(15.2, "tum"), (22.4, "tum"), (57.3, "tum"), (99.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers
def cartao_i(w=420, cor=NAVY, rot=-0.08):
    """cartão de crédito genérico (sem bandeira)"""
    def f(c):
        h = w * 0.63
        c.save(); c.rotate(rot)
        rr(c, -w / 2 + 12, -h / 2 + 16, w, h, 26); rgb(c, (0, 0, 0), 0.25); c.fill()
        rr(c, -w / 2, -h / 2, w, h, 26); lgrad(c, -w / 2, -h / 2, w / 2, h / 2, [(0, lt(cor, 0.25), 1), (1, dk(cor, 0.2), 1)]); c.fill()
        rr(c, -w / 2 + 40, -h / 2 + 60, w * 0.17, w * 0.13, 8); rgb(c, GOLD); c.fill()
        text(c, "•••• •••• •••• 1234", -w / 2 + 40, h * 0.12, w * 0.075, MARKER, CREME, align="l")
        text(c, "CRÉDITO", w / 2 - 34, -h / 2 + 50, w * 0.07, MARKER, GOLD, align="r")
        c.new_sub_path(); c.arc(w / 2 - 90, h / 2 - 50, 26, 0, 6.283); rgb(c, (0.86, 0.30, 0.24), 0.9); c.fill()
        c.new_sub_path(); c.arc(w / 2 - 58, h / 2 - 50, 26, 0, 6.283); rgb(c, GOLD, 0.9); c.fill()
        c.restore()
    return f


def selo(s, cor=VERMELHO, size=64, tcol=CREME, rot=-0.06):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(rot)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def topico(n, s, cor=GOLD):
    """número do tópico (círculo) + título"""
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(70)
        w = c.text_extents(s).x_advance
        x0 = -(w + 130) / 2
        c.new_sub_path(); c.arc(x0 + 50, 0, 52, 0, 6.283); rgb(c, cor); c.fill()
        numero_i(c, n, x0 + 50, 0, 64, NAVY, contorno=CREME)
        numero_i(c, s, x0 + 130, 0, 70, CREME, alinhamento="l")
    return f


def selo_serie(c):
    """selo da série (ilustrado)"""
    rr(c, -440, -100, 880, 200, 30); rgb(c, NAVY); c.fill()
    rr(c, -440, -100, 880, 200, 30); rgb(c, GOLD); c.set_line_width(6); c.stroke()
    numero_i(c, "SÉRIE", -390, -40, 46, GOLD, alinhamento="l")
    numero_i(c, "O que ninguém te conta", -390, 30, 50, CREME, alinhamento="l")
    rr(c, 220, -76, 180, 66, 14); rgb(c, GOLD); c.fill()
    numero_i(c, "EP. 5", 310, -43, 46, NAVY, contorno=CREME)


def check_linha(s, ok=True, w=760):
    def f(c):
        rr(c, -w / 2 + 6, -52 + 8, w, 104, 22); rgb(c, (0, 0, 0), 0.18); c.fill()
        rr(c, -w / 2, -52, w, 104, 22); rgb(c, (0.99, 0.99, 0.98)); c.fill()
        c.save(); c.translate(-w / 2 + 56, 0); check_icon(c, 30); c.restore()
        text(c, s, -w / 2 + 110, 2, 44, HAND, (0.2, 0.2, 0.25), align="l")
    return f


def seta(c, t, t0, x0, y0, x1, y1, col=CREME, lw=12, d=0.4):
    if t < t0:
        return
    k = ease_out(prog(t, t0, d))
    xe, ye = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    line(c, x0, y0, xe, ye, lw, col)
    if k > 0.9:
        a = math.atan2(y1 - y0, x1 - x0)
        c.move_to(x1 + 10 * math.cos(a), y1 + 10 * math.sin(a))
        c.line_to(x1 - 40 * math.cos(a - 0.5), y1 - 40 * math.sin(a - 0.5))
        c.line_to(x1 - 40 * math.cos(a + 0.5), y1 - 40 * math.sin(a + 0.5)); c.close_path()
        rgb(c, col); c.fill()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.6  gancho + selo da série
    fundo_marca(c, t, "navy", holofote=(300, 1000))
    numero_i(c, "CARTÃO DE CRÉDITO", 520, 250, 86, CREME)
    numero_i(c, "PARECE DE GRAÇA?", 520, 370, 96, GOLD)
    entra(c, t, 0.1, 660, 720, cartao_i(440), anim="pop")
    entra(c, t, 2.7, 640, 1010, selo("ANTES DE USAR, SAIBA", VERMELHO, 46, CREME), anim="stamp")
    consultor_i(c, t, 250, 1300, 1.35, poses=((0, "point_r"), (2.6, "finger_up")), exprs=((0, "think"), (2.6, "worried")), look=0.7)
    if 3.4 <= t < 5.6:
        entra(c, t, 3.4, 520, 560, selo_serie, anim="stamp", t1=5.3)


def s02(c, t):  # 5.6 - 16.0  1. pagamento mínimo
    cena_escritorio(c, t, "dia")
    entra(c, t, 5.8, 520, 250, topico("1", "O MÍNIMO"), anim="stamp")
    entra(c, t, 8.4, 610, 620, lambda c: fatura(c, t, 0, 0, 1.0, (("Mercado", "R$ 640"), ("Farmácia", "R$ 210"), ("Roupa", "R$ 350")),
                                                 "R$ 1.200", "Vence dia 10", minimo="R$ 200", t0=8.6), anim="drop")
    entra(c, t, 11.2, 640, 930, selo("PAGOU R$ 200", VERDE, 50, CREME), anim="pop")
    entra(c, t, 12.6, 640, 1060, lambda c: numero_i(c, "SOBRAM R$ 1.000", 0, 0, 62, CREME), anim="up")
    entra(c, t, 14.8, 640, 1180, selo("VIRA ROTATIVO", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 200, 1300, 1.25, poses=((0, "present"), (12.6, "shrug"), (14.8, "head")),
                exprs=((0, "neutral"), (12.6, "worried"), (14.8, "shocked")), look=0.8)


def s03(c, t):  # 16.0 - 26.6  os juros do rotativo
    fundo_marca(c, t, "vermelho", holofote=(270, 1000))
    numero_i(c, "JUROS DO ROTATIVO", 520, 250, 84, CREME)
    contador(c, t, 21.2, 0, 451, 520, 440, 200, d=1.6, col=GOLD, prefixo="", sufixo="%")
    if t > 23.4:
        numero_i(c, "AO ANO", 520, 590, 84, CREME)
    entra(c, t, 20.2, 640, 700, lambda c: text(c, "média do Banco Central (set/2026)", 0, 0, 38, HAND, CREME), anim="up")
    entra(c, t, 25.0, 640, 900, selo("~15% AO MÊS", NAVY, 66, GOLD), anim="stamp")
    consultor_i(c, t, 230, 1300, 1.3, poses=((0, "point_r"), (22.4, "head")), exprs=((0, "worried"), (22.4, "shocked")), look=0.6)


def s04(c, t):  # 26.6 - 34.0  a conta: 1.000 vira 1.150
    fundo_marca(c, t, "creme")
    numero_i(c, "VAMOS FAZER A CONTA", 520, 250, 74, NAVY, contorno=CREME)
    entra(c, t, 28.0, 560, 400, lambda c: numero_i(c, "R$ 1.000", 0, 0, 120, NAVY, contorno=CREME), anim="pop")
    if t > 29.7:
        seta(c, t, 29.7, 560, 480, 560, 600, VERMELHO)
        entra(c, t, 29.8, 740, 540, lambda c: text(c, "1 mês", 0, 0, 50, HAND, VERMELHO), anim="fade")
    contador(c, t, 30.6, 1000, 1150, 580, 690, 140, d=1.2, col=VERMELHO)
    entra(c, t, 32.5, 660, 900, selo("+ IOF", NAVY, 60, GOLD), anim="stamp")
    consultor_i(c, t, 170, 1300, 1.15, poses=((0, "stand"), (30.6, "point_r")), exprs=((0, "neutral"), (30.6, "worried")), look=0.7,
                prop=("l", prop_calc_i))


def s05(c, t):  # 34.0 - 42.9  2. rotativo só até a próxima fatura
    cena_sala(c, t, "tarde")
    entra(c, t, 34.1, 520, 250, topico("2", "SÓ 1 MÊS"), anim="stamp")
    entra(c, t, 35.4, 600, 470, selo("ATÉ A PRÓXIMA FATURA", NAVY, 44, CREME, rot=0.02), anim="up")
    entra(c, t, 39.6, 600, 700, lambda c: notificacao(c, 0, 0, 1.15, "Parcele sua fatura", "em até 12x", NAVY, "BANCO"), anim="drop")
    entra(c, t, 41.8, 640, 920, selo("PARECE ALÍVIO", VERDE, 54, CREME), anim="pop")
    consultor_i(c, t, 200, 1300, 1.3, poses=((0, "finger_up"), (39.6, "present"), (41.8, "relax")),
                exprs=((0, "think"), (39.6, "neutral"), (41.8, "happy")), look=0.8)


def s06(c, t):  # 42.9 - 48.2  mas o parcelamento tem juros
    fundo_marca(c, t, "vermelho", holofote=(270, 1000))
    numero_i(c, "MAS O PARCELAMENTO", 520, 250, 78, CREME)
    numero_i(c, "TAMBÉM TEM JUROS", 520, 360, 78, GOLD) if t > 44.6 else None
    contador(c, t, 46.4, 0, 9, 600, 620, 220, d=0.9, col=GOLD, prefixo="~", sufixo="%")
    numero_i(c, "AO MÊS", 600, 790, 84, CREME) if t > 47.5 else None
    consultor_i(c, t, 220, 1300, 1.3, poses=((0, "finger_up"), (45.2, "hips")), exprs=((0, "worried"), (45.2, "angry")), look=0.7)


def s07(c, t):  # 48.2 - 59.2  12x de 164 = quase o dobro
    fundo_marca(c, t, "creme")
    numero_i(c, "R$ 1.150 EM 12X", 520, 250, 86, NAVY, contorno=CREME)
    entra(c, t, 52.0, 520, 390, lambda c: numero_i(c, "12 x R$ 164", 0, 0, 96, VERMELHO), anim="pop")
    if t > 55.0:
        barras_i(c, t, 55.0, 330, 1000, 560, 380, dados=(("devia", 1000, NAVY), ("paga", 1963, VERMELHO)), maxv=2000,
                 fmt=lambda v: brl(round(v / 10) * 10), d=1.0, intervalo=0.4, size_val=58)
    entra(c, t, 57.3, 560, 1150, selo("QUASE O DOBRO", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 170, 1300, 1.15, poses=((0, "present"), (55.2, "point_r"), (57.4, "head")),
                exprs=((0, "neutral"), (55.2, "worried"), (57.4, "shocked")), look=0.8)


def s08(c, t):  # 59.2 - 75.0  3. teto de 100% por lei
    fundo_marca(c, t, "navy", holofote=(220, 1000))
    entra(c, t, 59.3, 520, 250, topico("3", "TETO POR LEI"), anim="stamp")
    entra(c, t, 61.0, 600, 380, lambda c: text(c, "desde 2024: juros e encargos até 100% da dívida", 0, 0, 34, HAND, CREME), anim="up")
    # pilha: dívida + juros máximos, com a linha do teto
    x0, yb, w = 480, 1120, 300
    if t > 69.3:
        k = ease_out(prog(t, 69.3, 0.6))
        rr(c, x0, yb - 300 * k, w, 300 * k, 14); rgb(c, NAVY if False else (0.36, 0.46, 0.70)); c.fill()
        numero_i(c, "R$ 1.000", x0 + w / 2, yb - 150, 52, CREME) if k > 0.9 else None
        text(c, "dívida", x0 + w + 20, yb - 150, 40, HAND, CREME, align="l")
    if t > 71.3:
        k = ease_out(prog(t, 71.3, 0.6))
        rr(c, x0, yb - 300 - 300 * k, w, 300 * k, 14); rgb(c, VERMELHO); c.fill()
        numero_i(c, "+ R$ 1.000", x0 + w / 2, yb - 450, 50, CREME) if k > 0.9 else None
        text(c, "juros", x0 + w + 20, yb - 450, 40, HAND, CREME, align="l")
    if t > 72.6:
        for i in range(10):
            line(c, x0 - 40 + i * 40, yb - 615, x0 - 14 + i * 40, yb - 615, 8, GOLD)
        numero_i(c, "TETO", x0 - 70, yb - 615, 52, GOLD, alinhamento="r") if x0 - 70 > 250 else numero_i(c, "TETO", x0 + w / 2, yb - 680, 56, GOLD)
    entra(c, t, 73.8, 630, 1210, selo("NÃO É DESCONTO", VERMELHO, 52, CREME), anim="stamp")
    consultor_i(c, t, 210, 1300, 1.25, poses=((0, "present"), (69.3, "point_r"), (73.8, "finger_up")),
                exprs=((0, "confident"), (69.3, "neutral"), (73.8, "worried")), look=0.8)


def s09(c, t):  # 75.0 - 84.8  4. anuidade
    cena_escritorio(c, t, "tarde")
    entra(c, t, 75.2, 520, 250, topico("4", "ANUIDADE"), anim="stamp")
    entra(c, t, 77.2, 610, 600, lambda c: fatura(c, t, 0, 0, 1.0, (("Mercado", "R$ 640"), ("Gasolina", "R$ 250"), ("Anuidade 3/12", "R$ 35")),
                                                  "R$ 925", "Vence dia 10", t0=77.4), anim="drop")
    if t > 79.6:
        k = ease_out(prog(t, 79.6, 0.4))
        c.save(); c.translate(610, 600 - 190 + 140 + 2 * 60 - 12); c.scale(k, k)
        c.new_sub_path(); ellipse(c, 0, 0, 270, 46); rgb(c, VERMELHO); c.set_line_width(8); c.stroke(); c.restore()
    entra(c, t, 81.6, 640, 930, selo("PEÇA ISENÇÃO", VERDE, 54, CREME), anim="pop")
    entra(c, t, 83.3, 620, 1070, selo("OU CARTÃO SEM ANUIDADE", NAVY, 40, CREME, rot=0.03), anim="up")
    consultor_i(c, t, 190, 1300, 1.25, poses=((0, "point_r"), (81.6, "finger_up")), exprs=((0, "think"), (81.6, "confident")), look=0.8)


def s10(c, t):  # 84.8 - 89.8  limite não é dinheiro seu
    cena_agencia(c, t)
    numero_i(c, "LIMITE ALTO", 520, 250, 100, GOLD)
    numero_i(c, "NÃO É DINHEIRO SEU", 520, 370, 76, CREME) if t > 85.9 else None
    entra(c, t, 84.9, 650, 700, lambda c: celular_app(c, t, 0, 0, 0.85, "Limite disponível", "R$ 8.000", linhas=(("Mercado", "R$ 0", NAVY), ("Fatura", "R$ 0", NAVY))), anim="pop")
    entra(c, t, 87.4, 640, 1080, selo("É QUANTO O BANCO", VERMELHO, 46, CREME, rot=-0.03), anim="stamp")
    entra(c, t, 88.2, 640, 1190, selo("ACEITA QUE VOCÊ DEVA", VERMELHO, 46, CREME, rot=0.02), anim="stamp")
    consultor_i(c, t, 220, 1300, 1.3, poses=((0, "finger_up"), (87.4, "point_r")), exprs=((0, "think"), (87.4, "worried")), look=0.8)


def s11(c, t):  # 89.8 - 99.1  antes de usar: checklist
    fundo_marca(c, t, "creme")
    numero_i(c, "ANTES DE USAR", 520, 250, 96, NAVY, contorno=CREME)
    itens = ((91.2, "pague a fatura inteira"), (94.6, "não deu? compare com"), (97.6, "confira a anuidade"))
    for i, (t0, s_) in enumerate(itens):
        entra(c, t, t0, 600, 440 + i * 160, check_linha(s_, w=640), anim="right")
    entra(c, t, 96.0, 640, 668, lambda c: text(c, "empréstimo mais barato", 0, 0, 38, HAND, (0.35, 0.35, 0.4)), anim="fade")
    consultor_i(c, t, 170, 1300, 1.15, poses=((0, "present"), (97.6, "thumb")), exprs=((0, "neutral"), (97.6, "happy")), look=0.6)


def s12(c, t):  # 99.1 - fim  segue + pergunta
    cena_sala(c, t, "tarde")
    numero_i(c, "SEGUE PRO EP. 6", 520, 250, 96, GOLD)
    entra(c, t, 102.3, 520, 390, selo("MEI", NAVY, 70, GOLD, rot=-0.04), anim="pop")
    entra(c, t, 102.8, 520, 495, lambda c: numero_i(c, "OU", 0, 0, 56, CREME), anim="pop")
    entra(c, t, 103.0, 520, 600, selo("EMPRÉSTIMO PESSOAL", NAVY, 54, GOLD, rot=0.03), anim="pop")
    entra(c, t, 104.3, 520, 735, selo("COMENTA", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 280, 1300, 1.15, poses=((0, "wave"), (101.5, "present")), exprs=((0, "happy"), (101.5, "grin")), look=0.6)
    pessoa(c, t, 760, 1300, 1.12, "bruno", poses=((0, "think_l"),), exprs=((0, "think"),), look=-0.5)


SCENES = [(0, 5.6, s01), (5.6, 16.0, s02), (16.0, 26.6, s03), (26.6, 34.0, s04), (34.0, 42.9, s05), (42.9, 48.2, s06),
          (48.2, 59.2, s07), (59.2, 75.0, s08), (75.0, 84.8, s09), (84.8, 89.8, s10), (89.8, 99.1, s11), (99.1, 999.0, s12)]
