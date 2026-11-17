"""O que muda pra comprar imóvel em 2027 (juros subiram). Só TikTok: vertical 1080x1920, ~108,6 s, estilo ilustrado.
Pedido do Matheus em 17/11/2026. Sem cartaz de abertura (2b.1): no quadro 0 o crédito de quem ganha R$ 10 mil já está caindo.
Narração: Afonso (HeyGen), 1 bloco. Contas e fontes em contas.py (SAC 30 anos, sem TR/seguros, mesma base da reportagem)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(13.2, "tum"), (50.3, "tum"), (74.0, "soft_ding"), (90.0, "tum")]
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


def pct(v):
    return ("%.1f%%" % v).replace(".", ",")


# ======================================================================= CENAS
def s01(c, t):  # 0 - 7.4  quem ganha 10 mil perdeu ~40 mil de financiamento
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(260, 1150))
    topo(c, "COMPRAR IMÓVEL EM 2027")
    entra(c, t, -1, 620, 380, selo("RENDA: R$ 10 MIL", NAVY, 54, GOLD), anim="pop")
    numero_i(c, "O BANCO TE EMPRESTA", 620, 520, 44, CREME)
    v = 249000 - 42000 * ease_io(prog(t, 0.0, 5.4))
    numero_i(c, brl(v), 620, 640, 120, GOLD)
    # barra encolhendo
    rr(c, 360, 740, 520, 60, 20); rgb(c, (0.85, 0.82, 0.76)); c.fill()
    rr(c, 360, 740, 520 * v / 249000, 60, 20); rgb(c, VERMELHO if t > 3 else VERDE); c.fill()
    if t > 4.6:
        entra(c, t, 4.6, 620, 920, selo("- R$ 42 MIL", VERMELHO, 80, CREME, rot=0.05), anim="stamp")
    pessoa(c, t, 190, 1300, 1.2, VOCE, poses=((0, "think"), (4.6, "head")), exprs=((0, "think"), (4.6, "desperate")), look=0.6)


def s02(c, t):  # 7.4 - 18.8  Bradesco: 11,7% -> 15% + TR, inclusive alta renda
    cena_agencia(c, t, hora="interior")
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "DEPOIS DAS ELEIÇÕES", 540, 230, 56, CREME)
    if t > 9.0:
        entra(c, t, 9.0, 540, 380, selo("BRADESCO", VERMELHO, 60, CREME), anim="drop")
    if t > 11.0:
        v = 11.69 + (15.0 - 11.69) * ease_out(prog(t, 12.0, 1.4))
        pop(c, t, 13.2, 540, 540, pct(v) + " AO ANO", 110, GOLD) if t > 13.2 else numero_i(c, pct(v) + " AO ANO", 540, 540, 110, GOLD)
    if t > 15.4:
        entra(c, t, 15.4, 540, 670, selo("+ TR", NAVY, 54, GOLD), anim="stamp")
    if t > 16.6:
        entra(c, t, 16.6, 400, 800, selo("ALTA RENDA TAMBÉM", VERMELHO, 46, CREME), anim="stamp")
    consultor_i(c, t, 840, 1320, 1.0, poses=((0, "present"), (13.2, "head")), exprs=((0, "neutral"), (13.2, "shocked")), look=-0.6)


def s03(c, t):  # 18.8 - 22.9  Itaú quase 13, Santander 12,5
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "OS OUTROS TAMBÉM SUBIRAM", NAVY, CREME)
    linha_conta(c, t, 18.9, 450, "Itaú", "11,99 > 12,95%", 19.6, VERMELHO, vsize=54)
    linha_conta(c, t, 20.9, 610, "Santander", "11,69 > 12,49%", 21.4, VERMELHO, vsize=54)
    consultor_i(c, t, 540, 1320, 1.0, poses=((0, "point_r"), (21.4, "shrug")), exprs=((0, "neutral"), (21.4, "think")), look=0.0)


def s04(c, t):  # 22.9 - 36.2  R$ 500 mil em 30 anos: 6.017 -> 7.246 (+1.229/mês)
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(220, 1150))
    topo(c, "R$ 500 MIL EM 30 ANOS")
    linha_conta(c, t, 23.7, 430, "1ª parcela antes", "R$ 6.017", 27.6, CREME if False else VERDE)
    linha_conta(c, t, 29.9, 590, "Bradesco agora", "R$ 7.246", 31.2, VERMELHO)
    if t > 33.4:
        pop(c, t, 33.5, 600, 780, "+ R$ 1.229", 120, GOLD)
        numero_i(c, "POR MÊS", 600, 900, 56, CREME)
    consultor_i(c, t, 160, 1320, 0.95, poses=((0, "hold"), (33.5, "head")), prop=("r", prop_calc_i) if t < 33.5 else None,
                exprs=((0, "neutral"), (33.5, "shocked")), look=0.6)


def s05(c, t):  # 36.2 - 43.0  renda de 10 mil: parcela até ~30% = 3 mil
    luz("dia")
    cena_escritorio(c, t, hora="dia")
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "E QUEM GANHA R$ 10 MIL?", 540, 230, 56, CREME)
    rosca_i(c, t, 37.8, 680, 560, r=170, pct=0.30, cor=VERMELHO, d=1.2)
    if t > 39.6:
        text(c, "DA RENDA", 680, 800, 44, MARKER, NAVY)
    if t > 41.3:
        entra(c, t, 41.3, 680, 930, selo("PARCELA ATÉ R$ 3.000", NAVY, 50, GOLD), anim="stamp")
    pessoa(c, t, 230, 1300, 1.25, VOCE, poses=((0, "stand"), (41.3, "think")), exprs=((0, "think"), (41.3, "neutral")), look=0.6)


def s06(c, t):  # 43.0 - 53.1  com 11,7%: ~249 mil; com 15%: ~207 mil -> 42 mil a menos
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "QUANTO O BANCO FINANCIA", NAVY, CREME)
    barras_i(c, t, 43.2, 320, 1150, w=640, h=520, dados=(("A 11,7%", 249000, VERDE), ("A 15%", 207000, VERMELHO)),
             fmt=lambda v: brl(v), intervalo=4.3, size_val=56)
    if t > 50.3:
        entra(c, t, 50.3, 640, 340, selo("- R$ 42 MIL", VERMELHO, 70, CREME), anim="stamp")
        numero_i(c, "MESMO SALÁRIO", 640, 450, 44, NAVY, contorno=CREME) if t > 51.0 else None
    pessoa(c, t, 160, 1330, 0.95, VOCE, poses=((0, "think"), (50.3, "head")), exprs=((0, "think"), (50.3, "desperate")), look=0.6)


def s07(c, t):  # 53.1 - 62.9  15% não é a média: Caixa ~11, BB 11,6; Caixa estuda subir
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "TAXA MÍNIMA HOJE (+ TR)")
    if t > 54.2:
        entra(c, t, 54.2, 540, 350, selo("15% NÃO É A MÉDIA", GOLD, 52, TINTA), anim="stamp")
    rows = (("Caixa", "11,19%", VERDE, 56.3), ("Banco do Brasil", "11,60%", VERDE, 58.3),
            ("Santander", "12,49%", GOLD, 59.0), ("Itaú", "12,95%", GOLD, 59.4), ("Bradesco", "15,00%", VERMELHO, 59.8))
    for k, (n, v, cor, t0) in enumerate(rows):
        linha_conta(c, t, t0, 490 + k * 140, n, v, t0 + 0.3, cor, vsize=58)
    if t > 60.6:
        entra(c, t, 60.6, 600, 1230, selo("CAIXA ESTUDA SUBIR", VERMELHO, 52, CREME, rot=0.05), anim="stamp")


def s08(c, t):  # 62.9 - 79.7  2027: novo modelo da poupança; SFH até 2,25 mi; teto 12% + TR
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(200, 1150))
    topo(c, "E EM 2027?")
    c.save(); c.translate(540, 470); c.scale(1.8, 1.8); calendar(c, "JAN", VERMELHO, 52); c.restore()
    numero_i(c, "2027", 540, 640, 64, GOLD)
    if t > 65.2:
        entra(c, t, 65.2, 560, 760, selo("NOVO MODELO DA POUPANÇA", NAVY, 46, GOLD), anim="stamp")
    cartao(c, t, 68.1, 600, 920, 700, 170, "IMÓVEL ATÉ (SFH)", "R$ 2,25 MILHÕES", NAVY, 60)
    cartao(c, t, 73.8, 600, 1120, 700, 170, "JUROS LIMITADOS A", "12% AO ANO + TR", VERDE, 60)
    consultor_i(c, t, 140, 1330, 0.85, poses=((0, "present"), (73.8, "thumb")), exprs=((0, "neutral"), (73.8, "grin")), look=0.6)


def s09(c, t):  # 79.7 - 92.7  a poupança perde dinheiro (-60 bi); bancos pedem adiar; BC não decidiu
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(220, 1150))
    topo(c, "O PROBLEMA")
    numero_i(c, "POUPANÇA EM 2026", 600, 380, 52, CREME)
    contador(c, t, 80.4, 0, 60.8, 580, 520, 100, d=4.0, col=GOLD, fmt=lambda v: ("- R$ %.1f BI" % v).replace(".", ","))
    if t > 84.0:
        numero_i(c, "SAÍRAM DE JAN A OUT", 600, 630, 40, CREME)
    if t > 86.4:
        entra(c, t, 86.4, 600, 780, selo("BANCOS PEDEM ADIAR", NAVY, 52, GOLD), anim="stamp")
    if t > 88.4:
        entra(c, t, 88.4, 620, 900, selo("E MEXER NO TETO", NAVY, 52, GOLD, rot=0.05), anim="stamp")
    if t > 90.0:
        entra(c, t, 90.0, 600, 1050, selo("BC AINDA NÃO DECIDIU", GOLD, 54, TINTA), anim="stamp")
    consultor_i(c, t, 150, 1330, 0.9, poses=((0, "think"), (86.4, "shrug")), exprs=((0, "think"), (86.4, "neutral")), look=0.6)


def s10(c, t):  # 92.7 - 103.4  se vai comprar em 2027: compare bancos (> R$ 1.000/mês) e olho no teto
    luz("dia")
    cena_sala(c, t, hora="tarde")
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "VAI COMPRAR EM 2027?", 540, 230, 56, CREME)
    cartao(c, t, 95.8, 540, 440, 840, 170, "1. COMPARE BANCO POR BANCO", "+ R$ 1.000/MÊS", VERMELHO, 60)
    if t > 97.8:
        text(c, "de diferença numa parcela", 540, 560, 36, HAND, NAVY)
    cartao(c, t, 100.5, 540, 700, 840, 170, "2. DE OLHO NO TETO", "12% AO ANO", VERDE, 60)
    consultor_i(c, t, 800, 1330, 1.0, poses=((0, "finger_up"), (100.5, "point_l") if False else (100.5, "thumb")),
                exprs=((0, "confident"), (100.5, "grin")), look=-0.6)


def s11(c, t):  # 103.4 - fim  financiaria agora ou espera 2027?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "E VOCÊ?")
    entra(c, t, 104.0, 560, 430, selo("FINANCIA AGORA?", VERMELHO, 72, CREME, rot=0.05), anim="pop")
    entra(c, t, 105.6, 640, 600, selo("ESPERA 2027?", VERDE, 72, CREME), anim="pop")
    entra(c, t, 107.7, 620, 800, selo("COMENTA", GOLD, 64, TINTA), anim="stamp")
    pessoa(c, t, 200, 1330, 1.2, VOCE, poses=((0, "think"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 7.4, s01), (7.4, 18.8, s02), (18.8, 22.9, s03), (22.9, 36.2, s04), (36.2, 43.0, s05),
          (43.0, 53.1, s06), (53.1, 62.9, s07), (62.9, 79.7, s08), (79.7, 92.7, s09), (92.7, 103.4, s10),
          (103.4, 999.0, s11)]
