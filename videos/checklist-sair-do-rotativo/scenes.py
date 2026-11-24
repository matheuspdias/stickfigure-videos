"""CHECKLIST DO CONSULTOR: "5 passos pra sair do rotativo do cartão" (TikTok vertical, ~72,5 s, estilo ilustrado, quadro navy).
1º item da lista Checklist do Consultor (25/11/2026, 10h). Modelo: videos/checklist-el-nino-mercado.
Contas (contas.py): rotativo 451,7% a.a. (BC, set/2026) = ~15,3% a.m.; R$ 1.000 -> ~R$ 1.150 em 1 mês; dobra em ~5 meses;
teto da Lei 14.690/2023 (desde 03/01/2024): juros e encargos até 100% da dívida; consignado ~R$ 20 a 30 por mês em R$ 1.000."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (10.4, "tum"), (16.2, "tum"), (29.0, "tum"), (40.3, "tum"), (52.6, "tum"), (68.7, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(10.4, "GUARDA O CARTÃO", 16.1), (16.2, "OLHA O TAMANHO", 28.9), (29.0, "NÃO PAGA SÓ O MÍNIMO", 40.2),
          (40.3, "TROCA POR UMA MAIS BARATA", 52.5), (52.6, "CONHECE O TETO", 68.6)]
LIN0, LINH = 342, 88
YC = 832
L1, L2, R1, R2 = (255, 960), (255, 1060), (790, 960), (790, 1060)
C1, C2 = (540, 955), (540, 1050)


def m(s):
    return s.replace("2.", "2 .")


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
    rr(c, 70 + 8, 285 + 10, 850, 470, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 70, 285, 850, 470, 30); rgb(c, CREME); c.fill()
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = LIN0 + i * LINH
        ativo = t0 - 0.6 <= t < t1
        if ativo:
            rr(c, 86, y - 41, 818, 82, 18); rgb(c, GOLD, 0.35); c.fill()
        c.new_sub_path(); c.arc(150, y, 31, 0, 6.283); rgb(c, VERDE if t >= t1 else NAVY); c.fill()
        if t >= t1:
            c.move_to(136, y); c.line_to(148, y + 13); c.line_to(168, y - 13); rgb(c, CREME); c.set_line_width(8); c.stroke()
        else:
            text(c, str(i + 1), 150, y + 14, 40, MARKER, CREME)
        if t < t0:
            c.move_to(210, y + 17); c.line_to(870, y + 17); rgb(c, TINTA, 0.25); c.set_line_width(5); c.set_dash([16, 12]); c.stroke(); c.set_dash([])
        else:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(205, y - 48, 690 * k, 96); c.clip()
            text(c, nome, 210, y + 15, 42, MARKER, TINTA, align="l")
            c.restore()


def marcador(c, t):
    yc = YC
    if t >= 68.7:
        k = 1 + 0.12 * math.sin(clamp01((t - 68.7) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -430, -68, 860, 136, 30); rgb(c, GOLD); c.fill()
        text(c, "SAI ANTES DO 5º MÊS", 0, 24, 62, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 62, 780, 124, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=40):
        text(c, s, 345, yc + 15, size, MARKER, CREME)

    def val(s, col=GOLD, size=70):
        numero_i(c, m(s), 720, yc + 25, size, col)

    def cont(t0, a, b, col, pref="R$ ", suf="", d=0.8):
        contador(c, t, t0, a, b, 710, yc, 72, d=d, col=col, prefixo=pref, sufixo=suf)
    if t < 3.0:
        lab("SUA FATURA", 40); cont(0.0, 0, 1000, CREME, d=1.2)
    elif t < 16.2:
        lab("1 MÊS DEPOIS", 38)
        if t < 4.4:
            val("R$ 1.000", CREME, 70)
        else:
            cont(4.4, 1000, 1150, VERMELHO, d=1.0)
    elif t < 22.6:
        lab("JUROS/ANO", 40)
        if t < 20.1:
            val("?", CREME, 76)
        else:
            cont(20.1, 0, 450, VERMELHO, pref="~", suf="%", d=0.9)
    elif t < 24.7:
        lab("JUROS/MÊS", 40); cont(23.0, 0, 15, VERMELHO, pref="~", suf="%", d=0.6)
    elif t < 29.0:
        lab("EM 30 DIAS", 40)
        if t < 25.9:
            val("R$ 1.000", CREME, 70)
        else:
            cont(25.9, 0, 150, VERMELHO, pref="+R$ ", d=0.7)
    elif t < 32.1:
        lab("SÓ O MÍNIMO?", 36); val("NÃO", VERMELHO, 72)
    elif t < 35.1:
        lab("DEPOIS DE", 40); val("30 DIAS", CREME, 66)
    elif t < 40.3:
        lab("O BANCO", 42); val("PARCELA", GOLD, 64)
    elif t < 47.7:
        lab("ROTATIVO", 42); val("+R$ 150", VERMELHO, 70)
    elif t < 52.6:
        lab("CONSIGNADO", 38)
        if t < 49.0:
            val("?", CREME, 76)
        else:
            val("R$ 20 A 30", VERDE, 54)
    elif t < 61.3:
        lab("TETO DA LEI", 38); val("100%", GOLD, 72)
    elif t < 65.7:
        lab("NO MÁXIMO", 40)
        if t < 63.3:
            val("R$ 1.000", CREME, 70)
        else:
            cont(63.3, 1000, 2000, VERMELHO, d=0.8)
    else:
        lab("ROTATIVO", 42)
        if t < 67.4:
            val("R$ 2.000", VERMELHO, 70)
        else:
            val("5 MESES", VERMELHO, 66)


def detalhes(c, t):
    if t < 6.3:
        a = 1.0 if t < 5.9 else max(0.0, 1 - (t - 5.9) / 0.4)
        c.push_group()
        notificacao(c, 540, 1000, 1.5, "Fatura não paga", "R$ 1.000 foi pro rotativo", VERMELHO, "CARTÃO")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if 6.3 <= t < 10.4:
        entra(c, t, 6.5, *C1, chip("5 PASSOS PRA SAIR", GOLD, TINTA, 46), anim="stamp")
        if t >= 8.4:
            entra(c, t, 8.4, *C2, chip("salva pro dia da fatura", CREME, TINTA, 40), anim="pop")
    # passo 1
    if 11.2 <= t < 16.2:
        entra(c, t, 11.2, *C1, chip("GUARDA O CARTÃO", CREME, TINTA, 48), anim="stamp")
        if t >= 12.5:
            entra(c, t, 12.5, *C2, chip("compra nova = mais juros", VERMELHO, CREME, 40), anim="pop")
    # passo 2
    if 17.3 <= t < 22.6:
        entra(c, t, 17.3, *C1, chip("o tamanho do buraco", CREME, TINTA, 44), anim="pop")
        if t >= 20.1:
            entra(c, t, 20.1, *C2, chip("~450% AO ANO", VERMELHO, CREME, 50), anim="stamp")
    if 22.6 <= t < 29.0:
        entra(c, t, 23.0, *C1, chip("~15% AO MÊS", VERMELHO, CREME, 50), anim="stamp")
        if t >= 24.9:
            entra(c, t, 24.9, *L2, chip("R$ 1.000", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 26.3:
            entra(c, t, 26.3, *R2, chip(m("+R$ 150 em 30 dias"), VERMELHO, CREME, 36, 0.04), anim="right")
    # passo 3
    if 30.1 <= t < 32.1:
        entra(c, t, 30.1, *C1, chip("SÓ O MÍNIMO? NÃO!", VERMELHO, CREME, 48), anim="stamp")
    if 32.1 <= t < 38.5:
        entra(c, t, 32.3, *C1, chip("1 mês no rotativo", CREME, TINTA, 44), anim="pop")
        if t >= 34.6:
            entra(c, t, 34.6, *C2, chip("banco oferece parcelar", GOLD, TINTA, 42), anim="stamp")
    if 38.5 <= t < 40.3:
        entra(c, t, 38.5, *C1, chip("COMPARA OS JUROS", VERDE, CREME, 48), anim="stamp")
    # passo 4
    if 41.4 <= t < 47.7:
        entra(c, t, 41.6, *C1, chip("dívida mais barata", GOLD, TINTA, 44), anim="stamp")
        if t >= 45.0:
            entra(c, t, 45.0, *L2, chip("consignado", CREME, TINTA, 40, -0.04), anim="left")
        if t >= 46.7:
            entra(c, t, 46.7, *R2, chip("uma fração", VERDE, CREME, 40, 0.04), anim="right")
    if 47.7 <= t < 52.6:
        entra(c, t, 47.7, *C1, chip("R$ 1.000 no consignado", CREME, TINTA, 44), anim="pop")
        if t >= 49.0:
            entra(c, t, 49.0, *L2, chip(m("R$ 20 a 30"), VERDE, CREME, 42, -0.04), anim="left")
        if t >= 51.1:
            entra(c, t, 51.1, *R2, chip("não R$ 150", VERMELHO, CREME, 42, 0.04), anim="right")
    # passo 5
    if 53.6 <= t < 57.1:
        entra(c, t, 53.6, *C1, chip("TETO DA LEI", GOLD, TINTA, 50), anim="stamp")
        if t >= 55.1:
            entra(c, t, 55.1, *C2, chip("desde 2024", CREME, TINTA, 42), anim="pop")
    if 57.1 <= t < 61.3:
        entra(c, t, 57.1, *C1, chip("juros + encargos", CREME, TINTA, 44), anim="pop")
        if t >= 59.4:
            entra(c, t, 59.4, *C2, chip("até o valor da dívida", GOLD, TINTA, 42), anim="stamp")
    if 61.3 <= t < 64.2:
        entra(c, t, 61.3, *C1, chip("R$ 1.000", CREME, TINTA, 46), anim="pop")
        if t >= 62.0:
            entra(c, t, 62.0, *C2, chip(m("NUNCA PASSA DE R$ 2.000"), VERMELHO, CREME, 42), anim="stamp")
    if 64.2 <= t < 68.7:
        entra(c, t, 64.4, *C1, chip("não espera chegar lá", CREME, TINTA, 44), anim="pop")
        if t >= 67.2:
            entra(c, t, 67.2, *C2, chip("no rotativo: 5 MESES", VERMELHO, CREME, 44), anim="stamp")
    if t >= 68.7:
        entra(c, t, 68.7, *C1, chip("QUAL É O JURO DO SEU CARTÃO?", GOLD, TINTA, 40), anim="pop")
        if t >= 70.7:
            entra(c, t, 70.7, *C2, chip("olha no app e comenta", CREME, TINTA, 40), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "SAIR DO ROTATIVO", 540, 230, 58, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "head"), (3.0, "shrug"), (6.3, "finger_up"), (8.4, "present"), (10.4, "finger_up"), (12.2, "point_r"),
             (16.2, "finger_up"), (20.1, "head"), (22.6, "present"), (25.9, "shrug"), (29.0, "finger_up"), (32.1, "present"),
             (38.5, "point_r"), (40.3, "finger_up"), (44.1, "present"), (49.0, "present"), (51.1, "shrug"), (52.6, "finger_up"),
             (57.1, "present"), (62.0, "point_r"), (64.2, "finger_up"), (67.2, "head"), (68.7, "present"))
    exprs = ((0, "shocked"), (6.3, "confident"), (20.1, "shocked"), (22.6, "think"), (29.0, "confident"), (49.0, "grin"),
             (51.1, "confident"), (62.0, "confident"), (67.2, "shocked"), (68.7, "grin"))
    consultor_i(c, t, 540, 2270, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
