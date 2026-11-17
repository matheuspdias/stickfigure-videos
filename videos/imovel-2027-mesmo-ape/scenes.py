"""Mesmo apartamento, 3 rendas: em 2027, quem ganha um pouco mais paga mais caro. Só TikTok: vertical 1080x1920, ~103,1 s, estilo ilustrado.
Pedido do Matheus em 17/11/2026 (refaz imovel-2027-o-que-muda com o ângulo dele). Sem cartaz de abertura (2b.1): no quadro 0 as parcelas dos três já estão subindo.
Narração: Afonso (HeyGen), 1 bloco. Contas e fontes em contas.py (SAC, R$ 280 mil financiados, sem TR/seguros)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(25.4, "soft_ding"), (49.0, "tum"), (67.1, "tum"), (95.5, "soft_ding")]
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



def tres(c, t, y=1300, s=0.85, xs=(200, 540, 880), poses=None, exprs=None, destaque=None):
    for k, (q, x) in enumerate(zip(("ana", "bruno", "carla"), xs)):
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
def s01(c, t):  # 0 - 6.5  mesmo apê, 3 pessoas: quem ganha mais paga mais caro
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "O MESMO APÊ, 3 RENDAS")
    barras_i(c, t, -1.2, 160, 920, w=760, h=440, dados=(("ANA", 2394, VERDE), ("BRUNO", 2899, GOLD), ("CARLA", 4058, VERMELHO)),
             fmt=lambda v: brl(v), d=2.2, intervalo=0.7, size_val=52)
    if t > 3.0:
        entra(c, t, 3.0, 540, 340, selo("QUEM GANHA MAIS PAGA MAIS", VERMELHO, 46, CREME), anim="stamp")
    tres(c, t, y=1350, s=0.55, xs=(290, 540, 790), poses=(((0, "stand"),), ((0, "stand"),), ((0, "stand"), (3.0, "head"))),
         exprs=(((0, "grin"),), ((0, "neutral"),), ((0, "think"), (3.0, "shocked"))))


def s02(c, t):  # 6.5 - 14.6  apê de 350 mil; entrada 70 mil; financia 280 mil
    cena_rua(c, t, hora="dia", carros=False)
    rr(c, 90, 170, 900, 120, 24); rgb(c, NAVY, 0.92); c.fill()
    numero_i(c, "O MESMO APARTAMENTO", 540, 230, 54, CREME)
    predio_moderno(c, 540, 1000, 300, 560)
    if t > 6.8:
        entra(c, t, 6.8, 560, 400, lambda c: etiqueta_preco(c, "R$ 350 MIL", GOLD, 64), anim="drop")
    if t > 9.6:
        entra(c, t, 9.6, 540, 560, selo("ENTRADA: R$ 70 MIL", NAVY, 52, GOLD), anim="stamp")
    if t > 12.4:
        entra(c, t, 12.4, 540, 680, selo("FINANCIA: R$ 280 MIL", VERMELHO, 52, CREME, rot=0.05), anim="stamp")
    tres(c, t, y=1320, s=0.85, xs=(200, 540, 880))


def s03(c, t):  # 14.6 - 27.0  Ana, 9 mil: MCMV faixa 3, <8% a.a., 35 anos -> ~2.400
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1150))
    ficha(c, t, "ANA", "R$ 9 MIL", ROXO, 14.8)
    if t > 17.3:
        entra(c, t, 17.3, 560, 480, selo("MINHA CASA MINHA VIDA: FAIXA 3", NAVY, 40, GOLD), anim="stamp")
    linha_conta(c, t, 20.2, 590, "Juros", "< 8% AO ANO", 21.4, VERDE, vsize=54)
    linha_conta(c, t, 22.4, 730, "Prazo", "35 ANOS", 23.0, NAVY)
    if t > 25.3:
        rr(c, 380, 840, 560, 200, 26); rgb(c, CREME); c.fill()
        text(c, "1ª PARCELA", 660, 895, 40, MARKER, NAVY)
        contador(c, t, 25.4, 0, 2394, 660, 980, 90, d=1.2, col=VERDE)
    pessoa(c, t, 190, 1350, 0.85, "ana", poses=((0, "stand"), (25.4, "thumb")), exprs=((0, "neutral"), (25.4, "grin")), look=0.6)


def s04(c, t):  # 27.0 - 33.6  Bruno, 12 mil: faixa 4, 10% -> ~2.900
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(220, 1150))
    ficha(c, t, "BRUNO", "R$ 12 MIL", AZUL, 27.1)
    if t > 28.7:
        entra(c, t, 28.7, 600, 520, selo("FAIXA 4", GOLD, 60, TINTA), anim="stamp")
    linha_conta(c, t, 29.6, 680, "Juros", "10% AO ANO", 30.2, GOLD, vsize=56)
    if t > 31.4:
        rr(c, 380, 790, 560, 200, 26); rgb(c, CREME); c.fill()
        text(c, "1ª PARCELA", 660, 845, 40, MARKER, NAVY)
        contador(c, t, 32.0, 0, 2899, 660, 930, 90, d=1.0, col=GOLD)
    pessoa(c, t, 190, 1330, 1.15, "bruno", poses=((0, "stand"), (32.0, "think")), exprs=((0, "neutral"), (32.0, "neutral")), look=0.6)


def s05(c, t):  # 33.6 - 51.6  Carla, 14 mil: passou do limite (13 mil) -> banco 11% a 15% -> 3.264 a 4.058
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(200, 1150))
    ficha(c, t, "CARLA", "R$ 14 MIL", CORAL, 33.7)
    if t > 35.6:
        entra(c, t, 35.6, 580, 470, selo("LIMITE DO PROGRAMA: R$ 13 MIL", NAVY, 40, GOLD), anim="stamp")
    if t > 38.4:
        entra(c, t, 38.4, 640, 570, selo("VAI PRO BANCO", GOLD, 52, TINTA, rot=0.05), anim="stamp")
    linha_conta(c, t, 41.6, 680, "Caixa", "11,19%", 42.4, GOLD, vsize=56)
    linha_conta(c, t, 43.6, 810, "Bradesco", "15,00%", 44.6, VERMELHO, vsize=56)
    if t > 46.2:
        rr(c, 330, 910, 620, 220, 26); rgb(c, CREME); c.fill()
        text(c, "1ª PARCELA", 640, 965, 40, MARKER, NAVY)
        if t < 49.0:
            contador(c, t, 46.3, 0, 3264, 640, 1060, 76, d=1.0, col=GOLD)
        else:
            numero_i(c, "R$ 3.264 a", 640, 1020, 50, GOLD)
            pop(c, t, 49.0, 640, 1090, "R$ 4.058", 76, VERMELHO)
    pessoa(c, t, 165, 1350, 0.75, "carla", poses=((0, "stand"), (35.6, "think"), (49.0, "head")),
           exprs=((0, "neutral"), (35.6, "think"), (49.0, "shocked")), look=0.6)


def s06(c, t):  # 51.6 - 60.9  mesmo apê: Carla paga até 1.664 a mais/mês; ~230 mil a mais de juros
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "MESMO APARTAMENTO", NAVY, CREME)
    barras_i(c, t, 51.7, 160, 1000, w=760, h=520, dados=(("ANA", 2394, VERDE), ("BRUNO", 2899, GOLD), ("CARLA", 4058, VERMELHO)),
             fmt=lambda v: brl(v), d=1.0, intervalo=0.3, size_val=52)
    if t > 54.0:
        entra(c, t, 54.0, 540, 340, selo("+ R$ 1.664 POR MÊS", VERMELHO, 56, CREME), anim="stamp")
    if t > 58.0:
        entra(c, t, 58.0, 540, 1150, selo("+ R$ 230 MIL DE JUROS", NAVY, 52, GOLD, rot=0.04), anim="stamp")


def s07(c, t):  # 60.9 - 72.7  R$ 13.100: 100 reais acima do limite -> parcela +1.000/mês
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(200, 1150))
    topo(c, "OLHA QUE ABSURDO")
    cartao(c, t, 62.3, 600, 440, 640, 190, "RENDA R$ 13.000", "R$ 2.899", GOLD, 70)
    cartao(c, t, 64.0, 600, 680, 640, 190, "RENDA R$ 13.100", "ATÉ R$ 4.058", VERMELHO, 70)
    if t > 65.6:
        entra(c, t, 65.6, 600, 850, selo("FORA DO PROGRAMA", VERMELHO, 52, CREME), anim="stamp")
    if t > 67.1:
        pop(c, t, 67.2, 600, 990, "+ R$ 1.159/MÊS", 76, GOLD)
    if t > 70.4:
        entra(c, t, 70.4, 600, 1120, selo("POR R$ 100 DE RENDA", NAVY, 50, GOLD, rot=0.05), anim="stamp")
    consultor_i(c, t, 150, 1330, 0.9, poses=((0, "present"), (67.2, "head")), exprs=((0, "neutral"), (67.2, "shocked")), look=0.6)


def s08(c, t):  # 72.7 - 90.9  2027: teto 12% no SFH seguraria; mas poupança perde, bancos pedem adiar, Caixa estuda subir
    luz("dia")
    fundo_marca(c, t, "verde" if t < 82.9 else "vermelho", holofote=(200, 1150))
    topo(c, "E EM 2027?")
    c.save(); c.translate(600, 440); c.scale(1.5, 1.5); calendar(c, "JAN", VERMELHO, 52); c.restore()
    numero_i(c, "2027", 600, 590, 56, GOLD)
    cartao(c, t, 75.0, 600, 740, 680, 170, "NOVO MODELO: TETO NO SFH", "12% AO ANO + TR", VERDE, 58)
    if 80.4 < t < 82.9:
        entra(c, t, 80.4, 600, 900, selo("SEGURARIA AS TAXAS", GOLD, 50, TINTA), anim="stamp")
    if t > 83.0:
        entra(c, t, 83.0, 600, 900, selo("POUPANÇA: - R$ 60,8 BI EM 2026", NAVY, 40, GOLD), anim="stamp")
    if t > 85.8:
        entra(c, t, 85.8, 600, 1020, selo("BANCOS PEDEM ADIAR", GOLD, 48, TINTA, rot=0.05), anim="stamp")
    if t > 88.6:
        entra(c, t, 88.6, 600, 1140, selo("CAIXA ESTUDA SUBIR", CREME, 48, VERMELHO), anim="stamp")
    consultor_i(c, t, 150, 1330, 0.9, poses=((0, "present"), (80.4, "thumb"), (83.0, "shrug")),
                exprs=((0, "neutral"), (80.4, "grin"), (83.0, "think")), look=0.6)


def s09(c, t):  # 90.9 - 98.4  classe média: ganha demais pro programa, paga o juro mais caro
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(880, 1250))
    topo(c, "OU SEJA:")
    if t > 92.5:
        entra(c, t, 92.5, 540, 420, selo("A CLASSE MÉDIA", GOLD, 70, TINTA), anim="stamp")
    if t > 93.9:
        entra(c, t, 93.9, 540, 580, selo("GANHA DEMAIS PRO PROGRAMA", NAVY if False else VERMELHO, 46, CREME, rot=0.04), anim="stamp")
    if t > 95.5:
        entra(c, t, 95.5, 540, 720, selo("E PAGA O JURO MAIS CARO", CREME, 50, VERMELHO), anim="stamp")
    tres(c, t, y=1330, s=0.85, xs=(200, 540, 860), destaque=2,
         poses=(((0, "stand"),), ((0, "stand"),), ((0, "stand"), (95.5, "head"))),
         exprs=(((0, "neutral"),), ((0, "neutral"),), ((0, "think"), (95.5, "desperate"))))


def s10(c, t):  # 98.4 - fim  dentro do programa ou passou do limite?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(300, 1150))
    topo(c, "E VOCÊ?")
    entra(c, t, 99.2, 560, 430, selo("DENTRO DO PROGRAMA?", VERDE, 60, CREME, rot=0.05), anim="pop")
    entra(c, t, 100.6, 620, 600, selo("PASSOU DO LIMITE?", VERMELHO, 60, CREME), anim="pop")
    entra(c, t, 102.2, 620, 800, selo("COMENTA", GOLD, 64, TINTA), anim="stamp")
    pessoa(c, t, 200, 1330, 1.15, "carla", poses=((0, "think"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 6.5, s01), (6.5, 14.6, s02), (14.6, 27.0, s03), (27.0, 33.6, s04), (33.6, 51.6, s05),
          (51.6, 60.9, s06), (60.9, 72.7, s07), (72.7, 90.9, s08), (90.9, 98.4, s09), (98.4, 999.0, s10)]
