"""DÓLAR A R$ 6: O QUE FICA MAIS CARO NO SEU BOLSO (TikTok vertical, ~76 s, estilo ilustrado, conta útil das 18h).
1º item [18h] da Fila do Matheus (24/11/2026), sem o ângulo político (nada de eleição/governo).
Contas (contas.py): dólar R$ 4,99 em 23/10/2026 -> R$ 6,00 em 23/11/2026 (+20%); viagem US$ 1.000 + IOF 3,5%:
R$ 5.175 -> R$ 6.210 (+R$ 1.035); compra de US$ 40: R$ 200 -> R$ 240 antes dos impostos.
Gráfico: PTAX/fechamentos citados pela imprensa (23/10 4,99; 03/11 5,49; 10/11 5,58; 13/11 5,65; 16/11 5,73; 18/11 5,81; 19/11 5,87; 23/11 6,00)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (11.7, "tum"), (29.8, "tum"), (41.8, "tum"), (55.4, "soft_ding"), (64.6, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

C1, C2 = (540, 925), (540, 1012)
PAINEL = (0.10, 0.14, 0.26)
SERIE = [(0, 4.99), (11, 5.49), (18, 5.58), (21, 5.65), (24, 5.73), (26, 5.81), (27, 5.87), (31, 6.00)]


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


def placar(c, t):
    """placar do dólar no topo: conta de R$ 5,00 a R$ 6,00 no quadro 0 e fica."""
    rr(c, 90 + 8, 290 + 10, 900, 150, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 90, 290, 900, 150, 30); rgb(c, CREME); c.fill()
    text(c, "US$ 1 =", 250, 388, 56, MARKER, NAVY)
    contador(c, t, 0.0, 5.0, 6.0, 560, 360, 96, d=2.2, col=VERMELHO, casas=2)
    if t >= 0.6:
        k = max(0.01, ease_out(clamp01((t - 0.6) / 0.5)))
        c.save(); c.translate(850, 365); c.scale(k, k)
        c.move_to(-40, 30); c.line_to(0, -40); c.line_to(40, 30); c.close_path(); rgb(c, VERMELHO); c.fill()
        c.restore()
    if t >= 4.7:
        entra(c, t, 4.7, 870, 300, chip("+20%", VERMELHO, CREME, 44, 0.08), anim="stamp")


def grafico(c, t, a=1.0):
    x0, y0, w, h = 140, 520, 800, 270
    c.push_group()
    rr(c, 100, 480, 880, 390, 30); rgb(c, PAINEL); c.fill()
    text(c, "UM MÊS DE DÓLAR", 540, 540, 40, MARKER, CREME)
    for v in (5.0, 5.5, 6.0):
        y = y0 + h - (v - 4.9) / 1.2 * h + 20
        c.move_to(x0 + 60, y); c.line_to(x0 + w, y); rgb(c, CREME, 0.18); c.set_line_width(3); c.stroke()
        text(c, f"{v:.2f}".replace(".", ","), x0 + 20, y + 12, 30, MARKER, CREME, alpha=0.7)
    k = ease_out(clamp01(t / 3.0))
    pts = [(x0 + 80 + d / 31 * (w - 120), y0 + h - (v - 4.9) / 1.2 * h + 20) for d, v in SERIE]
    n = (len(pts) - 1) * k
    c.move_to(*pts[0])
    for i in range(1, len(pts)):
        if i <= n:
            c.line_to(*pts[i])
        else:
            f = n - (i - 1)
            if f > 0:
                px, py = pts[i - 1]; qx, qy = pts[i]
                c.line_to(px + (qx - px) * f, py + (qy - py) * f)
            break
    rgb(c, VERMELHO); c.set_line_width(12); c.set_line_cap(1); c.set_line_join(1); c.stroke()
    text(c, "23/10", pts[0][0], y0 + h + 50, 32, MARKER, CREME)
    if t >= 2.3:
        text(c, "23/11", pts[-1][0] - 20, y0 + h + 50, 32, MARKER, GOLD)
        c.new_sub_path(); c.arc(pts[-1][0], pts[-1][1], 18, 0, 6.283); rgb(c, GOLD); c.fill()
    c.pop_group_to_source(); c.paint_with_alpha(a)


def comparacao(c, t, t_titulo, titulo, t_a, va, sub_a, t_h, vh, sub_h, t_dif=None, dif=""):
    """dois cartões: um mês atrás x hoje."""
    rr(c, 100, 480, 880, 80, 24); rgb(c, GOLD); c.fill()
    text(c, titulo, 540, 536, 48, MARKER, TINTA)
    for i, (t0, v, sub, lab, cor) in enumerate(((t_a, va, sub_a, "UM MÊS ATRÁS", CREME), (t_h, vh, sub_h, "HOJE", VERMELHO))):
        x = 100 + i * 450
        rr(c, x, 580, 430, 250, 26); rgb(c, PAINEL); c.fill()
        text(c, lab, x + 215, 640, 40, MARKER, CREME if i == 0 else (1.0, 0.72, 0.66))
        if t < t0:
            text(c, "...", x + 215, 740, 70, MARKER, CREME, alpha=0.6)
            continue
        entra(c, t, t0, x + 215, 720, lambda cc, v=v, cor=cor: numero_i(cc, v, 0, 0, 74, cor), anim="pop")
        if sub:
            text(c, sub, x + 215, 800, 32, MARKER, CREME, alpha=0.85)
    if t_dif is not None and t >= t_dif:
        entra(c, t, t_dif, 540, 905, chip(dif, VERMELHO, CREME, 56, -0.03), anim="stamp")


def linha_devagar(c, t, t0, y, nome, porque):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.45))
    c.save(); c.translate((1 - k) * -900, 0)
    rr(c, 100, y - 60, 880, 120, 24); rgb(c, CREME); c.fill()
    c.new_sub_path(); c.arc(170, y, 38, 0, 6.283); rgb(c, VERMELHO); c.fill()
    c.move_to(150, y + 14); c.line_to(170, y - 16); c.line_to(190, y + 14); c.close_path(); rgb(c, CREME); c.fill()
    text(c, nome, 235, y - 6, 44, MARKER, TINTA, align="l")
    text(c, porque, 235, y + 40, 32, MARKER, NAVY, align="l")
    c.restore()


def painel(c, t):
    if t < 11.7:
        a = 1.0 if t < 11.2 else max(0.0, 1 - (t - 11.2) / 0.5)
        grafico(c, t, a)
        if 7.0 <= t < 11.4:
            entra(c, t, 8.0, *C1, chip("O QUE FICA MAIS CARO?", GOLD, TINTA, 50), anim="stamp")
            if t >= 10.6:
                entra(c, t, 10.6, *C2, chip("faz a conta comigo", CREME, TINTA, 42), anim="pop")
        return
    if t < 29.8:
        sub_a = "+ IOF 3,5%" if t >= 17.0 else ""
        comparacao(c, t, 12.4, "VIAGEM: US$ 1.000", 15.7, "R$ 5.000" if t < 19.3 else "R$ 5.175", sub_a,
                   22.0, "R$ 6.210", "com IOF" if t >= 22.0 else "", 24.0, "+R$ 1.035")
        if t >= 26.1 and t < 27.5:
            entra(c, t, 26.1, *C2, chip("mesma viagem", CREME, TINTA, 42), anim="pop")
        if t >= 27.7:
            entra(c, t, 27.7, *C2, chip("e antes da taxa do banco", CREME, TINTA, 40), anim="pop")
        return
    if t < 41.8:
        comparacao(c, t, 30.6, "COMPRINHA: US$ 40", 34.2, "R$ 200", "", 36.1, "R$ 240", "antes dos impostos" if t >= 37.4 else "",
                   36.8, "+R$ 40")
        if t >= 39.2:
            entra(c, t, 39.2, *C2, chip("imposto em cima do valor maior", CREME, TINTA, 36), anim="pop")
        return
    if t < 55.4:
        rr(c, 100, 480, 880, 80, 24); rgb(c, GOLD); c.fill()
        text(c, "O QUE CHEGA DEVAGAR", 540, 536, 48, MARKER, TINTA)
        linha_devagar(c, t, 44.1, 640, "GASOLINA E DIESEL", "petróleo é cotado em dólar")
        linha_devagar(c, t, 47.7, 780, "PÃO, MACARRÃO, BISCOITO", "boa parte do trigo vem de fora")
        linha_devagar(c, t, 52.0, 920, "CELULAR E ELETRÔNICO", "peças importadas")
        return
    if t < 64.6:
        entra(c, t, 55.4, 540, 560, chip("A VIRADA", GOLD, TINTA, 56), anim="stamp")
        if t >= 56.4:
            k = 1 + 0.08 * math.sin(clamp01((t - 57.0) / 0.35) * math.pi)
            c.save(); c.translate(540, 700); c.scale(k, k)
            rr(c, -430, -70, 860, 140, 30); rgb(c, PAINEL); c.fill()
            text(c, "NÃO SOBE 20% AMANHÃ", 0, 24, 62, MARKER, CREME)
            c.restore()
        if 58.9 <= t < 61.9:
            entra(c, t, 59.4, 300, 870, chip("estoque", CREME, TINTA, 46, -0.04), anim="left")
            if t >= 60.2:
                entra(c, t, 60.2, 780, 870, chip("contrato", CREME, TINTA, 46, 0.04), anim="right")
        if t >= 61.9:
            entra(c, t, 61.9, 540, 880, chip("O QUE PESA: O TEMPO", VERMELHO, CREME, 50), anim="stamp")
        return
    if t < 72.6:
        rr(c, 100, 480, 880, 80, 24); rgb(c, GOLD); c.fill()
        text(c, "COMPRA EM DÓLAR?", 540, 536, 50, MARKER, TINTA)
        if t >= 67.5:
            rr(c, 140, 600, 800, 110, 24); rgb(c, PAINEL); c.fill()
            text(c, "TUDO NUM DIA SÓ", 540, 676, 54, MARKER, CREME)
            if t >= 68.4:
                k = max(0.01, ease_out(clamp01((t - 68.4) / 0.3)))
                c.move_to(160, 640); c.line_to(160 + 760 * k, 640 + 40 * k)
                rgb(c, VERMELHO); c.set_line_width(14); c.stroke()
        if t >= 69.6:
            for i in range(4):
                if t >= 69.6 + i * 0.25:
                    entra(c, t, 69.6 + i * 0.25, 230 + i * 207, 800, chip("1/4", VERDE, CREME, 52), anim="drop")
        if t >= 71.0:
            entra(c, t, 71.0, 540, 925, chip("PREÇO NA MÉDIA", GOLD, TINTA, 48), anim="stamp")
        return
    entra(c, t, 72.6, 540, 640, chip("E VOCÊ?", GOLD, TINTA, 60), anim="stamp")
    if t >= 73.0:
        entra(c, t, 73.0, 540, 790, chip("tem conta em dólar pra pagar?", CREME, TINTA, 42), anim="pop")
    if t >= 74.6:
        entra(c, t, 74.6, 540, 920, chip("COMENTA AÍ", VERDE, CREME, 50), anim="stamp")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "DÓLAR A R$ 6 NO SEU BOLSO", 540, 235, 56, CREME)
    placar(c, t)
    painel(c, t)
    poses = ((0, "shrug"), (2.3, "point_r"), (4.7, "head"), (6.4, "finger_up"), (8.0, "present"), (10.6, "finger_up"),
             (11.7, "finger_up"), (13.2, "present"), (17.0, "point_r"), (21.4, "finger_up"), (24.0, "head"), (27.5, "shrug"),
             (29.8, "finger_up"), (32.0, "present"), (36.1, "point_r"), (39.0, "finger_up"), (41.8, "finger_up"),
             (44.1, "present"), (47.7, "point_r"), (52.0, "present"), (55.4, "arms_up"), (56.4, "finger_up"), (58.7, "present"),
             (61.0, "finger_up"), (64.6, "present"), (67.5, "shrug"), (69.6, "finger_up"), (71.0, "arms_up"), (72.6, "present"))
    exprs = ((0, "shocked"), (2.3, "think"), (6.4, "confident"), (11.7, "confident"), (24.0, "shocked"), (27.5, "think"),
             (29.8, "confident"), (36.1, "shocked"), (39.0, "think"), (41.8, "confident"), (55.4, "grin"), (58.7, "confident"),
             (67.5, "think"), (69.6, "confident"), (71.0, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)


SCENES = [(0, 999.0, cena)]
