"""Thumbnails novas (modelo de 10/11/2026) para os vídeos longos já publicados com CTR baixa.
3 conceitos por vídeo: A = dilema (thumb_versus), B = resultado (número enorme), C = pergunta.
Rodar da raiz: python automacao/thumbs_v2.py [slug ...]   -> videos/<slug>/thumb/<slug>_v2_{A,B,C}.png"""
import os
import sys

sys.path.insert(0, os.getcwd())
from engine import *  # noqa
from ilustrado import *  # noqa

ROXO = (0.36, 0.22, 0.52)


def _fit(c, s, size, maxw, font=MARKER):
    c.select_font_face(font); c.set_font_size(size)
    while c.text_extents(s).x_advance > maxw and size > 40:
        size -= 4; c.set_font_size(size)
    return size


def num(s, size=150, col=GOLD, maxw=600):
    """número enorme que cabe na metade da tela dividida (sem encostar no selo do meio)"""
    def f(c):
        sz = _fit(c, s, size, maxw)
        lado = -1 if c.get_matrix()[4] < W / 2 else 1
        numero_i(c, s, -40 if lado < 0 else 40, 0, sz, col)
    return f


def consultor_centro(c, t, expr="shocked", pose="think"):
    thumb_close(c, t, 960, 1820, 2.3, expr, pose, 0.0)


def resultado(c, t, fundo, linhas, cores, objeto=None, expr="shocked", pose="point_r", glow=GOLD, tx=1250, ty=40, size=160):
    fundo_marca(c, t, fundo)
    rglow(c, 1380, 640, 720, glow, 0.30)
    if objeto:
        objeto(c)
    thumb_close(c, t, 400, 1560, 2.4, expr, pose, 0.8)
    # título cabe entre o Consultor e a borda direita (sem cortar)
    c.select_font_face(MARKER)
    while size > 70:
        c.set_font_size(size)
        larg = max(c.text_extents(l).x_advance * (1.0 if i == len(linhas) - 1 else 0.72) for i, l in enumerate(linhas))
        if larg * 1.06 <= 2 * (1860 - tx):
            break
        size -= 5
    thumb_texto(c, linhas, tx, ty, size, cores=cores)


def etiqueta_grande(texto, riscado=None, cor=VERDE, x=1000, y=640, s=2.4, size=60, borda=1840):
    """etiqueta de preço grande com o texto sempre dentro; encosta no máximo em x=borda"""
    def f(c):
        c.select_font_face(MARKER); c.set_font_size(size)
        tw = c.text_extents(texto).x_advance
        rw = 0
        if riscado:
            c.set_font_size(size * 0.5); rw = c.text_extents(riscado).x_advance
        w_ = max(tw, rw) + 120
        h = size * 1.5 + (size * 1.0 if riscado else 0)
        x_ = max(880, min(x, borda - w_ * s))
        sc_ = min(s, (borda - x_) / w_)
        c.save(); c.translate(x_, y); c.scale(sc_, sc_)
        for dx, dy, col_, a in ((6, 8, (0, 0, 0), 0.25), (0, 0, cor, 1)):
            pg(c, [(dx, dy), (36 + dx, -h / 2 + dy), (w_ + dx, -h / 2 + dy), (w_ + dx, h / 2 + dy), (36 + dx, h / 2 + dy)])
            rgb(c, col_, a); c.fill()
        c.new_sub_path(); c.arc(30, 0, 8, 0, 6.283); rgb(c, (1, 1, 1)); c.fill()
        if riscado:
            c.set_font_size(size * 0.5); c.move_to(80, -h / 2 + size * 0.62); rgb(c, (0.25, 0.18, 0.1)); c.show_text(riscado)
            c.rectangle(78, -h / 2 + size * 0.45, rw + 4, 4); rgb(c, TINTA); c.fill()
        c.set_font_size(size); c.move_to(80, h / 2 - size * 0.32); rgb(c, TINTA); c.show_text(texto)
        c.restore()
    return f


def celular(titulo, valor, sub="", x=1430, y=760, s=1.2, cor=NAVY):
    return lambda c: celular_app(c, 0, x, y, s, titulo, valor, sub=sub, cor=cor)


def rosca(pct, texto, cor=VERMELHO, x=1380, y=640, r=230):
    return lambda c: rosca_i(c, 99, 0, x, y, r, pct, cor, fundo=(0.95, 0.92, 0.86), texto=texto)


T = {}

# ------------------------------------------------------------ carro
T["carro-5000-v2"] = {
    "A": lambda c, t: (thumb_versus(c, t, "PARCELA", "DE VERDADE", (0.16, 0.36, 0.56), (0.62, 0.18, 0.16),
                                    num("R$ 1.000"), num("R$ 2.050"), meio="x"), consultor_centro(c, t, "shocked")),
    "B": lambda c, t: resultado(c, t, "vermelho", ["CARRO DE 60 MIL", "41% DO SALÁRIO"], [CREME, GOLD],
                                rosca(0.41, "41%", x=1420, y=650), "desperate", "head"),
    "C": lambda c, t: resultado(c, t, "navy", ["GANHO R$ 5 MIL.", "POSSO?"], [CREME, GOLD],
                                lambda c: (c.save(), c.translate(1420, 860), c.scale(2.0, 2.0), carro_i(c, 0, (0.86, 0.26, 0.22)), c.restore(),
                                           etiqueta_grande("R$ 60 MIL", cor=GOLD, x=1060, y=500, s=1.8)(c)),
                                "think", "think"),
}

# ------------------------------------------------------------ 100 mil
T["primeiros-100-mil"] = {
    "A": lambda c, t: (thumb_versus(c, t, "1º R$ 100 MIL", "3º R$ 100 MIL", (0.62, 0.18, 0.16), (0.16, 0.44, 0.30),
                                    num("6 ANOS"), num("3 ANOS"), meio="x"), consultor_centro(c, t, "shocked")),
    "B": lambda c, t: resultado(c, t, "verde", ["R$ 1.000/MÊS", "R$ 100 MIL?"], [CREME, GOLD],
                                celular("Saldo investido", "R$ 100.000", "em 6 anos e 4 meses"), "grin", "point_r"),
    "C": lambda c, t: resultado(c, t, "navy", ["O MAIS DIFÍCIL", "É O 1º"], [CREME, GOLD],
                                etiqueta_grande("R$ 100 MIL", cor=GOLD, x=1020, y=650, s=2.3), "desperate", "head"),
}

# ------------------------------------------------------------ R$ 10 por dia
T["dez-reais-um-milhao"] = {
    "A": lambda c, t: (thumb_versus(c, t, "VOCÊ PÕE", "OS JUROS", (0.16, 0.36, 0.56), (0.16, 0.44, 0.30),
                                    num("R$ 126 MIL"), num("R$ 904 MIL"), meio="+"), consultor_centro(c, t, "shocked", "arms_up")),
    "B": lambda c, t: resultado(c, t, "verde", ["R$ 10 POR DIA", "= R$ 1 MILHÃO?"], [CREME, GOLD],
                                celular("Saldo investido", "R$ 1 MILHÃO", "em 35 anos"), "shocked", "point_r"),
    "C": lambda c, t: resultado(c, t, "vermelho", ["SEU MILHÃO", "VALE R$ 260 MIL"], [CREME, GOLD],
                                etiqueta_grande("R$ 260 MIL", riscado="R$ 1 MILHÃO", cor=GOLD, x=1000, y=650, s=2.2), "desperate", "head"),
}

# ------------------------------------------------------------ reserva
T["reserva-de-emergencia"] = {
    "A": lambda c, t: (thumb_versus(c, t, "CAMILA", "BRUNO", (0.16, 0.44, 0.30), (0.62, 0.18, 0.16),
                                    num("+R$ 7 MIL", col=CREME), num("-R$ 15 MIL", col=CREME), meio="x"), consultor_centro(c, t, "shocked")),
    "B": lambda c, t: resultado(c, t, "vermelho", ["DEMITIDO HOJE.", "QUANTOS MESES?"], [CREME, GOLD],
                                celular("Saldo da conta", "R$ 0,00", "8 meses sem emprego", cor=VERMELHO), "desperate", "head", size=140),
    "C": lambda c, t: resultado(c, t, "navy", ["8 MESES", "SEM EMPREGO"], [CREME, GOLD],
                                etiqueta_grande("- R$ 15.423", riscado="cheque especial", cor=VERMELHO, x=1000, y=650, s=2.0), "desperate", "head"),
}

# ------------------------------------------------------------ 13º
T["decimo-terceiro"] = {
    "A": lambda c, t: (thumb_versus(c, t, "GASTAR", "INVESTIR", (0.62, 0.18, 0.16), (0.16, 0.44, 0.30),
                                    num("R$ 2.750"), num("R$ 183 MIL")), consultor_centro(c, t, "shocked")),
    "B": lambda c, t: resultado(c, t, "verde", ["SÓ O 13º", "VIRA R$ 183 MIL"], [CREME, GOLD],
                                celular("13º investido todo ano", "R$ 183 MIL", "em 30 anos"), "grin", "point_r"),
    "C": lambda c, t: resultado(c, t, "navy", ["SEU 13º", "NÃO VEM INTEIRO"], [CREME, GOLD],
                                etiqueta_grande("R$ 2.750", riscado="R$ 3.000", cor=GOLD, x=1020, y=650, s=2.3), "shocked", "point_r"),
}

# ------------------------------------------------------------ viver de renda
T["viver-de-renda"] = {
    "A": lambda c, t: (thumb_versus(c, t, "PARECE", "DE VERDADE", (0.16, 0.36, 0.56), (0.62, 0.18, 0.16),
                                    num("R$ 540 MIL"), num("3x MAIS"), meio="x"), consultor_centro(c, t, "shocked")),
    "B": lambda c, t: resultado(c, t, "verde", ["R$ 5 MIL/MÊS", "SEM TRABALHAR"], [CREME, GOLD],
                                celular("Renda por mês", "R$ 5.000", "sem trabalhar"), "grin", "point_r"),
    "C": lambda c, t: resultado(c, t, "navy", ["PAROU 24 ANOS", "ANTES DELE"], [CREME, GOLD],
                                etiqueta_grande("MESMO SALÁRIO", cor=GOLD, x=980, y=650, s=1.9, size=52), "shocked", "point_r", size=145),
}

# ------------------------------------------------------------ CLT ou PJ
T["clt-ou-pj-conta-completa"] = {
    "A": lambda c, t: (thumb_versus(c, t, "CLT", "PJ", (0.16, 0.36, 0.56), (0.36, 0.22, 0.52),
                                    num("R$ 5 MIL"), num("R$ 7 MIL")), consultor_centro(c, t, "think", "think")),
    "B": lambda c, t: resultado(c, t, "vermelho", ["PJ DE R$ 7 MIL", "SÓ R$ 131 A MAIS"], [CREME, GOLD],
                                etiqueta_grande("R$ 131", riscado="R$ 2.000", cor=VERDE, x=1020, y=650, s=2.4), "shocked", "point_r", size=140),
    "C": lambda c, t: resultado(c, t, "navy", ["PJ GANHA", "MAIS MESMO?"], [CREME, GOLD],
                                etiqueta_grande("+ R$ 2.000?", cor=GOLD, x=1020, y=650, s=2.3), "think", "think"),
}

# ------------------------------------------------------------ aumento
T["aumento-de-salario"] = {
    "A": lambda c, t: (thumb_versus(c, t, "AUMENTO", "NO BOLSO", (0.16, 0.44, 0.30), (0.62, 0.18, 0.16),
                                    num("R$ 1.000"), num("R$ 475"), meio="x"), consultor_centro(c, t, "shocked", "head")),
    "B": lambda c, t: resultado(c, t, "navy", ["CADÊ MEU", "AUMENTO?"], [CREME, GOLD],
                                etiqueta_grande("R$ 475", riscado="R$ 1.000", cor=VERDE, x=1000, y=640, s=2.5), "desperate", "head"),
    "C": lambda c, t: resultado(c, t, "vermelho", ["IR 2026: METADE", "DO AUMENTO SOME"], [CREME, GOLD],
                                rosca(0.53, "-53%", cor=GOLD, x=1420, y=650), "shocked", "point_r", size=135),
}


if __name__ == "__main__":
    alvo = sys.argv[1:] or list(T)
    for slug in alvo:
        pasta = os.path.join("videos", slug, "thumb")
        os.makedirs(pasta, exist_ok=True)
        for k, fn in T[slug].items():
            print(salvar_thumb(lambda c, t, fn=fn: fn(c, t), os.path.join(pasta, f"{slug}_v2_{k}.png")))
