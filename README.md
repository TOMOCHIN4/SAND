# SAND - AI教育ポッドキャスト生成システム

中学受験対策を中心とした教育コンテンツと、AIによるポッドキャスト自動生成システムです。

## 🎯 主な機能

- **教育ポッドキャスト生成**: 理科・社会・国語・算数の学習コンテンツを音声化
- **エンターテインメント系コンテンツ**: サンドウィッチマン風の対話型コメディ生成
- **マルチスピーカー対話**: Google Gemini TTSを使用した自然な会話音声
- **Gradio Webアプリ**: Hugging Face Spacesでの簡単なデプロイ

## 🚀 クイックスタート

### Hugging Face Spacesで使用

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/YOUR_USERNAME/SAND)

### ローカル開発

```bash
# リポジトリのクローン
git clone https://github.com/TOMOCHIN4/SAND.git
cd SAND

# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# アプリの起動
python app.py
```

## 📁 プロジェクト構造

```
SAND/
├── app.py                 # メインアプリケーション
├── app_config.py          # 設定ファイル
├── requirements.txt       # 依存関係
├── README.md             # このファイル
├── CHANGELOG.md          # 変更履歴
├── 教材資料/              # 学習教材（マークダウン形式）
│   ├── 全般/             # 汎用教材
│   ├── 理科/             # 理科専用
│   └── 社会/             # 社会専用
└── 自作ポッドキャスト/     # 音声生成スクリプト群
    ├── 共通リソース/      # APIキー、ドキュメント
    ├── サンドウィッチマン風/ # コメディコンテンツ
    ├── 理科/             # 理科ポッドキャスト
    ├── 社会/             # 社会ポッドキャスト
    ├── 算数/             # 算数ポッドキャスト
    └── 国語/             # 国語ポッドキャスト
```

## 🛠️ 開発

### ブランチ戦略

- `main`: 本番環境
- `develop`: 開発ブランチ
- `feature/*`: 機能開発用ブランチ

### 環境変数

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `GOOGLE_API_KEY` | Google AI StudioのAPIキー | ✅ |

### APIキーの取得

1. [Google AI Studio](https://aistudio.google.com/)にアクセス
2. 「Get API key」をクリック
3. 新しいAPIキーを作成

## 🎨 カスタマイズ

### 音声の追加

`app_config.py`の`ALL_VOICES`リストに新しい音声を追加：

```python
ALL_VOICES = [
    # 既存の音声...
    "新しい音声名",
]
```

### スタイルの追加

`app_config.py`でスタイルをカスタマイズ：

```python
EDUCATIONAL_STYLES = ["対話形式", "解説形式", "新しいスタイル"]
```

## 📝 ライセンス

MIT License

## 🤝 貢献

プルリクエスト歓迎です！大きな変更の場合は、まずissueを作成して変更内容を議論してください。

## 📞 サポート

- Issues: [GitHub Issues](https://github.com/TOMOCHIN4/SAND/issues)
- Discussions: [GitHub Discussions](https://github.com/TOMOCHIN4/SAND/discussions)