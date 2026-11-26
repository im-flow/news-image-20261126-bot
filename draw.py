#!/usr/bin/env python3
"""Draw THE WORLD TODAY - 26 November 2026 front page (1024x1024).

Original work for make.fun news-image-20261126. Draws a broadsheet
front page with PIL from the 35 verified 26-Nov-2026 stories, then
saves entry.png. Run: python3 draw.py  (writes entry.png next to it)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 240, 220)
INK = (18, 18, 18)
RED = (139, 26, 26)
MAROON = (120, 20, 20)
TEAL = (15, 95, 107)
GREEN = (34, 110, 60)
GREY = (90, 84, 72)
LIGHT = (232, 222, 198)
SKY = (16, 32, 64)
SEA = (52, 96, 120)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, kind):
    """Verification badge. Returns width used."""
    col = {"CONFIRMED": RED, "OFFICIAL": TEAL, "REPORTED": GREEN}[kind]
    f = F(SANSB, 8)
    w = int(d.textlength(kind, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 12], radius=2, fill=col)
    d.text((x + 5, y + 2), kind, font=f, fill=(255, 255, 255))
    return w


def para(d, x, y, text, font, maxw, leading, fill=INK, maxlines=2):
    lines = wrap(d, text, font, maxw)[:maxlines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=font, fill=fill)
    return y + len(lines) * leading


# --- story data: (n, headline, summary, badge, region) ---
HEROES = [
    (1, "ONE MILLION SATELLITES ABOVE US",
     "FCC approves SpaceX 'Starmind': 1m orbital data centres, first in US history. First satellite by Nov 2033, full fleet 2040; built with Nvidia.",
     "CONFIRMED", "space"),
    (2, "AMERICA'S NEW TARIFFS: 14 PARTNERS",
     "Washington proposes fresh tariffs on 14 trade partners, China highest. India faces 25% with no deal, 17% with a reciprocal deal.",
     "OFFICIAL", "tariffs"),
    (3, "ASIA BOUNCES BACK",
     "Stocks rebound Thursday: Nikkei +1.6%, Kospi +1.9%, Taiex +3.05%, Hang Seng +1.22%. Wall Street recovers from a -1,100 Dow intraday low.",
     "CONFIRMED", "markets"),
]

ILLUSTRATED = [
    (4, "NVIDIA -3.9% TO $149.30", "S&P puts the chipmaker's credit rating on watch, citing management and board weakness. Nasdaq 100 had touched -20% from its peak.", "CONFIRMED", "chip"),
    (5, "GIZA FUEL-TRUCK FIRE: 30-31 DEAD", "A fuel truck explodes on Cairo's ring road. 39 ambulances sent, 15 injured, after the blast on the Giza ring road.", "REPORTED", "fire"),
    (6, "PYONGYANG EXPELS SWISS DIPLOMAT", "North Korea orders Switzerland's diplomatic office in Pyongyang shut, weeks after it opened, in a sanctions dispute.", "CONFIRMED", "diplomat"),
    (7, "KIM: SPREAD TACTICAL NUKES WIDER", "Kim Jong Un calls for a wider deployment of tactical nuclear weapons, Pyongyang's latest escalation of its arsenal.", "CONFIRMED", "nuke"),
    (8, "UKRAINE HITS AIRBASE: 5 JETS DOWN", "Ukrainian strike damages five Russian military jets at an airfield, Kyiv reports, in a long-range hit on Russian air power.", "CONFIRMED", "jets"),
    (9, "HOUTHIS HIT SAUDI REFINERY", "Houthi attack on Saudi Arabia's largest refinery lifts Brent to $94.81. Gold $3,566/oz; dollar index 103.71; yen 159.14.", "CONFIRMED", "refinery"),
    (10, "ANDY TAYLOR, DURAN DURAN, DIES AT 65", "The guitarist of Duran Duran has died aged 65, the band's era-defining sound carried from the 1980s to today.", "CONFIRMED", "guitar"),
    (11, "LEBANON TO OPEN SECOND AIRPORT", "Lebanon will open a second international airport next month in the north, a boost for the economy as Hezbollah's grip weakens.", "REPORTED", "airport"),
    (12, "EU SPLIT OVER EUR45BN UKRAINE LOAN", "EU leaders clash in Brussels over a EUR45 billion loan for Ukraine, the bloc's biggest test of unity on war funding.", "REPORTED", "eu"),
    (13, "SAUDI INTERCEPTS 2 HOUTHI MISSILES", "The Saudi-led coalition intercepts two Houthi missiles heading for Riyadh in the early hours of Thursday.", "REPORTED", "missile"),
]

REST = [
    (14, "INDIA: Constitution Day; Rs15,000 cr Nepal package", "OFFICIAL"),
    (15, "BANGLADESH: garment minimum wage up 36%", "REPORTED"),
    (16, "CRICKET: South Africa sweep Bangladesh 2-0", "CONFIRMED"),
    (17, "CRICKET: Sooryavanshi 204 off 53 balls vs UAE", "CONFIRMED"),
    (18, "CHESS: Gukesh vs Sindarov, World title, Geneva", "REPORTED"),
    (19, "IPL 2027 AUCTION: 1,220 players register", "REPORTED"),
    (20, "FLIPKART CEO Krishnamurthy quits in Dec 2026", "REPORTED"),
    (21, "TRUMP to meet senator-elect El-Sayed on TrumpCare", "REPORTED"),
    (22, "THANKSGIVING: US markets shut for the holiday", "OFFICIAL"),
    (23, "HORMUZ: two tankers hit by Iranian mines", "REPORTED"),
    (24, "BOGOR: 13 miners trapped in flooded gold mine", "REPORTED"),
    (25, "PUERTO RICO: court voids Luma contract, 5-4", "CONFIRMED"),
    (26, "SYRIA: ISIL suicide attack kills 2 in Hasakah", "REPORTED"),
    (27, "SPAIN: snap election called for Sunday 29 Nov", "CONFIRMED"),
    (28, "ZAMBIA: protests banned over term-limit removal", "REPORTED"),
    (29, "UNICREDIT cleared to lift Commerzbank stake to ~50%", "CONFIRMED"),
    (30, "CHINA signals tariff retaliation; Indonesia seeks exemption", "REPORTED"),
    (31, "RAMAPHOSA cleared: Phala Phala report voided", "CONFIRMED"),
    (32, "ECUADOR + US weigh joint military operations", "REPORTED"),
    (33, "EU extends Mozambique military mission to end-2028", "OFFICIAL"),
    (34, "NIGERIA busts $227m meth lab, arrests 5 Mexicans", "CONFIRMED"),
    (35, "CHAMPIONS LEAGUE: Liverpool beat Brugge; Real hit 5 vs PSV", "CONFIRMED"),
]

EXCLUDED = [
    ("Shenzhou-24 + first Pakistani astronaut", "25 Nov - hero of ni25"),
    ("COP31 failure", "22-23 Nov"),
    ("Liverpool 4-0 Man Utd", "23 Nov"),
    ("Wellington Test draw, India v NZ", "23 Nov"),
    ("England beat Australia, 2nd T20I", "Tue 24 Nov"),
    ("Hodeidah mission / Canberra pact", "25 Nov - hero of ni25"),
    ("Murmansk governor held, corruption", "Wed 25 Nov"),
    ("2nd judge blocks Trump birthright order", "Wed 25 Nov"),
    ("Niger State gunmen, 30+ dead", "25 Nov 23:27"),
    ("Mississippi plane crash, 6 dead", "25 Nov"),
    ("Solomon Islands-Australia deal", "25 Nov"),
    ("Colombia supermarket hostages freed", "25 Nov"),
]
NOTYET = [
    "Spain snap election - Sun 29 Nov",
    "ZXOXO token TGE - Mon 30 Nov",
    "Starmind first satellite - by Nov 2033",
    "Lebanon 2nd airport opens - Dec",
    "IPL 2027 auction - date TBA",
    "Flipkart CEO exit - Dec 2026",
]


# --- illustrated scenes -------------------------------------------------
def scene(d, box, kind):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "space":
        d.rectangle(box, fill=SKY)
        for sx, sy in [(20, 12), (60, 30), (110, 8), (180, 22), (250, 10), (300, 35), (90, 45), (210, 48)]:
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255))
        d.ellipse([x0 - 40, y1 - 38, x0 + 130, y1 + 8], fill=(46, 110, 160))
        d.arc([x0 - 40, y1 - 38, x0 + 130, y1 + 8], 200, 340, fill=(140, 200, 230), width=3)
        for sx, sy in [(150, 30), (220, 55), (280, 25)]:
            d.rectangle([x0 + sx, y0 + sy, x0 + sx + 16, y0 + sy + 8], fill=(200, 210, 220))
            d.rectangle([x0 + sx - 8, y0 + sy + 2, x0 + sx, y0 + sy + 6], fill=(120, 160, 200))
            d.rectangle([x0 + sx + 16, y0 + sy + 2, x0 + sx + 24, y0 + sy + 6], fill=(120, 160, 200))
        d.text((x0 + 8, y1 - 16), "EARTH  •  ORBIT  •  1,000,000 SATELLITES", font=F(SANSB, 8), fill=(255, 255, 255))
    elif kind == "tariffs":
        d.rectangle(box, fill=(232, 214, 170))
        d.ellipse([x0 + 18, y0 + 14, x0 + 98, y0 + 94], fill=(52, 96, 120))
        d.arc([x0 + 18, y0 + 14, x0 + 98, y0 + 94], 0, 360, fill=(255, 255, 255), width=2)
        for bx, bh, lab in [(140, 30, "25%"), (185, 50, "17%"), (230, 66, "CHN")]:
            d.rectangle([x0 + bx, y1 - 12 - bh, x0 + bx + 30, y1 - 12], fill=RED)
            d.text((x0 + bx + 2, y1 - 24 - bh), lab, font=F(SANSB, 9), fill=RED)
        d.text((x0 + 8, y1 - 16), "WASHINGTON  •  BEIJING  •  NEW DELHI", font=F(SANSB, 8), fill=INK)
    elif kind == "markets":
        d.rectangle(box, fill=(16, 64, 48))
        pts = [(x0 + 10, y1 - 22), (x0 + 60, y1 - 48), (x0 + 110, y1 - 38), (x0 + 170, y1 - 66),
               (x0 + 230, y1 - 52), (x0 + 290, y1 - 88), (x0 + 315, y1 - 80)]
        d.line(pts, fill=(80, 220, 140), width=4)
        d.polygon(pts + [(x0 + 315, y1 - 10), (x0 + 10, y1 - 10)], fill=(80, 220, 140, 60))
        d.text((x0 + 10, y0 + 8), "NIKKEI +1.6%   KOSPI +1.9%   TAIEX +3.05%", font=F(SANSB, 10), fill=(255, 255, 255))
        d.text((x0 + 8, y1 - 16), "TOKYO  •  SEOUL  •  TAIPEI  •  HONG KONG", font=F(SANSB, 8), fill=(200, 240, 210))
    elif kind == "chip":
        d.rectangle(box, fill=(20, 20, 40))
        d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=(60, 120, 200), outline=(150, 200, 255), width=2)
        for i in range(4):
            d.line([cx - 16 + i * 10, cy - 24, cx - 16 + i * 10, cy - 16], fill=(150, 200, 255), width=2)
            d.line([cx - 16 + i * 10, cy + 16, cx - 16 + i * 10, cy + 24], fill=(150, 200, 255), width=2)
        d.text((cx - 12, cy - 6), "NVDA", font=F(SANSB, 8), fill=(255, 255, 255))
    elif kind == "fire":
        d.rectangle(box, fill=(40, 20, 10))
        d.polygon([(cx - 18, y1 - 6), (cx - 8, cy - 8), (cx, cy + 6), (cx + 10, cy - 14), (cx + 18, y1 - 6)], fill=(255, 120, 20))
        d.polygon([(cx - 8, y1 - 6), (cx - 2, cy + 2), (cx + 8, y1 - 6)], fill=(255, 220, 80))
        d.text((x0 + 4, y0 + 3), "GIZA", font=F(SANSB, 8), fill=(255, 255, 255))
    elif kind == "diplomat":
        d.rectangle(box, fill=(70, 90, 120))
        d.rectangle([x0 + 6, y0 + 6, x1 - 6, y1 - 6], outline=(255, 255, 255), width=2)
        d.line([x0 + 6, y0 + 6, x1 - 6, y1 - 6], fill=(255, 255, 255), width=2)
        d.text((cx - 14, cy - 6), "EXIT", font=F(SANSB, 9), fill=(255, 255, 255))
    elif kind == "nuke":
        d.rectangle(box, fill=(30, 30, 30))
        d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(255, 200, 40))
        d.pieslice([cx - 18, cy - 18, cx + 18, cy + 18], 0, 120, fill=INK)
        d.pieslice([cx - 18, cy - 18, cx + 18, cy + 18], 180, 300, fill=INK)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=INK)
    elif kind == "jets":
        d.rectangle(box, fill=(120, 170, 210))
        for jx in (x0 + 10, x0 + 30):
            d.polygon([(jx, cy - 4), (jx + 26, cy), (jx, cy + 4)], fill=(40, 40, 40))
            d.polygon([(jx + 8, cy - 10), (jx + 14, cy), (jx + 8, cy + 10)], fill=(40, 40, 40))
        d.text((x0 + 4, y0 + 3), "5 JETS", font=F(SANSB, 8), fill=(255, 255, 255))
    elif kind == "refinery":
        d.rectangle(box, fill=(50, 40, 30))
        for tx in (x0 + 8, x0 + 24, x0 + 40):
            d.rectangle([tx, cy - 6, tx + 10, y1 - 6], fill=(180, 180, 180))
            d.polygon([(tx + 2, cy - 6), (tx + 5, cy - 16), (tx + 8, cy - 6)], fill=(255, 120, 20))
        d.text((x0 + 4, y0 + 3), "$94.81", font=F(SANSB, 8), fill=(255, 220, 80))
    elif kind == "guitar":
        d.rectangle(box, fill=(90, 40, 60))
        d.ellipse([cx - 12, cy - 2, cx + 12, cy + 20], fill=(200, 140, 60))
        d.rectangle([cx - 2, y0 + 6, cx + 2, cy], fill=(120, 80, 40))
        d.ellipse([cx - 4, cy + 6, cx + 4, cy + 14], fill=INK)
        d.text((x0 + 4, y0 + 3), "1961-2026", font=F(SANSB, 7), fill=(255, 255, 255))
    elif kind == "airport":
        d.rectangle(box, fill=(140, 180, 200))
        d.polygon([(x0 + 6, y1 - 12), (x1 - 6, y0 + 12), (x1 - 6, y0 + 18), (x0 + 6, y1 - 6)], fill=(60, 60, 60))
        for i in range(5):
            d.line([x0 + 12 + i * 9, y1 - 14 - i * 5, x0 + 16 + i * 9, y1 - 16 - i * 5], fill=(255, 255, 255), width=2)
    elif kind == "eu":
        d.rectangle(box, fill=(20, 40, 110))
        for i in range(8):
            import math
            a = i * math.pi / 4
            sx, sy = cx + int(16 * math.cos(a)), cy + int(16 * math.sin(a))
            d.text((sx - 3, sy - 4), "*", font=F(SANSB, 10), fill=(255, 220, 80))
        d.text((cx - 7, cy - 7), "EU", font=F(SANSB, 11), fill=(255, 255, 255))
    elif kind == "missile":
        d.rectangle(box, fill=(30, 50, 80))
        d.line([x0 + 6, y1 - 8, x1 - 8, y0 + 8], fill=(255, 220, 80), width=3)
        d.polygon([(x1 - 14, y0 + 4), (x1 - 4, y0 + 4), (x1 - 4, y0 + 14)], fill=(255, 255, 255))
        d.text((x0 + 4, y1 - 14), "RIYADH", font=F(SANSB, 8), fill=(255, 255, 255))


# --- world map (schematic, numbered pins 1-35) -------------------------
# (lon, lat) approx per story; map area is a rough equirectangular plot.
PINS = {
    1: (-100, 55), 2: (-75, 40), 3: (120, 35), 4: (30, 30), 5: (30, 30),
    6: (127, 40), 7: (127, 40), 8: (32, 50), 9: (45, 25), 10: (-2, 53),
    11: (36, 34), 12: (78, 21), 13: (90, 24), 14: (28, -25), 15: (78, 21),
    16: (10, 50), 17: (0, 0), 18: (77, 21), 19: (-3, 40), 20: (-100, 20),
    21: (-77, 39), 22: (0, 0), 23: (56, 26), 24: (107, -6), 25: (-66, 18),
    26: (41, 36), 27: (-3, 40), 28: (28, -14), 29: (10, 50), 30: (104, 35),
    31: (28, -25), 32: (-79, -1), 33: (40, -18), 34: (8, 9), 35: (-2, 53),
}
# jitter duplicates so pins do not stack exactly
JITTER = {5: (8, -6), 7: (6, 5), 15: (-8, 6), 22: (10, -8), 27: (12, 6), 31: (-6, -6), 35: (8, -8), 19: (-8, 8), 29: (-10, -6), 12: (-12, 5), 16: (10, -7), 8: (4, 8), 14: (-8, 4)}


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 232, 238), outline=INK, width=1)
    # schematic continents as rough polygons (lon/lat -> x/y)
    def P(lon, lat):
        return (x0 + int((lon + 180) / 360 * (x1 - x0)),
                y0 + int((75 - lat) / 135 * (y1 - y0)))
    continents = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 70), (-80, 62), (-75, 45), (-80, 30), (-95, 20), (-105, 22), (-120, 32), (-125, 48), (-150, 60)],
        [(-80, 10), (-60, 5), (-50, -5), (-40, -20), (-55, -35), (-70, -40), (-75, -20), (-80, -5)],
        [(-10, 36), (0, 44), (-5, 50), (5, 58), (15, 58), (25, 60), (30, 55), (40, 50), (30, 42), (20, 40), (10, 38), (0, 36)],
        [(-17, 15), (-10, 30), (10, 35), (30, 32), (43, 12), (51, 10), (40, -5), (35, -20), (25, -30), (18, -35), (12, -18), (8, 4)],
        [(35, 35), (45, 40), (55, 40), (60, 30), (55, 25), (48, 30), (43, 30), (35, 30)],
        [(60, 70), (90, 75), (120, 75), (150, 70), (160, 60), (140, 45), (130, 35), (120, 25), (105, 10), (100, 5), (95, 15), (85, 20), (75, 10), (70, 25), (60, 25), (55, 45), (50, 60)],
        [(130, -12), (140, -15), (150, -25), (145, -38), (135, -35), (130, -25)],
    ]
    for c in continents:
        d.polygon([P(lo, la) for lo, la in c], fill=(222, 208, 170), outline=(120, 110, 85))
    for lab, (lo, la) in {"N AMERICA": (-105, 52), "S AMERICA": (-62, -18), "EUROPE": (12, 52),
                          "AFRICA": (18, 2), "ASIA": (105, 48), "OCEANIA": (140, -28),
                          "MIDDLE EAST": (48, 32)}.items():
        px, py = P(lo, la)
        d.text((px - 22, py - 4), lab, font=F(SANSB, 7), fill=GREY)
    d.text((x0 + 6, y0 + 4), "SPACE ^", font=F(SANSB, 7), fill=TEAL)
    for n, (lo, la) in PINS.items():
        jx, jy = JITTER.get(n, (0, 0))
        px, py = P(lo, la)
        px += jx
        py += jy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px - 3 if n < 10 else px - 6, py - 5), str(n), font=F(SANSB, 7), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)
    d.line([14, 10, W - 14, 10], fill=INK, width=2)

    # masthead
    d.text((16, 22), "No. 26  •  2026", font=F(SANS, 10), fill=GREY)
    d.text((14, 62), "ONE DAY  •  ONE PICTURE", font=F(SANSB, 9), fill=GREY)
    d.text((W - 14 - 218, 22), "THURSDAY 26 NOVEMBER 2026", font=F(SANSB, 11), fill=RED)
    d.text((W - 14 - 218, 62), "35 STORIES  •  ALL CHECKED", font=F(SANSB, 9), fill=GREY)
    title = "THE WORLD TODAY"
    tf = F(SERIFB, 46)
    d.text(((W - d.textlength(title, font=tf)) / 2, 14), title, font=tf, fill=INK)
    d.line([14, 78, W - 14, 78], fill=INK, width=2)
    sub = "EVERY STORY CHECKED TO 26 NOVEMBER 2026"
    sf = F(SANSB, 12)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 82), sub, font=sf, fill=RED)

    # stats strip
    d.rectangle([14, 100, W - 14, 120], fill=INK)
    stats = "35 STORIES  •  10 REGIONS  •  14 FIELDS  •  6 CONTINENTS + SPACE  •  3 HEROES  •  13 SCENES  •  MAP 1-35  •  UTC TIMELINE  •  DATE CHECK"
    stf = F(SANSB, 10)
    d.text(((W - d.textlength(stats, font=stf)) / 2, 106), stats, font=stf, fill=(255, 255, 255))

    # UTC timeline strip (hours only where the research gives them)
    d.rectangle([14, 124, W - 14, 146], outline=GREY, width=1)
    d.text((20, 128), "UTC TIMELINE", font=F(SANSB, 9), fill=RED)
    tl = "01:37 GMT Hormuz tankers hit  •  01:45 GMT Ecuador-US talks  •  morning: Asia rebound, Giza fire  •  day: tariffs, Starmind, Brent $94.81  •  night: Champions League"
    d.text((118, 129), tl, font=F(SANS, 9), fill=INK)
    d.line([14, 146, W - 14, 146], fill=INK, width=1)

    # heroes 1-3
    hy, hh = 152, 196
    for i, (n, head, summ, bdg, kind) in enumerate(HEROES):
        x = 14 + i * 334
        d.rectangle([x, hy, x + 326, hy + hh], outline=INK, width=1)
        scene(d, (x + 1, hy + 1, x + 325, hy + 104), kind)
        d.text((x + 8, hy + 108), f"{n}", font=F(SERIFB, 14), fill=RED)
        hf = F(SANSB, 12)
        lines = wrap(d, head, hf, 300)
        for j, ln in enumerate(lines[:2]):
            d.text((x + 26, hy + 110 + j * 14), ln, font=hf, fill=INK)
        para(d, x + 8, hy + 140, summ, F(SANS, 10), 310, 12, maxlines=3)
        badge(d, x + 8, hy + hh - 18, bdg)
        d.text((x + 84, hy + hh - 16), "26 NOV 2026", font=F(SANS, 8), fill=GREY)

    # illustrated 4-13
    d.rectangle([14, 354, W - 14, 372], fill=RED)
    d.text((20, 358), "ILLUSTRATED  •  STORIES 4-13  —  EVERY ONE WITH ITS OWN SCENE", font=F(SANSB, 10), fill=(255, 255, 255))
    iy = 376
    for row in range(5):
        for col in range(2):
            n, head, summ, bdg, kind = ILLUSTRATED[row * 2 + col]
            x = 14 + col * 501
            y = iy + row * 59
            d.rectangle([x, y, x + 497, y + 56], outline=GREY, width=1)
            scene(d, (x + 1, y + 1, x + 57, y + 55), kind)
            d.text((x + 64, y + 4), f"{n}", font=F(SERIFB, 12), fill=RED)
            hf = F(SANSB, 10)
            d.text((x + 82, y + 5), head, font=hf, fill=INK)
            para(d, x + 64, y + 20, summ, F(SANS, 9), 424, 11, maxlines=2)
            badge(d, x + 64, y + 42, bdg)

    # map 1-35
    my = 678
    d.rectangle([14, my, W - 14, my + 18], fill=INK)
    d.text((20, my + 3), "THE WORLD IN NUMBERS  —  MAP 1-35", font=F(SANSB, 10), fill=(255, 255, 255))
    d.text((W - 260, my + 3), "RED PIN = STORY NUMBER", font=F(SANS, 9), fill=(255, 255, 255))
    draw_map(d, (14, my + 20, W - 14, my + 108))

    # rest 14-35
    ry = 790
    d.rectangle([14, ry, W - 14, ry + 18], fill=RED)
    d.text((20, ry + 3), "THE REST OF THE DAY  —  STORIES 14-35", font=F(SANSB, 10), fill=(255, 255, 255))
    for idx, (n, head, bdg) in enumerate(REST):
        col = idx // 11
        row = idx % 11
        x = 14 + col * 501
        y = ry + 21 + row * 10
        d.text((x, y), f"{n}", font=F(SANSB, 9), fill=RED)
        d.text((x + 20, y), head, font=F(SANS, 9), fill=INK)
        bw = badge(d, x + 430, y, bdg)

    # date check + not yet
    by = 924
    for col, (title, items, colr) in enumerate([
        ("DATE CHECK — NOT 26 NOVEMBER (EXCLUDED)", EXCLUDED, RED),
        ("NOT YET — AFTER 26 NOVEMBER", NOTYET, TEAL),
    ]):
        x = 14 + col * 501
        d.rectangle([x, by, x + 497, by + 62], outline=INK, width=1)
        d.rectangle([x, by, x + 497, by + 16], fill=colr)
        d.text((x + 6, by + 3), title, font=F(SANSB, 9), fill=(255, 255, 255))
        if col == 0:
            for i, (t, why) in enumerate(items):
                cx = x + 6 + (i // 6) * 248
                cy = by + 19 + (i % 6) * 7
                d.text((cx, cy), f"✕ {t} — {why}", font=F(SANS, 7), fill=INK)
        else:
            for i, t in enumerate(items):
                cx = x + 6 + (i // 3) * 248
                cy = by + 19 + (i % 3) * 11
                d.text((cx, cy), f"• {t}", font=F(SANS, 8), fill=INK)

    # footer legend + sources
    fy = 990
    d.line([14, fy, W - 14, fy], fill=INK, width=1)
    d.text((14, fy + 4), "BADGES:  CONFIRMED = 2+ outlets  •  OFFICIAL = on the record  •  REPORTED = one outlet",
           font=F(SANSB, 8), fill=INK)
    d.text((14, fy + 15), "Sources: Reuters, BBC, TBS News, Daily Baku, GeekWire, Spaceflight Now, Jabulani Radio. All 35 stories dated 26 Nov 2026 (UTC).",
           font=F(SANS, 8), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
