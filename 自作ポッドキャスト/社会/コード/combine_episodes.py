#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wave
import struct
import os

def read_wav_header(filename):
    """WAVファイルのヘッダー情報を読み取る"""
    with wave.open(filename, 'rb') as wav:
        return {
            'nchannels': wav.getnchannels(),
            'sampwidth': wav.getsampwidth(),
            'framerate': wav.getframerate(),
            'nframes': wav.getnframes()
        }

def combine_wav_files(input_files, output_file, silence_duration=1.0):
    """
    複数のWAVファイルを結合する
    
    Args:
        input_files: 結合するWAVファイルのリスト
        output_file: 出力ファイル名
        silence_duration: ファイル間の無音時間（秒）
    """
    if not input_files:
        print("結合するファイルがありません。")
        return
    
    # 最初のファイルのパラメータを基準にする
    first_file = input_files[0]
    if not os.path.exists(first_file):
        print(f"ファイルが見つかりません: {first_file}")
        return
    
    header_info = read_wav_header(first_file)
    nchannels = header_info['nchannels']
    sampwidth = header_info['sampwidth']
    framerate = header_info['framerate']
    
    print(f"音声形式: {nchannels}ch, {sampwidth*8}bit, {framerate}Hz")
    
    # 無音データを作成（1秒間）
    silence_frames = int(framerate * silence_duration)
    silence_data = b'\x00' * (silence_frames * nchannels * sampwidth)
    
    # 出力ファイルを開く
    with wave.open(output_file, 'wb') as output_wav:
        output_wav.setnchannels(nchannels)
        output_wav.setsampwidth(sampwidth)
        output_wav.setframerate(framerate)
        
        total_duration = 0
        
        for i, input_file in enumerate(input_files):
            if not os.path.exists(input_file):
                print(f"ファイルが見つかりません: {input_file}")
                continue
            
            print(f"結合中: {os.path.basename(input_file)}")
            
            # ファイルを読み込んで出力に書き込み
            with wave.open(input_file, 'rb') as input_wav:
                # パラメータの確認
                if (input_wav.getnchannels() != nchannels or
                    input_wav.getsampwidth() != sampwidth or
                    input_wav.getframerate() != framerate):
                    print(f"警告: {input_file} の音声形式が異なります")
                    continue
                
                # 音声データをコピー
                frames = input_wav.readframes(input_wav.getnframes())
                output_wav.writeframes(frames)
                
                duration = input_wav.getnframes() / framerate
                total_duration += duration
                print(f"  時間: {duration:.1f}秒")
            
            # 最後のファイル以外には無音を追加
            if i < len(input_files) - 1:
                output_wav.writeframes(silence_data)
                total_duration += silence_duration
                print(f"  無音追加: {silence_duration}秒")
        
        print(f"\n結合完了!")
        print(f"出力ファイル: {output_file}")
        print(f"総時間: {total_duration:.1f}秒 ({total_duration/60:.1f}分)")

def main():
    # 結合するファイルのリスト（順番に注意）
    base_path = "/mnt/c/Users/tomo2/OneDrive/あおいお勉強/自作ポッドキャスト/社会/制作物/音源/"
    
    input_files = [
        base_path + "15_大正デモクラシーと護憲運動_3分版_0.wav",
        base_path + "16_第一次世界大戦と日本の発展_3分版_0.wav", 
        base_path + "17_社会運動の高まりと関東大震災_3分版_0.wav",
        base_path + "18_昭和恐慌と軍部の台頭_3分版_0.wav",
        base_path + "19_日中戦争から太平洋戦争へ_3分版_0.wav"
    ]
    
    output_file = base_path + "20_大正から戦争への道_長編_15分版_0.wav"
    
    print("大正から戦争への道 - 長編ポッドキャスト作成")
    print("=" * 50)
    
    # ファイルの存在確認
    missing_files = []
    for file in input_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("以下のファイルが見つかりません:")
        for file in missing_files:
            print(f"  - {os.path.basename(file)}")
        return
    
    # 結合実行
    combine_wav_files(input_files, output_file, silence_duration=1.5)

if __name__ == "__main__":
    main()