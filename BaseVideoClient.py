import os
from videodl import videodl

def main(url):
    video_client = videodl.VideoClient(
        init_video_clients_cfg={
            "DouyinVideoClient": {
                "work_dir": f'E:\\5.16',
                "max_retries": 3,
                "maintain_session": True,
            }
        },
        allowed_video_sources=["DouyinVideoClient"]
    )
    
    acfun_url = url
    video_infos = video_client.parsefromurl(acfun_url)

    to_download = []
    skipped = []

    for info in video_infos:
        # 先初始化 file_path，避免未赋值
        file_path = None
        
        # 情况1：如果 info.save_path 已经是完整文件路径
        if hasattr(info, 'save_path') and info.save_path:
            file_path = info.save_path
        else:
            print(f"警告: {getattr(info, 'identifier', '未知')} 无有效 save_path，跳过。")
            continue
        
        # 自定义文件名（使用自定义名称 + 原扩展名）
        custom_filename = f"{info.identifier}.{info.ext}"
        dirname = os.path.dirname(file_path)
        if not dirname:
            dirname = os.getcwd()
        custom_save_path = os.path.join(dirname, custom_filename)
        
        # 检查自定义文件名是否已存在
        if os.path.exists(custom_save_path):
            skipped.append((info.identifier, custom_save_path))
            print(f"跳过已存在文件: {custom_save_path}")
            continue
        
        # 更新 info 的 save_path 为自定义文件名
        info.save_path = custom_save_path
        to_download.append(info)
        

    # 如果有需要下载的视频，才调用下载
    if to_download:
        video_client.download(to_download)
        for info in to_download:
            print(info.title)
            print(info.source)
            print(info.download_url)
            print(info.save_path)
    else:
        print("所有文件均已存在，无需下载。")
    
    # 打印跳过的文件信息（可选）
    if skipped:
        print("\n以下文件已存在，被跳过:")
        for identifier, path in skipped:
            print(f" {identifier} -> {path}")

if __name__ == "__main__":
    # 假设你有一个URL传入，这里只是示例
    pass