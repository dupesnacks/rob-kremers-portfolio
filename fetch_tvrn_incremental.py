#!/usr/bin/env python3
"""
Incremental fetch of @tvRN20 tweets.
Only fetches tweets newer than the last archived timestamp.
Runs daily via cron.
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Load bearer token
env_file = Path.home() / "clawd" / ".env.local"
bearer_token = None
with open(env_file) as f:
    for line in f:
        if line.startswith("X_BEARER_TOKEN="):
            bearer_token = line.split("=", 1)[1].strip()
            break

if not bearer_token:
    print("Error: X_BEARER_TOKEN not found")
    exit(1)

headers = {"Authorization": f"Bearer {bearer_token}"}
base_url = "https://api.twitter.com/2"

def get_user_id(username):
    """Get user ID from username."""
    url = f"{base_url}/users/by/username/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching user: {response.text}")
        exit(1)
    return response.json()["data"]["id"]

def get_today_start():
    """Get today's start time in UTC (ISO 8601 format)."""
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return today.isoformat().replace('+00:00', 'Z')

def fetch_new_tweets(user_id, start_time=None):
    """Fetch tweets newer than start_time."""
    url = f"{base_url}/users/{user_id}/tweets"
    
    params = {
        "max_results": 100,
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,created_at",
    }
    
    if start_time:
        # Fetch only tweets after the last one we have
        params["start_time"] = start_time
    
    all_tweets = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        
        if "data" not in data or len(data["data"]) == 0:
            break
        
        all_tweets.extend(data["data"])
        
        if "meta" not in data or "next_token" not in data["meta"]:
            break
        
        params["pagination_token"] = data["meta"]["next_token"]
    
    return all_tweets

def append_tweets(tweets, filepath):
    """Append new tweets to JSONL file."""
    if not tweets:
        print("No new tweets to archive.")
        return 0
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "a") as f:
        for tweet in tweets:
            entry = {
                "id": tweet["id"],
                "text": tweet["text"],
                "created_at": tweet["created_at"],
                "public_metrics": tweet.get("public_metrics", {}),
                "archived_at": datetime.utcnow().isoformat(),
                "deleted": False,
            }
            f.write(json.dumps(entry) + "\n")
    
    print(f"Appended {len(tweets)} new tweets to {filepath}")
    return len(tweets)

if __name__ == "__main__":
    tweets_file = Path.home() / "clawd" / "memory" / "tvrn-tweets.jsonl"
    
    # Only fetch today's tweets
    today_start = get_today_start()
    print(f"Fetching tweets from today (UTC): {today_start}")
    
    user_id = get_user_id("tvRN20")
    print(f"Fetching new tweets for user {user_id}...")
    
    new_tweets = fetch_new_tweets(user_id, start_time=today_start)
    count = append_tweets(new_tweets, tweets_file)
    
    print(f"Done! Added {count} new tweets.")
