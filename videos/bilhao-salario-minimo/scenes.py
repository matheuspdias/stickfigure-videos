"""E se você guardasse um salário mínimo por mês até juntar R$ 1 bilhão? Só TikTok: vertical 1080x1920, ~77,2 s, estilo ilustrado.
Formato "E se..." das 10h (AUTOMATICO_TIKTOK.md 2c), sem cartaz de abertura (2b.1): no quadro 0 os salários já estão caindo na pilha.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (mínimo R$ 1.621; CDI 13,65% a.a., IR 15%; IPCA 4,5% a.a.)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(18.1, "tum"), (28.4, "tum"), (51.8, "tum"), (62.9, "soft_ding")]
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




def barra_bilhao(c, x, y, w, frac, rot="R$ 1 BILHÃO", h=60):
    rr(c, x, y, w, h, 20); rgb(c, (0.85, 0.82, 0.76)); c.fill()
    rr(c, x, y, max(h, w * frac), h, 20); rgb(c, VERDE); c.fill()
    text(c, rot, x + w / 2, y + h + 50, 42, MARKER, CREME)


def mamute(c, s=1.0, t=0.0):
    """mamute simples, olhando para a esquerda (origem = pés)"""
    c.save(); c.scale(s, s)
    pelo = (0.48, 0.32, 0.22); esc = dk(pelo, 0.25)
    for lx in (-110, -40, 50, 120):
        rr(c, lx - 30, -150, 60, 150, 20); rgb(c, esc if lx in (-40, 120) else pelo); c.fill()
    c.save(); c.translate(0, -230); c.scale(1.0, 0.7)
    c.new_sub_path(); c.arc(0, 0, 190, 0, 6.283); rgb(c, pelo); c.fill(); c.restore()
    c.new_sub_path(); c.arc(-170, -300, 105, 0, 6.283); rgb(c, pelo); c.fill()
    c.new_sub_path(); c.arc(-140, -260, 70, 0, 6.283); rgb(c, esc); c.fill()
    # tromba balançando
    a = 0.15 * math.sin(t * 2.2)
    c.save(); c.translate(-250, -280); c.rotate(a)
    c.move_to(0, 0); c.curve_to(-60, 60, -40, 170, -90, 200)
    rgb(c, pelo); c.set_line_width(46); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke(); c.restore()
    # presas
    c.move_to(-230, -230); c.curve_to(-300, -170, -330, -120, -260, -90)
    rgb(c, (0.97, 0.94, 0.86)); c.set_line_width(20); c.stroke()
    c.new_sub_path(); c.arc(-200, -320, 12, 0, 6.283); rgb(c, TINTA); c.fill()
    c.restore()


def nota_caindo(c, t, x, y_base, periodo=1.0, w=200):
    k = (t % periodo) / periodo
    y = y_base - 420 * (1 - ease_io(clamp01(k / 0.6)))
    if k < 0.6:
        c.save(); c.translate(x, y); c.rotate(math.sin(k * 9) * 0.25); nota_i(c, "100", w); c.restore()


def pilha_notas(c, x, y_base, h, w=180, cor="100"):
    """pilha alta de notas vista de lado (origem = base)"""
    col = NOTAS[cor]
    rr(c, x - w / 2 + 10, y_base - h + 10, w, h, 6); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, x - w / 2, y_base - h, w, h, 6); rgb(c, col); c.fill()
    yy = y_base
    while yy > y_base - h + 8:
        c.rectangle(x - w / 2, yy - 2, w, 2); rgb(c, lt(col, 0.35)); c.fill(); yy -= 14


# ======================================================================= CENAS
def s01(c, t):  # 0 - 9.5  um salário mínimo por mês, todo mês, sem gastar nada
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(620, 1000))
    topo(c, "E SE FOSSE ATÉ R$ 1 BILHÃO?")
    # maços caindo um por "mês" (1 por segundo) numa pilha que cresce, já no quadro 0
    n = 3 + int(t * 1.2)
    for i in range(n):
        c.save(); c.translate(680 + (i % 2) * 8, 1240 - i * 22); nota_i(c, "100", 300); c.restore()
    nota_caindo(c, t * 1.2 + 0.3, 690, 1240 - n * 22 - 40, w=300)
    mes = 1 + int(t * 1.2)
    numero_i(c, "MÊS %d" % mes, 680, 380, 80, CREME)
    numero_i(c, brl(1621 * mes), 680, 520, 130, GOLD)
    if t > 4.6:
        entra(c, t, 4.6, 680, 680, selo("+ R$ 1.621 TODO MÊS", NAVY, 60, GOLD), anim="stamp")
    if t > 8.5:
        entra(c, t, 8.5, 700, 800, selo("SEM GASTAR NADA", VERMELHO, 52, CREME, rot=0.05), anim="stamp")
    pessoa(c, t, 230, 1300, 1.3, VOCE, poses=((0, "point_r"), (4.6, "hold"), (8.5, "thumb")),
           exprs=((0, "think"), (4.6, "grin"), (8.5, "confident")), look=0.6)


def s02(c, t):  # 9.5 - 12.4  no primeiro ano, quase 20 mil
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "NO PRIMEIRO ANO", NAVY, CREME)
    mes = 1 + min(11, int(12 * prog(t, 9.6, 2.2)))
    c.save(); c.translate(560, 560); c.scale(2.0, 2.0); calendar(c, "%d" % mes, VERMELHO); c.restore()
    numero_i(c, "MÊS", 560, 390, 50, NAVY, contorno=CREME)
    contador(c, t, 9.8, 0, 19452, 500, 840, 120, d=2.2, col=VERDE)
    if t > 11.4:
        entra(c, t, 11.4, 480, 980, selo("QUASE R$ 20 MIL", NAVY, 56, GOLD), anim="stamp")
    pessoa(c, t, 860, 1330, 0.95, VOCE, poses=((0, "stand"), (11.4, "thumb")), exprs=((0, "think"), (11.4, "grin")), look=-0.6)


def s03(c, t):  # 12.4 - 16.8  primeiro milhão: 51 anos (você vira aposentado)
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1100))
    topo(c, "PRO PRIMEIRO MILHÃO")
    anos = int(51 * ease_io(prog(t, 13.0, 3.2)))
    numero_i(c, "%d ANOS" % anos, 640, 500, 150, GOLD)
    barra_bilhao(c, 380, 660, 540, 0.02 + 0.98 * ease_io(prog(t, 13.0, 3.2)), "R$ 1 MILHÃO")
    if t > 15.4:
        entra(c, t, 15.4, 650, 900, selo("51 ANOS!", VERMELHO, 70, CREME), anim="stamp")
    quem = VOCE if t < 15.0 else "aposentado"
    pessoa(c, t, 220, 1300, 1.3, quem, poses=((0, "stand"), (15.0, "head")), exprs=((0, "think"), (15.0, "shocked")), look=0.6)


def s04(c, t):  # 16.8 - 20.9  e pro bilhão? mais de 51 MIL anos
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(520, 1100))
    topo(c, "E PRO BILHÃO?")
    if t > 18.0:
        anos = int(51400 * ease_out(prog(t, 18.1, 1.6)))
        numero_i(c, "MAIS DE", 540, 370, 60, CREME)
        numero_i(c, brl(anos, 0, "") + " ANOS", 540, 500, 140, GOLD)
    if t > 19.8:
        entra(c, t, 19.8, 540, 650, selo("51 MIL ANOS", NAVY, 76, GOLD, rot=0.04), anim="stamp")
    consultor_i(c, t, 520, 1300, 1.1, poses=((0, "think"), (18.1, "head")), exprs=((0, "think"), (18.1, "shocked")), look=0.0)


def s05(c, t):  # 20.9 - 28.2  desde as pirâmides: nem 10% do caminho
    cena_deserto(c, t, hora="tarde", piramides=False)
    for x, w, h in ((260, 420, 300), (640, 560, 400), (930, 300, 210)):
        piramide(c, x, 820, w, h, depth=0.2)
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "SE COMEÇASSE NAS PIRÂMIDES", 540, 230, 50, CREME)
    if t > 22.6:
        entra(c, t, 22.6, 540, 400, selo("4.500 ANOS ATRÁS", GOLD, 60, TINTA), anim="drop")
    if t > 24.8:
        rr(c, 80, 960, 620, 210, 26); rgb(c, NAVY, 0.92); c.fill()
        barra_bilhao(c, 120, 1000, 540, 0.088 * ease_out(prog(t, 25.0, 1.4)))
    if t > 26.4:
        entra(c, t, 26.4, 560, 560, selo("NEM 10% DO CAMINHO", VERMELHO, 56, CREME, rot=0.05), anim="stamp")
    pessoa(c, t, 860, 1330, 1.1, VOCE, poses=((0, "think"), (26.4, "head")), exprs=((0, "think"), (26.4, "desperate")), look=-0.6)


def s06(c, t):  # 28.2 - 32.9  teria que ter começado na Idade da Pedra (mamute)
    cena_neve(c, t, hora="dia", nevando=True)
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "TERIA QUE COMEÇAR...", 540, 230, 54, CREME)
    x = 700 - 60 * ease_out(prog(t, 28.2, 2.0))
    c.save(); c.translate(x - 380, 1200); c.scale(-1, 1); mamute(c, 1.15, t); c.restore()
    if t > 29.4:
        entra(c, t, 29.4, 520, 420, selo("NA IDADE DA PEDRA", VERMELHO, 62, CREME), anim="stamp")
    if t > 30.6:
        entra(c, t, 30.6, 540, 560, selo("51 MIL ANOS ATRÁS", GOLD, 56, TINTA, rot=0.05), anim="drop")
    pessoa(c, t, 870, 1320, 1.1, VOCE, poses=((0, "stand"), (31.2, "head")), exprs=((0, "think"), (31.2, "shocked")), look=-0.7)


def s07(c, t):  # 32.9 - 41.6  10 milhões de notas de 100, pilha de 1 km, ~10 toneladas
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(240, 1150))
    topo(c, "R$ 1 BILHÃO EM NOTAS DE 100")
    contador(c, t, 33.6, 0, 10000000, 600, 400, 100, d=2.6, col=GOLD, prefixo="", sufixo="")
    if t > 34.5:
        numero_i(c, "NOTAS", 600, 500, 56, CREME)
    # pilha subindo e passando de um prédio
    predio_moderno(c, 860, 1290, 150, 520)
    hp = 40 + 680 * ease_io(prog(t, 36.6, 2.4))
    pilha_notas(c, 620, 1290, hp, 170)
    if t > 38.0:
        entra(c, t, 38.0, 700, 640, selo("MAIS DE 1 KM", VERMELHO, 60, CREME), anim="stamp")
    if t > 39.7:
        v = int(10 * ease_out(prog(t, 39.8, 1.0)))
        visor(c, "%d T" % v, 640, 1400 - 260, 380, 120, "BALANÇA: UMAS")
    consultor_i(c, t, 220, 1300, 1.25, poses=((0, "present"), (38.0, "head")), exprs=((0, "neutral"), (38.0, "shocked")), look=0.6)


def s08(c, t):  # 41.6 - 44.1  parece impossível? olha a virada
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(520, 1100))
    topo(c, "PARECE IMPOSSÍVEL?")
    if t > 42.9:
        pop(c, t, 43.0, 520, 430, "OLHA A VIRADA", 100, GOLD)
    consultor_i(c, t, 520, 1300, 1.4, poses=((0, "shrug"), (43.0, "finger_up")), exprs=((0, "think"), (43.0, "confident")), look=0.0)


def s09(c, t):  # 44.1 - 54.6  rendendo no CDI: ~79 anos, não 51 mil
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(200, 1150))
    topo(c, "E SE RENDESSE NO CDI?")
    if t > 44.3:
        entra(c, t, 44.3, 600, 380, selo("JÁ SEM IMPOSTO", NAVY, 52, GOLD), anim="stamp")
    grafico_curva(c, t, 45.0, 400, 860, w=500, h=330, d=4.5, cor=VERDE, eixo_x=("hoje", "79 anos"), f=lambda k: k ** 6)
    if t > 49.6:
        pop(c, t, 49.7, 650, 990, "79 ANOS", 110, GOLD)
    if t > 51.7:
        entra(c, t, 51.7, 640, 1130, selo("NÃO 51 MIL!", VERMELHO, 62, CREME), anim="stamp")
    consultor_i(c, t, 170, 1300, 1.15, poses=((0, "hold"), (49.7, "arms_up")), prop=("r", prop_tablet_i),
                exprs=((0, "neutral"), (49.7, "grin")), look=0.6)


def s10(c, t):  # 54.6 - 58.9  primeiro milhão: 17 anos, não 51
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "PRO PRIMEIRO MILHÃO", NAVY, CREME)
    barras_i(c, t, 54.9, 300, 1120, w=640, h=620, dados=(("GUARDANDO", 51, VERMELHO), ("NO CDI", 17, VERDE)),
             fmt=lambda v: "%d ANOS" % round(v), intervalo=1.4, size_val=64)
    pessoa(c, t, 150, 1330, 1.0, VOCE, poses=((0, "think"), (56.5, "arms_up")), exprs=((0, "think"), (56.5, "grin")), look=0.6)


def s11(c, t):  # 58.9 - 64.7  você colocou só 1,5 milhão; o resto é juros
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(220, 1150))
    topo(c, "DO BILHÃO INTEIRO...")
    rosca_i(c, t, 61.0, 620, 640, r=210, pct=0.998, cor=VERDE, texto="99,8%" if t > 62.0 else None, d=1.2)
    if t > 59.6:
        rr(c, 330, 900, 580, 130, 22); rgb(c, CREME); c.fill()
        text(c, "VOCÊ COLOCOU:", 620, 945, 40, MARKER, NAVY)
        text(c, "SÓ R$ 1,5 MILHÃO", 620, 1005, 52, MARKER, VERMELHO)
    if t > 62.9:
        entra(c, t, 62.9, 620, 1130, selo("O RESTO É JUROS", GOLD, 58, TINTA, rot=0.04), anim="stamp")
    consultor_i(c, t, 180, 1300, 1.15, poses=((0, "present"), (62.9, "arms_up")), exprs=((0, "neutral"), (62.9, "grin")), look=0.6)


def s12(c, t):  # 64.7 - 72.1  inflação: o bilhão vale uns 30 milhões de hoje
    luz("dia")
    cena_agencia(c, t, hora="interior")
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "SÓ UM DETALHE: A INFLAÇÃO", 540, 230, 52, CREME)
    if t > 66.0:
        def eti(c):
            etiqueta_preco(c, "R$ 1 BILHÃO", GOLD, 60)
        entra(c, t, 66.0, 380, 470, eti, anim="drop")
    if t > 68.6:
        # risco vermelho sobre o bilhão
        k = ease_out(prog(t, 68.6, 0.4))
        line(c, 420, 470, 420 + 430 * k, 470, 12, VERMELHO)
        entra(c, t, 69.6, 480, 640, selo("= UNS R$ 30 MILHÕES", VERDE, 56, CREME), anim="stamp")
        numero_i(c, "EM DINHEIRO DE HOJE", 480, 760, 44, NAVY, contorno=CREME) if t > 70.2 else None
    consultor_i(c, t, 800, 1300, 1.05, poses=((0, "finger_up"), (68.6, "shrug")), prop=("r", prop_calc_i) if t > 66 else None,
                exprs=((0, "think"), (68.6, "neutral")), look=-0.6)


def s13(c, t):  # 72.1 - fim  se você tivesse um bilhão, o que fazia primeiro?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "COM R$ 1 BILHÃO...")
    if t > 73.6:
        pop(c, t, 73.7, 560, 380, "O QUE VOCÊ", 96, GOLD)
    if t > 74.6:
        numero_i(c, "FAZIA PRIMEIRO?", 560, 490, 80, GOLD)
    for i, (t0, s, x, y, cor) in enumerate(((72.3, "CASA?", 700, 650, VERDE), (72.7, "VIAGEM?", 520, 790, BLUE),
                                            (73.1, "AJUDAR A FAMÍLIA?", 690, 930, PURPLE), (73.5, "INVESTIR?", 560, 1070, NAVY))):
        entra(c, t, t0, x, y, selo(s, cor, 52, CREME, rot=(-0.06 if i % 2 else 0.06)), anim="pop")
    entra(c, t, 76.3, 600, 1220, selo("COMENTA", VERMELHO, 64, CREME), anim="stamp")
    pessoa(c, t, 200, 1330, 1.2, VOCE, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 9.5, s01), (9.5, 12.4, s02), (12.4, 16.8, s03), (16.8, 20.9, s04), (20.9, 28.2, s05),
          (28.2, 32.9, s06), (32.9, 41.6, s07), (41.6, 44.1, s08), (44.1, 54.6, s09), (54.6, 58.9, s10),
          (58.9, 64.7, s11), (64.7, 72.1, s12), (72.1, 999.0, s13)]
