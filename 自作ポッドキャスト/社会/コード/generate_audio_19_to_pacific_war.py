#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import mimetypes
import os
import struct
from google import genai
from google.genai import types

def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to: {file_name}")

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data and parameters."""
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string."""
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}

def generate_to_pacific_war():
    # APIキーを読み込み
    with open("/mnt/c/Users/tomo2/OneDrive/あおいお勉強/自作ポッドキャスト/社会/音声化Doc/gemini_api_key.txt", "r") as f:
        api_key = f.read().strip()
    
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash-preview-tts"
    
    # システム指示を読み込み
    with open("/mnt/c/Users/tomo2/OneDrive/あおいお勉強/自作ポッドキャスト/社会/音声化Doc/system_instruction.txt", "r", encoding="utf-8") as f:
        system_instruction = f.read()
    
    # 対話内容を読み込み
    with open("/mnt/c/Users/tomo2/OneDrive/あおいお勉強/自作ポッドキャスト/社会/制作物/プロンプト/19_日中戦争から太平洋戦争へ_3分版.md", "r", encoding="utf-8") as f:
        prompt_content = f.read()
        # 対話部分を抽出
        start_marker = "Speaker 1（ゆうこ先生）: こんにちは"
        end_marker = "ありがとうございました！"
        start_index = prompt_content.find(start_marker)
        end_index = prompt_content.find(end_marker) + len(end_marker)
        dialogue_text = prompt_content[start_index:end_index]

    prompt = f"""
{system_instruction}

上記のキャラクター設定と状況設定に基づいて、以下の歴史の個別指導の対話を自然な音声で読み上げてください。

【重要な話し方の指示 - 3分版用】
■ゆうこ先生（40代金沢弁女性）：
- やや速めのテンポで、テキパキと話してください
- 明瞭で聞き取りやすく、親しみやすいトーンで話してください
- 重要な歴史用語や年号の前後での間は最小限に
- 説明は簡潔に、要点を絞って話してください
- 優しく包み込むような話し方で、安心感を与えてください

■あおいちゃん（11歳関西弁女児）：
- できるだけ高い音程で、子供らしい高い声で話してください
- 元気で明るく、テンポよく話してください
- リアクションは短く、的確に
- 驚いたり感動したりする場面では、感情を豊かに表現してください
- 少し早口気味で、子供らしい躍動感のある話し方をしてください

今日のテーマは「日中戦争から太平洋戦争へ」（3分版）です。

{dialogue_text}
"""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=0.9,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 1",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="autonoe"  # 40代女性の声
                            )
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 2",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="callirrhoe"   # 高い音程の声
                            )
                        ),
                    ),
                ]
            ),
        ),
    )

    print("日中戦争から太平洋戦争へ（3分版）音声生成を開始します...")
    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"/mnt/c/Users/tomo2/OneDrive/あおいお勉強/自作ポッドキャスト/社会/制作物/音源/19_日中戦争から太平洋戦争へ_3分版_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer)
        else:
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text)

if __name__ == "__main__":
    generate_to_pacific_war()