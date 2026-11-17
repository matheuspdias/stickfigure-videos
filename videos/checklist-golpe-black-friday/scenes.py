"""CHECKLIST DO CONSULTOR · "3 sinais de golpe na Black Friday" (TikTok vertical, ~73 s). Modelo: videos/checklist-13-caiu.
Black Friday 2026: 27/11. Exemplo: celular, R$ 2.000 no bolso.
1) desconto de mentira: "de R$ 2.800 por R$ 2.000", em outubro custava R$ 1.900 -> paga R$ 100 a mais.
2) loja desconhecida só no Pix: R$ 1.400 (30% abaixo de R$ 2.000); golpe = R$ 1.400 que não voltam.
3) "sem juros" com juros: 10 x R$ 220 = R$ 2.200 x R$ 2.000 à vista -> R$ 200 escondidos (~1,9% ao mês).
Em jogo numa compra só: 100 + 1.400 + 200 = R$ 1.700."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.25, "soft_ding"), (10.4, "tum"), (19.6, "tum"), (38.2, "tum"), (58.1, "tum"), (65.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(10.4, "O DESCONTO DE MENTIRA", 26.0), (26.6, "A LOJA SÓ NO PIX", 47.4), (48.0, "SEM JUROS COM JUROS", 64.6)]
L1, L2, R1, R2 = (240, 990), (240, 1100), (800, 990), (800, 1100)


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
    rr(c, 70 + 8, 290 + 10, 850, 390, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 70, 290, 850, 390, 30); rgb(c, CREME); c.fill()
    for i, (t0, nome, t1) in enumerate(PASSOS):
        y = 368 + i * 118
        if t0 - 0.6 <= t < t1:
            rr(c, 86, y - 48, 818, 96, 20); rgb(c, GOLD, 0.35); c.fill()
        c.new_sub_path(); c.arc(150, y, 36, 0, 6.283); rgb(c, VERDE if t >= t1 else NAVY); c.fill()
        if t >= t1:
            c.move_to(133, y); c.line_to(146, y + 15); c.line_to(170, y - 15); rgb(c, CREME); c.set_line_width(9); c.stroke()
        else:
            text(c, str(i + 1), 150, y + 16, 44, MARKER, CREME)
        if t < t0:
            c.move_to(210, y + 18); c.line_to(870, y + 18); rgb(c, TINTA, 0.25); c.set_line_width(5); c.set_dash([16, 12]); c.stroke(); c.set_dash([])
        else:
            k = ease_out(clamp01((t - t0) / 0.5))
            c.save(); c.rectangle(205, y - 50, 700 * k, 100); c.clip()
            text(c, nome, 210, y + 17, 46, MARKER, TINTA, align="l")
            c.restore()


def marcador(c, t):
    if t >= 65.9:
        k = 1 + 0.12 * math.sin(clamp01((t - 65.9) / 0.35) * math.pi)
        c.save(); c.translate(540, 790); c.scale(k, k)
        rr(c, -370, -70, 740, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "R$ 1.700 EM JOGO", 0, 30, 78, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, 725, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    if t < 10.4:
        text(c, "NO BOLSO", 300, 810, 46, MARKER, CREME)
        contador(c, t, 0.0, 0, 2000, 670, 790, 84, d=1.0, col=VERDE)
        return
    text(c, "EM JOGO", 290, 810, 50, MARKER, CREME)
    if t < 19.6:
        numero_i(c, "R$ 0", 670, 820, 84, CREME)
    elif t < 38.2:
        contador(c, t, 19.6, 0, 100, 670, 790, 84, d=0.6, col=VERMELHO)
        if t < 23.0:
            entra(c, t, 19.6, 830, 720, chip("+ R$ 100", VERMELHO, CREME, 40, 0.04), anim="stamp")
    elif t < 58.1:
        contador(c, t, 38.2, 100, 1500, 670, 790, 84, d=0.8, col=VERMELHO)
        if t < 41.5:
            entra(c, t, 38.2, 830, 720, chip("+ R$ 1.400", VERMELHO, CREME, 40, 0.04), anim="stamp")
    else:
        contador(c, t, 58.1, 1500, 1700, 670, 790, 84, d=0.6, col=VERMELHO)
        if t < 61.5:
            entra(c, t, 58.1, 830, 720, chip("+ R$ 200", VERMELHO, CREME, 40, 0.04), anim="stamp")


def detalhes(c, t):
    if t < 7.9:
        a = 1.0 if t < 7.4 else max(0.0, 1 - (t - 7.4) / 0.5)
        c.push_group(); notificacao(c, 540, 1040, 1.55, "BLACK FRIDAY 27/11", "Até 70% OFF · só hoje!", VERMELHO, "LOJA")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if 8.2 <= t < 10.4:
        entra(c, t, 8.2, 540, 1040, chip("R$ 2.000 pro celular", VERDE, CREME, 50), anim="pop")
    # sinal 1: desconto de mentira
    if 13.1 <= t < 22.7:
        entra(c, t, 13.1, *L1, chip("de R$ 2.800", VERMELHO, CREME, 46, -0.04), anim="left")
        entra(c, t, 15.6, *R1, chip("por R$ 2.000", VERDE, CREME, 46, 0.04), anim="right")
    if 16.7 <= t < 22.7:
        entra(c, t, 16.7, *L2, chip("outubro: R$ 1.900", CREME, TINTA, 40, 0.03), anim="left")
    if 19.6 <= t < 22.7:
        entra(c, t, 19.6, *R2, chip("R$ 100 A MAIS", VERMELHO, CREME, 42, -0.03), anim="stamp")
    if 22.7 <= t < 26.4:
        entra(c, t, 23.4, 540, 1040, chip("PRINT DO PREÇO HOJE", GOLD, TINTA, 50), anim="pop")
    # sinal 2: loja só no Pix
    if 29.5 <= t < 40.8:
        entra(c, t, 29.5, *L1, chip("loja que nunca viu", CREME, TINTA, 38, -0.04), anim="left")
        entra(c, t, 32.3, *R1, chip("R$ 1.400 só Pix", VERMELHO, CREME, 42, 0.04), anim="right")
    if 34.6 <= t < 40.8:
        entra(c, t, 34.6, *L2, chip("30% abaixo de todos", CREME, TINTA, 38, 0.03), anim="left")
    if 38.2 <= t < 40.8:
        entra(c, t, 38.2, *R2, chip("NÃO VOLTA", VERMELHO, CREME, 46, -0.03), anim="stamp")
    if 40.8 <= t < 47.8:
        entra(c, t, 42.1, *L1, chip("CNPJ", CREME, TINTA, 52, -0.04), anim="left")
        entra(c, t, 43.2, *R1, chip("Reclame Aqui", CREME, TINTA, 46, 0.04), anim="right")
        entra(c, t, 45.5, 540, 1110, chip("desconhecida? SÓ CARTÃO", GOLD, TINTA, 44), anim="pop")
    # sinal 3: sem juros com juros
    if 51.1 <= t < 60.9:
        entra(c, t, 51.1, *L1, chip("10x de R$ 220", CREME, TINTA, 46, -0.04), anim="left")
    if 53.2 <= t < 58.1:
        entra(c, t, 53.2, *R1, chip("sem juros?", CREME, TINTA, 46, 0.04), anim="right")
    if 58.1 <= t < 60.9:
        entra(c, t, 58.1, *R1, chip("R$ 200 escondidos", VERMELHO, CREME, 38, 0.04), anim="stamp")
    if 54.5 <= t < 60.9:
        entra(c, t, 54.5, *L2, chip("= R$ 2.200", VERMELHO, CREME, 46, 0.03), anim="left")
    if 56.1 <= t < 60.9:
        entra(c, t, 56.1, *R2, chip("à vista R$ 2.000", VERDE, CREME, 40, -0.03), anim="right")
    if 60.9 <= t < 65.6:
        entra(c, t, 61.6, 540, 1040, chip("PARCELA x VEZES", GOLD, TINTA, 52), anim="pop")
    if t >= 69.4:
        entra(c, t, 69.4, 540, 1040, chip("QUAL TENTARAM COM VOCÊ?", GOLD, TINTA, 46), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "GOLPES NA BLACK FRIDAY", 540, 235, 56, CREME)
    lista(c, t)
    marcador(c, t)
    poses = ((0, "present"), (2.4, "finger_up"), (7.8, "present"), (10.4, "finger_up"), (13.1, "point_r"), (19.5, "shrug"),
             (22.7, "finger_up"), (26.6, "finger_up"), (29.5, "point_r"), (38.1, "shrug"), (40.8, "finger_up"), (44.2, "present"),
             (48.0, "finger_up"), (51.1, "point_r"), (58.0, "shrug"), (60.9, "finger_up"), (64.9, "present"), (69.4, "present"))
    exprs = ((0, "confident"), (19.5, "shocked"), (22.7, "confident"), (38.1, "shocked"), (40.8, "confident"), (58.0, "shocked"),
             (60.9, "confident"), (65.9, "shocked"), (69.4, "grin"))
    consultor_i(c, t, 540, 2250, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
