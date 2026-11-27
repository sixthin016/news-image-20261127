"""news-image-20261127 — render Friday 27 November 2026's world news
as one 1024x1024 newspaper front page (PIL, deterministic). Revision 2.

Slate: 35 stories = 3 leads + 8 panels + 24 one-liners, 10 regions,
15 fields. The slate follows the Friday news cycle: stories first
reported overnight into Friday 27 Nov 2026, plus the day's own
events (Black Friday, the NZ final count, the Amazon walkouts).
Items that belong clearly to 26 Nov or earlier and were already
resolved are NOT in the slate; they are named in the red DATE
CHECK box instead.

Layout v2: masthead + one-line deck, a six-number strip, a regions
and fields bar, a UTC strip, three illustrated leads, eight
illustrated panels (11 drawn scenes in all), a full map, 24 more
stories, and a date check with a how-we-checked legend. Every
scene is drawn in code; no photo, no network, no randomness
beyond seeded grain.
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
TEAL = (36, 90, 86)
SEA = (24, 68, 92)
SAND = (222, 200, 150)
SHOP = (208, 182, 138)
BRICK = (122, 52, 44)
CREAM = (238, 230, 208)
NAVY = (22, 38, 66)

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
    dict(n=1, region="Middle East", field="War", badge="REPORTED",
         art="gulf",
         head="DRONE STRIKE KILLS TWO ITALIANS IN KUWAIT",
         body=("Kuwait says an Iranian drone hit a defence site, killing "
               "two Italian technicians; Iran denies any role. Two "
               "tankers are hit by sea mines off Oman."),
         why="A Gulf ally is struck directly for the first time.",
         src="Kuwait Defence Ministry / reports"),
    dict(n=2, region="N. America", field="Markets", badge="FORECAST",
         art="store",
         head="BLACK FRIDAY OPENS: $12.9BN DAY AHEAD",
         body=("Adobe forecasts $12.9bn in US online sales today, up "
               "9.2% on last year; 126 million Americans plan to shop. "
               "Stores open at 06:00 ET."),
         why="The biggest shopping day tests the consumer economy.",
         src="Adobe / NRF"),
    dict(n=3, region="Middle East", field="War", badge="REPORTED",
         art="gaza",
         head="HAMAS WEIGHS REPLY AFTER 10 DIE IN GAZA",
         body=("Israeli strikes kill 10 people in Gaza, medics say, as "
               "Hamas consults other factions on a reply. A strike on "
               "Deir al-Balah kills Hamas official Khaled Abu Nada."),
         why="The ceasefire holds by a thread; the reply decides.",
         src="Reuters / medics"),
]

EIGHT = [
    dict(n=4, region="Europe", field="War", badge="CONFIRMED",
         art="barrage",
         head="RUSSIA'S OVERNIGHT BARRAGE KILLS AT LEAST 3",
         body=("Missiles and drones hit Ukraine overnight, Kyiv among "
               "the targets. Ukraine hits back at a Su-34 airbase in "
               "Volgograd and refineries at Syzran and Kuibyshev."),
         why="Both sides widen the war to each other's home ground.",
         src="Reports, 27 Nov 00:21 UTC"),
    dict(n=5, region="Oceania", field="Politics", badge="OFFICIAL",
         art="ballot",
         head="NZ VOTE ENDS IN DEADLOCK",
         body=("The final count leaves the coalition on 65 seats, one "
               "short of a majority. The seven-seat Opportunity Party "
               "now holds the keys to power."),
         why="A new party of seven MPs decides who governs New Zealand.",
         src="Electoral Commission"),
    dict(n=6, region="Europe", field="Disaster", badge="REPORTED",
         art="tanker",
         head="TANKER CAPSIZES OFF IBIZA, ONE DEAD",
         body=("The chemical tanker Med Emre capsized off Ibiza with up "
               "to 7,000 tonnes of diesel aboard. Seventeen crew were "
               "rescued; one died. Spain raises its pollution alert."),
         why="A fuel spill would hit Ibiza's coast and tourist season.",
         src="Reuters / Balearic Islands"),
    dict(n=7, region="Europe", field="Sport", badge="OFFICIAL",
         art="chess",
         head="GUKESH-SINDAROV GAME 3 ENDS DRAWN",
         body=("World champion Gukesh and Sindarov drew in 60 moves in "
               "Geneva, leaving the match level at 1.5-1.5. Game 4 is "
               "on Saturday; today is a rest day."),
         why="The title match stays level heading into the weekend.",
         src="FIDE / Chess.com"),
    dict(n=8, region="Europe", field="Law", badge="OFFICIAL",
         art="court",
         head="DEPARDIEU TO STAND TRIAL FOR RAPE",
         body=("A Paris court orders Gerard Depardieu, 77, to stand "
               "trial over an alleged rape in 2018. He denies the "
               "charge and faces 15 to 20 years if convicted."),
         why="France's biggest #MeToo trial is now a certainty.",
         src="Reuters / Paris court"),
    dict(n=9, region="Global", field="Business", badge="REPORTED",
         art="warehouse",
         head="AMAZON WORKERS STRIKE IN 20 COUNTRIES",
         body=("Workers and supporters protest from Friday to Monday in "
               "over 20 countries. Germany's ver.di strikes at 11 "
               "Amazon sites on Friday morning."),
         why="A strike timed for Black Friday hits Amazon's biggest days.",
         src="UNI Global Union"),
    dict(n=10, region="N. America", field="Politics", badge="REPORTED",
         art="chart",
         head="TRUMP SEEKS PROBE INTO 'FAKE' GDP",
         body=("Trump demands an immediate probe, claiming without "
               "evidence the Commerce Dept. released 'fake' growth "
               "figures. The BEA revised Q3 growth up to 4.3%."),
         why="The claim targets the figures that undercut his midterm story.",
         src="Reuters / Truth Social"),
    dict(n=11, region="Europe", field="Migration", badge="OFFICIAL",
         art="border",
         head="UK MIGRATION FALLS TO NEAR 30-YEAR LOW",
         body=("Net migration hits its lowest outside Covid; jets go "
               "into hardened shelters; 100,000 reservists are told to "
               "be ready."),
         why="The numbers land as Britain's defence posture hardens.",
         src="ONS / reports"),
]

REST = [
    (12, "Middle East", "War", "REPORTED",
     "Houthis push on Aden as alarm grows",
     "Aden / Sanaa"),
    (13, "N. America", "Diplomacy", "REPORTED",
     "Trump and Rutte warn Russia not to escalate",
     "Washington / The Hague"),
    (14, "E. Asia", "War", "REPORTED",
     "Kim vows 'uncontrollable' nuclear build-up",
     "Pyongyang"),
    (15, "Europe", "Defence", "REPORTED",
     "Neighbours of Russia quit landmine ban",
     "Warsaw / Helsinki"),
    (16, "Africa", "Health", "REPORTED",
     "Ebola in Congo passes 12,000 cases",
     "Kinshasa"),
    (17, "Global", "Markets", "REPORTED",
     "Stocks slide as tariffs bite",
     "Markets"),
    (18, "Europe", "Defence", "REPORTED",
     "Ukraine to get Italy's Eurofighter jets",
     "Rome / Kyiv"),
    (19, "N. America", "Culture", "OFFICIAL",
     "Parade eve: Macy's 100th set for Saturday",
     "New York"),
    (20, "Europe", "Diplomacy", "REPORTED",
     "Zelensky questions Trump's peace timetable",
     "Kyiv interview"),
    (21, "Europe", "War", "OFFICIAL",
     "Ukraine gets remains of 250 fallen soldiers",
     "Deal with Russia"),
    (22, "Middle East", "War", "REPORTED",
     "Russia said to plan sea strikes from Libya",
     "Moscow / Tripoli"),
    (23, "Europe", "War", "REPORTED",
     "Ukrainian sea drones hit two Russian vessels",
     "Kyiv / Brussels"),
    (24, "Middle East", "War", "CLAIM",
     "IDF ready to strike Iran if needed",
     "IDF / reports"),
    (25, "Middle East", "Health", "REPORTED",
     "Gaza health chiefs warn on reproductive care",
     "Gaza health ministry"),
    (26, "Middle East", "Politics", "REPORTED",
     "Israel builds settlement road near Bethlehem",
     "Reports"),
    (27, "Middle East", "Energy", "CLAIM",
     "Two tankers hit by mines off Oman; oil falls",
     "IRGC / markets"),
    (28, "Middle East", "Diplomacy", "REPORTED",
     "Qatar: US-Iran mediation still on track",
     "Doha"),
    (29, "S. America", "Security", "REPORTED",
     "Guatemala reinforces frontiers vs crime gangs",
     "Guatemala City"),
    (30, "SE Asia", "Disaster", "REPORTED",
     "13 dead as flood hits illegal Indonesia mine",
     "Jakarta"),
    (31, "S. Asia", "Business", "REPORTED",
     "India and China reopen border trade",
     "New Delhi / Beijing"),
    (32, "Europe", "Security", "REPORTED",
     "Estonia to shut rail border; France cyber warning",
     "Tallinn / Paris"),
    (33, "Europe", "Diplomacy", "REPORTED",
     "Dutch PM: EU states may opt out of Ukraine aid",
     "The Hague"),
    (34, "N. America", "Climate", "REPORTED",
     "Super El Nino sends historic surf to California",
     "California"),
    (35, "Global", "Sport", "OFFICIAL",
     "Sinner pulls out of Australian Open, knee injury",
     "Melbourne"),
]

NUMBERS = [
    ("2", "Italians killed in Kuwait"),
    ("$12.9B", "Black Friday sales forecast"),
    ("126M", "Americans shopping today"),
    ("10", "killed in Gaza"),
    ("7,000", "tonnes of diesel off Ibiza"),
    ("65", "NZ coalition seats, 1 short"),
]
NUMBERS_TOP = [
    ("2", "Kuwait"), ("$12.9B", "Black Friday"), ("126M", "Shoppers"),
    ("10", "Gaza"), ("7,000T", "Ibiza diesel"), ("65", "NZ seats"),
]

TIMELINE = [
    ("00:04 UTC", "Hamas weighs its reply"),
    ("00:21 UTC", "Russia barrage reported"),
    ("MORNING", "NZ final count lands"),
    ("11:00 UTC", "US stores open for Black Friday"),
    ("FRIDAY", "Amazon walkouts begin"),
    ("FRIDAY NIGHT", "Balloons go up for parade"),
]

DATECHECK = ("NOT 27 NOVEMBER — left out on purpose: Bangkok refinery fire, "
             "9 hurt (26 Nov) · Cairo tanker fire, 31 dead (26 Nov) · ECB "
             "set to pick de Cos (26 Nov) · US $622M F-16 deal for Ukraine "
             "(26 Nov) · Macy's postponement announced (25 Nov) · Gaza "
             "drone strike kills 3 (26 Nov morning) · US tells citizens "
             "to leave Iran (25 Nov).")
HOWCHECKED = ("HOW WE CHECKED: first reports dated 27 Nov 2026 in some "
              "time zone; overnight items that broke into Friday count; "
              "earlier items listed above.")

ALSO = ("ALSO: Jolie-Pitt settle winery suit · AA flight rerouted after "
        "exit-door scare · NATO staffer held in Belgium.")

SOURCES = ("Sources: Reuters, AP, Bloomberg, CNN, USA TODAY, BBC, Al Jazeera, "
           "The Guardian, Adobe, NRF, NZ Electoral Commission. All stories "
           "first reported 27 Nov 2026 in some time zone.")


# ------------------------------------------------------------------- art
def sky_gradient(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = y1 - y0
    for i in range(n):
        t = i / max(1, n - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def art_store(draw, box):
    """Black Friday storefront at dawn: striped awning, glowing window,
    red SALE disc, door, queue of shoppers with bags. Box is 54 px tall."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (206, 164, 110), (238, 214, 170))
    draw.rectangle([x0, y0 + 18, x1, y1], fill=BRICK)
    for i in range(12):  # striped awning
        ax = x0 + i * 26
        draw.polygon([(ax, y0 + 18), (ax + 26, y0 + 18), (ax + 26, y0 + 26),
                      (ax + 13, y0 + 30), (ax, y0 + 26)],
                     fill=(240, 200, 60) if i % 2 == 0 else (178, 34, 44))
    draw.rectangle([x0 + 14, y0 + 32, x0 + 150, y1 - 8], fill=(255, 236, 180))
    draw.rectangle([x0 + 20, y0 + 34, x0 + 144, y1 - 10], fill=(120, 90, 60))
    cx, cy = x0 + 205, y0 + 28  # SALE disc
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(178, 34, 44),
                 outline=(255, 255, 255), width=2)
    draw.text((cx, cy), "SALE", font=font(SANS_B, 9), fill=(255, 255, 255),
              anchor="mm")
    draw.rectangle([x0 + 250, y0 + 32, x0 + 296, y1 - 8], fill=(40, 30, 24))
    draw.rectangle([x0 + 258, y0 + 34, x0 + 288, y1 - 10], fill=(255, 236, 180))
    draw.rectangle([x0, y1 - 6, x1, y1], fill=(90, 84, 76))  # pavement
    rnd = random.Random(41)  # queue of shoppers
    for _ in range(12):
        qx = rnd.randrange(x0 + 160, x1 - 12)
        qy = y1 - 5 + rnd.randrange(0, 2)
        draw.ellipse([qx, qy, qx + 4, qy + 4],
                     fill=rnd.choice([(26, 23, 18), (163, 22, 33),
                                      (31, 58, 95), (176, 132, 28)]))


def art_gaza(draw, box):
    """Gaza at dusk: amber-grey sky, broken skyline, smoke columns,
    one lit window in the dark. Box is 54 px tall."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (168, 128, 92), (96, 84, 74))
    draw.ellipse([x1 - 46, y0 + 4, x1 - 14, y0 + 30], fill=(232, 200, 150))
    rnd = random.Random(23)
    bx = x0
    while bx < x1 - 10:  # broken skyline, uneven tops
        bw = rnd.choice([22, 30, 38, 46])
        bh = rnd.choice([20, 28, 36, 40])
        top = y1 - bh
        draw.rectangle([bx, top, bx + bw, y1], fill=(52, 44, 40))
        draw.polygon([(bx, top), (bx + bw // 2, top - 6),
                      (bx + bw, top)], fill=(52, 44, 40))
        if rnd.random() < 0.5:
            draw.rectangle([bx + 6, top + 6, bx + 12, top + 11],
                           fill=(255, 196, 90))
        bx += bw + rnd.choice([3, 6, 9])
    for (sx, sy) in [(x0 + 70, y0 + 26), (x0 + 190, y0 + 22)]:  # smoke
        for i in range(3):
            r = 3 + i * 2
            cy = sy - i * 6
            draw.ellipse([sx - r, cy - r, sx + r, cy + r],
                         outline=(60, 54, 48), width=2)


def art_gulf(draw, box):
    """Dusk over the Gulf: amber sky, dark sea, tanker silhouette,
    drone dots, mine splash rings."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (214, 158, 92), (120, 84, 66))
    draw.ellipse([x1 - 52, y0 + 8, x1 - 16, y0 + 44], fill=(255, 226, 170))
    horizon = y0 + int((y1 - y0) * 0.55)
    draw.rectangle([x0, horizon, x1, y1], fill=(28, 42, 58))
    for i in range(3):  # sun glitter on water
        yy = horizon + 5 + i * 6
        draw.line([(x0 + 30 + i * 8, yy), (x1 - 40 - i * 6, yy)],
                  fill=(214, 158, 92), width=2)
    # tanker silhouette
    draw.rectangle([x0 + 34, horizon - 16, x0 + 190, horizon + 2],
                   fill=(10, 14, 20))
    draw.rectangle([x0 + 60, horizon - 26, x0 + 78, horizon - 16],
                   fill=(10, 14, 20))
    draw.rectangle([x0 + 150, horizon - 24, x0 + 162, horizon - 16],
                   fill=(10, 14, 20))
    # smoke column from tanker (kept inside the box)
    for i in range(3):
        r = 2 + i * 2
        cy = horizon - 10 - i * 4
        draw.ellipse([x0 + 66 - r, cy - r, x0 + 66 + r, cy + r],
                     outline=(70, 60, 52), width=2)
    # drones + mine splash rings
    for (dx, dy) in [(x0 + 230, y0 + 26), (x0 + 262, y0 + 44),
                     (x0 + 286, y0 + 18)]:
        draw.ellipse([dx - 3, dy - 2, dx + 3, dy + 2], fill=(12, 12, 14))
        draw.line([(dx - 8, dy), (dx + 8, dy)], fill=(12, 12, 14), width=1)
    for (sx, sy, r) in [(x0 + 250, horizon + 12, 8),
                        (x0 + 285, horizon + 18, 6)]:
        draw.ellipse([sx - r, sy - r // 2, sx + r, sy + r // 2],
                     outline=(220, 220, 210), width=2)


def art_barrage(draw, box):
    """Night barrage: dark sky, two missile arcs, one blast glow."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (14, 22, 46), (52, 62, 96))
    for (ax, ay, bx, by, cx, cy) in [
            (x0 + 10, y1 - 4, x0 + 80, y0 + 6, x0 + 150, y1 - 12),
            (x0 + 90, y1 - 2, x0 + 160, y0 + 4, x0 + 220, y1 - 16)]:
        pts = []
        for t in [i / 16 for i in range(17)]:
            px = (1 - t) ** 2 * ax + 2 * (1 - t) * t * bx + t * t * cx
            py = (1 - t) ** 2 * ay + 2 * (1 - t) * t * by + t * t * cy
            pts.append((px, py))
        draw.line(pts, fill=(240, 220, 160), width=2)
    draw.ellipse([x0 + 150 - 8, y1 - 20, x0 + 150 + 8, y1 - 4],
                 fill=(232, 110, 32))
    draw.ellipse([x0 + 150 - 4, y1 - 16, x0 + 150 + 4, y1 - 8],
                 fill=(255, 214, 120))
    draw.rectangle([x0, y1 - 6, x1, y1], fill=(8, 12, 26))


def art_ballot(draw, box):
    """Ballot box: pale paper, dark box, slot, paper slip, green tick."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 230, 208))
    draw.text((x0 + 8, y0 + 8), "VOTE", font=font(SANS_B, 10), fill=INK)
    draw.rectangle([x0 + 84, y0 + 10, x0 + 146, y1 - 4], fill=(31, 58, 95))
    draw.rectangle([x0 + 96, y0 + 10, x0 + 134, y0 + 14], fill=(238, 230, 208))
    draw.rectangle([x0 + 108, y0 + 2, x0 + 122, y0 + 10], fill=(255, 255, 255),
                   outline=(90, 80, 64))
    draw.line([(x0 + 160, y0 + 20), (x0 + 170, y1 - 8), (x0 + 196, y0 + 6)],
              fill=(34, 120, 60), width=3)


def art_tanker(draw, box):
    """Capsized tanker: grey sea, tilted hull, lifeboat, splash ring."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (158, 188, 214), (214, 226, 236))
    draw.rectangle([x0, y0 + 14, x1, y1], fill=SEA)
    draw.line([(x0, y0 + 14), (x1, y0 + 14)], fill=(210, 202, 182), width=1)
    draw.polygon([(x0 + 40, y0 + 16), (x0 + 150, y0 + 10),
                  (x0 + 150, y0 + 18), (x0 + 40, y0 + 24)], fill=(20, 24, 30))
    draw.rectangle([x0 + 60, y0 + 8, x0 + 72, y0 + 14], fill=(20, 24, 30))
    draw.rectangle([x0 + 168, y0 + 18, x0 + 196, y0 + 24], fill=(214, 110, 40))
    draw.ellipse([x0 + 170, y0 + 14, x0 + 194, y0 + 20],
                 outline=(220, 220, 210), width=1)


def art_chess(draw, box):
    """Chessboard strip: 8 alternating squares, two pieces."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 230, 208))
    sq = (x1 - x0) // 8
    for i in range(8):
        if i % 2 == 0:
            draw.rectangle([x0 + i * sq, y0, x0 + (i + 1) * sq, y0 + 14],
                           fill=(31, 58, 95))
        else:
            draw.rectangle([x0 + i * sq, y0 + 14, x0 + (i + 1) * sq, y1],
                           fill=(31, 58, 95))
    draw.ellipse([x0 + 30, y0 + 6, x0 + 48, y0 + 24], fill=(255, 255, 255),
                 outline=(20, 20, 20), width=1)
    draw.ellipse([x0 + 180, y0 + 6, x0 + 198, y0 + 24], fill=(20, 20, 20),
                 outline=(255, 255, 255), width=1)


def art_court(draw, box):
    """Courthouse: dark navy, three columns, pediment, steps."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY)
    draw.polygon([(x0 + 70, y0 + 4), (x0 + 160, y0 + 4), (x0 + 115, y0 + 12)],
                 fill=(238, 230, 208))
    for cx in (x0 + 80, x0 + 108, x0 + 136):
        draw.rectangle([cx, y0 + 12, cx + 10, y1 - 4], fill=(238, 230, 208))
    draw.rectangle([x0 + 60, y1 - 4, x0 + 170, y1], fill=(238, 230, 208))


def art_warehouse(draw, box):
    """Amazon warehouse: grey front, big door, picket sign, boxes."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (180, 190, 200), (220, 224, 228))
    draw.rectangle([x0 + 20, y0 + 8, x0 + 180, y1 - 4], fill=(90, 96, 104))
    draw.rectangle([x0 + 20, y0 + 8, x0 + 180, y0 + 12], fill=(60, 64, 70))
    draw.rectangle([x0 + 80, y0 + 14, x0 + 120, y1 - 4], fill=(40, 44, 50))
    draw.rectangle([x0 + 130, y0 + 14, x0 + 168, y0 + 22], fill=(255, 236, 180))
    draw.rectangle([x0 + 192, y0 + 6, x0 + 196, y1 - 6], fill=(60, 50, 40))
    draw.rectangle([x0 + 182, y0 + 4, x0 + 206, y0 + 12], fill=(255, 255, 255),
                   outline=RED, width=1)
    draw.rectangle([x0 + 188, y0 + 6, x0 + 200, y0 + 10], fill=RED)


def art_chart(draw, box):
    """GDP chart: rising bars, one red falling bar, trend line."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 230, 208))
    for (bx, bh) in [(x0 + 16, 10), (x0 + 52, 14), (x0 + 88, 18),
                     (x0 + 124, 8), (x0 + 160, 16), (x0 + 196, 12)]:
        draw.rectangle([bx, y1 - 4 - bh, bx + 24, y1 - 4], fill=(31, 58, 95))
    draw.rectangle([x0 + 124, y1 - 12, x0 + 148, y1 - 4], fill=(178, 34, 44))
    draw.line([(x0 + 16, y1 - 14), (x0 + 208, y1 - 22)], fill=(214, 110, 40),
              width=2)


def art_border(draw, box):
    """Border fence: pale sky, fence posts, barrier, UK sign."""
    x0, y0, x1, y1 = box
    sky_gradient(draw, box, (180, 200, 220), (228, 232, 236))
    draw.rectangle([x0, y1 - 6, x1, y1], fill=(120, 110, 96))
    for px in range(x0 + 8, x1 - 8, 22):
        draw.rectangle([px, y0 + 6, px + 4, y1 - 6], fill=(60, 56, 50))
    draw.line([(x0, y0 + 10), (x1, y0 + 10)], fill=(60, 56, 50), width=2)
    draw.line([(x0, y0 + 18), (x1, y0 + 18)], fill=(60, 56, 50), width=2)
    draw.rectangle([x0 + 100, y0 + 8, x0 + 130, y0 + 20], fill=(255, 255, 255),
                   outline=RED, width=1)
    draw.text((x0 + 115, y0 + 9), "UK", font=font(SANS_B, 8), fill=RED,
              anchor="ma")


ART = {"gulf": art_gulf, "store": art_store, "gaza": art_gaza}
PANEL_ART = {"barrage": art_barrage, "ballot": art_ballot,
             "tanker": art_tanker, "chess": art_chess,
             "court": art_court, "warehouse": art_warehouse,
             "chart": art_chart, "border": art_border}


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
# (Gaza/Kyiv, and the London/Paris/Geneva/Berlin/Ibiza cluster).
PINS = {1: (53, 31), 2: (-70, 44), 3: (40, 27), 4: (33, 55), 5: (175, -41),
        6: (2, 32), 7: (8, 42), 8: (-4, 50), 9: (22, 59), 10: (-84, 34),
        11: (-14, 58)}


# ---------------------------------------------------------------- layout
def draw_masthead(img, draw):
    hline(draw, 24, W - 24, 26, fill=INK, width=3)
    draw.text((24, 32), "THE WORLD IN ONE PICTURE",
              font=font(SERIF_BLK, 54), fill=INK)
    draw.text((24, 92),
              "FRIDAY 27 NOVEMBER 2026  •  35 STORIES  •  10 REGIONS  •  15 FIELDS",
              font=font(SANS_B, 13), fill=RED)
    draw.text((W - 24, 96), "PRICE: ONE DAY",
              font=font(SANS_B, 11), fill=GREY, anchor="ra")
    draw.text((24, 107),
              "A drone strike in Kuwait, a $12.9bn shopping day, and a "
              "ceasefire hanging by a thread — Friday in one picture.",
              font=font(SERIF, 11.5), fill=INK)
    hline(draw, 24, W - 24, 122, fill=INK, width=3)
    hline(draw, 24, W - 24, 126, fill=INK, width=1)


def draw_lead(draw, box, story):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    art_h = 48
    ART[story["art"]](draw, (x0 + 1, y0 + 1, x1 - 1, y0 + art_h))
    draw.rectangle([x0, y0 + art_h, x1, y0 + art_h + 16], fill=INK)
    draw.text((x0 + 8, y0 + art_h + 2), "LEAD %d" % story["n"],
              font=font(SANS_B, 11), fill=(240, 200, 60))
    badge(draw, x0 + 62, y0 + art_h + 2, story["badge"])
    ty = y0 + art_h + 20
    ty = para(draw, x0 + 8, ty, "%s · %s" % (story["region"].upper(),
              story["field"].upper()), font(SANS_B, 9), x1 - x0 - 16,
              leading=10)
    ty = para(draw, x0 + 8, ty + 1, story["head"], font(SERIF_B, 17),
              x1 - x0 - 16, leading=19)
    blines = wrap(draw, story["body"], font(SERIF, 11), x1 - x0 - 16)
    if len(blines) > 3:
        blines = blines[:3]
        blines[2] = blines[2].rstrip() + "…"
    for ln in blines:
        draw.text((x0 + 8, ty + 1), ln, font=font(SERIF, 11), fill=INK)
        ty += 12.5
    why = "WHY: " + story["why"]
    f = font(SERIF, 10)
    while draw.textlength(why, font=f) > x1 - x0 - 16 and len(why) > 10:
        why = why[:len(why) - 4].rstrip() + "…"
    draw.text((x0 + 8, y1 - 26), why, font=f, fill=RED)
    draw.text((x0 + 8, y1 - 14), story["src"], font=font(SANS, 9),
              fill=GREY)


def draw_panel(draw, box, story):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    scene_h = 24
    PANEL_ART[story["art"]](draw, (x0 + 1, y0 + 1, x1 - 1, y0 + scene_h))
    draw.rectangle([x0 + 2, y0 + 2, x0 + 22, y0 + 16], fill=RED)
    draw.text((x0 + 12, y0 + 3), str(story["n"]), font=font(SERIF_B, 11),
              fill=(255, 255, 255), anchor="ma")
    badge(draw, x0 + 26, y0 + 3, story["badge"])
    # head: at most 2 lines; body: at most 2 lines — never spill the box
    ty = y0 + scene_h + 4
    for ln in wrap(draw, story["head"], font(SERIF_B, 12),
                   x1 - x0 - 16)[:2]:
        draw.text((x0 + 8, ty), ln, font=font(SERIF_B, 12), fill=INK)
        ty += 14
    blines = wrap(draw, story["body"], font(SERIF, 10.5), x1 - x0 - 16)
    if len(blines) > 2:
        blines = blines[:2]
        blines[1] = blines[1].rstrip() + "…"
    for ln in blines:
        draw.text((x0 + 8, ty + 1), ln, font=font(SERIF, 10.5), fill=INK)
        ty += 12
    wlines = wrap(draw, "WHY: " + story["why"], font(SERIF, 9),
                  x1 - x0 - 16)
    if len(wlines) > 2:
        wlines = wlines[:2]
        wlines[1] = wlines[1].rstrip() + "…"
    wy = y1 - 23
    for ln in wlines:
        draw.text((x0 + 8, wy), ln, font=font(SERIF, 9), fill=RED)
        wy += 11


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
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((px, py - 1), str(n), font=font(SANS_B, 8),
                  fill=(255, 255, 255), anchor="mm")
    # BY THE NUMBERS column: 6 rows, big number + one-line caption,
    # 15 px step so rows never overlap (v1 used 14 px and collided).
    draw.text((nx0, y0), "BY THE NUMBERS", font=font(SANS_B, 11), fill=RED)
    hline(draw, nx0, x1, y0 + 16, fill=RED, width=2)
    yy = y0 + 20
    for big, small in NUMBERS:
        draw.text((nx0, yy), big, font=font(SERIF_BLK, 14), fill=INK)
        bw = draw.textlength(big, font=font(SERIF_BLK, 14))
        cap = small
        f = font(SERIF, 9.5)
        while draw.textlength(cap, font=f) > x1 - nx0 - bw - 8 \
                and len(cap) > 10:
            cap = cap[:len(cap) - 4].rstrip() + "…"
        draw.text((nx0 + bw + 8, yy + 2), cap, font=f, fill=INK)
        yy += 15
    return yy


def draw_rest(draw, y0, y1):
    """24 one-liners in 3 columns x 8 rows: number, one-line headline,
    small region/field/source line under it. Rows are 16.5 px so all
    eight fit above the date check."""
    draw.text((24, y0), "THE REST — 24 MORE STORIES",
              font=font(SANS_B, 11), fill=INK)
    hline(draw, 24, W - 24, y0 + 16, fill=INK, width=2)
    col_w = (W - 48 - 32) // 3
    per_col = 8
    for ci in range(3):
        cx = 24 + ci * (col_w + 16)
        yy = y0 + 20
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
            yy += 10
            draw.text((tx, yy), "%s · %s · %s" % (region, field, src),
                      font=font(SANS, 8), fill=GREY)
            yy += 6.5
    return y1


def draw_numbers_strip(draw, y0):
    """Six-number strip right under the masthead: big figure + label."""
    cell_w = (W - 48) // 6
    for i, (big, small) in enumerate(NUMBERS_TOP):
        cx = 24 + i * cell_w
        if i:
            vline(draw, cx - 4, y0 + 2, y0 + 28, fill=RULE, width=1)
        draw.text((cx + 8, y0), big, font=font(SERIF_BLK, 19), fill=INK)
        draw.text((cx + 8, y0 + 22), small.upper(), font=font(SANS_B, 8),
                  fill=GREY)
    hline(draw, 24, W - 24, y0 + 30, fill=INK, width=2)


def draw_regions_bar(draw, y0):
    """Counted region and field bars, computed from the slate itself."""
    all_stories = LEADS + EIGHT + [
        dict(n=n, region=r, field=f) for (n, r, f, _b, _h, _s) in REST]
    rc, fc = {}, {}
    for s in all_stories:
        rc[s["region"]] = rc.get(s["region"], 0) + 1
        fc[s["field"]] = fc.get(s["field"], 0) + 1
    regs = sorted(rc.items(), key=lambda kv: (-kv[1], kv[0]))
    flds = sorted(fc.items(), key=lambda kv: (-kv[1], kv[0]))
    draw.text((24, y0),
              "REGIONS (%d): " % len(rc) + " · ".join(
                  "%s %d" % kv for kv in regs),
              font=font(SANS_B, 9), fill=INK)
    draw.text((24, y0 + 11),
              "FIELDS (%d): " % len(fc) + " · ".join(
                  "%s %d" % kv for kv in flds),
              font=font(SANS_B, 9), fill=INK)
    hline(draw, 24, W - 24, y0 + 22, fill=INK, width=1)


def draw_utc_strip(draw, y0):
    """UTC strip: red dots on a rule, time above, event below."""
    hline(draw, 24, W - 24, y0 + 14, fill=RULE, width=1)
    f_time = font(SANS_B, 9)
    f_ev = font(SERIF, 9)
    for i, (when, what) in enumerate(TIMELINE):
        dx = 104 + i * 160
        draw.ellipse([dx - 4, y0 + 10, dx + 4, y0 + 18], fill=RED)
        draw.text((dx, y0), when, font=f_time, fill=RED, anchor="ma")
        ev = what
        while draw.textlength(ev, font=f_ev) > 150 and len(ev) > 10:
            ev = ev[:len(ev) - 4].rstrip() + "…"
        draw.text((dx, y0 + 21), ev, font=f_ev, fill=INK, anchor="ma")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(img, draw)

    # --- six-number strip: 130-160 ----------------------------------
    draw_numbers_strip(draw, 130)

    # --- regions + fields bar: 164-186 -------------------------------
    draw_regions_bar(draw, 164)

    # --- UTC strip: 190-218 ------------------------------------------
    draw_utc_strip(draw, 190)

    # --- three leads: 222-414 ----------------------------------------
    ly0, ly1 = 222, 414
    lw = (W - 48 - 16) // 3
    for i, story in enumerate(LEADS):
        draw_lead(draw, (24 + i * (lw + 8), ly0,
                         24 + i * (lw + 8) + lw, ly1), story)

    # --- eight more: header 422, panels 442-662 ----------------------
    ey0 = 422
    draw.text((24, ey0), "EIGHT MORE", font=font(SANS_B, 11), fill=INK)
    hline(draw, 24, W - 24, ey0 + 16, fill=INK, width=2)
    pw = (W - 48 - 24) // 4
    ph = 106
    for i, story in enumerate(EIGHT):
        r, c = divmod(i, 4)
        x = 24 + c * (pw + 8)
        y = ey0 + 20 + r * (ph + 8)
        draw_panel(draw, (x, y, x + pw, y + ph), story)

    # --- map + numbers: 668-778 --------------------------------------
    draw_map_numbers(img, draw, (24, 668, W - 24, 778))

    # --- the rest: header 784, rows 804-936 --------------------------
    draw_rest(draw, 784, 936)

    # --- date check + footer -----------------------------------------
    fy = 942
    draw.rectangle([24, fy, W - 24, fy + 52], outline=RED, width=2)
    draw.text((32, fy + 3), "DATE CHECK", font=font(SANS_B, 10), fill=RED)
    ty = para(draw, 32, fy + 16, DATECHECK, font(SERIF, 9.5), W - 64,
              leading=11)
    para(draw, 32, ty + 2, HOWCHECKED, font(SERIF, 9.5), W - 64,
         leading=11)
    fy2 = fy + 56
    draw.text((24, fy2), ALSO, font=font(SERIF, 9.5), fill=INK)
    fy3 = fy2 + 12
    hline(draw, 24, W - 24, fy3, fill=RULE, width=1)
    draw.text((24, fy3 + 3), SOURCES, font=font(SANS, 8), fill=GREY)

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
    # v2 structure: 3 illustrated leads + 8 illustrated panels = 11 scenes
    assert len(NUMBERS) == 6, len(NUMBERS)
    assert len(NUMBERS_TOP) == 6, len(NUMBERS_TOP)
    assert len(TIMELINE) == 6, len(TIMELINE)
    assert sorted(PINS) == list(range(1, 12)), sorted(PINS)
    assert set(ART) == {"gulf", "store", "gaza"}, sorted(ART)
    assert set(PANEL_ART) == {"barrage", "ballot", "tanker", "chess",
                              "court", "warehouse", "chart", "border"}, \
        sorted(PANEL_ART)
    for s in LEADS:
        assert s["art"] in ART, s["n"]
        assert s.get("why"), s["n"]
    for s in EIGHT:
        assert s["art"] in PANEL_ART, s["n"]
        assert s.get("why"), s["n"]
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
