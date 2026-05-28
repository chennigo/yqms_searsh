from wxauto4 import WeChat
import os
from push_error import sc_send
def wxchat(identifier, url, title):
    try:
        wx = WeChat(resize=True, ads=False)
    except Exception as e:
        sc_send(
            'SCT354857T488CbXZlyFhaEmjbW6Uyf8JV',
            '微信自动化初始化失败',
            f'错误详情：{str(e)}'
    )
        print(f"❌ 初始化微信失败：{e}")
        return 
    target = "总群"
    wx.ChatWith(target)
    chatinfo = wx.ChatInfo()
    file_path = os.path.join("E:\\5.16\\DouyinVideoClient", f"{identifier}.mp4")
    
    if not os.path.exists(file_path):
        print(f"错误：文件不存在 -> {file_path}")
        return
    
    file_size = os.path.getsize(file_path)
    try:
        if file_size == 0:
            print(f"错误：文件大小为0，禁止发送 -> {file_path}")
            return
        elif file_size < 1024: 
            print(f"警告：文件极小 ({file_size} bytes)，可能存在问题 -> {file_path}")
    except Exception as e:
         sc_send(
            'SCT354857T488CbXZlyFhaEmjbW6Uyf8JV',
            '发送失败,文件为0',
            f'错误详情：{str(e)}'
        )

    try:
        if chatinfo.get('chat_name') == target:
            wx.SendFiles(file_path)
            wx.SendMsg(
                "成都局贵阳处贵阳北所\n"
                f"{url}{title}\n"
                "类型:其他"
            )
    except Exception as e:
         sc_send(
            'SCT354857T488CbXZlyFhaEmjbW6Uyf8JV',
            '微信消息发送失败',
            f'错误详情：{str(e)}'
        )