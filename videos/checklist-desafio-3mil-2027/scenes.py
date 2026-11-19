"""CHECKLIST DO CONSULTOR: "Desafio R$ 3 mil em 2027 pra quem ganha pouco, 4 passos" (TikTok vertical, ~81 s, estilo ilustrado).
Item 1 da "Fila do Matheus" [10h Checklist]. Modelo: videos/checklist-salario-2mil.
Contas (contas.py): 3.000/12 = 250 por mês, ~58 por semana, ~8 por dia; 52 semanas (R$ 2 subindo R$ 2) = 2.756,
dezembro (semanas 49-52) = 404; R$ 250/mês a 100% do CDI (~13,1% em 2027 pelo Focus de 16/11/2026, IR ~20%) -> ~3.140."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (7.5, "tum"), (18.7, "tum"), (42.8, "tum"), (57.6, "tum"), (74.4, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(7.5, "QUEBRA A META", 18.6), (18.7, "ESCOLHE O JEITO", 42.7), (42.8, "NO AUTOMÁTICO", 57.5),
          (57.6, "A REGRA DE MARÇO", 74.3)]
LIN0, LINH = 365, 105
L1, L2, R1, R2 = (250, 1000), (250, 1115), (800, 1000), (800, 1115)
C1, C2 = (540, 1000), (540, 1115)


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


def marcador(c, t):
    yc = 835
    if t >= 74.4:
        k = 1 + 0.12 * math.sin(clamp01((t - 74.4) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -400, -70, 800, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "R$ 8/DIA = R$ 3.140", 0, 28, 76, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    def lab(s):
        text(c, s, 330, yc + 20, 42, MARKER, CREME)
    if t < 10.5:
        lab("META 2027"); contador(c, t, 0.3, 0, 3000, 700, yc, 84, d=1.4, col=VERDE)
    elif t < 15.7:
        lab("POR MÊS"); contador(c, t, 11.9, 3000, 250, 700, yc, 84, d=0.9, col=GOLD)
    elif t < 18.7:
        lab("POR DIA"); contador(c, t, 15.7, 250, 8, 700, yc, 84, d=0.7, col=GOLD)
    elif t < 27.0:
        lab("META 2027"); numero_i(c, "R$ 3.000", 700, yc + 30, 84, VERDE)
    elif t < 38.9:
        lab("52 SEMANAS"); contador(c, t, 27.0, 0, 2756, 700, yc, 84, d=1.2, col=GOLD)
    elif t < 53.6:
        lab("FIXO R$ 250"); contador(c, t, 38.9, 2756, 3000, 700, yc, 84, d=0.8, col=VERDE)
    else:
        lab("NO FIM"); contador(c, t, 53.6, 3000, 3140, 700, yc, 84, d=0.9, col=GOLD)


def detalhes(c, t):
    if t < 7.4:
        a = 1.0 if t < 6.9 else max(0.0, 1 - (t - 6.9) / 0.5)
        c.push_group(); notificacao(c, 540, 1040, 1.55, "Meta 2027", "R$ 3.000 ganhando pouco", GOLD, "COFRE"); c.pop_group_to_source(); c.paint_with_alpha(a)
    # passo 1
    if 10.5 <= t < 17.3:
        entra(c, t, 10.5, *L1, chip("R$ 3.000 ÷ 12", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 11.9, *R1, chip("= R$ 250/mês", VERDE, CREME, 44, 0.04), anim="right")
        entra(c, t, 14.0, *L2, chip("R$ 58/semana", CREME, TINTA, 44, 0.03), anim="left")
        entra(c, t, 15.7, *R2, chip("R$ 8/dia", GOLD, TINTA, 50, -0.03), anim="stamp")
    if 17.3 <= t < 18.7:
        entra(c, t, 17.3, *C1, chip("= 1 lanche a menos", GOLD, TINTA, 52), anim="stamp")
    # passo 2
    if 20.9 <= t < 30.4:
        entra(c, t, 20.9, *L1, chip("52 semanas", CREME, NAVY, 46, -0.04), anim="left")
        entra(c, t, 23.8, *R1, chip("R$ 2, R$ 4, R$ 6...", CREME, TINTA, 40, 0.04), anim="right")
        if t >= 27.0:
            entra(c, t, 27.0, *R2, chip("= R$ 2.756", GOLD, TINTA, 52), anim="stamp")
    if 30.6 <= t < 32.2:
        entra(c, t, 30.6, *C1, chip("PEGADINHA", VERMELHO, CREME, 56), anim="stamp")
    if 32.2 <= t < 37.7:
        entra(c, t, 32.2, *L1, chip("só dezembro", CREME, TINTA, 46, -0.04), anim="left")
        if t >= 33.9:
            entra(c, t, 33.9, *R1, chip("R$ 404", VERMELHO, CREME, 54, 0.04), anim="stamp")
        if t >= 36.6:
            entra(c, t, 36.6, 235, 1115, chip("no mês do Natal", VERMELHO, CREME, 40, 0.03), anim="pop")
    if 37.7 <= t < 42.7:
        entra(c, t, 37.7, *L1, chip("ganha pouco?", CREME, TINTA, 46, -0.04), anim="left")
        if t >= 39.1:
            entra(c, t, 39.1, *R1, chip("FIXO R$ 250", VERDE, CREME, 48, 0.04), anim="stamp")
        if t >= 41.3:
            entra(c, t, 41.3, 245, 1115, chip("mais fácil de manter", CREME, TINTA, 34, 0.03), anim="pop")
    # passo 3
    if 43.9 <= t < 51.3:
        entra(c, t, 43.9, *L1, chip("dia do salário", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 46.9:
            entra(c, t, 46.9, *R1, chip("Pix agendado", NAVY, CREME, 44, 0.04), anim="right")
        if t >= 48.1:
            entra(c, t, 48.1, *L2, chip("conta separada", CREME, TINTA, 40, 0.03), anim="left")
        if t >= 49.5:
            entra(c, t, 49.5, *R2, chip("100% do CDI", GOLD, TINTA, 44, -0.03), anim="stamp")
    if 51.4 <= t < 55.4:
        if t < 53.6:
            entra(c, t, 51.4, *C1, chip("no fim do ano", CREME, TINTA, 46), anim="pop")
        else:
            entra(c, t, 53.6, *C1, chip("+ R$ 140 de juros", VERDE, CREME, 50), anim="stamp")
    if 55.4 <= t < 57.6:
        entra(c, t, 55.4, *C1, chip("R$ 3.140", GOLD, TINTA, 64), anim="stamp")
    # passo 4
    if 60.1 <= t < 65.6:
        entra(c, t, 60.1, *L1, chip("MARÇO", VERMELHO, CREME, 50, -0.04), anim="stamp")
        if t >= 62.5:
            entra(c, t, 62.5, *R1, chip("IPVA", CREME, TINTA, 46, 0.04), anim="right")
        if t >= 63.3:
            entra(c, t, 63.3, *L2, chip("material escolar", CREME, TINTA, 40, 0.03), anim="left")
        if t >= 64.7:
            entra(c, t, 64.7, *R2, chip("fatura", VERMELHO, CREME, 46, -0.03), anim="stamp")
    if 66.4 <= t < 69.5:
        if t < 68.6:
            entra(c, t, 66.6, *C1, chip("APERTOU? DIMINUI", GOLD, TINTA, 52), anim="stamp")
        else:
            entra(c, t, 68.6, *C1, chip("MAS NÃO PARA", VERMELHO, CREME, 52), anim="stamp")
    if 69.6 <= t < 74.3:
        if t < 72.0:
            entra(c, t, 69.6, *C1, chip("R$ 100 em vez de R$ 250", CREME, TINTA, 42), anim="pop")
        else:
            entra(c, t, 72.0, *C1, chip("VALEU! marca e segue", VERDE, CREME, 44), anim="stamp")
    if t >= 77.2:
        entra(c, t, 77.2, 540, 1040, chip("QUANTO VOCÊ GUARDA POR MÊS?", GOLD, TINTA, 46), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "DESAFIO R$ 3 MIL EM 2027", 540, 235, 58, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "arms_up"), (4.1, "present"), (7.5, "finger_up"), (10.5, "point_r"), (17.3, "present"), (18.7, "finger_up"),
             (20.9, "point_r"), (30.4, "finger_up"), (32.2, "shrug"), (37.7, "present"), (42.8, "finger_up"), (46.9, "point_r"),
             (51.4, "present"), (57.6, "finger_up"), (60.1, "head"), (65.6, "finger_up"), (69.6, "present"), (74.4, "arms_up"),
             (77.2, "present"))
    exprs = ((0, "grin"), (4.1, "confident"), (17.3, "grin"), (18.7, "confident"), (30.4, "think"), (33.9, "shocked"),
             (37.7, "confident"), (53.6, "grin"), (57.6, "confident"), (60.1, "think"), (66.6, "confident"), (72.0, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
