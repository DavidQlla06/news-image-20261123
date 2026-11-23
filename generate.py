#!/usr/bin/env python3
"""Draw the Monday 23 November 2026 front page for news-image-20261123.

A broadsheet-style 1024x1024 image: masthead and dateline, a world map
with thirteen numbered pins next to the lead story, twelve illustrated
story cards, a twelve-item briefs panel and a ticker strip. The drawing
is deterministic: the same stories.json always yields the same bytes.
"""
import json
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
PAGE = 1024

CREAM = (248, 244, 234)
CARD_BG = (253, 251, 245)
INK = (24, 22, 20)
GREY = (108, 102, 94)
LINE = (62, 58, 52)
ACCENT = (176, 32, 32)
SEA_HI = (172, 208, 230)
SEA_LO = (118, 170, 208)
LAND_FILL = (234, 216, 172)
LAND_EDGE = (148, 126, 82)

REGION_INK = {
    "EUROPE": (43, 108, 176),
    "AMERICAS": (156, 66, 161),
    "ASIA-PACIFIC": (38, 140, 110),
    "AFRICA": (196, 120, 30),
    "MIDDLE EAST & GULF": (190, 45, 45),
    "CLIMATE & PLANET": (46, 150, 80),
    "BUSINESS · TECH · SPORT": (90, 90, 170),
}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def face(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(pen, text, fnt, width):
    """Greedy word wrap against a pixel width."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if pen.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def wash(img, box, top, bottom):
    """Vertical colour wash inside box."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    pen = ImageDraw.Draw(img)
    for step in range(span):
        frac = step / span
        col = tuple(int(top[k] + (bottom[k] - top[k]) * frac) for k in range(3))
        pen.line([(x0, y0 + step), (x1, y0 + step)], fill=col)


def grain(img, count, seed):
    """Light paper grain, seeded so reruns match byte for byte."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pen = ImageDraw.Draw(layer)
    for _ in range(count):
        x = rng.randint(0, PAGE - 1)
        y = rng.randint(0, PAGE - 1)
        shade = (0, 0, 0, 13) if rng.random() < 0.5 else (255, 255, 255, 13)
        pen.point((x, y), fill=shade)
    merged = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    img.paste(merged, (0, 0))


# Hand-simplified land outlines as (longitude, latitude) rings.
LANDMASSES = [
    # North America
    [(-166, 60), (-158, 58), (-150, 60), (-140, 60), (-134, 56), (-128, 51),
     (-125, 48), (-124, 43), (-122, 38), (-117, 33), (-112, 29), (-110, 24),
     (-106, 21), (-102, 18), (-97, 16), (-94, 18), (-91, 19), (-88, 16),
     (-84, 13), (-80, 9), (-78, 8), (-82, 9), (-85, 11), (-88, 14),
     (-90, 15), (-92, 15), (-95, 16), (-97, 19), (-97, 22), (-97, 26),
     (-94, 29), (-89, 30), (-84, 30), (-82, 28), (-81, 25), (-80, 29),
     (-79, 33), (-76, 35), (-75, 38), (-72, 41), (-70, 42), (-68, 44),
     (-66, 45), (-70, 44), (-72, 44), (-74, 47), (-76, 50), (-78, 55),
     (-80, 58), (-83, 61), (-88, 64), (-94, 66), (-100, 68), (-110, 68),
     (-120, 70), (-130, 70), (-140, 70), (-152, 70), (-160, 68), (-166, 65)],
    # South America
    [(-77, 8), (-75, 10), (-72, 12), (-68, 11), (-64, 10), (-60, 8),
     (-55, 6), (-51, 4), (-50, 0), (-46, -2), (-41, -3), (-35, -8),
     (-37, -11), (-39, -14), (-40, -20), (-42, -23), (-46, -25),
     (-49, -29), (-52, -33), (-55, -35), (-58, -39), (-62, -41),
     (-65, -45), (-67, -49), (-68, -52), (-68, -54), (-71, -54),
     (-73, -51), (-74, -47), (-73, -42), (-72, -36), (-71, -31),
     (-70, -25), (-70, -19), (-72, -18), (-75, -15), (-76, -13),
     (-77, -10), (-79, -7), (-81, -4), (-80, -1), (-78, 2), (-77, 5)],
    # Africa
    [(-17, 15), (-16, 19), (-15, 24), (-13, 27), (-10, 30), (-6, 34),
     (-2, 35), (2, 37), (6, 37), (10, 37), (11, 34), (15, 32), (20, 32),
     (25, 32), (30, 31), (32, 31), (34, 28), (36, 24), (38, 21), (40, 16),
     (42, 12), (44, 11), (47, 11), (50, 12), (51, 11), (49, 10), (46, 5),
     (42, 0), (40, -5), (40, -10), (39, -15), (37, -19), (35, -23),
     (33, -26), (31, -29), (28, -32), (25, -34), (20, -35), (18, -32),
     (16, -28), (15, -23), (13, -17), (13, -12), (12, -7), (13, -2),
     (10, 3), (6, 4), (2, 6), (-3, 5), (-7, 5), (-11, 7), (-14, 9),
     (-16, 12)],
    # Europe and Asia as one landmass
    [(-9, 37), (-9, 39), (-9, 43), (-6, 44), (-2, 44), (-1, 46), (-4, 48),
     (-1, 49), (1, 51), (4, 52), (6, 54), (8, 55), (8, 57), (10, 58),
     (7, 58), (5, 59), (5, 61), (7, 63), (11, 65), (15, 68), (20, 70),
     (26, 71), (32, 70), (40, 68), (48, 68), (56, 69), (66, 70),
     (74, 72), (84, 73), (94, 76), (104, 77), (112, 74), (122, 72),
     (132, 72), (142, 72), (152, 70), (162, 69), (172, 67), (178, 65),
     (172, 61), (164, 60), (160, 55), (157, 51), (152, 58), (146, 58),
     (143, 54), (142, 50), (140, 46), (136, 45), (133, 43), (130, 42),
     (128, 39), (126, 38), (123, 38), (121, 34), (120, 31), (120, 27),
     (116, 23), (112, 21), (109, 18), (109, 14), (107, 10), (105, 8),
     (103, 5), (101, 3), (100, 6), (99, 9), (98, 13), (96, 16), (93, 17),
     (91, 22), (88, 22), (86, 20), (82, 16), (80, 13), (78, 9), (77, 8),
     (75, 12), (73, 18), (71, 21), (68, 23), (64, 25), (60, 25), (57, 26),
     (55, 26), (52, 25), (50, 27), (49, 29), (48, 29), (50, 26), (52, 24),
     (55, 24), (57, 25), (58, 23), (59, 22), (56, 18), (53, 16), (49, 13),
     (45, 12), (43, 12), (42, 15), (40, 19), (38, 24), (35, 28), (34, 28),
     (35, 31), (36, 35), (34, 36), (31, 36), (28, 37), (25, 36), (22, 37),
     (20, 39), (18, 40), (16, 39), (16, 41), (14, 42), (12, 44), (9, 44),
     (7, 44), (4, 43), (2, 42), (0, 39), (-2, 37), (-5, 36), (-8, 37)],
    # Borneo
    [(110, 0), (113, 3), (116, 5), (118, 3), (118, -1), (115, -3),
     (112, -2), (110, -1)],
    # Indonesia and New Guinea chain
    [(96, 4), (100, 0), (104, -4), (108, -6), (112, -7), (117, -8),
     (122, -9), (127, -8), (131, -4), (136, -2), (141, -3), (146, -5),
     (149, -8), (146, -8), (141, -7), (136, -6), (131, -4), (126, -4),
     (121, -9), (116, -8), (110, -7), (105, -6), (100, -1), (97, 2)],
    # Australia
    [(114, -21), (113, -25), (114, -30), (115, -34), (118, -35), (123, -34),
     (128, -32), (132, -32), (135, -35), (137, -35), (139, -37), (141, -38),
     (145, -38), (148, -38), (150, -37), (152, -33), (153, -29), (153, -25),
     (151, -22), (149, -19), (146, -19), (145, -15), (143, -12), (142, -11),
     (142, -14), (141, -16), (139, -17), (137, -16), (136, -13), (134, -12),
     (131, -12), (128, -14), (125, -16), (122, -17), (119, -19), (116, -20)],
    # Greenland
    [(-52, 64), (-50, 68), (-52, 72), (-54, 76), (-50, 79), (-42, 81),
     (-32, 82), (-24, 79), (-20, 76), (-21, 71), (-26, 68), (-32, 67),
     (-40, 64), (-46, 61), (-50, 62)],
    # Britain
    [(-5, 50), (-3, 51), (-1, 52), (0, 53), (-1, 55), (-2, 57), (-4, 58),
     (-6, 58), (-7, 56), (-6, 54), (-5, 52)],
    # Japan
    [(131, 31), (133, 34), (136, 35), (139, 36), (140, 38), (141, 41),
     (142, 43), (141, 44), (140, 41), (139, 38), (137, 35), (134, 34),
     (132, 32)],
    # Madagascar
    [(44, -16), (46, -15), (49, -15), (50, -18), (48, -21), (47, -24),
     (45, -25), (44, -22), (43, -19)],
    # New Zealand
    [(168, -46), (170, -44), (172, -42), (173, -40), (175, -38), (177, -37),
     (178, -37), (176, -38), (174, -39), (173, -41), (171, -43), (169, -45)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 180) / 360.0 * (x1 - x0)
    py = y0 + (75 - lat) / 135.0 * (y1 - y0)
    return px, py


def pin(pen, cx, cy, number, colour):
    r = 10
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour,
                outline=(255, 255, 255), width=2)
    label = str(number)
    w = pen.textlength(label, font=face(SANS_B, 12))
    pen.text((cx - w / 2, cy - 7), label, font=face(SANS_B, 12),
             fill=(255, 255, 255))


def paint_map(img, box, pins):
    x0, y0, x1, y1 = box
    wash(img, box, SEA_HI, SEA_LO)
    pen = ImageDraw.Draw(img)
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, box)
        pen.line([(gx, y0), (gx, y1)], fill=(142, 182, 206), width=1)
    for lat in range(-60, 76, 30):
        _, gy = project(0, lat, box)
        pen.line([(x0, gy), (x1, gy)], fill=(142, 182, 206), width=1)
    for ring in LANDMASSES:
        pts = [project(lon, lat, box) for lon, lat in ring]
        pen.polygon(pts, fill=LAND_FILL, outline=LAND_EDGE)
    pen.text((x0 + 4, y1 - 13), "PACIFIC", font=face(SANS_R, 9),
             fill=(70, 110, 140))
    pen.text((x1 - 52, y1 - 13), "ATLANTIC", font=face(SANS_R, 9),
             fill=(70, 110, 140))
    for number, lon, lat, colour in pins:
        cx, cy = project(lon, lat, box)
        pin(pen, cx, cy, number, colour)
    pen.rectangle(box, outline=LINE, width=2)


def art_summit(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (96, 150, 200), (190, 215, 235))
    pen = ImageDraw.Draw(img)
    pen.rectangle([x0 + 14, y1 - 20, x1 - 14, y1 - 10], fill=(122, 86, 52))
    for i, col in enumerate([(200, 40, 40), (40, 90, 200), (40, 160, 80), (230, 180, 40)]):
        fx = x0 + 28 + i * 52
        pen.line([(fx, y1 - 20), (fx, y0 + 12)], fill=(62, 62, 62), width=2)
        pen.polygon([(fx, y0 + 12), (fx + 26, y0 + 18), (fx, y0 + 24)], fill=col)
    pen.line([(x1 - 48, y0 + 16), (x1 - 26, y0 + 38)], fill=(92, 62, 32), width=5)
    pen.rectangle([x1 - 54, y0 + 8, x1 - 38, y0 + 22], fill=(92, 62, 32))
    pen.line([(x0 + 10, y1 - 8), (x1 - 10, y1 - 8)], fill=ACCENT, width=3)


def art_building(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (122, 152, 187), (202, 212, 222))
    pen = ImageDraw.Draw(img)
    pen.rectangle([x0 + 40, y0 + 4, x0 + 140, y1 - 3], fill=(206, 191, 166),
                  outline=(122, 107, 82))
    for r in range(2):
        for c in range(4):
            wx = x0 + 48 + c * 23
            wy = y0 + 8 + r * 14
            pen.rectangle([wx, wy, wx + 13, wy + 9], fill=(72, 87, 107))
    pen.polygon([(x0 + 140, y0 + 4), (x0 + 205, y1 - 3), (x0 + 140, y1 - 3)],
                fill=(172, 157, 132))
    for i in range(6):
        rx = x0 + 150 + i * 10
        pen.polygon([(rx, y1 - 3), (rx + 8, y1 - 3), (rx + 4, y1 - 12 - (i % 3) * 3)],
                    fill=(132, 117, 92))
    pen.ellipse([x0 + 152, y0 + 3, x0 + 188, y0 + 15], fill=(92, 92, 97))


def art_shipfire(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (82, 122, 167), (172, 197, 217))
    pen = ImageDraw.Draw(img)
    pen.rectangle([x0, y1 - 16, x1, y1], fill=(52, 97, 142))
    pen.polygon([(x0 + 24, y1 - 26), (x1 - 30, y1 - 26), (x1 - 46, y1 - 14),
                 (x0 + 40, y1 - 14)], fill=(47, 47, 54))
    pen.rectangle([x0 + 60, y1 - 34, x0 + 96, y1 - 26], fill=(72, 72, 82))
    pen.rectangle([x0 + 150, y1 - 32, x0 + 176, y1 - 26], fill=(72, 72, 82))
    for fx in (x0 + 84, x0 + 112, x0 + 160):
        pen.polygon([(fx - 9, y1 - 26), (fx, y1 - 38), (fx + 9, y1 - 26)],
                    fill=(242, 112, 27))
        pen.polygon([(fx - 4, y1 - 26), (fx, y1 - 33), (fx + 4, y1 - 26)],
                    fill=(255, 192, 62))
    for sx, sy, sr in [(x0 + 90, y0 + 8, 11), (x0 + 118, y0 + 5, 13), (x0 + 150, y0 + 7, 10)]:
        pen.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=(62, 62, 68))


def art_exam(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (205, 228, 242), (242, 249, 251))
    pen = ImageDraw.Draw(img)
    cx = (x0 + x1) // 2
    # exam paper with red cross, smart glasses beside it
    pen.rectangle([cx - 52, y0 + 6, cx - 8, y1 - 6], fill=(255, 255, 252),
                  outline=(90, 110, 130), width=2)
    for i in range(3):
        ly = y0 + 12 + i * 7
        pen.line([(cx - 46, ly), (cx - 16, ly)], fill=(140, 150, 160), width=2)
    pen.line([(cx - 44, y0 + 28), (cx - 16, y0 + 40)], fill=ACCENT, width=3)
    pen.line([(cx - 16, y0 + 28), (cx - 44, y0 + 40)], fill=ACCENT, width=3)
    pen.ellipse([cx + 8, y0 + 14, cx + 34, y0 + 30], outline=(30, 30, 36), width=3)
    pen.ellipse([cx + 38, y0 + 14, cx + 64, y0 + 30], outline=(30, 30, 36), width=3)
    pen.line([(cx + 34, y0 + 20), (cx + 38, y0 + 20)], fill=(30, 30, 36), width=3)
    pen.line([(cx + 8, y0 + 18), (cx + 2, y0 + 12)], fill=(30, 30, 36), width=3)
    pen.line([(cx + 64, y0 + 18), (cx + 70, y0 + 12)], fill=(30, 30, 36), width=3)
    pen.text((x0 + 8, y0 + 4), "AI", font=face(SANS_B, 16), fill=ACCENT)


def art_factory(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (142, 152, 172), (202, 197, 187))
    pen = ImageDraw.Draw(img)
    pen.rectangle([x0 + 20, y1 - 26, x0 + 180, y1 - 6], fill=(152, 122, 97))
    pen.polygon([(x0 + 20, y1 - 26), (x0 + 60, y1 - 36), (x0 + 100, y1 - 26),
                 (x0 + 140, y1 - 36), (x0 + 180, y1 - 26)], fill=(112, 87, 67))
    pen.rectangle([x0 + 185, y0 + 10, x0 + 200, y1 - 6], fill=(122, 97, 77))
    for fx in (x0 + 55, x0 + 95, x0 + 140):
        pen.polygon([(fx - 10, y1 - 28), (fx, y1 - 38), (fx + 10, y1 - 28)],
                    fill=(242, 112, 27))
        pen.polygon([(fx - 4, y1 - 28), (fx, y1 - 34), (fx + 4, y1 - 28)],
                    fill=(255, 197, 72))
    pen.ellipse([x0 + 62, y0 + 4, x0 + 112, y0 + 20], fill=(72, 72, 78))
    pen.ellipse([x0 + 122, y0 + 2, x0 + 177, y0 + 18], fill=(87, 87, 94))


def art_handshake(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (150, 180, 205), (215, 228, 238))
    pen = ImageDraw.Draw(img)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    # two flags and a handshake bar
    pen.line([(x0 + 30, y1 - 8), (x0 + 30, y0 + 8)], fill=(60, 60, 60), width=2)
    pen.rectangle([x0 + 30, y0 + 8, x0 + 58, y0 + 22], fill=(220, 20, 60))
    pen.line([(x1 - 30, y1 - 8), (x1 - 30, y0 + 8)], fill=(60, 60, 60), width=2)
    pen.rectangle([x1 - 58, y0 + 8, x1 - 30, y0 + 22], fill=(255, 153, 51))
    pen.polygon([(cx - 46, cy - 4), (cx - 10, cy - 8), (cx + 6, cy - 2),
                 (cx - 8, cy + 8), (cx - 34, cy + 6)], fill=(210, 160, 120))
    pen.polygon([(cx + 46, cy - 4), (cx + 10, cy - 8), (cx - 6, cy - 2),
                 (cx + 8, cy + 8), (cx + 34, cy + 6)], fill=(190, 140, 100))
    pen.ellipse([cx - 10, cy - 6, cx + 10, cy + 10], fill=(200, 150, 110))


def art_crash(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (36, 36, 46), (72, 72, 87))
    pen = ImageDraw.Draw(img)
    pen.text((x0 + 8, y0 + 3), "-13.8%", font=face(SANS_B, 18), fill=(255, 80, 80))
    pts = [(x0 + 10, y0 + 28), (x0 + 55, y0 + 22), (x0 + 95, y0 + 32),
           (x0 + 135, y0 + 26), (x0 + 175, y0 + 36), (x0 + 215, y0 + 40)]
    pen.line(pts, fill=(255, 70, 70), width=4)
    pen.polygon([(x0 + 215, y0 + 40), (x0 + 200, y0 + 37), (x0 + 208, y0 + 30)],
                fill=(255, 70, 70))
    for gx in range(x0 + 10, x1 - 6, 24):
        pen.line([(gx, y0 + 20), (gx, y1 - 4)], fill=(92, 92, 107), width=1)


def art_f1car(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (31, 31, 61), (92, 72, 122))
    pen = ImageDraw.Draw(img)
    pen.rectangle([x0, y1 - 14, x1, y1], fill=(42, 42, 46))
    for i in range(8):
        pen.rectangle([x0 + 8 + i * 30, y1 - 9, x0 + 20 + i * 30, y1 - 5],
                      fill=(242, 242, 242))
    cy = y1 - 22
    pen.polygon([(x0 + 30, cy), (x0 + 70, cy - 8), (x0 + 120, cy - 9),
                 (x0 + 150, cy - 4), (x0 + 205, cy), (x0 + 205, cy + 6),
                 (x0 + 30, cy + 6)], fill=(212, 32, 42))
    pen.rectangle([x0 + 96, cy - 15, x0 + 112, cy - 8], fill=(212, 32, 42))
    pen.rectangle([x0 + 22, cy - 6, x0 + 40, cy + 2], fill=(32, 32, 32))
    for wx in (x0 + 58, x0 + 168):
        pen.ellipse([wx - 10, cy - 3, wx + 10, cy + 13], fill=(16, 16, 16))
        pen.ellipse([wx - 4, cy + 2, wx + 4, cy + 9], fill=(202, 202, 202))
    pen.text((x0 + 8, y0 + 6), "LAS VEGAS", font=face(SANS_B, 12),
             fill=(255, 220, 90))


def art_arson(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (60, 55, 60), (120, 95, 85))
    pen = ImageDraw.Draw(img)
    # two burning cars
    for bx in (x0 + 30, x0 + 130):
        pen.polygon([(bx, y1 - 14), (bx + 14, y1 - 22), (bx + 52, y1 - 22),
                     (bx + 66, y1 - 14)], fill=(40, 40, 46))
        pen.rectangle([bx, y1 - 14, bx + 66, y1 - 6], fill=(52, 52, 60))
        for wx in (bx + 12, bx + 48):
            pen.ellipse([wx - 6, y1 - 10, wx + 6, y1], fill=(14, 14, 14))
        pen.polygon([(bx + 22, y1 - 22), (bx + 33, y1 - 34), (bx + 44, y1 - 22)],
                    fill=(242, 112, 27))
        pen.polygon([(bx + 28, y1 - 22), (bx + 33, y1 - 29), (bx + 38, y1 - 22)],
                    fill=(255, 195, 70))
    pen.ellipse([x0 + 50, y0 + 4, x0 + 110, y0 + 18], fill=(55, 55, 60))
    pen.ellipse([x0 + 130, y0 + 2, x0 + 195, y0 + 16], fill=(70, 70, 76))


def art_intercept(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (90, 130, 180), (190, 215, 235))
    pen = ImageDraw.Draw(img)
    # incoming missile and interceptor burst
    pen.line([(x0 + 20, y0 + 8), (x0 + 110, y0 + 24)], fill=(255, 180, 60), width=3)
    pen.polygon([(x0 + 110, y0 + 24), (x0 + 98, y0 + 21), (x0 + 98, y0 + 27)],
                fill=(255, 220, 120))
    pen.line([(x1 - 30, y1 - 8), (x0 + 118, y0 + 26)], fill=(120, 200, 255), width=3)
    bx, by = x0 + 114, y0 + 25
    for ang in range(0, 360, 30):
        ex = bx + 14 * math.cos(math.radians(ang))
        ey = by + 14 * math.sin(math.radians(ang))
        pen.line([(bx, by), (ex, ey)], fill=(255, 140, 40), width=2)
    pen.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 210, 90))
    pen.rectangle([x0, y1 - 8, x1, y1], fill=(150, 135, 105))


def art_cricket(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (110, 170, 110), (180, 215, 160))
    pen = ImageDraw.Draw(img)
    pen.rectangle([x0 + 90, y1 - 16, x0 + 150, y1 - 6], fill=(210, 190, 150))
    # stumps, bat and ball
    for sx in (x0 + 104, x0 + 112, x0 + 120):
        pen.rectangle([sx, y1 - 26, sx + 4, y1 - 6], fill=(240, 230, 200),
                      outline=(150, 130, 90))
    pen.polygon([(x0 + 140, y0 + 8), (x0 + 148, y0 + 10), (x0 + 136, y1 - 14),
                 (x0 + 128, y1 - 16)], fill=(220, 190, 130))
    pen.ellipse([x0 + 60, y0 + 12, x0 + 72, y0 + 24], fill=(200, 30, 30))
    pen.arc([x0 + 60, y0 + 12, x0 + 72, y0 + 24], start=200, end=340,
            fill=(255, 255, 255), width=1)
    pen.text((x0 + 8, y0 + 4), "720/9", font=face(SANS_B, 16), fill=(20, 60, 20))


def art_march(img, box):
    x0, y0, x1, y1 = box
    wash(img, box, (170, 190, 215), (225, 232, 238))
    pen = ImageDraw.Draw(img)
    # crowd silhouettes with placards
    rng = random.Random(11)
    for i in range(9):
        px = x0 + 16 + i * 24 + rng.randint(-3, 3)
        pen.ellipse([px, y1 - 22, px + 10, y1 - 12], fill=(45, 45, 55))
        pen.rectangle([px + 1, y1 - 12, px + 9, y1 - 2], fill=(45, 45, 55))
    for px, col in [(x0 + 30, (220, 60, 60)), (x0 + 95, (50, 110, 200)),
                    (x0 + 160, (240, 190, 50))]:
        pen.line([(px + 10, y1 - 20), (px + 10, y0 + 14)], fill=(70, 60, 50), width=2)
        pen.rectangle([px, y0 + 4, px + 20, y0 + 14], fill=col)


ART = {
    "summit": art_summit,
    "building": art_building,
    "shipfire": art_shipfire,
    "exam": art_exam,
    "factory": art_factory,
    "handshake": art_handshake,
    "crash": art_crash,
    "f1car": art_f1car,
    "arson": art_arson,
    "intercept": art_intercept,
    "cricket": art_cricket,
    "march": art_march,
}


def paint_art(img, box, kind):
    ART[kind](img, box)
    pen = ImageDraw.Draw(img)
    pen.rectangle(box, outline=LINE, width=1)


def build_page(data):
    img = Image.new("RGB", (PAGE, PAGE), CREAM)
    pen = ImageDraw.Draw(img)
    margin = 24
    right = PAGE - margin

    # Masthead and dateline
    mast = data["masthead"]
    f_mast = face(SERIF_B, 58)
    tw = pen.textlength(mast, font=f_mast)
    pen.text(((PAGE - tw) / 2, 8), mast, font=f_mast, fill=INK)
    f_date = face(SERIF_B, 26)
    tw = pen.textlength(data["dateline"], font=f_date)
    pen.text(((PAGE - tw) / 2, 74), data["dateline"], font=f_date, fill=ACCENT)
    pen.line([(margin, 108), (right, 108)], fill=INK, width=3)
    pen.line([(margin, 113), (right, 113)], fill=INK, width=1)

    # World map beside the lead story
    map_box = (margin, 122, 582, 348)
    lead = data["lead"]
    pins = []
    for i, card in enumerate(data["cards"], start=2):
        pins.append((i, card["lon"], card["lat"], REGION_INK[card["region"]]))
    pins.append((1, lead["lon"], lead["lat"], ACCENT))
    paint_map(img, map_box, pins)
    pen = ImageDraw.Draw(img)
    pen.text((margin, 352), "Numbers match the story cards below.",
             font=face(SANS_R, 11), fill=GREY)

    lx = 598
    lw = right - lx
    f_tag = face(SANS_B, 15)
    kw = pen.textlength(lead["tag"], font=f_tag) + 16
    pen.rectangle([lx, 122, lx + kw, 146], fill=ACCENT)
    pen.text((lx + 8, 126), lead["tag"], font=f_tag, fill=(255, 255, 255))
    pin(pen, right - 12, 134, 1, ACCENT)
    f_lead = face(SERIF_B, 26)
    y = 154
    for line in fit_lines(pen, lead["headline"], f_lead, lw):
        pen.text((lx, y), line, font=f_lead, fill=INK)
        y += 31
    f_stand = face(SERIF_R, 14)
    y += 2
    for line in fit_lines(pen, lead["standfirst"], f_stand, lw):
        pen.text((lx, y), line, font=f_stand, fill=(56, 53, 49))
        y += 18
    y += 4
    f_pt = face(SANS_R, 13)
    for point in lead["points"]:
        pen.polygon([(lx, y + 3), (lx + 8, y + 7), (lx, y + 11)], fill=ACCENT)
        for line in fit_lines(pen, point, f_pt, lw - 14):
            pen.text((lx + 14, y), line, font=f_pt, fill=INK)
            y += 16
        y += 2

    # Twelve story cards, four across and three down
    cards = data["cards"]
    grid_top = 378
    cols, rows = 4, 3
    gap = 8
    cw = (right - margin - gap * (cols - 1)) // cols
    ch = 112
    art_h = 40
    for idx, card in enumerate(cards):
        r, c = divmod(idx, cols)
        cx0 = margin + c * (cw + gap)
        cy0 = grid_top + r * (ch + gap)
        cx1, cy1 = cx0 + cw, cy0 + ch
        pen.rectangle([cx0, cy0, cx1, cy1], fill=CARD_BG, outline=LINE, width=1)
        paint_art(img, (cx0 + 1, cy0 + 1, cx1 - 1, cy0 + art_h), card["art"])
        pen = ImageDraw.Draw(img)
        colour = REGION_INK[card["region"]]
        pin(pen, cx0 + 13, cy0 + art_h + 10, idx + 2, colour)
        pen.text((cx0 + 28, cy0 + art_h + 4), card["region"],
                 font=face(SANS_B, 10), fill=colour)
        f_head = face(SERIF_B, 13)
        hy = cy0 + art_h + 17
        for line in fit_lines(pen, card["headline"], f_head, cw - 10)[:2]:
            pen.text((cx0 + 5, hy), line, font=f_head, fill=INK)
            hy += 15
        f_body = face(SANS_R, 10)
        for line in fit_lines(pen, card["summary"], f_body, cw - 10)[:2]:
            pen.text((cx0 + 5, hy + 1), line, font=f_body, fill=(71, 67, 61))
            hy += 12

    # Briefs panel, two columns
    briefs_top = grid_top + rows * (ch + gap) + 6
    pen.text((margin, briefs_top), "ALSO TODAY — AROUND THE WORLD",
             font=face(SANS_B, 15), fill=INK)
    pen.line([(margin, briefs_top + 22), (right, briefs_top + 22)],
             fill=LINE, width=1)
    col_w = (right - margin - 24) // 2
    f_bh = face(SANS_B, 12)
    f_bs = face(SANS_R, 11)
    for i, item in enumerate(data["briefs"]):
        col = 0 if i < 6 else 1
        row = i % 6
        bx = margin + col * (col_w + 24)
        by = briefs_top + 28 + row * 31
        colour = REGION_INK[item["region"]]
        pen.rectangle([bx, by + 2, bx + 4, by + 24], fill=colour)
        for line in fit_lines(pen, item["headline"], f_bh, col_w - 12)[:1]:
            pen.text((bx + 10, by), line, font=f_bh, fill=INK)
        for line in fit_lines(pen, item["summary"], f_bs, col_w - 12)[:1]:
            pen.text((bx + 10, by + 15), line, font=f_bs, fill=(81, 77, 71))

    # Ticker strip and footer
    tick_top = briefs_top + 28 + 6 * 31 + 6
    pen.rectangle([margin, tick_top, right, tick_top + 40], fill=(26, 24, 23))
    f_tick = face(SANS_R, 11)
    tick_text = "  •  ".join(data["ticker"])
    ty = tick_top + 5
    for line in fit_lines(pen, tick_text, f_tick, right - margin - 16)[:2]:
        pen.text((margin + 8, ty), line, font=f_tick, fill=(241, 239, 233))
        ty += 15
    foot = data["footer"]
    f_foot = face(SANS_R, 11)
    tw = pen.textlength(foot, font=f_foot)
    pen.text(((PAGE - tw) / 2, tick_top + 44), foot, font=f_foot, fill=GREY)

    grain(img, 2600, seed=23)
    return img


def main():
    with open(os.path.join(BASE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    img = build_page(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", BASE)
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), optimize=True)
    print("wrote", os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
