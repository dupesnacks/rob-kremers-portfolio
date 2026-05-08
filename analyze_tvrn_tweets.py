#!/usr/bin/env python3
"""
Analyze @tvRN20 tweets to extract:
- Tickers mentioned
- Chart patterns (wedge, squeeze, support/resistance)
- Macro themes (Fed, liquidity, phases)
- Key levels and analysis
Outputs: summary + indexed markdown for searching
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

def load_tweets(filepath):
    """Load tweets from JSONL file."""
    tweets = []
    with open(filepath) as f:
        for line in f:
            tweets.append(json.loads(line))
    return tweets

def extract_tickers(text):
    """Extract stock tickers ($ prefix or all caps words)."""
    # Look for $TICKER format or common patterns
    tickers = set()
    
    # $TICKER pattern
    dollar_tickers = re.findall(r'\$([A-Z]{1,5})\b', text)
    tickers.update(dollar_tickers)
    
    # Common single/double letter tickers in context
    # Skip common words
    common_words = {'THE', 'AND', 'BUT', 'FOR', 'ARE', 'YOU', 'CAN', 'NOT', 'GET', 'OUT', 'ALL', 'ONE', 'TWO', 'NOW', 'WAY'}
    all_caps = re.findall(r'\b([A-Z]{1,5})\b', text)
    
    # Filter: keep if 2-5 chars and not common word
    for ticker in all_caps:
        if len(ticker) >= 1 and ticker not in common_words and ticker not in dollar_tickers:
            # Only keep if looks like a ticker context
            if ticker in ['GME', 'BYND', 'CAR', 'HTZ', 'GRPN', 'BMBL', 'DOGE', 'BTC', 'ETH', 'TSLA', 'SPY', 'QQQ', 'NVDA', 'AAPL']:
                tickers.add(ticker)
    
    return tickers

def extract_patterns(text):
    """Extract chart/market patterns mentioned."""
    patterns = []
    
    # Chart patterns
    if 'wedge' in text.lower() or '📐' in text:
        patterns.append('wedge')
    if 'squeeze' in text.lower():
        patterns.append('squeeze')
    if 'support' in text.lower() or 'resistance' in text.lower():
        patterns.append('support/resistance')
    if 'breakout' in text.lower() or 'break' in text.lower():
        patterns.append('breakout')
    if 'reversal' in text.lower():
        patterns.append('reversal')
    if 'consolidat' in text.lower():
        patterns.append('consolidation')
    
    # Market phases
    if 'fear' in text.lower():
        patterns.append('phase_fear')
    if 'speculation' in text.lower() or 'speculative' in text.lower():
        patterns.append('phase_speculation')
    if 'abundance' in text.lower():
        patterns.append('phase_abundance')
    
    # Key concepts
    if 'liquidity' in text.lower():
        patterns.append('liquidity')
    if 'short' in text.lower() and 'interest' in text.lower():
        patterns.append('short_interest')
    if 'positioning' in text.lower() or 'positioned' in text.lower():
        patterns.append('positioning')
    if 'wall of denial' in text.lower():
        patterns.append('wall_of_denial')
    if 'fed' in text.lower() or 'rate' in text.lower():
        patterns.append('fed/rates')
    
    return patterns

def extract_levels(text):
    """Extract price levels and numbers."""
    # Look for $ prices or percentage moves
    levels = []
    
    # $1.23 format
    prices = re.findall(r'\$([0-9.]+)', text)
    levels.extend([f"${p}" for p in prices[:5]])  # First 5 mentions
    
    # Percentage moves
    percents = re.findall(r'([0-9.]+)%', text)
    levels.extend([f"{p}%" for p in percents[:3]])
    
    return levels

def generate_summary(tweets):
    """Generate analysis summary."""
    
    all_tickers = Counter()
    all_patterns = Counter()
    tweets_by_date = defaultdict(list)
    
    ticker_context = defaultdict(list)  # Ticker -> list of tweets mentioning it
    pattern_tweets = defaultdict(list)  # Pattern -> list of tweets
    
    for tweet in tweets:
        text = tweet.get('text', '')
        date = tweet['created_at'][:10]
        
        tickers = extract_tickers(text)
        patterns = extract_patterns(text)
        levels = extract_levels(text)
        
        all_tickers.update(tickers)
        all_patterns.update(patterns)
        
        tweets_by_date[date].append({
            'text': text,
            'tickers': tickers,
            'patterns': patterns,
            'levels': levels,
            'created_at': tweet['created_at'],
            'likes': tweet.get('public_metrics', {}).get('like_count', 0),
        })
        
        for ticker in tickers:
            ticker_context[ticker].append(text)
        for pattern in patterns:
            pattern_tweets[pattern].append(text)
    
    return {
        'total_tweets': len(tweets),
        'all_tickers': dict(all_tickers.most_common(30)),
        'all_patterns': dict(all_patterns.most_common(20)),
        'ticker_context': {k: v[:3] for k, v in ticker_context.items()},  # First 3 mentions
        'pattern_tweets': {k: v[:2] for k, v in pattern_tweets.items()},  # First 2 examples
    }

def save_analysis(summary, output_file):
    """Save analysis to markdown."""
    content = f"""# TVRN Tweet Analysis

**Archived:** {datetime.now().isoformat()}
**Total Tweets:** {summary['total_tweets']}

## Top Tickers Mentioned

"""
    
    for ticker, count in list(summary['all_tickers'].items())[:20]:
        content += f"- **{ticker}**: {count} mentions\n"
    
    content += "\n## Key Patterns & Themes\n\n"
    
    for pattern, count in list(summary['all_patterns'].items())[:20]:
        content += f"- **{pattern}**: {count} mentions\n"
    
    content += "\n## Examples by Pattern\n\n"
    
    for pattern, examples in summary['pattern_tweets'].items():
        content += f"### {pattern}\n"
        for ex in examples:
            content += f"> {ex[:150]}...\n\n"
    
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(content)
    print(f"Saved analysis to {output_file}")

if __name__ == "__main__":
    tweets_file = Path.home() / "clawd" / "memory" / "tvrn-tweets.jsonl"
    output_file = Path.home() / "clawd" / "memory" / "tvrn-analysis.md"
    
    print(f"Loading tweets from {tweets_file}...")
    tweets = load_tweets(tweets_file)
    
    print(f"Analyzing {len(tweets)} tweets...")
    summary = generate_summary(tweets)
    
    save_analysis(summary, output_file)
    
    # Print stats
    print(f"\n=== SUMMARY ===")
    print(f"Total tweets: {summary['total_tweets']}")
    print(f"Unique tickers: {len(summary['all_tickers'])}")
    print(f"Unique patterns: {len(summary['all_patterns'])}")
    print(f"\nTop 10 tickers: {list(summary['all_tickers'].items())[:10]}")
