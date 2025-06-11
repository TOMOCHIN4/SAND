# 開発進捗記録

## 完了済みタスク

### 2025-01-06
1. ✅ **プロジェクト初期設定**
   - GitHubリポジトリ設定 (https://github.com/TOMOCHIN4/SAND.git)
   - Git構造の最適化
   - Hugging Face Spacesへのデプロイ環境構築

2. ✅ **デプロイシステム構築**
   - `deploy_to_hf.py` 自動デプロイスクリプト作成
   - DEPLOY.md ドキュメント作成
   - 手動デプロイ方式の確立（Claude Code経由）

3. ✅ **デフォルト設定の最適化**
   - Speaker1: ゆうこママ (Gacrux - 落ち着いた大人の女性)
   - Speaker2: あおたろちゃん (Leda - 明るい子どもの声)
   - 音声リストの教育向け最適化

## 今後の作業予定

### 次回セッション（未実装）
1. **長さ設定の変更**
   - スライダーを「1～30分」から「1～300秒」に変更
   - より細かい時間制御を可能に

2. **スタイル選択肢の拡張**
   - 現在: "ニュース解説", "対談風", "ストーリーテリング"
   - 追加予定: 教育向けスタイルの充実

3. **スタイル別台本生成の改善**
   - スタイルに応じたプロンプトテンプレートの実装
   - より自然で効果的な対話生成

## 現在の状態

### ファイル構成
```
SAND/
├── app.py                 # メインアプリ (Gradio 5.33.0)
├── app_config.py          # 設定ファイル
├── deploy_to_hf.py        # HF Spacesデプロイスクリプト
├── requirements.txt       # 依存関係
└── 各種ドキュメント
```

### デプロイ状況
- **GitHub**: https://github.com/TOMOCHIN4/SAND.git (最新)
- **Hugging Face**: https://huggingface.co/spaces/tomo2chin2/SAND (最新)

### 技術スタック
- Gradio 5.33.0
- Google Gemini 2.5 Pro (Text & TTS)
- Python 3.10+

## 再開時の手順

1. `TodoRead` でタスク一覧確認
2. `git status` で現在の状態確認
3. 次のタスクから順次実装
4. テスト → コミット → デプロイの流れで進行

## 注意事項

- HF_TOKEN.txt は機密情報のため取り扱い注意
- デプロイ時は `python deploy_to_hf.py [TOKEN]` を使用
- GitHubはバージョン管理専用、HF Spacesへのデプロイはローカルから実行