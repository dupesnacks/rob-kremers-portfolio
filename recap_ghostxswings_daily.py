#!/usr/bin/env python3
"""
Daily recap of @ghostxswings tweets organized by date.
Shows recent days with high-engagement trade calls.
"""

import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

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

def generate_recap():
    tweets = load_tweets()
    
    if not tweets:
        print("No tweets to recap")
        return
    
    # Organize by date
    by_date = defaultdict(list)
    for tweet in tweets:
        date = tweet['created_at'].split('T')[0]  # YYYY-MM-DD
        by_date[date].append(tweet)
    
    # Generate recap
    recap = f"""# @ghostxswings Daily Recap

**Generated:** {datetime.utcnow().isoformat()}
**Archive Status:** {len(tweets)} tweets captured
**Date Range:** {min(by_date.keys())} to {max(by_date.keys())}

---

## Summary
⚠️ **Note:** This account deletes tweets frequently. Recap captures what was available during last sync.
- Tweets captured: {len(tweets)}
- Unique dates: {len(by_date)}
- Avg per day: {len(tweets) / len(by_date):.1f}

---

"""
    
    # Sort dates descending (most recent first)
    for date in sorted(by_date.keys(), reverse=True):
        day_tweets = sorted(by_date[date], key=lambda t: t['created_at'], reverse=True)
        recap += f"## {date}\n\n"
        
        total_likes = sum(t.get('public_metrics', {}).get('like_count', 0) for t in day_tweets)
        recap += f"**Tweets:** {len(day_tweets)} | **Total Likes:** {total_likes}\n\n"
        
        for tweet in day_tweets:
            time = tweet['created_at'].split('T')[1].split('.')[0]
            likes = tweet.get('public_metrics', {}).get('like_count', 0)
            text = tweet['text']
            
            recap += f"**{time} UTC** ({likes}❤️)\n"
            recap += f"> {text}\n\n"
        
        recap += "---\n\n"
    
    # Save recap
    with open('memory/ghostxswings-recap.md', 'w') as f:
        f.write(recap)
    
    print(f"Saved recap to memory/ghostxswings-recap.md")
    print(f"\n=== RECAP SUMMARY ===")
    print(f"Total tweets: {len(tweets)}")
    print(f"Date range: {min(by_date.keys())} to {max(by_date.keys())}")
    print(f"Recent day ({max(by_date.keys())}): {len(by_date[max(by_date.keys())])} tweets")

if __name__ == "__main__":
    generate_recap()
