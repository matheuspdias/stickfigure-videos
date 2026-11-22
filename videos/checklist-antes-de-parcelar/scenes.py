"""CHECKLIST DO CONSULTOR: "3 passos antes de parcelar qualquer coisa" (TikTok vertical, ~77 s, estilo ilustrado).
1º item da lista "Checklist do Consultor" (10h, 23/11/2026, semana da Black Friday). Modelo: videos/checklist-vencimento-cartao.
Contas (contas.py): parcelas atuais celular R$ 150 + geladeira R$ 200 = R$ 350 (14% de R$ 2.500); teto 1/5 = R$ 500; sobra R$ 150;
TV R$ 2.400 em 12x = R$ 200 -> R$ 550 (22%), não cabe; falta pagar: celular 6x150 = 900, geladeira 8x200 = 1.600, TV 2.400 = R$ 4.900."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (8.4, "tum"), (20.3, "tum"), (40.4, "tum"), (45.8, "tum"), (67.3, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(8.4, "SOMA O QUE JÁ PARCELA", 20.2), (20.3, "COMPARA COM O SALÁRIO", 45.7), (45.8, "E SE A RENDA PARAR?", 67.2)]
LIN0, LINH = 365, 105
L1, L2, R1, R2 = (265, 890), (265, 1005), (770, 890), (770, 1005)
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
    if t >= 67.3:
        k = 1 + 0.12 * math.sin(clamp01((t - 67.3) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -430, -70, 860, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "TETO: 1/5 DO SALÁRIO", 0, 26, 64, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=42):
        text(c, s, 345, yc + 16, size, MARKER, CREME)

    def val(s, col=GOLD, size=72):
        numero_i(c, s, 720, yc + 26, size, col)

    def cont(t0, a, b, col, pref="R$ ", d=0.8):
        contador(c, t, t0, a, b, 710, yc, 76, d=d, col=col, prefixo=pref)
    if t < 8.4:
        lab("TV EM 12X", 44); cont(0.0, 0, 200, VERMELHO, d=1.6)
    elif t < 20.3:
        lab("JÁ PARCELA", 42)
        if t < 12.9:
            val("R$ 0", CREME, 76)
        elif t < 14.2:
            cont(12.9, 0, 150, VERMELHO)
        else:
            cont(14.2, 150, 350, VERMELHO)
    elif t < 28.0:
        lab("1/5 DO SALÁRIO", 34); val("20%", GOLD, 80)
    elif t < 31.8:
        lab("SEU TETO", 44)
        if t >= 30.4:
            cont(30.4, 0, 500, GOLD)
        else:
            val("...", CREME)
    elif t < 35.8:
        lab("SOBRAM", 46)
        if t >= 34.0:
            cont(34.0, 500, 150, VERDE)
        else:
            val("R$ 500", GOLD, 76)
    elif t < 41.3:
        lab("PARCELAS", 44)
        if t >= 38.8:
            cont(38.8, 350, 550, VERMELHO)
        else:
            val("R$ 350", CREME, 76)
    elif t < 45.8:
        lab("CABE ATÉ", 44); val("R$ 150", VERDE, 76)
    elif t < 50.3:
        lab("RENDA PAROU?", 36); val("R$ 0", VERMELHO, 80)
    elif t < 62.4:
        lab("FALTA PAGAR", 40)
        if t < 54.0:
            val("...", CREME)
        elif t < 56.8:
            cont(54.0, 0, 900, VERMELHO)
        elif t < 59.3:
            cont(56.8, 900, 2500, VERMELHO)
        else:
            cont(59.3, 2500, 4900, VERMELHO, d=1.0)
    else:
        lab("SEM SALÁRIO?", 40); val("R$ 4.900", VERMELHO, 76)


def detalhes(c, t):
    if t < 8.0:
        a = 1.0 if t < 7.6 else max(0.0, 1 - (t - 7.6) / 0.4)
        c.push_group()
        notificacao(c, 540, 930, 1.5, "TV R$ 2.400 em 12x!", "Black Friday: compre agora", VERMELHO, "LOJA")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    # passo 1
    if 9.2 <= t < 15.3:
        entra(c, t, 9.2, *C1, chip("SOMA TODAS", GOLD, TINTA, 50), anim="stamp")
        if t >= 12.0:
            entra(c, t, 12.0, *L2, chip("celular R$ 150", CREME, TINTA, 40, -0.03), anim="left")
        if t >= 13.7:
            entra(c, t, 13.7, *R2, chip("geladeira R$ 200", CREME, TINTA, 38, 0.03), anim="right")
    if 15.3 <= t < 20.3:
        entra(c, t, 15.6, *C1, chip("R$ 350 POR MÊS", VERMELHO, CREME, 50), anim="stamp")
        if t >= 18.1:
            entra(c, t, 18.1, *C2, chip("antes de comprar nada", CREME, TINTA, 42), anim="pop")
    # passo 2
    if 21.2 <= t < 28.0:
        entra(c, t, 21.2, *L1, chip("parcelas", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 22.1, *R1, chip("x salário", GOLD, TINTA, 44, 0.04), anim="right")
        if t >= 25.5:
            entra(c, t, 25.5, *C2, chip("no máximo 1/5", VERDE, CREME, 48), anim="stamp")
    if 28.0 <= t < 34.0:
        entra(c, t, 28.2, *L1, chip("salário R$ 2.500", CREME, TINTA, 40, -0.04), anim="left")
        if t >= 30.4:
            entra(c, t, 30.4, *R1, chip("teto R$ 500", GOLD, TINTA, 44, 0.04), anim="stamp")
        if t >= 32.1:
            entra(c, t, 32.1, *C2, chip("já usa R$ 350", VERMELHO, CREME, 44), anim="pop")
    if 34.0 <= t < 35.8:
        entra(c, t, 34.0, *C1, chip("SOBRAM R$ 150", VERDE, CREME, 50), anim="stamp")
    if 35.8 <= t < 41.3:
        entra(c, t, 36.2, *L1, chip("TV R$ 2.400", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 37.6:
            entra(c, t, 37.6, *R1, chip("12x R$ 200", CREME, TINTA, 44, 0.04), anim="right")
        if t >= 40.4:
            entra(c, t, 40.4, *C2, chip("NÃO CABE", VERMELHO, CREME, 56), anim="stamp")
    if 41.3 <= t < 45.8:
        entra(c, t, 41.5, *L1, chip("espera uma acabar", CREME, TINTA, 38, -0.04), anim="left")
        if t >= 43.1:
            entra(c, t, 43.1, *R1, chip("ou até R$ 150", VERDE, CREME, 40, 0.04), anim="right")
    # passo 3
    if 46.7 <= t < 50.3:
        entra(c, t, 46.8, *C1, chip("a pergunta que ninguém faz", CREME, TINTA, 40), anim="pop")
        if t >= 48.4:
            entra(c, t, 48.4, *C2, chip("E SE A RENDA PARAR?", VERMELHO, CREME, 46), anim="stamp")
    if 50.3 <= t < 62.4:
        entra(c, t, 50.4, *C1, chip("soma o que falta pagar", GOLD, TINTA, 42), anim="stamp") if t < 52.2 else None
        if t >= 52.2:
            entra(c, t, 52.2, *L1, chip("celular R$ 900", CREME, TINTA, 38, -0.04), anim="left")
        if t >= 55.0:
            entra(c, t, 55.0, *R1, chip("geladeira R$ 1.600", CREME, TINTA, 34, 0.04), anim="right")
        if t >= 57.8:
            entra(c, t, 57.8, *L2, chip("TV R$ 2.400", CREME, TINTA, 36, 0.03), anim="left")
        if t >= 60.2:
            entra(c, t, 60.2, *R2, chip("DÍVIDA", VERMELHO, CREME, 44, -0.03), anim="stamp")
    if 62.4 <= t < 67.3:
        entra(c, t, 62.6, *C1, chip("não paga sem salário?", CREME, TINTA, 42), anim="pop")
        if t >= 65.1:
            entra(c, t, 65.1, *C2, chip("GRANDE DEMAIS PRA AGORA", VERMELHO, CREME, 42), anim="stamp")
    if 67.3 <= t < 74.5:
        entra(c, t, 68.3, *L1, chip("1. soma", CREME, TINTA, 44, -0.04), anim="left")
        if t >= 69.1:
            entra(c, t, 69.1, *R1, chip("2. compara", CREME, TINTA, 44, 0.04), anim="right")
        if t >= 70.0:
            entra(c, t, 70.0, *C2, chip("3. pensa no pior", GOLD, TINTA, 46), anim="stamp")
    if t >= 74.5:
        entra(c, t, 74.5, 540, 930, chip("QUANTO SOMAM AS SUAS?", GOLD, TINTA, 48), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "ANTES DE PARCELAR", 540, 235, 58, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "shrug"), (2.8, "finger_up"), (4.7, "present"), (6.4, "finger_up"), (8.4, "finger_up"), (11.8, "point_r"),
             (15.3, "head"), (20.3, "finger_up"), (23.0, "present"), (28.0, "point_r"), (34.0, "present"), (35.8, "point_r"),
             (40.4, "shrug"), (41.3, "finger_up"), (45.8, "finger_up"), (48.4, "head"), (50.3, "point_r"), (60.2, "head"),
             (62.4, "finger_up"), (67.3, "arms_up"), (71.3, "finger_up"), (74.5, "present"))
    exprs = ((0, "think"), (2.8, "confident"), (11.8, "confident"), (15.3, "shocked"), (20.3, "confident"), (34.0, "grin"),
             (38.8, "shocked"), (41.3, "confident"), (48.4, "think"), (59.3, "shocked"), (62.4, "confident"), (67.3, "grin"),
             (71.3, "confident"), (74.5, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
