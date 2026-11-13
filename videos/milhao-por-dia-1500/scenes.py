"""R$ 1 milhão por dia desde 1500. Só TikTok: vertical nativo 1080x1920, ~72,4 s, estilo ilustrado.
Formato "e se..." (escala de números grandes), inspirado no vídeo de referência do Matheus (13/11/2026).
Narração: Afonso (HeyGen, voz nova escolhida pelo Matheus em 13/11/2026), 1 bloco. Contas em contas.py."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(5.5, "tum"), (16.0, "soft_ding"), (38.6, "tum"), (55.9, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

VOCE = "lucas"


def selo(s, cor=VERMELHO, size=64, tcol=CREME, rot=-0.06):
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


def visor(c, s, x, y, w=820, h=150, rot=None, cor=(1.0, 0.25, 0.22)):
    """display digital vermelho (contagem / balança)"""
    rr(c, x - w / 2 + 8, y - h / 2 + 10, w, h, 18); rgb(c, (0, 0, 0), 0.3); c.fill()
    rr(c, x - w / 2, y - h / 2, w, h, 18); rgb(c, (0.08, 0.08, 0.10)); c.fill()
    if rot:
        text(c, rot, x, y - h / 2 - 26, 30, MARKER, CREME)
    c.select_font_face(MARKER); c.set_font_size(h * 0.62)
    e = c.text_extents(s)
    c.move_to(x + w / 2 - 30 - e.x_advance, y + h * 0.22); rgb(c, cor); c.show_text(s)


def calendario(c, ano, x, y, s=1.0, topo="ANO", size=90):
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -150 + 8, -150 + 10, 300, 300, 22); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, -150, -150, 300, 300, 22); rgb(c, CREME); c.fill()
    rr(c, -150, -150, 300, 90, 22); rgb(c, VERMELHO); c.fill()
    c.rectangle(-150, -90, 300, 30); rgb(c, VERMELHO); c.fill()
    numero_i(c, topo, 0, -105, 40, CREME, contorno=VERMELHO)
    numero_i(c, str(ano), 0, 40, size, NAVY, contorno=CREME)
    c.restore()


def mar_1500(c, t):
    luz("dia")
    ceu(c, t, seed=3, horizonte=900)
    mar_i(c, t, 900)
    c.save(); c.translate(720 + (t % 60) * 3, 1120); nau(c, t, 0.7); c.restore()


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.0  gancho
    luz("dia")
    mar_1500(c, t)
    numero_i(c, "R$ 1 MILHÃO", 520, 240, 130, GOLD)
    numero_i(c, "POR DIA", 520, 370, 100, CREME)
    if t > 3.3:
        pop(c, t, 3.4, 520, 500, "DESDE 1500?", 120, CREME, NAVY)
    entra(c, t, 4.6, 560, 630, selo("DESDE QUE CABRAL CHEGOU", NAVY, 42, GOLD), anim="stamp")
    pessoa(c, t, 200, 1300, 1.3, VOCE, poses=((0, "stand"), (3.4, "arms_up")), exprs=((0, "think"), (3.4, "shocked")), look=0.6)


def s02(c, t):  # 6.0 - 9.8  todo dia, sem faltar, desde 1500
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1000))
    numero_i(c, "TODO DIA", 520, 240, 120, CREME)
    if t > 7.0:
        numero_i(c, "SEM FALTAR NENHUM", 520, 370, 72, GOLD)
    ano = 1500 + int(526 * clamp01((t - 8.1) / 1.6)) if t > 8.1 else 1500
    if t > 8.2:
        for i in range(10):
            k = ((t * 1.8 + i * 0.37) % 1.0)
            x = 540 + math.sin(i * 2.1) * 380 * k
            y = 680 - 300 * k + 900 * k * k
            c.save(); c.translate(x, y); c.rotate(k * 4 + i); c.scale(0.35, 0.35)
            rr(c, -150, -150, 300, 300, 22); rgb(c, CREME, 1 - k); c.fill()
            c.restore()
    calendario(c, ano, 540, 680, 1.1)
    pessoa(c, t, 220, 1300, 1.2, VOCE, poses=((0, "thumb"),), exprs=((0, "grin"),), look=0.6)


def s03(c, t):  # 9.8 - 17.3  192 mil dias -> R$ 192 bilhões
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    numero_i(c, "ATÉ HOJE", 520, 230, 110, CREME)
    if t < 13.3:
        contador(c, t, 11.0, 0, 192000, 540, 450, 140, d=1.6, col=GOLD, prefixo="")
        if t > 12.0:
            numero_i(c, "DIAS", 540, 580, 80, CREME)
    else:
        numero_i(c, "192 MIL DIAS", 540, 380, 80, CREME)
        numero_i(c, "VOCÊ TERIA", 540, 500, 70, CREME) if t > 14.1 else None
        if t > 14.6:
            contador(c, t, 14.6, 0, 192, 650, 650, 130, d=1.2, col=GOLD, sufixo=" BI")
        if t > 15.9:
            numero_i(c, "BILHÕES DE REAIS", 650, 780, 60, CREME)
    pessoa(c, t, 210, 1300, 1.3, VOCE, poses=((0, "stand"), (15.9, "arms_up")), exprs=((0, "think"), (15.9, "grin")), look=0.6)


def s04(c, t):  # 17.3 - 21.2  notas de 200: quase 1 bilhão de notas
    luz("dia")
    fundo_marca(c, t, "creme")
    numero_i(c, "EM NOTAS DE R$ 200", 520, 230, 80, NAVY, contorno=CREME)
    entra(c, t, 17.7, 560, 470, lambda c: maco(c, "200", 7, 380), anim="pop")
    if t > 18.9:
        numero_i(c, "QUASE", 630, 700, 70, NAVY, contorno=CREME)
        pop(c, t, 19.5, 630, 830, "1 BILHÃO", 120, GOLD)
        numero_i(c, "DE NOTAS", 630, 960, 70, NAVY, contorno=CREME) if t > 20.3 else None
    consultor_i(c, t, 150, 1300, 1.0, poses=((0, "present"), (19.5, "point_r")), exprs=((0, "neutral"), (19.5, "shocked")), look=0.6)


def s05(c, t):  # 21.2 - 27.4  empilhadas: 96 km, quase o espaço
    luz("dia")
    # céu que escurece conforme a câmera "sobe"
    k = clamp01((t - 21.6) / 4.5)
    top = mix((0.45, 0.72, 0.95), (0.03, 0.04, 0.10), k)
    bot = mix((0.78, 0.90, 0.98), (0.10, 0.14, 0.30), k)
    lgrad(c, 0, 0, 0, 1920, ((0, top, 1), (1, bot, 1))); c.rectangle(0, 0, 1080, 1920); c.fill()
    if k > 0.4:
        rnd = random.Random(7)
        for i in range(80):
            c.new_sub_path(); c.arc(rnd.uniform(0, 1080), rnd.uniform(0, 1300), rnd.uniform(1, 3), 0, 6.283)
            rgb(c, CREME, (k - 0.4) * 1.6); c.fill()
    # régua
    c.set_line_width(4); rgb(c, CREME, 0.8)
    c.move_to(220, 300); c.line_to(220, 1300); c.stroke()
    km = 96 * k
    for marca, nome in ((10, "AVIÃO 10 KM"), (100, "ESPAÇO 100 KM")):
        y = 1300 - 1000 * marca / 100
        line(c, 200, y, 980, y, 3, CREME)
        text(c, nome, 240, y - 26, 36, MARKER, CREME, align="l")
    # coluna de notas
    h = 1000 * km / 100
    c.rectangle(640, 1300 - h, 160, h); rgb(c, NOTAS["200"]); c.fill()
    for yy in range(int(1300 - h), 1300, 14):
        line(c, 640, yy, 800, yy, 2, dk(NOTAS["200"], 0.25))
    pop(c, t, 21.6, 540, 160, "EMPILHADAS", 96, CREME, NAVY) if t < 23.2 else numero_i(c, "%d KM" % round(km), 720, 160, 130, GOLD)
    if t > 25.5:
        entra(c, t, 25.5, 520, 300, selo("QUASE O ESPAÇO", VERMELHO, 56, CREME), anim="stamp")
    pessoa(c, t, 540, 1300, 0.75, VOCE, poses=((0, "point_r"), (25.5, "head")), exprs=((0, "shocked"),), look=0.6)


def s06(c, t):  # 27.4 - 30.3  quase mil toneladas
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "E IAM PESAR", 520, 230, 100, CREME)
    v = int(960000 * ease_out(prog(t, 27.9, 1.3)))
    visor(c, f"{v:,}".replace(",", ".") + " KG", 540, 450, 860, 160, "BALANÇA")
    if t > 28.8:
        pop(c, t, 28.8, 540, 640, "QUASE 1.000 TONELADAS", 70, GOLD)
    entra(c, t, 27.6, 680, 1000, lambda c: maco(c, "200", 8, 300), anim="drop")
    pessoa(c, t, 220, 1300, 1.25, VOCE, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.6)


def s07(c, t):  # 30.3 - 36.8  contando 1 nota por segundo: + de 30 anos
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(260, 1100))
    numero_i(c, "1 NOTA POR SEGUNDO", 520, 230, 80, CREME)
    numero_i(c, "SEM DORMIR", 520, 340, 84, GOLD) if t > 33.0 else None
    anos = 30 * ease_out(prog(t, 34.2, 1.4))
    visor(c, "%d ANOS" % int(anos), 630, 520, 560, 140, "CONTANDO")
    if t > 35.0:
        pop(c, t, 35.0, 660, 700, "+ DE 30 ANOS", 84, GOLD)
    k = (t * 3) % 1
    c.save(); c.translate(700 + 120 * k, 1060 - 90 * math.sin(k * math.pi)); c.rotate(k * 2); nota_i(c, "200", 150); c.restore()
    pessoa(c, t, 220, 1300, 1.2, VOCE, poses=((0, "hold"), (35.0, "head")), exprs=((0, "think"), (35.0, "desperate")), look=0.6)


def s08(c, t):  # 36.8 - 39.4  parece muito? olha a virada
    luz("dia")
    fundo_marca(c, t, "vermelho", holofote=(520, 1100))
    numero_i(c, "PARECE MUITO?", 520, 260, 110, CREME)
    if t > 38.3:
        pop(c, t, 38.3, 520, 440, "OLHA A VIRADA", 100, GOLD)
    consultor_i(c, t, 520, 1300, 1.3, poses=((0, "shrug"), (38.3, "finger_up")), exprs=((0, "think"), (38.3, "confident")), look=0.0)


def s09(c, t):  # 39.4 - 48.8  o mais rico do mundo tem + de 20x isso
    luz("dia")
    fundo_marca(c, t, "creme")
    numero_i(c, "O MAIS RICO DO MUNDO", 520, 220, 76, NAVY, contorno=CREME)
    numero_i(c, "TEM MAIS DE 20X ISSO", 520, 320, 70, VERMELHO, contorno=CREME) if t > 41.4 else None
    barras_i(c, t, 40.6, 140, 1180, 800, 720, dados=(("Você", 192, VERDE), ("O mais rico", 4600, NAVY)),
             fmt=lambda v: ("R$ %d BI" % v) if v < 1000 else ("R$ %.1f TRI" % (v / 1000)).replace(".", ","), d=1.6, size_val=50)
    if t > 47.2:
        entra(c, t, 47.2, 330, 960, selo("NEM PERTO", VERMELHO, 52, CREME), anim="stamp")


def s10(c, t):  # 48.8 - 59.6  rendendo ~1% ao mês: + de 50 milhões por dia
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    numero_i(c, "UM DETALHE", 520, 220, 110, CREME)
    if t < 54.4:
        entra(c, t, 51.4, 600, 470, lambda c: calendario(c, "1%", 0, 0, 1.0, topo="RENDE", size=110), anim="pop")
        numero_i(c, "AO MÊS", 600, 680, 70, CREME) if t > 53.9 else None
    else:
        numero_i(c, "RENDERIA", 600, 380, 70, CREME)
        contador(c, t, 55.5, 0, 50, 630, 520, 110, d=1.0, col=GOLD, prefixo="+ R$ ", sufixo=" MI")
        numero_i(c, "POR DIA", 630, 640, 70, CREME) if t > 57.0 else None
        entra(c, t, 58.2, 630, 780, selo("JÁ SEM O IMPOSTO", NAVY, 46, GOLD), anim="stamp")
    pessoa(c, t, 200, 1300, 1.25, VOCE, poses=((0, "stand"), (56.7, "arms_up")), exprs=((0, "think"), (56.7, "grin")), look=0.6)


def s11(c, t):  # 59.6 - 66.6  50x o que você ganhava; o dinheiro trabalha mais que você
    luz("dia")
    fundo_marca(c, t, "verde", holofote=(540, 1100))
    numero_i(c, "50X MAIS", 520, 230, 130, GOLD)
    numero_i(c, "DO QUE VOCÊ GANHAVA", 520, 360, 64, CREME)
    if t > 60.8:
        k = ease_out(prog(t, 60.8, 0.6))
        c.save(); c.translate(340, 680)
        line(c, 0, 60, 0, 60 - 150 * k, 34, GOLD); c.move_to(-60, 50 - 150 * k); c.line_to(0, -30 - 150 * k); c.line_to(60, 50 - 150 * k); c.close_path(); rgb(c, GOLD); c.fill()
        numero_i(c, "RENDE", 0, 130, 52, CREME); numero_i(c, "R$ 50 MI/DIA", 0, 200, 46, GOLD)
        c.restore()
        c.save(); c.translate(760, 680)
        line(c, 0, 60, 0, 60 - 20 * k, 34, CREME)
        numero_i(c, "VOCÊ", 0, 130, 52, CREME); numero_i(c, "R$ 1 MI/DIA", 0, 200, 46, CREME)
        c.restore()
    if t > 63.3:
        entra(c, t, 63.3, 540, 985, selo("O DINHEIRO TRABALHA MAIS", NAVY, 44, GOLD), anim="stamp")
    pessoa(c, t, 560, 1430, 0.8, VOCE, poses=((0, "thumb"), (63.3, "hips")), exprs=((0, "grin"), (63.3, "confident")), look=0.0)


def s12(c, t):  # 66.6 - fim  o que você fazia primeiro?
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1100))
    numero_i(c, "COM R$ 192 BILHÕES", 520, 230, 80, CREME)
    pop(c, t, 69.8, 520, 380, "O QUE VOCÊ", 110, GOLD) if t > 69.8 else None
    numero_i(c, "FAZIA PRIMEIRO?", 520, 500, 96, GOLD) if t > 70.3 else None
    entra(c, t, 71.5, 620, 650, selo("COMENTA", VERMELHO, 66, CREME), anim="stamp")
    # balão de pensamento
    if t > 67.2:
        for i, (dx, dy, r) in enumerate(((470, 900, 18), (530, 860, 28))):
            c.new_sub_path(); c.arc(dx, dy, r, 0, 6.283); rgb(c, CREME); c.fill()
        c.new_sub_path(); c.arc(700, 900, 130, 0, 6.283); rgb(c, CREME); c.fill()
        c.save(); c.translate(700, 890); maco(c, "200", 4, 160); c.restore()
    pessoa(c, t, 280, 1300, 1.3, VOCE, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.5)


SCENES = [(0, 6.0, s01), (6.0, 9.8, s02), (9.8, 17.3, s03), (17.3, 21.2, s04), (21.2, 27.4, s05),
          (27.4, 30.3, s06), (30.3, 36.8, s07), (36.8, 39.4, s08), (39.4, 48.8, s09), (48.8, 59.6, s10),
          (59.6, 66.6, s11), (66.6, 999.0, s12)]
