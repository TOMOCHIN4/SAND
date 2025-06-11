#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pydub import AudioSegment

def convert_wav_to_mp3():
    """WAVファイルをMP3に変換"""
    
    # 制作物/音源フォルダ内のWAVファイルを検索
    audio_dir = "制作物/音源"
    
    for filename in os.listdir(audio_dir):
        if filename.endswith(".wav"):
            wav_path = os.path.join(audio_dir, filename)
            mp3_path = os.path.join(audio_dir, filename.replace(".wav", ".mp3"))
            
            try:
                print(f"変換中: {filename}")
                # WAVファイルを読み込み
                audio = AudioSegment.from_wav(wav_path)
                
                # MP3として書き出し
                audio.export(mp3_path, format="mp3", bitrate="128k")
                print(f"変換完了: {mp3_path}")
                
                # 元のWAVファイルを削除（オプション）
                # os.remove(wav_path)
                # print(f"元ファイル削除: {wav_path}")
                
            except Exception as e:
                print(f"エラー: {filename} の変換に失敗しました - {e}")

if __name__ == "__main__":
    convert_wav_to_mp3()
    print("すべての変換が完了しました。")