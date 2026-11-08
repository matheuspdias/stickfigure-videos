"""Assinaturas esquecidas: quanto somam em um ano. Só TikTok: vertical nativo 1080x1920, 61,6 s, estilo ilustrado.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: 45 + 30 + 25 + 10 + 20 = R$ 130/mês = R$ 1.560/ano; cortando 30 + 20 = R$ 50/mês = R$ 600/ano."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(22.2, "tum"), (29.1, "tum"), (47.5, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ITENS = [  # (rótulo, valor, cor do ícone, tempo em que a narração cita)
    ("Streaming 1", "R$ 45", (0.80, 0.20, 0.22), 6.6),
    ("Streaming 2", "R$ 30", (0.30, 0.42, 0.80), 8.8),
    ("Música", "R$ 25", (0.20, 0.62, 0.40), 12.5),
    ("Nuvem", "R$ 10", (0.40, 0.66, 0.90), 16.0),
    ("App grátis*", "R$ 20", (0.86, 0.56, 0.20), 21.0),
]


# ---------------------------------------------------------------- helpers
def linha_assin(lab, val, cor, w=560, riscado=0.0, apagado=False):
    """cartão de uma assinatura (ícone redondo, nome, valor por mês). riscado 0..1 desenha o risco vermelho"""
    def f(c):
        h = 104
        rr(c, -w / 2 + 6, -h / 2 + 8, w, h, 22); rgb(c, (0, 0, 0), 0.20); c.fill()
        rr(c, -w / 2, -h / 2, w, h, 22); rgb(c, (0.93, 0.93, 0.91) if apagado else (0.99, 0.99, 0.98)); c.fill()
        c.new_sub_path(); c.arc(-w / 2 + 58, 0, 32, 0, 6.283); rgb(c, cor); c.fill()
        c.move_to(-w / 2 + 50, -14); c.line_to(-w / 2 + 50, 14); c.line_to(-w / 2 + 72, 0); c.close_path()
        rgb(c, (1, 1, 1)); c.fill()
        text(c, lab, -w / 2 + 108, 2, 44, HAND, (0.2, 0.2, 0.25), align="l")
        text(c, val, w / 2 - 26, 2, 46, MARKER, TINTA, align="r")
        text(c, "/mês", w / 2 - 26, 38, 22, HAND, (0.45, 0.45, 0.5), align="r")
        if riscado > 0:
            x1 = -w / 2 + 20 + (w - 40) * riscado
            line(c, -w / 2 + 20, 4, x1, -4, 12, VERMELHO)
    return f


def selo(s, cor=VERMELHO, size=64, tcol=CREME):
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        w = c.text_extents(s).x_advance + 70
        c.save(); c.rotate(-0.06)
        rr(c, -w / 2, -size * 0.8, w, size * 1.6, 18); rgb(c, cor); c.fill()
        numero_i(c, s, 0, 0, size, tcol)
        c.restore()
    return f


def risco(c, t, t0, x0, y0, x1, y1, d=0.35, lw=14, col=VERMELHO):
    if t < t0:
        return
    k = ease_out(prog(t, t0, d))
    line(c, x0, y0, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, lw, col)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 3.6  gancho: pergunta enorme já no 1º quadro
    cena_sala(c, t, "tarde")
    numero_i(c, "QUANTO VOCÊ PAGA", 520, 250, 92, CREME)
    numero_i(c, "EM ASSINATURAS?", 520, 370, 100, GOLD)
    c.save(); c.translate(700, 1060); tv_i(c, 380, True, t); c.restore()
    for i, (lab, val, cor, _) in enumerate(ITENS[:3]):
        entra(c, t, 0.4 + i * 0.35, 690, 560 + i * 120, linha_assin(lab, "?", cor, 400), anim="right")
    consultor_i(c, t, 260, 1300, 1.4, poses=((0, "think"), (2.6, "point_r")), exprs=((0, "think"), (2.6, "happy")), look=0.6)
    entra(c, t, 2.7, 700, 940, selo("CHUTA UM NÚMERO", NAVY, 52, GOLD), anim="stamp")


def s02(c, t):  # 3.6 - 11.6  streaming 1 e 2 (a série mudou de app)
    cena_sala(c, t, "tarde")
    numero_i(c, "VAMOS FAZER A CONTA", 520, 250, 76, GOLD)
    c.save(); c.translate(660, 1150); sofa_i(c, 520); c.restore()
    c.save(); c.translate(560, 820); tv_i(c, 520, True, t); c.restore()
    entra(c, t, 6.6, 300, 470, lambda c: etiqueta_preco(c, "R$ 45", GOLD, 64), anim="drop")
    entra(c, t, 8.8, 610, 470, lambda c: etiqueta_preco(c, "R$ 30", GOLD, 64), anim="drop")
    entra(c, t, 9.7, 560, 620, selo("A SÉRIE MUDOU DE APP", NAVY, 40, CREME), anim="pop")
    consultor_i(c, t, 210, 1300, 1.35, poses=((0, "present"), (8.8, "shrug")), exprs=((0, "neutral"), (8.8, "worried")), look=0.7)


def s03(c, t):  # 11.6 - 21.8  a lista completa
    fundo_marca(c, t, "creme")
    numero_i(c, "TODO MÊS NO CARTÃO", 520, 250, 76, NAVY, contorno=CREME)
    for i, (lab, val, cor, t0) in enumerate(ITENS):
        tt = min(t0, 11.8) if i < 2 else t0
        entra(c, t, tt, 640, 420 + i * 125, linha_assin(lab, val, cor, 540), anim="right")
    entra(c, t, 19.2, 640, 1050, lambda c: text(c, "*7 dias grátis... e esqueceu", 0, 0, 40, HAND, VERMELHO), anim="up")
    consultor_i(c, t, 200, 1300, 1.25, poses=((0, "point_r"), (16.6, "finger_up"), (19.4, "head")),
                exprs=((0, "neutral"), (16.6, "think"), (19.4, "shocked")), look=0.8)


def s04(c, t):  # 21.8 - 27.9  R$ 130 por mês, cai picadinho
    fundo_marca(c, t, "navy", holofote=(270, 950))
    numero_i(c, "DÁ", 520, 250, 80, CREME)
    contador(c, t, 22.0, 0, 130, 520, 400, 190, d=1.2, col=GOLD)
    numero_i(c, "POR MÊS", 520, 540, 80, CREME) if t > 23.3 else None
    entra(c, t, 24.1, 720, 720, selo("PARECE POUCO", (0.30, 0.42, 0.62), 48, CREME), anim="pop")
    # moedinhas caindo "picadinho"
    if t > 25.4:
        for i in range(6):
            tt = 25.4 + i * 0.25
            if t < tt:
                continue
            k = ease_out(prog(t, tt, 0.4))
            c.save(); c.translate(600 + (i % 3) * 110, 860 + (i // 3) * 110 - (1 - k) * 160); moeda_i(c, 34); c.restore()
    entra(c, t, 26.4, 720, 1120, lambda c: text(c, "no cartão, sem ver", 0, 0, 46, HAND, CREME), anim="up")
    consultor_i(c, t, 270, 1300, 1.4, poses=((0, "present_l"), (24.0, "shrug")), exprs=((0, "neutral"), (24.0, "worried")), look=0.6)


def s05(c, t):  # 27.9 - 31.3  no ano: R$ 1.560
    fundo_marca(c, t, "vermelho", holofote=(520, 1000))
    numero_i(c, "MAS NO ANO...", 520, 260, 96, CREME)
    contador(c, t, 28.9, 130, 1560, 520, 470, 170, d=1.4, col=GOLD)
    if t > 30.4:
        c.save(); c.translate(860, 1240); pilha_moedas(c, 9, 46, t, 30.4, 0.06); c.restore()
    consultor_i(c, t, 520, 1300, 1.45, poses=((0, "stand"), (29.4, "head")), exprs=((0, "worried"), (29.4, "shocked")), look=0.0)


def s06(c, t):  # 31.3 - 37.3  o preço sobe sem pedir licença
    cena_sala(c, t, "tarde")
    numero_i(c, "TEM UM DETALHE", 520, 250, 92, GOLD)
    entra(c, t, 32.7, 560, 520, lambda c: notificacao(c, 0, 0, 1.25, "Seu plano mudou", "novo valor na próxima fatura", VERMELHO, "STREAMING"), anim="drop")
    entra(c, t, 33.3, 620, 760, lambda c: etiqueta_preco(c, "R$ 55", VERMELHO, 70, riscado="R$ 45"), anim="drop")
    entra(c, t, 35.4, 560, 1000, selo("NO AUTOMÁTICO", VERMELHO, 56, CREME), anim="stamp")
    consultor_i(c, t, 230, 1300, 1.35, poses=((0, "finger_up"), (33.7, "hips")), exprs=((0, "think"), (33.7, "angry")), look=0.7)


def s07(c, t):  # 37.3 - 45.3  a parte boa: corta só duas
    fundo_marca(c, t, "verde")
    numero_i(c, "A PARTE BOA", 520, 250, 104, GOLD)
    entra(c, t, 38.9, 600, 360, lambda c: text(c, "não precisa cancelar tudo", 0, 0, 42, HAND, CREME), anim="up")
    marc = {1: 43.0, 4: 44.2}
    for i, (lab, val, cor, _) in enumerate(ITENS):
        tr = marc.get(i)
        k = ease_out(prog(t, tr, 0.35)) if tr and t > tr else 0
        show(c, t, 37.4 + i * 0.12, 600, 480 + i * 125, linha_assin(lab, val, cor, 520, riscado=k, apagado=k > 0.99), anim="fade")
    for i in (0, 2, 3):
        if t > 40.4:
            c.save(); c.translate(895, 480 + i * 125); check_icon(c, 24); c.restore()
    consultor_i(c, t, 170, 1300, 1.15, poses=((0, "present"), (41.0, "point_r")), exprs=((0, "happy"), (41.0, "confident")), look=0.8)


def s08(c, t):  # 45.3 - 50.4  R$ 50 por mês = R$ 600 por ano
    fundo_marca(c, t, "verde", holofote=(250, 1000))
    contador(c, t, 45.5, 0, 50, 520, 280, 130, d=0.8, col=CREME, sufixo="/MÊS")
    numero_i(c, "VIRA", 520, 390, 70, CREME) if t > 47.3 else None
    contador(c, t, 47.4, 0, 600, 520, 510, 180, d=1.2, col=GOLD)
    numero_i(c, "POR ANO", 520, 640, 80, CREME) if t > 48.6 else None
    for i, n in enumerate((7, 11)):
        c.save(); c.translate(660 + i * 170, 1250); pilha_moedas(c, n, 56, t, 47.6 + i * 0.4, 0.07); c.restore()
    chuva_dinheiro(c, t, 49.3, 10, area=(560, 900), area_y=900)
    consultor_i(c, t, 250, 1300, 1.25, poses=((0, "stand"), (49.3, "arms_up")), exprs=((0, "happy"), (49.3, "grin")), look=0.5)


def s09(c, t):  # 50.4 - 58.3  faz assim: abre a fatura
    cena_cozinha(c, t, "dia")
    numero_i(c, "FAZ ASSIM", 520, 250, 104, GOLD)
    itens = tuple((lab.replace("*", ""), val) for lab, val, _, _ in ITENS)
    FS, FY_ = 1.1, 780
    entra(c, t, 51.5, 600, FY_, lambda c: fatura(c, t, 0, 0, FS, itens, "R$ 130", "Todo mês", t0=51.7), anim="drop")
    row = lambda i: FY_ + FS * (-110 + 60 * i) - 12
    for i in range(5):  # marca os nomes que aparecem todo mês
        if t > 54.4 + i * 0.2:
            c.save(); c.translate(600 - FS * 252, row(i)); circle(c, 0, 0, 12, GOLD, 4); c.restore()
    risco(c, t, 57.0, 370, row(1) + 4, 850, row(1), d=0.3)
    risco(c, t, 57.3, 370, row(4) + 4, 850, row(4), d=0.3)
    entra(c, t, 57.8, 620, 1130, selo("CANCELA", VERMELHO, 70, CREME), anim="stamp")
    consultor_i(c, t, 190, 1300, 1.3, poses=((0, "point_r"), (55.2, "finger_up")), exprs=((0, "neutral"), (55.2, "confident")), look=0.8)


def s10(c, t):  # 58.3 - fim  pergunta para comentário
    cena_sala(c, t, "tarde")
    numero_i(c, "QUANTAS VOCÊ", 520, 250, 100, CREME)
    numero_i(c, "ENCONTROU AÍ?", 520, 380, 100, GOLD)
    entra(c, t, 61.0, 520, 560, selo("COMENTA", NAVY, 70, GOLD), anim="stamp")
    consultor_i(c, t, 300, 1300, 1.4, poses=((0, "present"),), exprs=((0, "happy"),), look=0.6)
    pessoa(c, t, 740, 1300, 1.3, "ana", poses=((0, "think_l"), (59.6, "point_ru")), exprs=((0, "think"), (59.6, "happy")), look=-0.5, prop=("r", prop_celular_i))


SCENES = [(0, 3.6, s01), (3.6, 11.6, s02), (11.6, 21.8, s03), (21.8, 27.9, s04), (27.9, 31.3, s05),
          (31.3, 37.3, s06), (37.3, 45.3, s07), (45.3, 50.4, s08), (50.4, 58.3, s09), (58.3, 999.0, s10)]
