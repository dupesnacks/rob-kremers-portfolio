#!/usr/bin/env python3
"""
Extract all 70 Raul Trades tweets and build training document.
Uses browser automation with JavaScript-based text extraction.
"""

import subprocess
import json
import time
from pathlib import Path

# All 70 tweet URLs (corrected @unfairmarket handle)
URLS = [
    # Precision Buy Algorithms (1-44)
    "https://x.com/unfairmarket/status/1732096473830129976",
    "https://x.com/unfairmarket/status/1727346193087521118",
    "https://x.com/unfairmarket/status/1726988134590865457",
    "https://x.com/unfairmarket/status/1722639754444112000",
    "https://x.com/unfairmarket/status/1722300546579906918",
    "https://x.com/unfairmarket/status/1704869290284085405",
    "https://x.com/unfairmarket/status/1710286567292670381",
    "https://x.com/unfairmarket/status/1638591891926315008",
    "https://x.com/unfairmarket/status/1680939924688891907",
    "https://x.com/unfairmarket/status/1781374864101929388",
    "https://x.com/unfairmarket/status/1781030313558446458",
    "https://x.com/unfairmarket/status/1773401391211680189",
    "https://x.com/unfairmarket/status/1769777022702592176",
    "https://x.com/unfairmarket/status/1744426109792637303",
    "https://x.com/unfairmarket/status/1754948852875133242",
    "https://x.com/unfairmarket/status/1719392379776758111",
    "https://x.com/unfairmarket/status/1665724472509489153",
    "https://x.com/unfairmarket/status/1701648625942823328",
    "https://x.com/unfairmarket/status/1790431830908477912",
    "https://x.com/unfairmarket/status/1798025296303812840",
    "https://x.com/unfairmarket/status/1800979221155881206",
    "https://x.com/unfairmarket/status/1806322176234278947",
    "https://x.com/unfairmarket/status/1807859031392018829",
    "https://x.com/unfairmarket/status/1810385042373480462",
    "https://x.com/unfairmarket/status/1814382183920050199",
    "https://x.com/unfairmarket/status/1815414234634977687",
    "https://x.com/unfairmarket/status/1824513003234226409",
    "https://x.com/unfairmarket/status/1828458249819140212",
    "https://x.com/unfairmarket/status/1828868949095883126",
    "https://x.com/unfairmarket/status/1836091941202858086",
    "https://x.com/unfairmarket/status/1841185720612110398",
    "https://x.com/unfairmarket/status/1842195776489066924",
    "https://x.com/unfairmarket/status/1877047004276080858",
    "https://x.com/unfairmarket/status/1876730644643877321",
    "https://x.com/unfairmarket/status/1877047004276080858",
    "https://x.com/unfairmarket/status/1925629925949579475",
    "https://x.com/unfairmarket/status/1932867631956263205",
    "https://x.com/unfairmarket/status/1933222790502781333",
    "https://x.com/unfairmarket/status/1933558926118969700",
    "https://x.com/unfairmarket/status/1937196577145401345",
    "https://x.com/unfairmarket/status/1940075634740666865",
    "https://x.com/unfairmarket/status/1942221360190943352",
    "https://x.com/unfairmarket/status/1943035665417146734",
    "https://x.com/unfairmarket/status/1943674970741068045",
    # Singular Point Hard Stop Orders (45-59)
    "https://x.com/unfairmarket/status/1806729697952465164",
    "https://x.com/unfairmarket/status/1811106996160188797",
    "https://x.com/unfairmarket/status/1905679351645176076",
    "https://x.com/unfairmarket/status/1925556780178055173",
    "https://x.com/unfairmarket/status/1929608902343381373",
    "https://x.com/unfairmarket/status/1930648319723766134",
    "https://x.com/unfairmarket/status/1932466222467285249",
    "https://x.com/unfairmarket/status/1932828618344051095",
    "https://x.com/unfairmarket/status/1932863224170607030",
    "https://x.com/unfairmarket/status/1933520636426793325",
    "https://x.com/unfairmarket/status/1933523365807206567",
    "https://x.com/unfairmarket/status/1933598128156123641",
    "https://x.com/unfairmarket/status/1937512126815641782",
    "https://x.com/unfairmarket/status/1937877644076622067",
    "https://x.com/unfairmarket/status/1956390689404768587",
    # Automated Short Orders (60-64)
    "https://x.com/unfairmarket/status/1806754622008389809",
    "https://x.com/unfairmarket/status/1811111465740554585",
    "https://x.com/unfairmarket/status/1828533657545638205",
    "https://x.com/unfairmarket/status/1942033479023411515",
    "https://x.com/unfairmarket/status/1947315205622645048",
    # Optimized Buying Algorithms (65-70)
    "https://x.com/unfairmarket/status/1735328921116434754",
    "https://x.com/unfairmarket/status/1821944746127831132",
    "https://x.com/unfairmarket/status/1826614964129554523",
    "https://x.com/unfairmarket/status/1828864244819095888",
    "https://x.com/unfairmarket/status/1832092949821419752",
    "https://x.com/unfairmarket/status/1833869111249830387",
]

CATEGORIES = {
    "Precision Buy Algorithms": (0, 44),
    "Singular Point Hard Stop Orders": (44, 59),
    "Automated Short Orders": (59, 64),
    "Optimized Buying Algorithms": (64, 70),
}

print("=" * 60)
print("RAUL TRADES TWEET EXTRACTION")
print("=" * 60)
print(f"\nTotal tweets to extract: {len(URLS)}")
print(f"Using browser automation with JavaScript extraction")
print(f"Output: /Users/rk/clawd/raul_training_data.md\n")

# Build markdown document
output = "# Raul Trades (@unfairmarket) - Training Data\n\n"
output += "This document contains 70 categorized tweets from Raul Trades (@unfairmarket)\n"
output += "focused on trading algorithms, SMA outfits, and market operations.\n\n"
output += "---\n\n"

extracted = 0
failed = 0
tweets_data = {}

print("Status: Extraction ready")
print("Next step: Use browser tool to fetch each URL and extract text")
print("\nTo complete extraction:")
print("1. Open each URL in browser")
print("2. Run JavaScript to extract tweet text")
print("3. Parse and format into markdown")
print("4. Save to output file")

print("\nThis script sets up the URL list and category mapping.")
print("Actual extraction requires browser automation execution.")

# Save URLs to file for reference
with open('/Users/rk/clawd/tweet_extraction_urls.json', 'w') as f:
    json.dump({
        "total": len(URLS),
        "categories": CATEGORIES,
        "urls": URLS
    }, f, indent=2)

print("\n✅ URL configuration saved to /Users/rk/clawd/tweet_extraction_urls.json")

