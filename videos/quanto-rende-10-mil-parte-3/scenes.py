"""QUANTO RENDE R$ 10 MIL EM 1 ANO (Parte 3 de 3): conta x poupança x Tesouro Selic x CDB 100% x CDB 110% + por mês
+ a virada da série (mesma %, bolo maior) + quanto precisa pra render 1 salário mínimo/mês (TikTok vertical, ~82 s).
Mesmas taxas das Partes 1 e 2 (19/11/2026): Selic 13,75%, CDI 13,65%, poupança 0,6638% a.m.
Contas (contas.py): poupança R$ 10.826 (isenta); Tesouro Selic/CDB 100%: bruto R$ 1.365, IR 17,5% R$ 239 -> R$ 11.126;
CDB 110%: R$ 11.239. Por mês ~R$ 94 x ~R$ 69 (R$ 300/ano). 1 mínimo (R$ 1.621) por mês com IR 15%: ~R$ 167.700 ("quase 170 mil")."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (17.2, "tum"), (29.2, "tum"), (35.5, "soft_ding"), (49.0, "tum"), (68.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

# nome, valor líquido, início do destaque, quando a barra cresce, fim do destaque
LINHAS = [("CONTA", 0, 0.0, 0.0, 10.9), ("POUPANÇA", 826, 16.4, 17.2, 20.9), ("TESOURO SELIC", 1126, 20.9, 24.3, 33.2),
          ("CDB 100% CDI", 1126, 20.9, 24.3, 33.2), ("CDB 110% CDI", 1239, 33.2, 35.5, 38.0)]
X0, WMAX, VMAX = 400, 420, 1400.0
L1, L2, R1, R2 = (275, 968), (275, 1062), (775, 968), (775, 1062)
C1, C2, CM = (540, 968), (540, 1060), (540, 1010)
AZUL = (0.55, 0.72, 0.90)


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
    if i in (2, 3):  # sobe ao bruto, depois o IR come um pedaço
        if t < tg:
            return 0.0
        if t < 29.2:
            return 1365.0 * ease_out(clamp01((t - tg) / 0.9))
        return 1365.0 - 239.0 * ease_out(clamp01((t - 29.2) / 0.7))
    if i == 0 or t < tg:
        return 0.0
    return v * ease_out(clamp01((t - tg) / 0.9))


def destaque(i, t):
    if 38.0 <= t < 42.6:
        return i == 3
    if 42.6 <= t < 45.0:
        return i == 1
    if 45.0 <= t < 49.0:
        return i in (1, 3)
    if 49.0 <= t < 61.3:
        return i == 3
    nome, v, th, tg, tf = LINHAS[i]
    return th <= t < tf


def tabela(c, t):
    rr(c, 60 + 8, 290 + 10, 870, 470, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 60, 290, 870, 470, 30); rgb(c, CREME); c.fill()
    text(c, "R$ 10.000 POR 1 ANO, JÁ SEM IMPOSTO", 495, 340, 34, MARKER, NAVY)
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
        if i in (2, 3) and 29.2 <= t:
            wb = WMAX * 1365.0 / VMAX
            a = max(0.0, 1 - (t - 30.8) / 1.0) if t > 30.8 else 1.0
            if a > 0:
                rr(c, X0, y - 26, wb, 52, 12); rgb(c, VERMELHO, 0.45 * a); c.fill()
        rr(c, X0, y - 26, w, 52, 12); rgb(c, cor); c.fill()
        s = ("bruto " + brl(vv)) if (i in (2, 3) and t < 29.2) else ("+" + brl(vv))
        text(c, s, X0 + w - 12, y + 9, 38, MARKER, CREME, align="r") if w > 210 else \
            text(c, s, X0 + w + 10, y + 9, 36, MARKER, TINTA, align="l")


def bloco_ouro(c, t, t0, s, size=64):
    k = 1 + 0.12 * math.sin(clamp01((t - t0) / 0.35) * math.pi)
    c.save(); c.translate(540, 850); c.scale(k, k)
    rr(c, -410, -70, 820, 140, 30); rgb(c, GOLD); c.fill()
    text(c, s, 0, 26, size, MARKER, TINTA)
    c.restore()


def marcador(c, t):
    if 68.9 <= t < 73.6:
        bloco_ouro(c, t, 68.9, "QUASE R$ 170 MIL")
        return
    rr(c, 150, 790, 780, 120, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=42):
        text(c, s, 330, 866, size, MARKER, CREME)
    if t < 16.4:
        lab("NA CONTA", 46)
        contador(c, t, 0.0, 0, 10000, 690, 850, 80, d=1.6, col=CREME)
        return
    if t < 38.0:
        lab("VIRA", 50)
        if t < 17.2:
            numero_i(c, "R$ 10.000", 690, 878, 80, CREME)
        elif t < 30.8:
            contador(c, t, 17.2, 10000, 10826, 690, 850, 80, d=0.9, col=AZUL)
        elif t < 35.5:
            contador(c, t, 30.8, 10826, 11126, 690, 850, 80, d=0.7, col=VERDE)
        else:
            contador(c, t, 35.5, 11126, 11239, 690, 850, 80, d=0.7, col=GOLD)
        return
    if t < 42.6:
        lab("CDB 100% / MÊS", 36)
        if t >= 40.8:
            contador(c, t, 40.8, 0, 94, 700, 850, 84, d=0.8, col=VERDE)
        else:
            numero_i(c, "...", 700, 878, 72, CREME)
        return
    if t < 45.0:
        lab("POUPANÇA / MÊS", 36)
        if t >= 43.8:
            numero_i(c, "R$ 69", 700, 878, 84, AZUL)
        else:
            numero_i(c, "...", 700, 878, 72, CREME)
        return
    if t < 49.0:
        lab("DIFERENÇA / ANO", 34)
        contador(c, t, 45.0, 0, 300, 700, 850, 84, d=0.8, col=GOLD)
        return
    if t < 61.3:
        if t < 53.0:
            lab("R$ 1 MIL RENDEU", 34); contador(c, t, 51.3, 0, 113, 700, 850, 80, d=0.7, col=VERDE) if t >= 51.3 else numero_i(c, "...", 700, 878, 72, CREME)
        elif t < 55.5:
            lab("R$ 5 MIL RENDEU", 34); contador(c, t, 53.8, 113, 563, 700, 850, 80, d=0.7, col=VERDE) if t >= 53.8 else numero_i(c, "R$ 113", 700, 878, 80, VERDE)
        elif t < 57.9:
            lab("R$ 10 MIL RENDEU", 32); contador(c, t, 55.9, 563, 1126, 700, 850, 80, d=0.8, col=VERDE) if t >= 55.9 else numero_i(c, "R$ 563", 700, 878, 80, VERDE)
        else:
            lab("SEMPRE", 46); numero_i(c, "11,3%", 700, 878, 84, GOLD)
        return
    if t < 68.9:
        lab("1 MÍNIMO / MÊS", 36)
        if t >= 63.0:
            numero_i(c, "R$ 1.621", 700, 878, 80, VERDE)
        else:
            numero_i(c, "...", 700, 878, 72, CREME)
        return
    if t < 78.9:
        lab("SELIC HOJE", 40); numero_i(c, "13,75%", 700, 878, 80, GOLD)
        return
    lab("FIM DA SÉRIE", 38); numero_i(c, "3 DE 3", 700, 878, 80, GOLD)


def detalhes(c, t):
    if 2.4 <= t < 8.0:
        entra(c, t, 2.4, *C1, chip("+ R$ 0,00 em 1 ano", VERMELHO, CREME, 48, -0.02), anim="stamp")
    if 6.5 <= t < 8.0:
        entra(c, t, 6.5, *C2, chip("já tirando o imposto", CREME, TINTA, 44, 0.02), anim="pop")
    if 8.0 <= t < 10.9:
        entra(c, t, 8.0, *C1, chip("PARTE 3: A ÚLTIMA", GOLD, TINTA, 52), anim="stamp")
        if t >= 10.1:
            entra(c, t, 10.1, *C2, chip("SALVA A TABELA", CREME, TINTA, 48), anim="pop")
    if 10.9 <= t < 16.4:
        entra(c, t, 11.2, *L1, chip("Selic 13,75%", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 13.4, *R1, chip("CDI 13,65%", GOLD, TINTA, 46, 0.04), anim="right")
        entra(c, t, 15.4, *C2, chip("ao ano", CREME, TINTA, 42), anim="pop")
    if 16.4 <= t < 20.9:
        entra(c, t, 17.2, *C1, chip("+ R$ 826", VERDE, CREME, 50), anim="stamp")
        if t >= 19.8:
            entra(c, t, 19.8, *C2, chip("SEM IMPOSTO", VERDE, CREME, 48), anim="stamp")
    if 20.9 <= t < 33.2:
        entra(c, t, 21.0, *L1, chip("Tesouro Selic", CREME, TINTA, 42, -0.04), anim="left")
        entra(c, t, 21.8, *R1, chip("= CDB 100%", CREME, TINTA, 44, 0.04), anim="right")
    if 27.1 <= t < 33.2:
        entra(c, t, 27.3, *L2, chip("IR 17,5%", VERMELHO, CREME, 44, 0.03), anim="stamp")
    if 29.2 <= t < 33.2:
        entra(c, t, 29.3, *R2, chip("sobra R$ 1.126", VERDE, CREME, 42, -0.03), anim="right")
    if 33.2 <= t < 38.0:
        entra(c, t, 33.4, *C1, chip("110% do CDI", CREME, TINTA, 46), anim="pop")
        entra(c, t, 35.5, *C2, chip("R$ 11.239", GOLD, TINTA, 54), anim="stamp")
    if 38.0 <= t < 45.0:
        entra(c, t, 38.1, *C1, chip("POR MÊS", GOLD, TINTA, 52), anim="stamp")
        if t >= 43.8:
            entra(c, t, 43.8, *C2, chip("poupança: R$ 69", (0.45, 0.62, 0.80), CREME, 44), anim="pop")
    if 45.0 <= t < 49.0:
        entra(c, t, 45.1, *C1, chip("R$ 300 POR ANO", VERDE, CREME, 50), anim="stamp")
        if t >= 47.3:
            entra(c, t, 47.3, *C2, chip("só de trocar de lugar", CREME, TINTA, 42), anim="pop")
    if 49.0 <= t < 57.9:
        if t < 50.5:
            entra(c, t, 49.1, *C1, chip("A VIRADA DA SÉRIE", VERMELHO, CREME, 50), anim="stamp")
        if t >= 50.5:
            entra(c, t, 50.5, *L1, chip("R$ 1 mil: +113", CREME, TINTA, 40, -0.04), anim="left")
        if t >= 53.0:
            entra(c, t, 53.0, *R1, chip("R$ 5 mil: +563", CREME, TINTA, 40, 0.04), anim="right")
        if t >= 55.5:
            entra(c, t, 55.5, *C2, chip("R$ 10 mil: +1.126", VERDE, CREME, 44), anim="stamp")
    if 57.9 <= t < 61.3:
        entra(c, t, 57.9, *C1, chip("A % É A MESMA", GOLD, TINTA, 50), anim="stamp")
        if t >= 59.4:
            entra(c, t, 59.4, *C2, chip("muda o tamanho do bolo", CREME, TINTA, 40), anim="pop")
    if 61.3 <= t < 68.9:
        entra(c, t, 61.4, *C1, chip("quanto precisa?", CREME, TINTA, 46), anim="pop")
        if t >= 64.8:
            entra(c, t, 64.8, *L2, chip("CDI 13,65%", CREME, TINTA, 40, 0.03), anim="left")
        if t >= 66.1:
            entra(c, t, 66.1, *R2, chip("IR 15% (2+ anos)", CREME, TINTA, 36, -0.03), anim="right")
    if 68.9 <= t < 73.6:
        entra(c, t, 69.2, *C1, chip("pra render 1 mínimo/mês", CREME, TINTA, 40), anim="pop")
        if t >= 71.2:
            entra(c, t, 71.2, *C2, chip("seus R$ 10 mil: 1º degrau", VERDE, CREME, 40), anim="stamp")
    if 73.6 <= t < 78.9:
        entra(c, t, 73.7, *C1, chip("AS TAXAS MUDAM", VERMELHO, CREME, 50), anim="stamp")
        if t >= 75.1:
            entra(c, t, 75.1, *C2, chip("Selic caindo em 2027?", CREME, TINTA, 42), anim="pop")
    if t >= 78.9:
        entra(c, t, 78.9, *CM, chip("QUAL NÚMERO TE SURPREENDEU?", GOLD, TINTA, 42), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANTO RENDE R$ 10 MIL (PARTE 3)", 540, 235, 44, CREME)
    tabela(c, t)
    marcador(c, t)
    poses = ((0, "present"), (2.4, "shrug"), (6.5, "finger_up"), (8.0, "present"), (10.9, "finger_up"), (16.4, "point_r"),
             (20.9, "point_r"), (27.1, "finger_up"), (29.2, "present"), (33.2, "point_r"), (35.5, "arms_up"),
             (38.0, "finger_up"), (40.8, "present"), (42.6, "shrug"), (45.0, "point_r"), (49.0, "finger_up"),
             (51.3, "present"), (55.9, "arms_up"), (57.9, "finger_up"), (61.3, "head"), (64.8, "finger_up"),
             (68.9, "arms_up"), (71.2, "present"), (73.6, "finger_up"), (78.9, "present"))
    exprs = ((0, "confident"), (2.4, "shocked"), (6.5, "confident"), (27.1, "shocked"), (29.2, "confident"), (35.5, "grin"),
             (38.0, "confident"), (40.8, "grin"), (42.6, "think"), (45.0, "confident"), (55.9, "grin"), (57.9, "confident"),
             (61.3, "think"), (68.9, "shocked"), (71.2, "grin"), (73.6, "confident"), (78.9, "grin"))
    consultor_i(c, t, 540, 2250, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
