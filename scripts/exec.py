from choose_app import choose_app
from collect_info import collect_info, format_info, compose_cmd, get_questions, get_audio_file
from process_audio import audio_recognize, text_to_speech
from utils import print_with_color
import os
if __name__ == "__main__":
    # 播放"请说出你的需求"
    os.system(f"afplay user_command.wav")
    task_desc = audio_recognize()
    # task_desc = "我要去虹桥火车站"
    print_with_color("用户的需求为:" + task_desc, "white")
    # 识别app
    print_with_color("===========选择app===========", "blue")
    app = choose_app(task_desc)
    print(app)

    # 决定使用哪个app
    if len(app) > 1:
        os.system(f"afplay choose_app.wav")
        # 输入app的顺序，下标从0开始
        choosed_app = input("请选择app")
        app = app[int(choosed_app)]
    else:
        app = app[0]
    print(app)
    app_name=app["app_name"]
    # print_with_color("选择的app是：" + app, "blue")
    print_with_color("===========收集app信息===========", "green")
    questions_list = get_questions(app_name)
    # msg = collect_info(task_desc, app["app_name"])
    # print(msg)
    # questions_list = format_info(msg)
    answers_list = []
    for question in questions_list:
        audio_file=get_audio_file(app_name,question)
        print_with_color(question, "green")
        os.system(f"afplay {audio_file}")
        answer = audio_recognize(refine=False)
        # answer = input()
        answers_list.append(answer)
    while True:
        i=0
        for question, answer in zip(questions_list, answers_list):
            print_with_color(f"问题{i}: {question}", "green")
            print_with_color(f"回答{i}: {answer}", "green")
            i+=1
        if input("是否确认回答？") == "y":
            break
        else:
            index = input("请选择需要重新回答的题目序号")
            answers_list[int(index)] = audio_recognize(refine=False)
            # answers_list[int(index)] = input()

    # 将提问与任务结合为最终的user_command
    task = compose_cmd(task_desc, app["app_name"], questions_list, answers_list)
    print_with_color("最终命令：" + task, "red")
    # 启动app
    print_with_color("===========启动app===========", "white")
    launch_command=app["launch_command"]
    app_name=app["app_name"]
    os.system(f"adb shell am  start -n {launch_command}")
    # 把app的name从app解析出来 app: meituan
    os.system(f"python self_explorer.py --app {app_name} --task_desc {task_desc}")   

