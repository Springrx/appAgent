import pyaudio
import wave
import whisper
# msvcrt库是Windows特有的
import msvcrt
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
    try:
        while True:
            if msvcrt.kbhit():
                if msvcrt.getch() == b'0':
                    break
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        pass
    # while (input("按下0结束录音") != "0"):
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
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
    # 将result过一层大模型，消除如“红桥火车站”这样的误差、纠正口语化的表达，比如“放歌”、“打亮”
    prompt = "You are a text proofreader who helps Chinese elderly people better express their needs for operating the app. Elderly people may input some colloquial expressions in Chinese during voice operation of the app, and spelling errors may also occur during voice transcription. Your function is to correct these colloquial expressions and spelling errors more accurately and formally, in order to facilitate subsequent analysis. For example, the oral expression of an elderly person is: turn on the flashlight, the formal expression is: turn on the flashlight switch; The phonetic transcription error is '去红桥火车站', and the correct expression is '去虹桥火车站'. There is a new oral expression now, please correct it. Remember, both input and output are in Chinese:" + result["text"]
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
# while True:
#     if input("按下回车键开始录音") == "":
#         audio_recognize()