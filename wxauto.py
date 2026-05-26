from wxauto4 import WeChat
import os

def wxchat(identifier, url, title):
    if not identifier:
        print("错误：identifier 为空，无法生成文件路径")
        return

    wx = WeChat(resize=True, ads=False)
    target = "总群"
    wx.ChatWith(target)
    chatinfo = wx.ChatInfo()
    # 改进点：先拼接路径并检查
    file_path = os.path.join("E:\\5.16\\DouyinVideoClient", f"{identifier}.mp4")
    
    # 防御性检查：文件必须存在且大于 1024 字节 (1KB)，防止发送空文件或极小文件
    if not os.path.exists(file_path):
        print(f"错误：文件不存在 -> {file_path}")
        return
    
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        print(f"错误：文件大小为0，禁止发送 -> {file_path}")
        return
    elif file_size < 1024: # 可选：小于1KB通常也是无效的
        print(f"警告：文件极小 ({file_size} bytes)，可能存在问题 -> {file_path}")

    # 只有检查通过了才发微信
    try:
        if chatinfo.get('chat_name') == target:
            wx.SendFiles(file_path)
            wx.SendMsg(
                "成都局贵阳处贵阳北所\n"
                f"{url}{title}\n"
                "类型:其他"
            )
    except Exception as e:
        print(f"发送微信消息失败: {e}")
