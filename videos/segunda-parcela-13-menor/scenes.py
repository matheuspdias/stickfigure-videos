"""Por que a 2ª parcela do 13º vem menor. Só TikTok: vertical nativo 1080x1920, ~71,4 s, estilo ilustrado.
18h, conta útil do momento (AUTOMATICO_TIKTOK.md 2b.2), pedido da "Fila do Matheus". Sem cartaz de abertura:
no quadro 0 as duas parcelas já estão crescendo e a 2ª encolhe. Narração: Afonso (HeyGen), 1 bloco.
Contas em contas.py (tabelas INSS e IR 2026, redução da Lei 15.270/2025)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(2.9, "tum"), (18.2, "tum"), (38.5, "soft_ding"), (55.6, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

VOCE = "lucas"


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


def coluna(c, x, base, h, w, cor, rot, valor, vcol=CREME):
    rr(c, x - w / 2 + 8, base - h + 10, w, h, 18); rgb(c, (0, 0, 0), 0.22); c.fill()
    rr(c, x - w / 2, base - h, w, h, 18); rgb(c, cor); c.fill()
    numero_i(c, valor, x, base - h - 50, 64, vcol)
    numero_i(c, rot, x, base + 55, 50, CREME)


def cartao_parcela(c, t, t0, x, y, nome, data, valor, desc=None, t_desc=None, cor=VERDE, s=1.0):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.4))
    c.save(); c.translate(x, y + 300 * (1 - k)); c.scale(s, s)
    rr(c, -200 + 8, -260 + 10, 400, 520, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, -200, -260, 400, 520, 30); rgb(c, CREME); c.fill()
    rr(c, -200, -260, 400, 120, 30); rgb(c, cor); c.fill(); c.rectangle(-200, -170, 400, 30); c.fill()
    text(c, nome, 0, -185, 54, MARKER, CREME)
    text(c, data, 0, -60, 46, MARKER, NAVY)
    if desc and t >= t_desc:
        text(c, desc, 0, 40, 40, MARKER, VERMELHO)
    text(c, valor, 0, 170, 70, MARKER, TINTA)
    c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 5.6  as duas parcelas crescendo; a 2ª encolhe
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(560, 1000))
    topo(c, "SEU 13º · SALÁRIO DE R$ 3 MIL")
    base = 1110
    h1 = 520 * ease_out(clamp01((t + 0.4) / 1.4))
    v1 = int(1500 * ease_out(clamp01((t + 0.4) / 1.4)))
    coluna(c, 470, base, h1, 230, VERDE, "1ª", brl(v1))
    if t > 0.9:
        g = ease_out(prog(t, 0.9, 1.2))
        enc = ease_out(prog(t, 2.9, 0.7)) if t > 2.9 else 0
        h2 = 520 * g - (520 - 434) * enc
        v2 = int(1500 * g - (1500 - 1251) * enc)
        coluna(c, 780, base, h2, 230, VERMELHO if enc > 0.5 else VERDE, "2ª", brl(v2))
    if t > 4.4:
        entra(c, t, 4.4, 620, 380, selo("NÃO É ERRO DO RH", VERMELHO, 56, CREME), anim="stamp")
    pessoa(c, t, 180, 1330, 1.15, VOCE, poses=((0, "stand"), (2.9, "head")), exprs=((0, "grin"), (2.9, "shocked")), look=0.6)


def s02(c, t):  # 5.6 - 11.0  a 1ª: até 30/11, metade, sem desconto
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(540, 1050))
    topo(c, "A 1ª PARCELA")
    cartao_parcela(c, t, 5.7, 600, 680, "1ª PARCELA", "até 30/11", "METADE", cor=VERDE, s=1.1)
    if t > 9.6:
        entra(c, t, 9.6, 600, 1080, selo("SEM DESCONTO", VERDE, 64, CREME), anim="stamp")
    pessoa(c, t, 180, 1330, 1.15, VOCE, poses=((0, "thumb"),), exprs=((0, "grin"),), look=0.6)


def s03(c, t):  # 11.0 - 21.3  a 2ª: até 18/12, com o desconto do 13º inteiro
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(260, 1100))
    topo(c, "A 2ª PARCELA")
    cartao_parcela(c, t, 11.0, 640, 680, "2ª PARCELA", "até 18/12", "MENOR", "- DESCONTO DO", 15.3, VERMELHO, s=1.05)
    if t > 16.4:
        text(c, "13º INTEIRO", 640, 760, 44, MARKER, VERMELHO)
    if t > 18.0:
        k = clamp01((t - 18.0) / 0.35)
        y = 300 + (560 - 300) * ease_out(k)
        entra(c, t, 18.0, 640, 1100, selo("INSS", NAVY, 80, GOLD), anim="drop")
    if t > 19.9:
        entra(c, t, 19.9, 640, 1230, selo("SÓ NELA", VERMELHO, 52, CREME, rot=0.05), anim="stamp")
    consultor_i(c, t, 200, 1330, 1.15, poses=((0, "present"), (14.0, "point_r")), exprs=((0, "neutral"), (17.8, "confident")), look=0.6)


def linha3(c, t, t0, y, sal, p1, t1, p2, t2):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.35))
    x = 540 - 600 * (1 - k)
    rr(c, x - 440, y - 66, 880, 132, 22); rgb(c, CREME); c.fill()
    text(c, sal, x - 300, y + 20, 56, MARKER, NAVY)
    if t >= t1:
        text(c, p1, x, y + 20, 56, MARKER, VERDE)
    if t >= t2:
        kk = 1 + 0.16 * math.sin(clamp01((t - t2) / 0.3) * math.pi)
        c.save(); c.translate(x + 300, y + 20); c.scale(kk, kk); text(c, p2, 0, 0, 60, MARKER, VERMELHO); c.restore()


def s04(c, t):  # 21.3 - 37.2  a conta: 2, 3 e 5 mil
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "OLHA A CONTA")
    if t > 22.0:
        for x, s in ((240, "SALÁRIO"), (540, "1ª"), (840, "2ª")):
            text(c, s, x, 390, 46, MARKER, GOLD)
    linha3(c, t, 22.4, 500, "R$ 2 MIL", "1.000", 23.8, "844", 25.9)
    linha3(c, t, 28.0, 670, "R$ 3 MIL", "1.500", 28.9, "1.251", 31.0)
    linha3(c, t, 32.8, 840, "R$ 5 MIL", "2.500", 33.8, "1.998", 36.0)
    consultor_i(c, t, 540, 1420, 0.9, poses=((0, "point_ru"),), exprs=((0, "neutral"), (36.0, "shocked")), look=0.0)


def s05(c, t):  # 37.2 - 44.0  virada: até 5 mil, IR zero no 13º
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    topo(c, "MAS OLHA A VIRADA")
    if t > 38.4:
        entra(c, t, 38.4, 640, 400, selo("NOVIDADE DE 2026", NAVY, 54, GOLD), anim="stamp")
    if t > 39.4:
        numero_i(c, "ATÉ R$ 5 MIL", 640, 560, 84, CREME)
    if t > 41.0:
        numero_i(c, "IMPOSTO DE RENDA", 640, 690, 56, CREME)
        numero_i(c, "NO 13º", 640, 770, 56, CREME)
        pop(c, t, 41.5, 640, 920, "R$ 0", 170, GOLD)
    pessoa(c, t, 200, 1330, 1.25, VOCE, poses=((0, "stand"), (41.5, "arms_up")), exprs=((0, "think"), (41.5, "grin")), look=0.6)


def s06(c, t):  # 44.0 - 50.4  ano passado: uns R$ 330 a mais de imposto
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "SALÁRIO DE R$ 5 MIL", NAVY, CREME)
    # 2025
    rr(c, 120, 360, 400, 420, 28); rgb(c, CREME); c.fill(); rr(c, 120, 360, 400, 110, 28); rgb(c, VERMELHO); c.fill()
    c.rectangle(120, 430, 400, 40); c.fill()
    text(c, "2025", 320, 440, 64, MARKER, CREME)
    text(c, "IR NO 13º", 320, 560, 48, MARKER, NAVY)
    if t > 47.3:
        contador(c, t, 47.3, 0, 335, 320, 700, 68, d=1.0, col=VERMELHO, prefixo="-R$ ")
    # 2026
    if t > 44.6:
        rr(c, 560, 360, 400, 420, 28); rgb(c, CREME); c.fill(); rr(c, 560, 360, 400, 110, 28); rgb(c, VERDE); c.fill()
        c.rectangle(560, 430, 400, 40); c.fill()
        text(c, "2026", 760, 440, 64, MARKER, CREME)
        text(c, "IR NO 13º", 760, 560, 48, MARKER, NAVY)
        text(c, "R$ 0", 760, 715, 84, MARKER, VERDE)
    for x in (120, 560):
        c.set_line_width(6); rgb(c, NAVY, 0.5); rr(c, x, 360, 400, 420, 28); c.stroke()
    consultor_i(c, t, 540, 1420, 0.95, poses=((0, "present"), (47.3, "point_ru")), exprs=((0, "neutral"), (48.3, "confident")), look=0.0)


def s07(c, t):  # 50.4 - 57.7  quem ganha 7 mil ainda paga
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(540, 1100))
    topo(c, "SALÁRIO DE R$ 7 MIL")
    base = 1050
    if t > 53.5:
        h1 = 560 * ease_out(prog(t, 53.5, 0.6))
        coluna(c, 470, base, h1, 220, VERDE, "1ª", "R$ 3.500")
    if t > 55.4:
        h2 = 560 * 1964 / 3500 * ease_out(prog(t, 55.4, 0.6))
        coluna(c, 790, base, h2, 220, NAVY, "2ª", "R$ 1.964")
    if t > 56.2:
        entra(c, t, 56.2, 700, 560, selo("- INSS - IR", NAVY, 46, CREME, rot=0.05), anim="stamp")
    if t < 53.5:
        numero_i(c, "AINDA PAGA IR", 540, 600, 90, GOLD)
    pessoa(c, t, 170, 1400, 0.95, VOCE, poses=((0, "think"), (55.6, "head")), exprs=((0, "think"), (55.6, "desperate")), look=0.0)


def s08(c, t):  # 57.7 - 66.2  a dica
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(240, 1100))
    topo(c, "A DICA")
    numero_i(c, "1ª", 430, 470, 130, VERDE) if t > 59.0 else None
    numero_i(c, "=", 620, 470, 130, CREME) if t > 59.4 else None
    numero_i(c, "2ª", 810, 470, 130, VERMELHO) if t > 59.4 else None
    if t > 60.4:
        c.save(); c.translate(620, 470); x_icon(c, 70); c.restore()
    if t > 62.3:
        entra(c, t, 62.3, 500, 700, selo("PRESENTE", VERMELHO, 54, CREME), anim="pop")
        entra(c, t, 63.5, 800, 760, selo("VIAGEM", BLUE, 54, CREME, rot=0.05), anim="pop")
    if t > 64.4:
        entra(c, t, 64.4, 610, 1090, selo("CONTA COM A 2ª MENOR", NAVY, 46, GOLD, rot=-0.03), anim="stamp")
    consultor_i(c, t, 220, 1360, 1.15, poses=((0, "finger_up"), (62.3, "point_r")), exprs=((0, "confident"),), look=0.6)


def s09(c, t):  # 66.2 - fim  salva e comenta
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(300, 1100))
    topo(c, "SALVA PRA CONFERIR")
    entra(c, t, 66.3, 640, 420, selo("SALVA", NAVY, 70, GOLD), anim="stamp")
    if t > 68.4:
        numero_i(c, "E A SUA,", 620, 600, 80, CREME)
        pop(c, t, 69.0, 620, 720, "QUANTO VEM?", 90, GOLD)
    if t > 70.0:
        entra(c, t, 70.0, 600, 1000, selo("COMENTA SEU SALÁRIO", VERMELHO, 46, CREME), anim="stamp")
    pessoa(c, t, 200, 1330, 1.25, VOCE, poses=((0, "hold"), (68.4, "think")), exprs=((0, "grin"), (68.4, "think")), look=0.6)


SCENES = [(0, 5.6, s01), (5.6, 11.0, s02), (11.0, 21.3, s03), (21.3, 37.2, s04), (37.2, 44.0, s05),
          (44.0, 50.4, s06), (50.4, 57.7, s07), (57.7, 66.2, s08), (66.2, 999.0, s09)]
