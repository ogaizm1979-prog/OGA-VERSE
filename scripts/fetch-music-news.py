#!/usr/bin/env python3
"""
朝8時ニュース取得スクリプト
4つのRSSフィードから音楽ニュースを取得してJSONで保存
"""

import feedparser
import json
from datetime import datetime
import os
from pathlib import Path

# 出力ディレクトリ
OUTPUT_DIR = Path("/Volumes/8TB_USB/OGA-VERSE/news")
OUTPUT_DIR.mkdir(exist_ok=True)

# RSSフィード設定
FEEDS = {
    "音楽ナタリー": "https://natalie.mu/music/feed/news",
    "Musicman": "https://www.musicman.co.jp/feed",
    "Billboard": "https://www.billboard.com/feed/biz/",
    "Rolling Stone": "https://www.rollingstone.com/music/feed/",
}

def fetch_feeds():
    """RSSフィードを取得して記事をまとめる"""
    all_articles = []

    for source_name, feed_url in FEEDS.items():
        try:
            print(f"Fetching {source_name}...", flush=True)
            feed = feedparser.parse(feed_url)

            # 最新10件を取得
            for entry in feed.entries[:10]:
                article = {
                    "source": source_name,
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", "#"),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "")[:200],  # 最初の200文字
                }
                all_articles.append(article)

        except Exception as e:
            print(f"Error fetching {source_name}: {e}", flush=True)

    return all_articles

def save_json(articles):
    """記事をJSONファイルとして保存"""
    output_file = OUTPUT_DIR / "news.json"

    data = {
        "updated": datetime.now().isoformat(),
        "articles": articles,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(articles)} articles to {output_file}", flush=True)

if __name__ == "__main__":
    articles = fetch_feeds()
    save_json(articles)
    print("Done!", flush=True)
