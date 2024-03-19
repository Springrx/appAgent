adb操作命令
启动活动: adb shell am  start -n {activity}(eg: com.tencent.mm/com.tencent.mm.ui.LauncherUI)
查看当前活动名称：adb logcat | findStr -i displayed
(https://blog.csdn.net/weixin_45614253/article/details/113741611)
