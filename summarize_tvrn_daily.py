#!/usr/bin/env python3
"""
Daily TVRN tweet summary.
Extracts the most important tweets from today, scores by conviction/relevance.
Outputs: tvrn-daily-summary.md
Runs at 22:00 PDT via cron.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

# Conviction keywords (high importance)
CONVICTION_WORDS = {
    'will': 2, 'must': 3, 'has to': 3, 'guaranteed': 3,
    'incoming': 2, 'imminent': 2, 'locked': 2,
    'bull': 2, 'bear': 2, 'squeeze': 3, 'trap': 2,
    'liquidity': 2, 'positioning': 2, 'phase': 2,
    'wall of denial': 3, 'ponzi': 3, 'manufactured': 2,
    'may 15': 3, 'fed': 2, 'intervention': 2,
}

# Asset mentions (track what he's focusing on)
KEY_ASSETS = ['BTC', 'SPY', 'DOGE', 'TSLA', 'GME', 'BYND', 'ETH', 'GOLD', 'DXY', 'VIX']

def score_tweet(text):
    """Score tweet by conviction + relevance."""
    score = 0
    text_lower = text.lower()
    
    # Conviction keywords
    for word, points in CONVICTION_WORDS.items():
        if word in text_lower:
            score += points
    
    # Asset mentions
    for asset in KEY_ASSETS:
        if asset in text:
            score += 1
    
    # Chart references (high importance)
    if 'chart' in text_lower or 'chart' in text or '📐' in text:
        score += 3
    
    # Framework concepts
    if any(phrase in text_lower for phrase in ['fear', 'speculation', 'abundance', 'reset']):
        score += 2
    
    # Deleted tweets (marked) are less valuable (already saw them)
    if 'DELETED' in text:
        score = 0
    
    # Length as proxy for substance (longer = more detailed)
    length_bonus = min(len(text) // 100, 2)
    score += length_bonus
    
    return score

def get_today_tweets(tweets_file):
    """Get all tweets from today."""
    today = datetime.utcnow().date()
    today_tweets = []
    
    with open(tweets_file) as f:
        for line in f:
            tweet = json.loads(line)
            tweet_date = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00')).date()
            
            if tweet_date == today:
                # Score the tweet
                score = score_tweet(tweet['text'])
                today_tweets.append({
                    'text': tweet['text'],
                    'created_at': tweet['created_at'],
                    'likes': tweet.get('public_metrics', {}).get('like_count', 0),
                    'score': score,
                })
    
    return sorted(today_tweets, key=lambda x: x['score'], reverse=True)

def extract_themes(tweets):
    """Extract themes from today's tweets."""
    all_text = ' '.join([t['text'] for t in tweets])
    
    themes = {
        'phase_signals': [],
        'assets_mentioned': Counter(),
        'key_levels': [],
        'timing_callouts': [],
    }
    
    # Phase signals
    for phrase in ['fear', 'speculation', 'abundance', 'reset', 'wall of denial', 'squeeze']:
        if phrase in all_text.lower():
            themes['phase_signals'].append(phrase)
    
    # Assets
    for asset in KEY_ASSETS:
        count = all_text.count(asset)
        if count > 0:
            themes['assets_mentioned'][asset] = count
    
    # Timing
    for phrase in ['may 15', 'fed', 'june', 'transition', 'window']:
        if phrase in all_text.lower():
            themes['timing_callouts'].append(phrase)
    
    return themes

def generate_summary(tweets, themes):
    """Generate markdown summary."""
    
    content = f"""# TVRN Daily Summary
**Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Total tweets today:** {len(tweets)}
**Top tweets by conviction:** {sum(1 for t in tweets if t['score'] > 0)}

---

## Top 5 Tweets (by conviction score)

"""
    
    for i, tweet in enumerate(tweets[:5], 1):
        if tweet['score'] == 0:
            continue
        
        content += f"""### {i}. [{tweet['score']} conviction]
**Time:** {tweet['created_at']}  
**Likes:** {tweet['likes']}

> {tweet['text'][:300]}{"..." if len(tweet['text']) > 300 else ""}

---

"""
    
    content += """## Today's Themes

"""
    
    if themes['phase_signals']:
        content += f"**Phase Signals:** {', '.join(set(themes['phase_signals']))}\n\n"
    
    if themes['assets_mentioned']:
        content += "**Assets Mentioned:**\n"
        for asset, count in themes['assets_mentioned'].most_common(8):
            content += f"- {asset}: {count}x\n"
        content += "\n"
    
    if themes['timing_callouts']:
        content += f"**Timing Callouts:** {', '.join(set(themes['timing_callouts']))}\n\n"
    
    content += """---

## Interpretation (What He's Saying Today)

"""
    
    # Auto-interpret based on themes
    if 'squeeze' in themes['phase_signals']:
        content += "- **Squeeze mechanics:** He's analyzing current squeeze setups or positioning\n"
    
    if 'may 15' in ' '.join(themes['timing_callouts']):
        content += "- **May 15 focus:** Fed decision is active concern — tracking liquidity injection timing\n"
    
    if themes['assets_mentioned'].get('BTC', 0) > themes['assets_mentioned'].get('SPY', 0):
        content += "- **Macro tilt:** Crypto/commodities leading narrative (phase shift signal?)\n"
    
    if 'speculation' in themes['phase_signals'] or 'abundance' in themes['phase_signals']:
        content += "- **Phase transition:** Appears to be tracking movement from Fear toward Speculation/Abundance\n"
    
    content += """

---

## Next Actions

1. Cross-reference top tweets with your institutional data (Schwab L/S, Raul bias)
2. Check BYND/CAR/HTZ volume if squeeze mentioned
3. Monitor TSLA hedge ratio if liquidity discussed
4. Watch Fed expectations if May 15 mentioned
5. Review chart setups he called out

---

**Generated automatically. Use to train your intuition on his thinking patterns.**
"""
    
    return content

def save_summary(content, output_file):
    """Save to markdown."""
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(content)
    print(f"✅ Saved daily summary to {output_file}")

if __name__ == "__main__":
    tweets_file = Path.home() / "clawd" / "memory" / "tvrn-tweets.jsonl"
    output_file = Path.home() / "clawd" / "memory" / "tvrn-daily-summary.md"
    
    today_tweets = get_today_tweets(tweets_file)
    
    if not today_tweets:
        print("No tweets today yet.")
        summary_content = f"# TVRN Daily Summary\n**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}\n\nNo tweets archived yet for today.\n"
    else:
        themes = extract_themes(today_tweets)
        summary_content = generate_summary(today_tweets, themes)
    
    save_summary(summary_content, output_file)
    
    print(f"\nSummary stats:")
    print(f"- Tweets today: {len(today_tweets)}")
    if today_tweets:
        print(f"- Top score: {today_tweets[0]['score']}")
        print(f"- Avg score: {sum(t['score'] for t in today_tweets) / len(today_tweets):.1f}")
