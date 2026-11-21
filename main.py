#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Saturday, November 21, 2026.

Draws a one-image summary of the world news of Saturday 21 November 2026
as a newspaper front page, entirely in code: an embedded 5x7 bitmap font,
canvas primitives and a hand-rolled PNG writer (zlib + struct).

Python 3 standard library only. No network access.
Writes /output/entry.png (falls back to ./entry.png).
Deterministic: every run produces byte-identical output.
"""
import os
import struct
import zlib

W = H = 1024

PAPER = (243, 238, 226)
INK = (26, 24, 20)
RED = (163, 32, 24)
GOLD = (146, 108, 32)
GREY = (96, 90, 80)
RULE = (60, 56, 48)
PANEL = (250, 246, 238)

# 5x7 bitmap font, one string per row, '#' = ink.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "....#", "....#", "....#", "....#", "#...#", ".###."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", ".#.#.", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": (".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "$": ("..#..", ".####", "#.#.#", ".###.", ".#.#.", "####.", "..#.."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "\u00b7": (".....", ".....", ".....", ".##..", ".##..", ".....", "....."),
    "\u2014": (".....", ".....", ".....", "#####", "#####", ".....", "....."),
    "\u2013": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "\u2019": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "\u2018": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "\u201c": (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "\u201d": (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def frame(self, x, y, w, h, color, t=2):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for r, row in enumerate(glyph):
                for c, cell in enumerate(row):
                    if cell == "#":
                        self.rect(cx + c * scale, y + r * scale, scale, scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def text_c(self, cx, y, s, scale, color):
        return self.text(cx - self.text_w(s, scale) // 2, y, s, scale, color)


def save_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def wrap(s, maxchars):
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if len(trial) <= maxchars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def panel(cv, x, y, w, h, num, kicker, headline, body, head_scale, head_cpl, body_cpl, body_lh):
    cv.rect(x, y, w, h, PANEL)
    cv.frame(x, y, w, h, RULE, 2)
    ix, iy = x + 16, y + 13
    cv.text(ix, iy, num, 2, RED)
    cv.text(ix + 42, iy, kicker, 2, GOLD)
    hy = iy + 22
    for line in wrap(headline, head_cpl):
        cv.text(ix, hy, line, head_scale, INK)
        hy += 7 * head_scale + 6
    by = hy + 4
    for line in wrap(body, body_cpl):
        cv.text(ix, by, line, 2, INK)
        by += body_lh


def draw(cv):
    M = 36
    CW = W - 2 * M  # 952, content width
    cv.rect(0, 0, W, H, PAPER)

    # Masthead
    cv.text_c(W // 2, 26, "SATURDAY, NOVEMBER 21, 2026 \u00b7 ALL THE NEWS ON ONE PAGE", 2, RED)
    cv.text_c(W // 2, 52, "THE WORLD IN ONE DAY", 7, INK)
    cv.text_c(W // 2, 112, "RUSSIA'S BARRAGE REACHES POLAND \u00b7 WALL STREET IN CORRECTION \u00b7 A CANCER PILL LANDMARK", 2, GREY)
    cv.rect(M, 138, CW, 4, INK)
    cv.rect(M, 146, CW, 2, INK)

    # 01 - lead story, wide
    panel(cv, M, 160, CW, 196, "01", "KYIV \u00b7 WARSAW \u2014 CONFLICT",
          "RUSSIA'S BIGGEST BARRAGE IN WEEKS - MISSILES LAND IN POLAND",
          "Russia fired more than 400 drones and 110 missiles at Ukraine overnight, "
          "killing at least eight people in Kyiv and wrecking bridges and rail stations. "
          "Two missiles and a suspected drone came down inside Poland, whose prime "
          "minister, Donald Tusk, called it a deliberate provocation.",
          4, 37, 75, 20)

    # 02-05 - grid, 2 x 2
    gw = (CW - 16) // 2
    gy1, gy2, gh = 372, 564, 176
    panel(cv, M, gy1, gw, gh, "02", "NEW YORK \u2014 MARKETS",
          "AI ROUT SENDS WALL STREET INTO CORRECTION",
          "The S&P 500 fell 3.7% to 6,910.39, its 7th straight loss, and the Nasdaq "
          "plunged 5.3% as Anthropic's flat second day soured the AI trade.",
          3, 24, 36, 19)
    panel(cv, M + gw + 16, gy1, gw, gh, "03", "LONDON \u2014 HEALTH",
          "CANCER PILL ERASES TUMORS IN TRIAL",
          "The pill daraxonrasib made pancreatic cancer undetectable on scans in "
          "1 in 12 patients - a landmark result for a deadly cancer.",
          3, 24, 36, 19)
    panel(cv, M, gy2, gw, gh, "04", "BRUSSELS \u2014 POLITICS",
          "UK AND EU SIGN BIGGEST POST-BREXIT DEALS",
          "PM Andy Burnham and EU leaders signed three deals in Brussels: food "
          "exports, carbon markets and youth mobility - a post-Brexit reset.",
          3, 24, 36, 19)
    panel(cv, M + gw + 16, gy2, gw, gh, "05", "ANTALYA \u2014 CLIMATE",
          "COP31 RUNS INTO OVERTIME IN ANTALYA",
          "The UN climate summit blew past its deadline as nearly 200 nations "
          "deadlocked over fossil fuels, talks dragging into the weekend.",
          3, 24, 36, 19)

    # 06 - wide
    panel(cv, M, 756, CW, 120, "06", "HORMUZ \u00b7 WASHINGTON \u2014 MIDEAST",
          "IRAN SAYS IT DOWNED A US DRONE OVER HORMUZ",
          "Tehran says it shot down a US MQ-9 over the Strait of Hormuz - the 58th "
          "it claims - as Trump weighs new strikes on Iran under pressure from Israel.",
          3, 50, 75, 19)

    # Markets ticker, dark band
    cv.rect(M, 892, CW, 58, INK)
    cv.text_c(W // 2, 902, "AT FRIDAY'S CLOSE: S&P 500 6,910.39 -3.70% \u00b7 NASDAQ 22,617.73 -5.28%", 2, PAPER)
    cv.text_c(W // 2, 924, "DOW 48,147.33 -1.93% \u00b7 GOLD $3,517.24 -3.02% \u00b7 NVIDIA $125.53 -14%", 2, PAPER)

    # Also today + footer
    cv.text_c(W // 2, 962, "ALSO TODAY - GEN Z PROTESTS SPREAD TO 25 EUROPEAN COUNTRIES", 2, GOLD)
    cv.text_c(W // 2, 982, "GTA 6 SMASHES DAY-ONE RECORD AT $4.9B \u00b7 MYANMAR CALLS ICJ RULING BIASED", 2, GREY)
    cv.text_c(W // 2, 1002, "SWIMMER LEWIS PUGH CROSSES THE STRAIT OF HORMUZ FOR ITS WILDLIFE", 2, GREY)


def main():
    cv = Canvas(W, H, PAPER)
    draw(cv)
    out = "/output/entry.png"
    try:
        os.makedirs("/output", exist_ok=True)
    except OSError:
        out = "./entry.png"
    if not os.path.isdir("/output"):
        out = "./entry.png"
    n = save_png(cv, out)
    print(f"wrote {out} ({n} bytes)")


if __name__ == "__main__":
    main()
