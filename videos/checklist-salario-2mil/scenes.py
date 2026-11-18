"""CHECKLIST DO CONSULTOR · Parte 2: "salário de R$ 2 mil caiu, 4 passos" (TikTok vertical, ~77 s, estilo ilustrado).
Continuação do `checklist-salario-caiu` (R$ 3 mil, 105 mil views, primeiro vídeo pago pelo programa de recompensas).
Mesma cena fixa e mesma lista preenchida passo a passo; passo novo: o mercado do mês no dia do pagamento.
Contas: 700 + 200 + 150 = 1.050 de fixas; 5% de 2.000 = 100 (x12 = 1.200 no ano); mercado 400;
2.000 - 1.050 - 100 - 400 = 450; 450 / 30 = 15 por dia; lanche de 30 = 2 dias."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.25, "soft_ding"), (8.1, "tum"), (22.9, "tum"), (36.1, "tum"), (46.9, "tum"), (55.1, "soft_ding"), (74.4, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(8.1, "O QUE JÁ TEM DONO", 22.6), (22.9, "A SUA PARTE", 35.8), (36.1, "O MERCADO DO MÊS", 46.6),
          (46.9, "SEU NÚMERO DO DIA", 70.2)]
LIN0, LINH = 365, 105  # primeira linha da lista e espaçamento


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
    rr(c, 70 + 8, 290 + 10, 850, 445, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 70, 290, 850, 445, 30); rgb(c, CREME); c.fill()
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = LIN0 + i * LINH
        ativo = t0 - 0.6 <= t < t1
        if ativo:
            rr(c, 86, y - 48, 818, 96, 20); rgb(c, GOLD, 0.35); c.fill()
        c.new_sub_path(); c.arc(160, y, 37, 0, 6.283); rgb(c, VERDE if t >= t1 else NAVY); c.fill()
        if t >= t1:  # concluído
            c.move_to(143, y); c.line_to(157, y + 16); c.line_to(181, y - 16); rgb(c, CREME); c.set_line_width(9); c.stroke()
        else:
            text(c, str(i + 1), 160, y + 16, 46, MARKER, CREME)
        if t < t0:
            c.move_to(230, y + 20); c.line_to(860, y + 20); rgb(c, TINTA, 0.25); c.set_line_width(5); c.set_dash([16, 12]); c.stroke(); c.set_dash([])
        else:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(225, y - 55, 650 * k, 110); c.clip()
            text(c, nome, 230, y + 18, 50, MARKER, TINTA, align="l")
            c.restore()


def saldo(c, t):
    yc = 835
    if t >= 55.1:
        k = 1 + 0.12 * math.sin(clamp01((t - 55.1) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -330, -70, 660, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "R$ 15 POR DIA", 0, 30, 84, MARKER, TINTA)
        c.restore()
        return
    rr(c, 190, yc - 65, 700, 130, 30); rgb(c, NAVY_ESC if "NAVY_ESC" in globals() else (0.10, 0.14, 0.26)); c.fill()
    text(c, "SALDO", 300, yc + 22, 46, MARKER, CREME)
    if t < 18.1:
        contador(c, t, 0.0, 0, 2000, 640, yc, 84, d=1.0, col=VERDE)
    elif t < 27.9:
        contador(c, t, 18.1, 2000, 950, 640, yc, 84, d=1.0, col=GOLD)
        if t < 22.6:
            entra(c, t, 18.1, 770, yc - 70, chip("- R$ 1.050", VERMELHO, CREME, 40, 0.04), anim="stamp")
    elif t < 40.0:
        contador(c, t, 27.9, 950, 850, 640, yc, 84, d=0.8, col=GOLD)
        if t < 31.5:
            entra(c, t, 27.9, 790, yc - 70, chip("- R$ 100", VERDE, CREME, 40, 0.04), anim="stamp")
    else:
        contador(c, t, 40.0, 850, 450, 640, yc, 84, d=0.8, col=GOLD)
        if t < 43.6:
            entra(c, t, 40.0, 790, yc - 70, chip("- R$ 400", VERMELHO, CREME, 40, 0.04), anim="stamp")


def detalhes(c, t):
    # quadro 0: a notificação do salário (some quando começa o passo 1)
    if t < 8.0:
        a = 1.0 if t < 7.4 else max(0.0, 1 - (t - 7.4) / 0.5)
        c.push_group(); notificacao(c, 540, 1020, 1.55, "Salário caiu!", "+ R$ 2.000,00 na sua conta", VERDE, "BANCO"); c.pop_group_to_source(); c.paint_with_alpha(a)
    # passo 1: o que já tem dono
    if 10.6 <= t < 22.6:
        entra(c, t, 10.6, 225, 990, chip("Aluguel R$ 700", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 12.3, 225, 1110, chip("Contas R$ 200", CREME, TINTA, 44, 0.03), anim="left")
        entra(c, t, 15.3, 790, 990, chip("Transp.+cel. R$ 150", CREME, TINTA, 38, 0.04), anim="right")
        if t >= 18.1:
            entra(c, t, 18.1, 790, 1110, chip("= R$ 1.050", VERMELHO, CREME, 46, -0.03), anim="stamp")
    # passo 2: a sua parte
    if 25.2 <= t < 35.8:
        if t < 26.7:
            entra(c, t, 25.2, 240, 1000, chip("10% aperta?", VERMELHO, CREME, 48, -0.04), anim="pop")
        elif t < 32.2:
            entra(c, t, 26.7, 240, 1000, chip("5% = R$ 100", VERDE, CREME, 50, -0.04), anim="stamp")
        if 29.4 <= t < 32.2:
            entra(c, t, 29.4, 790, 1000, chip("conta separada", NAVY, CREME, 42, 0.04), anim="right")
        if t >= 32.2:
            entra(c, t, 32.2, 540, 1000, chip("1 ano = R$ 1.200", GOLD, TINTA, 56), anim="stamp")
    # passo 3: o mercado do mês
    if 37.7 <= t < 46.6:
        if t < 43.3:
            entra(c, t, 37.7, 240, 1000, chip("1x no mês", CREME, TINTA, 48, -0.04), anim="left")
            if t >= 40.0:
                entra(c, t, 40.0, 790, 1000, chip("R$ 400 + lista", CREME, TINTA, 46, 0.04), anim="right")
        else:
            entra(c, t, 43.3, 540, 1000, chip("mercadinho todo dia = some", VERMELHO, CREME, 42), anim="stamp")
    # passo 4: o número do dia
    if 51.4 <= t < 58.0:
        entra(c, t, 51.4, 230, 1000, chip("R$ 450", CREME, TINTA, 56), anim="left")
        entra(c, t, 53.8, 800, 1000, chip("÷ 30 dias", CREME, TINTA, 56), anim="right")
    if 58.2 <= t < 66.4:
        for i, (t0, s_, x, y) in enumerate(((58.2, "Lanche", 210, 990), (59.0, "Uber", 210, 1110), (59.6, "Padaria", 820, 990))):
            if t < 61.8:
                entra(c, t, t0, x, y, chip(s_, CREME, TINTA, 50, (-0.03, 0.03, 0.04)[i]), anim="pop")
        if t >= 61.8:
            entra(c, t, 61.8, 250, 1000, chip("Lanche R$ 30", VERMELHO, CREME, 46, -0.04), anim="stamp")
        if t >= 63.8:
            entra(c, t, 63.8, 780, 1000, chip("= hoje + amanhã", VERMELHO, CREME, 42, 0.04), anim="stamp")
    if 66.5 <= t < 70.3:
        entra(c, t, 66.8, 240, 1000, chip("gastou R$ 10", CREME, TINTA, 46, -0.03), anim="left")
        entra(c, t, 68.6, 780, 1000, chip("+R$ 5 amanhã", VERDE, CREME, 44, 0.04), anim="right")
    if t >= 74.4:
        entra(c, t, 74.4, 540, 1020, chip("QUAL É O SEU NÚMERO?", GOLD, TINTA, 54), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "SALÁRIO DE R$ 2 MIL", 540, 235, 58, CREME)
    lista(c, t)
    saldo(c, t)
    poses = ((0, "arms_up"), (2.6, "present"), (8.1, "finger_up"), (10.6, "point_r"), (20.1, "present"), (22.9, "finger_up"),
             (25.2, "shrug"), (26.7, "point_r"), (32.2, "present"), (36.1, "finger_up"), (40.0, "point_r"), (43.3, "head"),
             (46.9, "finger_up"), (53.8, "present"), (58.2, "point_r"), (61.8, "head"), (66.5, "present"), (70.4, "finger_up"),
             (74.4, "present"))
    exprs = ((0, "grin"), (2.6, "confident"), (18.1, "neutral"), (25.2, "think"), (26.7, "confident"), (32.2, "grin"),
             (43.3, "think"), (46.9, "confident"), (55.1, "grin"), (61.8, "shocked"), (66.5, "confident"), (74.4, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
