#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用ポッドキャスト音声生成スクリプト
Google Gemini APIを使用して2人の対話形式の音声を生成します。
"""

import argparse
import base64
import mimetypes
import os
import struct
import sys
from pathlib import Path
from google import genai
from google.genai import types

# デフォルト設定
DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"
DEFAULT_TEMPERATURE = 0.9
DEFAULT_VOICE_1 = "autonoe"  # 大人の女性向け
DEFAULT_VOICE_2 = "leda"  # 子供向け最高音（11歳女児に最適）

# 利用可能な音声モデル
AVAILABLE_VOICES = [
    'achernar', 'achird', 'algenib', 'algieba', 'alnilam', 'aoede', 
    'autonoe', 'callirrhoe', 'charon', 'despina', 'enceladus', 'erinome', 
    'fenrir', 'gacrux', 'iapetus', 'kore', 'laomedeia', 'leda', 'orus', 
    'puck', 'pulcherrima', 'rasalgethi', 'sadachbia', 'sadaltager', 
    'schedar', 'sulafat', 'umbriel', 'vindemiatrix', 'zephyr', 'zubenelgenubi'
]

def save_binary_file(file_name, data):
    """バイナリファイルを保存"""
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"ファイル保存完了: {file_name}")

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """音声データにWAVヘッダーを追加"""
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
        chunk_size,       # ChunkSize
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size
        1,                # AudioFormat
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    """MIMEタイプから音声パラメータを解析"""
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

def load_api_key(api_key_path="音声化Doc/gemini_api_key.txt"):
    """APIキーを読み込み"""
    try:
        with open(api_key_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"エラー: APIキーファイルが見つかりません: {api_key_path}")
        print("Google AI StudioでAPIキーを取得し、上記ファイルに保存してください。")
        sys.exit(1)

def load_system_instruction(instruction_path="音声化Doc/system_instruction.txt"):
    """システム指示を読み込み"""
    try:
        with open(instruction_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"警告: システム指示ファイルが見つかりません: {instruction_path}")
        return ""

def load_dialogue_from_prompt(prompt_path):
    """プロンプトファイルから対話部分を抽出"""
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 対話部分を抽出（複数のパターンに対応）
        markers = [
            ("Speaker 1", "---"),
            ("<Style instructions>", "---"),
            ("## 具体的な指示", "## 音声生成時の注意事項")
        ]
        
        for start_marker, end_marker in markers:
            if start_marker in content and end_marker in content:
                start_idx = content.find(start_marker)
                end_idx = content.rfind(end_marker)
                if start_idx < end_idx:
                    return content[start_idx:end_idx].strip()
        
        # マーカーが見つからない場合は全体を返す
        print("警告: 対話マーカーが見つかりません。ファイル全体を使用します。")
        return content
            
    except FileNotFoundError:
        print(f"エラー: プロンプトファイルが見つかりません: {prompt_path}")
        sys.exit(1)

def generate_podcast(
    prompt_path,
    output_dir="制作物/音源/",
    model=DEFAULT_MODEL,
    temperature=DEFAULT_TEMPERATURE,
    voice1=DEFAULT_VOICE_1,
    voice2=DEFAULT_VOICE_2,
    api_key_path="音声化Doc/gemini_api_key.txt",
    instruction_path="音声化Doc/system_instruction.txt",
    additional_instructions="",
    target_duration=None
):
    """ポッドキャスト音声を生成"""
    
    # APIキーとシステム指示を読み込み
    api_key = load_api_key(api_key_path)
    system_instruction = load_system_instruction(instruction_path)
    
    # 対話内容を読み込み
    dialogue_text = load_dialogue_from_prompt(prompt_path)
    
    # クライアントを初期化
    client = genai.Client(api_key=api_key)
    
    # 時間指定があれば追加
    duration_instruction = ""
    if target_duration:
        duration_instruction = f"""
【重要：時間制限】
この音声は必ず{target_duration}分ちょうどに収まるように生成してください。
- 話すスピードを調整して、指定時間内に収める
- 間は最小限に、重要な箇所のみ短く入れる
- {target_duration}分±15秒の範囲内を目指す
"""
    
    # プロンプトを構築
    prompt = f"""
{system_instruction}

{duration_instruction}

{additional_instructions}

以下の対話を自然な音声で読み上げてください：

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
    
    # 音声設定
    generate_content_config = types.GenerateContentConfig(
        temperature=temperature,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 1",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice1
                            )
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 2",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice2
                            )
                        ),
                    ),
                ]
            ),
        ),
    )

    # 出力ファイル名を生成
    prompt_name = Path(prompt_path).stem
    output_filename = f"{prompt_name}_generated"
    
    print(f"音声生成を開始します...")
    print(f"モデル: {model}")
    print(f"Speaker 1: {voice1}")
    print(f"Speaker 2: {voice2}")
    
    # 音声生成
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
            os.makedirs(output_dir, exist_ok=True)
            file_name = os.path.join(output_dir, f"{output_filename}_{file_index}")
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

def main():
    parser = argparse.ArgumentParser(
        description="Google Gemini APIを使用してポッドキャスト音声を生成します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本的な使用方法
  python generate_podcast.py --prompt "制作物/プロンプト/01_テーマ.md"
  
  # 音声モデルを指定
  python generate_podcast.py --prompt "prompt.md" --voice1 aoede --voice2 leda
  
  # Pro版を使用（処理時間が長い）
  python generate_podcast.py --prompt "prompt.md" --model gemini-2.5-pro-preview-tts
  
利用可能な音声モデル:
  大人の女性: autonoe, aoede, enceladus
  子供・高音: leda（最高音）, callirrhoe, kore
  大人の男性: achird, algenib, fenrir
  若い男性: puck, orus, gacrux
        """
    )
    
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="対話プロンプトファイルのパス"
    )
    parser.add_argument(
        "--output", "-o",
        default="制作物/音源/",
        help="出力ディレクトリ（デフォルト: 制作物/音源/）"
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        choices=["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"],
        help=f"使用するモデル（デフォルト: {DEFAULT_MODEL}）"
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"生成の多様性（0.0-1.0、デフォルト: {DEFAULT_TEMPERATURE}）"
    )
    parser.add_argument(
        "--voice1", "-v1",
        default=DEFAULT_VOICE_1,
        choices=AVAILABLE_VOICES,
        help=f"Speaker 1の音声（デフォルト: {DEFAULT_VOICE_1}）"
    )
    parser.add_argument(
        "--voice2", "-v2",
        default=DEFAULT_VOICE_2,
        choices=AVAILABLE_VOICES,
        help=f"Speaker 2の音声（デフォルト: {DEFAULT_VOICE_2}・最高音）"
    )
    parser.add_argument(
        "--api-key-path",
        default="音声化Doc/gemini_api_key.txt",
        help="APIキーファイルのパス"
    )
    parser.add_argument(
        "--instruction-path",
        default="音声化Doc/system_instruction.txt",
        help="システム指示ファイルのパス"
    )
    parser.add_argument(
        "--additional-instructions", "-a",
        default="",
        help="追加の話し方指示"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="利用可能な音声モデルを表示"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        help="目標時間（分）。例: --duration 5 で5分の音声を生成"
    )
    
    args = parser.parse_args()
    
    if args.list_voices:
        print("利用可能な音声モデル:")
        for i, voice in enumerate(AVAILABLE_VOICES, 1):
            print(f"  {i:2d}. {voice}")
        sys.exit(0)
    
    # 音声生成を実行
    generate_podcast(
        prompt_path=args.prompt,
        output_dir=args.output,
        model=args.model,
        temperature=args.temperature,
        voice1=args.voice1,
        voice2=args.voice2,
        api_key_path=args.api_key_path,
        instruction_path=args.instruction_path,
        additional_instructions=args.additional_instructions,
        target_duration=args.duration
    )

if __name__ == "__main__":
    main()