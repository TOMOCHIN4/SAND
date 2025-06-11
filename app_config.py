"""
アプリケーション設定ファイル
環境変数や定数の管理を一元化
"""

import os
from typing import List

# API設定
API_KEY = os.getenv("GOOGLE_API_KEY")

# モデル設定
TEXT_MODEL_ID = "gemini-2.5-pro-preview-06-05"
TTS_MODEL_ID = "gemini-2.5-pro-preview-tts"

# 音声設定
SAMPLE_RATE = 24_000  # 24kHz
AUDIO_CHANNELS = 1    # モノラル
SAMPLE_WIDTH = 2      # 16-bit

# 利用可能な音声リスト（教育用に最適化）
EDUCATIONAL_VOICES = [
    "Gacrux",     # 先生役に最適（落ち着いた大人の女性）
    "Leda",       # 子供役に最適（明るい子どもの声）
    "Autonoe",    # 先生役の代替
    "Callirrhoe", # 子供役の代替
    "Kore",       # ナレーター向き
]

# コメディ用音声リスト
COMEDY_VOICES = [
    "Fenrir",     # 力強い男性（ツッコミ向き）
    "Umbriel",    # 落ち着いた男性（ボケ向き）
    "Enceladus",  # エネルギッシュな男性
    "Charon",     # 低音の男性
    "Sadachbia",  # 個性的な声
]

# 全音声リスト
ALL_VOICES = [
    "Zephyr", "Puck", "Kore", "Umbriel", "Fenrir",
    "Enceladus", "Charon", "Iapetus", "Leda", "Sadachbia",
    "Autonoe", "Callirrhoe", "Ceto", "Echo", "Electra",
    "Elara", "Hermione", "Himalia", "Ida", "Io",
    "Larissa", "Lyra", "Metis", "Mira", "Naiad",
    "Oberon", "Ophelia", "Pandora", "Proteus", "Setebos",
    "Gacrux",  # 追加：落ち着いた大人の女性
]

# スタイル設定
EDUCATIONAL_STYLES = ["対話形式", "解説形式", "クイズ形式", "物語形式"]
COMEDY_STYLES = ["漫才", "コント", "大喜利", "フリートーク"]

# デフォルト設定
DEFAULT_DURATION = 5  # 分
DEFAULT_STYLE = "対話形式"
DEFAULT_TEACHER_NAME = "ゆうこママ"
DEFAULT_STUDENT_NAME = "あおたろちゃん"
DEFAULT_TEACHER_VOICE = "Gacrux"  # 落ち着いた大人の女性
DEFAULT_STUDENT_VOICE = "Leda"    # 明るい子どもの声