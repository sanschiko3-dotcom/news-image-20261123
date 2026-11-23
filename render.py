"""Render 'The World Today' — 23 November 2026 front page, 1024x1024.

Deterministic: no clock, no randomness, no network, fixed geometry.
Writes assets/entry.png and prints its size + sha256.
"""

import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")

PAPER = "#f6f1e4"
INK = "#191919"
RED = "#a41220"
NAVY = "#1e2c3c"
GOLD = "#b57f24"
GREY = "#6b655a"
DIVIDER = "#c0b7a3"
PALE = "#dfe5ea"
ORANGE = "#e07b2a"
SMOKE = "#8a8a86"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((30, 12), "THE WORLD TODAY", font=SERIF_B(62), fill=INK)
    d.text((32, 90), "MONDAY, 23 NOVEMBER 2026", font=SANS_B(19), fill=INK)
    d.text((32, 118), "Six stories that shaped the day, in one page.",
           font=SANS(16), fill=GREY)
    d.line([(30, 146), (994, 146)], fill=RED, width=3)
    d.line([(30, 152), (994, 152)], fill=INK, width=1)

    # ---- Hero: text column (left, width 640) ----
    d.text((30, 168), "CLIMATE TALKS COLLAPSE", font=SANS_B(20), fill=RED)
    hl = wrap(d, "COP31 FAILS AS CLIMATE TALKS END WITHOUT A DEAL",
              SERIF_B(40), 640)
    y = draw_lines(d, hl, 30, 194, SERIF_B(40), INK, 47)
    deck1 = wrap(d, "EU and others reject any deal without language on a "
                    "fossil-fuel phase-out; talks expose deep divisions.",
                 SANS(19), 640)
    y = draw_lines(d, deck1, 30, y + 8, SANS(19), INK, 24)
    deck2 = wrap(d, "UN climate negotiations end with no overarching "
                    "agreement on tackling climate change.",
                 SANS(18), 640)
    draw_lines(d, deck2, 30, y + 6, SANS(18), INK, 23)

    # ---- Hero: illustration box (right) ----
    d.rectangle([(700, 168), (994, 428)], fill=NAVY)
    cx, cy, r = 847, 282, 82
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=PALE)
    # longitude / latitude lines on the globe
    for k in (-1, 0, 1):
        hw = 38 - abs(k) * 20
        d.ellipse([(cx - hw, cy - r), (cx + hw, cy + r)],
                  outline=NAVY, width=1)
    d.line([(cx - r, cy - 40), (cx + r, cy - 40)], fill=NAVY, width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=1)
    d.line([(cx - r, cy + 40), (cx + r, cy + 40)], fill=NAVY, width=1)
    # cracks: two thin pale zigzags over the globe
    d.line([(800, 240), (818, 258), (806, 272), (826, 290)], fill="#ffffff",
           width=2)
    d.line([(880, 230), (866, 250), (880, 264), (864, 284)], fill="#ffffff",
           width=2)
    # smoke: three layered grey ellipses over the lower half of the globe
    d.ellipse([(cx - 96, cy + 6), (cx - 6, cy + 52)], fill=SMOKE)
    d.ellipse([(cx - 30, cy + 18), (cx + 66, cy + 62)], fill="#7d7d79")
    d.ellipse([(cx + 30, cy + 2), (cx + 100, cy + 44)], fill=SMOKE)
    # small red-orange sun with short rays, top-right corner of the box
    sx, sy, sr = 962, 196, 14
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0),
                   (-1, -1), (1, -1), (-1, 1), (1, 1)):
        d.line([(sx + dx * (sr + 3), sy + dy * (sr + 3)),
                (sx + dx * (sr + 9), sy + dy * (sr + 9))],
               fill=ORANGE, width=2)
    d.ellipse([(sx - sr, sy - sr), (sx + sr, sy + sr)], fill="#d84a1f")
    d.text((716, 376), "COP31 · ANTALYA", font=SANS_B(17), fill="#ffffff")
    d.text((716, 400), "No deal on fossil fuels", font=SANS(14), fill=PALE)
    d.line([(30, 448), (994, 448)], fill=RED, width=2)

    # ---- Grid: six stories, 3 cols x 2 rows ----
    cols = [30, 358, 686]
    rows = [466, 624]
    stories = [
        ("rocket", NAVY,
         "HOUTHIS HIT SAUDI REFINERY",
         "Houthis claim strikes on a Saudi oil refinery; "
         "at least 6 injured."),
        ("ship", NAVY,
         "RUSSIAN SHIP BLAST IN LIBYA",
         "Blast on a Russian ship at Benghazi port; officials "
         "suspect a drone."),
        ("capitol", NAVY,
         "DEMOCRATS TAKE HOUSE",
         "Largest House majority since 1992 after flipping a "
         "North Carolina seat."),
        ("heart", GOLD,
         "BOY, 7, PULLED ALIVE",
         "Rescued from rubble hours after a Russian strike on Ukraine."),
        ("tennis", GOLD,
         "ALCARAZ WINS ATP FINALS",
         "First ATP Finals title, beating Alexander Zverev."),
        ("flag", NAVY,
         "VERSTAPPEN WINS IN VEGAS",
         "Max Verstappen wins the Las Vegas Grand Prix."),
    ]
    for i, (kind, color, head, deck) in enumerate(stories):
        x = cols[i % 3]
        y0 = rows[i // 3]
        draw_pictogram(d, kind, color, x, y0 + 2)
        hl = wrap(d, head, SERIF_B(21), 304)
        draw_lines(d, hl, x, y0 + 44, SERIF_B(21), INK, 25)
        dl = wrap(d, deck, SANS(17), 304)
        draw_lines(d, dl, x, y0 + 100, SANS(17), INK, 21)
    for vx in (346, 674):
        d.line([(vx, 466), (vx, 774)], fill=DIVIDER, width=1)
    d.line([(30, 616), (994, 616)], fill=DIVIDER, width=1)

    # ---- Also today ----
    d.line([(30, 790), (994, 790)], fill=RED, width=2)
    d.text((30, 804), "ALSO TODAY", font=SANS_B(17), fill=RED)
    left = wrap(d, "FIFA to confirm UK as 2035 Women's World Cup host · "
                   "Indonesia factory fire kills 3, dozens missing · "
                   "M6.5 quake strikes Vanuatu", SANS(17), 470)
    draw_lines(d, left, 30, 830, SANS(17), INK, 21)
    right = wrap(d, "Japan jolted by a 6.1 quake · Pant century in India v "
                    "New Zealand Test · Nepal PM Balen Shah visits India",
                 SANS(17), 470)
    draw_lines(d, right, 524, 830, SANS(17), INK, 21)

    # ---- Footer ----
    d.line([(30, 964), (994, 964)], fill=DIVIDER, width=1)
    d.text((30, 976), "Sources: BBC, Reuters, The Hindu, Indian Express · "
                      "23 November 2026", font=SANS(14), fill=GREY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    data = open(OUT, "rb").read()
    print("wrote %s (%d bytes) sha256=%s"
          % (OUT, len(data), hashlib.sha256(data).hexdigest()))


def draw_pictogram(d, kind, color, x, y):
    """Flat pictogram inside a 46x34 box at (x, y)."""
    if kind == "rocket":
        d.polygon([(x + 14, y + 26), (x + 26, y + 6), (x + 32, y + 12),
                   (x + 22, y + 30)], fill=color)
        d.polygon([(x + 14, y + 26), (x + 8, y + 30), (x + 16, y + 32)],
                  fill=ORANGE)
        d.polygon([(x + 30, y + 20), (x + 38, y + 14), (x + 36, y + 24)],
                  fill=ORANGE)
    elif kind == "ship":
        d.polygon([(x + 6, y + 20), (x + 40, y + 20), (x + 34, y + 30),
                   (x + 12, y + 30)], fill=color)
        d.rectangle([(x + 20, y + 12), (x + 26, y + 20)], fill=color)
        d.polygon([(x + 22, y + 4), (x + 26, y + 10), (x + 30, y + 4),
                   (x + 26, y + 14), (x + 20, y + 8)], fill=ORANGE)
    elif kind == "capitol":
        d.polygon([(x + 4, y + 12), (x + 23, y + 2), (x + 42, y + 12)],
                  fill=color)
        for cx in (10, 20, 30):
            d.rectangle([(x + cx, y + 14), (x + cx + 4, y + 26)], fill=color)
        d.rectangle([(x + 4, y + 27), (x + 42, y + 31)], fill=color)
    elif kind == "heart":
        d.ellipse([(x + 8, y + 8), (x + 22, y + 22)], fill=color)
        d.ellipse([(x + 22, y + 8), (x + 36, y + 22)], fill=color)
        d.polygon([(x + 10, y + 16), (x + 34, y + 16), (x + 22, y + 32)],
                  fill=color)
    elif kind == "tennis":
        d.ellipse([(x + 8, y + 2), (x + 38, y + 32)], fill=color)
        d.arc([(x + 2, y + 2), (x + 30, y + 32)], 300, 60,
              fill="#ffffff", width=2)
        d.arc([(x + 14, y + 2), (x + 42, y + 32)], 120, 240,
              fill="#ffffff", width=2)
    elif kind == "flag":
        d.rectangle([(x + 4, y + 4), (x + 6, y + 32)], fill=color)
        for r in range(3):
            for c in range(4):
                if (r + c) % 2 == 0:
                    d.rectangle([(x + 8 + c * 8, y + 4 + r * 8),
                                 (x + 15 + c * 8, y + 11 + r * 8)],
                                fill=color)


if __name__ == "__main__":
    main()
