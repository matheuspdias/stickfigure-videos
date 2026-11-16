"""Comprar ou alugar em 2026? (Parte 1 de 3): a conta do primeiro mês. Só TikTok: vertical 1080x1920, ~98,4 s, estilo ilustrado.
Conta útil das 18h (AUTOMATICO_TIKTOK.md 2b.2/2b.3), série numerada; sem cartaz de abertura (2b.1): no quadro 0 as barras de aluguel e parcela já estão subindo.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (apê R$ 300 mil, entrada 20%, SAC 30 anos ~12% a.a.; aluguel 0,5%/mês; CDI 13,65%, IR 15%; valorização 5% a.a.)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(32.8, "tum"), (55.6, "tum"), (64.3, "tum"), (78.2, "soft_ding")]
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
    k = ease_out(clamp01((t - t0) / 0.35))
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


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.5  comprar ou alugar em 2026? a conta do 1º mês. Parte 1
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "COMPRAR OU ALUGAR EM 2026?")
    barras_i(c, t, -1.6, 330, 1150, w=600, h=640, dados=(("ALUGAR", 1500, VERDE), ("COMPRAR", 2944, VERMELHO)),
             fmt=lambda v: brl(v), d=2.4, intervalo=0.6, size_val=60)
    if t > 2.8:
        entra(c, t, 2.8, 470, 360, selo("1º MÊS", GOLD, 60, TINTA), anim="stamp")
    if t > 5.7:
        entra(c, t, 5.7, 640, 1300, selo("PARTE 1", VERMELHO, 56, CREME, rot=0.06), anim="stamp")
    consultor_i(c, t, 140, 1300, 0.95, poses=((0, "point_r"), (2.8, "think")), exprs=((0, "neutral"), (2.8, "shocked")), look=0.6)


def s02(c, t):  # 6.5 - 11.9  apartamento de 300 mil; aluguel 1.500
    cena_rua(c, t, hora="dia", carros=True)
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "O MESMO APARTAMENTO", 540, 230, 54, CREME)
    predio_apto(c, 700, 1240, 1.0)
    if t > 7.0:
        entra(c, t, 7.0, 560, 420, lambda c: etiqueta_preco(c, "R$ 300 MIL", GOLD, 64), anim="drop")
    if t > 10.2:
        entra(c, t, 10.2, 620, 600, selo("ALUGUEL: R$ 1.500/MÊS", VERDE, 50, CREME), anim="stamp")
    pessoa(c, t, 230, 1300, 1.25, VOCE, poses=((0, "point_r"), (10.2, "think")), exprs=((0, "think"), (10.2, "neutral")), look=0.6)


def s03(c, t):  # 11.9 - 22.6  pra comprar: entrada 60 mil, 30 anos, ~12% ao ano
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "PRA COMPRAR", NAVY, CREME)
    linha_conta(c, t, 12.4, 380, "Entrada", "R$ 60 MIL", 13.0, NAVY)
    linha_conta(c, t, 13.6, 520, "Financia", "R$ 240 MIL", 14.4, VERMELHO)
    linha_conta(c, t, 15.6, 660, "Prazo", "30 ANOS", 16.3, NAVY)
    linha_conta(c, t, 17.2, 800, "Juros", "~12% AO ANO", 18.6, VERMELHO, vsize=56)
    if t > 19.8:
        entra(c, t, 19.8, 540, 935, selo("PREÇO DOS BANCOS EM 2026", GOLD, 44, TINTA), anim="stamp")
    consultor_i(c, t, 540, 1340, 0.6, poses=((0, "hold"),), prop=("r", prop_calc_i), exprs=((0, "neutral"), (19.8, "think")), look=0.0)


def s04(c, t):  # 22.6 - 26.7  primeira parcela: ~2.950
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(260, 1150))
    topo(c, "PRIMEIRA PARCELA")
    contador(c, t, 22.9, 0, 2944, 600, 480, 150, d=2.6, col=GOLD)
    if t > 25.6:
        entra(c, t, 25.6, 600, 640, selo("UNS R$ 2.950 POR MÊS", NAVY, 52, GOLD), anim="stamp")
    if t > 23.8:
        entra(c, t, 23.8, 680, 960, lambda c: notificacao(c, 0, 0, 1.0, titulo="Boleto do financiamento", texto="vence dia 10", cor=VERMELHO, app="BANCO"), anim="drop")
    pessoa(c, t, 200, 1300, 1.25, VOCE, poses=((0, "stand"), (24.5, "head")), exprs=((0, "think"), (24.5, "shocked")), look=0.6)


def s05(c, t):  # 26.7 - 38.3  dentro da parcela: 667 abate, 2.277 são juros (>3/4)
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(200, 1150))
    topo(c, "DENTRO DA PARCELA")
    rosca_i(c, t, 33.0, 540, 640, r=190, pct=0.77, cor=VERMELHO, texto="77%" if t > 34.2 else " ", d=1.2)
    if t > 33.8:
        text(c, "É JUROS", 540, 905, 44, MARKER, CREME)
    linha_conta(c, t, 28.9, 1010, "Abate a dívida", "R$ 667", 30.6, VERDE)
    linha_conta(c, t, 32.8, 1160, "Juros", "R$ 2.277", 33.4, VERMELHO)
    if t > 35.8:
        entra(c, t, 35.8, 540, 360, selo("MAIS DE 3/4 DA PARCELA", GOLD, 46, TINTA), anim="stamp")


def s06(c, t):  # 38.3 - 43.4  só os juros = 1,5x o aluguel
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "SÓ OS JUROS...", NAVY, CREME)
    barras_i(c, t, 38.6, 320, 1150, w=620, h=560, dados=(("JUROS", 2277, VERMELHO), ("ALUGUEL", 1500, VERDE)),
             fmt=lambda v: brl(v), intervalo=0.8, size_val=60)
    if t > 40.6:
        entra(c, t, 40.6, 600, 340, selo("1,5 VEZ O ALUGUEL", VERMELHO, 60, CREME), anim="stamp")
    pessoa(c, t, 160, 1330, 0.95, VOCE, poses=((0, "think"), (40.6, "head")), exprs=((0, "think"), (40.6, "shocked")), look=0.6)


def s07(c, t):  # 43.4 - 53.5  os 60 mil da entrada no CDI: ~550/mês que você deixa de ganhar
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1150))
    topo(c, "E TEM MAIS: A ENTRADA")
    if t > 44.4:
        entra(c, t, 44.4, 450, 470, lambda c: maco(c, "100", 7, 260), anim="drop")
        numero_i(c, "R$ 60 MIL", 450, 640, 70, GOLD)
    if t > 46.2:
        celular_app(c, t, 790, 640, 0.75, titulo="No CDI", valor="+ R$ 550", sub="por mês", curva=lambda k: k ** 1.3, cor=NAVY, t0=46.4)
    if t > 48.4:
        pop(c, t, 48.5, 610, 1000, "UNS R$ 550/MÊS", 64, GOLD)
    if t > 51.1:
        entra(c, t, 51.1, 600, 1130, selo("QUE VOCÊ DEIXA DE GANHAR", VERMELHO, 44, CREME), anim="stamp")
    consultor_i(c, t, 130, 1300, 0.9, poses=((0, "present"), (51.1, "shrug")), exprs=((0, "neutral"), (51.1, "think")), look=0.6)


def s08(c, t):  # 53.5 - 61.6  juros + rendimento perdido = ~2.830 que não voltam x 1.500
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(540, 1250))
    topo(c, "O QUE NÃO VOLTA")
    linha_conta(c, t, 53.6, 420, "Juros", "R$ 2.277", 53.9, VERMELHO)
    linha_conta(c, t, 54.2, 570, "Rendimento perdido", "R$ 551", 54.6, VERMELHO, vsize=56)
    if t > 55.6:
        k = ease_out(prog(t, 55.6, 0.4))
        c.rectangle(120, 660, 840 * k, 8); rgb(c, CREME); c.fill()
        contador(c, t, 55.7, 0, 2828, 540, 770, 120, d=2.4, col=GOLD)
    if t > 58.4:
        entra(c, t, 58.4, 540, 900, selo("POR MÊS", NAVY, 48, GOLD), anim="stamp")
    if t > 59.6:
        entra(c, t, 59.6, 620, 1040, selo("x ALUGUEL R$ 1.500", VERDE, 56, CREME, rot=0.05), anim="stamp")
    pessoa(c, t, 120, 1360, 0.85, VOCE, poses=((0, "stand"), (55.7, "head")), exprs=((0, "think"), (55.7, "desperate")), look=0.6)


def s09(c, t):  # 61.6 - 65.4  então alugar ganha disparado? calma, olha a virada
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(520, 1100))
    topo(c, "ALUGAR GANHA DISPARADO?")
    if t > 63.5:
        pop(c, t, 63.6, 520, 400, "CALMA...", 90, CREME)
    if t > 64.3:
        pop(c, t, 64.3, 520, 530, "OLHA A VIRADA", 96, GOLD)
    consultor_i(c, t, 520, 1300, 1.3, poses=((0, "shrug"), (63.6, "finger_up")), exprs=((0, "think"), (63.6, "confident")), look=0.0)


def s10(c, t):  # 65.4 - 72.0  o apê valoriza: ~5% ao ano = ~1.200/mês a seu favor
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1150))
    topo(c, "O APARTAMENTO VALORIZA")
    grafico_curva(c, t, 66.0, 400, 760, w=420, h=300, d=2.2, cor=VERDE, eixo_x=("hoje", "+1 ano"), f=lambda k: k ** 1.2)
    if t > 67.1:
        entra(c, t, 67.1, 600, 360, selo("UNS 5% AO ANO", NAVY, 54, GOLD), anim="stamp")
    if t > 69.0:
        pop(c, t, 69.1, 620, 930, "+ R$ 1.200/MÊS", 70, GOLD)
    if t > 70.6:
        entra(c, t, 70.6, 620, 1060, selo("A SEU FAVOR", VERDE, 50, CREME), anim="stamp")
    consultor_i(c, t, 130, 1330, 0.85, poses=((0, "point_r"), (69.1, "thumb")), exprs=((0, "neutral"), (69.1, "grin")), look=0.6)


def s11(c, t):  # 72.0 - 80.9  comprando custa ~1.600 x aluguel 1.500: praticamente empate
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "DESCONTANDO A VALORIZAÇÃO", NAVY, CREME)
    barras_i(c, t, 72.6, 320, 1100, w=620, h=560, dados=(("COMPRAR", 1606, VERMELHO), ("ALUGAR", 1500, VERDE)),
             fmt=lambda v: brl(v), intervalo=3.0, size_val=62, maxv=1700)
    if t > 78.2:
        entra(c, t, 78.2, 620, 380, selo("PRATICAMENTE EMPATE", NAVY, 56, GOLD), anim="stamp")
    pessoa(c, t, 160, 1330, 0.95, VOCE, poses=((0, "think"), (78.2, "shrug")), exprs=((0, "think"), (78.2, "neutral")), look=0.6)


def s12(c, t):  # 80.9 - 88.4  quem decide: valorização e o que você faz com os 1.400 de diferença
    luz("dia")
    cena_sala(c, t, hora="tarde")
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "QUEM DECIDE?", 540, 230, 58, CREME)
    cartao(c, t, 81.6, 540, 450, 820, 190, "1. QUANTO O IMÓVEL VALORIZA", "+5%? +2%?", VERDE, 62)
    cartao(c, t, 84.2, 540, 700, 820, 220, "2. O QUE VOCÊ FAZ COM A DIFERENÇA", "R$ 1.400/MÊS", GOLD, 70)
    if t > 86.6:
        entra(c, t, 86.6, 400, 880, selo("INVESTE OU GASTA?", VERMELHO, 52, CREME), anim="stamp")
    consultor_i(c, t, 800, 1330, 1.0, poses=((0, "finger_up"), (84.2, "present")), exprs=((0, "think"), (84.2, "neutral")), look=-0.6)


def s13(c, t):  # 88.4 - 93.1  parte 2: a conta de 10 anos com os números de 2026
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1150))
    topo(c, "NA PARTE 2")
    ano = 2026 + min(10, int(10 * ease_io(prog(t, 89.0, 2.6))))
    c.save(); c.translate(640, 560); c.scale(2.2, 2.2); calendar(c, "%d" % ano, VERMELHO, 46); c.restore()
    if t > 90.6:
        entra(c, t, 90.6, 600, 900, selo("A CONTA DE 10 ANOS", GOLD, 50, TINTA), anim="stamp")
    consultor_i(c, t, 180, 1330, 0.95, poses=((0, "present"), (90.6, "thumb")), exprs=((0, "neutral"), (90.6, "grin")), look=0.6)


def s14(c, t):  # 93.1 - fim  hoje você paga aluguel ou parcela? comenta e segue
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "E VOCÊ, HOJE PAGA...")
    entra(c, t, 93.8, 560, 430, selo("ALUGUEL?", VERDE, 84, CREME, rot=0.05), anim="pop")
    entra(c, t, 94.6, 640, 600, selo("PARCELA?", VERMELHO, 84, CREME), anim="pop")
    entra(c, t, 95.9, 620, 800, selo("COMENTA", GOLD, 64, TINTA), anim="stamp")
    entra(c, t, 96.6, 620, 960, selo("SEGUE PRA PARTE 2", NAVY, 52, GOLD, rot=0.04), anim="stamp")
    pessoa(c, t, 200, 1330, 1.2, VOCE, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 6.5, s01), (6.5, 11.9, s02), (11.9, 22.6, s03), (22.6, 26.7, s04), (26.7, 38.3, s05),
          (38.3, 43.4, s06), (43.4, 53.5, s07), (53.5, 61.6, s08), (61.6, 65.4, s09), (65.4, 72.0, s10),
          (72.0, 80.9, s11), (80.9, 88.4, s12), (88.4, 93.1, s13), (93.1, 999.0, s14)]
