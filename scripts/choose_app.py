from apps import apps
from model import ask_gpt4v
import re
import json

def choose_app(task_desc: str):
    # 选择app
    str_apps = str(apps)
    choose_app_prompt = (
        "There are apps on the phone: "
        + str_apps
        + ", and the user's command is"
        + task_desc
        + ". Please select one or more apps suitable for this task.Provide the app name and launch command in the format of a json array. For instance, <launch app>[{'app_name': 'Didi', 'launch_command': 'com.sdu.didi.psnger/com.didi.sdk.app.launch.splash.SplashActivity'},{'app_name': 'Baidu Map', 'launch_command': 'com.baidu.BaiduMap/com.baidu.baidumaps.MapsActivity'}]<end>."
    )
    rsp = ask_gpt4v(choose_app_prompt)
    if "error" not in rsp:
        app = rsp["choices"][0]["message"]["content"]
        # 匹配<launch app>和<end>之间的内容
        match = re.search(r"<launch app>(.*?)<end>", app)
        # 将match转换为数组格式
        if match:
            # 如果match的长度为1，则返回match[0]
            app_info = match.group(1)
            # 将单引号替换为双引号以符合JSON格式
            json_str = app_info.replace("'", '"')
            # 使用json.loads()函数将字符串转换为列表
            app_list = json.loads(json_str)
            return app_list
        else:
            print("No app information found.")
            return []
    else:
        print("Error occurred while retrieving app information.")
        return []
