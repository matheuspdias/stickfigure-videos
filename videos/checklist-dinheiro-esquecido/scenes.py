"""CHECKLIST DO CONSULTOR · "3 lugares onde pode ter dinheiro seu esquecido" (TikTok vertical, ~87,7 s). Modelo: checklist-golpe-black-friday.
Fontes (pesquisa de 18/11/2026):
1) Valores a Receber (BC, 10/11/2026): R$ 6,03 bi; 24,6 mi de pessoas físicas; 69,5% até R$ 10; 9,4% de R$ 100 a R$ 1 mil + 2,25% acima de R$ 1 mil
   (= ~1 em cada 10 com mais de R$ 100). Consulta grátis em valoresareceber.bcb.gov.br com CPF + data de nascimento.
2) Abono PIS/Pasep 2026 (ano-base 2024): até R$ 1.621 (R$ 135,08 por mês trabalhado), média até R$ 2.765,93/mês; 276.831 não sacaram
   (R$ 304,8 mi, Agência Gov 11/2026); prazo 28/12/2026. App Carteira de Trabalho Digital.
3) FGTS: 8% ao mês; 1 ano de R$ 2.000 = 12 x 160 = R$ 1.920 (+13º e férias ~R$ 2.130) -> "uns R$ 2 mil".
   Saque de conta antiga: demissão sem justa causa ou 3 anos seguidos fora do regime do FGTS. App FGTS.
Exemplo final: 150 + 1.080 (8 meses x 135,08) + 2.000 = R$ 3.230 ("mais de três mil")."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(0.3, "soft_ding"), (7.6, "tum"), (28.6, "tum"), (50.6, "tum"), (83.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

PASSOS = [(7.6, "VALORES A RECEBER (BC)", 28.4), (28.6, "ABONO DO PIS", 50.4), (50.6, "FGTS DE EMPREGO ANTIGO", 69.6)]
L1, L2, R1, R2 = (275, 990), (275, 1100), (775, 990), (775, 1100)
C1, C2, CM = (540, 990), (540, 1100), (540, 1040)


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
            text(c, nome, 210, y + 17, 44, MARKER, TINTA, align="l")
            c.restore()


def marcador(c, t):
    if t >= 83.2:
        k = 1 + 0.12 * math.sin(clamp01((t - 83.2) / 0.35) * math.pi)
        c.save(); c.translate(540, 790); c.scale(k, k)
        rr(c, -380, -70, 760, 140, 30); rgb(c, GOLD); c.fill()
        text(c, "R$ 3.230 PARADOS", 0, 30, 76, MARKER, TINTA)
        c.restore()
        return
    rr(c, 150, 725, 780, 130, 30); rgb(c, (0.10, 0.14, 0.26)); c.fill()
    if t < 7.6:
        text(c, "ESQUECIDO", 310, 810, 46, MARKER, CREME)
        contador(c, t, 0.0, 0, 6.03, 680, 790, 80, d=2.2, col=VERDE, casas=2, sufixo=" BI")
        return
    text(c, "EXEMPLO", 290, 810, 50, MARKER, CREME)
    if t < 20.1:
        numero_i(c, "R$ 0", 670, 820, 84, CREME)
    elif t < 37.2:
        contador(c, t, 20.1, 0, 150, 670, 790, 84, d=0.6, col=VERDE)
        if t < 23.5:
            entra(c, t, 20.1, 830, 720, chip("+ R$ 150", VERDE, CREME, 40, 0.04), anim="stamp")
    elif t < 58.4:
        contador(c, t, 37.2, 150, 1230, 670, 790, 84, d=0.8, col=VERDE)
        if t < 41.0:
            entra(c, t, 37.2, 820, 720, chip("+ R$ 1.080 (8 meses)", VERDE, CREME, 34, 0.04), anim="stamp")
    else:
        contador(c, t, 58.4, 1230, 3230, 670, 790, 84, d=0.8, col=VERDE)
        if t < 62.0:
            entra(c, t, 58.4, 830, 720, chip("+ R$ 2.000", VERDE, CREME, 40, 0.04), anim="stamp")


def detalhes(c, t):
    if t < 7.2:
        a = 1.0 if t < 6.7 else max(0.0, 1 - (t - 6.7) / 0.5)
        c.push_group(); notificacao(c, 540, 1040, 1.5, "Dinheiro parado!", "esperando você pedir", VERDE, "R$")
        c.pop_group_to_source(); c.paint_with_alpha(a)
    # 1) Valores a Receber
    if 10.9 <= t < 20.9:
        entra(c, t, 10.9, *L1, chip("R$ 6 BILHÕES", VERDE, CREME, 44, -0.04), anim="left")
        entra(c, t, 13.4, *R1, chip("bancos e consórcios", CREME, TINTA, 40, 0.04), anim="right")
    if 14.8 <= t < 20.9:
        entra(c, t, 14.8, *L2, chip("70%: até R$ 10", CREME, TINTA, 40, 0.03), anim="left")
    if 17.6 <= t < 20.9:
        entra(c, t, 17.6, *R2, chip("1 em 10: + de R$ 100", GOLD, TINTA, 40, -0.03), anim="stamp")
    if 20.9 <= t < 28.5:
        entra(c, t, 21.5, *C1, chip("valoresareceber.bcb.gov.br", CREME, NAVY, 40), anim="pop")
    if 25.1 <= t < 28.5:
        entra(c, t, 25.1, *L2, chip("CPF + nascimento", CREME, TINTA, 38, 0.03), anim="left")
    if 27.4 <= t < 28.5:
        entra(c, t, 27.4, *R2, chip("DE GRAÇA", VERDE, CREME, 46, -0.03), anim="stamp")
    # 2) Abono do PIS
    if 31.2 <= t < 43.5:
        entra(c, t, 31.4, *L1, chip("carteira em 2024", CREME, TINTA, 40, -0.04), anim="left")
    if 34.0 <= t < 43.5:
        entra(c, t, 34.0, *R1, chip("até ~R$ 2.766/mês", CREME, TINTA, 40, 0.04), anim="right")
    if 37.2 <= t < 43.5:
        entra(c, t, 37.2, *L2, chip("ATÉ R$ 1.621", VERDE, CREME, 44, 0.03), anim="left")
    if 40.0 <= t < 43.5:
        entra(c, t, 40.0, *R2, chip("276 mil não sacaram", GOLD, TINTA, 38, -0.03), anim="stamp")
    if 43.5 <= t < 46.2:
        entra(c, t, 43.6, *CM, chip("PRAZO: 28 DE DEZEMBRO", VERMELHO, CREME, 52), anim="stamp")
    if 46.2 <= t < 50.6:
        entra(c, t, 46.7, *C1, chip("app Carteira de Trabalho Digital", CREME, NAVY, 42), anim="pop")
        entra(c, t, 49.4, *C2, chip("aba BENEFÍCIOS", GOLD, TINTA, 42), anim="pop")
    # 3) FGTS antigo
    if 51.9 <= t < 59.9:
        entra(c, t, 51.9, *L1, chip("FGTS antigo", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 54.3, *R1, chip("1 conta por emprego", CREME, TINTA, 40, 0.04), anim="right")
    if 56.2 <= t < 59.9:
        entra(c, t, 56.2, *L2, chip("1 ano x R$ 2 mil", CREME, TINTA, 40, 0.03), anim="left")
    if 58.4 <= t < 59.9:
        entra(c, t, 58.4, *R2, chip("uns R$ 2.000", VERDE, CREME, 42, -0.03), anim="stamp")
    if 59.9 <= t < 65.5:
        entra(c, t, 60.3, 540, 935, chip("demitido sem justa causa", CREME, TINTA, 44, -0.02), anim="left")
        entra(c, t, 62.1, 540, 1030, chip("ou 3 anos sem carteira", CREME, TINTA, 44, 0.02), anim="right")
    if 64.2 <= t < 65.5:
        entra(c, t, 64.2, 540, 1125, chip("DÁ PRA SACAR", VERDE, CREME, 48), anim="stamp")
    if 65.5 <= t < 69.8:
        entra(c, t, 66.1, *CM, chip("app FGTS: conta por conta", GOLD, TINTA, 42), anim="pop")
    # aviso de golpe
    if 69.8 <= t < 74.6:
        entra(c, t, 70.7, *C1, chip("NINGUÉM MANDA LINK", VERMELHO, CREME, 46), anim="stamp")
        entra(c, t, 72.6, *C2, chip("nem liga oferecendo resgate", CREME, TINTA, 42), anim="pop")
    # exemplo final
    if 76.9 <= t < 85.7:
        entra(c, t, 77.8, *L1, chip("R$ 150 banco", CREME, TINTA, 44, -0.04), anim="left")
        entra(c, t, 79.8, *R1, chip("R$ 1.080 abono", CREME, TINTA, 44, 0.04), anim="right")
        entra(c, t, 81.3, *C2, chip("R$ 2.000 FGTS", CREME, TINTA, 46), anim="pop")
    if t >= 85.7:
        entra(c, t, 85.7, *CM, chip("QUANTO VOCÊ ACHOU?", GOLD, TINTA, 50), anim="pop")


def aviso(c, t):
    """faixa 'só site e app oficial' no topo da lista durante o alerta"""
    if 74.6 <= t < 76.9:
        entra(c, t, 74.6, 540, 1040, chip("SÓ SITE E APP OFICIAL", GOLD, TINTA, 54), anim="stamp")


def cena(c, t):
    luz("dia")
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "DINHEIRO ESQUECIDO", 540, 235, 56, CREME)
    lista(c, t)
    marcador(c, t)
    aviso(c, t)
    poses = ((0, "present"), (3.6, "finger_up"), (7.6, "finger_up"), (10.9, "point_r"), (17.6, "finger_up"), (20.9, "present"),
             (28.6, "finger_up"), (31.2, "point_r"), (36.8, "present"), (43.6, "finger_up"), (46.2, "present"),
             (50.6, "finger_up"), (54.3, "point_r"), (59.9, "present"), (64.2, "finger_up"), (69.8, "finger_up"),
             (72.6, "shrug"), (74.6, "finger_up"), (76.9, "present"), (83.2, "present"), (85.7, "present"))
    exprs = ((0, "confident"), (17.6, "shocked"), (20.9, "confident"), (37.2, "grin"), (40.0, "shocked"), (46.2, "confident"),
             (58.4, "grin"), (59.9, "confident"), (69.8, "shocked"), (74.6, "confident"), (83.2, "grin"))
    consultor_i(c, t, 540, 2250, 2.4, poses=poses, exprs=exprs, look=0.0)
    detalhes(c, t)


SCENES = [(0, 999.0, cena)]
