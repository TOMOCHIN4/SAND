# AI教育ポッドキャストプロジェクト - 社会科（歴史）

このプロジェクトは、Google Gemini APIのText-to-Speech機能を使用して、教育ポッドキャストとエンターテインメントポッドキャストを作成します。

## 🎭 2つのプロジェクト

### 1. ゆうこ先生とあおいちゃんの教育ポッドキャスト
中学受験対策の社会科（歴史・地理）を楽しく学べる対話形式の教育コンテンツ

### 2. サンドウィッチマン風お笑いポッドキャスト
人気芸人サンドウィッチマンのようなボケとツッコミの漫才形式エンターテインメント

## 🎯 プロジェクトの特徴

### 教育ポッドキャスト
- 40代金沢弁女性教師 × 11歳関西弁女児の自然な対話
- 中学受験レベルの歴史学習コンテンツ
- 高品質な音声合成（Gemini 2.5 TTS使用）
- 再現可能な制作フロー

### サンドウィッチマン風ポッドキャスト
- 富澤（ボケ）と伊達（ツッコミ）の掛け合い
- 聞き間違いや勘違いから生まれる笑い
- 「ちょっと何言ってるか分からない」の決め台詞
- テンポの良いリズミカルな漫才

## 📁 ディレクトリ構造
```
社会/
├── 音声化Doc/
│   ├── gemini_api_key.txt          # APIキー（要設定）
│   ├── system_instruction.txt      # キャラクター設定
│   ├── Get_started_TTS.ipynb       # Gemini TTS技術資料
│   └── sample_*.txt                # コード例
├── 資料/
│   └── *.md                        # 中学受験教材（歴史・地理）
├── 制作物/
│   ├── プロンプト/
│   │   ├── 01_明治維新と憲法発布.md
│   │   ├── 02_日清日露戦争と条約改正.md
│   │   ├── 03_明治維新と憲法発布_方言版.md
│   │   └── 04_日清日露戦争と条約改正_方言版.md
│   └── 音源/
│       ├── 13_明治維新と憲法発布_Callirrhoe版_0.wav
│       └── 14_日清日露戦争と条約改正_Callirrhoe版_0.wav
├── サンドウィッチマン風/
│   ├── テンプレート/
│   │   ├── キャラクター設定.md
│   │   └── プロンプトテンプレート.md
│   ├── 制作物/
│   │   ├── プロンプト/
│   │   └── 音源/
│   └── generate_sandwich_audio.py  # サンドウィッチマン風音声生成
├── generate_podcast.py             # 教育ポッドキャスト音声生成
├── setup_podcast_project.py        # プロジェクトセットアップ
├── requirements.txt                # 依存パッケージ
└── ポッドキャスト作成マニュアル.md    # 詳細マニュアル
```

## 🚀 クイックスタート

### 1. セットアップ
```bash
# 依存関係のインストール
pip install -r requirements.txt

# APIキーの設定（Google AI Studioで取得）
echo "YOUR_API_KEY" > 音声化Doc/gemini_api_key.txt
```

### 2. 新規プロジェクトの作成
```bash
# 他のジャンル用に新規プロジェクトを作成
python setup_podcast_project.py ./新規プロジェクト名
```

### 3. 音声生成

#### 教育ポッドキャスト
```bash
# 基本的な使用方法
python generate_podcast.py --prompt "制作物/プロンプト/03_明治維新と憲法発布_方言版.md"

# 音声モデルを指定
python generate_podcast.py --prompt "prompt.md" --voice1 autonoe --voice2 callirrhoe

# ヘルプを表示
python generate_podcast.py --help
```

#### サンドウィッチマン風ポッドキャスト
```bash
# カロリーゼロ理論のネタを生成
python サンドウィッチマン風/generate_sandwich_audio.py

# スクリプト内でテーマを変更して別のネタを生成可能
```

## 🎙️ 推奨設定

### 音声モデル
- **ゆうこ先生**: `autonoe` (40代女性・落ち着いた声)
- **あおいちゃん**: `callirrhoe` (11歳女児・高音)

### キャラクター設定
- **ゆうこ先生**: 石川県金沢市出身、金沢弁、優しく知的
- **あおいちゃん**: 大阪北部出身、ソフトな関西弁、元気で好奇心旺盛

## 📝 制作フロー
1. `音声化Doc/system_instruction.txt` でキャラクター設定
2. `制作物/プロンプト/` に対話スクリプトを作成
3. `generate_podcast.py` で音声生成
4. `制作物/音源/` に音声ファイル保存

## 🔧 カスタマイズ

### 他教科への適用
- 数学: 問題解説形式
- 英語: 会話練習形式
- 理科: 実験解説形式

### 年齢層の変更
```python
# 幼児向け
--voice2 kore --temperature 0.7

# 中高生向け
--voice2 leda --temperature 0.8
```

## 📚 詳細情報
- 完全マニュアル: `ポッドキャスト作成マニュアル.md`
- プロンプトテンプレート: `プロンプトテンプレート（話し方詳細版）.md`
- 技術資料: `音声化Doc/Get_started_TTS.ipynb`

## ⚠️ 注意事項
- APIキーは公開しない
- 生成には時間がかかる場合がある（約2-5分/10分音声）
- Pro版は高品質だが処理時間が長い

## 🤝 貢献
改善案やバグ報告は歓迎します。新しい教科やキャラクターの追加も可能です。

---
Created with ❤️ using Google Gemini API