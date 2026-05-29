from wxauto4 import WeChat
import os
from push_error import sc_send
from BaseVideoClient import down
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
            print(f"错误：第一次文件大小为0，再次下载 -> {file_path}")
            down(identifier, url)
            # 重新校验大小
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                print("重新下载后文件仍为空，终止流程")
                return
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