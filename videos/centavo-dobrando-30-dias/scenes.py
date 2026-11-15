"""E se o seu dinheiro dobrasse todo dia, começando com 1 centavo? Só TikTok: vertical 1080x1920, ~84,5 s, estilo ilustrado.
Formato "E se..." das 10h (AUTOMATICO_TIKTOK.md 2c), sem cartaz de abertura (2b.1): no quadro 0 o saldo já está dobrando.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (dia n = 0,01 x 2^(n-1); CDI 13,65% a.a., IR 15%)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(27.3, "tum"), (43.3, "soft_ding"), (56.3, "tum"), (82.8, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

VOCE = "lucas"


def dia_v(n):
    return 0.01 * 2 ** (n - 1)


def topo(c, s, cor=CREME, contorno=TINTA):
    """título pequeno no topo (regra 2b.1)"""
    numero_i(c, s, 520, 235, 58, cor, contorno=contorno)


def selo(s, cor=VERMELHO, size=60, tcol=CREME, rot=-0.06):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(rot)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def pop(c, t, t0, x, y, s, size, col=GOLD, contorno=TINTA):
    if t < t0:
        return
    k = 1 + 0.14 * math.sin(clamp01((t - t0) / 0.3) * math.pi)
    c.save(); c.translate(x, y); c.scale(k, k); numero_i(c, s, 0, 0, size, col, contorno=contorno); c.restore()


def cal(c, t, x, y, dia, s=1.6, cor=VERMELHO):
    """calendário com 'DIA n' (pula de leve quando muda)"""
    c.save(); c.translate(x, y); c.scale(s, s); calendar(c, "%d" % dia, cor); c.restore()
    text(c, "DIA", x, y - 86 * s - 18, 40, MARKER, CREME)


def dobra(c, t, x, y, s=1.0):
    """selo 'x2' pulsando"""
    k = 1 + 0.12 * math.sin(t * 7)
    c.save(); c.translate(x, y); c.scale(s * k, s * k); c.rotate(0.08)
    c.new_sub_path(); c.arc(0, 0, 78, 0, 6.283); rgb(c, VERMELHO); c.fill()
    c.new_sub_path(); c.arc(0, 0, 78, 0, 6.283); rgb(c, TINTA); c.set_line_width(6); c.stroke()
    numero_i(c, "x2", 0, 4, 80, CREME)
    c.restore()


def moedinhas(c, t, n, x0, y0, cols=8, r=26, gap=64, t0=None, d=0.03):
    """n moedas de 1 centavo em grade (aparecem uma a uma a partir de t0)"""
    for i in range(n):
        if t0 is not None and t < t0 + i * d:
            break
        x = x0 + (i % cols) * gap; y = y0 + (i // cols) * gap
        c.save(); c.translate(x, y); moeda_i(c, r); c.restore()


def barras_dias(c, t, t0, x, y, w, h, ate=30, destaque=30, d=2.0):
    """30 barras, uma por dia, altura proporcional ao saldo do dia (dia 30 = 100%)"""
    bw = w / 30
    c.rectangle(x - 10, y, w + 20, 5); rgb(c, CREME); c.fill()
    for n in range(1, ate + 1):
        tn = t0 + d * (n - 1) / 29
        if t < tn:
            break
        k = ease_out(prog(t, tn, 0.35))
        hh = max(3, h * dia_v(n) / dia_v(30) * k)
        rr(c, x + (n - 1) * bw + 2, y - hh, bw - 4, hh, 4)
        rgb(c, GOLD if n == destaque else VERDE); c.fill()
    text(c, "dia 1", x, y + 44, 32, HAND, CREME, align="l")
    text(c, "dia 30", x + w, y + 44, 32, HAND, CREME, align="r")


# ======================================================================= CENAS
def s01(c, t):  # 0 - 7.9  um centavo, dobrando: 1, 2, 4
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    topo(c, "E SE DOBRASSE TODO DIA?")
    # já em movimento no quadro 0: o x2 pulsando e o saldo piscando 0,01 -> 0,02 -> 0,04
    n = 1 if t < 5.2 else (2 if t < 6.6 else 4)
    dia = 1 if t < 5.2 else (2 if t < 6.6 else 3)
    cal(c, t, 760, 520, dia, 1.4)
    dobra(c, t, 500, 480, 1.0)
    if n == 1:
        pop(c, t, 0.0, 660, 780, "R$ 0,01", 150, GOLD)
        # moeda caindo e quicando no quadro 0
        k = clamp01(t / 0.7)
        y = 950 - 250 * (1 - ease_out(k)) - 40 * abs(math.sin(min(t, 1.6) * 5)) * (1 - clamp01(t / 1.6))
        c.save(); c.translate(560, y); c.rotate(t * 4 * (1 - clamp01(t / 1.6))); moeda_i(c, 48); c.restore()
    else:
        contador(c, t, 5.2 if n == 2 else 6.6, dia_v(dia) / 2, dia_v(dia), 660, 780, 150, d=0.4, col=GOLD, casas=2)
        moedinhas(c, t, n, 560, 950, cols=4, r=48, gap=120)
    if t > 2.4:
        entra(c, t, 2.4, 640, 1130, selo("COMEÇANDO COM 1 CENTAVO", VERMELHO, 44, CREME), anim="stamp")
    pessoa(c, t, 190, 1300, 1.3, VOCE, poses=((0, "point_r"), (2.4, "think"), (6.6, "head")),
           exprs=((0, "think"), (2.4, "neutral"), (6.6, "grin")), look=0.6)


def s02(c, t):  # 7.9 - 12.7  uma semana: 64 centavos, não paga nem uma bala
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "UMA SEMANA DEPOIS", NAVY, CREME)
    cal(c, t, 860, 470, 7, 1.1)
    contador(c, t, 8.6, 0.04, 0.64, 400, 470, 140, d=1.6, col=NAVY, casas=2)
    moedinhas(c, t, 64, 320, 640, cols=8, r=24, gap=62, t0=8.8, d=0.02)
    if t > 11.3:
        entra(c, t, 11.3, 560, 1170, selo("BALA: R$ 1", GOLD, 56, TINTA, rot=0.03), anim="pop")
        entra(c, t, 11.9, 560, 1170, lambda c: (line(c, -150, -60, 150, 60, 14, VERMELHO), line(c, -150, 60, 150, -60, 14, VERMELHO)), anim="stamp")
    pessoa(c, t, 220, 1330, 1.1, VOCE, poses=((0, "stand"), (11.3, "shrug")), exprs=((0, "think"), (11.3, "desperate")), look=0.6)


def s03(c, t):  # 12.7 - 16.9  dia 10: R$ 5,12, um pão de queijo
    luz("dia")
    cena_padaria(c, t, hora="dia", cardapio=(("PÃO DE QUEIJO", "R$ 5"), ("CAFÉ", "R$ 6")))
    rr(c, 90, 180, 900, 110, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "DIA 10", 540, 235, 58, CREME)
    contador(c, t, 13.3, 0.64, 5.12, 600, 470, 150, d=1.4, col=GOLD, casas=2)
    if t > 15.9:
        entra(c, t, 15.9, 640, 640, selo("= 1 PÃO DE QUEIJO", GOLD, 58, TINTA, rot=0.04), anim="stamp")
    pessoa(c, t, 300, 1300, 1.3, VOCE, poses=((0, "stand"), (15.9, "shrug")), exprs=((0, "neutral"), (15.9, "grin")), look=0.6)


def s04(c, t):  # 16.9 - 23.0  dia 15: R$ 163,84, metade do mês, não paga a conta de luz
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "METADE DO MÊS", NAVY, CREME)
    cal(c, t, 840, 480, 15, 1.1, NAVY)
    contador(c, t, 17.9, 5.12, 163.84, 390, 480, 110, d=1.5, col=VERDE, casas=2)
    # barra do mês: 50%
    k = ease_out(prog(t, 19.9, 0.8))
    rr(c, 180, 640, 700, 56, 20); rgb(c, (0.85, 0.82, 0.76)); c.fill()
    rr(c, 180, 640, 700 * 0.5 * k, 56, 20); rgb(c, NAVY); c.fill()
    text(c, "15 de 30 dias", 530, 750, 40, HAND, NAVY)
    if t > 21.8:
        def conta(c):
            papel(c, 420, 230)
            c.rectangle(-210, -115, 420, 70); rgb(c, GOLD); c.fill()
            text(c, "CONTA DE LUZ", 0, -64, 40, MARKER, TINTA)
            text(c, "VENCE DIA 10", 0, 20, 36, HAND, TINTA)
            text(c, "NÃO DÁ!", 0, 82, 50, MARKER, VERMELHO)
        entra(c, t, 21.8, 640, 1000, conta, anim="drop")
    pessoa(c, t, 210, 1330, 1.1, VOCE, poses=((0, "point_r"), (21.8, "head")), exprs=((0, "think"), (21.8, "desperate")), look=0.6)


def s05(c, t):  # 23.0 - 28.3  quase todo mundo desistiria. parece pouco? olha a virada
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(520, 1100))
    topo(c, "É AQUI QUE TODO MUNDO DESISTE")
    if t < 26.1:
        numero_i(c, "R$ 163,84", 520, 470, 110, CREME, alpha=0.9)
        numero_i(c, "15 DIAS DEPOIS...", 520, 590, 56, GOLD)
    if t > 26.1:
        pop(c, t, 26.1, 520, 400, "PARECE POUCO?", 90, CREME)
    if t > 27.3:
        pop(c, t, 27.3, 520, 540, "OLHA A VIRADA", 100, GOLD)
    consultor_i(c, t, 520, 1300, 1.4, poses=((0, "shrug"), (27.3, "finger_up")), exprs=((0, "think"), (27.3, "confident")), look=0.0)


def s06(c, t):  # 28.3 - 35.1  dia 20: R$ 5.242, mais de 3 salários mínimos
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(230, 1100))
    topo(c, "DIA 20")
    contador(c, t, 28.6, 163.84, 5242.88, 560, 430, 120, d=3.0, col=GOLD, casas=2)
    for i in range(3):
        ti = 33.3 + i * 0.25
        if t > ti:
            entra(c, t, ti, 480 + i * 170, 760 - i * 20, lambda c: contracheque(c, 0, 0, 0.5, bruto="R$ 1.621",
                  descontos=(("INSS", "- R$ 122"),), liquido="R$ 1.499"), anim="drop")
    if t > 33.9:
        entra(c, t, 33.9, 600, 1070, selo("+ DE 3 SALÁRIOS MÍNIMOS", NAVY, 42, GOLD), anim="stamp")
    consultor_i(c, t, 170, 1300, 1.15, poses=((0, "present"), (33.3, "point_r")), exprs=((0, "neutral"), (33.3, "shocked")), look=0.6)


def s07(c, t):  # 35.1 - 38.5  dia 25: R$ 167 mil
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "DIA 25")
    cal(c, t, 540, 470, 25, 1.3, VERDE)
    contador(c, t, 35.6, 5242.88, 167772.16, 540, 720, 120, d=2.2, col=GOLD, casas=2)
    if t > 37.2:
        for i in range(4):
            c.save(); c.translate(330 + i * 140, 890); maco(c, "100", 4 + i, 150); c.restore()
    pessoa(c, t, 540, 1490, 1.0, VOCE, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.0)


def s08(c, t):  # 38.5 - 44.5  dia 28: R$ 1,34 milhão, milionário
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(540, 1150))
    topo(c, "DIA 28")
    cal(c, t, 800, 450, 28, 1.1, VERDE)
    contador(c, t, 38.9, 167772.16, 1342177.28, 470, 630, 100, d=3.2, col=GOLD, casas=2)
    if t > 43.3:
        chuva_dinheiro(c, t, 43.3, n=22, seed=4)
        entra(c, t, 43.3, 540, 830, selo("MILIONÁRIO", GOLD, 96, TINTA, rot=0.04), anim="stamp")
    pessoa(c, t, 540, 1440, 1.0, VOCE, poses=((0, "think"), (43.3, "arms_up")), exprs=((0, "think"), (43.3, "grin")), look=0.0)


def s09(c, t):  # 44.5 - 55.6  dia 30: R$ 5,37 milhões; pilha de notas de 100 de quase 6 m, mais de 50 kg
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "DIA 30")
    contador(c, t, 45.2, 1342177.28, 5368709.12, 540, 380, 96, d=3.6, col=GOLD, casas=2)
    # pilha de notas crescendo ao lado do Lucas (1,75 m ~ 300 px -> 6 m ~ 1000 px)
    base = 1300
    if t > 49.9:
        hmax = 860 * ease_out(prog(t, 50.1, 2.6))
        n = int(hmax / 14)
        for i in range(n):
            c.save(); c.translate(640 + (i % 3 - 1) * 2, base - i * 14); c.scale(1, 0.18); nota_i(c, "100", 260); c.restore()
        if t > 52.2:
            line(c, 820, base, 820, base - 860, 5, CREME)
            line(c, 800, base - 860, 840, base - 860, 5, CREME)
            numero_i(c, "QUASE 6 m", 890, base - 430, 50, GOLD, inclina=-1.5708)
    if 46.4 < t < 50.1:
        entra(c, t, 46.4, 540, 560, selo("5,3 MILHÕES!", VERDE, 80, CREME), anim="stamp")
        chuva_dinheiro(c, t, 46.4, n=16, seed=9)
    if t > 53.9:
        entra(c, t, 53.9, 280, 560, selo("+ DE 50 KG", VERMELHO, 60, CREME), anim="stamp")
    pessoa(c, t, 360, base, 0.95, VOCE, poses=((0, "stand"), (50.1, "head")), exprs=((0, "grin"), (50.1, "shocked")), look=0.7)


def s10(c, t):  # 55.6 - 59.3  metade de tudo apareceu só no último dia
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "REPARA NO GRÁFICO")
    barras_dias(c, t, 55.6, 150, 900, 760, 480, d=1.0)
    if t > 57.4:
        entra(c, t, 57.4, 520, 370, selo("METADE SÓ NO DIA 30", VERMELHO, 56, CREME), anim="stamp")
    if t > 56.6:
        text(c, "dias 1 a 20: quase zero", 420, 860, 38, HAND, CREME)
    consultor_i(c, t, 540, 1420, 0.85, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.6)


def s11(c, t):  # 59.3 - 65.8  vida real: no CDI, sem imposto, dobra a cada ~6 anos
    luz("dia")
    cena_escritorio(c, t, hora="dia")
    rr(c, 90, 180, 900, 110, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "AGORA, A VIDA REAL", 540, 235, 58, CREME)
    if t > 61.2:
        celular_app(c, t, 680, 680, 0.95, titulo="Rendendo 100% do CDI", valor="x2", sub="a cada uns 6 anos",
                    curva=lambda k: k ** 2.0, cor=NAVY, t0=61.4, d=2.4)
    consultor_i(c, t, 260, 1300, 1.3, poses=((0, "present"), (63.8, "hold")), prop=("r", prop_tablet_i),
                exprs=((0, "neutral"), (63.8, "think")), look=0.6)


def s12(c, t):  # 65.8 - 71.3  29 dobradas: mais de 180 anos
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(540, 1200))
    topo(c, "AS MESMAS 29 DOBRADAS")
    anos = int(183 * ease_io(prog(t, 67.0, 3.2)))
    numero_i(c, "%d ANOS" % anos, 540, 520, 150, GOLD)
    if t > 69.4:
        entra(c, t, 69.4, 540, 700, selo("MAIS DE 180 ANOS", NAVY, 64, CREME), anim="stamp")
    pessoa(c, t, 360, 1300, 1.1, VOCE, poses=((0, "stand"), (69.4, "shrug")), exprs=((0, "think"), (69.4, "desperate")), look=0.6)
    pessoa(c, t, 700, 1300, 1.1, "aposentado", poses=((0, "stand"),), exprs=((0, "grin"),), look=-0.6) if t > 70.3 else None


def s13(c, t):  # 71.3 - 77.9  o segredo é o tempo; quem começa cedo
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(540, 1150))
    topo(c, "O SEGREDO")
    if t > 71.6:
        numero_i(c, "NÃO É SÓ A TAXA", 540, 400, 72, CREME)
    if t > 73.4:
        pop(c, t, 73.4, 540, 540, "É O TEMPO", 130, GOLD)
    grafico_curva(c, t, 74.6, 300, 1000, w=480, h=280, d=2.4, cor=GOLD, eixo_x=("começa cedo", "dias bons"))
    consultor_i(c, t, 170, 1320, 1.0, poses=((0, "finger_up"), (74.6, "point_r")), exprs=((0, "confident"), (74.6, "grin")), look=0.6)


def s14(c, t):  # 77.9 - fim  1 milhão agora ou o centavo que dobra? comenta
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "QUAL VOCÊ PEGAVA?")
    entra(c, t, 78.5, 520, 480, selo("R$ 1 MILHÃO AGORA", VERDE, 64, CREME, rot=-0.05), anim="left")
    if t > 79.8:
        pop(c, t, 79.8, 520, 640, "OU", 90, GOLD)
    entra(c, t, 80.2, 520, 800, selo("1 CENTAVO x2 POR 30 DIAS", VERMELHO, 52, CREME, rot=0.05), anim="right")
    entra(c, t, 82.8, 520, 960, selo("COMENTA", GOLD, 72, TINTA), anim="stamp")
    pessoa(c, t, 220, 1420, 0.9, VOCE, poses=((0, "think"),), exprs=((0, "think"),), look=0.5)
    consultor_i(c, t, 800, 1420, 0.9, poses=((0, "present"), (82.8, "point_l")), exprs=((0, "grin"),), look=-0.5)


SCENES = [(0, 7.9, s01), (7.9, 12.7, s02), (12.7, 16.9, s03), (16.9, 23.0, s04), (23.0, 28.3, s05),
          (28.3, 35.1, s06), (35.1, 38.5, s07), (38.5, 44.5, s08), (44.5, 55.6, s09), (55.6, 59.3, s10),
          (59.3, 65.8, s11), (65.8, 71.3, s12), (71.3, 77.9, s13), (77.9, 999.0, s14)]
