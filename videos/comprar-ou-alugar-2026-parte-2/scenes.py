"""Comprar ou alugar em 2026? (Parte 2 de 3): a conta de 10 anos. Só TikTok: vertical 1080x1920, ~88,3 s, estilo ilustrado.
Conta útil das 18h, série numerada (continua comprar-ou-alugar-2026-parte-1); sem cartaz de abertura: no quadro 0 o contador de juros já está subindo.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (apê R$ 300 mil, entrada 20% + ITBI/cartório 4%, SAC 30 anos 12% a.a.;
aluguel R$ 1.500 +4,5%/ano; CDI 2026 13,65% com IR 15% = ~11,6% a.a.; valorização 5% a.a.)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(23.7, "tum"), (48.1, "tum"), (64.3, "soft_ding"), (73.4, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

VOCE = "lucas"


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


def visor(c, s, x, y, w=560, h=130, rot=None, cor=(1.0, 0.25, 0.22)):
    rr(c, x - w / 2 + 8, y - h / 2 + 10, w, h, 18); rgb(c, (0, 0, 0), 0.3); c.fill()
    rr(c, x - w / 2, y - h / 2, w, h, 18); rgb(c, (0.08, 0.08, 0.10)); c.fill()
    if rot:
        text(c, rot, x, y - h / 2 - 22, 30, MARKER, CREME)
    c.select_font_face(MARKER); c.set_font_size(h * 0.62)
    e = c.text_extents(s)
    c.move_to(x + w / 2 - 30 - e.x_advance, y + h * 0.22); rgb(c, cor); c.show_text(s)


def linha_conta(c, t, t0, y, nome, valor, t_val, cor=VERMELHO, vsize=62):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.35))
    x = 540 - 600 * (1 - k)
    rr(c, x - 420, y - 62, 840, 124, 22); rgb(c, CREME); c.fill()
    text(c, nome, x - 390, y + 18, 50, MARKER, TINTA, align="l")
    if t >= t_val:
        kk = 1 + 0.14 * math.sin(clamp01((t - t_val) / 0.3) * math.pi)
        c.save(); c.translate(x + 390, y + 18); c.scale(kk, kk)
        text(c, valor, 0, 0, vsize, MARKER, cor, align="r"); c.restore()




def cartao(c, t, t0, x, y, w, h, rot, val, cor=VERMELHO, vsize=64):
    if t < t0:
        return
    k = max(0.02, ease_out(clamp01((t - t0) / 0.35)))
    c.save(); c.translate(x, y); c.scale(k, k)
    rr(c, -w / 2 + 8, -h / 2 + 10, w, h, 24); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, -w / 2, -h / 2, w, h, 24); rgb(c, CREME); c.fill()
    text(c, rot, 0, -h / 2 + 52, 38, MARKER, NAVY)
    numero_i(c, val, 0, h / 2 - 50, vsize, cor, contorno=TINTA)
    c.restore()


def predio_apto(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    predio_moderno(c, 0, 0, 300, 640)
    c.restore()



def cruzamento(c, t, t0, x=110, y=1080, w=820, h=560):
    """aluguel subindo (verde) x parcela SAC caindo (vermelho) em 10 anos"""
    rr(c, x - 40, y - h - 70, w + 80, h + 150, 24); rgb(c, (1, 1, 1), 0.9); c.fill()
    vmin, vmax = 1100, 3100
    Y = lambda v: y - h * (v - vmin) / (vmax - vmin)
    c.rectangle(x, y, w, 4); rgb(c, (0.4, 0.4, 0.45)); c.fill()
    c.select_font_face(HAND); c.set_font_size(32); rgb(c, (0.4, 0.4, 0.45))
    c.move_to(x, y + 44); c.show_text("ano 1")
    ww = c.text_extents("ano 10").x_advance; c.move_to(x + w - ww, y + 44); c.show_text("ano 10")
    p = ease_io(prog(t, t0, 4.2)) if t >= t0 else 0
    if p <= 0:
        return
    alug = [1500 * 1.045 ** a for a in range(10)]
    fin = 240000; i = 1.12 ** (1 / 12) - 1; am = fin / 360
    parc = [am + (fin - am * 12 * a) * i for a in range(10)]
    for serie, cor, nome in ((parc, VERMELHO, "PARCELA"), (alug, VERDE, "ALUGUEL")):
        n = 120
        m = max(2, int(n * p))
        pts = []
        for j in range(m + 1):
            k = j / n * 9
            a0 = min(8, int(k)); f = k - a0
            v = serie[a0] * (1 - f) + serie[a0 + 1] * f
            pts.append((x + w * j / n, Y(v)))
        c.move_to(*pts[0])
        for px, py in pts[1:]:
            c.line_to(px, py)
        rgb(c, cor); c.set_line_width(10); c.stroke()
        c.new_sub_path(); c.arc(*pts[-1], 14, 0, 6.283); rgb(c, cor); c.fill()
        if t > t0 + 0.6:
            ly = Y(serie[0]) + (-30 if nome == "PARCELA" else 70)
            text(c, nome, x + 20, ly, 40, MARKER, cor, align="l")


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.9  10 anos: 228 mil só de juros; quase o mesmo que o aluguel
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(200, 1150))
    topo(c, "FINANCIOU R$ 300 MIL")
    contador(c, t, 0.0, 120000, 228000, 560, 500, 140, d=6.2, col=GOLD)
    if t > 6.7:
        entra(c, t, 6.7, 560, 680, selo("SÓ DE JUROS", NAVY, 60, CREME), anim="stamp")
    if t > 8.0:
        entra(c, t, 8.0, 610, 880, selo("ALUGUEL 10 ANOS: R$ 221 MIL", VERDE, 36, CREME, rot=0.04), anim="stamp")
    consultor_i(c, t, 150, 1300, 1.0, poses=((0, "point_r"), (6.7, "head")), exprs=((0, "confident"), (6.7, "shocked")), look=0.6)


def s02(c, t):  # 9.9 - 14.0  comprar ou alugar em 2026, parte 2
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "COMPRAR OU ALUGAR EM 2026?")
    predio_apto(c, 700, 1240, 0.9)
    entra(c, t, 10.0, 470, 470, lambda c: etiqueta_preco(c, "R$ 300 MIL", GOLD, 64), anim="drop")
    if t > 12.8:
        entra(c, t, 12.8, 560, 660, selo("PARTE 2: 10 ANOS", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 250, 1300, 1.2, poses=((0, "present"), (12.8, "finger_up")), exprs=((0, "confident"),), look=0.5)


def s03(c, t):  # 14.0 - 25.4  Ana aluga; Bruno: entrada 60 mil + ITBI e cartório 12 mil
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "MESMO APÊ DA PARTE 1", NAVY, CREME)
    cartao(c, t, 16.0, 270, 500, 400, 200, "ANA ALUGA", "R$ 1.500", VERDE, 64)
    cartao(c, t, 19.7, 720, 420, 400, 180, "BRUNO: ENTRADA", "R$ 60 MIL", NAVY, 58)
    cartao(c, t, 21.5, 720, 630, 400, 180, "ITBI + CARTÓRIO", "R$ 12 MIL", VERMELHO, 58)
    if t > 23.7:
        entra(c, t, 23.7, 640, 740, selo("NINGUÉM PÕE NA CONTA", GOLD, 36, TINTA, rot=0.05), anim="stamp")
    pessoa(c, t, 250, 1300, 1.0, "ana", poses=((0, "stand"), (16.0, "present")), exprs=((0, "neutral"), (16.0, "grin")), look=0.4)
    pessoa(c, t, 780, 1300, 1.0, "bruno", poses=((0, "stand"), (19.0, "point_r"), (23.7, "head")),
           exprs=((0, "neutral"), (23.7, "shocked")), look=-0.4)


def s04(c, t):  # 25.4 - 28.6  primeira parcela: 2.950
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(260, 1150))
    topo(c, "1ª PARCELA DO BRUNO")
    contador(c, t, 25.5, 0, 2944, 560, 520, 150, d=2.2, col=GOLD)
    if t > 27.4:
        entra(c, t, 27.4, 580, 690, selo("UNS R$ 2.950 POR MÊS", NAVY, 50, GOLD), anim="stamp")
    pessoa(c, t, 260, 1300, 1.25, "bruno", poses=((0, "stand"), (26.5, "head")), exprs=((0, "think"), (26.5, "shocked")), look=0.6)


def s05(c, t):  # 28.6 - 42.9  Ana investe 72 mil + a diferença todo mês; CDI 2026 ~11,6% líquido
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(270, 1150))
    topo(c, "A ANA INVESTE")
    linha_conta(c, t, 29.0, 400, "Entrada + ITBI", "R$ 72 MIL", 30.4, VERDE)
    linha_conta(c, t, 32.0, 550, "Todo mês", "parcela - aluguel", 33.8, NAVY, vsize=44)
    if t > 33.8:
        entra(c, t, 33.8, 600, 690, selo("R$ 2.950 - R$ 1.500 = R$ 1.450", NAVY, 38, CREME, rot=0.03), anim="stamp")
    if t > 37.5:
        entra(c, t, 37.5, 640, 850, selo("CDI 2026: ~11,6% AO ANO", GOLD, 46, TINTA), anim="stamp")
    if t > 41.4:
        entra(c, t, 41.4, 680, 990, selo("JÁ SEM IMPOSTO", CREME, 40, TINTA, rot=0.05), anim="stamp")
    pessoa(c, t, 190, 1300, 1.15, "ana", poses=((0, "present"), (37.5, "arms_up")), exprs=((0, "confident"), (37.5, "grin")), look=0.6)


def s06(c, t):  # 42.9 - 50.7  aluguel sobe, parcela cai; no 10º ano se cruzam (~2.200)
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "ANO APÓS ANO", NAVY, CREME)
    cruzamento(c, t, 43.2)
    if t > 48.1:
        entra(c, t, 48.1, 620, 1200, selo("ANO 10: ~R$ 2.200 CADA", NAVY, 46, GOLD), anim="stamp")


def s07(c, t):  # 50.7 - 61.2  Bruno 10 anos depois: 489 - 160 = 329 mil
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "BRUNO, 10 ANOS DEPOIS")
    linha_conta(c, t, 52.2, 380, "O apê vale", "R$ 489 MIL", 53.6, VERDE)
    linha_conta(c, t, 55.7, 520, "Ainda deve", "- R$ 160 MIL", 56.5, VERMELHO)
    linha_conta(c, t, 58.8, 660, "Sobram", "R$ 329 MIL", 59.2, NAVY)
    pessoa(c, t, 540, 1300, 1.05, "bruno", poses=((0, "stand"), (52.2, "present"), (55.7, "shrug"), (58.8, "present")),
           exprs=((0, "neutral"), (52.2, "grin"), (55.7, "shocked"), (58.8, "confident")), look=0.0)


def s08(c, t):  # 61.2 - 66.6  Ana: 404 mil, 75 mil a mais
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(540, 1150))
    topo(c, "E A ANA?")
    barras_i(c, t, 61.6, 230, 1150, w=620, h=600, dados=(("BRUNO", 328668, BLUE), ("ANA", 403529, VERDE)),
             fmt=lambda v: brl(v), maxv=420000, intervalo=0.5, size_val=56)
    if t > 64.3:
        entra(c, t, 64.3, 540, 380, selo("+ R$ 75 MIL", GOLD, 70, TINTA), anim="stamp")


def s09(c, t):  # 66.6 - 74.4  se gastar a diferença: 216 mil. Perde feio
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(540, 1150))
    topo(c, "MAS OLHA O DETALHE")
    if t > 67.9:
        entra(c, t, 67.9, 540, 370, selo("ANA GASTOU A DIFERENÇA", NAVY, 46, CREME), anim="stamp")
    barras_i(c, t, 70.4, 230, 1150, w=620, h=600, dados=(("BRUNO", 328668, BLUE), ("ANA", 215810, VERMELHO)),
             fmt=lambda v: brl(v), maxv=420000, intervalo=0.5, size_val=56)
    if t > 73.4:
        entra(c, t, 73.4, 540, 520, selo("PERDE FEIO", GOLD, 60, TINTA, rot=0.06), anim="stamp")


def s10(c, t):  # 74.4 - 83.8  conclusão + parte 3
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "COM OS JUROS DE 2026")
    if t > 76.4:
        entra(c, t, 76.4, 540, 390, selo("ALUGAR + INVESTIR GANHA", VERDE, 50, CREME), anim="stamp")
    if t > 78.3:
        entra(c, t, 78.3, 540, 530, selo("SÓ SE INVESTIR TODO MÊS", GOLD, 48, TINTA, rot=0.04), anim="stamp")
    if t > 81.0:
        entra(c, t, 81.0, 540, 670, selo("PARTE 3: QUANDO COMPRAR GANHA", VERMELHO, 40, CREME), anim="stamp")
    consultor_i(c, t, 540, 1300, 1.05, poses=((0, "present"), (78.3, "finger_up"), (81.0, "point_r")),
                exprs=((0, "confident"), (81.0, "grin")), look=0.0)


def s11(c, t):  # 83.8 - fim  pergunta
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "E VOCÊ?")
    entra(c, t, 84.0, 540, 390, selo("CONSEGUIRIA INVESTIR", CREME, 52, TINTA), anim="stamp")
    if t > 85.5:
        entra(c, t, 85.5, 540, 530, selo("A DIFERENÇA TODO MÊS?", GOLD, 52, TINTA, rot=0.04), anim="stamp")
    if t > 87.5:
        entra(c, t, 87.5, 540, 670, selo("COMENTA", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 540, 1300, 1.05, poses=((0, "present"), (85.5, "point_r")), exprs=((0, "grin"),), look=0.0)


SCENES = [(0, 9.9, s01), (9.9, 14.0, s02), (14.0, 25.4, s03), (25.4, 28.6, s04), (28.6, 42.9, s05), (42.9, 50.7, s06),
          (50.7, 61.2, s07), (61.2, 66.6, s08), (66.6, 74.4, s09), (74.4, 83.8, s10), (83.8, 999.0, s11)]
