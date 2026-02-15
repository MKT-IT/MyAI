# X (Twitter) 自動投稿ツール

RSSフィードからAI/テック系ニュースを取得し、Claude AIで投稿文を生成してXに自動投稿するツール。

## 機能

- RSSフィードから最新ニュースを取得
- Claude (Anthropic API) で「コンサルファームのAI部門マネージャー」視点のコメントを生成
- X (Twitter) API v2で投稿

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成：

```bash
cp .env.example .env
```

`.env` ファイルを編集してAPIキーを設定：

```
# X (Twitter) API credentials
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_TOKEN_SECRET=your_access_token_secret_here

# Anthropic API key
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. APIキーの取得方法

#### X (Twitter) API
1. [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard) にアクセス
2. プロジェクト/アプリを作成
3. 「Keys and tokens」から以下を取得：
   - API Key and Secret
   - Access Token and Secret
4. アプリの権限を「Read and Write」に設定

#### Anthropic API
1. [Anthropic Console](https://console.anthropic.com/) にアクセス
2. APIキーを生成

## 使い方

```bash
python main.py
```

実行すると：
1. RSSフィードから最新ニュースを取得
2. Claude AIで投稿文を生成
3. 投稿内容を確認後、`y` を入力で投稿

## RSSフィード

デフォルトで以下のフィードを監視：
- ITmedia AI+ (`https://rss.itmedia.co.jp/rss/2.0/aiplus.xml`)
- The Hacker News (`https://feeds.feedburner.com/TheHackersNews`)

`main.py` の `RSS_FEEDS` を編集してカスタマイズ可能。

## ファイル構成

```
x-auto-post/
├── main.py           # メインスクリプト
├── .env              # APIキー設定（Git管理外）
├── .env.example      # 環境変数のテンプレート
├── .gitignore        # Git除外設定
├── requirements.txt  # 依存パッケージ
└── README.md         # このファイル
```
