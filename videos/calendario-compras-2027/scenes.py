"""VOCÊ COMPRA NO MÊS ERRADO: o calendário de 2027 pra pagar menos (TikTok vertical, ~77,5 s, estilo ilustrado).
2º item [18h] da Fila do Matheus (referência: dinheiro.falante "Você compra no dia errado"). Pesquisa de 18/11/2026:
- Celular: comparador Zoom (InfoMoney, 03/2019): modelo anterior perde até 20% do preço médio após o sucessor
  (Galaxy S7 -20% em ~4 meses depois do S8; iPhone 7 -10% depois do iPhone 8). Galaxy S sai no começo do ano; iPhone em setembro.
  Celular de R$ 4.000 x 20% = R$ 800.
- TV: Canaltech: melhor época jan-mar (procura menor, liquidação de estoque) e quando chega a linha nova o modelo anterior cai.
- Passagem: ~39 dias de antecedência pro voo nacional (levantamentos citados pelo O Hoje, 07/2026) -> "uns quarenta dias".
- Carro 0 km: PVZ MegaDealer/Auto Avaliar (out/2026): desconto médio recorde de 8,8%, R$ 15.372 por carro; virada do ano-modelo.
- FICOU DE FORA (sem fonte firme): apê no fim do ano da construtora (estava na ideia da fila).
Soma: 800 + 15.000 = R$ 15.800 ("quase dezesseis mil")."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (10.6, "tum"), (33.0, "tum"), (42.0, "tum"), (52.4, "tum"), (68.6, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

MESES = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
ROXO = (0.55, 0.32, 0.62)
LARANJA = (0.88, 0.45, 0.16)
# (t0, mês, rótulo, cor)
TAGS = [(24.9, 1, "GALAXY", NAVY), (27.9, 8, "iPHONE", NAVY),
        (34.7, 0, "TV", VERDE), (34.85, 1, "TV", VERDE), (35.2, 2, "TV", VERDE),
        (50.2, 6, "VIAJA", ROXO), (50.8, 5, "PASSAGEM", ROXO),
        (53.7, 10, "CARRO", LARANJA), (53.9, 11, "CARRO", LARANJA)]
L1, L2, R1, R2 = (275, 1010), (275, 1115), (775, 1010), (775, 1115)
C1, C2, CM = (540, 1010), (540, 1115), (540, 1060)


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


def calendario(c, t):
    rr(c, 70 + 8, 290 + 10, 850, 480, 30); rgb(c, (0, 0, 0), 0.25); c.fill()
    rr(c, 70, 290, 850, 480, 30); rgb(c, CREME); c.fill()
    # argolas do calendário
    for x in (250, 495, 740):
        rr(c, x - 10, 272, 20, 44, 8); rgb(c, NAVY); c.fill()
    cw, ch = 205, 152
    ativos = {}
    for (t0, m, nome, cor) in TAGS:
        if t >= t0:
            ativos.setdefault(m, []).append((t0, nome, cor))
    for i, m in enumerate(MESES):
        col, lin = i % 4, i // 4
        x0, y0 = 85 + col * cw, 305 + lin * ch
        tem = i in ativos
        rr(c, x0 + 4, y0 + 4, cw - 8, ch - 8, 16)
        rgb(c, (0.99, 0.93, 0.72) if tem else (0.94, 0.91, 0.84)); c.fill()
        text(c, m, x0 + cw / 2, y0 + 38, 34, MARKER, NAVY if tem else (0.55, 0.55, 0.58))
        for j, (t0, nome, cor) in enumerate(ativos.get(i, [])[:2]):
            k = ease_out(clamp01((t - t0) / 0.35))
            yy = y0 + 56 + j * 42
            c.save(); c.translate(x0 + cw / 2, yy + 14); c.scale(k, k)
            rr(c, -92, -19, 184, 38, 10); rgb(c, cor); c.fill()
            text(c, nome, 0, 4, 28, MARKER, CREME)
            c.restore()


def marcador(c, t):
    if t >= 68.6:
        k = 1 + 0.12 * math.sin(clamp01((t - 68.6) / 0.35) * math.pi)
        c.save(); c.translate(540, 850); c.scale(k, k)
        rr(c, -390, -70, 780, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "QUASE R$ 16 MIL", 0, 30, 78, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, 790, 780, 120, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    if t < 10.6:
        text(c, "O MESMO CELULAR", 360, 866, 40, MARKER, CREME)
        if t < 0.3:
            numero_i(c, "R$ 4.000", 740, 878, 76, VERMELHO)
        else:
            contador(c, t, 0.3, 4000, 3200, 740, 850, 76, d=3.0, col=VERDE)
        return
    text(c, "ECONOMIA", 300, 866, 48, MARKER, CREME)
    if t < 31.3:
        numero_i(c, "R$ 0", 680, 878, 84, CREME)
    elif t < 65.0:
        contador(c, t, 31.3, 0, 800, 680, 850, 84, d=0.6, col=VERDE)
        if t < 34.5:
            entra(c, t, 31.3, 830, 785, chip("+ R$ 800", VERDE, CREME, 40, 0.04), anim="stamp")
    else:
        contador(c, t, 65.0, 800, 15800, 680, 850, 84, d=0.8, col=VERDE)


def detalhes(c, t):
    if 1.6 <= t < 10.6:
        entra(c, t, 1.7, *C1, chip("MÊS ERRADO?", VERMELHO, CREME, 56, -0.03), anim="stamp")
    if 2.5 <= t < 8.2:
        entra(c, t, 3.0, 250, 1110, chip("celular", CREME, TINTA, 42, 0.03), anim="left")
        entra(c, t, 4.1, 540, 1120, chip("TV", CREME, TINTA, 42, -0.03), anim="pop")
        entra(c, t, 5.2, 800, 1110, chip("carro", CREME, TINTA, 42, 0.03), anim="right")
    if 8.2 <= t < 10.6:
        entra(c, t, 8.3, *C2, chip("SALVA O CALENDÁRIO", GOLD, TINTA, 48), anim="pop")
    # celular
    if 10.6 <= t < 14.5:
        entra(c, t, 11.8, *C1, chip("saiu o modelo novo", CREME, TINTA, 46), anim="pop")
        entra(c, t, 13.0, *C2, chip("o anterior CAI", VERDE, CREME, 50), anim="stamp")
    if 14.5 <= t < 23.8:
        entra(c, t, 15.4, *L1, chip("comparador Zoom", CREME, TINTA, 40, -0.04), anim="left")
        entra(c, t, 17.4, *R1, chip("Galaxy: -20%", VERDE, CREME, 44, 0.04), anim="right")
        entra(c, t, 19.0, *L2, chip("em ~4 meses", CREME, TINTA, 42, 0.03), anim="left")
        entra(c, t, 22.5, *R2, chip("iPhone: -10%", VERDE, CREME, 44, -0.03), anim="stamp")
    if 23.8 <= t < 28.7:
        entra(c, t, 24.4, *C1, chip("Galaxy: começo do ano", CREME, NAVY, 44, -0.02), anim="left")
        entra(c, t, 27.3, *C2, chip("iPhone: setembro", CREME, NAVY, 44, 0.02), anim="right")
    if 28.7 <= t < 33.0:
        entra(c, t, 29.0, *C1, chip("celular de R$ 4.000", CREME, TINTA, 46), anim="pop")
        entra(c, t, 31.1, *C2, chip("até R$ 800 a menos", VERDE, CREME, 48), anim="stamp")
    # TV
    if 33.0 <= t < 42.0:
        entra(c, t, 34.6, *L1, chip("JAN a MAR", GOLD, TINTA, 46, -0.04), anim="left")
        entra(c, t, 35.8, *R1, chip("pouca procura", CREME, TINTA, 42, 0.04), anim="right")
        entra(c, t, 37.2, *L2, chip("liquida o estoque", CREME, TINTA, 38, 0.03), anim="left")
        entra(c, t, 39.6, *R2, chip("linha nova chegou", CREME, TINTA, 38, -0.03), anim="right")
    if 40.8 <= t < 42.0:
        entra(c, t, 40.8, 540, 1215, chip("A ANTIGA BAIXA", VERDE, CREME, 48), anim="stamp")
    # passagem
    if 42.0 <= t < 49.2:
        entra(c, t, 43.4, *C1, chip("não é o mês: ANTECEDÊNCIA", CREME, TINTA, 42), anim="pop")
        entra(c, t, 46.6, *C2, chip("voo nacional: ~40 dias antes", GOLD, TINTA, 40), anim="stamp")
    if 49.2 <= t < 52.4:
        entra(c, t, 49.4, *C1, chip("viaja: meio de julho", CREME, ROXO, 44, -0.02), anim="left")
        entra(c, t, 50.8, *C2, chip("compra: começo de junho", ROXO, CREME, 44, 0.02), anim="right")
    # carro
    if 52.4 <= t < 58.8:
        entra(c, t, 53.5, *L1, chip("fim do ano", CREME, TINTA, 46, -0.04), anim="left")
        entra(c, t, 55.6, *R1, chip("vender o estoque", CREME, TINTA, 40, 0.04), anim="right")
        entra(c, t, 57.2, *C2, chip("virada do ano-modelo", GOLD, TINTA, 44), anim="pop")
    if 58.8 <= t < 66.9:
        entra(c, t, 60.6, *L1, chip("outubro/2026", CREME, TINTA, 42, -0.04), anim="left")
        entra(c, t, 62.1, *R1, chip("RECORDE", VERMELHO, CREME, 46, 0.04), anim="stamp")
        entra(c, t, 63.3, *L2, chip("desconto 8,8%", VERDE, CREME, 44, 0.03), anim="left")
        entra(c, t, 65.0, *R2, chip("~R$ 15 mil/carro", VERDE, CREME, 40, -0.03), anim="right")
    # soma
    if 66.9 <= t < 72.4:
        entra(c, t, 67.4, *C1, chip("celular + carro", CREME, TINTA, 48), anim="pop")
        entra(c, t, 70.9, *C2, chip("só por escolher a data", GOLD, TINTA, 44), anim="pop")
    if t >= 72.4:
        entra(c, t, 72.5, *C1, chip("O PREÇO CAIU", GOLD, TINTA, 50), anim="pop")
        entra(c, t, 74.6, *C2, chip("NO MÊS SEGUINTE?", GOLD, TINTA, 50), anim="pop")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "CALENDÁRIO DE COMPRAS 2027", 540, 235, 52, CREME)
    calendario(c, t)
    marcador(c, t)
    poses = ((0, "present"), (1.6, "shrug"), (5.5, "present"), (8.3, "finger_up"), (10.6, "finger_up"), (14.5, "point_r"),
             (17.4, "finger_up"), (23.8, "present"), (28.7, "present"), (31.1, "finger_up"), (33.0, "finger_up"), (35.8, "point_r"),
             (42.0, "finger_up"), (46.4, "present"), (49.2, "point_r"), (52.4, "finger_up"), (55.6, "present"), (62.1, "shrug"),
             (65.0, "finger_up"), (66.9, "present"), (72.4, "present"))
    exprs = ((0, "confident"), (1.6, "shocked"), (5.5, "confident"), (17.4, "grin"), (23.8, "confident"), (31.1, "grin"),
             (33.0, "confident"), (62.1, "shocked"), (65.0, "grin"), (68.6, "shocked"), (72.4, "grin"))
    consultor_i(c, t, 540, 2250, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
