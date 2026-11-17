"""Mesmo apartamento, 3 rendas: em 2027, quem ganha um pouco mais paga mais caro. Só TikTok: vertical 1080x1920, ~114,8 s, estilo ilustrado.
Pedido do Matheus em 17/11/2026 (v2: casal de R$ 5 mil na Faixa 2, apê de R$ 240 mil, gancho novo). Sem cartaz de abertura (2b.1): no quadro 0 as parcelas dos três já estão subindo.
Narração: Afonso (HeyGen), 1 bloco. Contas e fontes em contas.py (SAC, R$ 192 mil financiados, sem TR/seguros)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(2.4, "tum"), (33.1, "soft_ding"), (59.0, "tum"), (77.4, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ROXO = PURPLE; AZUL = BLUE; CORAL = (0.86, 0.40, 0.36)


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



def casal(c, t, x, y, s, poses=((0, "stand"),), exprs=((0, "neutral"),)):
    pessoa(c, t, x - 70 * s, y, s, "ana", poses=poses, exprs=exprs, look=0.3)
    pessoa(c, t, x + 70 * s, y, s, "diego", poses=poses, exprs=exprs, look=-0.3)


def tres(c, t, y=1300, s=0.85, xs=(200, 540, 880), poses=None, exprs=None, destaque=None):
    casal(c, t, xs[0], y, s * 0.92, poses=poses[0] if poses else ((0, "stand"),), exprs=exprs[0] if exprs else ((0, "neutral"),))
    for k, (q, x) in enumerate(zip(("casal", "bruno", "carla"), xs)):
        if k == 0:
            continue
        p = poses[k] if poses else ((0, "stand"),)
        e = exprs[k] if exprs else ((0, "neutral"),)
        ss = s * (1.12 if destaque == k else 1.0)
        pessoa(c, t, x, y, ss, q, poses=p, exprs=e, look=0.0)


def ficha(c, t, nome, renda, cor, t_renda):
    """nome + renda no topo da cena do personagem"""
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, nome, 540, 230, 60, CREME)
    if t > t_renda:
        entra(c, t, t_renda, 540, 370, selo("RENDA: " + renda, cor, 60, CREME), anim="stamp")


# ======================================================================= CENAS
DADOS = (("CASAL", 1467, VERDE), ("BRUNO", 1988, GOLD), ("CARLA", 2783, VERMELHO))


def s01(c, t):  # 0 - 12.0  gancho: ainda não comprou? para tudo. +1.300/mês pelo mesmo imóvel. 2027 pode piorar
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "FINANCIAMENTO EM 2027")
    barras_i(c, t, -1.2, 160, 900, w=760, h=420, dados=DADOS, fmt=lambda v: brl(v), d=2.2, intervalo=0.7, size_val=52)
    if t < 6.4:
        entra(c, t, -1, 540, 340, selo("AINDA NÃO COMPROU APÊ?", VERMELHO, 52, CREME), anim="pop")
    else:
        entra(c, t, 6.4, 540, 340, selo("+ R$ 1.300/MÊS NO MESMO APÊ", VERMELHO, 46, CREME), anim="stamp")
    if 2.3 < t < 3.9:
        pop(c, t, 2.4, 540, 640, "PARA TUDO!", 150, GOLD)
    if t > 9.8:
        entra(c, t, 9.8, 540, 1040, selo("2027 PODE PIORAR", GOLD, 56, TINTA, rot=0.04), anim="stamp")
    tres(c, t, y=1390, s=0.5, xs=(270, 560, 820), poses=(((0, "stand"),), ((0, "stand"),), ((0, "stand"), (6.4, "head"))),
         exprs=(((0, "grin"),), ((0, "neutral"),), ((0, "think"), (6.4, "shocked"))))


def s02(c, t):  # 12.0 - 19.2  apê de 240 mil; entrada 20%; financia 192 mil
    cena_rua(c, t, hora="dia", carros=False)
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "O MESMO APARTAMENTO", 540, 230, 54, CREME)
    predio_moderno(c, 540, 1000, 300, 560)
    if t > 12.2:
        entra(c, t, 12.2, 560, 400, lambda c: etiqueta_preco(c, "R$ 240 MIL", GOLD, 64), anim="drop")
    if t > 15.4:
        entra(c, t, 15.4, 540, 560, selo("ENTRADA: 20%", NAVY, 52, GOLD), anim="stamp")
    if t > 17.0:
        entra(c, t, 17.0, 540, 680, selo("FINANCIA: R$ 192 MIL", VERMELHO, 52, CREME, rot=0.05), anim="stamp")
    tres(c, t, y=1320, s=0.8, xs=(220, 590, 880))


def s03(c, t):  # 19.2 - 37.6  casal 2.500 + 2.500 = 5 mil: MCMV faixa 2, ~6,5%, 35 anos -> ~1.470 (+ subsídio)
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1150))
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "UM CASAL", 540, 230, 60, CREME)
    if t > 20.8:
        entra(c, t, 20.8, 540, 370, selo("R$ 2.500 + R$ 2.500", ROXO, 54, CREME), anim="stamp")
    if t > 23.0:
        entra(c, t, 23.0, 560, 480, selo("= R$ 5 MIL", NAVY, 50, GOLD, rot=0.05), anim="stamp")
    if t > 24.8:
        entra(c, t, 24.8, 560, 590, selo("MINHA CASA MINHA VIDA: FAIXA 2", GOLD, 38, TINTA), anim="stamp")
    linha_conta(c, t, 27.8, 700, "Juros", "~6,5% AO ANO", 29.0, VERDE, vsize=54)
    linha_conta(c, t, 30.2, 830, "Prazo", "35 ANOS", 30.8, NAVY)
    if t > 33.0:
        rr(c, 380, 910, 560, 200, 26); rgb(c, CREME); c.fill()
        text(c, "1ª PARCELA", 660, 965, 40, MARKER, NAVY)
        contador(c, t, 33.1, 0, 1467, 660, 1050, 90, d=1.2, col=VERDE)
    if t > 35.4:
        entra(c, t, 35.4, 660, 1180, selo("+ PODE TER SUBSÍDIO", NAVY, 44, GOLD, rot=-0.04), anim="stamp")
    casal(c, t, 200, 1380, 0.62, poses=((0, "stand"), (33.1, "thumb")), exprs=((0, "neutral"), (33.1, "grin")))


def s04(c, t):  # 37.6 - 43.3  Bruno, 12 mil: faixa 4, 10% -> ~2.000
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(220, 1150))
    ficha(c, t, "BRUNO", "R$ 12 MIL", AZUL, 37.7)
    if t > 39.2:
        entra(c, t, 39.2, 600, 520, selo("FAIXA 4", GOLD, 60, TINTA), anim="stamp")
    linha_conta(c, t, 39.8, 680, "Juros", "10% AO ANO", 40.2, GOLD, vsize=56)
    if t > 41.4:
        rr(c, 380, 790, 560, 200, 26); rgb(c, CREME); c.fill()
        text(c, "1ª PARCELA", 660, 845, 40, MARKER, NAVY)
        contador(c, t, 42.0, 0, 1988, 660, 930, 90, d=0.9, col=GOLD)
    pessoa(c, t, 190, 1330, 1.15, "bruno", poses=((0, "stand"), (42.0, "think")), exprs=((0, "neutral"),), look=0.6)


def s05(c, t):  # 43.3 - 61.3  Carla, 14 mil: passou do limite (13 mil) -> banco 11% a 15% -> 2.238 a 2.783
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(200, 1150))
    ficha(c, t, "CARLA", "R$ 14 MIL", CORAL, 43.4)
    if t > 45.2:
        entra(c, t, 45.2, 580, 470, selo("LIMITE DO PROGRAMA: R$ 13 MIL", NAVY, 40, GOLD), anim="stamp")
    if t > 48.3:
        entra(c, t, 48.3, 640, 570, selo("VAI PRO BANCO", GOLD, 52, TINTA, rot=0.05), anim="stamp")
    linha_conta(c, t, 51.5, 680, "Caixa", "11,19%", 52.4, GOLD, vsize=56)
    linha_conta(c, t, 53.5, 810, "Bradesco", "15,00%", 54.6, VERMELHO, vsize=56)
    if t > 55.8:
        rr(c, 330, 910, 620, 220, 26); rgb(c, CREME); c.fill()
        text(c, "1ª PARCELA", 640, 965, 40, MARKER, NAVY)
        if t < 59.0:
            contador(c, t, 55.9, 0, 2238, 640, 1060, 76, d=1.2, col=GOLD)
        else:
            numero_i(c, "R$ 2.238 a", 640, 1020, 50, GOLD)
            pop(c, t, 59.0, 640, 1090, "R$ 2.783", 76, VERMELHO)
    pessoa(c, t, 165, 1350, 0.75, "carla", poses=((0, "stand"), (45.2, "think"), (59.0, "head")),
           exprs=((0, "neutral"), (45.2, "think"), (59.0, "shocked")), look=0.6)


def s06(c, t):  # 61.3 - 71.5  mesmo apê: Carla paga até 1.316 a mais/mês; quase 200 mil a mais de juros
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "MESMO APARTAMENTO", NAVY, CREME)
    barras_i(c, t, 61.4, 160, 1000, w=760, h=520, dados=DADOS, fmt=lambda v: brl(v), d=1.0, intervalo=0.3, size_val=52)
    if t > 62.6:
        entra(c, t, 62.6, 540, 340, selo("+ R$ 1.316 POR MÊS", VERMELHO, 56, CREME), anim="stamp")
    if t > 67.0:
        entra(c, t, 67.0, 540, 1150, selo("+ QUASE R$ 200 MIL DE JUROS", NAVY, 46, GOLD, rot=0.04), anim="stamp")


def s07(c, t):  # 71.5 - 83.0  R$ 13.100: 100 reais acima do limite -> parcela +795/mês
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(200, 1150))
    topo(c, "OLHA QUE ABSURDO")
    cartao(c, t, 72.6, 600, 440, 640, 190, "RENDA R$ 13.000", "R$ 1.988", GOLD, 70)
    cartao(c, t, 74.3, 600, 680, 640, 190, "RENDA R$ 13.100", "ATÉ R$ 2.783", VERMELHO, 70)
    if t > 75.9:
        entra(c, t, 75.9, 600, 850, selo("FORA DO PROGRAMA", VERMELHO, 52, CREME), anim="stamp")
    if t > 77.4:
        pop(c, t, 77.5, 600, 990, "+ R$ 795/MÊS", 80, GOLD)
    if t > 80.9:
        entra(c, t, 80.9, 600, 1120, selo("POR R$ 100 DE RENDA", NAVY, 50, GOLD, rot=0.05), anim="stamp")
    consultor_i(c, t, 150, 1330, 0.9, poses=((0, "present"), (77.5, "head")), exprs=((0, "neutral"), (77.5, "shocked")), look=0.6)


def s08(c, t):  # 83.0 - 103.1  2027: teto 12% no SFH seguraria; mas poupança perde, bancos pedem adiar, Caixa estuda subir
    luz("dia")
    fundo_marca(c, t, "verde" if t < 94.6 else "vermelho", holofote=(200, 1150))
    topo(c, "2027 PODE PIORAR")
    c.save(); c.translate(600, 440); c.scale(1.5, 1.5); calendar(c, "JAN", VERMELHO, 52); c.restore()
    numero_i(c, "2027", 600, 590, 56, GOLD)
    cartao(c, t, 85.4, 600, 740, 680, 170, "NOVO MODELO: TETO NO SFH", "12% AO ANO + TR", VERDE, 58)
    if 92.1 < t < 94.6:
        entra(c, t, 92.1, 600, 900, selo("SEGURARIA AS TAXAS", GOLD, 50, TINTA), anim="stamp")
    if t > 94.7:
        entra(c, t, 94.7, 600, 900, selo("POUPANÇA: - R$ 60,8 BI EM 2026", NAVY, 40, GOLD), anim="stamp")
    if t > 97.6:
        entra(c, t, 97.6, 600, 1020, selo("BANCOS PEDEM ADIAR", GOLD, 48, TINTA, rot=0.05), anim="stamp")
    if t > 100.6:
        entra(c, t, 100.6, 600, 1140, selo("CAIXA ESTUDA SUBIR", CREME, 48, VERMELHO), anim="stamp")
    consultor_i(c, t, 150, 1330, 0.9, poses=((0, "present"), (92.1, "thumb"), (94.7, "shrug")),
                exprs=((0, "neutral"), (92.1, "grin"), (94.7, "think")), look=0.6)


def s09(c, t):  # 103.1 - 110.4  classe média: ganha demais pro programa, paga o juro mais caro
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(880, 1250))
    topo(c, "OU SEJA:")
    if t > 104.6:
        entra(c, t, 104.6, 540, 420, selo("A CLASSE MÉDIA", GOLD, 70, TINTA), anim="stamp")
    if t > 106.2:
        entra(c, t, 106.2, 540, 580, selo("GANHA DEMAIS PRO PROGRAMA", VERMELHO, 46, CREME, rot=0.04), anim="stamp")
    if t > 108.0:
        entra(c, t, 108.0, 540, 720, selo("E PAGA O JURO MAIS CARO", CREME, 50, VERMELHO), anim="stamp")
    tres(c, t, y=1330, s=0.8, xs=(220, 590, 880), destaque=2,
         poses=(((0, "stand"),), ((0, "stand"),), ((0, "stand"), (108.0, "head"))),
         exprs=(((0, "neutral"),), ((0, "neutral"),), ((0, "think"), (108.0, "desperate"))))


def s10(c, t):  # 110.4 - fim  dentro do programa ou passou do limite?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "E VOCÊ?")
    entra(c, t, 110.9, 560, 430, selo("DENTRO DO PROGRAMA?", VERDE, 60, CREME, rot=0.05), anim="pop")
    entra(c, t, 112.3, 620, 600, selo("PASSOU DO LIMITE?", VERMELHO, 60, CREME), anim="pop")
    entra(c, t, 113.9, 620, 800, selo("COMENTA", GOLD, 64, TINTA), anim="stamp")
    pessoa(c, t, 200, 1330, 1.15, "carla", poses=((0, "think"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 12.0, s01), (12.0, 19.2, s02), (19.2, 37.6, s03), (37.6, 43.3, s04), (43.3, 61.3, s05),
          (61.3, 71.5, s06), (71.5, 83.0, s07), (83.0, 103.1, s08), (103.1, 110.4, s09), (110.4, 999.0, s10)]
