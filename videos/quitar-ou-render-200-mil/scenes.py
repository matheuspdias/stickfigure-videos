"""R$ 200 MIL NA MÃO: QUITAR O FINANCIAMENTO OU DEIXAR RENDENDO? (TikTok vertical, ~77,6 s, estilo ilustrado).
Item [18h] da "Fila do Matheus". Contas em contas.py: 100% do CDI (13,65%) líquido de IR 15% ~ 11,6% a.a. = ~R$ 23 mil no 1º ano;
contrato de 12% (com TR) = ~R$ 24 mil de juros -> quitar ganha; contrato de 8% = ~R$ 16 mil -> render ganha ~R$ 7 mil/ano.
Regra: taxa do contrato acima de ~11,5% quita; abaixo, rende. Reserva antes; amortizar reduzindo o prazo."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (21.6, "tum"), (36.1, "tum"), (40.4, "tum"), (50.0, "soft_ding"), (69.2, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

L1, L2, R1, R2 = (250, 1000), (250, 1115), (800, 1000), (800, 1115)
C1 = (540, 1000)
X0, WMAX, VMAX = 450, 420, 25000.0


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


def painel(c):
    rr(c, 60 + 8, 290 + 10, 870, 460, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 60, 290, 870, 460, 30); rgb(c, CREME); c.fill()


def abertura(c, t):
    painel(c)
    for i, (nome, cor, t0) in enumerate((("NA MÃO", VERDE, 0.0), ("DEVE", VERMELHO, 2.7))):
        y = 400 + i * 150
        text(c, nome, 110, y + 18, 54, MARKER, NAVY, align="l")
        if t >= t0:
            contador(c, t, t0, 0, 200000, 610, y - 6, 74, d=1.3, col=cor)
        else:
            numero_i(c, "R$ ...", 610, y + 20, 70, CREME)
    if t >= 5.1:
        k = ease_out(clamp01((t - 5.1) / 0.4))
        text(c, "QUITA OU RENDE?", 495, 700, 60 * (0.6 + 0.4 * k), MARKER, VERMELHO)


def barra(c, t, y, nome, sub, valor, cor, tg, t_ini=None, v_ini=None):
    text(c, nome, 92, y + 2, 40, MARKER, NAVY, align="l")
    text(c, sub, 92, y + 40, 28, MARKER, TINTA, align="l")
    if t < tg:
        c.move_to(X0, y + 4); c.line_to(X0 + WMAX, y + 4); rgb(c, TINTA, 0.22); c.set_line_width(4)
        c.set_dash([12, 10]); c.stroke(); c.set_dash([])
        return
    v = valor * ease_out(clamp01((t - tg) / 0.9))
    if v_ini is not None and t_ini is not None:
        v = v_ini if t < t_ini else v_ini + (valor - v_ini) * ease_out(clamp01((t - t_ini) / 0.9))
    w = WMAX * v / VMAX
    rr(c, X0, y - 30, w, 64, 14); rgb(c, cor); c.fill()
    text(c, f"R$ {v/1000:.0f} MIL", X0 + w - 14, y + 15, 38, MARKER, CREME, align="r")


def comparacao(c, t):
    painel(c)
    text(c, "NO 1º ANO, SOBRE R$ 200 MIL", 495, 345, 40, MARKER, NAVY)
    barra(c, t, 430, "RENDE", "100% do CDI, sem IR", 23200, VERDE, 21.6)
    if t < 40.4:
        barra(c, t, 555, "JUROS", "contrato de 12%", 24000, VERMELHO, 34.6)
    else:
        barra(c, t, 555, "JUROS", "contrato de 8%" if t >= 44.8 else "contrato de 12%", 16000, VERMELHO, 0.0, t_ini=46.2, v_ini=24000)
    if 36.1 <= t < 40.4:
        entra(c, t, 36.1, 495, 670, chip("QUITAR GANHA", VERMELHO, CREME, 46), anim="stamp")
    elif t >= 49.9:
        entra(c, t, 49.9, 495, 670, chip("RENDER GANHA: + R$ 7 MIL/ANO", VERDE, CREME, 40), anim="stamp")


def detalhes_painel(c, t):
    painel(c)
    text(c, "MAIS 2 DETALHES", 495, 350, 48, MARKER, NAVY)
    itens = ((54.5, "1. SELIC CAINDO EM 2027", 58.8, "rende menos, contrato igual"),
             (61.3, "2. SEPARA A RESERVA ANTES", 65.6, "amortiza reduzindo o prazo"))
    for i, (t0, s, t1, s2) in enumerate(itens):
        y = 450 + i * 150
        if t >= t0:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(80, y - 50, 830 * k, 140); c.clip()
            rr(c, 90, y - 40, 810, 76, 18); rgb(c, GOLD, 0.35); c.fill()
            text(c, s, 120, y + 14, 44, MARKER, TINTA, align="l")
            c.restore()
        if t >= t1:
            text(c, s2, 130, y + 80, 36, MARKER, VERMELHO if i == 0 else VERDE, align="l", alpha=clamp01((t - t1) / 0.4))


def regra(c, t):
    painel(c)
    text(c, "A TAXA DO SEU CONTRATO", 495, 350, 46, MARKER, NAVY)
    for i, (t0, a, b, cor) in enumerate(((69.2, "ACIMA DE 11,5%", "QUITA", VERMELHO), (72.5, "ABAIXO DE 11,5%", "RENDE", VERDE))):
        y = 470 + i * 130
        if t >= t0:
            k = ease_out(clamp01((t - t0) / 0.4))
            c.save(); c.rectangle(80, y - 55, 830 * k, 110); c.clip()
            rr(c, 90, y - 45, 810, 90, 20); rgb(c, CREME); c.fill()
            rr(c, 90, y - 45, 810, 90, 20); rgb(c, cor, 0.15); c.fill()
            text(c, a, 120, y + 17, 46, MARKER, TINTA, align="l")
            text(c, b, 880, y + 17, 56, MARKER, cor, align="r")
            c.restore()
        else:
            c.move_to(120, y + 20); c.line_to(870, y + 20); rgb(c, TINTA, 0.22); c.set_line_width(4)
            c.set_dash([12, 10]); c.stroke(); c.set_dash([])


def marcador(c, t):
    yc = 860
    if t >= 74.6:
        k = 1 + 0.12 * math.sin(clamp01((t - 74.6) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -410, -70, 820, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "A LINHA: 11,5% AO ANO", 0, 26, 64, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=40):
        text(c, s, 335, yc + 18, size, MARKER, CREME)

    def val(s, col=GOLD, size=72):
        numero_i(c, s, 715, yc + 26, size, col)
    if t < 9.6:
        lab("O NÚMERO"); val("?", CREME, 84)
    elif t < 25.3:
        lab("RENDE/ANO")
        if t >= 19.0:
            val("~11,5%", VERDE, 80)
        elif t >= 12.0:
            val("SELIC 13,75%", CREME, 54)
        else:
            val("?", CREME, 84)
    elif t < 40.4:
        lab("CONTRATO")
        val("12% AO ANO", VERMELHO, 64) if t >= 31.9 else val("?", CREME, 84)
    elif t < 53.0:
        lab("CONTRATO")
        val("8% AO ANO", VERDE, 64) if t >= 44.8 else val("12% AO ANO", CREME, 64)
    else:
        lab("A LINHA"); val("11,5%", GOLD, 80)


def chips(c, t):
    if 0.6 <= t < 9.6:
        if t >= 5.1:
            entra(c, t, 5.1, *L1, chip("QUITA TUDO?", VERMELHO, CREME, 46, -0.04), anim="stamp")
        if t >= 6.1:
            entra(c, t, 6.1, *R1, chip("DEIXA RENDENDO?", VERDE, CREME, 42, 0.04), anim="stamp")
        if t >= 7.9:
            entra(c, t, 7.9, *L2, chip("depende de", GOLD, TINTA, 40, 0.03), anim="pop")
            entra(c, t, 8.4, *R2, chip("1 número", GOLD, TINTA, 46, -0.03), anim="pop")
    if 11.7 <= t < 21.4:
        entra(c, t, 12.0, *L1, chip("Selic 13,75%", CREME, NAVY, 42, -0.04), anim="left")
        if t >= 15.1:
            entra(c, t, 15.1, *R1, chip("100% do CDI", GOLD, TINTA, 44, 0.04), anim="right")
        if t >= 17.2:
            entra(c, t, 17.2, *L2, chip("já sem imposto", CREME, TINTA, 40, 0.03), anim="left")
        if t >= 19.2:
            entra(c, t, 19.2, *R2, chip("~11,5% ao ano", VERDE, CREME, 42, -0.03), anim="stamp")
    if 21.6 <= t < 25.3:
        entra(c, t, 22.8, *C1, chip("~R$ 23 MIL NO ANO", VERDE, CREME, 50), anim="stamp")
    if 28.3 <= t < 34.6:
        entra(c, t, 28.3, *L1, chip("taxa do contrato", CREME, TINTA, 40, -0.04), anim="left")
        if t >= 30.3:
            entra(c, t, 30.3, *R1, chip("+ TR", NAVY, CREME, 46, 0.04), anim="right")
        if t >= 31.9:
            entra(c, t, 31.9, *L2, chip("12% ao ano", VERMELHO, CREME, 44, 0.03), anim="stamp")
    if 37.4 <= t < 40.4:
        entra(c, t, 37.7, *C1, chip("+ some o seguro da parcela", GOLD, TINTA, 40), anim="pop")
    if 40.4 <= t < 46.2:
        entra(c, t, 40.6, *C1, chip("A VIRADA", VERMELHO, CREME, 56), anim="stamp") if t < 41.7 else None
        if t >= 41.7:
            entra(c, t, 41.7, *L1, chip("juro baixo", CREME, TINTA, 44, -0.04), anim="left")
        if t >= 44.8:
            entra(c, t, 44.8, *R1, chip("contrato de 8%", VERDE, CREME, 42, 0.04), anim="stamp")
    if 46.3 <= t < 49.9:
        entra(c, t, 46.3, *C1, chip("~R$ 16 mil de juros", CREME, TINTA, 44), anim="pop")
    if 49.9 <= t < 53.0:
        entra(c, t, 50.5, *C1, chip("A SEU FAVOR", VERDE, CREME, 52), anim="stamp")
    if 61.5 <= t < 65.6:
        entra(c, t, 61.6, *C1, chip("NUNCA O DINHEIRO TODO", VERMELHO, CREME, 44), anim="stamp")
    if t >= 74.8:
        entra(c, t, 74.8, 540, 1040, chip("QUAL A TAXA DO SEU?", GOLD, TINTA, 50), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUITAR OU DEIXAR RENDENDO?", 540, 235, 54, CREME)
    if t < 9.6:
        abertura(c, t)
    elif t < 53.0:
        comparacao(c, t)
    elif t < 68.2:
        detalhes_painel(c, t)
    else:
        regra(c, t)
    marcador(c, t)
    poses = ((0, "present"), (5.1, "shrug"), (7.2, "finger_up"), (9.6, "present"), (12.0, "point_r"), (21.4, "arms_up"),
             (25.3, "finger_up"), (28.3, "point_r"), (34.6, "head"), (36.1, "finger_up"), (40.4, "finger_up"), (44.8, "point_r"),
             (49.9, "arms_up"), (53.0, "finger_up"), (58.8, "shrug"), (61.3, "finger_up"), (65.6, "present"),
             (68.2, "finger_up"), (72.5, "point_r"), (74.8, "present"))
    exprs = ((0, "confident"), (5.1, "think"), (7.2, "confident"), (21.4, "grin"), (25.3, "confident"), (34.6, "shocked"),
             (36.1, "confident"), (40.4, "think"), (49.9, "grin"), (53.0, "confident"), (58.8, "think"), (61.3, "confident"),
             (68.2, "confident"), (74.8, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    chips(c, t)


SCENES = [(0, 999.0, cena)]
