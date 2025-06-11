#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光の世界大探険20分長編ポッドキャスト生成スクリプト
5セクションを個別生成して結合します
"""

import os
import re
import struct
import base64
import mimetypes
from pathlib import Path
from google import genai
from google.genai import types

# 設定
API_KEY_PATH = "../共通リソース/音声化Doc/gemini_api_key.txt"
SYSTEM_INSTRUCTION_PATH = "音声化Doc/system_instruction.txt"
SCRIPT_PATH = "制作物/台本/光の世界大探険_20分完全版.md"
OUTPUT_DIR = "制作物/音源"

# 音声設定
MODEL = "gemini-2.5-pro-preview-tts"
TEMPERATURE = 0.9
VOICE_1 = "autonoe"  # ゆうこ先生
VOICE_2 = "callirrhoe"  # あおいちゃん

def load_api_key():
    """APIキーを読み込み"""
    try:
        with open(API_KEY_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"APIキーファイルが見つかりません: {API_KEY_PATH}")
        return None

def load_system_instruction():
    """システム指示を読み込み"""
    try:
        with open(SYSTEM_INSTRUCTION_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"システム指示ファイルが見つかりません: {SYSTEM_INSTRUCTION_PATH}")
        return None

def parse_audio_mime_type(mime_type: str) -> dict:
    """MIMEタイプから音声パラメータを抽出"""
    parts = mime_type.split(';')
    parameters = {"bits_per_sample": 16, "rate": 24000}  # デフォルト値
    
    for part in parts[1:]:
        if '=' in part:
            key, value = part.strip().split('=')
            if key == "rate":
                parameters["rate"] = int(value)
            elif key == "bits":
                parameters["bits_per_sample"] = int(value)
    
    return parameters

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """音声データをWAV形式に変換"""
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    # WAVヘッダーを作成
    wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', chunk_size, b'WAVE', b'fmt ', 16,
        1, num_channels, sample_rate, byte_rate,
        block_align, bits_per_sample, b'data', data_size
    )
    
    return wav_header + audio_data

def extract_sections(script_content):
    """スクリプトからセクションを抽出"""
    sections = []
    section_pattern = r'<!-- セクション(\d+)開始.*?-->(.*?)<!-- セクション\d+終了 -->'
    matches = re.findall(section_pattern, script_content, re.DOTALL)
    
    for section_num, content in matches:
        sections.append({
            'number': int(section_num),
            'content': content.strip()
        })
    
    return sections

def count_dialogue_characters(content):
    """対話部分の文字数をカウント"""
    speaker_pattern = r'\*\*Speaker[12]\*\*:\s*(.*?)(?=\*\*Speaker[12]\*\*:|$)'
    matches = re.findall(speaker_pattern, content, re.DOTALL)
    total_chars = sum(len(match.strip()) for match in matches)
    return total_chars

def generate_section_audio(section, system_instruction, client):
    """セクションの音声を生成"""
    section_num = section['number']
    content = section['content']
    
    print(f"\n=== セクション{section_num}の音声生成開始 ===")
    
    # 文字数確認
    char_count = count_dialogue_characters(content)
    print(f"対話文字数: {char_count}文字")
    
    # プロンプト構築
    prompt = f"""以下の理科教育ポッドキャストの台本を、2人のキャラクターで自然な対話として音声化してください。

{system_instruction}

【台本】
{content}

重要な指示:
- Speaker1はゆうこ先生（金沢弁、落ち着いた話し方）
- Speaker2はあおいちゃん（関西弁、元気で好奇心旺盛）
- 固有名詞は必ずカタカナ表記の通り発音
- 実験の安全性を重視した説明
- 自然な間と抑揚をつけて対話"""

    try:
        # 音声生成
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE,
                system_instruction=system_instruction,
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=VOICE_1
                        )
                    )
                )
            )
        )
        
        if response.candidates and response.candidates[0].content.parts:
            audio_part = response.candidates[0].content.parts[0]
            if hasattr(audio_part, 'inline_data'):
                audio_data = base64.b64decode(audio_part.inline_data.data)
                mime_type = audio_part.inline_data.mime_type
                
                # WAV形式に変換
                wav_data = convert_to_wav(audio_data, mime_type)
                
                # ファイル保存
                filename = f"section_{section_num}_light_exploration.wav"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(wav_data)
                
                print(f"セクション{section_num}音声生成完了: {filepath}")
                return filepath
            else:
                print(f"セクション{section_num}: 音声データが見つかりません")
                return None
        else:
            print(f"セクション{section_num}: 応答の生成に失敗しました")
            return None
            
    except Exception as e:
        print(f"セクション{section_num}の音声生成エラー: {str(e)}")
        return None

def combine_audio_files(section_files, output_filename):
    """音声ファイルを結合"""
    print(f"\n=== 音声ファイル結合開始 ===")
    
    try:
        import wave
        
        # 結合後のファイルパス
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with wave.open(output_path, 'wb') as output_wav:
            first_file = True
            
            for section_file in section_files:
                if section_file and os.path.exists(section_file):
                    print(f"結合中: {os.path.basename(section_file)}")
                    
                    with wave.open(section_file, 'rb') as input_wav:
                        if first_file:
                            # 最初のファイルのパラメータを設定
                            output_wav.setparams(input_wav.getparams())
                            first_file = False
                        
                        # 音声データをコピー
                        frames = input_wav.readframes(input_wav.getnframes())
                        output_wav.writeframes(frames)
                        
                        # セクション間に短い無音を挿入（0.5秒）
                        silence_frames = int(input_wav.getframerate() * 0.5)
                        silence_data = b'\x00' * (silence_frames * input_wav.getsampwidth())
                        output_wav.writeframes(silence_data)
                else:
                    print(f"警告: ファイルが見つかりません: {section_file}")
        
        print(f"20分長編音声結合完了: {output_path}")
        return output_path
        
    except ImportError:
        print("音声結合にはwave libraryが必要です。個別ファイルをご利用ください。")
        return None
    except Exception as e:
        print(f"音声結合エラー: {str(e)}")
        return None

def main():
    print("光の世界大探険20分長編ポッドキャスト生成開始")
    
    # APIキー読み込み
    api_key = load_api_key()
    if not api_key:
        return
    
    # システム指示読み込み
    system_instruction = load_system_instruction()
    if not system_instruction:
        return
    
    # Gemini APIクライアント初期化
    client = genai.Client(api_key=api_key)
    
    # スクリプト読み込み
    try:
        with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except FileNotFoundError:
        print(f"台本ファイルが見つかりません: {SCRIPT_PATH}")
        return
    
    # セクション抽出
    sections = extract_sections(script_content)
    if not sections:
        print("セクションが見つかりません。台本を確認してください。")
        return
    
    print(f"検出されたセクション数: {len(sections)}")
    
    # 各セクションの音声生成
    section_files = []
    for section in sections:
        audio_file = generate_section_audio(section, system_instruction, client)
        section_files.append(audio_file)
    
    # 音声結合
    if all(section_files):
        combined_file = combine_audio_files(
            section_files, 
            "光の世界大探険_20分完全版_generated.wav"
        )
        
        if combined_file:
            print(f"\n🎉 20分長編ポッドキャスト生成完了!")
            print(f"📁 保存場所: {combined_file}")
            print(f"📊 生成されたセクション: {len(sections)}個")
        else:
            print("\n⚠️ 音声結合に失敗しましたが、個別セクションファイルは利用可能です。")
            for i, file in enumerate(section_files, 1):
                if file:
                    print(f"  セクション{i}: {file}")
    else:
        print("\n⚠️ 一部のセクションの生成に失敗しました。")
        for i, file in enumerate(section_files, 1):
            status = "✓" if file else "✗"
            print(f"  セクション{i}: {status}")

if __name__ == "__main__":
    main()