"""CHECKLIST DO CONSULTOR · "3 passos quando o salário cair" (TikTok vertical, ~67 s, estilo ilustrado).
Formato novo (15/11/2026), modelado no que viralizou em finanças (vídeos de 2 a 3 mi de views):
- UMA cena fixa o vídeo inteiro: o Consultor grande no centro, falando com quem assiste;
- a lista "1. 2. 3." VAZIA na tela desde o quadro 0, preenchida passo a passo (a pessoa fica para ver os 3);
- um salário concreto (R$ 3.000) atravessando o vídeo no "saldo", que muda a cada passo;
- detalhes do passo entrando dos lados, sem trocar de cenário.
Contas: 900 + 250 + 200 + 300 = 1.650 de fixas; 10% = 300; 3.000 - 1.650 - 300 = 1.050; 1.050 / 30 = 35 por dia."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.25, "soft_ding"), (9.2, "tum"), (19.5, "tum"), (25.9, "tum"), (28.7, "soft_ding"), (37.8, "tum"), (44.4, "soft_ding"), (51.2, "tum"), (61.0, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(9.2, "O QUE JÁ TEM DONO", 24.5), (25.9, "A SUA PARTE", 36.5), (37.8, "SEU NÚMERO DO DIA", 60.8)]


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
    rr(c, 70 + 8, 290 + 10, 850, 400, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 70, 290, 850, 400, 30); rgb(c, CREME); c.fill()
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = 380 + i * 125
        ativo = t0 - 0.6 <= t < t1
        if ativo:
            rr(c, 86, y - 56, 818, 112, 22); rgb(c, GOLD, 0.35); c.fill()
        c.new_sub_path(); c.arc(160, y, 42, 0, 6.283); rgb(c, VERDE if t >= t1 else NAVY); c.fill()
        if t >= t1:  # concluído
            c.move_to(140, y); c.line_to(156, y + 18); c.line_to(184, y - 18); rgb(c, CREME); c.set_line_width(10); c.stroke()
        else:
            text(c, str(i + 1), 160, y + 18, 50, MARKER, CREME)
        if t < t0:
            c.move_to(230, y + 22); c.line_to(860, y + 22); rgb(c, TINTA, 0.25); c.set_line_width(5); c.set_dash([16, 12]); c.stroke(); c.set_dash([])
        else:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(225, y - 60, 650 * k, 120); c.clip()
            text(c, nome, 230, y + 20, 54, MARKER, TINTA, align="l")
            c.restore()


def saldo(c, t):
    if t >= 44.4:
        k = 1 + 0.12 * math.sin(clamp01((t - 44.4) / 0.35) * math.pi)
        c.save(); c.translate(540, 790); c.scale(k, k)
        rr(c, -330, -70, 660, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "R$ 35 POR DIA", 0, 30, 84, MARKER, TINTA)
        c.restore()
        return
    rr(c, 190, 725, 700, 130, 30); rgb(c, NAVY_ESC if "NAVY_ESC" in globals() else (0.10, 0.14, 0.26)); c.fill()
    text(c, "SALDO", 300, 812, 46, MARKER, CREME)
    if t < 19.5:
        v = 3000
        contador(c, t, 0.0, 0, 3000, 640, 790, 84, d=1.0, col=VERDE)
    elif t < 28.7:
        contador(c, t, 19.5, 3000, 1350, 640, 790, 84, d=1.0, col=GOLD)
    else:
        contador(c, t, 28.7, 1350, 1050, 640, 790, 84, d=0.8, col=GOLD)


def detalhes(c, t):
    # quadro 0: a notificação do salário (some quando começa o passo 1)
    if t < 8.0:
        a = 1.0 if t < 7.4 else max(0.0, 1 - (t - 7.4) / 0.5)
        y = 1000
        c.push_group(); notificacao(c, 540, y, 1.55, "Salário caiu!", "+ R$ 3.000,00 na sua conta", VERDE, "BANCO"); c.pop_group_to_source(); c.paint_with_alpha(a)
    # passo 1: o que já tem dono
    if 10.8 <= t < 24.6:
        entra(c, t, 10.8, 225, 940, chip("Aluguel R$ 900", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 12.3, 225, 1060, chip("Contas R$ 250", CREME, TINTA, 44, 0.03), anim="left")
        entra(c, t, 15.6, 780, 940, chip("Transp. R$ 200", CREME, TINTA, 44, 0.04), anim="right")
        entra(c, t, 17.1, 780, 1060, chip("Celular R$ 300", CREME, TINTA, 44, -0.03), anim="right")
        if t >= 19.5:
            entra(c, t, 19.5, 540, 1500, chip("- R$ 1.650", VERMELHO, CREME, 60), anim="stamp")
    # passo 2: a sua parte
    if 27.6 <= t < 36.7:
        entra(c, t, 27.6, 240, 960, chip("10% = R$ 300", VERDE, CREME, 50, -0.04), anim="left")
        entra(c, t, 30.0, 790, 960, chip("conta separada", NAVY, CREME, 42, 0.04), anim="right")
        if t >= 33.9:
            entra(c, t, 33.9, 540, 1500, chip("no fim do mês = R$ 0", VERMELHO, CREME, 50), anim="stamp")
    # passo 3: o número do dia
    if 41.0 <= t < 47.2:
        entra(c, t, 41.0, 230, 960, chip("R$ 1.050", CREME, TINTA, 56), anim="left")
        entra(c, t, 42.7, 800, 960, chip("÷ 30 dias", CREME, TINTA, 56), anim="right")
    if 47.2 <= t < 56.9:
        for i, (t0, s_, x, y) in enumerate(((47.3, "Mercado", 210, 950), (48.2, "Lanche", 210, 1070), (49.0, "Uber", 820, 950))):
            if t < 51.0:
                entra(c, t, t0, x, y, chip(s_, CREME, TINTA, 50, (-0.03, 0.03, 0.04)[i]), anim="pop")
        if t >= 51.0:
            entra(c, t, 51.0, 250, 960, chip("Delivery R$ 45", VERMELHO, CREME, 46, -0.04), anim="stamp")
        if t >= 53.3:
            entra(c, t, 53.3, 760, 1080, chip("-R$ 10 de amanhã", VERMELHO, CREME, 40, 0.04), anim="stamp")
    if 57.0 <= t < 61.0:
        entra(c, t, 57.0, 240, 960, chip("gastou R$ 23", CREME, TINTA, 46, -0.03), anim="left")
        entra(c, t, 59.6, 770, 1080, chip("+R$ 12 amanhã", VERDE, CREME, 44, 0.04), anim="right")
    if t >= 64.7:
        entra(c, t, 64.7, 540, 950, chip("QUAL É O SEU NÚMERO?", GOLD, TINTA, 54), anim="pop")
        entra(c, t, 66.1, 540, 1500, chip("COMENTA AÍ", VERMELHO, CREME, 50, -0.03), anim="stamp")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "QUANDO O SALÁRIO CAIR", 540, 235, 58, CREME)
    lista(c, t)
    saldo(c, t)
    poses = ((0, "arms_up"), (2.6, "present"), (8.2, "finger_up"), (10.8, "point_r"), (22.2, "present"), (25.0, "finger_up"),
             (27.6, "point_r"), (33.9, "shrug"), (36.8, "finger_up"), (42.7, "present"), (47.3, "point_r"), (51.0, "head"),
             (57.0, "present"), (61.0, "finger_up"), (64.7, "present"))
    exprs = ((0, "grin"), (2.6, "confident"), (19.5, "neutral"), (33.9, "think"), (44.4, "grin"), (51.0, "shocked"),
             (57.0, "confident"), (64.7, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
