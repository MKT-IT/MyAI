"""
X (Twitter) 自動投稿ツール
RSSフィードからAI/テック系ニュースを取得し、Claudeで投稿文を生成してXに投稿する
"""

import sys
import os
import argparse

# Windowsコンソールの文字化け対策
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import feedparser
import tweepy
import anthropic
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# RSSフィードのURL一覧
RSS_FEEDS = [
    "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
    "https://feeds.feedburner.com/TheHackersNews",
]


def get_latest_news() -> dict | None:
    """
    RSSフィードから最新のニュースを1件取得する

    Returns:
        dict: ニュース情報（title, link, summary）またはNone
    """
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                entry = feed.entries[0]
                return {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "")[:500],  # 長すぎる場合は切り詰め
                }
        except Exception as e:
            print(f"RSSフィード取得エラー ({feed_url}): {e}")
            continue
    return None


def generate_tweet(news: dict) -> str:
    """
    Anthropic API (Claude) を使って投稿文を生成する

    Args:
        news: ニュース情報

    Returns:
        str: 生成された投稿文
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""あなたはコンサルファームのAI部門マネージャーです。
以下のニュースについて、X（Twitter）に投稿するコメントを作成してください。

【ニュースタイトル】
{news['title']}

【概要】
{news['summary']}

【URL】
{news['link']}

【条件】
- 投稿文は280文字以内（URLを含む）
- コンサルファームのAI部門マネージャーの視点でコメント
- 敬語は使わない（「です」「ます」禁止）
- でも物腰やわらかく穏やかな口調で（「〜だね」「〜かも」「〜だなぁ」など）
- フレンドリーで落ち着いた雰囲気
- ハッシュタグを2〜3個つける（例：#AI活用 #ビジネスAI #テック）
- URLは必ず投稿文の最後に含める

投稿文のみを出力してください。"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def post_to_x(tweet_text: str) -> bool:
    """
    X (Twitter) に投稿する（API v2使用）

    Args:
        tweet_text: 投稿するテキスト

    Returns:
        bool: 投稿成功ならTrue
    """
    try:
        client = tweepy.Client(
            consumer_key=os.getenv("X_API_KEY"),
            consumer_secret=os.getenv("X_API_SECRET"),
            access_token=os.getenv("X_ACCESS_TOKEN"),
            access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
        )

        response = client.create_tweet(text=tweet_text)
        print(f"投稿成功！ Tweet ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"投稿エラー: {e}")
        return False


def main(auto_mode: bool = False):
    """メイン処理"""
    print("=" * 50)
    print("X 自動投稿ツール")
    print("=" * 50)

    # 1. RSSフィードからニュースを取得
    print("\n[1/3] RSSフィードからニュースを取得中...")
    news = get_latest_news()
    if not news:
        print("ニュースを取得できませんでした。")
        return

    print(f"取得したニュース: {news['title']}")

    # 2. Claudeで投稿文を生成
    print("\n[2/3] 投稿文を生成中...")
    tweet_text = generate_tweet(news)
    print(f"\n--- 生成された投稿文 ---\n{tweet_text}")
    print(f"--- 文字数: {len(tweet_text)} ---\n")

    # 3. 投稿
    if auto_mode:
        # 自動モード：確認なしで投稿
        print("[3/3] Xに投稿中...")
        post_to_x(tweet_text)
    else:
        # 手動モード：確認してから投稿
        confirm = input("この内容で投稿しますか？ (y/N): ")
        if confirm.lower() == "y":
            print("\n[3/3] Xに投稿中...")
            post_to_x(tweet_text)
        else:
            print("投稿をキャンセルしました。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="X 自動投稿ツール")
    parser.add_argument("--auto", action="store_true", help="確認なしで自動投稿")
    args = parser.parse_args()
    main(auto_mode=args.auto)
