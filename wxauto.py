'''
from wxauto4 import WeChat 

# 切换到文件传输助手
def wxchat(aweme_id,url,title):
    wx = WeChat(resize=True, ads=False)
    target = "总群"
    wx.ChatWith(target)

    # 查看当前窗口信息
    chatinfo = wx.ChatInfo()
    # print(f"当前窗口信息：{chatinfo}")

    # 发送文件
    if chatinfo.get('chat_name') == target:  # 先判断是否为要发送的人
        wx.SendFiles(f"E:\\5.16\\{aweme_id}.mp4")
        wx.SendMsg("成都局贵阳处贵阳北所\n"
        f"{url+title}\n"
        "类型:其他")
'''

import os  # 新增：用于路径检查和拼接
from wxauto4 import WeChat 

def wxchat(identifier, url, title):
    # 校验 identifier 是否有效
    if not identifier:
        print("错误：identifier 为空，无法生成文件路径")
        return

    wx = WeChat(resize=True, ads=False)
    target = "总群"
    wx.ChatWith(target)

    chatinfo = wx.ChatInfo()

    if chatinfo.get('chat_name') == target:
        # 使用 os.path 安全拼接路径，避免硬编码反斜杠
        file_path = os.path.join("E:\\5.16\\DouyinVideoClient", f"{identifier}.mp4")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误：文件不存在 -> {file_path}")
            return

        # 发送文件
        wx.SendFiles(file_path)  # 使用已校验的完整路径
        wx.SendMsg(
            "成都局贵阳处贵阳北所\n"
            f"{url}{title}\n"  # 原代码 url+title 可简化
            "类型:其他"
        )