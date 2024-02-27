可改进的空间
appagent没有做反馈，所以只能一次把任务说清楚。我需要在prompt里面加一个ask_user_question的function
多agent，有一个agent来做rethink。将问题拿来再问llm一下，看看有没有错

只能做一轮的操作吗？
可以做多轮。

如何操作手机
adb的每一个操作的指令比较明确，如果要做成android的app，最好也要在比较明确的指令基础上填充内容
以及要搞清楚，!!安卓app能不能以一种脚本的形式跑代码!!
不行的话就得planb:在电脑上操作

用户如何主动发起会话

## *todo*
- [x] 接上语音接口
- [x] 加上反馈的function
- [ ] 加上启动app的功能, 首先收集手机中的所有app信息，直接使用adb命令打开。因为有些app并不会出现在桌面，所以使用桌面图标的方式会不准确
      如何收集：首先人工使用adb命令收集，并用json表示。缺点：不能打开系统软件
      问题：同一个任务可能有多个软件能够完成，所以要提供给用户选择。比如：我要去虹桥火车站，可能是打车、步行导航、买高铁票等
- [ ] **加上每一个组件功能的文本信息描述**

## 问题
**问题1、语音识别不准确**
description: 语音识别不准确的问题：eg:将虹桥火车站识别为红桥火车站
- [x] way1：过一遍llm，将信息发给llm让它纠正一下

**问题2、按钮lable不准确**
description: 对于手机截图上的按钮lable不准确，会直接影响后续的操作
    <node index="1" text="同意协议并开启" resource-id=""
        class="android.view.View"
        package="com.sdu.didi.psnger" content-desc=""
        checkable="false" checked="false"
        clickable="false" enabled="true"
        focusable="false" focused="false"
        scrollable="false" long-clickable="false"
        password="false" selected="false"
        bounds="[33,2057][1048,2110]" />
这个按钮是可以点击的，但clickable是false
应该怎样lable页面，lable好之后如何调用function操作
父节点或者子节点是true，
用4v玩iphone的，纯xml解析


**问题3、操作生成不准确**
description: 在打车界面，生成的操作是点击“一键叫车”，应该是先在“输入你的目的地”输入目的地

**问题4、操作生成的速度慢**
description: gpt4v的请求慢、adb操作手机的速度慢
4v生成action trace的库，遇到相似任务可以
gpt用于将非结构化的需求转化为结构化的需求

如何理解多agent？隔离上下文
function call


**图片标记的内容**
{
    "description":"图片的内容",
    "task":"",
    "plan":"",
    "step":"",
    "appName":"didi",
    "appFunction":"打车",
    "components":[
        {
            "pic":"url",
            "clickable":"true",
            "function":"",
        },
        {
            "pic":"url",
            "clickable":"true",
            "function":"",
        },
    ]
}