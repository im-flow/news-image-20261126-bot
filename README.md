# THE WORLD TODAY — 26 November 2026 in One Picture

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261126)

Entry for [Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126) (make.fun, bounty `news-image-20261126`).

## What it is

A broadsheet front page, **THE WORLD TODAY**, drawn for Thursday 26 November 2026:
35 stories, 10 regions, 14 fields, 6 continents + space, 3 heroes, 13 drawn
scenes, a numbered-pin world map (1–35), a UTC timeline, and a DATE CHECK box
with 12 excluded stories plus a NOT YET box — all dated 26 Nov 2026 (UTC).

- **Hero 1 — ONE MILLION SATELLITES ABOVE US:** FCC approves SpaceX
  "Starmind", 1m orbital data centres (CONFIRMED).
- **Hero 2 — AMERICA'S NEW TARIFFS: 14 PARTNERS:** Washington proposes fresh
  tariffs, China highest; India 25% with no deal, 17% with a deal (OFFICIAL).
- **Hero 3 — ASIA BOUNCES BACK:** Nikkei +1.6%, Kospi +1.9%, Taiex +3.05%,
  Hang Seng +1.22% (CONFIRMED).
- **Illustrated stories 4–13**, each with its own scene and a 2-line summary:
  Nvidia −3.9%, Giza fuel-truck fire, North Korea expels the Swiss diplomat,
  Kim's tactical-nuke call, Ukraine's airbase strike, the Houthi refinery
  attack, Andy Taylor dies at 65, Lebanon's second airport, the EU €45bn
  Ukraine loan clash, and the Saudi missile intercept.
- **Stories 14–35** cover India, Bangladesh, cricket, chess, the IPL auction,
  Flipkart, TrumpCare, Thanksgiving, Hormuz, Bogor, Puerto Rico, Syria, Spain,
  Zambia, UniCredit, China, Ramaphosa, Ecuador, Mozambique, Nigeria and the
  Champions League.

Badges: **CONFIRMED** = 2+ outlets, **OFFICIAL** = on the record,
**REPORTED** = one outlet. Sources: Reuters, BBC, TBS News, Daily Baku,
GeekWire, Spaceflight Now, Jabulani Radio.

## How it is built

- `draw.py` draws `entry.png` (1024×1024, PIL) from the story data in the file.
- `main.py` (Python 3.13, standard library only) copies `entry.png` unchanged
  to the output directory, validating the PNG magic, the 1 MiB cap and the
  1024×1024 cap. Deterministic: both runs write the same bytes, no network.

Run it locally:

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
