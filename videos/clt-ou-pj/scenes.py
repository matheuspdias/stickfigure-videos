"""CLT de R$ 5 mil ou PJ de R$ 7 mil? Só TikTok: vertical nativo 1080x1920, 88,3 s.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 1 bloco. Legendas palavra por palavra queimadas pelo tiktok.py.
Layout: título y~250, premissas pequenas y~330, palco até y 1230 (pés), legendas ~1400. Nada em x > 930.
Premissas (21/10/2026) no roteiro.txt."""
from engine import *  # noqa

VERTICAL = True

CX = 520
FY = 1230
SHIFT = 60
PINKISH = (1, 0.8, 0.76)
CLTC = BLUE      # cor do lado CLT
PJC = ORANGE     # cor do lado PJ

SFX = [(4.64, "tum"), (46.3, "soft_ding"), (56.9, "tum"), (78.0, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key", "transition")


# ---------------------------------------------------------------- helpers
def floor(c):
    line(c, 40, FY + 6, 1040, FY + 6, 4, LGRAY)


def clt_guy(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("shirt", CLTC); kw.setdefault("fid", 2)
    other(c, t, x, FY, s, poses, exprs, **kw)


def pj_guy(c, t, x, s, poses, exprs, **kw):
    kw.setdefault("shirt", PJC); kw.setdefault("hair", "tuft"); kw.setdefault("fid", 3)
    figure(c, t, x, FY, s, poses=poses, exprs=exprs, **kw)


def tag(s, col, size=54):
    """etiqueta colorida tipo crachá"""
    def f(c):
        w = text_w(c, s, size) + 44
        rrect(c, -w / 2, -size * 0.7, w, size * 1.4, 14); fs(c, col, 5)
        text(c, s, 0, 2, size, MARKER, WHITE)
    return f


def prem(c, t, t0, s, y=345):
    """premissa rápida em letra pequena, logo abaixo do título"""
    show(c, t, t0, CX, y, T(s, 38, DGRAY), anim="fade", d=0.3)


def row(label, val, col=INK, size=56):
    """linha de extrato: rótulo à esquerda, valor à direita (largura ~760)"""
    def f(c):
        text(c, label, -380, 0, size, HAND, INK, align="l")
        text(c, val, 380, 0, size + 4, MARKER, col, align="r")
    return f


def rule(c, w=760):
    line(c, -w / 2, 0, w / 2, 0, 5, DGRAY)


def stamp_txt(s, col=RED, size=70):
    def f(c):
        w = text_w(c, s, size) + 50
        c.save(); c.rotate(-0.07)
        rrect(c, -w / 2, -size * 0.75, w, size * 1.5, 12)
        rgb(c, col); c.set_line_width(9); c.stroke()
        text(c, s, 0, 0, size, MARKER, col)
        c.restore()
    return f


def strike(w=300, col=RED):
    return lambda c: line(c, -w / 2, 10, w / 2, -10, 10, col)


def item(s, ok=True, size=50):
    """item de lista com check verde ou x vermelho"""
    def f(c):
        c.save(); c.scale(0.55, 0.55)
        (check_icon if ok else x_icon)(c)
        c.restore()
        text(c, s, 42, 0, size, HAND, INK, align="l")
    return f


# ======================================================================= CENAS
def s01(c, t):  # 0 - 6.7  gancho: 7 mil PJ x 5 mil CLT
    floor(c)
    show(c, t, 0.0, 270, 300, M("R$ 7.000", 84, PJC), anim="stamp", d=0.3)
    show(c, t, 0.0, 270, 410, tag("PJ", PJC), anim="pop")
    show(c, t, 2.9, 770, 300, M("R$ 5.000", 84, CLTC), anim="stamp", d=0.3)
    show(c, t, 2.9, 770, 410, tag("CLT", CLTC), anim="pop")
    show(c, t, 4.64, CX, 560, lambda c: hl(c, "QUASE IGUAL?", 0, 0, 92, LYELLOW), anim="stamp")
    pj_guy(c, t, 260, 0.85, [(0, "arms_up"), (4.7, "shrug")], [(0, "grin"), (4.7, "think")], appear=0.0, look=0.5)
    clt_guy(c, t, 780, 0.85, [(0, "relax"), (4.7, "hips")], [(0, "worried"), (4.7, "confident")], appear=2.8, look=-0.5)
    hero(c, t, CX, FY, 0.6, [(0, "relax"), (4.7, "think")], [(0, "neutral"), (4.7, "think")], appear=4.4, look=0)


def s02(c, t):  # 6.7 - 18.3  CLT: líquido mensal
    floor(c)
    show(c, t, 6.8, CX - 200, 250, tag("CLT", CLTC, 60), anim="pop")
    show(c, t, 7.6, CX + 90, 250, M("R$ 5.000", 70, CLTC), anim="up")
    prem(c, t, 9.0, "tabela do INSS 2026 (até 14%)")
    show(c, t, 9.2, CX, 470, row("INSS", "- R$ 501", RED), anim="left", d=0.3)
    show(c, t, 11.0, CX, 570, row("Imposto de renda", "?", INK), anim="left", d=0.3, t1=12.4)
    show(c, t, 12.5, CX, 570, row("Imposto de renda", "R$ 0", GREEN), anim="fade", d=0.2)
    show(c, t, 14.4, CX, 680, lambda c: hl(c, "isento até R$ 5 mil em 2026", 0, 0, 46, LGREEN), anim="stamp")
    show(c, t, 16.3, CX, 760, sc(rule), anim="fade", d=0.2)
    show(c, t, 16.3, CX, 850, row("Sobram", "R$ 4.498", GREEN, 64), anim="up")
    clt_guy(c, t, 260, 0.62, [(0, "present"), (12.5, "thumb")], [(0, "neutral"), (12.5, "happy")], look=0.5)
    hero(c, t, 800, FY, 0.62, [(0, "relax"), (9.2, "point_lu"), (12.5, "finger_up")],
         [(0, "neutral"), (12.5, "confident")], prop=("r", prop_calculator), look=-0.5)


def s03(c, t):  # 18.3 - 28.0  CLT: o ano todo
    floor(c)
    title(c, t, 18.4, "CLT: o ano todo", y=250, size=74, col=CLTC)
    prem(c, t, 18.4, "12 salários + 13º + 1/3 de férias + FGTS de 8%")
    show(c, t, 18.7, 230, 560, icon_label(sc(calendar, "13", GREEN, 72, s=1.0), "13º", 50, 130), anim="pop")
    show(c, t, 19.96, CX, 560, icon_label(sc(beach_chair, s=0.6), "férias + 1/3", 50, 130), anim="pop")
    show(c, t, 21.5, 810, 560, icon_label(sc(piggy, s=0.7), "FGTS 8%", 50, 130), anim="pop")
    show(c, t, 22.6, CX, 830, lambda c: hl(c, "~ R$ 64,6 MIL/ANO", 0, 0, 84, LGREEN), anim="stamp")
    show(c, t, 25.36, CX, 960, M("= R$ 5.385 por mês", 64, CLTC), anim="up")
    prem(c, t, 25.6, "(no mês de férias, salário + 1/3 passa de 5 mil e paga IR)", y=395)
    hero(c, t, 880, FY, 0.5, [(0, "present"), (22.6, "arms_up")], [(0, "neutral"), (22.6, "grin")], look=-1)
    clt_guy(c, t, 150, 0.5, [(0, "relax"), (22.6, "thumb")], [(0, "happy")], look=1)


def s04(c, t):  # 28.0 - 35.3  PJ: não cabe no MEI
    floor(c)
    show(c, t, 28.2, CX, 250, group(at(-180, 0, tag("PJ", PJC, 60)), at(90, 0, M("R$ 7.000", 70, PJC))), anim="pop")
    show(c, t, 30.3, CX, 450, M("MEI", 90, NAVY), anim="stamp")
    show(c, t, 31.4, CX, 570, row("teto do MEI", "R$ 81 mil/ano", INK, 50), anim="left", d=0.3)
    show(c, t, 32.1, CX, 660, row("você fatura", "R$ 84 mil/ano", RED, 50), anim="left", d=0.3)
    show(c, t, 32.6, CX, 450, sc(big_x, 110), anim="stamp")
    prem(c, t, 32.6, "e várias profissões nem podem ser MEI:", y=750)
    prem(c, t, 32.6, "programador, médico, advogado, designer...", y=795)
    show(c, t, 33.72, CX, 900, lambda c: hl(c, "SIMPLES NACIONAL", 0, 0, 76, LYELLOW), anim="stamp")
    pj_guy(c, t, 200, 0.6, [(0, "wave"), (32.6, "head"), (33.8, "hips")], [(0, "happy"), (32.6, "shocked"), (33.8, "neutral")], look=1)
    hero(c, t, 860, FY, 0.55, [(0, "relax"), (30.4, "point_lu")], [(0, "neutral"), (32.6, "think")], look=-1)


def s05(c, t):  # 35.3 - 43.3  fator R: Anexo III x Anexo V
    floor(c)
    title(c, t, 35.4, "Fator R", y=250, size=80, col=NAVY)
    prem(c, t, 35.6, "pró-labore >= 28% do faturamento")
    show(c, t, 36.4, CX, 460, row("pró-labore 28%", "R$ 1.960", INK, 54), anim="left", d=0.3)
    # duas caixas: Anexo III (verde) e Anexo V (vermelho, apagado)
    def box(name, pct, col, sub):
        def f(c):
            rrect(c, -190, -150, 380, 300, 22); fs(c, WHITE, 7, col)
            text(c, name, 0, -85, 52, MARKER, col)
            text(c, pct, 0, 20, 110, MARKER, col)
            text(c, sub, 0, 110, 38, HAND, DGRAY)
        return f
    show(c, t, 38.08, 300, 730, box("ANEXO III", "6%", GREEN, "com fator R"), anim="pop")
    show(c, t, 41.04, 760, 730, box("ANEXO V", "15,5%", RED, "abaixo de 28%"), anim="pop")
    hero(c, t, CX, FY, 0.5, [(0, "present"), (38.1, "point_l"), (41.0, "point_r")],
         [(0, "neutral"), (38.1, "happy"), (41.0, "worried")], prop=("r", prop_pointer), look=0)


def s06(c, t):  # 43.3 - 51.1  PJ: líquido do mês e do ano
    floor(c)
    show(c, t, 43.35, CX, 250, group(at(-180, 0, tag("PJ", PJC, 60)), at(90, 0, M("R$ 7.000", 70, PJC))), anim="pop")
    prem(c, t, 43.4, "DAS 6% + INSS 11% do pró-labore + contador R$ 300")
    show(c, t, 43.4, CX, 450, row("DAS (6%)", "- R$ 420", RED), anim="left", d=0.3)
    show(c, t, 43.76, CX, 540, row("INSS pró-labore", "- R$ 216", RED), anim="left", d=0.3)
    show(c, t, 45.52, CX, 630, row("contador", "- R$ 300", RED), anim="left", d=0.3)
    show(c, t, 46.2, CX, 700, sc(rule), anim="fade", d=0.2)
    show(c, t, 46.28, CX, 785, row("Sobram", "R$ 6.064", GREEN, 64), anim="up")
    show(c, t, 48.84, CX, 940, lambda c: hl(c, "R$ 72,8 MIL/ANO", 0, 0, 84, LGREEN), anim="stamp")
    pj_guy(c, t, 170, 0.5, [(0, "relax"), (48.9, "arms_up")], [(0, "neutral"), (48.9, "grin")], look=1)
    hero(c, t, 880, FY, 0.5, [(0, "think"), (46.3, "thumb")], [(0, "think"), (46.3, "happy")],
         prop=("l", prop_calculator), look=-1)


def s07(c, t):  # 51.1 - 62.1  a virada: férias sem receber
    floor(c)
    title(c, t, 51.2, "Parece que o PJ ganhou...", y=250, size=64)
    base = 1000
    sc_k = 7.0   # px por mil
    # CLT
    hc = 64.6 * sc_k * ease_out(prog(t, 51.3, 0.5))
    show(c, t, 51.3, 330, base, lambda c: bar(c, hc, 190, CLTC, "CLT", "64,6 mil", 50), anim="fade", d=0.1)
    # PJ: 72,8 -> 66,4 quando para 30 dias
    k = ease_out(prog(t, 56.85, 0.6))
    v = 72.8 + (66.4 - 72.8) * k
    hp = v * sc_k * ease_out(prog(t, 51.6, 0.5))
    lab = f"{v:.1f}".replace(".", ",") + " mil"
    show(c, t, 51.6, 710, base, lambda c: bar(c, hp, 190, PJC, "PJ", lab, 50), anim="fade", d=0.1)
    show(c, t, 53.2, 760, 330, stamp_txt("FÉRIAS = R$ 0", RED, 52), anim="stamp", t1=56.6)
    show(c, t, 55.52, 300, 380, group(sc(calendar, "30", RED, 72, s=0.8), at(80, 0, lambda c: text(c, "dias parado", 0, 0, 44, HAND, RED, align="l"))),
         anim="pop", t1=58.9)
    show(c, t, 59.4, CX, 400, lambda c: hl(c, "~ R$ 150/mês de diferença", 0, 0, 56, LYELLOW), anim="stamp")
    prem(c, t, 59.3, "PJ faturando 11 meses; contador pago nos 12", y=320)
    hero(c, t, 520, FY, 0.48, [(0, "shrug"), (56.9, "head"), (59.4, "present_l")],
         [(0, "think"), (56.9, "shocked"), (59.4, "confident")], look=-1)


def s08(c, t):  # 62.1 - 76.4  o que a conta não mostra
    floor(c)
    title(c, t, 62.2, "O que a conta não mostra", y=250, size=64)
    line(c, CX, 330, CX, 1000, 4, LGRAY) if t > 63.9 else None
    show(c, t, 63.9, 280, 360, tag("CLT", CLTC, 52), anim="pop")
    for i, (t0, s) in enumerate(((64.96, "vale-refeição"), (66.04, "plano de saúde"),
                                 (67.16, "seguro-desemprego"), (68.48, "multa 40% FGTS"))):
        show(c, t, t0, 70, 470 + i * 95, item(s, True, 44), anim="left", d=0.3)
    show(c, t, 70.16, 760, 360, tag("PJ", PJC, 52), anim="pop")
    for i, (t0, s) in enumerate(((71.04, "mais na mão"), (72.36, "liberdade"), (73.36, "vários clientes"))):
        show(c, t, t0, 560, 470 + i * 95, item(s, True, 44), anim="left", d=0.3)
    show(c, t, 74.72, 740, 790, group(sc(shield, LGRAY, s=0.55), at(0, 0, sc(big_x, 60))), anim="pop")
    show(c, t, 75.2, 740, 900, T("sem rede de proteção", 42, RED), anim="up")
    clt_guy(c, t, 230, 0.48, [(0, "relax"), (68.5, "thumb")], [(0, "neutral"), (68.5, "happy")], look=0.5)
    pj_guy(c, t, 600, 0.48, [(0, "relax"), (72.4, "arms_up"), (74.8, "shrug")],
           [(0, "neutral"), (72.4, "grin"), (74.8, "worried")], look=-0.5)
    hero(c, t, 880, FY, 0.42, [(0, "think")], [(0, "think")], look=-1)


def s09(c, t):  # 76.4 - 84.6  regra de bolso
    floor(c)
    show(c, t, 76.56, CX, 250, lambda c: ribbon(c, "REGRA DE BOLSO", NAVY, 60), anim="stamp")
    show(c, t, 78.0, CX, 400, T("pra empatar só no dinheiro:", 54), anim="up")
    show(c, t, 80.56, CX, 540, M("PJ ~35% A MAIS", 100, PJC), anim="stamp")
    show(c, t, 81.2, CX, 660, T("R$ 5 mil de CLT  =  uns R$ 6,8 mil de PJ", 46, DGRAY), anim="fade")
    show(c, t, 82.8, CX, 820, lambda c: hl(c, "+ benefícios: mais ainda", 0, 0, 62, LYELLOW), anim="stamp")
    hero(c, t, CX, FY, 0.55, [(0, "present"), (80.6, "finger_up"), (82.8, "present")],
         [(0, "neutral"), (80.6, "confident")], prop=("l", prop_pointer), look=0)


def s10(c, t):  # 84.6 - fim  pergunta
    floor(c)
    show(c, t, 84.76, 300, 320, tag("CLT", CLTC, 80), anim="pop")
    show(c, t, 85.6, CX, 320, M("ou", 64, INK), anim="pop")
    show(c, t, 85.92, 740, 320, tag("PJ?", PJC, 80), anim="pop")
    show(c, t, 86.72, CX, 520, M("Trocaria?", 100, NAVY), anim="stamp")
    show(c, t, 87.6, CX + 120, 760, group(lambda c: speech(c, 520, 130, -160, 110), T("Comenta aí!", 62)), anim="pop")
    clt_guy(c, t, 160, 0.55, [(0, "wave")], [(0, "happy")], look=1)
    pj_guy(c, t, 880, 0.55, [(0, "wave")], [(0, "happy")], look=-1)
    hero(c, t, 330, FY, 0.65, [(0, "point_r")], [(0, "grin")], look=1)


def _shift(fn):
    def f(c, t):
        c.save(); c.translate(0, SHIFT); fn(c, t); c.restore()
    f.__name__ = fn.__name__
    return f


SCENES = [
    (0.0, 6.7, s01), (6.7, 18.3, s02), (18.3, 28.0, s03), (28.0, 35.3, s04), (35.3, 43.3, s05),
    (43.3, 51.1, s06), (51.1, 62.1, s07), (62.1, 76.4, s08), (76.4, 84.6, s09), (84.6, 999.0, s10),
]
SCENES = [(a, b, _shift(f)) for a, b, f in SCENES]
