#!/usr/bin/env python3
"""
Tweet scraper for @unfairmarket tweets
Extracts tweet text, timestamps, and view counts
"""

import json
import time
from datetime import datetime

# All 70 tweet URLs organized by category
tweets_data = {
    "Precision Buy Algorithms (1-44)": [
        (1, "https://x.com/unfairmarket/status/1732096473830129976"),
        (2, "https://x.com/unfairmarket/status/1727346193087521118"),
        (3, "https://x.com/unfairmarket/status/1726988134590865457"),
        (4, "https://x.com/unfairmarket/status/1722639754444112000"),
        (5, "https://x.com/unfairmarket/status/1722300546579906918"),
        (6, "https://x.com/unfairmarket/status/1704869290284085405"),
        (7, "https://x.com/unfairmarket/status/1710286567292670381"),
        (8, "https://x.com/unfairmarket/status/1638591891926315008"),
        (9, "https://x.com/unfairmarket/status/1680939924688891907"),
        (10, "https://x.com/unfairmarket/status/1781374864101929388"),
        (11, "https://x.com/unfairmarket/status/1781030313558446458"),
        (12, "https://x.com/unfairmarket/status/1773401391211680189"),
        (13, "https://x.com/unfairmarket/status/1769777022702592176"),
        (14, "https://x.com/unfairmarket/status/1744426109792637303"),
        (15, "https://x.com/unfairmarket/status/1754948852875133242"),
        (16, "https://x.com/unfairmarket/status/1719392379776758111"),
        (17, "https://x.com/unfairmarket/status/1665724472509489153"),
        (18, "https://x.com/unfairmarket/status/1701648625942823328"),
        (19, "https://x.com/unfairmarket/status/1790431830908477912"),
        (20, "https://x.com/unfairmarket/status/1798025296303812840"),
        (21, "https://x.com/unfairmarket/status/1800979221155881206"),
        (22, "https://x.com/unfairmarket/status/1806322176234278947"),
        (23, "https://x.com/unfairmarket/status/1807859031392018829"),
        (24, "https://x.com/unfairmarket/status/1810385042373480462"),
        (25, "https://x.com/unfairmarket/status/1814382183920050199"),
        (26, "https://x.com/unfairmarket/status/1815414234634977687"),
        (27, "https://x.com/unfairmarket/status/1824513003234226409"),
        (28, "https://x.com/unfairmarket/status/1828458249819140212"),
        (29, "https://x.com/unfairmarket/status/1828868949095883126"),
        (30, "https://x.com/unfairmarket/status/1836091941202858086"),
        (31, "https://x.com/unfairmarket/status/1841185720612110398"),
        (32, "https://x.com/unfairmarket/status/1842195776489066924"),
        (33, "https://x.com/unfairmarket/status/1877047004276080858"),
        (34, "https://x.com/unfairmarket/status/1876730644643877321"),
        (35, "https://x.com/unfairmarket/status/1877047004276080858"),
        (36, "https://x.com/unfairmarket/status/1925629925949579475"),
        (37, "https://x.com/unfairmarket/status/1932867631956263205"),
        (38, "https://x.com/unfairmarket/status/1933222790502781333"),
        (39, "https://x.com/unfairmarket/status/1933558926118969700"),
        (40, "https://x.com/unfairmarket/status/1937196577145401345"),
        (41, "https://x.com/unfairmarket/status/1940075634740666865"),
        (42, "https://x.com/unfairmarket/status/1942221360190943352"),
        (43, "https://x.com/unfairmarket/status/1943035665417146734"),
        (44, "https://x.com/unfairmarket/status/1943674970741068045"),
    ],
    "Singular Point Hard Stop Orders (45-59)": [
        (45, "https://x.com/unfairmarket/status/1806729697952465164"),
        (46, "https://x.com/unfairmarket/status/1811106996160188797"),
        (47, "https://x.com/unfairmarket/status/1905679351645176076"),
        (48, "https://x.com/unfairmarket/status/1925556780178055173"),
        (49, "https://x.com/unfairmarket/status/1929608902343381373"),
        (50, "https://x.com/unfairmarket/status/1930648319723766134"),
        (51, "https://x.com/unfairmarket/status/1932466222467285249"),
        (52, "https://x.com/unfairmarket/status/1932828618344051095"),
        (53, "https://x.com/unfairmarket/status/1932863224170607030"),
        (54, "https://x.com/unfairmarket/status/1933520636426793325"),
        (55, "https://x.com/unfairmarket/status/1933523365807206567"),
        (56, "https://x.com/unfairmarket/status/1933598128156123641"),
        (57, "https://x.com/unfairmarket/status/1937512126815641782"),
        (58, "https://x.com/unfairmarket/status/1937877644076622067"),
        (59, "https://x.com/unfairmarket/status/1956390689404768587"),
    ],
    "Automated Short Orders (60-64)": [
        (60, "https://x.com/unfairmarket/status/1806754622008389809"),
        (61, "https://x.com/unfairmarket/status/1811111465740554585"),
        (62, "https://x.com/unfairmarket/status/1828533657545638205"),
        (63, "https://x.com/unfairmarket/status/1942033479023411515"),
        (64, "https://x.com/unfairmarket/status/1947315205622645048"),
    ],
    "Optimized Buying Algorithms (65-70)": [
        (65, "https://x.com/unfairmarket/status/1735328921116434754"),
        (66, "https://x.com/unfairmarket/status/1821944746127831132"),
        (67, "https://x.com/unfairmarket/status/1826614964129554523"),
        (68, "https://x.com/unfairmarket/status/1828864244819095888"),
        (69, "https://x.com/unfairmarket/status/1832092949821419752"),
        (70, "https://x.com/unfairmarket/status/1833869111249830387"),
    ],
}

# Manually collected tweets (from browser snapshots)
collected_tweets = {
    1: {
        "text": "It's been all about the Nasdaq composite lately. Like this operation at 14171. Or that 3m maMA404. Just sharing so everyone can see it live and in real time too.",
        "time": "9:55 AM · Dec 5, 2023",
        "views": "26.9K"
    },
    2: {
        "text": "15s 46 outfit. 44.05. That's where the HFT was. Biden's outfit at ma736. They cut on a penny break.",
        "time": "7:19 AM · Nov 22, 2023",
        "views": "13.2K"
    },
    3: {
        "text": "2m ma999 43.29 . That's the only operation I see so far and this dip was very aggressive.",
        "time": "7:37 AM · Nov 21, 2023",
        "views": "41K"
    },
    4: {
        "text": "11/9/23 . 119 . Play on 911? World Trade Outfit. Think that 38.90 is risk if that's a candle close below operation. At least that's where the HFT has been striking. Advanced work. They liquidate on a penny break.",
        "time": "7:38 AM · Nov 9, 2023",
        "views": "4,764"
    },
}

# Save collected data to file
with open('/Users/rk/clawd/collected_tweets.json', 'w') as f:
    json.dump({
        'status': 'Script created for tweet collection',
        'tweets_to_collect': len([item for sublist in tweets_data.values() for item in sublist]),
        'collected_so_far': len(collected_tweets)
    }, f, indent=2)

print(f"Tweet collection script created.")
print(f"Total tweets to collect: 70")
print(f"Categories:")
for category, tweets in tweets_data.items():
    print(f"  - {category}: {len(tweets)} tweets")
