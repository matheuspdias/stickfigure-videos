"""E se você guardasse R$ 1 por segundo? Só TikTok: vertical nativo 1080x1920, ~68,8 s, estilo ilustrado.
Formato "E se..." das 10h (AUTOMATICO_TIKTOK.md 2c), sem cartaz de abertura (2b.1): no quadro 0 as moedas já estão caindo.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (moeda de R$ 1 = 7 g, CDI 13,65% a.a., IR 17,5%, mínimo R$ 1.621)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(13.1, "soft_ding"), (24.7, "tum"), (33.7, "tum"), (61.9, "soft_ding")]
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


def cronometro(c, t, s=1.0):
    """cronômetro com o ponteiro dando um tique por segundo"""
    c.save(); c.scale(s, s)
    rr(c, -26, -118, 52, 30, 8); rgb(c, dk(GOLD, 0.2)); c.fill()
    c.new_sub_path(); c.arc(0, 6, 100, 0, 6.283); rgb(c, (0, 0, 0), 0.25); c.fill()
    c.new_sub_path(); c.arc(0, 0, 100, 0, 6.283); rgb(c, GOLD); c.fill()
    c.new_sub_path(); c.arc(0, 0, 82, 0, 6.283); rgb(c, (0.99, 0.98, 0.95)); c.fill()
    for i in range(12):
        a = i * math.pi / 6
        line(c, 66 * math.cos(a), 66 * math.sin(a), 76 * math.cos(a), 76 * math.sin(a), 5, TINTA)
    seg = math.floor(t) + ease_out(clamp01((t % 1) / 0.15))
    a = seg * 2 * math.pi / 60
    line(c, 0, 0, 62 * math.sin(a), -62 * math.cos(a), 7, VERMELHO)
    c.new_sub_path(); c.arc(0, 0, 9, 0, 6.283); rgb(c, TINTA); c.fill()
    c.restore()


def moeda_caindo(c, t, x, y_base, periodo=1.0, r=46):
    """uma moeda cai a cada segundo em (x, y_base)"""
    k = (t % periodo) / periodo
    y = y_base - 420 * (1 - ease_io(clamp01(k / 0.6)))
    if k < 0.6:
        c.save(); c.translate(x, y); c.rotate(k * 6); moeda_i(c, r); c.restore()


def ao_vivo(c, t, x, y, size=120):
    """o que você teria guardado desde o segundo 0 deste vídeo"""
    numero_i(c, "R$ %d" % int(t), x, y, size, GOLD)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.9  um real por segundo, sem parar nem pra dormir
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(560, 900))
    topo(c, "E SE FOSSE R$ 1 POR SEGUNDO?")
    # moedas caindo uma por segundo num cofre-pilha (já em movimento no quadro 0)
    n = 4 + int(t)
    c.save(); c.translate(680, 1260); pilha_moedas(c, n, 95); c.restore()
    moeda_caindo(c, t + 0.35, 680, 1260 - n * 95 * 0.32 - 40, r=70)
    c.save(); c.translate(680, 520); cronometro(c, t + 0.35, 1.4); c.restore()
    numero_i(c, "R$ %d" % (4 + int(t)), 680, 760, 140, GOLD)
    if t > 4.7:
        entra(c, t, 4.7, 400, 330, selo("24 HORAS POR DIA", NAVY, 54, GOLD), anim="stamp")
    pessoa(c, t, 230, 1300, 1.3, VOCE, poses=((0, "point_r"), (2.4, "think"), (4.7, "head")),
           exprs=((0, "think"), (2.4, "grin"), (4.7, "shocked")), look=0.6)


def s02(c, t):  # 6.9 - 14.4  1 minuto, 1 hora, 27 minutos = 1 salário mínimo
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "QUANTO JUNTA EM...", NAVY, CREME)
    linha_conta(c, t, 6.9, 430, "1 minuto", "R$ 60", 7.6, VERDE)
    linha_conta(c, t, 8.5, 590, "1 hora", "R$ 3.600", 9.7, VERDE)
    linha_conta(c, t, 10.9, 750, "27 minutos", "1 SALÁRIO", 13.1, NAVY)
    if t > 13.1:
        numero_i(c, "MÍNIMO INTEIRO!", 600, 880, 64, VERDE)
    c.save(); c.translate(800, 1100); cronometro(c, t * 6, 0.9); c.restore()
    pessoa(c, t, 300, 1430, 0.85, VOCE, poses=((0, "stand"), (9.7, "thumb"), (13.1, "arms_up")),
           exprs=((0, "think"), (9.7, "grin"), (13.1, "shocked")), look=0.6)


def s03(c, t):  # 14.4 - 22.9  em um dia: 86.400 reais, uns 600 kg de moedas
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    topo(c, "EM UM DIA")
    contador(c, t, 15.4, 0, 86400, 540, 430, 130, d=2.6, col=GOLD)
    # pilhas de moedas que crescem
    for i in range(5):
        h = int(3 + 16 * ease_out(prog(t, 15.6 + i * 0.25, 3.0)))
        c.save(); c.translate(500 + i * 95, 1000 - (i % 2) * 20); pilha_moedas(c, h, 44); c.restore()
    if t > 18.7:
        v = int(600 * ease_out(prog(t, 19.6, 1.4)))
        visor(c, "%d KG" % v, 640, 1140, 480, 130, "BALANÇA")
    if t > 21.4:
        entra(c, t, 21.4, 540, 600, selo("POR DIA!", VERMELHO, 70, CREME), anim="stamp")
    consultor_i(c, t, 220, 1300, 1.3, poses=((0, "present"), (19.7, "head")), exprs=((0, "neutral"), (19.7, "shocked")), look=0.6)


def s04(c, t):  # 22.9 - 25.7  menos de 12 dias: milionário
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(540, 1100))
    topo(c, "MENOS DE 12 DIAS")
    dia = 1 + min(11, int(11 * ease_out(prog(t, 22.9, 1.6))))
    c.save(); c.translate(540, 520); c.scale(2.0, 2.0); calendar(c, "%d" % dia, VERMELHO); c.restore()
    if t > 24.7:
        chuva_dinheiro(c, t, 24.7, n=22, seed=4)
        entra(c, t, 24.7, 540, 820, selo("MILIONÁRIO", GOLD, 92, TINTA, rot=0.04), anim="stamp")
    pessoa(c, t, 540, 1430, 1.0, VOCE, poses=((0, "think"), (24.7, "arms_up")), exprs=((0, "think"), (24.7, "grin")), look=0.0)


def s05(c, t):  # 25.7 - 32.2  em um ano: 31,5 milhões e ~220 toneladas
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "EM UM ANO", NAVY, CREME)
    contador(c, t, 26.6, 0, 31536000, 540, 420, 110, d=2.2, col=VERDE)
    if t > 28.6:
        numero_i(c, "31,5 MILHÕES", 540, 540, 70, NAVY, contorno=CREME)
    # toneladas: caçambas de moedas aparecendo
    if t > 29.9:
        for i in range(6):
            ti = 29.9 + i * 0.18
            if t < ti:
                break
            x = 380 + (i % 3) * 220; y = 880 + (i // 3) * 190
            c.save(); c.translate(x, y); pilha_moedas(c, 8, 62); c.restore()
        pop(c, t, 30.4, 620, 1210, "QUASE 220 TONELADAS", 56, VERMELHO, CREME)
    pessoa(c, t, 150, 1330, 1.0, VOCE, poses=((0, "stand"), (28.0, "head")), exprs=((0, "think"), (28.0, "shocked")), look=0.6)


def s06(c, t):  # 32.2 - 35.0  parece muito? olha a virada
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(520, 1100))
    topo(c, "PARECE MUITO?")
    if t > 33.6:
        pop(c, t, 33.7, 520, 420, "OLHA A VIRADA", 100, GOLD)
    consultor_i(c, t, 520, 1300, 1.4, poses=((0, "shrug"), (33.7, "finger_up")), exprs=((0, "think"), (33.7, "confident")), look=0.0)


def s07(c, t):  # 35.0 - 42.0  1 bilhão: quase 32 anos, sem gastar um centavo
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    topo(c, "PRA CHEGAR EM R$ 1 BILHÃO")
    if t > 36.6:
        anos = 32 * ease_io(prog(t, 37.0, 2.4))
        numero_i(c, "QUASE", 640, 400, 60, CREME) if t > 37.9 else None
        numero_i(c, "%d ANOS" % round(anos), 640, 530, 140, GOLD)
        # barra de progresso até o bilhão
        rr(c, 380, 660, 520, 60, 20); rgb(c, (0.85, 0.82, 0.76)); c.fill()
        rr(c, 380, 660, 520 * max(0.03, anos / 32), 60, 20); rgb(c, VERDE); c.fill()
        text(c, "R$ 1 BI", 640, 770, 44, MARKER, CREME)
    if t > 40.9:
        entra(c, t, 40.9, 620, 900, selo("SEM GASTAR 1 CENTAVO", VERMELHO, 44, CREME), anim="stamp")
    consultor_i(c, t, 180, 1300, 1.1, poses=((0, "present"), (39.1, "head")), exprs=((0, "neutral"), (39.1, "shocked")), look=0.6)


def s08(c, t):  # 42.0 - 54.0  no CDI, em ~6,5 anos os juros pagam mais de R$ 1 por segundo
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(230, 1100))
    topo(c, "SÓ QUE TEM UM DETALHE")
    if t > 44.0:
        entra(c, t, 44.0, 600, 390, selo("RENDENDO NO CDI", NAVY, 58, GOLD), anim="stamp")
    grafico_curva(c, t, 44.6, 390, 900, w=500, h=360, d=2.4, cor=VERDE, eixo_x=("hoje", "6,5 anos"))
    if t > 45.8:
        pop(c, t, 45.8, 640, 1010, "EM 6 ANOS E MEIO", 54, GOLD)
    if t > 47.6:
        rr(c, 330, 1060, 580, 130, 22); rgb(c, CREME); c.fill()
        text(c, "SÓ OS JUROS:", 620, 1105, 40, MARKER, NAVY)
        v = 0.11 + 0.89 * ease_out(prog(t, 47.8, 1.8))
        text(c, "R$ %s POR SEGUNDO" % ("%.2f" % v).replace(".", ","), 620, 1170, 50, MARKER, VERDE)
    if t > 51.2:
        entra(c, t, 51.2, 620, 1290, selo("TRABALHA MAIS QUE VOCÊ", GOLD, 42, TINTA, rot=0.04), anim="pop")
    consultor_i(c, t, 170, 1300, 1.15, poses=((0, "think"), (44.0, "hold"), (51.2, "arms_up")), prop=("r", prop_tablet_i),
                exprs=((0, "think"), (44.0, "neutral"), (49.3, "grin")), look=0.6)


def s09(c, t):  # 54.0 - 59.2  vida real: no salário mínimo, ~8 minutos de trabalho por R$ 1
    luz("dia")
    cena_escritorio(c, t, hora="dia")
    rr(c, 90, 180, 900, 110, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "AGORA, A VIDA REAL", 540, 235, 58, CREME)
    pessoa(c, t, 300, 1300, 1.3, VOCE, poses=((0, "stand"), (57.4, "head")), exprs=((0, "neutral"), (57.4, "desperate")), look=0.6)
    if t > 55.9:
        entra(c, t, 55.9, 680, 470, lambda c: contracheque(c, 0, 0, 0.9, bruto="R$ 1.621", descontos=(("INSS", "- R$ 122"),), liquido="R$ 1.499"), anim="drop")
    if t > 57.4:
        c.save(); c.translate(720, 860); cronometro(c, t * 8, 0.9); c.restore()
        entra(c, t, 57.4, 680, 1100, selo("8 MIN = R$ 1", VERMELHO, 70, CREME), anim="stamp")


def s10(c, t):  # 59.2 - 63.7  enquanto você via: uns 70 reais
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    topo(c, "ENQUANTO VOCÊ ASSISTIA...")
    c.save(); c.translate(660, 560); cronometro(c, t, 1.3); c.restore()
    ao_vivo(c, t, 660, 860, 150)
    numero_i(c, "JÁ GUARDADOS", 660, 980, 56, CREME)
    if t > 61.9:
        entra(c, t, 61.9, 640, 1130, selo("UNS R$ 70", VERDE, 70, CREME), anim="stamp")
    pessoa(c, t, 220, 1300, 1.3, VOCE, poses=((0, "point_r"), (61.9, "arms_up")), exprs=((0, "think"), (61.9, "grin")), look=0.6)


def s11(c, t):  # 63.7 - fim  o que você comprava primeiro?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "COM R$ 1 POR SEGUNDO...")
    pop(c, t, 65.9, 560, 380, "O QUE VOCÊ", 96, GOLD) if t > 65.9 else None
    numero_i(c, "COMPRAVA PRIMEIRO?", 560, 490, 76, GOLD) if t > 66.5 else None
    for i, (t0, s, x, y, cor) in enumerate(((64.0, "CASA?", 700, 650, VERDE), (64.4, "CARRO?", 520, 790, BLUE),
                                            (64.8, "VIAGEM?", 760, 930, PURPLE), (65.2, "INVESTIR?", 560, 1070, NAVY))):
        entra(c, t, t0, x, y, selo(s, cor, 54, CREME, rot=(-0.06 if i % 2 else 0.06)), anim="pop")
    entra(c, t, 67.9, 600, 1220, selo("COMENTA", VERMELHO, 64, CREME), anim="stamp")
    pessoa(c, t, 200, 1330, 1.2, VOCE, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 6.9, s01), (6.9, 14.4, s02), (14.4, 22.9, s03), (22.9, 25.7, s04), (25.7, 32.2, s05),
          (32.2, 35.0, s06), (35.0, 42.0, s07), (42.0, 54.0, s08), (54.0, 59.2, s09), (59.2, 63.7, s10),
          (63.7, 999.0, s11)]
