#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
セクション1のみのテスト生成
"""

import os
import re
import struct
import base64
from google import genai
from google.genai import types

# 設定
API_KEY_PATH = "../共通リソース/音声化Doc/gemini_api_key.txt"
SYSTEM_INSTRUCTION_PATH = "音声化Doc/system_instruction.txt"
OUTPUT_DIR = "制作物/音源"

MODEL = "gemini-2.5-pro-preview-tts"
TEMPERATURE = 0.9
VOICE_1 = "autonoe"

# セクション1のテスト台本
TEST_SCRIPT = """
**Speaker1**: あおいちゃん、今日は光について一緒に勉強しようや。光って、普段当たり前に使っとるけど、実はとっても面白い性質があるがやちゃ。

**Speaker2**: ゆうこ先生、こんにちは！光の勉強、めっちゃ楽しみです！光って、懐中電灯から出てくるやつですよね？

**Speaker1**: そうそう、よく知っとるちゃ。まず、光の一番大切な性質から始めよう。光は必ず真っ直ぐ進むがや。これを「チョクシン」って言うんやちゃ。

**Speaker2**: チョクシン...真っ直ぐ進むんですね。でも、なんで影ができるんですか？

**Speaker1**: いい質問やちゃ！光が真っ直ぐ進むから、物があると光が遮られて、影ができるがよ。影は光が届かない暗いところながやちゃ。
"""

def load_api_key():
    with open(API_KEY_PATH, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_system_instruction():
    with open(SYSTEM_INSTRUCTION_PATH, 'r', encoding='utf-8') as f:
        return f.read().strip()

def parse_audio_mime_type(mime_type: str) -> dict:
    parts = mime_type.split(';')
    parameters = {"bits_per_sample": 16, "rate": 24000}
    
    for part in parts[1:]:
        if '=' in part:
            key, value = part.strip().split('=')
            if key == "rate":
                parameters["rate"] = int(value)
            elif key == "bits":
                parameters["bits_per_sample"] = int(value)
    
    return parameters

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    wav_header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', chunk_size, b'WAVE', b'fmt ', 16,
        1, num_channels, sample_rate, byte_rate,
        block_align, bits_per_sample, b'data', data_size
    )
    
    return wav_header + audio_data

def main():
    print("セクション1テスト生成開始")
    
    api_key = load_api_key()
    system_instruction = load_system_instruction()
    client = genai.Client(api_key=api_key)
    
    prompt = f"""以下の理科教育ポッドキャストの台本を、2人のキャラクターで自然な対話として音声化してください。

{system_instruction}

【台本】
{TEST_SCRIPT}

重要な指示:
- Speaker1はゆうこ先生（金沢弁、落ち着いた話し方）
- Speaker2はあおいちゃん（関西弁、元気で好奇心旺盛）
- 固有名詞は必ずカタカナ表記の通り発音
- 自然な間と抑揚をつけて対話"""

    try:
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
                
                wav_data = convert_to_wav(audio_data, mime_type)
                
                filename = "test_section_1_light.wav"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(wav_data)
                
                print(f"テスト音声生成完了: {filepath}")
            else:
                print("音声データが見つかりません")
        else:
            print("応答の生成に失敗しました")
            
    except Exception as e:
        print(f"音声生成エラー: {str(e)}")

if __name__ == "__main__":
    main()