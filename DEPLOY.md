# Hugging Face Spacesへのデプロイ手順

このドキュメントは、Claude Codeがアプリケーションを Hugging Face Spaces にデプロイする際の手順を記載しています。

## 前提条件

1. Hugging Face アカウントの作成
2. Hugging Face APIトークンの取得（Settings → Access Tokens）
3. 新しいSpaceの作成（https://huggingface.co/new-space）

## デプロイ方法

### 自動デプロイ（推奨）

Claude Codeが以下のコマンドを実行します：

```bash
# 環境変数の設定（初回のみ）
export HF_USERNAME="your_username"
export HF_TOKEN="your_hf_token"

# デプロイ実行
python deploy_to_hf.py
```

### 手動デプロイ

1. Hugging Face Spacesのリポジトリをクローン：
```bash
git clone https://huggingface.co/spaces/USERNAME/SPACE_NAME
cd SPACE_NAME
```

2. 必要なファイルをコピー：
```bash
cp /path/to/app.py .
cp /path/to/app_config.py .
cp /path/to/requirements.txt .
```

3. Hugging Face用のREADME.mdを作成（YAMLヘッダー付き）

4. コミットしてプッシュ：
```bash
git add .
git commit -m "Update application"
git push
```

## デプロイ後の設定

1. Space の Settings → Repository secrets で `GOOGLE_API_KEY` を設定
2. Space が正常に起動することを確認

## トラブルシューティング

- **ビルドエラー**: requirements.txt の依存関係を確認
- **起動エラー**: ログを確認して環境変数が正しく設定されているか確認
- **APIエラー**: GOOGLE_API_KEY が正しく設定されているか確認

## 注意事項

- GitHubはバージョン管理専用で、自動デプロイは行いません
- デプロイはClaude Codeがローカルから実行します
- HF_TOKENはデプロイ時のみ使用し、アプリケーション内では使用しません