"""Alugar ou comprar? A conta que quase ninguém faz.
Narração Calm Carlos (HeyGen, ElevenLabs v4), 3 blocos.
Tempos absolutos: bloco1 0,00 | bloco2 163,59 | bloco3 350,42 | fim da fala 576,98 | +15 s de tela final.
Premissas (contas.py): imóvel R$ 300 mil, entrada 20%, SAC 30 anos a 11,5% a.a. (sem TR/seguros), ITBI+cartório 4%,
manutenção 0,5% a.a., aluguel 6% a.a. do valor (FipeZap jul/2026), imóvel e aluguel +4,5% a.a., investimento 10% a.a. líquido.
MCMV faixa 3: 7,66% a.a., entrada 35% (Sul/Sudeste)."""
from engine import *  # noqa

PINKISH = (1, 0.8, 0.76)
C_COL = ORANGE   # Comprador
I_COL = PURPLE   # Inquilino
LORANGE = (1.0, 0.86, 0.70)
LPURPLE = (0.88, 0.83, 0.98)


def grow(t, t0, d=0.9):
    return ease_out(prog(t, t0, d))


def L(s, size=50, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col, align="l")


def comprador(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", C_COL); kw.setdefault("hair", "tuft"); kw.setdefault("fid", 2)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def inquilino(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", I_COL); kw.setdefault("fid", 3)
    other(c, t, x, y, s, poses, exprs, **kw)


def tio(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", GRAY); kw.setdefault("hair", None); kw.setdefault("fid", 5)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def strike(w=260, col=RED):
    return lambda c: line(c, -w / 2, 6, w / 2, -6, 9, col)


def down_arrow(col=RED, h=110):
    return lambda c: arrow(c, 0, -h / 2, 0, h / 2, col, 10, 0, 28)


def up_arrow(col=GREEN, h=110):
    return lambda c: arrow(c, 0, h / 2, 0, -h / 2, col, 10, 0, 28)


def tag(s, col=YELLOW, size=46):
    return lambda c: price_tag(c, s, col, size)


def name_tag(s, col):
    return lambda c: hl(c, s, 0, 0, 46, col, WHITE, MARKER, 18, 0)


def lerp_keys(t, keys):
    """interpola valores (tempo, valor) com ease"""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t < t1:
            return v0 + (v1 - v0) * ease_io(clamp01((t - t0) / max(0.01, t1 - t0)))
    return keys[-1][1]


def money(v):
    """mil reais -> texto curto"""
    if v >= 1000:
        return ("R$ %.2f mi" % (v / 1000)).replace(".", ",")
    return "R$ %d mil" % round(v)


def race_bars(c, t, t0, keys_c, keys_i, vmax, hmax=470, base=900, xc=760, xi=1160):
    """duas barras (Comprador laranja, Inquilino roxo) que crescem conforme keys (tempo, mil reais)"""
    if t < t0:
        return
    a = grow(t, t0, 0.5)
    for x, keys, col, lab in ((xc, keys_c, C_COL, "Comprador"), (xi, keys_i, I_COL, "Inquilino")):
        v = lerp_keys(t, keys)
        h = hmax * v / vmax * a
        c.save(); c.translate(x, base)
        bar(c, h, 200, col, None, None)
        c.restore()
        text(c, lab, x, base + 48, 46, HAND)
        if v > 0.5:
            text(c, money(v), x, base - h - 42, 50, MARKER, col)


def year_badge(c, t, keys, x=960, y=245):
    """contador 'ANO N' que troca nas marcas (tempo, ano)"""
    yr = val_at(t, keys)
    if yr is None or t < keys[0][0]:
        return
    t_last = max(k for k, _ in keys if k <= t)
    show(c, t, t_last, x, y, lambda c: hl(c, f"ANO {yr}", 0, 0, 70, LYELLOW), anim="pop", d=0.35)


def ruler(c, t, t0, lo, hi, val, thr, left_txt, right_txt, left_col, right_col, unit="%", t_thr=None, y=560,
          t_left=None, t_right=None, val_lbl=None):
    """régua de 'balança vira': valor atual (marcador) e limite (linha tracejada)"""
    if t < t0:
        return
    x0, x1 = 380, 1540
    X = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    a = grow(t, t0, 0.7)
    xe = x0 + (x1 - x0) * a
    rrect(c, x0, y - 22, xe - x0, 44, 22); fs(c, LGRAY, 5)
    for k in range(int(lo), int(hi) + 1):
        if X(k) <= xe:
            line(c, X(k), y + 26, X(k), y + 44, 4, DGRAY)
            text(c, f"{k}{unit}", X(k), y + 72, 34, HAND, DGRAY)
    if t_thr is not None and t >= t_thr:
        p = grow(t, t_thr, 0.5)
        xt = X(thr)
        c.save(); c.set_dash([14, 10]); line(c, xt, y - 120 * p, xt, y + 30, 6, RED); c.restore()
        # zonas
        if t_left is not None and t >= t_left:
            show(c, t, t_left, (x0 + xt) / 2, y - 175, lambda c: hl(c, left_txt, 0, 0, 44, left_col), anim="up")
        if t_right is not None and t >= t_right:
            show(c, t, t_right, (xt + x1) / 2, y - 175, lambda c: hl(c, right_txt, 0, 0, 44, right_col), anim="up")
    if t >= t0 + 0.6:
        p = ease_out_back(prog(t, t0 + 0.6, 0.45))
        xv = X(val)
        c.save(); c.translate(xv, y); c.scale(p, p)
        poly(c, [(-22, -64), (22, -64), (0, -26)]); fs(c, NAVY, 5)
        circle(c, 0, 0, 22, GOLD, 5)
        c.restore()
        if val_lbl:
            text(c, val_lbl, xv, y + 128, 44, MARKER, NAVY)


def number_head(c, t, t0, n, s, col=LYELLOW):
    show(c, t, t0, 960, 125, lambda c: hl(c, f"{n}. {s}", 0, 0, 66, col), anim="stamp")


# ======================================================================= BLOCO 1
def s01(c, t):  # 0 - 13.2  "aluguel é dinheiro jogado fora"
    tio(c, t, 470, 1010, 1.05, [(0, "point_r"), (8.0, "hips"), (9.8, "point_r")],
        [(0, "confident"), (8.0, "grin")], appear=0.0, look=1)
    show(c, t, 0.05, 900, 330, lambda c: speech(c, 700, 210, -230, 140), anim="pop")
    show(c, t, 0.3, 900, 315, T("Aluguel é dinheiro", 62), anim="fade")
    show(c, t, 1.3, 900, 390, T("jogado fora!", 62, RED), anim="fade")
    show(c, t, 5.6, 1180, 520, T("pai", 52, DGRAY), anim="up")
    show(c, t, 6.3, 1380, 520, T("tio", 52, DGRAY), anim="up")
    show(c, t, 7.0, 1600, 520, T("vizinho", 52, DGRAY), anim="up")
    show(c, t, 9.9, 1180, 950, sc(apartment, s=0.6), anim="pop")
    for i, tt in enumerate((10.7, 11.2, 11.7)):
        k = grow(t, tt, 1.2)
        if t > tt:
            show(c, t, tt, 1280 + 160 * k + i * 30, 820 - 120 * k + i * 40, sc(bill, s=0.55), anim="fade", rot=0.3 * k)
    show(c, t, 12.4, 1620, 840, sc(x_icon, 50), anim="stamp")


def s02(c, t):  # 13.2 - 25.2  e se quem alugou terminar com mais?
    title(c, t, 13.3, "E se...", y=120, size=66)
    inquilino(c, t, 420, 1010, 1.0, [(0, "stand"), (18.4, "arms_up"), (22.2, "shrug")],
              [(0, "neutral"), (18.4, "grin"), (22.2, "worried")], appear=14.9, look=1)
    show(c, t, 15.1, 420, 300, name_tag("ALUGOU", I_COL), anim="pop")
    comprador(c, t, 1500, 1010, 1.0, [(0, "stand"), (19.6, "hips"), (23.4, "arms_up")],
              [(0, "neutral"), (19.6, "worried"), (23.4, "grin")], appear=19.5, look=-1)
    show(c, t, 19.7, 1500, 300, name_tag("COMPROU", C_COL), anim="pop")
    show(c, t, 16.7, 960, 230, T("30 anos depois...", 52, DGRAY), anim="up")
    # barras que trocam
    if t > 18.3:
        k = grow(t, 23.4, 1.0) if t > 23.4 else 0
        hi_, lo_ = 400, 250
        hl_ = hi_ + (lo_ - hi_) * k
        hc_ = lo_ + (hi_ - lo_) * k
        a = grow(t, 18.3, 0.6)
        c.save(); c.translate(820, 920); bar(c, hl_ * a, 170, I_COL); c.restore()
        if t > 19.6:
            a2 = grow(t, 19.6, 0.6)
            c.save(); c.translate(1100, 920); bar(c, hc_ * a2, 170, C_COL); c.restore()
    show(c, t, 21.1, 960, 330, lambda c: hl(c, "mudando 1 número", 0, 0, 52, LYELLOW), anim="stamp", t1=24.6)
    show(c, t, 23.5, 960, 330, lambda c: hl(c, "o contrário!", 0, 0, 56, PINKISH), anim="stamp")


def s03(c, t):  # 25.2 - 33.1  a conta que quase ninguém faz
    show(c, t, 25.3, 960, 140, lambda c: ribbon(c, "A CONTA QUE QUASE NINGUÉM FAZ", NAVY, 58), anim="stamp")
    hero(c, t, 360, 1010, 1.1, [(0, "present"), (28.8, "shrug"), (30.8, "finger_up")],
         [(0, "happy"), (28.8, "neutral"), (30.8, "confident")], appear=25.25, look=1, prop=("l", prop_calculator))
    show(c, t, 28.9, 1150, 560, sc(balance, 0.0,
                                   lambda c: sc(house, s=0.55)(c), lambda c: sc(house_key, s=0.55)(c), s=1.0), anim="pop")
    show(c, t, 29.4, 1150, 820, T("sem torcida pra nenhum lado", 50, DGRAY), anim="up")
    show(c, t, 31.0, 1150, 930, lambda c: hl(c, "quem decide é a matemática", 0, 0, 54, LGREEN), anim="stamp")


def s04(c, t):  # 33.1 - 44.9  o cenário
    title(c, t, 33.2, "O cenário", y=120, size=66)
    show(c, t, 34.7, 470, 900, sc(apartment, s=1.25), anim="drop")
    show(c, t, 35.7, 470, 310, tag("R$ 300 mil", YELLOW, 52), anim="pop")
    show(c, t, 37.7, 1000, 380, L("entrada de", 52, DGRAY), anim="up")
    show(c, t, 38.4, 1300, 380, M("20%", 70, NAVY), anim="pop")
    show(c, t, 39.5, 1530, 380, lambda c: hl(c, "R$ 60 mil", 0, 0, 58, LGREEN), anim="stamp")
    show(c, t, 40.9, 1000, 560, L("financia", 52, DGRAY), anim="up")
    show(c, t, 42.0, 1420, 560, lambda c: hl(c, "R$ 240 mil", 0, 0, 62, PINKISH), anim="stamp")
    show(c, t, 43.6, 1180, 790, group(sc(calendar, "30", NAVY, s=0.8), at(170, 0, L("anos", 60))), anim="pop")
    hero(c, t, 1700, 1050, 0.72, [(0, "present_l")], [(0, "happy")], appear=33.2, look=-1)


def s05(c, t):  # 44.9 - 59.2  qual juro?
    title(c, t, 44.95, "Qual juro?", y=120, size=66)
    hero(c, t, 300, 1010, 1.05, [(0, "think"), (45.9, "point_r"), (55.4, "thumb")],
         [(0, "think"), (45.9, "neutral"), (55.4, "confident")], appear=44.95, look=1)
    rates = [("Caixa", 10.26), ("Bradesco", 11.45), ("BB", 11.60), ("Santander", 11.69), ("Itaú", 11.99)]
    for i, (nm, r) in enumerate(rates):
        tt = 47.2 + i * 0.35
        x = 720 + i * 230
        if t > tt:
            k = grow(t, tt, 0.6)
            h = (r - 8.5) * 110 * k
            c.save(); c.translate(x, 760); bar(c, h, 150, LBLUE, None, None); c.restore()
            text(c, nm, x, 808, 38, HAND)
            if t > tt + 0.4:
                text(c, ("%.2f%%" % r).replace(".", ","), x, 760 - h - 34, 40, MARKER, NAVY)
    show(c, t, 48.7, 960, 205, T("outubro de 2026, ao ano + TR", 44, DGRAY), anim="fade")
    if t > 55.4:
        p = grow(t, 55.4, 0.5)
        yy = 760 - (11.4 - 8.5) * 110
        c.save(); c.set_dash([16, 10]); line(c, 600, yy, 600 + 1100 * p, yy, 6, RED); c.restore()
    show(c, t, 56.9, 1180, 930, lambda c: hl(c, "média: uns 11,5% ao ano", 0, 0, 58, LYELLOW), anim="stamp")


def s06(c, t):  # 59.2 - 74.9  SAC; sem TR e seguros
    title(c, t, 59.3, "Sistema SAC", y=120, size=66)
    show(c, t, 61.2, 960, 205, T("o mais comum no Brasil", 46, DGRAY), anim="up")
    # parcelas decrescentes
    for i in range(10):
        tt = 62.8 + i * 0.12
        if t > tt:
            k = grow(t, tt, 0.4)
            h = (300 - i * 22) * k
            c.save(); c.translate(560 + i * 70, 640); bar(c, h, 52, C_COL); c.restore()
    show(c, t, 63.9, 520, 300, T("começa alta", 44), anim="fade")
    show(c, t, 64.4, 1230, 540, L("...e vai caindo", 44), anim="fade")
    show(c, t, 66.0, 1580, 330, lambda c: hl(c, "ignorando:", 0, 0, 48, LGRAY), anim="up")
    show(c, t, 67.3, 1620, 430, group(at(-40, 0, M("TR", 54, DGRAY)), at(-40, 0, strike(110))), anim="pop")
    show(c, t, 68.7, 1580, 540, group(T("seguros", 52, DGRAY), strike(200)), anim="pop")
    show(c, t, 70.2, 960, 830, lambda c: hl(c, "um pouquinho a favor de quem compra", 0, 0, 52, LORANGE), anim="stamp")
    hero(c, t, 260, 1050, 0.75, [(0, "point_r"), (73.4, "finger_up")], [(0, "neutral"), (73.4, "confident")],
         appear=59.3, look=1)


def s07(c, t):  # 74.9 - 84.8  1. a parcela
    show(c, t, 74.95, 960, 125, lambda c: ribbon(c, "O CUSTO REAL DE COMPRAR", C_COL, 58), anim="stamp")
    comprador(c, t, 420, 1010, 1.1, [(0, "stand"), (79.4, "hold"), (82.8, "head")],
              [(0, "neutral"), (79.4, "worried"), (82.8, "shocked")], appear=75.0, look=1)
    show(c, t, 77.5, 1100, 330, lambda c: hl(c, "1. a parcela", 0, 0, 60, LYELLOW), anim="up")
    show(c, t, 80.1, 1100, 560, tag("R$ 2.850 / mês", YELLOW, 60), anim="pop")
    show(c, t, 80.6, 1100, 690, T("(a primeira)", 44, DGRAY), anim="fade")
    show(c, t, 83.9, 1560, 520, sc(exclaim, s=1.0), anim="stamp")


def s08(c, t):  # 84.8 - 97.0  395 mil só de juros
    title(c, t, 84.85, "Somando 30 anos de parcelas", y=120, size=58)
    a = grow(t, 87.9, 0.8)
    if t > 87.9:
        rrect(c, 620, 820 - 240 * a, 260, 240 * a, 8); fs(c, LBLUE, 6)
        text(c, "R$ 240 mil", 750, 820 - 120 * a, 46, MARKER, NAVY)
        text(c, "emprestado", 750, 870, 42, HAND)
    if t > 90.7:
        b = grow(t, 90.7, 1.0)
        rrect(c, 620, 580 - 395 * b, 260, 395 * b, 8); fs(c, RED, 6)
        text(c, "R$ 395 mil", 750, 580 - 197 * b, 46, MARKER, WHITE)
    show(c, t, 93.2, 1180, 380, lambda c: hl(c, "só de juros!", 0, 0, 66, PINKISH), anim="stamp")
    show(c, t, 94.4, 1300, 640, sc(bank, s=1.1), anim="pop")
    if t > 95.0:
        for i in range(3):
            k = grow(t, 95.0 + i * 0.25, 0.9)
            show(c, t, 95.0 + i * 0.25, 940 + 260 * k, 640 - 60 * math.sin(k * 3.1) + i * 20, sc(bill, s=0.45), anim="fade")
    show(c, t, 95.8, 1300, 830, T("e não volta", 48, RED), anim="up")
    comprador(c, t, 260, 1050, 0.75, [(0, "head")], [(0, "desperate")], appear=84.85, look=1)


def s09(c, t):  # 97.0 - 113.7  2. ITBI + cartório
    show(c, t, 97.1, 960, 125, lambda c: hl(c, "2. tirar o imóvel do papel", 0, 0, 62, LYELLOW), anim="stamp")
    show(c, t, 100.5, 560, 460, sc(document, "ITBI", RED, 44, s=1.3), anim="pop")
    show(c, t, 101.7, 560, 680, T("imposto de transmissão", 44), anim="up")
    show(c, t, 104.0, 560, 770, M("2% a 3%", 60, NAVY), anim="pop")
    show(c, t, 106.2, 960, 460, M("+", 90), anim="pop")
    show(c, t, 106.5, 1360, 460, sc(document, "CARTÓRIO", NAVY, 22, s=1.3), anim="pop")
    show(c, t, 107.2, 1360, 680, T("e registro", 44), anim="up")
    show(c, t, 108.3, 960, 770, lambda c: hl(c, "uns 4%", 0, 0, 60, LYELLOW), anim="stamp")
    show(c, t, 109.6, 960, 900, lambda c: hl(c, "R$ 12 mil à vista", 0, 0, 64, PINKISH), anim="stamp")
    show(c, t, 112.3, 1630, 880, sc(brick, s=0.8), anim="pop")
    show(c, t, 112.6, 1630, 880, sc(big_x, 70), anim="stamp")


def s10(c, t):  # 113.7 - 130.1  3. IPTU e condomínio: se cancelam
    show(c, t, 113.8, 960, 125, lambda c: hl(c, "3. IPTU e condomínio", 0, 0, 62, LYELLOW), anim="stamp")
    show(c, t, 117.2, 960, 235, lambda c: ribbon(c, "PEGADINHA", RED, 46), anim="stamp")
    comprador(c, t, 470, 1000, 0.9, [(0, "hold")], [(0, "neutral")], appear=118.1, look=1)
    show(c, t, 118.3, 470, 380, name_tag("COMPRADOR", C_COL), anim="pop")
    show(c, t, 118.9, 760, 520, group(sc(document, "IPTU", RED, 36, s=1.0), at(0, 200, sc(document, "COND.", NAVY, 34, s=1.0))), anim="pop")
    inquilino(c, t, 1450, 1000, 0.9, [(0, "hold")], [(0, "neutral")], appear=120.3, look=-1)
    show(c, t, 120.4, 1450, 380, name_tag("INQUILINO", I_COL), anim="pop")
    show(c, t, 122.3, 1160, 520, group(sc(document, "IPTU", RED, 36, s=1.0), at(0, 200, sc(document, "COND.", NAVY, 34, s=1.0))), anim="pop")
    show(c, t, 124.7, 1450, 470, T("(quase sempre)", 40, DGRAY), anim="fade")
    show(c, t, 125.7, 960, 620, sc(eq, s=1.2), anim="pop")
    show(c, t, 127.7, 960, 900, lambda c: hl(c, "se cancelam", 0, 0, 60, LGREEN), anim="stamp")
    show(c, t, 128.8, 960, 990, T("vou deixar de fora", 42, DGRAY), anim="fade")


def s11(c, t):  # 130.1 - 148.0  4. manutenção
    show(c, t, 130.15, 960, 125, lambda c: hl(c, "4. manutenção", 0, 0, 62, LYELLOW), anim="stamp")
    items = [(132.85, "vazamento", lambda c: group(sc(wrench, s=0.8))(c)),
             (133.85, "pintura", lambda c: (rrect(c, -40, -70, 80, 90, 10), fs(c, LBLUE, 5), line(c, 0, 20, 0, 90, 10, BROWN))),
             (134.7, "reforma do banheiro", lambda c: (rrect(c, -80, -40, 160, 80, 30), fs(c, WHITE, 6),
                                                         line(c, -60, -40, -60, -110, 7), line(c, -60, -110, -20, -110, 7)))]
    for i, (tt, nm, fn) in enumerate(items):
        x = 420 + i * 420
        show(c, t, tt, x, 340, lambda c, fn=fn: (c.scale(1.4, 1.4), fn(c)), anim="pop")
        show(c, t, tt + 0.2, x, 500, T(nm, 46), anim="up")
    show(c, t, 137.9, 700, 640, lambda c: hl(c, "0,5% do imóvel por ano", 0, 0, 52, LYELLOW), anim="up")
    show(c, t, 140.4, 700, 760, L("uns R$ 125/mês no começo", 50), anim="up")
    show(c, t, 143.3, 1290, 760, sc(up_arrow(RED, 90)), anim="pop")
    show(c, t, 144.5, 700, 900, L("em 30 anos:", 50, DGRAY), anim="up")
    show(c, t, 146.4, 1130, 900, lambda c: hl(c, "R$ 90 mil", 0, 0, 60, PINKISH), anim="stamp")
    hero(c, t, 1650, 1050, 0.75, [(0, "point_l"), (144.5, "present_l")], [(0, "neutral"), (144.5, "worried")],
         appear=130.2, look=-1, prop=("r", prop_calculator))


def s12(c, t):  # 148.0 - 162.6  quase 500 mil que não viram patrimônio
    title(c, t, 148.05, "Resumindo, em 30 anos:", y=120, size=60)
    parts = [(149.0, "juros", 395, RED), (149.7, "impostos", 12, ORANGE), (150.5, "manutenção", 90, BROWN)]
    y = 820
    for tt, nm, v, col in parts:
        if t > tt:
            k = grow(t, tt, 0.6)
            h = v * 1.05 * k
            rrect(c, 820, y - h, 260, h, 6); fs(c, col, 5)
            y -= v * 1.05
    for i, (tt, nm, v, col) in enumerate(parts):
        show(c, t, tt, 220, 420 + i * 110, group(lambda c, col=col: (rrect(c, -18, -18, 36, 36, 6), fs(c, col, 4)),
                                                 at(40, 0, L(f"{nm}: R$ {v} mil", 48))), anim="left")
    show(c, t, 153.3, 1440, 330, lambda c: hl(c, "quase R$ 500 mil", 0, 0, 62, PINKISH), anim="stamp")
    show(c, t, 156.2, 1440, 430, T("que não viram patrimônio", 46, DGRAY), anim="up")
    show(c, t, 158.6, 960, 930, lambda c: hl(c, "comprar também tem 'dinheiro jogado fora'", 0, 0, 54, LYELLOW), anim="up")
    show(c, t, 161.5, 1440, 640, lambda c: ribbon(c, "SÓ MUDA O NOME", NAVY, 50), anim="stamp")
    hero(c, t, 1700, 1050, 0.7, [(0, "present_l"), (158.6, "shrug")], [(0, "neutral"), (158.6, "confident")],
         appear=148.05, look=-1)


# ======================================================================= BLOCO 2
def s13(c, t):  # 163.6 - 175.2  o outro lado: alugar
    show(c, t, 163.65, 960, 125, lambda c: ribbon(c, "O OUTRO LADO: ALUGAR", I_COL, 60), anim="stamp")
    show(c, t, 166.8, 760, 920, sc(apartment, LBLUE, "ALUGA-SE", s=1.2), anim="drop")
    show(c, t, 168.5, 1560, 380, sc(qmark, 120, I_COL), anim="pop")
    inquilino(c, t, 1560, 1010, 1.0, [(0, "think"), (170.0, "point_l")], [(0, "think"), (170.0, "neutral")],
              appear=165.7, look=-1)
    show(c, t, 170.0, 1180, 360, lambda c: hl(c, "índice FipeZap", 0, 0, 54, LYELLOW), anim="up")
    show(c, t, 172.5, 1180, 450, T("aluguel do ano / preço do imóvel", 42, DGRAY), anim="fade")


def s14(c, t):  # 175.2 - 186.4  6% ao ano = R$ 1.500
    title(c, t, 175.25, "Rentabilidade do aluguel (jul/2026)", y=120, size=56)
    show(c, t, 178.95, 700, 380, lambda c: text(c, "6% ao ano", 0, 0, 110, MARKER, I_COL), anim="stamp")
    show(c, t, 180.65, 700, 520, T("= 0,5% por mês", 56), anim="up")
    show(c, t, 182.4, 520, 820, sc(apartment, s=0.7), anim="pop")
    show(c, t, 182.95, 520, 500, tag("R$ 300 mil"), anim="pop", t1=999)
    arrow_draw(c, t, 184.0, 700, 760, 960, 760)
    show(c, t, 184.8, 1260, 760, lambda c: hl(c, "R$ 1.500 / mês", 0, 0, 68, LPURPLE), anim="stamp")
    hero(c, t, 1680, 1050, 0.72, [(0, "point_l")], [(0, "happy")], appear=175.3, look=-1, prop=("r", prop_pointer))


def s15(c, t):  # 186.4 - 205.7  o aluguel sobe
    title(c, t, 186.45, "E o aluguel sobe", y=120, size=64)
    show(c, t, 187.6, 960, 205, T("ultimamente, acima da inflação", 44, DGRAY), anim="up", t1=192.5)
    show(c, t, 193.0, 960, 205, T("no longo prazo: junto com o imóvel e a inflação", 44, DGRAY), anim="up")
    show(c, t, 197.6, 1600, 500, lambda c: hl(c, "+4,5% ao ano", 0, 0, 56, LYELLOW), anim="stamp")
    # curva 1.500 -> 5.400 em 30 anos
    x0, x1, yb = 420, 1380, 860
    line(c, x0, yb, x1 + 40, yb, 5); line(c, x0, yb, x0, 360, 5)
    show(c, t, 192.0, x0, yb + 40, T("hoje", 40), anim="fade")
    show(c, t, 199.5, x1, yb + 40, T("ano 30", 40), anim="fade")
    if t > 194.0:
        k = grow(t, 194.0, 9.0)
        n = int(60 * k) + 1
        c.move_to(x0, yb - 1500 * 0.09)
        for i in range(n):
            u = i / 60
            c.line_to(x0 + (x1 - x0) * u, yb - 1500 * 1.045 ** (30 * u) * 0.09)
        rgb(c, I_COL); c.set_line_width(9); c.stroke()
    show(c, t, 194.0, x0 + 140, yb - 1500 * 0.09 - 50, M("R$ 1.500", 44, I_COL), anim="pop")
    show(c, t, 203.4, x1 - 40, yb - 5400 * 0.09 - 60, lambda c: hl(c, "R$ 5.400", 0, 0, 54, LPURPLE), anim="stamp")
    inquilino(c, t, 1640, 1050, 0.7, [(0, "stand"), (203.4, "head")], [(0, "neutral"), (203.4, "worried")],
              appear=186.5, look=-1)


def s16(c, t):  # 205.7 - 214.3  mais de 1 milhão de aluguel
    title(c, t, 205.75, "Somando 30 anos de aluguel:", y=120, size=60)
    show(c, t, 207.6, 960, 340, lambda c: text(c, "+ de R$ 1 milhão", 0, 0, 120, MARKER, RED), anim="stamp")
    tio(c, t, 560, 1010, 1.0, [(0, "stand"), (211.6, "point_r")], [(0, "neutral"), (211.6, "grin")], appear=211.4, look=1)
    show(c, t, 211.8, 900, 560, lambda c: speech(c, 420, 140, -160, 90), anim="pop")
    show(c, t, 212.0, 900, 555, T("Eu não disse?", 52), anim="fade")
    hero(c, t, 1450, 1010, 1.0, [(0, "stand"), (213.6, "finger_up")], [(0, "neutral"), (213.6, "confident")],
         appear=205.8, look=-1)
    show(c, t, 213.7, 1450, 470, lambda c: hl(c, "Calma.", 0, 0, 64, LYELLOW), anim="stamp")


def s17(c, t):  # 214.3 - 229.5  a vantagem escondida: 72 mil no bolso
    title(c, t, 214.35, "A vantagem que ninguém põe na conta", y=120, size=56)
    inquilino(c, t, 360, 1010, 1.05, [(0, "stand"), (224.5, "arms_up"), (228.2, "think")],
              [(0, "neutral"), (224.5, "grin"), (228.2, "think")], appear=214.4, look=1)
    show(c, t, 219.5, 1050, 360, group(L("não deu", 52, DGRAY), at(220, 0, L("R$ 60 mil de entrada", 56))), anim="left")
    show(c, t, 221.8, 1050, 480, group(L("nem pagou", 52, DGRAY), at(250, 0, L("R$ 12 mil de ITBI", 56))), anim="left")
    show(c, t, 224.5, 1250, 650, lambda c: hl(c, "R$ 72 mil no bolso", 0, 0, 68, LGREEN), anim="stamp")
    show(c, t, 226.6, 820, 650, sc(piggy, s=0.7), anim="pop")
    show(c, t, 228.3, 1250, 850, lambda c: hl(c, "E se ele investir?", 0, 0, 58, LYELLOW), anim="up")


def s18(c, t):  # 229.5 - 241.9  rendimento de 10% a.a. líquido
    title(c, t, 229.55, "Rendimento do investimento", y=120, size=60)
    show(c, t, 231.4, 960, 330, lambda c: text(c, "10% ao ano", 0, 0, 110, MARKER, GREEN), anim="stamp")
    show(c, t, 232.9, 960, 450, T("já descontado o imposto", 50, DGRAY), anim="up")
    show(c, t, 234.6, 700, 640, L("CDI hoje:", 52, DGRAY), anim="up")
    show(c, t, 236.1, 1000, 640, M("~13,6%", 62, NAVY), anim="pop")
    show(c, t, 239.8, 960, 830, lambda c: hl(c, "pé no chão pra 30 anos", 0, 0, 56, LGREEN), anim="stamp")
    hero(c, t, 1650, 1050, 0.75, [(0, "point_l"), (239.8, "thumb")], [(0, "happy"), (239.8, "confident")],
         appear=229.6, look=-1, prop=("r", prop_tablet))


def s19(c, t):  # 241.9 - 255.7  a corrida e a regra
    show(c, t, 241.95, 960, 125, lambda c: ribbon(c, "A CORRIDA: 30 ANOS", NAVY, 62), anim="stamp")
    comprador(c, t, 420, 1010, 1.05, [(0, "run"), (247.0, "hips")], [(0, "confident")], appear=244.4, look=1)
    show(c, t, 244.5, 420, 330, name_tag("COMPRADOR", C_COL), anim="pop")
    inquilino(c, t, 1500, 1010, 1.05, [(0, "run"), (247.0, "hips")], [(0, "confident")], appear=246.4, look=-1)
    show(c, t, 246.5, 1500, 330, name_tag("INQUILINO", I_COL), anim="pop")
    show(c, t, 247.3, 960, 330, lambda c: hl(c, "regra justa", 0, 0, 52, LYELLOW), anim="up")
    show(c, t, 248.8, 960, 460, T("mesma renda", 50), anim="up")
    show(c, t, 250.4, 960, 550, T("mesmo valor pra moradia", 50), anim="up")
    show(c, t, 252.7, 960, 720, T("quem gastar menos no mês...", 50, DGRAY), anim="up")
    show(c, t, 254.8, 960, 820, lambda c: hl(c, "investe a diferença", 0, 0, 58, LGREEN), anim="stamp")


def s20(c, t):  # 255.7 - 269.4  começo: 2.850 x 1.500
    title(c, t, 255.75, "No começo:", y=120, size=64)
    comprador(c, t, 300, 1010, 0.95, [(0, "hold")], [(0, "worried")], appear=255.8, look=1)
    show(c, t, 257.6, 640, 360, tag("R$ 2.850", LORANGE, 56), anim="pop")
    show(c, t, 260.3, 640, 480, T("+ manutenção", 46), anim="up")
    inquilino(c, t, 1620, 1010, 0.95, [(0, "hold"), (264.2, "point_l")], [(0, "happy")], appear=261.5, look=-1)
    show(c, t, 262.6, 1280, 360, tag("R$ 1.500", LPURPLE, 56), anim="pop")
    show(c, t, 264.2, 960, 620, lambda c: hl(c, "diferença: ~R$ 1.480/mês", 0, 0, 58, LGREEN), anim="stamp")
    arrow_draw(c, t, 267.4, 1120, 700, 1300, 800)
    show(c, t, 267.6, 1400, 840, sc(piggy, I_COL, s=0.7), anim="pop")
    show(c, t, 268.0, 960, 840, T("vai pro investimento do Inquilino", 44), anim="up")


def s21(c, t):  # 269.4 - 292.9  placar: anos 1, 5, 10
    year_badge(c, t, [(269.45, 1), (280.8, 5), (286.8, 10)], y=130)
    kc = [(270.2, 0), (275.0, 81), (280.8, 81), (282.7, 174), (286.8, 174), (288.5, 306)]
    ki = [(270.2, 0), (276.2, 0), (277.2, 97), (280.8, 97), (285.2, 208), (286.8, 208), (290.95, 370)]
    race_bars(c, t, 270.2, kc, ki, vmax=400, hmax=520, base=900)
    show(c, t, 272.2, 460, 330, T("apartamento", 44), anim="fade")
    show(c, t, 272.6, 460, 390, T("- dívida no banco", 44, RED), anim="fade")
    show(c, t, 279.4, 1560, 330, lambda c: hl(c, "Inquilino na frente", 0, 0, 46, LPURPLE), anim="stamp")
    comprador(c, t, 300, 1050, 0.6, [(0, "stand"), (279.4, "shrug")], [(0, "neutral"), (279.4, "worried")], appear=270.2, look=1)
    inquilino(c, t, 1640, 1050, 0.6, [(0, "stand"), (279.4, "arms_up")], [(0, "neutral"), (279.4, "grin")], appear=270.2, look=-1)


def s22(c, t):  # 292.9 - 309.2  a virada do ano 11
    title(c, t, 292.95, "O que muita gente esquece", y=120, size=60)
    show(c, t, 296.3, 960, 220, lambda c: hl(c, "lá pelo ano 11", 0, 0, 56, LYELLOW), anim="stamp")
    show(c, t, 297.5, 560, 400, group(tag("parcela", LORANGE, 50), at(0, 120, sc(down_arrow(GREEN, 110)))), anim="pop")
    show(c, t, 299.5, 1360, 400, group(tag("aluguel", LPURPLE, 50), at(0, 120, sc(up_arrow(RED, 110)))), anim="pop")
    show(c, t, 301.9, 960, 450, sc(lambda c: arrow(c, -90, 0, 90, 0, INK, 9, 0.4)), anim="pop")
    show(c, t, 301.95, 960, 360, T("inverte!", 48, RED), anim="up")
    show(c, t, 303.0, 960, 700, lambda c: hl(c, "agora o Comprador gasta menos", 0, 0, 56, LORANGE), anim="up")
    comprador(c, t, 360, 1050, 0.8, [(0, "stand"), (305.0, "arms_up")], [(0, "neutral"), (305.0, "grin")], appear=303.0, look=1)
    arrow_draw(c, t, 307.0, 560, 880, 820, 900)
    show(c, t, 307.2, 960, 900, sc(piggy, C_COL, s=0.7), anim="pop")
    show(c, t, 308.0, 1380, 900, T("investimento dele", 46), anim="up")


def s23(c, t):  # 309.2 - 329.9  ano 20 e chegada (comprador)
    year_badge(c, t, [(309.2, 20), (317.5, 30)], y=130)
    kc = [(309.3, 306), (311.0, 786), (321.2, 786), (321.3, 1124), (323.8, 1124), (324.6, 2063)]
    ki = [(309.3, 370), (313.9, 370), (314.4, 960)]
    race_bars(c, t, 309.3, kc, ki, vmax=2500, hmax=560, base=930)
    if t > 315.95:
        show(c, t, 315.95, 1180, 230, sc(finish_flag, 140, s=0.7), anim="drop")
    show(c, t, 319.3, 360, 420, group(sc(house_key, s=0.8), at(0, 90, T("quitado", 44))), anim="pop")
    show(c, t, 321.2, 360, 580, T("imóvel R$ 1,12 mi", 44, C_COL), anim="up")
    show(c, t, 323.8, 360, 650, T("+ R$ 940 mil investidos", 44, GREEN), anim="up")
    if t > 327.1:
        sfx_hl = lambda c: hl(c, "total: R$ 2,06 mi", 0, 0, 50, LORANGE)
        show(c, t, 327.1, 360, 760, sfx_hl, anim="stamp")
    comprador(c, t, 1620, 1060, 0.6, [(0, "stand"), (319.3, "arms_up")], [(0, "neutral"), (319.3, "grin")], appear=309.3, look=-1)


def s24(c, t):  # 329.9 - 336.7  inquilino 2,49 mi
    year_badge(c, t, [(329.9, 30)], y=130)
    kc = [(329.9, 2063)]
    ki = [(329.9, 960), (331.2, 960), (332.6, 2489)]
    race_bars(c, t, 329.9, kc, ki, vmax=2500, hmax=560, base=930)
    show(c, t, 329.9, 1180, 230, sc(finish_flag, 140, s=0.7), anim="fade")
    show(c, t, 334.1, 1560, 420, lambda c: hl(c, "+ R$ 425 mil", 0, 0, 60, LGREEN), anim="stamp")
    inquilino(c, t, 1560, 1060, 0.6, [(0, "stand"), (332.6, "arms_up")], [(0, "neutral"), (332.6, "grin")], appear=329.95, look=-1)
    comprador(c, t, 360, 1060, 0.55, [(0, "stand"), (334.1, "shrug")], [(0, "happy"), (334.1, "worried")], look=1)


def s25(c, t):  # 336.7 - 350.4  em dinheiro de hoje
    title(c, t, 336.75, "Um detalhe honesto", y=120, size=64)
    show(c, t, 338.3, 960, 220, T("esses são valores do futuro", 48, DGRAY), anim="up")
    show(c, t, 340.3, 960, 330, group(sc(cart, s=0.6), at(160, 0, L("descontando a inflação", 46))), anim="pop")
    show(c, t, 341.6, 960, 450, lambda c: hl(c, "em dinheiro de hoje", 0, 0, 52, LYELLOW), anim="up")
    kc = [(343.8, 0), (344.3, 550)]
    ki = [(343.8, 0), (345.7, 0), (346.2, 665)]
    race_bars(c, t, 343.8, kc, ki, vmax=700, hmax=300, base=930)
    show(c, t, 347.9, 1570, 700, T("a vantagem continua", 44, I_COL), anim="up")
    hero(c, t, 300, 1050, 0.75, [(0, "present"), (347.9, "finger_up")], [(0, "neutral"), (347.9, "confident")],
         appear=336.8, look=1)


# ======================================================================= BLOCO 3
def s26(c, t):  # 350.4 - 360.0  depende de três números
    title(c, t, 350.45, "Então alugar é melhor?", y=120, size=64)
    show(c, t, 352.7, 960, 220, lambda c: hl(c, "não necessariamente", 0, 0, 54, PINKISH), anim="stamp")
    show(c, t, 355.5, 1300, 380, lambda c: hl(c, "depende de 3 números", 0, 0, 52, LYELLOW), anim="up")
    tilt = lerp_keys(t, [(356.6, -0.6), (358.4, 0.7), (359.2, -0.3), (360.0, 0.5)])
    show(c, t, 356.7, 1150, 730, sc(lambda c: balance(c, tilt, lambda c: sc(house_key, s=0.45)(c),
                                                     lambda c: sc(bills, 2, s=0.45)(c)), s=0.95), anim="pop")
    hero(c, t, 340, 1010, 1.05, [(0, "shrug"), (354.2, "finger_up")], [(0, "think"), (354.2, "confident")],
         appear=350.5, look=1)


def s27(c, t):  # 360.0 - 369.6  1. juro do financiamento
    number_head(c, t, 360.05, 1, "juro do financiamento")
    ruler(c, t, 361.1, 7, 13, 11.5, 9.9, "Comprador vence", "Inquilino vence", LORANGE, LPURPLE,
          t_thr=365.9, t_left=367.9, t_right=366.6, val_lbl="11,5% (nossa conta)")
    show(c, t, 366.3, 960, 880, lambda c: hl(c, "abaixo de ~10% a.a., o Comprador passa", 0, 0, 52, LORANGE), anim="up")
    hero(c, t, 1720, 1060, 0.55, [(0, "point_l")], [(0, "neutral")], appear=360.1, look=-1)


def s28(c, t):  # 369.6 - 387.9  2. aluguel / valor do imóvel
    number_head(c, t, 369.65, 2, "aluguel / valor do imóvel")
    ruler(c, t, 370.8, 3, 9, 6, 6.5, "Inquilino vence", "Comprador vence", LPURPLE, LORANGE,
          t_thr=376.8, t_left=381.3, t_right=379.6, val_lbl="6% a.a. (nossa conta)")
    show(c, t, 379.6, 1390, 880, lambda c: hl(c, "acima de 6,5%: comprar ganha", 0, 0, 48, LORANGE), anim="up")
    show(c, t, 382.3, 560, 880, lambda c: hl(c, "4% a 5%: alugar com folga", 0, 0, 48, LPURPLE), anim="up")
    show(c, t, 383.9, 560, 970, T("(muitos bairros caros)", 40, DGRAY), anim="fade")


def s29(c, t):  # 387.9 - 398.9  3. rendimento do investimento
    number_head(c, t, 387.9, 3, "rendimento do investimento")
    ruler(c, t, 388.8, 7, 13, 10, 9.2, "Comprador vence", "Inquilino vence", LORANGE, LPURPLE,
          t_thr=393.3, t_left=395.2, t_right=396.5, val_lbl="10% líquido (nossa conta)")
    hero(c, t, 1720, 1060, 0.55, [(0, "point_l")], [(0, "neutral")], appear=388.0, look=-1, prop=("r", prop_tablet))


def s30(c, t):  # 398.9 - 409.3  4. (escondido) valorização do imóvel
    number_head(c, t, 398.95, 4, "o escondido: valorização", col=LGRAY)
    ruler(c, t, 401.1, 2, 8, 4.5, 5.0, "Inquilino vence", "Comprador vence", LPURPLE, LORANGE,
          t_thr=405.3, t_left=405.8, t_right=407.5, val_lbl="4,5% = inflação")
    show(c, t, 401.2, 1640, 320, sc(apartment, s=0.45), anim="pop")
    show(c, t, 404.4, 960, 880, lambda c: hl(c, "acima de ~5% a.a., a balança vai pro Comprador", 0, 0, 50, LORANGE), anim="up")


def s31(c, t):  # 409.3 - 426.5  Minha Casa Minha Vida, faixa 3
    show(c, t, 409.35, 960, 125, lambda c: ribbon(c, "MINHA CASA MINHA VIDA", GREEN, 60), anim="stamp")
    show(c, t, 412.6, 960, 225, T("regras desde abril de 2026", 44, DGRAY), anim="up")
    show(c, t, 414.4, 700, 360, lambda c: hl(c, "faixa 3", 0, 0, 62, LYELLOW), anim="pop")
    show(c, t, 416.3, 700, 490, L("renda até R$ 9.600", 52), anim="left")
    show(c, t, 419.0, 700, 590, L("imóvel até R$ 400 mil", 52), anim="left")
    show(c, t, 422.3, 1220, 590, sc(check_icon, 40), anim="stamp")
    show(c, t, 421.4, 1500, 560, sc(apartment, s=0.6), anim="pop")
    show(c, t, 422.9, 700, 760, L("juro: até ~7,7% ao ano", 56, GREEN), anim="left")
    show(c, t, 424.3, 1380, 770, sc(down_arrow(GREEN, 100)), anim="pop")
    hero(c, t, 280, 1050, 0.7, [(0, "present"), (422.3, "thumb")], [(0, "happy"), (422.3, "grin")], appear=409.4, look=1)


def s32(c, t):  # 426.5 - 439.5  o porém: só 65% financiados no Sul/Sudeste
    show(c, t, 426.55, 960, 125, lambda c: hl(c, "O porém", 0, 0, 64, PINKISH), anim="stamp")
    show(c, t, 427.4, 960, 250, T("no Sul e no Sudeste", 50, DGRAY), anim="up")
    show(c, t, 429.3, 640, 450, sc(donut, 0.65, 160, 60, GREEN), anim="pop")
    show(c, t, 430.3, 640, 450, M("65%", 70, GREEN), anim="pop")
    show(c, t, 430.6, 640, 680, T("financiado", 46), anim="up")
    show(c, t, 432.0, 1300, 400, L("entrada:", 50, DGRAY), anim="up")
    show(c, t, 433.3, 1300, 490, lambda c: hl(c, "R$ 105 mil", 0, 0, 62, LORANGE), anim="stamp")
    inquilino(c, t, 1640, 1050, 0.7, [(0, "stand"), (436.5, "arms_up")], [(0, "neutral"), (436.5, "grin")], appear=434.5, look=-1)
    show(c, t, 436.6, 1150, 780, L("Inquilino começa com", 48, DGRAY), anim="up")
    show(c, t, 437.2, 1250, 880, lambda c: hl(c, "R$ 117 mil investidos", 0, 0, 56, LPURPLE), anim="stamp")


def s33(c, t):  # 439.5 - 458.7  a corrida refeita: o resultado vira
    title(c, t, 439.55, "Refazendo a corrida (MCMV)", y=120, size=60)
    show(c, t, 442.4, 960, 220, group(L("1ª parcela:", 48, DGRAY), at(250, 0, L("R$ 1.750", 56, C_COL))), anim="up")
    show(c, t, 444.3, 960, 300, T("o Comprador passa na frente já no 3º ano", 46), anim="up")
    kc = [(447.4, 0), (449.1, 2679)]
    ki = [(447.4, 0), (451.8, 0), (452.3, 2186)]
    race_bars(c, t, 447.4, kc, ki, vmax=2800, hmax=480, base=930)
    show(c, t, 447.45, 1560, 1000, sc(finish_flag, 140, s=0.7), anim="drop")
    show(c, t, 454.9, 1600, 460, lambda c: hl(c, "mudou 1 número:", 0, 0, 44, LYELLOW), anim="up")
    show(c, t, 456.2, 1600, 560, lambda c: hl(c, "o juro", 0, 0, 52, LYELLOW), anim="stamp")
    show(c, t, 457.5, 1600, 680, T("virou do avesso", 46, RED), anim="up")
    comprador(c, t, 330, 1060, 0.6, [(0, "stand"), (449.1, "arms_up")], [(0, "neutral"), (449.1, "grin")], appear=439.6, look=1)


def s34(c, t):  # 458.7 - 470.5  o que a planilha não mostra: segurança
    show(c, t, 458.75, 960, 125, lambda c: ribbon(c, "O QUE A PLANILHA NÃO MOSTRA", NAVY, 56), anim="stamp")
    show(c, t, 461.3, 960, 250, lambda c: hl(c, "1. segurança", 0, 0, 58, LYELLOW), anim="up")
    show(c, t, 462.9, 560, 600, sc(house, True, s=1.4), anim="pop")
    show(c, t, 463.4, 900, 640, sc(house_key, s=0.8), anim="pop")
    show(c, t, 465.0, 1250, 470, group(sc(calendar, "30", RED, s=0.7), at(160, 0, L("dias pra sair", 46))), anim="pop")
    show(c, t, 465.4, 1360, 470, sc(big_x, 90), anim="stamp")
    other(c, t, 1200, 1030, 0.65, [(0, "stand")], [(0, "happy")], appear=467.6, look=-1, shirt=YELLOW, fid=6)
    show(c, t, 467.8, 1200, 610, T("filho na escola do bairro", 44), anim="up")
    hero(c, t, 1720, 1050, 0.65, [(0, "stand"), (469.1, "thumb")], [(0, "neutral"), (469.1, "happy")], appear=458.8, look=-1)


def s35(c, t):  # 470.5 - 479.6  liberdade
    show(c, t, 470.55, 960, 125, lambda c: hl(c, "2. liberdade", 0, 0, 60, LYELLOW), anim="stamp")
    inquilino(c, t, lerp_keys(t, [(472.2, 460), (476.0, 1100)]), 1010, 0.95,
              [(0, "stand"), (472.2, "run"), (476.0, "wave")], [(0, "happy"), (472.2, "grin")], appear=471.3, look=1)
    show(c, t, 472.3, 640, 640, sc(moving_box, s=0.7), anim="pop", t1=475.5)
    show(c, t, 473.5, 1500, 760, sc(apartment, LBLUE, s=0.7), anim="pop")
    show(c, t, 474.0, 1500, 300, T("emprego melhor em outra cidade", 44), anim="up")
    show(c, t, 476.7, 700, 330, lambda c: hl(c, "vender imóvel: demora e custa", 0, 0, 46, PINKISH), anim="up")
    show(c, t, 478.1, 520, 470, sc(clock, t, s=0.7), anim="pop")
    show(c, t, 478.6, 760, 470, sc(bills, 2, s=0.6), anim="pop")


def s36(c, t):  # 479.6 - 487.1  valorização é aposta
    show(c, t, 479.65, 960, 125, lambda c: hl(c, "3. valorização é aposta", 0, 0, 60, LYELLOW), anim="stamp")
    x0, yb = 520, 800
    line(c, x0, yb, 1500, yb, 5); line(c, x0, yb, x0, 320, 5)
    if t > 482.4:
        k = grow(t, 482.4, 1.6)
        c.move_to(x0, yb - 120)
        for i in range(int(40 * k) + 1):
            u = i / 40
            c.line_to(x0 + 900 * u, yb - 120 - 300 * u ** 1.4)
        rgb(c, GREEN); c.set_line_width(8); c.stroke()
    show(c, t, 483.3, 1500, 360, T("sobe mais que a inflação?", 44, GREEN), anim="up")
    if t > 484.9:
        k = grow(t, 484.9, 1.4)
        c.save(); c.set_dash([16, 12])
        line(c, x0, yb - 120, x0 + 900 * k, yb - 130, 8, RED); c.restore()
    show(c, t, 485.0, 1500, 690, T("ou parado por 10 anos?", 44, RED), anim="up")
    show(c, t, 481.7, 1680, 520, sc(qmark, 140, NAVY), anim="pop")
    hero(c, t, 300, 1050, 0.7, [(0, "think")], [(0, "think")], appear=479.7, look=1)


def s37(c, t):  # 487.1 - 501.2  4. o mais importante: investir a diferença
    show(c, t, 487.1, 960, 125, lambda c: ribbon(c, "4. O MAIS IMPORTANTE", RED, 58), anim="stamp")
    show(c, t, 489.4, 960, 250, T("a vantagem do Inquilino só existe se ele investir", 48), anim="up")
    show(c, t, 492.3, 960, 350, lambda c: hl(c, "a diferença", 0, 0, 56, LGREEN), anim="stamp")
    show(c, t, 493.4, 700, 480, group(sc(calendar, "1", NAVY, s=0.6), at(110, 0, L("todo mês", 48))), anim="pop")
    show(c, t, 494.2, 1150, 480, group(sc(calendar, "30", NAVY, s=0.6), at(110, 0, L("por 30 anos", 48))), anim="pop")
    show(c, t, 496.4, 960, 620, lambda c: hl(c, "a maioria não faz", 0, 0, 56, PINKISH), anim="up")
    show(c, t, 498.8, 560, 840, sc(car, ORANGE, s=0.7), anim="pop")
    show(c, t, 499.5, 960, 840, sc(document, "VIAGEM", BLUE, 24, s=1.1), anim="pop")
    show(c, t, 500.5, 1340, 840, lambda c: (rrect(c, -90, -60, 180, 120, 14), fs(c, RED, 6),
                                            text(c, "DELIVERY", 0, 0, 30, MARKER, WHITE)), anim="pop")
    inquilino(c, t, 1700, 1050, 0.6, [(0, "stand"), (498.8, "shrug")], [(0, "neutral"), (498.8, "worried")], appear=487.2, look=-1)


def s38(c, t):  # 501.2 - 520.0  quando o inquilino gasta a diferença
    title(c, t, 501.2, "Se o Inquilino gastar a diferença...", y=120, size=58)
    show(c, t, 502.9, 960, 210, T("e só deixar a entrada rendendo", 46, DGRAY), anim="up")
    kc = [(503.0, 0), (503.6, 1124)]
    ki = [(503.0, 0), (504.0, 1256)]
    if t < 506.9:
        race_bars(c, t, 503.0, kc, ki, vmax=1400, hmax=420, base=830)
        show(c, t, 505.4, 960, 330, lambda c: hl(c, "praticamente empatam", 0, 0, 50, LYELLOW), anim="stamp")
    else:
        race_bars(c, t, 503.0, [(0, 1124)], [(506.9, 1256), (509.6, 0)], vmax=1400, hmax=420, base=830)
        show(c, t, 507.0, 960, 300, T("se gastar até a entrada...", 46, DGRAY), anim="up")
        show(c, t, 509.9, 1160, 760, lambda c: text(c, "ZERO", 0, 0, 80, MARKER, RED), anim="stamp")
        show(c, t, 514.5, 1500, 450, lambda c: hl(c, "poupança forçada", 0, 0, 52, LORANGE), anim="stamp")
        show(c, t, 518.6, 1500, 550, T("e isso tem valor", 44), anim="up")
    hero(c, t, 280, 1050, 0.65, [(0, "present"), (514.5, "finger_up")], [(0, "neutral"), (514.5, "confident")],
         appear=501.3, look=1)


def checklist(c, t, items, x=620, y0=340, dy=130, col=GREEN):
    for i, (tt, s) in enumerate(items):
        show(c, t, tt, x, y0 + i * dy, group(sc(check_icon, 36), at(60, 0, L(s, 52))), anim="left")


def s39(c, t):  # 520.0 - 536.6  quando comprar faz sentido
    show(c, t, 520.0, 960, 125, lambda c: ribbon(c, "QUANDO COMPRAR FAZ SENTIDO", C_COL, 56), anim="stamp")
    checklist(c, t, [(522.7, "vai ficar muitos anos no mesmo lugar"), (525.6, "consegue juro baixo (ex.: MCMV)"),
                     (528.8, "aluguel caro perto do preço do imóvel"), (532.5, "sabe que não investiria todo mês")])
    comprador(c, t, 330, 1050, 0.65, [(0, "stand"), (522.7, "thumb")], [(0, "happy")], appear=520.05, look=1)
    show(c, t, 520.2, 330, 520, sc(house_key, s=0.6), anim="pop")


def s40(c, t):  # 536.6 - 550.9  quando alugar faz sentido
    show(c, t, 536.65, 960, 125, lambda c: ribbon(c, "QUANDO ALUGAR FAZ SENTIDO", I_COL, 56), anim="stamp")
    checklist(c, t, [(538.8, "juro do financiamento alto"), (541.2, "aluguel barato perto do preço"),
                     (544.0, "você valoriza mobilidade"), (546.5, "investe a diferença todo santo mês")])
    show(c, t, 547.9, 1350, 860, lambda c: hl(c, "principalmente!", 0, 0, 48, LGREEN), anim="stamp")
    inquilino(c, t, 330, 1050, 0.65, [(0, "stand"), (538.8, "thumb")], [(0, "happy")], appear=536.7, look=1)
    show(c, t, 536.8, 330, 520, sc(moving_box, s=0.5), anim="pop")


def s41(c, t):  # 550.9 - 565.2  os dois são o preço de morar
    show(c, t, 551.0, 960, 250, T("Aluguel é dinheiro jogado fora", 62), anim="fade")
    if t > 552.4:
        k = grow(t, 552.4, 0.5)
        line(c, 960 - 430, 256, 960 - 430 + 860 * k, 244, 10, RED)
    show(c, t, 553.8, 960, 360, T("Juros também não.", 56), anim="up")
    show(c, t, 555.3, 960, 520, lambda c: hl(c, "os dois são o preço de morar", 0, 0, 64, LYELLOW), anim="stamp")
    show(c, t, 557.7, 960, 680, T("a pergunta certa:", 50, DGRAY), anim="up")
    show(c, t, 560.9, 960, 800, lambda c: hl(c, "qual te deixa com mais dinheiro", 0, 0, 58, LGREEN), anim="up")
    show(c, t, 563.7, 960, 910, lambda c: hl(c, "com os SEUS números?", 0, 0, 58, LGREEN), anim="stamp")
    comprador(c, t, 260, 1060, 0.55, [(0, "stand")], [(0, "happy")], appear=551.0, look=1)
    inquilino(c, t, 1660, 1060, 0.55, [(0, "stand")], [(0, "happy")], appear=551.0, look=-1)


def s42(c, t):  # 565.2 - 577.0  CTA: vídeo dos 100 mil
    title(c, t, 565.25, "Quer ver o poder de investir todo mês?", y=120, size=56)
    show(c, t, 570.0, 1050, 520, lambda c: video_card(c, "Os primeiros R$ 100 mil", "assista agora",
                                                        icon=lambda c: play_btn(c, 70)), anim="pop")
    show(c, t, 574.3, 1050, 850, T("tá aparecendo aqui na tela", 46, DGRAY), anim="up")
    hero(c, t, 300, 1010, 1.0, [(0, "present"), (570.0, "point_r"), (576.1, "wave")],
         [(0, "happy"), (576.1, "grin")], appear=565.3, look=1)


def s43(c, t):  # 577.0 - fim (15 s)  Tela final do YouTube: sem narração, áreas livres
    # Áreas livres: vídeo à esquerda (x 170-950, y 300-740), inscrever-se à direita (~1450, 520).
    show(c, t, 577.1, 960, 130, lambda c: text(c, "FAZ A CONTA", 0, 0, 84, MARKER, NAVY), anim="fade")
    show(c, t, 577.4, 560, 800, T("assista também", 46, DGRAY), anim="fade")
    show(c, t, 577.4, 1450, 800, T("inscreva-se", 46, DGRAY), anim="fade")
    hero(c, t, 960, 1060, 0.62, [(0, "wave"), (579.5, "relax")], [(0, "happy")], appear=577.1)


SCENES = [
    (0.0, 13.2, s01), (13.2, 25.2, s02), (25.2, 33.1, s03), (33.1, 44.9, s04), (44.9, 59.2, s05),
    (59.2, 74.9, s06), (74.9, 84.8, s07), (84.8, 97.0, s08), (97.0, 113.7, s09), (113.7, 130.1, s10),
    (130.1, 148.0, s11), (148.0, 163.59, s12),
    (163.59, 175.2, s13), (175.2, 186.4, s14), (186.4, 205.7, s15), (205.7, 214.3, s16), (214.3, 229.5, s17),
    (229.5, 241.9, s18), (241.9, 255.7, s19), (255.7, 269.4, s20), (269.4, 292.9, s21), (292.9, 309.2, s22),
    (309.2, 329.9, s23), (329.9, 336.7, s24), (336.7, 350.42, s25),
    (350.42, 360.0, s26), (360.0, 369.6, s27), (369.6, 387.9, s28), (387.9, 398.9, s29), (398.9, 409.3, s30),
    (409.3, 426.5, s31), (426.5, 439.5, s32), (439.5, 458.7, s33), (458.7, 470.5, s34), (470.5, 479.6, s35),
    (479.6, 487.1, s36), (487.1, 501.2, s37), (501.2, 520.0, s38), (520.0, 536.6, s39), (536.6, 550.9, s40),
    (550.9, 565.2, s41), (565.2, 577.0, s42), (577.0, 999.0, s43),
]

# só toques pontuais, sem ruído: R$ 395 mil de juros / +425 mil do inquilino / MCMV vira / os dois são o preço de morar
SFX = [(93.2, "tum"), (334.1, "tum"), (449.1, "tum"), (555.3, "soft_ding")]
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key")
