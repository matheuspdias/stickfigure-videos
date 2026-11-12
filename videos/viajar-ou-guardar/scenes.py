"""Viajar todo ano ou guardar? Ana x Bruno, 10 anos. Só TikTok: vertical nativo 1080x1920, 66,0 s, estilo ilustrado.
Narração Calm Carlos (HeyGen), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Contas em contas.py: R$ 5.000/ano por 10 anos a ~10% a.a., IR 15%: ~R$ 75 mil líquido ("mais de setenta mil");
meio-termo (ano sim, ano não): ~R$ 36-39 mil ("quase quarenta mil")."""
from engine import *  # noqa
VERTICAL = True
from ilustrado import *  # noqa

STYLE = "ilustrado"
SFX = [(2.8, "tum"), (26.5, "soft_ding"), (39.6, "tum"), (65.2, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")

ANA_COR = PURPLE
BRUNO_COR = BLUE
AREIA_ = (0.93, 0.84, 0.62)

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


def check(c, x, y, ok=True, r=40):
    c.new_sub_path(); c.arc(x, y, r, 0, 6.283); rgb(c, VERDE if ok else VERMELHO); c.fill()
    c.set_line_width(r * 0.22); rgb(c, CREME)
    if ok:
        c.move_to(x - r * 0.45, y); c.line_to(x - r * 0.1, y + r * 0.38); c.line_to(x + r * 0.5, y - r * 0.38)
    else:
        c.move_to(x - r * 0.4, y - r * 0.4); c.line_to(x + r * 0.4, y + r * 0.4)
        c.move_to(x + r * 0.4, y - r * 0.4); c.line_to(x - r * 0.4, y + r * 0.4)
    c.stroke()

def mala(c, s=1.0, cor=(0.85, 0.30, 0.28)):
    """mala de rodinha (origem = base)"""
    c.save(); c.scale(s, s)
    c.set_line_width(10); rgb(c, TINTA)
    c.move_to(-30, -250); c.line_to(-30, -330); c.line_to(30, -330); c.line_to(30, -250); c.stroke()
    rr(c, -95 + 6, -260 + 8, 190, 240, 22); rgb(c, (0, 0, 0), 0.2); c.fill()
    rr(c, -95, -260, 190, 240, 22); rgb(c, cor); c.fill()
    for dx in (-45, 0, 45):
        c.rectangle(dx - 5, -245, 10, 210); rgb(c, (0, 0, 0), 0.15); c.fill()
    rr(c, -60, -180, 70, 44, 8); rgb(c, GOLD); c.fill()
    for dx in (-60, 60):
        c.new_sub_path(); c.arc(dx, -8, 14, 0, 6.283); rgb(c, TINTA); c.fill()
    c.set_line_width(6); rgb(c, TINTA); rr(c, -95, -260, 190, 240, 22); c.stroke()
    c.restore()


def praia(c, t):
    """praia vertical: céu, mar, areia, sol"""
    lgrad(c, 0, 0, 0, 900, ((0, (0.45, 0.72, 0.95), 1), (1, (0.78, 0.90, 0.98), 1)))
    c.rectangle(0, 0, 1080, 1920); c.fill()
    rglow(c, 930, 560, 200, (1.0, 0.92, 0.55), 0.5)
    c.new_sub_path(); c.arc(930, 560, 80, 0, 6.283); rgb(c, (1.0, 0.86, 0.35)); c.fill()
    c.rectangle(0, 900, 1080, 400); rgb(c, (0.20, 0.55, 0.80)); c.fill()
    for i in range(6):
        y = 940 + i * 45
        c.move_to(0, y)
        for x in range(0, 1101, 30):
            c.line_to(x, y + 6 * math.sin(x / 60 + t * 2 + i))
        rgb(c, (1, 1, 1), 0.35); c.set_line_width(3); c.stroke()
    c.move_to(0, 1180)
    for x in range(0, 1101, 30):
        c.line_to(x, 1180 + 14 * math.sin(x / 90 + t * 1.5))
    c.line_to(1080, 1920); c.line_to(0, 1920); c.close_path(); rgb(c, AREIA_); c.fill()


def x_vermelho(c, x, y, r=40):
    check(c, x, y, False, r)


# ======================================================================= CENAS
def s01(c, t):  # 0 - 4.4  gancho: viajar todo ano te custa + de 70 mil?
    fundo_marca(c, t, "vermelho", holofote=(260, 1100))
    numero_i(c, "VIAJAR TODO ANO", 520, 240, 96, CREME)
    numero_i(c, "TE CUSTA", 520, 360, 90, CREME)
    if t < 2.4:
        numero_i(c, "R$ 70 MIL?", 540, 520, 150, GOLD)
    else:
        k = 1 + 0.12 * math.sin(clamp01((t - 2.4) / 0.3) * math.pi)
        c.save(); c.translate(540, 520); c.scale(k, k); numero_i(c, "+ DE R$ 70 MIL", 0, 0, 120, GOLD); c.restore()
    entra(c, t, 0.0, 780, 1270, lambda c: mala(c, 1.2), anim="up", d=0.3)
    consultor_i(c, t, 260, 1300, 1.35, poses=((0, "head"), (2.4, "point_r")), exprs=((0, "shocked"), (2.4, "shocked")), look=0.6)


def s02(c, t):  # 4.4 - 8.2  ou a melhor decisão da sua vida? depende de 1 coisa
    fundo_marca(c, t, "verde", holofote=(520, 1100))
    numero_i(c, "OU A MELHOR", 520, 240, 100, CREME)
    numero_i(c, "DECISÃO DA SUA VIDA?", 520, 350, 70, GOLD)
    entra(c, t, 6.8, 520, 530, selo("DEPENDE DE 1 COISA", NAVY, 64, GOLD), anim="stamp")
    if t > 7.6:
        numero_i(c, "(TE CONTO NO FIM)", 520, 660, 48, CREME)
    consultor_i(c, t, 520, 1300, 1.1, poses=((0, "shrug"), (6.8, "finger_up")), exprs=((0, "think"), (6.8, "confident")), look=0.0)


def s03(c, t):  # 8.2 - 13.9  Ana e Bruno ganham igual; 5 mil sobrando por ano
    cena_rua(c, t, "dia", carros=False)
    numero_i(c, "ANA E BRUNO", 520, 240, 100, CREME)
    entra(c, t, 9.5, 520, 370, selo("GANHAM IGUAL", NAVY, 60, GOLD), anim="stamp")
    contador(c, t, 12.0, 0, 5000, 520, 530, 130, d=0.8, col=VERDE)
    if t > 13.0:
        numero_i(c, "SOBRANDO POR ANO", 520, 650, 54, CREME)
    pessoa(c, t, 210, 1300, 1.3, "ana", poses=((0, "wave"), (12.0, "thumb")), exprs=((0, "happy"), (12.0, "grin")), look=0.4)
    pessoa(c, t, 860, 1300, 1.3, "bruno", poses=((0, "wave"), (12.0, "thumb")), exprs=((0, "happy"), (12.0, "grin")), look=-0.4)


def s04(c, t):  # 13.9 - 20.4  Ana viaja: praia, serra, fora; 10 anos, 10 viagens
    praia(c, t)
    numero_i(c, "A ANA VIAJA", 480, 240, 100, NAVY, contorno=CREME)
    for i, (tt, s, cor) in enumerate(((15.0, "PRAIA", (0.20, 0.55, 0.80)), (15.7, "SERRA", VERDE), (16.6, "EXTERIOR", ROXO_V))):
        entra(c, t, tt, 650, 420 + i * 120, selo(s, cor, 56, CREME), anim="right")
    entra(c, t, 18.0, 650, 790, selo("10 ANOS = 10 VIAGENS", VERMELHO, 52, CREME), anim="stamp")
    entra(c, t, 14.2, 470, 1300, lambda c: mala(c, 0.8), anim="up")
    pessoa(c, t, 190, 1300, 1.3, "ana", poses=((0, "arms_up"), (18.0, "thumb")), exprs=((0, "grin"), (18.0, "happy")), look=0.6)


ROXO_V = (0.55, 0.36, 0.72)


def s05(c, t):  # 20.4 - 24.0  Bruno não viaja: investe os 5 mil todo ano
    cena_sala(c, t, "tarde")
    numero_i(c, "O BRUNO", 520, 240, 100, GOLD)
    numero_i(c, "NÃO VIAJA", 520, 350, 84, CREME) if t > 20.9 else None
    entra(c, t, 21.8, 640, 520, cartao("Investe todo ano", "R$ 5 mil", VERDE, 640), anim="right")
    pessoa(c, t, 220, 1300, 1.35, "bruno", poses=((0, "stand"), (21.8, "hold")), exprs=((0, "neutral"), (21.8, "confident")),
           look=0.6, prop=("r", prop_celular_i) if t > 21.8 else None)


def s06(c, t):  # 24.0 - 28.0  10 anos depois: Bruno tem + de 70 mil
    fundo_marca(c, t, "verde", holofote=(220, 1100))
    numero_i(c, "10 ANOS DEPOIS", 520, 240, 96, CREME)
    numero_i(c, "O BRUNO TEM", 520, 350, 70, GOLD) if t > 25.4 else None
    if t < 27.4:
        contador(c, t, 26.4, 0, 70000, 560, 520, 140, d=0.9, col=GOLD)
    else:
        numero_i(c, "+ DE R$ 70 MIL", 560, 520, 110, GOLD)
    if t > 26.6:
        c.save(); c.translate(720, 1250); pilha_moedas(c, 7, 40, t, 26.6); c.restore()
    pessoa(c, t, 220, 1300, 1.35, "bruno", poses=((0, "stand"), (26.5, "arms_up")), exprs=((0, "happy"), (26.5, "grin")), look=0.6)


def s07(c, t):  # 28.0 - 32.2  Ana: zero na conta, 10 viagens na memória
    fundo_marca(c, t, "navy", holofote=(220, 1100))
    numero_i(c, "A ANA TEM", 520, 240, 100, CREME)
    if t > 28.5:
        numero_i(c, "R$ 0", 600, 420, 150, VERMELHO, contorno=CREME)
        numero_i(c, "NA CONTA", 600, 550, 60, CREME)
    entra(c, t, 30.2, 640, 720, selo("10 VIAGENS NA MEMÓRIA", ROXO_V, 46, CREME), anim="stamp")
    pessoa(c, t, 180, 1300, 1.3, "ana", poses=((0, "stand"), (30.2, "hips")), exprs=((0, "neutral"), (30.2, "grin")), look=0.6)


def s08(c, t):  # 32.2 - 36.6  quem ganhou? a internet briga; a resposta é outra
    fundo_marca(c, t, "navy", holofote=(520, 1100))
    numero_i(c, "QUEM GANHOU?", 520, 250, 110, GOLD)
    entra(c, t, 33.2, 520, 410, selo("A INTERNET BRIGA", VERMELHO, 60, CREME), anim="stamp")
    entra(c, t, 34.7, 520, 550, selo("A RESPOSTA É OUTRA", VERDE, 56, CREME), anim="stamp")
    consultor_i(c, t, 520, 1300, 1.15, poses=((0, "shrug"), (34.7, "finger_up")), exprs=((0, "think"), (34.7, "confident")), look=0.0)


def s09(c, t):  # 36.6 - 40.7  o problema nunca foi viajar; é viajar parcelado
    fundo_marca(c, t, "creme")
    numero_i(c, "O PROBLEMA", 520, 240, 100, NAVY, contorno=CREME)
    numero_i(c, "NUNCA FOI VIAJAR", 520, 350, 76, NAVY, contorno=CREME) if t > 37.2 else None
    if t > 39.3:
        k = 1 + 0.12 * math.sin(clamp01((t - 39.3) / 0.3) * math.pi)
        c.save(); c.translate(560, 540); c.scale(k, k); _ = selo("É VIAJAR PARCELADO", VERMELHO, 64, CREME)(c); c.restore()
    entra(c, t, 37.0, 760, 1270, lambda c: mala(c, 1.0), anim="up")
    consultor_i(c, t, 240, 1300, 1.3, poses=((0, "finger_up"), (39.3, "point_r")), exprs=((0, "think"), (39.3, "shocked")), look=0.6)


def s10(c, t):  # 40.7 - 48.1  paga em 10x: o ano inteiro pagando a viagem do ano passado; sem dinheiro, sem paz
    fundo_marca(c, t, "vermelho", holofote=(220, 1100))
    if t < 45.4:
        numero_i(c, "VIAGEM EM 10X", 520, 240, 96, CREME)
        entra(c, t, 41.5, 640, 640, lambda c: fatura(c, t, 0, 0, 0.85, itens=(("Viagem 2025", "3/10"), ("Viagem 2026", "1/10"), ("Mercado", "R$ 640")),
                                                     total="R$ 2.480", vence="Vence dia 10", t0=41.6), anim="up")
        if t > 43.8:
            numero_i(c, "O ANO INTEIRO PAGANDO", 640, 880, 46, CREME)
            numero_i(c, "A VIAGEM DO ANO PASSADO", 640, 950, 46, GOLD)
    else:
        numero_i(c, "NO FIM", 520, 240, 100, CREME)
        for tt, s, y in ((45.9, "Sem o dinheiro", 450), (47.0, "Sem a paz", 580)):
            if t > tt:
                k = ease_out(prog(t, tt, 0.35))
                c.save(); c.translate(640, y); c.scale(k, k)
                cartao(s, "", TINTA, 540, 100)(c); x_vermelho(c, 210, 0, 34)
                c.restore()
    pessoa(c, t, 210, 1300, 1.3, "ana", poses=((0, "hold"), (43.8, "head")), exprs=((0, "worried"), (43.8, "desperate")),
           look=0.6, prop=("r", prop_celular_i) if t < 43.8 else None)


def s11(c, t):  # 48.1 - 56.4  meio-termo: um ano sim, um não; 5 viagens e quase 40 mil
    fundo_marca(c, t, "creme")
    numero_i(c, "O MEIO-TERMO", 520, 240, 104, NAVY, contorno=CREME)
    entra(c, t, 49.5, 600, 390, cartao("Viaja um ano sim,", "", TINTA, 640, 96), anim="right")
    entra(c, t, 50.9, 600, 500, cartao("investe no outro", "", TINTA, 640, 96), anim="right")
    entra(c, t, 53.1, 600, 640, selo("5 VIAGENS", ROXO_V, 60, CREME), anim="stamp")
    if t > 54.4:
        numero_i(c, "+ QUASE", 640, 750, 66, NAVY, contorno=CREME)
        contador(c, t, 54.6, 0, 40000, 640, 860, 110, d=0.9, col=VERDE)
    consultor_i(c, t, 190, 1300, 0.95, poses=((0, "present"), (53.1, "thumb")), exprs=((0, "neutral"), (53.1, "grin")), look=0.6)


def s12(c, t):  # 56.4 - 63.1  a coisa que decide: paga antes = lembrança; paga depois = boleto
    fundo_marca(c, t, "navy", holofote=(220, 1100))
    numero_i(c, "A COISA QUE DECIDE", 520, 240, 80, GOLD)
    entra(c, t, 58.4, 600, 400, cartao("Viagem paga antes", "", TINTA, 660, 100), anim="right")
    entra(c, t, 59.9, 600, 510, selo("LEMBRANÇA", VERDE, 66, CREME), anim="stamp")
    entra(c, t, 61.1, 600, 650, cartao("Viagem paga depois", "", TINTA, 660, 100), anim="right")
    entra(c, t, 62.3, 600, 760, selo("BOLETO", VERMELHO, 70, CREME), anim="stamp")
    consultor_i(c, t, 200, 1300, 1.05, poses=((0, "finger_up"), (59.9, "thumb"), (62.3, "shrug")),
                exprs=((0, "think"), (59.9, "grin"), (62.3, "worried")), look=0.6)


def s13(c, t):  # 63.1 - fim  time Ana ou time Bruno?
    praia(c, t)
    numero_i(c, "VIAJAR OU", 520, 250, 110, NAVY, contorno=CREME)
    numero_i(c, "GUARDAR?", 520, 370, 120, GOLD)
    entra(c, t, 63.6, 270, 540, selo("TIME ANA", ANA_COR, 54, CREME), anim="stamp")
    entra(c, t, 64.5, 770, 540, selo("TIME BRUNO", BRUNO_COR, 54, CREME), anim="stamp")
    entra(c, t, 65.1, 520, 680, selo("COMENTA", VERMELHO, 62, CREME), anim="stamp")
    pessoa(c, t, 250, 1300, 1.2, "ana", poses=((0, "stand"), (63.6, "thumb")), exprs=((0, "happy"), (63.6, "grin")), look=0.4)
    pessoa(c, t, 790, 1300, 1.2, "bruno", poses=((0, "stand"), (64.5, "thumb")), exprs=((0, "happy"), (64.5, "grin")), look=-0.4)
    consultor_i(c, t, 520, 1330, 0.9, poses=((0, "present"),), exprs=((0, "happy"),), look=0.0)


SCENES = [(0, 4.4, s01), (4.4, 8.2, s02), (8.2, 13.9, s03), (13.9, 20.4, s04), (20.4, 24.0, s05),
          (24.0, 28.0, s06), (28.0, 32.2, s07), (32.2, 36.6, s08), (36.6, 40.7, s09), (40.7, 48.1, s10),
          (48.1, 56.4, s11), (56.4, 63.1, s12), (63.1, 999.0, s13)]
