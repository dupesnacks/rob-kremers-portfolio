import json
from datetime import datetime, timedelta
from collections import defaultdict

# Load tweets
tweets = []
with open('memory/ghostxswings-tweets.jsonl', 'r') as f:
    for line in f:
        tweets.append(json.loads(line))

# Filter for today (Apr 30)
today_tweets = [t for t in tweets if '2026-04-30' in t['created_at']]

# Sort by engagement (likes + retweets)
today_tweets_sorted = sorted(
    today_tweets,
    key=lambda x: x.get('public_metrics', {}).get('like_count', 0) + 
                  x.get('public_metrics', {}).get('retweet_count', 0),
    reverse=True
)

# Group by type
trade_calls = []
operational = []
other = []

for t in today_tweets_sorted:
    text = t['text'].lower()
    if any(x in text for x in ['1.55', 'break', 'magic', 'volume', 'squeeze', '$bynd', 'printer']):
        trade_calls.append(t)
    elif any(x in text for x in ['accept', 'telegram', 'whop', 'sunday', 'join', 'support']):
        operational.append(t)
    else:
        other.append(t)

# Generate recap
recap = "# ghostxswings Daily Recap — April 30, 2026\n\n"
recap += f"**Total tweets:** {len(today_tweets)}\n"
recap += f"**High-engagement tweets:** {len([t for t in today_tweets if t.get('public_metrics', {}).get('like_count', 0) >= 1])}\n"
recap += f"**Trade calls:** {len(trade_calls)}\n"
recap += f"**Operational:** {len(operational)}\n\n"

recap += "---\n\n## 🔥 HIGH-PRIORITY TRADE CALLS\n\n"
for i, tweet in enumerate(trade_calls[:5], 1):
    likes = tweet.get('public_metrics', {}).get('like_count', 0)
    retweets = tweet.get('public_metrics', {}).get('retweet_count', 0)
    recap += f"### {i}. [{likes}❤️ {retweets}🔄]\n"
    recap += f"**Time:** {tweet['created_at']}\n\n"
    recap += f"> {tweet['text']}\n\n"

recap += "---\n\n## 📊 OPERATIONAL UPDATES\n\n"
for i, tweet in enumerate(operational[:3], 1):
    likes = tweet.get('public_metrics', {}).get('like_count', 0)
    recap += f"### {i}. [{likes}❤️]\n"
    recap += f"**Time:** {tweet['created_at']}\n\n"
    recap += f"> {tweet['text']}\n\n"

recap += "---\n\n## 📈 KEY METRICS & PATTERNS\n\n"
recap += f"- **BYND mentions:** 3x\n"
recap += f"- **Volume emphasis:** High (stage 3 entry requirement)\n"
recap += f"- **Institutional signal:** Mikalche \"non stop printer\" accumulation\n"
recap += f"- **Options vs shares:** Emphasized options for leverage (tail risk hedge)\n"
recap += f"- **Target range:** $5–10 if $1.55 breaks\n"
recap += f"- **Group status:** 100+ accepted, Sunday deadline for enrollment\n\n"

recap += "---\n\n## ⚠️ RISK FACTORS MENTIONED\n\n"
recap += f"- Trump administration (don't hold shares, use options)\n"
recap += f"- Institutional selling pressure (BMNR example via Fundstrat)\n"
recap += f"- Rally chasing danger (31 days of blow-ups, winners in hindsight)\n\n"

recap += "---\n\n## 🎯 APRIL 30 OUTCOME\n\n"
recap += f"- **BYND $1.55 breakout:** ❌ Not broken (would have victory posts)\n"
recap += f"- **Setup status:** ✅ Carrying into May 1–14 (Friday retest likely)\n"
recap += f"- **Group execution:** Starting Friday (Sunday deadline = enrollment window)\n"

# Save
with open('memory/ghostxswings-daily-recap.md', 'w') as f:
    f.write(recap)

print(recap)
