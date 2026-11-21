"""CHECKLIST DO CONSULTOR: "4 passos pra juntar os primeiros R$ 10 mil" (TikTok vertical, ~75,6 s, estilo ilustrado).
1º item da lista "Checklist do Consultor" (10h). Modelo: videos/checklist-desafio-3mil-2027.
Contas (contas.py): CDI 13,65%, IR 17,5% -> ~11,3% a.a.; R$ 300 = 30 meses, R$ 500 = 19, R$ 1.000 = 10;
R$ 500 x poupança em 19 meses: ~R$ 230; R$ 500 + R$ 1.000 do 13º em cada dezembro: 15 meses."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (8.3, "tum"), (22.8, "tum"), (40.8, "tum"), (52.8, "tum"), (69.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(8.3, "O VALOR QUE CABE", 22.7), (22.8, "ONDE DEIXAR", 40.7), (40.8, "ACELERA COM O EXTRA", 52.7),
          (52.8, "COMEMORA AS METAS", 65.1)]
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
        if t >= t1:
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
    if t >= 69.9:
        k = 1 + 0.12 * math.sin(clamp01((t - 69.9) / 0.35) * math.pi)
        c.save(); c.translate(540, yc); c.scale(k, k)
        rr(c, -410, -70, 820, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "R$ 10 MIL EM 15 MESES", 0, 26, 66, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, yc - 65, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()

    def lab(s, size=42):
        text(c, s, 335, yc + 18, size, MARKER, CREME)

    def val(s, col=GOLD, size=72):
        numero_i(c, s, 715, yc + 26, size, col)
    if t < 12.9:
        lab("META"); contador(c, t, 0.0, 0, 10000, 700, yc, 84, d=1.6, col=VERDE)
    elif t < 17.7:
        lab("R$ 300/MÊS", 38); val("2,5 ANOS") if t >= 15.4 else val("...", CREME)
    elif t < 20.6:
        lab("R$ 500/MÊS", 38); val("19 MESES") if t >= 19.0 else val("...", CREME)
    elif t < 22.8:
        lab("R$ 1.000/MÊS", 34); val("10 MESES") if t >= 21.6 else val("...", CREME)
    elif t < 32.6:
        lab("META"); val("R$ 10.000", VERDE, 76)
    elif t < 40.8:
        lab("X POUPANÇA", 38)
        if t >= 34.5:
            contador(c, t, 34.5, 0, 230, 700, yc, 84, d=1.0, col=VERDE, prefixo="+R$ ")
        else:
            val("R$ 500/MÊS", CREME, 56)
    elif t < 49.3:
        lab("R$ 500/MÊS", 38); val("19 MESES", CREME)
    elif t < 52.8:
        lab("COM O 13º", 40); contador(c, t, 49.3, 19, 15, 700, yc, 84, d=0.8, col=GOLD, prefixo="", sufixo=" MESES")
    elif t < 65.2:
        lab("GUARDADO", 40)
        if t < 55.5:
            val("R$ 0", CREME)
        elif t < 56.1:
            contador(c, t, 55.5, 0, 1000, 700, yc, 84, d=0.5, col=GOLD)
        elif t < 57.4:
            contador(c, t, 56.1, 1000, 2500, 700, yc, 84, d=0.6, col=GOLD)
        else:
            contador(c, t, 57.4, 2500, 5000, 700, yc, 84, d=0.6, col=VERDE)
    else:
        lab("R$ 500 + 13º", 36); val("R$ 10 MIL", VERDE, 72)


def detalhes(c, t):
    if t < 8.2:
        a = 1.0 if t < 7.6 else max(0.0, 1 - (t - 7.6) / 0.5)
        c.push_group(); notificacao(c, 540, 1040, 1.55, "Meta: R$ 10.000", "os primeiros 10 mil", GOLD, "COFRE"); c.pop_group_to_source(); c.paint_with_alpha(a)
    # passo 1
    if 9.1 <= t < 12.9:
        entra(c, t, 9.1, *L1, chip("o que cabe", VERDE, CREME, 46, -0.04), anim="left")
        if t >= 11.5:
            entra(c, t, 11.5, *R1, chip("não a vontade", VERMELHO, CREME, 40, 0.04), anim="stamp")
    if 12.9 <= t < 20.6:
        entra(c, t, 12.9, *L1, chip("R$ 300", CREME, TINTA, 50, -0.04), anim="left")
        if t >= 15.4:
            entra(c, t, 15.4, *R1, chip("2 anos e meio", GOLD, TINTA, 42, 0.04), anim="stamp")
        if t >= 17.7:
            entra(c, t, 17.7, *L2, chip("R$ 500", CREME, TINTA, 50, 0.03), anim="left")
        if t >= 19.0:
            entra(c, t, 19.0, *R2, chip("1 ano e 7 meses", GOLD, TINTA, 38, -0.03), anim="stamp")
    if 20.6 <= t < 22.8:
        entra(c, t, 20.6, *L1, chip("R$ 1.000", CREME, TINTA, 50, -0.04), anim="left")
        if t >= 21.6:
            entra(c, t, 21.6, *R1, chip("10 meses", VERDE, CREME, 46, 0.04), anim="stamp")
    # passo 2
    if 25.1 <= t < 32.6:
        entra(c, t, 25.1, *L1, chip("conta separada", CREME, TINTA, 40, -0.04), anim="left")
        if t >= 27.2:
            entra(c, t, 27.2, *R1, chip("100% do CDI", GOLD, TINTA, 44, 0.04), anim="stamp")
        if t >= 29.1:
            entra(c, t, 29.1, *L2, chip("resgate no dia", CREME, TINTA, 40, 0.03), anim="left")
        if t >= 30.9:
            entra(c, t, 30.9, *R2, chip("garantia FGC", NAVY, CREME, 42, -0.03), anim="right")
    if 34.5 <= t < 38.1:
        entra(c, t, 34.5, *C1, chip("+ R$ 230 que a poupança", VERDE, CREME, 44), anim="stamp")
    if 38.1 <= t < 40.8:
        entra(c, t, 38.3, *C1, chip("LONGE DO APP DE GASTAR", VERMELHO, CREME, 44), anim="stamp")
    # passo 3
    if 42.6 <= t < 50.8:
        entra(c, t, 42.6, *L1, chip("dinheiro extra", CREME, TINTA, 42, -0.04), anim="left")
        if t >= 44.5:
            entra(c, t, 44.5, *R1, chip("R$ 1.000 do 13º", GOLD, TINTA, 42, 0.04), anim="stamp")
        if t >= 46.7:
            entra(c, t, 46.7, *L2, chip("todo dezembro", CREME, TINTA, 40, 0.03), anim="left")
        if t >= 49.3:
            entra(c, t, 49.3, *R2, chip("15 MESES", VERDE, CREME, 48, -0.03), anim="stamp")
    if 50.8 <= t < 52.8:
        entra(c, t, 50.8, *C1, chip("4 MESES MAIS CEDO", GOLD, TINTA, 52), anim="stamp")
    # passo 4
    if 55.5 <= t < 58.5:
        entra(c, t, 55.5, *L1, chip("R$ 1.000", GOLD, TINTA, 46, -0.04), anim="stamp")
        if t >= 56.1:
            entra(c, t, 56.1, *R1, chip("R$ 2.500", GOLD, TINTA, 46, 0.04), anim="stamp")
        if t >= 57.4:
            entra(c, t, 57.4, *L2, chip("R$ 5.000", VERDE, CREME, 46, 0.03), anim="stamp")
    if 58.5 <= t < 60.5:
        entra(c, t, 58.5, *C1, chip("o 1º mil é o mais difícil", CREME, TINTA, 42), anim="pop")
    if 60.5 <= t < 65.2:
        if t < 63.4:
            entra(c, t, 61.5, *C1, chip("o rendimento ajuda", VERDE, CREME, 46), anim="stamp")
        else:
            entra(c, t, 63.4, *C1, chip("e você para de mexer", CREME, TINTA, 42), anim="pop")
    if t >= 72.8:
        entra(c, t, 72.8, 540, 1040, chip("QUANTO VOCÊ SEPARA POR MÊS?", GOLD, TINTA, 46), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "OS PRIMEIROS R$ 10 MIL", 540, 235, 58, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "present"), (3.6, "finger_up"), (5.9, "present"), (8.3, "finger_up"), (11.5, "shrug"), (12.9, "point_r"),
             (20.6, "arms_up"), (22.8, "finger_up"), (25.1, "point_r"), (32.6, "present"), (38.1, "finger_up"),
             (40.8, "finger_up"), (44.0, "point_r"), (50.8, "arms_up"), (52.8, "finger_up"), (55.5, "arms_up"),
             (58.5, "head"), (60.5, "present"), (65.2, "finger_up"), (69.9, "arms_up"), (72.8, "present"))
    exprs = ((0, "think"), (3.6, "confident"), (5.9, "grin"), (8.3, "confident"), (11.5, "think"), (12.9, "confident"),
             (20.6, "grin"), (22.8, "confident"), (34.5, "grin"), (38.1, "think"), (40.8, "confident"), (50.8, "grin"),
             (52.8, "confident"), (55.5, "grin"), (58.5, "think"), (60.5, "confident"), (69.9, "grin"))
    consultor_i(c, t, 540, 2200, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]


# --- 21/11/2026: narração refeita com a voz nova (clone B). As cenas acima estão nos tempos da narração
# antiga (Afonso, palavras_afonso.json); aqui cada palavra da narração nova é ligada à mesma palavra da
# antiga, e o tempo das cenas e dos sons é convertido por interpolação linear entre essas âncoras.
import json as _json, os as _os
_d = _os.path.dirname(_os.path.abspath(__file__))
_old = _json.load(open(_os.path.join(_d, "palavras_afonso.json"), encoding="utf-8"))
_new = _json.load(open(_os.path.join(_d, "palavras.json"), encoding="utf-8"))
_A = [(0.0, 0.0)]
for _o, _n in zip(_old, _new):
    for _k in ("t0", "t1"):
        if _n[_k] > _A[-1][0] and _o[_k] > _A[-1][1]:
            _A.append((_n[_k], _o[_k]))


def _interp(x, xs, ys):
    if x <= xs[0]:
        return ys[0] + (x - xs[0])
    for i in range(1, len(xs)):
        if x <= xs[i]:
            f = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return ys[i - 1] + f * (ys[i] - ys[i - 1])
    return ys[-1] + (x - xs[-1])


_NX, _OX = [a for a, _ in _A], [b for _, b in _A]
novo_para_antigo = lambda t: _interp(t, _NX, _OX)
antigo_para_novo = lambda t: _interp(t, _OX, _NX)


def _warp(fn):
    def g(c, t):
        return fn(c, novo_para_antigo(t))
    return g


SCENES = [(antigo_para_novo(a), b if b >= 900 else antigo_para_novo(b), _warp(f)) for a, b, f in SCENES]
SFX = [(antigo_para_novo(t), n) for t, n in SFX]
