from pdfminer.high_level import extract_text
import pypdfium2 as pdfium
import requests
import json
import pyaudio
import wave


def vvox_test(text):
    # エンジン起動時に表示されているIP、portを指定
    host = "127.0.0.1"
    port = 50021

    # 音声化する文言と話者を指定(3で標準ずんだもんになる)
    params = (
        ('text', text),
        ('speaker', 3),
    )

    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )

    print("クエリ作成 完了")

    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers={"Content-Type": "application/json"},
        params=params,
        data=json.dumps(query.json())
    )

    print("音声合成 完了")

    return synthesis

# # 再生処理
    # voice = synthesis.content
    # pya = pyaudio.PyAudio()
    #
    # # サンプリングレートが24000以外だとずんだもんが高音になったり低音になったりする
    # stream = pya.open(format=pyaudio.paInt16,
    #                   channels=1,
    #                   rate=24000,
    #                   output=True)
    #
    # stream.write(voice)
    # stream.stop_stream()
    # stream.close()
    # pya.terminate()


if __name__ == "__main__":
    pdf = pdfium.PdfDocument("page_5.pdf")

    total_pages = len(pdf)
    print(f"全{total_pages}ページ 処理開始")

    for i in range(total_pages):
        text_page = pdf[i].get_textpage()
        text = text_page.get_text_bounded()
        voice_data = vvox_test(text)

        # データをファイルとして出力
        output_file = f"pdf_to_speech_{i+1:03}.wav"
        with wave.open(output_file, "w") as wf:
            wf.setnchannels(2)  # チャンネル数の設定 (1:mono, 2:stereo)
            wf.setsampwidth(2)  # サンプル幅の設定 (2bytes = 16bit)
            wf.setframerate(12000)  # サンプリングレートの設定
            wf.writeframes(voice_data.content)  # ステレオデータを書き込み
            print(f"{i+1}/{total_pages}ページが完了")

