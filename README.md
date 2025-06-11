# SAND - AI教育ポッドキャスト生成システム

中学受験対策を中心とした教育コンテンツと、AIによるポッドキャスト自動生成システムです。

## 🎯 主な機能

- **教育ポッドキャスト生成**: 理科・社会・国語・算数の学習コンテンツを音声化
- **エンターテインメント系コンテンツ**: サンドウィッチマン風の対話型コメディ生成
- **マルチスピーカー対話**: Google Gemini TTSを使用した自然な会話音声
- **Gradio Webアプリ**: Hugging Face Spacesでの簡単なデプロイ

## 🚀 Hugging Face Spacesでの使用

### デプロイ方法

1. [Hugging Face](https://huggingface.co/)でアカウントを作成
2. 新しいSpaceを作成（SDK: Gradio）
3. このリポジトリのコードをアップロード
4. Settings → Repository secretsで`GOOGLE_API_KEY`を設定

### 必要な環境変数

- `GOOGLE_API_KEY`: [Google AI Studio](https://aistudio.google.com/)から取得

## 💻 ローカル開発

```bash
# リポジトリのクローン
git clone https://github.com/TOMOCHIN4/SAND.git
cd SAND

# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r ベースとなるコード/requirements.txt

# 環境変数の設定
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# アプリの起動
python ベースとなるコード/app.py
```

## 📁 プロジェクト構造

```
SAND/
├── ベースとなるコード/      # Gradioアプリケーション
│   ├── app.py              # メインアプリ
│   ├── requirements.txt    # 依存関係
│   └── README.md          # HF Spaces用README
├── 教材資料/               # 学習教材（マークダウン形式）
├── 自作ポッドキャスト/      # 音声生成スクリプト群
└── CLAUDE.md              # 開発ガイドライン
```

## 🛠️ 技術スタック

- **Frontend**: Gradio 5.33.0
- **AI Models**: Google Gemini 2.5 Pro (Text & TTS)
- **Audio**: WAV形式（24kHz, 16-bit, Mono）
- **Deployment**: Hugging Face Spaces

## 📝 ライセンス

MIT License