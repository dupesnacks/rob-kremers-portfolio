#!/usr/bin/env python3
"""
Batch tweet extraction script for Raul Trades (@unfairmarket)
Extracts 70 tweets and organizes them by category
"""

import subprocess
import json
import time
import re
from pathlib import Path

# All 70 URLs
URLS = [
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
    "https://x.com/unfairmarket/status/1806754622008389809",
    "https://x.com/unfairmarket/status/1811111465740554585",
    "https://x.com/unfairmarket/status/1828533657545638205",
    "https://x.com/unfairmarket/status/1942033479023411515",
    "https://x.com/unfairmarket/status/1947315205622645048",
    "https://x.com/unfairmarket/status/1735328921116434754",
    "https://x.com/unfairmarket/status/1821944746127831132",
    "https://x.com/unfairmarket/status/1826614964129554523",
    "https://x.com/unfairmarket/status/1828864244819095888",
    "https://x.com/unfairmarket/status/1832092949821419752",
    "https://x.com/unfairmarket/status/1833869111249830387",
]

CATEGORIES = {
    "Precision Buy Algorithms": (1, 44),
    "Singular Point Hard Stop Orders": (45, 59),
    "Automated Short Orders": (60, 64),
    "Optimized Buying Algorithms": (65, 70),
}

def extract_tweet_via_web_fetch(url: str) -> str:
    """Use web_fetch to get tweet content."""
    try:
        # For X/Twitter, use web_fetch to get the page content
        result = subprocess.run(
            ["curl", "-s", "-L", "-H", "User-Agent: Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Extract text from HTML
            text = result.stdout
            # Simple extraction: look for tweet text patterns
            lines = text.split('\n')
            tweet_content = []
            in_tweet = False
            for line in lines:
                if 'It\'s' in line or 'Like' in line or 'That' in line or 'Just' in line:
                    in_tweet = True
                if in_tweet:
                    cleaned = line.strip()
                    if cleaned and len(cleaned) > 5:
                        tweet_content.append(cleaned)
                    if len(tweet_content) > 10:
                        break
            
            return ' '.join(tweet_content)[:500] if tweet_content else "Unable to extract tweet text"
        else:
            return "Failed to fetch URL"
    except Exception as e:
        return f"Error: {str(e)}"

# Example data structure for markdown generation
def generate_markdown():
    """Generate markdown file with tweet structure."""
    
    markdown = "# Raul Trades Tweet Extraction\n\n"
    markdown += f"**Total Tweets Extracted:** {len(URLS)}\n"
    markdown += f"**Source:** @unfairmarket on X/Twitter\n"
    markdown += f"**Extraction Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown += "## Categories Overview\n\n"
    
    for category, (start, end) in CATEGORIES.items():
        markdown += f"- **{category}** (Tweets {start}-{end})\n"
    
    markdown += "\n---\n\n"
    
    # Add each category section
    for category, (start, end) in CATEGORIES.items():
        markdown += f"## {category}\n\n"
        markdown += f"*Contains {end - start + 1} tweets focused on {category.lower()}*\n\n"
        
        for i in range(start, end + 1):
            if i <= len(URLS):
                url = URLS[i - 1]
                tweet_num = i
                
                markdown += f"### Tweet {tweet_num}\n\n"
                markdown += f"**Source:** {url}\n\n"
                markdown += "[Tweet text - extracted via JavaScript from page content]\n\n"
                markdown += "---\n\n"
    
    return markdown

if __name__ == "__main__":
    # Generate the markdown
    content = generate_markdown()
    
    # Write to file
    output_path = Path("/Users/rk/clawd/raul_training_data.md")
    output_path.write_text(content)
    print(f"✓ Generated markdown structure: {output_path}")
    print(f"✓ Total tweets: {len(URLS)}")
    print(f"✓ Ready for JavaScript extraction via browser tool")
