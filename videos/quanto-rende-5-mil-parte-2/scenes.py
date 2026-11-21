"""QUANTO RENDE R$ 5 MIL EM 1 ANO (Parte 2): conta x poupança x Tesouro Selic x CDB 100% x CDB 110% + por mês + 5 anos
(TikTok vertical, ~84 s). Mesmas taxas da Parte 1 (19/11/2026): Selic 13,75% (Copom 04/11/2026), CDI 13,65%, poupança 0,6638% a.m.
Contas (contas.py): poupança R$ 5.413 (+413, isenta); Tesouro Selic/CDB 100%: bruto R$ 682,50, IR 17,5% R$ 119 -> R$ 5.563;
CDB 110%: R$ 5.619. Por mês: CDB 100% ~R$ 47, poupança ~R$ 34. 5 anos com taxas iguais (IR 15% no resgate):
poupança ~R$ 7.437, CDB 100% ~R$ 8.808 -> ~R$ 1.370 ("quase mil e quatrocentos"). Parte 3 prometida: R$ 10 mil."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (16.9, "tum"), (29.3, "tum"), (42.8, "soft_ding"), (55.0, "tum"), (66.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

# nome, valor líquido, início do destaque, quando a barra cresce, fim do destaque
LINHAS = [("CONTA", 0, 0.0, 0.0, 9.0), ("POUPANÇA", 413, 15.9, 16.9, 23.2), ("TESOURO SELIC", 563, 23.2, 25.0, 34.2),
          ("CDB 100% CDI", 563, 34.2, 37.8, 40.5), ("CDB 110% CDI", 619, 40.5, 42.8, 45.3)]
X0, WMAX, VMAX = 400, 420, 700.0
L1, L2, R1, R2 = (275, 968), (275, 1062), (775, 968), (775, 1062)
C1, C2, CM = (540, 968), (540, 1060), (540, 1010)


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
        if t < 29.3:
            return 682.5 * ease_out(clamp01((t - tg) / 0.9))
        return 682.5 - 119.5 * ease_out(clamp01((t - 29.3) / 0.7))
    if i == 0 or t < tg:
        return 0.0
    return v * ease_out(clamp01((t - tg) / 0.9))


def destaque(i, t):
    if 45.3 <= t < 52.7:
        return i == 3
    if 52.7 <= t < 55.0:
        return i == 1
    if 55.0 <= t < 70.2:
        return i in (1, 3)
    nome, v, th, tg, tf = LINHAS[i]
    return th <= t < tf


def tabela(c, t):
    rr(c, 60 + 8, 290 + 10, 870, 470, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 60, 290, 870, 470, 30); rgb(c, CREME); c.fill()
    text(c, "R$ 5.000 POR 1 ANO, JÁ SEM IMPOSTO", 495, 340, 34, MARKER, NAVY)
    for i, (nome, v, th, tg, tf) in enumerate(LINHAS):
        y = 402 + i * 76
        if destaque(i, t):
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
        if i == 2 and 29.3 <= t:
            wb = WMAX * 682.5 / VMAX
            a = max(0.0, 1 - (t - 30.9) / 1.0) if t > 30.9 else 1.0
            if a > 0:
                rr(c, X0, y - 26, wb, 52, 12); rgb(c, VERMELHO, 0.45 * a); c.fill()
        rr(c, X0, y - 26, w, 52, 12); rgb(c, cor); c.fill()
        s = ("bruto " + brl(vv)) if (i == 2 and t < 29.3) else ("+" + brl(vv))
        text(c, s, X0 + w - 12, y + 9, 38, MARKER, CREME, align="r") if w > 190 else \
            text(c, s, X0 + w + 10, y + 9, 36, MARKER, TINTA, align="l")


def marcador(c, t):
    if 66.2 <= t < 70.2:
        k = 1 + 0.12 * math.sin(clamp01((t - 66.2) / 0.35) * math.pi)
        c.save(); c.translate(540, 850); c.scale(k, k)
        rr(c, -400, -70, 800, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "QUASE R$ 1.400 A MAIS", 0, 26, 64, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, 790, 780, 120, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=42):
        text(c, s, 330, 866, size, MARKER, CREME)
    if t < 15.9:
        lab("NA CONTA", 46)
        contador(c, t, 0.0, 0, 5000, 690, 850, 80, d=1.6, col=CREME)
        return
    if t < 45.3:
        lab("VIRA", 50)
        if t < 16.9:
            numero_i(c, "R$ 5.000", 690, 878, 84, CREME)
        elif t < 30.9:
            contador(c, t, 16.9, 5000, 5413, 690, 850, 84, d=0.9, col=VERDE)
        elif t < 42.8:
            contador(c, t, 30.9, 5413, 5563, 690, 850, 84, d=0.7, col=VERDE)
        else:
            contador(c, t, 42.8, 5563, 5619, 690, 850, 84, d=0.7, col=GOLD)
        return
    if t < 52.7:
        lab("CDB 100% / MÊS", 36)
        if t >= 48.9:
            contador(c, t, 48.9, 0, 47, 700, 850, 84, d=0.8, col=VERDE)
        else:
            numero_i(c, "...", 700, 878, 72, CREME)
        return
    if t < 55.0:
        lab("POUPANÇA / MÊS", 36)
        if t >= 53.7:
            numero_i(c, "R$ 34", 700, 878, 84, (0.55, 0.72, 0.90))
        else:
            numero_i(c, "...", 700, 878, 72, CREME)
        return
    if t < 62.6:
        lab("POUPANÇA 5 ANOS" if t >= 59.5 else "EM 5 ANOS", 34)
        if t >= 61.0:
            contador(c, t, 61.0, 5000, 7400, 700, 850, 80, d=0.9, col=(0.55, 0.72, 0.90))
        else:
            numero_i(c, "R$ 5.000", 700, 878, 80, CREME)
        return
    if t < 66.2:
        lab("CDB 100% 5 ANOS", 34)
        if t >= 64.7:
            contador(c, t, 64.7, 5000, 8800, 700, 850, 80, d=0.9, col=VERDE)
        else:
            numero_i(c, "R$ 7.400", 700, 878, 80, (0.55, 0.72, 0.90))
        return
    if t < 77.8:
        lab("IR EM 1 ANO" if t < 74.9 else "IR APÓS 2 ANOS", 36)
        numero_i(c, "17,5%" if t < 74.9 else "15%", 700, 878, 84, VERMELHO if t < 74.9 else VERDE)
        return
    lab("PARTE 3", 46)
    numero_i(c, "R$ 10 MIL", 700, 878, 80, GOLD)


def detalhes(c, t):
    if 2.4 <= t < 7.8:
        entra(c, t, 2.4, *C1, chip("+ R$ 0,00 em 1 ano", VERMELHO, CREME, 48, -0.02), anim="stamp")
    if 6.3 <= t < 7.8:
        entra(c, t, 6.3, *C2, chip("já tirando o imposto", CREME, TINTA, 44, 0.02), anim="pop")
    if 7.8 <= t < 10.2:
        entra(c, t, 7.8, *C1, chip("PARTE 2", GOLD, TINTA, 54), anim="stamp")
        if t >= 9.0:
            entra(c, t, 9.0, *C2, chip("SALVA A TABELA", CREME, TINTA, 48), anim="pop")
    if 10.2 <= t < 15.9:
        entra(c, t, 10.4, *L1, chip("Selic 13,75%", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 12.5, *R1, chip("CDI 13,65%", GOLD, TINTA, 46, 0.04), anim="right")
        entra(c, t, 15.0, *C2, chip("ao ano", CREME, TINTA, 42), anim="pop")
    if 15.9 <= t < 23.2:
        entra(c, t, 16.9, *C1, chip("0,66% ao mês", CREME, TINTA, 46), anim="pop")
        entra(c, t, 19.4, *C2, chip("+ R$ 413", VERDE, CREME, 48), anim="stamp") if t < 21.5 else \
            entra(c, t, 21.5, *C2, chip("SEM IMPOSTO", VERDE, CREME, 48), anim="stamp")
    if 23.2 <= t < 34.2:
        entra(c, t, 25.0, *L1, chip("bruto R$ 682", CREME, TINTA, 44, -0.04), anim="left")
    if 27.3 <= t < 34.2:
        entra(c, t, 27.3, *R1, chip("IR 17,5%", VERMELHO, CREME, 46, 0.04), anim="stamp")
    if 29.3 <= t < 34.2:
        entra(c, t, 29.3, *L2, chip("- R$ 119", VERMELHO, CREME, 46, 0.03), anim="left")
        entra(c, t, 29.7, *R2, chip("sobra R$ 563", VERDE, CREME, 44, -0.03), anim="right")
    if 34.2 <= t < 40.5:
        entra(c, t, 36.6, *C1, chip("a mesma conta", CREME, TINTA, 46), anim="pop")
        entra(c, t, 37.8, *C2, chip("R$ 5.563", VERDE, CREME, 52), anim="stamp")
    if 40.5 <= t < 45.3:
        entra(c, t, 41.0, *C1, chip("110% do CDI", CREME, TINTA, 46), anim="pop")
        entra(c, t, 42.8, *C2, chip("R$ 5.619", GOLD, TINTA, 54), anim="stamp")
    if 45.3 <= t < 55.0:
        entra(c, t, 45.6, *C1, chip("POR MÊS", GOLD, TINTA, 52), anim="stamp")
        if 50.2 <= t < 52.7:
            entra(c, t, 50.2, *C2, chip("sem fazer nada", CREME, TINTA, 44), anim="pop")
        if t >= 53.7:
            entra(c, t, 53.7, *C2, chip("poupança: R$ 34", (0.45, 0.62, 0.80), CREME, 44), anim="pop")
    if 55.0 <= t < 66.2:
        entra(c, t, 55.1, *C1, chip("A VIRADA: O TEMPO", VERMELHO, CREME, 50), anim="stamp")
        if t >= 56.7:
            entra(c, t, 56.7, *C2, chip("taxas iguais por 5 anos", CREME, TINTA, 40), anim="pop")
    if 66.2 <= t < 70.2:
        entra(c, t, 66.6, *C1, chip("R$ 7.400 x R$ 8.800", CREME, TINTA, 46), anim="pop")
        if t >= 68.7:
            entra(c, t, 68.7, *C2, chip("o mesmo dinheiro", GOLD, TINTA, 46), anim="pop")
    if 70.2 <= t < 77.8:
        entra(c, t, 71.7, *L1, chip("IR só no resgate", CREME, TINTA, 38, -0.04), anim="left")
        if t >= 73.6:
            entra(c, t, 73.6, *R1, chip("cai com o tempo", GOLD, TINTA, 40, 0.04), anim="right")
        if t >= 74.9:
            entra(c, t, 75.3, *C2, chip("2 anos: 15%", VERDE, CREME, 48), anim="stamp")
    if 77.8 <= t < 80.6:
        entra(c, t, 78.0, *C1, chip("PARTE 3: R$ 10 MIL", GOLD, TINTA, 52), anim="stamp")
    if t >= 80.6:
        entra(c, t, 80.6, *CM, chip("DEIXARIA OS R$ 5 MIL ONDE?", GOLD, TINTA, 44), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANTO RENDE R$ 5 MIL (PARTE 2)", 540, 235, 50, CREME)
    tabela(c, t)
    marcador(c, t)
    poses = ((0, "present"), (2.4, "shrug"), (6.3, "finger_up"), (9.0, "present"), (10.2, "finger_up"), (15.9, "point_r"),
             (21.5, "present"), (23.2, "point_r"), (27.3, "finger_up"), (29.3, "present"), (34.2, "point_r"), (40.5, "point_r"),
             (42.8, "arms_up"), (45.3, "finger_up"), (48.9, "present"), (52.7, "shrug"), (55.0, "finger_up"), (61.0, "point_r"),
             (64.7, "arms_up"), (66.2, "finger_up"), (70.2, "finger_up"), (74.9, "present"), (77.8, "present"), (80.6, "present"))
    exprs = ((0, "confident"), (2.4, "shocked"), (6.3, "confident"), (27.3, "shocked"), (29.3, "confident"), (42.8, "grin"),
             (45.3, "confident"), (48.9, "grin"), (52.7, "think"), (55.0, "confident"), (64.7, "grin"), (66.2, "shocked"),
             (70.2, "confident"), (77.8, "grin"))
    consultor_i(c, t, 540, 2250, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
