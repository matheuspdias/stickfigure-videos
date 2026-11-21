"""CHECKLIST DO CONSULTOR: "A melhor data de vencimento do cartão: 3 passos" (TikTok vertical, ~71 s, estilo ilustrado).
1º item da lista "Checklist do Consultor" (10h). Modelo: videos/checklist-primeiros-10-mil. Tempos da narração nova (clone B).
Contas (contas.py): salário dia 5 -> vencimento dia 10; fechamento ~7-10 dias antes (dia 3); compra 02/12 -> paga 10/12 (8 dias);
compra 04/12 -> paga 10/01 (37 dias); multa por atraso 2% (CDC) em R$ 1.000 = R$ 20; fechamento 10 dias antes -> até 40 dias."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (10.0, "tum"), (20.9, "tum"), (45.4, "tum"), (65.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(10.0, "VENCE DEPOIS DO SALÁRIO", 20.8), (20.9, "ACHA O FECHAMENTO", 45.3), (45.4, "COMPRA NO MELHOR DIA", 60.6)]
LIN0, LINH = 365, 105
L1, L2, R1, R2 = (255, 890), (255, 1005), (800, 890), (800, 1005)
C1, C2 = (540, 880), (540, 985)


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


def lista(c, t):
    rr(c, 70 + 8, 290 + 10, 850, 340, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 70, 290, 850, 340, 30); rgb(c, CREME); c.fill()
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = LIN0 + i * LINH
        ativo = t0 - 0.6 <= t < t1
        if ativo:
            rr(c, 86, y - 48, 818, 96, 20); rgb(c, GOLD, 0.35); c.fill()
        c.new_sub_path(); c.arc(160, y, 37, 0, 6.283); rgb(c, VERDE if t >= t1 else NAVY); c.fill()
        if t >= t1:
            c.move_to(143, y); c.line_to(157, y + 16); c.line_to(181, y - 16); rgb(c, CREME); c.set_line_width(9); c.stroke()
        else:
            text(c, str(i + 1), 160, y + 16, 46, MARKER, CREME)
        if t < t0:
            c.move_to(230, y + 20); c.line_to(860, y + 20); rgb(c, TINTA, 0.25); c.set_line_width(5); c.set_dash([16, 12]); c.stroke(); c.set_dash([])
        else:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(225, y - 55, 650 * k, 110); c.clip()
            text(c, nome, 230, y + 18, 46, MARKER, TINTA, align="l")
            c.restore()


def marcador(c, t):
    yc = 730
    if t >= 65.9:
        k = 1 + 0.12 * math.sin(clamp01((t - 65.9) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -420, -70, 840, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "ATÉ 40 DIAS SEM JUROS", 0, 26, 64, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=42):
        text(c, s, 345, yc + 16, size, MARKER, CREME)

    def val(s, col=GOLD, size=72):
        numero_i(c, s, 720, yc + 26, size, col)
    if t < 10.0:
        lab("SEU CARTÃO VENCE", 34); val("DIA 1", VERMELHO, 78)
    elif t < 12.9:
        lab("SALÁRIO CAI", 40); val("DIA 5", CREME, 78)
    elif t < 17.9:
        lab("FOLGA", 44); contador(c, t, 12.9, 0, 5, 710, yc, 80, d=0.8, col=GOLD, prefixo="", sufixo=" DIAS")
    elif t < 19.2:
        lab("SALÁRIO", 44); val("DIA 5", CREME, 78)
    elif t < 32.0:
        lab("VENCIMENTO", 40); val("DIA 10", VERDE, 78)
    elif t < 34.7:
        lab("FECHAMENTO", 40); val("DIA 3", GOLD, 78)
    elif t < 39.5:
        lab("PRA PAGAR", 42)
        if t >= 38.5:
            val("8 DIAS", VERMELHO, 78)
        else:
            val("...", CREME)
    elif t < 51.7:
        lab("PRA PAGAR", 42)
        if t >= 42.7:
            contador(c, t, 42.7, 8, 37, 710, yc, 80, d=0.9, col=VERDE, prefixo="", sufixo=" DIAS")
        else:
            val("8 DIAS", VERMELHO, 78)
    elif t < 60.7:
        lab("ATRASOU R$ 1.000", 32)
        if t >= 53.8:
            contador(c, t, 53.8, 0, 20, 710, yc, 80, d=0.7, col=VERMELHO, prefixo="- R$ ")
        else:
            val("...", CREME)
    else:
        lab("SALÁRIO 5 · VENCE 10", 30); val("FECHA 3", GOLD, 68)


def detalhes(c, t):
    if t < 9.6:
        a = 1.0 if t < 9.2 else max(0.0, 1 - (t - 9.2) / 0.4)
        c.push_group(); notificacao(c, 540, 930, 1.5, "Fatura vence hoje", "o salário só cai dia 5", VERMELHO, "CARTÃO"); c.pop_group_to_source(); c.paint_with_alpha(a)
    # passo 1
    if 10.8 <= t < 12.9:
        entra(c, t, 10.8, *L1, chip("vencimento", CREME, TINTA, 44, -0.04), anim="left")
        if t >= 11.6:
            entra(c, t, 11.6, *R1, chip("depois do salário", VERDE, CREME, 38, 0.04), anim="stamp")
    if 12.9 <= t < 17.9:
        entra(c, t, 13.1, *C1, chip("+ 5 DIAS DE FOLGA", GOLD, TINTA, 48), anim="stamp")
        if t >= 15.3:
            entra(c, t, 15.3, *L2, chip("atrasou?", CREME, TINTA, 42, 0.03), anim="left")
        if t >= 16.5:
            entra(c, t, 16.5, *R2, chip("fim de semana?", CREME, TINTA, 40, -0.03), anim="right")
    if 17.9 <= t < 20.9:
        entra(c, t, 17.9, *L1, chip("salário dia 5", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 19.2:
            entra(c, t, 19.2, *R1, chip("vence dia 10", VERDE, CREME, 44, 0.04), anim="stamp")
    # passo 2
    if 22.5 <= t < 30.9:
        entra(c, t, 22.5, *L1, chip("fecha quando?", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 25.7:
            entra(c, t, 25.7, *R1, chip("7 a 10 dias antes", GOLD, TINTA, 38, 0.04), anim="stamp")
        if t >= 29.3:
            entra(c, t, 29.3, *C2, chip("\"MELHOR DIA DE COMPRA\"", NAVY, CREME, 42), anim="pop")
    if 30.9 <= t < 34.7:
        entra(c, t, 30.9, *L1, chip("vence dia 10", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 32.0:
            entra(c, t, 32.0, *R1, chip("fecha dia 3", GOLD, TINTA, 44, 0.04), anim="stamp")
    if 34.7 <= t < 39.5:
        entra(c, t, 34.7, *L1, chip("compra 02/12", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 36.6:
            entra(c, t, 36.6, *R1, chip("paga 10/12", CREME, TINTA, 44, 0.04), anim="right")
        if t >= 38.5:
            entra(c, t, 38.5, *C2, chip("8 DIAS", VERMELHO, CREME, 52), anim="stamp")
    if 39.5 <= t < 45.4:
        entra(c, t, 39.5, *L1, chip("compra 04/12", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 41.0:
            entra(c, t, 41.0, *R1, chip("paga 10/01", VERDE, CREME, 44, 0.04), anim="right")
        if 42.7 <= t < 44.0:
            entra(c, t, 42.7, *C2, chip("37 DIAS", VERDE, CREME, 52), anim="stamp")
        if t >= 44.0:
            entra(c, t, 44.0, *C2, chip("A MESMA COMPRA", GOLD, TINTA, 50), anim="stamp")
    # passo 3
    if 46.3 <= t < 48.9:
        entra(c, t, 46.3, *L1, chip("compra grande", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 47.4:
            entra(c, t, 47.4, *R1, chip("no melhor dia", VERDE, CREME, 42, 0.04), anim="stamp")
    if 48.9 <= t < 51.7:
        entra(c, t, 49.0, *C1, chip("NUNCA VENCER ANTES DO SALÁRIO", VERMELHO, CREME, 40), anim="stamp")
    if 51.7 <= t < 60.7:
        entra(c, t, 52.4, *L1, chip("fatura R$ 1.000", CREME, TINTA, 40, -0.04), anim="left")
        if t >= 54.6:
            entra(c, t, 54.6, *R1, chip("multa R$ 20", VERMELHO, CREME, 44, 0.04), anim="stamp")
        if t >= 55.5:
            entra(c, t, 55.5, *L2, chip("+ juros", CREME, TINTA, 44, 0.03), anim="left")
        if t >= 57.5:
            entra(c, t, 57.5, *R2, chip("ROTATIVO", VERMELHO, CREME, 46, -0.03), anim="stamp")
    if 61.9 <= t < 68.7:
        entra(c, t, 62.0, *C1, chip("VENCE DEPOIS DO SALÁRIO", VERDE, CREME, 42), anim="stamp")
        if t >= 63.6:
            entra(c, t, 63.6, *C2, chip("COMPRA DEPOIS DO FECHAMENTO", GOLD, TINTA, 38), anim="stamp")
    if t >= 68.7:
        entra(c, t, 68.7, 540, 930, chip("QUE DIA CAI SEU SALÁRIO?", GOLD, TINTA, 46), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "A MELHOR DATA DO CARTÃO", 540, 235, 58, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "shrug"), (2.7, "finger_up"), (5.2, "present"), (7.9, "finger_up"), (10.0, "finger_up"), (12.9, "point_r"),
             (17.9, "present"), (20.9, "finger_up"), (24.2, "point_r"), (30.9, "present"), (33.3, "finger_up"), (38.5, "shrug"),
             (42.7, "arms_up"), (45.4, "finger_up"), (48.9, "finger_up"), (51.7, "point_r"), (57.5, "head"),
             (60.7, "finger_up"), (65.9, "arms_up"), (68.7, "present"))
    exprs = ((0, "shocked"), (2.7, "think"), (5.2, "confident"), (10.0, "confident"), (15.3, "think"), (17.9, "grin"),
             (20.9, "confident"), (38.5, "shocked"), (42.7, "grin"), (45.4, "confident"), (54.6, "shocked"),
             (60.7, "confident"), (65.9, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
