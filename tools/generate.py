"""news-image-20261127 — render Friday 27 November 2026's world news
as one 1024x1024 newspaper front page (PIL, deterministic).

Slate: 35 stories = 3 leads + 8 panels + 24 one-liners, 10 regions,
15 fields. Every story was first reported in the early hours of
27 Nov 2026 (00:00-01:00 UTC reporting window and overnight wire
items = 27 Nov in Asia-Pacific time zones). Items that belong to
26 Nov (or earlier) are NOT in the slate; they are named in the
red DATE CHECK box instead.
"""

import hashlib
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 23, 18)
RED = (163, 22, 33)
BLUE = (31, 58, 95)
GOLD = (176, 132, 28)
GREY = (94, 88, 78)
RULE = (60, 54, 44)
SKY_NIGHT = (18, 28, 52)
SKY_GULF = (196, 168, 120)
SKY_DAY = (146, 178, 205)

FDIR = "/usr/share/fonts/truetype/noto"
SERIF = os.path.join(FDIR, "NotoSerif-Regular.ttf")
SERIF_B = os.path.join(FDIR, "NotoSerif-Bold.ttf")
SERIF_BLK = os.path.join(FDIR, "NotoSerifDisplay-Black.ttf")
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None, spacing=0):
    """Draw wrapped paragraph; return y just below last line."""
    lh = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh + spacing
    return y


def hline(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def vline(draw, x, y0, y1, fill=RULE, width=1):
    draw.line([(x, y0), (x, y1)], fill=fill, width=width)


def badge(draw, x, y, text, fill=RED):
    """Small uppercase confidence badge; returns width used."""
    f = font(SANS_B, 8)
    w = int(draw.textlength(text, font=f)) + 8
    draw.rectangle([x, y, x + w, y + 12], fill=fill)
    draw.text((x + 4, y + 2), text, font=f, fill=(255, 255, 255))
    return w


def grain(img, seed=20261127, amount=9):
    """Photographic paper grain: deterministic speckle + vignette."""
    rnd = random.Random(seed)
    px = img.load()
    for _ in range(26000):
        x = rnd.randrange(W)
        y = rnd.randrange(H)
        r, g, b = px[x, y]
        d = rnd.randint(-amount, amount)
        px[x, y] = (max(0, min(255, r + d)),
                    max(0, min(255, g + d)),
                    max(0, min(255, b + d)))
    ov = Image.new("L", (W, H), 0)
    od = ImageDraw.Draw(ov)
    od.ellipse([-220, -220, W + 220, H + 220], fill=255)
    ov = ov.point(lambda v: 255 - int((255 - v) * 0.55))
    dark = Image.new("RGB", (W, H), (52, 40, 26))
    img.paste(Image.composite(img, dark, ov), (0, 0))
    return img


# ---------------------------------------------------------------- stories
# n, region, field, badge, headline, body, source
LEADS = [
    dict(n=1, region="Europe", field="War", badge="CONFIRMED",
         art="kyiv",
         head="RUSSIA'S OVERNIGHT BARRAGE KILLS AT LEAST 3",
         body=("Missiles and drones hit Ukraine overnight, Kyiv among "
               "the targets. Ukraine hits back at a Su-34 airbase in "
               "Volgograd and refineries at Syzran and Kuibyshev."),
         src="Reports, 27 Nov 00:21 UTC"),
    dict(n=2, region="Middle East", field="War", badge="REPORTED",
         art="gulf",
         head="TWO ITALIANS KILLED AS IRAN DRONES HIT KUWAIT",
         body=("Drone debris falls on a vital Kuwaiti site, killing two "
               "Italian technicians; Iran denies blame. Two tankers are "
               "hit by mines off Oman."),
         src="Kuwait Defence Ministry / reports"),
    dict(n=3, region="N. America", field="Culture", badge="OFFICIAL",
         art="parade",
         head="PARADE EVE: MACY'S 100TH SET FOR SATURDAY",
         body=("Balloons go up on Friday for the 100th parade, "
               "08:30 ET Saturday. Smash Mouth and EJAE are confirmed; "
               "Mayor Mamdani will skip it for foot surgery."),
         src="Macy's / NYC"),
]

EIGHT = [
    dict(n=4, region="Middle East", field="War", badge="REPORTED",
         head="HOUTHIS PUSH ON ADEN",
         body=("Alarm grows of a new humanitarian catastrophe as Houthis "
               "advance; they claim strikes on Saudi's Jizan ports.")),
    dict(n=5, region="N. America", field="Diplomacy", badge="REPORTED",
         head="TRUMP AND RUTTE TO RUSSIA: DON'T ESCALATE",
         body=("Trump pressed Putin in China, he says; Kushner calls the war "
               "Europe's 'indirect war'.")),
    dict(n=6, region="E. Asia", field="War", badge="REPORTED",
         head="KIM VOWS 'UNCONTROLLABLE' NUCLEAR BUILD-UP",
         body=("Kim ignores Trump's overture; Pyongyang expels a Swiss "
               "diplomat weeks after Bern reopened its embassy.")),
    dict(n=7, region="Europe", field="Migration", badge="OFFICIAL",
         head="UK MIGRATION FALLS TO NEAR 30-YEAR LOW",
         body=("Net migration hits its lowest outside Covid; jets go into "
               "hardened shelters; 100,000 reservists told to be ready.")),
    dict(n=8, region="Europe", field="Defence", badge="REPORTED",
         head="NEIGHBOURS OF RUSSIA QUIT LANDMINE BAN",
         body=("Several countries bordering Russia pull out of the global "
               "landmine treaty.")),
    dict(n=9, region="Africa", field="Health", badge="REPORTED",
         head="EBOLA IN CONGO PASSES 12,000 CASES",
         body=("Infections reach 12,000 as responders pull out of the "
               "outbreak zone.")),
    dict(n=10, region="Global", field="Markets", badge="REPORTED",
         head="STOCKS SLIDE AS TARIFFS BITE",
         body=("World markets fall as Trump's tariffs rattle trade and the AI "
               "rally fades; Nvidia's Huang faces scrutiny in Washington.")),
    dict(n=11, region="Europe", field="Defence", badge="REPORTED",
         head="UKRAINE TO GET ITALY'S EUROFIGHTERS",
         body=("Kyiv is set to receive Italy's Eurofighter Typhoon Tranche 1 "
               "jets as Europe arms Ukraine.")),
]

REST = [
    (12, "Europe", "Diplomacy", "REPORTED",
     "Zelensky questions Trump calling Putin a 'friend'",
     "Kyiv interview"),
    (13, "Europe", "War", "OFFICIAL",
     "Ukraine gets remains of 250 fallen soldiers",
     "Deal with Russia"),
    (14, "Middle East", "War", "REPORTED",
     "Russia: Ukraine widening war after Libya sea strikes",
     "Moscow / Tripoli"),
    (15, "Europe", "War", "REPORTED",
     "Ukrainian sea drones hunt Russian Black Sea supply",
     "Kyiv / Brussels"),
    (16, "Middle East", "War", "CLAIM",
     "IDF 'ready to strike Iran alone, imminently'",
     "IDF / reports"),
    (17, "Middle East", "Health", "REPORTED",
     "Gaza health chiefs warn on reproductive care",
     "Gaza health ministry"),
    (18, "Middle East", "Politics", "REPORTED",
     "Israel builds settlement road near Bethlehem",
     "Reports"),
    (19, "Middle East", "Energy", "CLAIM",
     "Two tankers hit by mines off Oman; oil falls",
     "IRGC / markets"),
    (20, "Middle East", "Diplomacy", "REPORTED",
     "Qatar: US-Iran mediation still on track",
     "Doha"),
    (21, "Middle East", "War", "REPORTED",
     "Lebanon army breaks up Hezbollah-area clash",
     "Beirut / UN"),
    (22, "Middle East", "Politics", "REPORTED",
     "Iraq judge to convene Erbil-Baghdad dialogue",
     "Baghdad"),
    (23, "Europe", "War", "CLAIM",
     "Georgia: Russia set to seize Abkhazia, S. Ossetia",
     "Tbilisi"),
    (24, "Europe", "Security", "REPORTED",
     "Estonia to shut rail border; France cyber warning",
     "Tallinn / Paris"),
    (25, "Europe", "Diplomacy", "REPORTED",
     "Dutch PM: EU states may opt out of Ukraine aid",
     "The Hague"),
    (26, "Europe", "Politics", "REPORTED",
     "Britain wins 'Swiss-style' EU consultative role",
     "London / Brussels"),
    (27, "Europe", "Diplomacy", "REPORTED",
     "Poland, Germany press EU to back Ukraine",
     "Warsaw / Berlin"),
    (28, "S. America", "Security", "REPORTED",
     "Guatemala reinforces frontiers vs crime gangs",
     "Guatemala City"),
    (29, "SE Asia", "Disaster", "REPORTED",
     "13 dead as flood hits illegal Indonesia mine",
     "Jakarta"),
    (30, "N. America", "Climate", "REPORTED",
     "Super El Nino sends historic surf to California",
     "California"),
    (31, "SE Asia", "Law", "REPORTED",
     "Myanmar defies ICJ genocide orders",
     "Naypyidaw"),
    (32, "E. Asia", "Diplomacy", "REPORTED",
     "China warns Japan over arming the Philippines",
     "Beijing"),
    (33, "Oceania", "Diplomacy", "OFFICIAL",
     "Australia, Solomons sign anti-China pact",
     "Canberra / Honiara"),
    (34, "S. Asia", "Business", "REPORTED",
     "India-China border 'generally stable', says Beijing",
     "Beijing / Mumbai"),
    (35, "Global", "Sport", "OFFICIAL",
     "Sinner out of Australian Open 2027, knee injury",
     "Melbourne"),
]

NUMBERS = [
    ("3", "killed in Russia's overnight barrage on Ukraine"),
    ("2", "Italian technicians killed in the Kuwait drone attack"),
    ("12,000", "Ebola infections in Congo"),
    ("13", "dead in the Indonesia gold-mine flood"),
    ("100,000", "UK reservists told to be ready"),
    ("250", "fallen soldiers' remains returned to Ukraine"),
    ("2", "tankers hit by sea mines off Oman"),
    ("100", "th Macy's Thanksgiving Day Parade, Saturday"),
]

TIMELINE = [
    ("00:21 UTC", "Russia's overnight barrage on Ukraine reported"),
    ("EARLY HOURS", "Kuwait toll confirmed; flights diverted; Aden alarm"),
    ("MORNING", "Parade eve in New York; world markets slide"),
    ("MIDDAY", "Brussels summit build-up; reservists on standby"),
    ("FRIDAY NIGHT", "Balloons go up for Saturday's parade"),
]

DATECHECK = ("NOT 27 NOVEMBER — left out on purpose: Bangkok refinery fire, "
             "9 hurt (26 Nov) · Cairo tanker fire, 31 dead (26 Nov) · ECB set "
             "to pick de Cos (26 Nov) · US $622M F-16 deal for Ukraine (26 Nov) "
             "· Macy's postponement announced (25 Nov) · Gaza drone strike kills "
             "3 (26 Nov morning) · US tells citizens to leave Iran (25 Nov).")

ALSO = ("ALSO: Jolie-Pitt settle winery suit · Depardieu to stand trial · "
        "AA flight rerouted after exit-door scare · NATO staffer held in Belgium.")

SOURCES = ("Sources: Reuters, AP, Bloomberg, CNN, USA TODAY, BBC, Al Jazeera, "
           "The Guardian, Irish Times, 360LiveNews. All stories first reported "
           "27 Nov 2026 in some time zone.")


# ------------------------------------------------------------------- art
def sky_gradient(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = y1 - y0
    for i in range(n):
        t = i / max(1, n - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def art_kyiv(draw, box):
    """Night skyline under missile arcs: dark blue sky, lit windows,
    orange blast glows, white arcs."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (14, 22, 46), (52, 62, 96))
    rnd = random.Random(11)
    for _ in range(46):  # stars
        sx = rnd.randrange(x0 + 4, x1 - 4)
        sy = rnd.randrange(y0 + 3, y0 + 34)
        draw.point((sx, sy), fill=(220, 220, 235))
    # missile arcs
    for (ax, ay, bx, by, cx, cy) in [
            (x0 + 12, y1 - 8, x0 + 95, y0 + 22, x0 + 178, y1 - 30),
            (x0 + 60, y1 - 4, x0 + 150, y0 + 12, x0 + 240, y1 - 44),
            (x0 + 200, y1 - 10, x0 + 260, y0 + 30, x0 + 305, y1 - 52)]:
        pts = []
        for t in [i / 24 for i in range(25)]:
            px = (1 - t) ** 2 * ax + 2 * (1 - t) * t * bx + t * t * cx
            py = (1 - t) ** 2 * ay + 2 * (1 - t) * t * by + t * t * cy
            pts.append((px, py))
        draw.line(pts, fill=(240, 220, 160), width=2)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 240, 190))
    # blast glows: solid discs, orange outer, yellow core
    for (gx, gy, r) in [(x0 + 52, y1 - 34, 20), (x0 + 238, y1 - 40, 16),
                        (x0 + 150, y1 - 26, 12)]:
        draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(232, 110, 32))
        draw.ellipse([gx - r // 2, gy - r // 2, gx + r // 2, gy + r // 2],
                     fill=(255, 214, 120))
    # skyline silhouettes with lit windows
    base = y1
    bx = x0
    while bx < x1 - 8:
        bw = rnd.choice([18, 24, 30, 38])
        bh = rnd.choice([34, 48, 62, 78])
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(8, 12, 26))
        for wy in range(base - bh + 6, base - 6, 9):
            for wx in range(bx + 4, bx + bw - 3, 7):
                if rnd.random() < 0.45:
                    draw.rectangle([wx, wy, wx + 3, wy + 4],
                                   fill=(255, 196, 90))
        bx += bw + rnd.choice([2, 4, 7])


def art_gulf(draw, box):
    """Dusk over the Gulf: amber sky, dark sea, tanker silhouette,
    drone dots, mine splash rings."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (214, 158, 92), (120, 84, 66))
    draw.ellipse([x1 - 52, y0 + 8, x1 - 16, y0 + 44], fill=(255, 226, 170))
    horizon = y0 + int((y1 - y0) * 0.55)
    draw.rectangle([x0, horizon, x1, y1], fill=(28, 42, 58))
    for i in range(5):  # sun glitter on water
        yy = horizon + 6 + i * 9
        draw.line([(x0 + 30 + i * 8, yy), (x1 - 40 - i * 6, yy)],
                  fill=(214, 158, 92), width=2)
    # tanker silhouette
    draw.rectangle([x0 + 34, horizon - 16, x0 + 190, horizon + 2],
                   fill=(10, 14, 20))
    draw.rectangle([x0 + 60, horizon - 30, x0 + 78, horizon - 16],
                   fill=(10, 14, 20))
    draw.rectangle([x0 + 150, horizon - 24, x0 + 162, horizon - 16],
                   fill=(10, 14, 20))
    # smoke column from tanker (kept inside the box)
    for i in range(4):
        r = 3 + i * 2
        cy = horizon - 20 - i * 7
        draw.ellipse([x0 + 66 - r, cy - r, x0 + 66 + r, cy + r],
                     outline=(70, 60, 52), width=2)
    # drones + mine splash rings
    for (dx, dy) in [(x0 + 230, y0 + 26), (x0 + 262, y0 + 44),
                     (x0 + 286, y0 + 18)]:
        draw.ellipse([dx - 3, dy - 2, dx + 3, dy + 2], fill=(12, 12, 14))
        draw.line([(dx - 8, dy), (dx + 8, dy)], fill=(12, 12, 14), width=1)
    for (sx, sy, r) in [(x0 + 250, horizon + 22, 12),
                        (x0 + 285, horizon + 34, 8)]:
        draw.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2],
                     outline=(220, 220, 210), width=2)


def art_parade(draw, box):
    """Daylight parade: pale blue sky, balloon disc + ropes, street,
    confetti, crowd dots. Box is 90 px tall."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (158, 188, 214), (214, 226, 236))
    # sunlit buildings left + right
    draw.rectangle([x0, y0 + 26, x0 + 44, y1], fill=(120, 110, 96))
    draw.rectangle([x1 - 44, y0 + 18, x1, y1], fill=(104, 96, 88))
    for wx in range(x0 + 6, x0 + 40, 11):
        for wy in range(y0 + 32, y1 - 8, 13):
            draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(232, 226, 210))
    for wx in range(x1 - 38, x1 - 6, 11):
        for wy in range(y0 + 24, y1 - 8, 13):
            draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(226, 220, 204))
    # big round balloon (red-gold) with highlight + ropes
    cx, cy, r = (x0 + x1) // 2, y0 + 36, 28
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 34, 44))
    draw.ellipse([cx - r + 7, cy - r + 6, cx - r + 21, cy - r + 18],
                 fill=(226, 120, 110))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 160,
             fill=(120, 16, 22), width=3)
    for dx in (-18, 0, 18):
        draw.line([(cx + dx, cy + r - 3), (cx + dx // 2, y1 - 14)],
                  fill=(60, 50, 40), width=2)
    # street + crowd
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(74, 70, 66))
    draw.line([(x0, y1 - 12), (x1, y1 - 12)], fill=(240, 200, 60), width=2)
    rnd = random.Random(27)
    for _ in range(46):  # crowd dots along the kerb
        kx = rnd.randrange(x0 + 48, x1 - 48)
        ky = y1 - 20 + rnd.randrange(0, 5)
        draw.ellipse([kx, ky, kx + 4, ky + 4],
                     fill=rnd.choice([(26, 23, 18), (163, 22, 33),
                                      (31, 58, 95), (176, 132, 28)]))
    for _ in range(22):  # confetti
        jx = rnd.randrange(x0 + 50, x1 - 50)
        jy = rnd.randrange(y0 + 6, y1 - 26)
        draw.rectangle([jx, jy, jx + 4, jy + 2],
                       fill=rnd.choice([(163, 22, 33), (240, 200, 60),
                                        (31, 58, 95), (255, 255, 255)]))


ART = {"kyiv": art_kyiv, "gulf": art_gulf, "parade": art_parade}


# ------------------------------------------------------------------- map
# Coarse continent polygons in (lon, lat); equirectangular projection.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-60, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-117, 33), (-125, 40), (-125, 49), (-150, 60),
     (-168, 66)],
    # South America
    [(-79, 9), (-62, 9), (-52, 5), (-44, -3), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-74, -44),
     (-73, -30), (-77, -12), (-80, 0), (-79, 9)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (51, 11), (46, -1), (40, -15), (36, -26),
     (28, -33), (18, -35), (12, -18), (9, -1), (-8, 5), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 58), (12, 62),
     (20, 70), (35, 68), (50, 69), (70, 72), (100, 76), (130, 72),
     (160, 69), (178, 66), (162, 60), (142, 52), (135, 43), (127, 40),
     (122, 31), (110, 20), (105, 9), (98, 8), (92, 16), (88, 22),
     (80, 13), (76, 8), (70, 20), (62, 25), (56, 26), (50, 29),
     (44, 29), (36, 36), (27, 40), (20, 40), (12, 44), (3, 43),
     (-2, 37), (-10, 36)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (147, -19),
     (153, -27), (150, -37), (140, -38), (130, -32), (120, -34),
     (114, -30), (114, -22)],
]


def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    return (x0 + (lon + 180) / 360.0 * (x1 - x0),
            y0 + (90 - lat) / 180.0 * (y1 - y0))


# story number -> (lon, lat) pin for the map (leads + eight-more).
# Nudged apart where true positions collide at this scale
# (3/5 on the US east coast, 2/4 in the Gulf, 7/8/11 in Europe).
PINS = {1: (32, 50), 2: (53, 31), 3: (-70, 45), 4: (43, 11), 5: (-82, 35),
        6: (127, 40), 7: (-8, 56), 8: (28, 62), 9: (25, -2), 10: (0, 20),
        11: (18, 38)}


# ---------------------------------------------------------------- layout
def draw_masthead(img, draw):
    hline(draw, 24, W - 24, 26, fill=INK, width=3)
    draw.text((24, 34), "THE WORLD IN ONE PICTURE",
              font=font(SERIF_BLK, 58), fill=INK)
    draw.text((24, 96),
              "FRIDAY 27 NOVEMBER 2026  •  35 STORIES  •  10 REGIONS  •  15 FIELDS",
              font=font(SANS_B, 13), fill=RED)
    draw.text((W - 24, 100), "PRICE: ONE DAY",
              font=font(SANS_B, 11), fill=GREY, anchor="ra")
    hline(draw, 24, W - 24, 122, fill=INK, width=3)
    hline(draw, 24, W - 24, 126, fill=INK, width=1)


def draw_lead(draw, box, story):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    art_h = 90
    ART[story["art"]](draw, (x0 + 1, y0 + 1, x1 - 1, y0 + art_h))
    draw.rectangle([x0, y0 + art_h, x1, y0 + art_h + 20], fill=INK)
    draw.text((x0 + 8, y0 + art_h + 3), "LEAD %d" % story["n"],
              font=font(SANS_B, 11), fill=(240, 200, 60))
    badge(draw, x0 + 62, y0 + art_h + 4, story["badge"])
    ty = y0 + art_h + 26
    ty = para(draw, x0 + 8, ty, story["head"], font(SERIF_B, 18),
              x1 - x0 - 16, leading=21)
    ty = para(draw, x0 + 8, ty + 2, story["body"], font(SERIF, 11.5),
              x1 - x0 - 16, leading=14)
    draw.text((x0 + 8, y1 - 15), story["src"], font=font(SANS, 9),
              fill=GREY)


def draw_panel(draw, box, story):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    draw.rectangle([x0, y0, x0 + 30, y0 + 22], fill=RED)
    draw.text((x0 + 15, y0 + 3), str(story["n"]), font=font(SERIF_B, 14),
              fill=(255, 255, 255), anchor="ma")
    badge(draw, x0 + 36, y0 + 5, story["badge"])
    # head: at most 2 lines; body: at most 3 lines — never spill the box
    ty = y0 + 28
    for ln in wrap(draw, story["head"], font(SERIF_B, 12.5),
                   x1 - x0 - 16)[:2]:
        draw.text((x0 + 8, ty), ln, font=font(SERIF_B, 12.5), fill=INK)
        ty += 14
    blines = wrap(draw, story["body"], font(SERIF, 11), x1 - x0 - 16)
    if len(blines) > 3:
        blines = blines[:3]
        blines[2] = blines[2].rstrip() + "…"
    for ln in blines:
        draw.text((x0 + 8, ty + 1), ln, font=font(SERIF, 11), fill=INK)
        ty += 12


def draw_map_numbers(img, draw, box):
    x0, y0, x1, y1 = box
    mx0, my0, mx1, my1 = x0, y0, x0 + 596, y1
    nx0 = mx1 + 12
    draw.text((mx0, y0), "WHERE IT HAPPENED — 1 TO 11",
              font=font(SANS_B, 11), fill=INK)
    mapbox = (mx0, y0 + 18, mx1, y1 - 4)
    draw.rectangle(mapbox, outline=RULE, width=1, fill=(232, 226, 210))
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, mapbox) for lon, lat in poly]
        draw.polygon(pts, fill=(196, 178, 140), outline=(90, 80, 64))
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = lonlat_to_xy(lon, 0, mapbox)
        draw.line([(gx, mapbox[1]), (gx, mapbox[3])],
                  fill=(210, 202, 182), width=1)
    for lat in (-60, -30, 0, 30, 60):
        _, gy = lonlat_to_xy(0, lat, mapbox)
        draw.line([(mapbox[0], gy), (mapbox[2], gy)],
                  fill=(210, 202, 182), width=1)
    for n, (lon, lat) in sorted(PINS.items()):
        px, py = lonlat_to_xy(lon, lat, mapbox)
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((px, py - 1), str(n), font=font(SANS_B, 9),
                  fill=(255, 255, 255), anchor="mm")
    # BY THE NUMBERS column
    draw.text((nx0, y0), "BY THE NUMBERS", font=font(SANS_B, 11), fill=RED)
    hline(draw, nx0, x1, y0 + 16, fill=RED, width=2)
    yy = y0 + 20
    for big, small in NUMBERS:
        draw.text((nx0, yy), big, font=font(SERIF_BLK, 17), fill=INK)
        bw = draw.textlength(big, font=font(SERIF_BLK, 17))
        para(draw, nx0 + bw + 8, yy + 3, small, font(SERIF, 10),
             x1 - nx0 - bw - 8, leading=11)
        yy += 14
    return yy


def draw_rest(draw, y0, y1):
    """24 one-liners in 3 columns x 8 rows: number, one-line headline,
    small region/field/source line under it."""
    draw.text((24, y0), "THE REST — 24 MORE STORIES",
              font=font(SANS_B, 11), fill=INK)
    hline(draw, 24, W - 24, y0 + 16, fill=INK, width=2)
    col_w = (W - 48 - 32) // 3
    per_col = 8
    for ci in range(3):
        cx = 24 + ci * (col_w + 16)
        yy = y0 + 22
        for item in REST[ci * per_col:(ci + 1) * per_col]:
            n, region, field, bdg, head, src = item
            draw.text((cx, yy), "%d." % n, font=font(SERIF_B, 11),
                      fill=RED)
            tx = cx + 26
            f = font(SERIF, 10.5)
            line = head
            while draw.textlength(line, font=f) > col_w - 26 and len(line) > 10:
                line = line[:len(line) - 4].rstrip() + "…"
            draw.text((tx, yy), line, font=f, fill=INK)
            yy += 13
            draw.text((tx, yy), "%s · %s · %s" % (region, field, src),
                      font=font(SANS, 8), fill=GREY)
            yy += 10
    return y1


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(img, draw)

    # --- three leads: 132-356 ---------------------------------------
    ly0, ly1 = 132, 356
    lw = (W - 48 - 16) // 3
    for i, story in enumerate(LEADS):
        draw_lead(draw, (24 + i * (lw + 8), ly0,
                         24 + i * (lw + 8) + lw, ly1), story)

    # --- eight more: header 364, panels 386-542 ---------------------
    ey0 = 360
    draw.text((24, ey0), "EIGHT MORE", font=font(SANS_B, 11), fill=INK)
    hline(draw, 24, W - 24, ey0 + 16, fill=INK, width=2)
    pw = (W - 48 - 24) // 4
    ph = 94
    for i, story in enumerate(EIGHT):
        r, c = divmod(i, 4)
        x = 24 + c * (pw + 8)
        y = ey0 + 20 + r * (ph + 8)
        draw_panel(draw, (x, y, x + pw, y + ph), story)
    map_y0 = 584

    # --- map + numbers: 550-698 --------------------------------------
    map_y1 = map_y0 + 128
    draw_map_numbers(img, draw, (24, map_y0, W - 24, map_y1))

    # --- the rest: header 706, rows 728-892 --------------------------
    rest_y0 = 720
    draw_rest(draw, rest_y0, rest_y0 + 198)

    # --- timeline: one wrapped line ----------------------------------
    ty = 926
    hline(draw, 24, W - 24, ty, fill=INK, width=2)
    tl = "AROUND THE CLOCK:  " + "  ·  ".join(
        "%s — %s" % (w, t) for w, t in TIMELINE)
    para(draw, 24, ty + 6, tl, font(SERIF, 10), W - 48, leading=12)
    fy = 954

    # --- date check + footer -----------------------------------------
    draw.rectangle([24, fy, W - 24, fy + 34], outline=RED, width=2)
    draw.text((32, fy + 3), "DATE CHECK", font=font(SANS_B, 10), fill=RED)
    para(draw, 32, fy + 16, DATECHECK, font(SERIF, 9.5), W - 64, leading=11)
    fy2 = fy + 40
    draw.text((24, fy2), ALSO, font=font(SERIF, 9.5), fill=INK)
    fy3 = fy2 + 14
    hline(draw, 24, W - 24, fy3, fill=RULE, width=1)
    draw.text((24, fy3 + 4), SOURCES, font=font(SANS, 8), fill=GREY)

    grain(img)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    return img


def self_check():
    all_stories = LEADS + EIGHT + [
        dict(n=n, region=r, field=f) for (n, r, f, _b, _h, _s) in REST]
    assert len(all_stories) == 35, len(all_stories)
    assert len({s["n"] for s in all_stories}) == 35
    assert len({s["region"] for s in all_stories}) == 10, \
        sorted({s["region"] for s in all_stories})
    assert len({s["field"] for s in all_stories}) == 15, \
        sorted({s["field"] for s in all_stories})
    assert sorted(s["n"] for s in all_stories) == list(range(1, 36))
    data = open(OUT, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    assert data.endswith(b"IEND\xaeB`\x82")
    assert len(data) <= 1048576, len(data)
    im = Image.open(OUT)
    assert im.size == (1024, 1024), im.size
    h = hashlib.sha256(data).hexdigest()
    print("OK 35 stories, 10 regions, 15 fields")
    print("PNG %d bytes sha256 %s" % (len(data), h))
    return h


if __name__ == "__main__":
    build()
    self_check()
