"""Seu 13º vai vir menor do que você pensa. Só TikTok: vertical nativo 1080x1920, ~65,5 s, estilo ilustrado.
Tema 1 da pesquisa de 22/11/2026, refeito a pedido do Matheus com outra cara (o `segunda-parcela-13-menor` usou colunas):
exemplo único de R$ 3 mil, app do banco, contracheque do 13º e o líquido revelado no fim.
Quadro 0: o saldo do 13º no celular já caindo de R$ 3.000. Narração: Consultor BR B (API HeyGen), 1 bloco. Contas em contas.py."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(21.1, "tum"), (30.5, "tum"), (44.1, "soft_ding"), (55.1, "tum")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

VOCE = "lucas"


def topo(c, s, cor=CREME, contorno=TINTA):
    numero_i(c, s, 520, 235, 58, cor, contorno=contorno)


def selo(s, cor=VERMELHO, size=60, tcol=CREME, rot=-0.06):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(rot)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def pop(c, t, t0, x, y, s, size, col=GOLD, contorno=TINTA):
    if t < t0:
        return
    k = 1 + 0.14 * math.sin(clamp01((t - t0) / 0.3) * math.pi)
    c.save(); c.translate(x, y); c.scale(k, k); numero_i(c, s, 0, 0, size, col, contorno=contorno); c.restore()


def coluna(c, x, base, h, w, cor, rot, valor, vcol=CREME):
    rr(c, x - w / 2 + 8, base - h + 10, w, h, 18); rgb(c, (0, 0, 0), 0.22); c.fill()
    rr(c, x - w / 2, base - h, w, h, 18); rgb(c, cor); c.fill()
    numero_i(c, valor, x, base - h - 50, 64, vcol)
    numero_i(c, rot, x, base + 55, 50, CREME)


def cartao_parcela(c, t, t0, x, y, nome, data, valor, desc=None, t_desc=None, cor=VERDE, s=1.0):
    if t < t0:
        return
    k = ease_out(clamp01((t - t0) / 0.4))
    c.save(); c.translate(x, y + 300 * (1 - k)); c.scale(s, s)
    rr(c, -200 + 8, -260 + 10, 400, 520, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, -200, -260, 400, 520, 30); rgb(c, CREME); c.fill()
    rr(c, -200, -260, 400, 120, 30); rgb(c, cor); c.fill(); c.rectangle(-200, -170, 400, 30); c.fill()
    text(c, nome, 0, -185, 54, MARKER, CREME)
    text(c, data, 0, -60, 46, MARKER, NAVY)
    if desc and t >= t_desc:
        text(c, desc, 0, 40, 40, MARKER, VERMELHO)
    text(c, valor, 0, 170, 70, MARKER, TINTA)
    c.restore()



# ======================================================================= CENAS
def s01(c, t):  # 0 - 4.3  o saldo do 13º já caindo de 3.000 pra 2.751
    luz("tarde")
    cena_sala(c, t, "tarde")
    topo(c, "SEU 13º · SALÁRIO DE R$ 3 MIL")
    p = ease_io(prog(t, 0.0, 2.6))
    v = 3000 - 249 * p
    celular_app(c, t, 640, 760, 1.25, titulo="13º salário", valor=brl(v), cor=VERDE if p < 0.5 else VERMELHO,
                linhas=[("1ª parcela", "+ R$ 1.500", VERDE), ("2ª parcela", "+ R$ 1.251", VERDE), ("INSS do 13º", "- R$ 249", VERMELHO)], t0=0.0, d=2.6)
    if t > 2.8:
        entra(c, t, 2.8, 640, 1150, selo("MENOR!", VERMELHO, 70, CREME), anim="stamp")
    pessoa(c, t, 210, 1330, 1.2, VOCE, poses=((0, "hold"), (1.7, "head")), exprs=((0, "grin"), (1.7, "shocked")), look=0.6)


def s02(c, t):  # 4.3 - 9.3  salário de 3 mil, você espera 3 mil
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1000))
    topo(c, "FAZ A CONTA COMIGO")
    numero_i(c, "SALÁRIO", 540, 420, 64, CREME)
    contador(c, t, 4.5, 0, 3000, 540, 560, 150, d=1.0, col=GOLD)
    if t > 6.6:
        numero_i(c, "VOCÊ ESPERA:", 540, 720, 60, CREME)
        pop(c, t, 7.1, 540, 850, "13º = R$ 3.000?", 86, VERDE)
    consultor_i(c, t, 540, 1440, 0.8, poses=((0, "present"), (6.6, "think")), exprs=((0, "neutral"), (6.6, "think")), look=0.0)


def s03(c, t):  # 9.3 - 11.3  vem em duas parcelas
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "DUAS PARCELAS", NAVY, CREME)
    entra(c, t, 9.6, 330, 700, selo("1ª", VERDE, 140, CREME), anim="pop")
    entra(c, t, 10.1, 750, 700, selo("2ª", NAVY, 140, GOLD, rot=0.06), anim="pop")
    consultor_i(c, t, 540, 1330, 1.1, poses=((0, "point_ru"),), exprs=((0, "confident"),), look=0.0)


def s04(c, t):  # 11.3 - 18.6  a 1ª: até 30/11, 1.500, sem desconto
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    topo(c, "A 1ª PARCELA")
    if t > 11.5:
        k = ease_out(prog(t, 11.5, 0.4))
        notificacao(c, 560, 400 - 200 * (1 - k), 1.2, titulo="13º: 1ª parcela", texto="até 30/11 · segunda-feira", cor=VERDE)
    if t > 14.6:
        numero_i(c, "METADE DO SALÁRIO", 600, 600, 62, CREME)
    contador(c, t, 15.9, 0, 1500, 600, 780, 170, d=0.8, col=GOLD)
    if t > 17.2:
        entra(c, t, 17.2, 600, 1000, selo("SEM DESCONTO", NAVY, 62, GOLD), anim="stamp")
    pessoa(c, t, 200, 1330, 1.15, VOCE, poses=((0, "stand"), (15.9, "thumb")), exprs=((0, "neutral"), (15.9, "grin")), look=0.6)


def s05(c, t):  # 18.6 - 21.9  a 2ª vem igual? não vem
    luz("tarde")
    cena_sala(c, t, "tarde")
    topo(c, "A 2ª VEM IGUAL?")
    numero_i(c, "1ª", 380, 600, 150, VERDE)
    numero_i(c, "=", 590, 600, 150, NAVY)
    if t > 19.9:
        numero_i(c, "2ª", 800, 600, 150, VERDE if t < 21.1 else VERMELHO)
    if t > 21.1:
        c.save(); c.translate(590, 600); x_icon(c, 90); c.restore()
        entra(c, t, 21.2, 600, 860, selo("NÃO VEM", VERMELHO, 80, CREME), anim="stamp")
    pessoa(c, t, 220, 1330, 1.2, VOCE, poses=((0, "stand"), (21.1, "head")), exprs=((0, "grin"), (21.1, "shocked")), look=0.6)


def s06(c, t):  # 21.9 - 28.3  a 2ª: até 18/12, com o INSS do 13º inteiro
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(260, 1100))
    topo(c, "A 2ª PARCELA")
    if t > 22.0:
        k = ease_out(prog(t, 22.0, 0.4))
        notificacao(c, 560, 400 - 200 * (1 - k), 1.2, titulo="13º: 2ª parcela", texto="até 18/12", cor=VERMELHO)
    if t > 25.6:
        entra(c, t, 25.6, 620, 640, selo("INSS", NAVY, 110, GOLD), anim="drop")
    if t > 26.5:
        numero_i(c, "DO 13º INTEIRO", 620, 840, 74, CREME)
    consultor_i(c, t, 200, 1330, 1.15, poses=((0, "present"), (24.7, "point_r")), exprs=((0, "neutral"), (25.6, "confident")), look=0.6)


def s07(c, t):  # 28.3 - 36.1  contracheque do 13º: INSS de 249, tudo na 2ª
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "O DESCONTO DO 13º", NAVY, CREME)
    desc = (("INSS (13º inteiro)", "- R$ 249"),) if t > 30.5 else (("INSS (13º inteiro)", "..."),)
    contracheque(c, 600, 640, 1.3, bruto="R$ 3.000", descontos=desc, liquido="?")
    if t > 30.5:
        pop(c, t, 30.5, 600, 1010, "- R$ 249", 120, VERMELHO)
    if t > 33.5:
        entra(c, t, 33.5, 600, 1160, selo("TUDO NA 2ª PARCELA", NAVY, 52, GOLD), anim="stamp")
    pessoa(c, t, 170, 1360, 1.05, VOCE, poses=((0, "think"), (30.5, "head")), exprs=((0, "think"), (30.5, "desperate")), look=0.6)


def s08(c, t):  # 36.1 - 39.8  a 2ª vem com 1.251
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "AS DUAS PARCELAS")
    base = 1080
    coluna(c, 380, base, 520, 230, VERDE, "1ª", "R$ 1.500")
    if t > 37.0:
        g = ease_out(prog(t, 37.0, 1.2))
        h2 = 520 * 1251 / 1500 * g
        coluna(c, 700, base, h2, 230, VERMELHO, "2ª", brl(int(1251 * g)))
    if t > 38.8:
        entra(c, t, 38.8, 800, 480, selo("- R$ 249", VERMELHO, 56, CREME, rot=0.06), anim="stamp")
    consultor_i(c, t, 540, 1500, 0.6, poses=((0, "present"),), exprs=((0, "neutral"), (37.5, "shocked")), look=0.0)


def s09(c, t):  # 39.8 - 46.3  notícia boa: IR zero no 13º até 5 mil
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    topo(c, "NOTÍCIA BOA")
    if t > 41.5:
        entra(c, t, 41.5, 640, 400, selo("ESTE ANO", NAVY, 60, GOLD), anim="stamp")
    if t > 42.7:
        numero_i(c, "ATÉ R$ 5 MIL", 640, 570, 90, CREME)
    if t > 44.1:
        numero_i(c, "IMPOSTO DE RENDA NO 13º", 640, 700, 50, CREME)
        pop(c, t, 44.3, 640, 860, "R$ 0", 180, GOLD)
    consultor_i(c, t, 200, 1330, 1.2, poses=((0, "stand"), (44.1, "arms_up")), exprs=((0, "neutral"), (44.1, "grin")), look=0.6)


def s10(c, t):  # 46.3 - 51.2  ano passado: uns 24 reais pro Leão
    luz("dia")
    fundo_marca(c, t, "creme")
    topo(c, "SALÁRIO DE R$ 3 MIL", NAVY, CREME)
    for x, ano, cor in ((320, "2025", VERMELHO), (760, "2026", VERDE)):
        if ano == "2026" and t < 46.6:
            continue
        rr(c, x - 200, 360, 400, 420, 28); rgb(c, CREME); c.fill(); rr(c, x - 200, 360, 400, 110, 28); rgb(c, cor); c.fill()
        c.rectangle(x - 200, 430, 400, 40); c.fill()
        text(c, ano, x, 440, 64, MARKER, CREME)
        text(c, "IR NO 13º", x, 560, 48, MARKER, NAVY)
        c.set_line_width(6); rgb(c, NAVY, 0.5); rr(c, x - 200, 360, 400, 420, 28); c.stroke()
    if t > 46.6:
        text(c, "R$ 0", 760, 715, 84, MARKER, VERDE)
    contador(c, t, 49.4, 0, 24, 320, 700, 72, d=0.8, col=VERMELHO, prefixo="-R$ ")
    if t > 50.5:
        entra(c, t, 50.5, 320, 860, selo("PRO LEÃO", VERMELHO, 46, CREME), anim="stamp")
    consultor_i(c, t, 540, 1420, 0.95, poses=((0, "present"), (49.4, "point_ru")), exprs=((0, "neutral"), (49.4, "confident")), look=0.0)


def s11(c, t):  # 51.2 - 57.4  resumo: esperava 3.000, caem 2.751
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    topo(c, "RESUMO")
    if t > 52.2:
        numero_i(c, "VOCÊ ESPERAVA", 540, 400, 58, CREME)
        numero_i(c, "R$ 3.000", 540, 520, 110, CREME)
        if t > 53.9:
            k = ease_out(prog(t, 53.9, 0.3))
            c.rectangle(300, 505, 480 * k, 14); rgb(c, VERMELHO); c.fill()
    if t > 53.9:
        numero_i(c, "NA CONTA, CAEM", 540, 700, 58, CREME)
    contador(c, t, 55.1, 0, 2751, 540, 860, 170, d=1.4, col=GOLD)
    if t > 56.6:
        entra(c, t, 56.6, 540, 990, selo("- R$ 249", VERMELHO, 60, CREME), anim="stamp")
    consultor_i(c, t, 540, 1450, 0.7, poses=((0, "stand"), (55.1, "point_ru")), exprs=((0, "neutral"), (56.5, "shocked")), look=0.0)


def s12(c, t):  # 57.4 - 61.9  a dica
    luz("tarde")
    cena_sala(c, t, "tarde")
    topo(c, "A DICA")
    if t > 58.4:
        entra(c, t, 58.4, 650, 450, selo("VAI PARCELAR PRESENTE?", VERMELHO, 48, CREME), anim="pop")
    if t > 59.7:
        numero_i(c, "CONTA COM A", 650, 640, 66, NAVY, contorno=CREME)
        pop(c, t, 60.3, 650, 780, "2ª MENOR", 110, VERMELHO, contorno=CREME)
    consultor_i(c, t, 220, 1330, 1.2, poses=((0, "finger_up"), (59.7, "point_r")), exprs=((0, "confident"),), look=0.6)


def s13(c, t):  # 61.9 - fim  comenta o seu salário
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(300, 1100))
    topo(c, "E O SEU?")
    numero_i(c, "QUANTO VAI CAIR?", 520, 560, 76, CREME)
    if t > 63.9:
        entra(c, t, 63.9, 620, 800, selo("COMENTA SEU SALÁRIO", NAVY, 50, GOLD), anim="stamp")
    pessoa(c, t, 200, 1330, 1.25, VOCE, poses=((0, "think"), (63.9, "point_r")), exprs=((0, "think"), (63.9, "grin")), look=0.6)


SCENES = [(0, 4.3, s01), (4.3, 9.3, s02), (9.3, 11.3, s03), (11.3, 18.6, s04), (18.6, 21.9, s05),
          (21.9, 28.3, s06), (28.3, 36.1, s07), (36.1, 39.8, s08), (39.8, 46.3, s09), (46.3, 51.2, s10),
          (51.2, 57.4, s11), (57.4, 61.9, s12), (61.9, 999.0, s13)]
