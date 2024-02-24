import pyaudio
import wave
import whisper
from model import ask_gpt4v

# 设置音频参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"
def audio_recognize():
    # 初始化PyAudio
    audio = pyaudio.PyAudio()

    # 打开音频流
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("录音开始...")

    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束...")

    # 关闭音频流
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 将录音数据保存为.wav文件
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    model = whisper.load_model("base")
    result = model.transcribe("output.wav")
    # 将result过一层大模型，消除如“红桥火车站”这样的误差
    prompt = "This sentence was generated using a phonetic transcription tool, so there may be typos inside, and there may be recognition errors for nouns such as geographical location. Modify the typos in this sentence based on possible errors: " + result["text"]
    content = [
    {
        "type": "text",
        "text": prompt
    },]
    rsp = ask_gpt4v(content)
    if "error" not in rsp:
        msg = rsp["choices"][0]["message"]["content"]
    return msg
    # print(result["text"])