<<<<<<< HEAD
from wxauto4 import WeChat 

# 切换到文件传输助手
def wxchat(id,url,title):
    wx = WeChat(resize=True, ads=False)
    target = "总群"
    wx.ChatWith(target)

    # 查看当前窗口信息
    chatinfo = wx.ChatInfo()
    # print(f"当前窗口信息：{chatinfo}")

    # 发送文件
    if chatinfo.get('chat_name') == target:  # 先判断是否为要发送的人
        wx.SendFiles(f"{id}.mp4")
    wx.SendMsg("成都局贵阳处贵阳北所\n" \
        f"{url+title}\n"
=======
from wxauto4 import WeChat 

# 切换到文件传输助手
def wxchat(video_path,url,title):
    wx = WeChat(resize=True, ads=False)
    target = "总群"
    wx.ChatWith(target)

    # 查看当前窗口信息
    chatinfo = wx.ChatInfo()
    # print(f"当前窗口信息：{chatinfo}")

    # 发送文件
    if chatinfo.get('chat_name') == target:  # 先判断是否为要发送的人
        wx.SendFiles(video_path.mp4)
    wx.SendMsg("成都局贵阳处贵阳北所\n" \
        f"{url+title}\n"
>>>>>>> add63119f5954bcc45dc8ce7f0154aa121f3c5c1
        "类型:其他")