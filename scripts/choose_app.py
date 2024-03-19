from apps import apps
from model import ask_gpt4v
import re
import json

# from audio_recognize import audio_recognize
def choose_app(task_desc):
    # task_desc = "和我说一下滴滴的出租车怎么打"
    # 选择app
    str_apps = str(apps)
    print(str_apps, "kc str_apps")
    choose_app_prompt = (
        "There are apps on the phone: "
        + str_apps
        + ", and the user's command is"
        + task_desc
        + ". Please choose one or more apps that can be used for the task. If it is an app, give me the app name and launch command using json format. For example, <launch app>{'app_name': '滴滴', 'launch_command': 'com.sdu.didi.psnger/com.didi.sdk.app.launch.splash.SplashActivity'}<end>. If it is multiple apps, return a question that describe the name and description of the alternative app starting with<app choose question>to help users choose the desired app."
    )
    print(choose_app_prompt, "kc choose_app_prompt")
    rsp = ask_gpt4v(choose_app_prompt)
    if "error" not in rsp:
        app = rsp["choices"][0]["message"]["content"]
        if "<app choose question>" in app:
            feedback = "请选择一个app"
            answer = "滴滴"
            app = ask_gpt4v(feedback)
        # 匹配<launch app>和<end>之间的内容
        match = re.search(r"<launch app>(.*?)<end>", app)
        if match:
            app_info = match.group(1)
            # 将内容转换为json
            app_json = json.loads(app_info)
            print(app_json, "kc app_json")
            return app_json['launch_command']
        else:
            print("No app information found.")
