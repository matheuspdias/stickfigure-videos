"""DESAFIO DO CASAL 2027 · R$ 10 mil em 12 meses, em 3 degraus (TikTok vertical, ~75 s, estilo ilustrado).
Modelado no formato que viralizou ("Desafio financeiro em casal para 2027", 3,3 mi): a tabela mês a mês na tela.
Mesma estrutura do Checklist (cena fixa, Consultor grande, tabela vazia no quadro 0 preenchida com a fala).
Contas em contas.py: 4x600 + 4x800 + 4x1.100 = 10.000; 100% do CDI (13,65%) ~R$ 505 líquidos -> ~R$ 10.500."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (20.6, "tum"), (25.0, "tum"), (29.3, "tum"), (42.6, "soft_ding"), (54.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

MESES = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
VALOR = [600] * 4 + [800] * 4 + [1100] * 4
T_DEGRAU = [20.6, 25.0, 29.3]          # quando cada degrau é preenchido
TINT = [CREME, (0.99, 0.86, 0.55), (0.70, 0.90, 0.72)]


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


def brl0(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def tabela(c, t):
    rr(c, 60 + 8, 290 + 10, 860, 440, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 60, 290, 860, 440, 30); rgb(c, CREME); c.fill()
    for i, (m, v) in enumerate(zip(MESES, VALOR)):
        col, lin = divmod(i, 6)
        x0, y = 80 + col * 420, 345 + lin * 68
        deg = i // 4
        t0 = T_DEGRAU[deg] + (i % 4) * 0.15
        # janeiro pisca em vermelho enquanto fala do mês apertado
        if i == 0 and 9.6 <= t < 16.6:
            rr(c, x0, y - 30, 400, 60, 14); rgb(c, VERMELHO, 0.35 + 0.15 * math.sin(t * 6)); c.fill()
        if t >= t0:
            k = ease_out(clamp01((t - t0) / 0.35))
            rr(c, x0, y - 30, 400 * k, 60, 14); rgb(c, TINT[deg]); c.fill()
        text(c, m, x0 + 20, y + 16, 44, MARKER, NAVY, align="l")
        if t < t0:
            c.move_to(x0 + 150, y + 14); c.line_to(x0 + 380, y + 14); rgb(c, TINTA, 0.25); c.set_line_width(4)
            c.set_dash([12, 10]); c.stroke(); c.set_dash([])
        else:
            text(c, brl0(v), x0 + 380, y + 16, 44, MARKER, TINTA, align="r")
    c.move_to(490, 310); c.line_to(490, 712); rgb(c, TINTA, 0.15); c.set_line_width(3); c.stroke()


def marcador(c, t):
    yc = 805
    if t >= 68.2:
        k = 1 + 0.12 * math.sin(clamp01((t - 68.2) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -360, -70, 720, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "DEZ/27: ~R$ 10.500", 0, 28, 72, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    if t < 19.3:
        text(c, "META", 270, yc + 22, 46, MARKER, CREME)
        contador(c, t, 0.2, 0, 10000, 640, yc, 84, d=1.3, col=VERDE)
    elif t < 44.3:
        text(c, "GUARDADO", 300, yc + 20, 40, MARKER, CREME)
        if t < T_DEGRAU[0]:
            contador(c, t, 19.3, 0, 0, 660, yc, 84, d=0.1, col=GOLD)
        elif t < T_DEGRAU[1]:
            contador(c, t, T_DEGRAU[0], 0, 2400, 660, yc, 84, d=0.8, col=GOLD)
        elif t < T_DEGRAU[2]:
            contador(c, t, T_DEGRAU[1], 2400, 5600, 660, yc, 84, d=0.8, col=GOLD)
        else:
            contador(c, t, T_DEGRAU[2], 5600, 10000, 660, yc, 84, d=0.8, col=VERDE)
    else:
        text(c, "COM CDI", 290, yc + 20, 42, MARKER, CREME)
        if t < 52.1:
            contador(c, t, 44.3, 10000, 10000, 660, yc, 84, d=0.1, col=VERDE)
        else:
            contador(c, t, 52.1, 10000, 10500, 660, yc, 84, d=2.4, col=GOLD)


def detalhes(c, t):
    # gancho: os dois guardando juntos
    if 0.8 <= t < 7.3:
        entra(c, t, 0.8, 230, 990, chip("ELE + ELA", NAVY, CREME, 48, -0.04), anim="left")
        entra(c, t, 4.1, 800, 990, chip("SALVA E MANDA", VERMELHO, CREME, 42, 0.04), anim="stamp")
    # janeiro apertado
    if 12.0 <= t < 16.6:
        for t0, s_, x, y, r in ((12.0, "IPVA", 220, 960, -0.04), (12.9, "IPTU", 220, 1080, 0.03),
                                (13.8, "Material escolar", 800, 960, 0.04), (15.2, "Fatura do Natal", 800, 1080, -0.03)):
            entra(c, t, t0, x, y, chip(s_, VERMELHO, CREME, 40, r), anim="pop")
    if 16.7 <= t < 19.2:
        entra(c, t, 16.7, 540, 1000, chip("3 DEGRAUS", GOLD, TINTA, 60), anim="stamp")
    # cada um
    for t0, t1, s_ in ((22.2, 25.0, "R$ 300 cada um"), (26.2, 29.3, "R$ 400 cada um"), (30.2, 32.2, "R$ 550 cada um")):
        if t0 <= t < t1:
            entra(c, t, t0, 540, 1000, chip(s_, NAVY, CREME, 50), anim="pop")
    if 32.4 <= t < 35.9:
        entra(c, t, 32.4, 540, 1000, chip("13º ajuda aqui", VERDE, CREME, 50), anim="stamp")
    # somando
    if 36.0 <= t < 44.2:
        entra(c, t, 36.9, 230, 960, chip("R$ 2.400", CREME, TINTA, 50, -0.03), anim="left")
        if t >= 38.9:
            entra(c, t, 38.9, 230, 1080, chip("+ R$ 3.200", CREME, TINTA, 50, 0.03), anim="left")
        if t >= 40.7:
            entra(c, t, 40.7, 810, 960, chip("+ R$ 4.400", CREME, TINTA, 50, 0.03), anim="right")
        if t >= 42.6:
            entra(c, t, 42.6, 810, 1080, chip("= R$ 10.000", VERDE, CREME, 50, -0.03), anim="stamp")
    # o detalhe do CDI
    if 45.4 <= t < 48.1:
        entra(c, t, 45.4, 540, 1000, chip("PARADO NÃO", VERMELHO, CREME, 56), anim="stamp")
    if 48.2 <= t < 59.8:
        entra(c, t, 48.2, 240, 980, chip("100% do CDI", CREME, TINTA, 46, -0.03), anim="left")
        if t >= 55.2:
            entra(c, t, 55.2, 800, 980, chip("já sem IR", CREME, TINTA, 46, 0.03), anim="right")
        if t >= 56.9:
            entra(c, t, 56.9, 800, 1095, chip("+ uns R$ 500", VERDE, CREME, 48, -0.03), anim="stamp")
    # a regra do casal
    if 59.9 <= t < 68.1:
        if t < 65.9:
            entra(c, t, 61.2, 240, 980, chip("dia do salário", CREME, TINTA, 44, -0.03), anim="left")
            if t >= 63.2:
                entra(c, t, 63.2, 800, 980, chip("conta só disso", NAVY, CREME, 44, 0.03), anim="right")
        else:
            entra(c, t, 65.9, 540, 1000, chip("atrasou = paga o jantar", GOLD, TINTA, 46), anim="stamp")
    if t >= 71.1:
        entra(c, t, 71.1, 540, 1000, chip("TOPA? MARCA QUEM", VERMELHO, CREME, 52), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "DESAFIO DO CASAL 2027", 540, 235, 56, CREME)
    tabela(c, t)
    marcador(c, t)
    poses = ((0, "arms_up"), (4.1, "point_r"), (7.4, "finger_up"), (9.6, "head"), (16.7, "present"), (19.3, "point_r"),
             (32.2, "present"), (36.0, "finger_up"), (42.6, "arms_up"), (44.3, "finger_up"), (48.2, "present"),
             (56.9, "arms_up"), (59.9, "finger_up"), (65.9, "shrug"), (68.2, "arms_up"), (71.1, "point_r"))
    exprs = ((0, "grin"), (7.4, "confident"), (9.6, "shocked"), (16.7, "confident"), (42.6, "grin"), (44.3, "think"),
             (52.1, "confident"), (56.9, "grin"), (65.9, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
