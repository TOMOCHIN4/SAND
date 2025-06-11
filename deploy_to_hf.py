#!/usr/bin/env python
"""
Hugging Face Spacesへの手動デプロイスクリプト
Claude Codeがローカルから実行します
"""

import os
import subprocess
import shutil
from pathlib import Path

def deploy_to_huggingface(space_name="SAND", username=None, token=None):
    """
    Hugging Face Spacesにアプリをデプロイ
    
    Args:
        space_name: Space名
        username: Hugging Faceユーザー名
        token: Hugging Face APIトークン
    """
    # 環境変数から取得
    if not username:
        username = os.getenv("HF_USERNAME")
    if not token:
        token = os.getenv("HF_TOKEN")
    
    if not username or not token:
        raise ValueError("HF_USERNAME と HF_TOKEN が必要です")
    
    # デプロイ用の一時ディレクトリ
    deploy_dir = Path("hf_deploy_temp")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    try:
        # 必要なファイルをコピー
        files_to_deploy = [
            "app.py",
            "app_config.py", 
            "requirements.txt",
            "README.md",
        ]
        
        for file in files_to_deploy:
            if Path(file).exists():
                shutil.copy(file, deploy_dir)
        
        # Hugging Face Spaces用のREADME.mdを作成
        hf_readme = f"""---
title: {space_name}
emoji: 🎙️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: mit
---

# {space_name} - AI教育ポッドキャスト生成システム

このアプリケーションは、Google Gemini APIを使用して教育コンテンツのポッドキャストを自動生成します。

## 使い方

1. テーマを入力
2. 長さとスタイルを選択
3. 話者の名前と音声を設定
4. 「生成」ボタンをクリック

## 必要な設定

Settings → Repository secretsに以下を設定してください：
- `GOOGLE_API_KEY`: Google AI StudioのAPIキー
"""
        
        with open(deploy_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(hf_readme)
        
        # Gitリポジトリを初期化してプッシュ
        os.chdir(deploy_dir)
        
        # リポジトリURL
        repo_url = f"https://{username}:{token}@huggingface.co/spaces/{username}/{space_name}"
        
        # Git操作
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Deploy to Hugging Face Spaces"], check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
        
        print(f"✅ デプロイ完了: https://huggingface.co/spaces/{username}/{space_name}")
        
    finally:
        # クリーンアップ
        os.chdir("..")
        if deploy_dir.exists():
            shutil.rmtree(deploy_dir)

if __name__ == "__main__":
    # Claude Codeが実行時に適切な認証情報を設定します
    deploy_to_huggingface()