import apps
from model import ask_gpt4v
from audio_recognize import audio_recognize
if input("按下回车键开始录音") == "":
    task_desc = audio_recognize()
    print(task_desc,'kc task_desc')
    # 选择app
    str_apps = str(apps)
    print(str_apps,'kc str_apps')
    choose_app_prompt = "There are apps on the phone: "+str_apps+", and the user's command is"+task_desc+". Please choose one or more apps that can be used for the task. If it is an app, give me the app name and start command using json format. For example, <launch app>{'app_name': '滴滴', 'start_command': 'com.sdu.didi.psnger/com.didi.sdk.app.launch.splash.SplashActivity'}. If it is multiple apps, return a question that describe the name and function of the alternative app starting with<app choose question>to help users choose the desired app."
    print(choose_app_prompt,'kc choose_app_prompt')
    app=ask_gpt4v(choose_app_prompt)
    if "error" not in app:
        if "<app choose question>" in app:
            print("app choose question")
            print(app)
        else:
            print(app)

