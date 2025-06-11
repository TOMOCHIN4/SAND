# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
このファイルは、このリポジトリでコードを扱う際のClaude Code (claude.ai/code)へのガイダンスを提供します。

## Project Overview / プロジェクト概要
This is an educational podcast creation system that generates conversational audio content about Japanese social studies (社会) for middle school entrance exam preparation. The system uses Google's Gemini API with Text-to-Speech capabilities to create dialogues between two characters: ゆうこ先生 (a tutor) and あおいちゃん (a 6th-grade student).

中学受験の社会科学習のための教育ポッドキャスト制作システムです。GoogleのGemini APIのText-to-Speech機能を使用して、ゆうこ先生（講師）とあおいちゃん（小学6年生）の2人のキャラクターによる対話形式の音声コンテンツを生成します。

## Key Commands and Workflows / 主要なコマンドとワークフロー

### Audio Generation / 音声生成
The project uses Gemini's TTS API. Example implementation can be found in:
プロジェクトはGeminiのTTS APIを使用します。実装例は以下にあります：
- Python: `音声化Doc/sample_python.txt`
- TypeScript: `音声化Doc/sample_typescript.txt`
- cURL: `音声化Doc/sample_curl.txt`

To generate audio / 音声生成の手順:
1. Create a dialogue prompt based on content from `資料/` folder / `資料/`フォルダの内容に基づいて対話プロンプトを作成
2. Use the system instruction template from `音声化Doc/system_instruction.txt` / `音声化Doc/system_instruction.txt`のシステム指示テンプレートを使用
3. Call Gemini API with multi-speaker configuration / マルチスピーカー設定でGemini APIを呼び出し
4. Save output as MP3 in `制作物/音源/` / 出力をMP3として`制作物/音源/`に保存
5. Save the used prompt in `制作物/プロンプト/` as markdown / 使用したプロンプトをマークダウンとして`制作物/プロンプト/`に保存

### Working with the Jupyter Notebook / Jupyter Notebookの使用
The main technical reference is `音声化Doc/Get_started_TTS.ipynb`. To use:
メインの技術リファレンスは`音声化Doc/Get_started_TTS.ipynb`です。使用方法：
```bash
jupyter notebook 音声化Doc/Get_started_TTS.ipynb
```

## Architecture and Workflow / アーキテクチャとワークフロー

### Content Pipeline / コンテンツパイプライン
1. **Source Material / 素材**: Educational content in `資料/` folder (geography and history textbooks) / `資料/`フォルダ内の教育コンテンツ（地理・歴史の教科書）
2. **Dialogue Generation / 対話生成**: Create conversations using the character templates / キャラクターテンプレートを使用して会話を作成
3. **Audio Production / 音声制作**: Convert to speech using Gemini TTS / Gemini TTSを使用して音声に変換
4. **Output Storage / 出力保存**: Save both audio files and prompts in `制作物/` / 音声ファイルとプロンプトの両方を`制作物/`に保存

### Character Profiles / キャラクタープロフィール
- **ゆうこ先生**: Gentle, intelligent tutor who explains concepts clearly / 優しく知的で、概念を分かりやすく説明する講師
- **あおいちゃん**: 6th-grade student who struggles with studying but is curious / 勉強が苦手だが好奇心旺盛な小学6年生

### API Configuration / API設定
- Model / モデル: `gemini-2.5-flash-preview-tts` or `gemini-2.5-pro-preview-tts`
- Output format / 出力形式: WAV (24kHz, 16-bit PCM) → Convert to MP3 / MP3に変換
- Multi-speaker mode with Japanese voices / 日本語音声によるマルチスピーカーモード

## Important Notes / 重要事項
- Wait for user instructions before creating audio content / 音声コンテンツを作成する前にユーザーの指示を待つ
- Always save both the generated audio and the prompt used / 生成された音声と使用したプロンプトの両方を必ず保存
- Do not overwrite existing files in `制作物/` - create new numbered files / `制作物/`内の既存ファイルを上書きしない - 新しい番号付きファイルを作成
- The API key is stored in `音声化Doc/gemini_api_key.txt` / APIキーは`音声化Doc/gemini_api_key.txt`に保存
- Use the character personalities defined in `system_instruction.txt` for consistent dialogue / 一貫した対話のために`system_instruction.txt`で定義されたキャラクター性を使用
- **CRITICAL: All proper nouns (especially person names) MUST be written in KATAKANA in the dialogue scripts** / **重要：すべての固有名詞（特に人名）は台本ではカタカナで表記する必要がある**
- **CRITICAL: When calculating character count for timing, count ONLY the actual dialogue text (both Speaker 1 and Speaker 2 lines), NOT headers, instructions, or formatting** / **重要：時間計算のための文字数カウントは、実際の対話テキスト（Speaker1とSpeaker2両方のセリフ）のみをカウントし、ヘッダーや指示文、フォーマットは除外する**