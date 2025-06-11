---
title: podcastジェネレーター
emoji: 🥪
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: mit
---

# 🥪 サンドウィッチマン風漫才ジェネレーター

サンドウィッチマンの伊達さんと富澤さんの漫才をAIで再現するアプリです。

## 機能
- Gemini 2.5 Flashでサンドウィッチマン風漫才台本を自動生成
- Gemini TTS Proでマルチスピーカー音声を生成
- 伊達さん（ツッコミ）と富澤さん（ボケ）の特徴を再現

## 使い方
1. 漫才のテーマを入力
2. 「漫才を生成する」ボタンをクリック
3. 台本と音声が自動生成されます

## 必要な環境変数
- `GEMINI_API_KEY`: Google AI Studio から取得したAPIキー