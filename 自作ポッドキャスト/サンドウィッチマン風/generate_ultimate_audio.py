"""
究極版の音声のみを生成
"""

import pathlib
import base64
import struct
from google import genai
from google.genai import types

def load_api_key():
    """APIキーを読み込む"""
    api_key_path = pathlib.Path(__file__).parent.parent / "音声化Doc" / "gemini_api_key.txt"
    with open(api_key_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def parse_audio_mime_type(mime_type: str) -> dict:
    """音声MIMEタイプから詳細パラメータを解析"""
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

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """WAVファイルヘッダー生成"""
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
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1,
        num_channels, sample_rate, byte_rate, block_align,
        bits_per_sample, b"data", data_size
    )
    return header + audio_data

def main():
    client = genai.Client(api_key=load_api_key())
    
    # 究極版の対話（牛丼ネタ）
    dialogue_text = """
富澤: 明治維新ってさ、肉食解禁でしょ？
伊達: いや、まぁ、それも一つだけど…
富澤: 牛丼屋オープンラッシュだよね。
伊達: 違う違う、もっと色々あるよ。
富澤: 吉野家とか、すき家とか。
伊達: え？ それチェーン店だし、ずっと後だよ。
富澤: 松屋もできた頃じゃないの？
伊達: 違うよ！ 江戸時代は肉食制限あったけど…
富澤: クーポンとかあったのかな？
伊達: クーポン！？ なかったよ、そんなの！
富澤: ペッパーランチもできた頃？
伊達: 違う！ ペッパーランチ関係ない！
富澤: 肉食解禁で、いきなりステーキブーム？
伊達: 違うわ！ そもそもステーキって…
富澤: あ、肉といえば、伊達ちゃん、焼肉好きだよね。
伊達: いや、好きだけど、今は明治維新の話…
富澤: 牛角の食べ放題、よく行くでしょ？
伊達: 行くけど！ それ、明治維新と関係ない！
富澤: で、明治維新ってさ、肉だけじゃないよね。
伊達: そうだよ、やっと気づいた？ 政治体制とか…
富澤: ハンバーガーとか？
伊達: ハンバーガー！？ それ、もっと後！
富澤: マクドナルドの1号店とかできたんじゃないの？
伊達: 違う！ 1号店は戦後！ 何言ってんの！？
富澤: あ、でもさ、ゼロカロリー理論で考えれば…
伊達: ゼロカロリー理論！？ 関係ない！ もう！
富澤: 明治維新ってさ、結局、肉食解禁のおかげで…
伊達: はぁ…
富澤: 今、牛丼並盛380円とかで食べられるんだよね。
伊達: ちょっと何言ってるか分からない。
"""
    
    # マルチスピーカー形式に変換
    lines = dialogue_text.strip().split('\n')
    contents = []
    
    for line in lines:
        if line.strip():
            if line.startswith('富澤:'):
                text = line.replace('富澤:', '').strip()
                contents.append(f"Speaker 1: {text}")
            elif line.startswith('伊達:'):
                text = line.replace('伊達:', '').strip()
                contents.append(f"Speaker 2: {text}")
    
    # 最適化された音声設定
    generate_content_config = types.GenerateContentConfig(
        temperature=0.85,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 1",  # 富澤
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="puck"  # 明るく軽快、高めの男性声
                            )
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 2",  # 伊達
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="charon"  # 中低音域、倍音豊富
                            )
                        ),
                    ),
                ]
            ),
        ),
    )
    
    # 詳細な音声指示
    tts_prompt = f"""
以下のサンドウィッチマンの漫才を、音声特徴分析に基づいて完璧に再現してください。

【究極版音声特徴指示】

■Speaker 1（富澤たけし）:
- 声質: 明るく軽快、やや高めで金属質（3-4kHz成分強調）
- 話速: 基本4.5音節/秒、興奮時は8音節/秒まで上昇
- 破裂音: /p/, /t/ を通常より20%長く発音
- 語尾上昇: 文節末で音程を+15Hz上げる
- 感情: 常に自信満々で明るい（confusion=95, joy=70）
- 特徴的語尾: 「〜だよね」「〜じゃん」「〜でしょ？」は軽快に
- 間: 確認を求めるときに0.1秒のポーズ
- 勘違いに全く気づかない無邪気さを強調

■Speaker 2（伊達みきお）:
- 声質: 中低音域（150-250Hz）、喉頭の倍音豊富
- 話速: 冷静時4.5音節/秒→ツッコミ時5.2音節/秒
- 感情変化: 冷静(anger=0)→困惑(surprise=60)→激昂(anger=85)
- 語尾伸ばし: 「〜だよねぇ」は0.3秒延長
- ため息: 富澤の勘違い後に軽くため息
- 強調: 「違う！」「〜じゃねーよ！」は音量20%増加
- 決め台詞: 「ちょっと何言ってるか分からない」は0.8秒ポーズ後、完全に呆れた感じで
- 段階的な感情変化（冷静→困惑→イライラ→諦め）

【高度なタイミング制御】
- 全体テンポ: 通常会話の1.3倍の速度
- ツッコミ前: 0.2-0.3秒の絶妙な間
- 展開の区切り: 0.8秒以上の長い間を効果的に配置
- オチ前: 1.0秒の決定的な間

【演技の完全再現】
- 富澤: 勘違いが加速していく様子を音声で表現
- 伊達: 最初の余裕から最後の諦めまでの感情変化
- 両者: 本物のサンドウィッチマンの掛け合いリズム
- 自然な会話の流れと笑いのタイミング

この牛丼ネタは富澤の「肉食解禁→現代チェーン店」という壮大な勘違いと、
伊達の段階的困惑が見どころです。

{chr(10).join(contents)}
"""
    
    print("究極版音声生成中...（牛丼ネタ）")
    print("音声特徴完全再現処理中 - 最大7分かかります")
    
    audio_chunks = []
    
    try:
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-pro-preview-tts",
            contents=tts_prompt,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
                
            if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                data_buffer = inline_data.data
                
                if isinstance(data_buffer, str):
                    data_buffer = base64.b64decode(data_buffer)
                
                audio_chunks.append(data_buffer)
                print("●", end="", flush=True)
            else:
                if hasattr(chunk, 'text') and chunk.text:
                    print(f"\nText: {chunk.text}")
        
        print()
        
        if audio_chunks:
            audio_data = b''.join(audio_chunks)
            audio_data = convert_to_wav(audio_data, "audio/L16;rate=24000")
            
            output_path = pathlib.Path(__file__).parent / "制作物" / "音源" / "サンドウィッチマン_明治維新_究極版.wav"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            file_size = len(audio_data) / (1024 * 1024)
            print(f"🎉 究極版音声ファイルを保存: {output_path}")
            print(f"ファイルサイズ: {file_size:.1f}MB")
            print("音声特徴完全再現版が完成しました！")
        else:
            raise Exception("音声データが生成されませんでした")
            
    except Exception as e:
        print(f"エラー: {e}")
        raise

if __name__ == "__main__":
    main()