"""Celular de R$ 8 mil: quanto custa por dia? Só TikTok: vertical nativo 1080x1920, ~80,9 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: top de 8 mil trocado todo ano (revende 5 mil) R$ 8,22/dia; intermediário de 2 mil por 3 anos
(revende 400) R$ 1,46/dia; top por 4 anos (revende 2 mil) R$ 4,11/dia; básico de 1.200 trocado todo ano (revende 300) R$ 2,47/dia."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(3.2, "tum"), (22.7, "soft_ding"), (39.7, "tum"), (60.1, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

TOP_COR = (0.20, 0.20, 0.24)
MEIO_COR = (0.25, 0.52, 0.78)
BASICO_COR = (0.62, 0.62, 0.60)


def selo(s, cor=VERMELHO, size=64, tcol=CREME, rot=-0.06):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(rot)
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


def fone(cor=TOP_COR, s=1.0, rachado=False, rot=0.0):
    """celular genérico (sem marca), origem = centro"""
    def f(c):
        c.save(); c.rotate(rot); c.scale(s, s)
        rr(c, -110 + 10, -210 + 14, 220, 420, 36); rgb(c, (0, 0, 0), 0.25); c.fill()
        rr(c, -110, -210, 220, 420, 36); rgb(c, cor); c.fill()
        rr(c, -96, -190, 192, 380, 26)
        lgrad(c, 0, -190, 0, 190, ((0, (0.40, 0.62, 0.92), 1), (1, (0.62, 0.40, 0.82), 1))); c.fill()
        rr(c, -34, -184, 68, 18, 9); rgb(c, (0.05, 0.05, 0.07)); c.fill()
        for i in range(3):
            for j in range(4):
                rr(c, -72 + i * 52, -130 + j * 62, 40, 40, 10); rgb(c, CREME, 0.55); c.fill()
        if rachado:
            c.set_line_width(4); rgb(c, CREME, 0.95)
            c.move_to(-60, -150); c.line_to(-10, -60); c.line_to(-40, 20); c.line_to(30, 110)
            c.move_to(-10, -60); c.line_to(60, -90); c.stroke()
        c.restore()
    return f


def etiqueta(s, cor=GOLD, size=52):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 60
        c.save(); c.rotate(0.05)
        rr(c, -w / 2 + 6, -size * 0.75 + 8, w, size * 1.5, 14); rgb(c, (0, 0, 0), 0.2); c.fill()
        rr(c, -w / 2, -size * 0.75, w, size * 1.5, 14); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, TINTA, contorno=CREME)
        c.restore()
    return f


def por_dia(c, t, t0, valor, x, y, col=GOLD, size=130, casas=2):
    """contador R$ x,xx + 'POR DIA'"""
    if t < t0:
        return
    contador(c, t, t0, 0, valor, x, y, size, d=0.8, col=col, casas=casas)
    if t > t0 + 0.5:
        numero_i(c, "POR DIA", x, y + size * 0.85, 54, CREME)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.3  gancho
    fundo_marca(c, t, "vermelho", holofote=(270, 1100))
    numero_i(c, "QUANTO CUSTA", 520, 230, 100, CREME)
    numero_i(c, "POR DIA", 520, 345, 110, GOLD)
    numero_i(c, "UM CELULAR DE R$ 8 MIL?", 520, 460, 62, CREME)
    entra(c, t, 0.2, 770, 930, fone(TOP_COR, 1.0, rot=0.08), anim="pop")
    entra(c, t, 2.9, 770, 1210, etiqueta("R$ 8.000", GOLD, 58), anim="stamp")
    entra(c, t, 4.6, 520, 600, selo("A RESPOSTA VAI INCOMODAR", NAVY, 44, GOLD), anim="stamp")
    consultor_i(c, t, 250, 1300, 1.35, poses=((0, "point_r"), (4.6, "head")), exprs=((0, "think"), (4.6, "shocked")), look=0.7)


def s02(c, t):  # 6.3 - 13.1  8 mil em 12x = 667 por mês durante um ano
    cena_sala(c, t, "tarde")
    numero_i(c, "R$ 8 MIL EM 12X", 520, 240, 100, CREME)
    entra(c, t, 9.1, 640, 470, cartao("Parcela", "R$ 667", VERMELHO, 600), anim="right")
    entra(c, t, 11.9, 640, 600, cartao("Durante", "1 ANO", TINTA, 600), anim="right")
    entra(c, t, 6.6, 780, 980, fone(TOP_COR, 0.95, rot=0.06), anim="up")
    pessoa(c, t, 260, 1300, 1.35, "bruno", poses=((0, "arms_up"), (9.1, "hold")), exprs=((0, "grin"), (9.1, "happy")), look=0.6,
           prop=("r", prop_celular_i) if t > 9.1 else None)


def s03(c, t):  # 13.1 - 16.8  a conta certa: quanto custa por dia de uso
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    numero_i(c, "A CONTA CERTA", 520, 240, 100, GOLD)
    numero_i(c, "É OUTRA", 520, 350, 90, CREME) if t > 14.1 else None
    if t > 14.8:
        rr(c, 300, 470, 640, 330, 26); rgb(c, CREME); c.fill()
        text(c, "preço − revenda", 620, 560, 58, HAND, TINTA)
        line(c, 360, 630, 880, 630, 6, TINTA)
        text(c, "dias de uso", 620, 710, 58, HAND, TINTA)
    entra(c, t, 15.6, 660, 900, selo("= CUSTO POR DIA", VERDE, 60, CREME), anim="stamp")
    consultor_i(c, t, 170, 1300, 1.3, poses=((0, "finger_up"), (14.8, "present")), exprs=((0, "think"), (14.8, "confident")), look=0.6)


def s04(c, t):  # 16.8 - 25.0  troca todo ano: vende 5 mil, perdeu 3 mil, + de R$ 8 por dia
    fundo_marca(c, t, "vermelho", holofote=(220, 1100))
    numero_i(c, "TROCA TODO ANO", 520, 230, 100, CREME)
    entra(c, t, 18.4, 600, 420, cartao("Comprou", "R$ 8.000", TINTA, 640), anim="right")
    entra(c, t, 19.3, 600, 540, cartao("Vendeu usado", "R$ 5.000", VERDE, 640), anim="right")
    if t > 20.5:
        entra(c, t, 20.5, 600, 670, cartao("Perdeu em 1 ano", "R$ 3.000", VERMELHO, 640), anim="stamp")
    if t > 22.7:
        numero_i(c, "MAIS DE", 640, 800, 60, CREME)
        por_dia(c, t, 22.7, 8.22, 640, 910, GOLD, 120)
    entra(c, t, 17.0, 830, 1150, fone(TOP_COR, 0.6, rot=0.1), anim="up")
    pessoa(c, t, 220, 1300, 1.3, "bruno", poses=((0, "hold"), (20.5, "head")), exprs=((0, "happy"), (20.5, "shocked")), look=0.6,
           prop=("r", prop_celular_i) if t < 20.5 else None)


def s05(c, t):  # 25.0 - 35.9  celular de 2 mil por 3 anos: vende 400, menos de R$ 1,50 por dia
    cena_rua(c, t, "dia", carros=False)
    numero_i(c, "CELULAR DE R$ 2 MIL", 520, 230, 84, CREME)
    numero_i(c, "POR 3 ANOS", 520, 340, 90, GOLD) if t > 27.6 else None
    entra(c, t, 29.4, 600, 480, cartao("Vende no fim", "R$ 400", VERDE, 640), anim="right")
    entra(c, t, 31.7, 600, 600, cartao("Perdeu em 3 anos", "R$ 1.600", VERMELHO, 640), anim="right")
    if t > 34.0:
        numero_i(c, "MENOS DE", 640, 740, 60, CREME)
        k = 1 + 0.12 * math.sin(clamp01((t - 34.3) / 0.3) * math.pi)
        c.save(); c.translate(640, 860); c.scale(k, k); numero_i(c, "R$ 1,50", 0, 0, 120, VERDE, contorno=CREME); c.restore()
        numero_i(c, "POR DIA", 640, 960, 54, CREME)
    entra(c, t, 25.8, 870, 1170, fone(MEIO_COR, 0.55, rot=0.08), anim="up")
    pessoa(c, t, 220, 1300, 1.3, "ana", poses=((0, "wave"), (29.4, "hold"), (34.0, "thumb")), exprs=((0, "happy"), (34.0, "grin")),
           look=0.6, prop=("r", prop_celular_i) if 29.4 <= t < 34.0 else None)


def s06(c, t):  # 35.9 - 40.6  8 contra 1,50: parece que o caro é burrice... mas olha a virada
    fundo_marca(c, t, "creme")
    numero_i(c, "POR DIA", 520, 220, 100, NAVY, contorno=CREME)
    barras_i(c, t, 36.0, 170, 880, 740, 520, dados=(("Troca todo ano", 8.22, TOP_COR), ("R$ 2 mil, 3 anos", 1.46, MEIO_COR)),
             fmt=lambda v: brl(v, 2), d=1.0, size_val=56)
    if t > 38.1:
        entra(c, t, 38.1, 560, 1030, selo("O CARO É BURRICE?", VERMELHO, 56, CREME), anim="stamp")
    if t > 39.7:
        entra(c, t, 39.7, 560, 1160, selo("OLHA A VIRADA", NAVY, 56, GOLD), anim="stamp")
    consultor_i(c, t, 920, 1330, 0.75, poses=((0, "shrug"), (39.7, "finger_up")), exprs=((0, "think"), (39.7, "confident")), look=-0.6)


def s07(c, t):  # 40.6 - 49.4  o mesmo top por 4 anos: vende 2 mil, perdeu 6 mil, uns R$ 4 por dia
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    numero_i(c, "O MESMO DE R$ 8 MIL", 520, 230, 78, CREME)
    numero_i(c, "POR 4 ANOS", 520, 340, 96, GOLD) if t > 42.4 else None
    entra(c, t, 43.9, 600, 480, cartao("Ainda vende por", "R$ 2.000", VERDE, 640), anim="right")
    entra(c, t, 45.4, 600, 600, cartao("Perdeu em 4 anos", "R$ 6.000", VERMELHO, 640), anim="right")
    if t > 47.7:
        numero_i(c, "UNS", 640, 730, 60, CREME)
        k = 1 + 0.12 * math.sin(clamp01((t - 48.0) / 0.3) * math.pi)
        c.save(); c.translate(640, 830); c.scale(k, k); numero_i(c, "R$ 4", 0, 0, 130, GOLD); c.restore()
        numero_i(c, "POR DIA", 640, 930, 54, CREME)
    entra(c, t, 41.2, 860, 1150, fone(TOP_COR, 0.6, rot=0.08), anim="up")
    pessoa(c, t, 220, 1300, 1.3, "bruno", poses=((0, "hold"), (47.7, "thumb")), exprs=((0, "neutral"), (47.7, "grin")), look=0.6,
           prop=("r", prop_celular_i) if t < 47.7 else None)


def s08(c, t):  # 49.4 - 57.4  o de 1.200 que trava e você troca todo ano: quase R$ 2,50 por dia
    cena_sala(c, t, "tarde")
    numero_i(c, "O DE R$ 1.200", 520, 230, 96, CREME)
    numero_i(c, "QUE TRAVA", 520, 340, 90, VERMELHO, contorno=CREME) if t > 51.4 else None
    entra(c, t, 52.6, 600, 480, cartao("Troca todo ano", "", TINTA, 640), anim="right")
    entra(c, t, 53.8, 600, 600, cartao("Vende por", "R$ 300", VERDE, 640), anim="right")
    if t > 55.4:
        numero_i(c, "QUASE", 640, 730, 60, CREME)
        k = 1 + 0.12 * math.sin(clamp01((t - 55.8) / 0.3) * math.pi)
        c.save(); c.translate(640, 830); c.scale(k, k); numero_i(c, "R$ 2,50", 0, 0, 120, GOLD); c.restore()
        numero_i(c, "POR DIA", 640, 930, 54, CREME)
    tr = 0.03 * math.sin(t * 30) if 51.4 < t < 52.6 else 0.0
    entra(c, t, 49.8, 860, 1150, fone(BASICO_COR, 0.55, rachado=True, rot=0.08 + tr), anim="up")
    pessoa(c, t, 220, 1300, 1.3, "ana", poses=((0, "hold"), (51.4, "head")), exprs=((0, "worried"), (51.4, "desperate")), look=0.6,
           prop=("r", prop_celular_i) if t < 51.4 else None)


def s09(c, t):  # 57.4 - 67.4  o problema não é o preço: é a frequência da troca
    fundo_marca(c, t, "navy", holofote=(220, 1100))
    numero_i(c, "O PROBLEMA", 520, 230, 100, CREME)
    numero_i(c, "NÃO É O PREÇO", 520, 340, 84, CREME) if t > 58.2 else None
    if t > 60.1:
        k = 1 + 0.12 * math.sin(clamp01((t - 60.1) / 0.3) * math.pi)
        c.save(); c.translate(560, 500); c.scale(k, k); selo("É A FREQUÊNCIA DA TROCA", VERMELHO, 52, CREME)(c); c.restore()
    if t > 62.0:
        entra(c, t, 62.0, 640, 660, cartao("12x para trocar", "", TINTA, 580), anim="right")
        entra(c, t, 63.7, 640, 780, cartao("de novo em 12 meses", "", TINTA, 580), anim="right")
    entra(c, t, 65.3, 640, 920, selo("A VIDA PAGANDO CELULAR", GOLD, 40, NAVY), anim="stamp")
    consultor_i(c, t, 160, 1300, 1.0, poses=((0, "finger_up"), (60.1, "point_r"), (65.3, "shrug")),
                exprs=((0, "think"), (60.1, "confident"), (65.3, "worried")), look=0.6)


def s10(c, t):  # 67.4 - 75.2  cabe no bolso + 4 anos: pode valer; trocar todo ano: o mais caro de todos
    fundo_marca(c, t, "creme")
    numero_i(c, "ENTÃO", 520, 220, 100, NAVY, contorno=CREME)
    entra(c, t, 67.6, 640, 380, cartao("Cabe no bolso", "", TINTA, 580, 96), anim="right")
    entra(c, t, 68.9, 640, 490, cartao("e usa por 4 anos", "", TINTA, 580, 96), anim="right")
    entra(c, t, 70.5, 640, 610, selo("O CARO PODE VALER", VERDE, 52, CREME), anim="stamp")
    entra(c, t, 72.1, 640, 760, cartao("Troca todo ano", "", TINTA, 580, 96), anim="right")
    entra(c, t, 73.8, 640, 880, selo("O MAIS CARO DE TODOS", VERMELHO, 46, CREME), anim="stamp")
    consultor_i(c, t, 150, 1300, 0.95, poses=((0, "present"), (70.5, "thumb"), (73.8, "shrug")),
                exprs=((0, "neutral"), (70.5, "grin"), (73.8, "worried")), look=0.6)


def s11(c, t):  # 75.2 - fim  time iPhone por 4 anos ou time celular de 2 mil?
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "E VOCÊ?", 520, 230, 120, GOLD)
    entra(c, t, 76.4, 520, 410, selo("TIME R$ 8 MIL POR 4 ANOS", GOLD, 44, NAVY), anim="stamp")
    entra(c, t, 78.5, 520, 550, selo("TIME R$ 2 MIL", MEIO_COR, 54, CREME), anim="stamp")
    entra(c, t, 80.0, 520, 720, selo("COMENTA", VERMELHO, 66, CREME), anim="stamp")
    pessoa(c, t, 230, 1300, 1.2, "bruno", poses=((0, "stand"), (76.4, "thumb")), exprs=((0, "happy"), (76.4, "grin")), look=0.4)
    pessoa(c, t, 830, 1300, 1.2, "ana", poses=((0, "stand"), (78.5, "thumb")), exprs=((0, "happy"), (78.5, "grin")), look=-0.4)
    consultor_i(c, t, 530, 1330, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.0)


SCENES = [(0, 6.3, s01), (6.3, 13.1, s02), (13.1, 16.8, s03), (16.8, 25.0, s04), (25.0, 35.9, s05),
          (35.9, 40.6, s06), (40.6, 49.4, s07), (49.4, 57.4, s08), (57.4, 67.4, s09), (67.4, 75.2, s10),
          (75.2, 999.0, s11)]
