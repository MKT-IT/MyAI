# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 基本ルール

1. オーナーとのやり取りは常に日本語で行うこと
2. 専門用語を使うときは中学生でもわかるように解説を添えること
3. ファイルを新しく作る際は、必ず目的を説明して許可を求めること
4. ユーザーのことは「オーナー」と呼ぶこと

## プロジェクト概要

個人用AIアシスタント開発プロジェクト。Webアプリケーションと開発補助ツールを含む。

## アーキテクチャ

### todo.html
スタンドアロンのToDoリストアプリ。単一HTMLファイルで完結（CSS/JS埋め込み）。
- データ永続化: localStorage使用
- フレームワーク: なし（Vanilla JS）
- ブラウザで直接開いて使用

## カスタムコマンド

### 日報
ユーザーが「日報」と言ったら、`/daily-report`スキルを実行する。
今日のセッションで行った作業内容をまとめて`Dairy_Report.txt`に追記保存する。

### ブログ記事生成
ユーザーが「ブログ記事」「記事作成」「Note記事」と言ったら、`/blog-article`スキルを実行する。
テーマを聞いて、読者の悩み→解決策→まとめの構成でプロ級記事を生成し、`article/`フォルダに保存する。

## Git運用

- リモート: git@github.com:MKT-IT/MyAI.git (SSH)
- メインブランチ: main
