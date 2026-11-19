"""QUANTO RENDE R$ 1.000 EM 1 ANO (Parte 1): conta x poupança x Tesouro Selic x CDB 100% x CDB 110% (TikTok vertical, ~72,1 s).
Pesquisa de 19/11/2026: Selic 13,75% (Copom manteve em 04/11/2026); CDI 13,65% a.a.
Poupança: 0,6638% ao mês (BC, ciclo de 05/10/2026) -> 1,006638^12 = 1,0826 -> ~R$ 83, isenta de IR.
Tesouro Selic ~ CDI: bruto 1.000 x 13,65% = R$ 136,50; IR de 361 a 720 dias 17,5% = R$ 23,89 -> líquido ~R$ 113
(custódia B3 zero até R$ 10 mil no Tesouro Selic). CDB 100% CDI: igual, ~R$ 113.
CDB 110% CDI: 15,015% bruto = R$ 150,15; IR 17,5% -> ~R$ 124. Diferença CDB 110% x poupança: 124 - 83 = R$ 41.
FGC: até R$ 250 mil por CPF e por instituição. IR até 180 dias: 22,5%. Regra da tabela regressiva (a MP 1.303 não virou lei)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (16.5, "tum"), (30.0, "tum"), (41.5, "soft_ding"), (47.4, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

# nome, valor líquido, início do destaque, quando a barra cresce, fim do destaque
LINHAS = [("CONTA", 0, 0.0, 0.0, 9.5), ("POUPANÇA", 83, 15.5, 16.5, 22.1), ("TESOURO SELIC", 113, 22.1, 23.9, 33.3),
          ("CDB 100% CDI", 113, 33.3, 37.0, 38.7), ("CDB 110% CDI", 124, 38.7, 41.5, 43.2)]
X0, WMAX, VMAX = 400, 420, 140.0
L1, L2, R1, R2 = (275, 1010), (275, 1115), (775, 1010), (775, 1115)
C1, C2, CM = (540, 1010), (540, 1115), (540, 1060)


def chip(s, cor=CREME, tcol=TINTA, size=44, rot=0.0):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 56
        c.save(); c.rotate(rot)
        rr(c, -w / 2 + 6, -size * 0.75 + 8, w, size * 1.5, 18); rgb(c, (0, 0, 0), 0.25); c.fill()
        rr(c, -w / 2, -size * 0.75, w, size * 1.5, 18); rgb(c, cor); c.fill()
        text(c, s, 0, size * 0.36, size, MARKER, tcol)
        c.restore()
    return f


def valor_barra(i, v, t, tg):
    """valor mostrado na barra i no tempo t"""
    if i == 2:  # Tesouro Selic: sobe ao bruto, depois o IR come um pedaço
        if t < tg:
            return 0.0
        if t < 30.0:
            return 136.5 * ease_out(clamp01((t - tg) / 0.9))
        return 136.5 - 23.5 * ease_out(clamp01((t - 30.0) / 0.7))
    if i == 0 or t < tg:
        return 0.0
    return v * ease_out(clamp01((t - tg) / 0.9))


def tabela(c, t):
    rr(c, 60 + 8, 290 + 10, 870, 470, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 60, 290, 870, 470, 30); rgb(c, CREME); c.fill()
    text(c, "R$ 1.000 POR 1 ANO, JÁ SEM IMPOSTO", 495, 340, 34, MARKER, NAVY)
    for i, (nome, v, th, tg, tf) in enumerate(LINHAS):
        y = 402 + i * 76
        dest = th <= t < tf or (43.2 <= t < 54.1 and i in (1, 4))
        if dest:
            rr(c, 76, y - 34, 838, 68, 16); rgb(c, GOLD, 0.35); c.fill()
        text(c, nome, 92, y + 13, 36, MARKER, NAVY, align="l")
        vv = valor_barra(i, v, t, tg)
        if vv < 1:
            c.move_to(X0, y + 4); c.line_to(X0 + WMAX, y + 4); rgb(c, TINTA, 0.22); c.set_line_width(4)
            c.set_dash([12, 10]); c.stroke(); c.set_dash([])
            if i == 0:
                text(c, "R$ 0", X0 + 10, y + 15, 40, MARKER, VERMELHO, align="l")
            continue
        w = WMAX * vv / VMAX
        cor = VERDE if i != 1 else (0.45, 0.62, 0.80)
        if i == 2 and 30.0 <= t:
            # pedaço do IR que saiu, em vermelho claro
            wb = WMAX * 136.5 / VMAX
            a = max(0.0, 1 - (t - 31.6) / 1.0) if t > 31.6 else 1.0
            if a > 0:
                rr(c, X0, y - 26, wb, 52, 12); rgb(c, VERMELHO, 0.45 * a); c.fill()
        rr(c, X0, y - 26, w, 52, 12); rgb(c, cor); c.fill()
        if i == 2 and t < 30.0:
            s = "bruto " + brl(vv)
        else:
            s = "+" + brl(vv)
        text(c, s, X0 + w - 12, y + 9, 38, MARKER, CREME, align="r") if w > 190 else \
            text(c, s, X0 + w + 10, y + 9, 36, MARKER, TINTA, align="l")


def marcador(c, t):
    if 48.3 <= t < 54.1:
        k = 1 + 0.12 * math.sin(clamp01((t - 48.3) / 0.35) * math.pi)
        c.save(); c.translate(540, 850); c.scale(k, k)
        rr(c, -390, -70, 780, 140, 30); rgb(c, VERMELHO); c.fill()
        text(c, "POUPANÇA: - R$ 41/ANO", 0, 26, 62, MARKER, CREME)
        c.restore()
        return
    rr(c, 150, 790, 780, 120, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    if t < 15.5:
        text(c, "NA CONTA", 300, 866, 46, MARKER, CREME)
        contador(c, t, 0.0, 0, 1000, 690, 850, 80, d=1.6, col=CREME)
        return
    text(c, "VIRA", 260, 866, 50, MARKER, CREME)
    if t < 16.5:
        numero_i(c, "R$ 1.000", 640, 878, 84, CREME)
    elif t < 31.6:
        contador(c, t, 16.5, 1000, 1083, 640, 850, 84, d=0.9, col=VERDE)
    elif t < 41.5:
        contador(c, t, 31.6, 1083, 1113, 640, 850, 84, d=0.7, col=VERDE)
    else:
        contador(c, t, 41.5, 1113, 1124, 640, 850, 84, d=0.7, col=GOLD)


def detalhes(c, t):
    if 2.6 <= t < 8.1:
        entra(c, t, 2.6, *C1, chip("+ R$ 0,00 em 1 ano", VERMELHO, CREME, 48, -0.02), anim="stamp")
    if 6.6 <= t < 8.1:
        entra(c, t, 6.6, *C2, chip("já tirando o imposto", CREME, TINTA, 44, 0.02), anim="pop")
    if 8.1 <= t < 9.5:
        entra(c, t, 8.1, *CM, chip("SALVA A TABELA", GOLD, TINTA, 54), anim="pop")
    if 9.5 <= t < 15.5:
        entra(c, t, 9.8, *L1, chip("Selic 13,75%", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 12.1, *R1, chip("CDI 13,65%", GOLD, TINTA, 46, 0.04), anim="right")
        entra(c, t, 14.4, *C2, chip("ao ano", CREME, TINTA, 42), anim="pop")
    if 15.5 <= t < 22.1:
        entra(c, t, 16.5, *C1, chip("0,66% ao mês", CREME, TINTA, 46), anim="pop")
    if 20.8 <= t < 22.1:
        entra(c, t, 20.8, *C2, chip("SEM IMPOSTO", VERDE, CREME, 48), anim="stamp")
    if 22.1 <= t < 33.3:
        entra(c, t, 23.9, *L1, chip("bruto R$ 136", CREME, TINTA, 44, -0.04), anim="left")
    if 27.4 <= t < 33.3:
        entra(c, t, 27.4, *R1, chip("IR 17,5%", VERMELHO, CREME, 46, 0.04), anim="stamp")
    if 30.0 <= t < 33.3:
        entra(c, t, 30.0, *L2, chip("- R$ 24", VERMELHO, CREME, 46, 0.03), anim="left")
        entra(c, t, 30.5, *R2, chip("sobra R$ 113", VERDE, CREME, 44, -0.03), anim="right")
    if 33.3 <= t < 38.7:
        entra(c, t, 35.9, *C1, chip("a mesma conta", CREME, TINTA, 46), anim="pop")
        entra(c, t, 37.0, *C2, chip("R$ 1.113", VERDE, CREME, 52), anim="stamp")
    if 38.7 <= t < 43.2:
        entra(c, t, 39.3, *C1, chip("110% do CDI", CREME, TINTA, 46), anim="pop")
        entra(c, t, 41.5, *C2, chip("R$ 1.124", GOLD, TINTA, 54), anim="stamp")
    if 43.2 <= t < 48.3:
        entra(c, t, 43.7, *C1, chip("A VIRADA", VERMELHO, CREME, 54), anim="stamp")
        entra(c, t, 45.0, *C2, chip("sem imposto... e PERDE", CREME, TINTA, 42), anim="pop")
    if 48.3 <= t < 54.1:
        entra(c, t, 50.2, *C1, chip("vs CDB de 110%", CREME, TINTA, 44), anim="pop")
        entra(c, t, 51.8, *C2, chip("a cada R$ 1.000, todo ano", GOLD, TINTA, 40), anim="pop")
    if 54.1 <= t < 65.7:
        entra(c, t, 56.7, *L1, chip("FGC", CREME, NAVY, 52, -0.04), anim="left")
        entra(c, t, 57.6, *R1, chip("até R$ 250 mil", VERDE, CREME, 42, 0.04), anim="right")
    if 60.1 <= t < 65.7:
        entra(c, t, 61.2, *L2, chip("antes de 6 meses", CREME, TINTA, 38, 0.03), anim="left")
        entra(c, t, 63.8, *R2, chip("IR 22,5%", VERMELHO, CREME, 46, -0.03), anim="stamp")
    if 65.7 <= t < 69.6:
        entra(c, t, 65.9, *C1, chip("PARTE 2: R$ 5 MIL", GOLD, TINTA, 52), anim="stamp")
        entra(c, t, 67.0, *C2, chip("no perfil", CREME, TINTA, 44), anim="pop")
    if t >= 69.6:
        entra(c, t, 69.7, *CM, chip("SEU DINHEIRO TÁ ONDE?", GOLD, TINTA, 50), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANTO RENDE R$ 1.000 (PARTE 1)", 540, 235, 50, CREME)
    tabela(c, t)
    marcador(c, t)
    poses = ((0, "present"), (2.6, "shrug"), (6.6, "finger_up"), (8.1, "present"), (9.5, "finger_up"), (15.5, "point_r"),
             (20.8, "present"), (22.1, "point_r"), (27.4, "finger_up"), (30.0, "present"), (33.3, "point_r"), (38.7, "point_r"),
             (41.5, "finger_up"), (43.2, "finger_up"), (47.4, "shrug"), (54.1, "finger_up"), (57.6, "present"), (61.2, "finger_up"),
             (65.7, "present"), (69.6, "present"))
    exprs = ((0, "confident"), (2.6, "shocked"), (6.6, "confident"), (27.4, "shocked"), (30.0, "confident"), (41.5, "grin"),
             (43.2, "confident"), (47.4, "shocked"), (54.1, "confident"), (63.8, "shocked"), (65.7, "grin"))
    consultor_i(c, t, 540, 2250, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
