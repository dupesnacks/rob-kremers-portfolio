#!/usr/bin/env python3
"""
Fetch new tweets from @ghostxswings (ID: 1557895057612705793)
Handles frequent tweet deletions by capturing daily snapshots.
"""

import json
import os
from datetime import datetime
import requests

def load_env():
    """Load X bearer token from .env.local"""
    with open('.env.local', 'r') as f:
        for line in f:
            if line.startswith('X_BEARER_TOKEN='):
                return line.strip().split('=', 1)[1]
    raise ValueError("X_BEARER_TOKEN not found in .env.local")

def fetch_ghostxswings_tweets():
    """Fetch latest tweets from @ghostxswings"""
    token = load_env()
    headers = {"Authorization": f"Bearer {token}"}
    
    user_id = "1557895057612705793"  # @ghostxswings
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    
    params = {
        "max_results": 100,
        "tweet.fields": "created_at,public_metrics",
        "expansions": "author_id"
    }
    
    all_tweets = []
    next_token = None
    
    print(f"Fetching tweets from @ghostxswings...")
    
    while True:
        if next_token:
            params['pagination_token'] = next_token
        
        try:
            resp = requests.get(tweets_url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if 'data' in data:
                all_tweets.extend(data['data'])
            
            if 'meta' in data and 'next_token' in data['meta']:
                next_token = data['meta']['next_token']
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tweets: {e}")
            break
    
    # Load existing tweets to check for duplicates
    archive_file = "memory/ghostxswings-tweets.jsonl"
    existing_ids = set()
    
    if os.path.exists(archive_file):
        with open(archive_file, 'r') as f:
            for line in f:
                try:
                    tweet = json.loads(line)
                    existing_ids.add(tweet['id'])
                except:
                    pass
    
    # Filter out duplicates and add new ones
    new_tweets = [t for t in all_tweets if t['id'] not in existing_ids]
    
    # Append new tweets
    if new_tweets:
        os.makedirs('memory', exist_ok=True)
        with open(archive_file, 'a') as f:
            for tweet in new_tweets:
                tweet['archived_at'] = datetime.utcnow().isoformat()
                tweet['deleted'] = False
                f.write(json.dumps(tweet) + "\n")
    
    print(f"Appended {len(new_tweets)} new tweets to {archive_file}")
    print(f"Done! Added {len(new_tweets)} new tweets.")
    
    return len(new_tweets)

if __name__ == "__main__":
    fetch_ghostxswings_tweets()
