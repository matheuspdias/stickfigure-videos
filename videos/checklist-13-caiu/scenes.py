"""CHECKLIST DO CONSULTOR · "4 passos quando o 13º cair" (TikTok vertical, ~68 s). Modelo: videos/checklist-salario-caiu.
Contas: 1ª parcela do 13º de quem ganha R$ 3.000 = R$ 1.500 (até 30/11, sem desconto). Rotativo do cartão: ~445% ao ano
(BC, agosto/2026) = ~15% ao mês, R$ 1.000 -> ~R$ 1.150 em 30 dias. 1.500 - 500 (fatura) = 1.000; - 300 (janeiro) = 700;
20% de 700 = 140 -> 560 de teto do Natal. 2ª parcela (até 18/12) = R$ 1.251,40 (ver videos/decimo-terceiro-quanto-cai/contas.py)."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.25, "soft_ding"), (12.5, "tum"), (27.0, "tum"), (28.2, "tum"), (34.3, "soft_ding"), (37.6, "tum"), (43.1, "soft_ding"),
       (45.3, "tum"), (51.2, "soft_ding"), (64.7, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(12.5, "DÍVIDA CARA PRIMEIRO", 27.6), (28.2, "SEPARA JANEIRO", 36.4),
          (37.6, "A SUA PARTE", 44.2), (45.3, "O TETO DO NATAL", 62.5)]
L1, L2, R1, R2 = (230, 990), (230, 1100), (800, 990), (800, 1100)


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
    rr(c, 70 + 8, 290 + 10, 850, 450, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 70, 290, 850, 450, 30); rgb(c, CREME); c.fill()
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = 362 + i * 102
        if t0 - 0.6 <= t < t1:
            rr(c, 86, y - 46, 818, 92, 20); rgb(c, GOLD, 0.35); c.fill()
        c.new_sub_path(); c.arc(150, y, 36, 0, 6.283); rgb(c, VERDE if t >= t1 else NAVY); c.fill()
        if t >= t1:
            c.move_to(133, y); c.line_to(146, y + 15); c.line_to(170, y - 15); rgb(c, CREME); c.set_line_width(9); c.stroke()
        else:
            text(c, str(i + 1), 150, y + 16, 44, MARKER, CREME)
        if t < t0:
            c.move_to(210, y + 18); c.line_to(870, y + 18); rgb(c, TINTA, 0.25); c.set_line_width(5); c.set_dash([16, 12]); c.stroke(); c.set_dash([])
        else:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(205, y - 50, 690 * k, 100); c.clip()
            text(c, nome, 210, y + 17, 46, MARKER, TINTA, align="l")
            c.restore()


def marcador(c, t):
    if t >= 51.2:
        k = 1 + 0.12 * math.sin(clamp01((t - 51.2) / 0.35) * math.pi)
        c.save(); c.translate(540, 840); c.scale(k, k)
        rr(c, -350, -70, 700, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "NATAL: R$ 560", 0, 30, 82, MARKER, TINTA)
        c.restore()
        return
    rr(c, 190, 775, 700, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    text(c, "13º", 290, 862, 50, MARKER, CREME)
    if t < 27.0:
        contador(c, t, 0.0, 0, 1500, 620, 840, 84, d=1.0, col=VERDE)
    elif t < 34.3:
        contador(c, t, 27.0, 1500, 1000, 620, 840, 84, d=0.8, col=GOLD)
        if t < 31.0:
            entra(c, t, 27.0, 790, 770, chip("- R$ 500", VERMELHO, CREME, 40, 0.04), anim="stamp")
    elif t < 43.1:
        contador(c, t, 34.3, 1000, 700, 620, 840, 84, d=0.8, col=GOLD)
        if t < 38.0:
            entra(c, t, 34.3, 790, 770, chip("- R$ 300", NAVY, CREME, 40, 0.04), anim="stamp")
    else:
        contador(c, t, 43.1, 700, 560, 620, 840, 84, d=0.8, col=GOLD)
        entra(c, t, 43.1, 790, 770, chip("- R$ 140", VERDE, CREME, 40, 0.04), anim="stamp")


def detalhes(c, t):
    if t < 11.4:
        a = 1.0 if t < 10.8 else max(0.0, 1 - (t - 10.8) / 0.5)
        c.push_group(); notificacao(c, 540, 1040, 1.55, "13º salário caiu!", "+ R$ 1.500,00 · 1ª parcela", VERDE, "BANCO")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    # passo 1: dívida cara
    if 14.5 <= t < 24.6:
        entra(c, t, 14.5, *L1, chip("Fatura no rotativo", VERMELHO, CREME, 40, -0.04), anim="left")
        entra(c, t, 17.6, *R1, chip("~15% ao mês", CREME, TINTA, 46, 0.04), anim="right")
        entra(c, t, 19.2, *L2, chip("R$ 1.000", CREME, TINTA, 46, 0.03), anim="left")
        entra(c, t, 20.3, *R2, chip("vira R$ 1.150", CREME, VERMELHO, 44, -0.03), anim="right")
    if 24.6 <= t < 27.9:
        entra(c, t, 24.7, *L1, chip("Fatura R$ 500", VERMELHO, CREME, 46, -0.04), anim="left")
        if t >= 27.0:
            entra(c, t, 27.0, *R1, chip("QUITA", VERDE, CREME, 56, 0.05), anim="stamp")
    # passo 2: janeiro
    if 30.4 <= t < 36.6:
        entra(c, t, 30.4, *L1, chip("IPVA", CREME, TINTA, 52, -0.04), anim="left")
        entra(c, t, 31.3, *R1, chip("IPTU", CREME, TINTA, 52, 0.04), anim="right")
        entra(c, t, 32.2, *L2, chip("Material escolar", CREME, TINTA, 40, 0.03), anim="left")
        entra(c, t, 34.3, *R2, chip("separa R$ 300", NAVY, CREME, 42, -0.03), anim="right")
    # passo 3: a sua parte
    if 38.8 <= t < 44.4:
        entra(c, t, 38.8, *L1, chip("20% do que sobrou", VERDE, CREME, 38, -0.04), anim="left")
        entra(c, t, 41.9, *R1, chip("R$ 700 x 20%", CREME, TINTA, 44, 0.04), anim="right")
        entra(c, t, 43.1, 540, 1100, chip("R$ 140 na reserva", VERDE, CREME, 44), anim="pop")
    # passo 4: o teto do Natal
    if 48.6 <= t < 55.3:
        entra(c, t, 48.6, *L1, chip("Presentes", CREME, TINTA, 48, -0.04), anim="left")
        entra(c, t, 49.4, *R1, chip("Ceia", CREME, TINTA, 48, 0.04), anim="right")
        entra(c, t, 50.3, *L2, chip("Roupa nova", CREME, TINTA, 46, 0.03), anim="left")
        if t >= 53.2:
            entra(c, t, 53.2, *R2, chip("acabou o Natal", VERMELHO, CREME, 42, -0.03), anim="stamp")
    # a 2ª parcela
    if 55.4 <= t < 64.6:
        entra(c, t, 55.6, *L1, chip("2ª parcela 18/12", NAVY, CREME, 42, -0.04), anim="left")
        entra(c, t, 58.4, *R1, chip("~R$ 1.250", CREME, TINTA, 50, 0.04), anim="right")
        if t >= 62.8:
            entra(c, t, 62.8, 540, 1100, chip("repete os 4 passos", GOLD, TINTA, 46), anim="pop")
    if t >= 64.7:
        entra(c, t, 64.7, 540, 1040, chip("QUAL PASSO VOCÊ PULA?", GOLD, TINTA, 52), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANDO O 13º CAIR", 540, 235, 60, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "arms_up"), (4.3, "present"), (11.5, "finger_up"), (14.5, "point_r"), (22.9, "shrug"), (27.0, "finger_up"),
             (30.4, "point_r"), (36.7, "finger_up"), (38.8, "present"), (44.5, "finger_up"), (48.6, "point_r"), (53.2, "shrug"),
             (55.4, "present"), (64.7, "present"))
    exprs = ((0, "grin"), (4.3, "confident"), (16.3, "shocked"), (24.7, "confident"), (43.1, "grin"), (53.2, "confident"), (64.7, "grin"))
    consultor_i(c, t, 540, 2250, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
