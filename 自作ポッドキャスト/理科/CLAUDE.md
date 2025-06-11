# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 理科ポッドキャスト制作プロジェクト

## プロジェクト概要
このプロジェクトは、Google Gemini APIのText-to-Speech機能を使用して、理科の個別指導ポッドキャストを制作するためのものです。

ゆうこ先生（40代金沢弁女性）とあおいちゃん（11歳関西弁女児）の対話形式で、実験・観察を重視した理科学習コンテンツを作成します。

## キャラクター設定
- **ゆうこ先生**: 理科が得意な40代女性教師、金沢弁、実験好き
- **あおいちゃん**: 好奇心旺盛な11歳女児、関西弁、実験大好き

## 重要なファイル
- `音声化Doc/system_instruction.txt` - 理科指導用キャラクター設定
- `generate_podcast.py` - 音声生成メインスクリプト
- `プロンプトテンプレート_理科版.md` - 理科用プロンプトテンプレート
- `プロンプトテンプレート_理科_5分版.md` - 5分版理科テンプレート

## アーキテクチャ

### 音声生成パイプライン
- **入力**: Markdownプロンプト → **処理**: Gemini TTS API → **出力**: WAV音声
- **マルチスピーカー**: 2キャラクター対話（ゆうこ先生・あおいちゃん）
- **音声品質**: 16bit WAV, サンプリングレート可変
- **制御パラメータ**: voice model, temperature, duration, streaming

### 依存関係
```bash
# 必須パッケージのインストール
pip install -r requirements.txt
```
- google-genai>=1.19.0 (Gemini API)
- pydub (音声処理)

### API設定
- Google AI Studio APIキー: `音声化Doc/gemini_api_key.txt`
- システム指示: `音声化Doc/system_instruction.txt`

## 主なコマンド

### 音声生成
```bash
# 基本的な理科ポッドキャスト生成
python generate_podcast.py --prompt "制作物/プロンプト/[ファイル名].md"

# 5分版の生成
python generate_podcast.py --prompt "prompt.md" --duration 5

# 音声モデル指定（推奨設定）
python generate_podcast.py --prompt "prompt.md" --voice1 autonoe --voice2 callirrhoe
```

### プロジェクト管理
```bash
# 新規理科プロジェクトの作成
python setup_podcast_project.py ./新規理科プロジェクト

# 利用可能な音声モデル確認
python generate_podcast.py --list-voices

# デバッグとテスト
python generate_podcast.py --help  # 全オプション確認
python generate_podcast.py --prompt "test.md" --dry-run  # 音声生成なしテスト
```

## 理科指導の特徴
1. **実験重視**: 体験を通じた学習
2. **身近な例**: 日常生活の科学現象を活用
3. **疑問解決**: 「なぜ？」を大切にした対話
4. **安全第一**: 実験の注意事項も適切に説明

## 対象分野
- 植物・動物の特徴と分類
- 地球と宇宙（月・太陽・星座）
- 物質の性質と変化
- 力の働きと運動
- 電気と磁石
- 光と音の性質

## プロンプト作成時の注意
- 実験手順は段階的に説明
- 安全注意事項を必ず含める
- 科学用語は正確だが年齢に配慮
- カタカナ表記で読み方を明示
- 身近な例での理解促進を重視

## 推奨音声設定
- **モデル**: gemini-2.5-flash-preview-tts（通常）
- **温度**: 0.9（自然な会話）
- **先生の声**: autonoe（落ち着いた40代女性）
- **生徒の声**: leda（最高音・11歳女児に最適）

## 時間管理
- **10分版**: 標準的な詳細説明
- **5分版**: 簡潔で要点を絞った内容
- **3分版**: 基本概念のみの短縮版

## ファイル構成
```
理科/
├── 音声化Doc/          # API設定・キャラクター設定
├── 資料/              # 理科教材・参考資料
├── 制作物/
│   ├── 台本/          # 対話スクリプト（新規追加のみ、上書き禁止）
│   └── 音源/          # 生成音声（WAV形式、新規追加のみ、上書き禁止）
└── [各種設定ファイル]
```

## ファイル管理ルール
- **制作物フォルダ内（台本・音源）**: 新規ファイルとして追加のみ。既存ファイルの上書き禁止
- **その他のファイル**: 必要に応じて更新・統合してファイル数を抑制
- **テンプレート類**: 統合して重複を削減
- **設定ファイル**: 常に最新の状態に更新

## よく使うコマンド例
```bash
# 植物の光合成について5分で説明
python generate_podcast.py --prompt "制作物/台本/光合成実験.md" --duration 5

# 電気の性質について詳細説明
python generate_podcast.py --prompt "制作物/台本/電気の実験.md" --duration 10

# 音声品質を最高に（Pro版使用、時間はかかる）
python generate_podcast.py --prompt "制作物/台本/[テーマ].md" --model gemini-2.5-pro-preview-tts --duration 5

# 現在の推奨設定（最適化済み）
python generate_podcast.py --prompt "制作物/台本/[テーマ].md" --model gemini-2.5-pro-preview-tts --duration 5
```

## 安定生成のポイント
- **台本の対話部分**: 5分版で1,800-2,200文字必須
- **音声設定**: autonoe（先生）+ leda（生徒・最高音）
- **品質管理**: 音声生成ベストプラクティス.md を参照
- **ファイル構成**: 制作物/台本/ に新規追加、制作物/音源/ に出力