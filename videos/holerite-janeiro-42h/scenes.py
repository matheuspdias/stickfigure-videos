"""EXTRA 19/11 21h · "Holerite de janeiro: confira 3 coisas" (jornada nova de 42 h). TikTok vertical, ~71 s.
Remodelado de um vídeo em alta (Direito do Trabalho em 1 Minuto) no formato Checklist do Consultor.
Fatos: PEC do fim da 6x1 promulgada em 16/10/2026; teto de 42 h/semana desde 16/12/2026 (40 h em dez/2027);
sem redução de salário; hora extra com adicional mínimo de 50% (CF art. 7º, XVI); divisor 42 x 5 = 210 (antes 220).
Contas (salário R$ 3.000): hora 3000/220 = 13,64 -> 3000/210 = 14,29; extra 50%: 20,45 -> 21,43;
quem segue em 44 h: 2 h extras/semana x 5 = 10 h/mês x 21,43 = R$ 214,29.
Narração acelerada x1,12 no render ("velocidade" no JSON); palavras.json já vem com os tempos divididos por 1,12."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.25, "soft_ding"), (12.3, "tum"), (24.9, "tum"), (43.0, "tum"), (39.6, "soft_ding"), (59.3, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(12.3, "O SALÁRIO", 24.8), (24.9, "AS HORAS EXTRAS", 42.9), (43.0, "O VALOR DA HORA", 59.2)]
LIN0, LINH = 365, 105


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
        if t0 - 0.6 <= t < t1:
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
            text(c, nome, 230, y + 18, 52, MARKER, TINTA, align="l")
            c.restore()


def faixa(c, t):
    yc = 735
    if t >= 59.3:
        s, cor, tc = "COMPARA NOV x JAN", GOLD, TINTA
    elif t >= 43.0:
        s, cor, tc = "÷ 210 (ERA 220)", (0.10, 0.14, 0.26), GOLD
    elif t >= 24.9:
        s, cor, tc = "PASSOU DE 42h = EXTRA", (0.10, 0.14, 0.26), GOLD
    elif t >= 12.3:
        s, cor, tc = "SALÁRIO NÃO PODE CAIR", (0.10, 0.14, 0.26), VERDE
    else:
        s, cor, tc = "JORNADA: 44h VIRA 42h", (0.10, 0.14, 0.26), GOLD
    t0 = max([x for x in (0, 12.3, 24.9, 43.0, 59.3) if x <= t])
    k = 1 + 0.10 * math.sin(clamp01((t - t0) / 0.35) * math.pi)
    c.save(); c.translate(540, yc); c.scale(k, k)
    rr(c, -390, -62, 780, 124, 30); rgb(c, cor); c.fill()
    text(c, s, 0, 22, 54, MARKER, tc)
    c.restore()


def L(c, t, t0, s, cor=CREME, tc=TINTA, size=46, y=980, anim="left"):
    entra(c, t, t0, 245, y, chip(s, cor, tc, size, -0.03), anim=anim)


def R(c, t, t0, s, cor=CREME, tc=TINTA, size=46, y=980, anim="right"):
    entra(c, t, t0, 800, y, chip(s, cor, tc, size, 0.03), anim=anim)


def detalhes(c, t):
    if t < 6.8:
        a = 1.0 if t < 6.3 else max(0.0, 1 - (t - 6.3) / 0.5)
        c.push_group(); notificacao(c, 540, 1020, 1.55, "Holerite disponível", "Janeiro/2027 · toque para ver", NAVY, "RH"); c.pop_group_to_source(); c.paint_with_alpha(a)
    elif t < 9.0:
        entra(c, t, 6.9, 540, 1000, chip("SALVA E CONFERE", VERMELHO, CREME, 54), anim="stamp")
    elif t < 12.2:
        entra(c, t, 9.1, 540, 1000, chip("CLT que fazia 44h", NAVY, CREME, 50), anim="pop")
    # 1. salário
    elif t < 19.5:
        if t >= 13.9: L(c, t, 13.9, "44h vira 42h")
        if t >= 17.7: R(c, t, 17.7, "salário igual", VERDE, CREME, anim="stamp")
    elif t < 24.8:
        L(c, t, 19.6, "NOV R$ 3.000")
        if t >= 22.0: R(c, t, 22.0, "JAN R$ 3.000", VERDE, CREME, anim="stamp")
        if t >= 23.3: L(c, t, 23.3, "nem R$ 1 a menos", VERMELHO, CREME, 38, y=1095, anim="pop")
    # 2. horas extras
    elif t < 26.8:
        pass
    elif t < 33.1:
        if t >= 27.9: L(c, t, 27.9, "passou de 42h?")
        if t >= 31.1: R(c, t, 31.1, "+50% no mínimo", VERDE, CREME, anim="stamp")
    elif t < 39.5:
        L(c, t, 33.2, "ainda faz 44h")
        if t >= 35.5: R(c, t, 35.5, "2h extras/semana", CREME, TINTA, 42)
        if t >= 37.8: L(c, t, 37.8, "~10h no mês", NAVY, CREME, 40, y=1095, anim="pop")
    elif t < 42.9:
        entra(c, t, 39.6, 540, 1000, chip("+ de R$ 200 no mês", GOLD, TINTA, 56), anim="stamp")
    # 3. valor da hora
    elif t < 44.8:
        pass
    elif t < 49.4:
        L(c, t, 44.9, "÷ 210", VERDE, CREME, 56, anim="stamp")
        if t >= 47.6: R(c, t, 47.6, "não ÷ 220", VERMELHO, CREME, 50)
    elif t < 54.4:
        L(c, t, 49.6, "hora R$ 13,64")
        if t >= 52.7: R(c, t, 52.7, "agora R$ 14,29", VERDE, CREME, 50, anim="stamp")
    elif t < 59.2:
        L(c, t, 54.5, "extra R$ 20,45")
        if t >= 57.5: R(c, t, 57.5, "agora R$ 21,43", VERDE, CREME, 50, anim="stamp")
    # faz assim
    elif t < 64.5:
        if t >= 60.6: L(c, t, 60.6, "holerite NOV")
        if t >= 62.8: R(c, t, 62.8, "holerite JAN")
        if t >= 63.4: L(c, t, 63.4, "linha por linha", NAVY, CREME, 38, y=1095, anim="pop")
    elif t < 69.2:
        if t >= 65.7: L(c, t, 65.7, "1º RH")
        if t >= 67.3: R(c, t, 67.3, "2º sindicato")
    else:
        entra(c, t, 69.3, 540, 1000, chip("VAI CONFERIR? COMENTA", GOLD, TINTA, 50), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "HOLERITE DE JANEIRO", 540, 235, 58, CREME)
    lista(c, t)
    faixa(c, t)
    poses = ((0, "present"), (4.2, "finger_up"), (6.9, "point_r"), (12.3, "finger_up"), (13.9, "point_r"), (17.7, "present"),
             (23.3, "head"), (24.9, "finger_up"), (31.1, "point_r"), (33.2, "shrug"), (39.6, "arms_up"), (43.0, "finger_up"),
             (49.6, "point_r"), (54.5, "present"), (59.3, "finger_up"), (64.6, "shrug"), (65.7, "point_r"), (69.3, "present"))
    exprs = ((0, "confident"), (6.9, "grin"), (12.3, "confident"), (23.3, "shocked"), (24.9, "confident"), (33.2, "think"),
             (39.6, "grin"), (43.0, "confident"), (52.7, "grin"), (64.6, "think"), (65.7, "confident"), (69.3, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
