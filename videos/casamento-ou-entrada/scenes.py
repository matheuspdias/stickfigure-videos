"""Festa de casamento de R$ 50 mil ou entrada do apê? Carla x Diego. Só TikTok: vertical nativo 1080x1920, 77,6 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: os dois casais têm R$ 50 mil; Carla gasta tudo na festa; Diego gasta R$ 5 mil (civil + almoço) e usa
R$ 45 mil de entrada. Juntar R$ 50 mil de novo guardando R$ 1.000/mês a 0,8%/mês: 43 meses (~3 anos e meio).
Festa no empréstimo: R$ 50 mil a 4%/mês em 36x = parcela ~R$ 2.644, total ~R$ 95 mil."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(20.4, "tum"), (32.5, "tum"), (61.6, "tum"), (76.8, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ROXO = PURPLE if "PURPLE" in globals() else (0.55, 0.36, 0.72)
ROSA = (0.88, 0.42, 0.52)
CARLA_COR = (0.86, 0.40, 0.36)
DIEGO_COR = (0.30, 0.46, 0.34)


# ---------------------------------------------------------------- helpers
def selo(s, cor=VERMELHO, size=64, tcol=CREME):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(-0.06)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def cartao(lab, val, cor_val=TINTA, w=600, h=104):
    def f(c):
        rr(c, -w / 2 + 6, -h / 2 + 8, w, h, 22); rgb(c, (0, 0, 0), 0.20); c.fill()
        rr(c, -w / 2, -h / 2, w, h, 22); rgb(c, (0.99, 0.99, 0.98)); c.fill()
        text(c, lab, -w / 2 + 30, 2, 46, HAND, (0.2, 0.2, 0.25), align="l")
        text(c, val, w / 2 - 26, 2, 52, MARKER, cor_val, align="r")
    return f


def luzinhas(c, t, y=120, n=3, amp=70):
    """varais de lâmpadas de festa (de borda a borda)"""
    cores = (GOLD, (0.98, 0.86, 0.50), ROSA, (0.70, 0.86, 0.98))
    for k in range(n):
        yy = y + k * 46
        pts = [(x, yy + amp * math.sin(math.pi * x / 1080)) for x in range(-20, 1101, 20)]
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        rgb(c, (0.12, 0.12, 0.16), 0.7); c.set_line_width(3); c.stroke()
        for i, x in enumerate(range(20 + k * 30, 1080, 90)):
            yb = yy + amp * math.sin(math.pi * x / 1080) + 14
            brilho = 0.75 + 0.25 * math.sin(t * 4 + i * 1.7 + k)
            rglow(c, x, yb, 34, cores[(i + k) % 4], 0.35 * brilho)
            ellipse(c, x, yb, 10, 13); rgb(c, cores[(i + k) % 4]); c.fill()


def bolo(c, s=1.0):
    """bolo de casamento de 3 andares (origem = base)"""
    c.save(); c.scale(s, s)
    for i, (w, h) in enumerate(((300, 120), (220, 105), (140, 90))):
        y = -sum(hh for _, hh in ((300, 120), (220, 105), (140, 90))[:i + 1])
        rr(c, -w / 2 + 6, y + 8, w, h, 14); rgb(c, (0, 0, 0), 0.15); c.fill()
        rr(c, -w / 2, y, w, h, 14); rgb(c, (0.99, 0.97, 0.93)); c.fill()
        for j in range(int(w / 40)):
            c.new_sub_path(); c.arc(-w / 2 + 20 + j * 40, y + 6, 12, 0, math.pi); rgb(c, ROSA); c.fill()
    ytopo = -315
    c.rectangle(-70, ytopo + 6, 140, 10); rgb(c, GOLD); c.fill()
    # topo: dois corações
    for dx, col in ((-22, ROSA), (22, VERMELHO)):
        c.save(); c.translate(dx, ytopo - 34)
        c.move_to(0, 22); c.curve_to(-40, -6, -18, -36, 0, -14); c.curve_to(18, -36, 40, -6, 0, 22)
        rgb(c, col); c.fill(); c.restore()
    c.restore()


def predio_icone(c, s=1.0):
    c.save(); c.scale(s, s)
    predio_moderno(c, -130, 0, 260, 480, (0.74, 0.70, 0.64), 0.0, seed=7)
    c.restore()


def festa_fundo(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    luzinhas(c, t, 60, 2, 60)


def check(c, x, y, ok=True, r=40):
    c.new_sub_path(); c.arc(x, y, r, 0, 6.283); rgb(c, VERDE if ok else VERMELHO); c.fill()
    c.set_line_width(r * 0.22); rgb(c, CREME)
    if ok:
        c.move_to(x - r * 0.45, y); c.line_to(x - r * 0.1, y + r * 0.38); c.line_to(x + r * 0.5, y - r * 0.38)
    else:
        c.move_to(x - r * 0.4, y - r * 0.4); c.line_to(x + r * 0.4, y + r * 0.4)
        c.move_to(x + r * 0.4, y - r * 0.4); c.line_to(x - r * 0.4, y + r * 0.4)
    c.stroke()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.3  gancho
    festa_fundo(c, t)
    numero_i(c, "R$ 50 MIL", 520, 300, 170, GOLD)
    numero_i(c, "NA FESTA OU", 520, 440, 84, CREME)
    numero_i(c, "NO APÊ?", 520, 560, 120, CREME)
    entra(c, t, 4.3, 645, 700, selo("DIVIDE ATÉ CASAL", VERMELHO, 46, CREME), anim="stamp")
    entra(c, t, 1.5, 750, 1230, lambda c: bolo(c, 1.05), anim="up")
    consultor_i(c, t, 250, 1300, 1.35, poses=((0, "think"), (4.3, "point_r")), exprs=((0, "think"), (4.3, "confident")), look=0.6)


def s02(c, t):  # 6.3 - 10.8  dois casais, mesmo dinheiro: 50 mil
    cena_rua(c, t, "dia", carros=False)
    numero_i(c, "DOIS CASAIS", 520, 230, 104, CREME)
    numero_i(c, "MESMO DINHEIRO", 520, 340, 72, GOLD) if t > 8.5 else None
    contador(c, t, 9.4, 0, 50000, 520, 480, 130, d=0.9, col=GOLD)
    pessoa(c, t, 250, 1300, 1.35, "carla", poses=((0, "wave"), (9.4, "thumb")), exprs=((0, "happy"), (9.4, "grin")), look=0.4)
    pessoa(c, t, 780, 1300, 1.35, "diego", poses=((0, "wave"), (9.4, "thumb")), exprs=((0, "happy"), (9.4, "grin")), look=-0.4)


def s03(c, t):  # 10.8 - 20.9  Carla: o festão; a conta zera
    festa_fundo(c, t)
    numero_i(c, "A CARLA", 520, 250, 100, GOLD)
    numero_i(c, "FAZ O FESTÃO", 520, 360, 84, CREME) if t > 12.3 else None
    itens = ((13.3, "150 CONVIDADOS"), (15.2, "BUFFET"), (15.9, "BANDA"), (16.7, "VESTIDO"))
    if t < 19.6:
        for i, (tt, s) in enumerate(itens):
            entra(c, t, tt, 660, 490 + i * 115, selo(s, (ROXO, (0.25, 0.45, 0.80), ROSA, GOLD)[i], 50, CREME if i < 3 else NAVY), anim="right")
    else:
        if t < 20.4:
            numero_i(c, "R$ 50.000", 640, 600, 120, CREME)
        else:
            contador(c, t, 20.4, 50000, 0, 640, 600, 120, d=0.5, col=VERMELHO)
        entra(c, t, 20.0, 640, 760, selo("A CONTA ZERA", VERMELHO, 60, CREME), anim="stamp")
    if 17.8 < t < 19.6:
        numero_i(c, "NOITE INESQUECÍVEL", 650, 990, 54, GOLD)
    pessoa(c, t, 230, 1300, 1.35, "carla", poses=((0, "present"), (13.3, "arms_up"), (19.8, "shrug")),
           exprs=((0, "happy"), (13.3, "grin"), (19.8, "worried")), look=0.6, roupa="vestido", cor_roupa=(0.97, 0.96, 0.93))


def s04(c, t):  # 20.9 - 30.1  Diego: civil + almoço, 5 mil; 45 mil viram entrada
    cena_sala(c, t, "dia")
    numero_i(c, "O DIEGO", 520, 230, 100, GOLD)
    entra(c, t, 22.4, 640, 400, cartao("Civil + almoço", "R$ 5 mil", VERMELHO, 600), anim="right")
    if t > 26.6:
        numero_i(c, "SOBRAM", 640, 540, 56, NAVY, contorno=CREME)
    contador(c, t, 27.0, 0, 45000, 640, 660, 110, d=0.9, col=VERDE)
    entra(c, t, 28.5, 640, 830, selo("ENTRADA DO APÊ", NAVY, 56, GOLD), anim="stamp")
    pessoa(c, t, 230, 1300, 1.35, "diego", poses=((0, "stand"), (22.4, "point_r"), (28.5, "thumb")),
           exprs=((0, "neutral"), (22.4, "happy"), (28.5, "confident")), look=0.6)


def s05(c, t):  # 30.1 - 33.6  Diego ganhou de lavada? não é tão simples
    fundo_marca(c, t, "navy", holofote=(520, 1080))
    numero_i(c, "DIEGO GANHOU", 520, 240, 100, CREME)
    numero_i(c, "DE LAVADA?", 520, 360, 110, GOLD)
    entra(c, t, 32.5, 520, 540, selo("NÃO É TÃO SIMPLES", VERMELHO, 62, CREME), anim="stamp")
    consultor_i(c, t, 520, 1300, 1.5, poses=((0, "shrug"), (32.5, "finger_up")), exprs=((0, "think"), (32.5, "confident")), look=0.0)


def s06(c, t):  # 33.6 - 41.7  Carla não jogou dinheiro fora: guardado, sem dívida, memória
    festa_fundo(c, t)
    numero_i(c, "A CARLA NÃO JOGOU", 520, 240, 74, CREME)
    numero_i(c, "DINHEIRO FORA", 520, 345, 92, GOLD)
    for tt, s, y in ((37.0, "Era guardado", 500), (38.0, "Sem dívida", 620)):
        if t > tt:
            k = ease_out(prog(t, tt, 0.35))
            c.save(); c.translate(640, y); c.scale(k, k)
            cartao(s, "", TINTA, 520, 96)(c); check(c, 200, 0, True, 34)
            c.restore()
    entra(c, t, 39.6, 625, 790, selo("MEMÓRIA PRA VIDA TODA", ROSA, 40, CREME), anim="stamp")
    entra(c, t, 39.2, 760, 1230, lambda c: bolo(c, 0.8), anim="up")
    pessoa(c, t, 240, 1300, 1.35, "carla", poses=((0, "stand"), (37.0, "thumb"), (39.6, "present")),
           exprs=((0, "neutral"), (37.0, "confident"), (39.6, "grin")), look=0.6, roupa="vestido", cor_roupa=(0.97, 0.96, 0.93))


def s07(c, t):  # 41.7 - 49.9  o preço é o tempo: 3 anos e meio pra juntar de novo
    fundo_marca(c, t, "vermelho", holofote=(250, 1080))
    numero_i(c, "O PREÇO É", 520, 230, 96, CREME)
    numero_i(c, "O TEMPO", 520, 350, 130, GOLD)
    entra(c, t, 44.1, 620, 520, cartao("Juntar de novo", "R$ 50 mil", NAVY, 600), anim="right")
    entra(c, t, 45.9, 620, 645, cartao("Guardando", "R$ 1 mil/mês", VERDE, 600), anim="right")
    if t > 48.2:
        numero_i(c, "3 ANOS", 640, 830, 130, CREME)
        numero_i(c, "E MEIO", 640, 960, 90, GOLD)
    consultor_i(c, t, 220, 1300, 1.35, poses=((0, "finger_up"), (48.2, "head")), exprs=((0, "think"), (48.2, "shocked")), look=0.7)


def s08(c, t):  # 49.9 - 53.3  enquanto isso, o Diego já está no apê
    cena_sala(c, t, "tarde")
    numero_i(c, "ENQUANTO ISSO...", 520, 240, 84, CREME)
    entra(c, t, 51.0, 560, 420, selo("O DIEGO JÁ ESTÁ NO APÊ", DIEGO_COR, 50, CREME), anim="stamp")
    pessoa(c, t, 640, 1300, 1.35, "diego", poses=((0, "stand"), (51.0, "arms_up")), exprs=((0, "happy"), (51.0, "grin")), look=-0.3)
    consultor_i(c, t, 230, 1300, 1.2, poses=((0, "present"),), exprs=((0, "neutral"),), look=0.6)


def s09(c, t):  # 53.3 - 61.4  festa no empréstimo: 50 mil, 4% ao mês, 3 anos
    cena_agencia(c, t)
    numero_i(c, "O PROBLEMA:", 520, 360, 84, CREME)
    numero_i(c, "FESTA NO EMPRÉSTIMO", 520, 465, 72, GOLD) if t > 55.2 else None
    entra(c, t, 56.0, 640, 640, lambda c: notificacao(c, 0, 0, 1.0, "Empréstimo liberado!", "R$ 50.000 na conta", VERDE, "BANCO"), anim="drop")
    entra(c, t, 58.6, 640, 810, cartao("Juros", "4% ao mês", VERMELHO, 560), anim="right")
    entra(c, t, 60.3, 640, 935, cartao("Prazo", "36 meses", NAVY, 560), anim="right")
    pessoa(c, t, 210, 1300, 1.2, "carla", poses=((0, "hold"), (58.6, "think")), exprs=((0, "happy"), (58.6, "worried")),
           look=0.6, prop=("r", prop_celular_i))


def s10(c, t):  # 61.4 - 65.3  viram ~95 mil pagos: quase o dobro
    fundo_marca(c, t, "vermelho", holofote=(250, 1080))
    numero_i(c, "VOCÊ PAGA", 520, 240, 100, CREME)
    contador(c, t, 61.7, 50000, 95000, 560, 440, 140, d=1.4, col=GOLD)
    entra(c, t, 64.1, 600, 610, selo("QUASE O DOBRO", NAVY, 66, CREME), anim="stamp")
    for i in range(6):
        tt = 62.0 + i * 0.25
        if t < tt:
            continue
        k = ease_out(prog(t, tt, 0.8))
        c.save(); c.translate(700 + (i % 3) * 90, 1200 - k * 330 - (i // 3) * 60); c.rotate(k * 0.5)
        nota_i(c, "100", 150); c.restore()
    consultor_i(c, t, 240, 1300, 1.25, poses=((0, "stand"), (62.4, "head")), exprs=((0, "neutral"), (62.4, "desperate")), look=0.6)


def s11(c, t):  # 65.3 - 72.4  festa com dinheiro guardado é escolha; no empréstimo é dívida com bolo
    fundo_marca(c, t, "creme")
    numero_i(c, "A CONTA É ESSA", 520, 230, 96, NAVY, contorno=CREME)
    if t > 66.8:
        entra(c, t, 66.8, 520, 400, cartao("Festa com dinheiro guardado", "", TINTA, 820, 100), anim="right")
    entra(c, t, 68.6, 520, 510, selo("ESCOLHA", VERDE, 66, CREME), anim="stamp")
    if t > 69.5:
        entra(c, t, 69.5, 520, 640, cartao("Festa no empréstimo", "", TINTA, 820, 100), anim="right")
    entra(c, t, 70.9, 520, 750, selo("DÍVIDA COM BOLO", VERMELHO, 62, CREME), anim="stamp")
    entra(c, t, 71.6, 820, 1240, lambda c: bolo(c, 0.65), anim="up")
    consultor_i(c, t, 230, 1300, 1.0, poses=((0, "present"), (68.6, "thumb"), (70.9, "shrug")),
                exprs=((0, "neutral"), (68.6, "confident"), (70.9, "worried")), look=0.6)


def s12(c, t):  # 72.4 - fim  festão ou apê? time Carla ou time Diego?
    festa_fundo(c, t)
    numero_i(c, "FESTÃO", 520, 250, 110, GOLD)
    numero_i(c, "OU APARTAMENTO?", 520, 370, 76, CREME)
    entra(c, t, 75.0, 270, 540, selo("TIME CARLA", CARLA_COR, 52, CREME), anim="stamp")
    entra(c, t, 75.8, 770, 540, selo("TIME DIEGO", DIEGO_COR, 52, CREME), anim="stamp")
    entra(c, t, 76.7, 520, 670, selo("COMENTA", VERMELHO, 62, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.2, "carla", poses=((0, "stand"), (75.0, "thumb")), exprs=((0, "happy"), (75.0, "grin")), look=0.4,
           roupa="vestido", cor_roupa=(0.97, 0.96, 0.93))
    pessoa(c, t, 780, 1300, 1.2, "diego", poses=((0, "stand"), (75.8, "thumb")), exprs=((0, "happy"), (75.8, "grin")), look=-0.4)
    consultor_i(c, t, 515, 1330, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.0)


SCENES = [(0, 6.3, s01), (6.3, 10.8, s02), (10.8, 20.9, s03), (20.9, 30.1, s04), (30.1, 33.6, s05),
          (33.6, 41.7, s06), (41.7, 49.9, s07), (49.9, 53.3, s08), (53.3, 61.4, s09), (61.4, 65.3, s10),
          (65.3, 72.4, s11), (72.4, 999.0, s12)]
