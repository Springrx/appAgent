from model import ask_gpt4v
def collect_info(user_task,app_info):
    # 收集信息
    # 1. 让gpt列出操作需要的步骤
    # 2. 根据步骤和用户的需求生成问题列表
    prompt="You are a helper designed to help users clarify their intentions when using an app. You need to generate a list of questions based on the user's task: {user_task} and the app they're using to accomplish this task: {app_info}. These questions should be returned in the form of a string array. \n You should carry out the task in four steps:\n 1. Consider the steps a user would take to accomplish {user_task} using {app_info}. Remember, focus on the user's actions within the app, don't get caught up in technical details.\n 2. Identify what additional information is needed to operate the app that the user didn't provide.\n 3. Transform the questions identified in step two into a string array.\n 4. Translate each question in the string array into Simplified Chinese.\n For instance, if the user's task is: I want to hail a cab; and the app he's using is: Didi. The questions generated could be: ['你的目的地是哪里?', '你从哪里出发?', '你会携带宠物吗?']"
    prompt = prompt.replace("{user_task}", user_task).replace("{app_info}", app_info)
    print(prompt)
    content = [
    {
        "type": "text",
        "text": prompt
    },]
    rsp = ask_gpt4v(content)
    if "error" not in rsp:
        msg = rsp["choices"][0]["message"]["content"]
        print(msg)
    return msg
collect_info("帮我导航到县医院",'百度地图')
