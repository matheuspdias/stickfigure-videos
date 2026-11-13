"""Seu 13º já tem dono: o Natal. Só TikTok: vertical nativo 1080x1920, ~70,2 s, estilo ilustrado.
Primeiro vídeo com as regras de 14/11/2026 (AUTOMATICO_TIKTOK.md 2b): sem cartaz de abertura, a conta já
acontecendo no quadro 0, título pequeno no topo; tema útil do momento. Narração: Afonso (HeyGen), 1 bloco.
Contas em contas.py (Natal: CNDL/SPC 2025; 13º: tabelas 2026)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.2, "soft_ding"), (3.7, "tum"), (12.1, "soft_ding"), (23.3, "tum"), (40.3, "soft_ding"), (44.7, "tum"), (54.5, "tum"), (62.7, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

VOCE = "lucas"


def topo(c, s, cor=CREME, contorno=TINTA):
    """título pequeno no topo (regra 2b.1: nada de cartaz grande)"""
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


def presente(c, s=1.0, cor=VERMELHO, laco=GOLD):
    c.save(); c.scale(s, s)
    rr(c, -90 + 8, -70 + 10, 180, 150, 12); rgb(c, (0, 0, 0), 0.22); c.fill()
    rr(c, -90, -70, 180, 150, 12); rgb(c, cor); c.fill()
    rr(c, -100, -100, 200, 44, 10); rgb(c, mix(cor, (1, 1, 1), 0.15)); c.fill()
    c.rectangle(-14, -100, 28, 180); rgb(c, laco); c.fill()
    for sx in (-1, 1):
        c.save(); c.translate(sx * 26, -112); c.scale(1.6, 1.0)
        c.new_sub_path(); c.arc(0, 0, 18, 0, 6.283); c.restore(); rgb(c, laco); c.set_line_width(10); c.stroke()
    c.restore()


def linha_conta(c, t, t0, y, nome, valor, cor=VERMELHO):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.35))
    x = 540 - 600 * (1 - k)
    rr(c, x - 400, y - 55, 800, 110, 22); rgb(c, CREME); c.fill()
    text(c, nome, x - 370, y + 18, 54, MARKER, TINTA, align="l")
    text(c, valor, x + 370, y + 18, 58, MARKER, cor, align="r")


def pop(c, t, t0, x, y, s, size, col=GOLD, contorno=TINTA):
    if t < t0:
        return
    k = 1 + 0.14 * math.sin(clamp01((t - t0) / 0.3) * math.pi)
    c.save(); c.translate(x, y); c.scale(k, k); numero_i(c, s, 0, 0, size, col, contorno=contorno); c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 4.6  o 13º cai... e já tem dono
    luz("dia")
    fundo_marca(c, t, "verde" if t < 3.6 else "vermelho", holofote=(560, 900))
    topo(c, "SEU 13º JÁ TEM DONO")
    chuva_dinheiro(c, t, -1.2, n=22, seed=3) if t < 3.6 else None
    if t < 3.6:
        linhas = [("13º salário", "+ R$ 3.000", VERDE)]
        celular_app(c, t, 640, 790, 1.15, titulo="Pix recebido", valor="R$ %s" % format(int(3000 * ease_out(clamp01(t / 1.2))), ",").replace(",", "."),
                    linhas=linhas, cor=VERDE, t0=0.0, d=0.5)
    else:
        linhas = [("Presentes", "- R$ 696", VERMELHO), ("Ceia", "- R$ 338", VERMELHO), ("Roupa nova", "- R$ 324", VERMELHO)]
        celular_app(c, t, 640, 790, 1.15, titulo="13º salário", valor="R$ 3.000", linhas=linhas, cor=VERMELHO, t0=3.6, d=0.9)
    entra(c, t, 3.6, 640, 400, selo("É O NATAL", VERMELHO, 64, CREME), anim="stamp")
    pessoa(c, t, 210, 1300, 1.3, VOCE, poses=((0, "arms_up"), (3.6, "head")), exprs=((0, "grin"), (3.6, "shocked")), look=0.6)


def s02(c, t):  # 4.6 - 14.4  4 presentes de R$ 174
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "PRESENTES", NAVY, CREME)
    cores = (VERMELHO, VERDE, BLUE, PURPLE)
    for i in range(4):
        t0 = 8.2 + i * 0.22
        x, y = 300 + (i % 2) * 360, 560 + (i // 2) * 330
        entra(c, t, t0, x, y, lambda c, k=i: presente(c, 1.05, cores[k]), anim="drop")
        if t > 9.9:
            entra(c, t, 9.9 + i * 0.12, x + 70, y + 110, lambda c: etiqueta_preco(c, "R$ 174", GOLD, 40), anim="pop")
    if t > 12.1:
        rr(c, 140, 1150, 800, 130, 26); rgb(c, NAVY); c.fill()
        text(c, "4 x 174 =", 330, 1240, 60, MARKER, CREME)
        pop(c, t, 12.3, 700, 1225, "R$ 696", 90, GOLD)
    if t < 8.2:
        consultor_i(c, t, 540, 1300, 1.3, poses=((0, "present"),), exprs=((0, "neutral"),), look=0.0)
        numero_i(c, "NO ANO PASSADO, EM MÉDIA", 540, 500, 50, NAVY, contorno=CREME)


def s03(c, t):  # 14.4 - 23.2  ceia, roupa, amigo secreto
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "O NATAL INTEIRO", NAVY, CREME)
    linha_conta(c, t, 14.4, 420, "Presentes", "R$ 696")
    linha_conta(c, t, 14.7, 560, "Ceia", "R$ 338")
    linha_conta(c, t, 17.1, 700, "Roupa nova", "R$ 324")
    linha_conta(c, t, 20.4, 840, "Amigo secreto", "R$ 72")
    consultor_i(c, t, 540, 1400, 0.95, poses=((0, "point_ru"),), exprs=((0, "neutral"), (20.4, "shocked")), look=0.5)


def s04(c, t):  # 23.2 - 26.0  total
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(540, 1000))
    topo(c, "TOTAL DO NATAL")
    contador(c, t, 23.4, 0, 1430, 540, 620, 170, d=1.3, col=GOLD)
    entra(c, t, 24.9, 380, 820, selo("NA MÉDIA", NAVY, 50, CREME), anim="stamp")
    pessoa(c, t, 790, 1340, 1.2, VOCE, poses=((0, "head"),), exprs=((0, "desperate"),), look=-0.6)


def cartao_parcela(c, t, t0, x, nome, data, valor, desc=None, t_desc=None, cor=VERDE):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.4))
    c.save(); c.translate(x, 700 + 300 * (1 - k))
    rr(c, -190 + 8, -260 + 10, 380, 520, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, -190, -260, 380, 520, 30); rgb(c, CREME); c.fill()
    rr(c, -190, -260, 380, 120, 30); rgb(c, cor); c.fill(); c.rectangle(-190, -170, 380, 30); c.fill()
    text(c, nome, 0, -185, 52, MARKER, CREME)
    text(c, data, 0, -60, 44, MARKER, NAVY)
    if desc and t >= t_desc:
        text(c, desc, 0, 40, 44, MARKER, VERMELHO)
    text(c, valor, 0, 170, 76, MARKER, TINTA)
    c.restore()


def s05(c, t):  # 26.0 - 42.9  as duas parcelas
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1200))
    topo(c, "SEU 13º · SALÁRIO DE R$ 3 MIL")
    cartao_parcela(c, t, 28.2, 270, "1ª PARCELA", "até 30/11", "R$ 1.500", "sem desconto", 32.3, VERDE)
    v2 = "R$ 1.251" if t >= 40.3 else "R$ 1.500"
    cartao_parcela(c, t, 33.8, 720, "2ª PARCELA", "até 18/12", v2, "- INSS R$ 248", 37.5, VERMELHO)
    consultor_i(c, t, 500, 1420, 0.85, poses=((0, "present"), (37.5, "point_r")), exprs=((0, "neutral"), (37.5, "confident")), look=0.4)


def s06(c, t):  # 42.9 - 47.6  o Natal come a 1ª parcela
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(540, 1000))
    topo(c, "O NATAL COME A 1ª PARCELA")
    rosca_i(c, t, 44.6, 540, 700, 230, 0.95, VERMELHO, texto="95%", d=1.6)
    numero_i(c, "R$ 1.430 DE R$ 1.500", 560, 1040, 58, CREME)
    pessoa(c, t, 170, 1400, 0.9, VOCE, poses=((0, "shrug"),), exprs=((0, "desperate"),), look=0.6)


def s07(c, t):  # 47.6 - 55.3  e aí chega janeiro
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "E AÍ CHEGA JANEIRO", NAVY, CREME)
    # calendário de janeiro
    rr(c, 330, 330, 420, 360, 26); rgb(c, CREME); c.fill(); rr(c, 330, 330, 420, 110, 26); rgb(c, VERMELHO); c.fill()
    c.rectangle(330, 400, 420, 40); c.fill()
    numero_i(c, "JANEIRO", 540, 400, 56, CREME, contorno=VERMELHO)
    numero_i(c, "2027", 540, 590, 110, NAVY, contorno=CREME)
    for i, (t0, s, x, y) in enumerate(((48.8, "IPVA", 400, 790), (49.7, "IPTU", 770, 790), (50.7, "MATERIAL ESCOLAR", 570, 930), (52.1, "FATURA", 740, 1070))):
        entra(c, t, t0, x, y, selo(s, VERMELHO, 48, CREME, rot=(-0.07 if i % 2 else 0.06)), anim="stamp")
    if t > 54.4:
        entra(c, t, 54.4, 540, 1210, selo("13º: R$ 0", NAVY, 64, GOLD), anim="stamp")
    pessoa(c, t, 160, 1380, 0.95, VOCE, poses=((0, "think"), (54.4, "head")), exprs=((0, "think"), (54.4, "desperate")), look=0.6)


def s08(c, t):  # 55.3 - 65.9  a saída
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(250, 1100))
    topo(c, "A SAÍDA")
    if t > 56.6:
        rr(c, 370, 370, 550, 320, 26); rgb(c, CREME); c.fill()
        text(c, "1ª PARCELA", 645, 450, 52, MARKER, VERDE)
        text(c, "= TETO DO NATAL", 645, 530, 50, MARKER, TINTA)
        if t > 61.4:
            text(c, "E NÃO PASSA DISSO", 645, 630, 42, MARKER, VERMELHO)
    if t > 62.7:
        rr(c, 370, 740, 550, 280, 26); rgb(c, CREME); c.fill()
        text(c, "2ª PARCELA", 645, 820, 52, MARKER, NAVY)
        text(c, "= GUARDA", 645, 900, 50, MARKER, TINTA)
        text(c, "PRA JANEIRO", 645, 975, 50, MARKER, TINTA) if t > 64.8 else None
    consultor_i(c, t, 200, 1340, 1.15, poses=((0, "finger_up"), (56.6, "point_r")), exprs=((0, "confident"),), look=0.6)


def s09(c, t):  # 65.9 - fim  pergunta
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "E O SEU 13º?")
    entra(c, t, 67.5, 320, 560, selo("NATAL", VERMELHO, 80, CREME, rot=-0.05), anim="stamp")
    numero_i(c, "OU", 540, 700, 70, GOLD) if t > 68.1 else None
    entra(c, t, 68.4, 720, 840, selo("JANEIRO", VERDE, 80, CREME, rot=0.05), anim="stamp")
    entra(c, t, 69.2, 620, 1060, selo("COMENTA AÍ", GOLD, 56, TINTA, rot=0), anim="pop")
    pessoa(c, t, 170, 1380, 1.0, VOCE, poses=((0, "think"),), exprs=((0, "think"),), look=0.0)


SCENES = [(0, 4.6, s01), (4.6, 14.4, s02), (14.4, 23.2, s03), (23.2, 26.0, s04), (26.0, 42.9, s05),
          (42.9, 47.6, s06), (47.6, 55.3, s07), (55.3, 65.9, s08), (65.9, 999.0, s09)]
