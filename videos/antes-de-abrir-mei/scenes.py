"""O que ninguém te conta antes de abrir MEI (série ep. 6). Só TikTok: vertical nativo 1080x1920, ~110,6 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Contas e fontes em contas.py: DAS 2026 R$ 82,05 / 86,05 / 87,05 (5% de R$ 1.621 + ICMS/ISS);
teto R$ 81 mil (R$ 6.750/mês); excesso até 20% = R$ 97.200."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(6.2, "tum"), (19.3, "tum"), (47.0, "tum"), (58.3, "tum"), (74.1, "tum"), (83.1, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers
def selo(s, cor=VERMELHO, size=64, tcol=CREME, rot=-0.06):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(rot)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def topico(n, s, cor=GOLD, size=70):
    """número do tópico (círculo) + título"""
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance
        x0 = -(w + 130) / 2
        c.new_sub_path(); c.arc(x0 + 50, 0, 52, 0, 6.283); rgb(c, cor); c.fill()
        numero_i(c, n, x0 + 50, 0, 64, NAVY, contorno=CREME)
        numero_i(c, s, x0 + 130, 0, size, CREME, alinhamento="l")
    return f


def selo_serie(c):
    rr(c, -440, -100, 880, 200, 30); rgb(c, NAVY); c.fill()
    rr(c, -440, -100, 880, 200, 30); rgb(c, GOLD); c.set_line_width(6); c.stroke()
    numero_i(c, "SÉRIE", -390, -40, 46, GOLD, alinhamento="l")
    numero_i(c, "O que ninguém te conta", -390, 30, 50, CREME, alinhamento="l")
    rr(c, 220, -76, 180, 66, 14); rgb(c, GOLD); c.fill()
    numero_i(c, "EP. 6", 310, -43, 46, NAVY, contorno=CREME)


def cartao(lab, val="", cor_val=TINTA, w=600, h=100, size=44):
    def f(c):
        rr(c, -w / 2 + 6, -h / 2 + 8, w, h, 22); rgb(c, (0, 0, 0), 0.20); c.fill()
        rr(c, -w / 2, -h / 2, w, h, 22); rgb(c, (0.99, 0.99, 0.98)); c.fill()
        text(c, lab, -w / 2 + 28, 2, size, HAND, (0.2, 0.2, 0.25), align="l")
        if val:
            text(c, val, w / 2 - 24, 2, 50, MARKER, cor_val, align="r")
    return f


def item(s, ok=True, w=600, size=42):
    def f(c):
        rr(c, -w / 2 + 6, -48 + 8, w, 96, 22); rgb(c, (0, 0, 0), 0.18); c.fill()
        rr(c, -w / 2, -48, w, 96, 22); rgb(c, (0.99, 0.99, 0.98)); c.fill()
        c.save(); c.translate(-w / 2 + 50, 0)
        if ok:
            check_icon(c, 28)
        else:
            x_icon(c, 28)
        c.restore()
        text(c, s, -w / 2 + 96, 2, size, HAND, (0.2, 0.2, 0.25), align="l")
    return f


def boleto(c, t, t0=None):
    """boleto do DAS"""
    c.save(); papel(c, 420, 300, rot=-0.03)
    text(c, "DAS - MEI", -180, -100, 44, MARKER, NAVY, align="l")
    for i in range(3):
        line(c, -180, -40 + i * 34, 120 - i * 60, -40 + i * 34, 8, (0.80, 0.80, 0.80))
    for i in range(28):
        c.rectangle(-180 + i * 13, 70, 7 if i % 3 else 4, 60); rgb(c, TINTA); c.fill()
    c.restore()


def tela_cnpj(c):
    """celular com 'CNPJ criado!'"""
    rr(c, -150 + 10, -270 + 14, 300, 540, 40); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, -150, -270, 300, 540, 40); rgb(c, (0.10, 0.10, 0.12)); c.fill()
    rr(c, -134, -252, 268, 504, 30); rgb(c, CREME); c.fill()
    c.save(); c.translate(0, -80); check_icon(c, 60); c.restore()
    numero_i(c, "CNPJ", 0, 40, 60, NAVY, contorno=CREME)
    numero_i(c, "CRIADO!", 0, 110, 52, VERDE, contorno=CREME)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.1  gancho + selo da série
    fundo_marca(c, t, "navy", holofote=(260, 1000))
    numero_i(c, "ABRIR MEI LEVA", 520, 240, 96, CREME)
    numero_i(c, "5 MINUTOS", 520, 370, 130, GOLD)
    if t < 4.2:
        entra(c, t, 0.2, 760, 860, tela_cnpj, anim="pop")
    entra(c, t, 3.4, 520, 520, selo("ANTES DE ABRIR, SAIBA", VERMELHO, 50, CREME), anim="stamp")
    consultor_i(c, t, 250, 1300, 1.35, poses=((0, "point_r"), (3.4, "finger_up")), exprs=((0, "happy"), (3.4, "worried")), look=0.7)
    if 4.2 <= t < 6.1:
        entra(c, t, 4.2, 580, 1110, lambda c: (c.scale(0.8, 0.8), selo_serie(c)), anim="stamp", t1=5.9)


def s02(c, t):  # 6.1 - 19.2  1. o DAS
    cena_escritorio(c, t, "dia")
    entra(c, t, 6.2, 520, 240, topico("1", "O BOLETO: DAS"), anim="stamp")
    entra(c, t, 7.1, 690, 470, lambda c: boleto(c, t), anim="drop")
    if t < 17.0:
        entra(c, t, 10.9, 640, 700, cartao("Comércio", "R$ 82,05", NAVY, 560), anim="right")
        entra(c, t, 11.5, 640, 810, cartao("Serviços", "R$ 86,05", NAVY, 560), anim="right")
        entra(c, t, 12.0, 640, 920, cartao("Os dois", "R$ 87,05", NAVY, 560), anim="right")
        entra(c, t, 14.1, 620, 1060, selo("MESMO SEM VENDER NADA", VERMELHO, 42, CREME), anim="stamp")
    else:
        numero_i(c, "EM 1 ANO, UNS", 640, 760, 60, CREME)
        contador(c, t, 17.6, 0, 1000, 640, 880, 130, d=0.7, col=GOLD)
    consultor_i(c, t, 190, 1300, 1.2, poses=((0, "present"), (14.1, "shrug")), exprs=((0, "neutral"), (14.1, "worried")), look=0.8)


def s03(c, t):  # 19.2 - 30.2  2. o teto
    fundo_marca(c, t, "navy", holofote=(220, 1100))
    entra(c, t, 19.3, 520, 240, topico("2", "O TETO"), anim="stamp")
    contador(c, t, 22.0, 0, 81000, 600, 420, 130, d=1.0, col=GOLD)
    if t > 23.4:
        numero_i(c, "POR ANO", 600, 530, 60, CREME)
    entra(c, t, 24.3, 620, 680, cartao("Faturamento = tudo que entra", "", TINTA, 600, 100, 40), anim="right")
    entra(c, t, 26.3, 620, 810, selo("NÃO É O LUCRO", VERMELHO, 56, CREME), anim="stamp")
    if t > 27.4:
        numero_i(c, "≈ R$ 6.750", 620, 960, 100, GOLD)
        numero_i(c, "POR MÊS", 620, 1060, 54, CREME)
    consultor_i(c, t, 180, 1300, 1.2, poses=((0, "finger_up"), (26.3, "point_r")), exprs=((0, "confident"), (26.3, "think")), look=0.6)


def s04(c, t):  # 30.2 - 46.8  passou do teto
    fundo_marca(c, t, "creme")
    if t < 39.8:
        numero_i(c, "PASSOU ATÉ 20%?", 520, 230, 96, NAVY, contorno=CREME)
        entra(c, t, 32.9, 520, 360, selo("ATÉ R$ 97.200", GOLD, 60, NAVY), anim="stamp")
        entra(c, t, 35.3, 620, 530, cartao("Guia extra sobre o que passou", "", TINTA, 600, 100, 38), anim="right")
        entra(c, t, 37.7, 620, 660, cartao("Ano seguinte: deixa de ser MEI", "", TINTA, 600, 100, 38), anim="right")
        consultor_i(c, t, 170, 1300, 1.15, poses=((0, "present"), (37.7, "finger_up")), exprs=((0, "neutral"), (37.7, "think")), look=0.6)
    else:
        fundo_marca(c, t, "vermelho", holofote=(220, 1100))
        numero_i(c, "PASSOU DE 20%?", 520, 230, 100, CREME)
        entra(c, t, 41.4, 620, 400, selo("VOLTA PRA JANEIRO", NAVY, 58, GOLD), anim="stamp")
        entra(c, t, 43.4, 620, 560, cartao("Imposto de microempresa", "", TINTA, 600, 100, 40), anim="right")
        entra(c, t, 45.3, 620, 680, cartao("sobre o ano inteiro", "", TINTA, 600, 100, 40), anim="right")
        consultor_i(c, t, 170, 1300, 1.15, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.6)


def s05(c, t):  # 46.8 - 58.1  3. seguro-desemprego
    fundo_marca(c, t, "vermelho", holofote=(200, 1100))
    entra(c, t, 47.0, 520, 240, topico("3", "SEGURO-DESEMPREGO", size=60), anim="stamp")
    entra(c, t, 48.9, 620, 420, lambda c: notificacao(c, 0, 0, 0.95, "Seguro-desemprego", "pedido em análise: CNPJ ativo", VERMELHO, "GOV"),
          anim="drop")
    entra(c, t, 51.7, 620, 590, selo("CNPJ ATIVO = RENDA PRÓPRIA?", VERMELHO, 40, CREME), anim="stamp")
    entra(c, t, 54.5, 620, 740, cartao("Dá pra recorrer...", "", TINTA, 580, 96), anim="right")
    entra(c, t, 56.4, 620, 850, cartao("provando que não teve renda", "", TINTA, 580, 96, 38), anim="right")
    pessoa(c, t, 180, 1300, 1.25, "lucas", poses=((0, "hold"), (51.7, "head")), exprs=((0, "worried"), (51.7, "desperate")), look=0.6,
           prop=("r", prop_celular_i) if t < 51.7 else None)


def s06(c, t):  # 58.1 - 73.9  4. aposentadoria
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    entra(c, t, 58.3, 520, 240, topico("4", "APOSENTADORIA"), anim="stamp")
    if t < 65.2:
        entra(c, t, 60.7, 620, 420, cartao("O DAS já inclui o INSS", "", TINTA, 600, 100), anim="right")
        if t > 62.8:
            numero_i(c, "MAS SÓ", 620, 560, 60, CREME)
            numero_i(c, "5% DO MÍNIMO", 620, 670, 90, GOLD)
            numero_i(c, "(R$ 81,05)", 620, 770, 54, CREME) if t > 64.2 else None
    else:
        numero_i(c, "GARANTE", 620, 390, 70, CREME)
        entra(c, t, 65.6, 620, 520, item("Aposentadoria por idade", True, 600, 38), anim="right")
        entra(c, t, 67.2, 620, 630, item("de 1 salário mínimo", True, 600, 38), anim="right")
        entra(c, t, 68.3, 620, 740, item("Auxílio-doença", True, 600), anim="right")
        entra(c, t, 69.6, 620, 850, item("Salário-maternidade", True, 600), anim="right")
        entra(c, t, 71.2, 650, 1000, selo("QUER MAIS? COMPLEMENTA", GOLD, 38, NAVY), anim="stamp")
    pessoa(c, t, 180, 1300, 1.2, "aposentado", poses=((0, "stand"), (65.6, "thumb"), (71.2, "finger_up")),
           exprs=((0, "neutral"), (65.6, "happy"), (71.2, "think")), look=0.6)


def s07(c, t):  # 73.9 - 82.9  5. declaração e nota
    cena_escritorio(c, t, "dia")
    entra(c, t, 74.1, 520, 240, topico("5", "A DECLARAÇÃO"), anim="stamp")
    entra(c, t, 75.1, 620, 420, cartao("Todo ano, até", "31/05", VERMELHO, 600), anim="right")
    entra(c, t, 78.0, 620, 550, selo("MESMO SEM FATURAR", NAVY, 50, GOLD), anim="stamp")
    entra(c, t, 79.8, 620, 720, cartao("Nota fiscal: obrigatória", "", TINTA, 600, 100, 40), anim="right")
    entra(c, t, 81.3, 620, 830, cartao("vendendo pra empresa", "", TINTA, 600, 100, 40), anim="right")
    consultor_i(c, t, 180, 1300, 1.2, poses=((0, "present"), (78.0, "finger_up")), exprs=((0, "neutral"), (78.0, "think")), look=0.6,
                prop=("l", prop_tablet_i) if t < 78.0 else None)


def s08(c, t):  # 82.9 - 94.5  por outro lado
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    numero_i(c, "POR OUTRO LADO", 520, 230, 96, CREME)
    entra(c, t, 84.7, 620, 400, item("CNPJ", True, 560), anim="right")
    entra(c, t, 85.9, 620, 510, item("Emite nota", True, 560), anim="right")
    entra(c, t, 86.9, 620, 620, item("Contribui pro INSS", True, 560), anim="right")
    entra(c, t, 88.8, 620, 730, item("Pouco imposto", True, 560), anim="right")
    entra(c, t, 90.2, 640, 880, selo("UM DOS MAIS BARATOS", GOLD, 44, NAVY), anim="stamp")
    if t > 91.4:
        numero_i(c, "pra quem fatura pouco", 640, 1000, 44, CREME, font=HAND)
    consultor_i(c, t, 160, 1300, 1.05, poses=((0, "present"), (88.8, "thumb")), exprs=((0, "happy"), (88.8, "grin")), look=0.6)


def s09(c, t):  # 94.5 - 103.5  antes de abrir
    fundo_marca(c, t, "navy", holofote=(220, 1100))
    numero_i(c, "ANTES DE ABRIR", 520, 230, 100, GOLD)
    entra(c, t, 95.8, 620, 420, item("Atividade permitida?", True, 600), anim="right")
    entra(c, t, 98.2, 620, 540, item("Conta do faturamento", True, 600), anim="right")
    entra(c, t, 100.6, 620, 660, item("Seguro-desemprego?", True, 600), anim="right")
    entra(c, t, 102.3, 620, 790, selo("SE INFORME PRIMEIRO", VERMELHO, 50, CREME), anim="stamp")
    consultor_i(c, t, 180, 1300, 1.2, poses=((0, "finger_up"), (98.2, "present")), exprs=((0, "confident"), (98.2, "neutral")), look=0.6,
                prop=("l", prop_tablet_i))


def s10(c, t):  # 103.5 - fim  ep. 7?
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "SEGUE PRO EP. 7", 520, 230, 100, GOLD)
    entra(c, t, 106.8, 520, 390, selo("EMPRÉSTIMO PESSOAL", BLUE, 52, CREME), anim="stamp")
    numero_i(c, "OU", 520, 500, 70, CREME) if t > 108.0 else None
    entra(c, t, 108.2, 520, 610, selo("CHEQUE ESPECIAL", PURPLE, 56, CREME), anim="stamp")
    entra(c, t, 109.5, 520, 750, selo("COMENTA", VERMELHO, 66, CREME), anim="stamp")
    consultor_i(c, t, 520, 1330, 0.95, poses=((0, "present"), (109.5, "point_r")), exprs=((0, "happy"), (109.5, "grin")), look=0.0)


SCENES = [(0, 6.1, s01), (6.1, 19.2, s02), (19.2, 30.2, s03), (30.2, 46.8, s04), (46.8, 58.1, s05),
          (58.1, 73.9, s06), (73.9, 82.9, s07), (82.9, 94.5, s08), (94.5, 103.5, s09), (103.5, 999.0, s10)]
