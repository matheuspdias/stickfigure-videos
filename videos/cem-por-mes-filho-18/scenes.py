"""R$ 100 POR MÊS DESDE QUE O FILHO NASCE: QUANTO ELE TEM AOS 18? (TikTok vertical, ~83,6 s, estilo ilustrado).
Item [18h] da "Fila do Matheus". Contas em contas.py, tudo em dinheiro de hoje (IPCA ~4,5% a.a.):
216 meses x R$ 100 = R$ 21.600; gaveta ~R$ 15 mil; poupança (~2% real) ~R$ 25-26 mil; Tesouro IPCA+ (~IPCA + 7,5% em 16/11/2026,
IR 15%) ~R$ 37 mil de hoje (~R$ 82 mil nominais, "mais de 70 mil"). Custo de criar um filho: estudo Bora Investir (B3)/Plano 2022,
renda de R$ 2,9 a 7,1 mil: R$ 281 a 343 mil até os 18 (~R$ 1.400/mês); R$ 100 = 7%. R$ 200/mês ~ R$ 74 mil de hoje."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (15.3, "tum"), (25.7, "tum"), (39.5, "soft_ding"), (47.3, "tum"), (62.1, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

# nome, valor de hoje, início do destaque, quando a barra cresce, fim do destaque
LINHAS = [("GAVETA", 15000, 15.3, 15.8, 25.7), ("POUPANÇA", 25000, 25.7, 28.3, 31.5), ("TESOURO IPCA+", 37000, 31.5, 39.5, 46.8)]
X0, WMAX, VMAX = 420, 440, 40000.0
L1, L2, R1, R2 = (250, 1000), (250, 1115), (800, 1000), (800, 1115)
C1 = (540, 1000)


def chip(s, cor=CREME, tcol=TINTA, size=44, rot=0.0):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 56
        c.save(); c.rotate(rot)
        rr(c, -w / 2 + 6, -size * 0.75 + 8, w, size * 1.5, 18); rgb(c, (0, 0, 0), 0.25); c.fill()
        rr(c, -w / 2, -size * 0.75, w, size * 1.5, 18); rgb(c, cor); c.fill()
        text(c, s, 0, size * 0.36, size, MARKER, tcol)
        c.restore()
    return f


def painel(c):
    rr(c, 60 + 8, 290 + 10, 870, 480, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 60, 290, 870, 480, 30); rgb(c, CREME); c.fill()


def valor_barra(i, v, t, tg):
    if t < tg:
        return 0.0
    if i == 0:  # gaveta: aparece com os 21.600 e a inflação come até 15 mil
        if t < 21.0:
            return 21600 * ease_out(clamp01((t - tg) / 0.9))
        return 21600 - 6600 * ease_out(clamp01((t - 21.0) / 1.2))
    return v * ease_out(clamp01((t - tg) / 0.9))


def tabela(c, t):
    painel(c)
    text(c, "AOS 18 ANOS, EM DINHEIRO DE HOJE", 495, 345, 38, MARKER, NAVY)
    for i, (nome, v, th, tg, tf) in enumerate(LINHAS):
        y = 450 + i * 105
        if th <= t < tf:
            rr(c, 76, y - 42, 838, 84, 18); rgb(c, GOLD, 0.35); c.fill()
        text(c, nome, 92, y + 14, 40, MARKER, NAVY, align="l")
        vv = valor_barra(i, v, t, tg)
        if vv < 1:
            c.move_to(X0, y + 4); c.line_to(X0 + WMAX, y + 4); rgb(c, TINTA, 0.22); c.set_line_width(4)
            c.set_dash([12, 10]); c.stroke(); c.set_dash([])
            continue
        w = WMAX * vv / VMAX
        cor = (VERMELHO if i == 0 and t >= 21.0 else (0.45, 0.62, 0.80) if i == 1 else VERDE)
        if i == 0 and t >= 21.0:  # contorno do que foi depositado
            wb = WMAX * 21600 / VMAX
            c.set_dash([10, 8]); rr(c, X0, y - 30, wb, 60, 12); rgb(c, TINTA, 0.5); c.set_line_width(4); c.stroke(); c.set_dash([])
        rr(c, X0, y - 30, w, 60, 12); rgb(c, cor); c.fill()
        s = "R$ " + f"{vv/1000:.0f} mil"
        if w > 200:
            text(c, s, X0 + w - 14, y + 13, 40, MARKER, CREME, align="r")
        else:
            text(c, s, X0 + w + 10, y + 13, 38, MARKER, TINTA, align="l")
    if t < 15.3:
        text(c, "QUANTO ELE TEM?", 495, 740, 44, MARKER, VERMELHO)
    elif t >= 41.1:
        a = clamp01((t - 41.1) / 0.4)
        text(c, "NA TELA DO BANCO: + DE R$ 70 MIL", 495, 740, 38, MARKER, VERMELHO, alpha=a)


def custo(c, t):
    painel(c)
    text(c, "CRIAR UM FILHO ATÉ OS 18", 495, 350, 46, MARKER, NAVY)
    text(c, "estudo Bora Investir (B3), 2022 · renda média", 495, 395, 28, MARKER, TINTA)
    if t >= 52.3:
        contador(c, t, 52.3, 0, 300000, 495, 480, 96, d=1.2, col=VERMELHO)
    # barra: R$ 1.400 por mês, os R$ 100 = 7%
    if t >= 55.8:
        k = ease_out(clamp01((t - 55.8) / 0.8))
        rr(c, 110, 560, 770 * k, 70, 16); rgb(c, VERMELHO, 0.85); c.fill()
        text(c, "R$ 1.400 POR MÊS", 110 + 770 * k - 16, 608, 40, MARKER, CREME, align="r") if k > 0.6 else None
    if t >= 57.6:
        k = ease_out(clamp01((t - 57.6) / 0.5))
        rr(c, 110, 650, 770 * 0.0714 * k + 1, 70, 16); rgb(c, VERDE); c.fill()
        text(c, "R$ 100 = SÓ 7%", 190, 698, 40, MARKER, VERDE, align="l")


def usos(c, t):
    painel(c)
    text(c, "R$ 37 MIL AOS 18 É...", 495, 355, 48, MARKER, NAVY)
    for i, (t0, s) in enumerate(((63.8, "A ENTRADA DE UM APÊ"), (65.1, "UM CARRO USADO À VISTA"), (66.4, "BOA PARTE DA FACULDADE"))):
        if t >= t0:
            y = 450 + i * 95
            k = ease_out(clamp01((t - t0) / 0.4))
            c.save(); c.rectangle(80, y - 45, 830 * k, 90); c.clip()
            rr(c, 90, y - 38, 810, 76, 18); rgb(c, GOLD, 0.35); c.fill()
            text(c, "✓ " + s if False else s, 130, y + 16, 44, MARKER, TINTA, align="l")
            c.restore()
    if t >= 62.1 and t < 63.8:
        numero_i(c, "R$ 37 MIL", 495, 520, 110, VERDE)


def marcador(c, t):
    yc = 860
    if t >= 80.6:
        k = 1 + 0.12 * math.sin(clamp01((t - 80.6) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -410, -70, 820, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "R$ 100/MÊS = R$ 37 MIL", 0, 26, 60, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    def lab(s):
        text(c, s, 330, yc + 20, 42, MARKER, CREME)
    if t < 8.1:
        lab("MÊS")
        contador(c, t, 0.0, 1, 216, 700, yc, 84, d=7.6, col=VERDE, prefixo="")
    elif t < 46.8:
        lab("DEPOSITADO")
        contador(c, t, 11.5, 0, 21600, 700, yc, 84, d=1.6, col=GOLD) if t >= 11.5 else numero_i(c, "R$ 100/mês", 700, yc + 30, 70, CREME)
    elif t < 60.6:
        lab("CUSTO/MÊS")
        numero_i(c, "R$ 1.400", 700, yc + 30, 84, VERMELHO) if t >= 55.8 else numero_i(c, "?", 700, yc + 30, 84, CREME)
    elif t < 67.8:
        lab("AOS 18")
        numero_i(c, "R$ 37 MIL", 710, yc + 28, 72, VERDE)
    else:
        lab("COM R$ 200")
        contador(c, t, 69.3, 37000, 74000, 700, yc, 84, d=0.9, col=GOLD) if t >= 69.3 else numero_i(c, "R$ 37 MIL", 710, yc + 28, 72, VERDE)


def detalhes(c, t):
    if 1.5 <= t < 8.1:
        entra(c, t, 1.5, *L1, chip("R$ 100/mês", VERDE, CREME, 46, -0.04), anim="left")
        entra(c, t, 2.0, *R1, chip("desde o nascimento", CREME, TINTA, 38, 0.04), anim="right")
        if t >= 6.3:
            entra(c, t, 6.3, *L2, chip("sem inflação", CREME, TINTA, 40, 0.03), anim="left")
    if 8.1 <= t < 15.3:
        entra(c, t, 9.1, *L1, chip("216 meses", CREME, TINTA, 46, -0.04), anim="left")
        entra(c, t, 11.5, *R1, chip("x R$ 100", GOLD, TINTA, 48, 0.04), anim="right")
        if t >= 13.6:
            entra(c, t, 13.6, *L2, chip("do seu bolso", CREME, TINTA, 40, 0.03), anim="left")
    if 15.3 <= t < 25.7:
        entra(c, t, 16.6, *L1, chip("inflação ~4,5%/ano", CREME, TINTA, 38, -0.04), anim="left")
        if t >= 21.0:
            entra(c, t, 21.0, *R1, chip("compra R$ 15 mil", VERMELHO, CREME, 40, 0.04), anim="stamp")
        if t >= 23.7:
            entra(c, t, 23.7, *R2, chip("PERDEU", VERMELHO, CREME, 50, -0.03), anim="stamp")
    if 28.3 <= t < 31.5:
        entra(c, t, 28.3, *C1, chip("~R$ 25 mil de hoje", CREME, TINTA, 46), anim="pop")
    if 31.5 <= t < 41.1:
        entra(c, t, 32.3, *L1, chip("título do Tesouro", CREME, NAVY, 40, -0.04), anim="left")
        if t >= 34.6:
            entra(c, t, 34.6, *R1, chip("IPCA + 7,5%", GOLD, TINTA, 46, 0.04), anim="stamp")
        if t >= 37.6:
            entra(c, t, 37.6, *L2, chip("já sem imposto", CREME, TINTA, 38, 0.03), anim="left")
        if t >= 39.5:
            entra(c, t, 39.5, *R2, chip("R$ 37 MIL", VERDE, CREME, 50, -0.03), anim="stamp")
    if 44.5 <= t < 46.8:
        entra(c, t, 44.8, *C1, chip("vale o que compra", GOLD, TINTA, 48), anim="stamp")
    if 46.8 <= t < 52.3:
        entra(c, t, 47.0, *C1, chip("A VIRADA", VERMELHO, CREME, 56), anim="stamp")
    if 57.6 <= t < 60.6:
        entra(c, t, 58.8, *C1, chip("só 7%", VERMELHO, CREME, 52), anim="stamp")
    if 60.6 <= t < 62.1:
        entra(c, t, 60.8, *C1, chip("mas olha o que vira", GOLD, TINTA, 46), anim="pop")
    if 67.8 <= t < 70.3:
        entra(c, t, 69.3, *C1, chip("R$ 200 = O DOBRO", VERDE, CREME, 50), anim="stamp")
    if 70.3 <= t < 75.8:
        entra(c, t, 70.5, *C1, chip("taxa não é garantida", CREME, TINTA, 44), anim="pop")
    if 75.8 <= t < 80.6:
        entra(c, t, 77.0, *C1, chip("começa cedo = mais juros", VERDE, CREME, 44), anim="stamp")
    if t >= 80.6:
        entra(c, t, 80.8, 540, 1040, chip("VOCÊ GUARDA PRO SEU FILHO?", GOLD, TINTA, 46), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "R$ 100 POR MÊS PRO FILHO", 540, 235, 56, CREME)
    if t < 46.8:
        tabela(c, t)
    elif t < 60.6:
        custo(c, t)
    else:
        usos(c, t)
    marcador(c, t)
    poses = ((0, "present"), (3.1, "shrug"), (5.1, "finger_up"), (8.1, "present"), (11.5, "point_r"), (15.3, "shrug"),
             (21.0, "head"), (25.7, "point_r"), (31.5, "finger_up"), (39.1, "arms_up"), (41.1, "present"), (44.8, "finger_up"),
             (46.8, "finger_up"), (52.3, "head"), (57.6, "shrug"), (60.6, "finger_up"), (63.8, "point_r"), (67.8, "arms_up"),
             (70.3, "present"), (75.8, "finger_up"), (80.6, "present"))
    exprs = ((0, "confident"), (3.1, "think"), (5.1, "confident"), (21.0, "shocked"), (25.7, "neutral"), (39.1, "grin"),
             (44.5, "confident"), (52.3, "shocked"), (60.6, "confident"), (62.1, "grin"), (70.3, "think"), (75.8, "confident"),
             (80.6, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
