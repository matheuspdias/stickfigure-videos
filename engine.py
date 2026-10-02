import cairo, math, random

W, H, FPS = 1920, 1080, 30

INK = (0.11, 0.11, 0.12)
PAPER = (0.984, 0.972, 0.945)
WHITE = (1, 1, 1)
GREEN = (0.20, 0.64, 0.38)
LGREEN = (0.78, 0.92, 0.80)
RED = (0.89, 0.29, 0.24)
YELLOW = (0.99, 0.77, 0.22)
LYELLOW = (1.0, 0.92, 0.55)
BLUE = (0.25, 0.50, 0.86)
LBLUE = (0.76, 0.88, 0.98)
ORANGE = (0.97, 0.56, 0.20)
PINK = (0.97, 0.66, 0.74)
PURPLE = (0.48, 0.36, 0.80)
GRAY = (0.62, 0.62, 0.64)
LGRAY = (0.88, 0.87, 0.84)
DGRAY = (0.32, 0.32, 0.35)
BROWN = (0.62, 0.43, 0.26)

MARKER = "Permanent Marker"
HAND = "Patrick Hand"


# ---------------------------------------------------------------- easing
def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def ease_out(p):
    return 1 - (1 - p) ** 3


def ease_io(p):
    return p * p * (3 - 2 * p)


def ease_out_back(p, s=1.9):
    p = p - 1
    return p * p * ((s + 1) * p + s) + 1


def prog(t, t0, d=0.4):
    return clamp01((t - t0) / d)


# ---------------------------------------------------------------- eventos sonoros
_CUES = None  # quando é uma lista, os eventos visuais são registrados aqui (ver sfx.py)


def cue(t0, kind):
    if _CUES is not None:
        _CUES.append((round(float(t0), 3), kind))


def rgb(c, col, a=1.0):
    c.set_source_rgba(col[0], col[1], col[2], a)


# ---------------------------------------------------------------- basic helpers
def rrect(c, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def fs(c, fill, lw=6, stroke=INK):
    """fill + stroke current path"""
    if fill is not None:
        rgb(c, fill)
        c.fill_preserve()
    rgb(c, stroke)
    c.set_line_width(lw)
    c.stroke()


def poly(c, pts):
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()


def line(c, x1, y1, x2, y2, lw=6, col=INK):
    c.move_to(x1, y1)
    c.line_to(x2, y2)
    rgb(c, col)
    c.set_line_width(lw)
    c.stroke()


def circle(c, x, y, r, fill=None, lw=6, stroke=INK):
    c.new_sub_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    if lw == 0:
        rgb(c, fill)
        c.fill()
    else:
        fs(c, fill, lw, stroke)


def ellipse(c, x, y, rx, ry):
    c.save()
    c.translate(x, y)
    c.scale(rx, ry)
    c.new_sub_path()
    c.arc(0, 0, 1, 0, 2 * math.pi)
    c.restore()


def text_w(c, s, size, font=MARKER):
    c.select_font_face(font)
    c.set_font_size(size)
    return c.text_extents(s).x_advance


def text(c, s, x=0, y=0, size=60, font=MARKER, col=INK, align="c", outline=None, ow=10, alpha=1.0):
    c.select_font_face(font)
    c.set_font_size(size)
    e = c.text_extents(s)
    if align == "c":
        tx = x - e.x_advance / 2
    elif align == "r":
        tx = x - e.x_advance
    else:
        tx = x
    ty = y + size * 0.36
    c.move_to(tx, ty)
    if outline is not None:
        c.text_path(s)
        rgb(c, outline, alpha)
        c.set_line_width(ow)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke_preserve()
        rgb(c, col, alpha)
        c.fill()
    else:
        rgb(c, col, alpha)
        c.show_text(s)
    return e.x_advance


def hl(c, s, x, y, size=56, bg=LYELLOW, col=INK, font=MARKER, pad=22, rot=-0.015, lw=0):
    """text with marker-highlight background"""
    w = text_w(c, s, size, font)
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    rrect(c, -w / 2 - pad, -size * 0.62, w + 2 * pad, size * 1.24, 14)
    if lw:
        fs(c, bg, lw)
    else:
        rgb(c, bg)
        c.fill()
    text(c, s, 0, 0, size, font, col)
    c.restore()


def show(c, t, t0, x, y, fn, s=1.0, anim="pop", d=0.45, t1=None, rot=0.0):
    """draw fn at (x,y) with an entrance animation starting at t0 (and optional fade-out at t1)"""
    cue(t0, "anim:" + anim)
    if t < t0:
        return
    p = prog(t, t0, d)
    alpha = 1.0
    if t1 is not None and t > t1:
        alpha = 1 - prog(t, t1, 0.3)
        if alpha <= 0:
            return
    c.save()
    c.translate(x, y)
    sc = s
    if anim == "pop":
        k = ease_out_back(p)
        if k < 0.02:
            c.restore()
            return
        sc = s * k
    elif anim == "fade":
        alpha *= ease_out(p)
    elif anim == "up":
        c.translate(0, (1 - ease_out(p)) * 70)
        alpha *= ease_out(p)
    elif anim == "left":
        c.translate(-(1 - ease_out(p)) * 260, 0)
        alpha *= ease_out(p)
    elif anim == "right":
        c.translate((1 - ease_out(p)) * 260, 0)
        alpha *= ease_out(p)
    elif anim == "drop":
        c.translate(0, -(1 - ease_out_back(p, 1.4)) * 500)
        alpha *= clamp01(p * 3)
    elif anim == "stamp":
        k = 1 + (1 - ease_out(p)) * 1.6
        sc = s * k
        alpha *= clamp01(p * 2.5)
    c.scale(sc, sc)
    if rot:
        c.rotate(rot)
    if alpha < 0.999:
        c.push_group()
        fn(c)
        c.pop_group_to_source()
        c.paint_with_alpha(alpha)
    else:
        fn(c)
    c.restore()


def arrow(c, x1, y1, x2, y2, col=INK, lw=7, bend=0.15, head=26):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * bend, my + dx * bend
    c.move_to(x1, y1)
    c.curve_to(cx, cy, cx, cy, x2, y2)
    rgb(c, col)
    c.set_line_width(lw)
    c.stroke()
    a = math.atan2(y2 - cy, x2 - cx)
    for s in (-1, 1):
        c.move_to(x2, y2)
        c.line_to(x2 - head * math.cos(a + s * 0.45), y2 - head * math.sin(a + s * 0.45))
    c.stroke()


def arrow_draw(c, t, t0, x1, y1, x2, y2, d=0.5, **kw):
    """arrow that grows from start"""
    cue(t0, "arrow")
    if t < t0:
        return
    p = ease_out(prog(t, t0, d))
    if p < 0.05:
        return
    arrow(c, x1, y1, x1 + (x2 - x1) * p, y1 + (y2 - y1) * p, **kw)


# ---------------------------------------------------------------- OBJECTS (drawn centered at 0,0)
def car(c, color=BLUE, ghost=False):
    body = [(-158, 26), (-158, -24), (-124, -40), (-78, -44), (-46, -92), (56, -92), (98, -44), (146, -36), (160, -10), (160, 26)]
    poly(c, body)
    if ghost:
        c.set_dash([18, 14])
        fs(c, None, 6, GRAY)
    else:
        fs(c, color, 6)
    wins = [[(-36, -80), (-3, -80), (-3, -48), (-62, -48)], [(8, -80), (50, -80), (82, -48), (8, -48)]]
    for w in wins:
        poly(c, w)
        if ghost:
            fs(c, None, 4, GRAY)
        else:
            fs(c, LBLUE, 4)
    if not ghost:
        line(c, 2, -44, 2, 18, 4)
        line(c, 18, -26, 34, -26, 5)
        circle(c, 149, -16, 9, YELLOW, 4)
        rrect(c, -160, -22, 12, 18, 3)
        fs(c, RED, 3)
    for wx in (-96, 96):
        if ghost:
            circle(c, wx, 28, 34, None, 6, GRAY)
        else:
            circle(c, wx, 28, 34, INK, 0)
            circle(c, wx, 28, 15, (0.78, 0.78, 0.8), 0)
    c.set_dash([])


def price_tag(c, s, col=YELLOW, size=46, tcol=INK):
    w = text_w(c, s, size) + 70
    h = size * 1.55
    c.save()
    c.rotate(-0.06)
    poly(c, [(-w / 2, 0), (-w / 2 + 30, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2 + 30, h / 2)])
    fs(c, col, 5)
    circle(c, -w / 2 + 28, 0, 7, PAPER, 4)
    text(c, s, 14, 0, size, MARKER, tcol)
    c.restore()


def bill(c):
    rrect(c, -90, -46, 180, 92, 8)
    fs(c, GREEN, 5)
    rrect(c, -78, -35, 156, 70, 6)
    rgb(c, LGREEN)
    c.set_line_width(3)
    c.stroke()
    circle(c, 0, 0, 25, LGREEN, 3, (0.1, 0.4, 0.2))
    text(c, "R$", 0, -2, 26, MARKER, (0.1, 0.4, 0.2))


def bills(c, n=3):
    for i in range(n):
        c.save()
        c.translate(-i * 12 + (n - 1) * 6, -i * 13 + (n - 1) * 6)
        c.rotate(-0.12 + i * 0.09)
        bill(c)
        c.restore()


def coin(c):
    circle(c, 0, 0, 40, YELLOW, 5)
    circle(c, 0, 0, 29, None, 3, (0.8, 0.55, 0.08))
    text(c, "$", 0, -2, 38, MARKER, (0.7, 0.45, 0.05))


def gas_pump(c):
    rrect(c, -60, -85, 90, 165, 12)
    fs(c, RED, 6)
    rrect(c, -46, -70, 62, 42, 6)
    fs(c, WHITE, 4)
    rrect(c, -72, 76, 114, 16, 4)
    fs(c, INK, 4)
    c.move_to(30, -40)
    c.curve_to(80, -40, 80, 30, 62, 50)
    rgb(c, INK)
    c.set_line_width(9)
    c.stroke()
    rrect(c, 50, -78, 22, 40, 5)
    fs(c, DGRAY, 4)
    c.move_to(-15, -5)
    c.curve_to(-30, 20, -28, 35, -15, 38)
    c.curve_to(-2, 35, 0, 20, -15, -5)
    fs(c, YELLOW, 3)


def shield(c, col=BLUE):
    c.move_to(0, -80)
    c.line_to(66, -56)
    c.curve_to(66, 12, 42, 55, 0, 80)
    c.curve_to(-42, 55, -66, 12, -66, -56)
    c.close_path()
    fs(c, col, 6)
    c.move_to(-26, 2)
    c.line_to(-6, 24)
    c.line_to(30, -24)
    rgb(c, WHITE)
    c.set_line_width(13)
    c.stroke()


def document(c, title="IPVA", tcol=RED, tsize=34):
    poly(c, [(-62, -82), (36, -82), (62, -56), (62, 82), (-62, 82)])
    fs(c, WHITE, 6)
    poly(c, [(36, -82), (36, -56), (62, -56)])
    fs(c, LGRAY, 4)
    text(c, title, -4, -32, tsize, MARKER, tcol)
    for y in (8, 32, 56):
        line(c, -40, y, 40, y, 5, GRAY)


def wrench(c):
    c.save()
    c.rotate(-0.75)
    line(c, 0, -20, 0, 100, 34, INK)
    line(c, 0, -20, 0, 100, 22, GRAY)
    circle(c, 0, -52, 40, GRAY, 6)
    rgb(c, PAPER)
    c.rectangle(-14, -100, 28, 48)
    c.fill()
    line(c, -14, -88, -14, -55, 6)
    line(c, 14, -88, 14, -55, 6)
    line(c, -14, -55, 14, -55, 6)
    circle(c, 0, 86, 7, PAPER, 4)
    c.restore()


def tire(c):
    circle(c, 0, 0, 60, INK, 0)
    for i in range(12):
        a = i * math.pi / 6
        line(c, 50 * math.cos(a), 50 * math.sin(a), 60 * math.cos(a), 60 * math.sin(a), 4, DGRAY)
    circle(c, 0, 0, 32, (0.75, 0.75, 0.78), 0)
    circle(c, 0, 0, 11, DGRAY, 0)


def wrench_tire(c):
    c.save(); c.translate(-30, 10); tire(c); c.restore()
    c.save(); c.translate(40, -10); c.scale(0.8, 0.8); wrench(c); c.restore()


def parking(c):
    rrect(c, -58, -58, 116, 116, 18)
    fs(c, BLUE, 6)
    text(c, "P", 0, 0, 92, MARKER, WHITE)


def toll(c):
    rrect(c, -86, -20, 22, 110, 4)
    fs(c, GRAY, 5)
    c.rectangle(-70, -18, 170, 26)
    fs(c, WHITE, 5)
    for i in range(5):
        if i % 2 == 0:
            c.rectangle(-64 + i * 33, -15, 30, 20)
            rgb(c, RED)
            c.fill()
    c.rectangle(-70, -18, 170, 26)
    rgb(c, INK); c.set_line_width(5); c.stroke()
    rrect(c, -95, -100, 170, 56, 10)
    fs(c, YELLOW, 5)
    text(c, "PEDÁGIO", -10, -72, 30, MARKER)


def house(c, big=False, col=LYELLOW):
    w = 190 if big else 120
    h = w * 0.72
    c.rectangle(-w / 2, -h * 0.35, w, h)
    fs(c, col, 6)
    poly(c, [(-w / 2 - 18, -h * 0.35), (0, -h * 1.05), (w / 2 + 18, -h * 0.35)])
    fs(c, RED, 6)
    dw = w * 0.22
    c.rectangle(-dw / 2 - w * 0.18, h * 0.65 - dw * 1.6, dw, dw * 1.6)
    fs(c, BROWN, 5)
    c.rectangle(w * 0.08, -h * 0.12, w * 0.26, w * 0.24)
    fs(c, LBLUE, 5)


def card(c, col=PURPLE):
    rrect(c, -95, -60, 190, 120, 14)
    fs(c, col, 6)
    c.rectangle(-95, -34, 190, 20)
    rgb(c, INK); c.fill()
    rrect(c, -70, 0, 38, 28, 5)
    fs(c, YELLOW, 4)
    circle(c, 46, 30, 17, RED, 0)
    circle(c, 66, 30, 17, ORANGE, 0)


def bank(c):
    poly(c, [(-95, -42), (0, -100), (95, -42)])
    fs(c, LGRAY, 6)
    text(c, "$", 0, -62, 34, MARKER, GREEN)
    c.rectangle(-95, -42, 190, 18)
    fs(c, LGRAY, 6)
    for x in (-72, -30, 12, 54):
        c.rectangle(x, -22, 20, 80)
        fs(c, WHITE, 5)
    c.rectangle(-105, 58, 210, 20)
    fs(c, LGRAY, 6)


def percent(c):
    circle(c, 0, 0, 72, ORANGE, 6)
    text(c, "%", 0, -2, 100, MARKER, WHITE)


def clock(c, t=0):
    circle(c, 0, 0, 72, WHITE, 7)
    for i in range(12):
        a = i * math.pi / 6
        line(c, 56 * math.cos(a), 56 * math.sin(a), 64 * math.cos(a), 64 * math.sin(a), 5)
    a = t * 2.5
    line(c, 0, 0, 45 * math.sin(a), -45 * math.cos(a), 7)
    line(c, 0, 0, 28 * math.sin(a / 12 + 1), -28 * math.cos(a / 12 + 1), 8)
    circle(c, 0, 0, 7, INK, 0)


def calendar(c, num="30", top=RED, size=72):
    rrect(c, -78, -72, 156, 156, 14)
    fs(c, WHITE, 6)
    c.save()
    rrect(c, -78, -72, 156, 156, 14)
    c.clip()
    c.rectangle(-78, -72, 156, 44)
    rgb(c, top); c.fill()
    c.restore()
    rrect(c, -78, -72, 156, 156, 14)
    rgb(c, INK); c.set_line_width(6); c.stroke()
    for x in (-38, 38):
        rrect(c, x - 6, -86, 12, 30, 5)
        fs(c, DGRAY, 3)
    text(c, num, 0, 28, size, MARKER)


def piggy(c, col=PINK, slot=True):
    for lx in (-50, -15, 30, 60):
        rrect(c, lx - 12, 40, 24, 42, 6)
        fs(c, col, 5)
    c.move_to(-96, -5)
    c.curve_to(-125, -25, -120, 15, -108, 5)
    rgb(c, INK); c.set_line_width(5); c.stroke()
    ellipse(c, 0, 0, 100, 74)
    fs(c, col, 6)
    poly(c, [(22, -62), (40, -100), (60, -55)])
    fs(c, col, 5)
    ellipse(c, 98, 8, 18, 24)
    fs(c, (0.93, 0.5, 0.6), 5)
    circle(c, 93, 2, 3.5, INK, 0)
    circle(c, 103, 2, 3.5, INK, 0)
    circle(c, 55, -18, 7, INK, 0)
    if slot:
        rrect(c, -30, -78, 50, 9, 4)
        rgb(c, INK); c.fill()


def calculator(c, disp="R$ ?"):
    rrect(c, -85, -115, 170, 230, 18)
    fs(c, DGRAY, 6)
    rrect(c, -64, -94, 128, 54, 8)
    fs(c, (0.80, 0.92, 0.76), 4)
    text(c, disp, 0, -68, 30, MARKER)
    for r in range(4):
        for k in range(4):
            col = ORANGE if k == 3 else LGRAY
            rrect(c, -64 + k * 33, -22 + r * 32, 26, 24, 5)
            fs(c, col, 3)


def check_icon(c, r=42):
    circle(c, 0, 0, r, GREEN, 6)
    c.move_to(-r * 0.45, 0)
    c.line_to(-r * 0.1, r * 0.35)
    c.line_to(r * 0.5, -r * 0.35)
    rgb(c, WHITE); c.set_line_width(r * 0.25); c.stroke()


def x_icon(c, r=42):
    circle(c, 0, 0, r, RED, 6)
    k = r * 0.38
    line(c, -k, -k, k, k, r * 0.25, WHITE)
    line(c, -k, k, k, -k, r * 0.25, WHITE)


def big_x(c, s=90, col=RED, lw=20):
    line(c, -s, -s * 0.8, s, s * 0.8, lw, col)
    line(c, -s, s * 0.8, s, -s * 0.8, lw, col)


def qmark(c, size=120, col=INK):
    text(c, "?", 0, 0, size, MARKER, col)


def exclaim(c, size=120, col=RED):
    text(c, "!", 0, 0, size, MARKER, col)


def bulb(c):
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * 0.45
        line(c, 70 * math.cos(a), -20 + 70 * math.sin(a), 92 * math.cos(a), -20 + 92 * math.sin(a), 6, ORANGE)
    circle(c, 0, -20, 46, YELLOW, 6)
    rrect(c, -22, 22, 44, 34, 6)
    fs(c, GRAY, 5)
    line(c, -22, 34, 22, 34, 4)
    line(c, -22, 45, 22, 45, 4)


def sparkle(c, r=30, col=YELLOW):
    k = r * 0.25
    poly(c, [(0, -r), (k, -k), (r, 0), (k, k), (0, r), (-k, k), (-r, 0), (-k, -k)])
    fs(c, col, 4)


def sweat(c, r=12):
    c.move_to(0, -r * 1.8)
    c.curve_to(r * 0.6, -r * 0.6, r, 0, 0, r)
    c.curve_to(-r, 0, -r * 0.6, -r * 0.6, 0, -r * 1.8)
    fs(c, LBLUE, 3)


def cloud_shape(c, w, h, fill=WHITE, lw=7, seed=3):
    rnd = random.Random(seed)
    circles = [(0, 0, None)]
    n = max(10, int((w + h) / 45))
    for i in range(n):
        a = 2 * math.pi * i / n
        r = min(w, h) * (0.16 + 0.04 * rnd.random())
        circles.append((math.cos(a) * (w / 2 - r * 0.7), math.sin(a) * (h / 2 - r * 0.7), r))
    for x, y, r in circles:
        if r is None:
            ellipse(c, 0, 0, w / 2 - 20, h / 2 - 20)
        else:
            c.new_sub_path(); c.arc(x, y, r, 0, 2 * math.pi)
        rgb(c, INK); c.set_line_width(lw * 2); c.stroke()
    for x, y, r in circles:
        if r is None:
            ellipse(c, 0, 0, w / 2 - 20, h / 2 - 20)
        else:
            c.new_sub_path(); c.arc(x, y, r, 0, 2 * math.pi)
        rgb(c, fill); c.fill()


def thought(c, w, h, tx, ty):
    """cloud centered at 0,0 with trailing dots toward (tx,ty) (relative)"""
    for i, k in enumerate((0.55, 0.75, 0.9)):
        r = 22 - i * 6
        x = tx * k
        y = ty * k
        circle(c, x, y, r, WHITE, 6)
    cloud_shape(c, w, h)


def speech(c, w, h, tx, ty, fill=WHITE):
    bx = max(-w / 2 + 40, min(w / 2 - 40, tx * 0.4))
    for pass_ in (0, 1):
        rrect(c, -w / 2, -h / 2, w, h, 36)
        poly(c, [(bx - 50, h / 2 - 6), (tx, ty), (bx + 20, h / 2 - 6)])
        if pass_ == 0:
            rgb(c, INK); c.set_line_width(14); c.stroke()
        else:
            rgb(c, fill); c.fill()


def ribbon(c, s, col=RED, size=58, tcol=WHITE):
    w = text_w(c, s, size) + 80
    h = size * 1.5
    for sx in (-1, 1):
        x0 = sx * (w / 2 - 10)
        poly(c, [(x0, -h / 2 + 18), (x0 + sx * 70, -h / 2 + 18), (x0 + sx * 50, 18), (x0 + sx * 70, h / 2 + 18), (x0, h / 2 + 18)])
        fs(c, tuple(v * 0.75 for v in col), 5)
    rrect(c, -w / 2, -h / 2, w, h, 6)
    fs(c, col, 6)
    text(c, s, 0, 0, size, MARKER, tcol)


def clipboard(c, title="ORÇAMENTO", items=3, checks=True):
    rrect(c, -115, -150, 230, 300, 16)
    fs(c, BROWN, 6)
    c.rectangle(-95, -118, 190, 252)
    fs(c, WHITE, 5)
    rrect(c, -45, -165, 90, 36, 8)
    fs(c, GRAY, 5)
    text(c, title, 0, -84, 30, MARKER)
    for i in range(items):
        y = -30 + i * 55
        c.rectangle(-75, y - 14, 28, 28)
        fs(c, WHITE, 4)
        if checks:
            c.move_to(-70, y)
            c.line_to(-62, y + 9)
            c.line_to(-44, y - 14)
            rgb(c, GREEN); c.set_line_width(6); c.stroke()
        line(c, -30, y, 70, y, 6, GRAY)


def subscribe_btn(c, done=False):
    rrect(c, -230, -62, 460, 124, 22)
    fs(c, GRAY if done else RED, 7)
    text(c, "INSCRITO" if done else "INSCREVA-SE", 0, -2, 54, MARKER, WHITE)


def bell(c):
    c.move_to(-55, 40)
    c.curve_to(-40, 25, -45, -50, 0, -58)
    c.curve_to(45, -50, 40, 25, 55, 40)
    c.close_path()
    fs(c, YELLOW, 6)
    circle(c, 0, 52, 13, YELLOW, 5)
    circle(c, 0, -64, 8, YELLOW, 5)


def cursor(c):
    poly(c, [(0, 0), (0, 70), (17, 54), (30, 82), (42, 76), (29, 49), (52, 48)])
    fs(c, WHITE, 5)


def envelope(c):
    c.rectangle(-90, -55, 180, 110)
    fs(c, WHITE, 6)
    c.move_to(-90, -55)
    c.line_to(0, 10)
    c.line_to(90, -55)
    rgb(c, INK); c.set_line_width(5); c.stroke()


def iceberg(c, t):
    pass


def donut(c, pct, r=230, lw=80, col=RED):
    c.new_sub_path(); c.arc(0, 0, r, 0, 2 * math.pi)
    rgb(c, LGRAY); c.set_line_width(lw); c.stroke()
    if pct > 0.001:
        c.new_sub_path()
        c.arc(0, 0, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * pct)
        rgb(c, col); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_BUTT); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_ROUND)
    for rr in (r - lw / 2, r + lw / 2):
        c.new_sub_path(); c.arc(0, 0, rr, 0, 2 * math.pi)
        rgb(c, INK); c.set_line_width(6); c.stroke()


def speed_lines(c, t, n=5, length=140):
    for i in range(n):
        y = -120 + i * 60
        off = ((t * 900 + i * 137) % 260)
        x = -off
        line(c, x - length, y, x, y, 6, GRAY)


def neq(c, s=60, col=RED, lw=14):
    line(c, -s, -s * 0.3, s, -s * 0.3, lw, col)
    line(c, -s, s * 0.3, s, s * 0.3, lw, col)
    line(c, s * 0.45, -s * 0.85, -s * 0.45, s * 0.85, lw, col)


def eq(c, s=60, col=INK, lw=14):
    line(c, -s, -s * 0.3, s, -s * 0.3, lw, col)
    line(c, -s, s * 0.3, s, s * 0.3, lw, col)


def icon_label(fn, label, size=44, dy=120, col=INK, s=1.0):
    def f(c):
        c.save(); c.scale(s, s); fn(c); c.restore()
        text(c, label, 0, dy, size, HAND, col)
    return f


# ---------------------------------------------------------------- STICK FIGURE
LEN = dict(torso=145, head=52, ua=80, fa=76, th=96, sh=94)

POSES = {
    "stand": dict(rh=(34, 138), lh=(-34, 138)),
    "relax": dict(rh=(42, 118), lh=(-42, 118)),
    "point_r": dict(rh=(156, -10), lh=(-34, 138), rf_="point"),
    "point_ru": dict(rh=(128, -92), lh=(-34, 138), rf_="point"),
    "point_l": dict(lh=(-156, -10), rh=(34, 138), lf_="point"),
    "point_lu": dict(lh=(-128, -92), rh=(34, 138), lf_="point"),
    "think": dict(rh=(-12, -40), rb=1, lh=(-26, 112)),
    "think_l": dict(lh=(12, -40), lb=-1, rh=(26, 112)),
    "hips": dict(rh=(26, 112), lh=(-26, 112)),
    "shrug": dict(rh=(92, -34), rb=1, lh=(-92, -34), lb=-1),
    "arms_up": dict(rh=(64, -140), rb=1, lh=(-64, -140), lb=-1),
    "head": dict(rh=(26, -98), rb=1, lh=(-26, -98), lb=-1),
    "thumb": dict(rh=(96, -40), rb=1, lh=(-34, 138), rf_="thumb"),
    "finger_up": dict(rh=(66, -110), rb=1, lh=(-26, 112), rf_="point_up"),
    "present": dict(rh=(140, 36), rb=1, lh=(-34, 138)),
    "present_l": dict(lh=(-140, 36), lb=-1, rh=(34, 138)),
    "wave": dict(rh=(88, -120), rb=1, lh=(-34, 138), wave=True),
    "hold": dict(rh=(48, 50), lh=(-48, 50)),
    "run": dict(rh=(34, 138), lh=(-34, 138), run=True),
}
LEGS = dict(rf=(30, 186), lf=(-30, 186))


def _ik(sx, sy, tx, ty, l1, l2, bend):
    dx, dy = tx - sx, ty - sy
    d = math.hypot(dx, dy)
    d = max(abs(l1 - l2) + 1, min(d, l1 + l2 - 0.5))
    a = math.atan2(dy, dx)
    cosv = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    al = math.acos(max(-1, min(1, cosv)))
    ex = sx + l1 * math.cos(a + bend * al)
    ey = sy + l1 * math.sin(a + bend * al)
    hx = sx + d * math.cos(a)
    hy = sy + d * math.sin(a)
    return (ex, ey), (hx, hy)


def _pose(name):
    p = dict(rb=-1, lb=1)
    p.update(LEGS)
    p.update(POSES[name])
    return p


def pose_at(t, keys, blend=0.32):
    """keys: list of (time, posename). returns interpolated pose dict"""
    cur = keys[0]
    prev = None
    for k in keys:
        if t >= k[0]:
            prev = cur if k is not keys[0] else None
            cur = k
    # find previous key
    idx = keys.index(cur)
    pc = _pose(cur[1])
    if idx == 0:
        return pc
    pp = _pose(keys[idx - 1][1])
    p = ease_io(prog(t, cur[0], blend))
    if p >= 1:
        return pc
    out = dict(pc)
    for k in ("rh", "lh", "rf", "lf"):
        a, b = pp[k], pc[k]
        out[k] = (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)
    if p < 0.5:
        for k in ("rb", "lb", "rf_", "lf_"):
            out[k] = pp.get(k)
    return out


def val_at(t, keys):
    v = keys[0][1]
    for k in keys:
        if t >= k[0]:
            v = k[1]
    return v


def face(c, expr, t, fid, look=0.0, r=52):
    ink = INK
    lx = look * 6
    blink = ((t * 1000 + fid * 1777) % 4100) < 130
    ey = -6
    big = expr in ("shocked", "desperate")
    # eyes
    for sx in (-1, 1):
        x = sx * 17 + lx
        if blink:
            line(c, x - 7, ey, x + 7, ey, 4.5)
        else:
            ellipse(c, x, ey + (-3 if expr == "think" else 0), 7.5 if big else 6.5, 11 if big else 9.5)
            rgb(c, ink); c.fill()
    c.set_line_width(5)
    rgb(c, ink)
    # brows
    if expr in ("worried", "desperate", "sad"):
        for sx in (-1, 1):
            c.move_to(sx * 30 + lx, -22)
            c.line_to(sx * 9 + lx, -31)
        c.stroke()
    elif expr == "shocked":
        for sx in (-1, 1):
            c.new_sub_path()
            c.arc(sx * 17 + lx, -16, 13, math.pi * 1.2, math.pi * 1.8)
        c.stroke()
    elif expr == "think":
        c.move_to(-28 + lx, -26); c.line_to(-8 + lx, -24)
        c.stroke()
        c.new_sub_path(); c.arc(17 + lx, -22, 12, math.pi * 1.15, math.pi * 1.85)
        c.stroke()
    elif expr == "angry":
        for sx in (-1, 1):
            c.move_to(sx * 30 + lx, -30)
            c.line_to(sx * 8 + lx, -21)
        c.stroke()
    elif expr == "confident":
        c.move_to(-28 + lx, -24); c.line_to(-8 + lx, -26)
        c.stroke()
        c.new_sub_path(); c.arc(17 + lx, -24, 12, math.pi * 1.15, math.pi * 1.85)
        c.stroke()
    # mouth
    mx = lx * 0.6
    if expr in ("happy", "confident"):
        c.new_sub_path(); c.arc(mx, 8, 21, math.radians(25), math.radians(155)); c.stroke()
    elif expr == "grin":
        c.new_sub_path()
        c.arc(mx, 12, 22, 0, math.pi)
        c.close_path()
        rgb(c, ink); c.fill()
    elif expr == "neutral":
        line(c, mx - 12, 24, mx + 12, 24, 5)
    elif expr in ("worried", "sad"):
        c.new_sub_path(); c.arc(mx, 40, 17, math.radians(205), math.radians(335)); c.stroke()
    elif expr == "shocked":
        ellipse(c, mx, 25, 10, 14); rgb(c, ink); c.fill()
    elif expr == "desperate":
        poly(c, [(mx - 20, 30), (mx - 12, 14), (mx + 12, 14), (mx + 20, 30)])
        rgb(c, ink); c.fill()
    elif expr == "think":
        line(c, mx - 4, 26, mx + 16, 20, 5)
    elif expr == "angry":
        line(c, mx - 14, 26, mx + 14, 26, 5)
    # sweat
    if expr in ("desperate", "shocked"):
        ph = (t * 0.9 + fid * 0.3) % 1.0
        c.save()
        c.translate(-r - 8, -10 + ph * 40)
        c.push_group()
        sweat(c, 11)
        c.pop_group_to_source()
        c.paint_with_alpha(1 - ph)
        c.restore()


def figure(c, t, x, y, s=1.0, poses=((0, "stand"),), exprs=((0, "happy"),), look=0.0, shirt=YELLOW,
           hair="tuft", fid=0, appear=None, flip_look=None, outfit=None):
    """draw stick figure with feet on ground y. poses/exprs are keyframe lists of (time, name)."""
    a_scale = 1.0
    if appear is not None:
        cue(appear, "appear")
        if t < appear:
            return
        a_scale = ease_out_back(prog(t, appear, 0.45))
        if a_scale < 0.02:
            return
    P = pose_at(t, list(poses))
    expr = val_at(t, list(exprs))
    if callable(look):
        look = look(t)
    c.save()
    c.translate(x, y)
    c.scale(s * a_scale, s * a_scale)
    rnd = random.Random(int(t * 8) * 31 + fid * 977)
    J = lambda: (rnd.uniform(-1.4, 1.4), rnd.uniform(-1.4, 1.4))
    bob = math.sin(t * 2.3 + fid) * 2.2
    run = P.get("run")
    # shadow
    ellipse(c, 0, 4, 85, 12)
    rgb(c, INK, 0.08); c.fill()

    hip = (0, -(LEN["th"] + LEN["sh"] - 4) + bob)
    rf, lf = P["rf"], P["lf"]
    rh, lh = P["rh"], P["lh"]
    lean = 0
    if run:
        ph = t * 11
        hip = (0, hip[1] + abs(math.sin(ph)) * -10)
        rf = (30 + 70 * math.sin(ph), 186 - 40 * max(0, math.cos(ph)))
        lf = (-30 - 70 * math.sin(ph), 186 - 40 * max(0, -math.cos(ph)))
        rh = (-20 + 70 * math.sin(ph), 96)
        lh = (20 - 70 * math.sin(ph), 96)
        lean = 0.12
    if P.get("wave"):
        rh = (rh[0] + math.sin(t * 9) * 26, rh[1])
    neck = (hip[0] + math.sin(lean) * LEN["torso"], hip[1] - math.cos(lean) * LEN["torso"])
    sh = (neck[0] - math.sin(lean) * 16, neck[1] + 16)
    head = (neck[0] + math.sin(lean) * (LEN["head"] + 12), neck[1] - (LEN["head"] + 12))

    lw = 9
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_line_join(cairo.LINE_JOIN_ROUND)

    def limb(origin, tgt, l1, l2, bend, foot=None, fing=None, side=1):
        j1, j2 = J(), J()
        (ex, ey), (hx, hy) = _ik(origin[0], origin[1], origin[0] + tgt[0], origin[1] + tgt[1], l1, l2, bend)
        ex += j1[0]; ey += j1[1]; hx += j2[0]; hy += j2[1]
        c.move_to(*origin); c.line_to(ex, ey); c.line_to(hx, hy)
        rgb(c, INK); c.set_line_width(lw); c.stroke()
        if foot:
            ellipse(c, hx + side * 14, hy + 2, 22, 9)
            rgb(c, INK); c.fill()
        else:
            circle(c, hx, hy, 9.5, INK, 0)
            a = math.atan2(hy - ey, hx - ex)
            if fing == "point":
                line(c, hx, hy, hx + 26 * math.cos(a), hy + 26 * math.sin(a), 6)
            elif fing == "thumb":
                line(c, hx, hy, hx, hy - 26, 7)
            elif fing == "point_up":
                line(c, hx, hy, hx, hy - 28, 6)
        return hx, hy

    # legs
    limb(hip, rf, LEN["th"], LEN["sh"], -1, foot=True, side=1)
    limb(hip, lf, LEN["th"], LEN["sh"], 1, foot=True, side=-1)
    # torso / shirt
    if shirt is not None:
        perp = (math.cos(lean), math.sin(lean))
        top = (neck[0] - math.sin(lean) * 8, neck[1] + 8)
        bot = (hip[0] - math.sin(lean) * -16, hip[1] + 16)
        pts = [(top[0] - perp[0] * 32, top[1] - perp[1] * 32), (top[0] + perp[0] * 32, top[1] + perp[1] * 32),
               (bot[0] + perp[0] * 44, bot[1] + perp[1] * 44), (bot[0] - perp[0] * 44, bot[1] - perp[1] * 44)]
        c.move_to(*pts[0])
        c.line_to(*pts[1])
        c.line_to(*pts[2])
        c.line_to(*pts[3])
        c.close_path()
        fs(c, shirt, 7)
        if outfit:
            _torso_outfit(c, outfit, top, bot, perp)
    else:
        c.move_to(*hip); c.line_to(*neck)
        rgb(c, INK); c.set_line_width(lw); c.stroke()
    # neck
    line(c, neck[0], neck[1], head[0], head[1] + LEN["head"] - 2, lw)
    # head
    hj = J()
    c.save()
    c.translate(head[0] + hj[0], head[1] + hj[1])
    c.rotate(lean * 0.6)
    circle(c, 0, 0, LEN["head"], WHITE, lw)
    if hair == "tuft":
        c.set_line_width(5); rgb(c, INK)
        for i in range(3):
            c.move_to(-4 + i * 13, -LEN["head"] + 2)
            c.curve_to(-2 + i * 13, -LEN["head"] - 14, 6 + i * 13, -LEN["head"] - 18, 14 + i * 13, -LEN["head"] - 14)
        c.stroke()
    elif hair == "spiky":
        c.set_line_width(5); rgb(c, INK)
        for i in range(5):
            a = -math.pi / 2 + (i - 2) * 0.28
            c.move_to(math.cos(a) * 50, math.sin(a) * 50)
            c.line_to(math.cos(a) * 68, math.sin(a) * 68)
        c.stroke()
    elif hair == "long":
        c.new_sub_path()
        c.arc(0, -4, LEN["head"] + 6, math.pi * 0.95, math.pi * 2.05)
        rgb(c, INK); c.set_line_width(14); c.stroke()
    face(c, expr, t, fid, look)
    if outfit:
        _head_outfit(c, outfit, look)
    c.restore()
    # arms
    perp = (math.cos(lean), math.sin(lean))
    rsh = (sh[0] + perp[0] * 26, sh[1] + perp[1] * 26)
    lsh = (sh[0] - perp[0] * 26, sh[1] - perp[1] * 26)
    rhand = limb(rsh, rh, LEN["ua"], LEN["fa"], P.get("rb", -1) or -1, fing=P.get("rf_"))
    lhand = limb(lsh, lh, LEN["ua"], LEN["fa"], P.get("lb", 1) or 1, fing=P.get("lf_"))
    if outfit and outfit.get("prop"):
        side, fn = outfit["prop"]
        hx, hy = lhand if side == "l" else rhand
        c.save(); c.translate(hx, hy); fn(c, t, P); c.restore()
    c.restore()


# ---------------------------------------------------------------- figurino de personagem fixo
def _torso_outfit(c, o, top, bot, perp):
    tx, ty = top; bx, by = bot
    def at(k, w):  # ponto no torso: k=0 topo, 1 base; w = deslocamento lateral
        x = tx + (bx - tx) * k + perp[0] * w
        y = ty + (by - ty) * k + perp[1] * w
        return x, y
    if o.get("vest"):
        for sx in (-1, 1):
            poly(c, [at(0, sx * 32), at(0.02, sx * 14), at(0.55, sx * 4), at(1.0, sx * 6), at(1.0, sx * 44)])
            fs(c, o["vest"], 6)
        for k in (0.62, 0.78, 0.92):
            circle(c, *at(k, 9), 4.5, INK, 0)
    if o.get("suspenders"):
        for sx in (-1, 1):
            line(c, *at(0, sx * 22), *at(1.0, sx * 26), 9, o["suspenders"])
            circle(c, *at(0.97, sx * 26), 5, LGRAY if "LGRAY" in globals() else WHITE, 2)
    if o.get("collar"):
        for sx in (-1, 1):
            poly(c, [at(0, 0), at(0, sx * 22), at(0.12, sx * 14)])
            fs(c, WHITE, 4)
    if o.get("tie"):
        poly(c, [at(0.02, -7), at(0.02, 7), at(0.09, 5), at(0.09, -5)]); fs(c, o["tie"], 4)
        poly(c, [at(0.09, -5), at(0.09, 5), at(0.62, 10), at(0.70, 0), at(0.62, -10)]); fs(c, o["tie"], 4)
    if o.get("bowtie"):
        cx, cy = at(0.03, 0)
        for sx in (-1, 1):
            poly(c, [(cx, cy), (cx + sx * 22, cy - 12), (cx + sx * 22, cy + 12)]); fs(c, o["bowtie"], 4)
        circle(c, cx, cy, 6, o["bowtie"], 3)
    if o.get("badge"):
        cx, cy = at(0.35, -20)
        circle(c, cx, cy, 13, o["badge"], 4)
        text(c, "$", cx, cy - 1, 18, MARKER, INK)


def _head_outfit(c, o, look):
    r = LEN["head"]
    hair = o.get("hair")
    if hair == "side":
        c.move_to(-r + 4, -18); c.curve_to(-r + 6, -r - 6, 10, -r - 22, r - 6, -r + 14)
        c.curve_to(10, -r + 4, -20, -r + 10, -r + 4, -18)
        fs(c, (0.25, 0.18, 0.12), 5)
    g = o.get("glasses")
    lx = look * 6
    if g == "rect":
        for sx in (-1, 1):
            rrect(c, sx * 17 + lx - 15, -18, 30, 22, 6)
            rgb(c, INK); c.set_line_width(4.5); c.stroke()
        line(c, -2 + lx, -10, 2 + lx, -10, 4)
    elif g == "round":
        for sx in (-1, 1):
            circle(c, sx * 17 + lx, -6, 14, None, 4.5)
        line(c, -3 + lx, -8, 3 + lx, -8, 4)
    h = o.get("hat")
    hc = o.get("hat_col", GREEN)
    if h == "cap":
        c.new_sub_path(); c.arc(0, -r + 26, r - 2, math.pi * 1.0, math.pi * 2.0); c.close_path()
        fs(c, hc, 6)
        c.move_to(r - 10, -r + 22); c.curve_to(r + 30, -r + 18, r + 46, -r + 26, r + 50, -r + 34)
        c.line_to(r - 6, -r + 34); c.close_path()
        fs(c, tuple(v * 0.8 for v in hc), 5)
        circle(c, 0, -2 * r + 26, 6, hc, 4)
        if o.get("hat_logo"):
            text(c, o["hat_logo"], -4, -r - 2, 26, MARKER, INK)


def prop_calculator(c, t, P):
    c.save(); c.translate(0, 18); c.scale(0.32, 0.32); calculator(c, "R$"); c.restore()


def prop_coin(c, t, P):
    c.save(); c.translate(0, -16); c.rotate(math.sin(t * 3) * 0.3); c.scale(0.5, 0.5); coin(c); c.restore()


def prop_pointer(c, t, P):
    line(c, 0, 0, 60, -70, 6, BROWN)
    circle(c, 60, -70, 6, RED, 0)


def prop_tablet(c, t, P):
    c.save(); c.translate(0, 10); c.rotate(-0.15)
    rrect(c, -34, -46, 68, 92, 8); fs(c, DGRAY, 5)
    c.rectangle(-26, -38, 52, 70); rgb(c, (0.85, 0.95, 0.88)); c.fill()
    c.move_to(-20, 20); c.line_to(-6, 4); c.line_to(6, 12); c.line_to(20, -20)
    rgb(c, GREEN); c.set_line_width(5); c.stroke()
    c.restore()


def head_top(y, s):
    """approx y of top of head for a figure with feet at y"""
    return y - s * (LEN["th"] + LEN["sh"] + LEN["torso"] + 2 * LEN["head"] + 12)


# ---------------------------------------------------------------- SCENE HELPERS
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


