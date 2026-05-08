"""
SMA Outfit definitions, ticker universe, timeframe configs, and constants.
All data sourced from raultrades/SMA-outfits GitHub repo and live trade docs.

── CANONICAL vs. OBSERVED AFFINITY (Raul Apr 9 2026 clarification) ──────
Raul clarified that ONLY four equities have a permanent, reliable system
outfit relationship:

    SPX  — 30m  [10, 50, 200]
    IXIC — 20m  [20, 100, 250]
    DJI  — 15m/1h [30, 60, 90, 300, 600, 900]
    VIX  — 15m/1h [36, 52, 106, 211, 422, 844]   (aka "SVIX (211)" outfit)

For every other equity, the outfit that's gaming it CHANGES per leg and
per timeframe. Example he gave: "on a leg higher I recorded GME operating
on the 420 outfit on the daily chart. The next time it's a manufactured
higher it could be on any other outfit. It can also be on any other
timeframe. [...] or it doesn't operate on any specific outfit because
these banks [...] don't necessarily need other firms to help manufacture
an equity higher because they may just be providing liquidity."

This means the entries in AFFINITIES below for NON-index tickers
(NVDA, AAPL, TSLA, META, etc.) are HISTORICAL OBSERVATIONS of legs we've
confirmed, NOT permanent tuning forks. A non-index ticker could be
operating on any outfit on any timeframe during any given leg, or on
none at all. True relevance must be scored from aggregated OHLC hit
history per (ticker, outfit, timeframe) tuple, weighted by recency and
by the outfit's historical % return before termination (see Raul's
"keys lose strength over time" framing).
─────────────────────────────────────────────────────────────────────────
"""
from typing import Optional, Set, Dict, List

# ── SMA Outfit Definitions ──────────────────────────────────────────────────

OUTFITS: Dict[str, dict] = {
    # System outfits (macro trend)
    "S&P": {
        "periods": [10, 50, 200],
        "category": "System",
        "notes": (
            "SPX on 30m chart. CANONICAL system outfit — Raul Apr 9 2026: "
            "'The only equities that have a relevant system are [...] SPX "
            "[...] 30m 10/50/200'. One of only 4 permanent outfit-ticker "
            "relationships (SPX, IXIC, DJI, VIX)."
        ),
    },
    "NAS": {
        "periods": [20, 100, 250],
        "category": "System",
        "notes": (
            "IXIC on 20m chart. CANONICAL system outfit — Raul Apr 9 2026: "
            "'NASDAQ's IXIC [...] 20m 20/100/250'. One of only 4 permanent "
            "outfit-ticker relationships (SPX, IXIC, DJI, VIX). Timeframe "
            "corrected Apr 9 from 20m/30m to 20m only."
        ),
    },
    "DJI": {
        "periods": [30, 60, 90, 300, 600, 900],
        "category": "System",
        "notes": (
            "DJI on 15m/1h chart. CANONICAL system outfit — Raul Apr 9 2026: "
            "'Dow Jones DJI [...] 15m/1h 30/60/90/300/600/900'. One of only "
            "4 permanent outfit-ticker relationships (SPX, IXIC, DJI, VIX). "
            "Note the 2-tier arithmetic structure: [30,60,90] at ×1 scale, "
            "[300,600,900] at ×10 scale."
        ),
    },
    # Core outfits
    "Base 2/NVDA": {
        "periods": [16, 32, 64, 128, 256, 512],
        "category": "Core",
        "notes": "Binary progression",
    },
    "Waring's Problem": {
        "periods": [19, 37, 73, 143, 279, 548],
        "category": "Core",
        "notes": (
            "Number theory integers (Hilbert's Waring's Problem). "
            "One of Raul's longest-tracked outfits — first documented Aug 24 2023: "
            "'If you can figure out when they use point/penny based operations using "
            "the Waring's Problem conjecture 19 37 73 143 279 548 in the Stock "
            "Market. Well you have nothing to worry about.' "
            "Raul reposted this on Apr 29 2026 (FOMC day) saying 'currently!' — "
            "confirming Waring's Problem was actively running point/penny operations "
            "across the major market on that date. OUTFIT_SURGE event. "
            "Cross-outfit price encoding confirmed same day: Raul short SVIX at "
            "19.37 using Regression (432) MA864 — entry price 19.37 encodes the "
            "first two Waring integers [19, 37]. UVIX day high that session = "
            "548, the final Waring integer. Raul: 'Finance is a cryptography "
            "game. If you know, you know.' Institutions encode outfit sequences "
            "directly into price levels, cross-referencing multiple outfits "
            "simultaneously. When Waring's Problem is active, it is one of the "
            "highest-conviction signals in the system — Raul has been watching "
            "it since 2023 as a primary indicator of institutional positioning."
        ),
    },
    "Time (144)": {
        "periods": [18, 36, 72, 144, 288, 576],
        "category": "Core",
        "notes": "144(0) reference",
    },
    "Time (365)": {
        "periods": [23, 46, 91, 183, 365, 730],
        "category": "Core",
        "notes": "Calendar year",
    },
    "Time (366)": {
        "periods": [23, 46, 92, 183, 366, 732],
        "category": "Core",
        "notes": "Leap year",
    },
    "TSLA (420)": {
        "periods": [27, 53, 69, 105, 210, 420, 840],
        "category": "Core",
        "notes": "Tesla / 420 meme. a(n)=420×2^n, n∈[-4,1] rounded + MA69 supplementary. Also operates on DXY (20m MA840 key level). DXY-TSLA inverse correlation: dollar strength via this outfit pressures TSLA, dollar weakness squeezes TSLA higher. Outfit integers (27,53,105) appear as closing price cents.",
    },
    "SVIX (211)": {
        "periods": [36, 52, 106, 211, 422, 844],
        "category": "Core",
        "notes": (
            "VIX canonical system outfit on 15m/1h. CANONICAL — Raul Apr 9 "
            "2026: 'Chicago VIX is SVIX [...] 15m/1h 36/52/106/211/422/844'. "
            "One of only 4 permanent outfit-ticker relationships (SPX, "
            "IXIC, DJI, VIX). Category left as 'Core' (not 'System') to "
            "preserve existing confluence/surge alert behavior — the "
            "System category suppresses those alerts in alerts.py. "
            "CORRECTION Apr 9 2026: first SMA is 36, NOT 26. Earlier "
            "config inferred 26 by halving from 52; Raul's canonical "
            "spec is 36. Fires on VIX, UVXY, SVXY, UVIX, BTC per "
            "historical affinity. "
            "IMPORTANT DISCREPANCY Apr 29 2026: Raul long RIVN 2H@15.14 "
            "using 'SVIX outfit' lists periods as MA26/MA52/MA106/MA211/"
            "MA422/MA855 — first period is 26 (mathematical: 211/8=26.375) "
            "NOT 36, and last period is 855 not 844. This suggests: "
            "MA36 is specific to VIX's canonical system; when SVIX outfit "
            "applies to individual equities the first period is MA26. "
            "MA855 vs 844 is likely chart display rounding. Pending "
            "resolution from Raul's new published repository."
        ),
    },
    "Resource missing (404)": {
        "periods": [25, 51, 101, 202, 404, 808],
        "category": "Core",
        "notes": "HTTP 404",
    },
    "Regression (432)": {
        "periods": [27, 54, 108, 216, 432, 864],
        "category": "Core",
        "notes": (
            "Raul Apr 29 2026: 'cryptographic play on binary and the sequential "
            "descent of the integers 4, 3, and 2 of 432.' Sequence doubles each "
            "step: 27→54→108→216→432→864 (pure ×2 chain). 432 = 4×3×2 descending. "
            "Confirmed live: Raul short SVIX (= long UVIX tangentially) at 19.37. "
            "MA864 = ~19.36, +0.01 offset to avoid HFT detection → entry 19.37. "
            "Shorting SVIX = shorting the vol short = long VIX / bearish market. "
            "Confirmed by community reply: 'so they are shorting the shorts on "
            "volatility?' Raul: 'yes!' "
            "Waring's Problem cross-outfit signal: entry price 19.37 encodes the "
            "first two Waring integers [19, 37]; UVIX day high was 548, the final "
            "Waring integer. Finance is cryptography — price levels encode outfit "
            "sequences across instruments simultaneously. "
            "Apr 29 2026 FOMC day bear basket: SVIX program at 19.37 is the lead "
            "operation. Threaded positions: UVIX long, SPXU short S&P 3x, "
            "WEBS short internet 3x, BITI short Bitcoin, SQQQ short NASDAQ 3x. "
            "SQQQ stop = penny break of candle low 52.22 (possible MA54 coincidence "
            "at that price level — pending confirmation). All positions cut when "
            "SVIX breaches 19.37 to upside OR own stop triggers, whichever first."
        ),
    },
    "REPEATER_9": {
        "periods": [9, 18, 27, 36, 45, 54],
        "category": "Core",
        "notes": "9x repeater sequence",
    },
    "Alphabet/GOOG (100)": {
        "periods": [25, 50, 100, 200, 400, 800],
        "category": "Core",
        "notes": "Alphabet Inc",
    },
    "France Pres (25)": {
        "periods": [25, 50, 100, 200, 400, 600],
        "category": "Political",
        "notes": "France's president seat 25",
    },
    # Angel number outfits
    "AN (11s)": {
        "periods": [11, 44, 88, 111, 444, 888],
        "category": "Angel",
        "notes": "Angel numbers",
    },
    "AN (22s)": {
        "periods": [22, 55, 77, 222, 555, 777],
        "category": "Angel",
        "notes": (
            "Angel numbers. Confirmed Apr 8 2026: Raul long YANG 30M@27.33 "
            "at MA555 (Direxion Daily FTSE China Bear 3X, 2,000 shares, "
            "penny-breach cut). Part of the recession thesis pair with "
            "ERX long on Octuple (816) 2H — global equities [HSI SP500] "
            "risk-off."
        ),
    },
    "AN (33s)": {
        "periods": [33, 66, 99, 333, 666, 999],
        "category": "Angel",
        "notes": "Angel numbers",
    },
    # Political outfits
    "US President (45)": {
        "periods": [29, 57, 114, 227, 455, 911],
        "category": "Political",
        "notes": "45th president seat",
    },
    "US President (46)": {
        "periods": [23, 46, 92, 184, 368, 736],
        "category": "Political",
        "notes": "46th president seat",
    },
    "US President (47)": {
        "periods": [24, 47, 94, 188, 376, 752],
        "category": "Political",
        "notes": "47th president seat",
    },
    "Speaker House (56)": {
        "periods": [28, 56, 112, 224, 448, 896],
        "category": "Political",
        "notes": "Speaker seat 56",
    },
    "Russia Pres (2000)": {
        "periods": [16, 31, 63, 125, 250, 500],
        "category": "Arbitrage",
        "subtype": "arbitrage",
        "timeframes": ["1m", "3m", "5m", "15m"],
        "notes": (
            "Putin year 2000. HFT arbitrage / whipsaw outfit (NOT trend). "
            "Confirmed Apr 6-7 2026: Raul shorted SSO 15M@53.34 (MA500, .01 offset) "
            "— MA500 marked the exact day-high on Apr 7, trade held without breach. "
            "Raul Apr 7: operates on 1m across SPX/IXIC/DJI/ProShares as pure HFT "
            "short-order gathering. Look for 1m MA16 / 1m MA31 precision selections "
            "with .01 penny precision. Does NOT produce market tops/bottoms — that "
            "signal comes from DXY/VIX/bonds budgets. Originally discovered Apr 30 2024."
        ),
    },
    "Turkey Pres (12)": {
        "periods": [24, 48, 96, 192, 384, 768],
        "category": "Political",
        "notes": "Erdogan seat 12",
    },
    "WTC (911)": {
        "periods": [28, 57, 114, 228, 456, 911],
        "category": "Political",
        "notes": "World Trade Center homage",
    },
    "China Chair (7)": {
        "periods": [28, 56, 112, 224, 448, 976],
        "category": "Political",
        "notes": "People's Republic of China Chair",
    },
    # SPY-specific outfit (confirmed from Raul Nov 2025 post, MA464 at 599.28)
    "SPY (928)": {
        "periods": [29, 58, 116, 232, 464, 928],
        "category": "Core",
        "notes": "SPY-specific outfit on 5M. MA464 at 599.28. Not the same as S&P system outfit [10,50,200].",
    },
    # Dual Sequence outfits (from live trades)
    "Dual Seq (TSLQ)": {
        "periods": [39, 78, 156, 311, 622, 944],
        "category": "Dual",
        "notes": (
            "Confirmed on TSLQ/TSLR 2H. Short TSLQ at MA622. "
            "Confirmed Apr 13 2026: Raul long TSLZ 5M at penny-breach "
            "protocol, stop = penny break of 16.21. MA values on 5M at "
            "entry: MA39=17.72 MA78=17.99 MA156=18.03 MA311=18.16 "
            "MA622=17.32 MA944=16.92. Confirms outfit fires on 5M "
            "timeframe (previously only 2H documented). TSLZ = "
            "T-Rex 2X Inverse Tesla Daily Target ETF."
        ),
    },
    "Dual Seq (IXIC)": {
        "periods": [28, 55, 111, 221, 442, 884],
        "category": "Dual",
        "notes": "Confirmed on IXIC 2H",
    },
    # Bitcoin outfit — Raul Apr 14 2026 BITI + SPXU threaded trade
    "Bitcoin (248)": {
        "periods": [16, 31, 62, 124, 248, 746],
        "category": "Core",
        "notes": (
            "Crypto trinary cipher outfit. Raul Apr 14 2026 full math explanation: "
            "Marker = 124.333̄ (124 + 1/3). Derived as: growth chain 1→2→4 encodes "
            "'124'; missing stabilizer '3' from sequence [1,2,3,4] is encoded in "
            "ternary as .333̄, giving 124.333̄. "
            "Two-stage cipher: "
            "(1) binary expansion: 124.333̄ × 2 = 248.666̄; "
            "(2) ternary scaling: 248.666̄ × 3 = 746 exactly. "
            "The '~' in ~746 denotes representation limit — SMA outfits cap at 999 "
            "and use deferred rounding (only the final product rounds). "
            "Full outfit: halve 124 down → [16, 31, 62], core → [124, 248, 746]. "
            "Initial tweet listed [246, 748] in error; chart correctly showed "
            "MA248/MA746. Periods [16, 31, 62, 124, 248, 746] are canonical. "
            "Confirmed: BITI 1H long@23.13 (+.01 offset to obscure entry from HFT "
            "detection), cut on penny break of 23.13. MA124=23.13 at entry. "
            "16,000 shares. Trade successful. "
            "SPXU 20M simultaneously as 'threaded' trade — SPXU stop pegged to "
            "BITI program at 23.13, not SPXU's own SMAs. 1,000 shares. "
            "WEBS (Direxion Daily Dow Jones Internet Bear 3X) added after hours "
            "Apr 14 2026 as third threaded position, same stop at BITI 23.13. "
            "Threaded basket: BITI (lead/stop trigger) + SPXU + WEBS. "
            "Threaded concept: same outfit fires on multiple tickers; the most "
            "precise ticker's SMA level acts as stop trigger for the basket. "
            "Raul: 'crypto and math professionals using this outfit on a ProShares stock.'"
        ),
    },
    # Cipher outfits (derived from rotation/inversion of base sequences)
    "AAPU Cipher (246)": {
        "periods": [31, 61, 122, 244, 466, 668],
        "category": "Dual",
        "notes": "Angel cluster 222/444/666 → 246. Confirmed by Raul tweet: 'AAPU 1D 31 61 122 244 466 668, protocol:cut on a penny break of 26.73'. Apple $AAPL at $246.00.",
    },
    # Palantir outfit (confirmed from Raul's MYY 2H short trade)
    "Palantir (770)": {
        "periods": [22, 55, 77, 220, 550, 770],
        "category": "Core",
        "notes": "Palantir outfit. MYY 2h shorted@17.65, MA550@17.65. Penny breach above 17.65. Shorting MYY = long MidCap400.",
    },
    # Octane outfit (confirmed from Raul's SMR 20m trade)
    "Octane (818)": {
        "periods": [26, 51, 102, 205, 409, 818],
        "category": "Core",
        "notes": "Octane sequence. SMR 20m MA102@11.71, MSTX 30m@24.28, MSTR 5+/session, SCO 10m MA205@8.26, DRN 2h@8.16, FAS 2h@108.92 (via UPRO@92.10). All penny breach.",
    },
    # Octuple outfit (confirmed from Raul's DOG/UDOW 4h and ERX 2h trades)
    "Octuple (816)": {
        "periods": [26, 51, 102, 204, 408, 816],
        "category": "Core",
        "notes": (
            "Octuple sequence (also spelled 'Octople' by Raul). "
            "Also called NVDA/AAPL Area Code outfit — 408 = Silicon Valley "
            "(Santa Clara/Cupertino), where NVDA and AAPL are HQ'd. "
            "DOG 4h shorted@24.93 (=long UDOW), MA816@24.91. Penny breach above 24.93. "
            "Confirmed Apr 8 2026: Raul long ERX 2H@86.13 at MA204 amid rising "
            "geopolitical escalation. 1,000 shares. Penny-breach cut at 86.13. "
            "Confirmed Apr 9 2026: Raul 'bankers used the area code 408 to "
            "manipulate Oil higher' — MA408 now known-active on crude oil "
            "(USO/SCO) alongside the existing NVDA/AAPL/ERX affinity. "
            "Confirmed Apr 14 2026: Raul long SOXS 2M@21.88 at MA408=21.88, "
            "penny-breach protocol. MA816=0.00 (insufficient 2m history). "
            "Confirms outfit fires on 2M timeframe and on SOXS "
            "(Direxion Daily Semiconductor Bear 3X)."
        ),
    },
    # 22-squared outfit — Raul Apr 29 2026 MSFL 32M trade
    "22² (484)": {
        "periods": [22, 44, 121, 242, 484, 968],
        "category": "Core",
        "notes": (
            "Named '22² or 484 outfit' by Raul Apr 29 2026. Anchor: 22²=484. "
            "Sequence built on multiples of 11: 11×{2,4,11,22,44,88} = "
            "[22,44,121,242,484,968]. Lower half uses 11×n, upper half doubles "
            "from 121 (11²). Confirmed: MSFL 32M long@17.28 at MA484=17.28, "
            "penny breach stop. MSFL = T-Rex 2X Long Microsoft Daily Target ETF. "
            "NOTE: 32M is a new timeframe (2^5 minutes, fits binary math pattern)."
        ),
    },
    # Japan / Nikkei 225 outfit — Raul Apr 29 2026 NVDX 30M trade
    "Nikkei (225)": {
        "periods": [25, 45, 75, 225, 450, 900],
        "category": "Core",
        "notes": (
            "Named 'Japan's 225 outfit' by Raul Apr 29 2026. Named for the "
            "Nikkei 225 (Japan's benchmark stock index). Anchor: 225. "
            "Upper chain: 225→450→900 (×2 each). Lower chain: 75→45→25 "
            "(÷1.67, ÷1.8 — not pure halving). 225=9×25=15². "
            "Confirmed: NVDX 30M long@17.67 at MA225=17.67, 'as risk' "
            "(smaller position). Penny breach stop. "
            "NVDX = Direxion Daily NVDA Bull 2X Shares."
        ),
    },
    # Hantavirus outfit — Raul May 7 2026
    "Hantavirus (650)": {
        "periods": [18, 36, 65, 180, 360, 650],
        "category": "Core",
        "notes": (
            "Raul May 7 2026. SAB 15M MA180=3.63 (speculative). "
            "SABS 2H MA650=3.410 magnetized, ~10K shares, position 6. "
            "Two-tier x10 structure: [18,36,65] x10 = [180,360,650]."
        ),
    },
    # Menlo Park outfit (inferred from Raul's Apr 9 2026 META tweet)
    "Menlo Park (650)": {
        "periods": [20, 41, 81, 163, 325, 650],
        "category": "Core",
        "notes": (
            "META area-code outfit — 650 = Menlo Park, where Meta is HQ'd. "
            "Inferred Apr 9 2026 from Raul: 'Meta closes up 650. Menlo "
            "Park's area code. Not something you would piece together if "
            "you just didn't know.' Sequence [20, 41, 81, 163, 325, 650] "
            "is inferred by halving from 650 (same convention as Octuple "
            "(816) and SPY (928) area-code outfits). Full period list "
            "awaiting direct Raul confirmation."
        ),
    },
}

# ── Ticker-Outfit Affinity Map ──────────────────────────────────────────────
# When a primary-affinity outfit fires on its associated ticker, weight × 2.

AFFINITIES: Dict[str, List[str]] = {
    "S&P": ["SPX", "UPRO", "SPXU", "SSO", "SDS"],
    "SPY (928)": ["SPY"],
    "NAS": ["IXIC", "QQQ", "TQQQ", "SQQQ"],
    "DJI": ["DJI", "DIA", "UDOW", "SDOW"],
    "Base 2/NVDA": ["NVDA", "SOXL", "SOXS", "AMD", "INTC"],
    # Apr 29 2026: Waring's Problem flashing across major market.
    # Price 19.37 for SVIX entry encoded first two Waring integers; UVIX day high = 548 (last integer).
    "Waring's Problem": ["MSTX", "SVIX", "UVIX", "VIX", "UVXY"],
    "TSLA (420)": ["TSLA", "TSLR", "TSLQ", "TSLT", "TSLL", "NKLA", "BYND", "DXY"],
    # VIX added Apr 9 2026 — Raul confirmed VIX has a permanent system outfit.
    # RIVN confirmed Apr 29 2026 — 2H MA855 long@15.14, penny breach stop
    "SVIX (211)": ["VIX", "SVIX", "UVXY", "SVXY", "UVIX", "BTC", "RIVN"],
    "AN (11s)": ["AAPL", "AAPU"],
    "AN (22s)": ["AAPL", "AAPU", "YANG"],
    "AN (33s)": ["ORCX", "BTC"],
    "22² (484)": ["MSFL", "MSFT", "MSFX"],
    "Nikkei (225)": ["NVDX", "NVDA", "NKE", "EWJ"],
    "Dual Seq (TSLQ)": ["TSLQ", "TSLR", "TSLZ"],
    "Dual Seq (IXIC)": ["IXIC", "QQQ", "TQQQ"],
    # BITI + SPXU + WEBS confirmed Apr 14 2026 — threaded trade, same outfit on all three.
    "Bitcoin (248)": ["BITI", "BITU", "SPXU", "UPRO", "SPY", "SPX", "WEBS"],
    "AAPU Cipher (246)": ["AAPU", "AAPL", "AAPD"],
    "Octane (818)": ["SMR", "OKLO", "MSTX", "MSTR", "SCO", "DRN", "FAS", "TSLL"],
    "Octuple (816)": ["DOG", "UDOW", "DIA", "DJI", "NVDA", "AAPL", "ERX", "USO", "SCO", "SOXS"],
    "REPEATER_9": ["BYND", "SVIX", "TSLZ"],
    "Hantavirus (650)": ["SAB", "SABS"],
    "Menlo Park (650)": ["META"],
    "Palantir (770)": ["MYY", "UMDD", "PLTR", "MDY", "IVOO"],
    "Alphabet/GOOG (100)": ["GOOG", "GOOGL"],
    # Apr 29 2026: Regression (432) SVIX lead program + full threaded FOMC bear basket
    "Regression (432)": ["SVIX", "UVIX", "VIX", "UVXY", "SVXY", "SQQQ", "SPXU", "WEBS"],
    "France Pres (25)": [],
    "WTC (911)": [],
    "China Chair (7)": ["BABA", "SOXL", "SOXS", "TSM"],
    "Russia Pres (2000)": [
        # Raul Apr 7 2026: operates across the entire major market as HFT arbitrage
        "SPX", "IXIC", "DJI",
        "SPY", "QQQ", "DIA",
        "SSO", "SDS", "UPRO", "SPXU",
        "TQQQ", "SQQQ",
        "UDOW", "SDOW",
    ],
}

# ── SMA Position Weights ────────────────────────────────────────────────────
# Longer-period SMAs produce higher-weight signals.

POSITION_WEIGHTS_6 = [1.0, 1.5, 2.0, 4.0, 6.0, 8.0]   # 6-SMA outfits
POSITION_WEIGHTS_7 = [1.0, 1.5, 1.75, 2.0, 4.0, 6.0, 8.0]  # 7-SMA outfits (TSLA 420 w/ MA69)
POSITION_WEIGHTS_3 = [1.0, 3.0, 8.0]                     # 3-SMA system outfits

INSTITUTIONAL_HOURS_MULTIPLIER = 1.5

# ── Timeframe Weight Scale ──────────────────────────────────────────────────
# Normalizes hit value across timeframes. A 1m MA16 hit is MUCH more common
# (and therefore less significant) than a 15m MA16 hit because 1m has 15×
# more candles per hour. Without this scaling, fast-TF hits drown out slow-TF
# hits purely from sample-size, independent of real significance.
# Baseline is 30m = 1.00.
TIMEFRAME_SCALE: Dict[str, float] = {
    "1m":  0.20,
    "2m":  0.25,
    "3m":  0.30,
    "5m":  0.40,
    "10m": 0.55,
    "15m": 0.70,
    "20m": 0.80,
    "30m": 1.00,  # baseline
    "32m": 1.05,  # confirmed Apr 29 2026: Raul MSFL 32M trade (2^5 minutes)
    "1h":  1.30,
    "2h":  1.55,
    "4h":  1.80,
    "1D":  2.20,
    "1W":  2.80,
}

# ── Algorithm Protocols ──────────────────────────────────────────────────────
# Stop conditions for active programs. Higher position SMAs default to more
# lenient protocols; magnetized buys upgrade to candle_close.

PROTOCOL_PENNY_BREACH = "penny_breach"     # cut on single penny break of SMA
PROTOCOL_POINT_BREAK = "point_break"       # cut on full point break
PROTOCOL_CANDLE_CLOSE = "candle_close"     # cut on candle closing below SMA

# Default protocol per SMA position index (0=fastest, 5=slowest)
DEFAULT_PROTOCOLS = {
    0: PROTOCOL_PENNY_BREACH,
    1: PROTOCOL_PENNY_BREACH,
    2: PROTOCOL_PENNY_BREACH,
    3: PROTOCOL_POINT_BREAK,
    4: PROTOCOL_POINT_BREAK,
    5: PROTOCOL_CANDLE_CLOSE,
}

# ── Ticker Universe ─────────────────────────────────────────────────────────
# yfinance symbol mapping (indices need ^ prefix)

YFINANCE_SYMBOL_MAP = {
    "SPX": "^GSPC",
    "IXIC": "^IXIC",
    "DJI": "^DJI",
    "VIX": "^VIX",
    "DXY": "DX-Y.NYB",
}

TICKERS = [
    # Major indices
    "SPX", "IXIC", "DJI",
    # Index ETFs
    "SPY", "QQQ", "DIA", "IWM",
    # Leveraged / Inverse
    "TQQQ", "SQQQ", "UPRO", "SDOW", "UDOW", "SOXL", "SOXS", "SPXU", "SSO", "SDS", "DOG", "MYY", "UMDD",
    # Volatility
    "VIX", "UVIX", "UVXY", "SVIX", "SVXY",
    # Currency
    "DXY",
    # Mega-caps
    "AAPL", "MSFT", "AMZN", "GOOG", "NVDA", "META", "TSLA", "AMD", "NFLX",
    # Financials
    "JPM", "V", "XLF", "FAS",
    # Leveraged single-stock
    "TSLQ", "TSLR", "TSLZ", "ORCX", "AAPU", "AAPD", "TSLT", "MSTX", "TSLL",
    # Commodities / Bonds / Gold
    "GLD", "TLT", "TBT", "USO", "SCO",
    # Crypto / BTC-linked
    "BTC", "BITO", "BITU", "BITI", "MSTR",
    # Nuclear / Energy
    "SMR", "OKLO",
    # Real Estate
    "DRN",
    # Sector leveraged (from Raul's spec)
    "ERX", "LABU", "GUSH", "DRIP", "BOIL", "WEBS", "REK",
    # China inverse
    "YANG", "YINN",
    # Other (from Raul's spec)
    "COIN", "QCOM", "PYPL", "AI", "GME", "UNH", "ARM",
    "INTC", "UPST", "RBLX", "GM", "ENPH", "UWM",
    "BABA", "TSM",
    # Meme / High-vol
    "NKLA", "EOSE", "AMC", "BYND", "CVNA",
    # EV / RIVN confirmed Apr 29 2026 on SVIX (211) outfit
    "RIVN",
    # Apr 29 2026 long trades: MSFL (22² outfit 32M) + NVDX (Nikkei 225 outfit 30M)
    "MSFL", "NVDX",
    # May 7 2026: SAB (15M MA180=3.63 speculative) + SABS (2H MA650=3.410 full conviction, magnetized)
    "SAB", "SABS",
]

# Light scan: just the most important tickers
TICKERS_LIGHT = [
    "SPX", "IXIC", "DJI",
    "SPY", "QQQ", "DIA", "SSO",
    "TQQQ", "SQQQ", "NVDA",
    "TSLA", "TSLQ", "TSLR", "TSLZ", "TSLT", "TSLL",
    "UVIX", "SVIX",
    "ORCX", "AAPU",
    "SOXL", "SOXS", "SMR", "MSTX", "MSTR", "SCO", "DRN", "FAS", "DOG", "MYY", "UMDD",
    # Raul Apr 8 2026 recession trades: oil shock + global equity risk-off
    "ERX", "YANG",
    # Raul Apr 9 2026 area-code confirmations: oil (USO via 408) + META (650)
    # SCO already in light list above via Octane (818); now also on Octuple (816).
    "USO", "META",
    "DXY", "BTC",
    # Raul Apr 14 2026 Bitcoin (248) threaded trade: BITI + SPXU + WEBS (after hours)
    "BITI", "SPXU", "WEBS",
    # Raul Apr 29 2026 FOMC bear basket: SVIX lead + SQQQ threaded (stop 52.22)
    "SQQQ", "UVIX",
    # RIVN confirmed Apr 29 2026 — SVIX (211) 2H MA855 long@15.14
    "RIVN",
    # Apr 29 2026 post-FOMC longs: MSFL (22² outfit 32M) + NVDX (Nikkei 225 30M)
    "MSFL", "NVDX",
    # May 8 2026: BYND (REPEATER_9) + SABS (Hantavirus 650) — volume monitor tracking
    "BYND", "SABS",
]

# TSLA scan: Tesla family + DXY correlation
TICKERS_TSLA = [
    "TSLA", "TSLR", "TSLQ", "TSLZ", "TSLT", "TSLL", "NKLA", "DXY",
]

# ── Timeframe Configs ───────────────────────────────────────────────────────
# yfinance interval → (yf_interval, resample_from, history_period)
# For timeframes not natively supported, we resample from a smaller interval.

TIMEFRAMES: Dict[str, dict] = {
    # 1m: Schwab-only. Used for HFT arbitrage outfits like Russia Pres (2000) on indices.
    "1m":  {"yf_interval": None,  "resample_from": None, "resample_factor": 1,  "period": None},
    # 2m: Schwab-only (resampled from 1m). Confirmed Apr 14 2026: Raul SOXS 2M Octuple (816).
    "2m":  {"yf_interval": None,  "resample_from": "1m", "resample_factor": 2,  "period": None},
    # 3m: Schwab-only (resampled from 1m). yfinance fallback will return None for this timeframe.
    "3m":  {"yf_interval": None,  "resample_from": "1m", "resample_factor": 3,  "period": None},
    # 32m: Schwab-only (resampled from 2m). Confirmed Apr 29 2026: Raul MSFL 22²(484) trade.
    # 32 = 2^5 fits binary math pattern. Resample from 2m (factor 16) to reduce API calls.
    "32m": {"yf_interval": None,  "resample_from": "2m", "resample_factor": 16, "period": None},
    "5m":  {"yf_interval": "5m",  "resample_from": None, "resample_factor": 1,  "period": "60d"},
    # 10m: Schwab-only (native 10m candles). Raul uses this timeframe.
    "10m": {"yf_interval": None,  "resample_from": None, "resample_factor": 1,  "period": None},
    "15m": {"yf_interval": "15m", "resample_from": None, "resample_factor": 1,  "period": "60d"},
    "20m": {"yf_interval": "5m",  "resample_from": "5m", "resample_factor": 4,  "period": "60d"},
    "30m": {"yf_interval": "30m", "resample_from": None, "resample_factor": 1,  "period": "60d"},
    "1h":  {"yf_interval": "60m", "resample_from": None, "resample_factor": 1,  "period": "60d"},
    "2h":  {"yf_interval": "60m", "resample_from": "1h", "resample_factor": 2,  "period": "60d"},
    "4h":  {"yf_interval": "60m", "resample_from": "1h", "resample_factor": 4,  "period": "60d"},
    "1D":  {"yf_interval": "1d",  "resample_from": None, "resample_factor": 1,  "period": "5y"},
    "1W":  {"yf_interval": "1wk", "resample_from": None, "resample_factor": 1,  "period": "5y"},
}

# Primary detection timeframes (per spec section 6.1.1)
# 1m included so arbitrage-subtype outfits (Russia Pres 2000) can fire on indices.
PRIMARY_TIMEFRAMES = ["1m", "2m", "3m", "5m", "10m", "15m", "20m", "30m", "32m", "1h"]
SECONDARY_TIMEFRAMES = ["2h", "4h", "1D", "1W"]

# Arbitrage/HFT timeframes — used only for arbitrage-subtype outfits.
# Raul confirmed Russia Pres (2000) operates on 1m for SPX/IXIC/DJI as pure HFT whipsaw.
ARBITRAGE_TIMEFRAMES = ["1m", "3m", "5m"]

# ── System Outfit Crossover Config ──────────────────────────────────────────
# Used only for institutional bias computation (not for hit-counting)

SYSTEM_CROSSOVERS = {
    # Timeframes per Raul Apr 9 2026 canonical spec.
    "S&P": {"ticker": "SPX",  "timeframe": "30m", "fast": 10, "slow": 50},
    "NAS": {"ticker": "IXIC", "timeframe": "20m", "fast": 20, "slow": 100},
    "DJI": {"ticker": "DJI",  "timeframe": "1h",  "fast": 90, "slow": 300},
}


def yf_symbol(ticker: str) -> str:
    """Convert our ticker name to yfinance symbol."""
    return YFINANCE_SYMBOL_MAP.get(ticker, ticker)


def position_weights(outfit_name: str) -> List[float]:
    """Return position weights for an outfit based on its SMA count."""
    periods = OUTFITS[outfit_name]["periods"]
    if len(periods) == 3:
        return POSITION_WEIGHTS_3
    if len(periods) == 7:
        return POSITION_WEIGHTS_7
    return POSITION_WEIGHTS_6


def is_affinity(outfit_name: str, ticker: str) -> bool:
    """Check if ticker has primary affinity with the outfit."""
    return ticker in AFFINITIES.get(outfit_name, [])


# ── Reverse Affinity Map ──────────────────────────────────────────────────
# Ticker → set of outfits that are known to operate on it.
# Built from AFFINITIES. System outfits (S&P, NAS, DJI) always apply.

SYSTEM_OUTFITS = {"S&P", "NAS", "DJI"}

# Canonical system tickers per Raul Apr 9 2026 tweet.
# These four are the ONLY equities with a permanent, reliable outfit
# relationship. Their scanning is restricted to confirmed outfits (canonical
# system + HFT arbitrage). Every other ticker scans all outfits, with
# historical affinities applied as a score boost via is_affinity().
CANONICAL_SYSTEM_TICKERS = {"SPX", "IXIC", "DJI", "VIX"}

def _build_ticker_outfit_map() -> Dict[str, set[str]]:
    """Build reverse map: ticker → set of outfit names with affinity."""
    result: Dict[str, set[str]] = {}
    for outfit_name, tickers_list in AFFINITIES.items():
        for t in tickers_list:
            if t not in result:
                result[t] = set()
            result[t].add(outfit_name)
    return result

TICKER_OUTFIT_MAP = _build_ticker_outfit_map()


def outfits_for_ticker(ticker: str) -> Optional[Set[str]]:
    """
    Return the set of outfits to scan for a given ticker.

    Canonical system tickers (SPX, IXIC, DJI, VIX) are RESTRICTED to their
    known affinity outfits — the canonical Raul Apr 9 2026 system outfit
    plus any confirmed HFT arbitrage outfits (Russia Pres 2000 on the three
    indices). These four tickers have a permanent, reliable outfit
    relationship per Raul's clarification.

    ALL OTHER TICKERS scan the full outfit universe (return None). Historical
    affinity entries are still honored as a 2× score boost via is_affinity()
    in engine.py, so Tesla-family tickers still emphasize TSLA (420), META
    emphasizes Menlo Park (650), NVDA/AAPL emphasize Octuple (816), etc. —
    but they're no longer restricted to only those outfits. This reflects
    Raul Apr 9 2026: 'No individual stock operates on a singular outfit.
    [...] It can also be on any other timeframe [...] or it doesn't operate
    on any specific outfit'.

    Returns:
        A set of outfit names if the ticker is restricted (canonical system
        tickers), or None meaning "scan all outfits" for everything else.
    """
    if ticker in CANONICAL_SYSTEM_TICKERS and ticker in TICKER_OUTFIT_MAP:
        return TICKER_OUTFIT_MAP[ticker]
    return None  # scan all outfits; is_affinity() provides score boost
