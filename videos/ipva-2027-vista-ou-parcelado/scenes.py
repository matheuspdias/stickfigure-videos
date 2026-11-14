"""IPVA 2027: à vista com 3% ou parcelado em 5x? (Parte 1 da série IPVA/IPTU). Só TikTok: vertical 1080x1920, ~84,7 s, estilo ilustrado.
Conta útil das 18h (AUTOMATICO_TIKTOK.md 2b.2), sem cartaz de abertura (2b.1): no quadro 0 o boleto já está com o valor caindo.
Narração: Afonso (HeyGen), 1 bloco. Contas em contas.py (carro R$ 50 mil, alíquota 4% em SP, CDI 13,65%, IR 22,5%)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(4.0, "soft_ding"), (31.9, "soft_ding"), (52.0, "tum"), (57.5, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

MOT = "bruno"


def topo(c, s, cor=CREME, contorno=TINTA):
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


def boleto(c, valor, sub="IPVA 2027", s=1.0, cor=NAVY, riscado=None):
    """guia do IPVA (origem = centro)"""
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


def parcela(c, mes, valor="R$ 400", pago=False):
    rr(c, -80, -70, 160, 140, 18); rgb(c, CREME); c.fill()
    rr(c, -80, -70, 160, 46, 18); rgb(c, NAVY); c.fill()
    c.rectangle(-80, -40, 160, 16); rgb(c, NAVY); c.fill()
    numero_i(c, mes, 0, -44, 30, CREME)
    text(c, valor, 0, 40, 38, MARKER, TINTA)
    if pago:
        c.save(); c.translate(48, 50); check_icon(c, 26); c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.9  o IPVA de 2 mil pode sair por 1.940. Ou não.
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(560, 1000))
    topo(c, "IPVA 2027: À VISTA OU 5X?")
    v = 2000 - 60 * ease_io(prog(t, 2.4, 1.8))
    rot = 0.02 * math.sin(t * 2.0)
    entra(c, t, -0.2, 560, 560, lambda c: (c.rotate(rot - 0.03), boleto(c, brl(v), riscado=("R$ 2.000" if t > 3.9 else None), s=1.25)), anim="drop", d=0.6)
    cx = 1350 - 670 * ease_out(prog(t, 0, 1.6))
    c.save(); c.translate(cx, 1290); c.scale(0.9, 0.9); carro_i(c, t, (0.86, 0.26, 0.22)); c.restore()
    if t > 4.0:
        entra(c, t, 4.0, 640, 860, selo("- R$ 60", VERDE, 70, CREME), anim="stamp")
    if t > 5.1:
        entra(c, t, 5.1, 620, 1020, selo("OU NÃO?", VERMELHO, 76, CREME, rot=0.05), anim="stamp")
    consultor_i(c, t, 180, 1300, 1.1, poses=((0, "point_r"), (5.1, "shrug")), exprs=((0, "neutral"), (4.0, "grin"), (5.1, "think")), look=0.6)


def s02(c, t):  # 5.9 - 19.9  calendário de SP saiu: à vista com 3% ou 5x sem juros
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "SP: CALENDÁRIO DO IPVA 2027", NAVY, CREME)
    if t < 10.3:
        c.save(); c.translate(640, 560); c.scale(2.2, 2.2); calendar(c, "JAN", VERMELHO, 56); c.restore()
        if t > 8.6:
            entra(c, t, 8.6, 640, 860, selo("JÁ SAIU", VERDE, 76, CREME), anim="stamp")
    else:
        numero_i(c, "EM JANEIRO, VOCÊ ESCOLHE:", 520, 360, 52, NAVY, contorno=CREME)
        entra(c, t, 12.4, 300, 600, lambda c: cartao_opcao(c, "À VISTA", "- 3%", "de desconto", VERDE, 400, 300), anim="pop")
        entra(c, t, 15.4, 760, 600, lambda c: cartao_opcao(c, "PARCELADO", "5x", "jan a mai", BLUE, 400, 300), anim="pop")
        if t > 18.9:
            entra(c, t, 18.9, 760, 830, selo("SEM JUROS", NAVY, 50, GOLD), anim="stamp")
    consultor_i(c, t, 200, 1330, 1.15, poses=((0, "present"), (12.4, "point_ru"), (15.4, "point_r")),
                exprs=((0, "neutral"), (10.4, "confident")), look=0.0)


def s03(c, t):  # 19.9 - 27.0  carro de 50 mil: IPVA 4% = 2 mil
    luz("dia")
    cena_rua(c, t, hora="dia", carros=False)
    rr(c, 90, 180, 900, 110, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "BORA FAZER A CONTA", 540, 235, 58, CREME)
    c.save(); c.translate(560, 1260); c.scale(1.5, 1.5); carro_i(c, t, (0.86, 0.26, 0.22)); c.restore()
    if t > 21.6:
        entra(c, t, 21.6, 450, 760, lambda c: etiqueta_preco(c, "R$ 50 MIL", GOLD, 70), anim="drop")
    if t > 23.6:
        entra(c, t, 23.6, 540, 450, selo("IPVA: 4%", VERMELHO, 70, CREME), anim="stamp")
    if t > 25.2:
        rr(c, 260, 520, 560, 150, 26); rgb(c, CREME); c.fill()
        contador(c, t, 25.2, 0, 2000, 540, 600, 110, d=0.9, col=VERMELHO)
    pessoa(c, t, 160, 1330, 1.1, MOT, poses=((0, "stand"), (23.6, "think")), exprs=((0, "neutral"), (25.2, "shocked")), look=0.6)


def s04(c, t):  # 27.0 - 33.0  à vista: 1.940, economiza 60
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(240, 1100))
    topo(c, "À VISTA, EM JANEIRO")
    c.save(); c.translate(620, 560); c.rotate(-0.03)
    boleto(c, "R$ 1.940" if t > 28.6 else "R$ 2.000", riscado=("R$ 2.000" if t > 28.6 else None), cor=VERDE)
    c.restore()
    if t > 30.4:
        numero_i(c, "ECONOMIZA", 620, 860, 60, CREME)
        contador(c, t, 30.9, 0, 60, 620, 990, 150, d=0.8, col=GOLD)
    pessoa(c, t, 210, 1300, 1.25, MOT, poses=((0, "stand"), (31.9, "thumb")), exprs=((0, "think"), (31.9, "grin")), look=0.6)


def s05(c, t):  # 33.0 - 40.6  parcelado: 5 de 400; "deixo rendendo e pago aos poucos"
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "PARCELADO", NAVY, CREME)
    for i, m in enumerate(("JAN", "FEV", "MAR", "ABR", "MAI")):
        ti = 33.2 + i * 0.3
        x = 160 + i * 190
        entra(c, t, ti, x, 430, lambda c, m=m: parcela(c, m), anim="drop")
    if t > 35.6:
        # balão de pensamento do motorista
        rr(c, 380, 640, 560, 230, 40); rgb(c, (1, 1, 1)); c.fill()
        for (bx, by, br) in ((420, 900, 22), (380, 945, 14)):
            c.new_sub_path(); c.arc(bx, by, br, 0, 6.283); rgb(c, (1, 1, 1)); c.fill()
        text(c, "DEIXO O DINHEIRO", 660, 725, 46, MARKER, NAVY)
        text(c, "RENDENDO E PAGO", 660, 785, 46, MARKER, NAVY) if t > 37.4 else None
        text(c, "AOS POUCOS", 660, 845, 46, MARKER, VERDE) if t > 38.4 else None
    pessoa(c, t, 260, 1330, 1.25, MOT, poses=((0, "stand"), (35.6, "think")), exprs=((0, "neutral"), (35.6, "confident")), look=0.6)


def s06(c, t):  # 40.6 - 49.6  testando: rendimento até maio ~ R$ 34
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    topo(c, "BORA TESTAR")
    linhas = [("Fevereiro", "+ R$ 13", VERDE), ("Março", "+ R$ 10", VERDE),
              ("Abril", "+ R$ 7", VERDE), ("Maio", "+ R$ 4", VERDE)]
    celular_app(c, t, 680, 720, 1.15, titulo="100% do CDI (já sem IR)", valor="R$ 1.600",
                linhas=linhas if t > 43.5 else None, cor=VERDE, t0=43.5, d=2.0) if t > 41.2 else None
    if t > 46.8:
        rr(c, 380, 1060, 600, 150, 26); rgb(c, CREME); c.fill()
        text(c, "ATÉ MAIO:", 680, 1105, 40, MARKER, NAVY)
        contador(c, t, 46.9, 0, 34, 680, 1170, 80, d=1.0, col=VERDE, prefixo="uns R$ ")
    consultor_i(c, t, 210, 1300, 1.2, poses=((0, "present"), (43.5, "hold")), prop=("r", prop_calc_i),
                exprs=((0, "neutral"), (46.8, "think")), look=0.6)


def s07(c, t):  # 49.6 - 57.4  60 x 34: o desconto ganha; juro embutido de 1,5% ao mês
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "60 CONTRA 34", NAVY, CREME)
    barras_i(c, t, 49.7, 320, 900, w=600, h=480, dados=(("Desconto", 60, VERDE), ("Rendimento", 34, BLUE)),
             fmt=lambda v: brl(v), d=1.0, intervalo=0.6)
    if t > 51.9:
        entra(c, t, 51.9, 590, 1080, selo("O DESCONTO GANHA", VERDE, 54, CREME), anim="stamp")
    if t > 54.6:
        rr(c, 200, 1180, 760, 120, 24); rgb(c, NAVY); c.fill()
        text(c, "PARCELADO EMBUTE ~1,5% AO MÊS", 580, 1258, 40, MARKER, GOLD)
    consultor_i(c, t, 120, 1420, 0.75, poses=((0, "point_r"), (51.9, "thumb")), exprs=((0, "neutral"), (51.9, "grin")), look=0.6)


def s08(c, t):  # 57.4 - 62.3  a virada: só vale se o dinheiro já estiver guardado
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(520, 1100))
    topo(c, "MAS TEM A VIRADA")
    if t > 58.6:
        pop(c, t, 58.6, 520, 400, "SÓ VALE SE O DINHEIRO", 62, CREME)
    if t > 60.6:
        entra(c, t, 60.6, 520, 520, selo("JÁ ESTIVER GUARDADO", GOLD, 64, TINTA, rot=0.04), anim="stamp")
    consultor_i(c, t, 520, 1330, 1.35, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)


def s09(c, t):  # 62.3 - 73.5  cheque especial ou cartão atrasado: parcela sem medo
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    topo(c, "PEGAR EMPRESTADO PRA PAGAR?")
    if t > 64.2:
        entra(c, t, 64.2, 420, 450, selo("CHEQUE ESPECIAL", VERMELHO, 50, CREME), anim="stamp")
    if t > 65.9:
        entra(c, t, 65.9, 700, 580, selo("CARTÃO ATRASADO", VERMELHO, 50, CREME, rot=0.05), anim="stamp")
    if t > 67.2 and t < 69.0:
        entra(c, t, 67.2, 620, 800, selo("PARCELA SEM MEDO", VERDE, 54, CREME), anim="stamp")
    if t >= 69.0:
        # o desconto de R$ 60 sendo comido pelos juros, dia a dia
        k = ease_io(prog(t, 69.4, 2.6))
        dia = int(1 + 11 * k)
        rr(c, 380, 760, 560, 80, 22); rgb(c, (0.85, 0.82, 0.76)); c.fill()
        rr(c, 380, 760, 560 * max(0.02, 1 - k), 80, 22); rgb(c, VERDE); c.fill()
        text(c, "DESCONTO: R$ %d" % round(60 * (1 - k)), 660, 815, 44, MARKER, NAVY)
        numero_i(c, "DIA %d" % dia, 660, 940, 84, GOLD)
        if t > 70.8:
            entra(c, t, 70.8, 640, 1100, selo("< 2 SEMANAS", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 200, 1300, 1.2, poses=((0, "stand"), (64.2, "head"), (67.2, "point_r")),
                exprs=((0, "think"), (64.2, "desperate"), (67.2, "confident"), (69.2, "shocked")), look=0.6)


def s10(c, t):  # 73.5 - 79.1  resumo
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "RESUMINDO", NAVY, CREME)
    if t > 73.7:
        rr(c, 120, 340, 840, 210, 26); rgb(c, CREME); c.fill(); rr(c, 120, 340, 840, 210, 26); rgb(c, VERDE); c.set_line_width(8); c.stroke()
        text(c, "TEM GUARDADO?", 540, 410, 50, MARKER, TINTA)
        pop(c, t, 75.0, 540, 490, "À VISTA", 70, VERDE, TINTA)
    if t > 75.8:
        rr(c, 120, 590, 840, 210, 26); rgb(c, CREME); c.fill(); rr(c, 120, 590, 840, 210, 26); rgb(c, BLUE); c.set_line_width(8); c.stroke()
        text(c, "NÃO TEM?", 540, 660, 50, MARKER, TINTA)
        pop(c, t, 76.5, 540, 740, "PARCELA", 70, BLUE, TINTA)
    if t > 77.4:
        entra(c, t, 77.4, 540, 900, selo("E NÃO PEGA EMPRÉSTIMO", VERMELHO, 48, CREME), anim="stamp")
    consultor_i(c, t, 540, 1420, 0.9, poses=((0, "present"), (77.4, "finger_up")), exprs=((0, "confident"),), look=0.0)


def s11(c, t):  # 79.1 - fim  Parte 2: IPTU. À vista ou parcelado?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1150))
    topo(c, "IPVA 2027 (PARTE 1)")
    entra(c, t, 79.2, 620, 400, selo("PARTE 2: O IPTU", GOLD, 64, TINTA), anim="stamp")
    if t > 81.2:
        pop(c, t, 81.2, 620, 600, "E VOCÊ?", 90, CREME)
        entra(c, t, 81.9, 470, 760, selo("À VISTA?", VERDE, 60, CREME, rot=0.05), anim="pop")
        entra(c, t, 82.6, 760, 900, selo("PARCELADO?", BLUE, 60, CREME), anim="pop")
    if t > 83.9:
        entra(c, t, 83.9, 620, 1100, selo("COMENTA", VERMELHO, 64, CREME), anim="stamp")
    consultor_i(c, t, 190, 1300, 1.15, poses=((0, "point_r"), (81.2, "think")), exprs=((0, "neutral"), (81.2, "think")), look=0.6)


SCENES = [(0, 5.9, s01), (5.9, 19.9, s02), (19.9, 27.0, s03), (27.0, 33.0, s04), (33.0, 40.6, s05),
          (40.6, 49.6, s06), (49.6, 57.4, s07), (57.4, 62.3, s08), (62.3, 73.5, s09), (73.5, 79.1, s10),
          (79.1, 999.0, s11)]
