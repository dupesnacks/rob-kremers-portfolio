#!/usr/bin/env python3
"""
Analyze @ghostxswings tweets for patterns, themes, and trades.
Focuses on actionable trade calls and macro commentary.
"""

import json
import os
from collections import Counter
import re

def load_tweets():
    """Load all archived ghostxswings tweets"""
    archive_file = "memory/ghostxswings-tweets.jsonl"
    tweets = []
    
    if not os.path.exists(archive_file):
        print(f"No tweets found in {archive_file}")
        return tweets
    
    with open(archive_file, 'r') as f:
        for line in f:
            try:
                tweet = json.loads(line)
                tweets.append(tweet)
            except:
                pass
    
    return tweets

def extract_tickers(text):
    """Extract ticker symbols from tweet text"""
    pattern = r'\$([A-Z]{1,5})\b'
    return re.findall(pattern, text)

def extract_patterns(text):
    """Extract trading patterns and keywords"""
    patterns = {
        'trade_call': r'(trade|short|long|buy|sell|entry|exit|target)',
        'squeeze': r'(squeeze|cover|covering)',
        'support_resistance': r'(support|resistance|level|break|hold)',
        'technicals': r'(wedge|channel|breakout|consolidation|reversal|pattern)',
        'sentiment': r'(bullish|bearish|neutral|bullish sentiment|bearish pressure)',
        'liquidity': r'(liquidity|volume|thin|thick|spike)',
    }
    
    found = {}
    for pattern_name, pattern_regex in patterns.items():
        if re.search(pattern_regex, text, re.IGNORECASE):
            found[pattern_name] = True
    
    return found

def analyze():
    tweets = load_tweets()
    
    if not tweets:
        print("No tweets to analyze")
        return
    
    # Basic stats
    total_tweets = len(tweets)
    tickers = Counter()
    patterns = Counter()
    high_engagement = []
    
    # Collect stats
    for tweet in tweets:
        # Tickers
        tweet_tickers = extract_tickers(tweet['text'])
        for ticker in tweet_tickers:
            tickers[ticker] += 1
        
        # Patterns
        tweet_patterns = extract_patterns(tweet['text'])
        for pattern in tweet_patterns:
            patterns[pattern] += 1
        
        # High engagement (trade calls worth noting)
        likes = tweet.get('public_metrics', {}).get('like_count', 0)
        if likes > 5 or 'trade' in tweet['text'].lower():
            high_engagement.append({
                'created_at': tweet['created_at'],
                'text': tweet['text'][:150],
                'likes': likes
            })
    
    # Generate report
    report = f"""# @ghostxswings Tweet Analysis

**Archived:** {json.loads(open('memory/ghostxswings-tweets.jsonl').readlines()[-1])['archived_at']}
**Total Tweets:** {total_tweets}
**Note:** This account deletes tweets frequently. This archive captures snapshots; check daily for new activity before tweets are deleted.

## Top Tickers Mentioned

"""
    
    for ticker, count in tickers.most_common(15):
        report += f"- **{ticker}**: {count} mentions\n"
    
    report += "\n## Key Themes\n\n"
    for pattern, count in patterns.most_common(10):
        report += f"- **{pattern}**: {count} tweets\n"
    
    report += "\n## Recent High-Engagement Tweets (Possible Trade Calls)\n\n"
    
    for item in sorted(high_engagement, key=lambda x: x['created_at'], reverse=True)[:10]:
        report += f"**{item['created_at']}** ({item['likes']} likes)\n"
        report += f"> {item['text']}\n\n"
    
    # Save report
    with open('memory/ghostxswings-analysis.md', 'w') as f:
        f.write(report)
    
    print(f"Loading tweets from memory/ghostxswings-tweets.jsonl...")
    print(f"Analyzing {total_tweets} tweets...")
    print(f"Saved analysis to memory/ghostxswings-analysis.md")
    print(f"\n=== SUMMARY ===")
    print(f"Total tweets: {total_tweets}")
    print(f"Unique tickers: {len(tickers)}")
    print(f"Unique patterns: {len(patterns)}")
    print(f"\nTop 5 tickers: {tickers.most_common(5)}")

if __name__ == "__main__":
    analyze()
