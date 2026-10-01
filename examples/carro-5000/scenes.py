from engine import *  # noqa


def hero(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", YELLOW)
    kw.setdefault("hair", "tuft")
    kw.setdefault("fid", 0)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def other(c, t, x, y, s, poses, exprs, **kw):
    kw.setdefault("shirt", BLUE)
    kw.setdefault("hair", "spiky")
    kw.setdefault("fid", 1)
    figure(c, t, x, y, s, poses=poses, exprs=exprs, **kw)


def title(c, t, t0, s, y=120, size=64, col=INK, bg=None, anim="up"):
    if bg:
        show(c, t, t0, 960, y, lambda c: hl(c, s, 0, 0, size, bg, col), anim=anim)
    else:
        show(c, t, t0, 960, y, lambda c: text(c, s, 0, 0, size, MARKER, col), anim=anim)


def T(s, size=48, col=INK, font=HAND):
    return lambda c: text(c, s, 0, 0, size, font, col)


def M(s, size=60, col=INK):
    return lambda c: text(c, s, 0, 0, size, MARKER, col)


def sc(fn, *a, s=1.0, **kw):
    def f(c):
        c.save()
        c.scale(s, s)
        fn(c, *a, **kw)
        c.restore()
    return f


def group(*fns):
    def f(c):
        for fn in fns:
            fn(c)
    return f


def at(x, y, fn):
    def f(c):
        c.save(); c.translate(x, y); fn(c); c.restore()
    return f


# ======================================================================= SCENES
def s01(c, t):  # 0 - 8  salário 5000 / carro 60000 / parece possível
    hero(c, t, 560, 960, 1.2, [(0, "stand"), (1.4, "present_l"), (3.4, "think"), (6.1, "thumb")],
         [(0, "happy"), (3.4, "think"), (6.1, "grin")], appear=0.1, look=lambda t: -1 if t < 3.4 else 0.6)
    show(c, t, 1.5, 230, 470, group(sc(bills, 3, s=1.2), at(0, 130, M("R$ 5.000", 60, GREEN)), at(0, 195, T("por mês", 46))))
    show(c, t, 3.6, 1310, 400, lambda c: thought(c, 700, 470, -520, 160), anim="pop")
    show(c, t, 4.0, 1310, 380, sc(car, RED, s=1.25))
    show(c, t, 4.6, 1430, 520, lambda c: price_tag(c, "R$ 60.000"))
    show(c, t, 6.1, 1310, 830, lambda c: hl(c, "Parece possível?", 0, 0, 64, LGREEN))
    show(c, t, 6.5, 1660, 820, sc(check_icon, 44))


def iceberg_bg(c, t):
    wl = 560
    # water
    c.rectangle(0, wl, W, H - wl)
    rgb(c, (0.80, 0.90, 0.98)); c.fill()
    # underwater mass
    poly(c, [(860, wl), (1440, wl), (1620, 720), (1560, 960), (1330, 1060), (980, 1050), (760, 930), (720, 740)])
    fs(c, (0.62, 0.80, 0.95), 6)
    # waves
    for i in range(14):
        x = i * 150 + (t * 30) % 150 - 150
        c.move_to(x, wl)
        c.curve_to(x + 37, wl - 14, x + 75, wl - 14, x + 112, wl)
    rgb(c, BLUE); c.set_line_width(5); c.stroke()
    # tip
    poly(c, [(900, wl), (1010, 470), (1070, 440), (1230, 440), (1300, 480), (1400, wl)])
    fs(c, WHITE, 6)


def s02(c, t):  # 8 - 18 iceberg
    show(c, t, 8.0, 0, 0, lambda c: iceberg_bg(c, t), anim="fade", d=0.5)
    show(c, t, 8.4, 1150, 395, sc(car, RED, s=0.95), anim="drop")
    show(c, t, 9.0, 1150, 270, lambda c: price_tag(c, "R$ 60.000", size=42))
    hero(c, t, 330, 960, 1.05, [(0, "stand"), (8.4, "point_r"), (13.0, "head")],
         [(0, "happy"), (8.4, "shocked"), (13.0, "worried")], appear=8.1, look=0.8)
    show(c, t, 10.6, 560, 230, lambda c: hl(c, "a parte menos importante?", 0, 0, 48, LYELLOW), anim="up")
    arrow_draw(c, t, 11.0, 830, 240, 990, 265)
    # hidden costs
    items = [(gas_pump, 900, 760, 0.62, 13.3), (shield, 1080, 860, 0.62, 13.8), (wrench_tire, 1310, 760, 0.6, 14.3),
             (lambda c: document(c, "IPVA"), 1250, 960, 0.6, 14.8), (coin, 1480, 650, 0.8, 15.3)]
    for fn, x, y, s, t0 in items:
        show(c, t, t0, x, y, sc(fn, s=s))
    show(c, t, 15.8, 1460, 880, M("?", 120, BLUE))
    title(c, t, 13.2, "Um carro de R$ 60.000 não custa só R$ 60.000", y=110, size=56)


def s03(c, t):  # 18 - 27 tranquila vs corrida
    line(c, 960, 60, 960, 1020, 5, LGRAY)
    show(c, t, 18.2, 480, 140, lambda c: hl(c, "Decisão tranquila", 0, 0, 58, LGREEN), anim="up")
    hero(c, t, 340, 950, 1.0, [(0, "hips")], [(0, "happy")], appear=18.3)
    show(c, t, 18.8, 700, 780, sc(car, BLUE, s=0.8))
    show(c, t, 19.4, 650, 420, sc(check_icon, 55))
    show(c, t, 22.2, 1440, 140, lambda c: hl(c, "Corrida até o fim do mês", 0, 0, 52, (1, 0.8, 0.76)), anim="up")
    if t > 22.4:
        show(c, t, 22.4, 1250, 760, lambda c: speed_lines(c, t), anim="fade")
    hero(c, t, 1390, 950, 1.0, [(0, "run")], [(0, "desperate")], appear=22.4, fid=5)
    show(c, t, 23.0, 1760, 560, group(sc(calendar, "30", s=1.05), at(0, 130, T("fim do mês", 42))))
    # flying bills
    if t > 23.6:
        for i in range(4):
            ph = ((t - 23.6) * 0.7 + i * 0.25) % 1.0
            x = 1300 - ph * 260 - i * 30
            y = 480 + math.sin(ph * 6 + i) * 30 - ph * 160 + i * 40
            c.save(); c.translate(x, y); c.rotate(ph * 4 + i); c.scale(0.45, 0.45)
            c.push_group(); bill(c); c.pop_group_to_source(); c.paint_with_alpha(1 - ph)
            c.restore()


def s04(c, t):  # 27 - 34 erro nº1
    show(c, t, 27.2, 960, 130, lambda c: ribbon(c, "ERRO Nº 1"), anim="pop")
    hero(c, t, 480, 970, 1.15, [(0, "stand"), (29.0, "think"), (32.4, "thumb")],
         [(0, "neutral"), (29.0, "think"), (32.4, "confident")], appear=27.4)
    show(c, t, 29.0, 1240, 560, lambda c: thought(c, 860, 560, -560, 80))
    show(c, t, 29.4, 1240, 400, lambda c: text(c, "Eu ganho R$ 5.000...", 0, 0, 58, MARKER, GREEN))
    show(c, t, 31.0, 1240, 520, lambda c: text(c, "parcela de R$ 1.000", 0, 0, 58, MARKER, BLUE))
    show(c, t, 32.4, 1240, 650, lambda c: hl(c, "= tá tudo certo!", 0, 0, 60, LYELLOW))


def s05(c, t):  # 34 - 43 o carro não termina na parcela
    title(c, t, 34.2, "Só que o carro não termina na parcela...", y=110, size=58)
    show(c, t, 34.3, 960, 560, sc(car, BLUE, s=1.15))
    show(c, t, 34.9, 960, 420, lambda c: price_tag(c, "Parcela", col=LYELLOW, size=40))
    items = [
        (gas_pump, "Combustível", 400, 380, 36.5),
        (shield, "Seguro", 690, 290, 37.3),
        (lambda c: document(c, "IPVA"), "IPVA", 1230, 290, 38.0),
        (wrench_tire, "Manutenção", 1520, 380, 38.7),
        (parking, "Estacionamento", 470, 760, 40.4),
        (toll, "Pedágio", 1450, 780, 41.6),
    ]
    for fn, lab, x, y, t0 in items:
        show(c, t, t0, x, y, icon_label(fn, lab, 44, 125, s=0.82))
    hero(c, t, 960, 1060, 0.55, [(0, "stand"), (38.7, "head")], [(0, "neutral"), (36.5, "worried"), (40.4, "desperate")], appear=35.2)


def s06(c, t):  # 43 - 46 conta de verdade
    title(c, t, 43.2, "Vamos fazer essa conta de verdade", y=130, size=64)
    hero(c, t, 640, 980, 1.15, [(0, "stand"), (43.6, "point_r")], [(0, "confident")], appear=43.2, look=1)
    show(c, t, 43.6, 1250, 590, lambda c: calculator(c, "R$ ?"), s=1.6)
    show(c, t, 44.2, 1480, 380, sc(sparkle, 34))
    show(c, t, 44.5, 1040, 380, sc(sparkle, 24))


def s07(c, t):  # 46 - 52 pessoa 5000, carro usado 60000
    hero(c, t, 420, 960, 1.1, [(0, "stand"), (46.5, "present_l"), (50.2, "point_r")], [(0, "happy")], appear=46.1,
         look=lambda t: -1 if t < 50.2 else 1)
    show(c, t, 46.6, 400, 240, group(sc(bills, 3, s=0.9), at(0, 100, M("Salário: R$ 5.000", 46, GREEN))))
    show(c, t, 50.2, 1300, 650, sc(car, ORANGE, s=1.35))
    show(c, t, 50.7, 1300, 400, lambda c: price_tag(c, "Usado: R$ 60.000", size=50))


def s08(c, t):  # 52 - 60 entrada 20000 + financiar 40000
    title(c, t, 52.2, "Carro de R$ 60.000", y=120, size=64)
    x0, y0, w, h = 260, 330, 1400, 130
    show(c, t, 52.4, 0, 0, lambda c: (rrect(c, x0, y0, w, h, 18), fs(c, WHITE, 7)), anim="fade")
    if t > 54.8:
        p = ease_out(prog(t, 54.8, 0.7))
        c.save(); rrect(c, x0, y0, w, h, 18); c.clip()
        c.rectangle(x0, y0, w / 3 * p, h); rgb(c, GREEN); c.fill()
        if t > 57.0:
            p2 = ease_out(prog(t, 57.0, 0.9))
            c.rectangle(x0 + w / 3, y0, w * 2 / 3 * p2, h); rgb(c, ORANGE); c.fill()
        c.restore()
        rrect(c, x0, y0, w, h, 18); rgb(c, INK); c.set_line_width(7); c.stroke()
        if t > 57.0:
            line(c, x0 + w / 3, y0, x0 + w / 3, y0 + h, 6)
    show(c, t, 55.2, x0 + w / 6, 395, M("R$ 20.000", 46, WHITE))
    show(c, t, 55.4, x0 + w / 6, 560, group(sc(bills, 2, s=0.7), at(0, 95, T("Entrada", 50))))
    show(c, t, 57.6, x0 + w * 2 / 3, 395, M("R$ 40.000", 50, WHITE))
    show(c, t, 58.0, x0 + w * 2 / 3, 560, T("Financiado", 50))
    show(c, t, 58.6, 1300, 800, group(sc(bank, s=1.1), at(0, 130, T("banco", 42))))
    arrow_draw(c, t, 58.6, 1130, 620, 1180, 760)
    hero(c, t, 430, 1060, 0.6, [(0, "stand"), (55.0, "point_ru")], [(0, "happy")], appear=52.6, look=1)


def s09(c, t):  # 60 - 65 juros prazo instituição
    title(c, t, 60.2, "A parcela depende de:", y=150, size=66)
    show(c, t, 61.0, 430, 560, icon_label(percent, "Taxa de juros", 40, 130, s=1.0), s=1.45)
    show(c, t, 62.1, 960, 560, icon_label(lambda c: clock(c, t), "Prazo", 40, 130, s=1.0), s=1.45)
    show(c, t, 63.1, 1490, 560, icon_label(bank, "Instituição financeira", 40, 130, s=1.0), s=1.45)


def s10(c, t):  # 65 - 73 não existe parcela universal / valor anunciado
    show(c, t, 65.2, 960, 130, lambda c: (hl(c, "Não existe parcela universal", 0, 0, 60, LYELLOW)), anim="up")
    # dealership platform
    show(c, t, 67.2, 1220, 780, lambda c: (ellipse(c, 0, 0, 330, 40), fs(c, LGRAY, 6)), anim="fade")
    show(c, t, 67.3, 1220, 690, sc(car, RED, s=1.35), anim="drop")
    show(c, t, 68.0, 1220, 430, lambda c: (ribbon(c, "OFERTA! R$ 60.000", col=RED, size=48)))
    show(c, t, 69.8, 1220, 920, lambda c: hl(c, "preço anunciado não é o custo real", 0, 0, 50, (1, 0.8, 0.76)), anim="up")
    hero(c, t, 400, 980, 1.1, [(0, "stand"), (65.3, "shrug"), (67.4, "point_r")],
         [(0, "neutral"), (67.4, "think")], appear=65.3, look=1)


def s11(c, t):  # 73 - 92 barra do salário
    title(c, t, 73.2, "Salário: R$ 5.000", y=110, size=60, col=GREEN)
    x0, y0, w, h = 210, 200, 1500, 120
    show(c, t, 73.3, 0, 0, lambda c: (rrect(c, x0, y0, w, h, 18), fs(c, WHITE, 7)), anim="fade")
    c.save(); rrect(c, x0, y0, w, h, 18); c.clip()
    if t > 74.0:
        p = ease_out(prog(t, 74.0, 0.8))
        c.rectangle(x0, y0, w * 0.2 * p, h); rgb(c, BLUE); c.fill()
    if t > 81.4:
        p = ease_out(prog(t, 81.4, 0.8))
        c.rectangle(x0 + w * 0.2, y0, w * 0.1 * p, h); rgb(c, ORANGE); c.fill()
    c.restore()
    if t > 73.3:
        rrect(c, x0, y0, w, h, 18); rgb(c, INK); c.set_line_width(7); c.stroke()
    show(c, t, 74.4, x0 + w * 0.1, 410, group(T("Parcela", 46), at(0, 50, M("R$ 1.000", 40, BLUE))))
    show(c, t, 77.0, x0 + w * 0.1, y0 + h / 2, M("20%", 56, WHITE))
    show(c, t, 81.8, x0 + w * 0.25, 410, group(T("Combustível", 46), at(0, 50, M("R$ 500", 40, ORANGE))))
    show(c, t, 77.0, 1340, 410, lambda c: hl(c, "20% do salário", 0, 0, 46, LYELLOW) if t < 82.4 else hl(c, "30% do salário", 0, 0, 46, LYELLOW), anim="up")
    show(c, t, 82.4, 1340, 530, lambda c: text(c, "Total: R$ 1.500", 0, 0, 56, MARKER, RED))
    # waiting icons
    for i, (fn, lab) in enumerate([(shield, "Seguro"), (lambda c: document(c, "IPVA"), "IPVA"), (wrench_tire, "Manutenção")]):
        show(c, t, 87.0 + i * 0.4, 540 + i * 330, 790, icon_label(fn, lab, 44, 120, s=0.75))
        show(c, t, 87.6 + i * 0.4, 640 + i * 330, 700, M("?", 70, RED))
    hero(c, t, 1690, 1050, 0.6, [(0, "stand"), (89.9, "finger_up")], [(0, "neutral"), (89.9, "confident")], appear=86.8, look=-1)
    show(c, t, 90.0, 1790, 620, lambda c: exclaim(c, 100))


MONTHS = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]


def s12(c, t):  # 92 - 99 nem todo gasto é mensal
    title(c, t, 92.3, "Nem todo gasto chega todo mês", y=110, size=60)
    gx, gy, cw, ch = 760, 230, 260, 190
    for i, m in enumerate(MONTHS):
        r, k = divmod(i, 4)
        x, y = gx + k * cw, gy + r * ch

        def cell(c, m=m, i=i):
            rrect(c, -cw / 2 + 10, -ch / 2 + 10, cw - 20, ch - 20, 14)
            fs(c, WHITE, 5)
            c.rectangle(-cw / 2 + 12, -ch / 2 + 12, cw - 24, 40)
            rgb(c, (1, 0.85, 0.82)); c.fill()
            text(c, m, 0, -ch / 2 + 32, 30, MARKER)
        show(c, t, 92.6 + i * 0.06, x + cw / 2, y + ch / 2, cell)
    # IPVA once a year (JAN)
    show(c, t, 94.9, gx + cw / 2, gy + ch / 2 + 22, group(sc(lambda c: document(c, "IPVA"), s=0.5)), anim="stamp")
    # maintenance surprise in JUL
    jx, jy = gx + 2 * cw + cw / 2, gy + ch + ch / 2 + 22
    wob = math.sin(t * 18) * 0.15 if t > 96.4 else 0
    show(c, t, 96.4, jx, jy, sc(wrench_tire, s=0.42), rot=wob)
    show(c, t, 96.8, jx + 85, jy - 50, M("!", 70, RED))
    show(c, t, 95.2, gx - 120, gy + ch / 2 + 20, lambda c: text(c, "anual", 0, 0, 44, HAND, RED), anim="right")
    hero(c, t, 330, 980, 1.0, [(0, "stand"), (95.0, "point_r"), (96.5, "head")], [(0, "neutral"), (96.5, "shocked")],
         appear=92.5, look=1)


def s13(c, t):  # 99 - 109 média mensal / quanto custa por mês
    title(c, t, 99.2, "Transforme em média mensal", y=120, size=64)
    show(c, t, 100.2, 470, 430, group(sc(calendar, "12", top=BLUE, s=1.2), at(0, 150, T("gasto do ano", 46))))
    show(c, t, 101.6, 960, 430, M("÷ 12", 110, RED))
    arrow_draw(c, t, 101.6, 650, 430, 820, 430, bend=0)
    arrow_draw(c, t, 102.6, 1100, 430, 1270, 430, bend=0)
    show(c, t, 102.8, 1450, 430, group(sc(calendar, "1", top=GREEN, s=1.2), at(0, 150, T("média por mês", 46))))
    show(c, t, 105.8, 1050, 820, lambda c: (hl(c, "Quanto esse carro custa POR MÊS?", 0, 0, 60, LYELLOW)), anim="up")
    hero(c, t, 230, 1060, 0.62, [(0, "stand"), (105.8, "think")], [(0, "happy"), (105.8, "think")], appear=99.4, look=1)


def s14(c, t):  # 109 - 129 nota de custos
    # receipt
    rx, ry, rw, rh = 760, 150, 900, 860

    def paper(c):
        c.move_to(0, 0); c.line_to(rw, 0); c.line_to(rw, rh)
        n = 18
        for i in range(n):
            c.line_to(rw - (i + 0.5) * rw / n, rh - 18)
            c.line_to(rw - (i + 1) * rw / n, rh)
        c.close_path()
        fs(c, WHITE, 6)
        text(c, "CUSTO POR MÊS", rw / 2, 60, 52, MARKER)
        text(c, "(exemplo)", rw / 2, 115, 36, HAND, GRAY)
        line(c, 40, 150, rw - 40, 150, 4, LGRAY)
    show(c, t, 109.2, rx, ry, paper, anim="up")
    rows = [
        (lambda c: sc(document, "R$", tcol=BLUE, s=0.3)(c), "Parcela", "R$ 1.000", 112.2),
        (sc(gas_pump, s=0.3), "Combustível", "R$ 500", 113.7),
        (sc(shield, s=0.3), "Seguro", "R$ 250", 115.2),
        (lambda c: sc(document, "IPVA", s=0.3)(c), "IPVA", "R$ 150", 116.7),
        (sc(wrench_tire, s=0.3), "Manutenção e pneus", "R$ 150", 121.2),
    ]
    for i, (ic, lab, val, t0) in enumerate(rows):
        y = ry + 225 + i * 100

        def row(c, ic=ic, lab=lab, val=val):
            c.save(); c.translate(70, 0); ic(c); c.restore()
            text(c, lab, 140, 0, 50, HAND, INK, align="l")
            text(c, val, rw - 50, 0, 50, MARKER, INK, align="r")
        show(c, t, t0, rx, y, row, anim="left")
    show(c, t, 118.2, rx + 380, ry + 225 + 3 * 100 + 40, lambda c: text(c, "(valor do ano ÷ 12)", 0, 0, 34, HAND, GRAY), anim="fade")
    if t > 124.6:
        p = ease_out(prog(t, 124.6, 0.4))
        line(c, rx + 40, ry + 735, rx + 40 + (rw - 80) * p, ry + 735, 6)
    def total(c):
        text(c, "TOTAL", 40, 0, 60, MARKER, RED, align="l")
        text(c, "R$ 2.050", rw - 50, 0, 64, MARKER, RED, align="r")
    show(c, t, 125.2, rx, ry + 790, total, anim="up")
    hero(c, t, 340, 970, 1.05, [(0, "stand"), (109.5, "think"), (125.2, "head")],
         [(0, "neutral"), (109.5, "think"), (125.2, "shocked")], appear=109.3, look=1)


def s15(c, t):  # 129 - 140 41% do salário
    title(c, t, 129.2, "R$ 2.050 de R$ 5.000", y=110, size=62)
    pct = 0.41 * ease_io(prog(t, 129.6, 1.4))
    show(c, t, 129.4, 1240, 520, lambda c: donut(c, pct, 230, 80, RED), anim="pop")
    show(c, t, 129.6, 1240, 500, lambda c: text(c, f"{round(pct*100)}%", 0, 0, 110, MARKER, RED))
    show(c, t, 130.4, 1240, 590, T("do salário", 44))
    extras = [(parking, "Estacionamento", 950, 134.4), (toll, "Pedágio", 1250, 135.3), (lambda c: exclaim(c, 130), "Imprevistos", 1560, 136.4)]
    for fn, lab, x, t0 in extras:
        show(c, t, t0, x, 900, icon_label(fn, "+ " + lab, 40, 110, s=0.62))
    hero(c, t, 420, 980, 1.1, [(0, "stand"), (130.4, "head")], [(0, "worried"), (130.4, "desperate")], appear=129.3, look=1)


def s16(c, t):  # 140 - 148 pergunta mais interessante / número mágico
    title(c, t, 140.2, "A pergunta mais interessante...", y=120, size=58)
    bob = math.sin(t * 3) * 8
    show(c, t, 140.5, 960, 400 + bob, M("?", 300, ORANGE))
    show(c, t, 142.8, 960, 690, lambda c: hl(c, "Quanto posso gastar em um carro?", 0, 0, 66, LYELLOW), anim="up")

    def magic(c):
        text(c, "número mágico", 0, 0, 64, MARKER, PURPLE)
        for sx, sy, r in ((-280, -30, 26), (270, -40, 22), (300, 30, 16)):
            c.save(); c.translate(sx, sy); sparkle(c, r); c.restore()
    show(c, t, 145.2, 1060, 905, magic)
    show(c, t, 145.9, 1060, 905, lambda c: big_x(c, 190, RED, 14), anim="stamp")
    show(c, t, 145.3, 1060, 1000, T("não existe", 46, RED))
    hero(c, t, 300, 1060, 0.62, [(0, "stand"), (140.4, "think"), (145.4, "shrug")], [(0, "think"), (145.4, "neutral")], appear=140.3, look=1)


def s17(c, t):  # 148 - 169 duas pessoas
    line(c, 960, 60, 960, 1020, 5, LGRAY)
    # person A
    show(c, t, 148.2, 480, 110, lambda c: hl(c, "Pessoa A • R$ 5.000", 0, 0, 52, LGREEN), anim="up")
    hero(c, t, 230, 980, 0.95, [(0, "stand"), (150, "hips"), (166.0, "thumb")], [(0, "happy"), (166.0, "grin")], appear=148.3)
    a_items = [(sc(house, False, s=0.6), "Aluguel baixo", 149.8), (sc(check_icon, 34), "Nenhuma dívida", 151.3), (sc(piggy, s=0.45), "Boa reserva", 152.6)]
    for i, (fn, lab, t0) in enumerate(a_items):
        y = 290 + i * 150
        show(c, t, t0, 560, y, group(fn, at(90, 0, lambda c, lab=lab: text(c, lab, 0, 0, 46, HAND, INK, align="l"))), anim="left")
    # person B
    show(c, t, 154.0, 1440, 110, lambda c: hl(c, "Pessoa B • R$ 5.000", 0, 0, 52, (1, 0.8, 0.76)), anim="up")
    other(c, t, 1190, 980, 0.95, [(0, "stand"), (157, "hips"), (166.0, "head")], [(0, "neutral"), (157.0, "worried"), (166.0, "desperate")], appear=154.1)
    b_items = [(sc(house, True, s=0.45), "Aluguel caro", 155.3), (sc(card, s=0.45), "Cartão", 156.9),
               (sc(document, "R$", tcol=RED, s=0.42), "Empréstimo", 157.8), (sc(piggy, (0.85, 0.85, 0.85), s=0.42), "Sem reserva", 159.4)]
    for i, (fn, lab, t0) in enumerate(b_items):
        y = 270 + i * 125
        show(c, t, t0, 1520, y, group(fn, at(90, 0, lambda c, lab=lab: text(c, lab, 0, 0, 46, HAND, INK, align="l"))), anim="left")
    if t > 159.6:
        show(c, t, 159.6, 1520, 270 + 3 * 125, lambda c: big_x(c, 40, RED, 9), anim="stamp")
    # verdicts
    show(c, t, 163.0, 960, 110, lambda c: (circle(c, 0, 0, 46, WHITE, 6), eq(c, 24, INK, 9)))
    show(c, t, 165.8, 690, 850, group(sc(check_icon, 40), at(0, 80, T("consegue manter", 44, GREEN))))
    show(c, t, 166.3, 1650, 850, group(sc(x_icon, 40), at(0, 80, T("aperta o orçamento", 44, RED))))


def s18(c, t):  # 169 - 180 trocar a pergunta
    hero(c, t, 300, 990, 1.05, [(0, "stand"), (169.3, "think"), (174.0, "finger_up")],
         [(0, "neutral"), (169.3, "think"), (174.0, "grin")], appear=169.2, look=1)
    show(c, t, 174.2, 300, 330, sc(bulb, s=0.9))

    def q1(c):
        hl(c, "“Qual carro consigo financiar?”", 0, 0, 56, LGRAY)
    show(c, t, 169.4, 1150, 260, q1, anim="up")
    if t > 172.2:
        p = ease_out(prog(t, 172.2, 0.5))
        line(c, 1150 - 470, 262, 1150 - 470 + 940 * p, 252, 12, RED)
    show(c, t, 173.0, 1150, 400, T("em vez disso, pergunte:", 48, GRAY), anim="fade")

    def q2(c):
        hl(c, "“Quanto do meu orçamento", 0, -75, 58, LGREEN)
        hl(c, "posso comprometer", 0, 15, 58, LGREEN)
        hl(c, "sem destruir minha vida financeira?”", 0, 105, 58, LGREEN)
    show(c, t, 174.2, 1150, 620, q2, anim="up")


def s19(c, t):  # 180 - 188 pagar ≠ manter
    show(c, t, 180.2, 520, 220, lambda c: hl(c, "Conseguir pagar a parcela", 0, 0, 52, LGREEN), anim="up")
    show(c, t, 180.5, 520, 520, sc(bills, 3, s=1.3))
    show(c, t, 181.4, 700, 400, sc(check_icon, 44))
    show(c, t, 182.4, 1400, 220, lambda c: hl(c, "Conseguir manter o carro", 0, 0, 52, LYELLOW), anim="up")
    show(c, t, 182.6, 1400, 540, sc(car, BLUE, s=1.0))
    for i, (fn, x, y) in enumerate([(gas_pump, 1210, 420), (shield, 1590, 420), (wrench_tire, 1400, 380)]):
        show(c, t, 183.0 + i * 0.25, x, y, sc(fn, s=0.4))
    show(c, t, 185.2, 960, 520, lambda c: neq(c, 70, RED, 16), anim="stamp")
    show(c, t, 185.6, 960, 860, lambda c: text(c, "Uma diferença enorme!", 0, 0, 72, MARKER, RED), anim="up")


def s20(c, t):  # 188 - 206 teste simples
    show(c, t, 188.2, 960, 120, lambda c: ribbon(c, "TESTE SIMPLES", col=BLUE), anim="pop")
    show(c, t, 192.8, 960, 250, T("Durante alguns meses, finja que já tem o carro", 52), anim="up")
    hero(c, t, 300, 990, 1.0, [(0, "stand"), (193.0, "present"), (200.8, "point_r")], [(0, "happy"), (193.0, "confident"), (200.8, "happy")], appear=188.4, look=1)
    show(c, t, 193.4, 760, 800, sc(car, s=1.05, ghost=True), anim="fade")
    show(c, t, 193.6, 760, 900, T("carro imaginário", 40, GRAY))
    show(c, t, 196.8, 760, 560, lambda c: price_tag(c, "R$ 1.800/mês", size=48))
    show(c, t, 200.6, 1430, 790, sc(piggy, s=1.35))
    show(c, t, 200.6, 1430, 950, T("separe todo mês", 46))
    if t > 201.2:
        month = min(6, 1 + int((t - 201.2) / 1.6))
        show(c, t, 201.2, 1430, 450, lambda c: hl(c, f"Mês {month}", 0, 0, 50, LGREEN))
        ph = ((t - 201.2) / 1.6) % 1.0
        if ph < 0.7:
            y = 540 + ease_io(ph / 0.7) * 120
            c.save(); c.translate(1430, y); c.scale(0.7, 0.7); coin(c); c.restore()


def s21(c, t):  # 206 - 216 sem cartão / cheque especial / contas
    title(c, t, 206.1, "Sem precisar de...", y=120, size=64)
    items = [(sc(card, s=1.0), "usar o cartão", 480, 206.4),
             (sc(document, "CHEQUE", tcol=BLUE, tsize=26, s=1.0), "cheque especial", 960, 207.8),
             (sc(document, "CONTAS", tcol=ORANGE, tsize=28, s=1.0), "atrasar contas", 1440, 209.1)]
    for fn, lab, x, t0 in items:
        show(c, t, t0, x, 400, icon_label(fn, lab, 48, 140))
        show(c, t, t0 + 0.6, x, 380, lambda c: big_x(c, 95, RED, 16), anim="stamp")
    show(c, t, 212.0, 960, 760, lambda c: hl(c, "Você enxerga o impacto real no orçamento", 0, 0, 54, LGREEN), anim="up")
    hero(c, t, 960, 1070, 0.42, [(0, "stand"), (212.0, "thumb")], [(0, "neutral"), (212.0, "grin")], appear=206.4)


def s22(c, t):  # 216 - 221 dinheiro continua seu
    title(c, t, 216.2, "E o dinheiro continua SEU!", y=130, size=72, col=GREEN)
    hero(c, t, 520, 990, 1.15, [(0, "arms_up")], [(0, "grin")], appear=216.3)
    show(c, t, 216.6, 1250, 640, sc(piggy, s=2.2))
    for i in range(6):
        t0 = 217.0 + i * 0.35
        a = i * 1.05
        show(c, t, t0, 1250 + math.cos(a) * 330, 600 + math.sin(a) * 250, sc(coin, s=0.8))
    for i, (x, y) in enumerate([(720, 400), (1600, 330), (1000, 300)]):
        show(c, t, 217.4 + i * 0.3, x, y, sc(sparkle, 30))


def s23(c, t):  # 221 - 231 quanto posso gastar? não é só um número
    show(c, t, 221.2, 960, 150, lambda c: (text(c, "Então, quanto posso gastar", 0, 0, 64, MARKER), text(c, "ganhando R$ 5.000?", 0, 85, 64, MARKER, GREEN)), anim="up")
    tags = [("R$ 50.000", 520, 225.2), ("R$ 60.000", 960, 225.9), ("R$ ???", 1400, 226.8)]
    for s, x, t0 in tags:
        show(c, t, t0, x, 520, lambda c, s=s: price_tag(c, s, size=56))
    for i, (s_, x, t0) in enumerate(tags):
        show(c, t, 228.0 + i * 0.25, x, 520, lambda c: big_x(c, 150, RED, 14), anim="stamp")
    show(c, t, 228.6, 960, 700, T("a resposta não é um número fixo", 54, RED), anim="up")
    hero(c, t, 960, 1070, 0.5, [(0, "stand"), (228.4, "shrug")], [(0, "think"), (228.4, "neutral")], appear=221.4)


def s24(c, t):  # 231 - 241 comprar ≠ manter / olhe o orçamento
    show(c, t, 231.2, 520, 190, lambda c: hl(c, "COMPRAR", 0, 0, 80, LGREEN))
    show(c, t, 231.9, 960, 190, lambda c: neq(c, 50, RED, 14), anim="stamp")
    show(c, t, 232.4, 1400, 190, lambda c: hl(c, "MANTER", 0, 0, 80, LYELLOW))
    hero(c, t, 420, 1000, 1.0, [(0, "stand"), (235.0, "think"), (238.0, "point_r")],
         [(0, "neutral"), (235.0, "happy"), (238.0, "confident")], appear=234.6, look=1)
    show(c, t, 235.3, 800, 520, lambda c: thought(c, 460, 320, -240, 160), t1=237.8)
    show(c, t, 235.6, 800, 520, sc(car, PURPLE, s=0.85), t1=237.8)
    show(c, t, 235.9, 800, 380, T("carro dos sonhos", 40), t1=237.8)
    for i, (x, y) in enumerate([(620, 420), (990, 440)]):
        show(c, t, 236.0 + i * 0.2, x, y, sc(sparkle, 20), t1=237.8)
    show(c, t, 238.0, 1300, 680, sc(clipboard, "ORÇAMENTO", s=1.25))
    show(c, t, 238.5, 1300, 920, T("olhe primeiro para o seu orçamento", 46))


def s25(c, t):  # 241 - 251 próximo vídeo
    show(c, t, 241.2, 960, 120, lambda c: ribbon(c, "NO PRÓXIMO VÍDEO", col=PURPLE), anim="pop")
    show(c, t, 242.2, 960, 530, sc(calculator, "R$ ?", s=1.5), t1=244.9)
    show(c, t, 242.6, 1150, 360, sc(sparkle, 30), t1=244.9)
    show(c, t, 245.0, 960, 270, lambda c: text(c, "Quanto preciso ganhar por mês para manter um carro de...", 0, 0, 46, HAND), anim="up")
    cars = [(BLUE, "R$ 60.000", 480, 247.6), (RED, "R$ 80.000", 960, 248.4), (DGRAY, "R$ 100.000", 1440, 249.2)]
    for col, s, x, t0 in cars:
        show(c, t, t0, x, 560, sc(car, col, s=0.95))
        show(c, t, t0 + 0.2, x, 720, lambda c, s=s: price_tag(c, s, size=46))
    show(c, t, 250.0, 960, 900, lambda c: hl(c, "Salário necessário = ?", 0, 0, 56, LYELLOW), anim="up")


def s26(c, t):  # 251 - end inscreva-se
    hero(c, t, 380, 990, 1.1, [(0, "wave")], [(0, "grin")], appear=251.1)
    done = t > 253.0
    k = 0.92 if 252.9 < t < 253.15 else 1.0
    show(c, t, 251.4, 1150, 360, sc(subscribe_btn, done, s=k))
    # cursor
    if 251.9 < t < 254.4:
        p = ease_io(prog(t, 251.9, 0.9)) - ease_io(prog(t, 253.4, 0.8))
        cx = 1700 + (1260 - 1700) * p
        cy = 640 + (380 - 640) * p
        c.save(); c.translate(cx, cy); cursor(c); c.restore()
    wig = math.sin(t * 20) * 0.25 * max(0, 1 - (t - 253.4) / 1.2) if t > 253.4 else 0
    show(c, t, 253.3, 1530, 360, sc(bell, s=1.0), rot=wig)
    show(c, t, 254.3, 1180, 700, lambda c: (speech(c, 880, 190, -260, 175), text(c, "Qual carro você gostaria de comprar?", 0, 0, 50, HAND)))
    show(c, t, 255.0, 1180, 900, T("comenta aqui embaixo!", 48, GRAY), anim="up")


SCENES = [
    (0.0, 8.0, s01), (8.0, 18.0, s02), (18.0, 27.0, s03), (27.0, 34.0, s04), (34.0, 43.0, s05),
    (43.0, 46.0, s06), (46.0, 52.0, s07), (52.0, 60.0, s08), (60.0, 65.0, s09), (65.0, 73.0, s10),
    (73.0, 92.0, s11), (92.0, 99.0, s12), (99.0, 109.0, s13), (109.0, 129.0, s14), (129.0, 140.0, s15),
    (140.0, 148.0, s16), (148.0, 169.0, s17), (169.0, 180.0, s18), (180.0, 188.0, s19), (188.0, 206.0, s20),
    (206.0, 216.0, s21), (216.0, 221.0, s22), (221.0, 231.0, s23), (231.0, 241.0, s24), (241.0, 251.0, s25),
    (251.0, 999.0, s26),
]
