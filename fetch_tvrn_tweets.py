#!/usr/bin/env python3
"""
Fetch all available tweets from @tvRN20 and archive them.
Uses X API v2 with pagination to collect as much historical data as possible.
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Load bearer token
env_file = Path.home() / "clawd" / ".env.local"
if not env_file.exists():
    print(f"Error: {env_file} not found")
    exit(1)

bearer_token = None
with open(env_file) as f:
    for line in f:
        if line.startswith("X_BEARER_TOKEN="):
            bearer_token = line.split("=", 1)[1].strip()
            break

if not bearer_token:
    print("Error: X_BEARER_TOKEN not found in .env.local")
    exit(1)

# X API setup
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

def fetch_all_tweets(user_id):
    """Fetch all available tweets from user with pagination."""
    url = f"{base_url}/users/{user_id}/tweets"
    
    params = {
        "max_results": 100,  # Max per request
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,created_at",
    }
    
    all_tweets = []
    pagination_token = None
    request_count = 0
    
    while True:
        if pagination_token:
            params["pagination_token"] = pagination_token
        
        response = requests.get(url, headers=headers, params=params)
        request_count += 1
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        
        if "data" not in data or len(data["data"]) == 0:
            print(f"No more tweets. Total requests: {request_count}")
            break
        
        tweets = data["data"]
        all_tweets.extend(tweets)
        
        print(f"Request {request_count}: Fetched {len(tweets)} tweets (total: {len(all_tweets)})")
        
        # Check for next page
        if "meta" in data and "next_token" in data["meta"]:
            pagination_token = data["meta"]["next_token"]
        else:
            print(f"No next_token. Final count: {len(all_tweets)} tweets")
            break
    
    return all_tweets

def save_tweets(tweets, filepath):
    """Save tweets to JSONL file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w") as f:
        for tweet in tweets:
            # Enrich with archival metadata
            entry = {
                "id": tweet["id"],
                "text": tweet["text"],
                "created_at": tweet["created_at"],
                "public_metrics": tweet.get("public_metrics", {}),
                "archived_at": datetime.utcnow().isoformat(),
                "deleted": False,
            }
            f.write(json.dumps(entry) + "\n")
    
    print(f"Saved {len(tweets)} tweets to {filepath}")

if __name__ == "__main__":
    print("Fetching @tvRN20 tweets...")
    
    user_id = get_user_id("tvRN20")
    print(f"User ID: {user_id}")
    
    tweets = fetch_all_tweets(user_id)
    
    filepath = Path.home() / "clawd" / "memory" / "tvrn-tweets.jsonl"
    save_tweets(tweets, filepath)
    
    print(f"\nDone! Archive: {filepath}")
