#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gemini 2.5 Pro Preview (text) × Gemini 2.5 Pro Preview-TTS (multi-speaker)
ポッドキャスト自動生成アプリ  –  Gradio 5.33.0

公式ドキュメント:
https://ai.google.dev/gemini-api/docs/guides/tts
"""

import io
import os
import pathlib
import re
import tempfile
import uuid
import wave
from typing import List, Tuple

import gradio as gr
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# 1) API キー  ―  HF Space では Settings → Secrets に GOOGLE_API_KEY を登録
# ---------------------------------------------------------------------------
if pathlib.Path(".env").exists():              # ローカル開発時のみ
    from dotenv import load_dotenv
    load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "環境変数 GOOGLE_API_KEY がありません。\n"
        "・本番 (HF Space): Settings → Secrets に登録\n"
        "・ローカル        : .env に GOOGLE_API_KEY=... を記載"
    )

client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------------------------
# 2) モデル ID & 定数
# ---------------------------------------------------------------------------
TEXT_MODEL_ID = "gemini-2.5-pro-preview-06-05"
TTS_MODEL_ID  = "gemini-2.5-pro-preview-tts"
SAMPLE_RATE   = 24_000                               # 公式推奨: 24 kHz / 16-bit / Mono

VOICE_OPTIONS = [
    # 公式 30+ から抜粋（教育向け優先）
    "Gacrux", "Leda", "Autonoe", "Callirrhoe", "Kore",
    "Zephyr", "Puck", "Umbriel", "Fenrir", "Enceladus",
]

# ---------------------------------------------------------------------------
# 3) PCM → WAV(bytes)
# ---------------------------------------------------------------------------
def pcm_to_wav_bytes(pcm: bytes) -> bytes:
    """PCM (s16le / 24 kHz / Mono) → WAV bytes"""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)                 # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
    return buf.getvalue()

# ---------------------------------------------------------------------------
# 4) 台本生成
# ---------------------------------------------------------------------------
SCRIPT_TEMPLATE = """\
あなたは熟練のポッドキャスト脚本家です。
以下の制約に**厳密**に従い、日本語の台本を作成してください。
---
* 話者は 2 名: {spk1} と {spk2}
* 各行は「<話者名>: <セリフ>」形式
* 行頭の話者名は必ず {spk1} または {spk2}
* 構成: 冒頭あいさつ → 本編 → まとめ
* 長さ: 約 {minutes} 分
* トーン: {style}
---
テーマ: {topic}
台本を開始してください。
"""

def make_script(topic: str,
                minutes: int,
                style: str,
                spk1: str,
                spk2: str) -> str:
    prompt = SCRIPT_TEMPLATE.format(
        topic=topic, minutes=minutes, style=style, spk1=spk1, spk2=spk2
    )
    resp = client.models.generate_content(
        model=TEXT_MODEL_ID,
        contents=prompt,
    )
    return resp.text.strip()

# ---------------------------------------------------------------------------
# 5) スクリプト検証
# ---------------------------------------------------------------------------
def sanitize_script(script: str, spk1: str, spk2: str) -> str:
    """誤フォーマット行を除去し、TTS で確実に解釈できる形に整える"""
    valid: List[str] = []
    pat = re.compile(rf"^({re.escape(spk1)}|{re.escape(spk2)})\s*:\s+.+")
    for ln in script.splitlines():
        ln = ln.strip()
        if pat.match(ln):
            valid.append(ln)
    return "\n".join(valid)

# ---------------------------------------------------------------------------
# 6) ポッドキャスト生成  –  戻り値は (script, filepath)
# ---------------------------------------------------------------------------
def generate_podcast(topic: str,
                     minutes: int,
                     style: str,
                     spk1_name: str,
                     spk1_voice: str,
                     spk2_name: str,
                     spk2_voice: str) -> Tuple[str, str]:

    # 6-1  台本
    raw_script = make_script(topic, minutes, style, spk1_name, spk2_name)
    script = sanitize_script(raw_script, spk1_name, spk2_name)

    # 6-2  マルチスピーカー TTS
    resp = client.models.generate_content(
        model=TTS_MODEL_ID,
        contents=script,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker=spk1_name,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=spk1_voice
                                )
                            ),
                        ),
                        types.SpeakerVoiceConfig(
                            speaker=spk2_name,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=spk2_voice
                                )
                            ),
                        ),
                    ]
                )
            ),
        ),
    )
    pcm = resp.candidates[0].content.parts[0].inline_data.data
    wav_bytes = pcm_to_wav_bytes(pcm)

    # ---- WAV を一時ファイルへ ----
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, f"{uuid.uuid4().hex}.wav")
    with open(file_path, "wb") as f:
        f.write(wav_bytes)

    return script, file_path

# ---------------------------------------------------------------------------
# 7) Gradio UI
# ---------------------------------------------------------------------------
with gr.Blocks(title="Gemini マルチスピーカー Podcast Generator") as demo:
    gr.Markdown("## 🎙️ Gemini 2.5 Pro + TTS で 2 人対話ポッドキャストを自動生成")

    topic_in   = gr.Textbox(label="テーマ", placeholder="例: 生成 AI の未来動向")
    minutes_in = gr.Slider(1, 30, value=5, step=1, label="長さ (分)")
    style_in   = gr.Dropdown(["ニュース解説", "対談風", "ストーリーテリング"],
                             value="対談風", label="スタイル")

    with gr.Row():
        spk1_name_in  = gr.Textbox(label="話者 1 名", value="ゆうこママ")
        spk1_voice_in = gr.Dropdown(VOICE_OPTIONS, value="Gacrux", label="話者 1 ボイス")
    with gr.Row():
        spk2_name_in  = gr.Textbox(label="話者 2 名", value="あおたろちゃん")
        spk2_voice_in = gr.Dropdown(VOICE_OPTIONS, value="Leda", label="話者 2 ボイス")

    gen_btn     = gr.Button("生成")
    script_out  = gr.Textbox(lines=22, label="生成された台本", show_copy_button=True)
    audio_out   = gr.Audio(label="Podcast (WAV)", type="filepath")   # ← filepath

    gen_btn.click(
        fn=generate_podcast,
        inputs=[topic_in, minutes_in, style_in,
                spk1_name_in, spk1_voice_in,
                spk2_name_in, spk2_voice_in],
        outputs=[script_out, audio_out],
    )

# ---------------------------------------------------------------------------
# 8) エントリポイント
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo.launch()
