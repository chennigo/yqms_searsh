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

    # 用于存储实际需要下载的视频信息
    to_download = []
    skipped = []

    for info in video_infos:
        
        # 情况1：如果 info.save_path 已经是完整文件路径
        if hasattr(info, 'save_path') and info.save_path:
            file_path = info.save_path
                 
        # 检查文件是否存在
        if os.path.exists(file_path):
            skipped.append((info.title, file_path))
            print(f"跳过已存在文件: {file_path}")
        else:
            to_download.append(info)
    
        # 自定义文件名（使用自定义名称 + 原扩展名）
        custom_filename = f"{info.id}.{info.ext}"
        # 保持原目录结构，只替换文件名
        dirname = os.path.dirname(info.save_path)
        info.save_path = os.path.join(dirname, custom_filename)
        


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
        for title, path in skipped:
            print(f"  {title} -> {path}")

if __name__ == "__main__":
    # 假设你有一个URL传入，这里只是示例
    pass