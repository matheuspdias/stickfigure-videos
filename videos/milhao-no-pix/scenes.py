"""E se você acordasse com R$ 1 milhão no Pix? Só TikTok: vertical nativo 1080x1920, ~65,9 s, estilo ilustrado.
Formato "E se..." das 10h (AUTOMATICO_TIKTOK.md 2c), sem cartaz de abertura (2b.1): no quadro 0 o saldo já está subindo.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (CDI 13,65% a.a., IR 17,5%, IPCA ~4,6%)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(2.9, "soft_ding"), (13.9, "tum"), (35.0, "tum"), (60.4, "soft_ding")]
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


def mochila(c, s=1.0, cor=(0.20, 0.42, 0.62)):
    c.save(); c.scale(s, s)
    rr(c, -130 + 10, -170 + 12, 260, 340, 60); rgb(c, (0, 0, 0), 0.22); c.fill()
    c.set_line_width(18); rgb(c, dk(cor, 0.3))
    c.new_sub_path(); c.arc(0, -170, 60, math.pi, 0); c.stroke()
    rr(c, -130, -170, 260, 340, 60); rgb(c, cor); c.fill()
    rr(c, -95, 10, 190, 130, 30); rgb(c, dk(cor, 0.18)); c.fill()
    c.save(); c.translate(0, -70); c.rotate(-0.08); maco(c, "100", 3, 170); c.restore()
    c.set_line_width(8); rgb(c, TINTA, 0.6); c.move_to(-95, 40); c.line_to(95, 40); c.stroke()
    c.restore()


def linha_conta(c, t, t0, y, nome, valor, t_val, cor=VERMELHO):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.35))
    x = 540 - 600 * (1 - k)
    rr(c, x - 420, y - 62, 840, 124, 22); rgb(c, CREME); c.fill()
    text(c, nome, x - 390, y + 18, 50, MARKER, TINTA, align="l")
    if t >= t_val:
        kk = 1 + 0.14 * math.sin(clamp01((t - t_val) / 0.3) * math.pi)
        c.save(); c.translate(x + 390, y + 18); c.scale(kk, kk)
        text(c, valor, 0, 0, 62, MARKER, cor, align="r"); c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.0  o saldo subindo: R$ 1 milhão no Pix
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(560, 900))
    topo(c, "E SE CAÍSSE NO SEU PIX?")
    chuva_dinheiro(c, t, 3.3, n=22, seed=3) if t > 3.3 else None
    v = int(1000000 * ease_out(clamp01((t + 0.4) / 3.2)))
    linhas = [("Pix", "+ R$ 1 MI", VERDE)] if t > 2.9 else None
    celular_app(c, t, 640, 850, 1.15, titulo="Saldo", valor="R$ %s" % format(v, ",").replace(",", "."),
                linhas=linhas, cor=VERDE, t0=2.9, d=0.4)
    if t > 2.9:
        entra(c, t, 2.9, 560, 400, lambda c: notificacao(c, 0, 0, 1.0, titulo="Pix recebido!", texto="R$ 1.000.000,00", cor=VERDE, app="BANCO"), anim="drop")
    if t > 5.3:
        entra(c, t, 5.3, 640, 1180, selo("É TODO SEU", NAVY, 60, GOLD), anim="stamp")
    pessoa(c, t, 210, 1300, 1.3, VOCE, poses=((0, "stand"), (3.5, "head"), (5.3, "arms_up")),
           exprs=((0, "think"), (3.5, "shocked"), (5.3, "grin")), look=0.6)


def s02(c, t):  # 6.0 - 14.9  10 mil notas de 100: 1 metro, mochila, 10 kg
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "EM NOTAS DE R$ 100", NAVY, CREME)
    if t < 12.1:
        n = int(10000 * ease_out(prog(t, 7.6, 1.2))) if t > 7.6 else 0
        numero_i(c, "%s NOTAS" % format(n, ",").replace(",", "."), 560, 380, 84, GOLD) if t > 7.6 else None
        entra(c, t, 6.4, 650, 650, lambda c: maco(c, "100", 6, 320), anim="pop") if t < 9.0 else None
        # pilha ao lado da pessoa: sobe até 1 metro
        k = ease_out(prog(t, 9.0, 2.4)) if t > 9.0 else 0
        base, alt = 1300, 600
        h = alt * k
        c.rectangle(520, base - h, 260, h); rgb(c, NOTAS["100"]); c.fill()
        for yy in range(int(base - h), base, 12):
            line(c, 520, yy, 780, yy, 2, dk(NOTAS["100"], 0.25))
        if t > 10.6:
            line(c, 830, base, 830, base - alt, 5, NAVY)
            line(c, 810, base - alt, 850, base - alt, 5, NAVY); line(c, 810, base, 850, base, 5, NAVY)
            pop(c, t, 10.9, 650, base - alt - 70, "1 METRO", 70, NAVY, CREME)
        pessoa(c, t, 270, 1300, 1.3, VOCE, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.6)
    else:
        entra(c, t, 12.1, 620, 760, lambda c: mochila(c, 1.4), anim="drop")
        if t > 13.4:
            v = int(10 * ease_out(prog(t, 13.4, 0.6)))
            visor(c, "%d KG" % v, 620, 1140, 480, 130, "BALANÇA")
        pessoa(c, t, 200, 1300, 1.3, VOCE, poses=((0, "hold"), (13.9, "thumb")), exprs=((0, "think"), (13.9, "grin")), look=0.6)


def s03(c, t):  # 14.9 - 20.0  quanto tempo dura, parado na conta?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1100))
    topo(c, "QUANTO TEMPO ELE DURA?")
    linhas = [("Rendimento", "R$ 0,00", VERMELHO)] if t > 18.4 else None
    celular_app(c, t, 690, 720, 1.05, titulo="Saldo", valor="R$ 1.000.000", linhas=linhas, cor=NAVY, t0=18.4, d=0.4)
    if t > 17.1:
        entra(c, t, 17.1, 690, 1150, selo("PARADO NA CONTA", VERMELHO, 52, CREME), anim="stamp")
    consultor_i(c, t, 230, 1300, 1.3, poses=((0, "think"), (17.1, "point_r")), exprs=((0, "think"), (17.1, "neutral")), look=0.6)


def s04(c, t):  # 20.0 - 33.4  gastando 1 mínimo / 5 mil / 20 mil por mês
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "SE VOCÊ GASTAR POR MÊS...", NAVY, CREME)
    linha_conta(c, t, 20.0, 420, "1 salário mínimo", "51 ANOS", 22.7, VERDE)
    linha_conta(c, t, 24.4, 580, "R$ 5 mil", "QUASE 17", 26.3, NAVY)
    linha_conta(c, t, 28.3, 740, "R$ 20 mil (luxo)", "4 ANOS", 31.1, VERMELHO)
    # saldo derretendo conforme o gasto aumenta
    gasto = 0.0 if t < 24.4 else (0.35 if t < 28.3 else 0.9)
    resto = 1 - clamp01(((t - 20.0) % 4.0) / 4.0) * gasto
    rr(c, 160, 880, 760, 70, 20); rgb(c, (0.85, 0.82, 0.76)); c.fill()
    rr(c, 160, 880, 760 * max(resto, 0.04), 70, 20); rgb(c, VERDE); c.fill()
    text(c, "SALDO", 540, 930, 40, MARKER, NAVY)
    pessoa(c, t, 540, 1420, 0.85, VOCE, poses=((0, "stand"), (22.7, "thumb"), (31.1, "head")),
           exprs=((0, "think"), (22.7, "grin"), (26.3, "neutral"), (31.1, "desperate")), look=0.0)


def s05(c, t):  # 33.4 - 36.0  parece pouco? olha a virada
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(520, 1100))
    topo(c, "PARECE POUCO, NÉ?")
    if t > 34.7:
        pop(c, t, 34.8, 520, 420, "OLHA A VIRADA", 100, GOLD)
    consultor_i(c, t, 520, 1300, 1.4, poses=((0, "shrug"), (34.8, "finger_up")), exprs=((0, "think"), (34.8, "confident")), look=0.0)


def s06(c, t):  # 36.0 - 46.7  aplicado a 100% do CDI: quase R$ 9 mil por mês
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    topo(c, "E SE ELE FICASSE APLICADO?")
    if t > 38.3:
        entra(c, t, 38.3, 640, 410, selo("100% DO CDI", NAVY, 64, GOLD), anim="stamp")
    if t > 41.0:
        numero_i(c, "RENDE QUASE", 640, 560, 60, CREME)
        contador(c, t, 41.3, 0, 8900, 640, 700, 130, d=1.2, col=GOLD)
        numero_i(c, "POR MÊS", 640, 820, 64, CREME) if t > 43.0 else None
    if t > 43.9:
        entra(c, t, 43.9, 640, 960, selo("JÁ SEM IMPOSTO", NAVY, 50, CREME), anim="stamp")
    if t > 45.4:
        entra(c, t, 45.4, 640, 1120, selo("E O MILHÃO FICA", GOLD, 50, CREME, rot=0.05), anim="stamp")
    pessoa(c, t, 210, 1300, 1.3, VOCE, poses=((0, "stand"), (41.8, "arms_up")), exprs=((0, "think"), (41.8, "grin")), look=0.6)


def s07(c, t):  # 46.7 - 53.9  a inflação: uns 4 mil ficam rendendo junto
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    topo(c, "SÓ QUE TEM UM DETALHE")
    if t > 47.9:
        entra(c, t, 47.9, 560, 400, selo("A INFLAÇÃO", VERMELHO, 76, CREME), anim="stamp")
    # barra dos R$ 9 mil do mês
    x0, w, y = 160, 760, 560
    rr(c, x0, y, w, 130, 24); rgb(c, VERDE); c.fill()
    text(c, "RENDIMENTO: R$ 9 MIL", x0 + w / 2, y - 30, 46, MARKER, CREME)
    if t > 51.2:
        k = ease_out(prog(t, 51.2, 0.6))
        rr(c, x0, y, w * 0.42 * k, 130, 24); rgb(c, VERMELHO); c.fill()
        if t > 51.6:
            text(c, "R$ 4 MIL", x0 + w * 0.21, y + 85, 54, MARKER, CREME)
            numero_i(c, "FICAM RENDENDO", 540, 790, 60, CREME)
            numero_i(c, "PRO MILHÃO NÃO ENCOLHER", 540, 870, 46, GOLD)
    consultor_i(c, t, 260, 1420, 0.95, poses=((0, "present"), (51.3, "point_r")), exprs=((0, "neutral"), (48.0, "shocked"), (51.3, "confident")), look=0.6)


def s08(c, t):  # 53.9 - 57.3  sobram uns 5 mil por mês, pra sempre
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(540, 1100))
    topo(c, "SOBRAM PRA GASTAR")
    contador(c, t, 54.2, 0, 5000, 540, 470, 160, d=1.0, col=GOLD)
    numero_i(c, "POR MÊS", 540, 610, 70, CREME) if t > 55.2 else None
    if t > 56.4:
        entra(c, t, 56.4, 440, 790, selo("PRA SEMPRE", NAVY, 76, GOLD), anim="stamp")
    pessoa(c, t, 760, 1400, 1.0, VOCE, poses=((0, "thumb"), (56.4, "arms_up")), exprs=((0, "grin"),), look=0.0)


def s09(c, t):  # 57.3 - 61.4  não te deixa rico, te deixa livre
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1150))
    topo(c, "OU SEJA")
    if t > 59.2:
        numero_i(c, "NÃO TE DEIXA", 540, 370, 80, CREME)
        pop(c, t, 59.7, 540, 480, "RICO", 110, CREME, VERMELHO)
    if t > 60.4:
        entra(c, t, 60.4, 540, 630, selo("TE DEIXA LIVRE", VERDE, 84, CREME, rot=-0.04), anim="stamp")
    consultor_i(c, t, 540, 1420, 1.1, poses=((0, "present"), (60.4, "arms_up")), exprs=((0, "neutral"), (60.4, "grin")), look=0.0)


def s10(c, t):  # 61.4 - fim  o que você fazia primeiro?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "COM R$ 1 MILHÃO NO PIX...")
    pop(c, t, 63.6, 560, 380, "O QUE VOCÊ", 96, GOLD) if t > 63.6 else None
    numero_i(c, "FAZIA PRIMEIRO?", 560, 490, 84, GOLD) if t > 64.0 else None
    for i, (t0, s, x, y, cor) in enumerate(((62.0, "CASA?", 700, 650, VERDE), (62.4, "VIAGEM?", 520, 790, BLUE),
                                            (62.8, "CARRO?", 760, 930, PURPLE), (63.2, "INVESTIR?", 560, 1070, NAVY))):
        entra(c, t, t0, x, y, selo(s, cor, 54, CREME, rot=(-0.06 if i % 2 else 0.06)), anim="pop")
    entra(c, t, 65.1, 600, 1220, selo("COMENTA", VERMELHO, 64, CREME), anim="stamp")
    pessoa(c, t, 200, 1330, 1.2, VOCE, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 6.0, s01), (6.0, 14.9, s02), (14.9, 20.0, s03), (20.0, 33.4, s04), (33.4, 36.0, s05),
          (36.0, 46.7, s06), (46.7, 53.9, s07), (53.9, 57.3, s08), (57.3, 61.4, s09), (61.4, 999.0, s10)]
