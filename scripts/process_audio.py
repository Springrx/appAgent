import pyaudio
import wave
import whisper
from model import ask_gpt4v
from gtts import gTTS
import os

def audio_recognize(refine:bool = True):
    # 设置音频参数
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "output.wav"
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
            # 通过 KeyboardInterrupt来结束录音
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        pass

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
    print('录音结果',result["text"])
    typo_prompt="You are a text editor tasked with aiding the elderly in China to navigate apps more efficiently. They might use colloquial Chinese phrases when utilizing the app's voice features, and transcription errors may occur during this process. Your role is to rectify these spoken phrases or spelling mistakes. Please ensure your response is in Simplified Chinese. The statement that needs your correction is"+result["text"]
    if (not refine):
        content = [{
            "type": "text",
            "text": typo_prompt
        },]
        rsp = ask_gpt4v(content)
        msg = "something error"
        if "error" not in rsp:
            msg = rsp["choices"][0]["message"]["content"]
        return msg
    # 将result过一层大模型，消除如“红桥火车站”这样的误差、纠正口语化的表达，比如“放歌”、“打亮”
    prompt = "You are a text proofreader who helps Chinese elderly people better express their needs for operating the app. Elderly people may input some colloquial expressions in Chinese during voice operation of the app, and spelling errors may also occur during voice transcription. Your function is to correct these colloquial expressions and spelling errors more accurately and formally, in order to facilitate subsequent analysis. For example, the oral expression of an elderly person is: turn on the flashlight, the formal expression is: turn on the flashlight switch; The phonetic transcription error is '去红桥火车站', and the correct expression is '去虹桥火车站'. There is a new oral expression now, please correct it. Remember, both input and output are in Chinese:" + result["text"]
    content = [
    {
        "type": "text",
        "text": prompt
    },]
    rsp = ask_gpt4v(content)
    msg = "something error"
    if "error" not in rsp:
        msg = rsp["choices"][0]["message"]["content"]
    return msg

def text_to_speech(text, lang='zh-CN'):
    # 初始化gTTS对象
    tts = gTTS(text=text, lang=lang)
    # 生成语音文件
    file_name = f"audios/calendar/{text}.wav"
    tts.save(file_name)
    print('kc ready')
    # 播放语音文件
    # os.system(f"afplay {file_name}")
    # 删除临时音频文件
    # os.remove(file_name)
