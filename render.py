#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page to a PNG file.

Pure Pillow drawing: no network, no clock, no randomness. Running it
twice writes byte-identical output. `build(path)` renders straight to
the path it is given, so a read-only repository is never written to;
the entrypoint main.py hands it the harness output directory.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (250, 246, 236)
INK = (22, 26, 33)
GREEN = (18, 53, 36)
GREEN_DARK = (11, 36, 24)
GOLD = (184, 134, 11)
GOLD_LIGHT = (212, 175, 55)
RED = (178, 34, 34)
RED_DARK = (139, 0, 0)
GRAY = (100, 106, 114)
LIGHT = (236, 231, 219)
BLUE = (36, 83, 140)
SKY = (168, 205, 235)
TEAL = (15, 118, 110)
WHITE = (255, 255, 255)
CREAM = (247, 240, 224)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
REG = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(f.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def letterspaced(draw, x, y, s, f, fill, tracking=3):
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ------------------------------------------------------------------ art
def globe(draw, cx, cy, r):
    """A cracked globe: blue disc, meridians, green land blobs, red crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY,
                 outline=BLUE, width=4)
    for k in (-0.55, 0.0, 0.55):
        draw.ellipse([cx - r * 0.45 + k * r * 0.55, cy - r,
                      cx + r * 0.45 + k * r * 0.55, cy + r],
                     outline=(120, 170, 210), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(120, 170, 210), width=2)
    draw.ellipse([cx - r * 0.75, cy - r * 0.62, cx - r * 0.18, cy - r * 0.12],
                 fill=(96, 160, 90))
    draw.ellipse([cx + r * 0.05, cy + r * 0.08, cx + r * 0.72, cy + r * 0.58],
                 fill=(96, 160, 90))
    draw.ellipse([cx - r * 0.28, cy + r * 0.30, cx + r * 0.18, cy + r * 0.72],
                 fill=(120, 175, 105))
    crack = [(cx - r * 0.30, cy - r * 0.85), (cx - r * 0.05, cy - r * 0.45),
             (cx - r * 0.28, cy - r * 0.10), (cx + r * 0.10, cy + r * 0.25),
             (cx - r * 0.12, cy + r * 0.60), (cx + r * 0.22, cy + r * 0.92)]
    draw.line(crack, fill=RED, width=5, joint="curve")


def stamp(img, cx, cy, text):
    """A tilted red NO DEAL stamp pasted onto the image."""
    pad = 16
    f = BOLD(30)
    tmp = Image.new("RGBA", (420, 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    tw = d.textlength(text, font=f)
    d.rectangle([pad, pad, pad + tw + 28, pad + 54], outline=RED, width=5)
    d.text((pad + 14, pad + 12), text, font=f, fill=RED)
    rot = tmp.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.paste(rot, (int(cx - rot.width // 2), int(cy - rot.height // 2)), rot)


def chart_icon(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=TEAL)
    draw.line([x + 10, y + s - 12, x + s - 10, y + s - 12],
              fill=WHITE, width=3)
    for i, h in enumerate((58, 46, 34, 22)):
        bx = x + 12 + i * 20
        draw.rectangle([bx, y + s - 14 - h, bx + 13, y + s - 14], fill=WHITE)
    draw.line([x + 10, y + 16, x + s - 12, y + s - 26], fill=RED, width=4)


def flats_icon(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(90, 70, 60))
    for bx, bw, bh in ((10, 26, 52), (42, 26, 66), (74, 18, 44)):
        draw.rectangle([x + bx, y + s - 12 - bh, x + bx + bw, y + s - 12],
                       fill=(210, 200, 185))
    for wx in (16, 48):
        for wy in (y + s - 58, y + s - 40):
            draw.rectangle([x + wx, wy, x + wx + 10, wy + 10], fill=RED)


def ship_icon(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=BLUE)
    draw.polygon([(x + 12, y + s - 34), (x + s - 12, y + s - 34),
                  (x + s - 24, y + s - 16), (x + 24, y + s - 16)],
                 fill=WHITE)
    draw.line([x + s // 2, y + 14, x + s // 2, y + s - 34], fill=WHITE, width=4)
    draw.polygon([(x + s // 2, y + 14), (x + s // 2 + 22, y + 30),
                  (x + s // 2, y + 30)], fill=RED)
    for i, yy in enumerate((y + s - 12, y + s - 6)):
        draw.line([x + 8, yy, x + s - 8, yy], fill=SKY, width=2)


# ------------------------------------------------------------------ page
def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 98], fill=GREEN)
    d.rectangle([0, 98, W, 102], fill=GOLD)
    letterspaced(d, 36, 14, "THE WORLD IN ONE DAY", BOLD(19), GOLD_LIGHT,
                 tracking=5)
    d.text((36, 38), "MONDAY, 23 NOVEMBER 2026", font=BOLD(46), fill=WHITE)
    d.text((W - 36 - text_w(d, "No. 327", BOLD(20)), 20), "No. 327",
           font=BOLD(20), fill=GOLD_LIGHT)

    # ---- hero: COP31 collapses
    d.text((36, 120), "TOP STORY  —  CLIMATE  ·  ANTALYA, TURKEY",
           font=BOLD(19), fill=RED)
    d.text((36, 146), "COP31 COLLAPSES", font=BOLD(72), fill=INK)
    d.text((36, 218),
           "No deal in Antalya — fossil fuels cut from the pact",
           font=BOLD(24), fill=INK)
    y = draw_wrapped(
        d, 36, 254,
        "After two weeks of talks and record overtime, the UN climate "
        "summit ended on Sunday with no deal — the first COP to fail "
        "since 2009. The EU and about 130 countries refused a text that "
        "never mentioned fossil fuels.",
        REG(21), 600, INK, leading=26, max_lines=4)
    y += 10
    for i, chip in enumerate(("LONGEST COP EVER", "FIRST FAILURE SINCE 2009",
                              "US ABSENT")):
        cx = 36 + i * 204
        d.rounded_rectangle([cx, y, cx + 196, y + 34], radius=17,
                            outline=RED, width=2)
        d.text((cx + 98 - text_w(d, chip, BOLD(12)) / 2, y + 10), chip,
               font=BOLD(12), fill=RED_DARK)
    globe(d, 838, 268, 92)
    stamp(img, 838, 372, "NO DEAL")

    # ---- divider
    d.line([36, 410, W - 36, 410], fill=GOLD, width=3)

    # ---- left column: markets
    lx, lw = 36, 452
    d.text((lx, 424), "MARKETS  —  THE AI SELL-OFF", font=BOLD(19), fill=RED)
    y = draw_wrapped(
        d, lx, 450,
        "Wall Street's AI rout spread across Asia. The S&P 500 fell 3.7% "
        "into correction; the Nikkei slid 5.1% to a seven-month low.",
        REG(20), lw, INK, leading=25, max_lines=3)
    y += 10
    d.text((lx, y), "CLOSES  —  FRIDAY 20 NOV", font=BOLD(16), fill=GRAY)
    y += 26
    rows = (("S&P 500", "6,910.39", "-3.70%"),
            ("Nasdaq", "22,617.73", "-5.28%"),
            ("Dow Jones", "48,147.33", "-1.93%"),
            ("Nikkei 225", "56,436.65", "-5.06%"),
            ("Kospi", "4,869.96", "-5.21%"))
    for name, close, chg in rows:
        d.text((lx, y), name, font=BOLD(21), fill=INK)
        d.text((lx + lw - 118 - text_w(d, close, REG(21)), y), close,
               font=REG(21), fill=INK)
        d.text((lx + lw - text_w(d, chg, BOLD(21)), y), chg,
               font=BOLD(21), fill=RED)
        y += 32
    y += 4
    y = draw_wrapped(
        d, lx, y,
        "Tokyo was shut on Monday for a holiday; futures point lower "
        "for Tuesday.",
        REG(16), lw, GRAY, leading=20, max_lines=2)

    # ---- right column: war
    rx, rw = 536, 452
    d.text((rx, 424), "WAR  —  UKRAINE & THE GULF", font=BOLD(19), fill=RED)
    y = 448
    flats_icon(d, rx, y, 84)
    draw_wrapped(d, rx + 98, y, "Strike on Dymer kills 10",
                 BOLD(24), rw - 98, INK, leading=28, max_lines=2)
    y = draw_wrapped(
        d, rx, 542,
        "A Russian strike hit a block of flats in Dymer, north of Kyiv. "
        "At least 10 people were killed; a seven-year-old boy was pulled "
        "alive from the rubble.",
        REG(20), rw, INK, leading=25, max_lines=3)
    y += 12
    ship_icon(d, rx, y, 84)
    draw_wrapped(d, rx + 98, y, "Russian warship sinks",
                 BOLD(24), rw - 98, INK, leading=28, max_lines=2)
    y = draw_wrapped(
        d, rx, y + 92,
        "The corvette Merkury went down at Benghazi after a suspected "
        "Ukrainian sea-drone attack, Libyan officials said.",
        REG(20), rw, INK, leading=25, max_lines=3)

    # ---- bottom strip: four more stories
    d.rectangle([0, 812, W, 950], fill=GREEN_DARK)
    d.rectangle([0, 812, W, 816], fill=GOLD)
    items = (
        ("WASHINGTON", "Democrats take 258 House seats — their biggest "
         "majority since 1992"),
        ("SHENZHEN", "Trump, Putin and Xi issue a Declaration toward Peace"),
        ("SINALOA", "FBI most-wanted cartel boss El Chapo Isidro captured"),
        ("HORMUZ", "Two tankers ablaze near the Strait of Hormuz"),
    )
    for i, (label, text) in enumerate(items):
        x = 36 + i * 242
        d.text((x, 830), label, font=BOLD(15), fill=GOLD_LIGHT)
        draw_wrapped(d, x, 854, text, REG(18), 226, WHITE, leading=22,
                     max_lines=4)

    # ---- footer
    d.text((36, 966),
           "MONDAY 23 NOVEMBER 2026  ·  Market closes are Friday 20 November — "
           "the Monday US session had not closed at press time.",
           font=REG(15), fill=GRAY)
    d.text((36, 990),
           "Sources: CNN, Reuters, AP, Al Jazeera  ·  COP31: Antalya, Turkey  ·  "
           "South Korea's exports topped $1 trillion for the first time.",
           font=REG(15), fill=GRAY)

    img.save(path, "PNG")


if __name__ == "__main__":
    # Local run only: write the pre-rendered copy next to this file.
    # The grader never runs this path; it runs main.py instead.
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png"))
