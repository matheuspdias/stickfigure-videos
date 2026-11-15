"""IPTU 2027: à vista ou em 10x? (Parte 2 da série IPVA/IPTU). Só TikTok: vertical 1080x1920, ~89,3 s, estilo ilustrado.
Conta útil das 18h, sem cartaz de abertura (2b.1): no quadro 0 a guia do IPTU já está se dividindo em parcelas.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (IPTU R$ 1.500; 3% à vista; 10x; CDI 13,65% a.a., IR 22,5%)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(4.9, "soft_ding"), (36.0, "soft_ding"), (55.2, "tum"), (76.5, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

DONA = "ana"
MESES = ("FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV")


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


def boleto(c, valor, sub="IPTU 2027", s=1.0, cor=NAVY, riscado=None):
    """guia do IPTU (origem = centro)"""
    c.save(); c.scale(s, s)
    papel(c, 520, 330)
    c.rectangle(-260, -165, 520, 80); rgb(c, cor); c.fill()
    c.select_font_face(MARKER); c.set_font_size(40); c.move_to(-230, -110); rgb(c, (1, 1, 1)); c.show_text(sub)
    for i in range(3):
        c.rectangle(-220, -50 + i * 34, 220 - i * 50, 10); rgb(c, (0.82, 0.82, 0.84)); c.fill()
    if riscado:
        c.select_font_face(MARKER); c.set_font_size(40)
        ww = c.text_extents(riscado).x_advance
        c.move_to(220 - ww, -20); rgb(c, (0.5, 0.5, 0.55)); c.show_text(riscado)
        c.rectangle(216 - ww, -34, ww + 8, 5); rgb(c, VERMELHO); c.fill()
    c.select_font_face(MARKER); c.set_font_size(76)
    ww = c.text_extents(valor).x_advance
    c.move_to(220 - ww, 70); rgb(c, TINTA); c.show_text(valor)
    for i in range(30):
        c.rectangle(-220 + i * 14, 105, 6 if i % 3 else 10, 40); rgb(c, TINTA); c.fill()
    c.restore()


def cartao_opcao(c, titulo, linha1, linha2, cor, w=420, h=330):
    rr(c, -w / 2 + 8, -h / 2 + 10, w, h, 28); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, -w / 2, -h / 2, w, h, 28); rgb(c, CREME); c.fill()
    rr(c, -w / 2, -h / 2, w, 90, 28); rgb(c, cor); c.fill()
    c.rectangle(-w / 2, -h / 2 + 50, w, 40); rgb(c, cor); c.fill()
    numero_i(c, titulo, 0, -h / 2 + 48, 50, CREME)
    numero_i(c, linha1, 0, 30, 76, cor, contorno=TINTA)
    text(c, linha2, 0, 115, 38, MARKER, TINTA)


def parcela(c, mes, valor="R$ 150", pago=False, s=1.0):
    c.save(); c.scale(s, s)
    rr(c, -80, -70, 160, 140, 18); rgb(c, CREME); c.fill()
    rr(c, -80, -70, 160, 46, 18); rgb(c, NAVY); c.fill()
    c.rectangle(-80, -40, 160, 16); rgb(c, NAVY); c.fill()
    numero_i(c, mes, 0, -44, 30, CREME)
    text(c, valor, 0, 40, 38, MARKER, TINTA)
    if pago:
        c.save(); c.translate(48, 50); check_icon(c, 26); c.restore()
    c.restore()


def grade_parcelas(c, t, t0, x0=200, y0=520, s=0.85, d=0.18, pagas=0, valor="R$ 150"):
    """10 parcelas (fev a nov) em 2 linhas de 5"""
    for i, m in enumerate(MESES):
        ti = t0 + i * d
        if t < ti:
            break
        x = x0 + (i % 5) * 150 * s / 0.85; y = y0 + (i // 5) * 150 * s / 0.85
        entra(c, t, ti, x, y, lambda c, m=m, i=i: parcela(c, m, valor, i < pagas, s), anim="pop", d=0.3)


def casa_i(c, s=1.0):
    """casinha simples (origem = base no centro)"""
    c.save(); c.scale(s, s)
    rr(c, -150, -230, 300, 230, 6); rgb(c, (0.96, 0.90, 0.78)); c.fill()
    pg(c, [(-185, -220), (0, -360), (185, -220)]); rgb(c, VERMELHO); c.fill()
    rr(c, -40, -130, 80, 130, 6); rgb(c, (0.55, 0.38, 0.24)); c.fill()
    for x in (-110, 70):
        rr(c, x, -190, 50, 50, 4); rgb(c, (0.62, 0.80, 0.92)); c.fill()
    c.rectangle(-150, -4, 300, 8); rgb(c, TINTA); c.fill()
    c.restore()


def balanca(c, t, x, y, inc, esq, dir_, cor_e=VERDE, cor_d=BLUE):
    """balança: inc > 0 pesa à direita"""
    c.save(); c.translate(x, y)
    rr(c, -14, 0, 28, 300, 8); rgb(c, TINTA); c.fill()
    rr(c, -110, 290, 220, 30, 10); rgb(c, TINTA); c.fill()
    c.rotate(inc)
    rr(c, -330, -12, 660, 24, 10); rgb(c, dk(GOLD, 0.2)); c.fill()
    for sx, lab, cor in ((-1, esq, cor_e), (1, dir_, cor_d)):
        c.save(); c.translate(sx * 300, 0); c.rotate(-inc)
        line(c, 0, 0, -80, 140, 4, TINTA); line(c, 0, 0, 80, 140, 4, TINTA)
        pg(c, [(-120, 140), (120, 140), (90, 175), (-90, 175)]); rgb(c, cor); c.fill()
        numero_i(c, lab, 0, 100, 46, CREME)
        c.restore()
    c.new_sub_path(); c.arc(0, 0, 22, 0, 6.283); rgb(c, GOLD); c.fill()
    c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 7.4  parcelar em 10x pode sair mais barato. parece errado? bora fazer a conta
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(200, 1100))
    topo(c, "IPTU 2027: À VISTA OU 10X?")
    # quadro 0: a guia já está se dividindo em 10 parcelas
    if t < 2.2:
        rot = 0.02 * math.sin(t * 3.0)
        c.save(); c.translate(560, 560); c.rotate(rot - 0.03)
        c.scale(1.1 - 0.3 * clamp01(t / 2.2), 1.1 - 0.3 * clamp01(t / 2.2)); boleto(c, "R$ 1.500"); c.restore()
    grade_parcelas(c, t, 0.6, x0=420, y0=870 if t < 2.2 else 500, s=0.65, d=0.12)
    if t > 3.0:
        entra(c, t, 3.0, 600, 850, selo("MAIS BARATO?", VERDE, 68, CREME), anim="stamp")
    if t > 4.9:
        entra(c, t, 4.9, 600, 1010, selo("PARECE ERRADO", VERMELHO, 60, CREME, rot=0.05), anim="stamp")
    consultor_i(c, t, 170, 1300, 1.1, poses=((0, "point_r"), (4.9, "shrug"), (6.3, "hold")), prop=("r", prop_calc_i) if t > 6.3 else None,
                exprs=((0, "neutral"), (4.9, "think"), (6.3, "confident")), look=0.6)


def s02(c, t):  # 7.4 - 12.4  na Parte 1 (IPVA) o à vista ganhou; agora o IPTU
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "NA PARTE 1...", NAVY, CREME)
    c.save(); c.translate(330, 640); c.scale(0.8, 0.8); carro_i(c, t, (0.86, 0.26, 0.22)); c.restore()
    entra(c, t, 8.5, 330, 420, selo("IPVA", NAVY, 64, GOLD), anim="pop")
    if t > 10.0:
        entra(c, t, 10.0, 330, 790, selo("À VISTA GANHOU", VERDE, 46, CREME), anim="stamp")
    if t > 10.9:
        entra(c, t, 10.9, 760, 760, lambda c: casa_i(c, 0.9), anim="drop")
        entra(c, t, 11.6, 760, 420, selo("IPTU?", VERMELHO, 70, CREME, rot=0.05), anim="stamp")
    pessoa(c, t, 560, 1400, 0.95, DONA, poses=((0, "stand"), (10.9, "point_r")), exprs=((0, "neutral"), (10.9, "think")), look=0.6)


def s03(c, t):  # 12.4 - 22.6  SP 2026: 3% à vista em fevereiro ou até 10x sem juros (fev a nov)
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "SÃO PAULO, REGRA DE 2026", NAVY, CREME)
    if t < 15.8:
        c.save(); c.translate(540, 560); c.scale(2.0, 2.0); calendar(c, "2026", NAVY, 44); c.restore()
        entra(c, t, 12.6, 540, 800, selo("CIDADE DE SP", VERMELHO, 56, CREME), anim="stamp")
    entra(c, t, 15.8, 300, 520, lambda c: cartao_opcao(c, "À VISTA", "- 3%", "em fevereiro", VERDE, 400, 300), anim="pop")
    entra(c, t, 19.2, 760, 520, lambda c: cartao_opcao(c, "PARCELADO", "ATÉ 10x", "sem juros", BLUE, 400, 300), anim="pop")
    if t > 21.1:
        for i, m in enumerate(MESES):
            ti = 21.1 + i * 0.07
            if t > ti:
                entra(c, t, ti, 120 + i * 92, 770, lambda c, m=m: (rr(c, -42, -30, 84, 60, 12), rgb(c, BLUE), c.fill(),
                      numero_i(c, m, 0, 2, 26, CREME)), anim="pop", d=0.25)
        text(c, "fevereiro a novembro", 540, 860, 40, HAND, NAVY)
    consultor_i(c, t, 540, 1460, 0.95, poses=((0, "present"), (15.8, "point_l"), (19.2, "point_r")),
                exprs=((0, "neutral"), (15.8, "confident")), look=0.0)


def s04(c, t):  # 22.6 - 28.4  o calendário de 2027 ainda vai sair (costuma seguir o mesmo modelo)
    luz("dia")
    cena_rua(c, t, hora="dia", carros=False)
    rr(c, 90, 180, 900, 110, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "E EM 2027?", 540, 235, 58, CREME)
    entra(c, t, 22.8, 620, 470, lambda c: notificacao(c, 0, 0, 1.0, titulo="Calendário IPTU 2027", texto="a prefeitura ainda vai divulgar",
                                                     cor=NAVY, app="PREFEITURA"), anim="drop")
    c.save(); c.translate(780, 1290); casa_i(c, 1.1); c.restore()
    if t > 26.3:
        entra(c, t, 26.3, 600, 700, selo("COSTUMA REPETIR", GOLD, 54, TINTA, rot=0.04), anim="stamp")
    pessoa(c, t, 280, 1330, 1.25, DONA, poses=((0, "stand"), (24.3, "hold")), prop=("r", prop_celular_i),
           exprs=((0, "think"), (26.3, "neutral")), look=0.6)


def s05(c, t):  # 28.4 - 37.5  IPTU de R$ 1.500: à vista R$ 1.455, economiza R$ 45
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    topo(c, "IPTU DE R$ 1.500")
    v = 1500 - 45 * ease_io(prog(t, 32.6, 1.6))
    c.save(); c.translate(620, 560); c.rotate(-0.03)
    boleto(c, brl(v), sub="À VISTA", riscado=("R$ 1.500" if t > 32.8 else None), cor=VERDE)
    c.restore()
    if t > 35.4:
        numero_i(c, "ECONOMIZA", 620, 860, 60, CREME)
        contador(c, t, 35.9, 0, 45, 620, 990, 150, d=0.8, col=GOLD)
    pessoa(c, t, 200, 1300, 1.25, DONA, poses=((0, "stand"), (36.0, "thumb")), exprs=((0, "think"), (36.0, "grin")), look=0.6)


def s06(c, t):  # 37.5 - 40.4  parcelado: 10 de 150
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1200))
    topo(c, "PARCELADO")
    numero_i(c, "10 x R$ 150", 540, 400, 110, GOLD) if t > 38.6 else None
    grade_parcelas(c, t, 37.7, x0=230, y0=600, s=0.85, d=0.12)
    consultor_i(c, t, 540, 1330, 1.1, poses=((0, "present"),), exprs=((0, "neutral"),), look=0.0)


def s07(c, t):  # 40.4 - 52.2  virada: deixa rendendo 100% do CDI e tira só a parcela -> ~R$ 58 até novembro
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(200, 1150))
    topo(c, "AGORA, A VIRADA")
    k = prog(t, 47.0, 4.4)
    saldo = 1350 * (1 - k) + 58 * k
    celular_app(c, t, 680, 640, 1.0, titulo="Rendendo 100% do CDI", valor=brl(saldo) if t > 42.5 else "R$ 1.350",
                sub="sai R$ 150 por mês", cor=NAVY,
                linhas=[("Parcela " + m, "- R$ 150", VERMELHO) for m in MESES[:min(5, int(k * 9) + 1)]] if t > 47.0 else None)
    if t > 49.4:
        rr(c, 380, 1030, 600, 150, 24); rgb(c, CREME); c.fill()
        text(c, "RENDIMENTO ATÉ NOVEMBRO", 680, 1075, 34, MARKER, NAVY)
        contador(c, t, 49.6, 0, 58, 680, 1140, 80, d=1.6, col=VERDE, prefixo="+ R$ ")
    consultor_i(c, t, 180, 1300, 1.15, poses=((0, "finger_up"), (42.5, "point_r"), (49.6, "thumb")),
                exprs=((0, "confident"), (42.5, "neutral"), (49.6, "grin")), look=0.6)


def s08(c, t):  # 52.2 - 56.4  58 contra 45: parcelar ganha
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "58 CONTRA 45")
    inc = 0.14 * ease_out(prog(t, 52.6, 1.2))
    balanca(c, t, 540, 560, inc, "R$ 45", "R$ 58", VERDE, BLUE)
    text(c, "desconto à vista", 240, 760, 36, HAND, CREME)
    text(c, "rende parcelando", 840, 850, 36, HAND, CREME)
    if t > 55.2:
        entra(c, t, 55.2, 540, 950, selo("AQUI, PARCELAR GANHA", GOLD, 58, TINTA, rot=0.03), anim="stamp")
    consultor_i(c, t, 540, 1500, 0.85, poses=((0, "point_r"), (55.2, "arms_up")), exprs=((0, "neutral"), (55.2, "grin")), look=0.3)


def s09(c, t):  # 56.4 - 70.1  por quê? IPVA 5x (juro 1,5%/mês) x IPTU 10x (0,68%/mês) < rendimento 0,83%/mês
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "POR QUÊ?", NAVY, CREME)

    def linha(y, nome, sub, val, cor, t0):
        if t < t0:
            return
        k = ease_out(clamp01((t - t0) / 0.35)); x = 540 - 600 * (1 - k)
        rr(c, x - 420, y - 80, 840, 160, 24); rgb(c, CREME); c.fill()
        rr(c, x - 420, y - 80, 840, 160, 24); rgb(c, cor); c.set_line_width(6); c.stroke()
        text(c, nome, x - 390, y - 10, 50, MARKER, TINTA, align="l")
        text(c, sub, x - 390, y + 46, 34, HAND, TINTA, align="l")
        if val:
            text(c, val, x + 390, y + 20, 56, MARKER, cor, align="r")
    linha(420, "IPVA: 5x", "juro escondido", "1,5%/mês" if t > 58.0 else None, VERMELHO, 57.1)
    linha(610, "IPTU: 10x", "mais tempo rendendo", "0,68%/mês" if t > 65.6 else None, BLUE, 59.5)
    linha(800, "INVESTIMENTO", "100% do CDI, sem IR", "0,83%/mês" if t > 68.0 else None, VERDE, 67.9)
    if t > 68.7:
        entra(c, t, 68.7, 540, 950, selo("RENDE MAIS QUE O JURO", VERDE, 48, CREME), anim="stamp")
    consultor_i(c, t, 540, 1480, 0.9, poses=((0, "think"), (59.5, "point_ru"), (68.0, "thumb")), prop=("l", prop_calc_i),
                exprs=((0, "think"), (63.1, "neutral"), (68.0, "grin")), look=0.6)


def s10(c, t):  # 70.1 - 78.3  atenção: só vale se o dinheiro ficar guardado; senão, paga à vista
    luz("tarde")
    cena_sala(c, t, hora="tarde")
    rr(c, 90, 180, 900, 110, 24); rgb(c, VERMELHO, 0.92); c.fill()
    numero_i(c, "MAS ATENÇÃO", 540, 235, 58, CREME)
    if t > 71.4:
        entra(c, t, 71.4, 600, 430, selo("SÓ SE FICAR GUARDADO", NAVY, 50, GOLD), anim="stamp")
    if t > 74.6:
        entra(c, t, 74.6, 620, 640, lambda c: notificacao(c, 0, 0, 0.9, titulo="Pix enviado: - R$ 600",
                                                         texto="saldo do IPTU: R$ 750", cor=VERMELHO, app="BANCO"), anim="drop")
    if t > 76.5:
        entra(c, t, 76.5, 660, 880, selo("PAGA À VISTA", VERDE, 70, CREME, rot=0.04), anim="stamp")
    pessoa(c, t, 220, 1360, 1.2, DONA, poses=((0, "stand"), (74.6, "hold"), (76.5, "thumb")), prop=("r", prop_celular_i) if t < 76.5 else None,
           exprs=((0, "neutral"), (74.6, "shocked"), (76.5, "confident")), look=0.6)


def s11(c, t):  # 78.3 - 85.0  a regra serve pra qualquer conta: compara o desconto com o que o dinheiro renderia
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "A REGRA PRA QUALQUER CONTA")
    inc = 0.10 * math.sin((t - 78.3) * 1.6)
    balanca(c, t, 540, 560, inc, "DESCONTO", "RENDE", GOLD, VERDE)
    if t > 82.0:
        entra(c, t, 82.0, 540, 930, selo("COMPARA OS DOIS", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 540, 1500, 0.85, poses=((0, "present"), (82.0, "finger_up")), exprs=((0, "neutral"), (82.0, "confident")), look=0.0)


def s12(c, t):  # 85.0 - fim  e você: à vista ou em 10x? comenta
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "E VOCÊ?")
    entra(c, t, 85.6, 290, 520, lambda c: cartao_opcao(c, "À VISTA", "- 3%", "paga tudo", VERDE, 360, 280), anim="left")
    if t > 86.9:
        pop(c, t, 87.0, 540, 710, "OU", 80, GOLD)
    entra(c, t, 87.3, 770, 520, lambda c: cartao_opcao(c, "EM 10x", "R$ 150", "e deixa rendendo", BLUE, 360, 280), anim="right")
    entra(c, t, 88.4, 540, 860, selo("COMENTA", GOLD, 72, TINTA), anim="stamp")
    pessoa(c, t, 250, 1400, 0.95, DONA, poses=((0, "think"),), exprs=((0, "think"),), look=0.5)
    consultor_i(c, t, 800, 1400, 0.95, poses=((0, "present"),), exprs=((0, "grin"),), look=-0.5)


SCENES = [(0, 7.4, s01), (7.4, 12.4, s02), (12.4, 22.6, s03), (22.6, 28.4, s04), (28.4, 37.5, s05),
          (37.5, 40.4, s06), (40.4, 52.2, s07), (52.2, 56.4, s08), (56.4, 70.1, s09), (70.1, 78.3, s10),
          (78.3, 85.0, s11), (85.0, 999.0, s12)]
