from model import ask_gpt4v
import re


def get_questions(app_name):
    switcher = {
        "滴滴": ["您的出发地是？", "您的目的地是？", "您的出发时间是？"],
        "百度地图": ["您的目的地是？", "您的出发地是？", "您偏好的出行方式是？"],
        "微信": [
            "您要发送的消息是？",
            "您要发送给谁呢？",
        ],
        "日历": [
            "日程确切的时间是什么时候呢？",
            "您要添加的具体内容是什么呢",
        ],
    }
    return switcher.get(app_name)


def get_audio_file(app_name, question):
    if app_name == "滴滴":
        if question == "您的目的地是？":
            return "audios/didi/destination.wav"
        if question == "您的出发地是？":
            return "audios/didi/pickup_location.wav"
        elif question == "您的出发时间是？":
            return "audios/didi/pickup_time.wav"
    if app_name == "百度地图":
        if question == "您的目的地是？":
            return "audios/baidu_map/destination.wav"
        if question == "您的出发地是？":
            return "audios/baidu_map/pickup_location.wav"
        elif question == "您偏好的出行方式是？":
            return "audios/baidu_map/travel_mode.wav"
    if app_name == "微信":
        if question == "您要发送的消息是？":
            return "audios/weixin/message.wav"
        if question == "您要发送给谁呢？":
            return "audios/weixin/contact.wav"
    if app_name == "日历":
        if question == "日程确切的时间是什么时候呢？":
            return "audios/calendar/time.wav"
        if question == "您要添加的具体内容是什么呢":
            return "audios/calendar/content.wav"


def collect_info(user_task, app_info):
    # 收集信息
    # 1. 让gpt列出操作需要的步骤
    # 2. 根据步骤和用户的需求生成问题列表
    prompt = "You are a helper designed to help users clarify their intentions when using an app. You need to generate a list of questions based on the user's task: {user_task} and the app they're using to accomplish this task: {app_info}. These questions should be returned in the form of a string array. \n You should carry out the task in four steps:\n 1. Consider the steps a user would take to accomplish {user_task} using {app_info}. Remember, focus on the user's actions within the app, don't get caught up in technical details.\n 2. Identify what additional information is needed to operate the app that the user didn't provide.\n 3. Transform the questions identified in step two into a string array.\n 4. Translate all the questions in the string array into Simplified Chinese and encapsulate the array with <QS><QE> tags.\n For instance, if the user's task is: I want to hail a cab; and the app he's using is: Didi. The questions generated could be: <QS>['你的目的地是哪里?', '你从哪里出发?', '你会携带宠物吗?']<QE>"
    prompt = prompt.replace("{user_task}", user_task).replace("{app_info}", app_info)
    content = [
        {"type": "text", "text": prompt},
    ]
    rsp = ask_gpt4v(content)
    msg = "something error when collect info"
    if "error" not in rsp:
        msg = rsp["choices"][0]["message"]["content"]
        # print(msg,'kc collect info')
    return msg


def format_info(msg):

    # 格式化信息
    pattern = r"<QS>(.*?)<QE>"

    # 使用正则表达式搜索
    match = re.search(pattern, msg)
    questions_list = []
    # 如果匹配成功
    if match:
        # 获取匹配到的内容
        questions_str = match.group(1).strip()
        # 将匹配到的内容转换为列表
        questions_list = eval(questions_str)
    return questions_list


def compose_cmd(task_desc, app, questions_list, answers_list):
    qa = ""
    for i in range(len(questions_list)):
        qa += questions_list[i] + answers_list[i] + "\n"
    print(qa)
    # 组装问题
    task = "我想" + task_desc + "，我使用的app是" + app + "，这是更详细的需求：\n" + qa
    prompt = (
        "你是一个帮助用户操作手机app的智能助手，负责将用户的需求表述地更清晰、流畅。需求表述的基本格式为\n我想：<基本需求>，我使用的app是<用户选择的app>，这是更详细的需求：<针对用户的需求问答>\n请将针对用户的需求问答以陈述的方式表达，并与前面的基本信息及app信息融合，形成通顺的陈述句，以方便后续执行用户的需求。比如：我想去虹桥火车站，我使用的app是滴滴，这是更详细的需求：您的出发地是？复旦大学江湾校区。您的出发时间是？现在出发。您携带宠物吗？不携带。\n返回结果应该是：我要从复旦大学江湾校区去虹桥火车站，现在就出发，不携带宠物。\n注意，你的返回应该是通顺的简体中文。你需要处理的用户需求为："
        + task
    )
    #  "You're an assistant that helps users navigate mobile apps via smart assistants, ensuring that users' requirements are articulated clearly and fluidly. The basic format for expressing requirements is \n 我想：<基本需求>，我使用的app是<用户选择的app>，这是更详细的需求：<针对用户的需求问答>\nPlease present the Q&A specific to user's requirement in a declarative manner, and blend it with the preceding basic information and app information to create a coherent statement, which will ease the subsequent execution of the user's requirement. For instance: 我想去虹桥火车站，我使用的app是滴滴，这是更详细的需求：您的出发地是？复旦大学江湾校区。您的出发时间是？现在出发。您携带宠物吗？不携带。\n返回结果应该是：我要从复旦大学江湾校区去虹桥火车站，现在就出发，不携带宠物。\nNote that your return should be in fluent Simplified Chinese. The user requirement you need to process is:"+task
    content = [
        {"type": "text", "text": prompt},
    ]
    rsp = ask_gpt4v(content)
    msg = "something error when collect info"
    if "error" not in rsp:
        msg = rsp["choices"][0]["message"]["content"]
        print(msg, "kc collect info")
    return msg
