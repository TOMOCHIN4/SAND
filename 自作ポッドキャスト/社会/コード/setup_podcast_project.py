#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ポッドキャストプロジェクトセットアップスクリプト
新しいプロジェクトの初期設定を自動化します。
"""

import os
import sys
import shutil
from pathlib import Path

def create_directory_structure(base_path="."):
    """プロジェクトのディレクトリ構造を作成"""
    directories = [
        "音声化Doc",
        "資料", 
        "制作物/プロンプト",
        "制作物/音源"
    ]
    
    for directory in directories:
        dir_path = Path(base_path) / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"ディレクトリ作成: {dir_path}")

def create_system_instruction_template(base_path="."):
    """システム指示テンプレートを作成"""
    template = """# Gemini TTS用 二人会話生成システムプロンプト

# プロンプト全体の目的
prompt_description: |
  このプロンプトは、個別指導の先生と生徒の二人が繰り広げる、心温まる学習風景の会話を生成するための指示書です。
  AIは以下のキャラクター設定と状況設定を深く理解し、二人の人格や関係性が伝わるような、自然で感情豊かな対話を作成してください。

# 登場人物の設定
characters:
  - name: [先生の名前]
    role: 個別指導の先生
    details:
      personality: |
        [先生の性格・特徴を記述]
      speech_style: |
        [先生の話し方の特徴・方言などを記述]

  - name: [生徒の名前]
    role: 小学[X]年生の[男の子/女の子]
    details:
      personality: |
        [生徒の性格・特徴を記述]
      speech_style: |
        [生徒の話し方の特徴・方言などを記述]

# 会話の状況設定
context:
  setting: |
    [場所・時間帯などの設定]
  topic: |
    [学習内容・教科・単元など]
  relationship: |
    [二人の関係性]

# AIへの具体的な指示
instructions:
  task: |
    上記のキャラクター設定と状況設定に基づき、個別指導中の会話を生成してください。
  conversation_flow: |
    [会話の流れの指示]
  key_elements_to_include:
    - [含めるべき要素1]
    - [含めるべき要素2]
    - [含めるべき要素3]

##  output_format: |
    以下の形式で、二人のセリフを交互に出力してください。
---
<Style instructions>
Speaker 1: <speaker1 talking>
Speaker 2: <speaker2 talking>
"""
    
    file_path = Path(base_path) / "音声化Doc" / "system_instruction.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"テンプレート作成: {file_path}")

def create_prompt_template(base_path="."):
    """対話プロンプトテンプレートを作成"""
    template = """# [テーマ名]についての対話プロンプト

## 使用するシステムプロンプト
音声化Doc/system_instruction.txt の内容を使用し、以下の内容で会話を生成してください。

## 学習テーマ
[具体的な学習内容と目標]

## キャラクター設定
- [先生名]：[年齢][地域]出身、[方言]を使う[性格]な先生
- [生徒名]：[年齢][地域]出身、[方言]を話す[学年]

## 具体的な指示
以下の内容を含む、約10分程度の対話を生成してください：

---

<Style instructions>
Speaker 1（[先生名]）: [挨拶と導入]

Speaker 2（[生徒名]）: [反応]

[以下、対話を記述]

---

## 音声生成時の注意事項
- [先生名]：[話し方の詳細指示]
- [生徒名]：[話し方の詳細指示]
- 固有名詞はすべてカタカナ表記で正確な読み方を指定
- 会話のテンポは自然に、[生徒名]の理解度に合わせてゆっくりめに
- 方言の特徴を活かしつつ、教育内容は正確に伝える"""
    
    file_path = Path(base_path) / "制作物" / "プロンプト" / "00_テンプレート.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"テンプレート作成: {file_path}")

def create_readme(base_path="."):
    """READMEファイルを作成"""
    readme = """# AIポッドキャストプロジェクト

このプロジェクトはGoogle Gemini APIを使用して教育ポッドキャストを作成します。

## クイックスタート

1. APIキーの設定
   ```
   音声化Doc/gemini_api_key.txt にGemini APIキーを保存
   ```

2. 依存関係のインストール
   ```bash
   pip install -r requirements.txt
   ```

3. キャラクター設定
   `音声化Doc/system_instruction.txt` を編集

4. 対話スクリプトの作成
   `制作物/プロンプト/` にマークダウンファイルを作成

5. 音声生成
   ```bash
   python generate_podcast.py --prompt "制作物/プロンプト/01_テーマ.md"
   ```

## ディレクトリ構造
- `音声化Doc/` - システム設定とAPIキー
- `資料/` - 参考資料や教材
- `制作物/プロンプト/` - 対話スクリプト
- `制作物/音源/` - 生成された音声ファイル

## 詳細
`ポッドキャスト作成マニュアル.md` を参照してください。
"""
    
    file_path = Path(base_path) / "README.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"README作成: {file_path}")

def copy_essential_files(source_dir, base_path="."):
    """必要なファイルをコピー"""
    files_to_copy = [
        ("generate_podcast.py", "generate_podcast.py"),
        ("requirements.txt", "requirements.txt"),
        ("ポッドキャスト作成マニュアル.md", "ポッドキャスト作成マニュアル.md")
    ]
    
    for src_file, dst_file in files_to_copy:
        src_path = Path(source_dir) / src_file
        dst_path = Path(base_path) / dst_file
        
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"ファイルコピー: {src_file} -> {dst_path}")
        else:
            print(f"警告: ソースファイルが見つかりません: {src_path}")

def main():
    print("=== ポッドキャストプロジェクトセットアップ ===\n")
    
    # プロジェクトパスを取得
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = input("プロジェクトパスを入力してください（デフォルト: ./新規プロジェクト）: ").strip()
        if not project_path:
            project_path = "./新規プロジェクト"
    
    # 絶対パスに変換
    project_path = Path(project_path).resolve()
    
    # 確認
    print(f"\nプロジェクトを作成します: {project_path}")
    confirm = input("続行しますか？ (y/n): ").strip().lower()
    if confirm != 'y':
        print("キャンセルしました。")
        return
    
    # セットアップ実行
    print("\nセットアップを開始します...")
    
    # ディレクトリ構造を作成
    create_directory_structure(project_path)
    
    # テンプレートファイルを作成
    create_system_instruction_template(project_path)
    create_prompt_template(project_path)
    create_readme(project_path)
    
    # 必要なファイルをコピー（同じディレクトリから）
    current_dir = Path(__file__).parent
    copy_essential_files(current_dir, project_path)
    
    print("\n=== セットアップ完了 ===")
    print(f"\nプロジェクトが作成されました: {project_path}")
    print("\n次のステップ:")
    print("1. cd", project_path)
    print("2. 音声化Doc/gemini_api_key.txt にAPIキーを保存")
    print("3. 音声化Doc/system_instruction.txt でキャラクターを設定")
    print("4. pip install -r requirements.txt")
    print("5. python generate_podcast.py --help で使い方を確認")

if __name__ == "__main__":
    main()