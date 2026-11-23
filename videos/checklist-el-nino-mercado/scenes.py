"""CHECKLIST DO CONSULTOR: "El Niño vai encarecer o mercado: 3 passos" (TikTok vertical, ~72 s, estilo ilustrado).
1º item [10h Checklist] da Fila do Matheus (24/11/2026). Modelo: videos/checklist-antes-de-parcelar.
Contas (contas.py): El Niño soma 1 a 3,4 p.p. na inflação da comida, cenário extremo (2015-16) quase 7; mercado R$ 800 x 7% = +R$ 56/mês;
estoque de 1 mês dos básicos ~R$ 150 uma vez; -1 kg carne vermelha (~R$ 45) +1 kg frango (~R$ 20) = ~R$ 25/semana = R$ 100/mês; sobram R$ 44."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (11.6, "tum"), (30.0, "tum"), (46.2, "tum"), (67.8, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(11.6, "DESCOBRE QUANTO SOBE", 29.9), (30.0, "ADIANTA OS BÁSICOS", 46.1), (46.2, "MEXE NA CARNE", 62.2)]
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
    if t >= 67.8:
        k = 1 + 0.12 * math.sin(clamp01((t - 67.8) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -430, -70, 860, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "SOBRAM R$ 44 POR MÊS", 0, 26, 64, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=42):
        text(c, s, 345, yc + 16, size, MARKER, CREME)

    def val(s, col=GOLD, size=72):
        numero_i(c, s, 720, yc + 26, size, col)

    def cont(t0, a, b, col, pref="R$ ", suf="", d=0.8):
        contador(c, t, t0, a, b, 710, yc, 76, d=d, col=col, prefixo=pref, sufixo=suf)
    if t < 11.6:
        lab("SEU MERCADO", 40); cont(0.0, 0, 800, CREME, d=1.6)
    elif t < 23.2:
        lab("COMIDA SOBE", 40)
        if t < 16.9:
            val("?", CREME, 80)
        elif t < 21.9:
            val("+1 A 3%", VERMELHO, 66)
        else:
            cont(21.9, 3, 7, VERMELHO, pref="+", suf="%", d=0.6)
    elif t < 25.6:
        lab("MERCADO", 44); val("R$ 800", CREME, 76)
    elif t < 30.0:
        lab("A MAIS/MÊS", 40); cont(25.6, 0, 56, VERMELHO, pref="+R$ ")
    elif t < 42.0:
        lab("ESTOQUE", 44); val("1 MÊS", CREME, 72)
    elif t < 46.2:
        lab("UMA VEZ SÓ", 40); cont(42.0, 0, 150, GOLD)
    elif t < 58.8:
        lab("PIOR CENÁRIO", 36); val("+R$ 56", VERMELHO, 76)
    elif t < 60.8:
        lab("POR SEMANA", 40); cont(58.8, 0, 25, VERDE)
    elif t < 65.4:
        lab("POR MÊS", 44); cont(60.8, 25, 100, VERDE)
    else:
        lab("SOBRA", 46); cont(65.4, 100, 44, VERDE, d=1.2)


def detalhes(c, t):
    if t < 7.0:
        a = 1.0 if t < 6.6 else max(0.0, 1 - (t - 6.6) / 0.4)
        c.push_group()
        notificacao(c, 540, 930, 1.5, "El Niño forte: dez a mar", "comida pode ficar mais cara", VERMELHO, "CLIMA")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if 7.0 <= t < 11.6:
        entra(c, t, 7.0, *C1, chip("3 PASSOS ANTES DA COMPRA", GOLD, TINTA, 44), anim="stamp")
        if t >= 9.7:
            entra(c, t, 9.7, *C2, chip("salva pro dia do mercado", CREME, TINTA, 40), anim="pop")
    # passo 1
    if 12.3 <= t < 19.2:
        entra(c, t, 12.3, *C1, chip("QUANTO PODE SUBIR?", CREME, TINTA, 46), anim="stamp")
        if t >= 16.9:
            entra(c, t, 16.9, *C2, chip("+1 a 3 pontos na comida", GOLD, TINTA, 40), anim="pop")
    if 19.2 <= t < 23.2:
        entra(c, t, 19.4, *C1, chip("caso extremo: 2015", CREME, TINTA, 44), anim="pop")
        if t >= 21.9:
            entra(c, t, 21.9, *C2, chip("QUASE +7%", VERMELHO, CREME, 52), anim="stamp")
    if 23.2 <= t < 30.0:
        entra(c, t, 23.4, *L1, chip("mercado R$ 800", CREME, TINTA, 38, -0.04), anim="left")
        if t >= 25.6:
            entra(c, t, 25.6, *R1, chip("x 7%", VERMELHO, CREME, 46, 0.04), anim="right")
        if t >= 28.9:
            entra(c, t, 28.9, *C2, chip("+R$ 56 TODO MÊS", VERMELHO, CREME, 48), anim="stamp")
    # passo 2
    if 32.8 <= t < 35.7:
        entra(c, t, 32.8, *L1, chip("arroz", CREME, TINTA, 46, -0.04), anim="left")
        if t >= 33.4:
            entra(c, t, 33.4, *R1, chip("feijão", CREME, TINTA, 46, 0.04), anim="right")
        if t >= 34.1:
            entra(c, t, 34.1, *L2, chip("macarrão", CREME, TINTA, 44, 0.03), anim="left")
        if t >= 34.9:
            entra(c, t, 34.9, *R2, chip("café", CREME, TINTA, 46, -0.03), anim="right")
    if 35.7 <= t < 38.3:
        entra(c, t, 35.7, *C1, chip("1 MÊS A MAIS", GOLD, TINTA, 50), anim="stamp")
        if t >= 37.3:
            entra(c, t, 37.3, *C2, chip("não 6!", VERMELHO, CREME, 50), anim="stamp")
    if 38.3 <= t < 42.0:
        entra(c, t, 38.3, *L1, chip("estoque grande", CREME, TINTA, 38, -0.04), anim="left")
        if t >= 39.1:
            entra(c, t, 39.1, *R1, chip("prende dinheiro", CREME, TINTA, 38, 0.04), anim="right")
        if t >= 40.5:
            entra(c, t, 40.5, *C2, chip("venceu = lixo", VERMELHO, CREME, 46), anim="stamp")
    if 42.0 <= t < 46.2:
        entra(c, t, 42.0, *C1, chip("uns R$ 150, uma vez", GOLD, TINTA, 44), anim="stamp")
        if t >= 44.8:
            entra(c, t, 44.8, *C2, chip("TRAVA O PREÇO DE HOJE", VERDE, CREME, 44), anim="stamp")
    # passo 3
    if 47.3 <= t < 52.5:
        entra(c, t, 47.8, *C1, chip("CARNE DEVE SUBIR", VERMELHO, CREME, 48), anim="stamp")
        if t >= 50.6:
            entra(c, t, 50.6, *C2, chip("milho da ração mais caro", CREME, TINTA, 38), anim="pop")
    if 52.5 <= t < 58.8:
        entra(c, t, 52.8, *L1, chip("-1 kg carne", VERMELHO, CREME, 40, -0.04), anim="left")
        if t >= 54.5:
            entra(c, t, 54.5, *L2, chip("por semana", CREME, TINTA, 38, 0.03), anim="left")
        if t >= 56.0:
            entra(c, t, 56.0, *R1, chip("+1 kg frango", VERDE, CREME, 40, 0.04), anim="right")
        if t >= 56.9:
            entra(c, t, 56.9, *R2, chip("ou 12 ovos", CREME, TINTA, 40, -0.03), anim="right")
    if 58.8 <= t < 62.3:
        entra(c, t, 59.1, *C1, chip("uns R$ 25 POR SEMANA", VERDE, CREME, 44), anim="stamp")
        if t >= 60.8:
            entra(c, t, 60.8, *C2, chip("R$ 100 POR MÊS", GOLD, TINTA, 48), anim="stamp")
    if 62.3 <= t < 69.1:
        entra(c, t, 63.5, *L1, chip("economia R$ 100", VERDE, CREME, 36, -0.04), anim="left")
        if t >= 65.4:
            entra(c, t, 65.4, *R1, chip("pior cenário R$ 56", VERMELHO, CREME, 32, 0.04), anim="right")
        if t >= 67.8:
            entra(c, t, 67.8, *C2, chip("cobre o pior cenário", VERDE, CREME, 44), anim="stamp")
    if t >= 69.1:
        entra(c, t, 69.1, 540, 930, chip("QUANTO É O SEU MERCADO?", GOLD, TINTA, 46), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "EL NIÑO NO MERCADO", 540, 235, 58, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "shrug"), (3.5, "finger_up"), (6.9, "present"), (9.7, "finger_up"), (11.6, "finger_up"), (14.2, "present"),
             (19.2, "head"), (23.2, "point_r"), (28.9, "shrug"), (30.0, "finger_up"), (32.8, "present"), (37.3, "finger_up"),
             (38.3, "shrug"), (42.0, "present"), (44.8, "arms_up"), (46.2, "finger_up"), (47.8, "head"), (52.5, "point_r"),
             (58.8, "present"), (60.8, "arms_up"), (62.3, "finger_up"), (67.8, "arms_up"), (69.1, "present"))
    exprs = ((0, "think"), (3.5, "confident"), (19.2, "shocked"), (23.2, "confident"), (28.9, "think"), (30.0, "confident"),
             (40.5, "think"), (42.0, "grin"), (46.2, "confident"), (47.8, "shocked"), (52.5, "confident"), (60.8, "grin"),
             (62.3, "confident"), (67.8, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
